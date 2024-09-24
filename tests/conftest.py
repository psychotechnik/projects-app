from base64 import b64encode

import pytest
from sqlalchemy.orm import scoped_session, sessionmaker

from projects import config
from projects.entrypoints.flask import create_app, db
from projects.domain.user import User

from projects.domain.project import Project
from projects.domain.task import Task

from projects.adapters.projects.repository import SqlAlchemyProjectRepository
from projects.adapters.users.repository import FlaskSqlAlchemyRepository


class TestConfig(config.Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "postgresql://eqb:eqb@127.0.0.1:5432/test_projects-app"

#ALEMBIC_CONFIG = '/home/pk/dev/pyproj/takehome-assignments/impactpoint/projects-app/alembic.ini'


@pytest.fixture(scope="session")
def test_client():
    test_app = create_app(TestConfig)
    test_client = test_app.test_client()

    with test_app.app_context():
        yield test_client


@pytest.fixture(scope="session")
def database(test_client):
    db.create_all()

    yield db

    db.drop_all()


@pytest.fixture(autouse=True)
def enable_transactional_tests(database):
    """https://docs.sqlalchemy.org/en/20/orm/session_transaction.html#joining-a-session-into-an-external-transaction-such-as-for-test-suites"""
    connection = database.engine.connect()
    transaction = connection.begin()

    database.session = scoped_session(
        session_factory=sessionmaker(
            bind=connection,
            join_transaction_mode="create_savepoint",
        )
    )

    yield

    database.session.close()
    transaction.rollback()
    connection.close()


#### Projects
####

def create_project(name: str, description: str = None):
    repo = SqlAlchemyProjectRepository(db.session)
    new_project = Project(name=name, description=description)
    repo.create(new_project)
    db.session.commit()
    return new_project

def create_projects_and_tasks():
    project1 = create_project("Test Project 1", "Description for project 1")
    project2 = create_project("Test Project 2", "Description for project 2")
    
    create_task(project1.id, "Task 1 for Project 1", "NEW")
    create_task(project1.id, "Task 2 for Project 1", "IN_PROGRESS")
    create_task(project2.id, "Task 1 for Project 2", "COMPLETED")
    

def create_task(project_id: int, name: str, status: str = None):
    repo = SqlAlchemyTaskRepository(db.session)
    new_task = Task(project_id=project_id, name=name, status=status)
    repo.create(new_task)
    db.session.commit()
    return new_task
        
def create_users():
    """Creating users: manager and employee."""
    manager = User(username='manager', email='manager@example.com', is_manager=True)
    manager.set_password('manager_password')
    
    employee = User(username='employee', email='employee@example.com', is_manager=False)
    employee.set_password('employee_password')
    
    db.session.add(manager)
    db.session.add(employee)
    db.session.commit()

def get_basic_auth_header(username, password):
    """Returns a header with Basic Auth."""
    credentials = f"{username}:{password}".encode('utf-8')
    basic_auth_header = { 'Authorization': 'Basic ' + b64encode(credentials).decode('utf-8')}
    return basic_auth_header

def get_token_auth_header(client, username, password):  
    """Returns a header with Token Auth. """
    basic_auth_header = get_basic_auth_header(username, password)
    token_response =  client.post('/api/tokens', headers=basic_auth_header)
    token = token_response.get_json()['token']
    return {
        'Authorization': f'Bearer {token}'
    }
    

#@pytest.fixture(scope="function", 
#    params=[
#        ('manager', 'manager_password', 200),
#        ('employee', 'employee_password', 200),                
#    ],
#    ids=[
#        'Role Manager',
#        'Role Employee',
#    ]
#)

#### Users
####

@pytest.fixture
def manager_user():

    user = User(
        username="manager1", 
        email="manager@example.com", 
        is_manager=True, 
    )
    user.set_password('secret')
    user.issue_token()
    db.session.add(user)
    db.session.commit()

    yield user


class AuthActions:
    def __init__(self, client):
        self._client = client

    def login(self, username="test", password="test"):
        return self._client.post(
            "/auth/login", data={"username": username, "password": password}
        )

    def logout(self):
        return self._client.get("/auth/logout")


@pytest.fixture
def auth(test_client):
    return AuthActions(test_client)

#@pytest.fixture
#def userA():
#    user = User(id=1, name="Alice")
#    db.session.add(user)
#    db.session.commit()

#    yield user


#@pytest.fixture
#def userB():
#    user = User(id=1, name="Bob")
#    db.session.add(user)
#    db.session.commit()

#    yield user


"""
@pytest.fixture(scope='session')
def database(request):
    '''
    Create a Postgres database for the tests, and drop it when the tests are done.
    '''
    pg_host = DB_OPTS.get("host")
    pg_port = DB_OPTS.get("port")
    pg_user = DB_OPTS.get("username")
    pg_db = DB_OPTS["database"]

    init_postgresql_database(pg_user, pg_host, pg_port, pg_db)

    @request.addfinalizer
    def drop_database():
        drop_postgresql_database(pg_user, pg_host, pg_port, pg_db, 9.6)


@pytest.fixture(scope='session')
def app(database):
    '''
    Create a Flask app context for the tests.
    '''
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = DB_CONN

    return app


@pytest.fixture(scope='session')
def _db(app):
    '''
    Provide the transactional fixtures with access to the database via a Flask-SQLAlchemy
    database connection.
    '''
    db = SQLAlchemy(app=app)

    return db


@pytest.fixture(scope='session')
def app(request):
    app = create_app(TestConfig)
    #app.config['SQLALCHEMY_DATABASE_URI'] == DB_CONN
    return app

#def apply_migrations():
#    config = Config(ALEMBIC_CONFIG)
#    upgrade(config, 'head')

@pytest.fixture(scope='session')
def database(app, request):

    @request.addfinalizer
    def drop_database():
        app_db.drop_all()

    #app_db.app = app
    #apply_migrations()
    return app_db

@pytest.fixture(scope='session')
def _db(database):
    return database

# Automatically enable transactions for all tests, without importing any extra fixtures.
#@pytest.fixture(autouse=True)
#def enable_transactional_tests(db_session):
#    pass


@pytest.fixture(scope='function')
def session(db, request):
    connection = db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session = db._make_scoped_session(options=options)
    
    db.session = session

    def teardown():
        transaction.rollback()
        connection.close()
        session.remove()

    request.addfinalizer(teardown)

    user = User(
        username="manager", 
        email="manager@example.com", 
        is_manager=True, 
        password_hash=_mgr_pass,
        token="84cf0a9a4a681a8902dfa7e8e9d5a2d4",
    )
    db.session.add(user)
    db.session.commit()

    return session


@pytest.fixture
def client(app):
    return app.test_client()


class AuthActions:
    def __init__(self, client):
        self._client = client

    def login(self, username="test", password="test"):
        return self._client.post(
            "/auth/login", data={"username": username, "password": password}
        )

    def logout(self):
        return self._client.get("/auth/logout")


@pytest.fixture
def auth(client):
    return AuthActions(client)
"""
