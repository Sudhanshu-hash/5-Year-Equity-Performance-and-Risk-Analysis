


import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.types import Date, Float, BigInteger, String
import pymysql
# 1. DATABASE CONNECTION 

DB_USER = 'root'
DB_PASSWORD = '152005'
DB_HOST = 'localhost'
DB_PORT = 3306
DB_NAME = 'stock_analysis_db'

CONNECTION_STRING = (
    f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
)
engine = create_engine(CONNECTION_STRING)
print(" Database engine created successfully.")

# 2. LOAD AND UPLOAD: cleaned_stock_data.csv
DAILY_PRICES_TABLE = 'daily_prices'
df_cleaned = pd.read_csv("cleaned_stock_data.csv")
df_cleaned['date'] = pd.to_datetime(df_cleaned['date'], format='%d-%m-%Y', errors='coerce')
df_cleaned.dropna(subset=['date'], inplace=True)
daily_dtype = {
        'date': Date,
        'open': Float(precision=4, asdecimal=True),
        'high': Float(precision=4, asdecimal=True),
        'low': Float(precision=4, asdecimal=True),
        'close': Float(precision=4, asdecimal=True),
        'volume': BigInteger,
        'Name': String(10),
        'Daily_Return': Float(precision=6, asdecimal=True),
        'Daily_Change': Float(precision=4, asdecimal=True),
        'Percent_Change': Float(precision=6, asdecimal=True),
    }

print(f" Starting robust upload of daily data to table: {DAILY_PRICES_TABLE}...")
df_cleaned.to_sql(
        name=DAILY_PRICES_TABLE,
        con=engine,
        if_exists='replace', 
        index=False,
        chunksize=5000,
        dtype=daily_dtype
    )
print(f" Success! Daily price data loaded into table '{DAILY_PRICES_TABLE}'.")

# 3. LOAD AND UPLOAD: stock_summary_analysis.csv
SUMMARY_TABLE = 'stock_summary'
df_summary = pd.read_csv("stock_summary_analysis.csv")
print(f"\nLoaded '{df_summary.shape[0]}' summary analysis rows.")
summary_dtype = {
        'Name': String(10),
        'Cumulative_Return_Pct': Float(precision=4, asdecimal=True),
        'Volatility': Float(precision=6, asdecimal=True),
        'total_volume': BigInteger,
    }
print(f" Starting upload of summary data to table: {SUMMARY_TABLE}...")

df_summary.to_sql(
        name=SUMMARY_TABLE,
        con=engine,
        if_exists='replace',
        index=False,
        dtype=summary_dtype
    )
print(f"Success! Summary analysis data loaded into table '{SUMMARY_TABLE}'.")