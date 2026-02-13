from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "SWIR Spectra Library API"
    database_url: str = "postgresql://swir:swir@db:5432/swir"
    raw_storage_path: str = "/data/raw"
    local_dev_open_admin: bool = True

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
