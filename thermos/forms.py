
# HTML form objects used to retrieve and post user data

from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, BooleanField, SubmitField
from wtforms.fields.html5 import URLField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo, \
    url, ValidationError
from models import User


class BookmarkForm(FlaskForm):
    """"
        Class represents the form used to add bookmarks
    """
    url = URLField('The URL for your bookmark:', validators=[DataRequired(), url()])
    description = StringField('Add an optional description:')

    def validate(self):
        # Validate URL contains HTTP
        if not self.url.data.startswith("http://") or \
                self.url.data.startswith("https://"):
                self.url.data = "http://" + self.url.data

        # Check other validators
        if not FlaskForm.validate(self):
            return False

        # Ensure description is not empty
        if not self.description.data:
            self.description.data = self.url.data

        return True


class LoginForm(FlaskForm):
    username = StringField('Your Username:', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')


class SignupForm(FlaskForm):
    username = StringField('Username',
                           validators=[
                               DataRequired(), Length(3, 80),
                               Regexp('^[A-Z-z0-9_]{3,}$',
                                      message='Usernames consists of numbers, letters, and underscores')
                           ])
    password = PasswordField('Password',
                             validators=[
                                 DataRequired(),
                                 EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Length(1, 120), Email()])

    def validate_email(self, email_field): # Generate error on email field
        if User.query.filter_by(email=email_field.data).first():
            raise ValidationError('There already is a user with this email address.')

    def validate_username(self, username_field): # Generate error on username field
        if User.query.filter_by(username=username_field.data).first():
            raise ValidationError('This username is already taken.')
