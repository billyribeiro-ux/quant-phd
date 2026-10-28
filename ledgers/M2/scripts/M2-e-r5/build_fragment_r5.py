"""Builds ledgers/M2/M2-e.json (round 5, slice M2-e) from the verifier's findings.

Run from the checkout root: .venv/bin/python ledgers/M2/scripts/M2-e-r5/build_fragment_r5.py
Every row names the command, test, lab output or file read that backs it (see run_r5.sh and the other files here).
"""
import json
import re
from pathlib import Path

ROOT = Path(".")
OUT = ROOT / "ledgers/M2/M2-e.json"
MUT_LOG = ROOT / "ledgers/M2/scripts/M2-e-r5/outputs/mutate_71_seeds0-49.txt"

P = "PASS"
F = "FAIL"
U = "UNVERIFIABLE"

carried_note = ""
rows = []


def row(rid, check, location, status, evidence, fix=None):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != P:
        r["fix"] = fix or ""
    rows.append(r)


# ---- rows from round 4, re-decided this round (every subject re-read or re-run) ----
row("m2e-lab1-numbers", "Rung 1 lab: hypothesis numbers, twin, output, recomputation",
    "project.html Lab 1 (lines 55-117); tests/labs/M2/lab-M2-project-1.py",
    P, "python -I -W error tests/labs/M2/lab-M2-project-1.py stdout equals the embedded expected block (run this round); "
       "hypothesis figures recomputed: 1081108.96 and 1081109; 1.56e-02/8514667.40 = 1.83e-9; 8.36/83766485.12 = 9.98e-8; "
       "duration 7.875864 -> 7.88 (ledgers/M2/scripts/M2-e-r5/twin_and_alt_runs.py output: twin project-1 stdout equals the embedded block)")
row("m2e-lab2-completion", "Rung 2 completion: blanks, twin output and claims",
    "project.html Lab 2 (lines 119-196); tests/labs/M2/lab-M2-project-2.py",
    P, "twin stdout equals embedded expected block; printed differences 5.11e-08 (< 1e-7 claimed) and 4.44e-16 (< 1e-15 claimed) match the claims in the hypothesis")
row("m2e-lab3-numbers", "Note's reference lab: hypothesis numbers, twin, output",
    "project.html Lab 3 (lines 268-376); tests/labs/M2/lab-M2-project-3.py",
    P, "twin stdout equals embedded expected block; 2721581.29, -23407826.81 (-23407826.805475), min central error 7.111207e-04 at 1e-06, orders 0.984 and 2.000, kink +1/-1/0, cancellation rows all recomputed")
row("m2e-lab3-report-lines", "Rung 3 instruction: report/run_report.py prints the same lines as Lab 3",
    "project.html Rung 3 'Required outputs' and Lab 3 hypothesis; ledgers/M2/scripts/M2-e-r5/report_sim/run_report.py",
    P, "no student report/run_report.py exists in the checkout; a replica built by the page's three replacements (difference->fd_derivative, exact->sensitivities(instance)['dprice_dy'], backward kink line -> fd_derivative(f, x-h, h, 'forward'), price function kept) printed lines identical to the Lab 3 expected block (diff, report_sim/run_report.out vs expected3_clean.txt)")
row("m2e-one-bond-claim", "Rungs 1-2 text: which lab uses which bond",
    "project.html 'Rungs 1 and 2' paragraph (line 53); tests/labs/M2/lab-M2-project-1.py line 77, -3.py line 301",
    P, "Lab 1 face_cents = 1_000_000 (10000.00); Lab 3 face_cents = 2_500_000 (25000.00); Lab 2 cubic (1,-2,3,0.5); text matches")
row("m2e-hess-tolerance-wording", "Conventions 'Tolerances' vs grader Hessian tests",
    "project.html Conventions 'Tolerances' item; grader/test_project.py test_hessian_matches_the_analytic_hessian (1e-4), test_hessian_positive_step_is_accepted",
    P, "grader lines 439-450 use step 1e-4 and tolerance 1e-5; lines 521-532 accept steps 1e-4, 1e-3, 1.0; page says 'step 1e-4' and 'from 1e-4 to 1'")
row("m2e-rubric-c1-vague-level4", "Rubric C1 level 4 is observable and matches the exemplars",
    "project.html rubric row C1 (line 400)", P, "level 4 names a derived 1/h floating-point term and the step below which the printed central error rises; both are checkable against Lab 3 rows (1e-06 minimum, 1e-07 onward rising)")
row("m2e-exemplar-b-C3-calibration", "Exemplar B scores and annotations",
    "project.html #exemplar-b (lines 464-527)", P, "official scoring C1 4, C2 4, C3 2, C4 3, C5 4 equals data-scores 4,4,2,3,4; each annotation's level matches the rubric cell text (C1 level 3 and 4, C3 level 2 with 'Misses level 3', C4 level 3 with 'Misses level 4')")
row("m2e-exemplar-a-C3-annotation", "Exemplar A scores and annotations",
    "project.html #exemplar-a (lines 412-462)", P, "official scoring C1 2, C2 1, C3 2, C4 2, C5 2 equals data-scores 2,1,2,2,2; annotations match the rubric cells")
row("m2e-richardson-claim", "'What the suite does not check' names alternatives the suite accepts",
    "project.html section 'What the suite does not check' (line 230); ledgers/M2/scripts/M2-e-r5/alts/",
    P, "named alternatives run on seeds 0-49 against the current grader: alt_a (Richardson central quotient, complex-step ad_derivative, exact Fraction price) 80/80 passed each seed; alt_b (reverse-mode tape ad_derivative, NumPy vector sums) 80/80; alt_c (five-point stencil, Decimal rounding) 80/80 after the precision fix")
row("m2e-forward-value-untested", "Forward estimate value is tested",
    "grader/test_project.py test_forward_estimate_is_the_forward_quotient (lines 187-198)",
    P, "the test expects f'(x) + h f''(x)/2 + h^2 p3 at h = 1e-3 to 1e-6; mutants m11 (backward difference) and m12 (double step) killed at seed 0")
row("m2e-mutants-existing-suite", "Every mutant that existed before this round is killed by the current suite",
    "ledgers/M2/mutants/ (68 files before this round); tools/mutate_graders.py --unit M2 --seeds 0-49",
    P, "run this round (outputs/mutate_68_seeds0-49.txt): 68/68 KILLED; the same run with the three new mutants (outputs/mutate_71_seeds0-49.txt) kills 70/71, the survivor is v01 (row m2e-v01-ad-fd-imposter-survives)")
row("m2e-mutants-own-killed", "Verifier-written student-error mutants x01-x14 are killed",
    "ledgers/M2/mutants/x01..x14", P, "mutate_graders run (outputs/mutate_71_seeds0-49.txt): all 14 KILLED")
row("m2e-mutants-own-survivors", "Previously surviving mutants m11 and m12 are killed",
    "ledgers/M2/mutants/m11_*.py, m12_*.py", P, "outputs/mutate_71_seeds0-49.txt: m11 killed by test_forward_estimate_is_the_forward_quotient[inst0]; m12 killed by the same test")
row("m2e-alt-impls-pass", "Alternative correct implementations pass 50 seeds",
    "ledgers/M2/scripts/M2-e-r5/alts/alt_a..alt_c vs course/modules/M/M2/grader/test_project.py",
    P, "the three implementations this round: 80 passed on every seed 0-49 (alt_c failed on seeds 0-49 only through an InvalidOperation in Decimal with the default 28-digit context, a defect of the alternative; fixed by prec 800, then 80/80)")
row("m2e-alt-richardson-fails", "Richardson alternative passes the order test",
    "alt_a_richardson_complexstep.py vs test_central_error_is_at_least_of_order_h_squared", P,
    "alt_a passes all 80 tests on seeds 0-49, including the central order test (its error ratio is about 16, above the 3.8 bound)")
row("m2e-mutants-existing-suite-old", "reference.py passes every test",
    "course/modules/M/M2/grader/reference.py", P, "tools/run_graders.py --unit M2 --seeds 0-49: 'run_graders M2: PASS (reference 50/50 seeds)'; pytest on seeds 0, 17, 49: 80 passed")
row("m2e-instances", "instance.py ranges and validity match its docstring",
    "course/modules/M/M2/grader/instance.py", P,
    "the 50 instances for seeds 0-49 are all distinct (quick_checks.py section 7); maturity 1-30, face 1000000-50000000 cents, coupon 0-1000 bps, yield 100-1500 bps, as the docstring says; x0 in [0.25,1.75]")
row("m2e-starter-fails", "The suite fails on the starter",
    "course/modules/M/M2/grader/starter.py", P, "starter copied as sensitivity_engine.py: pytest reports 80 failed (NotImplementedError); the wording defect is row m2e-starter-numpy-wording")
row("m2e-test-count", "Test count on the page equals the real collect-only count",
    "project.html 'Grading mode' ('runs 80 tests'); grader/test_project.py", P, "pytest --collect-only: 80 tests collected (run this round)")
row("m2e-tolerances-match-code", "Stated tolerances equal the code's tolerances",
    "project.html Conventions 'Tolerances' vs grader/test_project.py", P,
    "1e-6 central cubic at 1e-5 (line 151); 1e-9 forward-mode (353); 1e-5 Hessian (447); 1e-6 forward quotient at 1e-3 (195); 1e-6 symmetry (459); 1e-6 dprice_dy at 1e-5 (607); 1e-4 d2price at 1e-5 (620); 1e-9 ratios (631, 635); order steps 1e-2 and 5e-3 (164, 211); all as stated")
row("m2e-order-ratio-bounds", "Order-check bounds are not over-constraining",
    "grader/test_project.py forward and central order tests (lines 156-216)", P,
    "computed this round over seeds 0-49 (both instances): forward error ratio in [1.98784, 2.00820] (bounds 1.9-2.1); central ratio for sin in [3.9999849, 3.9999851] (bound 3.8); a five-point stencil (ratio about 16) and Richardson pass")
row("m2e-valueerror-conditions", "The ValueError conditions are exactly those the page names, both directions",
    "grader/test_project.py ValueError tests; project.html Constraints and Conventions (a)-(c)", P,
    "tests cover 0, -0.0, -1e-300, NaN, -inf for fd and hessian; schemes ''/' central'/'backward'/None/1; yield -10000, -10001, -20000 refused and -9999 accepted; no ValueError test for other inputs")
row("m2e-messages-no-leak", "Failure messages do not print the expected value",
    "grader/test_project.py require/must_raise/must_accept (lines 44-73) and all assertion messages", P,
    "read every message: each names a property and a hint; none formats a computed expected value")
row("m2e-pyodide", "Suite runs in the browser within limits",
    "tools/page_smoke.py --unit M2 --pages project.html --skip-sweep", P,
    "run this round: 'page_smoke M2: PASS' (outputs/page_smoke_project.txt); the suite runs in 0.03 s locally on seed 0")
row("m2e-timeout-120s", "'A run in your browser stops after 120 seconds'",
    "course/assets/js/python.js line 4", P, "line 4: const TIMEOUT_MS = 120000; file byte-identical to the previous pin (git diff --quiet)")
row("m2e-hours", "Hours: hub split, time-budget table, lesson hours",
    "project.html Time budget (lines 236-246); course/modules/M/M2/index.html data-hours; L01-L24 'study hours'", P,
    "hub data-hours-lessons=240 and data-hours-project=60 (sum 300); all 24 lessons declare 10 study hours (sum 240); project table 4+6+22+6+14+8 = 60 equals data-hours-project; no arithmetic inconsistency (pace not judged, per architect ruling)")
row("m2e-rubric-banned-words", "Banned phrases and omissions in the rubric and project text",
    "project.html full text; cards.json", P,
    "quick_checks.py section 2 searches project.html text and cards for roughly half, about 6%, historically, studies show, well known, important to note, beyond the scope, left as an exercise, typically, in practice, TODO, TBD, lorem, for brevity, roughly, build, builder, verifier, unit report: no hit")
row("m2e-exemplar-a-blind", "Exemplars: annotations and verdicts hidden until the reveal",
    "project.html #exemplar-a, #exemplar-b; course/assets/js/rubric.js setRevealed", P,
    "Chromium via playwright (ledgers/M2/scripts/M2-e-r5/reveal_check.py): before the reveal every .annotation and [data-reveal] of both exemplars is hidden (9 annotation blocks, 2 verdicts); after clicking 'Reveal the official scoring' all are visible; no page errors")
row("m2e-exemplar-level-overlap", "Rubric levels distinguish exemplar A's C4 descriptors",
    "project.html rubric row C4 (line 403)", P, "level 1 cell 'Gives no order for either scheme.' and level 2 cell 'states them with no derivation' are distinct; exemplar A's C4 text states orders without derivation, scored 2")
row("m2e-dag", "Links and concepts used by the project are in the prerequisite closure",
    "tools/check_dag.py --unit M2; project.html data-concept links", P,
    "check_dag M2 PASS (run this round); the only concept links are hessian (L19 #def-hessian) and finite-difference-derivative (L13 #def-finite-difference-derivative), both M2's own, both anchors exist; duration, convexity, Richardson, reverse-mode are prose-only (plan Q8)")
row("m2e-references", "References: keys and reading statements",
    "project.html #reading and #references; references/references.json entries spivak2008calculus, hubbard2015vector", P,
    "both keys exist with status verified, used_by ['M2'], Open Library records; the page attributes no statement and gives no locator; tools/verify_refs.py --unit M2 live: 2 of 560 entries re-verified, 0 problems; --offline: 560 entries, 0 problems")
row("m2e-lint", "ruff check and format on grader and labs; strict typing",
    "course/modules/M/M2/grader; tests/labs/M2/lab-M2-project-*.py", P,
    "ruff check: All checks passed; ruff format --check: 31 files already formatted; mypy --strict --ignore-missing-imports on the grader workspace: no issues (ledgers/M2/scripts/M2-e-r5/outputs); labs: no mypy errors")
row("m2e-run-labs", "All M2 labs run and match their expected output",
    "tools/run_labs.py --unit M2", P, "run_labs M2: PASS (27/27) (outputs/run_labs.txt)")
row("m2e-cards-count-coverage", "cards.json covers L01-L24 and counts",
    "course/modules/M/M2/cards.json", P,
    "377 cards (round 4 counted 376; M2-c378 added); every lesson L01-L24 has 11-22 cards; id M2-c164 is absent from the sequence (numbering gap, no card missing from a lesson)")
row("m2e-cards-numbers-in-lesson", "Every number on a card appears in its lesson or in the lab output the lesson prints",
    "course/modules/M/M2/cards.json vs course/modules/M/M2/L01..L24.html", P,
    "each card read against its lesson text (ledgers/M2/scripts/M2-e-r5/showcards.py, showlesson.py); numbers recomputed where a card gives a value (see m2e-cards-numeric-rederive); no card number absent from its lesson")
row("m2e-cards-dup-scan", "Duplicate scan of cards",
    "course/modules/M/M2/cards.json", P, "no duplicate ids; no duplicate fronts or backs (case-insensitive); two near-identical back prefixes 'Hypotheses: ...' belong to different theorems")
row("m2e-cards-numeric-rederive", "Numbers on the changed cards re-derived",
    "cards.json changed set: M2-c066, c131, c137, c163, c258, c262, c264, c291, c298, c334, c340, c375, c378 and c188-c190, c193, c370", P,
    "c131: 1/3 - L_n = (3n-1)/(6n^2); c137 bounds; c298 5/3 with the two inner integrals; c370: 2 sqrt(delta/e) = 1.808e-8 and (3 delta/e)^(1/3) = 6.258e-6 with delta = 2^-52; c188 (0.0135914, 0.0137280), c189 (4.4854e-5, 4.5760e-5), c190 (9.990, 10.101), c193 (98.91, 101.11) recomputed")
row("m2e-cards-grade-C-basis", "Grade-C cards name their basis",
    "cards.json grade C entries", P, "77 cards graded C, every one has a non-empty basis; no non-C card has a basis field (checked by script)")
row("m2e-cards-unchanged-322", "Every card agrees with the CURRENT lesson text",
    "cards.json (all 377) vs course/modules/M/M2/L01..L24.html", P,
    "every lesson was read in full (plain-text extraction, ledgers/M2/scripts/M2-e-r5/totext.py) and every card was compared with its lesson; defects found are separate rows: m2e-cards-c129-front-wording, m2e-cards-c267-proof-description, m2e-cards-c303-reason, m2e-cards-c307-domain")
row("m2e-cards-T-hypotheses-c131", "T card M2-c131 (L09): statement and hypotheses",
    "cards.json M2-c131; L09 Example 3.2 and Section 4", P, "statement equals Example 3.2: L_n = (n-1)(2n-1)/(6n^2) and 1/3 - L_n = (3n-1)/(6n^2) > 0; the front 'lower sums ... equal 1/3 at any finite n' matches")
row("m2e-cards-T-hypotheses-c205", "T card M2-c205 (L14 Proposition 3.1): hypotheses",
    "cards.json M2-c205; L14 Assumption 1 and Proposition 3.1", P, "card lists the denominator, differentiability and Assumption 1 hypotheses, as Proposition 3.1 states them")
row("m2e-cards-T-needed-c319", "T card M2-c319 (L21): 'sufficient, not necessary'",
    "cards.json M2-c319; L21 Section 3 (F = y^3 - x example)", P, "F = y^3 - x at the origin has F_y = 0 and the zero set y = x^(1/3) over R (Section 3); the card says F_y not 0 is sufficient, not necessary")
row("m2e-cards-T-needed-c292", "T card M2-c292 (L19 Theorem 2.1 and example): hypotheses and example values",
    "cards.json M2-c292; L19 Theorem 2.1 and Example 2.2", P, "f_xy(0,0) = -1 and f_yx(0,0) = 1 re-derived from f(x,0)-type quotients (f_x(0,y) = -y, f_y(x,0) = x)")
row("m2e-cards-lab-as-T-c294", "Lab-derived card M2-c294 carries grade C and basis",
    "cards.json M2-c294; L19 Lab 1", P, "grade C with basis 'Lab 1, one run at step 1e-5 (L19)'")
row("m2e-cards-lab-as-T-c371", "Card M2-c371 'a smaller step always better' is graded as lab-derived",
    "cards.json M2-c371; L24 Lab 1 Part B, Misconception 1", P, "grade C with basis; values 6.603e-09 and 2.154e-07 are the printed rows")
row("m2e-cards-c370-notation", "Card M2-c370 M_3 wording",
    "cards.json M2-c370; L24 Proposition 4.3 and prediction text", P, "wording 'M_3 approximately e ... on a small interval about 1' agrees with Proposition 4.3; numbers 1.8e-8 and 6.3e-6 re-derived")
row("m2e-lesson-L19-theorem-proof", "L19 proof and L11 integration-by-parts lines",
    "L19 Theorem 3.1 proof; L11 Theorem 2.1 proof", P,
    "L19 proof: MVT on phi on [0,1] then on phi' on [0,s1] gives phi(1) = s1 phi''(s2); |h^T M h| <= 2|h|^2 max|M_ij| since (|h1|+|h2|)^2 <= 2|h|^2; conclusion |R| <= 2|h|^2 omega is what the proof yields. L11: F=uv differentiable, F'=u'v+uv' integrable, Theorem 2.1 of L10 applies, linearity splits the integral; no gap found")
row("m2e-project-lede", "Project lede",
    "project.html lede (lines 34-37)", P, "lede claims (bond price in cents at first and second order; three methods; Hessian; note on accuracy) match the Rung 3 specification and the module list")
row("m2e-scope-words", "Scope words (only, all, always, every, any, same, drives) have a computation or hypothesis",
    "project.html (text, grep this round); Conventions (a); Constraints; 'What the suite does not check'", P,
    "the 'any size' claim of round 4 is gone: Constraints and Conventions (a) now say 'at the sizes the suite tests, from 1e-300 to 1e6' (grader test_very_small_positive_step_is_accepted and test_large_positive_step_is_accepted cover both ends); every remaining 'every'/'all'/'same' sentence is a stated definition, a printed computation or a derivation on the page")
row("m2e-cards-changed-restated-PASS", "Changed cards agree with the current lesson text",
    "cards.json changed set (M2-c066, c131, c137, c163, c258, c262, c264, c291, c298, c334, c340, c375, c378)", P,
    "each changed card compared with the current lesson text (L06, L09, L10, L11, L17, L19, L20, L22, L23, L24); all agree with their lessons; the FAIL cards of this round (c129, c267, c303, c307) are not in the changed set")
row("m2e-cards-changed-c370-PASS-numbers", "Numbers on card M2-c370 re-derived",
    "cards.json M2-c370", P, "delta = 2^-52 = 2.220446e-16; 2 sqrt(delta/e) = 1.8076e-8; (3 delta/e)^(1/3) = 6.2578e-6")
row("m2e-proj-numbers-recomputed", "Numbers in project.html labs and exemplars recomputed",
    "project.html Labs 1-3 and exemplars A and B", P,
    "Exemplar B: 1e-6 relative tolerance check 7.111207e-04/23407826.805 = 3.0e-11; spacing 2^-31 = 4.66e-10; 2^-26 = 1.49e-8; 2h/2^-26 = 1.34; 1/(2h) = 5e11; Exemplar A: -23407827 from -23407826.805; Lab 1 rung figures; all agree")
row("m2e-purity-forward-survivor", "Purity test covers the forward branch (round-3 survivor g01)",
    "grader/test_project.py test_module_prints_nothing_and_warns_nothing; ledgers/M2/mutants/g01", P, "g01 killed by test_module_prints_nothing_and_warns_nothing (seed 0)")
row("m2e-mutants-r3-killed", "Round-3 mutants g02, g03, g04 killed",
    "ledgers/M2/mutants/g02-g04", P, "all three KILLED in outputs/mutate_71_seeds0-49.txt")
row("m2e-alt-numerical-cutoff", "Different numerical cutoffs and valid algorithms are not over-constrained",
    "ledgers/M2/scripts/M2-e-r5/alts/alt_c_five_point_decimal_cutoffs.py", P,
    "alt_c uses h <= 0 and NaN refusal via math.isnan, a five-point central stencil, half-even rounding through Decimal, and yield checks with < and == on basis points; 80/80 on seeds 0-49")
row("m2e-mutants-new-killed", "Round-4 mutants m18 and m19 are killed",
    "ledgers/M2/mutants/m18_*.py, m19_*.py", P, "both KILLED in outputs/mutate_71_seeds0-49.txt")
row("m2e-negative-infinity-tests", "New negative-infinity refusal tests",
    "grader/test_project.py test_negative_infinite_step_raises_value_error and test_hessian_negative_infinite_step_raises_value_error", P,
    "x05 and x06 killed by these tests (outputs/mutate_71_seeds0-49.txt)")
row("m2e-scheme-type-refusal", "Non-string scheme refusal test",
    "grader/test_project.py test_scheme_that_is_not_a_name_raises_value_error[None, 1]", P, "x07 (None treated as central) killed by test_scheme_that_is_not_a_name_raises_value_error[None]")
row("m2e-purity-covers-every-function", "Purity test covers every function and branch the page names",
    "grader/test_project.py test_module_prints_nothing_and_warns_nothing (12-call list)", P,
    "the list calls fd_derivative (central, forward, zero step, unknown scheme), ad_derivative (non-constant, constant), hessian_fd (step, zero step), bond_price_cents and sensitivities (both at the refused yield), so all five functions and every refusal branch are covered; x11 and x12 killed")
row("m2e-mutants-ledger-count", "Mutant ledger count",
    "ledgers/M2/mutants (71 files)", P,
    "71 files: e01-e11, f01-f10, g01-g04, m01-m19, x01-x14, s01-s10 (68 from earlier rounds) and v01-v03 (this round); 70 killed, v01 survives (row m2e-v01-ad-fd-imposter-survives)")
row("m2e-fd-any-size-untested", "The 'any size' claim is enforced by the suite, or removed",
    "project.html Constraints and Conventions (a); grader/test_project.py test_large_positive_step_is_accepted", P,
    "claim removed from both places; the suite tests 1, 5 and 1e6 and mutant m17 (refuses steps above ten) is now KILLED at seed 0")
row("m2e-hessian-step-range", "Hessian step sizes the suite accepts, as stated on the page",
    "project.html Constraints and Conventions (a); grader/test_project.py test_hessian_positive_step_is_accepted", P,
    "page now says 1e-4 to 1; the test uses 1e-4, 1e-3, 1.0; mutant m18 (refuses step of one or more) killed")
row("m2e-ladder", "Ladder: four rungs in order with working links",
    "project.html section 'The ladder' (lines 40-49) and every link in the page", P,
    "all 25 hrefs resolve (quick_checks.py section 1): #placement exists in index.html, #spec, #grader-section, #report, #stretch, #brief, #self-assessment, #conventions exist; grader/starter.py exists; the rung descriptions match the sections")

# ---- new rows: defects found this round ----
row("m2e-starter-numpy-wording", "starter.py docstring agrees with the page's Constraints",
    "course/modules/M/M2/grader/starter.py line 9 ('Use the standard library only.') vs project.html Constraints ('The standard library, or NumPy, only.')",
    F, "read both: the starter (linked from 'Start from the starter file') says standard library only; the page allows NumPy; the page is the specification and the test file imports no NumPy restriction",
    "change starter.py line 9 to 'The standard library, or NumPy, only.' (grader file; a builder fix, not done here)")
row("m2e-binding-conventions-vs-accepted-alternatives", "Binding conventions do not contradict the alternatives the suite accepts",
    "project.html Constraints ('The conventions ... are binding'), Conventions 'Forward and central differences' (central estimate 'is the central quotient'), 'Hessian' (the diagonal and mixed formulas), 'Automatic differentiation' (a dual number); 'What the suite does not check' (line 230)",
    F, "ledgers/M2/scripts/M2-e-r5/alts/alt_a: its central estimate is a Richardson combination, its Hessian is Richardson-extrapolated, and its ad_derivative is complex-step; alt_b's ad_derivative is reverse-mode. All 80 tests pass on seeds 0-49 for each, while the page says the conventions are binding and that a dual number is the carrier",
    "state the conventions as the reference choice and say that any estimate meeting the stated value and order properties is accepted, or drop 'binding' for these items (page edit, not made here)")
row("m2e-v01-ad-fd-imposter-survives", "The suite kills an ad_derivative that is a finite difference, not dual-number forward mode",
    "ledgers/M2/mutants/v01_ad_derivative_is_a_central_difference_not_dual.py; project.html Conventions 'Automatic differentiation' ('carries a value and a derivative together, a dual number'); grader/test_project.py forward-mode tests",
    F, "mutate_graders M2 (outputs/mutate_71_seeds0-49.txt): SURVIVED on all 50 seeds (twin_and_alt_runs.py: v01 suite failing seeds none); v01 agrees with the derivative to 1e-9 on the cubic test points because h = 1e-6 is small. Probe ledgers/M2/scripts/M2-e-r5/probe/extra_test.py and twin_and_alt_runs.py: ad_derivative(x*x*x, 1e5) = 29999875000 for v01 (rel. error 4e-6) versus 3e10 for the reference and alt_a/alt_b/alt_c",
    "add a test: ad_derivative(lambda x: x*x*x, 1e5) within 1e-9 of 3e10 (ledgers/M2/scripts/M2-e-r5/probe/test_probe_addition.py): it kills v01 (1 failed) and passes reference, alt_a, alt_b, alt_c (1 passed each); not applied here")
row("m2e-cards-c129-front-wording", "Card M2-c129 front and back agree with the L09 misconception",
    "cards.json M2-c129; course/modules/M/M2/L09.html Misconception 2 and Lemma 1.2 / Definition 1.3",
    F, "front 'Do the left and right endpoint sums on the same side always bracket the integral?' garbles the misconception ('The left and right endpoint sums always bracket the integral'); back attributes the bracket 'in Lemma 1.2' whereas the bracket L <= integral <= U is Definition 1.3 (Lemma 1.2 gives L(P) <= U(Q) only)",
    "front: 'Do the left and right endpoint sums always bracket the integral?'; back: 'the bracket in Definition 1.3 uses suprema and infima' (cards.json edit, not made here)")
row("m2e-cards-c267-proof-description", "Card M2-c267 back describes the proof of Proposition 3.2 correctly",
    "cards.json M2-c267; course/modules/M/M2/L18.html Proposition 3.2 proof",
    F, "back: 'The uniqueness proof takes the triangle inequality for two candidate arrays along a unit vector v.' The proof takes h = t e_j, multiplies by the i-th component and reads off the partial derivative; no two candidate arrays and no unit vector v appear",
    "replace the second sentence with: 'The proof takes h = t e_j and reads the i-th component.' (cards.json edit, not made here)")
row("m2e-cards-c303-reason", "Card M2-c303 gives the reason the lesson gives",
    "cards.json M2-c303; course/modules/M/M2/L20.html Example 3.1 ('The page does not check the hypothesis of Definition 1.1 ... which is stated for a closed rectangle')",
    F, "back: 'The integrand is unbounded near the origin, so Definition 1.1 does not cover it.' The lesson's stated reason is that Definition 1.1 is stated for a closed rectangle and (0,1]^2 is not one; the page explicitly makes no claim about existence rather than asserting non-coverage by unboundedness",
    "back: 'No. Example 3.1 uses (0,1]^2, not a closed rectangle as Definition 1.1 requires, so the page makes no claim that the double integral exists.' (cards.json edit, not made here)")
row("m2e-cards-c307-domain", "Card M2-c307 agrees with the L20 'A rectangle is not enough' bullet",
    "cards.json M2-c307; course/modules/M/M2/L20.html Section 3 ('A rectangle is not enough')",
    F, "back: 'The domain is a rectangle, so the failure is in the integrand.' The lesson says the opposite emphasis: 'A rectangle is not enough. Example 3.1 uses the rectangle (0,1]^2, and its integrand is unbounded near the corner at the origin, which is not in that set.'",
    "back: 'No. (0,1]^2 is a half-open rectangle, outside Definition 1.1, and its integrand is unbounded at the origin (Section 3).' (cards.json edit, not made here)")

# ---- mutants ----
mutants = []
pat = re.compile(r"^(KILLED|SURVIVED) (\S+?): (.*?) -> (.*)$")
for line in MUT_LOG.read_text(encoding="utf-8").splitlines():
    m = pat.match(line)
    if not m:
        continue
    status, fname, desc, killed = m.groups()
    mutants.append({"file": fname, "description": desc,
                    "killed_by": None if status == "SURVIVED" else killed.strip()})

ROWS_OK = len(rows)
fragment = {
    "unit": "M2",
    "slice": "M2-e",
    "round": 5,
    "verifier": "Claude Haiku 5.5 (independent verifier, round 5; did not build M2; no shared context with builders)",
    "pin": "09b8751 (detached worktree /tmp/verifyB5-M2-e)",
    "previous_ledger": "2657ab5 (round 4 pin; fragment /tmp/fanout-frags/B-M2-e.round4.json)",
    "base": "2657ab5 (round 4 pin). Slice files changed since then: project.html, cards.json, grader/test_project.py, and the new mutants v01-v03 (ledgers/M2/mutants). grader/reference.py, instance.py, starter.py and project labs 1-3 are byte-identical.",
    "checkout": "/tmp/verifyB5-M2-e",
    "scratch": "/tmp/M2-v/M2-e-r5",
    "verified_at": "2026-10-28",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Scripts: ledgers/M2/scripts/M2-e-r5/ (run_r5.sh lists the commands; build_fragment_r5.py builds this file; alts/, probe/, report_sim/, outputs/).",
        "Cards: 377 entries read against the current lesson text of L01-L24 (every lesson read in full as plain text).",
        "Carried rows: none. Every round-4 row was re-decided this round from a fresh check (no byte-identical carry was needed).",
        "Not checked: the browser autograder panel beyond page_smoke (Pyodide run not re-run in a browser); the Lab 3 report file is absent in the checkout, so run_report was replicated from the page's instruction; bibliographic data of Spivak and Hubbard was not read from the books (no locators are claimed); the card id M2-c164 is absent (numbering gap only).",
        "No git commit or push. Edits: none to course, tool, test, reference, curriculum or atlas files.",
    ],
}
counts = {"PASS": 0, "FAIL": 0, "UNVERIFIABLE": 0}
for r in rows:
    counts[r["status"]] += 1
fragment["summary"] = {"rows": len(rows), "PASS": counts["PASS"], "FAIL": counts["FAIL"],
                       "UNVERIFIABLE": counts["UNVERIFIABLE"], "mutants": len(mutants),
                       "mutants_killed": sum(1 for m in mutants if m["killed_by"])}
OUT.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", OUT, fragment["summary"])
