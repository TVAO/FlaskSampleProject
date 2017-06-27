
# Main entry point of web app used to start up Flask

from flask import Flask, render_template, url_for

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    """"
    Renders the default index template
    """
    return render_template('index.html')


@app.route('/add')
def add():
    return render_template("add.html")

if __name__ == "__main__":
    app.run(debug=True)

