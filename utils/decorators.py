import time
import logging

class Decorator(object):

	@staticmethod
	def refresh_token(decorated):
		def wrapper(*args, **kwargs):
			client_object = args[0]
			if client_object.authentication_option['refresh'] == True:
				if time.time() > client_object.access_token_expiration:
					logging.info("Refreshing authentication ...")
					client_object.access_token_expiration, client_object.prep = client_object.authentication_function()
			return decorated(*args, **kwargs)
		return wrapper

	@staticmethod
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
