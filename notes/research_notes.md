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
## Five-Minute Entry Delay

The five-minute entry delay produced an unexpected result.

Instead of weakening the strategy, the delayed-entry version improved CAGR, Sharpe, Sortino, net profit, and end equity versus both the clean baseline and the one-minute delay test.

CAGR increased from 7.738% in the baseline to 8.936%. Sharpe increased from 0.224 to 0.285. Net profit increased from 59.896% to 71.429%.

However, max drawdown also increased from 16.100% to 17.600%.

This suggests that the five-minute delay may not be functioning only as an execution-friction test. It may also be acting as a confirmation filter by avoiding some breakouts that fail immediately after crossing the opening range high.

This is an important research distinction: execution delay can sometimes change the strategy logic itself, not just worsen fills.
## Ten-Minute Entry Delay

The ten-minute entry delay produced an even stronger unexpected result.

Instead of weakening performance, the strategy improved meaningfully versus the clean baseline, the one-minute delay, and the five-minute delay.

CAGR increased to 11.154%, Sharpe increased to 0.410, Sortino increased to 0.419, net profit increased to 94.629%, and max drawdown fell to 12.000%.

This is important because the experiment was intended to test execution delay, but the result suggests the delay is changing the strategy logic.

The current delayed-entry code enters ten minutes after the first breakout signal without checking whether price is still above the opening range high at the delayed entry time.

That means this is not a pure execution-friction test. It may be acting as a delayed confirmation rule, a pullback entry rule, or some combination of both.

## Updated Delay Finding

The one-minute delay weakened the strategy, but the five-minute and ten-minute delays improved performance.

This suggests that delayed entry is not automatically harmful. In this implementation, longer delays may filter out noisy immediate breakouts or create better entry timing.

The next test should require price to still be above the opening range high at the delayed entry time. That will help separate true breakout confirmation from accidental pullback behavior.
## Ten-Minute Delay With Breakout Still Valid

The next test kept the ten-minute entry delay but required price to still be above the opening range high at the delayed entry time.

This performed much worse than the unrestricted ten-minute delay.

CAGR fell to 4.489%, Sharpe fell to 0.045, Sortino fell to 0.040, net profit fell to 31.857%, and max drawdown rose to 21.900%.

This suggests that the strong EXP-004 result was probably not caused by clean breakout confirmation.

Instead, the unrestricted ten-minute delay may have changed the strategy into something closer to a post-breakout pullback or delayed-entry behavior. In other words, the code was not simply modeling worse execution; it was changing the trading rule.

## Updated Interpretation

The delay experiments show that execution assumptions and strategy logic can overlap.

A one-minute delay weakened the strategy, which supports execution sensitivity.

A five-minute and ten-minute delay improved performance, but the follow-up test showed that the improvement was not simply because price stayed strongly above the breakout level.

This is an important backtest-to-reality lesson: small implementation details can create very different strategies, and a researcher must understand exactly what the code is doing before interpreting the result.
## Five Basis Point Slippage Stress Test

The first explicit slippage test added 5 basis points of slippage per order.

This had a severe impact on the strategy.

The clean baseline had a CAGR of 7.738%, Sharpe of 0.224, net profit of 59.896%, and max drawdown of 16.100%.

With 5 bps slippage per order, CAGR fell to -12.681%, Sharpe fell to -0.882, net profit fell to -57.428%, and max drawdown rose to 60.800%.

This result shows how dangerous high turnover can be when the underlying edge is weak. A small-looking per-order friction becomes large when applied across 2,636 orders.

However, 5 bps per order may be a harsh assumption for QQQ, so this should be treated as a stress test rather than the only realistic slippage case.

The next step is to test smaller slippage assumptions such as 1 bps and 2 bps.
## One Basis Point Slippage

The next slippage test added 1 basis point of slippage per order.

This was much less severe than the 5 bps stress test, but it still significantly weakened the strategy.

CAGR fell from 7.738% in the clean baseline to 3.338%. Net profit fell from 59.896% to 23.003%. Sharpe fell from 0.224 to -0.009, and Sortino fell from 0.225 to -0.009. Max drawdown increased from 16.100% to 21.400%.

This is a major result for the project. Even a small per-order friction meaningfully damaged the QQQ 5-minute ORB because the strategy trades frequently and has a weak baseline edge.

The strategy remained positive on net profit, but its risk-adjusted performance effectively disappeared.
## Two Basis Point Slippage

The 2 bps slippage test pushed the strategy into negative territory.

CAGR fell from 7.738% in the clean baseline to -0.886%. Net profit fell from 59.896% to -5.457%. Sharpe fell from 0.224 to -0.234, and max drawdown increased from 16.100% to 26.900%.

This is one of the strongest findings so far.

The clean QQQ 5-minute ORB looked positive before additional slippage, but it could not survive modest execution friction. At 1 bps, risk-adjusted performance disappeared. At 2 bps, the strategy became negative.

This supports the project hypothesis that short-horizon, high-turnover strategies with weak baseline edge can be highly sensitive to small per-order frictions.