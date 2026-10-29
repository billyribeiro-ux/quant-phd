import json, re, sys, pathlib
from datetime import datetime, timezone
ROOT = pathlib.Path("/tmp/verify40-AC4-e")
OUT = ROOT / "ledgers/AC4/scripts/AC4-e-r40/out"
prev = json.load(open("/tmp/fanout-frags/AC4-e.round38.json", encoding="utf-8"))
CARRY_PREFIX = ("Carried from round 38 (the cited subject is byte-identical since the previous pin 81ff53b; the only "
                "course-file change in 81ff53b..b2082cc is project.html line 315, which this row does not cite): ")

# ---- rows re-verified this round (replace the round-38 row of the same id, or add) ----
NEW = {}
def row(id_, status, check, location, evidence):
    NEW[id_] = {"id": id_, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        NEW[id_]["fix"] = None  # filled below

row("proj-r38-rubric-C2-level3-monotone", "PASS",
    "Rubric C2 level 3 is at least as strict as level 2 (highest fully met level) [round-38 FAIL, fix re-verified]",
    "course/modules/AC/AC4/project.html line 315 (C2 row, column 3 Proficient, now 'Each of the four variances tied to a case figure.'); scoring rule line 308",
    "Fix verified. Round 38 FAIL: the level 3 cell read 'tied to a case figure, a named product or an input count', so a memo with zero case-tied variances could meet level 3. Now level 3 requires all four variances tied to a case figure (line 308 definition: the paragraph contains a number of the case or a number computed from them and shown). Enumeration (python -I, this round): k = number of variances tied, levels by the C2 descriptors [k<=1 -> 1; k=2,3 -> 2; k=4 -> 3]; the sequence [1, 1, 2, 2, 3] is non-decreasing, so the scoring rule is monotone on the level 2 and 3 cells. Level 4 (line 315 column 4) requires each variance tied to a named product and a case figure, which implies the level 3 condition. Witness re-run: four named-product paragraphs with no numbers meet no tie condition, score 1.")
row("proj-rubric-exhaustive", "PASS",
    "Rubric rows cover every criterion with four levels; C2 level cells are exhaustive",
    "course/modules/AC/AC4/project.html lines 312-318 (rubric table)",
    "Read in full this round (lines 312-318). Each criterion row has four td cells. C2 cells (line 315) now partition the tie count: 4 tied -> level 3 (and level 4 if named products and separation hold), 2-3 tied -> level 2, 0-1 tied -> level 1 (enumeration in proj-r38-rubric-C2-level3-monotone). C4 levels 1-2 cover zero actions, some-but-not-all, and all actions without observation; the zero-action case is fixed by line 308.")
row("proj-rubric-C2-terms", "PASS",
    "C2 rubric terms match the scoring rule",
    "course/modules/AC/AC4/project.html line 308 (scoring rule terms) and lines 315, 343-346",
    "Terms in the C2 cells: 'tied to a case figure' (level 2, level 3, level 4 cells) and 'named product' (level 4 cell only) are defined at line 308 before use. The term 'input count' is defined at line 308 and is no longer used in the C2 cells after the round-38 fix; it remains defined and is used in no C2 cell (grep of project.html: line 308 only). No C2 cell uses an undefined term.")
row("proj-r30-rubric-observability", "PASS",
    "Every rubric level descriptor is observable (VERIFIER_RULES 2.6 rubric 1)",
    "course/modules/AC/AC4/project.html line 315 (C2 levels 2-3) and line 317 (C4 level 1); scoring rule line 308",
    "Re-verified this round: C2 level 2 ('At least two variances tied to a case figure.') and level 3 ('Each of the four variances tied to a case figure.') are each decided by the tie definition at line 308 (a number of the case in the paragraph that states the variance); C4 level 1 ('No recommendation, or a recommendation that names no action for any unfavourable variance it discusses.') uses the defined term 'action'. The round-38 observability defect in C2 level 3 is fixed (row proj-r38-rubric-C2-level3-monotone).")
row("proj-calib-A-scores", "PASS",
    "Exemplar A official scores and the level it reports, under the amended C2 level 3",
    "project.html line 326 (data-scores=\"2,2,2,1,2\", data-level=\"1\"); exemplar A memo lines 330-340; rubric line 315",
    "Re-scored blind against the current rubric. C1: total plus three variances with correct signs (volume +, price +; mix shown +, sign wrong), efficiency absent: level 2 (level 3 needs all four). C2: three of four variances tied (volume, price, mix), efficiency untied: level 2 (level 3 needs all four tied to a case figure; the amended cell is met only with four). C3: fixed overhead stated as fixed, input price not stated: level 2. C4: no action for either unfavourable variance: level 1. C5: three headings, body inside 300-600: level 2. Overall min = 1 = data-level. Scores 2,2,2,1,2 match.")
row("proj-r23-exemplar-scores-and-words", "PASS",
    "Exemplar official scores, levels and body length (page lines 324-386)",
    "project.html exemplar-a and exemplar-b; word count of memo-text body",
    "Re-verified this round after the line 315 change. Exemplar A scores 2,2,2,1,2 (see proj-calib-A-scores; the C2 score 2 holds under the amended cell). Exemplar B scores 4,4,3,4,4: C2 level 4 is met (each variance tied to a named product and a case figure; volume and mix separated; shares 71.4% to 80.0% and 28.6% to 20.0%), so the amended level 3 cell does not change B. Body length of both memos was not changed by the delta (lines 330-340 and 361-373 unchanged). Overall levels 1 and 3 match data-level.")
row("proj-r30-exemplars-calibration", "PASS",
    "Calibration: score both exemplars blind and compare with the annotations",
    "course/modules/AC/AC4/project.html lines 326-386; ledgers/AC4/scripts/AC4-e-r40/out/pytest_memo_page_checks.out",
    "Re-run this round: .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_memo_exemplars.py tests/test_page_checks.py -> 55 passed (exit 0; the output shows 55 progress marks and exit 0). The tests check that annotations agree with the exemplar scores. A passing test does not cover the wording of the C2 level 3 annotation; that is row proj-r40-exemplar-A-C2-level3-annotation (FAIL).")
row("proj-calib-A-annotation", "FAIL",
    "Exemplar A annotation matches the memo text and the rubric",
    "course/modules/AC/AC4/project.html lines 343-351 (exemplar A annotation); the defect is at line 346",
    "The arithmetic is re-derived and correct: volume 542,857 = 3,142,857 - 2,600,000 (flexed 1,500 units at the budgeted mix, rounded); price 180,000 and efficiency -40,000 are the lab's steps 3 and 5 (lab-AC4-project-1 twin output, run this round, exit 0); steps 1-7 give 542,857 + 180,000 - 462,857 - 40,000 = 220,000. Hand check of the mix: budget unit margins 5,000-3*200 = 4,400 and 9,000-5*200 = 8,000; flexed units 1,500*1,000/1,400 = 1,071.43 and 428.57; (1,200-1,071.43)*4,400 + (300-428.57)*8,000 = -462,857. The C1, C3, C4 and C5 annotation claims agree with the memo text. The C2 level 3 miss annotation (line 346) gives reasons that are not conditions of the level 3 descriptor; see proj-r40-exemplar-A-C2-level3-annotation.")
row("proj-r40-exemplar-A-C2-level3-annotation", "FAIL",
    "Exemplar A 'Misses C2 level 3' annotation gives only reasons that the level 3 descriptor (line 315) contains",
    "course/modules/AC/AC4/project.html line 346 (Misses C2 level 3) against line 315 (level 3 cell), line 308 (tied definition) and line 345 (Meets C2 level 2)",
    "Witness from the page: line 346 says the level 3 miss is because 'the mix variance is explained by a wrong statement (...) and the efficiency variance is not tied to anything. The Result and Recommendation also infer that the plant can sell more ... no figure in the case tests either inference.' The amended level 3 descriptor is 'Each of the four variances tied to a case figure.' Under line 308 a variance is tied when its paragraph contains a number of the case or a computed one shown in the memo; the mix paragraph contains 462,857, so the mix variance is tied. The annotation at line 345 says the same ('the mix variance is tied to the magnitude of the computed mix shift, 462,857 cents'), so line 346 contradicts line 345. The mix-explanation clause and the Result/Recommendation inference sentence are not level 3 conditions of C2 (they bear on the factual correctness of the memo, not on the tie count). Only efficiency being untied is a level 3 miss under the descriptor. The level 3 score (2) is right; the stated reasons are wrong.",
    )
row("proj-banned-phrases", "PASS",
    "No banned phrase in the changed text or the cards",
    "course/modules/AC/AC4/project.html (whole file); course/modules/AC/AC4/cards.json",
    "Re-run this round: grep -n -i for 'roughly half', 'about 6%', 'historically', '...' and the ellipsis character over project.html and cards.json: no matches. Process words grep (builder, verifier, round) over project.html: no match.")
row("proj-r15-no-banned-phrases-changed-lines", "PASS",
    "Banned phrases in the changed lines and new grader comments",
    "course/modules/AC/AC4/project.html (whole file scan this round); line 315 (the one changed line)",
    "Whole-file scan re-run this round (see proj-banned-phrases). The one line changed since the pin (315) contains none of the banned phrases.")
row("proj-r38-banned-and-process-scan", "PASS",
    "Round-38 banned-phrase and process-word scan, re-run on the current pin",
    "course/modules/AC/AC4/project.html; course/modules/AC/AC4/cards.json",
    "Re-run this round on b2082cc: no matches (see proj-banned-phrases).")
row("proj-check-pages", "PASS", "check_pages passes for AC4",
    "course/modules/AC/AC4/*.html and cards.json",
    "Re-run this round: .venv/bin/python tools/check_pages.py --all -> output contains 'check_pages AC4: PASS' and 'exit 0' (ledgers/AC4/scripts/AC4-e-r40/out/check_pages.out).")
row("proj-check-dag", "PASS", "check_dag passes for AC4",
    "course/modules/AC/AC4/",
    "Re-run this round: tools/check_dag.py --all -> 'check_dag AC4: PASS', exit 0 (out/check_dag.out).")
row("proj-check-projects", "PASS", "check_projects passes for AC4",
    "course/modules/AC/AC4/project.html",
    "Re-run this round: tools/check_projects.py --all -> 'check_projects AC4: PASS', exit 0 (out/check_projects.out).")
row("proj-page-smoke", "PASS", "page_smoke passes for the project page in Chromium",
    "course/modules/AC/AC4/project.html",
    "Re-run this round: tools/page_smoke.py --unit AC4 --pages project.html -> 'page_smoke AC4: PASS', exit 0 (out/page_smoke_project.out). Not a driven browser UI check of the rubric form.")
row("proj-ruff-mypy", "PASS", "ruff and mypy pass on the AC4 grader and labs and on the repository",
    "course/modules/AC/AC4/grader; tests/labs/AC4",
    "Re-run this round: ruff check . -> 'All checks passed!' exit 0; ruff format --check . -> '220 files already formatted' exit 0; mypy --no-incremental -> 'Success: no issues found in 153 source files' exit 0 (out/ruff_check.out, ruff_format.out, mypy.out).")
row("proj-run-labs-ac4", "PASS", "run_labs passes for every AC4 lab including the two project labs",
    "tests/labs/AC4 via tools/run_labs.py --unit AC4",
    "Re-run this round: tools/run_labs.py --unit AC4 -> 'run_labs AC4: PASS (10/10)', exit 0 (out/run_labs.out). Also tests/labs/AC4/lab-AC4-project-1.py and lab-AC4-project-2.py run under python -I -W error: exit 0, last line 'step 8 four variances sum to total: True' (out/twin_project1.out, twin_project2.out).")
row("proj-run-graders-ac4", "PASS", "run_graders passes for AC4 on seeds 0-49, including the starter-fails check",
    "course/modules/AC/AC4/grader",
    "Re-run this round: tools/run_graders.py --unit AC4 --seeds 0-49 -> 'run_graders AC4: PASS (reference 50/50 seeds, slowest 0.3 s)', exit 0 (out/run_graders.out).")
row("proj-collect-count", "PASS", "The page's grading-mode count equals the real collect-only count on every seed",
    "course/modules/AC/AC4/grader/test_project.py; course/modules/AC/AC4/project.html line 265",
    "Re-run this round in a workspace built by run_graders.workspace with the reference solution (ledgers/AC4/scripts/AC4-e-r40/collect_ws40.py -> out/collect_ws40.out): '563 tests collected', rc 0. The bare pytest --collect-only on grader/ fails with ModuleNotFoundError: budget_engine (out/collect_ac4.out, exit 2), which is the harness design (the reference is copied to budget_engine.py per run), not a grader defect. Page line 265 states 563 checks.")
row("proj-r12-count-matches-page", "PASS", "The count on the page equals the collected count for every seed",
    "course/modules/AC/AC4/project.html line 265; grader/test_project.py",
    "Re-run this round: page line 265 '563 checks' equals the workspace collection count 563 (out/collect_ws40.out). Collection count is independent of the seed (the parametrised tests are fixed at range(50) and the seed affects only the instance values); seeds 3, 29 and 49 were checked in round 38 under the same suite.")
row("proj-r15-grader-count-527", "PASS", "Grader count stated on the page is the collected count (historical check text said 527; current page says 563)",
    "course/modules/AC/AC4/project.html line 265; grader/test_project.py",
    "The row's check text is historical (the page count was 527 in round 15). The current page line 265 states 563 checks and the workspace collection is 563 (out/collect_ws40.out). PASS for the current page; the historical wording is not on the page.")
row("proj-r30-collect-563", "PASS", "Collected count 563 re-verified on the current pin",
    "course/modules/AC/AC4/grader/test_project.py; ledgers/AC4/scripts/AC4-e-r40/out/collect_ws40.out",
    "Re-run this round: 563 tests collected (out/collect_ws40.out, rc 0).")
row("proj-autograder-rerun-mutants-m01-m37", "PASS", "Every committed top-level mutant is killed by the current grader",
    "ledgers/AC4/mutants/*.py (157 top-level files before this round; 161 after the round-40 additions)",
    "Re-run in round 40: tools/mutate_graders.py --unit AC4 --seeds 0-49 -> 'mutate_graders AC4: PASS (157/157 killed)', exit 0 (out/mutate_ac4.out). Round-40 additions r40e_01..r40e_04 are killed on seed 0 (out/new_r40e_mutants.out). The round-38 figure 153 was the count at that pin; the r38e files are now in the directory and are killed.")
row("proj-mutant-descriptions", "PASS", "Every mutant in the list has a description that names the student error",
    "ledgers/AC4/mutants/ (161 top-level files)",
    "Top-level files: each KILLED line in out/mutate_ac4.out and out/new_r40e_mutants.out prints a student-error docstring first line; none is '(no description)'. The six AC4-e-r23 subdirectory grader mutants do NOT: their first docstring line is the reference header (out/subdir_fx23_mutants.out), so they name no student error. See proj-r40-fx23-subdir-mutants (FAIL).")
row("proj-r14-mutants-all-rerun", "PASS", "Every committed mutant is re-run on seeds 0-49 by the current grader",
    "ledgers/AC4/mutants (top-level *.py, 161 files this round)",
    "Re-run this round on seeds 0-49: 157/157 top-level killed (out/mutate_ac4.out); the 4 new r40e files killed (out/new_r40e_mutants.out). Subdirectory mutants: see proj-r40-fx23-subdir-mutants and the lab-twin note in notes.")
row("proj-r15-mutants-all-rerun", "PASS", "Every top-level AC4 mutant killed on seeds 0-49",
    "ledgers/AC4/mutants/*.py (161 top-level files this round)",
    "Re-run this round: all 157 top-level files KILLED on seeds 0-49 (out/mutate_ac4.out, exit 0), plus r40e_01..04 KILLED (out/new_r40e_mutants.out).")
row("proj-r17-mutant-docstrings", "PASS", "Each mutant module has a docstring naming the student error",
    "ledgers/AC4/mutants/*.py (161 top-level files)",
    "The mutate tool takes the first docstring line as the description (tools/mutate_graders.py line 49); every KILLED line in out/mutate_ac4.out and out/new_r40e_mutants.out carries a non-empty description.")
row("proj-r38-mutants-all-rerun-count", "PASS", "Round-38 mutant count rows re-run: top-level 157 killed, subdirectory AC4-e-r23 6 killed",
    "ledgers/AC4/mutants/*.py (157 top-level at this pin, +4 r40e = 161); ledgers/AC4/mutants/AC4-e-r23/ (6 files)",
    "Re-run this round: 157/157 top-level KILLED (out/mutate_ac4.out) and the 6 AC4-e-r23 grader mutants KILLED (out/subdir_fx23_mutants.out).")
row("proj-r38-mutants-new-student-errors", "PASS", "Round-38 student-error mutants (r38e_01, 03, 04, 05) are killed",
    "ledgers/AC4/mutants/r38e_01_volume_variance_reported_as_magnitude.py; r38e_03; r38e_04; r38e_05 (r38e_02 is equivalent and out of the list)",
    "Re-run this round: each r38e file is among the KILLED lines of out/mutate_ac4.out (157/157 killed).")
row("proj-r40-mutants-new-student-errors", "PASS",
    "Four new student-error mutants written this round are each killed by the suite on seeds 0-49",
    "ledgers/AC4/mutants/r40e_01_flexed_variable_cost_truncated_revenue_rounded.py; r40e_02_efficiency_standard_on_budgeted_units.py; r40e_03_master_profit_forgets_fixed_overhead.py; r40e_04_no_budgeted_units_check_missing.py (made by ledgers/AC4/scripts/AC4-e-r40/make_r40e.py)",
    "Each is a full module derived from reference.py with one student error (docstring names it). Killed on seed 0 by the suite (out/new_r40e_mutants.out): r40e_01 truncates the flexed variable cost (floor) while revenue is rounded to the nearest cent; r40e_02 takes the standard inputs of budgeted units in the efficiency variance; r40e_03 leaves fixed overhead out of the master profit; r40e_04 drops the 'no budgeted units' refusal, so flexed budgets divide by zero. Each is a plausible student error; none is an equivalent mutant (each changes a value the suite checks).")
row("proj-r40-fx23-subdir-mutants", "FAIL",
    "The six grader mutants stored in ledgers/AC4/mutants/AC4-e-r23/ (fx23_01..06) are killed",
    "ledgers/AC4/mutants/AC4-e-r23/fx23_01..fx23_06 (the mutate tool globs only top-level files, so these were run by ledgers/AC4/scripts/AC4-e-r40/run_subdir_mutants.py)",
    "Re-run this round: all six KILLED on seed 0 (out/subdir_fx23_mutants.out), so the grader does catch them. Defect: each file's docstring is the reference header 'Reference solution for the AC4 budget and variance engine (budget_engine.py).' and names no student error, which the mutant ledger requires. Fix: give each of ledgers/AC4/mutants/AC4-e-r23/fx23_01..06 a docstring whose first line names the student error (as the top-level mutants do), or move them out of the mutants directory.")
row("proj-r40-alternatives-correct", "PASS",
    "Three further spec-correct alternatives pass the whole suite on seeds 0-49 (over-constraint check)",
    "ledgers/AC4/scripts/AC4-e-r40/alts/alt40_a_decimal_half_up.py; alt40_b_floor_of_plus_half.py; alt40_c_strict_int_type_check.py",
    "a: nearest cent via Decimal quantize with ROUND_HALF_UP; b: nearest cent as math.floor(amount + 1/2) on exact Fractions; c: whole numbers checked with type(value) is int (the only change, so int subclasses and bools are refused). All three SURVIVED the suite (no failure on any seed 0-49), i.e. they pass (out/alts40.out). None of the three is over-constrained by the suite.")
row("proj-hours", "PASS", "Declared project hours match the hub split and lesson hours",
    "course/modules/AC/AC4/project.html lines 277-285 (time-budget table); course/modules/AC/AC4/index.html line 29",
    "Carried from round 38 with a check of the current pin: lines 277-285 and index.html are not in the 81ff53b..b2082cc course delta (only project.html line 315 changed). Re-derived: hub split 50 lesson hours + 20 project hours; the time table sums to 20 (round 38 row proj-r13-hours-split).")

# ---- overrides for rows whose counts or subject changed ----
row("proj-mutant-descriptions", "FAIL",
    "Every mutant in the list has a description that names the student error",
    "ledgers/AC4/mutants/ (161 top-level files) and ledgers/AC4/mutants/AC4-e-r23/fx23_01..06",
    "Top-level files: every KILLED line in out/mutate_ac4.out and out/new_r40e_mutants.out prints a student-error first docstring line. The six AC4-e-r23 subdirectory grader mutants do not: their first docstring line is the reference header (out/subdir_fx23_mutants.out), so they name no student error.")
NEW["proj-mutant-descriptions"]["fix"] = "Give each ledgers/AC4/mutants/AC4-e-r23/fx23_01..06 a docstring whose first line names the student error (as the top-level mutants do), or move the files out of the mutants directory."
row("proj-r17-mutants-all-rerun", "PASS", "Every mutant in ledgers/AC4/mutants is re-run on seeds 0-49 (count re-stated)",
    "ledgers/AC4/mutants/*.py (161 top-level files this round)",
    "Re-run this round: 157 of 157 pre-existing top-level mutants KILLED on seeds 0-49 (out/mutate_ac4.out, exit 0); r40e_01..04 KILLED (out/new_r40e_mutants.out). The 'all' claim covers top-level files only, which is what tools/mutate_graders.py globs; the subdirectory files are handled in proj-r40-fx23-subdir-mutants and the lab-twin note.")
row("proj-r30-mutants-top-level", "PASS", "Top-level mutants all killed (count re-stated for the current pin)",
    "ledgers/AC4/mutants/*.py (157 top-level at the round-38 pin; 161 with the round-40 additions)",
    "Re-run this round: 157/157 KILLED (out/mutate_ac4.out) and the 4 round-40 additions KILLED (out/new_r40e_mutants.out).")

FAIL_R40 = None
mut_rows = [l for l in (OUT / "mutate_ac4.out").read_text().splitlines() if l.startswith("KILLED") or l.startswith("SURVIVED")]
pat = re.compile(r"^(KILLED|SURVIVED) (\S+): (.*) -> (.*)$")
mutants = []
for l in mut_rows:
    m = pat.match(l)
    assert m, l
    status, name, desc, killed = m.groups()
    mutants.append({"file": f"ledgers/AC4/mutants/{name}", "description": desc, "killed_by": killed + (" [KILLED]" if status == "KILLED" else " [SURVIVED]")})
for l in (OUT / "new_r40e_mutants.out").read_text().splitlines():
    m = pat.match(l)
    assert m, l
    status, name, desc, killed = m.groups()
    mutants.append({"file": f"ledgers/AC4/mutants/{name}", "description": desc, "killed_by": killed + (" [KILLED]" if status == "KILLED" else " [SURVIVED]")})
for l in (OUT / "subdir_fx23_mutants.out").read_text().splitlines():
    m = pat.match(l)
    assert m, l
    status, name, desc, killed = m.groups()
    mutants.append({"file": f"ledgers/AC4/mutants/AC4-e-r23/{name}", "description": desc, "killed_by": killed + (" [KILLED]" if status == "KILLED" else " [SURVIVED]")})
killed_n = sum(1 for m in mutants if m["killed_by"].endswith("[KILLED]"))
survived_n = len(mutants) - killed_n
assert survived_n == 0, survived_n
# the mutants list keeps every earlier mutant listed in round 38 as a killed entry (ids are file names)

NEW["proj-calib-A-annotation"]["fix"] = "Make the exemplar A annotation consistent with the rubric: see proj-r40-exemplar-A-C2-level3-annotation (line 346)."
NEW["proj-r40-exemplar-A-C2-level3-annotation"]["fix"] = "In project.html line 346 (Misses C2 level 3) state only the failing condition: the efficiency variance is not tied to a case figure (line 308 definition). Delete the mix-explanation clause and the Result/Recommendation inference sentence; line 345 already counts the mix variance as tied."
NEW["proj-r40-fx23-subdir-mutants"]["fix"] = "Give each ledgers/AC4/mutants/AC4-e-r23/fx23_01..06 a docstring whose first line names the student error, or move the files out of the mutants directory."
# ---- assemble rows ----
REPL = [("Re-run this round", "Re-run in round 38"), ("(run this round)", "(run in round 38)")]
rows = []
seen = set()
for r in prev["rows"]:
    rid = r["id"]
    seen.add(rid)
    if rid in NEW:
        rows.append(NEW.pop(rid))
        continue
    assert r["status"] == "PASS", ("carry needs PASS", rid, r["status"])
    ev = r["evidence"]
    for a, b in REPL:
        ev = ev.replace(a, b)
    rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": "PASS",
                 "evidence": CARRY_PREFIX + ev})
for rid, r in NEW.items():
    rows.append(r)
assert not any(r["status"] not in ("PASS", "FAIL") for r in rows)
for r in rows:
    if r["status"] != "PASS":
        assert r.get("fix"), r["id"]
assert len({r["id"] for r in rows}) == len(rows)
missing_prev = [i for i in seen if i not in {r["id"] for r in rows}]
assert not missing_prev, missing_prev

pass_n = sum(r["status"] == "PASS" for r in rows)
fail_n = len(rows) - pass_n
verdict = "PASS" if fail_n == 0 else "FAIL"
now = datetime.now(timezone.utc).isoformat(timespec="seconds")
frag = {
    "unit": "AC4",
    "slice": "AC4-e",
    "round": 40,
    "verifier": "Claude Haiku 5.5 (independent verifier, round 40, slice AC4-e; did not build AC4)",
    "pin": "b2082cc",
    "base": ("81ff53b (the previous fragment on disk is /tmp/fanout-frags/AC4-e.round38.json, pinned at 81ff53b; the brief names a round-39 fragment, which is not on disk, so the delta was computed from 81ff53b). Carried rows use the prefix 'Carried from round 38'."),
    "checkout": "/tmp/verify40-AC4-e",
    "scratch": "/tmp/ac4-v/AC4-e",
    "verified_at": now,
    "verdict": verdict,
    "rows": rows,
    "mutants": mutants,
    "registry_flags": prev["registry_flags"],
    "freshness_flags": prev["freshness_flags"],
    "notes": open(sys.argv[1], encoding="utf-8").read().strip() if len(sys.argv) > 1 else "",
    "summary": {"rows": len(rows), "pass": pass_n, "fail": fail_n, "unverifiable": 0,
                "mutants": len(mutants), "mutants_killed": killed_n, "mutants_survived": survived_n},
}
dest = ROOT / "ledgers/AC4/AC4-e.json"
dest.write_text(json.dumps(frag, ensure_ascii=False, indent=1), encoding="utf-8")
print("rows", len(rows), "pass", pass_n, "fail", fail_n, "verdict", verdict, "mutants", len(mutants), "killed", killed_n)
