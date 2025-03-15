# Blueprint for authorisation registration

from flask import Blueprint

auth = Blueprint('auth', __name__)

from . import views