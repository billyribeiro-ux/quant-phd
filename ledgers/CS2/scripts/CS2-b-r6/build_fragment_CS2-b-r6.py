"""Verifier round 6: write ledgers/CS2/CS2-b.json (slice b, L05-L08, twins, slice cards) at pin e896b7a4.

Usage: python3 -I build_fragment_CS2-b-r6.py <checkout>
Rows are the verifier's judgements, recorded from the commands and reads listed in each evidence string.
Round-5 row ids are all kept. Rows whose cited subject is byte-identical to the round-5 pin (dde0486b) are
carried with the required prefix; every other row was re-verified in this round.
"""
import json
import sys
from datetime import UTC, datetime
from pathlib import Path

root = Path(sys.argv[1])
S = "ledgers/CS2/scripts/CS2-b-r6"
R5 = json.load(open("/Users/billyribeiro/.fanout/frags/S-CS2-b.round5.json", encoding="utf-8"))
r5 = {r["id"]: r for r in R5["rows"]}
CARRY = "Carried from round 5 (cited lines of {n}, and any twin they name, are byte-identical since dde0486b; the round-6 delta hunks lie outside them): "
PASS = "PASS"


def fresh(i, check, location, evidence):
    return {"id": i, "check": check, "location": location, "status": PASS, "evidence": evidence}


def carried(i, n_or_text, location=None):
    old = r5[i]
    label = f"course/modules/CS/CS2/L0{n_or_text}.html" if n_or_text.isdigit() else "course/modules/CS/CS2/L05.html..L08.html"
    text = n_or_text if n_or_text.startswith("Carried") else CARRY.format(n=label) + old["evidence"]
    return {"id": i, "check": old["check"], "location": location or old["location"], "status": PASS, "evidence": text}


rows = [
    fresh("CS2b-gate-check-pages", r5["CS2b-gate-check-pages"]["check"], "course/modules/CS/CS2/L05.html..L08.html, cards.json",
          f"{S}/gates_r6.out: 'check_pages CS2 L05', L06, L07, L08 PASS (exit 0 each, run with --unit CS2 --page); 'check_pages CS2: PASS' exit 0."),
    fresh("CS2b-gate-check-dag", r5["CS2b-gate-check-dag"]["check"], "L05-L08 links; dfn ids",
          f"{S}/gates_r6.out: 'check_dag CS2: PASS' exit 0."),
    fresh("CS2b-gate-check-projects", r5["CS2b-gate-check-projects"]["check"], "course/modules/CS/CS2/project.html",
          f"{S}/gates_r6.out: 'check_projects CS2: PASS' exit 0 (no project change in this delta)."),
    fresh("CS2b-gate-run-labs", r5["CS2b-gate-run-labs"]["check"], "tests/labs/CS2/lab-CS2-L05-1.py .. lab-CS2-L08-1.py",
          f"{S}/gates_r6.out: 'run_labs CS2: PASS (14/14)' exit 0. Twins alone under python -I -W error: L05, L06, L07, L08 exit 0 ({S}/gates_misc_r6.out)."),
    fresh("CS2b-gate-lab-exact", r5["CS2b-gate-lab-exact"]["check"], "course/modules/CS/CS2/L05.html..L08.html; tests/labs/CS2/lab-CS2-L0{5,6,7,8}-1.py",
          f"{S}/page_code_eq_twin_r6.out: page lab code identical to twin after strip for L05, L06, L07, L08 (L06 and L07 identical after the docstring change). {S}/expected_vs_stdout_r6.out: expected block equals twin stdout line for line, L05 31 lines (starts line 383), L06 17 (349), L07 10 (498), L08 15 (534)."),
    fresh("CS2b-gate-page-smoke", r5["CS2b-gate-page-smoke"]["check"], "course/modules/CS/CS2/L05.html..L08.html",
          f"{S}/gates_run2_r6.out: 'page_smoke modules/CS/CS2/L05..L08.html: PASS', 'page_smoke CS2: PASS' (run alone with --pages L05 L06 L07 L08 --skip-sweep)."),
    fresh("CS2b-gate-ruff-mypy", r5["CS2b-gate-ruff-mypy"]["check"], "tests/labs/CS2/lab-CS2-L06-1.py, lab-CS2-L07-1.py (changed twins)",
          f"{S}/gates_misc_r6.out: ruff check 'All checks passed!', ruff format --check '2 files already formatted', mypy --no-incremental 'Success: no issues found in 2 source files'. L05 and L08 twins unchanged since dde0486b (checked by the round-5 run)."),
    fresh("CS2b-gate-pytest", r5["CS2b-gate-pytest"]["check"], "tests/test_labs.py -k CS2; tests/test_page_checks.py",
          f"{S}/gates_run_r6.out: pytest --collect-only tests/test_labs.py -k CS2 reports 14; pytest -q tests/test_labs.py -k CS2: 14 passed (exit 0); pytest -q tests/test_page_checks.py: 41 passed (exit 0)."),
    fresh("CS2b-gate-build-site", r5["CS2b-gate-build-site"]["check"], "tools/build_site.py --check (cards.json feeds the site data)",
          f"{S}/gates_misc_r6.out: 'site data current: 6 outputs', exit 0, after the cards.json change."),
    fresh("CS2b-gate-verify-refs", r5["CS2b-gate-verify-refs"]["check"], "references/references.json; L05 and L06 reference sections",
          f"{S}/gates_run2_r6.out: 'offline integrity: 560 entries, 0 problems', exit 0. The live run was not repeated (references/ unchanged in this delta; see notes)."),
    fresh("CS2b-L05-lab-numbers", r5["CS2b-L05-lab-numbers"]["check"], "L05.html lines 52, 99, 414, 422, 436, 440, 505, 519, 544; expected block 383-413",
          "Re-run of tests/labs/CS2/lab-CS2-L05-1.py (out_L05.txt, twin run in this round): rotation_calls_total 340, kinds 63/53/55/57, inserts_without_rotation 272 of 500, max_rotation_calls 2, avl_height 7 for keys 1..64, bound 8.6747, two_node_avl_height 2, 1/log2(phi) 1.440420 (page lines 99, 414, 436 and 440 show the same values). Expected block equal to stdout (expected_vs_stdout_r6.out)."),
    fresh("CS2b-L06-lab-numbers", r5["CS2b-L06-lab-numbers"]["check"], "L06.html lines 103, 362, 388, 453, 459, 467; expected block 349-365",
          "out_L06.txt (this round): graphs 40, sources 200, reachable 772, unreachable 308, mismatches 0; parenthesis pairs 440, violations 0; Part C weights 10/1/1/1 with a->lightest s-b-a weight 2 vs bfs s-a weight 10; Part D edges 619, enqueues 200, adjacency entries 1238, row reads 40000. Expected block equals stdout (expected_vs_stdout_r6.out)."),
    fresh("CS2b-L07-lab-numbers", r5["CS2b-L07-lab-numbers"]["check"], "L07.html lines 63, 198, 203, 210, 503-507, 513-514, 532, 585-586, 597, 604, 610-611, 656",
          "out_L07.txt (this round): LCS 30 instances all agree; coins 30 instances, 6 of 30 with no combination; (1,3,4) amount 6: greedy 3 coins, optimum 2; LCS ACGTACG/TGCATGC: 49 cells, memo stores 28, memo calls 47, no-memo calls 183; coins amount 20: 5 coins, stored 20, memo calls 56, no-memo calls 20736. All equal the page numbers cited. Expected block equals stdout."),
    fresh("CS2b-L08-lab-numbers", r5["CS2b-L08-lab-numbers"]["check"], "L08.html lines 541-549, 575, 637-640, 653-654; expected block 534-548",
          "out_L08.txt (this round): part C levels created 185, removed 177 (so 8 remain), binary searches 362 (= 185 + 177), largest comparison count 4; expected block equals stdout (expected_vs_stdout_r6.out). L08 twin unchanged since dde0486b."),
    fresh("CS2b-L05-lab-hypothesis", r5["CS2b-L05-lab-hypothesis"]["check"], "L05.html lines 122-123, 414-423, 436, 452-455; twin tests/labs/CS2/lab-CS2-L05-1.py",
          "L05.html line 123 read in this round: 500 seeded keys, sorted keys 1 to 64, Parts A to C as printed; checks after every insertion (Part A) match out_L05.txt (final_size 500, invariant lines). Lines 414-423 and 436 read in this round (interpretation and misconception paragraphs)."),
    fresh("CS2b-L06-lab-hypothesis", r5["CS2b-L06-lab-hypothesis"]["check"], "L06.html lines 124-140, 362-388; tests/labs/CS2/lab-CS2-L06-1.py parts A-D and docstring lines 1-15",
          "L06.html line 125 (hypothesis) read in this round: 'one weighted graph of 4 vertices' for Part C matches the twin's fixed adjacency and weights (twin lines 180-181). Its statement that the graphs of A, B and D are seeded matches twin lines 23, 200-202 and 216. Twin docstring now matches the code (see CS2b6-L06-docstring)."),
    {"id": "CS2b-L07-lab-hypothesis", "check": r5["CS2b-L07-lab-hypothesis"]["check"],
     "location": "course/modules/CS/CS2/L07.html line 206 and line 213 (lab docstring); tests/labs/CS2/lab-CS2-L07-1.py line 3 (docstring) and lines 23-27 (FIXED_X, FIXED_Y, FIXED_COINS, FIXED_AMOUNT, PART_C_AMOUNT)",
     "status": "FAIL",
     "evidence": "L07.html line 206 reads 'Every instance is SIMULATED: it is generated from a fixed seed, and none is market data.'; line 213 and twin line 3 read 'SIMULATED: every instance is generated from a fixed seed by an integer generator'. The code does not generate the Part C instance: the LCS pair FIXED_X = \"ACGTACG\", FIXED_Y = \"TGCATGC\" (twin lines 23-24) and the coin set FIXED_COINS = (1, 3, 4) with FIXED_AMOUNT = 6 and PART_C_AMOUNT = 20 (lines 25-27) are literals, not seeded draws. The page names the pair explicitly (lines 63, 210 and 657) and never says that it is generated from the seed. Same defect class as the L06 docstring that the round-6 delta corrected (L06.html lines 128-130 now say 'Part C uses one fixed weighted graph written out in the code').",
     "fix": "Replace the sentence in L07.html line 206 and in the twin and page docstring (twin line 3; page line 213) with: 'SIMULATED: the seeded instances of Parts A and B are generated from a fixed seed by an integer generator; the Part C pair ACGTACG and TGCATGC and the coin set (1, 3, 4) are fixed values written out in the code; none is market data.' Re-embed with tools/embed_labs.py L07 --refresh lab-CS2-L07-1 and re-run the page and twin gates."},
    carried("CS2b-L08-lab-hypothesis", "8"),
    carried("CS2b-L05-math", "5"),
    carried("CS2b-L06-math", "6"),
    carried("CS2b-L07-math", "7"),
    carried("CS2b-L08-math", "8"),
    carried("CS2b-L05-problems", "5"),
    carried("CS2b-L06-problems", "6"),
    carried("CS2b-L07-problems", "7"),
    carried("CS2b-L08-problems", "8"),
    carried("CS2b-L05-misconceptions-canon", "5"),
    carried("CS2b-misconception-counts", "5-8", "L05 lines 431-440; L06 379-388; L07 523-528; L08 566-575"),
    carried("CS2b-L06-canon-undirected", "6"),
    carried("CS2b-L06-connected-component", "6"),
    fresh("CS2b-L05-terms-avl", r5["CS2b-L05-terms-avl"]["check"], "L05.html line 52, Definition 2.1 lines 66-67, Remark 3.2 lines 117-118, Proposition 2.4 lines 86-87",
          "Definition 2.1 changed at line 67 in this delta. Re-read: it now says 'This unit uses the AVL variant, whose rule is stated below. Proposition 2.4 bounds the height of every tree that keeps that rule; that the restructuring keeps the rule after each insertion is not proved here (Remark 3.2).' Remark 3.2 (line 118) says the page does not prove that one single or double rotation restores the AVL rule after every insertion, so the cross-reference is accurate. Line 52 still cites Proposition 2.4 for the AVL variant, consistent with line 67. Card CS2-c057 agrees (see CS2b4-cards-balanced-tree)."),
    fresh("CS2b6-L05-def21-remark32", "Definition 2.1 and Remark 3.2 agree (new row for the round-6 change)",
          "course/modules/CS/CS2/L05.html lines 67 and 117-118",
          "Read in this round: Definition 2.1 defers the insertion claim to Remark 3.2; Remark 3.2 says that one single or double rotation restoring the AVL rule after every insertion is checked by Lab 1, Part A and not proved here. No contradiction. Lemma 2.3 and Proposition 2.4 are proved on lines 76-99 (unchanged)."),
    carried("CS2b-L06-quiz-terms", "6"),
    fresh("CS2b6-L06-docstring", "Lab docstring equals the code (new row for the round-6 change)",
          "course/modules/CS/CS2/L06.html lines 126-130; tests/labs/CS2/lab-CS2-L06-1.py lines 1-5",
          "Read in this round: 'the random graphs of Parts A, B and D are seeded undirected graphs (seed 20261028 and offsets from it); Part C uses one fixed weighted graph written out in the code.' Code: Parts A and B draw from random.Random(SEED) (twin lines 215-216, main), Part D from SEED + 1000 (line 200), Part C has a literal adjacency and weight dict (lines 180-181). Adjacency lists are sorted by random_graph (lines 35-36). Page code equals twin (page_code_eq_twin_r6.out)."),
    fresh("CS2b-quiz", r5["CS2b-quiz"]["check"], "L05 lines 571-641; L06 518-594; L07 667-725; L08 708-774 (L08 q4 line 730 changed)",
          "L08.html line 730 changed to 'so that price comparisons involve no floating-point rounding' (data-correct); distractors 'faster to read' (line 729) and 'fractional shares' (line 731) remain false, and the explanation at line 733 is the lesson convention of line 56 (integer cents, float refused in Part A). Read in this round. L05, L06 and L07 quiz blocks are outside the delta hunks."),
    carried("CS2b-hours", "5-8", "course/index.html and lesson lists; L05 9 h, L06 9 h, L07 10 h, L08 10 h"),
    fresh("CS2b-structure", r5["CS2b-structure"]["check"], "course/modules/CS/CS2/L05.html..L08.html",
          f"{S}/gates_r6.out check_pages PASS for each page (fresh run); page_smoke PASS (gates_run2_r6.out)."),
    fresh("CS2b-dag", r5["CS2b-dag"]["check"], "L05-L08 'Uses' lines and links",
          f"{S}/gates_r6.out check_dag CS2 PASS. New cross-reference in L05 line 67 ('Remark 3.2') resolves to the same page (line 117). No new concept links are added in the delta."),
    fresh("CS2b-notation", r5["CS2b-notation"]["check"], "changed math: L05 line 67 (\\(-1\\), \\(0\\), \\(1\\)); L06 docstring; L07 docstring; L08 line 730 (no math)",
          "Symbols in the changed text are the balance factors \\(-1\\), \\(0\\) and \\(1\\) (existing notation, Definition 2.1) and no new symbol is introduced; the docstrings and the quiz option contain no symbol outside notation."),
    fresh("CS2b-banned-and-process-words", r5["CS2b-banned-and-process-words"]["check"], "L05-L08 visible prose",
          "grep of L05-L08 for verifier, round N, delta, builder, revised, corrected, updated, ledger, fragment, 'we fixed' returns only ordinary words ('the previous', 'Previous' in navigation links at L05 line 654, L06 line 601, L07 line 739, L08 line 787) and no process word. Changed sentences read in this round contain none."),
    {"id": "CS2b-scope-words", "check": r5["CS2b-scope-words"]["check"],
     "location": "course/modules/CS/CS2/L07.html line 206 ('Every instance is SIMULATED: it is generated from a fixed seed'); L07.html line 213 and twin line 3 ('every instance is generated from a fixed seed')",
     "status": "FAIL",
     "evidence": "The universal scope word 'every' is asserted for 'instances' generated from a fixed seed, but Part C's instances (FIXED_X, FIXED_Y, FIXED_COINS, FIXED_AMOUNT, PART_C_AMOUNT, twin lines 23-27) are written literals and no computation in the lab generates them from the seed. Other changed sentences pass: L05 line 67 'every tree that keeps that rule' (Proposition 2.4 quantifies over every AVL tree); L06 docstring 'Part C uses one fixed weighted graph' (no universal claim); L08 line 730 has no scope word.",
     "fix": "Same edit as CS2b-L07-lab-hypothesis: name the seeded parts (A and B) and the fixed Part C values instead of 'every instance'."},
    carried("CS2b-grades", "5-8", "data-grade attributes in L05-L08 (14, 18, 15, 22 occurrences)"),
    carried("CS2b-data-figures", "5-8", "L05-L08 figures and data attributes"),
    fresh("CS2b-lab-simulated-labels", r5["CS2b-lab-simulated-labels"]["check"], "L05-L08 lab sections and twins",
          "The SIMULATED labels at L05 line 123, L06 line 125, L07 line 206 and L08 line 549 (read in this round) are accurate for each lab (seeded or fixed synthetic data, no market data). The L07 generation sentence is FAIL under CS2b-L07-lab-hypothesis, not here."),
    carried("CS2b-key-results-ungraded", "5-8", "L05.html 556-560; L06.html 508-510; L07.html 648-656; L08.html 691-697"),
    fresh("CS2b-cards-trivia", r5["CS2b-cards-trivia"]["check"], "cards.json slice cards (73 in L05-L08)",
          "All 73 slice cards read in full this round (json dump). None is a recall item without a stated proposition, definition or lab result. The card removed in this delta (CS2-c077, a count from Proposition 2.3) is replaced by CS2-c242 and CS2-c243, which cite Proposition 2.3 (L06 line 93)."),
    fresh("CS2b-cards-correctness", r5["CS2b-cards-correctness"]["check"], "cards.json CS2-c223; L08.html line 60 (Definition 1.1)",
          "Previous FAIL re-verified. CS2-c223 back now reads 'A dead entry stays in its queue until the head passes it or its price level is removed (Definition 1.1).' L08.html line 60: 'until the head passes it or its price level is removed, which happens when the level has no live order.' Agreement. Twin _drop_if_empty (lab-CS2-L08-1.py lines 155-158) removes a level when live == 0."),
    fresh("CS2b-cards-duplicates", r5["CS2b-cards-duplicates"]["check"], "cards.json CS2-c077 (removed), CS2-c242, CS2-c243",
          f"Previous FAIL re-verified. CS2-c077 is removed in this delta (git diff dde0486b e896b7a4 cards.json). CS2-c242 and CS2-c243 now split its two claims. Slice near-duplicate scan: only pair CS2-c242/CS2-c243 (front 0.81, back 0.67) and they state different counts (enqueues <= |V|; inspections <= 2|E|). {S}/duplicate_scan_r6.out."),
    fresh("CS2b-cards-hypotheses", r5["CS2b-cards-hypotheses"]["check"], "cards.json CS2-c242 and CS2-c243 against L06.html line 93 (Proposition 2.3)",
          "Proposition 2.3 hypotheses: undirected graph with |V| vertices and |E| edges, stored as adjacency lists. CS2-c242 states 'undirected graph with |V| vertices' and 'Assume the graph is stored as adjacency lists'; CS2-c243 states '|E| edges' with the same assumption. Both match."),
    fresh("CS2b-cards-numbers-crossrefs", r5["CS2b-cards-numbers-crossrefs"]["check"], "cards.json slice cards",
          f"{S}/cards_delta_r6.out: 'dangling citations in slice cards []' (every Definition, Proposition, Lemma, Theorem, Corollary, Remark, Example, Problem and Assumption cited by the 73 slice cards appears in its own lesson page). Numbers: CS2-c113 (185 - 177 = 8), CS2-c237 (362 = 185 + 177), CS2-c240 (4 comparisons imply >= 8 prices) agree with out_L08.txt."),
    fresh("CS2b-cards-full-scan", r5["CS2b-cards-full-scan"]["check"], "cards.json, 73 slice cards",
          "All 73 slice cards read in full this round (L05 18, L06 15, L07 22, L08 18 by lesson field). Changed or removed cards in the slice: CS2-c077 (removed), CS2-c223 (changed); all other slice cards are identical to dde0486b (cards_delta_r6.out, 'slice changed [CS2-c223]')."),
    fresh("CS2b4-cards-balanced-tree", r5["CS2b4-cards-balanced-tree"]["check"], "cards.json CS2-c057; L05.html line 67 (Definition 2.1) and line 86 (Proposition 2.4)",
          "Re-verified because Definition 2.1 changed. CS2-c057 back: 'A binary search tree that restructures itself after each change, with the aim of keeping its height logarithmic ... (Definition 2.1). Proposition 2.4 proves the height bound for the AVL variant, which this unit uses.' L05 line 67 and line 86 agree."),
    carried("CS2b4-L06-P2-forest-wording", "6", "L06.html line 437 (P2); recursion forest introduced in the proof of Proposition 3.2 at line 120"),
]

fragment = {
    "unit": "CS2",
    "slice": "b",
    "round": 6,
    "round_note": "Round 6 DELTA verification of CS2 slice b at pin e896b7a4 (base round-5 pin dde0486b). Delta read in full for the slice: L05.html line 67 (Definition 2.1); L06.html lines 126-130 (lab docstring); L07.html lines 215-218 (lab docstring); L08.html line 730 (quiz option); tests/labs/CS2/lab-CS2-L06-1.py lines 1-5 and lab-CS2-L07-1.py lines 1-8; cards.json (CS2-c077 removed, CS2-c223 changed; other changed cards are L04, L09, L10, L11 and belong to other slices). The round-5 fragment is read as context only; its FAIL rows CS2b-cards-correctness and CS2b-cards-duplicates were re-verified and are PASS; its PASS rows were not trusted where the subject changed.",
    "verifier": "Haiku 5.5 independent verifier, CS2 slice b, round 6 (did not build CS2)",
    "pin": "e896b7a4",
    "base": "dde0486b (round-5 pin)",
    "checkout": str(root),
    "scratch": "/tmp/cs2b_r6 (twin stdout out_L0{5,6,7,8}.txt copied to the scripts directory; card git-show copies)",
    "verified_at": datetime.now(UTC).isoformat(timespec="seconds"),
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Lesson and card slice: mutation testing does not apply (no project grader in this slice; lab twins are demonstrations, ruling 9). No mutants authored.",
        "Judgement, PASS: L08 quiz q4 'why are prices stored as integer cents' has a convention answer; the lesson states the convention (line 56) and the explanation (line 733) calls it a lesson convention, so it is not an unsupported result.",
        "Judgement, PASS: CS2-c242 and CS2-c243 share a front template but state different counts; not duplicates.",
        "Judgement, PASS: 'What is ...' definitional card fronts carried from round 4 and round 5 are not reopened (their subjects are byte-identical).",
        "Out of slice, not verified here: cards.json changes to CS2-c040, c047, c050, c055 (L04), c125, c194 (L09), c200 (L11), c231, c234 (L10) and removals CS2-c124 (L09) and CS2-c207 (L11) belong to other slices.",
        "Pre-existing tracked files in ledgers/CS2/scripts/CS2-b-r6/ (claims_r6.py, l07_l08_claims_r6.py, l08_claims_r6.py, from commit 7aa909e) were not written by this round and were not relied on.",
        "Not run: verify_refs live (references/ unchanged in this delta); check_pages --all and run_graders/mutate_graders (no grader in this slice, unit-wide run not needed for a lesson slice); repo-wide ruff and mypy (only the two changed twins were checked, plus the round-5 result for unchanged twins).",
        "Not checked: the L07 hypothesis and docstring rewording itself (the fix is proposed, not applied, per verifier rules).",
    ],
    "summary": "Slice b (L05-L08, twins, slice cards), round 6, pin e896b7a4. Rows: 53 total, 51 PASS, 2 FAIL (CS2b-L07-lab-hypothesis and CS2b-scope-words, the same L07 'every instance is generated from a fixed seed' claim at page lines 206 and 213 and twin line 3). Round-5 FAIL rows CS2b-cards-correctness and CS2b-cards-duplicates are PASS at this pin. New rows CS2b6-L05-def21-remark32 and CS2b6-L06-docstring are PASS.",
}

out = root / "ledgers/CS2/CS2-b.json"
out.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
sys.path.insert(0, str(root / "tools"))
import ledger  # noqa: E402

print("ids", len(rows), "unique", len({r["id"] for r in rows}))
print("missing round-5 ids", sorted(set(r5) - {r["id"] for r in rows}))
print("validate", ledger.validate(json.loads(out.read_text(encoding="utf-8")), "CS2-b"))
