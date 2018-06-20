# CORTEX

## CORTEX integration platform

This integration package is designed to get you up and running with Halo
_really_ fast.  It's also been designed with the idea that you want to build
your own environment-specific integrations, and thusly won't be using CORTEX
forever.  Many components in CORTEX can be implemented independently, using
your favorite CI (or other automation) tools.  So use CORTEX when you start
out with Halo, and as you build your own environment-specific automation, you
can peel off and re-implement specific components (the Halo-EC2 footprint delta
reporter and scan/event exporters, for instance) in a way that makes the most
sense for your environment, using your favorite automation tools.


### Features

* Don-Bot (extended version)
  * halo-oriented interactions:
    * list groups
    * list servers
    * list servers in group
    * find server by IP
    * describe server
      * server facts
      * server EC2 metadata
      * server issues
      * server events
    * group firewall policy graph renderer
    * Halo-EC2 footprint delta reporter
      * Produce a CSV with all EC2 workloads in an account which are not protected by Halo.
      * Support STS-based cross-account access.  Inventory multiple AWS accounts.
  * Don-Bot internal:
    * Job queue status
    * Bot health (thread health, etc...)
    * Bot running configuration (enabled features)
    * Bot command reference (`donbot help`)
* Quarantine (https://github.com/cloudpassage/don-bot/blob/master/QUARANTINE.md)
  * Configuration in cortex_conf.env
  * Quarantine criteria:
    * Server group
    * Event type
    * Event criticality
* IP-Blocker(https://github.com/cloudpassage/don-bot/blob/master/IP_BLOCKER.md)
  * Configuration in cortex_conf.env
    * IP zone name
    * Event type
    * Event criticality
* Critical Events Monitor
  * Send critical events to Slack channel
* Scans to S3 (daily task)
  * Send all scans for prior day to S3 (see `scheduler configuration`, below)
* Events to S3 (daily task)
  * Send all events from prior day to S3 (see `scheduler configuration`, below)


### Requirements

* docker-compose (https://docs.docker.com/compose/install/)
* For AWS EC2 instance, it is recommended to use:
  * Ubuntu 16.04
  * t2.medium (Variable ECUs, 2 vCPUs, 2.3 GHz, Intel Broadwell E5-2686v4, 4
    GiB memory, EBS only)
* API keys for adjacent systems (AWS, Slack, Halo)
  * Access requirements by feature:
    * Scans and events to S3
      * Halo read-only API keys (general requirement for basic Cortex operation-
        see table below)
      * Target S3 buckets (`SCANS_S3_BUCKET`, `EVENTS_S3_BUCKET`) for receiving
      scans and events must exist; this integration does not create S3 buckets.
      * API keys must be able to create and update files in target S3 buckets.
    * Halo EC2 Delta reporter
      * Read-only Halo API keys (general requirement for basic Cortex operation-
        see table below)
      * AWS API keys must be able to read EC2 metadata. For scanning multiple
        accounts, read the [implementation notes](https://github.com/cloudpassage/ec2-halo-delta#implementation-notes)
    * Quarantine, IP Blocker:
      * Halo administrative-level API keys are required for both Quarantine and IP Blocker (see `HALO_API_KEY_RW` and `HALO_API_SECRET_KEY_RW`, below).
      * Duplicated group names are not supported for monitored or quarantine group.  See [Quarantine docs](https://github.com/cloudpassage/don-bot/blob/master/QUARANTINE.md)
      * Duplicated group names for monitored groups in IP Blocker configuration are not
      supported.  See [IP Blocker documentation](https://github.com/cloudpassage/don-bot/blob/master/IP_BLOCKER.md)
      for details.
    * Slack integration
      * CloudPassage Halo read-only API keys (a default requirement for basic Cortex operation)
      * A [Slack bot user API token](https://api.slack.com/docs/token-types#bot)
      is required to enable don-bot.


### Setup and Use

* Create a virtual machine or cloud instance for hosting Cortex, which meets or
exceeds instance sizing in `Requirements`, above.
* Install [docker-ce](https://docs.docker.com/install/linux/docker-ce/ubuntu/)
and [docker-compose](https://docs.docker.com/compose/install/) on the Cortex
instance you just created.
* Use git to clone this repository into the Cortex instance.
* Navigate to the root directory of the cloned repository.
* Set these environment variables:

| Variable               | Purpose                                             |
|------------------------|-----------------------------------------------------|
| AWS_ACCESS_KEY_ID      | API key ID from Amazon AWS                          |
| AWS_SECRET_ACCESS_KEY  | Secret key corresponding to AWS_ACCESS_KEY_ID       |
| AWS_ROLE_NAME          | (Optional) Role to assume via STS, for cross-account inventory.|
| AWS_ACCOUNT_NUMBERS    | (Optional) Semicolon-delimited list of account numbers having `AWS_ROLE_NAME` |
| HALO_API_KEY           | Read-only API key for Halo                          |
| HALO_API_SECRET_KEY    | Secret corresponding to HALO_API_KEY                |
| HALO_API_KEY_RW        | Read-Write API key for Halo (Only required if you're using IP-Blocker and Quarantine) |
| HALO_API_SECRET_KEY_RW | Secret corresponding to HALO_API_KEY_RW (Only required if you're using IP-Blocker and Quarantine) |
| SLACK_API_TOKEN        | (optional) API token for Slack                      |
| SLACK_CHANNEL          | (optional) Channel Donbot should join and listen. Donbot will not interact with anyone who is not a member of this channel. |
| HTTPS_PROXY_URL        | If server routes through a proxy. Format is ip:port |

* For more information on `AWS_ROLE_NAME` and `AWS_ACCOUNT_NUMBERS` settings,
refer to https://github.com/cloudpassage/ec2-halo-delta

* Confirm that the configuration for ip blocker and quarantine in
`cortex_conf.yml` (found in the root directory of this repository) matches your
environment's requirements, especially regarding group names, ip list names, and
event types.

* As a user who has sufficient access to run Docker containers:
`docker-compose --compatibility up -d --build`

### Scheduler Configuration

Cortex has a built-in task scheduler for performing regular batch-type
integrations. Two such task definitions are included with Cortex, and are
very easy and straightforward to configure:

* `scheduled_events_to_s3.conf`
  * Copy the `scheduled_events_to_s3.conf` file from `config/available/` to the
  `config/enabled/` directory.
  * Open the `config/enabled/scheduled_events_to_s3.conf` file with your
  favorite editor and set the value for `AWS_S3_BUCKET` to the name of the
  S3 bucket you would like to send your Halo events to.
  * Finally, restart the Cortex scheduler by running `docker restart scheduler`.
  * Confirm that the scheduler picked up the configuration by running
  `docker logs scheduler` and looking for the task's configuration to be
  printed. (see below section on scheduler logs)

* `scheduled_scans_to_s3.conf`
  * Same process as `scheduled_events_to_s3.conf`; both configuration files are
  nearly identical. Copy the file to `config/enabled/`, set the `AWS_S3_BUCKET`
  variable, and restart the scheduler, as described above.

When examining scheduler startup logs (docker logs scheduler) to confirm the
correct consumption of scheduled task configuration, this is similar to what
you'll see:

```

ConfigManager: Parsing config file: /etc/config/scheduled_events_to_s3.conf
ConfigManager: Parsing config file: /etc/config/scheduled_scans_to_s3.conf
Scheduled tasks:
Task: scans_to_s3
Container image: docker.io/halotools/halo-scans-archiver:feature_CS-554
Retries: 5
Schedule:
	Minute: 01
	Hour: 12
	Day of week: *
	Day of month: *
	Month of year: *
===
Task: events_to_s3
Container image: docker.io/halotools/halo-events-archiver:feature_CS-555
Retries: 5
Schedule:
	Minute: 01
	Hour: 12
	Day of week: *
	Day of month: *
	Month of year: *

```

Notice that the ConfigManager parses two config files in the above example,
then prints the basic task configuration for both.  This output is useful to
confirm the correct consumption of basic task configuration. Any files which
are found in the `config/enabled/` directory which don't contain the correct
configuration sections will be ignored.

### Using without Slack

If you prefer not to use Slack, un-comment the line in docker-compose.yml that
contains `NOSLACK: true`.  This will cause donbot to stop and loop before
attempting to connect to Slack.  To interact with Halo from the command line,
SSH into the host running docker-compose and run this:
`sudo docker exec -it don-bot python /app/interrogate.py`.  You will then
be dropped into a shell where you can interact with cortex.  Type `help` and
press enter for details on available comands.  Output that is typically
returned in image form will come back as base64-encoded text.  You can
copy/paste from the terminal window into a text editor, then run it through
the decoding process (`cat FILE_WITH_BASE64_DATA | base64 -D > output.png`)
to get the original image.

### Docker host configuration recommendations

The use of journald for logging in Docker is strongly encouraged. The containers
in this application produce verbose logs, and it is best to send them to
journald instead of the default Docker logging mechanism. Instructions for
configuring Docker's logging driver can be found [here](https://docs.docker.com/engine/admin/logging/journald/#usage).
