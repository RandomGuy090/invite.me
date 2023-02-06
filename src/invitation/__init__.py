from flask import Blueprint, render_template, abort



invitation = Blueprint('invitation', __name__, template_folder='templates', static_folder="static")

from . import router