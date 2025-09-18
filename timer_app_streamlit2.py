import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# ========================
# Boss Data
# ========================
boss_data = [
    {"name": "Venatus", "interval": 600, "last_time": "02:31 AM"},
    {"name": "Viorent", "interval": 600, "last_time": "02:32 AM"},
    {"name": "Ego", "interval": 1260, "last_time": "04:32 PM"},
    {"name": "Araneo", "interval": 1440, "last_time": "04:33 PM"},
    {"name": "Livera", "interval": 1440, "last_time": "04:36 PM"},
    {"name": "Undomiel", "interval": 1440, "last_time": "04:42 PM"},
    {"name": "Amentis", "interval": 1740, "last_time": "04:42 PM"},
    {"name": "General Aquleus", "interval": 1740, "last_time": "04:45 PM"},
    {"name": "Baron Braudmore", "interval": 1920, "last_time": "04:37 PM"},
    {"name": "Gareth", "interval": 1920, "last_time": "04:38 PM"},
    {"name": "Shuliar", "interval": 2100, "last_time": "04:49 PM"},
    {"name": "Larba", "interval": 2100, "last_time": "04:55 PM"},
    {"name": "Catena", "interval": 2100, "last_time": "05:12 PM"},
    {"name": "Lady Dalia", "interval": 1080, "last_time": "10:42 AM"},
    {"name": "Titore", "interval": 2220, "last_time": "04:58 PM"},
    {"name": "Duplican", "interval": 2880, "last_time": "04:36 PM"},
    {"name": "Wannitas", "interval": 2880, "last_time": "04:40 PM"},
    {"name": "Metus", "interval": 2880, "last_time": "04:46 PM"},
    {"name": "Asta", "interval": 3720, "last_time": "04:53 PM"},
    {"name": "Ordo", "interval": 3720, "last_time": "04:59 PM"},
    {"name": "Secreta", "interval": 3720, "last_time": "05:07 PM"},
    {"name": "Supore", "interval": 3720, "last_time": "05:15 PM"},
]

# ========================
# Helper Functions
# ========================

def calculate_next_time(last_time_str, interval_minutes):
    """Calculate next spawn based on last kill time + interval, always rolling forward."""
    today = datetime.now().date()
    last_time = datetime.strptime(last_time_str, "%I:%M %p").replace(
        year=today.year, month=today.month, day=today.day
    )
    next_time = last_time + timedelta(minutes=interval_minutes)

    # Keep adding interval until it's in the future
    while next_time <= datetime.now():
        next_time += timedelta(minutes=interval_minutes)

    return last_time, next_time

def get_countdown(next_time):
    return next_time - datetime.now()

# ========================
# Streamlit Page Config
# ========================
st.set_page_config(page_title="Lord 9 Boss Timers", layout="wide")

st.markdown(
    "<h1 style='text-align: center; color: orange;'>⏳ Lord 9 Boss Timers (Adjusted Target Dates)</h1>",
    unsafe_allow_html=True,
)

# ========================
# Build Table
# ========================
data = []
for boss in boss_data:
    last_time, next_time = calculate_next_time(boss["last_time"], boss["interval"])
    countdown = get_countdown(next_time)

    # Default target date = real next_time
    target_date = next_time

    # Adjustment: Ego → Supore target dates only
    if boss["name"] in ["Ego", "Aranco", "Livera", "Undomiel", "Amentis",
                        "General Aquleus", "Baron Braudmore", "Gareth",
                        "Shuliar", "Larba", "Catena", "Lady Dalia",
                        "Titore", "Duplican", "Wannitas", "Metus",
                        "Asta", "Ordo", "Secreta", "Supore"]:
        target_date = target_date - timedelta(days=1)

    data.append({
        "Name": boss["name"],
        "Interval": boss["interval"],
        "Last Time": last_time.strftime("%I:%M %p"),
        "Countdown": str(countdown).split(".")[0],
        "Next Time": next_time.strftime("%I:%M %p"),
        "Target Date": target_date.strftime("%Y-%m-%d %I:%M:%S %p"),
    })

df = pd.DataFrame(data)

# ========================
# Display Table
# ========================
st.dataframe(
    df.style.set_properties(**{
        'text-align': 'center',
        'color': 'white',
        'background-color': 'black'
    }),
    use_container_width=True,
    height=720
)
