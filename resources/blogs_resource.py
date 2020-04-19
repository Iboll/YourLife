from flask import jsonify
from flask_restful import abort, Resource, reqparse

from data import db_session
from data.blogs import Blog

# Парсер
parser = reqparse.RequestParser()
parser.add_argument('name', required=True)
parser.add_argument('about', required=True)
parser.add_argument('author', required=True)


# Проверка существования записи
def abort_if_blog_not_found(blog_id):
    session = db_session.create_session()
    blog = session.query(Blog).get(blog_id)
    if not blog:
        abort(404, message=f"Blog {blog_id} not found")


# Ресурс записи
class BlogsResource(Resource):
    # Получение записи
    def get(self, blog_id):
        abort_if_blog_not_found(blog_id)
        session = db_session.create_session()
        blog = session.query(Blog).get(blog_id)
        return jsonify({'blog': blog.to_dict(
            only=('name', 'about', 'author', 'create_date'))})

    # Удаление записи
    def delete(self, blog_id):
        abort_if_blog_not_found(blog_id)
        session = db_session.create_session()
        blog = session.query(Blog).get(blog_id)
        session.delete(blog)
        session.commit()
        return jsonify({'success': 'OK'})


# Ресурс записей
class BlogsListResource(Resource):
    # Получение записей
    def get(self):
        session = db_session.create_session()
        blogs = session.query(Blog).all()
        return jsonify({'blogs': [item.to_dict(
            only=('name', 'about', 'author', 'create_date')) for item in blogs]})

    # Создание записи
    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        blog = Blog(
            name=args['name'],
            about=args['about'],
            author=args['author']
        )
        session.add(blog)
        session.commit()
        return jsonify({'success': 'OK'})