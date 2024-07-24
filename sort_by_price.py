from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import re


# Use ChromeDriverManager to download and install the correct version of chromedriver
service = ChromeService(ChromeDriverManager().install())

# Initialize the WebDriver
driver = webdriver.Chrome(service=service)

def test_sort_by_price():
    driver.get('https://www.only.in/')
    
    # Close the login popup if it appears
    try:
        close_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), '✕')]"))
        )
        close_button.click()
    except TimeoutException:
        print("Login popup did not appear or could not be closed.")
    
    search_bar = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, 'search'))
    )
    search_bar.send_keys('shirts')
    search_bar.send_keys(Keys.RETURN)
    
    try:
        # Locate and click the "Sort by" dropdown button
        sortby_dropdown = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".st-sorting-btn"))
        )
        sortby_dropdown.click()
    except Exception as e:
        print("Error while clicking 'sort by':", e)
        return
    
    try:
        # Locate and click the "Price - Low to High" option
        price_low_to_high = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Price (Low to High)')]"))
        )
        price_low_to_high.click()
    except Exception as e:
        print("Error while clicking 'Price - Low to High':", e)
        return
    
    try:
        # Wait for the sorted results to be loaded
        sorted_results = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.st-product-item'))
        )
        print("Test Passed: Products are sorted by price.")
    except TimeoutException:
        print("Test Failed: Sorted results did not load in time.")
        return
    
    if not sorted_results:
        print("No sorted results found.")
        return

    try:
        prices = []
        for element in sorted_results[:5]:  # Limiting to the first 5 results for demonstration
            try:
                # Extract price using the correct selector
                price_text = element.find_element(By.CSS_SELECTOR, 'span.st-price-new').text
                price_value = int(re.sub(r'[^\d]', '', price_text))
                prices.append(price_value)
            except Exception as e:
                print(f"An error occurred while extracting price: {e}")
        
        print(prices)  # Debug: Print extracted prices 
        assert prices == sorted(prices), "Products are not sorted by price."
        print("Test Passed: Products are sorted by price.")
    except AssertionError as e:
        print(f"Test Failed: {e}")

# Run the test case
test_sort_by_price()

# Close the WebDriver
driver.quit()
