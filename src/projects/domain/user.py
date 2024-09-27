import secrets
from typing import Optional
from datetime import datetime, timezone, timedelta

from werkzeug.security import generate_password_hash, check_password_hash
#import jwt


class User:

    id: Optional[int]
    password_hash: Optional[str]
    token: Optional[str]
    token_expiration: Optional[datetime]

    def __init__(self, 
            username: str, 
            email: str, 
            is_manager: bool = False,
                ) -> None:

        self.username = username
        self.email = email
        self.is_manager = is_manager

    def __eq__(self, other):
        if not isinstance(other, User):
            return False
        return other.username == self.username

    def __hash__(self):
        return hash(self.id)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def issue_token(self, expires_in: int=86400):
        now = datetime.now(timezone.utc)
        token = secrets.token_hex(16)
        token_expiration = now + timedelta(seconds=expires_in)
        self.token = token
        self.token_expiration = token_expiration

    def get_roles(self):
        return "manager" if self.is_manager else None

    #def revoke_token(self) -> None:
    #    self.token_expiration = datetime.now(timezone.utc) - timedelta(
    #        seconds=1)

    #def get_reset_password_token(self, expires_in=600):
    #    return jwt.encode(
    #        {'reset_password': self.id, 'exp': time() + expires_in},
    #        current_app.config['SECRET_KEY'], algorithm='HS256')

    #@staticmethod
    #def verify_reset_password_token(token):
    #    try:
    #        id = jwt.decode(token, current_app.config['SECRET_KEY'],
    #                        algorithms=['HS256'])['reset_password']
    #    except Exception:
    #        return
    #    return db.session.get(User, id)

    def to_dict(self, include_email=False):
        data = {
            'id': self.id,
            'username': self.username,
            'email': self.email,
        }
        if include_email:
            data['email'] = self.email
        return data

    def from_dict(self, data, new_user=False):
        for field in ['username', 'email',]:
            if field in data:
                setattr(self, field, data[field])
        if new_user and 'password' in data:
            self.set_password(data['password'])


