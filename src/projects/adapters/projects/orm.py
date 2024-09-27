from sqlalchemy import Column, Integer, String
from projects.domain import project
from projects.entrypoints.flask import db
from sqlalchemy.orm import registry

projects = db.Table(
    "projects",
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(100), nullable=False),
    Column("description", String(255), nullable=True)
)

def start_mappers():
    mapper_registry = registry()
    mapper_registry.map_imperatively(project.Project, projects)