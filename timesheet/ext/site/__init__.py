from flask import Flask

from . import main, point


def init_app(app: Flask) -> None:
    app.register_blueprint(main.bp)
    app.register_blueprint(point.bp)
