#import sqlalchemy as sa
from flask import (
    request, 
    #url_for, 
    #abort,
)

from projects.domain.user import User
from projects.adapters.users import repository
from projects.service_layer.users import handlers
from projects.entrypoints.flask.api import bp
from projects.entrypoints.flask.api.auth import token_auth
from projects.entrypoints.flask.api.errors import bad_request
from projects.entrypoints.flask import db
from projects.entrypoints.flask.schema import UserSchema


@bp.route('/users/<int:id>', methods=['GET'])
@token_auth.login_required
def get_user(id):
    """
    ---
    get:
      summary: Retrieve a user by ID
      description: Retrieve a specific user by their ID.
      tags:
        - User
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: integer
          description: The ID of the user to retrieve.
      responses:
        200:
          description: Successfully retrieved the user.
          content:
            application/json:
              schema: UserSchema
        401:
          description: Unauthorized access.
        404:
          description: User not found.
    """ 
    repo = repository.FlaskSqlAlchemyRepository(db)
    user = handlers.get_user(id, repo)
    return user.to_dict()

@bp.route("/users/user-by-username/<username>")
@token_auth.login_required
def user_by_username(username):
    """
    ---
    get:
      summary: Retrieve a user by username
      description: Retrieve a user based on their username.
      tags:
        - User
      parameters:
        - name: username
          in: path
          required: true
          schema:
            type: string
          description: The username of the user to retrieve.
      responses:
        200:
          description: Successfully retrieved the user.
          content:
            application/json:
              schema:
                type: object
                properties:
                  username:
                    type: string
                  email:
                    type: string
        401:
          description: Unauthorized access.
        404:
          description: User not found.
    """  
    repo = repository.FlaskSqlAlchemyRepository(db)
    user = handlers.get_user_by_username(username, repo)
    return {
        "username": user.username,
        "email": user.email,
    }

@bp.route('/users', methods=['GET'])
@token_auth.login_required
def get_users():
    """
    ---
    get:
      summary: Retrieve all users
      description: Get a list of all users.
      tags:
        - User
      responses:
        200:
          description: Successfully retrieved all users.
          content:
            application/json:
              schema:
                type: array
                items:
                  type: object
                  properties:
                    username:
                      type: string
                    email:
                      type: string
        401:
          description: Unauthorized access.
    """    
    #page = request.args.get('page', 1, type=int)
    #per_page = min(request.args.get('per_page', 10, type=int), 100)
    #return User.to_collection_dict(sa.select(User), page, per_page,
    #                               'api.get_users')
    repo = repository.FlaskSqlAlchemyRepository(db)
    users = handlers.get_users(repo)
    data = []
    for user in users:
        data.append({
            "username": user.username,
            "email": user.email,
        })
    return data

@bp.route('/users/promote/<username>', methods=['PATCH'])
@token_auth.login_required(role='manager')
def promote_to_manager(username):
    """
    ---
    patch:
      summary: Promote a user to manager
      description: Grant manager privileges to a specific user.
      tags:
        - User
      parameters:
        - name: username
          in: path
          required: true
          schema:
            type: string
          description: The username of the user to promote.
      responses:
        200:
          description: User successfully promoted.
          content:
            application/json:
              schema:
                type: object
                properties:
                  status:
                    type: string
                    example: ok
        401:
          description: Unauthorized access.
        404:
          description: User not found.
    """
    repo = repository.FlaskSqlAlchemyRepository(db)
    user = handlers.get_user_by_username(username, repo)
    handlers.promote_to_manager(user, repo)
    return {"status": "ok"}, 200

@bp.route('/users', methods=['POST'])
@token_auth.login_required(role='manager')
def create_user():
    """
    ---
    post:
      summary: Create a new user
      description: Create a new user account. Only managers are allowed to create users.
      tags:
        - User
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                username:
                  type: string
                  description: The desired username.
                email:
                  type: string
                  description: The user's email address.
                password:
                  type: string
                  description: The user's password.
      responses:
        201:
          description: User successfully created.
          content:
            application/json:
              schema: UserSchema
        400:
          description: Invalid input data.
        401:
          description: Unauthorized access.
    """
    data = request.get_json()
    if 'username' not in data or 'email' not in data or 'password' not in data:
        return bad_request('must include username, email and password fields')

    if handlers.get_user_by_username(data['username'], repository.FlaskSqlAlchemyRepository(db)):
        return bad_request('please use a different username')

    if handlers.get_user_by_email(data['email'], repository.FlaskSqlAlchemyRepository(db)):
        return bad_request('please use a different e-mail')

    repo = repository.FlaskSqlAlchemyRepository(db)
    user = User(
            username=data.get("username"),
            email=data.get("email"),
    )
    if 'password' in data:
        user.set_password(data['password'])

    handlers.create_user(user, repo)

    return user.to_dict(), 201, {}
    
def register_routes_and_specs(app):
    with app.app_context(): 
        app.spec.path(view=get_user)
        app.spec.path(view=user_by_username)
        app.spec.path(view=get_users)
        app.spec.path(view=promote_to_manager)
        app.spec.path(view=create_user)
      
"""
@bp.route('/users/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_user(id):
    if token_auth.current_user().id != id:
        abort(403)
    user = db.get_or_404(User, id)
    data = request.get_json()
    if 'username' in data and data['username'] != user.username and \
        db.session.scalar(sa.select(User).where(
            User.username == data['username'])):
        return bad_request('please use a different username')
    if 'email' in data and data['email'] != user.email and \
        db.session.scalar(sa.select(User).where(
            User.email == data['email'])):
        return bad_request('please use a different email address')
    user.from_dict(data, new_user=False)
    db.session.commit()
    return user.to_dict()

"""
