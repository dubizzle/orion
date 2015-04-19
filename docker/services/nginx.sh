#!/bin/bash

chmod a+r /etc/container_environment.sh
source /etc/container_environment.sh
envtpl < ${REPO_DIR}/deploy/nginx.conf.tpl > /etc/nginx/sites-enabled/nazgul.conf
exec /usr/sbin/nginx -c /etc/nginx/nginx.conf -g "daemon off;"
