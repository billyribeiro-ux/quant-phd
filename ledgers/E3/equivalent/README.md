# E3 equivalent mutants

Each file here differs from `course/modules/E/E3/grader/reference.py` only in `_half_up`, the rounding of a float
value to a whole cent, and only in how it breaks an exact tie (a float that is exactly x.5 cents).

| File | Change to `_half_up` | Tie rule |
|---|---|---|
| `f05_half_cent_goes_toward_minus_infinity.py` | `math.ceil(y - 0.5)` | toward minus infinity |
| `m06_half_cent_rounded_to_even.py` | `round(y)` | to even |
| `r13n01_half_cent_rounded_half_to_even.py` | `round(y)` | to even |
| `w05_half_cent_away_from_zero.py` | `floor(y + 0.5)` if `y >= 0`, else `ceil(y - 0.5)` | away from zero |

## Why each one is equivalent to the specification

1. **Every output is a nearest whole cent.** For each `y`, the mutant returns an integer `n` with `|y - n| <= 1/2`.
   The reference `floor(y + 1/2)` does the same. The two differ only when `y` is exactly `k + 1/2`, where both
   neighbours are at distance exactly 1/2.
2. **The specification accepts either neighbour at an exact half cent in the prospect model.** The Whole cents
   paragraph of `course/modules/E/E3/project.html` says that under the prospect model the value is a float, so an exact
   half cent may come out either side, and that the suite accepts either neighbouring cent. The prospect check in the
   Grading paragraph also accepts any whole cent within half a cent of the exact sure amount.
3. **The CRRA exact path is not affected.** At `gamma = 0` under the CRRA model the engine rounds an exact `Fraction`
   with `floor(expected + 1/2)`, not `_half_up`, so none of these mutants changes that output. The CRRA model at
   `gamma > 0` is compared with the oracle to half a cent, and `instance.py` rejects any draw within `1e-6` of a half
   cent, so no suite input reaches a tie there.
4. **Evidence.** Each file passes the whole suite on seeds 0 to 9 (`tools/mutate_graders.py` reports SURVIVED only for
   a file that passes every seed in the window; round 13 rerun in `ledgers/E3/scripts/fixer-d-r13/out/`). The four were
   killed only by `test_half_cent_goes_up_on_exact_halves` before the prospect exact-half check was relaxed to accept
   either neighbour (round 13, `test_half_cent_rounding_on_exact_halves`).

These files are kept as evidence of the decision. The architect should confirm the decision in item 2 of the Whole
cents paragraph. If the page is changed to require a specific tie rule for the prospect model, these four become
student-error mutants again and must be killed.

# Round 13: three survivors of seeds 0 to 9 that differ only on inputs no suite participant reaches

These three files are not equivalent on every input. Each differs from the reference only on an input that the page
states no behaviour for and that none of the suite's participants reaches, so no seed-independent fixture can kill them
from a stated behaviour. The residual difference is named for each file.

Evidence base (current reference, round 13): the reference's estimate on the 800 participants of generator seeds 0 to
399, each own participant (seed s) and second participant (seed s + 7919), of which 792 return an estimate and 8 raise
(the eight seeds the page names: own 108, 157, 165, 269; second 89, 110, 235, 373); and the fixed fixtures
`FIXED_26_ANSWERS` (gamma_hat 0.6534), the twelve-response B-side set (gamma_hat 0.1174), `LOW_KAPPA` (seed 30, gamma_hat
0.5190), `LARGE_LAMBDA` (seed 49, gamma_hat 0.7063) and `STALL` (seed 108, raises). Scan scripts:
`ledgers/E3/scripts/fixer-d-r13/`.

| File | Change | Differs from the reference only when | Evidence on the suite's inputs |
|---|---|---|---|
| `r11_03_gamma_hat_clamped_below_one_minus_1e3.py` | `gamma_hat` is clamped to 0.999 | the reference's `gamma_hat` exceeds 0.999 | largest `gamma_hat` over the 792 estimates is 0.98639 (own seed 352); no fixture exceeds 0.71 |
| `r12d_03_reported_gamma_floored_at_one_thousandth.py` | `gamma_hat` is floored at 0.001 | the reference's `gamma_hat` is below 0.001 | smallest `gamma_hat` over the 792 estimates is 0.02489 (own seed 373); no fixture is below 0.11 (the lowest is 0.1174) |
| `e12_03_search_returns_silently_when_it_stalls.py` | the stalled point is returned instead of raising when the step becomes negligible before the score does | the reference executes its raise `the step became negligible before the score did` | no run on the 800 participants or the fixtures raises that message. The eight raising runs raise `no damped Newton step raises the likelihood` (own 108, 157, 165, 269; second 373) or `the likelihood maximisation did not converge` (second 89, 110, 235). A run that returns never executes the raise |

Why none of these is a seed-independent kill: the page states the domain `0 < gamma < 1` and the score and local-maximum
checks, but it states no clamp or floor on `gamma_hat`, and it names no outcome for a raise. A fixture that reaches
`gamma_hat` above 0.999 or below 0.001, or that enters the negligible-step raise and returns, would need a participant
the reference fits; none exists among the drawn participants. The residual gap is stated here rather than hidden:
seeds 400 and above were not scanned, and the browser can draw any 31-bit seed.

The architect should decide whether the page should state an upper bound `gamma_hat <= 0.999`, a lower bound, or a
rule for a step that becomes negligible before the score does. If it does, a fixture must be written and these files
become student-error mutants again.
