import os
from dotenv import load_dotenv

load_dotenv()


class ConfigManager:

    @staticmethod
    def get(key, default=None):
        return os.getenv(key, default)

    @staticmethod
    def require(key):
        value = os.getenv(key)

        if not value:
            raise ValueError(
                f"Environment variable '{key}' is missing."
            )

        return value