"""Build ledgers/PC3/PC3-b.json for PC3 slice b, round 11 (verifier output; stdlib only).

Rows carry the evidence named in each entry. Run from the checkout root after the scripts in this folder have run.
"""

from __future__ import annotations

import json
import subprocess
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path.cwd()
S = "ledgers/PC3/scripts/PC3-b-r11"
CARRY = "Carried from round 10 ({files} byte-identical since the previous pin): "
C5 = "course/modules/PC/PC3/L05.html"
C4 = "course/modules/PC/PC3/L04.html"
C6 = "course/modules/PC/PC3/L06.html"

R = []


def row(rid, check, location, status, evidence, fix=None):
    d = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        d["fix"] = fix
    R.append(d)


# ---- gates (re-run this round) ----
row("gate-run-labs-unit", "2.5-labs", "tools/run_labs.py --unit PC3", "PASS",
    "run_labs PC3: PASS (9/9), exit 0 (" + S + "/out/run_labs.out)")
row("gate-check-pages", "2.9-prose", "tools/check_pages.py --unit PC3", "PASS",
    "check_pages PC3: PASS, exit 0 (out/check_pages.out)")
row("gate-check-dag", "2.9-DAG", "tools/check_dag.py --unit PC3", "PASS",
    "check_dag PC3: PASS, exit 0 (out/check_dag.out)")
row("gate-check-projects", "2.6-structure", "tools/check_projects.py --unit PC3", "PASS",
    "check_projects PC3: PASS, exit 0 (out/check_projects.out)")
row("gate-page-smoke-slice", "2.9-prose", "tools/page_smoke.py --unit PC3 --pages L04 L05 L06 (run alone)", "PASS",
    "page_smoke PC3: PASS; L04, L05 and L06 each PASS; exit 0 (out/page_smoke.out)")
row("gate-ruff-mypy-twins", "2.5-labs", "ruff check tests/labs/PC3; ruff format --check tests/labs/PC3; mypy --no-incremental",
    "PASS", "'All checks passed!' (ruff check); '9 files already formatted' (ruff format); "
    "'Success: no issues found in 385 source files' (mypy, strict config). Outputs in out/ruff_check.out, "
    "out/ruff_format.out, out/mypy.out")
row("gate-pytest-lab-tooling", "2.5-labs", "pytest -q tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py",
    "PASS", "all tests pass, exit 0 (out/pytest_lab_tooling.out)")
row("gate-verify-refs-offline", "2.1-citations", "tools/verify_refs.py --offline (whole registry)", "PASS",
    "'offline integrity: 560 entries, 0 problems', exit 0 (out/verify_refs_offline.out). The slice cites no registry key; "
    "this is the registry integrity check only.")

# ---- notation ----
row("notation-registry-L04-L06", "2.4-notation", C4 + "; " + C5 + "; " + C6 + " (math spans)", "PASS",
    "Scan of all math spans (L04 370, L05 314, L06 245): no occurrence of T, Phi, gamma_3, gamma_4, R^ast, R^{e ast}, "
    "R_f or mathbb{Q}. Registered macros in use: E (L04 12x) and Var (L04 3x), both with the registry meaning. "
    "Local symbols, conventionally local per notation.json 'about': sigma (fill sign, L04 Section 2), varepsilon "
    "(fair-value move, Definition 1.1 step 1), tau (expiry, L06 Standing assumptions A1), ell (Fermi bounds, L06 "
    "Proposition 3.2). L04 writes the maximum size as bar q; the plan lists Q; no registry collision.")

# ---- twins ----
row("twin-run-alone-L04-L06", "2.5-labs",
    "tests/labs/PC3/lab-PC3-L04-1.py, lab-PC3-L05-1.py, lab-PC3-L06-1.py", "PASS",
    "python -I -W error on each twin: exit 0 and 0 stderr bytes (out/twin_lab-PC3-L04-1.stdout/.stderr, and L05, L06)")
row("twin-page-code-equals-twin", "2.5-labs", C4 + ", " + C5 + ", " + C6 + " code blocks vs the three twins", "PASS",
    "embed_compare.py (scripts/PC3-b-r11/embed_compare.py): code==twin True for L04, L05 and L06 (out/embed_compare.out)")
row("twin-expected-equals-stdout", "2.5-labs",
    C4 + " lines 424-475 (52 lines); " + C5 + " lines 307-331 (25); " + C6 + " lines 283-303 (21)", "PASS",
    "expected block equals the stdout of the twin run, line for line: L04 52, L05 25, L06 21 (out/embed_compare.out)")

# ---- labs: hypothesis and interpretation ----
row("lab-L04-1-hypothesis-interpretation", "2.5-labs", C4 + " line 180 (hypothesis), line 476 (interpretation)", "PASS",
    "Hypothesis: identity True, cash flow -9950, P&L 30 (stdout: 'identity ... True', '-9950 cents', 'P&L ... = 30'); "
    "nine fair values (stdout Part 2, 9980 to 10020); Part 3 mean 0 and variance 25 I^2 for five inventories (stdout). "
    "Interpretation: 9 fills, cash flow -9950, inventory 1, settlement 9980, P&L 30, 13 informed arrivals, seed 1 with "
    "16 fills, 20100, -2, 10020, 60 (all in stdout). Matches out/twin_lab-PC3-L04-1.stdout.")
row("lab-L05-1-hypothesis-interpretation", "2.5-labs", C5 + " line 163 (hypothesis), line 332 (interpretation)", "PASS",
    "Hypothesis: 200 integers 0 to 999 from Random(5); naive 1351 = (n-k+1)(k-1); deque at most 400 comparisons; 200 "
    "pushes; seed 6 at window 8; five edge checks True (stdout Part 2). Interpretation: 354 deque comparisons at window 8, "
    "within 400; seed-6 350 comparisons; outputs equal for windows 1 to 20 (stdout lines 'deque comparisons = 354', "
    "'seed 6: ... deque comparisons = 350', 'outputs equal for window sizes 1 to 20: True').")
row("lab-L06-1-hypothesis-interpretation", "2.5-labs", C6 + " line 159 (hypothesis), line 304 (interpretation)", "PASS",
    "Hypothesis: payoff 0 at quote 10000 and 100 at 10100 over five spot values (stdout Part 1); annuity 3310/1331, "
    "break-even 399300/331, NPV zero at break-even, NPV increasing on the grid, NPV at bounds and at 8, 10, 12 percent "
    "(stdout Part 2). Interpretation: break-evens 1164.10, 1206.34, 1249.05 (stdout). Differences 42.24 (8 to 10) and 42.71 "
    "(printed 1249.05 minus 1206.34) and, from unrounded values, 42.24 and 42.70 (out/l06_indep.out: 42.2439, 42.7025).")

# ---- L04 ----
row("L04-definitions-A1-A6-notation", "2.4-notation", C4 + " lines 56-89", "PASS",
    "Re-read in full. Line 56 declares N, t, p, L as local. Definition 1.1 (lines 59-68). A1 (line 72): p=1/2 gives "
    "1/4, 1/4, 1/2, matching ARRIVAL_PROBABILITY in the twin. A5 (line 76) with L=10 matches LIMIT in the twin. A6 "
    "(lines 69-80) gives a = m+h, b = m-h. Example 1.3 (lines 87-88): h=10, q=1, which matches the twin's quote().")
row("L04-lab-section-locator", "2.9-prose", C4 + " line 72 (A1), line 161 (Section 4 heading), line 178-179 (Lab 1)", "PASS",
    "Lab 1 sits inside Section 4 (heading at line 161, lab at 178), so 'Lab 1 (Section 4)' in A1 and 'Lab 1, Section 4' "
    "in Example 1.3 are accurate.")
row("L04-prop-2.2-2.3-identity", "2.4-mathematics", C4 + " lines 100-122", "PASS",
    "Proposition 2.2 (lines 101-106): induction gives C_t = sum c_s and I_t = sum sigma_s, so W_N = sum c_t + (sum sigma_t) v_N. "
    "Proposition 2.3 (lines 111-116): W_t - W_{t-1} = (c_t + sigma_t v_t) + I_{t-1}(v_t - v_{t-1}); re-derived by hand. Remark 2.4 "
    "(line 121-122) checks against E3: 30 vs 40 cents (out/l04_indep.out).")
row("L04-example-3.2-values", "2.2-numbers", C4 + " line 143", "PASS",
    "E = 5 - (1/2)[(v-10010)^+ + (9990-v)^+]: v=10000 gives 5, v=10020 gives 0, v=9985 gives 5/2. Recomputed by "
    "l04_indep.py (out/l04_indep.out) and printed by the twin's Part 2 (stdout).")
row("L04-proposition-4.1-remark-4.2-sd", "2.2-numbers", C4 + " lines 164-175", "PASS",
    "Mean 0 and variance 25 I^2 (Proposition 4.1). SD = 5|I|: 15 cents at 3 units, 50 cents at 10 units (Remark 4.2 line 175). "
    "Twin Part 3 prints variance 225 at 3 and 2500 at 10 (stdout).")
row("L04-remark-4.2-inventory-independence", "2.4-mathematics", C4 + " line 175", "PASS",
    "The trade term equals its inventory-zero value for |I| <= 9 on the grid (out/l04_indep.out, 'Remark 4.2 trade term equal "
    "... True'). At I=10 and v=10000 the term is 5/2 (out/l04_indep.out, 'I=10, v=10000 ... 5/2'), as line 175 states.")
row("L04-remark-3.4-inventory-zero", "2.2-numbers", C4 + " lines 157-158", "PASS",
    "Uninformed flow earns (1-p)h (Proposition 3.1, cases (i) and (ii)). At p=1/2 this is h/2, a quarter of the spread 2h.")
row("L04-canon-breaks-tick", "2.9-prose", C4 + " lines 481-483 (Section 5, paragraphs 1-3)", "PASS",
    "Integer-cent quotes and 5-cent moves match Definition 1.1 and the twin (MOVE_CENTS = 5). 'Adverse selection' (line 482) is "
    "plain prose. 'Cannot show that a wider quote costs customers' (line 483) follows from A1 (arrival law independent of the quote).")
row("L04-canon-breaks-quote-rule", "2.4-mathematics", C4 + " line 484 (Section 5, paragraph 4)", "PASS",
    "Claim: mid at turn t is 10000 - 10 I_{t-1}, by induction on fills. Checked on seeds 0 to 199 and all turns "
    "(out/l04_indep.out, 'Section 5 mid claim ... True'). A3 (line 74) matches 'uses only the public history'.")
row("L04-R2-spread-criterion", "2.4-mathematics", C4 + " lines 597-601 (R2)", "PASS",
    "At v = m both brackets vanish, so E = (1-p)h (Proposition 3.1). With p fixed by A1: p<1 gives E>0 for every h>=1, and p=1 gives "
    "E=0 for every h, so no unique spread. The 'would have to change' claim is consistent: A1 is the assumption that fixes p.")
row("L04-E1-seed1-numbers", "2.2-numbers", C4 + " lines 565-571 (E1)", "PASS",
    "16 fills, cash flow 20100, inventory -2, settlement 10020, mark -20040, P&L 60. Equal to the twin's seed-1 line in stdout. "
    "Identity: 20100 - 20040 = 60.")
row("L04-E2-binomial-z", "2.2-numbers", C4 + " lines 572-578 (E2)", "PASS",
    "13/20 = 0.65; SE sqrt(0.25/20) = 0.1118; z = 0.15/0.1118 = 1.34 < 1.96 (out/l04_indep.out, 'E2 standard error = 0.111803, z = 1.3416').")
row("L04-E3-mid-vs-settlement", "2.2-numbers", C4 + " lines 579-586 (E3)", "PASS",
    "Seed-0 turn-20 quote 9980/10000 (stdout row 20), mid 9990, final inventory 1, cash flow -9950, settlement 9980: P&L 30 "
    "at settlement, 40 at mid, difference 10 (out/l04_indep.out).")
row("L04-problems-R1-R3-M-P", "2.4-mathematics", C4 + " lines 515-607 (M1 515, M2 522, M3 529-532, P1 540, P2 547, P3 554, E1-E3 565-586, R1 590, R2 597, R3 604)", "PASS",
    "M1: W = 10. M2: sell refused (|11| > 10), buy fills (|9|). M3 (inventory 0 stated at line 530): no trade at 10010, loss of 1 cent "
    "at 10011. P1: identity for N=2. P2: E = h/2 at a, 0 at a+h. P3: Var = 25 I^2 = 400 at I=-4. E1-E3 as above. R1: d = (1-p)h/p = 20/3. "
    "R2: as above. R3: 25 I^2 < 100 gives |I| <= 1, variance 25. Re-derived each.")
row("L04-M3-inventory-hypothesis", "2.9-prose", C4 + " lines 529-532 (M3, changed in this delta)", "PASS",
    "Hypothesis added: 'The inventory before the turn is 0'. The solution uses A4 only (tests v_t against a_t and b_t), so the "
    "added hypothesis matches what the solution assumes. Results unchanged: no trade at 10010; c + sigma v = 10010 - 10011 = -1 at 10011.")
row("L04-quiz-q11-citation", "2.9-prose", C4 + " lines 706-709 (quiz item 11)", "PASS",
    "Answer 9 matches 'fills 9 of 20 turns' (stdout, Part 1). The explanation cites Lab 1, Part 1, correctly.")
row("L04-quiz-answers", "2.9-prose", C4 + " lines 632-720 (12 items)", "PASS",
    "Q1 +10010 (A1 buy at ask); Q2 10; Q3 no trade at v=a (strict A4); Q4 0; Q5 5; Q6 refused (|11| > 10); Q7 400; Q8 mean zero; "
    "Q9 20/3 (tolerance 0.001 covers 6.6667); Q10 v_N; Q11 9; Q12 rises as (1-p)h. Each explanation supports its answer.")
row("L04-key-results-prop-3.1-assumptions", "2.9-prose", C4 + " line 622", "PASS",
    "Key-results row cites Proposition 3.1 under A1, A2, A4, A5, A6 and H1 to H3, with the fixed-quote qualification. Matches the "
    "hypotheses at lines 128-129.")
row("L04-prop-3.1-closed-form", "2.4-mathematics", C4 + " lines 127-139", "PASS",
    "Cases (i)-(iii) and the probability weights sum to (1-p)/2 (a-b) - p[...] = (1-p)h - p[...], since a-b = 2h. Hypotheses H1-H3 "
    "and the fixed-quote restriction are stated. No gap found.")
row("L04-corollary-3.3", "2.4-mathematics", C4 + " lines 146-154", "PASS",
    "p=1/2 and v>=a gives E = h/2 - (v-a)/2, zero iff v = a+h. Enumeration over 10010..10040 gives zero only at 10020 "
    "(out/l04_indep.out, 'zeros for v in 10010..10040 ... [10020]').")
row("L04-misconceptions", "2.9-prose", C4 + " lines 487-507 (four items)", "PASS",
    "Item 1 (spread on every trade) answered by (1-p)h and the 0 at 10020 (stdout). Item 2: cash flow 10010 but P&L 10 (M1). "
    "Item 3: variance 2500 at 10 units (stdout). Item 4: A3. Four misconceptions, three required.")
row("L04-key-results-table-other", "2.9-prose", C4 + " lines 620-629 (rows 1, 2, 5, 6)", "PASS",
    "Row 1 Proposition 2.2 (T), row 2 Proposition 2.3 (T), row 5 Proposition 4.1 (T, under A2), row 6 nine-value enumeration graded C "
    "naming Lab 1 Part 2 (lab-read results are C per the rules).")
row("L04-scope-and-banned-phrases", "2.9-prose", C4 + " (whole file)", "PASS",
    "check_pages PASS (banned phrases, out/check_pages.out). Scope-word scan of prose (every, all, always, never, any, same, only, "
    "exactly): each hit is a definition, a stated assumption, a proof step, or a lab-computed claim. Process words absent (grep).")
row("L04-structure-hours", "2.9-prose", C4 + " (whole file); course/modules/PC/PC3/index.html", "PASS",
    "Order: why-it-matters (52, 119 words), Sections 1-4, Lab 1 (178), Section 5 (480), Section 6 (488), Section 7 (510; three problems "
    "in each tier), Section 8 (615), Section 9 (632), Section 10 (724). data-hours 6 and eyebrow '6 study hours'. Hub: 6 lessons "
    "x 6 = 36 hours plus 14 project hours = 50 (curriculum.json PC3 hours 50; index.html data-hours-lessons 36).")
row("L04-DAG-D-terms", "2.9-DAG", C4 + " lines 60, 157-158, 482; out/check_dag.out", "PASS",
    "'adverse selection' appears at 157-158 and 482 as plain prose with no dfn and no link (plan D3). Bayes, martingale, inventory "
    "model, Kelly, Poisson, Markov absent (scan). Linked concepts: expected-value-game (L03), expectation (M4), market-maker, "
    "bid-ask-spread, limit-order-book (FC1): all in the closure or in the unit.")
row("L04-A1-project-consistency", "2.4-notation", C4 + " line 72; " + "course/modules/PC/PC3/project.html lines 53 and 404", "PASS",
    "project.html line 404 gives the same outcome probabilities (1/4, 1/4, 1/2). Line 53 says a fill is one unit at the bid or the ask "
    "and that the trading rules are those of Lesson 4 (the informed-trader rule is defined in the project conventions, outside this slice).")
row("L04-footer-registry-claim", "2.9-prose", C4 + " line 736 (site-footer)", "PASS",
    "'Each key result is proved on the page or computed by Lab 1, and each is graded.' Every key-results row carries a grade.")

# ---- L05 ----
row("L05-def-3.1-markup", "2.4-mathematics", C5 + " lines 105-106 (Definition 3.1)", "PASS",
    CARRY.format(files=C5 + " lines 105-106") +
    "the only L05 hunk in the delta is line 147. Definition 3.1 (strict x_j > x_m) matches the pseudocode (pop when back <= x_i).")
row("L05-prop-2.1-2.2-remark", "2.2-numbers", C5 + " lines 85-98", "PASS",
    CARRY.format(files=C5 + " lines 85-98") + "(n-k+1)(k-1) and Remark 2.2 peak n^2/4 re-checked (out/l05_indep.out).")
row("L05-prop-3.2-correctness", "2.4-mathematics", C5 + " lines 123-133", "PASS",
    CARRY.format(files=C5 + " lines 123-133") + "invariant and front-is-maximum proof re-read; l05_indep.out 'Prop 3.2 ... all pass' over 21324 cases.")
row("L05-prop-3.3-bound", "2.4-mathematics", C5 + " lines 135-142", "PASS",
    CARRY.format(files=C5 + " lines 135-142") + "appends = n, removals <= n, tests <= 2n (l05_indep.out, 400 random sequences).")
row("L05-remark-3.4-k-range", "2.2-numbers", C5 + " line 147 (Remark 3.4, first sentences)", "PASS",
    "Round 10 FAIL ('up to k-1') is fixed. Now: up to k entries. Checked by scripts/PC3-b-r11/l05_remark34_r11.py (out/l05_remark34_r11.out): "
    "for k=1..10 the witness x=(k,...,1,k+1), n=k+1 leaves the deque 1..k after step k, and step k+1 removes exactly k indices; "
    "exhaustive search over n<=7 with values 0..k+1 gives largest one-step removal = k for k=1..4; before step i the deque lies in "
    "{i-k..i-1} and every removal is from that set (0 violations). The bound k holds and is attained.")
row("L05-example-3.5-trace", "2.2-numbers", C5 + " lines 151-153", "PASS",
    CARRY.format(files=C5 + " lines 151-153") + "re-traced by hand: deques (1), (1,2), (3), (3,4), (5); outputs (4,4,5), as in out/l05_indep.out.")
row("L05-problems-M-P", "2.4-mathematics", C5 + " lines 367-413 (M1-M3, P1-P3)", "PASS",
    CARRY.format(files=C5 + " lines 367-413") + "M1 21, M2 outputs (5,5,1,3), P1 k=101 at n=200, P2 and P3 proofs re-read (l05_indep.out 'Problem M2').")
row("L05-E1-E3-numbers", "2.2-numbers", C5 + " lines 417-437", "PASS",
    CARRY.format(files=C5 + " lines 417-437") + "5239/382 = 13.7; 387 <= 400; 194 pops (l05_indep.out 'E1 ratio', 'E3 k=200').")
row("L05-E2-seed6-numbers", "2.2-numbers", C5 + " lines 424-430", "PASS",
    CARRY.format(files=C5 + " lines 424-430") + "seed 6: 350 comparisons, 200 pushes, 197 pops (l05_indep.out, 'seed6 k=8').")
row("L05-R1-scope-sentence", "2.9-prose", C5 + " lines 440-448", "PASS",
    CARRY.format(files=C5 + " lines 440-448") + "the lesson makes no timing claim; the counts are model counts.")
row("L05-R2-R3", "2.2-numbers", C5 + " lines 449-462", "PASS",
    CARRY.format(files=C5 + " lines 449-462") + "R2 = 10000 at k=101; R3 strictly increasing gives n-1 (Problem P3).")
row("L05-key-results-grades", "2.3-grades", C5 + " lines 466-481", "PASS",
    CARRY.format(files=C5 + " lines 466-481") + "T for proved results, C for the lab-read seed-5 agreement (rule 9).")
row("L05-quiz-answers", "2.9-prose", C5 + " lines 483-563 (quiz items 1-12)", "PASS",
    "Re-verified in full (items 4 and 6 to 10 reference Remark 3.4 or Proposition 3.3): item 1 21; item 2 400; item 4 'yes, total bound "
    "counts all removals' (each index leaves at most once); item 6 n-1; item 7 last occurrence of ties; item 8 1351; item 9 counts not times; "
    "item 10 no outputs. Answers and explanations consistent with the text.")
row("L05-misconceptions-canon-breaks", "2.9-prose", C5 + " lines 336-359", "PASS",
    "Re-verified: 'a single step can cost of order k, as Remark 3.4 shows' now matches the corrected remark (k removals). "
    "354 within 400. The amortised-bound paragraph (line 339) matches Proposition 3.3.")
row("L05-structure-hours", "2.9-prose", C5 + " (whole file)", "PASS",
    "Order: why-it-matters (52, 91 words), Section 1 (54), Section 2 (81), Section 3 (100), Lab 1 (162), Section 4 (336), "
    "Section 5 (344), Section 6 (362, three problems per tier), Section 7 (467), Section 8 (484), Section 9 (566). data-hours 6.")
row("L05-markup-raw-less-than", "2.9-prose", C5 + " Definition 3.1 and math", "PASS",
    CARRY.format(files=C5 + " Definition 3.1 and math") + "less-than signs are escaped as &lt; in math and definitions.")
row("L05-meta-uses-hash-map-heap", "2.9-DAG", C5 + " lines 38-40 and Remark 3.6 lines 157-158", "PASS",
    CARRY.format(files=C5 + " lines 38-40 and 157-158") + "hash-map, binary-heap and monotonic-deque are in the closure (CS2).")
row("L05-meta-uses-other", "2.9-DAG", C5 + " line 38 (Uses list)", "PASS",
    CARRY.format(files=C5 + " line 38") + "big-O (CS2) and unit-test (CS1) are in the closure.")
row("L05-why-it-matters-comparisons", "2.9-prose", C5 + " line 52", "PASS",
    CARRY.format(files=C5 + " line 52") + "'at most twice the input length in comparisons' matches Proposition 3.3.")
row("L05-footer-registry-claim", "2.9-prose", C5 + " line 578 (site-footer)", "PASS",
    CARRY.format(files=C5 + " line 578") + "every key result is graded and proved or computed.")
row("L05-DAG-links", "2.9-DAG", C5 + " lines 38, 58, 106, 157-158", "PASS",
    CARRY.format(files=C5 + " lines 38, 58, 106, 157-158") + "links resolve to closure concepts.")
row("L05-card-PC3-c092", "2.7-cards", "course/modules/PC/PC3/cards.json id PC3-c092 vs " + C5 + " line 147", "PASS",
    "Card changed in this delta. Front: x=(k,...,1,k+1), n=k+1, step k+1 removes k entries. Back: all k, deque holds 1..k, value k+1 "
    "at index k+1 exceeds all. Matches the corrected remark (line 147). Other cards are outside this slice (see could-not-check).")

# ---- L06 ----
row("L06-prop-1.1-payoff-identity", "2.4-mathematics", C6 + " lines 58-66", "PASS",
    "(s-K)^+ - (K-s)^+ = s-K, both cases re-derived (proof lines 63-64).")
row("L06-remark-1.2-put-call-parity", "2.9-DAG", C6 + " lines 68-71", "PASS",
    "Price form C - P = S - DK with D = e^{-r tau} is stated in FC2 L05 line 59 (def-put-call-parity). The lesson links, does not re-derive.")
row("L06-definition-1.3-NPV-and-prop-3.1", "2.4-mathematics", C6 + " lines 73-76, 110-118", "PASS",
    "NPV formula sum C_t (1+r)^-t matches CF1 L01 (line 59). Proposition 3.1: NPV(u) = -I + mAu; strictly increasing; u* = I/(mA); re-derived.")
row("L06-prop-2.1-forward", "2.4-mathematics", C6 + " lines 90-98", "PASS",
    "(i) zero-cost portfolio paying F' - S/D in every state; (ii) no-arbitrage in both directions under A4 and A5. Re-derived each branch.")
row("L06-remark-2.2-continuous-convention", "2.9-DAG", C6 + " lines 80-90 (A2) and 102-104 (Remark 2.2)", "PASS",
    "S/D = S e^{r tau} with D = e^{-r tau}, the cost-of-carry forward of FC2 L02 line 88 (F* = S e^{r tau}). The discrete NPV and "
    "continuous forward conventions in the canon section are stated accurately.")
row("L06-corollary-3.3-grade", "2.4-mathematics", C6 + " lines 130-139", "PASS",
    "If l < u* < h the sign is not fixed; if h < u* or l > u* the whole range has one sign. Proof uses Proposition 3.1 (linear NPV) and 3.2 (ends attained).")
row("L06-prop-3.2-fermi-bounds", "2.4-mathematics", C6 + " lines 120-128", "PASS",
    "Induction on k with positive bounds; ends attained by extreme choices. Re-derived.")
row("L06-example-4.2-numbers", "2.2-numbers", C6 + " lines 146-150", "PASS",
    "Units range [200, 1600] = 2000x1x(1/10) to 4000x2x(1/5). A = 3310/1331 (l06_indep.out, 2.486852). u* = 399300/331 = 1206.3444. "
    "NPV at 200 is -12513148 cents and at 1600 is +4894816 cents (twin stdout). Assumptions (10%, no tax, no salvage) as stated.")
row("L06-remark-4.3-sensitivity", "2.2-numbers", C6 + " lines 153-155", "PASS",
    "Unrounded break-evens 1164.1005, 1206.3444, 1249.0469 (out/l06_indep.out). Differences 42.2439 (8 to 10) displays 42.24; 42.7025 "
    "(10 to 12) displays 42.70. The NPV signs at 200 and 1600 hold at all three rates (twin stdout).")
row("L06-E1-12pct", "2.2-numbers", C6 + " lines 392-398", "PASS",
    "Annuity factor at 12% = 2.40183 (1/1.12 + 1/1.2544 + 1/1.404928); break-even 3000/2.40183 = 1249.05. Matches the printed value.")
row("L06-E2-first-negative", "2.2-numbers", C6 + " lines 399-405", "PASS",
    "NPV(1200) = -105000000/1331 = -78888.05; NPV(1300) = 1550000000/1331 = 1164537.94 (out/l06_indep.out, 'E2'). Four positive grid points; 1200 the largest negative.")
row("L06-E3-42.71", "2.2-numbers", C6 + " lines 406-416", "PASS",
    "Width 1249.0469 - 1164.1005 = 84.9464 (displays 84.95). Average 84.9464/4 = 21.2366 (displays 21.24). 8 to 10: 42.2439 (42.24); "
    "10 to 12: 42.7025 (42.70). The displayed-value difference 42.71 is explicitly not the answer.")
row("L06-E3-rest-and-quiz-q9", "2.2-numbers", C6 + " lines 406-416 and quiz item 9", "PASS",
    "Quiz item 9 (21.24, tolerance 0.01) equals 21.2366 rounded. Explanation's '84.95 over four points' is the displayed width, divided "
    "from the unrounded 84.9464 as the rule states.")
row("L06-M1-M3-numbers", "2.2-numbers", C6 + " lines 342-362", "PASS",
    "M1: 4900/0.98 = 5000; payoff 50. M2: 500/121 = 4.1322 (exact). M3: 33275/331 = 100.5287. Re-derived (out/l06_indep.out, 'M2', 'M3').")
row("L06-P1-P3-proofs", "2.4-mathematics", C6 + " lines 367-390", "PASS",
    "P1 reverse portfolio: cost 0, payoff S/D - F' in every state (A2, A3, A5). P2: affine with slope mA > 0, one zero. P3: product "
    "bounds 200 and 1600, both ends attained. Re-derived.")
row("L06-R1-R3", "2.2-numbers", C6 + " lines 417-437", "PASS",
    "R1: log-width of each factor is ln 2 (ratios 2, 2, 2), so the factors tie. R2: u* = I / sum m_t (1+r)^-t. R3: m* = 3769.8263 cents, "
    "ratio 0.75397 (displays 0.7540), fall 24.603% (displays 24.6). Re-derived (out/l06_indep.out, 'R3 margin').")
row("L06-quiz-answers", "2.9-prose", C6 + " lines 459-533 (10 items)", "PASS",
    "Q1 5000; Q2 F' - S/D; Q3 S/D; Q4 4.13 (500/121 = 4.1322, tolerance 0.005); Q5 1206.34 (1206.3444, tolerance 0.005); Q6 nothing "
    "decided; Q7 4; Q8 rises strictly; Q9 21.24; Q10 balance-sheet cash. Each explanation supports its answer.")
row("L06-canon-breaks-and-misconceptions", "2.9-prose", C6 + " lines 308-334", "PASS",
    "Canon: 'factor of 8' = 1600/200 with three factors each varying by 2. Misconception 2 '21.24 per point' = (1249.0469-1164.1005)/4. "
    "Misconception 3 and 4 values match the twin's stdout (sign at 200 and 1600 at all three rates).")
row("L06-DAG-and-cross-links", "2.9-DAG", C6 + " lines 38-39, 56, 75, 86", "PASS",
    "Links: forward-contract (FC2 L02 line 59), cost-of-carry-forward-price (FC2 L02 line 88), put-call-parity (FC2 L05 line 59), "
    "net-present-value (CF1 L01 line 59), statement-articulation (AC1 L03 line 57), fermi-estimation (PC3 L01). All in the closure "
    "{AC1, CF1, CS1, CS2, E1, FC1, FC2, M1, M2, M4, P0.1} or earlier in the unit; check_dag PASS.")
row("L06-articulation-claim-linked", "2.9-DAG", C6 + " line 75 and quiz item 10", "PASS",
    "AC1 L03 (statement-articulation, line 57) states 'the cash-flow statement ends at the balance-sheet cash'. The lesson's use of that "
    "identity matches it.")
row("L06-footer-registry-claim", "2.9-prose", C6 + " line 548 (site-footer)", "PASS",
    "Footer claim matches the key-results table, where every row carries a grade.")
row("L06-structure-hours", "2.9-prose", C6 + " (whole file); course/modules/PC/PC3/index.html", "PASS",
    "Order: why-it-matters (52, 81 words), Sections 1-4, Lab 1 (158), Section 5 (308), Section 6 (315), Section 7 (337; three problems per tier), "
    "Section 8 (442), Section 9 (459), Section 10 (536). data-hours 6. Hub hours 36 + 14 = 50.")
row("L06-why-it-matters-scope", "2.9-prose", C6 + " line 52 (why-it-matters) against lines 424-436 (R2, R3)", "FAIL",
    "The sentence reads: 'reports how the answer moves when the rate moves, the one assumption it varies'. The lesson also varies the margin: "
    "R3 (lines 431-436) solves for the margin m* = 15000000 x 1331 / (1600 x 3310), about 3769.8 cents (a 24.6 percent fall) that moves the "
    "break-even to 1600 units, and R2 (lines 424-429) varies the margin path. 'The one assumption it varies' is therefore false as written. "
    "Scope word 'one' without a computation that supports it (verifier rule 4).",
    "Change the clause to 'reports how the answer moves when the rate moves (Remark 4.3)', removing 'the one assumption it varies'. "
    "If the margin is to be named, say it too: 'and what margin would move the break-even to the top of the range (Problem R3)'. "
    "Keep the why-it-matters paragraph at 120 words or fewer.")
row("L06-lab-docstring-money-integer", "2.5-labs", "tests/labs/PC3/lab-PC3-L06-1.py line 6 (docstring); " + C6 + " line 165 (same text in the page code block)", "FAIL",
    "Docstring: 'Prices, cash flows and the outlay are integer numbers of cents.' Part 2 evaluates npv(cash_flows(break_even), RATE) with "
    "break_even = 399300/331 (twin line 97). At that break-even the cash flows are -15000000 and 1996500000/331 = 6031722.05 cents in each of "
    "years 1 to 3: 3 of 4 flows are not integer cents (scripts/PC3-b-r11/money_integer_check_r11.py, out/money_integer_check_r11.out). "
    "The docstring is a claim about the code's values, so it fails (verifier defect class 2, which includes docstrings).",
    "Replace line 6 with: 'Prices and the outlay are integer numbers of cents. A cash flow at a fractional number of units, such as the "
    "break-even, is an exact fraction of a cent.' Then run tools/embed_labs.py course/modules/PC/PC3/L06.html --refresh lab-PC3-L06-1 "
    "(the printed output does not change), and re-run run_labs, page_smoke for L06, and embed_compare.")

# ---- L04 lab docstring (changed this delta; re-verified) ----
row("L04-lab-docstring-money-integer", "2.5-labs", "tests/labs/PC3/lab-PC3-L04-1.py lines 3-6 and " + C4 + " line 184 (same text)", "PASS",
    "Docstring: 'Quotes, cash flows and inventory marks are integer numbers of cents.' Checked by re-running the game on seeds 0 to 199 "
    "with an independent loop: 0 non-integer quotes, fill cash flows or inventory marks (out/money_integer_check_r11.out). Expectations and "
    "variances are described as fractions and are, per the twin's Part 2 and Part 3 output.")

FRAG = {
    "unit": "PC3",
    "slice": "PC3-b",
    "round": 11,
    "verifier": "Claude Haiku 5.5, independent verifier for PC3-b round 11 (did not build PC3)",
    "pin": "11d7077a290f7960b183d3a5a6631af4773888f9",
    "base": "00a84795f276456fce19d4181373cc4efba11a36 (round-10 pin). Delta 00a84795..11d7077 touches, in this slice: "
            "course/modules/PC/PC3/L04.html (lines 181-189 lab docstring; M3 at 529-532), L05.html (line 147, Remark 3.4), "
            "L06.html (line 52 why-it-matters; lines 162-170 lab docstring), tests/labs/PC3/lab-PC3-L04-1.py (lines 3-6), "
            "tests/labs/PC3/lab-PC3-L06-1.py (lines 6-8). lab-PC3-L05-1.py is byte-identical. Outside the slice and read only where a "
            "slice row cites them: cards.json (PC3-c023, PC3-c092), project.html (line 53, lines 397 and 625-627), "
            "grader/test_project.py, plans/PC3-build-plan.md, references/references.json.",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE11-PC3-b",
    "scratch": "/Users/billyribeiro/.fanout/wt/verifyE11-PC3-b/" + S + "/out",
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "verdict": "FAIL",
    "rows": R,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Slice b: L04.html, L05.html, L06.html and the three lab twins. Lab twins are demonstrations; no grader mutants apply "
        "(architect ruling), so mutants is empty.",
        "Full read: each of the three pages was read line by line (prose, problems, key results, quizzes); the twins were read in full. "
        "Locators are current-file numbers.",
        "Independent recomputation (stdlib only, no lab code imported): l04_indep.py, l05_indep.py, l06_indep.py (re-run, outputs in out/), "
        "l05_remark34_r11.py (new; the round-10 script's 'up to k-1' check is superseded), money_integer_check_r11.py (new), embed_compare.py (re-run).",
        "Judgement, not a row: L05 Remark 3.4 says 'At step k the deque holds indices 1..k ... and the value k+1 at index k+1 ... removes all k'. "
        "The removing step is step k+1 (the card says so). The sentence is accurate; 'at step k+1' in the first clause would remove the ambiguity.",
        "Judgement, not a row: L05 Remark 3.6 bounds a push by floor(log2 m) for the heap after the push (m entries). Read that way it is "
        "correct; a heap of m entries before the push would give floor(log2(m+1)). Not a finding.",
        "Judgement, not a row: L04 Section 1 says 'Money is an integer number of cents' (line 56) and the new twin wording for L04 is accurate "
        "(verified by script). No change needed.",
        "Round-10 locators for L04 were one line off after the lab docstring hunk; all locators in this fragment are current.",
    ],
    "summary": {},
}

FRAG["summary"] = {
    "rows": len(R),
    "pass": sum(1 for r in R if r["status"] == "PASS"),
    "fail": sum(1 for r in R if r["status"] == "FAIL"),
    "unverifiable": sum(1 for r in R if r["status"] == "UNVERIFIABLE"),
}

out = ROOT / "ledgers/PC3/PC3-b.json"
out.write_text(json.dumps(FRAG, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("wrote", out, FRAG["summary"])
