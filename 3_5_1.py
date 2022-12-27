import sqlite3
import pandas as pd


def create_database_table():
    engine = sqlite3.connect('currency_by_month.db')
    df = pd.read_csv("currency_by_month.csv")
    df.to_sql("currency", con=engine, index=False)


create_database_table()
