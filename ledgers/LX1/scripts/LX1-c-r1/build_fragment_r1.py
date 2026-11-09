"""Round 1 (LX1-c) closing delta: builds ledgers/LX1/LX1-c.json from the base fragment (round 23, pin dde0486b) and the
round-1 outputs in ledgers/LX1/scripts/LX1-c-r1/out/. Rows of the base keep their ids. Rows re-verified this round carry
fresh evidence; the others carry the base evidence under the carry prefix (their cited subjects are byte-identical).
Usage: .venv/bin/python -I ledgers/LX1/scripts/LX1-c-r1/build_fragment_r1.py <repo_root> <base_fragment_json>"""
import json
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
base = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
out = root / "ledgers/LX1/scripts/LX1-c-r1/out"

CARRY = ("Carried from round 23 (course/modules/LX/LX1/project.html changed only at line 473 since the pin dde0486b, "
         "and tests/labs/LX1/ is byte-identical; the cited subject is unchanged): ")

fresh = {
    "proj-rubric-c1-level1-dominated": (
        "FAIL", "2.6-rubric (observable and reachable; no level dominated)",
        "course/modules/LX/LX1/project.html:473 (C1 td 4, new text 'Names only one of the episode and the condition, or names two without saying which is which.'); "
        "td 1 to 3 at the same line",
        "Re-verified from scratch at 95f3f8cb. The level-1 cell overlaps the level-2-to-4 cells under one reading of those cells. "
        "ledgers/LX1/scripts/LX1-c-r1/c1_levels_r1.py (out/c1_levels_r1.out) enumerates "
        "648 valid fact combinations of an essay (episodes named, conditions named, labelled or not, dates, locators, listed-type locators). "
        "Lenient reading (the cells 2 to 4 say 'names both' and do not require labelling): 144 combinations match level 1 and a level 2-4 "
        "cell; the highest-level rule then scores them 2, 3 or 4, so the level-1 clause 'names two without saying which is which' is inert "
        "for every essay that names one episode and one condition. Example: one episode and one condition, unlabelled, with dates and "
        "locators for both (fact vector 1,1,0,1,1,1,1,1,1) scores 4 while its own level-1 text describes it. Strict reading (labelling "
        "required for 2 to 4): 0 overlaps. The page does not state which reading applies. Classified LOW (wording), but the row's subject is the changed cell, so it is FAIL.",
        "Either add 'and says which is the episode and which the condition' to the level 2, 3 and 4 cells (td 1 to 3 at project.html:473), "
        "or change td 4 to 'Names only one of the episode and the condition, or names two items that are both episodes or both conditions.' "
        "Then re-run c1_levels_r1.py; the lenient overlap count must be 0."),
    "proj-rubric-c1-level1-event-term": (
        "PASS", "2.9-prose / 2.6-rubric (terms; literal reading of the level-1 element)",
        "course/modules/LX/LX1/project.html:473 (C1 td 4); :440 (brief item 1 'one historical episode and one current condition'); :261-265 (spec context)",
        "Re-verified. The round-23 defect (undefined 'event') is gone: td 4 now reads 'Names only one of the episode and the condition', and "
        "'episode' and 'condition' are the terms of brief item 1 at :440 and of the spec at :261-265, which precede the rubric (:467). "
        "grep for 'event' in the C1 row returns no match at 95f3f8cb.", None),
    "proj-rubric-c1-level3-unreachable": (
        "PASS", "2.6-rubric (level 3 reachable; level 3 and level 4 differ)",
        "course/modules/LX/LX1/project.html:473 (C1 td 1 = level 4, td 2 = level 3; td 1 to 3 byte-identical to dde0486b)",
        "Re-verified. Level 4 requires a locator of a listed type (page, table, section, title field, MANIFEST row); level 3 requires "
        "'at least one locator for each of the two' with no type. A locator of another type (for example a URL) with dates for both "
        "items scores 3 and not 4, so level 3 is reachable (ledgers/LX1/scripts/LX1-c-r1/c1_levels_r1.py, fact tE=0 with lE=1). "
        "The changed cell is td 4 only.", None),
    "proj-rubric-observable": (
        "PASS", "2.6-rubric (observable descriptors)",
        "course/modules/LX/LX1/project.html:467, :471-477",
        "Re-verified. The changed level-1 cell names observable items: one of the two items, and whether the essay says which item is "
        "which. A reader can check each element against the essay.", None),
    "proj-student-error-coverage": (
        "PASS", "2.6-rubric (student-error analogue)",
        "course/modules/LX/LX1/project.html:467, :473-477; plans/LX1-build-plan.md 5.4",
        "Re-verified. The level-1 cell still catches the student error of naming only the episode or only the condition, and of naming "
        "two items without placing them; the level-2 to 4 cells still catch a missing date or locator.", None),
    "proj-calibration-exemplars": (
        "PASS", "2.6-rubric-calibration (ruling 23: blind scorer, not this verifier)",
        "course/modules/LX/LX1/project.html:485 (exemplar A data-scores 4,4,4,4,3), :547 (exemplar B data-scores 2,2,1,2,1), :549 (exemplar B verdict: names both and dates only the episode), :568 (exemplar B C1 annotation 'Meets C1 level 2'); ~/.fanout/blind/LX1-c.json (A [4,4,4,4,3], B [2,2,1,2,1])",
        "The blind scorer file (dated 2026-11-08 23:58, before the closing commits) gives A [4,4,4,4,3] and B [2,2,1,2,1], equal to the official "
        "data-scores. The changed C1 level-1 cell cannot move either exemplar's C1 score: exemplar A's C1 is level 4 (the highest matched level), "
        "and exemplar B's C1 names both the episode and the condition (:549, :568), so it matches level 2 and not level 1 under the highest-level rule.", None),
    "proj-notation": (
        "PASS", "2.4-notation (every TeX span on the page)",
        "course/modules/LX/LX1/project.html TeX spans (31 spans)",
        "Re-run at 95f3f8cb: ledgers/LX1/scripts/LX1-c-r1/out/tex_href_identity_r1.out reports 31 TeX spans, current and pin identical; "
        "line 473 contains no TeX.", None),
    "proj-scope-words": (
        "PASS", "2.9-prose (scope words)",
        "course/modules/LX/LX1/project.html learner prose (tags stripped, pre excluded); the changed cell (:473)",
        "Re-run: ledgers/LX1/scripts/LX1-c-r1/out/prose_scan_r1.out. The one new match is 'only' in the level-1 cell ('Names only one of "
        "the episode and the condition'). It is a classification of the level, not a claim about the world, and needs no computation "
        "(ruling 4 concerns claims). Other scope-word matches are unchanged (54 of 55 identical).", None),
    "proj-process-words": (
        "PASS", "2.9-prose (process words)",
        "course/modules/LX/LX1/project.html learner prose",
        "Re-run: prose_scan_r1.out: current 2 matches (Round at :87, round at :174) = pin 2 matches; no new process word in the changed cell.", None),
    "proj-banned-phrases": (
        "PASS", "2.9-structure (BUILDER_RULES 1.3-1.4)",
        "course/modules/LX/LX1/project.html learner prose",
        "Re-run: prose_scan_r1.out: banned strings 0 matches current and pin.", None),
    "proj-links-anchors": (
        "PASS", "2.9-structure (href and id)",
        "course/modules/LX/LX1/project.html (href and id attributes)",
        "Re-run: tex_href_identity_r1.out: href/id attributes 60 current, 60 pin, identical.", None),
    "proj-dag-concepts": (
        "PASS", "2.9-DAG (concept links in the page)",
        "course/modules/LX/LX1/project.html:170, :474; ledgers/LX1/scripts/LX1-c-r1/out/check_dag_LX1.out",
        "Re-run: check_dag --unit LX1 rc=0 (check_dag_LX1.out). The changed cell has no concept link.", None),
    "proj-check-pages-project-scope": (
        "PASS", "2.9-structure",
        "course/modules/LX/LX1/project.html; ledgers/LX1/scripts/LX1-c-r1/out/check_pages_LX1.out",
        "Re-run: check_pages --unit LX1: PASS, rc=0.", None),
    "proj-page-smoke": (
        "PASS", "2.9-structure (page_smoke)",
        "ledgers/LX1/scripts/LX1-c-r1/out/page_smoke_project.out",
        "Re-run: page_smoke --unit LX1 --pages project: PASS rc=0 (labs 1 to 3 run; no overflow reported).", None),
    "proj-gate-commands": (
        "PASS", "gate (targeted gates for this slice, run in round 1)",
        "ledgers/LX1/scripts/LX1-c-r1/run_gates_r1.sh; ledgers/LX1/scripts/LX1-c-r1/out/*.out",
        "Re-run at 95f3f8cb: check_projects, check_pages, check_dag, run_labs (7/7 and project 3/3), page_smoke, verify_refs --offline "
        "(560 entries, 0 problems), ruff check and format, mypy --no-incremental on tests/labs/LX1 and the new test file, and pytest "
        "tests/test_labs.py, test_run_labs.py, test_page_smoke.py, test_page_checks.py: all rc=0. The one failing command is "
        "pytest tests/test_lx1_project_lab3.py (row proj-test-lab3-popsd-variant).", None),
    "proj-run-labs-project": (
        "PASS", "2.5-labs",
        "ledgers/LX1/scripts/LX1-c-r1/out/run_labs_project.out",
        "Re-run: run_labs --unit LX1 --page project: PASS (3/3), rc=0.", None),
    "proj-lab3-raise-claims-untested": (
        "PASS", "2.5-labs (claim that the lab raises)",
        "course/modules/LX/LX1/project.html:308-309 (Check paragraph: a blank or non-decimal GBP cell, and a month that does not follow, raise ValueError), :431; tests/test_lx1_project_lab3.py (new since dde0486b)",
        "The raise claims are now run. pytest tests/test_lx1_project_lab3.py: test_a_blank_or_non_decimal_gbp_cell_raises_value_error[blank] and [non-decimal] pass; test_a_month_that_does_not_follow_the_previous_one_raises_value_error passes (out/pytest_lx1_lab3.out). "
        "The one failing test in that file (population-sd variant) asserts a message the page does not state and the twin does not print (row proj-test-lab3-popsd-variant), so it does not bear on the page's claims.", None),
    "proj-lab3-blank-gap-inputs": (
        "PASS", "2.5-labs (blank cell and gap inputs)",
        "ledgers/LX1/mutants/r17n01, lx1c_r18n05, lx1c_r8n03, lx1c_r8n04; tests/labs/LX1/lab-LX1-project-3.py:21-22, :66-73; tests/test_lx1_project_lab3.py",
        "Re-run: survivor_tests_r1.py (out/survivor_tests_r1.out): the repo scenarios kill r17n01 and lx1c_r18n05 (blank GBP cell), the gap scenario passes for every survivor "
        "because no survivor drops a month. Mutants r8n03 and r8n04 are killed on the embedded snapshot (kill_all_r1.out).", None),
    "proj-mutants-student-errors": (
        "PASS", "2.6-mutation (lab analogue; LX1 has no grader)",
        "ledgers/LX1/mutants/ (94 files); ledgers/LX1/scripts/LX1-c-r1/out/kill_all_r1.out",
        "Re-run all 94 mutants (kill_all_r1.py, copy of the round-23 harness): 88 KILLED on the embedded snapshot, 6 survive it "
        "(r17n01, r18n02, r18n03, r18n04, r18n05, r20n04); each of the 6 is KILLED by a synthetic input (synth_kill_r1.out, "
        "diff_printed_search_r1.out, flat_1e10_r1.out). Lab mutants are demonstrations, not graders (ruling).", None),
    "proj-r23-delta-hunks": (
        "PASS", "2.9-prose / delta (every hunk in the slice, pin dde0486b to 95f3f8cb)",
        "git diff dde0486b..95f3f8cb -- course/modules/LX/LX1 tests/labs/LX1 tests/test_lx1_project_lab3.py ledgers/LX1/mutants",
        "Every hunk read. project.html: one changed line (:473, the C1 level-1 cell). tests/labs/LX1: no change. tests/test_lx1_project_lab3.py: "
        "new file, 102 lines, read in full (its failing scenario is row proj-test-lab3-popsd-variant). ledgers/LX1/mutants: 4 new files "
        "lx1c_r23n01 to n04 (the round-23 mutants; killed, see proj-mutants-student-errors).", None),
    "proj-alternatives": (
        "PASS", "2.6-mutation (over-constraint: five alternative correct implementations)",
        "ledgers/LX1/scripts/LX1-c-r20/alts/alt1..alt5; ledgers/LX1/scripts/LX1-c-r1/out/alts_r1.out",
        "Re-run at 95f3f8cb: alts_r23.py (out/alts_r1.out): all five alternatives print the page's expected block (rc=0, stdout equal to expected).", None),
}

fresh.update({
    "proj-r23-synthetic-survivors": (
        "PASS", "2.5-labs (synthetic inputs for the six embedded survivors)",
        "ledgers/LX1/mutants/r17n01, lx1c_r18n02..n05, lx1c_r20n04; ledgers/LX1/scripts/LX1-c-r1/out/synth_kill_r1.out, diff_printed_search_r1.out, flat_1e10_r1.out",
        "Re-run at 95f3f8cb: each of the six survivors of the embedded snapshot is KILLED by a synthetic input (blank GBP cell: r17n01 and lx1c_r18n05; "
        "1e-5 move: lx1c_r18n03; window-two drift: lx1c_r18n04; f=0.5 scaling: lx1c_r18n02 prints 1.13 against 1.14; 1e-10 move: lx1c_r20n04 prints 668 against 667 zero changes). "
        "These are lab demonstrations; the page does not claim the lab checks exact-zero tolerance or the unrounded difference as a check (ruling: labs are not mutation-tested). "
        "Four of the six have no repo test (r18n02, r18n03, r18n04, r20n04); noted for the architect, not a finding under that ruling.", None),
    "proj-lab3-r21-mutants": (
        "PASS", "2.5-labs (student-error mutants, own, round 21)",
        "ledgers/LX1/mutants/lx1c_r21n01..n04; ledgers/LX1/scripts/LX1-c-r1/out/kill_all_r1.out",
        "Re-run: all four KILLED on the embedded snapshot (stdout differs from the expected block).", None),
    "proj-lab3-r20-mutants": (
        "PASS", "2.5-labs (student-error mutants, r20)",
        "ledgers/LX1/mutants/lx1c_r20n01..n04; ledgers/LX1/scripts/LX1-c-r1/out/kill_all_r1.out, alts_r1.out",
        "Re-run: lx1c_r20n01..n03 KILLED on the embedded snapshot; lx1c_r20n04 KILLED by the synthetic 1e-10 input (flat_1e10_r1.out).", None),
    "proj-lab3-r19-mutants": (
        "PASS", "2.5-labs (student-error mutants, r19)",
        "ledgers/LX1/mutants/r19n01..n03; ledgers/LX1/scripts/LX1-c-r1/out/kill_all_r1.out",
        "Re-run: r19n01..n03 KILLED on the embedded snapshot.", None),
    "proj-r23-mutants-new": (
        "PASS", "2.5-labs (student-error mutants, own, round 23)",
        "ledgers/LX1/mutants/lx1c_r23n01..n04; ledgers/LX1/scripts/LX1-c-r1/out/kill_all_r1.out",
        "Re-run: lx1c_r23n01..n04 KILLED on the embedded snapshot (rc 0 or 1, stdout differs from the expected block). No new mutant is written this round (ruling 37).", None),
    "proj-lab3-twin-run": (
        "PASS", "2.5-labs (twin alone; page code equals twin)",
        "course/modules/LX/LX1/project.html:285-432; tests/labs/LX1/lab-LX1-project-3.py (byte-identical to dde0486b); ledgers/LX1/scripts/LX1-c-r1/out/run_labs_project.out",
        "Re-run: run_labs --unit LX1 --page project: 3/3 PASS, rc=0. The page's lab block lines 285-432 are unchanged, and the twin is unchanged.", None),
    "proj-lab1-twin-run": (
        "PASS", "2.5-labs (twin alone under python -I -W error; page code equals twin)",
        "course/modules/LX/LX1/project.html:78-169; tests/labs/LX1/lab-LX1-project-1.py; ledgers/LX1/scripts/LX1-c-r1/out/run_labs_project.out",
        "Re-run: run_labs --unit LX1 --page project: 3/3 PASS (includes lab 1), rc=0. Lines 78-169 and the twin are unchanged.", None),
})

FAIL_ROWS = {
    "proj-test-lab3-popsd-variant": {
        "id": "proj-test-lab3-popsd-variant",
        "check": "2.5-labs / gate (a repo test under tests/ must match the twin and the page)",
        "location": "tests/test_lx1_project_lab3.py:90-101 (test_a_population_sd_variant_of_the_two_pass_check_raises; the failing assertion is at :101); tests/labs/LX1/lab-LX1-project-3.py (no 'statistics.stdev', 'disagree', or tolerance text)",
        "status": "FAIL",
        "evidence": "pytest -q tests/test_lx1_project_lab3.py at 95f3f8cb: 4 passed, 1 failed (ledgers/LX1/scripts/LX1-c-r1/out/pytest_lx1_lab3.out): 'AssertionError: a population-sd variant must not pass the agreement check', assert 0 != 0 (the n-denominator variant runs to rc 0). The test expects 'ValueError: the two-pass and statistics.stdev standard deviations disagree', which the twin never prints; grep of the twin and of project.html for 'disagree', 'statistics', and '1e-9' returns nothing, and the page's only two-pass mention is :60. Later commit 9a85e9e8 (not in this pin; it changes only tests/test_lx1_project_lab3.py, the twin and the page are byte-identical between the two commits) rewrites this test to compare the printed 'sample sd' lines; that file run against this pin's twin gives 5 passed (/tmp/lx1c-r1-fix, PYTHONPATH=tools). The variant does change those lines (lx1c_r23n02 KILLED on the embedded snapshot). Gate impact: the CI pytest step fails on this file.",
        "fix": "Take tests/test_lx1_project_lab3.py from commit 9a85e9e8 (test-only change) or otherwise drop the statistics.stdev expectation; then .venv/bin/python -m pytest -q tests/test_lx1_project_lab3.py must report 5 passed.",
    },
}

rows = []
for r in base["rows"]:
    rid = r["id"]
    if rid in FAIL_ROWS:
        rows.append(FAIL_ROWS[rid])
        continue
    if rid in fresh:
        status, check, location, evidence, fix = fresh[rid]
        row = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
        if status != "PASS":
            row["fix"] = fix
        rows.append(row)
        continue
    rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": r["status"],
                 "evidence": CARRY + r["evidence"]})
rows.append(FAIL_ROWS["proj-test-lab3-popsd-variant"])
known = {r["id"] for r in rows}
assert "proj-test-lab3-popsd-variant" in known
assert "proj-rubric-c1-level1-dominated" in known

# ---- mutants: 94 files, base descriptions, round-1 kill evidence ----
import datetime
mutant_dir = root / "ledgers/LX1/mutants"
base_desc = {m["name"]: m["description"] for m in base["mutants"]}
kill_lines = (out / "kill_all_r1.out").read_text(encoding="utf-8").splitlines()
embedded = {}
pat = re.compile(r"^lab(\d) (\S+): rc=(\d+) stdout==expected (\w+) -> (KILLED|SURVIVED)")
for line in kill_lines:
    m = pat.match(line)
    if m:
        embedded[m.group(2)] = (int(m.group(1)), m.group(3), m.group(5))
SYNTH = {
    "r17n01_lab3_blank_gbp_cell_read_as_zero.py": "synthetic blank GBP cell 2010-06 (synth_kill_r1.out): mutant rc 1 with 'ValueError: expected a positive input, got 0.0' against the twin's blank-cell ValueError -> KILLED",
    "lx1c_r18n05_lab3_blank_cell_carried_forward_as_flat_rate.py": "synthetic blank GBP cell 2010-06 (synth_kill_r1.out): mutant rc 0 with stdout differing from the twin's ValueError run -> KILLED",
    "lx1c_r18n03_lab3_zero_change_tested_after_rounding_to_four_places.py": "synthetic 1e-5 relative move at month 100 (synth_kill_r1.out): mutant stdout differs from the twin -> KILLED",
    "lx1c_r18n04_lab3_window_two_centred_on_window_one_mean.py": "synthetic window-two drift of 1 percent a month (synth_kill_r1.out): mutant stdout differs from the twin -> KILLED",
    "lx1c_r18n02_lab3_difference_of_printed_sds.py": "synthetic window-two changes scaled by 0.5 (diff_printed_search_r1.out): difference 1.14 from the printed sds against 1.13 from the twin -> KILLED",
    "lx1c_r20n04_lab3_zero_test_with_tolerance.py": "synthetic flat series with one 1e-10 relative move (flat_1e10_r1.out): mutant 668 exact zero changes against the twin's 667 -> KILLED",
}
mutants = []
files = sorted(p.name for p in mutant_dir.glob("*.py"))
for name in files:
    if name not in base_desc:
        raise SystemExit(f"no base description for {name}")
    if name in embedded and embedded[name][2] == "KILLED":
        lab, rc, _ = embedded[name]
        killed = f"embedded snapshot (ledgers/LX1/scripts/LX1-c-r1/out/kill_all_r1.out): lab {lab} rc={rc}, stdout differs from the expected block -> KILLED"
    elif name in SYNTH:
        killed = SYNTH[name]
    else:
        raise SystemExit(f"{name} not killed")
    mutants.append({"name": name, "description": base_desc[name], "killed_by": killed})

# ---- assemble ----
counts = {s: sum(1 for r in rows if r["status"] == s) for s in ("PASS", "FAIL")}
notes = [
    "Round 1 (closing delta, ruling 30). Base: ledgers/LX1/LX1-c.json of round 23 at pin dde0486b (fragment /Users/billyribeiro/.fanout/frags/E-LX1-c.round23.json, verdict FAIL with one LOW row, proj-rubric-c1-level1-event-term). The task asks for round 1 of this verifier's ledger; the base is round 23. Pin 95f3f8cb is a descendant of dde0486b (git merge-base --is-ancestor holds).",
    "Delta dde0486b..95f3f8cb for the slice paths: course/modules/LX/LX1/project.html (one line, :473, the C1 level-1 cell, changed by b9912454); tests/test_lx1_project_lab3.py (new file, 102 lines, added in 4540351d); ledgers/LX1/mutants (four new round-23 mutants); ledgers/LX1/scripts/LX1-c-r23 (base scripts). tests/labs/LX1, the lesson pages, cards and data are byte-identical over the range (git diff --stat empty).",
    "The round-23 FAIL row (proj-rubric-c1-level1-event-term, undefined 'event') is fixed and re-verified PASS. The new level-1 text introduces a LOW overlap (proj-rubric-c1-level1-dominated, FAIL) under the lenient reading of levels 2 to 4.",
    "Blocking defect: proj-test-lab3-popsd-variant. The pin's pytest run of tests/test_lx1_project_lab3.py fails 1 of 5. A later commit 9a85e9e8 (outside this pin) fixes the test; its version passes against this pin's twin (5 passed). Ruling 26 'a failing gate' applies at this pin.",
    "Calibration (ruling 23): the blind scorer file ~/.fanout/blind/LX1-c.json (dated 2026-11-08 23:58, before the closing commits) gives A [4,4,4,4,3] and B [2,2,1,2,1], matching the official data-scores; the changed cell cannot move either exemplar's C1 score (A is level 4; B names both roles, :549 and :568, so level 2).",
    "No new mutants were written this round (ruling 37). Mutants: 94 files in ledgers/LX1/mutants re-run on the embedded snapshot: 88 KILLED, 6 survive it (r17n01, r18n02, r18n03, r18n04, r18n05, r20n04), each KILLED by a synthetic input (synth_kill_r1.out, diff_printed_search_r1.out, flat_1e10_r1.out). LX1 has no grader; these are lab demonstrations (ruling). Four of the six survivors have no repo test; noted for the architect, not a finding under the lab ruling.",
    "Ruling 37 check on the tests the fixer adds: the blank-cell scenario of tests/test_lx1_project_lab3.py kills r17n01 and r18n05; the gap scenario kills none (no survivor drops a month); the population-sd scenario is broken (see proj-test-lab3-popsd-variant). Output: ledgers/LX1/scripts/LX1-c-r1/out/survivor_tests_r1.out.",
    "Alternatives (over-constraint): all five alternatives print the expected block at this pin (alts_r1.out). Lab twins run alone under python -I -W error through run_labs (3/3 project, 7/7 unit).",
    "Gates run at this pin (ledgers/LX1/scripts/LX1-c-r1/run_gates_r1.sh): check_projects, check_pages, check_dag, run_labs (unit and project), page_smoke (project), verify_refs --offline (560 entries, 0 problems), ruff check and format, mypy --no-incremental (labs and the new test file), pytest of the lab-related test modules: all rc 0, except pytest tests/test_lx1_project_lab3.py rc 1.",
    "Carry rule: rows not listed as re-verified carry their base evidence under the prefix 'Carried from round 23', because the cited lines (other than :473) and tests/labs/LX1 are byte-identical since dde0486b. Whole-page scans (TeX, href/id, scope and process words, banned strings) were re-run, not carried.",
    "Not run or not checked: full repository pytest and the full gate (slice-only per ruling 30); the Pyodide run of the page in a browser (run_labs and page_smoke cover the labs); live verify_refs (offline only); mutate_graders (LX1 has no grader); the alternative implementations for LX1 labs beyond the five in ledgers/LX1/scripts/LX1-c-r20/alts; a fresh blind scoring of the exemplars (the existing blind file is used and cited).",
    "Registry flag (carried from round 23): friedman1963monetary registry record lists Friedman only (references/references.json); pages cite the key only. Correction is an architect request.",
]
summary = (f"Closing delta round 1 for LX1-c at 95f3f8cb. FAIL: one blocking gate row (proj-test-lab3-popsd-variant, a repo test fails 1 of 5; fixed by later commit 9a85e9e8, not in pin) and one LOW rubric overlap in the changed C1 level-1 cell (proj-rubric-c1-level1-dominated). "
           f"The round-23 event-term row is fixed (PASS). Rows: {len(rows)} ({counts['PASS']} PASS, {counts['FAIL']} FAIL). Mutants: {len(mutants)} (94 KILLED on embedded or synthetic inputs).")
fragment = {
    "unit": "LX1",
    "slice": "LX1-c",
    "round": 1,
    "verifier": "Claude Haiku 5.5 (claude-haiku-5-5), independent verifier for LX1-c, round 1 (closing delta; did not build LX1)",
    "pin": "95f3f8cb21c2cd9fc904430bd30a6b734d01f672",
    "base": "dde0486beeb0312e4ac1cc03aaa02e56644adb24 (round-23 fragment /Users/billyribeiro/.fanout/frags/E-LX1-c.round23.json)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyF31-LX1-c",
    "scratch": "ledgers/LX1/scripts/LX1-c-r1/ (scripts and out/); synthetic data only under /tmp/lx1c-r1-*",
    "verified_at": datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat(),
    "verdict": "FAIL",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": base["registry_flags"],
    "freshness_flags": [],
    "notes": notes,
    "summary": summary,
}
dest = root / "ledgers/LX1/LX1-c.json"
dest.write_text(json.dumps(fragment, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
print("rows", len(rows), counts, "mutants", len(mutants))
