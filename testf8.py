
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    UnexpectedAlertPresentException
)

HOME_URL = "https://opencart.abstracta.us/"
CART_URL = "https://opencart.abstracta.us/index.php?route=checkout/cart"


def test_manage_cart():
    driver = webdriver.Safari()
    wait = WebDriverWait(driver, 15)

    try:
        # Step 1: Open website
        driver.get(HOME_URL)

        # Step 2: Open MacBook product
        macbook = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//a[text()='MacBook']")
            )
        )
        macbook.click()

        # Step 3: Add MacBook to cart
        add_button = wait.until(
            EC.element_to_be_clickable(
                (By.ID, "button-cart")
            )
        )
        add_button.click()

        # Handle any website alert
        try:
            alert = WebDriverWait(driver, 3).until(
                EC.alert_is_present()
            )
            print("Website alert:", alert.text)
            alert.accept()
        except TimeoutException:
            pass

        # Step 4: Open shopping cart
        driver.get(CART_URL)

        # Check that MacBook was added
        quantity = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "input[name^='quantity[']")
            )
        )

        assert "MacBook" in driver.page_source
        print("PASS: MacBook added to cart")

        # Step 5: Update quantity to 2
        quantity.clear()
        quantity.send_keys("2")

        update_button = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button[data-original-title='Update']")
            )
        )
        update_button.click()

        # Handle any website alert
        try:
            alert = WebDriverWait(driver, 3).until(
                EC.alert_is_present()
            )
            print("Website alert:", alert.text)
            alert.accept()
        except TimeoutException:
            pass

        # Check updated quantity
        wait.until(
            lambda d: d.find_element(
                By.CSS_SELECTOR,
                "input[name^='quantity[']"
            ).get_attribute("value") == "2"
        )

        print("PASS: Quantity updated to 2")

        # Step 6: Remove MacBook
        driver.get(CART_URL)

        try:
            alert = WebDriverWait(driver, 3).until(
                EC.alert_is_present()
            )
            print("Website alert:", alert.text)
            alert.accept()
        except TimeoutException:
            pass

        remove_button = wait.until(
             EC.element_to_be_clickable(
                  (By.CSS_SELECTOR, "#checkout-cart button[onclick*='cart.remove']")
            )
        )
        print("Main cart Remove button found")
        remove_button.click()
        
        # Check shopping cart is empty
        wait.until(
            lambda d: len(d.find_elements(
                By.XPATH,
                "//form[@id='checkout-cart']//a[contains(text(), 'MacBook')]"
            )) == 0
        )

        # Verify MacBook is no longer in the cart
        assert len(driver.find_elements(
            By.XPATH,
            "//form[@id='checkout-cart']//a[contains(text(), 'MacBook')]"
        )) == 0, "FAIL: MacBook is still in the cart"

        print("PASS: MacBook removed from cart")
        print("PASS: F8 Manage Cart test completed")

    finally:
        driver.quit()
