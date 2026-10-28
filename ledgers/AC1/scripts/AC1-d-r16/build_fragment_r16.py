"""Builds the round-16 AC1-d fragment from the round-15 fragment and this round's re-runs (verifier-written).

Usage: python3 -I build_fragment_r16.py <round15 fragment.json> <out fragment.json>
Carried rows keep their round-15 text behind a prefix naming the files that are byte-identical since c093bf5.
"""
import datetime
import json
import sys

src = json.load(open(sys.argv[1], encoding="utf-8"))
old = {r["id"]: r for r in src["rows"]}
CARRY_PREFIX = "Carried from round 15 ({files} byte-identical since the previous pin c093bf5): "
F_LESSONS = "course/modules/AC/AC1/L01.html to L08.html, index.html, tests/labs/AC1/*, references/*"
F_PROJ = "project.html outside lines 368 and 396"
F_GRADER = "grader/test_project.py outside the hunks at lines 1028-1029, 1057-1059 and 1069-1084"
F_CARDS = "cards.json entries other than AC1-c059 (the only cards.json hunk, lines 409-411)"
F_MUT = "ledgers/AC1/mutants/ files"

OUT_MUT = "out/mutants_r16.out"
OUT_REF = "out/ref_50.out"
OUT_COL = "out/collect_50.out"

# Re-verified in round 16: the subject was re-run, or it changed, or the round-15 row was not a PASS.
REV = {
    "proj-run-graders": (
        "Round 16 re-run: ledgers/AC1/scripts/AC1-d-r16/run_suite.sh on grader/reference.py, seeds 0 to 49 "
        "(run with QF_SEED, -W error, --assert=plain): 285 passed on all 50 seeds (" + OUT_REF + "). Grader and "
        "reference.py, instance.py, starter.py checked byte-identical to c093bf5 except test_project.py (the "
        "round-15 delta)."
    ),
    "proj-collect-count-176": (
        "Re-run: pytest --collect-only on grader/reference.py, seeds 0 to 49: '285 tests collected' on every seed ("
        + OUT_COL + "). project.html line 368 says 285 and the count is 285. Arithmetic: 277 + 4 (the 2100-02-29 "
        "entry of test_period_end_must_be_a_month_end, one per function) + 4 (test_every_function_accepts_a_century_"
        "month_end, one per function) = 285."
    ),
    "proj-local-suite-reference": (
        "Re-run with the page's flags (QF_SEED, pytest -q -p no:cacheprovider --assert=plain -W error "
        "test_project.py) on grader/reference.py: seed 0 '285 passed in 0.19s'; seed 17 '285 passed'. pytest 9.0.2 "
        "confirmed by pytest --version (local Python 3.14.8, not Pyodide)."
    ),
    "proj-pyodide-smoke": (
        "Re-run: tools/page_smoke.py --unit AC1 --pages project.html -> 'page_smoke AC1: PASS' (out/smoke_project.out); "
        "--pages project.html L01.html L02.html L03.html -> 'page_smoke AC1: PASS' (out/smoke_pages.out). The Pyodide "
        "runtime itself was not run."
    ),
    "proj-check-pages": "Re-run: tools/check_pages.py --all -> 'check_pages AC1: PASS' (out/check_pages.out), exit 0.",
    "proj-check-projects": "Re-run: tools/check_projects.py --all -> 'check_projects AC1: PASS' (out/check_projects.out), exit 0.",
    "proj-check-dag": "Re-run: tools/check_dag.py --all -> 'check_dag AC1: PASS' (out/check_dag.out), exit 0.",
    "proj-run-labs": "Re-run: tools/run_labs.py --unit AC1 -> 'run_labs AC1: PASS (11/11)' (out/run_labs.out), exit 0.",
    "proj-lab-twin-embed": (
        "Re-run: the three project twins under python -I -W error (tests/labs/AC1/lab-AC1-project-1.py, -2.py, -3.py) "
        "print the lines of the page's expected blocks (out/twins.out; Lab 1 block at project.html lines 245-253 "
        "matches its nine printed lines; Lab 2 block at line 341-343 matches its three lines; Lab 3 block at "
        "lines 513-518 matches its six lines)."
    ),
    "proj-labs-ruff": (
        "Re-run: .venv/bin/python -m ruff check . -> 'All checks passed!'; ruff format --check . -> '212 files already "
        "formatted' (out/ruff.out), both exit 0."
    ),
    "proj-mypy-gate": "Re-run: mypy --no-incremental -> 'Success: no issues found in 153 source files' (out/mypy.out), exit 0.",
    "proj-verify-refs": (
        "Re-run: tools/verify_refs.py --unit AC1 -> 'live re-verification of AC1: 2 of 560 entries, 0 problems' "
        "(out/vr_live_AC1.out); tools/verify_refs.py --offline -> 'offline integrity: 560 entries, 0 problems' "
        "(out/vr_offline.out). project.html line 534 (penman2013financial) is outside the hunks."
    ),
    "proj-hours": (
        "Re-checked: index.html line 29 data-hours-lessons=90; project.html line 33 data-hours-project=30. Time-budget "
        "rows 1+3+4+4+3+5+2+5+3 = 30, equal to the Total cell; hub 90 + project 30 = 120 (index.html eyebrow: 120 hours). "
        "The changed row (line 396) keeps its 2 hours. Pace not judged (architect ruling)."
    ),
    "proj-prose-banned": (
        "Re-scan of project.html, grader/test_project.py and cards.json for the BUILDER_RULES 1.2/1.3 strings (roughly "
        "half, about 6%, historically, TODO, TBD, lorem, ellipsis, for brevity, details omitted, beyond the scope, left as "
        "an exercise, you can add more, it is important to note, studies show, experts agree, it is well known, obviously, "
        "clearly): 0 matches (out/banned_scan.out). The new sentences on lines 368 and 396 and the new grader comments "
        "and test names contain none of the listed strings."
    ),
    "proj-alt-implementations": (
        "Round 16: six alternative correct statements.py files, run on seeds 0 to 49 (300 runs, all '285 passed'): "
        "alt_r15_a_leap_arithmetic_table, alt_r15_b_next_day_probe, alt_r15_c_sorted_ledger_bisect (round 15) and "
        "alt_r16_a_thirty_two_day_jump, alt_r16_b_isinstance_int_cents, alt_r16_c_counter_balances (round 16; "
        "ledgers/AC1/scripts/AC1-d-r16/mk_alts16.py). Output: out/alts_all_50.out."
    ),
    "proj-overconstraint-nonmapping": (
        "Re-run: test_post_raises_a_value_error (grader lines 690-691) with its parametrize list (lines 318-688, the "
        "round-15 citation 658-686 is a sub-range). No alternative in the six is rejected by a post or century test "
        "(out/alts_all_50.out). The witness of out/witness_fix_test_project.py also passes all six alternatives and the "
        "reference."
    ),
    "proj-mutants-set-killed": (
        "Re-run of all 143 files in ledgers/AC1/mutants/ on seeds 0 and 17 (out/mutants_r16.out): 143 of 143 fail on both "
        "seeds. The round-15 survivors v15_m01, v15_m02 and v15_m03 are now killed (4, 3 and 2 failures on seed 0). The "
        "set now also contains the two round-16 survivors v16_m01 and v16_m02 (rows proj-v16-post-2100-02-29-not-enforced "
        "and proj-v16-post-2000-02-29-not-enforced), which pass the grader on both seeds: the set row is not PASS."
    ),
    "proj-page-spec-carry": (
        "Re-verified: the month-end sentence of project.html line 366 (Constraints) 'Each of the three statement functions "
        "and the articulation check raises for a period end that is not a month end ... 2100-02-29 is not a date' is "
        "enforced for all four functions: 2100-02-29 is in the period-end list of test_period_end_must_be_a_month_end "
        "(grader line 1029, parametrized over the four calls), and 2000-02-29 and 2100-02-28 are accepted by all four "
        "(test_every_function_accepts_a_century_month_end, lines 1071-1084). The post sentence on the same line "
        "('post raises ... a date that is not ... a real calendar date') is not enforced for 2100-02-29: see "
        "proj-v16-post-2100-02-29-not-enforced."
    ),
    "proj-page-spec-carry-post-cases": (
        "Re-verified: the post-error list of test_post_raises_a_value_error (grader lines 318-688) has no date case of "
        "2100-02-29 and no date case for a leap day of a century year that post must accept; the only 29 February cases "
        "are 2023-02-29 (line 528) and the 2024 entries. The reference and six alternatives pass; see "
        "proj-v16-post-2100-02-29-not-enforced."
    ),
    "proj-no-expected-value-leak": (
        "Re-verified against the changed line 368: its sentence 'A failing check names the property that failed and never "
        "prints the expected value' is byte-identical. The helpers name the key and the property and print no expected "
        "value: _check_values messages (grader lines 224-234, e.g. 'does not follow the definition in the specification'); "
        "articulation messages name the gap key (lines 742, 849, 892, 967)."
    ),
    "proj-grader-carry": (
        "Re-verified the changed grader hunks: the 2100-02-29 list entry (line 1029), the corrected century comment "
        "(lines 1057-1059, now correct: SMALL has all entries in January 2024, so the 2100-02-28 balance is the January "
        "balance and the 2000-02-29 balance is zero), the century test body (lines 1061-1068, unchanged code), and the new "
        "test_every_function_accepts_a_century_month_end (lines 1071-1084). Witness: the reference passes all of them."
    ),
    "proj-line-368-grading-claims": (
        "Re-verified line 368 (now 285 checks, matched by collect-only on seeds 0 to 49). 'the month-end rule, including "
        "century years' is now enforced for all four functions (lines 1029, 1056-1068, 1071-1084). The 'posting rules and "
        "each named error, with their boundary cases' clause has no 2100-02-29 posting case: that part is the open row "
        "proj-v16-post-2100-02-29-not-enforced."
    ),
    "proj-page-lab-carry": (
        "Re-verified: the project lab blocks at project.html lines 56-253, 260-343 and 423-518 are unchanged, and the three "
        "twins print the expected lines (out/twins.out; run_labs 11/11)."
    ),
    "proj-cards-c001-c126-coverage": (
        "Carried from round 15 (" + F_CARDS + " and " + F_LESSONS + " byte-identical since the previous pin): "
        "the twenty-odd cards of this coverage row are unchanged; AC1-c059 is re-verified in cards-c059-grade-basis. "
        + "Round-15 evidence: " + old["proj-cards-c001-c126-coverage"]["evidence"]
    ),
    "cards-inventory-and-dupes": (
        "Re-run (Python, cards.json): 132 cards; 132 unique ids; 0 duplicate fronts; 0 duplicate backs; every card has "
        "id, lesson, front, back (and grade/basis where graded); lessons L01 16, L02 16, L03 18, L04 17, L05 14, L06 16, "
        "L07 14, L08 21."
    ),
    "cards-grades": (
        "Re-run (cards.json grade and basis fields): grade C 44 (all with basis), grade T 42 (41 without basis, 1 with "
        "basis: AC1-c059), 46 ungraded (no grade field, as with round 15). No graded card lacks its basis where BUILDER_RULES "
        "requires one (a C grade names its lab). AC1-c059 is now T with basis 'Corollary 2.3 (L04 Section 2); the expiry of "
        "each payment's shares (Problem P1)', both proved on the page (see cards-c059-grade-basis)."
    ),
    "cards-numbers-in-lessons": (
        "Re-run of the number scan (ledgers/AC1/scripts/AC1-d-r16/cards_numbers.py, out/cards_numbers.out): 132 cards. One "
        "token is not found as typed: AC1-c077 '5,000' in the back ('plus 5,000'). The lesson writes it as 5{,}000 in KaTeX "
        "(L06.html line 68, Definition 1.3: '(L_{t-1} rho + 5{,}000) / 10{,}000'); the number is in its own lesson. AC1-c059 "
        "has no numbers."
    ),
    "cards-labels-resolve": (
        "Re-run (ledgers/AC1/scripts/AC1-d-r16/cards_labels.py): 'checked 132 cards', no MISS line (out/cards_labels.out). "
        "Every Definition/Proposition/Theorem/Corollary/Remark label in a card resolves in its lesson."
    ),
    "cards-banned": "Re-scan of cards.json for the banned strings (out/banned_scan.out): 0 matches.",
    "cards-L04": (
        "Re-verified: AC1-c059 (changed) now checked against L04 Corollary 2.3 (section 2, line 114), the misconception "
        "(section 6, line 344) and Problem P1 (section 7, line 391 onward); AC1-c132 (lab number 7) from the round-15 check. "
        "The other L04 cards (c046 to c058, c060, c122) are byte-identical and carry their round-15 evidence."
    ),
    "cards-c059-c060-c070-c090": (
        "AC1-c059 re-verified (see cards-c059-grade-basis). AC1-c060, AC1-c070 and AC1-c090 are byte-identical since the "
        "previous pin: Carried from round 15 (cards.json entries c060, c070, c090 byte-identical since c093bf5): "
        + old["cards-c059-c060-c070-c090"]["evidence"]
    ),
    "cards-c059-grade-basis": (
        "AC1-c059 (L04) now reads 'No. Over the full life of a payment the two rules recognize the same total, so a "
        "difference that reverses later is not a difference in total profit (Corollary 2.3).' with grade T and basis "
        "'Corollary 2.3 (L04 Section 2); the expiry of each payment's shares (Problem P1)'. Checked: Corollary 2.3 (L04.html "
        "line 114, graded T, proof at line 120 says the cash and receivable terms cancel), the misconception at L04.html "
        "lines 344 (section 6, which says 'Over the full life of a payment the two rules recognize the same total, because "
        "the balance expires to zero'), and Problem P1 (line 391 onward) whose solution says the four shares sum to Q_s "
        "exactly and an expired payment contributes nothing. The card's basis therefore names what the page proves. "
        "The card has no number that needs a lab."
    ),
    "cards-c108-constraints": "Carried from round 15 (cards.json entries other than AC1-c059 byte-identical since c093bf5): " + old["cards-c108-constraints"]["evidence"],
    "cards-c129-c131-definition11-cites": "Carried from round 15 (cards.json entries other than AC1-c059 byte-identical since c093bf5): " + old["cards-c129-c131-definition11-cites"]["evidence"],
    "cards-c132-lab1-quarter7": "Carried from round 15 (cards.json entries other than AC1-c059 byte-identical since c093bf5): " + old["cards-c132-lab1-quarter7"]["evidence"],
    "cards-c001-c128-coverage-r15": (
        "Carried from round 15 (cards.json entries other than AC1-c059 byte-identical since c093bf5): "
        + old["cards-c001-c128-coverage-r15"]["evidence"]
        + " AC1-c059 re-verified in cards-c059-grade-basis."
    ),
    "proj-pytest-version-claim": (
        "Re-verified: project.html line 415 unchanged; pytest --version -> 'pytest 9.0.2' and python -c sys.version -> 3.14.8 "
        "locally. The Pyodide 314.0.7 runtime was not run in this round."
    ),
    "proj-l01-pytest-claim-line-415": (
        "Re-verified: project.html line 415 unchanged; pytest 9.0.2 confirmed locally (see proj-pytest-version-claim). "
        "The Pyodide runtime was not run."
    ),
    "proj-tests-labs-pytest": (
        "Re-run: pytest tests/test_labs.py tests/test_run_labs.py tests/test_page_smoke.py tests/test_page_checks.py -k AC1 "
        "-> exit 0 (out/pytest_labs.out)."
    ),
    "proj-starter-fails": (
        "Re-run: starter.py on seed 0 -> '283 failed, 2 passed' (the suite fails on the starter, as the page says; "
        "the two passing tests do not call a function the student implements)."
    ),
    "proj-r14-alternatives-new": (
        "Round 16 re-run of the round-14 and round-15 alternatives on seeds 0 to 49 (out/alts_all_50.out): all pass. "
        "The round-14 alternatives are carried in the same way as their round-15 check."
    ),
    "proj-r15-century-test-comment": (
        "Re-verified: the comment at grader lines 1057-1059 now says 'The 2100-02-28 balance is the January balance of "
        "SMALL; no entry is dated before 2024, so the 2000-02-29 balance is zero.' SMALL has seven entries, all dated "
        "2024-01-02 to 2024-01-31 (lines 246-254), so both statements are true; SMALL_JAN_BALANCE_SHEET (line 255) is the "
        "January balance, and the 2000-02-29 check asserts zeros (line 1063)."
    ),
    "proj-r15-mutant-m01-income-blind-leap": (
        "Re-run (out/mutants_r16.out): v15_m01_income_statement_blind_leap_year fails on seed 0 (4 failed) and seed 17 "
        "(4 failed). The 2100-02-29 entry in test_period_end_must_be_a_month_end (grader line 1029) now kills it."
    ),
    "proj-r15-mutant-m02-cash-flow-blind-leap": (
        "Re-run (out/mutants_r16.out): v15_m02_cash_flow_blind_leap_year fails on seed 0 (3 failed) and seed 17 (3 failed), "
        "killed by the same entry (line 1029)."
    ),
    "proj-r15-mutant-m03-articulation-blind-leap": (
        "Re-run (out/mutants_r16.out): v15_m03_articulation_blind_leap_year fails on seed 0 (2 failed) and seed 17 (2 failed), "
        "killed by the same entry (line 1029)."
    ),
    "proj-r15-line-366-century-rule-four-functions": (
        "Re-verified the month-end part of project.html line 366 (unchanged text): the rule is enforced for all four functions "
        "(see proj-page-spec-carry). The post part of the same sentence is not enforced: proj-v16-post-2100-02-29-not-enforced."
    ),
    "proj-r15-mutant-m04-balance-control": "Re-run (out/mutants_r16.out): v15_m04_balance_sheet_blind_leap_year fails on seeds 0 and 17 (4 and 4 failed).",
    "proj-r15-mutant-m05-depreciation-gap-sign": "Re-run (out/mutants_r16.out): v15_m05_depreciation_gap_sign_reversed fails on seeds 0 and 17 (1 and 1 failed).",
    "proj-r15-mutant-m06-dividends-paid-sign": "Re-run (out/mutants_r16.out): v15_m06_dividends_paid_sign_reversed fails on seeds 0 and 17 (23 and 18 failed).",
    "proj-r15-alts-a-b-c": (
        "Re-run: alt_r15_a_leap_arithmetic_table, alt_r15_b_next_day_probe, alt_r15_c_sorted_ledger_bisect on seeds 0 to 49 "
        "(out/alts_all_50.out): 150 of 150 runs '285 passed'."
    ),
    "proj-r14-mutant-m101": "Re-run (out/mutants_r16.out): m101_int32_amount_cap fails on seeds 0 and 17.",
    "proj-r14-mutant-m103": "Re-run (out/mutants_r16.out): m103_amount_rounded_to_whole_dollars fails on seeds 0 and 17.",
    "proj-r14-mutant-m102": "Re-run (out/mutants_r16.out): m102_century_blind_leap_year fails on seeds 0 and 17 (round-14 survivor, still killed).",
    "proj-r14-mutant-m104": "Re-run (out/mutants_r16.out): m104_leap_rule_without_400_rule fails on seeds 0 and 17 (round-14 survivor, still killed).",
}
MUT_ROWS = [r for r in old if (r.startswith("proj-mutant") or r.startswith("proj-mutants-")) and r not in REV]
for rid in MUT_ROWS:
    REV[rid] = (
        "Round 16 re-run of every file in ledgers/AC1/mutants/ on seeds 0 and 17 (" + OUT_MUT + "): the mutant(s) named by "
        "this row's id are killed on both seeds (" + rid + " in the table of the round-16 output); the 143 files are all killed."
    )

# Carried rows: their cited subject is byte-identical since c093bf5 (see the prefix for the files).
CARRY_FILES = {
    "proj-line-37-lede-seed": F_PROJ + ", and grader/instance.py",
    "proj-footer-nothing-leaves": F_PROJ,
    "proj-line-377-working-capital-terms": F_PROJ,
    "proj-line-378-missing-space": F_PROJ,
    "proj-balance-gap-sign-unenforced": F_PROJ,
    "proj-scope-sentence-line-352": F_PROJ,
    "proj-conventions-debit-balance-sentence": F_PROJ,
    "proj-page-ladder-browser-carry": F_PROJ,
    "proj-instances-carry": "grader/instance.py (and " + F_PROJ + ")",
    "proj-index-explain-prop32": F_LESSONS,
    "proj-l03-check6-prose": F_LESSONS,
    "proj-l03-intangible-paragraph": F_LESSONS,
    "proj-l01-delta-prose-out-of-slice": F_LESSONS,
    "proj-l02-omits-real-items": F_LESSONS,
    "proj-l03-def11-indirect-cite": F_LESSONS,
    "proj-lab-l03-comment-scope": F_LESSONS,
    "proj-l03-check6-depreciation-reference": F_LESSONS,
    "proj-r13-year-edge-tests": F_GRADER,
    "proj-r13-l01-prop32-hypothesis-v": F_LESSONS,
    "proj-r13-l02-lowest-cash-sentences": F_LESSONS,
    "proj-r13-l02-intangible-cite": F_LESSONS,
    "proj-r13-l03-def11-depreciation-cite": F_LESSONS,
    "proj-r13-cards-L02": F_CARDS + " and " + F_LESSONS,
    "proj-r14-line-398-wording": F_PROJ,
    "proj-r14-test-large-amount": F_GRADER + " (lines 309-313); project.html line 368 changed in its count only, and the "
    "clause cited ('an entry of 1,000,000,000,000 cents') is byte-identical",
    "cards-L01": F_CARDS + " and L01.html",
    "cards-c015": F_CARDS + " and L01.html",
    "cards-c007-enforced-at-posting": F_CARDS + " and L01.html",
    "cards-L01-claims-table-scope": F_LESSONS,
    "cards-c040-investing-scope": F_CARDS + " and L03.html",
    "cards-c124-financing-scope": F_CARDS + " and L03.html",
    "cards-c126-straight-line": F_CARDS + " and L03.html",
    "cards-c027-prop32-scope": F_CARDS + " and L02.html",
    "cards-c028-net-income-scope": F_CARDS + " and L02.html",
    "cards-c029-prop32-hypotheses": F_CARDS + " and L02.html",
    "cards-c032-activity-split": F_CARDS + " and L02.html",
    "cards-L02": F_CARDS + " and L02.html",
    "cards-L03": F_CARDS + " and L03.html",
    "cards-c033-definition11-scope": F_CARDS + " and L03.html",
    "cards-c039-prop22-scope": F_CARDS + " and L03.html",
    "cards-c042-thm51-scope": F_CARDS + " and L03.html",
    "cards-c038-wrong-schedule": F_CARDS + " and L03.html",
    "cards-L03-c123": F_CARDS + " and L03.html",
    "cards-L03-theorem-5-1-print-claim": F_CARDS + " and L03.html and tests/labs/AC1/lab-AC1-L03-1.py",
    "cards-L03-theorem-5-1-print-claim-hypotheses": F_CARDS + " and L03.html",
    "cards-c127-check2-not-independent": F_CARDS + " and L03.html",
    "cards-c128-lab-prints-four-of-five": F_CARDS + " and L03.html",
    "cards-L05": F_CARDS + " and L05.html",
    "cards-L06": F_CARDS + " and L06.html",
    "cards-L07": F_CARDS + " and L07.html",
    "cards-c098-citation": F_CARDS + " and L07.html",
    "cards-c102-equity-wording": F_CARDS + " and L07.html",
    "cards-L08": F_CARDS + " and L08.html",
    "cards-c109-scope": F_CARDS + " and L08.html",
    "cards-c008-wording": F_CARDS + " and L01.html",
    "cards-c057": F_CARDS + " and L04.html",
    "cards-c069": F_CARDS + " and L05.html",
    "cards-c071": F_CARDS + " and L05.html",
    "cards-c079": F_CARDS + " and L06.html",
    "cards-c087": F_CARDS + " and L06.html",
    "cards-c104": F_CARDS + " and L07.html",
    "cards-c052": F_CARDS + " and L04.html",
    "cards-c013-scope": F_CARDS + " and L01.html",
    "cards-c088-scope": F_CARDS + " and L06.html",
    "cards-c018-wording": F_CARDS + " and L02.html",
    "cards-no-open-r10-fail": F_CARDS,
    "cards-registry-cites": F_CARDS + " (no card has a registry cite field; AC1-c059 cites no key)",
    "proj-l01-pytest-claim-line-415": F_PROJ,
}
for rid in list(CARRY_FILES):
    assert rid in old, rid

rows = []
for r in src["rows"]:
    rid = r["id"]
    if rid in REV and REV[rid]:
        new = dict(r)
        new["evidence"] = REV[rid]
        new["status"] = "PASS"
        if rid == "proj-mutants-set-killed":
            new["status"] = "FAIL"
            new["fix"] = (
                "Kill v16_m01 and v16_m02 by the two additions in proj-v16-post-2100-02-29-not-enforced and "
                "proj-v16-post-2000-02-29-not-enforced; the witness file out/witness_fix_test_project.py does both and keeps "
                "the reference and six alternatives green."
            )
        elif rid == "proj-page-spec-carry-post-cases":
            new["status"] = "PASS"
        rows.append(new)
    elif rid in CARRY_FILES:
        assert r["status"] == "PASS", rid
        new = dict(r)
        new["evidence"] = CARRY_PREFIX.format(files=CARRY_FILES[rid]) + r["evidence"]
        rows.append(new)
    else:
        raise SystemExit(f"row {rid} has no decision (status {r['status']})")

# Rows that the round-15 fragment had as FAIL and are now PASS are in REV above (they were given their new text).
# Rows that stay as the round-15 record: check that every round-15 PASS row has a decision.
decided = {r["id"] for r in rows}
missing = [rid for rid in old if rid not in decided]
assert not missing, missing

NEW = [
    {
        "id": "proj-v16-post-2100-02-29-not-enforced",
        "check": "2.5-mutation (new survivor, round 16, student error) and 2.9-spec (post rule)",
        "location": "course/modules/AC/AC1/project.html line 366 (Constraints): post raises 'for a date that is not in the form YYYY-MM-DD or is not a real calendar date', and '2100-02-29 is not a date'; grader/test_project.py: the posting-error list (lines 318-688) and test_post_raises_a_value_error (lines 690-691); ledgers/AC1/mutants/v16_m01_post_accepts_2100_02_29_as_a_date.py",
        "status": "FAIL",
        "evidence": (
            "Student error: post checks transaction dates with a hand-written leap rule with no century rule (year % 4 == 0), "
            "so post accepts 2100-02-29 as a transaction date. The mutant is not equivalent: the reference's _iso_date would "
            "reject it, and the mutant replaces that check in post with its own (a first version that still called _iso_date "
            "was equivalent and was discarded). Run on the round-16 grader: 285 passed on seed 0 and 285 passed on seed 17 "
            "(out/new_mutants_r16_final.out), so it survives. The page says post raises for a date that is not a real calendar "
            "date and that 2100-02-29 is not a date (line 366); no test posts 2100-02-29 (grep of the grader: the only "
            "2100-02-29 use is balance_sheet at line 1068 and the period-end list at line 1029)."
        ),
        "fix": (
            "Add ('a date of 2100-02-29, which is not a real calendar date', [{**SMALL[0], 'date': '2100-02-29'}]) to the "
            "posting-error list before 'a date whose month is beyond twelve' (grader line 528 region). Witness: "
            "out/witness_fix_test_project.py; with it, v16_m01 fails on seeds 0 and 17 (1 failed each), and the reference "
            "(287 passed) and the six alternatives (287 passed each) stay green."
        ),
    },
    {
        "id": "proj-v16-post-2000-02-29-not-enforced",
        "check": "2.5-mutation (new survivor, round 16, student error) and 2.9-spec (post accepts real dates)",
        "location": "course/modules/AC/AC1/project.html line 366 (Constraints): the named post conditions and 'A year divisible by 4 is a leap year, except ... so 2000-02-29 is a month end'; grader/test_project.py (no post test on 2000-02-29; the only 2000-02-29 uses are the balance_sheet lines 1062-1065 and the new test at 1083); ledgers/AC1/mutants/v16_m02_post_rejects_2000_02_29_as_a_date.py",
        "status": "FAIL",
        "evidence": (
            "Student error: post checks transaction dates with a leap rule that has the century exception but no 400-year "
            "exception, so post rejects the real date 2000-02-29. Run on the round-16 grader: 285 passed on seed 0 and 285 "
            "passed on seed 17 (out/new_mutants_r16_final.out), so it survives. The named post conditions (line 366) do not "
            "include rejecting a real calendar date, and the page states 2000-02-29 is a real leap day and a month end. The "
            "grader never posts 2000-02-29: the century test (lines 1056-1068) and the acceptance test (lines 1071-1084) pass "
            "2000-02-29 only as a period end."
        ),
        "fix": (
            "Add test_a_century_leap_day_posts_as_a_real_date (witness in out/witness_fix_test_project.py, lines 1114-1118): "
            "post([_entry('2000-02-29', ...)]) must post and balance_sheet at 2000-02-29 must show the entry. With it, "
            "v16_m02 fails on seeds 0 and 17 (1 failed each) and the reference and six alternatives pass."
        ),
    },
    {
        "id": "proj-v16-mutant-m03-articulation-no-month-end-test",
        "check": "2.5-mutation (new student error, round 16) against the non-string rule of articulation_check",
        "location": "ledgers/AC1/mutants/v16_m03_articulation_check_skips_the_month_end_test.py; grader/test_project.py test_a_period_end_that_is_not_a_string_is_rejected (line 1040-1047)",
        "status": "PASS",
        "evidence": (
            "Student error: articulation_check does not validate period_end itself. Run on the round-16 grader: 3 failed, 282 "
            "passed on seed 0 and on seed 17 (out/new_mutants_r16_final.out). The three failures are "
            "test_a_period_end_that_is_not_a_string_is_rejected for 20240131, None and True (a TypeError from the "
            "previous-month step instead of ValueError; pytest -rf names them). Month-end strings are still rejected, because "
            "articulation_check calls balance_sheet(ledger, end), which runs the month-end check. So this mutant is killed by "
            "the non-string rule for articulation_check; it does not isolate the month-end test for articulation_check, which "
            "the reference also satisfies through balance_sheet."
        ),
    },
    {
        "id": "proj-v16-alternatives-r16",
        "check": "2.6-over-constraint (architect ruling b), round 16 alternatives",
        "location": "ledgers/AC1/scripts/AC1-d-r16/mk_alts16.py; grader/test_project.py (whole suite) on seeds 0 to 49",
        "status": "PASS",
        "evidence": (
            "Three new correct alternatives written this round: alt_r16_a (month end by a 32-day jump; first version had a "
            "bug, the rerun passes), alt_r16_b (amounts checked with type() and isinstance(int) instead of numbers.Integral), "
            "alt_r16_c (balances in a Counter). Each: 50 of 50 seeds '285 passed' (out/alts_all_50.out). No over-constraint "
            "found, including the new century test and the 2100-02-29 list entry."
        ),
    },
    {
        "id": "proj-v16-century-tests-four-functions",
        "check": "2.4-expected-values and 2.6-spec (century rule for all four functions)",
        "location": "grader/test_project.py lines 1029 (2100-02-29 in the list of test_period_end_must_be_a_month_end, four calls), lines 1071-1084 (test_every_function_accepts_a_century_month_end)",
        "status": "PASS",
        "evidence": (
            "Verified the new tests: the reference returns dicts for 2000-02-29 and 2100-02-28 from all four functions "
            "(285 passed on 50 seeds); each of the four functions rejects 2100-02-29 (the list runs over four calls). The six "
            "alternatives and the three round-15 mutants (v15_m01 to m03) now fail, so the tests are not vacuous."
        ),
    },
    {
        "id": "proj-v16-line-396-gap-key",
        "check": "2.9-prose (changed time-budget row)",
        "location": "course/modules/AC/AC1/project.html line 396 (Time budget, 'articulation_check: the four gaps')",
        "status": "PASS",
        "evidence": (
            "The changed sentence 'each gap is the difference of two named quantities, and a failing check reports the gap's "
            "key' is true for the suite: each articulation gap assertion names the gap key in its failure message (grader lines 742, "
            "849, 892 through _check_values, 967 'the articulation gap ... must be zero'). The row's hours value is 2 and "
            "unchanged. The round-15 text ('so a nonzero gap names the identity that fails') is replaced by the key statement."
        ),
    },
]
rows += NEW

mutants_old = []
for m in src["mutants"]:
    e = dict(m)
    e["killed_by"] = "seeds 0 and 17 (" + OUT_MUT + "): both fail (round 16 re-run)"
    mutants_old.append(e)
FX15 = [
    ("fx15_01_income_rejects_century_leap_day", "fx15 01 income statement rejects the century leap day"),
    ("fx15_02_cash_flow_rejects_2100_02_28", "fx15 02 cash flow rejects 2100-02-28"),
    ("fx15_03_post_refuses_empty_transaction_list", "fx15 03 post refuses an empty transaction list"),
    ("fx15_04_post_drops_repeated_entries", "fx15 04 post drops repeated entries"),
    ("fx15_05_amount_under_a_dollar_read_as_zero", "fx15 05 amount under a dollar read as zero"),
    ("fx15_06_boolean_amount_accepted", "fx15 06 boolean amount accepted"),
    ("fx15_07_integral_float_amount_accepted", "fx15 07 integral float amount accepted"),
    ("fx15_08_century_rule_collapsed_in_month_end", "fx15 08 century rule collapsed in month end"),
    ("fx15_09_net_equipment_adds_accumulated_depreciation", "fx15 09 net equipment adds accumulated depreciation"),
    ("fx15_10_receivables_sign_not_reversed", "fx15 10 receivables sign not reversed"),
]
known = {m["file"].split("/")[-1][:-3] for m in mutants_old}
for name, desc in FX15:
    if name not in known:
        mutants_old.append({
            "id": name,
            "description": desc,
            "file": "ledgers/AC1/mutants/" + name + ".py",
            "killed_by": "seeds 0 and 17 (" + OUT_MUT + "): both fail (round 16 re-run)",
        })
mutants = mutants_old
mutants.append({
    "id": "v16_m01_post_accepts_2100_02_29_as_a_date",
    "description": "v16 m01 post accepts 2100-02-29 as a transaction date (leap rule with no century rule in post's own date check)",
    "file": "ledgers/AC1/mutants/v16_m01_post_accepts_2100_02_29_as_a_date.py",
    "killed_by": "",
})
mutants.append({
    "id": "v16_m02_post_rejects_2000_02_29_as_a_date",
    "description": "v16 m02 post rejects 2000-02-29 as a transaction date (century exception without the 400-year exception in post)",
    "file": "ledgers/AC1/mutants/v16_m02_post_rejects_2000_02_29_as_a_date.py",
    "killed_by": "",
})
mutants.append({
    "id": "v16_m03_articulation_check_skips_the_month_end_test",
    "description": "v16 m03 articulation_check does not validate period_end itself (a non-string period end raises TypeError)",
    "file": "ledgers/AC1/mutants/v16_m03_articulation_check_skips_the_month_end_test.py",
    "killed_by": "seeds 0 and 17 (out/new_mutants_r16_final.out): 3 failed on each seed",
})

counts = {"PASS": 0, "FAIL": 0, "UNVERIFIABLE": 0}
for r in rows:
    counts[r["status"]] += 1
killed = sum(1 for m in mutants if m["killed_by"])
verdict = "PASS" if counts["FAIL"] == 0 and counts["UNVERIFIABLE"] == 0 and killed == len(mutants) else "FAIL"
frag = {
    "unit": "AC1",
    "slice": "AC1-d",
    "round": 16,
    "verifier": "Claude Haiku 5.5, independent verifier for AC1-d, round 16; did not build AC1; read the round-15 fragment as context and computed the delta c093bf5..c5daab2 on the slice (project.html line 368 and line 396; grader/test_project.py lines 1028-1029, 1057-1059, 1069-1084; cards.json entry AC1-c059; mutants fx15_01 to fx15_10 added by the fix commit)",
    "pin": "c5daab2 (detached worktree /tmp/verify16-AC1-d)",
    "base": "c093bf5 (round-15 pin); previous fragment /tmp/fanout-frags/AC1-d.round15.json",
    "checkout": "/tmp/verify16-AC1-d",
    "scratch": "/tmp/v16d/",
    "verified_at": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
    "verdict": verdict,
    "summary": {
        "rows": len(rows),
        "PASS": counts["PASS"],
        "FAIL": counts["FAIL"],
        "UNVERIFIABLE": counts["UNVERIFIABLE"],
        "mutants": len(mutants),
        "mutants_killed_seed0_and_seed17": killed,
    },
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "Delta c093bf5..c5daab2 on the slice: project.html line 368 (count 277 to 285) and line 396 (articulation row); "
        "grader/test_project.py: the 2100-02-29 entry (line 1029), the corrected century comment (1057-1059), and the new "
        "parametrized test_every_function_accepts_a_century_month_end (1071-1084); cards.json AC1-c059 (now grade T, basis "
        "Corollary 2.3 and Problem P1). Lessons, index, labs, references, the reference, instance and starter are byte-identical "
        "since c093bf5. Re-run this round: check_pages, check_dag, check_projects, run_labs (11/11), the three project twins "
        "under python -I -W error, page_smoke (project and L01-L03), ruff check and format, mypy --no-incremental, verify_refs "
        "(live AC1 and offline), the AC1 lab and page pytest subset, collect-only and full runs of the reference on seeds 0 to "
        "49 (285 each), six alternatives on seeds 0 to 49 (300 runs, all pass), the starter, all 143 mutants on seeds 0 and "
        "17 (143 of 143 killed), and the three round-16 mutants. FAIL: v16_m01 and v16_m02 survive because post's date rule "
        "is untested for 2100-02-29 and 2000-02-29 (rows proj-v16-post-2100-02-29-not-enforced and "
        "proj-v16-post-2000-02-29-not-enforced); the witness fix in out/witness_fix_test_project.py kills both and keeps the "
        "reference and six alternatives green. NOT CHECKED: the Pyodide 314.0.7 runtime itself (only local Python 3.14.8 and "
        "pytest 9.0.2); the live verify_refs covers only the two AC1 entries it re-reads; the 46 ungraded cards were not "
        "re-graded beyond their citations; the 126 unchanged cards and the lessons were not re-read line by line this round "
        "(carried from round 15 by the prefix rule, and checked this round only by scripts for numbers, labels, duplicates and "
        "banned strings); the mutant files in the round-15 fragment were re-run, not re-derived."
    ),
}
json.dump(frag, open(sys.argv[2], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("rows", len(rows), counts, "mutants", len(mutants), "killed", killed, "verdict", verdict)
