"""Round 1 (M5 slice d, closing delta) fragment builder.

Reads the base round-6 fragment (pin e896b7a4), re-verification results written by this round's scripts in
ledgers/M5/scripts/M5-d-r1/out/, and the git delta e896b7a4..HEAD. Carries a base PASS row only when every path it
cites is byte-identical across the delta (checked here with git diff --quiet); every other row is re-verified and
its evidence is the command output recorded in out/. Writes ledgers/M5/M5-d.json.
"""

from __future__ import annotations

import ast
import json
import re
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path

REPO = Path(sys.argv[1]).resolve()
BASE_FRAG = Path("/Users/billyribeiro/.fanout/frags/S-M5-d.round6.json")
BASE_PIN = "e896b7a45344d1bc17ebfbf7fb05d87698ec9d6a"
HEAD = subprocess.run(
    ["git", "-C", str(REPO), "rev-parse", "HEAD"], capture_output=True, text=True, check=True
).stdout.strip()
OUT = REPO / "ledgers/M5/scripts/M5-d-r1/out"
base = json.loads(BASE_FRAG.read_text(encoding="utf-8"))
base_rows = {r["id"]: r for r in base["rows"]}


def unchanged(paths: list[str]) -> bool:
    r = subprocess.run(["git", "-C", str(REPO), "diff", "--quiet", BASE_PIN, HEAD, "--", *paths])
    return r.returncode == 0


def out(name: str) -> str:
    return (OUT / name).read_text(encoding="utf-8").strip()


def strip_prefix(text: str) -> str:
    return re.sub(r"^Carried from round \d+ \([^)]*\):\s*", "", text)


CARRY = {
    "M5-d-r1-02": ["course/modules/M/M5/grader/instance.py"],
    "M5-d-r1-07": ["course/modules/M/M5/grader/test_project.py"],
    "M5-d-r1-10": ["course/modules/M/M5/project.html", "course/assets"],
    "M5-d-r1-11": ["course/modules/M/M5/project.html"],
    "M5-d-r1-12": ["course/modules/M/M5/project.html"],
    "M5-d-r1-15": ["course/modules/M/M5/project.html", "course/modules/M/M5/index.html", "curriculum/curriculum.json"],
    "M5-d-r1-17": ["course/modules/M/M5/project.html"],
    "M5-d-r1-18": ["course/modules/M/M5/project.html"],
    "M5-d-r1-19": ["course/modules/M/M5/project.html"],
    "M5-d-r1-20": ["course/modules/M/M5/project.html"],
    "M5-d-r1-21": [
        "course/modules/M/M5/project.html",
        "course/modules/M/M5/grader/reference.py",
        "course/modules/M/M5/grader/test_project.py",
    ],
    "M5-d-r1-22": [
        "course/modules/M/M5/grader/starter.py",
        "course/modules/M/M5/grader/reference.py",
        "course/modules/M/M5/project.html",
    ],
    "M5-d-r1-23": ["course/modules/M/M5/project.html", "course/assets/js/python.js"],
    "M5-d-r1-24": ["course/modules/M/M5/project.html", "notation"],
    "M5-d-r1-25": ["course/modules/M/M5/project.html", "course/modules/M/M5/grader/instance.py"],
    "M5-d-r1-26": ["course/modules/M/M5/project.html"],
    "M5-d-r1-27": ["course/modules/M/M5/project.html"],
    "M5-d-r1-30": ["course/modules/M/M5/project.html"],
    "M5-d-r1-31": ["course/modules/M/M5/grader/instance.py", "course/modules/M/M5/project.html"],
    "M5-d-r1-32": ["course/modules/M/M5/project.html"],
    "M5-d-r2-37": ["course/modules/M/M5/project.html"],
    "M5-d-r3-42": ["course/modules/M/M5/project.html"],
    "M5-d-r4-45": ["course/modules/M/M5/grader/test_project.py"],
    "M5-d-r4-47": ["course/modules/M/M5/project.html", "course/assets/js/labs.js"],
    "M5-d-r4-49": ["course/modules/M/M5/project.html"],
}

carried: dict[str, str] = {}
for rid, paths in CARRY.items():
    assert rid in base_rows and base_rows[rid]["status"] == "PASS", rid
    assert unchanged(paths), (rid, paths)
    carried[rid] = (
        f"Carried from round 6 ({', '.join(paths)} byte-identical since the previous pin {BASE_PIN[:8]}; "
        f"git diff --quiet {BASE_PIN[:8]} {HEAD[:8]} clean): " + strip_prefix(base_rows[rid]["evidence"])
    )

# Subjects that changed in the delta, and rows re-verified here.
assert not unchanged(["plans/FINAL-ARCHITECT-RULINGS.md"])
assert not unchanged(["plans/M5-build-plan.md"])
assert unchanged(["plans/KNOWN-ISSUES.md"]) and unchanged(["plans/M5-open-items.md"])
assert unchanged(["course/modules/M/M5/grader"]) and unchanged(["course/modules/M/M5/project.html"])
assert unchanged(["tests/labs/M5"]) and unchanged(["ledgers/M5/alternatives"]) and unchanged(["tools"])

blind = json.loads(Path("/Users/billyribeiro/.fanout/blind/M5-d.json").read_text(encoding="utf-8"))
assert blind["A"] == [2, 1, 1, 2, 2, 1] and blind["B"] == [4, 3, 4, 3, 3, 3], blind
calib_text = (
    "Blind scores (dedicated scorer, ruling 23; ~/.fanout/blind/M5-d.json read this round): A = [2,1,1,2,2,1], "
    'B = [4,3,4,3,3,3]. Official (project.html:419 data-scores="2,2,1,2,2,2"; :451 data-scores="4,4,4,4,4,3"). '
    "Differences, all one level: A C2 and C6 (1 vs 2); B C2, C4, C5 (3 vs 4). plans/KNOWN-ISSUES.md "
    "'Rubric calibration' table (heading 'accepted by the architect') lists exactly these differences for M5 A and "
    "M5 B; plans/KNOWN-ISSUES.md is byte-identical across the delta."
)

# Mutants: the standing set (141 files) with killed_by from this round's mutate run.
mutant_files = sorted((REPO / "ledgers/M5/mutants").glob("*.py"))
kills: dict[str, str] = {}
for line in out("mutate_M5_0-9.out").splitlines():
    m = re.match(r"^KILLED (\S+?): .* -> (.+)$", line)
    if m:
        kills[m.group(1)] = m.group(2).strip()
assert len(mutant_files) == 141 and len(kills) == 141, (len(mutant_files), len(kills))
base_desc = {m["name"]: m["description"] for m in base["mutants"]}
mutants = []
for f in mutant_files:
    doc = (ast.get_docstring(ast.parse(f.read_text(encoding="utf-8"))) or "").strip().splitlines()[0]
    mutants.append(
        {
            "name": f.name,
            "description": base_desc.get(f.name, doc),
            "killed_by": kills[f.name],
        }
    )

R1 = "ledgers/M5/scripts/M5-d-r1/out"
rows = [
    {
        "id": "M5-d-r1-01",
        "check": "2.6-autograder-reference",
        "location": "course/modules/M/M5/grader/reference.py",
        "status": "PASS",
        "evidence": f"{R1}/run_graders_M5_0-49.out: 'run_graders M5: PASS (reference 50/50 seeds, slowest 0.3 s)' rc 0. "
        f"{R1}/r6_seeds_collect_twins_r1.out: 'collect-only tail: 101 tests collected'; reference seed 0 "
        "'rc: 0 101 passed'.",
    },
    {
        "id": "M5-d-r1-02",
        "check": "2.6-instances",
        "location": "course/modules/M/M5/grader/instance.py",
        "status": "PASS",
        "evidence": carried["M5-d-r1-02"],
    },
    {
        "id": "M5-d-r1-03",
        "check": "2.6-mutation-existing",
        "location": "ledgers/M5/mutants/ (141 files)",
        "status": "PASS",
        "evidence": f"{R1}/mutate_M5_0-9.out: 'mutate_graders M5: PASS (141/141 killed)' rc 0; 141 KILLED lines, "
        "0 survivors. Includes r6_01..03 and r5_01..03 (see M5-d-r4-46).",
    },
    {
        "id": "M5-d-r1-04",
        "check": "2.6-mutation-new-killed",
        "location": "ledgers/M5/mutants/d1_02_continuation_reads_the_current_state.py; d1_03_value_is_the_penultimate_iterate.py",
        "status": "PASS",
        "evidence": f"{R1}/mutate_M5_0-9.out: 'KILLED d1_02_... -> test_operator_matches_its_definition[0] (seed 0)'; "
        "'KILLED d1_03_... -> test_certified_error_bounds_the_distance_to_the_fixed_point[0] (seed 0)'.",
    },
    {
        "id": "M5-d-r1-05",
        "check": "2.6-mutation-survivor",
        "location": "course/modules/M/M5/grader/test_project.py:739-753; ledgers/M5/mutants/d1_01_top_grid_point_never_a_successor.py",
        "status": "PASS",
        "evidence": f"{R1}/mutate_M5_0-9.out: 'KILLED d1_01_... -> test_operator_uses_the_top_point_on_a_grid_inside_zero_one (seed 0)'. "
        "test_project.py unchanged across the delta.",
    },
    {
        "id": "M5-d-r1-06",
        "check": "2.6-alternatives",
        "location": "ledgers/M5/alternatives/alt1..alt5; ledgers/M5/alternatives/not_accepted/; plans/M5-build-plan.md:118-123 and :305-313; plans/M5-open-items.md:16-20; course/modules/M/M5/project.html:244-246",
        "status": "PASS",
        "evidence": f"Re-verified (subject changed: plan and ruling text). {R1}/alt_seeds_0-49.out (scripts/M5-d-r1/alt_seeds_r1.py, "
        "scratch copy per seed, pytest -I -W error, QF_SEED 0-49): alt1..alt5 each '50/50 seeds pass; first failure None'; "
        "not_accepted/alt1_gauss_seidel_in_place.py and alt2_residual_stop.py each '0/50 seeds pass' (first failure seed 0, "
        "test_certified_error_is_beta_over_one_minus_beta_times_the_last_change[1-0]). Page: project.html:244 'Each sweep is "
        "synchronous'; :245 certified error beta/(1-beta) times the last change; :246 stop at the first sweep with certified "
        "error at most tol. Plan :305-313 bullet names alt1..alt5 and says in-place and residual-bound stops are not valid "
        "(ruling 31); open-items decision 3 (lines 16-20) names the same two rejected variants and 0 of 50 each. "
        "Locator note: ruling 31 and open-items cite the bullet as plan lines 304-306; the amended bullet is at 305-313.",
    },
    {
        "id": "M5-d-r1-07",
        "check": "2.6-failure-message-leak",
        "location": "course/modules/M/M5/grader/test_project.py (every expect/must_raise/pytest.fail message)",
        "status": "PASS",
        "evidence": carried["M5-d-r1-07"],
    },
    {
        "id": "M5-d-r1-08",
        "check": "2.6-mutant-descriptions",
        "location": "ledgers/M5/mutants/ (141 files)",
        "status": "PASS",
        "evidence": f"{R1}/mutant_docstrings_r1.out: 'mutant files: 141 empty docstrings: []' (python -I ast.get_docstring over the 141 files, this round).",
    },
    {
        "id": "M5-d-r1-09",
        "check": "2.6-test-count",
        "location": "course/modules/M/M5/project.html:234-235 ('Grading mode', 101 checks); grader/test_project.py",
        "status": "PASS",
        "evidence": "Fresh: collect-only in scratch with reference.py as contraction_solver.py: '101 tests collected'; reference seed 0 '101 passed'. "
        "project.html:235 reads 'runs 101 checks with warnings as errors' (grep, this round); project.html unchanged across the delta.",
    },
    {
        "id": "M5-d-r1-10",
        "check": "2.6-browser-suite",
        "location": "course/modules/M/M5/project.html:272-281; course/assets/js/grader.js:34-61; course/assets/js/store.js; course/assets/js/py-worker.js:111",
        "status": "PASS",
        "evidence": carried["M5-d-r1-10"],
    },
    {
        "id": "M5-d-r1-11",
        "check": "2.6-rubric-observable",
        "location": "course/modules/M/M5/project.html:404-412 (rubric cells C1-C6)",
        "status": "PASS",
        "evidence": carried["M5-d-r1-11"],
    },
    {
        "id": "M5-d-r1-12",
        "check": "2.6-rubric-caption",
        "location": "course/modules/M/M5/project.html:403-404",
        "status": "PASS",
        "evidence": carried["M5-d-r1-12"],
    },
    {
        "id": "M5-d-r1-13",
        "check": "2.6-calibration-exemplar-A",
        "location": "course/modules/M/M5/project.html:419-449 (data-scores 2,2,1,2,2,2)",
        "status": "PASS",
        "evidence": "Calibration row (ruling 23). " + calib_text + " Exemplar A PASS within one level.",
    },
    {
        "id": "M5-d-r1-14",
        "check": "2.6-calibration-exemplar-B",
        "location": "course/modules/M/M5/project.html:451-481 (data-scores 4,4,4,4,4,3)",
        "status": "PASS",
        "evidence": "Calibration row (ruling 23). " + calib_text + " Exemplar B PASS within one level.",
    },
    {
        "id": "M5-d-r1-15",
        "check": "2.6-hours-arithmetic",
        "location": "course/modules/M/M5/project.html:33, 258-264; course/modules/M/M5/index.html:29, 39-42, 131; curriculum/curriculum.json (M5 hours 130)",
        "status": "PASS",
        "evidence": carried["M5-d-r1-15"] + " Re-derived this round: 1+2+8+7+3+5 = 26; 26/130 = 20.0 %.",
    },
    {
        "id": "M5-d-r1-16",
        "check": "2.6-labs",
        "location": "course/modules/M/M5/project.html:55-220, 287-390; tests/labs/M5/lab-M5-project-1..3.py",
        "status": "PASS",
        "evidence": f"{R1}/run_labs_M5_project.out: 'run_labs M5: PASS (3/3)' rc 0. {R1}/r6_seeds_collect_twins_r1.out: each twin alone "
        "with python -I -W error: lab-M5-project-1 rc 0, 14 stdout lines, 0 stderr bytes; -2 rc 0, 4 lines; -3 rc 0, 16 lines. "
        f"{R1}/page_smoke_M5_project.out: 'page_smoke modules/M/M5/project.html: PASS' with the three labs run in Chromium and "
        "'in-browser grader: All 101 tests pass'.",
    },
    {
        "id": "M5-d-r1-17",
        "check": "2.6-rung1-annotated",
        "location": "course/modules/M/M5/project.html:57, 58-155",
        "status": "PASS",
        "evidence": carried["M5-d-r1-17"],
    },
    {
        "id": "M5-d-r1-18",
        "check": "2.6-rung2-completion",
        "location": "course/modules/M/M5/project.html:159-222",
        "status": "PASS",
        "evidence": carried["M5-d-r1-18"],
    },
    {
        "id": "M5-d-r1-19",
        "check": "2.6-numbers-lab3",
        "location": "course/modules/M/M5/project.html:289, 293-298, 365, 373-388",
        "status": "PASS",
        "evidence": carried["M5-d-r1-19"],
    },
    {
        "id": "M5-d-r1-20",
        "check": "2.6-proof-math",
        "location": "course/modules/M/M5/project.html:393-399 (brief A1-A4); Conventions 244-248",
        "status": "PASS",
        "evidence": carried["M5-d-r1-20"],
    },
    {
        "id": "M5-d-r1-21",
        "check": "2.6-named-invalid-inputs",
        "location": "course/modules/M/M5/project.html:240-248; grader/reference.py:34-78; grader/test_project.py:618-785",
        "status": "PASS",
        "evidence": carried["M5-d-r1-21"],
    },
    {
        "id": "M5-d-r1-22",
        "check": "2.6-starter-signatures",
        "location": "course/modules/M/M5/grader/starter.py:18,23; grader/reference.py:94,101; project.html:231",
        "status": "PASS",
        "evidence": carried["M5-d-r1-22"],
    },
    {
        "id": "M5-d-r1-23",
        "check": "2.6-time-limit",
        "location": "course/modules/M/M5/project.html:233; course/assets/js/python.js:4",
        "status": "PASS",
        "evidence": carried["M5-d-r1-23"],
    },
    {
        "id": "M5-d-r1-24",
        "check": "2.6-notation",
        "location": "course/modules/M/M5/project.html (all math); notation/notation.json",
        "status": "PASS",
        "evidence": carried["M5-d-r1-24"],
    },
    {
        "id": "M5-d-r1-25",
        "check": "2.8-simulated-label",
        "location": "course/modules/M/M5/project.html:229; course/modules/M/M5/grader/instance.py:3, 41, 56",
        "status": "PASS",
        "evidence": carried["M5-d-r1-25"],
    },
    {
        "id": "M5-d-r1-26",
        "check": "2.8-data-manifest",
        "location": "course/modules/M/M5/project.html (no data-files attribute)",
        "status": "PASS",
        "evidence": carried["M5-d-r1-26"],
    },
    {
        "id": "M5-d-r1-27",
        "check": "2.8-figures",
        "location": "course/modules/M/M5/project.html",
        "status": "PASS",
        "evidence": carried["M5-d-r1-27"],
    },
    {
        "id": "M5-d-r1-28",
        "check": "2.1-references",
        "location": "course/modules/M/M5/project.html:500-512; references/references.json",
        "status": "PASS",
        "evidence": f"{R1}/verify_refs_offline.out: 'offline integrity: 560 entries, 0 problems' rc 0. references/ unchanged across the delta.",
    },
    {
        "id": "M5-d-r1-29",
        "check": "2.6-lint-and-types",
        "location": "course/modules/M/M5/grader; tests/labs/M5; ledgers/M5; repository",
        "status": "PASS",
        "evidence": f"{R1}/ruff_check_scope.out: 'All checks passed!' rc 0 (ruff check course/modules/M/M5/grader tests/labs/M5 ledgers/M5). "
        f"{R1}/ruff_format_scope.out: '17 files already formatted' rc 0. {R1}/mypy_no_incremental.out: 'Success: no issues found in 386 source files' rc 0 "
        "(base recorded 385; the added files come from other slices). ledgers/*/scripts is in pyproject extend-exclude, so the scripts of this round are not in the gate scope.",
    },
    {
        "id": "M5-d-r1-30",
        "check": "2.9-structure",
        "location": "course/modules/M/M5/project.html:40-49, 223-250, 270-281, 283-288, 491-498",
        "status": "PASS",
        "evidence": carried["M5-d-r1-30"],
    },
    {
        "id": "M5-d-r1-31",
        "check": "2.6-instance-simulated",
        "location": "course/modules/M/M5/grader/instance.py:3; project.html:229",
        "status": "PASS",
        "evidence": carried["M5-d-r1-31"],
    },
    {
        "id": "M5-d-r1-32",
        "check": "2.2-interpretive-claims",
        "location": "course/modules/M/M5/project.html:156, 219, 389",
        "status": "PASS",
        "evidence": carried["M5-d-r1-32"],
    },
    {
        "id": "M5-d-r2-33",
        "check": "2.6-mutation-new-survivor",
        "location": "ledgers/M5/mutants/d3_01_feasibility_allows_a_tie_tolerance_of_1e-12.py; course/modules/M/M5/grader/test_project.py:444-460",
        "status": "PASS",
        "evidence": f"{R1}/mutate_M5_0-9.out: 'KILLED d3_01_... -> test_successor_within_a_tie_tolerance_above_the_resources_is_infeasible (seed 0)'.",
    },
    {
        "id": "M5-d-r2-34",
        "check": "2.6-mutation-new-survivor",
        "location": "ledgers/M5/mutants/d3_02_first_point_bound_checked_only_for_longer_grids.py; course/modules/M/M5/grader/test_project.py:721-726",
        "status": "PASS",
        "evidence": f"{R1}/mutate_M5_0-9.out: 'KILLED d3_02_... -> test_grid_must_be_nonempty_positive_strictly_increasing_and_start_at_most_one[one-point-first-above-one] (seed 0)'.",
    },
    {
        "id": "M5-d-r2-35",
        "check": "2.6-mutation-new-killed",
        "location": "ledgers/M5/mutants/d3_03_value_is_the_penultimate_iterate_when_the_budget_runs_out.py",
        "status": "PASS",
        "evidence": f"{R1}/mutate_M5_0-9.out: 'KILLED d3_03_... -> test_the_first_sweep_starts_from_zero_and_is_synchronous[0] (seed 0)'.",
    },
    {
        "id": "M5-d-r2-36",
        "check": "2.6-dag",
        "location": "course/modules/M/M5/project.html:37, 227, 494, 501; curriculum/curriculum.json (M5 prereqs ['M2'])",
        "status": "PASS",
        "evidence": f"{R1}/check_dag_M5.out: 'check_dag M5: PASS' rc 0. page and curriculum unchanged across the delta.",
    },
    {
        "id": "M5-d-r2-37",
        "check": "2.6-spec-completeness",
        "location": "course/modules/M/M5/project.html:223-250",
        "status": "PASS",
        "evidence": carried["M5-d-r2-37"],
    },
    {
        "id": "M5-d-r2-38",
        "check": "2.6-atlas-studio",
        "location": "curriculum/curriculum.json (M5 entry); plans/M5-build-plan.md:409 (was :408 before the one-line amendment at 117-123)",
        "status": "PASS",
        "evidence": "Re-verified (plan line shifted). plans/M5-build-plan.md:409 reads 'No Atlas milestone. No Atlas entry names M5 (`curriculum/meta.yaml` "
        "atlas block; §0.1). The project has no `atlas` key.'; the same text at e896b7a4:408 (git show | sed -n 408p; diff clean). "
        f"{R1}/check_projects_M5.out: 'check_projects M5: PASS'. tools/check_projects.py atlas branch unchanged (tools/ unchanged across the delta).",
    },
    {
        "id": "M5-d-r3-39",
        "check": "2.6-mutation-new-survivor",
        "location": "ledgers/M5/mutants/r3_01_operator_clamps_each_image_at_zero.py; course/modules/M/M5/grader/test_project.py:121-141",
        "status": "PASS",
        "evidence": f"{R1}/mutate_M5_0-9.out: 'KILLED r3_01_... -> test_operator_matches_its_definition[0] (seed 0)'.",
    },
    {
        "id": "M5-d-r3-40",
        "check": "2.6-mutation-new-survivor",
        "location": "ledgers/M5/mutants/r3_02_continuation_uses_absolute_value.py; course/modules/M/M5/grader/test_project.py:121-141",
        "status": "PASS",
        "evidence": f"{R1}/mutate_M5_0-9.out: 'KILLED r3_02_... -> test_operator_matches_its_definition[0] (seed 0)'.",
    },
    {
        "id": "M5-d-r3-41",
        "check": "2.6-mutation-new-survivor",
        "location": "ledgers/M5/mutants/r3_03_feasibility_tie_tolerance_of_1e-14.py; course/modules/M/M5/grader/test_project.py:463-479",
        "status": "PASS",
        "evidence": f"{R1}/mutate_M5_0-9.out: 'KILLED r3_03_... -> test_feasibility_is_exact_with_no_tie_tolerance_at_the_last_bit (seed 0)'.",
    },
    {
        "id": "M5-d-r3-42",
        "check": "2.6-rubric-observable-exclusive",
        "location": "course/modules/M/M5/project.html:404-412 (rubric C5 row, line 410)",
        "status": "PASS",
        "evidence": carried["M5-d-r3-42"],
    },
    {
        "id": "M5-d-r3-43",
        "check": "2.6-calibration-exemplar-descriptor-exclusivity",
        "location": "course/modules/M/M5/project.html:419-482 (annotations)",
        "status": "PASS",
        "evidence": "Calibration row (ruling 23). "
        + calib_text
        + " Exemplar annotations PASS within one level (the descriptor tie rule is in the blind file's notes, read this round).",
    },
    {
        "id": "M5-d-r4-44",
        "check": "2.6-alternatives-five-pass",
        "location": "ledgers/M5/alternatives/alt1..alt5; ledgers/M5/alternatives/not_accepted/",
        "status": "PASS",
        "evidence": f"Fresh: {R1}/alt_seeds_0-49.out: alt1..alt5 '50/50 seeds pass' each (first failure None). alt5 builds a new list from the previous vector (out at alt5 _sweep, reversed(range(len(grid)))); alt2 is class ContractionSolver with precomputed feasible tables; alt3 comprehension over feasible index lists; alt4 bisect_right prefix; alt1 functools.reduce over tuples.",
    },
    {
        "id": "M5-d-r4-45",
        "check": "2.6-grader-docstring-claim",
        "location": "course/modules/M/M5/grader/test_project.py:559-562",
        "status": "PASS",
        "evidence": carried["M5-d-r4-45"],
    },
    {
        "id": "M5-d-r4-46",
        "check": "2.6-new-student-error-mutants",
        "location": "ledgers/M5/mutants/r4_01..r4_04; r5_01..r5_03; r6_01..r6_03",
        "status": "PASS",
        "evidence": f"{R1}/mutate_M5_0-9.out: r4_01..r4_04 KILLED (seed 0). {R1}/r5_seeds_r1.out: r5_01, r5_02, r5_03 rc 1 on each of seeds 0-9. "
        f"{R1}/r6_seeds_collect_twins_r1.out: r6_01, r6_02, r6_03 killed on 10/10 seeds. Killing tests (seed 0): r6_01 -> "
        "test_certified_error_exactly_at_tol_stops_the_first_sweep; r6_02 -> test_successor_exactly_at_the_resources_is_feasible; r6_03 -> the [1-0] certified-error test.",
    },
    {
        "id": "M5-d-r4-47",
        "check": "2.6-lab-comparator-absolute-tolerance",
        "location": "course/modules/M/M5/project.html:142, 215, 372 (data-tolerance 1e-15); course/assets/js/labs.js:50",
        "status": "PASS",
        "evidence": carried["M5-d-r4-47"],
    },
    {
        "id": "M5-d-r4-48",
        "check": "2.6-mutation-full-rerun",
        "location": "ledgers/M5/mutants/ (141 files); tools/mutate_graders.py --unit M5 --seeds 0-9",
        "status": "PASS",
        "evidence": f"{R1}/mutate_M5_0-9.out: 'mutate_graders M5: PASS (141/141 killed)' rc 0 (ruling 37: the standing set, no new mutants written this round).",
    },
    {
        "id": "M5-d-r4-49",
        "check": "2.9-process-words",
        "location": "course/modules/M/M5/project.html (learner text)",
        "status": "PASS",
        "evidence": carried["M5-d-r4-49"],
    },
    {
        "id": "M5-d-r6-01",
        "check": "2.6-ruling-path",
        "location": "plans/FINAL-ARCHITECT-RULINGS.md:103-106 (ruling 31); ledgers/M5/alternatives/not_accepted/",
        "status": "PASS",
        "evidence": "Re-verified (subject changed: ruling 31 text). plans/FINAL-ARCHITECT-RULINGS.md:106 now reads 'ledgers/M5/alternatives/not_accepted/ keeps the two files as documented non-accepted variants'. "
        "ls ledgers/M5/alternatives/not_accepted: alt1_gauss_seidel_in_place.py, alt2_residual_stop.py, README.md (exist). "
        "ls ledgers/M5/not_accepted: 'No such file or directory'. grep -rn 'ledgers/M5/not_accepted' over the repo (excluding .venv, .git) matches "
        "only the historical round-6 script ledgers/M5/scripts/M5-d-r6/build_fragment_r6.py (a record, not a doc or gate).",
    },
    {
        "id": "M5-d-r6-02",
        "check": "2.6-plan-consistency",
        "location": "plans/M5-build-plan.md:118-123 (section 1, 'Grader tests demand an exception type only...')",
        "status": "PASS",
        "evidence": "Re-verified (subject changed). Section 1 now lists the accepted set alt1 to alt5 in ledgers/M5/alternatives (functional reduce; a class with precomputed feasible tables; comprehensions over feasible index lists; bisect for feasible successors; a reverse-order synchronous sweep) and states 'In-place (Gauss-Seidel) sweeps and residual-bound stops are not valid alternatives of this project (ruling 31)'. Each description matches the file: alt1 reduce/tuples (imports functools.reduce), alt2 ContractionSolver class (line 82), alt3 comprehension over feasible lists, alt4 bisect_right, alt5 reversed(range(len(grid))) synchronous sweep. The sentence no longer lists in-place or residual-stop as examples; the plan bullet at 305-313 says the same.",
    },
    {
        "id": "M5-d-r6-03",
        "check": "2.6-new-student-error-mutants",
        "location": "ledgers/M5/mutants/r6_01_stop_only_when_certified_error_strictly_below_tol.py; r6_02_saving_must_leave_strictly_positive_consumption.py; r6_03_solve_starts_from_the_ones_vector.py",
        "status": "PASS",
        "evidence": f"Re-verified (mutant files unchanged in content since the base; diffed against grader/reference.py this round). r6_01: 'if certified < target' for '<=' (student error: stop only when strictly below tol). r6_02: 'if successor < available' for '<=' (saving equal to k**alpha refused). r6_03: 'values = [1.0] * len(points)' for [0.0] (start from ones). Per-seed on seeds 0-9: rc 1 on every seed for each ({R1}/r6_seeds_collect_twins_r1.out). Page: project.html:246 'at most tol'; :241 feasible when c >= 0, i.e. k' <= k**alpha; :244 'V_0 = 0'.",
    },
]

ids = [r["id"] for r in rows]
assert len(ids) == len(set(ids))
assert set(ids) >= set(base_rows), sorted(set(base_rows) - set(ids))
assert all(r["status"] == "PASS" for r in rows)
extra = sorted(set(ids) - set(base_rows))

notes = [
    f"Closing delta (ruling 30) for slice d: pin {HEAD} vs base {BASE_PIN} (git diff {BASE_PIN[:8]}..HEAD). "
    "Subjects that changed for slice d: plans/FINAL-ARCHITECT-RULINGS.md (ruling 31 path fixed; ruling 37 added), plans/M5-build-plan.md "
    "(section 1 bullet at 118-123, one line longer, so the Atlas line moved 408 to 409). Re-verified: M5-d-r6-01, M5-d-r6-02, M5-d-r1-06, M5-d-r2-38, M5-d-r4-44.",
    "Unchanged across the delta (checked with git diff --quiet): course/modules/M/M5 (project.html, grader/, index.html, cards), tests/labs/M5, "
    "course/assets, curriculum, notation, references, tools, plans/KNOWN-ISSUES.md, plans/M5-open-items.md, ledgers/M5/alternatives. "
    "Rows citing only these are carried with the carry prefix; their paths are checked in the build script (assert unchanged()).",
    "Mutants: the r6_01..r6_03 files are in git since 4540351d (not at e896b7a4); the base fragment's statement that they were present at e896b7a4 "
    "describes the worktree, not the git tree. Content is verified at HEAD. Provenance note only.",
    "Ruling 37: this closing round wrote no new mutants and no new survivors were searched for; the standing set of 141 is run.",
    "Locator drift (not a ruling-26 defect, recorded as a note): ruling 31 (plans/FINAL-ARCHITECT-RULINGS.md:103-106) and plans/M5-open-items.md:21 "
    "cite the amended bullet as plans/M5-build-plan.md lines 304-306; the amended bullet is at 305-313 (the in-place sentence at 310-312). "
    "Row M5-d-r1-06 uses the current lines.",
    "Calibration: the two exemplars' blind scores match the KNOWN-ISSUES table exactly (one-level differences). Scores not re-derived by this verifier (ruling 23).",
    "Scope: slice d gates re-run at 95f3f8cb. Other slices' changes in the delta (M7, FC1, FC2, E3, CS2, LX1, L05 and others) are out of scope.",
    "Shared directory: ledgers/M5/scripts/M5-d-r1/ already held tracked files from an earlier verification (commit 9294b914); this round's files "
    "use distinct names (alt_seeds_r1.py, r6_seeds_collect_twins_r1.py, build_fragment_r1.py, r5 per-seed run in out/r5_seeds_r1.out); out/ is new.",
]

fragment = {
    "unit": "M5",
    "slice": "d",
    "round": 1,
    "verifier": "Haiku independent verifier (closing delta, round 1 of this checkout); no build context; calibration by the dedicated blind scorer (ruling 23)",
    "pin": HEAD,
    "base": BASE_PIN,
    "delta_from": BASE_PIN,
    "base_fragment": str(BASE_FRAG),
    "checkout": str(REPO),
    "scratch": str(REPO / "ledgers/M5/scripts/M5-d-r1"),
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "verdict": "PASS",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": notes,
    "summary": (
        f"Closing delta, slice d, round 1 (base round 6, pin {BASE_PIN[:8]} -> {HEAD[:8]}). {len(rows)} rows: "
        f"PASS {len(rows)}, FAIL 0, UNVERIFIABLE 0. Base FAIL rows M5-d-r6-01 (ruling 31 path) and M5-d-r6-02 (plan section 1) "
        "are fixed at HEAD and re-verified PASS. Carried rows: "
        f"{len(carried)}; fresh rows: {len(rows) - len(carried)}. Gates: check_pages, check_dag, check_projects, run_labs (project), "
        "run_graders 0-49, page_smoke (project), verify_refs --offline, ruff check/format (scope), mypy --no-incremental, pytest -k M5, "
        "mutate_graders 0-9 (141/141), alternatives 50 seeds (5 pass, 2 not_accepted 0/50), per-seed kills of r5/r6 mutants. All PASS."
    ),
    "what_not_checked": [
        "Mutants on seeds 10-49 (gate is 0-9).",
        "Exemplar annotations were not scored by this verifier (ruling 23); calibration rests on ~/.fanout/blind/M5-d.json, read this round.",
        "No new student-error mutants were written (ruling 37, closing round). The ruling-26 FAIL kinds were the only ones counted.",
        "verify_refs live run (offline only, per the M5 gate).",
        "Full repository pytest (only -k M5 selected, 13 tests, as in the base gate).",
        "Browser run of the labs was done through tools/page_smoke.py (Chromium), not by hand.",
        "Other slices' changes in the same delta (M7, FC1, FC2, E3, CS2, LX1, L05) were not verified.",
    ],
}

problems = []
sys.path.insert(0, str(REPO / "tools"))
import ledger  # noqa: E402

problems = ledger.validate(fragment, "M5-d")
print("validate:", problems)
(REPO / "ledgers/M5/M5-d.json").write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(
    "rows",
    len(rows),
    "carried",
    len(carried),
    "fresh",
    len(rows) - len(carried),
    "extra",
    extra,
    "mutants",
    len(mutants),
)
