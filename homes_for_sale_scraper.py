import dotenv
import os
import time
from bs4 import BeautifulSoup
import requests
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys


class HomesForSaleScraper:

    def __init__(self):
        dotenv.load_dotenv()
        self.macbook_headers = {
            "User-Agent": "Mozilla/5.0"
        }
        self.driver = None

    def get_listings(self):
        zillow_url = "https://www.zillow.com/valparaiso-in-46383/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3A%2246383%22%2C%22mapBounds%22%3A%7B%22west%22%3A-87.8708135859375%2C%22east%22%3A-86.26406309765625%2C%22south%22%3A41.22312766665844%2C%22north%22%3A41.57851339768033%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A78126%2C%22regionType%22%3A7%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22ah%22%3A%7B%22value%22%3Atrue%7D%2C%22sort%22%3A%7B%22value%22%3A%22globalrelevanceex%22%7D%2C%22beds%22%3A%7B%22min%22%3A4%7D%2C%22baths%22%3A%7B%22min%22%3A3%7D%7D%2C%22isListVisible%22%3Atrue%7D"
        zillow_response = requests.get(url=zillow_url, headers=self.macbook_headers)
        zillow_response.raise_for_status()
        zillow_page = BeautifulSoup(zillow_response.text, "html.parser")
        # listing_class = "ListItem-c11n-8-82-3__sc-10e22w8-0 srp__hpnp3q-0 enEXBq with_constellation"
        # all_listing_els = zillow_page.find_all(class_=listing_class)
        all_prices = [price_el.text for price_el in zillow_page.select('span[data-test="property-card-price"]')]
        print(all_prices)

        # zillow_url = f"https://www.zillow.com/"
        # self.driver.get(zillow_url)
        # time.sleep(2)
        # search_box_el = self.driver.find_element(By.ID, "search-box-input")
        # search_box_el.click()
        # search_box_el.send_keys(self.zip_code, Keys.ENTER)
        # time.sleep(2)
        # bed_bath_num_el = self.driver.find_element(by=By.CSS_SELECTOR, value='button[data-test="beds-filters-button"]')
        # bed_bath_num_el.click()
        # time.sleep(1)
        # bed_options_el = self.driver.find_element(By.NAME, "bed-options")
        # num_of_beds_el = bed_options_el.find_element(By.CSS_SELECTOR, 'button[value="4"]')
        # num_of_beds_el.click()
        # bath_options_el = self.driver.find_element(By.NAME, "bath-options")
        # num_of_baths_el = bath_options_el.find_element(By.CSS_SELECTOR, 'button[value="3"')
        # num_of_baths_el.click()
        # apply_button_el = self.driver.find_element(By.CSS_SELECTOR, 'button[data-test="close-filters-button"]')
        # apply_button_el.click()

    def complete_google_form(self):
        # PROXY = "182.72.203.246"
        # webdriver.DesiredCapabilities.FIREFOX['proxy'] = {
        #     "httpProxy": PROXY,
        #     "ftpProxy": PROXY,
        #     "sslProxy": PROXY,
        #     "proxyType": "MANUAL",
        # }
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        chrome_options.page_load_strategy = 'eager'
        # self.zip_code = input("Enter zip code to search:\n")
        # while not self.zip_code.isdigit() or len(self.zip_code) != 5:
        #     self.zip_code = input("Please enter valid zip code:\n")
        self.driver = webdriver.Chrome(chrome_options=chrome_options)
