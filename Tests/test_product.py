import pytest

from Locators.alllocators import LoginPageLocators, ProductPageLocators
from Pages.LoginPage import LoginPage

from Pages.ProductPage import ProductPage


@pytest.fixture()
def login_and_go_to_product_page(driver):
    login_page = LoginPage(driver)
    login_page.login(LoginPageLocators.valid_username, LoginPageLocators.valid_password)
    product_page = ProductPage(driver)
    print("User is in Product Page")
    return product_page
@pytest.mark.order(4)
def test_product_title(login_and_go_to_product_page):
    print("Product Title Test")
    assert login_and_go_to_product_page.get_page_title() == "Products",f"Product title should be visible after clicking show product button: Got title:{login_and_go_to_product_page.get_page_title().text}"

@pytest.mark.order(5)
def test_product_url(login_and_go_to_product_page):
    assert login_and_go_to_product_page.get_current_url()==ProductPageLocators.ProductPageUrl,f"Got{login_and_go_to_product_page.get_current_url()} Expected:{ProductPageLocators.ProductPageUrl}"
@pytest.mark.order(6)
def test_item_count(login_and_go_to_product_page):
    print("Item Total Count of items at product Page Test")
    product_page = login_and_go_to_product_page
    assert product_page.get_item_count()==6,f"Total item count should be 6: Got {product_page.get_item_count()}"
    assert product_page.is_displayed(ProductPageLocators.title_path)
    assert product_page.is_displayed(ProductPageLocators.cart_button_path)
    assert product_page.is_displayed(ProductPageLocators.select_filter_path)
@pytest.mark.order(7)
def test_add_remove_all_items(login_and_go_to_product_page):
    print("Adding All Items Test")
    product_page = login_and_go_to_product_page
    product_page.add_all_item()
    assert product_page.get_cart_count()== 6,f"Total cart item count should be 6: Got {product_page.get_cart_count()}"
    print("All Items added successfully")
    print("Removing All Items Test")
    product_page.remove_all_item()
    assert product_page.get_cart_count() == 0, f"Total cart item count should be 0: Got {product_page.get_cart_count()}"
    print("All Items Removed successfully")
@pytest.mark.order(8)
def test_add_item_and_remove_item(login_and_go_to_product_page):
    print("Adding single Item ")
    product_page =login_and_go_to_product_page
    product_page.add_single_item(ProductPageLocators.add_back_pack_path)
    assert product_page.get_cart_count() == 1,f"Expected 1 items in the cart counter. Got {product_page.get_cart_count()}"
    print("Item added successfully")
    print("Adding 2nd Item ")
    product_page.add_single_item(ProductPageLocators.add_Jacket_path)
    assert product_page.get_cart_count() == 2,f"Expected 2 items in the cart counter.Got {product_page.get_cart_count()}"
    print("Item added successfully")
    print("Removing single Item ")
    product_page.remove_single_item(ProductPageLocators.remove_back_pack_path)
    assert product_page.get_cart_count() == 1,f"Expected 1 items in the cart counter.Got {product_page.get_cart_count()}"
    print("Item Removed successfully")
    print("Removing 2nd Item ")
    product_page.remove_single_item(ProductPageLocators.remove_Jacket_path)
    assert product_page.get_cart_count() == 0,f"Expected 0 items in the cart counter.Got {product_page.get_cart_count()}"
    print("Item Removed successfully Cart item reset to 0")
@pytest.mark.order(9)
def test_sorting(login_and_go_to_product_page):
    print("Sorting Test")
    product_page = login_and_go_to_product_page
    print("By Default Sorting: it is in Name(A to Z)")
    item_name = product_page.get_all_items_names()
    result = product_page.is_sorted_ascending(item_name)
    assert result == True, "By Default: Item are not sorted according to Name(A to Z)"
    print("Sorting According to Name(Z to A)")
    product_page.select_filter_button("Name (Z to A)")
    item_name=product_page.get_all_items_names()
    result=product_page.is_sorted_descending(item_name)
    assert result==True,"Item are not sorted according to Name(Z to A)"
    print("Sorting According to Price(low to high)")
    product_page.select_filter_button("Price (low to high)")
    item_price = product_page.get_all_items_price()
    result = product_page.is_sorted_ascending(item_price)
    assert result == True, "Item are not sorted according to Price(low to high)"
    print("Sorting According to Price(high to low)")
    product_page.select_filter_button("Price (high to low)")
    item_price = product_page.get_all_items_price()
    result = product_page.is_sorted_descending(item_price)
    assert result == True, "Item are not sorted according to Price(high to low)"
    print("Sorting According to Name(A to Z)")
    product_page.select_filter_button("Name (A to Z)")
    item_name = product_page.get_all_items_names()
    result = product_page.is_sorted_ascending(item_name)
    assert result == True, "Item are not sorted according to Name(A to Z)"
@pytest.mark.order(10)
@pytest.mark.parametrize("sort_option,expected_result", [("Name (A to Z)","ascending"),("Name (Z to A)","descending"),
                                                         ("Price (low to high)","ascending"),("Price (high to low)","descending"),])
def test_sorting_using_parametrize(login_and_go_to_product_page,sort_option,expected_result):
    product_page=login_and_go_to_product_page
    product_page.select_filter_button(sort_option)
    if "Name" in sort_option:
        items=product_page.get_all_items_names()
    else:
        items=product_page.get_all_items_price()
    if expected_result == "ascending":
        assert product_page.is_sorted_ascending(items)
    else:
        assert product_page.is_sorted_descending(items)

@pytest.mark.order(11)
def test_click_to_cart_button(login_and_go_to_product_page):
    print("Test Going to cart Inventory")
    product_page = login_and_go_to_product_page
    product_page.click_on_cart_button()
    print(f"User is in Url: {product_page.get_current_url()}")
    assert "cart" in product_page.get_current_url(),f"Cart page not found: found url:{product_page.get_current_url()}"


