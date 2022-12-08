import glob


def main():
    import pandas as pd
    from currency_converter import CurrencyConverter as c


    def poundsToGrams(pounds):
        kilograms = pounds / 2.2
        grams = kilograms * 1000
        return int(grams % 1000)


    poundsToGrams(1)
    import pandas as pd
    # import csv files from the exports
    files = glob.glob("coffee_cleaned_*.csv")
    for index, item in enumerate(files):


    # Read the first CSV file into a DataFrame

    # Merge the two DataFrames based on a common column (e.g., "id")
    # The values from df1 will be preserved
        merged_df = pd.merge(df1, df2, on="id", how="left")

    # Save the merged DataFrame to a new CSV file
        merged_df.to_csv("merged.csv", index=False)


if __name__ == "__main__":
    main()
