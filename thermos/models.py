
from datetime import datetime
from thermos import db


# Database entities used to generate tables in SQL Alchemy


class Bookmark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.String(300))

    # Clear printing and logging of values
    def __repr__(self):
        return "<Bookmark '{}': '{}'>".format(self.description, self.url)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(80), unique=True)

    def __repr__(self):
        return '<User %r>' % self.username

