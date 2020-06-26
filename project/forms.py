from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from project.models import User


class RegistrationForm(FlaskForm):
  username = StringField("Username", 
                validators=[DataRequired(), Length(min=2, max=20)])
  email = StringField("Email", validators=[DataRequired(), Email()])
  password = PasswordField("Password", validators=[DataRequired()])
  confirmPassword = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
  submit = SubmitField("Register")



