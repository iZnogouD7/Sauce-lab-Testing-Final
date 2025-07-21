import pytest

from Locators.alllocators import (
    LoginPageLocators,
    ProductPageLocators,
    CartPageLocators,
    CheckoutPageLocators,
    FinishPageLocators
)

from Pages.LoginPage import LoginPage
from Pages.ProductPage import ProductPage
from Pages.CheckoutOverviewPage import CheckoutOverviewPage
from Pages.BasePage import BasePage


@pytest.mark.usefixtures("driver")
def test_checkout_overview_with_backpack(driver):
    base = BasePage(driver)
    driver.get(LoginPageLocators.loginpageUrl)

    # Step 1: Login
    login = LoginPage(driver)
    login.login(LoginPageLocators.valid_username, LoginPageLocators.valid_password)

    # Step 2: Add 1 item (Backpack)
    product = ProductPage(driver)
    product.add_single_item(ProductPageLocators.add_back_pack_path)
    cart_count = product.get_cart_count()
    assert cart_count == 1, f"Expected 1 item in cart, got {cart_count}"
    product.click_on_cart_button()

    # Step 3: Go to Checkout Info Page
    base.click_element(CartPageLocators.checkout_path)
    base.type_in_element(CheckoutPageLocators.first_name_path, CheckoutPageLocators.valid_first_name)
    base.type_in_element(CheckoutPageLocators.last_name_path, CheckoutPageLocators.valid_last_name)
    base.type_in_element(CheckoutPageLocators.Zip_code_path, CheckoutPageLocators.valid_zip_code)
    base.click_element(CheckoutPageLocators.continue_button_path)

    # Step 4: On Checkout Overview Page
    overview = CheckoutOverviewPage(driver)

    # 4.1: Validate item name and price
    item_names = base.find_elements(ProductPageLocators.inventory_name_class_path)
    item_prices = base.find_elements(ProductPageLocators.inventory_price_class_path)

    item_name_texts = [item.text for item in item_names]
    item_price_texts = [item.text for item in item_prices]

    assert "Sauce Labs Backpack" in item_name_texts, "Backpack name not found"
    assert "$29.99" in item_price_texts, "Backpack price incorrect"

    # 4.2: Static Payment and Shipping Information
    payment_info = base.get_text_from_element(("xpath", '//*[@class="summary_value_label"][1]'))
    shipping_info = base.get_text_from_element(("xpath", '//*[@class="summary_value_label"][2]'))
    assert payment_info == "SauceCard #31337", f"Expected payment info mismatch: {payment_info}"
    assert shipping_info == "Free Pony Express Delivery!", f"Expected shipping info mismatch: {shipping_info}"

    # 4.3: Total Calculations
    item_total = float(base.get_text_from_element(("class name", "summary_subtotal_label")).split("$")[1])
    tax = float(base.get_text_from_element(("class name", "summary_tax_label")).split("$")[1])
    total = float(base.get_text_from_element(("class name", "summary_total_label")).split("$")[1])

    assert item_total == 29.99, f"Expected item total 29.99, got {item_total}"
    assert tax == 2.40, f"Expected tax 2.40, got {tax}"
    assert total == 32.39, f"Expected total 32.39, got {total}"

    # Step 5: Click Finish → Go to Finish Page
    overview.click_finish_button()
    assert FinishPageLocators.finish_page_url in driver.current_url, "Not redirected to finish page"
    print("Checkout Overview Test Passed!")


def test_cancel_checkout_overview(driver):
    base = BasePage(driver)
    driver.get(LoginPageLocators.loginpageUrl)

    # Step 1: Login
    login = LoginPage(driver)
    login.login(LoginPageLocators.valid_username, LoginPageLocators.valid_password)

    # Step 2: Add 1 item (Backpack)
    product = ProductPage(driver)
    product.add_single_item(ProductPageLocators.add_back_pack_path)
    cart_count = product.get_cart_count()
    assert cart_count == 1, f"Expected 1 item in cart, got {cart_count}"
    product.click_on_cart_button()

    # Step 3: Go to Checkout Info Page
    base.click_element(CartPageLocators.checkout_path)
    base.type_in_element(CheckoutPageLocators.first_name_path, CheckoutPageLocators.valid_first_name)
    base.type_in_element(CheckoutPageLocators.last_name_path, CheckoutPageLocators.valid_last_name)
    base.type_in_element(CheckoutPageLocators.Zip_code_path, CheckoutPageLocators.valid_zip_code)
    base.click_element(CheckoutPageLocators.continue_button_path)

    # Step 4: On Checkout Overview Page
    overview = CheckoutOverviewPage(driver)
    overview.click_cancel_button()
    assert "inventory.html" in driver.current_url, "Cancel did not return to products page"


def test_finish_checkout_overview(driver):
    base = BasePage(driver)
    driver.get(LoginPageLocators.loginpageUrl)

    # Step 1: Login
    login = LoginPage(driver)
    login.login(LoginPageLocators.valid_username, LoginPageLocators.valid_password)

    # Step 2: Add 1 item (Backpack)
    product = ProductPage(driver)
    product.add_single_item(ProductPageLocators.add_back_pack_path)
    cart_count = product.get_cart_count()
    assert cart_count == 1, f"Expected 1 item in cart, got {cart_count}"
    product.click_on_cart_button()

    # Step 3: Go to Checkout Info Page
    base.click_element(CartPageLocators.checkout_path)
    base.type_in_element(CheckoutPageLocators.first_name_path, CheckoutPageLocators.valid_first_name)
    base.type_in_element(CheckoutPageLocators.last_name_path, CheckoutPageLocators.valid_last_name)
    base.type_in_element(CheckoutPageLocators.Zip_code_path, CheckoutPageLocators.valid_zip_code)
    base.click_element(CheckoutPageLocators.continue_button_path)

    # Step 4: On Checkout Overview Page
    overview = CheckoutOverviewPage(driver)
    overview.click_finish_button()
    assert FinishPageLocators.finish_page_url in driver.current_url, "Not redirected to finish page"

