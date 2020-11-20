from flask import Flask

from .resources import api


def init_app(app: Flask) -> None:
    api.init_app(app)
