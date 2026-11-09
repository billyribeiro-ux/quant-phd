import json, re, sys

BASE = "/Users/billyribeiro/.fanout/frags/S-CS2-a.round7.json"
OUT = "/Users/billyribeiro/.fanout/wt/verifyF11-CS2-a/ledgers/CS2/CS2-a.json"
base = json.load(open(BASE, encoding="utf-8"))
D = "ledgers/CS2/scripts/CS2-a-r1/"

CARRY = ("Carried from round 7 (course/modules/CS/CS2/index.html, L01.html..L04.html, tests/labs/CS2/lab-CS2-L01..L04-1.py, "
         "notation/notation.json, curriculum/, tools/, tests/test_labs.py, tests/test_run_labs.py, tests/test_docs_figures.py "
         "byte-identical between the previous pin aa659725 and pin 95f3f8cb; git diff --quiet, output in " + D + "carry_identity_r1.txt): ")
CARRY_CARDS = ("Carried from round 7 (per-record identity of the cited cards between aa659725 and 95f3f8cb: "
               "cards_delta_r1.txt 'L01-L04 changed []' and 'L01-L04 records in head 76'): ")

# rows re-verified from scratch in this round (subject changed or tool gate re-run)
REVERIFY = {}
REVERIFY["SA-DELTA-READ"] = (
    "Round 1 delta read in full: `git diff --name-only aa659725..95f3f8cb` over slice-a paths (course/modules/CS/CS2/index.html, "
    "L01-L04.html, tests/labs/CS2/lab-CS2-L01..L04-1.py, cards.json, notation, curriculum) lists only "
    "course/modules/CS/CS2/cards.json. Its four hunks (ledgers/CS2/scripts/CS2-a-r1/cards_delta_r1.txt 'changed'): "
    "CS2-c200 (L11, back: hypotheses added), CS2-c231 (L10, front and back), CS2-c244 (L09, back: mechanism hedged), "
    "CS2-c245 (L11, back: hypotheses added). All four are outside the slice-a card scope (L01-L04), so no slice-a card "
    "row's subject changed; they are read here for the scan rows only and not content-verified (base notes assign L05-L11 "
    "to other slices). No change to index.html, L01-L04, twins, notation or curriculum (carry_identity_r1.txt). Outside "
    "the slice, plans/FINAL-ARCHITECT-RULINGS.md gains ruling 37 only; tools/ and tests/ are unchanged.")
REVERIFY["SA-CARDS-DUP"] = (
    "Re-verified in round 1: cards_delta_r1.py on course/modules/CS/CS2/cards.json at 95f3f8cb: 198 records, ids unique, "
    "no duplicate fronts and no duplicate backs (case and space normalised), output in cards_delta_r1.txt. "
    "Observation (not a row, pre-existing, same ids at aa659725): ids have gaps (e.g. c241 removed in round 7) and are not "
    "in file order.")
REVERIFY["SA-CARDS-GRADE"] = (
    "Re-verified in round 1: cards_delta_r1.py over all 198 records at 95f3f8cb: grades T 159, C 39; no grade outside "
    "{T,A,B,C,D,X}; every non-T card has a basis (39 of 39); no T card carries a basis; lessons L01-L11 only; keys limited to "
    "id, lesson, front, back, grade, basis, cite; violations []. Output cards_delta_r1.txt.")
REVERIFY["SA-TOOL-CHECKPAGES"] = "Re-run in round 1: tools/check_pages.py --unit CS2: 'check_pages CS2: PASS', exit 0 (" + D + "check_pages_CS2.txt)."
REVERIFY["SA-TOOL-DAG"] = "Re-run in round 1: tools/check_dag.py --unit CS2: 'check_dag CS2: PASS', exit 0 (" + D + "check_dag_CS2.txt)."
REVERIFY["SA-TOOL-RUNLABS"] = "Re-run in round 1: tools/run_labs.py --unit CS2: 'run_labs CS2: PASS (14/14)', exit 0 (" + D + "run_labs_CS2.txt)."
REVERIFY["SA-TOOL-PAGESMOKE"] = ("Re-run alone in round 1: tools/page_smoke.py --unit CS2 --pages index L01 L02 L03 L04: "
                                 "PASS for index, L01, L02, L03, L04; 'page_smoke CS2: PASS', exit 0 (" + D + "page_smoke_CS2_hub_L01-L04.txt).")
REVERIFY["SA-TOOL-LINT"] = ("Re-run in round 1: ruff check on the four twins: 'All checks passed!'; ruff format --check: "
                            "'4 files already formatted'; mypy --no-incremental on the four twins: 'Success: no issues found in "
                            "4 source files', exit 0 (" + D + "ruff_twins.txt, " + D + "mypy_twins.txt).")
REVERIFY["SA-TOOL-PYTEST"] = ("Re-run in round 1: pytest tests/test_labs.py -k CS2: 14 passed, exit 0 (" + D + "pytest_labs_CS2.txt); "
                              "pytest tests/test_run_labs.py tests/test_docs_figures.py: 20 passed, exit 0 (" + D + "pytest_run_labs_docs.txt).")
REVERIFY["SA-TOOL-REFS"] = "Re-run in round 1: tools/verify_refs.py --offline: 'offline integrity: 560 entries, 0 problems', exit 0 (" + D + "verify_refs_offline.txt)."
REVERIFY["SA-TOOL-PROJECTS"] = "Re-run in round 1: tools/check_projects.py --unit CS2: 'check_projects CS2: PASS', exit 0 (" + D + "check_projects_CS2.txt)."
REVERIFY["SA-TOOL-GRADERS"] = "Re-run in round 1: tools/run_graders.py --unit CS2 --seeds 0-49: 'run_graders CS2: PASS (reference 50/50 seeds)', exit 0 (" + D + "run_graders_CS2_0-49.txt)."
REVERIFY["SA-PY314-TWINS"] = ("Re-run in round 1: each twin run as .venv/bin/python -I -W error (CPython 3.14.8): exit 0 for L01-L04 with "
                              "0 stderr bytes (" + D + "twin_L01..L04.err). Python 3.15 not re-run in this round.")
REVERIFY["SA-LAB-SEEDED"] = ("Re-run in round 1: page_smoke CS2 PASS for L01-L04 (" + D + "page_smoke_CS2_hub_L01-L04.txt; L04 lab 0.7 s); "
                             "twin seeds unchanged (twins byte-identical, carry_identity_r1.txt).")

CARDS_ROWS = {"SA-CARDS-L01", "SA-CARDS-L02", "SA-CARDS-L03", "SA-CARDS-L04", "SA-CARDS-HYP"}
rows = []
for r in base["rows"]:
    rid = r["id"]
    if rid in REVERIFY:
        ev = REVERIFY[rid]
    else:
        prev = re.sub(r"^Carried from round \d+ \([^)]*\):\s*", "", r["evidence"]).strip()
        prev = re.sub(r"^Re-verified in round 7:\s*", "", prev)
        prefix = CARRY_CARDS if rid in CARDS_ROWS else CARRY
        ev = prefix + "prior evidence (round 7): " + prev
    rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": "PASS", "evidence": ev})

assert len(rows) == 62 and all(x["status"] == "PASS" for x in rows)
frag = {
    "unit": "CS2",
    "slice": "a",
    "round": 1,
    "round_note": ("Closing delta verification (ruling 30) of CS2 slice a, pinned at 95f3f8cb. Base: the round-7 fragment "
                   "pinned at aa659725 (/Users/billyribeiro/.fanout/frags/S-CS2-a.round7.json, 62 rows, all PASS). Delta "
                   "aa659725..95f3f8cb over slice-a paths: only course/modules/CS/CS2/cards.json changed, four records "
                   "(CS2-c200, c231, c244, c245), all outside L01-L04. Pages, twins, notation and curriculum are byte-identical. "
                   "Rows whose subject changed (SA-CARDS-DUP, SA-CARDS-GRADE, SA-DELTA-READ) and all tool gates were re-run; "
                   "the other rows are carried under the carry prefix. Slice a has no grader, no project, no mutants."),
    "verifier": "independent closing-delta verifier (Haiku 5.5), fresh context; did not build CS2 slice a",
    "pin": "95f3f8cb21c2cd9fc904430bd30a6b734d01f672",
    "base": "aa6597255304919b9c4e5e5ca07763ae3e13d45c",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyF11-CS2-a (detached at 95f3f8cb, .venv symlinked)",
    "scratch": "/Users/billyribeiro/.fanout/wt/verifyF11-CS2-a/ledgers/CS2/scripts/CS2-a-r1",
    "verified_at": "2026-11-09",
    "verdict": "PASS" if all(x["status"] == "PASS" for x in rows) else "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Out of slice a (not verified here): the content of CS2-c200 (L11), c231 (L10), c244 (L09) and c245 (L11), changed "
        "in this delta. Their scan-level checks (grade, basis, duplicates) are in SA-CARDS-GRADE and SA-CARDS-DUP and pass. "
        "The base notes assign L05-L11 cards and pages to other slices.",
        "Observation, not a row (pre-existing, same ids at aa659725): card ids have gaps (67, 77, 79, ..., 241) and the file is not "
        "in id order. No rule in BUILDER_RULES section 7 is stated for gaps; ids are unique.",
        "Observation (carried from the base, LOW, non-blocking): title casing differs between the hub card and the lesson. "
        "index.html:148 and the L03 next link say 'Comparison Sorting and Binary Search'; L04.html h1 and <title> say "
        "'Comparison sorting and binary search'.",
        "Judgment carried from the base (SA-L04-R3-SCOPE, PASS): R3 hypothesis (2) at L04.html:549 covers the whole algorithm; "
        "a non-blocking wording fix is to restrict it to absent-key runs.",
        "Not run: Python 3.15 twin run (only 3.14.8 available in the venv); full-repo gates (outside slice a; the rule is a "
        "targeted run for a closing delta with no dependency change).",
        "ledgers/CS2/scripts/CS2-a-r1/ already contained tracked files from an earlier commit (cards_scan.py, check_twins.py, "
        "cmp_labs.py, indep.py, independent_numbers.py, write_fragment.py); they were not used or modified here.",
        "Blind calibration (ruling 23): not applicable; CS2 slice a has no rubric exemplars.",
    ],
    "summary": {"rows": len(rows), "pass": len(rows), "fail": 0, "unverifiable": 0, "mutants": 0, "mutants_killed": 0},
}
json.dump(frag, open(OUT, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
open(OUT, "a", encoding="utf-8").write("\n")
print("wrote", OUT, len(rows), frag["verdict"])
