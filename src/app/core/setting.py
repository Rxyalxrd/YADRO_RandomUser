from pydantic import RedisDsn
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class RedisSettings(BaseSettings):

    redis_host: str
    redis_port: int

    @property
    def redis_url(self) -> str:
        return RedisDsn.build(
            scheme="redis",
            host=self.redis_host,
            port=self.redis_port
        ).unicode_string()


class APIURLSettings(BaseSettings):

    api_url: str


class Settings(RedisSettings, APIURLSettings):

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings() # type: ignore
