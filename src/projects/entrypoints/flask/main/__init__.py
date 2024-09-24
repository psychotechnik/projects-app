from flask import Blueprint

bp = Blueprint('main', __name__)

from projects.entrypoints.flask.main import routes
