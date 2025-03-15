# entry point to the application

from flask import Blueprint
from ..models import Permission

main = Blueprint('main', __name__)

from . import views, errors

@main.context_processor
def inject_permission():
    return dict(Permission=Permission)

 