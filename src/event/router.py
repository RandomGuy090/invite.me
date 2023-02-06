from flask import Blueprint, render_template, abort

from . import event 

from .create.views import create 
from .get.views import get 
from .delete.views import delete 
from .update.views import update 


event.add_url_rule("/create", view_func=create, methods=["POST", "GET"])
event.add_url_rule("/delete", view_func=delete, methods=["POST", "GET"])
event.add_url_rule("/get", view_func=get, methods=["POST", "GET"])
event.add_url_rule("/update", view_func=update, methods=["POST", "GET"])
