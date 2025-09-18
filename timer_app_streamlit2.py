# Repo-ready Streamlit app for Lord9 Boss Timer


# Folder structure:
# / (root)
# ├── streamlit_app.py <- main app
# └── requirements.txt


# ================= streamlit_app.py =================
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo # Python 3.9+
from streamlit_autorefresh import st_autorefresh


# Manila timezone
MANILA = ZoneInfo("Asia/Manila")


# Timer data
timers_data = [
("Venatus", 600, "12:31 PM"),
("Viorent", 600, "12:32 PM"),
("Ego", 1260, "04:32 PM"),
("Araneo", 1440, "04:33 PM"),
("Livera", 1440, "04:36 PM"),
("Undomiel", 1440, "04:42 PM"),
("Amentis", 1740, "04:42 PM"),
("General Aqulcus", 1740, "04:45 PM"),
("Baron Braudmore", 1920, "04:37 PM"),
("Gareth", 1920, "04:38 PM"),
("Shuliar", 2100, "04:49 PM"),
("Larba", 2100, "04:55 PM"),
("Catena", 2100, "05:12 PM"),
("Lady Dalia", 1080, "10:42 AM"),
("Titore", 2220, "04:58 PM"),
("Duplican", 2880, "04:36 PM"),
("Wannitas", 2880, "04:40 PM"),
("Metus", 2880, "04:46 PM"),
("Asta", 3720, "04:53 PM"),
("Ordo", 3720, "04:59 PM"),
("Secreta", 3720, "05:07 PM"),
("Supore", 3720, "05:15 PM"),
]


class TimerEntry:
def __init__(self, name, interval_minutes, last_time_str):
self.name = name
self.interval_minutes = interval_minutes
self.interval = interval_minutes * 60


today = datetime.now(tz=MANILA).date()
parsed_time = datetime.strptime(f"{today} {last_time_str}", "%Y-%m-%d %I:%M %p")
parsed_time = parsed_time.replace(tzinfo=MANILA)


self.last_time = parsed_time
self.next_time = self.last_time + timedelta(seconds=self.interval)


self.update_next()


def update_next(self):
now = datetime.now(tz=MANILA)
while self.next_time < now:
self.last_time = self.next_time
self.next_time = self.last_time + timedelta(seconds=self.interval)


def countdown(self):
return self.next_time - datetime.now(tz=MANILA)


def format_countdown(self):
td = self.countdown()
total_seconds = int(td.total_seconds())
if total_seconds < 0:
return "00:00:00"
days, rem = divmod(total_seconds, 86400)
hours, rem = divmod(rem, 3600)
minutes, seconds = divmod(rem, 60)
if days > 0:
return f"{days}d {hours:02}:{minutes:02}:{seconds:02}"
return f"{hours:02}:{minutes:02}:{seconds:02}"


def countdown_color(self):
seconds = self.countdown().total_seconds()
if seconds < 60:
return "red"
elif seconds < 300:
return "orange"
else:
return "green"


# Streamlit setup
st.set_page_config(page_title="Lord9 Boss Timer", layout="wide")
