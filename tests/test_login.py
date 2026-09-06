"""
test_login.py

Login test cases for OrangeHRM.
"""

import os
import sys

import pytest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# ---------------------------------------------------------
# Project path
# ---------------------------------------------------------

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

sys.path.append(PROJECT_ROOT)


from pages.login_page import LoginPage


# ---------------------------------------------------------
# Test data
# ---------------------------------------------------------

USERNAME = os.getenv(
    "ORANGE_USERNAME",
    "Admin"
)

PASSWORD = os.getenv(
    "ORANGE_PASSWORD",
    "admin123"
)


# ---------------------------------------------------------
# Browser fixture
# ---------------------------------------------------------

@pytest.fixture
def driver():

    options = Options()

    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-popup-blocking")

    driver = webdriver.Chrome(
        options=options
    )

    driver.set_page_load_timeout(30)

    yield driver

    try:
        driver.quit()
    except Exception:
        pass


# ---------------------------------------------------------
# Helper function
# ---------------------------------------------------------

def open_login_page(driver):

    login_page = LoginPage(driver)

    driver.get(login_page.URL)

    WebDriverWait(
        driver,
        20
    ).until(
        EC.visibility_of_element_located(
            (By.NAME, "username")
        )
    )

    return login_page


# ---------------------------------------------------------
# TEST 1
# ---------------------------------------------------------

def test_valid_login(driver):

    login_page = open_login_page(driver)

    login_page.enter_username(
        USERNAME
    )

    login_page.enter_password(
        PASSWORD
    )

    login_page.click_login()

    assert login_page.is_login_successful(), \
        "Valid login failed - Dashboard was not displayed"


# ---------------------------------------------------------
# TEST 2
# ---------------------------------------------------------

def test_invalid_username(driver):

    login_page = open_login_page(driver)

    login_page.login(
        "InvalidUser",
        PASSWORD
    )

    assert login_page.is_visible(
        login_page.ERROR_ALERT,
        timeout=10
    ), \
        "Error message was not displayed"


# ---------------------------------------------------------
# TEST 3
# ---------------------------------------------------------

def test_invalid_password(driver):

    login_page = open_login_page(driver)

    login_page.login(
        USERNAME,
        "InvalidPassword"
    )

    assert login_page.is_visible(
        login_page.ERROR_ALERT,
        timeout=10
    ), \
        "Error message was not displayed"


# ---------------------------------------------------------
# TEST 4
# ---------------------------------------------------------

def test_empty_credentials(driver):

    login_page = open_login_page(driver)

    login_page.click_login()

    assert login_page.is_visible(
        login_page.USERNAME_REQUIRED,
        timeout=5
    ), \
        "Username required validation was not displayed"

    assert login_page.is_visible(
        login_page.PASSWORD_REQUIRED,
        timeout=5
    ), \
        "Password required validation was not displayed"


# ---------------------------------------------------------
# TEST 5
# ---------------------------------------------------------

def test_empty_username(driver):

    login_page = open_login_page(driver)

    login_page.enter_password(
        PASSWORD
    )

    login_page.click_login()

    assert login_page.is_visible(
        login_page.USERNAME_REQUIRED,
        timeout=5
    ), \
        "Username required validation was not displayed"


# ---------------------------------------------------------
# TEST 6
# ---------------------------------------------------------

def test_empty_password(driver):

    login_page = open_login_page(driver)

    login_page.enter_username(
        USERNAME
    )

    login_page.click_login()

    assert login_page.is_visible(
        login_page.PASSWORD_REQUIRED,
        timeout=5
    ), \
        "Password required validation was not displayed"