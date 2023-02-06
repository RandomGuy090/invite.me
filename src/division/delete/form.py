from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import InputRequired, Length, ValidationError, EqualTo


class DeleteForm(FlaskForm):
	name = StringField(validators=[InputRequired(), Length(min=0, max=100)])
	submit = SubmitField("Add event")

	class Meta:
		csrf = False

