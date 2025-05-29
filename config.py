from pydantic_settings import BaseSettings, SettingsConfigDict

DEBUG = False


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env-dev' if DEBUG else 'deploy/.env',
    )

    DEBUG: bool = DEBUG

    SECRET_KEY: str

    DB_HOST: str
    DB_PORT: str
    DB_USER: str
    DB_PASS: str
    DB_NAME: str


settings = Settings()
