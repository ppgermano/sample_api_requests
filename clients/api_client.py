from mixings.mixing import LoggerMixin
from auxiliar.http_request import HttpRequest

def unrestricted():
	def decorator_func(execute_function):
		def wrapper_func(*args, **kwargs):
			client_object = args[0]
			client_object.authentication_option['refresh'] = False
			r = execute_function(*args, **kwargs)
			client_object.authentication_option['refresh'] = True
			return r
		return wrapper_func
	return decorator_func

class NoAuthApiClient(LoggerMixin, HttpRequest):

	def __init__(self, dominio):
		super(NoAuthApiClient, self).__init__(domain=dominio, authentication_option="None")

	def list(self):
		endpoint = '/no-auth'
		self.logger.info('{} endpoint'.format(endpoint))
		return self._http_request('GET', '{}'.format(endpoint))

class BearerAuthApiClient(LoggerMixin, HttpRequest):

	domain = "http://localhost:4000"
	auth_endpoint = "/users/authenticate"
	username_key_in_auth_schema = "username"
	password_key_in_auth_schema = "password"
	auth_schema = {"username": "", "password": ""}

	def __init__(self, username, password):
		self.auth_schema[self.username_key_in_auth_schema], self.auth_schema[self.password_key_in_auth_schema] = username, password
		self.auth_data = self.auth_schema
		auth_option = "Bearer"
		super(BearerAuthApiClient, self).__init__(self.domain, self.auth_endpoint, username, password,
											self.auth_data, expire=2, authentication_option=auth_option)

	@unrestricted()
	def unrestricted_endpoint(self):
		endpoint = '/no-auth'
		self.logger.info('{} endpoint'.format(endpoint))
		return self._http_request('GET', '{}'.format(endpoint))

	def restricted_endpoint(self):
		endpoint = '/users'
		self.logger.info('{} endpoint'.format(endpoint))
		return self._http_request('GET', '{}'.format(endpoint))
