from flask_wtf import FlaskForm
from wtforms import SubmitField, BooleanField, PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


# Класс формы для авторизации пользователя
class LoginForm(FlaskForm):
    email = EmailField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')