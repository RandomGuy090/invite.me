from flask import Blueprint, render_template, abort

from .inside.views import  *
from .outside.views import  *


from . import attendance


attendance.add_url_rule("/inside", view_func=att_inside, methods=["POST"])
attendance.add_url_rule("/outside", view_func=att_outside, methods=["POST"])
