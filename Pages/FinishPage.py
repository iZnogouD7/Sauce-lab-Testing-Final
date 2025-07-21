from Locators.alllocators import FinishPageLocators, ProductPageLocators
from Pages.BasePage import BasePage


class FinishPage(BasePage):
    def is_thank_you_displayed(self):
        return self.is_displayed(FinishPageLocators.Thank_message)
    def click_back_home(self):
        self.click_element(FinishPageLocators.back_home_button)
    def get_finish_title(self):
        return self.get_text_from_element(FinishPageLocators.finish_page_title)
    def get_final_cart_count(self):
        return int(self.get_text_from_element(ProductPageLocators.cart_count_path))
    # def get_finish_url(self):
    #     return self.get_current_url()