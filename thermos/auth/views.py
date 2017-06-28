from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user

from . import auth  # Import blueprint taking place as app object
from .. import db  # Import db from parent
from ..models import User  # Import user from parent module
from .forms import LoginForm, SignupForm  # Forms module inside blueprint

# Views (i.e. MVC Controllers) used to handle HTTP requests and issue responses


@auth.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Login and validate user
        user = User.get_by_username(form.username.data)
        if user is not None and user.check_password(form.password.data):
            login_user(user, form.remember_me.data)
            flash("Logged in successfully as {}.".format(user.username))
            # Redirect to intended page (e.g. add bookmark page) or index
            return redirect(request.args.get('next') or url_for('bookmarks.user',
                                                username=user.username))
        flash('Incorrect username or password.')
    return render_template("login.html", form=form)


@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@auth.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password = form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Welcome, {}! Please login.'.format(user.username))
        return redirect(url_for('.login'))
    return render_template("signup.html", form=form)
