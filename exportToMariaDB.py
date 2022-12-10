def main():
    # Module Imports
    import mariadb
    import sys
    import pandas as pd
    from sqlalchemy import create_engine
    import pymysql

    # Connect to MariaDB Platform
    try:
        conn = mariadb.connect(
            user="MRieder",
            password="8.1mangObauM",
            host="localhost",
            port=3306,
            database="CIP"

        )
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)

    # Get cursor to communicate with the database
    cursor = conn.cursor()

    cursor.execute("select database();")
    record = cursor.fetchone()
    print("You're connected to database: ", record)
    cursor.execute('DROP TABLE IF EXISTS RAST_COFFEE_STAGE_Marco')
    print('Creating table....')

    rast = pd.read_csv('merged_final_coffee.csv')
    # create table in our database
    cursor.execute(
                "CREATE TABLE RAST_COFFEE_STAGE_Marco (`Unnamed: 0` INT, retailer VARCHAR(255), name VARCHAR(255), "
                "type VARCHAR(255), price1000 NUMERIC(5,2), "
                "currency VARCHAR(255), taste VARCHAR(255), "
                "bitterness INT, acidity INT, "
                "roastlevel_cat INT, country1 VARCHAR(255), "
                "country2 VARCHAR(255), country3 VARCHAR(255), "
                "url VARCHAR(255), timestamp DATETIME, "
                "country4 VARCHAR(255), country5 VARCHAR(255), "
                "label VARCHAR(255), price250 NUMERIC(5, 2), "
                "price_250_wayback NUMERIC(5, 2), price1000_wayback NUMERIC(5, 2), "
                "origin_list VARCHAR(255), roastlevel NUMERIC(5,2),"
                "sweetness INT, floweriness INT,"
                "fruitiness INT, nutty INT, "
                "spicy INT, roasty INT, "
                "body INT, finish INT)"
    )

    print("Table is created....")

    # create sqlalchemy engine
    engine = create_engine(
        "mariadb+pymysql://{user}:{pw}@localhost:3306/{db}".
        format(user="MRieder", pw="8.1mangObauM",
               db="CIP"))

    # Insert whole DataFrame into MySQL
    rast.to_sql('RAST_COFFEE_STAGE_Marco', con=engine, if_exists='append', index=False)

    print("process is done")
if __name__ == "__main__":
    main()
