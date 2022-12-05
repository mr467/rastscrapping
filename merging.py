def main():
    import pandas as pd
    from currency_converter import CurrencyConverter as c


    def poundsToGrams(pounds):
        kilograms = pounds / 2.2
        grams = kilograms * 1000
        return int(grams % 1000)


    poundsToGrams(1)


if __name__ == "__main__":
    main()
