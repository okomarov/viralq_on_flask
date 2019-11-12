from flask import Flask

from app.config import BaseConfig


def create_app():
    app = Flask(__name__)
    app.config.from_object(BaseConfig)

    register_extensions(app)
    register_blueprints(app)

    return app


def register_extensions(app):
    from app.extensions import db
    from app.extensions import mail
    from app.extensions import migrate

    db.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)


def register_blueprints(app):
    from app.routes import webapp_bp
    app.register_blueprint(webapp_bp)

    from app.routes import error_bp
    app.register_blueprint(error_bp)


app = create_app()
