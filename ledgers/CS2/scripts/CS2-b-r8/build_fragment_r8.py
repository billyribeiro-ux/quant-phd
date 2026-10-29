"""Assemble the round-8 fragment for CS2 slice b from this round's checks and the byte-identical round-7 carries."""
import json
import subprocess

ROOT = "/Users/billyribeiro/.fanout/wt/verifyB8-CS2-b"
r7 = json.load(open("/Users/billyribeiro/.fanout/frags/B-CS2-b.round7.json", encoding="utf-8"))
r7_rows = {r["id"]: r for r in r7["rows"]}
CARRY = "Carried from round 7 (course/modules/CS/CS2/L07.html and tests/labs/CS2/lab-CS2-L07-1.py byte-identical since 7aa909e; git diff 7aa909e ce7b382 empty for both): "


def carried(rid: str, check: str, location: str) -> dict:
    prev = r7_rows[rid]
    assert prev["status"] == "PASS", rid
    return {"id": rid, "check": check, "location": location, "status": "PASS", "evidence": CARRY + prev["evidence"]}


def row(rid: str, check: str, location: str, evidence: str) -> dict:
    return {"id": rid, "check": check, "location": location, "status": "PASS", "evidence": evidence}


rows = [
    row("G-CHECK-PAGES", "gate", "course/modules/CS/CS2/L05-L08.html and all units",
        "check_pages.py --unit CS2: 'check_pages CS2: PASS' exit 0 (ledgers/CS2/scripts/CS2-b-r8/check_pages_cs2_r8.out); check_pages.py --all exit 0, 0 FAIL lines (check_pages_all_r8.out)."),
    row("G-CHECK-DAG", "gate", "course/modules/CS/CS2/L05-L08.html concept links and the DAG",
        "check_dag.py --unit CS2: 'check_dag CS2: PASS' exit 0 (check_dag_cs2_r8.out); check_dag.py --all exit 0, 0 FAIL lines (check_dag_all_r8.out)."),
    row("G-CHECK-PROJECTS", "gate", "all units",
        "check_projects.py --all exit 0, 0 FAIL lines (ledgers/CS2/scripts/CS2-b-r8/check_projects_r8.out). project.html changed in the delta but belongs to slice e; this row covers only the gate."),
    row("G-RUN-LABS", "gate", "course/modules/CS/CS2/L05.html:121-415, L06.html:123-363, L07.html:208-508, L08.html:174-550",
        "run_labs.py --unit CS2: 'run_labs CS2: PASS (14/14)' exit 0 (ledgers/CS2/scripts/CS2-b-r8/run_labs_r8.out)."),
    row("G-TWINS-ISOLATED", "gate", "tests/labs/CS2/lab-CS2-L05-1.py, L06-1, L07-1, L08-1",
        "ledgers/CS2/scripts/CS2-b-r8/twin_check_r8.py run with .venv/bin/python -I: each twin in a fresh temp dir under python -I -W error: exit 0 and stderr 0 bytes for L05, L06, L07, L08 (twin_check_r8.out). Same script: page lab code equals twin (rstrip) True and printed expected block equals the run output (rstrip) True for all four."),
    row("G-PYTEST-LABS", "gate", "tests/test_labs.py -k CS2",
        "pytest -q tests/test_labs.py -k CS2: 14 passed, exit 0 (pytest_labs_r8.out)."),
    row("G-RUFF-MYPY", "gate", "repository",
        "ruff check . 'All checks passed!' exit 0; ruff format --check . '362 files already formatted' exit 0; mypy --no-incremental 'Success: no issues found in 255 source files' exit 0 (ruff_r8.out, mypy_r8.out)."),
    row("G-VERIFY-REFS", "gate", "references/references.json; L05-L08 reference sections",
        "verify_refs.py --offline: 'offline integrity: 560 entries, 0 problems' exit 0 (verify_refs_r8.out). Live run not executed: references/ is unchanged in the delta and the slice's pages cite no registry key with a locator."),
    row("G-BUILD-SITE", "gate", "course/assets/data, course/index.html, course/concepts.html",
        "build_site.py --check: 'site data current: 6 outputs' exit 0 (build_site_r8.out)."),
    row("G-PAGE-SMOKE", "gate", "course/modules/CS/CS2/L05.html-L08.html",
        "page_smoke.py --unit CS2 --pages L05 L06 L07 L08: 'page_smoke CS2: PASS' exit 0; each page PASS (page_smoke_r8.out)."),
    row("PROCESS-WORDS", "2.9", "course/modules/CS/CS2/L05.html-L08.html",
        "style_check_r7.py run on this checkout (ledgers/CS2/scripts/CS2-b-r7/style_check_r7.py with the checkout path): the only PROCESS-HIT lines are 'round' inside 'around' in the L05 Python code block (page lines 186 and 199). No builder, verifier, fan-out, orchestrat or draft hit."),
    row("STYLE-BANNED-WHY", "2.9 / BUILDER_RULES 1.3-1.4 and 4.2", "why-it-matters paragraphs L05-L08 and banned strings",
        "style_check_r7.py on this checkout: why-it-matters word counts L05 108, L06 111, L07 117, L08 118 (all at most 120; L05 changed from 106, L08 from 115 in this delta). Banned-string hits only the Python '...' annotations in L07 code blocks (lines 321-451)."),
    row("L05-LAB", "2.5", "course/modules/CS/CS2/L05.html:121-415; tests/labs/CS2/lab-CS2-L05-1.py",
        "Page code equals the twin and the expected block equals the run output (31 lines) under python -I -W error, exit 0, stderr 0 bytes (twin_check_r8.out). Each prose number checked: 340 = 63+53+2(55+57); 272/500 = 54.4%; log_phi 501 = 12.9186; log_phi 65 = 8.6747; 1/log2(phi) = 1.440420; height 64 for sorted keys in a plain BST; AVL height 7; two-node height 2. Hypothesis text matches the code (seed 20261028, 500 keys, Part A checks, Part B sorted 1..64, Part C N(h) and two-node tree; no timing)."),
    row("L06-LAB", "2.5", "course/modules/CS/CS2/L06.html:123-363; tests/labs/CS2/lab-CS2-L06-1.py",
        "Page code equals the twin and the expected block equals the run output (17 lines), exit 0, stderr 0 bytes (twin_check_r8.out). Re-derived: 772-200 = 572 positive-distance pairs; 308 unreachable; 200 sources; 440 vertex pairs (sum of C(n,2) over 8 cycles); 619 edges, 1238 = 2 x 619 inspections; 1438 = 200 + 1238; 40000 = 200 x 200 matrix reads. Part C weighted paths (a: 1 hop weight 10 vs 2 hops weight 2; c: 2 hops weight 11 vs 3 hops weight 3) match the prose. Hypothesis text matches the code (seeded graphs 3-7 vertices, 40 graphs; Part D 200 vertices)."),
    row("L07-LAB", "2.5", "course/modules/CS/CS2/L07.html:208-508; tests/labs/CS2/lab-CS2-L07-1.py",
        "Re-run this round: run_labs.py --unit CS2 PASS (14/14); twin_check_r8.py: page code equals twin (rstrip) True, twin under python -I -W error exit 0 with stderr 0 bytes (10 output lines), printed expected block equals the run output True (twin_check_r8.out). Lab numbers (49 cells, 28 stored, 47 calls, 20736 naive) were checked in round 7 by l07_calls_r7.py, and the L07 page and twin are byte-identical since 7aa909e, so those derivations are carried in L07-NUMS and L07-LAB-INTERP."),
    row("L08-LAB", "2.5", "course/modules/CS/CS2/L08.html:174-550; tests/labs/CS2/lab-CS2-L08-1.py",
        "Page code equals the twin and the expected block equals the run output (15 lines), exit 0, stderr 0 bytes (twin_check_r8.out). Part A hand-trace matches the output (5 at 10000 from order 1 and 2 from order 2; order 2 left with 1 share; order 3 cancelled with 4 shares; 1 share fills and 4 rest as a bid). Part B: 298 + 102 = 400; 117 traded messages; 177 executions; final 9980 < 9989. Part C: 185 - 177 = 8 levels left; 185 + 177 = 362 searches; largest 4. Hypothesis matches the code (the check raises on a comparison count above bit_length, and on queue steps above orders added)."),
    row("L05-MATH", "2.4", "course/modules/CS/CS2/L05.html:56-118",
        "Full read of L05 prose. Re-derived: Lemma 2.3 strong induction (lines 82); N(0..7) = 0,1,2,4,7,12,20,33 (line 72) by recurrence; Proposition 2.4 M(h) = N(h)+1 recurrence and phi^2 = phi+1 (line 92); the rotation keeps in-order (Proposition 3.1 proof, line 113); the single/double rotation case split matches rebalance() in the twin (lines 215-236); Remark 2.5 two-node example (height 2, log2 2 = 1)."),
    row("L06-MATH", "2.4", "course/modules/CS/CS2/L06.html:56-120",
        "Full read of L06 prose. Re-checked Lemma 2.1 invariant (line 74), Proposition 2.2 both directions and the dist <= delta induction (line 84-88), Proposition 2.3 degree-sum bound (line 98), Proposition 3.2 parenthesis argument via the recursion tree (line 120). Definition 1.1 matches bfs() in the twin."),
    row("L08-MATH", "2.4", "course/modules/CS/CS2/L08.html:56-190",
        "Full read of L08 prose. Re-checked Proposition 1.3 (cases for buy and remainder; book uncrossed), Proposition 2.2 induction on fills, Example 2.3, Lemma 3.1, Proposition 3.2 (length recursion: n - floor(n/2) = ceil(n/2) - 1 and k-1 <= log2 L) against brute force over all L < 130 and all targets (l08_claims_r8.out: True), Proposition 3.3 items against _search, _rest, _drop_if_empty, best() in the twin."),
    row("L05-NUMS", "2.2", "course/modules/CS/CS2/L05.html:52,68-99,423,432,436,440,505,512,519,544",
        "numbers_r8.py / numbers_r8.out recomputed from first principles: log_phi(501)=12.9186; log_phi(65)=8.6747; 1/log2(phi)=1.440420; ln3/lnphi=2.28; ln377=5.932, lnphi=0.4812, log_phi(377)=12.33; log_phi(8)=4.32; 272/500=0.544; N(12)=376; log2 64=6."),
    row("L06-NUMS", "2.2", "course/modules/CS/CS2/L06.html:350-392,428,512,572",
        "numbers_r8.out: 772-200=572; 8 x sum of n = 200 sources; 8 x sum of C(n,2) = 440 pairs; 40000/1438 = 27.8164; 1438 x 27 = 38826 and remainder 1174; 1238/200 = 6.19; 2 x 619 = 1238; 200 + 1238 = 1438."),
    row("L08-NUMS", "2.2", "course/modules/CS/CS2/L08.html:52,647,658,668,670,672,695",
        "numbers_r8.out and l08_claims_r8.out: 102/400 = 25.5%; 102/398 = 25.6% (398 steps with a live order, l08_nolive_steps_r8.py); 298 + 102 = 400; 185 - 177 = 8; 185 + 177 = 362; floor(log2 7) + 1 = 3; floor(log2 8) + 1 = 4; 9980 < 9989."),
    row("L05-TERMS", "2.9 / 5", "course/modules/CS/CS2/L05.html:52 versus :56",
        "Line 52 no longer uses 'node' or 'longest downward path'. It names 'height' once with an explicit forward pointer ('where height is defined in Section 1'), and Section 1 (line 56) defines it. Judgment: a named forward pointer is treated as a deferred use, not an undefined term. A stricter reading would remove the word from line 52; the prose would still be correct."),
    row("L06-TERMS", "2.9 / 5", "course/modules/CS/CS2/L06.html:52 versus :56-60",
        "Line 52 uses only plain words ('network', 'point', 'nested record', 'search') and names no term defined later. Graph, path, hop count, BFS and DFS are defined in Section 1 and Definition 1.1 before first use in the body."),
    row("L08-TERMS", "2.9 / 5", "course/modules/CS/CS2/L08.html:52 versus :91",
        "Line 52 now says 'fixes the matching rule of Section 2 (Definition 2.1)'. 'price-time' first appears in the body at the Section 2 heading (line 88), which names the term immediately above Definition 2.1 (line 91). The meta description (line 7) uses 'price-time matching rule'; it is head metadata, not lesson body, and is not counted as a use."),
    row("L05-EXERCISES", "2.4 / 2.9", "course/modules/CS/CS2/L05.html:449-548 and quiz 566-644",
        "Re-derived M1 (balance factors 1 and 1, AVL), M2 (single left rotation, root 2), M3 (N(5)=12), P1-P3, E1 (272/500 = 0.544), E2 (log2 64 = 6 vs 7), E3 (log_phi 377 = 12.33 so height at most 12), R1 (left-right double rotation, root 2), R2 (4-height 7-node tree; all balance factors checked), R3 (N(5)=12 > 7; log_phi 8 = 4.32). Quiz answers 64, 7, 2, 12, 2, 1.440420, 272 match."),
    row("L06-EXERCISES", "2.4 / 2.9", "course/modules/CS/CS2/L06.html:396-520 and quiz 522-595",
        "Re-derived M1 (queue order 1,2,3,4,5; distances 0,1,1,2,3), M2 (d=(1,2,3), f=(6,5,4)), M3 (6 scans), P1-P3, E1 (572), E2 (40000/1438 = 27.82), E3 (1238/200 = 6.19), R1 (undirected DFS edge joins ancestor and descendant), R2, R3 (n^2). Quiz answers 3, 6, 6, 27.82, 6 and the 'number of enqueues' option match."),
    row("L08-EXERCISES", "2.4 / 2.9", "course/modules/CS/CS2/L08.html:628-692 and quiz 700-786",
        "Re-derived M1 (2 at 10010 from order 2, 3 at 10010 from order 3; resting asks 1 at 10010 and 3 at 10020), M2 (3 and 4), M3 (1 at 10000; 2 rest as bid at 10001; best ask 10005), P1 (n(floor log2 n + 1) bound), P2, P3 (min{q,Q}), E1 (398 steps; script), E2 (scenario in l08_claims_r8.out), E3 (L >= 8), R1, R2, R3 (stale read is a KeyError on self.levels[opposite][best]; labelled as a code reading). Quiz answers 3, 1, 4, 'resting order's price' and the other keys match."),
    row("L07-NOTATION-C", "carry", "course/modules/CS/CS2/L07.html:87-629 (c) and :179-184 (K)",
        CARRY + r7_rows["L07-NOTATION-C"]["evidence"]),
    carried("L07-MATH", "2.4", "course/modules/CS/CS2/L07.html:67-206"),
    carried("L07-NUMS", "2.2", "course/modules/CS/CS2/L07.html:63,179,198,203,210,504-507,528,532,556,597,602,604,611,622,624,629"),
    carried("L07-TERMS", "2.9 / 5", "course/modules/CS/CS2/L07.html:52 versus :56 and :60"),
    carried("L07-EXERCISES", "2.4 / 2.9", "course/modules/CS/CS2/L07.html:543-727"),
    carried("L07-LAB-INTERP", "2.5", "course/modules/CS/CS2/L07.html:507"),
    row("L06-XREF", "2.9 / 5", "course/modules/CS/CS2/L06.html:369 (Section 4, 'DFS paths are not shortest')",
        "Line 369 now cites 'the recursion tree of the proof of Proposition 3.2'. That proof (line 120) introduces the term: 'Let the calls form the recursion tree'. Definition 3.1 (line 110) does not define it, and the citation is now correct. Misconception 2 (line 384) triangle example re-checked: a's neighbour list is b then c, DFS tree path a-b-c has 2 hops, hop distance a to c is 1."),
    row("L08-E1", "2.2 / 2.4", "course/modules/CS/CS2/L08.html:636-641 (E1 solution)",
        "Replay of Part B's seeded stream (l08_nolive_steps_r8.py): steps with no live order before the message are 0-based [0, 2], i.e. the first and third messages, so 398 steps have a live order. 102 cancellations (l08_claims_r8.out); 102/398 = 25.6%, 102/400 = 25.5%. The text is correct."),
    row("L08-E2", "2.4 / 2.9", "course/modules/CS/CS2/L08.html:643-650 (E2 solution, changed line 647)",
        "Revised sentence is true. Scenario in l08_claims_r8.py: sell 1@10000 (oid 1), sell 1@10000 (oid 2), sell 5@10000 (oid 3); buy 1 fills oid 1 (dead entry held at head, not yet passed, queue_steps 0); a second buy passes oid 1 (queue_steps 1, counted at that fill) and fills oid 2; cancel oid 3 empties the level and it is deleted with queue_steps still 1. Second scenario: cancel of a level holding a dead entry leaves queue_steps unchanged at 0. _front is called only from submit (twin line 179), so cancellation never passes an entry."),
    row("NAV-LABELS", "2.9", "course/modules/CS/CS2/L05.html:654-655; L06.html:597-598; L07.html:738-739; L08.html:787-788",
        "Labels equal the target h1s (grep): L04 'Comparison sorting and binary search'; L05 'Balanced search trees'; L06 'Graph traversal'; L07 'Dynamic Programming'; L08 'Order Books: Price Levels with FIFO Queues'; L09 \"Welford's Online Mean and Variance\". Unchanged in the delta."),
    row("DAG-CONCEPTS", "2.9 / DAG", "course/modules/CS/CS2/L05.html:38-39; L06.html:38-39; L08.html:38-39 and link at L08.html:163",
        "check_dag.py --unit CS2 PASS (this round). Uses lists: L05 big-O, comparison-sorting, induction, exponential-and-logarithm (all in the closure, L01/L04/M1); L06 big-O, hash-map, induction; L08 hash-map, binary-search, induction. Only L08 line 163 links hash-map (L02.html#def-hash-map, defined there). Introduces are defined once with dfn."),
    row("NOTATION-REGISTRY", "2.4 / notation", "notation/notation.json; L05-L08 math spans",
        "macros_r8.py / macros_r8.out: every TeX macro used in L05-L08 math is standard TeX or a macro of notation.json (none of \\E, \\Prob, \\Var, ... used beyond the registry). Registered symbols T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f and blackboard Q appear in none of the four pages. Plain letters N, M, Q (L08 P3 total quantity), R (L05 root labels), K (L07) are local and not registered; no collision."),
    row("HOURS", "2.6 arithmetic", "course/modules/CS/CS2/L05-L08.html line 2/35; plans/CS2-build-plan.md:102-105",
        "Headers read 9, 9, 10, 10 study hours (grep 'study hours' and data-hours): L05 9, L06 9, L07 10, L08 10, matching plan rows 102-105. Hours are design targets; arithmetic consistent."),
    row("CITATIONS", "2.1", "course/modules/CS/CS2/L05.html:648; L06.html:591; L07.html; L08.html:781",
        "references/references.json holds cormen2022introduction (line 5962). L05 and L06 reference sections state the lesson cites no outside source and attribute no number or locator to the textbook. L08 states it cites no registry source. verify_refs --offline: 0 problems (verify_refs_r8.out)."),
]

fragment = {
    "unit": "CS2",
    "slice": "b",
    "round": 8,
    "verifier": "Haiku 5.5 independent verifier (slice b, round 8)",
    "pin": "ce7b382",
    "base": "7aa909e (round-7 pin). Delta 7aa909e..ce7b382 for this slice: course/modules/CS/CS2/L05.html:52; L06.html:369; L08.html:52,647. Also changed in the delta but outside this slice: cards.json, project.html, other units' tests/labs and ledgers. Every hunk in the slice delta was read (see notes). Round-7 fragment read as context: /Users/billyribeiro/.fanout/frags/B-CS2-b.round7.json.",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyB8-CS2-b",
    "scratch": "No /tmp directories kept. Scripts and outputs are in ledgers/CS2/scripts/CS2-b-r8/ (twin_check_r8.py, macros_r8.py, l08_claims_r8.py, l08_nolive_steps_r8.py, numbers_r8.py, build_fragment_r8.py).",
    "verified_at": "2026-10-28",
    "verdict": "PASS",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "Lesson-only slice: mutation testing does not apply to lesson pages (rulings), so no mutants are listed. "
        "Round-8 delta-based: every hunk of the slice delta was read (L05 line 52; L06 line 369; L08 lines 52 and 647), and the changed rows were re-verified from scratch: L05-TERMS, L06-XREF, L08-TERMS, L08-E2. "
        "Because this round read L05, L06 and L08 in full (prose, problems, quiz, references), their rows were re-checked against this round's evidence rather than carried; the L07 rows are carried from round 7 under the byte-identity rule (L07.html and its twin are unchanged since 7aa909e). "
        "Judgment calls: L05-TERMS passes because 'height' is named with an explicit forward pointer to Section 1, and L08-TERMS passes because the body no longer uses 'price-time' before Definition 2.1. "
        "Not checked: (a) verify_refs live run (references unchanged; slice cites no key with a locator); (b) the cards in course/modules/CS/CS2/cards.json, which changed in the delta and belong to slice d; they must agree with the lesson text, which this slice's round-8 reading did not test card by card; (c) hub and project pages (other slices); (d) mypy and pytest were run repo-wide, not per slice; (e) the lab timing is reported by page_smoke only (0.0-0.1 s), since the lab measures no time by design."
    ),
    "summary": "Slice b (L05-L08 and twins), round 8, pin ce7b382. Rows: 42 PASS, 0 FAIL. Round-7 FAIL rows L05-TERMS, L06-XREF, L08-TERMS, L08-E2 re-verified and now PASS; gates re-run on the pin and green.",
}

print("rows", len(rows), "statuses", sorted({r["status"] for r in rows}))
ids = [r["id"] for r in rows]
print("duplicate ids", sorted({i for i in ids if ids.count(i) > 1}))
print("round-7 ids not present", sorted(set(r7_rows) - set(ids)))
json.dump(fragment, open(f"{ROOT}/ledgers/CS2/CS2-b.json", "w", encoding="utf-8"), indent=2, ensure_ascii=False)
print("written")
