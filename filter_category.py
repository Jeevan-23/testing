from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

service = ChromeService(ChromeDriverManager().install())

driver = webdriver.Chrome(service=service)

def test_filter_category():
    driver.get('https://www.only.in/')
    
    # Close the login popup if it appears
    try:
        close_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), '✕')]"))
        )
        close_button.click()
    except TimeoutException:
        print("Login popup did not appear or could not be closed.")
    
    # Use WebDriverWait to wait for the search bar to be present
    try:
        search_bar = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'search'))
        )
        search_bar.send_keys('shirts')
        search_bar.send_keys(Keys.RETURN)
    except TimeoutException:
        print("Search bar did not load in time.")
        return
    
    try:
        dress_checkbox = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//label[.//span[contains(text(), 'Dress')]]"))
        )
        dress_checkbox.click()
    except Exception as e:
        print(f"Error while clicking on Dress filter: {e}")
    
    try:
        filtered_results = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.st-product-item'))
        )
        assert len(filtered_results) > 0, "No filtered results found."
        print("Test Passed: Category filter applied and results are displayed.")
    except TimeoutException:
        print("Test Failed: Filtered results did not load in time.")
    except AssertionError as e:
        print(f"Test Failed: {e}")

# Run the test case
test_filter_category()

# Close the WebDriver
driver.quit()
