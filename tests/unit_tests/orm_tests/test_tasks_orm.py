from projects.domain.task import Task
from sqlalchemy.sql import text

# Test for loading tasks
def test_task_mapper_can_load_tasks(database):
    database.session.execute(
        text("INSERT INTO projects (name, description) VALUES ('test-project', 'Test Project Description')")
    )
    project_id = database.session.execute(text("SELECT id FROM projects WHERE name='test-project'")).scalar()

    database.session.execute(
        text(f"INSERT INTO tasks (project_id, name, status) VALUES "
             f"({project_id}, 'task-01', 'Pending'),"
             f"({project_id}, 'task-02', 'Completed')")
    )

    expected_tasks = [
        Task(name='task-01', status='Pending', project_id=project_id),
        Task(name='task-02', status='Completed', project_id=project_id)
    ]

    tasks = database.session.query(Task).all()

    assert len(tasks) == 2
    assert tasks[0].name == "task-01"
    assert tasks[1].name == "task-02"

    assert tasks[0].status == "Pending"
    assert tasks[1].status == "Completed"

# Test for saving tasks
def test_task_mapper_can_save_task(database):
    database.session.execute(
        text("INSERT INTO projects (name, description) VALUES ('test-project', 'Test Project Description')")
    )
    project_id = database.session.execute(text("SELECT id FROM projects WHERE name='test-project'")).scalar()

    new_task = Task(name="task-01", status="Pending", project_id=project_id)
    database.session.add(new_task)
    database.session.commit()

    rows = list(database.session.execute(text('SELECT name, status FROM "tasks"')))
    assert rows == [("task-01", "Pending")]

# Test for deleting tasks
def test_task_mapper_can_delete_task(database):
    database.session.execute(
        text("INSERT INTO projects (name, description) VALUES ('test-project', 'Test Project Description')")
    )
    project_id = database.session.execute(text("SELECT id FROM projects WHERE name='test-project'")).scalar()

    database.session.execute(
        text(f"INSERT INTO tasks (project_id, name, status) VALUES ({project_id}, 'task-01', 'Pending')")
    )
    task = database.session.query(Task).filter_by(name="task-01").one()
    database.session.delete(task)
    database.session.commit()

    rows = list(database.session.execute(text('SELECT name, status FROM "tasks"')))
    assert rows == []

# Test for updating tasks
def test_task_mapper_can_update_task(database):
    database.session.execute(
        text("INSERT INTO projects (name, description) VALUES ('test-project', 'Test Project Description')")
    )
    project_id = database.session.execute(text("SELECT id FROM projects WHERE name='test-project'")).scalar()

    database.session.execute(
        text(f"INSERT INTO tasks (project_id, name, status) VALUES ({project_id}, 'task-01', 'Pending')")
    )
    task = database.session.query(Task).filter_by(name="task-01").one()
    task.status = "Completed"
    database.session.commit()

    rows = list(database.session.execute(text('SELECT name, status FROM "tasks"')))
    assert rows == [("task-01", "Completed")]   

# Test for rollback on error
def test_task_mapper_rollback_on_error(database):
    database.session.execute(
        text("INSERT INTO projects (name, description) VALUES ('test-project', 'Test Project Description')")
    )
    project_id = database.session.execute(text("SELECT id FROM projects WHERE name='test-project'")).scalar()
    assert project_id is not None, "Project was not created successfully."
    database.session.execute(
        text(f"INSERT INTO tasks (project_id, name, status) VALUES ({project_id}, 'task-01', 'Pending')")
    )
    database.session.commit()  # Commit the transaction to ensure the task is saved
    task = database.session.query(Task).filter_by(name="task-01").one_or_none()
    assert task is not None, "Task was not created successfully."

    try:
        # Modify the task status and trigger an exception
        task.status = "Completed"
        raise Exception("Test Error")
    except:
        # Rollback the transaction
        database.session.rollback()
        # Clear the session to ensure the task is fetched anew from the database
        database.session.expire_all()
        # Reload the task from the database to verify the rollback
        task_after_rollback = database.session.query(Task).filter_by(name="task-01").one_or_none()

    assert task_after_rollback is not None, "Task was not found after rollback."
    assert task_after_rollback.status == "Pending"
    rows = list(database.session.execute(text('SELECT name, status FROM "tasks"')))
    assert rows == [("task-01", "Pending")]
