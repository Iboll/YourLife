import datetime
import os

import requests
from flask import Flask, render_template
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_restful import Api
from werkzeug.utils import redirect

from data import db_session
from data.aims import Aim
from data.habits import Habit
from data.tasks import Task
from data.users import User
from forms.ft_habits import HabitForm
from forms.gl_aims import AimForm
from forms.day_tasks import TaskForm
from forms.log_user import LoginForm
from forms.reg_user import RegisterForm
from resources import users_resource, tasks_resource, aims_resource, habits_resource

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
api.add_resource(aims_resource.AimsResource, '/api/aims/<int:aim_id>')
api.add_resource(aims_resource.AimsListResource, '/api/aims')
api.add_resource(habits_resource.HabitsResource, '/api/habits/<int:habit_id>')
api.add_resource(habits_resource.HabitsListResource, '/api/habits')


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


def update_aims():
    session = db_session.create_session()
    for elem in session.query(Aim):
        if '.'.join(str(datetime.date.today()).split('-')) == str(elem.finish_date):
            aim_id = elem.id
            requests.delete(f'http://localhost:{PORT}/api/aims/{aim_id}').json()


def update_habits():
    session = db_session.create_session()
    date_now = datetime.datetime.now()
    for elem in session.query(Habit):
        date_2 = elem.create_date
        difference = date_2 - date_now
        if difference.days == -8:
            habit_id = elem.id
            requests.delete(f'http://localhost:{PORT}/api/habits/{habit_id}').json()


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        res = requests.post(f'http://localhost:{PORT}/api/users', json={
            'email': form.email.data,
            'name': form.name.data,
            'surname': form.surname.data,
            'age': form.age.data,
            'about': form.about.data,
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
            'author': current_user.email
        }).json()
        if 'message' in res:
            return render_template('add_task.html', title='Задачи на день', form=form,
                                   message=res['message'])
        return redirect('/tasks')
    return render_template('add_task.html', title='Задачи на день', form=form)


@app.route('/edit_task/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_task(id):
    form = TaskForm()
    if form.validate_on_submit():
        res = requests.post(f'http://localhost:{PORT}/api/tasks', json={
            'name': form.name.data,
            'about': form.about.data,
            'is_finished': form.is_finished.data,
            'author': current_user.email
        }).json()
        requests.delete(f'http://localhost:{PORT}/api/tasks/{id}').json()
        if 'message' in res:
            return render_template('edit_task.html', title='Редактирование задачи', form=form,
                                   message=res['message'])
        return redirect('/tasks')
    return render_template('edit_task.html', title='Задачи на день', form=form)


@app.route('/task_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def task_delete(id):
    requests.delete(f'http://localhost:{PORT}/api/tasks/{id}').json()
    return redirect('/tasks')


@app.route('/change_task/<int:id>')
def change_task(id):
    session = db_session.create_session()
    news = session.query(Task).filter(Task.id == id).first()
    if news.is_finished is False:
        news.is_finished = True
    elif news.is_finished is True:
        news.is_finished = False
    session.commit()
    return redirect('/tasks')


@app.route('/aims')
def aims():
    update_aims()
    session = db_session.create_session()
    aims = session.query(Aim)
    return render_template("aims.html", news=aims)


@app.route('/add_aim', methods=['GET', 'POST'])
def add_aim():
    form = AimForm()
    if form.validate_on_submit():
        res = requests.post(f'http://localhost:{PORT}/api/aims', json={
            'name': form.name.data,
            'about': form.about.data,
            'is_finished': form.is_finished.data,
            'author': current_user.email,
            'finish_date': form.finish_date.data
        }).json()
        if 'message' in res:
            return render_template('add_aim.html', title='Задачи на день', form=form,
                                   message=res['message'])
        return redirect('/aims')
    return render_template('add_aim.html', title='Задачи на день', form=form)


@app.route('/edit_aim/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_aim(id):
    form = AimForm()
    if form.validate_on_submit():
        res = requests.post(f'http://localhost:{PORT}/api/aims', json={
            'name': form.name.data,
            'about': form.about.data,
            'is_finished': form.is_finished.data,
            'author': current_user.email,
            'finish_date': form.finish_date.data
        }).json()
        requests.delete(f'http://localhost:{PORT}/api/aims/{id}').json()
        if 'message' in res:
            return render_template('aim_edit.html', title='Редактирование цели', form=form,
                                   message=res['message'])
        return redirect('/aims')
    return render_template('aim_edit.html', title='Задачи на день', form=form)


@app.route('/aim_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def aim_delete(id):
    requests.delete(f'http://localhost:{PORT}/api/aims/{id}').json()
    return redirect('/aims')


@app.route('/change_aim/<int:id>')
def change_aim(id):
    session = db_session.create_session()
    news = session.query(Aim).filter(Aim.id == id).first()
    if news.is_finished is False:
        news.is_finished = True
    elif news.is_finished is True:
        news.is_finished = False
    session.commit()
    return redirect('/aims')


@app.route('/habits')
def habits():
    update_habits()
    session = db_session.create_session()
    task = session.query(Habit)
    return render_template("habits.html", news=task)


@app.route('/add_habit', methods=['GET', 'POST'])
def add_habit():
    form = HabitForm()
    if form.validate_on_submit():
        res = requests.post(f'http://localhost:{PORT}/api/habits', json={
            'name': form.name.data,
            'day1': False,
            'day2': False,
            'day3': False,
            'day4': False,
            'day5': False,
            'day6': False,
            'day7': False,
            'author': current_user.email
        }).json()
        if 'message' in res:
            return render_template('add_habit.html', title='Задачи на день', form=form,
                                   message=res['message'])
        return redirect('/habits')
    return render_template('add_habit.html', title='Задачи на день', form=form)


@app.route('/edit_habit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_habit(id):
    form = HabitForm()
    if form.validate_on_submit():
        res = requests.post(f'http://localhost:{PORT}/api/habits', json={
            'name': form.name.data,
            'day1': False,
            'day2': False,
            'day3': False,
            'day4': False,
            'day5': False,
            'day6': False,
            'day7': False,
            'author': current_user.email
        }).json()
        requests.delete(f'http://localhost:{PORT}/api/habits/{id}').json()
        if 'message' in res:
            return render_template('edit_habit.html', title='Редактирование задачи', form=form,
                                   message=res['message'])
        return redirect('/habits')
    return render_template('edit_habit.html', title='Задачи на день', form=form)


@app.route('/habit_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def habit_delete(id):
    requests.delete(f'http://localhost:{PORT}/api/habits/{id}').json()
    return redirect('/habits')


@app.route('/change_habit/<int:idd>/<int:id>')
def change_habit(idd, id):
    session = db_session.create_session()
    news = session.query(Habit).filter(Habit.id == id).first()
    if idd == 1:
        if news.day1 is False:
            news.day1 = True
        elif news.day1 is True:
            news.day1 = False
    if idd == 2:
        if news.day2 is False:
            news.day2 = True
        elif news.day2 is True:
            news.day2 = False
    if idd == 3:
        if news.day3 is False:
            news.day3 = True
        elif news.day3 is True:
            news.day3 = False
    if idd == 4:
        if news.day4 is False:
            news.day4 = True
        elif news.day4 is True:
            news.day4 = False
    if idd == 5:
        if news.day5 is False:
            news.day5 = True
        elif news.day5 is True:
            news.day5 = False
    if idd == 6:
        if news.day6 is False:
            news.day6 = True
        elif news.day6 is True:
            news.day6 = False
    if idd == 7:
        if news.day7 is False:
            news.day7 = True
        elif news.day7 is True:
            news.day7 = False
    session.commit()
    return redirect('/habits')


def main():
    db_session.global_init("db/data.sqlite")
    app.run(host='127.0.0.1', port=PORT)


if __name__ == '__main__':
    main()
