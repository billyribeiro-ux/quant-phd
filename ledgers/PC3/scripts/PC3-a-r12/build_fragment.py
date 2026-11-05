"""Round-12 PC3 slice a fragment builder: writes ledgers/PC3/PC3-a.json from the evidence recorded by the round-12 verifier.

Run from the checkout root: python3 -I ledgers/PC3/scripts/PC3-a-r12/build_fragment.py
Every evidence string names a script or an output under ledgers/PC3/scripts/PC3-a-r12/ or a locator read in the pin.
"""

import datetime
import json
import sys

PIN = "5db69a9bee460736c318ebfacc7200ee5a6eb0f0"
PREV = "00a84795f276456fce19d4181373cc4efba11a36"
G = "ledgers/PC3/scripts/PC3-a-r12/outputs"
N = "ledgers/PC3/scripts/PC3-a-r12/numbers_r12.py"

R = []


def row(rid, check, location, evidence):
    R.append({"id": rid, "check": check, "location": location, "status": "PASS", "evidence": evidence})


# ---- mechanical gates (run_gates.sh, exit codes in outputs/exit_codes.txt) ----
row("PC3a-check-pages", "2.9 structure: check_pages --unit PC3 (hub, L01-L03 and the rest of the unit)",
    "index.html; L01.html; L02.html; L03.html",
    f"run_gates.sh; {G}/check_pages.out = 'check_pages PC3: PASS'; exit_codes.txt check_pages exit=0 (run at pin {PIN[:8]}).")
row("PC3a-check-dag", "2.9 DAG: check_dag --unit PC3 plus an independent link scan",
    "index.html; L01.html; L02.html; L03.html",
    f"{G}/check_dag.out = 'check_dag PC3: PASS', exit 0. Independent grep of data-concept links: index.html uses "
    "exponential-and-logarithm, taylor-theorem (M1, M2), expectation, independence, conditional-expectation-elementary "
    "(M4), big-o-complexity, hash-map, binary-heap, monotonic-deque (CS2), cost-of-carry-forward-price (FC2), "
    "net-present-value (CF1), statement-articulation (AC1); all owners checked in curriculum/curriculum.json 'concepts' "
    "and all in the closure {AC1,CF1,CS1,CS2,E1,FC1,FC2,M1,M2,M4,P0.1}. L01 links M1/M2 concepts and defines fermi-estimation "
    "(L01.html dfn); L02 links M4 concepts only; L03 links expectation and defines expected-value-game (L03.html dfn).")
row("PC3a-check-projects", "2.6 projects: check_projects --unit PC3 (tool result only; project pages are not in this slice)",
    "course/modules/PC/PC3/project.html",
    f"{G}/check_projects.out = 'check_projects PC3: PASS', exit 0.")
row("PC3a-run-labs", "2.5 labs: run_labs --unit PC3 (page code equals twin; expected block equals output)",
    "tests/labs/PC3/lab-PC3-L01-1.py, L02-1.py, L03-1.py; L01.html:144-311; L02.html:132-360; L03.html:112-287",
    f"{G}/run_labs.out = 'run_labs PC3: PASS (9/9)', exit 0; run_labs_L01/L02/L03.out each 'PASS (1/1)', exit 0.")
row("PC3a-twins-alone", "2.5 labs: each slice twin alone under python -I -W error, no network",
    "tests/labs/PC3/lab-PC3-L01-1.py, L02-1.py, L03-1.py",
    "Each twin copied alone into a fresh mktemp directory under /tmp and run as python3 -I -W error: exit 0 for L01, L02, L03; "
    "stderr 0 bytes; stdout 26, 32 and 30 lines saved to outputs/twin-L01-1.stdout, twin-L02-1.stdout, twin-L03-1.stdout. "
    "grep for open(, urllib, socket in the three twins: 0 hits.")
row("PC3a-pytest-labs", "2.5 labs: pytest -q -k PC3 (tests/test_labs.py PC3 cases)", "tests/test_labs.py",
    f"{G}/pytest_pc3.out: nine dots, [100%]; exit 0 (exit_codes.txt pytest_pc3 exit=0).")
row("PC3a-page-smoke", "2.9 page_smoke, run alone on each of the four slice pages", "index.html; L01.html; L02.html; L03.html",
    f"{G}/page_smoke_index.out, page_smoke_L01.out, page_smoke_L02.out, page_smoke_L03.out: each prints "
    "'page_smoke PC3: PASS'; each reports its lab timing (0.0 s) and runtime boot; exit 0.")
row("PC3a-ruff-mypy", "2.5 labs: ruff check, ruff format --check and mypy --no-incremental on the twins",
    "tests/labs/PC3/lab-PC3-L01-1.py, L02-1.py, L03-1.py",
    f"{G}/ruff_check.out 'All checks passed!'; ruff_format.out '9 files already formatted'; mypy.out "
    "'Success: no issues found in 9 source files'; all exit 0.")
row("PC3a-verify-refs", "2.1 citations: verify_refs --offline (registry integrity) and verify_refs --unit PC3 (live)",
    "references/references.json; index.html:177",
    f"{G}/verify_refs_offline.out: 'offline integrity: 560 entries, 0 problems', exit 0. "
    f"{G}/verify_refs_unit_live.out: 'live re-verification of PC3: 2 of 560 entries, 0 problems', exit 0 "
    "(the two keys zhou2008practical and crack2015heard, both verified_by openlibrary).")
row("PC3a-hub-hours", "2.9 structure: the hours split sums to the declared figure",
    "index.html:29, 42, 167; L01.html:34; L02.html:34; L03.html:34",
    "index.html:42 '36 h lessons · 14 h project (28%)'; index.html data-hours-lessons=\"36\", data-hours-project=\"14\"; "
    "six lessons at 6 h (index.html:145-150). index.html:167 gives the seven project lines 1 + 1 + 3 + 2 + 2 + 4 + 1 = 14 "
    "and 14/50 = 28 percent. project.html:421-434 time-budget table (read at the pin): 1, 1, 3, 2, 2, 4, 1 and Total 14, "
    "'Equals the project hours in the hub: 14 of the module's 50, or 28.0 %'. data-hours=\"6\" on L01, L02, L03 and "
    "'6 study hours' on each page.")
row("PC3a-hub-placement", "2.2/2.4 numbers and answers: placement diagnostic, ten items",
    "index.html:72-136 (data-answer, data-correct, data-mastery=\"0.8\")",
    f"Ten items at index.html:76, 81, 86, 91, 96, 105, 114, 119, 128, 133. data-answer 3.5, 0.25, 2, 3, 90.909091 "
    f"(tolerance 1e-6), -10005, 10040; the three mc keys carry data-correct on O(log n) (line 99), S e^(r tau) (line 108) "
    f"and 'Assets = liabilities + equity' (line 122). {N} (output {G}/numbers_r12.out): E[face] = 7/2, P(both heads) = 1/4, "
    "ln(e^2) = 2, d/dx x^3 at 1 = 3, 100/1.1 = 90.9090909..., the 80 percent bar needs 8 of 10. Eight items test the "
    "prerequisites (M4 x2, M1, M2, CS2, FC2, CF1, AC1), two are skill checks (lines 128, 133).")
row("PC3a-hub-titles-prereqs", "2.9 structure: hub titles and prerequisite closure",
    "index.html:35, 61-67",
    "index.html:35 names M4, CS2, FC2 and the closure M1, M2, AC1, CF1, CS1, E1, FC1, P0.1. Titles checked in "
    "curriculum/curriculum.json parts[].modules: M4 Probability, CS2 Algorithms & Data Structures, FC2 Derivatives "
    "Fundamentals, M1 Precalculus & Mathematical Reasoning, M2 Single & Multivariable Calculus, PC3 Quant & Finance "
    "Interviews, AC1 Financial Accounting, CF1 Time Value & Capital Budgeting, FC1 The Financial System, Markets & "
    "Instruments, CS1 Programming in Python from Zero, E1 Microeconomics, P0.1 How to Study This Program. The prerequisite "
    "graph (prereqs fields) gives the closure {AC1,CF1,CS1,CS2,E1,FC1,FC2,M1,M2,M4,P0.1}, which is the 11 modules of "
    "plans/PC3-build-plan.md §0.2; index.html:61-67 names the 3 direct and the 8 others.")
row("PC3a-hub-objectives", "2.9 prose: the seven objectives match the lessons", "index.html:47-55",
    "Seven objectives with measurable verbs (Bound, Compute, Compute, Derive, Implement, Compute, Write). Lesson-specific "
    "objectives match: L01 Theorem 1.2 and Proposition 1.3 (L01.html:68, 85); L02 Definition 2.2, Propositions 2.4 and 2.5 "
    "(L02.html:66, 76, 89); L03 Definition 3.1, Proposition 3.2 and Theorem 3.8 (L03.html:61, 66, 297). Objective 3's "
    "'stopping rule ... finite fair game' matches Theorem 3.8 with A3 over a finite horizon.")
row("PC3a-hub-lesson-map", "2.9 structure: lesson map cards link every lesson", "index.html:145-150; L01.html:35, L02.html:35, L03.html:35",
    "index.html:145-150 has six cards L01..L06 at 6 h each, each href present in the unit (L01.html..L06.html). Card titles "
    "'Fermi Estimation and Mental Math', 'Probability Puzzles and Conditional Reasoning', 'Expected-Value Games' equal the "
    "H1 of L01.html:35, L02.html:35, L03.html:35.")
row("PC3a-hub-data", "2.8 data: no dataset and no data-files on any slice page or lab", "index.html:37, 170-173; tests/labs/PC3/lab-PC3-L01-1.py, L02-1.py, L03-1.py",
    "grep -c data-files on index.html, L01.html, L02.html, L03.html: 0 each. Twins: no open(, urllib or socket (grep). "
    "index.html:37 and 171-172 say no data file is read, and L02.html:134 and 359 label the drill items as generated.")
row("PC3a-hub-P0.1-claim", "2.9 prose: the P0.1 claims", "index.html:35, 74; course/concepts.html:34-47",
    "course/concepts.html:34-47: each P0.1 entry ends 'not yet released' (eleven entries, read). index.html:35 and 74 say "
    "so. No href in index, L01, L02 or L03 points to a P0.1 concept (grep of href values lists only concepts.html anchors "
    "of closure concepts and lesson anchors).")
row("PC3a-L01-numbers", "2.2 numbers in prose and rounding (whole page)",
    "L01.html:55, 99-100, 107, 137-141, 287-309, 328, 336, 401-415, 433, 447, 462-465",
    f"{N} / {G}/numbers_r12.out: bounds 12000 and 234000; ratio 19.5; ln 19.5 = 2.9704144656; factor widths 1.0986, 1.6094, "
    "0.2624 summing to 2.9704144656; geometric midpoint 52990.5651979671 (52 990.57 to two decimals); narrowing reductions "
    "0.4055, 0.9163, 0.1754 with shares 13.65, 30.8472, 5.9033 percent. Example 1.7: remainder 0.0046221254, bound "
    "0.0048728552, ratio 0.948546 (0.9485), bound over remainder minus 1 = 0.054245 (5.4 percent); x = 1/20: miss 0.1289 "
    "(7.91 percent of exact 1.6289), bound 0.1662. All match the prose and the printed block (L01.html:284-309).")
row("PC3a-L01-proofs", "2.4 mathematics: Theorem 1.2, Proposition 1.3, Theorem 1.5, Remark 1.6, problems P1-P3",
    "L01.html:76-80, 92-94, 128-135, 374-391",
    "Re-derived by hand: ab - a'b' = a(b - b') + b'(a - a') and AB - ab = A(B - b) + b(A - a), with each term nonnegative under "
    "the stated positivity (L01.html:78); induction hypotheses 0 < L <= P <= U give both inequalities (L01.html:79). "
    "Proposition 1.3: ln of a product of positive ratios is the sum (L01.html:94). Theorem 1.5: f' = n(1+t)^(n-1), "
    "f'' = n(n-1)(1+t)^(n-2); Lagrange gives 1/2 n(n-1)(1+xi)^(n-2) x^2 with 1 <= (1+xi)^(n-2) <= (1+x)^(n-2) (L01.html:130); "
    "Remark 1.6 n = 2 equality. P1 (reciprocal bounds, Theorem 1.2 for a/b), P2 (Bernoulli, induction step multiplies by "
    "1+x > 0 and uses n x^2 >= 0), P3 (binomial tail) checked line by line.")
row("PC3a-L01-A2-false-at-x0", "2.4 mathematics: assumption used only where it holds", "L01.html:115 (A2), 123 (H3), 130 (x = 0)",
    "A2 is stated for x != 0 (L01.html:115). Theorem 1.5 (H3, L01.html:123) applies A2 only for x > 0. The proof treats x = 0 "
    "directly (L01.html:130): both sides are 0. Correct.")
row("PC3a-L01-grades-lab-only", "2.3 grades: T for proved results, C for lab-printed results", "L01.html:458-465 (key results)",
    "Rows 458-462 are T and proved or hand-computed on the page (Theorem 1.2, Proposition 1.3, Theorem 1.5, the Example 1.4 "
    "bounds, the width identity). Rows 463-465 are C and name Lab 1 Parts 1-3 (L01.html:463-465). The lab prints the same "
    "values (outputs/twin-L01-1.stdout, Parts 1-3).")
row("PC3a-L02-grade-drill-lab-only", "2.3 grades: lab-only result graded C", "L02.html:508",
    "L02.html:508 'Generated drill set: the closed form equals the enumeration on 12 of 12 items' is graded C and names Lab 1, "
    "Part 1 (seed 0). twin-L02-1.stdout prints 'closed form equals enumeration on 12 of 12 items'.")
row("PC3a-L01-claims", "2.3/2.9 prose claims checked against the proofs and the lab",
    "L01.html:67-90, 82, 105-107, 113-141, 317-319, 328",
    "L01.html:105 'exactly the drop' holds by Proposition 1.3 (the total is a sum over factors). 'at most that small width' "
    "holds because a narrowing has nonnegative log width. L01.html:107 values 2.5649, 0.4055, 2.0541, 0.9163, 2.7951, "
    "0.1754 and the 30.8 and 5.9 percent shares recomputed in numbers_r12.out. L01.html:317-319 (no probability, correlated "
    "factors, nonnegative x) and L01.html:82 (worst case) match Theorem 1.2 and the proof's use of ranges only.")
row("PC3a-L01-lab-match", "2.5 labs: page code equals twin; expected block equals twin output", "L01.html:144-311; tests/labs/PC3/lab-PC3-L01-1.py",
    "run_labs PASS (outputs/run_labs_L01.out). The page code (L01.html:147, <pre><code data-run>) equals the twin after the "
    "trailing newline (stripped equal; the exact string differs only by the final newline). pre.expected (L01.html:284, "
    "data-tolerance 1e-9) equals twin-L01-1.stdout line for line (26 lines, identical).")
row("PC3a-L01-problems-quiz", "2.9 structure: problem tiers, worked solutions and quiz", "L01.html:345-451 (13 problems), 470-548 (quiz)",
    "13 <details class=\"solution\"> blocks in L01.html: M1-M3, P1-P3, E1-E4, R1-R3 (Mechanics 3, Proof 3, Empirical 4, "
    "Research 3). Quiz: 10 items at L01.html:475, 484, 489, 498, 503, 512, 517, 526, 535, 540, each with an explanation "
    "(8 to 15 required).")
row("PC3a-L01-only-scope", "2.9 scope: the exceptions named to 'only the ordinary order and arithmetic'", "L01.html:55, 82, 314",
    "L01.html:55 lists the non-arithmetic tools: logarithm (M1, used in Proposition 1.3 and Example 1.4), derivatives and Taylor "
    "(M2, Section 3), binomial theorem (Remark 1.6), square root (geometric midpoint, Example 1.4). Each appears only where "
    "stated (L01.html:94, 99, 114-130, 135, 100). The lemma of Theorem 1.2 and the induction use order and arithmetic only.")
row("PC3a-L01-twin-docstring-decimals", "2.5 labs: twin docstring matches the code", "tests/labs/PC3/lab-PC3-L01-1.py:1-8, 96",
    "Docstring (lines 1-8 region) says fractions for bounds and grid, floats for log widths, a 1e-12 float check and ten-place "
    "printing. Code: Fraction bounds and grid (product_bounds, grid_products), math.log widths, "
    "abs(sum(parts) - width) < 1e-12, and :.10f on ratio, midpoint, widths and Part 3 values. Matches.")
row("PC3a-L01-research-problems", "2.4 mathematics: research problems R1-R3 answers", "L01.html:430-449",
    f"{N}: half of ln 19.5 is 1.4852; ln 5 = 1.6094 exceeds it, ln 3 = 1.0986 and ln 1.3 = 0.2624 do not (R1). R2: the proof "
    "uses only (H1) and (H2) (no joint distribution) (R2). R3: A = [1,3] reduced to [1,2] gives ln(3/2) = 0.4055; B = [1,2.5] "
    "reduced to [1,1.01] gives ln(2.5/1.01) = 0.9063 > 0.4055, so the claim fails (R3). E3 (L01.html:415): 198000, ratio 16.5, "
    "ln 16.5 = 2.8034, change 0.167054, width decreased. R1 part (c) is answered by dominance (L01.html:433); see notes.")
row("PC3a-L01-misconception-accuracy", "2.2/2.3 misconception: wrong belief and correction", "L01.html:327-328",
    "Correction values 0.1754 (5.9 percent of 2.9704) and 0.9163 (30.8 percent) match numbers_r12.out; the drop-is-the-same claim "
    "follows from Proposition 1.3; the share depends on the other widths through the total. Correct.")
row("PC3a-L01-KR-ln19.5-grade", "2.3 grades: key-results rows 462 and 463", "L01.html:461-463",
    "Row 462 is T (Proposition 1.3 and Example 1.4 by hand). Row 463 is C and names 'Lab 1, Part 1 (printed floating-point "
    "value)'. 2.9704144656 = ln 19.5 by numbers_r12.out.")
row("PC3a-L01-E2-shares", "2.2 numbers: E2 solution (shares of the total width); round-9 FAIL re-verified after the fix",
    "L01.html:405-410 (E2 solution at 408)",
    f"{N} / numbers_r12.out: 0.9163 / 2.9704 = 0.3084770 -> 0.308477, 30.8477 percent, 30.85 percent to two places, 30.8 to one; "
    "full-precision 0.9162907319 / 2.9704144656 = 0.3084724 -> 0.308472 and 30.8 percent; minutes 0.1753528875 / "
    "2.9704144656 = 0.059033 -> 5.9 percent. L01.html:408 matches every value.")
row("PC3a-L01-claims-E1", "2.2 numbers: E1 ratio", "L01.html:401-404",
    "0.0046221254 / 0.0048728552 = 0.9485456 (numbers_r12.out); the solution's 0.94854... and 0.9485 are its prefix and 4-place value.")
row("PC3a-L02-numbers", "2.2 numbers: examples, exercises and key rows", "L02.html:111-130, 398-417, 449-466, 489-493, 503-507",
    f"{N} (outputs/numbers_r12.out): Example 2.6 gives 1/3 and 1/2, reverse conditional 1; Example 2.7 gives 3/5, 3/5, 3/10 and "
    "P(second red | first blue) = 3/4; Example 2.8 gives 1/3, 2/3 (rule A) and 1/2, 1/2 (rule B); Example 2.9 gives 1/2 and 3/4; "
    "M1 1/6, M2 P(B) = 29/100 and P(A|B) = 15/29, M3 2/5 (12/30), E1 57/64, R3 conditional 1.")
row("PC3a-L02-proofs", "2.4 mathematics: Propositions 2.4 and 2.5, P1-P3 (with the C_i rename)", "L02.html:75-100, 423-441",
    "Proposition 2.4: both products equated and divided by P(B) > 0 (L02.html:84-86). Proposition 2.5: disjoint pieces B and C_i, "
    "H2 gives Definition 2.2 (L02.html:98-99). P1: equivalence by multiplying by P(B) > 0. P2: three-cell case. P3: "
    "Prob_B(Omega) = 1 and additivity on disjoint C_1, C_2. All hypotheses used are listed.")
row("PC3a-L02-lab-match", "2.5 labs: page code equals twin; expected block equals twin output", "L02.html:132-360; tests/labs/PC3/lab-PC3-L02-1.py",
    "run_labs PASS (outputs/run_labs_L02.out). Page code equals the twin after the trailing newline. pre.expected (L02.html:327, "
    "data-tolerance 0) equals twin-L02-1.stdout line for line (32 lines).")
row("PC3a-L02-interp-reverse-conditional", "2.2 interpretation: reverse conditional", "L02.html:359",
    "1/3 against 1 for two flips, both printed by Part 4 (twin-L02-1.stdout: 'P(both heads | at least one head) = 1/3' and "
    "'P(at least one head | both heads) = 1').")
row("PC3a-L02-misconceptions-quiz", "2.9 structure: misconceptions and retrieval quiz", "L02.html:376-388; L02.html:517-587",
    "Three misconceptions (L02.html:377, 381, 385). Quiz: 10 items at L02.html:518, 527, 532, 541, 546, 555, 560, 569, 574, 583, "
    "each with an explanation; the values (1/3, 2/3, 3/5, 1/2, 3/4, 1, 3/10) match numbers_r12.out.")
row("PC3a-L02-where-canon-breaks", "2.9 prose: canon-breaks bullets", "L02.html:362-371",
    "L02.html:366: rule A gives 2/3 and rule B gives 1/2 (Example 2.8, numbers_r12.out); L02.html:367 swap symmetry (Example 2.7); "
    "L02.html:368 the two readings of Example 2.6; L02.html:369 A1 finite spaces. Each bullet is backed by a computed value or A1.")
row("PC3a-L02-twin-bag-ball-label", "2.5 labs: twin labels equal the page's examples", "tests/labs/PC3/lab-PC3-L02-1.py Parts 3-4; L02.html:116, 129",
    "Twin Part 3 bags {bag 1: (3 red, 1 blue), bag 2: (1 red, 3 blue)} equal Example 2.9 (L02.html:129). Twin Part 4 balls r1-r3, b1, b2 "
    "(urn of three red and two blue) equal Example 2.7 (L02.html:116).")
row("PC3a-L02-finite-probability-space-redefined", "2.4 definitions: Definition 2.1 attribution to M4 Lesson 1",
    "L02.html:57; L02.html:62", "course/modules/M/M4/L01.html:55 defines a finite probability space: weights p(omega) > 0 summing to 1 "
    "(read). L02.html:57 cites M4 Lesson 1 for that definition; the link target course/modules/M/M4/L01.html exists.")
row("PC3a-L02-spaced-repetition", "2.9 structure: curriculum lab 'timed ... with spaced repetition' (curriculum yaml:174)",
    "L02.html:132-134 (lab hypothesis), 359 (interpretation); L02.html:515; review.html:7, 35",
    "L02.html:134: 'The drill set has no spacing of its own'; spacing comes from this lesson's cards via the review deck. "
    "review.html:7 and :35 name the FSRS-4.5 scheduler. The curriculum string is routed through the cards; see notes.")
row("PC3a-L03-numbers", "2.2 numbers: expectations, continuation values, fee sensitivity, biased-game values",
    "L03.html:80, 102-104, 322, 329-337, 340-356, 418-432, 441-450, 455-457",
    f"{N}: E[face] = 7/2; 100 x 7/2 = 350; continuation 250; backward value 1150/3 = 383.33; choice gain 100/3 = 33.33; "
    "fair game zero for all five rules over six turns (recursion and 64 sequences); biased play-all 150, first win and first "
    "loss 1575/32, total >= 100 gives 575/8, total +-200 gives 625/8 (recursion and brute force agree); E2 -575/8 = -71.875; "
    "R1 mean 50; R2 fee c = 100 gives 100/3, c = 1 gives 149/2 = 74.5.")
row("PC3a-L03-proofs", "2.4 mathematics: Proposition 3.2, Theorem 3.8 and proof, Definition 3.7",
    "L03.html:66-76, 107-110, 296-311",
    "Proposition 3.2: distributive law and exchange of finite sums (L03.html:75). Theorem 3.8 (L03.html:307-311): base t = N uses "
    "H3 and Definition 3.7; step: V(h) = sum_x P(x|h) V(h,x) with V(h,x) = W(h) + x gives W(h) times a sum of 1 plus a sum of "
    "x P(x|h), which is 0 by H2; empty history gives E[W] = 0. Definition 3.7 matches W(h) and the forced stop at length N.")
row("PC3a-L03-A3-zero-probability-histories", "2.4 mathematics: A3 and H2 quantify positive-probability histories only",
    "L03.html:292-293 (A3), 300 (H2), 308 (proof)",
    "A3 and H2 both quantify histories with positive probability (L03.html:293, 300); the proof restricts to them (L03.html:308) "
    "and says zero-probability histories add nothing. Consistent.")
row("PC3a-L03-thm-number-3-10", "2.2 cross-references: no Theorem 3.10", "index.html; L01.html; L02.html; L03.html",
    "grep -c 'Theorem 3.10' on the four pages: 0 each. Example 3.10 is a named example (L03.html:320).")
row("PC3a-L03-adapted-undefined", "2.4 notation and terms: no undefined probabilistic term", "index.html; L01.html; L02.html; L03.html",
    "grep -c for martingale, stopping time, adapted, sigma-algebra and filtration: 0 on each of the four pages. The stopping rule "
    "is defined at Definition 3.7 by the history alone.")
row("PC3a-L03-each-rule-claim", "2.4/2.9 claim: each of the five rules is a stopping rule of Definition 3.7",
    "L03.html:321, 552; tests/labs/PC3/lab-PC3-L03-1.py RULES tuple",
    "Each rule uses only the history: h[-1] for the first win and loss, sum(h) for the totals (lab RULES, twin-L03-1.stdout). "
    "stopping_expectation forces a stop at HORIZON = 6, so each rule stops at length N (Definition 3.7).")
row("PC3a-L03-grades-lab-only", "2.3 grades: T for proved results, C for lab-printed results", "L03.html:468-475",
    "Rows 468, 469, 473 and 475 are T (Proposition 3.2, Theorem 3.8 with A2 over N = 6, Example 3.3). Rows 471, 472 and 474 are C "
    "and name Lab 1 Parts 2, 3 and 3b (L03.html:471-474); the printed values match outputs/twin-L03-1.stdout.")
row("PC3a-L03-any-game-fee", "2.2 numbers: R2 reroll-game gain and fee formula", "L03.html:448-450",
    "numbers_r12.out: (sum_f max(100f, 350 - c))/6 - 350 gives 100/3 at c = 100 and 149/2 = 74.5 at c = 1, as printed on the page.")
row("PC3a-L03-lab-docstring-two-methods", "2.5 labs: docstring claims match code", "tests/labs/PC3/lab-PC3-L03-1.py docstring and functions; L03.html:114",
    "Docstring lines 121-124: Part 2 by backward induction (backward_induction) and by enumerating every policy "
    "(policy_value over product((0, 1), repeat=6)); Part 3 by two methods (stopping_expectation and stopping_by_sequences); "
    "Part 3b by the recursion alone (only stopping_expectation is called). Matches.")
row("PC3a-L03-why-rhetorical-questions", "2.9 prose: why-it-matters paragraphs (no rhetorical question; length by word count)",
    "L01.html:51; L02.html:51; L03.html:51",
    "The why-it-matters paragraphs contain no question mark. Word counts (split on whitespace after tag removal): L01 119, L02 117, L03 120; each within 120.")
row("PC3a-L03-numbers-prose-claims", "2.2 prose numbers: 6 x 25, mean 350, 1150/3 - 350", "L03.html:104, 322, 336, 349",
    "6 x 25 = 150; mean 350 = 100 x 7/2; 1150/3 - 350 = 100/3 = 33.33 (numbers_r12.out). All match.")
row("PC3a-L03-quiz", "2.9 structure: retrieval quiz", "L03.html:480-564 (12 items)",
    "12 items at L03.html:485, 494, 499, 508, 513, 522, 527, 532, 541, 546, 551, 560, each with an explanation; M2 item p = 1/3 "
    "(numbers_r12.out); reroll items (522-538) match Example 3.6 and P3.")
row("PC3a-L03-lab-match", "2.5 labs: page code equals twin; expected block equals twin output", "L03.html:112-287; tests/labs/PC3/lab-PC3-L03-1.py",
    "run_labs PASS (outputs/run_labs_L03.out). Page code equals the twin after the trailing newline. pre.expected (L03.html:256, "
    "data-tolerance 0) equals twin-L03-1.stdout line for line (30 lines).")
row("PC3a-L03-canon-breaks", "2.9 prose: canon-breaks bullets", "L03.html:330-337",
    "Unbounded stopping: Theorem 3.8 needs finite N (L03.html:307-311). Fairness hypothesis: Example 3.10 (biased values nonzero, "
    "numbers_r12.out). Choice has value in a game that is not fair: reroll game mean 350 and gain 100/3 (numbers_r12.out).")
row("PC3a-L03-fair-game-before-definition", "2.5/2.9 terms before definition: Definitions 3.5 and 3.7 precede the lab",
    "L03.html:51, 83, 91-92, 108-110, 112",
    "'fair game' is first defined at L03.html:92 (plain dfn). Earlier 'fair' is the adjective in 'fair die' (L03.html:80, 102). "
    "The section heading 'Expected-value games and fairness' (L03.html:83) is a title that precedes the definition; see notes. "
    "The why-it-matters line (L03.html:51) names a zero-expectation game without the term.")
row("PC3a-why-terms-before-definition", "2.9 terms used before definition", "L01.html:51-58; L02.html:38, 51; L03.html:51, 91-92",
    "L01 'log-error width' first appears in the title of Proposition 1.3 (L01.html:85) and is defined in its conclusion "
    "(L01.html:89), a title-only use; L02 'Introduces' names concepts defined later on the page (conventional meta line); "
    "L03 'stopping rule' appears in why-it-matters (L03.html:51) and is defined at Definition 3.7 (L03.html:108).")
row("PC3a-L03-numbers-key-rows-lab", "2.3 grades: key-results rows 471, 474, 475", "L03.html:471, 474, 475",
    "Row 471 (best of 64 policies = 1150/3) is C with Lab 1 Part 2; row 474 (play-all 150; stopping values 1575/32, 575/8, 625/8) "
    "is C with Lab 1 Part 3b; row 475 (E[X+Y] = 7) is T with Lab 1 Part 1. All values in numbers_r12.out.")
row("PC3a-notation", "2.4 notation: registered symbols and macros", "index.html; L01.html; L02.html; L03.html; notation/notation.json",
    "Macros used in the four pages (TeX control-word count): \\Prob 143, \\E 32, \\R 2, \\indic 2, plus standard LaTeX. Each is in "
    "notation.json 'macros'. No registered symbol (T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q}) appears. "
    "Local symbols N (horizon, L03.html:109), t, h, W, V, p(omega), C_i are defined where used and not registered.")
row("PC3a-dag-prose-only-terms", "2.9 DAG: concepts outside the closure appear only as prose", "index.html:148; L01 misconception; L02.html:56-57; L03.html:57",
    "'adverse selection' appears in plain words at index.html:148 with no link and no dfn. 'finite probability space' (L02.html:56-57, "
    "L03.html:57) quotes the M4 Lesson 1 phrase; the M6 concept probability-space is not linked or defined (curriculum concepts: owner M6). "
    "Bayes' rule (L02.html:76) is plain prose. grep over the four pages: no martingale, stopping time, Poisson, Kelly, CAPM, duration, DCF.")
row("PC3a-canon-misconceptions-problems-counts", "2.9 structure: misconception and problem counts",
    "L01.html:326-449; L02.html:376-493; L03.html:343-459",
    "Misconceptions: three each (L01 327, 331, 335; L02 377, 381, 385; L03 344, 348, 352). Problems: L01 13, L02 12, L03 12 "
    "solution blocks, each tier at least three (L02 and L03 Empirical 3 each; L01 Empirical 4).")
row("PC3a-hours-declared", "2.9 structure: lesson hours declared", "L01.html:2, 34; L02.html:2, 34; L03.html:2, 34",
    "'6 study hours' on each page (line 34) and data-hours=\"6\" (grep).")
row("PC3a-r4-delta-read", "2.9 change read: every hunk since the previous pin",
    f"git diff {PREV[:8]} {PIN[:8]} for index.html, L01-L03, the three twins; hub-claim hunks elsewhere",
    f"git diff --stat {PREV[:8]} {PIN[:8]} -- index.html L01.html L02.html L03.html tests/labs/PC3/lab-PC3-L01-1.py L02-1.py L03-1.py: "
    "no change (0 lines). Hunks read in the rest of the unit (for the hub's claims): L04.html, L05.html, L06.html, project.html, "
    "grader/test_project.py, cards.json, tests/labs L04/L06, plans/PC3-build-plan.md, curriculum yaml and json (one brief line "
    "at 02-economics yaml:428), references.json (generated_at, used_by for BK4/LX1 only). None touches a slice sentence.")
row("PC3a-r4-cross-references", "2.9 cross-references resolve", "index.html; L01.html:82, 107, 332, 546; L02.html:458; L03.html:316, 345",
    "L01.html:82 and 332 'Section 4' = 'Where the canon breaks' (L01.html:314). L01.html:546 'Section 2' = 'Which factor to refine' "
    "(L01.html:103). L02.html:458 'Section 3' = the 'Where the canon breaks' section (L02.html:363). L03.html:316 'Section 4' "
    "= 'Where the canon breaks' (L03.html:331). Research problem R1 (L03.html:440) is the look-ahead rule.")
row("PC3a-r4-recompute-all-numbers", "2.2 numbers: every number in the slice recomputed by script",
    f"{N}; {G}/numbers_r12.out",
    "numbers_r12.py recomputes every prose number in index, L01, L02 and L03 by exact Fraction or math.log (full output "
    "numbers_r12.out). No mismatch with the page. The round-9 display value 0.308477 (L01.html:408) recomputes.")
row("PC3a-r4-restated-M4-concepts", "2.5 DAG: M4 concepts referenced by link, not redefined", "L02.html:57, 67; L03.html:62",
    "The M4 concepts (independence, conditional-expectation-elementary, expectation) are linked to concepts.html and are not "
    "defined in PC3 (no data-concept dfn for them in the slice pages). L02.html:57 cites M4 L01 (verified at M4 L01.html:55); "
    "L03.html:62 says Definition 3.1 is the M4 expectation on a finite space.")
row("PC3a-r4-observations-no-row", "2.4 observations (no defect)", "L01.html:433",
    "Observation only: the R1 criterion's part (c) is answered by dominance (L01.html:433). No defect recorded; see notes.")
row("PC3a-L03-misconception-most-likely", "2.2 misconception: wrong belief and correction", "L03.html:352-353",
    "'A fair game with expected payoff zero never pays a gain' is corrected by Example 3.11 (L03.html:327): +100 cents with "
    "probability 1/2. Correct.")
row("PC3a-L03-def35-next-turn", "2.4 definitions: fairness at histories of fewer than N turns", "L03.html:92 (Definition 3.5), 293 (A3), 300 (H2)",
    "Definition 3.5 quantifies over histories of fewer than N turns with positive probability, as A3 (L03.html:293) and H2 "
    "(L03.html:300) do. Consistent.")
row("PC3a-banned-and-process-words", "2.9 banned phrases and process words (learner text)", "L01.html, L02.html, L03.html, index.html",
    "check_pages PASS (banned strings). Whole-word scan (ledgers/PC3/scripts/PC3-a-r12/text_scans_r12.sh -> outputs/text_scans_r12.out): zero hits for build, "
    "builder, round, verifier, REQUESTS, unit report, fixer, TODO, TBD, lorem, studies show, experts agree, obviously, clearly, "
    "well known, for brevity, left as an exercise, beyond the scope, details omitted, it is important to note, you can add more. "
    "The substring 'rounded' occurs once (L03.html:286, arithmetic sense: 'the rounded display of 1150/3'); the list bans the "
    "process word, and that is recorded in notes, not as a FAIL.")
row("PC3a-r6-hub-ladder-rung2-wording", "2.9 consistency: hub describes rung 2 as the project does",
    "index.html:159; course/modules/PC/PC3/project.html:45, 53, 349-350",
    "project.html rung 2 (line 45): the two lines that give the cash flow and the mark are left blank; project.html:349-350 "
    "'cash_flow = ___' and 'mark = ___'. index.html:159 says the same (cash-flow line and mark line, each replaced by ___).")
row("PC3a-r6-hub-project-file-names", "2.9 consistency: hub and project name the same student files",
    "index.html:160, 167; course/modules/PC/PC3/project.html:46, 393, 429",
    "project.html:393 defines market_maker.py with quote(state) and replay(log); project.html:429 names the quoting rule and replay "
    "in market_maker.py; index.html:160 and 167 name the same file and functions.")
row("PC3a-r6-hours-curriculum-attribution", "2.9 prose: attribution of the 14-hour project figure", "index.html:167",
    "index.html:167 '50 hours: 36 hours of lessons and 14 hours of project' matches the curriculum hours (50) and project.html:434 "
    "'Total 14'.")
row("PC3a-r6-def21-m4-weights-positivity", "2.4 attribution: the definition cited to M4 Lesson 1", "L02.html:57 (Definition 2.1); L03.html:57 (A1)",
    "course/modules/M/M4/L01.html:55: finite probability space, p(omega) > 0 summing to 1. Both cite it correctly.")
row("PC3a-r7-hub-skill-check-bid-ask", "2.9 prose and arithmetic: skill-check convention for a maker's fill", "index.html:129, 131",
    "index.html:131: a maker that buys pays its bid, so the cash flow is -10005 (data-answer -10005). Consistent with "
    "plans/PC3-build-plan.md §3 (L04 rule: a maker that buys pays its bid; the L04 page is outside this slice).")
row("PC3a-r7-hub-hours-line-items", "2.6 hours: the project's line items against the project time budget", "index.html:167; project.html:421-435",
    "project.html:425-434: 1, 1, 3, 2, 2, 4, 1 hours; total 14. index.html:167 gives the same seven figures and the sum 14.")
row("PC3a-r7-hub-autograder-seeds", "2.9 prose: what the autograder runs", "index.html:55 (objective 7), index.html:160; course/modules/PC/PC3/grader/test_project.py:10",
    "test_project.py:10: 'fixed seeds 0 to 49, on the learner's seed SEED and on seed SEED + 7919' (read at the pin). index.html:160 "
    "says seeds 0 to 49, the workspace seed and that seed plus 7919.")
row("PC3a-r7-L02-timed-drill-budget", "2.9 structure: the curriculum lab's timed element and the Architect-default budget",
    "L02.html:132-134 (lab hypothesis), 359 (interpretation)",
    "L02.html:134: 'stated here as 60 seconds per item, with no timer on this page'; L02.html:359: the lab 'does not time anyone'. "
    "The architect default (no JavaScript timer) is followed.")
row("PC3a-r10-E2-fix-verified", "2.2 numbers: round-9 FAIL row re-derived after the fix", "L01.html:408",
    "Same subject as PC3a-L01-E2-shares: 0.308477, 30.8477 percent, 30.85, 30.8 and 0.308472 all recomputed in numbers_r12.out.")
row("PC3a-r10-L02-rename-consistency", "2.4 notation and proof: the C_i rename is consistent in Proposition 2.5, P2, P3 and the quiz",
    "L02.html:91-99, 428-440, 574-580",
    "grep -c 'A_i', 'A_1', 'A_2', 'A_3' on L02.html: 0. C_i, C_1, C_2 appear 42 times in the statements, proofs and quiz "
    "(grep -o).")
row("PC3a-r10-L03-R2-fee-formula", "2.2 numbers: L03 R2 fee formula and its two values", "L03.html:450",
    f"{N}: (sum_f max(100f, 350 - c))/6 - 350 evaluated exactly: c = 100 gives 100/3; c = 1 gives 149/2 = 74.5.")
row("PC3a-r10-L03-example-3-10-A3", "2.4 definitions: A3 is stated before Example 3.10 uses it", "L03.html:292-293 (A3), 321 (use)",
    "A3 is Assumption at L03.html:292. Example 3.10 at L03.html:321 uses 'the fairness condition of A3 with N = 6'. Defined before use.")
row("PC3a-r10-scope-words", "2.9 / verifier rule 4: scope words backed by a computation or a stated hypothesis",
    "ledgers/PC3/scripts/PC3-a-r12/outputs/view-index-r12.txt, view-L01-r12.txt, view-L02-r12.txt, view-L03-r12.txt (read in full, made by strip.py); L01.html:55, 82, 317-319; L02.html:116, 122-124, 369; L03.html:286, 334-336, 345",
    "Every 'every', 'all', 'always', 'only', 'any', 'same', 'exactly' sentence was read in context. Universal claims: Theorem 1.2 "
    "(every combination), Theorem 3.8 (every stopping rule over a finite horizon), 'Under rule A the host always opens a goat "
    "door' (a model rule), the 125-point grid and the six (n, x) pairs are stated as finite checks (L01.html:310), and 'the "
    "same doors give 2/3 and 1/2' is the enumerated pair of rules.")
row("PC3a-r10-process-and-dag-terms", "2.9 process words and D-terms (plan section 4, D1-D9) in learner text",
    "L01.html; L02.html; L03.html; index.html",
    "Process-word scan: zero hits (see PC3a-banned-and-process-words). D-term scan: 'Bayes' rule' (plain, D1), 'adverse selection' "
    "(plain, D3, index.html:148), 'combination' (English), 'probability space' (M4 phrase), 'roll' (verb). No martingale, "
    "stopping-time, Kelly, Poisson, MDP, CAPM, duration or DCF term.")
row("PC3a-r10-twins-unchanged", "2.5 labs: twins byte-identical since the previous pin (carry check)",
    "tests/labs/PC3/lab-PC3-L01-1.py, lab-PC3-L02-1.py, lab-PC3-L03-1.py",
    f"git diff --stat {PREV[:8]} {PIN[:8]} -- tests/labs/PC3/lab-PC3-L01-1.py L02-1.py L03-1.py: empty. md5sum of the current "
    "twins: 61325160af1e2f377d2708c38d53bdce (L01), 669a943df35c27ef3dae06f8b0b059b3 (L02), c196e3ad85bbd2dfd67e742a49fd964e "
    "(L03), identical to the round-10 md5_twins.out.")
row("PC3a-r10-hub-claims-outside-slice", "2.9 hub claims about pages outside the slice (read only to check the hub's claims)",
    "index.html:33-37, 143-150, 160-161, 167, 172; L04.html; L05.html; L06.html; project.html; grader/test_project.py",
    "index.html:64 lists the CS2 concepts used in L05 (big-o-complexity, hash-map, binary-heap, monotonic-deque); index.html:65-67 "
    "lists the FC2, CF1 and AC1 concepts used in L06 (cost-of-carry-forward-price, put-call-parity, net-present-value, "
    "statement-articulation); these are the concepts the pages link (index.html data-concept list). L05 Remark 3.4 changed in "
    "the delta (step cost, still a per-step bound statement). L04 M3 and E2 changed (not hub claims). L06 hunks (why-it-matters, Proposition 2.1 title, Example 4.2, a misconception) "
    "read; none touches a hub claim. project.html rung and hours claims as in PC3a-r7 rows. test_project.py:10 seeds as in PC3a-r7.")


SCAN = "[scan: ledgers/PC3/scripts/PC3-a-r12/text_scans_r12.sh -> outputs/text_scans_r12.out]"
for r_ in R:
    if r_["id"] in {"PC3a-hub-data", "PC3a-L03-thm-number-3-10", "PC3a-L03-adapted-undefined", "PC3a-hub-P0.1-claim",
                    "PC3a-dag-prose-only-terms", "PC3a-notation", "PC3a-r10-process-and-dag-terms", "PC3a-r10-scope-words",
                    "PC3a-r10-twins-unchanged", "PC3a-L03-why-rhetorical-questions", "PC3a-L02-where-canon-breaks"}:
        r_["evidence"] += " " + SCAN


def build():
    now = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat()
    ids = [r["id"] for r in R]
    assert len(ids) == len(set(ids)), "duplicate row ids"
    fragment = {
        "unit": "PC3",
        "slice": "PC3-a",
        "round": 12,
        "verifier": "Claude Haiku 5.5, independent verifier PC3 slice a, round 12 (did not build PC3; no shared context with the builders)",
        "pin": PIN,
        "base": PREV + " (the round-10 pin; delta read for the slice files: none; out-of-slice hunks read for hub claims)",
        "checkout": "/Users/billyribeiro/.fanout/wt/verifyE12-PC3-a (detached at the pin; .venv symlinked)",
        "scratch": "/Users/billyribeiro/.fanout/scratch-PC3a-r12 (strip.py, text views); twin runs in fresh mktemp /tmp directories",
        "verified_at": now,
        "verdict": "PASS" if all(r["status"] == "PASS" for r in R) else "FAIL",
        "scope": "course/modules/PC/PC3/index.html, L01.html, L02.html, L03.html and tests/labs/PC3/lab-PC3-L01-1.py, L02-1.py, L03-1.py. Not in this slice: L04-L06, project.html, grader/, cards.json, the project labs (read only to check hub claims).",
        "rows": R,
        "mutants": [],
        "registry_flags": [
            "crack2015heard (references/references.json:6223): publisher string '[Timothy Falcon Crack]' carries brackets; the curriculum string says '16th ed.' and the record has no edition (plan B4). Registry owner should correct the publisher string; not edited here.",
            "zhou2008practical (references/references.json:23402 block): publisher 'Lulu,]' has a stray bracket (plan B4). Not edited here.",
        ],
        "freshness_flags": [
            "No 2025-2026 work is cited in the slice. PC3 cites two books at book level only (zhou2008practical, crack2015heard) and no passage. Nothing for a debate brief (PC3 has no debate key).",
        ],
        "notes": [
            "Mutation testing is not applicable to this slice: it has no grader (ruling: lab twins are demonstrations). mutants is empty.",
            "The fragment named in the brief as the round-11 previous fragment (/Users/billyribeiro/.fanout/frags/E-PC3-a.round11.json) does not exist; the latest slice-a fragment is E-PC3-a.round10.json (pin 00a84795). This round used round 10 only as context.",
            "Delta: between 00a84795 and 5db69a9 no byte of index.html, L01.html, L02.html, L03.html or the three slice twins changed. Every row is re-verified from scratch in this round; no row is carried.",
            "Architect note (not verdict-changing): the L02 'Introduces:' meta line lists conditional probability, Bayes' rule and the law of total probability. The lesson template fills that line with plain names (other modules do the same, e.g. AC1 L01 'double-entry bookkeeping'), and the plan's 'L02 introduces no curriculum concept' is respected: no data-concept dfn is in L02.",
            "Architect note (not verdict-changing): the curriculum lab wording 'with spaced repetition' (curriculum yaml:174) is served by the cards (L02.html:134, review.html:7, 35); the page says the drill set has no spacing of its own.",
            "Heading note: the L03 section heading 'Expected-value games and fairness' (L03.html:83) and the L01 title 'log-error widths add' (L01.html:85) name a term before its definition in the body; these are titles, and the definitions follow at L03.html:91-92 and L01.html:89.",
            "R1 (L01.html:433) answers criterion part (c) by dominance: a factor whose width exceeds half the total can remove more than all others together. Recorded as an observation; a PASS.",
            "Observation (not a FAIL): the process-word list (fixer-rule 14) bans the word 'round'; L03.html:286 uses the arithmetic word 'rounded' once. It is not a verification round or a build word, so it is not counted.",
            "Not checked in this slice: cards.json (its L01-L03 cards were not scanned against the lesson text in this round); L04-L06, project.html, grader/, cards and the project labs (outside the slice; read only where the hub claims them); the live Crossref path for the book keys (openlibrary-verified records, live run exit 0 only); fetch_data --check (no data in PC3); run_graders and mutate_graders (no grader in slice a).",
        ],
        "summary": {
            "rows": len(R),
            "pass": sum(1 for r in R if r["status"] == "PASS"),
            "fail": sum(1 for r in R if r["status"] == "FAIL"),
            "unverifiable": sum(1 for r in R if r["status"] == "UNVERIFIABLE"),
            "mutants_killed": 0,
            "mutants_total": 0,
        },
    }
    return fragment


if __name__ == "__main__":
    frag = build()
    out = sys.argv[1] if len(sys.argv) > 1 else "ledgers/PC3/PC3-a.json"
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(frag, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    print(json.dumps(frag["summary"]), frag["verdict"])
