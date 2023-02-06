from flask import render_template, redirect, session, url_for, request

from src.models import User
from src.config import db, app
from flask_login import login_user, current_user
from src.models import User

from werkzeug.security import check_password_hash

from .forms import LoginForm




def login():
	form = LoginForm()
	if form.validate_on_submit():
			
		user = User.query.filter_by(email=form.email.data).first()
		if user:
			if check_password_hash(user.password, form.password.data):
					login_user(user, remember=True)
					print(request.args)
					if request.args.get("next"):
						return redirect(request.args.get("next"))
			return redirect(url_for("home.home"))
		
	return render_template("login_admin.html", form=form, next=request.args.get("next"))


