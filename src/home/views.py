from flask import render_template, redirect, session, Blueprint, request

from src.models import User, Event, Participants
from src.config import db, mail
from flask_login import UserMixin, login_user, LoginManager, current_user, login_required

from src.models import User, Divisions
from src.handlers.views import autherntication_required, superadmin_required

from src.participant.create.forms import NewParticipantForm

from src.event.create.form import CreateEventForm
from src.division.create.forms import NewDivisionForm

from src.admins.register.forms import RegisterAdminForm
from src.admins.get.forms import GetAdminForm





@autherntication_required
@login_required
def home():
	user = current_user

	event = request.args.get("event")
	
	event_host_id = current_user.id if current_user.superadmin else  current_user.added_by

	participants = Event.query\
		.join(Participants, Participants.event_id == Event.id)\
		.add_columns(Participants.id.label("participant_id"), 
		Participants.first_name.label("participant_first_name"), 
		Participants.declaration_string.label("participant_declaration_string"),
		Participants.invitation_string.label("participant_invitation_string"),
		Participants.last_name.label("participant_last_name"), 
		Participants.email.label("participant_email"),
		Participants.is_vip.label("participant_is_vip"),
		Participants.declarated.label("participant_declarated"), 
		Participants.declaration_sent.label("participant_declaration_sent"), 
		Participants.invitation_sent.label("participant_invitation_sent"), 
		Participants.canceled.label("participant_canceled"), 
		Participants.added_by_id.label("participant_added_by"),
		Event.name.label("event_name"),
		Event.id.label("event_id"))\
		.join(User, User.id == Event.superadmin_id)\
		.add_columns(User.email.label("User_email"))\
		.join(Divisions, Participants.division_id == Divisions.id)\
		.add_columns(Divisions.division_name.label("division_name"))\
		.where(User.id == event_host_id)

	divisions = Event.query\
		.add_columns(Event.name.label("event_name"))\
		.add_columns(Event.id.label("event_id"))\
		.join(Divisions, Divisions.event_id == Event.id)\
		.add_columns(Divisions.id.label("division_id"))\
		.add_columns(Divisions.superadmin_id.label("superadmin_id"))\
		.add_columns(Divisions.division_leader.label("division_leader"))\
		.add_columns(Divisions.division_name.label("division_name"))\
		.filter_by(superadmin_id=event_host_id)

	if event:
		divisions = divisions.where(Event.id == event, Event.superadmin_id == event_host_id)
		participants = participants.where(User.id == event_host_id, Event.id == event)


	divisions = divisions.all()


	# events = Event.query.all()
	if current_user.added_by:
		events = Event.query.filter_by(superadmin_id=current_user.added_by).all()
	else:
		events = Event.query.filter_by(superadmin_id=current_user.id).all()

	

	users = User.query.filter_by(added_by=current_user.id).all()		
	

	return render_template("index.html", user=user, 
		participants=participants, 
		events=events,
		users=users,
		divisions=divisions,
		participantCreateForm=NewParticipantForm(),
		eventCreateForm=CreateEventForm(),
		RegisterAdminForm=RegisterAdminForm(),
		divisionCreateForm=NewDivisionForm(),
		GetAdminForm=GetAdminForm(),
		next="/")

	return f"you arent logged"

