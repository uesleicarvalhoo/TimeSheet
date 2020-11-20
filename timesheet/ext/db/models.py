import datetime as dt
from typing import Dict, List

from flask_login import UserMixin
from sqlalchemy import event
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

    def to_dict(self) -> Dict:
        return {col: getattr(self, col) for col in self.__table__.columns.keys()}

    def to_json(self) -> Dict:
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
        data_copy = data.copy()

        for col in data_copy.keys():
            if col not in self.editable_fields:
                data.pop(col, None)

        self.populate_object(**data)

        if "updated_at" in self.__table__.columns.keys():
            self.updated_at = dt.datetime.now()
            self.save()

    def save(self) -> Dict:
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
    workload = db.Column("workload", db.Integer)
    admin = db.Column("admin", db.Boolean, default=False)
    active = db.Column("active", db.Boolean, default=True)
    created_at = db.Column("created_at", db.Date, default=dt.datetime.utcnow())
    updated_at = db.Column("updated_at", db.Date, default=dt.datetime.utcnow())

    @staticmethod
    def create(user: str, password: str, name: str, workload: int, admin: bool = False, save: bool = True):
        user = User(username=user, password=password, name=name, workload=workload, admin=admin)

        if save:
            user.save()

        return user

    @staticmethod
    def delete(**kwargs: dict):
        User.query.filter_by(**kwargs).delete()
        db.session.commit()

    @property
    def is_admin(self) -> bool:
        return self.admin

    @property
    def is_active(self) -> bool:
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
    editable_fields = ["entry", "finish"]

    @staticmethod
    def get(**filter: dict) -> db.Model:
        return Register.query.filter_by(**filter).first()

    @staticmethod
    def get_all(**filter: dict) -> List[db.Model]:
        return Register.query.filter_by(**filter).all()

    @staticmethod
    def get_by_date(user_id: int, date: dt.datetime) -> db.Model:
        return Register.query.filter_by(user_id=user_id, date=date).first()

    @staticmethod
    def filter(*args: List) -> List[db.Model]:
        return Register.query.filter(*args).all()

    @staticmethod
    def create(user_id: int, date: dt.date, save: bool = True) -> Dict:
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

    def to_dict(self) -> Dict:
        data = super().to_dict()
        data["pauses"] = [pause.to_dict() for pause in self.pauses]

        return data

    def to_json(self) -> Dict:
        data = super().to_json()
        data["pauses"] = [pause.to_json() for pause in self.pauses]

        return data

    def get_pause(self, pause_id: int) -> db.Model:
        return Pauses.get(register_id=self.id, pause_id=pause_id) or Pauses()

    @property
    def entry_hour(self) -> str:
        if self.entry:
            return self.entry.strftime("%H:%M")
        return "--:--"

    @property
    def finish_hour(self) -> str:
        if self.finish:
            return self.finish.strftime("%H:%M")
        return "--:--"

    def validate(self, event: str) -> Dict:
        success = True
        msg = ""
        if event == "entry":
            if self.entry:
                msg = "A entrada já foi registrada!"

        elif event == "finish":
            if not self.entry:
                success = False
                msg = "Você precisa registrar a entrada primeiro"

            if self.finish:
                success = False
                msg = "A saida já foi registrada!"

        return {"success": success, "message": msg}


class Pauses(BaseModel, db.Model):
    __tablename__ = "pauses"
    __name__ = "pausa"
    editable_fields = ["entry", "finish"]
    id = db.Column("id", db.Integer, primary_key=True)
    register_id = db.Column("register_id", db.Integer, db.ForeignKey("register.id"))
    pause_id = db.Column("pause_id", db.Integer, db.ForeignKey("pause_infos.id"))
    entry = db.Column("entry", db.Time(6))
    finish = db.Column("finish", db.Time(6))
    created_at = db.Column("created_at", db.Date, default=dt.datetime.utcnow())
    updated_at = db.Column("updated_at", db.Date, default=dt.datetime.utcnow())

    register = db.relationship("Register", back_populates="pauses")
    info = db.relationship("PauseInfos")

    @staticmethod
    def create(register_id: int, pause_id: int, save: bool = True) -> Dict:
        pause = Pauses(register_id=register_id, pause_id=pause_id)
        if save:
            return pause.save()

        return pause

    @staticmethod
    def get(**filter) -> db.Model:
        return Pauses.query.filter_by(**filter).first()

    @property
    def init_hour(self) -> str:
        if self.entry:
            return self.entry.strftime("%H:%M")
        return "--:--"

    @property
    def finish_hour(self) -> str:
        if self.finish:
            return self.finish.strftime("%H:%M")
        return "--:--"

    def validate(self, event: str) -> Dict:
        success = True
        msg = ""
        if event == "entry":
            if self.entry:
                success = False
                msg = "A entrada já foi registrada!"

        elif event == "finish":
            if not self.entry:
                success = False
                msg = "Você precisa registrar a entrada primeiro!"

            elif self.finish:
                success = False
                msg = "A saida já foi registrada!"

        else:
            return {"success": self.finish is not None}

        return {"success": success, "message": msg}


class PauseInfos(BaseModel, db.Model):
    __tablename__ = "pause_infos"
    id = db.Column("id", db.Integer, primary_key=True)
    init_label = db.Column("init_label", db.Unicode(20), nullable=False)
    end_label = db.Column("end_label", db.Unicode(20), nullable=False)
    time = db.Column("time", db.Integer, nullable=False)

    @staticmethod
    def get_all(**filter):
        return PauseInfos.query.filter_by(**filter).all()


@event.listens_for(User.password, 'set', retval=True)
def hash_user_password(target, value, oldvalue, initiator):
    if value != oldvalue:
        return generate_password_hash(value)

    return value
