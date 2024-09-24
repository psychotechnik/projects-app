from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth

from projects.adapters.users import repository
from projects.service_layer.users import handlers
from projects.entrypoints.flask import db
from projects.entrypoints.flask.api.errors import error_response

basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()


@basic_auth.verify_password
def verify_password(username, password):
    user = handlers.\
        get_user_by_username(username, repository.FlaskSqlAlchemyRepository(db))

    if user and user.check_password(password):
        return user

@basic_auth.error_handler
def basic_auth_error(status):
    return error_response(status)

@token_auth.verify_token
def verify_token(token):
    return handlers.\
        check_token(token, repository.FlaskSqlAlchemyRepository(db)) if token else None

@token_auth.error_handler
def token_auth_error(status):
    return error_response(status)

@token_auth.get_user_roles
def get_user_roles(user):
    return user.get_roles()
