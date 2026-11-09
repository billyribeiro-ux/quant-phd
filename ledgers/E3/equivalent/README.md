# E3 equivalent mutants

These files are student errors that the suite cannot separate from the reference on any input where the page states a
behaviour (ruling 9 in `plans/FINAL-ARCHITECT-RULINGS.md`). Each file differs from
`course/modules/E/E3/grader/reference.py` only where the page states nothing. Each section below gives the difference
and the proof.

# Tie-rule mutants (rulings 9 and 27)

Each of the four files differs from `course/modules/E/E3/grader/reference.py` only in `_half_up`, the rounding of a
float value to a whole cent, and only in how it breaks an exact tie (a float that is exactly x.5 cents).

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
2. **The specification accepts either neighbour at an exact half cent in two cases.** (a) Under the prospect model the
   value is a float, so an exact half cent may come out either side, and the prospect check accepts any whole cent
   within half a cent of the exact sure amount. (b) Under the CRRA model with `gamma != 0` the value is a float too, so
   an exact tie may come out on either neighbouring cent, and the suite accepts either one (ruling 27). Both sentences are
   in the Whole cents paragraph of `course/modules/E/E3/project.html`, and the Grading mode paragraph lists the CRRA tie
   among the exceptions to exact comparison.
3. **The CRRA exact path is not affected by the mutants at `gamma = 0`.** There the engine rounds an exact `Fraction` with
   `floor(expected + 1/2)`, not `_half_up`, so none of these mutants changes that output. At `gamma > 0` under the CRRA
   model, a mutant differs from the reference only on an exact tie, which is case 2. The suite's instance draws contain
   no such tie: `instance.py` rejects any draw with a certainty equivalent within `1e-6` of a half cent. The one tie the
   suite constructs is `test_crra_exact_tie_at_nonzero_gamma_accepts_either_neighbour` (gamma = 1/2, exact value 219.5
   cents), and it accepts either neighbour, so it does not separate these mutants.
4. **Evidence.** Each file passes the whole suite on seeds 0 to 9 with the round-15 suite (run with
   `ledgers/E3/scripts/E3-d-r14/run_suite_seeds.sh`; output `ledgers/E3/scripts/E3-d-r15/out/equivalent_seeds_0-9.txt`).
   `tools/mutate_graders.py` never runs this directory. In round 14 the four were killed only by
   `test_half_cent_goes_up_on_exact_halves`, before the prospect exact-half check was relaxed to accept either neighbour.

Ruling 27 settled the question that round 14 left open. The four files stay here.

# Gamma-clamp mutants (ruling 28)

| File | Change | Differs from the reference only when | Evidence on the suite's inputs |
|---|---|---|---|
| `r11_03_gamma_hat_clamped_below_one_minus_1e3.py` | `gamma_hat` is clamped to 0.999 | the reference's `gamma_hat` exceeds 0.999 | largest `gamma_hat` over the 792 estimates is 0.98639 (own seed 352); no fixture exceeds 0.71 |
| `r12d_03_reported_gamma_floored_at_one_thousandth.py` | `gamma_hat` is floored at 0.001 | the reference's `gamma_hat` is below 0.001 | smallest `gamma_hat` over the 792 estimates is 0.02489 (own seed 373); no fixture is below 0.11 (the lowest is 0.1174) |

Ruling 28 asks for fixtures with `gamma_hat` above 0.999 and below 0.001 first. The round-15 probes
(`ledgers/E3/scripts/E3-d-r15/`) found the following.

- **No converged fit lies above 0.999.** The 4000-trial random scan (`gamma_scan_high_4000_r15.txt`) found none
  (`HIGH hits 0`). The targeted probe (`gamma_high_probe_r15.txt`) ran 480 low-noise participants with gamma truths of
  0.95, 0.99 and 0.999: 186 raised, and the largest converged `gamma_hat` with `kappa_hat` and `lambda_hat` below 1e4 was
  0.99444. The survey of 576 converged fits (`gamma_survey_800_r15.txt`) has its largest values near 0.994, several with
  `kappa_hat` above 1e12 (degenerate, separable answers). No fixture above 0.999 was found.
- **Below 0.001 the reference does converge, but only at the boundary.** The 2000-trial scan (`gamma_scan_low_2000_r15.txt`)
  found 85 converged fits with `gamma_hat < 0.001`, from 7.2e-13 up to 8.6e-4. These sit at the edge of the domain, which
  the instance guard in `instance.py` rejects for the suite's participants (the likelihood must beat the edge value by
  0.5).

Because no high-side fixture exists, the page takes the fallback branch of ruling 28. It states the supported range of
the curvature estimate as `[0.001, 0.999]` (Estimation convention in `project.html`) and states no outcome outside it.
Both mutants differ from the reference only outside that range, so both stay in this directory. A low-side fixture would
test behaviour that the page now leaves unstated, so it is not added.

# Removed: e12_03 (ruling 28)

`e12_03_search_returns_silently_when_it_stalls.py` is deleted. Its only difference from the reference was that it
returned the stalled point where the reference raised `the step became negligible before the score did`, the branch of
`_maximise` entered when the step becomes negligible before the score does and polishing does not move the point. No
run in the round-14 evidence reached that branch: the eight raising runs raise the other two messages, and every returning
run ends before it. Ruling 28 treats the branch as dead code, so the reference no longer raises there. It now ends the
search with `break`, and the error after the loop (`the likelihood maximisation did not converge`) reports the stall.
The mutant is removed with it.

# Evidence base (round 13, unchanged)

The reference's estimate on the 800 participants of generator seeds 0 to 399, each own participant (seed s) and second
participant (seed s + 7919), of which 792 return an estimate and 8 raise (the eight seeds the page names: own 108, 157,
165, 269; second 89, 110, 235, 373). The fixed fixtures are `FIXED_26_ANSWERS` (gamma_hat 0.6534), the twelve-response
B-side set (gamma_hat 0.1174), `LOW_KAPPA` (seed 30, gamma_hat 0.5190), `LARGE_LAMBDA` (seed 49, gamma_hat 0.7063) and
`STALL` (seed 108, raises). Scan scripts: `ledgers/E3/scripts/fixer-d-r13/`.

The residual gap is stated here rather than hidden: seeds 400 and above were not scanned, and the browser can draw any
31-bit seed.
