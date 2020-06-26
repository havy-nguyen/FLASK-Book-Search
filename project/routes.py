import os
import requests
from project.forms import RegistrationForm
from project.models import User
from flask_sqlalchemy import SQLAlchemy
from project import app, db, bcrypt
from flask import render_template, url_for, flash, redirect, request, abort
from flask_login import login_user, current_user, logout_user, login_required

@app.route("/", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created!', 'info')
    return render_template("register.html", title="Register Page", form=form)