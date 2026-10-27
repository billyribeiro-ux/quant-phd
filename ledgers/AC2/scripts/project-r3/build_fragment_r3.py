"""Round 3 (AC2 project): writes ledgers/AC2/project.json (round 3). Rows are the verifier's findings; every
round-2 id is kept. Run from the repository root: .venv/bin/python ledgers/AC2/scripts/project-r3/build_fragment_r3.py
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "tools"))
import ledger  # noqa: E402

LOG = "ledgers/AC2/scripts/project-r3"
SURV = {
    "p14": ("p14_standardize_reads_every_unit_of_a_tag", "standardize reads every unit of a tag, not only USD for money and shares for share counts"),
    "p15": ("p15_accn_read_by_direct_indexing", "standardize reads obs['accn'] directly, so an observation without accn raises KeyError"),
    "p16": ("p16_tie_break_orders_form_before_accn", "as-of tie-break orders (filed, form, accn), so the form decides on one filing date"),
    "p17": ("p17_modified_jones_needs_five_firm_years", "modified_jones rejects a four-row sample (contract: four is legal)"),
    "p18": ("p18_modified_jones_finiteness_skips_regressors", "modified_jones checks finiteness of total accruals and lag only, not the regressors"),
    "p20": ("p20_piotroski_roa_plain_division", "piotroski ROA uses plain division: zero previous-year assets raises ZeroDivisionError"),
    "p21": ("p21_piotroski_shares_by_direct_indexing", "piotroski reads shares_outstanding by direct indexing: a missing latest share count raises KeyError"),
    "p29": ("p29_beneish_current_liabilities_by_direct_indexing", "beneish reads latest current_liabilities by direct indexing: KeyError, not ValueError"),
    "p35": ("p35_accruals_cash_flow_zero_average_raises_zero_division", "accruals_cash_flow raises ZeroDivisionError on zero average assets"),
    "p36": ("p36_accruals_balance_sheet_plain_division", "accruals_balance_sheet plain division: zero average assets raises ZeroDivisionError"),
    "p37": ("p37_conflict_check_skipped_when_accn_missing", "a same-date, same-value-different tie with no accn is not reported as a conflict"),
}
WITNESS = f"{LOG}/witness_r3.py"
MUT_LOG = f"{LOG}/mutate_all_r3.txt"

def surv_row(key):
    fname, desc = SURV[key]
    return (
        f"r3-surv-{key}",
        f"Mutant {key}: {desc}. Survives seeds 0-9 (mutate tool) and kills nothing in the suite.",
        f"ledgers/AC2/mutants/{fname}.py; {WITNESS}; {MUT_LOG}",
        "FAIL",
        {
            "p14": "Witness: a shares-unit observation on Assets. Reference standardize -> {} ; mutant -> {'2021-12-31': {'total_assets': 5.0}}. Contract: unit USD for money. No test feeds a non-USD unit to a money tag.",
            "p15": "Witness: an annual observation without accn. Reference -> {'2021-12-31': {'total_assets': 100.0}}; mutant raises KeyError 'accn'. Contract: accn is optional. Every observation in the suite carries accn.",
            "p16": "Witness: 10-K accn ...002 = 100 and 10-K/A accn ...001 = 90, same filing date. Reference -> 100 (greatest accn); mutant -> 90 (form '10-K/A' sorts above '10-K'). Contract tie-break is (filed, accn or ''). The instance's amendment always has the larger accn, so the suite cannot tell the two rules apart.",
            "p17": "Witness: exactly four firm-years. Reference fits (a1 = 51051.846); mutant raises ValueError. Contract and page: fewer than four raises, four is legal. Suite samples have 6 rows, so no test uses 4.",
            "p18": "Witness: NaN d_revenue in one firm-year. Reference raises ValueError; mutant raises LinAlgError (SVD did not converge). Contract: a non-finite value raises ValueError. No test puts a non-finite value in d_revenue or d_receivables.",
            "p20": "Witness: total assets of the previous year = 0. Reference raises ValueError; mutant raises ZeroDivisionError. Contract: a zero denominator raises ValueError. The suite zeroes total assets two years back only (test_piotroski_zero_assets_two_years_back_raise).",
            "p21": "Witness: latest shares_outstanding deleted. Reference raises ValueError ('nothing is imputed'); mutant raises KeyError. The suite removes only previous-year items for piotroski (PRIOR_ITEM_USE).",
            "p29": "Witness: latest current_liabilities deleted. Reference raises ValueError; mutant raises KeyError. The suite removes depreciation, ppe, receivables (prior), sga and cfo (latest) for beneish, never current_liabilities.",
            "p35": "Witness: average total assets = 0 (latest TA = -previous TA). Reference raises ValueError; mutant raises ZeroDivisionError. Zero-denominator tests cover dupont, current_ratio, gross_margin, debt_to_assets and DSO only.",
            "p36": "Witness: same zero average as p35. Reference raises ValueError; mutant raises ZeroDivisionError. Overflow tests cover accruals_cash_flow only; accruals_balance_sheet is not tested for zero average assets.",
            "p37": "Witness: two 10-K observations, same filing date, no accn, values 100 and 90. Reference raises ValueError (tie on (filed, '')); mutant returns 100. Contract: equal to (filed, accn or '') tie with different values raises. The conflict test always uses an accn.",
        }[key],
    )

ROUND2 = [
    ("proj-spec-return-keys", "2.6-spec", "course/modules/AC/AC2/project.html Required outputs; grader/test_project.py test_dupont_numbers", "PASS", "Carried from round 2 (project.html outside the bc3226e..4a8690a changed lines; re-read the Required outputs paragraph and the test: dupont keys asserted by set equality; piotroski {signals, score}, beneish eight variables and m_score, modified_jones keys all match the tests)."),
    ("proj-spec-make-instance-claim", "2.6-spec", "project.html Inputs; grader/instance.py make_instance return", "PASS", "Re-verified: make_instance returns exactly seed, label, latest, prior, prior2, payload (instance.py lines 393-400); payload holds facts, conflict, period_ends, truth, cutoffs, restatement, sample, planted."),
    ("proj-spec-formulas-deferred", "2.6-spec", "project.html Conventions and Required outputs", "PASS", "Re-read: the page defers formulas to the module lessons and the A15 contract, which states the same definitions (atlas/A15.contract.md lines 86-160)."),
    ("proj-spec-rung3-scope", "2.6-spec", "project.html Rung 3 Specification Context", "PASS", "Re-read: Context says live EDGAR retrieval is outside the autograded project; the library takes a parsed mapping. Consistent with contract Input section."),
    ("proj-spec-named-error-missing-val", "2.6-spec", "project.html Constraints; test_observation_without_a_named_field_raises[val]", "PASS", "Re-verified: the 'val' case removes val and requires ValueError; mutant p06 is killed by it (seed 0)."),
    ("proj-spec-named-error-nonfinite-result", "2.6-spec", "project.html Constraints; test_overflowing_quotient_raises", "PASS", "Re-verified: six overflow cases with finite non-zero denominators require ValueError; mutant p03 killed."),
    ("proj-spec-named-error-covered", "2.6-spec", "project.html line 245; grader/test_project.py invalid-input tests", "PASS", "Re-verified in round 3 item by item (r3-valueerror-list): every named condition on page line 243 maps to a test; the only edge without a test is in the surviving mutants list (r3-surv rows), not in the page's claim."),
    ("proj-spec-toolchain-claim", "2.6-spec", "project.html line 293; course/assets/vendor/pyodide/pyodide-lock.json", "PASS", "Re-verified: vendored wheels are cp314 (Python 3.14), numpy-2.4.6, pytest-9.0.2; the page says NumPy 2.4 and pytest 9.0."),
    ("proj-spec-local-command", "2.6-spec", "project.html line 292; course/assets/js/grader.js line 53", "PASS", "Re-verified: same flags (-q -p no:cacheprovider --assert=plain -W error) as grader.js and tools/run_graders.py PYTEST_FLAGS."),
    ("proj-spec-ladder-rung1", "2.6-spec", "project.html Rung 1 (lines 44) and Lab 1 (lines 53-173)", "PASS", "Re-ran tests/labs/AC2/lab-AC2-project-1.py under python -I -W error: output equals the page's expected block (run_labs AC2 PASS 11/11)."),
    ("proj-spec-ladder-rung2", "2.6-spec", "project.html Rung 2 (line 45) and Lab 2 (lines 175-230)", "PASS", "Re-ran lab-AC2-project-2.py: DuPont identity True, roe 0.255814, net margin 0.091667, nopat 120.0, roic 0.230769, accruals -0.02; matches page."),
    ("proj-spec-ladder-rung4", "2.6-spec", "project.html Rung 4 stretch (lines 336-342)", "PASS", "Re-read: two open-ended extensions with no numeric claim."),
    ("proj-spec-contract-conformity", "2.6-atlas", "atlas/A15.contract.md vs grader/reference.py", "PASS", "Re-verified the reference against the contract, function by function (standardize as-of and tie rule, tag table, ratios, accruals, modified_jones, piotroski, beneish). No contract statement the reference contradicts."),
    ("proj-spec-cumulative-and-reuse", "2.6-atlas", "atlas/A15.contract.md lines 6-9, 192-205", "PASS", "Re-verified after ec4fe27: the contract no longer claims a real company-facts file kept outside the repository; 'Cumulative suite' says the reference passes on generated filers and that a real file is honestly pending. Observed: data.sec.gov SEC reuse page www.sec.gov/os/webmaster-faq returns HTTP 403 'Request Rate Threshold Exceeded' to a plain curl (round 3, one request); not bypassed."),
    ("proj-spec-studios", "2.6-studio", "project.html; grader/test_project.py", "PASS", "Re-grepped round 3: no 'studio' or 'rubric' wording in the project page or test file."),
    ("proj-hours-split", "2.9-hours", "project.html data-hours-project=34; index.html data-hours-lessons=76", "PASS", "Re-verified: lesson card hours L01 9, L02 10, L03 8, L04 9, L05 8, L06 10, L07 10, L08 12 sum to 76; 76 + 34 = 110 matches the hub eyebrow and meta description."),
    ("proj-hours-estimate", "2.6-hours", "project.html Time budget (lines 262-281)", "PASS", "Re-summed: 1+2+6+5+2+5+4+4+5 = 34 = data-hours-project. Component estimates not timed; the sum check is all the round asked of this row."),
    ("proj-hub-ladder-claim", "2.9-structure", "course/modules/AC/AC2/index.html line 161 (project ladder rung 3)", "FAIL", "The hub says 'the suite checks that each instance is valid, that instances differ across seeds, and that the reference solution passes every seed'. test_project.py has no test of validity across seeds, no cross-seed difference test and no reference-passes-every-seed test (grep: no 'differ' or 'distinct' test; 73 test functions, all single-seed). Those properties are checked by tools/run_graders.py, not by the learner's suite. Learner-facing claim exceeds what the suite checks."),
    ("proj-placement-condition", "2.9-structure", "project.html line 42 vs index.html line 70", "PASS", "Re-verified: project page line 42 now says 'reach the placement bar and answer all three skill checks ... as the hub states', matching index.html line 70. The remaining hub inconsistency (line 157) is row r3-hub-line157."),
    ("proj-grader-reference-50", "2.6-autograder", "grader/reference.py; tools/run_graders.py --unit AC2 --seeds 0-49", "PASS", "Re-run: 'run_graders AC2: PASS (reference 50/50 seeds, slowest 0.3 s)' (ledgers/AC2/scripts/project-r3/run_graders_0-49.txt)."),
    ("proj-grader-instances-valid", "2.6-autograder", "grader/instance.py; scripts/project-r3/new_seeds_check.py", "PASS", "Re-verified on 20 new seeds (random.Random(20261030).sample(range(1000,100000),20)): 20 of 20 pass the independent structural checks (5-7 years, gaps 364-366 days, SIMULATED label, sample size 40-80, >= 4 planted, lag > 0, finite); reference standardize equals the generator's truth at every cut on 20 of 20."),
    ("proj-grader-instances-differ", "2.6-autograder", "scripts/project-r3/new_seeds_check.py output", "PASS", "Distinct over 20 new seeds: latest revenue 20/20, ROIC 20/20, M-score 20/20, modified-Jones a2 20/20, discretionary[0] 20/20; F-scores 4 to 9. Answers depend on the seed."),
    ("proj-grader-collect-count", "2.6-autograder", "grader/test_project.py; pytest --collect-only", "PASS", "Re-run round 3: 210 collected on seeds 0-11 and on 10 new seeds (scripts/project-r3/collect_only.py); page says 210."),
    ("proj-grader-starter-fails", "2.6-autograder", "grader/starter.py", "PASS", "Re-run: the starter fails the suite (harness output lists FAILED for starter.py, seed 0); run_graders' starter check PASS."),
    ("proj-grader-pyodide", "2.6-autograder", "page_smoke AC2 project (in-browser grader)", "PASS", "page_smoke --unit AC2 --pages project PASS; 'in-browser grader: All 210 tests pass on seed 942678012'."),
    ("proj-grader-local-pytest", "2.6-autograder", "project.html line 292", "PASS", "Same command reproduced through the harness (reference 210 passed on seeds 0-1, 20 new seeds)."),
    ("proj-grader-overconstraint", "2.6-autograder", "grader/test_project.py vs five fresh implementations V1-V5", "PASS", "Five fresh implementations (SVD cutoff 1e-8, SVD 1e-12, condition number 1e12, Cholesky pivot, strict bool-rejecting with SVD 1e-10) each pass 210/210 on seeds 0-11 and on 10 new seeds (scripts/project-r3/candidates_0-11.txt and impls/). No over-constraint found; no test rejects a valid implementation."),
    ("proj-grader-failure-messages", "2.6-autograder", "grader/test_project.py assertion messages", "PASS", "Re-read round 3: messages name the property, never print expected values (grep of f-string messages); must_raise message names the condition."),
    ("proj-grader-exception-type", "2.6-autograder", "grader/test_project.py must_raise", "PASS", "Re-read: must_raise catches ValueError only; a KeyError or ZeroDivisionError propagates as a failure (not a pass). Checks type, not wording."),
    ("proj-grader-integrity", "2.6-autograder", "project.html line 245; instance answers across seeds", "PASS", "Integrity claim is that answers change with the seed: confirmed on 20 new seeds (proj-grader-instances-differ)."),
    ("proj-grader-rubric", "2.6-rubric", "project.html Grading mode (line 245)", "PASS", "Re-read: the page describes coverage, not a grading rubric; no rubric weights are claimed."),
    ("proj-mut-p04", "2.6-mutation", "ledgers/AC2/mutants/p04_piotroski_cfo_scaled_by_year_end_assets.py", "PASS", "Killed round 3 by test_piotroski_signals_match_the_definitions (seed 1) (scripts/project-r3/mutate_all_r3.txt)."),
    ("proj-mut-p05", "2.6-mutation", "ledgers/AC2/mutants/p05_as_of_cut_excludes_a_filing_made_on_the_as_of_date.py", "PASS", "Killed round 3 by test_standardize_matches_each_as_of_cut (seed 0)."),
    ("proj-mut-p01", "2.6-mutation", "ledgers/AC2/mutants/p01_previous_year_without_the_350_380_window.py", "PASS", "Killed round 3 by test_previous_year_window_edges[dupont-349-False] (seed 0)."),
    ("proj-mut-p02", "2.6-mutation", "ledgers/AC2/mutants/p02_annual_duration_narrowed_to_360_370_days.py", "PASS", "Killed round 3 by test_annual_flow_duration_window_edges[350-True] (seed 0)."),
    ("proj-mut-p03", "2.6-mutation", "ledgers/AC2/mutants/p03_ratio_result_not_checked_for_finiteness.py", "PASS", "Killed round 3 by test_overflowing_quotient_raises[current_ratio-edit0] (seed 0)."),
    ("proj-mut-p06", "2.6-mutation", "ledgers/AC2/mutants/p06_missing_val_taken_as_zero.py", "PASS", "Killed round 3 by test_observation_without_a_named_field_raises[val] (seed 0)."),
    ("proj-mut-p07", "2.6-mutation", "ledgers/AC2/mutants/p07_prior_year_balance_filled_from_current_year.py", "PASS", "Killed round 3 by test_missing_previous_year_item_raises[dupont-total_assets] (seed 0)."),
    ("proj-mut-summary", "2.6-mutation", "tools/mutate_graders.py --unit AC2 --seeds 0-9 (scripts/project-r3/mutate_all_r3.txt)", "FAIL", "Round 3 output: 'mutate_graders AC2: FAIL (26/37 killed)'. All 13 round-2 mutants die (p01-p13). Of the 24 new mutants (p14-p37), 11 survive (rows r3-surv-p14 ... r3-surv-p37) and 13 die. Every survivor is a FAIL row; the grader was not changed."),
    ("proj-mut-p08", "2.6-mutation", "ledgers/AC2/mutants/p08_rank_checks_only_zero_columns.py", "PASS", "Round-2 FAIL fixed: the suite now has test_modified_jones_rejects_a_collinear_design_without_a_zero_column; p08 is killed on seed 0 (mutate_all_r3.txt)."),
    ("proj-mut-p09", "2.6-mutation", "ledgers/AC2/mutants/p09_piotroski_roa_signal_weak_inequality.py", "PASS", "Round-2 FAIL fixed: test_piotroski_strict_signals_score_zero_at_an_exact_tie[signal 1] kills p09 on seed 0."),
    ("proj-mut-p10", "2.6-mutation", "ledgers/AC2/mutants/p10_tag_priority_last_tag_wins.py", "PASS", "Killed round 3 by test_standardize_matches_the_final_numbers (seed 0)."),
    ("proj-mut-p11", "2.6-mutation", "ledgers/AC2/mutants/p11_modified_jones_fit_with_intercept_returns_slopes.py", "PASS", "Killed round 3 by test_modified_jones_coefficients_are_the_least_squares_fit (seed 0)."),
    ("proj-mut-p12", "2.6-mutation", "ledgers/AC2/mutants/p12_balance_sheet_accruals_adds_depreciation.py", "PASS", "Killed round 3 by test_accruals_balance_sheet_number (seed 0)."),
    ("proj-mut-p13", "2.6-mutation", "ledgers/AC2/mutants/p13_as_of_tie_on_filing_date_keeps_first_listed.py", "PASS", "Killed round 3 by test_standardize_matches_each_as_of_cut (seed 0)."),
    ("proj-lab-1", "2.5-labs", "project.html Lab 1; tests/labs/AC2/lab-AC2-project-1.py", "PASS", "Re-run under python -I -W error: revenue 990.0 / 1200.0 latest; 1000.0 / 1200.0 on 2023-03-01; {} on 2022-01-31. Matches the page block."),
    ("proj-lab-2", "2.5-labs", "project.html Lab 2; tests/labs/AC2/lab-AC2-project-2.py", "PASS", "Re-run: matches the page block (identity True, roe 0.255814, net margin 0.091667, nopat 120.0, roic 0.230769, accruals -0.02)."),
    ("proj-lab-3", "2.5-labs", "project.html Lab 3; tests/labs/AC2/lab-AC2-project-3.py", "PASS", "Re-run: coefficients [25081.462105, -0.821498, -0.006263], discretionary [0.002703, -0.004013, 0.006209, 0.000235, 0.004347, -0.009161], rank 3; matches the page block. The lab's own sentence about the suite is row r3-lab3-sample-claim."),
    ("proj-labs-run", "2.5-labs", "tools/run_labs.py --unit AC2", "PASS", "Re-run round 3: 'run_labs AC2: PASS (11/11)'."),
    ("proj-numbers-134", "2.2-numbers", "project.html Labs 1-3 printed numbers", "PASS", "Every printed number in the three project labs was recomputed by running the twins (lab outputs above); no prose number outside the labs in the project page."),
    ("proj-numbers-lab", "2.2-numbers", "project.html Lab 1-3 interpretation sentences", "PASS", "Interpretations checked against the printed outputs: 'the amendment is not yet known' on 2023-03-01 (filed 2023-03-20); 'the 10-Q is never a candidate'; 'accrual negative' (cfo 130 > ni 110); the fifth firm-year discretionary 0.004347 is positive as predicted."),
    ("proj-numbers-contract-quoted", "2.2-numbers", "atlas/A15.contract.md Piotroski and Beneish numbers", "PASS", "Contract numbers are the Beneish constants (labelled UNCONFIRMED in the page) and no other numeric claim; the Beneish constants are confirmed against the readable Wikipedia copy only (proj-beneish-values-match-wiki)."),
    ("proj-cite-registry", "2.1-citations", "references/references.json piotroski2000value, dechow1995detecting, beneish1999detection", "PASS", "Registry keys exist and are cited by key. piotroski2000value record: JAR 38, pages '1' (no range; not a locator)."),
    ("proj-cite-dechow", "2.1-attribution", "project.html Lab 3 hypothesis and reading list; grader files", "PASS", "Cited by key and title 'Detecting Earnings Management'; no author names in the project page, labs or grader text (grep)."),
    ("proj-cite-piotroski", "2.1-attribution", "atlas/A15.contract.md lines 164-169; registry piotroski2000value", "PASS", "Round-2 UNVERIFIABLE resolved. A plain curl of the Ivey-hosted PDF (https://www.ivey.uwo.ca/media/3775523/value_investing_the_use_of_historical_financial_statement_information.pdf, HTTP 200, printed page numbers = PDF page numbers) confirms the locators: income before extraordinary items p.7 (line 40) and p.8 (line 14); equity issuance 'did not issue common equity in the year preceding portfolio formation' p.9 (line 6); total long-term debt p.8 (line 25). The contract's pp. 7-8, p. 9 and p. 8 are right."),
    ("proj-cite-beneish", "2.1-attribution", "project.html Conventions; instance.py BENEISH_STATUS", "PASS", "Beneish (1999) cited by registry key beneish1999detection and labelled unconfirmed; no locator claimed."),
    ("proj-cite-sloan-penman", "2.1-attribution", "project.html and contract references to Sloan (1996) and Penman", "PASS", "Sloan (1996) cited for the cash exclusion in the balance-sheet accruals test (test_cash_is_subtracted...); no page locator claimed on the project page."),
    ("proj-beneish-labelled", "2.3-grades", "project.html line 258; instance.py BENEISH_STATUS; reference.py comment", "PASS", "Every place the constants appear carries 'UNCONFIRMED' (project page Conventions, instance BENEISH_STATUS, reference.py, starter.py, test_project.py lines 166-167, 826-827)."),
    ("proj-beneish-grader-honest", "2.3-grades", "grader/test_project.py test_beneish_constants_are_exported (lines 165-175)", "PASS", "Round-2 FAIL fixed: the message now reads 'differs from the shared (unconfirmed) table in instance.py'. grep 'published' in test_project.py: 0 hits."),
    ("proj-beneish-one-source", "2.1-attribution", "project.html line 258; instance.py BENEISH_STATUS; scope: project slice only", "PASS", "Project page and instance say ONE secondary source (Wikipedia). Round 3 plain curl of https://en.wikipedia.org/wiki/Beneish_M-score: HTTP 200 (read 2026-10-27) reproduces the intercept and eight coefficients and the -1.78 threshold, citing Beneish (1999) without a locator. L08 (outside this slice) is not judged here."),
    ("proj-beneish-values-match-wiki", "2.2-numbers", "project.html line 258; reference.py and instance.py constants", "PASS", "Constants identical to the Wikipedia equation: -4.84; DSRI 0.92, GMI 0.528, AQI 0.404, SGI 0.892, DEPI 0.115, SGAI -0.172, LVGI -0.327, TATA 4.679 (curl, round 3)."),
    ("proj-grades-paper-claims", "2.3-grades", "atlas/A15.contract.md lines 164-169 (paper-level claims)", "PASS", "Round-2 FAIL resolved: the three Piotroski paper claims now carry locators (proj-cite-piotroski) confirmed against a readable copy. The learner page makes no further paper claim."),
    ("proj-structure", "2.9-structure", "project.html structure (sections, nav, labs)", "PASS", "tools/check_pages.py --all: AC2 PASS (round 3). Page section ids and anchors resolve."),
    ("proj-banned-phrases", "2.9-prose", "project.html", "PASS", "Grep for 'roughly half', 'about 6%', 'historically', unexplained ellipses: no hits. The one ellipsis (line 241, '(s1, ..., s9)') is list notation for nine numbered signals defined in the contract, not omitted content."),
    ("proj-dag", "2.9-dag", "tools/check_dag.py --all", "PASS", "Round 3: 'check_dag AC2: PASS'."),
    ("proj-pagesmoke", "2.9-structure", "tools/page_smoke.py --unit AC2 --pages project", "PASS", "Round 3: 'page_smoke modules/AC/AC2/project.html: PASS'; 'page_smoke AC2: PASS'."),
    ("proj-lint-types", "2.9-tooling", "ruff and mypy on grader and lab twins", "PASS", "Round 3: ruff check (grader, labs): All checks passed. mypy --no-incremental on reference.py, starter.py, instance.py: Success, no issues."),
    ("proj-data-honest", "2.8-data", "project.html lines 239 and 365; grep for real company names", "PASS", "No real company name, CIK or real figure in the project page, labs or grader (grep). Real EDGAR files are honestly pending; the SEC reuse page returned HTTP 403 to one plain request (not bypassed)."),
    ("proj-spec-asof-named-condition", "2.6-spec", "project.html Constraints (line 243) and test_invalid_facts_raise", "PASS", "Round-2 FAIL fixed: line 243 now says 'an as-of date that is not an ISO date (an as-of date before every filing gives an empty mapping, not an error)'. Tests: bad-as-of, impossible-as-of, int-as-of raise ValueError; test_as_of_before_any_filing_gives_an_empty_mapping returns {}."),
    ("proj-cite-dechow-contract", "2.1-attribution", "atlas/A15.contract.md line 123", "PASS", "Round-2 FAIL fixed: the contract now cites 'dechow1995detecting, Detecting Earnings Management' with no authors."),
    ("proj-contract-scale-grader-claim", "2.6-atlas", "atlas/A15.contract.md Scale row; test_modified_jones_is_invariant_to_money_units", "PASS", "Round-2 FAIL fixed: the Scale row now says the grader tests that a1 scales by k; the test asserts b[a1] == c * a[a1] (rel 1e-6) and that a2, a3 are unchanged."),
    ("proj-lab1-inclusive-overreach", "2.5-labs", "project.html Lab 1 interpretation (line 172)", "PASS", "Round-2 FAIL fixed: the interpretation no longer says the cut-off is inclusive; it says a later filing cannot leak backwards, which Lab 1 shows (2023-03-01 excludes the 2023-03-20 amendment)."),
    ("proj-section-refs", "2.9-structure", "project.html rung and specification links (lines 46-47, 177)", "PASS", "Round-2 FAIL fixed: links now name sections ('the specification section', 'the Conventions section'); no '§3'/'§5'/'§7' in the page. The one remaining internal reference is row r3-blueprint-ref."),
    ("proj-spec-proxy-claims", "2.6-spec", "atlas/A15.contract.md lines 162-169; project.html Conventions line 256", "PASS", "Re-verified: the page says the contract defines three Piotroski proxies; the contract names net_income (NetIncomeLoss), signal 7 (shares change) and long_term_debt (LongTermDebtNoncurrent) with the locators confirmed (proj-cite-piotroski)."),
    ("proj-learner-process-words", "2.9-prose", "project.html and grader text", "PASS", "Grep for 'builder', 'this build', 'REQUESTS', 'unit report': 0 hits in project.html and test_project.py."),
]

NEW = [
    ("r3-run-graders", "2.6-autograder", "tools/run_graders.py --unit AC2 --seeds 0-49", "PASS", "'run_graders AC2: PASS (reference 50/50 seeds, slowest 0.3 s)' (scripts/project-r3/run_graders_0-49.txt)."),
    ("r3-collect-only", "2.6-autograder", "pytest --collect-only, scripts/project-r3/collect_only.py", "PASS", "210 collected on seeds 0-11 and on 10 new seeds (5899, 17179, 19590, 20410, 22023, 29803, 35334, 36395, 38882, 44746)."),
    ("r3-new-seeds-validity", "2.6-autograder", "scripts/project-r3/new_seeds_check.py (20 new seeds)", "PASS", "New seeds = random.Random(20261030).sample(range(1000,100000),20): 5899, 17179, 19590, 20410, 22023, 29803, 35334, 36395, 38882, 44746, 45472, 54979, 55071, 68753, 72476, 74431, 78482, 84177, 87275, 97186. Disjoint from 0-49 and from round 2's sample (asserted). 'instances with problems: none'; 5/6/7 years; reference standardize equals generator truth at every cut."),
    ("r3-new-seeds-differ", "2.6-autograder", "scripts/project-r3/new_seeds_check.py output", "PASS", "Distinct on 20 of 20 seeds for latest revenue, ROIC(25%), M-score, modified-Jones a2 and discretionary[0]; F-scores 4-9; same-day amendment on 8 of 20 seeds."),
    ("r3-new-seeds-suite", "2.6-autograder", "scripts/project-r3/drive_new_seeds.py: reference over 20 new seeds", "PASS", "210 passed on 20 of 20 new seeds."),
    ("r3-candidates", "2.6-autograder", "impls/V1..V5 (scripts/project-r3/impls); candidates_0-11.txt", "PASS", "Five fresh implementations, each 210 passed on seeds 0-11 and 210 passed on 10 new seeds: V1 SVD cutoff 1e-8 relative; V2 1e-12 relative; V3 condition number cutoff 1e12; V4 Cholesky pivot (squared pivot <= 1e-10 rejects); V5 SVD 1e-10 with bool rejection. Written fresh from the contract; the non-rank code is shared between them and was not copied from reference.py."),
    ("r3-mut-round2-set", "2.6-mutation", "ledgers/AC2/mutants/p01-p13 with tools/mutate_graders.py --seeds 0-9", "PASS", "All 13 round-2 mutants die (killed_by in the fragment's mutants list)."),
    ("r3-mut-new-killed", "2.6-mutation", "ledgers/AC2/mutants/p19, p22-p28, p30-p34", "PASS", "13 new mutants die on seeds 0-9: p19, p22, p23, p24, p25, p26, p27, p28, p30, p31, p32, p33, p34 (killed_by in the fragment)."),
    ("r3-hub-line157", "2.9-structure", "course/modules/AC/AC2/index.html line 157", "FAIL", "Hub text: 'a student who passes that check skips them'. Line 70 of the same page (placement) says skip only if the bar AND all three skill checks are met, and project.html line 42 says the same. Line 157 drops the skill-check condition."),
    ("r3-placement-s2", "2.9-structure", "course/modules/AC/AC2/index.html lines 60, 68-70", "FAIL", "Line 60 says AC2 assumes AC1, S0 and S2; line 70 says 'six on the prerequisites (AC1 and S0)' and then 'revisit AC1, S0 and S2 first'. The six prerequisite items are four AC1 and two S0 items (Pq1, gross-margin, Pq3, Pq4 AC1; median, MNAR S0); none tests S2, which the hub names as a prerequisite."),
    ("r3-same-day-claim", "2.6-spec", "project.html line 245 (Grading mode, 'as-of cut-offs that include a same-day amendment')", "FAIL", "The instance draws a same-day amendment on only some seeds: 25 of seeds 0-49 and 8 of 20 new seeds (computed from payload restatement.same_day). On other seeds the suite has no same-day amendment to check, so the sentence describes a coverage that varies with the seed."),
    ("r3-tuple-claim", "2.6-spec", "project.html line 241 (Required outputs: piotroski signals as a tuple, modified_jones coefficients as a tuple)", "FAIL", "Minor. The page presents the return shapes as tuples; test_project.py checks length, values and sums but never the container type (a list passes). A learner-facing shape claim the suite does not enforce."),
    ("r3-lab3-sample-claim", "2.5-labs", "project.html Lab 3 hypothesis (line 300)", "FAIL", "Minor. 'Your modified_jones must reproduce these coefficients and discretionary accruals on the same sample' — the suite never runs the literal six-row sample (it uses instance.py's SAMPLE). The statement is a correct mathematical expectation of a correct module, but the sentence reads as something the autograder enforces."),
    ("r3-blueprint-ref", "2.9-prose", "project.html line 245", "FAIL", "Minor. Learner-facing text cites 'BLUEPRINT §5.2', an internal planning document the learner does not have. Process reference in learner text."),
    ("r3-sec-pending", "2.8-data", "https://www.sec.gov/os/webmaster-faq (one plain curl)", "PASS", "HTTP 403 'SEC.gov | Request Rate Threshold Exceeded'. The access block was not bypassed. The page's statement that the SEC reuse statement has not been read from a reachable issuer page is consistent with this."),
    ("r3-piotroski-locators", "2.1-attribution", "atlas/A15.contract.md lines 164-168 vs the Ivey-hosted PDF", "PASS", "See proj-cite-piotroski. Registry piotroski2000value has no page range; the page locators come from the hosted copy, not from JSTOR."),
    ("r3-wiki-beneish", "2.2-numbers", "https://en.wikipedia.org/wiki/Beneish_M-score (plain curl, HTTP 200)", "PASS", "Wikipedia equation reproduces -4.84 and the eight coefficients exactly; threshold -1.78 'see Beneish 1999' with no locator. Basis for the 'ONE secondary source' statement."),
    ("r3-banned-numbers", "2.3-grades", "grep -rn '4.697|2.22' over course, tests, atlas, plans, references, curriculum, tools (AC2 surfaces)", "PASS", "No 4.697 and no -2.22 in any AC2 surface (hits found only in unrelated S7 and market data files)."),
    ("r3-valueerror-list", "2.6-spec", "project.html line 243 and line 245 list vs test_project.py", "PASS", "Item by item: mapping without facts (no-facts); observation without end/val/filed/form (no-end, no-filed, no-form, test_observation_without_a_named_field_raises); non-finite value (nan, inf, string-value); bad date (bad-end, bad-filed, bad-start, bad-as-of, impossible-as-of, int-as-of); period end not in statements or not ISO (test_unknown_or_malformed_period_end_raises); missing item (test_each_ratio_raises_on_a_missing_item, test_beneish_raises_on_a_missing_item); missing previous year (test_ratios_that_need_the_prior_year..., test_previous_year_window_edges, test_missing_previous_year_item_raises); zero denominator (test_zero_denominator_raises, zero average assets/equity); non-finite result (test_overflowing_*); tax rate (roic invalid tax); non-positive IC (test_roic_rejects_nonpositive_invested_capital); modified Jones: <4 (three, empty), non-positive lag (zero-lag, negative-lag), non-finite (nan, inf), rank-deficient (rank-zero-column, rank-zero-diff, collinear). Every condition on the page has a test."),
    ("r3-test-assertions", "2.6-spec", "grader/test_project.py: every assertion added or changed since bc3226e (diff read in full)", "PASS", "Each new assertion is in the contract or the page: piotroski ties (strict signals 1, 2, 6, 8, 9 are strict by contract; weak signal 7 is contract '<='); as-of before any filing gives {} (contract); flow without start ignored (contract); instant with start ignored (contract); collinear design rejected (contract rank-deficient); tolerances (FLOAT_RTOL 1e-6, FLOAT_ATOL 1e-9) are documented in the test comment and no learner sentence states a tolerance."),
    ("r3-int-as-of", "2.6-spec", "grader/test_project.py test_invalid_facts_raise id 'int-as-of'", "PASS", "Passing an int as as_of must raise ValueError. Contract Input section: dates are parsed with fromisoformat and 'anything else raises ValueError'. Consistent with the contract."),
    ("r3-tolerance-scope", "2.6-autograder", "grader/test_project.py FLOAT_RTOL 1e-6, FLOAT_ATOL 1e-9", "PASS", "One documented bound for all float comparisons except the DuPont identity at 1e-12 (contract). Five candidate implementations with different rank tolerances pass; no test depends on a threshold the contract does not state (rank checks are judged by the two rank tests only)."),
    ("r3-commands", "2.9-structure", "tools/check_pages.py --all; tools/check_dag.py --all; tools/check_projects.py --all; tools/run_labs.py --unit AC2", "PASS", "All PASS for AC2 (check_pages AC2 PASS, check_dag AC2 PASS, check_projects AC2 PASS, run_labs AC2 PASS 11/11)."),
    ("r3-page-smoke", "2.9-structure", "tools/page_smoke.py --unit AC2 --pages project", "PASS", "'page_smoke AC2: PASS'; in-browser grader 'All 210 tests pass on seed 942678012'."),
    ("r3-lab-twins", "2.5-labs", "tests/labs/AC2/lab-AC2-project-{1,2,3}.py under python -I -W error", "PASS", "All three twins run clean; outputs equal the page's expected blocks (see proj-lab-1..3)."),
]
SURVIVOR_ROWS = [surv_row(k) for k in ["p14", "p15", "p16", "p17", "p18", "p20", "p21", "p29", "p35", "p36", "p37"]]

ROWS = []
for rid, check, loc, status, ev in ROUND2:
    ROWS.append({"id": rid, "check": check, "location": loc, "status": status, "evidence": ev})
for rid, check, loc, status, ev in NEW:
    ROWS.append({"id": rid, "check": check, "location": loc, "status": status, "evidence": ev})
for rid, desc, loc, status, ev in SURVIVOR_ROWS:
    ROWS.append({"id": rid, "check": "2.6-mutation", "location": loc, "status": status, "evidence": ev + " " + desc})

MUTANTS = [
    ("p01_previous_year_without_the_350_380_window", "test_previous_year_window_edges[dupont-349-False] (seed 0)"),
    ("p02_annual_duration_narrowed_to_360_370_days", "test_annual_flow_duration_window_edges[350-True] (seed 0)"),
    ("p03_ratio_result_not_checked_for_finiteness", "test_overflowing_quotient_raises[current_ratio-edit0] (seed 0)"),
    ("p04_piotroski_cfo_scaled_by_year_end_assets", "test_piotroski_signals_match_the_definitions (seed 1)"),
    ("p05_as_of_cut_excludes_a_filing_made_on_the_as_of_date", "test_standardize_matches_each_as_of_cut (seed 0)"),
    ("p06_missing_val_taken_as_zero", "test_observation_without_a_named_field_raises[val] (seed 0)"),
    ("p07_prior_year_balance_filled_from_current_year", "test_missing_previous_year_item_raises[dupont-total_assets] (seed 0)"),
    ("p08_rank_checks_only_zero_columns", "test_modified_jones_rejects_a_collinear_design_without_a_zero_column (seed 0)"),
    ("p09_piotroski_roa_signal_weak_inequality", "test_piotroski_strict_signals_score_zero_at_an_exact_tie[signal 1] (seed 0)"),
    ("p10_tag_priority_last_tag_wins", "test_standardize_matches_the_final_numbers (seed 0)"),
    ("p11_modified_jones_fit_with_intercept_returns_slopes", "test_modified_jones_coefficients_are_the_least_squares_fit (seed 0)"),
    ("p12_balance_sheet_accruals_adds_depreciation", "test_accruals_balance_sheet_number (seed 0)"),
    ("p13_as_of_tie_on_filing_date_keeps_first_listed", "test_standardize_matches_each_as_of_cut (seed 0)"),
    ("p14_standardize_reads_every_unit_of_a_tag", None),
    ("p15_accn_read_by_direct_indexing", None),
    ("p16_tie_break_orders_form_before_accn", None),
    ("p17_modified_jones_needs_five_firm_years", None),
    ("p18_modified_jones_finiteness_skips_regressors", None),
    ("p19_accruals_cash_flow_plain_division", "test_overflowing_quotient_raises[accruals_cash_flow-edit5] (seed 0)"),
    ("p20_piotroski_roa_plain_division", None),
    ("p21_piotroski_shares_by_direct_indexing", None),
    ("p22_shares_read_in_usd_unit", "test_standardize_matches_the_final_numbers (seed 0)"),
    ("p23_dupont_leverage_uses_year_end_equity", "test_dupont_numbers (seed 0)"),
    ("p24_accruals_balance_sheet_year_end_assets", "test_accruals_balance_sheet_number (seed 0)"),
    ("p25_piotroski_signal4_cfo_scaled_by_year_end_assets", "test_piotroski_signals_match_the_definitions (seed 1)"),
    ("p26_roic_invested_capital_adds_cash", "test_roic_number (seed 0)"),
    ("p27_modified_jones_lists_sorted_by_lag", "test_modified_jones_fitted_and_discretionary_identities (seed 0)"),
    ("p28_beneish_depi_without_depreciation_in_denominator", "test_beneish_variables_and_score_match_the_definitions (seed 0)"),
    ("p29_beneish_current_liabilities_by_direct_indexing", None),
    ("p30_tie_break_prefers_plain_10k_on_one_date", "test_standardize_matches_each_as_of_cut (seed 0)"),
    ("p31_piotroski_signal5_weak_inequality", "test_piotroski_ties_follow_the_strict_and_weak_inequalities (seed 0)"),
    ("p32_piotroski_signal7_strict_inequality", "test_piotroski_ties_follow_the_strict_and_weak_inequalities (seed 0)"),
    ("p33_piotroski_leverage_uses_total_liabilities", "test_missing_previous_year_item_raises[piotroski_f_score-long_term_debt] (seed 0)"),
    ("p34_piotroski_current_ratio_over_total_assets", "test_missing_previous_year_item_raises[piotroski_f_score-current_liabilities] (seed 0)"),
    ("p35_accruals_cash_flow_zero_average_raises_zero_division", None),
    ("p36_accruals_balance_sheet_plain_division", None),
    ("p37_conflict_check_skipped_when_accn_missing", None),
]
mutants = []
for name, killed in MUTANTS:
    mutants.append({
        "description": f"{name.split('_')[0]}: " + (
            "round-2 mutant (builder-era verifier set)" if int(name[1:3]) <= 13 else "round-3 student-error mutant"
        ),
        "killed_by": killed,
        "file": f"ledgers/AC2/mutants/{name}.py",
    })
# descriptions taken from each file's docstring (first line), for the record
import ast  # noqa: E402
for m in mutants:
    src = (ROOT / m["file"]).read_text(encoding="utf-8")
    doc = ast.get_docstring(ast.parse(src)) or ""
    m["description"] = doc.splitlines()[0] if doc else m["description"]

FIXES = {
    "proj-hub-ladder-claim": "Edit index.html line 161 to say only what the learner's suite checks (single-seed correctness); the cross-seed and reference-on-every-seed checks belong to tools/run_graders.py, not to the learner suite.",
    "proj-mut-summary": "Add tests for the eleven surviving mutants (rows r3-surv-*), then re-run tools/mutate_graders.py --unit AC2 --seeds 0-9.",
    "r3-hub-line157": "Edit index.html line 157 to match line 70: skip only with the bar and all three skill checks.",
    "r3-placement-s2": "Either add an S2 item to the placement diagnostic or state the six items as AC1 and S0 only and give S2 its own check; make lines 60 and 70 consistent.",
    "r3-same-day-claim": "Reword project.html line 245 to say same-day amendments are checked on the seeds that draw one (about half), or add a fixed same-day test that does not depend on the seed.",
    "r3-tuple-claim": "Reword the return shapes on project.html line 241 to 'a sequence' or add a type check (tuple) to the suite.",
    "r3-lab3-sample-claim": "Reword the Lab 3 hypothesis: the six-row sample is checked by hand against the printed output, not by the autograder.",
    "r3-blueprint-ref": "Remove 'BLUEPRINT §5.2' from project.html line 245; name the autograder section instead.",
}
for row in ROWS:
    if row["status"] != "PASS" and not row.get("fix"):
        row["fix"] = FIXES.get(row["id"], "Add a suite test that the contract requires this case (witness in evidence); the grader was not changed in this verification.")

fails = [r for r in ROWS if r["status"] != "PASS"]
counts = {"rows": len(ROWS), "pass": sum(r["status"] == "PASS" for r in ROWS), "fail": len(fails),
          "unverifiable": sum(r["status"] == "UNVERIFIABLE" for r in ROWS),
          "mutants": len(mutants), "mutants_killed": sum(1 for m in mutants if m["killed_by"]),
          "survivors": [m["file"].split("/")[-1][:3] for m in mutants if not m["killed_by"]]}
frag = {
    "unit": "AC2",
    "slice": "project",
    "round": 3,
    "verifier": "Claude Haiku 5.5 (independent project-slice verifier, round 3; did not build AC2; fresh context)",
    "pin": "4a8690a",
    "base": "round 2 fragment (pin bc3226e) read as context; its PASS rows were re-verified, not carried, where the subject changed",
    "checkout": "/tmp/verify-ac2-p (detached at 4a8690a)",
    "scratch": "/tmp/ac2-v/project/",
    "verified_at": "2026-10-27",
    "verdict": "FAIL" if fails else "PASS",
    "rows": ROWS,
    "mutants": mutants,
    "registry_flags": [
        "piotroski2000value: registry page range is '1' (no range); the contract's locators (pp. 7-8, 9, 8) are confirmed against the Ivey-hosted copy, not against the registry record.",
        "beneish1999detection: UNCONFIRMED constants (one secondary source, Wikipedia, reproduces them); no locator into the paper.",
        "dechow1995detecting: authors remain an open question; the project page and contract cite by key and title, with no author names.",
    ],
    "freshness_flags": [],
    "notes": [
        "Round 3 delta: project.html (14 lines), test_project.py (+129/-44), A15.contract.md (27 lines), index.html ladder (2 lines). Every changed hunk was read.",
        "Five fresh implementations (V1-V5) pass 210/210 on seeds 0-11 and on 10 new seeds: no over-constraint found.",
        "The learner-facing claims that exceed the suite (hub ladder suite claim, same-day coverage, tuple shape, lab-3 sample, BLUEPRINT reference) are FAIL rows; the grader was not changed.",
        "Survivors are 11 of 37 mutants; each has a witness in scripts/project-r3/witness_r3.py output.",
        "Not checked: JSTOR and other publisher pages (not attempted); SEC reuse statement (403 on one plain request, not bypassed); L08 and the other lessons (other slices).",
        "Carried rows: none carried byte-identically; several round-2 PASS rows were re-verified by their listed commands or by the greps recorded in their evidence.",
    ],
    "summary": {**counts, "sentence": (
        f"Round 3 project: suite 210 checks (collect 210 on 22 seeds); run_graders 50/50; 20 new seeds valid and answers differ; "
        f"five fresh implementations pass; mutants {counts['mutants_killed']}/{counts['mutants']} killed; "
        f"survivors {', '.join(counts['survivors'])} are FAIL rows; hub ladder suite claim, hub line 157, placement prerequisites, same-day coverage claim, tuple shape, lab-3 sample wording and BLUEPRINT reference are FAIL rows."
    )},
}
out = ROOT / "ledgers/AC2/project.json"
out.write_text(json.dumps(frag, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out, counts["rows"], "rows;", counts["fail"], "non-PASS;", counts["mutants_killed"], "/", counts["mutants"], "killed")
