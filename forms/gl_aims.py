from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, BooleanField
from wtforms.validators import DataRequired


class AimForm(FlaskForm):
    name = StringField('Цель', validators=[DataRequired()])
    about = TextAreaField("Описание")
    is_finished = BooleanField("Законченость")
    finish_date = StringField('Дата окончания в формате ГГГГ.ММ.ДД', validators=[DataRequired()])
    submit = SubmitField('Добавить')


