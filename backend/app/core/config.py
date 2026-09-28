import os
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file=".env",
        extra="allow"
    )

    PROJECT_NAME: str = "SIH26017 Land Acquisition Delay Prediction System"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    
    # Server host & port
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    
    # Security
    SECRET_KEY: str = Field(
        default=os.getenv("SECRET_KEY", "nexora-tau-sih26017-super-secret-security-key-change-in-prod-2026")
    )
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours
    
    # Database
    DATABASE_URL: str = Field(
        default=os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:postgres@localhost:5432/land_acquisition_db")
    )
    SQLITE_FALLBACK_URL: str = os.getenv("SQLITE_FALLBACK_URL", "sqlite:///./land_acquisition.db")
    
    # CORS
    CORS_ORIGINS: str = os.getenv("CORS_ORIGINS", "http://localhost:4200,http://127.0.0.1:4200,http://localhost:3000,http://localhost:80")
    
    # Demo and Alerts
    DEMO_DATA_MODE: bool = True
    ENABLE_SOUND_ALERTS: bool = True
    ALERT_REFRESH_INTERVAL_SECONDS: int = 15

    @property
    def cors_origins_list(self) -> List[str]:
        if self.CORS_ORIGINS == "*":
            return ["*"]
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]

settings = Settings()
