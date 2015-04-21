FROM        phusion/baseimage:0.9.15

MAINTAINER  Qasim Khan <qasim@dubizzle.com>

ENV         USER            meteor
ENV         GROUP           $USER
ENV         USER_DIR        /opt/$USER
ENV         VENV_DIR        $USER_DIR/.env
ENV         REPO_DIR        $USER_DIR/orion
ENV         VENV_PYTHON     $VENV_DIR/bin/python
ENV         VENV_PIP        $VENV_DIR/bin/pip

USER        root
RUN         set -e && \
            apt-get update -y && \
            apt-get install -y make \
                               screen \
                               vim \
                               build-essential \
                               python-setuptools \
                               python2.7-dev \
                               wget \
                               python-virtualenv \
                               gettext \
                               git

RUN         useradd -m -d $USER_DIR -p $USER -s /bin/bash $USER && \
            chown $USER:$GROUP $USER_DIR -R && \
            mkdir -p /var/log/$USER && \
            chown $USER:$GROUP /var/log/$USER -R

USER        $USER
RUN         git clone https://github.com/dubizzle/orion.git $REPO_DIR
RUN         virtualenv --system-site-packages $VENV_DIR && \
            $VENV_PIP install -r $REPO_DIR/requirements/base.txt

CMD         ["/sbin/my_init"]
