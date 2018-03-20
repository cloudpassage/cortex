# OCTOBOX

## OCTO prototype platform

This integration package is designed to get you up and running with Halo
_really_ fast.  It's also been designed with the idea that you want to build
your own environment-specific integrations, and thusly won't be using OCTOBOX
forever.  Many components in OCTOBOX can be implemented independently, using
your favorite CI (or other automation) tools.  So use OCTOBOX when you start
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
* Quarantine
  * Configuration in bot/octo-conf.yml
  * Quarantine criteria:
    * Server group
    * Event type
    * Event criticality
* IP-Blocker
  * Configuration in bot/octo-conf.yml
    * IP zone name
    * Event type
    * Event criticality
* Critical Events Monitor
  * Send critical events to Slack channel
* Scans to S3 (daily job)
  * Send all scans for prior day to S3
* Events to S3 (daily job)
  * Send all events from prior day to S3


### Requirements

* docker-compose (https://docs.docker.com/compose/install/)

### Use

* Clone this repository
* Navigate to the root directory of this repository
* Set these environment variables:

| Variable               | Purpose                                             |
|------------------------|-----------------------------------------------------|
| AWS_ACCESS_KEY_ID      | API key ID from Amazon AWS                          |
| AWS_SECRET_ACCESS_KEY  | Secret key corresponding to AWS_ACCESS_KEY_ID       |
| AWS_ROLE_NAME          | (Optional) Role to assume via STS, for cross-account inventory.|
| AWS_ACCOUNT_NUMBERS    | (Optional) Semicolon-delimited list of account numbers having `AWS_ROLE_NAME` |
| SCANS_S3_BUCKET        | Name of S3 bucket for scan archive                  |
| EVENTS_S3_BUCKET       | Name of S3 bucket for events archive                |
| HALO_API_KEY           | Read-only API key for Halo                          |
| HALO_API_SECRET_KEY    | Secret corresponding to HALO_API_KEY                |
| HALO_API_KEY_RW        | Read-Write API key for Halo                         |
| HALO_API_SECRET_KEY_RW | Secret corresponding to HALO_API_KEY_RW             |
| SLACK_API_TOKEN        | API token for Slack                                 |
| SLACK_CHANNEL          | Channel Octobot should join and listen.  Octobot will not interact with anyone who is not a member of this channel. |

* For more information on `AWS_ROLE_NAME` and `AWS_ACCOUNT_NUMBERS` settings, refer to
https://github.com/ashmastaflash/ec2-halo-delta

* Confirm that the configuration for ip blocker and quarantine in
`octo-box/bot/octo_conf.yml` matches your environment, especially regarding
group names, ip list names, and event types.

* As a user who has sufficient access to run Docker containers:
`docker-compose up -d --build`

### Using without Slack

If you prefer not to use Slack, un-comment the line in docker-compose.yml that
contains `NOSLACK: true`.  This will cause octo-bot to stop and loop before
attempting to connect to Slack.  To interact with Halo from the command line,
SSH into the host running docker-compose and run this:
`sudo docker exec -it octo-bot python /app/interrogate.py`.  You will then
be dropped into a shell where you can interact with octo-box.  Type `help` and
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
