from flask import jsonify
from flask_restful import abort, Resource, reqparse

from data import db_session
from data.users import User

# Парсер
parser = reqparse.RequestParser()
parser.add_argument('email', required=True)
parser.add_argument('name', required=True)
parser.add_argument('surname', required=True)
parser.add_argument('age', required=True, type=int)
parser.add_argument('about', required=True)
parser.add_argument('password', required=True)


# Проверка существования аккаунта
def abort_if_user_not_found(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        abort(404, message=f"User {user_id} not found")


# Проверка корректности возраста
def check_age(age):
    if age < 0:
        abort(404, message='Возраст отрицателен!')


# Ресурс пользователя
class UsersResource(Resource):
    # Получение данных пользователя
    def get(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        return jsonify({'user': user.to_dict(
            only=('email', 'name', 'surname', 'age', 'about'))})

    # Удаление аккаунта
    def delete(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        session.delete(user)
        session.commit()
        return jsonify({'success': 'OK'})


# Ресурс пользователей
class UsersListResource(Resource):
    # Получение ланных пользователей
    def get(self):
        session = db_session.create_session()
        users = session.query(User).all()
        return jsonify({'users': [item.to_dict(
            only=('email', 'name', 'surname', 'age', 'about')) for item in users]})

    # Создание аккаунта
    def post(self):
        args = parser.parse_args()
        check_age(args['age'])
        session = db_session.create_session()
        user = User(
            surname=args['surname'],
            name=args['name'],
            age=args['age'],
            about=args['about'],
            email=args['email']
        )
        user.set_password(args['password'])
        session.add(user)
        session.commit()
        return jsonify({'success': 'OK'})
