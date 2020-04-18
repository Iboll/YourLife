from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


class BlogForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired()])
    about = TextAreaField("Описание")
    submit = SubmitField('Добавить')