from flask import render_template, redirect, session, request, url_for, jsonify
from flask_login import login_user, login_required, current_user


from src.handlers.views import autherntication_required
from src.models import User, Event, Participants, Divisions
from src.config import db, mail, app

from .form import DeleteForm

@login_required
@autherntication_required
def delete():
	division_id = request.args.get("division_id")
	next = request.args.get("next")

	if request.method == "POST":
		# qr =  Event.query\
		# 	.add_columns(Event.name.label("event_name"))\
		# 	.join(Divisions, Divisions.event_id == Event.id)\
		# 	.add_columns(Divisions.id.label("division_id"))\
		# 	.add_columns(Divisions.division_leader.label("division_leader"))\
		# 	.add_columns(Divisions.division_name.label("division_name"))
		qr = Divisions.query.filter_by(id=division_id)

		if len(qr.all()):
			qr = qr.delete()
			db.session.commit()
		else:
			return "no such user "

	if next:
		return redirect(next)

	return redirect(url_for("participant.get" ))



