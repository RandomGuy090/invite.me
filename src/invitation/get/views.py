from flask import render_template, redirect, session, url_for, request, flash, render_template_string

from flask_login import login_user, logout_user, login_required, current_user


from src.models import User, specific_string, Participants, Event, Enters, Accompanying
from src.config import db,  app, lang
from src.email_sending.email_utils import Register_email

from src.handlers.views import autherntication_required

def check_permissions(user, invitation_string):
	if current_user.is_authenticated:
		participant = Participants.query.filter_by(invitation_string=invitation_string).first()
		
		if not participant or participant == None:
			participant = Accompanying.query.filter_by(invitation_string=invitation_string).first()

		if participant == None:
			return False
		event = Event.query.filter_by(id=participant.event_id).first()			


		if not participant:
			return False

		
		if current_user.superadmin:
			if current_user.id == event.superadmin_id:
				return True

		if current_user.added_by == event.superadmin_id:
			return True
	return False


# @login_required
# @autherntication_required
def get():
	invitation_string = request.args.get("invitation")
	admin = request.args.get("admin")

	inv_of_particip = False


	if Participants.query.filter_by(invitation_string=invitation_string).first():
		inv_of_particip = True
		participant = Participants.query\
		.add_columns(Participants.id.label("participant_id"),
			Participants.first_name.label("participant_first_name"),
			Participants.first_name_by_user.label("participant_first_name_by_user"),
			Participants.last_name.label("participant_last_name"),
			Participants.last_name_by_user.label("participant_last_name_by_user"),
			Participants.declaration_sent.label("participant_declaration_sent"),
			Participants.invitation_sent.label("participant_invitation_sent"),
			Participants.invitation_string.label("participant_invitation_string"),
			Participants.declaration_string.label("participant_declaration_string"),
			Participants.event_id.label("participant_event_id"),
			Participants.declarated.label("participant_declarated"),
			Participants.email.label("participant_email"))\
		.join(Accompanying, Accompanying.id == Participants.accomapnying_id, isouter=True)\
		.add_columns(
			Accompanying.id.label("accompanying_person_id"),
			Accompanying.email.label("accompanying_person_email"),
			Accompanying.first_name.label("accompanying_first_name"),
			Accompanying.last_name.label("accompanying_last_name"),
			Accompanying.invitation_string.label("accompanying_invitation_string"),
			)\
		.join(Event, Event.id == Participants.event_id, isouter=True)\
		.add_columns(
			Event.name.label("event_name"),
			Event.google_map_link.label("event_google_map_link"),
			Event.google_map_iframe.label("event_google_map_iframe"),
			Event.address.label("event_address"),
			Event.contact_to_organizators.label("event_contact_to_organizators"),
			Event.image_link_header.label("event_image_link_header"),
			Event.image_link_footer.label("event_image_link_footer"),
			Event.invitation_mail_content.label("event_invitation_mail_content"),
			Event.place_img.label("event_place_img"),
			Event.time.label("event_time"),
			Event.date.label("event_date"),)\
		.where(Participants.invitation_string == invitation_string).first()
	else:
		participant = Participants.query\
		.add_columns(Participants.id.label("participant_id"),
			Participants.first_name.label("participant_first_name"),
			Participants.first_name_by_user.label("participant_first_name_by_user"),
			Participants.last_name.label("participant_last_name"),
			Participants.last_name_by_user.label("participant_last_name_by_user"),
			Participants.declaration_sent.label("participant_declaration_sent"),
			Participants.invitation_sent.label("participant_invitation_sent"),
			Participants.invitation_string.label("participant_invitation_string"),
			Participants.declaration_string.label("participant_declaration_string"),
			Participants.declarated.label("participant_declarated"),
			Participants.event_id.label("participant_event_id"),
			Participants.email.label("participant_email"))\
		.join(Accompanying, Accompanying.id == Participants.accomapnying_id, isouter=True)\
		.add_columns(
			Accompanying.id.label("accompanying_person_id"),
			Accompanying.email.label("accompanying_person_email"),
			Accompanying.first_name.label("accompanying_first_name"),
			Accompanying.last_name.label("accompanying_last_name"),
			Accompanying.invitation_string.label("accompanying_invitation_string"),
			)\
		.join(Event, Event.id == Participants.event_id, isouter=True)\
		.add_columns(
			Event.name.label("event_name"),
			Event.time.label("event_time"),
			Event.google_map_link.label("event_google_map_link"),
			Event.google_map_iframe.label("event_google_map_iframe"),
			Event.address.label("event_address"),
			Event.place_img.label("event_place_img"),
			Event.contact_to_organizators.label("event_contact_to_organizators"),
			Event.image_link_header.label("event_image_link_header"),
			Event.image_link_footer.label("event_image_link_footer"),
			Event.invitation_mail_content.label("event_invitation_mail_content"),
			Event.date.label("event_date"),)\
		.where(Accompanying.invitation_string == invitation_string).first()
	

	# participant.event_date = 
	# participant.event_time = str(participant.event_time)[str(participant.event_time).index(":"):]


	if not participant:
		flash(lang.declaration_is_invalid)
		return render_template("invitation.html")

	# if not participant.participant_declarated and  participant.participant_invitation_sent == False:
	# 	flash(lang.user_isnt_declarated)
	# 	return render_template("invitation.html")

		# return "user isn't declarated"

	if not participant:
		return "no such user"

	imgs = []
	recipients = []
	link = f"{app.config['APPLICATION_ROOT']}{url_for('invitation.get')}?invitation={participant.participant_invitation_string}"
	img = f"https://api.qrserver.com/v1/create-qr-code/?size={app.config['QR_CODE_RES']}&data={link}"
	imgs.append({"first_name":participant.participant_first_name,
		"link": link,
		"img": img})
	if participant.accompanying_person_email:
		recipients.append(participant.accompanying_person_email)
		
		link = f"{app.config['APPLICATION_ROOT']}{url_for('invitation.get')}?invitation={participant.accompanying_invitation_string}"
		img = f"https://api.qrserver.com/v1/create-qr-code/?size={app.config['QR_CODE_RES']}&data={link}"
		imgs.append({"first_name": participant.accompanying_first_name,
			"link": link,
			"img": img})

	content = participant.event_invitation_mail_content

	print(f"participant.accompanying_first_name {participant.accompanying_first_name}")
	print(f"participant.accompanying_last_name {participant.accompanying_last_name}")
	print(f"participant.accompanying_person_email {participant.accompanying_person_email}")

	# if not participant.accompanying_person_email:
	if not participant.accompanying_last_name:
		content = content.replace("participant.accompanying_first_name","")
		content = content.replace("participant.accompanying_last_name","")
		content = content.replace("{{  }}","")
	# print(content)
	content = render_template_string(content, participant=participant, link=link, lang=lang)
	content = content.replace("00:00:00","")
	content = content.replace(str(participant.event_date), str(participant.event_date.strftime("%d.%m.%Y")))
	content = content.replace(str(participant.event_time), str(participant.event_time.strftime("%H:%M")))
	content = content.replace("&amp;", "&")
	content = content.replace(":00:00",":00")
	content = content.replace("None","")

	if check_permissions(current_user, invitation_string) and (admin == False or admin == None) :
		print("user is logged")
		if not participant:
			return "no such user"

		has_entered = False

		if inv_of_particip:
			ent = Enters.query.filter_by(participant_id=participant.participant_id).order_by(Enters.id.desc()).first()
		else:
			ent = Enters.query.filter_by(accompanying_id=participant.accompanying_person_id).order_by(Enters.id.desc()).first()


	
		if ent :
			#user has already been registered

			if ent.has_entered :
				print("participant leaves the building")
				has_entered = False

			else:
				print("participant enters the building")
				has_entered = True

		else:
			# first time
			print("participant enters to the building first time")

			has_entered = True


		if inv_of_particip:
			enter = Enters(has_entered=has_entered,
				participant_id=participant.participant_id,
				recorded_by_id=current_user.id,
				event_id=participant.participant_event_id)
		else:
			enter = Enters(has_entered=has_entered,
				accompanying_id=participant.accompanying_person_id,
				recorded_by_id=current_user.id,
				event_id=participant.participant_event_id)


		db.session.add(enter)
		db.session.commit()

		enters = Enters.query\
		.add_columns(
			Enters.date.label("enter_date"),
			Enters.has_entered.label("enter_has_entered"),
			Enters.recorded_by_id.label("enter_recorded_by_id"),
			)\
		.join(Participants, Participants.id == Enters.participant_id, isouter=True)\
		.add_columns(
			Participants.first_name.label("participant_first_name"),
			Participants.last_name.label("participant_last_name"),
			Participants.invitation_string.label("participant_invitation_string"),
			)\
		.join(Accompanying, Accompanying.id == Enters.accompanying_id, isouter=True)\
		.add_columns(
			Accompanying.first_name.label("accompanying_first_name"),
			Accompanying.last_name.label("accompanying_last_name"),
			Accompanying.invitation_string.label("accompanying_invitation_string"),
			)\
		.join(User, User.id == Enters.recorded_by_id)\
		.add_columns(
			User.email.label("user_recorded_by_id"),
			)\
		.where(Enters.event_id == participant.participant_event_id)

		if inv_of_particip:
			enters = enters.where(Participants.invitation_string == invitation_string)
		else:
			enters = enters.where(Accompanying.invitation_string == invitation_string)
		enters = enters.all()


		# Enters()
		
		# return "admin"
		return render_template("invitation.html", participant=participant, content=content, imgs=imgs, enters=enters, lang=lang)



	else:
		if not participant:
			return render_template("invitation.html", errors="Invitation is invalid")
	
		return render_template("invitation.html", participant=participant, imgs=imgs,content=content,  lang=lang)





