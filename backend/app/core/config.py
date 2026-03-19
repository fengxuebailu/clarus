from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings"""

    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/clarus_db"

    # Gemini API
    GEMINI_API_KEY: str
    GEMINI_MODEL: str = "gemini-1.5-pro"

    # KataGo Configuration
    KATAGO_PATH: str = ""  # Path to KataGo executable
    KATAGO_CONFIG: str = ""  # Path to config file
    KATAGO_MODEL: str = ""  # Path to model file
    KATAGO_TIMEOUT: int = 30

    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://localhost:8080",  # Frontend HTTP server
        "http://127.0.0.1:8080"
    ]

    # Reconstruction Loop
    MAX_RECONSTRUCTION_RETRIES: int = 3
    RECONSTRUCTION_THRESHOLD: float = 0.15

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
