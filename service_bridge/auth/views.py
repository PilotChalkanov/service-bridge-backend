from quart import request, render_template_string, redirect, url_for
from quart.views import MethodView
from quart_auth import login_user, AuthUser, logout_user, login_required, current_user

from auth import auth_bp
from auth.dummy_templates import template_register, login_template, reset_pass_templ
from auth.models import User
from auth.user_data_gateway import UserDataGateway


class RegisterView(MethodView):
    @staticmethod
    async def get():
        return await render_template_string(template_register)

    @staticmethod
    async def post():
        form_data = await request.form
        email = form_data["email"]

        user = await UserDataGateway.get_user(email)  # Make sure this method is async
        if user:
            return {"error": f"User with mail {email} already exists."}, 400
        user = User(**form_data)
        await UserDataGateway.register_user(
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            password=user.password,
            created_on=user.created_on,
            updated_on=user.updated_on,
        )

        return "User registered successfully.", 201


class LoginView(MethodView):
    @staticmethod
    async def get():

        return await render_template_string(login_template)

    @staticmethod
    async def post():
        form_data = await request.form
        email = form_data.get("email")
        user = await UserDataGateway.get_user(email)
        if user and user.verify_password(form_data.get("password")):
            login_user(AuthUser(str(user.id)))
            _next = request.args.get("next")
            if _next is None or not _next.startswith("/"):
                _next = url_for("main.index")
            return redirect(_next)
        return "Password is missing or invalid", 400


class ResetPassView:
    @staticmethod
    async def get():
        if current_user.is_authenticated:
            return redirect("main.index")
        return render_template_string(reset_pass_templ)

    async def post(self):
        form_data = await request.form
        user = UserDataGateway.get_user(form_data.get("username"))
        if user:
            ...


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))


auth_bp.add_url_rule("/register", view_func=RegisterView.as_view("register"))
auth_bp.add_url_rule("/login", view_func=LoginView.as_view("login"))
