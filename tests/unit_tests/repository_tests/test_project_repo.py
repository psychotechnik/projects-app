from sqlalchemy.sql import text
from projects.domain.project import Project
from projects.adapters.projects.repository import SqlAlchemyProjectRepository

# Helper function for creating a project
def insert_project(session, name, description):
    session.execute(
        text(f"INSERT INTO projects (name, description) VALUES ('{name}', '{description}')")
    )
    [[project_id]] = session.execute(
        text("SELECT id FROM projects WHERE name=:name AND description=:description"),
        dict(name=name, description=description),
    )
    return project_id

# Creation Verification Test
def test_repository_can_save_a_project(database):
    # Create a new project instance
    project = Project(name="test-project-01", description="Test Project Description")
    repo = SqlAlchemyProjectRepository(database.session)  # Use the correct session
    # Save the project
    repo.create(project)
    database.session.commit()
    # Verify the project was saved in the database
    rows = database.session.execute(text("SELECT name, description FROM projects"))
    assert list(rows) == [("test-project-01", "Test Project Description")]
    
# Test for checking receipt by ID
def test_repository_can_retrieve_a_project(database):
    project_id = insert_project(database.session, "test-project-01", "Test Project Description")
    repo = SqlAlchemyProjectRepository(database.session)
    retrieved = repo.get(project_id)
    assert retrieved.id == project_id
    assert retrieved.name == "test-project-01"
    assert retrieved.description == "Test Project Description"
    
# Update Check Test    
def test_repository_can_update_a_project(database):
    project_id = insert_project(database.session, "test-project-01", "Old Description")
    repo = SqlAlchemyProjectRepository(database.session)
    project = repo.get(project_id)
    project.description = "Updated Description"
    repo.update(project)
    database.session.commit()

    updated_project = repo.get(project_id)
    
    assert updated_project.id == project_id
    assert updated_project.name == "test-project-01"
    assert updated_project.description == "Updated Description"
    
# Deletion Check Test
def test_repository_can_delete_a_project(database):
    project_id = insert_project(database.session, "test-project-01", "Test Project Description")
    repo = SqlAlchemyProjectRepository(database.session)
    project = repo.get(project_id)
    repo.delete(project)
    database.session.commit()

    deleted_project = repo.get(project_id)
    assert deleted_project is None
    
# Test of checking the receipt of the task list
def test_repository_can_list_projects(database):
    insert_project(database.session, "test-project-01", "Description 1")
    insert_project(database.session, "test-project-02", "Description 2")
    insert_project(database.session, "test-project-03", "Description 3")

    repo = SqlAlchemyProjectRepository(database.session)
    projects = repo.list()

    assert len(projects) == 3
    assert projects[0].name == "test-project-01"
    assert projects[1].name == "test-project-02"
    assert projects[2].name == "test-project-03"

    assert projects[0].description == "Description 1"
    assert projects[1].description == "Description 2"
    assert projects[2].description == "Description 3"
    