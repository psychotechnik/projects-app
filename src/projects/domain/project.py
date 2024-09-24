from typing import Optional

class Project:
    id: Optional[int]
    name: str
    description: Optional[str] = None

    def __repr__(self):
        return f'<Project {self.name}>'
