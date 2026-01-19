from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore'
    )
    
    # Telegram
    BOT_TOKEN: str
    ADMIN_IDS: str
    
    # Pyrus
    PYRUS_API_KEY: str
    PYRUS_API_URL: str = "https://api.pyrus.com/v4"
    
    # Database
    DATABASE_URL: str
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379"
    
    # App
    LOG_LEVEL: str = "INFO"
    ENVIRONMENT: str = "production"
    MAX_DESCRIPTION_LENGTH: int = 1000
    
    @property
    def admin_ids_list(self) -> List[int]:
        return [int(id.strip()) for id in self.ADMIN_IDS.split(',')]


settings = Settings()  # type: ignore