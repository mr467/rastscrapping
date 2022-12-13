def main():

    import numpy as np
    import pandas as pd
    import re
    import glob

    # import csv files from the exports
    files = glob.glob("coffee_raw_*.csv")
    for index, item in enumerate(files):
        raw = pd.read_csv(item)

    # ------------------Author of this code------------------
    # Student A: Rieder

    # -----------cleaning starts-----------

        # -----------url-----------
        # Print out to console to inform that cleaning script is started and running
        print("Cleaning in progress...")
        # removing unwanted {url: } part in the url column using r- and l-strip
        raw['url'] = raw['url'].str.rstrip("'}").str.lstrip("{'url': '")


        # -----------prices & weight-----------
        # 250g
        # split pricing into multiple columns from one column like 250g à 10.00 CHF
        # into 3 columns for weight, numeric price
        # and currency
        # first we split weight and price
        raw[['Weight250', "price250gcurrency"]] = raw.price_250g.str.split('à ', expand=True)

        # split price in two columns currency and numeric value
        raw[['currency', "price250"]] = raw.price250gcurrency.str.split(' ', expand=True)

        # remove the g in the weight column
        raw['Weight250'] = raw['Weight250'].str.rstrip(" g ")

        # similar for 1000g, the letter à can be used to separate these two information
        raw[['Weight1000', "price1000gcurrency"]] = raw.price_1000g.str.split('à ', expand=True)

        # split price in two columns currency and numeric value
        raw[['currency', "price1000"]] = raw.price1000gcurrency.str.split(' ', expand=True)

        # remove the g in the weight column
        raw['Weight1000'] = raw['Weight1000'].str.rstrip(" g ")
        # replace the 1 k information with 1000 as all information are in the same unit: g
        raw['Weight1000'] = raw['Weight1000'].replace(to_replace="1 k", value='1000')

        # -----------origin and typ-----------

        # splitting the information in the origin_typ field into two separate fields. Using string split
        raw[['type', 'origin_list']] = raw.typ_origin.str.split(pat="\n", expand=True)
        # dropping the original column as it isn't needed anymore
        raw = raw.drop('typ_origin', axis=1)
        # replacing empty spaces
        raw['origin_list'] = raw['origin_list'].str.replace(" ", "")
        # creating new columns and filling them with the values of the origin_list, splitting by the comma-separator
        raw[
            ['country1', 'country2',
             'country3', 'country4',
             'country5']
        ] = raw['origin_list'].str.split(',', expand=True)

        # -----------roastlevel-----------
        # these information are only available for the current page,
        # therefore the try-except handles missing values from the archive.org

        try:
            # first remove part of string to get only numeric value

            raw['roastlevel'] = raw['roastlevel'].str.rstrip("%;']").str.lstrip("['right: ")
            # adjust datatype to a numeric value
            raw['roastlevel'] = pd.to_numeric(raw['roastlevel'])
            # The roast level is shown on a visual element on the webpage,
            # displaying from the right side a marker (using negative values) on a "ruler" element,
            # indicating the percentage of the roast level.
            # But the information has to be corrected - to get the percentage from the left side
            # Correcting it in this way, as it is changed with a lambda function.
            # original value of -55 will be corrected into 45
            raw['roastlevel'] = raw['roastlevel'].apply(lambda x: x * (-1) + 100)

            # new column with standardized categories for comparing with other data and roasteries
            roastlevel = raw['roastlevel']
            # creating a list for the values of the categories
            cond_list = [roastlevel < 20.00, roastlevel < 40.00, roastlevel < 60.00,
                         roastlevel < 80, roastlevel >= 80]
            # simplifying the naming of the roast level values, same scale as other roastery.
            choice_list = ["1", "2", "3", "4", "5"]
            # new column with a categorical value, based of the original percent values.

            raw["roastlevel_cat"] = np.select(cond_list, choice_list)

            # -----------labels-----------

            # first filling NaN values correctly
            raw['label'] = raw['label'].replace(to_replace="['']", value='NaN')
            # left and right side get cleaned
            raw['label'] = raw['label'].str.lstrip("['").str.rstrip("', '']")
            # replace label to get just the values
            raw['label'] = raw['label'].str.replace("Label ", "")
            raw['label'] = raw['label'].str.replace("', '", ", ")

            # -----------chart-----------
            # looping through chart rows, filtering for first [] brackets
            chart_raw_values = []
            for row in raw['chartjs']:
                # regex is used to remove outer brackets
                re.sub(r"[\[\]]", '', row)
                # find() method will search the row and store the first index
                mk1 = row.find('[') + 1
                # find() method will search the row and store the second index
                mk2 = row.find(']', mk1)
                # using slicing to get the values between the two markers
                values = row[mk1: mk2]
                chart_raw_values.append(values)
            raw['chart_values'] = chart_raw_values

            # list for labels for naming the new columns, in the correct order.
            # Order is found on the webpage displayed in the radar plot
            chart_labels = ["sweetness", "bitterness", "floweriness", "fruitiness", "nutty", "spicy", "roasty", "body",
                            "finish", "acidity"]

            # split by comma and use labels for naming
            raw[chart_labels] = raw['chart_values'].str.split(',', expand=True)

            # dropping non needed columns, as these aren't used for the
            # analysis and will therefore not be uploaded
            raw = raw.drop(['Unnamed: 0', 'price_250g', 'price_1000g',
                            'chartjs', 'chart_values', 'price1000gcurrency',
                            'price250gcurrency'], axis=1)

            # write data from the current rast page in csv file
            raw.to_csv("coffee_cleaned_rast_stage2.csv")
        except KeyError:
            # on archive.org page the roast level, labels and chart values aren't available,
            # the wayback csv can be created instead
            raw = raw.drop(['Unnamed: 0', 'price_250g', 'price_1000g',
                            'price1000gcurrency', 'price250gcurrency'], axis=1)

            # rename column for price to make it different to current price
            raw = raw.rename(columns={"price1000": "price1000_wayback", "price250": "price_250_wayback"})

            # write csv file for wayback machine
            raw.to_csv("coffee_cleaned_wayback_stage2.csv")


if __name__ == "__main__":
    main()
