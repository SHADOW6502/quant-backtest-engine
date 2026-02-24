import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from core.backtester import VectorizedBacktester
from strategies.mean_reversion import bollinger_bands_strategy
from strategies.ma_crossover import ma_crossover_strategy

def main():
    print("Fetching historical market data for Bitcoin...")
    data = yf.download("BTC-USD", period="730d", interval="1h")
    
    if data is None or data.empty:
        print("Error: Dataset is empty or could not be fetched.")
        return
        
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.droplevel(1)
        
    print(f"Successfully loaded {len(data)} rows of market data.\n")

    # --- Engine 1: Mean Reversion ---
    print("Initializing Engine 1 (Bollinger Bands)...")
    engine_bb = VectorizedBacktester(data, initial_capital=10000.0, tc=0.001)
    metrics_bb = engine_bb.run_strategy(bollinger_bands_strategy, window=20, num_std=2)

    # --- Engine 2: Trend Following ---
    print("Initializing Engine 2 (Moving Average Crossover)...")
    engine_ma = VectorizedBacktester(data, initial_capital=10000.0, tc=0.001)
    metrics_ma = engine_ma.run_strategy(ma_crossover_strategy, short_window=20, long_window=50)

    # --- Print Metrics Comparison ---
    print("\n" + "="*50)
    print(f"{'METRIC':<20} | {'BOLLINGER':<12} | {'MA CROSSOVER'}")
    print("="*50)
    for key in metrics_bb.keys():
        print(f"{key:<20} | {metrics_bb[key]:<12} | {metrics_ma[key]}")
    print("="*50)

    # --- Custom Combined Plot ---
    print("\nRendering combined equity curve visualization...")
    plt.figure(figsize=(14, 7))
    
    # Plot Strategy 1
    plt.plot(engine_bb.data.index, engine_bb.data['Cumulative_Strategy'], 
             label='Bollinger Bands Equity', color='blue')
             
    # Plot Strategy 2
    plt.plot(engine_ma.data.index, engine_ma.data['Cumulative_Strategy'], 
             label='MA Crossover Equity', color='green')
             
    # Plot Market Benchmark (using engine_bb's market data, since they are identical)
    plt.plot(engine_bb.data.index, engine_bb.data['Cumulative_Market'], 
             label='Buy & Hold (Market)', color='orange', alpha=0.5)
    
    plt.title('Strategy Comparison: Mean Reversion vs. Trend Following')
    plt.ylabel('Portfolio Value')
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()