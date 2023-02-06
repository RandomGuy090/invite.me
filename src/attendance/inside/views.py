from flask import render_template, redirect, session, url_for, request, flash, render_template_string, json
from flask_login import login_user, logout_user, login_required, current_user

from src.models import User, specific_string, Participants, Event, Enters, Accompanying
from src.config import db,  app, lang
from src.handlers.views import autherntication_required
from src.models import User, specific_string, Participants, Event, Enters, Accompanying
from src.invitation.get.views import check_permissions
from src.attendance.utils import json_response


def att_inside():
	invitation_string = request.args.get("invitation_string")


	print(invitation_string)
	if invitation_string == None:	

		return json_response(content={"info":"invitaiton invalid", "details":"no invitaiton string"}, code=404)



	if check_permissions(current_user, invitation_string) :
		print("user is logged")

		# is it a participant or an accompanying person?
		# True means its participant, False its accompany

		user_not_acc = True

		participant = Participants.query.filter_by(invitation_string = invitation_string).first()
		if participant == None:
			user_not_acc = False
			participant = Accompanying.query.filter_by(invitation_string = invitation_string).first()


		# return f"{ participant.first_name} { participant.last_name}"

		if not participant:
			return json_response(content={"info":"invitaiton invalid", "details":"no such user"}, code=404)


		if user_not_acc:
			# this is when participant checks in
			enter = Enters(has_entered=True,
				participant_id=participant.id,
				recorded_by_id=current_user.id,
				event_id=participant.event_id)
		else:
			# when accompanying checks in

			enter = Enters(has_entered=True,
				accompanying_id=participant.id,
				recorded_by_id=current_user.id,
				event_id=participant.event_id)
		
		db.session.add(enter)
		db.session.commit()

		details = {
			"info": "user registered into event",
			"first_name" : participant.first_name,
			"last_name" : participant.last_name,

		}
		return json_response(content={"info":"ok", "details": details }, code=200)



	else:
		return json_response(content={"info":"invitaiton invalid", "details":"no invitaiton string"}, code=404)


		# return render_template("invitation.html", errors="Invitation is invalid")
	


