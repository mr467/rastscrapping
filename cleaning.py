def main():

    import numpy as np
    import pandas as pd
    import re
    import glob

    # import csv files from the exports
    files = glob.glob("coffee_raw_*.csv")
    for index, item in enumerate(files):
        raw = pd.read_csv(item)

    # -----------cleaning starts-----------

    # add row with source

    # -----------url-----------
        # removing unwanted {url: } part in the url column
        raw['url'] = raw['url'].str.rstrip("'}").str.lstrip("{'url': '")
        # -----------prices & weight-----------
        # 250g
        # split pricing into multiple columns from one column like 250g à 10.00 CHF into 3 columns for weight, numeric price
        # and currency

        # first we spllit weight and price
        raw[['Weight250', "price250gcurrency"]] = raw.price_250g.str.split('à ', expand=True)

        # split price in two columns currency and numeric value
        raw[['curreny', "price250"]] = raw.price250gcurrency.str.split(' ', expand=True)

        # remove the g in the weight column
        raw['Weight250'] = raw['Weight250'].str.rstrip(" g ")

        # similar for 1000g
        raw[['Weight1000', "price1000gcurrency"]] = raw.price_1000g.str.split('à ', expand=True)

        # split price in two columns currency and numeric value
        raw[['curreny', "price1000"]] = raw.price1000gcurrency.str.split(' ', expand=True)

        # remove the g in the weight column
        raw['Weight1000'] = raw['Weight1000'].str.rstrip(" g ")
        raw['Weight1000'] = raw['Weight1000'].replace(to_replace="1 k", value='1000')

        # -----------origin and typ-----------

        # splitting the information in the origin_typ field into two separate fields
        raw[['typ', 'origin_list']] = raw.typ_origin.str.split(pat="\n", expand=True)
        raw = raw.drop('typ_origin', axis=1)
        raw['origin_list'] = raw['origin_list'].str.replace(" ", "")

        raw[['country1', 'country2', 'country3', 'country4', 'country5']] = raw['origin_list'].str.split(',', expand=True)

        # -----------roastlevel-----------
        # these infomation are only available for the current page,
        # therefore the try-except handels missing values from the archive.org

        try:
            # first remove part of string to get only nummeric value

            raw['roastlevel'] = raw['roastlevel'].str.rstrip("%;']").str.lstrip("['right: ")
            # adjust datatype to float
            raw['roastlevel'] = pd.to_numeric(raw['roastlevel'])
            # roastlevel is shown on a scale pointing from the right side. Correcting it in this way
            raw['roastlevel'] = raw['roastlevel'].apply(lambda x: x * (-1) + 100)

            # new column with standardized categories for comparing with other data and roasteries

            roastlevel = raw['roastlevel']

            cond_list = [roastlevel < 20.00, roastlevel < 40.00, roastlevel < 60.00, roastlevel < 80, roastlevel >= 80]
            choice_list = ["1", "2", "3", "4", "5"]

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
                re.sub(r"[\[\]]", '', row)

                # find() method will search the row and store the first index
                mk1 = row.find('[') + 1
                # find() method will search the row and store the second index
                mk2 = row.find(']', mk1)
                # using slicing to get the values between the two markers
                values = row[mk1: mk2]
                chart_raw_values.append(values)
            raw['chart_values'] = chart_raw_values

            # list for labels for naming the new columns, in the correct order
            chart_labels = ["Süsse", "Bitterkeit", "Blumig", "Fruchtig", "Nussig", "Würzig", "Röstartig", "Körper",
                            "Abgang", "Säure"]

            # split by comma and use labels for naming
            raw[chart_labels] = raw['chart_values'].str.split(',', expand=True)

            # droping non needed columns
            raw = raw.drop(['Unnamed: 0', 'price_250g', 'price_1000g', 'chartjs', 'chart_values', 'price1000gcurrency', 'price250gcurrency'], axis=1)


            #write data in csv file
            raw.to_csv("coffee_cleaned_rast_{}.csv".format(index))
        except KeyError:
            #on archive.org page the roastlevel, labels and chart values aren't avaible,
            # the wayback csv can be created instead
            raw = raw.drop(['Unnamed: 0', 'price_250g', 'price_1000g', 'price1000gcurrency', 'price250gcurrency'], axis=1)

            raw.to_csv("coffee_cleaned_wayback_{}.csv".format(index))

if __name__ == "__main__":
        main()
