from sqlalchemy.sql import text

from projects.domain.user import User
from projects.adapters.users.repository import FlaskSqlAlchemyRepository


def test_repository_can_save_a_user(database):
    user = User("test-user-01", "test-user-01@example.com")
    repo = FlaskSqlAlchemyRepository(database)
    repo.create(user)
    database.session.commit()

    rows = database.session.execute(
        text("SELECT username, email, is_manager FROM users")
    )
    assert list(rows) == [("test-user-01", "test-user-01@example.com", False)]


def insert_user(session, username, email):
    session.execute(
        text(f"INSERT INTO users (username, email) VALUES ('{username}', '{email}')")
    )
    [[username]] = session.execute(
        text("SELECT id FROM users WHERE username=:username AND email=:email"),
        dict(username=username, email=email),
    )

def test_repository_can_retrieve_a_user(database):
    insert_user(database.session, "test-user-01", "test-user-01@example.com")

    repo = FlaskSqlAlchemyRepository(database)
    retrieved = repo.get_by_username("test-user-01")
    expected = User("test-user-01", "test-user-01@example.com")
    assert retrieved == expected  # User.__eq__ only compares reference
    assert retrieved.email == expected.email

