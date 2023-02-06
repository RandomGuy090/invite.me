from flask import render_template, redirect, session, request
from flask_login import current_user, login_required

from src.models import User
from src.config import db, app

@login_required
def activate_account():
	activate_string = request.args.get("activate_string")
	if not activate_string:
		return render_template("activate.html", activated=False, user=current_user)
		
	user = User.query.filter_by(activate_string=activate_string).first()
	print(user)
	
	if user.id == current_user.id:
		user.verified = True
		db.session.commit()

	# return "thanks for activating your account"
	return render_template("activate.html", activated=True, user=current_user)


