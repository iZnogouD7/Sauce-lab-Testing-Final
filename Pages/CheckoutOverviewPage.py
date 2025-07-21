from Locators.alllocators import CheckoutOverviewPageLocators, ProductPageLocators
from Pages.BasePage import BasePage


class CheckoutOverviewPage(BasePage):

    def click_finish_button(self):
        self.click_element(CheckoutOverviewPageLocators.finish_button_path)

    def click_cancel_button(self):
        self.click_element(CheckoutOverviewPageLocators.cancel_button_path)

    # def get_checkout_overview_page_url(self):
    #     return self.driver.current_url

    # def get_checkout_overview_page_title(self):
    #     return self.driver.title

        # Get item names from overview page

    def get_item_names(self):
        elements = self.find_elements(ProductPageLocators.inventory_name_class_path)
        return [e.text for e in elements]

        #  Get item prices from overview page

    def get_item_prices(self):
        elements = self.find_elements(ProductPageLocators.inventory_price_class_path)
        return [e.text for e in elements]

        #  Get payment info (static)

    def get_payment_info(self):
        return self.get_text_from_element(("xpath", '//*[@class="summary_value_label"][1]'))

        #  Get shipping info (static)

    def get_shipping_info(self):
        return self.get_text_from_element(("xpath", '//*[@class="summary_value_label"][2]'))

        #  Get item total

    def get_item_total(self):
        item_text = self.get_text_from_element(("class name", "summary_subtotal_label"))
        return float(item_text.split("$")[1])

        #  Get tax

    def get_tax(self):
        tax_text = self.get_text_from_element(("class name", "summary_tax_label"))
        return float(tax_text.split("$")[1])

        # Get total (item total + tax)

    def get_total(self):
        total_text = self.get_text_from_element(("class name", "summary_total_label"))
        return float(total_text.split("$")[1])


