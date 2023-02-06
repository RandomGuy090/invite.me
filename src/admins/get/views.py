from flask import render_template, redirect, session, url_for, request
from flask.views import View

from src.models import User
from src.config import db, app
from flask_login import login_user, current_user, login_required

from src.models import User, Participants, Event
from src.handlers.views import autherntication_required

from .forms import GetAdminForm




@login_required
@autherntication_required
def get():
	form = GetAdminForm()

	if event:
		users = User.query.filter_by(added_by=current_user.id).all()		
	
		print(f"----------------users {users}")
	else:
		participants = Participants.query.all()
	
	next=request.args.get("next")
	if next:
		return redirect(next) 
		
	return render_template("get_admin.html", participantCreateForm=form, participants=participants)


#