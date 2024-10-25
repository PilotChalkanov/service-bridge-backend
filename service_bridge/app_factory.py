import os

from quart import Quart
from quart_auth import QuartAuth
from quart_bcrypt import Bcrypt
from quart_db import QuartDB

from config import config

bcrypt = Bcrypt()
auth_manager = QuartAuth()
db = QuartDB(migrations_folder='../database/migrations')

def create_app(mode=os.getenv("MODE")):
    """In production create as app = create_app('Production')"""
    app = Quart(__name__)
    app.config.from_object(config[mode])
    auth_manager.init_app(app)
    bcrypt.init_app(app)
    db.init_app(app)
    from auth import auth_bp

    app.register_blueprint(auth_bp)
    return app