from Locators.alllocators import LoginPageLocators, ProductPageLocators
from Pages.LoginPage import LoginPage
from Pages.OtherPage import OtherPage
from Pages.ProductPage import ProductPage


def test_cart_persist_after_refresh(driver):
    print("Test Cart Persist After Refresh")
    login_page = LoginPage(driver)
    login_page.login(LoginPageLocators.valid_username, LoginPageLocators.valid_password)
    product_page = ProductPage(driver)
    product_page.add_single_item(ProductPageLocators.add_back_pack_path)
    initial_count=product_page.get_cart_count()
    product_page.refresh_page()
    product_page=ProductPage(driver)
    assert product_page.get_cart_count() == initial_count,f"Expected {initial_count} items in the cart counter but got {product_page.get_cart_count()}"

def test_cart_persist_after_logout(driver):
    print("Test Cart Persist After Logout")
    login_page = LoginPage(driver)
    login_page.login(LoginPageLocators.valid_username, LoginPageLocators.valid_password)
    product_page = ProductPage(driver)
    product_page.add_single_item(ProductPageLocators.add_back_pack_path)
    initial_count=product_page.get_cart_count()
    menu_page=OtherPage(driver)
    menu_page.click_menu_button()
    menu_page.logout()
    login_page.login(LoginPageLocators.valid_username, LoginPageLocators.valid_password)
    product_page = ProductPage(driver)
    assert product_page.get_cart_count() == initial_count,f"Cart count before logout {initial_count} .cart counter after logging again {product_page.get_cart_count()}"


