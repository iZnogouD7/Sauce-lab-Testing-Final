import time

import pytest
from selenium.webdriver.common.by import By

from Locators.alllocators import LoginPageLocators, CartPageLocators, CheckoutPageLocators, FinishPageLocators
from Pages.BasePage import BasePage
from Pages.CheckoutOverviewPage import CheckoutOverviewPage
from Pages.LoginPage import LoginPage
from Pages.ProductPage import ProductPage
from Utils.read_checkout_data import read_checkout_data

checkout_test_data = read_checkout_data("Data/checkout_overview_data.csv")

@pytest.mark.parametrize("item", checkout_test_data)
def test_checkout_overview_dynamic(driver, item):
    base = BasePage(driver)
    driver.get(LoginPageLocators.loginpageUrl)

    LoginPage(driver).login(LoginPageLocators.valid_username, LoginPageLocators.valid_password)
    time.sleep(2)
    # Add dynamic product
    product = ProductPage(driver)
    time.sleep(2)
    base.click_element((By.ID, item["item_id"]))
    time.sleep(2)
    product.click_on_cart_button()
    time.sleep(2)

    base.click_element(CartPageLocators.checkout_path)
    time.sleep(2)
    base.type_in_element(CheckoutPageLocators.first_name_path, CheckoutPageLocators.valid_first_name)
    time.sleep(0.5)
    base.type_in_element(CheckoutPageLocators.last_name_path, CheckoutPageLocators.valid_last_name)
    time.sleep(0.5)
    base.type_in_element(CheckoutPageLocators.Zip_code_path, CheckoutPageLocators.valid_zip_code)
    time.sleep(0.5)
    base.click_element(CheckoutPageLocators.continue_button_path)
    time.sleep(0.5)

    overview = CheckoutOverviewPage(driver)
    time.sleep(2)

    # Item check
    item_names = overview.get_item_names()
    time.sleep(2)
    item_prices = overview.get_item_prices()
    time.sleep(2)
    assert item["item_name"] in item_names
    time.sleep(2)
    assert f"${item['price']}" in item_prices
    time.sleep(2)

    # Static content
    assert overview.get_payment_info() == "SauceCard #31337"
    time.sleep(2)
    assert overview.get_shipping_info() == "Free Pony Express Delivery!"
    time.sleep(2)

    # Financials


    assert overview.get_item_total() == float(item["price"])
    assert overview.get_tax() == float(item["tax"])
    assert overview.get_total() == float(item["total"])

    overview.click_finish_button()
    assert FinishPageLocators.finish_page_url in driver.current_url
