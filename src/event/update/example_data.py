from src.models import  Participants
from src.config import db , app, mail, lang
from flask import render_template, redirect, session, url_for, request, flash, render_template_string


def dummy_participant(event):

	dum_particip = Participants()
	dum_particip.participant_first_name = "John"
	dum_particip.participant_first_name_by_user = "John"
	dum_particip.participant_last_name = "smith"
	dum_particip.participant_last_name_by_user = "smith"
	dum_particip.participant_declaration_sent = False
	dum_particip.participant_declarated = False
	dum_particip.participant_invitation_sent = False
	dum_particip.participant_invitation_string = "dummy_invitation_string"
	dum_particip.participant_declaration_string = "dummy_declaration_string"
	dum_particip.participant_email = "john.smith@gmail.com"
	
	dum_particip.participant_event = "Event_Name"
	dum_particip.accompanying_person_id = 99
	dum_particip.accompanying_person_email = "jane.smith@gmail.com"
	dum_particip.accompanying_first_name = "Jane"
	dum_particip.accompanying_last_name = "Smith"
	dum_particip.accompanying_invitation_string = "dummy_invitation_string"

	dum_particip.event_name = event.name
	dum_particip.event_google_map_link = event.google_map_link
	dum_particip.event_google_map_iframe = event.google_map_iframe
	dum_particip.event_address = event.address
	dum_particip.event_place_img = event.place_img
	dum_particip.event_invitation_mail_content = event.invitation_mail_content
	dum_particip.event_declaration_mail_content = event.declaration_mail_content
	dum_particip.event_date = event.date
	dum_particip.event_time = event.time

	return dum_particip

def dummy_declaration(particip):
	link = f"{app.config['APPLICATION_ROOT']}{url_for('declarate.get')}?declaration_string={particip.participant_declaration_string}"

	content = particip.event_declaration_mail_content
	content = content.replace("{{  }}","")

	content = render_template_string(particip.event_declaration_mail_content, participant=particip, link=link, lang=lang)
	content = content.replace("00:00:00","")
	content = content.replace(str(particip.event_date), str(particip.event_date.strftime("%d.%m.%Y")))
	content = content.replace(str(particip.event_time), str(particip.event_time.strftime("%H:%M")))
	content = content.replace("&amp;", "&")
	content = content.replace(":00:00",":00")
	content = content.replace("None","")
	# html_body = render_template("declaration_mail.html", participant=particip, link=link, lang=lang, content=content)


	return content

def dummy_invitation(particip):
	imgs = []
	recipients = []

	link = f"{app.config['APPLICATION_ROOT']}{url_for('invitation.get')}?invitation={particip.participant_invitation_string}"
	img = f"https://api.qrserver.com/v1/create-qr-code/?data={link};size={app.config['QR_CODE_RES']}"
	imgs.append({"first_name":particip.participant_first_name,
		"link": link,
		"img": img})

	if particip.accompanying_person_email:
		recipients.append(particip.accompanying_person_email)
		
		link = f"{app.config['APPLICATION_ROOT']}{url_for('invitation.get')}?invitation={particip.accompanying_invitation_string}"
		img = f"https://api.qrserver.com/v1/create-qr-code/?data={link};size={app.config['QR_CODE_RES']}"
		imgs.append({
			"first_name": particip.accompanying_first_name,
			"link": link,
			"img": img})

	content = particip.event_invitation_mail_content
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

	# html_body = render_template("invitation_mail.html", participant=particip, link=link, lang=lang, content=content, imgs=imgs)
	return {"content":content, "imgs":imgs}
