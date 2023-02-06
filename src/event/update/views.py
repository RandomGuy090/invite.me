from flask import render_template, redirect, session, url_for, request, flash, render_template_string
from flask.views import View

from src.models import User
from src.config import db , app, mail, lang
from flask_login import login_user, current_user, login_required

from src.models import User, Participants, Event, Divisions, Accompanying
from src.handlers.views import autherntication_required, superadmin_required

from src.event.create.form import CreateEventForm
from src.event.create.utils import parse_google_map_link, parse_google_map_iframe

from .example_data import dummy_invitation, dummy_declaration, dummy_participant




@superadmin_required
@login_required
@autherntication_required
def update():
	event_id = request.args.get("event_id")
	declaration_string = request.args.get("declaration_string")
	form = CreateEventForm()
	
	if current_user.added_by:
		events = Event.query.filter_by(superadmin_id=current_user.added_by)
	else:
		events = Event.query.filter_by(superadmin_id=current_user.id)


	event = events.filter_by(id=event_id).first()
	# event = Event.query.filter_by(id=event).first()
	if not event:
		flash(lang.no_events)
		return render_template("event_update.html")

	particip = Participants.query.filter_by(event_id = event_id).all()
	inv_sent = False


	if app.UPDATE_EVENT_AFTER_SEND == False:
		for elem in particip:
			if elem.invitation_sent:
				inv_sent = True
		if inv_sent:
			flash(lang.invitation_already_sent)
			return render_template("event_update.html")



	if form.validate_on_submit():

		if form.name.data: event.name = form.name.data

		if form.datetime.data: 
			time = form.datetime.data.strftime("%H:%M")
			event.time = time


		if form.delcaration_deadline.data: 
			# event.date = form.data.data
			date = form.delcaration_deadline.data.strftime("%Y-%m-%d")
			date = f"{date} {event.time}"
			event.delcaration_deadline = date

		if form.address.data: event.address = form.address.data
		if form.google_map_iframe.data: event.google_map_iframe = parse_google_map_iframe(form.google_map_iframe.data)
		if form.google_map_link.data: event.google_map_link = parse_google_map_link(form.google_map_link.data)
		if form.place_img.data: event.place_img = form.place_img.data
		if form.declaration_mail_content.data: event.declaration_mail_content = form.declaration_mail_content.data
		if form.invitation_mail_content.data: event.invitation_mail_content = form.invitation_mail_content.data
		
		if form.contact_to_organizators.data: event.contact_to_organizators = form.contact_to_organizators.data
		
		db.session.add(event)
		db.session.commit()

		next=request.args.get("next")
		if next:
			return redirect(next) 

	form.datetime.data = str(event.date).replace(" ", "T")

	dummy_particip = dummy_participant(event)

	return render_template("event_update.html", eventUpdateForm=form, 
		event=event, 
		lang=lang,  
		participant=dummy_particip,
		content_invitation=dummy_invitation(dummy_particip), 
		content_declaration=dummy_declaration(dummy_particip))
	# return redirect(url_for("events.get"))
	# 
	# return redirect(url_for("declarate.get", declaration_string=declaration_string))


#