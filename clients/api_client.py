from mixings.mixing import LoggerMixin
from auxiliar.http_request import NoAuthHttpRequest, JwtHttpRequest


class NoAuthApiClient(LoggerMixin, NoAuthHttpRequest):

    def __init__(self, dominio):
        super(NoAuthApiClient, self).__init__(dominio)

    def list(self):
        self.logger.info('list endpoint')
        return self._http_request('GET', '/teste')


class JWTApiClient(LoggerMixin, JwtHttpRequest):

    domain = "http://localhost:4000"
    auth_endpoint = "/users/authenticate"
    auth_schema = {"username": "", "password": ""}

    def __init__(self, username, password):
        self.auth_schema['username'], self.auth_schema['password'] = username, password
        self.auth_data = self.auth_schema
        super(JWTApiClient, self).__init__(username, password, self.domain,
                                           self.auth_endpoint, self.auth_data)

    def list(self):
        self.logger.info('list endpoint')
        return self._http_request('GET', '/teste')
