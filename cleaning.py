import scrapping_rast
import pandas as pd
import numpy as np


# import csv files from the exports
raw = pd.read_csv("coffee_rast_raw.csv")
# quick look at the data
print(raw.head(4))

# cleaning starts

# removing unwanted {url: } part in the url column
raw['url'] = raw['url'].str.rstrip("'}").str.lstrip("{'url': '")

# split pricing into multiple columns from one column like 250g à 10.00 CHF into 3 columns for weight, numeric price
# and currency

#first we spllit weight and price

raw[['Weight250', "price250gcurrency"]]= raw.price_250g.str.split('à ', expand=True)

#split price in two columns currency and numeric value
raw[['curreny', "price250"]]= raw.price250gcurrency.str.split(' ', expand=True)

#remove the g in the weight column
raw['Weight250'] = raw['Weight250'].str.rstrip(" g ")

raw[['Weight1000', "price1000gcurrency"]]= raw.price_1000g.str.split('à ', expand=True)

#split price in two columns currency and numeric value
raw[['curreny', "price1000"]]= raw.price1000gcurrency.str.split(' ', expand=True)

#remove the g in the weight column
raw['Weight1000'] = raw['Weight1000'].str.rstrip(" g ")

# splitting the information in the origin_typ field into two separate fields
raw[['typ', 'origin_list']]= raw.typ_origin.str.split(pat="\n", expand=True)
raw = raw.drop('typ_origin', axis=1)
# additional normalizing of origin_list into multiple column

# drop columns which aren't needed anymore
raw = raw.drop(raw.columns[[0, 4, 5, 10, 14]], axis=1)

raw.to_csv("coffee_rast_cleaned.csv")

