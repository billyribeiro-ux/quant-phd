# PROPOSALS-L05-lab6-r7: central edit after the round-7 fix of L05 Lab 6

The round-7 verifier failed row `L05-lab-6`: the twin built each moving average
from a floating-point running sum, so an exact tie between a rate and its
average, where the stated rule holds no position, was broken by rounding
noise.

## What changed on the branch (committed)

- `tests/labs/S7/lab-S7-L05-6.py` compares each rate with its average exactly,
  in int64 integers scaled from the published decimals (each column times 10 to
  its largest number of decimal places), so a tie is exactly zero and the rule
  is flat. No tolerance is involved. The lab now prints the count of tied
  rule-days, 14.
- Exact rational arithmetic (Python `Fraction` on the published strings, a
  separate check) finds the same 14 ties as the verifier: AUD MA10 5, MA20 1,
  MA50 1; EUR MA10 1, MA20 2; GBP MA10 4. The old float construction went long
  on 11 and short on 3 of them. The smallest genuine relative gap between a
  rate and its average is 5.5e-7.
- `L05.html`: the hypothesis states the flat-on-tie rule and the exact
  comparison; §8's position set is \(\{-1, 0, 1\}\); the output is re-embedded
  (`embed_labs.py --refresh lab-S7-L05-6`); the interpretation's Reality Check
  p-value is 0.853, and one sentence reports the 14 ties.
- Six t-statistics and three bootstrap figures moved: AUD-MA10 −0.262 → −0.232,
  AUD-MA20 0.026 → 0.021, AUD-MA50 0.149 → 0.134, EUR-MA10 0.126 → 0.119,
  EUR-MA20 −0.819 → −0.811, GBP-MA10 −0.686 → −0.706; Reality Check p 0.852 →
  0.853; at mean block 5 the Reality Check p is 0.876 → 0.874; at mean block 20
  StepM's first step is 2.772 → 2.771. Every other printed figure, and every
  other number on the page, is unchanged. No conclusion changes.
- L08 Lab 4 and the project's Lab 3 take the sign of a log-price difference,
  not of a computed average. Checked exactly over all 16,340 signal pairs from
  1999-01: 16 exact ties, each giving a zero signal in floating point too, and
  no sign mismatch. They need no change.

## Central edit: card S7-c165 in `course/modules/S/S7/cards.json`

Exact replacement (the old string occurs once):

| Old | New |
|---|---|
| `The Reality Check p-value was 0.852, and every 95% sup-t interval` | `The Reality Check p-value was 0.853, and every 95% sup-t interval` |

No other card quotes a number that moved (the other figures in S7-c165, 1.105,
1.645, 2.837 and 10.08, are unchanged), and the project's memo exemplars use
only L08 Lab 4's grid. `PROPOSALS-G1-G3.md` still shows 0.852 in its proposed
card S7-cNEW-2, which became S7-c165; this file supersedes it.
