from quart import Quart, request, jsonify

from config import create_app

app = create_app()
# Start the app
if __name__ == "__main__":
    app.run()
