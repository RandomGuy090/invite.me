from flask import render_template, redirect, session, request, url_for, jsonify, flash
from flask_login import login_user, login_required, current_user


from src.handlers.views import autherntication_required
from src.models import User, Event, Participants, Accompanying
from src.config import db, mail, app

from .form import DeleteForm

def cancel():
	next = request.args.get("next")	
	participant_id = request.args.get("participant")
	declaration_string = request.args.get("declaration_string")

	if declaration_string:
		# if request.method == "POST":
		qr = Participants.query.filter_by(declaration_string=declaration_string)
	
	elif participant_id:
		qr = Participants.query.filter_by(id=participant_id)

	part_id = qr.first()

	if not part_id:
		flash("no such user")
		if next:
			return redirect(next)
		else:
			return "no such user"

	part_id.canceled = not(part_id.canceled)
	db.session.add(part_id)
	db.session.commit()
		

	if next:
		return redirect(next)

	return redirect(url_for("participant.get" ))



