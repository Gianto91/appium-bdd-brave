from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class GooglePage:
    def __init__(self, driver):
        self.driver = driver
        self.search_box = (By.NAME, "q")

    def open(self, url):
        self.driver.get(url)

    def search(self, text):
        box = self.driver.find_element(*self.search_box)
        box.send_keys(text)
        box.send_keys(Keys.ENTER)
