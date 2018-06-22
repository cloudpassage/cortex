Changelog
=========

v1.1
----

New
~~~

- Include policy for monitoring scheduled tasks. [Ash Wilson]

  A policy has been included at policies/cortex-scheduler.json to
  aid in monitoring Cortex logs for failed scheduled task execution.

  Instructions for implementation have been included in README.md, under
  the heading, "Monitoring Cortex's scheduled tasks"

  Closes #55

- Updated various components. [Ash Wilson]

  Updated halocelery to v0.8.  Enables file-based configuration for scheduler.  Introduce generic launch tasks for scheduled and ad-hoc tasks.
  Closes #52

  Updated don-bot to v0.19.  Don-bot now uses halocelery's generic container launch tasks for all ad-hoc containerized tasks.  Improvements to Slack integration allow more graceful handling of errors when communicating with Slack's API.  This version of don-bot is based on halocelery v0.8.
  Closes #50

  Pinned versions for events shipper and scan shipper (see scheduled_events_to_s3.conf and scheduled_scans_to_s3.conf in config/available/) to v0.12 and v0.18, respectively.
  Closes #49

- File-based configuration for scheduler. [Ash Wilson]

  Scheduled task configuration is now defined in configuration files.
  Details in README.md and DESIGN.md.

  Configuration files for tasks which ship events and scans to S3 added at
  config/available/.

  Supports HALO_API_HOSTNAME environment variable.
  Closes #46

- Added interrogate.py, a CLI tool for interrogating Halo. [Ash Wilson]

Changes
~~~~~~~

- Remove 'server compliance graph' feature.  Add 'ec2 halo footprint
  csv'. [Ash Wilson]

- Documentation improvements. [Ash Wilson]

- Added better support for Slack-less operation, and documentation for
  use without Slack. [Ash Wilson]

- IP Blocker removes IP from list after an hour. [Ash Wilson]

- Added job-list page in app server. [Ash Wilson]

- Adding IP block and Quarantine functionality. [Ash Wilson]

Fix
~~~

- Remove octobot. [Jye Lee]

Other
~~~~~

- Rev donbot to 0.18.0 and halocelery to 0.7.0. [Jye Lee]

- TEST: add HTTPS_PROXY as a env var. [Jye Lee]

- Rev halocelery to v0.6.0. [Jye Lee]

- Rev donbot to v0.17.6. [Jye Lee]

- Doc change: remove wrong link. [Jye Lee]

- Rev donbot to v0.17.5. [Jye Lee]

- Test maintenance: rev donbot to v0.17.4. [Jye Lee]

- Rev halocelery to 0.5.0. [Jye Lee]

- Set service mem limit to 256mb. [Jye Lee]

- Add mem limit as a parameter to halocelery. [Jye Lee]

- Add ubuntu 16.04 vm specs in recommendation. [Jye Lee]

- Add travis test to make sure halocelery version is consistent
  throughout don-bot flower celeryworker scheduler. [Jye Lee]

  when built using docker-compose up -d --build

  Files added:
  Add .travis.yml
  Add requirements.txt
  Add test/integration/test_integration_version_parity.py

- Changed don-bot version to v0.17.3 added SUPPRESS_EVENTS_IN_CHANNEL to
  cortex_conf.env. [Hana Lee]

- Updated readme. [Hana Lee]

- Updated readme. [Hana Lee]

- Fixed merge conflict. [Hana Lee]

- Rename confusing octobot to donbot. remove fieryboat (deprecated)
  included in halocelery now. update to docker-compose v3.4 to use
  extension fields. [Jye Lee]

- Added cortex_conf.env. [Hana Lee]

- Rename confusing octobot to donbot. remove fieryboat (deprecated)
  included in halocelery now. update to docker-compose v3.4 to use
  extension fields. [Jye Lee]

- Update design.md. [Jye Lee]

- 1. Removed appserver 2. Removed web 3. Updated halo_scans_archiver
  image version to 0.17 4. Updated README (octo to cortex) [Jye Lee]

- Revert "name change from octo to cortex" [mong2]

- TEST: name change from octo to cortex. [Jye Lee]

- Remove bot, migrated to don-bot. [Jye Lee]

- Switching to halocelery. [Hana Lee]


