# -----------------------------------------------------------
# Stock Data Analytics Project
# Tools: Python (Pandas, NumPy)
# Goal: Clean stock data, handle missing values, calculate
#       daily returns, volatility, cumulative returns, and
#       aggregated summaries for Power BI / MySQL / Excel.
# -----------------------------------------------------------

import pandas as pd
import numpy as np

# Load Data
df = pd.read_csv("all_stocks_5yr.csv")

# Convert 'date' column to datetime
df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y', errors='coerce')

# Sort by stock name and date (important for time-series)
df = df.sort_values(by=['Name', 'date']).reset_index(drop=True)

# Handle Missing Values
price_cols = ['open', 'high', 'low', 'close']

# Forward-fill missing prices *within each stock group*
df[price_cols] = df.groupby('Name')[price_cols].ffill()

# Drop any remaining rows missing essential price values
df.dropna(subset=price_cols, inplace=True)

# Optional: Fill any missing volume values with median
df['volume'] = df['volume'].fillna(df['volume'].median())

# Feature Engineering 
# Calculate daily percentage return for each stock
df['Daily_Return'] = df.groupby('Name')['close'].pct_change()

# Add helpful metrics for BI analysis
df['Daily_Change'] = df['close'] - df['open']
df['Percent_Change'] = ((df['close'] - df['open']) / df['open']) * 100

#Aggregation: Volatility & Cumulative Return 
def calculate_performance(group):
    """Calculates volatility and cumulative return for a single stock."""
    volatility = group['Daily_Return'].std()
    cumulative_return = (group['Daily_Return'] + 1).prod() - 1
    return pd.Series({
        'Volatility': volatility,
        'Cumulative_Return': cumulative_return
    })

performance_df = df.groupby('Name').apply(calculate_performance).reset_index()
performance_df['Cumulative_Return_Pct'] = (performance_df['Cumulative_Return'] * 100).round(2)
performance_df['Volatility'] = performance_df['Volatility'].round(6)

# Aggregation: Company Summary for Power BI ---
summary_df = df.groupby('Name').agg(
    avg_open=('open', 'mean'),
    avg_close=('close', 'mean'),
    max_high=('high', 'max'),
    min_low=('low', 'min'),
    total_volume=('volume', 'sum'),
    avg_percent_change=('Percent_Change', 'mean')
).reset_index()

# Merge both analytics into one table
final_summary = pd.merge(summary_df, performance_df[['Name', 'Volatility', 'Cumulative_Return_Pct']], on='Name')

# Sort for presentation
final_summary_sorted = final_summary.sort_values(by='Cumulative_Return_Pct', ascending=False)

#  Save Outputs ---
df.to_csv("cleaned_stock_data.csv", index=False)       # Cleaned data (for MySQL / further use)
final_summary_sorted.to_csv("stock_summary_analysis.csv", index=False)  # Aggregated performance summary

print("\n✅ Cleaned dataset shape:", df.shape)
print("\n--- Top 5 Stocks by Cumulative Return ---")
print(final_summary_sorted.head(5))

print("\n--- Top 5 Stocks by Volatility ---")
print(final_summary_sorted.sort_values(by='Volatility', ascending=False).head(5))

print("\nFiles saved:")
print("cleaned_stock_data.csv  → full clean dataset")
print("stock_summary_analysis.csv  → summary for Power BI/MySQL/Excel")
