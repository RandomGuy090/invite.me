from flask import Blueprint, render_template, abort, url_for

from .get.views import get
from .create.views import create
from .update.views import update
from .send_declaration.views import send

from . import declarate

# index_page = Blueprint('index', __name__, template_folder='templates', static_folder="static")


# declarate.add_url_rule("/", view_func=home_view, methods=["GET","POST"])
declarate.add_url_rule("/", view_func=get, methods=["GET","POST"])
declarate.add_url_rule("/create", view_func=create, methods=["GET","POST"])
declarate.add_url_rule("/update", view_func=update, methods=["GET","POST"])
declarate.add_url_rule("/send", view_func=send, methods=["POST"])


