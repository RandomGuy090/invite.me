from flask import Blueprint, render_template, abort

from .create.views import  create
from .delete.views import  delete
from .get.views import  get
# from .get.views import  Participant


from . import division

division.add_url_rule("/get", view_func=get, methods=["GET"])
# participant.add_url_rule("/get", view_func=Participant.as_view("participants_get"), methods=["GET"])
division.add_url_rule("/create", view_func=create, methods=["POST", "GET"])
division.add_url_rule("/delete", view_func=delete, methods=["POST"])

