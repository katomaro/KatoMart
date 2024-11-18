import requests
import copy

from .base import BaseScraper

class RequestsScraper(BaseScraper):
    DEFAULT_HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0'}

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(self.DEFAULT_HEADERS)

    def get(self, url):
        self.response = self.session.get(url)
        return self.response

    def post(self, url, data):
        self.response = self.session.post(url, data=data)
        return self.response

    def get_page_source(self):
        return self.response.text if self.response else ''

    def get_cookies(self):
        return self.session.cookies.get_dict()

    def set_cookies(self, cookies):
        self.session.cookies.update(cookies)

    def close(self):
        self.session.close()
