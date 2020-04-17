from flask import jsonify
from flask_restful import abort, Resource, reqparse

from data import db_session
from data.tasks import Task
from data.users import User

parser = reqparse.RequestParser()
parser.add_argument('name', required=True)
parser.add_argument('about', required=True)
parser.add_argument('is_finished', required=True, type=bool)
parser.add_argument('author', required=True)


def abort_if_task_not_found(task_id):
    session = db_session.create_session()
    news = session.query(Task).get(task_id)
    if not news:
        abort(404, message=f"Task {task_id} not found")


class TasksResource(Resource):
    def get(self, task_id):
        abort_if_task_not_found(task_id)
        session = db_session.create_session()
        user = session.query(Task).get(task_id)
        return jsonify({'users': user.to_dict(
            only=('name', 'about', 'is_finished', 'author'))})

    def delete(self, task_id):
        abort_if_task_not_found(task_id)
        session = db_session.create_session()
        news = session.query(Task).get(task_id)
        session.delete(news)
        session.commit()
        return jsonify({'success': 'OK'})


class TasksListResource(Resource):
    def get(self):
        session = db_session.create_session()
        news = session.query(Task).all()
        return jsonify({'tasks': [item.to_dict(
            only=('name', 'about', 'is_finished')) for item in news]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        user = Task(
            name=args['name'],
            about=args['about'],
            is_finished=args['is_finished'],
            author=args['author']
        )
        session.add(user)
        session.commit()
        return jsonify({'success': 'OK'})
