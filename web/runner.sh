cat /etc/octobox.conf | envsubst > /etc/nginx/conf.d/default.conf

/usr/sbin/nginx -g "daemon off;"
