import pytest
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, UnexpectedAlertPresentException

HOME = "https://opencart.abstracta.us/"
PRODUCT = HOME + "index.php?route=product/product&product_id=40"
CART = HOME + "index.php?route=checkout/cart"
CHECKOUT = HOME + "index.php?route=checkout/checkout"


def test_checkout():
    driver = webdriver.Safari()
    wait = WebDriverWait(driver, 20)
    step = "Starting test"

    try:
        # Step 1: Open website
        step = "Open website"
        driver.get(HOME)

        wait.until(
            EC.presence_of_element_located((By.NAME, "search"))
        )
        print("PASS: Website opened")

        # Step 2: Search for iPhone
        step = "Search for iPhone"
        search = driver.find_element(By.NAME, "search")
        search.send_keys("iPhone")

        driver.find_element(
            By.CSS_SELECTOR, "#search button"
        ).click()

        wait.until(EC.url_contains("product/search"))
        print("PASS: iPhone search opened")

        # Step 3: Open iPhone using HTTPS
        step = "Open iPhone product"
        driver.get(PRODUCT)

        wait.until(
            EC.element_to_be_clickable(
                (By.ID, "button-cart")
            )
        )

        assert wait.until(
            EC.visibility_of_element_located((
                By.CSS_SELECTOR, "#content h1"
            ))

        ).text.strip() == "iPhone"

        print("PASS: iPhone product opened")

        # Step 4: Add iPhone to cart
        step = "Add iPhone to cart"

        wait.until(
            EC.element_to_be_clickable(
                (By.ID, "button-cart")
            )
        ).click()

        # Wait until the cart counter shows an item
        wait.until(
            lambda d: "1 item" in d.find_element(
                By.ID, "cart-total"
            ).text
        )

        print("PASS: iPhone added to cart")

        # Step 5: Verify shopping cart
        step = "Verify shopping cart"
        driver.get(CART)

        wait.until(EC.url_contains("checkout/cart"))

        wait.until(
            EC.presence_of_element_located(
                (By.TAG_NAME, "body")
            )
        )

        cart_products = driver.find_elements(
            By.CSS_SELECTOR,
            "table tbody tr td:nth-child(2) a"
)

        assert any(
            product.text.strip() == "iPhone"
            for product in cart_products
        ), "iPhone not found in the shopping cart table"

        print("PASS: Shopping cart opened")
        print("PASS: iPhone found in shopping cart")

        # Step 6: Open Checkout
        step = "Open Checkout"

        checkout = wait.until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//a[contains(@href, 'checkout/checkout')]"
            ))
        )

        checkout.click()

        # Step 7: Verify Checkout page
        step = "Verify Checkout page"

        try:
            alert = WebDriverWait(driver, 3).until(EC.alert_is_present())
            print("Website alert:", alert.text)
            alert.accept()
        except TimeoutException:
            pass

        try:
            wait.until(EC.url_contains("checkout/checkout"))
        except UnexpectedAlertPresentException:
            alert = driver.switch_to.alert
            print("Website alert:", alert.text)
            alert.accept()

            wait.until(EC.url_contains("checkout/checkout"))

        assert "checkout/checkout" in driver.current_url

        print("PASS: Checkout page opened")
        print("PASS: F5 Checkout navigation completed")

    except Exception:
        print("FAILED STEP:", step)
        try:
            print("FAILED URL:", driver.current_url)
            print("PAGE TITLE:", driver.title)
            driver.save_screenshot("f5_error.png")
        except Exception:
            pass
        raise

    finally:
        driver.quit()


def test_checkout_empty_billing():
    driver = webdriver.Safari()
    wait = WebDriverWait(driver, 20)

    try:
        # Open checkout with a product in the cart
        driver.get(PRODUCT)

        wait.until(
            EC.element_to_be_clickable((By.ID, "button-cart"))
        ).click()

        wait.until(
            lambda d: "1 item" in d.find_element(
                By.ID, "cart-total"
            ).text
        )

        driver.get(CHECKOUT)

        # Select Guest Checkout
        wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "input[value='guest']")
            )
        ).click()

        driver.find_element(By.ID, "button-account").click()

        # Continue without filling billing details
        wait.until(
            EC.element_to_be_clickable(
                (By.ID, "button-guest")
            )
        ).click()

        # Verify validation errors
        errors = wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, ".text-danger")
            )
        )

        assert errors.is_displayed()
        print("PASS: Empty billing details rejected")
        print("PASS: F5 Scenario 2 completed")

    finally:
        driver.quit()


def test_checkout_valid_billing():
    driver = webdriver.Safari()
    wait = WebDriverWait(driver, 20)

    try:
        # Step 1: Add product to cart
        driver.get(PRODUCT)
        wait.until(
            EC.element_to_be_clickable((By.ID, "button-cart"))
        ).click()

        wait.until(
            lambda d: "1 item" in d.find_element(
                By.ID, "cart-total"
            ).text
        )

        # Step 2: Open checkout
        driver.get(CHECKOUT)

        # Step 3: Select Guest Checkout
        wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "input[value='guest']")
            )
        ).click()

        driver.find_element(By.ID, "button-account").click()

        # Step 4: Enter valid billing details
        wait.until(
            EC.visibility_of_element_located(
                (By.ID, "input-payment-firstname")
            )
        )

        details = {
            "input-payment-firstname": "Test",
            "input-payment-lastname": "Customer",
            "input-payment-email": "checkouttest@example.com",
            "input-payment-telephone": "0412345678",
            "input-payment-address-1": "123 Test Street",
            "input-payment-city": "Sydney",
            "input-payment-postcode": "2000"
        }

        for field, value in details.items():
            driver.find_element(By.ID, field).send_keys(value)

        # Select Australia
        country = Select(driver.find_element(By.ID, "input-payment-country"))
        country.select_by_visible_text("Australia")

        # Wait for state options to load
        wait.until(
            lambda d: any(
                "New South Wales" in option.text
                for option in Select(
                    d.find_element(By.ID, "input-payment-zone")
                ).options
            )
        )

        # Show available states
        state = Select(driver.find_element(By.ID, "input-payment-zone"))
        print("Available states:", [option.text for option in state.options])

        # Select New South Wales
        state.select_by_visible_text("New South Wales")

        print("PASS: Australia and New South Wales selected")
       
        # Step 6: Continue
        driver.find_element(By.ID, "button-guest").click()

        # Step 7: Verify payment step
        wait.until(
            EC.visibility_of_element_located(
                (By.ID, "collapse-payment-method")
            )
        )

        print("PASS: Valid billing details accepted")
        print("PASS: Payment method step displayed")
        print("PASS: F5 Scenario 3 completed")

    finally:
        driver.quit()


        
