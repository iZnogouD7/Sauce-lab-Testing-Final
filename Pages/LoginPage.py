
from Locators.alllocators import LoginPageLocators
from Pages.BasePage import BasePage


class LoginPage(BasePage):
    def login(self,username,password):
        self.type_in_element(LoginPageLocators.username_field,username)
        self.type_in_element(LoginPageLocators.password_field,password)
        self.click_element(LoginPageLocators.login_button)
        print("Logged in successfully")
    def login_with_valid_data(self):
        self.login(LoginPageLocators.valid_username,LoginPageLocators.valid_password)

    def get_error_message(self):
        return self.get_text_from_element(LoginPageLocators.error_field_path)
    def is_error_displayed(self):
        return self.is_displayed(LoginPageLocators.error_field_path)
    def is_password_masked(self):
        password_field=self.find_element(LoginPageLocators.password_field)
        return password_field.get_attribute("type")=="password"
    def click_show_password(self):
        self.click_element(LoginPageLocators.show_password_path)
    def dismiss_error_message(self):
        if self.is_displayed(LoginPageLocators.error_cancel_path):
            self.click_element(LoginPageLocators.error_cancel_path)
    def is_login_successful(self):
        return self.wait_for_page_load("inventory")

    def are_elements_displayed(self):
        return (self.is_displayed(LoginPageLocators.username_field) and
                self.is_displayed(LoginPageLocators.password_field) and
                self.is_displayed(LoginPageLocators.login_button))

    #def get_url(self):
#     return self.driver.current_url
#
# def  get_title(self):
#     return self.driver.title
    