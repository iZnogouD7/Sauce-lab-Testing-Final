from Locators.alllocators import LoginPageLocators, CheckoutPageLocators
from Pages.CartPage import CartPage
from Pages.CheckoutOverviewPage import CheckoutOverviewPage
from Pages.CheckoutPage import CheckoutPage
from Pages.FinishPage import FinishPage
from Pages.LoginPage import LoginPage
from Pages.OtherPage import OtherPage
from Pages.ProductPage import ProductPage


def test_bug1_empty_cart_checkout(driver):
    login_page = LoginPage(driver)
    login_page.login(LoginPageLocators.valid_username, LoginPageLocators.valid_password)
    product_page = ProductPage(driver)
    product_page.click_on_cart_button()
    cart_page = CartPage(driver)
    cart_page.click_checkout_button()
    checkout_page = CheckoutPage(driver)
    checkout_page.enter_checkout_info(CheckoutPageLocators.valid_first_name, CheckoutPageLocators.valid_last_name,
                                      CheckoutPageLocators.valid_zip_code)
    checkout_overview_page = CheckoutOverviewPage(driver)
    checkout_overview_page.click_finish_button()
    finish_page = FinishPage(driver)
    assert finish_page.is_thank_you_displayed(),f"User able to checkout with empty cart. Displayed {finish_page.is_thank_you_displayed()}"

def test_bug2_menu_not_collapsing(driver):
    login_page = LoginPage(driver)
    login_page.login(LoginPageLocators.valid_username, LoginPageLocators.valid_password)
    menu_page = OtherPage(driver)
    menu_page.click_menu_button()
    assert menu_page.is_menu_sidebar_displayed(),"Menu sidebar is not displayed"
    menu_page.go_to_all_item()
    #assert not menu_page.is_menu_sidebar_displayed(),"Menu sidebar is still displayed"
    #assert menu_page.is_menu_button_displayed(),"Menu button is not displayed"

