from flask_wtf import FlaskForm
from wtforms import EmailField, StringField, SubmitField, IntegerField, SelectField
from wtforms.validators import InputRequired, Length, ValidationError, EqualTo

from flask_login import current_user

from src.models import Participants, Event, Divisions

# class LoginForm(FlaskForm):
# 	email = EmailField(validators=[InputRequired(), Length(min=0, max=100)], render_kw={"placeholder":"Username"})
# 	password = PasswordField(validators=[InputRequired(), Length(min=0, max=100)], render_kw={"placeholder":"Password"})
# 	submit = SubmitField("Login")

class GetDivisionsForm(FlaskForm):
	def choice():
		event_host_id = current_user.id if current_user.superadmin else  current_user.added_by
		events = Event.query.filter_by(superadmin_id=event_host_id).all()
		return events

	division_name = StringField(validators=[InputRequired(), Length(min=0, max=100)], render_kw={"placeholder":"name of division"})
	division_leader = StringField(validators=[InputRequired(), Length(min=0, max=100)], render_kw={"placeholder":"division leader"})
	event = SelectField('Choose',validators=[InputRequired()], render_kw={"placeholder":"event"}, choices=choice)
	
	
	submit = SubmitField("submit declaration")

