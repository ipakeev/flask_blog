import wtforms as wf
from flask_wtf import FlaskForm
from wtforms import validators
from wtforms.widgets import PasswordInput


class LoginForm(FlaskForm):
    username = wf.StringField(
        label="Логин",
        validators=[
            validators.DataRequired(),
            validators.Length(min=3),
        ])
    password = wf.StringField(
        label="Пароль",
        widget=PasswordInput(hide_value=False),
        validators=[
            validators.DataRequired(),
            validators.Length(min=3),
        ])
    remember = wf.BooleanField(label="Запомнить")


class RegistrationForm(FlaskForm):
    username = wf.StringField(
        label="Логин",
        validators=[
            validators.DataRequired(),
            validators.Length(min=3),
        ])
    password = wf.StringField(
        label="Пароль",
        widget=PasswordInput(hide_value=False),
        validators=[
            validators.DataRequired(),
            validators.Length(min=3),
            # validators.EqualTo("repeat_password", message="Пароли не совпадают"), # не работает!
        ])
    repeat_password = wf.StringField(
        label="Повторите пароль",
        widget=PasswordInput(hide_value=False),
        validators=[
            validators.DataRequired(),
            validators.Length(min=3),
        ])


class CommentForm(FlaskForm):
    text = wf.TextAreaField(
        label="Прокомментировать",
        validators=[
            validators.DataRequired(),
            validators.Length(min=1),
        ])
