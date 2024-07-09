from pydantic_settings import BaseSettings
from pydantic import EmailStr


class Settings(BaseSettings):
    database_url: str
    secret_key: str
    algorithm: str
    mail_username: str
    mail_password: str
    mail_from: EmailStr
    mail_port: int
    mail_server: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


settings = Settings()
