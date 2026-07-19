# Backtest-to-Reality Gap

## Overview

This project studies how short-horizon trading strategies can look promising in a clean backtest but weaken once more realistic execution assumptions are introduced.

The project uses the QQQ 5-minute Opening Range Breakout strategy from my prior ORB Robustness Study as the base case. That strategy was positive in a clean backtest, but had weak risk-adjusted performance, high turnover, many orders, and meaningful fees.

The goal is not to make the strategy look better. The goal is to test how fragile the backtest is once execution delay and slippage are introduced.

## Research Question

How sensitive are short-horizon trading strategies to transaction costs, slippage, fill assumptions, and execution delay?

## Plain-English Version

Can a strategy look decent in a clean backtest but become unattractive or unusable once realistic trading frictions are added?

## Initial Hypothesis

Short-horizon strategies are highly sensitive to execution assumptions.

Small changes in slippage, transaction costs, or execution timing can meaningfully reduce performance. A strategy with weak edge and high turnover may become unattractive even if the clean backtest looks positive.

## Base Strategy

The base strategy is the best simple ORB version from the prior ORB Robustness Study:

- Asset: QQQ
- Opening range: 5 minutes
- Direction: Long-only
- Entry: Break above the 5-minute opening range high
- Exit: End of day
- Stop-loss: None
- Profit target: None
- Data resolution: Minute
- Test period: 2020-01-01 to 2026-07-01

## Tools Used

- QuantConnect
- Python
- Minute-level ETF data
- GitHub
- CSV experiment logging

## Why This Strategy Was Useful for the Study

The QQQ 5-minute ORB was useful because it had:

- Positive clean-backtest returns
- Weak Sharpe ratio
- High turnover
- More than 2,600 orders
- Meaningful fees
- Intraday entry and exit timing

That makes it a good case study for testing the gap between clean backtest results and more realistic trading assumptions.

## Experiment Summary

| Experiment | Execution Assumption | CAGR | Sharpe | Sortino | Max Drawdown | Net Profit | Notes |
|---|---|---:|---:|---:|---:|---:|---|
| EXP-001 | Clean baseline | 7.738% | 0.224 | 0.225 | 16.100% | 59.896% | Positive but weak baseline |
| EXP-002 | 1-minute entry delay | 7.130% | 0.192 | 0.192 | 16.500% | 54.296% | Delay weakened performance |
| EXP-003 | 5-minute entry delay | 8.936% | 0.285 | 0.268 | 17.600% | 71.429% | Delay improved returns but increased drawdown |
| EXP-004 | 10-minute entry delay | 11.154% | 0.410 | 0.419 | 12.000% | 94.629% | Strongest delayed-entry result |
| EXP-005 | 10-minute delay, require still above OR high | 4.489% | 0.045 | 0.040 | 21.900% | 31.857% | Confirmation requirement weakened performance sharply |
| EXP-006 | 5 bps slippage per order | -12.681% | -0.882 | -0.887 | 60.800% | -57.428% | Harsh slippage stress test destroyed strategy |
| EXP-007 | 1 bps slippage per order | 3.338% | -0.009 | -0.009 | 21.400% | 23.00s3% | Small slippage erased risk-adjusted performance |
| EXP-008 | 2 bps slippage per order | -0.886% | -0.234 | -0.235 | 26.900% | -5.457% | Modest slippage pushed strategy negative |
| EXP-009 | 10-minute delay + 1 bps slippage | 6.610% | 0.165 | 0.168 | 14.800% | 49.720% | Improved logic survived but weakened sharply |

Full experiment details are available in:


results/experiment_log.csv