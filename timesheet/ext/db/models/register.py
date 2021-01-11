from datetime import date as dt
from datetime import datetime, time
from typing import Dict, List

from timesheet.ext.db import db
from timesheet.ext.utils import get_today, subtract_time

from . import BaseModel
from .pauses import Pauses


class Register(BaseModel, db.Model):
    __tablename__ = "register"
    __name__ = "registro"
    id = db.Column("id", db.Integer, primary_key=True)
    user_id = db.Column("user_id", db.Integer)
    entry = db.Column("entry", db.Time)
    finish = db.Column("finish", db.Time)
    date = db.Column("date", db.Date, default=datetime.now().date())
    workload = db.Column("workload", db.Time, nullable=False)
    created_at = db.Column("created_at", db.Date, default=datetime.utcnow())
    updated_at = db.Column("updated_at", db.Date, onupdate=datetime.utcnow())
    pauses = db.relationship("Pauses", back_populates="register")
    editable_fields = ["entry", "finish"]

    @staticmethod
    def get(**filter: dict) -> db.Model:
        return Register.query.filter_by(**filter).first()

    @staticmethod
    def get_all(**filter: dict) -> List[db.Model]:
        return Register.query.filter_by(**filter).all()

    @staticmethod
    def get_by_date(user_id: int, date: datetime) -> db.Model:
        return Register.query.filter_by(user_id=user_id, date=date).first()

    @staticmethod
    def filter(*args: List) -> List[db.Model]:
        return Register.query.filter(*args).all()

    @staticmethod
    def create(user_id: int, date: dt, save: bool = True) -> Dict:
        register = Register(user_id=user_id, date=date)
        if save:
            return register.save()
        return register

    @staticmethod
    def get_user_register(user_id: int, date: dt) -> db.Model:
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

    def get_delay(self) -> time:
        time = datetime(datetime.today().year, 1, 1)
        for pause in self.pauses:
            time += pause.get_delay()

        return time.time()

    def get_bank_of_hours(self) -> time:
        return time(0, 0, 0)

    def get_worked_hours(self) -> time:
        if not self.entry or not self.finish:
            return time()

        return (get_today() + subtract_time(self.finish, self.entry)).time()

    def get_balance_hours(self) -> Dict:
        today = get_today()
        worked_hours = self.get_worked_hours()

        if worked_hours > self.workload:
            balance = (today + subtract_time(self.get_worked_hours(), self.workload)).time()
            return {"time": (get_today() + subtract_time(balance, self.get_delay())).time(), "negative": False}

        balance = (today + subtract_time(self.workload, self.get_worked_hours())).time()

        return {"time": (today + subtract_time(balance, self.get_delay())).time(), "negative": True}
