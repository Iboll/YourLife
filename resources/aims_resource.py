from flask import jsonify
from flask_restful import abort, Resource, reqparse

from data import db_session
from data.aims import Aim

parser = reqparse.RequestParser()
parser.add_argument('name', required=True)
parser.add_argument('about', required=True)
parser.add_argument('is_finished', required=True, type=bool)
parser.add_argument('author', required=True)
parser.add_argument('finish_date', required=True)


def abort_if_task_not_found(aim_id):
    session = db_session.create_session()
    news = session.query(Aim).get(aim_id)
    if not news:
        abort(404, message=f"Aim {aim_id} not found")


class AimsResource(Resource):
    def get(self, aim_id):
        abort_if_task_not_found(aim_id)
        session = db_session.create_session()
        user = session.query(Aim).get(aim_id)
        return jsonify({'users': user.to_dict(
            only=('name', 'about', 'is_finished', 'author', 'finish_date'))})

    def delete(self, aim_id):
        abort_if_task_not_found(aim_id)
        session = db_session.create_session()
        news = session.query(Aim).get(aim_id)
        session.delete(news)
        session.commit()
        return jsonify({'success': 'OK'})


class AimsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        news = session.query(Aim).all()
        return jsonify({'tasks': [item.to_dict(
            only=('name', 'about', 'is_finished', 'finish_date')) for item in news]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        aim = Aim(
            name=args['name'],
            about=args['about'],
            is_finished=args['is_finished'],
            author=args['author'],
            finish_date=args['finish_date']
        )
        session.add(aim)
        session.commit()
        return jsonify({'success': 'OK'})
