import time
import pytest
from pages.login_page import LoginPage
from pages.product_page import ProductPage
from pages.basket_page import BasketPage

LINK = "http://selenium1py.pythonanywhere.com/en-gb/catalogue/the-city-and-the-stars_95/"


@pytest.mark.authorized
class TestUserAddToBasketFromProductPage:
    @pytest.fixture(scope="function", autouse=True)
    def setup(self, browser):
        self.email = str(time.time()) + "@fakemail.org"
        self.password = "VeRy_haRd_t0_guess_p4s$w0rD" + str(time.time())
        self.page = ProductPage(browser, LINK)
        self.page.open()
        self.page.go_to_login_page()
        self.register_page = LoginPage(browser, browser.current_url)
        self.register_page.register_new_user(self.email, self.password)
        self.register_page.should_be_authorized_user()

    def test_user_cant_see_success_message(self, browser):
        page = ProductPage(browser, LINK)
        page.open()
        page.should_not_be_success_message()

    @pytest.mark.need_review
    def test_user_can_add_product_to_basket(self, browser, link=LINK):
        page = ProductPage(browser, link)
        page.open()
        page.add_to_basket()
        page.should_be_success_message()
        page.should_be_message_about_total_cost()


@pytest.mark.need_review
def test_guest_can_add_product_to_basket(browser, link=LINK):
    page = ProductPage(browser, link)
    page.open()
    page.add_to_basket()
    page.should_be_success_message()
    page.should_be_message_about_total_cost()


@pytest.mark.xfail
def test_guest_cant_see_success_message_after_adding_product_to_basket(browser):
    page = ProductPage(browser, LINK)
    page.open()
    page.add_to_basket()
    page.should_not_be_success_message()


def test_guest_cant_see_success_message(browser):
    page = ProductPage(browser, LINK)
    page.open()
    page.should_not_be_success_message()


@pytest.mark.xfail
def test_message_disappeared_after_adding_product_to_basket(browser):
    page = ProductPage(browser, LINK)
    page.open()
    page.add_to_basket()
    page.should_disappear_success_message()


@pytest.mark.need_review
def test_guest_should_see_login_link_on_product_page(browser):
    page = ProductPage(browser, LINK)
    page.open()
    page.should_be_login_link()


def test_guest_can_go_to_login_page_from_product_page(browser):
    page = ProductPage(browser, LINK)
    page.open()
    page.go_to_login_page()
    login_page = LoginPage(browser, browser.current_url)
    login_page.should_be_login_page()


@pytest.mark.need_review
def test_guest_cant_see_product_in_basket_opened_from_product_page(browser):
    page = BasketPage(browser, LINK)
    page.open()
    page.go_to_basket_page()
    page.should_be_no_products_in_basket()
    page.should_be_message_that_basket_is_empty()
