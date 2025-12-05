## Sector Analysis & Seasonality Research Module

### Overview:
1. Introduces a complete Sector Rotation & Seasonality Analysis framework into the project.
2. It includes automated data extraction from Kite APIs, weekly → monthly candle conversion, sector mapping, and a hypothesis engine for identifying high-performing months for each sector and stock.
---------------------------------------------------------------
### Folder: data_sectors/

This folder now contains all sector-related datasets used for analysis:

File	Description:
1. sectors.csv	Maps NSE sectors to their respective list of stocks (e.g., NIFTY IT, NIFTY BANK, etc.).
2. NSE_instruments.csv	Full list of NSE instruments used for filtering sector constituents.
3. *_weekly.csv	Auto-generated weekly OHLC datasets for each sector (e.g., it_weekly.csv).
4. *_monthly.csv	Derived monthly candles created from weekly data (e.g., it_monthly.csv).
These datasets are used for seasonality modeling, sector rotation, and statistical hypothesis testing.
-------------------------------------------------------------
### Script: get_sectors.py

This module handles:
1. Loading sector → stock mappings
2. Extracting instrument tokens
3. Fetching 3 years of weekly historical data from Kite
4. Saving sector-wise weekly OHLC datasets
5. Converting weekly candles into monthly candles for seasonality analysis
6. It ensures rate-limiting safety for API calls and is fully automated for all sectors.

### Script: hypothesis.py

This script is responsible for:
1. Reading it_monthly.csv (or any other sector)
2. Computing monthly percentage returns for every stock
3. Aggregating results across years
4. Generating Sector Seasonality Heatmaps
5. Producing Stock-wise Seasonality Heatmaps
---------------------------------------------------------------
### Findings Included

1. The hypothesis confirms strong seasonality patterns — especially for NIFTY IT, which historically performs best in: June, August, November
2. These findings support the sector rotation thesis and can be used to position trades ahead of seasonal strength.
------------------------------------------------------------------------------
### What This Module Enables:

By integrating these scripts and datasets, the project now supports:
1. Multi-sector seasonality analysis
2. Monthly return forecasting
3. Sector rotation dashboards
4. Heatmap-based visualization of market cycles
5. Data-driven hypothesis testing for swing trading & portfolio allocation
------------------------------------------------------------------------
### How to Run:

1. Extract Sector Data
  python get_sectors.py
2. Generate Monthly Candles
  Automatically runs inside the extraction pipeline or can be called separately:
    python hypothesis.py

3. View Heatmaps
  The script displays:
    Sector Seasonality
    Individual Stock Seasonality
  --------------------------------------------------------------------------------------------
