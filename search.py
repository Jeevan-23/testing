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

def test_search_product():
    driver.get('https://www.only.in/')
    
    # Close the login popup if it appears
    try:
        close_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), '✕')]"))
        )
        close_button.click()
    except TimeoutException:
        print("Login popup did not appear or could not be closed.")
    
    # Locate the search bar input element
    search_bar = driver.find_element(By.NAME, 'search')
    
    search_bar.send_keys('shirts')
    search_bar.send_keys(Keys.RETURN)
    
    try:
        results = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.MuiGrid-root.MuiGrid-container.MuiGrid-spacing-xs-2'))
        )
        assert len(results) > 0, "No search results found."
        print("Test Passed: Search results are displayed.")
    except TimeoutException:
        print("Test Failed: Search results did not load in time.")
    except AssertionError as e:
        print(f"Test Failed: {e}")

# Run the test case
test_search_product()
