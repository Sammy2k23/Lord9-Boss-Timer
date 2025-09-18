import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from streamlit_autorefresh import st_autorefresh

# Auto-refresh every 1 second
st_autorefresh(interval=1000, key="timer_refresh")

# Sample data (updated Last Times for Venatus, Viorent, Ego)
data = [
    {"Name": "Venatus", "Interval": 600, "Last Time": "12:31 PM"},
    {"Name": "Viorent", "Interval": 600, "Last Time": "12:32 PM"},
    {"Name": "Ego", "Interval": 1260, "Last Time": "01:32 PM"},
    {"Name": "General Aquleus", "Interval": 1740, "Last Time": "04:45 PM"},
    {"Name": "Baron Braudmore", "Interval": 1920, "Last Time": "04:37 PM"},
    {"Name": "Gareth", "Interval": 1920, "Last Time": "04:38 PM"},
    {"Name": "Shuliar", "Interval": 2100, "Last Time": "04:49 PM"},
    {"Name": "Larba", "Interval": 2100, "Last Time": "04:55 PM"},
    {"Name": "Catena", "Interval": 2100, "Last Time": "05:12 PM"},
    {"Name": "Lady Dalia", "Interval": 1080, "Last Time": "10:42 AM"},
    {"Name": "FRIOX", "Interval": 1440, "Last Time": "05:00 AM"},
    {"Name": "Titore", "Interval": 2220, "Last Time": "04:58 PM"},
    {"Name": "Duplican", "Interval": 2880, "Last Time": "04:36 PM"},
    {"Name": "Wannitas", "Interval": 2880, "Last Time": "04:40 PM"},
    {"Name": "Metus", "Interval": 2880, "Last Time": "04:46 PM"},
    {"Name": "Asta", "Interval": 3720, "Last Time": "04:53 PM"},
    {"Name": "Ordo", "Interval": 3720, "Last Time": "04:59 PM"},
    {"Name": "Secreta", "Interval": 3720, "Last Time": "05:07 PM"},
    {"Name": "Supore", "Interval": 3720, "Last Time": "05:15 PM"},
]

df = pd.DataFrame(data)

st.set_page_config(page_title="Timer App", layout="wide")
st.title("⏳ Lord 9 Boss Timers (Live Updating)")

placeholder = st.empty()

# Function to color countdown
def color_countdown(val):
    try:
        parts = val.split(":")
        minutes = int(parts[0]) * 60 + int(parts[1])
        seconds = minutes * 60 + int(parts[2]) if len(parts) == 3 else minutes
    except:
        return val

    if seconds < 300:  # <5 min
        return f"<span style='color:red; font-weight:bold;'>{val}</span>"
    elif seconds < 900:  # <15 min
        return f"<span style='color:orange;'>{val}</span>"
    else:
        return f"<span style='color:green;'>{val}</span>"

# Calculate countdowns and target times
now = datetime.now()
next_times = []
target_dates = []
countdowns = []
countdown_seconds = []
highlight_names = []
updated_last_times = []

for i, row in df.iterrows():
    # Parse last time as today’s datetime
    last_dt = datetime.strptime(row["Last Time"], "%I:%M %p").replace(
        year=now.year, month=now.month, day=now.day
    )
    interval = timedelta(minutes=row["Interval"])

    # Compute next time strictly based on interval
    next_time = last_dt + interval

    # If already passed, roll forward
    while next_time <= now:
        last_dt = next_time
        next_time = last_dt + interval

    # Countdown
    countdown = next_time - now
    countdown_str = str(countdown).split(".")[0]

    # Save updated values
    updated_last_times.append(last_dt.strftime("%I:%M %p"))
    next_times.append(next_time.strftime("%I:%M %p"))
    target_dates.append(next_time.strftime("%Y-%m-%d %I:%M:%S %p"))
    countdowns.append(color_countdown(countdown_str))
    countdown_seconds.append(countdown.total_seconds())

    # Highlight if <5min
    if countdown.total_seconds() < 300:
        highlight_names.append(f"<span style='color:red; font-weight:bold;'>{row['Name']}</span>")
    else:
        highlight_names.append(row["Name"])

# Update DataFrame
df["Name"] = highlight_names
df["Last Time"] = updated_last_times
df["Countdown"] = countdowns
df["Next Time"] = next_times
df["Target Date"] = target_dates

# 🔥 Apply -1 day shift for bosses below Ego
shift_from = "General Aquleus"
for i, row in df.iterrows():
    clean_name = row["Name"].replace("<span style='color:red; font-weight:bold;'>","").replace("</span>","")
    if clean_name == shift_from:
        shift_index = i
        break

for i in range(shift_index, len(df)):
    target_dt = datetime.strptime(df.at[i, "Target Date"], "%Y-%m-%d %I:%M:%S %p")
    target_dt -= timedelta(days=1)  # shift -1 day
    df.at[i, "Target Date"] = target_dt.strftime("%Y-%m-%d %I:%M:%S %p")

    # Recompute countdown
    countdown = target_dt - now
    countdown_str = str(countdown).split(".")[0]
    df.at[i, "Countdown"] = color_countdown(countdown_str)

# Sort bosses almost spawning to top
df["Seconds Remaining"] = countdown_seconds
df = df.sort_values("Seconds Remaining")
df = df.drop(columns=["Seconds Remaining"])

# Display table
with placeholder.container():
    st.markdown(df.to_html(escape=False, index=False), unsafe_allow_html=True)
