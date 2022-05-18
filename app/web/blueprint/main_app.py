from typing import Optional

from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.exceptions import NotFound

from app.database import accessor
from app.database.models import Post, User, Comment
from app.web.forms import LoginForm, RegistrationForm, CommentForm

main_app = Blueprint("main_app", __name__)


@main_app.route("/", endpoint="index")
def main_page():
    user = current_user if current_user.is_authenticated else None
    posts: list[Post] = Post.query.all()
    return render_template(
        "main.html",
        title="Умный дом",
        user=user,
        posts=posts,
    )


@main_app.route("/posts/<int:post_id>/", methods=["GET", "POST"], endpoint="posts")
def post_by_id(post_id: int):
    user = current_user if current_user.is_authenticated else None
    post: Optional[Post] = Post.query.filter_by(id=post_id).first()
    if post is None:
        raise NotFound(f"Post with id={post_id} is not existed.")

    form = CommentForm()
    if request.method == "POST":
        if user is None:
            flash("Для оставления комментариев необходимо авторизоваться!")
        else:
            if form.validate_on_submit():
                accessor.add_comment(user.id, post_id, form.text.data)
                return redirect(url_for("main_app.posts", post_id=post_id) + "#comments")

    author: User = User.query.filter_by(id=post.user_id).one()
    if post.comments:
        users: dict[int, User] = {i.id: i for i in User.query.all()}
        for comment in post.comments:
            comment.username = users[comment.user_id].username

    return render_template(
        "post.html",
        title=post.title,
        user=user,
        post=post,
        author=author,
        form=form,
        comments=post.comments,
    )


@main_app.route("/contacts/", endpoint="contacts")
def contacts():
    user = current_user if current_user.is_authenticated else None
    return render_template(
        "contacts.html",
        title="Контакты",
        user=user,
    )


@main_app.route("/login/", methods=["GET", "POST"], endpoint="login")
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main_app.index"))

    form = LoginForm()
    if request.method == "POST":
        if form.validate_on_submit():
            user: Optional[User] = User.query.filter_by(username=form.username.data).first()
            if user is not None and user.is_correct_password(form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for("main_app.index"))
            else:
                flash("Неправильный логин или пароль!", category="error")
        else:
            flash("Неизвестная ошибка!", category="error")

    return render_template("login.html", title="Войти", form=form)


@main_app.route("/registration/", methods=["GET", "POST"], endpoint="registration")
def registration():
    if current_user.is_authenticated:
        return redirect(url_for("main_app.index"))

    form = RegistrationForm()
    if request.method == "POST":
        if form.validate_on_submit():
            if User.query.filter_by(username=form.username.data).first():
                flash("Пользователь с данным ником уже существует!", category="error")
            elif form.password.data != form.repeat_password.data:
                flash("Пароли не совпадают!", category="error")
            else:
                user = accessor.add_user(form.username.data, form.password.data, is_admin=False)
                login_user(user)
                return redirect(url_for("main_app.index"))
        else:
            flash("Неизвестная ошибка!", category="error")

    return render_template("registration.html", title="Зарегистрироваться", form=form)


@main_app.route("/logout/", endpoint="logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main_app.index"))


@main_app.route("/user/", endpoint="user")
@login_required
def user_page():
    user: User = current_user
    posts: list[Post] = Post.query.filter_by(user_id=user.id).all()
    n_comments: int = Comment.query.filter_by(user_id=user.id).count()
    return render_template(
        "user.html",
        title="Личный кабинет",
        user=user,
        posts=posts,
        n_comments=n_comments,
    )
