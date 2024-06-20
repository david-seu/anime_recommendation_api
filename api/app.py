from flask import Flask

from routes import anime


def create_app():
    app = Flask(__name__)

    app.register_blueprint(anime)
    return app


