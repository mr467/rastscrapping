# Rast Coffee scrapping

Welcome to my first web scraping project. This is part of a course at the HSLU Lucerne. 

## Goal

Scraping websites together with two colleagues and bringing all the information together to gain more knowledge.
We choose the topic of coffee. 
This part of the project shows the scraping of the Rast Roastery (www.rastshop.ch). The data cleaning and merging.
Analysis and merging with the other data is not part of this repository.

IMPORTANT: The coffees of RAST are great and tasty, you should try them out -> Here: www.rastshop.ch 

The scripts are in an order.

1. Scraping_one.py: uses selenium to get the information from the pages including the main page and the information on the wayback machine.
2. cleaning.py: The data from the selenium scrapping are mixed up and need preparation and cleaning. This script cleans, splits, replaces, extracts etc. the data.
3. merging.py: Merges the two information from the main page and the wayback machine. In this case it uses mainly price information to merge with the main page.

## Legal
The robots.txt file of rastshop.ch (www.rastshop.ch/robots.txt) allows bots to scrape the page, 
at the time this code was writen (December 2022). 
Always check if it is allowed, otherwise ask domain owners.