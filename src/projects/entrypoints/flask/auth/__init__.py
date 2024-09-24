from flask import Blueprint, current_app
import click
from werkzeug import exceptions as wz_exc

from projects.service_layer.users import handlers
from projects.entrypoints.flask import db
from projects.domain.user import User
from projects.adapters.users import repository

bp = Blueprint('auth', __name__)

@bp.cli.command('create-manager')
@click.option('--username')
@click.option('--email')
@click.option('--password')
def create(username, email, password):
    repo = repository.FlaskSqlAlchemyRepository(db)
    user = None

    if handlers.get_user_by_username(username, repository.FlaskSqlAlchemyRepository(db)):
        current_app.logger.info(f"user exists with username: {username}. Please select another username.")
        return

    if handlers.get_user_by_email(email, repository.FlaskSqlAlchemyRepository(db)):
        current_app.logger.info(f"user exists with e-mail: {email}. Please select another e-mail.")
        return

    if not user:
        user = User(
                username=username,
                email=email,
        )
        user.set_password(password)
        handlers.create_user(user, repo)
        handlers.promote_to_manager(user, repo)
        token = handlers.issue_new_token(user, 86400, repository.FlaskSqlAlchemyRepository(db))
        current_app.logger.info(f"Manager created with token {token}")

from projects.entrypoints.flask.auth import routes
