def main():
    import pandas as pd
    import scraping_one
    import cleaning
    import numpy as np

    # run the two scripts for scraping the data and cleaning them.
    # Producing 4 files in total, two raw files
    # can be commented out if files already exist

    scraping_one.main()

    # and two cleaned csv files
    # can be commented out if files already exist

    cleaning.main()

    # read the cleaned csv files from the other scripts. One for the current rast homepage
    rast = pd.read_csv("coffee_cleaned_rast_stage2.csv")
    # and one for the archive.org from the wayback machine
    wayback = pd.read_csv("coffee_cleaned_wayback_stage2.csv")
    # merge the two files with a left join, to add the different prices form the archive file,
    # the ID isn't publicly available for these products, therefore the name column was chosen.
    merged = pd.merge(rast,
                      wayback[['name', 'price_250_wayback', 'price1000_wayback']],
                      on='name',
                      how='left')
    merged = merged.reindex(columns=[
        'retailer', 'name', 'type', 'price1000', 'currency',
        'taste', 'bitterness', 'acidity', 'roastlevel_cat',
        'country1', 'country2', 'country3', 'url', 'timestamp',
        'country4', 'country5', 'label', 'price250', 'price_250_wayback',
        'price1000_wayback', 'origin_list', 'roastlevel', 'sweetness',
        'floweriness', 'fruitiness', 'nutty', 'spicy', 'roasty', 'body', 'finish'
    ])
    # set index to one
    merged.index = np.arange(1, len(merged) + 1)

    # write data in one csv file - result of scraping and cleaning process
    merged.to_csv("merged_final_coffee.csv")


if __name__ == "__main__":
    main()
