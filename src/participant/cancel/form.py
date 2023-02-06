from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import InputRequired, Length, ValidationError, EqualTo


class DeleteForm(FlaskForm):
	name = StringField(validators=[InputRequired(), Length(min=0, max=100)], render_kw={"placeholder":"Name"})
	submit = SubmitField("Add event")

	class Meta:
		csrf = False

