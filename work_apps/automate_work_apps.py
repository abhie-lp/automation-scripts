from datetime import datetime
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

WORK_STARTED = False


def notify_user(message) -> None:
    """Send the bubble notification for windows with message"""
    run(["powershell", NOTIFICATION, f'"{message}"'], shell=True)


def start_office_apps() -> None:
    """Start the office apps like Chrome, Teams, Outlook"""
    run(
        ["start", "chrome", "--start-maximized",
         GMAIL_LINK, CALENDAR_LINK, CHATS_LINK],
        shell=True
    )
    startfile(TEAMS_LOCATION)
    startfile(OUTLOOK_LOCATION)


notify_user("Starting script to automate office apps.")

current_datetime: datetime
while current_datetime := datetime.today():
    if current_datetime.weekday() in (5, 6):
        pass
    elif not WORK_STARTED and 9 <= current_datetime.hour < 18:
        start_office_apps()
        WORK_STARTED = True
    elif WORK_STARTED and current_datetime.hour >= 18:
        WORK_STARTED = False

    # Sleep for 15 seconds and then check again.
    sleep(20)
