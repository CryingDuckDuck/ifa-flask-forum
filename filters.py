from pytz import timezone

from app import app


@app.template_filter("datetime")
def format_datetime(value):
    return value.replace(tzinfo=timezone(app.config["TZ"])).strftime("%d-%m-%Y, %H:%M")