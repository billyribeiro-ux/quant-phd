"""Builds the round-13 AC1-d fragment: carries round-12 rows whose cited subject is byte-identical, replaces re-verified
rows with round-13 evidence, and adds the new rows and mutants. Reads the round-12 fragment (outside the checkout)."""

import json
import re

CHK = "/tmp/verify13-AC1-d"
PREV = "/tmp/fanout-frags/AC1-d.round12.json"
OUT = CHK + "/ledgers/AC1/AC1-d.json"

prev = json.load(open(PREV, encoding="utf-8"))
prev_rows = {r["id"]: r for r in prev["rows"]}

GEN = "cards.json, index.html, grader/reference.py, grader/instance.py, grader/starter.py, L04-L08.html and tests/labs/AC1 byte-identical since the previous pin aebdc15"
P368 = "project.html except line 368 byte-identical since aebdc15"

# carry prefix per row: which cited subject is byte-identical since aebdc15
CARRY = {
    "proj-hours": "project.html line 35 and the index.html hours markup byte-identical since aebdc15 (the only changed project.html line is 368)",
    "proj-page-spec-carry": "project.html line 366 byte-identical since aebdc15 (the only changed project.html line is 368)",
    "proj-line-37-lede-seed": "project.html line 37 byte-identical since aebdc15",
    "proj-footer-nothing-leaves": "project.html line 549 byte-identical since aebdc15",
    "proj-line-377-working-capital-terms": "project.html line 377 byte-identical since aebdc15",
    "proj-line-378-missing-space": "project.html lines 378-379 byte-identical since aebdc15",
    "proj-balance-gap-sign-unenforced": "project.html line 378 byte-identical since aebdc15",
    "proj-scope-sentence-line-352": "project.html line 352 byte-identical since aebdc15",
    "proj-conventions-debit-balance-sentence": "project.html line 373 byte-identical since aebdc15",
    "proj-page-lab-carry": "the project.html lab blocks (56-253, 260-343, 420-518) byte-identical since aebdc15",
    "proj-page-ladder-browser-carry": "project.html lines 40-47, 51-52, 406, 414, 533, 548 byte-identical since aebdc15",
    "proj-instances-carry": "grader/instance.py byte-identical since aebdc15",
    "cards-inventory-and-dupes": GEN,
    "cards-grades": GEN,
    "cards-banned": GEN,
    "cards-registry-cites": GEN,
    "cards-c015": "cards.json AC1-c015 and L01.html Remark 2.2 (line 103), not among the changed L01 lines (388)",
    "cards-c007-enforced-at-posting": "cards.json AC1-c007 and L01.html line 87, not among the changed L01 lines (388)",
    "cards-L01-claims-table-scope": "L01.html Key results table row (line 559), not among the changed L01 lines (388)",
    "cards-c040-investing-scope": "cards.json AC1-c040 and L03.html Proposition 3.1, not among the changed L03 line (57)",
    "cards-c124-financing-scope": "cards.json AC1-c124 and L03.html Proposition 3.1, not among the changed L03 line (57)",
    "cards-c126-straight-line": "cards.json AC1-c126 and L03.html Definition 1.2 and Remark 6.3, not among the changed L03 line (57)",
    "cards-c027-prop32-scope": "cards.json AC1-c027 and L02.html Proposition 3.2 (line 96-97), not among the changed L02 lines (133, 535, 552)",
    "cards-c028-net-income-scope": "cards.json AC1-c028 and L02.html Definition 2.1 and Proposition 2.2, not among the changed L02 lines",
    "cards-c029-prop32-hypotheses": "cards.json AC1-c029 and L02.html Proposition 3.2 (line 96-97), not among the changed L02 lines",
    "cards-c032-activity-split": "cards.json AC1-c032 and the L02.html activity-split bullet, not among the changed L02 lines (133, 535, 552)",
    "cards-c039-prop22-scope": "cards.json AC1-c039 and L03.html Proposition 2.2, not among the changed L03 line (57)",
    "cards-c042-thm51-scope": "cards.json AC1-c042 and L03.html Theorem 5.1, not among the changed L03 line (57)",
    "cards-c038-wrong-schedule": "cards.json AC1-c038 and L03.html Theorem 5.1 paragraph, not among the changed L03 line (57)",
    "cards-L03-c123": "cards.json AC1-c123 and L03.html Proposition 4.2, not among the changed L03 line (57)",
    "cards-L03-theorem-5-1-print-claim": "L03.html Theorem 5.1 paragraph (line 135) and tests/labs/AC1/lab-AC1-L03-1.py, not among the changed L03 line (57)",
    "cards-L03-theorem-5-1-print-claim-hypotheses": "L03.html Theorem 5.1 hypotheses (line 127), not among the changed L03 line (57)",
    "cards-c127-check2-not-independent": "cards.json AC1-c127 and the L03.html paragraph after Theorem 5.1, not among the changed L03 line (57)",
    "cards-c128-lab-prints-four-of-five": "cards.json AC1-c128 and the L03.html paragraph after Theorem 5.1 and Lab 3 output, not among the changed L03 line (57)",
    "cards-L04": GEN, "cards-L05": GEN, "cards-L06": GEN, "cards-L07": GEN, "cards-L08": GEN,
    "cards-c098-citation": "cards.json AC1-c098 and L07.html Theorem 2.1 and Corollary 2.2 (byte-identical lesson)",
    "cards-c102-equity-wording": "cards.json AC1-c102 and L07.html Corollary 2.2 (byte-identical lesson)",
    "cards-c109-scope": "cards.json AC1-c109 and L08.html Definition 1.2 (byte-identical lesson)",
    "cards-c008-wording": "cards.json AC1-c008 and L01.html Definition 1.3 (line 71 region), not among the changed L01 lines (388)",
    "cards-c057": GEN, "cards-c069": GEN, "cards-c071": GEN, "cards-c079": GEN, "cards-c087": GEN, "cards-c104": GEN,
    "cards-c052": GEN, "cards-c088-scope": GEN, "cards-c059-c060-c070-c090": GEN,
    "cards-c018-wording": "cards.json AC1-c018 and L02.html Definition 1.1 (line 40 region), not among the changed L02 lines",
    "cards-no-open-r10-fail": GEN,
    "proj-index-explain-prop32": "course/modules/AC/AC1/index.html line 141 byte-identical since aebdc15",
    "proj-l03-check6-prose": "L03.html Check 6 interpretation (line 669) and the Lab 3 printed labels, not among the changed L03 line (57)",
    "proj-l03-intangible-paragraph": "L03.html intangible-purchase paragraph (line 803), not among the changed L03 line (57)",
    "proj-lab-l03-comment-scope": "tests/labs/AC1/lab-AC1-L03-1.py lines 606-621 and L03.html lab block 606-621, not among the changed L03 line (57)",
    "proj-l03-check6-depreciation-reference": "L03.html interpretation paragraph (line 669), not among the changed L03 line (57)",
    "proj-l01-pytest-claim-line-415": "project.html line 415 byte-identical since aebdc15",
    "proj-pytest-version-claim": "project.html line 415 byte-identical since aebdc15",
}

# Round-13 evidence for every row whose subject changed or that is re-run in this round
NEW = {}

def row(rid, check, location, status, evidence, fix=None):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if fix:
        r["fix"] = fix
    NEW[rid] = r

row("proj-run-graders", "2.6-autograder-reference",
    "course/modules/AC/AC1/grader/ (reference.py, test_project.py, instance.py)", "PASS",
    "Re-run this round: `.venv/bin/python tools/run_graders.py --unit AC1 --seeds 0-49` -> 'run_graders AC1: PASS (reference 50/50 seeds, slowest 0.3 s)' (/tmp/v13d/run_graders.out). Each seed also run with ledgers/AC1/scripts/AC1-d-r13/run_suite.sh on grader/reference.py: '265 passed' on all 50 seeds (the grader now collects 265).")
row("proj-collect-count-176", "2.6-collect-count",
    "project.html line 368 ('collects 265 checks'); grader/test_project.py", "PASS",
    "Re-run: `run_suite.sh reference.py <dir> s collect` for seeds 0, 17 and 49: '265 tests collected' each. project.html line 368 says 265 and 'the count is 265 for each of the seeds 0 to 49'; the 50-seed run gives 265 passed for every seed, so none is collected more or fewer times.")
row("proj-local-suite-reference", "2.6-local-suite",
    "grader/test_project.py; project.html 'Running the suite locally' (line 415)", "PASS",
    "Re-run: QF_SEED=s pytest -q -p no:cacheprovider --assert=plain -W error test_project.py on reference.py: 265 passed for s in 0..49. Starter (grader/starter.py): '263 failed, 2 passed' (/tmp/v13d/st0), so the suite fails on the starter as project.html line 364 says ('the suite fails on the starter').")
row("proj-pyodide-smoke", "2.5-page-smoke", "course/modules/AC/AC1/project.html; L01.html, L02.html, L03.html", "PASS",
    "Re-run: `tools/page_smoke.py --unit AC1 --pages project.html` -> 'page_smoke AC1: PASS' (/tmp/v13d/smoke_project.out); `--pages L01.html L02.html L03.html` -> 'page_smoke AC1: PASS' (/tmp/v13d/smoke_L.out), rc=0 both.")
row("proj-check-pages", "2.9-structure", "course/modules/AC/AC1/*.html; cards.json", "PASS",
    "Re-run: `tools/check_pages.py --all` rc=0; the AC1 line reads 'check_pages AC1: PASS' (/tmp/v13d/check_pages.out).")
row("proj-check-projects", "2.9-structure", "course/modules/AC/AC1/project.html (budget, rungs)", "PASS",
    "Re-run: `tools/check_projects.py --all` rc=0; 'check_projects AC1: PASS' (/tmp/v13d/check_projects.out).")
row("proj-check-dag", "DAG", "project.html 'Concepts used here'; L01-L03 concept definitions (line 56 in L03, line 384 region in L01)", "PASS",
    "Re-run: `tools/check_dag.py --all` rc=0; 'check_dag AC1: PASS' (/tmp/v13d/check_dag.out). The delta adds no new concept use: the new L03 wording names 'Definition 1.2, below' (a definition of the same unit, in order) and the L01 parenthetical names Lesson 3, Definition 1.2 (a later lesson, cited explicitly as a forward reference).")
row("proj-run-labs", "2.5-labs", "tests/labs/AC1/lab-AC1-project-1.py, -project-2.py, -project-3.py, and the L01-L08 twins", "PASS",
    "Re-run: `tools/run_labs.py --unit AC1` -> 'run_labs AC1: PASS (11/11)'. Twins run directly under `-I -W error`: L02 (/tmp/v13d/l02.out) and L03 (/tmp/v13d/l03.out), both exit 0. The L02 run's last line is 'lowest cash balance at any year end (USD): 3,000,000.00'.")
row("proj-lab-twin-embed", "2.5-labs", "project.html lab blocks (Lab 1 56-253, Lab 2 260-343, Lab 3 420-518); L02.html and L03.html lab blocks; tests/labs/AC1", "PASS",
    "run_labs AC1 (above) checks that each page lab is byte-identical to its twin: 11/11. The delta changed prose around the L02 lab (hypothesis line 133, interpretation line 535) and not its code, and the L03 twin is unchanged; the code blocks are identical to the twins.")
row("proj-labs-ruff", "gate", "tests/labs/AC1; course/modules/AC/AC1/grader", "PASS",
    "Re-run: `.venv/bin/ruff check tests/labs/AC1 course/modules/AC/AC1/grader` -> 'All checks passed!'; `ruff format --check` -> '15 files already formatted'.")
row("proj-mypy-gate", "gate", "tests/labs/AC1; course/modules/AC/AC1/grader", "PASS",
    "Re-run: `.venv/bin/mypy --no-incremental tests/labs/AC1 course/modules/AC/AC1/grader` -> 'Success: no issues found in 15 source files'.")
row("proj-verify-refs", "2.1-citations", "references/references.json; project.html (data-cite penman2013financial)", "PASS",
    "Re-run: `tools/verify_refs.py --offline` -> 'offline integrity: 560 entries, 0 problems'; `tools/verify_refs.py --unit AC1` -> 'live re-verification of AC1: 2 of 560 entries, 0 problems'.")
row("proj-prose-banned", "1.2/1.3-banned-phrases", "project.html; cards.json; grader/test_project.py; L01-L02-L03 changed passages", "PASS",
    "Re-run: every added line of `git diff aebdc15 eaf6d87 -- course/modules/AC/AC1 tests/labs/AC1` scanned for roughly|about|historically|typically|usually|approximately|ellipsis|half|most|generally|often|tends|always. None found. Scope words in the AC1 added lines read in context: 'only' (L01 Proposition 3.2 hypotheses (i) twice, (iii), (iv) twice, which state the hypotheses; L02 'the lab checks the balance sheet only', matched by the single True flag in /tmp/v13d/l02.out; project.html line 368 and the grader case name 'an entry that balances only with another entry'); 'all four year ends' and 'each year end' (the four year-end columns and 'True' flag in the L02 output); 'never prints the expected value' (grader _check_values prints the key name only); 'all' and 'any' in the grader and L02 text are quantifiers over the stated set and are backed by the same outputs.")
row("proj-alt-implementations", "2.6-over-constraint (architect ruling b)", "course/modules/AC/AC1/grader/test_project.py (whole suite) against nine correct alternatives", "PASS",
    "Re-run this round on all nine alternatives, 50 seeds each, '265 passed' on 50/50: round-13 A alt_r13_a_date_objects_windows.py (date objects, windowed flows prev<day<=end), B alt_r13_b_sorted_lists_bisect.py (per-account sorted lists, bisect cutoffs, regex dates), C alt_r13_c_strict_types_regex.py (type(v) is int, regex dates); round-12 alt_r12_a/b/c (ledgers/AC1/scripts/AC1-d-r12/alts) and round-11 alt_r11 x3: all 50/50. Alt A failed 50/50 on a first try: my own bug (a missing key raised KeyError, not ValueError); fixed before recording.")
row("proj-overconstraint-nonmapping", "2.6-over-constraint (architect ruling b)", "grader/test_project.py test_post_raises_a_value_error parametrize list; project.html line 366", "PASS",
    "Re-verified (grader hunk 619-625 read): the added case 'an amount that is a float with a fraction of a cent' (debit 5.5) is in test_post_raises_a_value_error. Its condition is 'an amount that is not an integer, including a boolean or a float such as 100.0' (project.html line 366), so the case tests a named condition. All nine alternatives pass it.")
row("proj-mutants-set-killed", "2.5-mutation (project slice)", "ledgers/AC1/mutants/ (103 files: m01-m93 and fx01-fx10)", "PASS",
    "Re-ran the 89 m-files of round 12 (ledgers/AC1/scripts/AC1-d-r13/run_mutants.sh -> /tmp/v13d/mutants_r13.out, 89 lines): every one fails on seed 0 and on seed 17. Also fx01-fx10 (row proj-mutants-fx01-fx10) and m91-m93 (row proj-mutants-new-r13-m91-m93): all killed. The one survivor is m90 (row proj-mutant-m90-amount-cap-survives, FAIL).")
row("proj-mutants-new-r10-m58-m61", "mutants", "ledgers/AC1/mutants/ m58-m61", "PASS",
    "Re-run this round (/tmp/v13d/mutants_r13.out): m58-m61 each fail on seed 0 and seed 17.")
for rid, rng in [("proj-mutants-m01-m08", "m01-m08"), ("proj-mutants-m11-m20", "m11-m20"), ("proj-mutants-m21-m25", "m21-m25"),
                 ("proj-mutants-m33-m38", "m33-m38"), ("proj-mutants-new-m26-m28", "m26-m57"), ("proj-mutants-m62-m71-fixer", "m62-m71"),
                 ("proj-mutants-new-r11-m72-m75", "m72-m75"), ("proj-mutants-new-r9-three-written", "m45-m47")]:
    row(rid, "mutants", f"ledgers/AC1/mutants/ {rng}", "PASS",
        f"Re-run this round (/tmp/v13d/mutants_r13.out): every file in {rng} fails on seed 0 and seed 17 ('N failed' with N>0 on both lines).")
for rid, fname, label in [
    ("proj-mutant-m09-articulation-zero", "m09_articulation_zero.py", "m09"),
    ("proj-mutant-m10-depreciation-gap", "m10_depreciation_gap.py", "m10"),
    ("proj-mutant-m26-payables-sign", "m26_payables_sign.py", "m26"),
    ("proj-mutant-m27-cogs-from-balance", "m27_cogs_from_balance.py", "m27"),
    ("proj-mutant-m28-timestamp-date-accepted", "m28_timestamp_date_accepted.py", "m28"),
    ("proj-mutant-m29-boolean-credit-accepted", "m29_boolean_credit_accepted.py", "m29"),
    ("proj-mutant-m30-whitespace-date-accepted", "m30_whitespace_date_accepted.py", "m30"),
    ("proj-mutant-m31-account-name-case-folded", "m31_account_name_case_folded.py", "m31"),
    ("proj-mutant-m32-retained-gap-sign", "m32_retained_gap_sign.py", "m32"),
    ("proj-mutant-m39-account-name-whitespace-stripped", "m39_account_name_whitespace_stripped.py", "m39"),
    ("proj-mutant-m40-credit-float-accepted", "m40_credit_float_accepted.py", "m40"),
    ("proj-mutant-m41-week-date-accepted", "m41_week_date_accepted.py", "m41"),
    ("proj-mutant-m42-month-end-previous-length", "m42_month_end_previous_length.py", "m42"),
    ("proj-mutant-m43-negative-credit-absolute", "m43_negative_credit_absolute.py", "m43"),
    ("proj-mutant-m44-unbalanced-one-direction", "m44_unbalanced_one_direction.py", "m44"),
    ("proj-mutant-m45-negative-debit-clamped", "m45_negative_debit_clamped.py", "m45"),
    ("proj-mutant-m46-unpadded-date-accepted", "m46_unpadded_date_accepted.py", "m46"),
    ("proj-mutant-m47-numeric-string-amount", "m47_numeric_string_amount.py", "m47")]:
    row(rid, "mutants", f"ledgers/AC1/mutants/{fname}", "PASS",
        f"Re-run this round: {label} fails on seed 0 and seed 17 (/tmp/v13d/mutants_r13.out).")
row("proj-mutant-m89-first-day-entry-rejected", "2.5-mutation (grader survivor, round 12)",
    "ledgers/AC1/mutants/m89_post_rejects_entry_on_first_day_of_year.py; grader/test_project.py test_entries_on_the_first_and_last_days_of_the_year_post_and_count", "PASS",
    "Resolved in eaf6d87: the grader adds YEAR_EDGE_LEDGER (entries dated 2024-01-01 and 2024-12-31) and the test test_entries_on_the_first_and_last_days_of_the_year_post_and_count. Re-run this round: m89 fails on seed 0 (192 failed), seed 17 (1 failed), and on 50/50 seeds (loop over seeds 0-49 with run_suite.sh).")
row("proj-mutants-new-r12-m86-m89", "mutants", "ledgers/AC1/mutants/m86..m89", "PASS",
    "Re-run this round: m86, m87, m88 and m89 each fail on seed 0 and seed 17 (/tmp/v13d/mutants_r13.out); m89 also on 50/50 seeds (see proj-mutant-m89-first-day-entry-rejected).")
row("proj-mutant-m90-amount-cap-survives", "2.5-mutation (grader survivor, new in round 13)",
    "ledgers/AC1/mutants/m90_amount_cap_one_million_dollars.py; grader/test_project.py test_post_returns_a_ledger_that_the_functions_accept (no case with a large valid amount)", "FAIL",
    "m90 adds `if value > 100_000_000: raise ValueError` to _cents (a limit of one million dollars). It passes all 265 checks on seed 0, seed 17 and 50/50 seeds ('265 passed', /tmp/v13d/new/*). project.html line 366 says 'The named conditions are these.' and gives the list; a cap is not in the list, and the same sentence says 'Money is never converted and never adjusted: the engine reports the cents it is given' (project.html line 366). So a post that refuses a valid entry of 1,000,001 dollars violates the spec and no test catches it.",
    "Add a fixed valid case to test_post_returns_a_ledger_that_the_functions_accept with a balanced entry of a large amount (for example 10**12 cents on each side, dated 2024-03-05) and check one balance-sheet cash value; then re-run the 50-seed sweep and m90 must fail on all seeds.")
row("proj-mutants-new-r13-m91-m93", "mutants", "ledgers/AC1/mutants/m91_financing_omits_stock_issued.py, m92_operating_expenses_include_depreciation.py, m93_balance_sheet_counts_only_the_month.py", "PASS",
    "Written this round by one edit each to grader/reference.py (ledgers/AC1/scripts/AC1-d-r13/make_mutants_r13.py). Each killed: m91 '12 failed' (seed 0) and '16 failed' (seed 17); m92 '40 failed' and '70 failed'; m93 '48 failed' and '48 failed'. First failing test for m91/m92: test_small_ledger_january_cash_flow; for m93: test_entries_on_the_first_and_last_days_of_the_year_post_and_count.")
row("proj-mutants-fx01-fx10", "mutants", "ledgers/AC1/mutants/fx01..fx10 (added in eaf6d87 as the round-12 fix mutants)", "PASS",
    "Run this round on seeds 0 and 17: fx01 192/192 failed; fx02 194/194; fx03 4/4; fx04 4/4; fx05 52/55; fx06 199/199; fx07 34/40; fx08 93/93; fx09 8/8; fx10 1/1 (/tmp/v13d/fx/). fx01, fx02, fx03 and fx10 killed on 50/50 seeds (loop over seeds 0-49). Each is one student error the new tests name: year-end and leap-day entries, fraction-of-cent amounts, three-line entry.")
row("proj-alt-round13-only-own", "2.6-over-constraint (round-13 alternatives)", "ledgers/AC1/scripts/AC1-d-r13/alts/", "PASS",
    "Covered by proj-alt-implementations.")
row("proj-r13-year-edge-tests", "2.4-expected-values (new grader tests)", "grader/test_project.py test_entries_on_the_first_and_last_days_of_the_year_post_and_count and test_an_entry_dated_on_the_leap_day_posts_and_counts", "PASS",
    "Expected values recomputed by hand: 2024-01-01 entry cash 300 / common stock 300 -> balance sheet 2024-01-31 total assets 300 = total L+E 300. 2024-12-31 entry cash 50 / sales 50 -> 2024-12-31 cash 350, common stock 300, retained earnings 50, total assets 350, total equity 350; income statement sales 50, net income 50; cash flow beginning cash 300 (cash at 2024-11-30), cash from operations 50, net change 50, ending 350. Leap day: cash 4 / common stock 4 -> 2024-02-29 total assets 4. The reference passes all three checks on 50/50 seeds (265 passed), and the alternatives A-C pass.")
row("proj-r13-l01-prop32-hypothesis-v", "2.4-prose (changed hypothesis)", "course/modules/AC/AC1/L01.html line 388 (Proposition 3.2, hypothesis (v))", "PASS",
    "Re-read: hypothesis (v) now reads 'with no other non-cash expense (depreciation is one, defined in Lesson 3, Definition 1.2)'. Depreciation is defined at L03.html line 61-62 ('Definition 1.2 (depreciation, straight-line)': 'Depreciation is an expense, but it is not a payment'). The proof at L01.html line 393 has expense X = X_a + X_k with no depreciation term, so the parenthetical names the excluded non-cash expense correctly. Scope unchanged: the proof of Proposition 3.2 is on the page and is T.")
row("proj-r13-l02-lowest-cash-sentences", "2.9-prose (changed lines 133 and 535)", "course/modules/AC/AC1/L02.html lines 133 (hypothesis) and 535 (interpretation); tests/labs/AC1/lab-AC1-L02-1.py line 359", "PASS",
    "Re-run /tmp/v13d/l02.out: 'ending cash, balance sheet' 2025-2027 = 4,454,305.29 / 5,945,920.93 / 7,489,781.87, and 'net change in cash' 1,454,305.29 / 1,491,615.64 / 1,543,860.94; the 2024 cash (opening) is 3,000,000.00 since 4,454,305.29 - 1,454,305.29 = 3,000,000.00; lowest = min over the four balance sheets (lab line 359, sheets include 2024) = 3,000,000.00 = opening. Line 133 'which holds if cash rises in each year' is a condition that holds here (all three net changes are positive). Line 535: 'lowest cash balance is taken over the year ends, including the opening position, and not over the quarters ... In this run it equals the opening cash, because cash rises at each year end' is true of this run and of the code. T vs C: the figures are SIMULATED (lab-stated), grade C basis Lab 2.")
row("proj-r13-l02-intangible-cite", "2.9-prose (changed line 552)", "course/modules/AC/AC1/L02.html line 552 bullet 'The lab omits real items'", "PASS",
    "Cited 'Lesson 3, Definition 1.2' is correct: L03.html line 62 (body of Definition 1.2) says 'In this lesson, amortization applies the same arithmetic to an intangible asset with a finite life.' 'Outside the four of Definition 2.1': the four accounts are sales, cost of sales, operating expense and depreciation (card AC1-c022 and L02 line 78: 'the four of Definition 2.1'), so amortization expense is outside them. Proposition 3.2's hypotheses (L02 line 97) restrict revenue and expense accounts to the four, so the bullet's 'does not cover that case' follows. grep of tests/labs/AC1/lab-AC1-L02-1.py for tax|interest|inventory|intangible: 0 hits, so the lab omits them as the bullet says.")
row("proj-r13-l03-def11-depreciation-cite", "2.9-prose (changed line 57)", "course/modules/AC/AC1/L03.html line 57 (Definition 1.1) and line 61 (Definition 1.2)", "PASS",
    "Re-read: Definition 1.1 now reads 'adding back depreciation (Definition 1.2, below)'. Definition 1.2 is at line 61 (below line 57) and its body at line 62 defines depreciation as a non-cash charge. Definition 2.1 (line 70-71) uses the same add-back. The statement 'gives the same figure as the direct method' is Proposition 2.2 (line 75) and is proved there; no new claim.")
row("proj-l03-def11-indirect-cite", "2.9-prose (changed line 57)", "L03.html Definition 1.1 (line 57) and Definition 2.1 (line 71)", "PASS",
    "Re-verified (changed line 57; see proj-r13-l03-def11-depreciation-cite): the pointer 'Definition 1.2, below' is correct; the claim is Proposition 2.2's, proved at L03.html line 80.")
row("proj-l02-omits-real-items", "2.9-prose (changed line 552)", "course/modules/AC/AC1/L02.html line 552 (The lab omits real items)", "PASS",
    "Re-verified (changed line; see proj-r13-l02-intangible-cite): the only change is the added '(Lesson 3, Definition 1.2)' after 'An intangible asset that is amortized'; the rest of the bullet is unchanged and was checked in round 12 (no taxes, interest, inventory or intangible words in the lab: grep 0 hits this round).")
row("proj-l01-delta-prose-out-of-slice", "2.9-prose", "course/modules/AC/AC1/L01.html (line 48 why-it-matters, line 559 table row) and L02.html (line 552 bullet)", "PASS",
    "Re-verified: L01 line 48 and line 559 byte-identical since aebdc15 (see cards-L01-claims-table-scope); L02 line 552 re-verified this round (proj-r13-l02-intangible-cite). Both sentences as stated.")
row("proj-tests-labs-pytest", "2.5-labs (pytest)", "tests/test_run_labs.py, tests/test_labs.py, tests/test_page_checks.py", "PASS",
    "Re-run: `.venv/bin/pytest -q tests/test_run_labs.py tests/test_labs.py tests/test_page_checks.py -p no:cacheprovider` -> exit 0 (/tmp/v13d/pytest_labs.out).")
row("proj-page-spec-carry-post-cases", "2.6-over-constraint", "grader/test_project.py test_post_raises_a_value_error parametrize list (added cases)", "PASS",
    "Re-verified (subject changed): the added case (float with a fraction of a cent) and the existing float and boolean cases each name a condition on project.html line 366. The new test functions (year edge, leap day) check only valid postings; no case tests an unnamed shape. Alternatives A-C and the round-12 set pass 50/50.")
row("proj-no-expected-value-leak", "2.6-spec", "project.html line 368 ('A failing check names the property that failed and never prints the expected value'); grader/test_project.py _check_values", "PASS",
    "Re-verified: _check_values (test_project.py lines 224-234) fails with 'the {what} for {end} has no {key} entry', 'must be an integer number of cents', or 'does not follow the definition in the specification': the key name only, no expected or actual values. The new tests use _check_values and _check_values' messages print no values.")
row("proj-grader-carry", "2.6-grader", "grader/test_project.py (delta hunks at lines 619-625, 723-748 read in full: 39 added lines, 0 removed)", "PASS",
    "Delta read in full: one posting-error case (a float with a fraction of a cent, debit 5.5) in test_post_raises_a_value_error; the YEAR_EDGE_LEDGER constant and two tests (test_entries_on_the_first_and_last_days_of_the_year_post_and_count, test_an_entry_dated_on_the_leap_day_posts_and_counts). The rest of the file is unchanged since aebdc15 and was exercised by the 50-seed sweep. Honest limit: unchanged lines were not re-read this round (read in full in round 11). Residual FAIL: m90 (proj-mutant-m90-amount-cap-survives).")
row("proj-line-368-grading-claims", "2.9-prose", "project.html line 368 (Grading mode)", "PASS",
    "Re-verified (changed line): '265 checks' = collect count (proj-collect-count-176); 'seeds 0 to 49' = 50/50 sweep; 'warnings as errors' = run_suite.sh with -W error; the named coverage: 'an entry that balances only with another entry' (test_post_raises_a_value_error case), 'a one-cent entry' (test_a_one_cent_entry_posts_at_one_cent, line 750), 'a zero on one side of a line' (test_a_zero_on_the_debit_side_of_a_credit_line_posts, line 756), 'a repeated entry' (line 817), 'two entries on one date' (line 832), 'an empty list of transactions' (line 806), 'entries dated 1 January, 31 December and 29 February' (test_entries_on_the_first_and_last_days_of_the_year_post_and_count and test_an_entry_dated_on_the_leap_day_posts_and_counts), 'the month-end rule' (test_period_end_must_be_a_month_end, line 997), 'a hand-worked January ledger' (test_small_ledger_january_*, lines 693-710), 'the cash tie' (test_cash_flow_ends_at_the_balance_sheet_cash, line 910). Each name exists (grep this round).")
row("proj-line-37-lede-seed", "2.9-prose", "project.html line 37 and the grader panel", "PASS",
    "Carried from round 12 (project.html line 37 byte-identical since aebdc15): " + prev_rows["proj-line-37-lede-seed"]["evidence"].replace("this round", "in round 12"))
row("proj-cards-c001-c126-coverage", "2.7-cards", "course/modules/AC/AC1/cards.json (128 cards) against L01-L08", "PASS",
    "Re-run this round: card ids c001-c128 (128 cards, no duplicate ids). Labels: ledgers/AC1/scripts/AC1-d-r13/cards_labels_r13.py printed 'checked 128 cards' with no MISS line: every 'Definition/Proposition/Theorem/Corollary/Remark N.M' cited by a card's text appears in its own lesson. Numbers: cards_numbers.py output /tmp/v13d/cards_numbers.out (see cards-numbers-in-lessons).")
row("cards-numbers-in-lessons", "2.7-cards (numbers)", "cards.json; L01-L08 (tag-stripped text)", "PASS",
    "Re-run: ledgers/AC1/scripts/AC1-d-r13/cards_numbers.py -> /tmp/v13d/cards_numbers.out: 128 cards, one flagged number: AC1-c077 (L06) '5,000' is absent from the tag-stripped text, because L06.html line 68 writes it in TeX as 5{,}000 ('(L_{t-1} \\rho + 5{,}000)'); the number is the lesson's own, so PASS. The changed L01-L03 text added no card number and removed none; L02 numbers in c025/c026 re-checked against the lab output (proj-r13-cards-L02).")
row("cards-labels-resolve", "2.7-cards (labels)", "cards.json citations against each card's own lesson", "PASS",
    "Re-run: ledgers/AC1/scripts/AC1-d-r13/cards_labels_r13.py -> 'checked 128 cards', no MISS lines (every cited Definition/Proposition/Theorem/Corollary/Remark number is present in the card's lesson).")
row("cards-L01", "2.7-cards (L01)", "cards.json c001-c016 (except c007, c015); L01.html", "PASS",
    "Re-verified (L01.html line 388 changed): the cards citing Proposition 3.2 or depreciation are c013 (re-read: hypotheses (i) to (v) and the 'listed debit and credit sources' still match the page) and c003 (Definition 1.1 of L01, unchanged). The other cards cite passages not in the hunk.")
row("cards-L02", "2.7-cards (L02)", "cards.json c017-c032; L02.html", "PASS",
    "Re-verified (L02.html lines 133, 535, 552 changed): cards c017-c032 checked against the changed text; the numbers in c025 (1,003,421.14; 1,654,305.29), c026 (3,000,000.00; 4,454,305.29) match /tmp/v13d/l02.out; c027-c029 cite Proposition 3.2 and Definition 2.1 (lines 96-97, 72-78), not changed; c032 cites Definition 4.1, unchanged. No card repeats the changed sentences.")
row("cards-L03", "2.7-cards (L03)", "cards.json c033-c039, c041-c045, c123, c126, c127, c128; L03.html", "PASS",
    "Re-verified (L03.html line 57 changed): c033 re-read against the new Definition 1.1 (proj-r13 row cards-c033-definition11-scope); c034-c044 cite Definitions 1.2/2.1 and Propositions 2.2, 3.1, 4.1, 4.2, 6.2, unchanged; c037 and c044 numbers match the Lab 3 output (/tmp/v13d/l03.out: add-back 1,300,000.00 in 2026, operating 2,191,615.64; accumulated depreciation 1,000,000.00 / 2,300,000.00 / 3,600,000.00).")
row("cards-c033-definition11-scope", "2.7-cards (changed Definition 1.1)", "cards.json AC1-c033 (What is articulation?); L03.html Definition 1.1 (line 57)", "PASS",
    "Re-read: c033 says 'the change in retained earnings is net income less dividends; ... under the hypotheses of Proposition 2.2, indirect operating cash flow equals the direct figure (Definition 1.1)'. The new Definition 1.1 (L03.html line 57) lists the same identities; its depreciation add-back pointer is 'Definition 1.2, below', which c033 does not restate. Consistent.")
row("cards-c013-scope", "2.7-cards (changed L01 Proposition 3.2 line 388)", "cards.json AC1-c013 (L01); L01 Proposition 3.2 (line 388)", "PASS",
    "Re-read with the changed hypothesis (v): c013 says 'under the hypotheses (i) to (v) of Proposition 3.2 (no write-offs, returns or allowances, and the listed debit and credit sources)'. The card does not restate (v); the sentence 'Proposition 3.2 holds for any opening balances' matches L01.html line 396. Consistent.")
row("cards-c018-wording", "2.7-cards", "cards.json AC1-c018 (L02); L02 Definition 1.1", "PASS",
    "Carried from round 12 (cards.json and the L02 definition not in the changed lines 133, 535, 552): " + prev_rows["cards-c018-wording"]["evidence"].replace("this round", "in round 12"))
row("cards-no-open-r10-fail", "2.7-cards (carry)", "cards.json (all round-10 and round-11 FAIL rows)", "PASS",
    "Carried from round 12 (cards.json byte-identical since aebdc15): " + prev_rows["cards-no-open-r10-fail"]["evidence"].replace("this round", "in round 12"))
row("proj-index-explain-prop32-carry-check", "2.9-prose", "course/modules/AC/AC1/index.html line 141", "PASS",
    "Covered by proj-index-explain-prop32 (index.html byte-identical since aebdc15).")
row("proj-starter-fails", "2.6-starter", "grader/starter.py; project.html line 364", "PASS",
    "Run: run_suite.sh grader/starter.py seed 0 -> '263 failed, 2 passed'. project.html line 364 says 'every function raises NotImplementedError until you replace it, and the suite fails on the starter'. Consistent.")
row("proj-r13-cards-L02", "2.7-cards (numbers from changed L02 lines)", "cards.json AC1-c025, AC1-c026; L02.html lab output", "PASS",
    "Re-checked: c025 '1,003,421.14' (net income 2025) and '1,654,305.29' (operating cash flow 2025) = lab output lines 'net_income 1,003,421.14' and 'subtotal, operating 1,654,305.29' (/tmp/v13d/l02.out); c026 '3,000,000.00' and '4,454,305.29' = 'cash' 2024 and 'ending cash, balance sheet' 2025 (same file).")

# rows that stay as carried from round 12 (their cited subject is byte-identical) get the carry prefix
out_rows = []
for r in prev["rows"]:
    rid = r["id"]
    if rid in NEW:
        out_rows.append(NEW.pop(rid))
        continue
    if rid in CARRY:
        ev = "Carried from round 12 (" + CARRY[rid] + "): " + r["evidence"].replace("this round", "in round 12")
        out_rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": r["status"], "evidence": ev})
        continue
    raise SystemExit(f"row {rid} has no round-13 decision")
# new rows that did not exist in round 12
for rid, r in NEW.items():
    if rid in ("proj-alt-round13-only-own", "proj-index-explain-prop32-carry-check"):
        continue
    out_rows.append(r)

ids = [r["id"] for r in out_rows]
assert len(ids) == len(set(ids)), "duplicate ids"
missing = [rid for rid in prev_rows if rid not in ids]
print("previous ids missing:", missing)

mut_prev = prev["mutants"]
mutants = []
for m in mut_prev:
    mutants.append({"id": m["id"], "description": m["description"], "file": m["file"],
                    "killed_by": "seed 0 and seed 17 (round-13 sweep, /tmp/v13d/mutants_r13.out)" if m["id"] != "m89"
                    else "seed 0 (192 failed), seed 17 (1 failed), 50/50 seeds after the eaf6d87 grader"})
new_m = [
    ("m90", "Round-13 student-error mutant m90: post refuses any single amount above one million dollars (100000000 cents), a limit the specification does not name.",
     "ledgers/AC1/mutants/m90_amount_cap_one_million_dollars.py", "SURVIVES: passes 265 checks on seeds 0, 17 and 50/50 seeds (FAIL row proj-mutant-m90-amount-cap-survives)"),
    ("m91", "Round-13 student-error mutant m91: cash_from_financing leaves out stock issued.",
     "ledgers/AC1/mutants/m91_financing_omits_stock_issued.py", "seed 0 (12 failed), seed 17 (16 failed)"),
    ("m92", "Round-13 student-error mutant m92: operating_expenses reported with depreciation added in.",
     "ledgers/AC1/mutants/m92_operating_expenses_include_depreciation.py", "seed 0 (40 failed), seed 17 (70 failed)"),
    ("m93", "Round-13 student-error mutant m93: balance_sheet sums only the entries dated in the month of period_end.",
     "ledgers/AC1/mutants/m93_balance_sheet_counts_only_the_month.py", "seed 0 (48 failed), seed 17 (48 failed)"),
]
for mid, desc, f, kb in new_m:
    mutants.append({"id": mid, "description": desc, "file": f, "killed_by": kb})
for fx in ["fx01_year_end_entry_rejected", "fx02_leap_day_entry_rejected", "fx03_fraction_of_cent_truncated",
           "fx04_leap_february_month_end_day_28_accepted", "fx05_previous_month_end_two_days_back",
           "fx06_second_entry_on_a_date_rejected", "fx07_cost_of_goods_sold_negative_in_income",
           "fx08_beginning_cash_one_day_early", "fx09_balance_sheet_accepts_any_day", "fx10_three_line_entry_rejected"]:
    mutants.append({"id": fx.split("_")[0], "description": "Round-12 fix mutant " + fx.split("_", 1)[1].replace("_", " ") + " (eaf6d87).",
                    "file": "ledgers/AC1/mutants/" + fx + ".py", "killed_by": "seed 0 and seed 17 (/tmp/v13d/fx/)"})

total = len(out_rows)
fails = [r for r in out_rows if r["status"] != "PASS"]
passes = total - len(fails)
frag = {
    "unit": "AC1",
    "slice": "AC1-d",
    "round": 13,
    "verifier": "Claude Haiku 5.5, independent verifier for AC1-d, round 13; did not build AC1; read the round-12 fragment as context and computed the delta aebdc15..eaf6d87 on the AC1 files (L01, L02, L03, project.html, grader/test_project.py, mutants)",
    "pin": "eaf6d87 (detached worktree /tmp/verify13-AC1-d)",
    "base": "aebdc15 (round 12 pin); previous fragment /tmp/fanout-frags/AC1-d.round12.json",
    "checkout": "/tmp/verify13-AC1-d",
    "scratch": "/tmp/v13d/",
    "verified_at": "2026-10-28T13:00:00+00:00",
    "rows": out_rows,
    "verdict": "FAIL" if fails else "PASS",
    "summary": {"rows": total, "PASS": passes, "FAIL": len(fails), "UNVERIFIABLE": 0,
                "mutants": len(mutants), "mutants_killed_seed0_and_seed17": len(mutants) - 1},
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": ("Delta aebdc15..eaf6d87 on AC1: L01.html line 388 (Proposition 3.2 hypothesis (v) parenthetical); "
              "L02.html lines 133, 535, 552 (hypothesis, interpretation, bullet); L03.html line 57 (Definition 1.1 pointer); "
              "project.html line 368 (count 265 and coverage list); grader/test_project.py (one float case, YEAR_EDGE_LEDGER, "
              "two tests); ledgers/AC1/mutants fx01-fx10 added. Not changed in the delta and carried: cards.json, index.html, "
              "grader/reference.py, grader/instance.py, grader/starter.py, L04-L08.html, tests/labs/AC1. "
              "Not checked: real EDGAR data (none in this unit); the unchanged ~960 lines of test_project.py were not re-read this round."),
}
json.dump(frag, open(OUT, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("rows", total, "PASS", passes, "FAIL", len(fails), "mutants", len(mutants), "verdict", frag["verdict"])
