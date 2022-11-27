import pandas as pd
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import matplotlib.pyplot as plt
import os
import logging
from urllib.parse import urlparse


## Setup chrome options
chrome_options = Options()
chrome_options.add_argument("--headless") # Ensure GUI is off
chrome_options.add_argument("--no-sandbox")

# Silent download of drivers
logging.getLogger('WDM').setLevel(logging.NOTSET)
os.environ['WDM_LOG'] = 'False'

# Create service
webdriver_service = Service(ChromeDriverManager().install())

# Create driver
driver = webdriver.Chrome(service = webdriver_service, options = chrome_options)
# URL of coffee roastery displaying all the coffees available
page_url = 'https://www.rastshop.ch/de'

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get(page_url)

# find coffees currently offered
coffee_types = driver.find_elements(by=By.CLASS_NAME, value='rs-btn-white')

coffee_links = []
for type in coffee_types:
    url = type.get_attribute('href')
    coffee_links.append({"url": url})

coffee = []

for coffee in coffee_links:
    # go to detailpage of each coffee
    driver.get(coffee['url'])

    coffee_elems = driver.find_elements(by=By.CLASS_NAME, value='category-page__member-link')

    for elem in character_elems:
