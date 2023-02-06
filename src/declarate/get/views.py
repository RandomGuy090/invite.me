from flask import render_template, redirect, session, url_for, request, flash
from flask.views import View

from src.models import User
from src.config import db, app, lang
from flask_login import login_user, current_user, login_required
from wtforms.validators import InputRequired

from src.models import User, Participants, Event, Divisions
from src.handlers.views import autherntication_required

# from .forms import GetDeclarationForm
from src.declarate.create.forms import NewDeclarationForm





def get():
	# event = request.args.get("event")
	declaration_string = request.args.get("declaration_string")


	if not declaration_string:
		# return "check link"
		flash(lang.declaration_not_found)
		return render_template("declaration.html", lang=lang)


	# qr = Participants.query.filter_by(declaration_string=declaration_string).first()

	qr = Participants.query\
	.join(Event, Event.id == Participants.event_id)\
	.add_columns(Event.delcaration_deadline.label("delcaration_deadline"),)\
	.add_columns(Event.contact_to_organizators.label("contact_to_organizators"),)\
	.add_columns(Event.name.label("event_name"))\
	.add_columns(Event.superadmin_id.label("event_superadmin_id"))\
	.where(Participants.declaration_string == declaration_string)\
	.add_columns(Participants.first_name.label("first_name"))\
	.add_columns(Participants.last_name.label("last_name"))\
	.add_columns(Participants.is_vip.label("participant_is_vip"))\
	.add_columns(Participants.canceled.label("participant_canceled"))\
	.add_columns(Participants.email.label("email"))\
	.add_columns(Participants.declarated.label("declarated"))\
	.join(Divisions, Participants.division_id == Divisions.id, isouter=True)\
		.add_columns(
			Divisions.division_name.label("division_name"),
		)\
	.first()
	
	if not qr:
		flash(lang.declaration_not_found)
		return render_template("declaration.html", lang=lang)

	
	form = NewDeclarationForm(qr)
	form.first_name.validators.append(InputRequired())
	form.last_name.validators.append(InputRequired())
	form.email.validators.append(InputRequired())
	

	division = Divisions.query\
	.join(Event, Divisions.event_id == Event.id)\
	.join(Participants, Participants.event_id == Event.id)\
	.where(Participants.declaration_string == declaration_string)\
	.all()
	
	form.division.choices = division


	if not qr.declarated:
		# return f"not declarated yet   first_name:   {qr.first_name}  last_name:   {qr.last_name}"
		return render_template("declaration.html", declarationCreateForm=form, participant=qr, declaration_string=declaration_string, lang=lang)
	else:
		# user already declarated, send qr code
		print("declarated")
		return render_template("declaration.html", participant=qr, declaration_string=declaration_string, lang=lang)
		# return f"you are already declarated {qr.first_name} {qr.last_name}"
		pass


	

	
	next=request.args.get("next")
	if next:
		return redirect(next) 
