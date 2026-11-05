"""Build the PC3-b round-13 verifier fragment (ledgers/PC3/PC3-b.json) and validate it with tools/ledger.py.

Every row was re-derived in this round from the pinned checkout (e919577). Outputs cited as out/... live in
ledgers/PC3/scripts/PC3-b-r13/out/. No previous PASS row is carried; each subject was re-read.
"""

import json
import sys
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyE13-PC3-b")
sys.path.insert(0, str(ROOT / "tools"))
import ledger  # noqa: E402

OUT = "ledgers/PC3/scripts/PC3-b-r13/out"

rows: list[dict[str, str]] = []


def row(rid: str, check: str, location: str, status: str, evidence: str, fix: str | None = None) -> None:
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix or ""
    rows.append(r)


# ---- gates (run by the verifier on the pin) -------------------------------------------------------------------
row("gate-run-labs-unit", "2.5-labs", "tools/run_labs.py --unit PC3", "PASS",
    f"run_labs PC3: PASS (9/9), exit 0 ({OUT}/run_labs.out)")
row("gate-check-pages", "2.9-prose", "tools/check_pages.py --unit PC3", "PASS",
    f"check_pages PC3: PASS, exit 0 ({OUT}/check_pages.out)")
row("gate-check-dag", "2.9-DAG", "tools/check_dag.py --unit PC3", "PASS",
    f"check_dag PC3: PASS, exit 0 ({OUT}/check_dag.out)")
row("gate-check-projects", "2.6-structure", "tools/check_projects.py --unit PC3", "PASS",
    f"check_projects PC3: PASS, exit 0 ({OUT}/check_projects.out)")
row("gate-page-smoke-slice", "2.9-prose", "tools/page_smoke.py --unit PC3 --pages L04 L05 L06 (run alone)", "PASS",
    f"page_smoke L04, L05, L06 each PASS; page_smoke PC3: PASS, exit 0; lab runtimes 0.0 s ({OUT}/page_smoke.out)")
row("gate-ruff-mypy-twins", "2.5-labs",
    "ruff check tests/labs/PC3; ruff format --check tests/labs/PC3; mypy --no-incremental", "PASS",
    f"ruff: All checks passed, exit 0 ({OUT}/ruff_check.out); ruff format: 9 files already formatted, exit 0 "
    f"({OUT}/ruff_format.out); mypy: Success: no issues found in 385 source files, exit 0 ({OUT}/mypy.out)")
row("gate-pytest-lab-tooling", "2.5-labs",
    "pytest -q tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py", "PASS",
    f"46 tests passed, exit 0 ({OUT}/pytest_lab_tooling.out)")
row("gate-verify-refs-offline", "2.1-citations", "tools/verify_refs.py --offline (whole registry)", "PASS",
    f"offline integrity: 560 entries, 0 problems, exit 0 ({OUT}/verify_refs_offline.out); slice cites no key")
row("gate-run-graders-unit", "2.6-structure", "tools/run_graders.py --unit PC3 --seeds 0-49", "PASS",
    f"run_graders PC3: PASS (reference 50/50 seeds), exit 0 ({OUT}/run_graders.out); recorded, grader is another slice")

# ---- notation and labs -----------------------------------------------------------------------------------------
row("notation-registry-L04-L06", "2.4-notation", "course/modules/PC/PC3/L04.html, L05.html, L06.html (all math spans)",
    "PASS",
    "notation/notation.json has 8 symbols (T, Phi, gamma_3, gamma_4, R^ast, R^{e ast}, R_f, Q) and macros. "
    "grep of the three pages for each registered symbol and macro finds no reuse; the registered macros used are "
    "\\E (L04 x12) and \\Var (L04 x3); other commands are standard KaTeX. Lesson-local symbols N, t, p, L (L04 line 56) "
    "and the plain letters I, C, W, D, A, m, h, u, n, k, r are not registry entries and carry one meaning each per lesson.")
row("twin-run-alone-L04-L06", "2.5-labs", "tests/labs/PC3/lab-PC3-L04-1.py, lab-PC3-L05-1.py, lab-PC3-L06-1.py",
    "PASS", f"python -I -W error on each twin: exit 0, 0 stderr bytes ({OUT}/embed_r13.out)")
row("twin-page-code-equals-twin", "2.5-labs",
    "course/modules/PC/PC3/L04.html line 181, L05.html line 164, L06.html line 160 (data-run blocks) vs the three twins",
    "PASS",
    "html-unescaped data-run block equals the twin after rstrip of the final newline for L04, L05, L06 "
    f"(tools/embed_labs.py:117 rstrips the embedded text; {OUT}/embed_r13.out)")
row("twin-expected-equals-stdout", "2.5-labs",
    "L04.html expected block lines 424-475; L05.html 307-331; L06.html 284-304", "PASS",
    f"stdout of python -I -W error equals each expected block after rstrip, all three lab twins ({OUT}/embed_r13.out; "
    f"{OUT}/stdout_L04.txt, stdout_L05.txt, stdout_L06.txt)")
row("lab-L04-1-hypothesis-interpretation", "2.5-labs",
    "course/modules/PC/PC3/L04.html line 180 (hypothesis), line 476 (interpretation)", "PASS",
    f"hypothesis (identity True, -9950, P&L 30, nine grid values, variance 25 I^2) matches expected output; "
    f"interpretation numbers 9 fills, 13 informed, seed 1 16/20100/-2/10020/60 recomputed in {OUT}/l04_r13.out")
row("lab-L05-1-hypothesis-interpretation", "2.5-labs",
    "course/modules/PC/PC3/L05.html line 163 (hypothesis), line 332 (interpretation)", "PASS",
    f"hypothesis (1351, bound 400, 200 pushes, seed 6, windows 1..20, five edge checks, five window sizes) matches "
    f"output; interpretation 354, 350, 1351, 5239 recomputed in {OUT}/l05_r13.out")
row("lab-L06-1-hypothesis-interpretation", "2.5-labs",
    "course/modules/PC/PC3/L06.html line 159 (hypothesis), line 305 (interpretation)", "PASS",
    f"hypothesis (payoff 0/100 at 8000..12000, annuity 3310/1331, break-even 399300/331, NPVs at bounds and "
    f"8/10/12 percent) matches output; 42.24 and 42.71 printed, 42.24 and 42.70 unrounded, recomputed in "
    f"{OUT}/l06_r13.out")

# ---- L04 ---------------------------------------------------------------------------------------------------------
row("L04-definitions-A1-A6-notation", "2.4-notation", "course/modules/PC/PC3/L04.html lines 56-89", "PASS",
    "A1 probabilities 1/4, 1/4, 1/2 and the A5 test |I after| <= L = 10 with q >= 1 match play() in "
    "tests/labs/PC3/lab-PC3-L04-1.py lines 104-139; A6 a = m + h, b = m - h matches quote() lines 80-83; "
    "Example 1.3 (line 88) is that rule.")
row("L04-lab-section-locator", "2.9-prose", "course/modules/PC/PC3/L04.html lines 72, 87, 161, 178-179", "PASS",
    "the lab sits in lesson Section 4 (line 178, after Remark 4.2 at line 175); 'Lab 1 (Section 4)' at line 72 and "
    "'Lab 1, Section 4' at line 87 refer to that placement; Lab 1 has Parts 1-3 and no numbered sections, so the "
    "reference resolves. Recorded as a reading, not a defect.")
row("L04-prop-2.2-2.3-identity", "2.4-mathematics", "course/modules/PC/PC3/L04.html lines 100-122", "PASS",
    "Prop 2.3: W_t - W_{t-1} = c_t + sigma_t v_t + I_{t-1}(v_t - v_{t-1}) re-derived; Prop 2.2 telescopes to "
    "sum c_t + (sum sigma_t) v_N; c_t = -sigma_t f_t matches play() cash_flow = -side*price.")
row("L04-example-3.2-values", "2.4-mathematics", "course/modules/PC/PC3/L04.html line 143", "PASS",
    f"exact enumeration at v = 10000, 10020, 9985 gives 5, 0, 5/2 (lab Part 2 grid in expected block); "
    f"closed form from line 143 matches ({OUT}/l04_r13.out)")
row("L04-proposition-4.1-remark-4.2-sd", "2.4-mathematics", "course/modules/PC/PC3/L04.html lines 164-175", "PASS",
    "E[I eps] = 0 and Var = 25 I^2 re-derived; sd 15 cents at 3 units, 50 at 10 units; I = 10 example: uninformed "
    "buy 10 cents at prob 1/4 gives 5/2, and the uninformed sell is refused (11 > L), the informed does not trade "
    "at v = 10000 inside 9990/10010; matches Part 3 of the expected block (variance 2500 at I = 10).")
row("L04-remark-4.2-inventory-independence", "2.4-mathematics", "course/modules/PC/PC3/L04.html line 175", "PASS",
    "for |I| <= L-1 both sides fill, and c_t and sigma_t do not depend on I, so the trade term has the same law as at "
    "I = 0; checked against play() (size and |I| test only).")
row("L04-remark-3.4-inventory-zero", "2.4-mathematics", "course/modules/PC/PC3/L04.html lines 157-158", "PASS",
    "(1-p)h at p = 1/2 is h/2 = (2h)/4, a quarter of the quoted spread; the informed cost is the distance outside the "
    "quote (A4).")
row("L04-canon-breaks-tick", "2.9-prose", "course/modules/PC/PC3/L04.html lines 481-483 (Section 5, paragraphs 1-3)",
    "PASS", "tick of 5 cents (A2), integer cents, A1-A6 conditioning and the no-claim statement; paragraph 3 "
    "E = (1-p)h inside the quote rising with h matches Prop 3.1.")
row("L04-canon-breaks-quote-rule", "2.9-prose", "course/modules/PC/PC3/L04.html line 484 (Section 5, paragraph 4)",
    "PASS", f"mid at turn t equals 10000 - 10 I_{{t-1}} along all 20 turns of seed 0: True ({OUT}/l04_r13.out line 5); "
    "a maker purchase lowers the mid by 10 (the fill at the bid).")
row("L04-R2-spread-criterion", "2.4-mathematics", "course/modules/PC/PC3/L04.html lines 597-601 (R2)", "PASS",
    "at v = m both brackets vanish, E = (1-p)h; p < 1 gives E > 0 for every h >= 1; p = 1 gives E = 0 for every h; "
    "statement that no unique spread follows is correct.")
row("L04-E1-seed1-numbers", "2.2-numbers", "course/modules/PC/PC3/L04.html lines 565-571 (E1)", "PASS",
    f"seed 1 recomputed: 16 fills, cash flow 20100, inventory -2, settlement 10020, P&L 60; mark -20040 by hand "
    f"({OUT}/l04_r13.out line 2)")
row("L04-E2-binomial-z", "2.2-numbers", "course/modules/PC/PC3/L04.html lines 572-578 (E2)", "PASS",
    "13/20 = 0.65; sqrt(0.25/20) = 0.111803; 0.15/0.111803 = 1.3416 < 1.959964; informed count 13 recomputed "
    f"({OUT}/l04_r13.out line 1)")
row("L04-E3-mid-vs-settlement", "2.2-numbers", "course/modules/PC/PC3/L04.html lines 579-586 (E3)", "PASS",
    f"final mid = 10000 - 10 x I_19 = 9990 (recomputed, {OUT}/l04_r13.out line 4); P&L at settlement 30, at mid 40, "
    "difference 10 = I_N x (mid - v_N) = 1 x 10")
row("L04-problems-R1-R3-M-P", "2.4-mathematics", "course/modules/PC/PC3/L04.html lines 515-607", "PASS",
    "M1 W = 10; M2 refusal at 11 units; M3 no trade at 10010, buy at 10011 with one-cent loss; P1 identity N = 2; "
    "P2 E = h/2 at a and 0 at a+h; P3 Var = 400 at I = -4; R1 d = (1-p)h/p = 20/3; R3 |I| < 2, largest 1 (variance 25). "
    "All recomputed by hand.")
row("L04-M3-inventory-hypothesis", "2.4-mathematics", "course/modules/PC/PC3/L04.html lines 529-532 (M3)", "PASS",
    "A4 is strict: at 10010 neither test holds, so no trade; at 10011 the buy at 10010 loses one cent.")
row("L04-quiz-q11-citation", "2.9-prose", "course/modules/PC/PC3/L04.html lines 706-709 (quiz item 11)", "PASS",
    "'fills 9 of 20 turns' matches expected block and the recomputed count 9 "
    f"({OUT}/l04_r13.out line 1).")
row("L04-quiz-answers", "2.4-mathematics", "course/modules/PC/PC3/L04.html lines 632-720 (12 items)", "PASS",
    "numeric keys 10, 0, 5, 400, 6.6667 (tolerance 0.001 vs 20/3); mc keys re-derived (+10010, strict A4, mean 0, "
    "(1-p)h rises with h).")
row("L04-key-results-prop-3.1-assumptions", "2.4-mathematics", "course/modules/PC/PC3/L04.html line 622 (row 3)",
    "PASS", "assumptions listed (A1, A2, A4, A5, A6, H1 to H3) match Proposition 3.1 hypotheses at line 129.")
row("L04-prop-3.1-closed-form", "2.4-mathematics", "course/modules/PC/PC3/L04.html lines 127-139", "PASS",
    "proof re-derived case by case; exact check over integer v in 9900..10099 for quote 9990/10010 gives 0 mismatches "
    f"({OUT}/l04_r13.out).")
row("L04-corollary-3.3", "2.4-mathematics", "course/modules/PC/PC3/L04.html lines 146-154", "PASS",
    "E = h/2 - (v-a)/2 for v >= a; zero iff v = a + h; re-derived.")
row("L04-misconceptions", "2.9-prose", "course/modules/PC/PC3/L04.html lines 487-507 (four items)", "PASS",
    "10-cent P&L after a buy at 10010 with settlement 10000; variance 2500 at 10 units; zero at a+h; A3 excludes "
    "quotes that depend on v_t. All recomputed or read against the lesson.")
row("L04-key-results-table-other", "2.3-grades", "course/modules/PC/PC3/L04.html lines 620-629 (rows 1, 2, 5, 6)",
    "PASS", "identities T; variance T; nine-value enumeration C with Lab 1, Part 2 as basis (closed form T). "
    "Matches ruling 13 and the cards c075 and c069.")
row("L04-scope-and-banned-phrases", "2.9-prose", "course/modules/PC/PC3/L04.html (whole file) and L04 lab code",
    "PASS", "grep for TODO, TBD, lorem, ellipsis, 'for brevity', 'details omitted', 'beyond the scope', "
    "'left as an exercise', 'it is important to note', 'studies show', 'experts agree', 'it is well known', "
    "'obviously', 'clearly', 'roughly', 'it can be shown' and process words: no hits in L04-L06 pages or twins.")
row("L04-structure-hours", "2.9-prose", "course/modules/PC/PC3/L04.html (whole file); course/modules/PC/PC3/index.html "
    "lines 29, 143, 148, 167", "PASS",
    "data-hours 6; hub 36 h lessons (6 x 6) and 14 h project = 50 h; template sections present in BUILDER_RULES §4 "
    "order; problem set has M, P, E, R tiers with three problems each; quiz 12 items.")
row("L04-DAG-D-terms", "2.9-DAG", "course/modules/PC/PC3/L04.html lines 60, 157-158, 482", "PASS",
    "D3 adverse selection is plain prose with no dfn and no link (line 158); D4 inventory is plain prose; grep of the "
    "three pages for bayes, martingale, stopping, kelly, poisson, markov, capm, beta, duration, DCF, gordon, binomial, "
    "nash, auction, winner's curse returns nothing (except one 'Proposition 2.3 (the turn decomposition)' heading "
    "which is not a concept).")
row("L04-A1-project-consistency", "2.9-prose",
    "course/modules/PC/PC3/L04.html line 72; course/modules/PC/PC3/project.html lines 53 and 404", "PASS",
    "project.html line 53 states the rule (mid = last fill or 10000, bid and ask 10 cents from mid, one unit) and line "
    "404 states arrivals 1/4, 1/4, 1/2; both match L04 Example 1.3 (line 88) and A1 (line 72). project.html changed "
    "since round 12 and these lines were re-read; the grader is another slice.")
row("L04-footer-registry-claim", "2.9-prose", "course/modules/PC/PC3/L04.html line 736 (site-footer)", "PASS",
    "footer claim 'each key result is proved on the page or computed by Lab 1, and each is graded' holds for the "
    "L04 key-results table (T rows proved; C row from Lab 1, Part 2).")
row("L04-lab-docstring-money-integer", "2.9-prose",
    "tests/labs/PC3/lab-PC3-L04-1.py lines 3-6; course/modules/PC/PC3/L04.html line 184", "PASS",
    "docstring: quotes, cash flows and marks are integer cents; Fraction for expectations; play() uses int cents; "
    "'5/2 is 2.5 cents' matches expected block line 'E[change] = 5/2'.")

# ---- L05 ---------------------------------------------------------------------------------------------------------
row("L05-def-3.1-markup", "2.9-prose", "course/modules/PC/PC3/L05.html lines 105-106 (Definition 3.1)", "PASS",
    "strict survivor condition x_j > x_m and front-to-back increasing index match deque_maxima; survivor sets equal "
    f"the Definition 3.1 brute force at k = 1, 2, 3, 8, 32 ({OUT}/l05_r13.out 'survivor mismatches 0').")
row("L05-prop-2.1-2.2-remark", "2.4-mathematics", "course/modules/PC/PC3/L05.html lines 85-98", "PASS",
    "Prop 2.1 count (n-k+1)(k-1) matches naive_maxima (1351, 5239, 199, 0 recomputed); Remark 2.2 algebra "
    "n^2/4 - (r - n/2)^2 = (n-r)r checked; k = n/2 + 1 maximal for even n.")
row("L05-prop-3.2-correctness", "2.4-mathematics", "course/modules/PC/PC3/L05.html lines 123-133", "PASS",
    "Steps A, B, C re-read; 4000 random sequences with ties (n <= 30, values 0..5, all k) give output equal to the "
    f"naive maxima and front equal to the last occurrence of the window maximum: 0 failures ({OUT}/extra_r13.out).")
row("L05-prop-3.3-bound", "2.4-mathematics", "course/modules/PC/PC3/L05.html lines 135-142", "PASS",
    f"same 4000 trials: comparisons <= 2n, pushes = n, pops <= n; 0 failures ({OUT}/extra_r13.out); seed 5, k = 8: "
    "354 <= 400.")
row("L05-remark-3.4-k-range", "2.4-mathematics", "course/modules/PC/PC3/L05.html line 147 (Remark 3.4)", "PASS",
    f"x = (k, ..., 1, k+1): step k+1 removes all k entries for k = 1..11 ({OUT}/l05_r13.out 'R3.4' lines); "
    "before step i the deque holds indices in {i-k..i-1}, so at most k per step.")
row("L05-example-3.5-trace", "2.4-mathematics", "course/modules/PC/PC3/L05.html lines 151-153", "PASS",
    f"deque_maxima([3,1,4,1,5], 3) = [4, 4, 5] ({OUT}/l05_r13.out 'Ex3.5'); the step-by-step deque states match.")
row("L05-problems-M-P", "2.4-mathematics", "course/modules/PC/PC3/L05.html lines 367-413", "PASS",
    f"M1 21; M2 outputs (5, 5, 1, 3) ({OUT}/l05_r13.out 'M2'); M3 k = 1 and k = n as stated; P1 n^2/4 with n = 200 "
    f"giving k = 101 and 10000; P2 survival of q; P3 n - 1 for increasing sequences, 199 for k = 1, 2, 5, 100.")
row("L05-E1-E3-numbers", "2.2-numbers", "course/modules/PC/PC3/L05.html lines 417-437 (E1, E3)", "PASS",
    "E1: 169 x 31 = 5239 and ratio 5239/382 = 13.7147, 13.7; E3: k = 200 row 387 comparisons, 194 pops, 200 pushes, "
    f"387 <= 194 + 200 = 394 <= 400 ({OUT}/l05_r13.out).")
row("L05-E2-seed6-numbers", "2.2-numbers", "course/modules/PC/PC3/L05.html lines 424-430 (E2)", "PASS",
    f"seed 6, window 8: outputs equal, naive 1351, deque 350, pushes 200, pops 197 ({OUT}/l05_r13.out 'seed6 k8')")
row("L05-R1-scope-sentence", "2.9-prose", "course/modules/PC/PC3/L05.html lines 440-448 (R1)", "PASS",
    "R1 says no timing result is proved or run; the lab imports random, collections and dataclasses only, with no "
    "timer (the import block of tests/labs/PC3/lab-PC3-L05-1.py).")
row("L05-R2-R3", "2.4-mathematics", "course/modules/PC/PC3/L05.html lines 449-462", "PASS",
    "R2: k = 101, count 100 x 100 = 10000; R3: strictly increasing input, n - 1 comparisons for every k "
    f"({OUT}/l05_r13.out 'P3 increasing').")
row("L05-key-results-grades", "2.3-grades", "course/modules/PC/PC3/L05.html lines 466-481", "PASS",
    "Prop 2.1, Remark 2.2, Prop 3.2, Prop 3.3 and P3 rows are T with proofs on the page; the seed-5 agreement row is C "
    "with Lab 1, Part 2 as basis (ruling 13).")
row("L05-quiz-answers", "2.4-mathematics", "course/modules/PC/PC3/L05.html lines 483-563 (quiz items 1-10)", "PASS",
    "numeric keys 400, 10000, 5, 1351 and mc keys re-derived; item 7 (last occurrence of a tied maximum) confirmed "
    "by the tie trials (0 failures); item 10 (no outputs when k > n) matches the lab convention.")
row("L05-misconceptions-canon-breaks", "2.9-prose", "course/modules/PC/PC3/L05.html lines 336-359", "PASS",
    "354 within 400 (Lab 1 print); the counts are not run times (lab has no timer); Part 2 is one sequence; the "
    "amortised total is at most 2n by Prop 3.3.")
row("L05-structure-hours", "2.9-prose", "course/modules/PC/PC3/L05.html (whole file)", "PASS",
    "data-hours 6; template sections present; problem set M, P, E, R with three problems each; quiz 10 items; "
    "references and lesson navigation present.")
row("L05-markup-raw-less-than", "2.9-prose", "course/modules/PC/PC3/L05.html Definition 3.1 and math spans", "PASS",
    "inequalities in the definition are escaped (line 106, 'i-k&lt;j'); page_smoke reports all math rendered "
    f"({OUT}/page_smoke.out).")
row("L05-meta-uses-hash-map-heap", "2.9-DAG", "course/modules/PC/PC3/L05.html lines 38-40 and Remark 3.6 lines 157-158",
    "PASS", "meta 'Uses' lists hash-map and binary-heap, both linked in Remark 3.6; check_dag PASS.")
row("L05-meta-uses-other", "2.9-DAG", "course/modules/PC/PC3/L05.html line 38 (Uses list)", "PASS",
    f"big-O-complexity, monotonic-deque and unit-test are linked; check_dag PASS ({OUT}/check_dag.out).")
row("L05-why-it-matters-comparisons", "2.9-prose", "course/modules/PC/PC3/L05.html line 52 (why-it-matters)", "PASS",
    "the 'of this lesson' addition changes no claim: naive count exact (Prop 2.1), deque at most twice the input length "
    "(Prop 3.3); 'does not claim how long any session allows' matches Remark 1.2.")
row("L05-footer-registry-claim", "2.9-prose", "course/modules/PC/PC3/L05.html line 578 (site-footer)", "PASS",
    "footer claim matches the key-results table (T proved on the page; C from Lab 1).")
row("L05-DAG-links", "2.9-DAG", "course/modules/PC/PC3/L05.html lines 38, 58, 106, 157-158", "PASS",
    "each concept link resolves in concepts.html; the dfn for timed-coding-interview is defined once; check_dag PASS.")
row("L05-card-PC3-c092", "2.7-cards", "cards.json id PC3-c092 vs course/modules/PC/PC3/L05.html line 147", "PASS",
    "card says step k+1 removes all k entries in one run of the while loop, matching Remark 3.4 and the example.")
row("L05-card-PC3-c096-grade", "2.3-grades", "cards.json id PC3-c096 (now grade T, basis 'Proposition 2.1 with n = 200, "
    "k = 8 (Problem E2 hand computation)')", "PASS",
    "Prop 2.1 hypotheses hold; E2 (L05.html line 428) derives 193 x 7 = 1351 by hand from the formula; grade T with that "
    "basis matches ruling 13 and the fix of round 12.")
row("L05-card-PC3-c097-grade", "2.3-grades", "cards.json id PC3-c097 (now grade T, basis 'Proposition 2.1 with n = 200, "
    "k = 32 (Problem E1 hand computation)')", "PASS",
    "E1 (L05.html line 421) derives 169 x 31 = 5239 from Prop 2.1; grade T with that basis matches ruling 13.")

# ---- L06 ---------------------------------------------------------------------------------------------------------
row("L06-prop-1.1-payoff-identity", "2.4-mathematics", "course/modules/PC/PC3/L06.html lines 58-66", "PASS",
    "(s-K)^+ - (K-s)^+ = s - K checked in both cases; proof lines 65 complete.")
row("L06-remark-1.2-put-call-parity", "2.1-citations", "course/modules/PC/PC3/L06.html lines 68-71", "PASS",
    "the payoff form is proved; the price form is taken from the linked prerequisite concept and not re-derived; no "
    "registry key cited (slice cites none); check_dag PASS.")
row("L06-definition-1.3-NPV-and-prop-3.1", "2.4-mathematics", "course/modules/PC/PC3/L06.html lines 73-76, 110-118",
    "PASS", "NPV(r) = sum C_t (1+r)^-t (line 73) as used; Prop 3.1 proof gives NPV(u) = -I + mAu, strictly increasing "
    "since mA > 0, unique zero u* = I/(mA) (lines 116-117).")
row("L06-prop-2.1-forward", "2.4-mathematics", "course/modules/PC/PC3/L06.html lines 90-98", "PASS",
    "(i) cost zero and payoff F' - S/D in every state, re-derived with A1-A3; (ii) reverse portfolio uses A4 and A5 "
    "as stated; both directions checked.")
row("L06-remark-2.2-continuous-convention", "2.1-citations", "course/modules/PC/PC3/L06.html lines 80-90 (A2) and "
    "102-104 (Remark 2.2)", "PASS",
    "D = e^{-r tau} is stated as the linked forward concept's convention, not derived; S/D = S e^{r tau} is immediate; "
    "no registry key.")
row("L06-corollary-3.3-grade", "2.4-mathematics", "course/modules/PC/PC3/L06.html lines 130-139", "PASS",
    "product bounds attained (Prop 3.2), sign by Prop 3.1; with straddling bounds the loss at 200 and gain at 1600 "
    "match the lab output at all three rates.")
row("L06-prop-3.2-fermi-bounds", "2.4-mathematics", "course/modules/PC/PC3/L06.html lines 120-128", "PASS",
    "induction with positive bounds re-read; ends attained by choosing each factor at an end; [200, 1600] recomputed.")
row("L06-example-4.2-numbers", "2.2-numbers", "course/modules/PC/PC3/L06.html lines 146-150", "PASS",
    f"units 2000 x 1 x 1/10 = 200 and 4000 x 2 x 1/5 = 1600; A = 3310/1331; break-even 399300/331 = 1206.34; NPV "
    f"negative at 200 and positive at 1600 ({OUT}/l06_r13.out)")
row("L06-remark-4.3-sensitivity", "2.2-numbers", "course/modules/PC/PC3/L06.html lines 153-155 (Remark 4.3)", "FAIL",
    "Recomputed in out/l06_r13.out and extra_r13.out: exact A(8%) = 2.5770969872, A(10%) = 2.4868519910, "
    "A(12%) = 2.4018312682; exact 3000/A = 1164.100542, 1206.344411, 1249.046942. The displayed factors 2.5770970, "
    "2.4868520, 2.4018313 reproduce 1164.1005, 1206.3444, 1249.0469 to 4 dp, so the derivation is now on the page. "
    "DEFECT: line 154 says the factors are 'taken to seven significant digits', but 2.5770970, 2.4868520 and "
    "2.4018313 have eight significant digits (seven decimal places). Seven significant digits would be 2.401831, "
    "and 3000/2.401831 = 1249.0471, which does not reproduce 1249.0469.",
    "On line 154 (and in E1 line 397 and E3 line 411) replace 'to seven significant digits' with 'rounded to seven "
    "decimal places'. Keep the seven-decimal factors; they reproduce 1164.1005, 1206.3444 and 1249.0469.")
row("L06-E2-first-negative", "2.2-numbers", "course/modules/PC/PC3/L06.html lines 399-405 (E2)", "PASS",
    f"NPV(1200) = -105000000/1331 = -78888.05 and NPV(1300) = 1550000000/1331 = 1164537.94 recomputed exact "
    f"({OUT}/l06_r13.out); grid points above 1206.34 are 1300, 1400, 1500, 1600 (four); 1200 is the largest negative.")
row("L06-E1-12pct", "2.2-numbers", "course/modules/PC/PC3/L06.html lines 392-398 (E1)", "FAIL",
    "A = 1/1.12 + 1/1.2544 + 1/1.404928 = 2.40183126822 (exact). 3000/A = 1249.046942, which gives 1249.0469 at 4 dp "
    "and 'about 1249.05' at 2 dp; both correct. DEFECT: line 397 says 'which to seven significant digits is "
    "A = 2.4018313', but 2.4018313 has eight significant digits.",
    "On line 397 replace 'to seven significant digits' with 'to seven decimal places'.")
row("L06-E3-42.71", "2.2-numbers", "course/modules/PC/PC3/L06.html lines 406-416 (E3)", "FAIL",
    "The solution now writes A(8%) = 2.5770970, A(10%) = 2.4868520, A(12%) = 2.4018313 and break-evens 1164.1005, "
    "1206.3444, 1249.0469; all reproduce from 3000/A at 4 dp (out/l06_r13.out). Width 84.9464 (84.95), average "
    "84.9464/4 = 21.2366 (21.24), differences 42.2439 (42.24) and 42.7025 (42.70), and 1249.05 - 1206.34 = 42.71 "
    "from displayed values are all correct. DEFECT: line 411 says each factor is 'to seven significant digits', "
    "but the factors shown have eight significant digits.",
    "On line 411 replace 'to seven significant digits' with 'to seven decimal places'.")
row("L06-E3-rest-and-quiz-q9", "2.2-numbers", "course/modules/PC/PC3/L06.html lines 406-416 (E3 rest) and quiz "
    "item 9, lines 519-523", "PASS",
    "answer 21.24 (tolerance 0.01) correct; quiz explanation '84.9464/4 = 21.2366' is reproducible from the unrounded "
    "break-evens now derived on line 411. The label defect is recorded under L06-E3-42.71.")
row("L06-M1-M3-numbers", "2.2-numbers", "course/modules/PC/PC3/L06.html lines 342-362 (M1-M3)", "PASS",
    "M1 4900/0.98 = 5000 and payoff 50; M2 -100 + 600/11 + 6000/121 = 500/121 = 4.1322 ('about 4.13'); M3 "
    "33275/331 = 100.5287 ('about 100.53'); all recomputed.")
row("L06-P1-P3-proofs", "2.4-mathematics", "course/modules/PC/PC3/L06.html lines 367-390 (P1-P3)", "PASS",
    "P1 reverse portfolio cost 0 and payoff S/D - F' re-derived with signs; P2 affine zero; P3 bounds 200 and 1600 with "
    "attained ends.")
row("L06-R1-R3", "2.4-mathematics", "course/modules/PC/PC3/L06.html lines 417-437 (R1-R3)", "PASS",
    "R1 ratios 2 give ln 2 each; R2 closed form re-derived; R3 margin 15000000 x 1331/(1600 x 3310) = 3769.83 = 0.75397 "
    f"x 5000, fall 24.6 percent ({OUT}/l06_r13.out 'R3').")
row("L06-quiz-answers", "2.4-mathematics", "course/modules/PC/PC3/L06.html lines 459-533 (10 items)", "PASS",
    "numeric keys 5000, 4.13 (4.1322), 1206.34, 4, 21.24 re-derived within tolerance; mc keys match Prop 2.1, "
    "Corollary 3.3, Prop 3.1 and the linked articulation concept.")
row("L06-canon-breaks-and-misconceptions", "2.9-prose", "course/modules/PC/PC3/L06.html lines 308-334, line 324",
    "PASS",
    "line 324 quotes (1249.0469 - 1164.1005)/4 from unrounded values, now derived on the page (Remark 4.3 and E3) and "
    "reproducible (21.2366, out/l06_r13.out); 'factor of 8' = 2 x 2 x 2 = 1600/200; Section 5 model limits follow "
    "from Example 4.2.")
row("L06-articulation-claim-linked", "2.1-citations", "course/modules/PC/PC3/L06.html line 75 and quiz item 10 "
    "(lines 524-532)", "PASS",
    "the statement is the linked prerequisite identity (statement-articulation link, check_dag PASS); the lesson cites "
    "no registry key and claims only that identity.")
row("L06-footer-registry-claim", "2.9-prose", "course/modules/PC/PC3/L06.html line 549 (site-footer)", "PASS",
    "footer claim holds: T rows proved on the page; C rows graded and sourced to Lab 1.")
row("L06-structure-hours", "2.9-prose", "course/modules/PC/PC3/L06.html (whole file); course/modules/PC/PC3/index.html",
    "PASS", "data-hours 6; template sections present; problem set M, P, E, R with three problems each; quiz 10 items; "
    "hub 36 + 14 = 50 h.")
row("L06-DAG-and-cross-links", "2.9-DAG", "course/modules/PC/PC3/L06.html lines 38-39, 56, 75, 86", "PASS",
    "uses forward-contract, cost-of-carry-forward-price, put-call-parity, net-present-value, statement-articulation, "
    "fermi-estimation (L01 link); case-interview defined once (line 144); the D6 excluded concepts (CAPM, duration, DCF, "
    "ratios) do not appear; check_dag PASS.")
row("L06-why-it-matters-scope", "2.9-prose", "course/modules/PC/PC3/L06.html line 52 (why-it-matters)", "PASS",
    "each named result is on the page (Prop 2.1 forward price, Prop 3.1 break-even, Remark 4.3 sensitivity); the "
    "'of this lesson' additions change no claim.")
row("L06-lab-docstring-money-integer", "2.9-prose", "tests/labs/PC3/lab-PC3-L06-1.py lines 6-9; "
    "course/modules/PC/PC3/L06.html lines 165-168", "PASS",
    "docstring: prices and the outlay are integer cents; a fractional break-even is an exact fraction of a cent; "
    "all values are fractions.Fraction; display is the only rounding step (half_up, page L06.html lines 196-205).")
row("L06-card-PC3-c148-grade", "2.3-grades", "cards.json id PC3-c148 (now grade T, basis 'Problem E1 (annuity factor "
    "A = 2.4018313 at 12 percent, so 3000/A = 1249.0469)')", "PASS",
    "value re-derived from the closed form in Prop 3.1 and E1 (1249.046942, 1249.05 at 2 dp); ruling 13 applies "
    "(page-derived, with the problem as basis); the labelling defect is recorded under L06-E1-12pct.")
row("L06-card-PC3-c151", "2.3-grades", "cards.json id PC3-c151 (grade T, basis 'Problem E3 solution ...')", "PASS",
    "the unrounded break-evens and the factor derivation are now on the page; the card's 21.2366 and 21.24 reproduce "
    f"({OUT}/l06_r13.out). The E3 label defect is recorded under L06-E3-42.71; the card's number is unaffected.")

# ---- cards ---------------------------------------------------------------------------------------------------------
row("card-full-scan-L04", "2.7-cards", "cards.json, lesson L04 (37 cards: c062-c083, c137-c141, c153-c154, c162-c164, "
    "c168, c171, c174-c176)", "PASS",
    f"all 37 read in full ({OUT}/cards_L456.txt); numbers and statements checked against L04 (e.g. c067 40 vs 30 cents, "
    "c069 Prop 3.1, c070 Example 3.2 values, c074 15 and 50 cents, c078 zero at a+h, c082 20/3, c083 variance 100 strict).")
row("card-full-scan-L05", "2.7-cards", "cards.json, lesson L05 (26 cards: c084-c101, c142-c146, c169-c170, c177)",
    "PASS", f"all 26 read in full ({OUT}/cards_L456.txt); c096 and c097 corrected to T with page-derived basis; "
    "c142-c146 match Lab 1 output (354, 200 and 199, 387, 382, five edge checks); c092, c094, c095 match.")
row("card-full-scan-L06", "2.7-cards", "cards.json, lesson L06 (35 cards: c102-c127, c147-c151, c165-c167, c178-c179)",
    "PASS", f"all 35 read in full ({OUT}/cards_L456.txt); c116 (A 2.5770970), c148 and c151 match Remark 4.3 and E1/E3; "
    "c117 and c150 match lab expected output; c179 matches E2. Id c118 is absent from the file (a gap; no reference "
    "to it in cards or pages).")
row("card-duplicate-scan", "2.7-cards", "course/modules/PC/PC3/cards.json (all 174 cards, ids and fronts)", "PASS",
    "174 ids, 174 unique ids, 174 unique fronts (python collections.Counter over cards.json)")
row("card-key-results-agreement", "2.7-cards", "L04 key results (lines 620-629), L05 (472-477), L06 (448-453) vs cards",
    "PASS", "each key-results row has a card with the same statement and grade (L05 n-1 with c095 T; L05 seed-5 "
    "agreement with c101 C; L06 399300/331 with c147 T; L04 nine-value check with c075 C; L04 Prop 3.1 with c069 T).")
row("card-number-in-lesson", "2.7-cards", "cards.json numbers vs L04, L05, L06 text", "PASS",
    "numbers in the card backs, including the changed c096 (1351, 193, 7), c097 (5239, 169, 31), c116 (2.5770970, "
    "1164.1005), c148 (2.4018313, 1249.0469) and c151 (21.2366, 21.24), appear in the lesson text (L05 lines 421, 428; "
    "L06 lines 154, 397, 411).")
row("card-cite-empty", "2.1-citations", "cards.json, lessons L04-L06 (98 cards)", "PASS",
    "all 98 cite arrays are empty; no card makes an empirical claim that needs a registry key; graded non-T cards name "
    "a basis (lab part or page result), as BUILDER_RULES §7 requires.")

fragment = {
    "unit": "PC3",
    "slice": "PC3-b",
    "round": 13,
    "verifier": "Claude Haiku 5.5, independent verifier for PC3-b round 13 (did not build PC3)",
    "pin": "e919577b45b431ce68e1e6533b00b8a301277937",
    "base": "5db69a9bee460736c318ebfacc7200ee5a6eb0f0 (round-12 pin). Delta 5db69a9..e919577 in this slice: "
            "L05.html (why-it-matters line 52; quiz item 4 line 508-514); L06.html (why-it-matters line 52; Remark 4.3 "
            "line 154; E1 line 397; E3 line 411); cards.json c096, c097, c116, c148 (c055 is L03, outside the slice). "
            "L04.html and all three twins are byte-identical to the round-12 pin. project.html changed and was re-read at "
            "lines 53 and 404. No PASS row is carried: every subject was re-derived this round.",
    "checkout": str(ROOT),
    "scratch": f"{ROOT}/{OUT}",
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Slice b: L04.html, L05.html, L06.html, lab twins lab-PC3-L04-1.py, lab-PC3-L05-1.py, lab-PC3-L06-1.py, and the "
        "98 PC3 cards for L04-L06, all read in full (out/cards_L456.txt). Lab twins are demonstrations; mutation "
        "testing does not apply (architect ruling), so mutants is empty.",
        "Full read: each page read line by line (prose, problems, key results, quiz); each twin read in full; the "
        "embedded code diffed against the twin; each expected block diffed against a fresh run.",
        "Independent recomputation (out/): l04_r13.py (own game simulator, enumeration of the nine-value grid, 1-cent grid "
        "closed-form check, seed 0 and seed 1 summaries, mid identity), l05_r13.py (own deque and naive scan, survivor "
        "brute force, Remark 3.4, Example 3.5, M2, P3, E1, E3), l06_r13.py (exact annuity factors, break-evens, E2, R3, M2, "
        "M3), extra_r13.py (random tie trials for Prop 3.2, 3.3 and the Q7 tie rule, lab NPV bounds at 8, 10, 12 percent), "
        "embed_r13.py (page code vs twin, expected vs stdout).",
        "Judgement (not a row): 'Lab 1 (Section 4)' (L04 lines 72, 87) refers to the lesson's Section 4, which hosts the lab; "
        "accepted. Cards for definitions and assumptions carry no grade (grade is optional in the schema, check_pages.py "
        "lines 386-394); accepted.",
        "Judgement (not a row): the three FAIL rows share one defect (precision labelled 'seven significant digits' for "
        "factors shown to seven decimal places). The fix is a relabel; the values stay.",
        "Judgement (not a row): round-12 judgements re-confirmed: 'adds no expected gain' (L04 why-it-matters, Remark 4.2) "
        "refers to the fair-move term, which has mean zero; the L05 Remark 3.6 push bound floor(log2 m) is read after the push.",
    ],
    "summary": {},
}

problems = ledger.validate(fragment, "PC3-b")
counts = {s: sum(1 for r in rows if r["status"] == s) for s in ("PASS", "FAIL", "UNVERIFIABLE")}
fragment["summary"] = {"rows": len(rows), "pass": counts["PASS"], "fail": counts["FAIL"],
                       "unverifiable": counts["UNVERIFIABLE"]}
out_path = ROOT / "ledgers/PC3/PC3-b.json"
out_path.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("validate:", problems)
print("summary:", fragment["summary"], "verdict:", fragment["verdict"])
