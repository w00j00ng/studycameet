from flask import Flask
import config
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)
    migrate.init_app(app, db)

    from .views import main_views, cambot_views, auth_views, student_views, teacher_views

    app.register_blueprint(main_views.bp)
    app.register_blueprint(cambot_views.bp)
    app.register_blueprint(auth_views.bp)
    app.register_blueprint(student_views.bp)
    app.register_blueprint(teacher_views.bp)

    return app
