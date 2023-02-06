from flask import render_template, redirect, session, url_for, request
from flask.views import View

from src.models import User
from src.config import db, app
from flask_login import login_user, current_user, login_required

from src.models import User, Participants, Event, Divisions
from src.handlers.views import autherntication_required

from src.participant.create.forms import NewParticipantForm




@login_required
@autherntication_required
def get():
	form = NewParticipantForm()
	event = request.args.get("event")
	division = request.args.get("division")
	print(f"----{event}")

	event_host_id = current_user.id if current_user.superadmin else  current_user.added_by

	# if event:
	# 	# participants = Event.query\
	# 	# 	.join(Participants, Participants.event_id == Event.id)\
	# 	# 	.add_columns(Participants.id.label("participant_id"), 
	# 	# 	Participants.first_name.label("participant_first_name"), 
	# 	# 	Participants.last_name.label("participant_last_name"), 
	# 	# 	Participants.email.label("participant_email"),
	# 	# 	Participants.declarated.label("participant_declarated"), 
	# 	# 	Participants.added_by_id.label("participant_added_by"),
	# 	# 	Participants.division_id.label("participant_division_id"),
	# 	# 	Event.name.label("event_name"))\
	# 	# 	.join(User, User.id == Event.superadmin_id)\
	# 	# 	.add_columns(User.email.label("User_email"))\
	# 	# 	.join(Divisions, Divisions.event_id == Participants.division_id)\
	# 	# 	.where(User.id == event_host_id, Event.id == event)

	# 	participants = Participants.query\
	# 	.add_columns(
	# 		Participants.id.label("participant_id"),
	# 		Participants.first_name.label("participant_first_name"),
	# 		Participants.last_name.label("participant_last_name"),
	# 		Participants.added_by.label("participant_added_by"),
	# 		Participants.declaration_string.label("participant_declaration_string"),
	# 		Participants.declaration_sent.label("participant_declaration_sent"), 
	# 		Participants.invitation_string.label("participant_invitation_string"),
	# 		Participants.invitation_sent.label("participant_invitation_sent"), 
	# 		Participants.canceled.label("participant_canceled"), 
	# 		Participants.email.label("participant_email"))\
	# 	.join(Divisions, Divisions.id == Participants.division_id)\
	# 	.add_columns(Divisions.id.label("division_id"),
	# 		Divisions.division_name.label("division_name"),
	# 		Divisions.division_leader.label("division_leader"),)\
	# 	.join(Event, Event.id == Participants.event_id)\
	# 	.add_columns(
	# 		Event.id.label("event_id"),
	# 		Event.name.label("event_name"),
	# 		).where(Event.id == event).group_by(Participants.id)
	# else:
	# 	# participants = Event.query\
	# 	# 	.join(Participants, Participants.event_id == Event.id)\
	# 	# 	.add_columns(Participants.id.label("participant_id"), 
	# 	# 	Participants.first_name.label("participant_first_name"), 
	# 	# 	Participants.last_name.label("participant_last_name"), 
	# 	# 	Participants.email.label("participant_email"),
	# 	# 	Participants.declarated.label("participant_declarated"), 
	# 	# 	Participants.added_by_id.label("participant_added_by"),
	# 	# 	Event.name.label("event_name"))\
	# 	# 	.join(User, User.id == Event.superadmin_id)\
	# 	# 	.add_columns(User.email.label("User_email"))\
	# 	# 	.join(Divisions, Divisions.event_id == Participants.division_id)\
	# 	# 	.add_columns(Divisions.division_name.label("participant_division_id"))\
	# 	# 	.where(User.id == event_host_id)
	# 	participants = Participants.query\
	# 	.add_columns(Participants.id.label("participant_id"),
	# 		Participants.first_name.label("participant_first_name"),
	# 		Participants.last_name.label("participant_last_name"),
	# 		Participants.declarated.label("participant_declarated"),
	# 		Participants.canceled.label("participant_canceled"), 
	# 		Participants.declaration_string.label("participant_declaration_string"),
	# 		Participants.invitation_string.label("participant_invitation_string"),
	# 		Participants.invitation_sent.label("participant_invitation_sent"), 
	# 		Participants.email.label("participant_email"))\
	# 	.join(Divisions, Divisions.id == Participants.division_id)\
	# 	.add_columns(Divisions.id.label("division_id"),
	# 		Divisions.division_name.label("division_name"),
	# 		Divisions.division_leader.label("division_leader"),)\
	# 	.join(Event, Event.id == Participants.event_id)\
	# 	.add_columns(
	# 		Event.id.label("event_id"),
	# 		Event.name.label("event_name"),
	# 		).group_by(Participants.id)
	
	participants = Participants.query\
	.add_columns(Participants.id.label("participant_id"),
		Participants.first_name.label("participant_first_name"),
		Participants.last_name.label("participant_last_name"),
		Participants.is_vip.label("participant_is_vip"),
		Participants.declarated.label("participant_declarated"),
		Participants.canceled.label("participant_canceled"), 
		Participants.declaration_string.label("participant_declaration_string"),
		Participants.invitation_string.label("participant_invitation_string"),
		Participants.invitation_sent.label("participant_invitation_sent"), 
		Participants.email.label("participant_email"))\
	.join(Divisions, Divisions.id == Participants.division_id)\
	.add_columns(Divisions.id.label("division_id"),
		Divisions.division_name.label("division_name"),
		Divisions.division_leader.label("division_leader"),)\
	.join(Event, Event.id == Participants.event_id)\
	.add_columns(
		Event.id.label("event_id"),
		Event.name.label("event_name"),
		).group_by(Participants.id)
	
	participants = participants.group_by(Participants.id)
	
	if event:
		participants = participants.where(Event.id == event)

	if division:
		participants = participants.where(Divisions.id == division)

	participants = participants.all()

	
	next=request.args.get("next")
	if next:
		return redirect(next) 

		
	return render_template("participants.html", participantCreateForm=form, participants=participants)


#