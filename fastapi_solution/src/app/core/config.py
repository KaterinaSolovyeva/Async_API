import os
from typing import Optional

from pydantic import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    ES_HOST: str = 'localhost'
    ES_PORT: int = 9200

    STORAGE_FILE_PATH: str = 'etl/state.json'

    POSTGRES_DB: str = 'postgres'
    POSTGRES_USER: str = 'postgres'
    POSTGRES_PASSWORD: str = 'postgres'
    POSTGRES_HOST: str = 'localhost'
    POSTGRES_PORT: int = 5432

    REDIS_URL: str = 'redis://localhost:6379'

    PROJECT_NAME: str = 'Read-only API for an online cinema'
    PROJECT_DESCRIPTION: str = 'Information about films, genres and people who participated in the creation of the work'
    PROJECT_VERSION: str = '1.0.0'

    BASE_DIR: Optional[str] = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    DEFAULT_PAGE_SIZE: int = 50
    DEFAULT_PAGE_NUMBER: int = 1

    ELASTIC_HOST: str = 'localhost'
    ELASTIC_PORT: int = 9200


settings = Settings()
