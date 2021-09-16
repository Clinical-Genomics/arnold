from pathlib import Path
from typing import Optional

from pydantic import BaseSettings

ARNOLD_PACKAGE = Path(__file__).parent
PACKAGE_ROOT: Path = ARNOLD_PACKAGE.parent
ENV_FILE: Path = PACKAGE_ROOT / ".env"


class Settings(BaseSettings):
    """Settings for serving the arnold app and connect to the mongo database"""

    db_uri: str = "mongodb://localhost:27017/arnold-demo"
    db_name: str = "arnold-demo"
    secret_key: str = "dummy"
    algorithm: str = "ABC"
    host: str = "localhost"
    access_token_expire_minutes: int = 60
    port: int = 8000

    class Config:
        env_file = str(ENV_FILE)


settings = Settings()
