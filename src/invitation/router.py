from flask import Blueprint, render_template, abort

from . import invitation 

# from .create.views import create 
# from .get.views import get 
from .get.views import get 
from .send_invitation.views import send 


invitation.add_url_rule("/", view_func=get, methods=["POST", "GET"])
invitation.add_url_rule("/send", view_func=send, methods=["POST", "GET"])

# event.add_url_rule("/delete", view_func=delete, methods=["POST", "GET"])
# event.add_url_rule("/get", view_func=get, methods=["POST", "GET"])
