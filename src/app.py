from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()

def create_app():
    # create and configure the Flask application
    app = Flask(__name__, template_folder="templates", static_folder="static", static_url_path="/")
    app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///./testdb.db'
    app.config["SECRET_KEY"] = 'test' # TODO this is temporary
    app.permanent_session_lifetime = timedelta(hours=1)

    db.init_app(app)

    # import and register all blueprints
    from .rate.routes import rate_bp
    from .admin.routes import admin_bp
    from .core.routes import core_bp

    app.register_blueprint(rate_bp, url_prefix="/rate", config = app.config)
    app.register_blueprint(admin_bp, url_prefix="/admin", config = app.config)
    app.register_blueprint(core_bp, url_prefix="/", config = app.config)

    migrate = Migrate(app, db)

    return app
