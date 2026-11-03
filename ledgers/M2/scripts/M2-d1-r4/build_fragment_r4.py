"""Writes the round-4 verifier fragment for M2 slice d1 (ledgers/M2/M2-d1.json). Standard library only."""
import json
from pathlib import Path

S = "ledgers/M2/scripts/M2-d1-r4/"
SCRIPT = S + "build_fragment_r4.py"
rows = []

def row(rid, check, location, evidence, status="PASS"):
    rows.append({"id": rid, "check": check, "location": location, "status": status, "evidence": evidence})

# ---- gates (run on pin 4eb6788f in this round)
row("G-check-pages", "2.9 structure (gate)", "tools/check_pages.py --unit M2",
    S + "check_pages.out: 'check_pages M2: PASS', exit 0.")
row("G-check-dag", "2.9 DAG (gate)", "tools/check_dag.py --unit M2", S + "check_dag.out: 'check_dag M2: PASS', exit 0.")
row("G-check-projects", "2.6 projects (gate)", "tools/check_projects.py --unit M2",
    S + "check_projects.out: 'check_projects M2: PASS', exit 0. The M2 project page is outside this slice.")
row("G-run-labs", "2.5 labs (gate)", "tools/run_labs.py --unit M2", S + "run_labs_M2.out: 'run_labs M2: PASS (27/27)', exit 0; includes lab-M2-L19-1, L20-1, L21-1.")
row("G-twins-isolated", "2.5 labs: twin alone under python -I -W error", "tests/labs/M2/lab-M2-L19-1.py, lab-M2-L20-1.py, lab-M2-L21-1.py",
    S + "twin_L19.out, twin_L20.out, twin_L21.out: each run as 'python -I -W error <twin>', exit 0 (stdout ends with the last printed line, then 'exit 0'); twin_L*.err are 0 bytes.")
row("G-page-vs-twin", "2.5 labs: page code equals twin; expected equals output", "course/modules/M/M2/L19.html:128-249, L20.html:99-188, L21.html:108-183",
    S + "page_vs_twin.py (run with -I) -> page_vs_twin.out: L19 code_equals_twin True (112 lines), expected_equals_output_exact True; L20 True (82), True; L21 True (71), True.")
row("G-ruff-check-format", "2.5 / CLAUDE.md gate (ruff)", "tests/labs/M2, course/modules/M/M2/grader",
    S + "ruff_check.out: 'All checks passed!', exit 0; ruff_format.out: '27 files already formatted', exit 0.")
row("G-mypy-twins", "CLAUDE.md gate (mypy strict, twins)", "tests/labs/M2/lab-M2-L19-1.py, L20-1, L21-1",
    S + "mypy_twins.out: 'Success: no issues found in 3 source files', exit 0.")
row("G-mypy-labs-M2", "CLAUDE.md gate (mypy, tests/labs/M2)", "tests/labs/M2", S + "mypy_labs_M2.out: 'Success: no issues found in 27 source files', exit 0.")
row("G-mypy-repo", "CLAUDE.md gate (mypy, whole repository)", "repository", S + "mypy_repo.out: 'Success: no issues found in 331 source files', exit 0.")
row("G-page-smoke-L19-L21", "2.5 / 2.9 Pyodide, console, math, 360 px (page_smoke, pages alone)", "tools/page_smoke.py --unit M2 --pages L19 L20 L21",
    S + "page_smoke_L19-21.out: L19, L20, L21 each PASS (lab runtime 0.0 s, boot 1.1 s); 'page_smoke M2: PASS', exit 0.")
row("G-pytest-labs-M2", "CLAUDE.md gate (pytest, labs)", "tests/test_labs.py -k M2", S + "pytest_M2_labs.out: all selected tests passed, exit 0.")
row("G-pytest-page-checks", "CLAUDE.md gate (pytest, page checks)", "tests/test_page_checks.py", S + "pytest_page_checks.out: all passed, exit 0.")
row("G-verify-refs-offline", "2.1 registry (offline)", "tools/verify_refs.py --offline", S + "verify_refs_offline.out: 'offline integrity: 560 entries, 0 problems', exit 0.")
row("G-verify-refs-live-M2", "2.1 registry (live, unit M2)", "tools/verify_refs.py --unit M2",
    S + "verify_refs_unit_M2_live.out: 'live re-verification of M2: 2 of 560 entries, 0 problems', exit 0.")
row("G-run-graders-M2", "2.6 grader gate (run for completeness)", "tools/run_graders.py --unit M2 --seeds 0-49",
    S + "run_graders_M2.out: 'run_graders M2: PASS (reference 50/50 seeds, slowest 0.2 s)', exit 0. This slice holds no grader.")
row("REF-openlibrary-M2", "2.1 attribution: registry keys used by the three pages", "references/references.json keys spivak2008calculus, hubbard2015vector; course/modules/M/M2/L19.html:484, L20.html:427, L21.html:420",
    "Plain curl (HTTP 200, no access control) to https://openlibrary.org/books/OL28292750M.json and .../OL35954342M.json, saved as " + S + "openlibrary_spivak.json and " + S + "openlibrary_hubbard.json. Spivak: title 'Calculus', 2008, 'Publish or Perish, inc', edition 'Fourth Edition', ISBN 9780914098911. Hubbard: 'Vector Calculus, Linear Algebra, and Differential Forms', 2015, 'Matrix Editions', ISBN 9780971576681. The pages name them as the curriculum's source strings (curriculum/01-foundations.yaml:145-147; registry source_strings) and attribute no passage to either (L19.html:484 'No passage or theorem locator ... has been confirmed'). The Hubbard subtitle 'A Unified Approach' is omitted from the prose name, as in the curriculum's own source string; accepted as a name, not a bibliographic claim.")

# ---- numbers (re-derived this round with my own script)
row("NUM-L19", "2.2 numbers: L19 prose and lab values", "course/modules/M/M2/L19.html:55-250, 268, 272, 341, 348, 355, 392-395",
    S + "rederive_r4.py (run -I) -> rederive_r4.out: closed form f_xx=0.412180, f_xy=2.148721, f_yy=1.000000; e^0.5/4=0.41218, e^0.5+0.5=2.14872; d^T H d=-1.27439 (page -1.274, L19.html:348); g'''(0) analytic 0.96854 and numeric 0.96852 (page 0.969, L19.html:355); central-difference worst error 2.261e-11 and asymmetry 1.943e-11 (page 2.26e-11, 1.94e-11); first/second-order ratios 3.9509 7.8836, 3.9750 7.9429, 3.9874 7.9717 (match L19.html:247-249). Lab output agrees exactly (twin_L19.out).")
row("NUM-L20", "2.2 numbers: L20 prose and lab values", "course/modules/M/M2/L20.html:63-71, 82-88, 98-107, 182-188, 193-202, 209-212, 233, 296-312, 349-352, 376-411",
    S + "rederive_r4.out: exact Fraction midpoint sums in both orders equal 5/3-1/(6n^2) for n in {1,2,3,4,5,8,16,32,64} (True); n=1 value 3/2, n=2 value 13/8 (hand-checked: 3.25/2); odd-square identity for n<=200 True; P1 algebra identity for n<500 True; Example 3.1 antiderivative derivatives match the integrand at 2000 random points (0 failures). Expected block equals twin output exactly (page_vs_twin.out). Integrals in Theorem 1.2 and Proposition 2.2: 5/3, 1/2, 1/3, 2 (hand-checked).")
row("NUM-L21", "2.2 numbers: L21 prose and lab values", "course/modules/M/M2/L21.html:97, 107, 184, 265, 290, 306-322, 333-336, 362-411",
    S + "rederive_r4.py with an independent bisection root finder: roots 0.9168754789, 0.8351223485, 0.6823278038, 0.4533976515 and formula values -0.3307653158, -0.3221564676, -0.2846930800, -0.1732702316 reproduce the page and twin_L21.out; F_y 2.771982, 2.592288, 2.396714, 2.616708 (page 'between about 2.4 and 2.8'). Formula-vs-central-difference differences from bisection roots are 1e-14 to 1e-11 (round-off-sensitive); the printed 6.2e-13, 5.2e-14, 3.7e-12, 3.9e-12 are the Newton twin's own run (twin_L21.out), which the page quotes. Circle slope -0.75 and -F_x/F_y -0.75 (hand-checked, L21.html:97).")

# ---- DELTA and structure
row("DELTA-r4-slice", "0 delta since previous pin (read every hunk)", "course/modules/M/M2/L19.html, L20.html, L21.html, cards.json; cross-refs in L22.html, L23.html, L24.html, L16.html",
    S + "delta_slice.diff (git diff a007712f..4eb6788f for the slice; 469 lines). Every hunk read. Changes: prefixes 'Assuming Assumption 2.1 of Lesson L06' / 'Assuming Assumption 1.2 and Assumption 2.1' added to the conditional statements, the Theorem 1.2/Proposition 2.2/Example 3.1 statements, and the solutions; rewrites of L19 references and L21 E3; card backs for M2-c296, c298, c302, c304, c305, c307 and c319 (cards.json hunks at lines 2072-2229). Lab twins L19-L21 and the hub are byte-identical to the previous pin (git diff empty). All changed statements were re-verified from scratch (rows below).")
row("STRUCT-L19", "2.9 structure: L19 template sections", "course/modules/M/M2/L19.html",
    S + "check_pages.out PASS. Read: data-hours=10 (L19.html:2); why-it-matters (L19.html:51); sections 1-3 with Definition, Theorem, Proof, Example, Remark, Proposition; Lab 1 inline (:125-251); canon-breaks (:253-261); three misconceptions (:263-279); problem set with three problems in each tier and worked solutions (:281-383); key-results table with four T rows (:386-399); retrieval quiz with 10 items (:401-480); references (:482-486); lesson nav (:489-492).")
row("STRUCT-L20", "2.9 structure: L20 template sections", "course/modules/M/M2/L20.html",
    S + "check_pages.out PASS. Read: data-hours=10 (:2); sections 1-3; Lab 1 inline (:96-190); canon-breaks (:204-218); three misconceptions (:220-236); three problems per tier with solutions (:238-341); key-results table with four T rows (:343-356); quiz with 8 items (:358-423); references (:425-429).")
row("STRUCT-L21", "2.9 structure: L21 template sections", "course/modules/M/M2/L21.html",
    S + "check_pages.out PASS. Read: data-hours=10 (:2); sections 1-3; Lab 1 inline (:105-185); canon-breaks (:187-203); three misconceptions (:205-221); three problems per tier with solutions (:223-326); key-results table with three T rows (:328-340); quiz with 9 items (:342-416); references (:418-422).")
row("PROSE-banned-and-process", "2.9 banned phrases (BUILDER_RULES 1.3-1.4) and process words", "course/modules/M/M2/L19.html, L20.html, L21.html, cards.json (L19-L21 cards)",
    S + "scan_r4.py -> scan_r4.out: 0 hits for TODO, TBD, lorem, for brevity, details omitted, beyond the scope, left as an exercise, you can add more, it is important to note, studies show, experts agree, it is well known, obviously, clearly, it can be shown. No process words in learner text.")
row("SCOPE-words", "2.9 / rule 4 scope words (only, all, always, every, any, same, drives, exactly; smooth, fast, small, typically)", "course/modules/M/M2/L21.html:297 (E3 solution); scan of L19-L21",
    "Round-3 FAIL re-verified and fixed. L21.html:297 now reads 'Hence, assuming Assumption 1.2 and Assumption 2.1 of Lesson L06, for each x in I with x > 0, the Newton root equals g(x).' The step F_y = 3y^2 + x > 0 for x > 0 (every real y) gives one real zero, so the Newton root is the zero in J (argument checked by hand). Remaining scope words: L19.html:250 'since f is smooth' (f = e^x y + x y^2 is C-infinity), L19.html:380 'small steps' (argument uses omega(|s|) -> 0), L20.html:189 'these grids only', L21.html:184 'at four points'; each is backed by a computation or a stated limit on the claim. L20.html:214 bullet heading 'Order matters without a hypothesis' is read as 'order can matter when the hypothesis fails'; the example's integrand violates the boundedness hypothesis; accepted.")

# ---- math
row("MATH-L19-thm2.1", "2.4 math: Theorem 2.1 (mixed partials) and proof", "course/modules/M/M2/L19.html:71-84",
    "Hypotheses stated (:73: f_x, f_y, f_xy on N; f_xy continuous at p) and Assumption 2.1 named. Proof re-read line by line: Step 1 two MVT applications give Delta = h k f_xy(xi, eta) with |xi-a|<=|h|, |eta-b|<=|k| (L06 Theorem 2.3 is the MVT, L06.html read); Step 2 bound uses the disc of radius delta/sqrt(2) < delta; Step 3 letting k->0 is legitimate because f_y exists on N. Conclusion is the standard Schwarz/Young statement with the hypotheses it needs.")
row("MATH-L19-ex2.2", "2.4 math: Example 2.2 (counterexample)", "course/modules/M/M2/L19.html:87-89",
    S + "rederive_r4.out: f_x(0,y) = -y (numeric -0.300000 at y=0.3), f_y(x,0) = x (0.400000 at x=0.4); f_xy(t,t) ~ 0, f_xy(t,0) ~ 1 (numeric); hand algebra f_x = y M/D with M = x^4+4x^2y^2-y^4, D = (x^2+y^2)^2 (numerator (3x^2-y^2)(x^2+y^2)-2x(x^3-xy^2) = x^4+4x^2y^2-y^4). Conclusion f_xy(0,0) = -1 != 1 = f_yx(0,0) correct; continuity hypothesis indeed fails at the origin.")
row("MATH-L19-thm3.1", "2.4 math: Theorem 3.1 (second-order expansion with remainder) and proof", "course/modules/M/M2/L19.html:94-108",
    "Re-derived: g'' = h^T H(p+th) h (chain rule, convention f_xy = d_y d_x f matches Definition 1.1); phi(0)=phi'(0)=0; two MVT steps give phi(1) = s1 phi''(s2); |h^T M h| <= (|h1|+|h2|)^2 max|M_ij| <= 2|h|^2 max|M_ij| (verified (|h1|+|h2|)^2 <= 2(h1^2+h2^2)); bound 2|h|^2 omega(|h|) follows. Hypotheses (twice differentiable on the disc, H continuous at p, Assumption 2.1) stated in the statement at :96-99.")
row("MATH-L19-rem3.2", "2.4 math: Remark 3.2", "course/modules/M/M2/L19.html:110-113",
    "Coefficient of s^2 = (1/2)(d1^2 f_xx + d1 d2 (f_xy + f_yx) + d2^2 f_yy) re-derived; the term d1 d2 f_xy when the mixed partials agree is correct. Statement begins 'Assuming Assumption 2.1 of Lesson L06' (:112).")
row("MATH-L19-prop3.3", "2.4 math: Proposition 3.3 (cubic term) and proof", "course/modules/M/M2/L19.html:116-123",
    "Lagrange form of Taylor (L08 Theorem 2.1, L08.html read: hypotheses (n+1) times differentiable on an open interval; n=2 here) gives E(s) = (1/6) g'''(theta s) s^3; continuity of g''' at 0 gives (1/6) g'''(0) s^3 + o(s^3); ratio E(s)/E(s/2) -> (1/6)/(1/48) = 8. Re-derived; statement begins 'Assuming Assumption 2.1 of Lesson L06' (:117). The statement's 'interval containing [0,s]' is adequate for the Lagrange form on a slightly larger open interval.")
row("MATH-L19-key-results-and-refs", "2.3/2.4 key-results rows and references paragraph", "course/modules/M/M2/L19.html:392-395, 484",
    "Four T rows (Theorem 2.1 'Proved in §2'; Example 2.2 'Computed in Example 2.2'; Theorem 3.1 'Proved in §3'; Proposition 3.3 'Proved in §3 from Lesson L08'). Each conditional row begins 'Assuming Assumption 2.1 of Lesson L06'. Grades re-derived against BLUEPRINT 3 (theorem with proof on page).")
row("L19-example-2.2-discontinuity", "2.4 math: Example 2.2 and its key-results row", "course/modules/M/M2/L19.html:87-89, 393", "Same evidence as MATH-L19-ex2.2 (rederive_r4.out); key-results row 2 (:393) T and matches the example.")
row("L19-lab-1-prose-and-docstring", "2.5 labs: docstring and prose match code and output", "course/modules/M/M2/L19.html:127-136, 250; tests/labs/M2/lab-M2-L19-1.py:1-12",
    "Docstring: Part A prints gradient, Hessian, largest central-difference error and asymmetry; Part B prints first- and second-order errors at s, s/2, s/4, s/8 with ratios; standard library only (code lines 141-148 read). The page's description and the twin output (twin_L19.out) agree. Interpretation (:250) states only what is printed.")
row("L19-theorem-2.1-hypothesis-count", "2.4 statement hypotheses vs prose", "course/modules/M/M2/L19.html:255, 73", "L19.html:255 says 'two hypotheses on f, besides the assumed Assumption 2.1', and the statement at :73 lists exactly two (existence of f_x, f_y and f_xy on N; continuity of f_xy at p). Consistent.")
row("L19-solutions-omit-assumption-2.1", "2.4 conditional statements in solutions and quiz name the assumption", "course/modules/M/M2/L19.html:268, 272, 276, 298, 305, 323, 348, 355, 373, 380, 435, 449, 472",
    "Every solution, misconception and quiz explanation that applies Theorem 2.1, Theorem 3.1, Remark 3.2 or Proposition 3.3 begins its conditional sentence with 'Assuming Assumption 2.1 of Lesson L06' (read at each line).")
row("L19-quiz-Q9-circular-answer", "2.9 quiz item correctness", "course/modules/M/M2/L19.html:466-472",
    "Marked answer 'It is a term of the quadratic form, non-zero when f_xy(p) != 0' is correct; distractors wrong; explanation correct (the cross term vanishes for every h only when f_xy(p) = 0). Other numeric answers re-derived: f_xy of x^2 y = 2 (L19.html:424), g''(0) = 2 (:438), E(s)/E(s/2) -> 8 (:443-449), f_xy of x^3 y at (2,1) = 12 (:452), f_xx of e^x y at (0,2) = 2 (:475).")
row("L19-refs-every-graded-result", "2.9 / 2.4 references paragraph: every graded result sentence", "course/modules/M/M2/L19.html:484",
    "Round-3 FAIL re-verified and fixed. The sentence now reads: 'Theorems 2.1 and 3.1 and Proposition 3.3 are proved on the page from the mean value theorem (Lesson L06, Theorem 2.3) or the Lagrange form of Taylor's theorem (Lesson L08, Theorem 2.1). Example 2.2 is checked by direct computation of limits and uses neither.' L06 Theorem 2.3 is the mean value theorem and L08 Theorem 2.1 the Lagrange form (both read). Example 2.2 uses neither (its proof is limits and rational functions). Correct.")
row("L19-lab1-prop3.3-assumption", "2.4 / 2.5 lab hypothesis cites Proposition 3.3 with its assumption", "course/modules/M/M2/L19.html:127",
    "Round-3 FAIL re-verified and fixed. The prediction now reads 'Assuming Assumption 2.1 of Lesson L06, the second-order error should fall by a factor near 8 if the third derivative g'''(0) ... is non-zero, by Proposition 3.3.' The interpretation at :250 also names the assumption. The predictions are checked against twin_L19.out (ratios 7.8836 to 7.9717).")
row("LAB-L19-1", "2.5 lab: runs, hypotheses, interpretation", "course/modules/M/M2/L19.html:125-251; tests/labs/M2/lab-M2-L19-1.py",
    "Runs under python -I -W error (twin_L19.out, exit 0); predictions (Hessian entries 0.41218, 2.14872, 1; error <= 1e-10; first-order ratio near 4; second-order ratio near 8 under g'''(0) != 0) are checked against the printed output (g'''(0) = 0.96854 re-derived, so the 8 is expected). Interpretation does not overreach: the lab does not compute g'''(0) (L19.html:127, :250).")

# ---- L20
row("MATH-L20-thm1.2", "2.4 math: Theorem 1.2 and proof (round-3 FAIL, FTC assumption)", "course/modules/M/M2/L20.html:62-72; key-results row 1 :349; card M2-c296",
    "Round-3 FAIL re-verified and fixed. The statement now begins 'Assuming Assumption 2.1 of Lesson L06 (the extreme value theorem),'. The proof's values 1/2, 1/3, 2 are FTC evaluations (L10 Theorem 2.1, read: requires Assumption 2.1 of L06 and integrability), which the statement's assumption covers. The monotone input is L09 Corollary 2.3 (read: for monotone f and any Riemann sum R, |R - int f| <= delta |f(b)-f(a)|), so convergence holds for every choice of tags as mesh -> 0. Product splitting S = (sum xi dx)(sum eta dy) + (sum xi^2 dx)(sum dy) re-derived; limit 5/3 correct.")
row("MATH-L20-prop2.2", "2.4 math: Proposition 2.2 and proof (round-3 FAIL, FTC assumption and integrability)", "course/modules/M/M2/L20.html:82-88; key-results row 2 :350; card M2-c298",
    "Round-3 FAIL re-verified and fixed. The statement begins 'Assuming Assumption 2.1 of Lesson L06 (the extreme value theorem),'. The proof now states that each one-variable integrand is nondecreasing for each fixed value of the other variable (verified: d/dx(xy+x^2) = y+2x >= 0, d/dy = x >= 0 on the rectangle), hence integrable by L09 Theorem 2.2 (read: monotone implies integrable), before the FTC step (L10 Theorem 2.1). Both iterated integrals equal 5/3 (both orders re-derived by hand: 2x+2x^2 and y/2+1/3).")
row("MATH-L20-prop2.4", "2.4 math: Proposition 2.4 and proof", "course/modules/M/M2/L20.html:193-202",
    "Re-derived: sum of midpoints x_i = (2i+1)/(2n), sum(2i+1) = n^2, so sum x_i/n = 1/2; sum(2i+1)^2 = n(4n^2-1)/3 by induction (n(4n^2-1) + 3(2n+1)^2 = 4n^3+12n^2+11n+3 = (n+1)(4(n+1)^2-1)), so sum x_i^2/n = 1/3 - 1/(12n^2); the y-direction midpoint rule is exact for linear y (sums 2 and 2); both orders give 5/3 - 1/(6n^2). Exact Fraction check in rederive_r4.out for n up to 64. No FTC or theorem needed, so grade T is correct without an assumption.")
row("MATH-L20-ex3.1-claims", "2.4 math: Example 3.1 (round-3 FAIL, FTC and Assumption 3.1)", "course/modules/M/M2/L20.html:209-212, 352; card M2-c302",
    "Round-3 FAIL re-verified and fixed. The example begins 'Assuming Assumption 2.1 of Lesson L06 (through the FTC, Lesson L10, Theorem 2.1 ...) and Assumption 3.1 (inverse tangent, which this page does not prove)'. Re-derived: d/dy[y/(x^2+y^2)] = (x^2-y^2)/(x^2+y^2)^2, so int_0^1 f dy = 1/(1+x^2); d/dx[-x/(x^2+y^2)] = same integrand, so int_0^1 f dx = -1/(1+y^2); outer integrals pi/4 and -pi/4 (arctan facts, Assumption 3.1). Numeric antiderivative check passes (rederive_r4.out). Unboundedness sentence (:212) now complete: 1/t^2 grows without bound as t -> 0. Key-results row 4 (:352) names both assumptions.")
row("MATH-L20-problems-and-remarks", "2.4 / 2.9 Remark 2.3, misconceptions, problem solutions", "course/modules/M/M2/L20.html:91-94, 220-236, 243-337",
    "Remark 2.3 ungraded and says so (:93). Misconceptions 1-3 correct (Example 3.1 pi/4 vs -pi/4; product-of-integrals misconception 1/2*2 + 1/3*2; midpoint error -1/(6n^2) is the square of the cell width; printed errors -1/6, -1/24, -1/96). Solutions M1 (3, 3), M2 (2/3, 2/3), M3 (3/2, -1/6), P1 induction, P2 midpoint exactness, P3 product form, E1-E3 (ratios of 1/4), R1-R3 (R3: f(x)=x, tag 1 gives 1, midpoint 1/2) re-derived; each conditional solution names Assumption 2.1 where needed.")
row("LAB-L20-1", "2.5 lab: runs, hypothesis, interpretation", "course/modules/M/M2/L20.html:96-190; tests/labs/M2/lab-M2-L20-1.py",
    "Runs under python -I -W error (twin_L20.out, exit 0). Predicted 3/2 (n=1) and 13/8 (n=2) and 5/3 - 1/(6n^2) match printed lines (:182-188; hand-checked n=2 sum 3.25/2 = 13/8). Interpretation: 'six values of n, up to 32' (code line 166: n in (1,2,4,8,16,32)) and 'identity up to 50' (code line 177) are correct. The lab does not invoke any theorem equating iterated integrals (docstring lines 106-107).")

# ---- L21
row("MATH-L21-thm1.3", "2.4 math: Theorem 1.3 (implicit-function theorem) and proof", "course/modules/M/M2/L21.html:63-81",
    "Assumption 1.2 (IVT, L21.html:63-64) matches the standard statement. Re-derived step by step: WLOG F_y(x0,y0)>0; rectangle R in U with F_y>0; F(x0,y0-c)<0<F(x0,y0+c); a1 with the same signs for |x-x0|<a1; I x J in R; unique zero by IVT and strict monotonicity; continuity of g by monotonicity and continuity of F; differentiability by MVT in x and in y, the identity 0 = h F_x(xi,y2) + (y2-y1) F_y(x1,eta), and continuity of F_x, F_y; g' = -F_x/F_y continuous. Statement names Assumption 1.2 and 2.1 (:68-69).")
row("MATH-L21-thm2.1", "2.4 math: Theorem 2.1 (slope formula) and proof", "course/modules/M/M2/L21.html:85-93", "Chain rule on F(x, g(x)) = 0 gives F_x + F_y g' = 0; division by F_y != 0 on I x J (Theorem 1.3). Statement names both assumptions (:87).")
row("MATH-L21-examples", "2.4 math: Examples 2.2, 3.1, 3.2", "course/modules/M/M2/L21.html:96-103, 190-197",
    "Example 2.2: F_y = 1.6, g' = -x/sqrt(1-x^2) = -0.75 at 0.6, -F_x/F_y = -1.2/1.6 = -0.75 (hand-checked). Example 3.1: at (1,0) F_y = 0, F_x = 2, dx/dy = -y/sqrt(1-y^2) = 0 at y=0 (hand-checked). Example 3.2: x^2+g^2 > 0 for x != 0, no g with g(0)=0 (hand-checked; I open and contains 0).")
row("MATH-L21-misconceptions", "2.4 / 2.9 misconception with a conditional result (round-3 FAIL)", "course/modules/M/M2/L21.html:209-218",
    "Round-3 FAIL re-verified and fixed. L21.html:214 now begins 'Assuming Assumption 1.2 and Assumption 2.1 of Lesson L06, the chain rule in Theorem 2.1 gives F_x + F_y g' = 0'. Numbers re-derived: F_y/F_x = 1.6/1.2 = 4/3; slope -0.75. Misconceptions 1 and 3 correct and conditional where they use the theorem (L21.html:218 names both assumptions).")
row("L21-sec3-bullet-thm1.3-assumption", "2.4 bullet cites a conditional result (round-3 FAIL)", "course/modules/M/M2/L21.html:199",
    "Round-3 FAIL re-verified and fixed. The bullet now reads 'Assuming Assumption 1.2 and Assumption 2.1 of Lesson L06, Theorem 1.3 gives one branch near each point with F_y != 0.'")
row("MATH-L21-problems", "2.4 / 2.9 problem solutions and remarks", "course/modules/M/M2/L21.html:228-326",
    "Mechanics M1 (-1), M2 (-1), M3 (-1, y = 2-e^x) re-derived; P1 -a/b; P2 derivative -x/sqrt(1-x^2) equals -F_x/F_y with y>0; P3 no function through origin; E1 sign (negative, from -y/(3y^2+x)); E2 bootstrap (see L21-E2-third-derivative); E3 uniqueness for x>0 (see SCOPE-words); R1 dy/dP0 = 1/P'(y) < 0 (F_{P0} = -1, F_y = P'(y)), re-derived, hypothesis P'(y)<0 named as a hypothesis (:306); R2 ungraded and says so (:315); R3 Taylor remainder bound (1/2) sup|g''| dx^2 by L08 Theorem 2.1 (n=1), correct and conditional (:322).")
row("L21-E2-third-derivative", "2.4 / 2.2 E2 solution: bootstrap and truncation/rounding sizes", "course/modules/M/M2/L21.html:288-291",
    "F polynomial; g C^k => g' = -F_x(x,g)/F_y(x,g) is C^k => g is C^(k+1); induction gives C-infinity (Theorem 1.3, Theorem 2.1 and Assumptions named). Central difference = g' + (h^2/6) g'''(xi) (standard); (1/6)(1e-5)^2 = 1.67e-11 (page 1.7e-11); eps/h = 2.2e-11 (page about 2e-11). Printed 3.9e-12 below that scale; the page says it does not measure either term (correct).")
row("L21-E3-solution-incomplete", "2.4 uniqueness argument (round-3 FAIL, scope)", "course/modules/M/M2/L21.html:297",
    "Round-3 pass row re-verified: the uniqueness argument is given for x > 0 (F_y = 3y^2 + x > 0 for all real y), the page states the printed residuals do not show x in I, and the lab does not compute I or J (lab code lines 120-124 read; I and J are not computed).")
row("LAB-L21-1", "2.5 lab: runs, hypothesis, interpretation", "course/modules/M/M2/L21.html:105-185; tests/labs/M2/lab-M2-L21-1.py",
    "Runs under python -I -W error (twin_L21.out, exit 0). Hypothesis: F = y^3 + xy - 1 (SIMULATED, labelled), Newton from y = 1 (matches root(), code line 144-147), F_x = y, F_y = 3y^2 + x (matches relation_y). Predicted agreement to about 1e-11 holds for the output (max 3.9e-12). Interpretation: four points, F_y between 2.397 and 2.773 ('about 2.4 and 2.8'), residuals at rounding level; claims confined to the lab's four points.")
row("XREF-L21-M2", "2.9 cross references to L19-L21 from other lessons (numbering)", "course/modules/M/M2/L16.html:303; L22.html:88, 369, 460, 466, 473 (L21) and 374, 376 (L19); L23.html:379",
    "L16.html:303 cites L19 Theorem 2.1 (symmetry of mixed partials), which is L19.html:71-73: correct. L22 cites Theorem 1.3 of L21 (lines 88, 369, 466, 473) and its Assumption 1.2 and Assumption 2.1 of L06 (matching L21.html:63, 67-69), and L19 for the Hessian (L19.html:59, anchor def-hessian exists); L23.html:379 cites Theorem 2.1 of L21 for the slope formula (matches L21.html:85-87) and Assumption 1.2 of L21. No 'Assumption 1.3' or 'Theorem 1.2' of L21 is cited. Numbering of L19, L20 and L21 unchanged between pins.")
row("SIMULATED-labels", "2.8 SIMULATED labels for generated data", "course/modules/M/M2/L19.html:127, 130; L20.html:98, 101; L21.html:107, 110; cards.json c287, c288, c289, c294, c301, c313, c314",
    "Each lab hypothesis labels its function or relation SIMULATED; each docstring repeats the label; no data-files attribute and no figure on these pages; cards that report lab numbers carry a basis field naming Lab 1 and SIMULATED where the function is named (c287, c301, c313, c314).")
row("HOURS-L19-L21", "2.9 hours arithmetic", "course/modules/M/M2/L19.html:2, L20.html:2, L21.html:2; index.html:29",
    "data-hours=10 on each page (eyebrow '10 study hours'); index.html data-hours-lessons=240 and data-hours-project=60 total 300, matching the curriculum figure (plan section 1). Lab durations are under 1 s (page_smoke).")
row("L-mathbb-R", "2.9 / notation: no \\mathbb, \\R used", "course/modules/M/M2/L19.html, L20.html, L21.html, cards.json",
    S + "scan_r4.out: \\mathbb count 0 in each file; \\R count 2 (L19), 1 (L20), 4 (L21); no \\mathbb in cards (L19-L21 cards).")
row("NOTATION-L19-L21", "2.4 notation vs notation/notation.json", "course/modules/M/M2/L19.html, L20.html, L21.html",
    S + "scan_r4.out: no math segment uses a registered symbol with another meaning (T, Q, R_f, R^*, R^{e*}, Phi, gamma_3, gamma_4, \\E, \\Prob). Local symbols f, g, F, H, M, D, E(s), R(h), R (rectangle), N (disc), n, m, L, omega, eps, delta are not registered and carry one meaning per lesson.")
row("DAG-L19-L21", "2.9 DAG: prerequisite closure, definitions and uses", "course/modules/M/M2/L19.html, L20.html, L21.html; check_dag.out",
    "check_dag.out PASS. L19 uses partial derivative (L16), gradient (L17), derivative (L04), Taylor's theorem (L08), mean value theorem (L06 prose), all earlier; defines hessian once (def-hessian). L20 uses definite integral (L09), FTC (L10, prose), limit (L01), all earlier; defines multiple-integral once. L21 uses derivative (L04), partial derivative (L16), the Jacobian of L18 in prose (R2), defines implicit-function-theorem once. Later-module concepts appear only as plain prose with no link and no dfn: 'compact' (L19 R3 solution; compactness is M5), 'Newton's method' (L21 lab and E3; newtons-method is M8), per architect rulings Q5-Q7 (plan section 9). Fubini, continuity, Lagrange multiplier, Riemann-Stieltjes, Lebesgue, duration and convexity are not named by these pages (grep).")
row("GRADES-L19-L21", "2.3 grades re-derived against BLUEPRINT 3 (round-3 FAIL, chain of MATH-L20 rows)", "course/modules/M/M2/L19.html:392-395; L20.html:349-352; L21.html:334-336; data-grade spans",
    "Round-3 FAIL re-verified and fixed. Every T claim is a theorem, a proposition or a computed example whose proof is on the page; each conditional T claim names Assumption 2.1 of L06 (EVT), Assumption 1.2 (IVT) or Assumption 3.1 (arctan) in its statement or key-results row. Lab results carry C (cards c287-c289, c301, c313, c314). Re-graded: L19 Theorem 2.1 T, Example 2.2 T, Theorem 3.1 T, Proposition 3.3 T; L20 Theorem 1.2 T, Proposition 2.2 T, Proposition 2.4 T (pure algebra), Example 3.1 T; L21 Theorem 2.1 T, Example 2.2 T, Example 3.2 T.")
row("CARDS-coverage-L19-L21", "2.7 retrieval cards: every definition, theorem, misconception, lab result and assumption has a card", "course/modules/M/M2/cards.json: M2-c280..c294 (L19), c295..c307 and c402 (L20), c308..c322 and c403 (L21)",
    "43 cards read in full for the three lessons. L19: definition c280, examples c281, theorems c282 c284 c286, remark c285, lab c287-c289, misconceptions c292-c294, c291 (Theorem 3.1 no cubic). L20: definition c295, c297; theorem c296; Proposition c298, c300; remark c299; lab c301; Example c302, c303; misconceptions c304-c306; Assumption 3.1 c402. L21: definition c308, theorems c309, c310; examples c311, c317, c318; remark c312; lab c313, c314; c315, c316; misconceptions c320-c322; c319; Assumption 1.2 c403. Ids c283 and c290 are absent (non-sequential ids are not defects, architect ruling 2).")
row("CARDS-dup-scan", "2.7 full scan for duplicate cards", "course/modules/M/M2/cards.json (394 cards)",
    "cards_scan_r4.py -> cards_scan_r4.out: 394 cards, 394 unique ids; one normalised duplicate front pair exists (M2-c342 and M2-c343, both L23, outside this slice); no duplicate among the 43 L19-L21 cards.")
row("CARDS-numbers-in-lesson", "2.7 card numbers appear in their lesson", "course/modules/M/M2/cards.json (L19-L21 cards)",
    "Every number on the 43 cards appears in its lesson or expected block: c287-c289 (L19.html:241-249), c288 (:243-244), c294 (:244), c301 (L20.html:182-184), c313 (L21.html:180-183), c314 (:182), c300 (L20.html:194), c302 (:210-212), c298 (:88), c296 (:71). Checked by reading each card against its lesson.")
row("CARDS-agree-with-text-L19-L21", "2.7 cards agree with the current lesson text (round-3 FAIL, card statements)", "course/modules/M/M2/cards.json (L19-L21 cards)",
    "Round-3 FAIL re-verified and fixed. All 43 cards compared with the current lesson text. c296, c298 and c302 now carry 'Assuming Assumption 2.1 of Lesson 6' or name the assumption; c302 and c307 now include 'and 1/t^2 grows without bound as t decreases to 0'; c305 names the assumption; c310 and c309 match Theorem 2.1 and Theorem 1.3 hypotheses; c319 matches Section 3 (F = y^3 - x, F_y = 0 at origin, graph y = x^(1/3)); c321 and c322 match Misconceptions 2 and 3. No card disagrees with its lesson.")
row("CARDS-L19-hypotheses", "2.7 L19 card hypotheses name the assumption", "course/modules/M/M2/cards.json: M2-c282, c284, c285, c286, c291, c292, c293, c294", "Each conditional back names Assumption 2.1 of Lesson 6 (c282 'Assuming Assumption 2.1'; c284 'Assuming'; c285 'Assuming'; c286 'Assuming'; c291 'Assuming'; c292 'Assuming'; c293 'Assuming'; c294 'Assuming'), matching L19.html:112, 259, 268, 272, 276.")
row("CARDS-L21-hypotheses", "2.7 L21 card hypotheses name the assumption", "course/modules/M/M2/cards.json: M2-c309, c310, c311, c312, c315, c319, c321, c322",
    "Each conditional back names Assumption 1.2 and Assumption 2.1 of Lesson 6 (c309, c310, c311, c312, c319, c321, c322; c315 names both as assumed), matching L21.html:63-69, 87, 102, 189, 214, 218, 322.")
row("CARD-M2-c307-witness", "2.7 card M2-c307 reasoning (round-3 FAIL)", "course/modules/M/M2/cards.json: M2-c307 back",
    "Round-3 FAIL re-verified and fixed. The back reads 'No. For fixed t in (0, 1], f(t, y) tends to 1/t^2 as y decreases to 0, and 1/t^2 grows without bound as t decreases to 0, so f is unbounded on (0, 1]^2 (Section 3).' The unboundedness step is now present and matches L20.html:212.")
row("CARD-M2-c302-witness", "2.7 card M2-c302 reasoning (round-3 FAIL)", "course/modules/M/M2/cards.json: M2-c302 back",
    "Round-3 FAIL re-verified and fixed. The back now ends 'The integrand is unbounded on (0, 1]^2: for fixed t in (0, 1], f(t, y) tends to 1/t^2 as y decreases to 0, and 1/t^2 grows without bound as t decreases to 0.' and names Assumption 2.1 and Assumption 3.1 before the integrals.")
row("CARDS-L20-assumption", "2.7 / 2.3 L20 T cards name the FTC assumption (round-3 FAIL)", "course/modules/M/M2/cards.json: M2-c296, c298, c302, c304, c305",
    "Round-3 FAIL re-verified and fixed. c296 'Assuming Assumption 2.1 of Lesson 6 (the extreme value theorem), it exists and equals 5/3'; c298 'Yes, assuming Assumption 2.1 of Lesson 6'; c302 'Assuming Assumption 2.1 of Lesson 6 (through the fundamental theorem of calculus) and Assumption 3.1'; c304 'No. Assuming Assumption 2.1 of Lesson 6 and Assumption 3.1, Example 3.1 gives pi/4 for one order'; c305 'assuming Assumption 2.1 of Lesson 6'. Matches the lesson statements at L20.html:64, 83, 210, 85-88.")
row("L19-lab1-prop3.3-cards", "2.7 card for the L19 lab numbers (SIMULATED basis)", "course/modules/M/M2/cards.json: M2-c287, c288, c289", "Card numbers equal twin_L19.out and the page expected block (2.26e-11 and 1.94e-11 at L19.html:243-244; ratios at :247-249); basis fields name Lab 1.")

rid = [r["id"] for r in rows]
assert len(rid) == len(set(rid)), "duplicate ids"
frag = {
    "unit": "M2",
    "slice": "d1",
    "round": 4,
    "round_note": "Round 4, slice d1 (L19, L20, L21 and their lab twins). Full re-verification from scratch of every row (no carry-forward): the delta from the round-3 pin a007712 to 4eb6788 for the slice was read in full (" + S + "delta_slice.diff), and all three pages and the 43 cards were read line by line. Previous FAIL rows were re-verified and are PASS now.",
    "verifier": "Haiku 5.5 independent verifier, slice d1 (L19, L20, L21 and their lab twins), round 4",
    "pin": "4eb6788fe3b408bb6d90ac73addc6fb17af47b8b",
    "base": "a007712fdbfc8b4851123f4de76b5310ac5a9e64 (round-3 pin; round-3 fragment /Users/billyribeiro/.fanout/frags/D-M2-d1.round3.json)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyD4-M2-d1",
    "scratch": "/Users/billyribeiro/.fanout/wt/verifyD4-M2-d1/" + S.rstrip("/"),
    "verified_at": "2026-11-03T13:40:00Z",
    "verdict": "PASS",
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Mutants: none. This slice holds no project grader, and lab twins are demonstrations (ruling 9; VERIFIER_RULES 2.6 mutation applies to project graders), so no mutant is owed. ledgers/M2/mutants/ was not touched.",
        "Carry-forward: none. Every row was re-verified on pin 4eb6788 this round; no PASS row was copied from round 3.",
        "Not checked: the Hub, project and grader pages and cards outside L19-L21 (other slices); repo-wide gates (check_pages --all, build_site --check, render_curriculum) are the architect's; no screenshot was viewed (page_smoke checks layout, overflow, text-in-SVG and console, and passed); no Crossref lookup (no DOI in these records; OpenLibrary read by plain curl).",
        "Non-blocking wording notes (PASS): L20.html:214 bullet heading 'Order matters without a hypothesis' could be read more precisely as 'when the boundedness hypothesis fails'; L21.html:192 'Near (1,0) the curve is the graph x = sqrt(1-y^2)' is an explicit computation, needs no theorem.",
        "Scripts: ledgers/M2/scripts/M2-d1-r4/ (check_pages.out, check_dag.out, check_projects.out, run_labs_M2.out, twin_L19/20/21.out and .err, page_vs_twin.py/.out, rederive_r4.py/.out, scan_r4.py/.out, ruff, mypy, pytest, verify_refs, run_graders, openlibrary_*.json, delta_slice.diff, build_fragment_r4.py).",
    ],
    "mutants": [],
    "rows": rows,
    "summary": None,
}
counts = {"pass": sum(r["status"] == "PASS" for r in rows), "fail": sum(r["status"] == "FAIL" for r in rows),
          "unverifiable": sum(r["status"] == "UNVERIFIABLE" for r in rows)}
frag["summary"] = "M2-d1 round 4: %d rows (pass=%d fail=%d unverifiable=%d). Verdict PASS: every gate passes on the pin; every L19-L21 claim re-derived; the four round-3 FAIL groups (FTC assumption in L20 Theorem 1.2, Proposition 2.2 and Example 3.1 with cards; the L21 uniqueness scope word; the L21 misconception and bullet assumption; the L19 lab and references sentences; cards c302 and c307) are fixed and re-verified." % (len(rows), counts["pass"], counts["fail"], counts["unverifiable"])
out = Path("ledgers/M2/M2-d1.json")
out.write_text(json.dumps(frag, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(out, counts, len(rows))
