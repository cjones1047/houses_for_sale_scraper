import dotenv
import os
import time
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import requests
# from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.keys import Keys


class HomesForSaleScraper:

    def __init__(self):
        dotenv.load_dotenv()
        proxy = os.getenv("PROXY")
        self.proxies = {"http": f"http://{proxy}"}
        ua = UserAgent()
        self.macbook_headers = {"User-Agent": ua.random}
        self.all_prices = None
        self.all_addresses = None
        self.all_listing_links = None
        self.driver = None

    def get_listings(self):
        zillow_url = ("https://www.zillow.com/valparaiso-in-46383/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%"
                      "22usersSearchTerm%22%3A%2246383%22%2C%22mapBounds%22%3A%7B%22west%22%3A-87.8708135859375%2C%"
                      "22east%22%3A-86.26406309765625%2C%22south%22%3A41.22312766665844%2C%22north%22%"
                      "3A41.57851339768033%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A78126%2C%22regionType%"
                      "22%3A7%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22ah%22%3A%7B%22value%22%"
                      "3Atrue%7D%2C%22sort%22%3A%7B%22value%22%3A%22globalrelevanceex%22%7D%2C%22beds%22%3A%"
                      "7B%22min%22%3A4%7D%2C%22baths%22%3A%7B%22min%22%3A3%7D%7D%2C%22isListVisible%22%3Atrue%7D")
        zillow_response = requests.get(url=zillow_url, headers=self.macbook_headers, proxies=self.proxies)
        zillow_response.raise_for_status()
        time.sleep(1)
        zillow_page = BeautifulSoup(zillow_response.text, "html.parser")
        self.all_prices = [price_el.text for price_el in zillow_page.select('span[data-test="property-card-price"]')]
        self.all_addresses = [address_el.text for address_el in zillow_page.select('address[data-test='
                                                                                   '"property-card-addr"]')]
        self.all_listing_links = [link_el['href'] for link_el in zillow_page.select('a[class="StyledPropertyCard'
                                                                                    'DataArea-'
                                                                                    'c11n-8-82-3__sc-yipmu-0 hiBOYq '
                                                                                    'property-card-link"]')]
        print(self.all_prices, self.all_addresses, self.all_listing_links)
        if len(self.all_listing_links) == 0:
            print("wait 3 seconds to run again...")
            ua = UserAgent()
            self.macbook_headers = {"User-Agent": ua.random}
            time.sleep(3)
            self.get_listings()

    def complete_google_forms(self):
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(chrome_options=chrome_options)
        for index, value in enumerate(self.all_listing_links):
            self.driver.get("https://forms.gle/vM3gCaPqhuHuDWcD9")
            time.sleep(1)
            address_input_el = self.driver.find_element(By.CSS_SELECTOR, 'input[aria-labelledby="i1"]')
            address_input_el.click()
            address_input_el.send_keys(self.all_addresses[index])
            price_input_el = self.driver.find_element(By.CSS_SELECTOR, 'input[aria-labelledby="i5"]')
            price_input_el.click()
            price_input_el.send_keys(self.all_prices[index])
            link_input_el = self.driver.find_element(By.CSS_SELECTOR, 'input[aria-labelledby="i9"]')
            link_input_el.click()
            link_input_el.send_keys(self.all_listing_links[index])
            submit_button_el = self.driver.find_element(By.CSS_SELECTOR, 'span[class="NPEfkd RveJvd snByac"]')
            submit_button_el.click()
