from flask import render_template, redirect, session, request, url_for, flash
from flask_login import login_user, login_required, current_user
from wtforms.validators import ValidationError

from src.handlers.views import autherntication_required, superadmin_required

from src.models import User, Event
from src.config import db, mail, app 

# from ..get.form import EventForm
from ..create.form import CreateEventForm
import time
from datetime import datetime

from .utils import parse_google_map_link, parse_google_map_iframe

@superadmin_required
@autherntication_required
@login_required
def create():
	form = CreateEventForm()
	next = request.args.get("next")
	if request.method == "POST":
		if form.validate_on_submit():
			if current_user:
				
				try:
					event = Event()
					if form.name.data: event.name = form.name.data
					if form.contact_to_organizators.data: event.contact_to_organizators = form.contact_to_organizators.data

					if form.datetime.data: 
						time = form.datetime.data.strftime("%H:%M")
						event.time = time
						print(f"event_time. {event.time}")


					if form.datetime.data: 
						# event.date = form.data.data
						date = form.datetime.data.strftime("%Y-%m-%d")
						date = f"{date} {event.time}"
						event.date = date
						print(f"event_date. {event.date}")

					if form.delcaration_deadline.data: 
						# event.date = form.data.data
						date = form.delcaration_deadline.data.strftime("%Y-%m-%d")
						date = f"{date} {event.time}"
						event.delcaration_deadline = date
						print(f"event_date. {event.date}")

					if form.address.data: event.address = form.address.data
					if form.google_map_iframe.data: event.google_map_iframe = parse_google_map_iframe(form.google_map_iframe.data)
					if form.google_map_link.data: event.google_map_link = parse_google_map_link(form.google_map_link.data)
					if form.place_img.data: event.place_img = form.place_img.data
					if form.declaration_mail_content.data: event.declaration_mail_content = form.declaration_mail_content.data
					if form.invitation_mail_content.data: event.invitation_mail_content = form.invitation_mail_content.data
					event.superadmin_id=current_user.id
					
					if form.image_link_header.data: event.image_link_header = form.image_link_header.data
					if form.image_link_footer.data: event.image_link_footer = form.image_link_footer.data

					db.session.add(event)
					db.session.commit()
					print("added")

				except Exception as e:
					flash(f"error: {e}")
				
			if next:
				return redirect(next)
			return redirect(url_for("event.create"))
		else:
			print(form.errors)
			errs = ""
			for elem in form.errors:
				errs += f" {elem}  {form.errors.get(elem)[0]} "
			flash(f"error adding {errs}")

			if next:
				return redirect(next)
			return redirect(url_for("event.create"))
		
	else:

		event = Event.query.all()

		return redirect(url_for("event.get"))
	# return "ok"





