def main():
    import pandas as pd
    import scraping_one
    import cleaning

    # run the two scripts for scraping the data and cleaning them.
    #scraping_one.main()
    cleaning.main()

    # read the cleaned csv files from the other scripts
    rast = pd.read_csv("coffee_cleaned_rast_1.csv")
    wayback = pd.read_csv("coffee_cleaned_wayback_0.csv")
    # merge the two files with a left join, to add the different prices form the archive file,
    # the id of these products, isn't used, therefore the name column was chosen.
    merged = pd.merge(rast,
                      wayback[['name', 'price_250_wayback', 'price1000_wayback']],
                      on='name',
                      how='left')
    merged = merged.reindex(columns=['retailer', 'name', 'type', 'price1000', 'currency', 'taste', 'bitterness',
                     'acidity', 'roastlevel_cat', 'country1', 'country2', 'country3',
                     'url', 'timestamp',
                            'country4', 'country5','price250', 'price_250_wayback', 'price1000_wayback',
                     'origin_list','sweetness', 'floweriness',
                            'fruitiness', 'nutty', 'spicy', 'roasty', 'body', 'finish'])
    merged.to_csv("merged_coffee.csv")


if __name__ == "__main__":
    main()
