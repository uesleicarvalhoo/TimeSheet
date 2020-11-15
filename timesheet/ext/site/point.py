from flask import Blueprint, Response, render_template
from flask_login import login_required

from timesheet.ext.db.models import PauseInfos

bp = Blueprint("point", __name__)


@bp.route("/point/register", methods=["GET", "POST"])
@login_required
def register() -> Response:
    return render_template("site/point/register.html", pauses=PauseInfos.get_all())


@bp.route("/point/consult", methods=["GET", "POST"])
@login_required
def consult() -> Response:
    return render_template("site/point/consult.html")
