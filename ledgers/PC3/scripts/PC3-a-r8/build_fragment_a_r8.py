"""Writes ledgers/PC3/PC3-a.json (round 8) from the rows verified in this round. Run from the checkout root."""
import json
import sys

S = "ledgers/PC3/scripts/PC3-a-r8"
OUT = "ledgers/PC3/scripts/PC3-a-r8/outputs"
rows = []


def row(rid, check, location, status, evidence, fix=""):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    rows.append(r)


# ---- gates (2.1, 2.5, 2.6, 2.9) ----
row("PC3a-check-pages", "2.9 structure: check_pages (hub and L01-L03)", "index.html; L01.html; L02.html; L03.html", "PASS",
    f"{OUT}/check_pages.out: 'check_pages PC3: PASS' exit 0, run this round from the 0dee921a checkout (script {S}/run_gates_a_r8.sh).")
row("PC3a-check-dag", "2.9 DAG: check_dag and independent link/anchor/concept scan", "index.html; L01.html; L02.html; L03.html", "PASS",
    f"{OUT}/check_dag.out: 'check_dag PC3: PASS' exit 0. {OUT}/links_dag_a_r8.out (script {S}/links_dag_a_r8.py): no missing file, anchor or concept id; every concept on the four pages is introduced by M4, CS2, FC2, M1, M2, CF1 or AC1 except fermi-estimation and expected-value-game, which PC3 defines on its own pages with dfn.")
row("PC3a-check-projects", "2.6 projects: check_projects (tool result only)", "course/modules/PC/PC3/project.html", "PASS",
    f"{OUT}/check_projects.out: 'check_projects PC3: PASS' exit 0. Project content is outside this slice; the hub's claims about it are checked under PC3a-hub-project-file-names, PC3a-hub-hours-line-items and PC3a-hub-autograder-seeds.")
row("PC3a-run-labs", "2.5 labs: run_labs", "tests/labs/PC3/lab-PC3-L01-1.py, L02-1.py, L03-1.py; L01.html:144-311; L02.html:132-360; L03.html:112-287", "PASS",
    f"{OUT}/run_labs_all.out: 'run_labs PC3: PASS (9/9)' exit 0; run_labs_L01.out, run_labs_L02.out, run_labs_L03.out each 'PASS (1/1)' exit 0.")
row("PC3a-twins-alone", "2.5 labs: each twin alone under python -I -W error", "tests/labs/PC3/lab-PC3-L01-1.py, L02-1.py, L03-1.py", "PASS",
    f"{OUT}/twin_L01.out, twin_L02.out, twin_L03.out: each run as `.venv/bin/python -I -W error <twin>` from /Users/billyribeiro/.fanout/wt/verifyE8-PC3-a with exit=0 and the printed output shown.")
row("PC3a-pytest-labs", "2.5 labs: pytest on the lab cases", "tests/test_labs.py (PC3 cases)", "PASS",
    f"{OUT}/pytest_labs_PC3.out: `pytest tests/test_labs.py -k PC3 -q` -> 9 dots, exit 0; pytest_collect_PC3.out: `tests/test_labs.py: 9` collected.")
row("PC3a-page-smoke", "2.9 page_smoke, run alone on the four slice pages", "index.html; L01.html; L02.html; L03.html", "PASS",
    f"{OUT}/page_smoke_slice.out: `tools/page_smoke.py --unit PC3 --pages index L01 L02 L03` prints PASS for modules/PC/PC3/index.html, L01.html, L02.html and L03.html and 'page_smoke PC3: PASS' exit 0; lab runtimes 0.0 s each (lab-PC3-L01-1, L02-1, L03-1). Console errors, external requests and math rendering are as the tool reports; visual inspection was not performed.")
row("PC3a-ruff-mypy", "2.5 labs: ruff and mypy --no-incremental on the twins", "tests/labs/PC3/lab-PC3-L01-1.py, L02-1.py, L03-1.py", "PASS",
    f"{OUT}/ruff_check.out: 'All checks passed!' (ruff check tests/labs/PC3 tools); ruff_format.out: '9 files already formatted'; mypy_twins.out: `.venv/bin/mypy --no-incremental` 'Success: no issues found in 385 source files'.")
row("PC3a-verify-refs", "2.1 citations: verify_refs offline for the registry", "references/references.json; index.html:177", "PASS",
    f"{OUT}/verify_refs_offline.out: 'offline integrity: 560 entries, 0 problems' exit 0. Live re-resolution was not re-run this round; references/ is byte-identical since the round-7 pin (git diff 06994db1 0dee921a, no references/ hunk). Registry keys zhou2008practical and crack2015heard exist with used_by containing PC3 (references.json; see registry_flags).")

# ---- hub (index.html) ----
row("PC3a-hub-hours", "2.9 hours: the split sums to the declared figure", "index.html:29, 42, 167; L01.html:2; L02.html:2; L03.html:2", "PASS",
    "index.html:29 data-hours-lessons=\"36\" data-hours-project=\"14\"; :42 '36 h lessons · 14 h project (28%)'; 14/50 = 28 percent; 6 lessons x 6 h = 36 (recompute_a_r8.out). L01, L02, L03 data-hours=\"6\" (scans_a_r8.out).")
row("PC3a-hub-placement", "2.4 numbers and answers: placement diagnostic", "index.html:76-136 (ten items)", "PASS",
    f"{OUT}/recompute_a_r8.out: 3.5 (21/6), 0.25, 2 (ln e^2), 3 (derivative of x^3 at 1), 90.909091 (100/1.1 to six places, tolerance 1e-6), -10005 and 10040 (skill checks), 8 of 10 = 80 percent and 7 of 10 = 70 percent. Ten items: eight prerequisite items (M4 x2, M1, M2, CS2, FC2, CF1, AC1) and two data-skill items (index.html:128-137). Item 1 cites PC3 Example 3.3, which is the die (L03.html:79).")
row("PC3a-hub-titles-prereqs", "2.9 structure: hub titles and prerequisite closure", "index.html:35, 61-67", "PASS",
    f"{OUT}/recompute_a_r8.out and ledgers/PC3/scripts/PC3-a-r8/outputs/links_dag_a_r8.out: prerequisite closure computed from curriculum/curriculum.json = {{M4, CS2, FC2, M1, M2, AC1, CF1, CS1, E1, FC1, P0.1}}, the set index.html:35 lists. Curriculum title 'Quant & Finance Interviews', tier U, hours 50 (curriculum.json PC3).")
row("PC3a-hub-objectives", "2.9 prose: objectives match the lessons", "index.html:48-56", "PASS",
    "Objectives 1-6 map to Lesson 1 (Theorem 1.2, Proposition 1.3; L01.html:67-90), Lesson 2 (Propositions 2.4 and 2.5; L02.html:75-100), Lesson 3 (Theorem 3.8 with A3; L03.html:296-311) and Lessons 4-6, which are outside this slice (key terms present in the pages, grep counts this round: 'adverse selection' 2 and P&amp;L 8 in L04; 'monotonic' 6 in L05; 'net present value' 20 and 'sensitiv' 4 in L06). Objective 7 (index.html:55) now names 'seeds 0 to 49 and on your own workspace seed'. It names a subset of the seeds the grade uses (seed plus 7919 is graded too; project.html:397, 442), so it is not false, but it understates the grade. The round-7 fix text was applied as prescribed.")
row("PC3a-hub-lesson-map", "2.9 structure: lesson map cards", "index.html:145-150; L01.html:35, L02.html:35, L03.html:35", "PASS",
    "Card titles at index.html:145-147 equal the h1 of L01, L02 and L03 (L01.html:35, L02.html:35, L03.html:35); card titles for L04-L06 equal their h1 (L04 'Market-making games and inventory risk', L05 'Timed coding interviews', L06 'Technical finance questions and case interviews'). Card body texts for L01-L03 match the sections (Section 1-3 of each page).")
row("PC3a-hub-data", "2.8 data: no dataset and no data-files", "index.html:37, 170-173; tests/labs/PC3/lab-PC3-L01-1.py, L02-1.py, L03-1.py; grader/*.py; project.html", "PASS",
    f"{OUT}/scans_a_r8.out and grep: no data-files attribute on the four pages; project.html contains data-cite only at :714-715 (the reading list); the twins, grader/*.py and project labs contain no open(, read_text, urllib, requests or http. 12 lines of project.html contain 'SIMULATED'.")
row("PC3a-hub-P0.1-claim", "2.9 prose: P0.1 claims", "index.html:35, 74; course/concepts.html:34-47", "PASS",
    "concepts.html:34-47 lists eleven P0.1 entries, each ending 'not yet released' (read this round). No href or data-concept on the four pages points to a P0.1-owned concept (links_dag_a_r8.out).")

# ---- L01 ----
row("PC3a-L01-numbers", "2.2 numbers in prose and rounding", "L01.html:55, 99-100, 107, 137-141, 287-309, 328, 336, 401-415, 433, 447, 462-465", "PASS",
    f"{OUT}/recompute_a_r8.out (script {S}/recompute_a_r8.py): 137 of 138 checks PASS. Covers 12000, 234000, ratio 19.5, ln 19.5 = 2.9704144656 (2.970414465570), factor widths 1.0986, 1.6094, 0.2624, midpoint 52990.5651979671 (52990.57 to 2 dp, 52990.5652 to 4 dp), reductions 0.4054651081, 0.9162907319, 0.1753528875, totals 2.5649, 2.0541, 2.7951, shares 30.8 and 5.9 percent, all six Part 3 remainders and bounds to ten places, the 0.054 and 0.079 ratios, E3 (ln 16.5 = 2.8034, change 0.167054), R1 half-total 1.4852, R3 reductions 0.4055 and 0.9063. The one FAIL in the script is my 5-place check of the E1 ratio, which is 0.94854560...: the page's '0.94854...' is a correct truncation, and its 4-place value 0.9485 is right.")
row("PC3a-L01-proofs", "2.4 mathematics: Theorem 1.2, Proposition 1.3, Theorem 1.5, Remark 1.6, P1-P3", "L01.html:76-80, 92-94, 128-135, 374-391", "PASS",
    "Re-derived this round. Lemma (L01.html:78): ab - a'b' = a(b - b') + b'(a - a') and AB - ab = A(B - b) + b(A - a), each term nonnegative under the stated order. Induction (79) applies the lemma with (a, a', b, b') = (P, L, x_k, l_k) and (A, B, a, b) = (U, u_k, P, x_k), each hypothesis checked. Attainment at the corners. Proposition 1.3 (92-94): ln is additive on positive products. Theorem 1.5 (130): f'(0)=n, f''(t)=n(n-1)(1+t)^(n-2); Lagrange form with xi in (0, x); bound by (1+xi)^(n-2) <= (1+x)^(n-2) for n-2 >= 0. Remark 1.6: n=2 gives equality with x^2; strict for n>=3 since xi < x. P1 (376): 1/l - 1/x = (x-l)/(lx), quotient bound by Theorem 1.2 with 1/b. P2 Bernoulli (383), P3 binomial tail (390) re-derived.")
row("PC3a-L01-A2-false-at-x0", "2.4 mathematics: assumption used only where it holds", "L01.html:115 (A2), 123 (H3), 130 (x = 0)", "PASS",
    "A2 (115) is stated for x != 0; H3 (123) invokes A2 for x > 0 only; the x = 0 case is proved directly at L01.html:130 (both sides 0).")
row("PC3a-L01-grades-lab-only", "2.3 grades: T for proved results, C for lab-printed results", "L01.html:458-465 (key results)", "PASS",
    "Rows 458-462 are T with on-page bases (Theorem 1.2, Proposition 1.3, Theorem 1.5 under A2, Example 1.4 hand product, ln 19.5 via Proposition 1.3). Rows 463-465 (ten-place ln 19.5, the two narrowing reductions, the n=10 x=1/100 remainder and bound) are C and each names Lab 1 Parts 1-3 as its source; the numbers match recompute_a_r8.out.")
row("PC3a-L02-grade-drill-lab-only", "2.3 grades: lab-only result graded C", "L02.html:508", "PASS",
    "L02.html:508 grades 'closed form equals enumeration on 12 of 12 items' as C with source 'Lab 1, Part 1 (seed 0, self-check)'. The twin prints 'closed form equals enumeration on 12 of 12 items' (embed_compare_a_r8.out, L02 expected block line 340).")
row("PC3a-L01-claims", "2.3/2.9 prose claims checked against the proofs and the lab", "L01.html:67-90, 82, 105-107, 113-141, 317-319, 328", "PASS",
    "'Both bounds are attained' (73) matches the attainment argument (79). Order independence and 'lowers the total by exactly the drop' (105) follow from Proposition 1.3. 'A factor whose own width is already small can lower the total by at most that small width' (105) holds because the drop is at most the factor width (recompute_a_r8.out). Section 4 cross-references (82, 332, 495) resolve to s4 (links_dag_a_r8.out).")
row("PC3a-L01-lab-match", "2.5 labs: page code equals twin; expected block equals twin output", "L01.html:144-311; tests/labs/PC3/lab-PC3-L01-1.py", "PASS",
    f"{OUT}/embed_compare_a_r8.out (script {S}/embed_compare_a_r8.py): 'L01: page code == twin: True'; 'expected == twin stdout: True' (26 lines); twin exit 0 under python -I -W error.")
row("PC3a-L01-problems-quiz", "2.9 structure: problem tiers, solutions and quiz", "L01.html:345-451 (13 problems), 470-548 (quiz)", "PASS",
    f"{OUT}/scans_a_r8.out: problems mechanics 3, proof 3, empirical 4, research 3; 13 solutions in details.solution; 10 quiz items (8-15). Quiz keys recomputed: 10 (Q1), 1.386294 (ln 4, tolerance 1e-6), 234000, 0.004622 (remainder 0.0046221254), 52990.5652 (|diff| 2e-6 against tolerance 1e-4), 30.8 percent (Q5 matches E2 and the Part 2 reduction).")
row("PC3a-L01-only-scope", "2.9 scope: the exceptions named to 'only the ordinary order and arithmetic'", "L01.html:55, 82, 314", "PASS",
    "L01.html:55 names the exceptions the lesson uses: the logarithm (Proposition 1.3, Example 1.4), derivatives and the Taylor theorem (Section 3), the binomial theorem (Remark 1.6, P3) and the square root (Example 1.4). The lesson uses no other operation: the proofs and the lab use only products, sums, powers and these functions.")
row("PC3a-L01-twin-docstring-decimals", "2.5 labs: twin docstring matches the code", "tests/labs/PC3/lab-PC3-L01-1.py:1-8, 96", "PASS",
    "Lab docstring (page lines 147-158, byte-identical to the twin by embed_compare_a_r8.out): 'The one float check ... uses a tolerance of 1e-12' and 'Decimal values print to ten places'. The only float check is line 242 (abs(sum(parts) - width) < 1e-12); Part 1, 2 and 3 print with :.10f. Grid is 5^3 = 125 products (line 204), and Part 3 covers six (n, x) pairs (2 x 3 = 6 in the expected block).")
row("PC3a-L01-research-problems", "2.4 mathematics: open problems R1-R3 answers", "L01.html:430-449", "PASS",
    f"{OUT}/recompute_a_r8.out: R1 half of ln 19.5 = 1.4852; ln 5 = 1.6094 exceeds it; ln 3 = 1.0986 and ln 1.3 = 0.2624 do not. R3: ln 3 - ln 1.5 gives reduction 0.4055 for factor A (width 1.0986 larger), ln(2.5/1.01) = 0.9063 for factor B (width 0.9163 smaller), so the claim fails. R2: the proof uses only (H1) and (H2) (L01.html:438-440, and Theorem 1.2 at 71-73).")
row("PC3a-L01-misconception-accuracy", "2.2/2.3 misconception: wrong belief and correction", "L01.html:327-328", "PASS",
    "Changed sentence (quote-updates factor 'refining the quote-updates factor removes the most width', 328). recompute_a_r8.out: drops 0.1753528875 and 0.9162907319, shares 5.9 and 30.8 percent of the baseline 2.9704, and the quote-updates drop is the largest of the three.")
row("PC3a-L01-KR-ln19.5-grade", "2.3 grades: key-results rows 462 and 463", "L01.html:461-463", "PASS",
    "Row 462 'log-error width ln 19.5 ... the sum of the three factor widths' is T (Proposition 1.3 and Example 1.4, proof on this page). Row 463 'ln 19.5 = 2.9704144656, to ten places' is C with source Lab 1, Part 1, a printed floating value; recompute_a_r8.out confirms 2.970414465570.")
row("PC3a-L01-E2-shares", "2.2 numbers: E2 solution (shares of the total width)", "L01.html:405-410", "PASS",
    "E2 (408) gives 0.3085 from four-place values (0.9163/2.9704 = 0.308476), 30.85 percent, which would display as 30.9 percent, then full precision 0.9162907319/2.9704144656 = 0.308472 (30.8 percent) and 0.1753528875/2.9704144656 = 0.059033 (5.9 percent). recompute_a_r8.out: all four PASS. The explanation of why full precision is used is consistent with the arithmetic.")

# ---- L02 ----
row("PC3a-L02-numbers", "2.2 numbers: examples, exercises and key rows", "L02.html:111-130, 398-417, 449-466, 489-493, 503-507", "PASS",
    f"{OUT}/recompute_a_r8.out: two-flip conditionals 1/3 and 1/2 and reverse conditional 1; urn 20 ordered pairs, 3/5, 3/5, 3/10, 3/4 conditional; Monty Hall by independent brute force over (car, pick, host): rule A (1/3, 2/3), rule B (1/2, 1/2); bag 1/2 and 3/4; M1 1/6; M2 29/100 and 15/29; M3 2/5 (12 of 30); E1 57/64 (1 + 6 of 64 excluded); E3 1/6; R3 3/3 = 1. Q-values 0.333333, 0.6, 0.75, 1 and 0.3 match.")
row("PC3a-L02-proofs", "2.4 mathematics: Propositions 2.4 and 2.5, P1-P3", "L02.html:75-100, 423-441", "PASS",
    "Re-derived. Proposition 2.4 (85): Definition 2.2 applied both ways, both conditionals defined by (H1), division by P(B) > 0. Proposition 2.5 (99): B is the disjoint union of B and A_i by (H1), additivity, Definition 2.2 with (H2). P1 (426) is an equivalence by multiplying by P(B) > 0. P2 (433) and P3 (440) re-derived.")
row("PC3a-L02-lab-match", "2.5 labs: page code equals twin; expected block equals twin output", "L02.html:132-360; tests/labs/PC3/lab-PC3-L02-1.py", "PASS",
    f"{OUT}/embed_compare_a_r8.out: 'L02: page code == twin: True'; 'expected == twin stdout: True' (32 lines); the expected block has data-tolerance=\"0\" (exact fractions). run_labs_L02.out PASS (1/1).")
row("PC3a-L02-interp-reverse-conditional", "2.2 interpretation: reverse conditional", "L02.html:359", "PASS",
    "L02.html:359 '1/3 against 1 for two flips' matches expected block line 350 (P(both heads | at least one head) = 1/3) and line 352 (P(at least one head | both heads) = 1), as printed by twin_L02.out and embed_compare_a_r8.out.")
row("PC3a-L02-misconceptions-quiz", "2.9 structure: misconceptions and retrieval quiz", "L02.html:376-388; L02.html:517-587", "PASS",
    "Three misconceptions with corrections (Monty Hall 1/2 by symmetry, rule A 2/3 by Example 2.8; the two conditioning events 1/3 and 1/2; P(A|B) = P(B|A) with the two-flip values 1/3 and 1 and Bayes' rule). Quiz: 10 items (scans_a_r8.out); each key checked in recompute_a_r8.out; explanations cite Definition 2.2, Example 2.6, 2.7, 2.8, 2.9, Proposition 2.4 and 2.5 correctly.")
row("PC3a-L02-where-canon-breaks", "2.9 prose: canon-breaks bullets", "L02.html:362-371", "PASS",
    "Bullet 1: 2/3 under rule A and 1/2 under rule B (Example 2.8; recompute_a_r8.out). Bullet 2: Example 2.7 swap symmetry and the blue-first case 3/4 (recompute_a_r8.out). Bullet 3: Example 2.6 gives 1/3 and 1/2 for the two events. Bullet 4: Assumption A1 limits the results to finite spaces (L02.html:62).")
row("PC3a-L02-twin-bag-ball-label", "2.5 labs: twin labels equal the page's examples", "tests/labs/PC3/lab-PC3-L02-1.py Parts 3-4; L02.html:116, 129", "PASS",
    "Twin bags {'bag 1': (3, 1), 'bag 2': (1, 3)} (lab line 268) equal Example 2.9 (L02.html:129). Twin balls r1, r2, r3, b1, b2 with 20 ordered pairs (line 305-306) equal Example 2.7 (L02.html:116).")
row("PC3a-L02-finite-probability-space-redefined", "2.4 definitions: Definition 2.1 attribution to M4 Lesson 1", "L02.html:57; L02.html:62", "PASS",
    "Definition 2.1 reads 'weights p(omega) > 0 that sum to 1'. M4 Lesson 1 states 'weights p(omega) > 0' (course/modules/M/M4/L01.html, grep match 1 this round). The definition is attributed to M4 Lesson 1 by link (L02.html:57).")
row("PC3a-L02-spaced-repetition", "2.9 structure: curriculum lab element 'with spaced repetition'", "L02.html:132-134 (lab hypothesis), 359 (interpretation); L02.html:515 (quiz sentence); curriculum/curriculum.json PC3 'lab' ('Timed probability drill set with spaced repetition.'); course/review.html:7; course/assets/js/fsrs.js", "FAIL",
    "The curriculum's lab for PC3 is 'Timed probability drill set with spaced repetition.' (curriculum.json PC3 entry; plans/PC3-build-plan.md:31). The L02 lab is a seeded drill set whose items are regenerated on each run (lab lines 172-187); it is not scheduled, and no sentence on L02 mentions spacing. The only spacing in the program is the review deck, which is FSRS-4.5 (review.html:7; fsrs.js) and receives the quiz cards (L02.html:515), not the drill items. The architect defaults (plan 0.3 B2, Q2) settle timing, not spacing, so the curriculum element is neither delivered nor stated as a gap on the page.",
    "Either (a) add one sentence to the L02 hypothesis paragraph (L02.html:134) stating that the drill set has no spacing of its own and that spacing for this lesson comes from the review deck (FSRS-4.5) through the quiz cards, or (b) record the gap in plans/PC3-open-items.md for the architect to rule on, or (c) if the architect requires the drill items themselves to be spaced, add them as cards in cards.json (Builder F). Option (a) is a prose change outside the lab code, so embed_labs need not rerun; then run check_pages.")

# ---- L03 ----
row("PC3a-L03-numbers", "2.2 numbers: expectations, continuation values, fee sensitivity, biased-game values", "L03.html:80, 102-104, 322, 329-337, 340-356, 418-432, 441-450, 455-457", "PASS",
    f"{OUT}/recompute_a_r8.out (script {S}/recompute_a_r8.py): E[face] 7/2, E[X+Y] 7, 350 cents, continuation 250, value 1150/3 (383.33; 383.333333 to six places), best of 64 policies 1150/3, stop-on-every-face 350, gain 100/3 (33.33), biased rules 150, 1575/32, 1575/32, 575/8, 625/8 (independent memoised recursion), E2 change -575/8 = -71.875, per-turn 25.")
row("PC3a-L03-proofs", "2.4 mathematics: Proposition 3.2, Theorem 3.8 and proof, Definition 3.7", "L03.html:66-76, 107-110, 296-311", "PASS",
    "Proposition 3.2 (75): distributive law and exchange of finite sums. Theorem 3.8 (307-311): base at N by Definition 3.7 (the rule stops at length N); step: V(h) = W(h) sum P(x|h) + sum x P(x|h) with the first sum 1 and the second 0 by (H2) at a positive-probability history of fewer than N turns; empty history gives E[W] = 0. Re-derived. P2 (400) and P3 (407) re-derived; P3 threshold 100f < 250 holds for f = 1, 2 only (recompute_a_r8.out).")
row("PC3a-L03-A3-zero-probability-histories", "2.4 mathematics: A3 and H2 quantify positive-probability histories only", "L03.html:292-293 (A3), 300 (H2), 308 (proof)", "PASS",
    "A3 (293) states the fairness condition for histories with P(h) > 0; H2 (300) restates it for those histories; the proof (308) states that histories of probability zero add nothing and are not needed.")
row("PC3a-L03-thm-number-3-10", "2.2 cross-references: no Theorem 3.10", "index.html; L01.html; L02.html; L03.html", "PASS",
    "grep -c 'Theorem 3.10' on the four pages: 0 each (this round). Example 3.10 (L03.html:319-323) cites Theorem 3.8 (321-322).")
row("PC3a-L03-adapted-undefined", "2.4 notation and terms: no undefined probabilistic term", "index.html; L01.html; L02.html; L03.html", "PASS",
    "Case-insensitive grep on the four pages for 'adapted', 'filtration', 'sigma', 'martingale', 'stopping time', 'optional stopping', 'Poisson', 'Markov' returned no undefined use (this round, scans_a_r8.out, plus the round-7 grep).")
row("PC3a-L03-each-rule-claim", "2.4/2.9 claim: each of the five rules is a stopping rule of Definition 3.7", "L03.html:321, 552; tests/labs/PC3/lab-PC3-L03-1.py RULES (lines 223-229)", "PASS",
    "L03.html:321 'Each is a stopping rule in the sense of Definition 3.7'. The RULES tuple depends only on the history h (sum(h), h[-1], len(h)), so each rule satisfies (H3); the lab's stopping_expectation stops at HORIZON (line 200), as Definition 3.7 requires.")
row("PC3a-L03-grades-lab-only", "2.3 grades: T for proved results, C for lab-printed results", "L03.html:468-475", "PASS",
    "T rows 468, 469, 470, 473, 475 each have an on-page basis (Proposition 3.2; Theorem 3.8 under A3; Example 3.6 backward induction; Theorem 3.8 with A2 over N = 6; Example 3.3 and Proposition 3.2). C rows 471, 472, 474 name Lab 1 Parts 2, 3 and 3b. Values match the expected block of the twin.")
row("PC3a-L03-any-game-fee", "2.2 numbers: R2 reroll-game gain and fee formula", "L03.html:448-450", "PASS",
    f"{OUT}/recompute_a_r8.out: gain = (sum_f max(100f, 350 - c))/6 - 350 equals 100/3 at c = 100 and 149/2 = 74.5 at c = 1.")
row("PC3a-L03-lab-docstring-two-methods", "2.5 labs: docstring claims match code", "tests/labs/PC3/lab-PC3-L03-1.py docstring and functions; L03.html:114", "PASS",
    "Docstring: Part 2 'by backward induction ... and by enumerating every stopping policy' (backward_induction; policy_value over product((0,1), repeat=6), 64 policies). Part 3 'by two methods that must agree' (stopping_expectation and stopping_by_sequences, both over the same five RULES; the checks at lines 239-243). Part 3b 'by the recursion alone' (lines 244-246 call only stopping_expectation).")
row("PC3a-L03-why-rhetorical-questions", "2.9 prose: why-it-matters paragraphs (no rhetorical question, length)", "L01.html:51; L02.html:51; L03.html:51", "PASS",
    f"{OUT}/scans_a_r8.out: why-it-matters word counts 119 (L01), 117 (L02), 120 (L03), each at most 120 (BUILDER_RULES §4.2). None contains a question mark.")
row("PC3a-L03-numbers-prose-claims", "2.2 prose numbers: 6 x 25, mean 350, 1150/3 - 350", "L03.html:104, 322, 336, 349", "PASS",
    f"{OUT}/recompute_a_r8.out: 6 x 25 = 150; 1575/32, 575/8, 625/8 (biased rules); 350 and 1150/3 (Example 3.6); 1150/3 - 350 = 100/3.")
row("PC3a-L03-quiz", "2.9 structure: retrieval quiz", "L03.html:480-564 (12 items)", "PASS",
    f"{OUT}/scans_a_r8.out: 12 items (8-15). Numeric keys 350, 0.333333 (tolerance 1e-6), 383.333333 (tolerance 1e-4), 250, 50, 150, 7 and 0.333333 verified by recompute_a_r8.out. MC keys: Definition 3.1, Definition 3.5 (zero expected payoff), Theorem 3.8's (H3), faces 1 and 2, and 'yes, in this biased game' (Part 3b) agree with the page.")
row("PC3a-L03-lab-match", "2.5 labs: page code equals twin; expected block equals twin output", "L03.html:112-287; tests/labs/PC3/lab-PC3-L03-1.py", "PASS",
    f"{OUT}/embed_compare_a_r8.out: 'L03: page code == twin: True'; 'expected == twin stdout: True' (30 lines); data-tolerance=\"0\".")
row("PC3a-L03-canon-breaks", "2.9 prose: canon-breaks bullets", "L03.html:330-337", "PASS",
    "Unbounded stopping (no value claimed, Remark 3.9 and Section 4 agree); fairness as a hypothesis (Example 3.10 values verified by recompute_a_r8.out); choice in a non-fair game (Example 3.6, mean 350 cents for the stop payoff, verified).")
row("PC3a-L03-fair-game-before-definition", "2.5/2.9 terms before definition: Definitions 3.5 and 3.7 precede the lab", "L03.html:51, 91-92, 108-110, 112", "PASS",
    "The why paragraph (51) describes a stopping rule and a fair game in plain words and then points to Definition 3.7 and Definition 3.5, which are defined at 108-110 and 91-92, before the lab at 112. No formal use precedes its definition.")
row("PC3a-why-terms-before-definition", "2.9 terms used before definition", "L01.html:51-58; L02.html:38, 51; L03.html:51, 91-92", "PASS",
    "L01: 'Fermi estimate' is defined at 59 (dfn) and introduced in the meta-row as 'defined in Section 1' (L01.html:38); 'factor range' is defined at 59; 'product interval' at 73 and 'log-error width' at 89 precede their use in Example 1.4. L02: conditional probability is introduced by a pointer to Definition 2.2 (38). No term is used before its definition.")
row("PC3a-L03-numbers-key-rows-lab", "2.3 grades: key-results rows 471, 474, 475", "L03.html:471, 474, 475", "PASS",
    "Row 471 (best of 64 policies = 1150/3) is C and matches Lab Part 2 (L03.html:269, the best-of-64 line, matched to the twin output by embed_compare_a_r8.out). Row 474 (biased values) is C and matches Part 3b (L03.html:281-285). Row 475 (two dice = 7) is T (Example 3.3, Proposition 3.2) with the lab line 257 as a check.")

# ---- notation, DAG, structure, prose ----
row("PC3a-notation", "2.4 notation: registered symbols and macros", "index.html; L01.html; L02.html; L03.html; notation/notation.json", "PASS",
    f"{OUT}/scans_a_r8.out and {OUT}/recompute_a_r8.out: macros used on the four pages are \\E (32), \\Prob (143), \\R (2), \\indic (2), all registered in notation/notation.json:macros; every other macro is standard LaTeX. No registered symbol is used with another meaning: T is not used, \\Phi, \\gamma, R^\\ast, R^{{e\\ast}}, R_f and \\mathbb{{Q}} do not appear (plan §2.3). N is defined where first used (L03 Definition 3.7), which notation.json 'about' permits for N. Local symbols L, Q and W are not registered; see notes.")
row("PC3a-dag-prose-only-terms", "2.9 DAG: concepts outside the closure appear only as prose", "index.html:148; L01.html (misconception 2); L02.html:57, Problem P2; L03.html:57", "PASS",
    "'adverse selection' (outside the closure) appears only once, in the hub's L04 card (index.html:148), as plain prose with no link and no dfn (grep count 1). The other terms in the slice that name M4 or M1 items are linked to their concept-index entries (links_dag_a_r8.out).")
row("PC3a-canon-misconceptions-problems-counts", "2.9 structure: misconception and problem counts", "L01.html:326-449; L02.html:376-493; L03.html:343-459", "PASS",
    f"{OUT}/scans_a_r8.out: L01 13 problems and 13 solutions (mechanics 3, proof 3, empirical 4, research 3), 3 misconceptions; L02 12 solutions (mechanics 3, proof 3, empirical 3, research 3), 3 misconceptions; L03 12 solutions (3, 3, 3, 3), 3 misconceptions. Section order per BUILDER_RULES §4.2 (why, core, labs, canon breaks, misconceptions, problems, key results, quiz, references) is the order in each page's section list.")
row("PC3a-hours-declared", "2.9 structure: lesson hours declared", "L01.html:2, 34; L02.html:2, 34; L03.html:2, 34", "PASS",
    f"{OUT}/scans_a_r8.out: data-hours=\"6\" on each page and 'Lesson n of 6 · 6 study hours' in each eyebrow.")
row("PC3a-r4-delta-read", "2.9 change read: every hunk since the round-7 pin", "git diff 06994db1 0dee921a for index.html, L01.html, L02.html and the three twins", "PASS",
    "Hunks read in full. index.html: :36 (project meta-row wording), :55 (objective 7), :129 and :131 (skill-check bid), :160 (rung 3) and :167 (hours). L01.html:328 (quote-updates wording). L02.html:134 (timed budget). The three twins are byte-identical to the round-7 pin (git diff --quiet).")
row("PC3a-r4-cross-references", "2.9 cross-references resolve", "index.html; L01.html:82, 107, 532; L02.html:458, 592; L03.html:316, 345, 509, 518, 537, 542, 568", "PASS",
    f"{OUT}/links_dag_a_r8.out: no missing file or anchor on the four pages. Section, Remark, Definition, Example, Theorem, Proposition and Problem references (L01 Section 4 at 82 resolves to s4 at 314; L03 Section 4 at 316 resolves to s4 at 331) point to existing labels.")
row("PC3a-r4-recompute-all-numbers", "2.2 numbers: every number in the slice recomputed by script", "recompute_a_r8.py; scans_a_r8.py", "PASS",
    f"{OUT}/recompute_a_r8.out: 137 of 138 PASS; the single FAIL is a rounding check of mine on the E1 ratio that the page renders correctly as a truncation (see PC3a-L01-numbers).")
row("PC3a-r4-restated-M4-concepts", "2.5 DAG: M4 concepts referenced by link, not redefined", "L02.html:57, 67; L03.html:62", "PASS",
    "M4 concepts are linked (conditional-expectation-elementary, expectation, independence). L02 Definition 2.2 gives conditional probability for events, and Remark 2.3 identifies it as the elementary case of M4's conditional distribution rather than restating it.")
row("PC3a-r4-observations-no-row", "2.4 observations (no defect)", "L01.html:433; tests/labs/PC3/lab-PC3-L02-1.py", "PASS",
    "Observation only: R1's criterion (c) (what changes when the threshold is crossed) is answered by the 'larger possible effect' sentence (L01.html:433). Not a defect.")
row("PC3a-L03-misconception-most-likely", "2.2 misconception: wrong belief and correction", "L03.html:352-353", "PASS",
    "Example 3.11 gives the fair turn that ends at +100 with probability 1/2; zero expectation balances gains and losses and does not rule them out. Correction is correct.")
row("PC3a-L03-def35-next-turn", "2.4 definitions: fairness at histories of fewer than N turns", "L03.html:92 (Definition 3.5), 293 (A3), 300 (H2)", "PASS",
    "Definition 3.5 (92) quantifies histories of fewer than N turns with positive probability, as A3 (293) and H2 (300) do. A2's game satisfies it at every history with positive probability (L03.html:97).")
row("PC3a-banned-and-process-words", "2.9 banned phrases and process words (learner text)", "L01.html, L02.html, L03.html, index.html", "PASS",
    f"{OUT}/scans_a_r8.out (script {S}/scans_a_r8.py): zero hits for the banned phrases in visible prose (TODO, TBD, lorem, for brevity, beyond the scope, roughly half, historically, about 6 percent, it is important to note, studies show, experts agree, it is well known, obviously, clearly, it can be shown, ellipsis) and zero hits for process words (builder, verif, ledger, agent, round, fragment, audit, mutant, blocking, plan, architect). One hit for 'Verify it by counting the complement' (L02.html E1) is a learner instruction, not a process word.")
row("PC3a-r6-hub-ladder-rung2-wording", "2.9 consistency: hub describes rung 2 as the project does", "index.html:159; course/modules/PC/PC3/project.html:45, 253, 349-350", "PASS",
    "index.html:159 reads 'left blank (each of the two lines replaced by ___)'. project.html:45 says 'left blank', :253 'blanked with ___'. Consistent.")
row("PC3a-r6-hub-project-file-names", "2.9 consistency: hub and project name the same student files", "index.html:160, 167; course/modules/PC/PC3/project.html:46, 393, 429-448", "PASS",
    "Round-6 FAIL is fixed. index.html:160 reads 'Write market_maker.py, with quote(state), the quoting rule, and replay(log), the replay and the P&L decomposition'; :167 names quote and replay in market_maker.py. project.html:46 and :393 name market_maker.py with quote(state) and replay(log); project.html:429 names quote and replay in the same file. grep for policy.py and pnl.py over index.html and L01-L03 returns 0 (this round).")
row("PC3a-r6-hours-curriculum-attribution", "2.9 prose: attribution of the 14-hour project figure", "index.html:167", "PASS",
    "index.html:167 reads 'The lines sum to 1 + 1 + 3 + 2 + 2 + 4 + 1 = 14 hours, which is 28 percent of the module.' No curriculum-figure attribution remains; the 14 is the project's own budget table (project.html:434, 'Equals the project hours in the hub').")
row("PC3a-r6-def21-m4-weights-positivity", "2.4 attribution: the definition cited to M4 Lesson 1", "L02.html:57 (Definition 2.1); L03.html:57 (Assumption A1)", "PASS",
    "Both read 'weights p(omega) > 0'. M4 Lesson 1 states 'weights p(omega) > 0' (course/modules/M/M4/L01.html; grep match this round).")
row("PC3a-r7-hub-skill-check-bid-ask", "2.9 prose and arithmetic: skill-check convention for a maker's fill", "index.html:129, 131", "PASS",
    "Round-7 FAIL is fixed. index.html:129 now reads 'a market maker buys one unit at a bid of 10 005 cents' and :131 'A fill in which the maker buys pays its bid, so the cash flow is -10 005 cents'. Consistent with project.html:112-117 (maker_side: +1 when the maker buys one unit at the bid), project.html:406 ('a maker purchase at the bid b changes cash by -b'), and the answer -10005 (data-answer) is right.")
row("PC3a-r7-hub-hours-line-items", "2.6 hours: the project's line items against the project time budget", "index.html:167; course/modules/PC/PC3/project.html:421-435 (Time budget table)", "PASS",
    "Round-7 FAIL is fixed. index.html:167 lines 1 (rung 1), 1 (rung 2), 3 (quote), 2 (replay), 2 (autograder), 4 (analysis), 1 (self-assessment) equal project.html:427-433 rows exactly. Sum 14 equals project.html:434 and 28 percent of 50 (recompute_a_r8.out: 1+1+3+2+2+4+1 = 14).")
row("PC3a-r7-hub-autograder-seeds", "2.9 prose: what the autograder runs", "index.html:55 (objective 7), index.html:160", "PASS",
    "Round-7 FAIL is fixed. index.html:160 reads 'The autograder runs them on seeds 0 to 49, on your own workspace seed, and on that seed plus 7919', matching project.html:397 ('Eight checks run on each distinct seed of the set, which holds the fixed seeds 0 to 49, your seed and your seed plus 7919') and project.html:442. Objective 7 is discussed in PC3a-hub-objectives.")
row("PC3a-r7-L02-timed-drill-budget", "2.9 structure: the curriculum lab's timed element and the Architect-default budget", "L02.html:132-134 (lab hypothesis), 359 (interpretation); curriculum.json PC3 'lab'; plans/PC3-build-plan.md §0.3 B2 and §12 Q2", "PASS",
    "Round-7 FAIL is fixed. L02.html:134 now reads 'The drill set is timed by a budget you keep on your own clock, stated here as 60 seconds per item, with no timer on this page; the lab counts the items on which the two methods agree and does not measure time.' This is the plan's B2 default (plan §0.3 B2: 'a stated per-item time budget (for example 60 seconds)' kept by the student's own clock, no JavaScript timer). The lab does not measure time (L02 code, lines 190-220). Interpretation at 359 is consistent. The separate spaced-repetition element is PC3a-L02-spaced-repetition.")

# ---- verdict and summary ----
counts = {"PASS": 0, "FAIL": 0, "UNVERIFIABLE": 0}
for r in rows:
    counts[r["status"]] += 1
verdict = "PASS" if counts["FAIL"] == 0 and counts["UNVERIFIABLE"] == 0 else "FAIL"

frag = {
    "unit": "PC3",
    "slice": "PC3-a",
    "round": 8,
    "verifier": "Claude Haiku 5.5, independent verifier PC3 slice a, round 8 (did not build PC3; no shared context with the builders)",
    "pin": "0dee921a33dc1275ff9b1babc6c2fdf3daac62c3 (detached)",
    "base": "06994db16d1ab449bcf29898a7f56cfa999dce57 (the round-7 pin). Delta for the slice: index.html (4 hunks at :36, :55, :129-131 and :160-167), L01.html (1 hunk at :328), L02.html (1 hunk at :134); the three lab twins and L03.html are byte-identical. Every round-7 row id is kept. Rows whose subject changed were re-verified; L03 was re-read in full this round, so no row is carried from round 7.",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE8-PC3-a (detached at 0dee921a; .venv symlinked to /Users/billyribeiro/dev/quant-phd/.venv)",
    "scratch": "none outside the checkout: every script and output is under ledgers/PC3/scripts/PC3-a-r8/ (outputs/ subfolder)",
    "verified_at": "2026-11-05T01:44:17+00:00",
    "verdict": verdict,
    "scope": "course/modules/PC/PC3/index.html, L01.html, L02.html, L03.html and tests/labs/PC3/lab-PC3-L01-1.py, L02-1.py, L03-1.py. Not in this slice: L04-L06, project.html, grader/, cards.json, the project labs (project.html and L04-L06 were read only to check the hub's claims).",
    "rows": rows,
    "mutants": [],
    "registry_flags": [
        "crack2015heard (references/references.json): publisher string '[Timothy Falcon Crack]' carries brackets and the source string says '16th ed.' while the record has no edition; zhou2008practical: publisher 'Lulu,]' has a stray bracket. Both are the known B4 items (plan §0.3 B4). Registry records are not edited by this verifier; the registry owner should correct the publisher strings.",
    ],
    "freshness_flags": [
        "No 2025-2026 work is cited in the slice. PC3 cites two books at book level (zhou2008practical, crack2015heard) and no passage. Not applicable to a debate brief (PC3 curriculum entry has no debate field).",
    ],
    "notes": [
        "Mutation testing: not applicable. The slice has no grader; the ruling says lab twins are demonstrations. mutants is empty by ruling.",
        "Round-7 FAIL rows fixed and re-verified PASS: PC3a-hub-objectives (objective 7 now names the workspace seed; a subset of the graded seeds, noted), PC3a-r6-hub-project-file-names, PC3a-r7-hub-skill-check-bid-ask, PC3a-r7-hub-hours-line-items, PC3a-r7-hub-autograder-seeds, PC3a-r7-L02-timed-drill-budget.",
        "Still FAIL, new in this round's reading of the curriculum: PC3a-L02-spaced-repetition. The curriculum lab text includes 'with spaced repetition'; the page's drill set is not spaced and the page does not say so. The architect may rule the element out of scope; if so, the page needs one honest sentence.",
        "Notation (judgement, not a registry row): the local letters L (L01 Theorem 1.2 proof, product of lower ends) and W (L03 total paid, Definition 3.7 and Theorem 3.8) are reused in L04 for inventory limit and mark-to-market wealth (plan §2.3 lists L as the L04 inventory limit). Neither letter is registered in notation/notation.json, so no FAIL row is raised. The builder of L04 should choose other letters or state the lesson-local meaning.",
        "Reference (not a row): L03 Problem P2 and Remark 3.9 cite '(H2)' as the fairness hypothesis of Theorem 3.8 in a proof that has its own hypotheses list; the citation is correct but could name Theorem 3.8's H2 explicitly.",
        "Scope note: L01-L03 quiz items point to cards.json (data-cards). Cards are not in this slice; cards.json changed in the delta only for L06 (git diff 06994db1 0dee921a -- course/modules/PC/PC3/cards.json). The 25 L01, 23 L02 and 29 L03 cards were not verified in this round.",
        "Lab sample count: the twins are demonstrations, so the 20-seed instance sample, the five alternative implementations and the grader mutation rules do not apply to slice a.",
        "Live verify_refs was not re-run this round; the offline integrity gate passed and no reference or registry file changed since the round-7 pin.",
    ],
    "summary": {
        "rows": len(rows),
        "pass": counts["PASS"],
        "fail": counts["FAIL"],
        "unverifiable": counts["UNVERIFIABLE"],
        "mutants_killed": 0,
        "mutants_total": 0,
        "recompute": "137 of 138 PASS in recompute_a_r8.py; the one FAIL is my own rounding check of the E1 ratio, which the page renders as a correct truncation",
    },
}

problems = []
for r in rows:
    if r["status"] != "PASS" and not r.get("fix"):
        problems.append(r["id"])
path = "ledgers/PC3/PC3-a.json"
with open(path, "w", encoding="utf-8") as fh:
    json.dump(frag, fh, ensure_ascii=False, indent=2)
    fh.write("\n")
print("rows", len(rows), counts, "verdict", verdict, "problems", problems)
