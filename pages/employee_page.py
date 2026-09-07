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
        self.click(self.SAVE_BUTTON)

    # ------------------------------------------------
    # Add employee
    # ------------------------------------------------


    def add_employee(
        self,
        first_name,
        last_name,
        middle_name=""
    ):
        
        self.enter_first_name(first_name)

        if middle_name:
            self.enter_middle_name(middle_name)

        self.enter_last_name(last_name)

        self.click_save()

    # Wait for the employee details page to load
        self.wait.until(
            lambda driver:
            "viewPersonalDetails" in driver.current_url
            or "employeeId" in driver.current_url
        )


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