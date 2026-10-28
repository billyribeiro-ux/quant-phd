"""Builds ledgers/AC1/AC1-d.json (round 14) from the round-13 fragment and round-14 evidence.

Every round-13 row id is kept. A round-13 PASS row is carried only when its subject files are byte-identical
since eaf6d87 (the round-13 pin); rows whose subject is in the delta are re-verified with new evidence.
"""

import json
import re
import sys
from pathlib import Path

CHK = Path("/tmp/verify14-AC1-d")
OUT = Path("/tmp/v14d")
PREV = json.loads(Path("/tmp/fanout-frags/AC1-d.round13.json").read_text())
MUT = {}
for line in (OUT / "mutants_r14.out").read_text().splitlines():
    name, rest = line.split(" | ", 1)
    s0 = re.search(r"seed0: (\d+) failed", rest)
    s17 = re.search(r"seed17: (\d+) failed", rest)
    first = rest.split("first: ", 1)[1] if "first: " in rest else ""
    MUT[name] = (int(s0.group(1)) if s0 else 0, int(s17.group(1)) if s17 else 0, first)


def killed(name: str) -> bool:
    s0, s17, _ = MUT[name]
    return s0 > 0 and s17 > 0


def mutant_ids(location: str) -> list[str]:
    ids: list[str] = []
    for token in re.findall(r"\b(?:m\d{2,3}|fx\d{2})(?:-(?:m\d{2,3}|fx\d{2}))?", location):
        if "-" in token:
            a, b = token.split("-")
            if a.startswith("fx"):
                ids += [f"fx{i:02d}" for i in range(int(a[2:]), int(b[2:]) + 1)]
            else:
                ids += [f"m{i:02d}" for i in range(int(a[1:]), int(b[1:]) + 1)]
        else:
            ids.append(token)
    return ids


def stems_for(prefix: str) -> list[str]:
    return sorted(n for n in MUT if n.split("_")[0] == prefix)


def group_row(row_id: str, location: str, check: str) -> dict:
    ids = mutant_ids(location)
    names: list[str] = []
    for i in ids:
        names += stems_for(i)
    names = sorted(set(names))
    dead = [n for n in names if not killed(n)]
    lines = "; ".join(f"{n} {MUT[n][0]}/{MUT[n][1]} failed (seed 0/seed 17)" for n in names)
    status = "PASS" if names and not dead else "FAIL"
    return {
        "id": row_id,
        "check": check,
        "location": location,
        "status": status,
        "evidence": f"Re-run this round (ledgers/AC1/scripts/AC1-d-r14/run_mutants.sh -> /tmp/v14d/mutants_r14.out): "
        f"{len(names)} files, every one fails on seed 0 and seed 17" if status == "PASS" else
        f"survivors on seeds 0 and 17: {dead}",
        **({"fix": "Add the missing boundary case to the grader."} if status != "PASS" else {}),
    }


DELTA_HUNKS = "grader/test_project.py outside the hunks at lines 306-314 and 998-1001"
CARRY_SET = {
    "project": "project.html outside lines 368 and 398",
    "cards": "cards.json, L01-L08.html, index.html, grader/reference.py, grader/instance.py, grader/starter.py, "
    "tests/labs/AC1 and tests/test_*.py",
}

prev_rows = {r["id"]: r for r in PREV["rows"]}

RE_VERIFIED = {}


def put(row_id: str, status: str, check: str, location: str, evidence: str, fix: str | None = None) -> None:
    row = {"id": row_id, "check": check, "location": location, "status": status, "evidence": evidence}
    if fix:
        row["fix"] = fix
    RE_VERIFIED[row_id] = row


put("proj-run-graders", "PASS", "2.6-autograder-reference", "course/modules/AC/AC1/grader/ (reference.py, test_project.py, instance.py)",
    "Re-run: tools/run_graders.py --unit AC1 --seeds 0-49 -> 'run_graders AC1: PASS (reference 50/50 seeds, slowest 0.3 s)' (/tmp/v14d/run_graders.out). Also 50 seeds run with ledgers/AC1/scripts/AC1-d-r14/run_suite.sh on grader/reference.py: '274 passed' on every seed (/tmp/v14d/ref_50.out: 50 of 50 lines '274 passed').")
put("proj-collect-count-176", "PASS", "2.6-collect-count", "project.html line 368 ('collects 274 checks'); grader/test_project.py",
    "Re-run: `pytest --collect-only` (run_suite.sh ... collect) on reference.py for seeds 0 through 49: '274 tests collected' on 50 of 50 seeds (/tmp/v14d/ref_50.out). project.html line 368 says 274 and 'the count is 274 for each of the seeds 0 to 49': matches. The round-13 value 265 is gone from the page.")
put("proj-local-suite-reference", "PASS", "2.6-local-suite", "grader/test_project.py; project.html 'Running the suite locally' (line 412-415)",
    "Re-run: run_suite.sh with QF_SEED=s, pytest -q -p no:cacheprovider --assert=plain -W error test_project.py on reference.py: '274 passed' for s in 0..49 (/tmp/v14d/ref_50.out). On grader/starter.py: '272 failed, 2 passed' (seed 0, /tmp/v14d/st0 run), so the suite fails on the starter as project.html says at line 364.")
put("proj-pyodide-smoke", "PASS", "2.5-page-smoke", "course/modules/AC/AC1/project.html; L01.html, L02.html, L03.html",
    "Re-run: `tools/page_smoke.py --unit AC1 --pages project.html` -> 'page_smoke AC1: PASS' (/tmp/v14d/smoke_project.out); `--pages L01.html L02.html L03.html` -> 'page_smoke AC1: PASS' (/tmp/v14d/smoke_L.out).")
put("proj-check-pages", "PASS", "2.9-structure", "course/modules/AC/AC1/*.html; cards.json",
    "Re-run: `tools/check_pages.py --all` -> the AC1 line reads 'check_pages AC1: PASS' (/tmp/v14d/check_pages.out, rc=0).")
put("proj-check-projects", "PASS", "2.9-structure", "course/modules/AC/AC1/project.html (budget, rungs)",
    "Re-run: `tools/check_projects.py --all` rc=0; 'check_projects AC1: PASS' (/tmp/v14d/check_projects.out).")
put("proj-check-dag", "PASS", "DAG", "project.html 'Concepts used here'; L01-L03 concept definitions",
    "Re-run: `tools/check_dag.py --all` rc=0; 'check_dag AC1: PASS' (/tmp/v14d/check_dag.out). The delta changed project.html line 368 and line 398 only; neither introduces a concept use.")
put("proj-run-labs", "PASS", "2.5-labs", "tests/labs/AC1/lab-AC1-project-1.py, -project-2.py, -project-3.py, and the L01-L08 twins",
    "Re-run: `tools/run_labs.py --unit AC1` -> 'run_labs AC1: PASS (11/11)' (/tmp/v14d/run_labs.out). Twins run directly under `python -I -W error` (/tmp/v14d/twin_lab-AC1-*.out): project-1 rc=0 (last line 'ending cash equals the February balance sheet cash: True'), project-2 rc=0 ('retained change 700000 earnings gap 0'), project-3 rc=0 ('ending cash less balance sheet cash: 0'), L02 rc=0 ('lowest cash balance at any year end (USD): 3,000,000.00'), L03 rc=0 ('checks 1 to 4 hold in every year: True').")
put("proj-lab-twin-embed", "PASS", "2.5-labs", "project.html lab blocks (Lab 1 56-253, Lab 2 260-343, Lab 3 420-518); L02.html and L03.html lab blocks; tests/labs/AC1",
    "run_labs AC1 (above) checks each page lab against its twin: 11/11. project.html lines 368 and 398 are the only changed project.html lines, outside the lab blocks.")
put("proj-labs-ruff", "PASS", "gate", "tests/labs/AC1; course/modules/AC/AC1/grader",
    "Re-run: `.venv/bin/ruff check tests/labs/AC1 course/modules/AC/AC1/grader` -> 'All checks passed!' (/tmp/v14d/ruff.out); `ruff format --check` -> '15 files already formatted'.")
put("proj-mypy-gate", "PASS", "gate", "tests/labs/AC1; course/modules/AC/AC1/grader",
    "Re-run: `.venv/bin/mypy --no-incremental tests/labs/AC1 course/modules/AC/AC1/grader` -> 'Success: no issues found in 15 source files' (/tmp/v14d/mypy.out).")
put("proj-verify-refs", "PASS", "2.1-citations", "references/references.json; project.html (data-cite penman2013financial)",
    "Re-run: `tools/verify_refs.py --offline` -> 'offline integrity: 560 entries, 0 problems'; `tools/verify_refs.py --unit AC1` (live) -> 'live re-verification of AC1: 2 of 560 entries, 0 problems' (/tmp/v14d/vr_live.out, rc=0).")
put("proj-hours", "PASS", "hours", "project.html line 33 (data-hours-project 30) and the time-budget table (lines 386-398); index.html lines 29 and 148",
    "Re-computed: the time-budget rows sum to 1+3+4+4+3+5+2+5+3 = 30, equal to the 'Total 30' cell and to data-hours-project 30. index.html (byte-identical since eaf6d87) declares data-hours-lessons 90 and data-hours-project 30 and says the hours 'sum to the 90 lesson hours' (line 148). The delta changed only the wording of the row 'Local runs on other seeds' (line 398) and its hours cell (3) is unchanged. Hours are design targets (architect ruling): no pace check.")
put("proj-prose-banned", "PASS", "1.2/1.3-banned-phrases", "project.html line 368 and 398; grader/test_project.py added lines (306-314, 998-1001); cards.json unchanged",
    "Re-run: the 12 added lines of `git diff eaf6d87 cef676e -- course/modules/AC/AC1 tests/labs/AC1` scanned for roughly|about|historically|typically|usually|approximately|ellipsis|half|most|generally|often|tends|always: none found. Scope words in the added lines, read in context: 'never adjusted' (grader comment at test_project.py line 309; backed by project.html line 366 'Money is never converted and never adjusted' and by the new test passing on the reference and on 20 alternatives); 'names no upper limit' (grader comment; project.html line 366 names no limit); 'can expose that' (project.html line 398; hedged).")
put("proj-alt-implementations", "PASS", "2.6-over-constraint (architect ruling b)", "course/modules/AC/AC1/grader/test_project.py (whole suite) against twenty correct alternatives",
    "Re-run this round, 50 seeds each, '274 passed' 50/50 for all 20: round-14 alt_r14_a_ledger_class.py, alt_r14_b_ordinals_prefix.py (ordinal days, bisect prefix sums, integer check by type name), alt_r14_c_exclusive_cutoff.py (exclusive next-day cutoff, float rejected); round-13 alt_r13_a/b/c; round-12 alt_r12_a/b/c; round-11 alt_r11 x3; round-10 alts_all x8 (ledgers/AC1/scripts/AC1-d-r14/alts and the earlier AC1-d-r10..r13 alts directories; /tmp/v14d/alts/summary.txt). First run of alt_r14_b failed on the chart-of-accounts type (a dict was needed; my bug, fixed before recording) and its 'set(line) <' check was a bug in my alternative, fixed before recording.")
put("proj-overconstraint-nonmapping", "PASS", "2.6-over-constraint (architect ruling b)", "grader/test_project.py test_post_raises_a_value_error parametrize list; project.html line 366",
    "Re-verified: the float-with-a-fraction-of-a-cent case (debit 5.5) is still in test_post_raises_a_value_error and names the condition 'an amount that is not an integer, including a boolean or a float such as 100.0' (project.html line 366). All 20 alternatives pass it.")
put("proj-mutants-set-killed", "FAIL", "2.5-mutation (project slice)", "ledgers/AC1/mutants/ (117 files after this round)",
    "Re-run all 117 files (ledgers/AC1/scripts/AC1-d-r14/run_mutants.sh -> /tmp/v14d/mutants_r14.out): 115 fail on seed 0 and seed 17. Two survive both seeds: m102_century_blind_leap_year (274 passed on seed 0 and 17) and m104_leap_rule_without_400_rule (274 passed on seed 0 and 17). Each is a FAIL row of its own (proj-r14-mutant-m102, proj-r14-mutant-m104). The round-13 survivor m90 is now killed (proj-mutant-m90-amount-cap-survives).",
    "Fix the two grader gaps in proj-r14-mutant-m102 and proj-r14-mutant-m104; then the set is fully killed.")
put("proj-mutant-m90-amount-cap-survives", "PASS", "2.5-mutation (grader survivor, round 13)", "ledgers/AC1/mutants/m90_amount_cap_one_million_dollars.py; grader/test_project.py test_a_large_amount_posts_at_its_full_value (added this delta, line 309-313)",
    f"Re-run: m90 (cap at 100,000,000 cents) fails on seed 0 and seed 17 ({MUT['m90_amount_cap_one_million_dollars'][0]} and {MUT['m90_amount_cap_one_million_dollars'][1]} failed); the first failure is test_a_large_amount_posts_at_its_full_value. The round-13 FAIL is resolved by the delta (the added test posts 10**12 cents). Re-run output: /tmp/v14d/mutants_r14.out.")
put("proj-page-spec-carry-post-cases", "PASS", "2.6-over-constraint", "grader/test_project.py test_post_raises_a_value_error parametrize list (added cases) and the new test at lines 309-313",
    "Re-verified: the new test test_a_large_amount_posts_at_its_full_value checks a valid posting (balanced, non-negative integers); it names no error. The new dates in test_period_end_must_be_a_month_end ('2023-02-29', '2024-13-31') are invalid calendar dates and raise ValueError (a real calendar date is not a month end). All 20 alternatives pass both.")
put("proj-no-expected-value-leak", "PASS", "2.6-spec", "project.html line 368 ('A failing check names the property that failed and never prints the expected value'); grader/test_project.py _check_values (lines 224-236)",
    "Re-verified: _check_values (test_project.py lines 224-236) fails with 'the {what} for {end} has no {key} entry', 'must be an integer number of cents', or 'does not follow the definition in the specification': key names only, no expected or actual values. The new test uses _check_values.")
put("proj-grader-carry", "PASS", "2.6-grader", "grader/test_project.py (delta hunks at lines 309-313 and 1001-1002, 39 lines added in round 13 and 10 lines in this delta)",
    "Delta read in full (git diff eaf6d87 cef676e -- grader/test_project.py): one new test (lines 309-313: a balanced entry of 10**12 cents on cash and common_stock, checked against four keys with _check_values) and two added period-end strings ('2023-02-29', '2024-13-31'). Nothing removed. Round-13 hunks unchanged. Unchanged lines were exercised by the 50-seed sweep (274 passed on the reference).")
put("proj-line-368-grading-claims", "PASS", "2.9-prose", "project.html line 368 (Grading mode)",
    "Re-verified (changed line): '274 checks' = collect count on 50 of 50 seeds; 'seeds 0 to 49' = the sweep; 'warnings as errors' = run_suite.sh with -W error; named coverage: 'an entry that balances only with another entry' (test_post_raises_a_value_error case); 'a one-cent entry' (test_a_one_cent_entry_posts_at_one_cent); 'an entry of 1,000,000,000,000 cents' (test_a_large_amount_posts_at_its_full_value, 10**12); 'a zero on one side of a line'; 'a repeated entry'; 'two entries on one date'; 'an empty list of transactions'; 'entries dated 1 January, 31 December and 29 February' (year-edge and leap-day tests). 'boundary cases' is read as the extremes of the named ranges; the 10**12 case is the upper extreme of an unbounded amount (no limit is named on the page).")
put("proj-r14-line-398-wording", "PASS", "2.9-prose", "project.html line 398 (Time-budget row 'Local runs on other seeds')",
    "Re-verified: the sentence says running on other seeds 'can expose' a solution that hard-codes its answer, which is a hedged claim. Evidence that a seed-specific answer fails on other seeds: m05_seed0_cash_hardcoded fails on seed 0 (2 failed) and on seed 17 (5 failed) in /tmp/v14d/mutants_r14.out. The row's hours cell (3) is unchanged.")
put("proj-r14-test-large-amount", "PASS", "2.6-spec and over-constraint", "grader/test_project.py test_a_large_amount_posts_at_its_full_value (lines 309-313); project.html line 368",
    "The test posts a balanced entry of 10**12 cents and checks four balance-sheet keys. Passes on the reference (274/274, 50 seeds) and on all 20 alternatives (50 seeds each), so it is not over-constraining. It kills the cap mutants m90 (cap 10**8) and m98 (cap ten million dollars) and the int32 cap m101 (2,147,483,647 cents).")
put("proj-r14-mutant-m101", "PASS", "2.5-mutation (new mutant, round 14)", "ledgers/AC1/mutants/m101_int32_amount_cap.py",
    f"Student error: an int32-style cap on every amount ('if value > 2_147_483_647: raise ValueError'). Killed on seed 0 ({MUT['m101_int32_amount_cap'][0]} failed) and seed 17 ({MUT['m101_int32_amount_cap'][1]} failed) and on 50 of 50 seeds. Reason: test_a_large_amount_posts_at_its_full_value. A survivor would be a spec violation (project.html line 366: 'Money is never converted and never adjusted'), so it must be killed.")
put("proj-r14-mutant-m103", "PASS", "2.5-mutation (new mutant, round 14)", "ledgers/AC1/mutants/m103_amount_rounded_to_whole_dollars.py",
    f"Student error: each amount rounded to whole dollars ('int(round(value, -2))'). Killed on seed 0 ({MUT['m103_amount_rounded_to_whole_dollars'][0]} failed), seed 17 ({MUT['m103_amount_rounded_to_whole_dollars'][1]} failed) and on 50 of 50 seeds.")
put("proj-r14-mutant-m102", "FAIL", "2.5-mutation (new survivor, round 14)", "ledgers/AC1/mutants/m102_century_blind_leap_year.py; grader/test_project.py test_period_end_must_be_a_month_end (no 1900 or 2100 case); project.html line 366",
    "Student error: the month-end check uses a leap rule 'year % 4 == 0' with no century rule. It passes 274 of 274 on all 50 seeds (50/50, /tmp/v14d/n/m102sweep). Probe (ledgers/AC1/scripts/AC1-d-r14/out/century_probe.py): the mutant raises ValueError for '2100-02-28' ('a period end must be the last day of a calendar month'), while the reference accepts 2100-02-28. project.html line 366 defines a period end as 'the last day of a calendar month' and a date as 'a real calendar date'; 2100-02-28 is the last day of February 2100, so the mutant violates the stated spec and no test catches it.",
    "Add to test_a_non_leap_year_february_end_is_accepted (or a new test): balance_sheet(post(TXS), '2100-02-28') returns the all-zero dict (accepted), and balance_sheet(..., '2100-02-29') raises ValueError. Then re-run the 50-seed sweep and m102 must fail on every seed.")
put("proj-r14-mutant-m104", "FAIL", "2.5-mutation (new survivor, round 14)", "ledgers/AC1/mutants/m104_leap_rule_without_400_rule.py; grader/test_project.py test_a_leap_year_month_end_is_accepted (2024 only)",
    "Student error: the leap rule 'year % 4 == 0 and year % 100 != 0' (no 400-year rule). It passes 274 of 274 on all 50 seeds (50/50, /tmp/v14d/n/m104). Probe: the mutant raises ValueError for '2000-02-29' (a real month end, accepted by the reference; 2000 is divisible by 400). Spec: project.html line 366 ('the last day of a calendar month' and 'a real calendar date'). The grader never tests a century year.",
    "Add a test that balance_sheet(..., '2000-02-29') is accepted, together with the 2100 cases in the m102 fix. Then m104 must fail on every seed.")
put("proj-r14-alternatives-new", "PASS", "2.6-over-constraint (architect ruling b)", "ledgers/AC1/scripts/AC1-d-r14/alts/alt_r14_a_ledger_class.py, alt_r14_b_ordinals_prefix.py, alt_r14_c_exclusive_cutoff.py",
    "Three new correct implementations, each 274/274 on 50 of 50 seeds (ledgers/AC1/scripts/AC1-d-r14/out/alts_summary_r14.txt). They use a class ledger with string cutoffs (A), ordinal days with bisect prefix sums and a next-day month-end test (B), and an exclusive next-day cutoff with floats rejected (C).")

for mid in ["m09", "m10"]:
    pass

FAIL_IDS = {"proj-r14-mutant-m102", "proj-r14-mutant-m104"}
groups = {
    "proj-mutants-m01-m08": ("ledgers/AC1/mutants/ m01-m08", "2.5-mutation"),
    "proj-mutants-m11-m20": ("ledgers/AC1/mutants/ m11-m20", "2.5-mutation"),
    "proj-mutants-m21-m25": ("ledgers/AC1/mutants/ m21-m25", "2.5-mutation"),
    "proj-mutants-m33-m38": ("ledgers/AC1/mutants/ m33-m38", "2.5-mutation"),
    "proj-mutants-new-r10-m58-m61": ("ledgers/AC1/mutants/ m58-m61", "2.5-mutation"),
    "proj-mutants-new-r9-three-written": ("ledgers/AC1/mutants/ m45-m47", "2.5-mutation"),
    "proj-mutants-new-m26-m28": ("ledgers/AC1/mutants/ m26-m57", "2.5-mutation"),
    "proj-mutants-m62-m71-fixer": ("ledgers/AC1/mutants/ m62-m71", "2.5-mutation"),
    "proj-mutants-new-r11-m72-m75": ("ledgers/AC1/mutants/ m72-m75", "2.5-mutation"),
    "proj-mutants-new-r12-m86-m89": ("ledgers/AC1/mutants/ m86-m89", "2.5-mutation"),
    "proj-mutants-new-r13-m91-m93": ("ledgers/AC1/mutants/ m91-m93", "2.5-mutation"),
    "proj-mutants-fx01-fx10": ("ledgers/AC1/mutants/ fx01-fx10", "2.5-mutation"),
}
for rid, (loc, chk) in groups.items():
    RE_VERIFIED[rid] = group_row(rid, loc, chk)

for rid, old in prev_rows.items():
    if rid.startswith("proj-mutant-") and rid != "proj-mutant-m90-amount-cap-survives":
        num = re.search(r"-m(\d{2})-", rid).group(1)
        matches = [n for n in MUT if n.startswith(f"m{num}_")]
        if len(matches) != 1:
            raise SystemExit(f"{rid}: {len(matches)} files match m{num}_")
        stem = matches[0]
        s0, s17, first = MUT[stem]
        cited = old["location"].split()[0].rstrip(";")
        corrected = f"ledgers/AC1/mutants/{stem}.py"
        note = "" if cited == corrected else (
            f" Location corrected in round 14: the round-13 path '{cited}' does not exist in the checkout; "
            f"the file for this mutant is '{corrected}' (same m-number, same mutation).")
        RE_VERIFIED[rid] = {
            "id": rid, "check": old["check"], "location": corrected, "status": "PASS" if killed(stem) else "FAIL",
            "evidence": f"Re-run this round (/tmp/v14d/mutants_r14.out): {stem} fails on seed 0 ({s0} failed) and seed 17 ({s17} failed); first failure {first}.{note}",
            **({} if killed(stem) else {"fix": "Add a grader case that rejects this error."}),
        }

# Carry rules: a round-13 PASS row is carried when its subject is outside the delta.
DELTA_PROJECT_LINES = {368, 398}
def carry(rid: str, old: dict) -> dict:
    loc = old["location"]
    if "project.html" in loc:
        subject = CARRY_SET["project"]
    elif "grader" in loc or "test_project" in loc:
        subject = DELTA_HUNKS
    else:
        subject = CARRY_SET["cards"]
    prefix = f"Carried from round 13 ({subject} byte-identical since the previous pin eaf6d87):"
    return {"id": rid, "check": old["check"], "location": loc, "status": old["status"],
            "evidence": f"{prefix} {old['evidence']}"}

rows = []
for rid, old in prev_rows.items():
    if rid in RE_VERIFIED:
        rows.append(RE_VERIFIED[rid])
    elif old["status"] == "PASS":
        rows.append(carry(rid, old))
    else:
        raise SystemExit(f"unhandled non-PASS previous row {rid}")

ids = [r["id"] for r in rows]
assert len(ids) == len(set(ids)), "duplicate row id"
for rid in RE_VERIFIED:
    if rid not in prev_rows:
        rows.append(RE_VERIFIED[rid])
assert len({r["id"] for r in rows}) == len(rows)
missing = set(prev_rows) - {r["id"] for r in rows}
assert not missing, missing

mutants = []
for stem in sorted(MUT):
    s0, s17, _ = MUT[stem]
    file_ = f"ledgers/AC1/mutants/{stem}.py"
    mutants.append({
        "id": stem,
        "description": stem.split("_", 1)[1].replace("_", " ") if "_" in stem else stem,
        "file": file_,
        "killed_by": (f"seed 0 and seed 17 (/tmp/v14d/mutants_r14.out: {s0} and {s17} failed)" if killed(stem)
                      else f"SURVIVES seed 0 and seed 17 (see the FAIL row for {stem})"),
    })

fail_count = sum(1 for r in rows if r["status"] != "PASS")
killed_count = sum(1 for m in mutants if killed(Path(m["file"]).stem))
frag = {
    "unit": "AC1",
    "slice": "AC1-d",
    "round": 14,
    "verifier": "Claude Haiku 5.5, independent verifier for AC1-d, round 14; did not build AC1; read the round-13 fragment as context and computed the delta eaf6d87..cef676e on AC1 (project.html lines 368 and 398, grader/test_project.py lines 306-314 and 998-1001, mutants m90-m100 and duplicates, the round-13 scripts)",
    "pin": "cef676e (detached worktree /tmp/verify14-AC1-d)",
    "base": "eaf6d87 (round 13 pin); previous fragment /tmp/fanout-frags/AC1-d.round13.json",
    "checkout": "/tmp/verify14-AC1-d",
    "scratch": "/tmp/v14d/",
    "verified_at": "2026-10-28T15:00:00+00:00",
    "verdict": "FAIL" if fail_count else "PASS",
    "summary": {"rows": len(rows), "PASS": len(rows) - fail_count, "FAIL": fail_count,
                "UNVERIFIABLE": 0, "mutants": len(mutants), "mutants_killed_seed0_and_seed17": killed_count},
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": ("Delta eaf6d87..cef676e on AC1: grader/test_project.py (one new test, two period-end strings), project.html lines 368 "
              "and 398, and mutant files m90-m100 with duplicates. Cards, lessons, index, references, labs, tools and reference/instance/starter are byte-identical since eaf6d87. "
              "Cards: all 128 read (/tmp/v14d/cards_dump.txt); numbers and labels re-checked by script; AC1-c077 '5,000' is written 5{,}000 in L06.html line 67 (not a MISSING). "
              "Carried rows are cited with the round-13 evidence. Round-14 new mutants m101, m103 killed; m102 and m104 survive. Not checked: the full text of L01-L08 was not re-read this round (unchanged since eaf6d87); pytest count of tests/test_*.py not re-run."),
}
dest = CHK / "ledgers/AC1/AC1-d.json"
dest.write_text(json.dumps(frag, indent=1, ensure_ascii=False) + "\n")
print("rows", len(rows), "fail", fail_count, "mutants", len(mutants), "killed", killed_count)
