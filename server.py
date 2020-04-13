import os

import requests
from flask import Flask, render_template
from flask_login import LoginManager
from flask_restful import Api
from werkzeug.utils import redirect

from data import db_session
from data.users import User
from forms.reg_user import RegisterForm
from resources import users_resource

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)
PORT = int(os.environ.get("PORT", 5000))

api.add_resource(users_resource.UsersResource, '/api/users/<int:user_id>')
api.add_resource(users_resource.UsersListResource, '/api/users')


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        res = requests.post(f'http://localhost:{PORT}/api/users', json={
            'email': form.email.data,
            'name': form.name.data,
            'surname': form.surname.data,
            'age': form.age.data,
            'about': '',
            'password': form.password.data
        }).json()
        if 'message' in res:
            return render_template('register.html', title='Регистрация', form=form,
                                   message=res['message'])
        return redirect('/')
    return render_template('register.html', title='Регистрация', form=form)


def main():
    db_session.global_init("db/data.sqlite")
    app.run(host='127.0.0.1', port=PORT)


if __name__ == '__main__':
    main()
