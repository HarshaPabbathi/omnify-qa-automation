import os
import sys
import time

import pytest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Add project root to Python path
PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

sys.path.append(PROJECT_ROOT)

from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.pim_page import PIMPage
from pages.employee_page import EmployeePage
from pages.employee_list_page import EmployeeListPage


# OrangeHRM demo credentials
USERNAME = os.getenv(
    "ORANGE_USERNAME",
    "Admin"
)

PASSWORD = os.getenv(
    "ORANGE_PASSWORD",
    "admin123"
)


# Generate unique employee names for each execution
TEST_SUFFIX = str(
    int(time.time())
)

NEW_EMPLOYEES = [
    (
        f"Alice{TEST_SUFFIX}",
        "Johnson"
    ),
    (
        f"Brian{TEST_SUFFIX}",
        "Smith"
    ),
    (
        f"Carla{TEST_SUFFIX}",
        "Davis"
    ),
    (
        f"David{TEST_SUFFIX}",
        "Wilson"
    ),
]


@pytest.fixture
def driver():

    options = Options()

    options.add_argument(
        "--start-maximized"
    )

    driver = webdriver.Chrome(
        options=options
    )

    yield driver

    driver.quit()


def test_add_and_verify_employees(driver):

    # ------------------------------------------------
    # STEP 1: Login
    # ------------------------------------------------

    login_page = LoginPage(driver)

    login_page.load()

    login_page.login(
        USERNAME,
        PASSWORD
    )

    assert login_page.is_login_successful(), \
        "Login failed - Dashboard was not displayed"

    print("\nLogin Successful")


    # ------------------------------------------------
    # STEP 2: Navigate to PIM
    # ------------------------------------------------

    dashboard_page = DashboardPage(driver)

    assert dashboard_page.is_dashboard_displayed(), \
        "Dashboard was not displayed"

    dashboard_page.go_to_pim()

    pim_page = PIMPage(driver)

    assert pim_page.is_pim_page_displayed(), \
        "PIM page was not displayed"

    print("PIM Navigation Successful")


    # ------------------------------------------------
    # STEP 3: Add 4 Employees
    # ------------------------------------------------

    employee_page = EmployeePage(driver)

    for first_name, last_name in NEW_EMPLOYEES:

        print(
            f"Adding Employee: "
            f"{first_name} {last_name}"
        )

        pim_page.click_add_employee()

        employee_page.add_employee(
            first_name,
            last_name
        )

        assert employee_page.is_employee_saved(), \
            f"Employee {first_name} {last_name} was not saved"

        print(
            f"Employee Added: "
            f"{first_name} {last_name}"
        )

        # Navigate back to PIM
        dashboard_page.go_to_pim()

        assert pim_page.is_pim_page_displayed(), \
            "Could not return to PIM page"


    # ------------------------------------------------
    # STEP 4: Employee List
    # ------------------------------------------------

    pim_page.click_employee_list()

    employee_list_page = EmployeeListPage(driver)

    assert employee_list_page.is_employee_list_page_displayed(), \
        "Employee List page was not displayed"

    print("Employee List Opened")


    # ------------------------------------------------
    # STEP 5: Verify Employees
    # ------------------------------------------------

    for first_name, last_name in NEW_EMPLOYEES:

        full_name = (
            f"{first_name} {last_name}"
        )

        found = employee_list_page.is_employee_listed(
            first_name,
            last_name
        )
        

        assert found, \
            f"{full_name} was not found in Employee List"


    # ------------------------------------------------
    # STEP 6: Logout
    # ------------------------------------------------

    dashboard_page.logout()

    assert dashboard_page.is_logged_out(), \
        "Logout failed - Login page was not displayed"

    print("Logout Successful")