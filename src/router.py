from flask import url_for
from .auth import auth
from .home import home
from .event import event
from .handlers import auth_req
from .participant import participant
from .admins import admin
from .declarate import declarate
from .division import division
from .invitation import invitation
from .attendance import attendance

from src.config import app


# register.add_url_rule("/register")

# app.register_blueprint(login_page, url_prefix='/auth')
# app.register_blueprint(register_page, url_prefix='/auth')
# app.register_blueprint(logout_page, url_prefix='/auth')
# app.register_blueprint(activate_page, url_prefix='/auth')

app.register_blueprint(auth, url_prefix='/auth')

app.register_blueprint(home, url_prefix='/')
# app.register_blueprint(home, url_prefix='/home')

# app.register_blueprint(auth_req, url_prefix='/auth')


# app.register_blueprint(index_page, url_prefix='/')

app.register_blueprint(event, url_prefix='/event')
app.register_blueprint(participant, url_prefix='/participant')
app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(declarate, url_prefix='/declarate')
app.register_blueprint(division, url_prefix='/division')
app.register_blueprint(invitation, url_prefix='/invitation')
app.register_blueprint(attendance, url_prefix='/attendance')

