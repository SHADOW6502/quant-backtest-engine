import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from core.metrics import calculate_metrics

class VectorizedBacktester:
    def __init__(self, data, initial_capital=10000.0, tc=0.001):
        # Expects a DataFrame with at least 'Close' prices
        self.data = data.copy()
        self.initial_capital = initial_capital
        self.tc = tc # Transaction costs (e.g., 0.1%)
        
    def run_strategy(self, strategy_func, *args, **kwargs):
        """Applies the strategy function to generate a 'Position' column (1 for Long, -1 for Short, 0 for Flat)."""
        self.data['Position'] = strategy_func(self.data, *args, **kwargs)
        
        # Shift positions by 1 to avoid look-ahead bias (we trade on tomorrow's open based on today's close)
        self.data['Position'] = self.data['Position'].shift(1).fillna(0)
        
        self._calculate_returns()
        return calculate_metrics(self.data)

    def _calculate_returns(self):
        # Calculate daily market returns
        self.data['Market_Returns'] = np.log(self.data['Close'] / self.data['Close'].shift(1))
        
        # Calculate strategy returns (Position * Market Return)
        self.data['Strategy_Returns'] = self.data['Position'] * self.data['Market_Returns']
        
        # Deduct transaction costs when positions change
        trade_executions = self.data['Position'].diff().abs() > 0
        self.data.loc[trade_executions, 'Strategy_Returns'] -= self.tc
        
        # Calculate cumulative equity curves
        self.data['Cumulative_Market'] = self.initial_capital * np.exp(self.data['Market_Returns'].cumsum())
        self.data['Cumulative_Strategy'] = self.initial_capital * np.exp(self.data['Strategy_Returns'].cumsum())

    def plot_results(self):
        plt.figure(figsize=(14, 7))
        plt.plot(self.data.index, self.data['Cumulative_Strategy'], label='Strategy Equity')
        plt.plot(self.data.index, self.data['Cumulative_Market'], label='Buy & Hold', alpha=0.7)
        plt.title('Backtest Equity Curve')
        plt.ylabel('Portfolio Value')
        plt.legend()
        plt.grid(True)
        plt.show()