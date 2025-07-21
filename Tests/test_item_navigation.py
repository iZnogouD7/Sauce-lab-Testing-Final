import pytest
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from Locators.alllocators import LoginPageLocators, ProductPageLocators
from Pages.LoginPage import LoginPage
from Pages.ProductPage import ProductPage
from Pages.CartPage import CartPage


def load_item_list():
    """Load test data with proper mapping to actual locators"""
    test_data = [
        ("Sauce Labs Backpack", ProductPageLocators.add_back_pack_path,
         ProductPageLocators.title_back_pack_path, ProductPageLocators.img_back_pack_path, 29.99,
         "carry.allTheThings()"),
        ("Sauce Labs Bike Light", ProductPageLocators.add_bike_light_path,
         ProductPageLocators.title_bike_light_path, ProductPageLocators.img_bike_light_path, 9.99, "illuminate"),
        ("Sauce Labs Fleece Jacket", ProductPageLocators.add_Jacket_path,
         ProductPageLocators.title_Jacket_path, ProductPageLocators.img_Jacket_path, 49.99, "fleece"),
        ("Sauce Labs Bolt T-Shirt", ProductPageLocators.add_Tshirt_path,
         ProductPageLocators.title_Tshirt_path, ProductPageLocators.img_Tshirt_path, 15.99, "bolt"),
        ("Sauce Labs Onesie", ProductPageLocators.add_onesie_path,
         ProductPageLocators.title_onesie_path, ProductPageLocators.img_onesie_path, 7.99, "onesie"),
        ("Test.allTheThings() T-Shirt (Red)", ProductPageLocators.add_allthings_path,
         ProductPageLocators.title_allthing_path, ProductPageLocators.img_allthing_path, 15.99, "allTheThings")
    ]
    return test_data


@pytest.fixture()
def login_to_product_page(driver):
    """Login and navigate to product page with proper wait"""
    login_page = LoginPage(driver)
    login_page.login(LoginPageLocators.valid_username, LoginPageLocators.valid_password)

    # Wait for inventory page to load
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "inventory_item")))

    return ProductPage(driver)


def wait_for_page_load(driver, timeout=10):
    """Wait for inventory page to fully load"""
    wait = WebDriverWait(driver, timeout)
    try:
        # Wait for inventory items to be present
        wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "inventory_item")))
        time.sleep(1)  # Additional small wait for JS to complete
        return True
    except Exception as e:
        print(f"Page load timeout: {e}")
        return False


@pytest.mark.parametrize("item_name,add_locator,title_locator,img_locator,expected_price,expected_desc",
                         load_item_list())
def test_item_title_navigation(driver, item_name, add_locator, title_locator, img_locator, expected_price,
                               expected_desc):
    """Test clicking item title to navigate to detail page for all items"""
    # Login
    login_page = LoginPage(driver)
    login_page.login(LoginPageLocators.valid_username, LoginPageLocators.valid_password)

    # Wait for page to load completely
    assert wait_for_page_load(driver), "Inventory page failed to load properly"

    product_page = ProductPage(driver)

    # Debug information
    print(f"Testing item: {item_name}")
    print(f"Current URL: {driver.current_url}")

    # Get item details using the specific locator instead of searching by name
    try:
        # Get item details from inventory page using specific locators
        inventory_details = product_page.get_item_details_by_locator(title_locator, add_locator)

        # Click on the specific item title using the locator
        title_element = driver.find_element(*title_locator)
        title_element.click()

        # Wait for navigation to detail page
        wait = WebDriverWait(driver, 10)
        wait.until(lambda d: "inventory-item" in d.current_url)

    except Exception as e:
        print(f"Error during item interaction: {e}")
        driver.save_screenshot(f"debug_error_{item_name.replace(' ', '_')}.png")
        raise

    # Verify navigation and details
    assert product_page.is_on_item_detail_page(), f"Should be on detail page for {item_name}"
    detail_details = product_page.get_item_details_from_detail_page()
    assert product_page.verify_item_details_match(inventory_details, detail_details), \
        f"Details should match for {item_name}"


@pytest.mark.parametrize("item_name,add_locator,title_locator,img_locator,expected_price,expected_desc",
                         load_item_list())
def test_item_image_navigation(driver, item_name, add_locator, title_locator, img_locator, expected_price,
                               expected_desc):
    """Test clicking item image to navigate to detail page for all items"""
    # Login
    login_page = LoginPage(driver)
    login_page.login(LoginPageLocators.valid_username, LoginPageLocators.valid_password)

    # Wait for page to load
    assert wait_for_page_load(driver), "Inventory page failed to load properly"

    product_page = ProductPage(driver)

    # Get details using specific locator and click image
    inventory_details = product_page.get_item_details_by_locator(title_locator, add_locator)

    # Click the specific image
    img_element = driver.find_element(*img_locator)
    img_element.click()

    # Wait for navigation
    wait = WebDriverWait(driver, 10)
    wait.until(lambda d: "inventory-item" in d.current_url)

    # Verify navigation and details
    assert product_page.is_on_item_detail_page(), f"Should be on detail page for {item_name}"
    detail_details = product_page.get_item_details_from_detail_page()
    assert product_page.verify_item_details_match(inventory_details, detail_details), \
        f"Details should match for {item_name}"


@pytest.mark.parametrize("item_name,add_locator,title_locator,img_locator,expected_price,expected_desc",
                         load_item_list())
def test_add_remove_from_detail_page(driver, item_name, add_locator, title_locator, img_locator, expected_price,
                                     expected_desc):
    """Test adding and removing items from detail page for all items"""
    # Login and navigate to detail page
    login_page = LoginPage(driver)
    login_page.login(LoginPageLocators.valid_username, LoginPageLocators.valid_password)

    assert wait_for_page_load(driver), "Inventory page failed to load properly"

    product_page = ProductPage(driver)

    # Click on title to navigate to detail page
    title_element = driver.find_element(*title_locator)
    title_element.click()

    # Wait for detail page to load
    wait = WebDriverWait(driver, 10)
    wait.until(lambda d: "inventory-item" in d.current_url)

    # Test add/remove functionality
    initial_cart_count = product_page.get_cart_count()

    # Add item from detail page
    product_page.add_item_from_detail_page()
    time.sleep(1)  # Wait for cart update
    new_cart_count = product_page.get_cart_count()
    assert new_cart_count == initial_cart_count + 1, \
        f"Cart count should increase by 1 for {item_name}"

    # Remove item from detail page
    product_page.remove_item_from_detail_page()
    time.sleep(1)  # Wait for cart update
    final_cart_count = product_page.get_cart_count()
    assert final_cart_count == initial_cart_count, \
        f"Cart count should return to initial value for {item_name}"


@pytest.mark.parametrize("item_name,add_locator,title_locator,img_locator,expected_price,expected_desc",
                         load_item_list())
def test_item_verification_in_cart(driver, item_name, add_locator, title_locator, img_locator, expected_price,
                                   expected_desc):
    """Test item details verification in cart for all items"""
    # Login and add item
    login_page = LoginPage(driver)
    login_page.login(LoginPageLocators.valid_username, LoginPageLocators.valid_password)

    assert wait_for_page_load(driver), "Inventory page failed to load properly"

    product_page = ProductPage(driver)
    product_page.add_single_item(add_locator)

    # Wait for cart update
    time.sleep(1)

    product_page.click_on_cart_button()

    # Wait for cart page to load
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "cart_item")))

    # Verify item in cart
    cart_page = CartPage(driver)
    cart_items = cart_page.get_cart_items()

    assert len(cart_items) >= 1, f"Cart should have at least 1 item after adding {item_name}"

    # Find the added item in cart
    added_item = None
    for item in cart_items:
        if item['name'] == item_name:
            added_item = item
            break

    assert added_item is not None, f"Item {item_name} should be in cart"
    assert added_item['price'] == f"${expected_price}", \
        f"Expected price {expected_price} for {item_name}, got {added_item['price']}"
    assert expected_desc in added_item['desc'], \
        f"Expected description to contain '{expected_desc}' for {item_name}"


@pytest.mark.parametrize("item_name,add_locator,title_locator,img_locator,expected_price,expected_desc",
                         load_item_list())
def test_cart_item_navigation(driver, item_name, add_locator, title_locator, img_locator, expected_price,
                              expected_desc):
    """Test navigation from cart item to detail page for all items"""
    # Login, add item, and go to cart
    login_page = LoginPage(driver)
    login_page.login(LoginPageLocators.valid_username, LoginPageLocators.valid_password)

    assert wait_for_page_load(driver), "Inventory page failed to load properly"

    product_page = ProductPage(driver)
    product_page.add_single_item(add_locator)
    time.sleep(1)  # Wait for cart update

    product_page.click_on_cart_button()

    # Wait for cart page
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "cart_item")))

    # Navigate from cart to detail page
    cart_page = CartPage(driver)
    cart_page.click_item_title_in_cart(item_name)

    # Wait for navigation
    time.sleep(2)

    # Verify navigation
    assert product_page.is_on_item_detail_page(), \
        f"Should navigate to detail page from cart for {item_name}"

    # Test back navigation
    product_page.click_back_to_product()
    time.sleep(1)
    assert "inventory.html" in product_page.get_current_url(), \
        f"Should navigate back to inventory page for {item_name}"


def test_comprehensive_multi_item_workflow(driver):
    """Test workflow with multiple items from test data"""
    # Login
    login_page = LoginPage(driver)
    login_page.login(LoginPageLocators.valid_username, LoginPageLocators.valid_password)

    assert wait_for_page_load(driver), "Inventory page failed to load properly"

    product_page = ProductPage(driver)

    # Load test data and add first 3 items
    test_data = load_item_list()[:3]  # Limit to first 3 items for comprehensive test

    # Add multiple items using their specific locators
    for item_name, add_locator, title_locator, img_locator, expected_price, expected_desc in test_data:
        product_page.add_single_item(add_locator)
        time.sleep(1)  # Wait between additions

    # Verify cart
    product_page.click_on_cart_button()

    # Wait for cart page
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "cart_item")))

    cart_page = CartPage(driver)
    cart_items = cart_page.get_cart_items()

    assert len(cart_items) == len(test_data), \
        f"Cart should have {len(test_data)} items"

    # Verify each item in cart
    cart_item_names = [item['name'] for item in cart_items]
    for item_name, _, _, _, expected_price, _ in test_data:
        assert item_name in cart_item_names, f"{item_name} should be in cart"

    # Remove all items
    cart_page.remove_all_items_from_cart()
    time.sleep(2)  # Wait for removal
    assert cart_page.verify_cart_is_empty(), "Cart should be empty after removing all items"


def test_back_to_products_navigation(login_to_product_page):
    """Test back to products button functionality"""
    product_page = login_to_product_page

    # Use first item from test data
    test_data = load_item_list()
    item_name, add_locator, title_locator, img_locator, expected_price, expected_desc = test_data[0]

    # Navigate to detail page using specific locator
    title_element = product_page.driver.find_element(*title_locator)
    title_element.click()

    # Wait for navigation
    wait = WebDriverWait(product_page.driver, 10)
    wait.until(lambda d: "inventory-item" in d.current_url)

    assert product_page.is_on_item_detail_page(), "Should be on item detail page"

    product_page.click_back_to_product()
    time.sleep(1)
    assert "inventory.html" in product_page.get_current_url(), \
        "Should be back on inventory page"


# Alternative approach: Create a simplified test using direct locators
def test_direct_locator_navigation(driver):
    """Test using direct locators instead of searching by name"""
    # Login
    login_page = LoginPage(driver)
    login_page.login(LoginPageLocators.valid_username, LoginPageLocators.valid_password)

    assert wait_for_page_load(driver), "Inventory page failed to load properly"

    # Test backpack item directly
    print("Testing backpack navigation using direct locators")

    # Click backpack title
    backpack_title = driver.find_element(*ProductPageLocators.title_back_pack_path)
    backpack_title.click()

    # Wait for navigation
    wait = WebDriverWait(driver, 10)
    wait.until(lambda d: "inventory-item" in d.current_url)

    # Verify we're on detail page
    assert "inventory-item" in driver.current_url, "Should be on item detail page"

    # Go back to products
    back_button = driver.find_element(*ProductPageLocators.back_to_product)
    back_button.click()

    time.sleep(1)
    assert "inventory.html" in driver.current_url, "Should be back on inventory page"

    print("Direct locator test passed")


# import pytest
# import csv
# import os
# from Locators.alllocators import LoginPageLocators, ProductPageLocators
# from Pages.LoginPage import LoginPage
# from Pages.ProductPage import ProductPage
# from Pages.CartPage import CartPage
#
#
# # def load_test_data_from_csv():
#     # """Load test data from CSV file"""
#     # csv_file = "test_items.csv"
#     # test_data = []
#     #
#     # if os.path.exists(csv_file):
#     #     with open(csv_file, 'r') as file:
#     #         reader = csv.DictReader(file)
#     #         for row in reader:
#     #             test_data.append((
#     #                 row['item_name'],
#     #                 getattr(ProductPageLocators, row['add_button_locator']),
#     #                 float(row['expected_price']),
#     #                 row['expected_desc_contains']
#     #             ))
#     # else:
#         # Fallback data if CSV doesn't exist
# def load_item_list():
#     test_data = [
#             ("Sauce Labs Backpack", ProductPageLocators.add_back_pack_path, 29.99, "carry.allTheThings()"),
#             ("Sauce Labs Bike Light", ProductPageLocators.add_bike_light_path, 9.99, "illuminate"),
#             ("Sauce Labs Fleece Jacket", ProductPageLocators.add_Jacket_path, 49.99, "fleece"),
#         ("Sauce Labs Bolt T - Shirt",ProductPageLocators.add_Tshirt_path, 15.99, "bolt"),
#         ("Sauce Labs Onesie", ProductPageLocators.add_onesie_path, 7.99, "onesie"),
#         ("Test.allTheThings() T - Shirt(Red)", ProductPageLocators.add_allthings_path, 15.99, "allTheThings")
#         ]
#
#     return test_data
#
#
# @pytest.fixture()
# def login_to_product_page(driver):
#     """Login and navigate to product page"""
#     login_page = LoginPage(driver)
#     login_page.login(LoginPageLocators.valid_username, LoginPageLocators.valid_password)
#     return ProductPage(driver)
#
#
# @pytest.mark.parametrize("item_name,add_locator,expected_price,expected_desc", load_item_list())
# def test_item_title_navigation(driver, item_name, add_locator, expected_price, expected_desc):
#     """Test clicking item title to navigate to detail page for all items"""
#     # Login
#     login_page = LoginPage(driver)
#     login_page.login(LoginPageLocators.valid_username, LoginPageLocators.valid_password)
#     product_page = ProductPage(driver)
#
#     # Get item details from inventory and click title
#     inventory_details = product_page.get_item_details_from_inventory(item_name)
#     product_page.click_item_by_name(item_name)
#
#     # Verify navigation and details
#     assert product_page.is_on_item_detail_page(), f"Should be on detail page for {item_name}"
#     detail_details = product_page.get_item_details_from_detail_page()
#     assert product_page.verify_item_details_match(inventory_details, detail_details), \
#         f"Details should match for {item_name}"
#
#
# @pytest.mark.parametrize("item_name,add_locator,expected_price,expected_desc", load_item_list())
# def test_item_image_navigation(driver, item_name, add_locator, expected_price, expected_desc):
#     """Test clicking item image to navigate to detail page for all items"""
#     # Login
#     login_page = LoginPage(driver)
#     login_page.login(LoginPageLocators.valid_username, LoginPageLocators.valid_password)
#     product_page = ProductPage(driver)
#
#     # Get details and click image
#     inventory_details = product_page.get_item_details_from_inventory(item_name)
#     product_page.click_item_image_by_name(item_name)
#
#     # Verify navigation and details
#     assert product_page.is_on_item_detail_page(), f"Should be on detail page for {item_name}"
#     detail_details = product_page.get_item_details_from_detail_page()
#     assert product_page.verify_item_details_match(inventory_details, detail_details), \
#         f"Details should match for {item_name}"
#
#
# @pytest.mark.parametrize("item_name,add_locator,expected_price,expected_desc", load_item_list())
# def test_add_remove_from_detail_page(driver, item_name, add_locator, expected_price, expected_desc):
#     """Test adding and removing items from detail page for all items"""
#     # Login and navigate to detail page
#     login_page = LoginPage(driver)
#     login_page.login(LoginPageLocators.valid_username, LoginPageLocators.valid_password)
#     product_page = ProductPage(driver)
#
#     product_page.click_item_by_name(item_name)
#
#     # Test add/remove functionality
#     initial_cart_count = product_page.get_cart_count()
#
#     # Add item
#     product_page.add_item_from_detail_page()
#     new_cart_count = product_page.get_cart_count()
#     assert new_cart_count == initial_cart_count + 1, \
#         f"Cart count should increase by 1 for {item_name}"
#
#     # Remove item
#     product_page.remove_item_from_detail_page()
#     final_cart_count = product_page.get_cart_count()
#     assert final_cart_count == initial_cart_count, \
#         f"Cart count should return to initial value for {item_name}"
#
#
# @pytest.mark.parametrize("item_name,add_locator,expected_price,expected_desc", load_item_list())
# def test_item_verification_in_cart(driver, item_name, add_locator, expected_price, expected_desc):
#     """Test item details verification in cart for all items"""
#     # Login and add item
#     login_page = LoginPage(driver)
#     login_page.login(LoginPageLocators.valid_username, LoginPageLocators.valid_password)
#     product_page = ProductPage(driver)
#
#     product_page.add_single_item(add_locator)
#     product_page.click_on_cart_button()
#
#     # Verify item in cart
#     cart_page = CartPage(driver)
#     cart_items = cart_page.get_cart_items()
#
#     assert len(cart_items) >= 1, f"Cart should have at least 1 item after adding {item_name}"
#
#     # Find the added item in cart
#     added_item = None
#     for item in cart_items:
#         if item['name'] == item_name:
#             added_item = item
#             break
#
#     assert added_item is not None, f"Item {item_name} should be in cart"
#     assert added_item['price'] == expected_price, \
#         f"Expected price {expected_price} for {item_name}, got {added_item['price']}"
#     assert expected_desc in added_item['desc'], \
#         f"Expected description to contain '{expected_desc}' for {item_name}"
#
#
# @pytest.mark.parametrize("item_name,add_locator,expected_price,expected_desc", load_item_list())
# def test_cart_item_navigation(driver, item_name, add_locator, expected_price, expected_desc):
#     """Test navigation from cart item to detail page for all items"""
#     # Login, add item, and go to cart
#     login_page = LoginPage(driver)
#     login_page.login(LoginPageLocators.valid_username, LoginPageLocators.valid_password)
#     product_page = ProductPage(driver)
#
#     product_page.add_single_item(add_locator)
#     product_page.click_on_cart_button()
#
#     # Navigate from cart to detail page
#     cart_page = CartPage(driver)
#     cart_page.click_item_title_in_cart(item_name)
#
#     # Verify navigation
#     assert product_page.is_on_item_detail_page(), \
#         f"Should navigate to detail page from cart for {item_name}"
#
#     # Test back navigation
#     product_page.click_back_to_product()
#     assert "inventory.html" in product_page.get_current_url(), \
#         f"Should navigate back to inventory page for {item_name}"
#
#
# def test_comprehensive_multi_item_workflow(driver):
#     """Test workflow with multiple items from CSV data"""
#     # Login
#     login_page = LoginPage(driver)
#     login_page.login(LoginPageLocators.valid_username, LoginPageLocators.valid_password)
#     product_page = ProductPage(driver)
#
#     # Load test data and add first 3 items
#     test_data = load_item_list()[:3]  # Limit to first 3 items for comprehensive test
#
#     # Add multiple items
#     for item_name, add_locator, expected_price, expected_desc in test_data:
#         product_page.add_single_item(add_locator)
#
#     # Verify cart
#     product_page.click_on_cart_button()
#     cart_page = CartPage(driver)
#     cart_items = cart_page.get_cart_items()
#
#     assert len(cart_items) == len(test_data), \
#         f"Cart should have {len(test_data)} items"
#
#     # Verify each item in cart
#     cart_item_names = [item['name'] for item in cart_items]
#     for item_name, _, expected_price, _ in test_data:
#         assert item_name in cart_item_names, f"{item_name} should be in cart"
#
#     # Remove all items
#     cart_page.remove_all_items_from_cart()
#     assert cart_page.verify_cart_is_empty(), "Cart should be empty after removing all items"
#
#
# def test_back_to_products_navigation(login_to_product_page):
#     """Test back to products button functionality"""
#     product_page = login_to_product_page
#
#     # Use first item from test data
#     test_data = load_item_list()
#     item_name = test_data[0][0]
#
#     # Navigate to detail page and back
#     product_page.click_item_by_name(item_name)
#     assert product_page.is_on_item_detail_page(), "Should be on item detail page"
#
#     product_page.click_back_to_product()
#     assert "inventory.html" in product_page.get_current_url(), \
#         "Should be back on inventory page"
#
#
#
# # # New comprehensive test file: test_item_navigation.py
# # import pytest
# # import time
# # from Locators.alllocators import LoginPageLocators, ProductPageLocators
# # from Pages.LoginPage import LoginPage
# # from Pages.ProductPage import ProductPage
# # from Pages.CartPage import CartPage
# #
# #
# # @pytest.fixture()
# # def login_to_product_page(driver):
# #     login_page = LoginPage(driver)
# #     login_page.login(LoginPageLocators.valid_username, LoginPageLocators.valid_password)
# #     product_page = ProductPage(driver)
# #     print("User logged in and on product page")
# #     return product_page
# #
# #
# # @pytest.fixture()
# # def setup_cart_with_items(driver):
# #     login_page = LoginPage(driver)
# #     login_page.login(LoginPageLocators.valid_username, LoginPageLocators.valid_password)
# #     product_page = ProductPage(driver)
# #
# #     # Add multiple items to cart
# #     product_page.add_single_item(ProductPageLocators.add_back_pack_path)
# #     product_page.add_single_item(ProductPageLocators.add_Jacket_path)
# #     product_page.click_on_cart_button()
# #
# #     cart_page = CartPage(driver)
# #     print("Cart setup with items")
# #     return cart_page, product_page
# #
# #
# # def test_click_item_title_navigation(login_to_product_page):
# #     """Test clicking item title to navigate to detail page"""
# #     print("Testing item title click navigation")
# #     product_page = login_to_product_page
# #
# #     # Get item details from inventory page
# #     item_name = "Sauce Labs Backpack"  # Adjust based on your actual item names
# #     inventory_details = product_page.get_item_details_from_inventory(item_name)
# #
# #     # Click on item title
# #     product_page.click_item_by_name(item_name)
# #     time.sleep(2)
# #
# #     # Verify navigation to detail page
# #     assert product_page.is_on_item_detail_page(), "Should be on item detail page"
# #
# #     # Get details from detail page and verify they match
# #     detail_page_details = product_page.get_item_details_from_detail_page()
# #     assert product_page.verify_item_details_match(inventory_details, detail_page_details), \
# #         "Item details should match between inventory and detail pages"
# #
# #     print("Item title navigation test passed")
# #
# #
# # def test_click_item_image_navigation(login_to_product_page):
# #     """Test clicking item image to navigate to detail page"""
# #     print("Testing item image click navigation")
# #     product_page = login_to_product_page
# #
# #     item_name = "Sauce Labs Bike Light"  # Adjust based on your actual item names
# #     inventory_details = product_page.get_item_details_from_inventory(item_name)
# #
# #     # Click on item image
# #     product_page.click_item_image_by_name(item_name)
# #     time.sleep(2)
# #
# #     # Verify navigation and details match
# #     assert product_page.is_on_item_detail_page(), "Should be on item detail page"
# #     detail_page_details = product_page.get_item_details_from_detail_page()
# #     assert product_page.verify_item_details_match(inventory_details, detail_page_details), \
# #         "Item details should match between inventory and detail pages"
# #
# #     print("Item image navigation test passed")
# #
# #
# # def test_add_remove_from_detail_page(login_to_product_page):
# #     """Test adding and removing items from detail page"""
# #     print("Testing add/remove from detail page")
# #     product_page = login_to_product_page
# #
# #     # Navigate to item detail page
# #     item_name = "Sauce Labs Backpack"
# #     product_page.click_item_by_name(item_name)
# #     time.sleep(1)
# #
# #     # Test adding item
# #     initial_cart_count = product_page.get_cart_count()
# #     product_page.add_item_from_detail_page()
# #     time.sleep(1)
# #
# #     new_cart_count = product_page.get_cart_count()
# #     assert new_cart_count == initial_cart_count + 1, \
# #         f"Cart count should increase by 1. Expected: {initial_cart_count + 1}, Got: {new_cart_count}"
# #
# #     # Test removing item
# #     product_page.remove_item_from_detail_page()
# #     time.sleep(1)
# #
# #     final_cart_count = product_page.get_cart_count()
# #     assert final_cart_count == initial_cart_count, \
# #         f"Cart count should return to initial value. Expected: {initial_cart_count}, Got: {final_cart_count}"
# #
# #     print("Add/remove from detail page test passed")
# #
# #
# # def test_back_to_products_navigation(login_to_product_page):
# #     """Test back to products button functionality"""
# #     print("Testing back to products navigation")
# #     product_page = login_to_product_page
# #
# #     # Navigate to item detail page
# #     product_page.click_item_by_name("Sauce Labs Backpack")
# #     time.sleep(1)
# #     assert product_page.is_on_item_detail_page(), "Should be on item detail page"
# #
# #     # Click back to products
# #     product_page.click_back_to_product()
# #     time.sleep(1)
# #
# #     # Verify back on inventory page
# #     assert "inventory.html" in product_page.get_current_url(), \
# #         f"Should be back on inventory page. Current URL: {product_page.get_current_url()}"
# #
# #     print("Back to products navigation test passed")
# #
# #
# # def test_cart_item_removal(setup_cart_with_items):
# #     """Test removing items from cart page"""
# #     print("Testing cart item removal")
# #     cart_page, product_page = setup_cart_with_items
# #
# #     # Get initial cart items
# #     initial_cart_items = cart_page.get_cart_items()
# #     initial_count = len(initial_cart_items)
# #     assert initial_count > 0, "Cart should have items"
# #
# #     # Remove one item
# #     item_to_remove = initial_cart_items[0]['name']
# #     cart_page.remove_item_by_name(item_to_remove)
# #     time.sleep(1)
# #
# #     # Verify item was removed
# #     remaining_items = cart_page.get_cart_items()
# #     assert len(remaining_items) == initial_count - 1, \
# #         f"Cart should have one less item. Expected: {initial_count - 1}, Got: {len(remaining_items)}"
# #
# #     # Verify specific item was removed
# #     remaining_names = [item['name'] for item in remaining_items]
# #     assert item_to_remove not in remaining_names, f"Item {item_to_remove} should be removed from cart"
# #
# #     print("Cart item removal test passed")
# #
# #
# # def test_cart_item_title_navigation(setup_cart_with_items):
# #     """Test clicking item title in cart to navigate to detail page"""
# #     print("Testing cart item title navigation")
# #     cart_page, product_page = setup_cart_with_items
# #
# #     # Get cart items
# #     cart_items = cart_page.get_cart_items()
# #     assert len(cart_items) > 0, "Cart should have items"
# #
# #     # Click on first item title
# #     item_name = cart_items[0]['name']
# #     cart_details = cart_page.get_item_details_from_cart(item_name)
# #
# #     cart_page.click_item_title_in_cart(item_name)
# #     time.sleep(2)
# #
# #     # Verify navigation to detail page
# #     assert product_page.is_on_item_detail_page(), "Should navigate to item detail page"
# #
# #     # Verify item details match
# #     detail_page_details = product_page.get_item_details_from_detail_page()
# #     assert cart_details['name'] == detail_page_details['name'], "Item names should match"
# #     assert cart_details['price'] == detail_page_details['price'], "Item prices should match"
# #
# #     print("Cart item title navigation test passed")
# #
# #
# # def test_cart_item_image_navigation(setup_cart_with_items):
# #     """Test clicking item image in cart to navigate to detail page"""
# #     print("Testing cart item image navigation")
# #     cart_page, product_page = setup_cart_with_items
# #
# #     # Get cart items
# #     cart_items = cart_page.get_cart_items()
# #     assert len(cart_items) > 0, "Cart should have items"
# #
# #     # Click on first item image
# #     item_name = cart_items[0]['name']
# #     cart_page.click_item_image_in_cart(item_name)
# #     time.sleep(2)
# #
# #     # Verify navigation to detail page
# #     assert product_page.is_on_item_detail_page(), "Should navigate to item detail page from cart image"
# #
# #     print("Cart item image navigation test passed")
# #
# #
# # def test_remove_all_items_from_cart(setup_cart_with_items):
# #     """Test removing all items from cart"""
# #     print("Testing remove all items from cart")
# #     cart_page, product_page = setup_cart_with_items
# #
# #     # Verify cart has items initially
# #     initial_items = cart_page.get_cart_items()
# #     assert len(initial_items) > 0, "Cart should have items initially"
# #
# #     # Remove all items
# #     cart_page.remove_all_items_from_cart()
# #     time.sleep(2)
# #
# #     # Verify cart is empty
# #     assert cart_page.verify_cart_is_empty(), "Cart should be empty after removing all items"
# #     assert cart_page.get_cart_count() == 0, "Cart count should be 0"
# #
# #     print("Remove all items from cart test passed")
# #
# #
# # def test_comprehensive_item_journey(login_to_product_page):
# #     """Test complete user journey: inventory -> detail -> cart -> detail -> back"""
# #     print("Testing comprehensive item journey")
# #     product_page = login_to_product_page
# #
# #     # Step 1: Click item from inventory page
# #     item_name = "Sauce Labs Backpack"
# #     inventory_details = product_page.get_item_details_from_inventory(item_name)
# #     product_page.click_item_by_name(item_name)
# #     time.sleep(1)
# #
# #     # Step 2: Verify detail page and add to cart
# #     assert product_page.is_on_item_detail_page(), "Should be on detail page"
# #     detail_details = product_page.get_item_details_from_detail_page()
# #     assert product_page.verify_item_details_match(inventory_details, detail_details), "Details should match"
# #
# #     product_page.add_item_from_detail_page()
# #     assert product_page.get_cart_count() == 1, "Cart should have 1 item"
# #
# #     # Step 3: Go to cart and verify item
# #     product_page.click_on_cart_button()
# #     time.sleep(1)
# #     cart_page = CartPage
# #     cart_items = cart_page.get_cart_items()
# #     assert len(cart_items) == 1, "Cart should have 1 item"
# #     assert cart_items[0]['name'] == item_name, "Cart item should match added item"
# #
# #     # Step 4: Click item in cart to go back to detail page
# #     cart_page.click_item_title_in_cart(item_name)
# #     time.sleep(1)
# #     assert product_page.is_on_item_detail_page(), "Should be back on detail page"
# #
# #     # Step 5: Remove item and go back to inventory
# #     product_page.remove_item_from_detail_page()
# #     assert product_page.get_cart_count() == 0, "Cart should be empty after removal"
# #
# #     product_page.click_back_to_product()
# #     time.sleep(1)
# #     assert "inventory.html" in product_page.get_current_url(), "Should be back on inventory page"
# #
# #     print("Comprehensive item journey test passed")
# #
