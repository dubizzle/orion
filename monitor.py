import requests
import logging
import logging.config
import time
from datetime import datetime

from src.conf import settings
from requests import exceptions
from datadog import initialize, api


logging.config.dictConfig(settings.LOGGING)
logger = logging.getLogger('orion')

# Intialize datadog API
options = {
    'api_key': settings.DATADOG_API_KEY,
    'app_key': settings.DATADOG_APP_KEY
}
initialize(**options)


def iso_to_timestamp(metric_datetime):
    """ Returns the timestamp

    metric_datetime: datetime in iso format
    """

    metric_timestamp = None
    try:
        metric_timestamp = time.mktime(datetime.strptime(
            metric_datetime,
            "%Y-%m-%dT%H:%M:%S.%fZ"
        ).timetuple())
    except (ValueError, TypeError):
        pass

    return metric_timestamp


def datadog_post(metric, points, tags):
    """ This function sends the data to datadog

    metric: A custom matric will be generated based on this name
    points: A value of the metric
    """

    status = api.Metric.send(metric=metric, points=points, tags=tags)
    message = ("Metric: %s - Points: %s, Tags: %s - Status: %s" %
        (metric, points, tags, status)
    )
    print message
    logger.info(message)


def prepare_and_post_data(available_fields, items,
                          metric=None, tags=[]):
    """ This function prepares the data and send it to datadog

    available_fields: list of fields we want to send to datadog
    items: list of tasks/jobs
    metric: datadog metric
    tags: list of tags
    """

    for item in items:
        if not metric:
            metric = "chronos_%s" % item['name']
        for field in available_fields.get('int', []):
            datadog_post("%s.%s" % (metric, field), item[field], tags)
        for field in available_fields.get('boolean', []):
            datadog_post("%s.%s" % (metric, field), int(item[field]), tags)
        for field in available_fields.get('datetime', []):
            metric_timestamp = iso_to_timestamp(item[field])
            if metric_timestamp:
                datadog_post("%s.%s" % (metric, field),
                    (metric_timestamp, 1), tags)


def process_chronos_jobs():
    """ This function gets all the scheduled jobs
    from chronos and send its data to datadog
    """

    try:
        req = requests.get(settings.CHRONOS_JOBS_URI, timeout=5)
    except exceptions.ConnectionError as e:
        logger.error("Chronos Endpoint exception: %s" % e)
        return

    if req.ok:
        prepare_and_post_data(settings.CHRONOS_FIELDS, req.json())

    return True

def process_marathon_tasks():
    """ This function gets all the marathon tasks
    health check and send it to datadog
    """

    try:
        # get the apps
        req = requests.get(settings.MARATHON_APPS_URI, timeout=5)
    except exceptions.ConnectionError as e:
        logger.error("Chronos Endpoint exception: %s" % e)
        return

    if !req.ok:
        return

    data = req.json()

    for app in data['apps']:
        # gets app health checks
        req = requests.get("%s%s" % (settings.MARATHON_APPS_URI, app['id']))
        metric = "marathon_%s" % app['id'][1:]

        apps = req.json()

        tasks = apps['app']['tasks']
        for task in tasks:
            tags = [task['id']]
            results = task.get('healthCheckResults', [])
            prepare_and_post_data(settings.MARATHON_FIELDS,
                results, metric, tags)

    return True

if __name__ == "__main__":

    while True:
        process_marathon_tasks()
        process_chronos_jobs()
        time.sleep(settings.CHECK_INTERVAL)
