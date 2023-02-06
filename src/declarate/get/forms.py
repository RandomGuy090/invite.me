from flask_wtf import FlaskForm
from wtforms import EmailField, StringField, SubmitField, IntegerField, SelectField
from wtforms.validators import InputRequired, Length, ValidationError, EqualTo

from flask_login import current_user

from src.models import Divisions, Participants, Event

# class LoginForm(FlaskForm):
# 	email = EmailField(validators=[InputRequired(), Length(min=0, max=100)], render_kw={"placeholder":"Username"})
# 	password = PasswordField(validators=[InputRequired(), Length(min=0, max=100)], render_kw={"placeholder":"Password"})
# 	submit = SubmitField("Login")

class GetDeclarationForm(FlaskForm):


	first_name = StringField(validators=[InputRequired(), Length(min=0, max=100)], render_kw={"placeholder":"First name"})
	last_name = StringField(validators=[InputRequired(), Length(min=0, max=100)], render_kw={"placeholder":"Last name"})
	email = EmailField(validators=[InputRequired(), Length(min=0, max=100)], render_kw={"placeholder":"Contact email"})

	accompanying_person_first_name = StringField(validators=[ Length(min=0, max=100)], render_kw={"placeholder":"accompanying_person_first_name email"})
	accompanying_person_last_name = StringField(validators=[Length(min=0, max=100)], render_kw={"placeholder":"accompanying_person_last_name email"})

	# division = SelectField('Choose',validators=[InputRequired()], render_kw={"placeholder":"event"}, choices=list_divisions)
	division = SelectField('Choose',validators=[InputRequired()], render_kw={"placeholder":"event"})

	submit = SubmitField("add participant")

	
