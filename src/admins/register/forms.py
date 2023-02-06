from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, BooleanField
from wtforms.validators import InputRequired, Length, ValidationError, EqualTo

from src.models import User

class RegisterAdminForm(FlaskForm):
	email = EmailField(validators=[InputRequired(), Length(min=0, max=100)], render_kw={"placeholder":"Email"})
	password = PasswordField(validators=[InputRequired(), Length(min=0, max=100), EqualTo('confirm', message='Passwords must match')], render_kw={"placeholder":"Password"})
	
	first_name = StringField(validators=[InputRequired(), Length(min=0, max=100)], render_kw={"placeholder":"first name"})
	last_name = StringField(validators=[InputRequired(), Length(min=0, max=100)], render_kw={"placeholder":"last name"})
	
	confirm  = PasswordField(render_kw={"placeholder":"Password"})

	verify = BooleanField(default=False,  render_kw={"placeholder":"verify admin mail"})
	
	submit = SubmitField("Register")

	def validate_email(self, email):
		existing_user_username = User.query.filter_by(email=self.email.data).first()
		
		if existing_user_username:
			raise ValidationError("user already exists")