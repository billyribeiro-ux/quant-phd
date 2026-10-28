"""Builds ledgers/AC1/AC1-d.json (round 7) from the evidence gathered in this round. Row ids of round 6 are kept."""

import json
import pathlib
import re

CHK = pathlib.Path("/tmp/verify7-AC1-d")
RUN = pathlib.Path("/tmp/AC1-v7/AC1-d")
PREV = json.loads(pathlib.Path("/tmp/fanout-frags/AC1-d.round6.json").read_text(encoding="utf-8"))
def CARRY_OF(files):
    return f"Carried from round 6 ({files} byte-identical since the previous pin d57df1e):"


CARRY = CARRY_OF("project.html line 352")

R = "Re-verified round 7: "
rows = []


def row(rid, check, location, status, evidence, fix=None):
    item = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        item["fix"] = fix or "see evidence"
    rows.append(item)


# --- command rows (re-run this round) ---
row("proj-run-graders", "2.6-autograder-reference", "course/modules/AC/AC1/grader/ (reference.py, instance.py, test_project.py)", "PASS",
    R + "tools/run_graders.py --unit AC1 --seeds 0-49 -> 'run_graders AC1: PASS (reference 50/50 seeds, slowest 0.3 s)' (" + str(RUN / "run_graders.out") + "). Direct run of ledgers/AC1/scripts/AC1-d-r7/run_suite.sh on reference.py seed 0: 180 passed.")
row("proj-collect-count-176", "2.6-spec-test-count", "project.html line 368 ('collects 180 checks'); grader/test_project.py", "PASS",
    R + "pytest --collect-only (run_suite.sh ... collect) on reference.py for seeds 0-49: '180 tests collected' for all 50 seeds (uniq count 50 x 180). Matches the page's 180 and 'the count is 180 for each of the seeds 0 to 49'.")
row("proj-local-suite-reference", "2.6-autograder-local-run", "grader/test_project.py; project.html line 413 local command", "PASS",
    R + "The line-413 flags (-q -p no:cacheprovider --assert=plain -W error) run with QF_SEED set: reference.py 180 passed. Starter: 178 failed, 2 passed (ledgers/AC1/scripts/AC1-d-r7/run_suite.sh).")
row("proj-pyodide-smoke", "2.6-autograder-pyodide", "course/modules/AC/AC1/project.html (labs 1-3, grader panel)", "PASS",
    R + "tools/page_smoke.py --unit AC1 --pages project -> 'in-browser grader: All 180 tests pass on seed 2353908'; labs lab-AC1-project-1/2/3 run; 'page_smoke AC1: PASS' (" + str(RUN / "page_smoke.out") + ").")
row("proj-check-pages", "2.9-structure", "course/modules/AC/AC1/*.html; cards.json", "PASS", R + "tools/check_pages.py --all -> 'check_pages AC1: PASS', exit 0.")
row("proj-check-projects", "2.6-hours-and-structure", "course/modules/AC/AC1/project.html (budget, rungs)", "PASS", R + "tools/check_projects.py --all -> 'check_projects AC1: PASS', exit 0.")
row("proj-check-dag", "2.9-dag-concepts", "project.html 'Concepts used here' (line 379, byte-identical)", "PASS", R + "tools/check_dag.py --all -> 'check_dag AC1: PASS', exit 0.")
row("proj-run-labs", "2.5-labs", "tests/labs/AC1/lab-AC1-project-1.py, -project-2.py, -project-3.py", "PASS",
    R + "tools/run_labs.py --unit AC1 -> 'run_labs AC1: PASS (11/11)'. ledgers/AC1/scripts/AC1-d-r7/check_lab_embeds.py: Lab 1 and Lab 3 embedded code equals the twin and prints the page's expected block; Lab 2 page code is the template with four blanks, and its twin, run alone with python -I -W error, prints the expected block (exit 0).")
row("proj-lab-twin-embed", "2.5-lab-embed-equals-twin", "project.html lab blocks 56-253, 260-343, 420-518; tests/labs/AC1/lab-AC1-project-*.py", "PASS",
    R + "check_lab_embeds.py: lab-AC1-project-1 embedded==twin True, stdout==page expected True; lab-AC1-project-3 same; lab-AC1-project-2 differs from its twin only in the four blanks (diff: ending_cash, cash_gap, retained_change, earnings_gap), and the twin's stdout equals the expected block.")
row("proj-labs-ruff", "gate-ruff", "tests/labs/AC1; course/modules/AC/AC1/grader", "PASS", R + "ruff check course/modules/AC/AC1 tests/labs/AC1 -> 'All checks passed!'; ruff format --check -> '15 files already formatted'.")
row("proj-mypy-gate", "gate-mypy", "tests/labs/AC1; course/modules/AC/AC1/grader", "PASS", R + "mypy --no-incremental (repo) -> 'Success: no issues found in 153 source files', exit 0.")
row("proj-verify-refs", "2.1-citations-tool", "references/references.json; project.html line 533 (data-cite penman2013financial)", "PASS",
    R + "verify_refs.py --offline -> 'offline integrity: 560 entries, 0 problems'; verify_refs.py --unit AC1 -> 'live re-verification of AC1: 2 of 560 entries, 0 problems'. The key penman2013financial is in references.json (line 18942). The page attaches no quoted number to it.")
row("proj-hours", "2.6-hours", "project.html line 35 and time-budget rows (lines 389-398); index.html data-hours-lessons; L01-L08 study hours", "PASS",
    R + "Time-budget rows 1+3+4+4+3+5+2+5+3 = 30 = line 398 total = line 35. Hub data-hours-lessons 90 = declared lesson hours 11+12+11+11+12+12+11+10 = 90; 90 + 30 = 120. Pace estimates not failed (architect ruling: hours are design targets).")
row("proj-prose-banned", "2.9-banned-phrases", "project.html; cards.json", "PASS",
    R + "grep -i -E for roughly half, about 6%, historically, typically, usually, generally, ellipsis, builder, verifier, round N, unit report, request, TODO, FIXME on project.html and cards.json: no hits. The two prose defects of this round are separate rows.")
row("proj-alt-implementations", "2.6-grader alternatives (ruling b)", "course/modules/AC/AC1/grader/test_project.py (whole suite)", "PASS",
    R + "Three genuinely different correct solutions, ledgers/AC1/scripts/AC1-d-r7/alternatives/: alt_a_prefix_sums.py (bisect prefix sums over sorted postings, regex-validated dates), alt_b_window_sums.py (signed posting list, flows as direct window sums, class-based validation), alt_c_per_account.py (per-account lists, date-arithmetic month ends). Each: 180 passed for every seed 0-49 (run_suite.sh).")
row("proj-overconstraint-nonmapping", "2.6-over-constraint (ruling b)", "grader/test_project.py (new cases at lines 316, 379-402)", "PASS",
    R + "All three alternatives pass the new cases. The new cases each reject an input the page's spec names: padded date ' 2024-01-02 ' (form YYYY-MM-DD), account 'Cash' (outside the chart, whose keys are lower-case), boolean True on the credit side (not an integer). No alternative correct solution fails.")
row("proj-mutants-m01-m08", "2.6-mutation (round 2-3 set)", "ledgers/AC1/mutants/m01 to m08", "PASS", R + "run_mutants.sh over the full set: all killed (first failure per mutant in " + str(RUN / "mutants_r7_run1.out") + ").")
row("proj-mutant-m09-articulation-zero", "2.6-mutation", "ledgers/AC1/mutants/m09_articulation_all_zero.py", "PASS", R + "killed: test_articulation_gaps_report_a_ledger_that_does_not_articulate (seed 0).")
row("proj-mutant-m10-depreciation-gap", "2.6-mutation", "ledgers/AC1/mutants/m10_depreciation_gap_no_expense.py", "PASS", R + "killed: test_small_ledger_january_articulation_is_zero (seed 0).")
row("proj-mutants-m11-m20", "2.6-mutation (round 2-3 set)", "ledgers/AC1/mutants/m11 to m20", "PASS", R + "all killed on seed 0 (run_mutants.sh).")
row("proj-mutants-m21-m25", "2.6-mutation (round 4 set)", "ledgers/AC1/mutants/m21 to m25", "PASS", R + "all killed on seed 0 (run_mutants.sh).")
row("proj-mutant-m26-payables-sign", "2.6-mutation (round 5 student error, re-run)", "ledgers/AC1/mutants/m26_payables_increase_sign_reversed.py", "PASS", R + "killed: test_small_ledger_january_cash_flow (seed 0); 50 failures in the full run.")
row("proj-mutant-m27-cogs-from-balance", "2.6-mutation (round 5 student error, re-run)", "ledgers/AC1/mutants/m27_cogs_from_balance_not_flow.py", "PASS",
    R + "Round 6 killed it only with a NameError: income_statement read an undefined name 'now', so the kill did not test the described error. Repaired (ledgers/AC1/scripts/AC1-d-r7/repair_m23_m27.py: the unpacking now binds now). Now killed by 48 genuine failures, first test_income_statement_matches_the_ledger[2024-05-31] (seed 0). m23 repaired the same way (66 genuine failures).")
row("proj-mutant-m28-timestamp-date-accepted", "2.6-mutation (round 5 FAIL, now killed)", "ledgers/AC1/mutants/m28_timestamp_truncated_accepted.py; grader/test_project.py", "PASS",
    R + "killed: test_post_raises_a_value_error[a date with a time of day] (seed 0).")
row("proj-mutants-set-killed", "2.6-mutation (set, 41 mutants)", "ledgers/AC1/mutants/ (41 files)", "FAIL",
    R + "run_mutants.sh (seeds 0-4) and tools/mutate_graders.py --unit AC1 --seeds 0-9 -> 'mutate_graders AC1: FAIL (38/41 killed)' (" + str(RUN / "mutate_gate.out") + "). Survivors: m39_account_name_whitespace_stripped, m40_credit_float_accepted, m41_week_date_accepted (rows below).",
    "Add the three cases named in the survivor rows to grader/test_project.py (the grader is not edited by this verifier).")
row("proj-mutants-new-m26-m28", "2.6-mutation (ruling g, at least three new)", "ledgers/AC1/mutants/m26, m27, m28 (round 5); m29-m32 (round 6); m33-m41 (round 7)", "PASS",
    R + "Nine new student-error mutants are in the set: m33-m38 (round 7, killed) and m39-m41 (round 7, survived, FAIL rows).")
row("proj-mutant-m29-boolean-credit-accepted", "2.6-mutation (round 6 FAIL, now killed)", "ledgers/AC1/mutants/m29_boolean_credit_accepted.py; grader/test_project.py lines 391-402", "PASS",
    R + "killed by test_post_raises_a_value_error[an amount that is a boolean on the credit side] (seed 0; the case added this round).")
row("proj-mutant-m30-whitespace-date-accepted", "2.6-mutation (round 6 FAIL, now killed)", "ledgers/AC1/mutants/m30_whitespace_date_accepted.py; grader/test_project.py line 316", "PASS",
    R + "killed by test_post_raises_a_value_error[a date with surrounding spaces] (seed 0; the case added this round).")
row("proj-mutant-m31-account-name-case-folded", "2.6-mutation (round 6 FAIL, now killed)", "ledgers/AC1/mutants/m31_account_name_case_folded.py; grader/test_project.py lines 379-390", "PASS",
    R + "killed by test_post_raises_a_value_error[an account name in capitals] (seed 0; the case added this round).")
row("proj-mutant-m32-retained-gap-sign", "2.6-mutation (round 6 student error)", "ledgers/AC1/mutants/m32_retained_gap_dividends_added.py", "PASS", R + "killed: test_small_ledger_january_articulation_is_zero (5 failures, seed 0).")
row("proj-mutants-m33-m38", "2.6-mutation (NEW round 7, six student errors)", "ledgers/AC1/mutants/m33 to m38 (generated by ledgers/AC1/scripts/AC1-d-r7/make_new_mutants.py from grader/reference.py, one line each)", "PASS",
    R + "m33 total liabilities omits long-term debt -> test_balance_sheet_matches_the_ledger[2024-06-30]; m34 net income omits depreciation -> test_cash_flow_ends_at_the_balance_sheet_cash[2024-09-30]; m35 working capital from balance not change -> test_net_change_in_cash_equals_the_cash_lines_of_the_month[2024-02-29]; m36 beginning cash equals period-end cash -> test_cash_flow_ends_at_the_balance_sheet_cash[2024-01-31]; m37 depreciation gap from net equipment -> test_small_ledger_january_articulation_is_zero; m38 balance gap ignores equity -> test_small_ledger_january_articulation_is_zero. All six killed on seed 0.")
row("proj-mutant-m39-account-name-whitespace-stripped", "2.6-mutation (NEW round 7, student error; spec-named condition)", "ledgers/AC1/mutants/m39_account_name_whitespace_stripped.py; grader/test_project.py lines 331-342, 379-390", "FAIL",
    R + "SURVIVED seeds 0-4 (run_mutants.sh; mutate_graders seeds 0-9). Witness (witness_survivors.py): post([{'date':'2024-01-02','lines':[{'account':' cash ','debit':5,'credit':0},{'account':'common_stock','debit':0,'credit':5}]}]) is accepted; the reference raises ValueError. The suite has no account case with surrounding spaces. Spec line 366 names 'an account outside the chart'; ' cash ' is not a key of ACCOUNTS.",
    "Add a case with an account name ' cash ' (padded) to the post parametrize list in grader/test_project.py.")
row("proj-mutant-m40-credit-float-accepted", "2.6-mutation (NEW round 7, student error; spec-named condition)", "ledgers/AC1/mutants/m40_credit_float_accepted.py; grader/test_project.py lines 355-366 (the only float case is on the debit side)", "FAIL",
    R + "SURVIVED seeds 0-4. Witness: post with credit 5.0 on the second line is accepted (reference: ValueError 'an amount must be an integer number of cents'). The only float case, 'an amount that is not an integer', has debit 5.0. Spec line 366: 'an amount that is not an integer, including a boolean or a float such as 100.0' is not enforced on the credit side.",
    "Add a float case on the credit side (credit 5.0) to the post parametrize list in grader/test_project.py.")
row("proj-mutant-m41-week-date-accepted", "2.6-mutation (NEW round 7, student error; spec-named condition)", "ledgers/AC1/mutants/m41_week_date_accepted.py; grader/test_project.py lines 311-315", "FAIL",
    R + "SURVIVED seeds 0-4. Witness: date '2024-W01-1' (ten characters; Python 3.14 date.fromisoformat returns 2024-01-01) is accepted when the round-trip check is removed (reference: ValueError). Spec line 366: 'a date that is not in the form YYYY-MM-DD'; no suite case uses a week date.",
    "Add a post case with date '2024-W01-1' to grader/test_project.py.")
row("proj-balance-gap-sign-unenforced", "2.6-spec-claim not enforceable (ruling a); equivalent-mutant proof", "project.html line 378 (Conventions, Articulation gaps: 'balance_gap is total assets less total liabilities and equity')", "FAIL",
    R + "Round 6 FAIL stands in substance. The new sentence states that balance_gap is zero for every accepted ledger and that the suite checks zero: both are true (balance_gap_witness.py: 720 month-end values over 60 random balanced ledgers, max |balance_gap| = 0; test_articulation_gaps_are_zero and test_small_ledger_january_articulation_is_zero check it). But the sentence still defines the gap by its sign, and no test can detect a sign reversal (equivalent mutant: the sum of signed balances of all 13 accounts is zero by construction of post). Ruling (a) forbids claiming a sign the tests cannot enforce.",
    "Keep the zero result and the check; state that the sign of this always-zero quantity is not tested, or drop the sign convention for balance_gap.")
row("proj-scope-sentence-line-352", "2.9-prose (claim about the ledgers)", "course/modules/AC/AC1/project.html line 352 (Context)", "PASS",
    CARRY + " the labs' ledgers are written out by hand in the lab code; autograder ledger from make_instance (instance.py, label SIMULATED, 200 transactions per seed); the Lab 1-3 ledgers carry the SIMULATED comment (round 6 evidence, re-read this round).")
row("proj-conventions-debit-balance-sentence", "2.9-prose (line 373, changed this round)", "course/modules/AC/AC1/project.html line 373 (Conventions, Balance through a date)", "PASS",
    R + "'Assets other than accumulated depreciation have a normal debit balance, and so do dividends and expenses. The other classes, accumulated depreciation included, have credit balances': matches the starter's classes (asset, distribution, expense debit-normal; contra_asset, liability, equity, revenue credit-normal) and the statements' positive-amount convention.")
row("proj-page-spec-carry", "2.6-spec-named-errors and spec-unenforced", "project.html lines 366, 368, 391-393; grader/test_project.py lines 307-430 (post cases)", "FAIL",
    R + "Each named condition has a case (nine conditions, 21 post cases). The three generic-form gaps of round 6 are closed (boolean on the credit side, padded date, capitalised account: m29-m31 killed). The generic wording of line 366 still outruns the suite in three places: a float on the credit side (m40 survives), a padded account name (m39 survives), and an ISO week date (m41 survives). Line 391's 'each has a test' is literally true of the nine conditions as parametrised.",
    "Add the cases listed in rows proj-mutant-m39, -m40, -m41.")
row("proj-page-lab-carry", "2.5-labs (carry, re-run)", "project.html lines 56-253 (Lab 1), 260-343 (Lab 2), 420-518 (Lab 3); tests/labs/AC1/", "PASS",
    R + "Labs re-run (run_labs AC1 11/11; check_lab_embeds.py). Lab 1 predicted and printed values match (22 postings, balance gaps 0, February net income 700,000, operating -700,000, ending cash 4,800,000). Lab 3 values recomputed by hand: retained earnings -380,000 = 70,000 - 450,000; financing 850,000 = 1,000,000 - 150,000; ending cash 4,850,000.")
row("proj-page-ladder-browser-carry", "2.6-ladder and browser claims (carry)", "project.html lines 40-47, 51-52, 406, 414, 533, 548", "PASS",
    CARRY_OF("project.html lines 40-47, 51-52, 406, 414, 533, 548") + " re-read this round: line 414 pytest 9.0 and Python 3.14 match vendor LOCK (pytest@9.0.2, pyodide 314.0.7) and the local interpreter (3.14.8, pytest 9.0.2); py-worker runs --assert=plain -W error; line 548 'nothing you write leaves it': store.js keeps learner state in IndexedDB, and grader.js fetches only the grader files.")
row("proj-instances-carry", "2.6-instances (validity, labels, 2024 dates) (carry)", "course/modules/AC/AC1/grader/instance.py", "PASS",
    CARRY_OF("grader/instance.py") + " instance.py is the same file. Re-run: balance_gap_witness.py reads seeds 0-49: 10,000 transactions, all dated 2024-, label SIMULATED.")
row("proj-grader-carry", "2.6-grader tests (re-verified, not carried)", "grader/test_project.py (whole file, 661 lines)", "PASS",
    R + "Read in full. must_raise checks the exception type; _check_values and the articulation messages name the property and never print the expected value (failure output for m01: 'the cash flow statement for 2024-01-31: cash_from_operations does not follow the definition'). Oracle independent of statements.py. SMALL ledger values recomputed (balances 560/300/80/400/50/350/1290; cash flow 130/50/-300/-80/200 -> CFO 0; ending cash 560). GAP_WITNESS (cash_gap -100, depreciation_gap -100) recomputed. Stdlib-only imports.")
row("proj-line-368-grading-claims", "2.6-grading-mode claims (line 368, round-7 wording)", "project.html line 368; grader/test_project.py", "PASS",
    R + "'collects 180 checks' and 'the count is 180 for each of the seeds 0 to 49' (run_suite.sh collect, 50 seeds). The coverage list maps to tests: chart (test_chart_of_accounts), imports (test_the_module_imports_only_the_standard_library), posting and named errors (test_post_raises_a_value_error), silence (test_the_functions_are_silent), twelve month ends (MONTH_ENDS parametrisations), balance identity (test_the_balance_sheet_balances), cash tie (test_cash_flow_ends_at_the_balance_sheet_cash), net change in cash (test_net_change_in_cash_equals_the_cash_lines_of_the_month), retained earnings (test_retained_earnings_move_by_net_income_less_dividends), operating cash flow formula (test_operating_cash_flow_is_net_income_plus_add_backs_and_working_capital), four gaps (test_articulation_gaps_are_zero and GAP_WITNESS test), month-end rule (test_period_end_must_be_a_month_end), hand-worked ledger (SMALL tests). 'A failing check ... never prints the expected value': confirmed in _check_values and must_raise.")
row("proj-line-37-lede-seed", "2.9-prose (line 37, byte-identical)", "course/modules/AC/AC1/project.html line 37 (lede) and the panel at line 407; local command at line 413", "PASS",
    R + "200-transaction ledger per seed (10,000 over seeds 0-49). The seed is shown in the panel (grader.js line 53: 'Your instance seed is ${seed}').")
row("cards-inventory-and-dupes", "2.7-cards (inventory, duplicates)", "course/modules/AC/AC1/cards.json (125 cards)", "PASS",
    R + "125 cards, ids AC1-c001 to AC1-c125 contiguous and unique; no duplicate front or back text (script).")
row("cards-grades", "2.7-cards (grades and basis)", "cards.json grade and basis fields", "PASS",
    R + "Grades: 41 C, 41 T, 43 without a grade (definition cards). Every card whose answer reads a lab number carries grade C with basis naming the lab (c056, c059, c060, c070, c072, c073, c086, c088, c089, c090, c099, c100, c116, c117; c051 and c050 'convention of Lab 1'). Proved identities are T (c052, c058, c097, c098, c102, c104, c112-c115, c121, c125).")
row("cards-numbers-in-lessons", "2.7-cards (every number in its lesson)", "cards.json; course/modules/AC/AC1/L01.html to L08.html (tag-stripped text)", "PASS",
    R + "ledgers/AC1/scripts/AC1-d-r7/cards_numbers.py: every number on each card of L04-L08 appears in its lesson text, except that c077's 5,000 is written 5{,}000 in L06 (the same number, KaTeX notation). Lab values (c086, c088, c089, c090) match run of lab-AC1-L06-1.py.")
row("cards-labels-resolve", "2.7-cards (cited labels exist)", "cards.json citations against each card's own lesson", "PASS",
    R + "Every cited label on the L04-L08 cards read in the current lesson text (for example c069 -> P3 in L05, c057 -> Remark 1.2 and Section 4 of L04, c121 -> Theorem 2.1 (b) of L08).")
row("cards-banned", "2.9-banned-phrases (cards)", "cards.json", "PASS", R + "grep on cards.json: no banned phrase, no process word, no ellipsis.")
row("cards-registry-cites", "2.1-citations (cards)", "cards.json", "PASS", R + "cards.json contains no data-cite and no registry key; citations are lesson labels only.")
row("cards-c015", "2.7-cards (card versus passage) (carry)", "cards.json AC1-c015; L01 Remark 2.2 and Definition 1.1", "PASS", CARRY_OF("L01.html and the c015 card line") + " the lesson text and this card are the same.")
row("cards-L01", "2.7-cards (lesson 1) (carry)", "cards.json c001-c016; course/modules/AC/AC1/L01.html", "PASS", CARRY_OF("L01.html and cards c001-c016") + " the same lesson and cards.")
row("cards-L01-claims-table-scope", "2.9-lesson claim (round-5 FAIL re-verified in round 6) (carry)", "course/modules/AC/AC1/L01.html Key results table", "PASS", CARRY_OF("L01.html") + " the round-6 PASS stands.")
row("cards-L02", "2.7-cards (lesson 2) (carry)", "cards.json c017-c032; L02.html", "PASS", CARRY_OF("L02.html and cards c017-c032") + " the same lesson and cards.")
row("cards-L03", "2.7-cards (lesson 3, c033-c045 and c124) (carry)", "cards.json c033-c045, c124; L03.html", "PASS", CARRY_OF("L03.html and cards c033-c045, c124") + " The c123 card is a separate row.")
row("cards-L03-c123", "2.7-cards (c123 against Proposition 4.2, re-verified)", "cards.json AC1-c123 (grade T); L03.html Proposition 4.2 and its proof", "FAIL",
    R + "L03.html byte-identical; Proposition 4.2 still says 'in a ledger with no disposals, meaning no entry that credits equipment at cost'. Its proof says the net equipment change is additions less the depreciation credit and ignores debits to accumulated depreciation, which the hypothesis does not exclude. Counterexample: buy equipment 1,000,000 for cash; post depreciation 300,000 (Dr depreciation expense, Cr accumulated depreciation); post Dr accumulated depreciation 100,000 / Cr cash 100,000. Net equipment at year end = 1,000,000 - (300,000 - 100,000) = 800,000; the stated right side gives 1,000,000 - 300,000 = 700,000. Card graded T repeats it.",
    "State the hypothesis as no debit and no credit to equipment or accumulated depreciation other than depreciation, or correct the proof and the card.")
row("cards-L03-theorem-5-1-print-claim", "2.9-lesson claim about printed output (round-5 FAIL re-verified)", "course/modules/AC/AC1/L03.html Theorem 5.1 paragraph ('the checks print True')", "FAIL",
    R + "L03.html byte-identical. The paragraph says the checks print True, including 'Check 1 tests the balance sheet'. Run of tests/labs/AC1/lab-AC1-L03-1.py (labout_L03.txt, exit 0): Check 1 prints 'assets less liabilities and equity = 0.00' at each year end, not True.",
    "Say that Check 1 prints the gap, 0.00 at each year end, and that the other checks print True.")
row("cards-L04", "2.7-cards (lesson 4) (re-verified)", "cards.json c046-c060, c122; L04.html (changed Remark 1.2, Section 2 and Lab 1 text)", "PASS",
    R + "All 16 cards read against the current L04 text and the run of lab-AC1-L04-1.py (seed 2604). c059's purchases checked by probe (l04_prepaid_probe.py): quarter 1 4,886,040; quarter 3 4,233,446; quarter 4 6,325,624; quarter 7 6,632,381; expense 1,658,095 + 1,581,406 at quarter 7; unexpired 4,974,286. c122 matches Definition 2.2 and the Proposition 2.2 proof. c057 matches Remark 1.2 and Section 4.")
row("cards-L05", "2.7-cards (lesson 5) (re-verified)", "cards.json c061-c074; L05.html (changed Definition 1.3 and Section 2 text)", "PASS",
    R + "Each card read against current L05 text and run of lab-AC1-L05-1.py: peak 32,792,272; asset 23,333,398 in 8 months; totals 80,495,111; month-6 difference 20,583,168 (equal to the over-time schedule sums 2,717,022 + 17,866,146). c069 matches the paragraph before Lab 1 and problem P3.")
row("cards-L06", "2.7-cards (lesson 6) (re-verified)", "cards.json c075-c090; L06.html (changed Remark 2.5 and Section 3 text)", "PASS",
    R + "Each card read against current L06 text and run of lab-AC1-L06-1.py: year-1 expense 14,820,224 (c088); year-1 difference 1,785,952 and year-7 difference -1,977,098 (c086); asset 61,708,083 and liability 63,494,035 after year 1 (c089); final payment 13,034,273 vs 13,034,272 (c090). The lesson's new Remark 2.5 numbers (amortization 10,284,680, 10,284,683; smallest interest fall 535,420) are printed by the lab; no card cites them.")
row("cards-L07", "2.7-cards (lesson 7) (re-verified)", "cards.json c091-c104; L07.html (changed Definition 1.2, Corollary 2.2 and Lab text)", "PASS",
    R + "Each card read against current L07 text and run of lab-AC1-L07-1.py (seed 20260701): 4/4 schedules, 6/6 years for each identity (c099); peak year 3 at 57,822.92 with all four grants vesting in year 3 (c100: G1 years 2-4, G2 years 1-3, G3 years 1-4, G4 years 3-5).")
row("cards-c102-equity-wording", "2.7-cards (changed card c102, wording) (round 6 FAIL re-verified)", "cards.json AC1-c102 (L07); L07 Corollary 2.2 and Theorem 2.1 (c)", "PASS",
    R + "The round-6 wording ('equity moves from retained earnings to APIC') is replaced: 'net income falls by the expense, retained earnings fall and APIC rises by the same amount, so total equity is unchanged (Corollary 2.2)'. Corollary 2.2 says a change in S_t moves delta RE (= NI) and delta APIC in opposite directions by the same amount and leaves delta Equity and delta Cash unchanged, holding OI fixed; Theorem 2.1 (c) gives delta APIC + delta RE = OI for every S. The card's 'retained earnings fall' is the change in retained earnings, and 'total equity is unchanged' is the corollary's claim. Note for the builder: the card omits the corollary's 'holding OI fixed'; it is not needed for the equity answer.")
row("cards-c098-citation", "2.7-cards (citation for the total-equity sentence)", "cards.json AC1-c098 (L07); Theorem 2.1 (c) and (d); Corollary 2.2", "PASS",
    R + "Same reading as c102. The equity answer 'No' holds for every S (delta Equity = OI in Theorem 2.1 (c)); the expense move is the corollary's isolated change.")
row("cards-L08", "2.7-cards (lesson 8) (re-verified)", "cards.json c105-c121, c125; L08.html (changed Section 3 and Example 2.2 text; Theorem 2.1 (c))", "PASS",
    R + "Read against current L08 text and run of lab-AC1-L08-1.py (seed 20260702): DTL peak 2,942.10 in years 2 and 3 with K_t 14,010.00 (c116); zero at year 5 (c116); 5 of 5 years (c117); Example 2.2 year-1 current tax 6,300 and deferred expense 4,200, total 10,500 (c119, c120). c121 matches the new sentence on an extra deduction of d.")
row("cards-c057", "2.7-cards (changed card) (re-verified)", "cards.json AC1-c057 (L04); L04 Remark 1.2 and Section 4", "PASS", R + "Card says the lesson does not say which framework requires which timing or classification; Remark 1.2 and Section 4 say the same.")
row("cards-c069", "2.7-cards (changed card, T) (re-verified)", "cards.json AC1-c069 (L05); L05 Section 2 paragraph and problem P3", "PASS", R + "The difference between conventions at month m < 12 is the convention-1 revenue of the over-time obligations through m; P3 proves it.")
row("cards-c071", "2.7-cards (changed card) (re-verified)", "cards.json AC1-c071 (L05); L05 Section 3", "PASS", R + "Section 3 names the four inputs and states that the standards' requirements are open; no primary text is cited.")
row("cards-c079", "2.7-cards (changed card) (re-verified)", "cards.json AC1-c079 (L06); L06 Definition 1.4", "PASS", R + "A0 = L0 because there are no initial direct costs, prepayments or incentives; straight-line with the remainder in the last year.")
row("cards-c087", "2.7-cards (changed card) (re-verified)", "cards.json AC1-c087 (L06); L06 Section 3", "PASS", R + "Section 3 lists the discount rate, initial asset, expense pattern, and variable payments and options as open; no primary text is cited.")
row("cards-c104", "2.7-cards (changed card, T) (re-verified)", "cards.json AC1-c104 (L07); L07 Definition 1.1 and Theorem 1.3", "PASS", R + "The schedule is fixed by grant year, vesting years and total cost, and sums to the total.")
row("cards-c052", "2.7-cards (changed card, T) (re-verified)", "cards.json AC1-c052 (L04); L04 Proposition 2.1", "PASS", R + "Proposition 2.1 proof: the recognition rule changes the quarter of expense, not the payments.")
row("cards-c013-scope", "2.7-cards (scope 'any opening balances') (carry)", "cards.json AC1-c013 (L01); L01 Proposition 3.2", "PASS", CARRY_OF("L01.html and the c013 card line") + " the same text.")
row("cards-c088-scope", "2.7-cards (scope of the 'No' answer) (re-verified)", "cards.json AC1-c088 (L06); L06 Lab 1 figures and Proposition 2.3", "PASS", R + "'Only the sums over the term are guaranteed equal' matches Proposition 2.3; figures match the lab run.")
row("cards-c018-wording", "2.7-cards (paraphrase wording) (carry)", "cards.json AC1-c018 (L02); L02 Definition 1.1", "PASS", CARRY_OF("L02.html and the c018 card line") + " the same text.")
row("cards-c059-c060-c070-c090", "2.7-cards (C-graded lab results, re-computed)", "cards.json AC1-c059, c060, c070, c090 (L04, L05, L06)", "PASS",
    R + "Re-computed from the lab runs: c059 -4,974,286 and the purchase of 6,632,381 (probe); c060 3,319,293 (lab output); c070 32,792,272 and 23,333,398 in 8 months (lab output); c090 13,034,273 vs 13,034,272 (lab output).")
row("proj-line-377-working-capital-terms", "2.9-prose (wording) (new round 7)", "course/modules/AC/AC1/project.html line 377 (Cash flow statement, indirect method)", "FAIL",
    R + "'cash_from_operations is net income plus depreciation plus those three terms, which are the changes in working capital (receivables, inventory and payables)'. The same sentence defines receivables and inventory as the NEGATIVES of their increases, so the terms are the cash effects of those changes, not the changes. Verified numerically: lab Lab 3 receivables term 0 and payables -(-250,000) = +250,000 in the cash flow formula.",
    "Replace 'which are the changes in working capital' with 'which are the cash effects of the changes in receivables, inventory and payables'.")
row("proj-line-378-missing-space", "2.9-prose (typography) (new round 7)", "course/modules/AC/AC1/project.html line 378 ('...the suite checks that it is zero.<code>cash_gap</code>')", "FAIL",
    R + "The Articulation gaps item joins two definitions with no space or break: 'it is zero.<code>cash_gap</code>' renders as 'zero.cash_gap'. A reader sees the balance gap's sentence run into the next name.",
    "Insert a space after 'zero.' (or split the item).")

# ---- mutants ----
prev_mut = {m["id"]: m for m in PREV["mutants"]}
kills = {}
for line in (RUN / "mutants_r7_run1.out").read_text(encoding="utf-8").splitlines():
    m = re.match(r"(m\d\d)\S*: KILLED seed (\d+): (FAILED \S+)", line)
    if m:
        kills[m.group(1)] = f"{m.group(3).replace('FAILED ', '')} (seed {m.group(2)})"
for line in (RUN / "mutants_new_r7.out").read_text(encoding="utf-8").splitlines():
    m = re.match(r"(m\d\d)\S*: KILLED seed (\d+): (FAILED \S+)", line)
    if m:
        kills[m.group(1)] = f"{m.group(3).replace('FAILED ', '')} (seed {m.group(2)})"
kills["m23"] = "test_income_statement_matches_the_ledger[2024-02-29] (seed 0; 66 failures after repair)"
kills["m27"] = "test_income_statement_matches_the_ledger[2024-05-31] (seed 0; 48 failures after repair)"
kills["m05"] = "test_balance_sheet_matches_the_ledger[2024-12-31] (seed 1; passes on seed 0 by design)"
mut_rows = []
files = sorted(p for p in (CHK / "ledgers/AC1/mutants").glob("m*.py"))
new_desc = {
    "m33": "a student who leaves long-term debt out of total liabilities",
    "m34": "a student who forgets depreciation in net income",
    "m35": "a student who takes working-capital changes from the balance, not the month's change",
    "m36": "a student who starts the cash flow from period-end cash instead of previous month end",
    "m37": "a student who measures the depreciation gap with the change in net equipment",
    "m38": "a student who computes balance_gap as assets less liabilities, leaving out equity",
    "m39": "a student who strips spaces from account names before the chart check",
    "m40": "a student who lets an integral float on the credit side through",
    "m41": "a student who length-checks dates and trusts fromisoformat, accepting week dates",
}
for path in files:
    mid = path.name[:3]
    first_line = path.read_text(encoding="utf-8").splitlines()[0].strip('"')
    desc = prev_mut[mid]["description"] if mid in prev_mut else new_desc[mid]
    entry = {"id": mid, "description": desc, "file": f"ledgers/AC1/mutants/{path.name}"}
    if mid in ("m39", "m40", "m41"):
        entry["killed_by"] = ""
        entry["survived"] = "seeds 0-4 (run_mutants.sh) and mutate_graders seeds 0-9"
    else:
        entry["killed_by"] = kills.get(mid, "")
    mut_rows.append(entry)

fragment = {
    "unit": "AC1",
    "slice": "AC1-d",
    "round": 7,
    "verifier": "Claude Haiku 5.5, independent verifier for AC1-d, round 7; did not build AC1; the round-6 fragment was read as context only; no round-6 PASS row is trusted unless its cited subject is byte-identical, and every row whose subject changed was re-verified",
    "pin": "de53f7e (detached worktree /tmp/verify7-AC1-d); previous pin d57df1e (round 6)",
    "base": "d57df1e. Delta in slice: project.html lines 368, 373, 377, 378; cards.json line 716 (card AC1-c102); grader/test_project.py (three new post cases, collect count 177 -> 180); tests/labs/AC1/lab-AC1-L07-1.py (not in slice). L04-L08 changed (cards depend on them and were re-read in full).",
    "checkout": "/tmp/verify7-AC1-d",
    "scratch": "/tmp/AC1-v7/AC1-d/",
    "verified_at": "__NOW__",
    "rows": rows,
    "mutants": mut_rows,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Round-7 scope: all 70 round-6 row ids are kept. Rows whose subject changed were re-verified, not carried: project.html lines 368/373/377/378, grader/test_project.py, cards.json (c102), and the L04-L08 lessons that cards cite. Carried rows use the 'Carried from round 6' prefix and cite only byte-identical subjects.",
        "Mutants m23 and m27 (round 6) were defective: their income_statement read an undefined name 'now' and died with NameError, so their round-6 kill did not test the described error. Repaired in the checkout (ledgers/AC1/scripts/AC1-d-r7/repair_m23_m27.py) and re-killed by genuine failures.",
        "Out of slice, not graded here: index.html lines 165-166 (the hub's worked-example card) says 'ten generated transactions', while project.html line 352 says the labs' ledgers are written out by hand; L04 new Lab 1 claim (per-quarter net-income difference equals minus the change in prepaid_balance_b) was checked numerically by this verifier (quarters 1 and 2) but belongs to the L04 slice; L07 Remark claim about the generator's grant years 1-3 and vesting 3-4 years (every vesting year within years 1-6) was checked by the lab code only.",
        "Not checked: no network reads (verify_refs live ran for AC1 only, 2 of 560 entries); no bibliographic claim about penman2013financial beyond the registry key; the course-level gates (run_graders for other units, page_smoke for other pages) are other slices; the browser (Pyodide) run was run through tools/page_smoke.py, not by a human in a browser.",
        "Not checked: the seed shown in the browser panel is read from grader.js, not by loading the page in a browser; hours are design targets (no pace estimate failed).",
    ],
    "summary": {},
}
counts = {"PASS": 0, "FAIL": 0, "UNVERIFIABLE": 0}
for r in rows:
    counts[r["status"]] += 1
killed = sum(1 for m in mut_rows if m.get("killed_by"))
fragment["summary"] = {
    "rows": len(rows),
    "pass": counts["PASS"],
    "fail": counts["FAIL"],
    "unverifiable": counts["UNVERIFIABLE"],
    "mutants": len(mut_rows),
    "mutants_killed": killed,
    "verdict": "FAIL" if counts["FAIL"] or counts["UNVERIFIABLE"] or killed != len(mut_rows) else "PASS",
}
fragment["verdict"] = fragment["summary"]["verdict"]
import datetime
fragment["verified_at"] = datetime.datetime.now(datetime.UTC).replace(microsecond=0).isoformat()
out = CHK / "ledgers/AC1/AC1-d.json"
out.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(json.dumps(fragment["summary"]))
