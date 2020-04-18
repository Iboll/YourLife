from flask import jsonify
from flask_restful import abort, Resource, reqparse

from data import db_session
from data.blogs import Blog

parser = reqparse.RequestParser()
parser.add_argument('name', required=True)
parser.add_argument('about', required=True)
parser.add_argument('author', required=True)


def abort_if_blog_not_found(blog_id):
    session = db_session.create_session()
    news = session.query(Blog).get(blog_id)
    if not news:
        abort(404, message=f"Task {blog_id} not found")


class BlogsResource(Resource):
    def get(self, blog_id):
        abort_if_blog_not_found(blog_id)
        session = db_session.create_session()
        user = session.query(Blog).get(blog_id)
        return jsonify({'users': user.to_dict(
            only=('name', 'about', 'is_finished', 'author'))})

    def delete(self, blog_id):
        abort_if_blog_not_found(blog_id)
        session = db_session.create_session()
        news = session.query(Blog).get(blog_id)
        session.delete(news)
        session.commit()
        return jsonify({'success': 'OK'})


class BlogsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        news = session.query(Blog).all()
        return jsonify({'blogs': [item.to_dict(
            only=('name', 'about', 'is_finished')) for item in news]})

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