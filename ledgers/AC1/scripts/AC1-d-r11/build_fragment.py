"""Builds ledgers/AC1/AC1-d.json for round 11 (verifier checkout /tmp/verify11-AC1-d, pin 91946cf)."""

import json
import re
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path("/tmp/verify11-AC1-d")
OUT = Path("/tmp/AC1-v11/AC1-d")
SUITE = "ledgers/AC1/scripts/AC1-d-r11/run_suite.sh"
CARRY = "Carried from round 10 (course/modules/AC/AC1/cards.json entry and cited lesson passage byte-identical since the previous pin af08ad1): "
CARRY_PROJ = "Carried from round 10 (course/modules/AC/AC1/project.html and the cited lines byte-identical since the previous pin af08ad1): "
CARRY_GRADER = "Carried from round 10 (course/modules/AC/AC1/grader/instance.py byte-identical since af08ad1): "

rows = []


def row(rid, check, location, status, evidence, fix=None):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix or "see evidence"
    rows.append(r)


# ---- command rows and grader --------------------------------------------------------------------------------------
row("proj-run-graders", "2.6-autograder-reference", "course/modules/AC/AC1/grader/ (reference.py, instance.py, test_project.py)", "PASS",
    "Re-run this round: reference.py installed as statements.py, run per seed with -I -W error --assert=plain (" + SUITE + "). Seeds 0-49: every seed prints '264 passed' (output in " + str(OUT / "run") + "/all<seed>)."
    )
row("proj-collect-count-176", "2.6-spec-test-count", "project.html line 368 ('collects 264 checks'); grader/test_project.py", "PASS",
    "project.html line 368 says 264. 'pytest --collect-only -q' on the reference: 264 tests collected for seeds 0, 7, 49 and a full run on seeds 0-49 reports 264 passed each. The count matches the page.")
row("proj-local-suite-reference", "2.6-autograder-local-run", "grader/test_project.py; project.html grading panel", "PASS",
    "Local command on the page's flags (QF_SEED=0 pytest -q -p no:cacheprovider --assert=plain -W error test_project.py) on the reference: 264 passed in 0.15s.")
row("proj-pyodide-smoke", "2.6-autograder-pyodide", "course/modules/AC/AC1/project.html (labs 1-3, grader panel)", "PASS",
    "tools/page_smoke.py --unit AC1 --pages project.html: 'page_smoke AC1: PASS' (output " + str(OUT / "page_smoke_project.out") + ").")
row("proj-check-pages", "2.9-structure", "course/modules/AC/AC1/*.html; cards.json", "PASS",
    "tools/check_pages.py --all exit 0; 'check_pages AC1: PASS' (" + str(OUT / "check_pages.out") + ").")
row("proj-check-projects", "2.6-hours-and-structure", "course/modules/AC/AC1/project.html (budget, rungs)", "PASS",
    "tools/check_projects.py --all exit 0; 'check_projects AC1: PASS'.")
row("proj-check-dag", "2.9-dag-concepts", "project.html 'Concepts used here'", "PASS",
    "tools/check_dag.py --all exit 0; 'check_dag AC1: PASS'.")
row("proj-run-labs", "2.5-labs", "tests/labs/AC1/lab-AC1-project-1.py, -project-2.py, -project-3.py and the L01-L08 twins", "PASS",
    "tools/run_labs.py --unit AC1: 'run_labs AC1: PASS (11/11)'. Each twin run alone as python -I -W error: exit 0, stderr 0 bytes (lab-AC1-L01-1 ... lab-AC1-project-3). L03 output re-read: Checks 1-4 print the gap 0.00 and True; Check 6 prints the new labels.")
row("proj-lab-twin-embed", "2.5-lab-embed-equals-twin", "project.html lab blocks (Lab 1 56-253, Lab 2 260-343, Lab 3 420-518); tests/labs/AC1/lab-AC1-project-*.py", "PASS",
    "run_labs.py checks each embedded lab's code byte-identical to its twin and its stdout against the page's expected output: 11/11 PASS. The project.html lab blocks are not in the delta (diff af08ad1..91946cf touches only lines 45 and 368 of project.html).")
row("proj-labs-ruff", "2.9-lint", "tests/labs/AC1; course/modules/AC/AC1/grader", "PASS",
    ".venv/bin/python -m ruff check and ruff format --check on both paths: 'All checks passed!', '15 files already formatted' (" + str(OUT / "ruff.out") + ").")
row("proj-mypy-gate", "2.9-types", "tests/labs/AC1; course/modules/AC/AC1/grader", "PASS",
    ".venv/bin/python -m mypy --no-incremental on both paths: 'Success: no issues found in 15 source files' (" + str(OUT / "mypy.out") + ").")
row("proj-verify-refs", "2.1-citations", "references/references.json; project.html (data-cite penman2013financial)", "PASS",
    "tools/verify_refs.py --offline: 'offline integrity: 560 entries, 0 problems' (exit 0). tools/verify_refs.py --unit AC1 (live): '2 of 560 entries, 0 problems' (exit 0). No citation was added or changed in the delta.")
row("proj-hours", "2.9-hours", "project.html line 35 (data-hours-project 30), time-budget rows; index.html data-hours-lessons 90; L01-L08 data-hours 11,12,11,11,12,12,11,10", "PASS",
    "Lesson hours sum to 90 (11+12+11+11+12+12+11+10). Project time-budget rows sum to 30 (1+3+4+4+3+5+2+5+3). 90+30=120 matches the hub. Hours are design targets (architect ruling); no pace estimate is failed.")
row("proj-prose-banned", "2.9-banned-phrases", "project.html; cards.json; grader/test_project.py; L01-L03 changed passages", "PASS",
    "Scan of every added line in the delta for TODO, TBD, lorem, roughly, historically, about N%, an ellipsis, 'left as an exercise', 'obviously', 'clearly' and scope words: none in a banned form; scope words ('only', 'all', 'every', 'always') checked in the context rows below.")
row("proj-alt-implementations", "2.6-alternatives-pass", "course/modules/AC/AC1/grader/test_project.py (whole suite) against three correct alternatives and the type-strict variant", "FAIL",
    "Alternatives (ledgers/AC1/scripts/AC1-d-r11/alts/), seeds 0-9: alt_r11_dict_by_account.py 264 passed on all 10 seeds; alt_r11_strptime_next_day.py (strptime dates, next-day month-end test) 264 passed on all 10 seeds. alt_r11_type_errors_for_shape.py (reference with TypeError for a non-mapping transaction and for lines given as a string or mapping) fails 3 tests on every seed: test_post_raises_a_value_error[a transaction that is not a mapping], [lines given as a mapping], [lines given as a string]. The page's named conditions do not include these shapes (see proj-overconstraint-unnamed-post-cases).",
    "Accept any exception type for the unnamed shapes or drop those cases from test_post_raises_a_value_error; keep ValueError for the nine named conditions.")
row("proj-overconstraint-nonmapping", "2.6-over-constraint", "grader/test_project.py test_post_raises_a_value_error parametrize list (added cases 'a transaction that is not a mapping', 'lines given as a mapping', 'lines given as a string'); project.html line 366", "FAIL",
    "project.html line 366: 'Every named error condition raises ValueError ... The named conditions are these.' and gives nine conditions (a transaction without a date or without lines; a bad date; an empty list of lines; a line without account, debit or credit; an account outside the chart; a non-integer amount; a negative amount; both or neither side; an unbalanced entry). The three shapes above are not named, so the page states no exception type for them; the grader requires ValueError. A correct implementation that raises TypeError for them (alt_r11_type_errors_for_shape.py) fails 3 checks on seeds 0-9. Each other added case maps to a named condition (the date and amount cases are 'not in the form YYYY-MM-DD', 'not an integer', 'without a date').",
    "In test_post_raises_a_value_error, remove the three unnamed shape cases, or add them to the page's named list with 'raises ValueError' so the spec states the requirement.")
row("proj-mutants-set-killed", "2.6-mutants", "ledgers/AC1/mutants/ (75 files: m01-m75)", "PASS",
    "Re-ran all 75 mutants on the round-11 grader for seeds 0 and 17 (ledgers/AC1/scripts/AC1-d-r11/run_mutants.sh; output mutants_all_r11.out): every mutant has at least one failing test on both seeds. Killed count 75/75.")
row("proj-mutants-new-r10-m58-m61", "2.6-mutants-new", "ledgers/AC1/mutants/ m58-m61", "PASS",
    "The four round-10 mutants each fail on seeds 0 and 17 (mutants_all_r11.out).")
row("proj-mutants-m01-m08", "2.6-mutants", "ledgers/AC1/mutants/ m01-m08", "PASS", "Each fails on seeds 0 and 17 (mutants_all_r11.out); killed_by in the mutants list.")
row("proj-mutants-m11-m20", "2.6-mutants", "ledgers/AC1/mutants/ m11-m20", "PASS", "Each fails on seeds 0 and 17 (mutants_all_r11.out).")
row("proj-mutants-m21-m25", "2.6-mutants", "ledgers/AC1/mutants/ m21-m25", "PASS", "Each fails on seeds 0 and 17 (mutants_all_r11.out).")
row("proj-mutants-m33-m38", "2.6-mutants", "ledgers/AC1/mutants/ m33-m38", "PASS", "Each fails on seeds 0 and 17 (mutants_all_r11.out).")
row("proj-mutant-m09-articulation-zero", "2.6-mutant", "ledgers/AC1/mutants/m09_articulation_all_zero.py", "PASS", "Fails on seeds 0 and 17 (mutants_all_r11.out); first failing test in killed_by.txt.")
row("proj-mutant-m10-depreciation-gap", "2.6-mutant", "ledgers/AC1/mutants/m10_depreciation_gap_no_expense.py", "PASS", "Fails on seeds 0 and 17 (mutants_all_r11.out).")
row("proj-mutant-m26-payables-sign", "2.6-mutant", "ledgers/AC1/mutants/m26_payables_increase_sign_reversed.py", "PASS", "Fails on seeds 0 and 17 (mutants_all_r11.out).")
row("proj-mutant-m27-cogs-from-balance", "2.6-mutant", "ledgers/AC1/mutants/m27_cogs_from_balance_not_flow.py", "PASS", "Fails on seeds 0 and 17 (mutants_all_r11.out).")
row("proj-mutant-m28-timestamp-date-accepted", "2.6-mutant", "ledgers/AC1/mutants/m28_timestamp_truncated_accepted.py", "PASS", "Fails on seeds 0 and 17 (mutants_all_r11.out).")
row("proj-mutant-m29-boolean-credit-accepted", "2.6-mutant", "ledgers/AC1/mutants/m29_boolean_credit_accepted.py", "PASS", "Fails on seeds 0 and 17 (mutants_all_r11.out).")
row("proj-mutant-m30-whitespace-date-accepted", "2.6-mutant", "ledgers/AC1/mutants/m30_whitespace_date_accepted.py", "PASS", "Fails on seeds 0 and 17 (mutants_all_r11.out).")
row("proj-mutant-m31-account-name-case-folded", "2.6-mutant", "ledgers/AC1/mutants/m31_account_name_case_folded.py", "PASS", "Fails on seeds 0 and 17 (mutants_all_r11.out).")
row("proj-mutant-m32-retained-gap-sign", "2.6-mutant", "ledgers/AC1/mutants/m32_retained_gap_dividends_added.py", "PASS", "Fails on seeds 0 and 17 (mutants_all_r11.out).")
row("proj-mutant-m39-account-name-whitespace-stripped", "2.6-mutant", "ledgers/AC1/mutants/m39_account_name_whitespace_stripped.py", "PASS", "Fails on seeds 0 and 17 (mutants_all_r11.out).")
row("proj-mutant-m40-credit-float-accepted", "2.6-mutant", "ledgers/AC1/mutants/m40_credit_float_accepted.py", "PASS", "Fails on seeds 0 and 17 (mutants_all_r11.out).")
row("proj-mutant-m41-week-date-accepted", "2.6-mutant", "ledgers/AC1/mutants/m41_week_date_accepted.py", "PASS", "Fails on seeds 0 and 17 (mutants_all_r11.out).")
row("proj-mutant-m42-month-end-previous-length", "2.6-mutant", "ledgers/AC1/mutants/m42_month_end_uses_previous_month_length.py", "PASS", "Fails on seeds 0 and 17 (mutants_all_r11.out).")
row("proj-mutant-m43-negative-credit-absolute", "2.6-mutant", "ledgers/AC1/mutants/m43_negative_credit_taken_as_absolute.py", "PASS", "Fails on seeds 0 and 17 (mutants_all_r11.out).")
row("proj-mutant-m44-unbalanced-one-direction", "2.6-mutant", "ledgers/AC1/mutants/m44_unbalanced_only_when_debits_exceed_credits.py", "PASS", "Fails on seeds 0 and 17 (mutants_all_r11.out).")
row("proj-mutant-m45-negative-debit-clamped", "2.6-mutant", "ledgers/AC1/mutants/m45_negative_debit_clamped_to_zero.py", "PASS", "Fails on seeds 0 and 17 (mutants_all_r11.out).")
row("proj-mutant-m46-unpadded-date-accepted", "2.6-mutant", "ledgers/AC1/mutants/m46_strptime_date_accepts_unpadded.py", "PASS", "Fails on seeds 0 and 17 (mutants_all_r11.out).")
row("proj-mutant-m47-numeric-string-amount", "2.6-mutant", "ledgers/AC1/mutants/m47_numeric_string_amount_accepted.py", "PASS", "Fails on seeds 0 and 17 (mutants_all_r11.out).")
row("proj-mutants-new-r9-three-written", "2.6-mutants", "ledgers/AC1/mutants/ m45 to m47", "PASS", "Fail on seeds 0 and 17 (mutants_all_r11.out).")
row("proj-mutants-new-m26-m28", "2.6-mutants", "ledgers/AC1/mutants/ m26-m28, m29-m32, m33-m41, m42-m57", "PASS", "All fail on seeds 0 and 17 (mutants_all_r11.out).")
row("proj-mutants-m62-m71-fixer", "2.6-mutants", "ledgers/AC1/mutants/ m62-m71 (added in 91946cf, not by this verifier)", "PASS",
    "The ten mutants added in the fix commit each fail on seeds 0 and 17 (mutants_all_r11.out). Their docstrings name the error; the errors are student errors (e.g. m62 balance checked over the whole ledger, m71 February always has 29 days).")
row("proj-mutants-new-r11-m72-m75", "2.6-mutants-new", "ledgers/AC1/mutants/m72_gross_profit_deducts_operating_expense.py, m73_depreciation_gap_uses_year_to_date_charge.py, m74_articulation_check_skips_month_end_rule.py, m75_post_marks_each_input_transaction.py", "PASS",
    "Four new student-error mutants written this round from grader/reference.py by one edit each. m72 gross profit deducts operating expense (killed by the income-statement tests); m73 depreciation gap uses the year-to-date charge (5 failures on seed 0, 11 on seed 7); m74 articulation_check skips the month-end rule (3 failures); m75 post marks each input transaction (1 failure: test_post_does_not_change_its_argument). All four fail on seeds 0 and 17. No survivor.")
row("proj-page-spec-carry", "2.4-spec-vs-suite", "project.html line 366 (Constraints: 'Every named error condition raises ValueError ... The named conditions are these'); grader/test_project.py", "PASS",
    CARRY_PROJ + "the sentence at line 366 is unchanged; the defect in the grader's cases is recorded in proj-overconstraint-nonmapping.")
row("proj-page-spec-carry-post-cases", "2.4-spec-vs-suite", "grader/test_project.py test_post_raises_a_value_error parametrize list (added cases)", "FAIL",
    "Re-verified this round: the added cases 'a transaction that is not a mapping', 'lines given as a mapping', 'lines given as a string' test a shape the page does not name (see proj-overconstraint-nonmapping). Other added cases (date None, empty date, day 0, month 0, letter in date, 31 April, account None, empty account, amount None, boolean False, balances only with another entry) each map to a named condition.",
    "Remove the three unnamed shape cases or name them in the page's list.")
row("proj-no-expected-value-leak", "2.4-page-claim-vs-output", "project.html line 368 ('A failing check names the property that failed and never prints the expected value'); grader/test_project.py _check_values (lines 224-236)", "PASS",
    "Round 10 FAIL re-verified as fixed. With the documented command (no --tb flag), the mutant m03 (dividends not deducted) run gives 44 failures with 0 long numbers and 0 'expected =' lines; --tb=short, --tb=line, --tb=native and --tb=long --showlocals also print no expected dict. Across the 71 earlier mutants the default output shows only inputs (test transactions) and source lines; 'expected' values are not printed. Caveat recorded: -l / --showlocals prints test-frame locals (the candidate's got, ledger, net, dividends), which are the candidate's values, not the oracle's, for the mutants checked. _check_values sets __tracebackhide__ = True; pytest.fail messages name the key only.")
row("proj-grader-carry", "2.6-grader-file", "grader/test_project.py (whole file read; delta hunks read in full)", "FAIL",
    "The grader file was read in full this round (diff af08ad1..91946cf, 187 changed lines): oracle helpers, the leak fix (__tracebackhide__), 24 added parametrize cases (15 post cases, 7 period-end strings, 2 added period-end values), 12 new test functions. Reference passes 264 on seeds 0-49. The file fails on one point: the unnamed-shape cases in test_post_raises_a_value_error (proj-overconstraint-nonmapping).",
    "See proj-overconstraint-nonmapping.")
row("proj-line-368-grading-claims", "2.4-page-claims", "project.html line 368 (collect count, seeds, warnings, coverage list, 'never prints the expected value')", "PASS",
    "Count 264: collected and run (proj-collect-count-176). Seeds 0-49: 50 runs, 264 passed each. Warnings as errors: the command uses -W error. Coverage list: each item traced to a test name in the file (chart of accounts; standard-library imports; posting rules and named errors; silence and return values; statement functions for 12 month ends; balance identity; cash tie; net change; retained earnings; operating cash flow; four gaps; month-end rule; hand-worked January ledger). Boundary cases named on the page are each a test: balances-only-with-another-entry, one-cent entry, zero on one side, repeated entry, two entries on one date, empty list of transactions. 'Never prints the expected value' verified by proj-no-expected-value-leak.")
row("proj-line-37-lede-seed", "2.9-lede", "project.html line 37 and the grader panel", "PASS", CARRY_PROJ + "line 37 unchanged; the seed claim is consistent with the 50-seed run.")
row("proj-footer-nothing-leaves", "2.9-footer", "project.html line 549 footer ('nothing you write leaves it')", "PASS", CARRY_PROJ + "line 549 unchanged.")
row("proj-line-377-working-capital-terms", "2.4-convention-formula", "project.html line 377 (Cash flow statement, indirect method)", "PASS", CARRY_PROJ + "line 377 unchanged; the formula matches grader/reference.py cash_flow_statement.")
row("proj-line-378-missing-space", "2.9-prose", "project.html lines 378-379 (Articulation gaps)", "PASS", CARRY_PROJ + "unchanged.")
row("proj-balance-gap-sign-unenforced", "2.4-page-claim", "project.html line 378 (Conventions, Articulation gaps)", "PASS", CARRY_PROJ + "unchanged; the suite's balance_gap test checks zero only, as the page says.")
row("proj-scope-sentence-line-352", "2.4-scope", "project.html line 352 (Context)", "PASS", CARRY_PROJ + "unchanged.")
row("proj-conventions-debit-balance-sentence", "2.4-convention", "project.html line 373 (Conventions, Balance through a date)", "PASS", CARRY_PROJ + "unchanged.")
row("proj-page-lab-carry", "2.5-lab-page", "project.html lab blocks (Lab 1 56-253, Lab 2 260-343, Lab 3 420-518)", "PASS", "run_labs AC1 11/11 (proj-run-labs); blocks unchanged in the delta.")
row("proj-page-ladder-browser-carry", "2.9-ladder", "project.html lines 40-47, 51-52, 406, 414, 533, 548", "PASS",
    "Re-verified: line 45 (Rung 2) now says 'the ending cash and the three articulation lines left as blanks'. Lab 2 (project.html lines 259-343) has four blanks: ending_cash, cash_gap, retained_change, earnings_gap, i.e. ending cash and three articulation lines. Other lines unchanged.")
row("proj-instances-carry", "2.6-instance", "course/modules/AC/AC1/grader/instance.py", "PASS", CARRY_GRADER + "the file is not in the delta; make_instance(seed) for seeds 0-49 runs in the 50-seed grader run.")
row("proj-cards-c001-c126-coverage", "2.7-coverage", "course/modules/AC/AC1/cards.json (128 cards)", "PASS",
    "Every card id AC1-c001 .. AC1-c128 present once (no gaps, no duplicates; 128 entries). No duplicate or near-duplicate fronts or backs (difflib ratio above 0.85 only for c019/c021 and c040/c124, which are different questions). Card ids are covered by the lesson-group rows (cards-L01 to cards-L08 and the per-card rows); every id AC1-c001 to AC1-c128 falls in one of them.")

# ---- cards ---------------------------------------------------------------------------------------------------------
row("cards-inventory-and-dupes", "2.7-cards-inventory", "course/modules/AC/AC1/cards.json (128 cards)", "PASS",
    "Re-run: 128 entries; ids unique; lessons L01 16, L02 16, L03 18, L04 16, L05 14, L06 16, L07 14, L08 18. Grade counts: C 44, T 41, no grade 43 (definitions, misconceptions and formulas carry no grade by BUILDER_RULES 7; every C card has a basis).")
row("cards-grades", "2.3-grades", "cards.json grade and basis fields", "PASS",
    "Every card with grade C has a non-empty basis (script check). Grade T cards re-read in the card rows. New cards AC1-c127 (grade C, basis 'Lab 3 (SIMULATED); the paragraph after Theorem 5.1 in Section 5') and AC1-c128 (grade C, same basis) match their paragraph.")
row("cards-numbers-in-lessons", "2.7-card-numbers", "cards.json; L01-L08 (tag-stripped text)", "PASS",
    "ledgers/AC1/scripts/AC1-d-r11/cards_numbers.py lists each number in each card and whether it appears in its own lesson. All appear except AC1-c077 '5,000', which L06 line 68 writes as the TeX '5{,}000' (checked by reading the line: floor((L rho + 5{,}000)/10{,}000)). Tool artefact, not a mismatch.")
row("cards-labels-resolve", "2.7-card-citations", "cards.json citations against each card's own lesson", "PASS", "Each parenthetical citation in the changed cards resolves to a definition, proposition, theorem or remark in the card's lesson (see the card rows).")
row("cards-banned", "2.7-banned", "cards.json", "PASS", "No banned phrase in any card (scan of front and back).")
row("cards-registry-cites", "2.7-registry", "cards.json", "PASS", "No card carries a registry key; the cards cite lesson definitions, propositions and labs only.")
row("cards-c015", "2.7-card", "cards.json AC1-c015 (L01, grade T, changed); L01.html Remark 2.2 (line 43-44)", "PASS",
    "Back now lists the four posting checks exactly as Remark 2.2 does: balances, accounts exist, non-negative integer cents, not both a debit and a credit. The remark's 'does not refuse a line that carries neither' is consistent with the card, which does not claim it. Re-verified against the changed text.")
row("cards-L01", "2.7-cards", "cards.json c001-c016 (except c007, c015); L01.html", "PASS",
    "c001-c006, c008-c014, c016 carried from round 10 (cards byte-identical and the cited L01 passages unchanged: Definitions 1.1-1.3, Proposition 2.1, Proposition 3.2, Example 3.3, Lab 1 figures). c009 numbers 255,314.48 - 30,594.17 = 224,720.31 (arithmetic checked).")
row("cards-c007-enforced-at-posting", "2.7-card", "cards.json AC1-c007 (L01); L01.html Double-entry bookkeeping paragraph (Section 2)", "FAIL",
    "The card back says 'The rule is enforced at posting, not at the end of a period (Section 2).' Round 11 diff removed the sentence 'The rule is enforced at posting, not at the end of a period.' from L01 Section 2 (af08ad1 line 37; now line 37 reads only 'In this lab the rule is enforced at posting'). grep of L01.html for 'end of a period' now finds only card c007. The card therefore states a general claim the current lesson does not make, and cites a location that no longer contains it.",
    "Change the back to 'In this lab the rule is enforced at posting: an unbalanced entry is refused (Section 2).' or restore the removed sentence in L01 Section 2 and keep the card.")
row("cards-L01-claims-table-scope", "2.7-table-vs-remark", "course/modules/AC/AC1/L01.html Key results (section 8), row 'A balanced entry posted to the wrong account passes the check (Remark 2.2)' (line 559)", "FAIL",
    "Unchanged since af08ad1 (round 10 FAIL not fixed in 91946cf). The basis cell reads 'The posting check tests balance, integer non-negative cents and at most one side per line (Remark 2.2)'. Remark 2.2 (L01 line 43-44) lists four posting checks; the fourth is 'that its accounts exist'. The cell omits it and then says the account test 'belongs to the lab, not to Definition 1.1', which contradicts the remark. Card AC1-c015 (changed) now states all four checks, so the table and the card disagree.",
    "Replace the cell with 'The posting check tests balance, that accounts exist, integer non-negative cents and at most one side per line (Remark 2.2); a line with neither side passes it. The lab also refuses an account outside its chart of accounts (Lab 1).'")
row("cards-c040-investing-scope", "2.7-card-scope", "cards.json AC1-c040 (grade T, L03); L03.html Proposition 3.1 (hypotheses (i)-(iv))", "PASS", CARRY + "AC1-c040 unchanged; Proposition 3.1 unchanged.")
row("cards-c124-financing-scope", "2.7-card-scope", "cards.json AC1-c124 (grade T, L03); L03.html Proposition 3.1 (iii), (ii)", "PASS", CARRY + "AC1-c124 unchanged; Proposition 3.1 unchanged.")
row("cards-c126-straight-line", "2.7-card", "cards.json AC1-c126 (grade C, L03); L03.html Definition 1.2 and Remark 6.3", "PASS", CARRY + "Definition 1.2 text unchanged: 'the charge is an equal amount for each quarter of the life... The lab's assets have no residual value.'")
row("cards-c027-prop32-scope", "2.7-card-scope", "cards.json AC1-c027 (grade T, L02); L02.html Proposition 3.2 (hypotheses, line 41)", "PASS",
    "Round 10 FAIL fixed. Back now states the hypotheses: 'balanced entries, equity accounts only common stock and dividends, and only the four income accounts of Definition 2.1'. These are the hypotheses of L02 Proposition 3.2 (line 41), word for word in substance.")
row("cards-c028-net-income-scope", "2.7-card", "cards.json AC1-c028 (grade T, L02); L02.html Definition 2.1 and Proposition 2.2 (line 33: hypothesis, only the four income accounts)", "PASS", CARRY + "re-read this round; the hypothesis 'only the four income accounts of Definition 2.1' matches Proposition 2.2 (line 33).")
row("cards-c029-prop32-hypotheses", "2.7-card-scope", "cards.json AC1-c029 (grade T, L02); L02.html Proposition 3.2 (line 40-41)", "PASS", CARRY + "re-read: the card's conditions match Proposition 3.2's hypotheses on line 41.")
row("cards-c032-activity-split", "2.7-card", "cards.json AC1-c032 (grade C, basis 'Convention of Lab 2 (Definition 4.1)'); L02.html Definition 4.1", "PASS", CARRY + "unchanged; the convention is stated in L02 Definition 4.1 and Section 'Caveats' line 428.")
row("cards-L02", "2.7-cards", "cards.json c017-c032; L02.html", "PASS",
    "c027, c028, c029, c032 re-verified above. c019-c021 cite L02 Definition 1.2 (unchanged). c017, c018, c022-c026, c030, c031 carried from round 10 (cards byte-identical; the cited L02 passages are unchanged, and the only L02 change in the delta is the depreciation sentence of the net-income paragraph, which no card cites).")
row("cards-L03", "2.7-cards", "cards.json c033-c039, c041-c045, c123, c126, c127, c128; L03.html", "PASS",
    "c033, c039, c042 re-verified (Round 10 FAILs fixed). c034-c038, c041, c043-c045 carried from round 10: cards byte-identical; their Lab 3 numbers (1,300,000.00; 2,191,615.64) appear in the unchanged output and text. New c127 and c128 verified below.")
row("cards-c033-definition11-scope", "2.7-card-scope", "cards.json AC1-c033 (What is articulation?); L03.html Definition 1.1 (line 24)", "PASS",
    "Round 10 FAIL fixed. Back now says 'under the hypotheses of Proposition 2.2, indirect operating cash flow equals the direct figure (Definition 1.1)', which matches Definition 1.1's clause 'under the hypotheses of Proposition 2.2, operating cash flow can be computed from net income by the indirect method and gives the same figure as the direct method'.")
row("cards-c039-prop22-scope", "2.7-card-scope", "cards.json AC1-c039 (grade T); L03.html Proposition 2.2 (hypotheses (i)-(v)) and key-results row", "PASS",
    "Round 10 FAIL fixed. Front and back are conditional on hypotheses (i)-(v) of Proposition 2.2, and the back cites the Proposition's conclusion 'the indirect operating cash flow ... equals the sum of the operating cash lines of the year'.")
row("cards-c042-thm51-scope", "2.7-card-scope", "cards.json AC1-c042 (grade T); L03.html Theorem 5.1 (hypotheses) and key-results row", "PASS",
    "Round 10 FAIL fixed. Front and back are conditional on the hypotheses of Theorem 5.1, which the back lists as those of Propositions 2.2, 3.1 and 4.2 of L03, Proposition 3.2 of L02 with its hypotheses, and Proposition 4.2 of L02 with the cash-line hypothesis. These match the theorem's text (line 53).")
row("cards-c038-wrong-schedule", "2.7-card", "cards.json AC1-c038 (grade T); L03.html Theorem 5.1 paragraph and misconception 'Statements that articulate are correct'", "PASS", CARRY + "unchanged.")
row("cards-L03-c123", "2.7-card", "cards.json AC1-c123 (grade T); L03.html Proposition 4.2 and its proof", "PASS", CARRY + "unchanged.")
row("cards-L03-theorem-5-1-print-claim", "2.7-card", "L03.html Theorem 5.1 paragraph (line 56); tests/labs/AC1/lab-AC1-L03-1.py", "PASS",
    "Lab output re-read: Check 1 prints gaps 0.00 each year; Checks 2, 3, 4 print True. The paragraph says 'The lab checks four of its five parts' and 'Checks 2, 3 and 4 print True', both consistent with the output (the fifth part, investing and financing, is not printed; output has no such line).")
row("cards-L03-theorem-5-1-print-claim-hypotheses", "2.7-card", "L03.html Theorem 5.1 hypotheses (line 53)", "PASS", "Hypotheses line re-read: consistent with the cards c039, c042, c127, c128.")
row("cards-c127-check2-not-independent", "2.7-card", "cards.json AC1-c127 (grade C, basis 'Lab 3 (SIMULATED); the paragraph after Theorem 5.1 in Section 5'); L03.html line 56 paragraph", "PASS",
    "The card says Check 2 prints True and that this is 'not an independent test of Proposition 2.2 (the Theorem 5.1 paragraph)'. The paragraph says 'It is not an independent test of the theorem, which the proof already gives', and the proof gives Check 2's claim as Proposition 2.2 ('The first claim is Proposition 2.2'). The card names the proposition the proof attributes the claim to; the paragraph wording is 'the theorem'. Accepted: the attribution is stated in the proof.")
row("cards-c128-lab-prints-four-of-five", "2.7-card", "cards.json AC1-c128 (grade C); L03.html Theorem 5.1 paragraph; Lab 3 output", "PASS",
    "The card says the lab prints four of the five parts, Checks 1-4, and not Proposition 3.1's investing and financing equalities. The paragraph says 'The lab checks four of its five parts' and 'The investing and financing equalities of Proposition 3.1 ... are not printed by the lab'. Lab output has Checks 1-4 as described.")
row("cards-L04", "2.7-cards", "cards.json c046-c060, c122; L04.html", "PASS", CARRY + "the cited L04 passages are unchanged in the delta (no L04 file changed).")
row("cards-L05", "2.7-cards", "cards.json c061-c074; L05.html", "PASS", CARRY + "no L05 file changed in the delta.")
row("cards-L06", "2.7-cards", "cards.json c075-c090; L06.html", "PASS", CARRY + "no L06 file changed in the delta. c077 number check re-run (see cards-numbers-in-lessons).")
row("cards-L07", "2.7-cards", "cards.json c091-c101, c103, c104; L07.html", "PASS", CARRY + "no L07 file changed in the delta.")
row("cards-c098-citation", "2.7-card", "cards.json AC1-c098 (L07); L07 Theorem 2.1 (c)(d) and Corollary 2.2", "PASS", CARRY + "no L07 change.")
row("cards-c102-equity-wording", "2.7-card", "cards.json AC1-c102 (grade T, L07); L07.html Corollary 2.2", "PASS", CARRY + "no L07 change.")
row("cards-L08", "2.7-cards", "cards.json c105-c108, c110-c121, c125; L08.html", "PASS", CARRY + "no L08 change in the delta.")
row("cards-c109-scope", "2.7-card", "cards.json AC1-c109 (L08); L08.html Definition 1.2", "PASS", CARRY + "no L08 change.")
row("cards-c008-wording", "2.7-card", "cards.json AC1-c008 (L01); L01.html Definition 1.3", "PASS", CARRY + "Definition 1.3 unchanged in the delta.")
row("cards-c057", "2.7-card", "cards.json AC1-c057 (L04); L04 Remark 1.2 and Section 4", "PASS", CARRY + "no L04 change.")
row("cards-c069", "2.7-card", "cards.json AC1-c069 (L05); L05 Section 2 and problem P3", "PASS", CARRY + "no L05 change.")
row("cards-c071", "2.7-card", "cards.json AC1-c071 (L05); L05 Section 3", "PASS", CARRY + "no L05 change.")
row("cards-c079", "2.7-card", "cards.json AC1-c079 (L06); L06 Definition 1.4", "PASS", CARRY + "no L06 change.")
row("cards-c087", "2.7-card", "cards.json AC1-c087 (L06); L06 Section 3", "PASS", CARRY + "no L06 change.")
row("cards-c104", "2.7-card", "cards.json AC1-c104 (L07); L07 Definition 1.1 and Theorem 1.3", "PASS", CARRY + "no L07 change.")
row("cards-c052", "2.7-card", "cards.json AC1-c052 (L04); L04 Proposition 2.1", "PASS", CARRY + "no L04 change.")
row("cards-c013-scope", "2.7-card", "cards.json AC1-c013 (L01); L01 Proposition 3.2", "PASS", CARRY + "Proposition 3.2 text unchanged; the card's hypotheses match its line 281-282.")
row("cards-c088-scope", "2.7-card", "cards.json AC1-c088 (L06); L06 Lab 1 figures and Proposition 2.3", "PASS", CARRY + "no L06 change.")
row("cards-c018-wording", "2.7-card", "cards.json AC1-c018 (L02); L02 Definition 1.1", "PASS", CARRY + "Definition 1.1 unchanged.")
row("cards-c059-c060-c070-c090", "2.7-card", "cards.json AC1-c059, c060 (L04), c070 (L05), c090 (L06)", "PASS", CARRY + "no change in those lessons.")

# ---- delta notes (out of slice or context) -------------------------------------------------------------------------
row("proj-index-explain-prop32", "2.4-scope", "course/modules/AC/AC1/index.html explain line (Proposition 3.2 with no write-offs, returns or allowances)", "PASS",
    "The changed hub explain now says 'Under Proposition 3.2 with no write-offs, returns or allowances, revenue less cash received equals the change in receivables: 2,500 less 1,900 is 600'. Proposition 3.2 hypothesis (i) (L01 line 282) states 'no write-offs, returns or allowances'; 2,500 - 1,900 = 600 (arithmetic checked).")
row("proj-l03-check6-prose", "2.5-lab-prose", "L03.html interpretation paragraph (Check 6) and Lab 3 printed labels", "PASS",
    "Lab output re-read: Check 6 prints 'retained earnings with this year's dividend not deducted would be ...' for 2025-2027 and the gap 200,000.00 equals dividends: True; operating gap 1,000,000.00 / 1,300,000.00 / 1,300,000.00 equals depreciation: True. The prose 'It removes one term from the computed figure, so each gap equals that term whenever the identity it tests holds' matches the code (the lab subtracts one term; the gap is that term).")
row("proj-l03-intangible-paragraph", "2.4-scope", "L03.html intangible-purchase paragraph (Lab 3 cases)", "PASS",
    "'Definition 2.1 of this lesson names depreciation as the add-back, and an amortization charge with no cash line would be added back in the same way, but Proposition 2.2 is not proved for it here.' Definition 1.2 gives amortization the same arithmetic; the sentence is conditional on the charge having no cash line, which Definition 1.2 states for depreciation. Arithmetic: 1,200,000.00 / 4 = 300,000.00 per year is the first year's charge (4-year life implied by the text; not a lab computation, as the text says).")
row("proj-l01-delta-prose-out-of-slice", "2.4-scope", "course/modules/AC/AC1/L01.html and L02.html changed sentences (why-it-matters, Lab 1 interpretation, Proposition 3.2 timing paragraph, exercises P2, E2 cross-reference)", "PASS",
    "Out of this slice (lesson prose belongs to the other AC1 slices). Read for the cards' sake: 'Lesson 2 uses the same identity to check the closing receivable (its exercise E2)' is supported by L02 E2 (closing receivable 515,320.87 from 9,168,896.75 - 8,653,575.88, matches the cash-flow receivables line in Lab 3, 2025). Recorded as a note, not a row of this slice.")
row("cards-no-open-r10-fail", "2.7-round10-carry", "cards.json (all round-10 FAIL rows)", "PASS",
    "Each round-10 cards FAIL is re-checked above: c027, c033, c039, c042 are now PASS; c007 is a new FAIL (cards-c007-enforced-at-posting); the L01 key-results row is still FAIL.")

# ---- mutants ---------------------------------------------------------------------------------------------------------
killed = {}
for line in (OUT / "killed_by.txt").read_text(encoding="utf-8").splitlines():
    name, _, test = line.partition("|")
    killed[name] = test
mutants = []
mdir = ROOT / "ledgers/AC1/mutants"
for path in sorted(mdir.glob("m*.py")):
    text = path.read_text(encoding="utf-8")
    m = re.match(r'"""(.*?)(?:\n\n|""")', text, re.S)
    desc = " ".join(m.group(1).split()) if m else path.stem
    desc = desc.replace("Fixer student-error mutant ", "")
    test = killed.get(path.stem, "")
    mutants.append({
        "id": path.stem.split("_")[0],
        "description": desc[:300],
        "file": f"ledgers/AC1/mutants/{path.name}",
        "killed_by": f"{test.replace('test_project.py::', '')} (seed 0); also fails on seed 17" if test else "",
    })

fragment = {
    "unit": "AC1",
    "slice": "AC1-d",
    "round": 11,
    "verifier": "Claude Haiku 5.5, independent verifier for AC1-d, round 11; did not build AC1; read the round-10 fragment as context; computed the delta af08ad1..91946cf; re-ran every command row; re-verified every round-10 non-PASS row and every changed subject",
    "pin": "91946cf (detached worktree /tmp/verify11-AC1-d)",
    "base": "af08ad1 (round 10 pin); previous ledger /tmp/fanout-frags/AC1-d.round10.json",
    "checkout": "/tmp/verify11-AC1-d",
    "scratch": str(OUT) + "/",
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "verdict": None,
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "Mutants: ledgers/AC1/mutants/ holds 75 files (m01-m75): m01-m61 and m62-m71 (added in 91946cf) and m72-m75 written this round. "
        "All 75 fail on seeds 0 and 17 (scripts/AC1-d-r11/mutants_all_r11.out). "
        "Alternatives: scripts/AC1-d-r11/alts/ (alt_r11_dict_by_account.py and alt_r11_strptime_next_day.py pass 264 on seeds 0-9; alt_r11_type_errors_for_shape.py is the type-strict witness that fails 3). "
        "Scripts: scripts/AC1-d-r11/run_suite.sh, run_mutants.sh, cards_numbers.py, build_fragment.py. "
        "Not checked: live external sources beyond verify_refs (none cited in the delta); the SEC reuse statement (no real EDGAR data in this unit); the L02 misconception item 'Proposition 3.2 is a consequence of double entry' (L02 line 436) still omits the hypotheses of Proposition 3.2 (out of slice, carried from round 10 observation); "
        "L01 line 414 exercise explain still says 'known account names' without the account-exists scope (out of slice). "
        "Round-11 numbers are not claimed beyond the cited command outputs; hours are design targets and were not failed on pace."
    ),
    "summary": None,
}
counts = {"PASS": 0, "FAIL": 0, "UNVERIFIABLE": 0}
for r in rows:
    counts[r["status"]] += 1
fragment["summary"] = {"rows": len(rows), "PASS": counts["PASS"], "FAIL": counts["FAIL"], "UNVERIFIABLE": counts["UNVERIFIABLE"], "mutants": len(mutants), "mutants_killed": sum(1 for m in mutants if m["killed_by"])}
fragment["verdict"] = "PASS" if counts["FAIL"] == 0 and counts["UNVERIFIABLE"] == 0 else "FAIL"
out = ROOT / "ledgers/AC1/AC1-d.json"
out.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("rows", len(rows), counts, "mutants", len(mutants), "verdict", fragment["verdict"])
