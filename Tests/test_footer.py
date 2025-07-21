import time

import pytest


from Locators.alllocators import LoginPageLocators
from Pages.LoginPage import LoginPage
from Pages.OtherPage import OtherPage


def test_footer(driver):
    login_page = LoginPage(driver)
    login_page.login(LoginPageLocators.valid_username,LoginPageLocators.valid_password)
    footer_page=OtherPage(driver)
    assert footer_page.is_footer_displayed(), "Footer bar not displayed"

    main_window=driver.current_window_handle

    footer_page.click_twitter_logo()
    footer_page.window_handle(driver,main_window)
    time.sleep(2)
    assert "twitter.com" or "x.com" in driver.current_url, f"Twitter site is not displayed,Got url:{driver.current_url}"
    driver.close()
    driver.switch_to.window(main_window)
    time.sleep(2)
    footer_page.click_facebook_logo()

    footer_page.window_handle(driver, main_window)
    time.sleep(2)
    assert "facebook.com" in driver.current_url, f"Facebook site is not displayed, Got url:{driver.current_url}"
    driver.close()
    driver.switch_to.window(main_window)
    time.sleep(2)
    footer_page.click_linkedin_logo()
    footer_page.window_handle(driver, main_window)
    time.sleep(2)
    print(f"{driver.current_url} is displayed")
    assert "linkedin.com" in driver.current_url, f"Linkedin site is not displayed,Got url:{driver.current_url}"

@pytest.mark.parametrize("social_link,expected_url",[("twitter","twitter.com"),("facebook","facebook.com"),("linkedin","linkedin.com")])
def test_footer_using_parameters(driver,social_link,expected_url):
    login_page = LoginPage(driver)
    login_page.login(LoginPageLocators.valid_username,LoginPageLocators.valid_password)
    footer_page=OtherPage(driver)
    assert footer_page.is_footer_displayed(), "Footer bar not displayed"
    assert footer_page.is_copyright_displayed(),"Copyright bar not displayed"
    main_window=driver.current_window_handle
    time.sleep(2)
    if social_link == "twitter":
        footer_page.click_twitter_logo()
    elif social_link == "facebook":
        footer_page.click_facebook_logo()
    else:
        footer_page.click_linkedin_logo()
    footer_page.window_handle(driver,main_window)
    time.sleep(2)
    assert expected_url in driver.current_url, f"Expected url:{driver.current_url}"
    driver.close()
    driver.switch_to.window(main_window)

