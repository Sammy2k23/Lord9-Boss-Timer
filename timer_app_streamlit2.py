import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
from streamlit_autorefresh import st_autorefresh

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

        today = datetime.now().date()
        parsed_time = datetime.strptime(f"{today} {last_time_str}", "%Y-%m-%d %I:%M %p")
        if parsed_time > datetime.now():
            parsed_time -= timedelta(days=1)
        self.last_time = parsed_time
        self.update_next()

    def update_next(self):
        self.next_time = self.last_time + timedelta(seconds=self.interval)
        while self.next_time < datetime.now():
            self.last_time = self.next_time
            self.next_time = self.last_time + timedelta(seconds=self.interval)

    def countdown(self):
        return self.next_time - datetime.now()

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

    def format_colored_countdown(self):
        seconds = self.countdown().total_seconds()
        if seconds < 60:
            color = "red"
        elif seconds < 300:
            color = "orange"
        else:
            color = "green"
        return f"<span style='color:{color}; font-weight:bold'>{self.format_countdown()}</span>"

# Streamlit app
st.set_page_config(page_title="Lord9 Boss Timer", layout="wide")
st.title("Lord9 Boss Timer")

# Refresh every 1 second
st_autorefresh(interval=1000, key="timer_refresh")

# Initialize timers
timers = [TimerEntry(*data) for data in timers_data]

# Update timers
for t in timers:
    t.update_next()

# Sort timers by countdown
timers_sorted = sorted(timers, key=lambda x: x.countdown())

# Build dataframe with row highlighting for next boss
rows = []
for i, t in enumerate(timers_sorted):
    if i == 0:  # Next boss
        style = "background-color:#D1FFD6"  # Light green
    else:
        style = ""
    rows.append(f"""
        <tr style="{style}">
            <td>{t.name}</td>
            <td>{t.interval_minutes}</td>
            <td>{t.last_time.strftime("%Y-%m-%d %I:%M %p")}</td>
            <td>{t.format_colored_countdown()}</td>
            <td>{t.next_time.strftime("%Y-%m-%d %I:%M %p")}</td>
        </tr>
    """)

html_table = f"""
<table border="1" cellpadding="5" cellspacing="0" style="border-collapse:collapse; width:100%">
    <thead>
        <tr style="background-color:#A6C8FF">
            <th>Name</th>
            <th>Interval (min)</th>
            <th>Last Time</th>
            <th>Countdown</th>
            <th>Next Time</th>
        </tr>
    </thead>
    <tbody>
        {''.join(rows)}
    </tbody>
</table>
"""

st.markdown(html_table, unsafe_allow_html=True)
