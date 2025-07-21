from selenium.webdriver.common.by import By
class LoginPageLocators:
    loginpageUrl="https://www.saucedemo.com/"
    valid_username="standard_user"
    valid_password="secret_sauce"


    username_field = (By.ID,"user-name")
    password_field = (By.ID,"password")
    login_button=(By.ID,"login-button")

    error_field_path = (By.XPATH,'//*[@id="login_button_container"]/div/form/div[3]/h3')
    username_cancel_path=(By.XPATH,'//*[@id="login_button_container"]/div/form/div[1]/svg/path')
    password_cancel_path=(By.XPATH,'//*[@id="login_button_container"]/div/form/div[2]/svg')
    error_cancel_path=(By.XPATH,'//*[@id="login_button_container"]/div/form/div[3]/h3/button')
    show_password_path=(By.XPATH,'//*[@id="password"]')

class ProductPageLocators:
    ProductPageUrl="https://www.saucedemo.com/inventory.html"
    title_path=(By.XPATH,'//*[@id="header_container"]/div[2]/span')
    inventory_count_path=(By.CLASS_NAME,'inventory_item')
    cart_count_path=(By.CLASS_NAME,'shopping_cart_badge')

    cart_button_path = (By.XPATH, '//*[@id="shopping_cart_container"]/a')
    select_filter_path=(By.CLASS_NAME, 'product_sort_container')
    all_item_name_class_path=(By.CLASS_NAME,'inventory_item_name')
    all_item_price_class_path=(By.CLASS_NAME,'inventory_item_price')
    all_item_img_class_path=(By.CLASS_NAME,'inventory_item_img')

    img_back_pack_path=(By.XPATH,'//*[@id="item_4_img_link"]/img')
    img_bike_light_path=(By.XPATH,'//*[@id="item_0_img_link"]/img')
    img_Tshirt_path=(By.XPATH,'//*[@id="item_1_img_link"]/img')
    img_Jacket_path=(By.XPATH,'//*[@id="item_5_img_link"]/img')
    img_onesie_path=(By.XPATH,'//*[@id="item_2_img_link"]/img')
    img_allthing_path=(By.XPATH,'//*[@id="item_3_img_link"]/img')

    title_back_pack_path=(By.XPATH,'//*[@id="item_4_title_link"]/div')
    title_bike_light_path=(By.XPATH,'//*[@id="item_0_title_link"]/div')
    title_Tshirt_path=(By.XPATH,'//*[@id="item_1_title_link"]/div')
    title_Jacket_path=(By.XPATH,'//*[@id="item_5_title_link"]/div')
    title_onesie_path=(By.XPATH,'//*[@id="item_2_title_link"]/div')
    title_allthing_path=(By.XPATH,'//*[@id="item_3_title_link"]/div')

    add_back_pack_path = (By.ID,'add-to-cart-sauce-labs-backpack')
    add_bike_light_path = (By.ID,'add-to-cart-sauce-labs-bike-light')
    add_Tshirt_path = (By.ID,'add-to-cart-sauce-labs-bolt-t-shirt')
    add_Jacket_path = (By.ID,'add-to-cart-sauce-labs-fleece-jacket')
    add_onesie_path=(By.ID,'add-to-cart-sauce-labs-onesie')
    #add_allthings_path=(By.XPATH,'//*[@id="add-to-cart-test.allthethings()-t-shirt-(red)"]')
    add_allthings_path=(By.ID,'add-to-cart-test.allthethings()-t-shirt-(red)')

    remove_back_pack_path=(By.ID,'remove-sauce-labs-backpack')
    remove_bike_light_path=(By.ID,'remove-sauce-labs-bike-light')
    remove_Tshirt_path=(By.ID,'remove-sauce-labs-bolt-t-shirt')
    remove_Jacket_path=(By.ID,'remove-sauce-labs-fleece-jacket')
    remove_onesie_path=(By.ID,'remove-sauce-labs-onesie')
    #remove_allthings_path=(By.XPATH,'//*[@id="remove-test.allthethings()-t-shirt-(red)"]')
    remove_allthings_path=(By.ID,'remove-test.allthethings()-t-shirt-(red)')
    backpack_name_detail=(By.XPATH,'//*[@id="inventory_item_container"]/div/div/div[2]/div[1]')
    backpack_image_detail=(By.XPATH,'//*[@id="inventory_item_container"]/div/div/div[1]/img')
    backpack_desc_detail=(By.XPATH,'//*[@id="inventory_item_container"]/div/div/div[2]/div[2]')
    backpack_price_detail=(By.XPATH,'//*[@id="inventory_item_container"]/div/div/div[2]/div[3]')

    back_to_product = (By.ID, 'back-to-products')


    @staticmethod
    def product_card_by_name(name):
        return By.XPATH,f"//div[text()='{name}']/ancestor::div[@class='inventory-item']"
    inventory_name_class_path=(By.CLASS_NAME, 'inventory_item_name')
    inventory_desc_class_path=(By.CLASS_NAME, 'inventory_item_desc')
    inventory_img_class_path=(By.CLASS_NAME, 'inventory_item_img')
    inventory_price_class_path=(By.CLASS_NAME, 'inventory_item_price')
    inventory_add_to_cart_button=(By.ID, 'add-to-cart')
    inventory_add_to_remove_button=(By.ID, 'remove')

class CartPageLocators:
    cart_page_title=(By.XPATH,'//*[@id="header_container"]/div[2]/span')
    continue_shopping_path=(By.ID,'continue-shopping')
    checkout_path=(By.ID,'checkout')
    first_item_path=(By.XPATH,'// *[ @ id = "item_4_title_link"] / div')
    second_item_path=(By.XPATH,'//*[@id="item_0_title_link"]/div')

class CheckoutPageLocators:
    checkout_page_url="https://www.saucedemo.com/checkout-step-one.html"
    valid_first_name="Eric"
    valid_last_name="Rocks"
    valid_zip_code="44600"
    checkout_title=(By.XPATH,'//*[@id="header_container"]/div[2]/span')
    first_name_path=(By.ID,'first-name')
    last_name_path=(By.ID,'last-name')
    Zip_code_path=(By.ID,'postal-code')
    cancel_button_path=(By.ID,'cancel')
    continue_button_path=(By.ID,'continue')
    error_message_path=(By.XPATH,'//*[@id="checkout_info_container"]/div/form/div[1]/div[4]/h3')
    error_cancel_button=(By.XPATH,'//*[@id="checkout_info_container"]/div/form/div[1]/div[4]/h3/button')

class CheckoutOverviewPageLocators:
    checkout_overview_url='https://www.saucedemo.com/checkout-step-two.html'
    checkout_overview_title=(By.XPATH,'//*[@id="header_container"]/div[2]/span')

    payment_page_url = 'https://www.saucedemo.com/checkout-step-two.html'
    payment_info_path = (By.XPATH, '//*[@id="checkout_summary_container"]/div/div[2]/div[2]')
    shipping_info_path = (By.XPATH, '//*[@id="checkout_summary_container"]/div/div[2]/div[4]')
    payment_title = (By.XPATH, '//*[@id="header_container"]/div[1]/div[2]/div')
    finish_button_path = (By.XPATH, '//*[@id="finish"]')
    cancel_button_path = (By.XPATH, '//*[@id="cancel"]')


class FinishPageLocators:
    finish_page_url='https://www.saucedemo.com/checkout-complete.html'
    finish_page_title=(By.XPATH,'//*[@id="header_container"]/div[2]/span')
    back_home_button=(By.XPATH,'//*[@id="back-to-products"]')
    Thank_message=(By.CLASS_NAME,'complete-header')


class OtherPageLocators:
    menu_button_path = (By.ID,'react-burger-menu-btn')
    all_item_path = (By.ID, 'inventory_sidebar_link')
    about_path = (By.ID, 'about_sidebar_link')
    logout_path = (By.ID, 'logout_sidebar_link')
    reset_app_state_path = (By.ID, 'reset_sidebar_link')
    menu_close_path = (By.ID,'react-burger-cross-btn')
    #menu_container_path=(By.CLASS_NAME, 'bm-menu-wrap')
    menu_container_path=(By.XPATH,'//*[@id="menu_button_container"]/div/div[2]')
    footer_path = (By.CLASS_NAME, 'footer')
    twitter_path = (By.XPATH, '//*[@id="page_wrapper"]/footer/ul/li[1]/a')
    facebook_path = (By.XPATH, '//*[@id="page_wrapper"]/footer/ul/li[2]/a')
    linkedin_path = (By.XPATH, '//*[@id="page_wrapper"]/footer/ul/li[3]/a')
    copyright_path=(By.XPATH,'//*[@id="page_wrapper"]/footer/div')



