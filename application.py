import os
import requests

from flask import Flask, session
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask import render_template, url_for, flash, redirect, request, abort
from forms import RegistrationForm
from flask import render_template, url_for, flash, redirect, request, abort
from flask_login import login_user, current_user, logout_user, login_required

# goodread key: vfTYhqGEGd0ajlUm2JQ8A
# goodread secret: CvaXaTGKgjtGT5SindIjfdlFYGT8kaqTZwfe5pNq7I
# request = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "vfTYhqGEGd0ajlUm2JQ8A", "isbns": "9781632168146"})

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
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    return render_template("register.html", title="Register Page", form=form)




if __name__ == "__main__":
    app.run(debug=True)
