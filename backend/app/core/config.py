"""Módulo de configuración de la aplicación.

Carga variables de entorno y provee un objeto de configuración centralizado.
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL")

settings = Settings()