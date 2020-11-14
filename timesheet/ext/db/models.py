import datetime as dt
from typing import List

from flask_login import UserMixin
from werkzeug.security import generate_password_hash

from . import db


class BaseModel:
    editable_fields = []

    def populate_object(self, **data: dict) -> None:
        columns = self.__table__.columns.keys()
        for key, value in data.items():
            if key in columns:
                setattr(self, key, value)

    def to_dict(self) -> dict:
        return {col: getattr(self, col) for col in self.__table__.columns.keys()}

    def to_json(self) -> dict:
        data = self.to_dict()

        for col, value in data.items():
            if isinstance(value, dt.datetime) or isinstance(value, dt.date):
                data[col] = value.isoformat()

        return data

    def save(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete(self) -> None:
        db.session.delete(self)
        db.session.commit()

    def update(self, **data: dict) -> None:
        data = data.copy()

        for col in data.keys():
            if col not in self.editable_fields:
                data.pop(col, None)

        self.populate_object(**data)

        if "updated_at" in self.__table__.columns.keys():
            self.updated_at = dt.datetime.now()
            self.save()


class User(BaseModel, UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column("id", db.Integer, primary_key=True)
    username = db.Column("username", db.Unicode, unique=True)
    password = db.Column("password", db.Unicode)
    name = db.Column("name", db.Unicode)

    admin = db.Column("admin", db.Boolean, default=False)
    active = db.Column("active", db.Boolean, default=True)

    @staticmethod
    def create(user: str, password: str, name: str, admin=False, active=False):
        hash_passwd = generate_password_hash(password)
        user = User(
            username=user, password=hash_passwd, name=name, admin=admin, active=active
        )
        db.session.add(user)
        db.session.commit()

        return user

    @staticmethod
    def delete(**kwargs):
        User.query.filter_by(**kwargs).delete()
        db.session.commit()

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active

    @staticmethod
    def get(**kwags) -> db.Model:
        return User.query.filter_by(**kwags).first()


class Register(BaseModel, db.Model):
    __tablename__ = "register"
    id = db.Column("id", db.Integer, primary_key=True)
    user_id = db.Column("user_id", db.Integer)
    date = db.Column("date", db.Date, default=dt.datetime.utcnow())
    updated_at = db.Column("updated_at", db.Date, default=dt.datetime.utcnow())
    hour = db.Column("hour", db.Time, default=dt.datetime.now().time())
    pause_id = db.Column("pause_id", db.Unicode(15))
    event = db.Column("event", db.Unicode(15))

    editable_fields = []

    def populate_obj(self, **data: dict) -> db.Model:
        columns = self.__table__.columns.keys()

        for key, value in data.items():
            if key in columns:
                setattr(self, key, value)

    @staticmethod
    def get(id: int) -> db.Model:
        return Register.query.filter(id).first()

    @staticmethod
    def get_by_date(id: int, date: dt.datetime) -> List[db.Model]:
        return Register.query.filter_by(id=id, date=date).all()

    @staticmethod
    def create(user_id: int, pause: str, event: str) -> dict:
        return Register(user_id=user_id, pause_name=pause, event_name=event)

    def delete(self, id: int) -> dict:
        register = Register.get(id)
        if register is not None:
            try:
                register.delete()

            except Exception as err:
                db.rollback()
                response = {"success": False, "message": err}

            else:
                response = {
                    "success": True,
                    "message": "Registro excluido com sucesso",
                }

        else:
            response = {
                "success": False,
                "message": f"Usuario com a ID {id} não localizado",
            }

        return response

    def update(self, **data: dict) -> dict:
        for key, value in data.items():
            if key in self.editable_fields:
                setattr(self, key, value)
                self.updated_at = dt.datetime.utcnow()

        response = self.save()

        return response

    def save(self) -> dict:
        try:
            db.session.add(self)
            db.session.commit()

        except Exception as err:
            db.session.rollback()

            response = {
                "success": False,
                "message": f"Não foi possível salvar o registro\nDescrição: {err}",
            }

        else:
            response = {"success": True, "data": self.to_dict()}

        return response

    @staticmethod
    def get_user_register(user_id: int, date: dt.date) -> db.Model:
        register = Register.get(id=user_id, date=date.isoformat())
        if register is None:
            register = Register.create()
            register.save()

        return register


class Pauses(BaseModel, db.Model):
    __tablename__ = "pauses"
    id = db.Column("id", db.Integer, primary_key=True)
    init_name = db.Column("init_name", db.Unicode(20), nullable=False)
    end_name = db.Column("end_name", db.Unicode(20), nullable=False)
