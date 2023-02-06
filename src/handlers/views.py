from flask import redirect, render_template, url_for, session
from flask_login import current_user, logout_user

from src.config import login_manager, app 
from src.models import User, Event

# from src.event.create.views import update_load
from functools import wraps

import datetime



# @app.before_first_request
# def init_app():
# 	logout_user()

@login_manager.user_loader
def user_loader(user_id):

	user =  User.query.filter_by(id=int(user_id)).first()
	# user =  User.query.filter_by(id=int(session.get("_user_id"))).first()
	print(user)
	if user:
		return user
	else:
		return None





def autherntication_required(f):
	@wraps(f)
	def decorated_function(*args, **kws):

		if current_user.is_authenticated:
			if not current_user.verified :
				# return "you have to authenticate"
				# return render_template("auth.html", user=current_user)
				user = current_user
				return redirect(url_for("auth.activate_account"))


		return f(*args, **kws)            
	return decorated_function



def superadmin_required(f):
	@wraps(f)
	def decorated_function(*args, **kws):

		if current_user.is_authenticated:
			if not current_user.superadmin :
				# return "you have to authenticate"
				# return render_template("auth.html", user=current_user)
				user = current_user
				print("not superuser")
				# return redirect(url_for("auth.activate_account"))
				return "no such privilages"


		return f(*args, **kws)            
	return decorated_function



@app.before_request
def before_request():
	session.permanent = True
	
	app.permanent_session_lifetime = datetime.timedelta(minutes=999999)
	session.modified = True
	# printa(session)
	# if current_user.added_by:
	# 	qr = Event.query.filter_by(superadmin_id=current_user.added_by).all()
	# else:
	# 	qr = Event.query.filter_by(superadmin_id=current_user.id).all()



	# print(qr)


# @app.context_processor
# def inject_load():
#     if sys.platform.startswith('linux'): 
#         with open('/proc/loadavg', 'rt') as f:
#             load = f.read().split()[0:3]
#     else:
#         load = [int(random.random() * 100) / 100 for _ in range(3)]
#     return {'load1': load[0], 'load5': load[1], 'load15': load[2]}


# @app.before_first_request
# def before_first_request():
#     threading.Thread(target=update_load).start()

