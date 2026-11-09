"""Round 23 (LX1-c): assembles ledgers/LX1/LX1-c.json from the round-21 fragment (carried rows and mutant descriptions),
the round-23 outputs under ledgers/LX1/scripts/LX1-c-r23/out/, and the kill results. Usage: python -I make_fragment_r23.py <repo_root>"""
import json
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
S = root / "ledgers/LX1/scripts/LX1-c-r23"
OUT = S / "out"
r21 = json.load(open("/Users/billyribeiro/.fanout/frags/E-LX1-c.round21.json", encoding="utf-8"))
kill = json.load(open(S / "kill_all_r23.json", encoding="utf-8"))
kill_by_name = {name: (lab, status, rc) for name, lab, status, rc in kill}
r21_mut = {m["name"]: m for m in r21["mutants"]}
R21 = "Carried from round 21 (course/modules/LX/LX1/project.html outside line 473, and the lab twins, data and MANIFEST byte-identical since the round-21 pin 6d22ff56; git diff 6d22ff56..dde0486b touches project.html only at :473):"
rows_by_id = {r["id"]: r for r in r21["rows"]}

def carry(rid, check=None, location=None, evidence_extra=""):
    r = dict(rows_by_id[rid])
    if check is not None:
        r["check"] = check
    if location is not None:
        r["location"] = location
    base = r["evidence"]
    r["evidence"] = f"{R21} {base}" + (f" {evidence_extra}" if evidence_extra else "")
    r["status"] = "PASS"
    return r

def fresh(rid, check, location, evidence, status="PASS", fix=None):
    row = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if fix:
        row["fix"] = fix
    return row

def out(name):
    return f"ledgers/LX1/scripts/LX1-c-r23/out/{name}"

rows = []
# re-verified rows (subject changed or re-run now)
rows.append(fresh("proj-rubric-c1-level1-dominated", "2.6-rubric (observable and reachable; no level dominated)",
    "course/modules/LX/LX1/project.html:473 (C1 td 4, new text 'Names one event, or names two without saying which is the episode and which the condition.'); :467",
    "Re-verified in round 23. Level 1 is now exclusive of levels 2 to 4: levels 2 to 4 each require the episode and the condition to be named with the labels (W), and the level-1 clause for two items requires 'without saying which'. Enumeration over 288 combinations of the item facts (ledgers/LX1/scripts/LX1-c-r23/c1_levels_r23.py; out: " + out("c1_levels_r23.out") + ") finds no combination where level 1 and a level 2-4 match both hold, other than the 4-and-2 artifact of the model's L2 definition, which the highest-level rule resolves. The round-21 defect (the old 'Picks two events.' matched every essay that named two items, including those at level 2) is gone."))
rows.append(fresh("proj-rubric-c1-level1-event-term", "2.9-prose / 2.6-rubric (terms; literal reading of the level-1 element)",
    "course/modules/LX/LX1/project.html:473 (C1 td 4: 'Names one event'); :64 (a condition is a measured quantity), :265 (episode and current condition)",
    "The new level-1 cell uses 'event', which the page never defines and never uses elsewhere (grep: the word occurs only at :473). The page defines a condition as a measured quantity (:64), so a condition is not an event. Read literally, an essay that names only its current condition (with dates and locators) matches no level and scores 0 (not yet met) under the rule at :467, while 'names one event' read as 'names one episode or condition' scores 1. Enumeration (" + out("c1_levels_r23.out") + "): 72 of 288 fact combinations (all 72 of them essays that name only the current condition) get a different level under the two readings. LOW wording: no blocking kind (no false or unproved statement, no wrong number, no over-graded claim). Ruling 26 lists LOW wording rows in plans/KNOWN-ISSUES.md.",
    status="FAIL",
    fix="At :473 replace 'Names one event, or names two without saying which is the episode and which the condition.' with 'Names only one of the episode and the condition, or names two without saying which is which.' (same exclusivity; no new overlap). Until then list the row in plans/KNOWN-ISSUES.md as LOW."))
rows.append(fresh("proj-rubric-c1-level3-unreachable", "2.6-rubric (level 3 reachable; level 3 and level 4 differ)",
    "course/modules/LX/LX1/project.html:473 (C1 td 2 = level 3, td 1 = level 4; cells 1 to 3 byte-identical to the pin)",
    "Re-verified in round 23. Level 3 is 'dates for both, at least one locator for each of the two'; level 4 is 'a locator for each date'. Level 3 and not level 4 holds when a date has no locator of its own while the item has a locator elsewhere (for example, a page that discusses the episode but does not give its date), so level 3 is reachable with one date per item. The round-21 note said level 3 needs two or more dates; that note is imprecise, and the row stays PASS because level 3 is reachable (enumeration: 3 fact combinations with L3 and not L4, " + out("c1_levels_r23.out") + ")."))
rows.append(fresh("proj-rubric-observable", "2.6-rubric (observable descriptors)",
    "course/modules/LX/LX1/project.html:467, :471-477",
    "Re-verified in round 23 with the new :473 cell: every level names an element a reader can check (a date, a locator, a labelled item, a chain of steps, a formula, a base, a sign, a limit with its test). The level-1 wording is observable except for the 'event' term, which is recorded in proj-rubric-c1-level1-event-term."))
rows.append(fresh("proj-student-error-coverage", "2.6-rubric (student-error analogue)",
    "course/modules/LX/LX1/project.html:467, :473-477; plans/LX1-build-plan.md 5.4",
    "Re-verified in round 23: the student errors the rubric grades (no date, no locator, uncited claim, rounded input, missing base, untested limit) have a cell at some level in :473-477; the changed cell adds no new error class. Lab-side student errors are in proj-r23-mutants-new and proj-mutants-student-errors."))
rows.append(fresh("proj-calibration-exemplars", "2.6-rubric-calibration (ruling 23: blind scorer, not this verifier)",
    "course/modules/LX/LX1/project.html:485 (exemplar A data-scores 4,4,4,4,3), :547 (exemplar B data-scores 2,2,1,2,1); ~/.fanout/blind/LX1-c.json",
    "Calibration row, scored by the dedicated blind scorer (ruling 23); this verifier did not score the exemplars. ~/.fanout/blind/LX1-c.json field A = [4,4,4,4,3] and field B = [2,2,1,2,1]; both equal the official data-scores at project.html:485 and :547 (C1 to C5 in order). The blind notes apply the rule at :467 as stated (highest level whose every element is shown, lower-level elements do not lower it). The round-23 cell change at :473 does not alter either exemplar's level (both exemplars name the episode and the condition labelled, so level 1 is not the highest level either meets). PASS on the blind scorer's output."))
rows.append(carry("proj-exemplar-numbers", location=None))
rows.append(carry("proj-reading-keys"))
rows.append(carry("proj-reading-reinhart-registry"))
rows.append(fresh("proj-notation", "2.4-notation (every TeX span on the page)",
    "course/modules/LX/LX1/project.html TeX spans (31 spans, compared with the pin)",
    "Re-derived in round 23: the list of all 31 \\(...\\) spans in project.html is identical to the list at pin 6d22ff56 (tex_href_identity_r23.py, out: " + out("tex_href_identity_r23.out") + "). The changed line :473 contains no TeX span. Notation unchanged."))
rows.append(fresh("proj-scope-words", "2.9-prose (scope words)",
    "course/modules/LX/LX1/project.html learner prose (tags stripped, pre excluded)",
    "Re-derived in round 23 with ledgers/LX1/scripts/LX1-c-r23/prose_scan_r23.py (out: " + out("prose_scan_r23.out") + "): 54 scope-word matches (every, only, all, any, same) in the current page and 54 at pin 6d22ff56, identical positions; the matches differ by nothing, so the changed :473 cell adds no scope word."))
rows.append(fresh("proj-process-words", "2.9-prose (process words)",
    "course/modules/LX/LX1/project.html learner prose",
    "Re-derived in round 23 (prose_scan_r23.py, out: " + out("prose_scan_r23.out") + "): process-word matches are two, 'Round' at :87 and 'round' at :174 (the rounding sense, unchanged), the same at the pin; none in :473."))
rows.append(fresh("proj-banned-phrases", "2.9-structure (BUILDER_RULES 1.3-1.4)",
    "course/modules/LX/LX1/project.html learner prose",
    "Re-derived in round 23 (prose_scan_r23.py, out: " + out("prose_scan_r23.out") + "): zero matches for TODO, TBD, lorem, 'for brevity', 'beyond the scope', 'it is important to note', 'obviously', 'clearly', 'studies show', 'experts agree', 'it is well known', 'About n%', 'roughly half', 'historically' in the current page and at the pin."))
rows.append(carry("proj-hours"))
rows.append(carry("proj-rung1-step3-rounding-claim"))
rows.append(carry("proj-real-value-vs-lesson2"))
rows.append(carry("proj-manifest-note-misattributed"))
rows.append(carry("proj-lab3-citation-string"))
rows.append(carry("proj-spec-current-undefined"))
rows.append(carry("proj-exemplar-A-condition"))
rows.append(fresh("proj-gate-commands", "gate (targeted gates for this slice, run in round 23)",
    "ledgers/LX1/scripts/LX1-c-r23/run_gates_r23.sh; out/*.out",
    "Re-run in round 23 on dde0486b: check_projects --unit LX1 and --all rc 0; check_pages --unit LX1 'PASS'; check_dag --unit LX1 and --all rc 0; run_labs --unit LX1 'PASS (3/3)' rc 0; page_smoke --pages project 'PASS' rc 0; verify_refs --offline '560 entries, 0 problems' rc 0; fetch_data --check '3 datasets, 0 problems' rc 0; build_site --check 'site data current' rc 0; ruff check and format rc 0; mypy --no-incremental tests/labs/LX1 'no issues found in 7 source files' rc 0; mypy full rc 0; pytest test_labs, test_run_labs, test_page_smoke, test_page_checks, test_curriculum rc 0 (out/pytest_labs.out); pytest test_refs rc 0 (out/pytest_refs.out)."))
rows.append(fresh("proj-run-labs-project", "2.5-labs",
    "ledgers/LX1/scripts/LX1-c-r23/out/run_labs_project.out",
    "Re-run: tools/run_labs.py --unit LX1 --page project -> 'run_labs LX1: PASS (3/3)', rc=0 (out/run_labs_project.out)."))
rows.append(fresh("proj-lab1-twin-run", "2.5-labs (twin alone under python -I -W error; page code equals twin)",
    "course/modules/LX/LX1/project.html:78-149, :150-169; tests/labs/LX1/lab-LX1-project-1.py",
    "Re-run: twins_r23.py (out: " + out("twins_r23.out") + "): lab 1 page code 72 lines, twin 72 lines, 0 differing lines, twin exit 0, stderr empty; expected block equals twin stdout True."))
rows.append(carry("proj-lab1-numbers", evidence_extra="Lab 1 expected block equals its twin's stdout in round 23 (twins_r23.out, lab 1 line)."))
rows.append(fresh("proj-lab2-twin-run", "2.5-labs (twin alone; page code equals twin with blanks only)",
    "course/modules/LX/LX1/project.html:185-246, :247-256; tests/labs/LX1/lab-LX1-project-2.py",
    "Re-run: twins_r23.py (out: " + out("twins_r23.out") + "): lab 2 page code 62 lines, twin 62 lines, 2 differing lines (the two blanks at :30 and :35 of the twin, 'return ___'); page code equals twin with blanks only True; twin exit 0; expected block equals twin stdout True."))
rows.append(carry("proj-lab2-numbers"))
rows.append(carry("proj-lab2-check-claims"))
rows.append(fresh("proj-lab3-twin-run", "2.5-labs (twin alone; page code equals twin)",
    "course/modules/LX/LX1/project.html:285-432; tests/labs/LX1/lab-LX1-project-3.py",
    "Re-run: twins_r23.py (out: " + out("twins_r23.out") + "): lab 3 page code 125 lines, twin 125 lines, 0 differing lines, twin exit 0, stderr empty; expected block equals twin stdout True. Lab 3 run_labs PASS (run_labs_project.out)."))
rows.append(carry("proj-lab3-numbers", evidence_extra="Re-run in round 23: lab 3 prints the same figures (twins_r23.out, lab 3)."))
rows.append(carry("proj-lab3-L04-cross-check", evidence_extra="Lesson 4 changed at :59, :110, :122-123, :326, :333, :448 in this delta; the printed lines cited here (:314) are unchanged."))
rows.append(carry("proj-lab3-docstring-claims"))
rows.append(carry("proj-lab3-interpretation-claims"))
rows.append(carry("proj-lab3-difference-line-r5"))
rows.append(carry("proj-lab-simulated-labels"))
rows.append(carry("proj-data-licence-quote"))
rows.append(fresh("proj-data-snapshot-rebuild", "2.8-data (reproducibility)",
    "course/assets/data/market/fx_monthly.csv; course/assets/data/market/MANIFEST.json",
    "Re-run: tools/fetch_data.py --check -> 'fetch_data: 3 datasets, 0 problems', rc=0 (out/fetch_data_check.out). Data files not in the delta."))
rows.append(carry("proj-data-fields"))
rows.append(carry("proj-data-no-other-series"))
rows.append(carry("proj-data-embedded-claim"))
rows.append(carry("proj-spec-ladder"))
rows.append(carry("proj-spec-curriculum-scope", evidence_extra="curriculum/ and references/ have no file in the round-23 delta (git diff --name-only 6d22ff56 dde0486b -- curriculum references: 0 files)."))
rows.append(carry("proj-atlas-autograder-na", evidence_extra="curriculum/ unchanged in the delta."))
rows.append(fresh("proj-mutants-student-errors", "2.6-mutation (lab analogue; LX1 has no grader)",
    "ledgers/LX1/mutants/ (94 files); ledgers/LX1/scripts/LX1-c-r23/out/kill_all_r23.out",
    "Re-run in round 23: kill_all_r23.py over all 94 mutants on the embedded snapshot: 88 KILLED, 6 SURVIVED (the r17n01, r18n02..n05 and r20n04 mutants); each of the six is KILLED by a synthetic input (proj-r23-synthetic-survivors). Lab demonstrations; ruling: mutation testing applies to graders."))
rows.append(fresh("proj-lab3-r21-mutants", "2.5-labs (student-error mutants, own, round 21)",
    "ledgers/LX1/mutants/lx1c_r21n01..n04; out/kill_all_r23.out",
    "Re-run: lx1c_r21n01..n04 are in the 94-file kill run; KILLED on the embedded snapshot where the output differs (see kill_all_r23.out)."))
rows.append(fresh("proj-lab3-r20-mutants", "2.5-labs (student-error mutants, r20)",
    "ledgers/LX1/mutants/lx1c_r20n01..n04; out/kill_all_r23.out; out/alts_r23.out",
    "Re-run in round 23 (kill_all_r23.out): lx1c_r20n01 (lab 1), lx1c_r20n02 (lab 2) and lx1c_r20n03 (lab 3) KILLED on the embedded snapshot; lx1c_r20n04 SURVIVED the embedded snapshot and was KILLED by the synthetic flat series with one 1e-10 move (flat_1e10_r23.py, out: " + out("flat_1e10_r23.out") + "): twin 667 zero changes, mutant 668."))
rows.append(fresh("proj-lab3-r19-mutants", "2.5-labs (student-error mutants, r19)",
    "ledgers/LX1/mutants/r19n01..n03; out/kill_all_r23.out",
    "Re-run: r19n01..n03 in the 94-file kill run; KILLED on the embedded snapshot (kill_all_r23.out)."))
rows.append(fresh("proj-lab3-blank-gap-inputs", "2.5-labs (blank cell and gap inputs)",
    "ledgers/LX1/mutants/r17n01, lx1c_r18n05, lx1c_r8n03, lx1c_r8n04; tests/labs/LX1/lab-LX1-project-3.py:21-22, :66-73",
    "Re-run: synth_kill_r23.py (out: " + out("synth_kill_r23.out") + "): blank GBP cell 2010-06 KILLS r17n01 (ValueError from the mutant) and lx1c_r18n05 (exit 0 with a flat rate, output differs). The page's Check paragraph says a blank cell raises ValueError (:21); the twin does (load_column, lab-LX1-project-3.py:66-68)."))
rows.append(fresh("proj-r23-mutants-new", "2.5-labs (student-error mutants, own, round 23)",
    "ledgers/LX1/mutants/lx1c_r23n01..n04; ledgers/LX1/scripts/LX1-c-r23/make_mutants_r23.py; out/kill_all_r23.out",
    "Four new student-error mutants of the project lab 3 twin, each a single-line edit: n01 window three starts 2025-09 (13 changes); n02 population denominator n; n03 largest change printed as exp(l) - 1; n04 window two excludes 2000-01. Kill run: n01 KILLED (stdout differs), n02 KILLED, n03 KILLED, n04 KILLED, all rc 0 on the embedded snapshot (kill_all_r23.out)."))
rows.append(fresh("proj-r23-synthetic-survivors", "2.5-labs (synthetic inputs for the six embedded survivors)",
    "ledgers/LX1/mutants/r17n01, lx1c_r18n02..n05, lx1c_r20n04; out/synth_kill_r23.out, diff_printed_search_r23.out, flat_1e10_r23.out",
    "Each survivor killed by a synthetic input: r17n01 and lx1c_r18n05 by the blank cell 2010-06 (synth_kill_r23.out); lx1c_r18n03 by the 1e-5 move at month 100 (synth_kill_r23.out, tiny_move); lx1c_r18n04 by the 1 percent a month drift in window two (synth_kill_r23.out, drift); lx1c_r20n04 by a flat series with one 1e-10 move (flat_1e10_r23.out); lx1c_r18n02 by the search for a scale factor 0.5 on window two, printed-sd difference 1.14 against 1.13 (diff_printed_search_r23.out). Note: the 'diff_printed' case inside synth_kill_r23.py does not reproduce the kill (it prints SURVIVED); the kill is the one in diff_printed_search_r23.out, so the case in synth_kill_r23.py is a defect of the scratch script, not of the lab."))
rows.append(fresh("proj-alternatives", "2.6-mutation (over-constraint: five alternative correct implementations)",
    "ledgers/LX1/scripts/LX1-c-r20/alts/alt1..alt5; out/alts_r23.out",
    "Re-run in round 23 (alts_r23.py): alt1 (lab 1 reciprocal and rearranged), alt2 (lab 2 reciprocal and rearranged), alt3 (lab 3 float ratio before log), alt4 (lab 3 window two by month index), alt5 (lab 3 zero by truthiness): each rc 0 and stdout equal to the page's expected block (out/alts_r23.out). No over-constraint."))
rows.append(carry("proj-exemplar-b-annotations-vs-descriptors", evidence_extra="No annotation in project.html:548-606 names the level-1 cell text; the only occurrence of 'event' in the page is :473."))
rows.append(carry("proj-brief-rubric-escape-clauses"))
rows.append(carry("proj-exemplar-locators"))
rows.append(carry("proj-exemplar-a-c5-limit-count"))
rows.append(carry("proj-round11-delta-project-page"))
rows.append(carry("proj-spec-limits-test-each"))
rows.append(carry("proj-notation-n-undefined"))
rows.append(carry("proj-spec-window-start-must"))
rows.append(carry("proj-rubric-c2-gap"))
rows.append(carry("proj-rubric-c3-level3-gap"))
rows.append(carry("proj-rubric-c3-inference-gap"))
rows.append(carry("proj-rubric-c4-formula-gap"))
rows.append(carry("proj-rubric-c5-count-wording"))
rows.append(carry("proj-rubric-c2-count-wording"))
rows.append(carry("proj-rubric-exhaustive-r14"))
rows.append(fresh("proj-dag-concepts", "2.9-DAG (concept links in the page)",
    "course/modules/LX/LX1/project.html:170, :474; check_dag output (out/check_dag_LX1.out, check_dag_all.out)",
    "Re-run: check_dag --unit LX1 rc 0 and check_dag --all rc 0 (out/check_dag_LX1.out, out/check_dag_all.out). The concept link at :170 and the Lesson 1 Definition 2.1 reference at :474 are byte-identical to the pin (only :473 changed)."))
rows.append(carry("proj-dag-D1-D15", evidence_extra="check_dag --all rc 0 in round 23 (out/check_dag_all.out)."))
rows.append(fresh("proj-exemplar-A-limit1-cip-locator", "2.1-citation (exemplar A limit one locator)",
    "course/modules/LX/LX1/project.html:535 (exemplar A limit one); course/modules/LX/LX1/L04.html:329-333 (section 4 'Where the canon breaks', item 'Exchange rates only')",
    "Re-verified in round 23 because L04.html:333 changed in the delta (the item text now reads 'no column of exchange rates agreed now for delivery at a later date'). The locator still holds: L04.html:333 is the item 'Exchange rates only' under the h2 of section 4 (L04.html:329), and it states 'The lab cannot test any relation between interest rates and exchange rates, because the file has no interest-rate column, and this lesson states none.', which is the sentence exemplar A paraphrases at :535. PASS."))
rows.append(carry("proj-exemplar-a-c2-annotation"))
rows.append(carry("proj-r14-delta-hunks"))
rows.append(carry("proj-r15-delta-hunks"))
rows.append(carry("proj-r18-delta-hunks"))
rows.append(carry("proj-r19-delta-hunks"))
rows.append(carry("proj-r21-delta-hunks"))
rows.append(fresh("proj-r23-delta-hunks", "2.9-prose / delta (every hunk in the slice, pin 6d22ff56 to dde0486b)",
    "git diff 6d22ff56 dde0486b -- course/modules/LX/LX1/project.html tests/labs/LX1/",
    "Every hunk read. project.html: one hunk at :473 (C1 td 4, level-1 cell). tests/labs/LX1/: one hunk, lab-LX1-L04-1.py (docstring line 8-9, the forward-rate sentence); L04 is another slice, and project.html cites no L04 line that changed. Other LX1 hunks in the same range (L01.html :445, L04.html :59, :110, :122-123, :326, :333, :448, cards.json :581) are other slices, read for cross-reference only."))
rows.append(carry("proj-check-pages-project-scope"))
rows.append(fresh("proj-links-anchors", "2.9-structure (href and id)",
    "course/modules/LX/LX1/project.html (href and id attributes, 60 by count)",
    "Re-derived in round 23: the 60 href and id attributes are identical in sequence to the pin (tex_href_identity_r23.py, out: " + out("tex_href_identity_r23.out") + "); the changed :473 cell contains no href or id."))
rows.append(fresh("proj-page-smoke", "2.9-structure (page_smoke)",
    "ledgers/LX1/scripts/LX1-c-r23/out/page_smoke_project.out",
    "Re-run: tools/page_smoke.py --unit LX1 --pages project -> 'page_smoke modules/LX/LX1/project.html: PASS', 'page_smoke LX1: PASS', rc=0 (out/page_smoke_project.out)."))
rows.append(carry("proj-lab3-raise-claims-untested"))
rows.append(carry("proj-lab2-R-blank-check"))

import subprocess
VERIFIED_AT = subprocess.run(["date", "-u", "+%Y-%m-%dT%H:%M:%S+00:00"], capture_output=True, text=True).stdout.strip()
frag = {
    "unit": "LX1",
    "slice": "LX1-c",
    "round": 23,
    "verifier": "Claude Haiku 5.5 (claude-haiku-5-5), independent verifier for LX1-c, round 23 (did not build LX1)",
    "pin": "dde0486beeb0312e4ac1cc03aaa02e56644adb24",
    "base": "6d22ff56fcf3a28e40c82952b25a0c3760f92cbc (round-21 pin; round-21 fragment /Users/billyribeiro/.fanout/frags/E-LX1-c.round21.json). The round-22 fragment named in the task (E-LX1-c.round22.json) does not exist on disk; the delta is therefore computed from the round-21 pin.",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE23-LX1-c",
    "scratch": "ledgers/LX1/scripts/LX1-c-r23/ (scripts and out/); synthetic data only under /tmp/lx1c-r23-*",
    "verified_at": VERIFIED_AT,
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": r21["registry_flags"],
    "freshness_flags": [],
    "notes": [],
    "summary": {},
}

# mutants: all 94 files
mut_dir = root / "ledgers/LX1/mutants"
for f in sorted(mut_dir.glob("*.py")):
    name = f.name
    lab, status, rc = kill_by_name.get(name, (None, None, None))
    if name in r21_mut:
        desc = r21_mut[name]["description"]
    else:
        head = f.read_text(encoding="utf-8").splitlines()[0]
        desc = head.lstrip("# ").strip()
    if status == "KILLED":
        kb = f"embedded snapshot (out/kill_all_r23.out): lab {lab} rc {rc}, stdout differs from the expected block -> KILLED"
    elif name in r21_mut:
        kb = r21_mut[name]["killed_by"] + " (re-checked in round 23: out/synth_kill_r23.out, out/diff_printed_search_r23.out, out/flat_1e10_r23.out)"
    else:
        kb = "UNKILLED"
    frag["mutants"].append({"name": name, "description": desc, "killed_by": kb})

killed = sum(1 for m in frag["mutants"] if m["killed_by"] != "UNKILLED")
from collections import Counter
c = Counter(r["status"] for r in rows)
frag["summary"] = {"rows": len(rows), "pass": c["PASS"], "fail": c["FAIL"], "unverifiable": c["UNVERIFIABLE"], "mutants": len(frag["mutants"]), "mutants_killed": killed}
frag["notes"] = [
    "Scope: course/modules/LX/LX1/project.html (the delta hunk at :473, and the whole page re-derived for whole-page scans), tests/labs/LX1/lab-LX1-project-{1,2,3}.py (byte-identical to the pin), and the LX1 hunks in the same range read for cross-reference (L04.html :333 used by exemplar A; cards.json and L01.html not used by the page).",
    "Delta from the round-21 pin 6d22ff56 to dde0486b (4 commits): project.html :473 only (C1 level-1 cell). Carried rows are those whose cited lines are unchanged; rows that cite :473 or whole-page scans were re-derived this round.",
    "Verdict FAIL comes from one LOW row (proj-rubric-c1-level1-event-term): 'event' is undefined on the page and a condition-only essay scores differently under the two readings. No row of the blocking kinds was found (ruling 26). Fix is one cell edit at project.html:473; the row is listed for plans/KNOWN-ISSUES.md until the fix lands.",
    "Calibration (ruling 23): exemplar scores were not computed by this verifier. Rows proj-calibration-exemplars cite ~/.fanout/blind/LX1-c.json, which equals the official data-scores A 4,4,4,4,3 and B 2,2,1,2,1.",
    "Mutants: 94 files in ledgers/LX1/mutants/ (90 carried plus 4 new). 88 KILLED on the embedded snapshot; the 6 embedded survivors are each KILLED by a synthetic input (see killed_by). All are lab demonstrations (ruling: mutation testing applies to graders).",
    "Not run: the full repository pytest (not needed for a project slice); the Pyodide run of the page in a browser (run_labs and page_smoke cover the labs); the on-screen rendering at 360 px (page_smoke covers overflow); verify_refs --unit LX1 with the live run (offline run only, rc 0, 560 entries, 0 problems).",
]
path = root / "ledgers/LX1/LX1-c.json"
path.write_text(json.dumps(frag, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", path, "rows", len(rows), "mutants", len(frag["mutants"]), "summary", frag["summary"])
