from sqlalchemy.sql import text
from projects.domain.task import Task
from projects.adapters.tasks.repository import SqlAlchemyTaskRepository

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

# Helper function for creating a task
def insert_task(session, name, status, project_id):
    session.execute(
        text(f"INSERT INTO tasks (name, status, project_id) VALUES ('{name}', '{status}', {project_id})")
    )
    [[task_id]] = session.execute(
        text("SELECT id FROM tasks WHERE name=:name AND status=:status AND project_id=:project_id"),
        dict(name=name, status=status, project_id=project_id),
    )
    return task_id

# Creation Verification Test
def test_repository_can_save_a_task(database):
    project_id = insert_project(database.session, "test-project-01", "Test Project Description")
    task = Task(name="test-task-01", status="pending", project_id=project_id)
    repo = SqlAlchemyTaskRepository(database.session)
    repo.create(task)
    database.session.commit()
    rows = database.session.execute(text("SELECT name, status, project_id FROM tasks"))
    assert list(rows) == [("test-task-01", "pending", project_id)]

# Test for checking receipt by ID
def test_repository_can_retrieve_a_task(database):
    project_id = insert_project(database.session, "test-project-01", "Test Project Description")
    task_id = insert_task(database.session, "test-task-01", "pending", project_id)
    repo = SqlAlchemyTaskRepository(database.session)
    retrieved = repo.get(task_id)
    assert retrieved.id == task_id
    assert retrieved.name == "test-task-01"
    assert retrieved.status == "pending"
    assert retrieved.project_id == project_id

# Update Check Test
def test_repository_can_update_a_task(database):
    project_id = insert_project(database.session, "test-project-01", "Test Project Description")
    task_id = insert_task(database.session, "test-task-01", "pending", project_id)
    repo = SqlAlchemyTaskRepository(database.session)
    task = repo.get(task_id)
    task.status = "completed"
    repo.update(task)
    database.session.commit()
    updated_task = repo.get(task_id)
    assert updated_task.id == task_id
    assert updated_task.name == "test-task-01"
    assert updated_task.status == "completed"

# Deletion Check Test
def test_repository_can_delete_a_task(database):
    project_id = insert_project(database.session, "test-project-01", "Test Project Description")
    task_id = insert_task(database.session, "test-task-01", "pending", project_id)
    repo = SqlAlchemyTaskRepository(database.session)
    task = repo.get(task_id)
    repo.delete(task)
    database.session.commit()
    deleted_task = repo.get(task_id)
    assert deleted_task is None

# Test of checking the receipt of the task list
def test_repository_can_list_tasks(database):
    project_id = insert_project(database.session, "test-project-01", "Test Project Description")
    insert_task(database.session, "test-task-01", "pending", project_id)
    insert_task(database.session, "test-task-02", "completed", project_id)
    insert_task(database.session, "test-task-03", "pending", project_id)
    repo = SqlAlchemyTaskRepository(database.session)
    tasks = repo.list(project_id)
    assert len(tasks) == 3
    assert tasks[0].name == "test-task-01"
    assert tasks[1].name == "test-task-02"
    assert tasks[2].name == "test-task-03"
    assert tasks[0].status == "pending"
    assert tasks[1].status == "completed"
    assert tasks[2].status == "pending"
