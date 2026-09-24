import os
from typing import List
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    PROJECT_NAME: str = "SIH26017 Land Acquisition Delay Prediction System"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api"
    ENVIRONMENT: str = "development"
    
    # Server host & port
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Security
    SECRET_KEY: str = "nexora-tau-sih26017-super-secret-security-key-change-in-prod-2026"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours
    
    # Database
    DATABASE_URL: str = Field(
        default="postgresql+psycopg2://postgres:postgres@localhost:5432/land_acquisition_db",
        env="DATABASE_URL"
    )
    SQLITE_FALLBACK_URL: str = "sqlite:///./land_acquisition.db"
    
    # CORS
    CORS_ORIGINS: str = "http://localhost:4200,http://127.0.0.1:4200,http://localhost:3000,http://localhost:80"
    
    # Demo and Alerts
    DEMO_DATA_MODE: bool = True
    ENABLE_SOUND_ALERTS: bool = True
    ALERT_REFRESH_INTERVAL_SECONDS: int = 15

    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]

    class Config:
        case_sensitive = True
        env_file = ".env"
        extra = "allow"

settings = Settings()
