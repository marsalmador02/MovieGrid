"""
Application configuration module.

Loads environment variables and provides a centralized configuration object.
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    TMDB_API_KEY: str = os.getenv("TMDB_API_KEY")

settings = Settings()