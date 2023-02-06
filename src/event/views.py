# from flask import render_template, redirect, session, request
# from flask_login import login_user, login_required, current_user


# from src.handlers.views import autherntication_required
# from src.models import User, Event
# from src.config import db , mail, app

# @autherntication_required
# def add():
# 	name = request.form.get("name")
# 	if name != "":
# 		event = Event(name=name, superadmin_id=current_user.id);
# 		db.session.add(event)
# 		db.session.commit()

# 	return "event"

