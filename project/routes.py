import os
import requests
from project.forms import RegistrationForm, LoginForm, SearchForm
from project.models import User, Book
from flask_sqlalchemy import SQLAlchemy
from project import app, db, bcrypt
from flask import render_template, url_for, flash, redirect, request, abort
from flask_login import login_user, current_user, logout_user, login_required

@app.route("/", methods=['GET', 'POST'])
@app.route('/register', methods=['GET', 'POST'])
def register():
  if current_user.is_authenticated:
    return redirect(url_for('index'))
  form = RegistrationForm()
  if form.validate_on_submit():
    hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
    user = User(username=form.username.data, email=form.email.data, password=hashed_password)
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('login'))
  return render_template("register.html", title="Register Page", form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
  if current_user.is_authenticated:
    return redirect(url_for('index'))
  form = LoginForm()
  if form.validate_on_submit():
    user = User.query.filter_by(email=form.email.data).first()
    if user and bcrypt.check_password_hash(user.password, form.password.data):
      login_user(user, remember=form.remember.data)
      return redirect(url_for('index'))
    else:
      flash('Login unsuccessful. Please check email and password', 'danger')
  return render_template('login.html', title='Sign In', form=form)


@app.route("/logout")
def logout():
  logout_user()
  return redirect(url_for('login'))


@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
  form = SearchForm()
  input_isbn = str(form.isbn.data)
  input_title = str(form.title.data)
  input_author = str(form.author.data)
  if form.validate_on_submit():
    title_list = Book.query.filter(Book.title.like("%" + input_title.title() + "%")).all()
    isbn_list = Book.query.filter(Book.isbn.like("%" + input_isbn + "%")).all()
    author_list = Book.query.filter(Book.author.like("%" + input_author.title() + "%")).all()
    books = list(set(title_list).intersection(set(isbn_list), set(author_list)))
    return render_template("results.html", title="Search Results", books=books, form=form)
  else:
    recommendations = Book.query.filter(Book.year > 2016).limit(3).all()
    return render_template("index.html", title="Book Search", recommendations=recommendations, form=form)

