from flask import Blueprint, render_template, abort



# login_page = Blueprint('login', __name__, template_folder='templates')
# register_page = Blueprint('register', __name__, template_folder='templates')
# logout_page = Blueprint('logout', __name__, template_folder='templates')
# activate_page = Blueprint('activate', __name__, template_folder='templates')

attendance = Blueprint('attendance', __name__, template_folder='templates')

from . import router