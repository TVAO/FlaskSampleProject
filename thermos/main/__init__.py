
# Main blueprint for index page and error handlers

from flask import Blueprint

main = Blueprint('main', __name__)

from . import views