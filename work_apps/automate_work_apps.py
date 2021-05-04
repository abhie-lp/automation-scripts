from datetime import datetime, timedelta
from os import startfile, path
from subprocess import run
from time import sleep

from decouple import config

GMAIL_LINK = config("GMAIL_LINK")
CALENDAR_LINK = config("CALENDAR_LINK")
CHATS_LINK = config("CHATS_LINK")

TEAMS_LOCATION = config("TEAMS_LOCATION")
OUTLOOK_LOCATION = config("OUTLOOK_LOCATION")

NOTIFICATION = path.join(path.dirname(__file__), "notify_user.ps1")


def notify_user(message) -> None:
    """Send the bubble notification for windows with message"""
    run(["powershell", NOTIFICATION, f'"{message}"'], shell=True)


def sleep_seconds(today: datetime) -> int:
    """Returns the number of seconds the script has to sleep"""
    # Assuming that script is running between 12 AM to 9 AM
    # Copy today's data
    next_datetime = today.replace()
    
    # Check if script is running in off day or after work hours
    if today.weekday() in (5, 6) or today.hour > 18:
        # Increment 1 day in today and assign to next_datetime
        next_datetime = today + timedelta(1)

    # Replace next_datetime hour, minute and seconds to 9 o'clock
    next_datetime = next_datetime.replace(hour=9, minute=0, second=0)

    return int((next_datetime - today).total_seconds())


notify_user("Starting script to automate office apps.")


current_datetime: datetime
while current_datetime := datetime.today():
    if current_datetime.weekday() in (5, 6):
        notify_user("No office today. XD")
        sleep(sleep_seconds(current_datetime) + 20)
        continue

    if 9 <= current_datetime.hour <= 18:
        run(
            ["start", "chrome", "--start-maximized",
             GMAIL_LINK, CALENDAR_LINK, CHATS_LINK],
            shell=True
        )
        startfile(TEAMS_LOCATION)
        startfile(OUTLOOK_LOCATION)

        # Sleep for next 12 hours
        notify_user("Sleeping for next 12 hours")
        sleep(43200)
    else:
        sleepy_seconds = sleep_seconds(current_datetime) + 20
        notify_user(f"You are early. Sleeping for {sleepy_seconds} seconds")
        sleep(sleepy_seconds)
