"""Builds ledgers/CS2/CS2-b.json (round 4, slice CS2-b: L05-L08 and lab twins). Run with -I from the checkout."""

import json
from datetime import datetime, UTC
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
L = "course/modules/CS/CS2/"
DELTA = (
    "git diff -U0 aa3c26c 2657ab5 hunks in this slice: L05.html 52,67,77,82,87,436; L06.html 380; "
    "L07.html 101,106,164,169,579; L08.html 112-116,121,131,257,546,689; tests/labs/CS2/lab-CS2-L08-1.py 81; "
    "cards.json 47 cards changed (ledgers/CS2/scripts/CS2-b-r4/delta_cards.diff)"
)


def carry(files_and_lines):
    return (
        "Carried from round 3 (" + files_and_lines + " byte-identical since the previous pin aa3c26c; "
        "not in the round-4 delta: " + DELTA + "):"
    )


def ok(id_, check, location, evidence):
    return {"id": id_, "check": check, "location": location, "status": "PASS", "evidence": evidence}


def bad(id_, check, location, evidence, fix):
    return {"id": id_, "check": check, "location": location, "status": "FAIL", "evidence": evidence, "fix": fix}


rows = [
    # ---------------- commands, re-run on 2657ab5
    ok("CS2b-cmd-pin", "2.9-structure", "git checkout /tmp/verifyB4-CS2-b",
       "git log -1 --oneline: 2657ab5 Batch 2: fixes for independent verification round 3; git status shows no tracked "
       "change. " + DELTA + "."),
    ok("CS2b-cmd-run_labs", "tools/run_labs.py --unit CS2", "tools/run_labs.py",
       "rc=0; 'run_labs CS2: PASS (14/14)'; scratch /tmp/CS2-v/CS2-b-r4/run_labs.txt"),
    ok("CS2b-cmd-lab-cpython-W-error", "python -I -W error on lab-CS2-L05-1..L08-1",
       "tests/labs/CS2/lab-CS2-L05-1.py, L06-1, L07-1, L08-1",
       "each rc=0; outputs /tmp/CS2-v/CS2-b-r4/lab-L0n.out (31, 17, 10, 15 lines) equal the <pre class=\"expected\"> "
       "blocks of L05.html..L08.html line for line (script comparison: True for all four); the code block of each page "
       "equals its twin (script: True for all four)"),
    ok("CS2b-cmd-page_smoke", "tools/page_smoke.py --unit CS2 --pages L05 L06 L07 L08", "tools/page_smoke.py",
       "rc=0; 'page_smoke CS2: PASS'; lab-CS2-L08-1 0.0 s; scratch /tmp/CS2-v/CS2-b-r4/page_smoke.txt"),
    ok("CS2b-cmd-check_pages", "tools/check_pages.py --unit CS2; tools/check_projects.py --unit CS2",
       "tools/check_pages.py, tools/check_projects.py",
       "rc=0 for both: 'check_pages CS2: PASS', 'check_projects CS2: PASS'"),
    ok("CS2b-cmd-check_dag", "tools/check_dag.py --unit CS2", "curriculum/curriculum.json CS2 entry",
       "rc=0; 'check_dag CS2: PASS'; CS2 prereqs read from curriculum.json are ['CS1', 'M1'] (plan Architect issue 1)"),
    ok("CS2b-cmd-lint", "ruff check and ruff format --check on the four lab twins",
       "tests/labs/CS2/lab-CS2-L05-1.py..L08-1.py", "'All checks passed!'; '4 files already formatted'"),
    ok("CS2b-cmd-verify_refs", "tools/verify_refs.py --offline; tools/verify_refs.py --unit CS2",
       "references/references.json; tools/verify_refs.py",
       "offline: 'integrity: 560 entries, 0 problems', rc=0; live --unit CS2: '1 of 560 entries, 0 problems', rc=0"),
    ok("CS2b-cit-cormen", "2.1-citations (key exists; no locator or claim attributed)",
       L + "L05.html:648; " + L + "L06.html:591",
       "references/references.json entry cormen2022introduction read this round: 'Introduction to Algorithms, Fourth "
       "Edition', year 2022, pages null, container null, no DOI, verified_by openlibrary. Both pages attribute no claim "
       "to it and state that the record has no locator; both paragraphs are unchanged in the round-4 delta"),
    # ---------------- numbers (re-derived this round, not carried)
    ok("CS2b-num-L05-lab", "2.2-numbers (a) computed", L + "L05.html:414 interpretation; lab-CS2-L05-1 output",
       "lab output equals every printed value at line 414 (invariant True x3, height 11, 501-key bound 12.9186, 340 rotation "
       "calls, 272 of 500, plain height 64, AVL height 7, bound 8.6747, 1.440420); ledgers/CS2/scripts/CS2-b-r4/"
       "recompute_r4.py gives log_phi 501 = 12.9186 and log_phi 65 = 8.6747 and 340 = 63+53+2(55+57)"),
    ok("CS2b-num-L05-derived", "2.2-numbers (c) derived", L + "L05.html:99, 414, 519, 544 (R3), 440 (misconception)",
       "recompute_r4.py: 1/log2(phi)=1.440420090 (shown 1.440420); ln3/lnphi=2.2830 (shown 2.28); ln8/lnphi=4.3213 "
       "(shown 4.32); ln377/lnphi=12.3277 (shown 12.33; ln377=5.9322, lnphi=0.4812); 272/500=0.5440 (shown 54.4%); "
       "every displayed digit agrees with its unrounded value"),
    ok("CS2b-num-L06", "2.2-numbers (a)+(c)", L + "L06.html:362 interpretation, 388, 519-ish E2 and E3 (459-468)",
       "lab-L06.out: 772 reachable pairs, 308 unreachable, 200 sources; 772-200=572 positive pairs (recompute_r4.py); "
       "pairs 440 = 8*(3+6+10+15+21) recomputed; 1238 = 2*619; 1438 = 200+1238; 40000 = 200*200; 40000/1438 = 27.8164 "
       "shown 27.82; 1238/200 = 6.19"),
    ok("CS2b-num-L07", "2.2-numbers (a)+(c)", L + "L07.html:210, 507, 603-611, 622, 653-656, 697-711",
       "lab-L07.out: LCS 3, 49 cells, 28 stored, 47 memo calls, 183 no-memo calls, coins amount 20 -> 5 coins, 56 memo "
       "calls, 20736 no-memo calls; recompute_r4.py re-derives 28, 47, 183, (5, 20, 56), 20736, f(0..6)=0,1,2,1,1,2,2, "
       "f(9) for {2,5}=3, 2^40 has 41 bits and exceeds 10^12, 2^20+1=1048577 with 21 bits, bits(1000)=10"),
    ok("CS2b-num-L08", "2.2-numbers (a)+(c)", L + "L08.html:546, 572, 637, 689",
       "lab-L08.out (298 new, 102 cancels, 117 traded messages, 177 executions, 10 resting, best bid 9980, best ask 9989, "
       "185 created, 177 removed, 362 searches, largest 4) reproduced by an independent list-based book in "
       "recompute_r4.py on the same seeded stream; 102/400 = 25.5%"),
    # ---------------- grades
    ok("CS2b-grade-L05", "2.3-grades", L + "L05.html section 7 key results (556-560)",
       carry(L + "L05.html lines 556-560") + " grades T, T, T, T and 'not graded' re-read this round"),
    ok("CS2b-grade-L06", "2.3-grades", L + "L06.html section 7 key results (504-508)",
       carry(L + "L06.html lines 504-508") + " grades T, T, T, T and 'not graded' re-read"),
    ok("CS2b-grade-L07", "2.3-grades", L + "L07.html section 8 key results (648-656)",
       carry(L + "L07.html lines 648-656") + " rows 655-656 are C and name Lab 1 parts A-C (SIMULATED)"),
    ok("CS2b-grade-L08", "2.3-grades", L + "L08.html section 7 key results (689)",
       "line 689 read this round: 'Under Assumptions 1 and 2 of Proposition 2.2 ... price-time priority' is T; the "
       "hypotheses are at lines 111-114 and the proof at 121; grade C rows at 693-694 name the SIMULATED stream and one run"),
    # ---------------- mathematics
    ok("CS2b-math-L05-proofs", "2.4-mathematics",
       L + "L05.html Lemma 2.3 (76-83), Proposition 2.4 (85-95), Remark 2.5 (97-100), Proposition 3.1 (106-114)",
       "lines 77, 82, 87 changed by notation only (T -> calA). Re-derived: N nondecreasing; induction with h_2 in "
       "[h-2, h-1]; M(h)=N(h)+1 satisfies M(h)=M(h-1)+M(h-2); phi^2=phi+1 from (6+2 sqrt5)/4; phi<2 from sqrt5<3; "
       "in-order A,x,B,y,C before and after the right rotation"),
    ok("CS2b-math-L05-problems", "2.4-mathematics (problems)", L + "L05.html M1-M3 (453-467), P1-P3 (478-494), E3, R1-R3 (528-544)",
       carry(L + "L05.html lines 453-544 (solutions unchanged)") + " re-checked this round: M2 balance factors, R1 "
       "left-right case, R2 tree (heights 4, 7 nodes, balance factors in {-1,0,1}), R3 N(5)=12 and log_phi 8 = 4.32"),
    ok("CS2b-math-L06-proofs", "2.4-mathematics", L + "L06.html Lemma 2.1 (68-75), Proposition 2.2 (78-89), Proposition 2.3 (92-99), Proposition 3.2 (114-121)",
       carry(L + "L06.html lines 68-121") + " re-read this round: Lemma 2.1 induction, Prop 2.2 both inequalities, "
       "Prop 2.3 degree sum, Prop 3.2 nesting by recursion tree; R1 (476-479) and P2 re-derived"),
    ok("CS2b-math-L07-proofs", "2.4-mathematics",
       L + "L07.html Theorem 2.2 (72-90), Corollary 2.3 (94-107), Example 2.4 (109-112), Lemma 3.2, Theorem 3.3, Corollary 3.4, Proposition 3.5, Proposition 4.2 (191-203)",
       "Corollary 2.3 statement and proof changed (dp for T, lines 101, 106); re-proved by strong induction. Theorem 2.2 "
       "upper/lower/infinite cases re-derived; Theorem 3.3 cases (i)-(iii) and part (b) re-derived; Prop 4.2 bounds "
       "2^(b-1) < A+1 <= 2^b re-derived; script confirms f = dp for {1,3,4} up to 6 and f(6)=2"),
    ok("CS2b-math-L08-lemmas", "2.4-mathematics",
       L + "L08.html Proposition 1.3 (70-86), Proposition 2.2 (108-122), Lemma 3.1 (133-141), Proposition 3.2 (143-156), Proposition 3.3 (158-172)",
       "Prop 2.2 hypotheses (112-114) and proof (121) re-read: Assumption 1 used for the head, Assumption 2 for the level, "
       "the arrival-order hypothesis for the earliest live order; Prop 1.3 proof cases checked; Prop 3.2 length bound "
       "re-derived (length after k tests <= floor(L/2^k)); Prop 3.3 items match the code (_search, insert, delete)"),
    # ---------------- labs
    ok("CS2b-lab-L05", "2.5-labs", "tests/labs/CS2/lab-CS2-L05-1.py; " + L + "L05.html Lab 1 paragraph (123) and interpretation (414)",
       "twin unchanged in this round; the hypothesis paragraph matches the code (500 seeded keys, sorted 1..64, Part C "
       "N(h) for h=1..12, two-node height); 'checks, not proves' wording matches Remark 3.2 (118)"),
    ok("CS2b-lab-L07", "2.5-labs", "tests/labs/CS2/lab-CS2-L07-1.py; " + L + "L07.html Lab 1 paragraph (210), interpretation (507)",
       "'Expected result' (210) matches the output: agreement on 30 + 30 instances, 49 cells, 28 stored, 47 calls, 183 "
       "no-memo calls, 3 vs 2 coins, 20 amounts; the interpretation (507) describes base calls and exhaustive search "
       "correctly against the code"),
    ok("CS2b-lab-L08", "2.5-labs", "tests/labs/CS2/lab-CS2-L08-1.py; " + L + "L08.html Lab 1 paragraph (176) and interpretation (546)",
       "'Expected result' (176) matches the printed lines; Part A hand reading (546) matches the output (5 + 2 at 10000, "
       "1 share left, cancel of order 3, best bid 10000, best ask 10010); the stream sentences match Part B; the bound "
       "sentence (546) matches the Part C assertion (comparisons <= bit_length of list length). Scope issues are the "
       "separate FAIL rows CS2b3-L08-scope-words, CS2b4-L08-any-stream and CS2b4-L08-three-counts"),
    ok("CS2b-L06-lab-exhaustive", "2.5-labs", "tests/labs/CS2/lab-CS2-L06-1.py brute_min_hops; " + L + "L06.html Lab 1 paragraph (125)",
       carry("tests/labs/CS2/lab-CS2-L06-1.py (byte-identical to aa3c26c) and " + L + "L06.html:125") +
       " the twin's docstring 'two paths differ' is a separate FAIL row (CS2b4-L06-twin-docstring)"),
    # ---------------- cards
    bad("CS2b-cards-consistency", "2.7-cards (aggregate)", L + "cards.json CS2-c056..c115 (60 cards)",
       "re-checked all 60 cards this round against the CURRENT lesson text. Remaining mismatches are separate rows "
       "CS2b4-cards-c080, CS2b4-cards-c084, CS2b4-cards-notation-T (c060, c061, c088, c092). CS2b3-card-c082 and "
       "CS2b3-card-c094 are fixed and PASS below. All other cards in the slice agree with their lesson text and claims",
       "fix each card named in the separate FAIL rows (CS2b4-cards-c080, CS2b4-cards-c084, CS2b4-cards-notation-T)"),
    ok("CS2b-cards-dupe-scan", "2.7-cards (full duplicate scan)", L + "cards.json (167 cards, all lessons)",
       "re-run: 167 cards, no duplicate id, no duplicate front (case-insensitive)"),
    ok("CS2b-cards-coverage", "2.7-cards (coverage)", L + "cards.json lesson field for L05..L08",
       "60 cards with lesson in L05..L08 (c056..c115), each with a lesson field, grade present; grade C cards carry a basis "
       "naming the lab (c065, c066, c068, c075, c079, c080, c097, c098, c099, c113, c114, c115)"),
    ok("CS2b4-cards-L05", "2.7-cards (sample of 14, c056-c069)", L + "cards.json CS2-c056..c069",
       "each card checked against L05 text: c056 Section 1; c057-c059 Definitions 2.1 and 2.2 and Lemma 2.3 remark; c062 "
       "Prop 3.1; c063 Remark 3.2; c064 Remark 1.1; c066 (changed) matches line 414 and the 500-insertion check; c067; "
       "c068 (grade C, basis Lab 1 Part A) matches 436; c069 Remark 2.5. c068 keeps 'only at a node' while the lesson "
       "sentence (436) drops 'only'; the claim is the same and rebalance() in the twin calls rotations only in its +-2 "
       "branches, so PASS"),
    ok("CS2b4-cards-L08", "2.7-cards (sample of 16, c100-c115)", L + "cards.json CS2-c100..c115",
       "checked against L08 Definitions 1.1, 1.2, 2.1, Props 1.3, 2.2, 3.2, 3.3, Lemma 3.1, Example 2.3 and Lab 1 counts "
       "(185, 177, 362, 4, 7, 298, 10 resting); c113-c115 grade C basis names the lab; c112 matches Prop 1.3"),
    ok("CS2b4-cards-L07-R-part", "2.7-cards (c089, c090-c093, c095-c099)", L + "cards.json CS2-c089..c099",
       "c089 Example 2.4; c090-c091 Theorem 3.3 and Lemma 3.2 with exact equality; c093 Prop 3.5; c095 Problem P3 value 6; "
       "c096 Prop 4.2; c097-c099 grade C with basis Lab 1 Part C; c094 fixed (see CS2b3-card-c094). c084, c088, c092 are "
       "separate FAIL rows"),
    bad("CS2b4-cards-c080", "2.7-cards vs current lesson text", L + "cards.json CS2-c080 vs " + L + "L06.html:380",
        "card back says 'BFS returns the first path'. L06.html:380 (changed this round) now reads 'BFS returns the path "
        "with the fewest edges, here the direct edge from s to a'. The card was not updated, and 'the first path' is "
        "ambiguous (first found, or first in some order)",
        "replace the final sentence with: 'BFS returns the path with the fewest edges, here the direct edge from s to a.'"),
    bad("CS2b4-cards-c084", "2.7-cards vs its own front", L + "cards.json CS2-c084",
        "front asks 'What are the steps of dynamic programming, and what are its two forms?' but the back gives only the "
        "three steps (changed this round); the two forms (memoized recursion and table fill, Definition 1.1 at line 60) "
        "are not stated",
        "add to the back: 'Two forms: memoized recursion, which calls itself and returns stored values, and table fill, "
        "which writes entries in an order where each depends only on entries already written (Definition 1.1).'"),
    bad("CS2b4-cards-notation-T", "2.7-cards vs notation.json and current lesson text",
        L + "cards.json CS2-c060, c061, c088, c092",
        "the cards use the symbol T for a tree (c060 'Assume T is an AVL tree', c061 'Assume T is an AVL tree with n nodes'), "
        "and for the coin table (c088 'T[a] = min{1 + T[a - c]}', c092 'T[i][j] = lambda(i, j)'). notation/notation.json "
        "registers T as 'number of return observations (periods) in a sample' (module S1), so the symbol may not take "
        "this meaning. The lesson now uses \\mathcal{A} (L05.html:77, 87) and dp[a], dp[i][j] (L07.html:101, 106, 164, 169), "
        "so these cards name a symbol that no current lesson page defines",
        "rewrite the four cards with \\mathcal{A} for the tree and dp[a] / dp[i][j] for the tables, matching the lesson lines"),
    ok("CS2b4-cards-notation-c068", "2.7-cards", L + "cards.json CS2-c068 vs L05.html:436",
       "card and lesson state the same rule and the same counts (272 of 500); the 'only' scope in the card is backed by "
       "rebalance() in tests/labs/CS2/lab-CS2-L05-1.py calling rotate only in its factor > 1 and factor < -1 branches"),
    # ---------------- L05-L08 remaining rows: quiz, misconceptions, problems
    ok("CS2b4-quiz-L05-L08", "2.9-structure (quizzes)", L + "L05.html..L08.html quiz sections",
       "each answer checked against its lesson: L05 answers 64, 7, 2 (balance factor 2), 12, 2, 1.440420, 272, insertion "
       "not proved; L06 answers 3, 6, 27.82 (40000/1438), |V|, 6, 'disjoint or nested'; L07 answers 2, 1, 40, 1025, 10, "
       "'at most 2^b'; L08 answers 3, 1, 4, 'integer cents', 'the resting order's price'"),
    ok("CS2b4-misconceptions-L05-L08", "2.9-structure (misconceptions)", L + "L05.html:430-442, L06.html:378-390, L07.html:522-534, L08.html:562-574",
       "each misconception's counter-example checked: L05 height 64 vs 7 and 2 vs 1; L06 weighted path 1 hop/10 vs 2 hops/2, "
       "triangle DFS 2 hops vs BFS 1 hop; L07 f(6)=2 vs 3 coins, 47 calls vs 28 stored; L08 price before time, 185-177=8 "
       "levels with 10 orders (pigeonhole). The L08 line-572 pigeonhole argument is correct"),
    ok("CS2b4-problems-L06-L08", "2.4-mathematics (problem solutions)",
       L + "L06.html M1-R3 (399-492); L07.html M1-R3 (543-638); L08.html M1-R2, P1-P3, E1-E3 (585-670)",
       "re-derived: L06 M1 (1..5 BFS removal order 1..5), M2 (times 1,2,3 / 6,5,4), M3 (6), P1-P3, R1 (ancestor), R2, "
       "R3 (n(n-1), n^2); L07 M1 (f(9)=3 for {2,5}), M2 (LCS 1, table), M3 (54, 40, 14), P1 (single denomination), P2, "
       "P3 (smallest failing amount 6), E1 (20 stored), E2, E3, R1 (1,048,577 and the 2^(b-1)+1 .. 2^b range), R2 (D={1,c}), "
       "R3 (two rows, 2(n+1))"),
    bad("CS2b4-L08-R3", "2.4-mathematics / problem solution",
        L + "L08.html R3 (673-677)",
        "the problem asks 'give a book where reading [the best ask] once gives a wrong trade'. The solution's example "
        "(asks 1 at 10000 and 5 at 10005, buy 3 at 10010) and its own last sentence say that a stale price 'raises a "
        "KeyError ... rather than trading at a wrong price'. No wrong trade is given, so the question is not answered",
        "either give a book where a stale read produces a trade that Definition 2.1 does not allow (and show the trade), "
        "or change the question to ask for the error a stale read raises"),
    bad("CS2b4-L07-memo-correct", "2.4-mathematics (unproved claim)", L + "L07.html:63",
        "'Both forms are correct when the recurrence is correct. On every subproblem that both compute, they store the "
        "same value.' No proof of memoized recursion correctness appears on the page, and no key result or grade covers "
        "it. The only evidence is the Lab 1 agreement on 60 instances, which is grade C",
        "add a short induction (each memoized call returns the recurrence value, by induction on the order of calls) "
        "as a T-graded statement, or state the sentence as a C-graded observation from Lab 1 with its basis"),
    bad("CS2b4-L08-any-stream", "2.2-numbers / scope words", L + "L08.html:546 (interpretation of Lab 1 Part B)",
        "'Under Assumptions 1 and 2 of Proposition 2.2, the fills of each submission are the sorted-scan fills for any "
        "stream that satisfies them'. Assumptions 1 and 2 (lines 113-114) are properties of the structure (head passes "
        "only dead entries; every listed price has a live order), not of the stream. Proposition 2.2 is stated for one "
        "submission, and no argument lifts it to every stream",
        "replace with: 'Under Assumptions 1 and 2 of Proposition 2.2, at each submission, the fills are the sorted-scan "
        "fills; the lab checks this on one stream only, and the assumptions are not checked by the lab'"),
    bad("CS2b4-L08-three-counts", "2.5-labs (what the lab keeps)", L + "L08.html:131 vs tests/labs/CS2/lab-CS2-L08-1.py class Counts (twin lines 80-87)",
        "'The lab keeps three kinds of count: queue steps, level creations and removals, and the number of tests of each "
        "binary search'. Counts also keeps orders_added, which Part C prints ('orders added: 298') and the page uses at "
        "546 ('checks them against the 298 orders added')",
        "change to 'four kinds of count: orders added, queue steps, level creations and removals, and binary-search tests'"),
    bad("CS2b3-L08-scope-words", "2.9-structure / prose claim vs code", L + "L08.html:56 and lab docstring (twin line 5)",
        "'The code in Lab 1 raises an error for any other type, and it never uses floating point.' The twin's Part A "
        "passes a float: tests/labs/CS2/lab-CS2-L08-1.py line 274 'book.submit(\"B\", cast(int, 100.5), 1, 8)', which "
        "creates a float that the check refuses. The round-3 row said grep showed no float in the code path; the grep "
        "did not catch the literal 100.5. The book's arithmetic uses no float (checked: no '/' operator, floor division "
        "only at line 120)",
        "change to 'the book's prices and quantities are never floats; Part A passes one float to show that it is refused'"),
    bad("CS2b4-L06-twin-docstring", "2.5-labs (docstring vs code and output)", "tests/labs/CS2/lab-CS2-L06-1.py:12 (docstring, Part C)",
        "docstring: 'The BFS path is the fewest hops; the lightest path is found by exhaustive search. The two paths differ.' "
        "Output (lab-L06.out, 'to b'): bfs_path s-b and lightest_path s-b, both weight 1. The two paths differ for a and c, "
        "not for b. The code's output line for b is the same in both",
        "change to 'The two paths differ for a and c; for b they coincide'"),
    ok("CS2b4-L08-E-problems", "2.4 / 2.7 (empirical solutions)", L + "L08.html E1-E3 (633-652)",
       "E1 102/400=25.5% and the code rule (cancel when a live order exists and draw < 25); E2 explanation consistent "
       "with _front (passes only dead entries at the front of a level that still has live orders, Definition 1.1); "
       "E3 bound L >= 8 from 4 <= floor(log2 L)+1, and the lab prints no list length"),
    ok("CS2b4-L08-P-problems", "2.4-mathematics (proof problems)", L + "L08.html P1-P3 (608-627)",
       "P1 bound n(floor(log2 n)+1) with k-1 <= n; P2 trade price a <= p from the stop test; P3 traded quantity min{q,Q} "
       "re-derived from the two stopping cases"),
    ok("CS2b-struct-template", "2.9-structure", L + "L05.html..L08.html",
       "all four pages carry the template in order: header with hours (9, 9, 10, 10 h), why-it-matters, numbered sections, "
       "lab section with hypothesis, code, expected block and interpretation, canon-breaks, misconceptions, problem set "
       "(mechanics, proof, empirical, research), key results table with grades, quiz, references, lesson nav; re-read this round"),
    ok("CS2b-prose-banned", "1.2/1.3 banned phrases", L + "L05.html..L08.html prose",
       "grep for 'roughly half', 'about 6%', 'historically', and ellipsis: no prose hit. The '...' hits in L07.html (lines "
       "321-451) are Python type hints tuple[int, ...] inside the lab code block (code block spans 211-496)"),
    ok("CS2b-prose-process-words", "1.2 process words", L + "L05.html..L08.html prose",
       "grep (case-insensitive) for build, builder, verifier, round, REQUEST, unit report: no prose hit"),
    ok("CS2b-dag-closure", "DAG / concepts", L + "L05.html..L08.html data-concept links",
       "check_dag CS2 PASS. Concepts used: mathematical-induction and exponential-and-logarithm (M1, in closure since "
       "CS2 prereqs = [CS1, M1]); big-O (L01), hash-map (L02), comparison-sorting and binary-search (L04); the unit's "
       "own balanced-search-tree, graph-traversal, dynamic-programming, order-book-data-structure. limit-order-book is not "
       "linked (plan section 1)"),
    ok("CS2b-hours", "hours (arithmetic only; pace not judged)", L + "L05..L08 data-hours; " + L + "index.html:29, 149-152",
       "data-hours 9, 9, 10, 10 equal the hub cards (L05 9 h, L06 9 h, L07 10 h, L08 10 h); all 11 lesson data-hours sum "
       "to 100 = data-hours-lessons; project 30 h; total 130"),
    ok("CS2b-figures", "2.8-figures", L + "L05.html..L08.html", "no img, svg or figure element on any of the four pages"),
    # ---------------- carried rows whose cited lines are outside the delta
    ok("CS2b-L05-key-h2", "2.3-grades", L + "L05.html:557 (Key results row 2)",
       carry(L + "L05.html line 557") + " grade T for Lemma 2.3"),
    ok("CS2b-L05-def-2.2", "2.4 definitions", L + "L05.html:71-72 (Definition 2.2); min_nodes docstring",
       carry(L + "L05.html lines 71-72") + " recurrence values N(0..7) = 0,1,2,4,7,12,20,33 match min_nodes output in the lab"),
    ok("CS2b-L05-E3", "2.4-mathematics", L + "L05.html:517-519 (E3)",
       carry(L + "L05.html lines 517-519") + " 12.33 re-derived this round (12.3277)"),
    ok("CS2b-L06-M3", "2.4-mathematics", L + "L06.html:415-417 (M3)",
       carry(L + "L06.html lines 415-417") + " 2+2+2 = 6 = 2|E|"),
    ok("CS2b-L06-intro-scope", "2.9-structure / scope", L + "L06.html:52 (why-it-matters)",
       carry(L + "L06.html line 52") + " 'proves both properties' matches Prop 2.2 and Prop 3.2"),
    ok("CS2b-L07-def1.1", "2.9-structure", L + "L07.html:63 (paragraph after Definition 1.1)",
       carry(L + "L07.html line 63") + " this row covers only the structure of the paragraph; its unproved claim is the "
       "separate FAIL row CS2b4-L07-memo-correct"),
    ok("CS2b-L07-canon-row", "2.9-structure / claims", L + "L07.html:515 (canon-breaks, memory paragraph)",
       carry(L + "L07.html line 515") + " 'only depends on the row above and entries to its left' matches Corollary 3.4"),
    ok("CS2b-L07-intro-often", "2.9-structure / scope", L + "L07.html:52 (why-it-matters)",
       carry(L + "L07.html line 52") + " 'two traps' and 'Example 2.4 shows' match the page"),
    ok("CS2b-L08-prop1.3", "2.4-mathematics", L + "L08.html:84 (Proposition 1.3 proof)",
       carry(L + "L08.html line 84") + " re-derived this round: cancellation and buy cases"),
    ok("CS2b-L08-every-stream", "2.9-structure / scope words", L + "L08.html:546",
       "the phrase 'for every stream' is no longer in the paragraph (checked by grep). The new scope issue in the same "
       "sentence is FAIL row CS2b4-L08-any-stream"),
    ok("CS2b-L08-limit-order-book", "DAG / concepts", L + "L08.html:52, 56",
       carry(L + "L08.html lines 52, 56") + " no limit-order-book link"),
    ok("CS2b-L05-heavy-child", "2.9-structure (term before definition)", L + "L05.html:104 and uses at 462, 530, 605",
       carry(L + "L05.html line 104 and its uses") + " heavy child defined at 104 before its uses"),
    ok("CS2b-L06-adjacency-matrix", "2.9-structure (term before definition)", L + "L06.html:56 (definition), 103, 125, 139, 362, 387-388",
       carry(L + "L06.html lines 56, 103, 125, 139, 362, 387-388") + " adjacency matrix defined at 56 before all uses"),
    ok("CS2b-L07-R1-about", "2.4-mathematics / scope", L + "L07.html:622 (R1) and 719-725 (quiz)",
       carry(L + "L07.html lines 622, 719-725") + " re-derived: 2^(b-1)+1 <= A+1 <= 2^b with the attainment conditions"),
    ok("CS2b-L08-prop2.2-hyp", "2.4 hypotheses", L + "L08.html:60, 112-114, 121, 546",
       "re-read this round: head and dead entry defined at 60 before the first use; the three hypothesis items (112-114) "
       "are used at the places the proof cites them; the single-proof structure is consistent. Remaining issues are the "
       "separate FAIL rows CS2b4-L08-any-stream and CS2b4-L08-three-counts"),
    ok("CS2b3-card-c082", "2.7-cards vs current lesson text", L + "cards.json CS2-c082 vs " + L + "L06.html:388",
       "card now: 'the row reads are |V| times the number of dequeued vertices, which is at most |V|^2', matching L06.html:388; "
       "round-3 FAIL is fixed"),
    ok("CS2b3-card-c094", "2.7-cards vs grade T and hypotheses", L + "cards.json CS2-c094 vs " + L + "L07.html:195-198",
       "card now begins 'Assume A >= 1.' and states A+1 entries and A+1 > 2^(b-1), matching Proposition 4.2 hypothesis "
       "(1) (L07.html:195); round-3 FAIL is fixed"),
    ok("CS2b3-L05-remark3.2", "2.9-structure / claims", L + "L05.html:104, 118, 123",
       carry(L + "L05.html lines 104, 118, 123") + " Remark 3.2 says 'checked, not proved'; matches the lab"),
    ok("CS2b3-L05-rotation-rule", "2.4-mathematics", L + "L05.html:104",
       carry(L + "L05.html line 104") + " sign rule stated as the choice used, not claimed as the only one"),
    ok("CS2b3-L06-weighted", "2.4 / 2.5 (counterexample)", L + "L06.html:368, 388; lab Part C",
       carry(L + "L06.html lines 368, 388; lab Part C output") + " weight 11 with 2 hops and weight 3 with 3 hops are the only two simple paths to c (c's only neighbour is a)"),
    ok("CS2b3-L06-row-reads", "2.2-numbers", L + "L06.html:125, 388; lab line 207",
       carry(L + "L06.html lines 125, 388") + " row reads = |V| x dequeued = 40000 for a connected graph"),
    ok("CS2b3-L06-misconception-2", "2.9-structure / claims", L + "L06.html:384 (Misconception 2)",
       carry(L + "L06.html line 384") + " triangle DFS example re-derived"),
    ok("CS2b3-L07-prop4.2", "2.4-mathematics", L + "L07.html:192-203",
       carry(L + "L07.html lines 192-203") + " statement with A>=1; proof re-derived; 2^40 has 41 bits"),
    ok("CS2b3-L07-quiz9", "2.9-structure (quiz)", L + "L07.html:654, 719-725",
       carry(L + "L07.html lines 654, 719-725") + " correct option 'at most 2^b entries'; explanation matches Prop 4.2"),
    ok("CS2b3-L07-greedy-def", "2.9-structure (term before definition)", L + "L07.html:111 (Example 2.4)",
       carry(L + "L07.html line 111") + " largest-coin-first defined at 111; f(6)=2 and the three-coin greedy re-derived"),
    ok("CS2b3-L07-hyp-expected", "2.5-labs (expected result)", L + "L07.html:210",
       carry(L + "L07.html line 210") + " 'Expected result' matches lab-L07.out"),
    ok("CS2b3-L08-def-head", "2.9-structure (term before definition)", L + "L08.html:60",
       carry(L + "L08.html line 60") + " head and dead entry defined before first use at 113"),
    ok("CS2b3-L08-pigeonhole", "2.4 / 2.9 (counting claim)", L + "L08.html:572",
       carry(L + "L08.html line 572") + " 10 orders on 8 levels: at least one level holds two orders"),
    ok("CS2b3-L08-part-C-bound", "2.2-numbers (bound)", L + "L08.html:546 (Part C sentences)",
       "re-derived this round: a search with 4 tests needs floor(log2 L)+1 >= 4, so L >= 8; a list of 7 has 3 binary "
       "digits (bit_length 3); the lab asserts comparisons <= bit_length and prints largest 4"),
]

# Round-3 rows not repeated above keep their ids: CS2b3-L05-remark3.2, CS2b3-L05-rotation-rule (kept), and the
# round-3 fragment's CS2b-lab-L05 / CS2b-lab-L07 / CS2b-lab-L08 are re-verified above.

ids = [r["id"] for r in rows]
dups = sorted({i for i in ids if ids.count(i) > 1})
assert not dups, dups
counts = {s: sum(1 for r in rows if r["status"] == s) for s in ("PASS", "FAIL", "UNVERIFIABLE")}
fragment = {
    "unit": "CS2",
    "slice": "CS2-b",
    "round": 4,
    "verifier": "independent verifier (Haiku), round 4, CS2 slice b (L05-L08 and lab twins lab-CS2-L05-1..L08-1); did not build CS2",
    "pin": "2657ab5",
    "base": "round 3 pin aa3c26c (round-3 fragment /tmp/fanout-frags/B-CS2-b.round3.json); delta computed with git diff -U0 aa3c26c 2657ab5",
    "checkout": "/tmp/verifyB4-CS2-b (detached at 2657ab5, .venv symlink, vendor present)",
    "scratch": "/tmp/CS2-v/CS2-b-r4",
    "verified_at": datetime(2026, 10, 28, tzinfo=UTC).isoformat(),
    "verdict": "FAIL" if counts["FAIL"] or counts["UNVERIFIABLE"] else "PASS",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "Lesson slice, no grader: mutants empty (architect ruling). Lab twins L05, L06, L07 byte-identical to aa3c26c; "
        "L08 twin changed in one docstring line. Scripts: ledgers/CS2/scripts/CS2-b-r4/ (recompute_r4.py: independent "
        "recomputation of the L05-L08 numbers and of the L08 stream; build_fragment_r4.py: this fragment; "
        "delta_lessons_labs.diff, delta_cards.diff). Not checked: a line-by-line re-read of every carried paragraph (carried "
        "rows name the byte-identical lines); the Pyodide run beyond page_smoke timing; ruff/mypy on the whole repo; no "
        "outside source is cited, so no publisher or bot-protected site was contacted."
    ),
    "summary": (
        f"{len(rows)} rows: {counts['PASS']} PASS, {counts['FAIL']} FAIL, {counts['UNVERIFIABLE']} UNVERIFIABLE. "
        "FAIL rows: CS2b-cards-consistency (aggregate), CS2b4-cards-c080, CS2b4-cards-c084, CS2b4-cards-notation-T, "
        "CS2b4-L08-R3, CS2b4-L07-memo-correct, CS2b4-L08-any-stream, CS2b4-L08-three-counts, CS2b3-L08-scope-words, "
        "CS2b4-L06-twin-docstring. Round-3 FAIL rows CS2b3-card-c082 and CS2b3-card-c094 are fixed and PASS."
    ),
}

out = ROOT / "ledgers" / "CS2" / "CS2-b.json"
out.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out, counts)
