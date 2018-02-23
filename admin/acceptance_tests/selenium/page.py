from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions


class BasePage(object):
    """Base class to initialize the base page that will be called from all pages"""

    def __init__(self, driver):
        self.driver = driver

    def find_element(self, by, value, timeout=None):
        if timeout:
            return WebDriverWait(self.driver, timeout).until(
                expected_conditions.presence_of_element_located((by, value)))
        else:
            return self.driver.find_element(by, value)

    def select_language(self, locale):
        self.find_element(By.XPATH, '//li[@id="language-dropdown"]').click()
        self.find_element(
            By.XPATH,
            '//a[contains(@href,"language={}")]'.format(locale)
        ).click()


class IndexPage(BasePage):

    def select_page_size(self, size, timeout=None):
        page_list = self.find_element(By.XPATH, '//*[@class="page-list"]', timeout)
        page_list.find_element(By.XPATH, './/button[@data-toggle="dropdown"]').click()
        page_list.find_element(By.XPATH, './/a[text()="{}"]'.format(size)).click()

    def check_pagination_info(self, expected, timeout):
        WebDriverWait(self.driver, timeout).until(
            expected_conditions.text_to_be_present_in_element(
                (By.XPATH, '//span[@class="pagination-info"]'),
                expected))

    def find_item_action(self, id_, action):
        td = self.find_element(By.XPATH, '//tr[@data-uniqueid="{}"]/td[@class="actions"]'.format(id_))
        td.find_element(By.XPATH, './/button[@data-target="item-{}-actions"]'.format(id_)).click()
        return td.find_element(By.XPATH, './/a[contains(@class, "{}")]'.format(action))

    def click_delete(self, id_):
        self.find_item_action(id_, 'delete').click()
        self.driver.switch_to_alert().accept()
        self.driver.switch_to_default_content()