def main():
    # import pandas, time, and webdriver of selenium, with all the needed functions
    import pandas as pd
    import time
    from selenium import webdriver
    from selenium.common import NoSuchElementException
    from selenium.webdriver.common.by import By
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

    # Specifying the shop URL's of the coffee roastery,
    # list is expandable for the future and writes
    # each scraping into a new csv file. Rule the current
    # url of the productive shop, has to be the first element in the list.

    # the web.archive provides an older version of the same website, with partly various prices.
    page_urls = ['https://www.rastshop.ch/de', 'https://web.archive.org/web/20220118213133/https://www.rastshop.ch/de']

    # ---------------setup finished--------
    # get URL and open browser to start scrapping - loop takes first url, uses index to name the csv output
    # using python enumerate function
    for index, item in enumerate(page_urls):

        # install fresh webdriver
        driver = webdriver.Chrome(options=chrome_options)

        # using item to get driver to the right page
        driver.get(item)

        # Click on Accept cookies to get the banner away, as it can interfere with the driver
        # Set 2 seconds for a buffer to wait till everything is loaded
        time.sleep(2)
        # path of button to click accept
        driver.find_element(By.XPATH, '//*[@id="app"]/footer/div/div[3]/div[2]/button').click()

        # find URLs of coffees offered and the adding the timestamp
        coffee_links = driver.find_elements(by=By.CLASS_NAME, value='rs-btn-white')

        coffee_urls = []  # empty list for the urls
        coffee_timestamp = []  # empty list for timestamps of scraping

        for link in coffee_links:  # loop to get each url
            url = link.get_attribute('href')  # get the URL attribute (href)
            coffee_urls.append({"url": url})  # append each URL into the empty list
            # add the timestamp for each capturing
            coffee_timestamp.append(pd.to_datetime('now', utc=True).tz_localize(None))
        # footer element at the bottom of the page uses same class name, this can be deleted
        del coffee_urls[-1]

        # the name of the coffee is in another object so the xpath methode is used
        coffee_names = driver.find_elements(by=By.XPATH, value='//h3')
        coffee_title = []  # empty list for the names
        for name in coffee_names:  # loop to get each name
            title = name.text  # get the text of this element
            coffee_title.append(title)  # add to list
        # footer element at the bottom of the page uses same relative xpath, this can be deleted
        del coffee_title[-1]

        # Country and type of coffee information from overview page
        coffee_typ_origins = []
        coffee_country = driver.find_elements(
            by=By.CLASS_NAME,  # get value by class name within the card element
            value='absolute.text-small.left-2.bottom-1.text-beige-hue3.tracking-wider')
        for location in coffee_country:  # looping through all the elements
            origin = location.text
            # appending it to the empty list, currently country and type remain in one field
            coffee_typ_origins.append(origin)

        # extract string for the description of the aromas of the coffees from overview page
        coffee_aromas = []  # empty list to fill
        aroma_path = driver.find_elements(
            # search elements by xpath
            by=By.XPATH, value='//*[@id="app"]/main/div[*]/div/div[*]/div[*]/div[*]/div/div[*]/div/dl/div[1]/dd')

        for aroma in aroma_path:
            # get the information out of the inner HTML
            aroma = aroma.get_attribute("innerHTML")
            # append to the empty list
            coffee_aromas.append(aroma)

        # price information

        # first for standard size of 250g (default value by webpage)
        coffee_price_250 = []
        # in a second step the price for 1000g gets added too
        coffee_price_kg = []
        # defining path to the dropdown element with xpath
        dropdown = driver.find_elements(by=By.XPATH, value="//*[contains(text(),'250 g')]")
        for i in dropdown:
            # getting standard price for 250g as default
            price = i.text
            # and saving it in the 250 g ist
            coffee_price_250.append(price)
            # then click on the dropdown element with .click
            i.click()
            # wait to open and adjust for one second
            time.sleep(1)
            # get the value of the 1000g out of the dropdown list, as the element has to be opened to
            # show information in the DOM
            coffee_price_path = driver.find_element(by=By.XPATH, value="//*[contains(text(), '1 kg')]")
            # get information
            price_kg = coffee_price_path.text
            # append it to the kg list
            coffee_price_kg.append(price_kg)

        # add lists from the scrapped data into a pandas dataframe, which will be
        # expanded with more data from the specific coffee detail pages
        coffees = pd.DataFrame(
            list(zip(coffee_title, coffee_aromas, coffee_urls,
                     coffee_typ_origins, coffee_price_250,
                     coffee_price_kg, coffee_timestamp)),
            columns=['name', 'taste', 'url', 'typ_origin', 'price_250g', 'price_1000g', 'timestamp'])
        # adding a column with information about retailer. As all the coffees are from one
        # producer this value is fixed.
        coffees["retailer"] = 'Rast Kaffee'

        # ------------detail page scraping starts here------------

        # Links for the detail pages aren't existing for archive.org pages, therefore
        # checking if index of urls is larger than zero.  If it is zero, it scrapes all the details.
        if index > 0:
            # for the wayback machine this is the final stage of scraping, the csv is produced
            # string formatting in case more than one archive page is scrapped.
            coffees.to_csv("coffee_raw_wayback_{}_stage1.csv".format(index))
        else:
            # for the current productive webpage at rastshop.ch three more details are scrapped
            # three empty lists for the information of the detail page
            coffee_roast_level = []
            coffee_label = []
            coffee_chart = []

            # loop through the captured urls from the overview page
            for i in coffee_urls:
                # use the urls for the driver to visit each of the detail page, it is saved as dictionary
                driver.get(i['url'])
                roastlevel_path = driver.find_elements(
                    by=By.XPATH,
                    value='//*[@id="app"]/main/section[2]/div/div[1]/div[2]/div[2]/div[1]/div/div')
                t = []
                for path in roastlevel_path:
                    if roastlevel_path:
                        # getting css style information, as it is providing the roast level. It is
                        # displayed on a graphic element on the page
                        roast_level = path.get_attribute('style')
                        t.append(roast_level)
                    else:
                        # checking if element is existing
                        # if not use NaN as value
                        t.append("NaN")

                coffee_roast_level.append(t)

                # catching the chart values with detailed statistics about each coffee.
                # this information is displayed in a html canvas,
                # which is hard to scrap similar to a picture element,
                # luckily the information can be gained
                # from the javascript which creates the canvas element
                try:
                    # path shows to the chartjs script
                    chart_path = driver.find_element(by=By.XPATH, value="/html/body/script[4]")
                    chart = chart_path.get_attribute("innerHTML")  # getting complete javascript
                except NoSuchElementException:
                    chart = "NaN"  # if chartjs isn't present, it files NaN value
                coffee_chart.append(chart)  # append it to the empty chart list

                # labels
                # using if-else loop as only a minority (less than 50%) of
                # entries have one or more labels - therefore more efficient

                # identify element
                label_path = driver.find_elements(by=By.XPATH, value="//*[contains(text(), 'Label')]")
                # helping variable as more than one element can be found on a single page
                # coffees can be bio and fair trade, this information is in two elements
                p = []
                for label in label_path:
                    if label_path:
                        # label stores all the elements of a single page
                        label = label.text
                        # p creates then the entry in the list coffee_label
                        p.append(label)
                    else:
                        # if no labels are found it uses "NaN"
                        p.append("NaN")

                coffee_label.append(p)

            # closing selenium
            driver.close()
            # adding the lists with the values from the overview page together
            coffees['label'] = coffee_label
            coffees['roastlevel'] = coffee_roast_level
            coffees['chartjs'] = coffee_chart

            # creating csv files for all the pages the driver is visiting
            coffees.to_csv("coffee_raw_rast_{}_stage1.csv".format(index))


if __name__ == "__main__":
    main()
