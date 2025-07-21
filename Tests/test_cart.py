import pytest

from Locators.alllocators import LoginPageLocators, ProductPageLocators
from Pages.CartPage import CartPage
from Pages.LoginPage import LoginPage
from Pages.ProductPage import ProductPage


@pytest.fixture()
def go_to_cart_page(driver):
    login_page = LoginPage(driver)
    login_page.login(LoginPageLocators.valid_username, LoginPageLocators.valid_password)
    product_page = ProductPage(driver)
    product_page.add_single_item(ProductPageLocators.add_back_pack_path)
    product_page.add_single_item(ProductPageLocators.add_Jacket_path)
    product_page.click_on_cart_button()
    cart_page = CartPage(driver)
    print("User is in cart page")
    return cart_page
@pytest.mark.order(14)
def test_cart_page(go_to_cart_page):
    print("Test Cart Page title")
    cart_page = go_to_cart_page
    assert "cart.html" in cart_page.get_current_url(),f"Expected cart.html in '{cart_page.get_current_url()}'"
    assert "Your Cart" in cart_page.cart_title(),f"Expected Your Cart but Got {cart_page.cart_title()}"
@pytest.mark.order(15)
def test_continue_shopping_button(go_to_cart_page):
    print("Test Continue Shopping Button ")
    cart_page = go_to_cart_page
    cart_page.click_continue_button()
    assert "inventory" in cart_page.get_current_url(),f"Expected inventory in url but Got {cart_page.get_current_url()}"
@pytest.mark.order(16)
def test_checkout_button(go_to_cart_page):
    print("Test Checkout Button ")
    cart_page = go_to_cart_page
    cart_page.click_checkout_button()
    assert "checkout-step-one" in cart_page.get_current_url(),f"Expected checkout-step-one in url but Got {cart_page.get_current_url()}"

