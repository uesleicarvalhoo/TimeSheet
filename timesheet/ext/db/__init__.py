from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_app(app: Flask) -> None:
    db.init_app(app)


def create_all() -> None:
    db.create_all()


def drop_db() -> None:
    db.drop_all()
