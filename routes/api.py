from flask import jsonify
from sqlalchemy.orm import joinedload

from app import app
from models import Post


def comment_to_dict(comment):
    return {
        "id": comment.id,
        "text": comment.text,
        "user": comment.user.username,
        "posted_at": comment.posted_at,
    }


def post_to_dict(post):
    return {
        "id": post.id,
        "title": post.title,
        "text": post.text,
        "posted_at": post.posted_at,
        "user": post.user.username,
        "comment_count": post.comment_count,
        "comments": list(map(lambda c: comment_to_dict(c), post.comments))
    }


@app.route("/api/posts")
def all_posts_api():
    posts = Post.query.options(
        joinedload("user"),
        joinedload("comments"),
        joinedload("comments.user")
    ).order_by(Post.posted_at.desc()).all()
    return jsonify(list(map(lambda p: post_to_dict(p), posts)))
