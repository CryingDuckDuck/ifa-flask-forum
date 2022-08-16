from flask import Blueprint

admin_pages = Blueprint("admin_pages", __name__, template_folder="templates")


@admin_pages.route("/")
def index():
    return "admin"
