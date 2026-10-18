# Round-7 proposals for central files: L03–L04 (branch `worktree-g6-g4`)

These are the central-file changes that the round-7 verifier rows need. `cards.json` is central, so the branch
does not edit it. Apply the changes below to `course/modules/S/S7/cards.json`. They change no other central
file: the registry, the curriculum and the notation stay as they are. The strings are shown as they appear in
the JSON file, with backslashes escaped.

## 1. S7-c128 (rows L03-math-canon-null and card-S7-c128)

In `back`, replace

```
Autocorrelated or overlapping returns widen the null of Sharpe-ratio z-statistics
```

with

```
Positively autocorrelated or overlapping returns widen the null of Sharpe-ratio z-statistics
```

This matches the corrected L03 §9 bullet, which now reads "positively autocorrelated or overlapping returns
(Lesson 4)". With negative autocorrelation the long-run variance is below gamma(0), so the null narrows (L04
Remark 3.4).

## 2. S7-c134 (rows L04-math-remark1.6 and card-S7-c134)

In `back`, replace

```
equal mean squared errors \\(s^2\\) and error correlation \\(\\rho \\lt 1\\)
```

with

```
unbiased forecasts with equal mean squared errors \\(s^2\\) and error correlation \\(\\rho \\lt 1\\)
```

The formula E[e0(e0 - e1)] = s^2(1 - rho), and with it s^2(1 + rho)/2, needs E[e0 e1] = rho s^2, which holds
when both errors have mean zero. L04 Remark 1.6 now reads "If both forecasts are unbiased, with mean squared
error s^2 and error correlation rho < 1".

## 3. Split S7-c124 and add a Definition 7.1 card (row cards-L03L04-coverage-L03)

**Why:** S7-c124 tested Proposition 7.6 and Definition 7.7 in one card. Definition 7.1, the two-group model,
had no card of its own.

**What to do:**

1. Replace S7-c124 with the Proposition 7.6 card below.
2. Add S7-cNEW-1 for Definition 7.1.
3. Add S7-cNEW-2 for Definition 7.7.

Give the new cards the next free ids. They can go anywhere in the file; card order does not affect the deck.

Current S7-c124:

```json
{
 "id": "S7-c124",
 "lesson": "L03",
 "front": "State the posterior of a true Sharpe ratio \\(\\theta \\sim \\Normal(\\mu, \\tau^2)\\) given an estimate \\(X \\mid \\theta \\sim \\Normal(\\theta, \\sigma^2)\\), and how empirical Bayes shrinkage fits it.",
 "back": "\\(\\theta \\mid X \\sim \\Normal(\\mu + B(X - \\mu), B\\sigma^2)\\) with \\(B = \\tau^2/(\\tau^2 + \\sigma^2)\\), and marginally \\(X \\sim \\Normal(\\mu, \\tau^2 + \\sigma^2)\\) (Proposition 7.6). Empirical Bayes shrinkage fits \\(\\hat\\mu = \\bar X\\) and \\(\\hat\\tau^2 = \\max\\{0, s_X^2 - \\sigma^2\\}\\) by moments (Definition 7.7).",
 "grade": "T"
}
```

Replacement S7-c124:

```json
{
 "id": "S7-c124",
 "lesson": "L03",
 "front": "State the posterior of a true Sharpe ratio \\(\\theta \\sim \\Normal(\\mu, \\tau^2)\\) given an estimate \\(X \\mid \\theta \\sim \\Normal(\\theta, \\sigma^2)\\).",
 "back": "\\(\\theta \\mid X \\sim \\Normal(\\mu + B(X - \\mu), B\\sigma^2)\\) with \\(B = \\tau^2/(\\tau^2 + \\sigma^2)\\), and marginally \\(X \\sim \\Normal(\\mu, \\tau^2 + \\sigma^2)\\) (Proposition 7.6).",
 "grade": "T"
}
```

New cards:

```json
[
 {
  "id": "S7-cNEW-1",
  "lesson": "L03",
  "front": "State the two-group model.",
  "back": "The pairs \\((H_n, Z_n)\\), \\(n = 1, \\dots, N\\), are independent and identically distributed. Each hypothesis is null with probability \\(\\pi_0 \\gt 0\\) and non-null with probability \\(\\pi_1 = 1 - \\pi_0\\); given \\(H_n = 0\\) the statistic \\(Z_n\\) has density \\(f_0\\), and given \\(H_n = 1\\) density \\(f_1\\). The statistics therefore have the mixture density \\(f = \\pi_0 f_0 + \\pi_1 f_1\\) (Definition 7.1).",
  "grade": "T"
 },
 {
  "id": "S7-cNEW-2",
  "lesson": "L03",
  "front": "How does empirical Bayes shrinkage of \\(N\\) Sharpe ratios fit its normal population, and what does it report?",
  "back": "By moments: \\(\\hat\\mu = \\bar X\\) and \\(\\hat\\tau^2 = \\max\\{0, s_X^2 - \\sigma^2\\}\\), with \\(s_X^2\\) the cross-sectional sample variance, give \\(\\hat B = \\hat\\tau^2/(\\hat\\tau^2 + \\sigma^2)\\). It reports \\(\\tilde\\theta_n = \\hat\\mu + \\hat B(X_n - \\hat\\mu)\\), which moves each estimate toward the mean by the share \\(1 - \\hat B\\) of its distance, equal to \\(\\sigma^2/s_X^2\\) when \\(\\hat\\tau^2 \\gt 0\\) (Definition 7.7).",
  "grade": "T"
 }
]
```

Each back can be checked against L03 Definition 7.1, Proposition 7.6 and Definition 7.7 as they stand on the
branch.
