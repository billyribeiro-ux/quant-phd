"""Writes the round-8 verifier fragment for M2 slice d2 (L22, L23, L24 and their lab twins) to ledgers/M2/M2-d2.json.

Run from the checkout root: .venv/bin/python -I ledgers/M2/scripts/M2-d2-r8/make_fragment_r8.py
Every row's evidence cites a script or command output kept under ledgers/M2/scripts/M2-d2-r8/.
"""

import json
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
S = "ledgers/M2/scripts/M2-d2-r8/"

FAIL_XHAT = (
    "Sentence states as a fact that the printed x-hat is off by between 1e-8 and 2e-8 at the four printed values of a. "
    "The unrounded location errors computed from the twin's own maximizer_a (" + S + "l22_xhat.out) are +1.366e-8 at a=1.5, "
    "+7.059e-9 at a=2, -7.235e-9 at a=3 and -2.174e-8 at a=4. The 1e-8 floor is the displayed-digit reading (0.50000001, "
    "1.00000001, 1.99999999), not the true error: at a=2 and a=3 the true deviation is 0.71e-8 and 0.72e-8, below 1e-8."
)
FIX_XHAT = (
    "Rewrite the sentence on L22.html:231 to separate the two readings, e.g. 'At the displayed eight decimals the printed x-hat "
    "differs from the exact maximizer by 1e-8 at a = 1.5, 2 and 3, and by 2e-8 at a = 4. The unrounded errors, which the lab does "
    "not print, are 1.37e-8, 0.71e-8, 0.72e-8 and 2.17e-8.' Lines 279 and 342 ('about 10^-8') already agree with the true values "
    "and need no change."
)


def row(rid, check, location, status, evidence, fix=None):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    return r


rows = [
    row("G-check-pages", "2.9 structure: tools/check_pages.py --unit M2 --page L22/L23/L24",
        "course/modules/M/M2/L22.html, L23.html, L24.html", "PASS",
        S + "gates_pages_dag.out: 'check_pages M2 L22: PASS', 'L23: PASS', 'L24: PASS' (rc 0 each); unit-wide 'check_pages M2: PASS'."),
    row("G-check-dag", "2.9 DAG: tools/check_dag.py --unit M2", "course/modules/M/M2/L22.html..L24.html", "PASS",
        S + "gates_pages_dag.out: 'check_dag M2: PASS' rc 0 (unit-wide)."),
    row("G-run-labs", "2.5 labs: tools/run_labs.py --unit M2 --page L22/L23/L24",
        "tests/labs/M2/lab-M2-L22-1.py, lab-M2-L23-1.py, lab-M2-L24-1.py", "PASS",
        S + "run_labs.out: 'run_labs M2: PASS (1/1)' for each page, rc 0."),
    row("G-twin-isolated", "2.5 labs: each twin under python -I -W error in an empty scratch cwd",
        "tests/labs/M2/lab-M2-L22-1.py, lab-M2-L23-1.py, lab-M2-L24-1.py", "PASS",
        S + "twin_vs_page.out (script twin_vs_page.py): exit=0 and stderr_len=0 for all three twins; direct re-run of the L22 "
        "twin with -I -W error also exit 0."),
    row("G-page-code-equals-twin", "2.5 labs: embedded code block equals the twin (modulo trailing newline)",
        "course/modules/M/M2/L22.html:100-221, L23.html:91-214, L24.html:137-217", "PASS",
        S + "twin_vs_page.out: 'page code == twin ... True' for L22, L23 and L24."),
    row("G-expected-equals-live", "2.5 labs: expected block equals live stdout, exact text",
        "course/modules/M/M2/L22.html:222-230, L23.html:215-225, L24.html:218-242", "PASS",
        S + "twin_vs_page.out: 'exact stdout == expected block: True' for L22, L23 and L24 (live stdout printed in the same file)."),
    row("G-page-smoke-L22", "2.9 page_smoke, L22 alone", "course/modules/M/M2/L22.html", "PASS",
        S + "page_smoke_r8.out: 'page_smoke modules/M/M2/L22.html: PASS' (command tools/page_smoke.py --unit M2 --pages L22)."),
    row("G-page-smoke-L23", "2.9 page_smoke, L23 alone", "course/modules/M/M2/L23.html", "PASS",
        S + "page_smoke_r8.out: 'page_smoke modules/M/M2/L23.html: PASS'."),
    row("G-page-smoke-L24", "2.9 page_smoke, L24 alone", "course/modules/M/M2/L24.html", "PASS",
        S + "page_smoke_r8.out: 'page_smoke modules/M/M2/L24.html: PASS'."),
    row("G-ruff-mypy-twins", "tooling: ruff check, ruff format --check, mypy --no-incremental on the three twins",
        "tests/labs/M2/lab-M2-L22-1.py, lab-M2-L23-1.py, lab-M2-L24-1.py", "PASS",
        S + "gates_tooling.out: 'All checks passed!', '3 files already formatted', 'Success: no issues found in 3 source files'."),
    row("G-pytest-labs-M2", "tooling: pytest tests/test_labs.py -q -k M2", "tests/test_labs.py", "PASS",
        S + "pytest_labs_M2.out: 27 tests pass, rc 0 (command .venv/bin/python -m pytest tests/test_labs.py -q -k M2)."),
    row("G-verify-refs-offline", "2.1 citations: tools/verify_refs.py --offline (whole registry)", "references/references.json", "PASS",
        S + "gates_refs_pytest_projects.out: 'offline integrity: 560 entries, 0 problems', rc 0. The live --unit M2 run "
        "needs the network and was not run; the slice cites no registry key with a locator, so it is not needed."),
    row("G-links-anchors", "2.9 structure: every internal href and fragment on L22-L24 resolves",
        "course/modules/M/M2/L22.html, L23.html, L24.html", "PASS",
        S + "links_and_scope.out: 'broken internal links or anchors in L22-L24: []' (checked against the id attributes of each target file)."),
    row("G-cards-dup-scan", "2.7 cards: full duplicate scan of cards.json (394 cards)", "course/modules/M/M2/cards.json", "PASS",
        S + "cards_scan.out: 394 cards; no duplicate ids; no duplicate normalized fronts; no duplicate normalized backs; 15 + 24 + 18 "
        "= 57 cards for L22-L24 listed."),
    row("G-notation", "3.2 notation: every macro against notation/notation.json; no registered symbol reused",
        "course/modules/M/M2/L22.html, L23.html, L24.html", "PASS",
        S + "prose_scan.out: L22 uses the registered \\R (4 uses) and no \\mathbb anywhere; L23 and L24 use no registered macro. "
        "The math of the slice contains none of the registered symbols T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f, "
        "\\mathbb{Q} (grep of every inline math block, round-8 command output in prose_scan.out). Local symbols are defined on "
        "their pages: L23 c_1..c_N and N (L23.html:55), L22 J, I (L22.html:55), L22 K and G (L22.html:88), L24 H, M2, M3 "
        "(L24.html:75, 85, 107, 117)."),
    row("N-L22-xhat-error", "2.2 numbers (rule 1): x-hat printed error, displayed digits vs unrounded values, sqrt(eps), 3.3e-17",
        "course/modules/M/M2/L22.html:231 (interpretation), :279 (misconception 3), :342 (E1)", "FAIL",
        FAIL_XHAT, FIX_XHAT),
    row("N-L22-partB-5.4e-12", "2.2 numbers: Part B central differences agree with a/2 to within 5.4e-12; naive partial prints 0",
        "course/modules/M/M2/L22.html:231, card M2-c329", "PASS",
        S + "twin_vs_page.out Part B: errors 1.9e-13, 1.0e-12, 5.4e-12; naive partial 0.00000000 at a = 1, 2, 3; the largest "
        "printed error is 5.4e-12 as the page says."),
    row("N-L22-partA-ln", "2.2 numbers: Part A central differences equal ln a to eight decimals",
        "course/modules/M/M2/L22.html:231, card M2-c328", "PASS",
        S + "twin_vs_page.out Part A: 0.40546511, 0.69314718, 1.09861229, 1.38629436; ln 1.5 = 0.4054651081, ln 2 = 0.6931471806, "
        "ln 3 = 1.0986122887, ln 4 = 1.3862943611 (recomputed by l22_xhat.py, output l22_xhat.out) round to these eight decimals."),
    row("N-L23-price-cents", "2.2 numbers: unrounded price 108110.895779, integer 108111; P'(y0), P''(y0) and their differences",
        "course/modules/M/M2/L23.html:226, expected block :216-219, cards M2-c341..c343, c382", "PASS",
        S + "l23_numbers.out (Fraction closed forms, script l23_numbers.py): P(0.04) = 108110.89577935502, rounds half-even to "
        "108111; P'(0.04) = -851466.7395285615; P''(0.04) = 8376648.51191949. Expected block shows the same digits; "
        "|P' closed - central| = 1.55e-3 (page 1.6e-03) and |P'' closed - central| = 1.90 (page 1.9)."),
    row("N-L23-ratios-and-shifts", "2.2 numbers: first- and second-order errors, ratios 3.9279/7.8807 and 3.9634/7.9396",
        "course/modules/M/M2/L23.html:51, :226, :281; cards M2-c345, c346, c384, c385", "PASS",
        S + "l23_numbers.out: first-order errors 4.037716e+02, 1.027970e+02, 2.593632e+01; second-order -1.506081e+01, "
        "-1.911100e+00, -2.407040e-01; ratios (previous over current) 0.01/0.005 = 3.927854 and 7.880704; 0.005/0.0025 = "
        "3.963438 and 7.939627, printed as 3.9279, 7.8807, 3.9634, 7.9396 (page and expected block agree)."),
    row("N-L23-cents-minus15-plus16", "2.2 numbers: exact minus second-order expansion, whole cents -15 and +16; unrounded -15.06",
        "course/modules/M/M2/L23.html:51, :226, :281; cards M2-c352, c383", "PASS",
        S + "l23_numbers.out: at +0.01 exact 100000.000000, expansion 100015.060810, exact - expansion -15.060810 (rounded -15); "
        "at -0.01 exact 117060.405674 rounds to 117060, expansion 117044.395600, difference +16.010073 (rounded +16)."),
    row("N-L23-E3-offset", "2.2 numbers: float 0.04+0.01 vs 1/20 offset 2.78e-18; P'(0.05); price move -2.1e-12",
        "course/modules/M/M2/L23.html:368 (E3 solution)", "PASS",
        S + "l23_numbers.out: 0.04+0.01 = 0.05 (float), offset from 1/20 = 2.7755575615628915e-18 (page 2.78e-18); P'(0.05) = "
        "-772173.49 (page -7.72e5); offset x P' = -2.14e-12 (page -2.1e-12); unrounded price at the float 0.05 = 100000.0 "
        "(rounds to 100000); exact 1/20 price = 100000."),
    row("N-L23-previews", "2.2 numbers: preview -P'/P = 7.875864 and P''/P = 77.482001 (printed only)",
        "course/modules/M/M2/L23.html:90 (hypothesis), :226", "PASS",
        S + "l23_numbers.out: -P'/P = 7.875864253926185, P''/P = 77.4820007875571; expected block prints 7.875864 and 77.482001."),
    row("N-L23-two-cash-flows", "2.2 numbers: quiz explanation P'(0.04) = -1777.07 for c1 = -1, c2 = 1000",
        "course/modules/M/M2/L23.html:481 (quiz Q8 explanation)", "PASS",
        S + "l23_numbers.out: P'(0.04) = -1777.068161128812, two decimals -1777.07."),
    row("N-L23-M1-M3", "2.2 numbers: M1 price 50/1.05 + 1050/1.05^2 = 1000.000; M3 zero-coupon derivative formula",
        "course/modules/M/M2/L23.html:304 (M1 solution), :318 (M3 solution), quiz :463",
        "PASS", S + "l23_numbers.out: 47.61904761904762 + 952.3809523809524 = 1000.0 (exact); M3 P'(0.04) = -200/1.04^3 "
        "(stated symbolically on the page, no decimal printed)."),
    row("N-L24-remark44-numbers", "2.2 numbers: exact forward error +1.359e-8 at h=1e-8; computed error -6.603e-9",
        "course/modules/M/M2/L24.html:129 (Remark 4.4), :243, card M2-c365", "PASS",
        S + "l24_numbers.out: exact forward error via Decimal at h=1e-8 = +1.3591409e-8; computed signed error (lab formula) = "
        "-6.6027508e-9; l24_numbers.out extra checks: exact forward error at 1e-9 = 1.3591409e-9 (page 1.36e-9)."),
    row("N-L24-E3-unrounded", "2.2 numbers: unrounded central quotient errors 5.858691e-11 (1e-5) and 5.858736e-11 (1e-7)",
        "course/modules/M/M2/L24.html:348 (E3 solution)", "PASS",
        S + "l24_unrounded.out: unrounded errors 5.858691309867936e-11 and 5.8587357187889e-11 (printed to six digits: 5.858691e-11, "
        "5.858736e-11)."),
    row("N-L24-E3-difference", "2.2 numbers (rule 1, unrounded vs displayed digits): the unrounded difference of the two errors",
        "course/modules/M/M2/L24.html:348 (E3 solution), :243", "PASS",
        S + "l24_unrounded.out: unrounded difference = -4.440892098500626e-16, i.e. 4.4e-16 (page now 4.4e-16, the round-7 FAIL "
        "is resolved); equals one ulp of e = 4.440892098500626e-16. The six-digit values differ by 4.5e-16 "
        "(5.858736 - 5.858691), which the page attributes to rounding, correctly."),
    row("N-L24-E3-exact-and-grid", "2.2 numbers: exact central error e(sinh h/h - 1) at 1e-5, 1e-6, 1e-7; grid spacing; 1.3e-11 round-off",
        "course/modules/M/M2/L24.html:348", "PASS",
        S + "l24_unrounded.out and l24_numbers.out: exact central errors 4.5305e-11, 4.5305e-13, 4.5305e-15; grid spacing "
        "ulp(e)/(2h) = 2.22e-11 (1e-5) and 2.22e-9 (1e-7); 5.8587e-11 - 4.5305e-11 = 1.33e-11 (page 'about 1.3e-11')."),
    row("N-L24-minimizers", "2.2 numbers: predicted minimizers 2 sqrt(delta/e) = 1.8e-8 and (3 delta/e)^(1/3) = 6.3e-6",
        "course/modules/M/M2/L24.html:136 (hypothesis), :346-348, card M2-c370", "PASS",
        S + "l24_numbers.out: 2*sqrt(delta/e) = 1.8076e-8; (3*delta/e)^(1/3) = 6.2578e-6, which rounds to 6.3e-6 at two significant "
        "figures; log10 distance of 6.3e-6 to 1e-5 is 0.20 and to 1e-6 is 0.80, so 'closer in logarithm to 1e-5' holds."),
    row("N-L24-E2-roundoff-bound", "2.2 numbers: round-off bound 2 delta/h = 0.444 at h = 1e-15; printed error 0.390",
        "course/modules/M/M2/L24.html:341 (E2 solution), expected block :240", "PASS",
        S + "l24_numbers.out: 2*delta/1e-15 = 0.44408920985 (page 0.444); printed forward error at 1e-15 = 0.3903426 (page 0.390, "
        "expected block 3.903e-01)."),
    row("N-L24-half-ulp", "2.2 numbers: delta = 2.22e-16 described as half a unit in the last place of values near e",
        "course/modules/M/M2/L24.html:136", "PASS",
        S + "l24_numbers.out: ulp(e) = 4.440892098500626e-16, half ulp = 2.220446049250313e-16 = the page's delta."),
    row("N-L24-decade-ratios", "2.2 numbers: central errors fall x100 per decade to 1e-4; 4.531e-9 / 5.859e-11 = 77",
        "course/modules/M/M2/L24.html:243 (interpretation)", "PASS",
        S + "twin_vs_page.out Part B: central errors 4.533e-03, 4.530e-05, 4.530e-07, 4.531e-09 (ratio 100 per decade); "
        "l24_numbers.out: 4.531e-9 / 5.859e-11 = 77.33 (page 'about 77'); exact central error at 1e-4 = 4.5305e-9 (page 4.530e-9)."),
    row("N-L24-M3-numbers", "2.2 numbers: M3 forward quotient 12.61, error 0.61, bound 0.63 with M2 = 12.6",
        "course/modules/M/M2/L24.html:298 (M3 solution)", "PASS",
        S + "l24_numbers.out: (2.1^3 - 2^3)/0.1 = 12.61; error 0.61; sup|6x| on [2,2.1] = 12.6; (1/2)(12.6)(0.1) = 0.63."),
    row("LAB-L22-statements", "2.5 labs: L22 hypothesis, docstring, interpretation and E-problems vs code and output",
        "course/modules/M/M2/L22.html:99, :100-112 (twin docstring), :231", "PASS",
        "Twin lab-M2-L22-1.py: golden-section on [0, 10] (maximizer_a, PARAMETERS_A = 1.5, 2, 3, 4), STEP = 1e-4, naive partial "
        "= central difference of a frozen product, which is 0 (lines 22, 58, 84-85, 114); Part B has three values "
        "(PARAMETERS_B); docstring lines 4-11 match the code; the page's 'two problems' statement holds. Output in twin_vs_page.out."),
    row("LAB-L23-statements", "2.5 labs: L23 hypothesis, docstring and interpretation vs code and output",
        "course/modules/M/M2/L23.html:90, :91-107, :226", "PASS",
        "Twin lab-M2-L23-1.py: FACE 100000, COUPON 5000, YEARS 10, BASE 0.04 (lines 26-29); docstring lines 1-17 match the code; "
        "STEPS has three positive shifts (line 30) and the Part C loop has two shifts (line 115); the printed price at 0.05 is "
        "100000 (twin_vs_page.out 'yield shift +0.01'). Interpretation claims re-derived in l23_numbers.out."),
    row("LAB-L24-statements", "2.5 labs: L24 hypothesis, docstring and interpretation vs code and output",
        "course/modules/M/M2/L24.html:136, :137-149, :243", "PASS",
        "Twin lab-M2-L24-1.py: KINK_EXPONENTS 1..6 (line 20), SMOOTH_EXPONENTS 1..15 (line 21), decade steps, forward/backward/central "
        "as defined (lines 35-53), docstring lines 1-12 match; the interpretation's printed values match twin_vs_page.out; "
        "'the lab does not measure delta or M2' is true (no delta or M2 in the code)."),
    row("LAB-L22-L24-expected", "2.5 labs: run_labs expected blocks and tolerance",
        "course/modules/M/M2/L22.html:222, L23.html:215, L24.html:218", "PASS",
        S + "run_labs.out PASS for each page; twin_vs_page.out exact equality of stdout and expected block for all three. The "
        "data-tolerance attribute is 1e-6 but the comparison is exact text, which is at least as strict."),
    row("GR-L22-T", "2.3 grades: Lemma 1.2, Theorem 1.3, Proposition 2.1 and Example 2.3 graded T",
        "course/modules/M/M2/L22.html:63, :73, :239, :256, key results :395-398",
        "PASS", "Lemma 1.2 proof (L22.html:69) covers both signs of phi'; Theorem 1.3 proof (:80-83) uses H1 and H3 for the chain "
        "rule; Proposition 2.1 (:240-246) states all hypotheses its proof uses; Example 2.3 (:256) is computed correctly; each "
        "key-results row points to a proof on the page."),
    row("GR-L23-T", "2.3 grades: Propositions 2.1, 2.2, 3.2, 3.3 and Theorem 3.1 graded T",
        "course/modules/M/M2/L23.html:67, :79, :232, :242, :252, key results :405-409",
        "PASS", "Proposition 2.1 (:69-75) derivatives and signs re-derived; Proposition 2.2 (:80-85) uses the closed form of "
        "M1 Lesson 6 (M1 L06 Theorem 2.2 is the geometric-sum closed form, verified present); Theorem 3.1 (:233-238) uses L08 "
        "Theorem 2.1 with n = 2 under Assumption 1.1 of L08, which is EVT (L08.html:61); Propositions 3.2 and 3.3 proved on the page."),
    row("GR-L24-T", "2.3 grades: Theorem 2.1, Propositions 3.1, 3.2, 4.2, 4.3 graded T",
        "course/modules/M/M2/L24.html:60, :74, :84, :106, :116, key results :385-389",
        "PASS", "Theorem 2.1 (:61-66) re-derived; Propositions 3.1 and 3.2 (:75-93) use L08 Theorem 2.1 with n = 1 and n = 2 "
        "(two Taylor expansions with xi_1, xi_2); Propositions 4.2 and 4.3 (:107-123) minimize g(h) by the derivative test. "
        "Assumption 4.1 (:132) is a named, numbered assumption, and Remark 4.4 is ungraded."),
    row("M-L22-lemma-thm", "2.4 math: Lemma 1.2 and Theorem 1.3 proofs", "course/modules/M/M2/L22.html:63-83", "PASS",
        "Lemma 1.2 proof (:69): the limit of the difference quotient gives a positive quotient for small t > 0 when phi' > 0, and the "
        "same with t < 0 when phi' < 0; both cases are valid. Theorem 1.3 proof (:80-83): chain rule, f_x = 0 by Lemma 1.2, so V' = f_a."),
    row("M-L22-remark14", "2.4 math: Remark 1.4 (local (H3) from the implicit-function theorem)", "course/modules/M/M2/L22.html:88", "PASS",
        "Applies L21 Theorem 1.3 (L21.html:68: C^1 on an open U, F_y != 0, unique g on I x J) to G(a,x) = f_x(x,a), with G_x = f_xx "
        "!= 0 (the page's hypothesis); L21 Assumption 1.2 is IVT (L21.html:63), L06 Assumption 2.1 is EVT (L06.html:72); the zero "
        "in K is unique by the L21 uniqueness clause; x-hat in K by continuity at a0; conclusion local (H3)."),
    row("M-L22-example15", "2.4 math: Example 1.5 (logarithmic objective)", "course/modules/M/M2/L22.html:91-95", "PASS",
        "Re-derived: f_x = a/(1+x) - 1 vanishes at x = a - 1 (in J for a > 0); f_xx = -a/(1+x)^2 < 0, so f_x is strictly decreasing "
        "and the zero is the global maximizer; V = a ln a - (a - 1); V' = ln a under Assumption 1.1 (:94); f_a(x-hat, a) = ln a."),
    row("M-L22-prop21", "2.4 math: Proposition 2.1 (a constraint solved for one variable)", "course/modules/M/M2/L22.html:240-246",
        "PASS", "Re-derived: F(x,a) = g(x, c(x,a), a); chain rule gives F_a = g_y c_a + g_a at x-hat; hypotheses (C^1 of g and c, "
        "H1-H3 for F) are all stated and used."),
    row("M-L22-example22-23", "2.4 math: Example 2.2 (xy on x+y=a) and Example 2.3 (max ax on [0,1])", "course/modules/M/M2/L22.html:251, :256",
        "PASS", "Example 2.2: F_x = a - 2x, x-hat = a/2, F_xx = -2, V = a^2/4, g_y c_a = a/2 (matches V' = a/2). Example 2.3: "
        "V = max(a,0) with one-sided derivatives 1 and 0 at a = 0; the statements about the two cases and the non-unique maximizer are correct."),
    row("M-L22-problems", "2.4 math: problem-set solutions M1-M3, P1-P3, E1-E3, R1-R3 (L22)", "course/modules/M/M2/L22.html:290-386",
        "PASS", "M1 (:294): V = a^2/2, V' = a; M2 (:301): x-hat = a + 3/2, V = 3a + 9/4, V' = 3 = f_a; M3 (:308): c_a = 1/2, "
        "x-hat = a/2, y* = a/4, V = a^2/8, V' = a/4 = g_y c_a. P1-P3 (:319, :326, :333) correct. E1-E3 numbers match "
        "twin_vs_page.out (0.50000001, 1e-8, 0.40546511 vs 0.40546512). R1 (:369) cites L21 Assumption 1.2 and L06 Assumption 2.1, "
        "both exist; R2 (:376) states the vector case as unproved; R3 (:383) correct."),
    row("M-L23-prop21-22", "2.4 math: Proposition 2.1 derivatives and sign; Proposition 2.2 (price at face)",
        "course/modules/M/M2/L23.html:69-85", "PASS",
        "Derivatives of (1+y)^(-t) re-derived (-t(1+y)^(-t-1), t(t+1)(1+y)^(-t-2)); Prop 2.2: v = 1/(1+r), 1 - v = rv, "
        "sum_{t=1}^N v^t = (1 - v^N)/r (M1 L06 closed form), price F(1 - v^N) + F v^N = F; the r = 0 case is handled."),
    row("M-L23-thm31-prop32", "2.4 math: Theorem 3.1 (remainder bound) and Proposition 3.2 (sign of the remainder)",
        "course/modules/M/M2/L23.html:233-248", "PASS",
        "Theorem 3.1: Lagrange remainder of order 2 from L08 (Theorem 2.1, n = 2) and the bound (1/6) M |Delta|^3 over the closed "
        "interval; M exists because P''' is continuous on a compact interval. Proposition 3.2: P''' = -sum t(t+1)(t+2) c_t (1+y)^(-t-3) "
        "< 0 for positive cash flows; R = (1/6)P'''(theta) Delta^3 has the sign of -Delta, as the statement says."),
    row("M-L23-prop33", "2.4 math: Proposition 3.3 (first-order expansion lies below the price)", "course/modules/M/M2/L23.html:252-258",
        "PASS", "P - P1 = (1/2) P''(theta) Delta^2 from L08 Theorem 2.1 with n = 1, and P'' > 0 from Proposition 2.1, so the difference is "
        "non-negative for every admissible Delta, including Delta = 0."),
    row("M-L23-problems", "2.4 math: L23 problem set M1-M3, P1-P3, E1-E3, R1-R3", "course/modules/M/M2/L23.html:300-395",
        "PASS", "M1 (:304): 50/1.05 + 1050/1.05^2 = 1000.000; M2 (:311) P' = -c(1+y)^-2, P'' = 2c(1+y)^-3; M3 (:318) P'(0.04) = "
        "-200/1.04^3; P1 (:329) uses L06 Corollary 3.1(ii) (L06.html:103) on -P and P'; P2 (:336), P3 (:343) correct; E1-E3 "
        "(:354, :361, :368) correct, including the 2.78e-18 offset of E3 (l23_numbers.out); R1 (:379) dy/dP = 1/P'(y) < 0; "
        "R2 (:386) correct; R3 (:393) correct."),
    row("M-L24-thm21-prop31-32", "2.4 math: Theorem 2.1, Propositions 3.1 and 3.2", "course/modules/M/M2/L24.html:60-93", "PASS",
        "Theorem 2.1 re-derived for both steps (Delta = h > 0 and h < 0); Proposition 3.1 uses L08 Theorem 2.1 with n = 1; "
        "Proposition 3.2: Taylor with n = 2 at x + h and x - h gives D0 - f' = (1/12) h^2 (f'''(xi1) + f'''(xi2)), bounded by (1/6) M3 h^2."),
    row("M-L24-prop42-43", "2.4 math: Propositions 4.2 and 4.3 (bound functions and minimizers)", "course/modules/M/M2/L24.html:107-123",
        "PASS", "Prop 4.2: g(h) = (M2/2) h + 2 delta/h minimized at h* = 2 sqrt(delta/M2), value 2 sqrt(M2 delta); the round-off "
        "term 2 delta/h is correct (numerator error at most 2 delta). Prop 4.3: g(h) = (M3/6) h^2 + delta/h, h^3 = 3 delta/M3 "
        "(derivative 2Ch - B/h^2 = 0 with C = M3/6, B = delta), correct."),
    row("M-L24-remark44-assumption", "2.4 math (round-6 FAIL re-verified): Remark 4.4 claims about the bound at h* and the error",
        "course/modules/M/M2/L24.html:129; card M2-c365", "PASS",
        "Remark 4.4 now says the bound is guaranteed at h* only if h* is in H, and that Proposition 4.2 says nothing about the "
        "error at h* otherwise; it does not claim h* minimizes the error (the page says so at :125). The numbers it quotes match "
        + S + "l24_numbers.out. The round-6 FAIL is no longer present."),
    row("M-L24-problems", "2.4 math: L24 problem set M1-M3, P1-P3, E1-E3, R1-R3", "course/modules/M/M2/L24.html:281-375",
        "PASS", "M1 (:284): D+ = 2 + h, D- = 2 - h, D0 = 2; M2 (:291) |x| central 0, forward 1; M3 (:298) 12.61, error 0.61, "
        "bound 0.63 (l24_numbers.out); P1 (:309), P2 (:316), P3 (:323) correct; E1 (:334) correct; E2 (:341) 0.444 and 0.390 "
        "(l24_numbers.out); E3 (:348) corrected to 4.4e-16 (l24_unrounded.out); R1 (:359) factor-of-10 argument correct; R2 (:366) "
        "Lipschitz bound correct; R3 (:373) cites L14 forward mode (def-automatic-differentiation, L14.html)."),
    row("CARD-L22", "2.7 cards: all 15 L22 cards (M2-c323..c337, c404) against the current L22 text", "course/modules/M/M2/cards.json (lesson L22)",
        "PASS", S + "cards_scan.out lists the 15 L22 cards. Each is checked against L22.html: c325 hypotheses (H1)-(H3) match :74; c331 "
        "hypotheses match :240; c334 'uniqueness is not assumed' is right because (H2) requires only a maximizer; c328, c329 and c336 "
        "quote printed values that match twin_vs_page.out; c336's 'about 10^-8' is consistent with the unrounded errors. No card quotes "
        "the two changed L22 sentences (:93, :231)."),
    row("CARD-L23", "2.7 cards: all 24 L23 cards (M2-c338..c357, c382..c386, c407) against the current L23 text", "course/modules/M/M2/cards.json (lesson L23)",
        "PASS", S + "cards_scan.out lists the 24 L23 cards. L23.html is byte-identical to the round-7 pin; each card matches its lesson: "
        "c340 hypotheses of Proposition 2.2; c348 remainder bound; c349 sign; c350 first-order result; c341-343, c345-346, c352, c382-385, "
        "c407 match l23_numbers.out and twin_vs_page.out."),
    row("CARD-L24", "2.7 cards: all 18 L24 cards (M2-c358..c373, c375, c387, c405, c410) against the current L24 text", "course/modules/M/M2/cards.json (lesson L24), M2-c365 at cards.json:2564",
        "PASS", S + "cards_scan.out lists the 18 L24 cards. Each matches L24.html: c359 Theorem 2.1; c360-361 Propositions 3.1-3.2; c363-364 "
        "Propositions 4.2-4.3; c365 Remark 4.4; c367-368 and c370 match twin_vs_page.out and l24_numbers.out (c370 '6.3e-6' is the "
        "two-figure rounding of 6.2578e-6); no card quotes the changed sentence at L24.html:348."),
    row("CARD-DUP", "2.7 cards: no duplicate card in L22-L24 and none across the unit", "course/modules/M/M2/cards.json",
        "PASS", S + "cards_scan.out: no duplicate ids, normalized fronts or normalized backs across all 394 cards."),
    row("S-L22-L24-structure", "2.9 structure: section order, quiz of 8 items per lesson, misconceptions, problem tiers",
        "course/modules/M/M2/L22.html, L23.html, L24.html", "PASS",
        S + "prose_scan.out: each page has 12 solutions (all at least 15 words), 3 misconceptions, 8 quiz items, the four tiers "
        "mechanics, proof, empirical, research, and 12 problems; check_pages PASS (gates_pages_dag.out)."),
    row("S-banned-phrases", "2.9 banned phrases (BUILDER_RULES 1.3-1.4): TODO, TBD, lorem, ellipsis, for brevity, etc.",
        "course/modules/M/M2/L22.html, L23.html, L24.html", "PASS",
        S + "prose_scan.out: zero hits for TODO, TBD, lorem, an ellipsis, 'for brevity', 'details omitted', 'beyond the scope', "
        "'left as an exercise', 'you can add more', 'it is important to note', 'studies show', 'experts agree', 'it is well known', "
        "'obviously', 'clearly'. 'round-off' (23 hits in L24) is the technical term, not a process word."),
    row("S-process-words", "2.9 no process words in learner text (round, builder, verifier, architect, fixed, request tags)",
        "course/modules/M/M2/L22.html, L23.html, L24.html", "PASS",
        S + "prose_scan.out: zero hits for builder, verifier, architect, 'round 7', 'round 8', R7, R8, DAG_DEFECT, NOTATION_REQUEST, "
        "REFERENCE_REQUEST, GLOSSARY_REQUEST, 'fixed in', 'Open item'."),
    row("S-scope-words", "2.9 scope words (only, all, always, every, any, same, exactly, never, none)",
        "course/modules/M/M2/L22.html, L23.html, L24.html", "PASS",
        S + "links_and_scope.out lists each occurrence with context (55 lines). Each universal word is a stated hypothesis (for example "
        "'every c_t > 0', 'for every h in H') or a computed fact ('vanishes exactly at a - 1'); 'always' appears only inside a "
        "misconception the page refutes (L23.html misconception 3)."),
    row("DAG-prerequisites", "2.9 DAG: L22-L24 use only concepts of M2 lessons up to their own, M1 and P0.1, plus prose terms",
        "course/modules/M/M2/L22.html:37, L23.html:37, L24.html:37", "PASS",
        S + "check_dag.py --unit M2 PASS. Uses lines: L22 derivative (L04), partial (L16), gradient (L17), hessian (L19), IFT (L21); "
        "L23 taylor (L08), derivative (L04), IFT (L21), present-value and discount-factor (M1 L05, concepts.html anchors exist), "
        "geometric-series (M1 L06, anchor exists); L24 finite-difference (L13), derivative (L04), taylor (L08), "
        "automatic-differentiation (L14). Every anchor is defined in its lesson (grep of id= attributes). Prose-only terms: continuity "
        "(L22), open set (L22), Lipschitz (L24 R2, defined inline), Lagrange form of Taylor's theorem (L08 result), duration and "
        "convexity (L23 meta and lab docstring only, unlinked: Architect Q8)."),
    row("DAG-no-later-definitions", "2.9 DAG: no concept defined twice; no later-module dfn or link (Fubini, continuity, Lagrange multiplier, etc.)",
        "course/modules/M/M2/L22.html, L23.html, L24.html", "PASS",
        S + "grep: def-envelope-theorem appears once (L22.html:59); L23 and L24 define no concept. No occurrence of fubini, "
        "epsilon-delta, riemann-stieltjes, lebesgue, lagrange-multiplier, lagrangian-duality in the three pages. 'Lagrange' appears "
        "only as 'Lagrange form of Taylor's theorem' (L08 result). duration and convexity are unlinked prose (Architect Q8)."),
    row("H-hours", "2.9 hours: data-hours=10 and '10 study hours' on each of L22, L23, L24", "course/modules/M/M2/L22.html:2, L23.html:2, L24.html:2",
        "PASS", "data-hours=\"10\" on the html element of each page (L22.html:2, L23.html:2, L24.html:2) and the eyebrow '10 study "
        "hours' (:34 in each). The hub split (240 + 60) is outside this slice."),
    row("REF-cross-lesson", "2.1 attributions: cross-lesson references in L22, L23, L24 resolve to the stated results",
        "course/modules/M/M2/L22.html:473, L23.html:488, L24.html:468", "PASS",
        "L06 Assumption 2.1 is the extreme value theorem (L06.html:72); L06 Theorem 2.3 is the mean value theorem (L06.html:87); L08 "
        "Assumption 1.1 is the same EVT (L08.html:61) and L08 Theorem 2.1 is the Lagrange form (n-th order); L21 Assumption 1.2 is the "
        "intermediate value theorem (L21.html:63) and L21 Theorem 1.3 is the IFT with a uniqueness clause (L21.html:68); M1 L06 is the "
        "geometric series (Theorem 2.2) and M1 L05 is present value."),
    row("REG-registry-flags", "2.1 registry: no key cited with a locator on L22-L24; nothing to flag",
        "course/modules/M/M2/L22.html:473, L23.html:488, L24.html:468", "PASS",
        "The References sections name spivak2008calculus and hubbard2015vector with 'no locator confirmed'; no statement is attributed to "
        "them. references.json offline integrity: 560 entries, 0 problems (gates_refs_pytest_projects.out). No registry_flags."),
]

fragment = {
    "unit": "M2",
    "slice": "d2",
    "round": 8,
    "verifier": "Claude Haiku 5.5, independent verifier for M2-d2, round 8 (did not build M2; no context shared with the builders).",
    "pin": "2d755599d8d74df292e3e43025f0458c4053802e",
    "base": "9373ef398589097500ea849e30ff9da423b98943 (round-7 pin). Delta 9373ef39..2d755599 touches course/modules/M/M2/L22.html "
            "(Example 1.5 wording at :93; interpretation at :231), L24.html (E3 solution at :348), cards.json (M2-c399 and c400, not in "
            "this slice) and project.html (not in this slice). tests/labs/M2 and notation/references are unchanged. Every hunk in "
            "the slice was read (git diff output). All slice rows were re-verified from scratch; no PASS row is carried forward.",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyD8-M2-d2",
    "scratch": "/Users/billyribeiro/.fanout/wt/verifyD8-M2-d2/ledgers/M2/scripts/M2-d2-r8",
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "Lab-only slice: L22-L24 hold no project grader, so run_graders, mutate_graders and alternative implementations are not "
        "applicable (architect ruling 9 applies to grader mutants); mutants is empty. Not run: run_graders and mutate_graders for M2 "
        "(no grader in the slice); verify_refs --unit M2 (live network); repository-wide gates (check_pages --all, build_site --check, "
        "render_curriculum, fetch_data --check, run_graders --all); the other M2 slices. check_projects --unit M2 was run as context and "
        "returned PASS. Round-7 non-PASS row N-L24-E3-difference (4.5e-16) is PASS now (page reads 4.4e-16, unrounded difference "
        "4.440892e-16). Round-7 PASS rows were all re-verified; the L23 page and its cards are byte-identical to the round-7 pin. "
        "Only one defect: N-L22-xhat-error, a sentence introduced in this delta. Observation, not a defect: L22 Problem R2 (:376) "
        "states the vector-case need for an invertible Hessian without proof and says so (ungraded, hedged)."
    ),
    "summary": "",
}
counts = {"PASS": 0, "FAIL": 0, "UNVERIFIABLE": 0}
for r in rows:
    counts[r["status"]] += 1
fragment["summary"] = (
    f"slice d2 round 8: rows={len(rows)}, pass={counts['PASS']}, fail={counts['FAIL']}, unverifiable={counts['UNVERIFIABLE']}. "
    "Mutants 0 (lab-only slice). Single non-PASS row: N-L22-xhat-error (L22.html:231, the new sentence 'off by between 1e-8 and 2e-8')."
)

out = ROOT / "ledgers/M2/M2-d2.json"
out.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out, "rows", len(rows), counts)
