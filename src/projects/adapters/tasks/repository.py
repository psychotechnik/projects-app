from typing import List
import abc

from sqlalchemy import exc
from sqlalchemy import orm

from projects.domain import  task

class AbstractTaskRepository(abc.ABC):

    @abc.abstractmethod
    def create(self, task: task.Task):
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, task: task.Task):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, id: int):
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, task: task.Task):
        raise NotImplementedError

    @abc.abstractmethod
    def list(self) -> List[task.Task]:
        raise NotImplementedError

class SqlAlchemyTaskRepository(AbstractTaskRepository):
    def __init__(self, session: orm.Session):
        self.session = session

    def create(self, task: task.Task):
        self.session.add(task)

    def update(self, task: task.Task) -> task.Task:
        return task

    def get(self, id: int) -> task.Task:
        try:
            return self.session.query(task.Task).filter_by(id=id).one()
        except exc.NoResultFound:
            pass

    def delete(self, task: task.Task) -> None:
        self.session.delete(task)

    def list(self, project_id: int) -> List[task.Task]:
        return self.session.query(task.Task).filter_by(project_id=project_id).all()
