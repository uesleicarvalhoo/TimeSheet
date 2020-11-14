from flask import Blueprint, Response, render_template

bp = Blueprint("point", __name__)


@bp.route("/point/register", methods=["GET", "POST"])
def register() -> Response:
    return render_template("site/point/register.html")


@bp.route("/point/consult", methods=["GET", "POST"])
def consult() -> Response:
    return render_template("site/point/consult.html")
