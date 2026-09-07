import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from pages.base_page import BasePage


class EmployeeListPage(BasePage):

    # ------------------------------------------------
    # Locators
    # ------------------------------------------------

    EMPLOYEE_NAME_INPUT = (
        By.XPATH,
        "//label[contains(normalize-space(),'Employee Name')]"
        "/ancestor::div[contains(@class,'oxd-input-group')]"
        "//input"
    )

    EMPLOYEE_SUGGESTIONS = (
        By.XPATH,
        "//div[contains(@class,'oxd-autocomplete-option')]"
    )

    SEARCH_BUTTON = (
        By.XPATH,
        "//button[normalize-space()='Search']"
    )

    RESET_BUTTON = (
        By.XPATH,
        "//button[normalize-space()='Reset']"
    )

    RESULT_ROWS = (
        By.XPATH,
        "//div[contains(@class,'oxd-table-body')]"
        "//div[@role='row']"
    )

    EMPLOYEE_LIST_HEADER = (
        By.XPATH,
        "//h5[normalize-space()='Employee Information']"
    )

    NO_RECORDS_MESSAGE = (
        By.XPATH,
        "//span[normalize-space()='No Records Found']"
    )

    LOADER = (By.CSS_SELECTOR, ".oxd-form-loader")

    # ------------------------------------------------
    # Page verification
    # ------------------------------------------------

    def is_employee_list_page_displayed(self):
        return self.is_visible(self.EMPLOYEE_LIST_HEADER, timeout=10)

    # ------------------------------------------------
    # Wait for loader (appear, then disappear)
    # ------------------------------------------------

    def wait_for_loader(self, appear_timeout=2, disappear_timeout=10):
        """Best-effort wait: first give the loader a short window to show
        up at all, then wait for it to go away. If it never appears
        (request resolved before we could catch it), that's fine — we
        just move on to the disappearance check, which will also no-op
        if there's nothing there."""

        try:
            from selenium.webdriver.support.ui import WebDriverWait
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
    # Reset search filters
    # ------------------------------------------------

    def reset_search(self):
        """Clicks Reset (if present) to clear any filter state left over
        from a previous search before starting a new one."""

        reset_buttons = self.driver.find_elements(*self.RESET_BUTTON)

        if not reset_buttons:
            return

        try:
            reset_buttons[0].click()
            self.wait_for_loader()
        except Exception:
            # Non-fatal — proceed with the search regardless.
            pass

    # ------------------------------------------------
    # Select autocomplete suggestion
    # ------------------------------------------------

    def select_employee_from_suggestion(self, first_name, last_name):

        full_name = f"{first_name} {last_name}"

        try:
            self.wait.until(
                lambda driver: len(
                    driver.find_elements(*self.EMPLOYEE_SUGGESTIONS)
                ) > 0
            )
        except TimeoutException:
            print(f"No autocomplete suggestions appeared for {full_name}")
            return False

        suggestions = self.driver.find_elements(*self.EMPLOYEE_SUGGESTIONS)

        valid_suggestions = []

        for suggestion in suggestions:
            suggestion_text = suggestion.text.strip()
            print(f"Autocomplete suggestion: {suggestion_text}")

            if not suggestion_text or "searching" in suggestion_text.lower():
                continue

            valid_suggestions.append(suggestion)

        # Try exact full-name match first.
        for suggestion in valid_suggestions:
            suggestion_text = suggestion.text.strip()
            if (
                first_name.lower() in suggestion_text.lower()
                and last_name.lower() in suggestion_text.lower()
            ):
                try:
                    self.driver.execute_script("arguments[0].click();", suggestion)
                    print(f"Selected employee: {suggestion_text}")
                    return True
                except Exception:
                    pass

        # Fall back to first-name-only match.
        for suggestion in valid_suggestions:
            suggestion_text = suggestion.text.strip()
            if first_name.lower() in suggestion_text.lower():
                try:
                    self.driver.execute_script("arguments[0].click();", suggestion)
                    print(f"Selected employee: {suggestion_text}")
                    return True
                except Exception:
                    pass

        print(f"No matching employee suggestion found for {full_name}")
        return False

    # ------------------------------------------------
    # Search employee
    # ------------------------------------------------

    def search_employee(self, first_name, last_name):

        full_name = f"{first_name} {last_name}"
        print(f"Searching for: {full_name}")

        # Clear any leftover filter state from a previous search.
        self.reset_search()

        field = self.wait.until(
            EC.visibility_of_element_located(self.EMPLOYEE_NAME_INPUT)
        )

        field.click()
        field.clear()
        field.send_keys(first_name)

        selected = self.select_employee_from_suggestion(first_name, last_name)

        if not selected:
            print(f"Autocomplete selection skipped for {full_name}")

        search_button = self.wait.until(
            EC.element_to_be_clickable(self.SEARCH_BUTTON)
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            search_button
        )

        search_button.click()

        self.wait_for_loader()

    # ------------------------------------------------
    # Get result rows (polls until stable / matched / no-records / timeout)
    # ------------------------------------------------

    def get_result_rows(self, expected_name=None, timeout=10):
        """Actively polls the results table instead of trusting loader
        timing alone. Returns as soon as:
          - a row containing expected_name is found, or
          - the 'No Records Found' message appears, or
          - the row content stops changing between two consecutive polls
            (used when expected_name isn't provided), or
          - the timeout is reached (returns whatever is present, if
            anything).
        """

        end_time = time.time() + timeout
        last_rows_text = None
        stable_count = 0

        while time.time() < end_time:
            no_records = self.driver.find_elements(*self.NO_RECORDS_MESSAGE)
            if no_records:
                return []

            rows = self.driver.find_elements(*self.RESULT_ROWS)

            if rows:
                current_text = "|".join(
                    r.text.strip() for r in rows if r.text.strip()
                )

                if expected_name and expected_name.lower() in current_text.lower():
                    return rows

                if not expected_name:
                    if current_text == last_rows_text:
                        stable_count += 1
                        if stable_count >= 2:
                            return rows
                    else:
                        stable_count = 0
                        last_rows_text = current_text

            time.sleep(0.3)

        # Timed out — return whatever is currently present (may be empty).
        return self.driver.find_elements(*self.RESULT_ROWS)

    # ------------------------------------------------
    # Verify employee
    # ------------------------------------------------

    def is_employee_listed(self, first_name, last_name):

        full_name = f"{first_name} {last_name}"

        self.search_employee(first_name, last_name)

        rows = self.get_result_rows(expected_name=full_name, timeout=10)

        if not rows:
            print(f"No employee rows found for {full_name}")
            return False

        for row in rows:
            row_text = row.text.strip()

            if not row_text:
                continue

            print(f"Checking row: {row_text}")

            if (
                first_name.lower() in row_text.lower()
                and last_name.lower() in row_text.lower()
            ):
                print(f"Name Verified: {full_name}")
                return True

        print(f"Name NOT Verified: {full_name}")
        return False