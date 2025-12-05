import pandas as pd
import numpy as np
import sqlite3
import talib as ta
from nselib import capital_market as cm
import nsepython as nse
from kiteconnect import KiteConnect
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import time
import seaborn as sns
import matplotlib.pyplot as plt

last_request_time = 0

def rate_limited_call():
    global last_request_time
    min_interval = 0.35
    now = time.time()
    wait_time = min_interval - (now - last_request_time)
    if wait_time > 0:
        time.sleep(wait_time)
    last_request_time = time.time()

def gen_ses():
    key = open(r"data\api.txt","r").read().split()
    kite = KiteConnect(api_key=key[0])
    kite.set_access_token(key[2])
    return kite

def get_data(kite, row, interval):
    try:
        to_date = datetime.now()
        from_date = to_date - relativedelta(years=3)

        rate_limited_call()  
        data = kite.historical_data(
            int(row['instrument_token']),
            from_date,
            to_date,
            interval
        )

        df = pd.DataFrame(data)
        if df.empty:
            return pd.DataFrame()

        df["symbol"] = row['tradingsymbol']
        df["instrument_token"] = row['instrument_token']
        df["interval"] = interval
        df = df[['symbol','instrument_token', 'date', 'open', 'high', 'low', 'close']]
        return df

    except Exception as e:
        print(f"Error for {row['tradingsymbol']} - {interval}: {e}")
        return pd.DataFrame()

def get_sectors_data(stock_df):
    kite = gen_ses()
    print("Kite Session Generated")

    sector_w = pd.DataFrame()
    total_stocks = len(stock_df)

    for i, row in stock_df.iterrows():
        temp = get_data(kite, row, "week")  # use month for seasonality
        sector_w = pd.concat([sector_w, temp], ignore_index=True)
        print(f"Processing {i+1}/{total_stocks}: {row['tradingsymbol']}")

    if not sector_w.empty:
        sector_w['date'] = pd.to_datetime(sector_w['date'])
        sector_w.to_csv(r"data_sectors\it_weekly.csv", index=False)
        print("it_weekly CSV saved.")
    else:
        print("Warning: No data fetched!")


def convert_to_month():
    df = pd.read_csv("data_sectors/it_weekly.csv")  
    df['date'] = pd.to_datetime(df['date'])

    monthly = (
        df.groupby('symbol')
        .resample('M', on='date')
        .agg({
            'open': 'first',
            'high': 'max',
            'low': 'min',
            'close': 'last'
        })
        .reset_index()
    )

    monthly['date'] = monthly['date'].dt.strftime('%Y-%m-%d')
    monthly.to_csv("data_sectors/it_monthly.csv", index=False)

    return monthly

def extract_sector():
    instruments = pd.read_csv(r"data_sectors\NSE_instruments.csv")
    sectors = pd.read_csv(r"data_sectors\sectors.csv")

    raw = sectors.loc[sectors['sector']=="NIFTY IT", 'symbols_list'].iloc[0]

    symbols = (
        raw.replace("[","")
           .replace("]","")
           .replace("'","")
           .replace(" ","")
           .split(",")
    )
    it_df = instruments[instruments['tradingsymbol'].isin(symbols)]
    #get_sectors_data(it_df)
    monthly_df  = convert_to_month()
    return monthly_df

if __name__ == "__main__":
    extract_sector()
    df = pd.read_csv(r"data_sectors\it_monthly.csv")
    df['date'] = pd.to_datetime(df['date'])
    df['month'] = df['date'].dt.month
    df['year'] = df['date'].dt.year
    df['date'] = pd.to_datetime(df['date']).dt.date
    df = df[['symbol','date','month','year','close']]
    df['returns'] = df.groupby('symbol')['close'].pct_change()
    df['returns'] = df['returns']*100
    seasonality = df.groupby(['symbol','month'])['returns'].mean().reset_index()
    seasonality_pivot = seasonality.pivot(index='symbol', columns='month', values='returns')
    plt.figure(figsize=(14,8))
    sns.heatmap(seasonality_pivot, cmap="RdYlGn", annot=True, fmt=".1f", center=0)
    plt.title("Seasonality Heatmap (%)")
    plt.xlabel("Month")
    plt.ylabel("IT")
    plt.show()
