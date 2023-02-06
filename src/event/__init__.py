from flask import Blueprint, render_template, abort



event = Blueprint('event', __name__, template_folder='templates', static_folder="static")

from . import router