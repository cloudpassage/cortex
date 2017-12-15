FROM docker.io/halotools/don-bot:v0.17.0
MAINTAINER toolbox@cloudpassage.com

ENV HALO_SDK_VERSION=1.0.1
ENV HALO_CELERY_VERSION=v0.4.1
ENV FIREWALL_GRAPH_VERSION=v0.1

ENV SLACK_ICON_URL=http://www.cloudpassage.com/wp-content/uploads/2016/12/don-operator.png
ENV HALO_API_HOSTNAME=api.cloudpassage.com
ENV HALO_API_PORT=443

# Up to root to add additional packages
USER root

RUN apk add -U --no-cache \
    gcc==5.3.0-r0 \
    graphviz==2.38.0-r5 \
    graphviz-dev==2.38.0-r5 \
    libmagic==5.27-r0 \
    linux-headers==4.4.6-r1 \
    musl-dev==1.1.14-r16 \
    python==2.7.12-r0 \
    python-dev==2.7.12-r0 \
    py-pip==8.1.2-r0


RUN pip install \
    boto3==1.4.3 \
    celery[redis]==4.0.2 \
    cloudpassage==${HALO_SDK_VERSION} \
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


# Install Firewall Graph library
RUN git clone https://github.com/cloudpassage-community/firewall-graph
RUN cd firewall-graph && \
    git checkout ${FIREWALL_GRAPH_VERSION} && \
    pip install .

RUN git clone https://github.com/ashmastaflash/halocelery
RUN cd halocelery && \
    git checkout ${HALO_CELERY_VERSION} && \
    cd ../ && \
    mv ./halocelery /app


WORKDIR /app

RUN pip install -r requirements.txt

# Now take ownership and drop to non-root user
RUN chown -R ${APP_USER}:$APP_GROUP /app

USER ${APP_USER}

RUN py.test

WORKDIR /app


CMD ["python", "/app/runner.py"]
