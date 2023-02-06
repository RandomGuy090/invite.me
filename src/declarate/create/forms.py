from flask_wtf import FlaskForm
from wtforms import EmailField, StringField, SubmitField, IntegerField, SelectField, BooleanField
from wtforms.validators import InputRequired, Length, ValidationError, EqualTo

from flask_login import current_user

from src.models import Divisions, Participants, Event
from src.config import lang


# class LoginForm(FlaskForm):
# 	email = EmailField(validators=[InputRequired(), Length(min=0, max=100)])
# 	password = PasswordField(validators=[InputRequired(), Length(min=0, max=100)])
# 	submit = SubmitField("Login")

class NewDeclarationForm(FlaskForm):


	first_name = StringField(validators=[Length(min=0, max=100)])
	last_name = StringField(validators=[ Length(min=0, max=100)])
	email = EmailField(validators=[Length(min=0, max=100)])

	accompanying_person_first_name = StringField(validators=[ Length(min=0, max=100)])
	accompanying_person_last_name = StringField(validators=[Length(min=0, max=100)])
	accompanying_person_email = EmailField(validators=[Length(min=0, max=100)])

	# division = SelectField('Choose',validators=[InputRequired()])
	personal_data = BooleanField(validators=[InputRequired()],default=True)
	car_park = BooleanField(default=False)
	division = SelectField('Choose',validators=[InputRequired()])

	submit = SubmitField(lang.submit_declaration)

	class Meta:
		csrf = False


