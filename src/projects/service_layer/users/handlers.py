import secrets
from datetime import datetime, timezone, timedelta
from typing import List

from projects.adapters.users import repository
from projects.domain.user import User

def get_user(id: int, repo: repository.AbstractRepository):
    return repo.get(id)

def get_user_by_username(username: str, repo: repository.AbstractRepository):
    return repo.get_by_username(username)

def get_user_by_email(email: str, repo: repository.AbstractRepository):
    return repo.get_by_email(email)

def update_user(user: User, repo: repository.AbstractRepository):
    user = repo.update(user)
    repo.db.session.commit()
    return user

def get_users(repo: repository.AbstractRepository) -> List[User]:
    return repo.list()

def create_user(user: User, repo: repository.AbstractRepository) -> None:
    repo.create(user)
    repo.db.session.commit()

def issue_new_token(user: User, expires_in: int, repo: repository.AbstractRepository) -> str:
    now = datetime.now(timezone.utc)
    token = secrets.token_hex(16)
    token_expiration = now + timedelta(seconds=expires_in)
    user.token = token
    user.token_expiration = token_expiration
    repo.db.session.commit()
    return user.token

def revoke_token(user: User, repo: repository.AbstractRepository) -> None:
    user.revoke_token()
    repo.db.session.commit()

def check_token(token, repo: repository.AbstractRepository):
    user = repo.get_by_token(token)
    if user is None or user.token_expiration.replace(
            tzinfo=timezone.utc) < datetime.now(timezone.utc):
        return None
    return user

def promote_to_manager(user: User, repo: repository.AbstractRepository) -> None:
    user.is_manager = True
    repo.db.session.commit()
from flask import abort
def delete_user(id: int, repo: repository.AbstractRepository):
    user = repo.get(id)
    if not user:  
        abort(404, description="User not found")
    repo.delete(user) 
    repo.db.session.commit() 