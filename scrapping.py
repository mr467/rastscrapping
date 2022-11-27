import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.support.select import Select
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

# # Click on Accept cookies
time.sleep(3)
driver.find_element(By.XPATH, '//*[@id="app"]/footer/div/div[3]/div[2]/button').click()

# find URLs of coffees currently offered
coffee_links = driver.find_elements(by=By.CLASS_NAME, value='rs-btn-white')


coffee_urls = []                        #empty list for the urls
for link in coffee_links:               #loop to get each url
    url = link.get_attribute('href')
    coffee_urls.append({"url": url})

#the name of the coffee is in another object so the xpath methode is used
coffee_names = driver.find_elements(by = By.XPATH, value= '//h3')
coffee_titel= []                        #empty list for the names
for name in coffee_names:               #loop to get each name
    titel = name.text
    coffee_titel.append({titel})

#delete last element as it isn't a coffee type
del coffee_titel[-1]
del coffee_urls[-1]

#add list into a pandas dataframe which will be expanded with more data from the specific coffee detailpages
coffees = pd.DataFrame(list(zip(coffee_titel, coffee_urls)), columns=['name','url'])


coffee_data=[]
for i in coffee_urls:
    # go to book page
    driver.get(i['url'])
    origin = driver.find_element(by=By.XPATH, value='// div[1] /h3')
    aroma = driver.find_element(by=By.XPATH, value='//*[@id="app"]/main/section[2]/div/div[1]/div[2]/div[1]/table/tbody/tr[1]/td[2]')
    flavour = driver.find_element(by=By.XPATH, value='//*[@id="app"]/main/section[2]/div/div[1]/div[2]/div[1]/table/tbody/tr[2]/td[2]')
    driver.find_element(by= By.ID, value='vs1__combobox').click()
    driver.find_element(by=By.ID, value="vs1__option-3").click()
    price = driver.find_element(by=By.XPATH, value='//*[@id="vs1__combobox"]/div[1]/span')
    driver.quit()






#
# #-------------------------------------
# coffee_names =[]
#
# for coffee in coffee_urls:
#     driver.get(coffee['url'])
#     coffee_names = driver.find_elements(by=By.CLASS_NAME, value='text-h1 text-white font-bold')
#     for name in coffee_names:
#         coffee.append({'Name': name.text})
#
# pd.DataFrame(coffee_names)
