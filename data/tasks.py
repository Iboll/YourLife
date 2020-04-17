import datetime
import sqlalchemy
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Task(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'tasks'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    about = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    is_finished = sqlalchemy.Column(sqlalchemy.Boolean)
    author = sqlalchemy.Column(sqlalchemy.Integer,
                               sqlalchemy.ForeignKey("users.id"), nullable=True)
    create_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                    default=datetime.date.today)

    user = orm.relation('User')
