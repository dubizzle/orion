import logging


class HostnameContextFilter(logging.Filter):
    """
    This is a filter which injects contextual information into the log.
    """

    def __init__(self, hostname, appname, *args, **kwargs):
        super(HostnameContextFilter, self).__init__(*args, **kwargs)

        self.hostname = hostname
        self.appname = appname

    def filter(self, record):
        record.hostname = self.hostname
        record.appname = self.appname
        return True
