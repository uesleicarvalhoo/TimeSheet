from datetime import datetime
from typing import Any, List

from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import PasswordField, SelectField, StringField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import Required

from timesheet.ext.db.models import User

MONTHS = [
    (1, "Janeiro"),
    (2, "Fevereiro"),
    (3, "Março"),
    (4, "Abril"),
    (5, "Maio"),
    (6, "Junho"),
    (7, "Julho"),
    (8, "Agosto"),
    (9, "Setembro"),
    (0, "Outubro"),
    (11, "Novembro"),
    (12, "Dezembro"),
]


def choice(data: dict, item: Any) -> str:
    for key, value in data:
        if key == item:
            return key


def generate_years() -> List[int]:
    year = datetime.today().year
    return [2020] + [y + 1 for y in range(2020, year)]


class BaseForm(FlaskForm):
    def populate_obj(self, obj: FlaskForm):
        super(FlaskForm, self).populate_obj(obj)
        for field in self:
            if isinstance(field, QuerySelectField):
                setattr(obj, field.name, field.data.id)


class FormLogin(BaseForm):
    username = StringField("Usuario", [Required("Informe o usuario")])
    passwd = PasswordField("Senha", [Required("Informe a senha")])


class FormTimeSheet(BaseForm):
    month = SelectField(
        "Mês",
        validators=[Required("Selecione o mês")],
        choices=MONTHS,
        default=choice(MONTHS, datetime.today().month),
    )

    year = SelectField(
        "Ano",
        validators=[Required("Selecione o ano")],
        choices=generate_years(),
        default=datetime.today().year,
    )
    users_list = QuerySelectField(
        "Funcionarios",
        validators=[Required("Selecione o funcionario")],
        get_label="name",
        get_pk=lambda x: x.id,
        query_factory=lambda: User.query,
        allow_blank=True,
        default=lambda: User.get(id=current_user.id),
    )
