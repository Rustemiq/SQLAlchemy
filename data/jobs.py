import sqlalchemy
import datetime

from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin
from data.category import Category


class Job(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'jobs'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    teamleader = sqlalchemy.Column(sqlalchemy.Integer,
                                   sqlalchemy.ForeignKey("users.id"))
    user = sqlalchemy.orm.relationship('User')
    job = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    work_size = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    collaborators = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    start_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                   default=datetime.datetime.now)
    end_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                 default=datetime.datetime.now)
    is_finished = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True)
    creator = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    categories = sqlalchemy.orm.relationship("Category",
                                  secondary="jobs_to_category",
                                  backref="jobs")