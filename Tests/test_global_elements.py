
import pytest

from Locators.alllocators import LoginPageLocators, ProductPageLocators
from Pages.CartPage import CartPage
from Pages.LoginPage import LoginPage
from Pages.OtherPage import OtherPage
from Pages.ProductPage import ProductPage


@pytest.mark.parametrize("page_url",["/inventory.html","/cart.html","/checkout-step-one.html","/checkout-step-two.html"])
def test_global_elements(driver,page_url):
    login_page = LoginPage(driver)
    login_page.login(LoginPageLocators.valid_username,LoginPageLocators.valid_password)
    driver.get(f"https://www.saucedemo.com{page_url}")
    other_page = OtherPage(driver)
    assert other_page.is_menu_sidebar_displayed(),"Menu Button Not Displayed"
    assert other_page.is_cart_button_displayed(),"Cart Button Not Displayed"
    assert other_page.is_footer_displayed(),"Footer Not Displayed"
    assert other_page.is_copyright_displayed(),"Copyright Not Displayed"
    other_page.click_menu_button()
    other_page.go_to_all_item()
    assert "inventory.html" in other_page.get_current_url(),f"Got url:{other_page.get_current_url()}"

def test_known_verification(driver):
    login_page = LoginPage(driver)
    login_page.login(LoginPageLocators.valid_username,LoginPageLocators.valid_password)
    product_page = ProductPage(driver)
    product_page.add_single_item(ProductPageLocators.add_back_pack_path)
    expected={
        'name':'Sauce Labs Backpack',
        'description': 'carry.allTheThings()',
        'price':29.99,
        'image':'backpack.jpg'
    }
    product_page.click_on_cart_button()
    cart_page = CartPage(driver)
    cart_items = cart_page.get_cart_items()
    assert len(cart_items) == 1, f"Expected 1 item in cart, but found {len(cart_items)}"
    actual_item = cart_items[0]
    print(f"{actual_item}")
    assert actual_item['name'] == expected[
        'name'], f"Expected name '{expected['name']}', but got '{actual_item['name']}'"

    assert expected['description'] in actual_item[
        'description'], f"Expected description to contain '{expected['description']}', but got '{actual_item['description']}'"

    assert actual_item['price'] == f"${expected['price']}", f"Expected price ${expected['price']}, but got {actual_item['price']}"

    # assert expected['image'] in actual_item[
    #     'image'], f"Expected
    #     image to contain '{expected['image']}', but got '{actual_item['image']}'"