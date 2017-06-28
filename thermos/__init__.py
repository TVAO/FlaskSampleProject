
# Configuration of and bundling of application
# Secret key for session generated by OS with os.urandom(24) TODO: replace with hidden value

import os

from flask import Flask
from logging import DEBUG
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.logger.setLevel(DEBUG)
app.config["SECRET_KEY"] = b'\x12\x1d\x9c\xfd\x8e\xd5\r\xdb\x81\x99t\x98\x01.2\xe2Ra\x07\x14\x92.\tD'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'thermos.db')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['DEBUG'] = True
db = SQLAlchemy(app)

# Configure authentication
login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.init_app(app)

# Old Python 2 import
#import models
#import views

# New Python 3 import
from . import models
from . import views



