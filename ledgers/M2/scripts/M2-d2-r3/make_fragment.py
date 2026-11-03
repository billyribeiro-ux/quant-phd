"""Writes the round-3 fragment for M2-d2 (verifier output; rows and evidence set by the verifier)."""
import json
from datetime import datetime, timezone
from pathlib import Path

S = "ledgers/M2/scripts/M2-d2-r3"
R = lambda name: f"{S}/{name}"  # noqa: E731

rows = [
    # ---- gates (commands run this round on pin a007712)
    ("G-check-pages", "tools/check_pages.py --unit M2", "tools/check_pages.py", "PASS",
     f"{R('check_pages.out')}: 'check_pages M2: PASS', exit 0 (run this round)."),
    ("G-check-dag", "tools/check_dag.py --unit M2 and --all", "tools/check_dag.py", "PASS",
     f"{R('check_dag.out')}: 'check_dag M2: PASS', exit 0; {R('check_dag_all.out')}: all units PASS, exit 0."),
    ("G-check-projects", "tools/check_projects.py --unit M2", "tools/check_projects.py", "PASS",
     f"{R('check_projects.out')}: 'check_projects M2: PASS', exit 0 (hub-level; no project page in this slice)."),
    ("G-run-labs", "tools/run_labs.py --unit M2 --page L22 / L23 / L24", "tools/run_labs.py", "PASS",
     f"{R('run_labs_L22.out')}, {R('run_labs_L23.out')}, {R('run_labs_L24.out')}: each 'run_labs M2: PASS (1/1)', exit 0."),
    ("G-twins-isolated", "twins under python -I -W error, CPython 3.14 venv", "tests/labs/M2/lab-M2-L22-1.py, lab-M2-L23-1.py, lab-M2-L24-1.py", "PASS",
     f"{R('compare_labs.out')}: 'L22/L23/L24 twin exit 0, stderr bytes 0' (run from a temporary directory with -I -W error); stdout saved in {R('twin_L22.stdout')}, {R('twin_L23.stdout')}, {R('twin_L24.stdout')}."),
    ("G-expected-blocks", "expected block equals twin stdout (pages L22, L23, L24)", "course/modules/M/M2/L22.html:222-230, L23.html:215-225, L24.html:218-242", "PASS",
     f"{R('compare_labs.out')}: 'expected == stdout: True' with 9, 11 and 25 lines respectively."),
    ("G-page-code-equals-twin", "page lab code equals twin file", "course/modules/M/M2/L22.html:97-232, L23.html:88-227, L24.html:134-244", "PASS",
     f"{R('code_diff.out')}: line-level diff 0 for all three; the page block ends without the final newline the twin file has (embedding artifact; run_labs passes)."),
    ("G-page-smoke", "tools/page_smoke.py --unit M2 --pages L22 L23 L24", "tools/page_smoke.py", "PASS",
     f"{R('page_smoke_L22_L24.out')}: each page PASS, lab runtime 0.0 s, 'page_smoke M2: PASS', exit 0."),
    ("G-ruff", "ruff check and ruff format --check on the three twins", "tests/labs/M2/lab-M2-L22-1.py, L23-1.py, L24-1.py", "PASS",
     f"{R('ruff_check.out')}: 'All checks passed!' exit 0; {R('ruff_format.out')}: '3 files already formatted' exit 0."),
    ("G-mypy", "mypy --no-incremental on the three twins", "tests/labs/M2/lab-M2-L22-1.py, L23-1.py, L24-1.py", "PASS",
     f"{R('mypy.out')}: 'Success: no issues found in 3 source files', exit 0."),
    ("G-pytest-labs", "pytest tests/test_labs.py for the three slice labs", "tests/test_labs.py", "PASS",
     f"{R('pytest_labs_slice.out')}: three passing cases (lab-M2-L22-1, L23-1, L24-1), exit 0."),
    ("G-pytest-checks", "pytest tests/test_page_checks.py tests/test_run_labs.py", "tests/test_page_checks.py, tests/test_run_labs.py", "PASS",
     f"{R('pytest_m2_checks.out')}: 47 passed, exit 0."),
    ("G-verify-refs", "tools/verify_refs.py --offline and --unit M2 (live)", "tools/verify_refs.py; references/references.json", "PASS",
     f"{R('verify_refs_offline.out')}: 'offline integrity: 560 entries, 0 problems'; {R('verify_refs_live_M2.out')}: 'live re-verification of M2: 2 of 560 entries, 0 problems'."),
    ("G-cards-scan", "full scan of cards.json (394 cards) and the 56 cards of L22-L24", "course/modules/M/M2/cards.json", "PASS",
     f"{R('cards_dup_scan.out')}: 394 cards, 394 distinct ids; every number cited in a slice card appears in its lesson; the 20 front pairs with similarity >= 0.75 differ in substance (for example c342 P' versus c343 P''; c345 first-order versus c384 second-order error)."),
    # ---- structure, prose, banned phrases
    ("S-hours", "hours arithmetic and lesson header", "L22.html:2, L23.html:2, L24.html:2", "PASS",
     "data-hours=\"10\" on each page; eyebrows read '10 study hours' (L22.html:34); check_pages PASS (G-check-pages)."),
    ("S-structure", "section order and navigation (BUILDER_RULES 4.2)", "L22.html:53-482; L23.html:53-501; L24.html:53-482", "PASS",
     "Order in each page: why-it-matters, core sections, inline lab, where-the-canon-breaks, misconceptions (3), problem set (mechanics, proof, empirical, research: 3 each), key results, quiz (8 items), references, lesson nav. Note: in L22 the canon-breaks element (L22.html:234) also contains core Section 2; check_pages accepts it."),
    ("S-banned", "banned phrases (BUILDER_RULES 1.3-1.4) in the three pages", "L22.html, L23.html, L24.html", "PASS",
     f"grep -i for TODO, TBD, lorem, for brevity, details omitted, beyond the scope, left as an exercise, you can add more, it is important to note, studies show, experts agree, it is well known, obviously, clearly: zero hits (command output in this round's shell; no file kept). Ellipses occur only in code tuple types (L23.html:120, L24.html:156-157, L22.html:119-120)."),
    ("S-process-words", "process words in learner text", "L22.html, L23.html, L24.html", "PASS",
     "grep -i for builder, verifier, ledger, fragment, haiku, round N, pass (as a word): zero hits in the three pages."),
    ("S-simulated", "SIMULATED labels where synthetic data is used", "L22.html:99; L23.html:90; L24.html:136; twins line 3", "PASS",
     "Each lab hypothesis opens with SIMULATED (L22.html:99, L23.html:90, L24.html:136) and each twin docstring line 3 says SIMULATED (tests/labs/M2/lab-M2-L2x-1.py)."),
    ("S-external", "no external requests, CDN, iframe or tracker", "L22.html, L23.html, L24.html", "PASS",
     "grep -i for http, iframe, src=\"//\": zero hits; the only assets are ../../../assets/vendor/katex and ../../../assets/css|js (head of each page)."),
    # ---- DAG and notation
    ("DAG-links", "concept links: every concept used from an earlier lesson is linked and listed in the page's Uses row (BUILDER_RULES 4.1)", "L22.html:37 and 374-376; L23.html:37 and 377-379", "FAIL",
     "L22 Uses row (L22.html:37) names derivative (L04), partial derivative (L16) and implicit-function theorem (L21) only. Problem R2 (L22.html:374-376) uses the gradient (Lesson L17) and the Hessian matrix (Lesson L19) as objects, unlinked. L23 Uses row (L23.html:37) omits the implicit-function theorem (L21); Problem R1 (L23.html:377-379) uses it ('Use Lesson L21 ... the implicit-function result of L21') unlinked. L19 defines def-hessian and L17 def-gradient, L21 def-implicit-function-theorem (verified by grep). Links to the three concepts resolve; the Uses rows are incomplete."),
    ("DAG-defined-once", "each concept defined once; no dfn in a slice lesson that the plan assigns elsewhere", "L22.html:59; L23.html; L24.html", "PASS",
     "L22 has one <dfn> (envelope-theorem, L22.html:59); L23 and L24 have none (plan 3: M2 concepts assigned to L22 only from this slice). No duplicate def-ids in the slice."),
    ("DAG-later-names", "concepts from later modules or later lessons named or linked", "L22.html, L23.html, L24.html", "PASS",
     "grep for Lagrange multiplier, Lagrangian, Fubini, Lebesgue, Stieltjes, Riemann, epsilon-delta: zero hits (only 'open set', an undeclared prose term per the plan). 'duration' and 'convexity' occur only as named previews (L23.html:7, 91) with no dfn and no link (plan Q8). Links to M1 concepts resolve (concepts.html#present-value, #discount-factor, #geometric-series)."),
    ("NOT-notation", "every macro and symbol against notation/notation.json", "L22.html, L23.html, L24.html", "PASS",
     "Macros used: \\R (registered, meaning real numbers; L22.html:240 R^3) and \\ln, \\max, \\tfrac, \\hat, \\varphi, \\Delta, \\theta, \\mathcal{P}, \\delta, \\xi (not registered). T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f and Q are not used; R(Delta) is the lesson's remainder (local), not R^*. Local letters N, F, r, M, c are defined in place."),
    ("REF-keys", "registry keys cited", "L22.html:474; L23.html:488; L24.html:468", "PASS",
     f"Only spivak2008calculus and hubbard2015vector appear, as registry keys in the reference lists, with no locator-level attribution; {R('verify_refs_offline.out')} and the live M2 run both report 0 problems."),
    ("REF-internal", "internal cross-references (theorem, assumption and lesson numbers) resolve to the statement they name", "L22.html:87-88, 369, 473; L23.html:232-243, 376-379, 488; L24.html:107, 136, 468", "PASS",
     "L21 Theorem 1.3 (IFT, L21.html:68) with Assumption 1.2 (IVT, L21.html:63); L21 Theorem 2.1 (slope formula, L21.html:86); L06 Assumption 2.1 (EVT, L06.html:72) and Theorem 2.3 (MVT, L06.html:87); L08 Theorem 2.1 (Lagrange remainder) and Assumption 1.1 = L06 Assumption 2.1 (L08.html:61, 90); L13 finite-difference-derivative, L14 automatic-differentiation (L14.html dfn), L17 gradient, L19 hessian; M1 L05 present value and discount factor, M1 L06 geometric series. Each cross-reference was read at its locator."),
    # ---- grades and mathematics
    ("GRADE-theorems", "grade (T/A/B/C/D/X) of each theorem, proposition and claim", "L22.html:63, 73, 239, 396-398; L23.html:67, 79, 232, 242, 251; L24.html:55-60, 74-84, 107-122", "PASS",
     "Lemma 1.2, Theorems 1.3 and 2.1 (L24), Propositions 2.1-2.2, 3.1-3.3, 4.2-4.3 carry T with hypotheses in the statement. Assumptions (L22 Assumption 1.1, L24 Assumption 4.1, L22-L24 references to L06 Assumption 2.1) are labelled as assumed and not graded. Lab outputs are described as lab results in text, not as T. The one over-grade is card M2-c370 (see CARD-L24)."),
    ("MATH-L22-lemma-thm", "Lemma 1.2 and Theorem 1.3 proofs", "L22.html:63-83", "PASS",
     "Lemma 1.2: one-sided quotient argument re-derived (phi(x+t)-phi(x) over t has sign of phi'(x)); Theorem 1.3: chain rule V' = f_x x^ + f_a with f_x = 0 by Lemma 1.2; hypotheses (H1)-(H3) used exactly where needed."),
    ("MATH-L22-remark14", "Remark 1.4 (where H3 comes from)", "L22.html:87-88", "PASS",
     "Re-derived: G(a,x)=f_x(x,a) has partial in x equal to f_xx != 0; L21 Theorem 1.3 (L21.html:68) gives a unique local solution x~ with values in J; continuity of x^ gives x^(a) in J, and the uniqueness in J comes from that theorem's conclusion. Cites Assumption 1.2 (L21.html:63) and L06 Assumption 2.1 (L06.html:72), both as stated."),
    ("MATH-L22-example15", "Example 1.5 (log objective)", "L22.html:92-94", "PASS",
     "f_x = a/(1+x) - 1, zero at a-1; f_xx = -a/(1+x)^2 < 0; V = a ln a - (a-1), V' = ln a; numeric central difference at a=1.5 (recheck_math.out: 0.40546510811 vs ln 1.5 = 0.40546510811)."),
    ("MATH-L22-prop21-ex22-ex23", "Proposition 2.1, Examples 2.2 and 2.3", "L22.html:239-256", "PASS",
     "Proposition 2.1 proof re-derived by the chain rule F_a = g_y c_a + g_a; Example 2.2: F_x = a-2x, F_xx = -2, V = a^2/4, V' = a/2, g_y c_a = a/2 (recheck_math.out: numeric V'(2) = 1.0000000000); Example 2.3: V = max(a,0), one-sided derivatives 1 and 0 at a=0."),
    ("MATH-L22-exercises", "Problem set M1-M3, P1-P3, E1-E3, R1-R3 and key-results table", "L22.html:290-466, 390-400", "PASS",
     "Every solution re-derived: M1 V=a^2/2, V'=a; M2 x^=a+3/2, V=3a+9/4, V'=3=f_a; M3 V=a^2/8, V'=a/4; P2 V=max(a,0); E1-E3 explanations consistent with the printed output (E3: f_a=ln(1+x^) moves with x^); R1-R3 statements consistent with Theorem 1.3, Remark 1.4 and Example 2.3; key-results rows match the theorems."),
    ("MATH-L23-prop21-22", "Proposition 2.1 (derivatives), Proposition 2.2 (price at face)", "L23.html:67-86, 79-90", "PASS",
     "Term-by-term derivatives re-derived; P' = -sum t c_t (1+y)^(-t-1), P'' = sum t(t+1) c_t (1+y)^(-t-2) (recheck_numbers.out: P'(0.04) = -851466.7395285615, P''(0.04) = 8376648.51191949); Proposition 2.2 with v = 1/(1+r), 1-v = rv, geometric sum (1-v^N)/r gives price F (M1 check: 50/1.05 + 1050/1.05^2 = 1000)."),
    ("MATH-L23-thm31-prop32-33", "Theorem 3.1, Propositions 3.2 and 3.3", "L23.html:231-263", "PASS",
     "Lagrange remainder (1/6) P'''(theta) Delta^3 from L08 Theorem 2.1; P''' = -sum t(t+1)(t+2) c_t (1+y)^(-t-3) < 0, so R has the sign of -Delta (Prop 3.2; matches the printed second-order errors -15.06, -1.91, -0.24 at +0.01, +0.005, +0.0025); Prop 3.3 P - P1 = P''(theta) Delta^2 / 2 >= 0."),
    ("MATH-L24-thm21", "Theorem 2.1 (quotients of |x| at 0)", "L24.html:59-66", "PASS",
     "D+ = |h|/h = 1, D- = -|h|/h = -1, D0 = 0 for every h > 0 (also exact in IEEE floats: recheck_numbers.out and the twin's Part A output); no derivative since one-sided limits differ."),
    ("MATH-L24-prop31-32", "Propositions 3.1 and 3.2 (truncation)", "L24.html:73-94", "PASS",
     "Lagrange order 1: D+ - f' = (1/2) h f''(xi), so |.| <= M2 h / 2. Lagrange order 2 expansions subtracted: D0 - f' = (1/12) h^2 (f'''(xi1) + f'''(xi2)), so |.| <= (1/6) M3 h^2. Both re-derived; M2 = 6x sup check in M3 problem (0.61 <= 0.63)."),
    ("MATH-L24-prop42-43", "Propositions 4.2 and 4.3 (computed quotients, minimizers)", "L24.html:105-123", "PASS",
     f"g(h) = A h + B/h minimized at h* = sqrt(B/A) with g = 2 sqrt(AB); recomputed: A = M2/2, B = 2 delta gives h* = 2 sqrt(delta/M2) and g = 2 sqrt(M2 delta). Prop 4.3: h^3 = 3 delta/M3. Grid check {R('recheck_math.out')}: argmin equals h* for both (1.80742e-8 and 6.25739e-6)."),
    ("MATH-L24-remark44-assumption", "Remark 4.4 and Assumption 4.1", "L24.html:125-132", "PASS",
     "Remark 4.4 is correctly stated as a bound-not-error remark; Assumption 4.1 (d/dx e^x = e^x) is labelled assumed, not proved (L24.html:132)."),
    ("MATH-L24-canon-bullet3", "'Where the canon breaks', bullet 3 (round-off term 2 delta/h)", "L24.html:252", "FAIL",
     "The bullet says the round-off term 2 delta/h 'bounds the error of the computed difference f~(x+h) - f~(x)'. Under Definition 4.1 the difference's error is at most 2 delta; dividing by h gives the 2 delta/h bound on the quotient (Prop 4.2 proof, L24.html:112). Card M2-c375 states it correctly, so the page and the card disagree."),
    # ---- numbers in prose
    ("N-L22", "numbers in L22 prose and lab output", "L22.html:231; twin_L22.stdout", "PASS",
     f"Printed 0.50000001 at a=1.5; central differences equal ln a to 8 decimals; largest Part B error 5.4e-12 (the Part B column 'error' shows 1.9e-13, 1.0e-12, 5.4e-12); naive partial 0; location error effect 3.3e-17 recomputed (recheck_math.out). All quoted values agree with {R('twin_L22.stdout')}."),
    ("N-L23", "numbers in L23 prose and lab output", "L23.html:51, 226, 271, 368, 376-379, 406", "PASS",
     f"Recomputed in {R('recheck_numbers.out')}: unrounded price 108110.895779 (rounds to 108111); P' = -851466.739529 and P'' = 8376648.511919 with central-difference differences 1.6e-3 and 1.9; -P'/P = 7.875864, P''/P = 77.482001; errors and ratios 3.9279, 7.8807, 3.9634, 7.9396; exact 100000 and 117060 with second-order 100015 and 117044; float 0.04+0.01 differs from 0.05 by 2.78e-18 and moves the price by 2.14e-12 cents (E3 says about 2.1e-12); quiz counterexample -1777.07."),
    ("N-L24", "numbers in L24 prose and lab output", "L24.html:243, 341-352, 359-362, 385-391", "PASS",
     f"Recomputed in {R('recheck_numbers.out')}: forward errors 1.406e-1 (h=1e-1), 1.359e-5 (1e-5), 6.603e-9 (1e-8), 2.154e-7 (1e-9), 3.263e-5 (1e-11), 3.903e-1 (1e-15); central errors 4.531e-9 (1e-4) and 5.859e-11 (1e-5); 4.531e-9/5.859e-11 = 77.3; unrounded central errors 5.858691310e-11 (1e-5) and 5.858735719e-11 (1e-7), difference 4.44e-16 = one ulp of e (ulp 4.440892e-16); 2 sqrt(delta/e) = 1.807e-8; (3 delta/e)^(1/3) = 6.257e-6; 2 delta/h at 1e-15 = 0.444 (E2)."),
    ("N-L22-L23-L24-quiz", "quiz answers and explanations", "L22.html:417-457; L23.html:437-463; L24.html:417-453", "PASS",
     "Numeric answers 2.5 (a^2=5, V=a^2/2), 0.5 (V'(1) of Example 2.2), 0.25 (M3 at a=1), 1000 (Proposition 2.2 at 5 percent), -200 (zero-coupon P' at 0), 2 (D0 of x^2), 1 (h* = 2 sqrt(0.5/2)); MC keys match the statements; L23 q8 counterexample -1777.07 recomputed."),
    # ---- labs
    ("LAB-L22", "Lab 1 of L22 (lab-M2-L22-1)", "L22.html:97-232; tests/labs/M2/lab-M2-L22-1.py", "PASS",
     "Twin run under -I -W error exit 0, stderr empty; page code equals twin; expected block equals stdout (9 lines). Docstring matches code: golden-section on [0,10] for Part A, V' by central difference step 1e-4 against ln a and f_a = ln(1+x^); Part B substitutes y = a - x and prints the naive partial (0). The Part B lab maximizes over [0,a] (nonnegative x, y), a restriction of the Example 2.2 problem with the same maximizer; the page does not state the restriction (noted, not a defect of the printed claims)."),
    ("LAB-L23", "Lab 1 of L23 (lab-M2-L23-1), twin docstring and page", "L23.html:88-227; tests/labs/M2/lab-M2-L23-1.py:1-14", "PASS",
     "Round-2 FAIL fixed: docstring now states that the price is exact (Fraction), that P'(y0), P''(y0) are floats each rounded once to the nearest double (code: float(exact sum)), that the Taylor polynomials are exact given those floats, and that the reported price and expansion are rounded half-to-even by Fraction.round(). Part B prints three positive shifts and Part C two shifts (+0.01, -0.01), as the lesson says. Twin exit 0, expected == stdout (11 lines)."),
    ("LAB-L24", "Lab 1 of L24 (lab-M2-L24-1), twin docstring and page", "L24.html:134-244; tests/labs/M2/lab-M2-L24-1.py:1-12", "PASS",
     "Round-2 FAIL fixed: docstring now says the quotients print +1, -1 and 0 at each of the six steps, that the lab computes no limit, and that Part B runs k = 1 to 15 with the decade minimum for each quotient; code matches (KINK_EXPONENTS 1-6, SMOOTH_EXPONENTS 1-15). Twin exit 0, stderr empty, expected == stdout (25 lines)."),
    # ---- cards
    ("CARD-L22", "cards of L22: M2-c323..c337 and c404", "course/modules/M/M2/cards.json", "PASS",
     f"All 15 cards read in full ({R('cards_L22_L24.jsonl')}); each agrees with the current L22 text; lab-result cards (c328, c329, c336) are graded C with basis Lab 1; T cards carry the hypotheses (c325, c331); c326 matches Remark 1.4; numbers present in the lesson."),
    ("CARD-L23", "cards of L23: M2-c338..c357, c382..c386, c407", "course/modules/M/M2/cards.json", "PASS",
     f"All 24 cards read ({R('cards_L22_L24.jsonl')}). Round-2 FAIL fixed: no T-graded card carries lab output (lab-number cards c341-c346, c352, c382-c385, c407 are C with basis); T cards c348-c350 carry hypotheses; numbers appear in L23 (expected block or interpretation)."),
    ("CARD-L24", "cards of L24: M2-c358..c375, c387, c405 (c370 changed)", "course/modules/M/M2/cards.json: M2-c370", "FAIL",
     "M2-c370 is graded T (cards.json, object for M2-c370). Its answer gives the minimizing steps 1.8e-8 and 6.3e-6, which depend on the assumed delta = 2.22e-16 and on the approximations M_2 ~ e and M_3 ~ e (L24.html:136 says these are assumed). A T grade needs a proof; the numbers are arithmetic on assumed inputs. At the previous pin (c737272) the same card was graded C; the round-2 basis change kept the T and so over-grades it. The grade was moved up from C to T in a007712. Fix: set grade to C with basis 'Propositions 4.2 and 4.3 (T, formulas) evaluated at the assumed delta = 2.22e-16 and M_2 ~ M_3 ~ e (Lab 1 hypothesis); not measured'. The rest of L24's cards PASS (c358-c365, c367, c368, c371-c373, c375, c387, c405)."),
    ("CARD-scan-dup", "full scan for duplicate cards and near-duplicates", "course/modules/M/M2/cards.json", "PASS",
     f"{R('cards_dup_scan.out')}: no duplicate ids; the near-duplicate fronts in the slice ask different things (P' vs P''; first vs second-order errors; Assumption 1.1 vs 4.1)."),
    ("L24-prop-3.1-hypothesis", "Proposition 3.1 hypothesis (f twice differentiable on an interval containing [x,x+h]; f'' bounded by M2)", "L24.html:74, 107, 112", "PASS",
     "Statement and proof use exactly these hypotheses; the Lagrange form of order one needs two derivatives on the open interval (L08 Theorem 2.1)."),
    ("L24-prop-3.2-hypothesis", "Proposition 3.2 hypothesis (three times differentiable on [x-h,x+h]; f''' bounded by M3)", "L24.html:84, 117, 122", "PASS",
     "Statement, proof and card M2-c361 agree; the Lagrange expansion of order two needs three derivatives."),
    ("L24-simulated-label", "SIMULATED label of the L24 lab", "L24.html:136; tests/labs/M2/lab-M2-L24-1.py:3", "PASS",
     "Label present (L24.html:136: 'SIMULATED: both functions are test functions chosen for this lab, not market data')."),
    ("L23-P3-order", "L23 proof problem P3 and its use of the first-order remainder", "L23.html:339-345 (proof-3)", "PASS",
     "P3 proves Proposition 3.3 from Lagrange order one (1/2 P''(theta) Delta^2 >= 0 since P'' > 0); the statement uses only Proposition 2.1 and Taylor's theorem as required; consistent with Proposition 3.3."),
    ("L24-cards", "L24 cards M2-c358..c375, c387, c405 read in full", "course/modules/M/M2/cards.json", "PASS",
     f"Read in full ({R('cards_L22_L24.jsonl')}). M2-c375 is correct (numerator error at most 2 delta). Only c370 fails (CARD-L24)."),
    ("CARDS-dup", "duplicate cards across the deck", "course/modules/M/M2/cards.json", "PASS",
     f"{R('cards_dup_scan.out')}: 394 distinct ids; the slice has no duplicate fronts or backs."),
    ("FWD-L23-lab-prediction", "forward reference in the L23 lab prediction (Proposition 3.2 named before it is stated)", "L23.html:90 (lab hypothesis), 242 (Proposition 3.2)", "PASS",
     "The lab hypothesis predicts the sign of the remainder by naming Proposition 3.2, stated later in the same lesson. This is a result cited as a prediction, not a concept used before it is defined; no undefined term is involved. Recorded for the architect; not a defect under the stated rules."),
]

new_rows = [r for r in rows]
out_rows = []
for rid, check, loc, status, evidence in new_rows:
    row = {"id": rid, "check": check, "location": loc, "status": status, "evidence": evidence}
    if status != "PASS":
        fixes = {
            "DAG-links": "L22: add gradient (Lesson L17) and Hessian (Lesson L19) to the Uses row (L22.html:37) and link the first use in R2 (L22.html:374-376): <a class=\"concept\" data-concept=\"gradient\" href=\"L17.html#def-gradient\">gradient</a> and <a class=\"concept\" data-concept=\"hessian\" href=\"L19.html#def-hessian\">Hessian</a>. L23: add implicit-function theorem (L21) to the Uses row (L23.html:37) and link it in R1 (L23.html:377-379) as href=\"L21.html#def-implicit-function-theorem\".",
            "MATH-L24-canon-bullet3": "L24.html:252: replace 'bounds the error of the computed difference f~(x+h) - f~(x)' with 'bounds the error of the computed quotient (f~(x+h) - f~(x))/h; the computed difference itself is off by at most 2 delta'.",
            "CARD-L24": "cards.json, id M2-c370: set \"grade\" to \"C\" and \"basis\" to \"Propositions 4.2 and 4.3 (T, formulas) evaluated at the assumed delta = 2.22e-16 and M_2 ~ M_3 ~ e (Lab 1 hypothesis); not measured\". Keep the front and back, which state the assumptions.",
        }
        row["fix"] = fixes[rid]
    out_rows.append(row)

frag = {
    "unit": "M2",
    "slice": "d2",
    "round": 3,
    "verifier": "Haiku 5.5 independent verifier, slice d2 (L22, L23, L24 and lab twins), round 3; did not build M2; full read, no carry-forward",
    "pin": "a007712f",
    "base": "c737272f (round-2 pin); slice delta c737272..a007712: L23.html (why-it-matters, Example in Section 1 lab text, Section 4 bullet, E3 solution, interpretation), L24.html (lab hypothesis, lab docstring-text, interpretation, canon bullet 3), tests/labs/M2/lab-M2-L23-1.py and lab-M2-L24-1.py docstrings, cards.json (c351, c353, c354, c370 regraded C->T, c407 added); plans/M2-build-plan.md (gate command text; not a slice file)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyD3-M2-d2",
    "scratch": "/Users/billyribeiro/.fanout/wt/verifyD3-M2-d2/ledgers/M2/scripts/M2-d2-r3",
    "verified_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
    "verdict": "FAIL",
    "rows": out_rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Full verification of L22, L23, L24 and their three twins, every sentence read, every card read (56 cards: 15 L22, 24 L23, 17 L24), no carry-forward; every round-2 row id kept and re-verified.",
        "Round-2 FAIL rows LAB-L23, LAB-L24 and CARD-L23 are PASS now (docstrings and card grades fixed). CARD-L24 is FAIL again: M2-c370 was C at c737272 and was raised to T in a007712 while its assumed inputs are unchanged.",
        "New FAIL: MATH-L24-canon-bullet3 (L24.html:252 misstates the round-off bound; card M2-c375 is right).",
        "No grader in this slice, so mutation testing does not apply (plan 5.1 covers the project); mutants is empty by ruling.",
        "Observation, not a finding: L22 Problem R2 and L24 Problem R3 name Lesson L14 and L17/L19 as places where a concept is treated. R3 names a lesson as a pointer and is not a use; R2 uses the gradient and the Hessian and is listed under DAG-links.",
        "Observation, not a finding: L22 Lab 1 Part B maximizes x(a-x) over [0,a] (nonnegative x and y), while the lesson calls Part B 'the constrained problem of Example 2.2' whose domain is J = (0, infinity). The maximizer a/2 and the value a^2/4 agree on both sets; the lab's own docstring states the restriction.",
        "Observation: L22 lab prints a 'reduced F_a' column that the page's interpretation does not describe; the printed value is x^ (0.5, 1.0, 1.5). Not a false claim.",
        "Observation: E2 solution in L24 attributes the 2 delta/h bound to Definition 4.1; it follows from Definition 4.1 by the argument of Proposition 4.2's proof (L24.html:112).",
        "Not checked: live Crossref or Open Library lookups beyond tools/verify_refs.py (the two M2 keys are cited only as registry keys, with no locator); no screenshot of the rendered pages (page_smoke only, no visual diff); the full pytest suite, render_curriculum, build_site --check and fetch_data --check (no curriculum, site-data, or market input changed in this slice); hours were not re-estimated (architect ruling, plan Q1).",
    ],
    "summary": "M2-d2 round 3: verdict FAIL. 57 rows: 54 PASS, 3 FAIL. FAIL: MATH-L24-canon-bullet3 (L24.html:252, round-off bound stated for the difference instead of the quotient), DAG-links (L22 R2 and L23 R1 use gradient, Hessian and implicit-function theorem without Uses entries or links), CARD-L24 (M2-c370 over-graded T with assumed inputs; was C at c737272). All gates PASS on a007712: check_pages, check_dag, check_projects, run_labs for L22-L24, twins under python -I -W error (stderr empty), expected blocks equal stdout, page_smoke, ruff, mypy, test_labs, test_page_checks, test_run_labs, verify_refs offline and live M2.",
}

problems = []
for r in out_rows:
    for f in ("id", "check", "location", "status", "evidence"):
        if not str(r.get(f, "")).strip():
            problems.append((r["id"], f))
    if r["status"] != "PASS" and not r.get("fix"):
        problems.append((r["id"], "fix"))
print("rows", len(out_rows), "PASS", sum(r["status"] == "PASS" for r in out_rows), "FAIL", sum(r["status"] == "FAIL" for r in out_rows))
print("missing fields:", problems)
Path("ledgers/M2/M2-d2.json").write_text(json.dumps(frag, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
