from datetime import datetime
from logging import getLogger, INFO, Formatter
from os import startfile, environ, path
from subprocess import run
from threading import Thread
from time import sleep
from logging.handlers import TimedRotatingFileHandler

import pyautogui as pg
from decouple import config, Config, RepositoryEnv

from selenium.webdriver import Chrome, ChromeOptions
from selenium.common.exceptions import NoSuchElementException, \
    WebDriverException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

FILE_DIRECTORY = path.abspath(path.dirname(__file__))

log_file = path.join(FILE_DIRECTORY, "automation.log")
logger = getLogger(__name__)
logger.setLevel(INFO)
file_handler = TimedRotatingFileHandler(
    log_file, when="midnight", backupCount=1
)
file_handler.setFormatter(Formatter(
    "%(asctime)s - %(levelname)s - %(message)s", datefmt="%d-%b-%y %H:%M:%S")
)
logger.addHandler(file_handler)

WORK_STARTED = False
MEETING_STARTED = False
TIMESHEET_FILLED = False


def notify_user(message) -> None:
    """Send the bubble notification for windows with message"""
    run(["powershell",
         path.join(FILE_DIRECTORY, "notify_user.ps1"),
         f'"{message}"'],
        shell=True)


def start_office_apps() -> None:
    """Start the office apps like Chrome, Teams, Outlook"""
    logger.info("Starting Chrome")
    run(
        ["start", "chrome", "--start-maximized",
         config("GMAIL_LINK"), config("CALENDAR_LINK"),
         config("CHATS_LINK"), config("CREDENTIALS_SHEET_LINK")],
        shell=True
    )
    logger.info("Starting Microsoft Teams")
    startfile(config("TEAMS_LOCATION"))
    logger.info("Starting Outlook")
    startfile(config("OUTLOOK_LOCATION"))


def start_hd_meeting(meeting_id: str):
    """Start HD Meeting with the given meeting id"""
    logger.info("Starting HD Meeting for ID %s" % meeting_id)
    startfile(config("HD_MEETINGS_LOCATION"))
    sleep(3)

    # Move to Join a Meeting button and click
    logger.info("Move pointer to Join a Meeting button")
    pg.moveTo(int(config("JOIN_MEETING_X")), int(config("JOIN_MEETING_Y")))
    logger.info("Click on Join a Meeting Button")
    pg.click()
    sleep(3)

    # Move cursor to Meeting ID input, click and enter meeting id
    logger.info("Move to Meeting ID input")
    pg.moveTo(int(config("MEETING_ID_X")), int(config("MEETING_ID_Y")))
    logger.info("Click on Meeting ID input")
    pg.click()
    logger.info("Enter Meeting ID %s" % meeting_id)
    pg.write(meeting_id)

    # Move cursor to Enter your name , click, delete all and enter name
    logger.info("Move to Your Name input")
    pg.moveTo(int(config("YOUR_NAME_X")), int(config("YOUR_NAME_Y")))
    logger.info("Click on Your Name input")
    pg.click()
    logger.info("Select all text using Ctrl + a")
    pg.hotkey("ctrl", "a")
    logger.info("Delete current text")
    pg.press("delete")
    logger.info("Enter name")
    pg.typewrite(config("YOUR_NAME"))

    # Move and click Join button
    logger.info("Move to Join button")
    pg.moveTo(int(config("JOIN_BTN_X")), int(config("JOIN_BTN_Y")))
    logger.info("Click on Join button")
    pg.click()
    sleep(8)

    # Move to Join with Computer Audio button and click
    logger.info("Move to Join with Computer Audio button")
    pg.moveTo(int(config("JOIN_WITH_AUDIO_X")),
              int(config("JOIN_WITH_AUDIO_Y")))
    logger.info("Click on Join with Computer Audio button")
    pg.click()
    sleep(1)

    # Mute HD Meeting and Maximize window
    logger.info("Mute HD Meeting using Alt + a")
    pg.hotkey("alt", "a")
    sleep(0.5)
    logger.info("Maximize the HD Meeting window using Win + UP")
    pg.hotkey("win", "up")


def fill_timesheet() -> None:
    """Just open the timesheet filling table and close after 5 minutes."""
    options = ChromeOptions()
    driver = Chrome(executable_path=environ.get("CHROME_DRIVER"),
                    options=options)
    driver.maximize_window()
    wait = WebDriverWait(driver, 60)

    selectors = Config(RepositoryEnv(path.join(
        FILE_DIRECTORY, "timesheet_selectors.env"
    )))
    try:
        logger.info("Opening ERP link in browser")
        driver.get(config("ERP_LINK"))
        logger.info("Waiting for login button to be clickable")
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                               selectors("login_button"))))
        logger.info("Entering username")
        driver.find_element_by_id(selectors("username_input")) \
            .send_keys(config("USERNAME"))
        logger.info("Entering password")
        driver.find_element_by_id(selectors("password_input")) \
            .send_keys(config("PASSWORD"))
        logger.info("Clicking login button")
        driver.find_element_by_css_selector(selectors("login_button")).click()

        logger.info("Waiting for left expand menu to be clickable")
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                               selectors("left_expand_menu"))))
        logger.info("Clicking timesheet expand menu")
        driver.find_element_by_css_selector(selectors("left_expand_menu"))\
            .click()
        logger.info("Waiting for timesheet submenu to be visible")
        wait.until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, selectors("timesheet_menu"))
        ))
        logger.info("Clicking timesheet expand menu")
        driver.find_element_by_css_selector(selectors("timesheet_menu"))\
            .click()
        logger.info("Waiting for recent timecard to be clickable")
        wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, selectors("recent_timecard_link"))
        ))
        logger.info("Clicking recent timecard link")
        driver.find_element_by_css_selector(selectors("recent_timecard_link"))\
            .click()
        logger.info("Waiting for timesheet table to load")
        wait.until(EC.presence_of_element_located((
            By.CSS_SELECTOR, selectors("timesheet_first_row")
        )))
        logger.info("Get first row of timesheet table")
        timesheet_first_row = driver.find_element_by_css_selector(
            selectors("timesheet_first_row")
        )
        logger.info("Getting each data in first row of timesheet")
        first_row_data = timesheet_first_row.find_elements_by_tag_name(
            selectors("first_row_data")
        )

        if first_row_data[1].text == selectors("timesheet_status_new"):
            logger.info("Editing the timesheet")
            first_row_data[7].find_element_by_css_selector(
                selectors("edit_timesheet_button")
            ).click()
        elif first_row_data[1].text == selectors("timesheet_status_old"):
            logger.info("Creating a new timesheet")
            driver.find_element_by_id(selectors("create_card_button"))

        logger.info("Going to sleep for 900 seconds")
        sleep(900)
        logger.info("Wakey wakey!!")

        logger.info("Checking if browser is running")
        if driver.title:
            logger.info("Browser is still open. Trying to find logout button")
            driver.find_element_by_css_selector(selectors("logout_button"))\
                .click()
    except NoSuchElementException as e:
        logger.error("Element not found %s " % e, exc_info=True)
    except TimeoutException as e:
        logger.error("Tired of waiting %s" % e, exc_info=True)
    except WebDriverException as e:
        logger.error("Webdriver crash %s" % e, exc_info=True)
    finally:
        logger.info("Closing driver. Peace out.")
        driver.quit()


notify_user("Starting script to automate office apps.")

logger.info("Starting the loop")
current_datetime: datetime
while current_datetime := datetime.today():
    if current_datetime.weekday() in (5, 6):
        logger.info("Its a off day. :D")
        pass
    elif not WORK_STARTED and 9 <= current_datetime.hour < 5:
        logger.info("Starting the work. :B")
        start_office_apps()
        WORK_STARTED = True
        TIMESHEET_FILLED = False
    elif not MEETING_STARTED and current_datetime.hour == 10 \
            and current_datetime.minute >= 58:
        pass
    elif not TIMESHEET_FILLED and current_datetime.hour == 17 \
            and current_datetime.minute >= 45:
        logger.info("Timesheet filling time, running another thread.")
        Thread(target=fill_timesheet, daemon=True).start()
        TIMESHEET_FILLED = True
    elif WORK_STARTED and current_datetime.hour >= 5:
        logger.info("Office time over. Set WORK_STARTED = False")
        WORK_STARTED = False
    elif not MEETING_STARTED and current_datetime.hour == 18:
        if current_datetime.minute >= 13:
            logger.info("QA evening meeting")
            notify_user("Evening QA Meeting. Launching HD Meeting")
            start_hd_meeting(config("QA_MEETING"))
            MEETING_STARTED = True
        elif current_datetime.minute >= 58:
            logger.info("Evening scrum")
            notify_user("Evening SCRUM. Launching HD Meeting")
            start_hd_meeting(config("SCRUM_MEETING"))
            MEETING_STARTED = True
    elif MEETING_STARTED:
        if current_datetime.hour == 18 and 58 > current_datetime.minute >= 45:
            logger.info("Evening QA meeting over, MEETING_STARTED = False")
            MEETING_STARTED = False
        elif current_datetime.hour == 19 and current_datetime.minute > 30:
            logger.info("Evening Scrum over, MEETING_STARTED = False")
            MEETING_STARTED = False

    # Sleep for 20 seconds and then check again.
    sleep(20)
