import pandas as pd
import numpy as np

def ma_crossover_strategy(data, short_window=20, long_window=50):
    """
    Vectorized Moving Average Crossover Strategy.
    Returns a Pandas Series representing the daily position (1, -1, or 0).
    """
    df = data.copy()
    
    # 1. Calculate the Rolling Averages
    df['SMA_Short'] = df['Close'].rolling(window=short_window).mean()
    df['SMA_Long'] = df['Close'].rolling(window=long_window).mean()
    
    # 2. Generate Signals
    # np.where is highly optimized in NumPy. 
    # If Short > Long, go Long (1). Otherwise, go Short (-1).
    df['Signal'] = np.where(df['SMA_Short'] > df['SMA_Long'], 1, -1)
    
    # 3. Clean up NaNs from the initial rolling window period
    df['Position'] = df['Signal'].copy()
    df.loc[df['SMA_Long'].isna(), 'Position'] = 0
    
    return df['Position']