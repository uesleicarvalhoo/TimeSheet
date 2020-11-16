from datetime import date

from pydantic import BaseModel, validator


class Pause(BaseModel):
    id: int = None
    event: str = None
    type: str

    @validator("event")
    def validate_event(cls, v):
        if v and v not in ["entry", "finish"]:
            raise ValueError(f'{v} não é um evento valido')

        return v

    @validator("type")
    def validate_type(cls, v):
        if v not in ["register", "pause"]:
            raise ValueError(f'{v} não é um tipo valido')

        return v


class Date(BaseModel):
    date: date
