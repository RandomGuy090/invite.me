from flask import render_template, redirect, session, url_for, request, flash
from flask_login import login_user, current_user, login_required

from src.models import User, Participants, Event, unique_str, Divisions
from src.config import app, db

from src.email_sending.email_utils import Code_email



def create_participant(*args, **kwargs):
	# def create_participant(first_name, last_name, email, added_by_id, event, division, division_leader=None):
	first_name =  kwargs.get("first_name")
	last_name =  kwargs.get("last_name")
	email = kwargs.get("email")
	added_by_id = kwargs.get("added_by_id")
	event =  kwargs.get("event")
	division =   kwargs.get("division")
	division_leader =  kwargs.get("division_leader")
	is_vip =  kwargs.get("is_vip")

	event_host_id = current_user.id if current_user.superadmin else  current_user.added_by
	declaration_string = unique_str(Participants, 48, field="declaration_string")
	invitation_string = unique_str(Participants, 64, field = "invitation_string")


	# first_name, last_name and email are necessary, return false when not defined
	if  email == "":
		return False

	event = Event.query.filter_by(name=event, superadmin_id=event_host_id).first()
	division_qr = Divisions.query.filter_by(division_name=division, superadmin_id=event_host_id).first()
	print(f"division qr {division_qr}")

	if not division_qr:
		if division_leader:
			print(f"division leader defined")
			# create nev division if leader defined
			new_division = Divisions(
				division_name=division,
				division_leader=division_leader,
				event_id=event.id,
				superadmin_id=event_host_id)

			# when division created
			if new_division:
				db.session.add(new_division)
				db.session.commit()
				division_id = new_division.id
				
			else:
				raise Exception(f"couldn't create new division {new_division}")
		else:
			raise Exception(f"cannot create new division {division} division leader not provided. Create division or add 'division_leader' columnt to csv file")
	else:
		# division exists
		division_id = division_qr.id
		
	# division already exists
	# print(f"division_qr {division_qr.id}")
	# division_id = division_qr.id
	print(f"division_id {division_id}")

	new_participant = Participants(first_name=first_name,
		last_name=last_name,
		email=email,
		added_by_id = added_by_id,
		event_id=event.id,
		declaration_string=declaration_string,
		division_id=division_id,
		is_vip=is_vip,
		invitation_string=invitation_string)
		# return False
	return new_participant
