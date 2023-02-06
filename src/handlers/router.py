from flask import Blueprint, render_template, abort

from .views import  autherntication_required

from . import auth_req


# auth_req.add_url_rule("/autherntication_required", view_func=login, methods=["GET","POST"])


