# Get the halocelery component
FROM docker.io/halotools/python-sdk:ubuntu-16.04_sdk-1.0.6 as downloader
MAINTAINER toolbox@cloudpassage.com

ARG HALOCELERY_BRANCH=v0.4.4

RUN apt-get update && \
    apt-get install -y \
        git

WORKDIR /app/

RUN echo "Target branch for this build: $HALOCELERY_BRANCH"

RUN git clone https://github.com/ashmastaflash/halocelery

RUN cd halocelery && \
    git archive --verbose --format=tar.gz -o /app/halocelery.tar.gz $HALOCELERY_BRANCH


#####################################

FROM docker.io/halotools/python-sdk:ubuntu-16.04_sdk-1.0.6
MAINTAINER toolbox@cloudpassage.com

ENV HALO_CELERY_VERSION=v0.4.1

ENV SLACK_ICON_URL=http://www.cloudpassage.com/wp-content/uploads/2016/12/don-operator.png
ENV HALO_API_HOSTNAME=api.cloudpassage.com
ENV HALO_API_PORT=443

# Up to root to add additional packages
USER root

RUN pip install \
    boto3==1.4.3 \
    celery[redis]==4.0.2 \
    docker==2.6.1 \
    flower==0.9.1 \
    pytest==2.8.0 \
    pytest-flake8==0.1 \
    pytest-cover==3.0.0 \
    python-magic==0.4.15 \
    slackclient==1.0.2

# Drop in the app code
COPY app/ /app/
COPY octo_conf.yml /

# Setup for manual library installation
RUN mkdir /src/
WORKDIR /src/


COPY --from=downloader /app/halocelery.tar.gz /src/halocelery/halocelery.tar.gz

RUN cd halocelery && \
    tar -zxvf ./halocelery.tar.gz && \
    cd /src/ && \
    mv ./halocelery /app


WORKDIR /app

RUN pip install -r requirements.txt

# Now take ownership and drop to non-root user
RUN chown -R ${APP_USER}:$APP_GROUP /app

USER ${APP_USER}

RUN py.test

WORKDIR /app


CMD ["python", "/app/runner.py"]
