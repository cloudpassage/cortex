# OCTOBOX

## OCTO prototype platform

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
    * server compliance graph report renderer
  * Don-Bot internal:
    * Job queue status
    * Bot health (thread health, etc...)
    * Bot running configuration (enabled features)
    * Bot command reference (`donbot help`)
* Quarantine (incomplete)
  * Configuration in bot/octo-conf.yml
  * Quarantine criteria:
    * Server group
    * Event type
    * Event criticality
* IP-Blocker (incomplete)
  * Configuration in bot/octo-conf.yml
    * IP zone name
    * Event type
    * Event criticality
* Critical Events Monitor
  * Send critical events to Slack channel
* Scans to S3 (daily job)
* Events to S3 (daily job)

### Potential expansion

* Candidate features:
  * Events to ticket
    * Filters like Quarantine
    * On match, create issue in Jira, ServiceNow, Remedy
  * Scan server XXX
    * Don-Bot extended feature
    * Similar syntax to "describe server", above
    * Trigger scans for all modules, report results (formatted text) in channel
  * Describe policy
    * Don-Bot extended feature
    * Request policy by ID or name
    * Returns a formatted text document in channel

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
| SCANS_S3_BUCKET        | Name of S3 bucket for scan archive                  |
| EVENTS_S3_BUCKET       | Name of S3 bucket for events archive                |
| HALO_API_KEY           | Read-only API key for Halo                          |
| HALO_API_SECRET_KEY    | Secret corresponding to HALO_API_KEY                |
| HALO_API_KEY_RW        | Read-Write API key for Halo                         |
| HALO_API_SECRET_KEY_RW | Secret corresponding to HALO_API_KEY_RW             |
| SLACK_API_TOKEN        | API token for Slack                                 |
| SLACK_CHANNEL          | Channel Octobot should join and listen.  Octobot will not interact with anyone who is not a member of this channel. |

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
