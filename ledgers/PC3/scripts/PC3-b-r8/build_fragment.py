"""Writes the round-8 PC3-b fragment (verifier output). Run: .venv/bin/python -I ledgers/PC3/scripts/PC3-b-r8/build_fragment.py"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
S = "ledgers/PC3/scripts/PC3-b-r8/out/"
SC = "ledgers/PC3/scripts/PC3-b-r8/"

rows: list[dict[str, str]] = []


def row(rid: str, check: str, location: str, status: str, evidence: str, fix: str = "") -> None:
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    rows.append(r)


# ---- gates (run by this verifier on pin 0dee921)
row("gate-run-labs-unit", "2.5-labs", "tools/run_labs.py --unit PC3", "PASS",
    S + "run_labs.out: 'run_labs PC3: PASS (9/9)', rc 0.")
row("gate-check-pages", "2.9-prose", "tools/check_pages.py --unit PC3", "PASS",
    S + "check_pages.out: 'check_pages PC3: PASS', rc 0.")
row("gate-check-dag", "2.9-DAG", "tools/check_dag.py --unit PC3", "PASS",
    S + "check_dag.out: 'check_dag PC3: PASS', rc 0.")
row("gate-check-projects", "2.6-structure", "tools/check_projects.py --unit PC3", "PASS",
    S + "check_projects.out: 'check_projects PC3: PASS', rc 0 (unit-wide; the project is not in slice b).")
row("gate-page-smoke-slice", "2.9-prose", "tools/page_smoke.py --unit PC3 --pages L04 L05 L06", "PASS",
    S + "page_smoke_L04_L06.out: 'page_smoke modules/PC/PC3/L04.html: PASS', L05.html PASS, L06.html PASS, "
    "'page_smoke PC3: PASS', rc 0 (Chromium, both themes, 360 px, labs in Pyodide; lab timings 0.0 s).")
row("gate-ruff-mypy-twins", "2.5-labs",
    "ruff check, ruff format --check on the three twins; mypy --no-incremental (full project)", "PASS",
    S + "ruff_check.out 'All checks passed!' rc 0; ruff_format.out '3 files already formatted' rc 0; "
    "mypy_twins.out 'Success: no issues found in 3 source files'; mypy_full.out 'Success: no issues found in 385 source files' rc 0.")
row("gate-pytest-lab-tooling", "2.5-labs",
    "pytest -q tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py", "PASS",
    S + "pytest_labs.out: progress dots only, no F or E, rc 0.")
row("gate-verify-refs-offline", "2.1-citations", "tools/verify_refs.py --offline (whole registry)", "PASS",
    S + "verify_refs_offline.out: 'offline integrity: 560 entries, 0 problems', rc 0. Slice b cites no registry key: "
    "grep -c 'data-cite\\|data-locator' on L04.html, L05.html, L06.html gives 0 for each.")
row("notation-registry-L04-L06", "2.4-notation", "course/modules/PC/PC3/L04.html, L05.html, L06.html (math)", "PASS",
    "notation/notation.json lists T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q}; none occurs in the three "
    "pages (grep of LaTeX commands inside math segments). Registered macros used: \\E (L04, 12 uses), \\Var (L04, 3). "
    "Local letters (N, t, p, L, v, a, b, q, I, C, W, sigma, S, m, h, D, A, u, r, n, k, x) are defined on the page where first used.")
row("twin-run-alone-L04-L06", "2.5-labs", "tests/labs/PC3/lab-PC3-L04-1.py, lab-PC3-L05-1.py, lab-PC3-L06-1.py", "PASS",
    S + "embed_compare.out: each twin run alone as python -I -W error from a scratch directory: rc 0, stderr 0 bytes (L04, L05, L06). "
    "Script: " + SC + "embed_compare.py.")
row("twin-page-code-equals-twin", "2.5-labs", "course/modules/PC/PC3/L04.html, L05.html, L06.html vs the three twins", "PASS",
    S + "embed_compare.out: 'page code == twin: True' for L04, L05, L06 (after html.unescape of data-run blocks).")
row("twin-expected-equals-stdout", "2.5-labs", "expected blocks L04 (50 lines), L05 (23), L06 (21)", "PASS",
    S + "embed_compare.out: 'expected == twin stdout: True' for all three.")

# ---- labs: hypothesis and interpretation
row("lab-L04-1-hypothesis-interpretation", "2.5-labs",
    "course/modules/PC/PC3/L04.html line 180 (hypothesis), line 460 (interpretation)", "FAIL",
    "Hypothesis numbers match " + S + "L04.stdout (identity True, cash flow -9950, P&L 30, nine values, variance 25 I^2). "
    "The interpretation sentence 'the proof covers every fair value for a fixed quote' omits the inventory-zero hypothesis "
    "H1 of Proposition 3.1 (L04.html line 129, which this round added); the same page's Part 2 text and Section 5 state "
    "'from inventory zero', so the interpretation overreaches the amended statement.",
    "In L04.html line 460, change 'the proof covers every fair value for a fixed quote' to 'the proof covers every fair value "
    "for a fixed quote, from inventory zero (Proposition 3.1, H1)'. Then run tools/embed_labs.py only if the twin changes "
    "(it does not); re-run check_pages.")
row("lab-L05-1-hypothesis-interpretation", "2.5-labs",
    "course/modules/PC/PC3/L05.html line 163 (hypothesis), line 321 (interpretation)", "PASS",
    S + "L05.stdout: 1351 = (n-k+1)(k-1), deque comparisons 354, pushes 200, pops 199, five edge checks True, Part 3 rows. "
    "Interpretation numbers (1351, 354, bound 400, 'not run times') match the output.")
row("lab-L06-1-hypothesis-interpretation", "2.5-labs",
    "course/modules/PC/PC3/L06.html line 159 (hypothesis), line 304 (interpretation)", "PASS",
    S + "L06.stdout: forward F = 10000, payoff 0 and 100 at five spot values, annuity 3310/1331, break-even 399300/331 = 1206.34, "
    "NPV -12513148 and 4894816, rate rows 1164.10 / 1206.34 / 1249.05. Interpretation's 42.24 and 42.71 differences match the printed values "
    "(l06_independent.out: 42.2439 and 42.7025 unrounded).")

# ---- L04 mathematics and prose
row("L04-definitions-A1-A6-notation", "2.4-notation", "course/modules/PC/PC3/L04.html lines 56-89", "PASS",
    "Definition 1.1 steps and A1 to A6 (lines 62-77) read in full. Symbols N, t, p, L defined at line 56; "
    "probabilities 1/4, 1/4, 1/2 agree with project.html line 404 (1/4, 1/4, 1/2). Locator error in A1 and Example 1.3 is row "
    "L04-lab-section-locator.")
row("L04-lab-section-locator", "2.9-prose", "course/modules/PC/PC3/L04.html line 72 (A1) and line 87 (Example 1.3 title)", "FAIL",
    "Both say the lab is in Section 3: 'Lab 1 (Section 3)' and 'the quoting rule of Lab 1, Section 3'. The lab is inside Section 4 "
    "(h2 id=s4 'Inventory risk' at line 161; the lab section at line 178; h2 id=s5 at line 464). Section 3 has no lab. "
    "Both strings were introduced by this round's delta (06994db1..0dee921).",
    "Change 'Lab 1 (Section 3)' to 'Lab 1 (Section 4)' at line 72 and 'Lab 1, Section 3' to 'Lab 1, Section 4' at line 87; "
    "re-run tools/check_pages.py --unit PC3.")
row("L04-prop-2.2-2.3-identity", "2.4-mathematics", "course/modules/PC/PC3/L04.html lines 100-118, P1 (line ~524)", "PASS",
    "Re-derived by hand: C_t and I_t induction; W_N identity; turn decomposition W_t - W_{t-1} = (c_t + sigma_t v_t) + I_{t-1}(v_t - v_{t-1}). "
    "Numerical: " + SC + "l04_independent.py, out/l04_independent.out 'identity and mid=10000-10I over seeds 0..199: failing seeds = []'.")
row("L04-example-3.2-values", "2.2-numbers", "course/modules/PC/PC3/L04.html line 143", "PASS",
    "Prop 3.1 at a=10010, b=9990, p=1/2: v=10000 -> 5, v=10020 -> 0, v=9985 -> 5/2 (l04_independent.out 'Example 3.2 ... 5 0 5/2').")
row("L04-proposition-4.1-remark-4.2-sd", "2.2-numbers", "course/modules/PC/PC3/L04.html lines 163-176", "PASS",
    "Prop 4.1 proof re-derived: mean 0, variance 25 I^2. Remark 4.2: SD 5|I| gives 15 cents at 3 units and 50 at 10 units; "
    "Lab 1 Part 3 prints variance 2500 at inventory 10 (L04.stdout).")
row("L04-remark-4.2-inventory-independence", "2.4-mathematics", "course/modules/PC/PC3/L04.html line 175", "PASS",
    "At I=10, v=10000, quote 9990/10010, p=1/2: informed does not trade (v inside), uninformed sell refused (11 > L), uninformed buy "
    "contributes 10 cents with probability 1/4, so 5/2 (l04_independent.out 'Remark 4.2 expected trade term ... 5/2'). "
    "'Same distribution while |I| <= L-1' follows from A5 (no refusal) and Prop 3.1's proof.")
row("L04-remark-3.4-inventory-zero", "2.4-mathematics", "course/modules/PC/PC3/L04.html lines 157-158", "PASS",
    "(1-p)h at p=1/2 equals h/2 = a quarter of the spread 2h (arithmetic). Informed cost stated under A4, A5.")
row("L04-canon-breaks-tick", "2.9-prose", "course/modules/PC/PC3/L04.html lines 462-464 (Section 5, paragraphs 1-2)", "PASS",
    "Model limits named (queue, learning, A5 fill), no number asserted beyond 5 cents and the limit-order-book link (FC1, in closure).")
row("L04-canon-breaks-quote-rule", "2.4-mathematics", "course/modules/PC/PC3/L04.html lines 464-468 (Section 5, paragraphs 3-4)", "PASS",
    "'From inventory zero' now stated. Mid induction 'mid_t = 10000 - 10 I_{t-1}' checked by l04_independent.py on seeds 0..199 "
    "(mid_eq_10000_minus_10I True for all). Lab-line claims about the rule match Example 1.3.")
row("L04-R2-spread-criterion", "2.4-mathematics", "course/modules/PC/PC3/L04.html lines 582-584 (R2)", "PASS",
    "At v=m both brackets vanish, E=(1-p)h from inventory zero (Prop 3.1). p<1: E>0 for every h, so no zero; p=1: E=0 for every h. "
    "Conclusion correct.")
row("L04-E1-seed1-numbers", "2.2-numbers", "course/modules/PC/PC3/L04.html lines 549-553 (Problem E1)", "FAIL",
    "The solution states 16 fills, cash flow 20100, final inventory -2, settlement 10020, mark -20040, P&L 60 for seed 1. "
    "My independent run (l04_independent.out 'E1 seed1 fills, cash_flow, inv_end, settle, pnl: 16 20100 -2 10020 60') agrees, "
    "so the values are correct. But Lab 1 is hard-wired to SEED = 0 (tests/labs/PC3/lab-PC3-L04-1.py line 35, play(SEED) at line 142) "
    "and prints only the seed-0 path; no lab on the page produces these numbers and the solution does not derive them. "
    "Under VERIFIER 2.2(a) and BUILDER 1.2 they are unsourced.",
    "Have Lab 1 Part 1 also play seed 1 and print its fills, cash flow, inventory, settlement and P&L (for example, loop over (0, 1) "
    "in part_one), then run tools/embed_labs.py page --refresh lab-PC3-L04-1 and quote the printed values in E1. "
    "Alternatively delete the seed-1 numbers from E1 and keep only the instruction to run the lab.")
row("L04-E2-binomial-z", "2.2-numbers", "course/modules/PC/PC3/L04.html line 559 (Problem E2)", "PASS",
    "13 informed arrivals in the Lab 1 seed-0 table (L04.html expected block, lines 410-430, arrival column; l04_independent.out 'informed_count': 13). "
    "SE sqrt(0.25/20) = 0.111803; z = 1.341641 (l04_independent.out). 1.34 < 1.96.")
row("L04-E3-mid-vs-settlement", "2.2-numbers", "course/modules/PC/PC3/L04.html lines 564-566 (Problem E3)", "PASS",
    "Turn-20 quote 9980/10000 (table row 20) gives mid 9990. P&L -9950 + 9980 = 30 (printed), -9950 + 9990 = 40, difference 10 = 1 x (9990 - 9980).")
row("L04-problems-R1-R3-M-P", "2.4-mathematics", "course/modules/PC/PC3/L04.html lines 498-595 (M1-M3, P1-P3, R1-R3)", "PASS",
    "M1 (5000 cents, P&L 10), M2 (I=10 refuses sell), M3 (v=10010 no trade, v=10011 buys at ask, loss 1); "
    "P2 (h/2 and 0); P3 (25 I^2 = 400 at I=-4); R1 (d = (1-p)h/p = 20/3, l04_independent.out 'R1 d ... 20/3'); "
    "R2 (see row); R3 (25 I^2 < 100 gives |I| <= 1: l04_independent.out 'R3 ... [-1, 0, 1]').")
row("L04-quiz-q11-citation", "2.9-prose", "course/modules/PC/PC3/L04.html lines 690-692 (quiz item 11)", "PASS",
    "'fills 9 of 20 turns' (L04.stdout) matches the seed-0 table (nine filled rows counted).")
row("L04-quiz-answers", "2.9-prose", "course/modules/PC/PC3/L04.html quiz items 1-12 (lines 620-705)", "PASS",
    "Answers re-derived: +10010 cash; 10 P&L; strict-inequality trade rule; 0 at v=a+h; 5 at mid-inside; refused at 11; 400; "
    "mean 0; d=20/3; settlement v_N; 9 fills; h rises as (1-p)h. Items 4, 5 and 12 now carry 'inventory zero'.")
row("L04-key-results-prop-3.1-assumptions", "2.9-prose", "course/modules/PC/PC3/L04.html line 605 (key results row 3)", "PASS",
    "Row 3 now states H1 (I_{t-1}=0) in the conditional expectation, matching Proposition 3.1 line 129.")
row("L04-prop-3.1-closed-form", "2.4-mathematics", "course/modules/PC/PC3/L04.html lines 127-139", "PASS",
    "Hypotheses H1 (I_{t-1}=0, positive probability), H2 (fixed quote, a-b=2h, q>=1, L>=1), H3 (A1, A2, A4); proof steps (i)-(iii) re-derived by hand. "
    "Numerical: l04_independent.out 'Prop 3.1 closed form equals one-turn enumeration, general p, cases: 520520 all equal: True'; "
    "DP over the full game with a fixed quote, conditioning on I_{t-1}=0 and v_t=v for t=1..20: 'cases checked=230, max |difference| = 0'.")
row("L04-corollary-3.3", "2.4-mathematics", "course/modules/PC/PC3/L04.html lines 146-154", "PASS",
    "With p=1/2, v>=a: E = h/2 - (v-a)/2, zero iff v=a+h. l04_independent.out 'Corollary 3.3 zero iff v=a+h for h=1..30 ... True'.")
row("L04-misconceptions", "2.9-prose", "course/modules/PC/PC3/L04.html lines 471-487", "PASS",
    "Four misconceptions with evidence: quarter-spread arithmetic; M1 10 cents; 2500 cents^2 at inventory 10 (Lab 1 Part 3); "
    "A3 exclusion. All numbers agree with the lab output and proofs.")
row("L04-key-results-table-other", "2.9-prose", "course/modules/PC/PC3/L04.html lines 603-608 (rows 1, 2, 5, 6)", "PASS",
    "Row 1 (W_N identity) T, Prop 2.2; row 2 T, Prop 2.3; row 5 T, Prop 4.1; row 6 C, Lab 1 Part 2 nine values 9980 to 10020 (L04.stdout).")
row("L04-scope-and-banned-phrases", "2.9-prose", "course/modules/PC/PC3/L04.html (whole file)", "PASS",
    "grep for BANNED list (TODO, TBD, lorem, for brevity, details omitted, beyond the scope, left as an exercise, you can add more, "
    "it is important to note, studies show, experts agree, it is well known, obviously, clearly) and process words "
    "(build, builder, round, verifier, REQUESTS, unit report) in L04, L05, L06: no hits (the word 'round' occurs only in 'rounded' and 'unrounded' in L06). "
    "No ellipsis outside code. Scope-word sentences read individually (see notes).")
row("L04-structure-hours", "2.9-prose", "course/modules/PC/PC3/L04.html (whole file); course/modules/PC/PC3/index.html line 29", "PASS",
    "data-hours=6; sections 1-9 plus References in BUILDER 4.2 order; why-it-matters 119 words (<=120); 4 misconceptions; "
    "problem tiers M1-M3, P1-P3, E1-E3, R1-R3 each with details.solution; quiz 12 items. Hub line 29: data-hours-lessons=36, "
    "data-hours-project=14 (sum 50); hub line 143 says six lessons of six hours each.")
row("L04-DAG-D-terms", "2.9-DAG", "course/modules/PC/PC3/L04.html lines 38, 60, 97, 158, 465", "PASS",
    "Links: expected-value-game (L03 #def), expectation, market-maker, bid-ask-spread, limit-order-book (all in closure). "
    "Adverse selection (line 158) is plain prose with no dfn and no link (D3). Inventory and mark-to-market are plain dfn without data-concept. "
    "No MS1, PR3, AP1 or S1 concept name or link appears in L04-L06; check_dag PASS.")
row("L04-A1-project-consistency", "2.4-notation", "course/modules/PC/PC3/L04.html line 72 (A1); course/modules/PC/PC3/project.html line 404", "PASS",
    "Arrival probabilities 1/4, 1/4, 1/2 agree (project.html line 404: 'probability 1/4 ... an uninformed buy', 'probability 1/4 ... an uninformed sell'). "
    "The Section-3 locator in A1 is row L04-lab-section-locator.")
row("L04-footer-registry-claim", "2.9-prose", "course/modules/PC/PC3/L04.html line 719 (site-footer)", "PASS",
    "'Each key result is proved on the page or computed by Lab 1, and each is graded.' Key results rows 1 to 5 are proved on the page "
    "(§2 to §4), row 6 is computed by Lab 1, and every row has a grade.")

# ---- L05
row("L05-def-3.1-markup", "2.4-mathematics", "course/modules/PC/PC3/L05.html line 106 (Definition 3.1)", "PASS",
    "Definition 3.1 'surviving at step i' with strict inequality; matches the pseudocode's strict comparison and the twin's break condition "
    "(tests/labs/PC3/lab-PC3-L05-1.py line 71).")
row("L05-prop-2.1-2.2-remark", "2.2-numbers", "course/modules/PC/PC3/L05.html lines 85-98", "PASS",
    "Prop 2.1 count (n-k+1)(k-1): exhaustive over {0,1,2}^n, n<=7, all k (l05_independent.out: naive count equals formula: True). "
    "Remark 2.2: (n-r)r <= n^2/4 with equality at r=n/2, n<=60: True.")
row("L05-prop-3.2-correctness", "2.4-mathematics", "course/modules/PC/PC3/L05.html lines 123-133 (Prop 3.2, Steps A-C)", "PASS",
    "Steps A, B, C re-read line by line; Step B's q-argument checked. Exhaustive {0,1,2}^n n<=7 and all k: outputs equal the brute-force "
    "window maximum (24604 cases); 3000 random cases, failures 0 (l05_independent.out).")
row("L05-prop-3.3-bound", "2.4-mathematics", "course/modules/PC/PC3/L05.html lines 135-142 (Prop 3.3 and proof)", "PASS",
    "Appends n, removals <= n, comparisons <= 2n: exhaustive small cases and 3000 random cases (max comparisons/(2n) = 0.9661); "
    "proof argument (tests = back removals + at most one failed test per step) re-read.")
row("L05-remark-3.4-k-range", "2.4-mathematics", "course/modules/PC/PC3/L05.html line 147 (Remark 3.4)", "PASS",
    "Input (k, k-1, ..., 2, k+1), n=k: the last step removes k-1 indices, k=2..11 (l05_independent.out 'Remark 3.4 ... checked', no failures).")
row("L05-example-3.5-trace", "2.2-numbers", "course/modules/PC/PC3/L05.html lines 151-153", "PASS",
    "Trace of (3,1,4,1,5), k=3 gives outputs (4,4,5) (l05_independent.out 'Example 3.5 outputs: [4, 4, 5]').")
row("L05-problems-M-P", "2.4-mathematics", "course/modules/PC/PC3/L05.html lines 344-396", "PASS",
    "M1 21 (formula); M2 trace of (2,5,1,0,3), k=2, outputs (5,5,1,3) re-traced by hand; M3 k=1 output is the input, k=n one entry; "
    "P1 peak at k=101 for n=200 (10000 = 100*100); P2 survival argument (strict inequality, largest index with value M); "
    "P3 n-1 for increasing sequences, checked by l05_seed6.py for all n<=12, k<=n.")
row("L05-E1-E3-numbers", "2.2-numbers", "course/modules/PC/PC3/L05.html lines 400-420 (E1, E3); expected block lines 298-320", "PASS",
    "E1: 169*31 = 5239 (printed), ratio 5239/382 = 13.717 -> 13.7 (printed counts). E3: row 200 prints comparisons 387, pushes 200, pops 194 "
    "(L05.stdout); bound 2n = 400; split bound 194 + 200 = 394. Both use printed values.")
row("L05-E2-seed6-numbers", "2.2-numbers", "course/modules/PC/PC3/L05.html lines 413-417 (Problem E2)", "FAIL",
    "The solution gives 350 deque comparisons, 200 pushes and 197 pops on the seed-6 sequence, and says 'Lab 1 does not print it'. "
    "My run (out/l05_seed6.out: 'twin deque_maxima on seed 6, k=8: comparisons 350 pops 197 pushes 200') reproduces them, so the values are "
    "correct, but no lab on the page produces them (Lab 1 uses SEED = 5 only, lab-PC3-L05-1.py line 23). Under VERIFIER 2.2(a) they are unsourced.",
    "Add a seed-6 line to Lab 1 Part 1 or Part 3 (for example, print the deque comparisons, pops and pushes for seed 6 at window 8), "
    "then run tools/embed_labs.py page --refresh lab-PC3-L05-1 and quote the printed values; or delete the seed-6 counts and keep "
    "only the statement that the outputs agree.")
row("L05-R1-scope-sentence", "2.9-prose", "course/modules/PC/PC3/L05.html lines 423-431 (R1)", "PASS",
    "No number; states that the lesson runs no timing protocol and proves operation counts only.")
row("L05-R2-R3", "2.2-numbers", "course/modules/PC/PC3/L05.html lines 432-446 (R2, R3)", "PASS",
    "R2: k=101, count 100*100 = 10000 (computed). R3: increasing sequence, n-1 comparisons for any k (P3, checked numerically).")
row("L05-key-results-grades", "2.3-grades", "course/modules/PC/PC3/L05.html lines 449-464", "PASS",
    "Rows 1 to 5 are T with proofs or Problem P3; row 6 is C and cites Lab 1 Part 2, which prints equal outputs for k=1..20 on seed 5.")
row("L05-quiz-answers", "2.9-prose", "course/modules/PC/PC3/L05.html quiz items 1-10 (lines 472-552)", "PASS",
    "21; 400; 10000; 'Yes' for the total bound; 5; n-1; last occurrence of the maximum (ties pop with <=, the code line 71); 1351 (printed); "
    "operation counts are not times; 'no outputs' for a window longer than the sequence.")
row("L05-misconceptions-canon-breaks", "2.9-prose", "course/modules/PC/PC3/L05.html lines 324-348 (Section 4 canon breaks and Section 5 misconceptions)", "PASS",
    "Canon-breaks names model limits (count is not time; comparable values; edge convention). Misconception 1 cites 354 within 400 (printed).")
row("L05-structure-hours", "2.9-prose", "course/modules/PC/PC3/L05.html (whole file)", "PASS",
    "data-hours=6; section order 1-9 with Remark, Problem set, Key results, Quiz, References; why-it-matters 89 words; 3 misconceptions; "
    "problem tiers each 3 items with details.solution; quiz 10 items.")
row("L05-markup-raw-less-than", "2.9-prose", "course/modules/PC/PC3/L05.html (Definition 3.1 and math)", "PASS",
    "Less-than signs are escaped (&lt;) inside the HTML; rendered math verified by page_smoke (all math rendered).")
row("L05-meta-uses-hash-map-heap", "2.9-DAG", "course/modules/PC/PC3/L05.html lines 38-40 and Remark 3.6 lines 157-158", "PASS",
    "Hash map and binary heap linked to the closure (CS2) concepts; Remark 3.6 does not use them as dfn.")
row("L05-meta-uses-other", "2.9-DAG", "course/modules/PC/PC3/L05.html line 38 (Uses list)", "PASS",
    "big-O, monotonic deque, unit test: CS2 and CS1 concepts, all linked and in the closure.")
row("L05-why-it-matters-comparisons", "2.9-prose", "course/modules/PC/PC3/L05.html line 52", "PASS",
    "'at most twice the input length in comparisons' matches Prop 3.3 (<= 2n).")
row("L05-footer-registry-claim", "2.9-prose", "course/modules/PC/PC3/L05.html line 567 (site-footer)", "PASS",
    "Footer: each key result is proved on the page or computed by Lab 1, and each is graded. Row 6 is Lab 1 Part 2; all rows graded.")
row("L05-DAG-links", "2.9-DAG", "course/modules/PC/PC3/L05.html lines 38, 106, 157-158", "PASS",
    "check_dag PASS. timed-coding-interview defined once (line 58, dfn with data-concept); no link to a later lesson.")

# ---- L06
row("L06-prop-1.1-payoff-identity", "2.4-mathematics", "course/modules/PC/PC3/L06.html lines 58-66", "PASS",
    "(s-K)^+ - (K-s)^+ = s-K: both cases re-derived (lines 65).")
row("L06-remark-1.2-put-call-parity", "2.4-mathematics", "course/modules/PC/PC3/L06.html lines 69-71", "PASS",
    "Price form call - put = S - DK with D = e^{-r tau} matches course/modules/FC/FC2/L05.html line 59 (put-call-parity definition, C - P = S - DK).")
row("L06-definition-1.3-NPV-and-prop-3.1", "2.4-mathematics", "course/modules/PC/PC3/L06.html lines 73-76, 110-118", "PASS",
    "NPV formula matches course/modules/CF/CF1/L01.html line 60. Prop 3.1 (i) affine, (ii) strictly increasing, (iii) unique break-even: "
    "re-derived; exact identity on a grid (l06_independent.out 'Prop 3.1 (i) identity exact on grid: True').")
row("L06-prop-2.1-forward", "2.4-mathematics", "course/modules/PC/PC3/L06.html lines 90-98", "PASS",
    "(i) zero-cost portfolio paying F' - S/D; (ii) both sides by A4 with A5 for the reverse portfolio. Numerically: "
    "l06_independent.out quote 10000 payoffs 0 and quote 10100 payoffs 100 at five spot values; reverse-portfolio identity True.")
row("L06-remark-2.2-continuous-convention", "2.9-DAG", "course/modules/PC/PC3/L06.html lines 86, 101-104", "PASS",
    "FC2 L02 Assumption A4 (line 81) and Definition 2.1 (line 88): continuous compounding and F* = S e^{r tau}, so S/D = S e^{r tau} with D = e^{-r tau}.")
row("L06-corollary-3.3-grade", "2.4-mathematics", "course/modules/PC/PC3/L06.html lines 130-139", "PASS",
    "Statement and proof (line 137) re-derived: at l < u* < h the signs at the endpoints are opposite (NPV = mA(u-u*)).")
row("L06-prop-3.2-fermi-bounds", "2.4-mathematics", "course/modules/PC/PC3/L06.html lines 120-128", "PASS",
    "Induction re-read; positivity used to preserve order; ends attained. Random product check: l06_independent.out 'Prop 3.2 random product check: True'.")
row("L06-example-4.2-numbers", "2.2-numbers", "course/modules/PC/PC3/L06.html lines 146-150 (Example 4.2)", "PASS",
    "Fermi range [200, 1600] (2000*1*1/10, 4000*2*1/5); A = 3310/1331 exact; break-even 399300/331 = 1206.344 (l06_independent.out); "
    "NPV negative at 200 and positive at 1600 (-12513148, 4894816 printed).")
row("L06-remark-4.3-sensitivity", "2.2-numbers", "course/modules/PC/PC3/L06.html lines 153-155 (Remark 4.3)", "PASS",
    "Unrounded break-evens 1164.1005421, 1206.3444109, 1249.0469417 (l06_independent.out) match 1164.1005, 1206.3444, 1249.0469. "
    "Differences 42.24 (8 to 10) and 42.70 (10 to 12) confirmed. NPV signs at all three rates confirmed (display values match the printed lab rows).")
row("L06-E1-12pct", "2.2-numbers", "course/modules/PC/PC3/L06.html lines 395-401 (Problem E1)", "PASS",
    "A(12%) = 2.4018313 (l06_independent.out), break-even 3000/A = 1249.0469 = the value Lab 1 prints (1249.05).")
row("L06-E2-first-negative", "2.2-numbers", "course/modules/PC/PC3/L06.html lines 402-408 (Problem E2)", "PASS",
    "Grid 200..1600 step 100 at 10%: positive at 1300, 1400, 1500, 1600 (count 4), largest negative 1200. "
    "NPV(1200) = -105000000/1331 = -78888.05, NPV(1300) = 1550000000/1331 = 1164537.94 (exact, l06_independent.out).")
row("L06-E3-42.71", "2.2-numbers", "course/modules/PC/PC3/L06.html lines 410-416 (Problem E3)", "PASS",
    "Width 1249.0469 - 1164.1005 = 84.9464 -> 84.95; /4 = 21.2366 -> 21.24; 42.2439 -> 42.24; 42.7025 -> 42.70; "
    "the difference of displayed values 1249.05 - 1206.34 = 42.71 is correctly rejected (l06_independent.out).")
row("L06-E3-rest-and-quiz-q9", "2.2-numbers", "course/modules/PC/PC3/L06.html lines 409-416 and quiz item 9 (lines 518-522)", "PASS",
    "Quiz item 9 answer 21.24 with tolerance 0.01 matches E3 (21.2366 -> 21.24).")
row("L06-M1-M3-numbers", "2.2-numbers", "course/modules/PC/PC3/L06.html lines 345-366 (M1-M3)", "PASS",
    "M1: 4900/0.98 = 5000, payoff 50; M2: 500/121 = 4.1322 (l06_independent.out 'M2 NPV: ... True'); "
    "M3: 33275/331 = 100.5287 -> 100.53 (l06_independent.out 'M3 u* exact ... True').")
row("L06-P1-P3-proofs", "2.4-mathematics", "course/modules/PC/PC3/L06.html lines 370-390", "PASS",
    "P1 reverse portfolio: cost S - S = 0 by A3, payoff S/D - F' (re-derived). P2 affine with slope mA > 0, unique zero. "
    "P3 bounds 200 and 1600, attained at (2000,1,1/10) and (4000,2,1/5).")
row("L06-R1-R3", "2.2-numbers", "course/modules/PC/PC3/L06.html lines 418-440 (R1-R3)", "PASS",
    "R1: each factor ratio is 2, so each log-width ln 2 (tie). R2: closed form I/sum m_t(1+r)^-t. "
    "R3: m* = 3769.83 cents, 0.75397 of 5000, fall 24.6 percent (l06_independent.out 'R3 m* = 3769.826 ... fall 24.60').")
row("L06-quiz-answers", "2.9-prose", "course/modules/PC/PC3/L06.html quiz items 1-10 (lines 466-536)", "PASS",
    "5000; F' - S/D; 'equals S/D with no expectation'; 4.13 (500/121 = 4.1322); 1206.34; 'nothing, the range straddles'; "
    "4 grid points; rises strictly; 21.24; balance-sheet cash. All re-derived.")
row("L06-canon-breaks-and-misconceptions", "2.9-prose", "course/modules/PC/PC3/L06.html lines 310-337", "PASS",
    "Model limits named. Misconception 2: 21 units per point (84.95/4 = 21.24, derived from printed rates). "
    "Misconception 4: signs at the bounds same at 8, 10, 12 percent (verified).")
row("L06-DAG-and-cross-links", "2.9-DAG", "course/modules/PC/PC3/L06.html lines 38-39, 56, 75, 86", "PASS",
    "forward-contract, cost-of-carry-forward-price, put-call-parity, net-present-value, statement-articulation linked to prerequisite modules; "
    "fermi-estimation linked to L01 #def-fermi-estimation (earlier lesson). check_dag PASS.")
row("L06-articulation-claim-linked", "2.9-DAG", "course/modules/PC/PC3/L06.html line 75 and quiz item 10", "PASS",
    "course/modules/AC/AC1/L03.html line 57 defines articulation: 'the cash-flow statement ends at the balance-sheet cash'.")
row("L06-footer-registry-claim", "2.9-prose", "course/modules/PC/PC3/L06.html line 548 (site-footer)", "PASS",
    "Footer claim true for L06 key results: rows 1-5 proved on the page, row 6 cites Lab 1 Part 2; all rows graded.")
row("L06-structure-hours", "2.9-prose", "course/modules/PC/PC3/L06.html (whole file)", "PASS",
    "data-hours=6; sections 1-9 plus References; why-it-matters 76 words; 4 misconceptions; problem tiers 3 each with details.solution; quiz 10 items.")

fragment = {
    "unit": "PC3",
    "slice": "PC3-b",
    "round": 8,
    "verifier": "Claude Haiku 5.5, independent verifier for PC3-b round 8 (did not build PC3)",
    "pin": "0dee921a33dc1275ff9b1babc6c2fdf3daac62c3",
    "base": "06994db16d1ab449bcf29898a7f56cfa999dce57 (round-7 pin). Delta 06994db1..0dee921a touches L04.html (Prop 3.1 hypotheses, Cor 3.3, Remark 1.2 and 4.2 wording, problem wording, quiz wording, footer), L05.html (footer only), L06.html (Example 4.2-linked misconception wording and footer), tests/labs/PC3/lab-PC3-L04-1.py (docstring only). Every row was re-verified from the entire pages in this round; no PASS row is carried from round 7.",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE8-PC3-b",
    "scratch": "/Users/billyribeiro/.fanout/wt/verifyE8-PC3-b/ledgers/PC3/scripts/PC3-b-r8/out",
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Slice b: course/modules/PC/PC3/L04.html, L05.html, L06.html and tests/labs/PC3/lab-PC3-L04-1.py, lab-PC3-L05-1.py, lab-PC3-L06-1.py. cards.json, project.html and the grader are outside this slice and are not checked here.",
        "Mutants: none. Lab twins are demonstrations; mutation testing applies to project graders (ruling). No grader mutant is claimed.",
        "Four FAIL rows: L04-lab-section-locator (introduced by this round's delta), lab-L04-1-hypothesis-interpretation (interpretation omits H1 of Prop 3.1), L04-E1-seed1-numbers and L05-E2-seed6-numbers (correct values that no lab on the page prints or derives). Round-7 FAIL rows L04-prop-3.1-closed-form, L04-corollary-3.3, L04-key-results-prop-3.1-assumptions, L04-canon-breaks-quote-rule, L04-R2-spread-criterion, L04-problems-R1-R3-M-P, L04-quiz-answers, L04-footer-registry-claim, L05-footer-registry-claim and L06-footer-registry-claim are re-verified and PASS.",
        "Scope-word sentences were read individually in all three pages. Sentences with every, all, always, only, any, same and exactly were checked against a proof, a finite enumeration or a lab line; none fails beyond the rows above.",
        "Ungraded model-limit statements (for example, L04 Section 5: 'A market maker in a limit order book also sees the queue of resting orders at each price'; L06 Section 5: 'Real assets pay income, real borrowing and lending rates differ, and short sales have costs') are descriptions of the model's limits, not results the unit relies on; they are not graded and are not counted as failures. The pages grade theorem titles and key-results rows, which is the page convention.",
        "Round-8 scratch scripts (repository paths): ledgers/PC3/scripts/PC3-b-r8/embed_compare.py, l04_independent.py, l05_independent.py, l05_seed6.py, l06_independent.py, build_fragment.py; outputs in ledgers/PC3/scripts/PC3-b-r8/out/.",
    ],
    "summary": {},
}

counts = {"rows": len(rows), "pass": 0, "fail": 0, "unverifiable": 0}
for r in rows:
    counts[{"PASS": "pass", "FAIL": "fail", "UNVERIFIABLE": "unverifiable"}[r["status"]]] += 1
fragment["summary"] = counts

out = ROOT / "ledgers" / "PC3" / "PC3-b.json"
out.write_text(json.dumps(fragment, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("wrote", out, counts)
