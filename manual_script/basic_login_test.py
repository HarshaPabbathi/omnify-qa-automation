"""
basic_login_test.py

Basic non-POM Selenium login test script.

This script demonstrates:
1. Valid login
2. Invalid login

Run:

python manual_script/basic_login_test.py
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


URL = (
    "https://opensource-demo.orangehrmlive.com/"
    "web/index.php/auth/login"
)

VALID_USERNAME = "Admin"
VALID_PASSWORD = "admin123"


def create_driver():

    driver = webdriver.Chrome()

    driver.maximize_window()

    return driver


def test_valid_login():

    driver = create_driver()

    try:

        driver.get(URL)

        wait = WebDriverWait(
            driver,
            10
        )

        username_field = wait.until(
            EC.visibility_of_element_located(
                (By.NAME, "username")
            )
        )

        password_field = driver.find_element(
            By.NAME,
            "password"
        )

        username_field.send_keys(
            VALID_USERNAME
        )

        password_field.send_keys(
            VALID_PASSWORD
        )

        password_field.send_keys(
            Keys.RETURN
        )

        wait.until(
            EC.url_contains("dashboard")
        )

        assert "dashboard" in driver.current_url.lower()

        print(
            "PASS: Valid login redirected "
            "to Dashboard."
        )

    finally:

        driver.quit()


def test_invalid_login():

    driver = create_driver()

    try:

        driver.get(URL)

        wait = WebDriverWait(
            driver,
            10
        )

        username_field = wait.until(
            EC.visibility_of_element_located(
                (By.NAME, "username")
            )
        )

        password_field = driver.find_element(
            By.NAME,
            "password"
        )

        username_field.send_keys(
            "wrong_user"
        )

        password_field.send_keys(
            "wrong_pass"
        )

        password_field.send_keys(
            Keys.RETURN
        )

        error = wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//p[contains(@class,'oxd-alert-content-text')]"
                )
            )
        )

        error_text = error.text

        assert "invalid" in error_text.lower()

        print(
            f"PASS: Invalid login showed error: "
            f"'{error_text}'"
        )

    finally:

        driver.quit()


if __name__ == "__main__":

    test_valid_login()

    test_invalid_login()