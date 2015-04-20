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


def datadog_post(metric, points):
	""" This function sends the data to datadog

	metric: A custom matric will be generated based on this name
	points: A value of the metric
	"""

	status = api.Metric.send(metric=metric, points=points)
	logger.info("Metric: %s - Points: %s - Status: %s" %
				(metric, points, status))


def process_chronos_jobs():
	""" This function gets all the scheduled jobs
	from chronos and send its data to datadog
	"""

	try:
		req = requests.get(settings.CHRONOS_JOBS_URI, timeout=5)
	except exceptions.ConnectionError as e:
		logger.error("Chronos Endpoint exception: %s" % e)
		return

	jobs = req.json()

	for job in data:
		metric = "chronos_%s" % job['name']
		for field in settings.CHRONOS_FIELDS:
			datadog_send_data("%s.%s" % (metric, field), job[field])

		for field in settings.CHRONOS_TIME_FIELDS:
			metric_timestamp = iso_to_timestamp(job[field])
			if metric_timestamp:
				datadog_send_data("%s.%s" % (metric, field),
								  (metric_timestamp, 1))

	return True
