from .selenium_based import SeleniumScraper
from .requests_based import RequestsScraper
# from .selenium_wire_scraper import SeleniumWireScraper
import copy, requests

def scraper_factory(platform_type):
    if platform_type == 'javascript':
        return SeleniumScraper()
    # elif platform_type == 'javascript_with_requests':
        # return SeleniumWireScraper()
    elif platform_type == 'static':
        return RequestsScraper()
    else:
        raise ValueError('Unknown platform type')


def transfer_cookies_selenium_to_requests(selenium_scraper, requests_scraper):
    selenium_cookies = selenium_scraper.get_cookies()
    requests_scraper.set_cookies(selenium_cookies)

def transfer_cookies_requests_to_selenium(requests_scraper, selenium_scraper):
    requests_cookies = requests_scraper.get_cookies()
    selenium_scraper.set_cookies(requests_cookies)

def transfer_local_storage_selenium_to_selenium(source_scraper, target_scraper):
    local_storage_data = source_scraper.get_local_storage()
    target_scraper.set_local_storage(local_storage_data)

def clone_session(session):
    new_session = requests.Session()

    # Copy headers
    new_session.headers = session.headers.copy()

    # Copy cookies
    new_session.cookies = requests.cookies.RequestsCookieJar()
    for cookie in session.cookies:
        new_session.cookies.set_cookie(copy.copy(cookie))

    # Copy authentication
    new_session.auth = copy.deepcopy(session.auth)

    # Copy proxies
    new_session.proxies = session.proxies.copy()

    # Copy hooks
    new_session.hooks = session.hooks.copy()

    # Copy query parameters
    new_session.params = session.params.copy()

    # Copy SSL verification settings
    new_session.verify = session.verify

    # Copy SSL client certificate settings
    new_session.cert = session.cert

    # Copy maximum redirects
    new_session.max_redirects = session.max_redirects

    # Copy trust environment settings
    new_session.trust_env = session.trust_env

    # Copy streaming settings
    new_session.stream = session.stream

    # Copy adapters
    for prefix, adapter in session.adapters.items():
        new_adapter = requests.adapters.HTTPAdapter()
        new_adapter.max_retries = copy.deepcopy(adapter.max_retries)
        new_session.mount(prefix, new_adapter)

    return new_session
