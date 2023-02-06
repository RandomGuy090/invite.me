from flask import render_template, redirect, session, url_for, request
from flask.views import View

from src.models import User
from src.config import db, app
from flask_login import login_user, current_user, login_required

from src.models import User, Participants, Event, Divisions
from src.handlers.views import autherntication_required, superadmin_required

from src.division.create.forms import NewDivisionForm


from ..create.form import CreateEventForm




@login_required
@autherntication_required
def get():
	event_id = request.args.get("event")


	event_host_id = current_user.id if current_user.superadmin else  current_user.added_by


	form = CreateEventForm()
	if current_user.added_by:
		event = Event.query.filter_by(superadmin_id=current_user.added_by).all()
	else:
		event = Event.query.filter_by(superadmin_id=current_user.id).all()
	
	divisions = Event.query\
		.add_columns(Event.name.label("event_name"))\
		.add_columns(Event.id.label("event_id"))\
		.join(Divisions, Divisions.event_id == Event.id)\
		.add_columns(Divisions.id.label("division_id"))\
		.add_columns(Divisions.superadmin_id.label("superadmin_id"))\
		.add_columns(Divisions.division_leader.label("division_leader"))\
		.add_columns(Divisions.division_name.label("division_name"))\
		.filter_by(superadmin_id=event_host_id)
	if event_id:
		divisions = divisions.where(Event.id == event_id, Event.superadmin_id == event_host_id)

	print(divisions)
	divisions = divisions.all()



	next=request.args.get("next")
	if next:
		return redirect(next)

	user = current_user
	


	return render_template("event.html", eventCreateForm=form, 
		events=event,
		divisionCreateForm=NewDivisionForm(),
		divisions=divisions,
		user=user)


