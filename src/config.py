from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


from sqlalchemy import MetaData
from flask_mail import Mail
from src.email_sending.email_core import  Email_core


import os
from datetime import timedelta
from languages.lang import Language



# SECRET_KEY = os.urandom(32)
SECRET_KEY = ""
PORT = 8080
# SESSION_COOKIE_SAMESITE = "None"

app = Flask(__name__)








#  ----------------CUSTOM SETTINGS---------------
app.INVITATION_ONLY_AFTER_DECLARATION_SENT = True
app.INVITATION_ONLY_AFTER_DECLARATED = True
app.UPDATE_EVENT_AFTER_SEND  = True
app.SEND_AGAIN = True



SECRET_KEY = ""

# app.config['SERVER_NAME'] = SECRET_KEY
app.config['APPLICATION_ROOT'] = '127.0.0.1:5000/'
# app.config['SERVER_NAME'] = SECRET_KEY

app.config["SQLALCHEMY_DATABASE_URI"] =  "mariadb+pymysql://SQL_USER:SQL_PASSWORD@ADDRESS/TABLE_NAME?charset=utf8mb4"

app.config['MAIL_SENDER'] = ""
app.config['MAIL_SERVER']=''
app.config['MAIL_PORT'] = 557
app.config['MAIL_USERNAME'] = ''
app.config['MAIL_PASSWORD'] = ''

app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['QR_CODE_RES'] = "500x500"

# ---------------- END OF CUSTOM SETTINGS ----------------------------------







app.config['SQLALCHEMY_POOL_TIMEOUT'] =  1000 
app.config['SQLALCHEMY_POOL_SIZE'] = 100
app.config['SQLALCHEMY_POOL_RECYCLE'] = 280

app.sercret_key = SECRET_KEY
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SESSION_COOKIE_DOMAIN'] = False
app.config['SESSION_COOKIE_PATH'] = "/"


app.config["SESSION_PERMANENT"] = True

app.tempalte_folder = ("home/templates/", 
                        "/participant/templates/",
                        "/auth/templates/",
                        "/handlers/templates/",
                        "/event/templates/",
                        "/declarate/templates/",
                        "/invitation/templates/",
                        )


naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))

# db = SQLAlchemy()


login_manager = LoginManager()

# login_manager.session_protection = "strong"
login_manager.login_view = 'auth.login'



login_manager.init_app(app)

migrate = Migrate(app, db, render_as_batch=True)
db.init_app(app)
# bcrypt = Bcrypt(app)
mail = Mail(app)
# mail = Email_core(app)


# app.config["SESSION_TYPE"] = "filesystem"

# # it fails even without such a small lifetime
# app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=1)
# app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=10)


class Email_config():
    def __str__(self):
        return "PL_lang"
    



    def __init__(self):
        print("email_config")
    # html_template = 




lang = Language()
lang = lang.lang



