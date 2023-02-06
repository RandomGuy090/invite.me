from flask import Blueprint, render_template, abort



declarate = Blueprint('declarate', __name__, template_folder='templates', static_folder='static')

from . import router