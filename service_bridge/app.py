from db import db
from service_bridge.config import create_app

app = create_app()

if __name__ == "__main__":
    app.run()
