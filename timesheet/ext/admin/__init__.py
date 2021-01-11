from flask_admin import Admin

from timesheet.ext.db import db
from timesheet.ext.db.models.infos import PauseInfos
from timesheet.ext.db.models.users import User

from .models import AdminView, PauseInfosView, UserModelView

admin = Admin(index_view=AdminView())


def init_app(app):
    admin.name = app.config.get("APP_NAME", "TimeSheet")
    admin.url = "/"
    admin.index_view.is_visible = lambda: False
    admin.template_mode = app.config.get("ADMIN_TEMPLATE_MODE", "bootstrap3")
    admin.add_view(UserModelView(User, db.session, "Funcionarios"))
    admin.add_view(PauseInfosView(PauseInfos, db.session, "Pausas"))

    admin.init_app(app)
