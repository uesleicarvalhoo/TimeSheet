from datetime import timedelta
from functools import wraps
from typing import Callable, Dict

from flask import Flask, flash, redirect, request, url_for
from flask_login import LoginManager, current_user, login_user
from werkzeug.security import check_password_hash

from timesheet.ext.db.models import User

login_manager = LoginManager()


def init_app(app: Flask) -> None:
    login_manager.init_app(app)
    login_manager.login_view = "site.login"
    app.permanent_session_lifetime = timedelta(hours=1)


@login_manager.user_loader
def load_user(user_id: int) -> User:
    return User.get(id=user_id)


def validate_user(username: str, password: str) -> Dict:
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


def check_api_auth(func: Callable, *args, **kwargs) -> Callable:
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return {
                "success": False,
                "message": "Você precisa fazer login antes de continuar",
            }, 401
        return func(*args, **kwargs)

    return decorated_function


@login_manager.unauthorized_handler
def unauthorized():
    flash("Você precisa estar logado para acessar esta página.", "is-danger")
    return redirect(url_for("site.login", next=request.url))
