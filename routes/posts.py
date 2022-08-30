from flask import render_template, redirect, url_for, abort
from flask_login import current_user, login_required
from flask_wtf import FlaskForm
from sqlalchemy.orm import joinedload
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired, Length
from wtforms.widgets import TextArea

from app import app, db
from models import Post, Comment


class PostForm(FlaskForm):
    title = StringField('Titel',
                        validators=[InputRequired("Bitte geben Sie einen Titel an"), Length(1, 64)])
    text = StringField('Text',
                       validators=[InputRequired("Bitte geben Sie einen Text an"), Length(1, 255)], widget=TextArea())

    submit = SubmitField("Beitrag erstellen")

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)


class CommentForm(FlaskForm):
    text = StringField('Text',
                       validators=[InputRequired("Bitte geben Sie einen Text an"), Length(1, 255)], widget=TextArea())

    submit = SubmitField("Kommentar erstellen")

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)


@app.route("/")
def all_posts():
    posts = Post.query.options(joinedload("user")).order_by(Post.posted_at.desc()).all()
    return render_template("posts/index.html", posts=posts)


@app.route("/posts/<post_id>", methods=["GET", "POST"])
def post_by_id(post_id):
    post = Post.query.options(
        joinedload("user"),
        joinedload("comments"),
        joinedload("comments.user")
    ).get(post_id)

    if post is None:
        return abort(404)

    form = CommentForm()

    if form.validate_on_submit():
        text = form.text.data
        comment = Comment(text=text, user_id=current_user.id, post_id=post.id)
        db.session.add(comment)
        db.session.commit()
        form.text.data = ""

    return render_template("posts/id.html", post=post, form=form)


@app.route("/posts/create", methods=["GET", "POST"])
@login_required
def create_post():
    form = PostForm()

    if form.validate_on_submit():
        title = form.title.data
        text = form.text.data
        user_id = current_user.id
        post = Post(title=title, text=text, user_id=user_id)
        db.session.add(post)
        db.session.commit()
        return redirect("/")

    return render_template(
        "posts/form.html",
        form=form,
        title="Neuen Beitrag erstellen",
        action=url_for("create_post")
    )


@app.route("/posts/<post_id>/edit", methods=["GET", "POST"])
@login_required
def edit_post(post_id):
    post = Post.query.get(post_id)

    if post is None:
        return abort(404)

    if post.user_id != current_user.id and not current_user.is_admin:
        return abort(401)

    form = PostForm(obj=post)
    form.submit.label.text = "Beitrag editieren"

    if form.validate_on_submit():
        post.title = form.title.data
        post.text = form.text.data
        db.session.commit()
        return redirect("/")

    return render_template(
        "posts/form.html",
        form=form,
        title="Beitrag editieren",
        action=url_for("edit_post", post_id=post_id),
        post=post,
        page="edit"
    )


@app.route("/posts/<post_id>/delete", methods=["POST"])
@login_required
def delete_post(post_id):
    post = Post.query.get(post_id)

    if post is None:
        return abort(404)

    if post.user_id != current_user.id and not current_user.is_admin:
        return abort(401)

    db.session.delete(post)
    db.session.commit()

    return redirect("/")


@app.route("/comments/<comment_id>/delete", methods=["POST"])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get(comment_id)

    if comment is None:
        return abort(404)

    if comment.user_id != current_user.id and not current_user.is_admin:
        return abort(401)

    post_id = comment.post_id

    db.session.delete(comment)
    db.session.commit()

    return redirect(url_for("post_by_id", post_id=post_id))
