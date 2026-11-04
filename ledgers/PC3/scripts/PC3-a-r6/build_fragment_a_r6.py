"""Round-6 fragment builder for PC3 slice a. Writes ledgers/PC3/PC3-a.json from the rows below (evidence strings cite the
scripts and outputs under ledgers/PC3/scripts/PC3-a-r6/). Run from the checkout root: .venv/bin/python -I <this file>.
"""

import datetime
import json
from pathlib import Path

R = "ledgers/PC3/scripts/PC3-a-r6/outputs/"
PAGES = "course/modules/PC/PC3/"

P = "PASS"
F = "FAIL"
rows: list[dict[str, str]] = []


def row(rid: str, check: str, location: str, status: str, evidence: str, fix: str = "") -> None:
    item = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != P:
        item["fix"] = fix
    rows.append(item)


# ---- 2.6/2.5 gates (all re-run this round on the pin) ----
row("PC3a-check-pages", "2.9 structure: check_pages", "index.html, L01.html, L02.html, L03.html", P,
    R + "gates.out (script ledgers/PC3/scripts/PC3-a-r6/run_gates_a_r6.sh): 'check_pages PC3: PASS' (exit 0, includes check_hub for the hub); "
    "'check_pages PC3 L01/L02/L03: PASS' (exit 0 each).")
row("PC3a-check-dag", "2.9 DAG: check_dag", "index.html; L01.html; L02.html; L03.html", P,
    R + "gates.out: 'check_dag PC3: PASS' exit 0. Independent: ledgers/PC3/scripts/PC3-a-r6/links_and_ids_a_r6.py -> "
    + R + "links_and_ids_a_r6.out: PROBLEMS 0 (every href resolves, every fragment exists, every data-concept is a concepts.html id, no duplicate ids); "
    "'protected P0.1 links: []'.")
row("PC3a-check-projects", "2.6 projects: check_projects (outside slice; tool result only)", "course/modules/PC/PC3/project.html", P,
    R + "gates.out: 'check_projects PC3: PASS' exit 0. Project content is outside this slice and was not verified by this row.")
row("PC3a-run-labs", "2.5 labs: run_labs", "tests/labs/PC3/lab-PC3-L01-1.py, lab-PC3-L02-1.py, lab-PC3-L03-1.py; L01.html:144-310, L02.html:132-359, L03.html:112-287", P,
    R + "gates.out: 'run_labs PC3: PASS (9/9)' exit 0; per page 'run_labs PC3: PASS (1/1)' for --page L01, L02, L03 (exit 0 each).")
row("PC3a-twins-alone", "2.5 labs: each twin run alone under python -I -W error", "tests/labs/PC3/lab-PC3-L01-1.py, lab-PC3-L02-1.py, lab-PC3-L03-1.py", P,
    "Run by me: .venv/bin/python -I -W error <twin> exit 0 for L01, L02, L03. " + R + "embed_compare_a_r6.out (script ledgers/PC3/scripts/PC3-a-r6/embed_compare_a_r6.py): "
    "'L01 twin exit=0 stderr_bytes=0', 'L02 twin exit=0 stderr_bytes=0', 'L03 twin exit=0 stderr_bytes=0'.")
row("PC3a-pytest-labs", "2.5 labs: pytest on the lab cases", "tests/test_labs.py (PC3 cases)", P,
    R + "pytest_labs_pc3_r6.out: `pytest tests/test_labs.py -k PC3 -q` -> 9 dots (9 passed); `--collect-only -k PC3` -> 'tests/test_labs.py: 9'.")
row("PC3a-page-smoke", "2.9 page_smoke (run alone on the four slice pages)", "index.html, L01.html, L02.html, L03.html", P,
    R + "page_smoke_slice_r6.out: `page_smoke.py --unit PC3 --pages modules/PC/PC3/index.html ... L03.html` -> 'page_smoke PC3: PASS' exit 0 "
    "(light and dark, 360 px, zero console errors, zero external requests, no unrendered math). gates.out 'page_smoke --unit PC3: PASS' for every PC3 page.")
row("PC3a-ruff-mypy", "2.5 labs: ruff and mypy --no-incremental on the twins", "tests/labs/PC3/lab-PC3-L01-1.py, L02-1.py, L03-1.py", P,
    R + "gates.out: ruff check 'All checks passed!' exit 0; ruff format --check '3 files already formatted' exit 0; "
    "mypy --no-incremental 'Success: no issues found in 3 source files' exit 0.")
row("PC3a-verify-refs", "2.1 citations: verify_refs (offline integrity and live re-verification of the PC3 unit)", "references/references.json; index.html:177", P,
    R + "gates.out: 'offline integrity: 560 entries, 0 problems' exit 0. Live: " + R + "verify_refs_unit_PC3_r6.out: 'live re-verification of PC3: 2 of 560 entries, 0 problems' (exit 0). "
    "Keys zhou2008practical and crack2015heard exist with status verified and used_by PC3 (read from references/references.json).")

# ---- hub (index.html) ----
row("PC3a-hub-hours", "2.9 hours: split sums to the declared figure", "index.html:29, 42, 167; L01.html:2, L02.html:2, L03.html:2", P,
    "index.html:29 data-hours-lessons=\"36\", :42 '36 h lessons · 14 h project (28%)', :167 'The lines sum to 2 + 6 + 4 + 2 = 14'. Each lesson data-hours=\"6\". "
    "Recomputed by ledgers/PC3/scripts/PC3-a-r6/recompute_hub_r6.py -> " + R + "recompute_hub_r6.out (18 of 18): 6 x 6 = 36, 36 + 14 = 50 = curriculum PC3 hours 50 (curriculum/curriculum.json, PC3 entry), 14/50 = 28 percent. "
    "The attribution of the 14 h to the curriculum is a separate row (PC3a-r6-hours-curriculum-attribution).")
row("PC3a-hub-placement", "2.4 numbers and answers: placement diagnostic", "index.html:72-138 (ten items)", P,
    "Recomputed in recompute_hub_r6.py (" + R + "recompute_hub_r6.out): data-answer 3.5 (21/6), 0.25 (1/2 x 1/2), 2 (ln e^2), 3 (d/dx x^3 at 1), 90.909091 (100/1.1 within 1e-6), -10005, 10040; "
    "the 80 percent bar of ten items is eight correct; seven of ten is 70 percent. Option keys read from index.html:97-111, 119-127 (binary search O(log n); S e^{r tau}; balance sheet identity).")
row("PC3a-hub-titles-prereqs", "2.9 structure: hub titles and prerequisite closure", "index.html:35, 61-67", P,
    "curriculum/curriculum.json PC3 entry: title 'Quant & Finance Interviews', prereqs [M4, CS2, FC2], hours 50; M4 'Probability', CS2 'Algorithms & Data Structures', FC2 'Derivatives Fundamentals' (curriculum.json, read this round). "
    "tools/coursekit.py prerequisite_closure('PC3') (run this round) = {AC1, CF1, CS1, CS2, E1, FC1, FC2, M1, M2, M4, P0.1}, the same set the hub lists at index.html:35.")
row("PC3a-hub-objectives", "2.9 prose: objectives match the lessons", "index.html:48-56", P,
    "Seven objectives (Bound, Compute, Compute, Derive, Implement, Compute, Write). Objective 3 (line 51) matches Theorem 3.8 with A3 (L03.html:296-311); objective 1 matches Theorem 1.2 and Proposition 1.3 (L01.html:67-90); objective 2 matches Propositions 2.4 and 2.5 (L02.html:75-100).")
row("PC3a-hub-lesson-map", "2.9 structure: lesson map cards", "index.html:145-147; L01.html:35, L02.html:35, L03.html:35", P,
    "Card titles 'Fermi Estimation and Mental Math', 'Probability Puzzles and Conditional Reasoning', 'Expected-Value Games' equal the h1 of L01, L02, L03. Kickers 'L0n · 6 h' equal data-hours=6 on each page.")
row("PC3a-hub-data", "2.8 data: no dataset, no data-files", "index.html:37, 170-173; tests/labs/PC3/lab-PC3-L01-1.py, L02-1.py, L03-1.py", P,
    R + "scans_a_r6.out: 'data-cite'/'data-files' absent and no http(s) reference on the four pages; grep of the three twins for open(, read_text, csv, json., urllib, requests, http: 0 matches each.")
row("PC3a-hub-P0.1-claim", "2.9 prose: P0.1 claims", "index.html:35, 74; course/concepts.html:34-47", P,
    "concepts.html P0.1 section (lines 34-47) lists 11 entries, each reading 'not yet released' (read this round). No href on the four pages points to P0.1 (links_and_ids_a_r6.out). The placement claim that none of the ten items tests P0.1 holds by reading index.html:72-138.")

# ---- L01 ----
row("PC3a-L01-numbers", "2.2 numbers in prose (a, b, c) and rounding", "L01.html:55, 99-100, 107, 137-141, 287-309, 328, 336, 401-415, 433, 447, 462-465", P,
    "ledgers/PC3/scripts/PC3-a-r6/recompute_L01_r6.py -> " + R + "recompute_L01_r6.out: 62 of 62 checks pass. Covers 12000, 234000, ratio 19.5, ln 19.5 = 2.9704144656, geometric midpoint 52990.5651979671 (page: 52 990.57), "
    "reductions 0.4054651081, 0.9162907319, 0.1753528875, totals 2.5649, 2.0541, 2.7951, remainder/bound at (1.01)^10: 1.1046221254, 0.0046221254, 0.0048728552, ratio 0.948545615 (0.9485 to four places; truncation 0.94854), "
    "bound excess 5.4 percent, miss at x=1/20: 0.1289, bound 0.1662, 7.9 percent, E3 16.5 and ln 16.5 = 2.8034, ln 19.5 - ln 16.5 = 0.167054, R1 half-width 1.4852, R3 0.4055 and 0.9063.")
row("PC3a-L01-proofs", "2.4 mathematics: proofs of Theorem 1.2, Proposition 1.3, Theorem 1.5, Remark 1.6", "L01.html:78-79, 92-94, 128-131, 134-135, 374-391", P,
    "Re-derived by hand this round: ab - a'b' = a(b - b') + b'(a - a') with both terms nonnegative under 0 < a' <= a, 0 < b' <= b (L01.html:78); the induction with the two lemma applications (79) uses L > 0 from the hypothesis; attainment (79). "
    "Proposition 1.3 (92-94) uses the product rearrangement and ln(ab) = ln a + ln b (M1). Theorem 1.5 (128-131) uses A2 for x > 0 with xi strictly between 0 and x, and gives 0 <= remainder <= n(n-1)/2 (1+xi)^(n-2) x^2 <= the stated bound, with x = 0 handled directly. Remark 1.6 (134-135) is correct for n = 2 (equality) and strict for n >= 3, x > 0. No gap.")
row("PC3a-L01-A2-false-at-x0", "2.4 mathematics: assumption used only where it holds", "L01.html:115 (A2), 123 (H3), 130 (x = 0 proof)", P,
    "A2 is stated for x != 0 (L01.html:115). H3 invokes A2 only for x > 0 (L01.html:123). The x = 0 case is proved directly at L01.html:130 (both sides 0).")
row("PC3a-L01-grades-lab-only", "2.3 grades: T for proved results, C for lab-printed results", "L01.html:458-465 (key results)", P,
    "Rows 458-462 graded T and each cites a proof on the page (Theorem 1.2, Proposition 1.3, Theorem 1.5 under A2, the hand product 12000 and 234000 of Example 1.4, ln 19.5 by Proposition 1.3). "
    "Rows 463-465 graded C and cite Lab 1 printed values (expected block L01.html:284-309). Grades match BLUEPRINT evidence rules as applied in the lesson.")
row("PC3a-L02-grade-drill-lab-only", "2.3 grades: lab-only result graded C", "L02.html:508", P,
    "L02.html:508 grades 'Generated drill set: the closed form equals the enumeration on 12 of 12 items' as C with basis 'Lab 1, Part 1 (seed 0, self-check)'; the expected block (L02.html:327-340) prints 'closed form equals enumeration on 12 of 12 items'.")
row("PC3a-L01-claims", "2.3/2.9 claims in prose checked against the proofs and the lab", "L01.html:67-90, 82, 105-107, 113-131, 133-141, 317-319, 328", P,
    "'Both bounds are attained' (73) matches the attainment argument (79). 'The total does not depend on the order' and 'lowers the total by exactly the drop' (105) follow from Proposition 1.3 additivity. "
    "'A factor whose own width is already small can lower the total by at most that small width' follows since a drop cannot exceed the factor's width. 'Theorem 1.2 holds for every combination' (317) matches its ranges-only proof. "
    "The Taylor claim is restricted to x >= 0 (319), matching H2 of Theorem 1.5. Remark 1.6 'the printed remainder is below the printed bound' for n=5 and n=10 holds in the expected block (lines 304-307: 0.0010100501 < 0.0010303010; 0.0262815625 < 0.0289406250; 0.0046221254 < 0.0048728552; 0.1288946268 < 0.1662137374).")
row("PC3a-L01-lab-match", "2.5 labs: page code equals twin, expected block equals twin output", "L01.html:144-310; tests/labs/PC3/lab-PC3-L01-1.py", P,
    R + "embed_compare_a_r6.out: 'L01: page code == twin: True (code 5775 chars, twin 5775 chars)'; 'L01: expected block == twin stdout: True (stdout lines 26, expected lines 25)'; tolerance attribute data-tolerance=\"1e-9\". "
    "Hypothesis (L01.html:146) names 12000, 234000, 19.5, 2.9704144656, 125 products, the Part 2 narrowings, Part 3 with n=2,5,10 and x=0.01,0.05, the 1e-9 tolerance and the 1e-12 float check (twin line 242 'abs(...) < 1e-12').")
row("PC3a-L01-problems-quiz", "2.9 structure: problem tiers, solutions and quiz", "L01.html:345-451 (13 problems), 473-548 (10 quiz items)", P,
    R + "scans_a_r6.out structure counts: L01 problems 13 (mechanics 3, proof 3, empirical 4, research 3), solutions 13, quiz 10. Keyed answers recomputed in recompute_L01_r6.py: 10 (Q1), ln 4 = 1.386294 (Q2), 234000 (Q4), remainder 0.004622 (Q6), 52990.5652 (Q9). "
    "Solutions M1-M3, P1-P3, E1-E4 and R1-R3 were re-derived this round (no arithmetic error found; E2 solution rewritten, see the E2 row below).")
row("PC3a-L01-only-scope", "2.9 scope: exceptions to 'only the ordinary order and arithmetic'", "L01.html:55, 82", P,
    "L01.html:55 lists the exceptions used (logarithm M1 in Proposition 1.3 and Example 1.4; derivatives and the Taylor theorem M2 in Section 3; the binomial theorem in Remark 1.6; the square root in Example 1.4). L01.html:82 points to Section 4, which exists (L01.html:314).")
row("PC3a-L01-twin-docstring-decimals", "2.5 labs: twin docstring matches the code and the page", "tests/labs/PC3/lab-PC3-L01-1.py:6-7; L01.html:146-154", P,
    "Twin lines 6-7: 'one float check ... uses a tolerance of 1e-12' and 'Decimal values print to ten places'. The code prints ratio, geometric midpoint, log-error widths and Taylor values with :.10f (twin Part 1 and Part 3 print statements) and the one float check is abs(...) < 1e-12 (twin line 242).")
row("PC3a-L01-research-problems", "2.4 mathematics: open problems R1-R3 answers", "L01.html:430-449", P,
    "R1: half of ln 19.5 = 1.4852; ln 5 = 1.6094 exceeds it; ln 3 = 1.0986 and ln 1.3 = 0.2624 do not (recompute_L01_r6.py). R2: the proof uses only (H1), (H2) (L01.html:70-71, 438-440). "
    "R3: ln(3/2) = 0.4055 for narrowing A; ln 2.5 = 0.9163 is B's width; ln(2.5/1.01) = 0.9063 > 0.4055, so the claim is false (recomputed).")
row("PC3a-L01-misconception-accuracy", "2.2/2.3 misconception: wrong belief and correction", "L01.html:327-328", P,
    "Round-5 FAIL is fixed. The correction states Proposition 1.3's drop is independent of the other factors while its share of the baseline total is not; the shares 5.9 and 30.8 percent and the drops 0.1754 and 0.9163 are recomputed (recompute_L01_r6.out) and printed by Lab 1 Part 2 (expected block lines 298-300).")
row("PC3a-L01-KR-ln19.5-grade", "2.3 grades: row 462 and 463 of L01 key results", "L01.html:461-463", P,
    "Row 462 'Log-error width ln 19.5 ... the sum of the three factor widths' graded T (Proposition 1.3 and Example 1.4, proof on this page). Row 463 'ln 19.5 = 2.9704144656, to ten places' graded C (printed by Lab 1, Part 1). Both values recomputed.")
row("PC3a-L01-E2-shares", "2.2 numbers: E2 solution (shares of the total width)", "L01.html:405-410", P,
    "Four-place division 0.9163 / 2.9704 = 0.308477..., whose four-place value 0.3085 is 30.85 percent to two places (so the page rounding to 30.9 is a display of 30.85); full precision 0.9162907319 / 2.9704144656 = 0.308472 -> 30.8 percent; minutes 0.1753528875 / 2.9704144656 = 0.059033 -> 5.9 percent (recompute_L01_r6.out). The page's statement about the four-place route is arithmetically correct.")

# ---- L02 ----
row("PC3a-L02-numbers", "2.2 numbers: examples, exercises and key rows", "L02.html:111-130, 398-417, 449-466, 489-493, 503-507", P,
    "ledgers/PC3/scripts/PC3-a-r6/recompute_L02_L03_r6.py -> " + R + "recompute_L02_L03_r6.out (64 checks across L02 and L03, 0 fails): the twelve drill items parsed from the L02 expected block (L02.html:327-340) recomputed by sequence enumeration, all equal; "
    "Monty Hall rule A 1/3, 2/3 and rule B 1/2, 1/2 by a separate weight table; urn 3/5, 3/5, 3/10 and 3/4; bag P(red) = 1/2 and P(bag 1 | red) = 3/4; M1 = 1/6; M2 = 15/29; E1 = 57/64.")
row("PC3a-L02-proofs", "2.4 mathematics: Propositions 2.4 and 2.5, and P1-P3", "L02.html:75-100, 423-446", P,
    "Re-derived: Bayes' rule (85) needs Prob(A), Prob(B) > 0 (H1) and divides by Prob(B) > 0; the total-probability proof (99) uses the disjoint union B = union of B and A_i (H1) and H2 for each term. P1-P3 solutions (L02.html:424-441) use only A1 and positivity; no gap found.")
row("PC3a-L02-lab-match", "2.5 labs: L02 page code equals twin; expected block equals twin output", "L02.html:132-360; tests/labs/PC3/lab-PC3-L02-1.py", P,
    R + "embed_compare_a_r6.out: 'L02: page code == twin: True (code 8171 chars, twin 8171 chars)'; 'L02: expected block == twin stdout: True (stdout lines 32, expected lines 31)'; data-tolerance=\"0\" (exact fractions).")
row("PC3a-L02-interp-reverse-conditional", "2.2 interpretation: reverse conditional", "L02.html:359", P,
    "L02.html:359 '1/3 against 1 for two flips' matches expected lines 350 (P(both heads | at least one head) = 1/3) and 352 (P(at least one head | both heads) = 1).")
row("PC3a-L02-misconceptions-quiz", "2.9 structure: misconceptions and quiz", "L02.html:376-388 (3 misconceptions), 517-587 (10 quiz items)", P,
    "Each misconception is tied to a worked example or printed lab line (Example 2.8, Example 2.6, Lab Part 4). Quiz keys recomputed: 1/3 (0.333333), 0.6, 3/10 (0.3), 1 and 0.75 and 2/3 and 1/2 (recompute_L02_L03_r6.out).")
row("PC3a-L02-where-canon-breaks", "2.9 prose: canon-breaks bullets", "L02.html:362-371", P,
    "Bullet 1: Example 2.8 gives 2/3 under rule A and 1/2 under rule B (recomputed). Bullet 2: Example 2.7 swap symmetry, and the blue-first conditional 3/4 (recomputed). Bullet 3: Example 2.6 gives 1/3 and 1/2 (recomputed).")
row("PC3a-L02-twin-bag-ball-label", "2.2 labels: twin and page use the same bag and colour wording", "L02.html:142, 267, 345; tests/labs/PC3/lab-PC3-L02-1.py", P,
    "grep -c 'bag, ball' = 0 in L02.html and in the twin (" + R + "scans_a_r6.out). The twin docstring and the page use '(bag, colour)'.")
row("PC3a-L02-finite-probability-space-redefined", "2.5 DAG and notation: the M4 term used by reference", "L02.html:57; course/modules/M/M4/L01.html:55", P,
    "M4 Lesson 1 defines 'a finite probability space' in prose at course/modules/M/M4/L01.html:55 (not a dfn). L02 gives no dfn for it (the L02 dfn list is 'equally likely outcomes' and 'Bayes' rule'). "
    "The concept probability-space is owned by M6 (curriculum.json concepts, read this round), is not linked and is not in the closure; the lesson uses the M4 term by reference to M4 Lesson 1. "
    "The weight-positivity wording is a separate FAIL row.")

# ---- L03 ----
row("PC3a-L03-numbers", "2.2 numbers: expectations, continuation values, fee sensitivity, biased-game values", "L03.html:80, 102-104, 322, 329-337, 340-356, 418-432, 441-450, 455-457", P,
    "recompute_L02_L03_r6.py (" + R + "recompute_L02_L03_r6.out): E[face] = 7/2, E[X+Y] = 7 over 36 outcomes, continuation 250, reroll value 1150/3, best of 64 policies 1150/3, gain 100/3, stop-always 350; "
    "R2 gains 100/3 at fee 100 and 74.5 at fee 1; biased-game expectations 150, 1575/32, 575/8, 625/8 by listing all 64 sequences; E2 change -575/8 = -71.875; R1 expectation 50; fair-game expectation 0 for all five rules.")
row("PC3a-L03-proofs", "2.4 mathematics: Proposition 3.2, Theorem 3.8 and proof, Definition 3.7", "L03.html:66-76, 107-110, 296-311", P,
    "Re-derived: linearity (75) uses the finite sum rearrangement. Definition 3.7 (108-110) defines W(h) for every history of length t <= N and the rule stops at length N. Theorem 3.8 (296-311): base t = N by (H3) and Definition 3.7; step uses the induction hypothesis V(h,x) = W(h) + x and (H2) to kill sum x P(x|h); histories of probability zero are excluded. No gap.")
row("PC3a-L03-A3-zero-probability-histories", "2.4 mathematics: A3 and H2 quantify positive-probability histories only", "L03.html:292-293 (A3), 300 (H2), 308", P,
    "A3 quantifies histories with Prob(h) > 0 and fewer than N turns (L03.html:293). H2 (300) is stated for positive-probability histories. The proof (308) excludes zero-probability histories and says why.")
row("PC3a-L03-thm-number-3-10", "2.2 cross-references: no Theorem 3.10", "index.html; L01.html; L02.html; L03.html", P,
    R + "scans_a_r6.out: 'Theorem 3.10' count 0 on all four pages. Theorem references in L03 (296, 316, 322) point to Theorem 3.8 (296) and Remark 3.9 (314) and Example 3.10 (320), which exist.")
row("PC3a-L03-adapted-undefined", "2.4 notation/terms: no undefined probabilistic term", "index.html; L01.html; L02.html; L03.html", P,
    R + "scans_a_r6.out: 'adapted', 'martingale', 'optional stopping' counts are 0 on the four pages (D2 terms kept out of the prose).")
row("PC3a-L03-each-rule-claim", "2.4/2.9 claim: each of five rules is a stopping rule of Definition 3.7", "L03.html:321, 552; tests/labs/PC3/lab-PC3-L03-1.py RULES tuple", P,
    "The five rules (twin RULES tuple, lines 223-229) are functions of the history alone (H3); the recursion stops at len(history) == HORIZON (twin stopping_expectation), so each stops at N as Definition 3.7 requires.")
row("PC3a-L03-grades-lab-only", "2.3 grades: T for proved results, C for lab-printed results", "L03.html:468-475", P,
    "T rows: linearity (Prop 3.2), Theorem 3.8 for the five rules over six turns (A2 with N = 6), reroll values (Example 3.6 by hand), two dice E[X+Y] = 7 (Example 3.3 and Prop 3.2). C rows: best of 64 policies, Part 3 zeros, biased-game values; each matches the expected block (L03.html:256-285).")
row("PC3a-L03-any-game-fee", "2.2 numbers: R2 reroll-game gain and fee formula", "L03.html:448-450", P,
    "Optimal 1150/3 and stop-at-once 350 give gain 100/3 > 10 (recomputed). The fee formula sum max(100f, 350 - c)/6 - 350 gives 100/3 at c = 100 and 74.5 at c = 1 (recompute_L02_L03_r6.out). The game is not fair because its stop payoff has mean 350 (450).")
row("PC3a-L03-lab-docstring-two-methods", "2.5 labs: docstring claims match code", "tests/labs/PC3/lab-PC3-L03-1.py docstring and functions; L03.html:114", P,
    "Docstring: Part 3 'by two methods that must agree' (stopping_expectation and stopping_by_sequences are the two methods); Part 3b 'by the recursion alone' (Part 3b calls only stopping_expectation).")
row("PC3a-L03-why-rhetorical-questions", "2.9 prose: no rhetorical question in why-it-matters; length", "L01.html:51; L02.html:51; L03.html:51", P,
    R + "scans_a_r6.out: '?' count 0 in each why-it-matters paragraph. Naive word counts (tags stripped): L01 119, L02 117, L03 120 (limit 120).")
row("PC3a-L03-numbers-prose-claims", "2.2 prose numbers: '6 times 25', 'mean 350', '1150/3 - 350'", "L03.html:322, 336, 349, 104", P,
    "6 x 25 = 150 (per-turn 25 = 1/2 x 150 + 1/2 x (-100)), stop-payoff mean 350 (not zero), 1150/3 - 350 = 100/3 = 33.33 (recompute_L02_L03_r6.out).")
row("PC3a-L03-quiz", "2.9 structure: retrieval quiz", "L03.html:479-564 (12 items)", P,
    R + "scans_a_r6.out: 12 quiz items. Keyed answers recomputed: 350, 1/3 (0.333333), 383.333333, 250, 50, 150, 7; explanations point to Example 3.3, Problem M2, Example 3.6, Problem R1, Example 3.10 and match the lesson text.")
row("PC3a-L03-lab-match", "2.5 labs: page code equals twin; expected block equals twin output", "L03.html:112-287; tests/labs/PC3/lab-PC3-L03-1.py", P,
    R + "embed_compare_a_r6.out: 'L03: page code == twin: True (code 6052 chars, twin 6052 chars)'; 'L03: expected block == twin stdout: True (stdout lines 30, expected lines 29)'; data-tolerance=\"0\".")
row("PC3a-L03-canon-breaks", "2.9 prose: three canon-breaks bullets", "L03.html:330-337", P,
    "Unbounded stopping: Theorem 3.8 needs finite N. Fairness: Example 3.10 values for the biased game (1575/32, 575/8, 625/8, recomputed) against zero for the fair game. Choice in an unfair game: 100/3 gain over stopping at once with stop mean 350 (recomputed).")
row("PC3a-L03-fair-game-before-definition", "2.5/2.9 terms before definition: Definition 3.5 and 3.7 precede the lab", "L03.html:90-93, 107-110, 112 (lab)", P,
    "Definition 3.5 (fair game, dfn 'fair' and 'history') at L03.html:90-93 and Definition 3.7 (stopping rule, dfn) at 107-110 both precede Lab 1 at 112. First body occurrence of 'fair game' is the Definition 3.5 heading (line 91); 'stopping rule' first appears at Definition 3.7 (line 108). 'fair die' (line 80) is the ordinary adjective.")
row("PC3a-why-terms-before-definition", "2.9 terms before definition in the why-it-matters and first uses", "L01.html:51-58; L02.html:38, 51; L03.html:51, 91-92", P,
    "L01: first body use of 'Fermi estimate' is the Section 1 heading (53), the definition is at 59; 'log-error width' first appears in Proposition 1.3 (dfn there). L02: 'conditional probability' and 'Bayes' rule' are listed in the Introduces header (38), defined at 67 and 80. L03: no defined term in why-it-matters (51).")
row("PC3a-L03-numbers-key-rows-lab", "2.3 grades: key rows 471, 474, 475", "L03.html:471, 474, 475", P,
    "Row 471 (best of 64 policies) graded C, matching Lab 1 Part 2 only. Row 474 (biased game) graded C, matching Part 3b. Row 475 (E[X+Y] = 7) graded T with Example 3.3 and Proposition 3.2 on the page, and Lab 1 Part 1 as a check.")
row("PC3a-notation", "2.4 notation: registered symbols and macros", "index.html; L01.html; L02.html; L03.html; notation/notation.json", P,
    "notation.json symbols are T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q}. None appears in the slice (scans_a_r6.out macro list). Macros used (\\Prob, \\E, \\R, \\indic) are registered. "
    "Local symbols (N in L03 Definition 3.7; L, U, P, xi and l_i, u_i in L01's proof; tau and S in the index's placement item) are defined where used. F^\\ast (index.html:106-112, forward price) is not the registered R^\\ast.")
row("PC3a-dag-prose-only-terms", "2.9 DAG: prose-only terms (D1-D9) appear without links", "index.html:148 (L04 card); L01-L03 prose", P,
    R + "scans_a_r6.out D-term scan: 'adverse selection' appears only in the L04 card (index.html:148), plain prose, no link, no dfn (plan D3). No martingale, stopping time, Markov, Poisson, Kelly, CAPM, DCF, duration or Bayesian inference term appears in L01-L03. 'probability space' appears only as M4's phrase (see the L02 DAG row).")
row("PC3a-canon-misconceptions-problems-counts", "2.9 structure: misconception and problem counts", "L01.html:326-337, 345-449; L02.html:376-388, 395-493; L03.html:343-355, 362-459", P,
    R + "scans_a_r6.out structure counts: misconceptions 3, 3, 3; problems L01 13 (3, 3, 4, 3), L02 12 (3, 3, 3, 3), L03 12 (3, 3, 3, 3); solutions equal the problem counts.")
row("PC3a-hours-declared", "2.9 structure: lesson hours declared", "L01.html:2, 34; L02.html:2, 34; L03.html:2, 34", P,
    "data-hours=\"6\" on each page and the eyebrow reads 'PC3 · Lesson n of 6 · 6 study hours' (grep of each page).")

# ---- round-4 rows kept by id (re-verified this round) ----
row("PC3a-r4-delta-read", "2.9 change read: delta from the round-5 pin", "git diff 7376a5e2 4bd8cb94 (index.html, L01-L03, twins)", P,
    "git diff --quiet 7376a5e2 4bd8cb94 -- index.html tests/labs/PC3/ exits 0 (both byte-identical). git diff 7376a5e2 4bd8cb94 on L01.html: 3 hunks (Remark 1.6 at 135, Example 1.7 at 140-141, lab hypothesis at 146, misconception at 327-328, E2 solution at 408); "
    "L02.html: 2 hunks (Introduces line 38, lab hypothesis line 134); L03.html: 5 hunks (Definition 3.5 at 92, Example 3.6 at 102, Example 3.11 at 327, misconception 352-353, key rows 471-475). Every hunk was read in full and every changed claim re-verified above.")
row("PC3a-r4-cross-references", "2.9 cross-references resolve", "L01.html:82, 107, 532; L02.html:458, 592; L03.html:316, 345, 509, 518, 537, 542, 568; index.html:79", P,
    "Resolved by reading the pages: Section 4 (L01.html:314), Research problem R3 (L01.html:444), Problem P2 (L01.html:380), Section 3 (L02.html:363), Research problem R1 (L03.html:440), Problem M2 (L03.html:372), Problem P3 (L03.html:404), Example 3.3 (L03.html:79) for the hub's placement item 1.")
row("PC3a-r4-recompute-all-numbers", "2.2 numbers: every number in the slice recomputed by script", "recompute_L01_r6.py, recompute_L02_L03_r6.py, recompute_hub_r6.py", P,
    R + "recompute_L01_r6.out 62/62; " + R + "recompute_L02_L03_r6.out 64/64; " + R + "recompute_hub_r6.out 18/18. Total 144 checks, 0 failures.")
row("PC3a-r4-restated-M4-concepts", "2.5 DAG: M4 concepts referenced by link, not redefined", "L02.html:57, 67; L03.html:62", P,
    "L02.html:57 links M4 Lesson 1 and names events without a dfn; L02.html:67 Definition 2.2 links conditional-expectation-elementary (concepts.html); L03.html:62 links expectation. No M4 concept is given a dfn with data-concept in L01-L03 (dfn list in scans).")
row("PC3a-r4-observations-no-row", "2.4 observations (no defect)", "L01.html:433; tests/labs/PC3/lab-PC3-L02-1.py:278-280", P,
    "(a) R1 criterion (c) is answered by a bound (L01.html:433); acceptable for an open design question. (b) Twin lines 278-280 type a prior 1/2 and a likelihood 3/4 as constants in the Bayes check; the lab labels that check as an exact check, not an estimate. No defect.")
row("PC3a-L03-misconception-most-likely", "2.2 misconception: wrong belief and correction", "L03.html:352-353", P,
    "Round-5 FAIL is fixed. The correction says zero average confuses with absence of gains and cites Example 3.11 (+100 with probability 1/2). Consistent with Example 3.11 (L03.html:327).")
row("PC3a-L03-def35-next-turn", "2.4 definitions: fairness at histories of fewer than N turns", "L03.html:92 (Definition 3.5), 293 (A3), 300 (H2)", P,
    "Round-5 FAIL is fixed. Definition 3.5 now quantifies histories of fewer than the game's number of turns with positive probability, matching A3 (293) and H2 (300); at length N there is no next turn, so the definition is well-formed.")

# ---- round-6 new rows ----
row("PC3a-banned-and-process-words", "2.9 banned phrases and process words (learner text)", "L01.html:408", F,
    R + "scans_a_r6.out (script ledgers/PC3/scripts/PC3-a-r6/scans_a_r6.sh): banned phrases none on the four pages. The process-word grep finds the whole word 'round' at L01.html:408 "
    "('Dividing those four-place values gives 0.3085, which is 30.85 percent and would round to 30.9 percent'). The plan bans 'round' from learner text (plans/PC3-build-plan.md §2.1 item 11; the E5 process-word rule).",
    "L01.html:408: replace 'would round to 30.9 percent' with 'would display as 30.9 percent'. Then rerun scans_a_r6.sh and confirm the process-word grep returns nothing on the four pages.")
row("PC3a-r6-hub-ladder-rung2-wording", "2.9 consistency: hub describes rung 2 as the project does", "index.html:159; course/modules/PC/PC3/project.html:45, 253, 349-350", F,
    "index.html:159 says rung 2 is 'the same replay with the cash-flow line and the mark line removed'. project.html:45 says those two lines are 'left blank', project.html:253 says they are 'blanked with ___', and project.html:349-350 contains 'cash_flow = ___' and 'mark = ___'. Nothing is removed.",
    "index.html:159: change 'removed' to 'left blank (each of the two lines replaced by ___)'.")
row("PC3a-r6-hub-project-file-names", "2.9 consistency: hub and project name the same student files", "index.html:160, 167; course/modules/PC/PC3/project.html:46, 393, 429-448", F,
    "index.html:160 and :167 name policy.py and pnl.py. project.html names only market_maker.py (grep -o: 46, 393, 429, 430, 442, 443, 448) and contains no policy.py or pnl.py. "
    "plans/PC3-build-plan.md §5.2 requires policy.py (quote) and pnl.py (replay). The hub matches the plan; the project does not (project.html is outside this slice, owner of the project slices).",
    "Project owner (project.html, grader/): rename the student's files to policy.py and pnl.py as plans/PC3-build-plan.md §5.2 requires, so index.html:160 and :167 are true. If the architect adopts market_maker.py instead, change index.html:160 and :167 to market_maker.py (and the grader file names to match).")
row("PC3a-r6-hours-curriculum-attribution", "2.9 prose: attribution of the 14-hour project figure", "index.html:167", F,
    "index.html:167 says the 14 hours 'is the curriculum figure's project share'. curriculum/curriculum.json PC3 entry has hours 50 and no project-hours field; curriculum/06-profession-capstone.yaml:157-182 has no project hours (read this round). 14 hours is a unit design figure (plans/PC3-build-plan.md §1 and open question 11).",
    "index.html:167: delete 'which is the curriculum figure's project share' and end the sentence with 'which is 28 percent of the module'.")
row("PC3a-r6-def21-m4-weights-positivity", "2.4 attribution: the definition cited to M4 Lesson 1", "L02.html:57 (Definition 2.1); L03.html:57 (Assumption A1)", F,
    "Both say 'a finite probability space, as defined in M4 Lesson 1, with weights p(omega) that sum to 1'. M4 Lesson 1 defines a finite probability space with weights p(omega) > 0 (course/modules/M/M4/L01.html:55). The text omits the positivity condition while attributing the definition to M4, so the attribution misstates M4.",
    "L02.html:57 and L03.html:57: write 'with weights p(omega) > 0 that sum to 1' (or drop 'as defined in M4 Lesson 1' and say 'as in M4 Lesson 1, with zero weights also allowed'). Nothing else changes; no theorem depends on positivity.")

fragment = {
    "unit": "PC3",
    "slice": "PC3-a",
    "round": 6,
    "verifier": "Claude Haiku 5.5, independent verifier PC3 slice a, round 6 (did not build PC3; no shared context with the builders)",
    "pin": "4bd8cb9 (4bd8cb94a8e171e80c4c34da1b3f32be7cb93f07), detached",
    "base": "7376a5e2 (the round-5 pin, the fragment's pin 7376a5e). Delta for the slice: git diff 7376a5e2 4bd8cb94 touches L01.html, L02.html and L03.html only; index.html and the three twins are byte-identical (git diff --quiet). No round-5 PASS row was carried: every row was re-verified this round, and the round-5 evidence was used only as a pointer.",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE6-PC3-a (detached at 4bd8cb9; .venv symlinked to /Users/billyribeiro/dev/quant-phd/.venv, CPython 3.14)",
    "scratch": "none outside the checkout: every script and output is under ledgers/PC3/scripts/PC3-a-r6/ (outputs/ subfolder)",
    "verified_at": datetime.datetime.now(datetime.UTC).replace(microsecond=0).isoformat(),
    "verdict": "FAIL",
    "scope": "course/modules/PC/PC3/index.html, L01.html, L02.html, L03.html and tests/labs/PC3/lab-PC3-L01-1.py, lab-PC3-L02-1.py, lab-PC3-L03-1.py. Not in this slice: L04-L06, project.html, grader/, cards.json, project labs.",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Mutation testing: not applicable to lesson pages or lab twins (architect ruling: mutation applies to project graders only). mutants is empty by ruling; no grader is in this slice.",
        "Round-5 FAIL rows PC3a-L01-misconception-accuracy, PC3a-L03-misconception-most-likely and PC3a-L03-def35-next-turn are fixed in the round-6 checkout and are PASS here, each re-verified from the text and the lab output.",
        "Four new defects are FAIL in round 6: PC3a-banned-and-process-words (L01.html:408 'round'), PC3a-r6-hub-ladder-rung2-wording (index.html:159), PC3a-r6-hub-project-file-names (index.html:160, 167 against project.html), PC3a-r6-hours-curriculum-attribution (index.html:167), PC3a-r6-def21-m4-weights-positivity (L02.html:57, L03.html:57). One of the five (the project file names) is a cross-slice defect whose fix lies in project.html.",
        "Gate misuse avoided: check_pages is run with --unit PC3 (which runs the hub check), not --page index.",
        "Not checked: 360 px and dark-mode visual inspection (page_smoke geometry and console checks only, no screenshot); a passage-level check of the two reading-list books (the slice cites no locator, and the books are cited at book level only); L04-L06, project.html, grader/, cards.json and the project labs (outside this slice; only the tool gates were run for them).",
        "No freshness flag: the slice makes no empirical claim and cites no 2025-2026 work; the two reading-list keys are cited at book level only.",
    ],
    "summary": {},
}
fragment["summary"] = {
    "rows": len(rows),
    "pass": sum(1 for r in rows if r["status"] == P),
    "fail": sum(1 for r in rows if r["status"] == F),
    "unverifiable": 0,
}
out = Path("ledgers/PC3/PC3-a.json")
out.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out, fragment["summary"])
