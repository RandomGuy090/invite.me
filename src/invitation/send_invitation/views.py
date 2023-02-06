from flask import render_template, redirect, session, url_for, request, flash, render_template_string
from flask.views import View

import time, random

from src.models import User
from src.config import db, app, mail, lang
from flask_login import login_user, current_user, login_required

from src.models import User, Participants, Event, Divisions, Accompanying
from src.handlers.views import autherntication_required
from src.email_sending.email_utils import Invitation_mail
from threading import Thread



def  send_invitation_mail(particip, form=None):
	imgs = []
	recipients = []
	# mail = Code_email(form, event_name=particip.event_name)
	mail = Invitation_mail(form, event_name=f"{lang.email_subject_invitation}: {particip.event_name}")
	
	
	link = f"{app.config['APPLICATION_ROOT']}{url_for('invitation.get')}?invitation={particip.participant_invitation_string}"
	img = f"https://api.qrserver.com/v1/create-qr-code/?size={app.config['QR_CODE_RES']}&data={link}"
	imgs.append({"first_name":particip.participant_first_name,
		"link": link,
		"img": img})
	if particip.accompanying_person_email:
		print(f"acc. person {particip.accompanying_person_email}")
		recipients.append(particip.accompanying_person_email)
		
		link = f"{app.config['APPLICATION_ROOT']}{url_for('invitation.get')}?invitation={particip.accompanying_invitation_string}"
		img = f"https://api.qrserver.com/v1/create-qr-code/?size={app.config['QR_CODE_RES']}&data={link}"
		imgs.append({"first_name": particip.accompanying_first_name,
			"link": link,
			"img": img})

	
	content = particip.event_invitation_email_content
	content = content.replace("{{  }}","")
	content = render_template_string(content, participant=particip, link=link, lang=lang)
	if not particip.accompanying_person_email:
		content = content.replace("participant.accompanying_first_name","")
		content = content.replace("participant.accompanying_last_name","")
		content = content.replace("{{  }}","")
	content = content.replace("00:00:00","")
	content = content.replace(str(particip.event_date), str(particip.event_date.strftime("%d.%m.%Y")))
	content = content.replace(str(particip.event_time), str(particip.event_time.strftime("%H:%M")))
	content = content.replace("&amp;", "&")
	content = content.replace(":00:00",":00")
	content = content.replace("None","")
	html_body = render_template("invitation_mail.html", participant=particip, link=link, lang=lang, content=content, imgs=imgs)

	mail.html_body = html_body
	recipients.append(particip.participant_email)


	mail.send(recipients=recipients)
	
	p = Participants.query.filter_by(id=particip.participant_id).first()
	p.invitation_sent = True
	db.session.add(p)
	db.session.commit()




@login_required
@autherntication_required
def send():
	event_host_id = current_user.id if current_user.superadmin else  current_user.added_by

	division = request.args.get("division")
	participant_id = request.args.get("participant")
	event = request.args.get("event")
	next = request.args.get("next")


	if not event:
		return "no such event"

	# events = Event.query.filter_by(id=event).all()
	
	participant = Participants.query\
	.add_columns(Participants.id.label("participant_id"),
		Participants.first_name.label("participant_first_name"),
		Participants.first_name_by_user.label("participant_first_name_by_user"),
		Participants.last_name.label("participant_last_name"),
		Participants.last_name_by_user.label("participant_last_name_by_user"),
		Participants.declaration_sent.label("participant_declaration_sent"),
		Participants.declarated.label("participant_declarated"),
		Participants.invitation_sent.label("participant_invitation_sent"),
		Participants.invitation_string.label("participant_invitation_string"),
		Participants.canceled.label("particip_canceled"),
		Participants.declaration_string.label("participant_declaration_string"),
		Participants.event.label("participant_event"),
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
		Event.place_img.label("event_place_img"),
		Event.contact_to_organizators.label("event_contact_to_organizators"),
		Event.image_link_header.label("event_image_link_header"),
		Event.image_link_footer.label("event_image_link_footer"),	
		Event.invitation_mail_content.label("event_invitation_email_content"),
		Event.date.label("event_date"),
		Event.time.label("event_time")
		,)\
	.join(Divisions, Participants.division_id == Divisions.id, isouter=True)\
		.add_columns(
		Divisions.id.label("division_id"),
		Divisions.division_name.label("division_name"),
		)\
	.where(Event.id == int(event),  Event.superadmin_id == event_host_id)
	
	if participant_id:
		print(f"participant taken")
		participant = participant.where(Participants.id == participant_id)
	
	if division:
		participant = participant.where(Divisions.id == division)


	recipients = []
	for elem in participant:
		if not participant_id and elem.participant_invitation_sent:
			flash(f"you have already send invitation to {elem.participant_email}, send it personally")
			continue

		if app.INVITATION_ONLY_AFTER_DECLARATION_SENT == True:
			if not elem.participant_declaration_sent:
				flash(f"you must send declaration first {elem.participant_email}")
				continue
				# return redirect(next)

		if app.INVITATION_ONLY_AFTER_DECLARATED == True:
			if not elem.participant_declarated:
				flash(f"user isn't declarated: {elem.participant_email}")
				continue
		
			# return redirect(next)		 
		if elem.particip_canceled:
			flash(f"user has cancelled declaration: {elem.participant_email}")
			continue
		if ( elem.participant_invitation_sent == False ) or (elem.participant_invitation_sent == True and app.SEND_AGAIN == True):

			# print(f"participants to send {elem}")
			send_invitation_mail(elem)
			# thr = Thread(target=self.send_async_email, args=[elem])
			# thr.start()



	if next:
		return redirect(next)
	return "email sent successfuly"




 