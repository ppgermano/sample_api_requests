import time
import logging
import requests
from urllib.parse import urljoin


class Decorators(object):
	@staticmethod
	def refresh_token(decorated):
		def wrapper(*args, **kwargs):
			client_object = args[0]
			if client_object.authentication_option['refresh'] == True:
				if time.time() > client_object.access_token_expiration:
					logging.info("Refreshing authentication ...")
					client_object.authentication_option['authentication_method']()
			return decorated(*args, **kwargs)
		return wrapper


class HttpRequest(object):

	def __init__(self, domain, auth_endpoint="", username="", password="",
				 auth_data="", authentication_option="None"):

		self.authentication_options = {
			"None": {
				"refresh": False,
				"authentication_method": self._no_auth
			},
			"Bearer": {
				"refresh": True,
				"authentication_method": self._bearer_auth
			}
		}
		self.authentication_option = self.authentication_options[authentication_option]

		self.username, self.password = username, password
		self.domain = domain
		self.auth_endpoint = auth_endpoint
		self.auth_data = auth_data

		self.session = requests.Session()
		self.authentication_option['authentication_method']()

	def _no_auth(self):
		self.prep = requests.Request('GET', self.domain).prepare()

	def _bearer_auth(self, expire=3600):

		url = urljoin(self.domain, self.auth_endpoint)
		r = self.session.post(url, json=self.auth_data)

		self.token = r.json()['token']
		self.access_token_expiration = time.time() + expire

		logging.debug('Got token {}'.format(self.token))

		self.prep = requests.Request("GET", self.domain).prepare()
		self.prep.headers = {"Authorization": "Bearer {}".format(self.token)}

	@Decorators.refresh_token
	def _http_request(self, method='GET', endpoint="", json_data={}):

		self.prep.method = method
		self.prep.url = urljoin(
			self.domain, endpoint) if endpoint else self.domain

		if json_data:
			self.prep.prepare_body(data=json_data, files=None, json=True)

		return self.session.send(self.prep)
