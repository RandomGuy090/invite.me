from flask import render_template, redirect, session, request, url_for, jsonify
from flask_login import login_user, login_required, current_user


from src.handlers.views import autherntication_required
from src.models import User, Event, Participants, Accompanying
from src.config import db, mail, app

from .form import DeleteForm

@login_required
@autherntication_required
def delete():
	user_id = request.args.get("user_id")
	next = request.args.get("next")

	if request.method == "POST":
		qr = Participants.query.filter_by(id=user_id)
		acc_id = qr.first().accomapnying_id
		acc = None
		if acc_id:
			acc = Accompanying.query.filter_by(id=acc_id)

		if len(qr.all()):
			qr = qr.delete()
			if acc and acc.all():
				acc.delete()
			db.session.commit()
		else:
			return "no such user "

	if next:
		return redirect(next)

	return redirect(url_for("participant.get" ))



