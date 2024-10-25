import os
from distutils.command.config import config

from dotenv import load_dotenv

load_dotenv("./.env")

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_PWD = os.getenv("DB_PWD")
DB_USER = os.getenv("DB_USER")


class Config:
    DEBUG = False
    TESTING = False
    SECRET_KEY = "secret"
    QUART_DB_DATABASE_URL = (
        f"postgresql://{DB_USER}:{DB_PWD}@{DB_HOST}:{DB_PORT}/servicebridge"
    )
    BCRYPT_LOG_ROUNDS = 12
    BCRYPT_HASH_PREFIX = os.getenv("HASHING_ALG")
    BCRYPT_HANDLE_LONG_PASSWORDS = False


class DevConfig(Config):
    DEBUG = True

class TestConfig(config):
    DEBUG = False
    QUART_DB_DATABASE_URL = (
        f"postgresql://{DB_USER}:{DB_PWD}@{DB_HOST}:{DB_PORT}/servicebridge_test"
    )


class ProdConfig(Config):
    SECRET_KEY = os.getenv("SECRET_KEY")
    BCRYPT_HANDLE_LONG_PASSWORDS = True

config = {
    "dev": DevConfig,
    "test": TestConfig,
    "prod": ProdConfig

}
