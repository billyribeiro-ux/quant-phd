"""Builds ledgers/CS2/CS2-b.json for round 3 (CS2 slice b: L05-L08 and lab twins).

Run: .venv/bin/python -I ledgers/CS2/scripts/CS2-b-r3/build_fragment_r3.py
Reads the round 2 fragment from /tmp/fanout-frags/B-CS2-b.round2.json (context only; its PASS rows are
re-verified or carried with the hunk-based prefix below). The lesson delta is ledgers/CS2/scripts/CS2-b-r3/
delta_lessons_labs.diff (git diff -U0 1817191 aa3c26c); the card delta is delta_cards.diff.
"""

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[4]
R2 = json.loads(pathlib.Path("/tmp/fanout-frags/B-CS2-b.round2.json").read_text(encoding="utf-8"))

HUNKS = "git diff -U0 1817191 aa3c26c hunks: L05.html 104,118,123,537; L06.html 56,93,103,125,368,388; L07.html 111,198,203,210,622,654,719,722,725; L08.html 60,113-114,176,546,572,587,676,689; cards.json changes only for L02-L04, L09-L11 and c155 (L02)"


def carry(text: str) -> str:
    # The lesson files changed since round 2, so the carry is limited to the cited lines, which are byte-identical.
    return (
        "Carried from round 2 (cited lines byte-identical since the previous pin; files changed elsewhere, "
        + HUNKS
        + "): "
        + text
    )


OVR: dict[str, dict[str, str]] = {}


def row(rid: str, status: str, check: str, location: str, evidence: str) -> None:
    OVR[rid] = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}


# ---- commands, re-run on the round 3 pin
row("CS2b-cmd-pin", "PASS", "2.9-structure", "git checkout /tmp/verifyB3-CS2-b (detached at aa3c26c)",
    "git log -1 --oneline: aa3c26c Batch 2: fixes for independent verification round 2; git status clean; "
    "delta from 1817191 computed (git diff --stat, scratch CS2-v/CS2-b-r3/delta_lessons_labs.diff)")
row("CS2b-cmd-run_labs", "PASS", "tools/run_labs.py --unit CS2; tests/labs/CS2/lab-CS2-L05-1.py..L08-1.py",
    "tools/run_labs.py --unit CS2",
    "run_labs CS2: PASS (14/14), rc=0; scratch CS2-v/CS2-b-r3/run_labs.txt")
row("CS2b-cmd-lab-cpython-W-error", "PASS",
    "tests/labs/CS2/lab-CS2-L05-1.py, L06, L07, L08 under python -I -W error",
    "tests/labs/CS2/lab-CS2-L0{5,6,7,8}-1.py",
    "each run rc=0 (L05 31 lines, L06 17, L07 10, L08 15 output lines); outputs in CS2-v/CS2-b-r3/lab-L0n.out")
row("CS2b-cmd-page_smoke", "PASS", "tools/page_smoke.py --unit CS2 --pages L05 L06 L07 L08", "tools/page_smoke.py",
    "page_smoke CS2: PASS; L08 lab 0.0 s; scratch CS2-v/CS2-b-r3/page_smoke.txt")
row("CS2b-cmd-check_pages", "PASS", "tools/check_pages.py --unit CS2; tools/check_projects.py --unit CS2",
    "tools/check_pages.py, tools/check_projects.py", "check_pages CS2: PASS; check_projects CS2: PASS")
row("CS2b-cmd-check_dag", "PASS", "tools/check_dag.py --unit CS2", "curriculum/curriculum.json CS2 entry",
    "check_dag CS2: PASS; the delta adds one data-concept link (order-book-data-structure, L08 line 60) to a term defined in L08")
row("CS2b-cmd-lint", "PASS", "ruff check and ruff format --check on the four lab twins",
    "tests/labs/CS2/lab-CS2-L05-1.py..L08-1.py", "ruff check: All checks passed!; ruff format --check: 4 files already formatted")
row("CS2b-cmd-verify_refs", "PASS", "tools/verify_refs.py --offline; tools/verify_refs.py --unit CS2 (live)",
    "references/references.json; tools/verify_refs.py",
    "offline: 560 entries, 0 problems, rc=0; live CS2: 1 of 560 entries, 0 problems, rc=0 (CS2 cites one key)")
row("CS2b-cit-cormen", "PASS", "2.1-citations", "L06.html:591 (section 9), key cormen2022introduction",
    "the key exists (live verify_refs CS2 0 problems); the text states no claim is attributed to it, so no bibliographic claim is made; re-read this round")

# ---- numbers, re-derived this round
row("CS2b-num-L05-lab", "PASS", "2.2-numbers", "L05.html hypothesis paragraph (line 123), Part A interpretation, lab output",
    "lab-L05.out: invariant True, final_size 500, final_height 11, log_phi_501 12.9186, rotation_calls_total 340, "
    "inserts_without_rotation 272 of 500, plain_bst_height 64, avl_height 7, avl_bound_log_phi_65 8.6747 (recomputed: ln65/ln phi = 8.67474); "
    "the text's 500 insertions, 64 keys and 12 values of N(h) match the code")
row("CS2b-num-L05-derived", "PASS", "2.2-numbers", "L05.html Part A interpretation, Remark 2.5 (2.28), E3 (12.33), R3 (4.32), E1",
    "recomputed: 63+53+2(55+57)=340; 272/500=0.544 (54.4%); ln3/ln phi=2.2830 (shown as 2.28); ln377/ln phi=12.3277 (shown 12.33, ln377=5.932, ln phi=0.4812); "
    "ln8/ln phi=4.3213 (shown 4.32); 1/log2 phi=1.4404 (shown 1.44)")
row("CS2b-num-L06", "PASS", "2.2-numbers", "L06.html Lab 1 paragraph (125), Part A/B/C/D interpretation (368, 388), E2, E3, M3",
    "lab-L06.out: 772 reachable pairs, 308 unreachable, 200 sources; 772-200 self pairs=572 positive; 440 pairs; Part C weights 10,2,11,3; "
    "Part D: enqueues 200, adjacency entries 1238 = 2*619, list work 1438 = 200+1238, matrix 40000 = 200*200 (lab line 207, formula reached*n)")
row("CS2b-num-L07", "PASS", "2.2-numbers", "L07.html Example 2.4 (111), lab paragraph (210), Section 4, Section 5, Misconceptions, E1-E3, P3",
    "lab-L07.out: LCS 3; table cells 49 = 7*7; memo stored 28, calls 47, no-memo 183; coins 20 -> 5 coins; memo calls 56, no-memo 20736; "
    "script check_r3.py: f(0..6)=0,1,2,1,1,2,2; greedy(6)=3; smallest greedy failure for {1,3,4} is 6; 2^40 has 41 bits, 2^40+1>10^12")
row("CS2b-num-L08", "PASS", "2.2-numbers", "L08.html Lab 1 Part A-C interpretation (546, 572, 587, 676), Misconception 3, E1-E3, Key results row 7 (689)",
    "lab-L08.out: 298 new, 102 cancels, 117 traded, 177 executions, 10 resting, 185 created, 177 removed, 362 searches, max comparisons 4, "
    "queue steps 7; 185-177=8 levels; 10 orders on 8 levels gives at least one level with 2 orders (pigeonhole); 298 orders added; M1 worked example re-derived by hand")

# ---- grades
row("CS2b-grade-L05", "PASS", "2.3-grades", "L05.html section 7 Key results table",
    carry("the Key results table has no hunk (row 2 at line 557 is unchanged since 1817191; the only changed grade-related lines are 118 and 537, re-verified)"))
row("CS2b-grade-L06", "PASS", "2.3-grades", "L06.html section 7 Key results table",
    carry("no key-results line is in the hunks; the changed Proposition 2.3 text (93) and Lab 1 paragraph (125) were re-verified above"))
row("CS2b-grade-L07", "PASS", "2.3-grades", "L07.html section 8 Key results table, row at line 654",
    "row 654 now reads 'The coin table has A+1 entries, with 2^(b-1) < A+1 <= 2^b for an amount of b bits' (T, Proposition 4.2); "
    "Proposition 4.2 proved on page with hypothesis A>=1 (line 195); script check over A in 1..200000 finds no violation")
row("CS2b-grade-L08", "PASS", "2.3-grades", "L08.html section 7 Key results table, row at line 689",
    "row 689 now reads 'Under hypotheses (1)-(3) of Proposition 2.2, the matching rule fills orders in price-time priority' (T); "
    "the hypotheses are stated at lines 111-114 and the proof at line 121 uses them; the round 2 FAIL is fixed")

# ---- math
row("CS2b-math-L05-proofs", "PASS", "2.4-math", "L05.html Lemma 2.3 (~64), Proposition 2.4 (~72-74), Proposition 3.1 (107), Remark 2.5",
    carry("the Lemma 2.3 and Proposition 2.4 proof lines are not in the hunks; Proposition 3.1 (107) is not in the hunks; the Remark 3.2 wording at 118 was re-read and matches Lab 1 Part A"))
row("CS2b-math-L05-problems", "PASS", "2.4-math", "L05.html R2 solution (line 537)",
    "rewritten solution: the tree of M1 (root 5, left 3 with left 2, right 7) under root R with right child s with left child t; "
    "script check_r3.py: R height 4, 7 nodes, balance factors R 1, 5 1, 3 1, 2 0, 7 0, s 1, t 0, all in {-1,0,1}; N(4)=7 by Lemma 2.3. Round 2 FAIL fixed")
row("CS2b-math-L06-proofs", "PASS", "2.4-math", "L06.html Lemma 2.1 (~54), Proposition 2.2, Proposition 2.3 (74-78, 93), Proposition 3.2 (92-96), R1-R3, P1-P3",
    carry("Proposition 2.3 (93) was re-read: 'each enqueue and each adjacency-entry inspection costs one operation' matches the count in Prop 2.3 and lab line 200-207; other proof lines are outside the hunks"))
row("CS2b-math-L07-proofs", "PASS", "2.4-math", "L07.html Theorem 2.2, Corollary 2.3, Example 2.4 (111), Lemma 3.2, Theorem 3.3, Corollary 3.4, Proposition 3.5, Proposition 4.2 (192-203), M1-M3, P1-P3, R2, R3",
    "Example 2.4 (111) re-derived by script: f(6)=2 via 3+3; largest-coin-first 4+1+1. Proposition 4.2 (192-203) re-proved: 2^(b-1) <= A gives A+1 > 2^(b-1); A < 2^b gives A+1 <= 2^b; script confirms for A in 1..200000. "
    "The round 2 Theorem/Lemma/Problem lines not in the hunks are carried by the same hunk list")
row("CS2b-math-L08-lemmas", "PASS", "2.4-math", "L08.html Proposition 1.3 (84), Proposition 2.2 (107-121), Lemma 3.1 (123), Proposition 3.2 (137), Proposition 3.3 (153), P1-P3, M1-M3, R1-R3",
    "Proposition 2.2 hypotheses (113-114) and proof (121) re-read: hypothesis (2) and (3) are used exactly where the proof cites them; "
    "M1 (587) re-derived: trades 2 at 10010 from order 2 and 3 at 10010 from order 3, rests 1 at 10010 and 3 at 10020; "
    "R-stale-level (676): dict lookup at lab line 175 raises KeyError, so 'KeyError' is accurate")

# ---- labs
row("CS2b-lab-L05", "PASS", "2.5-labs", "tests/labs/CS2/lab-CS2-L05-1.py; L05.html Lab 1 paragraph (123) and interpretation",
    "lab output checked: rotation kinds printed by code; height bound printed True; two-node AVL height 2; 'checks, not proves' wording matches Remark 3.2 (118)")
row("CS2b-lab-L07", "PASS", "2.5-labs", "tests/labs/CS2/lab-CS2-L07-1.py; L07.html Lab 1 paragraph (210) and interpretation",
    "'Expected result' (210) is accurate: memo, table and exhaustive agree (lab A/B print 'agree on all of them'); table cells 49 = mn; memo stored 28 <= 49; calls 47 > 28; no-memo 183 > 47; coin 20 -> 5 coins")
row("CS2b-lab-L08", "PASS", "2.5-labs", "tests/labs/CS2/lab-CS2-L08-1.py; L08.html Lab 1 paragraph (176) and interpretation (546, 572, 587, 676)",
    "lab output and the 'Expected result' sentence agree; the 'on this one stream only' sentence (546) matches the Part B seeded stream; part C queue-step assertion at lab line 336 checks queue steps <= orders added")
row("CS2b-L06-lab-exhaustive", "PASS", "2.5-labs", "tests/labs/CS2/lab-CS2-L06-1.py brute_min_hops; L06.html Lab 1 paragraph (125)",
    "the twin is byte-identical since 1817191 (not in the delta); the Lab 1 paragraph still says 'exhaustive search' and the code enumerates simple paths")

# ---- cards
row("CS2b-cards-consistency", "FAIL", "2.7-cards", "course/modules/CS/CS2/cards.json: CS2-c056..c115 (60 cards, lessons L05-L08)",
    "re-checked all 60 cards against the CURRENT lesson text. FAIL: CS2-c082 says 'the cost is about |V|^2' but L06.html:388 now says the row reads are |V| times the dequeued count, 'which is at most |V|^2'; "
    "FAIL: CS2-c094 is graded T and gives A+1 > 2^(b-1) without the hypothesis A >= 1 of Proposition 4.2 (L07.html:195)")
row("CS2b3-card-c082", "FAIL", "2.7-cards", "cards.json CS2-c082 vs L06.html:388",
    "card back 'so the cost is about |V|^2' disagrees with the current lesson 'so the row reads are |V| times the number of dequeued vertices, which is at most |V|^2'; "
    "fix: 'With an adjacency matrix a dequeued vertex reads its full row of |V| entries, so the row reads are at most |V|^2 (Lab 1, Part D: 40000 for 200 vertices).'")
row("CS2b3-card-c094", "FAIL", "2.7-cards", "cards.json CS2-c094 vs L07.html:192-198",
    "T-graded card gives 'A + 1 entries ... A + 1 > 2^(b-1)' and drops Proposition 4.2's hypothesis A >= 1 (L07.html:195); "
    "fix: add 'Assume A >= 1.' to the back")
row("CS2b-cards-dupe-scan", "PASS", "2.7-cards", "course/modules/CS/CS2/cards.json (155 cards, full scan)",
    "re-run: 155 cards, no duplicate id, no duplicate front (case-insensitive); CS2-c155 is an L02 card added in the delta")
row("CS2b-cards-coverage", "PASS", "2.7-cards", "cards.json lesson field for L05, L06, L07, L08",
    "60 cards with lesson in L05-L08 (c056..c115), all with a lesson field; re-run this round")

# ---- structure, prose, DAG, hours, figures
row("CS2b-struct-template", "PASS", "2.9-structure", "L05.html..L08.html",
    carry("the template sections (why-it-matters, sections, problem set, key results, references) are not in the hunks; check_pages CS2 PASS this round"))
row("CS2b-prose-banned", "PASS", "2.9-structure", "L05.html..L08.html text",
    "grep for roughly half, about 6%, historically, builder, verifier, round N, REQUEST, unit report, ellipsis: no prose hits (only code '...' in type hints of L07 code)")
row("CS2b-prose-process-words", "PASS", "2.9-structure", "L05.html..L08.html text",
    "grep for process words (build, builder, round, verifier, REQUESTS, unit report): no prose hits this round")
row("CS2b-dag-closure", "PASS", "DAG", "L05-L08 data-concept links and Uses lines",
    "check_dag CS2 PASS; the one added link in the delta is order-book-data-structure (defined at L08:60 in the same unit)")
row("CS2b-hours", "PASS", "2.6-hours", "L05.html (9 h), L06.html (9 h), L07.html (10 h), L08.html (10 h); course/modules/CS/CS2/index.html",
    carry("no hunk touches a hours line and index.html is unchanged since 1817191 (git diff --stat lists no CS2 index change); the hub split 9+9+10+10 = 38 h equals the lesson hours"))
row("CS2b-figures", "PASS", "2.8-figures", "L05.html..L08.html", carry("no figure line is in the hunks"))

# ---- key lesson-level rows (carried; cited lines outside the hunks)
row("CS2b-L05-key-h2", "PASS", "2.3-grades", "L05.html:557 (Key results row 2)",
    carry("line 557 is not in the hunk list"))
row("CS2b-L05-def-2.2", "PASS", "2.4-math", "L05.html:71-72 (Definition 2.2); min_nodes docstring",
    "Definition 2.2 N(0)=0, N(1)=1, N(h)=1+N(h-1)+N(h-2) re-read this round; script: N(0..7)=0,1,2,4,7,12,20,33 equals lab Part C N_h values; the lines are not in the hunks")
row("CS2b-L05-E3", "PASS", "2.4-math", "L05.html:519 (Problem E3 solution; question at 517)",
    "12.33 recomputed this round (ln377/ln phi = 12.3277); line 519 not in the hunks")
row("CS2b-L06-M3", "PASS", "2.4-math", "L06.html:417 (Problem M3 solution)", carry("line 417 is not in the hunks"))
row("CS2b-L06-intro-scope", "PASS", "2.9-structure", "L06.html:52 (why-it-matters)", carry("line 52 is not in the hunks"))
row("CS2b-L07-def1.1", "PASS", "2.9-structure", "L07.html:63 (paragraph after Definition 1.1)", carry("line 63 is not in the hunks"))
row("CS2b-L07-canon-row", "PASS", "2.9-structure", "L07.html:515 (canon-breaks, memory paragraph)", carry("line 515 is not in the hunks"))
row("CS2b-L07-intro-often", "PASS", "2.9-structure", "L07.html:52 (why-it-matters)", carry("line 52 is not in the hunks"))
row("CS2b-L08-prop1.3", "PASS", "2.4-math", "L08.html:84 (Proposition 1.3 submission of a buy)", carry("line 84 is not in the hunks"))
row("CS2b-L08-every-stream", "PASS", "2.9-structure", "L08.html:546 (Lab 1 Part B interpretation)",
    "the round 2 'for every stream' is replaced by 'for any stream that satisfies them' with the hypotheses named; the lab 'on this one stream only' is accurate; no unscoped 'every stream' remains in the paragraph")
row("CS2b-L08-limit-order-book", "PASS", "DAG", "L08.html:52 (why-it-matters), 56 (limit order in Section 1)",
    carry("lines 52 and 56 are not in the hunk list; no new concept link"))

# ---- round 2 FAIL rows, now fixed
row("CS2b-L05-heavy-child", "PASS", "2.9-structure", "L05.html:104 (first use and definition of heavy child), 462, 530, 605",
    "'heavy child' is now defined in the paragraph at line 104 (the balance-factor-2 child is the left child, -2 the right child) before its later uses; round 2 FAIL fixed")
row("CS2b-L06-adjacency-matrix", "PASS", "2.9-structure", "L06.html:56 (definition), 103, 125, 139, 362, 387-388",
    "'adjacency matrix' is defined at line 56 in the same paragraph as adjacency lists, before the uses at 103, 125, 139, 362 and 387-388; round 2 FAIL fixed")
row("CS2b-L07-R1-about", "PASS", "2.2-numbers", "L07.html:622 (Research R1 solution) and 719-725 (quiz)",
    "round 2 'about 2^b' replaced: 622 now gives 2^(b-1)+1 <= A+1 <= 2^b with the attainment conditions A=2^b-1 and A=2^(b-1), re-derived; quiz stem 719 now asks which bound holds; round 2 FAIL fixed")
row("CS2b-L08-prop2.2-hyp", "PASS", "2.4-math", "L08.html:60 (definitions of head and dead entry), 113-114 (hypotheses), 121 (proof), 546",
    "head and dead entry are defined at line 60 before use; hypothesis (2) and (3) now state the Definition 1.1 invariants; 'for every stream' is replaced at 546 by a scoped sentence; round 2 FAIL fixed")

# ---- new round 3 rows for the changed text
row("CS2b3-L05-remark3.2", "PASS", "2.9-structure", "L05.html:104, 118 (Remark 3.2), 123",
    "Remark 3.2 now says the AVL rule after insertion is checked, not proved, and 'only that check is stated here'; lab Part A checks every balance factor after each of 500 insertions (lab-L05.out invariant True)")
row("CS2b3-L05-rotation-rule", "PASS", "2.4-math", "L05.html:104 (rotation, heavy child, lean, single/double rule)",
    "the sign rule (same sign or 0 gives single rotation; opposite sign gives double) is the standard AVL repair choice for an insertion; 'leans' is defined by the child's balance factor; the rule is not claimed to be the only possible choice")
row("CS2b3-L06-weighted", "PASS", "2.2-numbers", "L06.html:368 (Hops are not weights), 388; lab Part C",
    "exhaustive enumeration of simple paths from s to c: [0,1,3] weight 11 with 2 hops and [0,2,1,3] weight 3 with 3 hops; these are the only two simple paths to c (c's only neighbour is a)")
row("CS2b3-L06-row-reads", "PASS", "2.2-numbers", "L06.html:125, 388; lab line 207",
    "row reads = |V| x dequeued vertices = 200 x 200 = 40000 for a connected graph; the text's 'at most |V|^2' is right and the printed value is the formula reached*n")
row("CS2b3-L06-misconception-2", "PASS", "2.9-structure", "L06.html:384 (Misconception 2, DFS triangle)",
    carry("line 384 is not in the hunk list; the paragraph does not name DFS, but it sits in the DFS misconception (section 5) and describes the DFS tree path; BFS would discover c from a directly"))
row("CS2b3-L07-prop4.2", "PASS", "2.4-math", "L07.html:192-203 (Proposition 4.2 and proof)",
    "statement with hypotheses A>=1 and b = floor(log2 A)+1; proof re-derived; script check over A in 1..200000 finds no violation; the 2^40 example re-derived (41 bits, 2^40+1 > 10^12)")
row("CS2b3-L07-quiz9", "PASS", "2.9-structure", "L07.html:719-725 (quiz) and 654 (Key results)",
    "option 'at most 2^b entries' is the correct bound by Proposition 4.2; the explanation matches the statement; the question no longer says 'about'")
row("CS2b3-L07-greedy-def", "PASS", "2.9-structure", "L07.html:111 (Example 2.4)",
    "largest-coin-first is defined at 111 as taking the largest denomination not exceeding the remainder; 4+1+1 uses 3 coins and f(6)=2 by 3+3 (script)")
row("CS2b3-L07-hyp-expected", "PASS", "2.5-labs", "L07.html:210 (Lab 1 hypothesis)",
    "'Expected result' with the same claims as the lab output: agreement on 30+30 instances, mn = 49 cells, 28 <= 49 stored, 47 > 28 calls, 183 no-memo calls")
row("CS2b3-L08-def-head", "PASS", "2.9-structure", "L08.html:60 (Definition 1.1 body)",
    "head and dead entry are defined in the Definition 1.1 body before the first use at 113; no undefined term")
row("CS2b3-L08-pigeonhole", "PASS", "2.2-numbers", "L08.html:572",
    "10 resting orders on 8 levels: by pigeonhole at least one level holds two orders; stated correctly")
row("CS2b3-L08-scope-words", "PASS", "2.9-structure", "L08.html:181 ('never uses floating point'), 546, 552",
    "'never uses floating point': grep of lab-CS2-L08-1.py shows no float in the code path (only the printed refusal message); the code refuses non-int types via type(x) is not int (lab line 91-92); 'any other type' is accurate for check_order")
row("CS2b3-L08-part-C-bound", "PASS", "2.2-numbers", "L08.html:546 (largest comparison count 4)",
    "a search with 4 comparisons needs floor(log2 L)+1 >= 4, so L >= 8; a list of 7 or fewer has at most 3 binary digits; the statement is correct")

# ---- mutants: lesson slice, no grader, none required
mutants: list = []

rows = []
for r in R2["rows"]:
    rid = r["id"]
    if rid in OVR:
        rows.append(OVR[rid])
    else:
        raise SystemExit(f"round 2 row {rid} has no round 3 disposition")
for rid, rr in OVR.items():
    if rid not in {r["id"] for r in R2["rows"]}:
        rows.append(rr)

FIXES = {
    "CS2b-cards-consistency": "Fix CS2b3-card-c082 and CS2b3-card-c094 as stated in those rows; the lesson text is not changed.",
    "CS2b3-card-c082": "Edit cards.json CS2-c082 back to: 'With an adjacency matrix a dequeued vertex reads its full row of |V| entries, so the row reads are at most |V|^2 (Lab 1, Part D: 40000 for 200 vertices).'",
    "CS2b3-card-c094": "Edit cards.json CS2-c094 back to add: 'Assume A >= 1.' (Proposition 4.2 hypothesis, L07.html:195).",
}
for r in rows:
    if r["status"] != "PASS":
        r["fix"] = FIXES[r["id"]]

verdict = "FAIL" if any(r["status"] != "PASS" for r in rows) else "PASS"
counts = {s: sum(1 for r in rows if r["status"] == s) for s in ("PASS", "FAIL", "UNVERIFIABLE")}
frag = {
    "unit": "CS2",
    "slice": "CS2-b",
    "round": 3,
    "verifier": "independent verifier (Haiku), round 3, CS2 slice b (L05-L08 and lab twins lab-CS2-L05-1..L08-1); did not build CS2",
    "pin": "aa3c26c",
    "base": "round 2 pin 1817191 (round 2 fragment /tmp/fanout-frags/B-CS2-b.round2.json); delta computed with git diff -U0 1817191 aa3c26c",
    "checkout": "/tmp/verifyB3-CS2-b (detached at aa3c26c, .venv symlink, vendor present)",
    "scratch": "/tmp/CS2-v/CS2-b-r3",
    "verified_at": "2026-10-28T00:00:00+00:00",
    "verdict": verdict,
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "Lesson slice, no grader: mutants empty (architect ruling). Scripts: ledgers/CS2/scripts/CS2-b-r3/ "
        "(check_r3.py: numeric and proof re-derivations; build_fragment_r3.py: this fragment; delta_lessons_labs.diff, delta_cards.diff). "
        "Lab twins L05-L08 are byte-identical to 1817191; lab-CS2-L02-1 and L09-1 changed and are out of slice. "
        "Lesson pages changed in round 3 at the hunk lines listed in carry(); rows whose cited lines are outside the hunks are carried with that prefix. "
        "Not checked: a full re-read of every unchanged paragraph of L05-L08 beyond the hunk-adjacent and cited lines (carried, not re-derived); "
        "the Pyodide run beyond page_smoke timing; ruff/mypy on the whole repo; registry record contents beyond the key's existence; "
        "no Springer/ScienceDirect/JSTOR access was attempted and none is needed (no outside source is cited)."
    ),
    "summary": (
        f"{len(rows)} rows: {counts['PASS']} PASS, {counts['FAIL']} FAIL, {counts['UNVERIFIABLE']} UNVERIFIABLE. "
        "FAIL rows: CS2b-cards-consistency (aggregate), CS2b3-card-c082 (card says 'about |V|^2' where the lesson now says 'at most |V|^2'), "
        "CS2b3-card-c094 (T card drops Proposition 4.2's hypothesis A>=1). "
        "Round 2 FAIL rows CS2b-grade-L08, CS2b-math-L05-problems, CS2b-L05-heavy-child, CS2b-L06-adjacency-matrix, CS2b-L07-R1-about, "
        "CS2b-L08-prop2.2-hyp are fixed and re-verified (PASS). All commands re-run on aa3c26c."
    ),
}

out = ROOT / "ledgers" / "CS2" / "CS2-b.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(frag, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("wrote", out, counts, verdict)
