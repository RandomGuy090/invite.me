from flask import render_template, redirect, session, url_for, request
from werkzeug.utils import secure_filename

from src.models import User
from src.config import db 
from flask_login import login_user, current_user, login_required

from src.models import User, Event,  Divisions
from src.handlers.views import autherntication_required

from .forms import NewDivisionForm



@login_required
@autherntication_required
def create():
	form = NewDivisionForm()
	event_host_id = current_user.id if current_user.superadmin else  current_user.added_by

	if request.method == "POST":
		if form.validate_on_submit():
			event = Event.query.filter_by(name=form.event.data).first()
			new_division = Divisions(
				division_name=form.division_name.data,
				division_leader=form.division_leader.data,
				event_id=event.id,
				superadmin_id=event_host_id)
			print("creating new divison")
			if new_division:
				db.session.add(new_division)
				db.session.commit()

			# session["userid"] = user.id
			return redirect(url_for("division.get", next=request.args.get("next")))

	
	# return render_template("division_create.html", divisionCreateForm=form)
	return redirect(url_for("division.get"))


