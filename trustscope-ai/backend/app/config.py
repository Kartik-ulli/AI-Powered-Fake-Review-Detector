from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    database_url: str = "sqlite:///./trustscope.db"
    app_env: str = "development"
    secret_key: str = "trustscope-secret"
    cors_origins: str = "http://localhost:5173,http://localhost:3000"
    demo_mode: bool = True
    rate_limit_per_minute: int = 20
    rainforest_api_key: str = ""

    @property
    def cors_origins_list(self) -> List[str]:
        return [o.strip() for o in self.cors_origins.split(",")]

    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
