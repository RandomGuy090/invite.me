from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import InputRequired, Length, ValidationError, EqualTo

from flask_login import login_user, logout_user
from flask import session

from src.models import User




class LoginForm(FlaskForm):
	email = EmailField(validators=[InputRequired(), Length(min=0, max=100)], render_kw={"placeholder":"Username"})
	password = PasswordField(validators=[InputRequired(), Length(min=0, max=100)], render_kw={"placeholder":"Password"})
	submit = SubmitField("Login")
	
	def validate_email(self, email):
		user = User.query.filter_by(email=self.email.data).first()

		if not user:		
			raise ValidationError("wrong email or password")


