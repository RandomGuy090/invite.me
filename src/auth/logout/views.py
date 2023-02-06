from flask import  redirect, session, url_for, session
from flask_login import  logout_user, current_user

from src.config import app

def logout():

	logout_user()

	print("user logged out")
	print(current_user)
	print(session)
	
	if session.get("_user_id"):
		session.pop("_user_id")



	return redirect(url_for("auth.login"))
