from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    REDIS_URL: str = "redis://localhost:6379/0"
    SECRET_KEY: str = "default-secret-key"

    class Config:
        env_file = "/app/env/api.env"

settings = Settings()
