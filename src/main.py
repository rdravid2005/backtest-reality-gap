"""
Project 3: Backtest-to-Reality Gap

EXP-001_QQQ_ORB_5M_BASELINE

This is the clean baseline version before adding extra execution frictions.
It reuses the best simple strategy from Project 2:

- QQQ
- 5-minute opening range
- Long-only breakout
- End-of-day exit
- No stop-loss
- No profit target
- Minute data

Later experiments will add slippage, higher costs, delayed entries, and other
real-world frictions to test how fragile the strategy is.
"""

from AlgorithmImports import *
from datetime import timedelta


class BacktestRealityGap(QCAlgorithm):

    def initialize(self):
        self.set_start_date(2020, 1, 1)
        self.set_end_date(2026, 7, 1)
        self.set_cash(100000)

        self.symbol = self.add_equity("QQQ", Resolution.MINUTE).symbol

        self.opening_range_minutes = 5

        self.opening_range_high = None
        self.opening_range_low = None
        self.opening_range_complete = False
        self.traded_today = False
        self.current_day = None

        self.schedule.on(
            self.date_rules.every_day(self.symbol),
            self.time_rules.before_market_close(self.symbol, 5),
            self.exit_position
        )

    def on_data(self, data: Slice):
        if self.symbol not in data.bars:
            return

        bar = data.bars[self.symbol]

        current_time = self.time
        current_day = current_time.date()

        if self.current_day != current_day:
            self.reset_daily_state(current_day)

        market_open = current_time.replace(hour=9, minute=30, second=0)
        opening_range_end = market_open + timedelta(minutes=self.opening_range_minutes)

        if market_open <= current_time < opening_range_end:
            self.update_opening_range(bar)
            return

        if current_time >= opening_range_end:
            self.opening_range_complete = True

        if not self.opening_range_complete:
            return

        if self.traded_today:
            return

        if self.opening_range_high is None:
            return

        if bar.close > self.opening_range_high:
            self.set_holdings(self.symbol, 1)
            self.traded_today = True

    def reset_daily_state(self, current_day):
        self.current_day = current_day
        self.opening_range_high = None
        self.opening_range_low = None
        self.opening_range_complete = False
        self.traded_today = False

    def update_opening_range(self, bar):
        if self.opening_range_high is None:
            self.opening_range_high = bar.high
            self.opening_range_low = bar.low
            return

        self.opening_range_high = max(self.opening_range_high, bar.high)
        self.opening_range_low = min(self.opening_range_low, bar.low)

    def exit_position(self):
        if self.portfolio[self.symbol].invested:
            self.liquidate(self.symbol)