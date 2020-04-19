import datetime

import sqlalchemy
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


#  Класс привычек
class Habit(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'habits'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    author = sqlalchemy.Column(sqlalchemy.Integer,
                               sqlalchemy.ForeignKey("users.id"), nullable=True)
    day1 = sqlalchemy.Column(sqlalchemy.Boolean)
    day2 = sqlalchemy.Column(sqlalchemy.Boolean)
    day3 = sqlalchemy.Column(sqlalchemy.Boolean)
    day4 = sqlalchemy.Column(sqlalchemy.Boolean)
    day5 = sqlalchemy.Column(sqlalchemy.Boolean)
    day6 = sqlalchemy.Column(sqlalchemy.Boolean)
    day7 = sqlalchemy.Column(sqlalchemy.Boolean)
    create_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                    default=datetime.date.today)

    user = orm.relation('User')