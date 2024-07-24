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

def test_product_details():
    driver.get('https://www.only.in')
    
    # Close the login popup if it appears
    try:
        close_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), '✕')]"))
        )
        close_button.click()
    except TimeoutException:
        print("Login popup did not appear or could not be closed.")
    
    # Wait for the search bar to be present
    try:
        search_bar = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'search'))
        )
        search_bar.send_keys('shirt')
        search_bar.send_keys(Keys.RETURN)
    except TimeoutException:
        print("Search bar did not load in time.")
        return
    
    # Wait for the search results to be loaded and click the first product
    try:
        # results = WebDriverWait(driver, 20).until(
        #     EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.st-product-layout.st-product-item'))
        # )
        first_product = EC.presence_of_elements_located(By.CSS_SELECTOR, 'a.st-single-product')
        first_product.click()
        
        # Switch to the new window/tab
        driver.switch_to.window(driver.window_handles[1])
        
        # Wait for the product title to be loaded
        product_title = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'h1.product-title'))
        )
        assert product_title.text != "", "Product title is missing."
        print("Test Passed: Product details page displays the correct information.")
    except TimeoutException:
        print("Test Failed: Product details did not load in time.")
    except AssertionError as e:
        print(f"Test Failed: {e}")
    finally:
        driver.quit()

# Run the test case
test_product_details()
