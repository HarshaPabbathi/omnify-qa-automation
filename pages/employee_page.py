"""
employee_page.py

Page Object for the OrangeHRM Add Employee page.

Fixes applied:
  1. click_save() previously waited only for the loader to become
     INVISIBLE, without confirming it had appeared first. On a fast page
     load, the pre-existing loader can already be gone by the time the
     check runs, letting Save get clicked before the Angular form (and
     especially the auto-populated Employee ID field) has fully
     initialized. Now we wait for the loader to appear, then disappear,
     the same fix applied to EmployeeListPage.
  2. Before typing, we explicitly wait for the Employee ID field to be
     populated with a non-empty value — this is OrangeHRM's own signal
     that the Add Employee form has finished loading/initializing.
  3. is_employee_saved() no longer swallows failures silently. If the
     URL never changes to viewPersonalDetails, it actively looks for
     inline validation error messages on the page and prints them, so a
     failed save tells you *why* instead of just "was not saved".
"""

import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

from pages.base_page import BasePage


class EmployeePage(BasePage):

    # ------------------------------------------------
    # Locators
    # ------------------------------------------------

    FIRST_NAME_INPUT = (By.NAME, "firstName")
    LAST_NAME_INPUT = (By.NAME, "lastName")

    SAVE_BUTTON = (
        By.XPATH,
        "//button[@type='submit' and normalize-space()='Save']"
    )

    EMPLOYEE_ID_INPUT = (
        By.XPATH,
        "//label[contains(normalize-space(),'Employee Id')]"
        "/ancestor::div[contains(@class,'oxd-input-group')]"
        "//input"
    )

    LOADER = (By.CSS_SELECTOR, ".oxd-form-loader")

    VALIDATION_ERROR_MESSAGES = (
        By.XPATH,
        "//span[contains(@class,'oxd-input-field-error-message')]"
        " | //span[contains(@class,'oxd-text--span') and contains(@class,'error')]"
    )

    TOAST_MESSAGE = (
        By.XPATH,
        "//div[contains(@class,'oxd-toast')]"
    )

    # ------------------------------------------------
    # Wait for loader (appear, then disappear)
    # ------------------------------------------------

    def wait_for_loader(self, appear_timeout=2, disappear_timeout=10):
        """Best-effort wait: give the loader a short window to show up at
        all, then wait for it to go away. If it never appears (already
        gone, or too fast to catch), that's fine — we move on."""

        try:
            WebDriverWait(self.driver, appear_timeout).until(
                EC.visibility_of_element_located(self.LOADER)
            )
        except TimeoutException:
            pass

        try:
            self.wait.until(
                EC.invisibility_of_element_located(self.LOADER)
            )
        except TimeoutException:
            pass

    # ------------------------------------------------
    # Wait for the Add Employee form to be fully ready
    # ------------------------------------------------

    def wait_for_form_ready(self, timeout=10):
        """OrangeHRM auto-populates the Employee ID field asynchronously
        right after the Add Employee page renders. Waiting for it to be
        non-empty is a reliable signal that the form has fully
        initialized and it's safe to type into first/last name."""

        try:
            WebDriverWait(self.driver, timeout).until(
                lambda d: d.find_element(*self.EMPLOYEE_ID_INPUT).get_attribute("value").strip() != ""
            )
        except TimeoutException:
            # Not fatal — some builds/themes may not auto-populate this.
            # Proceed anyway rather than blocking the whole test.
            pass

    # ------------------------------------------------
    # Enter first name
    # ------------------------------------------------

    def enter_first_name(self, first_name):

        field = self.wait.until(
            EC.visibility_of_element_located(self.FIRST_NAME_INPUT)
        )

        field.clear()
        field.send_keys(first_name)

    # ------------------------------------------------
    # Enter last name
    # ------------------------------------------------

    def enter_last_name(self, last_name):

        field = self.wait.until(
            EC.visibility_of_element_located(self.LAST_NAME_INPUT)
        )

        field.clear()
        field.send_keys(last_name)

    # ------------------------------------------------
    # Click Save
    # ------------------------------------------------

    def click_save(self):

        self.wait_for_loader()

        save_button = self.wait.until(
            EC.element_to_be_clickable(self.SAVE_BUTTON)
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            save_button
        )

        save_button.click()

        # Give the submit its own loader cycle to complete before anyone
        # checks the URL/result.
        self.wait_for_loader()

    # ------------------------------------------------
    # Add employee
    # ------------------------------------------------

    def add_employee(self, first_name, last_name):

        self.wait_for_form_ready()

        self.enter_first_name(first_name)
        self.enter_last_name(last_name)

        self.click_save()

    # ------------------------------------------------
    # Diagnose a failed save
    # ------------------------------------------------

    def get_validation_errors(self):
        """Returns any visible inline validation error text currently on
        the page, so a failed save can explain itself."""

        errors = []

        for el in self.driver.find_elements(*self.VALIDATION_ERROR_MESSAGES):
            text = el.text.strip()
            if text:
                errors.append(text)

        return errors

    # ------------------------------------------------
    # Verify employee was saved
    # ------------------------------------------------

    def is_employee_saved(self, timeout=15):

        try:
            WebDriverWait(self.driver, timeout).until(
                EC.url_contains("/pim/viewPersonalDetails")
            )
            return True

        except TimeoutException:

            errors = self.get_validation_errors()

            if errors:
                print(
                    "Employee was NOT saved — validation error(s) found: "
                    + " | ".join(errors)
                )
            else:
                print(
                    "Employee was NOT saved — no validation errors found; "
                    f"current URL: {self.driver.current_url}"
                )

            return False