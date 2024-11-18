from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from .base import BaseScraper

class SeleniumScraper(BaseScraper):
    def __init__(self):
        self.options = Options()
        self.options.add_argument("--window-size=1500,1080")
        self.options.set_preference("general.useragent.override", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
        self.driver = webdriver.Firefox(options=self.options)
        self.driver.maximize_window()
        self.driver.implicitly_wait(60)

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def close(self):
        if self.driver:
            self.driver.quit()

    def get(self, url):
        self.driver.get(url)
        return self.driver.page_source
    
    def login_static_form(self, url, username, password, username_selector, password_selector, submit_selector):
        self.driver.get(url)
        self.handle_alert()

        self.driver.find_element(By.XPATH, username_selector).send_keys(username)
        self.driver.find_element(By.XPATH, password_selector).send_keys(password)

        self.driver.find_element(By.XPATH, submit_selector).click()

        self.handle_alert()

    def attempt_cookie_popup(self, accept_selector):
        try:
            self.driver.find_element(By.XPATH, accept_selector).click()
            return True
        except:
            return False

    def handle_alert(self):
        """
        Handle and dismiss unexpected alerts or dialogs that may appear.
        """
        try:
            WebDriverWait(self.driver, 10).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            alert.accept()  # can also use alert.dismiss()
            print("Alert accepted successfully.")
        except:
            print("No alert found.")

    def post(self, url, data):
        # Needs Javascript per site implementation
        raise NotImplementedError("POST method is not implemented for SeleniumScraper")

    def get_page_source(self):
        return self.driver.page_source

    def get_cookies(self):
        cookies = self.driver.get_cookies()
        return {cookie['name']: cookie['value'] for cookie in cookies}

    def set_cookies(self, cookies):
        for name, value in cookies.items():
            self.driver.add_cookie({'name': name, 'value': value})

    def get_local_storage(self):
        # Execute JavaScript to return all localStorage data
        local_storage = self.driver.execute_script("""
            const localStorageData = {};
            for (let i = 0; i < localStorage.length; i++) {
                const key = localStorage.key(i);
                const value = localStorage.getItem(key);
                localStorageData[key] = value;
            }
            return localStorageData;
""")
        return local_storage

    def set_local_storage(self, items):
        # Set items in localStorage using JavaScript execution
        for key, value in items.items():
            self.driver.execute_script(f"window.localStorage.setItem('{key}', '{value}');")

    def clear_local_storage(self):
        # Clear all data from localStorage
        self.driver.execute_script("window.localStorage.clear();")
