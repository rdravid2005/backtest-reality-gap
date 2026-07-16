# Research Charter — Backtest-to-Reality Gap

## Project Title

The Backtest-to-Reality Gap

## Research Question

How sensitive are short-horizon trading strategies to transaction costs, slippage, fill assumptions, and execution delay?

## Plain-English Version

Can a strategy look decent in a clean backtest but become unattractive or unusable once realistic trading frictions are added?

## Motivation

This project builds on the Opening Range Breakout Robustness Study.

The QQQ 5-minute ORB strategy had positive returns, but it also had high turnover, many orders, meaningful fees, and weak Sharpe. That makes it a useful case study for testing how execution assumptions affect short-horizon strategies.

This also connects to a broader trading lesson: a strategy can have a statistically interesting signal but still fail in live trading because of costs, slippage, delays, spread, or poor fill quality.

## Initial Hypothesis

Short-horizon strategies are highly sensitive to execution assumptions.

Small changes in transaction costs, slippage, or execution delay can significantly reduce performance. Some strategies that appear positive in a clean backtest may become economically unattractive under more realistic assumptions.

## Base Strategy

The base strategy will be the best simple ORB version from Project 2:

- Asset: QQQ
- Opening range: 5 minutes
- Direction: Long-only
- Entry: Break above opening range high
- Exit: End of day
- Stop-loss: None
- Profit target: None
- Data resolution: Minute
- Backtest period: 2020-01-01 to 2026-07-01

## Baseline Result From Project 2

The base QQQ 5-minute ORB result was:

- CAGR: 7.342%
- Sharpe: 0.203
- Sortino: 0.204
- Max drawdown: 16.100%
- Net profit: 56.116%
- Total orders: 2,628
- Fees: $4,381.39
- Turnover: 114.03%

This result was positive, but weak. The purpose of Project 3 is to test how much worse it becomes as execution assumptions become more realistic.

## Variables To Test

This project may test:

- Higher transaction costs
- Fixed slippage per trade
- Percentage slippage
- Delayed entry
- Delayed exit
- Worse fill assumptions
- Reduced position sizing
- Higher turnover impact
- Trade frequency sensitivity

## What Would Support the Hypothesis?

The hypothesis would be supported if small increases in costs, slippage, or execution delay meaningfully reduce CAGR, Sharpe, Sortino, net profit, or drawdown profile.

It would also be supported if the QQQ 5-minute ORB strategy becomes unattractive or negative under modest execution frictions.

## What Would Weaken the Hypothesis?

The hypothesis would be weakened if the strategy remains stable and positive under reasonable cost, slippage, and delay assumptions.

If performance does not materially deteriorate when execution assumptions become harsher, then the strategy may be more robust than expected.

## Key Risks

- Overstating precision of slippage assumptions
- Using unrealistic cost models
- Confusing modeled slippage with real bid-ask spread
- Assuming QuantConnect fills perfectly reflect live execution
- Ignoring liquidity differences across assets
- Testing too many friction assumptions without structure
- Drawing conclusions beyond what the data supports

## Research Standard

The goal is not to make the strategy look better.

The goal is to understand how fragile or resilient the strategy is when the backtest becomes more realistic.

A negative result is useful if it shows that a strategy is not economically tradable after costs.

## First Exit Test

Before coding, I should be able to explain:

1. Why a clean backtest can overstate live performance.
2. Why short-horizon strategies are more execution-sensitive than long-horizon strategies.
3. How fees, slippage, and delayed fills can reduce edge.
4. Why a strategy can have a real signal but still be unattractive to trade.