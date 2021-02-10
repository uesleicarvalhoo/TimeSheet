from datetime import date

from pydantic import BaseModel


class Date(BaseModel):
    date: date
