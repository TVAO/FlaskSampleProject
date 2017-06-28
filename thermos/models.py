
# Models in database layer

from datetime import datetime
from sqlalchemy import desc
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from thermos import db
#from . import db


# Database entities used to generate tables in SQL Alchemy
class Bookmark(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.String(300))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    @staticmethod
    def newest(num):
        return Bookmark.query.order_by(desc(Bookmark.date)).limit(num)

    # Clear printing and logging of values
    def __repr__(self):
        return "<Bookmark '{}': '{}'>".format(self.description, self.url)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(80), unique=True)
    # Work with user objects and load dynamically (lazy query to load bookmarks)
    bookmarks = db.relationship('Bookmark', backref='user', lazy='dynamic')
    password_hash = db.Column(db.String)

    @property
    def password(self):
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password): # Hash pw
        self.password_hash = generate_password_hash(password)

    def check_password(self, password): # Check pw against hash
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def get_by_username(username): # Replace filter_by
        return User.query.filter_by(username=username).first()

    def __repr__(self):
        return '<User %r>' % self.username

