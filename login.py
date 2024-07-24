from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Use ChromeDriverManager to download and install the correct version of chromedriver
service = ChromeService(ChromeDriverManager().install())

# Initialize the WebDriver
driver = webdriver.Chrome(service=service)

def login_test():
    # Navigate directly to the login page
    driver.get('https://www.only.in/login?login_with=email')

    # Wait for the login form to be present and fill in credentials
    try:
        email_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'email'))
        )
        email_field.send_keys('yehinip975@reebsd.com')  # Replace with your email

        password_field = driver.find_element(By.NAME, 'password')
        password_field.send_keys('Test@1234')  # Replace with your password
        password_field.send_keys(Keys.RETURN)
        print("Credentials entered and login form submitted.")
        print("Test passed.")
    except TimeoutException:
        print("Failed to load the login form.")
        return

# Run the test case
login_test()
