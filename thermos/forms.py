
from flask_wtf import Formfrom wtforms.fields import Stringfield
from flask.ext.wtf.html5 import URLField
from wtforms.validators import  import DataRequired, url

class BookmarkForm(Form):
    """"
        Class represents the form used to add bookmarks
    """
    url = URLField('url', validators=[DataRequired, url()])
    description = Stringfield('description')