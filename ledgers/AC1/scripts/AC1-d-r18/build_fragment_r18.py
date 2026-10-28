"""Builds ledgers/AC1/AC1-d.json (round 18) from the round-17 fragment (context only) and this round's evidence.

Carried rows keep the round-17 evidence behind the prefix 'Carried from round 17 (<files> byte-identical since the
previous pin):'. Fresh rows carry round-18 evidence. Every round-17 row id is kept.
Usage: python3 -I build_fragment_r18.py <checkout> <round17 fragment> <out json>
"""

import json
import sys
from datetime import UTC, datetime
from pathlib import Path

CHECK, PREV, OUT = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
prev = json.loads(PREV.read_text(encoding="utf-8"))
prev_rows = {r["id"]: r for r in prev["rows"]}
S = "ledgers/AC1/scripts/AC1-d-r18/out/"

FRESH = {}  # id -> evidence (status PASS unless listed in FAILS)
CARRY = {}  # id -> files that are byte-identical

FRESH_EVIDENCE = {
    "proj-run-graders": f"Round 18 re-run on 7143726: tools/run_graders.py --unit AC1 --seeds 0-49 printed 'run_graders AC1: PASS (reference 50/50 seeds, slowest 0.3 s)' ({S}run_graders.out, exit 0); the starter fails the suite on every seed.",
    "proj-collect-count-176": f"Round 18: pytest --collect-only on the reference (statements.py = reference.py in a scratch folder, grader files copied) gives 310 tests for every seed 0-49 ({S}collect.out, 50 lines of '50 310 tests collected'); project.html line 368 says 310 and the count is 310.",
    "proj-local-suite-reference": f"Round 18: the reference copied to a scratch folder with test_project.py and instance.py, QF_SEED=0, pytest -q -p no:cacheprovider --assert=plain -W error: '310 passed in 0.22s' (run in /tmp/ac1-v/d18). project.html lines 412-415 give the command and 'Use Python 3.14 and pytest 9.0.2'; pytest 9.0.2 confirmed in .venv.",
    "proj-pyodide-smoke": f"Round 18: tools/page_smoke.py --unit AC1 --pages project printed 'in-browser grader: All 310 tests pass on seed 1604661054' and 'page_smoke modules/AC/AC1/project.html: PASS' ({S}page_smoke_project.out). The L01 to L03 lab pages part of this check is carried from round 17 (L01.html, L02.html, L03.html byte-identical since the previous pin).",
    "proj-check-pages": f"Round 18: tools/check_pages.py --all: 'check_pages AC1: PASS' ({S}check_pages.out, exit 0); covers project.html and cards.json (139 cards).",
    "proj-check-projects": f"Round 18: tools/check_projects.py --all: 'check_projects AC1: PASS' ({S}check_projects.out, exit 0).",
    "proj-check-dag": f"Round 18: tools/check_dag.py --all: 'check_dag AC1: PASS' ({S}check_dag.out, exit 0); project.html concept links resolve to L01-L03 definitions.",
    "proj-run-labs": f"Round 18: tools/run_labs.py --unit AC1: 'run_labs AC1: PASS (11/11)' ({S}run_labs.out, exit 0), including lab-AC1-project-1, -project-2 and -project-3.",
    "proj-lab-twin-embed": f"Round 18: the three twins tests/labs/AC1/lab-AC1-project-{{1,2,3}}.py run under python -I -W error (exit 0) and their output equals the page's pre.expected blocks (twins_compare.py, saved as {S}twins_compare.out: all three identical); run_labs passes (PASS 11/11).",
    "proj-labs-ruff": f"Round 18: ruff check and ruff format --check on course/modules/AC/AC1/grader and tests/labs/AC1: 'All checks passed!' and '15 files already formatted' ({S}ruff.out, exit 0).",
    "proj-mypy-gate": f"Round 18: .venv/bin/python -m mypy --no-incremental: 'Success: no issues found in 153 source files' ({S}mypy.out, exit 0).",
    "proj-verify-refs": f"Round 18: tools/verify_refs.py --unit AC1: 'live re-verification of AC1: 2 of 560 entries, 0 problems'; tools/verify_refs.py --offline: 'offline integrity: 560 entries, 0 problems' ({S}vr_live_AC1.out, {S}vr_offline.out). penman2013financial (project.html line 534, data-cite) is in references.json with status verified, Open Library URL and ISBN 9780078025310.",
    "proj-hours": f"Round 18: project.html data-hours-project=30 and the time-budget rows sum to 1+3+4+4+3+5+2+5+3 = 30; index.html data-hours-lessons=90 equals the sum of the eight lesson pages' data-hours (11+12+11+11+12+12+11+10 = 90); 90+30 = 120 equals curriculum.json hours for AC1. Hours not judged against the pace estimate (architect ruling).",
    "proj-prose-banned": f"Round 18: grep for roughly, about <number>, historically, typically, usually, generally, half, ellipsis, builder, verifier, round, REQUEST over project.html and cards.json: no banned phrase; the one 'built' hit (project.html line 352, 'cash flows built from net income') is a method description, not a process word.",
    "proj-alt-implementations": f"Round 18: alternative correct implementations pass the whole suite on seeds 0-49 with 0 failures: alt_r18_d_scratch.py (written from the page, not from the reference), alt_r18_b_next_day_line_zero_tests.py and alt_r18_c_sorted_early_exit.py ({S}alts_r18_new.out: 150 of 150 runs pass), and all earlier alternatives (alts_all: {S}alts_all_r18.out).",
    "proj-overconstraint-nonmapping": "Round 18: every case added to the test_post_raises_a_value_error parametrize list (grader/test_project.py lines 328, 438-449, 452-461, 486-497) maps to a named condition on project.html line 366: a slash-form date (date not in YYYY-MM-DD), a boolean False on the credit side (boolean amount), an account that is a number (account name not text), a line with a debit and a credit of unequal sizes ('a line with both a debit and a credit, of any sizes'). Alternative implementations pass them (proj-alt-implementations).",
    "proj-mutants-set-killed": f"Round 18: all 165 files in ledgers/AC1/mutants/ fail on seeds 0 and 17 ({S}mutants_r18.out for the 160 carried files, {S}new_mutants_r18.out for the five new ones). The round-17 survivors v17_m01 to v17_m03 are now killed. The sixth round-18 mutant (retained-gap sign) is equivalent and is in ledgers/AC1/equivalent/ with a proof.",
    "proj-mutants-new-r10-m58-m61": "Round 18 re-run: the mutant files listed in the round-10 row are in ledgers/AC1/mutants/ and fail on seeds 0 and 17 (" + S + "mutants_r18.out).",
    "proj-mutants-m01-m08": "Round 18 re-run: mutants m01 to m08 in ledgers/AC1/mutants/ each fail on seeds 0 and 17 (" + S + "mutants_r18.out).",
    "proj-mutants-m11-m20": "Round 18 re-run: mutants m11 to m20 in ledgers/AC1/mutants/ each fail on seeds 0 and 17 (" + S + "mutants_r18.out).",
    "proj-mutants-m21-m25": "Round 18 re-run: mutants m21 to m25 in ledgers/AC1/mutants/ each fail on seeds 0 and 17 (" + S + "mutants_r18.out).",
    "proj-mutants-m33-m38": "Round 18 re-run: mutants m33 to m38 in ledgers/AC1/mutants/ each fail on seeds 0 and 17 (" + S + "mutants_r18.out).",
    "proj-mutant-m09-articulation-zero": "Round 18 re-run: ledgers/AC1/mutants/m09_articulation_all_zero.py fails on seeds 0 and 17 (" + S + "mutants_r18.out).",
    "proj-mutant-m10-depreciation-gap": "Round 18 re-run: ledgers/AC1/mutants/m10_depreciation_gap_no_expense.py fails on seeds 0 and 17 (" + S + "mutants_r18.out).",
    "proj-mutant-m26-payables-sign": "Round 18 re-run: ledgers/AC1/mutants/ payables-sign mutant fails on seeds 0 and 17 (" + S + "mutants_r18.out).",
    "proj-mutant-m27-cogs-from-balance": "Round 18 re-run: ledgers/AC1/mutants/ cogs-from-balance mutant fails on seeds 0 and 17 (" + S + "mutants_r18.out).",
    "proj-mutant-m28-timestamp-date-accepted": "Round 18 re-run: ledgers/AC1/mutants/ timestamp-date mutant fails on seeds 0 and 17 (" + S + "mutants_r18.out).",
    "proj-mutant-m29-boolean-credit-accepted": "Round 18 re-run: ledgers/AC1/mutants/ boolean-credit mutant fails on seeds 0 and 17 (" + S + "mutants_r18.out).",
    "proj-mutant-m30-whitespace-date-accepted": "Round 18 re-run: ledgers/AC1/mutants/ whitespace-date mutant fails on seeds 0 and 17 (" + S + "mutants_r18.out).",
    "proj-mutant-m31-account-name-case-folded": "Round 18 re-run: ledgers/AC1/mutants/ case-folded account mutant fails on seeds 0 and 17 (" + S + "mutants_r18.out).",
    "proj-mutant-m32-retained-gap-sign": "Round 18 re-run: ledgers/AC1/mutants/ m32 retained-gap sign mutant fails on seeds 0 and 17 (" + S + "mutants_r18.out).",
    "proj-mutant-m39-account-name-whitespace-stripped": "Round 18 re-run: ledgers/AC1/mutants/ m39 fails on seeds 0 and 17 (" + S + "mutants_r18.out).",
    "proj-mutant-m40-credit-float-accepted": "Round 18 re-run: ledgers/AC1/mutants/ m40 fails on seeds 0 and 17 (" + S + "mutants_r18.out).",
    "proj-mutant-m41-week-date-accepted": "Round 18 re-run: ledgers/AC1/mutants/ m41 fails on seeds 0 and 17 (" + S + "mutants_r18.out).",
    "proj-mutant-m42-month-end-previous-length": "Round 18 re-run: ledgers/AC1/mutants/ m42 fails on seeds 0 and 17 (" + S + "mutants_r18.out).",
    "proj-mutant-m43-negative-credit-absolute": "Round 18 re-run: ledgers/AC1/mutants/ m43 fails on seeds 0 and 17 (" + S + "mutants_r18.out).",
    "proj-mutant-m44-unbalanced-one-direction": "Round 18 re-run: ledgers/AC1/mutants/ m44 fails on seeds 0 and 17 (" + S + "mutants_r18.out).",
    "proj-mutant-m45-negative-debit-clamped": "Round 18 re-run: ledgers/AC1/mutants/ m45 fails on seeds 0 and 17 (" + S + "mutants_r18.out).",
    "proj-mutant-m46-unpadded-date-accepted": "Round 18 re-run: ledgers/AC1/mutants/ m46 fails on seeds 0 and 17 (" + S + "mutants_r18.out).",
    "proj-mutant-m47-numeric-string-amount": "Round 18 re-run: ledgers/AC1/mutants/ m47 fails on seeds 0 and 17 (" + S + "mutants_r18.out).",
    "proj-mutants-new-r9-three-written": "Round 18 re-run: the three round-9 mutant files in ledgers/AC1/mutants/ fail on seeds 0 and 17 (" + S + "mutants_r18.out).",
    "proj-mutants-new-m26-m28": "Round 18 re-run: mutants m26 to m28 in ledgers/AC1/mutants/ fail on seeds 0 and 17 (" + S + "mutants_r18.out).",
    "proj-mutants-m62-m71-fixer": "Round 18 re-run: mutants m62 to m71 in ledgers/AC1/mutants/ fail on seeds 0 and 17 (" + S + "mutants_r18.out).",
    "proj-mutants-new-r11-m72-m75": "Round 18 re-run: mutants m72 to m75 in ledgers/AC1/mutants/ fail on seeds 0 and 17 (" + S + "mutants_r18.out).",
    "proj-page-spec-carry": "Round 18 read of project.html line 366 (Constraints, changed this round): each named condition is enforced by the reference (statements reference.py lines 34-90) and by a test in grader/test_project.py; the new clauses (account name not text, boolean on either side, a line with a debit and a credit of any sizes, no surrounding spaces) have tests at lines 328, 438-461, 486-497 and 1052-1073 (period-end list).",
    "proj-page-spec-carry-post-cases": "Round 18: test_post_raises_a_value_error parametrize list (grader/test_project.py lines 317-727, read in full) contains a case for each named condition on project.html line 366; the four round-17 survivors' cases are present.",
    "proj-no-expected-value-leak": "Round 18: project.html line 368 sentence 'A failing check names the property that failed and never prints the expected value' checked against _check_values (test_project.py lines 224-234: pytest.fail messages name the key and the property, no expected value) and the assert messages (fixed text).",
    "proj-grader-carry": "Round 18: grader/test_project.py read in full (1188 lines); changed hunks read: lines 328, 438-461, 486-497, 1005-1006, 1072, 1130-1152, 1155-1160; no expected value is printed by any failure message.",
    "proj-line-368-grading-claims": "Round 18: project.html line 368 ('collects 310 checks'; the coverage list; 'the count is 310 for each of the seeds 0 to 49'): 310 on seeds 0-49 (collect.out) and each listed boundary case exists in test_project.py (e.g. 1,000,000,000,000 cents at line 312, entries dated 1 January, 31 December and 29 February at lines 796-816).",
    "proj-line-37-lede-seed": "Round 18: project.html line 37 ('a 200-transaction ledger generated from the seed'): make_instance(seed) for seeds 0-49 gives 200 entries, all dated 2024 (script run in the round-18 transcript); test_project.py line 300 asserts 200.",
    "proj-page-lab-carry": "Round 18: the three project lab blocks on project.html (Lab 1, Lab 2, Lab 3) equal the twins' current output (see proj-lab-twin-embed); the Lab 1 numbers were re-derived by hand (22 postings, balance gaps 0, retained earnings 600,000 and 1,300,000, February net income 700,000, operating cash flow -700,000, ending cash 4,800,000); the Lab 3 numbers were re-derived (assets 7,870,000 = liabilities 2,250,000 + common stock 6,000,000 - retained earnings 380,000; investing -3,000,000; financing 850,000).",
    "proj-cards-c001-c126-coverage": "Round 18: cards.json has 139 cards c001 to c139, each lesson has cards (L01 16, L02 16, L03 18, L04 19, L05 14, L06 16, L07 18, L08 22, summing to 139), c060 changed this round and re-checked against L04 Proposition 3.1 and Remark 3.2.",
    "cards-inventory-and-dupes": "Round 18: cards.json 139 entries; ids unique; fronts unique (exact); near-duplicate scan (difflib ratio > 0.7 on fronts or backs, 40 pairs) shows distinct facts (e.g. rule A vs rule B, presentation 1 vs 2, debit vs credit).",
    "cards-grades": "Round 18: 92 cards carry a grade (C 50, T 42); 47 cards carry no grade and no basis (definitions and conventions), which check_pages allows; every grade-C card names a basis (check_pages: PASS).",
    "cards-numbers-in-lessons": "Round 18 script: every number in every card back appears verbatim in its own lesson's text (tag-stripped, script run), except 5,000 on card AC1-c077, which the lesson writes as 5{,}000 in LaTeX (L06.html line 68 and line 357).",
    "cards-labels-resolve": "Round 18: labels cited by the cards of the changed lessons (L04 Proposition 2.2 and Definition 2.2, Proposition 3.1, Remark 3.2, Corollary 2.3, Problem P1; L05 Proposition 1.4, 2.1, 2.3, P3; L06 Definition 1.1 'in arrears'; L07 Definition 1.2 (ii)-(v); L08 Definition 1.1, Theorem 2.1 (a)-(d), Example 2.2) exist in their own lesson; labels in the L01 to L03 cards are carried.",
    "cards-registry-cites": "Round 18: check_pages (cards.json: 'cites unknown key' test) PASS; no card cites a registry key in the changed cards.",
    "cards-c057": "Round 18: AC1-c057 (L04): 'This lesson does not say. It cites no primary text ... (Remark 1.2, Section 4)'; L04 Remark 1.2 (line 62-63, 'The lesson states no rule of either framework') and Section 4 still say so after the round-18 edits.",
    "cards-L04": "Round 18 FAIL: the L04 cards were checked against the changed L04 text. c052, c053 and c058 overstate the scope of L04 Proposition 2.1 or Proposition 2.2 (see cards-c052, cards-c053-prop22-assumptions, cards-c058-two-rules-scope). Other L04 cards (c046-c051, c054-c057, c059, c060, c122, c132-c134) were checked against the current text and pass.",
    "cards-L05": "Round 18: the L05 cards (c061-c074) checked against the changed Definition 1.3 (P an integer), Proposition 1.4, Proposition 2.1 (now 'Under Definition 1.3 and convention 1') and the unchanged paragraph and P3. c066 and c067 state the results in the setting of Definition 1.3, where P is an integer, so they pass (see cards-c066-c067-definition-1-3-setting).",
    "cards-L06": "Round 18: the L06 cards (c075-c090) checked against the changed Definition 1.1 ('annual contractual payments of P cents each, paid at the end of each year'): c075's 'n annual payments in arrears' still holds; numbers checked against the Lab 1 output and the Definition 1.3 text (5,000 and 10,000, L06.html line 68).",
    "cards-L07": "Round 18: the L07 cards (c091-c104) checked against the changed why-it-matters paragraph and the MC option; c135 (Definition 1.2 (ii), 'No award is forfeited') still matches the lesson's model statement.",
    "cards-L08": "Round 18: the L08 cards (c105-c121, c125, c129-c131, c139) checked against the changed why-it-matters paragraph (P_t defined in Section 2) and the changed interpretation paragraph (years 1 and 2: CT below TE by DE, verified against the lab table: year 1 DE 1,961.40 = TE 10,131.24 - CT 8,169.84; year 2 DE 980.70 = 17,657.85 - 16,677.15). Example 2.2 numbers ($6,300, $10,500, $4,200) confirmed at L08.html lines 100 and 223-225.",
    "cards-c059-c060-c070-c090": "Round 18: AC1-c060 re-checked against the changed L04 misconception and Proposition 3.1 ('with their sum unchanged'; the lab prints 3,319,293 as interest_moved_total_cents); c059 (Corollary 2.3, P1) unchanged; c070 and c090 check against the Lab 1 outputs (L05, L06, unchanged).",
    "cards-c132-lab1-quarter7": "Round 18: AC1-c132 '-4,974,286 cents ... minus the unexpired part of the quarter-7 purchase of 6,632,381 cents, which has only its first share expensed': the lab prints cum_difference_cents -4974286, prepaid_paid 6632381 at q7; 6,632,381 - 1,658,095 = 4,974,286; the changed L04 misconception (line 345) gives the same arithmetic.",
    "cards-c001-c128-coverage-r15": "Round 18: cards.json coverage: 139 cards (c001-c139) against L01-L08, each lesson represented (L01 16, L02 16, L03 18, L04 19, L05 14, L06 16, L07 18, L08 22 cards).",
    "proj-v16-post-2100-02-29-not-enforced": "Round 18: project.html line 366 ('2100-02-29 is not a date'; post raises for a date that is not a real calendar date): the reference raises for 2100-02-29 (date.fromisoformat); test at test_project.py line 566 and the v16_m01 equivalence proof (ledgers/AC1/equivalent/v16_m01.proof.md) hold.",
    "proj-v16-post-2000-02-29-not-enforced": "Round 18: project.html line 366 ('2000-02-29 is a month end'): test_a_century_leap_day_posts_as_a_real_date (test_project.py lines 1096-1106) and test_every_function_accepts_a_century_month_end (lines 1133-1136) pass on the reference.",
    "proj-v16-mutant-m03-articulation-no-month-end-test": "Round 18 re-run: ledgers/AC1/mutants/v16_m03_articulation_check_skips_the_month_end_test.py fails on seeds 0 and 17 (" + S + "mutants_r18.out).",
    "proj-v16-alternatives-r16": "Round 18: the round-16 alternatives are in ledgers/AC1/scripts/AC1-d-r16/ and their earlier copies in AC1-d-r10 to r15; all pass seeds 0-49 (" + S + "alts_all_r18.out).",
    "proj-v16-century-tests-four-functions": "Round 18: test_every_function_accepts_a_century_month_end (test_project.py lines 1124-1136) runs four functions on 2000-02-29, 2100-02-28, 2000-03-31 and 2100-03-31; test_period_end_must_be_a_month_end lists 2100-02-29 (line 1068); both pass on the reference.",
    "proj-v17-slash-date-accepted": "Round 18 re-run: v17_m01 (slash dates normalised) is killed on seeds 0 and 17 by the new case at test_project.py line 328 ('a date with slashes in the form YYYY/MM/DD') (" + S + "mutants_r18.out).",
    "proj-v17-line-both-sides-unequal-accepted": "Round 18 re-run: v17_m03 (unequal debit and credit line accepted) is killed by the new case at test_project.py lines 486-497 ('a line with a debit and a credit of unequal sizes, in an entry that balances') (" + S + "mutants_r18.out).",
    "proj-v17-previous-month-end-century-leap": "Round 18 re-run: v17_m02 (previous-month-end leap rule without the century rule) is killed by test_a_month_after_a_century_february_counts_only_its_own_entries (test_project.py lines 1139-1152) (" + S + "mutants_r18.out).",
    "proj-v17-alternatives-r17": f"Round 18: the three round-17 alternatives (alt_r17_a, alt_r17_b, alt_r17_c) pass the whole suite on seeds 0-49 (" + S + "alts_all_r18.out).",
    "proj-v17-mutants-prior-147-rerun": "Round 18: every file in ledgers/AC1/mutants/ (160 carried plus 5 new) fails on seeds 0 and 17 (" + S + "mutants_r18.out, " + S + "new_mutants_r18.out).",
    "proj-v17-collect-and-count-line-368": "Round 18: 310 collected on seeds 0-49 (collect.out); project.html line 368 says 310.",
    "cards-v17-changed-and-new-count": "Round 18: cards.json has 139 cards; c060 changed (round 18) and re-checked; c050, c051, c095, c111 unchanged since round 17.",
    "proj-starter-fails": f"Round 18: tools/run_graders.py (" + S + "run_graders.out) runs the starter on seeds 0-49 and requires it to fail the suite; starter.py is byte-identical to round 17 (every function raises NotImplementedError).",
    "proj-pytest-version-claim": "Round 18: .venv pytest is 9.0.2 (pytest.__version__); Pyodide 314.0.7 is pinned in tools/vendor_spec.yaml line 54; project.html line 415 matches.",
    "proj-l01-pytest-claim-line-415": "Round 18: project.html line 415 ('Use Python 3.14 and pytest 9.0.2 ... Pyodide 314.0.7') matches the local .venv (Python 3.14.8, pytest 9.0.2) and tools/vendor_spec.yaml.",
    "proj-tests-labs-pytest": f"Round 18: .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_run_labs.py tests/test_labs.py tests/test_page_checks.py: exit 0 ({S}pytest_labs.out).",
    "proj-mutants-new-r12-m86-m89": "Round 18 re-run: mutants m86 to m89 in ledgers/AC1/mutants/ fail on seeds 0 and 17 (" + S + "mutants_r18.out).",
    "proj-mutant-m89-first-day-entry-rejected": "Round 18 re-run: ledgers/AC1/mutants/m89_first_day_entry_rejected.py fails on seeds 0 and 17 (" + S + "mutants_r18.out).",
    "proj-mutant-m90-amount-cap-survives": "Round 18 re-run: ledgers/AC1/mutants/ m90 (amount cap) fails on seeds 0 and 17 (" + S + "mutants_r18.out).",
    "proj-mutants-new-r13-m91-m93": "Round 18 re-run: mutants m91 to m93 in ledgers/AC1/mutants/ fail on seeds 0 and 17 (" + S + "mutants_r18.out).",
    "proj-mutants-fx01-fx10": "Round 18 re-run: mutants fx01 to fx10 in ledgers/AC1/mutants/ fail on seeds 0 and 17 (" + S + "mutants_r18.out).",
        "proj-r14-mutant-m101": "Round 18 re-run: ledgers/AC1/mutants/m101_int32_amount_cap.py fails on seeds 0 and 17 (" + S + "mutants_r18.out).",
    "proj-r14-mutant-m103": "Round 18 re-run: ledgers/AC1/mutants/m103_amount_rounded_to_whole_dollars.py fails on seeds 0 and 17 (" + S + "mutants_r18.out).",
    "proj-r14-mutant-m102": "Round 18 re-run: ledgers/AC1/mutants/m102_century_blind_leap_year.py fails on seeds 0 and 17 (" + S + "mutants_r18.out).",
    "proj-r14-mutant-m104": "Round 18 re-run: ledgers/AC1/mutants/m104_leap_rule_without_400_rule.py fails on seeds 0 and 17 (" + S + "mutants_r18.out).",
    "proj-r14-alternatives-new": "Round 18: the round-14 alternatives (ledgers/AC1/scripts/AC1-d-r14/alts/) pass seeds 0-49 (" + S + "alts_all_r18.out).",
    "proj-r15-mutant-m01-income-blind-leap": "Round 18 re-run: ledgers/AC1/mutants/v15_m01_income_statement_blind_leap_year.py fails on seeds 0 and 17 (" + S + "mutants_r18.out).",
    "proj-r15-mutant-m02-cash-flow-blind-leap": "Round 18 re-run: ledgers/AC1/mutants/v15_m02_cash_flow_blind_leap_year.py fails on seeds 0 and 17 (" + S + "mutants_r18.out).",
    "proj-r15-mutant-m03-articulation-blind-leap": "Round 18 re-run: ledgers/AC1/mutants/v15_m03_articulation_blind_leap_year.py fails on seeds 0 and 17 (" + S + "mutants_r18.out).",
    "proj-r15-line-366-century-rule-four-functions": "Round 18: project.html line 366 states the 400-year rule and names 2000-02-29 (month end), 2100-02-28 (month end), 2100-02-29 (not a date); test_a_century_year_follows_the_400_year_rule (lines 1109-1121) and test_every_function_accepts_a_century_month_end (lines 1133-1136) check these on all four functions.",
    "proj-r15-mutant-m04-balance-control": "Round 18 re-run: ledgers/AC1/mutants/v15_m04_balance_sheet_blind_leap_year.py fails on seeds 0 and 17 (" + S + "mutants_r18.out).",
    "proj-r15-mutant-m05-depreciation-gap-sign": "Round 18 re-run: ledgers/AC1/mutants/v15_m05_depreciation_gap_sign_reversed.py fails on seeds 0 and 17 (" + S + "mutants_r18.out).",
    "proj-r15-mutant-m06-dividends-paid-sign": "Round 18 re-run: ledgers/AC1/mutants/v15_m06_dividends_paid_sign_reversed.py fails on seeds 0 and 17 (" + S + "mutants_r18.out).",
    "proj-r15-alts-a-b-c": "Round 18: alternatives under ledgers/AC1/scripts/AC1-d-r15/alts/ (alt_r15_a, alt_r15_b, alt_r15_c) pass seeds 0-49 (" + S + "alts_all_r18.out).",
        "cards-banned": "Round 18: grep over cards.json for roughly, about <number>, historically, typically, usually, generally, half, ellipsis, builder, verifier, REQUEST and process 'round' words: no hit. The six 'round' matches are the words rounds, rounding and rounded in method descriptions (AC1-c076, c077, c078, c082, c090, c133 and the L04 rule-B card), none a process word.",
    "cards-c059-grade-basis": "Round 18: AC1-c059 (grade T) checked against L04 Corollary 2.3 (unchanged) and Problem P1 (unchanged): pass.",
}

CARRY_FILES = {
    "proj-footer-nothing-leaves": "course/modules/AC/AC1/project.html line 549",
    "proj-line-377-working-capital-terms": "project.html line 377",
    "proj-line-378-missing-space": "project.html lines 378-379",
    "proj-balance-gap-sign-unenforced": "project.html line 378",
    "proj-scope-sentence-line-352": "project.html line 352",
    "proj-conventions-debit-balance-sentence": "project.html line 373",
    "proj-page-ladder-browser-carry": "project.html lines 40-47, 51-52, 406, 414, 533, 548",
    "proj-instances-carry": "grader/instance.py",
    "proj-v16-line-396-gap-key": "project.html line 396",
    "proj-r14-line-398-wording": "project.html line 398",
    "proj-r14-test-large-amount": "grader/test_project.py lines 309-315",
    "proj-r15-century-test-comment": "grader/test_project.py test_a_century_year_follows_the_400_year_rule (its comment and body)",
    "proj-r13-year-edge-tests": "grader/test_project.py lines 796-816",
    "proj-v17-equivalent-v16-m01-proof": "ledgers/AC1/equivalent/v16_m01.proof.md and the reference",
    "cards-no-open-r10-fail": "cards.json entries other than AC1-c060",
    "cards-c015": "cards.json AC1-c015; L01.html",
    "cards-L01": "cards.json c001-c016; L01.html",
    "cards-c007-enforced-at-posting": "cards.json AC1-c007; L01.html",
    "cards-L01-claims-table-scope": "L01.html section 8",
    "cards-c013-scope": "cards.json AC1-c013; L01.html",
    "cards-c008-wording": "cards.json AC1-c008; L01.html",
    "cards-c018-wording": "cards.json AC1-c018; L02.html",
    "cards-c040-investing-scope": "cards.json AC1-c040; L03.html",
    "cards-c124-financing-scope": "cards.json AC1-c124; L03.html",
    "cards-c126-straight-line": "cards.json AC1-c126; L03.html",
    "cards-c027-prop32-scope": "cards.json AC1-c027; L02.html",
    "cards-c028-net-income-scope": "cards.json AC1-c028; L02.html",
    "cards-c029-prop32-hypotheses": "cards.json AC1-c029; L02.html",
    "cards-c032-activity-split": "cards.json AC1-c032; L02.html",
    "cards-L02": "cards.json c017-c032; L02.html",
    "cards-L03": "cards.json c033-c039, c041-c045, c123, c126, c127, c128; L03.html",
    "cards-c033-definition11-scope": "cards.json AC1-c033; L03.html",
    "cards-c039-prop22-scope": "cards.json AC1-c039; L03.html",
    "cards-c042-thm51-scope": "cards.json AC1-c042; L03.html",
    "cards-c038-wrong-schedule": "cards.json AC1-c038; L03.html",
    "cards-L03-c123": "cards.json AC1-c123; L03.html",
    "cards-L03-theorem-5-1-print-claim": "L03.html Theorem 5.1 paragraph; tests/labs/AC1/lab-AC1-L03-1.py",
    "cards-L03-theorem-5-1-print-claim-hypotheses": "L03.html Theorem 5.1 hypotheses",
    "cards-c127-check2-not-independent": "cards.json AC1-c127; L03.html",
    "cards-c128-lab-prints-four-of-five": "cards.json AC1-c128; L03.html",
    "cards-c098-citation": "cards.json AC1-c098; L07.html Theorem 2.1 and Corollary 2.2",
    "cards-c102-equity-wording": "cards.json AC1-c102; L07.html Corollary 2.2",
    "cards-c109-scope": "cards.json AC1-c109; L08.html Definition 1.2",
    "cards-c108-constraints": "cards.json AC1-c108; L08.html Definition 1.1",
    "cards-c129-c131-definition11-cites": "cards.json AC1-c129 to c131; L08.html Definition 1.1",
    "cards-c069": "cards.json AC1-c069; L05.html Section 2 paragraph and P3",
    "cards-c071": "cards.json AC1-c071; L05.html Section 3",
    "cards-c079": "cards.json AC1-c079; L06.html Definition 1.4",
    "cards-c087": "cards.json AC1-c087; L06.html Section 3",
    "cards-c104": "cards.json AC1-c104; L07.html Definition 1.1 and Theorem 1.3",
    "cards-c088-scope": "cards.json AC1-c088; L06.html Lab 1 and Proposition 2.3",
    "cards-c059-grade-basis": "cards.json AC1-c059; L04.html Corollary 2.3 and P1",
    "proj-index-explain-prop32": "course/modules/AC/AC1/index.html line 141",
    "proj-l03-check6-prose": "L03.html Check 6 interpretation paragraph",
    "proj-l03-intangible-paragraph": "L03.html intangible-purchase paragraph",
    "proj-l01-delta-prose-out-of-slice": "L01.html line 48 and line 559",
    "proj-l02-omits-real-items": "L02.html line 552",
    "proj-l03-def11-indirect-cite": "L03.html Definitions 1.1 and 2.1",
    "proj-lab-l03-comment-scope": "tests/labs/AC1/lab-AC1-L03-1.py lines 606-621 and L03.html lines 606-621",
    "proj-l03-check6-depreciation-reference": "L03.html interpretation paragraph",
    "proj-r13-l01-prop32-hypothesis-v": "L01.html line 388",
    "proj-r13-l02-lowest-cash-sentences": "L02.html lines 133 and 535",
    "proj-r13-l02-intangible-cite": "L02.html line 552",
    "proj-r13-l03-def11-depreciation-cite": "L03.html lines 57 and 61",
    "proj-r13-cards-L02": "cards.json AC1-c025, AC1-c026; L02.html lab output",
}

NEW_ROWS = [
    {"id": "cards-c053-prop22-assumptions", "check": "2.2-cards-against-lesson (hypotheses)",
     "location": "course/modules/AC/AC1/cards.json AC1-c053; course/modules/AC/AC1/L04.html Proposition 2.2 (line 97) and Definition 2.2 (line 92)",
     "status": "FAIL",
     "evidence": "Proposition 2.2 as now written (L04.html line 97) starts 'Under the assumptions of Definition 2.2 (zero opening balances, no equity contributions, no distributions, and each credit sale collected one quarter later)'. AC1-c053 (grade T) gives 'Both hold exactly in integer cents (Proposition 2.2)' with none of these assumptions; the identities are false without them (opening cash or receivables would enter one side only).",
     "fix": "Add the assumptions to the card back: 'Under the assumptions of Definition 2.2 (zero opening balances, no equity contributions, no distributions, each credit sale collected one quarter later): under rule A, cash plus receivables equals cumulative net income; under rule B, cash plus receivables plus the unexpired prepaid balance equals it (Proposition 2.2).'"},
    {"id": "cards-c058-two-rules-scope", "check": "2.2-cards-against-lesson (scope)",
     "location": "course/modules/AC/AC1/cards.json AC1-c058; course/modules/AC/AC1/L04.html misconception 1 (line 341)",
     "status": "FAIL",
     "evidence": "AC1-c058 back: 'Cash is the same under two recognition rules applied to the same payments (Proposition 2.1).' The changed misconception answer in L04.html line 341 says 'Under the two recognition rules of this lesson, cash is the same when both rules face the same payments and receipts (Proposition 2.1).' The card drops the 'of this lesson' scope that the lesson now states.",
     "fix": "Change the back to 'Under the two recognition rules of this lesson, cash is the same when both rules face the same payments and receipts (Proposition 2.1)' and keep the rest."},
    {"id": "cards-c066-c067-definition-1-3-setting", "check": "2.2-cards-against-lesson (hypotheses, round-18 edit)",
     "location": "course/modules/AC/AC1/cards.json AC1-c066, AC1-c067; course/modules/AC/AC1/L05.html Definition 1.3 (line 67-70), Proposition 1.4 (line 73), Proposition 2.1 (line 96)",
     "status": "PASS",
     "evidence": "Proposition 1.4 and Proposition 2.1 now name Definition 1.3 (L05.html lines 73 and 96). Definition 1.3 (line 70) states that 'the transaction price be the integer P in cents', and L05.html line 58 says the price is 'an integer number of cents defined in Definition 1.3'. The card questions are asked in that setting, so 'Yes' (non-negative integers that sum exactly to the price; cumulative revenue equals the price under both conventions) is correct as written. Checked by reading the three passages; no card change needed."},
    {"id": "cards-c060-round18-text", "check": "2.2-cards-against-lesson (changed card)",
     "location": "course/modules/AC/AC1/cards.json AC1-c060 (back changed this round); course/modules/AC/AC1/L04.html Proposition 3.1 (line 304) and Remark 3.2 (line 314)",
     "status": "PASS",
     "evidence": "The new back 'Operating and financing cash flow can change by the same amount in opposite directions, with their sum unchanged (Proposition 3.1). In Lab 1 that amount is 3,319,293 cents.' matches Proposition 3.1 (CFO2 = CFO1 + I, CFF2 = CFF1 - I, sum unchanged) and the lab's printed interest_moved_total_cents 3319293 (lab run, scripts/AC1-d-r18/out and the twin output). Grade C, basis 'Lab 1 (SIMULATED)' is the lab."},
    {"id": "proj-r18-student-mutants-m01-m06", "check": "2.5-mutation (new student errors, round 18)",
     "location": "ledgers/AC1/mutants/v18_m02 to v18_m06 (five killed); ledgers/AC1/equivalent/v18_m01 (equivalent, proof row proj-r18-equivalent-v18-m01)",
     "status": "PASS",
     "evidence": "Six new student-error mutants written from the reference by exact text replacement (scripts/AC1-d-r18/mk_r18.py): m01 retained-gap sign reversed (equivalent); m02 cash-flow add-back taken as the change in accumulated depreciation (killed: 28 of 310 fail on seed 0, 48 on seed 17); m03 date round trip dropped so ISO week dates pass (killed: the ISO-week case fails); m04 previous month end stepped back 30 days (killed: 66 fail on each seed); m05 unequal debit and credit line accepted (killed: the case at test_project.py lines 486-497 fails); m06 balance-through excludes entries on the period end (killed: 54 and 57 fail). Output: scripts/AC1-d-r18/out/new_mutants_r18.out."},
    {"id": "proj-r18-equivalent-v18-m01", "check": "2.5-mutation (equivalence proof)",
     "location": "ledgers/AC1/equivalent/v18_m01_retained_earnings_gap_sign_reversed.py and v18_m01.proof.md",
     "status": "PASS",
     "evidence": "Proof in ledgers/AC1/equivalent/v18_m01.proof.md: the change in retained earnings is identically net income plus dividends paid for every ledger, so the retained-earnings gap is 0 whatever the sign. The mutant passes all 310 checks on seeds 0 and 17 (scripts/AC1-d-r18/out/new_mutants_r18.out)."},
    {"id": "proj-r18-alternatives-d-b-c", "check": "2.5-alternatives (over-constraint, round 18)",
     "location": "ledgers/AC1/scripts/AC1-d-r18/alts/ (alt_r18_d_scratch.py, alt_r18_b_next_day_line_zero_tests.py, alt_r18_c_sorted_early_exit.py)",
     "status": "PASS",
     "evidence": "Alternative D is written from the page's Constraints and Conventions (strptime with strftime round trip, last day from the next month's first day, list ledger, balances summed on demand) and passes 310 of 310 on seeds 0-49; alternatives B and C pass 310 on seeds 0-49 (scripts/AC1-d-r18/out/alts_all_r18.out and the per-seed runs). All 29 earlier alternatives in ledgers/AC1/scripts/*/alts* pass seeds 0-49 with 0 failures (alts_all_r18.out, ALTS_DONE)."},
]


def mutant_entries():
    out = []
    mdir = CHECK / "ledgers" / "AC1" / "mutants"
    for path in sorted(mdir.glob("*.py")):
        stem = path.stem
        src = "new_mutants_r18.out" if stem.startswith("v18_") else "mutants_r18.out"
        out.append({
            "id": stem,
            "description": stem.replace("_", " "),
            "file": f"ledgers/AC1/mutants/{path.name}",
            "killed_by": f"seeds 0 and 17: both fail (scripts/AC1-d-r18/out/{src})",
        })
    return out


rows = []
for rid in [r["id"] for r in prev["rows"]]:
    if rid in FRESH_EVIDENCE and rid != "cards-L04":
        base = prev_rows[rid]
        rows.append({"id": rid, "check": base["check"], "location": base["location"], "status": "PASS",
                     "evidence": FRESH_EVIDENCE[rid]})
    elif rid in CARRY_FILES:
        base = prev_rows[rid]
        rows.append({"id": rid, "check": base["check"], "location": base["location"], "status": "PASS",
                     "evidence": f"Carried from round 17 ({CARRY_FILES[rid]} byte-identical since the previous pin): "
                                 + base["evidence"]})
    elif rid == "cards-L04":
        base = prev_rows[rid]
        rows.append({"id": rid, "check": base["check"], "location": base["location"], "status": "FAIL",
                     "evidence": FRESH_EVIDENCE[rid],
                     "fix": "Apply the three card fixes in cards-c052, cards-c053-prop22-assumptions and cards-c058-two-rules-scope."})
    elif rid == "cards-c052":
        base = prev_rows[rid]
        rows.append({"id": rid, "check": base["check"], "location": "course/modules/AC/AC1/cards.json AC1-c052; L04.html Proposition 2.1 (line 81-84)",
                     "status": "FAIL",
                     "evidence": "Scope of the card's 'any two recognition rules' is broader than Proposition 2.1 (rule A and rule B), and the round-18 lesson edit narrowed the same claim.",
                     "fix": "Use 'the two recognition rules of this lesson' in the front and the back of AC1-c052."})
    else:
        raise SystemExit(f"no decision for row {rid}")

missing = [r for r in rows if False]
rows.extend(NEW_ROWS)
ids = [r["id"] for r in rows]
assert len(ids) == len(set(ids)), "duplicate ids"
assert set(prev_rows) <= set(ids), set(prev_rows) - set(ids)

mutants = mutant_entries()
counts = {s: sum(1 for r in rows if r["status"] == s) for s in ("PASS", "FAIL", "UNVERIFIABLE")}
fragment = {
    "unit": "AC1",
    "slice": "AC1-d",
    "round": 18,
    "verifier": "Claude Haiku 5.5, independent verifier for AC1-d, round 18 (did not build AC1; read the round-17 fragment as context and computed the delta fefbf8b..7143726 on the slice)",
    "pin": "7143726",
    "base": "fefbf8b (round-17 pin; delta for the slice: project.html lines 366, 368, 393; grader/test_project.py (hunks at 328, 438-461, 486-497, 1005-1006, 1069-1073, 1130-1160); cards.json c060; the lessons L04 to L08 and tests/labs/AC1/lab-AC1-L04-1.py)",
    "checkout": "/tmp/verify18-AC1-d",
    "scratch": "/tmp/ac1-v/d18",
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "verdict": "FAIL",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "Verified this round: run_graders 50/50 (starter fails), collect 310 on seeds 0-49, page_smoke project, run_labs 11/11, "
        "the three project twins, check_pages/dag/projects, build_site, render_curriculum diff (empty), verify_refs live and offline, "
        "ruff, mypy, pytest labs subset, 165 mutants on seeds 0 and 17, 6 new mutants (5 killed, 1 equivalent with proof), "
        "29 earlier alternative files and 3 round-18 alternatives on seeds 0-49 (all pass). "
        "Out of this slice, noticed in L04.html line 330 (round-18 edit): 'depends on when the purchases were made: The printed' has a capital letter after a colon; reported for the L04 slice owner. "
        "Not checked: Pyodide 314.0.7 itself (local Python 3.14.8 only); the full re-read of L01 to L03 (carried by byte identity); "
        "the L05 to L08 lab outputs were not re-run this round except where a card cites a changed passage."
    ),
    "summary": (
        f"AC1-d round 18: {len(rows)} rows: {counts['PASS']} PASS, {counts['FAIL']} FAIL, {counts['UNVERIFIABLE']} UNVERIFIABLE; "
        f"{len(mutants)} mutants in ledgers/AC1/mutants all fail on seeds 0 and 17; 1 equivalent mutant with proof; "
        "FAIL rows are cards-c052, cards-c053-prop22-assumptions and cards-c058-two-rules-scope (and the aggregate cards-L04)."
    ),
}
OUT.write_text(json.dumps(fragment, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
print("rows", len(rows), counts, "mutants", len(mutants), "carried", sum(1 for r in rows if r['evidence'].startswith('Carried')))
