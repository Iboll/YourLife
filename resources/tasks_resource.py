from flask import jsonify
from flask_restful import abort, Resource, reqparse

from data import db_session
from data.tasks import Task

# Парсер
parser = reqparse.RequestParser()
parser.add_argument('name', required=True)
parser.add_argument('about', required=True)
parser.add_argument('is_finished', required=True, type=bool)
parser.add_argument('author', required=True)


# Проверка существования задачи
def abort_if_task_not_found(task_id):
    session = db_session.create_session()
    task = session.query(Task).get(task_id)
    if not task:
        abort(404, message=f"Task {task_id} not found")


# Ресурс задачи
class TasksResource(Resource):
    # Получение задачи
    def get(self, task_id):
        abort_if_task_not_found(task_id)
        session = db_session.create_session()
        task = session.query(Task).get(task_id)
        return jsonify({'task': task.to_dict(
            only=('name', 'about', 'is_finished', 'author'))})

    # Удаление задачи
    def delete(self, task_id):
        abort_if_task_not_found(task_id)
        session = db_session.create_session()
        task = session.query(Task).get(task_id)
        session.delete(task)
        session.commit()
        return jsonify({'success': 'OK'})


# Ресурс задач
class TasksListResource(Resource):
    # Получение задач
    def get(self):
        session = db_session.create_session()
        tasks = session.query(Task).all()
        return jsonify({'tasks': [item.to_dict(
            only=('name', 'about', 'is_finished')) for item in tasks]})

    # Создание задачи
    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        task = Task(
            name=args['name'],
            about=args['about'],
            is_finished=args['is_finished'],
            author=args['author']
        )
        session.add(task)
        session.commit()
        return jsonify({'success': 'OK'})
