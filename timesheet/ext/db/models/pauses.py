from datetime import datetime, timedelta
from typing import Dict

from timesheet.ext.db import db
from timesheet.ext.db.models import BaseModel, PauseInfos
from timesheet.ext.utils import parse_int_to_time, subtract_time


class Pauses(BaseModel):
    __tablename__ = "pauses"
    __name__ = "pausa"
    editable_fields = ["entry", "finish"]

    id = db.Column("id", db.Integer, primary_key=True)
    register_id = db.Column("register_id", db.Integer, db.ForeignKey("register.id"))
    pause_id = db.Column("pause_id", db.Integer, db.ForeignKey("pause_infos.id"))
    entry = db.Column("entry", db.Time(6))
    finish = db.Column("finish", db.Time(6))
    time = db.Column("time", db.Time, nullable=False)
    created_at = db.Column("created_at", db.Date, default=datetime.utcnow())
    updated_at = db.Column("updated_at", db.Date, default=datetime.utcnow())

    register = db.relationship("Register", back_populates="pauses")
    info = db.relationship("PauseInfos")

    @staticmethod
    def create(register_id: int, pause_id: int, save: bool = True) -> Dict:
        pause = Pauses(register_id=register_id, pause_id=pause_id)
        pause.time = PauseInfos.get_time(pause_id)

        if save:
            return pause.save()

        return pause

    @staticmethod
    def get(**filter) -> db.Model:
        return Pauses.query.filter_by(**filter).first()

    def get_delay(self) -> timedelta:
        if not self.entry or not self.finish:
            return timedelta()

        pause_time = subtract_time(self.finish, self.entry)

        if parse_int_to_time(pause_time.seconds) > self.time:
            return subtract_time(parse_int_to_time(pause_time.seconds), self.time)

        return timedelta()

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
