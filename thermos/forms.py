
from flask_wtf import FlaskForm
from wtforms.fields import StringField
from wtforms.fields.html5 import URLField
from wtforms.validators import DataRequired, url


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