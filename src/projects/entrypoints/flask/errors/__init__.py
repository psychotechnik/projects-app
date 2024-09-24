from flask import Blueprint

bp = Blueprint('errors', __name__)

from projects.entrypoints.flask.errors import handlers

