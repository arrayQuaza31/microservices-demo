from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    MONGO_HOST: str
    MONGO_PORT: int
    MONGO_DB_NAME: str
    MONGO_COLLECTION_NAME: str
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


Config = Settings()
