
import os
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE = "https://opencart.abstracta.us/index.php?route="

def login(driver, wait):
    # Open Login page
    driver.get(BASE + "account/login")

    # Enter registered email
    
    email = wait.until(
    EC.visibility_of_element_located((By.ID, "input-email"))
)
    email.clear()
    email.send_keys(os.environ["OPENCART_TEST_EMAIL"])

    # Enter password
    password = driver.find_element(By.ID, "input-password")
    password.clear()
    password.send_keys(os.environ["OPENCART_TEST_PASSWORD"])

    print("Email entered:", repr(email.get_attribute("value")))
    print("Password length:", len(password.get_attribute("value") or ""))
   
    # Click Login
    driver.find_element(
        By.CSS_SELECTOR, "input[type='submit']"
    ).click()

    # Check login result
    print("URL after login:", driver.current_url)

    errors = driver.find_elements(By.CSS_SELECTOR, ".alert-danger")

    if errors:
        for error in errors:
            print("LOGIN FAILED:", error.text)
    else:
        print("No login error displayed")

    # Verify successful login
    wait.until(
    EC.visibility_of_element_located(
        (By.LINK_TEXT, "Logout")
    )
)

print("PASS: Customer logged in successfully")


def test_f6_add_to_wishlist():
    driver = webdriver.Safari()
    wait = WebDriverWait(driver, 20)

    try:
        # Step 1: Login
        login(driver, wait)

        # Step 2: Open MacBook product
        driver.get(BASE + "product/product&product_id=43")
        print("PASS: MacBook product opened")

        # Step 3: Click Add to Wish List
        heart = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR,
                 "button[data-original-title='Add to Wish List']")
            )
        )
        heart.click()

        # Step 4: Verify success message
        message = wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, ".alert-success")
            )
        )
        assert "wish list" in message.text.lower()
        print("PASS: MacBook added to Wishlist")

        # Step 5: Open Wishlist
        driver.get(BASE + "account/wishlist")

        # Step 6: Verify MacBook is displayed
        product = wait.until(
            EC.visibility_of_element_located(
                (By.LINK_TEXT, "MacBook")
            )
        )
        assert product.is_displayed()

        print("PASS: MacBook displayed in Wishlist")
        print("PASS: F6 Scenario 1 completed")

    finally:
        driver.quit()


def test_f6_view_wishlist():
    driver = webdriver.Safari()
    wait = WebDriverWait(driver, 20)

    try:
        # Step 1: Login
        login(driver, wait)

        # Step 2: Open Wishlist
        driver.get(BASE + "account/wishlist")
        print("PASS: Wishlist page opened")

        # Step 3: Verify MacBook exists
        product = wait.until(
            EC.visibility_of_element_located(
                (By.LINK_TEXT, "MacBook")
            )
        )
        assert product.is_displayed()

        print("PASS: MacBook found in Wishlist")
        print("PASS: F6 Scenario 2 completed")

    finally:
        driver.quit()


def test_f6_remove_from_wishlist():
    driver = webdriver.Safari()
    wait = WebDriverWait(driver, 20)

    try:
        # Step 1: Login
        login(driver, wait)

        # Step 2: Open Wishlist
        driver.get(BASE + "account/wishlist")
        print("PASS: Wishlist page opened")

        # Step 3: Find MacBook row
        row = wait.until(
            EC.presence_of_element_located(
                (By.XPATH,
                 "//tr[.//a[normalize-space()='MacBook']]")
            )
        )

        # Step 4: Click Remove button
        remove = row.find_element(
            By.CSS_SELECTOR,
            "a[href*='account/wishlist&remove=']"
        )
        remove.click()

        # Step 5: Verify MacBook is removed
        wait.until(
            EC.invisibility_of_element_located(
                (By.XPATH,
                 "//tr[.//a[normalize-space()='MacBook']]")
            )
        )

        print("PASS: MacBook removed from Wishlist")
        print("PASS: F6 Scenario 3 completed")

    finally:
        driver.quit()


def test_add_product_to_wishlist():
    driver = webdriver.Safari()
    wait = WebDriverWait(driver, 15)

    try:
        # Step 1: Open login page
        driver.get(
            "https://opencart.abstracta.us/index.php?route=account/login"
        )

        # Step 2: Log in
        driver.find_element(By.ID, "input-email").send_keys(
            "cripymix2@gmail.com"
        )
        driver.find_element(By.ID, "input-password").send_keys(
            os.environ["OPENCART_TEST_PASSWORD"]
        )
        driver.find_element(
            By.CSS_SELECTOR, "input[type='submit']"
        ).click()

        # Step 3: Verify login
        wait.until(EC.url_contains("account/account"))
        print("PASS: Login successful")

        # Step 4: Open iPhone product
        driver.get(
            "https://opencart.abstracta.us/index.php?route=product/product&product_id=40"
        )

        # Step 5: Add iPhone to wishlist
        wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button[data-original-title='Add to Wish List']")
            )
        ).click()

        # Step 6: Verify success message
        wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, ".alert-success")
            )
        )

        print("PASS: iPhone added to wishlist")
        print("PASS: F6 Scenario 1 completed")

    finally:
        driver.quit()

    
def test_view_wishlist():
    driver = webdriver.Safari()
    wait = WebDriverWait(driver, 15)

    try:
        # Step 1: Open login page
        driver.get(
            "https://opencart.abstracta.us/index.php?route=account/login"
        )

        # Step 2: Log in
        driver.find_element(By.ID, "input-email").send_keys(
            "cripymix2@gmail.com"
        )
        driver.find_element(By.ID, "input-password").send_keys(
            os.environ["OPENCART_TEST_PASSWORD"]
        )
        driver.find_element(
            By.CSS_SELECTOR, "input[type='submit']"
        ).click()

        wait.until(EC.url_contains("account/account"))
        print("PASS: Login successful")

        # Step 3: Open wishlist
        driver.get(
            "https://opencart.abstracta.us/index.php?route=account/wishlist"
        )

        # Step 4: Verify iPhone appears
        wait.until(
            EC.visibility_of_element_located(
                (By.LINK_TEXT, "iPhone")
            )
        )

        print("PASS: iPhone displayed in wishlist")
        print("PASS: F6 Scenario 2 completed")

    finally:
        driver.quit()

def test_remove_from_wishlist():
    driver = webdriver.Safari()
    wait = WebDriverWait(driver, 15)

    try:
        # Step 1: Open login page
        driver.get(
            "https://opencart.abstracta.us/index.php?route=account/login"
        )

        # Step 2: Log in
        driver.find_element(By.ID, "input-email").send_keys(
            "cripymix2@gmail.com"
        )
        driver.find_element(By.ID, "input-password").send_keys(
            os.environ["OPENCART_TEST_PASSWORD"]
        )
        driver.find_element(
            By.CSS_SELECTOR, "input[type='submit']"
        ).click()

        wait.until(EC.url_contains("account/account"))
        print("PASS: Login successful")

        # Step 3: Open wishlist
        driver.get(
            "https://opencart.abstracta.us/index.php?route=account/wishlist"
        )

        # Step 4: Find iPhone in wishlist
        product = wait.until(
            EC.visibility_of_element_located(
                (By.LINK_TEXT, "iPhone")
            )
        )
        print("PASS: iPhone found in wishlist")

        # Step 5: Remove iPhone from wishlist
        row = product.find_element(By.XPATH, "./ancestor::tr")
        row.find_element(
            By.CSS_SELECTOR,
            "a[data-original-title='Remove']"
        ).click()

        # Step 6: Verify iPhone is removed
        wait.until(
            EC.invisibility_of_element_located(
                (By.LINK_TEXT, "iPhone")
            )
        )

        print("PASS: iPhone removed from wishlist")
        print("PASS: F6 Scenario 3 completed")

    finally:
        driver.quit()


