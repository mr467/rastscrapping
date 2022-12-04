import scrapping_rast
import pandas as pd
import numpy as np


# import csv files from the exports
raw = pd.read_csv("coffee_rast1.csv")
print(raw.head(4))
raw[['typ', 'origin_list']]= raw.typ_origin.str.split(pat="\n", expand=True)
raw = raw.drop('typ_origin', axis=1)

for i in raw


raw.to_csv("test.csv")

