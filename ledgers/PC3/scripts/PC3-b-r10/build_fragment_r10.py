"""Build ledgers/PC3/PC3-b.json (round 10) from the row specification below. Stdlib only.

Every row was re-derived in this round from the checkout (pin 00a84795); none is carried from round 9.
Row ids are the round-9 ids, kept as required by the verifier rules; one row changed status to FAIL.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyE10-PC3-b")
S = "ledgers/PC3/scripts/PC3-b-r10"
O = f"{S}/out"

ROWS: list[tuple[str, str, str, str, str]] = [
    # gates and tooling
    ("gate-run-labs-unit", "2.5-labs", "tools/run_labs.py --unit PC3",
     "PASS", f"Run on pin 00a84795: 'run_labs PC3: PASS (9/9)', exit 0 ({O}/run_labs.out)."),
    ("gate-check-pages", "2.9-prose", "tools/check_pages.py --unit PC3",
     "PASS", f"Run: 'check_pages PC3: PASS', exit 0 ({O}/check_pages.out)."),
    ("gate-check-dag", "2.9-DAG", "tools/check_dag.py --unit PC3",
     "PASS", f"Run: 'check_dag PC3: PASS', exit 0 ({O}/check_dag.out)."),
    ("gate-check-projects", "2.6-structure", "tools/check_projects.py --unit PC3",
     "PASS", f"Run: 'check_projects PC3: PASS', exit 0 ({O}/check_projects.out). Unit-wide; project files are outside this slice."),
    ("gate-page-smoke-slice", "2.9-prose", "tools/page_smoke.py --unit PC3 --pages L04 L05 L06 (run alone)",
     "PASS", f"Run alone: L04, L05, L06 each PASS; lab runtime 0.0 s; 'page_smoke PC3: PASS', exit 0 ({O}/page_smoke.out)."),
    ("gate-ruff-mypy-twins", "2.5-labs", "ruff check and ruff format --check tests/labs/PC3; mypy --no-incremental (full project)",
     "PASS", f"'All checks passed!' ({O}/ruff_check.out); '9 files already formatted' ({O}/ruff_format.out); "
             f"'Success: no issues found in 385 source files', exit 0 ({O}/mypy.out)."),
    ("gate-pytest-lab-tooling", "2.5-labs", "pytest -q tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py",
     "PASS", f"Exit 0, all dots, 100% ({O}/pytest_lab_tooling.out)."),
    ("gate-verify-refs-offline", "2.1-citations", "tools/verify_refs.py --offline (whole registry)",
     "PASS", f"'offline integrity: 560 entries, 0 problems', exit 0 ({O}/verify_refs_offline.out). The slice pages carry no data-cite (grep count 0)."),
    # notation and mathematics
    ("notation-registry-L04-L06", "2.4-notation", "course/modules/PC/PC3/L04.html, L05.html, L06.html (math)",
     "PASS", "Macro inventory by grep: only \\E (12 uses in L04) and \\Var (3 uses in L04) are registered macros used; \\T, \\Phi, "
             "\\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q}, \\R, \\Prob absent. L06 uses \\operatorname{NPV} (a KaTeX operator name, "
             "no registered symbol). Local symbols per lesson (L04: N, t, p, L, h, I, v, a, b, q, m, sigma, varepsilon, c, C, W; L05: x, k, n, r, p, M; "
             "L06: r, A, D, S, I, m, u, tau, ell, h) do not take a registered meaning."),
    ("twin-run-alone-L04-L06", "2.5-labs", "tests/labs/PC3/lab-PC3-L04-1.py, lab-PC3-L05-1.py, lab-PC3-L06-1.py",
     "PASS", f"'python -I -W error <twin>' exit 0 with empty stderr for all three ({O}/twin_lab-PC3-L04-1.stdout/.stderr, L05, L06)."),
    ("twin-page-code-equals-twin", "2.5-labs", "course/modules/PC/PC3/L04.html, L05.html, L06.html vs the three twins",
     "PASS", f"{S}/embed_compare.py: unescaped page code equals each twin, compared after the final newline that the embed convention omits ({O}/embed_compare.out)."),
    ("twin-expected-equals-stdout", "2.5-labs", "expected blocks L04 (52 lines), L05 (25), L06 (21)",
     "PASS", f"{S}/embed_compare.py: unescaped expected block equals the twin's stdout line for line ({O}/embed_compare.out). Round 9 recorded 50 lines for L04; the block has 52."),
    ("lab-L04-1-hypothesis-interpretation", "2.5-labs", "course/modules/PC/PC3/L04.html line 180 (hypothesis), line 475 (interpretation)",
     "PASS", f"Hypothesis predictions (identity True, cash -9950, P&L 30, nine grid values, five inventories) match the printed output at lines 451, 446-450, 459-474. "
             f"Interpretation numbers (9 fills, 13 informed arrivals, seed 1: 16 fills, 20100, -2, 10020, 60) match {S}/out/l04_indep.out."),
    ("lab-L05-1-hypothesis-interpretation", "2.5-labs", "course/modules/PC/PC3/L05.html line 163 (hypothesis), line 332 (interpretation)",
     "PASS", f"Hypothesis: 200 integers 0..999 from Random(5); naive 1351 = 193 x 7; deque at most 400 comparisons; 200 pushes. Printed output lines 309-324 match; "
             f"interpretation counts 1351, 354, 350 match {S}/out/l05_indep.out."),
    ("lab-L06-1-hypothesis-interpretation", "2.5-labs", "course/modules/PC/PC3/L06.html line 159 (hypothesis), line 304 (interpretation)",
     "PASS", f"Hypothesis: F = 10000, payoff 0 at 10000 and 100 at 10100 for five spot values, annuity 3310/1331, break-even 399300/331, NPVs at bounds and 8/10/12 percent "
             f"match printed lines 284-303 and {S}/out/l06_indep.out. Interpretation differences 42.24 and 42.71 (printed), 42.24 and 42.70 (unrounded) verified."),
    # L04
    ("L04-definitions-A1-A6-notation", "2.4-notation", "course/modules/PC/PC3/L04.html lines 56-89",
     "PASS", "Read lines 56-89: N, t, p, L declared local; A1-A6 stated; Remark 1.2 and Example 1.3 constants match the code (N=20, v0=10000, moves 5, q-bar 5, L 10, h 10, q 1)."),
    ("L04-lab-section-locator", "2.9-prose", "course/modules/PC/PC3/L04.html line 72 (A1) and line 87 (Example 1.3 title)",
     "PASS", "A1 at line 72 and Example 1.3 at line 87 are as cited. Lab 1 sits at line 178, inside Section 4 (line 161), so 'Lab 1 (Section 4)' is correct."),
    ("L04-prop-2.2-2.3-identity", "2.4-mathematics", "course/modules/PC/PC3/L04.html lines 100-118",
     "PASS", "Proposition 2.2 and Proposition 2.3 re-derived by hand (C_t and I_t induction; W_t - W_{t-1} = (c_t + sigma_t v_t) + I_{t-1}(v_t - v_{t-1})). Lab Part 1 identity prints True (line 451)."),
    ("L04-example-3.2-values", "2.2-numbers", "course/modules/PC/PC3/L04.html line 143",
     "PASS", f"v = 10000 -> 5, 10020 -> 0, 9985 -> 5/2 by closed form and by enumeration ({S}/out/l04_indep.out, Example 3.2 lines)."),
    ("L04-proposition-4.1-remark-4.2-sd", "2.2-numbers", "course/modules/PC/PC3/L04.html lines 163-176",
     "PASS", "Standard deviation 5|I| (3 units -> 15 cents, 10 units -> 50 cents); Part 3 variances 0, 25, 225, 225, 2500 (printed lines 470-474) equal 25 I^2."),
    ("L04-remark-4.2-inventory-independence", "2.4-mathematics", "course/modules/PC/PC3/L04.html line 175",
     "PASS", f"Enumeration over |I| <= 9 on a grid equals the inventory-0 value (True); at I = +/-10, v = 10000 the expected trade term is 5/2 ({S}/out/l04_indep.out)."),
    ("L04-remark-3.4-inventory-zero", "2.2-numbers", "course/modules/PC/PC3/L04.html lines 157-158",
     "PASS", "(1-p)h with p = 1/2 is h/2, a quarter of 2h; re-derived from Proposition 3.1. Adverse selection is described in plain prose (plan D3), with no citation."),
    ("L04-canon-breaks-tick", "2.9-prose", "course/modules/PC/PC3/L04.html lines 480-482 (Section 5, paragraphs 1-3)",
     "PASS", "Limit-order-book queue, adverse selection, the arrival-probability claim and the 'cannot show a wider quote costs customers' sentence are consistent with A1, A4 and Proposition 3.1."),
    ("L04-canon-breaks-quote-rule", "2.4-mathematics", "course/modules/PC/PC3/L04.html line 483 (Section 5, paragraph 4)",
     "PASS", f"'Mid at turn t is 10000 - 10 I_(t-1)': checked on seeds 0-199, every turn, and by Lab Part 1 rows ({S}/out/l04_indep.out, line 'Section 5 mid claim')."),
    ("L04-R2-spread-criterion", "2.4-mathematics", "course/modules/PC/PC3/L04.html lines 597-600 (R2)",
     "PASS", "At v = m both brackets vanish, so E = (1-p)h; p < 1 gives E > 0 for every h, p = 1 gives E = 0 for every h. The 'would need the arrival distribution to depend on the quote' claim is necessary, as argued."),
    ("L04-E1-seed1-numbers", "2.2-numbers", "course/modules/PC/PC3/L04.html lines 566-568",
     "PASS", f"Independent game on seed 1: 16 fills, cash flow 20100, inventory -2, settlement 10020, P&L 60 ({S}/out/l04_indep.out)."),
    ("L04-E2-binomial-z", "2.2-numbers", "course/modules/PC/PC3/L04.html lines 572-575",
     "PASS", f"SE sqrt(0.25/20) = 0.111803; z = 0.15 / 0.111803 = 1.3416 < 1.96; 13 informed arrivals on seed 0 ({S}/out/l04_indep.out)."),
    ("L04-E3-mid-vs-settlement", "2.2-numbers", "course/modules/PC/PC3/L04.html lines 579-582",
     "PASS", f"Seed 0: turn-20 mid 9990, settlement 9980, cash flow -9950, inventory 1: P&L 30 at settlement, 40 at mid, difference 10 ({S}/out/l04_indep.out)."),
    ("L04-problems-R1-R3-M-P", "2.4-mathematics", "course/modules/PC/PC3/L04.html lines 514-607 (M1-M3, P1-P3, E1-E3, R1-R3)",
     "PASS", "M1 (+10010 cash, mark 10), M2 (sell refused at 10, buy fills to 9), M3 (no trade at 10010; -1 at 10011), P1, P2 (h/2 and 0), P3 (400), R1 (d = 20/3), R2, R3 (|I| < 2, variance 25) re-derived by hand; no mismatch."),
    ("L04-quiz-q11-citation", "2.9-prose", "course/modules/PC/PC3/L04.html lines 705-709 (quiz item 11)",
     "PASS", "Answer 9 matches 'fills 9 of 20 turns' printed at line 445 for seed 0."),
    ("L04-quiz-answers", "2.9-prose", "course/modules/PC/PC3/L04.html lines 633-719",
     "PASS", "Twelve items: numeric keys 10, 0, 5, 400, 6.6667 (tolerance 0.001 covers 20/3), 9 re-derived; each multiple-choice item has one data-correct option that matches the lesson; every item has an explanation."),
    ("L04-key-results-prop-3.1-assumptions", "2.9-prose", "course/modules/PC/PC3/L04.html line 621",
     "PASS", "Row 3 lists A1, A2, A4, A5, A6 and H1 to H3, which are the hypotheses Proposition 3.1 uses (A3 is not needed because the quote is fixed by H2)."),
    ("L04-prop-3.1-closed-form", "2.4-mathematics", "course/modules/PC/PC3/L04.html lines 127-139",
     "PASS", f"Enumeration equals the closed form at 1212 points (six quotes, fair values in half-cent steps from 9950 to 10050): 0 mismatches ({S}/out/l04_indep.out). Proof re-derived line by line."),
    ("L04-corollary-3.3", "2.4-mathematics", "course/modules/PC/PC3/L04.html lines 146-154",
     "PASS", f"Zero exactly at v = 10020 = a + h on 10010..10040 ({S}/out/l04_indep.out); proof E = h/2 - (v-a)/2 re-derived."),
    ("L04-misconceptions", "2.9-prose", "course/modules/PC/PC3/L04.html lines 486-506",
     "PASS", "Four misconceptions. Numbers checked: 0 cents at v = 10020 (printed line 467), cash flow +10010 and mark 10 cents, variance 2500 cents^2 at I = 10 (printed line 474)."),
    ("L04-key-results-table-other", "2.9-prose", "course/modules/PC/PC3/L04.html lines 613-628 (rows 1, 2, 5, 6)",
     "PASS", "Rows 1, 2, 5 are T and proved on the page (Propositions 2.2, 2.3, 4.1). Row 6 is C and names Lab 1, Part 2 as the source, as the lab-read rule requires."),
    ("L04-scope-and-banned-phrases", "2.9-prose", "course/modules/PC/PC3/L04.html (whole file)",
     "PASS", "Banned-phrase grep over L04 (tools/check_pages.py BANNED list, plus ellipsis and process words): no hits. Scope words read in context (every, all, only, same, exactly, any); each is backed by a proof, enumeration, or lab check."),
    ("L04-structure-hours", "2.9-prose", "course/modules/PC/PC3/L04.html (whole file); course/modules/PC/PC3/index.html (data-hours-lessons=36)",
     "PASS", "data-hours=6. Order matches BUILDER_RULES 4.2. Why-it-matters is 119 words (limit 120). Four misconceptions. Twelve problems (three per tier), each with details.solution. Twelve quiz items. Hours 6 x 6 = 36 plus project 14 = 50."),
    ("L04-DAG-D-terms", "2.9-DAG", "course/modules/PC/PC3/L04.html lines 38-39, 97, 158, 481",
     "PASS", "Links: L03#def-expected-value-game (defined in L03.html), expectation, market-maker, bid-ask-spread, limit-order-book (all in the closure, owners M4 and FC1). Adverse selection (D3) and inventory (D4) appear as plain prose. No martingale, Bayes, MS1 or Kelly term."),
    ("L04-A1-project-consistency", "2.4-notation", "course/modules/PC/PC3/L04.html line 72; course/modules/PC/PC3/project.html lines 400-408 (Conventions)",
     "PASS", "project.html states the arrival split 1/4, 1/4, 1/2 and the +/-5 moves with probability 1/2, matching A1, A2 and Definition 1.1."),
    ("L04-footer-registry-claim", "2.9-prose", "course/modules/PC/PC3/L04.html line 735 (site-footer)",
     "PASS", "Footer says each key result is proved on the page or computed by Lab 1, and graded. All six rows are T (proved) or C (Lab 1)."),
    # L05
    ("L05-def-3.1-markup", "2.4-mathematics", "course/modules/PC/PC3/L05.html line 106 (Definition 3.1)",
     "PASS", f"Surviving-index definition checked exhaustively: the deque equals the surviving set after every step, over {{0,1,2}}^n for n <= 7, all k (21324 cases, {S}/l05_indep.py output {O}/l05_indep.out)."),
    ("L05-prop-2.1-2.2-remark", "2.2-numbers", "course/modules/PC/PC3/L05.html lines 85-98",
     "PASS", f"Comparison count (n-k+1)(k-1) checked for n < 60, all k ({O}/l05_indep.out). Remark 2.2 identity and peak at k = n/2 + 1 checked; n = 200 peak k = 101, count 10000."),
    ("L05-prop-3.2-correctness", "2.4-mathematics", "course/modules/PC/PC3/L05.html lines 123-133",
     "PASS", f"Steps A-C re-read. Output equals brute-force window maximum in all 21324 exhaustive cases and in 400 random sequences ({O}/l05_indep.out)."),
    ("L05-prop-3.3-bound", "2.4-mathematics", "course/modules/PC/PC3/L05.html lines 135-142",
     "PASS", f"On 400 random sequences (n <= 120, all k): pushes = n, pops <= n, while-loop tests <= 2n; largest tests/(2n) = 0.972 ({O}/l05_indep.out)."),
    ("L05-remark-3.4-k-range", "2.2-numbers", "course/modules/PC/PC3/L05.html line 147 (Remark 3.4, first sentence)",
     "FAIL", "Remark 3.4 says 'One step can remove up to k-1 entries.' This is false: a step can remove k entries. "
             f"Exhaustive search ({S}/l05_remark34_max_step_removals.py, output {O}/l05_remark34_max_step_removals.out) finds largest one-step back-removal count = k for k = 2, 3, 4, "
             "with witnesses (1,0,1) for k=2, (2,1,0,2) for k=3, (3,2,1,0,3) for k=4. "
             f"The witness x = (k, k-1, ..., 1, k+1) with n = k+1 removes all k entries at step k+1 for k = 2..10 ({O}/l05_remark34_fix_witness.out). "
             "The example x = (k, ..., 2, k+1) with n = k (k-1 removals) is correct as an example but is not a bound. "
             "FIX: change 'One step can remove up to k-1 entries' to 'One step can remove up to k entries', and take the witness x = (k, k-1, ..., 1, k+1) with n = k+1 "
             "(at step k+1 the deque holds indices 1..k in decreasing value and the value k+1 removes all k in one loop). Keep 'so the cost of one step is not bounded by a constant'. "
             "Quiz item 4 (a step that removes k-1 entries) remains true and needs no change."),
    ("L05-example-3.5-trace", "2.2-numbers", "course/modules/PC/PC3/L05.html lines 151-153",
     "PASS", f"Deque states (1), (1,2), (3), (3,4), (5) and outputs (4,4,5) reproduced by the script ({O}/l05_indep.out, Example 3.5 line)."),
    ("L05-problems-M-P", "2.4-mathematics", "course/modules/PC/PC3/L05.html lines 365-413 (M1-M3, P1-P3)",
     "PASS", "M1 = 21; M2 trace gives deques (1),(2),(2,3),(3,4),(5) and outputs (5,5,1,3), reproduced; M3 for k=1 and k=n; P1 gives k = 101 and count 10000; P2 survival argument; P3 n-1 checked for n <= 30 and all k."),
    ("L05-E1-E3-numbers", "2.2-numbers", "course/modules/PC/PC3/L05.html lines 417-437",
     f"PASS", f"E1: 169 x 31 = 5239 and 5239/382 = 13.7147 (rounded 13.7). E3: largest deque count 387 at k = 200, bound 2n = 400, split bound 194 + 200 = 394 ({O}/l05_indep.out)."),
    ("L05-E2-seed6-numbers", "2.2-numbers", "course/modules/PC/PC3/L05.html lines 424-430",
     "PASS", f"Seed 6, k = 8: outputs equal, naive 1351, deque tests 350, pushes 200, pops 197 (back 178, front 19) ({O}/l05_indep.out)."),
    ("L05-R1-scope-sentence", "2.9-prose", "course/modules/PC/PC3/L05.html lines 440-448 (R1)",
     "PASS", "The solution says the lesson runs no timing protocol and proves no timing result, consistent with Remark 1.2 and the no-timer rule."),
    ("L05-R2-R3", "2.2-numbers", "course/modules/PC/PC3/L05.html lines 449-462",
     "PASS", "R2: k = 101 gives 10000 (Remark 2.2). R3: strictly increasing input removes one entry per step i >= 2; total n-1 (P3 check)."),
    ("L05-key-results-grades", "2.3-grades", "course/modules/PC/PC3/L05.html lines 466-481",
     "PASS", "Rows 1-5 are T and proved on the page (Propositions 2.1, 3.2, 3.3, Remark 2.2, Problem P3). Row 6 is C and names Lab 1, Part 2 as the source."),
    ("L05-quiz-answers", "2.9-prose", "course/modules/PC/PC3/L05.html lines 483-563",
     "PASS", "Ten items. Numeric keys 21, 400, 10000, 5, 1351 re-derived. Item 7 (last occurrence of ties) matches the strict survival test and the lab's pop rule (out/l05_quiz7_ties.out: sequence [5,5], k=2, final front index 2). Items 4 and 6 consistent with Remark 3.4 as corrected and with P3."),
    ("L05-misconceptions-canon-breaks", "2.9-prose", "course/modules/PC/PC3/L05.html lines 336-359",
     "PASS", "'Amortised' claim (at most two comparisons per step on average) and 'order k in one step' are consistent with Proposition 3.3 and the corrected Remark 3.4."),
    ("L05-structure-hours", "2.9-prose", "course/modules/PC/PC3/L05.html (whole file)",
     "PASS", "data-hours=6. Section order matches BUILDER_RULES 4.2. Why-it-matters is 91 words. Three misconceptions. Twelve problems (three per tier). Ten quiz items. No debate key."),
    ("L05-markup-raw-less-than", "2.9-prose", "course/modules/PC/PC3/L05.html Definition 3.1 and math",
     "PASS", "Escapes render: page_smoke PASS, all math rendered (out/page_smoke.out)."),
    ("L05-meta-uses-hash-map-heap", "2.9-DAG", "course/modules/PC/PC3/L05.html lines 38-40 and Remark 3.6 lines 157-158",
     "PASS", "hash-map and binary-heap (CS2) are linked; both are in the closure."),
    ("L05-meta-uses-other", "2.9-DAG", "course/modules/PC/PC3/L05.html line 38 (Uses list)",
     "PASS", "big-o-complexity, monotonic-deque (CS2) and unit-test (CS1) are linked, and each is in the closure."),
    ("L05-why-it-matters-comparisons", "2.9-prose", "course/modules/PC/PC3/L05.html line 52",
     "PASS", "'at most twice the input length in comparisons' is Proposition 3.3 (tests <= 2n). Why-it-matters is 91 words."),
    ("L05-footer-registry-claim", "2.9-prose", "course/modules/PC/PC3/L05.html line 578 (site-footer)",
     "PASS", "Each key result is proved on the page or computed by Lab 1 and graded (rows 1-6)."),
    ("L05-DAG-links", "2.9-DAG", "course/modules/PC/PC3/L05.html lines 38, 58, 106, 157-158",
     "PASS", "Linked concepts resolve (check_dag PASS). timed-coding-interview is defined at line 58 before any use; monotonic-deque is defined in CS2 and linked."),
    # L06
    ("L06-prop-1.1-payoff-identity", "2.4-mathematics", "course/modules/PC/PC3/L06.html lines 58-66",
     "PASS", "Both cases (s >= K, s < K) re-derived; (s-K)^+ - (K-s)^+ = s-K."),
    ("L06-remark-1.2-put-call-parity", "2.9-DAG", "course/modules/PC/PC3/L06.html lines 68-71",
     "PASS", "FC2 L07 Proposition 1.4 proof states C - P = S - K e^{-r tau} under A1 to A5, matching the price form cited here; the lesson defers to the linked module and does not re-derive it."),
    ("L06-definition-1.3-NPV-and-prop-3.1", "2.4-mathematics", "course/modules/PC/PC3/L06.html lines 73-76, 110-118",
     "PASS", f"NPV formula matches CF1 L01 Definition 1.1 (sum of C_t/(1+r)^t). Proposition 3.1 identity NPV(u) = -I + mAu checked on 300 random inputs ({O}/l06_indep.out)."),
    ("L06-prop-2.1-forward", "2.4-mathematics", "course/modules/PC/PC3/L06.html lines 90-98",
     "PASS", "Parts (i) and (ii) re-derived. Reverse-portfolio payoff S/D - F' > 0 in every state, as A4 requires for the contradiction."),
    ("L06-remark-2.2-continuous-convention", "2.9-DAG", "course/modules/PC/PC3/L06.html lines 86, 101-104",
     "PASS", "FC2 L02 Definition 2.1 gives F* = S e^{r tau}, and the discount factor e^{-r tau}. CF1 NPV is discrete. The discrete-versus-continuous statement (line 309) matches both linked modules."),
    ("L06-corollary-3.3-grade", "2.4-mathematics", "course/modules/PC/PC3/L06.html lines 130-139",
     "PASS", f"Sign argument: NPV(u) = mA(u - u*), so l < u* < h gives a loss at l and a gain at h. Example 4.2 range [200,1600] straddles 1206.34 ({O}/l06_indep.out)."),
    ("L06-prop-3.2-fermi-bounds", "2.4-mathematics", "course/modules/PC/PC3/L06.html lines 120-128",
     "PASS", f"Induction re-read. 20,000 random interior factor draws lie in [200,1600]; ends attained at (2000,1,1/10) and (4000,2,1/5) ({O}/l06_indep.out)."),
    ("L06-example-4.2-numbers", "2.2-numbers", "course/modules/PC/PC3/L06.html lines 146-150",
     "PASS", f"A = 3310/1331; u* = 399300/331 = 1206.3444; range [200,1600]; NPV(200) = -16655000000/1331 = -12513148 cents; NPV(1600) = 4894816 cents ({O}/l06_indep.out)."),
    ("L06-remark-4.3-sensitivity", "2.2-numbers", "course/modules/PC/PC3/L06.html lines 153-155",
     "PASS", f"Unrounded break-evens 1164.1005, 1206.3444, 1249.0469. Differences 42.2439 (shown 42.24) and 42.7025 (shown 42.70). NPV at 200 negative and at 1600 positive at all three rates ({O}/l06_indep.out)."),
    ("L06-E1-12pct", "2.2-numbers", "course/modules/PC/PC3/L06.html lines 395-401",
     "PASS", "Annuity 2.40183 at 12 percent; 3000 / 2.40183 = 1249.05 (l06_indep.out, E1 line)."),
    ("L06-E2-first-negative", "2.2-numbers", "course/modules/PC/PC3/L06.html lines 402-408",
     "PASS", "NPV(1200) = -105000000/1331 = -78888.05; NPV(1300) = 1550000000/1331 = 1164537.94; positive grid points 1300, 1400, 1500, 1600 (four); largest negative point 1200."),
    ("L06-E3-42.71", "2.2-numbers", "course/modules/PC/PC3/L06.html lines 410-416",
     "PASS", "Width 84.9464 (shown 84.95); /4 = 21.2366 (shown 21.24); 8-to-10 42.2439 (shown 42.24); 10-to-12 42.7025 (shown 42.70); displayed-value difference 42.71 is not the answer."),
    ("L06-E3-rest-and-quiz-q9", "2.2-numbers", "course/modules/PC/PC3/L06.html lines 409-416 and quiz item 9 (lines 518-522)",
     "PASS", "Quiz item 9 key 21.24 with tolerance 0.01 against 21.2366: within tolerance."),
    ("L06-M1-M3-numbers", "2.2-numbers", "course/modules/PC/PC3/L06.html lines 342-366",
     "PASS", f"M1: 5000 and 50 cents. M2: 500/121 = 4.1322. M3: 33275/331 = 100.5287 ({O}/l06_indep.out)."),
    ("L06-P1-P3-proofs", "2.4-mathematics", "course/modules/PC/PC3/L06.html lines 367-390",
     "PASS", "P1 reverse portfolio (cost 0, payoff S/D - F'); P2 unique zero from the affine form; P3 product bounds 200 and 1600 with attained ends. Re-derived by hand."),
    ("L06-R1-R3", "2.2-numbers", "course/modules/PC/PC3/L06.html lines 417-437",
     "PASS", f"R1: each factor ratio 2, so each log-width is ln 2 and the factors tie. R2: closed form u* = I / sum m_t (1+r)^-t. R3: m* = 3769.83 cents, ratio 0.75397, fall 24.6 percent ({O}/l06_indep.out)."),
    ("L06-quiz-answers", "2.9-prose", "course/modules/PC/PC3/L06.html lines 458-533",
     "PASS", "Ten items. Numeric keys 5000, 4.13 (tolerance 0.005 against 4.1322), 1206.34 (tolerance 0.005 against 1206.3444), 4, 21.24 (tolerance 0.01 against 21.2366) re-derived. Multiple-choice keys correct."),
    ("L06-canon-breaks-and-misconceptions", "2.9-prose", "course/modules/PC/PC3/L06.html lines 307-334",
     "PASS", f"Printed break-evens 1164.10, 1206.34, 1249.05; 21.24 per point; sign at the bounds is the same at all three rates ({O}/l06_indep.out and the lab output lines 301-303)."),
    ("L06-DAG-and-cross-links", "2.9-DAG", "course/modules/PC/PC3/L06.html lines 38-39, 56, 75, 86",
     "PASS", "L01.html#def-fermi-estimation exists (L01.html defines def-fermi-estimation). forward-contract, cost-of-carry, put-call-parity, net-present-value, statement-articulation are in the closure (FC2, CF1, AC1)."),
    ("L06-articulation-claim-linked", "2.9-DAG", "course/modules/PC/PC3/L06.html line 75 and quiz item 10 (lines 523-531)",
     "PASS", "AC1 L03 Definition 1.1: 'the cash-flow statement ends at the balance-sheet cash'. Line 75 and quiz key 'Balance-sheet cash' match it."),
    ("L06-footer-registry-claim", "2.9-prose", "course/modules/PC/PC3/L06.html line 548 (site-footer)",
     "PASS", "Footer claim holds: rows 1-6 are T (proved on the page) or T with Lab 1, Part 2 as a computed source."),
    ("L06-structure-hours", "2.9-prose", "course/modules/PC/PC3/L06.html (whole file)",
     "PASS", "data-hours=6. Section order matches BUILDER_RULES 4.2. Why-it-matters is 76 words. Four misconceptions. Twelve problems (three per tier). Ten quiz items. No debate key."),
]


def main() -> None:
    fragment = {
        "unit": "PC3",
        "slice": "PC3-b",
        "round": 10,
        "verifier": "Claude Haiku 5.5, independent verifier for PC3-b round 10 (did not build PC3)",
        "pin": "00a84795f276456fce19d4181373cc4efba11a36",
        "base": "c93dd526025c6dffd34c54cd2c89eb62a890f885 (round-9 pin). Delta c93dd526..00a84795 does not touch course/modules/PC/PC3/L04.html, L05.html, L06.html or tests/labs/PC3/lab-PC3-L04-1.py, lab-PC3-L05-1.py, lab-PC3-L06-1.py (byte-identical), nor tools/, notation/, references/, BUILDER_RULES.md, plans/PC3-build-plan.md. Every round-9 row was re-verified from scratch this round; none is carried.",
        "checkout": str(ROOT),
        "scratch": f"{ROOT}/{O}",
        "verified_at": "2026-11-05T08:26:13+00:00",
        "verdict": "FAIL",
        "rows": [
            {"id": i, "check": c, "location": loc, "status": st, "evidence": ev,
             **({"fix": ev.split("FIX: ", 1)[1]} if st != "PASS" else {})}
            for (i, c, loc, st, ev) in ROWS
        ],
        "mutants": [],
        "registry_flags": [],
        "freshness_flags": [],
        "notes": [
            "Slice b: course/modules/PC/PC3/L04.html, L05.html, L06.html and tests/labs/PC3/lab-PC3-L04-1.py, lab-PC3-L05-1.py, lab-PC3-L06-1.py. cards.json, project.html, the grader and the other lessons are outside this slice and are not checked here (project.html was read only for the arrival-split consistency row L04-A1-project-consistency).",
            "Mutants: none. Lab twins are demonstrations, and mutation testing applies to project graders only (architect ruling). No grader mutant is claimed.",
            "Independent recomputation: every numeric claim in the three lessons and the lab outputs was re-derived with stdlib scripts that do not import the lab code (l04_indep.py, l05_indep.py, l06_indep.py, l05_remark34_max_step_removals.py), with outputs in out/.",
            "Judgement recorded, not a row: the twin docstrings say 'Money is an integer number of cents' (L04 twin line 184; L06 twin line 165) while the NPV and expectation values printed are exact fractions of a cent (L06 line 297; L04 line 460). The plan's convention allows fractional expected values in labs, so I did not fail the sentence; a reword to 'inputs are integer cents' would remove the tension.",
            "Judgement recorded: the L04 Remark 4.2 clause 'the same distribution as at inventory 0' is read as the trade term's distribution for a fixed quote, which A1 and A5 support for |I| <= L-1. Not a finding.",
            "Judgement recorded: the L04 Proposition 3.1 interpretation at Lab 1 ('the proof covers every fair value for a fixed quote, from inventory zero') relies on H1 (positive-probability conditioning event). Read as citing the full H1. Not a finding.",
            "Round-9 notes stated 50 lines for the L04 expected block; the current block has 52 (embed_compare.out). The round-9 line numbers were round-8 numbers; all locators in this fragment are current-file numbers.",
            "The only FAIL is L05 Remark 3.4 'up to k-1 entries': the true maximum is k, shown by exhaustive search and by an explicit witness (see the row fix).",
        ],
        "summary": None,
    }
    counts = {"rows": len(fragment["rows"])}
    counts["pass"] = sum(1 for r in fragment["rows"] if r["status"] == "PASS")
    counts["fail"] = sum(1 for r in fragment["rows"] if r["status"] == "FAIL")
    counts["unverifiable"] = sum(1 for r in fragment["rows"] if r["status"] == "UNVERIFIABLE")
    fragment["summary"] = counts
    out = ROOT / "ledgers/PC3/PC3-b.json"
    out.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(out, counts)


if __name__ == "__main__":
    main()
