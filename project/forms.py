from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, RadioField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from project.models import User, Book, Review


class RegistrationForm(FlaskForm):
  username = StringField("Username", 
                validators=[DataRequired(), Length(min=2, max=20)])
  email = StringField("Email", validators=[DataRequired(), Email()])
  password = PasswordField("Password", validators=[DataRequired()])
  confirmPassword = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
  submit = SubmitField("Register")

  def validate_username(self, username):
    user = User.query.filter_by(username=username.data).first()
    if user:
      raise ValidationError("Username is not available!")

  
  def validate_email(self, email):
    user = User.query.filter_by(email=email.data).first()
    if user:
      raise ValidationError("Email is not available!")


class LoginForm(FlaskForm):
  email = StringField("Email", validators=[DataRequired(), Email()])
  password = PasswordField("Password", validators=[DataRequired()])
  remember = BooleanField("Remember me")
  submit = SubmitField("Sign in")

  def validate_email(self, email):
    user = User.query.filter_by(email=email.data).first()
    if not user:
      raise ValidationError("Email is incorrect!")


class SearchForm(FlaskForm):
  isbn = StringField("Isbn", validators=[Length(max=30)])
  title = StringField("Title", validators=[Length(max=150)])
  author = StringField("Author", validators=[Length(max=120)])
  submit = SubmitField("Search")


class ReviewForm(FlaskForm):
  content = TextAreaField('Write a review', validators=[DataRequired()])
  rate = RadioField("Rate book", validators=[DataRequired()], choices=[("1","rate"),("2","rate"),("3","rate"),("4","rate"),("5","rate")])
  submit = SubmitField('Post review')








  


