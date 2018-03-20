FROM docker.io/ashmastaflash/fiery-boat
MAINTAINER toolbox@cloudpassage.com

RUN pip install flask

USER root
COPY app/ /app/
RUN chown -R ${APP_USER}:${APP_GROUP} /app

USER ${APP_USER}
ENV FLASK_APP=octoapp.py

CMD flask run --host=0.0.0.0
