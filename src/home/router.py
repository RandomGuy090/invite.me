from flask import Blueprint, render_template, abort, url_for

from .views import  home as home_view

from . import home

# index_page = Blueprint('index', __name__, template_folder='templates', static_folder="static")


home.add_url_rule("/", view_func=home_view, methods=["GET","POST"])
home.add_url_rule("/home", view_func=home_view, methods=["GET","POST"])


