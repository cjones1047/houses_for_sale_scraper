import dotenv
import os
import time
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys


class HomesForSaleScraper:

    def __init__(self):
        dotenv.load_dotenv()
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        self.zip_code = input("Enter zip code to search:\n")
        while not self.zip_code.isdigit() or len(self.zip_code) != 5:
            self.zip_code = input("Please enter valid zip code:\n")
        self.driver = webdriver.Chrome(options=chrome_options)

    def get_listings(self):
        zillow_url = f"https://www.zillow.com/homes/{self.zip_code}/"
        self.driver.get(zillow_url)
