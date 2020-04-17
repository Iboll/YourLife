from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, BooleanField
from wtforms.validators import DataRequired


class AimForm(FlaskForm):
    name = StringField('Цель', validators=[DataRequired()])
    about = TextAreaField("Описание")
    is_finished = BooleanField("Законченость")
    author = StringField('Автор задачи (ваш логин)', validators=[DataRequired()])
    finish_date = StringField('Дата окончания', validators=[DataRequired()])
    submit = SubmitField('Добавить')

