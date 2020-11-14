from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import Required


class BaseForm(FlaskForm):
    def populate_obj(self, obj: FlaskForm):
        super(FlaskForm, self).populate_obj(obj)
        for field in self:
            if isinstance(field, QuerySelectField):
                setattr(obj, field.name, field.data.id)


class FormLogin(BaseForm):
    username = StringField("Usuario", [Required()])
    passwd = PasswordField("Senha", [Required()])
