# from flask import Flask
# from flask_login import LoginManager
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate


# app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
# app.sercret_key = "secret"

# db = SQLAlchemy()
# login_manager = LoginManager()


# login_manager.init_app(app)
# migrate = Migrate(app, db)
# db.init_app(app)