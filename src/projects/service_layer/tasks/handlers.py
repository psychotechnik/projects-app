from typing import List

from projects.adapters.tasks import repository
from projects.domain.task import Task #TaskStatusEnum

def get_task(id: int, repo: repository.AbstractTaskRepository) -> Task:
    """Gets a task by its ID."""
    return repo.get(id)

def get_tasks_for_project(project_id: int, repo: repository.AbstractTaskRepository) -> List[Task]:
    """Gets all tasks for a specific project."""
    return repo.list(project_id)

def create_task(project_id: int, name: str, status:str, repo: repository.AbstractTaskRepository) -> Task:
    """Creates a new task in the project."""
    task = Task(id=None, project_id=project_id, name=name, status=status)
    repo.create(task)
    repo.session.commit()
    return task

def update_task_status(project_id: int, task_id: int, status: str, repo: repository.AbstractTaskRepository) -> Task:
    """Updates the task status."""
    task = repo.get(task_id)
    if task and task.project_id == project_id:
        task.status = status  # Enum ??
        repo.update(task)
        repo.session.commit()
    return task

def delete_task(id: int, repo: repository.AbstractTaskRepository):
    """Deletes a task by its ID."""
    task = repo.get(id)
    if task:
        repo.delete(task)
        repo.session.commit()