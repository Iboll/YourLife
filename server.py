import datetime
import os

import requests
from flask import Flask, render_template
from flask_login import LoginManager, login_user, login_required, logout_user
from flask_restful import Api
from werkzeug.utils import redirect

from data import db_session
from data.tasks import Task
from data.users import User
from forms.day_tasks import TaskForm
from forms.log_user import LoginForm
from forms.reg_user import RegisterForm
from resources import users_resource, tasks_resource

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)
PORT = int(os.environ.get("PORT", 5000))

api.add_resource(users_resource.UsersResource, '/api/users/<int:user_id>')
api.add_resource(users_resource.UsersListResource, '/api/users')
api.add_resource(tasks_resource.TasksResource, '/api/tasks/<int:task_id>')
api.add_resource(tasks_resource.TasksListResource, '/api/tasks')


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route("/")
def index():
    return render_template('base.html')


def update_tasks():
    session = db_session.create_session()
    for task in session.query(Task):
        if str(task.create_date) != str(datetime.date.today()) + ' 00:00:00':
            task_id = task.id
            requests.delete(f'http://localhost:{PORT}/api/tasks/{task_id}').json()


@app.route('/tasks')
def tasks():
    update_tasks()
    session = db_session.create_session()
    task = session.query(Task)
    return render_template("tasks.html", news=task)


@app.route('/add_task', methods=['GET', 'POST'])
def add_task():
    form = TaskForm()
    if form.validate_on_submit():
        res = requests.post(f'http://localhost:{PORT}/api/tasks', json={
            'name': form.name.data,
            'about': form.about.data,
            'is_finished': form.is_finished.data,
            'author': form.author.data
        }).json()
        if 'message' in res:
            return render_template('add_task.html', title='Задачи на день', form=form,
                                   message=res['message'])
        return redirect('/tasks')
    return render_template('add_task.html', title='Задачи на день', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
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


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/login")


def main():
    db_session.global_init("db/data.sqlite")
    app.run(host='127.0.0.1', port=PORT)


if __name__ == '__main__':
    main()
