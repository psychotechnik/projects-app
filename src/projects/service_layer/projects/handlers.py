from typing import List

from projects.adapters.projects import repository
from projects.domain.project import Project

def get_project(id: int, repo: repository.AbstractProjectRepository) -> Project:
    """Gets a project by its ID."""
    return repo.get(id)

def get_projects(repo: repository.AbstractProjectRepository) -> List[Project]:
    """Gets a list of all projects."""
    return repo.list()

def create_project(name: str, description: str, repo: repository.AbstractProjectRepository) -> Project:
    """Creates a new project."""
    project = Project(name=name, description=description)
    repo.create(project)
    repo.session.commit()
    return project

def update_project(id: int, name: str, description: str, repo: repository.AbstractProjectRepository) -> Project:
    """Updates an existing project."""
    project = repo.get(id)
    if project:
        project.name = name
        project.description = description
        repo.update(project)
        repo.session.commit()
    return project

def delete_project(id: int, repo: repository.AbstractProjectRepository):
    """Deletes a project by its ID."""
    project = repo.get(id)
    if project:
        repo.delete(project)
        repo.session.commit()
