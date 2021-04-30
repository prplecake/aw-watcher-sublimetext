import json
import socket
import requests
from datetime import datetime, timezone

from . import utils


class ActivityWatchAPI(object):
	_last_heartbeat = datetime.now(timezone.utc)
	debug = False
	url = None

	def __init__(self):
		utils.log("ActivityWatchAPI initializing")

	def setup(self, client_id, host, port, heartbeat_freq):
		self.url = "http://{}:{}".format(host, port)
		self.client_id = client_id
		self.hostname = socket.gethostname()
		self.freq = heartbeat_freq

	def enable_debugging(self):
		self.debug = True
		utils.log("API debugging enabled.")

	def _make_url(self, endpoint):
		return "{}/api/0/buckets/{}".format(self.url, endpoint)

	def _rate_limited(self, now):
		return (now - self._last_heartbeat).total_seconds() > self.freq

	def check(self):
		if self.debug:
			utils.log("Checking server connection")
		headers = {"Content-type": "application/json"}
		try:
			requests.get(self._make_url(""), headers=headers)
			self.connected = True
		except requests.RequestException:
			self.connected = False
			utils.log("could not connect\n\turl: {}".format(self.url))

		return self.connected

	def ensure_bucket(self, bucket_id):
		if self.debug:
			utils.log("Ensuring bucket exists.")
		bucket = self.get_bucket(bucket_id)
		bucket_exists = 'id' in bucket
		if not bucket_exists:
			self.create_bucket(bucket_id)

	def get_bucket(self, bucket_id):
		if self.debug:
			utils.log("Retrieving bucket.")
		endpoint = "{}".format(bucket_id)
		headers = {"Content-type": "application/json"}
		resp = requests.get(self._make_url(endpoint), headers=headers)
		return json.loads(resp.text)

	def create_bucket(self, bucket_id):
		if self.debug:
			utils.log("Creating bucket.")
		endpoint = "{}".format(bucket_id)
		data = {
			"client": self.client_id,
			"type": 'app.editor.activity',
			"hostname": self.hostname,
		}
		headers = {"Content-type": "application/json"}
		resp = requests.post(
			self._make_url(endpoint),
			data=json.dumps(data), headers=headers)
		return json.loads(resp.text)

	def delete_bucket(self, bucket_id):
		if self.debug:
			utils.log("Deleting bucket.")
		endpoint = "{}?force=1".format(bucket_id)
		resp = requests.delete(self._make_url(endpoint))
		return json.loads(resp.text)

	def heartbeat(self, bucket_id, event_data, pulsetime=30):
		now = datetime.now(timezone.utc)

		if not self._rate_limited(now):
			return

		if self.debug:
			utils.log("Heartbeat")
			utils.log("now: {}".format(now))

		endpoint = "{}/heartbeat?pulsetime={}".format(
			bucket_id, pulsetime)

		data = {
			"timestamp": now.isoformat(),
			'duration': 0,
			'data': event_data,
		}
		headers = {"Content-type": "application/json"}
		resp = requests.post(
			self._make_url(endpoint),
			data=json.dumps(data),
			headers=headers)
		self._last_heartbeat = now
		return resp
