import numpy as np

def calculate_metrics(data, risk_free_rate=0.0):
    returns = data['Strategy_Returns'].dropna()
    
    # Total Trading Days
    days = len(returns)
    
    # 1. Annualized Return (Assuming 365 days for Crypto/24-7 assets, change to 252 for equities)
    cumulative_return = np.exp(returns.sum()) - 1
    annualized_return = (1 + cumulative_return)**(365 / days) - 1
    
    # 2. Sharpe Ratio
    excess_returns = returns - (risk_free_rate / 365)
    sharpe_ratio = np.sqrt(365) * excess_returns.mean() / excess_returns.std()
    
    # 3. Maximum Drawdown
    cumulative_equity = np.exp(returns.cumsum())
    peak = cumulative_equity.cummax()
    drawdown = (cumulative_equity - peak) / peak
    max_drawdown = drawdown.min()
    
    return {
        "Annualized Return": f"{annualized_return:.2%}",
        "Sharpe Ratio": f"{sharpe_ratio:.2f}",
        "Max Drawdown": f"{max_drawdown:.2%}"
    }