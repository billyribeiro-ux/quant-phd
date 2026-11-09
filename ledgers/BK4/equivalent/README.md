# BK4 equivalent mutants

Each file here differs from `course/modules/BK/BK4/grader/reference.py` in one place, and the difference is not a
student error that the suite could detect. They are kept as evidence of that decision, and they are not counted among
the student-error mutants in `ledgers/BK4/mutants/`.

| File | Change to the reference | Differs from the reference |
|---|---|---|
| `r15c_cover_float_floor.py` | `cover_bps` returns `math.floor(10000 * covered / len(losses_cents))`, a float quotient floored | in the arithmetic of the floored quotient only; the integers returned are the same |

## r15c: the float quotient in `cover_bps` floors to the same integer

**Claim.** For every integer `c` and `S` with `0 <= c <= S` and `1 <= S <= 9 * 10^11`,
`math.floor(10000 * c / S) == 10000 * c // S`. Here `c` is the covered count and `S` the number of scenarios, so the
two functions return the same integer for every input that `cover_bps` accepts on a list that fits in memory.

**Proof.** Write `N = 10000 * c` and `n = N // S`, so `q = N / S` is the exact rational quotient and `n <= q < n + 1`.
Note `0 <= q <= 10000`, because `c <= S`. The Python expression `10000 * c / S` is the integer quotient rounded to the
nearest double `x`, and `|x - q| <= 2^-53 * q <= 10000 * 2^-53`.

1. *`S` divides `N`.* Then `q = n` is an integer, which a double represents exactly, so `x = n` and
   `math.floor(x) = n`.
2. *`S` does not divide `N`.* Then `q = n + r / S` with `1 <= r <= S - 1`, so the distance from `q` up to the next
   integer is `(n + 1) - q = (S - r) / S >= 1 / S`. Rounding is monotone and `n` is representable, so `n <= x`. For the
   upper side, `x - q <= 10000 * 2^-53 < 1 / S`, because `S <= 9 * 10^11 < 2^53 / 10000`. So `x < q + 1 / S <= n + 1`,
   and `math.floor(x) = n`.

In both cases the float floor equals `n = 10000 * c // S`. The bound `9 * 10^11` is far above the length of any list a
learner can hold in memory: a list of that many Python ints needs at least 7.2 TB for its pointers alone.

**Why the suite cannot detect it.** The grader checks the cover values (`course/modules/BK/BK4/project.html`, the
Grading mode paragraph: "It checks the cent results and the cover values, not the method that computes them"). The
page's sentence "no float appears" is a constraint, and the grader does not check it. So a difference in method that
returns the same integer is not a behaviour the suite can test, and the page states no other output for `cover_bps`.

**Evidence.** The check is `ledgers/BK4/scripts/BK4-c-r15/equivalent_check_r15c.py`. Re-run with `.venv/bin/python` for this
README, it printed:

```
exhaustive S<=2000: 2003000 pairs, disagreements 0
random S<=10^7: 200000 pairs, disagreements 0
```

The exhaustive part covers every `0 <= c <= S <= 2000`. The random part covers 200,000 pairs with `S` up to `10^7`.
The argument above covers the rest of the range up to `9 * 10^11`, which the random check does not sample.

**If the page changes.** If the page states that `cover_bps` must use integer arithmetic and the grader must check
it, this file becomes a student-error mutant again, and the grader must kill it with a test that the page states.
