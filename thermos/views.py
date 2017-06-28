
# Views (i.e. similar to controllers in MVC) used to control HTTP requests and responses

from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, login_user, current_user, logout_user
#from thermos import app, db, login_manager
#from forms import BookmarkForm, LoginForm, SignupForm
#from models import User, Bookmark
# New Python 3 import
from . import app, db, login_manager
from .forms import BookmarkForm, LoginForm, SignupForm
from .models import User, Bookmark


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
    return render_template('bookmark_form.html', form=form)  # Get request or error


@app.route('/edit/<int:bookmark_id>', metods=['GET', 'POST'])
@login_required
def edit_bookmark(bookmark_id):
    bookmark = Bookmark.query.get_or_404(bookmark_id)
    if current_user != bookmark.user:
        abort(403)  # Forbidden
    form = BookmarkForm(obj=bookmark) # Prefill from db if no data
    if form.validate_on_submit():
        form.populate_obj(bookmark)
        db.session.commit()
        flash("Stored '{}'".format(bookmark.description))
        return redirect (url_for('user', username=current_user.username))
    return render_template('bookmark_form.html', form=form, title="Edit bookmark")


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
        user = User.get_by_username(form.username.data)
        if user is not None and user.check_password(form.password.data):  # Check hash
            login_user(user, form.remember_me.data)
            flash("Logged in successfully as {}.".format(user.username))
            # Redirect to intended page (e.g. add bookmark page) or index
            return redirect(request.args.get('next') or url_for('user'),
                            username=user.username)
        flash('Incorrect username or password.')
    return render_template('login.html', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route("/signup", methods=['GET, POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Welcome, {}! Please login.'.format(user.username))
        return redirect(url_for('login'))
    return render_template("signup.html", form=form)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

