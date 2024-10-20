import os
from dotenv import load_dotenv
from quart import Quart
from quart_bcrypt import Bcrypt

from db import db

load_dotenv("./.env")

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_PWD = os.getenv("DB_PWD")
DB_USER = os.getenv("DB_USER")
print(DB_USER)
print(os.getenv("MODE"))


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


class Development(Config):
    DEBUG = True


class Production(Config):
    SECRET_KEY = os.getenv("SECRET_KEY")
    BCRYPT_HANDLE_LONG_PASSWORDS = True


def create_app(mode=os.getenv("MODE")):
    """In production create as app = create_app('Production')"""
    app = Quart(__name__)
    app.config.from_object(f"config.{mode}")
    print(app.config.get("DATABASE_URL"))
    db.init_app(app)
    bcrypt = Bcrypt()
    bcrypt.init_app(app)
    return app
