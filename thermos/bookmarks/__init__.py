
# Bookmark blueprint object for bundling bookmark functionality

from flask import Blueprint

bookmarks = Blueprint('bookmarks', __name__)

from . import views