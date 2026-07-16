# Backtest-to-Reality Gap — Research Notes

## Current Stage

The project has established the clean baseline version of the strategy before adding additional execution frictions.

## Baseline Strategy

The baseline strategy is the same simple ORB structure from Project 2:

- Asset: QQQ
- Opening range: 5 minutes
- Direction: Long-only
- Entry: Break above opening range high
- Exit: End of day
- Stop-loss: None
- Profit target: None
- Data: Minute resolution
- Period: 2020-01-01 to 2026-07-01

## Baseline Result

The clean baseline produced:

- CAGR: 7.738%
- Sharpe: 0.224
- Sortino: 0.225
- Max drawdown: 16.100%
- Net profit: 59.896%
- Total orders: 2,636
- Fees: $4,391.32
- Turnover: 114.18%

## Initial Interpretation

The baseline is positive, but still weak.

The strategy has many trades, high turnover, meaningful fees, and a low Sharpe ratio. This makes it a good candidate for testing the backtest-to-reality gap because even small execution frictions may materially weaken performance.

## Important Note

This baseline is slightly different from the final Project 2 baseline rerun. For Project 3, this exact run will be treated as the reference point. All later friction experiments should be compared against this Project 3 baseline, not against the older Project 2 numbers.
## One-Minute Entry Delay

The first execution-friction test delayed entry by one minute after the breakout signal.

The strategy still remained positive, but performance weakened versus the clean baseline.

CAGR fell from 7.738% to 7.130%. Sharpe fell from 0.224 to 0.192. Sortino fell from 0.225 to 0.192. Net profit fell from 59.896% to 54.296%, and drawdown increased from 16.100% to 16.500%.

This supports the idea that the QQQ 5-minute ORB is execution-sensitive. A one-minute delay did not destroy the strategy, but it clearly weakened it.