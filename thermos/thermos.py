
# Main entry point of web app used to start up Flask

from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
from logging import DEBUG

app = Flask(__name__)
app.logger.setLevel(DEBUG)

bookmarks = []

# Secret key for session generated by OS with os.urandom(24)
# TODO: replace with hidden value
app.config["SECRET_KEY"] = b'\x12\x1d\x9c\xfd\x8e\xd5\r\xdb\x81\x99t\x98\x01.2\xe2Ra\x07\x14\x92.\tD'


def store_bookmark(url):
    bookmarks.append(dict(
        url=url,
        user="tvao",
        date=datetime.utcnow
    ))


def new_bookmarks(num):
    return sorted(bookmarks, key=lambda bm: bm['date'], reverse=True)[:num]


@app.route('/')
@app.route('/index')
def index():
    """"
    Renders the default index template
    """
    return render_template('index.html', new_bookmarks=new_bookmarks(5))


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == "POST":
        url = request.form['url']
        store_bookmark(url)
        flash("Stored bookmark '{}'".format(url))
        app.logger.debug('stored url: ' + url)
        return redirect(url_for('index'))
    return render_template('add.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500


if __name__ == "__main__":
    app.run(debug=True)

