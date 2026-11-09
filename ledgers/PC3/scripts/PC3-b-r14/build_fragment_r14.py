"""Writes the round-14 verifier fragment for PC3 slice b (ledgers/PC3/PC3-b.json). Evidence is cited per row."""

import json
import pathlib
import sys

ROOT = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyE14-PC3-b")
OUT = "ledgers/PC3/scripts/PC3-b-r14/out/"
S = "ledgers/PC3/scripts/PC3-b-r14/"
rows = []


def P(rid, check, location, evidence):
    rows.append({"id": rid, "check": check, "location": location, "status": "PASS", "evidence": evidence})


def F(rid, check, location, evidence, fix):
    rows.append({"id": rid, "check": check, "location": location, "status": "FAIL", "evidence": evidence, "fix": fix})


# ---- 2.5 labs and gates (command rows run by the verifier on pin 8e5751c) ----
P("gate-run-labs-unit", "2.5-labs", "tools/run_labs.py --unit PC3",
  f"run_labs PC3: PASS (9/9) (exit 0) ({OUT}run_labs_unit.out)")
P("gate-check-pages", "2.9-prose", "tools/check_pages.py --unit PC3",
  f"check_pages PC3: PASS (exit 0) ({OUT}check_pages.out)")
P("gate-check-dag", "2.9-DAG", "tools/check_dag.py --unit PC3",
  f"check_dag PC3: PASS (exit 0) ({OUT}check_dag.out)")
P("gate-check-projects", "2.6-structure", "tools/check_projects.py --unit PC3",
  f"check_projects PC3: PASS (exit 0) ({OUT}check_projects.out); project grader is another slice")
P("gate-page-smoke-slice", "2.9-prose", "tools/page_smoke.py --unit PC3 --pages L04 L05 L06 (run alone)",
  f"page_smoke: L04, L05, L06 each PASS; page_smoke PC3: PASS, exit 0; lab runtimes 0.0 s ({OUT}page_smoke_L456.out)")
P("gate-ruff-mypy-twins", "2.5-labs", "ruff check tests/labs/PC3; ruff format --check tests/labs/PC3; mypy --no-incremental",
  f"ruff check: 'All checks passed!' exit 0 ({OUT}ruff_check.out); ruff format: '9 files already formatted' exit 0 ({OUT}ruff_format.out); mypy: 'Success: no issues found in 385 source files' exit 0 ({OUT}mypy.out)")
P("gate-pytest-lab-tooling", "2.5-labs", "pytest -q tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py",
  f"exit 0, no failures ({OUT}pytest_lab_tooling.out; the -q output is dots only, and the exit code is recorded in {OUT}ALL_EXIT.txt)")
P("gate-verify-refs-offline", "2.1-citations", "tools/verify_refs.py --offline (whole registry)",
  f"offline integrity: 560 entries, 0 problems, exit 0 ({OUT}verify_refs_offline.out); L04-L06 pages cite no key (ol data-references is empty; cards cite [] in {OUT}cards_L456_r14.txt)")
P("gate-run-graders-unit", "2.6-structure", "tools/run_graders.py --unit PC3 --seeds 0-49",
  f"run_graders PC3: PASS (reference 50/50 seeds), exit 0 ({OUT}run_graders_unit.out); recorded, grader is another slice")
P("notation-registry-L04-L06", "2.4-notation", "course/modules/PC/PC3/L04.html, L05.html, L06.html (math spans) vs notation/notation.json",
  f"Registry symbols: T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{{e\\ast}}, R_f, \\mathbb{{Q}}. grep of the three pages finds no math use of any of them (only grade labels 'T' at L0x.html line 44 and in key-results cells). Registered macros used: \\E (L04 lines 129, 170, 558, 622, 690) and \\Var (L04 lines 170, 556, 558); grep output in {OUT}notation_grep_r14.txt. Lesson-local symbols (N, t, p, L, v_t, b_t, a_t, q_t, I_t, C_t, W_t, sigma_t, c_t, f_t, epsilon_t, h, m_t; S, F, D, K, I, m, u, A, tau in L06) carry one meaning per lesson. Grep output in {OUT}notation_grep_r14.txt (command in the registry row's evidence file).")
P("twin-run-alone-L04-L06", "2.5-labs", "tests/labs/PC3/lab-PC3-L04-1.py, lab-PC3-L05-1.py, lab-PC3-L06-1.py",
  f"python -I -W error <twin>: exit 0, 0 stderr bytes for all three ({S}embed_check_r14.py; {OUT}embed_r14.out)")
P("twin-page-code-equals-twin", "2.5-labs", "L04.html data-run block vs tests/labs/PC3/lab-PC3-L04-1.py; L05.html vs lab-PC3-L05-1.py; L06.html vs lab-PC3-L06-1.py",
  f"html-unescaped data-run block equals the twin after the trailing newline is stripped (ruling: trailing newlines aside), for all three ({OUT}embed_r14.out). Byte-identity fails only on the final newline: the page block ends at 'main()' with no newline.")
P("twin-expected-equals-stdout", "2.5-labs", "L04.html pre.expected lines 424-475; L05.html 307-331; L06.html 284-304",
  f"stdout of the twin equals each expected block after rstrip (embed_r14.out; stdout files in {OUT}stdout_L0*_r14.txt; table rows checked by {S}table_check_r14.py: 20/20 L04 table rows match an independent replay)")

# ---- lab hypothesis/interpretation rows ----
P("lab-L04-1-hypothesis-interpretation", "2.5-labs", "L04.html line 180 (hypothesis), 476 (interpretation), code 181-423",
  f"Hypothesis claims identity True, cash flow -9950, P&L 30, nine grid values, variance 25 I^2: all match output lines 452, 447, 451, 459-469, 471-475 ({OUT}stdout_L04_r14.txt). Interpretation numbers (9 fills, -9950, inventory 1, settlement 9980, P&L 30, 13 informed arrivals, seed-1 16 fills / 20100 / -2 / 10020 / 60) match output lines 446-458 and the independent replay ({OUT}recompute_r14.out). Lab docstring (lines 183-202) says SIMULATED, seeded with 0, no network, and that the proof, not the grid, covers every fair value: consistent.")
P("lab-L05-1-hypothesis-interpretation", "2.5-labs", "L05.html line 163 (hypothesis), 332 (interpretation), code 164-306",
  f"Hypothesis: 200 values from random.Random(5) in 0..999; naive count 1351 = (200-8+1)(8-1); deque at most 2n = 400 with 200 pushes; Part 2 five edge-case checks all True (output lines 319-324); Part 3 five window sizes (lines 327-331). All match output and the independent replay ({OUT}recompute_r14.out). Interpretation counts 1351, 354, 350 match output lines 312-317.")
P("lab-L06-1-hypothesis-interpretation", "2.5-labs", "L06.html line 159 (hypothesis), 305 (interpretation), code 160-283",
  f"Hypothesis: forward price 10000, payoff 0 at 10000 and 100 at 10100 over spots 8000..12000; annuity 3310/1331; break-even 399300/331; exact zero NPV; increasing NPV; NPVs at bounds and at 8/10/12 percent. All match output lines 285-304. Interpretation: printed break-evens 1164.10, 1206.34, 1249.05; differences 42.24 and 42.71 printed, 42.24 and 42.70 unrounded: matches output and {OUT}recompute_r14.out.")

# ---- L04 ----
P("L04-definitions-A1-A6-notation", "2.4-mathematics", "L04.html lines 56 (symbols), 62-65 (Def 1.1), 72 (A1), 76 (A5), 77 (A6)",
  "A1 probabilities 1/4, 1/4, 1/2 at p=1/2 (line 72) re-derived; A5 fill rule q_t>=1 and |I|<=L after trade (line 76) matches the lab's play() test abs(inventory+side)<=LIMIT (lab line 295); A6 a=m+h, b=m-h matches quote() (lab line 263). Notation vs registry: no reuse (see notation-registry-L04-L06).")
P("L04-lab-section-locator", "2.9-prose", "L04.html line 72 and 83 ('Lab 1 (Section 4)'; 'unit project (Project · Market-making game)'); lab at line 178 under h2 s4 (line 161)",
  "Lab 1 sits inside Section 4 (h2 id=s4 line 161; lab section line 178): the locator is correct. The project's title is 'PC3 Project · Market-making game' (project.html line 6) and h1 'Market-making game' (line 36): the citation form is consistent with L06 next-link text (L06.html line 545).")
P("L04-prop-2.2-2.3-identity", "2.4-mathematics", "L04.html lines 101-108 (Prop 2.2 + proof), 111-118 (Prop 2.3 + proof)",
  "Re-derived: C_t = sum c_s, I_t = sum sigma_s by induction, so W_N = sum c_t + (sum sigma_t) v_N; W_t - W_{t-1} = (c_t + sigma_t v_t) + I_{t-1}(v_t - v_{t-1}). Lab identity True on seeds 0 and 1 ({OUT}recompute_r14.out lines 1-2).")
P("L04-example-3.2-values", "2.4-mathematics", "L04.html lines 142-143 (Example 3.2)",
  "Example 3.2 values 5, 0, 5/2 at v = 10000, 10020, 9985 re-derived by exact enumeration (recompute_r14.out 'v=10000 E=5', 'v=10020 E=0', 'v=9985 E=5/2'); formula E = 5 - (1/2)[(v-10010)^+ + (9990-v)^+] checked on 766 grid cells with zero mismatches.")
P("L04-proposition-4.1-remark-4.2-sd", "2.4-mathematics", "L04.html lines 163-170 (Prop 4.1), 173-175 (Remark 4.2)",
  "Mean 0 and variance 25 I^2 re-derived (recompute_r14.out lines 'I 0..I 10'). Remark 4.2 standard deviations 15 cents (I=3) and 50 cents (I=10) match 5|I| (recompute_r14.out 'sd at 3 units 15 sd at 10 units 50').")
P("L04-remark-4.2-inventory-independence", "2.4-mathematics", "L04.html line 175 (Remark 4.2, I=10 case)",
  "At I=10, quote 9990/10010, v=10000, p=1/2: informed does not trade (v inside quote), uninformed sell refused (|11|>10), uninformed buy contributes 10 cents with probability 1/4: expected trade term 5/2 against 5 at I=0. Re-derived (recompute_r14.out 'L04 Remark 4.2 I=10 expected trade term: 5/2').")
P("L04-remark-3.4-inventory-zero", "2.4-mathematics", "L04.html lines 157-158 (Remark 3.4)",
  "(1-p)h at p=1/2 equals h/2 = (2h)/4, a quarter of the quoted spread 2h. The informed cost equals the distance outside the quote (A4). Re-derived.")
P("L04-canon-breaks-tick", "2.2-numbers", "L04.html line 484 (mid at turn t equals 10000 - 10 I_{t-1})",
  f"The induction claim verified on all 20 turns of seeds 0 and 1 by the verifier's own replay: mid_t == 10000 - 10*I_(t-1) True for both ({OUT}recompute_r14.out lines 3-4). Also matches the lab log quote column: turn 3 quote 9980/10000 with I_2=1.")
P("L04-canon-breaks-quote-rule", "2.3-grades", "L04.html lines 481-483 (canon breaks paragraphs)",
  "Statements: results conditional on A1 to A6 (line 481); for each fixed quote from inventory zero the trade term is (1-p)h at a fair value inside the quote (line 483, Prop 3.1); across quotes it rises with h (line 483). Re-derived: Prop 3.1 at v inside the quote gives (1-p)h, increasing in h. The statement 'the model cannot show that a wider quote costs customers' is a statement about the model's scope, consistent with A1.")
P("L04-R2-spread-criterion", "2.4-mathematics", "L04.html lines 599-601 (R2)",
  "For fixed h at v=m: E=(1-p)h by Prop 3.1 (both brackets vanish). Under A1 p does not depend on h, so E=0 has no unique finite solution unless p=1 (then all h). The conclusion that a unique choice needs the arrival distribution to depend on the quote follows from that.")
P("L04-E1-seed1-numbers", "2.2-numbers", "L04.html lines 567-570 (E1)",
  f"Seed-1 line of the lab output (line 458): 16 fills, cash flow 20100, inventory -2, settlement 10020, P&L 60. Verifier replay gives the same ({OUT}recompute_r14.out seed1 line). Mark -2*10020 = -20040; 20100-20040 = 60 correct.")
P("L04-E2-binomial-z", "2.2-numbers", "L04.html lines 573-577 (E2)",
  f"Standard error sqrt(0.25/20) = 0.111803; distance 0.15; z = 1.3416; two-sided 5% critical value 1.959964 (normal quantile). Verifier computation in {OUT}recompute_r14.out ('E2 se 0.111803 z 1.3416 crit 1.959964'). 13/20 informed matches lab line 457.")
P("L04-E3-mid-vs-settlement", "2.2-numbers", "L04.html lines 580-583 (E3); expected block line 445 (turn 20 quote 9980/10000)",
  "Settlement marking: -9950 + 1*9980 = 30 (lab line 451). Mid marking: mid of 9980/10000 is 9990, so -9950 + 1*9990 = 40; difference 10 = inventory x (9990-9980). Correct.")
P("L04-problems-R1-R3-M-P", "2.3-grades", "L04.html lines 515-612 (M1-M3, P1-P3, E1-E3, R1-R3 with solutions)",
  "All worked solutions re-derived: M1 W=10; M2 limit refuses 11 and allows 9; M3 no trade at 10010, buy at 10011 loses one cent; P1 two-turn identity; P2 h/2 and 0, difference h/2; P3 25*16=400; R1 d=(1-p)h/p=20/3 at p=3/5, h=10; R2 as above; R3 |I|<2, largest magnitude 1, variance 25, and 100 fails the strict bound. Three per tier; 12 problems total.")
P("L04-M3-inventory-hypothesis", "2.4-mathematics", "L04.html lines 522-526 (M2, the inventory limit) and 529-533 (M3)",
  "M2: inventory 10, sell to maker makes 11, refused; buy from maker makes 9, fills. Matches A5 and the lab test abs(inv+side)<=10. M3 matches A4 strict inequalities. Re-derived.")
P("L04-quiz-q11-citation", "2.2-numbers", "L04.html quiz item 11 (line 707-709); lab output line 446",
  f"Quiz answer 9 equals 'fills 9 of 20 turns' printed at lab output line 446 ({OUT}stdout_L04_r14.txt).")
P("L04-quiz-answers", "2.4-mathematics", "L04.html lines 634-720 (12 items with explanations)",
  "Each answer re-derived: q1 +10010; q2 10; q3 'No' (strict inequality); q4 0 (5 - 5); q5 5; q6 refused; q7 400; q8 mean zero; q9 20/3 ~ 6.6667 within tolerance 0.001; q10 settlement; q11 9; q12 (1-p)h rises. Tolerances admit the exact values.")
P("L04-key-results-prop-3.1-assumptions", "2.3-grades", "L04.html line 622 (key results row for Prop 3.1)",
  "Row cites 'A1, A2, A4, A5, A6 and H1 to H3 (the quote is fixed, not history-dependent)': consistent with Prop 3.1's H1 to H3 (line 129), which list A1, A2, A4, A5, and H2 which contains A6.")
P("L04-prop-3.1-closed-form", "2.4-mathematics", "L04.html lines 127-139 (Prop 3.1 + proof)",
  "Three arrival cases re-derived: uninformed buy (a-v), uninformed sell (v-b), informed -(v-a)^+ - (b-v)^+; weighted sum gives (1-p)h - p[(v-a)^+ + (b-v)^+]. Exact check on 766 (quote, v) cells at p=1/2 with zero mismatches ({S}recompute_r14.py output 'cells checked: 766 mismatches: 0').")
P("L04-corollary-3.3", "2.3-grades", "L04.html lines 146-153 (Corollary 3.3 + proof)",
  "With p=1/2 and v>=a: E = h/2 - (v-a)/2, zero iff v=a+h. Re-derived; the zero-edge value 10020 = a+h gives 0 (lab output line 468).")
P("L04-misconceptions", "2.3-grades", "L04.html lines 490-505 (four misconceptions)",
  "Each misconception's correction re-derived: spread (1-p)h and zero at v=a+h (10020, lab line 468); P&L 10 cents after buy at 10010; variance 2500 at I=10 (lab line 475); A3 excludes quotes depending on v_t. Four items (at least three required).")
P("L04-key-results-table-other", "2.3-grades", "L04.html lines 620-625 (key results, six rows)",
  "Grades T for proved results, C for row 625 (lab-enumerated nine-value grid), with sources matching the lesson's labelled results. Each key result is proved or computed and graded.")
P("L04-scope-and-banned-phrases", "2.9-prose", "L04.html full text; L05, L06 full text (grep BUILDER_RULES banned list and process words)",
  "No banned phrase (TODO, TBD, lorem, for brevity, details omitted, beyond the scope, left as an exercise, you can add more, it is important to note, studies show, experts agree, it is well known, obviously, clearly, three-dot ellipsis outside code): grep empty. Process words ('build', 'builder', 'round', 'verifier', 'REQUESTS', 'unit report') absent from learner text. Universal words checked: 'always' (Remark 1.2: a fill is always one unit, by A5), 'every' (Prop 3.1, Prop 2.2, Lab checks), 'any' (A3 any rule on public history): each is proved or computed.")
P("L04-structure-hours", "2.9-prose", "L04.html header data-hours=6; section order lines 52-629; quiz 12 items; 3 per problem tier",
  "Section order matches BUILDER_RULES §4.2 (why it matters 119 words, sections 1-4, lab, canon breaks, misconceptions 4, problem set 4 tiers x 3, key results, quiz 12, references). eyebrow '6 study hours' (line 35).")
P("L04-DAG-D-terms", "2.9-DAG", "L04.html lines 158, 482 (adverse selection), 97 (mark-to-market dfn), 38 (linked closure concepts)",
  "D3 'adverse selection' appears as prose only (no link, no dfn): allowed by the architect default. Linked uses (expected-value-game, expectation, market-maker, bid-ask-spread, limit-order-book) are all in the closure and resolve (concepts.html ids present; L03.html#def-expected-value-game exists at L03.html). 'mark-to-market' is a plain dfn with no data-concept (allowed). No D1-D9 term is linked or defined.")
P("L04-A1-project-consistency", "2.6-structure", "L04.html line 72 vs project.html line 404",
  "Project states arrivals 1/4 uninformed buy, 1/4 uninformed sell, 1/2 informed, the same as A1 at p=1/2; project trade rule matches A4 and A5 (|I|<=10 after the fill).")
P("L04-footer-registry-claim", "2.1-citations", "L04.html lines 725-727 (references), 736 (footer)",
  "References state the lesson cites no registry source; <ol data-references> is empty; the footer's 'each key result is proved on the page or computed by Lab 1, and each is graded' matches the key-results table (all rows graded; row 625 computed by Lab 1).")
P("L04-lab-docstring-money-integer", "2.5-labs", "tests/labs/PC3/lab-PC3-L04-1.py lines 1-203 (docstring) and code 209-263",
  "Docstring: quotes, cash flows and marks are integer cents; expectations and variances are Fraction (line 185-186). Code: Turn fields are int; cash_flow = -side*price (int); one_turn_change and fair_move_mark_change use Fraction. Matches the docstring.")

# ---- L05 ----
P("L05-def-3.1-markup", "2.9-prose", "L05.html lines 104-107 (Definition 3.1)",
  "Markup: 'x_j>x_m' is written with a raw '>' in math, which is legal HTML text; '&lt;' is escaped at 'i-k&lt;j' (line 106). Raw '<' count outside tags and code is 0 (scan in {OUT}markup_scan_r14.txt). Definition matches the lab's while-loop rule (strict > for survival, lab line 235).")
P("L05-prop-2.1-2.2-remark", "2.4-mathematics", "L05.html lines 85-98 (Prop 2.1, proof, Remark 2.2)",
  "Count (n-k+1)(k-1) re-derived and equal to naive() comparisons for k=1,2,8,32,200 on seed 5 (recompute_r14.out lines 'k=... naive=... formula=...'). Remark 2.2 identity (n-r)r = n^2/4 - (r-n/2)^2 re-derived; k=n/2+1 maximises (n=200 gives k=101, count 10000).")
P("L05-prop-3.2-correctness", "2.4-mathematics", "L05.html lines 123-133 (Prop 3.2, Steps A, B, C) and pseudocode 113-120",
  "Steps A and B re-read. The verifier's deque run asserts after every step that the deque equals the surviving indices of Definition 3.1 (recompute_r14.py assert in deque_run); 400 random cases with ties (n<=30, values 0..5) found 0 violations of the output or invariant ({OUT}recompute_r14.out 'random stress ... violations 0').")
P("L05-prop-3.3-bound", "2.4-mathematics", "L05.html lines 135-143 (Prop 3.3 + proof)",
  "Appends = n (pushes 200 for n=200 in every run), removals <= n (pops 194-199), comparisons <= 2n: seed 5 counts 199, 263, 354, 382, 387 for k=1,2,8,32,200, all <= 400 (recompute_r14.out); random stress 0 violations.")
P("L05-remark-3.4-k-range", "2.4-mathematics", "L05.html lines 145-148 (Remark 3.4)",
  "Example x=(k,...,1,k+1): step k+1 removes exactly k entries for k=1,2,5,9 (recompute_r14.out 'Remark3.4 k=... removals at step n = k'). Deque size before step i is at most k: re-derived.")
P("L05-example-3.5-trace", "2.4-mathematics", "L05.html lines 150-153 (Example 3.5)",
  "Outputs (4,4,5) and deque states re-derived; verifier run prints 'Example 3.5 outputs [4, 4, 5]' (recompute_r14.out).")
P("L05-problems-M-P", "2.3-grades", "L05.html lines 367-413 (M1-M3, P1-P3)",
  "M1 21; M2 outputs (5,5,1,3) (recompute_r14.out 'M2 outputs [5, 5, 1, 3]'); M3 k=1 outputs equal the input, k=n gives one output (re-derived); P1 n^2/4 at r=n/2 and n=200 gives k=101, count 10000; P2 survival of q re-derived; P3 n-1 for increasing input (recompute_r14.out 'increasing n-1 for all k: True').")
P("L05-E1-E3-numbers", "2.2-numbers", "L05.html lines 417-437 (E1, E3)",
  f"E1: 169*31 = 5239, ratio 5239/382 = 13.7147 -> 13.7 (recompute_r14.out 'E1 ratio 13.7147'). E3: 387 <= 400, pushes 200, pops 194 (lab line 331), split bound 194+200 = 394 >= 387: arithmetic correct.")
P("L05-E2-seed6-numbers", "2.2-numbers", "L05.html lines 424-429 (E2); lab output line 316-317",
  f"Seed-6 sequence (random.Random(6), same generator): outputs equal True, naive 1351, deque 350 comparisons, 200 pushes, 197 pops (recompute_r14.out 'seed6 k=8: naive=1351 deque_cmp=350 pops=197 pushes=200 eq=True'). Matches lab output lines 316-317.")
P("L05-R1-scope-sentence", "2.3-grades", "L05.html lines 442-448 (R1)",
  "The protocol and the statement 'the lesson establishes no timing result' are consistent: the lesson's lab counts operations and times nothing (lab docstring lines 169-170).")
P("L05-R2-R3", "2.4-mathematics", "L05.html lines 449-462 (R2, R3)",
  "R2: maximiser k=101 with count 10000 (recompute_r14.out 'R2 argmax k for n=200: 101 10000'). R3: strictly increasing input removes one back index per step i>=2, total n-1 for every k (recompute_r14.out 'increasing n-1 for all k: True'); the claim 'does not force order nk' follows.")
P("L05-key-results-grades", "2.3-grades", "L05.html lines 472-477 (six rows)",
  "Row 477 is C (seeded lab, window sizes 1-20, with the proof for every sequence cited separately); rows 472-476 are T and match Props 2.1, 3.2, 3.3, Remark 2.2 and P3, each proved on the page.")
P("L05-quiz-answers", "2.4-mathematics", "L05.html lines 487-562 (10 items)",
  "Answers re-derived: q1 21; q2 400; q3 10000; q4 Yes (each index leaves at most once); q5 5; q6 n-1; q7 last-occurrence front (follows from strict survival in Def 3.1 and the lab's while-loop 'xs[back] > x' test at lab line 235); q8 1351; q9 counts are not run times; q10 no outputs.")
P("L05-misconceptions-canon-breaks", "2.3-grades", "L05.html lines 346-358 (misconceptions), 335-341 (canon breaks)",
  "Misconception 1 cites 354 vs bound 400 (lab output line 313, 314) correctly; misconception 2 and 3 match the lab docstring and Definition 3.1/Prop 3.2. Canon breaks name the model limit (operation count is not a run time; amortised bound; comparability).")
P("L05-structure-hours", "2.9-prose", "L05.html header data-hours=6; sections lines 52-580",
  "Section order matches BUILDER_RULES §4.2; 3 misconceptions; problem set 4 tiers x 3; 10 quiz items; eyebrow '6 study hours'. Why-it-matters 94 words (<=120).")
P("L05-markup-raw-less-than", "2.9-prose", "L05.html full text outside pre and script blocks",
  "Verifier markup scan: 0 raw '<' characters in text outside tags (the one escaped '<' is 'i-k&lt;j' in Definition 3.1, line 106).")
P("L05-meta-uses-hash-map-heap", "2.9-DAG", "L05.html line 38 (Uses row), line 157-158 (Remark 3.6)",
  "Uses row links big-O complexity, hash map, binary heap, monotonic deque, unit test; all are closure concepts (CS2, CS1) and resolve in concepts.html. Remark 3.6 heap bound 3*200*floor(log2 200) = 4200 re-derived (recompute_r14.out 'heap bound n=200: 4200').")
P("L05-meta-uses-other", "2.9-DAG", "L05.html lines 38-39 and in-text terms",
  "'Introduces' lists timed coding interview (defined by dfn at line 58, data-concept). No other non-closure concept is linked; 'time budget' and 'deque' defined in lesson text before use (Definition 1.1; Definition 3.1).")
P("L05-why-it-matters-comparisons", "2.9-prose", "L05.html line 52 (why it matters)",
  "The sentence 'a monotonic deque returns the same answers with at most twice the input length in comparisons' is Prop 3.3 (<=2n) plus Prop 3.2. 94 words. Counts described as operation counts, not time.")
P("L05-footer-registry-claim", "2.1-citations", "L05.html lines 567-569 (references), 578 (footer)",
  "No registry source cited; data-references empty; footer matches the key-results table (row 477 computed by Lab 1, rest proved).")
P("L05-DAG-links", "2.9-DAG", "L05.html links at lines 38, 106, 157-158; lesson nav 573-574",
  "Links to concepts.html#monotonic-deque, #hash-map, #binary-heap, #big-o-complexity, #unit-test resolve (ids present in course/concepts.html); internal #def-timed-coding-interview defined at line 58. check_dag PASS.")
P("L05-card-PC3-c092", "2.7-cards", "cards.json PC3-c092 (L05 Remark 3.4 card)",
  "Card asks how many entries step k+1 removes: All k of them. Re-derived (k=1,2,5,9 replay) and the lesson's Remark 3.4 text agrees.")
P("L05-card-PC3-c096-grade", "2.7-cards", "cards.json PC3-c096 (grade T)",
  "Card answer 1351 = 193 x 7 is a Proposition 2.1 consequence (T) and also printed by Lab 1 (output line 312); T is correct for the derived value, with the lab as corroboration.")
P("L05-card-PC3-c097-grade", "2.7-cards", "cards.json PC3-c097 (grade T)",
  "Card answer 5239 = 169 x 31 is a Proposition 2.1 consequence (T); Lab 1 Part 3 also prints it in the naive column for k=32 (output line 330). Grade T is justified.")

# ---- L06 ----
P("L06-prop-1.1-payoff-identity", "2.4-mathematics", "L06.html lines 58-66 (Prop 1.1 + proof)",
  "(s-K)^+ - (K-s)^+ = s-K for all real s, K: both cases re-derived.")
P("L06-remark-1.2-put-call-parity", "2.4-mathematics", "L06.html lines 68-71 (Remark 1.2); linked FC2 put-call parity definition",
  "Price form C - P = S - DK (D from A2) is attributed to the prerequisite module (course/modules/FC/FC2/L05.html, def-put-call-parity 'parity cost' and the parity portfolio). The page does not re-derive it. No bibliographic claim.")
P("L06-definition-1.3-NPV-and-prop-3.1", "2.4-mathematics", "L06.html line 73 (NPV formula); linked CF1 definition (course/modules/CF/CF1/L01.html)",
  "NPV(r) = sum C_t (1+r)^(-t), t=0..n: identical to the linked CF1 definition 'NPV(r) = sum C_t/(1+r)^t' (CF1 L01 def-net-present-value). Prop 3.1 uses the same formula.")
P("L06-prop-2.1-forward", "2.4-mathematics", "L06.html lines 90-99 (Prop 2.1 + proof), 79-88 (A1-A5)",
  "(i) state-free portfolio: cost -S + S = 0, payoff F' - S/D; (ii) A4 and A5 force F' = S/D: both reverse-portfolio arguments re-derived. Hypotheses A1 to A5 are listed before the statement.")
P("L06-remark-2.2-continuous-convention", "2.4-mathematics", "L06.html lines 101-104 (Remark 2.2); linked FC2 L02 cost-of-carry definition (F* = S e^{r tau})",
  "With D = e^{-r tau}, S/D = S e^{r tau}, the linked cost-of-carry price. Linked forward concept is continuously compounded (FC2 L02). The 'rational input' sentence is consistent: e^{-r tau} is not rational in general.")
F("L06-corollary-3.3-grade", "2.3-grades", "L06.html lines 131-133 (Corollary 3.3 statement: 'The sign is fixed when the whole interval [ell,h] lies on one side of u*.') and line 137 (proof: 'If h<u* or ell>u*')",
  f"Graded T. The proof's operative condition is strict (h<u* or ell>u*, line 137). The statement's 'lies on one side of u*' admits the boundary case h=u* (or ell=u*): then NPV(h)=0, so the sign is not fixed on [ell,h] (negative on [ell,h) and zero at h). Counterexample: any single factor range [ell,h] with h=u* (NPV(u)<0 for ell<=u<h, NPV(h)=0); the verifier's arithmetic: NPV(u)=mA(u-u*) (Prop 3.1). The statement omits the strictness the proof needs (VERIFIER class 6). Also card PC3-c112 back text repeats the claim.",
  "Change the statement (L06.html line 132) to 'The sign is fixed when the whole interval [ell,h] lies strictly on one side of u*, that is h < u* or ell > u*.' and make the same change to the back of card PC3-c112 ('A range that lies strictly on one side of the break-even, with neither end at it, does fix it'). The proof on line 137 already states the strict condition.")
P("L06-prop-3.2-fermi-bounds", "2.4-mathematics", "L06.html lines 120-128 (Prop 3.2 + induction proof)",
  "Induction re-derived: P_{k-1} >= L_{k-1} > 0 and x_k >= ell_k > 0 give P_k >= L_k ell_k; attainment by choosing ends. Hypotheses 0 < ell_j <= h_j listed.")
P("L06-example-4.2-numbers", "2.2-numbers", "L06.html lines 147-150 (Example 4.2)",
  f"Range [200,1600] (2000x1x0.1 and 4000x2x0.2); A = 3310/1331 (1/1.1+1/1.21+1/1.331 = 3.31/1.331); u* = 399300/331 = 1206.34 (recompute_r14.out 'Example 4.2 break-even 399300/331 1206.344410876133'); NPV negative at 200 and positive at 1600 (lab output lines 298-299 and recompute).")
P("L06-remark-4.3-sensitivity", "2.2-numbers", "L06.html lines 152-155 (Remark 4.3) after the fix from the round-13 'seven significant digits' wording",
  f"The round-13 defect is fixed: the text now says the factors are 'rounded to seven decimal places': A(8%)=2.5770970 (exact 2.5770969872, 7 dp = 2.5770970), A(10%)=2.4868520 (exact 2.4868519910), A(12%)=2.4018313 (exact 2.4018312682). Verifier: 3000/A exact = 1164.100542, 1206.344411, 1249.046942; with the 7-dp A, 1164.100536, 1206.344407, 1249.046925: all four-decimal displays 1164.1005, 1206.3444, 1249.0469 hold ({OUT}recompute_r14.out lines 'r=2/25 ...', 'r=1/10 ...', 'r=3/25 ...'). Differences 42.2439 -> 42.24 and 42.7025 -> 42.70 (verifier: -42.24386874, +42.70253080). NPV signs at 200/1600 at all three rates match lab lines 302-304.")
P("L06-E2-first-negative", "2.2-numbers", "L06.html lines 401-405 (E2)",
  f"Grid 200..1600 step 100 at 10%: positive NPV at 1300, 1400, 1500, 1600 (four points) (recompute_r14.out 'E2 grid points > breakeven [1300, 1400, 1500, 1600]'). NPV(1200) = -105000000/1331 = -78888.054 (recompute_r14.out 'NPV 1200 exact'); NPV(1300) = 1550000000/1331 = 1164537.94. Both as stated.")
P("L06-E1-12pct", "2.2-numbers", "L06.html lines 393-398 (E1) after the round-13 fix",
  f"Defect from round 13 fixed: 'rounded to seven decimal places' now used. A(12%) = 1/1.12+1/1.2544+1/1.404928 = 2.40183126822 (verifier: '1/1.12+1/1.2544+1/1.404928 = 2.4018312682215743'); 7 dp = 2.4018313 (8th digit 6 rounds up). 3000/A = 1249.046942 -> 1249.0469 and 1249.05 at two decimals (recompute_r14.out). Matches lab line 304 display 1249.05.")
P("L06-E3-42.71", "2.2-numbers", "L06.html lines 407-413 (E3) after the round-13 fix",
  f"Defect from round 13 fixed: factors described as 'rounded to seven decimal places' (line 411). Width 1249.0469-1164.1005 = 84.9464 -> 84.95; average 84.9464/4 = 21.2366 -> 21.24 (recompute_r14.out 'E3 avg per point 21.236599884883976'); 8-10: 42.2439 -> 42.24; 10-12: 42.7025 -> 42.70; displayed subtraction 1249.05-1206.34 = 42.71 correctly labelled as not the answer.")
P("L06-E3-rest-and-quiz-q9", "2.2-numbers", "L06.html lines 411 (E3), quiz item 9 lines 519-523",
  "Quiz item 9 answer 21.24 with tolerance 0.01 matches 21.2366 (|diff| 0.0034). Explanation '84.9464/4=21.2366' correct.")
P("L06-M1-M3-numbers", "2.2-numbers", "L06.html lines 345-361 (M1-M3)",
  "M1 4900/0.98 = 5000; payoff 50 (verified). M2 NPV = 500/121 = 4.1322 -> 4.13 (recompute_r14.out 'M2 NPV 500/121 4.132231404958677'). M3 u* = 33275/331 = 100.5287 -> 100.53 (recompute_r14.out 'M3 break-even 33275/331 100.52870090634441').")
P("L06-P1-P3-proofs", "2.4-mathematics", "L06.html lines 370-388 (P1-P3)",
  "P1 reverse portfolio payoff S/D - F' with zero cost (A2, A3, A5 used in the right places). P2 affine with positive slope, unique zero, sign on each side. P3 product bounds 200 and 1600 with attainment ends (recompute_r14.out 'P3 bounds 200 1600').")
P("L06-R1-R3", "2.3-grades", "L06.html lines 418-438 (R1-R3)",
  "R1: ratios 4000/2000 = 2, 2/1 = 2, (1/5)/(1/10) = 2, so each log-width is ln 2 (recompute_r14.out 'R1 log width ratios 2.0 2.0 2.0'); tie is correct. R3: m* = 15000000*1331/(1600*3310) = 3769.83 cents, ratio 0.75397 -> 0.7540, fall 24.60% -> 24.6 (recompute_r14.out 'R3 margin 3769.8262839879153 ratio 0.7539652567975831 fall % 24.60347432024169'). R2 closed form re-derived.")
P("L06-quiz-answers", "2.4-mathematics", "L06.html lines 463-533 (10 items)",
  "q1 5000; q2 F'-S/D; q3 S/D; q4 4.13 (500/121 = 4.1322, tolerance 0.005); q5 1206.34 (1206.3444, tolerance 0.005: |diff| 0.0044); q6 range straddles -> nothing; q7 4 grid points; q8 rises strictly; q9 21.24; q10 balance-sheet cash (AC1 L08 statement-articulation definition says the cash-flow statement ends at balance-sheet cash).")
P("L06-canon-breaks-and-misconceptions", "2.3-grades", "L06.html lines 310-312 (canon breaks), 318-333 (misconceptions)",
  "Canon breaks name model limits (margin fixed, rate fixed, tax, salvage, option to stop; Fermi range is not evidence). Misconceptions: forward price is S/D (no expectation); break-even moves with rate (1164.10 to 1249.05, 21.24 per point); bounds straddle (Corollary 3.3); one rate (sign same, break-even moves). Range 'factor of 8' (1600/200) re-derived.")
P("L06-articulation-claim-linked", "2.1-citations", "L06.html line 75 and quiz item 10 (line 525-531) vs course/modules/AC/AC1/L08.html statement-articulation definition",
  "AC1 L08 def-statement-articulation: 'the cash-flow statement ends at the balance-sheet cash' (verified by grep). The claim is the linked prerequisite's statement and is attributed to it.")
P("L06-footer-registry-claim", "2.1-citations", "L06.html lines 538-540 (references), 549 (footer)",
  "No registry source; data-references empty; footer matches key results (rows T; row 453 computed/derived with the lab).")
P("L06-structure-hours", "2.9-prose", "L06.html header data-hours=6; sections lines 52-546",
  "Section order matches BUILDER_RULES §4.2; 4 misconceptions; problem set 4 tiers x 3; 10 quiz items; eyebrow 6 study hours; next link to project.html present (line 545).")
P("L06-DAG-and-cross-links", "2.9-DAG", "L06.html links lines 38-39, 75, 545; L01.html#def-fermi-estimation (anchor exists in L01.html)",
  "Closure concepts linked (forward-contract, cost-of-carry-forward-price, put-call-parity, net-present-value, statement-articulation, fermi-estimation) and resolved; 'case-interview' defined with dfn at line 144. Remark 1.2 and Section 2 refer to linked concepts without new unlinked closure uses. check_dag PASS.")
P("L06-why-it-matters-scope", "2.9-prose", "L06.html line 52 (why it matters)",
  "86 words (<=120). Says the lesson proves the forward price and the payoff identity (Props 2.1, 1.1), derives the break-even (Prop 3.1), and reports sensitivity (Remark 4.3): each is on the page.")
P("L06-lab-docstring-money-integer", "2.5-labs", "tests/labs/PC3/lab-PC3-L06-1.py docstring lines 1-177 and code 186-283",
  "Docstring: prices and outlay are integer cents; every value is Fraction; display is the only place rounding happens (half_up, applied once to the exact value). Code matches: SPOT_CENTS, OUTLAY_CENTS int; annuity and npv are Fraction; half_up is called only in print statements.")
P("L06-card-PC3-c148-grade", "2.7-cards", "cards.json PC3-c148 (grade T)",
  "Card answer 'About 1249.05 units per year' is the derived break-even at 12% (3000/A with A = 2.4018312682, recompute_r14.out 'r=3/25 ... 3000/A=1249.046942'); T is justified by Prop 3.1 with the closed-form A; the lab print (1249.05) is corroboration.")
P("L06-card-PC3-c151", "2.7-cards", "cards.json PC3-c151 (grade T)",
  "Card computes (1249.0469 - 1164.1005)/4 = 21.2366 -> 21.24: arithmetic correct; the unrounded values are derived by Prop 3.1 (T). Consistent with L06 E3.")

# ---- cards (2.7) ----
F("card-full-scan-L06", "2.7-cards", "cards.json PC3-c112 (L06 Corollary 3.3 card) inside the full scan of L06 cards (37 L06 cards read in full: PC3-c102..c127 except c118, c147..c151, c165..c167, c178..c179, c183..c184)",
  "All L06 card fronts and backs were read against the L06 text. One card asserts the corollary claim that fails at the boundary: PC3-c112 back says 'A range that lies wholly on one side of the break-even does fix it' (cards.json line ~954-960). Same defect as row L06-corollary-3.3-grade. Other 36 L06 cards agree with the lesson text and carry the proposition hypotheses where they make a proposition claim.",
  "Fix card PC3-c112 back text as in row card-PC3-c112-corollary-boundary (strict one-side condition, h < u* or ell > u*).")
F("card-PC3-c112-corollary-boundary", "2.7-cards", "cards.json line ~954-960, PC3-c112 back text",
  "Card back: 'A range that lies wholly on one side of the break-even does fix it, because the NPV is strictly increasing in u (Proposition 3.1).' Wrong at the boundary: a range whose upper end is exactly the break-even contains a zero NPV at that end and is not fixed in sign. Same statement as L06.html line 132.",
  "Change to 'A range that lies strictly on one side of the break-even, with neither end at it, does fix it, because the NPV is strictly increasing in u (Proposition 3.1).' Also reword the front to match the lesson's Corollary 3.3 hypothesis if needed.")
P("card-full-scan-L04", "2.7-cards", "cards.json PC3-c062..c083, c137..c141, c153..c154, c162..c164, c168, c171, c174..c175, c176, c185..c186 (all 39 L04 cards read in full; {OUT}cards_L456_r14.txt)",
  "Every L04 card read against L04.html: Def 1.1, A1, A5, Def 2.1, Prop 2.2, Remark 2.4, Prop 2.3, Prop 3.1 (with H1-H3 as on the page), Example 3.2, Cor 3.3, Remark 3.4, Prop 4.1, Remark 4.2, Lab 1 cards (c077, c137-c141, c075), misconceptions, research R1 and R3. New cards c185 and c186 (cash change, inventory change) agree with Section 2. Card c081's basis cites H3 of Prop 3.1 while the card's content depends on H2 (the quote is fixed): a basis-field imprecision, not a learner-facing error. No card contradicts the lesson.")
P("card-full-scan-L05", "2.7-cards", "cards.json PC3-c084..c101, c142..c146, c169..c170, c177, c180..c182 (all 29 L05 cards read in full)",
  "Every L05 card read against L05.html and the lab: Def 1.1 (six steps), Remark 1.2, Def 1.3, Prop 2.1, Remark 2.2, Def 3.1, Prop 3.2, Prop 3.3 (cards 091, 092, 181, 182 match the proof), Remark 3.4, Example 3.5, M2, P3, E1 counts (c096, c097), misconceptions and Lab 1 counts (c142-c146). New cards c180-c182 agree with the Prop 3.2/3.3 text. All numbers (354, 382, 387, 1351, 5239, 199, 200, 5, 4200) are in the lesson or its lab output.")
P("card-duplicate-scan", "2.7-cards", "cards.json all 105 L04-L06 cards (full scan for identical or near-identical fronts)",
  "No two L04-L06 cards are identical. Near-overlaps judged as distinct prompts: PC3-c112 (corollary statement) and PC3-c178 (misconception 'bounds decide the case') test the same fact with different prompts and answers; PC3-c121 and PC3-c123 test different misconceptions (assumptions as a footnote; one rate settles the case). Both are accepted as distinct retrieval prompts. No duplicate ids (verifier scan: 181 ids, 0 duplicates).")
P("card-key-results-agreement", "2.7-cards", "cards.json L04-L06 cards vs key-results tables L04.html 620-625, L05.html 472-477, L06.html 448-453",
  "Every card whose content states a key result agrees with the table row (for example PC3-c066/c068 with Prop 2.2/2.3; PC3-c110 with key row 451; PC3-c087 with row 472). No card contradicts a key-results row.")
P("card-number-in-lesson", "2.7-cards", "cards.json numbers vs lesson text and lab output",
  "Every number on a card appears in its lesson or in the lab output printed on the page: e.g. -12513148 (c117, lab line 298), 4894816 (c150, lab line 299), 387 and 382 (c144, c145, Part 3 lines 330-331), 1164.10/1206.34/1249.05 (c121, c148, lab lines 302-304), 21.24 (c151, E3), 4200 (c170, Remark 3.6), 1200 (c124, c179, E2), 3769.8 and 0.7540 (c127, R3). None is absent.")
P("card-cite-empty", "2.7-cards", "cards.json L04-L06 cards: 'cite' field",
  "All 105 L04-L06 cards have cite = [] (verifier scan). No registry key is cited, consistent with the unit's rule that no reference is admitted in this batch.")

# ---- delta (round 14 only) ----
P("delta-r14-hunks-L04-L06-cards", "2.9-prose", "git diff e919577..8e5751c for L04.html (lines 65, 72, 83), L06.html (lines 154, 397, 411), cards.json (c090, c091, c110, c123, c124, c174, c175, new c180-c186), project.html line 404 (outside slice, read for the cross-reference)",
  "Every hunk read. L04 hunks: A5 condition added (line 65), 'Project · Market-making game' wording (lines 72, 83): correct and consistent with project.html title. L06 hunks: 'rounded to seven decimal places' (lines 154, 397, 411): numerically correct (see L06 rows); the Corollary 3.3 text (line 132) is unchanged and remains the defect above. cards: c090/c091/c110/c123/c124/c174/c175 agree with the current lesson text; c180-c186 are new and checked in the full card scans.")
P("delta-r14-twins-unchanged", "2.5-labs", "tests/labs/PC3/lab-PC3-L04-1.py, lab-PC3-L05-1.py, lab-PC3-L06-1.py (git diff e919577..8e5751c empty for these files)",
  "No twin changed since the round-13 pin, so the twin rows were re-run rather than carried: all PASS on this pin.")


FRAGMENT = {
    "unit": "PC3",
    "slice": "PC3-b",
    "round": 14,
    "verifier": "Claude Haiku 5.5, independent verifier for PC3-b round 14 (did not build PC3)",
    "pin": "8e5751c903f0246115eba746afdf5d71f612bb37",
    "base": "e919577b45b431ce68e1e6533b00b8a301277937 (round-13 pin). Delta e919577..8e5751c in this slice: L04.html (lines 65, 72, 83), L06.html (lines 154, 397, 411), cards.json (c090, c091, c110, c123, c124, c174, c175; new c180-c186). L05.html and all three twins are byte-identical to the round-13 pin. Every row was re-derived this round; no PASS row is carried.",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE14-PC3-b",
    "scratch": "/Users/billyribeiro/.fanout/wt/verifyE14-PC3-b/ledgers/PC3/scripts/PC3-b-r14/out",
    "verified_at": __import__("datetime").datetime.now(__import__("datetime").timezone.utc).replace(microsecond=0).isoformat(),
    "verdict": "FAIL" if any(r["status"] != "PASS" for r in rows) else "PASS",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Slice b: L04.html, L05.html, L06.html, lab twins lab-PC3-L04-1.py, lab-PC3-L05-1.py, lab-PC3-L06-1.py, and the 105 PC3 cards for L04-L06 (39 + 29 + 37), all read in full line by line.",
        "Round-13 FAIL rows (L06-remark-4.3-sensitivity, L06-E1-12pct, L06-E3-42.71: factors described as 'seven significant digits' for eight-digit values) are fixed on this pin: the text now says 'rounded to seven decimal places'. Re-derived from scratch with exact Fractions (ledgers/PC3/scripts/PC3-b-r14/recompute_r14.py): PASS.",
        "New FAIL on this pin: Corollary 3.3 (L06.html lines 131-133, 137) states the sign is fixed when [ell,h] lies on one side of u*; the proof needs the strict condition h < u* or ell > u*. Card PC3-c112 repeats the claim. The defect is wording at the boundary only; the closed form and the strict-inequality proof are correct.",
        "Judgement (not a row): card PC3-c081 basis cites H3 of Prop 3.1, while its content depends on H2 (fixed quote). Basis field only; not learner-facing; PASS.",
        "Judgement (not a row): PC3-c112 and PC3-c178 test the same fact (bounds straddling the break-even do not fix the sign) with different prompts; accepted as distinct retrieval prompts. The Corollary fix above changes both.",
        "Judgement (not a row): 'adverse selection' appears in L04 lines 158 and 482 (two uses) and card PC3-c176. Plan D3 says 'used once' in prose; the architect default permits prose use with no link or dfn, so accepted.",
        "Judgement (not a row): L04 Remark 4.2 and key-results rows are consistent with Prop 4.1 and Prop 2.3; L04 Problem R2 'would need the arrival distribution to depend on the quote' is a necessary-condition statement that follows under A1; accepted.",
        "Judgement (not a row): L06 Remark 4.3 calls the 4-dp break-evens 'unrounded values' while they are displayed to four decimals. Their exact values (3000/A with the exact annuity factor) display to the same four decimals, so the display claim holds; accepted.",
        "Command rows run on the pin: run_labs, check_pages, check_dag, check_projects, page_smoke (alone, L04 L05 L06), ruff check/format, mypy --no-incremental, pytest (lab tooling), verify_refs --offline, fetch_data --check, render_curriculum + git diff --exit-code (no change), build_site --check, run_graders --seeds 0-49. Outputs under ledgers/PC3/scripts/PC3-b-r14/out/.",
        "Mutation testing: not applicable to this slice (architect ruling: lab twins are demonstrations; the grader belongs to another slice). mutants is empty; no mutant was written or killed.",
        "Not checked: the Pyodide browser runtime beyond page_smoke's own run; the linked prerequisite modules beyond the definitions cited above; any registry record (no key is cited in this slice); the project grader, the project page and the hub (other slices); tests/test_docs_figures.py (not in the slice's gates).",
    ],
    "summary": {},
}
FRAGMENT["summary"] = {
    "rows": len(rows),
    "pass": sum(1 for r in rows if r["status"] == "PASS"),
    "fail": sum(1 for r in rows if r["status"] == "FAIL"),
    "unverifiable": sum(1 for r in rows if r["status"] == "UNVERIFIABLE"),
}
out = ROOT / "ledgers/PC3/PC3-b.json"
out.write_text(json.dumps(FRAGMENT, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out, FRAGMENT["summary"], FRAGMENT["verdict"])
