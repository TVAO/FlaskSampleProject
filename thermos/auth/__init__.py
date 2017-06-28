
# Create blueprint object of current module (authentication functionality)
# Blueprint of how to construct authentication modules
# Blueprint used to break up growing application into modules

from flask import Blueprint

auth = Blueprint('auth', __name__)

from . import views