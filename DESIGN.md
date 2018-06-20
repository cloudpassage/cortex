# Cortex design

## Design notes

Cortex is a collection of Docker containers managed by docker-compose.  All long-running components are stateless and configured to restart in the event of failure, eliminating the need for human interaction to correct component failure.

### donbot

Users can interact with Cortex via SSH or Slack integration. Both of these communication paths exist via the `donbot` component.  The `donbot` component is a long-running container within the Cortex application.  Most of the `donbot` component's human interaction functionality is delivered by queueing jobs for the `celeryworker` component, via the `rabbitmq` component.  The task definitions used in the `celeryworker` component are included in the `donbot` component at container image build time. See https://github.com/cloudpassage/cortex/blob/master/docker-compose.yml for more information.

### donbot interaction lifecycle (https://github.com/cloudpassage/don-bot):

1. User messages `donbot` in Slack: *donbot servers in group DONBOT*
1. Message received in channel by `app/runner.py: slack_in_manager()`, placed in `slack_inbound` FIFO.
1. The `donbot` component pulls the message from `slack_inbound` FIFO and processes in `app/runner.py: daemon_speaker()`
1. The `daemon_speaker()` function calls `donlib.Lexicals.parse()` to determine interaction type and to extract metadata from the user interaction, then calls `halo.interrogate()`.
1. The `halo.interrogate()` function can perform three different kinds of tasks:
    * `Synchronous`, which are expected to return results fast, and are blocking, though very briefly.
    * `Asynchronous-containerized`, which are triggered via the `celeryworker` component and use short-running containers to produce the information the user requests.
    * `Asynchronous-native`, which uses Python code that ships in the `celeryworker` itself, which in turn produces the information that the user requests.
1. If the `halo.interrogate()` function creates a synchronous task, it places the results of the task directly into the `slack_outbound` FIFO queue.  In the case of an asynchronous task (native or containerized), an `AsynchronousTaskObject` (which is a Celery construct) is placed in the `async_jobs` FIFO queue.
1. The `async_manager()` thread continually checks the `AsynchronousTaskObject`s in the `async_jobs` queue and when one completes, it is de-queued and the results are placed in the `slack_outbound` queue.
1. The `slack_out_manager()` thread makes some determination of the message type (unpacking base64-encoded messages when appropriate) and sends the message via Slack, back to the user or channel from which it originated.

### celeryworker

The `celeryworker` component is responsible for dispatching and managing the results for `asynchronous-native` and `asynchronous-containerized` tasks. Most of the functionality in this component is facilitated by the `halocelery` library which is located at (https://github.com/cloudpassage/halocelery)

### redis

The `redis` component holds the results of completed asynchronous tasks.

### scheduler

The `scheduler` component is responsible for triggering timed tasks (like cron
jobs), like the event and scan shippers.  This long-running container
builds its scheduled job configuration based on configuration files.
To add tasks to the scheduler, you should add correctly-formatted configuration
files to `config/enabled` in the cortex repository and restart the scheduler
with `docker restart scheduler`. For details on the file format required for
custom scheduled tasks, see the `example.conf` file in the halocelery
repository [here](https://github.com/cloudpassage/halocelery).

### flower

Flower is a web interface for managing Celery.  This is implemented in Cortex to give us access to task history via the *donbot tasks* command and is not, by default, exposed outside of the Docker-internal network.

## Adding functionality

Adding new functionality to Cortex is designed to be straightforward, versatile, and easy to reliably deliver.

1. Create a Docker container image which produces the desired information, encoded in base64, via the container's stdout.  Create this as a completely separate repository in Github and Dockerhub, not in the Cortex repository.  Make sure that your end-to-end testing is rock solid, and you use non-default tags for your codebase and docker image, so you can precisely pin the task in Cortex configuration.
2. In project https://github.com/cloudpassage/halocelery
   - create a task definition in the `halocelery` library (`halocelery/tasks.py` and `halocelery/apputils/containerized.py`).
3. In project https://github.com/cloudpassage/don-bot
   - add an entry into `app/donlib/lexicals.py: get_message_type()` as well as tests in `app/test/unit/test_unit_lexicals.py`.  _DO NOT SKIP ON THE TESTS!_
   - add an entry to `app/donlib/halo.py: interrogate()` to call the new task you created in the prior step.
4. Tag a new version of `donbot` and `halocelery`.
5. Re-pin the `don-bot` and `halocelery` libraries in cortex/docker-compose.yml:
   - `&default_halocelery_version docker.io/halotools/halocelery:<version>`
   - `&default_donbot_version docker.io/halotools/don-bot:<version>`
6. Update the halocelery image version in Dockerfile (https://github.com/cloudpassage/don-bot)
