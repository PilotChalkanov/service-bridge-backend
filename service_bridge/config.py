import os
from distutils.command.config import config

from dotenv import load_dotenv
from quart import Quart
from quart_bcrypt import Bcrypt
from quart_auth import QuartAuth

from auth.auth import auth_blueprint
from service_bridge.db import db

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


bcrypt = Bcrypt()
auth_manager = QuartAuth()


def create_app(mode=os.getenv("MODE")):
    """In production create as app = create_app('Production')"""
    app = Quart(__name__)
    app.config.from_object(config[mode])
    db.init_app(app)
    auth_manager.init_app(app)
    bcrypt.init_app(app)

    from service_bridge.auth.auth import auth_blueprint

    app.register_blueprint(auth_blueprint)

    return app

config = {
    "dev": DevConfig,
    "test": TestConfig,
    "prod": ProdConfig


}
