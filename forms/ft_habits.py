from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, BooleanField
from wtforms.validators import DataRequired


# Класс формы создания привычки
class HabitForm(FlaskForm):
    name = StringField('Привычка', validators=[DataRequired()])
    submit = SubmitField('Добавить')


