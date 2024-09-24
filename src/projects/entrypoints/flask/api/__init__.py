from flask import Blueprint

bp = Blueprint('api', __name__)

from projects.entrypoints.flask.api import users, errors, tokens,  projects, tasks
