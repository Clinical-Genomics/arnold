from pathlib import Path
from pymongo import MongoClient

from pydantic import BaseSettings

from arnold.adapter import ArnoldAdapter

ARNOLD_PACKAGE = Path(__file__).parent
PACKAGE_ROOT: Path = ARNOLD_PACKAGE.parent
ENV_FILE: Path = PACKAGE_ROOT / ".env"


class Settings(BaseSettings):
    """Settings for serving the arnold app and connect to the mongo database"""

    db_uri: str = "mongodb://localhost:20817/arnold"
    db_name: str = "arnold"
    secret_key: str = "dummy"
    algorithm: str = "ABC"
    host: str = "localhost"
    access_token_expire_minutes: int = 60
    port: int = 8008

    class Config:
        env_file = str(ENV_FILE)


settings = Settings()


def get_arnold_adapter():
    client = MongoClient(settings.db_uri)
    return ArnoldAdapter(client, db_name=settings.db_name)
