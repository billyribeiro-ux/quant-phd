"""Build ledgers/CS2/CS2-d.json (round 1, closing delta of slice d) from the base fragment and this round's evidence."""

import datetime
import json
import re
import sys

ROOT = sys.argv[1]
BASE = "/Users/billyribeiro/.fanout/frags/F1-CS2-d.round1.json"
S = "ledgers/CS2/scripts/CS2-d-r1"
base = json.load(open(BASE, encoding="utf-8"))
CARRY_PREFIX = (
    "Carried from round 1 (course/modules/CS/CS2/project.html, course/modules/CS/CS2/grader/*, "
    "tests/labs/CS2/lab-CS2-project-{1,2,3}.py byte-identical since the previous pin 95f3f8cb, "
    "checked by git diff --quiet over those paths): "
)
base_rows = {r["id"]: r for r in base["rows"]}

fresh = {
    "gate-mutate-cs2": (
        "PASS",
        "tools/mutate_graders.py --unit CS2 --seeds 0-9 at pin 2a805c83: 'mutate_graders CS2: PASS (178/178 killed)' "
        "(ledgers/CS2/scripts/CS2-d-r1/mutate_CS2_0-9_r1.txt, 178 KILLED lines, 0 SURVIVED). The pass holds only because "
        "r15_04, r15_06 and r15_07 were moved out of mutants/; r15_07 is a non-equivalent survivor (row mut-r15-survivors).",
        None,
    ),
    "gate-run-graders": (
        "PASS",
        "tools/run_graders.py --unit CS2 --seeds 0-49: 'run_graders CS2: PASS (reference 50/50 seeds, slowest 0.3 s)', "
        "rc=0 (ledgers/CS2/scripts/CS2-d-r1/gates_graders_r1.txt).",
        None,
    ),
    "gate-check-projects": (
        "PASS",
        "tools/check_projects.py --unit CS2: 'check_projects CS2: PASS' (gates_quick_r1.txt).",
        None,
    ),
    "gate-check-dag": (
        "PASS",
        "tools/check_dag.py --unit CS2: 'check_dag CS2: PASS' (gates_quick_r1.txt).",
        None,
    ),
    "gate-check-pages": (
        "PASS",
        "tools/check_pages.py --unit CS2: 'check_pages CS2: PASS' (gates_quick_r1.txt).",
        None,
    ),
    "gate-run-labs": (
        "PASS",
        "tools/run_labs.py --unit CS2 --page project: 'run_labs CS2: PASS (3/3)' (gates_mid_r1.txt).",
        None,
    ),
    "gate-page-smoke": (
        "PASS",
        "tools/page_smoke.py --unit CS2 --pages project: 'page_smoke CS2: PASS', 175 of 175 in-browser grader tests on "
        "seed 1869382297 (gates_graders_r1.txt).",
        None,
    ),
    "gate-ruff-mypy": (
        "PASS",
        "ruff check . -> 'All checks passed!'; ruff format --check . -> '555 files already formatted'; "
        "mypy --no-incremental -> 'Success: no issues found in 386 source files' (gates_quick_r1.txt, gates_mid_r1.txt, "
        "and a rerun after the verifier scripts were added, ruff_mypy_rerun_r1.txt).",
        None,
    ),
    "gate-verify-refs": (
        "PASS",
        "tools/verify_refs.py --offline: 'offline integrity: 560 entries, 0 problems' (gates_quick_r1.txt).",
        None,
    ),
    "gate-collect-count": (
        "PASS",
        "pytest --collect-only -q test_project.py in a scratch workspace (reference copied as streamstats.py, "
        "instance.py copied, QF_SEED=0): '175 tests collected'. project.html:211 states 175. Direct collection inside "
        "grader/ fails on the missing streamstats module, as in the base (collect_test_project.txt).",
        None,
    ),
    "gate-pytest-relevant": (
        "PASS",
        "pytest -q -k CS2 tests/test_labs.py tests/test_page_smoke.py tests/test_page_checks.py: rc=0 "
        "(pytest_k_CS2_current_r1.txt).",
        None,
    ),
    "gate-local-pytest": (
        "PASS",
        "Reference copied as streamstats.py in a scratch workspace, env -i QF_SEED=0 PYTHONHASHSEED=0, "
        "python -I -W error -m pytest --assert=plain -W error -q test_project.py: '175 passed in 0.07s', rc=0 "
        "(local_pytest_reference_seed0_current_r1.txt).",
        None,
    ),
    "labs-project-1": (
        "PASS",
        "run_labs CS2 --page project: PASS (3/3) (gates_mid_r1.txt); twin tests/labs/CS2/lab-CS2-project-1.py run alone "
        "with python -I -W error: rc=0. Page-to-twin equality carried from round 1: project.html and the twin are "
        "byte-identical since 95f3f8cb.",
        None,
    ),
    "labs-project-2": (
        "PASS",
        "run_labs CS2 --page project: PASS (3/3) (gates_mid_r1.txt); twin tests/labs/CS2/lab-CS2-project-2.py run alone "
        "with python -I -W error: rc=0. Page-to-twin equality carried from round 1 (byte-identical since 95f3f8cb).",
        None,
    ),
    "labs-project-3": (
        "PASS",
        "run_labs CS2 --page project: PASS (3/3) (gates_mid_r1.txt); twin tests/labs/CS2/lab-CS2-project-3.py run alone "
        "with python -I -W error: rc=0. Page-to-twin equality carried from round 1 (byte-identical since 95f3f8cb).",
        None,
    ),
    "grader-alternatives": (
        "PASS",
        "Eight alt_r15 alternatives (ledgers/CS2/scripts/CS2-d-r15/alts/alt_r15_A..E, both variants of A, B and C) run "
        "on seeds 0-49 by run_alts_r1.py through tools/run_graders.py workspace/run_suite: every file '50/50 seeds pass; "
        "failing seeds: []' (ledgers/CS2/scripts/CS2-d-r1/alts_r15_current_0-49_r1.txt).",
        None,
    ),
    "grader-alt-r12-A-F": (
        "PASS",
        "Round-12 A, B, F, G run directly on seeds 0-49: 50/50 each (alts_r12_ABFG_current_r1.txt). Round-12 C, D, E and "
        "alt_r7_06 must be repointed: the committed copies import reference.py from the deleted worktree "
        "verifyF11-CS2-d and fail with '1 error' (0/50) in this checkout. Repointed copies in "
        "ledgers/CS2/scripts/CS2-d-r1/alts_repointed_current_r1/ (path changed to this checkout, nothing else) pass 50/50 "
        "each (alts_repointed_current_0-49_r1.txt).",
        None,
    ),
    "grader-guarantee-battery": (
        "PASS",
        "Battery ledgers/CS2/scripts/CS2-d-r15/guarantee_battery_r15.py run with python -I on the current paths: "
        "reference.py checks=15300 violations=0; equivalent/r15_04 checks=15300 violations=0; equivalent/r15_06 "
        "checks=15300 violations=0 (guarantee_battery_r1_currentpaths.txt). Measurement only, not a proof. A prefix-wise "
        "search (every add, exact probes, 43,688 exhaustive small streams and 120 long streams, eps 0.2 and 0.3 exhaustive, 0.1 to 0.3 random) gave 0 "
        "violations for reference, r15_04 and r15_06 (r15_04_06_extra.txt).",
        None,
    ),
    "mut-survivors": (
        "PASS",
        "mutate_CS2_0-9_r1.txt (this round): KILLED r12f_10_sketch_refuses_negative_values.py, "
        "r7_02_sketch_drops_repeated_values.py, r8v_02_welford_mean_rounded_to_six_places.py and "
        "r9v_03_sketch_new_tuple_delta_drops_successor_delta.py. Their files are byte-identical since 95f3f8cb.",
        None,
    ),
    "equiv-m14_01": (
        "PASS",
        "Re-read the changed README (ledgers/CS2/equivalent/README.md, diff 95f3f8cb..HEAD: notation paragraph, Lemma 3 "
        "variable renamed x to t, band definition added, r15 sections, Status). The m14_01 section is unchanged and its "
        "argument holds: every stored g >= 1, so the first tuple's running rank is >= 1 and any target <= 1 returns "
        "values[0] in both versions. rank_target_without_clamp.py is byte-identical to 95f3f8cb. It passes the grader "
        "on seeds 0-9 (175 passed each, this round), so it is a survivor the README correctly places in equivalent/.",
        None,
    ),
    "grader-new-mutants": (
        "FAIL",
        "New mutants in ledgers/CS2/mutants/ this round: r14_01..03 and r15_01..03, r15_05, r15_08 (eight). All eight are "
        "KILLED on seeds 0-9 (mutate_CS2_0-9_r1.txt). Ruling 9 requires that the first docstring line names the student "
        "error. The first docstring line of r15_05_sample_variance_one_value_zero_division.py and "
        "r15_08_quantile_target_float_q_times_n.py is 'Reference solution for the CS2 streaming statistics library "
        "(streamstats.py).' (line 1 of each file; the mutate log prints the same line as the description). r15_04, "
        "r15_06 and r15_07 were given student-error first lines in 2a805c83 and now sit in equivalent/.",
        "Replace the first docstring line of ledgers/CS2/mutants/r15_05_sample_variance_one_value_zero_division.py and "
        "ledgers/CS2/mutants/r15_08_quantile_target_float_q_times_n.py with a line that names the student error (for "
        "example: 'Sample variance of one value divides by zero instead of raising ValueError.'), then re-run "
        "tools/mutate_graders.py --unit CS2 --seeds 0-9.",
    ),
    "mut-r15-survivors": (
        "FAIL",
        "r15_07_welford_nan_checked_after_state_change.py is a non-equivalent survivor, moved to equivalent/ on an "
        "invalid basis. Direct run (r15_checks.txt, part A): after update(5.0) and a refused update(nan), the reference "
        "raises ValueError for variance(1) with one value added, and r15_07 returns nan without raising, and its count "
        "is 2 and its mean() is nan. project.html:209 names condition (2): variance(1) when fewer than two values have "
        "been added raises ValueError. project.html:216 Conventions (Welford): after n values the mean is mean() and both "
        "statistics describe every value added so far. The README basis (project.html:209 says nothing about state "
        "after a refusal) is therefore wrong. The grader suite does not kill it: test_project.py, 175 passed on each of "
        "seeds 0-9 with r15_07 as streamstats.py (r15_checks; this round). r15_04 and r15_06 are split out to row "
        "equiv-r15-04-06-proof.",
        "Add a test to grader/test_project.py: after update(5.0) and a refused update(nan) that raises ValueError, "
        "variance(1) still raises ValueError (condition 2) and mean() == 5.0 (Conventions). Confirm it fails on r15_07 and "
        "passes on reference for seeds 0-49. Move r15_07 back to ledgers/CS2/mutants/ with a student-error first docstring "
        "line, remove its README section, and update the grader count stated at project.html:211 if the count changes. "
        "This is a grader change: run the full CS2 gate.",
    ),
    "equiv-r15-04-06-proof": (
        "FAIL",
        "New row (split from mut-r15-survivors). equivalent/r15_04_sketch_interior_delta_without_minus_one.py and "
        "equivalent/r15_06_sketch_interior_delta_is_floor_2en.py are filed as equivalent with the README's own words "
        "'measured, not proved'. Ruling 9 requires a README proof for a move to equivalent/. The README gives no proof: "
        "its Lemma 2 (band bound) does not cover them, because the new interior band is g_s + Delta_s + 1 for r15_04 "
        "(README r15_04 section) and 1 + floor(2 eps n) for r15_06, and the README says so. Searches found no violation: "
        "15300 battery checks per module (final state only), and in r15_04_06_extra.txt 43,688 exhaustive small streams "
        "and 120 long random streams, checked after every add, 0 violations for reference, r15_04 and r15_06. These are "
        "measurements. Ruling 26 counts an unproved statement as a defect, and the README Status claim that none of them "
        "violates the specification is unproved for these two.",
        "Either prove the rank guarantee (Conventions, both inequalities, after every add) for r15_04 and r15_06 with a "
        "weaker invariant that replaces Lemma 2 for these two variants, or find a counterexample and kill it with a grader "
        "test and move the file back to ledgers/CS2/mutants/. Then update the README Status and rerun this delta.",
    ),
}

new_rows = []
for rid, r in base_rows.items():
    if rid in fresh:
        status, evidence, fix = fresh[rid]
        row = {k: r[k] for k in ("id", "check", "location")}
        row.update(status=status, evidence=evidence)
        if fix:
            row["fix"] = fix
        new_rows.append(row)
    else:
        row = {k: r[k] for k in ("id", "check", "location")}
        row.update(status="PASS", evidence=CARRY_PREFIX + r["evidence"])
        new_rows.append(row)
    if rid == "mut-r15-survivors":
        extra = {"id": "equiv-r15-04-06-proof"}
        status, evidence, fix = fresh["equiv-r15-04-06-proof"]
        extra.update(check="2.6-mutation: equivalent/ move needs a README proof (ruling 9); split from mut-r15-survivors",
                     location="ledgers/CS2/equivalent/README.md (r15_04, r15_06 sections; Status); "
                              "ledgers/CS2/equivalent/r15_04_*.py, r15_06_*.py",
                     status=status, evidence=evidence, fix=fix)
        new_rows.append(extra)

# Mutants: 178 KILLED in mutants/ from this round's log, plus the three files moved to equivalent/.
mut_rows = []
for line in open(f"{ROOT}/{S}/mutate_CS2_0-9_r1.txt", encoding="utf-8"):
    m = re.match(r"^KILLED (\S+\.py): (.*) -> (\S+) \(seed (\d+)\)$", line.strip())
    if m:
        mut_rows.append({
            "id": m.group(1)[:-3],
            "description": m.group(2),
            "file": f"ledgers/CS2/mutants/{m.group(1)}",
            "killed_by": f"{m.group(3)} (seed {m.group(4)})",
        })
assert len(mut_rows) == 178, len(mut_rows)
for name, desc in [
    ("r15_04_sketch_interior_delta_without_minus_one", "Quantile sketch sets an inserted interior tuple's delta to g + delta of its successor, dropping the minus one."),
    ("r15_06_sketch_interior_delta_is_floor_2en", "Quantile sketch sets an inserted interior tuple's delta to floor(2 epsilon n), not the successor's g + delta - 1."),
    ("r15_07_welford_nan_checked_after_state_change", "Welford update checks for NaN only after it has changed count, mean and M2, so a refused NaN leaves state altered."),
]:
    mut_rows.append({
        "id": name,
        "description": desc,
        "file": f"ledgers/CS2/equivalent/{name}.py",
        "killed_by": None,
        "disposition": "moved to equivalent/ in 2a805c83; survives all 175 checks on seeds 0-9 (this round)",
    })

now = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
counts = {"PASS": 0, "FAIL": 0}
for r in new_rows:
    counts[r["status"]] += 1
verdict = "PASS" if counts["FAIL"] == 0 and len(new_rows) and all(r["status"] == "PASS" for r in new_rows) else "FAIL"
fragment = {
    "unit": "CS2",
    "slice": "d",
    "round": 1,
    "verifier": "independent verifier (Haiku), CS2 slice d, round 1: closing delta verification (rulings 30, 37); did not build CS2",
    "pin": "2a805c831410ab77c38c227f7e121e8537193ce9",
    "base": "95f3f8cb21c2cd9fc904430bd30a6b734d01f672",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyG1-CS2-d",
    "scratch": S,
    "verified_at": now,
    "verdict": verdict,
    "rows": new_rows,
    "mutants": mut_rows,
    "registry_flags": [],
    "freshness_flags": [
        "The committed round-12 repointed copies ledgers/CS2/scripts/CS2-d-r1/alts_repointed_r1/alt_r12_C_*, alt_r12_D_*, alt_r12_E_* and alt_r7_06_r9path.py hard-code the deleted worktree /Users/billyribeiro/.fanout/wt/verifyF11-CS2-d for reference.py and fail 0/50 in any other checkout. Repointed copies in alts_repointed_current_r1/ pass 50/50. Fix by repointing or retiring the committed copies.",
        "The CS2 delta moved the three sketch survivors from mutants/ to equivalent/ in 2a805c83 and the mutate gate now reads 178/178 only because of it. The mutants/ count is 178, not 181.",
        "ledgers/CS2/equivalent/r15_05 and r15_08 docstring banner: see grader-new-mutants.",
    ],
    "notes": [
        "Delta scope (ruling 30): git diff 95f3f8cb..2a805c83 over the slice paths. Changed: ledgers/CS2/equivalent/README.md; ledgers/CS2/mutants/r15_04, r15_06, r15_07 renamed to ledgers/CS2/equivalent/ with edits (first docstring lines changed to student errors); plans/FINAL-ARCHITECT-RULINGS.md (rulings 38 and 39 appended; text of 30 and 37 unchanged). Byte-identical since 95f3f8cb (git diff --quiet, checked): course/modules/CS/CS2/project.html, course/modules/CS/CS2/grader/*, course/modules/CS/CS2/index.html, tests/labs/CS2/lab-CS2-project-{1,2,3}.py, curriculum/, notation/, references/, plans/KNOWN-ISSUES.md, tools/, ledgers/CS2/scripts/CS2-d-r15/ and -r12/, and the carried equivalent and mutant files.",
        "Re-verified from scratch: every base non-PASS row (gate-mutate-cs2, mut-r15-survivors) and every row whose subject changed (grader-new-mutants, grader-guarantee-battery, grader-alternatives, grader-alt-r12-A-F, equiv-m14_01, mut-survivors, all gate rows). Carried with prefix: 30 rows whose subjects are byte-identical.",
        "The README Lemmas 0 to 3 were re-read after the notation change (x renamed t in Lemma 3) and the band definition added; the Lemma 3 chain (K - 1 <= floor(t), and the sum to floor(t + 2 eps n)) is internally consistent. The d8_01, d9_04 and d8_02 claims were read, not re-derived line by line (no base row carried them separately).",
        "Observation outside the rows (not verified here): course/modules/CS/CS2/cards.json changed in 2a805c83 and belongs to the lesson slices. Lesson pages L04 to L11 are outside slice d.",
        "Blind calibration (ruling 23): the dedicated scorer's file ~/.fanout/blind/CS2-d.json (A [1,1,2,1,1,1], B [3,3,3,4,4,4]) was read, not re-scored. The attribute values in project.html:365 (1,1,2,1,1,1) and :376 (4,4,4,4,4,4) match. The B gap is within one level and is accepted in plans/KNOWN-ISSUES.md (unchanged since 95f3f8cb).",
        "Observation (ruling 30, not a row): the README Status claims 'none violates a behaviour that the specification states' for all seven files, which is false for r15_07 (see mut-r15-survivors).",
    ],
    "summary": (
        f"CS2 slice d round 1 (closing delta, rulings 30 and 37): {verdict}. Rows: {len(new_rows)} "
        f"({counts['PASS']} PASS, {counts['FAIL']} FAIL). Mutants in ledgers/CS2/mutants/: 178 of 178 killed on seeds 0-9. "
        "Three sketch files moved to equivalent/ in 2a805c83: r15_04 and r15_06 lack a proof (equiv-r15-04-06-proof), and "
        "r15_07 is a non-equivalent survivor that the grader does not kill (mut-r15-survivors). "
        "r15_05 and r15_08 have a reference banner as first docstring line (grader-new-mutants). All gates re-run "
        "and PASS."
    ),
}
out = f"{ROOT}/ledgers/CS2/CS2-d.json"
json.dump(fragment, open(out, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
open(out, "a", encoding="utf-8").write("\n")
print("wrote", out, verdict, counts, len(mut_rows))
