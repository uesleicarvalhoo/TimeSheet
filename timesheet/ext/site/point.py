from flask import Blueprint, Response, render_template
from flask_login import current_user, login_required
from sqlalchemy import extract

from timesheet.ext.db.models import PauseInfos, Register

from .forms import FormTimeSheet

bp = Blueprint("point", __name__)


@bp.route("/point/register", methods=["GET", "POST"])
@login_required
def register() -> Response:
    return render_template("site/point/register.html", pauses=PauseInfos.get_all())


@bp.route("/point/consult", methods=["GET", "POST"])
@login_required
def consult() -> Response:
    form = FormTimeSheet()
    user_id = form.users_list.data.id if current_user.is_admin else current_user.id

    registers = Register.filter(
        Register.user_id == user_id,
        extract("month", Register.date) == form.month.data,
        extract("year", Register.date) == form.year.data,
    )

    return render_template("site/point/consult.html", form=form, registers=registers, pauses=PauseInfos.get_all())
