# Octobox design

## Design notes

Octobox is a collection of Docker containers managed by docker-compose.  All long-running components are stateless and configured to restart in the event of failure, eliminating the need for human interaction to correct component failure.

### octobot

Users can interact with Octobox via SSH or Slack integration. Both of these communication paths exist via the `octobot` component.  The `octobot` component is a long-running container within the Octobox application.  Most of the `octobot` component's human interaction functionality is delivered by queueing jobs for the `celeryworker` component, via the `rabbitmq` component.  The task definitions used in the `celeryworker` component are included in the `octobot` component at container image build time.  See bot/Dockerfile for more information.

Example interaction lifecycle:

1. User messages `octobot` in Slack: *donbot servers in group OCTOBOX*
1. Message received in channel by `bot/app/runner.py: slack_in_manager()`, placed in `slack_inbound` FIFO.
1. The `octobot` component pulls the message from `slack_inbound` FIFO and processes in `bot/app/runner.py: daemon_speaker()`
1. The `daemon_speaker()` function calls `donlib.Lexicals.parse()` to determine interaction type and to extract metadata from the user interaction, then calls `halo.interrogate()`.
1. The `halo_interrogate()` function can perform three different kinds of tasks:
    * `Synchronous`, which are expected to return results fast, and are blocking, though very briefly.
    * `Asynchronous-containerized`, which are triggered via the `celeryworker` component and use short-running containers to produce the information the user requests.
    * `Asynchronous-native`, which uses Python code that ships in the `celeryworker` itself, which in turn produces the information that the user requests.
1. If the `halo_interrogate()` function creates a synchronous task, it places the results of the task directly into the `slack_outbound` FIFO queue.  In the case of an asynchronous task (native or containerized), an `AsynchronousTaskObject` (which is a Celery construct) is placed in the `async_jobs` FIFO queue.  
1. In the case of the example message above, an `asynchronous-native` task is created.
1. The `asynchronous-native` task causes a message to be placed into the `rabbitmq` component, which is in turn picked up by the `celeryworker` component.
1. The `celeryworker` component works the task to completion, places the full results in the `redis` component, and the corresponding `AsynchronousTaskObject` is marked as being completed.
1. The `async_manager()` thread continually checks the `AsynchronousTaskObject`s in the `async_jobs` queue and when one completes, it is de-queued and the results are placed in the `slack_outbound` queue.
1. The `slack_out_manager()` thread makes some determination of the message type (unpacking base64-encoded messages when appropriate) and sends the message via Slack, back to the user or channel from which it originated.

### celeryworker

The `celeryworker` component is responsible for dispatching and managing the results for `asynchronous-native` and `asynchronous-containerized` tasks.  Most of the functionality in this component is facilitated by the `halocelery` library, located [here](https://github.com/ashmastaflash/halocelery).

### redis

The `redis` component holds the results of completed asynchronous tasks.

### scheduler

The `scheduler` component is responsible for triggering timed tasks (like cron jobs), like the event and scan shippers.  This long-running container incorporates the task definitions from the `halocelery` library.

### flower

Flower is a web interface for managing Celery.  This is implemented in Octobox to give us access to task history via the *donbot tasks* command and is not, by default, exposed outside of the Docker-internal network.

## Adding functionality

Adding new functionality to Octobox is designed to be straightforward, versatile, and easy to reliably deliver.

1. Create a Docker container image which produces the desired information, encoded in base64, via the container's stdout.  Create this as a completely separate repository in Github and Dockerhub, not in the Octobox repository.  Make sure that your end-to-end testing is rock solid, and you use non-default tags for your codebase and docker image, so you can precisely pin the task in Octobox configuration.
1. Add an entry into `app/donlib/lexicals.py: get_message_type()` as well as tests in `bot/app/test/unit/test_unit_lexicals.py`.  _DO NOT SKIP ON THE TESTS!_
1. Create a task definition in the `halocelery` library (`halocelery/tasks.py` and `halocelery/apputils/containerized.py`) to support running the container image you created in the first step.
1. Add an entry to `bot/app/donlib/halo.py: interrogate()` to call the new task you created the prior step.
1. Tag a new version of `halocelery` and expand the build instructions in the `fiery-boat` repository to accommodate the new github repository tag you just created.  The `fiery-boat` repository containerizes the `halocelery` library for consumption in other Octobox components.
1. Re-pin the `fiery-boat` and `halocelery` libraries in the following places:
    * docker-compose.yml:
        * flower
        * celeryworker
        * scheduler
    * bot/Dockerfile (improvement: this needs to be parameterized in docker-compose.yml)
