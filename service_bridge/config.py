import os
from dotenv import load_dotenv
from quart import Quart


load_dotenv('./.env')

class Config:
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'secret'

class Development(Config):
    DEBUG = True

class Production(Config):
    SECRET_KEY = os.getenv("SECRET_KEY")

def create_app(mode=os.getenv("MODE")):
    """In production create as app = create_app('Production')"""
    app = Quart(__name__)
    app.config.from_object(f"config.{mode}")
    return app