
# Create blueprint object of current module (auth)

from flask import Blueprint

auth = Blueprint('auth', __name__)

from . import views