from flask import Blueprint, Response, flash, redirect, render_template, request, url_for
from flask_login import login_required, logout_user

from timesheet.ext.auth import validate_user

from .forms import FormLogin

bp = Blueprint("site", __name__)


@bp.route("/login", methods=["GET", "POST"])
def login() -> Response:
    form = FormLogin()
    if request.method == "POST":
        response = validate_user(form.username.data, form.passwd.data)
        if response["success"]:
            return redirect(url_for("site.index"))

        else:
            flash(response["message"], "is-danger")

    return render_template("auth/login.html", form=form)


@bp.route("/", methods=["GET"])
@login_required
def index() -> Response:
    return render_template("site/index.html")


@bp.route("/logout", methods=["GET"])
def logout() -> Response:
    logout_user()
    return redirect(url_for("site.login"))
