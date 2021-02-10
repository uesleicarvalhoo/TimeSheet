from timesheet.ext.db import db
from timesheet.ext.db.models import BaseModel


class PauseInfos(BaseModel):
    __tablename__ = "pause_infos"
    id = db.Column("id", db.Integer, primary_key=True)
    init_label = db.Column("init_label", db.Unicode(20), nullable=False)
    end_label = db.Column("end_label", db.Unicode(20), nullable=False)
    time = db.Column("time", db.Integer, nullable=False)

    @staticmethod
    def get_all(**filter):
        return PauseInfos.query.filter_by(**filter).all()

    @staticmethod
    def get_time(id: int) -> int:
        return PauseInfos.query.filter_by(id=id).first().time


class DaysOff(BaseModel):
    __tablename__ = "days_off"
    id = db.Column("id", db.Integer, primary_key=True)
    user_id = db.Column("user_id", db.Integer, db.ForeignKey("user.id"))
    date = db.Column("date", db.Date, nullable=False)

    user = db.relationship("User", back_populates="days_off")
