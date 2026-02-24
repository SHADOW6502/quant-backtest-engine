import pandas as pd
import numpy as np

def bollinger_bands_strategy(data, window=20, num_std=2):
    """
    Vectorized Bollinger Bands Mean Reversion Strategy.
    Returns a Pandas Series representing the daily position (1, -1, or 0).
    """
    df = data.copy()
    
    # 1. Calculate the Rolling Mean and Standard Deviation
    df['SMA'] = df['Close'].rolling(window=window).mean()
    df['Std_Dev'] = df['Close'].rolling(window=window).std()
    
    # 2. Construct the Bands
    df['Upper_Band'] = df['SMA'] + (df['Std_Dev'] * num_std)
    df['Lower_Band'] = df['SMA'] - (df['Std_Dev'] * num_std)
    
    # 3. Generate Raw Signals using NaN for state retention
    # We use np.nan so we can later forward-fill our active positions
    df['Signal'] = np.nan 
    
    # Entry Rules: Price crosses outside the bands
    df.loc[df['Close'] <= df['Lower_Band'], 'Signal'] = 1  # Oversold -> Go Long
    df.loc[df['Close'] >= df['Upper_Band'], 'Signal'] = -1 # Overbought -> Go Short
    
    # Exit Rule: Price reverts to the mean (crosses the SMA)
    # np.sign() checks if the distance from SMA is positive or negative.
    # .diff().ne(0) flags exactly when that sign changes (a crossover).
    cross_condition = np.sign(df['Close'] - df['SMA']).diff().ne(0) & df['SMA'].notna()
    df.loc[cross_condition, 'Signal'] = 0
    
    # 4. Vectorized State Machine: Forward fill the signals
    # This holds the 1 or -1 position day-over-day until it hits a 0 (exit) or reverses.
    df['Position'] = df['Signal'].ffill().fillna(0)
    
    return df['Position']