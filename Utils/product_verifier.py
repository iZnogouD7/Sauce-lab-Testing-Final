from Locators.alllocators import ProductPageLocators


class ProductVerifier:
    @staticmethod
    def verify_product_details(actual:dict,expected:dict,page_name:str):
        assert actual['name'] == expected['name'],f"{page_name} name mismatch: {actual['name']} != {expected['name']}"
        assert actual['price']==expected['price'],f"{page_name} price mismatch: {actual['price']}!= {expected['price']}"
        if 'desc' in expected:
            assert actual['desc'] ==expected['desc'],f"{page_name} desc mismatch: {actual['desc']}!= {expected['desc']}"
        if 'image' in expected:
            assert actual['image'] ==expected['image'],f"{page_name} image mismatch: {actual['image']}!= {expected['image']}"
    @staticmethod
    def get_product_dictionary(element,include_desc=True,include_image=True):
        details={
            'name':element.find_element(ProductPageLocators.inventory_name_class_path).text,
            'price':float(element.find_element(ProductPageLocators.inventory_price_class_path).text.replace('$',''))
        }
        if include_desc:
            details['desc']=element.find_element(ProductPageLocators.inventory_desc_class_path).text
        if include_image:
            details['image']=element.find_element(ProductPageLocators.inventory_img_class_path).get_attribute('src')
        return details
