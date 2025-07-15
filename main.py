# region imports
from AlgorithmImports import *
from collections import deque
# endregion

class QuantLeague(QCAlgorithm):
    def initialize(self):
        self.set_start_date(2023, 1, 1)
        self.set_end_date(2023, 12, 31)
        self.set_cash(1000000)
        self.symbol = self.add_equity("SPY", Resolution.Daily).Symbol
        self.window =20
        self.moving_average = self.sma(self.symbol, self.window, Resolution.Daily)
        self.rsi = self.RSI(self.symbol, 20, Resolution.Daily)
        self.last_action = None
        self.prices = deque(maxlen=self.window)
        self.entryZ = 2
        self.exitZ = 0.5
        self.enterStrat = 0
        self.last_trade_time = None
        self.volumes = deque(maxlen=5)

    def on_data(self, data):
        # Ensure we have enough data to calculate the moving average
        price = self.Securities[self.symbol].Price
        volume = self.Securities[self.symbol].Volume
        self.prices.append(price)
        self.volumes.append(volume)
        self.Plot("Price Chart", "Price", price)
        self.Plot("volume chart", "volume", volume)
        if not self.moving_average.is_ready:#or not self.rsi.is_ready:
           return
        #self.Plot("Price Chart", "Mean", self.moving_average.current.value)

        std = (sum([(x - self.moving_average.current.value) ** 2 for x in self.prices]) / len(self.prices)) ** 0.5

        if std == 0:
            return
        avgVolume = sum(self.volumes)/len(self.volumes)
        self.Plot("volume chart", "avgVolume", avgVolume)
        volumeIndicator = volume>(1.5*avgVolume)
        self.Plot("volume chart", "volumeIndicator", int(volumeIndicator))
        z_score = (price - self.moving_average.current.value) / std
        self.Plot("z Chart", "z_score", z_score)
        if self.rsi.is_ready:
            self.Plot("RSI", "RSI", self.rsi.current.value)
        if self.last_trade_time:
            days_since_trade = (self.Time - self.last_trade_time).days

        invested = self.Portfolio[self.symbol].Invested
        
        if invested and (((self.entry_price - price)/self.entry_price) > 0.04): #stoploss
            self.liquidate(self.symbol)
            self.Debug(f"exiting on stoploss: {z_score:.2f}")

        if (z_score> 1 and z_score<2.2) and not invested:
        #if (self.rsi.current.value> 60 and self.rsi.current.value<80) and not self.enterStrat: #and not invested: ## Long Momentum
            self.set_holdings(self.symbol, 1)
            self.Debug(f"entering long momentum Z-score: {z_score:.2f}")
            self.enterStrat = 1
        if self.enterStrat and invested and z_score<0.5:
        #if self.enterStrat and invested and (self.rsi.current.value<50 or self.rsi.current.value>85):
            self.liquidate(self.symbol)
            self.Debug(f"exiting long momentum Z-score: {z_score:.2f}")
        
        if z_score < -self.entryZ and z_score>-3 and not invested:
            self.set_holdings(self.symbol, 1)
            self.Debug(f"entering long mean reversion Z-score: {z_score:.2f}")  

        if invested and abs(z_score) < self.exitZ:
            self.liquidate(self.symbol)
            self.Debug(f"exiting mean reversion Z-score: {z_score:.2f}")

        if invested and abs(z_score) > 3: # exit long mean reversion as trend does not revert
            self.liquidate(self.symbol)
            self.Debug(f"exiting because mean did not revert Z-score: {z_score:.2f}")
            
    def OnOrderEvent(self, order_event):
        if order_event.Status != OrderStatus.Filled:
            return

        # Only update on entry trades (not liquidations, if needed)
        if order_event.Direction in [OrderDirection.Buy, OrderDirection.Sell]:
            self.last_trade_time = self.Time
        if order_event.Direction in [OrderDirection.Buy]:
            self.entry_price = self.Securities[self.symbol].Price
        if order_event.Direction in [OrderDirection.Sell]:
            self.enterStrat = 0

    def OnEndOfAlgorithm(self):
        closed_trades = self.TradeBuilder.ClosedTrades

        if not closed_trades:
            self.Debug("No trades executed.")
            return

        #worst_trade = min(closed_trades, key=lambda trade: trade.ProfitLoss)
        losers = sorted(closed_trades, key=lambda x: x.ProfitLoss)[:3]
        for i, worst_trade in enumerate(losers):
            #self.Debug(f"#{i+1} Loss: {trade.Symbol} | PnL: {trade.ProfitLoss:.2f} | Entry: {trade.EntryTime}")
            self.Debug(f"Worst Trade: {worst_trade.Symbol.Value}")
            self.Debug(f"Entry Time: {worst_trade.EntryTime}")
            self.Debug(f"Exit Time: {worst_trade.ExitTime}")
            self.Debug(f"PnL: {worst_trade.ProfitLoss:.2f}")
            self.Debug(f"Entry Price: {worst_trade.EntryPrice}")
            self.Debug(f"Exit Price: {worst_trade.ExitPrice}")
            #self.Debug(f"Quantity: {worst_trade.Quantity}")