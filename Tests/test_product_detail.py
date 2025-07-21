import pytest

from Locators.alllocators import LoginPageLocators, ProductPageLocators
from Pages.LoginPage import LoginPage
from Pages.ProductPage import ProductPage


@pytest.fixture()
def go_to_product_details(driver):
    login_page = LoginPage(driver)
    login_page.login(LoginPageLocators.valid_username, LoginPageLocators.valid_password)
    product_page = ProductPage(driver)
    product_page.click_element(ProductPageLocators.title_back_pack_path)
    return product_page
@pytest.mark.order(12)
def test_product_details(go_to_product_details):
    product_page = go_to_product_details
    assert "inventory-item" in product_page.get_current_url(),f"Not on Product details page: Got Url:{product_page.get_current_url()}"
    assert product_page.is_displayed(ProductPageLocators.backpack_name_detail),"Product name is not displayed"
    assert product_page.is_displayed(ProductPageLocators.backpack_image_detail), "Product image is not displayed"
    assert product_page.is_displayed(ProductPageLocators.backpack_desc_detail), "Product description is not displayed"
    assert product_page.is_displayed(ProductPageLocators.backpack_price_detail), "Product price is not displayed"
    assert product_page.is_displayed(ProductPageLocators.back_to_product),"Back button is not displayed"
    assert product_page.is_displayed(ProductPageLocators.inventory_add_to_cart_button),"Add to cart button is not displayed"
@pytest.mark.order(12)
def test_add_remove_in_detail_page(go_to_product_details):
    product_page = go_to_product_details
    initial_count=product_page.get_cart_count()
    product_page.click_element(ProductPageLocators.inventory_add_to_cart_button)
    assert product_page.get_cart_count()==initial_count+1,f"Cart count must be {initial_count+1} but got cart count {product_page.get_cart_count()}"
    product_page.click_element(ProductPageLocators.inventory_add_to_remove_button)
    assert product_page.get_cart_count()==initial_count,f"Cart count must be {initial_count} but got cart count {product_page.get_cart_count()}"
@pytest.mark.order(13)
def test_back_to_inventory_page(go_to_product_details):
    product_page = go_to_product_details
    product_page.click_element(ProductPageLocators.back_to_product)
    assert "inventory.html" in product_page.get_current_url(),f"Inventory page is not displayed. Got Url:{product_page.get_current_url()}"