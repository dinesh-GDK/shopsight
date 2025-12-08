"""Configuration management for ShopSight backend."""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Application
    APP_NAME: str = "ShopSight"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    # API
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_RELOAD: bool = True

    # Data Paths
    DATA_DIR: str = "../hm_with_images"
    ARTICLES_PATH: str = "../hm_with_images/articles/*.parquet"
    CUSTOMERS_PATH: str = "../hm_with_images/customers/*.parquet"
    TRANSACTIONS_PATH: str = "../hm_with_images/transactions/*.parquet"

    # LLM
    OLLAMA_HOST: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3.2"
    OLLAMA_TIMEOUT: int = 30

    # Performance
    DUCKDB_THREADS: int = 4
    DUCKDB_MEMORY_LIMIT: str = "4GB"

    # Logging
    LOG_LEVEL: str = "INFO"

    # CORS
    CORS_ORIGINS: list = ["http://localhost:5173", "http://localhost:3000"]

    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()
