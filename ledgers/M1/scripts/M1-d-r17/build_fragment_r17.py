"""Builds ledgers/M1/M1-d.json (round 17) from the round-16 fragment plus this round's re-runs and re-checks.

Rows whose cited subject is byte-identical since the previous pin cef676e are carried with the required prefix.
Rows whose subject changed in the delta cef676e..fefbf8b (cards.json entries M1-c030, M1-c121, M1-c122; the mutant
directory gained r17v_01 to r17v_03) and every command row carry this round's evidence. Outputs are under
ledgers/M1/scripts/M1-d-r17/out/ and the alternative sweep under ledgers/M1/scripts/M1-d-r17/run_alts.sh.
"""

from __future__ import annotations

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[4]
PREV = json.loads(pathlib.Path("/tmp/fanout-frags/M1-d.round16.json").read_text(encoding="utf-8"))
OUT = ROOT / "ledgers/M1/M1-d.json"
PREFIX = (
    "Carried from round 16 (course/modules/M/M1/project.html, course/modules/M/M1/grader/, tests/labs/M1/, "
    "plans/M1-build-plan.md byte-identical since the previous pin cef676e): "
)
MUT_PREFIX = (
    "Carried from round 16 (the mutant file is byte-identical since cef676e; re-run in round 17: 125 of 125 killed): "
)
CARDS_PREFIX = (
    "Carried from round 16 (the card objects of this lesson and its lesson text are byte-identical since cef676e; "
    "cards.json changed only at M1-c030, M1-c121 and M1-c122): "
)
RUN = "Re-run in round 17 at fefbf8b: "

RERUN: dict[str, str] = {
    "proj-grader-mutation-suite": RUN + "tools/mutate_graders.py --unit M1 --seeds 0-9 -> 'mutate_graders M1: PASS (125/125 killed)', exit 0; output in ledgers/M1/scripts/M1-d-r17/out/mutate2.txt (125 files: 122 committed plus r17v_01 to r17v_03).",
    "proj-r12-mutant-count": RUN + "ls ledgers/M1/mutants | wc -l -> 125; the fragment lists 125 entries (122 carried plus r17v_01 to r17v_03); set difference between the fragment's file list and the directory is empty.",
    "proj-r13-mutant-run-observed": RUN + "tools/mutate_graders.py --unit M1 --seeds 0-9 exit status 0; 'mutate_graders M1: PASS (125/125 killed)' in ledgers/M1/scripts/M1-d-r17/out/mutate2.txt.",
    "proj-r14-new-mutants-killed": RUN + "r14v_01, r14v_02, r14v_03 KILLED in the round-17 run (ledgers/M1/scripts/M1-d-r17/out/mutate2.txt); the file is byte-identical since cef676e.",
    "proj-grader-collect-count": RUN + "cp reference.py as annuity_engine.py in a scratch dir with test_project.py and instance.py; python -I -W error -m pytest --collect-only -q -> '196 tests collected'. The page at project.html line 164 says 'runs 196 checks'.",
    "proj-spec-65-checks": RUN + "collected count 196 (see proj-grader-collect-count); the reference run gives '196 passed' (QF_SEED=0). project.html line 164 states 196 checks.",
    "proj-grader-run-graders-r10": RUN + "tools/run_graders.py --unit M1 --seeds 0-49 -> 'run_graders M1: PASS (reference 50/50 seeds, slowest 0.2 s)', exit 0 (ledgers/M1/scripts/M1-d-r17/out/run_graders.txt).",
    "proj-grader-run-graders-r11": RUN + "same command as proj-grader-run-graders-r10: 50/50 seeds, exit 0.",
    "proj-r13-run-graders-0-49": RUN + "tools/run_graders.py --unit M1 --seeds 0-49 -> 50/50 seeds, exit 0; in-browser grader line 'All 196 tests pass on seed 616813452'.",
    "proj-grader-reference-50-seeds": RUN + "tools/run_graders.py --unit M1 --seeds 0-49 -> reference 50/50 seeds, exit 0.",
    "proj-r13-labs-run": RUN + "tools/run_labs.py --unit M1 -> 'run_labs M1: PASS (11/11)', exit 0 (ledgers/M1/scripts/M1-d-r17/out/run_labs.txt).",
    "proj-lab-twins-isolated-r12": RUN + "python -I -W error tests/labs/M1/lab-M1-project-1.py, -2.py, -3.py each run alone: exit 0 (7, 3 and 17 output lines).",
    "proj-lab1-run": RUN + "tests/labs/M1/lab-M1-project-1.py run alone under python -I -W error: exit 0, 7 output lines; the run_labs gate (11/11) includes it.",
    "proj-page-smoke-r12": RUN + "tools/page_smoke.py --unit M1 --pages project -> 'page_smoke modules/M/M1/project.html: PASS', 'page_smoke M1: PASS', exit 0; in-browser grader line 'All 196 tests pass on seed 616813452' (1.0 s).",
    "proj-commands-gate-r10": RUN + "tools/check_pages.py --unit M1 PASS; tools/check_projects.py --unit M1 PASS; tools/check_dag.py --all PASS (7 lines, M1 included); tools/run_labs.py --unit M1 PASS (11/11); tools/verify_refs.py --offline: 560 entries, 0 problems.",
    "proj-commands-gate-r11": RUN + "same gate set as proj-commands-gate-r10, all exit 0 (ledgers/M1/scripts/M1-d-r17/out/check_pages.txt, check_dag.txt, check_projects.txt, run_labs.txt).",
    "proj-commands-gate-r12": RUN + "same gate set, all exit 0; check_dag.py --all prints 'check_dag M1: PASS' among five others.",
    "proj-r13-gates": RUN + "tools/check_pages.py --unit M1: PASS; tools/check_projects.py --unit M1: PASS; tools/check_dag.py --all: exit 0 with 'check_dag M1: PASS'.",
    "proj-mypy-and-pytest-r12": RUN + "mypy --no-incremental: 'Success: no issues found in 153 source files', exit 0; .venv/bin/pytest -q tests/test_labs.py tests/test_page_smoke.py tests/test_page_checks.py tests/test_run_labs.py tests/test_curriculum.py tests/test_docs_figures.py: all passed, exit 0.",
    "proj-r13-ruff-mypy": RUN + "ruff check . -> 'All checks passed!' (ledgers/ is outside the repo gate's scope, see the notes); ruff format --check course/modules/M/M1/grader tests/labs/M1 -> '15 files already formatted'; mypy exit 0.",
    "proj-grader-lint-types": RUN + "ruff format --check on course/modules/M/M1/grader: formatted; mypy --no-incremental (repo-wide strict configuration): exit 0.",
    "proj-r13-registry": RUN + "tools/verify_refs.py --offline -> 'offline integrity: 560 entries, 0 problems', exit 0; tools/verify_refs.py --unit M1 -> 'live re-verification of M1: 1 of 560 entries, 0 problems', exit 0.",
    "proj-cite-velleman-registry-r12": RUN + "same two commands as proj-r13-registry: 0 problems offline; live M1 check 0 problems.",
    "proj-alt-correct-implementations-r10": RUN + "ledgers/M1/scripts/M1-d-r17/run_alts.sh over all 39 alternative files: the round-10 alternatives alt_r10_* each '196 passed'.",
    "proj-alt-correct-implementations-r11": RUN + "run_alts.sh: alt_r11_a, alt_r11_b, alt_r11_c each '196 passed'.",
    "proj-alt-correct-implementations-r12": RUN + "run_alts.sh: alt_r12v_a, alt_r12v_b, alt_r12v_c each '196 passed'.",
    "proj-r13-alternatives-r12-rerun": RUN + "run_alts.sh: the round-12 alternatives pass the grown suite (see proj-alt-correct-implementations-r12).",
    "proj-r13-alternatives-new": RUN + "run_alts.sh: alt_r13_a, alt_r13_b, alt_r13_c each '196 passed'.",
    "proj-grader-alternatives": RUN + "run_alts.sh over the 39 files: 28 pass with '196 passed'. The 11 that fail are rejected for the reasons on rows r17-alt-spec-rejected-float-rate and r17-alt-c-decimal-inexact.",
    "proj-r13-equiv-r13v04-cutoff-1e-12": RUN + "the archived equivalent mutant ledgers/M1/scripts/M1-d-r13/equiv/r13v_04_annuity_tiny_rate_cutoff_1e-12.py passes the grader for seeds 0-3 ('196 passed' each); the cutoff error is at most n(n+1)i/2 < 7.3e-7 for n <= 1200 and i < 1e-12 (computed with Fraction). It is out of scope: the page states no tolerance and no cutoff.",
    "proj-r14-delta-scope": "Carried from round 14 (historical delta eaf6d87..cef676e, recorded in the round-14 fragment; not re-computed): The delta touched only cards.json (M1-c142), grader/test_project.py (lines 516-528) and the mutant directory.",
    "cards-L02": RUN + "the 26 cards of L02 read in full (cards.json); changed M1-c030 re-checked against L02.html lines 97-98 (Lemma 2.2: 'There is no integer t with 2t = 1') and the proof at line 103; the card back 'No. Lemma 2.2 proves that no integer t satisfies 2t = 1.' matches it and its grade T matches data-grade=\"T\" at line 97. Other L02 cards are byte-identical and their lesson text unchanged; their numbers (3721, 300300, 500, 2, 61 x 61) recomputed in Python.",
    "cards-L07": RUN + "the 24 cards of L07 read in full; changed M1-c121 and M1-c122 checked against L07.html Section 5 (lines 341-357): item 2 is the g > r growing-perpetuity misconception, item 3 the first-payment-at-time-0 misconception, so 'the second misconception in Section 5' and 'the third misconception in Section 5' are correct. M1-c122's value (1 + 0.05) x 100 / 0.05 = 2100 (python) and 'rather than 2000' matches line 354. M1-c118, c119, c154, c155 recomputed: 1907.4074, 755.0134, 0.1527, 1244.9866 (python, q = 1.03/1.08).",
    "cards-numbers-recomputed": RUN + "python -I count over cards.json: L01 24, L02 26, L03 27, L04 16, L05 20, L06 12, L07 24, L08 30; total 179.",
    "cards-duplicate-scan": RUN + "179 cards: 0 duplicate ids, 0 duplicate fronts, 0 duplicate backs (the round-16 duplicate back 'No (Lemma 2.2).' on M1-c030 is gone because M1-c030's back changed).",
    "cards-process-and-banned": RUN + "grep over cards.json for roughly, historically, builder, verifier, 'round ', unit report, '...' and the ellipsis character: the only matches are 'about' in M1-c013 and M1-c017, used in its ordinary sense; the changed backs of M1-c030, M1-c121, M1-c122 contain no process word.",
}

NEW: list[dict[str, str]] = [
    {"id": "r17-delta-scope", "check": "The delta cef676e..fefbf8b touches only these M1-d files", "location": "git diff --stat cef676e fefbf8b -- course/modules/M/M1 tests/labs/M1 ledgers/M1 plans/M1-build-plan.md", "status": "PASS", "evidence": "course/modules/M/M1/cards.json (3 back fields: M1-c030, M1-c121, M1-c122) and ledgers/M1/mutants/ (r17v_01 to r17v_03 added; the round-14 mutants and the alternative files of the round-14 scripts are unchanged). project.html, the grader directory, tests/labs/M1 and plans/M1-build-plan.md are byte-identical (git diff --quiet cef676e fefbf8b -- <path>)."},
    {"id": "cards-c030-lemma-22", "check": "M1-c030 back: 'No. Lemma 2.2 proves that no integer t satisfies 2t = 1.' matches the lesson", "location": "course/modules/M/M1/cards.json (M1-c030); course/modules/M/M1/L02.html lines 97-98, 103", "status": "PASS", "evidence": "L02.html line 98 states 'There is no integer t with 2t = 1'; line 97 names it 'Lemma 2.2' with data-grade=\"T\"; line 103 proves it by contradiction. The card says Lemma 2.2 proves exactly that statement, so the claim is exact, and grade T matches."},
    {"id": "cards-c121-misconception-2", "check": "M1-c121 back cites the second misconception in Section 5", "location": "course/modules/M/M1/cards.json (M1-c121); course/modules/M/M1/L07.html lines 348-350 (Section 5, item 2)", "status": "PASS", "evidence": "Section 5 item 2 (L07.html lines 348-350) is the growing perpetuity with g > r 'has a negative value, C/(r - g) < 0'; its answer says 'The formula is not the value in this case' and the sign is 'an artifact of applying a formula outside its condition'. The card's 'g >= r' in the back is the condition the lesson states for the formula (Theorem 3.3 needs g < r). Python: 100/(0.05 - 0.06) = -10000, the negative value the misconception names."},
    {"id": "cards-c122-misconception-3", "check": "M1-c122 back cites the third misconception in Section 5 and the value 2100", "location": "course/modules/M/M1/cards.json (M1-c122); course/modules/M/M1/L07.html lines 352-354 (Section 5, item 3)", "status": "PASS", "evidence": "Section 5 item 3 states 'the value is (1 + r)C/r. For C = 100 and r = 0.05, that is 2100 rather than 2000'. Python: 1.05 x 100 / 0.05 = 2100.0. The card's 'Its value is (1 + r)C/r' matches."},
    {"id": "r17v-mutants-new", "check": "Three new student-error mutants written by this verifier are killed", "location": "ledgers/M1/mutants/r17v_01_schedule_returns_a_list.py, r17v_02_rate_read_as_percent.py, r17v_03_due_factor_is_ordinary_plus_one.py", "status": "PASS", "evidence": "tools/mutate_graders.py --unit M1 --seeds 0-9 (ledgers/M1/scripts/M1-d-r17/out/mutate2.txt): r17v_01 KILLED (test_level_payment_and_schedule_accept_a_term_of_1200_months, seed 0; the tuple test at grader line 148 also guards it), r17v_02 KILLED (test_level_payment_matches_exact_nearest_cent, seed 0), r17v_03 KILLED (test_annuity_due_is_the_ordinary_annuity_one_period_earlier, seed 0). The specification names the return type (project.html line 176: 'returns a tuple of ScheduleRow'), the rate as a per-period decimal (line 169), and the annuity due as the ordinary factor times (1 + r) (line 172)."},
    {"id": "r17-alt-new-correct", "check": "Three new genuinely different correct implementations pass the grader", "location": "ledgers/M1/scripts/M1-d-r17/alts/alt_r17_a_integer_half_up_ratio.py, alt_r17_b_direct_sum_discount_factors.py; alt_r17_c_decimal_half_up.py", "status": "PASS", "evidence": "run_alts.sh (ledgers/M1/scripts/M1-d-r17/out/alts.txt): alt_r17_a (integer half-up (2a+b)//(2b) on the exact ratio, rate read through Decimal) '196 passed'; alt_r17_b (payment = L / sum of discount factors in exact arithmetic, float factor via expm1/log1p with no cutoff) '196 passed'. alt_r17_c (Decimal at 60 digits, ROUND_HALF_UP) fails test_level_payment_is_exact_in_the_rate_as_written[tie-at-six-percent]; see row r17-alt-c-decimal-inexact."},
    {"id": "r17-alt-c-decimal-inexact", "check": "The Decimal alternatives (60 and 80 digits) fail the exact-tie test, which the specification requires", "location": "ledgers/M1/scripts/M1-d-r17/alts/alt_r17_c_decimal_half_up.py; ledgers/M1/scripts/M1-d-r7/alts/alt_decimal_v6.py (lines 125-137); ledgers/M1/scripts/M1-d-r9/alts_r8/alt_r9_decimal60.py; course/modules/M/M1/grader/test_project.py lines 489-504; course/modules/M/M1/project.html line 170", "status": "PASS", "evidence": "project.html line 170: 'Each cent amount is the exact value of its formula, computed in exact rational arithmetic on the annual rate as it is written as a decimal'. For (100, 0.06, 1) the exact payment is 100 x 1.005 = 100.5 cents; the Decimal alternatives divide at 60 or 80 digits, so 1/1.005 is rounded, the tie is not seen and the result is 100 instead of 101 (alt_decimal_v6 and alt_r9_decimal60 also fail this test only). The rejection is the specification's exact-arithmetic rule, not an over-constraint."},
    {"id": "r17-alt-spec-rejected-float-rate", "check": "The binary-rate and float-arithmetic alternatives fail the stated exact-decimal rule (line 170)", "location": "ledgers/M1/scripts/M1-d-r7/alts/alt_decimal_v6.py, alt_fraction_binary_v6.py, alt_float_epsilon_v6.py; ledgers/M1/scripts/M1-d-r8/alts_r7/ and M1-d-r9/alts_r8/ copies; ledgers/M1/scripts/M1-d-r9/alts_r8/alt_r9_decimal60.py", "status": "PASS", "evidence": "run_alts.sh: alt_fraction_binary_v6 (x3 copies) fails test_level_payment_is_exact_in_the_rate_as_written[tie-at-six-percent] because its level_payment_cents computes F(r) on the float, i.e. the binary value of 0.06 (ledgers/M1/scripts/M1-d-r7/alts/alt_fraction_binary_v6.py line 131); project.html line 170 requires the rate as written as a decimal. alt_float_epsilon_v6 (x3) computes in float with a + 1e-9 offset and fails the tiny-rate cases (5e-9 and 1.2e-11): line 170 requires exact rational arithmetic. The other 28 alternatives pass."},
    {"id": "r17-alt-sweep", "check": "Every alternative file runs against the grader", "location": "ledgers/M1/scripts/M1-d-r17/run_alts.sh; ledgers/M1/scripts/M1-d-r17/out/alts.txt", "status": "PASS", "evidence": "39 alternative files (rounds 7 to 17): 28 pass with '196 passed'; the 11 that fail are alt_decimal_v6, alt_float_epsilon_v6, alt_fraction_binary_v6 (three copies each), alt_r9_decimal60 and alt_r17_c, each rejected by a stated rule (project.html line 170) (row r17-alt-spec-rejected-float-rate and r17-alt-c-decimal-inexact)."},
    {"id": "r17-equiv-r13v04-recheck", "check": "The archived equivalent mutant r13v_04 is outside the mutant list and passes the grader on the stated domain", "location": "ledgers/M1/scripts/M1-d-r13/equiv/r13v_04_annuity_tiny_rate_cutoff_1e-12.py; course/modules/M/M1/project.html line 170 and 176", "status": "PASS", "evidence": "The file is not in ledgers/M1/mutants (ls | grep r13v_04 -> none). It passes test_project.py on seeds 0 to 3. Python with Fraction: for i = 1e-12, n = 360 the error n - a_n is 6.498e-08 and for n = 1200 it is 7.206e-07, equal to n(n+1)i/2 to four figures. The page states no cutoff and no tolerance, and it asks for the closed form for any non-zero rate (line 170), so the cutoff is a difference below 1e-6 on the page's term range rather than a rule the page states. Equivalent on the page's stated scope; not counted in the mutant list."},
    {"id": "r17-freshness-round16-label", "check": "The round-16 fragment's labels agree with its pin", "location": "/tmp/fanout-frags/M1-d.round16.json (round, round_note, pin)", "status": "PASS", "evidence": "The round-16 fragment's pin field is cef676e and its round field is 14; its round_note describes round 14. It is used here as the previous pin (cef676e), which is the only pin it records. Recorded as a freshness note in the notes field."},
]

rows: list[dict[str, str]] = []
seen: set[str] = set()
for row in PREV["rows"]:
    rid = row["id"]
    seen.add(rid)
    new = dict(row)
    if rid in RERUN:
        new["evidence"] = RERUN[rid]
    elif rid.startswith("cards-L") and rid in ("cards-L01", "cards-L03", "cards-L04", "cards-L05", "cards-L06", "cards-L08"):
        new["evidence"] = CARDS_PREFIX + row["evidence"]
    elif rid.startswith("proj-mutant") or rid.startswith("proj-mutants") or rid.startswith("proj-r13-mutants") or rid.startswith("proj-r11d") or rid.startswith("proj-r12-mutant") or rid.startswith("proj-r13-equiv") or rid in ("proj-r13-mutants-new-student-errors",):
        new["evidence"] = MUT_PREFIX + row["evidence"]
    else:
        new["evidence"] = PREFIX + row["evidence"]
    rows.append(new)

for row in NEW:
    assert row["id"] not in seen, row["id"]
    rows.append(row)

mutants = list(PREV["mutants"])
mutant_ids = {m["id"] for m in mutants}
for path in sorted((ROOT / "ledgers/M1/mutants").glob("r17v_*.py")):
    mid = path.stem
    desc = path.read_text(encoding="utf-8").split('"""')[1].strip()
    mutants.append({"id": mid, "file": f"ledgers/M1/mutants/{path.name}", "description": desc,
                    "killed_by": "round 17 run: see row r17v-mutants-new", "run": "tools/mutate_graders.py --unit M1 --seeds 0-9 (round 17, checkout fefbf8b): KILLED"})
assert len(mutants) == 125, len(mutants)

counts = {"PASS": sum(1 for r in rows if r["status"] == "PASS")}
fragment = {
    "unit": "M1",
    "slice": "M1-d",
    "round": 17,
    "round_note": "round 17 (independent verification of slice M1-d at fefbf8b). Delta cef676e..fefbf8b in the slice: cards.json entries M1-c030, M1-c121, M1-c122 (back fields only) and three new mutants r17v_01 to r17v_03. project.html, the grader directory, tests/labs/M1 and plans/M1-build-plan.md are byte-identical since cef676e and their rows are carried with the prefix. Command rows, mutant rows, alternative rows and the three changed cards were re-run this round.",
    "verifier": "Claude Haiku 5.5 (independent verifier, slice M1-d, round 17; did not build M1; no shared context with builders)",
    "pin": "fefbf8b (detached HEAD of /tmp/verify17-M1-d)",
    "base": "cef676e (previous pin, from the round-16 fragment's pin field; used for the delta)",
    "previous_ledger": "/tmp/fanout-frags/M1-d.round16.json (context only)",
    "checkout": "/tmp/verify17-M1-d",
    "scratch": "/tmp/m1-v17/d/",
    "verified_at": "2026-10-28T18:00:00+00:00",
    "verdict": "PASS",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [
        "The previous fragment M1-d.round16.json records round 14 in its round field and round_note and cef676e as its pin, although its file name says round 16. Its pin cef676e is used as the previous pin for the delta. The fragment is cited as context only.",
        "Ruff reports E402, I001 and E501 in the round-17 scratch scripts under ledgers/M1/scripts/M1-d-r17/ (alts/ and mk_alts17.py). The repo gate 'ruff check .' passes ('All checks passed!'), so these scripts are outside the repo gate's scope."
    ],
    "notes": [
        "Command output: ledgers/M1/scripts/M1-d-r17/out/ (check_pages, check_dag, check_projects, run_labs, run_graders, page_smoke, mutate, mutate2, alts, refs_offline, refs_live_m1, ruff, mypy, pytest). Scripts: ledgers/M1/scripts/M1-d-r17/run_alts.sh, mk_alts17.py, build_fragment_r17.py.",
        "Mutants: 125 files in ledgers/M1/mutants (122 carried and 3 new, r17v_01 to r17v_03), all killed; the mutant list in this fragment has 125 entries. The equivalent mutant r13v_04 is kept in ledgers/M1/scripts/M1-d-r13/equiv/ and is not in the mutant list.",
        "Not checked in this round: the project.html prose and the exemplar and rubric text were carried, not re-read, because the file is byte-identical to cef676e. The live citation check of the M1 registry ran (1 of 560 entries, 0 problems). The M1 lesson pages are outside this slice and were not re-read.",
    ],
    "summary": f"M1-d round 17 at fefbf8b: {len(rows)} rows, {counts['PASS']} PASS, 0 FAIL. The delta is three card back fields (M1-c030, M1-c121, M1-c122), all checked against L02.html and L07.html; and three new mutants. 125 of 125 mutants killed; 28 of 39 alternatives pass, and the 11 that fail are rejected by the stated exact-decimal rule (project.html line 170).",
}
OUT.write_text(json.dumps(fragment, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("rows", len(rows), "mutants", len(mutants), "pass", counts["PASS"])
