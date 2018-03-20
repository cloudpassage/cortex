FROM nginx:alpine
MAINTAINER toolbox@cloudpassage.com

expose 443

COPY octobox.conf /etc/octobox.conf

COPY index.html /usr/share/nginx/html/index.html

COPY runner.sh /

CMD /runner.sh
