# app/core/config.py
import os
from dotenv import load_dotenv

load_dotenv() # بيقرأ ملف الـ .env

class Settings:
    PROJECT_NAME: str = " digital wallet"
    MONGO_URL: str = os.getenv("MONGO_URL")
    DATABASE_NAME: str = os.getenv("DATABASE_NAME")

settings = Settings()