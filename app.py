import os
from flask import Flask, render_template
from blueprints.admin import admin_pages
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    from models.user import User

    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["SQLALCHEMY_DATABASE_URI"]
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

    with app.app_context():
        db.init_app(app)
        db.drop_all()
        db.create_all()

    app.register_blueprint(admin_pages, url_prefix="/admin")
    return app


app = create_app()


@app.route("/")
def index():
    return render_template("index.html")
