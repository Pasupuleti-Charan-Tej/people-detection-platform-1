from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://visionai:visionai_secret@localhost:5432/visionai"
    REDIS_URL: str = "redis://localhost:6379"
    SECRET_KEY: str = "your-super-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ENVIRONMENT: str = "development"

    class Config:
        env_file = ".env"

settings = Settings()
