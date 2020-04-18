from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, BooleanField
from wtforms.validators import DataRequired


class TaskForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired()])
    about = TextAreaField("Описание")
    is_finished = BooleanField("Законченость")
    submit = SubmitField('Добавить')

