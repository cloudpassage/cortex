FROM docker.io/ashmastaflash/fiery-boat
MAINTAINER toolbox@cloudpassage.com

RUN pip install flask

COPY app/ /app/
RUN chown -R ${APP_USER}:${APP_GROUP} /app

ENV FLASK_APP=octoapp.py

CMD flask run --host=0.0.0.0
