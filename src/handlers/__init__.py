from flask import Blueprint, url_for

auth_req = Blueprint('autherntication_required', __name__, template_folder='templates')

from . import router