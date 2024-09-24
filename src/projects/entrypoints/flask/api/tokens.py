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
    user = token_auth.current_user()
    handlers.revoke_token(user, repository.FlaskSqlAlchemyRepository(db))
    return '', 204

