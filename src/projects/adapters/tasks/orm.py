from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Table
from projects.domain import project, task
from projects.entrypoints.flask import db
from sqlalchemy.orm import registry

tasks = db.Table(
    "tasks",
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("project_id", Integer, ForeignKey("projects.id"), nullable=False),
    Column("name", String(100), nullable=False),
    Column("status", String(100), nullable=True)
    # Column("status", Enum(task.TaskStatusEnum), default=task.TaskStatusEnum.NEW, nullable=False)
)

def start_mappers():
    mapper_registry = registry()
    mapper_registry.map_imperatively(task.Task, tasks)