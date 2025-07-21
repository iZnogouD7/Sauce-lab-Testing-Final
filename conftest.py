import pytest
from selenium import webdriver


@pytest.fixture()
def driver():
    base_url = "https://www.saucedemo.com/"
    driver=webdriver.Firefox()
    #driver = webdriver.ChromiumEdge()
    driver.maximize_window()
    driver.get(base_url)
    yield driver
    driver.quit()

