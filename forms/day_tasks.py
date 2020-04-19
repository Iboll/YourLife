from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, BooleanField
from wtforms.validators import DataRequired


#  Класс формы создания задачи
class TaskForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired()])
    about = TextAreaField("Описание")
    is_finished = BooleanField("Законченность")
    submit = SubmitField('Добавить')

