from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import time
import os

# Manila timezone
MANILA = ZoneInfo("Asia/Manila")

# Timer data
timers_data = [
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

RESET = "\033[0m"
RED = "\033[91m"
YELLOW = "\033[93m"
GREEN = "\033[92m"
CYAN = "\033[96m"

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

        # Ensure next_time is in the future
        while self.next_time < datetime.now(tz=MANILA):
            self.last_time = self.next_time
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

def print_table(timers):
    os.system('cls' if os.name == 'nt' else 'clear')
    headers = ["Name", "Interval (min)", "Last Time", "Countdown", "Next Time"]
    col_widths = [20, 15, 22, 15, 22]

    print(CYAN + "-" * sum(col_widths) + RESET)
    print("".join(f"{h:<{w}}" for h, w in zip(headers, col_widths)))
    print(CYAN + "-" * sum(col_widths) + RESET)

    for t in timers:
        remaining = t.countdown().total_seconds()
        color = GREEN if remaining >= 300 else (YELLOW if remaining >= 60 else RED)
        countdown_str = t.format_countdown()
        row = [
            t.name,
            str(t.interval_minutes),
            t.last_time.strftime("%Y-%m-%d %I:%M %p"),
            f"{color}{countdown_str}{RESET}",
            t.next_time.strftime("%Y-%m-%d %I:%M %p"),
        ]
        print("".join(f"{val:<{w}}" for val, w in zip(row, col_widths)))

    print(CYAN + "-" * sum(col_widths) + RESET)

def run_timers():
    timers = [TimerEntry(*data) for data in timers_data]
    while True:
        # Update next_time for bosses that already spawned
        for t in timers:
            t.update_next()
        # Sort by closest countdown
        timers_sorted = sorted(timers, key=lambda x: x.countdown())
        print_table(timers_sorted)
        time.sleep(1)

if __name__ == "__main__":
    run_timers()
