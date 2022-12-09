

def main():
    import glob
    import pandas as pd
    import scraping_one
    import cleaning

    # run the two scripts for scraping the data and cleaning them.
    #scraping_one.main()
    cleaning.main()


    #
    rast = pd.read_csv("coffee_cleaned_rast_1.csv")
    wayback = pd.read_csv("coffee_cleaned_wayback_0.csv")
    merged = pd.merge(rast,
                      wayback[['name', 'Weight250', 'price250', 'Weight1000', 'price1000']],
                      on='name',
                      how='left')
    merged = pd.merge(rast,wayback, how="left", on="name")
    merged.to_csv("merged_coffee.csv")

if __name__ == "__main__":
    main()
