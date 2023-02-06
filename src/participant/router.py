from flask import Blueprint, render_template, abort

from .create.views import  create
from .delete.views import  delete
from .cancel.views import  cancel
from .get.views import  get
# from .get.views import  Participant


from . import participant

participant.add_url_rule("/get", view_func=get, methods=["GET"])
# participant.add_url_rule("/get", view_func=Participant.as_view("participants_get"), methods=["GET"])
participant.add_url_rule("/create", view_func=create, methods=["POST", "GET"])
participant.add_url_rule("/delete", view_func=delete, methods=["POST"])
participant.add_url_rule("/cancel", view_func=cancel, methods=["POST", "GET"])

