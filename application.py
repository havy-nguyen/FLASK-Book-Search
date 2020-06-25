import os
import requests

from flask import Flask, session
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask import render_template, url_for, flash, redirect, request, abort

# goodread key: vfTYhqGEGd0ajlUm2JQ8A
# goodread secret: CvaXaTGKgjtGT5SindIjfdlFYGT8kaqTZwfe5pNq7I

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

# request = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "vfTYhqGEGd0ajlUm2JQ8A", "isbns": "9781632168146"})


@app.route("/")
def index():
    return render_template("register.html", title="Register Page")




if __name__ == "__main__":
    app.run(debug=True)
