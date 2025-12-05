import pandas as pd
from datetime import datetime, timedelta
import time
import talib as ta
from nselib import capital_market as cm
import nsepython as nse
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


df = pd.read_csv(r"data_sectors\sector_monthly.csv")
df['date'] = pd.to_datetime(df['date'])
df['month'] = df['date'].dt.month
df['year'] = df['date'].dt.year
df['date'] = pd.to_datetime(df['date']).dt.date
df = df[['symbol','date','month','year','close']]
df['returns'] = df.groupby('symbol')['close'].pct_change()
df['returns'] = df['returns']*100
#print(df.head())
seasonality = df.groupby(['symbol','month'])['returns'].mean().reset_index()
seasonality_pivot = seasonality.pivot(index='symbol', columns='month', values='returns')
#print(seasonality_pivot.head())
#seasonality_pivot.to_csv(r"data_sectors\seasonality.csv")
plt.figure(figsize=(14,8))
sns.heatmap(seasonality_pivot, cmap="RdYlGn", annot=True, fmt=".1f", center=0)
plt.title("Sector Seasonality Heatmap (%)")
plt.xlabel("Month")
plt.ylabel("Sector")
plt.show()