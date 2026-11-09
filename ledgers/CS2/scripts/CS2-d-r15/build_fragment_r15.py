"""Build the round-15 CS2 slice-d fragment from the round-14 fragment (carried rows) and this round's evidence."""

import json
import re
from datetime import UTC, datetime
from pathlib import Path

CHECKOUT = Path("/Users/billyribeiro/.fanout/wt/verifyD15-CS2-d")
SCR = "ledgers/CS2/scripts/CS2-d-r15"
PREV = json.loads(Path("/Users/billyribeiro/.fanout/frags/D-CS2-d.round14.json").read_text(encoding="utf-8"))
CARRY = (
    "Carried from round 14 (course/modules/CS/CS2/project.html, grader/instance.py, grader/reference.py, "
    "grader/starter.py, grader/test_project.py and tests/labs/CS2/lab-CS2-project-{1,2,3}.py byte-identical since the "
    "previous pin 1431aa1d, checked by git diff --quiet): "
)
# Rows whose subject is re-run or re-verified this round (new evidence replaces the round-14 evidence).
REFRESHED = {
    "gate-mutate-cs2", "gate-run-graders", "gate-check-projects", "gate-check-dag", "gate-check-pages",
    "gate-run-labs", "gate-page-smoke", "gate-ruff-mypy", "gate-verify-refs", "gate-collect-count",
    "gate-pytest-relevant", "gate-local-pytest", "labs-project-1", "labs-project-2", "labs-project-3",
    "proj-rubric-calibration", "grader-new-mutants", "grader-alternatives", "grader-alt-r12-A-F",
    "grader-guarantee-battery", "mut-survivors",
}
NEW = {
    "row_r15_survivors": None,
}

rows = []
for row in PREV["rows"]:
    rid = row["id"]
    if rid in REFRESHED:
        continue
    if row["status"] != "PASS":
        raise SystemExit(f"unexpected carried non-PASS row {rid}")
    rows.append({"id": rid, "check": row["check"], "location": row["location"], "status": "PASS",
                 "evidence": CARRY + row["evidence"]})

FRESH = {
    "gate-mutate-cs2": (
        "2.6-mutation (tools/mutate_graders.py --unit CS2 --seeds 0-9, all 181 mutants)",
        "ledgers/CS2/mutants/ (181 files, 176 pre-existing + r15_04..08)",
        f"{SCR}/mutate_graders_0-9_all181_r15.txt: 'mutate_graders CS2: FAIL (178/181 killed)', rc=1. "
        f"{SCR}/mutate_graders_0-9_r15.txt (176 pre-existing mutants, run before r15_04..08 existed): 'PASS (176/176 killed)', rc=0. "
        "Of the five new mutants, r15_05 and r15_08 are killed. r15_04, r15_06 and r15_07 survive all ten seeds; they are "
        "classified under row mut-r15-survivors (spec-permitted, not a grader defect under the ruling), so the verifier row is "
        "PASS. The tool's exit status 1 is reported to the architect as an open policy point (see notes)."
    ),
    "gate-run-graders": (
        "2.6-autograder run_graders --unit CS2 --seeds 0-49", "course/modules/CS/CS2/grader/",
        f"{SCR}/run_graders.txt: 'run_graders CS2: PASS (reference 50/50 seeds, slowest 0.3 s)', rc=0."),
    "gate-check-projects": (
        "2.6 check_projects --unit CS2", "course/modules/CS/CS2/project.html",
        f"{SCR}/check_projects.txt: 'check_projects CS2: PASS', rc=0."),
    "gate-check-dag": (
        "2.9 check_dag --unit CS2", "curriculum/01-foundations.yaml CS2 prereqs [CS1, M1]",
        f"{SCR}/check_dag.txt: 'check_dag CS2: PASS', rc=0."),
    "gate-check-pages": (
        "2.9 check_pages --unit CS2", "course/modules/CS/CS2/",
        f"{SCR}/check_pages.txt: 'check_pages CS2: PASS', rc=0 (the CS2 lesson pages changed since the previous pin; re-run)."),
    "gate-run-labs": (
        "2.5 run_labs --unit CS2 --page project", "tests/labs/CS2/lab-CS2-project-{1,2,3}.py",
        f"{SCR}/run_labs_project.txt: 'run_labs CS2: PASS (3/3)', rc=0."),
    "gate-page-smoke": (
        "2.9 page_smoke --unit CS2 --pages project", "course/modules/CS/CS2/project.html",
        f"{SCR}/page_smoke_project.txt: 'page_smoke modules/CS/CS2/project.html: PASS', 'page_smoke CS2: PASS', "
        "in-browser grader 'All 175 tests pass', rc=0."),
    "gate-ruff-mypy": (
        "2.9 ruff check ., ruff format --check ., mypy --no-incremental", "whole repository (incl. grader/, tests/labs/CS2/, ledgers/CS2/mutants/)",
        f"{SCR}/ruff_check.txt: 'All checks passed!', rc=0; {SCR}/ruff_format.txt: '554 files already formatted', rc=0; "
        f"{SCR}/mypy.txt: 'Success: no issues found in 385 source files', rc=0."),
    "gate-verify-refs": (
        "2.1 verify_refs --offline", "references/references.json",
        f"{SCR}/verify_refs_offline.txt: 'offline integrity: 560 entries, 0 problems', rc=0. The live run was not repeated: "
        "references/ is unchanged since the previous pin (git diff --name-only is empty for references/)."),
    "gate-collect-count": (
        "2.6 pytest --collect-only on test_project.py", "course/modules/CS/CS2/grader/test_project.py",
        "Collect in a temporary workspace (reference as streamstats.py): '175 tests collected'. The page states 175 (project.html:210-211)."),
    "gate-pytest-relevant": (
        "relevant pytest: -k CS2 over tests/test_labs.py, tests/test_page_smoke.py, tests/test_page_checks.py",
        "tests/test_labs.py, tests/test_page_smoke.py, tests/test_page_checks.py",
        f"{SCR}/pytest_k_CS2.txt: 14 tests, all passing, rc=0."),
    "gate-local-pytest": (
        "2.6 local pytest on the reference (-p no:cacheprovider --assert=plain -W error, QF_SEED=0)",
        "course/modules/CS/CS2/grader/test_project.py",
        f"{SCR}/local_pytest_reference_seed0_r15.txt: '175 passed in 0.17s', rc=0."),
    "labs-project-1": (
        "2.5 lab, rung 1 (lab-CS2-project-1): twin alone under python -I -W error, and run_labs", "course/modules/CS/CS2/project.html:53-146",
        "tests/labs/CS2/lab-CS2-project-1.py run alone: rc=0. run_labs: PASS (3/3). Page code and twin byte-identical to the "
        "previous pin (project.html and the twin are unchanged; carried)."),
    "labs-project-2": (
        "2.5 lab, rung 2 completion (lab-CS2-project-2): twin alone under python -I -W error, and run_labs",
        "course/modules/CS/CS2/project.html:148-189",
        "tests/labs/CS2/lab-CS2-project-2.py run alone: rc=0 (3 lines). run_labs: PASS (3/3)."),
    "labs-project-3": (
        "2.5 lab, rung 3 reference numbers (lab-CS2-project-3): twin alone under python -I -W error, and run_labs",
        "course/modules/CS/CS2/project.html:260-340",
        "tests/labs/CS2/lab-CS2-project-3.py run alone: rc=0; output 'count 11', 'exact mean 10004.181818', 'welford mean within 1e-9 of exact: True', "
        "'the 5th smallest value is 10003.2'. run_labs: PASS (3/3)."),
    "proj-rubric-calibration": (
        "2.6 rubric calibration (exemplars scored blind by the dedicated scorer, ruling 23)",
        "course/modules/CS/CS2/project.html:365 (exemplar-a data-scores=1,1,2,1,1,1), :376 (exemplar-b data-scores=4,4,4,4,4,4)",
        "Blind scorer output ~/.fanout/blind/CS2-d.json: A = 1,1,2,1,1,1 (exact match to exemplar-a data-scores); B = 3,3,3,4,4,4 "
        "against 4,4,4,4,4,4 (C1, C2, C3 one level below official; C4 to C6 exact). VERIFIER_RULES.md:127-129 requires each "
        "score within one level on every criterion: met for both exemplars. The scorer's notes say the B judgement calls are "
        "C1 (H1 and H3 cited only in the closing sentence), C2 (squared-sum expansion not named) and C3 (sample-variance "
        "conversion not carried through). NOTE: the blind file cites plans/KNOWN-ISSUES.md as the architect's acceptance of "
        "the one-level gap; that file (27 lines) has no CS2 or calibration entry (grep for CS2, calibrat, exemplar, one level, "
        "within: no match). The PASS rests on the VERIFIER_RULES.md tolerance, not on that citation."),
    "grader-new-mutants": (
        "2.6-mutation: at least three new student-error mutants of my own",
        "ledgers/CS2/mutants/r14_01..03 and r15_04..08",
        f"Mutants r14_01..03 (committed since the pin): killed in the 181-mutant run ({SCR}/mutate_graders_0-9_all181_r15.txt). "
        f"Five new mutants of my own written by {SCR}/gen_r15.py from grader/reference.py: r15_04 (interior delta without - 1), "
        "r15_05 (variance guard count < 1, ZeroDivisionError), r15_06 (interior delta = floor(2 eps (n+1))), r15_07 (NaN check after "
        "state change), r15_08 (float q times n target). Results (harness.py, seeds 0-9, "
        f"{SCR}/new_mutants_r15.txt): r15_05 killed by test_welford_sample_variance_of_one_value_raises; r15_08 killed by "
        "test_sketch_rank_target_is_exact_where_a_float_target_is_one_short; r15_04, r15_06, r15_07 survive (see mut-r15-survivors)."),
    "grader-alternatives": (
        "2.6-autograder: correct alternatives pass (over-constraint check), seeds 0-49",
        f"{SCR}/alts/alt_r15_A..E (five, written this round)",
        f"{SCR}/alts_r15_results.txt: alt_r15_A_exact_sorted_storage 50/50, alt_r15_B_decimal_exact_target 50/50, "
        "alt_r15_C_float_cutoff_no_floor 50/50, alt_r15_D_welford_alt_arithmetic 50/50, alt_r15_E_rolling_list_bruteforce 50/50. "
        "Prior-round alternatives re-run on the current suite (ledgers/CS2/scripts/CS2-d-r12/alts/*.py and "
        "ledgers/CS2/scripts/CS2-d-r14/alts/alt_r14_*.py, output in prior_alts_rerun_r15.txt): all pass 50/50 except the "
        "path-dependent alt_r12_C, alt_r12_D, alt_r12_E and alt_r7_06 (row grader-alt-r12-A-F) and make_alts_r14.py, which is a "
        "generator script and not an alternative."),
    "grader-alt-r12-A-F": (
        "2.6 round-12 alternatives A-G and round-14 alternatives re-run on the current suite",
        f"ledgers/CS2/scripts/CS2-d-r12/alts/ and ledgers/CS2/scripts/CS2-d-r14/alts_repointed_r14/",
        f"Committed alt_r12_C, alt_r12_D, alt_r12_E and alt_r7_06 load reference.py from deleted worktrees (verifyD12-CS2-d, "
        "verifyD14-CS2-d, verifyB12-CS2-d); as committed they fail at import (0/50, harness.py). Repointed copies in "
        f"{SCR}/alts_repointed_d15/ (path replaced by the current checkout's reference.py) pass 50/50 each "
        f"({SCR}/alts_repointed_d15_results.txt). alt_r12_A, alt_r12_B, alt_r12_F, alt_r12_G pass 50/50 "
        f"({SCR}/prior_alts_rerun_r15.txt)."),
    "grader-guarantee-battery": (
        "2.6 rank guarantee battery (exact Fraction counts, spec Conventions; epsilons 0.05-0.5; 15300 checks per module)",
        "course/modules/CS/CS2/grader/reference.py; ledgers/CS2/mutants/r15_04, r15_06",
        f"{SCR}/guarantee_battery_r15.txt: reference.py 'checks=15300 violations=0'; r15_04 'violations=0'; r15_06 'violations=0'. "
        "Monotonicity in q also checked."),
    "mut-survivors": (
        "2.6-mutation: earlier survivors at seeds 0-1 are killed in the window",
        "ledgers/CS2/mutants/r12f_10, r7_02, r8v_02, r9v_03",
        f"{SCR}/mutate_graders_0-9_all181_r15.txt: KILLED r12f_10_sketch_refuses_negative_values.py, KILLED r7_02_sketch_drops_repeated_values.py, "
        "KILLED r8v_02_welford_mean_rounded_to_six_places.py, KILLED r9v_03_sketch_new_tuple_delta_drops_successor_delta.py."),
}

for rid, (check, location, evidence) in FRESH.items():
    rows.append({"id": rid, "check": check, "location": location, "status": "PASS", "evidence": evidence})

rows.append({
    "id": "mut-r15-survivors",
    "check": "2.6-mutation: surviving new grader mutants are FAIL only if project.html, the plan or the contract states the behaviour they violate (ruling)",
    "location": "project.html:209 (Constraints), project.html:218 (rank guarantee bullet, memory sentence)",
    "status": "PASS",
    "evidence": (
        f"r15_04 (interior tuple delta without - 1) and r15_06 (interior delta floor(2 eps (n+1))) satisfy the spec's only sketch "
        f"requirement, the rank guarantee: {SCR}/guarantee_battery_r15.txt, 15300 exact checks each, 0 violations, and "
        "project.html:218 says 'The specification does not bound the memory of the sketch, and the autograder does not test "
        "memory.' Both differ only in memory (compression), so no stated behaviour is violated. r15_07 (update(NaN) raises "
        "ValueError but has already incremented count and set mean to NaN) raises the named ValueError (project.html:209 "
        "condition 3); the spec states no state after a rejected call (project.html:209 says only that 'No method changes the "
        "value it is given, and each class holds its state in the object only'), so no stated behaviour is violated. Under the "
        "ruling these are not FAIL rows. Because mutate_graders.py counts them as survivors, the tool exits 1."
    ),
})

mutants = []
text = (CHECKOUT / SCR / "mutate_graders_0-9_all181_r15.txt").read_text(encoding="utf-8")
new_desc = {
    "r15_04_sketch_interior_delta_without_minus_one": "Sketch: a new interior tuple takes delta = g + delta of its successor (the rule has - 1). SURVIVES; spec-permitted (row mut-r15-survivors).",
    "r15_05_sample_variance_one_value_zero_division": "Welford variance(1): the guard tests count < 1, so one value reaches a division by zero (ZeroDivisionError, not ValueError).",
    "r15_06_sketch_interior_delta_is_floor_2en": "Sketch: a new interior tuple takes delta = floor(2 * epsilon * (n+1)) (the cap) instead of the successor rule. SURVIVES; spec-permitted (row mut-r15-survivors).",
    "r15_07_welford_nan_checked_after_state_change": "Welford update: the NaN check runs after count and M2 have changed, so a rejected NaN leaves count incremented and mean NaN. SURVIVES; spec-permitted (row mut-r15-survivors).",
    "r15_08_quantile_target_float_q_times_n": "Sketch quantile: the rank target is computed as q * n - epsilon * n in floats (q is a float, not a Fraction).",
}
for line in text.splitlines():
    m = re.match(r"^(KILLED|SURVIVED) ([^:]+): (.*)$", line)
    if not m:
        continue
    status, fname, rest = m.groups()
    stem = fname.removesuffix(".py")
    if " -> " in rest:
        desc, killed = rest.rsplit(" -> ", 1)
    else:
        desc, killed = rest, ""
    if stem in new_desc:
        desc = new_desc[stem]
    if status == "KILLED":
        killed_by = killed.strip()
    else:
        killed_by = ""
    mutants.append({"id": stem, "description": desc.strip(), "killed_by": killed_by})
assert len(mutants) == 181, len(mutants)

out = {
    "unit": "CS2",
    "slice": "d",
    "round": 15,
    "verifier": "independent verifier (Haiku), round 15; did not build CS2",
    "pin": "dde0486beeb0312e4ac1cc03aaa02e56644adb24",
    "base": "1431aa1d842a5d2d05fd5953c098500bf78a4307",
    "checkout": str(CHECKOUT),
    "scratch": SCR,
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "verdict": "PASS",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [
        "The committed alternatives alt_r12_C_shifted_sums_brute_window.py, alt_r12_D_weighted_exact_list.py, alt_r12_E_reference_cap_no_plus_one.py (ledgers/CS2/scripts/CS2-d-r12/alts/) and alt_r7_06_r9path.py (both r12 and r14 copies) read reference.py from worktrees that no longer exist (verifyD12-CS2-d, verifyD14-CS2-d, verifyB12-CS2-d). They fail at import as committed; repointed copies in ledgers/CS2/scripts/CS2-d-r15/alts_repointed_d15/ pass.",
        "plans/KNOWN-ISSUES.md does not contain the CS2 calibration acceptance that the blind scorer file and the task cite; the only tolerance rule is VERIFIER_RULES.md:127-129 (within one level on every criterion), which the blind scores meet.",
    ],
    "notes": [
        "Scope: slice d of CS2 (project.html, grader/, the three project labs, ledgers/CS2/mutants/ and the alternatives). Delta since the round-14 pin 1431aa1d, measured with git diff: project.html, grader/*.py and tests/labs/CS2/lab-CS2-project-{1,2,3}.py are byte-identical (no hunks), so their PASS rows are carried. In the slice, the delta is three committed mutants (r14_01..03, 143 lines each) and the alternatives/scripts directories; all are re-verified here.",
        "Outside the slice (not verified here): the lesson twins tests/labs/CS2/lab-CS2-L01-1.py, L03, L04 and L06 changed; their pages (course/modules/CS/CS2/L01..L11.html, index.html, cards.json) changed; these belong to the lesson slices. I ran the four changed lesson twins alone under python -I -W error: rc=0 each. No changes in curriculum/, notation/, references/ or tools/ since the pin.",
        "Calibration: the row is PASS on the dedicated blind scorer's output (ruling 23) and the within-one-level rule. I did not read the exemplar annotations for scoring; I read data-scores (project.html:365, :376) only to compare with the scorer's numbers.",
        "Gate tool status: tools/mutate_graders.py --unit CS2 exits 1 with 178/181 killed. The three survivors (r15_04, r15_06, r15_07) are spec-permitted under the ruling (row mut-r15-survivors). The architect must decide whether spec-permitted survivors are accepted (the tool has no such category) or whether the mutants are moved or the tool changed. ledger.merge counts them as unkilled, so the merged CS2 verdict stays FAIL until that decision.",
        "Output path: the committed ledgers/CS2/CS2-d.json held another lineage's round-15 fragment (pin 448548f9); it is overwritten as the task requires. The tracked files in ledgers/CS2/scripts/CS2-d-r15/ (alts/alt_r15_A_exact_list_sketch.py, alt_r15_B_m2_textbook_form.py, alt_r15_C_rolling_brute_scan.py, cards_check.py, guarantee_battery.py, lab_equal.py, mutate_full.txt, naive_offsets.py, run_alt.sh, write_fragment.py) predate this round and were not modified; this round's files have different names.",
        "Not run: live verify_refs (references unchanged since the pin); cards and the other slices' pages; the full repository gate (scope limited to this slice; the unit-level gates above were run). No git commit or push. No course, tool, test, reference, curriculum or atlas file was edited.",
    ],
    "summary": "",
}
pass_n = sum(1 for r in rows if r["status"] == "PASS")
out["summary"] = (
    f"CS2 slice d round 15: PASS on the rows ({pass_n}/{len(rows)} PASS). Mutants: {len(mutants)} listed, "
    f"{sum(1 for m in mutants if m['killed_by'])} killed; 3 new survivors (r15_04, r15_06, r15_07) are spec-permitted "
    "(row mut-r15-survivors). The mutate_graders tool itself exits 1 on them (see notes)."
)
Path(CHECKOUT / "ledgers/CS2/CS2-d.json").write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("rows", len(rows), "PASS", pass_n, "mutants", len(mutants), "killed", sum(1 for m in mutants if m["killed_by"]))
