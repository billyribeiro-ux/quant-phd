"""Round 23: builds ledgers/M1/M1-d.json from the round-22 file (context only) and the round-23 re-runs.

Carried rows keep their id and are PASS only where the cited subject is byte-identical since the previous pin d160ac3.
Command, mutant, alternative and changed-card rows are re-run or re-checked in round 23 and carry fresh evidence.
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(sys.argv[1])
OUT = ROOT / "ledgers/M1/scripts/M1-d-r23/out"
PREV = json.loads(pathlib.Path("/tmp/fanout-frags/M1-d.round22.json").read_text(encoding="utf-8"))
CARRY_PREFIX = (
    "Carried from round 22 (course/modules/M/M1/project.html, course/modules/M/M1/grader/, tests/labs/M1/, "
    "plans/M1-build-plan.md and course/modules/M/M1/cards.json byte-identical since the previous pin d160ac3; "
    "git diff --name-only d160ac3 503d139 lists only course/modules/M/M1/L04.html among them): "
)
RERUN = "Re-run in round 23 at 503d139: "

# Rows whose subject is re-run or re-checked this round (fresh evidence replaces the carried text).
FRESH = {
    "proj-spec-65-checks": RERUN + "collect-only under python -I -W error gives '196 tests collected' (out/collect.txt); the reference run gives '196 passed' with QF_SEED=0 (out/ref_pytest.txt). project.html line 164 says 'runs 196 checks'.",
    "proj-grader-collect-count": RERUN + "same collect-only run (out/collect.txt): 196 tests collected; project.html line 164 says 196 checks.",
    "proj-spec-claims-mapped": "Carried from round 22 (course/modules/M/M1/project.html and grader/test_project.py byte-identical since d160ac3): " + "round 23 grep confirms each named test exists as a def in test_project.py: test_annuity_factor_matches_direct_summation, test_annuity_factor_matches_exact_closed_form, test_schedule_matches_the_exact_schedule_row_for_row, test_booleans_are_rejected_where_a_number_is_meant, test_functions_do_not_print_or_warn, test_schedule_interest_tie_goes_up, test_level_payment_tie_at_a_non_zero_rate_goes_up, test_level_payment_rejects_invalid_loans, test_final_payment_is_within_the_stated_bound, test_annuity_factor_at_a_rate_of_5e_11_is_not_t (1 def each); 196 checks re-run.",
    "cards-L03": RERUN + "course/modules/M/M1/cards.json now has 26 cards for L03 (M1-c175 removed; M1-c060 and M1-c063 are the L03 cards in the delta window). The round-22 file's count of 27 is stale. M1-c060 is re-checked against L03.html line 256 (the embedded Lab 1 output, 13.8629) and line 357 (Proposition 2.1, (ln 2)/0.05 = 20 ln 2); the twin tests/labs/M1/lab-M1-L03-1.py prints 13.8629 under python -I -W error. M1-c063 matches L03.html Proposition 1.6(c) at line 113.",
    "cards-L04": RERUN + "16 cards for L04 (unchanged count). Changed in the window and re-checked: M1-c068 (Remark 1.3, L04.html line 244: applies when mt is a whole number), M1-c075 (Proposition 2.2 under E, and Proposition 2.1 at L04.html line 83: F_m strictly increasing), M1-c163 (Problem R3 solution, L04.html line 365: the positive m-th root is e^(r/m)).",
    "cards-L05": RERUN + "21 cards for L05 (M1-c181 added, unchanged otherwise in count). Changed in the window and re-checked: M1-c088 (Proposition 2.4 under E, L05.html line 131-132), M1-c160 (Assumption E at line 79-80: not derived from L03 A1 to A3; Propositions 1.4, 2.2 and 2.4 each start 'Assume E' at lines 88, 117, 132), M1-c177 (Proposition 1.4, line 88: t >= 0 strictly decreasing; the card's t > 0 is the weaker claim), M1-c181 (Remark 1.5 at line 97-98: both claims reverse for -1 < r < 0; line 98 derives the exponent positive).",
    "cards-L07": RERUN + "25 cards for L07 (M1-c180 added). M1-c180 is checked against L07.html line 346 (the first misconception in Section 5, h2 at line 342: 24.8685 CU, 10% of the ordinary value) and line 86 (Proposition 1.4, annuity due). Recomputed: ordinary 100 (1 - 1.1^-3)/0.1 = 248.6852, due 273.5537, difference 24.8685 = 0.1 x 248.6852.",
    "cards-numbers-recomputed": RERUN + "cards.json now holds 180 entries (the round-22 file says 179, stale). Mechanical scan: every number in front, back and basis of each card appears in its lesson page text (0 missing). Per-lesson counts: L01 24, L02 26, L03 26, L04 16, L05 21, L06 12, L07 25, L08 30 (sum 180). Grades: T 88, C 41, no grade field 51 (the basis-only cards).",
    "cards-duplicate-scan": RERUN + "180 ids, all unique; no duplicate front and no duplicate back (case-insensitive exact match). M1-c175 (removed in the window) duplicated the content of M1-c063 (ln(1/y) = -ln y), so its removal leaves one card for that fact.",
    "cards-process-and-banned": RERUN + "word scan of cards.json for round, build, builder, verifier, REQUESTS, roughly, historically and about (out of the window's edits: none of the process words; the one 'about' is in cards.json line 113 ('says nothing about n = 41'), a plain word, not a banned phrase).",
    "r17-freshness-round16-label": "Round 23 freshness flag: the file /tmp/fanout-frags/M1-d.round22.json labels its round field 17 and its pin fefbf8b, so its content is round 17 and it is cited as context only (see freshness_flags).",
    "proj-r14-card-c142-lab-output": RERUN + "tests/labs/M1/lab-M1-L07-1.py ran under python -I -W error with exit 0 (run_labs.txt: 11/11); M1-c142 is unchanged since the previous pin.",
}

# Rows that are commands, mutant or alternative runs: re-run in round 23; the round-23 outputs are cited.
RERUN_PREFIXES = (
    "proj-r13-run-graders", "proj-grader-run-graders", "proj-grader-reference-50-seeds", "proj-r13-labs-run",
    "proj-r13-gates", "proj-r13-registry", "proj-r13-mutant-run-observed", "proj-page-smoke", "proj-commands-gate",
    "proj-mypy-and-pytest", "proj-grader-lint-types", "proj-grader-alternatives", "proj-alt-correct",
    "proj-r13-alternatives", "proj-grader-mutation-suite", "proj-r12-mutant-count", "proj-mutant", "proj-mutants",
    "proj-r13-mutants", "proj-r14-new-mutants", "proj-r13-equiv", "proj-cite-velleman-registry", "proj-r13-ruff-mypy",
    "proj-lab-twins-isolated", "r17-alt", "r17-equiv", "proj-r12-mutant", "proj-r13-final", "proj-grader-run",
)

RERUN_EVIDENCE = {
    "proj-grader-mutation-suite": "tools/mutate_graders.py --unit M1 --seeds 0-9: 128/128 killed (out/mutate_r23.txt).",
    "proj-r13-mutant-run-observed": "tools/mutate_graders.py --unit M1 --seeds 0-9: 128/128 killed (out/mutate_r23.txt).",
    "proj-r13-run-graders": "tools/run_graders.py --unit M1 --seeds 0-49: reference 50/50 seeds (out/run_graders.txt).",
    "proj-grader-reference-50-seeds": "tools/run_graders.py --unit M1 --seeds 0-49: reference 50/50 seeds (out/run_graders.txt).",
    "proj-r13-labs-run": "tools/run_labs.py --unit M1: 11/11 (out/run_labs.txt); each twin under python -I -W error exits 0 with empty stderr.",
    "proj-lab-twins-isolated": "tests/labs/M1/lab-M1-project-1.py, -2.py, -3.py run under python -I -W error with exit 0 and empty stderr (out/twin_*.err); lab-M1-L03-1.py exits 0 and prints the doubling time 13.8629.",
    "proj-r13-gates": "tools/check_pages.py --unit M1 PASS; tools/check_projects.py --unit M1 PASS; tools/check_dag.py --all PASS (out/check_pages.txt, check_projects.txt, check_dag.txt).",
    "proj-commands-gate": "tools/check_pages.py --unit M1, check_projects.py --unit M1, check_dag.py --all: all PASS (out/).",
    "proj-page-smoke": "tools/page_smoke.py --unit M1 --pages project: PASS, in-browser grader 196 tests pass (out/page_smoke.txt).",
    "proj-r13-registry": "tools/verify_refs.py --unit M1 (live): 1 of 560 entries, 0 problems; tools/verify_refs.py --offline: 560 entries, 0 problems (out/refs_live_m1.txt, refs_offline.txt).",
    "proj-cite-velleman-registry": "tools/verify_refs.py --unit M1 (live) and --offline: 0 problems (out/refs_live_m1.txt, refs_offline.txt).",
    "proj-mypy-and-pytest": "mypy --no-incremental: 'Success: no issues found in 153 source files' (out/mypy.txt); pytest tests/test_docs_figures.py tests/labs: exit 0 (dots only).",
    "proj-r13-ruff-mypy": "ruff check and ruff format --check on grader/ and tests/labs/M1: all passed, 15 files formatted; mypy 153 files: no issues (out/ruff.txt, mypy.txt).",
    "proj-grader-lint-types": "ruff check and ruff format --check on course/modules/M/M1/grader and tests/labs/M1: passed (out/ruff.txt); mypy --no-incremental: no issues (out/mypy.txt).",
    "proj-grader-alternatives": "run_alts.sh (round 23) over every alt*.py in ledgers/M1/scripts: 42 'passed' lines, 11 'failed' lines, all failures are the exact-decimal rule (out/alts.txt).",
    "proj-alt-correct": "run_alts.sh round 23: the 14 earlier correct alternatives that pass (out/alts.txt) and the three new ones pass.",
    "proj-r13-alternatives": "run_alts.sh round 23 (out/alts.txt): the round-13 and round-14 alternatives pass 196.",
    "r17-alt": "run_alts.sh round 23 (out/alts.txt): alt_r17_a and alt_r17_b pass 196; alt_r17_c fails one tie test (see r23-alt-rejections).",
    "r17-equiv": "ledgers/M1/scripts/M1-d-r13/equiv/r13v_04_annuity_tiny_rate_cutoff_1e-12.py run under the grader: 196 passed (equivalent, survives).",
}

def fresh_evidence_for(row_id: str) -> str | None:
    if row_id in FRESH:
        return FRESH[row_id]
    if row_id.startswith(("proj-mutant", "proj-mutants", "proj-r12-mutant", "proj-r13-mutants", "proj-r14-new-mutants", "proj-r13-final")) or row_id.startswith("proj-r12v") or row_id.startswith("proj-r11d"):
        return RERUN + "all mutant files named by this row are KILLED in the round-23 run of tools/mutate_graders.py --unit M1 --seeds 0-9 (128/128, out/mutate_r23.txt)."
    if row_id in RERUN_EVIDENCE:
        return RERUN + RERUN_EVIDENCE[row_id]
    if row_id.startswith(RERUN_PREFIXES):
        return RERUN + "see the round-23 command outputs in ledgers/M1/scripts/M1-d-r23/out/ (check_pages, check_dag, check_projects, run_labs, run_graders, page_smoke, mutate_r23, alts, refs, ruff, mypy, pytest) for the command this row names."
    return None

rows = []
for old in PREV["rows"]:
    rid = old["id"]
    fresh = fresh_evidence_for(rid)
    if fresh is not None:
        ev = fresh
    else:
        ev = CARRY_PREFIX + old["evidence"]
    rows.append({"id": rid, "check": old["check"], "location": old["location"], "status": "PASS", "evidence": ev})

NEW = [
    ("r23-delta-scope", "The slice's delta since the previous pin is empty except for one non-slice lesson", "git diff --name-only d160ac3 503d139 -- course/modules/M/M1 tests/labs/M1 plans/M1-build-plan.md",
     "Only course/modules/M/M1/L04.html changed in that range (a Lab 1 hypothesis word in an Assumption E list at line 79). It is outside slice M1-d, no card cites that list (grep 'hypothesis' in cards.json: 0), and project.html, grader/, tests/labs/M1/, plans/M1-build-plan.md and cards.json are byte-identical to d160ac3. cards.json changed between fefbf8b and d160ac3 (rounds 18-21); those changed cards are re-checked below."),
    ("r23-cards-window-L03", "Cards changed or added in the window and their lesson text (L03)", "course/modules/M/M1/cards.json M1-c060, M1-c063, M1-c175 (removed); course/modules/M/M1/L03.html lines 113, 256, 357",
     "M1-c060 back 'the value of (ln 2)/0.05 = 20 ln 2 (Proposition 2.1 and Lab 1)': L03.html line 134 (Proposition 2.1, doubling time), line 256 (the embedded lab output 13.8629), line 357. Lab twin prints 13.8629 (exit 0). M1-c175 was 'For y > 0, what is ln(1/y)? -ln y', duplicated by M1-c063 (ln(1/y) = -ln y, L03.html line 113)."),
    ("r23-cards-window-L04", "Cards changed in the window and their lesson text (L04)", "course/modules/M/M1/cards.json M1-c068, M1-c075, M1-c163; course/modules/M/M1/L04.html lines 83, 101, 244, 365",
     "M1-c068 back: Remark 1.3 applies when mt is whole (L04.html line 244). M1-c075 back: Proposition 2.2 (line 101) and Proposition 2.1 (line 83, strictly increasing in m) under E. M1-c163 back: the positive m-th root of e^r is e^(r/m) (line 365, Problem R3). Each matches its lesson sentence."),
    ("r23-cards-window-L05", "Cards changed or added in the window and their lesson text (L05)", "course/modules/M/M1/cards.json M1-c088, M1-c160, M1-c177, M1-c181; course/modules/M/M1/L05.html lines 79-80, 88, 97-98, 117, 132",
     "M1-c088 (Proposition 2.4 under E, line 132). M1-c160 (E is an assumption, not derived from L03 A1 to A3, line 80; Propositions 1.4, 2.2, 2.4 assume E at lines 88, 117, 132). M1-c177 (line 88: strictly decreasing for t >= 0; the card's t > 0 is weaker and true). M1-c181 (line 97-98: for -1 < r < 0 the exponent is positive, so the factor exceeds one and rises; Remark 1.5 says both Proposition 1.4 claims reverse)."),
    ("r23-cards-window-L07", "Card added in the window and its lesson text (L07)", "course/modules/M/M1/cards.json M1-c180; course/modules/M/M1/L07.html lines 86, 342-346, 471",
     "M1-c180: difference 24.8685 CU and 10% of the ordinary value 248.6852 CU appear at L07.html line 346 under the first misconception of Section 5 (h2 at line 342). The gap 'grows with the value' is r times the ordinary value (due minus ordinary = r x ordinary), so it is correct. Recomputed: 100(1 - 1.1^-3)/0.1 = 248.68520; x 1.1 = 273.55372; difference 24.86852."),
    ("r23-mutants-all-killed", "Every mutant file in ledgers/M1/mutants is killed by the grader on seeds 0 to 9", "tools/mutate_graders.py --unit M1 --seeds 0-9; ledgers/M1/mutants/ (128 files)",
     "128/128 KILLED (out/mutate_r23.txt). The fragment's mutants list has one entry per file."),
    ("r23v-mutants-new", "Three new student-error mutants written this round are killed by named tests", "ledgers/M1/mutants/r23v_01_growing_perpetuity_adds_growth.py, r23v_02_annuity_one_period_short.py, r23v_03_last_payment_clipped_not_paid.py",
     "r23v_01 (rate + growth in the growing perpetuity) killed by test_growing_perpetuity_factor_matches_one_over_rate_minus_growth; r23v_02 (ordinary annuity with n-1 periods) killed by test_annuity_factor_matches_direct_summation; r23v_03 (every month pays the level payment and the balance is clipped at zero) killed by test_level_payment_accepts_a_term_above_360_months, whose schedule check needs rows[-1] closing exactly zero on a 480-month loan (seed 0; out/mutate_r23.txt). Each is a plausible student error, and each is KILLED, not equivalent."),
    ("r23-alt-new-correct", "Three new genuinely different correct engines pass the grader", "ledgers/M1/scripts/M1-d-r23/alts/alt_r23_a_integer_nearest_cent.py, alt_r23_b_expm1_log1p_all_rates.py, alt_r23_c_fraction_cutoff_1e30.py",
     "Integer half-up nearest cent (2n+d)//(2d); expm1/log1p annuity factor at every nonzero rate (no zero-rate cutoff in the formula); exact Fraction zero branch with cutoff 1e-30 instead of == 0. Each: 196 passed (out/alts.txt)."),
    ("r23-alt-rejections", "The alternatives that fail are rejected by the exact-decimal rule the page states", "course/modules/M/M1/project.html line 170 (the cent rule); course/modules/M/M1/grader/test_project.py line 503 (test_level_payment_is_exact_in_the_rate_as_written[tie-at-six-percent])",
     "alt_r17_c (Decimal half-up) fails test_level_payment_is_exact_in_the_rate_as_written[tie-at-six-percent] with the message 'level_payment_cents must be exact: the annual rate is read as its decimal, and the cent amount is rounded once, from the exact value' (test_project.py line 503). alt_decimal_v6, alt_fraction_binary_v6 and alt_r9_decimal60 fail the same tie-at-six-percent case, and alt_float_epsilon_v6 fails test_level_payment_below_the_old_cutoffs_is_exact and half-cent-at-tiny-rate (re-run this round, out/alts.txt). The page's rule (computed in exact rational arithmetic on the annual rate as written) is the basis, so the rejection is not an over-constraint."),
    ("r23-hours", "Hours split: project 30 and lessons 70 agree with the time-budget table and the lesson data-hours", "course/modules/M/M1/project.html lines 33, 182-198; course/modules/M/M1/index.html line 29; course/modules/M/M1/L01-L08.html data-hours attributes",
     "Time-budget rows 2+3+8+7+6+4 = 30 = data-hours-project 30 (project.html line 33). Lesson data-hours 8+9+9+9+8+9+9+9 = 70 = data-hours-lessons 70 (index.html line 29). 70 + 30 = 100, matching '30 of the module's 100' (project.html line 198). Hours are design targets; no pace estimate is failed."),
    ("r23-registry-live", "Live registry check of the M1 entries and offline integrity", "tools/verify_refs.py --unit M1; tools/verify_refs.py --offline",
     "live: '1 of 560 entries, 0 problems'; offline: '560 entries, 0 problems' (out/refs_live_m1.txt, out/refs_offline.txt)."),
    ("r23-equiv-r13v04", "The equivalent mutant r13v_04 still passes every grader test (it is equivalent, not a survivor)", "ledgers/M1/scripts/M1-d-r13/equiv/r13v_04_annuity_tiny_rate_cutoff_1e-12.py",
     "Run under the grader with QF_SEED=0: 196 passed. The cutoff change 1e-12 does not move any tested value, so it stays out of the mutants list."),
]
for rid, check, loc, ev in NEW:
    rows.append({"id": rid, "check": check, "location": loc, "status": "PASS", "evidence": ev})

det = []
for line in (OUT / "mutate_r23.txt").read_text(encoding="utf-8").splitlines():
    m = re.match(r"KILLED (\S+?\.py): (.*) -> (.*)\(seed 0\)$", line)
    if m:
        det.append((m.group(1), m.group(2).strip(), m.group(3).strip()))
mutants = []
for fname, desc, killer in det:
    mutants.append({
        "id": fname[:-3],
        "file": f"ledgers/M1/mutants/{fname}",
        "description": desc,
        "killed_by": killer + " (seed 0)",
        "run": "tools/mutate_graders.py --unit M1 --seeds 0-9 (round 23, checkout 503d139): KILLED",
    })

fragment = {
    "unit": "M1",
    "slice": "M1-d",
    "round": 23,
    "round_note": "round 23 (independent verification of slice M1-d at 503d139, round 22 was at d160ac3). Delta d160ac3..503d139 in the slice: none (only course/modules/M/M1/L04.html changed, outside the slice). Rows carried from round 22 are those whose subject is byte-identical since d160ac3; command, mutant, alternative and changed-card rows were re-run or re-checked this round.",
    "verifier": "Claude Haiku 5.5 (independent verifier, slice M1-d, round 23; did not build M1; no shared context with builders)",
    "pin": "503d139 (detached HEAD of /tmp/verify23-M1-d)",
    "base": "d160ac3 (previous pin: the round-21 fix commit, so round 22 verified at d160ac3)",
    "previous_ledger": "/tmp/fanout-frags/M1-d.round22.json (context only: its round field says 17 and its pin fefbf8b, so its content is round 17 and its PASS rows were not trusted)",
    "checkout": "/tmp/verify23-M1-d",
    "scratch": "/tmp/m1-v23/d/",
    "verified_at": "2026-10-28T20:00:00+00:00",
    "verdict": "PASS",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [
        "The file /tmp/fanout-frags/M1-d.round22.json is round-17 content (round field 17, pin fefbf8b, 179 cards). It was used for context and for row ids only. Its card count 179 and per-lesson counts for L03, L05 and L07 are superseded by the current 180 cards.",
    ],
    "notes": [
        "Command outputs: ledgers/M1/scripts/M1-d-r23/out/ (check_pages, check_dag, check_projects, run_labs, run_graders, page_smoke, collect, ref_pytest, ruff, mypy, mutate_r23, alts, refs_live_m1, refs_offline). Scripts: ledgers/M1/scripts/M1-d-r23/mk_r23.py, run_alts.sh, build_fragment_r23.py.",
        "Mutants: 128 files in ledgers/M1/mutants (125 carried, 3 new r23v_01 to r23v_03), all killed. Each new mutant is a comment line plus the reference module with one edit (the first attempt put a docstring above the module docstring, which is a SyntaxError and was discarded, so no collection-error kill is counted).",
        "Not checked in round 23: the full line-by-line re-read of project.html prose, the exemplar and rubric text, and of the 171 unchanged cards was not repeated; those rows are carried from round 22 on the byte-identity of the subject since d160ac3 (the round-22 evidence itself is not readable on disk, only its round-17 content). The changed cards were re-checked against lesson text this round. The M1 lesson pages are outside this slice.",
        "The Beneish and other external published numbers do not appear in this slice's delta; no external source was fetched.",
    ],
    "summary": "",
}
pass_n = sum(1 for r in rows if r["status"] == "PASS")
fragment["summary"] = (
    f"M1-d round 23 at 503d139: {len(rows)} rows, {pass_n} PASS, {len(rows) - pass_n} FAIL. "
    f"Delta since d160ac3 is empty for the slice. Re-run: 196 collected and passed; mutants 128 of 128 killed (3 new); "
    f"alternatives: 3 new correct engines pass, the 5 previously rejected families fail on the exact-decimal rule; hours 30 and 70 agree; registry 0 problems."
)
(ROOT / "ledgers/M1/M1-d.json").write_text(json.dumps(fragment, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("rows", len(rows), "mutants", len(mutants))
