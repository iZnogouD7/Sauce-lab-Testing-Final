import pytest
import time
from Locators.alllocators import LoginPageLocators
from Pages.LoginPage import LoginPage
from Utils.FileReader import load_csv_data

@pytest.mark.order(1)
@pytest.mark.parametrize("username,password,expected", load_csv_data("Data/login_data.csv"))
def test_login(driver,username, password, expected):
    login_page = LoginPage(driver)
    assert login_page.get_current_url()== LoginPageLocators.loginpageUrl,f"Got:{login_page.get_current_url()},Expected:{LoginPageLocators.loginpageUrl}"
    assert login_page.are_elements_displayed()== True,"Login failed as elements are not displayed"
    login_page.login(username, password)
    print(f"Logging with username:{username} and password :{password}")
    time.sleep(3)
    if expected=="success":
        print("Successfully logged in")
        assert login_page.get_current_url() == "https://www.saucedemo.com/inventory.html",f"Wrong url: {login_page.get_current_url()}"
        assert login_page.get_page_title()== "Swag Labs",f"Wrong title: {login_page.get_page_title()}"
    elif expected=="failed":
        print(f"Login failed {login_page.get_error_message()}")
        assert "Epic sadface" in login_page.get_error_message(),f"Got error message: {login_page.get_error_message()}"
    elif expected=="lockedout":
        print(f"Login failed {login_page.get_error_message()}")
        assert "Epic sadface: Username and password do not match any user in this service" in login_page.get_error_message(),f"Expected locked user error message: {login_page.get_error_message()}"
    else:
        print("Unexpected value and Error Found")
@pytest.mark.order(2)
def test_password_masking(driver):
    login_page = LoginPage(driver)
    assert login_page.get_current_url()== LoginPageLocators.loginpageUrl
    password_field=login_page.find_element(LoginPageLocators.password_field)
    assert password_field.get_attribute("type") == "password",f"Password should be masked by default. Got attribute:{password_field.get_attribute('type')}"
    #login_page.click_element(LoginPageLocators.show_password_path)
    #assert password_field.get_attribute("type")=="text","Password should be visible after clicking show password button"

@pytest.mark.order(3)
def test_error_message_cancel_button(driver):
    login_page = LoginPage(driver)
    login_page.click_element(LoginPageLocators.login_button)
    assert login_page.is_displayed(LoginPageLocators.error_field_path),"error field is not displayed"
    #assert login_page.is_displayed(LoginPageLocators.username_cancel_path),"Username filed cancel button not displayed"
    #assert login_page.click_element(LoginPageLocators.username_cancel_path)
    #print("Username Cancel button displayed")
    #assert login_page.is_displayed(LoginPageLocators.password_cancel_path),"password fieldcancel button not displayed"
    #assert login_page.click_element(LoginPageLocators.password_cancel_path)
    #print("Password Cancel button displayed")
    #assert login_page.is_displayed(LoginPageLocators.error_cancel_path),"Error field cancel button not displayed"
    #assert login_page.click_element(LoginPageLocators.error_cancel_path)
    #print("Error Cancel button displayed")
    login_page.click_element(LoginPageLocators.error_cancel_path)
    assert not login_page.is_displayed(LoginPageLocators.error_field_path),"Error field still displayed"

