import json, sys
from pathlib import Path

base = json.load(open(sys.argv[1], encoding="utf-8"))
out_path = Path(sys.argv[2])
CARRY = ("Carried from round 5 (course/modules/M/M7/L07.html, L08.html, index.html, tests/labs/M7/*.py, "
         "notation/, tools/, references/, curriculum/, course/concepts.html, course/assets/data, "
         "plans/M7-build-plan.md, and the 42 L07/L08 card objects of cards.json are byte-identical or "
         "object-identical since dde0486b, see M7-c-r1/cards_delta_summary.txt):")

FRESH = {
 "M7c-r1-cmd-check_pages": "Fresh at 95f3f8cb: `.venv/bin/python tools/check_pages.py --unit M7` -> 'check_pages M7: PASS', exit 0 (ledgers/M7/scripts/M7-c-r1/check_pages.txt). Re-run because cards.json changed in the delta.",
 "M7c-r1-cmd-check_dag": "Fresh at 95f3f8cb: `tools/check_dag.py --unit M7` -> 'check_dag M7: PASS', exit 0 (ledgers/M7/scripts/M7-c-r1/check_dag.txt).",
 "M7c-r1-cmd-run_labs-L07": "Fresh at 95f3f8cb: `tools/run_labs.py --unit M7 --page L07` -> 'run_labs M7: PASS (1/1)', exit 0 (ledgers/M7/scripts/M7-c-r1/run_labs_L07.txt).",
 "M7c-r1-cmd-run_labs-L08": "Fresh at 95f3f8cb: `tools/run_labs.py --unit M7 --page L08` -> 'run_labs M7: PASS (1/1)', exit 0 (ledgers/M7/scripts/M7-c-r1/run_labs_L08.txt).",
 "M7c-r1-twins-alone-python-I-W-error": "Fresh at 95f3f8cb: `python -I -W error tests/labs/M7/lab-M7-L07-1.py` and `...lab-M7-L08-1.py` each exit 0 with empty stderr (ledgers/M7/scripts/M7-c-r1/twin_L07.out, twin_L08.out, twin_L0*.err of 0 bytes). Printed output: Part A-C of each twin, recursion_matches_brute_force True, optimal_plan_every_tail_optimal True (L07), recursion_matches_brute_force True, iterate_equals_n_period_recursion True (L08).",
 "M7c-r1-cmd-ruff": "Fresh at 95f3f8cb: `ruff check tests/labs/M7` -> 'All checks passed!'; `ruff format --check tests/labs/M7` -> '11 files already formatted'; repo `ruff check .` -> 'All checks passed!'; `ruff format --check .` -> '555 files already formatted'; all exit 0 (ledgers/M7/scripts/M7-c-r1/ruff_*.txt).",
 "M7c-r1-cmd-mypy-strict": "Fresh at 95f3f8cb: `mypy --strict tests/labs/M7/lab-M7-L07-1.py tests/labs/M7/lab-M7-L08-1.py` -> 'Success: no issues found in 2 source files', exit 0; repo `mypy --no-incremental` -> 'Success: no issues found in 386 source files', exit 0 (ledgers/M7/scripts/M7-c-r1/mypy_twins.txt, mypy_repo.txt).",
 "M7c-r1-cmd-pytest-lab-cases": "Fresh at 95f3f8cb: `pytest tests/test_labs.py -k M7 -q` -> 11 collected, 11 passed, exit 0 (ledgers/M7/scripts/M7-c-r1/pytest_labs_M7.txt).",
 "M7c-r1-cmd-page_smoke": "Fresh at 95f3f8cb, each page alone: `tools/page_smoke.py --unit M7 --pages L07` -> 'page_smoke modules/M/M7/L07.html: PASS', 'page_smoke M7: PASS', exit 0; same for L08 (ledgers/M7/scripts/M7-c-r1/page_smoke_L07.txt, page_smoke_L08.txt).",
 "M7c-r1-cmd-verify_refs-offline": "Fresh at 95f3f8cb: `tools/verify_refs.py --offline` -> 'offline integrity: 560 entries, 0 problems', exit 0 (ledgers/M7/scripts/M7-c-r1/verify_refs_offline.txt). references/ is byte-identical since dde0486b.",
 "M7c-r2-cmd-check_projects": "Fresh at 95f3f8cb: `tools/check_projects.py --unit M7` -> 'check_projects M7: PASS', exit 0 (ledgers/M7/scripts/M7-c-r1/check_projects.txt). Re-run because project.html changed in the delta; the project is outside this slice.",
 "M7c-r3-cmd-build_site-check": "Fresh at 95f3f8cb: `tools/build_site.py --check` -> 'site data current: 6 outputs', exit 0 (ledgers/M7/scripts/M7-c-r1/build_site_check.txt).",
 "M7c-r3-cmd-pytest-docs-refs": "Fresh at 95f3f8cb: `pytest tests/test_docs_figures.py tests/test_refs.py -v` -> '133 passed in 1.03s' (ledgers/M7/scripts/M7-c-r1/pytest_docs_refs.txt).",
 "M7c-r1-cards-duplicates-and-numbers": "Fresh at 95f3f8cb (cards.json changed): 203 cards (was 201); no duplicate id, front or back (python scan, ledgers/M7/scripts/M7-c-r1/cards_delta.py output); lesson counts L01 24, L02 25, L03 29, L04 22, L05 28, L06 33, L07 20, L08 22; L07/L08 still 42 cards. Every number of length >1 in every card back appears in its own lesson HTML (ledgers/M7/scripts/M7-c-r1/card_numbers.py -> 'none' for all eight lessons). The two added cards M7-c228 (L06) and M7-c229 (L03) are not L07/L08 cards.",
 "M7c-r2-delta-cards": "Fresh delta read at 95f3f8cb (`git diff dde0486b..HEAD -- course/modules/M/M7/cards.json`, 30 lines): hunks change M7-c004 (L01), c018 (L02), c050 (L03), c058 (L04), c103 and c114 (L06), and add M7-c228 (L06) and c229 (L03). No hunk touches a card of lesson L07 or L08. Object comparison (ledgers/M7/scripts/M7-c-r1/cards_delta_summary.txt): changed in L07/L08 = []; added in L07/L08 = []; the 42 L07/L08 cards are identical to dde0486b.",
}

NEW_ROWS = [{
 "id": "M7c-r1-delta-slice-paths",
 "check": "delta dde0486b..95f3f8cb over the slice paths: lessons, twins, hub, cards, plus shared inputs",
 "location": "course/modules/M/M7/L07.html, L08.html, index.html, tests/labs/M7, notation/, tools/, references/, curriculum/, course/concepts.html, course/assets, plans/M7-build-plan.md",
 "status": "PASS",
 "evidence": "`git diff --quiet dde0486b..95f3f8cb` over L07.html, L08.html, index.html and tests/labs/M7 exits 0 (byte-identical), and over notation/, references/, curriculum/, tools/, course/assets/, course/concepts.html, course/index.html and plans/M7-build-plan.md also exits 0. The M7 paths that changed in the delta are cards.json, grader/reference.py, grader/test_project.py and project.html only (`git diff --name-only dde0486b..HEAD -- course/modules/M/M7`). Changed plans/ files are FINAL-ARCHITECT-RULINGS.md, KNOWN-ISSUES.md, M5-build-plan.md and M5-open-items.md, none of which is an M7 slice input (rulings 30 and 37 read in full).",
}]

rows = []
seen = set()
for r in base["rows"]:
    rid = r["id"]
    seen.add(rid)
    if rid in FRESH:
        rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": "PASS", "evidence": FRESH[rid]})
    else:
        rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": r["status"],
                     "evidence": CARRY + " " + r["evidence"]})
assert set(FRESH) <= seen, set(FRESH) - seen
rows.extend(NEW_ROWS)

fresh_n = sum(1 for r in rows if r["id"] in FRESH or r["id"] in {n["id"] for n in NEW_ROWS})
carried_n = len(rows) - fresh_n
frag = {
 "unit": "M7",
 "slice": "c",
 "round": 1,
 "verifier": "independent verifier (Haiku), unit M7 slice c, round 1 (closing delta verification per ruling 30 from round-5 fragment pin dde0486b)",
 "pin": "95f3f8cb21c2cd9fc904430bd30a6b734d01f672",
 "base": "round-5 fragment /Users/billyribeiro/.fanout/frags/S-M7-c.round5.json (pin dde0486b, verdict PASS, 57 rows). Delta dde0486b..95f3f8cb for this slice: cards.json only (hunks on L01-L06 cards and new M7-c228, c229; no L07/L08 card changed). L07.html, L08.html, index.html and tests/labs/M7 byte-identical.",
 "checkout": "/Users/billyribeiro/.fanout/wt/verifyF21-M7-c",
 "scratch": "ledgers/M7/scripts/M7-c-r1/",
 "verified_at": "2026-11-09",
 "verdict": "PASS" if all(r["status"] == "PASS" for r in rows) else "FAIL",
 "rows": rows,
 "mutants": [],
 "registry_flags": [],
 "freshness_flags": [],
 "notes": [
  "Rulings applied: 30 (closing delta: re-verify listed rows and changed subjects, carry the rest, no hunting for new defects) and 37 (closing round writes no new mutants). Ruling 26 kinds: no FAIL row of any ruling-26 kind was found.",
  "Mutants: none. Slice c is lesson pages and cards with lab twins; VERIFIER_RULES 2.5 and the rulings file require mutation testing only for project graders. No M7 grader is in this slice.",
  "Out of slice, not verified here (owner slices must check): cards M7-c004 (L01), c018 (L02), c050 and new c229 (L03), c058 (L04), c103, c114 and new c228 (L06). Their hunks were read in full (cards_delta.py summary) but their text was not checked against lessons L01-L06.",
  "Observation carried from round 5: L08.html:115-117 uses raw \\mathcal{G} for the Bellman operator; no registered macro covers it and it collides with no registered symbol.",
  "The checkout's ledgers/M7/M7-c.json was overwritten with this fragment (protocol); nothing was committed or pushed.",
 ],
 "summary": f"M7 slice c, closing delta round 1 at pin 95f3f8cb: {len(rows)} rows, {len(rows)-carried_n} re-verified fresh (gates, cards duplicate and number scan, delta read), {carried_n} carried from round 5 with byte-identical or object-identical subjects. 0 non-PASS rows. Only cards.json changed inside the slice paths, and none of its changed or added cards belongs to L07 or L08. No mutants (ruling 37).",
}
out_path.write_text(json.dumps(frag, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("rows", len(rows), "fresh", fresh_n, "carried", carried_n, "verdict", frag["verdict"])
