class BaseScraper:
    def get(self, url):
        raise NotImplementedError

    def post(self, url, data):
        raise NotImplementedError

    def get_page_source(self):
        raise NotImplementedError
    
    def get_headers(self):
        raise NotImplementedError

    def set_headers(self, headers):
        raise NotImplementedError

    def get_cookies(self):
        raise NotImplementedError

    def set_cookies(self, cookies):
        raise NotImplementedError

    def close(self):
        raise NotImplementedError
