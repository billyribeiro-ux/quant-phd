"""Build the round-3 verifier fragment for CS2 slice b (L05-L08) and write ledgers/CS2/CS2-b.json.

Usage (from the checkout root): python -I -W error ledgers/CS2/scripts/CS2-b-r3/v3_build_fragment.py
Writes only ledgers/CS2/CS2-b.json. Every evidence string names the script, file, line or command that backs it.
"""

import json
from pathlib import Path

ROWS = [
    # ---- gates (run on pin 8196077d; outputs in ledgers/CS2/scripts/CS2-b-r3/gates_r3.out) ----
    {
        "id": "CS2b-gate-check-pages",
        "check": "2.9 structure gate (check_pages)",
        "location": "course/modules/CS/CS2/L05.html .. L08.html, cards.json",
        "status": "PASS",
        "evidence": "gates_r3.out: check_pages.py --unit CS2 --page L05, L06, L07, L08 each 'check_pages CS2 Lxx: PASS'; "
        "check_pages.py --unit CS2: 'check_pages CS2: PASS'.",
    },
    {
        "id": "CS2b-gate-check-dag",
        "check": "2.9 DAG gate (check_dag) plus own link and dfn check",
        "location": "L05-L08 concept links; dfn ids; L01.html, L02.html, L04.html, concepts.html",
        "status": "PASS",
        "evidence": "gates_r3.out: check_dag.py --unit CS2: 'check_dag CS2: PASS'. Own grep: link targets L01#def-big-o-complexity, "
        "L02#def-hash-map, L04#def-comparison-sorting, L04#def-binary-search each defined exactly once; concepts.html ids "
        "mathematical-induction and exponential-and-logarithm exist; dfn ids def-balanced-search-tree (L05), "
        "def-graph-traversal (L06), def-dynamic-programming (L07), def-order-book-data-structure (L08) occur once each.",
    },
    {
        "id": "CS2b-gate-check-projects",
        "check": "2.6 project gate (unit level; slice has no project)",
        "location": "course/modules/CS/CS2/project.html",
        "status": "PASS",
        "evidence": "gates_r3.out: check_projects.py --unit CS2: 'check_projects CS2: PASS'. Not in slice; run for completeness.",
    },
    {
        "id": "CS2b-gate-run-labs",
        "check": "2.5 labs run (run_labs)",
        "location": "tests/labs/CS2/lab-CS2-L05-1.py .. lab-CS2-L08-1.py",
        "status": "PASS",
        "evidence": "gates_r3.out: run_labs.py --unit CS2 --page L05..L08, each 'run_labs CS2: PASS (1/1)'.",
    },
    {
        "id": "CS2b-gate-lab-exact",
        "check": "2.5 labs: twin alone under -I -W error; page code == twin; expected == stdout",
        "location": "course/modules/CS/CS2/L05.html..L08.html; tests/labs/CS2/lab-CS2-L0{5,6,7,8}-1.py",
        "status": "PASS",
        "evidence": "ledgers/CS2/scripts/CS2-b-r3/v3_lab_exact.py run as python -I -W error, output v3_lab_exact.out: ALL_OK; "
        "for L05, L06, L07, L08 page_code_equals_twin=True, exit=0, stderr empty, expected_equals_stdout=True, "
        "files_written=[] (each twin run alone in an empty temp directory); stdout lines 31, 17, 10, 15.",
    },
    {
        "id": "CS2b-gate-page-smoke",
        "check": "2.9 page_smoke (Chromium, Pyodide, 360 px, both themes, console errors, external requests)",
        "location": "course/modules/CS/CS2/L05.html..L08.html",
        "status": "PASS",
        "evidence": "tools/page_smoke.py --unit CS2 --pages L05 L06 L07 L08, run alone on a quiet machine; output saved in "
        "ledgers/CS2/scripts/CS2-b-r3/page_smoke_r3.out: 'page_smoke modules/CS/CS2/Lxx.html: PASS' for all four and "
        "'page_smoke CS2: PASS', exit 0. Lab runtimes 0.0 s.",
    },
    {
        "id": "CS2b-gate-ruff-mypy",
        "check": "lab twin lint, format and types",
        "location": "tests/labs/CS2/lab-CS2-L05-1.py .. lab-CS2-L08-1.py",
        "status": "PASS",
        "evidence": "gates_r3.out: ruff check on the four twins 'All checks passed!'; ruff format --check '4 files already formatted'; "
        "mypy --no-incremental on the four twins 'Success: no issues found in 4 source files'.",
    },
    {
        "id": "CS2b-gate-pytest",
        "check": "2.5 lab and page tests",
        "location": "tests/test_labs.py -k CS2; tests/test_page_checks.py",
        "status": "PASS",
        "evidence": "gates_r3.out: pytest tests/test_labs.py -k CS2 -q exit 0 (14 tests); pytest tests/test_page_checks.py -q exit 0.",
    },
    {
        "id": "CS2b-gate-verify-refs",
        "check": "2.1 citations (registry integrity and live unit run)",
        "location": "references/references.json; L05 and L06 References sections",
        "status": "PASS",
        "evidence": "gates_r3.out: verify_refs.py --offline 'offline integrity: 560 entries, 0 problems'; verify_refs.py --unit CS2 "
        "(live, plain tool run) 'live re-verification of CS2: 1 of 560 entries, 0 problems' (verify_refs_unit_r3.out). "
        "grep: no data-cite attribute in L05-L08; cormen2022introduction is named in the L05 and L06 References paragraphs with "
        "no claim attributed to it (L05.html line 648, L06.html line 591).",
    },
    # ---- numbers (independent recomputation: v3_numbers.py, v3_book_levels.py) ----
    {
        "id": "CS2b-L05-lab-numbers",
        "check": "2.2 numbers in L05 prose and lab expected block (recomputed from unrounded values)",
        "location": "L05.html lines 52, 99, 414, 422, 436, 440, 505, 519, 544; expected block lines 383-413",
        "status": "PASS",
        "evidence": "ledgers/CS2/scripts/CS2-b-r3/v3_numbers.py (independent AVL written from the definitions), output v3_numbers.out: "
        "final height 11; rotation calls 340; kinds LL 63, RR 53, LR 55, RL 57 with 63+53+2(55+57)=340; no-rotation inserts 272 of 500 "
        "= 54.4%; max calls per insert 2; log_phi 501 = 12.9186; plain BST height 64 and AVL height 7 on keys 1..64; log_phi 65 = 8.6747; "
        "N(0..12) = 0,1,2,4,7,12,20,33,54,88,143,232,376; N(h)+1 >= phi^h for h=1..12; 1/log2(phi) = 1.440420; log_phi 3 = 2.28; "
        "log_phi 8 = 4.32; log_phi 377 = 12.33; ln 377 = 5.932; ln phi = 0.4812; two-node height 2. All prose numbers agree.",
    },
    {
        "id": "CS2b-L06-lab-numbers",
        "check": "2.2 numbers in L06 prose and lab expected block (recomputed)",
        "location": "L06.html lines 362, 368, 370, 380, 388, 453, 460, 467, 566; expected block lines 345-361",
        "status": "PASS",
        "evidence": "v3_numbers.py (own BFS, own exhaustive simple-path minimum, own DFS, own weighted exhaustive search), v3_numbers.out: "
        "200 sources, 772 reachable pairs incl. self, 308 unreachable, 572 positive, 0 mismatches; 440 vertex pairs, 0 violations; "
        "Part C lightest paths: a via s-b-a weight 2 (2 hops), c via s-b-a-c weight 3 (3 hops), b direct weight 1; Part D: 619 edges, "
        "200 reached, 1238 inspections = 2*619, 40000 matrix reads, 1438 list work; 40000/1438 = 27.8164 (1438*27 = 38826, rem 1174); "
        "1238/200 = 6.19.",
    },
    {
        "id": "CS2b-L07-lab-numbers",
        "check": "2.2 numbers in L07 prose and lab expected block (recomputed)",
        "location": "L07.html lines 63, 210, 497-506 (expected block), 507, 513-515, 528, 532, 546-566 (M and E solutions), 597-611 (E1-E3), 622 (R1)",
        "status": "PASS",
        "evidence": "v3_numbers.out: ACGTACG/TGCATGC: LCS 3, memo stored 28, memo calls 47 = 28 stored + 11 lookups + 8 base calls, "
        "no-memo calls 183, table cells 49 = 7*7; coins (1,3,4) amount 20: f = 5, stored amounts 20, memo calls 56, no-memo 20736; "
        "f(0..6) = 0,1,2,1,1,2,2; f(9) for {2,5} = 3, f(7) = 2, f(4) = 2; largest-coin-first 3 coins vs optimum 2 at amount 6, first "
        "greedy failure at 6; greedy optimal for {1,c}, c=2..30, a<=200 (0 mismatches); AB/BA LCS 1; 2^20+1 = 1048577; 2^40 has 41 bits "
        "and 2^40+1 > 10^12; 1000 has 10 bits; (m+1)(n+1)=54, mn=40, boundary 14 (m=5, n=8). Expected block reproduced by run_labs and "
        "v3_lab_exact.out.",
    },
    {
        "id": "CS2b-L08-lab-numbers",
        "check": "2.2 numbers in L08 prose and lab expected block (recomputed by two independent models)",
        "location": "L08.html lines 534-548 (expected block), 549, 571, 575, 638-654, 696-697; code lines 92-99, 119-130, 178-190",
        "status": "PASS",
        "evidence": "v3_numbers.py (flat reference, own stream): orders 298, cancels 102, traded messages 117, executions 177, "
        "steps with no live order [0, 2] so 398 steps with a live order, 102/400 = 25.5%, 102/398 = 25.6%, final best bid 9980, "
        "best ask 9989, 10 resting. v3_book_levels.py (own level model with head passes, deletion and halving search), output "
        "v3_book_levels.out: queue steps 7, levels created 185, removed 177, searches 362 = 185 + 177, max comparisons 4, levels left 8, "
        "10 live orders. Part A trades (5 @10000 order 1, 2 @10000 order 2; cancel of order 3; 1 @10000 from order 2, 4 rest as bid) "
        "match the hand computation.",
    },
    # ---- lab hypotheses and interpretations ----
    {
        "id": "CS2b-L05-lab-hypothesis",
        "check": "3 lab hypothesis and interpretation vs code and output",
        "location": "L05.html line 123 (hypothesis), 124-136 (docstring), 414 (interpretation); code lines 144-382",
        "status": "PASS",
        "evidence": "Hypothesis lists the checks in check_invariant, in_order and height_bound (L05.html code lines 253-262, 265-271, 292-294; checks at lines 325-328); "
        "rotation counts by kind (lines 221-236); Part B inserts 1..64 (line 349); Part C prints N_h beside phi^h and the two-node height (lines 363-372). "
        "Interpretation (line 414) matches output lines 383-413. No time import (grep).",
    },
    {
        "id": "CS2b-L06-lab-hypothesis",
        "check": "3 lab hypothesis and interpretation vs code and output",
        "location": "L06.html line 125 (hypothesis), 126-140 (docstring), 362 (interpretation); code lines 152-333",
        "status": "PASS",
        "evidence": "Part A brute_min_hops comparison with mismatch count (L06.html code lines 266-273); Part B nested_or_disjoint over all pairs (lines "
        "284-296); Part C exhaustive lightest path, the docstring's 'differ for a and c, coincide for b' matches output lines 353-355; "
        "Part D matrix reads by formula len(order)*n (line 332). Interpretation (line 362) matches output lines 345-361.",
    },
    {
        "id": "CS2b-L07-lab-hypothesis",
        "check": "3 lab hypothesis and interpretation vs code and output",
        "location": "L07.html lines 206, 210 (hypothesis), 507 (interpretation); code lines 437-496",
        "status": "PASS",
        "evidence": "Expected result (line 210) is asserted in code: memo == table == exhaustive (line 442), cells == m*n (line 444), coin "
        "methods agree (line 456); Part C counts printed (lines 476-477, 503-506). Interpretation (line 507) decomposes 47 = 28 + 11 + 8 and "
        "matches the output; 'the lab checks on 60 seeded instances, not proofs' is stated.",
    },
    {
        "id": "CS2b-L08-lab-hypothesis",
        "check": "3 lab hypothesis and interpretation vs code and output",
        "location": "L08.html line 176 (expected result), 52, 549 (interpretation); code lines 92-99 (check_order), 294-318 (Part B), 341-348 (Part C)",
        "status": "PASS",
        "evidence": "Part A refuses a float price with TypeError (check_order line 94-95, Part A line 277) and a zero quantity with ValueError "
        "(line 96-97, Part A line 281); Part B asserts trades, best bid/ask and resting ids after each message (lines 306-314); Part C "
        "asserts queue_steps <= orders_added (339-340) and comparisons <= bit_length (341-343). The rested count is not printed, as "
        "line 549 says.",
    },
    {
        "id": "CS2b-lab-simulated-labels",
        "check": "1.7 SIMULATED labels on simulated data",
        "location": "L05.html line 123; L06.html line 125; L07.html line 206; L08.html lines 52, 549",
        "status": "PASS",
        "evidence": "Each lab's hypothesis paragraph or the paragraph before its code carries SIMULATED; each twin docstring states the seed "
        "and that no market data or network is used (L05.html line 126-130, L06.html 128-130, L07.html 213-214 and L08 twin lines 3, 179-182).",
    },
    # ---- mathematics ----
    {
        "id": "CS2b-L05-math",
        "check": "2.4 theorems, derivations and key formulas (L05)",
        "location": "L05.html line 82 (Lemma 2.3 proof, first sentence); Prop 2.4 lines 86-94; Prop 3.1 lines 107-113",
        "status": "FAIL",
        "evidence": "Read lines 76-118 in full (v3_strip.py). Lemma 2.3 proof, line 82: 'For h >= 2, N(h) - N(h-1) = 1 + N(h-2) >= 1 > 0'. "
        "The step '>= 1' needs N(h-2) >= 0, which neither the lemma nor its proof establishes; the only proof of N(h) >= 0 on the page is "
        "the worked solution of P2 (line 487), a later problem solution the lemma does not cite. The rest of Lemma 2.3 (strong induction; "
        "root-subtree heights h-2 <= h2 <= h-1; N(h2) >= N(h-2) by monotonicity) is correct. Proposition 2.4 (M(h) = N(h) + 1 satisfies "
        "M(h) = M(h-1) + M(h-2); phi < 2; phi^2 = phi + 1; M(h) >= phi^h; log step) and Proposition 3.1 (in-order A, x, B, y, C before "
        "and after) re-derived and correct. Card CS2-c179 (cards.json line 1228) repeats the same step.",
        "fix": "L05.html line 82: insert before 'First, N is nondecreasing': 'Also N(h) >= 0 for every h, by induction: N(0) = 0, "
        "N(1) = 1, and each later value N(h) = 1 + N(h-1) + N(h-2) is a sum of nonnegative terms.' Then N(h) - N(h-1) >= 1 is justified "
        "inside the lemma.",
    },
    {
        "id": "CS2b-L06-math",
        "check": "2.4 theorems and derivations (L06)",
        "location": "L06.html Lemma 2.1 (68-75), Prop 2.2 (78-89), Prop 2.3 (92-98), Remark 2.4 (102-103), Prop 3.2 (114-120)",
        "status": "PASS",
        "evidence": "Line 120 hunk read: the proof now covers the recursion forest, the same-tree LCA case and the different-tree case "
        "(earlier root finishes before later root starts), so every pair of distinct vertices is handled. Lemma 2.1, Prop 2.2 "
        "(reachable/discovered both ways; dist >= delta by walks; dist <= delta by Lemma 2.1 removal order), Prop 2.3 (each vertex "
        "enqueued once; scans sum to 2|E| under undirectedness) re-derived and correct. Hypotheses stated (lines 68-69, 78, 92, 114-115).",
    },
    {
        "id": "CS2b-L07-math",
        "check": "2.4 theorems and derivations (L07)",
        "location": "L07.html Def 2.1 (68-70), Thm 2.2 (72-92), Cor 2.3 (94-107), Ex 2.4 (109-112), Def 3.1 (116-119), Lemma 3.2 (121-139), Thm 3.3 (141-159), Cor 3.4 (161-170), Prop 3.5 (172-185), Prop 4.2 (191-204)",
        "status": "PASS",
        "evidence": "Theorem 2.2 base, upper bound, lower bound (remove one coin), infinite case re-derived; Cor 2.3 strong induction valid (lines 105-106); "
        "Example 2.4 values f(0..6) recomputed; Lemma 3.2 both inequalities; Theorem 3.3 cases (i)-(iii) exhaustive and each bound checked; "
        "Cor 3.4 induction on i+j; Prop 3.5 counts mn and (m+1)(n+1); Prop 4.2 inequalities 2^(b-1) < A+1 <= 2^b with A = 2^40 checked. "
        "Hypotheses listed for each theorem.",
    },
    {
        "id": "CS2b-L08-math",
        "check": "2.4 theorems and derivations (L08)",
        "location": "L08.html Def 1.1 (60-62), Def 1.2 (65-66), Prop 1.3 (71-86), Def 2.1 (92-95), Prop 2.2 (109-122), Ex 2.3 (125-126), Lemma 3.1 (134-141), Prop 3.2 (144-156), Prop 3.3 (159-172)",
        "status": "PASS",
        "evidence": "Changed hunk read: Prop 3.2 hypotheses (lines 147-150) now define the half-open interval [lo, hi), mid = lo + floor((hi-lo)/2), "
        "and the proof (line 155) uses the same interval; re-derived: new lengths n - floor(n/2) - 1 = ceil(n/2) - 1 and floor(n/2), so the "
        "k-th test needs 2^(k-1) <= L and k <= floor(log2 L) + 1 (matches code lines 119-130, which use mid = (lo+hi)//2, equal to "
        "lo + floor((hi-lo)/2)). Prop 1.3 (cancellation; buy and sell submissions; A' > p at stop) valid; Prop 2.2 with Assumptions 1 and 2 "
        "labelled; Lemma 3.1 valid; Prop 3.3 items match code lines 132-203.",
    },
    {
        "id": "CS2b-L05-problems",
        "check": "2.4 worked solutions and problem set (L05)",
        "location": "L05.html M1-M3 (451-471), P1-P3 (476-496; P2 solution line 487), E1-E3 (501-521), R1-R3 (526-546)",
        "status": "PASS",
        "evidence": "Changed P2 solution (line 487) read: the reason is now induction on N(0)=0, N(1)=1 with nonnegative terms, which is correct. "
        "All other solutions re-derived: M1 heights/balance factors (root 5, bf 1), M2 single left rotation, root 2, M3 N(5)=12; P1 left rotation "
        "keeps order; P3 identity; E1 272/500 = 54.4%; E2 log2 64 = 6 and bound 8.6747; E3 bound 12.33 at 376 nodes; R1 left-right double rotation, "
        "root 2; R2 seven-node height-4 tree (balance factors recomputed, N(4)=7); R3 N(5)=12 > 7 and log_phi 8 = 4.32.",
    },
    {
        "id": "CS2b-L06-problems",
        "check": "2.4 worked solutions and problem set (L06)",
        "location": "L06.html M1-M3 (400-418), P1-P3 (425-443), E1-E3 (450-469), R1-R3 (476-493)",
        "status": "PASS",
        "evidence": "M1 BFS distances 0,1,1,2,3 and removal order 1..5 (re-derived, v3_numbers.py bfs); M2 DFS times d=(1,2,3), f=(6,5,4); "
        "M3 triangle 2|E|=6; P1-P3 valid; E1 572; E2 27.8164 -> 27.82; E3 6.19; R1 undirected DFS edge argument re-derived (lines 478); "
        "R2 connected component (line 485); R3 complete graph n(n-1) = 2|E|, total n^2.",
    },
    {
        "id": "CS2b-L07-problems",
        "check": "2.4 worked solutions and problem set (L07)",
        "location": "L07.html M1-M3 (543-563), P1-P3 (568-588), E1-E3 (593-613), R1-R3 (618-638)",
        "status": "PASS",
        "evidence": "M1 f(9) = 3 for {2,5} (2+2+5) re-derived; M2 table for AB, BA gives 1 (lambda(2,2) = 1); M3 54, 40, 14; P1 induction valid "
        "(base, c not dividing a, step); P2 column-major order valid; P3 smallest failing amount 6 (f(1..5) matched by greedy, f(6)=2 vs 3); "
        "E1 20 stored amounts (denomination 1 in D); E2 49 cells vs 28 reached (recomputed); E3 47 = 28 + 11 + 8; R1 1048577 and the bounds; "
        "R2 proof k + (a-kc) = a - k(c-1) and exhaustive check c=2..30; R3 two rows of n+1 entries.",
    },
    {
        "id": "CS2b-L08-problems",
        "check": "2.4 worked solutions and problem set (L08)",
        "location": "L08.html M1-M3 (587-606), P1-P3 (612-631), E1-E3 (637-656), R1-R3 (662-681)",
        "status": "PASS",
        "evidence": "M1 trades 2 @10010 (order 2) and 3 @10010 (order 3), rests 1 @10010 and 3 @10020 (re-derived); M2 bounds 3 and 4; M3 trades "
        "1 @10000, rests 2 as bid 10001, best ask 10005; P1 bound n(floor(log2 n)+1) valid; P2 trade price a <= p (line 622); P3 min{q,Q} "
        "both stop cases; E1 102/400 = 25.5%, 102/398 = 25.6%; E2 queue steps only in _front, called only from submit (grep: one call site); "
        "E3 L >= 8; R1 newest-first differs from Def 2.1; R2 injection argument; R3 KeyError at line 178 (self.levels[opposite][best]) after the "
        "level is deleted, a reading of the code that the lab does not exercise, labelled as such.",
    },
    # ---- lesson prose: problems and misconceptions ----
    {
        "id": "CS2b-L06-quiz-terms",
        "check": "2.9 terms used before definition / undefined term (defect class 5)",
        "location": "L06.html lines 578-584 (quiz item); cards.json CS2-c081 (line 563-566)",
        "status": "FAIL",
        "evidence": "L06.html line 578: 'In an undirected DFS tree, how is each non-tree edge related to the tree?' grep of L06.html for "
        "'DFS tree' and 'non-tree' finds only line 578 (and line 584's reference to R1). Neither term is defined on the page; the search "
        "structure is defined only in the proof of Proposition 3.2 (line 120: 'the recursion forest'). Card CS2-c081 (cards.json line 566) "
        "also uses 'the DFS tree path from a to c' with no definition, although the lesson's Misconception 2 (line 384) says 'its tree path'.",
        "fix": "L06.html line 578: replace the prompt with 'In an undirected graph searched by Definition 3.1, how is each edge \\(\\{u, v\\}\\) "
        "related to the recursion forest of the search?' (options and the answer 'It joins a vertex to its ancestor or descendant' stay; "
        "line 584 stays). cards.json CS2-c081 back: replace 'the DFS tree path from a to c' with 'the path from a to c through the search's "
        "recursion calls'.",
    },
    {
        "id": "CS2b-L06-canon-undirected",
        "check": "2.9 canon-breaks claim about directed graphs (L06)",
        "location": "L06.html line 370 (Where the canon breaks, 'Directed graphs')",
        "status": "PASS",
        "evidence": "Re-checked: Prop 2.3's proof uses symmetry only in the degree-sum step (line 98); Lemma 2.1 (line 68-75), Prop 2.2 (78-89) "
        "and Prop 3.2 (120) do not use it; the page says it does not cover directed DFS classification.",
    },
    {
        "id": "CS2b-L06-connected-component",
        "check": "2.4 R2 solution (L06)",
        "location": "L06.html line 485 (solution to Problem R2)",
        "status": "PASS",
        "evidence": "Read in full: reachable set equals the connected component of s for an undirected graph, which follows from Prop 2.2 and the "
        "definition of connectedness via paths; no claim beyond that.",
    },
    {
        "id": "CS2b-L05-misconceptions-canon",
        "check": "2.9 misconceptions and where-the-canon-breaks prose (L05-L08)",
        "location": "L05.html 420-423, 431-440; L06.html 368-371, 379-388; L07.html 513-515, 523-532; L08.html 555-558, 566-575",
        "status": "PASS",
        "evidence": "Each lesson has at least 3 misconceptions with a computation or lab. Claims re-derived: L05 272/500 and 340 calls, "
        "log_phi(n+1) about 1.44 log2(n+1); L06 1238 vs 40000 vs 1438; L07 greedy 4+1+1 vs 3+3, 2^40 needs 41 bits; L08 Example 2.3, "
        "185 - 177 = 8 levels with 10 orders forces a level of two orders (pigeonhole).",
    },
    {
        "id": "CS2b-key-results-ungraded",
        "check": "2.3 key-results tables: every claim graded with a source (L05-L08)",
        "location": "L05.html line 560 (row 5); L06.html line 508 (row 5); L07.html lines 655-656; L08.html lines 696-697",
        "status": "PASS",
        "evidence": "Each non-proved row carries grade C and a basis naming the lab and part (L05 line 560 'Lab 1, Part A (SIMULATED seeded run; "
        "not a proof)'; L06 line 508; L07 655-656; L08 696-697). T rows name the proving section.",
    },
    {
        "id": "CS2b-grades",
        "check": "2.3 grades re-graded against BLUEPRINT section 3",
        "location": "L05-L08 block-title claim spans (Lemma/Proposition/Theorem/Corollary), key-results tables, cards grades",
        "status": "PASS",
        "evidence": "grep of data-grade on block titles: every Lemma, Proposition, Theorem and Corollary is T (L05 Lemma 2.3, Prop 2.4, Prop 3.1; "
        "L06 Lemma 2.1, Props 2.2, 2.3, 3.2; L07 Thm 2.2, Cor 2.3, Lemma 3.2, Thm 3.3, Cor 3.4, Props 3.5, 4.2; L08 Props 1.3, 2.2, 3.2, 3.3, "
        "Lemma 3.1). Remarks carry no block grade, and key-results rows grade them (L05 row 556 Remark 1.1 T; row 560 Remark 3.2 C). "
        "Card grades: T 56, C 15; every C card has a basis (v3_cards.out).",
    },
    # ---- cards ----
    {
        "id": "CS2b-cards-trivia",
        "check": "2.7 cards are not trivia (round-2 row, re-checked)",
        "location": "course/modules/CS/CS2/cards.json CS2-c163 (line 1145)",
        "status": "PASS",
        "evidence": "Round-2 FAIL on CS2-c163 is resolved: the front and back were rewritten (delta read, git diff 9294b914..8196077d) to the Lemma 3.1 "
        "mechanism, so the card is no longer trivia. Its duplication of CS2-c107 is recorded in row CS2b-cards-duplicates.",
    },
    {
        "id": "CS2b-cards-correctness",
        "check": "2.7 each card correct against the current lesson text (all 71 slice cards read)",
        "location": "course/modules/CS/CS2/cards.json, the 71 cards with lesson L05-L08 (lines 430-1480 range)",
        "status": "PASS",
        "evidence": "Every card read in full (dump scripted by v3_cards.py; v3_cards.out). Card CS2-c215 (line 1376) changed from C to T with basis "
        "removed (round-2 row); its content (heavy child, single vs double rotation) matches L05.html lines 104 and Section 3; graded as a "
        "procedure definition in the same way as CS2-c058 (T). CS2-c237 (new, L08 C, '362 searches ... largest count of 4') matches "
        "L08.html line 549 and the v3_book_levels.py count (362 = 185 + 177, max 4). CS2-c063 and CS2-c068 match Remark 3.2 and the lab output.",
    },
    {
        "id": "CS2b-cards-duplicates",
        "check": "2.7 no duplicate cards (full scan)",
        "location": "course/modules/CS/CS2/cards.json CS2-c163 (line 1145) and CS2-c107 (line 741)",
        "status": "FAIL",
        "evidence": "v3_cards.py: no duplicate ids (204 cards). Semantic duplicate: CS2-c107 (T, Lemma 3.1, back 'Then the steps are at most the "
        "number of orders that rested over the run ... (Lemma 3.1)') and CS2-c163 (C, back 'Each queue entry is passed at most once, so queue "
        "steps are at most the orders that rested (Lemma 3.1). Lab 1, Part C shows 7 steps against 298 orders added.') test the same lemma. "
        "The only new content in c163 is the lab count, which is on the page (L08.html line 549) and is not a key-results row.",
        "fix": "Delete CS2-c163 from course/modules/CS/CS2/cards.json (it is a second card for Lemma 3.1 that CS2-c107 already carries); "
        "the 7-versus-298 figure stays in the L08 prose at line 549.",
    },
    {
        "id": "CS2b-cards-hypotheses",
        "check": "2.7 cards carry the proposition's hypotheses",
        "location": "cards.json CS2-c077 (line 541) and CS2-c082 (line 570), both citing Proposition 2.3 (L06.html line 93)",
        "status": "FAIL",
        "evidence": "L06.html line 93 states Proposition 2.3 with 'Assume an undirected graph with |V| vertices and |E| edges, stored as adjacency "
        "lists.' CS2-c077 back: 'At most |V| enqueues and at most 2|E| adjacency entries inspected, for a graph with |V| vertices and |E| edges "
        "stored as adjacency lists (Proposition 2.3).' CS2-c082 back: 'Lists cost at most |V| + 2|E| operations (Proposition 2.3).' Neither "
        "states the undirected hypothesis. (The bounds remain true for directed graphs, since the out-degree sum is |E| <= 2|E|, but the card "
        "must carry the stated hypothesis.)",
        "fix": "CS2-c077 back: prefix 'Assume an undirected graph with |V| vertices and |E| edges, stored as adjacency lists.' CS2-c082 back: "
        "prefix 'Assume an undirected graph stored as adjacency lists.'",
    },
    {
        "id": "CS2b-cards-numbers-crossrefs",
        "check": "2.7 card numbers appear in their lesson; no card cites an absent section",
        "location": "course/modules/CS/CS2/cards.json, slice cards",
        "status": "PASS",
        "evidence": "v3_cards.py: every number of two or more digits (and decimals) in each slice card's front and back appears in its own lesson "
        "text (none missing, v3_cards.out). Section and Definition/Proposition references were matched to the lesson headings (checked by reading).",
    },
    {
        "id": "CS2b-cards-full-scan",
        "check": "2.7 one row per 10 cards sampled, plus full scan for grades, bases and duplicates",
        "location": "course/modules/CS/CS2/cards.json, 71 slice cards",
        "status": "PASS",
        "evidence": "Full scan (not a sample): all 71 slice cards read; v3_cards.out: grades T 56 and C 15; every C card has a basis; no bad grade; "
        "delta vs 9294b914: added CS2-c237, changed CS2-c163, CS2-c215 (outside-slice changes c195, c199 removed and c207, c217, c236 changed are "
        "for L09 and L11 and were not judged).",
    },
    # ---- structure, hours, DAG, notation, prose ----
    {
        "id": "CS2b-structure",
        "check": "2.9 lesson structure per BUILDER_RULES 4.2 (L05-L08)",
        "location": "L05.html..L08.html section order, labs, misconceptions, problems, key results, quiz, references",
        "status": "PASS",
        "evidence": "Order checked by reading: why it matters (<=120 words, check_pages), core sections, inline lab, where the canon breaks, "
        "misconceptions (3 each), problem set (M1-3, P1-3, E1-3, R1-3 in each lesson, each with a worked solution), key results, retrieval quiz "
        "(10, 9, 9, 9 items, each with an explanation), references. No debate (curriculum has no debate key for CS2; grep 'debate' = 0).",
    },
    {
        "id": "CS2b-hours",
        "check": "2.9 hours arithmetic (hub split and lesson hours)",
        "location": "course/modules/CS/CS2/index.html line 29 (data-hours-lessons=100, data-hours-project=30); L05-L08 data-hours",
        "status": "PASS",
        "evidence": "Lesson data-hours L01..L11 = 8,9,10,10,9,9,10,10,10,8,7 sums to 100 = hub data-hours-lessons; project 30; total 130 = curriculum "
        "hours (curriculum.json CS2 hours 130). L05 9, L06 9, L07 10, L08 10 match the eyebrow line in each page.",
    },
    {
        "id": "CS2b-dag",
        "check": "2.9 DAG: nothing used before definition, nothing defined twice (slice)",
        "location": "L05-L08 concept links and dfn ids; curriculum CS2 prereqs",
        "status": "PASS",
        "evidence": "Concept links (grep class=concept): L05 balanced-search-tree (own), big-o-complexity (L01), comparison-sorting (L04), "
        "exponential-and-logarithm and mathematical-induction (M1, now in CS2 prereqs per Architect decision issue 1); L06 graph-traversal (own), "
        "hash-map (L02), big-o; L07 dynamic-programming (own), hash-map, big-o, induction; L08 order-book-data-structure (own), hash-map, "
        "binary-search (L04). Each dfn id occurs once; link targets exist (see CS2b-gate-check-dag). Terms in quiz (see CS2b-L06-quiz-terms) are "
        "the only undefined-term defect found.",
    },
    {
        "id": "CS2b-notation",
        "check": "2.4 notation conformance against notation/notation.json",
        "location": "L05-L08 math; notation/notation.json (symbols T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q})",
        "status": "PASS",
        "evidence": "Registry read (8 symbols, 26 macros). Slice math uses no registered macro (\\E, \\Prob, \\N, ... absent) and none of the "
        "registered symbols. Collision check by grep: L05 'R' is a node name (lines 82, 537), not R^\\ast or R_f; L08 'Q' (line 627, P3 total "
        "quantity) is plain Q, not \\mathbb{Q}; L05 \\varphi (golden ratio, lines 52, 87-94) is not the registered \\Phi (normal CDF). Standard "
        "LaTeX commands are not custom macros. No symbol reused with another meaning inside the slice (N, M, h, n, lambda, delta, dp, f, d, m, k).",
    },
    {
        "id": "CS2b-banned-and-process-words",
        "check": "2.9 banned phrases (BUILDER_RULES 1.3-1.4) and process words in learner text",
        "location": "L05-L08 visible prose",
        "status": "PASS",
        "evidence": "grep (case-insensitive) for TODO, TBD, lorem, for brevity, beyond the scope, left as an exercise, it is important to note, "
        "studies show, experts agree, well known, obviously, clearly, you can add more, details omitted, builder, verifier, round, pin: no hit in "
        "prose; the only ellipses are inside code docstrings or math (e.g. L07.html line 385 '(k_1, ..., k_d)'), not omitted content. "
        "check_pages banned-string check PASS.",
    },
    {
        "id": "CS2b-scope-words",
        "check": "1.4 scope words (only, all, always, every, any, same, drives, exactly) have support",
        "location": "L05-L08 prose (e.g. L05 lines 52, 421-423; L06 lines 370, 388; L07 lines 507, 514; L08 lines 52, 557, 571)",
        "status": "PASS",
        "evidence": "Each scope word was checked against the proof or computation it relies on: 'never keeps a buy price at or above a sell price' "
        "(Prop 1.3); 'every AVL tree' (Prop 2.4, with the N >= 0 step fixed by CS2b-L05-math); 'optimal for {1,c}' (Problem R2); 'every "
        "source' (Lab 1, Part A, 200 sources); 'Proposition 2.3 ... at most' (proof). No unsupported 'always' or 'all' found.",
    },
    {
        "id": "CS2b-quiz",
        "check": "2.9 retrieval quiz (8-15 items, each explained) and answers",
        "location": "L05.html 567-641; L06.html 515-584; L07.html 663-725; L08.html 704-774",
        "status": "PASS",
        "evidence": "Item counts: L05 10, L06 9, L07 9, L08 9 (8-15 each). Each item has an explanation. Answers checked: L05 64, 2, 12, rotation 1 "
        "single left, 1.440420, 272, 'No' (Remark 3.2); L06 BFS queue, distance 3, 'No' (weights), 2|E| = 6, finish 6, 'disjoint or nested', "
        "27.82, |V|, 'ancestor or descendant'; L07 f(6)=2, 3 coins vs 2, AB/BA 1, 47/28, 1025, 10 bits, <= 2^b; L08 'earliest arrival at 10000', 3 "
        "tests for 7 prices, 1 share rests, integer cents, 'removed', index access, orders that rested, resting order's price. The L06 quiz item "
        "with undefined terms is recorded in CS2b-L06-quiz-terms.",
    },
    {
        "id": "CS2b-data-figures",
        "check": "2.8 data and figures (none in slice)",
        "location": "L05-L08 (no svg, no data-files, no figures-Lnn.js, no debate)",
        "status": "PASS",
        "evidence": "grep: '<svg', 'data-files', 'figures-L' count 0 in L05-L08; no chart or dataset in the slice; SIMULATED labels present "
        "(CS2b-lab-simulated-labels).",
    },
    {
        "id": "CS2b-L05-terms-avl",
        "check": "2.9 terms used before definition (defect class 5, L05)",
        "location": "L05.html line 52 (why it matters); Definition 2.1 at lines 66-67",
        "status": "FAIL",
        "evidence": "The name 'AVL tree' first appears in visible text at line 52 ('... that an AVL tree with \\(n\\) nodes has height at most ...'). "
        "Definition 2.1 (lines 66-67) names the AVL variant and defines the tree later in the same block. Line 52 has pointers for 'height' "
        "(Section 1) and for Proposition 2.4, but none for the name AVL. The round-3 wording change introduced this use.",
        "fix": "L05.html line 52: replace 'an AVL tree with \\(n\\) nodes' with 'a tree with \\(n\\) nodes that keeps the balance rule of "
        "Definition 2.1 (the AVL variant)'.",
    },
    {
        "id": "CS2b-misconception-counts",
        "check": "2.9 misconception count (at least 3 per lesson)",
        "location": "L05.html 431-440; L06.html 379-388; L07.html 523-532; L08.html 566-575",
        "status": "PASS",
        "evidence": "Counted in each page: L05 3, L06 3, L07 3, L08 3, each with the wrong belief, the correction and a computation or lab.",
    },
]

FRAGMENT = {
    "unit": "CS2",
    "slice": "b",
    "round": 3,
    "round_note": "Round 3 FINAL FULL verification of CS2 slice b (L05-L08 pages, lab twins L05-L08, the 71 slice cards) at pin 8196077d. "
    "Delta read from 9294b914: L05.html lines 52 and 487; L06.html lines 120 and 384; L07.html line 63; L08.html lines 148 and 155; "
    "tests/labs/CS2 L05-L08 unchanged; cards.json slice cards CS2-c163 (rewritten), CS2-c215 (C to T, basis removed), CS2-c237 (added). "
    "Everything was re-verified from scratch; no PASS row is carried from round 2.",
    "verifier": "Haiku independent verifier, CS2 slice b, round 3 (did not build CS2)",
    "pin": "8196077d",
    "base": "9294b914 (round-2 pin; previous fragment /Users/billyribeiro/.fanout/frags/S-CS2-b.round2.json read as context, its PASS rows not trusted)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyS3-CS2-b (detached at 8196077d, .venv symlinked to the main repo venv, vendor copied)",
    "scratch": "/tmp/cs2b_r3_cards.txt (card dump), /tmp/cs2b_r3_pt1.txt and /tmp/cs2b_r3_pt2.txt (pytest logs). Repo scripts: ledgers/CS2/scripts/CS2-b-r3/",
    "verified_at": "2026-11-09",
    "verdict": "FAIL",
    "rows": ROWS,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Scope: slice b = course/modules/CS/CS2/L05.html, L06.html, L07.html, L08.html; tests/labs/CS2/lab-CS2-L05-1.py .. lab-CS2-L08-1.py; the 71 cards of cards.json with lesson L05-L08. Hub, L01-L04, L09-L11, project and grader are other slices and were not judged (DAG and definition effects only).",
        "Delta (9294b914..8196077d) for the slice: L05.html line 52 (why it matters: 'an AVL tree with n nodes') and line 487 (P2 solution); L06.html line 120 (Prop 3.2 proof: forest and different-tree case) and line 384 (misconception 2 wording: 'depth-first search'); L07.html line 63 (coin set wording); L08.html lines 148 and 155 (Prop 3.2 hypothesis and proof: half-open interval). Lab twins unchanged. Cards: CS2-c163 rewritten, CS2-c215 grade C to T, CS2-c237 added. Outside the slice, cards c195 and c199 were removed and c207, c217, c236 changed (L09, L11); not judged.",
        "Mutants: none. The slice contains no project grader; lab twins are demonstrations and mutation testing applies to project graders only (verifier rulings). mutants=[] is correct.",
        "Judgement calls: (a) CS2b-L05-math fails on the unproved N(h-2) >= 0 step at line 82 although the P2 solution proves it (the proof is incomplete where it is used). (b) CS2b-L05-terms-avl fails because the name AVL is used at line 52 before Definition 2.1 with no pointer; a plain-words description precedes it, so this is a minor defect. (c) CS2-c215 is graded T as a procedure definition, the same convention as CS2-c058; the page says Remark 3.2 proves nothing about the repair, and the card states only the rule. (d) CS2-c069 grades T the closed-form constant 1/log2(phi) = 1.440420, which I recomputed (v3_numbers.out); accepted as exact-form arithmetic. (e) CS2-c163 is a duplicate of CS2-c107 (same lemma) after the round-2 rewrite; failed as duplicate.",
        "Notation: L08 P3 uses plain Q (the total live quantity) while the registry symbol is \\mathbb{Q}; these are different symbols, so no collision was recorded. L05 uses \\varphi (golden ratio), not the registered \\Phi. Not a finding.",
        "Consistency note (no row): L06 uses 'recursion tree' at line 369 and in the key-results source at line 507, while the proof at line 120 calls the structure a recursion forest; the key-results source could say 'recursion forest'. Not a defect of meaning.",
        "Labs: all four twins run alone under python -I -W error with no written files and no stderr; the page code equals each twin; each expected block equals its output; runtimes 0.0 s under Pyodide (page_smoke_r3.out). Labs are SIMULATED (seeded), graded C where read off.",
        "Independent recomputation: v3_numbers.py (AVL, BFS/DFS/brute force, LCS/coin DP, flat order-book reference) and v3_book_levels.py (level model with head passes and halving search) reproduce every number in the lab outputs and the prose.",
        "Not checked: (a) run_graders (no grader in slice; project belongs to another slice); (b) visual light/dark rendering beyond page_smoke's checks (no screenshots); (c) the full CI gate (the targeted gates per CLAUDE.md were run instead); (d) whole-repo ruff and mypy (twins only); (e) cross-slice pages beyond their effect on the DAG and definitions; (f) cards in other lessons beyond the lesson-level ones listed in the delta.",
    ],
    "summary": {
        "rows": len(ROWS),
        "pass": sum(1 for r in ROWS if r["status"] == "PASS"),
        "fail": sum(1 for r in ROWS if r["status"] == "FAIL"),
        "unverifiable": sum(1 for r in ROWS if r["status"] == "UNVERIFIABLE"),
    },
}

if __name__ == "__main__":
    out = Path("ledgers/CS2/CS2-b.json")
    out.write_text(json.dumps(FRAGMENT, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {out} rows={len(ROWS)} summary={FRAGMENT['summary']}")
