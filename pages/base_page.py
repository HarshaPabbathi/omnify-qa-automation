from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


class BasePage:
    """Base class containing reusable Selenium methods."""

    DEFAULT_TIMEOUT = 15

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, self.DEFAULT_TIMEOUT)

    def open(self, url):
        """Open a URL."""
        self.driver.get(url)

    def find(self, locator):
        """Wait until an element exists and return it."""
        return self.wait.until(
            EC.presence_of_element_located(locator)
        )

    def find_clickable(self, locator):
        """Wait until an element is clickable and return it."""
        return self.wait.until(
            EC.element_to_be_clickable(locator)
        )

    def find_all(self, locator):
        """Wait until all matching elements exist."""
        return self.wait.until(
            EC.presence_of_all_elements_located(locator)
        )

    def click(self, locator):
        """Click an element after waiting for it."""
        self.find_clickable(locator).click()

    def type_text(self, locator, text):
        """Clear an input field and type text."""
        field = self.find(locator)
        field.clear()
        field.send_keys(text)

    def get_text(self, locator):
        """Return visible text of an element."""
        return self.find(locator).text

    def hover(self, locator):
        """Move the mouse over an element."""
        element = self.find_clickable(locator)

        ActionChains(self.driver) \
            .move_to_element(element) \
            .perform()

    def hover_and_click(self, locator):
        """
        Hover over an element and click the same element.
        Used for the PIM navigation requirement.
        """
        element = self.find_clickable(locator)

        ActionChains(self.driver) \
            .move_to_element(element) \
            .click() \
            .perform()

    def is_visible(self, locator, timeout=5):
        """Check whether an element becomes visible."""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except Exception:
            return False

    def wait_for_url_contains(self, text, timeout=10):
        """Wait until the current URL contains the given text."""
        WebDriverWait(self.driver, timeout).until(
            EC.url_contains(text)
        )