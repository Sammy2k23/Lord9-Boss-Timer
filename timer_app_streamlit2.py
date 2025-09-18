import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo  # Python 3.9+
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

# TimerEntry class
class TimerEntry:
    def __init__(self, name, interval_minutes, last_time_str):
        self.name = name
        self.interval_minutes = interval_minutes
        self.interval = interval_minutes * 60

        today = datetime.now(tz=MANILA).date()
        parsed_time = datetime.strptime(f"{today} {last_time_str}", "%Y-%m-%d %I:%M %p")
        parsed_time = parsed_time.replace(tzinfo=MANILA)
        if parsed_time > datetime.now(tz=MANILA):
            parsed_time -= timedelta(days=1)

        self.last_time = parsed_time
        self.next_time = self.last_time + timedelta(seconds=self.interval)

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
        """Return color based on remaining time"""
        seconds = self.countdown().total_seconds()
        if seconds < 60:
            return "red"
        elif seconds < 300:
            return "orange"
        else:
            return "green"

# Streamlit setup
st.set_page_config(page_title="Lord9 Boss Timer", layout="wide")
st.title("🛡️ Lord9 Boss Timer (Manila Time GMT+8)")
st_autorefresh(interval=1000, key="refresh")

# Initialize timers
timers = [TimerEntry(*data) for data in timers_data]

# Update next_time for all timers
for t in timers:
    t.update_next()

# Sort by closest countdown
timers_sorted = sorted(timers, key=lambda x: x.countdown())

# Build DataFrame
df = pd.DataFrame({
    "Name": [t.name for t in timers_sorted],
    "Interval (min)": [t.interval_minutes for t in timers_sorted],
    "Last Time": [t.last_time.strftime("%Y-%m-%d %I:%M %p") for t in timers_sorted],
    "Countdown": [t.format_countdown() for t in timers_sorted],
    "Next Time": [t.next_time.strftime("%Y-%m-%d %I:%M %p") for t in timers_sorted],
    "Color": [t.countdown_color() for t in timers_sorted],
})

# Apply countdown colors
def color_countdown(s):
    return [f"color: {c}" for c in df["Color"]]

# Display table
st.dataframe(df.drop(columns=["Color"]).style.apply(color_countdown, subset=["Countdown"], axis=0))
