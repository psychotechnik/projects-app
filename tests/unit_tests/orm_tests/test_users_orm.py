from sqlalchemy.sql import text

from projects.domain.user import User


def test_users_mapper_can_load_users(database):
    database.session.execute(
        text( "INSERT into users (username, email ) VALUES "
            "('test-user-01', 'test-user-01@example.com'),"
            "('test-user-02', 'test-user-02@example.com'),"
            "('test-user-03', 'test-user-03@example.com')"
    )
    )
    expected = [
        User("test-user-01", "test-user-01@example.com"),
        User("test-user-02", "test-user-02@example.com"),
        User("test-user-03", "test-user-03@example.com"),
    ]
    assert database.session.query(User).all() == expected

def test_users_mapper_can_save_users(database):
    new_user = User("test-user-01", "test-user-01@example.com")
    database.session.add(new_user)
    database.session.commit()

    rows = list(database.session.execute(text('SELECT username, email FROM "users"')))
    assert rows == [("test-user-01", "test-user-01@example.com")]
