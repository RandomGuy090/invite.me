from flask_wtf import FlaskForm
from wtforms import EmailField, StringField, SubmitField, IntegerField, SelectField
from wtforms.validators import InputRequired, Length, ValidationError, EqualTo

from flask_login import current_user

from src.models import Participants, Event

# class LoginForm(FlaskForm):
# 	email = EmailField(validators=[InputRequired(), Length(min=0, max=100)])
# 	password = PasswordField(validators=[InputRequired(), Length(min=0, max=100)])
# 	submit = SubmitField("Login")

class EventForm(FlaskForm):
	class Meta:
		csrf = False

	# first_name = StringField(validators=[InputRequired(), Length(min=0, max=100)])
	# last_name = StringField(validators=[InputRequired(), Length(min=0, max=100)])
	# email = EmailField(validators=[InputRequired(), Length(min=0, max=100)])
	
	# event = IntegerField(validators=[InputRequired()])
	
	name = StringField(validators=[InputRequired(), Length(min=0, max=100)])
	submit = SubmitField("add participant")

	# event = SelectField('Choose',validators=[InputRequired()])



	# def validate_email(self, email):
	# 	qr = Participants.query.filter_by(email=self.email.data).first()

	# 	if qr:
	# 		raise ValidationError("user already exists")


