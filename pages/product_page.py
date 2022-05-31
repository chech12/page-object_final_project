from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.common.by import By
from .locators import ProductPageLocators
from .base_page import BasePage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import math


class ProductPage(BasePage):
    def solve_quiz_and_get_code(self):
        alert = self.browser.switch_to.alert
        x = alert.text.split(" ")[2]
        answer = str(math.log(abs((12 * math.sin(float(x))))))
        alert.send_keys(answer)
        alert.accept()
        try:
            alert = self.browser.switch_to.alert
            alert_text = alert.text
            print(f"Your code: {alert_text}")
            alert.accept()
        except NoAlertPresentException:
            print("No second alert presented")

    def get_product_name(self):
        return self.browser.find_element(*ProductPageLocators.PRODUCT_NAME).text

    def get_product_price(self):
        return self.browser.find_element(*ProductPageLocators.PRODUCT_PRICE).text[:4]

    def add_to_basket(self):
        button = self.browser.find_element(*ProductPageLocators.ADD_TO_BASKET_BTN)
        button.click()

    def should_be_success_message(self):
        product_name = self.get_product_name()
        assert self.is_element_present(By.XPATH, f'//strong[text()="{product_name}"]'), "Message is wrong"

    def should_be_message_about_total_cost(self):
        price = self.get_product_price()
        print(price)
        assert self.is_element_present(By.XPATH, f'//strong[contains(text(), "{price}")]'), "Message is wrong"
