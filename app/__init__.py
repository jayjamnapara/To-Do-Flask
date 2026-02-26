from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # app secret key and sqlite the config
    app.config["SECRET_KEY"] = "hksjjvkbsvkbskvbk"
    app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///to_do_app.db'
    app.config["SQLALCHMEY_TRACE_MODIFICATION"] = False

    db.init_app(app)

    # register all the blueprints
    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp)
    from app.routes.tasks import task_bp
    app.register_blueprint(task_bp)

    return app