from abc import ABCMeta
from datetime import date, datetime, time
from typing import Dict

from timesheet.ext.db import db
from timesheet.utils.date import get_now_datetime


class BaseModel(db.Model, ABCMeta):
    __name__ = "registro"
    __abstract__ = True
    editable_fields = []

    def populate_object(self, **data: Dict) -> None:
        columns = self.__table__.columns.keys()
        for key, value in data.items():
            if key in columns:
                setattr(self, key, value)

    def to_dict(self) -> Dict:
        return {col: getattr(self, col) for col in self.__table__.columns.keys()}

    def to_json(self) -> Dict:
        data = self.to_dict()

        for col, value in data.items():
            if isinstance(value, datetime) or isinstance(value, date):
                data[col] = value.isoformat()

            elif isinstance(value, time):
                data[col] = value.isoformat()[:8]

        return data

    def delete(self) -> None:
        db.session.delete(self)
        db.session.commit()

    def update(self, **data: Dict) -> None:
        data_copy = data.copy()

        for col in data_copy.keys():
            if col not in self.editable_fields:
                data.pop(col, None)

        self.populate_object(**data)

        if "updated_at" in self.__table__.columns.keys():
            self.updated_at = get_now_datetime()
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
        try:
            return excp.orig.msg

        except Exception:
            return str(excp)
