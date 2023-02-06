from flask import render_template, redirect, session, url_for, request

from flask_login import login_user, login_required, current_user
from src.handlers.views import autherntication_required

from src.models import User
from src.config import db, app
from flask_login import login_user, current_user
from src.models import User

from .forms import LoginForm



@login_required
@autherntication_required
def delete():
	user_id = request.args.get("user_id")
	next = request.args.get("next")
	print(user_id)
	if request.method == "POST":
		if user_id:		

			qr = User.query.filter_by(id=user_id)
			if len(qr.all()):
				qr = qr.delete()
				db.session.commit()
			else:
				return "no such user "

			if next:
				return redirect(next)

		
	return render_template("delete_login.html", next=request.args.get("next"))


