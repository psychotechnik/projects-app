from projects.domain.project import Project
from sqlalchemy.sql import text

# Test for loading project
def test_project_mapper_can_load_projects(database):
    database.session.execute(
        text("INSERT INTO projects (name, description) VALUES "
                "('test-project-01', 'Test Project Description 1'),"
                "('test-project-02', 'Test Project Description 2'),"
                "('test-project-03', 'Test Project Description 3')"
    )
    )
    
    projects = database.session.query(Project).all()
    
    assert len(projects) == 3
    assert projects[0].name == "test-project-01"
    assert projects[1].name == "test-project-02"
    assert projects[2].name == "test-project-03"

    assert projects[0].description == "Test Project Description 1"
    assert projects[1].description == "Test Project Description 2"
    assert projects[2].description == "Test Project Description 3"
    

#  Test for saving project 
def test_project_mapper_can_save_project(database):
    new_project = Project(name="project-01", description="Initial Description")
    database.session.add(new_project)
    database.session.commit()
    
    rows = list(database.session.execute(text('SELECT name, description FROM "projects"')))
    assert rows == [("project-01", "Initial Description")] 
    
    
#  Test for update project 
def test_project_mapper_can_update_project(database):
    new_project = Project(name="test-project-01", description="Initial Description")
    database.session.add(new_project)
    database.session.commit()
    
    project = database.session.query(Project).filter_by(name="test-project-01").one_or_none()
    assert project is not None, "Project was not created successfully."
    project.description = "Update Description"
    database.session.commit()
    
    rows = list(database.session.execute(text('SELECT name, description FROM "projects"')))
    assert rows == [("test-project-01", "Update Description")]     

# Test for deleting project 
def test_project_mapper_can_delete_project(database):
    database.session.execute(
        text("INSERT INTO projects (name, description) VALUES  ('test-project-01', 'Test Project Description 1')"
    )
    )
    project = database.session.query(Project).filter_by(name="test-project-01").one()
    database.session.delete(project)
    database.session.commit()
    
    rows = list(database.session.execute(text('SELECT name, description FROM "projects"')))
    assert rows == []
    
    
# Test for rollback on error    
def test_project_mapper_rollback_on_error(database):
    database.session.execute(
        text("INSERT INTO projects (name, description) VALUES ('test-project-01', 'Initial Description')")
    )
    database.session.commit()
    project = database.session.query(Project).filter_by(name="test-project-01").one()
    try:
        # Modify the task status and trigger an exception
        project.description = "Updated Description"
        raise Exception("Test Error")
    except:
        # Rolling back the transaction
        database.session.rollback()
        # Removing an object from the session
        database.session.expunge(project)
        # Reloading the project from the database after rollback
        project = database.session.query(Project).filter_by(name="test-project-01").one()

    rows = list(database.session.execute(text('SELECT name, description FROM "projects"')))
    assert rows == [("test-project-01", "Initial Description")]