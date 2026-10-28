"""Builds ledgers/M1/M1-d.json (round 14) from the round-13 fragment plus this round's re-runs.

Rows whose cited subject is byte-identical since the round-13 pin are carried with the required prefix. Rows whose
subject changed in the delta eaf6d87..cef676e (cards.json M1-c142, grader/test_project.py lines 516-528, the mutant
directory) or whose command was re-run carry this round's evidence (outputs under ledgers/M1/scripts/M1-d-r14/).
"""

from __future__ import annotations

import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[4]
PREV = json.loads(pathlib.Path("/tmp/fanout-frags/M1-d.round13.json").read_text(encoding="utf-8"))
OUT = ROOT / "ledgers/M1/M1-d.json"
CARRY = "Carried from round 13 (byte-identical since the previous pin eaf6d87): "
TESTS_CARRY = (
    "Carried from round 13 (grader/test_project.py lines outside 516-528 and project.html unchanged since the previous "
    "pin eaf6d87; the cited tests are outside the delta): "
)
CARDS_CARRY = (
    "Carried from round 13 (the card objects of this lesson are byte-identical; only M1-c142 in lesson L07 changed in "
    "cards.json since the previous pin eaf6d87): "
)
RERUN = "Re-run in round 14 at cef676e: "

NEW: dict[str, dict[str, str]] = {
    "proj-grader-tie-comment-digits": {
        "status": "PASS",
        "location": "course/modules/M/M1/grader/test_project.py lines 516-528 (tie parametrization and docstring)",
        "evidence": RERUN + "the 2.7 comment's float product 462554000 x (0.027/12) is 1040746.4999999999 (Python float), "
        "exact product 2081493/2 = 1040746.5 (Fraction). The 7.2 case: 100000250 x (0.072/12) is 600001.4999999999 "
        "(float), exact 1200003/2 = 600001.5. The comments and the docstring now state the computed arithmetic correctly. "
        "The round-13 FAIL is closed.",
    },
    "proj-r13-tie-test-1-numbers": {
        "status": "PASS",
        "location": "course/modules/M/M1/grader/test_project.py parametrized tie cases (tie-at-2.7-percent, tie-at-7.2-percent)",
        "evidence": RERUN + "case 1 expects 1040747 = floor(2081493/2 + 1/2); case 2 expects 600002 = floor(1200003/2 + 1/2). "
        "The reference passes both; the float variant p*(r/12) rounds down in both.",
    },
    "proj-grader-collect-count": {
        "status": "PASS",
        "location": "course/modules/M/M1/grader/test_project.py; course/modules/M/M1/project.html line 164",
        "evidence": RERUN + "pytest --collect-only in a scratch workspace (test_project.py, instance.py, reference as "
        "annuity_engine.py) prints '196 tests collected'; the page says 'runs 196 checks'.",
    },
    "proj-spec-65-checks": {
        "status": "PASS",
        "location": "course/modules/M/M1/project.html line 164 ('which runs 196 checks'); grader/test_project.py",
        "evidence": RERUN + "196 collected and 196 passed on the reference (scratch workspace, -W error).",
    },
    "proj-grader-mutation-suite": {
        "status": "PASS",
        "location": "ledgers/M1/mutants/ (122 files); tools/mutate_graders.py --unit M1 --seeds 0-9",
        "evidence": RERUN + "'mutate_graders M1: PASS (122/122 killed)', exit 0; output in "
        "ledgers/M1/scripts/M1-d-r14/out/mutate_r14.out (122 KILLED lines, no SURVIVED).",
    },
    "proj-r12-mutant-count": {
        "status": "PASS",
        "location": "ledgers/M1/mutants/ (122 files)",
        "evidence": RERUN + "the directory holds 122 .py files: m01 to m58, r10_01 to r10_10, r11_01 to r11_10, r11d_01 to "
        "r11d_04, r12d_01 to r12d_10, r12v_01 to r12v_04, r13f_01 to r13f_10, r13v_01 to r13v_03, r14d_01 to r14d_10, "
        "r14v_01 to r14v_03; the fragment's mutants list has one entry per file.",
    },
    "proj-r13-mutant-run-observed": {
        "status": "PASS",
        "location": "tools/mutate_graders.py --unit M1 --seeds 0-9",
        "evidence": RERUN + "exit 0, 'mutate_graders M1: PASS (122/122 killed)'.",
    },
    "cards-L07": {
        "status": "PASS",
        "location": "course/modules/M/M1/cards.json, the 24 cards of lesson L07 (M1-c142 changed in the delta)",
        "evidence": RERUN + "M1-c142 back is now 'N = 1, 5, 10, 50, 100, 200 and 400, the seven horizons that Part B "
        "prints.' The lab (tests/labs/M1/lab-M1-L07-1.py, Part B, lines 282-289) loops over exactly (1, 5, 10, 50, 100, "
        "200, 400) and raises AssertionError unless the remainder matches (C/(r-g)) q^N at rel 1e-9 / abs 1e-9; its output "
        "prints seven 'part B: N = ...' rows for those horizons. L07.html line 476 names the same seven horizons. The "
        "removed tolerance wording is still in L07.html line 329, where it matches the lab code. The other 23 L07 cards are "
        "byte-identical.",
    },
    "cards-duplicate-scan": {
        "status": "PASS",
        "location": "course/modules/M/M1/cards.json (179 cards)",
        "evidence": RERUN + "0 duplicate ids, 0 duplicate fronts; one duplicate back, 'No (Lemma 2.2).', on M1-c030 "
        "('Is there an integer t with 2t = 1?') and M1-c173 ('Can an integer be both even and odd?'). The fronts differ, "
        "each card tests one fact, and Lemma 2.2 (L02.html line 97) is the result behind both answers.",
    },
    "cards-numbers-recomputed": {
        "status": "PASS",
        "location": "course/modules/M/M1/cards.json (179 cards)",
        "evidence": RERUN + "per lesson L01 24, L02 26, L03 27, L04 16, L05 20, L06 12, L07 24, L08 30; total 179.",
    },
    "cards-process-and-banned": {
        "status": "PASS",
        "location": "course/modules/M/M1/cards.json; course/modules/M/M1/project.html line 164",
        "evidence": RERUN + "no card front or back contains 'roughly', 'historically', 'round ', 'verifier', 'builder', "
        "'unit report' or 'REQUEST'; the two cards with the word 'about' (M1-c013, M1-c017) use it in its ordinary sense.",
    },
    "proj-mypy-and-pytest-r12": {
        "status": "PASS",
        "location": "mypy --no-incremental (repo); pytest tests/",
        "evidence": RERUN + "'Success: no issues found in 153 source files'; 'python -m pytest -q tests': exit 0, no failures.",
    },
    "proj-grader-lint-types": {
        "status": "PASS",
        "location": "course/modules/M/M1/grader/ (test_project.py, reference.py, starter.py, instance.py)",
        "evidence": RERUN + "ruff check: 'All checks passed!'; ruff format --check: '4 files already formatted'.",
    },
    "proj-grader-reference-50-seeds": {
        "status": "PASS",
        "location": "course/modules/M/M1/grader/reference.py; tools/run_graders.py --unit M1 --seeds 0-49",
        "evidence": RERUN + "'run_graders M1: PASS (reference 50/50 seeds, slowest 0.2 s)', exit 0.",
    },
    "proj-r13-run-graders-0-49": {
        "status": "PASS",
        "location": "course/modules/M/M1/grader/reference.py; tools/run_graders.py --unit M1 --seeds 0-49",
        "evidence": RERUN + "'run_graders M1: PASS (reference 50/50 seeds, slowest 0.2 s)'.",
    },
    "proj-r13-gates": {
        "status": "PASS",
        "location": "tools/check_pages.py --unit M1; tools/check_projects.py --unit M1; tools/check_dag.py --all",
        "evidence": RERUN + "'check_pages M1: PASS', 'check_projects M1: PASS', 'check_dag M1: PASS' (every unit PASS), exit 0.",
    },
    "proj-commands-gate-r12": {
        "status": "PASS",
        "location": "tools/check_pages.py, check_projects.py, check_dag.py, run_labs.py (--unit M1)",
        "evidence": RERUN + "check_pages, check_projects, check_dag all PASS for M1; 'run_labs M1: PASS (11/11)'.",
    },
    "proj-commands-gate-r11": {
        "status": "PASS",
        "location": "tools/check_pages.py, check_projects.py, check_dag.py (--unit M1)",
        "evidence": RERUN + "all three PASS for M1.",
    },
    "proj-commands-gate-r10": {
        "status": "PASS",
        "location": "tools/verify_refs.py --offline; check_pages, check_projects, check_dag, run_labs",
        "evidence": RERUN + "verify_refs --offline: 'offline integrity: 560 entries, 0 problems'; the other commands PASS.",
    },
    "proj-r13-labs-run": {
        "status": "PASS",
        "location": "tools/run_labs.py --unit M1; tests/labs/M1/lab-M1-project-1.py, -2.py, -3.py",
        "evidence": RERUN + "'run_labs M1: PASS (11/11)', exit 0.",
    },
    "proj-lab1-run": {
        "status": "PASS",
        "location": "tests/labs/M1/lab-M1-project-1.py; course/modules/M/M1/project.html lines 55-104",
        "evidence": RERUN + "python -I -W error on the twin exits 0.",
    },
    "proj-lab-twins-isolated-r12": {
        "status": "PASS",
        "location": "tests/labs/M1/lab-M1-project-1.py, lab-M1-project-2.py, lab-M1-project-3.py",
        "evidence": RERUN + "each project twin run alone under python -I -W error exits 0.",
    },
    "proj-page-smoke-r12": {
        "status": "PASS",
        "location": "course/modules/M/M1/project.html; tools/page_smoke.py --unit M1 --pages project",
        "evidence": RERUN + "'page_smoke modules/M/M1/project.html: PASS', in-browser grader '196 tests pass', exit 0.",
    },
    "proj-r13-registry": {
        "status": "PASS",
        "location": "tools/verify_refs.py --unit M1 (live); tools/verify_refs.py --offline",
        "evidence": RERUN + "live: 'live re-verification of M1: 1 of 560 entries, 0 problems', exit 0; offline: "
        "'560 entries, 0 problems'.",
    },
    "proj-cite-velleman-registry-r12": {
        "status": "PASS",
        "location": "tools/verify_refs.py --offline; tools/verify_refs.py --unit M1",
        "evidence": RERUN + "same live and offline results as proj-r13-registry (0 problems).",
    },
    "proj-r13-ruff-mypy": {
        "status": "PASS",
        "location": "course/modules/M/M1/grader/test_project.py; mypy files list in pyproject.toml",
        "evidence": RERUN + "ruff check and format check pass; mypy --no-incremental: no issues in 153 source files.",
    },
    "proj-r13-alternatives-new": {
        "status": "PASS",
        "location": "ledgers/M1/scripts/M1-d-r14/alts/ (alt_r14_a, alt_r14_b, alt_r14_c); ledgers/M1/scripts/M1-d-r13/alts/",
        "evidence": RERUN + "ledgers/M1/scripts/M1-d-r14/run_alts.sh runs 16 alternatives against the grader: all '196 "
        "passed'. The first draft of alt_r14_a had a parenthesis error that made 33 tests fail (a defect in this "
        "verifier's generator, not in the suite); it was corrected and re-run.",
    },
    "proj-grader-alternatives": {
        "status": "PASS",
        "location": "ledgers/M1/scripts/M1-d-r14/alts/; ledgers/M1/scripts/M1-d-r13/alts/; ledgers/M1/scripts/M1-d-r12/alts/",
        "evidence": RERUN + "16 of 16 alternative correct implementations (rounds 10 to 14) pass the grader.",
    },
    "proj-alt-correct-implementations-r10": {
        "status": "PASS",
        "location": "ledgers/M1/scripts/M1-d-r10/ (alt_r10_*)",
        "evidence": RERUN + "all four round-10 alternatives: 196 passed.",
    },
    "proj-alt-correct-implementations-r11": {
        "status": "PASS",
        "location": "ledgers/M1/scripts/M1-d-r11/alts/",
        "evidence": RERUN + "all three round-11 alternatives: 196 passed.",
    },
    "proj-alt-correct-implementations-r12": {
        "status": "PASS",
        "location": "ledgers/M1/scripts/M1-d-r12/alts/ (alt_r12v_a..c)",
        "evidence": RERUN + "all three: 196 passed.",
    },
    "proj-r13-alternatives-r12-rerun": {
        "status": "PASS",
        "location": "ledgers/M1/scripts/M1-d-r12/alts/alt_r12v_a_expm1_closed_form.py and siblings",
        "evidence": RERUN + "196 passed for each.",
    },
}

rows = []
for row in PREV["rows"]:
    rid = row["id"]
    if rid in NEW:
        new = NEW[rid]
        rows.append({"id": rid, "check": row["check"], "location": new["location"], "status": new["status"],
                     "evidence": new["evidence"]})
        continue
    if row["status"] != "PASS":
        raise SystemExit(f"non-PASS round-13 row {rid} has no round-14 re-verification")
    if rid.startswith("cards-L"):
        prefix = CARDS_CARRY
    elif "grader" in row["location"] or "test_project" in row["location"]:
        prefix = TESTS_CARRY
    else:
        prefix = CARRY
    rows.append({"id": rid, "check": row["check"], "location": row["location"], "status": row["status"],
                 "evidence": prefix + row["evidence"]})

rows.append({
    "id": "proj-r14-delta-scope",
    "check": "The delta eaf6d87..cef676e touches only these M1-d files",
    "location": "git diff --stat eaf6d87 cef676e -- course/modules/M/M1 tests/labs/M1 ledgers/M1",
    "status": "PASS",
    "evidence": "cards.json (1 line, M1-c142), grader/test_project.py (lines 516-528), and the mutant directory (r14d_01 "
    "to r14d_10 added). project.html, the labs, the references and the other grader files are byte-identical to the "
    "round-13 pin. The CF1 lab change (tests/labs/CF1/lab-CF1-L05-1.py) is outside this slice.",
})
rows.append({
    "id": "proj-r14-tie-7-2-arithmetic",
    "check": "The new 7.2 percent tie case is exact and rounds up",
    "location": "course/modules/M/M1/grader/test_project.py lines 519-523 (case 100000250, 0.072)",
    "status": "PASS",
    "evidence": RERUN + "Fraction(100000250)*Fraction('0.072')/12 = 1200003/2 = 600001.5, so floor(x + 1/2) = 600002, the "
    "expected value. The float 100000250*(0.072/12) = 600001.4999999999 rounds down, so the case separates exact from float "
    "arithmetic (reference 196 passed; mutant r14v_01 fails it).",
})
rows.append({
    "id": "proj-r14-new-mutants-killed",
    "check": "Three new student-error mutants written by this verifier are killed",
    "location": "ledgers/M1/mutants/r14v_01_schedule_interest_float_rate_over_twelve.py, r14v_02_level_payment_rounded_to_whole_units.py, r14v_03_annual_rate_simplified_to_denominator_1000.py",
    "status": "PASS",
    "evidence": RERUN + "r14v_01 (schedule interest from the float rate/12, rounded in float) fails 3 tests including both tie "
    "cases; r14v_02 (level payment rounded to whole 100-cent units) fails 14; r14v_03 (annual rate simplified with "
    "limit_denominator(1000)) fails 7. All three are KILLED in the mutate run.",
})
rows.append({
    "id": "proj-r14-card-c142-lab-output",
    "check": "Card M1-c142 horizons equal the lab's Part B output",
    "location": "course/modules/M/M1/cards.json M1-c142; tests/labs/M1/lab-M1-L07-1.py lines 282-289",
    "status": "PASS",
    "evidence": RERUN + "the lab (python -I -W error) prints 'part B: N = ...' rows for N = 1, 5, 10, 50, 100, 200, 400 "
    "(seven rows), the same list as the card's answer.",
})

mutants = []
for line in (ROOT / "ledgers/M1/scripts/M1-d-r14/out/mutate_r14.out").read_text(encoding="utf-8").splitlines():
    m = re.match(r"KILLED (\S+?\.py): (.*) -> (\S+) \(seed (\d+)\)$", line)
    if not m:
        continue
    name, desc, test, seed = m.group(1), m.group(2), m.group(3), m.group(4)
    mutants.append({
        "id": name.removesuffix(".py"),
        "file": f"ledgers/M1/mutants/{name}",
        "description": desc,
        "killed_by": f"{test} (seed {seed})",
        "run": "tools/mutate_graders.py --unit M1 --seeds 0-9 (round 14, checkout cef676e): KILLED",
    })

n_fail = sum(1 for r in rows if r["status"] != "PASS")
fragment = {
    "unit": "M1",
    "slice": "M1-d",
    "round": 14,
    "round_note": "round 14 (independent re-verification of slice M1-d at cef676e). Delta eaf6d87..cef676e in the slice: "
    "cards.json (M1-c142 back), grader/test_project.py lines 516-528 (the 7.2 percent tie case replaces the 23 percent "
    "case; comments and docstring rewritten), and ten mutants r14d_01 to r14d_10. project.html is unchanged. Rows whose "
    "subject is byte-identical carry round 13 evidence with the prefix; rows whose subject changed, and every command row, "
    "were re-run this round. Mutants: 119 committed files re-run plus 3 new (r14v_01 to r14v_03), 122 in all, all killed.",
    "verifier": "Claude Haiku 5.5 (independent verifier, slice M1-d, round 14; did not build M1; no shared context with builders)",
    "pin": "cef676e (detached HEAD of /tmp/verify14-M1-d)",
    "base": "eaf6d87 (round-13 pin, used for the delta)",
    "previous_ledger": "/tmp/fanout-frags/M1-d.round13.json (context only)",
    "checkout": "/tmp/verify14-M1-d",
    "scratch": "/tmp/m1-v14/d/",
    "verified_at": "2026-10-28T16:00:00+00:00",
    "verdict": "PASS" if n_fail == 0 else "FAIL",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Command output: ledgers/M1/scripts/M1-d-r14/out/mutate_r14.out (mutants); run_alts.sh (16 alternatives); "
        "mk_alts14.py and mk_r14v.py (new alternatives and mutants generated from reference.py); build_fragment_r14.py "
        "(this fragment).",
        "Carried mutant rows (m01 to r13f) are backed by the 122-file mutate run of this round, not by a separate run.",
        "Not checked: the live citation run reads one entry for M1 only (1 of 560); the other entries are checked offline. "
        "Browser rendering of the project page was not run; page_smoke covers the in-browser grader.",
        "Equivalent mutant r13v_04 (cutoff 1e-12) is not in the mutants list, as in round 13; not re-run this round.",
    ],
    "summary": f"M1-d round 14 at cef676e: {len(rows)} rows, {len(rows) - n_fail} PASS, {n_fail} FAIL. The round-13 FAIL "
    "(proj-grader-tie-comment-digits) is closed. Card M1-c142 matches the lab's seven horizons. 122 of 122 mutants killed; "
    "16 of 16 alternatives pass.",
}
OUT.write_text(json.dumps(fragment, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("rows", len(rows), "mutants", len(mutants), "verdict", fragment["verdict"])
