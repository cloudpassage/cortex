# OCTOBOX

## OCTO prototype platform

### Features:

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

### Potential expansion:

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
