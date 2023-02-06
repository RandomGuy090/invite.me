from flask import render_template, redirect, session, url_for, request

from flask_login import login_user, logout_user, current_user, login_required
from flask_mail import Message


from src.models import User, unique_str
from src.config import db, mail, app
from src.handlers.views import autherntication_required

from werkzeug.security import generate_password_hash

from .forms import RegisterAdminForm

@autherntication_required
@login_required
def register():
	form = RegisterAdminForm()

	print("form")
	if form.validate_on_submit():
		print(f"{form.errors}")

		while True:
			print("generating")
			activate_string = unique_str(object=User, length=32, field="activate_string")
			print("activate_string")

			qr = User.query.filter_by(activate_string=activate_string).all()
			if len(qr)<1:
				break

		hashed_pass = generate_password_hash(form.password.data)
		new_user = User(email=form.email.data, 
			password=hashed_pass,
			superadmin=False, 
			login_parameter=None, 
			verified=not(form.verify.data), 
			first_name=form.first_name.data, 
			last_name=form.last_name.data, 
			activate_string=activate_string,
			added_by=current_user.id)

		db.session.add(new_user)
		db.session.commit()

		# login_user(new_user, remember=True)

		# session["user"] = {"email":new_user.email, "id":new_user.id}

		if form.verify.data:

			msg = Message("Hello",
	                  sender=app.config.get("MAIL_SENDER"),
	                  recipients=[form.email.data])
			url = f"{app.config['APPLICATION_ROOT']}{url_for('auth.activate_account')}?activate_string={new_user.activate_string}"
			msg.body = f"your activation link is: {url}" 
			mail.send(msg)	
			return redirect(url_for("home.home"))


	return render_template("register_admin.html", RegisterAdminForm=form)


