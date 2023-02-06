from flask import render_template, redirect, session, url_for, request

from flask_login import login_user, logout_user

from werkzeug.security import generate_password_hash

from src.models import User, specific_string
from src.config import db,  app
from src.email_sending.email_utils import Register_email

from .forms import RegisterForm






def register():
	form = RegisterForm()


	if form.validate_on_submit():
		while True:
			activate_string = specific_string(32)
			qr = User.query.filter_by(activate_string=activate_string).all()
			if len(qr)<1:
				break

		hashed_pass = generate_password_hash(form.password.data)
		new_user = User(email=form.email.data, password=hashed_pass,superadmin=True, login_parameter=None, verified=False, activate_string=activate_string )
		db.session.add(new_user)
		db.session.commit()
		# logout_user()
		login_user(new_user, remember=True)

		# session["user"] = {"email":new_user.email, "id":new_user.id}

		url = f"{app.config['APPLICATION_ROOT']}{url_for('auth.activate_account')}?activate_string={new_user.activate_string}"

		# msg = Message("Hello",
		# 		  sender=app.config.get("MAIL_SENDER"),
		# 		  recipients=[form.email.data])
		# msg.body = f"your activation link is: {url}" 
		# mail.send(msg)
		

		# send_email(subject="Registration link",
		# 	sender=app.config.get("MAIL_SENDER"),
		# 	recipients=[form.email.data],
		# 	text_body = f"your activation link is: {url}" )
		mail = Register_email(form)
		print(mail)
		mail.text_body =  f"your activation link is: {url}" 
		print(mail.text_body)
		mail.send(recipients=[form.email.data])
		print(f"mail sent")


	
		
		return redirect(url_for("home.home"))

	return render_template("register.html", form=form)


