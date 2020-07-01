from project import db, login_manager
from datetime import datetime
from email_validator import *
from flask_login import UserMixin


@login_manager.user_loader 
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    # reviews = db.relationship("Review", backref="author", lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


class Book(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(30), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    author = db.Column(db.String(120), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    # reviews = db.relationship("Review", backref="book", lazy=True)

    def __repr__(self):
        return f"Book('{self.id}', '{self.isbn}', '{self.title}', '{self.author}', '{self.year}')"


# class Review(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     content = db.Column(db.Text, nullable=False)
#     date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
#     user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
#     book_id = db.Column(db.Integer, db.ForeignKey("book.id"), nullable=False)

#     def __repr__(self):
#         return f"Review('{self.content}', '{self.date}')" 