from flask import render_template, redirect, session, request, url_for
from flask_login import login_user, login_required, current_user

from src.handlers.views import autherntication_required, superadmin_required

from src.models import User, Event
from src.config import db, mail, app 

from ..get.form import EventForm
import time

@superadmin_required
@login_required
@autherntication_required
def delete():
	event_id = request.args.get("event_id")	
	qr = Event.query.filter_by(id=event_id);
	next = request.args.get("next")


	if len(qr.all()):
		qr = qr.delete()
	db.session.commit()

	if next:
		return redirect(next)
	return redirect(url_for("event.get"))


	
