import datetime
import sqlalchemy
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Blog(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'blogs'

    date = '.'.join(str(datetime.date.today()).split('-'))
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    about = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    author = sqlalchemy.Column(sqlalchemy.Integer,
                               sqlalchemy.ForeignKey("users.id"), nullable=True)
    create_date = sqlalchemy.Column(sqlalchemy.String,
                                    default=date)

    user = orm.relation('User')
