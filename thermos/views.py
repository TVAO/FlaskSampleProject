
# Views (i.e. similar to controllers in MVC) used to control HTTP requests and responses

from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, login_user, current_user
from thermos import app, db, login_manager
from forms import BookmarkForm
from models import User, Bookmark
# New Python 3 import
#from . import app, db, login_manager
#from .forms import BookmarkForm, LoginForm
#from .models import User, Bookmark


@login_manager.user_loader
def load_user(userid):
    return USer.query.get(int(userid))


@app.route('/')
@app.route('/index')
def index():
    """"
    Renders the default index template
    """
    return render_template('index.html', new_bookmarks=Bookmark.newest(5))


@app.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = BookmarkForm()
    if form.validate_on_submit():  # Check request and validate content
        url = form.url.data
        description = form.description.data
        bm = Bookmark(user=current_user, url=url, description=description)
        db.session.add(bm)
        db.session.commit()
        flash("Stored '{}'".format(description))
        app.logger.debug('stored url: ' + url)
        return redirect(url_for('index'))
    return render_template('add.html', form=form)  # Get request or error


@app.route('/user/<username>')
def user(username):
    # Fetch user and return or 404
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Login and validate user
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None:
            login_user(user, form.remember_me.data)
            flash("Logged in successfully as {}.".format(user.username))
            # Redirect to intended page (e.g. add bookmark page) or index
            return redirect(request.args.get('next') or url_for('index'))
        flash('Incorrect username or password.')
    return render_template('login.html', form=form)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

