from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, DateField, TimeField, TextAreaField, DateTimeField
from wtforms.validators import InputRequired, Length, ValidationError, EqualTo

from src.config import lang

class CreateEventForm(FlaskForm):
	name = StringField(validators=[InputRequired(), Length(min=0, max=100)], render_kw={"placeholder":lang.event_Name})
	address = StringField(validators=[InputRequired(), Length(min=0, max=500)], render_kw={"placeholder":lang.event_Address})

	google_map_iframe = StringField(validators=[Length(min=0, max=500)], render_kw={"placeholder":lang.event_iframe})
	google_map_link = StringField(validators=[Length(min=0, max=500)], render_kw={"placeholder":lang.event_google_map_link})
	place_img = StringField(validators=[Length(min=0, max=500)], render_kw={"placeholder":lang.event_place_img})

	# date = DateField(validators=[InputRequired()], format='%Y-%m-%s', render_kw={"placeholder":lang.event_Date})
	datetime = DateTimeField(validators=[InputRequired()],format='%Y-%m-%dT%H:%M', render_kw={"placeholder":lang.event_Date})
	delcaration_deadline = DateTimeField(validators=[InputRequired()],format='%Y-%m-%dT%H:%M', render_kw={"placeholder":lang.event_declaration_deadline})
	# time = TimeField(validators=[InputRequired()],format='%H:%M-%S', render_kw={"placeholder":lang.event_Time})

	declaration_mail_content = TextAreaField(validators=[InputRequired(), Length(min=0, max=2048)], render_kw={"placeholder":lang.event_declaration_content})
	invitation_mail_content = TextAreaField(validators=[InputRequired(), Length(min=0, max=2048)], render_kw={"placeholder":lang.event_invitation_content})
	
	image_link_header = StringField(validators=[Length(min=0, max=2048)], render_kw={"placeholder":lang.image_link_header})
	image_link_footer = StringField(validators=[Length(min=0, max=2048)], render_kw={"placeholder":lang.image_link_footer})
	
	contact_to_organizators = StringField(validators=[Length(min=0, max=2048)], render_kw={"placeholder":lang.contact})


	submit = SubmitField(lang.event_add_event)



	class Meta:
		csrf = False
