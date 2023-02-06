from flask_wtf import FlaskForm

from wtforms import EmailField, StringField, SubmitField, IntegerField, SelectField, BooleanField
from wtforms.validators import InputRequired, Length, ValidationError, EqualTo
from flask_wtf.file import FileField

from flask_login import current_user

from src.models import Participants, Event, Divisions



# class LoginForm(FlaskForm):
# 	email = EmailField(validators=[InputRequired(), Length(min=0, max=100)], render_kw={"placeholder":"Username"})
# 	password = PasswordField(validators=[InputRequired(), Length(min=0, max=100)], render_kw={"placeholder":"Password"})
# 	submit = SubmitField("Login")

class NewParticipantForm(FlaskForm):
	class Meta:
		csrf = False


	def choice_event():
		event_host_id = current_user.id if current_user.superadmin else  current_user.added_by
		events = Event.query.filter_by(superadmin_id=event_host_id).all()
		return events

	def choice_division():
		event_host_id = current_user.id if current_user.superadmin else  current_user.added_by

		divisions = Divisions.query.filter_by(superadmin_id=event_host_id).all()
		
		return divisions

	first_name = StringField(validators=[Length(min=0, max=100)], render_kw={"placeholder":"First name"})
	last_name = StringField(validators=[ Length(min=0, max=100)], render_kw={"placeholder":"Last name"})
	email = EmailField(validators=[ Length(min=0, max=100)], render_kw={"placeholder":"email"})	
	submit = SubmitField("add participant")
	file = FileField(render_kw={"value":"file"})
	is_vip = BooleanField("is vip: ", default=False)


	event = SelectField('Choose',validators=[InputRequired()], render_kw={"placeholder":"event"}, choices=choice_event)
	division = SelectField('Choose',validators=[], render_kw={"placeholder":"division"}, choices=choice_division, validate_choice=False)


	# def validate_email(self, email):
	# 	if self.email.data == "" and self.file.data:
	# 		return 
			
	# 	qr = Participants.query.filter_by(email=self.email.data).first()

	# 	if qr:
	# 		raise ValidationError("user already exists")

	def validate_file(self, file):
		if not self.file.data:
			return

	# def validate_divisions(self, division):
	# 	division_id = Divisions.query.filter_by(division_name=self.divison_id.data).first()
	# 	print(f"divison_id {division_id}")
	# 	if divison_id:
	# 		division_id = division_id.id
	# 		self.divison_id.data = divison_id
	# 		return divison_id
	# 	else:
	# 		return True




	


