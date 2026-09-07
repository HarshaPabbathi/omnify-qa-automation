from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class PIMPage(BasePage):

    # ---------------------------------------------------------
    # Locators
    # ---------------------------------------------------------

    PIM_HEADER = (
        By.XPATH,
        "//h6[normalize-space()='PIM']"
    )

    ADD_EMPLOYEE_BUTTON = (
        By.XPATH,
        "//a[normalize-space()='Add Employee']"
    )

    EMPLOYEE_LIST_TAB = (
        By.XPATH,
        "//a[normalize-space()='Employee List']"
    )

    # ---------------------------------------------------------
    # Page verification
    # ---------------------------------------------------------

    def is_pim_page_displayed(self):
        """Verify that the PIM page is displayed."""
        return self.is_visible(
            self.PIM_HEADER,
            timeout=10
        )

    # ---------------------------------------------------------
    # Navigation
    # ---------------------------------------------------------

    def click_add_employee(self):
        """Open the Add Employee page."""

        button = self.wait.until(
            EC.visibility_of_element_located(
                self.ADD_EMPLOYEE_BUTTON
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            button
        )

        self.wait.until(
            EC.url_contains("pim/addEmployee")
        )

    def click_employee_list(self):
        """Open the Employee List page."""

        button = self.wait.until(
            EC.visibility_of_element_located(
                self.EMPLOYEE_LIST_TAB
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            button
        )

        self.wait.until(
            EC.url_contains("pim/viewEmployeeList")
        )