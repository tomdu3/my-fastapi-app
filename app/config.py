from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables or .env file.
    
    This provides type-safe configuration management with validation.
    Settings are loaded in this priority order:
    1. Environment variables
    2. .env file
    3. Default values (if specified)
    """
    app_name: str = "My FastAPI App"
    admin_email: str
    items_per_user: int = 20
    secret_key: str
    database_url: str = "sqlite:///./sql_app.db"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # This tells Pydantic to read from a .env file
    model_config = SettingsConfigDict(env_file=".env")


# Singleton instance - import this in your app
settings = Settings()
