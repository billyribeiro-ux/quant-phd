"""Build the round-6 delta fragment for M5 slice d from the fresh outputs of this round (pin e896b7a4).

Rows carried from earlier rounds name their subject and its byte-identity since the previous pin dde0486b.
Usage: build_fragment_r6.py <repo-root>
"""
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(sys.argv[1])
OUT = REPO / "ledgers/M5/scripts/M5-d-r6/out"
prev = json.loads(Path("/Users/billyribeiro/.fanout/frags/S-M5-d.round5.json").read_text(encoding="utf-8"))
prev_rows = {r["id"]: r for r in prev["rows"]}


def carried(n: int, files: str, text: str) -> str:
    return (f"Carried from round {n} ({files} byte-identical since the previous pin dde0486b; "
            f"unchanged across e896b7a4): {text}")


def row(rid: str, check: str, location: str, status: str, evidence: str) -> dict:
    return {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}


rows: list[dict] = []
# Fresh evidence this round (commands run at e896b7a4 in this checkout; outputs under scripts/M5-d-r6/out/).
rows.append(row("M5-d-r1-01", "2.6-autograder-reference", "course/modules/M/M5/grader/reference.py", "PASS",
    "Fresh: tools/run_graders.py --unit M5 --seeds 0-49 -> 'run_graders M5: PASS (reference 50/50 seeds, slowest 0.3 s)' "
    "(out/run_graders_M5_0-49.out, rc 0). Scratch workspace with reference.py as contraction_solver.py: "
    "QF_SEED=0 pytest --collect-only -q test_project.py -> '101 tests collected' (out/collect_only.out); "
    "QF_SEED=0 pytest --assert=plain -W error -> '101 passed'. Seeds 0-9 rc 0 each "
    "(out/seeds_and_docs_r6.out, 'reference: [0, 0, ... 0]')."))
rows.append(row("M5-d-r1-02", "2.6-instances", "course/modules/M/M5/grader/instance.py", "PASS",
    carried(4, "grader/instance.py", "round 4 ran ledgers/M5/scripts/M5-d-r2/d2_instances.py under python -I: invalid seeds [], "
    "15 betas, 27 alphas, 17 sizes, 50 distinct solved vectors; docstring ranges (lines 5-12) match code (lines 44-53). "
    "Not re-run this round; the file is unchanged.")))
rows.append(row("M5-d-r1-03", "2.6-mutation-existing", "ledgers/M5/mutants/ (141 files at this pin)", "PASS",
    "Fresh: .venv/bin/python tools/mutate_graders.py --unit M5 --seeds 0-9 -> 'mutate_graders M5: PASS (141/141 killed)', "
    "rc 0 (out/mutate_M5_0-9.out: 141 KILLED lines, no survivor). The 3 round-5 mutants and the 3 new round-6 mutants are included."))
rows.append(row("M5-d-r1-04", "2.6-mutation-new-killed",
    "ledgers/M5/mutants/d1_02_continuation_reads_the_current_state.py; d1_03_value_is_the_penultimate_iterate.py", "PASS",
    "Fresh: out/mutate_M5_0-9.out -> 'KILLED d1_02 ... -> test_operator_matches_its_definition[0] (seed 0)'; "
    "'KILLED d1_03 ... -> test_certified_error_bounds_the_distance_to_the_fixed_point[0] (seed 0)'. "
    "grader/test_project.py unchanged since dde0486b."))
rows.append(row("M5-d-r1-05", "2.6-mutation-survivor",
    "course/modules/M/M5/grader/test_project.py:739-753; ledgers/M5/mutants/d1_01_top_grid_point_never_a_successor.py", "PASS",
    "Fresh: out/mutate_M5_0-9.out -> 'KILLED d1_01 ... -> test_operator_uses_the_top_point_on_a_grid_inside_zero_one (seed 0)'. "
    "test_project.py unchanged since dde0486b."))
rows.append(row("M5-d-r1-06", "2.6-alternatives",
    "ledgers/M5/alternatives/alt1..alt5; ledgers/M5/alternatives/not_accepted/; plans/M5-build-plan.md:304-309; "
    "plans/M5-open-items.md:16-20; course/modules/M/M5/project.html:244-246", "PASS",
    "Re-verified from scratch under ruling 31. Fresh: scripts/M5-d-r6/alt_seeds_r6.py -> alt1..alt5 50/50 seeds each, first failure None; "
    "not_accepted/alt1_gauss_seidel_in_place.py and alt2_residual_stop.py 0/50 each, first failure at seed 0 on "
    "test_certified_error_is_beta_over_one_minus_beta_times_the_last_change[1-0] (out/alt_seeds_0-49.out). "
    "The page: project.html:244 'Each sweep is synchronous'; project.html:245 certified error beta/(1-beta) times the last change; "
    "project.html:246 stop at the first sweep with certified error at most tol. Amended plan text (M5-build-plan.md:304-309) and "
    "open-items decision 3 (lines 16-20) state the same contract and name the same two rejected variants. alt5 reads values "
    "only from the previous vector (out is a new list). The ruling's path for the not_accepted files is checked in M5-d-r6-01 "
    "and the plan section 1 sentence in M5-d-r6-02."))
rows.append(row("M5-d-r1-07", "2.6-failure-message-leak", "course/modules/M/M5/grader/test_project.py (every expect/must_raise/pytest.fail message)", "PASS",
    carried(4, "grader/test_project.py", "the file is unchanged, and round 4 read every assertion message in it: none states the expected "
    "formula, constant or branch in terms the learner can copy.")))
rows.append(row("M5-d-r1-08", "2.6-mutant-descriptions", "ledgers/M5/mutants/ (141 files)", "PASS",
    "Fresh: ast.get_docstring on all 141 mutant files, empty list (out/seeds_and_docs_r6.out: 'mutant files: 141; empty docstrings: []')."))
rows.append(row("M5-d-r1-09", "2.6-test-count", "course/modules/M/M5/project.html:235 ('Grading mode', 101 checks); grader/test_project.py", "PASS",
    "Fresh: collect-only in scratch -> '101 tests collected' (out/collect_only.out); project.html:235 reads 'runs 101 checks with warnings as errors'; "
    "reference 101 passed."))
for rid, check, loc, n, files, text in [
    ("M5-d-r1-10", "2.6-browser-suite", "course/modules/M/M5/project.html:272-281; course/assets/js/grader.js:34-61; course/assets/js/store.js; course/assets/js/py-worker.js:111", 5,
     "course/modules/M/M5/project.html and course/assets/**", "round 5 read project.html:272 'is saved in this browser as you type' against grader.js:34 (load) and :61 (save); the assets are unchanged (git diff dde0486b..e896b7a4 -- course/assets is empty)."),
    ("M5-d-r1-11", "2.6-rubric-observable", "course/modules/M/M5/project.html:404-412 (rubric cells C1-C6)", 5,
     "course/modules/M/M5/project.html", "the rubric cells are unchanged at this pin (project.html has no delta)."),
    ("M5-d-r1-12", "2.6-rubric-caption", "course/modules/M/M5/project.html:403-404", 5,
     "course/modules/M/M5/project.html", "the caption is unchanged at this pin."),
]:
    rows.append(row(rid, check, loc, "PASS", carried(n, files, text)))
for rid, loc, extra in [
    ("M5-d-r1-13", "course/modules/M/M5/project.html:419-449 (data-scores 2,2,1,2,2,2)", "Exemplar A"),
    ("M5-d-r1-14", "course/modules/M/M5/project.html:451-481 (data-scores 4,4,4,4,4,3)", "Exemplar B"),
    ("M5-d-r3-43", "course/modules/M/M5/project.html:419-482 (annotations)", "Exemplar A and B annotations"),
]:
    rows.append(row(rid, "2.6-calibration-" + ("exemplar-A" if extra.startswith("Exemplar A") and "43" not in rid else
                    "exemplar-B" if "14" in rid else "exemplar-descriptor-exclusivity"), loc, "PASS",
        "Calibration row (ruling 23), accepted (ruling 31 context; task text). Blind scores in ~/.fanout/blind/M5-d.json: "
        "A = [2,1,1,2,2,1], B = [4,3,4,3,3,3] (read this round). Official scores (project.html data-scores): A = [2,2,1,2,2,2], "
        "B = [4,4,4,4,4,3]. Differences are one level: A C2 and C6 (1 vs 2), B C2, C4, C5 (3 vs 4). plans/KNOWN-ISSUES.md "
        "'Rubric calibration' table (lines 28-38 at this pin) records these exact differences for M5 A and M5 B, accepted by the "
        "architect. " + extra + " PASS within one level."))
rows.append(row("M5-d-r1-15", "2.6-hours-arithmetic", "course/modules/M/M5/project.html:33, 258-264; course/modules/M/M5/index.html:29, 39-42, 131; curriculum/curriculum.json (M5 hours 130)", "PASS",
    carried(5, "project.html, index.html and curriculum/curriculum.json", "the project table rows 1+2+8+7+3+5 = 26 (line 264), 26/130 = 20.0 %; the delta has no hunk in these files.")))
rows.append(row("M5-d-r1-16", "2.6-labs", "course/modules/M/M5/project.html:55-220, 287-390; tests/labs/M5/lab-M5-project-1..3.py", "PASS",
    "Fresh: tools/run_labs.py --unit M5 --page project -> 'run_labs M5: PASS (3/3)' (out/run_labs_M5_project.out, rc 0). Each twin run "
    "alone with .venv/bin/python -I -W error exits 0 (lab-M5-project-1: 14 lines, -2: 4 lines, -3: 16 lines). The three project twins "
    "and project.html have no delta since dde0486b."))
for rid, loc, text, n in [
    ("M5-d-r1-17", "course/modules/M/M5/project.html:57, 58-155", "the rung-1 numbers are unchanged; round 5 re-derived them with scripts/M5-d-r5/numbers.py.", 5),
    ("M5-d-r1-18", "course/modules/M/M5/project.html:159-222", "the filled Lab 2 ratio 0.3 is unchanged; round 5 re-derived it.", 5),
    ("M5-d-r1-19", "course/modules/M/M5/project.html:289, 293-298, 365, 373-388", "the Lab 3 gap 0.021828872 and the tie check are unchanged; round 5 re-derived them with numbers3.py.", 5),
    ("M5-d-r1-20", "course/modules/M/M5/project.html:393-399 (brief A1-A4); Conventions 244-248", "the proof brief is unchanged; round 5 re-derived A1-A4.", 5),
    ("M5-d-r1-21", "course/modules/M/M5/project.html:240-248; grader/reference.py:34-78; grader/test_project.py:618-785", "each named invalid-input condition has a branch in reference.py and a test in both directions; reference.py and the test file are unchanged.", 5),
    ("M5-d-r1-22", "course/modules/M/M5/grader/starter.py:18,23; grader/reference.py:94,101; project.html:231", "the signatures are unchanged.", 5),
    ("M5-d-r1-23", "course/modules/M/M5/project.html:233; course/assets/js/python.js:4", "TIMEOUT_MS = 120000 in python.js (assets unchanged).", 5),
    ("M5-d-r1-24", "course/modules/M/M5/project.html (all math); notation/notation.json", "the notation registry and the page's symbols are unchanged (notation/ and project.html have no delta).", 5),
    ("M5-d-r1-25", "course/modules/M/M5/project.html:229; course/modules/M/M5/grader/instance.py:3, 41, 56", "the SIMULATED statements are unchanged.", 5),
    ("M5-d-r1-26", "course/modules/M/M5/project.html (no data-files attribute)", "no data-files attribute at this pin.", 5),
    ("M5-d-r1-27", "course/modules/M/M5/project.html", "no live figure; the page is unchanged.", 5),
    ("M5-d-r1-30", "course/modules/M/M5/project.html:40-49, 223-250, 270-281, 283-288, 491-498", "the section order is unchanged.", 5),
    ("M5-d-r1-31", "course/modules/M/M5/grader/instance.py:3; project.html:229", "instance and page statements unchanged.", 5),
    ("M5-d-r1-32", "course/modules/M/M5/project.html:156, 219, 389", "the interpretive claims are unchanged; round 5 checked them against the printed lines.", 5),
    ("M5-d-r3-42", "course/modules/M/M5/project.html:404-412 (rubric C5 row, line 410)", "the C5 level text is unchanged since round 5 fixed it.", 5),
    ("M5-d-r4-45", "course/modules/M/M5/grader/test_project.py:559-562", "the docstring of test_stop_uses_the_largest_absolute_change_over_the_grid matches its assertion; the file is unchanged.", 5),
    ("M5-d-r4-47", "course/modules/M/M5/project.html:142, 215, 372 (data-tolerance 1e-15); course/assets/js/labs.js:50", "data-tolerance is 1e-15 on all three experiments; the page and labs.js are unchanged.", 5),
    ("M5-d-r4-49", "course/modules/M/M5/project.html (learner text)", "the learner-text scan of round 5 stands; the page is unchanged.", 5),
]:
    rows.append(row(rid, prev_rows[rid]["check"], loc, "PASS", carried(n, "project.html and the cited M5 files", text)))
rows.append(row("M5-d-r2-33", prev_rows["M5-d-r2-33"]["check"], "ledgers/M5/mutants/d3_01_feasibility_allows_a_tie_tolerance_of_1e-12.py; course/modules/M/M5/grader/test_project.py:444-460", "PASS",
    "Fresh: out/mutate_M5_0-9.out -> 'KILLED d3_01 ...' (rc 0 gate); test_project.py unchanged since dde0486b."))
rows.append(row("M5-d-r2-34", prev_rows["M5-d-r2-34"]["check"], "ledgers/M5/mutants/d3_02_first_point_bound_checked_only_for_longer_grids.py; course/modules/M/M5/grader/test_project.py:721-726", "PASS",
    "Fresh: out/mutate_M5_0-9.out -> 'KILLED d3_02 ...'; test_project.py unchanged since dde0486b."))
rows.append(row("M5-d-r2-35", prev_rows["M5-d-r2-35"]["check"], "ledgers/M5/mutants/d3_03_value_is_the_penultimate_iterate_when_the_budget_runs_out.py", "PASS",
    "Fresh: out/mutate_M5_0-9.out -> 'KILLED d3_03 ...'."))
rows.append(row("M5-d-r2-36", "2.6-dag", "course/modules/M/M5/project.html:37, 227, 494, 501 (concept links and prose); curriculum/curriculum.json (M5 prereqs ['M2'])", "PASS",
    "Fresh: tools/check_dag.py --unit M5 -> 'check_dag M5: PASS' (out/check_dag_M5.out, rc 0). The page has no delta; curriculum/ has no delta."))
rows.append(row("M5-d-r2-37", prev_rows["M5-d-r2-37"]["check"], "course/modules/M/M5/project.html:223-250", "PASS",
    carried(5, "project.html", "the spec (inputs, outputs, constraints) is unchanged at this pin; read at lines 223-250 this round.")))
rows.append(row("M5-d-r2-38", "2.6-atlas-studio", "curriculum/curriculum.json (M5 entry); plans/M5-build-plan.md:408 (was :402 before the +6-line amendment at 301-315; text byte-identical)", "PASS",
    "Fresh: 'No Atlas milestone. No Atlas entry names M5 ... The project has no atlas key.' is the same text at plans/M5-build-plan.md:408 (sed -n 408p at e896b7a4; sed -n 402p at dde0486b). curriculum/ has no delta."))
rows.append(row("M5-d-r3-39", prev_rows["M5-d-r3-39"]["check"], "ledgers/M5/mutants/r3_01_operator_clamps_each_image_at_zero.py; course/modules/M/M5/grader/test_project.py:121-141", "PASS",
    "Fresh: out/mutate_M5_0-9.out -> 'KILLED r3_01 ...'; test_project.py unchanged since dde0486b."))
rows.append(row("M5-d-r3-40", prev_rows["M5-d-r3-40"]["check"], "ledgers/M5/mutants/r3_02_continuation_uses_absolute_value.py; course/modules/M/M5/grader/test_project.py:121-141", "PASS",
    "Fresh: out/mutate_M5_0-9.out -> 'KILLED r3_02 ...'; test_project.py unchanged since dde0486b."))
rows.append(row("M5-d-r3-41", prev_rows["M5-d-r3-41"]["check"], "ledgers/M5/mutants/r3_03_feasibility_tie_tolerance_of_1e-14.py; course/modules/M/M5/grader/test_project.py:463-479", "PASS",
    "Fresh: out/mutate_M5_0-9.out -> 'KILLED r3_03 ...'; test_project.py unchanged since dde0486b."))
rows.append(row("M5-d-r4-44", prev_rows["M5-d-r4-44"]["check"], "ledgers/M5/alternatives/alt1..alt5; ledgers/M5/alternatives/not_accepted/", "PASS",
    "Fresh: scripts/M5-d-r6/alt_seeds_r6.py -> alt1..alt5 50/50 seeds each (out/alt_seeds_0-49.out). The alternatives are synchronous (alt5 out list built from values, project.html:244)."))
rows.append(row("M5-d-r4-46", prev_rows["M5-d-r4-46"]["check"], "ledgers/M5/mutants/r4_01..r4_04 (round 4); r5_01..r5_03 (round 5); r6_01..r6_03 (round 6)", "PASS",
    "Fresh: out/mutate_M5_0-9.out -> r4_01..r4_04 KILLED. Per-seed (out/seeds_and_docs_r6.out): r5_01, r5_02, r5_03 each killed on 10/10 seeds (rc 1 on every seed); "
    "r6_01, r6_02, r6_03 each killed on 10/10 seeds. Each of the new mutants is a student error: r6_01 stops only on strict < tol; "
    "r6_02 treats a saving equal to k**alpha as infeasible; r6_03 starts value iteration from the ones vector (the page names V_0 = 0)."))
rows.append(row("M5-d-r4-48", "2.6-mutation-full-rerun", "ledgers/M5/mutants/ (141 files); tools/mutate_graders.py --unit M5 --seeds 0-9", "PASS",
    "Fresh: 'mutate_graders M5: PASS (141/141 killed)' (out/mutate_M5_0-9.out). Mutants on seeds 10-49 are not run (gate is 0-9)."))
rows.append(row("M5-d-r1-29", "2.6-lint-and-types", "course/modules/M/M5/grader; tests/labs/M5; ledgers/M5; repository", "PASS",
    "Fresh: ruff check course/modules/M/M5/grader tests/labs/M5 ledgers/M5 -> 'All checks passed!' rc 0; ruff format --check on the same scope -> '17 files already formatted' rc 0; "
    "mypy --no-incremental -> 'Success: no issues found in 385 source files' rc 0 (out/ruff_*_scope.out, out/mypy_no_incremental.out). Mutant files are excluded by pyproject extend-exclude (ledgers/*/mutants)."))
rows.append(row("M5-d-r1-28", "2.1-references", "course/modules/M/M5/project.html:500-512; references/references.json", "PASS",
    "Fresh: tools/verify_refs.py --offline -> 'offline integrity: 560 entries, 0 problems' rc 0 (out/verify_refs_offline.out). The data-cite keys at project.html:503-504 are unchanged; references/ has no delta."))
rows.append(row("M5-d-r6-01", "2.6-ruling-path", "plans/FINAL-ARCHITECT-RULINGS.md:118-120 (ruling 31: 'ledgers/M5/not_accepted/ keeps the two files'); ledgers/M5/alternatives/not_accepted/", "FAIL",
    "The binding ruling 31 names ledgers/M5/not_accepted/ for the two rejected files. That directory does not exist at e896b7a4 "
    "(ls ledgers/M5/not_accepted: No such file or directory). The files are at ledgers/M5/alternatives/not_accepted/ "
    "(alt1_gauss_seidel_in_place.py, alt2_residual_stop.py, README.md), and plans/M5-build-plan.md:309 and plans/M5-open-items.md:18-20 "
    "name that path correctly. The ruling is architect text, so this verifier does not edit it. "
    "Fix: the architect amends ruling 31's path to ledgers/M5/alternatives/not_accepted/ (or the files are moved and all three documents are kept in step)."))
rows.append(row("M5-d-r6-02", "2.6-plan-consistency", "plans/M5-build-plan.md:119-122 (section 1, 'Grader tests demand an exception type only...')", "FAIL",
    "Section 1 still says the five alternatives 'must all pass' and gives as examples 'synchronous and in-place sweeps' and 'stopping on the a-posteriori bound and on a residual with the bound reported'. "
    "Ruling 31 says the in-place sweep and the residual-bound stop are not valid alternatives of this project, and the same plan's bullet at lines 304-309 now says so. "
    "Two plan sentences contradict each other and the binding ruling. "
    "Fix: the architect (or planner) amends plans/M5-build-plan.md:119-122 to list the five accepted alternatives (alt1..alt5) and drop the in-place and residual-stop examples, as the bullet at 304-309 does."))
rows.append(row("M5-d-r6-03", "2.6-new-student-error-mutants", "ledgers/M5/mutants/r6_01_stop_only_when_certified_error_strictly_below_tol.py; r6_02_saving_must_leave_strictly_positive_consumption.py; r6_03_solve_starts_from_the_ones_vector.py", "PASS",
    "Three new student-error mutants written from grader/reference.py by scripts/M5-d-r6/make_mutants_r6.py. Per-seed kill on seeds 0-9: each rc 1 on every seed (out/seeds_and_docs_r6.out). "
    "Killing tests (seed 0, out/mutate_M5_0-9.out): r6_01 -> test_certified_error_exactly_at_tol_stops_the_first_sweep; "
    "r6_02 -> test_successor_exactly_at_the_resources_is_feasible; r6_03 -> test_certified_error_is_beta_over_one_minus_beta_times_the_last_change[1-0]. "
    "Each violates a behaviour the page states: project.html:246 'at most tol'; project.html:243 'k' is feasible when c >= 0, that is k' <= k**alpha'; project.html:244 'V_0 = 0'."))
rows = rows

# Check: every previous row id is kept, and no row is missing.
ids_now = {r["id"] for r in rows}
missing = [rid for rid in prev_rows if rid not in ids_now]
assert not missing, missing
print("rows", len(rows), "missing from previous", missing)

mut_lines = (OUT / "mutate_M5_0-9.out").read_text(encoding="utf-8").splitlines()
mutants = []
pat = re.compile(r"^KILLED (\S+?): (.*) -> (.*)$")
for ln in mut_lines:
    m = pat.match(ln)
    if m:
        mutants.append({"name": m.group(1), "description": m.group(2), "killed_by": m.group(3)})
assert len(mutants) == 141, len(mutants)

summary_counts = {s: sum(1 for r in rows if r["status"] == s) for s in ("PASS", "FAIL", "UNVERIFIABLE")}
fragment = {
    "unit": "M5",
    "slice": "d",
    "round": 6,
    "verifier": "Haiku independent verifier (round 6), delta verification from the round-5 fragment; no build context; calibration by the dedicated blind scorer (ruling 23)",
    "pin": "e896b7a45344d1bc17ebfbf7fb05d87698ec9d6a",
    "base": "8196077d5f56c3919d33e69888176d197d378ad4",
    "delta_from": "dde0486beeb0312e4ac1cc03aaa02e56644adb24",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyS6-M5-d",
    "scratch": "/Users/billyribeiro/.fanout/wt/verifyS6-M5-d/ledgers/M5/scripts/M5-d-r6 (temp workspaces under /tmp/m5d6/tmp)",
    "verified_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    "verdict": "FAIL",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Delta dde0486b..e896b7a4 for slice d: plans/FINAL-ARCHITECT-RULINGS.md (ruling 31 added), plans/M5-build-plan.md (lines 301-315), plans/M5-open-items.md (decision 3), plans/KNOWN-ISSUES.md (M5 calibration table added), ledgers/M5/mutants/r5_01..r5_03 (added to git in e896b7a4; not present at dde0486b). course/modules/M/M5/project.html, grader/, course/assets/, curriculum/, notation/, references/, tools/ and the three project lab twins have no delta.",
        "Out of slice d, observed only: tests/labs/M5/lab-M5-L05-1.py (docstring changed to [0, 1/2]) and course/modules/M/M5/L05.html, L06.html, L07.html, L08.html, L10.html, cards.json changed. The L05 twin runs under python -I -W error with exit 0 (18 output lines). Not verified against the lesson text.",
        "Ruling 31 names ledgers/M5/not_accepted/; the files are at ledgers/M5/alternatives/not_accepted/ (M5-d-r6-01).",
        "Plan section 1 (plans/M5-build-plan.md:119-122) still lists the in-place and residual-stop variants as alternatives that must pass (M5-d-r6-02).",
        "The round-5 fragment recorded the three r5 mutants as existing at pin dde0486b; git shows them added in e896b7a4 (the delta lists them as new files). Re-verified fresh here: 10/10 seeds each.",
        "Calibration: plans/KNOWN-ISSUES.md now holds the M5 rows of the blind-versus-official table; the architect acceptance is read from the table's heading ('accepted by the architect'). Numbers re-read from ~/.fanout/blind/M5-d.json.",
        "Fresh gates at e896b7a4: check_pages M5, check_dag M5, check_projects M5, run_labs M5 project, run_graders M5 0-49, page_smoke M5 project, verify_refs --offline, ruff check/format on scope, mypy --no-incremental, pytest -k M5, mutate_graders M5 0-9 (141/141).",
    ],
    "summary": (f"Round 6 delta, slice d, verdict FAIL. {len(rows)} rows: PASS {summary_counts['PASS']}, FAIL {summary_counts['FAIL']}, "
                f"UNVERIFIABLE {summary_counts['UNVERIFIABLE']}. Previous FAIL M5-d-r1-06 is now PASS (ruling 31 and the amended plan "
                "bullet and open-items match the page; the two rejected variants fail 50/50 seeds as before). New FAILs: "
                "M5-d-r6-01 (ruling 31 path ledgers/M5/not_accepted/ does not exist) and M5-d-r6-02 (plan section 1 lines 119-122 "
                "still says the in-place and residual-stop variants must pass). 141/141 mutants killed; 3 new student-error mutants killed 10/10 seeds; "
                "alt1..alt5 50/50; not_accepted 0/50 each; 101 tests collected and passed; all gates PASS."),
    "what_not_checked": [
        "Browser (Pyodide) run of the three project labs; not run in this checkout.",
        "Mutants on seeds 10-49 (gate is 0-9).",
        "Exemplar annotations were not scored by this verifier (ruling 23); calibration rests on the blind file.",
        "The L05 lab twin and lesson pages changed in the delta but are outside slice d; only the twin's exit code was checked.",
        "verify_refs live run (offline only, per the M5 gate).",
        "Whether the architect accepts the calibration rows beyond the KNOWN-ISSUES table (ruling 31 context accepts them; not re-read beyond the table).",
    ],
}
dest = REPO / "ledgers/M5/M5-d.json"
dest.write_text(json.dumps(fragment, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("wrote", dest, summary_counts, "mutants", len(mutants))
