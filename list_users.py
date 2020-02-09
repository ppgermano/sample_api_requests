import logging
from clients.api_client import JWTApiClient, NoAuthApiClient
from dynaconf import settings

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)-15s - [%(levelname)s] - %(name)s - %(message)s")

c = NoAuthApiClient("http://localhost:4000")
print(c.list().json())

c = JWTApiClient(settings.get("username"), settings.get("password"))
print(c.list().json())
