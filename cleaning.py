import scraping_rast
import pandas as pd
import numpy as np
import re


# import csv files from the exports
raw = pd.read_csv("coffee_rast_raw.csv")
# quick look at the data
print(raw.head(4))

# -----------cleaning starts-----------

# -----------url-----------

# removing unwanted {url: } part in the url column
raw['url'] = raw['url'].str.rstrip("'}").str.lstrip("{'url': '")

# -----------prices-----------
# 250g
# split pricing into multiple columns from one column like 250g à 10.00 CHF into 3 columns for weight, numeric price
# and currency

#first we spllit weight and price
raw[['Weight250', "price250gcurrency"]]= raw.price_250g.str.split('à ', expand=True)

#split price in two columns currency and numeric value
raw[['curreny', "price250"]]= raw.price250gcurrency.str.split(' ', expand=True)

#remove the g in the weight column
raw['Weight250'] = raw['Weight250'].str.rstrip(" g ")

# similar for 1000g
raw[['Weight1000', "price1000gcurrency"]]= raw.price_1000g.str.split('à ', expand=True)

#split price in two columns currency and numeric value
raw[['curreny', "price1000"]]= raw.price1000gcurrency.str.split(' ', expand=True)

#remove the g in the weight column
raw['Weight1000'] = raw['Weight1000'].str.rstrip(" g ")


# -----------origin and typ-----------

# splitting the information in the origin_typ field into two separate fields
raw[['typ', 'origin_list']]= raw.typ_origin.str.split(pat="\n", expand=True)
raw = raw.drop('typ_origin', axis=1)

# -----------roastlevel-----------

#first remove part of string to get only nummeric value
raw['roastlevel'] = raw['roastlevel'].str.rstrip("%;']").str.lstrip("['right: ")
# adjust datatype to float
raw['roastlevel'] = pd.to_numeric(raw['roastlevel'])
# roastlevel is shown on a scale pointing from the right side. Correcting it in this way
raw['roastlevel'] = raw['roastlevel'].apply(lambda x: x * (-1)+100)

# -----------labels-----------

# first filling NaN values correctly
raw['label'] = raw['label'].replace(to_replace="['']", value= 'NaN')
#left and right side get cleaned
raw['label'] = raw['label'].str.lstrip("['").str.rstrip("', '']")
# replace label to get just the values
raw['label'] = raw['label'].str.replace("Label ", "")
raw['label'] = raw['label'].str.replace("', '", ", ")

# -----------chart-----------
# looping through chart rows, filtering for first [] brackets
chart_raw_values = []
for row in raw['chartjs']:
    brackets = re.findall(r'(?<=\[).+?(?=\])', row)
    chart_raw_values.append(brackets)


raw['chart_values'] = chart_raw_values
values = []
for row in raw['chart_values']:
    for n in row:
        int(filter(str.isdigit, just))

raw['chart_values'] = values
int(filter(str.isdigit, just))

# filter the first 10 values of each row

#list for labels
chart_labels = ["Süsse", "Bitterkeit", "Blumig", " Fruchtig", "Nussig", "Würzig", "Röstartig", "Körper",
                "Abgang", "Säure"]

raw.to_csv("coffee_rast_cleaned.csv")

