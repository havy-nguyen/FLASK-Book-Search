import os
import requests
from project.forms import RegistrationForm, LoginForm, SearchForm, ReviewForm
from project.models import User, Book, Review
from flask_sqlalchemy import SQLAlchemy
from project import app, db, bcrypt
from sqlalchemy import and_
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
  return render_template("register.html", pageTitle="Register Page", form=form)


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
  return render_template('login.html', pageTitle='Sign In', form=form)


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
    print("first")
    print(input_isbn, input_title, input_author)
    books = Book.query.filter(and_(Book.isbn.like("%" + input_isbn + "%"), 
            Book.title.like("%" + input_title.title() + "%"), 
            Book.author.like("%" + input_author.title() + "%"))).paginate(page=1, per_page=8, error_out=False)
    print("here")
    return render_template("index.html", pageTitle="Search Results", 
                          books=books, form=form, page=2, isbn=input_isbn, title=input_title, author=input_author)
  else:
    page = request.args.get('page', 2, type=int)
    isbn = request.args.get("isbn", "isbn")
    title = request.args.get("title", "title")
    author = request.args.get("author", "author")
    print("second")
    print(isbn, title, author)
    books = Book.query.filter(and_(Book.isbn.like("%" + isbn + "%"), 
            Book.title.like("%" + title.title() + "%"), 
            Book.author.like("%" + author.title() + "%"))).paginate(page=page, per_page=8, error_out=False)
    return render_template("results.html", pageTitle="Search Results", 
                        books=books, form=form, isbn=isbn, title=title, author=author)

  
@app.route("/index/<int:id>",  methods=['GET', 'POST'])
@login_required
def book(id):
  book = Book.query.get_or_404(id)
  page = request.args.get('page', 1, type=int)
  reviews = Review.query.join(Book).filter(Book.id == book.id).order_by(Review.id.desc()).paginate(page=page, per_page=4, error_out=False)
  form = ReviewForm()
  if form.validate_on_submit():
    review = Review(content=form.content.data, reviewer=current_user, book=book) 
    flash("Your review has been added", 'danger')
    db.session.add(review)
    db.session.commit()
    return redirect(url_for('book', id=book.id))
  return render_template('book.html', pageTitle=book.title, book=book, form=form, reviews=reviews)








