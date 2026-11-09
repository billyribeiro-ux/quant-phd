# Verifier script (M7-b round 1): builds ledgers/M7/M7-b.json from the round-2 base fragment and this round's evidence.
# Carried rows keep the base evidence and get the carry prefix; fresh rows carry this round's command outputs.
import datetime
import json
import os

BASE = os.path.expanduser("~/.fanout/frags/S-M7-b.round2.json")
base = {r["id"]: r for r in json.load(open(BASE, encoding="utf-8"))["rows"]} if False else None
base_frag = json.load(open(BASE, encoding="utf-8"))
base = {r["id"]: r for r in base_frag["rows"]}
S = "ledgers/M7/scripts/M7-b-r1"
PFX = "Carried from round 2 (%s byte-identical since the previous pin 9294b914): "

CARRY = {
    "b-r1-L04-math": "course/modules/M/M7/L04.html",
    "b-r1-L04-lab-claims": "course/modules/M/M7/L04.html; tests/labs/M7/lab-M7-L04-1.py",
    "b-r1-L04-grades-scope": "course/modules/M/M7/L04.html",
    "b-r1-L05-math": "course/modules/M/M7/L05.html",
    "b-r1-L05-lab-claims": "course/modules/M/M7/L05.html; tests/labs/M7/lab-M7-L05-1.py",
    "b-r1-L05-grades-scope": "course/modules/M/M7/L05.html",
    "b-r1-L06-math": "course/modules/M/M7/L06.html",
    "b-r1-L06-lab-claims": "course/modules/M/M7/L06.html; tests/labs/M7/lab-M7-L06-1.py",
    "b-r1-L06-grades-scope": "course/modules/M/M7/L06.html",
    "b-r1-L06-E2-E3-unrounded": "course/modules/M/M7/L06.html; tests/labs/M7/lab-M7-L06-1.py",
    "b-r1-stray-CU": "course/modules/M/M7/L05.html; course/modules/M/M7/L06.html; tests/labs/M7/lab-M7-L05-1.py; tests/labs/M7/lab-M7-L06-1.py",
    "b-r1-notation": "course/modules/M/M7/L04.html; L05.html; L06.html; notation/notation.json",
    "b-r1-citations": "course/modules/M/M7/L04.html; L05.html; L06.html; references/references.json",
    "b-r1-process-words-banned": "course/modules/M/M7/L04.html; L05.html; L06.html",
    "b-r1-prose-numbers-printed": "course/modules/M/M7/L04.html; L05.html; L06.html; tests/labs/M7/lab-M7-L04-1.py; lab-M7-L05-1.py; lab-M7-L06-1.py",
    "b-r1-hypotheses-proofs": "course/modules/M/M7/L04.html; L05.html; L06.html",
    "b-r1-quiz-keys": "course/modules/M/M7/L04.html; L05.html; L06.html",
    "b-r1-cards-L05": "course/modules/M/M7/cards.json L05 objects (ids c073-c093, c166, c171, c172, c182, c198, c205, c223: object-equal to 9294b914 per %s/cards_delta_by_id.out); course/modules/M/M7/L05.html" % S,
    "b-r2-slater-converse-xref": "course/modules/M/M7/L04.html; course/modules/M/M7/L03.html",
    "b-r2-efficient-set-definition": "course/modules/M/M7/L06.html",
    "b-r2-L05-part-b-candidates": "course/modules/M/M7/L05.html; tests/labs/M7/lab-M7-L05-1.py",
}

FRESH = {
    "b-r1-check-pages": ("check_pages --unit M7 and --unit M7 --page L04, L05, L06 on 95f3f8cb: all PASS, exit 0 (%s/check_pages_M7.txt, check_pages_L04.txt, check_pages_L05.txt, check_pages_L06.txt)." % S),
    "b-r1-dag-concepts": ("check_dag --unit M7 PASS and check_dag --all PASS (SC1, LX1, LX2, PC3 and every unit listed; exit 0) on 95f3f8cb (%s/check_dag_M7.txt, check_dag_all.txt). The DAG prose claims for L04-L06 (dfn lagrangian-duality L04.html:59; quadratic-programming L05.html:60; mean-variance L06.html:65 and :120) are carried: the three pages are byte-identical since 9294b914." % S),
    "b-r1-page-smoke": ("page_smoke --unit M7 --pages L04 L05 L06 on 95f3f8cb: 'page_smoke M7: PASS', exit 0; PASS for modules/M/M7/L04.html, L05.html, L06.html (%s/page_smoke_M7_L04-L06.txt)." % S),
    "b-r1-run-labs-twins": ("run_labs --unit M7 on 95f3f8cb: 'run_labs M7: PASS (11/11)', exit 0 (%s/run_labs_M7.txt). pytest tests/test_labs.py -k M7: 11 passed, exit 0 (%s/pytest_labs_M7.txt). Each twin run as python -I -W error exits 0 with 0 bytes of stderr (%s/twin_L04.err, twin_L05.err, twin_L06.err). Twin md5 equals 9294b914 for L05 and L06 (git show comparison; L04 unchanged by git diff). The twins hold no test functions, so pytest --collect-only on them reports 'no tests collected' (exit 5, %s/collect_L04-L06_plain.txt); the lab tests are the 11 in tests/test_labs.py." % (S, S, S, S)),
    "b-r1-lint-types": ("ruff check on the three twins: 'All checks passed!' exit 0; ruff format --check: '3 files already formatted' exit 0; MYPYPATH=course/modules/M/M7/grader mypy --no-incremental --strict on the three twins: 'Success: no issues found in 3 source files' exit 0 (%s/ruff_check_twins.txt, ruff_format_twins.txt, mypy_twins.txt)." % S),
    "b-r1-cards-L04": ("Fresh because M7-c058 (L04) changed in the delta. All 22 L04 card texts read (%s/cards_L04-L06_dump.txt). c058 'standing assumption of Section 1' checked: L04.html:55 'Assume throughout that F is non-empty.' is inside Section 1 (h2 at L04.html:53); Prop 1.3 at L04.html:75-76 says it needs no convexity. c058 PASS. Numbers recomputed from scratch with Fractions (%s/l04_cards_check.py, l04_cards_check.out): g(0,0) = -199/300 and p*-g(0,0) = 49/300 (c064, c069); mu'Sinv mu = 199/150 (c064); g(0,3/10),-1/2 = -1/2 = f(1,0) (c218, c170); max of g over lambda=(0,0), nu in {-1..0}/10 is -157/300, so grid gap 7/300 (c060); 1331 dual and 21 primal points, 27951 of 27951 weak-duality pairs (c063, c204); grid gap 0 (c213); largest dual value -1/2 at one point (c170); Example 3.4 g(lambda) = -1/(4 lambda) checked by hand (c068). Card numbers present in L04 (%s/cards_numbers_check.out, 83 L04-L06 cards checked, missing 0). Every L04 numeric claim above was recomputed; the card texts of the 21 unchanged L04 objects (c056-c057, c059-c060, c061-c065, c067-c071, c170, c196, c197, c204, c213, c218, c222) are object-equal to 9294b914 (cards_delta_by_id.out) and their lesson text is byte-identical. PASS." % (S, S, S)),
    "b-r1-cards-L06-except-c114": ("Fresh for the changed objects: M7-c103 (L06.html:108 'the infimum of f_gamma over F+ is at least the infimum over F0'; L06.html:113 F+ subset F0; card text matches; PASS); M7-c174 (L06.html:150 predicts one passing candidate at each gamma; the twin prints candidates_passing 1 at gamma 1, 2, 4, 8, 16 in the Part B table, twin_L06.out; card text matches; PASS). M7-c114 and M7-c228 are the subject of their own rows. The other 29 L06 card objects (c097-c102, c104-c113 except c114, c115-c118, c163, c164, c167, c200, c206-c210) are object-equal to 9294b914 (%s/cards_delta_by_id.out) and their lesson text is byte-identical, so the round-2 verdict carries: 'Carried from round 2 (course/modules/M/M7/L06.html and those 29 card objects byte-identical since the previous pin 9294b914)'. All 33 L06 card texts were read in %s/cards_L04-L06_dump.txt. PASS." % (S, S)),
    "b-r1-card-c114": ("Fresh: M7-c114 back now reads '0.5588607333 from the exact fractions, as the lab's ten-place line turnover_exact_at_gamma 4 prints; it is 0.558861 to six places (line turnover_at_gamma 4).' Printed lines: twin_L06.out 'turnover_at_gamma 4 0.558861' and 'turnover_exact_at_gamma 4 0.5588607333'; the twin computes turnover from Fraction weights (lab-M7-L06-1.py:205-207, Fraction(0) sums). L06.html:407 and :514-516 agree. The removed sentence about the six-place weights moved to new card c228. PASS." ),
    "b-r1-cards-duplicates": ("Fresh on the whole cards.json (203 cards, up from 199): 203 unique ids and 0 duplicate fronts (python -I scan, %s/cards_dup_scan.py). Near-duplicate scan (SequenceMatcher front >= 0.8 or back >= 0.9, %s/cards_dup_scan.out) flags 7 pairs: c043/c216, c046/c047, c087/c182, c110/c209, c110/c210, c209/c210, c202/c203. Each pair asks a different fact (for example c110 asks Part A return, c209 Part A risk term, c210 Part A weights; c087 asks x, c182 asks lambda); none is a repeat. c043, c046, c047, c202, c203, c216 are outside slice b and not judged further. PASS." % (S, S)),
    "b-r1-cards-numbers-labels": ("Fresh: cards_numbers_check.py (copy at %s/cards_numbers_check.py) reports 'cards checked 83, missing count 0' over L04, L05 and L06 cards (%s/cards_numbers_check.out). Lab-derived cards: grade C with a basis naming Lab 1 for all lab-result cards; c228 basis 'Lab 1, Part D (SIMULATED), computed from the printed six-place weights'. Grade/basis scan in %s/cards_grade_basis_check.out: C 25, T 58; the five T cards that name Lab 1 (c060, c085, c090, c099, c101) state hand-derivable facts (Problem R3 gap 7/300 recomputed; Remark 3.5; 2^p count; Section 1 input status; Remark 1.4). PASS." % (S, S, S)),
    "b-r1-simulated-labels": ("Fresh because M7-c174 changed and c228 is new. Every C card in L04-L06 names Lab 1 in its basis; 23 of 25 carry '(SIMULATED)' in the basis. The two without it, c204 and c213 (basis 'Lab 1, exact arithmetic on the listed grids'), are L04 lab results whose lab carries the visible label: lab docstring 'illustrative inputs, SIMULATED and not market data' at L04.html:131. Not a BUILDER_RULES 6.7 failure (no synthetic data presented as real); noted as a labelling inconsistency, not a FAIL. c174 basis 'Lab 1, Part B (SIMULATED)' and c228 basis 'Lab 1, Part D (SIMULATED)' carry the label. Lab twins use no RNG and no network (L06 fixed-seed integer recurrence; lab-M7-L06-1.py). PASS." ),
    "b-r1-hours": ("Fresh because course/modules/M/M7/index.html changed (L08 card body text only, index.html hunk at line 150). Declared hours: L04, L05, L06 data-hours=\"10\" (line 2 of each page); index.html kickers L01 9, L02 9, L03 10, L04 10, L05 10, L06 10, L07 9, L08 10 h (index.html:143-150) sum to 77; data-hours-lessons=\"77\" (index.html:29); data-hours-project=\"33\"; 77 + 33 = 110 matches the eyebrow 'Tier F · 110 hours' (index.html:31). Hub prose at index.html:141 ('Eight lessons of nine or ten study hours ... totalling 77 hours. Lessons 1, 2, 7 declare 9 hours') matches. check_pages M7 PASS (%s/check_pages_M7.txt). PASS." % S),
    "b-r2-cards-round2-text": ("Fresh: the round-2 changed cards c114 and c174 are re-read against the current text (see rows b-r1-card-c114 and b-r1-cards-L06-except-c114). c174 still says 'Exactly one, at each of gamma = 1, 2, 4, 8 and 16 (the candidates_passing column of Part B)'; the twin prints candidates_passing 1 for each gamma; L06.html:150 predicts one passing candidate for each gamma. PASS."),
    "b-r2-delta-hunks": ("Fresh delta read for slice b, git diff 9294b914..95f3f8cb over the slice paths. Pages L04.html, L05.html, L06.html and twins lab-M7-L04-1.py, lab-M7-L05-1.py, lab-M7-L06-1.py: no hunks (git diff --quiet). cards.json: 13 changed objects (c004, c018, c041, c050, c058, c103, c114, c123, c124, c136, c142, c150, c174) and 4 added (c226-c229); slice-b hunks are c058, c103, c114, c174 (changed) and c228 (added), read in full (%s/cards_delta_by_id.out and git diff output). The rest are L01-L03, L07, L08 and are outside this slice. index.html: one hunk, the L08 card body (line 150), no L04-L06 change. Scope out of slice b: notation, references, tools, course/assets/data: no diff. PASS." % S),
    "b-r2-scripts-provenance": ("Ledger hygiene for this round: scripts and outputs are in %s/ (check_pages, check_dag, check_projects, run_labs, page_smoke, ruff, mypy, pytest, verify_refs, twin runs and outputs, l04_cards_check.py, cards_numbers_check.py, cards_dup_scan.py, cards_grade_basis_check.py, cards_delta_by_id.out, build_fragment.py). The round-2 scripts under ledgers/M7/scripts/M7-b-r2/ are cited only for carried evidence." % S),
}

NEW = [
    {
        "id": "b-r1-card-c228",
        "check": "2.7 new retrieval card M7-c228 (L06, grade C): number and claim against the lesson and the printed lines",
        "location": "course/modules/M/M7/cards.json (id M7-c228); course/modules/M/M7/L06.html:514-516 (E3); tests/labs/M7/lab-M7-L06-1.py Part B table and Part D lines",
        "status": "PASS",
        "evidence": "Card: turnover at gamma 4 from the six-place weights printed in Part B gives 0.558860, differs from the exact value 0.558861 in the sixth place; the lab reports the exact-fraction value. Printed weights at gamma 4 (twin_L06.out, nonneg row): 0.389219, 0.220570, 0.390211, 0.000000. Recomputed: sum |w_i - 1/4| = 0.558860 (%s/c228_check.py, c228_check.out); L06.html:516 states 'sum to 0.558860'. Exact fraction value 0.5588607333 (twin_L06.out turnover_exact_at_gamma 4) rounds to 0.558861 (turnover_at_gamma 4). Basis 'Lab 1, Part D (SIMULATED), computed from the printed six-place weights' is correct. Grade C is consistent with a number from the lab's printed output. PASS." % S,
    },
]

fresh_ids = set(FRESH)
rows = []
order = [r["id"] for r in base_frag["rows"]]
for rid in order:
    b = base[rid]
    if rid in CARRY:
        rows.append({"id": rid, "check": b["check"], "location": b["location"], "status": "PASS",
                     "evidence": PFX % CARRY[rid] + b["evidence"]})
    elif rid in FRESH:
        rows.append({"id": rid, "check": b["check"], "location": b["location"], "status": "PASS", "evidence": FRESH[rid]})
    else:
        raise SystemExit("unclassified base row " + rid)
for n in NEW:
    rows.append(n)
assert len(rows) == 37, len(rows)
assert len({r["id"] for r in rows}) == len(rows)

now = datetime.datetime.now().astimezone().isoformat(timespec="seconds")
frag = {
    "unit": "M7",
    "slice": "b",
    "round": 1,
    "verifier": "independent verifier (Haiku 5.5), M7-b round 1 (closing delta: rulings 30, 37; ruling 26 FAIL kinds only; no new mutants). Did not build M7 and shares no context with the builders.",
    "pin": "95f3f8cb",
    "base": "9294b914 (round-2 pin; base fragment ~/.fanout/frags/S-M7-b.round2.json, verdict PASS, 36 rows). Delta over slice b: course/modules/M/M7/cards.json (c058, c103, c114, c174 changed; c228 added; other hunks are outside slice b) and course/modules/M/M7/index.html (L08 card body only). L04.html, L05.html, L06.html and the three lab twins are byte-identical to 9294b914. The instruction's 'round 1' label is kept for this file as instructed; the carry prefix names the base's round 2.",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyF21-M7-b",
    "scratch": "none used; all outputs in ledgers/M7/scripts/M7-b-r1/",
    "verified_at": now,
    "verdict": "PASS",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Scope of slice b: L04.html, L05.html, L06.html, tests/labs/M7/lab-M7-L04-1.py, lab-M7-L05-1.py, lab-M7-L06-1.py, and the 83 L04-L06 cards in course/modules/M/M7/cards.json. The project grader, L01-L03, L07, L08 and the hub are other slices. The hub index.html was read only for the hours row (its delta is one L08 line).",
        "Mutation testing: not applicable. No grader is in this slice; VERIFIER_RULES ruling: lab twins are demonstrations. mutants is empty.",
        "Commands run on 95f3f8cb (outputs in ledgers/M7/scripts/M7-b-r1/): check_pages --unit M7 (and --page L04, L05, L06); check_dag --unit M7 and --all; check_projects --unit M7; run_labs --unit M7; page_smoke --unit M7 --pages L04 L05 L06; ruff check and ruff format --check on the three twins; mypy --no-incremental --strict on the three twins; pytest tests/test_labs.py -k M7 (11 passed); verify_refs --offline (560 entries, 0 problems). Twins run under python -I -W error (exit 0, empty stderr). Card scripts: l04_cards_check.py, cards_numbers_check.py, cards_dup_scan.py, cards_grade_basis_check.py, cards_delta_by_id.out.",
        "Carried rows (round-2 PASS, subject byte-identical to 9294b914): b-r1-L04-math, L04-lab-claims, L04-grades-scope, L05-math, L05-lab-claims, L05-grades-scope, L06-math, L06-lab-claims, L06-grades-scope, L06-E2-E3-unrounded, cards-L05, stray-CU, notation, citations, process-words-banned, prose-numbers-printed, hypotheses-proofs, quiz-keys, b-r2-slater-converse-xref, b-r2-efficient-set-definition, b-r2-L05-part-b-candidates. Fresh rows: the gate rows, every row whose subject changed (cards.json, index.html), the delta row, the scripts row, and the new row b-r1-card-c228.",
        "Pre-existing fragment: ledgers/M7/M7-b.json at HEAD in this checkout was an older round-8 fragment (pin ce7b382). It is replaced here as the task instructs; it remains in git history at 95f3f8cb.",
        "Observation, not a FAIL: cards c204 and c213 (L04 lab results, grade C) name Lab 1 without the '(SIMULATED)' tag in their basis; L04.html:131 carries the visible SIMULATED label for the lab inputs. Noted under b-r1-simulated-labels.",
        "Observation, not a FAIL: the twins contain no test functions, so pytest --collect-only reports no tests (exit 5). The round-2 note 'collect-only (3)' is read here as three files, not a test count; no lab page states a test count.",
        "Could not check: (1) Pyodide in-browser timings beyond page_smoke's 0.1 s resolution; (2) the Pyodide version pin; (3) full repository gate (targeted commands only, per the testing rules); (4) the hub, L01-L03, L07, L08 and the project grader, which are other slices; (5) byte-level re-verification of the 28 unchanged L06 card texts against the lesson beyond the carry-by-object basis, which is stated as carried.",
    ],
    "summary": "Slice b (L04-L06 pages, twins, 83 cards), closing delta on 95f3f8cb against 9294b914: 37 rows, 37 PASS, 0 FAIL, 0 UNVERIFIABLE. Changed subjects re-verified: c058, c103, c114, c174, new c228, index.html hours line. All gates re-run and green on 95f3f8cb.",
}

out = "ledgers/M7/M7-b.json"
with open(out, "w", encoding="utf-8") as fh:
    json.dump(frag, fh, ensure_ascii=False, indent=1)
    fh.write("\n")
print("wrote", out, "rows", len(rows), "verdict", frag["verdict"])
