from Locators.alllocators import ProductPageLocators, CheckoutPageLocators, OtherPageLocators
from Pages.BasePage import BasePage


class CheckoutPage(BasePage):
    def checkout_title(self):
        return self.get_text_from_element(CheckoutPageLocators.checkout_title)
    def click_cart_icon(self):
        self.click_element(ProductPageLocators.cart_button_path)
    def click_menu_icon(self):
        self.click_element(OtherPageLocators.menu_button_path)
    def click_continue_button(self):
        self.click_element(CheckoutPageLocators.continue_button_path)
    def click_cancel_button(self):
        self.click_element(CheckoutPageLocators.cancel_button_path)

    def enter_checkout_info(self,firstname,lastname,zipcode):
        self.type_in_element(CheckoutPageLocators.first_name_path,firstname)
        self.type_in_element(CheckoutPageLocators.last_name_path,lastname)
        self.type_in_element(CheckoutPageLocators.Zip_code_path,zipcode)
        print(f"Typed in {firstname} {lastname} {zipcode} in checkout info")
        self.click_element(CheckoutPageLocators.continue_button_path)

    def get_error(self):
        return self.get_text_from_element(CheckoutPageLocators.error_message_path)
    def click_error_cancel_button(self):
        self.click_element(CheckoutPageLocators.error_cancel_button)