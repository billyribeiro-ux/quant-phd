"""Verifier G1: builds ledgers/LX1/LX1-c.json (closing delta, LX1-c, round 1) from the base fragment F3-LX1-c.round1.json.
Rows whose cited subject changed in 95f3f8cb..2a805c83 or that were non-PASS are re-verified (FRESH); every other base
row is carried under the carry prefix. Usage: python -I verifier-G1-fragment.py <checkout> <base.json>."""
import json
import re
import sys
from pathlib import Path

root, base_path = Path(sys.argv[1]), Path(sys.argv[2])
base = json.loads(base_path.read_text(encoding="utf-8"))
S = "ledgers/LX1/scripts/LX1-c-r1/out/"

def covers_473(loc):
    for a, b in re.findall(r"(?<!\d)(\d{3})-(\d{3})(?!\d)", loc):
        if int(a) <= 473 <= int(b):
            return True
    return any(int(x) == 473 for x in re.findall(r"(?<!\d)(\d{3})(?!\d)", loc))

FRESH = {
    "proj-rubric-c1-level1-dominated": (
        "PASS",
        "Re-verified at 2a805c83. Line 473 (C1 row) read from the checkout by "
        f"{S}../verifier-G1-c1_levels.py and printed in {S}G1_c1_levels.out: the level-2 to level-4 cells now each require "
        "'says which is the episode and which the condition'; the level-1 cell is 'names only one ... or names two without "
        "saying which is which'. Enumerating all 2^8 fact vectors: 'vectors meeting level 1 and a level 2-4 cell: 0'; "
        "'vectors with more than one level met: 1' is the typed level-3/level-4 pair, resolved by the highest-level rule. "
        "The base FAIL (lenient reading, 144 overlaps) no longer applies because the labelling clause is written into "
        "levels 2 to 4. Observation only (not a ruling-26 kind): no level text covers an essay that names neither the "
        "episode nor the condition (64 vectors; see notes)."),
    "proj-rubric-c1-level1-event-term": (
        "PASS",
        "Re-verified at 2a805c83. project.html:473 td 4 reads 'Names only one of the episode and the condition, or names "
        "two without saying which is which.'; grep -c -i event on line 473 = 0. The terms 'episode' and 'condition' are "
        "defined by brief item 1 (:440) and the spec (:261-265), which precede the rubric (:467)."),
    "proj-rubric-c1-level3-unreachable": (
        "PASS",
        "Re-verified at 2a805c83 with the enumerator on line 473. Highest-level counts over 256 fact vectors: "
        "{1: 160, 2: 30, 3: 1, 4: 1}. Level 3 is the highest level met only when no locator is of a listed type "
        "(level 4 text lists page, table, section, title field, MANIFEST row; level 3 text has no type), so level 3 is "
        "reachable; the typed vector scores 4. Both td 1 and td 2 carry the new labelling clause."),
    "proj-rubric-observable": (
        "PASS",
        "Re-verified at 2a805c83. Every C1 descriptor in project.html:473 names an element a reader can find on the page: "
        "the two items, the dates, the locators (by listed type), and whether the essay says which item is the episode. "
        "No descriptor depends on an unstated judgement. Other cells (:474-477) unchanged."),
    "proj-student-error-coverage": (
        "PASS",
        "Re-verified at 2a805c83. The student error 'names both, without saying which is which' now falls in level 1 "
        "(project.html:473 td 4); 'a date or a locator missing' falls in level 2 (td 3); the level-3 and level-4 cells "
        "require the labelled, dated, located form. Student error 'names neither' is not caught by any level text (observation)."),
    "proj-calibration-exemplars": (
        "PASS",
        "Blind scores cited (ruling 23): ~/.fanout/blind/LX1-c.json (A [4,4,4,4,3], B [2,2,1,2,1]); its file time "
        "(2026-11-08 23:58) predates the C1 change (commit b9912454, 2026-11-09 04:51). Verifier check, not a blind score: "
        "the official C1 values stay correct under the labelled C1 cell. Exemplar A's C1 = 4 (project.html:491 'Episode one "
        "is ...' and 'The condition is ...'; :491 dates; locators title field and MANIFEST/Lab 3 window; annotation :495). "
        "Exemplar B's C1 = 2 (:564 'The episode is ...' and 'The condition is ...'; condition undated; annotation :568, "
        "C1 level 3 miss :571). Data-scores attributes unchanged (:485 '4,4,4,4,3', :547 '2,2,1,2,1'). A fresh blind C1 "
        "re-score is recommended but is not performed by this verifier (ruling 23)."),
    "proj-exemplar-b-annotations-vs-descriptors": (
        "PASS",
        "Re-verified at 2a805c83. B's C1 annotations (project.html:568 'Meets C1 level 2: names both ..., and a date is "
        "missing for the condition only'; :571 'Misses C1 level 3: the condition has no date') agree with the current cells. "
        "The annotations do not mention the new labelling clause, which B meets (:564); that omission is not a misstatement."),
    "proj-test-lab3-popsd-variant": (
        "PASS",
        "Base FAIL re-verified. At 95f3f8cb the test failed: out/pytest_lx1_lab3.out 'AssertionError: a population-sd variant "
        "must not pass the agreement check' and 'FAILED tests/test_lx1_project_lab3.py::test_a_population_sd_variant_of_the_two_pass_check_raises'. "
        f"At 2a805c83 (commit 9a85e9e8): {S}G1_pytest_lab3.out, 'pytest -q tests/test_lx1_project_lab3.py' rc=0, five dots "
        "(5 passed). The new test asserts that the printed 'sample sd' lines differ between the twin and a /n variant; the "
        "twin is byte-identical to 95f3f8cb (tests/labs/LX1 has no diff in the range)."),
    "proj-gate-commands": (
        "PASS",
        f"Re-run at 2a805c83 by ledgers/LX1/scripts/LX1-c-r1/verifier-G1-gates.sh; outputs {S}G1_*.out, all rc=0: "
        "check_projects PASS, check_pages PASS, check_dag PASS, run_labs unit 7/7, run_labs project 3/3, page_smoke project "
        "PASS, verify_refs --offline 560 entries 0 problems, ruff check and format clean, mypy --no-incremental 8 files "
        "clean, pytest lab-3 file 5 passed, pytest test_labs/test_run_labs/test_page_smoke/test_page_checks 0 failures."),
    "proj-run-labs-project": (
        "PASS",
        f"Re-run at 2a805c83: {S}G1_run_labs_project.out 'run_labs LX1: PASS (3/3)' rc=0; {S}G1_run_labs_unit.out 'PASS (7/7)'."),
    "proj-check-pages-project-scope": (
        "PASS", f"Re-run at 2a805c83: {S}G1_check_pages.out 'check_pages LX1: PASS' rc=0."),
    "proj-page-smoke": (
        "PASS", f"Re-run at 2a805c83: {S}G1_page_smoke_project.out 'page_smoke modules/LX/LX1/project.html: PASS' rc=0."),
    "proj-notation": (
        "PASS",
        f"TeX spans of project.html: 31 old and 31 new, identical sequence (out/G1_page_delta.out); the only changed line (473) "
        "has no TeX. notation/ and references/ unchanged in the range (git diff --stat empty), so the symbol check is "
        "unchanged."),
    "proj-links-anchors": (
        "PASS", f"href and id attributes identical old and new (out/G1_page_delta.out)."),
    "proj-scope-words": (
        "PASS",
        f"Line 473 scope words (out/G1_page_delta.out): 'only' (in 'Names only one', a count descriptor, not a universal claim) "
        "and 'each' (not a scope word in the ruling list); identical to the old line, so no scope word was added."),
    "proj-process-words": (
        "PASS",
        f"Line 473: zero process words. Whole page (learner prose, pre excluded): 'Round once, at print time' and "
        "'rounds an input' are rounding instructions, not process words (out/G1_page_delta.out)."),
    "proj-banned-phrases": (
        "PASS", f"Whole page learner prose: zero banned strings from BUILDER_RULES 1.3-1.4 (out/G1_page_delta.out)."),
    "proj-lab3-blank-gap-inputs": (
        "PASS",
        f"Re-run: {S}G1_survivor_tests.out. The repo blank scenario kills r17n01 and lx1c_r18n05; the gap scenario passes "
        "for every survivor (no survivor drops a month). Mutants r8n03 and r8n04 killed on the embedded snapshot "
        f"({S}G1_kill_all.out)."),
    "proj-lab3-raise-claims-untested": (
        "PASS",
        "Re-verified: the blank/non-decimal and gap tests pass against the twin at 2a805c83 (G1_pytest_lab3.out, 5 passed); "
        "the Check paragraph (project.html:308-309) is therefore run by the repo test file. The population-sd test no longer "
        "asserts a raise."),
    "proj-mutants-student-errors": (
        "PASS",
        f"Standing set re-run (ruling 37): {S}G1_kill_all.out, 'TOTAL mutants 94: killed on embedded snapshot 88, survived 6' "
        "(the six survivors are the base set; killed by synthetic inputs, see mutants list; lab mutants are demonstrations, "
        "ruling on labs). Mutants directory unchanged in the range."),
    "proj-r23-synthetic-survivors": (
        "PASS",
        "Carried from round 1 (twins and ledgers/LX1/mutants byte-identical since 95f3f8cb; the synthetic-input scripts read "
        "only the twin and the mutants): " + "out/synth_kill_r1.out (r17n01, r18n03, r18n04, r18n05, r20n04 SURVIVED on tiny_move), "
        "out/diff_printed_search_r1.out (r18n02 differs from the twin at f=0.50), out/flat_1e10_r1.out (r20n04 zero-change count "
        "667 vs 668). Base evidence in the base fragment."),
    "proj-closing-delta-hunks": (
        "PASS",
        "New row for 95f3f8cb..2a805c83 (slice paths). git diff --stat over course/modules/LX/LX1, tests/labs/LX1, "
        "tests/test_lx1_project_lab3.py, ledgers/LX1/mutants: project.html 1 line (473, re-verified above); "
        "tests/test_lx1_project_lab3.py 18 lines (population-sd test, re-verified above); tests/labs/LX1 and ledgers/LX1/mutants "
        "no change (git diff --name-status empty for mutants)."),
    "proj-closing-delta-cards": (
        "PASS",
        "New row for the cards.json delta (course/modules/LX/LX1/cards.json: fronts/backs of LX1-c001, c006, c021, c022, c092 "
        "changed, c094 added). No row of the project slice cites a card id or cards.json: grep -n 'LX1-c' course/modules/LX/LX1/project.html "
        "returns nothing. Card content is lesson-slice scope and is not verified here (note)."),
    "proj-closing-delta-lessons": (
        "PASS",
        "New row for lesson pages cited by the project. Changed lines (git diff -U0 95f3f8cb..2a805c83): L01.html 67, 334, 342, "
        "348, 353, 356; L02.html 60, 131, 300. Project citations checked against them: L01 Definition 1.2 (block :64-67, the defining "
        "sentence unchanged; the trailing sentence changed) and Definition 2.1 (:104, unchanged); L02 Proposition 2.1 (:87-97), "
        "(A2) :89, (A3) :90, def-debt-deflation (:110), Remark 3.3 (:127-129): all unchanged. The project's references to Lesson 1 "
        "and Lesson 2 cite these definitions by name, so the changed wording does not alter what the page cites."),
    "proj-dag-concepts": (
        "PASS", f"Re-run at 2a805c83: {S}G1_check_dag.out 'check_dag LX1: PASS' rc=0; the concept links at project.html:170 and :474 are carried."),
}
mutant_lines = (root / S / "G1_kill_all.out").read_text(encoding="utf-8").splitlines()
killed_by_status = {}
for line in mutant_lines:
    m = re.match(r"^lab(\d) (\S+): rc=\d+ stdout==expected (\w+) -> (KILLED|SURVIVED)", line)
    if m:
        killed_by_status[m.group(2)] = m.group(4)
SYNTH = {
    "r17n01_lab3_blank_gbp_cell_read_as_zero.py": "repo test blank scenario (survivor_tests G1 output) and synth_kill_r1.out blank_cell",
    "lx1c_r18n05_lab3_blank_cell_carried_forward_as_flat_rate.py": "repo test blank scenario (survivor_tests G1 output) and synth_kill_r1.out blank_cell",
    "lx1c_r18n03_lab3_zero_change_tested_after_rounding_to_four_places.py": "synth_kill_r1.out tiny_move (carried from round 23)",
    "lx1c_r18n04_lab3_window_two_centred_on_window_one_mean.py": "synth_kill_r1.out drift (carried from round 23)",
    "lx1c_r18n02_lab3_difference_of_printed_sds.py": "out/diff_printed_search_r1.out f=0.50 (carried from round 23)",
    "lx1c_r20n04_lab3_zero_test_with_tolerance.py": "out/flat_1e10_r1.out zero-change count 667 vs 668 (carried from round 23)",
}
mutants = []
for f in sorted((root / "ledgers/LX1/mutants").glob("*.py")):
    st = killed_by_status.get(f.name)
    if st is None:
        raise SystemExit(f"mutant {f.name} missing from G1_kill_all.out")
    if st == "KILLED":
        killed = f"embedded expected block, {S}G1_kill_all.out (KILLED)"
    else:
        killed = "synthetic input, " + SYNTH[f.name]
    desc = f.stem.replace("_", " ")
    mutants.append({"id": f.name, "description": "Standing mutant " + desc + " (ledgers/LX1/mutants)", "killed_by": killed})

rows = []
carried = 0
for r in base["rows"]:
    rid = r["id"]
    if rid in FRESH:
        status, ev = FRESH[rid]
        rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": status, "evidence": ev})
        continue
    if r["status"] != "PASS":
        raise SystemExit(f"non-PASS base row {rid} not re-verified")
    historical = r["location"].startswith("git ")
    if "project.html" in r["location"] and not historical and covers_473(r["location"]):
        raise SystemExit(f"carried row {rid} cites a changed or covering line: {r['location']}")
    if "test_lx1_project_lab3" in r["location"] and not historical:
        raise SystemExit(f"carried row {rid} cites the changed test file")
    carried += 1
    prefix = ("Carried from round 1 (course/modules/LX/LX1/project.html changed only at line 473 since pin 95f3f8cb, "
              "git diff -U0 95f3f8cb..2a805c83; tests/labs/LX1 byte-identical; cited lines unchanged"
              + ("; the cited git range is a historical diff, byte-identical" if historical else "") + "): ")
    rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": "PASS",
                 "evidence": prefix + r["evidence"]})

for rid in ("proj-closing-delta-hunks", "proj-closing-delta-cards", "proj-closing-delta-lessons"):
    status, ev = FRESH[rid]
    rows.append({"id": rid, "check": "closing delta (ruling 30): every hunk of the slice paths in 95f3f8cb..2a805c83",
                 "location": "git diff --stat 95f3f8cb..2a805c83 (slice paths)", "status": status, "evidence": ev})
ids_base = [r["id"] for r in base["rows"]]
ids_new = [r["id"] for r in rows]
assert ids_base == [i for i in ids_new if i in ids_base], "row ids and order must match the base"
assert len(set(ids_new)) == len(ids_new), "duplicate row ids"
new_ids = [i for i in ids_new if i not in ids_base]
assert set(FRESH) - set(ids_base) == set(new_ids), (set(FRESH) - set(ids_base), new_ids)

notes = [
    "Round 1 closing delta (ruling 30) for LX1-c. Base: F3-LX1-c.round1.json at pin 95f3f8cb (verdict FAIL, 81 rows: 79 PASS, 2 FAIL). "
    "Pin now 2a805c83 (descendant of 95f3f8cb: git merge-base --is-ancestor holds). Range changes in the slice: project.html line 473 (C1 cell), "
    "tests/test_lx1_project_lab3.py (population-sd test, 9a85e9e8), cards.json, L01.html and L02.html (lesson wording; project citations unchanged).",
    "Both base FAILs are re-verified and PASS at 2a805c83: proj-rubric-c1-level1-dominated (labelling clause now in levels 2-4, enumerator shows no level-1 overlap) and "
    "proj-test-lab3-popsd-variant (pytest 5 passed; base failed 1 of 5 at 95f3f8cb). Ruling 26 kinds: no failing gate, no false claim, no surviving non-equivalent grader mutant at this pin.",
    "Observation (not a ruling-26 kind, not a FAIL): the C1 cell gives no level for an essay naming neither the episode nor the condition (64 of 256 fact vectors). "
    "Observation: the exemplar annotations do not mention the new labelling clause; the official C1 scores are unchanged by it.",
    "Calibration (ruling 23): the blind file ~/.fanout/blind/LX1-c.json predates the C1 change. It is cited; the C1 levels of both exemplars were re-derived by the verifier from the labels in the text, "
    "not blind. A fresh blind C1 re-score is recommended.",
    "Ruling 37: no new mutants written. The standing set (94) was re-run (G1_kill_all.out: 88 killed on the embedded snapshot, 6 survivors killed on synthetic inputs as in the base). "
    "Survivor-kill scenarios of the repo test file re-run (G1_survivor_tests.out).",
    "Scratch directory note: ledgers/LX1/scripts/LX1-c-r1/ already held the base round-1 scratch; this verifier's files are named verifier-G1-* and out/G1_* so nothing was overwritten.",
    "Registry flag carried (references/references.json unchanged in the range): friedman1963monetary lists Friedman only; pages cite the key. Architect request, not a page defect.",
    "Not checked: the full repository gate (slice-only, ruling 30); a browser run of the page in Pyodide; alternatives for the labs (LX1 has no grader; the five alternatives of round 20 were not re-run); "
    "mutate_graders (no LX1 grader); card content of the changed cards (lesson-slice scope); a fresh blind scoring of the exemplars.",
]
fragment = {
    "unit": "LX1",
    "slice": "LX1-c",
    "round": 1,
    "verifier": "Claude Haiku 5.5 (claude-haiku-5-5), independent verifier G1 for LX1-c, round 1 (closing delta; did not build LX1)",
    "pin": "2a805c831410ab77c38c227f7e121e8537193ce9",
    "base": "95f3f8cb21c2cd9fc904430bd30a6b734d01f672 (fragment ~/.fanout/frags/F3-LX1-c.round1.json, round 1, verdict FAIL)",
    "checkout": str(root),
    "scratch": "ledgers/LX1/scripts/LX1-c-r1/ (verifier-G1-*.py/.sh and out/G1_*.out); temporary scratch /tmp/lx1c-g1-*",
    "verified_at": "2026-11-09T17:20:00+00:00",
    "verdict": "PASS" if all(r["status"] == "PASS" for r in rows) else "FAIL",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": base["registry_flags"],
    "freshness_flags": [],
    "notes": notes,
    "summary": (f"Closing delta round 1 for LX1-c at 2a805c83. Rows: {len(rows)} ({len(FRESH)} re-verified fresh, {carried} carried from round 1, "
                f"0 FAIL). Mutants: {len(mutants)} (standing set re-run: 88 killed on the embedded snapshot, 6 killed on synthetic inputs). "
                "Both base FAIL rows re-verified PASS."),
}
out = root / "ledgers/LX1/LX1-c.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(fragment, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
print("rows", len(rows), "fresh", len(FRESH), "carried", carried, "new", new_ids, "mutants", len(mutants),
      "verdict", fragment["verdict"])
