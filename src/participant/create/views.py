from flask import render_template, redirect, session, url_for, request, flash
from werkzeug.utils import secure_filename

from src.models import User
from src.config import db
from flask_login import login_user, current_user, login_required
from wtforms.validators import InputRequired

from src.models import User, Participants, Event, unique_str, Divisions
from src.handlers.views import autherntication_required

from .forms import NewParticipantForm
from .csv_parsing import csv_parse
from .particip_utils import create_participant


@login_required
@autherntication_required
def create():
	form = NewParticipantForm()
	
	event_host_id = current_user.id if current_user.superadmin else  current_user.added_by
	print(f"{request.method}")

	if request.method == "POST":

		if form.validate_on_submit():
			print("validated")
			#if user has included a csv file
			if form.file.data:

				#parsing data from file
				filename = secure_filename(form.file.data.filename)
				x = csv_parse(file=form.file.data)

				for elem in x:
					#none because try is able not to assign 
					new_participant = None
					try:
						# check if all field has value (not None)
						field_list = ["email"]
						for  field in field_list:
							if not elem.get(field):
								raise Exception(f"column not defined ({field})")


						# create new_participant
						new_participant = create_participant(first_name=elem.get("first_name"), 
								last_name=elem.get("last_name"), 
								email=elem.get("email"), 
								added_by_id=current_user.id, 
								event=form.event.data,
								is_vip=elem.get("is_vip"),
								division=elem.get("division"),
								division_leader=elem.get("division_leader"))

						# new_participant is created successfully, adding to db
						try:
							db.session.add(new_participant)
							db.session.commit()
						except Exception as e:
							flash(f"error adding new participant {new_participant}: {e.args[0]}")

					except Exception as e:
						flash(f"error importing user {elem.get('last_name')}: {e.args[0]}")


				return redirect(url_for("participant.get", next=request.args.get("next"))) 

			# creating participant without file, by hand
			print(f"-----------create participants {form.first_name.data}")
			new_participant = create_participant(first_name=form.first_name.data, 
							last_name=form.last_name.data, 
							email=form.email.data, 
							added_by_id=current_user.id, 
							is_vip=form.is_vip.data,
							event=form.event.data,
							division=form.division.data)
			print(f"new_participant {new_participant}")

			if new_participant:
				try:
					db.session.add(new_participant)
					db.session.commit()

				except Exception as e:
					print(e)	

					flash(f"error adding new participant {new_participant}: {e.args[0]}")

			
		return redirect(url_for("participant.get", next=request.args.get("next")))
	
	elif request.method == "GET":
		event = request.args.get("event")
		if event:
			try:
				event = int(event)
				event = Event.query.filter_by(id=event).first()			
			except:
				event = Event.query.filter_by(name=event).first()

			participants = Participants.query.filter_by(event_id=event.id).all()
		else:
			participants = Participants.query.all()

		
		return render_template("create.html", participantCreateForm=form, participants=participants)


