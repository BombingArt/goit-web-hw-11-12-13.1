from pydantic_settings import BaseSettings
from pydantic import EmailStr
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    database_url: str
    secret_key: str
    algorithm: str
    mail_username: str
    mail_password: str
    mail_from: EmailStr
    mail_port: int
    mail_server: str
    redis_host: str
    redis_port: int
    cloudinary_name: str
    cloudinary_api_key: str
    cloudinary_api_secret: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


settings = Settings()
