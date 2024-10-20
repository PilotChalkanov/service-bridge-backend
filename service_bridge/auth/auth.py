from datetime import datetime, timezone

import bcrypt
from quart import Blueprint, request, render_template_string, g
from quart.views import MethodView
from auth.database_gateway import DatabaseTemplate
from auth.user_data_gateway import UserDataGateway
from db import db

auth_blueprint = Blueprint("auth", __name__)
db_template = DatabaseTemplate(db)

# HTML template for the registration form
template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Register</title>
</head>
<body>
    <h1>User Registration</h1>
    <form action="{{ url_for('auth.register') }}" method="POST">
        <label for="username">Username:</label>
        <input type="text" id="username" name="username" required><br><br>

        <label for="email">Email:</label>
        <input type="email" id="email" name="email" required><br><br>

        <label for="password">Password:</label>
        <input type="password" id="password" name="password" required><br><br>

        <input type="submit" value="Register">
    </form>
</body>
</html>
"""


class RegisterView(MethodView):
    async def get(self):
        return await render_template_string(template)

    async def post(self):
        form_data = await request.form
        username = form_data["username"]
        email = form_data["email"]

        user = await UserDataGateway.get_user(
            username, db_template=db_template
        )  # Make sure this method is async
        if user:
            return {"error": f"User with name {username} already exists."}, 400

        hashed_password = bcrypt.hashpw(
            form_data["password"].encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")

        await UserDataGateway.register_user(
            db_template=db_template,
            username=username,
            password=hashed_password,
            email=email,
            first_name=form_data.get("first_name", ""),
            last_name=form_data.get("last_name", ""),
            created_on=datetime.now(tz=timezone.utc),
            updated_on=datetime.now(tz=timezone.utc),
        )

        return {"message": "User registered successfully."}, 201


auth_blueprint.add_url_rule("/register", view_func=RegisterView.as_view("register"))
