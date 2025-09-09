from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str = "change_me"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 120
    DATABASE_URL: str | None = None

    class Config:
        env_file = ".env"

settings = Settings()
