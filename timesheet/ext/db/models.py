import datetime as dt

from flask_login import UserMixin
from werkzeug.security import generate_password_hash

from . import db


class BaseModel:
    __name__ = "registro"
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

            elif isinstance(value, dt.time):
                data[col] = value.isoformat()[:8]

        return data

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

    def save(self) -> dict:
        try:
            db.session.add(self)
            db.session.commit()

        except Exception as err:
            db.session.rollback()
            response = {
                "success": False,
                "message": f"Não foi possível salvar o {self.__name__}\nDescrição: {self.parse_exception(err)}",
            }

        else:
            response = {"success": True, "data": self.to_json()}

        return response

    def parse_exception(self, excp: Exception) -> str:
        return str(excp)


class User(BaseModel, UserMixin, db.Model):
    __tablename__ = "user"
    __name__ = "usuario"
    id = db.Column("id", db.Integer, primary_key=True)
    username = db.Column("username", db.Unicode, unique=True)
    password = db.Column("password", db.Unicode)
    name = db.Column("name", db.Unicode)
    admin = db.Column("admin", db.Boolean, default=False)
    active = db.Column("active", db.Boolean, default=True)
    created_at = db.Column("created_at", db.Date, default=dt.datetime.utcnow())
    updated_at = db.Column("updated_at", db.Date, default=dt.datetime.utcnow())

    @staticmethod
    def create(user: str, password: str, name: str, admin: bool = False, active: bool = True, save: bool = True):
        hash_passwd = generate_password_hash(password)
        user = User(username=user, password=hash_passwd, name=name, admin=admin, active=active)

        if save:
            user.save()

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
    __name__ = "registro"
    id = db.Column("id", db.Integer, primary_key=True)
    user_id = db.Column("user_id", db.Integer)
    entry = db.Column("entry", db.Time)
    finish = db.Column("finish", db.Time)
    date = db.Column("date", db.Date, default=dt.datetime.now().date())
    created_at = db.Column("created_at", db.Date, default=dt.datetime.utcnow())
    updated_at = db.Column("updated_at", db.Date, default=dt.datetime.utcnow())
    pauses = db.relationship("Pauses", back_populates="register")
    editable_fields = []

    @staticmethod
    def get(**filter) -> db.Model:
        return Register.query.filter_by(**filter).first()

    @staticmethod
    def get_by_date(user_id: int, date: dt.datetime) -> db.Model:
        return Register.query.filter_by(user_id=user_id, date=date).first()

    @staticmethod
    def create(user_id: int, date: dt.date, save: bool = True) -> dict:
        register = Register(user_id=user_id, date=date)
        if save:
            return register.save()
        return register

    @staticmethod
    def get_user_register(user_id: int, date: dt.date) -> db.Model:
        register = Register.get(id=user_id, date=date.isoformat())
        if register is None:
            register = Register.create()
            register.save()

        return register

    def get_pauses(self):
        return Pauses.get_all(register_id=self.id)

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["pauses"] = [pause.to_dict() for pause in self.pauses]

        return data

    def to_json(self) -> dict:
        data = super().to_json()
        data["pauses"] = [pause.to_json() for pause in self.pauses]

        return data


class Pauses(BaseModel, db.Model):
    __tablename__ = "pauses"
    __name__ = "pausa"
    id = db.Column("id", db.Integer, primary_key=True)
    register_id = db.Column("register_id", db.Integer, db.ForeignKey("register.id"))
    pause_id = db.Column("pause_id", db.Integer, db.ForeignKey("pause_infos.id"))
    init = db.Column("init", db.Time(6))
    finish = db.Column("finish", db.Time(6))
    created_at = db.Column("created_at", db.Date, default=dt.datetime.utcnow())
    updated_at = db.Column("updated_at", db.Date, default=dt.datetime.utcnow())

    register = db.relationship("Register", back_populates="pauses")
    info = db.relationship("PauseInfos")

    @staticmethod
    def create(register_id: int, pause_id: int, save: bool = True) -> dict:
        pause = Pauses(register_id=register_id, pause_id=pause_id)
        if save:
            return pause.save()

        return pause

    @staticmethod
    def get(**filter) -> db.Model:
        return Pauses.query.filter_by(**filter).first()


class PauseInfos(BaseModel, db.Model):
    __tablename__ = "pause_infos"
    id = db.Column("id", db.Integer, primary_key=True)
    init_label = db.Column("init_label", db.Unicode(20), nullable=False)
    end_label = db.Column("end_label", db.Unicode(20), nullable=False)
    time = db.Column("time", db.Integer, nullable=False)

    @staticmethod
    def get_all(**filter):
        return PauseInfos.query.filter_by(**filter).all()
