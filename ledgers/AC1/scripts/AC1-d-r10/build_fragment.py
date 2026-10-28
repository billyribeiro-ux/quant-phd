"""Writes ledgers/AC1/AC1-d.json (round 10, slice AC1-d). Run with python -I from the checkout root.

Every command row was run on this pin (af08ad1); the outputs are in /tmp/AC1-v10/AC1-d/ and cited by command.
Carried rows cite files that are byte-identical since the previous pin 96dd532.
"""

import json
import pathlib
import re

ROOT = pathlib.Path("/tmp/verify10-AC1-d")
OUT = ROOT / "ledgers/AC1/AC1-d.json"
CARRY = "Carried from round 9 (course/modules/AC/AC1/project.html, tests/labs/AC1 twins, grader/instance.py, grader/reference.py byte-identical since the previous pin 96dd532): "
CARRY_CARDS = "Carried from round 9 (cards.json entries and the cited lesson sections byte-identical since 96dd532): "
RE = "Re-verified round 10: "
rows = []


def row(rid, check, location, status, evidence, fix=None):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        assert fix, rid
        r["fix"] = fix
    rows.append(r)


# ---- commands, re-run on af08ad1 ----
row("proj-run-graders", "2.6-autograder-reference", "course/modules/AC/AC1/grader/ (reference.py, instance.py, test_project.py)", "PASS",
    RE + "tools/run_graders.py --unit AC1 --seeds 0-9 -> 'run_graders AC1: PASS (reference 10/10 seeds, slowest 0.3 s)'. Direct: ledgers/AC1/scripts/AC1-d-r10/run_suite.sh on reference.py seeds 0-4 -> '208 passed in 0.14s' to '0.15s' each.")
row("proj-collect-count-176", "2.6-spec-test-count", "project.html line 368 ('collects 208 checks'); grader/test_project.py", "PASS",
    RE + "ledgers/AC1/scripts/AC1-d-r10/run_suite.sh reference.py seeds 0-49, collect-only: 50 of 50 runs print '208 tests collected' (/tmp/AC1-v10/AC1-d/w/c*). Page line 368: 208 for each seed 0 to 49, equal.")
row("proj-local-suite-reference", "2.6-autograder-local-run", "grader/test_project.py; project.html line 413-415 local command", "PASS",
    RE + "run_suite.sh uses the page flags (-q -p no:cacheprovider --assert=plain -W error) with QF_SEED=0..4 on reference.py: '208 passed' each. The page's local command is the same flag set.")
row("proj-pyodide-smoke", "2.6-autograder-pyodide", "course/modules/AC/AC1/project.html (labs 1-3, grader panel)", "PASS",
    RE + "tools/page_smoke.py --unit AC1 --pages project.html -> 'page_smoke AC1: PASS'. pytest pin: LOCK.json pytest@9.0.2 (pyodide 314.0.7), matching the page's 'pytest 9.0' and 'Python 3.14'.")
row("proj-check-pages", "2.9-structure", "course/modules/AC/AC1/*.html; cards.json", "PASS",
    RE + "tools/check_pages.py --all -> 'check_pages AC1: PASS' (exit 0).")
row("proj-check-projects", "2.6-hours-and-structure", "course/modules/AC/AC1/project.html (budget, rungs)", "PASS",
    RE + "tools/check_projects.py --all -> 'check_projects AC1: PASS' (exit 0).")
row("proj-check-dag", "2.9-dag-concepts", "project.html 'Concepts used here' (line 380)", "PASS",
    RE + "tools/check_dag.py --all -> 'check_dag AC1: PASS' (exit 0). Line 380 is unchanged since 96dd532 (git diff).")
row("proj-run-labs", "2.5-labs", "tests/labs/AC1/lab-AC1-project-1.py, -project-2.py, -project-3.py and the L01-L08 twins", "PASS",
    RE + "tools/run_labs.py --unit AC1 -> 'run_labs AC1: PASS (11/11)'. Also .venv/bin/python -I -W error -m pytest tests/test_labs.py -k AC1: 11 passed.")
row("proj-lab-twin-embed", "2.5-lab-embed-equals-twin", "project.html lab blocks 56-253 (Lab 1), 260-343 (Lab 2), 420-518 (Lab 3); tests/labs/AC1/lab-AC1-project-*.py", "PASS",
    CARRY + "run_labs AC1 (re-run this round) compares each embedded block with its twin and its page expected output: 11/11 PASS. Lab 2 blanks are the completion-lab rule.")
row("proj-labs-ruff", "2.9-lint", "tests/labs/AC1; course/modules/AC/AC1/grader", "PASS",
    RE + ".venv/bin/ruff check course/modules/AC/AC1/grader tests/labs/AC1 -> 'All checks passed!'; ruff format --check -> '15 files already formatted'.")
row("proj-mypy-gate", "2.9-types", "tests/labs/AC1; course/modules/AC/AC1/grader", "PASS",
    RE + ".venv/bin/mypy --no-incremental course/modules/AC/AC1/grader tests/labs/AC1 -> 'Success: no issues found in 15 source files'.")
row("proj-verify-refs", "2.1-citations", "references/references.json; project.html line 534 (data-cite penman2013financial)", "PASS",
    RE + "tools/verify_refs.py --offline -> 'offline integrity: 560 entries, 0 problems'; tools/verify_refs.py --unit AC1 (live) -> '2 of 560 entries, 0 problems'. The registry entry penman2013financial is an Open Library book record (verified_by openlibrary). The page's reading statement (line 536) says no chapter is assigned, which the page itself states.")
row("proj-hours", "2.9-hours", "project.html line 35 (data-hours-project 30), time-budget rows (lines 390-398); index.html data-hours-lessons 90; L01-L08 data-hours 11,12,11,11,12,12,11,10", "PASS",
    RE + "Sum of the nine rows 1+3+4+4+3+5+2+5+3 = 30 = the total row and data-hours-project. Lesson hours 11+12+11+11+12+12+11+10 = 90 = data-hours-lessons; 90+30 = 120 = the hub's '120 hours'. No arithmetic inconsistency; pace is not judged (architect ruling).")
row("proj-prose-banned", "2.9-banned-phrases", "project.html; cards.json; grader/test_project.py; L01-L08 changed passages", "PASS",
    RE + "grep -i for roughly, historically, typically, usually, approximately, generally, 'about <digit>', ellipsis, builder, verifier, round: no hit in project.html, test_project.py or changed card text; the only hits are 'rounds half up' (cards.json, a technical term), 'one half' (L01 problem text, a fraction) and 'typically' in L07 quiz text (a lesson quiz, outside this slice).")
row("proj-alt-implementations", "2.6-alternatives-pass", "course/modules/AC/AC1/grader/test_project.py (whole suite)", "PASS",
    RE + "ledgers/AC1/scripts/AC1-d-r10/run_alts.sh alts_all (8 correct implementations: 3 new in alts/ made by make_r10.py, 3 round-8 and 2 round-9 in alts_all/): all 8 PASS seeds 0-9 (/tmp/AC1-v10/AC1-d/run_alts.out). New alternatives: regex date with strptime and an exact int type; sorted postings with an early break and a month-length table; statement-dict articulation with str dates.")
row("proj-overconstraint-nonmapping", "2.6-over-constraint", "grader/test_project.py post cases (lines ~503-550) and period-end cases (line ~735)", "PASS",
    RE + "Every new case maps to a sentence of the Constraints list on project.html line 366 (named conditions) or to the Conventions (line 373, the account repeated within one entry, 375-379). The alternatives above pass all 208 checks on seeds 0-9, so none of the new cases over-constrains a correct implementation tested here.")
row("proj-mutants-set-killed", "2.6-mutants", "ledgers/AC1/mutants/ (61 files)", "PASS",
    RE + "tools/mutate_graders.py --unit AC1 --seeds 0-9 -> 'mutate_graders AC1: PASS (61/61 killed)' (/tmp/AC1-v10/AC1-d/mutate2.out). Round 9 reported 44/47 with m45, m46, m47 surviving; the grader now has the post cases that kill them.")
row("proj-mutants-new-r10-m58-m61", "2.6-mutants-new", "ledgers/AC1/mutants/m58-m61 (4 new student-error mutants)", "PASS",
    RE + "Written this round by ledgers/AC1/scripts/AC1-d-r10/make_r10.py from reference.py: m58 keeps one posting per account (a second line on one account overwrites the first; killed by test_an_account_repeated_within_one_entry_is_posted_in_full); m59 leaves payables out of cash from operations (killed by test_articulation_gaps_are_zero[2024-05-31]); m60 compares balance-sheet cash with beginning cash (killed by test_small_ledger_january_articulation_is_zero); m61 sets retained earnings to minus the dividends (killed by test_articulation_gaps_are_zero[2024-04-30]). Each is a plausible student error against Conventions on project.html lines 373-379.")
for rid, desc, killer in [
    ("proj-mutants-m01-m08", "m01-m08", "killed on seed 0 (mutate2.out)"),
    ("proj-mutants-m11-m20", "m11-m20", "killed on seed 0 (mutate2.out)"),
    ("proj-mutants-m21-m25", "m21-m25", "killed on seed 0 (mutate2.out)"),
    ("proj-mutants-m33-m38", "m33-m38", "killed on seed 0 (mutate2.out)"),
]:
    row(rid, "2.6-mutants", f"ledgers/AC1/mutants/ {desc}", "PASS",
        RE + f"tools/mutate_graders.py --unit AC1 --seeds 0-9: every mutant in {desc} KILLED on seed 0 (/tmp/AC1-v10/AC1-d/mutate2.out).")
MUTANT_ROWS = [
    ("proj-mutant-m09-articulation-zero", "m09_articulation_all_zero.py"),
    ("proj-mutant-m10-depreciation-gap", "m10_depreciation_gap_no_expense.py"),
    ("proj-mutant-m26-payables-sign", "m26_payables_increase_sign_reversed.py"),
    ("proj-mutant-m27-cogs-from-balance", "m27_cogs_from_balance_not_flow.py"),
    ("proj-mutant-m28-timestamp-date-accepted", "m28_timestamp_truncated_accepted.py"),
    ("proj-mutant-m29-boolean-credit-accepted", "m29_boolean_credit_accepted.py"),
    ("proj-mutant-m30-whitespace-date-accepted", "m30_whitespace_date_accepted.py"),
    ("proj-mutant-m31-account-name-case-folded", "m31_account_name_case_folded.py"),
    ("proj-mutant-m32-retained-gap-sign", "m32_retained_gap_dividends_added.py"),
    ("proj-mutant-m39-account-name-whitespace-stripped", "m39_account_name_whitespace_stripped.py"),
    ("proj-mutant-m40-credit-float-accepted", "m40_credit_float_accepted.py"),
    ("proj-mutant-m41-week-date-accepted", "m41_week_date_accepted.py"),
    ("proj-mutant-m42-month-end-previous-length", "m42_month_end_uses_previous_month_length.py"),
    ("proj-mutant-m43-negative-credit-absolute", "m43_negative_credit_taken_as_absolute.py"),
    ("proj-mutant-m44-unbalanced-one-direction", "m44_unbalanced_only_when_debits_exceed_credits.py"),
    ("proj-mutant-m45-negative-debit-clamped", "m45_negative_debit_clamped_to_zero.py"),
    ("proj-mutant-m46-unpadded-date-accepted", "m46_strptime_date_accepts_unpadded.py"),
    ("proj-mutant-m47-numeric-string-amount", "m47_numeric_string_amount_accepted.py"),
]
for rid, fname in MUTANT_ROWS:
    row(rid, "2.6-mutant", f"ledgers/AC1/mutants/{fname}", "PASS",
        RE + f"mutate_graders.py --seeds 0-9: {fname} KILLED (/tmp/AC1-v10/AC1-d/mutate2.out).")
row("proj-mutants-new-r9-three-written", "2.6-mutants", "ledgers/AC1/mutants/ m45 to m47", "PASS",
    RE + "m45, m46, m47 KILLED in the round-10 gate run (mutate2.out); the round-9 survivors are now killed by post cases for a negative debit balanced by a credit, unpadded dates and numeric-string amounts.")
row("proj-mutants-new-m26-m28", "2.6-mutants", "ledgers/AC1/mutants/ m26-m28, m29-m32, m33-m41, m42-m57", "PASS",
    RE + "All 61 mutant files KILLED in mutate2.out (m26-m57 included).")

# ---- page specification and statements ----
row("proj-page-spec-carry", "2.4-spec-vs-suite", "project.html line 366 (Constraints: 'Every named error condition raises ValueError ... The named conditions are these'); grader/test_project.py post cases", "PASS",
    RE + "Each named condition has a test (test_post_raises_a_value_error ids and the period-end list): transaction without date, without lines; date form and calendar date (2024-02-30, 02/01/2024, 20240102, W01, time, spaces, unpadded month/day, 2023-02-29, month 13, non-string); empty lines; line without account, debit, credit; account outside chart and case and spaces; amount not integer (5.0, True, numeric string); negative amount (debit -5 balanced; credit -5; -1 cent debit and credit); line with both or neither; unbalanced entry. The period-end test covers all four statement functions for six non-month-end forms and two more (2024-01-30, 2024-04-31). The round-9 survivors m45-m47 are now killed.")
row("proj-page-spec-carry-post-cases", "2.4-spec-vs-suite", "grader/test_project.py test_post_raises_a_value_error parametrize list (lines ~503-550)", "PASS",
    RE + "The new cases at lines 504-552 were read in full and each raises the named ValueError in the reference (the reference rejects each: ledgers/AC1/scripts/AC1-d-r10/run_suite.sh reference.py, 208 passed means every case raised ValueError as the reference does).")
row("proj-no-expected-value-leak", "2.4-page-claim-vs-output", "project.html line 368 ('A failing check names the property that failed and never prints the expected value'); grader/test_project.py _check_values (line ~225-236)", "FAIL",
    RE + "Local command on the page's flags (QF_SEED=0, pytest -q -p no:cacheprovider --assert=plain -W error test_project.py) with a candidate that has retained earnings wrong (m03_dividends_not_deducted.py): output has 26 traceback blocks printing 'expected = {'accounts_payable': ..., 'cash': 68785524, ...}' (seed 0) and 'got = {...}' (/tmp/AC1-v10/AC1-d/w/full_m03_seed0.txt). The leak persists with --no-showlocals (26 lines). '--tb=short' removes it (0 lines). The in-browser runner (py-worker.js line 107-108) reports only reprcrash.message, which carries no expected value, so the leak is in the local output the page documents.",
    fix="In grader/test_project.py _check_values add '__tracebackhide__ = True' as its first statement (scratch test: /tmp/AC1-v10/AC1-d/fixtest/test_project.py gives 0 'expected =' lines and '43 failed, 165 passed'), or keep the page claim narrower ('the message never prints the expected value'). Re-run the suite on seeds 0-9 after the change.")
row("proj-grader-carry", "2.6-grader-file", "grader/test_project.py (whole file, 792 lines, read in full this round)", "FAIL",
    RE + "Read in full. Oracle (_through, _expected_*) recomputed independently from TXS; all 208 checks pass on the reference for seeds 0-49; every test traced to the Constraints/Conventions; the leak of expected values in pytest's traceback output is in _check_values (see proj-no-expected-value-leak).",
    fix="Apply the __tracebackhide__ fix in _check_values (see proj-no-expected-value-leak).")
row("proj-line-368-grading-claims", "2.4-page-claims", "project.html line 368 (collect count, seeds, warnings, coverage list, 'never prints the expected value')", "FAIL",
    RE + "Count and seed claims: PASS (208 on seeds 0-49). The 'never prints the expected value' sentence: FAIL (proj-no-expected-value-leak). The coverage list is accurate: chart, imports, posting rules and each named error, silence and return values, 12 month ends, balance identity, cash tie, net change, retained earnings, operating formula, four gaps, month-end rule, hand-worked January ledger (SMALL and GAP_WITNESS).",
    fix="Make the traceback match the sentence (see proj-no-expected-value-leak), or narrow the sentence to the failure message.")
row("proj-line-37-lede-seed", "2.9-lede", "project.html line 37 (lede) and the grader panel", "PASS",
    CARRY + "line 37 states a 200-transaction ledger from the seed in the autograder section; instance.py make_instance(seed) gives 200 transactions dated 2024-01-01 to 2024-12-31 for seeds 0, 7 and 49, all balanced, all labelled SIMULATED (re-run this round).")
row("proj-footer-nothing-leaves", "2.9-footer", "project.html line 549 footer ('nothing you write leaves it')", "PASS",
    CARRY + "footer line byte-identical; course/assets/js/grader.js and py-worker.js unchanged; the only fetch in grader.js (line 18, text(url)) loads the grader's own local files, and no outbound request appears in grader.js, py-worker.js or python.js.")
row("proj-line-377-working-capital-terms", "2.4-convention-formula", "project.html line 377 (Cash flow statement, indirect method)", "PASS",
    RE + "Recomputed: operating = net income + depreciation - change(AR) - change(inventory) - change(AP) in debit-minus-credit terms; the payables term -change(AP) is the increase in accounts payable (credit balance), matching reference.py cash_flow_statement and the page wording. Lab 1 check: receivables +200,000, inventory +900,000, payables -2,500,000 sum to -1,400,000.")
row("proj-line-378-missing-space", "2.9-prose", "project.html lines 378-379 (Articulation gaps)", "PASS",
    RE + "Re-read lines 378-379 in full. 'The suite does not test the sign of this always-zero quantity, since a reversed sign also gives zero.' True: -0 = 0, and the suite asserts == 0 only (test_articulation_gaps_are_zero, test_small_ledger_january_articulation_is_zero).")
row("proj-balance-gap-sign-unenforced", "2.4-page-claim", "project.html line 378 (Conventions, Articulation gaps)", "PASS",
    RE + "The suite contains no test of the sign of balance_gap (grep balance_gap in test_project.py: only zero checks). Claim verified.")
row("proj-scope-sentence-line-352", "2.4-scope", "course/modules/AC/AC1/project.html line 352 (Context)", "PASS",
    RE + "The sentence names balances through the date, the flows of the calendar month, and cash flows built from net income (indirect); the suite's oracle (_through, _expected_flows, _expected_cash_flow) does exactly these three things.")
row("proj-conventions-debit-balance-sentence", "2.4-convention", "project.html line 373 (Conventions, Balance through a date)", "PASS",
    RE + "Chart classes in starter.py and test_project.py: asset, distribution, expense debit-normal; contra_asset, liability, equity, revenue credit-normal. The sentence matches the chart.")
row("proj-page-lab-carry", "2.5-lab-page", "project.html lab blocks (Lab 1 56-253, Lab 2 260-343, Lab 3 420-518)", "PASS",
    RE + "Lab 1: 22 postings, rejected message, balance gap 0 at both month ends, Feb net income 700,000, operating -700,000, ending cash 4,800,000 (run_labs PASS). Lab 2: 700,000 / -700,000 / 0 / 0; cash gap 0, earnings gap 0 (run_labs PASS). Lab 3: March investing -3,000,000, financing 850,000, net income -330,000, assets 7,870,000 = 2,250,000 + 6,000,000 - 380,000 (re-derived by hand). Interpretation paragraphs checked line by line.")
row("proj-page-ladder-browser-carry", "2.9-ladder", "project.html lines 40-47, 51-52, 406, 414, 533, 548", "PASS",
    RE + "Rung 2 and Rung 3 statements match index.html line 72 (mastery bar 8 of 9); Lab 3 is eleven entries (counted); the autograder uses 200 transactions (instance.py COUNT = 200).")
row("proj-instances-carry", "2.6-instance", "course/modules/AC/AC1/grader/instance.py", "PASS",
    RE + "instance.py unchanged since 96dd532. Re-generated seeds 0, 7, 49: 200 transactions, all dated 2024, all balanced, label SIMULATED (no unbalanced entry; accounts within the chart).")
row("cards-inventory-and-dupes", "2.7-cards-inventory", "course/modules/AC/AC1/cards.json (126 cards)", "PASS",
    RE + "126 cards, ids AC1-c001 to AC1-c126 with no gap; no duplicate id; no duplicate front; lesson counts L01 16, L02 16, L03 16, L04 16, L05 14, L06 16, L07 14, L08 18 (sum 126).")
row("cards-grades", "2.3-grades", "cards.json grade and basis fields", "PASS",
    RE + "41 cards grade T, 42 grade C (each C card has a basis), 43 cards carry no grade field (definition and restatement cards; check_pages validates a grade only when present, tools/check_pages.py line 387). Basis fields read for every C card.")
row("cards-numbers-in-lessons", "2.7-card-numbers", "cards.json; L01-L08 (tag-stripped text)", "PASS",
    RE + "ledgers/AC1/scripts/AC1-d-r10/cards_numbers.py over all 126 cards (/tmp/AC1-v10/AC1-d/cards_numbers.out): every number appears in the card's own lesson, except AC1-c077 whose '5,000' is written as \\(5{,}000\\) in L06 (line 68) and so differs only by TeX markup.")
row("cards-labels-resolve", "2.7-card-citations", "cards.json citations against each card's own lesson", "PASS",
    RE + "Each citation in the changed cards resolves: c028 Definition 2.1 and Proposition 2.2 (L02 lines 30-33); c029 Proposition 3.2 (L02 line 40); c032 Definition 4.1; c040 and c124 Proposition 3.1 (L03 line 38); c033 Definition 1.1 (L03 line 23).")
row("cards-banned", "2.7-banned", "cards.json", "PASS",
    RE + "No banned phrase in any card (grep: roughly, about, historically, typically, ellipsis, 'process' words): none.")
row("cards-registry-cites", "2.7-registry", "cards.json", "PASS",
    RE + "No card carries a registry key or a citation outside its lesson labels; every basis is a lesson convention or a lab, and c057, c071, c087 state that the lesson cites no primary text.")
row("cards-c015", "2.7-card", "cards.json AC1-c015; L01.html Remark 2.2 (changed) and Definition 1.1", "PASS",
    RE + "Remark 2.2 now lists the posting checks: balance, accounts exist, non-negative integer cents, not both sides. The card answers the question correctly (the wrong-account entry passes) and states the balance and account tests as the check; it attributes cents and one-side to Definition 1.1 (lines 30-32: 'either a debit or a credit'). It omits two tests the Remark also names but does not claim the check lacks them, so the answer is supported.")
row("cards-L01", "2.7-cards", "cards.json c001-c007, c009-c016; L01.html", "PASS",
    RE + "c010 re-read against Remark 2.2 (its 'does not check ... right account' sentence is unchanged): PASS. c013 against Proposition 3.2 of L01 (unchanged, hypotheses (i)-(v) stated). Other cards: " + CARRY_CARDS + "their cited L01 sections are byte-identical.")
row("cards-L01-claims-table-scope", "2.7-table-vs-remark", "course/modules/AC/AC1/L01.html Key results (section 8), row 'A balanced entry posted to the wrong account passes the check (Remark 2.2)'", "FAIL",
    RE + "The basis cell reads 'The posting check tests balance, integer non-negative cents and at most one side per line (Remark 2.2)'. Remark 2.2 (L01 line 43-44) lists four posting checks, and the fourth is that the accounts exist. The cell therefore lists three of the four and then says 'that test [accounts outside the chart] belongs to the lab, not to Definition 1.1', which contradicts the Remark's statement that the posting check tests the accounts.",
    fix="In the basis cell of the key-results row, list the four posting checks of Remark 2.2 (balance, accounts exist, non-negative integer cents, not both sides) and drop the claim that the account test belongs only to the lab.")
row("cards-c040-investing-scope", "2.7-card-scope", "cards.json AC1-c040 (grade T, L03); L03.html Proposition 3.1 (hypotheses (i)-(iv), line 39)", "PASS",
    RE + "Round-9 FAIL cured. The card now reads 'In the lab's ledger, under the hypotheses of Proposition 3.1, investing cash flow equals minus the change in equipment at cost'. Proposition 3.1 (i)-(iv) is the hypothesis set; the card states it as a condition and does not claim the lab meets it.")
row("cards-c124-financing-scope", "2.7-card-scope", "cards.json AC1-c124 (grade T, L03); L03.html Proposition 3.1 (iii), (ii)", "PASS",
    RE + "Round-9 FAIL cured. The card now states 'under the hypotheses of Proposition 3.1' and matches the financing sentence of the proposition.")
row("cards-c126-straight-line", "2.7-card", "cards.json AC1-c126 (grade C, L03); L03.html Definition 1.2 and Remark 6.3", "PASS",
    CARRY_CARDS + "cited Definition 1.2 and Remark 6.3 byte-identical.")
row("cards-c027-prop32-scope", "2.7-card-scope", "cards.json AC1-c027 (grade T, L02, 'Balance follows from double entry (Proposition 3.2)'); L02.html Proposition 3.2 (hypotheses, lines 40-41)", "FAIL",
    RE + "Proposition 3.2 (L02, changed this round) holds only under its hypotheses: balanced entries, equity accounts only common stock and dividends, and the four income accounts of Definition 2.1 only. The card states the consequence 'Balance follows from double entry (Proposition 3.2)' without them, so it drops the condition the cited proposition states (the class of the round-9 FAILs on c040 and c124).",
    fix="Change the back of AC1-c027 to: 'No. Under the hypotheses of Proposition 3.2 (balanced entries, equity accounts only common stock and dividends, and only the four income accounts of Definition 2.1), balance follows from double entry. A wrong amount posted to both sides keeps the balance sheet in balance, as a balanced entry on the wrong account does (Lesson 1, Remark 2.2).' (The lesson's own sentence 'Proposition 3.2 is a consequence of double entry' in L02 misconceptions has the same gap; it belongs to the L02 slice.)")
row("cards-c028-net-income-scope", "2.7-card", "cards.json AC1-c028 (grade T, L02); L02.html Definition 2.1 and Proposition 2.2 (hypothesis: only the four income accounts)", "PASS",
    RE + "Changed card. 'Yes, with only the four income accounts of Definition 2.1' is the hypothesis of Proposition 2.2 as written at L02 line 33. Definition 2.1 (line 30) matches the S-K-O-D formula on the card (AC1-c022).")
row("cards-c029-prop32-hypotheses", "2.7-card-scope", "cards.json AC1-c029 (grade T, L02); L02.html Proposition 3.2 (line 40)", "PASS",
    RE + "Changed card. The back now states the hypotheses of Proposition 3.2 (only common stock and dividends as equity; only the four income accounts) and the year-end scope exactly as the proposition states them.")
row("cards-c032-activity-split", "2.7-card", "cards.json AC1-c032 (grade C, basis 'Convention of Lab 2 (Definition 4.1)'); L02.html key-results row and Definition 4.1", "PASS",
    RE + "Changed card. 'The lesson does not say ... not stated here' matches the key-results row (L02 line ~497) and Definition 4.1's convention.")
row("cards-L02", "2.7-cards", "cards.json c017-c032; L02.html", "FAIL",
    RE + "Per-card: c027 FAIL (scope drop, cards-c027-prop32-scope). c028, c029, c032 PASS (changed cards re-verified). c030 (Proposition 4.2, unchanged), c022 (Def 2.1, text changed but the card is consistent), c025, c026, c031 (Lab 2 numbers: 1,003,421.14; 1,654,305.29; 3,000,000.00; 4,454,305.29; 803,421.14, unchanged in the lab output and misconceptions) carried: " + CARRY_CARDS,
    fix="Fix AC1-c027 as in cards-c027-prop32-scope.")
row("cards-L03", "2.7-cards", "cards.json c033-c039, c041-c045; L03.html", "FAIL",
    RE + "c033 FAIL (Definition 1.1 now carries the hypotheses of Proposition 2.2); c039 FAIL (see cards-c039-prop22-scope); c042 FAIL (see cards-c042-thm51-scope). c034, c035, c036, c037 (Lab 3 numbers 1,300,000.00 and 2,191,615.64 for 2026 re-read at L03 lines 644 and 655, and the misconception text at line 531), c038 (see below), c041, c043, c044, c045 PASS (carried or re-verified).",
    fix="Fix AC1-c033, AC1-c039 and AC1-c042 as in their rows.")
row("cards-c033-definition11-scope", "2.7-card-scope", "cards.json AC1-c033 (What is articulation?); L03.html Definition 1.1 (line 24, changed)", "FAIL",
    RE + "Definition 1.1 now reads 'and, under the hypotheses of Proposition 2.2, operating cash flow can be computed from net income by the indirect method and gives the same figure as the direct method'. The card lists 'indirect operating cash flow equals the direct figure (Definition 1.1)' with no hypothesis, which is more than the definition states.",
    fix="In the back of AC1-c033 write 'and, under the hypotheses of Proposition 2.2, indirect operating cash flow equals the direct figure (Definition 1.1)'.")
row("cards-c039-prop22-scope", "2.7-card-scope", "cards.json AC1-c039 (grade T); L03.html Proposition 2.2 (hypotheses (i)-(v), changed (iv)) and key-results row (line 590)", "FAIL",
    RE + "The card answers 'Yes, in every year' for the lab's ledger at grade T and cites Proposition 2.2 as proving it 'for the lab's operating activity'. Proposition 2.2 proves the equality only under hypotheses (i)-(v). The page's own key-results row states the result 'under the hypotheses (i) to (v)'. The page does not show that the lab's ledger meets (i)-(v); the printed Check 2 is evidence and the lesson says it is not a test of the theorem (L03 Theorem 5.1 paragraph). A lab-level 'Yes in every year' is therefore graded above its evidence.",
    fix="Rewrite the back of AC1-c039: 'Under the hypotheses (i) to (v) of Proposition 2.2, the indirect and direct operating flows are equal (T). Whether the lab's ledger meets those hypotheses is shown only by Check 2 of Lab 3 (SIMULATED, C).' Split the grade accordingly or grade the lab part C.")
row("cards-c042-thm51-scope", "2.7-card-scope", "cards.json AC1-c042 (grade T); L03.html Theorem 5.1 (hypotheses, changed) and key-results row (line 593)", "FAIL",
    RE + "The card answers 'Yes' for every fiscal year of the lab's ledger and lists the five conclusions of Theorem 5.1, without its hypotheses. The Theorem and the key-results row state the result 'under the hypotheses of Theorem 5.1'. The hypotheses are not shown to hold for the lab's ledger; the card asserts the conclusion as a fact about the ledger.",
    fix="In the back of AC1-c042 write 'Under the hypotheses of Theorem 5.1 (those of Propositions 2.2, 3.1 and 4.2, and the hypotheses of Lesson 2, Propositions 3.2 and 4.2), the three statements agree in every fiscal year of the lab's ledger. The lab checks four of the five parts (SIMULATED, C).'")
row("cards-c038-wrong-schedule", "2.7-card", "cards.json AC1-c038 (grade T); L03.html Theorem 5.1 paragraph and misconception 'Statements that articulate are correct'", "PASS",
    RE + "The claim 'a wrong depreciation schedule still articulates, because the schedule enters the income statement and the balance sheet together' is the lesson's own misconception text (unchanged). Any schedule posted as balanced entries meets the hypotheses of Theorem 5.1, so the example is within them; the card does not claim the lab's numbers are right.")
row("cards-L03-c123", "2.7-card", "cards.json AC1-c123 (grade T); L03.html Proposition 4.2 and its proof", "PASS",
    CARRY_CARDS + "card states the hypotheses (no credit to equipment, no debit to accumulated depreciation, depreciation-only credits) as Proposition 4.2 does.")
row("cards-L03-theorem-5-1-print-claim", "2.7-card", "course/modules/AC/AC1/L03.html Theorem 5.1 paragraph; tests/labs/AC1/lab-AC1-L03-1.py", "PASS",
    RE + "The paragraph (L03 line 56) still says the lab checks four of five parts; Check 1 prints a gap 0.00 at each year end; Checks 2-4 print True (L03 lab output). run_labs PASS, and the twin changed only in its class docstring.")
row("cards-L03-theorem-5-1-print-claim-hypotheses", "2.7-card", "L03.html Theorem 5.1 hypotheses (line 53, changed)", "PASS",
    RE + "The stated hypotheses are: those of Propositions 2.2, 3.1, 4.2 of L03; Proposition 3.2 of L02 with its two hypotheses; Proposition 4.2 of L02 with its activity hypothesis. Each matches the statement of the cited proposition (L02 line 40 and 50; L03 lines 32, 39, 48). The gap in cards c039 and c042 is the lab's own compliance, not a mis-stated hypothesis.")
row("cards-L04", "2.7-cards", "cards.json c046-c060, c122; L04.html", "PASS",
    CARRY_CARDS + "L04.html byte-identical since 96dd532 (not in the delta). Lab output numbers are covered by run_labs PASS (L04 not re-derived this round).")
row("cards-L05", "2.7-cards", "cards.json c061-c074; L05.html", "PASS",
    CARRY_CARDS + "L05.html byte-identical since 96dd532.")
row("cards-L06", "2.7-cards", "cards.json c075-c090; L06.html", "PASS",
    CARRY_CARDS + "L06.html byte-identical since 96dd532. c077's '5,000' is \\(5{,}000\\) in L06 line 68.")
row("cards-L07", "2.7-cards", "cards.json c091-c101, c103, c104; L07.html", "PASS",
    CARRY_CARDS + "L07 text unchanged except the lab comment (HORIZON line) and the footer; the Lab 1 output (c099, c100) is unchanged and run_labs PASS.")
row("cards-c098-citation", "2.7-card", "cards.json AC1-c098 (L07); Theorem 2.1 (c)(d) and Corollary 2.2", "PASS",
    CARRY_CARDS + "theorem and corollary text unchanged.")
row("cards-c102-equity-wording", "2.7-card", "cards.json AC1-c102 (grade T, L07); L07.html Corollary 2.2", "PASS",
    CARRY_CARDS + "Corollary 2.2 unchanged; the card's 'total equity is unchanged' matches it.")
row("cards-L08", "2.7-cards", "cards.json c105-c108, c110-c121, c125; L08.html", "PASS",
    RE + "The changed §3 paragraphs (L08 line 141-142) are not cited by any card. c118 ('The recognition test for a deferred tax asset is outside the model and is not stated on this page (Section 3)') still matches the unchanged sentence at L08 line 251. Other cards carried: " + CARRY_CARDS + "Definition 1.1, 1.2, Section 2 and Theorem 2.1 unchanged.")
row("cards-c109-scope", "2.7-card", "cards.json AC1-c109 (L08); L08.html Definition 1.2", "PASS",
    CARRY_CARDS + "Definition 1.2 unchanged.")
row("cards-c008-wording", "2.7-card", "cards.json AC1-c008 (L01); L01.html Definition 1.3", "PASS",
    CARRY_CARDS + "Definition 1.3 unchanged.")
row("cards-c057", "2.7-card", "cards.json AC1-c057 (L04); L04 Remark 1.2 and Section 4", "PASS", CARRY_CARDS + "L04 unchanged.")
row("cards-c069", "2.7-card", "cards.json AC1-c069 (L05); L05 Section 2 and problem P3", "PASS", CARRY_CARDS + "L05 unchanged.")
row("cards-c071", "2.7-card", "cards.json AC1-c071 (L05); L05 Section 3", "PASS", CARRY_CARDS + "L05 unchanged.")
row("cards-c079", "2.7-card", "cards.json AC1-c079 (L06); L06 Definition 1.4", "PASS", CARRY_CARDS + "L06 unchanged.")
row("cards-c087", "2.7-card", "cards.json AC1-c087 (L06); L06 Section 3", "PASS", CARRY_CARDS + "L06 unchanged.")
row("cards-c104", "2.7-card", "cards.json AC1-c104 (L07); L07 Definition 1.1 and Theorem 1.3", "PASS", CARRY_CARDS + "L07 definitions unchanged.")
row("cards-c052", "2.7-card", "cards.json AC1-c052 (L04); L04 Proposition 2.1", "PASS", CARRY_CARDS + "L04 unchanged.")
row("cards-c013-scope", "2.7-card", "cards.json AC1-c013 (L01); L01 Proposition 3.2", "PASS", CARRY_CARDS + "L01 Proposition 3.2 (hypotheses (i)-(v)) unchanged.")
row("cards-c088-scope", "2.7-card", "cards.json AC1-c088 (L06); L06 Lab 1 figures and Proposition 2.3", "PASS", CARRY_CARDS + "L06 unchanged; Lab 1 output unchanged.")
row("cards-c018-wording", "2.7-card", "cards.json AC1-c018 (L02); L02 Definition 1.1", "PASS", CARRY_CARDS + "Definition 1.1 unchanged.")
row("cards-c059-c060-c070-c090", "2.7-card", "cards.json AC1-c059, c060, c070, c090 (L04, L05, L06)", "PASS", CARRY_CARDS + "L04-L06 unchanged; Lab 1 outputs unchanged.")
row("proj-cards-c001-c126-coverage", "2.7-coverage", "cards.json (all 126 cards)", "PASS",
    RE + "Every card was read this round (cards_dump in /tmp/AC1-v10/AC1-d/cards_dump.txt) and given a row above, a carried row, or a cards-L row; c001-c126 are each covered (c001-c007, c009-c016 cards-L01; c008 and c018 separate; c017-c032 cards-L02; c033-c045 cards-L03; c046-c060 and c122 cards-L04; c061-c074 cards-L05; c075-c090 cards-L06; c091-c104 cards-L07; c105-c121, c125 cards-L08; c123 cards-L03-c123; c124 and c040 scope rows; c126 row).")

FRAG = {
    "unit": "AC1",
    "slice": "AC1-d",
    "round": 10,
    "verifier": "Claude Haiku 5.5, independent verifier for AC1-d, round 10; did not build AC1; read the round-9 fragment as context; re-ran every command row; re-derived the delta since 96dd532; carried PASS rows only where the cited subject is byte-identical",
    "pin": "af08ad1 (detached worktree /tmp/verify10-AC1-d)",
    "base": "96dd532 (round 9 pin); delta is AC1 lessons L01, L02, L03, L07, L08 (prose, footers, lab comments), cards.json c028, c029, c032, c040, c124, grader/test_project.py (new post, period-end, and calendar cases), project.html line 368 (208 checks), index.html eyebrow, AC4/CF1/M1 excluded",
    "previous_ledger": "/tmp/fanout-frags/AC1-d.round9.json",
    "checkout": "/tmp/verify10-AC1-d",
    "scratch": "/tmp/AC1-v10/AC1-d/",
    "verified_at": "2026-10-28T06:00:00+00:00",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": "Mutants: ledgers/AC1/mutants/ holds 61 files (m01-m57 committed; m58-m61 written this round by ledgers/AC1/scripts/AC1-d-r10/make_r10.py). Gate output: /tmp/AC1-v10/AC1-d/mutate2.out. Alternatives: ledgers/AC1/scripts/AC1-d-r10/alts/ and alts_all/ (8 files), run by run_alts.sh. Scripts: ledgers/AC1/scripts/AC1-d-r10/ (run_suite.sh, run_alts.sh, make_r10.py, build_fragment.py, cards_numbers.py). Out-of-slice observations for the L01 and L02 slices: L02 misconceptions item 'Proposition 3.2 is a consequence of double entry' omits the hypotheses of Proposition 3.2; L01 problem set item 'The lab tests balance, integer amounts and known account names' does not mention the account-exists check Remark 2.2 places in the posting check. Not verified: the SEC or any external source (none cited); lesson-level prose outside cards was checked only where a card or a project claim cites it.",
    "summary": {},
}

mut_text = (ROOT / "ledgers/AC1/mutants").glob("*.py")
out = (pathlib.Path("/tmp/AC1-v10/AC1-d/mutate2.out")).read_text(encoding="utf-8")
killers = {}
for line in out.splitlines():
    m = re.match(r"KILLED (\S+?\.py): (.*?) -> (.*)$", line)
    if m:
        killers[m.group(1)] = (m.group(2), m.group(3))
mutants = []
for path in sorted((ROOT / "ledgers/AC1/mutants").glob("*.py")):
    desc, killed = killers.get(path.name, ("", ""))
    mid = path.name.split("_")[0]
    mutants.append({"id": mid, "description": desc or path.name, "file": f"ledgers/AC1/mutants/{path.name}", "killed_by": killed})
FRAG["mutants"] = mutants
counts = {}
for r in rows:
    counts[r["status"]] = counts.get(r["status"], 0) + 1
FRAG["summary"] = {"rows": len(rows), "PASS": counts.get("PASS", 0), "FAIL": counts.get("FAIL", 0),
                   "UNVERIFIABLE": counts.get("UNVERIFIABLE", 0), "mutants": len(mutants),
                   "mutants_killed": sum(1 for m in mutants if m["killed_by"])}
OUT.write_text(json.dumps(FRAG, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", OUT, FRAG["summary"])
