from pydantic import BaseSettings
from pydantic import Field


class Config(BaseSettings):
    ALLOWED_HOSTS: list[str] = Field(default_factory=list)
    CELERY_BEAT_CALSYNC: int = 15 * 60
    DATABASE_URL: str = ...
    EMAIL_FROM: str = ""
    EMAIL_HOST: str = ""
    EMAIL_HOST_PASSWORD: str = ""
    EMAIL_HOST_USER: str = ""
    EMAIL_PORT: int = 0
    EMAIL_USE_SSL: bool = False
    EMAIL_USE_TLS: bool = False
    MODE_CACHING: bool = False
    MODE_DEBUG: bool = False
    MODE_PROFILING: bool = False
    SECRET_KEY: str = ...
    SENTRY_DSN: str = ""
    SITE_ID: int = -1
    TIME_ZONE: str = "UTC"
