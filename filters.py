import pytz
from pytz import timezone

from app import app

tz = timezone(app.config["TZ"])


@app.template_filter("datetime")
def format_datetime(value):
    return value.replace(tzinfo=pytz.utc).astimezone(tz).strftime("%d-%m-%Y, %H:%M")
