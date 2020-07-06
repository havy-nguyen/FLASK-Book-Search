import os
import requests
from project.forms import RegistrationForm, LoginForm, SearchForm, ReviewForm
from project.models import User, Book, Review
from flask_sqlalchemy import SQLAlchemy
from project import app, db, bcrypt
from sqlalchemy import and_
from flask import render_template, url_for, flash, redirect, request, abort, jsonify
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
  if form.validate_on_submit():
    input_isbn = str(form.isbn.data)
    input_title = str(form.title.data)
    input_author = str(form.author.data)
    isbn = request.args.get("isbn", input_isbn)
    title = request.args.get("title", input_title)
    author = request.args.get("author", input_author)
    books = Book.query.filter(and_(Book.isbn.like("%" + input_isbn + "%"), 
            Book.title.like("%" + input_title.title() + "%"), 
            Book.author.like("%" + input_author.title() + "%"))).paginate(page=1, per_page=8, error_out=False)
    return render_template("index.html", pageTitle="Search Results", 
                          books=books, form=form, isbn=input_isbn, title=input_title, author=input_author)
  else:
    page = request.args.get('page', 2, type=int)
    isbn = request.args.get("isbn", "isbn")
    title = request.args.get("title", "title")
    author = request.args.get("author", "author")
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
  res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "vfTYhqGEGd0ajlUm2JQ8A", "isbns": book.isbn})
  goodreads_json = res.json()
  goodreads_ratings = goodreads_json['books'][0]['work_ratings_count']
  goodreads_avg = goodreads_json['books'][0]['average_rating']
  print(goodreads_avg, goodreads_ratings)
  form = ReviewForm()
  if form.is_submitted():
    review = Review(content=form.content.data, rate=form.rate.data, reviewer=current_user, book=book) 
    if form.validate_on_submit():
      flash("Your review has been added.", 'info')
      db.session.add(review)
      db.session.commit()
      return redirect(url_for('book', id=book.id))
    else:
      flash("Please also rate book.", 'info')
  return render_template('book.html', pageTitle=book.title, book=book, form=form, 
            reviews=reviews, goodreads_ratings=goodreads_ratings, goodreads_avg=goodreads_avg)


@app.route("/index/api/<isbn>",  methods=['GET', 'POST'])
def book_api(isbn):
  book = Book.query.filter(Book.isbn == isbn).first()
  if book is None:
    return jsonify({"Error": "Invalid Isbn"}), 422
  total_rating = 0
  for review in book.reviews:
    total_rating += review.rate
  try:
    avg_rating = round(total_rating / int(len(book.reviews)),2)
    return jsonify({"title": book.title,
                    "author": book.author,
                    "year": book.year,
                    "isbn": book.isbn,
                    "review_count": total_rating,
                    "average_score": avg_rating})
  except ZeroDivisionError:
    return jsonify({"title": book.title,
                    "author": book.author,
                    "year": book.year,
                    "isbn": book.isbn,
                    "review_count": "no rating",
                    "average_score": "no rating"})







