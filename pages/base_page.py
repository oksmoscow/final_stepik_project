from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import TimeoutException

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from .locators import BasePageLocators

import math


class BasePage():
    def __init__(self, browser, url, timeout=5):
        self.browser = browser
        self.url = url
        # self.browser.implicitly_wait(timeout)   # команда для неявного ожидания со значением по умолчанию в 10


    def go_to_login_page(self):
        link = self.browser.find_element(*BasePageLocators.LOGIN_LINK)
        link.click()
        # return LoginPage(browser=self.browser, url=self.browser.current_url)    # создается новый объект - страница входа и регистрации
        # alert = self.browser.switch_to.alert
        #alert.accept()

    def go_to_busket_page(self):
        link = self.browser.find_element(*BasePageLocators.BASKET_BUTTON)
        link.click()


    def is_element_present(self, how, what):    # метод, в котором перехватываем исключение. Передаются два аргумента: как искать (how - css, id, xpath и тд (By.CSS_SELECTOR)) и что искать (what - строку-селектор ("#login_link"))
        try:
            self.browser.find_element(how, what)
        except (NoSuchElementException):
            return False
        return True


    # is_not_element_present: упадет, как только увидит искомый элемент. Не появился: успех, тест зеленый. 
    # is_disappeared: будет ждать до тех пор, пока элемент не исчезнет.     

    def is_not_element_present(self, how, what, timeout=4):     # метод, который проверяет, что элемент не появляется на странице в течение заданного времени
        try:
            WebDriverWait(self.browser, timeout).until(EC.presence_of_element_located((how, what)))
        except TimeoutException:
            return True

        return False


    def is_disappeared(self, how, what, timeout=4):             # метод, который проверяет, что элемент исчезает со временем
        try:
            WebDriverWait(self.browser, timeout, 1, TimeoutException).\
                until_not(EC.presence_of_element_located((how, what)))
        except TimeoutException:
            return False

        return True    


    def open(self):
        self.browser.get(self.url)


    def should_be_authorized_user(self):                        # метод, который проверяет, что пользователь залогинен
        assert self.is_element_present(*BasePageLocators.USER_ICON), "User icon is not presented," \
                                                                     " probably unauthorised user"


    def should_be_login_link(self):                             # метод, который будет проверять наличие ссылки
        assert self.is_element_present(*BasePageLocators.LOGIN_LINK), "Login link is not presented"


    def solve_quiz_and_get_code(self):                          # метод для получения проверочного кода при добавлении товара в корзину
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


