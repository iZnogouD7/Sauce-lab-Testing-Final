
import pytest

from Locators.alllocators import LoginPageLocators, CheckoutPageLocators
from Pages.CartPage import CartPage
from Pages.CheckoutPage import CheckoutPage
from Pages.LoginPage import LoginPage
from Pages.ProductPage import ProductPage
from Utils.FileReader import load_csv_data

@pytest.fixture()
def checkout_setup(driver):
    login_page = LoginPage(driver)
    login_page.login(LoginPageLocators.valid_username, LoginPageLocators.valid_password)
    product=ProductPage(driver)
    product.click_on_cart_button()
    cart=CartPage(driver)
    cart.click_checkout_button()
    checkout_page = CheckoutPage(driver)
    print("user is in Checkout Page")
    return checkout_page

@pytest.mark.parametrize("firstname,lastname,zip_code,expected", load_csv_data("Data/checkout_data.csv"))
def test_checkout_validation(checkout_setup,firstname, lastname,zip_code,expected):
    assert checkout_setup.get_current_url()== CheckoutPageLocators.checkout_page_url
    checkout_setup.enter_checkout_info(firstname,lastname,zip_code)
    print(f"Giving Data :{firstname},{lastname},{zip_code} ")
    if "Success" in expected:
        print(f"Test Passed and directed to url: {checkout_setup.get_current_url()}")
        assert checkout_setup.get_current_url() == "https://www.saucedemo.com/checkout-step-two.html",f"{checkout_setup.get_current_url()}"
        print(f"Got title : {checkout_setup.checkout_title()}")
        assert checkout_setup.checkout_title() == "Checkout: Overview",f"Got checkout title: {checkout_setup.checkout_title()}"
    elif "FirstNameNotGiven" in expected:

        print(f"FAILURE{firstname}{lastname}{zip_code}{checkout_setup.get_error()}")

        assert "Error: First Name is required" in checkout_setup.get_error(),f"Got error : {checkout_setup.get_error()}"
    elif "LastNameNotGiven" in expected:
        print(f"FAILURE{firstname}{lastname}{zip_code}{checkout_setup.get_error()}")

        assert "Error: Last Name is required" in checkout_setup.get_error(),f"Got error : {checkout_setup.get_error()}"
    elif "ZipCodeNotGiven" in expected:
        print(f"FAILURE{firstname}{lastname}{zip_code}{checkout_setup.get_error()}")

        assert "Error: Postal Code is required" in checkout_setup.get_error(), f"Got error : {checkout_setup.get_error()}"
    else:
        print("Other Errors Found")

def test_continue_button(checkout_setup):
        checkout_page=checkout_setup
        checkout_page.enter_checkout_info(CheckoutPageLocators.valid_first_name,CheckoutPageLocators.valid_last_name,CheckoutPageLocators.valid_zip_code)
        assert "checkout-step-two.html" in checkout_page.get_current_url(),f"Got:{checkout_page.get_current_url()}"
def test_cancel_button(checkout_setup):
    checkout_page=checkout_setup
    checkout_page.click_cancel_button()
    assert "cart.html" in checkout_page.get_current_url(),f"Got:{checkout_page.get_current_url()}"

def test_error_cancel_button(checkout_setup):
    checkout_page=checkout_setup
    checkout_page.click_continue_button()
    assert checkout_page.is_displayed(CheckoutPageLocators.error_message_path),f"Got:{checkout_page.is_displayed(CheckoutPageLocators.error_message_path)}"
    checkout_page.click_error_cancel_button()
    assert not checkout_page.is_displayed(CheckoutPageLocators.error_message_path),f"Got:{checkout_page.is_displayed(CheckoutPageLocators.error_message_path)}"
