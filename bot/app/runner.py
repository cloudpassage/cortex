#!/usr/bin/python

import base64
import donlib
import io
import octolib
import os
import sys
import threading
import time
# import celery
from halocelery import tasks
from collections import deque


def main():
    global slack_inbound
    global slack_outbound
    global health_string
    global health_last_event_timestamp
    global async_jobs
    async_jobs = deque([])
    health_last_event_timestamp = ""
    health_string = ""
    slack_inbound = deque([])
    slack_outbound = deque([])
    config = donlib.ConfigHelper()
    """First we make sure that all configs are sound..."""
    check_configs(config)
    """Next, we start the Slack ingestion thread..."""
    slack_consumer = threading.Thread(target=slack_in_manager, args=[config])
    slack_consumer.daemon = True
    slack_consumer.start()
    """Now, we start the Slack emitter..."""
    slack_emitter = threading.Thread(target=slack_out_manager, args=[config])
    slack_emitter.daemon = True
    slack_emitter.start()
    """Next, our asynchronous job manager gets crunk"""
    async_mgr = threading.Thread(target=async_manager, args=[config])
    async_mgr.daemon = True
    async_mgr.start()
    """Finally, we start up the Daemon Speaker"""
    halo_enricher = threading.Thread(target=daemon_speaker, args=[config])
    halo_enricher.daemon = True
    halo_enricher.start()
    msg = "Starting Don-Bot v%s\nName is set to %s" % (donlib.__version__,
                                                       config.slack_username)
    print(msg)
    msg = "Don-Bot sends general notifications to #%s" % config.slack_channel
    print(msg)
    if config.monitor_events == "yes":
        print("Starting Halo event monitor")
        halo_collector = threading.Thread(target=event_connector, args=[config])
        halo_collector.daemon = True
        halo_collector.start()

    while True:
        s_consumer = " Slack consumer alive: %s" % str(slack_consumer.is_alive())
        s_emitter = "  Slack emitter alive: %s" % str(slack_emitter.is_alive())
        h_enricher = "  Halo enricher alive: %s" % str(halo_enricher.is_alive())
        a_manager = "  Async job manager alive: %s" % str(async_mgr.is_alive())
        if config.monitor_events == "yes":
            h_events = "  Halo event monitor alive: %s\n  Last event: %s" % (
                halo_collector.is_alive(), health_last_event_timestamp)
        else:
            h_events = ""
        health_string = "\n".join([s_consumer, s_emitter, h_enricher, a_manager,
                                   h_events])
        die_if_unhealthy(config.slack_channel)
        time.sleep(30)


def die_if_unhealthy(slack_channel):
    if "False" in health_string:
        msg = health_string
        msg += "\n\nI'm feeling sick.  I'm going to die.  Be back in a few..."
        channel = slack_channel
        sad_note = (channel, msg)
        slack_outbound.append(sad_note)
        time.sleep(5)
        sys.exit(2)
    else:
        pass


def event_connector(config):
    global health_last_event_timestamp
    halo = donlib.Halo(config, str(health_string), tasks)
    events = donlib.HaloEvents(config)
    quarantine = octolib.Quarantine()
    ipblock = octolib.IpBlockCheck()
    # We add a short delay in case of time drift between container and API
    time.sleep(10)
    while True:
        for event in events:
            quarantine_check = quarantine.should_quarantine(event)
            ip_block_check = ipblock.should_block_ip(event)
            health_last_event_timestamp = event["created_at"]
            if donlib.Utility.event_is_critical(event):
                print("EVENT_CONNECTOR: Critical event detected!")
                event_fmt = donlib.Formatter.format_item(event, "event")
                slack_outbound.append((config.slack_channel, event_fmt))
            if quarantine_check is not False:
                async_jobs.append((config.slack_channel,
                                   halo.quarantine_server(event)))
            if ip_block_check is not False:
                target_ip = ipblock.extract_ip_from_event(event)
                target_zone_name = ipblock.ip_zone_name
                async_jobs.append((config.slack_channel,
                                   halo.add_ip_to_blocklist(target_ip,
                                                            target_zone_name)))


def daemon_speaker(config):
    while True:
        celery_tasks = tasks
        halo = donlib.Halo(config, str(health_string), celery_tasks)
        try:
            message = slack_inbound.popleft()
            channel = message["channel"]
            halo_query, target = donlib.Lexicals.parse(message)
            halo_results = halo.interrogate(halo_query, target)
            print "DAEMON_SPEAKER: Results object type:%s" % type(halo_results)
            if isinstance(halo_results, (str, unicode)):
                slack_outbound.append((channel, halo_results))
            else:
                print "DAEMON_SPEAKER: queueing up async job"
                async_jobs.append((channel, halo_results))
        except IndexError:
            time.sleep(1)
    return


def async_manager(config):
    while True:
        try:
            job = async_jobs.popleft()
            if job[1].ready():
                if job[1].successful():
                    outbound_construct = (job[0], job[1].result)
                    slack_outbound.append(outbound_construct)
                    job[1].forget()
                elif job[1].failed():
                    outbound_construct = (job[0], "REQUEST FAILED")
                    slack_outbound.append(outbound_construct)
                    job[1].forget()
                else:  # If not successful and not failed, throw it back.
                    async_jobs.append(job)
            else:
                async_jobs.append(job)
                time.sleep(1)
        except IndexError:
            time.sleep(1)


def slack_in_manager(config):
    slack = donlib.Slack(config)
    for message in slack:
        print("Message in slack consumer")
        slack_inbound.append(message)


def slack_out_manager(config):
    slack = donlib.Slack(config)
    while True:
        try:
            message = slack_outbound.popleft()
            try:
                # Attempt to decode from Base64.
                if "\n" in message[1]:
                    raise TypeError("Detected plaintext response...")
                dec_msg = base64.decodestring(message[1])
                print("Detected Base64-encoded file...")
                slack.send_file(message[0], io.BytesIO(dec_msg).read(),
                                "Daemonic File")
            except TypeError as e:
                print(e)
                slack.send_report(message[0], message[1],
                                  "Daemonic Report")
        except IndexError:
            time.sleep(1)


def check_configs(config):
    halo = donlib.Halo(config, "", "")
    if halo.credentials_work() is False:
        print("Halo credentials are bad!  Exiting!")
        sys.exit(1)

    # If NOSLACK env var is set, don't go any further!
    if os.getenv("NOSLACK"):
        noslack_hold()

    if config.sane() is False:
        print("Configuration is bad!  Exiting!")
        sys.exit(1)

    slack = donlib.Slack(config)
    if slack.credentials_work() is False:
        print("Slack credentials are bad!  Exiting!")
        sys.exit(1)

def noslack_hold():
    msg = ("Slack integration is disabled.  "
           "Interact with Halo using:"
           " 'docker exec -it octo-bot python /app/interrogate.py'")
    while True:
        print(msg)
        time.sleep(3600)

if __name__ == "__main__":
    main()
