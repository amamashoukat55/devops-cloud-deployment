
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_student_records_app():
    driver = webdriver.Chrome()

    try:
        driver.get("http://16.171.17.4:8002")

        wait = WebDriverWait(driver, 10)

        heading = wait.until(
            EC.visibility_of_element_located((By.TAG_NAME, "h1"))
        )
        assert heading.text == "Student Records Management System"

        name_input = driver.find_element(By.ID, "name")
        email_input = driver.find_element(By.ID, "email")

        name_input.send_keys("Selenium Test Student")
        email_input.send_keys("selenium.test@example.com")

        driver.find_element(By.ID, "add-student").click()

        saved_student = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//td[text()='Selenium Test Student']")
            )
        )

        assert saved_student.text == "Selenium Test Student"
        print("TEST PASSED: Student was saved successfully!")

    finally:
        driver.quit()
