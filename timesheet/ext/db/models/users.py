import re
from datetime import datetime, time
from typing import Any

from flask_login import UserMixin
from sqlalchemy import event
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash

from timesheet.ext.db import db
from timesheet.ext.db.models import BaseModel


class User(BaseModel, UserMixin):
    __tablename__ = "user"
    __name__ = "usuario"
    id = db.Column("id", db.Integer, primary_key=True)
    username = db.Column("username", db.Unicode(30), unique=True, nullable=False)
    password = db.Column("password", db.Unicode(150), nullable=False)
    name = db.Column("name", db.Unicode(50), nullable=False)
    workload = db.Column("workload", db.Time, nullable=False)
    admin = db.Column("admin", db.Boolean, default=False)
    active = db.Column("active", db.Boolean, default=True)
    created_at = db.Column("created_at", db.Date, default=datetime.utcnow())
    updated_at = db.Column("updated_at", db.Date, onupdate=datetime.utcnow())
    week_days_off = db.Column("week_days_off", db.Unicode(50))
    days_off = db.relationship("DaysOff", back_populates="user")

    @staticmethod
    def create(user: str, password: str, name: str, workload: int, admin: bool = False, save: bool = True):
        user = User(username=user, password=password, name=name, workload=workload, admin=admin)
        if save:
            user.save()

        return user

    @staticmethod
    def delete(**kwargs: dict) -> None:
        User.query.filter_by(**kwargs).delete()
        db.session.commit()

    @property
    def is_admin(self) -> bool:
        return self.admin

    @property
    def is_active(self) -> bool:
        return self.active

    @staticmethod
    def get(**kwags: dict) -> db.Model:
        return User.query.filter_by(**kwags).first()

    def parse_exception(self, excp: IntegrityError) -> str:
        err = excp.orig.msg

        if "duplicate" in err.lower():
            return "%s já cadastrado" % self.username.upper()

        elif "cannot be null" in err.lower():
            return "O campo '%s' é obrigatorio" % re.search("\'(.*?)\'", err).group(1)

        return err

    def get_bank_of_hours(self) -> str:
        return time(0, 0, 0).isoformat()


@event.listens_for(User.password, 'set', retval=True)
def hash_user_password(target, value, oldvalue, initiator) -> Any:
    if value != oldvalue:
        return generate_password_hash(value)

    return value
