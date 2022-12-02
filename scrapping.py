def main():
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
    chrome_options.add_argument("--headless")  # Ensure GUI is off
    chrome_options.add_argument("--no-sandbox")

    # Silent download of drivers
    logging.getLogger('WDM').setLevel(logging.NOTSET)
    os.environ['WDM_LOG'] = 'False'

    # Create service
    webdriver_service = Service(ChromeDriverManager().install())

    # Create driver
    driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)

    # URL of coffee roastery displaying all the coffees available
    page_url = 'https://www.rastshop.ch/de'

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(page_url)

    # # Click on Accept cookies
    time.sleep(5)
    driver.find_element(By.XPATH, '//*[@id="app"]/footer/div/div[3]/div[2]/button').click()

    # find URLs of coffees currently offered
    coffee_links = driver.find_elements(by=By.CLASS_NAME, value='rs-btn-white')

    coffee_urls = []  # empty list for the urls
    for link in coffee_links:  # loop to get each url
        url = link.get_attribute('href')
        coffee_urls.append({"url": url})

    # the name of the coffee is in another object so the xpath methode is used
    coffee_names = driver.find_elements(by=By.XPATH, value='//h3')
    coffee_titel = []  # empty list for the names
    for name in coffee_names:  # loop to get each name
        titel = name.text
        coffee_titel.append({titel})

    # Country information from overview page
    coffee_origins = []
    coffee_country = driver.find_elements(
        by=By.CLASS_NAME,
        value='absolute.text-small.left-2.bottom-1.text-beige-hue3.tracking-wider')
    for location in coffee_country:
        origin = location.text
        coffee_origins.append({origin})

    #extract aromatics from overview page
    coffee_aromas = []
    aroma_path = driver.find_elements(
        by=By.XPATH,value='//*[@id="app"]/main/div[*]/div/div[*]/div[*]/div[*]/div/div[*]/div/dl/div[1]/dd')
    for aroma in aroma_path:
        aroma = aroma.get_attribute("innerHTML")
        coffee_aromas.append(aroma)

    # price information
    # coffee_price_kilo = []
    # dropdown = driver.find_elements(by=By.CLASS_NAME, value='vs__dropdown-toggle')
    # coffee_price_path = driver.find_elements(by=By.XPATH, value="//a[contains(text(), '1 kg')]")
    # for element in dropdown:
    #     try:
    #         element.click()
    #         for price in coffee_price_path:
    #             time.sleep(3)
    #             coffee_price = price.text
    #             coffee_price_kilo.append({coffee_price})
    #     except:
    #         print("An exception occurred")

    # delete last element as it isn't a coffee type
    del coffee_titel[-1]
    del coffee_urls[-1]

    # clean country and split classification in new row

    # add list into a pandas dataframe which will be expanded with more data from the specific coffee detailpages
    # coffees = pd.DataFrame(list(zip(coffee_titel, coffee_urls)), columns=['name','url'])
    # coffees.to_csv("coffee_rast.csv")

    coffee_price = []
    coffee_flavours = []
    coffee_roastlevel = []
    coffee_label = []

    for i in coffee_urls:
        # go to each detail page and get information
        driver.get(i['url'])
        roastlevel_path = driver.find_elements(
            by=By.XPATH,
            value = '//*[@id="app"]/main/section[2]/div/div[1]/div[2]/div[2]/div[1]/div/div')
        for roastlevel in roastlevel_path:
            roastlevel = roastlevel.get_attribute('style')
            coffee_roastlevel.append(roastlevel)

        # labels
        #using if-else loop as only a minority (less than 50%) of
        # entries have one or more labels - therefore more efficient

        # identify element
        label_path = driver.find_elements(by=By.XPATH, value="//*[contains(text(), 'Label')]")
        for i in label_path:
        # get list size with len
            s = len(label_path)
        # check condition, if list size > 0, element exists
            if (s > 0):
                label = i.text
                coffee_label.append(label)
            else:
                coffee_label.append("NaN")

        # origin_path = driver.find_element(by=By.XPATH, value='//*[@id="app"]/header/div[1]/div/div[3]/div[2]/div[1]/div[1]/h3')
        # origin = origin_path.text

        # driver.find_element(by= By.ID, value='vs1__combobox').click()
        # driver.find_element(by=By.ID, value="vs1__option-3").click()
        # price = driver.find_element(by=By.XPATH, value='//*[@id="vs1__combobox"]/div[1]/span')

        # driver.quit()
        # coffee_titel.append({origin,aroma,flavour,price})

    coffees = pd.DataFrame(
        list(zip(coffee_titel, coffee_urls, coffee_origins, coffee_aromas, coffee_roastlevel, coffee_label)),
        columns=['name', 'url', 'country', 'aroma', 'coffee_roastlevel', 'label'])
    coffees.to_csv("coffee_rast.csv")

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


if __name__ == "__main__":
    main()
