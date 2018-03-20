Ease of troubleshooting was a matter of consideration in the development of
Cortex.  For instance, none of the containers in Cortex store persistent
data.  If an error is detected and a long-running component (like Don-Bot)
enters a degraded state, the component dies and Docker restarts the container.

If Don-Bot restarts, the bot will place a message in-channel indicating which
component failed before exiting, and a couple of seconds later the Don-Bot
startup message will appear in-channel.

The best place to start looking when troubleshooting a problem is the
application logs, which are managed by Docker. The setup instructions in
README.md encourage the use of journald for logging.  This makes it easy to
manage log volume and to scroll back through a consolidated event stream.
See the manpage for `journald` for more details on viewing log history.

Container-specific logs are easy to get to using the `docker logs` command.
The syntax to follow the logs from a particular container is:
`docker logs -f $CONTAINER_NAME` where ``$CONTAINER_NAME` is the name of the
running container.  The names of the currently-running containers can be seen
in the far-right column of the output of `docker ps`.

If you see error code 137 in connection to a component's malfunction, that
indicates an out-of-memory error.  Strict controls have been put in place to
keep tasks from over-consuming RAM. Memory constraints for specific tasks are in
the docker-compose.yaml file.
