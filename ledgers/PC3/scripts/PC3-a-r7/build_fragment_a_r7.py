"""Round 7: write the PC3 slice-a fragment (hub index, L01-L03, lab twins). Rows keep every round-6 id."""
import json
import sys
from datetime import datetime, UTC
from pathlib import Path

ROOT = Path(sys.argv[1])
O = "ledgers/PC3/scripts/PC3-a-r7/outputs/"
P = "PASS"
F = "FAIL"
rows = []


def R(rid, check, location, status, evidence, fix=None):
    row = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != P:
        row["fix"] = fix
    rows.append(row)


# ---- gates and tool runs ----
R("PC3a-check-pages", "2.9 structure: check_pages (hub and L01-L03)", "index.html; L01.html; L02.html; L03.html", P,
  O + "gates.out (script ledgers/PC3/scripts/PC3-a-r7/run_gates_a_r7.sh): 'check_pages PC3: PASS' exit 0 (includes the hub); 'check_pages PC3 L01', 'L02', 'L03: PASS' exit 0 each.")
R("PC3a-check-dag", "2.9 DAG: check_dag and independent link/anchor/concept-id scan", "index.html; L01.html; L02.html; L03.html", P,
  O + "gates.out: 'check_dag PC3: PASS' exit 0. " + O + "links_and_titles_a_r7.out (script ledgers/PC3/scripts/PC3-a-r7/links_and_titles_a_r7.py): no MISSING anchor, file or concept id; every concept link's href fragment equals its data-concept.")
R("PC3a-check-projects", "2.6 projects: check_projects (tool result only; project.html is outside this slice)", "course/modules/PC/PC3/project.html", P,
  O + "gates.out: 'check_projects PC3: PASS' exit 0. Project content is outside this slice; the hub's claims about it are checked under the hub rows.")
R("PC3a-run-labs", "2.5 labs: run_labs", "tests/labs/PC3/lab-PC3-L01-1.py, L02-1.py, L03-1.py; L01.html:144-311; L02.html:132-360; L03.html:112-287", P,
  O + "gates.out: 'run_labs PC3: PASS (9/9)' exit 0; 'run_labs PC3: PASS (1/1)' for --page L01, L02 and L03 (exit 0 each).")
R("PC3a-twins-alone", "2.5 labs: each twin alone under python -I -W error", "tests/labs/PC3/lab-PC3-L01-1.py, L02-1.py, L03-1.py", P,
  O + "gates.out: the three twins run as `python -I -W error <twin>` exit 0 each, output discarded.")
R("PC3a-pytest-labs", "2.5 labs: pytest on the lab cases", "tests/test_labs.py (PC3 cases)", P,
  O + "gates.out: `pytest tests/test_labs.py -k PC3 -q` -> 9 passed, exit 0; `--collect-only -k PC3` -> 'tests/test_labs.py: 9'.")
R("PC3a-page-smoke", "2.9 page_smoke, run alone on the four slice pages", "index.html; L01.html; L02.html; L03.html", P,
  O + "page_smoke_slice_r7.out: `tools/page_smoke.py --unit PC3 --pages index L01 L02 L03` (page stems; a run with path arguments matched no page and was discarded) -> each of the four pages PASS, labs lab-PC3-L01-1 to L03-1 run, 'page_smoke PC3: PASS' exit 0.")
R("PC3a-ruff-mypy", "2.5 labs: ruff and mypy --no-incremental on the twins", "tests/labs/PC3/lab-PC3-L01-1.py, L02-1.py, L03-1.py", P,
  O + "gates.out: 'All checks passed!' (ruff check); '3 files already formatted' (ruff format --check); 'Success: no issues found in 3 source files' (mypy --no-incremental). All exit 0.")
R("PC3a-verify-refs", "2.1 citations: verify_refs offline and live for PC3", "references/references.json; index.html:177", P,
  O + "gates.out: 'offline integrity: 560 entries, 0 problems' exit 0. " + O + "verify_refs_unit_PC3_r7.out: 'live re-verification of PC3: 2 of 560 entries, 0 problems', exit 0. references.json: zhou2008practical and crack2015heard, status verified, used_by [PC3]. Both are cited at book level only (index.html:177).")

# ---- hub ----
R("PC3a-hub-hours", "2.9 hours: the split sums to the declared figure", "index.html:29, 42, 167; L01.html:2; L02.html:2; L03.html:2", P,
  "index.html:29 data-hours-lessons=\"36\", data-hours-project=\"14\"; :42 '36 h lessons · 14 h project (28%)'. L01, L02, L03 data-hours=\"6\" (" + O + "scans_a_r7.out). Arithmetic: 6 x 6 = 36, 36 + 14 = 50 = PC3 hours in curriculum.json (" + O + "links_and_titles_a_r7.out), 14/50 = 28 percent (" + O + "hub_placement_and_scans_r7.out). The line items of the project split are a separate row.")
R("PC3a-hub-placement", "2.4 numbers and answers: placement diagnostic", "index.html:76-136 (ten items)", P,
  O + "hub_placement_and_scans_r7.out and recompute_r7.py: data-answer values 3.5 (21/6), 0.25, 2, 3, 90.909091 (100/1.1 = 90.909090909, six places), -10005 and 10040 match their items; 80 percent of ten items is eight, and seven of ten is 70 percent. Option keys read at index.html:97-127 (binary search O(log n); S e^{r tau}; balance-sheet identity). The skill-check convention in item 9 is a separate row (PC3a-r7-hub-skill-check-bid-ask).")
R("PC3a-hub-titles-prereqs", "2.9 structure: hub titles and prerequisite closure", "index.html:35, 61-67", P,
  O + "links_and_titles_a_r7.out: curriculum.json PC3 'Quant & Finance Interviews', prereqs [M4, CS2, FC2], hours 50; M4 'Probability', CS2 'Algorithms & Data Structures', FC2 'Derivatives Fundamentals'. tools/coursekit.py prerequisite_closure('PC3') = {AC1, CF1, CS1, CS2, E1, FC1, FC2, M1, M2, M4, P0.1}, the set listed at index.html:35.")
R("PC3a-hub-objectives", "2.9 prose: objectives match the lessons", "index.html:48-56", F,
  "Objectives 1-6 map to the lessons: objective 1 to Theorem 1.2 and Proposition 1.3 (L01.html:67-90); objective 2 to Propositions 2.4 and 2.5 (L02.html:75-100); objective 3 to Theorem 3.8 with A3 (L03.html:296-311); objectives 4-6 name Lessons 4-6, which are outside this slice. Objective 7 (index.html:55) says the policy and replay 'pass the autograder on seeds 0 to 49', which omits the workspace seed and seed + 7919 that the project grades (project.html:397, '52 seeds'). See PC3a-r7-hub-autograder-seeds.",
  "Change objective 7 at index.html:55 so that it names the workspace seed as well as seeds 0 to 49, as in the fix of PC3a-r7-hub-autograder-seeds. Objectives 1-6 need no change.")
R("PC3a-hub-lesson-map", "2.9 structure: lesson map cards", "index.html:145-150; L01.html:35, L02.html:35, L03.html:35", P,
  "Card titles at index.html:145-147 ('Fermi Estimation and Mental Math', 'Probability Puzzles and Conditional Reasoning', 'Expected-Value Games') equal the h1 of L01, L02, L03; kickers 'L0n · 6 h' equal data-hours=\"6\" (" + O + "scans_a_r7.out). Cards for L04-L06 are outside this slice.")
R("PC3a-hub-data", "2.8 data: no dataset and no data-files", "index.html:37, 170-173; tests/labs/PC3/lab-PC3-L01-1.py, L02-1.py, L03-1.py", P,
  "No data-files, data-cite or http(s) reference on the four pages (" + O + "scans_a_r7.out). grep -l 'open(\\|read_text\\|urllib\\|requests\\|json.load\\|csv' over tests/labs/PC3/*.py and course/modules/PC/PC3/grader/*.py: no match (exit 1). Twins: open/read/http hits 0 (scans_a_r7.out).")
R("PC3a-hub-P0.1-claim", "2.9 prose: P0.1 claims", "index.html:35, 74; course/concepts.html:34-47", P,
  "concepts.html:34-47: the P0.1 section lists eleven entries, each ending 'not yet released' (read this round). No href or data-concept on the four pages names a P0.1 concept (" + O + "links_and_titles_a_r7.out). The placement claim that no item tests P0.1 holds (index.html:72-138).")

# ---- L01 ----
R("PC3a-L01-numbers", "2.2 numbers in prose and rounding", "L01.html:55, 99-100, 107, 137-141, 287-309, 328, 336, 401-415, 433, 447, 462-465", P,
  O + "recompute_r7.out (script recompute_r7.py): 96 of 96 checks PASS, FAILS []. Covers 12000, 234000, ratio 19.5, ln 19.5 = 2.9704144656, geometric midpoint 52990.57 (2 dp) and 52990.5652 (4 dp), factor widths 1.0986, 1.6094, 0.2624, Part 2 reductions 0.4054651081, 0.9162907319, 0.1753528875 and totals, shares 30.8 and 5.9 percent, ratio 0.9485, bound excess 5.4 percent, miss share 7.9 percent, E3 ln 16.5 = 2.8034 and 0.167054, R1 half-width 1.4852, R3 0.4055 and 0.9063, and the Taylor values for n = 2, 5, 10 and x = 0.01, 0.05.")
R("PC3a-L01-proofs", "2.4 mathematics: Theorem 1.2, Proposition 1.3, Theorem 1.5, Remark 1.6, P1-P3", "L01.html:76-80, 92-94, 128-135, 374-391", P,
  "Re-derived by hand this round. L01.html:78: ab - a'b' = a(b - b') + b'(a - a') and AB - ab = A(B - b) + b(A - a) (expansions checked term by term), with the sign conditions stated. Induction (79): the lemma applied with (P, L, x_k, l_k) and (U, u_k, P, x_k) under the induction hypothesis 0 < L <= P <= U; attainment at the corners. Proposition 1.3 (92-94): rearrangement and ln(ab) = ln a + ln b (M1). Theorem 1.5 (128-131): A2 for x > 0 gives remainder = n(n-1)/2 (1+xi)^(n-2) x^2 with 0 < xi < x, so 0 <= remainder <= the bound; x = 0 direct. Remark 1.6 (134-135): equality at n = 2, strict for n >= 3, x > 0. P1 (374-377), P2 (381-383) and P3 (387-391) solutions re-derived; no gap found.")
R("PC3a-L01-A2-false-at-x0", "2.4 mathematics: assumption used only where it holds", "L01.html:115 (A2), 123 (H3), 130 (x = 0)", P,
  "A2 is stated for x != 0 (L01.html:115). H3 invokes A2 only for x > 0 (L01.html:123). The x = 0 case is proved directly at L01.html:130 (both sides 0).")
R("PC3a-L01-grades-lab-only", "2.3 grades: T for proved results, C for lab-printed results", "L01.html:458-465 (key results)", P,
  "Rows 458-462 are T and each has an on-page basis: Theorem 1.2, Proposition 1.3, Theorem 1.5 under A2, the hand product of Example 1.4, and ln 19.5 by Proposition 1.3. Rows 463-465 are C and name Lab 1 (Parts 1-3); the printed values equal the expected block (" + O + "embed_compare_a_r7.out).")
R("PC3a-L02-grade-drill-lab-only", "2.3 grades: lab-only result graded C", "L02.html:508", P,
  "L02.html:508 grades 'closed form equals enumeration on 12 of 12 items' as C with basis 'Lab 1, Part 1 (seed 0, self-check)'; the expected block line 340 prints 'closed form equals enumeration on 12 of 12 items' (" + O + "embed_compare_a_r7.out: expected == twin stdout).")
R("PC3a-L01-claims", "2.3/2.9 prose claims checked against the proofs and the lab", "L01.html:67-90, 82, 105-107, 113-141, 317-319, 328", P,
  "'Both bounds are attained' (73) matches the attainment argument (79). Order independence and 'lowers the total by exactly the drop' (105) follow from Proposition 1.3. 'A factor whose own width is already small can lower the total by at most that small width' follows since a narrowed width is nonnegative. 'Theorem 1.2 holds for every combination' (317, 82) matches its ranges-only proof. The Taylor claim is restricted to x >= 0 (319) as in H2. Remark 1.6's 'the printed remainder is below the printed bound' for n = 5 and n = 10 holds in the expected block lines 304-307 (four inequalities).")
R("PC3a-L01-lab-match", "2.5 labs: page code equals twin; expected block equals twin output", "L01.html:144-311; tests/labs/PC3/lab-PC3-L01-1.py", P,
  O + "embed_compare_a_r7.out (script embed_compare_a_r7.py, trailing newline ignored): 'L01: page code == twin True' (5775 chars); 'expected == twin stdout True' (26 lines); data-tolerance=1e-9; no @@ placeholders. Hypothesis (L01.html:146) names 12000, 234000, 19.5, 2.9704144656, 125 products, the Part 2 narrowings, Part 3 with n = 2, 5, 10 and x = 0.01, 0.05, the 1e-9 tolerance and the 1e-12 float check; all match the twin and the output.")
R("PC3a-L01-problems-quiz", "2.9 structure: problem tiers, solutions and quiz", "L01.html:345-451 (13 problems), 470-548 (quiz)", P,
  O + "scans_a_r7.out: 13 problems and 13 solutions (mechanics 3, proof 3, empirical 4, research 3); 10 quiz items. Keyed answers re-derived in recompute_r7.py: 10 (Q1), ln 4 = 1.386294 (Q2), 234000 (Q4), 0.004622 (Q6), 52990.5652 (Q9); the MC keys (Q3, Q5, Q7, Q8, Q10) checked against the lesson text. Solutions M1-M3, P1-P3, E1-E4, R1-R3 re-derived by hand.")
R("PC3a-L01-only-scope", "2.9 scope: the exceptions named to 'only the ordinary order and arithmetic'", "L01.html:55, 82, 314", P,
  "L01.html:55 names the exceptions used: the logarithm (Proposition 1.3, Example 1.4), derivatives and the Taylor theorem (Section 3), the binomial theorem (Remark 1.6) and the square root (Example 1.4). Each is used where named. L01.html:82 points to Section 4, which exists (L01.html:314).")
R("PC3a-L01-twin-docstring-decimals", "2.5 labs: twin docstring matches the code", "tests/labs/PC3/lab-PC3-L01-1.py:1-8, 96", P,
  "Twin docstring lines 6-7: 'one float check ... uses a tolerance of 1e-12' and 'Decimal values print to ten places'. Line 96: abs(sum(parts) - width) < 1e-12, the one float check. Part 1-3 prints use :.10f (expected block shows ten places).")
R("PC3a-L01-research-problems", "2.4 mathematics: open problems R1-R3 answers", "L01.html:430-449", P,
  O + "recompute_r7.out: R1 half of ln 19.5 = 1.4852; ln 5 = 1.6094 exceeds it, ln 3 = 1.0986 and ln 1.3 = 0.2624 do not. R2: the proof uses only (H1) and (H2) (L01.html:70-71, 438-440). R3: ln(3/2) = 0.4055 is the reduction for A, ln(2.5/1.01) = 0.9063 for B; B's width ln 2.5 = 0.9163 is smaller than A's ln 3 = 1.0986, so the claim is false.")
R("PC3a-L01-misconception-accuracy", "2.2/2.3 misconception: wrong belief and correction", "L01.html:327-328", P,
  O + "recompute_r7.out: the drops 0.1753528875 and 0.9162907319; shares 5.9 and 30.8 percent of the baseline total 2.9704 (Lab 1, Part 2 prints the drops, expected lines 298-300).")
R("PC3a-L01-KR-ln19.5-grade", "2.3 grades: key-results rows 462 and 463", "L01.html:461-463", P,
  "Row 462 'log-error width ln 19.5 ... the sum of the three factor widths' is T (Proposition 1.3 and Example 1.4, proof on this page). Row 463 'ln 19.5 = 2.9704144656, to ten places' is C (printed by Lab 1, Part 1). Both values recomputed (recompute_r7.out).")
R("PC3a-L01-E2-shares", "2.2 numbers: E2 solution (shares of the total width)", "L01.html:405-410", P,
  "The E2 solution now says 'would display as 30.9 percent' (the word 'round' is removed). 0.9163 / 2.9704 = 0.308477, whose four-place value 0.3085 is 30.85 percent; full precision 0.9162907319 / 2.9704144656 = 0.308472, which is 30.8 percent; minutes 0.1753528875 / 2.9704144656 = 0.059033, which is 5.9 percent (recompute_r7.out).")

# ---- L02 ----
R("PC3a-L02-numbers", "2.2 numbers: examples, exercises and key rows", "L02.html:111-130, 398-417, 449-466, 489-493, 503-507", P,
  O + "recompute_r7.out (script recompute_r7.py): Bayes and total-probability values 29/100, 15/29 (M2), 2/5 (M3, 12/30), 1/6 (M1), 57/64 (E1), 1/6 (E3); Example 2.6 1/3 and 1/2; Example 2.7 3/5, 3/5, 3/10 and 12/20, 6/20; Example 2.9 1/2 and 3/4; the Monty Hall values 1/3, 2/3 (rule A) and 1/2, 1/2 (rule B) by a separate brute force over (car, pick, host door) in monty().")
R("PC3a-L02-proofs", "2.4 mathematics: Propositions 2.4 and 2.5, P1-P3", "L02.html:75-100, 423-441", P,
  "Re-derived. Proposition 2.4 (85): Definition 2.2 applied both ways, both conditionals defined by (H1), division by P(B) > 0. Proposition 2.5 (99): B is the disjoint union of B and A_i by (H1), each term by Definition 2.2 with (H2). P1 (426), P2 (433) and P3 (440) use only A1, positivity and additivity; no gap found.")
R("PC3a-L02-lab-match", "2.5 labs: page code equals twin; expected block equals twin output", "L02.html:132-360; tests/labs/PC3/lab-PC3-L02-1.py", P,
  O + "embed_compare_a_r7.out: 'L02: page code == twin True'; 'expected == twin stdout True' (32 lines); data-tolerance=0 (exact fractions).")
R("PC3a-L02-interp-reverse-conditional", "2.2 interpretation: reverse conditional", "L02.html:359", P,
  "L02.html:359 '1/3 against 1 for two flips' matches expected block line 350 (P(both heads | at least one head) = 1/3) and line 352 (P(at least one head | both heads) = 1).")
R("PC3a-L02-misconceptions-quiz", "2.9 structure: misconceptions and retrieval quiz", "L02.html:376-388; L02.html:517-587", P,
  "Three misconceptions with corrections (Monty Hall 1/2 by symmetry; the two conditioning events; P(A|B) = P(B|A)); each correction matches Examples 2.6 and 2.8 and Proposition 2.4. Quiz: 10 items (8-15); numeric keys 1/3 (0.333333, tolerance 1e-6), 3/5 (0.6), 3/4 (0.75), 1, 3/10 (0.3); MC keys re-derived from Definition 2.2, Example 2.8 and H1 of Proposition 2.4.")
R("PC3a-L02-where-canon-breaks", "2.9 prose: canon-breaks bullets", "L02.html:362-371", P,
  "Bullet 1: 2/3 under rule A and 1/2 under rule B (Example 2.8, verified). Bullet 2: Example 2.7 symmetry and the blue-first case 3/4 (verified). Bullet 3: Example 2.6 values (verified). Bullet 4: A1 limits results to finite spaces (L02.html:62).")
R("PC3a-L02-twin-bag-ball-label", "2.5 labs: twin labels equal the page's examples", "tests/labs/PC3/lab-PC3-L02-1.py Parts 3-4; L02.html:116, 129", P,
  "Twin bags {'bag 1': (3, 1), 'bag 2': (1, 3)} equal Example 2.9 (L02.html:129). Twin balls r1, r2, r3, b1, b2 and the 20 ordered pairs equal Example 2.7 (L02.html:116).")
R("PC3a-L02-finite-probability-space-redefined", "2.4 definitions: Definition 2.1 attribution to M4 Lesson 1", "L02.html:57; L02.html:62", P,
  "Definition 2.1 reads 'weights p(omega) > 0 that sum to 1'. M4 Lesson 1 states the same ('weights p(omega) > 0', course/modules/M/M4/L01.html, Section 1 first paragraph). Assumption A1 (L02.html:62) limits the lesson to finite spaces.")

# ---- L03 ----
R("PC3a-L03-numbers", "2.2 numbers: expectations, continuation values, fee sensitivity, biased-game values", "L03.html:80, 102-104, 322, 329-337, 340-356, 418-432, 441-450, 455-457", P,
  O + "recompute_r7.out (script recompute_r7.py): 350 and 7/2 (die), 7 (two dice); continuation 250; value 1150/3 = 383.33 (2300/6); gain 100/3 = 33.33; 1150/3 - 350; biased per-turn 25 and 150; biased rules 1575/32, 575/8, 625/8 and -575/8 = -71.875 (independent recursion); fair rules 0; R1 expected total 50; R2 gain 74.5 at fee 1 and 100/3 at fee 100; best of 64 policies = 1150/3.")
R("PC3a-L03-proofs", "2.4 mathematics: Proposition 3.2, Theorem 3.8 and proof, Definition 3.7", "L03.html:66-76, 107-110, 296-311", P,
  "Proposition 3.2 (75): distributive law and exchange of finite sums. Theorem 3.8 (307-311): base at N by Definition 3.7 (the rule stops at length N); step: continue case gives V(h) = sum_x P(x|h)(W(h) + x) = W(h) + 0 by fairness at h (H2), using V(h,x) = W(h) + x for each x with P(h,x) > 0; V(empty) = E[W] = 0. Re-derived; no gap found.")
R("PC3a-L03-A3-zero-probability-histories", "2.4 mathematics: A3 and H2 quantify positive-probability histories only", "L03.html:292-293 (A3), 300 (H2), 308", P,
  "A3 (292-293) states the fairness condition for histories with P(h) > 0; H2 (300) restates it for those histories; the proof (308) states that histories of probability zero add nothing and are not needed.")
R("PC3a-L03-thm-number-3-10", "2.2 cross-references: no Theorem 3.10", "index.html; L01.html; L02.html; L03.html", P,
  "grep -c 'Theorem 3.10' on the four pages: 0 each. Example 3.10 (L03.html:319-323) cites Theorem 3.8 (321-322).")
R("PC3a-L03-adapted-undefined", "2.4 notation and terms: no undefined probabilistic term", "index.html; L01.html; L02.html; L03.html", P,
  "Case-insensitive grep on the four pages: 'adapted', 'filtration', 'sigma', 'martingale', 'stopping time', 'optional stopping', 'Poisson', 'Markov', 'Kelly', 'binomial distribution', 'Bayesian': 0 each. 'Bernoulli' appears in L01 (Problem P2 and quiz item Q8) as Bernoulli's inequality, which is proved on the page (P2).")
R("PC3a-L03-each-rule-claim", "2.4/2.9 claim: each of the five rules is a stopping rule of Definition 3.7", "L03.html:321, 552; tests/labs/PC3/lab-PC3-L03-1.py RULES", P,
  "L03.html:321 'Each is a stopping rule in the sense of Definition 3.7'. The RULES tuple in the twin (lines 223-229) depends only on the history h; the engine forces a stop at length HORIZON (the definition's clause). A2 holds fairness at every history (97), so Theorem 3.8 applies to all five.")
R("PC3a-L03-grades-lab-only", "2.3 grades: T for proved results, C for lab-printed results", "L03.html:468-475", P,
  "T rows 468, 469, 470, 473, 475 each have an on-page basis (Proposition 3.2; Theorem 3.8 under A3; Example 3.6 backward induction; Theorem 3.8 with A2 over N = 6; Example 3.3 and Proposition 3.2). C rows 471, 472, 474 name Lab 1 Parts 2, 3 and 3b, whose printed values equal the expected block (embed_compare_a_r7.out).")
R("PC3a-L03-any-game-fee", "2.2 numbers: R2 reroll-game gain and fee formula", "L03.html:448-450", P,
  O + "recompute_r7.out: gain = (sum_f max(100f, 350 - c))/6 - 350 equals 100/3 at c = 100 and 74.5 at c = 1; the R2 criterion (gain of at least 10 cents, both values exact, game not fair) holds for c = 100.")
R("PC3a-L03-lab-docstring-two-methods", "2.5 labs: docstring claims match code", "tests/labs/PC3/lab-PC3-L03-1.py docstring and functions; L03.html:114", P,
  "Docstring: Part 2 'by backward induction ... and by enumerating every stopping policy' (backward_induction, policy_value over product((0,1), repeat=6)); Part 3 'by two methods that must agree' (stopping_expectation by recursion, stopping_by_sequences over 64 sequences, the agreement check printed True); Part 3b 'by the recursion alone' (only stopping_expectation is called in part_three's second loop).")
R("PC3a-L03-why-rhetorical-questions", "2.9 prose: why-it-matters paragraphs (no rhetorical question, length)", "L01.html:51; L02.html:51; L03.html:51", P,
  O + "scans_a_r7.out: why-it-matters word counts 119 (L01), 117 (L02), 120 (L03), each at most 120. None of the three contains '?'. Question marks elsewhere are quiz and open-problem prompts.")
R("PC3a-L03-numbers-prose-claims", "2.2 prose numbers: 6 x 25, mean 350, 1150/3 - 350", "L03.html:104, 322, 336, 349", P,
  O + "recompute_r7.out: 6 x 25 = 150; 1575/32, 575/8, 625/8 (biased rules); 350 and 1150/3 (Example 3.6); 1150/3 - 350 = 100/3 = 33.33 and 383.33 to two places.")
R("PC3a-L03-quiz", "2.9 structure: retrieval quiz", "L03.html:480-564 (12 items)", P,
  "12 items (8-15). Numeric keys 350, 0.333333, 383.333333 (tolerance 1e-4), 250, 50, 150, 7 verified by recompute_r7.out. MC keys (Definition 3.1, Definition 3.5, H3 of Theorem 3.8, faces 1 and 2, the biased game) match the lesson text.")
R("PC3a-L03-lab-match", "2.5 labs: page code equals twin; expected block equals twin output", "L03.html:112-287; tests/labs/PC3/lab-PC3-L03-1.py", P,
  O + "embed_compare_a_r7.out: 'L03: page code == twin True'; 'expected == twin stdout True' (30 lines); data-tolerance=0.")
R("PC3a-L03-canon-breaks", "2.9 prose: canon-breaks bullets", "L03.html:330-337", P,
  "Unbounded stopping (no value claimed, Remark 3.9 and Section 4 agree); fairness as a hypothesis (Example 3.10 values verified); choice in a non-fair game (Example 3.6, mean 350) verified.")
R("PC3a-L03-fair-game-before-definition", "2.5/2.9 terms before definition: Definitions 3.5 and 3.7 precede the lab", "L03.html:51, 91-92, 108-110, 112", P,
  "Forward references in the why paragraph (51) name Definition 3.7 (stopping rule) and Definition 3.5 (fair game) and are defined at 91-92 and 108-110, before the lab at 112 and before the computation that uses them.")
R("PC3a-why-terms-before-definition", "2.9 terms used before definition", "L01.html:51-58; L02.html:38, 51; L03.html:51, 91-92", P,
  "L01: 'Fermi estimate' and 'factor range' are defined at line 59 (dfn); 'product interval' at 73 and 'log-error width' at 89 precede their use in Example 1.4. L02: Bayes' rule appears in the meta line and the why paragraph as a named forward reference to Proposition 2.4 (80). L03: 'stopping rule' and 'history' are forward references naming Definitions 3.7 and 3.5, defined before the first computation that uses them.")
R("PC3a-L03-numbers-key-rows-lab", "2.3 grades: key-results rows 471, 474, 475", "L03.html:471, 474, 475", P,
  O + "row 471 (best of 64 policies = 1150/3) is C and matches Lab Part 2; row 474 (biased values) is C and matches Part 3b; row 475 (two dice E = 7) is T with Example 3.3 and the Part 1 cross-check. Values equal the printed output (embed_compare_a_r7.out).")
R("PC3a-notation", "2.4 notation: registered symbols and macros", "index.html; L01.html; L02.html; L03.html; notation/notation.json", P,
  "Macros in the slice: \\E, \\Prob, \\R, \\indic (registered in notation/notation.json), plus standard \\ln, \\log, \\max, \\binom, \\sqrt, \\tfrac, \\dfrac, \\text, \\mid, \\dots, \\cdots, \\ldots. No \\mathbb, \\Phi, \\gamma_3, \\gamma_4, \\mathbb{Q} or R^\\ast. The only \\ast is the forward price F^\\ast (index.html:112), which is not a registered symbol. Local letters (N, t, h, x, W, V, p, c, f, m, P, L, U, Q, X, Y) are defined where first used (L03.html:109 for N); none takes a registered meaning.")
R("PC3a-dag-prose-only-terms", "2.9 DAG: concepts outside the closure appear only as prose", "index.html:148; L01.html (misconception 2); L02.html:57, Problem P2; L03.html:57", P,
  "'adverse selection' (E2 concept, outside the closure) appears only in the hub's L04 card (index.html:148) as plain prose: no link, no dfn. 'confidence interval' (S1 concept, outside the closure) appears only inside a stated misconception (L01.html:331), with no link and no dfn. 'finite probability space' (L02.html:57, L03.html:57) is M4's term, attributed to M4 Lesson 1, and is not the M6 concept 'Measure and probability space'. Bernoulli's inequality is not a registered concept. All are prose-only under the Architect default.")
R("PC3a-canon-misconceptions-problems-counts", "2.9 structure: misconception and problem counts", "L01.html:326-449; L02.html:376-493; L03.html:343-459", P,
  O + "scans_a_r7.out: L01 13 problems and 13 solutions (M 3, P 3, E 4, R 3), 3 misconceptions; L02 12 and 12 (M 3, P 3, E 3, R 3), 3 misconceptions; L03 12 and 12 (M 3, P 3, E 3, R 3), 3 misconceptions. Every tier has at least three problems.")
R("PC3a-hours-declared", "2.9 structure: lesson hours declared", "L01.html:2, 34; L02.html:2, 34; L03.html:2, 34", P,
  "data-hours=\"6\" on each page (" + O + "scans_a_r7.out) and 'Lesson n of 6 · 6 study hours' in each eyebrow.")
R("PC3a-r4-delta-read", "2.9 change read: every hunk since the round-6 pin", "git diff 4bd8cb94 06994db1 for index.html, L01-L03.html and the three twins", P,
  "Eight hunks in the slice, each read in full: index.html:159 (rung 2 wording) and :167 (hours sentence); L01.html:408 (E2 solution word); L02.html:38 (meta line), :57 (Definition 2.1 positivity), :366 (Section 3 bullet); L03.html:57 (A1 positivity), :286 (Part 3b interpretation). The three twins are unchanged (git diff --quiet exit 0). Each changed claim is re-verified in its own row.")
R("PC3a-r4-cross-references", "2.9 cross-references resolve", "index.html; L01.html:82, 107, 532; L02.html:458, 592; L03.html:316, 345, 509, 518, 537, 542, 568", P,
  O + "links_and_titles_a_r7.out: all hrefs resolve; fragments exist. Section, Remark, Definition, Example, Theorem, Problem and quiz references (Section 2, Section 3, Section 4, Remark 1.6, Remark 2.3, Definition 3.5, Definition 3.7, Theorem 3.8, R1, P2, P3, Examples 2.6-2.9, 3.3, 3.6, 3.10, 3.11) were checked against the labels on the pages.")
R("PC3a-r4-recompute-all-numbers", "2.2 numbers: every number in the slice recomputed by script", "recompute_r7.py; hub_placement_and_scans_r7.py", P,
  O + "recompute_r7.out: 96 of 96 PASS, FAILS []. " + O + "hub_placement_and_scans_r7.out: placement answers and hours arithmetic.")
R("PC3a-r4-restated-M4-concepts", "2.5 DAG: M4 concepts referenced by link, not redefined", "L02.html:57, 67; L03.html:62", P,
  "M4 concepts are linked (conditional-expectation-elementary, expectation, independence). L02 Definition 2.2 gives conditional probability for events, which Remark 2.3 identifies as the elementary case of M4's conditional distribution (course/modules/M/M4/L04.html:139). The Architect rule on prerequisite definitions is respected because the M4 definition is cited, not restated.")
R("PC3a-r4-observations-no-row", "2.4 observations (no defect)", "L01.html:433; tests/labs/PC3/lab-PC3-L02-1.py", P,
  "Observation only: R1's criterion (c) (what changes when the threshold is crossed) is answered by the 'larger possible effect' sentence (L01.html:433). Not a defect.")
R("PC3a-L03-misconception-most-likely", "2.2 misconception: wrong belief and correction", "L03.html:352-353", P,
  "Example 3.11 gives the fair turn that ends at +100 with probability 1/2; zero expectation balances gains and losses and does not rule them out. Correction accurate.")
R("PC3a-L03-def35-next-turn", "2.4 definitions: fairness at histories of fewer than N turns", "L03.html:92 (Definition 3.5), 293 (A3), 300 (H2)", P,
  "Definition 3.5 (92) quantifies histories of fewer than N turns with positive probability, as A3 (293) and H2 (300) do. A2's game satisfies it at every history (97).")

# ---- banned words and round-6 carries ----
R("PC3a-banned-and-process-words", "2.9 banned phrases and process words (learner text)", "L01.html:408 and all four pages", P,
  O + "scans_a_r7.out: zero hits for the banned phrases in visible prose; process words 'build', 'builder', 'round', 'verifier', 'requests', 'unit report', 'fixer', 'ledger' absent from visible text. The raw HTML of the four pages contains no 'round' (the round-6 hit at L01.html:408 is gone). Ellipses appear only in Python code and in KaTeX \\dots, \\cdots and \\ldots.")
R("PC3a-r6-hub-ladder-rung2-wording", "2.9 consistency: hub describes rung 2 as the project does", "index.html:159; course/modules/PC/PC3/project.html:45, 253, 349-350", P,
  "index.html:159 now reads 'left blank (each of the two lines replaced by ___)'. project.html:45 says 'left blank', :253 'blanked with ___', and :349-350 contain 'cash_flow = ___' and 'mark = ___'. The round-6 FAIL is fixed.")
R("PC3a-r6-hub-project-file-names", "2.9 consistency: hub and project name the same student files", "index.html:160, 167; course/modules/PC/PC3/project.html:46, 393, 429-448", F,
  "index.html:160 says 'Write policy.py ... and pnl.py' and :167 says 'The autograded policy.py and pnl.py'. project.html names the one student module market_maker.py (:46, :393, :429-448, with quote(state) and replay(log) at :393-397); grep for policy.py and pnl.py in project.html returns no match. analysis.md is named by both pages. Not fixed in round 7; the defect is still present at this pin.",
  "Change index.html:160 to 'Write market_maker.py, with quote(state), the quoting rule, and replay(log), the replay and the P&L decomposition', and change :167 to match (see PC3a-r7-hub-hours-line-items). If the project owner renames the file instead, the hub must follow the renamed file.")
R("PC3a-r6-hours-curriculum-attribution", "2.9 prose: attribution of the 14-hour project figure", "index.html:167", P,
  "index.html:167 now reads 'The lines sum to 2 + 6 + 4 + 2 = 14 hours, which is 28 percent of the module.' No curriculum-figure attribution remains. curriculum.json PC3 has hours 50 and no project-hours field. The round-6 FAIL is fixed.")
R("PC3a-r6-def21-m4-weights-positivity", "2.4 attribution: the definition cited to M4 Lesson 1", "L02.html:57 (Definition 2.1); L03.html:57 (Assumption A1)", P,
  "Both now read 'weights p(omega) > 0'. M4 Lesson 1 states 'weights p(omega) > 0' (course/modules/M/M4/L01.html, Section 1, first paragraph). The round-6 FAIL is fixed.")

# ---- round-7 new rows ----
R("PC3a-r7-hub-skill-check-bid-ask", "2.9 prose and arithmetic: skill-check convention for a maker's fill", "index.html:129, 131", F,
  "index.html:129: 'a market maker buys one unit at an ask of 10 005 cents'; :131: 'A buy fill pays the ask'. The model's convention is the opposite. A customer who sells gives the maker one unit at the bid, so the maker buys at the bid (course/modules/PC/PC3/L04.html, the customer-side rules: 'A customer who sells gives the maker one unit at the bid, so sigma = +1, f = b'). project.html maker_side: '+1 when the maker buys one unit at the bid, -1 when it sells one at the ask'. A maker that buys at its own ask does not occur in the model. The cash-flow answer -10005 and the mark 10040 are arithmetically right.",
  "index.html:129: 'a market maker buys one unit at a bid of 10 005 cents'. index.html:131: 'A fill in which the maker buys pays its bid, so the cash flow is -10 005 cents.' Keep the answer -10005 and the data-answer.")
R("PC3a-r7-hub-hours-line-items", "2.6 hours: the project's line items against the project time budget", "index.html:167; course/modules/PC/PC3/project.html (Time budget table)", F,
  "index.html:167 gives four lines (2, 6, 4, 2) and says 'the autograded policy.py and pnl.py take 6 hours'. project.html Time budget: rung 1 1 h, rung 2 1 h, quoting rule 3 h, replay 2 h, autograder runs 2 h, analysis 4 h, self-assessment 1 h, total 14 h (" + O + "hub_placement_and_scans_r7.out). The quoting rule and the replay take 5 h, not 6, and the 1 h self-assessment is not in the hub's breakdown. The total of 14 agrees; the line items do not.",
  "Replace the sentence at index.html:167 with: 'Rungs 1 and 2 take 2 hours (1 each). The quoting rule and the replay take 5 hours (3 and 2). The autograder runs take 2 hours. The analysis takes 4 hours. The self-assessment takes 1 hour. The lines sum to 2 + 5 + 2 + 4 + 1 = 14 hours, which is 28 percent of the module.'")
R("PC3a-r7-hub-autograder-seeds", "2.9 prose: what the autograder runs", "index.html:55 (objective 7), index.html:160", F,
  "index.html:55 says 'pass the autograder on seeds 0 to 49'; index.html:160 says 'The autograder runs them on seeds 0 to 49'. project.html Grading mode (line 397): 'Eight checks run on each of 52 seeds, the fixed seeds 0 to 49, your seed and your seed plus 7919'. The hub omits the workspace seed and seed + 7919, which the grade uses.",
  "index.html:160: 'The autograder runs them on seeds 0 to 49, on your own workspace seed, and on that seed plus 7919.' index.html:55: 'pass the autograder on seeds 0 to 49 and on your own workspace seed.'")
R("PC3a-r7-L02-timed-drill-budget", "2.9 structure: the curriculum lab's timed element and the Architect-default budget", "L02.html:132-134 (lab hypothesis), 359 (interpretation); curriculum/06-profession-capstone.yaml:174; plans/PC3-build-plan.md section 0.3 B2 and section 12 Q2", F,
  "The curriculum lab is 'Timed probability drill set with spaced repetition' (curriculum/06-profession-capstone.yaml:174). Plan section 0.3 B2 default, which the Architect's binding rule follows where the plan states a recommendation: 'timed' means a stated per-item time budget (for example 60 seconds) kept on the student's own clock, with no JavaScript timer, and 'the page says so'. L02.html never uses 'timed' or states a budget (grep: no match in L02.html; index.html uses 'timed' only for coding). The lab hypothesis (134) and the interpretation (359) describe an untimed set of 12 generated items.",
  "In the hypothesis paragraph at L02.html:134, after 'a seeded drill set of 12 generated items', add: 'The drill set is timed by a budget you keep on your own clock: stated here as 60 seconds per item, with no timer on this page; the lab counts answers and does not measure time.' This is prose outside the code block, so embed_labs need not rerun; run check_pages afterwards.")

out = {
    "unit": "PC3",
    "slice": "PC3-a",
    "round": 7,
    "verifier": "Claude Haiku 5.5, independent verifier PC3 slice a, round 7 (did not build PC3; no shared context with the builders)",
    "pin": "06994db1 (06994db16d1ab449bcf29898a7f56cfa999dce57), detached",
    "base": "4bd8cb9 (the round-6 pin, 4bd8cb94a8e171e80c4c34da1b3f32be7cb93f07). Delta for the slice: eight hunks in index.html (2), L01.html (1), L02.html (3), L03.html (2); the three lab twins are byte-identical. Every row was re-verified this round; no round-6 PASS row was carried, because each subject changed or was re-read.",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE7-PC3-a (detached at 06994db1; .venv symlinked to /Users/billyribeiro/dev/quant-phd/.venv)",
    "scratch": "none outside the checkout: every script and output is under ledgers/PC3/scripts/PC3-a-r7/ (outputs/ subfolder)",
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "verdict": "FAIL",
    "scope": "course/modules/PC/PC3/index.html, L01.html, L02.html, L03.html and tests/labs/PC3/lab-PC3-L01-1.py, L02-1.py, L03-1.py. Not in this slice: L04-L06, project.html, grader/, cards.json, the project labs. project.html and L04 were read only to check the hub's claims.",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Mutation testing: not applicable. The slice has no project grader; the ruling says lab twins are demonstrations and mutation applies to project graders only. mutants is empty by ruling.",
        "Round-6 non-PASS rows: PC3a-banned-and-process-words, PC3a-r6-hub-ladder-rung2-wording, PC3a-r6-hours-curriculum-attribution, PC3a-r6-def21-m4-weights-positivity are fixed and PASS here. PC3a-r6-hub-project-file-names is still FAIL (index.html:160, 167 against project.html).",
        "Page-smoke caution: the first run used path arguments to --pages, which matches no page (the tool compares page stems) and reports PASS vacuously. That run was discarded; the reported run uses the stems index L01 L02 L03 and prints one PASS line per page.",
        "Judgement, not a row: 'finite probability space' (L02.html:57, L03.html:57, Problem bodies) is M4's term attributed to M4 Lesson 1. The M6 concept 'Measure and probability space' is not used.",
        "Judgement, not a row: L02 Definition 2.2 defines conditional probability for events and calls it 'Introduces' (L02.html:38). Remark 2.3 identifies it as the elementary case of M4's conditional distribution, so it is not a restatement of a prerequisite definition.",
        "Clarity, not a row: L03 Problem P2's solution cites '(H2)' for the N = 1 case (L03.html:400), a label of Theorem 3.8 rather than of P2, whose hypothesis is A3. The step is correct under A3.",
        "The plan's Definition-level wording that a stopping rule 'can change the expected payoff of a fair game' (plans/PC3-build-plan.md section 3, L03 paragraph) is false for history-based rules over a finite horizon, and the page correctly proves the opposite (Theorem 3.8). Not a page defect.",
        "Live verification of references ran (network available): verify_refs --unit PC3 live, 2 of 560 entries, 0 problems.",
        "Not checked: visual inspection of screenshots (page_smoke geometry, console and dark-mode checks only); the two reading-list books (cited at book level only; no passage was read, none is claimed); L04-L06 and project.html content beyond the hub's references to it; the grader and project labs (only the tool gates were run for them).",
    ],
    "summary": {},
}
rc = {}
for r in rows:
    rc[r["status"]] = rc.get(r["status"], 0) + 1
out["summary"] = {"rows": len(rows), "pass": rc.get(P, 0), "fail": rc.get(F, 0), "unverifiable": rc.get("UNVERIFIABLE", 0),
                  "mutants": 0, "mutants_killed": 0}
dest = ROOT / "ledgers/PC3/PC3-a.json"
dest.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", dest, out["summary"])
