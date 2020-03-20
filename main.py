import logging, time
from dynaconf import settings

from clients.api_client import BearerAuthApiClient, NoAuthApiClient

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)-15s - [%(levelname)s] - %(name)s - %(message)s")

c = NoAuthApiClient("http://localhost:4000")
print(c.list().json())

c = BearerAuthApiClient(settings.get("USERNAME"), settings.get("PASSWORD"))
print(c.unrestricted_endpoint().json())

time.sleep(3)
print('\n')
print(c.restricted_endpoint().json())
