"""Round-10 PC3 slice a: writes the ledger fragment ledgers/PC3/PC3-a.json from the outputs in outputs/."""
import datetime
import json
import pathlib

ROOT = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyE10-PC3-a")
S = "ledgers/PC3/scripts/PC3-a-r10"
O = f"{S}/outputs"
GATES = f"{S}/run_gates.sh (outputs {O}/<name>.out; exit codes {O}/exit_codes.txt)"

rows = []


def row(rid, check, location, evidence, status="PASS", fix=None):
    item = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        item["fix"] = fix
    rows.append(item)


# ---- commands and labs
row("PC3a-check-pages", "2.9 structure: check_pages --unit PC3 (hub and L01-L03 checked, round 10)",
    "index.html; L01.html; L02.html; L03.html",
    f"{GATES}: check_pages.out = 'check_pages PC3: PASS', exit 0.")
row("PC3a-check-dag", "2.9 DAG: check_dag --unit PC3 and an independent link scan",
    "index.html; L01.html; L02.html; L03.html",
    f"check_dag.out = 'check_dag PC3: PASS', exit 0. Independent grep: every data-concept link in L01-L03 is in the closure "
    "(exponential-and-logarithm, taylor-theorem, conditional-expectation-elementary, independence, expectation); fermi-estimation "
    "(L01) and expected-value-game (L03) are each defined once with a dfn; no other data-concept dfn on the slice pages.")
row("PC3a-check-projects", "2.6 projects: check_projects --unit PC3 (tool result only; project pages not in this slice)",
    "course/modules/PC/PC3/project.html", f"check_projects.out = 'check_projects PC3: PASS', exit 0 ({GATES}).")
row("PC3a-run-labs", "2.5 labs: run_labs --unit PC3 (page code equals twin; expected block equals output)",
    "tests/labs/PC3/lab-PC3-L01-1.py, lab-PC3-L02-1.py, lab-PC3-L03-1.py; L01.html:144-311; L02.html:132-360; L03.html:112-287",
    f"run_labs.out = 'run_labs PC3: PASS (9/9)', exit 0 ({GATES}).")
row("PC3a-twins-alone", "2.5 labs: each slice twin alone under python -I -W error, no network",
    "tests/labs/PC3/lab-PC3-L01-1.py, L02-1.py, L03-1.py",
    f"Copied each twin to a fresh /tmp directory and ran it with python -I -W error: exit 0 for all three, stderr 0 bytes, "
    f"stdout in {O}/twin-L0x-1.stdout (26, 32 and 30 lines). Imports are __future__, math, random, fractions, itertools, "
    "dataclasses, collections.abc only (grep of import lines).")
row("PC3a-pytest-labs", "2.5 labs: pytest -k PC3 (tests/test_labs.py PC3 cases)",
    "tests/test_labs.py (PC3 cases)", f"{O}/pytest_pc3.out: 9 tests passed, exit 0 (.venv/bin/pytest -q -k PC3).")
row("PC3a-page-smoke", "2.9 page_smoke, run alone on the four slice pages",
    "index.html; L01.html; L02.html; L03.html",
    f"{O}/page_smoke.out: each of the four pages PASS; 'page_smoke PC3: PASS', exit 0 (zero console errors, no external "
    "requests, no horizontal scroll at 360 px, KaTeX parses). Lab timings 0.0 s.")
row("PC3a-ruff-mypy", "2.5 labs: ruff check, ruff format --check and mypy --no-incremental on the twins",
    "tests/labs/PC3/lab-PC3-L01-1.py, L02-1.py, L03-1.py",
    f"{O}/ruff_check.out 'All checks passed!'; ruff_format.out '9 files already formatted'; mypy.out "
    "'Success: no issues found in 9 source files'; all exit 0.")
row("PC3a-verify-refs", "2.1 citations: verify_refs --offline (registry integrity)",
    "references/references.json; index.html:177",
    f"{O}/verify_refs_offline.out: 'offline integrity: 560 entries, 0 problems', exit 0. Live Crossref run not repeated "
    "(offline gate only, as in round 9). The slice cites no registry key for a published claim; index.html:177 names the two keys at book level.")

# ---- hub (index.html)
row("PC3a-hub-hours", "2.9 structure: the hours split sums to the declared figure",
    "index.html:29, 42, 167; L01.html:34; L02.html:34; L03.html:34",
    "index.html:42 '36 h lessons · 14 h project (28%)'; index.html:167 '1 + 1 + 3 + 2 + 2 + 4 + 1 = 14' (seven lines, changed in round 10). "
    "project.html:422-434 table has the same seven lines (1, 1, 3, 2, 2, 4, 1) and 'Total 14'. 6 x 6 = 36, 36 + 14 = 50; "
    "data-hours-lessons=36 and data-hours-project=14 on the hub; data-hours=6 on L01-L03.")
row("PC3a-hub-placement", "2.2/2.4 numbers and answers: placement diagnostic, ten items",
    "index.html:76-136 (data-answer values, data-mastery 0.8)",
    f"{S}/numbers_r10.py and {O}/numbers_r10.out: E[face]=21/6=7/2; P(both heads)=1/4; ln(e^2)=2; d/dx x^3 at 1 = 3; "
    "100/1.1 = 90.9090909 -> 90.909091; balance sheet A = L + E; cost of carry S e^{r tau}; binary search O(log n). "
    "Eight prerequisite items (M4 x2, M1, M2, CS2, FC2, CF1, AC1) and two skill checks (-10005, 10040). 7 numeric + 3 mc = 10 items; "
    "8 of 10 = 80 percent and 7 of 10 = 70 percent.")
row("PC3a-hub-titles-prereqs", "2.9 structure: hub titles and prerequisite closure",
    "index.html:35, 61-67",
    "index.html:35 lists M4, CS2, FC2 and the closure M1, M2, AC1, CF1, CS1, E1, FC1, P0.1: together the 11-module closure of "
    "plans/PC3-build-plan.md §0.2 (AC1, CF1, CS1, CS2, E1, FC1, FC2, M1, M2, M4, P0.1). The hub's concept hrefs are 13 unique "
    "concepts.html#<id> targets, each present as id= in course/concepts.html (grep, round 10).")
row("PC3a-hub-objectives", "2.9 prose: the seven objectives match the lessons",
    "index.html:48-56",
    "index.html:49-55: L01 bound and log-error width (Theorem 1.2, Proposition 1.3); L02 conditional probability, Bayes' rule and the "
    "law of total probability (Definition 2.2, Propositions 2.4-2.5); L03 expected payoff, fairness and the stopping result "
    "(Definition 3.1, Theorem 3.8); L04-L06 and the project named (outside this slice; checked for the hub claims only). Seven items, inside 4-8.")
row("PC3a-hub-lesson-map", "2.9 structure: lesson map cards link every lesson",
    "index.html:145-150; L01.html:35, L02.html:35, L03.html:35",
    "index.html:145-150 map L01-L06 at 6 h each with hrefs L01.html..L06.html (all present); the L01-L03 titles match the map "
    "('Fermi Estimation and Mental Math', 'Probability Puzzles and Conditional Reasoning', 'Expected-Value Games').")
row("PC3a-hub-data", "2.8 data: no dataset and no data-files on any slice page or lab",
    "index.html:37, 170-173; tests/labs/PC3/lab-PC3-L01-1.py, L02-1.py, L03-1.py",
    "grep -c data-files on index.html and L01-L03.html: 0 each. Twins contain no open( or network import (grep). index.html:37 says "
    "the L04 and project games are SIMULATED: L04.html has 10 SIMULATED labels (grep -c). index.html:37 says the L03 games are fixed "
    "with no randomness: lab-PC3-L03-1.py docstring 'No randomness and no network', and FAIR_GAME and BIASED_GAME are constants.")
row("PC3a-hub-P0.1-claim", "2.9 prose: the P0.1 claims",
    "index.html:35, 74; course/concepts.html:34-47",
    "concepts.html:34-47: every P0.1 entry reads 'not yet released', as index.html:35 says. grep for concepts.html#p0 or a P0.1 "
    "data-concept on index.html and L01-L03: 0 hits (greps_r10.out). None of the ten placement items tests P0.1 (index.html:76-136).")

# ---- L01 (full read; every number recomputed)
row("PC3a-L01-numbers", "2.2 numbers in prose and rounding (whole page)",
    "L01.html:55, 99-100, 107, 137-141, 287-309, 328, 336, 401-415, 433, 447, 462-465",
    f"{O}/numbers_r10.out: bounds 12000 and 234000; ratio 19.5; ln 19.5 = 2.9704144656; geometric midpoint 52990.5651979671 "
    "-> 52 990.57 (2 dp), 52990.5652 (4 dp); factor widths 1.0986, 1.6094, 0.2624; reductions 0.4054651081, 0.9162907319, "
    "0.1753528875 -> 0.4055, 0.9163, 0.1754; totals 2.5649, 2.0541, 2.7951; quote share 30.8 percent; minutes share 5.9 percent. "
    f"{O}/ratio_check.out and numbers_r10.out: Example 1.7 remainder 0.0046221254, bound 0.0048728552, ratio 0.948545615 "
    "(0.9485 at 4 dp; 0.94854... is its prefix), bound/remainder - 1 = 0.054246 (5.4 percent), (1.01)^10 = 1.1046221254; "
    "x = 1/20: (1.05)^10 = 1.6288946268 -> 1.6289, remainder 0.1288946268 -> 0.1289, bound 0.1662137374 -> 0.1662, "
    "remainder/exact 0.079130 -> 7.9 percent; ln 16 = 2.7726; ln 16.5 = 2.8034; ln 19.5 - ln 16.5 = 0.167054; "
    "half the total 1.4852; ln 4 = 1.386294 (quiz); 0.004622 (quiz); 52990.5652 (quiz).")
row("PC3a-L01-proofs", "2.4 mathematics: Theorem 1.2, Proposition 1.3, Theorem 1.5, Remark 1.6, problems P1-P3",
    "L01.html:76-80, 92-94, 128-135, 374-391",
    "Re-derived by hand: the lemma a'b' <= ab from ab - a'b' = a(b-b') + b'(a-a') and AB - ab = A(B-b) + b(A-a), both terms "
    "nonnegative under the stated positivity; the induction step applies the lemma to (P, L, x_k, l_k) and (U, u_k, P, x_k); "
    "attainment at x_i = l_i and u_i. Prop 1.3: product of ratios and ln(ab) = ln a + ln b. Thm 1.5: f'' = n(n-1)(1+t)^{n-2}, "
    "Lagrange form, 0 <= (1+xi)^{n-2} <= (1+x)^{n-2}. P1: 1/l - 1/x = (x-l)/(lx). P2: (1+x)(1+nx) = 1 + (n+1)x + nx^2. "
    "P3 binomial tail. M3: remainder 31/1000, bound 33/1000 (numbers_r10.out). All correct.")
row("PC3a-L01-A2-false-at-x0", "2.4 mathematics: assumption used only where it holds",
    "L01.html:115 (A2), 123 (H3), 130 (x = 0)",
    "A2 needs x != 0 (L01.html:115); Theorem 1.5 (H3) applies A2 only for x > 0 (L01.html:123); the proof treats x = 0 directly "
    "(L01.html:130: both sides 0). Correct.")
row("PC3a-L01-grades-lab-only", "2.3 grades: T for proved results, C for lab-printed results",
    "L01.html:458-465 (key results)",
    "Rows 458-462 are T and proved on the page (Theorem 1.2, Proposition 1.3, Theorem 1.5, Example 1.4 by hand). Rows 463-465 are C "
    "and name Lab 1 Parts 1-3 (lab-printed values). Consistent with verifier rules item 9.")
row("PC3a-L02-grade-drill-lab-only", "2.3 grades: lab-only result graded C",
    "L02.html:508",
    "Row 'Generated drill set: the closed form equals the enumeration on 12 of 12 items' is graded C and names Lab 1, Part 1 "
    "(seed 0, self-check); the lab prints 'closed form equals enumeration on 12 of 12 items' (outputs/twin-L02-1.stdout).")
row("PC3a-L01-claims", "2.3/2.9 prose claims checked against the proofs and the lab",
    "L01.html:67-90, 82, 105-107, 113-141, 317-319, 328",
    "Prop 1.3 'exactly the drop' (L01.html:105) holds by Prop 1.3. 'at most that small width' holds (a narrowing removes at most the "
    "width). 'the largest reduction comes from the factor with the largest width' (L01.html:107): widths 1.0986, 1.6094, 0.2624; "
    "reductions 0.4055, 0.9163, 0.1754: quote updates has both the largest width and the largest reduction. 'the bound grows with x' "
    "(L01.html:319): n(n-1)/2 (1+x)^{n-2} x^2 is increasing in x >= 0; it rises from 0.0049 to 0.1662 (numbers_r10.out).")
row("PC3a-L01-lab-match", "2.5 labs: page code equals twin; expected block equals twin output",
    "L01.html:144-311; tests/labs/PC3/lab-PC3-L01-1.py",
    "run_labs PASS (round 10). Twin stdout (26 lines, outputs/twin-L01-1.stdout) matches pre.expected (L01.html:284, "
    "data-tolerance 1e-9), e.g. 'sum equals product log-width: True' and 'grid products inside the bounds: 125 of 125'.")
row("PC3a-L01-problems-quiz", "2.9 structure: problem tiers, worked solutions and quiz",
    "L01.html:345-451 (M1-M3, P1-P3, E1-E4, R1-R3 = 13 problems), 470-548 (10 quiz items)",
    "Counted in outputs/view-L01.txt: Mechanics 3, Proof 3, Empirical 4, Research 3, each with a solution; quiz 10 items (8-15 required).")
row("PC3a-L01-only-scope", "2.9 scope: the exceptions named to 'only the ordinary order and arithmetic'",
    "L01.html:55, 82, 314",
    "L01.html:55 lists the non-arithmetic tools (M1 logarithm, M2 Taylor and derivatives, binomial theorem, square root). Each is used "
    "where stated: Prop 1.3 and Example 1.4 (log), Section 3 (Taylor, A2), Remark 1.6 (binomial), Example 1.4 (square root).")
row("PC3a-L01-twin-docstring-decimals", "2.5 labs: twin docstring matches the code",
    "tests/labs/PC3/lab-PC3-L01-1.py:1-8, 96",
    "Docstring: fractions for bounds and grid; floats for log widths; a 1e-12 float check (code: abs(sum(parts) - width) < 1e-12); "
    "ten-place printing (:.10f). Matches the code.")
row("PC3a-L01-research-problems", "2.4 mathematics: research problems R1-R3 answers",
    "L01.html:430-449",
    "R1 threshold: half of 2.9704 is 1.4852; ln 5 = 1.6094 exceeds it, ln 3 = 1.0986 and ln 1.3 = 0.2624 do not (numbers_r10.out). "
    "The solution names the threshold and its justification; criterion (c) is answered as the dominance of the single factor. "
    "R2: the proof uses only (H1)-(H2): correct. R3 counterexample: ln 3 = 1.0986 > ln 2.5 = 0.9163, while the reduction ln(3/2) = 0.4055 "
    "< ln(2.5/1.01) = 0.906340 (numbers_r10.out).")
row("PC3a-L01-misconception-accuracy", "2.2/2.3 misconception: wrong belief and correction",
    "L01.html:327-328",
    "The correction's values 0.1754 (5.9 percent) and 0.9163 (30.8 percent) match numbers_r10.out; the relative gain depends on the "
    "other factors through the total, as drop/total shows.")
row("PC3a-L01-KR-ln19.5-grade", "2.3 grades: key-results rows 462 and 463",
    "L01.html:461-463",
    "Row 462 T (Proposition 1.3, Example 1.4 by hand); row 463 C names 'Lab 1, Part 1 (printed floating-point value)'; "
    "2.9704144656 = ln 19.5 in numbers_r10.out.")
row("PC3a-L01-E2-shares", "2.2 numbers: E2 solution (shares of the total width); round-9 FAIL re-verified",
    "L01.html:405-410 (E2 solution at 408)",
    "Round-9 FAIL is FIXED. L01.html:408 now reads 'Dividing those four-place values gives 0.308477, or 30.8477 percent, which is "
    "30.85 percent to two places and 30.8 percent to one decimal place.' Recomputed: 0.9163/2.9704 = 0.30847697 -> 0.308477, 30.8477 "
    "percent, 30.85 (2 dp), 30.8 (1 dp) (numbers_r10.out). Full precision: 0.9162907319/2.9704144656 = 0.30847235 -> 0.308472, 30.8 "
    "percent; minutes 0.05903314 -> 0.059033, 5.9 percent. grep '30\\.9' L01.html: 0 hits (greps_r10.out).")
row("PC3a-L01-claims-E1", "2.2 numbers: E1 ratio",
    "L01.html:401-404",
    "remainder/bound = 0.0046221254/0.0048728552 = 0.948545608 (ratio_check.out); the solution's '0.94854...' is its prefix and '0.9485' "
    "is its 4-place value; the lab does not print the ratio, as the solution says.")

# ---- L02
row("PC3a-L02-numbers", "2.2 numbers: examples, exercises and key rows",
    "L02.html:111-130, 398-417, 449-466, 489-493, 503-507",
    f"{O}/numbers_r10.out: P(both heads | >=1 head) = 1/3; P(both | first H) = 1/2; P(>=1 | both) = 1; urn P(second red) = "
    "P(first red) = 3/5, P(both red) = 3/10, P(second red | first blue) = 3/4; bag P(red) = 1/2, P(bag 1 | red) = 3/4; "
    "M1 P(sum 7 | first 3) = 1/6; M2 P(A|B) = 15/29 with P(B) = 29/100; M3 2/5; E1 57/64; Monty rule A (1/3, 2/3), rule B (1/2, 1/2); "
    "E3 difference 1/6. All exact.")
row("PC3a-L02-proofs", "2.4 mathematics: Propositions 2.4 and 2.5, P1-P3 (with the C_i rename)",
    "L02.html:75-100, 423-441",
    "Prop 2.4: both sides of Definition 2.2 equated and divided by P(B) > 0: correct. Prop 2.5 with C_i (H1 partition, H2 P(C_i) > 0): "
    "B is the disjoint union of B and C_i; additivity; Definition 2.2 times P(C_i): correct. P2 and P3 use C_i consistently, and grep "
    "finds no A_i, A_1, A_2 or A_3 left in the proof text (greps_r10.out). P3 additivity of Prob_B: correct.")
row("PC3a-L02-lab-match", "2.5 labs: page code equals twin; expected block equals twin output",
    "L02.html:132-360; tests/labs/PC3/lab-PC3-L02-1.py",
    "run_labs PASS; twin stdout (32 lines, outputs/twin-L02-1.stdout) matches pre.expected (L02.html:327, data-tolerance 0). "
    "Part 1 items 1-12 all 'equal True'; 'closed form equals enumeration on 12 of 12 items'.")
row("PC3a-L02-interp-reverse-conditional", "2.2 interpretation: reverse conditional",
    "L02.html:359",
    "1/3 (P(both | >=1 head)) against 1 (P(>=1 head | both)) for two flips, both printed by Part 4 "
    "(outputs/twin-L02-1.stdout).")
row("PC3a-L02-misconceptions-quiz", "2.9 structure: misconceptions and retrieval quiz",
    "L02.html:376-388; L02.html:517-587",
    "3 misconceptions (L02.html:377, 381, 385); quiz 10 items (lines 518-583), each with an explanation. The renamed quiz item "
    "(L02.html:574-580) is correct; the 3/10 item (583-585) is 6/20 (numbers_r10.out).")
row("PC3a-L02-where-canon-breaks", "2.9 prose: canon-breaks bullets (round-10 hunk at 366)",
    "L02.html:362-371",
    "The changed bullet (L02.html:366) 'Switching wins with probability 2/3 under rule A, and with probability 1/2 under rule B given "
    "that the revealed door hides a goat' matches Example 2.8 and the twin output (rule A 1/3, 2/3; rule B 1/2, 1/2). Bullet 2 "
    "matches Example 2.7 (3/4 against 3/5).")
row("PC3a-L02-twin-bag-ball-label", "2.5 labs: twin labels equal the page's examples",
    "tests/labs/PC3/lab-PC3-L02-1.py Parts 3-4; L02.html:116, 129",
    "Twin Part 3 (bags of 3 red and 1 blue; 1 red and 3 blue) and Part 4 (urn of 3 red and 2 blue) match Examples 2.9 and 2.7.")
row("PC3a-L02-finite-probability-space-redefined", "2.4 definitions: Definition 2.1 attribution to M4 Lesson 1",
    "L02.html:57; L02.html:62",
    "course/modules/M/M4/L01.html:55 defines a finite probability space (weights p(omega) > 0 summing to 1), as cited. The phrase "
    "'probability space' is not linked or dfn'd in PC3; the registered concept probability-space is owned by M6, outside the closure, "
    "and is used as prose only (architect default).")
row("PC3a-L02-spaced-repetition", "2.9 structure: curriculum lab 'timed ... with spaced repetition' (curriculum yaml:174)",
    "L02.html:132-134 (lab hypothesis), 359 (interpretation); L02.html:515; review.html:7, 35",
    "L02.html:134 says the drill set has no spacing of its own; the spacing comes from this lesson's cards via the review deck "
    "(FSRS-4.5; review.html:7 and 35). Honest and consistent with review.html. NOTE for the architect: "
    "curriculum/06-profession-capstone.yaml:174 names the lab 'with spaced repetition'; the page routes the spacing through the cards "
    "(round-9 precedent). Not a page defect.")

# ---- L03
row("PC3a-L03-numbers", "2.2 numbers: expectations, continuation values, fee sensitivity, biased-game values",
    "L03.html:80, 102-104, 322, 329-337, 340-356, 418-432, 441-450, 455-457",
    f"{O}/numbers_r10.out: E[face] = 7/2; 100 x 7/2 = 350; continuation 250; backward value 1150/3 = 383.33 (2 dp); choice gain "
    "100/3 = 33.33; biased per-turn 25 and play-all 150; first win and first loss 1575/32; total 100 -> 575/8; total 200 -> 625/8 "
    "(exact recursion); E2 625/8 - 150 = -575/8 = -71.875; E3 100/3; R1 look-ahead mean (200+100+0-100)/4 = 50; R2 fee 1 gain 149/2 "
    "= 74.5, fee 100 gain 100/3; M1 net 300; M2 p = 1/3; M3 200.")
row("PC3a-L03-proofs", "2.4 mathematics: Proposition 3.2, Theorem 3.8 and proof, Definition 3.7",
    "L03.html:66-76, 107-110, 296-311",
    "Prop 3.2 (distributive law; exchange of finite sums): correct. Theorem 3.8: base t = N by (H3) and Definition 3.7; the step uses "
    "V(h) = sum_x P(x|h)(W(h) + x) = W(h) + 0 by (H2); histories of probability zero excluded: correct.")
row("PC3a-L03-A3-zero-probability-histories", "2.4 mathematics: A3 and H2 quantify positive-probability histories only",
    "L03.html:292-293 (A3), 300 (H2), 308 (proof)",
    "A3 and H2 both say 'with positive probability'; the proof at L03.html:308 restricts to positive-probability histories. Correct.")
row("PC3a-L03-thm-number-3-10", "2.2 cross-references: no Theorem 3.10",
    "index.html; L01.html; L02.html; L03.html",
    "grep -c 'Theorem 3\\.10' on the four pages: 0 each (greps_r10.out). Example 3.10 is a named example, not a theorem.")
row("PC3a-L03-adapted-undefined", "2.4 notation and terms: no undefined probabilistic term",
    "index.html; L01.html; L02.html; L03.html",
    f"{O}/text_scans.out (DTERM lines): 'martingale', 'stopping time', 'adapted' absent from the four views; the only DTERM hits are "
    "'roll' (verb) and 'probability space' (M4 attribution). 'stopping rule' is defined at L03.html:109 (dfn) before its Definition 3.7 use.")
row("PC3a-L03-each-rule-claim", "2.4/2.9 claim: each of the five rules is a stopping rule of Definition 3.7",
    "L03.html:321, 552; tests/labs/PC3/lab-PC3-L03-1.py RULES tuple (line 109)",
    "Each rule depends only on the history (first win and loss use h[-1]; totals use sum(h)), and each stops at history length N "
    "(stopping_expectation forces a stop at HORIZON). Correct.")
row("PC3a-L03-grades-lab-only", "2.3 grades: T for proved results, C for lab-printed results",
    "L03.html:468-475",
    "Rows 468, 469 and 473 are T (Proposition 3.2 and Theorem 3.8 with A2 over N = 6, proved on the page). Rows 471, 472 and 474 are "
    "C and name Lab 1 Parts 2, 3 and 3b. Row 470 is T with Lab 1 Part 2 as a second source.")
row("PC3a-L03-any-game-fee", "2.2 numbers: R2 reroll-game gain and fee formula",
    "L03.html:448-450",
    "numbers_r10.out: (sum_f max(100f, 350 - c))/6 - 350 gives 100/3 at c = 100 and 149/2 = 74.5 at c = 1 (both on the page).")
row("PC3a-L03-lab-docstring-two-methods", "2.5 labs: docstring claims match code",
    "tests/labs/PC3/lab-PC3-L03-1.py docstring and functions; L03.html:114",
    "Docstring: Part 2 by backward induction and by enumerating every policy (backward_induction; policy_value over "
    "product((0, 1), repeat=6)); Part 3 by two methods (stopping_expectation and stopping_by_sequences); Part 3b by recursion alone "
    "(only stopping_expectation is called there). Matches the code.")
row("PC3a-L03-why-rhetorical-questions", "2.9 prose: why-it-matters paragraphs (no rhetorical question; length by check_pages)",
    "L01.html:51; L02.html:51; L03.html:51",
    f"{O}/view-*.txt is the stripped text: line 51 of view-L01.txt, view-L02.txt and view-L03.txt contains no question mark. "
    "Length of each paragraph is within the 120-word limit (check_pages PASS).")
row("PC3a-L03-numbers-prose-claims", "2.2 prose numbers: 6 x 25, mean 350, 1150/3 - 350",
    "L03.html:104, 322, 336, 349",
    "6 x 25 = 150; mean 350 (100 x 7/2); 1150/3 - 350 = 100/3 = 33.33 (numbers_r10.out). All match.")
row("PC3a-L03-quiz", "2.9 structure: retrieval quiz",
    "L03.html:480-564 (12 items)",
    "12 quiz items (lines 485-560), each with an explanation; the M2 item (508) gives p = 1/3 = 0.333333; the reroll items (524-538) "
    "match Example 3.6 and P3.")
row("PC3a-L03-lab-match", "2.5 labs: page code equals twin; expected block equals twin output",
    "L03.html:112-287; tests/labs/PC3/lab-PC3-L03-1.py",
    "run_labs PASS; twin stdout (30 lines, outputs/twin-L03-1.stdout) matches pre.expected (L03.html:256, data-tolerance 0), "
    "including 'value of the game by backward induction = 1150/3 cents (383.33 to two places)'.")
row("PC3a-L03-canon-breaks", "2.9 prose: canon-breaks bullets",
    "L03.html:330-337",
    "Unbounded stopping (Theorem 3.8 needs a finite N: consistent); fairness hypothesis (Example 3.10: 1575/32, 575/8, 625/8 and 150 are "
    "all nonzero on the biased game); choice has value in a non-fair game (100/3 cents, mean 350). All numbers match numbers_r10.out.")
row("PC3a-L03-fair-game-before-definition", "2.5/2.9 terms before definition: Definitions 3.5 and 3.7 precede the lab",
    "L03.html:51, 91-92, 108-110, 112",
    "'fair' is first used as a term at Definition 3.5 (L03.html:92, dfn). Earlier appearance at L03.html:51 is the phrase 'average "
    "payoff ... zero on every turn' (no term). 'stopping rule' dfn at L03.html:109 precedes the lab at 112.")
row("PC3a-why-terms-before-definition", "2.9 terms used before definition",
    "L01.html:51-58; L02.html:38, 51; L03.html:51, 91-92",
    "L01 'log-error width' has its dfn in the Proposition 1.3 conclusion (L01.html:89); its title '(log-error widths add)' at L01.html:85 "
    "names it earlier (title only). L02 'Introduces' (line 38) names Bayes' rule before its Proposition 2.4 dfn (meta list only). "
    "No running text uses a term before its definition.")
row("PC3a-L03-numbers-key-rows-lab", "2.3 grades: key-results rows 471, 474, 475",
    "L03.html:471, 474, 475",
    "Row 471 (best of 64 policies = 1150/3, C), row 474 (play-all 150; stopping values 1575/32, 575/8, 625/8, C), row 475 "
    "(E[X+Y] = 7, T with lab Part 1). All values in numbers_r10.out.")

# ---- notation, DAG, process words
row("PC3a-notation", "2.4 notation: registered symbols and macros",
    "index.html; L01.html; L02.html; L03.html; notation/notation.json",
    f"{O}/math_symbols.out lists every macro and single-letter symbol in the four pages. Registered symbols T, \\Phi, \\gamma_3, "
    "\\gamma_4, R^\\ast, R^{e\\ast}, R_f and \\mathbb{Q} do not occur. The only \\ast is F^\\ast in index.html:112 (cost-of-carry "
    "forward price, not a registered symbol). Macros used are registered (\\E, \\Prob, \\R, \\indic). N (L03 horizon) is local per "
    "notation.json 'about'. C_i (L02 events) and Q (L01 quantity) are not registered symbols. No collision.")
row("PC3a-dag-prose-only-terms", "2.9 DAG: concepts outside the closure appear only as prose",
    "index.html:148; L01.html (misconception 2); L02.html:57, Problem P2; L03.html:57",
    "adverse selection (E2, D3) appears in plain words at index.html:148 with no link and no dfn. 'probability space' (M6 concept; the M4 "
    "phrase 'finite probability space') appears at L02.html:57 and L03.html:57 with the M4 attribution and no link or dfn. "
    "check_dag PASS (no link to an outside-closure concept).")
row("PC3a-canon-misconceptions-problems-counts", "2.9 structure: misconception and problem counts",
    "L01.html:326-449; L02.html:376-493; L03.html:343-459",
    "L01: 3 misconceptions; problems M1-M3, P1-P3, E1-E4, R1-R3. L02: 3 misconceptions; M1-M3, P1-P3, E1-E3, R1-R3. L03: 3 "
    "misconceptions; M1-M3, P1-P3, E1-E3, R1-R3. Each tier has at least 3 with worked solutions (counted in outputs/view-*.txt).")
row("PC3a-hours-declared", "2.9 structure: lesson hours declared",
    "L01.html:2, 34; L02.html:2, 34; L03.html:2, 34",
    "'6 study hours' on each page (outputs/view-*.txt line 34) and data-hours=\"6\" (grep).")
row("PC3a-r4-delta-read", "2.9 change read: every hunk since the previous pin",
    "git diff c93dd526 00a84795 for index.html, L01.html, L02.html, L03.html and the three twins",
    "Round-10 delta read in full: index.html 2 hunks (line 37 data meta-row; lines 167-172 hours and data section); L01.html 7 hunks "
    "(37, 55, 94, 115, 408, 447, 552); L02.html 4 hunks (88-99 C_i rename of Proposition 2.5; 363-369 canon bullet; 428-440 P2 and P3 "
    "rename; 571-580 quiz rename); L03.html 3 hunks (286 interpretation; 321-327 Examples 3.10 and 3.11; 457 R3 solution). 16 hunks in "
    "total (greps_r10.out). The twins are byte-identical (git diff --stat empty for tests/labs/PC3). Every hunk is re-verified this "
    "round (no row carried from round 9).")
row("PC3a-r4-cross-references", "2.9 cross-references resolve",
    "index.html; L01.html:82, 107, 532; L02.html:458, 592; L03.html:316, 345, 509, 51",
    "'Section 4' (L01.html:82, 332) is 'Where the canon breaks'; 'Section 2' (L01.html:546) is 'Which factor to refine'; 'Section 3' "
    "(L02.html:458) is L02's 'Where the canon breaks'; 'Section 6' (L02.html:592) is Key results; 'Section 4' (L03.html:316) and "
    "'Section 7' (L03 key results) match the heading numbers in outputs/view-*.txt. Problems P2 (L01), P3 and R1 (L03), M2 (L03) exist.")
row("PC3a-r4-recompute-all-numbers", "2.2 numbers: every number in the slice recomputed by script (round-9 FAIL re-verified)",
    f"{S}/numbers_r10.py; {O}/numbers_r10.out; {O}/ratio_check.out",
    "numbers_r10.py recomputes every number in index, L01, L02 and L03 prose (its full output is numbers_r10.out). Every value matches "
    "the page. The round-9 display claim (30.9 percent) is removed and the new text matches.")
row("PC3a-r4-restated-M4-concepts", "2.5 DAG: M4 concepts referenced by link, not redefined",
    "L02.html:57, 67; L03.html:62",
    "The M4 concepts (independence, conditional-expectation-elementary, expectation) are linked to concepts.html and not defined "
    "in PC3 (grep: no dfn for them in L01-L03, greps_r10.out).")
row("PC3a-r4-observations-no-row", "2.4 observations (no defect)",
    "L01.html:433; tests/labs/PC3/lab-PC3-L02-1.py",
    "Observation only: the R1 criterion's part (c) (what changes when the threshold is crossed) is answered by dominance (L01.html:433). "
    "No defect recorded.")
row("PC3a-L03-misconception-most-likely", "2.2 misconception: wrong belief and correction",
    "L03.html:352-353",
    "'A fair game with expected payoff zero never pays a gain' is corrected by Example 3.11 (a +100 turn with probability 1/2). Correct.")
row("PC3a-L03-def35-next-turn", "2.4 definitions: fairness at histories of fewer than N turns",
    "L03.html:92 (Definition 3.5), 293 (A3), 300 (H2)",
    "Definition 3.5 quantifies over histories of fewer than N turns with positive probability, as A3 and H2 do. Consistent.")
row("PC3a-banned-and-process-words", "2.9 banned phrases and process words (learner text)",
    "L01.html, L02.html, L03.html, index.html",
    f"check_pages PASS (banned strings); {O}/text_scans.out PROCESS hits: 0 (build, builder, round, verifier, REQUESTS, unit report, "
    "fixer absent from the four views).")

# ---- hub consistency with project.html (read only for the hub's claims)
row("PC3a-r6-hub-ladder-rung2-wording", "2.9 consistency: hub describes rung 2 as the project does",
    "index.html:159; course/modules/PC/PC3/project.html:45, 253, 349-350",
    "project.html:45 'Rung 2 · Completion problem ... the two lines that give the cash flow and the mark ... left blank'; project.html:349-350 "
    "'cash_flow = ___' and 'mark = ___'. index.html:159 'each of the two lines replaced by ___' agrees. Re-read in round 10; the "
    "round-10 project.html change is at other lines.")
row("PC3a-r6-hub-project-file-names", "2.9 consistency: hub and project name the same student files",
    "index.html:160, 167; course/modules/PC/PC3/project.html:46, 393, 429-448",
    "project.html:393 defines market_maker.py with quote(state) and replay(log); project.html:46 names analysis; index.html:160 names "
    "market_maker.py, quote(state), replay(log) and analysis.md. Agrees.")
row("PC3a-r6-hours-curriculum-attribution", "2.9 prose: attribution of the 14-hour project figure",
    "index.html:167",
    "index.html:167 '50 hours: 36 hours of lessons and 14 hours of project' matches curriculum/06-profession-capstone.yaml:160 (50) and "
    "project.html:434 ('Total 14').")
row("PC3a-r6-def21-m4-weights-positivity", "2.4 attribution: the definition cited to M4 Lesson 1",
    "L02.html:57 (Definition 2.1); L03.html:57 (Assumption A1)",
    "course/modules/M/M4/L01.html:55: finite probability space with p(omega) > 0 summing to 1. Both cite it correctly.")
row("PC3a-r7-hub-skill-check-bid-ask", "2.9 prose and arithmetic: skill-check convention for a maker's fill",
    "index.html:129, 131",
    "index.html:131: a maker that buys pays its bid, so the cash flow is -10005 (data-answer -10005). Consistent with project.html's "
    "rung-1 fill rule (a fill at the bid or at the ask).")
row("PC3a-r7-hub-hours-line-items", "2.6 hours: the project's line items against the project time budget",
    "index.html:167; course/modules/PC/PC3/project.html:421-435 (Time budget table)",
    "project.html:425-434: 1, 1, 3, 2, 2, 4, 1 hours; total 14 (read in round 10). index.html:167 gives the same seven figures and the sum 14.")
row("PC3a-r7-hub-autograder-seeds", "2.9 prose: what the autograder runs",
    "index.html:55 (objective 7), index.html:160; course/modules/PC/PC3/grader/test_project.py:10",
    "test_project.py:10: 'fixed seeds 0 to 49, on the learner's seed SEED and on seed SEED + 7919'. index.html:160 says seeds 0 to 49, "
    "the workspace seed, and that seed plus 7919. Agrees.")
row("PC3a-r7-L02-timed-drill-budget", "2.9 structure: the curriculum lab's timed element and the Architect-default budget",
    "L02.html:132-134 (lab hypothesis), 359 (interpretation)",
    "L02.html:134: 'stated here as 60 seconds per item, with no timer on this page' (architect default); the lab counts agreement and "
    "does not time anyone (L02.html:359). Consistent.")

# ---- round-10 new checks
row("PC3a-r10-E2-fix-verified", "2.2 numbers: round-9 FAIL row re-derived after the fix",
    "L01.html:408",
    "Same subject as PC3a-L01-E2-shares; re-verified in numbers_r10.out ('four-place quotient' and 'full precision' lines).")
row("PC3a-r10-L02-rename-consistency", "2.4 notation and proof: the C_i rename is consistent in Proposition 2.5, P2, P3 and the quiz",
    "L02.html:91-99, 428-440, 574-580",
    "greps_r10.out: no A_i, A_1, A_2 or A_3 remains in L02.html; C_i, C_1, C_2, C_3 are used (19, 12, 11, 3 occurrences) in the "
    "statements and proofs that were renamed.")
row("PC3a-r10-L03-R2-fee-formula", "2.2 numbers: L03 R2 fee formula and its two values",
    "L03.html:450",
    "(sum_f max(100f, 350 - c))/6 - 350 evaluated exactly: c = 100 gives 100/3; c = 1 gives 149/2 = 74.5 (numbers_r10.out).")
row("PC3a-r10-L03-example-3-10-A3", "2.4 definitions: A3 is stated before Example 3.10 uses it",
    "L03.html:292-293 (A3), 321 (use)",
    "A3 is Assumption at L03.html:292; Example 3.10 at L03.html:320-321 uses 'the fairness condition of A3 with N = 6'. Defined before use.")
row("PC3a-r10-scope-words", "2.9 / verifier rule 4: scope words backed by a computation or a stated hypothesis",
    f"{O}/text_scans.out (SCOPE lines); the sentences were read in full in view-*.txt",
    "Every scope sentence in index, L01, L02 and L03 was read with its context. Universal claims are backed by a theorem with hypotheses "
    "(Theorem 1.2, Proposition 1.3, Theorem 1.5, Propositions 2.4-2.5, Theorem 3.8), by an exact enumeration of a stated finite space "
    "(Lab Parts 1-4, the 125-point grid, the 64 policies, the 20 ordered draws), or by an explicit scope statement ('six pairs of n and x, "
    "not every x >= 0'; 'three narrowings'; 'two host rules'; A1 finite spaces). No unsupported 'always' or 'never' claim found.")
row("PC3a-r10-process-and-dag-terms", "2.9 process words and D-terms (plan section 4, D1-D9) in learner text",
    f"{O}/text_scans.out (PROCESS and DTERM lines)",
    "PROCESS: 0 hits. DTERM hits: 'roll' (verb), 'combination' (English), 'adverse selection' (index.html:148, plain prose, D3), "
    "'probability space' (L02.html:56-57, L03.html:57, M4 attribution, no link). No martingale, stopping-time, Poisson, Kelly, Markov, "
    "CAPM, duration, Gordon, binomial-distribution, Nash or Bayesian-inference term appears.")
row("PC3a-r10-twins-unchanged", "2.5 labs: twins byte-identical since the previous pin (carry check)",
    "tests/labs/PC3/lab-PC3-L01-1.py, lab-PC3-L02-1.py, lab-PC3-L03-1.py",
    "git diff --stat c93dd526 00a84795 -- tests/labs/PC3 is empty. md5 of the three twins is recorded in outputs/md5_twins.out (run on the current bytes; the twin rows above).")
row("PC3a-r10-hub-claims-outside-slice", "2.9 hub claims about pages outside the slice (read only to check the hub's claims)",
    "index.html:33-37, 143-150, 160-161, 167, 172; L04.html; L05.html; L06.html; project.html",
    "L05.html uses big-o-complexity, hash-map, binary-heap and monotonic-deque; L06.html uses cost-of-carry-forward-price, "
    "put-call-parity, net-present-value and statement-articulation, as the hub's prerequisite list says. L04.html has 10 SIMULATED "
    "labels, consistent with index.html:37. This row does not verify L04-L06 content, which is outside this slice.")

verdict = "PASS" if all(r["status"] == "PASS" for r in rows) else "FAIL"
fragment = {
    "unit": "PC3",
    "slice": "PC3-a",
    "round": 10,
    "verifier": "Claude Haiku 5.5, independent verifier PC3 slice a, round 10 (did not build PC3; no shared context with the builders)",
    "pin": "00a84795f276456fce19d4181373cc4efba11a36 (detached)",
    "base": "c93dd526025c6dffd34c54cd2c89eb62a890f885 (the round-9 pin; delta read hunk by hunk)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE10-PC3-a",
    "scratch": "none in the checkout beyond ledgers/PC3/scripts/PC3-a-r10/; each twin run used a fresh /tmp directory holding only a copy of the twin",
    "verified_at": datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat(),
    "verdict": verdict,
    "scope": ("course/modules/PC/PC3/index.html, L01.html, L02.html, L03.html and tests/labs/PC3/lab-PC3-L01-1.py, L02-1.py, L03-1.py. "
              "Not in this slice: L04-L06, project.html, grader/, cards.json, the project labs (read only to check hub claims)."),
    "rows": rows,
    "mutants": [],
    "registry_flags": [
        "crack2015heard (references/references.json:6222): publisher string '[Timothy Falcon Crack]' carries brackets; the curriculum "
        "string says '16th ed.' while the record has no edition (plan B4). Registry owner should correct the publisher string; not edited here.",
        "zhou2008practical (references/references.json:23402): publisher 'Lulu,]' has a stray bracket (plan B4). Not edited here.",
    ],
    "freshness_flags": [
        "No 2025-2026 work is cited in the slice. PC3 cites two books at book level only (zhou2008practical, crack2015heard) and no passage.",
    ],
    "notes": [
        "Delta since the round-9 pin (c93dd526..00a84795) for the slice: index.html (2 hunks), L01.html (7), L02.html (4), L03.html (3); "
        "the twins are byte-identical. Every hunk was read and every changed claim re-verified; no row is carried from round 9.",
        "The round-9 FAIL (PC3a-L01-E2-shares, and its duplicate PC3a-r4-recompute-all-numbers) is fixed: L01.html:408 now gives "
        "0.308477 / 30.8477 percent / 30.85 / 30.8, which recomputes exactly. Both rows are PASS.",
        "Mutation testing is not applicable: the slice has no grader (ruling: lab twins are demonstrations). mutants is empty.",
        "Architect notes (not verdict-changing): (a) curriculum/06-profession-capstone.yaml:174 names the L02 lab 'with spaced repetition'; "
        "the page routes spacing through the cards (L02.html:134). (b) L02's meta line 'Introduces:' lists conditional probability, Bayes' "
        "rule and the law of total probability, which the curriculum does not register as concepts (plan: L02 introduces none); the page "
        "defines them in plain prose and does not link them.",
        "Not checked in this slice: cards.json (its L01-L03 cards were not scanned against the lesson text; the quiz items were); L04-L06, "
        "project.html, grader/, the project labs; live verify_refs (offline only); fetch_data --check (no data in PC3).",
    ],
    "summary": {
        "rows": len(rows),
        "pass": sum(r["status"] == "PASS" for r in rows),
        "fail": sum(r["status"] == "FAIL" for r in rows),
        "unverifiable": sum(r["status"] == "UNVERIFIABLE" for r in rows),
        "mutants_killed": 0,
        "mutants_total": 0,
    },
}
out = ROOT / "ledgers/PC3/PC3-a.json"
out.write_text(json.dumps(fragment, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("wrote", out, "rows", len(rows), "verdict", verdict)
