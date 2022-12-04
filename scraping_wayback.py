def main():
    # import pandas, time, and webdriver of selenium, with all the needed functions
    import pandas as pd
    import time
    from selenium import webdriver
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    import os
    import logging

    # ------------Setup chrome options------------
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless")
    chrome_options.headless = True

    # Silent download of drivers
    logging.getLogger('WDM').setLevel(logging.NOTSET)
    os.environ['WDM_LOG'] = 'False'

    # Shop URL of coffee roastery displaying all the coffees available
    page_urls = ['https://www.rastshop.ch/de', 'https://web.archive.org/web/20220118213133/https://www.rastshop.ch/de']

    # ---------------setup finished--------
    # get URL and open browser to start scrapping - loop takes first url, uses index to name the csv output

    for index, item in enumerate(page_urls):

        # install fresh webdriver
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        driver = webdriver.Chrome(options=chrome_options)

        # using item to get driver to the page
        driver.get(item)

        # Click on Accept cookies to get the banner away  Set 2 seconds to wait till everything is loaded
        time.sleep(2)
        # path of button to click accept
        driver.find_element(By.XPATH, '//*[@id="app"]/footer/div/div[3]/div[2]/button').click()

        # find URLs of coffees currently offered
        coffee_links = driver.find_elements(by=By.CLASS_NAME, value='rs-btn-white')

        coffee_urls = []  # empty list for the urls
        for link in coffee_links:  # loop to get each url
            url = link.get_attribute('href') # get the URL attribute (href)
            coffee_urls.append({"url": url}) # append each URL into the empty list
        del coffee_urls[-1]

        # the name of the coffee is in another object so the xpath methode is used
        coffee_names = driver.find_elements(by=By.XPATH, value='//h3')
        coffee_titel = []  # empty list for the names
        for name in coffee_names:  # loop to get each name
            title = name.text # get the text of this element
            coffee_titel.append(title) # add to list
        del coffee_titel[-1]

        # Country information from overview page
        coffee_typ_origins = []
        coffee_country = driver.find_elements(
            by=By.CLASS_NAME,
            value='absolute.text-small.left-2.bottom-1.text-beige-hue3.tracking-wider')
        for location in coffee_country:
            origin = location.text
            coffee_typ_origins.append(origin)

        #extract aromatics from overview page
        coffee_aromas = []
        aroma_path = driver.find_elements(
            by=By.XPATH,value='//*[@id="app"]/main/div[*]/div/div[*]/div[*]/div[*]/div/div[*]/div/dl/div[1]/dd')
        for aroma in aroma_path:
            aroma = aroma.get_attribute("innerHTML")
            coffee_aromas.append(aroma)

        # price information

        #first for standard size of 250g (default value by webpage)
        coffee_price_250 = []
        coffee_price_kg = []
        dropdown = driver.find_elements(by=By.XPATH, value="//*[contains(text(),'250 g')]")
        for i in dropdown:
            price = i.text
            coffee_price_250.append(price)
            i.click()
            time.sleep(1)
            coffee_price_path = driver.find_element(by=By.XPATH, value="//*[contains(text(), '1 kg')]")
            price_kg = coffee_price_path.text
            coffee_price_kg.append(price_kg)

        # add lists from the scrapped data into a pandas dataframe, which will be
        # expanded with more data from the specific coffee detail pages
        coffees = pd.DataFrame(
            list(zip(coffee_titel, coffee_urls, coffee_typ_origins, coffee_aromas, coffee_price_250, coffee_price_kg)),
            columns=['name','url', 'typ_origin', 'taste', 'price_250g', 'price_1000g'])

    # ------------detailpage starts here------------

        # three empty lists for the information of the detail page
        coffee_roast_level = []
        coffee_label = []
        coffee_chart = []

        #loop through the captured urls from the overview
        for i in coffee_urls:
            # use the urls for the driver to visit
            driver.get(i['url'])
            roastlevel_path = driver.find_elements(
                by=By.XPATH,
                value = '//*[@id="app"]/main/section[2]/div/div[1]/div[2]/div[2]/div[1]/div/div')
            t=[]
            for i in roastlevel_path:
                if roastlevel_path:
                    roast_level = i.get_attribute('style')
                    t.append(roast_level)
                else:
                    t.append("NaN")

            coffee_roast_level.append(t)

            # chartvalues
            chart_path = driver.find_elements(by=By.XPATH, value="/html/body/script[4]")
            c = []
            for i in chart_path:
                if chart_path:
                    chart = i.get_attribute("innerHTML")
                    c.append(chart)
                else:
                    c.append("NaN")
            coffee_chart.append(c)

            # labels
            #using if-else loop as only a minority (less than 50%) of
            # entries have one or more labels - therefore more efficient

            # identify element
            label_path = driver.find_elements(by=By.XPATH, value="//*[contains(text(), 'Label')]")
            p=[]

            for i in label_path:

                if label_path:
                    label = i.text
                    p.append(label)
                else:
                    p.append("NaN")

            coffee_label.append(p)

        # closing selenium
        driver.close()
        # adding the lists with the values from the overview page together
        coffees['label'] = coffee_label
        coffees['roastlevel'] = coffee_roast_level
        coffees['chartjs'] = coffee_chart

        # creating csv files for all the pages the driver is visiting
        coffees.to_csv("coffee_raw_{}.csv".format(index))

if __name__ == "__main__":
    main()