from flask import Flask
from flask_login import LoginManager
from flask_restful import Api

from data import db_session
from data.users import User

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


def main():
    db_session.global_init("db/data.sqlite")
    app.run()


if __name__ == '__main__':
    main()