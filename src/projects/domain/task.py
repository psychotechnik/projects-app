from sqlalchemy import Enum
from typing import Optional
from projects.entrypoints.flask import db

class Task:
    id: Optional[int]
    project_id: int
    name: str
    status:  Optional[str] = None

    def __repr__(self):
        return f'<Task {self.name} - {self.status}>'
