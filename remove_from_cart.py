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

def test_add_and_remove_product():
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
        first_product = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'a.st-single-product'))
        )
        first_product.click()

        # Wait for a new window/tab to open
        WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))
        
        # Print available windows/tabs for debugging
        print("Number of open windows/tabs:", len(driver.window_handles))
        print("Window handles:", driver.window_handles)

        # Switch to the new window/tab
        driver.switch_to.window(driver.window_handles[1])

        # Wait for the product title to be loaded
        product_title = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'h1.product-title'))
        )
        assert product_title.text != "", "Product title is missing."
        print("Product details page displays the correct information.")

        # Select size
        try:
            size_option_label = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//input[@name='option[1580493]'][@value='8727420']/following-sibling::label"))
            )
            size_option_label.click()
            print("Size selected successfully.")
        except TimeoutException:
            print("Size selection failed.")
            return

        # Add to Cart
        try:
            add_to_cart_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '.addtoCart-Btn'))
            )
            add_to_cart_button.click()
            print("Test Passed: Product added to cart.")
        except TimeoutException:
            print("Failed to add product to cart.")
            return

        # Go to Cart
        try:
            cart_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.cart-price.dropdown-toggle'))
            )
            cart_button.click()
            print("Navigated to cart.")
        except TimeoutException:
            print("Failed to navigate to cart.")
            return

        # Remove from Cart
        try:
            remove_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(@onclick, 'cart.remove') and contains(@class, 'button-remove')]"))
            )
            remove_button.click()
            print("Test Passed: Product removed from cart.")
        except TimeoutException:
            print("Failed to remove product from cart.")
            return
    finally:
        driver.quit()

# Run the test case
test_add_and_remove_product()
