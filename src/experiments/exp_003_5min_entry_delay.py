"""
Project 3: Backtest-to-Reality Gap

EXP-002_QQQ_ORB_5M_1MIN_ENTRY_DELAY

This experiment tests execution delay.

Instead of entering immediately when QQQ breaks above the 5-minute opening
range high, the strategy waits one additional minute before entering.

The goal is to test whether a short-horizon ORB signal is sensitive to delayed
execution.
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
        self.entry_delay_minutes = 5

        self.opening_range_high = None
        self.opening_range_low = None
        self.opening_range_complete = False

        self.traded_today = False
        self.current_day = None

        self.pending_entry = False
        self.pending_entry_time = None

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

        if self.pending_entry:
            if current_time >= self.pending_entry_time:
                self.set_holdings(self.symbol, 1)
                self.pending_entry = False
                self.pending_entry_time = None
                self.traded_today = True
            return

        if self.traded_today:
            return

        if self.opening_range_high is None:
            return

        if bar.close > self.opening_range_high:
            self.pending_entry = True
            self.pending_entry_time = current_time + timedelta(minutes=self.entry_delay_minutes)

    def reset_daily_state(self, current_day):
        self.current_day = current_day
        self.opening_range_high = None
        self.opening_range_low = None
        self.opening_range_complete = False
        self.traded_today = False
        self.pending_entry = False
        self.pending_entry_time = None

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