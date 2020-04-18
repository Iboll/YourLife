from flask import jsonify
from flask_restful import abort, Resource, reqparse

from data import db_session
from data.habits import Habit

parser = reqparse.RequestParser()
parser.add_argument('name', required=True)
parser.add_argument('day1', required=True, type=bool)
parser.add_argument('day2', required=True, type=bool)
parser.add_argument('day3', required=True, type=bool)
parser.add_argument('day4', required=True, type=bool)
parser.add_argument('day5', required=True, type=bool)
parser.add_argument('day6', required=True, type=bool)
parser.add_argument('day7', required=True, type=bool)
parser.add_argument('author', required=True)


def abort_if_habit_not_found(habit_id):
    session = db_session.create_session()
    news = session.query(Habit).get(habit_id)
    if not news:
        abort(404, message=f"Task {habit_id} not found")


class HabitsResource(Resource):
    def get(self, habit_id):
        abort_if_habit_not_found(habit_id)
        session = db_session.create_session()
        user = session.query(Habit).get(habit_id)
        return jsonify({'users': user.to_dict(
            only=('name', 'day1', 'day2', 'day3', 'day4', 'day5', 'day6', 'day7', 'author'))})

    def delete(self, habit_id):
        abort_if_habit_not_found(habit_id)
        session = db_session.create_session()
        habit = session.query(Habit).get(habit_id)
        session.delete(habit)
        session.commit()
        return jsonify({'success': 'OK'})


class HabitsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        news = session.query(Habit).all()
        return jsonify({'tasks': [item.to_dict(
            only=('name', 'day1', 'day2', 'day3', 'day4', 'day5', 'day6', 'day7', 'author')) for item in news]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        habit = Habit(
            name=args['name'],
            author=args['author'],
            day1=args['day1'],
            day2=args['day2'],
            day3=args['day3'],
            day4=args['day4'],
            day5=args['day5'],
            day6=args['day6'],
            day7=args['day7']
        )
        session.add(habit)
        session.commit()
        return jsonify({'success': 'OK'})