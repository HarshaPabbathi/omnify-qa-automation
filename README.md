# OrangeHRM QA Automation

## Project Overview

This project automates functional testing of the OrangeHRM web application using Selenium WebDriver and Pytest.

The automation covers the complete employee-management workflow, starting from user login and continuing through PIM navigation, employee creation, employee verification, and logout.

The project also includes manual login test cases and potential usability/functional issues.

## Application Under Test

**Application:** OrangeHRM Demo
**URL:** https://opensource-demo.orangehrmlive.com/

## Objectives

* Automate the OrangeHRM login functionality.
* Navigate to the PIM module using mouse hover and click.
* Add four employees with unique names.
* Navigate to the Employee List.
* Search for and verify the newly added employees.
* Logout successfully.
* Document manual test scenarios and potential bugs.

## Technologies Used

* Python
* Selenium WebDriver
* Pytest
* Page Object Model (POM)
* Chrome WebDriver
* Git and GitHub

## Project Structure

```text
omnify_qa/
│
├── pages/
│   ├── base_page.py
│   ├── login_page.py
│   ├── dashboard_page.py
│   ├── pim_page.py
│   ├── employee_page.py
│   └── employee_list_page.py
│
├── tests/
│   ├── test_login.py
│   └── test_orangehrm_workflow.py
│
├── manual_script/
│   └── basic_login_test.py
│
├── documentation/
│   └── OrangeHRM_QA_Test_Cases.xlsx
│
├── screenshots/
│
├── requirements.txt
├── pytest.ini
└── README.md
```

## Page Object Model

The project follows the Page Object Model design pattern.

Each page has its own class containing:

* Page locators
* Page-specific actions
* Reusable methods

### Page Objects

**LoginPage**

* Opens the login page
* Enters username and password
* Performs login
* Validates login results

**DashboardPage**

* Verifies Dashboard
* Navigates to PIM
* Performs logout

**PIMPage**

* Opens Add Employee
* Opens Employee List

**EmployeePage**

* Enters employee information
* Saves employees
* Verifies employee details

**EmployeeListPage**

* Searches employees
* Verifies employee names

**BasePage**

* Contains reusable Selenium functions such as:

  * Click
  * Find element
  * Type text
  * Hover
  * Wait
  * Visibility checks

## Automated Login Tests

The login automation contains the following scenarios:

1. Valid username and password
2. Invalid username
3. Invalid password
4. Empty username and password
5. Empty username
6. Empty password

### Login Test Result

```text
6 passed
```

## Automated Employee Workflow

The main workflow performs:

```text
Login
  ↓
Dashboard
  ↓
Hover over PIM
  ↓
Click PIM
  ↓
Add Employee 1
  ↓
Add Employee 2
  ↓
Add Employee 3
  ↓
Add Employee 4
  ↓
Employee List
  ↓
Search Employees
  ↓
Name Verified
  ↓
Logout
```

### Workflow Test Result

```text
1 passed
```

Four employees were successfully added and verified in the Employee List.

## How to Install

Clone the repository:

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
```

Navigate to the project:

```bash
cd omnify_qa
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Running Login Tests

Run:

```bash
pytest -v tests/test_login.py
```

## Running the Complete Workflow

Run:

```bash
pytest -s -v tests/test_orangehrm_workflow.py
```

The `-s` option displays messages such as:

```text
Login Successful
PIM Navigation Successful
Name Verified: ...
Logout Successful
```

## Test Documentation

The Excel test documentation contains:

* 10 login test cases
* Employee Add test case
* Employee View test case
* Employee Update test case
* Employee Delete test case
* 3 potential bugs/usability issues

File:

```text
documentation/OrangeHRM_QA_Test_Cases.xlsx
```

## Test Results

| Test Suite            | Result   |
| --------------------- | -------- |
| Login Tests           | 6 Passed |
| Employee Workflow     | 1 Passed |
| Employees Added       | 4        |
| Employee Verification | Passed   |
| Logout                | Passed   |

## Potential Issues

Three potential login-related usability/functional issues have been documented in the test-case Excel file.

These are identified as potential issues and should be validated against the current application behavior.

## Future Improvements

* Add automated tests for employee update functionality.
* Add automated tests for employee deletion.
* Add HTML test reports.
* Add screenshots automatically when a test fails.
* Integrate the tests with a CI/CD pipeline.
* Improve autocomplete handling during employee search.

## Author

Harsha Pabbathi
