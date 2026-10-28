"""Builds the round-15 AC1-d fragment (ledgers/AC1/AC1-d.json) from the round-14 fragment and round-15 evidence.

Rows re-verified this round carry new evidence; rows whose cited subject is byte-identical since cef676e carry the
round-14 evidence with the prefix required by the brief. Every round-14 row id is kept. Run with -I from the checkout.
"""
import datetime
import json
import re
from pathlib import Path

CHK = Path("/tmp/verify15-AC1-d")
OUT = CHK / "ledgers/AC1/scripts/AC1-d-r15/out"
R14 = json.load(open("/tmp/fanout-frags/AC1-d.round14.json", encoding="utf-8"))
PREFIX = "Carried from round 14 (%s byte-identical since the previous pin): "
PROJ_OK = "course/modules/AC/AC1/project.html (lines other than 366 and 368)"
LESSONS = "course/modules/AC/AC1/L01.html to L08.html and index.html"

old_rows = {r["id"]: r for r in R14["rows"]}
new = {}


def row(rid, check, location, status, evidence, fix=None):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        assert fix, rid
        r["fix"] = fix
    new[rid] = r


def carry(rid, files, location=None):
    old = old_rows[rid]
    assert old["status"] == "PASS", rid
    row(rid, old["check"], location or old["location"], "PASS", PREFIX % files + old["evidence"])


# --- command rows re-run this round -------------------------------------------------------------------------------
row("proj-run-graders", "2.6-autograder-reference", "course/modules/AC/AC1/grader/ (reference.py, test_project.py, instance.py)", "PASS",
    "Re-run: ledgers/AC1/scripts/AC1-d-r15/run_suite.sh on grader/reference.py for seeds 0 to 49: 50 of 50 seeds give '277 passed' (out/ref_50.out).")
row("proj-collect-count-176", "2.6-collect-count", "course/modules/AC/AC1/project.html line 368 ('collects 277 checks'); grader/test_project.py", "PASS",
    "Re-run: pytest --collect-only on grader/reference.py for seeds 0 to 49 gives '277 tests collected' on every seed (out/ref_50.out). The page says 277 and the count is 277. The previous round's 176 was superseded by the new tests.")
row("proj-local-suite-reference", "2.6-local-suite", "course/modules/AC/AC1/project.html lines 412-415 ('Running the suite locally')", "PASS",
    "Re-run with the page's flags (QF_SEED, pytest -q -p no:cacheprovider --assert=plain -W error test_project.py) on grader/reference.py, seed 0: '277 passed in 0.18s'. The page names pytest 9.0.2; the collect header reads pytest-9.0.2 under Python 3.14.8 locally (not Pyodide).")
row("proj-pyodide-smoke", "2.5-page-smoke", "course/modules/AC/AC1/project.html (and L01 to L03 lab pages)", "PASS",
    "Re-run: tools/page_smoke.py --unit AC1 --pages project.html -> 'page_smoke AC1: PASS', exit 0 (/tmp/v15d/smoke_project_r15.out).")
row("proj-check-pages", "2.9-structure", "course/modules/AC/AC1/*.html; cards.json", "PASS",
    "Re-run: tools/check_pages.py --all -> 'check_pages AC1: PASS' (out/check_pages.out), exit 0.")
row("proj-check-projects", "2.9-structure", "course/modules/AC/AC1/project.html (budget, rungs)", "PASS",
    "Re-run: tools/check_projects.py --all -> 'check_projects AC1: PASS' (out/check_projects.out), exit 0.")
row("proj-check-dag", "DAG", "project.html 'Concepts used here'; L01-L03 concept definitions", "PASS",
    "Re-run: tools/check_dag.py --all -> 'check_dag AC1: PASS' (out/check_dag.out), exit 0.")
row("proj-run-labs", "2.5-labs", "tests/labs/AC1/lab-AC1-project-1.py, -project-2.py, -project-3.py (and the L01-L08 twins)", "PASS",
    "Re-run: tools/run_labs.py --unit AC1 -> 'run_labs AC1: PASS (11/11)' (out/run_labs.out). Each twin also run alone under python -I -W error: exit 0, empty stderr. Output compared with the page's expected blocks: Lab 1 lines 245-253, Lab 2 lines 341-343, Lab 3 lines 513-518 match line for line.")
row("proj-lab-twin-embed", "2.5-labs", "project.html lab blocks (Lab 1 lines 56-253, Lab 2 lines 260-343, Lab 3 lines 423-518)", "PASS",
    "run_labs (above) checks that each page lab's code is byte-identical to its twin and that stdout matches the page's expected block; 11 of 11 labs pass. The lab blocks are unchanged since cef676e.")
row("proj-labs-ruff", "gate", "tests/labs/AC1; course/modules/AC/AC1/grader", "PASS",
    "Re-run: ruff check course/modules/AC/AC1/grader tests/labs/AC1 -> 'All checks passed!' (out/ruff.out); ruff format --check on the same paths exit 0.")
row("proj-mypy-gate", "gate", "tests/labs/AC1; course/modules/AC/AC1/grader", "PASS",
    "Re-run: mypy --no-incremental over the repository -> 'Success: no issues found in 153 source files', exit 0 (out/mypy.out).")
row("proj-verify-refs", "2.1-citations", "references/references.json; project.html line 534 (data-cite penman2013financial)", "PASS",
    "Re-run: tools/verify_refs.py --offline -> 'offline integrity: 560 entries, 0 problems' (out/vr_offline.out); tools/verify_refs.py --unit AC1 -> 'live re-verification of AC1: 2 of 560 entries, 0 problems' (out/vr_live_AC1.out). The registry is byte-identical since cef676e.")
row("proj-tests-labs-pytest", "2.5-labs (pytest)", "tests/test_run_labs.py, tests/test_labs.py, tests/test_page_checks.py", "PASS",
    "Re-run: .venv/bin/python -I -m pytest -q -p no:cacheprovider tests/test_run_labs.py tests/test_labs.py tests/test_page_checks.py -> dots only, exit 0 (out/pytest_labs.out).")
row("proj-starter-fails", "2.6-starter", "grader/starter.py; project.html line 364", "PASS",
    "Re-run: run_suite.sh on grader/starter.py, seed 0 -> '275 failed, 2 passed' (the two passes are the ACCOUNTS check and the standard-library import check, which the starter satisfies). project.html line 364 says every function raises NotImplementedError and the suite fails on the starter: each function test fails.")
row("proj-instances-carry", "2.6-data", "course/modules/AC/AC1/grader/instance.py", "PASS",
    "Re-run: make_instance(seed) for seeds 0 to 49 through the reference (out/ref_50.out: 277 passed each seed), so the generator yields 200 transactions and the suite passes on every seed. instance.py is byte-identical since cef676e.")

# --- hours and prose --------------------------------------------------------------------------------------------
row("proj-hours", "hours", "project.html line 33 (data-hours-project 30); the time-budget table (lines 386-402); index.html line 29 (data-hours-lessons 90); L01-L08 data-hours 11,12,11,11,12,12,11,10",
    "PASS", "Re-run by hand: the table rows are 1, 3, 4, 4, 3, 5, 2, 5, 3 hours, total 30 (line 399 states 30). The lesson hours sum to 11+12+11+11+12+12+11+10 = 90, and 90 + 30 = 120 (index.html line 31 and project line 399). No arithmetic inconsistency between the split and the lesson hours. Declared hours are design targets (architect ruling), not checked against pace.")
row("proj-prose-banned", "1.2/1.3-banned-phrases", "project.html lines 368 and 398; grader/test_project.py added lines", "PASS",
    "Re-run: grep of project.html for 'roughly', 'about', 'historically', ellipsis and process words (builder, round, verifier, unit report) finds none. The added lines of the grader (lines 658-686 and 1055-1068) were read; none contains a banned phrase.")
row("proj-alt-implementations", "2.6-over-constraint (architect ruling b)", "course/modules/AC/AC1/grader/test_project.py (whole suite) against alternative implementations",
    "PASS", "Three alternatives written this round (ledgers/AC1/scripts/AC1-d-r15/alts/): alt_r15_a_leap_arithmetic_table.py (leap year by arithmetic and a month-length table, no calendar import), alt_r15_b_next_day_probe.py (month end found by stepping one day forward; integer check by type), alt_r15_c_sorted_ledger_bisect.py (postings sorted by date and balances by bisect). Each runs the whole suite on seeds 0 to 49: 50 of 50 pass with 277 tests each (out/alts_50.out, 150 runs). The reference also passes 50 of 50.")
row("proj-overconstraint-nonmapping", "2.6-over-constraint (architect ruling b)", "grader/test_project.py test_post_raises_a_value_error parametrize list (lines 658-686); project.html line 366", "PASS",
    "The two new cases are 'an unbalanced entry of four lines' (debits 7, credits 6) and 'a line with both a debit and a credit on the last line of a balanced entry' (line 'equipment' 7 and 7). Both are named conditions of project.html line 366 ('an entry whose debits do not equal its credits'; 'a line with both a debit and a credit'). All three alternatives raise ValueError for both.")
row("proj-page-spec-carry-post-cases", "2.6-over-constraint", "grader/test_project.py test_post_raises_a_value_error parametrize list; project.html line 366", "PASS",
    "The post cases (lines 317-688) each name a condition listed on project.html line 366 (the list of named post conditions). The three alternatives pass them all.")
row("proj-no-expected-value-leak", "2.6-spec", "project.html line 368 ('A failing check names the property that failed and never prints the expected value')", "PASS",
    "grader/test_project.py: _check_values (lines 224-234) and must_raise (lines 97-103) pass fixed messages that name the key or condition, never the expected value. The new century test (lines 1055-1068) uses must_raise and _check_values in the same way. Read directly: the pytest.fail messages in _check_values (lines 230-234) and must_raise (line 103) name the key or the condition and never format an expected value.")
row("proj-grader-carry", "2.6-grader", "grader/test_project.py (delta hunks at lines 658-686, 1055-1068 and 1052-1053)", "PASS",
    "Each added test or case was read in full. The new tests pass on the reference and on the three alternatives (50 seeds), and the century test kills the blind-leap mutant of balance_sheet (v15_m04). The defect in the century test's comment is a separate row (proj-r15-century-test-comment).")
row("proj-line-368-grading-claims", "2.9-prose", "project.html line 368 (Grading mode)", "FAIL",
    "project.html line 368 says the suite covers 'the month-end rule, including century years'. The century cases (test_a_century_year_follows_the_400_year_rule) call balance_sheet only; the period-end list at lines 1011-1032 has no 2100-02-29 entry, so income_statement, cash_flow_statement and articulation_check are never tested on a century year. Three survivors show this (proj-r15-mutant-m01/m02/m03).",
    "Add \"2100-02-29\" to the period-end list of test_period_end_must_be_a_month_end (lines 1012-1032). Witness (run this round in /tmp/v15d/fix): with that line added the three blind-leap mutants fail (1 failed each), the balance control fails, and the reference and the three alternatives still give 281 passed.")
carry("proj-line-37-lede-seed", "course/modules/AC/AC1/project.html line 37")
carry("proj-footer-nothing-leaves", "course/modules/AC/AC1/project.html line 549")
carry("proj-line-377-working-capital-terms", "course/modules/AC/AC1/project.html line 377")
carry("proj-line-378-missing-space", "course/modules/AC/AC1/project.html lines 378-379")
carry("proj-balance-gap-sign-unenforced", "course/modules/AC/AC1/project.html line 378")
carry("proj-scope-sentence-line-352", "course/modules/AC/AC1/project.html line 352")
carry("proj-conventions-debit-balance-sentence", "course/modules/AC/AC1/project.html line 373")
carry("proj-page-lab-carry", "course/modules/AC/AC1/project.html lab blocks (lines 56-253, 260-343, 423-518)")
carry("proj-page-ladder-browser-carry", "course/modules/AC/AC1/project.html lines 40-47, 51-52, 406, 414, 533, 548")
carry("proj-r14-line-398-wording", "course/modules/AC/AC1/project.html line 398")
carry("proj-r14-test-large-amount", "course/modules/AC/AC1/grader/test_project.py test_a_large_amount_posts_at_its_full_value (lines 309-313)")
carry("proj-r13-year-edge-tests", "course/modules/AC/AC1/grader/test_project.py test_entries_on_the_first_and_last_days_of_the_year_post_and_count (lines 765-776 in the round-15 file)")
carry("proj-pytest-version-claim", "course/modules/AC/AC1/project.html line 415")
carry("proj-l01-pytest-claim-line-415", "course/modules/AC/AC1/project.html line 415")
carry("proj-index-explain-prop32", "course/modules/AC/AC1/index.html line 141")
carry("proj-l03-check6-prose", "course/modules/AC/AC1/L03.html line 669 and the Lab 3 printed labels")
carry("proj-l03-intangible-paragraph", "course/modules/AC/AC1/L03.html intangible-purchase paragraph")
carry("proj-l01-delta-prose-out-of-slice", "course/modules/AC/AC1/L01.html lines 48 and 559")
carry("proj-r13-l01-prop32-hypothesis-v", "course/modules/AC/AC1/L01.html line 388")
carry("proj-r13-l02-lowest-cash-sentences", "course/modules/AC/AC1/L02.html lines 133 and 535")
carry("proj-r13-l02-intangible-cite", "course/modules/AC/AC1/L02.html line 552")
carry("proj-r13-l03-def11-depreciation-cite", "course/modules/AC/AC1/L03.html lines 57 and 61")
carry("proj-r13-cards-L02", "course/modules/AC/AC1/cards.json AC1-c025 and AC1-c026 and L02.html lab output")
carry("proj-l02-omits-real-items", "course/modules/AC/AC1/L02.html line 552")
carry("proj-l03-def11-indirect-cite", "course/modules/AC/AC1/L03.html lines 57 and 71")
carry("proj-lab-l03-comment-scope", "tests/labs/AC1/lab-AC1-L03-1.py lines 606-621 and L03.html lines 606-621")
carry("proj-l03-check6-depreciation-reference", "course/modules/AC/AC1/L03.html line 669")
carry("proj-l01-pytest-claim-line-415", "course/modules/AC/AC1/project.html line 415")

# --- the grader's test-comment defect, found this round --------------------------------------------------------
row("proj-r15-century-test-comment", "2.9-prose (grader comment)", "grader/test_project.py lines 1056-1058 (test_a_century_year_follows_the_400_year_rule)", "FAIL",
    "The comment says 'Only the 2024 entries of SMALL are in the ledger, so both balances below are the balances of SMALL.' The first balance is at 2000-02-29 and the code asserts it is all zeros (dict.fromkeys(BALANCE_SHEET_KEYS, 0), lines 1061-1065); no entry of SMALL is dated on or before 2000-02-29. Only the 2100-02-28 balance equals SMALL_JAN_BALANCE_SHEET. The statement is wrong for one of the two balances.",
    "Replace the last sentence with: 'The 2100-02-28 balance is the January balance of SMALL; no entry is dated before 2024, so the 2000-02-29 balance is zero.'")

# --- the three blind-leap survivors and the page claim --------------------------------------------------------
MUT = "ledgers/AC1/mutants/"
row("proj-r15-mutant-m01-income-blind-leap", "2.5-mutation (new survivor, round 15, student error)", MUT + "v15_m01_income_statement_blind_leap_year.py; grader/test_project.py test_period_end_must_be_a_month_end", "FAIL",
    "Student error: income_statement validates the period end with a leap rule that has no century rule (2000 and 2100 both leap), and the other three functions are the reference. Probe: income_statement(post([]), '2100-02-29') returns a dict (accepted); the reference raises ValueError. Passes 277 of 277 on seeds 0 and 17 (out/mutants_v15_new.out). project.html line 366 states that each of the three statement functions and the articulation check raises for a period end that is not a month end, and that 2100-02-29 is not a date. No test calls income_statement on 2100-02-29.",
    "Add \"2100-02-29\" to the period-end list at grader/test_project.py lines 1012-1032 (witness: see proj-line-368-grading-claims, where the same line makes the three mutants fail).")
row("proj-r15-mutant-m02-cash-flow-blind-leap", "2.5-mutation (new survivor, round 15, student error)", MUT + "v15_m02_cash_flow_blind_leap_year.py; grader/test_project.py test_period_end_must_be_a_month_end", "FAIL",
    "Student error: cash_flow_statement with the same blind leap rule. Probe: cash_flow_statement(post([]), '2100-02-29') is accepted. Passes 277 of 277 on seeds 0 and 17 (out/mutants_v15_new.out). Same spec sentence as m01 (project.html line 366).",
    "Add \"2100-02-29\" to the period-end list at grader/test_project.py lines 1012-1032 (the mutant then fails).")
row("proj-r15-mutant-m03-articulation-blind-leap", "2.5-mutation (new survivor, round 15, student error)", MUT + "v15_m03_articulation_blind_leap_year.py; grader/test_project.py test_period_end_must_be_a_month_end", "FAIL",
    "Student error: articulation_check with the same blind leap rule. Probe: articulation_check(post([]), '2100-02-29') is accepted. Passes 277 of 277 on seeds 0 and 17 (out/mutants_v15_new.out). project.html line 366 names the articulation check among the four functions that must raise.",
    "Add \"2100-02-29\" to the period-end list at grader/test_project.py lines 1012-1032 (the mutant then fails).")
row("proj-r15-line-366-century-rule-four-functions", "2.9-spec (rule enforced by tests)", "course/modules/AC/AC1/project.html line 366 (Constraints)", "FAIL",
    "Line 366 states: 'Each of the three statement functions and the articulation check raises for a period end that is not a month end ... A year divisible by 4 is a leap year, except ... so 2000-02-29 is a month end, 2100-02-28 is one, and 2100-02-29 is not a date.' The suite enforces the 2100-02-29 case for balance_sheet only (test_a_century_year_follows_the_400_year_rule, line 1068). Architect ruling (a): a requirement the tests do not enforce must not be claimed; the three survivors show the gap.",
    "Add \"2100-02-29\" to the period-end list at grader/test_project.py lines 1012-1032 (it covers all four functions in one line).")
row("proj-r15-mutant-m04-balance-control", "2.5-mutation (control)", MUT + "v15_m04_balance_sheet_blind_leap_year.py", "PASS",
    "Control: the blind leap rule applied to balance_sheet only. balance_sheet(post([]), '2100-02-29') is accepted; the suite fails on seed 0 and seed 17 with 1 failed, 276 passed; first failure test_a_century_year_follows_the_400_year_rule (out/mutants_v15_new.out).")
row("proj-r15-mutant-m05-depreciation-gap-sign", "2.5-mutation (new, round 15)", MUT + "v15_m05_depreciation_gap_sign_reversed.py", "PASS",
    "depreciation_gap computed as expense less the change in accumulated depreciation (sign reversed). Killed on seed 0 and seed 17: 1 failed, 276 passed each; first failure test_articulation_gaps_report_a_ledger_that_does_not_articulate (out/mutants_v15_new.out).")
row("proj-r15-mutant-m06-dividends-paid-sign", "2.5-mutation (new, round 15)", MUT + "v15_m06_dividends_paid_sign_reversed.py", "PASS",
    "dividends_paid carries the wrong sign (a payout shown as an inflow). Killed: 23 failed on seed 0 and 18 on seed 17; first failure test_small_ledger_january_cash_flow (out/mutants_v15_new.out).")
row("proj-r15-alts-a-b-c", "2.6-over-constraint (architect ruling b)", "ledgers/AC1/scripts/AC1-d-r15/alts/alt_r15_a/b/c", "PASS",
    "Three genuinely different correct implementations pass the whole suite on seeds 0 to 49 (277 passed each seed; out/alts_50.out, 150 runs, 0 failures). They are the arithmetic leap rule with a month-length table, the next-day probe for month ends with a strict integer type check, and the date-sorted ledger with bisect balances.")

# --- the card defect and the new/changed cards ------------------------------------------------------------------
row("cards-c059-grade-basis", "2.7-cards (grade and basis)", "course/modules/AC/AC1/cards.json AC1-c059 (L04)", "FAIL",
    "The back changed this round to 'No. A difference that reverses later is not a difference in total profit (Corollary 2.3).' The answer is a proved statement: L04 Corollary 2.3 (line 115) says the cumulative difference is minus the unexpired balance, and reverses as it expires. The card still has grade 'C' with basis 'Lab 1 (SIMULATED)', and the Lab 1 numbers were removed from the back. Judgement: the answer rests on Corollary 2.3 and the expiry argument; the basis names a lab whose numbers the back no longer gives.",
    "Set grade to T and basis to 'Corollary 2.3 (L04 Section 2); the expiry identity of Proposition 2.2' (the lab's -4,974,286 now lives on card AC1-c132, which keeps grade C with basis Lab 1).")
row("cards-grades", "2.3-grades", "cards.json grade and basis fields (all cards)", "FAIL",
    "Grade and basis fields: the six changed or new cards were read (c059 fails, row cards-c059-grade-basis; c108 and c129 to c131 are ungraded definitional cards citing Definition 1.1; c132 is grade C with basis Lab 1, which its number supports). The other 126 cards are byte-identical and carry the round-14 grade check.",
    "Fix cards-c059-grade-basis.")
row("cards-L04", "2.7-cards", "cards.json c046-c060, c122, c132 (L04); L04.html", "FAIL",
    "c059 changed and fails (row cards-c059-grade-basis). c132 (new) was checked against L04.html and recomputed by script (row cards-c132-lab1-quarter7). The other L04 cards (c046 to c058, c060, c122) are byte-identical and carry their round-14 evidence.",
    "Fix cards-c059-grade-basis.")
row("cards-c059-c060-c070-c090", "2.7-cards", "cards.json AC1-c059 (L04), c060 (L04), c070 (L05), c090 (L06)", "FAIL",
    "c060, c070 and c090 are carried (byte-identical). c059 fails: its grade and basis do not match its answer (row cards-c059-grade-basis).",
    "Fix cards-c059-grade-basis.")
row("cards-c108-constraints", "2.7-cards (changed card)", "cards.json AC1-c108 (L08); L08.html Definition 1.1 (line 59)", "PASS",
    "Back: 'The cost C is a multiple of 10,000 cents, the book life L is a number of years, and C divided by L is a multiple of 100 cents (Definition 1.1).' L08.html line 59 (Definition 1.1): 'An asset has cost C, a multiple of 10,000 cents, and a book life of L years, where C / L is a multiple of 100 cents.' Matches. Front 'What constraints does the model's asset satisfy?' is answered by the back.")
row("cards-c129-c131-definition11-cites", "2.7-cards (new cards)", "cards.json AC1-c129, c130, c131 (L08); L08.html Definition 1.1 (line 59)", "PASS",
    "c129: 'Straight-line: b = C / L in each year t from 1 to L' matches 'Book depreciation is straight-line, b = C / L in each year t = 1, ..., L' (line 59). c130: 'In year t it is C p_t / 100, where the integer tax percentages p_1 to p_L sum to 100' matches 'tau_t = C p_t / 100, where the integers p_1, ..., p_L are the tax percentages and sum to 100' (line 59). c131: 'Yes. One flat rate of r percent applies to every year, and r is a whole number' matches 'the model's flat tax rate is a whole number of percent, r, the same in every year' (line 59). No grade field (definitional, as the other 46 ungraded cards).")
row("cards-c132-lab1-quarter7", "2.7-cards (new card, number)", "cards.json AC1-c132 (L04); L04.html lines 289, 344; tests/labs/AC1/lab-AC1-L04-1.py", "PASS",
    "Back: '-4,974,286 cents ... quarter-7 purchase of 6,632,381 cents, which has only its first share expensed by the horizon (Corollary 2.3).' Recomputed by running the lab's generate() with seed 2604: quarter-7 prepaid_paid 6632381; first share 6632381 // 4 = 1658095; unexpired 4974286. Lab 1 prints cum_difference_cents -4974286 (out of the twin run). L04.html line 344 states the same. Grade C with basis 'Lab 1 (SIMULATED)' is correct: the number is read off the lab.")
row("cards-L08", "2.7-cards", "cards.json c105-c108, c110-c121, c125 (L08); L08.html", "PASS",
    "Re-checked this round: c108 changed (row cards-c108-constraints, PASS); c105, c106, c107, c110-c121 and c125 are byte-identical since cef676e and were checked against L08.html in round 14 (see the carried rows). Definition 1.1 cited by c108, c129-c131 exists at L08.html line 59.")
row("cards-c001-c128-coverage-r15", "2.7-cards", "cards.json (132 cards) against L01-L08", "PASS",
    "All 132 cards were checked by script (numbers, labels, banned phrases, duplicates). The six cards added or changed since cef676e (AC1-c059, c108, c129 to c132) were read in full against their lessons and have their own rows. The other 126 cards are byte-identical since cef676e and carry their round-14 evidence.")
row("cards-inventory-and-dupes", "2.7-cards", "course/modules/AC/AC1/cards.json", "PASS",
    "Re-run by script: 132 cards; ids AC1-c001 to AC1-c132 contiguous; no duplicate id, front or back; lesson counts L01 16, L02 16, L03 18, L04 17, L05 14, L06 16, L07 14, L08 21. Fields only id, lesson, front, back, grade, basis.")
row("cards-numbers-in-lessons", "2.7-cards (numbers)", "cards.json; L01-L08 (tag-stripped text)", "PASS",
    "Re-run ledgers/AC1/scripts/AC1-d-r15/cards_numbers.py over 132 cards: every number appears in the card's lesson except AC1-c077's '5,000', which L06.html line 68 writes as 5{,}000 (LaTeX grouping; the script does not strip braces). Checked by reading line 68.")
row("cards-labels-resolve", "2.7-cards (labels)", "cards.json citations against each card's own lesson", "PASS",
    "Re-run ledgers/AC1/scripts/AC1-d-r15/cards_labels_r15.py over 132 cards: 'checked 132 cards', no MISS line (every Definition, Proposition, Theorem, Corollary, Remark or Lemma cited in a back exists in the card's lesson).")
row("cards-banned", "1.2/1.3-banned", "cards.json", "PASS",
    "Scan of all 132 fronts and backs for 'roughly', 'about <number>', 'historically', ellipsis, 'builder', 'round', 'verifier', 'unit report': no match.")
row("cards-registry-cites", "2.1-citations", "cards.json", "PASS",
    "Script: each of the 560 keys of references/references.json tested for substring presence in cards.json: none found. No card cites a registry key; cards cite only lesson labels.")
carry("cards-c015", "course/modules/AC/AC1/L01.html (Remark 2.2, line 103) and cards.json AC1-c015")
carry("cards-L01", "course/modules/AC/AC1/L01.html and cards.json AC1-c001 to AC1-c016 (except c007 and c015)")
carry("cards-c007-enforced-at-posting", "course/modules/AC/AC1/L01.html line 87 and cards.json AC1-c007")
carry("cards-L01-claims-table-scope", "course/modules/AC/AC1/L01.html Key results table (section 8) and cards.json")
carry("cards-c040-investing-scope", "course/modules/AC/AC1/L03.html Proposition 3.1 and cards.json AC1-c040")
carry("cards-c124-financing-scope", "course/modules/AC/AC1/L03.html Proposition 3.1 (iii), (ii) and cards.json AC1-c124")
carry("cards-c126-straight-line", "course/modules/AC/AC1/L03.html Definition 1.2 and Remark 6.3 and cards.json AC1-c126")
carry("cards-c027-prop32-scope", "course/modules/AC/AC1/L02.html Proposition 3.2 and cards.json AC1-c027")
carry("cards-c028-net-income-scope", "course/modules/AC/AC1/L02.html Definition 2.1 and Proposition 2.2 and cards.json AC1-c028")
carry("cards-c029-prop32-hypotheses", "course/modules/AC/AC1/L02.html Proposition 3.2 and cards.json AC1-c029")
carry("cards-c032-activity-split", "course/modules/AC/AC1/L02.html Definition 4.1 and cards.json AC1-c032")
carry("cards-L02", "course/modules/AC/AC1/L02.html and cards.json AC1-c017 to AC1-c032")
carry("cards-L03", "course/modules/AC/AC1/L03.html and cards.json AC1-c033 to AC1-c039, c041 to c045, c123, c126 to c128")
carry("cards-c033-definition11-scope", "course/modules/AC/AC1/L03.html Definition 1.1 (line 57) and cards.json AC1-c033")
carry("cards-c039-prop22-scope", "course/modules/AC/AC1/L03.html Proposition 2.2 and cards.json AC1-c039")
carry("cards-c042-thm51-scope", "course/modules/AC/AC1/L03.html Theorem 5.1 and cards.json AC1-c042")
carry("cards-c038-wrong-schedule", "course/modules/AC/AC1/L03.html Theorem 5.1 paragraph and cards.json AC1-c038")
carry("cards-L03-c123", "course/modules/AC/AC1/L03.html Proposition 4.2 and cards.json AC1-c123")
carry("cards-L03-theorem-5-1-print-claim", "course/modules/AC/AC1/L03.html Theorem 5.1 paragraph (line 135) and tests/labs/AC1/lab-AC1-L03-1.py")
carry("cards-L03-theorem-5-1-print-claim-hypotheses", "course/modules/AC/AC1/L03.html Theorem 5.1 hypotheses (line 127)")
carry("cards-c127-check2-not-independent", "course/modules/AC/AC1/L03.html and cards.json AC1-c127")
carry("cards-c128-lab-prints-four-of-five", "course/modules/AC/AC1/L03.html and cards.json AC1-c128")
carry("cards-L05", "course/modules/AC/AC1/L05.html and cards.json AC1-c061 to AC1-c074")
carry("cards-L06", "course/modules/AC/AC1/L06.html and cards.json AC1-c075 to AC1-c090")
carry("cards-L07", "course/modules/AC/AC1/L07.html and cards.json AC1-c091 to AC1-c101, c103, c104")
carry("cards-c098-citation", "course/modules/AC/AC1/L07.html Theorem 2.1 and Corollary 2.2 and cards.json AC1-c098")
carry("cards-c102-equity-wording", "course/modules/AC/AC1/L07.html Corollary 2.2 and cards.json AC1-c102")
carry("cards-c109-scope", "course/modules/AC/AC1/L08.html Definition 1.2 and cards.json AC1-c109")
carry("cards-c008-wording", "course/modules/AC/AC1/L01.html Definition 1.3 and cards.json AC1-c008")
carry("cards-c057", "course/modules/AC/AC1/L04.html Remark 1.2 and Section 4 and cards.json AC1-c057")
carry("cards-c069", "course/modules/AC/AC1/L05.html Section 2 and problem P3 and cards.json AC1-c069")
carry("cards-c071", "course/modules/AC/AC1/L05.html Section 3 and cards.json AC1-c071")
carry("cards-c079", "course/modules/AC/AC1/L06.html Definition 1.4 and cards.json AC1-c079")
carry("cards-c087", "course/modules/AC/AC1/L06.html Section 3 and cards.json AC1-c087")
carry("cards-c104", "course/modules/AC/AC1/L07.html Definition 1.1 and Theorem 1.3 and cards.json AC1-c104")
carry("cards-c052", "course/modules/AC/AC1/L04.html Proposition 2.1 and cards.json AC1-c052")
carry("cards-c013-scope", "course/modules/AC/AC1/L01.html Proposition 3.2 (line 388) and cards.json AC1-c013")
carry("cards-c088-scope", "course/modules/AC/AC1/L06.html Lab 1 figures and Proposition 2.3 and cards.json AC1-c088")
carry("cards-c018-wording", "course/modules/AC/AC1/L02.html Definition 1.1 and cards.json AC1-c018")
carry("cards-no-open-r10-fail", "course/modules/AC/AC1/cards.json entries of the round-10 and round-11 FAIL rows (none is AC1-c059 or AC1-c108)")

# --- mutant rows (re-run this round) --------------------------------------------------------------------------
RUN = {}
for line in (OUT / "mutants_r15.out").read_text().splitlines():
    name = line.split(" | ")[0]
    RUN[name] = line
for line in (OUT / "mutants_v15_new.out").read_text().splitlines():
    RUN[line.split(" | ")[0]] = line


def killed(name):
    line = RUN[name]
    return "failed" in line.split(" | ")[1] and "failed" in line.split(" | ")[2]


def mut_row(rid, check, names, location):
    bad = [n for n in names if not killed(n)]
    evidence = ("Re-run this round (ledgers/AC1/scripts/AC1-d-r15/run_mutants.sh): %d of %d files fail on seed 0 and seed 17 "
                "(out/mutants_r15.out): %s" % (len(names) - len(bad), len(names), ", ".join(names)))
    if bad:
        row(rid, check, location, "FAIL", "Surviving: " + ", ".join(bad), "See the surviving-mutant rows.")
    else:
        row(rid, check, location, "PASS", evidence)


ALL = sorted(RUN)
assert len(ALL) == 133, len(ALL)

mut_row("proj-mutants-new-r10-m58-m61", "2.5-mutation", [n for n in ALL if re.match(r"m(5[89]|6[01])_", n)], MUT)
mut_row("proj-mutants-m01-m08", "2.5-mutation", [n for n in ALL if re.match(r"m0[1-8]_", n)], MUT)
mut_row("proj-mutants-m11-m20", "2.5-mutation", [n for n in ALL if re.match(r"m(1[1-9]|20)_", n)], MUT)
mut_row("proj-mutants-m21-m25", "2.5-mutation", [n for n in ALL if re.match(r"m2[1-5]_", n)], MUT)
mut_row("proj-mutants-m33-m38", "2.5-mutation", [n for n in ALL if re.match(r"m3[3-8]_", n)], MUT)
mut_row("proj-mutant-m09-articulation-zero", "mutants", [n for n in ALL if re.match(r"m09_", n)], MUT + "m09_articulation_all_zero.py")
mut_row("proj-mutant-m10-depreciation-gap", "mutants", [n for n in ALL if re.match(r"m10_", n)], MUT + "m10_depreciation_gap_no_expense.py")
for rid, pre in (("proj-mutant-m26-payables-sign", "m26_"), ("proj-mutant-m27-cogs-from-balance", "m27_"),
                 ("proj-mutant-m28-timestamp-date-accepted", "m28_"), ("proj-mutant-m29-boolean-credit-accepted", "m29_"),
                 ("proj-mutant-m30-whitespace-date-accepted", "m30_"), ("proj-mutant-m31-account-name-case-folded", "m31_"),
                 ("proj-mutant-m32-retained-gap-sign", "m32_"), ("proj-mutant-m39-account-name-whitespace-stripped", "m39_"),
                 ("proj-mutant-m40-credit-float-accepted", "m40_"), ("proj-mutant-m41-week-date-accepted", "m41_"),
                 ("proj-mutant-m42-month-end-previous-length", "m42_"), ("proj-mutant-m43-negative-credit-absolute", "m43_"),
                 ("proj-mutant-m44-unbalanced-one-direction", "m44_"), ("proj-mutant-m45-negative-debit-clamped", "m45_"),
                 ("proj-mutant-m46-unpadded-date-accepted", "m46_"), ("proj-mutant-m47-numeric-string-amount", "m47_"),
                 ("proj-mutant-m89-first-day-entry-rejected", "m89_"), ("proj-mutant-m90-amount-cap-survives", "m90_")):
    mut_row(rid, "mutants", [n for n in ALL if n.startswith(pre)], MUT)
mut_row("proj-mutants-new-r9-three-written", "2.5-mutation", [n for n in ALL if re.match(r"m4[5-7]_", n)], MUT)
mut_row("proj-mutants-new-m26-m28", "2.5-mutation", [n for n in ALL if re.match(r"m2[6-8]_", n)], MUT)
mut_row("proj-mutants-m62-m71-fixer", "2.5-mutation", [n for n in ALL if re.match(r"m(6[2-9]|7[01])_", n)], MUT)
mut_row("proj-mutants-new-r11-m72-m75", "2.5-mutation", [n for n in ALL if re.match(r"m7[2-5]_", n)], MUT)
mut_row("proj-mutants-new-r12-m86-m89", "2.5-mutation", [n for n in ALL if re.match(r"m8[6-9]_", n)], MUT)
mut_row("proj-mutants-new-r13-m91-m93", "2.5-mutation", [n for n in ALL if re.match(r"m9[1-3]_", n)], MUT)
mut_row("proj-mutants-fx01-fx10", "2.5-mutation", [n for n in ALL if re.match(r"fx(0[1-9]|10)_", n)], MUT)
mut_row("proj-r14-mutant-m101", "2.5-mutation (new mutant, round 14)", ["m101_int32_amount_cap"], MUT + "m101_int32_amount_cap.py")
mut_row("proj-r14-mutant-m103", "2.5-mutation (new mutant, round 14)", ["m103_amount_rounded_to_whole_dollars"], MUT + "m103_amount_rounded_to_whole_dollars.py")
mut_row("proj-r14-mutant-m102", "2.5-mutation (round-14 survivor, now killed)", ["m102_century_blind_leap_year"], MUT + "m102_century_blind_leap_year.py")
mut_row("proj-r14-mutant-m104", "2.5-mutation (round-14 survivor, now killed)", ["m104_leap_rule_without_400_rule"], MUT + "m104_leap_rule_without_400_rule.py")
mut_row("proj-mutants-set-killed", "2.5-mutation (project slice)", [n for n in ALL], MUT)
new["proj-mutants-set-killed"]["status"] = "FAIL"
new["proj-mutants-set-killed"]["evidence"] = ("All 133 files re-run on seeds 0 and 17. 130 fail on both seeds. Three survive both seeds: "
    "v15_m01_income_statement_blind_leap_year, v15_m02_cash_flow_blind_leap_year, v15_m03_articulation_blind_leap_year "
    "(rows proj-r15-mutant-m01/m02/m03). m102 and m104 (round-14 survivors) now fail on both seeds.")
new["proj-mutants-set-killed"]["fix"] = "Add \"2100-02-29\" to the period-end list at grader/test_project.py lines 1012-1032; then the set is fully killed."

row("proj-page-spec-carry", "2.9-spec", "course/modules/AC/AC1/project.html line 366 (Constraints)", "FAIL",
    "Line 366 claims the century rule for the three statement functions and the articulation check (see proj-r15-line-366-century-rule-four-functions). The round-14 carry of the rule's wording is superseded; the new sentence on century years is only enforced for balance_sheet.",
    "Add \"2100-02-29\" to the period-end list at grader/test_project.py lines 1012-1032.")
row("proj-cards-c001-c126-coverage", "2.7-cards", "course/modules/AC/AC1/cards.json (132 cards) against L01-L08", "PASS",
    "Re-verified this round: all 132 cards checked by script; the six changed or new cards were read in full. The 126 cards of round 14 that are byte-identical since cef676e are carried; AC1-c059 and AC1-c108 changed (rows cards-c059-grade-basis FAIL and cards-c108-constraints PASS); AC1-c129 to c132 are new (rows cards-c129-c131-definition11-cites and cards-c132-lab1-quarter7).")
row("proj-r14-alternatives-new", "2.6-over-constraint (architect ruling b)", "ledgers/AC1/scripts/AC1-d-r15/alts/ (round 15); round-14 alternatives carried", "PASS",
    "Round-15 alternatives (alt_r15_a, alt_r15_b, alt_r15_c) pass the whole suite on seeds 0 to 49 (out/alts_50.out, 150 runs, each '277 passed'). The round-14 alternatives were not re-run this round; the grader hunks they tested are unchanged except the two new post cases and the century test, which the round-15 alternatives exercise.")

# --- every round-14 id must now have a decision ----------------------------------------------------------------
missing = [rid for rid in old_rows if rid not in new]
print("round-14 ids without a round-15 decision:", missing)

# --- write the fragment ----------------------------------------------------------------------------------------------
rows = [new[rid] for rid in old_rows] + [new[rid] for rid in new if rid not in old_rows]
mutants = []
SURVIVORS = {"v15_m01_income_statement_blind_leap_year", "v15_m02_cash_flow_blind_leap_year", "v15_m03_articulation_blind_leap_year"}
for name in ALL:
    entry = {"id": name, "description": name.replace("_", " "), "file": MUT + name + ".py"}
    if name in SURVIVORS:
        entry["survived"] = "277 passed on seed 0 and seed 17 (out/mutants_v15_new.out); a FAIL row names it"
    else:
        entry["killed_by"] = "seed 0 and seed 17 (out/mutants_r15.out or out/mutants_v15_new.out): " + RUN[name].split(" | ")[1].strip() + "; " + RUN[name].split(" | ")[2].split(" | ")[0].strip()
    mutants.append(entry)
counts = {s: sum(1 for r in rows if r["status"] == s) for s in ("PASS", "FAIL", "UNVERIFIABLE")}
killed = sum(1 for m in mutants if m.get("killed_by"))
fragment = {
    "unit": "AC1",
    "slice": "AC1-d",
    "round": 15,
    "verifier": "Claude Haiku 5.5, independent verifier for AC1-d, round 15; did not build AC1; read the round-14 fragment as context and computed the delta cef676e..c093bf5 on AC1 (project.html lines 366 and 368, grader/test_project.py lines 658-686, 1055-1068, cards.json entries AC1-c059, c108, c129 to c132, mutants v15_m01 to v15_m06 written this round)",
    "pin": "c093bf5 (detached worktree /tmp/verify15-AC1-d)",
    "base": "cef676e (round-14 pin); previous fragment /tmp/fanout-frags/AC1-d.round14.json",
    "checkout": "/tmp/verify15-AC1-d",
    "scratch": "/tmp/v15d/",
    "verified_at": datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat(),
    "verdict": "FAIL" if counts["FAIL"] else "PASS",
    "summary": {"rows": len(rows), "PASS": counts["PASS"], "FAIL": counts["FAIL"], "UNVERIFIABLE": counts["UNVERIFIABLE"],
                "mutants": len(mutants), "mutants_killed_seed0_and_seed17": killed},
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "Delta cef676e..c093bf5 on the slice: project.html lines 366 and 368; grader/test_project.py (two post cases at "
        "lines 658-686, the century test at lines 1055-1068); cards.json (AC1-c059 and c108 changed, c129 to c132 added). "
        "Lessons, index, labs, references and tools are byte-identical since cef676e. Re-run this round: check_pages, "
        "check_projects, check_dag, run_labs (11/11), the three project twins under python -I -W error, page_smoke for "
        "project.html, ruff, mypy, verify_refs offline and live (AC1), pytest of the lab tests, collect-only and full runs "
        "of the reference on seeds 0 to 49 (277 each), three new alternatives on seeds 0 to 49 (150 runs, all pass), and "
        "all 133 mutants on seeds 0 and 17. Round-14 survivors m102 and m104 are now killed by the century test. New "
        "survivors (round 15): the leap rule without the century rule in income_statement, cash_flow_statement and "
        "articulation_check (v15_m01 to m03): the period-end list at grader/test_project.py lines 1012-1032 has no "
        "2100-02-29 entry, so only balance_sheet is tested on that date; adding it kills all three and keeps the reference "
        "and the alternatives green (witness run in /tmp/v15d/fix). Also FAIL: the grader comment at lines 1056-1058 "
        "(both balances called SMALL balances; the 2000 balance is zero) and the card AC1-c059 (grade C, basis Lab 1, for "
        "an answer that now rests on Corollary 2.3). Not checked: the Pyodide 314.0.7 runtime itself (only the local "
        "Python 3.14.8 and pytest 9.0.2); the live reference check covers only the 2 AC1 entries that the tool re-reads "
        "(the other registry entries were checked offline); the 46 ungraded cards were not re-graded beyond their citations."
    ),
}
OUT_PATH = CHK / "ledgers/AC1/AC1-d.json"
OUT_PATH.write_text(json.dumps(fragment, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", OUT_PATH, fragment["verdict"], fragment["summary"])
