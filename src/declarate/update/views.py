from flask import render_template, redirect, session, url_for, request, flash
from flask.views import View

from src.models import User
from src.config import db , app, mail, lang
from flask_login import login_user, current_user, login_required
from wtforms.validators import InputRequired


from src.models import User, Participants, Event, Divisions, Accompanying
from src.handlers.views import autherntication_required

from src.declarate.create.forms import NewDeclarationForm




def update():
	# event = request.args.get("event")
	declaration_string = request.args.get("declaration_string")
	form = NewDeclarationForm()
	form.first_name.validators.append(InputRequired())
	form.last_name.validators.append(InputRequired())
	form.email.validators.append(InputRequired())


	division = Divisions.query\
	.join(Event, Divisions.event_id == Event.id)\
	.join(Participants, Participants.event_id == Event.id)\
	.where(Participants.declaration_string == declaration_string).all()

	form.division.choices = division


	qr = Participants.query\
		.add_columns(
			Accompanying.id.label("id_acc"),
			Accompanying.first_name.label("accompanying_person_first_name"),
			Accompanying.last_name.label("accompanying_person_last_name"),
			Accompanying.email.label("accompanying_person_email"))\
		.join(Accompanying, Participants.accomapnying_id == Accompanying.id, isouter=True)\
		.add_columns(
			Participants.id.label("id"),
			Participants.first_name.label("first_name"),
			Participants.first_name_by_user.label("first_name_by_user"),
			Participants.last_name.label("last_name"),
			Participants.is_vip.label("participant_is_vip"),
			Participants.last_name_by_user.label("last_name_by_user"),
			Participants.email_by_user.label("email_by_user"),
			Participants.personal_data.label("personal_data"),
			Participants.car_park.label("car_park"),
			Participants.accomapnying_id.label("accomapnying_id"),
			Participants.invitation_sent.label("invitation_sent"),
			Participants.declaration_sent.label("declaration_sent"),
			Participants.division_id.label("division"),
			Participants.email.label("email"),)\
		.add_columns(
			Accompanying.id.label("id_acc"),
			Accompanying.first_name.label("accompanying_person_first_name"),
			Accompanying.last_name.label("accompanying_person_last_name"),
			Accompanying.email.label("accompanying_person_email"))\
		.join(Divisions, Participants.division_id == Divisions.id, isouter=True)\
		.add_columns(
			Divisions.division_name.label("division_name"),
		)\
		.join(Event, Participants.event_id == Event.id, isouter=True)\
		.add_columns(
			Event.name.label("event_name"),
			Event.delcaration_deadline.label("event_declaration_deadline"),
			Event.contact_to_organizators.label("event_contact_to_organizators")
		)\
		.where(Participants.declaration_string == declaration_string)
		
	qr = qr.first()

	# form.division.data = qr.division_name
	# form.process()

	
	# qr = Participants.query.filter_by(declaration_string = declaration_string).first()
	# if qr.accomapnying_id:
	# 	qr = qr, Accompanying.query.filter_by(id=qr.id)
	if not qr:
		flash(lang.declaration_not_found)
		return render_template("declaration_update.html", lang=lang)

	if qr.invitation_sent:
		flash(lang.invitation_already_sent)

		return render_template("declaration.html")
	
	if form.validate_on_submit():



		particpant = Participants.query.filter_by(id=qr.id).first()
		if form.first_name.data:
			particpant.first_name_by_user = particpant.first_name_by_user
			particpant.first_name = form.first_name.data

		if form.last_name.data:
			particpant.last_name_by_user = particpant.last_name
			particpant.last_name = form.last_name.data

		if form.email.data:
			particpant.email_by_user = particpant.email
			particpant.email = form.email.data

		if form.personal_data.data:
			particpant.personal_data = form.personal_data.data

		if form.car_park.data:
			particpant.car_park = form.car_park.data

		if form.division.data:
			# value = dict(form.division.choices).get(form.division.data)
			particpant.division_id = Divisions.query.filter_by(division_name=form.division.data).first().id

		acc = None
		if form.accompanying_person_first_name.data != "" and form.accompanying_person_last_name.data  != "":
			acc = Accompanying.query.filter_by(id = qr.id_acc).first()
			if not acc:
				acc = Accompanying()

			acc.first_name = form.accompanying_person_first_name.data
			acc.last_name = form.accompanying_person_last_name.data
			acc.email = form.accompanying_person_email.data
			

		else:
			particpant.participants_accomapnying_id = False

		if particpant:
			particpant.declarated = True
			if acc:
				# db.session.add(acc)

				# qr.accomapnying= acc
				particpant.accompanying = acc

			db.session.add(particpant)
			db.session.commit()
			# send_invitation_mail(particip=qr, form=form)
		return redirect(url_for("declarate.get", declaration_string=declaration_string))

	else:
		print(form.errors)

	
	next=request.args.get("next")
	if next:
		return redirect(next) 


		
	return render_template("declaration_update.html", declarationCreateForm=form, participant=qr, declaration_string=declaration_string, lang=lang)
	# return redirect(url_for("declarate.get", declaration_string=declaration_string))


#