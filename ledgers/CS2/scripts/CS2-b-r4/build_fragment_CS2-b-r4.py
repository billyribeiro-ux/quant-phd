"""Writes ledgers/CS2/CS2-b.json for verifier round 4 (slice b, pin edbb7aa8). Evidence cites scripts under this directory."""
import json
from datetime import UTC, datetime

G = "ledgers/CS2/scripts/CS2-b-r4/"
rows = []


def row(rid, check, location, status, evidence, fix=None):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    rows.append(r)


row("CS2b-gate-check-pages", "2.9 structure gate (check_pages) for L05-L08 and unit",
    "course/modules/CS/CS2/L05.html..L08.html, cards.json", "PASS",
    G + "gates_structure_r4.out: 'check_pages CS2 L05: PASS', L06, L07, L08 PASS; 'check_pages CS2: PASS' (tools/check_pages.py --unit CS2 --page Lxx, then --unit CS2).")
row("CS2b-gate-check-dag", "2.9 DAG gate (check_dag) plus own dfn and link check",
    "L05-L08 links; dfn ids; concepts.html", "PASS",
    G + "gates_structure_r4.out: 'check_dag CS2: PASS'. " + G + "dfn_links_r4.out: 13 unit dfn ids, none duplicated; targets L01#def-big-o-complexity, L02#def-hash-map, L04#def-comparison-sorting, L04#def-binary-search, concepts.html#mathematical-induction and #exponential-and-logarithm (both present in course/concepts.html).")
row("CS2b-gate-check-projects", "2.6 project gate (unit level; slice has no project)",
    "course/modules/CS/CS2/project.html", "PASS",
    G + "gates_structure_r4.out: 'check_projects CS2: PASS' (not in slice; run for completeness).")
row("CS2b-gate-run-labs", "2.5 labs run (run_labs)",
    "tests/labs/CS2/lab-CS2-L05-1.py .. lab-CS2-L08-1.py", "PASS",
    G + "run_labs_r4.out: 'run_labs CS2: PASS (1/1)' for --page L05, L06, L07, L08 (each run alone).")
row("CS2b-gate-lab-exact", "2.5 labs: twin alone under -I -W error; page code == twin; expected == stdout",
    "course/modules/CS/CS2/L05.html..L08.html; tests/labs/CS2/lab-CS2-L0{5,6,7,8}-1.py", "PASS",
    G + "expected_vs_stdout_r4.out: each twin copied alone to an empty scratch dir (/tmp/cs2b_r4/run), run as python3 -I -W error: exit 0, stderr 0 bytes, stdout 31/17/10/15 lines; page expected block equal to stdout for L05, L06, L07, L08. Page code byte-identity to the twin is the run_labs check (run_labs_r4.out).")
row("CS2b-gate-page-smoke", "2.9 page_smoke (Chromium/Pyodide, console, external requests)",
    "course/modules/CS/CS2/L05.html..L08.html", "PASS",
    G + "page_smoke_r4.out: 'page_smoke modules/CS/CS2/L05..L08.html: PASS', 'page_smoke CS2: PASS', exit 0 (run alone). Lab runtimes 0.0 s.")
row("CS2b-gate-ruff-mypy", "lab twin lint, format and types",
    "tests/labs/CS2/lab-CS2-L05-1.py .. lab-CS2-L08-1.py", "PASS",
    G + "gates_misc_r4.out: ruff check 'All checks passed!'; ruff format --check '4 files already formatted'; mypy --no-incremental 'Success: no issues found in 4 source files'.")
row("CS2b-gate-pytest", "2.5 lab and page tests",
    "tests/test_labs.py -k CS2; tests/test_page_checks.py", "PASS",
    G + "pytest_labs_r4.out: pytest tests/test_labs.py -k CS2 -q exit 0 (14 tests); pytest tests/test_page_checks.py -q exit 0.")
row("CS2b-gate-verify-refs", "2.1 citations (registry integrity and unit run)",
    "references/references.json; L05 and L06 References sections", "PASS",
    G + "gates_misc_r4.out: verify_refs.py --offline 'offline integrity: 560 entries, 0 problems'; " + G + "verify_refs_unit_r4.out: 'live re-verification of CS2: 1 of 560 entries, 0 problems'. cormen2022introduction (registry key, Introduction to Algorithms, Fourth Edition) is named in L05 line 648 and L06 line 591 with no claim attributed to it; the slice has no data-cite or data-locator.")
row("CS2b-L05-lab-numbers", "2.2 numbers in L05 prose and expected block, recomputed from unrounded values",
    "L05.html lines 52, 99, 414, 422, 436, 440, 505, 519, 544; expected block 383-413", "PASS",
    G + "numbers_L05_L06_L07_r4.py (AVL written from Definitions 2.1 and 2.2, independent of the twin) -> numbers_L05_L06_L07_r4.out: final height 11; log_phi 501 = 12.9186; LL 63, RR 53, LR 55, RL 57; calls 63+53+2*(55+57)=340; 272/500 = 54.4% without rotation; plain BST height 64, AVL height 7, log_phi 65 = 8.6747; 1/log2(phi) = 1.44042 (prints 1.440420); log_phi 3 = 2.283 (prose 2.28); log_phi 8 = 4.321 (prose 4.32); ln 377 = 5.932, ln phi = 0.4812, log_phi 377 = 12.328 (prose 12.33); N(0..7) = 0,1,2,4,7,12,20,33; N(h)+1 >= phi^h for h=1..12 True.")
row("CS2b-L06-lab-numbers", "2.2 numbers in L06 prose and expected block, recomputed",
    "L06.html lines 103, 362, 388, 453, 459, 467; expected block", "PASS",
    G + "numbers_L06 block of numbers_L05_L06_L07_r4.out: 772 reachable pairs, 308 unreachable, 200 sources, 0 mismatches; 440 pairs, 0 violations; 619 edges, 1238 inspections, 1438 list work, 40000 matrix reads; 40000/1438 = 27.8164 (27.82); average degree 1238/200 = 6.19; weighted example s-a 10 (1 hop), s-b-a 2 (2 hops), s-a-c 11 (2 hops), s-b-a-c 3 (3 hops).")
row("CS2b-L07-lab-numbers", "2.2 numbers in L07 prose and expected block, recomputed",
    "L07.html lines 63, 210, 503-507, 532, 585-586, 597, 604, 610-611, 656", "PASS",
    G + "numbers_L05_L06_L07_r4.out: LCS ACGTACG/TGCATGC: stored 28, calls 47 (28 computed + 11 lookups + 8 base), naive 183, table 49; coins (1,3,4) amount 20: 20 stored, 56 memo calls, 20736 naive. " + G + "l07_seeded_facts_r4.out: first LCS pair GGTTA/G length 1; 6 of 30 coin cases impossible; greedy 3 vs optimum 2. P3 greedy failure first at a=6 (f values 1,2,1,1,2,2,2 for a=1..7 in numbers output).")
row("CS2b-L08-lab-numbers", "2.2 numbers in L08 prose and expected block, recomputed from the seeded stream",
    "L08.html lines 541-549, 575, 637-640, 653-654; expected block 534-548", "PASS",
    G + "l08_stream_facts_r4.py (replays Part B stream with the twin's classes) -> l08_stream_facts_r4.out: steps without a live order = [0, 2] (first and third messages), so 398 steps with a live order; 102 cancels: 25.5% of 400, 25.63% of 398; levels 185 created, 177 removed, 8 at end; 10 resting orders; 362 searches; largest comparison 4; queue steps 7 of 298 orders added. Part A hand-checked from the code (lines 439-459): 5@10000 from order 1, 2@10000 from order 2; best ask 10000; after cancel of order 3, 1@10000 from order 2, best bid 10000 best ask 10010.")
row("CS2b-L05-lab-hypothesis", "2.5 lab demonstrates its stated hypothesis; interpretation does not overreach",
    "L05.html lines 122-123, 414-423, 436, 452-455", "PASS",
    "Twin Part A checks invariant, height bound and in-order after each of 500 inserts (tests/labs/CS2/lab-CS2-L05-1.py lines 325-328); Part C checks N(h)+1 >= phi^h only for h=1..12 (line 365) and the prose says so (L05 line 296). Prose line 421 says the 500 insertions are one seeded run; code uses one seed. No overreach found.")
row("CS2b-L06-lab-hypothesis", "2.5 lab demonstrates its stated hypothesis; interpretation does not overreach",
    "L06.html lines 124-140, 362-388", "PASS",
    "Twin part_a compares bfs() dist with brute_min_hops (simple paths) on 40 graphs, part_b counts nested_or_disjoint violations on 40 graphs, part_d counts operations; prose matches (numbers above). L06 line 384 misconception path 2 hops and line 380 weighted example match Part C output (lab-CS2-L06-1 lines 301-317).")
row("CS2b-L07-lab-hypothesis", "2.5 lab demonstrates its stated hypothesis; interpretation does not overreach",
    "L07.html lines 206-210, 346, 507", "PASS",
    "Twin part_a asserts memo == table == exhaustive on 30 LCS pairs and asserts cells == m*n (lines 442-445); part_b asserts memo == table == exhaustive on 30 coin cases (lines 456-457); part_c counts. Prose line 507 states the equalities are checks on 60 instances, not proofs, and the exhaustive search is exponential; no overreach found.")
row("CS2b-L08-lab-hypothesis", "2.5 lab demonstrates its stated hypothesis; interpretation does not overreach",
    "L08.html lines 176, 549, 555-558", "PASS",
    "Twin Part B asserts identical trades to the flat reference and equal best bid/ask and resting ids after every message (lines 306-314); Part C asserts queue_steps <= orders_added and comparisons <= bit_length(L) (lines 339-343). Prose line 549 says the assumptions are not checked by the lab, which the code agrees with.")
row("CS2b-lab-simulated-labels", "2.5 SIMULATED labels and no-network, seeded RNG statements",
    "L05-L08 lab sections and twins", "PASS",
    "Each lab section and twin docstring carries SIMULATED and a seed (L05 twin line 126; L06 line 128; L07 line 213; L08 line 179). Grep of the four twins: no socket, urllib, requests or time module imports. Expected output runs under -I with no stdin.")
row("CS2b-L05-math", "2.4 mathematics: Lemma 2.3, Proposition 2.4, Proposition 3.1, Remark 2.5 and problems",
    "L05.html lines 82, 86-94, 107-113, 98-102, 487", "PASS",
    "Round-3 FAIL re-verified. Lemma 2.3 proof now begins with N(h) >= 0 by induction (line 82), so N(h)-N(h-1) = 1+N(h-2) >= 1 is supported; P2 (line 487) uses the same induction. Prop 2.4: M(h)=N(h)+1 satisfies M(h)=M(h-1)+M(h-2) and M(h) >= phi^h by induction, phi < 2 since sqrt5 < 3, phi^2 = phi+1; each step re-derived by hand. Prop 3.1 in-order argument re-derived. R2 tree balances re-checked (factor 1 at R, 5, 3, s; 0 at 2, 7, t).")
row("CS2b-L06-math", "2.4 mathematics: Lemma 2.1, Prop 2.2, Prop 2.3, Prop 3.2, Remark 2.4, problems",
    "L06.html lines 68-120, 393-441, 475-492", "PASS",
    "Lemma 2.1 induction re-derived; Prop 2.2 both directions and dist = delta re-derived (the walk-to-path step is covered by the definition of path in Section 1); Prop 2.3 hypotheses present (line 93); Prop 3.2 recursion-forest argument re-derived; P2/P3/R1/R2/R3 solutions re-derived. Symmetry claim (line 370) checked by reading each proof: symmetry enters only the degree-sum step of Prop 2.3.")
row("CS2b-L07-math", "2.4 mathematics: Theorem 2.2, Corollary 2.3, Theorem 3.3, Lemma 3.2, Prop 3.5, Prop 4.2, problems",
    "L07.html lines 73-92, 110-111, 118-158, 173-184, 192-203, 547-561, 569-629", "PASS",
    G + "numbers_L05_L06_L07_r4.out: f(0..6)=0,1,2,1,1,2,2 and f(6) via 3+3 (Example 2.4) re-derived; greedy 4+1+1 on 6. Theorem 3.3 cases (i)-(iii) and part (b) re-derived; Lemma 3.2 used with correct indices. Prop 4.2: 2^(b-1) < A+1 <= 2^b, 2^40 has 41 bits, 2^40+1 > 1e12. R1: 2^20+1 = 1048577, 21 bits. R2 (largest-coin-first optimal for {1,c}) re-derived. M1 f(9)=3 (2+2+5), M2 table 1, M3 54/40/14.")
row("CS2b-L08-math", "2.4 mathematics: Prop 1.3, Prop 2.2 (under Assumptions 1 and 2), Lemma 3.1, Prop 3.2, Prop 3.3, problems",
    "L08.html lines 82-85, 120-125, 134-140, 144-171, 587-629, 646-665", "PASS",
    "Prop 1.3 buy and sell cases re-derived (best-ask stopping condition gives A' > p when remainder rests). Prop 2.2 induction over fills re-derived using the named Assumptions 1 and 2 (stated as assumptions, not derived). Prop 3.2 length bound k-1 <= floor(log2 L) re-derived; L=7 gives 3 tests, L=8 gives 4. P1 bound n(floor(log2 n)+1), P3 min{q,Q} re-derived. M1 trades 2@10010 order 2 and 3@10010 order 3 with 1 left resting; M3 trades 1@10000, rests 2 at 10001.")
row("CS2b-L05-problems", "2.2 and 2.4 problems: worked solutions, tiers and answers",
    "L05.html lines 452-519 (M1-M3, P1-P3, E1-E3, R1-R3)", "PASS",
    "Every worked solution re-derived: M1 heights 2,3 and balance 1,1; M2 single left rotation, root 2; M3 N(5)=12; P1 left rotation; P2; P3 phi^2 = phi+1; E1 272/500 = 0.544; E2 log2 64 = 6, bound 8.6747; E3 log_phi 377 = 12.33, height at most 12; R1 double rotation (left-right) gives root 2; R2 7-node height-4 tree; R3 N(5)=12 and log_phi 8 = 4.32.")
row("CS2b-L06-problems", "2.2 and 2.4 problems: worked solutions, tiers and answers",
    "L06.html lines 400-526 (M1-M3, P1-P3, E1-E3, R1-R3)", "PASS",
    "M1 distances 0,1,1,2,3 and removal order 1,2,3,4,5 re-derived; M2 d=(1,2,3), f=(6,5,4); M3 6 adjacency entries; E1 572 positive-distance pairs; E2 27.82; E3 6.19; R2 connected component; R3 n^2 total operations; R1 DFS ancestor argument re-read.")
row("CS2b-L07-problems", "2.2 and 2.4 problems: worked solutions, tiers and answers",
    "L07.html lines 545-697", "PASS",
    "M1 f(9)=3 (2+2+5); M2 lambda(2,2)=1; M3 54 entries, 40 computed, 14 boundary; P1 single denomination proof by induction; P2 column-major order; P3 smallest failing amount 6; E1 stored amounts 20 (1 in D); E2/E3 explanation consistent with the counts; R1, R2, R3 re-derived.")
row("CS2b-L08-problems", "2.2 and 2.4 problems: worked solutions, tiers and answers",
    "L08.html lines 587-690", "PASS",
    "M1 (2@10010 from order 2, 3@10010 from order 3; resting asks 1@10010, 3@10020); M2 bounds 3 and 4; M3 1@10000 then 2 rest at 10001; E1 102/400 = 25.5%, 102/398 = 25.6% (rule re-run: steps without live order are 0 and 2); E2 queue-step explanation consistent with code (_front called only from submit); E3 L >= 8; R3 KeyError reading of self.levels[opposite][best] confirmed at twin line 178.")
row("CS2b-L06-quiz-terms", "2.2/2.9 quiz items use only defined terms",
    "L06.html lines 578-584; recursion forest defined at line 120", "PASS",
    "Round-3 FAIL re-verified. The quiz item (line 578) now asks about an undirected graph searched by Definition 3.1, the recursion forest, which is defined in the proof of Proposition 3.2 (line 120, 'Let the calls form the recursion forest ...') before any use in the quiz. The correct option (ancestor or descendant) matches Problem R1. Grep: no 'DFS tree' or 'non-tree' left in L06.")
row("CS2b-L06-canon-undirected", "2.9 'Where the canon breaks' undirected hypothesis statement",
    "L06.html lines 370", "PASS",
    "Each named statement's hypothesis checked: Lemma 2.1 and Prop 2.2 and Prop 3.2 proofs contain no symmetry use (read line by line); Prop 2.3 uses the degree sum (line 98). Statement correct.")
row("CS2b-L06-connected-component", "2.4 R2 'connected component' term defined before use",
    "L06.html lines 485", "PASS",
    "R2 defines the component inline ('the vertices joined to s by a path ... the connected component of s') before using the term; Prop 2.2 gives the discovered set.")
row("CS2b-L05-misconceptions-canon", "2.9 misconceptions and canon paragraphs",
    "L05.html lines 418-443", "PASS",
    "Misconception counts and values re-derived: plain BST 64, AVL 7; 272 of 500 without rotation; two-node height 2; the ' log2 n' claim corrected by Remark 2.5. Canon paragraph (deletion not covered) makes no claim.")
row("CS2b-key-results-ungraded", "2.3 every key-results claim carries a grade and matches its proof or lab",
    "L05.html 556-560; L06.html 504-508; L07.html 648-656; L08.html 691-697", "PASS",
    "Each row's grade re-graded against BLUEPRINT section 3 and ruling 13: proved results T (Remark 1.1, Lemma 2.3, Prop 2.4, Prop 3.1; Lemma 2.1, Prop 2.2, Prop 2.3, Prop 3.2; Theorem 2.2, Cor 2.3, Example 2.4, Theorem 3.3, Cor 3.4, Prop 3.5, Prop 4.2; Prop 1.3, Prop 2.2 under named assumptions, Lemma 3.1, Prop 3.2, Prop 3.3); lab-only results C naming the lab (L05 line 560; L06 line 508; L07 655-656; L08 696-697).")
row("CS2b-grades", "2.3 grade letters and claim grades on the four pages",
    "data-grade attributes in L05-L08", "PASS",
    G + "strip.py output: every [G:x] token is a valid grade (T, A, B, C, D, X); inline claims follow the key-results grades above.")
row("CS2b-cards-trivia", "2.7 cards are not trivia (rule 2.7)",
    "cards.json (73 slice cards)", "FAIL",
    "CS2-c103 (cards.json line 713): 'What is a FIFO queue?' restates the glossary sentence of L08 Section 1 and tests nothing beyond it. Rule 2.7 says not trivia. Ruling 26: card style is LOW and non-blocking; list in plans/KNOWN-ISSUES.md.",
    "Replace CS2-c103 with a card that uses the queue, e.g. 'Which order does a FIFO queue at one price fill first?' citing Definition 2.1 (order of arrival), or delete it.")
row("CS2b-cards-correctness", "2.7 one card per 10 sampled, plus all slice cards against the current lesson text",
    "cards.json CS2-c056..c239 (73 slice cards)", "PASS",
    G + "cards_r4.py -> cards_r4.out: 73 slice cards (L05 18, L06 14, L07 22, L08 19); every number token in every back appears verbatim in its own lesson page. Each card read against its lesson paragraph: CS2-c060/c061/c062/c064 match Lemma 2.3, Prop 2.4, Prop 3.1, Remark 1.1; c066 and c068 match Lab 1 Part A; c074-c078 match Lemma 2.1, Prop 2.2, Prop 2.3, Prop 3.2 with hypotheses; c080 and c081 match Lab 1 Part C and the misconception; c087-c095 match Theorem 2.2, Cor 2.3, Example 2.4, Theorem 3.3, Lemma 3.2, Cor 3.4, Prop 3.5, Prop 4.2; c100-c114 and c223-c240 match Defs 1.1-2.1, Props 1.3, 2.2, 3.2, 3.3, Lemma 3.1 and the Lab 1 Part B/C counts.")
row("CS2b-cards-duplicates", "2.7 full scan for duplicate ids and semantic duplicates",
    "cards.json", "PASS",
    G + "cards_r4.out: 204 unit cards, 0 duplicate ids, 0 duplicate fronts. Round-3 semantic duplicate (CS2-c107 vs CS2-c163) is resolved: CS2-c163 no longer exists in cards.json, and CS2-c107 (T, Lemma 3.1) is the only queue-steps card. Pairwise read of the 73 slice fronts: no two cards ask the same question.")
row("CS2b-cards-hypotheses", "2.7 cards carry the hypotheses of the proposition they cite",
    "cards.json CS2-c077 (line 541), CS2-c082 (line 570), others", "PASS",
    "Round-3 FAIL re-verified. CS2-c077 now begins 'Assume an undirected graph with |V| vertices and |E| edges, stored as adjacency lists' (matches Prop 2.3 line 93); CS2-c082 begins 'Assume an undirected graph stored as adjacency lists'. Every other slice card that cites a proposition with hypotheses states them (c074, c076, c078, c087, c088, c090-c094, c105-c110, c222, c224).")
row("CS2b-cards-numbers-crossrefs", "2.7 every card number appears in its lesson; cross-references",
    "cards.json slice cards", "PASS",
    G + "cards_r4.out: 'card numbers not found verbatim in own lesson text: []'. Cross-references (Definition, Proposition, Problem, Misconception and Lab numbers) checked by reading: 'Misconception 1' (L05 quiz line 582, L06 quiz line 538), 'Misconception 2' (L06 line 369), 'Misconception 3' (L08 quiz line 742), 'Proposition 3.3, item 1' (L08 quiz line 756) all resolve.")
row("CS2b-cards-full-scan", "2.7 full scan of slice cards for correctness and grade consistency",
    "cards.json 73 slice cards", "PASS",
    "Every slice card read in full (dump of L05, L06, L07, L08 cards). Each grade matches the key-results row it mirrors (c060-c062, c064 T; c063, c065, c066, c068 C; c074-c078 T and c075, c080 C; c087-c095 T; c097, c098, c232 C; c100-c110 T; c113, c114, c237, c240 C). c102 is a convention graded C with basis Section 1 and Part A (ruling 13).")
row("CS2b-structure", "2.9 structure and section order; minimum counts; banned phrases",
    "L05-L08 pages", "PASS",
    G + "gates_structure_r4.out (check_pages PASS for all four pages, which enforces section order, 3 misconceptions, 3 problems per tier, key results table, 8-15 quiz items, references, study hours). Prev/next links: L05<-L04, L05->L06, L06->L07, L07->L08, L08->L09 titles match the hub and L09 title.")
row("CS2b-hours", "2.9 hours split sums to curriculum figure; hub arithmetic",
    "L05 9 h, L06 9 h, L07 10 h, L08 10 h; index.html line 143 and lesson list", "PASS",
    "Lesson headers L05 9, L06 9, L07 10, L08 10 match hub lines 149-152. Hub: 100 lesson hours = 8+9+10+10+9+9+10+10+10+8+7 = 100 (L01 8, L10 8, L11 7 from their headers). Hub 30 h project, 130 h total.")
row("CS2b-dag", "2.9 DAG: nothing used before defined, nothing defined twice, outside closure",
    "L05-L08 'Uses' lines and links", "PASS",
    G + "dfn_links_r4.out and check_dag PASS. L05 uses comparison sorting (L04), big-O (L01), induction and exponential/log (concepts); L06 uses hash map (L02) and big-O; L07 uses hash map and big-O; L08 uses hash map (L02) and binary search (L04); all are in the prerequisite closure. Each dfn defined once.")
row("CS2b-notation", "2.4/13 notation: every symbol against notation/notation.json and local definitions",
    "L05-L08 math segments (macro census by script)", "PASS",
    "Registered program-wide symbols (notation/notation.json): T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, Q. The slice uses none of them (no T as a symbol in math; no Phi, gamma, R_f or Q). Slice-local symbols are defined in their lessons: phi (L05 line 87), N(h) and M(h) (Def 2.2, proof line 92), A (AVL tree, Lemma 2.3), delta(v) and dist(v) (L06 Sec 2), ell (Lemma 2.1 proof), d(v), f(v) (Def 3.1), f(a) (Def 2.1 of L07, a different symbol from L06 f(v) and defined per lesson), lambda(i,j) (Def 3.1), dp (Cor 2.3, 3.4). Macro census: L05-L08 use no \\mathbb or other registered macro; \\R is not needed.")
row("CS2b-banned-and-process-words", "2.9 banned phrases and process words in learner text",
    "L05-L08 visible prose", "PASS",
    "check_pages PASS (banned strings). Process-word scan of stripped visible text for round, verif, builder, audit, sweep, fix, revis, todo, draft, reviewer, ledger, erratum, correction, previous, earlier, updated, pending, placeholder, agent, claude: only mathematical or lab words hit ('fixed seed', 'fixed constant K', 'Before that' in a proof). No process words.")
row("CS2b-scope-words", "2.2/2.4 scope words (only, all, always, every, any, same, exactly) need computation or an explicit hypothesis",
    "L05-L08 visible prose", "PASS",
    "Scope-word sentences listed by script (strip.py + grep) and each checked: 'every balance factor' (Def 2.1), 'every AVL tree of height h' (Lemma 2.3), 'for every h' (Prop 2.4, lab checks only h<=12, stated), 'every source' and 'every pair' (L06 Parts A and B, counts 200 and 440), 'every entry', 'exactly mn' (L07, asserted in code), 'every call' (Def 1.1 L07), 'only' in 'Exhaustive search ... only at small sizes' (design statement), 'on this run only' (L05, L06, L08 seeded runs). No unsupported scope word.")
row("CS2b-quiz", "2.9 retrieval quiz: 8-15 items, correct answers and explanations",
    "L05 lines 571-641; L06 519-584; L07 667-725; L08 708-774", "PASS",
    "Correct options (data-correct) re-checked by computation: L05 64 (plain BST height), 2 (balance 3-1), single left rotation, log_phi(n+1), 272, 'No'; L06 BFS queue, 'No' (weighted), 3 edges, 6 (finish of vertex 1), disjoint-or-nested, |V|, ancestor-or-descendant; L07 min formula, 3 coins vs 2, agree-on-seeded-instances, at most 2^b; L08 earliest arrival at 10000, exact prices, removed with queue discarded, best bid or ask, orders that rested, resting price. Explanations match the page.")
row("CS2b-data-figures", "2.8 data and figures: none in slice",
    "L05-L08", "PASS",
    G + "grep: no <svg>, <figure> or <img> in L05-L08; no data-files attribute; no script beyond site and KaTeX includes. No dataset or figure to check.")
row("CS2b-L05-terms-avl", "2.9/2.6 'AVL' and 'balanced search tree' used before Definition 2.1",
    "L05.html line 52 and Definition 2.1 lines 66-67", "PASS",
    "Round-3 row re-verified. Line 52 now reads 'a tree with n nodes that keeps the balance rule of Definition 2.1 (the AVL variant)'; the name is used with an explicit forward pointer to Definition 2.1 in the same section, and balanced search tree is introduced at line 39 metadata with the dfn at Definition 2.1. Judged PASS as a forward reference (same pattern as 'denominations, Definition 2.1' in L07 line 63). Not a term used without pointer.")
row("CS2b-misconception-counts", "2.9 misconception count (>=3 per lesson) and each misconception correct",
    "L05 lines 431-440; L06 379-388; L07 523-528; L08 566-575", "PASS",
    "Three misconceptions per lesson (L05 three, L06 three, L07 three, L08 three). Each wrong statement and correction re-derived; the L06 triangle and L08 level statements verified by the stream/code.")
row("CS2b4-cards-balanced-tree", "2.7 card claim matches the lesson definition (balanced search tree: 'aim', proved only for AVL)",
    "course/modules/CS/CS2/cards.json line 403 (CS2-c057); L05.html line 67 (Definition 2.1) and line 67 (Proposition 2.4)", "FAIL",
    "CS2-c057 (grade T) back: 'A binary search tree that restructures itself after each change, so that its height stays logarithmic in the number of its keys. This unit uses the AVL variant (Definition 2.1).' Definition 2.1 (L05.html line 67) says the structure restructures itself 'with the aim of keeping its height logarithmic', and says Proposition 2.4 proves the height bound only for the AVL variant. The card states as a T-graded fact a guarantee that the lesson calls an aim and proves only for AVL. False or unproved statement under ruling 26: blocking.",
    "In CS2-c057 replace 'so that its height stays logarithmic in the number of its keys' with 'with the aim of keeping its height logarithmic in the number of its keys (Definition 2.1). Proposition 2.4 proves the height bound for the AVL variant, which this unit uses.' Regenerate nothing else; re-run check_pages --unit CS2.")
row("CS2b4-L06-P2-forest-wording", "2.9 wording: problem refers to the recursion forest 'of Definition 3.1'",
    "L06.html line 433 (P2); recursion forest first defined in the proof of Proposition 3.2 at line 120", "FAIL",
    "P2 says 'In the recursion forest of Definition 3.1'. Definition 3.1 (line 110) does not define a forest; the forest is introduced in the proof of Proposition 3.2 (line 120). The term is defined before its uses, so the defect is a pointer, not an undefined term. Ruling 26: wording, LOW, non-blocking; list in plans/KNOWN-ISSUES.md.",
    "Change 'of Definition 3.1' in P2 to 'of the proof of Proposition 3.2' (or 'of the search of Definition 3.1, as in the proof of Proposition 3.2').")

verdict = "FAIL" if any(r["status"] != "PASS" for r in rows) else "PASS"
blocking = [r["id"] for r in rows if r["status"] != "PASS" and "LOW" not in r["fix"] and "ruling 26: " not in r["evidence"]]
counts = {s: sum(1 for r in rows if r["status"] == s) for s in ("PASS", "FAIL", "UNVERIFIABLE")}
fragment = {
    "unit": "CS2",
    "slice": "b",
    "round": 4,
    "round_note": "Round 4 FINAL FULL verification of CS2 slice b (L05-L08 pages, lab twins L05-L08, the 73 slice cards) at pin edbb7aa8. Delta from round-3 pin 8196077d read in full (ledgers/CS2/scripts/CS2-b-r4/delta_slice_8196077d_edbb7aa8.diff): L05.html lines 52 and 82; L06.html lines 60, 369, 384, 433, 475-476, 507, 578; L07.html lines 63, 65, 111, 513-514; cards.json (CS2-c057 rewritten, CS2-c077/c082 hypotheses, c163 removed, c215/c237/c240 changed). Twins L05-L08 and L08.html unchanged. Every row re-verified from scratch at this pin; no PASS row is carried from round 3, as the task requires.",
    "verifier": "Haiku 5.5 independent verifier, CS2 slice b, round 4 (did not build CS2)",
    "pin": "edbb7aa8",
    "base": "8196077d (round-3 pin; previous fragment /Users/billyribeiro/.fanout/frags/S-CS2-b.round3.json read as context, its PASS rows not trusted)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyS4-CS2-b (detached at edbb7aa8, .venv symlinked to the main repo venv, vendor copied)",
    "scratch": "/tmp/cs2b_r4 (twin copies and outputs of the -I -W error runs). Repo scripts and outputs: ledgers/CS2/scripts/CS2-b-r4/",
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "verdict": verdict,
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Lesson and card slice: mutation testing does not apply (ruling 9 and the verifier rules: lab twins are demonstrations; no project grader in this slice). No mutants authored, none listed.",
        "Ruling 26 (convergence): the blocking row is CS2b4-cards-balanced-tree (a T-graded card claim the lesson does not prove). The LOW rows (CS2b4-L06-P2-forest-wording, CS2b-cards-trivia) are wording and card style and are non-blocking; per ruling 26 they go to plans/KNOWN-ISSUES.md with their ledger ids.",
        "All four lesson pages were read in full as stripped text with source line numbers (scripts/strip.py); all twins read in full; all 73 slice cards read in full; all Definitions, Propositions, Lemmas, Remarks, Examples, problem solutions, key-results rows, misconceptions and quiz items read.",
        "Round-3 FAIL rows re-verified: CS2b-L05-math, CS2b-L06-quiz-terms, CS2b-cards-duplicates, CS2b-cards-hypotheses, CS2b-L05-terms-avl are PASS at this pin (evidence rows above).",
        "Judgement calls: 'AVL variant' at L05 line 52 is a forward pointer to Definition 2.1 and is PASS; 'recursion forest' is defined inline in the proof of Proposition 3.2 and is PASS; L05 1/log2(phi) = 1.440420 graded T as a constant the page states (not SIMULATED data); CS2b-L08 E2 explanation of the 7 queue steps is consistent with the code (_front is called only in submit) but was checked by reading, not by instrumenting each step.",
        "Existing files in ledgers/CS2/scripts/CS2-b-r4/ from an earlier lineage (build_fragment_r4.py, recompute_r4.py, delta_cards.diff, delta_lessons_labs.diff) were tracked before this round; they were not run or relied on. This round's files use distinct names (cards_r4.py, numbers_L05_L06_L07_r4.py, l08_stream_facts_r4.py, l07_seeded_facts_r4.py, dfn_links_r4.py, expected_vs_stdout_r4.py, strip.py, build_fragment_CS2-b-r4.py).",
        "ledgers/CS2/CS2-b.json existed (round 8, pin ce7b382, from another lineage) and is replaced by this round-4 fragment at the path the task specifies.",
    ],
    "summary": f"Slice b (L05-L08, twins, 73 cards), round 4, pin edbb7aa8. Rows: {counts['PASS']} PASS, {counts['FAIL']} FAIL, {counts['UNVERIFIABLE']} UNVERIFIABLE. Blocking: CS2b4-cards-balanced-tree. LOW (non-blocking under ruling 26): CS2b4-L06-P2-forest-wording, CS2b-cards-trivia. Gates green at the pin: check_pages, check_dag, check_projects, run_labs, page_smoke, ruff, mypy, pytest CS2 labs and page checks, build_site --check, verify_refs offline and unit.",
}
with open("ledgers/CS2/CS2-b.json", "w", encoding="utf-8") as fh:
    json.dump(fragment, fh, indent=2, ensure_ascii=False)
    fh.write("\n")
print("rows", len(rows), counts, "verdict", verdict, "blocking", blocking)
