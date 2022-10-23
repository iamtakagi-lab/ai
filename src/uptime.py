import datetime
import time
from constants import STARTED

def get_uptime():
    delta = datetime.datetime.utcnow() - STARTED
    hours, remainder = divmod(int(delta.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    days, hours = divmod(hours, 24)
    uptime = ("{} days, {:0=2}:{:0=2}:{:0=2}".format(days, hours, minutes, seconds))
    return uptime

def get_uptime_fmt():
    return "⌚ 稼働時間: {}".format(get_uptime())
