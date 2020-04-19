from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, BooleanField
from wtforms.validators import DataRequired


# Класс формы создания цели
class AimForm(FlaskForm):
    name = StringField('Цель', validators=[DataRequired()])
    about = TextAreaField("Описание")
    is_finished = BooleanField("Законченость")
    finish_date = StringField('Дата окончания. Обязательно в формате ГГГГ.ММ.ДД', validators=[DataRequired()])
    submit = SubmitField('Добавить')


