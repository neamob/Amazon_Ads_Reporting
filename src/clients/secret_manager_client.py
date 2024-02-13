import json
from google.cloud import secretmanager
from dotenv import load_dotenv
import os
import logging
from pydantic import Json

load_dotenv()

secret_logger = logging.getLogger("Secret Logger")


class SecretManagerClient:
    @staticmethod
    def get_secret_value() -> Json:
        try:
            client = secretmanager.SecretManagerServiceClient()
            name = os.environ["SECRET_PATH"]
            response = client.access_secret_version(request={"name": name})
            secret_logger.info("Returned secret value succesfully")
            return json.loads(response.payload.data.decode("UTF-8"))

        except:
            secret_logger.error("Something went wrong with secret value")
            raise (Exception)




