from flask import render_template, redirect, session, url_for, request
from flask.views import View

from src.models import User
from src.config import db, app, mail, lang
from flask_login import login_user, current_user, login_required
from wtforms.validators import InputRequired

from src.models import User, Participants, Event, Divisions, Accompanying, unique_str
from src.handlers.views import autherntication_required
from src.email_sending.email_utils import Code_email

from .forms import NewDeclarationForm



def send_invitation_mail(particip, form=None):


	mail = Code_email(form)
	# mail.text_body =  f"your activation link is: http://{url}" 
	link = f"{app.config['APPLICATION_ROOT']}{url_for('invitation.get')}?invitation={particip.invitation_string}"
	img = f"https://api.participantserver.com/v1/create-participant-code/?data={link};size={app.config['participant_CODE_RES']}"
	print(img)
	print("mail_init")
	
	html_body = render_template("invitation_mail.html", particip=particip, link=link, img=img)
	print(html_body)

	mail.html_body = html_body
	recipients = [particip.email]
	if particip.accompanying_person_email:
		recipients.append(particip.accompanying_person_email)

	mail.send(recipients=recipients)



def create():
	# event = request.args.get("event")
	declaration_string = request.args.get("declaration_string")
	form = NewDeclarationForm()
	form.first_name.validators.append(InputRequired())
	form.last_name.validators.append(InputRequired())
	form.email.validators.append(InputRequired())


	division = Divisions.query\
	.join(Event, Divisions.event_id == Event.id)\
	.join(Participants, Participants.event_id == Event.id)



	form.division.choices = division

	print(form.division.data)
	

	if form.validate_on_submit():

		participant = Participants.query.filter_by(declaration_string=declaration_string).first()

		if form.first_name.data:
			participant.first_name_by_user = participant.first_name_by_user
			participant.first_name = form.first_name.data

		if form.last_name.data:
			participant.last_name_by_user = participant.last_name
			participant.last_name = form.last_name.data

		if form.email.data:
			participant.email_by_user = participant.email
			participant.email = form.email.data

		if form.personal_data.data:
			participant.personal_data = form.personal_data.data

		if form.car_park.data:
			participant.car_park = form.car_park.data

		if form.division.data:
			# value = dict(form.division.choices).get(form.division.data)
			participant.division_id = Divisions.query.filter_by(division_name=form.division.data).first().id

		acc = None
		if form.accompanying_person_first_name.data != "" and \
			form.accompanying_person_last_name.data  != "" and \
			form.accompanying_person_email.data != "" :
			
			invitation_string = unique_str(Accompanying, 64, field = "invitation_string")

			acc = Accompanying()


			acc.first_name = form.accompanying_person_first_name.data
			acc.last_name = form.accompanying_person_last_name.data
			acc.invitation_string = invitation_string
			acc.email = form.accompanying_person_email.data
			acc.event_id = participant.event_id
			

		else:
			participant.participants_accomapnying_id = False

		if participant:
			participant.declarated = True
			if acc:
				participant.accompanying = acc

			db.session.add(participant)
			db.session.commit()
			# send_invitation_mail(particip=participant, form=form)


	else:
		pass
	
	next=request.args.get("next")
	if next:
		return redirect(next) 


		
	# return render_template("participants.html", participantCreateForm=form)
	return redirect(url_for("declarate.get", declaration_string=declaration_string))


#