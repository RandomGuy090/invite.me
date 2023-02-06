from flask_wtf import FlaskForm
from wtforms import EmailField, StringField, SubmitField, IntegerField, SelectField
from wtforms.validators import InputRequired, Length, ValidationError, EqualTo

from flask_login import current_user

from src.models import Participants, Event

# class LoginForm(FlaskForm):
# 	email = EmailField(validators=[InputRequired(), Length(min=0, max=100)], render_kw={"placeholder":"Username"})
# 	password = PasswordField(validators=[InputRequired(), Length(min=0, max=100)], render_kw={"placeholder":"Password"})
# 	submit = SubmitField("Login")

class GetAdminForm(FlaskForm):


	first_name = StringField(validators=[InputRequired(), Length(min=0, max=100)], render_kw={"placeholder":"First name"})
	last_name = StringField(validators=[InputRequired(), Length(min=0, max=100)], render_kw={"placeholder":"Last name"})
	email = EmailField(validators=[InputRequired(), Length(min=0, max=100)], render_kw={"placeholder":"email"})
	
	added_by = IntegerField(validators=[InputRequired()], render_kw={"placeholder":"event"})
	
	submit = SubmitField("add participant")

	


	def validate_email(self, email):
		qr = Participants.query.filter_by(email=self.email.data).first()

		if qr:
			raise ValidationError("user already exists")


