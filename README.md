# QC Long Strategy: Mean Reversion and Momentum on SPY

This QuantConnect project implements a daily strategy on SPY using a combination of long-only mean reversion and long-only momentum signals based on z-scores of moving averages.


Strategy Summary

- **Asset**: SPY (S&P 500 ETF)
- **Data**: Daily bars
- **Core Signals**:
- **Z-score** of price deviation from moving average (mean reversion)
- **Z-score** of moving average slope (momentum)
- **Positioning**: Long-only trades, no shorts


Performance

| Year | Return | Sharpe Ratio |
|------|--------|--------------|
| 2023 | ~14%   | ~0.7         |
| 2024 | ~30%   | ~2.0         |

- Z-score-based momentum outperformed RSI-based signal.
- Long-only strategies performed better than long-short ones in this period.


Key Insights

- **Trend Adaptation**: SPY had a strong bullish trend in 2023–24, making short positions less effective.
- **Momentum Complementarity**: Adding a momentum filter to the mean reversion setup significantly improved returns and Sharpe.
- **Z-score Superiority**: Z-score proved to be a more stable signal than RSI in this use case. Realised in periods of low volatality at highs and lows z score reacts faster as compared to RSI.


Limitations & Potential Biases

- **Bull Market Bias**: The strategy performs well in upward-trending markets; may underperform in flat or bearish regimes.
- **Overfitting Risk**: Insights are based on only two years of data (2023–24).
- **Lookahead Bias Check Needed**: Ensure that moving average and z-score calculations don't inadvertently use future data.


Future Improvements

- Add Bearish Regime Testing : Backtest during volatile/bearish periods (e.g., 2020 COVID crash).
- Feature Expansion : Include macro indicators, volatility filters, or volume analysis.
- Parameter Optimization : Automate the tuning of MA window and z-score thresholds using grid search or Bayesian optimization.
- Regime Detection : Build logic to switch between mean reversion and momentum based on market regime classification.
- Live Paper Trading : Test strategy on paper trading for robustness under live conditions.


Author Note

This is a work in progress aimed at building a robust long-only strategy tailored to large-cap indices in bullish or neutral market conditions.
