#!/bin/bash

chmod a+r /etc/container_environment.sh
source /etc/container_environment.sh
exec /sbin/setuser dubizzle $VENV_DIR/bin/uwsgi --ini $REPO_DIR/deploy/uwsgi.ini
