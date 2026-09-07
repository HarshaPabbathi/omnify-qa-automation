from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class LoginPage(BasePage):

    URL = (
        "https://opensource-demo.orangehrmlive.com/"
        "web/index.php/auth/login"
    )

    # Locators
    USERNAME_INPUT = (By.NAME, "username")
    PASSWORD_INPUT = (By.NAME, "password")
    LOGIN_BUTTON = (By.XPATH, "//button[@type='submit']")

    ERROR_ALERT = (
        By.XPATH,
        "//p[contains(@class,'oxd-alert-content-text')]"
    )

    DASHBOARD_HEADER = (
        By.XPATH,
        "//h6[text()='Dashboard']"
    )

    USERNAME_REQUIRED = (
        By.XPATH,
        "//input[@name='username']/ancestor::div[contains(@class,'oxd-input-group')]//span"
    )

    PASSWORD_REQUIRED = (
        By.XPATH,
        "//input[@name='password']/ancestor::div[contains(@class,'oxd-input-group')]//span"
    )

    def load(self):
        self.open(self.URL)
        return self

    def enter_username(self, username):
        """Enter username."""
        self.type_text(self.USERNAME_INPUT, username)

    def enter_password(self, password):
        """Enter password."""
        self.type_text(self.PASSWORD_INPUT, password)

    def click_login(self):
        """Click Login button."""
        self.click(self.LOGIN_BUTTON)

    def login(self, username, password):
        """Perform login."""
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()

    def get_error_message(self):
        """Return login error message."""
        return self.get_text(self.ERROR_ALERT)

    def is_login_successful(self):
        """Verify Dashboard is displayed."""
        return self.is_visible(
            self.DASHBOARD_HEADER,
            timeout=10
        )

    def is_login_page_displayed(self):
        """Verify login page is displayed."""
        return self.is_visible(
            self.USERNAME_INPUT,
            timeout=10
        )

    def get_username_validation_message(self):
        """Return username validation message."""
        return self.get_text(self.USERNAME_REQUIRED)

    def get_password_validation_message(self):
        """Return password validation message."""
        return self.get_text(self.PASSWORD_REQUIRED)