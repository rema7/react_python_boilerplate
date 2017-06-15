from datetime import datetime

from sqlalchemy import Column, BigInteger, String, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class BaseInfo:
    __table__ = None

    def __init__(self, **kwargs):
        for column in self.__table__.columns.items():
            column_name = column[0]
            if column_name not in kwargs:
                default = getattr(self.__table__.c, column_name).default
                if default:
                    kwargs[column_name] = default.arg if not hasattr(default.arg, '__call__') else None

        super(BaseInfo, self).__init__(**kwargs)

    _id = Column("id", BigInteger, primary_key=True, autoincrement=True)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow, nullable=False)


class ToDo(BaseInfo, Base):
    __tablename__ = 'todo'

    title = Column(String, nullable=False)
    description = Column(String, nullable=False)

    def update(self, title, description):
        self.title = title
        self.description = description

    def as_dict(self):
        return {
            'id': self._id,
            'title': self.title,
            'description': self.description,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }
