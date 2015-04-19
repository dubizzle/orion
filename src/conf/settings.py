import os
import socket

SYSLOG_HOST = os.environ.get('SYSLOG_HOST', 'syslog-aws.dubizzlecloud.internal')
SYSLOG_PORT = os.environ.get('SYSLOG_PORT', '1122')
LOGGING_FILE_HANDLER = os.environ.get('LOGGING_FILE_HANDLER', 'file_handler')

MARATHON_PORT = os.environ.get('MARATHON_PORT', 8080)
CHRONOS_PORT = os.environ.get('CHRONOS_PORT', 4400)

DATADOG_API_KEY = os.environ.get('DATADOG_API_KEY')
DATADOG_APP_KEY = os.environ.get('DATADOG_APP_KEY')

ZK_HOSTS = os.environ.get('ZK_HOSTS')

current_path = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.abspath(os.path.join(current_path, 'local_settings.py'))

try:
    execfile(file_path, globals(), locals())
except:
    pass

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'orion': {
            '()': 'src.utils.customlogging.HostnameContextFilter',
            'hostname': socket.gethostname(),
            'appname': 'orion'
        }
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'standard': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'syslog': {
            'format': '%(hostname)s %(appname)s %(levelname)s %(asctime)s %(module)s %(message)s'
        },
    },
    'handlers': {
        'syslog_handler': {
            'level': 'DEBUG',
            'class': 'logging.handlers.SysLogHandler',
            'facility': 'local0',
            'formatter': 'syslog',
            'filters': ['orion'],
            'address': [SYSLOG_HOST, SYSLOG_PORT],
        },
        'file_handler': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': ('/var/log/meteor/orion.log'),
            'formatter': 'standard',
        }
    },
    'loggers': {
        'orion': {
              'handlers': LOGGING_FILE_HANDLER,
              'propagate': True,
              'level': 'DEBUG',
        }
    }
}
