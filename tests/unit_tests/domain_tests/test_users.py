
from projects.domain.user import User

def test_password_hashing():
    u = User(username='test-user-01', email='test-user-01@example.com')
    u.set_password('secret')
    assert not u.check_password('notsecret')
    assert u.check_password('secret')

def test_get_roles():
    u = User(username='test-user-01', email='test-user-01@example.com')
    assert not u.get_roles()

    u = User(username='test-user-01', email='test-user-01@example.com', is_manager=True)
    assert u.get_roles() == "manager"
