from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./dev.db"
    SECRET_KEY: str = "change-me-to-a-secure-random-value"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    DEBUG: bool = True

    class Config:
        env_file = ".env"

settings = Settings()
