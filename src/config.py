import sys

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


def get_model_config():
    return SettingsConfigDict(env_file='src/.env')


class Settings(BaseSettings):
    DB_HOST: str = Field(default='192.168.0.19')
    DB_PORT: int = Field(default='5432')
    DB_USER: str = Field(default='postgres')
    DB_PASS: str = Field(default='postgres')
    DB_NAME: str = Field(default='postgres')
    secret_key: str = Field(default='mrtwon1488')
    algorithm: str = Field(default='HS256')

    def get_auth_data(self):
        return {"secret_key": self.secret_key, "algorithm": self.algorithm}

    @property
    def DATABASE_URL_asyncpg(self):
        return f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'

    @property
    def DATABASE_URL_psycopg(self):
        return f'postgresql+psycopg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'

    model_config = get_model_config()


settings = Settings()
