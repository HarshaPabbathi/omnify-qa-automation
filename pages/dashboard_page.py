from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class DashboardPage(BasePage):

    # Locators

    PIM_MENU_ITEM = (
        By.XPATH,
        "//span[text()='PIM']"
    )

    USER_DROPDOWN = (
        By.XPATH,
        "//span[contains(@class,'oxd-userdropdown-tab')]"
    )

    LOGOUT_LINK = (
        By.XPATH,
        "//a[text()='Logout']"
    )

    DASHBOARD_HEADER = (
        By.XPATH,
        "//h6[text()='Dashboard']"
    )

    LOGIN_USERNAME_INPUT = (
        By.NAME,
        "username"
    )

    def is_dashboard_displayed(self):
        """Verify that Dashboard is displayed."""
        return self.is_visible(
            self.DASHBOARD_HEADER,
            timeout=10
        )

    def go_to_pim(self):
        """
        Hover over PIM and click it.

        This directly implements the assignment requirement:
        mouse hover over PIM and click PIM.
        """
        self.hover_and_click(self.PIM_MENU_ITEM)

    def logout(self):
        """Logout from the OrangeHRM application."""
        self.click(self.USER_DROPDOWN)

        self.click(self.LOGOUT_LINK)

    def is_logged_out(self):
        """Verify that logout returned to Login page."""
        return self.is_visible(
            self.LOGIN_USERNAME_INPUT,
            timeout=10
        )