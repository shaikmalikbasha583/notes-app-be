from pydantic import BaseSettings


class Settings(BaseSettings):
    TEST_VAR: str

    class Config:
        env_file = ".env"


settings = Settings()
