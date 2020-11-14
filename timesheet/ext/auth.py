from datetime import timedelta

from flask import Flask
from flask_login import LoginManager, login_user
from werkzeug.security import check_password_hash

from timesheet.ext.db.models import User

login_manager = LoginManager()


def init_app(app: Flask) -> None:
    login_manager.init_app(app)
    login_manager.login_view = "login"
    app.permanent_session_lifetime = timedelta(hours=1)


@login_manager.user_loader
def load_user(user_id):
    return User.get(id=user_id)


def validate_user(username: str, password: str) -> dict:
    user = User.get(username=username)
    if user is None:
        response = {"success": False, "message": "Usuario não cadastrado"}

    else:
        if not user.is_active:
            response = {
                "success": False,
                "message": "Você não está autorizado a acessar o sistema",
            }

        elif check_password_hash(user.password, password):
            login_user(user)
            response = {"success": True, "message": "Usuario logado com sucesso"}

        else:
            response = {"success": False, "message": "Senha incorreta"}

    return response
