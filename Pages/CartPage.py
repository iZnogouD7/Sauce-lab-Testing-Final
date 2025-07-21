from selenium.webdriver.common.by import By

from Locators.alllocators import CartPageLocators, ProductPageLocators
from Pages.BasePage import BasePage


class CartPage(BasePage):
    # def get_cart_page_url(self):
    #     return self.driver.current_url

    def cart_title(self):
        return self.get_text_from_element(CartPageLocators.cart_page_title)

    def click_continue_button(self):
        self.click_element(CartPageLocators.continue_shopping_path)

    def click_checkout_button(self):
        self.click_element(CartPageLocators.checkout_path)

    def get_cart_count(self):
        try:
            return int(self.get_text_from_element(ProductPageLocators.cart_count_path))
        except:
            return 0

    def remove_item(self,locator):
        self.driver.find_element(locator).click()

    # NEW METHODS FOR CART ITEM MANAGEMENT
    def get_cart_items(self):
        """Get all items in cart with their details"""
        cart_items = []
        item_containers = self.find_elements((By.CLASS_NAME, 'cart_item'))

        for container in item_containers:
            item_details = {
                'name': container.find_element(By.CLASS_NAME, 'inventory_item_name').text,
                'description': container.find_element(By.CLASS_NAME, 'inventory_item_desc').text,
                'price': container.find_element(By.CLASS_NAME, 'inventory_item_price').text,
                'quantity': container.find_element(By.CLASS_NAME, 'cart_quantity').text,
                'remove_button': container.find_element(By.XPATH, ".//button[starts-with(@id, 'remove-')]")
            }
            cart_items.append(item_details)

        return cart_items

    def remove_item_by_name(self, item_name):
        """Remove specific item from cart by name"""
        remove_button_locator = (By.XPATH,
                                 f"//div[@class='inventory_item_name' and text()='{item_name}']/ancestor::div[@class='cart_item']//button[starts-with(@id, 'remove-')]")
        self.click_element(remove_button_locator)
        print(f"Removed item from cart: {item_name}")

    def click_item_title_in_cart(self, item_name):
        """Click on item title in cart to go to item detail page"""
        item_title_locator = (By.XPATH,
                              f"//div[@class='cart_item']//div[@class='inventory_item_name' and text()='{item_name}']")
        self.click_element(item_title_locator)
        print(f"Clicked on cart item title: {item_name}")

    def click_item_image_in_cart(self, item_name):
        """Click on item image in cart to go to item detail page"""
        item_image_locator = (By.XPATH,
                              f"//div[@class='cart_item']//div[@class='inventory_item_name' and text()='{item_name}']/ancestor::div[@class='cart_item']//img")
        self.click_element(item_image_locator)
        print(f"Clicked on cart item image: {item_name}")

    def get_item_details_from_cart(self, item_name):
        """Get item details from cart for comparison"""
        cart_item = self.find_element((By.XPATH,
                                       f"//div[@class='inventory_item_name' and text()='{item_name}']/ancestor::div[@class='cart_item']"))

        details = {
            'name': cart_item.find_element(By.CLASS_NAME, 'inventory_item_name').text,
            'description': cart_item.find_element(By.CLASS_NAME, 'inventory_item_desc').text,
            'price': cart_item.find_element(By.CLASS_NAME, 'inventory_item_price').text,
            'quantity': cart_item.find_element(By.CLASS_NAME, 'cart_quantity').text
        }
        return details

    def remove_all_items_from_cart(self):
        """Remove all items from cart"""
        cart_items = self.get_cart_items()
        for item in cart_items:
            item['remove_button'].click()
            print(f"Removed {item['name']} from cart")

    def verify_cart_is_empty(self):
        """Verify that cart is empty"""
        try:
            cart_items = self.find_elements((By.CLASS_NAME, 'cart_item'))
            return len(cart_items) == 0
        except:
            return True