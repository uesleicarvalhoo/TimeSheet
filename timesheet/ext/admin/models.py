from flask import current_app, flash, redirect, request, url_for
from flask_admin import AdminIndexView, expose
from flask_admin.contrib.sqla.view import ModelView
from flask_login import current_user
from wtforms import IntegerField


class AdminView(AdminIndexView):
    @expose("/")
    def index(self):
        if not current_user.is_authenticated:
            flash(
                current_app.config.get(
                    "MSG_ADMIN_ONLY",
                    "Essa página só está disponível para administradores.",
                ),
                "is-danger",
            )
            return redirect(url_for("site.login", next=request.url))

        if current_user.is_admin:
            return super().index()

        else:
            flash(
                current_app.config.get(
                    "MSG_ADMIN_ONLY",
                    "Essa página só está disponível para administradores.",
                ),
                "is-danger",
            )
            return redirect(url_for("site.login", next=request.url))


class BaseView(ModelView):
    page_size = 10

    def is_accessible(self):
        if current_user.is_authenticated:
            return current_user.is_admin

        return False

    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            flash(
                current_app.config.get(
                    "MSG_ADMIN_ONLY",
                    "Essa página só está disponível para administradores.",
                ),
                "is-danger",
            )
            return redirect(url_for("site.login", next=request.url))


class UserModelView(BaseView):
    column_exclude_list = ["id", "password"]
    column_searchable_list = ["username", "name"]
    column_labels = {
        "userame": "Usuario",
        "name": "Nome",
        "password": "Senha",
        "workload": "Carga horaria (mensal)",
        "created_at": "Criado em",
        "updated_at": "Atualizado em",
    }
    form_excluded_columns = ["created_at", "updated_at"]


class PauseInfosView(BaseView):
    column_searchable_list = [
        "init_label",
        "end_label",
    ]

    form_columns = ["init_label", "end_label", "time"]

    column_labels = {
        "init_label": "Inicio",
        "end_label": "Retorno",
        "time": "Tempo (mim)",
    }

    form_overrides = {"time": IntegerField}
