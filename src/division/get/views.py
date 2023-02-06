from flask import render_template, redirect, session, url_for, request
from flask.views import View

from src.models import User
from src.config import db, app
from flask_login import login_user, current_user, login_required

from src.models import User, Participants, Event, Divisions
from src.handlers.views import autherntication_required

from src.division.create.forms import NewDivisionForm




@login_required
@autherntication_required
def get():
	form = NewDivisionForm()
	event = request.args.get("event")

	event_host_id = current_user.id if current_user.superadmin else  current_user.added_by

	if event:
		divisions = Event.query\
		.add_columns(Event.name.label("event_name"))\
		.add_columns(Event.id.label("event_id"))\
		.join(Divisions, Divisions.event_id == Event.id)\
		.add_columns(Divisions.id.label("division_id"))\
		.add_columns(Divisions.division_leader.label("division_leader"))\
		.add_columns(Divisions.division_name.label("division_name"))\
		.where(Event.id == event, Event.superadmin_id == event_host_id)
		divisions = divisions.all()

	else:
		divisions = Event.query\
		.add_columns(Event.name.label("event_name"))\
		.add_columns(Event.id.label("event_id"))\
		.join(Divisions, Divisions.event_id == Event.id)\
		.add_columns(Divisions.id.label("division_id"))\
		.add_columns(Divisions.division_leader.label("division_leader"))\
		.add_columns(Divisions.division_name.label("division_name"))\
		.where(Event.superadmin_id == event_host_id)

		divisions = divisions.all()
			
	print(divisions)
	next=request.args.get("next")
	if next:
		return redirect(next) 


		
	return render_template("division.html", divisionCreateForm=form, divisions=divisions)


#