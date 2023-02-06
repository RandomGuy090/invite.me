from flask import render_template, redirect, session, url_for, request, render_template_string, flash
from flask.views import View

from src.models import User
from src.config import db, app, mail, lang
from flask_login import login_user, current_user, login_required

from src.models import User, Participants, Event, Divisions, Accompanying
from src.handlers.views import autherntication_required
from src.email_sending.email_utils import Declaration_email



def send_declaration_mail(particip, form=None):

	mail = Declaration_email(form, event_name=f"{lang.declaration_for}: {particip.event_name}")
	# mail.text_body =  f"your activation link is: http://{url}" 
	link = f"{app.config['APPLICATION_ROOT']}{url_for('declarate.get')}?declaration_string={particip.participant_declaration_string}"

	content = particip.event_declaration_email_content
	content = content.replace("{{  }}","")

	content = render_template_string(particip.event_declaration_email_content, participant=particip, link=link, lang=lang)
	content = content.replace("00:00:00","")
	content = content.replace(str(particip.event_date), str(particip.event_date.strftime("%d.%m.%Y")))
	content = content.replace(str(particip.event_time), str(particip.event_time.strftime("%H:%M")))
	content = content.replace("&amp;", "&")
	content = content.replace(":00:00",":00")
	content = content.replace("None","")
	html_body = render_template("declaration_mail.html", participant=particip, link=link, lang=lang, content=content)

	mail.html_body = html_body
	recipients = [particip.participant_email]

	mail.send(recipients=recipients)

	p = Participants.query.filter_by(id=particip.participant_id).first()
	p.declaration_sent = True
	db.session.add(p)
	db.session.commit()



@login_required
@autherntication_required
def send():
	event_host_id = current_user.id if current_user.superadmin else  current_user.added_by

	participant = request.args.get("participant")
	event = request.args.get("event")
	division = request.args.get("division")

	next = request.args.get("next")


	if not event:
		return "no such event"

	events = Event.query.filter_by(id=event).all()
	
	qr = Participants.query\
	.add_columns(Participants.id.label("participant_id"),
		Participants.first_name.label("participant_first_name"),
		Participants.first_name_by_user.label("participant_first_name_by_user"),
		Participants.last_name.label("participant_last_name"),
		Participants.last_name_by_user.label("participant_last_name_by_user"),
		Participants.declaration_sent.label("participant_declaration_sent"),
		Participants.declaration_string.label("participant_declaration_string"),
		Participants.event.label("participant_event"),
		Participants.email.label("participant_email"))\
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
		Event.declaration_mail_content.label("event_declaration_email_content"),
		Event.time.label("event_time"),
		Event.date.label("event_date"))\
	.join(Divisions, Participants.division_id == Divisions.id, isouter=True)\
		.add_columns(
		Divisions.id.label("division_id"),
		Divisions.division_name.label("division_name"),
		)\
	.where(Event.id == int(event),  Event.superadmin_id == event_host_id)
	# Event.date = Event.date.rsplit(" ")[1]
	
	if participant:
		qr = qr.where(Participants.id == int(participant))
	
	if division:
		qr = qr.where(Divisions.id == int(division))

	qr = qr.all()

	recipients = []
	for elem in qr:
		if not participant and elem.participant_declaration_sent:
			flash(f"you have already send declaration to {elem.participant_email}, send it personally")
			continue

		# if not elem.participant_declaration_sent:
		if ( elem.participant_declaration_sent == False ) or (elem.participant_declaration_sent == True and app.SEND_AGAIN == True):
			send_declaration_mail(elem)

	print(recipients)
		


	if next:
		return redirect(next)
	return "email sent successfuly"




 