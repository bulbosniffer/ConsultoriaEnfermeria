# config.py
import os
from urllib.parse import quote_plus
from dotenv import load_dotenv
from pathlib import Path

# Cargar archivo .env de forma explícita
env_path = Path(__file__).resolve().parent / '.env'
load_dotenv(dotenv_path=env_path)

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'clave-segura-por-defecto')


class DevelopmentConfig(Config):
    USER = os.getenv('DB_USER')
    RAW_PASSWORD = os.getenv('DB_PASSWORD')
    if RAW_PASSWORD is None:
        raise ValueError("Falta la variable DB_PASSWORD en .env")
    PASSWORD = quote_plus(RAW_PASSWORD)
    HOST = os.getenv('DB_HOST')
    PORT = os.getenv('DB_PORT')
    DB_NAME = os.getenv('DB_NAME')

    SQLALCHEMY_DATABASE_URI = (
        f'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}'
    )
    DEBUG = True


class ProductionConfig(DevelopmentConfig):
    DEBUG = False

