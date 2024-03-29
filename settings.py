"""FastAPI settings."""
import logging
from functools import lru_cache

from pydantic import Extra, Field, PostgresDsn, field_validator
from pydantic_core.core_schema import ValidationInfo
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import URL


def _build_db_dsn(values_dict: dict, async_dsn: bool = False) -> URL:
    driver_name = 'postgresql'
    if async_dsn:
        driver_name = '{name}+asyncpg'.format(name=driver_name)
    return URL.create(
        drivername=driver_name,
        username=values_dict['POSTGRES_USER'],
        password=values_dict['POSTGRES_PASSWORD'],
        host=values_dict['POSTGRES_HOST'],
        port=values_dict['POSTGRES_PORT'],
        database=values_dict['POSTGRES_DB'],
    )


class MainSettings(BaseSettings):
    """App settings."""

    model_config = SettingsConfigDict(
        extra=Extra.ignore,
        env_file='.env',
        env_file_encoding='UTF-8',
        env_nested_delimiter='__',
    )

    # DATABASE SETTINGS
    POSTGRES_ECHO: bool = Field(default=False)
    POSTGRES_DB: str = Field(default='postgres')
    POSTGRES_USER: str = Field(default='postgres')
    POSTGRES_HOST: str = Field(default='127.0.0.1')
    POSTGRES_PASSWORD: str = Field(default='postgres')
    POSTGRES_PORT: int = Field(default=5432)
    POSTGRES_DSN: PostgresDsn | None = Field(default=None)
    POSTGRES_DSN_ASYNC: PostgresDsn | None = Field(default=None)

    # BACK-END SETTINGS
    DEBUG: bool = Field(default=False)
    ENABLE_OPENAPI: bool = Field(default=False)
    HOST: str = Field(default='127.0.0.1')
    PORT: int = Field(default=8000)
    WORKERS_COUNT: int = Field(default=1)
    TRUSTED_HOSTS: list[str] = Field(default=['*'])
    DATETIME_FORMAT: str = Field('%Y-%m-%d %H:%M:%S')  # noqa WPS323

    # ONE-TIME TOKEN SETTINGS
    TOKEN_LIFE_TIME: int = Field(default=3600)

    # JWT SETTINGS
    JWT_SECRET_KEY: str = Field('JWT_SECRET_KEY')
    JWT_REFRESH_SECRET_KEY: str = Field('JWT_REFRESH_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRE_SECONDS: int = Field(default=3660)
    JWT_REFRESH_TOKEN_EXPIRE_SECONDS: int = Field(default=(60 * 60 * 24 * 7))
    JWT_ALGORITHM: str = Field(default='HS256')

    # CORS SETTINGS
    CORS_ALLOW_CREDENTIALS: bool = Field(default=True)
    CORS_ALLOW_HEADERS: list[str] = Field(default=['*'])
    CORS_ALLOW_METHODS: list[str] = Field(default=['*'])
    CORS_ALLOW_ORIGINS: list[str] = Field(default=['*'])

    # LOGGING SETTINGS
    LOG_LEVEL: int = Field(default=logging.WARNING)
    LOG_USE_COLORS: bool = Field(default=False)

    @field_validator('POSTGRES_DSN', 'POSTGRES_DSN_ASYNC', check_fields=True)
    @classmethod
    def validate_database_url(
        cls,
        url_value: str | int | None,
        model_info: ValidationInfo,
    ) -> URL | str:
        """Validate db sync and async urls."""
        async_dsn: bool = True
        if model_info.field_name == 'POSTGRES_DSN':
            async_dsn = False
        if url_value is None:
            return _build_db_dsn(values_dict=model_info.data, async_dsn=async_dsn)
        return url_value


@lru_cache
def get_settings() -> MainSettings:
    """Get settings instance."""
    return MainSettings()


Settings: MainSettings = get_settings()

if Settings.DEBUG:
    import pprint  # noqa WPS400

    printer = pprint.PrettyPrinter()
    printer.pprint(Settings.dict())
