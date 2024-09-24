from typing import List
import abc

from sqlalchemy import exc
from sqlalchemy import orm

from projects.domain import project


class AbstractProjectRepository(abc.ABC):

    @abc.abstractmethod
    def create(self, project: project.Project):
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, project: project.Project):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, id: int):
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, project: project.Project):
        raise NotImplementedError

    @abc.abstractmethod
    def list(self) -> List[project.Project]:
        raise NotImplementedError


class SqlAlchemyProjectRepository(AbstractProjectRepository):
    def __init__(self, session: orm.Session):
        self.session = session

    def create(self, project: project.Project):
        self.session.add(project)

    def update(self, project: project.Project) -> project.Project:
        return project

    def get(self, id: int) -> project.Project:
        try:
            return self.session.query(project.Project).filter_by(id=id).one()
        except exc.NoResultFound:
            pass

    def delete(self, project: project.Project) -> None:
        self.session.delete(project)

    def list(self) -> List[project.Project]:
        return self.session.query(project.Project).all()