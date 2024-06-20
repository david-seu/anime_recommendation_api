from flask import Flask

from routes import anime_bp


def create_app():
    app = Flask(__name__)

    app.register_blueprint(anime_bp)
    return app


