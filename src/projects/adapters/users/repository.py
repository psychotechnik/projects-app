from typing import List
import abc

import flask_sqlalchemy

from projects.domain import user


class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def create(self, user: user.User):
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, user: user.User):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, id: int):
        raise NotImplementedError

    @abc.abstractmethod
    def get_by_username(self, username: str) -> user.User:
        raise NotImplementedError

    @abc.abstractmethod
    def get_by_email(self, email: str) -> user.User:
        raise NotImplementedError

    @abc.abstractmethod
    def get_by_token(self, token: str) -> user.User:
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, user: user.User):
        raise NotImplementedError

    @abc.abstractmethod
    def list(self) -> List[user.User]:
        raise NotImplementedError



class FlaskSqlAlchemyRepository(AbstractRepository):

    def __init__(self, db: flask_sqlalchemy.SQLAlchemy):
        self.db = db


    def create(self, user: user.User):
        self.db.session.add(user)

    def update(self, user: user.User) -> user.User:
        #user.username = user.username
        return user

    def get(self, id: int) -> user.User:
        return self.db.session.query(user.User).filter_by(id=id).scalar()

    def get_by_username(self, username: str) -> user.User:
        return self.db.session.execute(
                self.db.select(user.User).filter_by(username=username)
        ).scalar()

    def get_by_email(self, email: str) -> user.User:
        return self.db.session.execute(
                self.db.select(user.User).filter_by(email=email)
        ).scalar()

    def get_by_token(self, token: str) -> user.User:
        return self.db.session.execute(
                self.db.select(user.User).filter_by(token=token)
        ).scalar()

    def delete(self, user: user.User) -> None:
        self.db.session.delete(user)

    def list(self) -> List[user.User]:
        return self.db.session.execute(
                self.db.select(user.User).order_by(user.User.username)
        ).scalars()
