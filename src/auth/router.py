from flask import Blueprint, render_template, abort

from .login.views import  login
from .register.views import  register
from .logout.views import  logout
from .delete.views import delete
from .activate.views import activate_account

# from . import login_page, register_page, logout_page, activate_page
from . import auth

# login_page.add_url_rule("/login", view_func=login, methods=["GET","POST"])
# register_page.add_url_rule("/register", view_func=register, methods=["GET","POST"])
# logout_page.add_url_rule("/logout", view_func=logout, methods=["GET"])
# activate_page.add_url_rule("/activate/<activate_string>/", view_func=activate_account, methods=["GET"])


auth.add_url_rule("/login", view_func=login, methods=["GET","POST"])
auth.add_url_rule("/register", view_func=register, methods=["GET","POST"])
auth.add_url_rule("/logout", view_func=logout, methods=["GET", "POST"])
auth.add_url_rule("/activate/", view_func=activate_account, methods=["GET"])

auth.add_url_rule("/delete/", view_func=delete, methods=["GET", "POST"])

