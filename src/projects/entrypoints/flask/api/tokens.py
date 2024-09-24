from datetime import datetime, timezone, timedelta

from flask import current_app

from projects.entrypoints.flask import db
from projects.entrypoints.flask.api import bp
from projects.entrypoints.flask.api.auth import basic_auth, token_auth
from projects.adapters.users import repository
from projects.service_layer.users import handlers


@bp.route('/tokens', methods=['POST'])
@basic_auth.login_required
def get_token():
    """
    ---
    post:
      summary: Get authentication token
      description: Issue a new authentication token for the current user.
      tags:
        - Authentication 
      security:
        - basicAuth: []  # Using Basic Authentication
      responses:
        200:
          description: Token successfully generated.
          content:
            application/json:
              schema:
                type: object
                properties:
                  token:
                    type: string
                    description: The authentication token.
        401:
          description: Unauthorized. User credentials are invalid.
    """
    user = basic_auth.current_user()
    now = datetime.now(timezone.utc)
    if user.token and user.token_expiration.replace(
            tzinfo=timezone.utc) > now + timedelta(seconds=60):
        return {'token': user.token}

    token = handlers.issue_new_token(user, 86400, repository.FlaskSqlAlchemyRepository(db))
    return {'token': token}


@bp.route('/tokens', methods=['DELETE'])
@token_auth.login_required(role='manager')
def revoke_token():
    """
    ---
    delete:
      summary: Revoke authentication token
      description: Revoke the current user's authentication token.
      tags:
        - Authentication
      security:
        - bearerAuth: []  # Using tokens for authentication
      responses:
        204:
          description: Token successfully revoked.
        401:
          description: Unauthorized. User does not have permission or invalid token.
    """
    user = token_auth.current_user()
    handlers.revoke_token(user, repository.FlaskSqlAlchemyRepository(db))
    return '', 204

def register_routes_and_specs(app):
    with app.app_context(): 
        app.spec.path(view=get_token)
        app.spec.path(view=revoke_token)


