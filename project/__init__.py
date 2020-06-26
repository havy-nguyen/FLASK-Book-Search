import os
from flask import Flask, session
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from email_validator import *


app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['SECRET_KEY'] = "cff2150872a5e6d41b0c019021cc31fa38a2e86"
Session(app)

# Set up database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DATABASE_URL')
db = SQLAlchemy(app)

# Hash password
bcrypt = Bcrypt(app)

from project import routes

# -----------------------------------------------------------
# goodread key: vfTYhqGEGd0ajlUm2JQ8A
# goodread secret: CvaXaTGKgjtGT5SindIjfdlFYGT8kaqTZwfe5pNq7I
# request = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "vfTYhqGEGd0ajlUm2JQ8A", "isbns": "9781632168146"})
