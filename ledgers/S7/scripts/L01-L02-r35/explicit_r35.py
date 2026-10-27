"""Round-35 explicit rows for the S7 L01-L02 fragment (imported by build_fragment_r35.py).

Every value below is copied from a command output of this round (logs under /tmp/ap1-r5/s7-l12-r35/) or from a
script archived in this repository. Scripts: ledgers/S7/scripts/L01-L02-r35/ (expmax_gap_r35.py,
koning_sim_r35.py, make_koning_mutants_r35.py, visible_text_r35.py, build_fragment_r35.py) and
ledgers/S7/scripts/L01-L02-r33r34/ (rederive.py, m5.py, scripts__recompute.py, scripts__prose_scan.py,
scripts__structure_checks.py).
"""

from __future__ import annotations

S = "ledgers/S7/scripts/L01-L02-r35"
A = "ledgers/S7/scripts/L01-L02-r33r34"
LOG = "/tmp/ap1-r5/s7-l12-r35/logs"
CARRY_L01_NOTE = "git diff -U0 e6d10ab HEAD: @@ -133 +133 @@"

EXPLICIT: dict[str, dict[str, str]] = {}

# ---------------- Koning (architect ruling applied) ----------------
EXPLICIT["L01-cmd-koning-spot-a2a631a"] = {
    "status": "PASS",
    "evidence": (
        "Round 35, architect ruling applied. Subject: the claims that the L01 span at line 436 makes about Koning and van "
        "Meer Theorem 1: claim 3 (phi_N = phi), the fixed-N test has its level, E_P[phi_n] is a martingale, and "
        "E_P[phi_tau] <= alpha for stopping times. The round-24 printed digits (size 0.05; stopping sizes 0.05012 ... 0.05004) "
        "are UNRECOVERABLE: the round-24 script and its output are gone and no committed file holds them. This row does not "
        "claim to reproduce them. (a) Committed check: tests/test_koning_spot.py (commit e6d10ab; the docstring and TOLERANCE "
        "line changed at a90b52b, TOLERANCE = 6*sqrt(0.05*0.95/400000) = 0.0020676). It checks claim 3 "
        "(test_the_last_conditional_expectation_is_the_test_itself), the level and the martingale "
        "(test_the_fixed_n_test_has_its_level_and_phi_n_is_a_martingale: every E[phi_n] within TOLERANCE of 0.05), and claim 1 "
        "for three first-crossing rules (test_stopping_at_a_look_never_pushes_the_size_above_the_level, bound LEVEL + TOLERANCE). "
        "Run: .venv/bin/python -m pytest -p no:cacheprovider -v tests/test_koning_spot.py tests/test_figure_kernels.py "
        "tests/test_docs_figures.py -> 49 passed in 18.67s (rc 0). (b) Independent run, scratch-free: "
        f"python -I {S}/koning_sim_r35.py (rc 0, 'ALL CHECKS PASS'), which loads _paths() from the committed test file and "
        "prints each quantity against its six-SE bound: size 0.0498375 (dev -0.0001625); claim 3 max|phi_N - phi| = 0.0; "
        "E[phi_n] for n = 1..20 within 0.0020676 of 0.05 (min 0.0495071 at n = 14, max 0.0499481 at n = 1); claim 1: "
        "E[phi_tau] = 0.0496554 (threshold 0.5, 6.979% stopped early), 0.0498147 (0.2, 18.761%), 0.0499906 (0.05, 70.718%), "
        "each within 6 SE of 0.05 (SE = 0.0003446). The Bernoulli SE bounds every such mean because Var[X] <= p(1-p) for "
        "X in [0,1] with mean p. (c) Mutants: T34-koning-test-mutants (5 of 5 killed, re-run this round with the mutants "
        "committed). Quoted digits on the page: L01.html contains no 0.0501, 0.0500 or 0.0498 (grep). The strings 50.6% and "
        "57.8% (L01.html line 436 and key-results line 680) and 0.64% / 1.79% are the Lab 4 expected-block values 0.506, 0.578, "
        "0.0064, 0.0179 (L01.html lines 430-431), reproduced by run_labs --unit S7 --page L01 (4/4, rc 0), which compares each "
        "lab's stdout to its page expected block. They are not Koning digits, and the line-436 Koning sentence quotes no number "
        "(T35-koning-quoted-digits). Result: the claims are checked, every quantity is within its six-SE bound, and the mutants "
        "are killed. PASS. The claim-1 check covers three named stopping rules; the general statement is the analytic proof "
        "row L01-math-koning-theorem1-proof-a2a631a (carried, line-level)."
    ),
}

EXPLICIT["T34-koning-test-mutants"] = {
    "status": "PASS",
    "evidence": (
        f"Round 35 re-run and archived. {S}/make_koning_mutants_r35.py writes five complete mutant copies of the committed test "
        "to ledgers/S7/mutants/koning-r35/ (each with a leading comment that names the error) and runs pytest on each. Output "
        f"({LOG}/koning_mutants.log, rc 0): committed test passes; cutoff-wrong-quantile (ppf(1-0.025)) FAILS "
        "test_the_fixed_n_test_has_its_level_and_phi_n_is_a_martingale; conditional-variance-off-by-one (N-j for N-(j+1)) FAILS "
        "the martingale test and test_stopping_at_a_look_never_pushes_the_size_above_the_level; look-ahead-stop (phi.argmax) "
        "FAILS the stopping test; claim-3-changed (0.999*reject) FAILS test_the_last_conditional_expectation_is_the_test_itself; "
        "cutoff-inflated-2pct (1.02 x cutoff, size about 0.0465) FAILS the level test. Killed 5 of 5. Each mutant differs from the "
        "committed test by one line (SRC.count(old) == 1 asserted in the script)."
    ),
}

EXPLICIT["T34-banned-roughly-half-caption"] = {
    "status": "PASS",
    "evidence": (
        "Round 35 re-derivation (the round-34 FAIL is cleared). (1) The phrase is gone: git diff -U0 e6d10ab HEAD shows the one "
        "hunk @@ -133 +133 @@; the visible text of L01 at a90b52b has no 'roughly half' (visible-text diff, T35-visible-text-diff; "
        "prose scan, T35-prose-differential). (2) The replacement is a calculation, BUILDER_RULES 1.2: its N values (10, 100, "
        "10,000) and its unit are stated, and it is derived from two formulas displayed on the page: bound (1), sqrt(2 ln N), "
        "in Theorem 2.1 (L01 lines 82-92), and the exact expectation, the integral of x N phi(x) Phi(x)^(N-1), named in the "
        "figure's source span on line 134 and drawn by figures-L01.js (expectedMaxNormal). The three gaps were recomputed from "
        f"scratch by {S}/expmax_gap_r35.py: 0.607213 (N = 10), 0.527261 (N = 100), 0.440316 (N = 10,000), which round to the page's "
        "0.61, 0.53 and 0.44 (T35-expmax-gap-numbers). (3) The unit is the standard deviation of each Z_n, which is 1 (Section 2: "
        "'each Z_n is approximately standard normal'; Theorem 2.1: 'each have the standard normal distribution'), and the figure's "
        "y-axis is 'Expected maximum (SD units)' (figures-L01.js line 61) (T35-caption-unit-sd). (4) Caveat, stated plainly: the "
        "page prints the arithmetic only through the two displayed formulas; the three gaps are not printed live by the figure. "
        "The reader reproduces them from those formulas, so the sentence meets 1.2(c) and is not a vague quantity. (5) The "
        "surrounding paragraph still holds: '(3) sits slightly above the exact expectation for every N >= 3' (checked for "
        "N = 3..10,000) and 'At N = 2 it is below' (T35-caption-sign-sweep). PASS."
    ),
}

EXPLICIT["L01-L02-expmax-claims-a2a631a"] = {
    "status": "PASS",
    "evidence": (
        "Round 35 re-derived for the caption sentences it cites. Section 3 caption (line 133): the (3) sign and the N = 2 values "
        "(1/sqrt(pi) = 0.564190; (3) at N = 2 = 0.519755) are re-derived in L01-num-fig-caption-n2 and T35-caption-sign-sweep; the gap "
        "sentence is ruled in T34-banned-roughly-half-caption and recomputed in T35-expmax-gap-numbers. Lab 1 lines (hypothesis and "
        "interpretation) are byte-identical since e6d10ab, as is the figure desc (figures-L01.js lines 55-71). Problem M1(b)-(c) (L01 "
        "lines 504-505) is re-derived in L01-cmd-m1-m4-a2a631a; L02 Problem M3 (line 401) in L02-cmd-m3-example42-a2a631a. PASS."
    ),
}

# ---------------- Round-35 re-derivations of caption rows ----------------
EXPLICIT["L01-num-fig-caption-n2"] = {
    "status": "PASS",
    "evidence": (
        "Round 35 re-derived. L01.html line 133: '1/sqrt(pi) = 0.564' and '(3) gives gamma Phi^-1(1 - 1/(2e)) = 0.520'. "
        f"{S}/expmax_gap_r35.py prints 1/sqrt(pi) = 0.564190 and the exact E[max of 2] = 0.5641895835 (quad), and (3) at N = 2 = "
        "0.519755 (the Phi^-1(0.5) term is 0). Both round to the page's values. The N = 2 sign ((3) - exact = -0.044434) is "
        "below, as the caption says."
    ),
}
EXPLICIT["L01-num-fig-caption"] = {
    "status": "PASS",
    "evidence": (
        "Round 35 re-derived for the caption (L01.html line 133) and the expected-max desc (figures-L01.js lines 55-71, unchanged "
        f"since e6d10ab). The desc says the approximation 'lies below it at N = 2 and just above it from N = 3 on' and the bound "
        f"'well above both': {S}/expmax_gap_r35.py confirms (3) - exact > 0 for every N = 3..10000 and < 0 at N = 2, and bound - "
        "exact = 0.61 (N = 10), 0.53 (N = 100), 0.44 (N = 10,000) SD. The curve values match the page sentence."
    ),
}
EXPLICIT["L01-fig-1-caption"] = {
    "status": "PASS",
    "evidence": (
        "Round 35 re-derived for the new caption (L01.html line 133). The two numbers that were there before are re-computed: "
        "1/sqrt(pi) = 0.564190 and (3) at N = 2 = 0.519755 (rounds to 0.520); the 'roughly half a standard deviation' sentence "
        "that the round-34 FAIL quoted is removed (git diff -U0). The replacement sentence is ruled in T34-banned-roughly-half-caption "
        "(1.2(c)); its three gaps are recomputed in T35-expmax-gap-numbers; its unit is ruled in T35-caption-unit-sd. PASS."
    ),
}
EXPLICIT["L01-fig-expected-max"] = {
    "status": "PASS",
    "evidence": (
        "Round 35 re-derived for the section 3 figure (data-chart expected-max, static): the caption (line 133) is checked "
        "sentence by sentence in T35-caption-sign-sweep, T35-expmax-gap-numbers and T35-caption-unit-sd; the desc (figures-L01.js "
        "lines 55-71) and the figure code are byte-identical since e6d10ab; the exact curve it draws is the one "
        "test_figure_kernels.py checks against the Python reference (49 passed, round 35). PASS."
    ),
}
EXPLICIT["L01-fig-expected-max-desc-202ea24"] = {
    "status": "PASS",
    "evidence": (
        "Round 35 re-derived: the figure section (L01.html section 3 caption at line 133) and the desc (figures-L01.js lines 55-71, "
        "byte-identical since e6d10ab). The desc's claims (below at N = 2, just above from N = 3, bound well above both) agree "
        "with the recomputed sweep (T35-caption-sign-sweep), and the caption's numbers agree with T35-expmax-gap-numbers. PASS."
    ),
}
EXPLICIT["L01-fig-expected-max-gap-e968af2"] = {
    "status": "PASS",
    "evidence": (
        "Round 35 re-derived, because the gap sentence (caption line 133) changed. The three gaps (bound (1) minus exact, SD units): "
        "N = 10: 0.607213 (0.61); N = 100: 0.527261 (0.53); N = 10,000: 0.440316 (0.44). Scratch-free recomputation: "
        f"{S}/expmax_gap_r35.py (quad and grid agree to 1.2e-11). The desc (figures-L01.js lines 55-71) is unchanged. PASS. "
        "See T35-expmax-gap-numbers for the full table."
    ),
}
EXPLICIT["L01-fig-expected-max-765bcb1"] = {
    "status": "PASS",
    "evidence": (
        "Round 35 re-derived for the static section 3 figure (caption line 133 and figures-L01.js lines 55-71, byte-identical since "
        "e6d10ab). Caption sentences are checked in T35-caption-sign-sweep, T35-expmax-gap-numbers and T35-caption-unit-sd. "
        "The figure's rendering is covered by page_smoke (round 35 PASS, zero overlap and no horizontal scroll at 360 px). PASS."
    ),
}
EXPLICIT["L01-fig-expected-max-a2a631a"] = {
    "status": "PASS",
    "evidence": (
        "Round 35 re-derived for the static section 3 figure (caption line 133 and desc, figures-L01.js lines 55-71). Caption "
        "sentences: T35-caption-sign-sweep, T35-expmax-gap-numbers, T35-caption-unit-sd. Rendering: page_smoke --pages L01 L02 "
        "PASS (round 35). PASS."
    ),
}
EXPLICIT["L01-fig-1-legibility"] = {
    "status": "PASS",
    "evidence": (
        "Round 35 re-checked, because the caption grew by one sentence. The SVG (figures-L01.js lines 55-71, chart.js, course.css) "
        "is byte-identical since e6d10ab. Round 35 page_smoke --unit S7 --pages L01 L02 (rc 0, 'page_smoke S7: PASS'): each page in "
        "light and dark at 1280 px and at 360 px, with no horizontal scroll (document scrollWidth - innerWidth <= 1 px), no SVG text "
        "leaving its SVG and no overlaps. Limit: no screenshot of the caption text itself was taken this round; the 360 px check is "
        "the horizontal-scroll and geometry check that page_smoke applies to every figcaption. PASS on that evidence."
    ),
}
EXPLICIT["L01-fig-1-provenance"] = {
    "status": "PASS",
    "evidence": (
        "Round 35 re-checked: the section 3 figure's source line (L01.html line 134, 'Computed live in your browser: the exact curve "
        "integrates x N phi(x) Phi(x)^(N-1) numerically ...') is unchanged (one-line hunk at line 133 only, git diff -U0). The "
        "curve data come from figures-L01.js and stats.js (byte-identical since e6d10ab), and the caption's numbers come from the "
        "same integrand (T35-expmax-gap-numbers). PASS."
    ),
}
EXPLICIT["L01-fig-1-furniture"] = {
    "status": "PASS",
    "evidence": (
        "Round 35 re-checked: the figure has its title, axes ('Number of independent trials N (log scale)', 'Expected maximum "
        "(SD units)'), source line and caption (figures-L01.js lines 55-71 and L01.html lines 132-134). Only the caption text "
        "changed (line 133); its sentences are ruled in T35-caption-unit-sd and T35-caption-sign-sweep. PASS."
    ),
}
EXPLICIT["L01-banned-roughly-half"] = {
    "status": "PASS",
    "evidence": (
        "Round 35 re-derived. The figure caption (line 133) no longer contains 'roughly half a standard deviation' "
        "(visible-text diff: T35-visible-text-diff). A recursive grep for 'roughly half' over the L01 and L02 visible text, "
        "cards.json and figures-L01.js / figures-L02.js at a90b52b finds 0 hits in L01 and L02 (the prose scan's 'roughly' count "
        "drops from 2 to 1 in L01; the remaining 'roughly zero' in quiz item 10 is not in the banned list). The quiz phrase "
        "'about half the time' (line 768, keyed option) is backed by Lab 2's printed output (T35-quiz10-about-half). PASS."
    ),
}
EXPLICIT["L01-L02-fig-captions-states-8d2fca9"] = {
    "status": "PASS",
    "evidence": (
        "Round 35 re-derived for the figcaption of the section 3 figure (line 133, the only changed caption); other live figures' "
        "captions are byte-identical since e6d10ab. The new caption sentence is ruled in T34-banned-roughly-half-caption. "
        "Rendering: page_smoke PASS (round 35). PASS."
    ),
}
EXPLICIT["L01-fig-drive-e968af2"] = {
    "status": "PASS",
    "evidence": (
        "Round 35: the section 2 control (years 1-20) is unchanged (figures-L01.js lines 12-53 and the section 2 markup are "
        "byte-identical since e6d10ab); the section 3 figure is static, so it has no control state, and its caption (line 133) is "
        "ruled in T35-caption-sign-sweep, T35-expmax-gap-numbers and T35-caption-unit-sd. The round-33 Chromium drive "
        "(L01-L02-cmd-fig-drive-a2a631a) is carried line-level for the section 2 control. PASS."
    ),
}

# ---------------- Whole-page numeric and text sweeps re-run on the new line ----------------
EXPLICIT["T33-decimal-coverage"] = {
    "status": "PASS",
    "evidence": (
        "Round 35 re-derived as a differential. The round-33 coverage (every decimal in the visible prose of L01 and L02, 327 "
        "distinct tokens at e6d10ab, each traced to a locator) still holds for every token that is on a line other than 133. "
        "The decimal-token diff of L01 visible text (e6d10ab -> a90b52b, 418 -> 421 tokens, 219 -> 222 distinct) adds exactly "
        "0.61, 0.53 and 0.44 and removes none (T35-decimal-differential). Those three are traced in T35-expmax-gap-numbers. "
        "L02 visible text is identical. PASS."
    ),
}
EXPLICIT["L01-num-recompute-r19-e968af2"] = {
    "status": "PASS",
    "evidence": (
        f"Round 35 re-run: python -I {A}/scripts__recompute.py <txt dir> on the a90b52b visible text (T35-recompute-47): 47 checks, "
        "0 failures (TOTAL checks 47 failures 0: []). It covers every derived number of L01 and L02 that the round-19 sweep named. "
        "PASS."
    ),
}
EXPLICIT["L01-L02-numbers-unmentioned-0f4068a"] = {
    "status": "PASS",
    "evidence": (
        "Round 35 re-run as a differential: T35-decimal-differential (only 0.61, 0.53, 0.44 are new) and T35-recompute-47 "
        "(47 checks, 0 failures) cover the numeric tokens that the diff changes. PASS."
    ),
}
EXPLICIT["L01-L02-numbers-sweep-0f4068a"] = {
    "status": "PASS",
    "evidence": (
        "Round 35 re-run: the sweep is T35-recompute-47 (47 checks, 0 failures) plus the L01 decimal differential "
        "(T35-decimal-differential). The L02 text is identical to e6d10ab (T35-visible-text-diff). PASS."
    ),
}
EXPLICIT["L01-L02-cmd-expmax-sweep-a2a631a"] = {
    "status": "PASS",
    "evidence": (
        f"Round 35 re-run: .venv/bin/python -I {S}/expmax_gap_r35.py (rc 0). It computes the exact expected maximum of N iid "
        "standard normals by scipy quad (N = 2, 10, 100, 10000) and on a 200001-point trapezoid grid for every N = 2..10000; the two "
        "methods agree to 1.196e-11. It prints bound sqrt(2 ln N) minus exact (0.613220 at N = 2; 0.607213 at N = 10; 0.527261 at "
        "N = 100; 0.440316 at N = 10,000) and checks the sign of (3) - exact for N = 3..10000 (True; no N with diff <= 0). PASS."
    ),
}
EXPLICIT["L01-L02-cmd-prose-scan-a2a631a"] = {
    "status": "PASS",
    "evidence": (
        f"Round 35 re-run, differential: visible text extracted from e6d10ab and a90b52b by {S}/visible_text_r35.py; scanned by "
        f"{A}/scripts__prose_scan.py. Outputs: e6d10ab -> L01 '?' 25, 'about ' 18, 'roughly' 2, '...' / ellipsis 2; a90b52b -> the same "
        "except 'roughly' 1. L02 identical (? 13, about 15, roughly 1, ellipsis 3). Cards: 243 total, 56 L01+L02, no duplicate ids. "
        "No new banned string or question mark is introduced by the caption change (T35-prose-differential). PASS."
    ),
}

# ---------------- Commands re-run in round 35 ----------------
EXPLICIT["L01-cmd-m1-m4-a2a631a"] = {
    "status": "PASS",
    "evidence": (
        f"Round 35 re-run of the archived round-34 script {A}/rederive.py (python -I, rc 0): M1(a) bound 2.4477 x (1/sqrt(756)) x "
        "sqrt(252) = 1.4132 (page 1.413). M1(b) Phi^-1(0.95) = 1.6449, Phi^-1(1 - 1/(20e)) = 2.0881, bracket 1.9007, annualized "
        "1.0974 (page 1.097). M4(a) Z = 2.6726 (page 2.673). M4(b) M504 = 6.2442 (page 6.244), b504 = 73.2127 (page 73.21). M4(c) "
        "interval [-0.02622, 0.26431] per day, annualized [-0.42, 4.20], point 1.89, fixed half-width 0.08730. Matches the "
        "round-34 values exactly. The round-34 scratch path is superseded by the archived script. PASS."
    ),
}
EXPLICIT["L02-cmd-m3-example42-a2a631a"] = {
    "status": "PASS",
    "evidence": (
        f"Round 35 re-run of {A}/rederive.py (rc 0) and {A}/scripts__recompute.py (L02-num-M3 and L02-num-ex42 checks). M3 "
        "(page line 401): Phi^-1(0.995) = 2.575829 (page 2.576), Phi^-1(0.9995) = 3.290527 (3.291), Phi^-1(0.99995) = 3.890592 "
        "(3.891); bounds sqrt(2 ln 100) = 3.034854 (3.035), sqrt(2 ln 1000) = 3.716922 (3.717), sqrt(2 ln 10000) = 4.291932 (4.292). "
        "Example 4.2 (page line 294): critical values 1.9600, 2.8070, 3.4808, 4.0556 (page 1.960, 2.807, 3.481, 4.056); powers "
        "0.938224, 0.755835, 0.507677, 0.289233 (page 0.938, 0.756, 0.508, 0.289). PASS."
    ),
}
EXPLICIT["L01-cmd-m5-a2a631a"] = {
    "status": "PASS",
    "evidence": (
        f"Round 35 re-run of the archived {A}/m5.py (rc 0): l = 2 ln 20 = 5.991465; fixed point u* = 8.211968 (page 8.212); "
        "sqrt(1+u*) = 3.035122 (page 3.035); kappa = 756/u* = 92.0608. Minimum over integer t = 1..199999 at kappa = 252 is "
        "3.035122 at t = 2069 (continuous optimum 2069.42); b_756/sqrt(756) at kappa = 252 = 3.1364; b_2520/sqrt(2520) at "
        "kappa = 92.1 = 3.1109; b_36/sqrt(36) = 7.0 (page 7.0). Matches round 34 exactly. PASS."
    ),
}
EXPLICIT["L01-L02-cmd-run_labs-S7-a2a631a"] = {
    "status": "PASS",
    "evidence": (
        f"Round 35 re-run: .venv/bin/python tools/run_labs.py --unit S7 (rc 0, log {LOG}/run_labs.log): 'run_labs S7: PASS (42/42)'. "
        "The run compares each lab's stdout to its page's expected block (run_labs docstring). PASS."
    ),
}
EXPLICIT["L01-L02-cmd-run_labs-L01-a2a631a"] = {
    "status": "PASS",
    "evidence": (
        "Round 35 re-run: .venv/bin/python tools/run_labs.py --unit S7 --page L01 (rc 0): 'run_labs S7: PASS (4/4)'. Lab 2's "
        "printed share 0.52 (expected block line 212) is reproduced on this run (the twin prints 0.52). PASS."
    ),
}
EXPLICIT["L01-L02-cmd-run_labs-L02-a2a631a"] = {
    "status": "PASS",
    "evidence": "Round 35 re-run: .venv/bin/python tools/run_labs.py --unit S7 --page L02 (rc 0): 'run_labs S7: PASS (3/3)'. PASS.",
}
EXPLICIT["L01-L02-cmd-ruff-mypy-a2a631a"] = {
    "status": "PASS",
    "evidence": (
        f"Round 35 re-run, repo-wide (logs {LOG}/ruff_check.log, ruff_format.log, mypy.log): .venv/bin/ruff check . -> 'All checks "
        "passed!' (rc 0); .venv/bin/ruff format --check . -> '125 files already formatted' (rc 0); .venv/bin/mypy -> 'Success: no "
        "issues found in 102 source files' (rc 0). pyproject.toml changed at a90b52b (extend-exclude now also ledgers/*/scripts); the "
        "gates ran on that config. PASS."
    ),
}
EXPLICIT["L01-L02-lab-timings-0f4068a"] = {
    "status": "PASS",
    "evidence": (
        f"Round 35 re-run (same page_smoke run, {LOG}/page_smoke.log): runtime boot (with numpy) 1.0 s; package preload 0.2 s; "
        "L01 labs 0.2, 0.1, 0.1, 0.4 s; L02 labs 0.1, 0.0, 0.1 s. All far below the 10 s limit. PASS."
    ),
}
EXPLICIT["L01-L02-cmd-page_smoke-a2a631a"] = {
    "status": "PASS",
    "evidence": (
        f"Round 35 re-run: .venv/bin/python tools/page_smoke.py --unit S7 --pages L01 L02 (rc 0, log {LOG}/page_smoke.log): "
        "'page_smoke modules/S/S7/L01.html: PASS', 'page_smoke modules/S/S7/L02.html: PASS', 'page_smoke S7: PASS'. PASS."
    ),
}
EXPLICIT["L01-L02-cmd-pytest-figure-kernels-a2a631a"] = {
    "status": "PASS",
    "evidence": (
        f"Round 35 re-run: .venv/bin/python -m pytest -p no:cacheprovider -v tests/test_koning_spot.py tests/test_figure_kernels.py "
        f"tests/test_docs_figures.py (rc 0, log {LOG}/pytest_3_verbose.log): '49 passed in 18.67s'. The Koning file ran "
        "3 tests. PASS."
    ),
}
EXPLICIT["L01-L02-cmd-check_pages-a2a631a"] = {
    "status": "PASS",
    "evidence": f"Round 35 re-run: .venv/bin/python tools/check_pages.py --unit S7 (rc 0): 'check_pages S7: PASS' (log {LOG}/check_pages.log). PASS.",
}
EXPLICIT["L01-L02-cmd-check_dag-a2a631a"] = {
    "status": "PASS",
    "evidence": f"Round 35 re-run: .venv/bin/python tools/check_dag.py --unit S7 (rc 0): 'check_dag S7: PASS' (log {LOG}/check_dag.log). PASS.",
}
EXPLICIT["L01-L02-cmd-check_projects-a2a631a"] = {
    "status": "PASS",
    "evidence": f"Round 35 re-run: .venv/bin/python tools/check_projects.py --unit S7 (rc 0): 'check_projects S7: PASS' (log {LOG}/check_projects.log). PASS.",
}
EXPLICIT["L01-L02-cmd-verify_refs-live-S7-a2a631a"] = {
    "status": "PASS",
    "evidence": (
        f"Round 35 re-run (live, network permitted, no access block): .venv/bin/python tools/verify_refs.py --unit S7 --workers 1 "
        f"(rc 0, log {LOG}/verify_refs_live.log): 'live re-verification of S7: 94 of 560 entries, 0 problems'. The 94 entries are "
        "those whose used_by names S7 (checked in references/references.json). PASS."
    ),
}
EXPLICIT["L01-L02-cmd-verify_refs-offline-a2a631a"] = {
    "status": "PASS",
    "evidence": (
        f"Round 35 re-run: .venv/bin/python tools/verify_refs.py --offline (rc 0, log {LOG}/verify_refs_offline.log): "
        "'offline integrity: 560 entries, 0 problems'. PASS."
    ),
}
EXPLICIT["L01-L02-cmd-crossref-koning-a2a631a"] = {
    "status": "PASS",
    "evidence": (
        "Round 35: koning2026anytime is in the S7 live scope (references/references.json: its used_by is ['S7']), so the live run "
        "above (94 of 560 entries, 0 problems, rc 0) re-verified its Crossref record. The record is not re-typed here. PASS."
    ),
}
EXPLICIT["L01-L02-cmd-git-a2a631a"] = {
    "status": "PASS",
    "evidence": (
        f"Round 35: git rev-parse --short HEAD = a90b52b; base e6d10ab. git diff --stat e6d10ab HEAD: 55 files. The slice files "
        "(course/modules/S/S7, tests, tools, references, notation, atlas, course/assets) changed only at course/modules/S/S7/L01.html "
        "line 133 and tests/test_koning_spot.py (docstring and TOLERANCE line); VERIFIER_RULES.md (+6 lines), pyproject.toml (1 line changed), "
        "and ledgers/ changed as well. The uncommitted working tree holds this round's fragment (ledgers/S7/L01-L02.json) and the "
        "new ledgers/S7/scripts/L01-L02-r35/ and ledgers/S7/mutants/koning-r35/. PASS."
    ),
}
EXPLICIT["L01-xref-R1-atlas"] = {
    "status": "PASS",
    "evidence": (
        "Carried from round 34 (atlas/A8.contract.md byte-identical since e6d10ab; course/modules/S/S7/L01.html byte-identical since "
        f"e6d10ab except line 133, the only changed line ({CARRY_L01_NOTE})): the R1 sentence is at line 615 (8d2fca9 numbering) and is "
        "outside the changed line. Round-34 evidence follows: " 
        "Round 34 re-check, because atlas/A8.contract.md changed since bcf4e25; that change is in the e6d10ab amendment and "
        "is unchanged since e6d10ab (git diff --quiet). Its 'Consumed by' and integrity_report signature are unchanged. PASS."
    ),
}


# Rows whose text matches the line-133 screen only by a false positive ('BLUEPRINT section 3', 'Section 3.5', a count of
# 133, the 'expected maximum' in lab or card prose). Reviewed by hand in round 35; carried on the line-level variant.
CARRY_REVIEWED = {
    "L01-grade-bailey2014", "L01-cite-bailey2014deflated", "L01-math-P1", "L01-cite-howard2021time",
    "L01-grade-wang2023catoni", "L01-cards-misc4-variants", "L01-keyresults-row11-hunk", "L01-cards-c189-grade",
    "L01-cards-c238-45fff85", "L01-L02-key-howard2021time-e968af2", "L01-cite-howard-arxivv9-e968af2",
    "L01-L02-counter-white2000reality-e968af2", "L01-L02-cards-inventory-0f4068a", "L01-grade-koning2026anytime",
    "L01-banned-ellipsis-722-a2a631a", "T33-holm-states",
}

# ---------------- New rows ----------------
NEW_ROWS: list[dict[str, str]] = [
    {
        "id": "T35-git-hunk-scope",
        "check": "2.9-structure",
        "location": "course/modules/S/S7/L01.html; every slice file",
        "status": "PASS",
        "evidence": (
            f"git diff -U0 e6d10ab HEAD -- course/modules/S/S7/L01.html gives exactly one hunk, '@@ -133 +133 @@' (the figcaption "
            "of the section 3 figure). git diff --quiet e6d10ab HEAD -- course/modules/S/S7 is 1 (changed) only for L01.html. "
            "L02.html, cards.json, figures-L01.js, figures-L02.js, tests/labs/S7, references/references.json, notation/notation.json, "
            "course/assets/data/notation.json, tools/page_smoke.py, tools/verify_refs.py and tools/run_labs.py: git diff --quiet rc 0 "
            "(byte-identical). Every carried row below relies on this."
        ),
    },
    {
        "id": "T35-carry-identity",
        "check": "2.9-structure",
        "location": "ledgers/S7/L01-L02.json (carried rows)",
        "status": "PASS",
        "evidence": (
            "Carry rule applied by ledgers/S7/scripts/L01-L02-r35/build_fragment_r35.py. For every row whose evidence began "
            "'Carried from round 33 (FILES byte-identical since bcf4e25)', the script runs git diff --quiet e6d10ab HEAD -- FILES. "
            "For every group without L01.html it passed (rc 0; the script exits on any change). Rows whose subject includes L01.html "
            "carry the line-level variant ('byte-identical since e6d10ab except line 133, the only changed line (git diff -U0 e6d10ab "
            "HEAD: @@ -133 +133 @@)'), and the script refuses to carry any such row whose location or evidence cites line 133, the "
            "caption, the expected-max figure or the removed phrase: those rows are re-derived in this fragment. 21 round-34 rows "
            "were re-run or re-derived explicitly. The 70 rows that cite vanished scratch scripts stay carried on byte-identity "
            "(architect decision); scripts from now on are archived in ledgers/S7/scripts/L01-L02-r35/."
        ),
    },
    {
        "id": "T35-visible-text-diff",
        "check": "2.9-structure",
        "location": "course/modules/S/S7/L01.html, L02.html visible text",
        "status": "PASS",
        "evidence": (
            f"python -I {S}/visible_text_r35.py e6d10ab and HEAD write the visible text of both lessons (scripts and styles dropped). "
            "diff of L01.txt: one changed line (line 60), the caption of the section 3 figure; L02.txt: identical. This is the basis of "
            "the line-level variant for every L01 row: nothing but that caption changed in the lesson text. PASS."
        ),
    },
    {
        "id": "T35-prose-differential",
        "check": "2.9-banned",
        "location": "L01.html and L02.html visible text (banned strings, question marks, ellipses)",
        "status": "PASS",
        "evidence": (
            f"python -I {A}/scripts__prose_scan.py <txt dir> <repo>, run on the e6d10ab and a90b52b texts. The outputs differ only in "
            "'L01 chars 76028 -> 76104' and 'HIT L01 roughly 2 -> 1' (the removed 'roughly half a standard deviation'). L01 '?' 25 and "
            "'about ' 18 are unchanged; the new sentence adds no banned string, no question mark, no ellipsis and no 'about'. "
            "L02 unchanged. PASS."
        ),
    },
    {
        "id": "T35-decimal-differential",
        "check": "2.2-number",
        "location": "course/modules/S/S7/L01.html visible text (decimal tokens)",
        "status": "PASS",
        "evidence": (
            "Decimal tokens (regex on the visible text, both versions): e6d10ab 418 tokens, 219 distinct; a90b52b 421 tokens, 222 "
            "distinct. Added: 0.61, 0.53, 0.44. Removed: none. L02 unchanged. Each new token is recomputed in T35-expmax-gap-numbers "
            "(0.607213, 0.527261, 0.440316 SD). PASS."
        ),
    },
    {
        "id": "T35-expmax-gap-numbers",
        "check": "2.2-number",
        "location": "course/modules/S/S7/L01.html line 133 (caption); Theorem 2.1 (lines 82-92); Definition 3.1 (line 125)",
        "status": "PASS",
        "evidence": (
            f"{S}/expmax_gap_r35.py (rc 0, 10.6 s). Exact E[max of N iid N(0,1)] = integral of x N phi(x) Phi(x)^(N-1) (scipy quad, "
            "and a grid), bound sqrt(2 ln N): N = 2: exact 0.5641895835, bound 1.1774100225, gap 0.613220; N = 3: exact 0.8462843753, gap "
            "0.636019; N = 10: exact 1.5387527308, bound 2.1459660263, gap 0.607213; N = 100: exact 2.5075936364, bound 3.0348542588, "
            "gap 0.527261; N = 1000: gap 0.475486; N = 10000: exact 3.8516158171, bound 4.2919320526, gap 0.440316. The caption's "
            "'0.61 standard deviations at N = 10, 0.53 at N = 100 and 0.44 at N = 10,000' matches to two places. The gap is in SD units, "
            "i.e. the SD of each Z_n (=1). PASS."
        ),
    },
    {
        "id": "T35-caption-unit-sd",
        "check": "2.2-number",
        "location": "course/modules/S/S7/L01.html Section 2 (lines 79-92, Theorem 2.1 at lines 82-92), figcaption line 133; course/modules/S/S7/figures-L01.js line 61",
        "status": "PASS",
        "evidence": (
            "The caption's 'standard deviations' is the unit the page itself defines: Section 2 standardizes Z_n so that 'each Z_n is "
            "approximately standard normal'; Theorem 2.1 assumes 'Z_1, ..., Z_N each have the standard normal distribution' and bounds "
            "E[max Z_n]; the figure's y-axis label is 'Expected maximum (SD units)' (figures-L01.js line 61). So the unit is the SD of "
            "one Z_n, which is 1. Read this way the sentence is true, and the gap in that unit equals the number printed. PASS."
        ),
    },
    {
        "id": "T35-caption-sign-sweep",
        "check": "2.2-number",
        "location": "course/modules/S/S7/L01.html line 133 (first two sentences); figures-L01.js lines 55-71 (desc)",
        "status": "PASS",
        "evidence": (
            f"{S}/expmax_gap_r35.py: (3) - exact > 0 for every N = 3..10000 (True; first N with diff <= 0: none), and (3) - exact at N = 2 "
            "= -0.044434 (below). 1/sqrt(pi) = 0.564190 (the caption's 0.564). (3) at N = 2 = gamma Phi^-1(1 - 1/(2e)) = 0.519755 "
            "(the caption's 0.520). The desc's 'just above it from N = 3 on' agrees. PASS."
        ),
    },
    {
        "id": "T35-quiz10-about-half",
        "check": "2.2-number",
        "location": "course/modules/S/S7/L01.html quiz item 10 (line 768, keyed option); Lab 2 expected block line 212",
        "status": "PASS",
        "evidence": (
            "The keyed option 'It fell to roughly zero, losing money about half the time' states the share of out-of-sample losses. "
            "That share is Lab 2's printed output 'share of selections that lose money out of sample: 0.52' (L01.html line 212, expected "
            "block; the twin tests/labs/S7/lab-S7-L01-2.py prints 0.52 on this run; run_labs --page L01 PASS). So 'about half' is a "
            "computed live number of the lab, meeting BUILDER_RULES 1.2(a). PASS."
        ),
    },
    {
        "id": "T35-koning-claims-coverage",
        "check": "2.4-math",
        "location": "tests/test_koning_spot.py; course/modules/S/S7/L01.html line 436 (Koning span: Theorem 1, claims 1 and 3)",
        "status": "PASS",
        "evidence": (
            "Claim-by-claim coverage of the committed test (VERIFIER_RULES 2.4; architect ruling). Claim 3 (phi_N = phi): "
            "test_the_last_conditional_expectation_is_the_test_itself, exact (max deviation 0.0). Fixed-N level 0.05: "
            "test_the_fixed_n_test_has_its_level_and_phi_n_is_a_martingale, |E[phi] - 0.05| < 6SE (measured 0.0001625). Martingale "
            "E[phi_n] constant in n: the same test, every E[phi_n] within 6SE of 0.05 (measured range 0.0495071 to 0.0499481). Claim 1 "
            "(E[phi_tau] <= alpha for stopping times): test_stopping_at_a_look_never_pushes_the_size_above_the_level for three "
            "first-crossing rules, bound 0.05 + 6SE (measured 0.0496554, 0.0498147, 0.0499906). The tolerance is 6 SE (0.0020676), as "
            "the architect's ruling states. The general statement is proved analytically in L01-math-koning-theorem1-proof-a2a631a "
            "(carried). PASS."
        ),
    },
    {
        "id": "T35-koning-quoted-digits",
        "check": "2.2-number",
        "location": "course/modules/S/S7/L01.html (all); course/modules/S/S7/cards.json",
        "status": "PASS",
        "evidence": (
            "Grep of L01.html, L02.html and cards.json for 0.0501, 0.0500, 0.0498, 0.0496, 0.0499, 50.6, 57.8 and Koning / van Meer: "
            "no 0.0501, 0.0500, 0.0498, 0.0496 or 0.0499 anywhere. 50.6% and 57.8% appear at L01.html line 436 and key-results line 680 "
            "(and 0.506 / 0.578 in the expected block, lines 430-431, which are the Lab 4 values): these are Lab 4 numbers, not the "
            "round-24 Koning digits, and run_labs --page L01 (rc 0) reproduces them through the page's expected block. The Koning sentence "
            "on line 436 quotes no number. So no round-24 Koning digit is quoted on the page. PASS."
        ),
    },
    {
        "id": "T35-recompute-47",
        "check": "2.2-number",
        "location": "course/modules/S/S7/L01.html, L02.html (all derived numbers the script names)",
        "status": "PASS",
        "evidence": (
            f"python -I {A}/scripts__recompute.py <txt dir> on the a90b52b visible text (rc 0): 'TOTAL checks 47 failures 0: []'. The "
            "script recomputes each derived number of L01 and L02 (for example the M3 bounds 3.035, 3.717, 4.292; the Holm and "
            "Bonferroni values; the Example 4.2 critical values and powers; the Lab 2 p-values) and checks that the printed token is on the "
            "page. PASS."
        ),
    },
    {
        "id": "T35-structure-checks",
        "check": "2.9-structure",
        "location": "course/modules/S/S7/L01.html, L02.html (data-cite keys, dfn, references)",
        "status": "PASS",
        "evidence": (
            f"python -I {A}/scripts__structure_checks.py <repo> (rc 0): L01 distinct data-cite keys 15, unresolved []; L02 distinct keys 3, "
            "unresolved []. The change is text-only inside one figcaption; no id, dfn, data-cite or heading changed (git diff -U0). PASS."
        ),
    },
]

MUTANT_ROWS: list[tuple[str, str]] = [
    ("cutoff-wrong-quantile: cutoff uses the two-sided 0.975 quantile instead of the one-sided 0.95 quantile",
     "test_the_fixed_n_test_has_its_level_and_phi_n_is_a_martingale"),
    ("conditional-variance-off-by-one: phi_n uses N-j instead of N-(j+1), breaking the martingale",
     "test_the_fixed_n_test_has_its_level_and_phi_n_is_a_martingale"),
    ("look-ahead-stop: the stopping rule reads the maximum over all looks, not the first crossing",
     "test_stopping_at_a_look_never_pushes_the_size_above_the_level"),
    ("claim-3-changed: phi_N = 0.999 * reject, so phi_N differs from the fixed-N test",
     "test_the_last_conditional_expectation_is_the_test_itself"),
    ("cutoff-inflated-2pct: cutoff inflated by 2 percent, size about 0.0465 (level too low)",
     "test_the_fixed_n_test_has_its_level_and_phi_n_is_a_martingale"),
]

NOTES = [
    "ROUND 35: verifier re-check of the S7 L01-L02 slice at a90b52b (base e6d10ab). Architect ruling applied to the Koning row "
    "(L01-cmd-koning-spot-a2a631a): PASS. The round-24 printed Koning digits are unrecoverable; the row says so and does not reproduce them.",
    "Delta (git diff e6d10ab..a90b52b): L01.html line 133 only (the caption). It removed 'loose by roughly half a standard deviation' "
    "and added 'exceeds the exact expectation by 0.61 standard deviations at N = 10, 0.53 at N = 100 and 0.44 at N = 10,000'. The three "
    "numbers were recomputed from scratch (expmax_gap_r35.py: 0.607213, 0.527261, 0.440316 SD; quad and grid agree to 1.2e-11). "
    "Ruling (BUILDER_RULES 1.2(c)): the sentence is a calculation whose N and unit are stated and whose inputs are displayed on the page "
    "(bound (1) in Theorem 2.1; the exact integrand in the figure source line). The page does not print the arithmetic, and the figure "
    "does not print the gap; this is recorded as a caveat in T34-banned-roughly-half-caption.",
    "Koning: tests/test_koning_spot.py tolerance is now 6 SE = 6*sqrt(0.05*0.95/400000) = 0.0020676. koning_sim_r35.py (committed "
    "_paths(), seed 20261021) reproduces the committed values (size 0.0498375; E[phi_tau] 0.0496554, 0.0498147, 0.0499906) and passes "
    "every six-SE check. Five repo mutants (ledgers/S7/mutants/koning-r35/) are killed 5 of 5. The page quotes no round-24 Koning digit "
    "(T35-koning-quoted-digits).",
    "Re-run in round 35 (exact outputs in the rows): run_labs --unit S7 (42/42; L01 4/4; L02 3/3), check_pages, check_dag, check_projects "
    "(S7 PASS), page_smoke --unit S7 --pages L01 L02 (PASS), verify_refs --unit S7 --workers 1 live (94 of 560 entries, 0 problems), "
    "verify_refs --offline (560 entries, 0 problems), ruff check . and ruff format --check . (pass), mypy (102 files, pass), pytest on "
    "tests/test_koning_spot.py tests/test_figure_kernels.py tests/test_docs_figures.py (49 passed).",
    "Carry rule: 432 rows carried by git diff --quiet e6d10ab HEAD (prefix 'Carried from round 34 (...) byte-identical since e6d10ab'). "
    "Rows whose subject includes course/modules/S/S7/L01.html use the line-level variant, which holds because the only change to that file "
    "is line 133 (git diff -U0 gives @@ -133 +133 @@); the builder refuses to carry any such row whose location or evidence cites line 133, the "
    "section 3 figure or the removed phrase. Those rows are re-derived. Whole-page text scans (banned strings, question marks, decimals, "
    "structure, numeric recompute) are re-run as differentials (T35-visible-text-diff, T35-prose-differential, T35-decimal-differential, "
    "T35-recompute-47, T35-structure-checks), so the line-level carries are backed by an explicit check of the one changed line.",
    "Decided (architect): the 70 carried rows that cite vanished round-33/34 scratch scripts stay carried on byte-identity of their "
    "subjects. From round 35 on, scripts that back a row are archived in the repository: ledgers/S7/scripts/L01-L02-r35/ (this round) and "
    "ledgers/S7/scripts/L01-L02-r33r34/ (the earlier archive). The round-34 rows that cited /tmp scripts (L01-cmd-m1-m4, L01-cmd-m5, "
    "L02-cmd-m3-example42) are re-run from the archived copies.",
    "Quiz item 10 (line 768): 'losing money about half the time' is backed by Lab 2's printed share 0.52 (T35-quiz10-about-half); "
    "not a banned phrase, not a free number.",
    "Judgment calls for the architect to confirm: (1) the caption sentence is ruled 1.2(c) on the strength of the two displayed formulas, "
    "not a printed calculation; (2) claim 1 of Koning is checked for three first-crossing rules within 6 SE, as the ruling asked, and the "
    "general claim rests on the analytic row L01-math-koning-theorem1-proof-a2a631a; (3) the 360 px caption check relies on page_smoke's "
    "horizontal-scroll and geometry checks, not on a screenshot of the caption.",
]
