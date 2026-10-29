"""Build the round-23 CF1 slice d fragment from the round-22 rows (carry or re-verify each row)."""
import json, pathlib

CHK = "/tmp/verify23-CF1-d"
O = f"{CHK}/ledgers/CF1/scripts/CF1-d-r23/out"
prev = json.load(open("/tmp/fanout-frags/CF1-d.round22.json"))
CARRY = ("Carried from round 22 (course/modules/CF/CF1/project.html, grader/, tests/labs/CF1/, references/ and the "
         "lesson and hub pages byte-identical since the previous pin d160ac3; the cited cards.json entries byte-identical, "
         "the file having changed only at CF1-c014, CF1-c054 and by the appended CF1-c110):")

over = {
 "cards-grade-semantics": ("FAIL", "Round 23: cards.json now has 110 entries (59 T, 51 C; scan of the file). CF1-c110 is graded C "
   "(basis 'Assumption 4.0 and Remark 4.3; Problem R3'), but the claim it restates ('the decision can change with the rate that "
   "applies', Problem R3) is graded T in the lesson: L01.html line 466 table row 'With different borrowing and lending rates the "
   "decision depends on which rate applies (Problem R3)' carries data-grade T, and the R3 values -1 + 1.05/1.06 = -0.009434 and "
   "-1 + 1.05/1.03 = +0.019417 are computed on the page (L01.html line 446). BLUEPRINT section 3: T means proved on the page. "
   "Fix (owning builder, cards.json only): set CF1-c110 grade to T and basis to 'Problem R3 (values on the page) and Remark 4.3'. "
   "The other 109 entries were checked for grade and basis in round 22 and their grade fields are byte-identical."),
 "cards-c110-content": None,
 "cards-c014-section7-locator": None,
 "cards-c054-theorem41": None,
 "cards-missing-grade-or-basis": ("PASS", "Round 23 scan of course/modules/CF/CF1/cards.json (110 entries): every entry has a grade in {T, C} and a non-empty basis or cite; CF1-c110 has basis 'Assumption 4.0 and Remark 4.3; Problem R3' and no cite key (no key is required when a basis is given)."),
 "cards-duplicate-scan": ("PASS", "Round 23 re-run: duplicate ids [], duplicate fronts [], duplicate backs [] over all 110 entries; ids are CF1-c001 to CF1-c110 with no gap (python -I scan)."),
 "cards-numbers-in-lesson": ("PASS", "Round 23: the numbers in the three changed entries appear in their lessons: CF1-c054 '4.1' (L04.html line 126, Theorem 4.1), CF1-c110 '4.0', '4.1', '4.3' (L01.html lines 119, 114-ish block and 147) and 'R3' (L01.html line 442); CF1-c014 has no number. Other entries carried."),
 "cards-count-vs-plan": ("PASS", "Round 23: 110 entries; per lesson L01 19, L02 18, L03 17, L04 23, L05 18, L06 15 (sum 110). plans/CF1-build-plan.md section 12 sets no fixed count per lesson (its text: 'the count follows BUILDER_RULES section 7'); no page states a card count (grep '[0-9]+ cards' in course/modules/CF/CF1/*.html: none)."),
 "cards-misconception-locator": ("PASS", "Round 23: the locators of the changed entries exist: CF1-c014 'Section 7, third misconception' = L01.html line 340 (third li of section.misconceptions, h2 line 330); CF1-c110 'Remark 4.3' = L01.html line 147; 'Problem R3' = L01.html line 441. Other entries carried."),
 "cards-cite-keys-and-locators": ("PASS", "Round 23: the changed entries cite no registry key (CF1-c014 and CF1-c110 use basis; CF1-c054 uses basis 'Theorem 4.1, proved in Section 4'); CF1-c071 and CF1-c084 carried, byte-identical."),
 "cards-changed-c014-c037-c047-c057": ("PASS", "Round 23: CF1-c014 re-verified (see cards-c014-section7-locator); CF1-c037, c047, c057 carried, byte-identical entries."),
 "r15-cards-c054-c056-c058-c060-c094": ("PASS", "Round 23: CF1-c054 re-verified (see cards-c054-theorem41); CF1-c056, c058, c060, c094 carried, byte-identical entries."),
 "proj-banned-phrases": ("PASS", "Round 23: grep -n -i -E 'roughly half|about 6%|historically|\\.\\.\\.|…|builder|verifier|round|unit report|REQUEST' course/modules/CF/CF1/cards.json: no match (empty output). project.html byte-identical to d160ac3 (carried)."),
 "proj-process-words-r10": ("PASS", "Round 23: the same grep over cards.json finds no process word; project.html byte-identical (carried)."),
 "proj-collect-count-50-seeds": ("PASS", "Round 23: collect-only count on the reference engine, seeds 0-9 and 1407000004: 157 each (ledgers/CF1/scripts/CF1-d-r23/out/collect_r23.out); course/modules/CF/CF1/project.html line 192 says 157."),
 "proj-grader-reference-50-seeds": ("PASS", "Round 23: tools/run_graders.py --unit CF1 --seeds 0-49: 'run_graders CF1: PASS (reference 50/50 seeds, slowest 0.4 s)', exit 0 (out/run_graders.out)."),
 "proj-structure-and-gates": ("PASS", "Round 23 re-run: check_pages.py --unit CF1 PASS (out/check_pages.out); check_dag.py --all 'check_dag CF1: PASS' (out/check_dag.out); check_projects.py --all 'check_projects CF1: PASS' (out/check_projects.out), exit 0 each."),
 "proj-check-dag": ("PASS", "Round 23 re-run: tools/check_dag.py --all, 'check_dag CF1: PASS', exit 0 (ledgers/CF1/scripts/CF1-d-r23/out/check_dag.out)."),
 "proj-verify-refs": ("PASS", "Round 23 re-run: tools/verify_refs.py --unit CF1 'live re-verification of CF1: 2 of 560 entries, 0 problems' (out/verify_refs_live_unit.out); tools/verify_refs.py --offline 'offline integrity: 560 entries, 0 problems' (out/verify_refs_offline.out). references/ byte-identical."),
 "proj-ruff-format": ("PASS", "Round 23 re-run: ruff check . 'All checks passed!'; ruff format --check . '220 files already formatted'; exit 0 each (out/ruff_check.out)."),
 "proj-mypy-grader-gate": ("PASS", "Round 23 re-run: .venv/bin/mypy --no-incremental 'Success: no issues found in 153 source files', exit 0 (out/mypy.out)."),
 "proj-page-smoke": ("PASS", "Round 23 re-run: tools/page_smoke.py --unit CF1 'page_smoke CF1: PASS', exit 0; every CF1 page and lab timed (out/page_smoke.out)."),
 "r13-twins-under-python-I-W-error": ("PASS", "Round 23 re-run: each of the nine tests/labs/CF1/lab-CF1-*.py run as python -I -W error exits 0 (out/twins_I_W_error.out)."),
 "r13-run-graders-50": ("PASS", "Round 23 re-run: run_graders CF1 seeds 0-49 PASS (out/run_graders.out)."),
 "proj-mutants-killed": ("PASS", "Round 23: 211 CF1 mutant files in ledgers/CF1/mutants/*.py. tools/mutate_graders.py --unit CF1 --seeds 0-9: 208 of 208 KILLED, 'mutate_graders CF1: PASS (208/208 killed)' (out/mutate_r23.out; the 208 files existed when the run started). The three new files r23d_01..03 were run with run_mut_one.sh: each KILLED at seed 0 (proj-mutants-r23-new)."),
 "proj-alternatives-correct": ("PASS", "Round 23 re-run of every alternative engine in ledgers/CF1/scripts/CF1-d-r*/ (65 files, 46 unique by SHA-256), seeds 0-9 each: 46 of 46 PASS (out/alts_r23.out; run_alts23.py)."),
 "proj-pytest-lab-helper": ("PASS", "Round 23 re-run: .venv/bin/python -I -m pytest -q tests/test_labs.py tests/test_page_checks.py tests/test_refs.py tests/test_docs_figures.py tests/test_curriculum.py: all dots, no failure (out/pytest_r23.out); run_labs CF1 '9/9' PASS (out/run_labs.out)."),
}

new_rows = [
 {"id": "cards-c110-content", "check": "cards: changed entry CF1-c110 restates its lesson text",
  "location": "course/modules/CF/CF1/cards.json CF1-c110 (new, line ~881); L01.html lines 119-125 (Assumption 4.0), 147-148 (Remark 4.3), 323 (misconception-list bullet), 442-446 (Problem R3 and solution)",
  "status": "PASS",
  "evidence": "Round 23: the front asks whether the one-rate market of Assumption 4.0 holds with two rates; the back says 'No', that Assumption 4.0 needs one rate r at every period (L01.html line 120: 'At every period the owner can lend or borrow any amount at the rate r'), that the proof of Proposition 4.1 does not apply with two rates (line 323), and that the decision can change with the rate that applies (Remark 4.3, line 148; Problem R3 values -0.009434 and +0.019417, line 446). Text agrees with the lesson; grade defect is in cards-grade-semantics."},
 {"id": "cards-c014-section7-locator", "check": "cards: changed entry CF1-c014 agrees with L01 section 7",
  "location": "course/modules/CF/CF1/cards.json CF1-c014 (line 107-112); L01.html line 340 (section 7 third misconception) and line 342",
  "status": "PASS",
  "evidence": "Round 23: the new back (the rate is the return on an alternative of the same risk, Section 1; a loan rate is set by the lender's terms and need not match the risk) is the first two sentences of L01.html line 342; the locator 'Section 7, third misconception' matches the third li of section.misconceptions (h2 'Misconceptions', line 330; the li's wrong statement is line 340, 'A project's rate is the firm's loan rate by default.'). Grade C with basis 'convention, Section 1 (the meaning of r) and Section 7' matches the lesson's convention reading."},
 {"id": "cards-c054-theorem41", "check": "cards: changed entry CF1-c054 restates Theorem 4.1",
  "location": "course/modules/CF/CF1/cards.json CF1-c054 (line ~427-433); L04.html lines 126-130 (Theorem 4.1, proof line 131)",
  "status": "PASS",
  "evidence": "Round 23: Theorem 4.1 defines flows -K_A, C_A and -K_B, C_B with all four amounts positive, Delta K = K_B - K_A, Delta C = C_B - C_A; if Delta K != 0 and Delta C/Delta K > 0 the NPVs are equal at exactly one rate r* = Delta C/Delta K - 1. The card gives r* = (C_B - C_A)/(K_B - K_A) - 1 under the same two conditions and says 'K is the outlay and C the inflow', which matches the theorem's definitions. Grade T with basis 'Theorem 4.1, proved in Section 4' matches the lesson's T claim (L04.html line 126, data-grade T). The worked case (r* = 20 per cent, L04.html line 135) is not restated in the card."},
 {"id": "proj-mutants-r23-new", "check": "project grader: three new student-error mutants are killed",
  "location": "ledgers/CF1/mutants/r23d_01_working_capital_released_one_year_late.py; r23d_02_irr_search_window_too_narrow.py; r23d_03_last_year_depreciation_shield_dropped.py; ledgers/CF1/scripts/CF1-d-r23/make_mutants23.py, run_mut_one.sh",
  "status": "PASS",
  "evidence": "Round 23: each mutant is a copy of grader/reference.py with one student error. r23d_01 (working capital held one year past the last year; the flow at year life is non-zero): KILLED at seed 0 by test_working_capital_investment_and_recovery_sum_to_zero. r23d_02 (IRR search window narrowed to x in [1e-2, 1e2], spec at project.html line 207): KILLED at seed 0 by test_irr_finds_roots_across_the_whole_search_window. r23d_03 (depreciation shield dropped in the last year): KILLED at seed 0 by test_depreciation_shield_is_depreciation_times_tax_rate. No survivor."},
 {"id": "proj-alternatives-r23-new-engines", "check": "project grader: alternative correct implementations pass",
  "location": "ledgers/CF1/scripts/CF1-d-r*/alts/ (65 files, 46 unique); ledgers/CF1/scripts/CF1-d-r23/run_alts23.py",
  "status": "PASS",
  "evidence": "Round 23: all 46 unique engines pass the CF1 suite on seeds 0-9 (out/alts_r23.out: 46 lines ': PASS (10 seeds)', no FAIL). Engines differ in numerical method (Horner and running discount factor NPV, geometric bisection IRR, fsum payback, expanded Fisher), so no numerical cutoff of the reference is required."},
]

rows = []
for r in prev["rows"]:
    rid = r["id"]
    if rid in over and over[rid] is not None:
        st, ev = over[rid]
        rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": st, "evidence": ev})
    elif rid in over:  # placeholder for cards content rows, handled below
        continue
    else:
        ev = r["evidence"] if r["evidence"].startswith("Round") else CARRY + " " + r["evidence"]
        rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": r["status"], "evidence": ev})
ids = {r["id"] for r in rows}
for nr in new_rows:
    assert nr["id"] not in ids
    rows.append(nr)
# keep all previous ids
prev_ids = [r["id"] for r in prev["rows"]]
assert set(prev_ids) <= {r["id"] for r in rows}, set(prev_ids) - {r["id"] for r in rows}

extra = [f"ledgers/CF1/mutants/r23d_0{i}_{n}.py" for i, n in [(1, "working_capital_released_one_year_late"), (2, "irr_search_window_too_narrow"), (3, "last_year_depreciation_shield_dropped")]]
mutants = list(prev["mutants"]) + [
  {"file": extra[0], "description": "r23d_01: working capital is held one year past the last year of the project, so the balance does not return to zero in year life.", "killed_by": "test_working_capital_investment_and_recovery_sum_to_zero (seed 0)"},
  {"file": extra[1], "description": "r23d_02: the IRR search window is narrowed to x in [1e-2, 1e2], missing roots at rates beyond about -0.99 or 99.", "killed_by": "test_irr_finds_roots_across_the_whole_search_window (seed 0)"},
  {"file": extra[2], "description": "r23d_03: the depreciation tax shield is dropped in the last year of life.", "killed_by": "test_depreciation_shield_is_depreciation_times_tax_rate (seed 0)"},
]
frag = {
 "unit": "CF1", "slice": "CF1-d", "round": 23,
 "verifier": "independent verifier (Haiku), round 23 of CF1 slice d (project page incl. case-memo rubric, grader, project labs, cards.json; project slice needs mutants)",
 "pin": "503d139 (detached, /tmp/verify23-CF1-d)",
 "base": "d160ac3 (round-22 pin; delta computed with git diff --stat d160ac3 503d139; the slice hunks are cards.json only: CF1-c014, CF1-c054 and the appended CF1-c110)",
 "checkout": "/tmp/verify23-CF1-d", "scratch": "/tmp/CF1-v/d23",
 "verified_at": "2026-10-28T00:00:00+00:00",
 "verdict": "FAIL",
 "rows": rows,
 "mutants": mutants,
 "registry_flags": prev["registry_flags"],
 "freshness_flags": prev["freshness_flags"],
 "notes": ("Round-23 delta for this slice: cards.json only (CF1-c014 back, CF1-c054 back, new CF1-c110). project.html, grader/, tests/labs/CF1/, references/ and all lesson/index pages are byte-identical to d160ac3 (git diff --name-only). "
           "Re-run: check_pages, check_dag, check_projects, run_graders 0-49, run_labs, page_smoke, ruff, mypy, verify_refs live and offline, collect-only 157 on 11 seeds, pytest (labs, page checks, refs, docs figures, curriculum), mutate_graders (208/208), the three new mutants, all 46 alternatives. "
           "Not re-run: the live-web reads of external sources (none are cited by the changed entries); the full prose audit of project.html (byte-identical, carried)."),
 "summary": ("CF1-d round 23 (pin 503d139): %d rows; FAIL on one row: cards-grade-semantics, because CF1-c110 is graded C while the lesson grades the same claim T (L01.html line 466). Fix: set CF1-c110 grade to T. All other rows PASS (carried rows keep their round-22 subject, byte-identical). Mutants: 211 of 211 killed (3 new). Alternatives: 46 of 46 pass. Collect 157." % len(rows)),
}
out = pathlib.Path(f"{CHK}/ledgers/CF1/CF1-d.json")
out.write_text(json.dumps(frag, indent=1, ensure_ascii=False) + "\n")
print("rows", len(rows), "mutants", len(mutants), "FAIL", [r["id"] for r in rows if r["status"] != "PASS"])
