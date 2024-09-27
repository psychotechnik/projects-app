#import pytest

from projects.domain.user import User
from projects.service_layer.users import handlers
from projects.adapters.users.repository import AbstractRepository as UsersAbstractRepository


class FakeSession:
    committed = False

    def commit(self):
        print("FakeSession.commit called --")
        self.committed = True



class FakeFlaskSQLAlchemy:

    def __init__(self, session: FakeSession):
        super().__init__()
        self.session = session



class FakeUsersRepository(UsersAbstractRepository):

    def __init__(self, users, db: FakeFlaskSQLAlchemy):
        super().__init__()
        self._users = set(users)
        self.db = db

    def create(self, user):
        self._users.add(user)

    def get(self, id):
        return next(u for u in self._users if u.id == id)

    def list(self):
        return list(self._users)

    def delete(self, user: User) -> None: 
        self._users.remove(user)

    def get_by_email(self, email:str) -> User:
        return next(u for u in self._users if u.email == email)

    def get_by_token(self, token: str) -> User:
        return next(u for u in self._users if u.token == token)

    def get_by_username(self, username: str) -> User:
        return next(u for u in self._users if u.username == username)

    def update(self, user: User) -> User:
        return user
        



def test_returns_user():

    u1 = User(username='test-user-01', email='test-user-01@example.com')
    u1.id = 1
    u2 = User(username='test-user-02', email='test-user-02@example.com')
    u2.id = 2
    u3 = User(username='test-user-03', email='test-user-03@example.com')
    u3.id = 3
    u4 = User(username='test-user-04', email='test-user-04@example.com')
    u4.id = 4
    u5 = User(username='test-user-05', email='test-user-05@example.com')
    u5.id = 5

    db = FakeFlaskSQLAlchemy(session=FakeSession())

    repo = FakeUsersRepository([u1, u2, u3, u4, u5], db)
    user1  = handlers.get_user(u1.id, repo)
    user2 = handlers.get_user(u2.id, repo)
    user3 = handlers.get_user(u3.id, repo)
    user4 = handlers.get_user(u4.id, repo)
    user5 = handlers.get_user(u5.id, repo)

    assert user1.id == 1
    assert user2.id == 2
    assert user3.id == 3
    assert user4.id == 4
    assert user5.id == 5


def test_commits():

    u1 = User(username='test-user-01', email='test-user-01@example.com')
    u1.id = 1
    db = FakeFlaskSQLAlchemy(session=FakeSession())
    repo = FakeUsersRepository([u1], db)
    _  = handlers.update_user(u1, repo)

    assert repo.db.session.committed
