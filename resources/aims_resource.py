from flask import jsonify
from flask_restful import abort, Resource, reqparse

from data import db_session
from data.aims import Aim

# Парсер
parser = reqparse.RequestParser()
parser.add_argument('name', required=True)
parser.add_argument('about', required=True)
parser.add_argument('is_finished', required=True, type=bool)
parser.add_argument('author', required=True)
parser.add_argument('finish_date', required=True)


#  Проверка существования цели
def abort_if_aim_not_found(aim_id):
    session = db_session.create_session()
    news = session.query(Aim).get(aim_id)
    if not news:
        abort(404, message=f"Aim {aim_id} not found")


# Ресурс цели
class AimsResource(Resource):
    # Получение цели
    def get(self, aim_id):
        abort_if_aim_not_found(aim_id)
        session = db_session.create_session()
        aim = session.query(Aim).get(aim_id)
        return jsonify({'aims': aim.to_dict(
            only=('name', 'about', 'is_finished', 'author', 'finish_date'))})

    # Удаление цели
    def delete(self, aim_id):
        abort_if_aim_not_found(aim_id)
        session = db_session.create_session()
        aim = session.query(Aim).get(aim_id)
        session.delete(aim)
        session.commit()
        return jsonify({'success': 'OK'})


# Ресурс целей
class AimsListResource(Resource):
    # Получение целей
    def get(self):
        session = db_session.create_session()
        aims = session.query(Aim).all()
        return jsonify({'aims': [item.to_dict(
            only=('name', 'about', 'is_finished', 'finish_date')) for item in aims]})

    def post(self):
        # Создание цели
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
