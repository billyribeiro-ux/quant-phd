"""Build ledgers/CS2/CS2-d.json (round 1, closing delta verification of slice d).

Carried rows come from the base fragment (pin dde0486b), each with the carry prefix; re-verified rows carry this
round's evidence. Mutant list comes from the scratch log of tools/mutate_graders.py --unit CS2 --seeds 0-9.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

CHECKOUT = Path("/Users/billyribeiro/.fanout/wt/verifyF11-CS2-d")
SCRATCH = "ledgers/CS2/scripts/CS2-d-r1"
BASE_FRAGMENT = Path("/Users/billyribeiro/.fanout/frags/D-CS2-d.round15.json")
BASE_PIN = "dde0486beeb0312e4ac1cc03aaa02e56644adb24"
HEAD_PIN = "95f3f8cb21c2cd9fc904430bd30a6b734d01f672"

CARRY_FILES = (
    "course/modules/CS/CS2/project.html, course/modules/CS/CS2/grader/ (instance.py, reference.py, starter.py, "
    "test_project.py), tests/labs/CS2/lab-CS2-project-{1,2,3}.py"
)
CARRY_PREFIX = (
    f"Carried from round 15 ({CARRY_FILES} byte-identical since the previous pin {BASE_PIN[:8]}, "
    "checked by git diff --quiet over those paths): "
)

base = json.loads(BASE_FRAGMENT.read_text(encoding="utf-8"))
base_rows = {r["id"]: r for r in base["rows"]}

RE_VERIFIED: dict[str, dict[str, str]] = {
    "gate-mutate-cs2": {
        "status": "FAIL",
        "evidence": (
            f"tools/mutate_graders.py --unit CS2 --seeds 0-9 at pin {HEAD_PIN[:8]} (exit 1; log {SCRATCH}/mutate_CS2_0-9.txt, "
            "final line 'mutate_graders CS2: FAIL (178/181 killed)'). Survived: r15_04_sketch_interior_delta_without_minus_one.py, "
            "r15_06_sketch_interior_delta_is_floor_2en.py, r15_07_welford_nan_checked_after_state_change.py. The other 178 "
            "mutants in ledgers/CS2/mutants/ are killed (176 pre-existing plus r15_05 and r15_08)."
        ),
        "fix": (
            "Move r15_04, r15_06 and r15_07 from ledgers/CS2/mutants/ to ledgers/CS2/equivalent/ with a README section each "
            "(ruling 9; ruling 37 forbids new mutants in the closing round). r15_07 changes count, mean and M2 before its NaN "
            "check; project.html:209 states only that the named ValueError is raised, not the state after a refusal. "
            "r15_04 and r15_06 change only the sketch's internal delta; project.html:218 states only the rank guarantee, and "
            "guarantee_battery_r1.txt shows 0 violations in 15300 checks each (measured, not proved: state that in the README, "
            "ruling 25). Update the first sentence of ledgers/CS2/equivalent/README.md ('Four mutants survive') to the new count. "
            "Then re-run tools/mutate_graders.py --unit CS2 --seeds 0-9 and expect 'mutate_graders CS2: PASS (178/178 killed)'."
        ),
    },
    "mut-r15-survivors": {
        "status": "FAIL",
        "evidence": (
            "Ruling 9 ('never leave a survivor in ledgers/<UNIT>/mutants/') and ruling 37 (the closing round checks that new "
            "survivors are killed by tests the fixer adds) are both unmet: r15_04, r15_06 and r15_07 are still in mutants/ "
            f"({SCRATCH}/mutate_CS2_0-9.txt, SURVIVED lines), and course/modules/CS/CS2/grader/ is byte-identical to "
            f"{BASE_PIN[:8]} (git diff --quiet), so no test was added. Violation check of the stated behaviour (verifier rule): "
            f"guarantee_battery_r1.txt gives 0 violations for reference.py, r15_04 and r15_06 over 15300 exact-Fraction checks "
            "each; r15_07 changes only object state after a refused NaN, which project.html:209 does not state, and it raises "
            "the named ValueError. So no survivor violates a stated behaviour, and the survivors belong in equivalent/."
        ),
        "fix": (
            "Apply the move in gate-mutate-cs2 (equivalent/ with README proofs, ruling 9). Do not add a test for r15_07: a test "
            "that the state is unchanged after a refused NaN would constrain behaviour the page does not state. If the architect "
            "instead decides that the page must state the post-refusal state, write that sentence in project.html, add a "
            "grader test that kills r15_07, and re-run the grader gates (the grader then changes)."
        ),
    },
    "grader-new-mutants": {
        "status": "PASS",
        "evidence": (
            "Five new single-change mutants exist at pin HEAD and not at dde0486b (git ls-tree): ledgers/CS2/mutants/"
            "r15_04..r15_08. Each differs from course/modules/CS/CS2/grader/reference.py by one line (diff, reference.py:116 "
            "for r15_04 and r15_06, :47 for r15_05, the update() body for r15_07, :137 for r15_08): a student-error candidate "
            f"each. r15_05 and r15_08 are killed (mutate_CS2_0-9.txt: test_welford_sample_variance_of_one_value_raises, "
            "test_sketch_rank_guarantee_at_wide_epsilon[0.3]). Observation, not a ruling-26 kind: the first docstring line of "
            "all five says 'Reference solution for the CS2 streaming statistics library', not the student error (ruling 9); see notes."
        ),
    },
    "grader-alternatives": {
        "status": "PASS",
        "evidence": (
            "Five alternatives of different styles (alt_r15_A_exact_sorted_storage, alt_r15_B_decimal_exact_target, "
            "alt_r15_C_float_cutoff_no_floor, alt_r15_D_welford_alt_arithmetic, alt_r15_E_rolling_list_bruteforce), and the "
            "three older alt_r15 A/B/C variants, run on seeds 0-49 by ledgers/CS2/scripts/CS2-d-r1/run_alts_r1.py (which calls "
            "tools/run_graders.py panel/workspace/run_suite of this checkout): every file '50/50 seeds pass; failing seeds: []' "
            f"({SCRATCH}/alts_r15_and_repointed_0-49.txt). Alternative C is a float-cutoff compression whose target is still "
            "computed with Fraction (exact rank target as Conventions requires), so it is not a wrong-on-exact-rule mutant (ruling 10)."
        ),
    },
    "grader-alt-r12-A-F": {
        "status": "PASS",
        "evidence": (
            "Round-12 alternatives A, B, F, G (ledgers/CS2/scripts/CS2-d-r12/alts/) run directly on seeds 0-49: 50/50 each "
            f"({SCRATCH}/alts_r12_ABFG_0-49.txt). Round-12 C, D, E and alt_r7_06_r9path run from repointed copies in "
            f"{SCRATCH}/alts_repointed_r1/ (the reference path is changed to this checkout, nothing else): 50/50 each "
            f"({SCRATCH}/alts_repointed_r1_0-49.txt). The committed copies hard-code deleted worktrees (see freshness_flags)."
        ),
    },
    "grader-guarantee-battery": {
        "status": "PASS",
        "evidence": (
            "tracked battery ledgers/CS2/scripts/CS2-d-r15/guarantee_battery_r15.py (copied unchanged to "
            f"{SCRATCH}/guarantee_battery_r1_copy.py), run with python -I by this round on the reference and on the two sketch "
            f"survivors: reference.py checks=15300 violations=0; r15_04 checks=15300 violations=0; r15_06 checks=15300 "
            f"violations=0 ({SCRATCH}/guarantee_battery_r1.txt). This is a measured sweep, not a proof."
        ),
    },
    "mut-survivors": {
        "status": "PASS",
        "evidence": (
            f"{SCRATCH}/mutate_CS2_0-9.txt (run this round): KILLED r12f_10_sketch_refuses_negative_values.py (seed 0), "
            "KILLED r7_02_sketch_drops_repeated_values.py (seed 0), KILLED r8v_02_welford_mean_rounded_to_six_places.py (seed 0), "
            "KILLED r9v_03_sketch_new_tuple_delta_drops_successor_delta.py (seed 0). Earlier survivors at seeds 0-1 are killed "
            "within the window."
        ),
    },
    "gate-run-graders": {
        "status": "PASS",
        "evidence": (
            "tools/run_graders.py --unit CS2 --seeds 0-49: 'run_graders CS2: PASS (reference 50/50 seeds, slowest 0.3 s)', rc=0 "
            f"({SCRATCH}/run_graders_CS2_0-49.txt)."
        ),
    },
    "gate-check-projects": {
        "status": "PASS",
        "evidence": f"tools/check_projects.py --unit CS2: 'check_projects CS2: PASS', rc=0 ({SCRATCH}/check_projects_CS2.txt).",
    },
    "gate-check-dag": {
        "status": "PASS",
        "evidence": f"tools/check_dag.py --unit CS2: 'check_dag CS2: PASS', rc=0 ({SCRATCH}/check_dag_CS2.txt).",
    },
    "gate-check-pages": {
        "status": "PASS",
        "evidence": (
            "tools/check_pages.py --unit CS2 (course/modules/CS/CS2 changed: L04-L11 and cards.json): 'check_pages CS2: PASS', "
            f"rc=0 ({SCRATCH}/check_pages_CS2.txt)."
        ),
    },
    "gate-run-labs": {
        "status": "PASS",
        "evidence": f"tools/run_labs.py --unit CS2 --page project: 'run_labs CS2: PASS (3/3)', rc=0 ({SCRATCH}/run_labs_CS2_project.txt).",
    },
    "gate-page-smoke": {
        "status": "PASS",
        "evidence": (
            f"tools/page_smoke.py --unit CS2 --pages project: 'page_smoke CS2: PASS', rc=0 ({SCRATCH}/page_smoke_CS2_project.txt)."
        ),
    },
    "gate-ruff-mypy": {
        "status": "PASS",
        "evidence": (
            f"ruff check . : 'All checks passed!' rc=0 ({SCRATCH}/ruff_check.txt); ruff format --check . : '555 files already "
            f"formatted' rc=0 ({SCRATCH}/ruff_format.txt); mypy --no-incremental: 'Success: no issues found in 386 source files' "
            f"rc=0 ({SCRATCH}/mypy.txt)."
        ),
    },
    "gate-verify-refs": {
        "status": "PASS",
        "evidence": f"tools/verify_refs.py --offline: 'offline integrity: 560 entries, 0 problems', rc=0 ({SCRATCH}/verify_refs_offline.txt).",
    },
    "gate-collect-count": {
        "status": "PASS",
        "evidence": (
            "pytest --collect-only -q on course/modules/CS/CS2/grader/test_project.py in a workspace (instance.py and "
            "reference.py copied as streamstats.py, as tools/run_graders.py does): '175 tests collected' for QF_SEED=0 and "
            f"QF_SEED=49 ({SCRATCH}/collect_count_seeds_0_49.txt). project.html:211 states 175. (Direct collection in the grader "
            f"directory fails on the missing streamstats module, {SCRATCH}/collect_test_project.txt, as expected without the workspace copy.)"
        ),
    },
    "gate-pytest-relevant": {
        "status": "PASS",
        "evidence": (
            "pytest -p no:cacheprovider -q -k CS2 tests/test_labs.py tests/test_page_smoke.py tests/test_page_checks.py: rc=0 "
            f"({SCRATCH}/pytest_k_CS2_r1.txt)."
        ),
    },
    "gate-local-pytest": {
        "status": "PASS",
        "evidence": (
            "workspace copy of reference as streamstats.py, env -i PATH QF_SEED=0 PYTHONHASHSEED=0, python -I -W error -m pytest "
            f"--assert=plain -W error -q -p no:cacheprovider test_project.py: '175 passed', rc=0 ({SCRATCH}/local_pytest_reference_seed0_r1.txt)."
        ),
    },
    "labs-project-1": {
        "status": "PASS",
        "evidence": (
            "tests/labs/CS2/lab-CS2-project-1.py run alone under python -I -W error from a scratch cwd: rc=0, stderr empty, 15 "
            f"stdout lines ({SCRATCH}/twins_project_1-3_python_I_W_error.txt); run_labs 3/3 (gate-run-labs)."
        ),
    },
    "labs-project-2": {
        "status": "PASS",
        "evidence": (
            "tests/labs/CS2/lab-CS2-project-2.py alone under python -I -W error: rc=0, stderr empty, 3 stdout lines "
            f"({SCRATCH}/twins_project_1-3_python_I_W_error.txt); run_labs 3/3."
        ),
    },
    "labs-project-3": {
        "status": "PASS",
        "evidence": (
            "tests/labs/CS2/lab-CS2-project-3.py alone under python -I -W error: rc=0, stderr empty, 9 stdout lines "
            f"({SCRATCH}/twins_project_1-3_python_I_W_error.txt); run_labs 3/3."
        ),
    },
    "proj-rubric-calibration": {
        "status": "PASS",
        "evidence": (
            "Blind scores by the dedicated scorer (ruling 23), ~/.fanout/blind/CS2-d.json: A [1,1,2,1,1,1], B [3,3,3,4,4,4]. "
            "Official data-scores in project.html:365 '1,1,2,1,1,1' and :376 '4,4,4,4,4,4' (grep of the attribute only). "
            "Every criterion is within one level (ruling 15 and VERIFIER_RULES tolerance). The B differences on C1, C2, C3 are "
            "listed as accepted in plans/KNOWN-ISSUES.md (section 'Rubric calibration', CS2 B row), which is present at pin HEAD. "
            "project.html is byte-identical to dde0486b, so the blind scores apply to these bytes."
        ),
    },
}

# Mutant descriptions: the tool prints the first docstring line; for the five r15 mutants that line is the reference
# banner, so the description is the student error taken from the one-line diff against reference.py.
MUTANT_DESCRIPTION_OVERRIDE = {
    "r15_04_sketch_interior_delta_without_minus_one": "Sketch interior insert sets delta = g + Delta of the successor, omitting the - 1 of reference.py:116.",
    "r15_05_sample_variance_one_value_zero_division": "variance(1) with one value is not refused: the guard reads count < 1, so one value divides by zero.",
    "r15_06_sketch_interior_delta_is_floor_2en": "Sketch interior insert sets delta = floor(2 eps (n + 1)) instead of g + Delta - 1 (reference.py:116).",
    "r15_07_welford_nan_checked_after_state_change": "update() adds the value to count, mean and M2 before the NaN check, so a refused NaN leaves the state changed.",
    "r15_08_quantile_target_float_q_times_n": "quantile() forms the rank target from float q times n, not Fraction(q) times n (reference.py:137).",
}

LOG_RE = re.compile(r"^(KILLED|SURVIVED) (\S+?): (.*) -> (.*)$")


def parse_mutants() -> list[dict[str, object]]:
    mutants: list[dict[str, object]] = []
    seen: set[str] = set()
    for line in (CHECKOUT / SCRATCH / "mutate_CS2_0-9.txt").read_text(encoding="utf-8").splitlines():
        m = LOG_RE.match(line)
        if not m:
            continue
        outcome, filename, description, killed = m.groups()
        stem = filename.removesuffix(".py")
        if stem in seen:
            continue
        seen.add(stem)
        description = MUTANT_DESCRIPTION_OVERRIDE.get(stem, description)
        mutants.append(
            {
                "id": stem,
                "description": description,
                "killed_by": None if outcome == "SURVIVED" else killed,
                "outcome": "survived" if outcome == "SURVIVED" else "killed",
            }
        )
    return mutants


def main() -> int:
    rows: list[dict[str, str]] = []
    carried = 0
    for row in base["rows"]:
        rid = row["id"]
        if rid in RE_VERIFIED:
            spec = RE_VERIFIED[rid]
            new = {
                "id": rid,
                "check": row["check"],
                "location": row["location"],
                "status": spec["status"],
                "evidence": spec["evidence"],
            }
            if spec["status"] != "PASS":
                new["fix"] = spec["fix"]
            rows.append(new)
        else:
            carried += 1
            rows.append(
                {
                    "id": rid,
                    "check": row["check"],
                    "location": row["location"],
                    "status": "PASS",
                    "evidence": CARRY_PREFIX + row["evidence"],
                }
            )
    missing = set(RE_VERIFIED) - set(base_rows)
    if missing:
        raise SystemExit(f"re-verified ids not in base: {sorted(missing)}")
    statuses = [r["status"] for r in rows]
    verdict = "PASS" if all(s == "PASS" for s in statuses) else "FAIL"
    mutants = parse_mutants()
    killed = sum(1 for m in mutants if m["killed_by"])

    fragment = {
        "unit": "CS2",
        "slice": "d",
        "round": 1,
        "verifier": "independent verifier (Haiku), CS2 slice d, round 1: closing delta verification (rulings 30, 37); did not build CS2",
        "pin": HEAD_PIN,
        "base": BASE_PIN,
        "checkout": str(CHECKOUT),
        "scratch": SCRATCH,
        "verified_at": "2026-11-09T15:33:52+00:00",
        "verdict": verdict,
        "rows": rows,
        "mutants": mutants,
        "registry_flags": [],
        "freshness_flags": [
            "Committed alternatives ledgers/CS2/scripts/CS2-d-r12/alts/alt_r12_C_shifted_sums_brute_window.py, alt_r12_D_weighted_exact_list.py, "
            "alt_r12_E_reference_cap_no_plus_one.py and alt_r7_06_r9path.py, the copies in ledgers/CS2/scripts/CS2-d-r14/alts_repointed_r14/ and "
            "ledgers/CS2/scripts/CS2-d-r15/alts_repointed_d15/ (path only changed in my copies) import reference.py from deleted worktrees "
            "(grep: verifyB12, verifyD12, verifyD14 and verifyD15-CS2-d; verifyD15-CS2-d is absent, and the committed r15 copies fail at "
            "import with '1 error', 0/50). Repointed copies in "
            f"{SCRATCH}/alts_repointed_r1/ pass 50/50. Fix the committed copies or retire them.",
            "ledgers/CS2/scripts/CS2-d-r15/run_alt.sh hard-codes /Users/billyribeiro/.fanout/wt/verifyB15-CS2-d (not used this round).",
            "plans/KNOWN-ISSUES.md now carries the CS2 blind-calibration row (the round-15 freshness flag on it is resolved).",
            "ledgers/CS2/CS2-d.json and ledgers/CS2/scripts/CS2-d-r1/ were tracked from other lineages before this round; this round overwrote "
            "ledgers/CS2/CS2-d.json and added only new file names under ledgers/CS2/scripts/CS2-d-r1/.",
        ],
        "notes": [
            "Delta scope (ruling 30): git diff dde0486b..95f3f8cb over the slice paths. Byte-identical since dde0486b (git diff --quiet): "
            "course/modules/CS/CS2/project.html, course/modules/CS/CS2/grader/*, tests/labs/CS2/lab-CS2-project-{1,2,3}.py, "
            "tools/, curriculum/, notation/, references/, ledgers/CS2/equivalent/. Changed in slice: ledgers/CS2/mutants/r15_04..r15_08 "
            "(five new files), ledgers/CS2/scripts/CS2-d-r15/alts/ and alts_repointed_d15/ (new files). Rows whose subject changed were "
            "re-verified from scratch; the rest are carried with the carry prefix.",
            "Outside slice d (not verified here, observation only): lesson pages course/modules/CS/CS2/L04..L11.html, cards.json, lesson twins "
            "tests/labs/CS2/lab-CS2-L04-1.py, L06, L07, plans/FINAL-ARCHITECT-RULINGS.md (rulings 30 to 37 added; ruling 9 text unchanged), "
            "plans/KNOWN-ISSUES.md, tests/test_lx1_project_lab3.py and other units. Those belong to the lesson slices.",
            "Mutant docstrings (observation, not a ruling-26 kind): the first docstring line of r15_04..r15_08 is the reference banner "
            "'Reference solution for the CS2 streaming statistics library', not the student error required by ruling 9. The fixer should "
            "replace that line when moving the mutants. The log descriptions for those five are overridden in this fragment.",
            "Rank-guarantee battery (ledgers/CS2/scripts/CS2-d-r15/guarantee_battery_r15.py): 15300 exact-Fraction checks per module, 0 "
            "violations for the reference, r15_04 and r15_06. This is evidence for the moved-to-equivalent proofs, not a proof.",
            "Calibration: the blind scorer's output was cited (~/.fanout/blind/CS2-d.json). This verifier did not score the exemplars and "
            "did not read the annotation text; only the data-scores attribute was grepped.",
            "Gate outcome: tools/mutate_graders.py --unit CS2 exits 1 (178/181). Under ruling 26 that is a failing gate, so the slice is "
            "not accepted this round. The fix is listed on gate-mutate-cs2; after it, a delta round is needed (ruling 30).",
        ],
        "summary": (
            f"CS2 slice d round 1 (closing delta, rulings 30 and 37): {verdict}. Rows: {len(rows)} "
            f"({sum(1 for s in statuses if s == 'PASS')} PASS, {sum(1 for s in statuses if s != 'PASS')} FAIL; "
            f"{carried} carried from round 15, {len(RE_VERIFIED)} re-verified). Mutants: {len(mutants)} listed, {killed} killed, "
            f"{len(mutants) - killed} survivors (r15_04, r15_06, r15_07). FAIL rows: gate-mutate-cs2 and mut-r15-survivors, both on the "
            "three survivors in mutants/ (ruling 9 and ruling 37)."
        ),
    }
    out = CHECKOUT / "ledgers/CS2/CS2-d.json"
    out.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {out}: rows={len(rows)} carried={carried} re-verified={len(RE_VERIFIED)} verdict={verdict} "
          f"mutants={len(mutants)} killed={killed}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
