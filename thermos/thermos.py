
# Main entry point of web app used to start up Flask

import os
from flask import Flask, render_template, redirect, url_for, flash
from logging import DEBUG
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.logger.setLevel(DEBUG)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'thermos.db')
# Secret key for session generated by OS with os.urandom(24) TODO: replace with hidden value
app.config["SECRET_KEY"] = b'\x12\x1d\x9c\xfd\x8e\xd5\r\xdb\x81\x99t\x98\x01.2\xe2Ra\x07\x14\x92.\tD'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

from forms import BookmarkForm
#from .models import Bookmark
import models

def new_bookmarks(num):
    return []


@app.route('/')
@app.route('/index')
def index():
    """"
    Renders the default index template
    """
    return render_template('index.html', new_bookmarks=new_bookmarks(5))


@app.route('/add', methods=['GET', 'POST'])
def add():
    form = BookmarkForm()
    if form.validate_on_submit():  # Check request and validate content
        url = form.url.data
        description = form.description.data
        bm = models.Bookmark(url=url, description=description)
        db.session.add(bm)
        flash("Stored '{}'".format(description))
        app.logger.debug('stored url: ' + url)
        return redirect(url_for('index'))
    return render_template('add.html', form=form)  # Get request or error


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500


if __name__ == "__main__":
    app.run(debug=True)

