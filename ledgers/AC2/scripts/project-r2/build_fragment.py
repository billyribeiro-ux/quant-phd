# ruff: noqa (verifier scratch code: style is not gated; see the fragment)
"""Write the round-2 project fragment ledgers/AC2/project.json (AC2 project slice). Usage: run from the checkout root."""

from __future__ import annotations

import datetime as dt
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
P = "course/modules/AC/AC2/project.html"
T = "course/modules/AC/AC2/grader/test_project.py"
C = "atlas/A15.contract.md"
LOG = "/tmp/ac2-v/project-r2/logs"
R2 = "ledgers/AC2/scripts/project-r2"
MUT = "ledgers/AC2/mutants"

rows: list[dict[str, str]] = []


def row(rid: str, check: str, location: str, status: str, evidence: str, fix: str = "") -> None:
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    rows.append(r)


# ---- spec, page and contract (round-1 ids kept)
row("proj-spec-return-keys", "2.6-spec", f"{P} lines 240-241 (Required outputs); {T} test_dupont_numbers, test_piotroski_*, test_beneish_*, test_modified_jones_*", "PASS",
    f"Round 1 FAIL fixed. Page line 241 names dupont {{net_margin, asset_turnover, leverage, roe, roa}}, piotroski_f_score {{signals (s1..s9), score}}, beneish_m_score (DSRI..TATA, m_score), modified_jones {{coefficients (a1,a2,a3), nondiscretionary, discretionary}}. Test line 404-405 asserts set(out) == the five dupont keys exactly; lines 749-752, 757-759, 812-814, 618-639 read the other keys. Matches reference.py lines 275-281, 394-398, 435, 488.")
row("proj-spec-make-instance-claim", "2.6-spec", f"{P} line 239; course/modules/AC/AC2/grader/instance.py lines 393-400", "PASS",
    "Round 1 FAIL fixed. Page says make_instance(seed) returns keys seed, label, latest, prior, prior2, payload. instance.py return dict (lines 393-400) has exactly seed, label, latest, prior, prior2, payload; the suite reads INST['payload'], INST['latest'], INST['prior'], INST['prior2'] (test lines 45-52). Payload holds facts and sample (instance.py line 390; test line 55).")
row("proj-spec-formulas-deferred", "2.6-spec", f"{P} lines 254-256 (Conventions)", "PASS",
    "Page defers accrual, Piotroski and Beneish formulas to the lessons and the A15 contract (line 255). Contract lines 84-140 (scores section) define them; reference.py lines 404-488 implement them. Re-read: no formula is stated on the page that conflicts with the contract.")
row("proj-spec-rung3-scope", "2.6-spec", f"{P} line 237 (Context); curriculum/02-economics-finance-core.yaml line 581 (brief 'Ingest EDGAR XBRL'); curriculum/01-foundations.yaml line 473 ('Atlas A2: data layer')", "PASS",
    "Round 1 FAIL fixed. Page line 237 names the curriculum's EDGAR ingestion brief and states live EDGAR retrieval is outside the autograded project, with the A2 data layer as the loader. Both names exist in the curriculum; the A15 contract (line 9) says A2 supplies the loader.")
row("proj-spec-named-error-missing-val", "2.6-spec", f"{P} line 243; {T} test_observation_without_a_named_field_raises[val]", "PASS",
    f"Round 1 FAIL fixed. The test pops 'val' and requires ValueError. Mutant p06 (val taken as zero) is killed by test_observation_without_a_named_field_raises[val] on seed 0 ({LOG}/mutate_all_seeds0-9_fixed.txt).")
row("proj-spec-named-error-nonfinite-result", "2.6-spec", f"{P} line 243; {T} test_overflowing_quotient_raises (6 cases), test_overflowing_roic_raises", "PASS",
    "Round 1 FAIL fixed. Each case has finite non-zero denominators whose quotient overflows to inf, and each requires ValueError. Mutant p03 (overflow returned) is killed by test_overflowing_quotient_raises[current_ratio-edit0] on seed 0. Contract line 'Division' (Conventions table) says a non-finite result raises ValueError, so the test is contract-backed.")
row("proj-spec-named-error-covered", "2.6-spec", f"{P} line 245 ('every named ValueError'); {T} test_modified_jones_invalid_input_raises ids rank-zero-column and rank-zero-diff", "FAIL",
    f"The page claims the suite covers every named ValueError. The named condition 'a rank-deficient design' is tested only when a regressor column is identically zero (rank-zero-column, rank-zero-diff). A linearly dependent design with no zero column is not rejected by the suite: mutant p08 (rank test only rejects all-zero columns) survives seeds 0-9 and seeds 0-49 ({LOG}/mutate_all_seeds0-9_fixed.txt; {LOG}/p08_p09_seeds0-49.txt). Witness: {R2}/witness_r2.py prints the reference raising ValueError and p08 returning coefficients [-7.0, 0.5, 0.5] for ppe = dRev - dRec ({LOG}/witness_r2.txt).",
    "Add a test: a sample whose ppe equals d_revenue - d_receivables (two proportional regressors) must raise ValueError; or narrow the page's claim to 'a rank-deficient design with an identically zero regressor'.")
row("proj-spec-toolchain-claim", "2.6-spec", f"{P} line 293", "PASS",
    "Page: 'Use Python 3.14 with NumPy 2.4 and pytest 9.0'. course/assets/vendor/pyodide/pyodide-lock.json: python 3.14.2, numpy 2.4.6, pytest 9.0.2 (the browser grader's versions). Local interpreter 3.14.8 (.venv). Major.minor match.")
row("proj-spec-local-command", "2.6-spec", f"{P} line 292; course/assets/js/grader.js line 53", "PASS",
    "Page command 'QF_SEED=<seed> pytest -q -p no:cacheprovider --assert=plain -W error test_project.py' is the same flag set grader.js prints (line 53) and tools/run_graders.py uses. Run through run_graders (50 seeds PASS) and run_candidates.py (same flags, seeds 0-9 and 20 new seeds).")
row("proj-spec-ladder-rung1", "2.6-spec", f"{P} lines 44 and 52-171 (Lab 1)", "PASS",
    "Rung 1 describes Lab 1 as the as-of rule and tag priority for one item, annotated. Lab 1 twin runs under python -I -W error with output identical to the page's expected block (ledger log {LOG}/twin1.txt; diff of page code vs twin: IDENTICAL).")
row("proj-spec-ladder-rung2", "2.6-spec", f"{P} lines 45 and 175-230 (Lab 2)", "PASS",
    "Rung 2 describes Lab 2 as the DuPont, ROIC and accrual lines with blanks, graded against completed lines. The page's blank code differs from the twin only in the 7 completed lines (diff); the twin's output equals the page's expected block (exp2 match). Browser grading is output comparison (lab.js lines 56-61).")
row("proj-spec-ladder-rung4", "2.6-spec", f"{P} lines 336-341 (Rung 4)", "PASS",
    "Two open-ended stretch items; no test or grade is claimed for them.")
row("proj-spec-contract-conformity", "2.6-atlas", f"{C} lines 1-200; course/modules/AC/AC2/grader/reference.py lines 26-488", "PASS",
    "Re-read reference against contract: ITEMS (17, order), TAG_PRIORITY (all 17 entries), the as-of rule, tie rule, previous-year window, averages, NOPAT, invested capital, accrual formulas, modified_jones design and rank check, Piotroski nine signals (signal 4 strict, 7 weak), Beneish eight variables and M. No divergence found between reference and contract formulas. Contract statements that conflict with the suite are separate rows.")
row("proj-spec-cumulative-and-reuse", "2.6-atlas", f"{C} lines 6-9 and 'Cumulative suite' (lines 200-202)", "FAIL",
    "The contract's cumulative-suite paragraph says the A15 reference passes its suite 'on at least one real company-facts file kept outside the repository for the verifier'. No such file exists: a search of /tmp and /Users/billyribeiro/dev for companyfacts files returned nothing, and the page and contract state real EDGAR data is honestly pending (SEC reuse statement unread). The contract therefore claims a verification no one can perform now. The contract's own 'Data' section says the autograder uses generated filers, which is what is evidenced.",
    "Change the contract's cumulative-suite sentence to state the pending real-file check as an explicit open item (plans/AC2-open-items.md), or remove the claim until a reuse statement is read.")
row("proj-spec-studios", "2.6-studio", f"{P} (no studio section)", "PASS", "No studio on the project page; check_projects.py --unit AC2 PASS.")

# ---- hours
row("proj-hours-split", "2.9-hours", "course/modules/AC/AC2/index.html data-hours-lessons=76 data-hours-project=34; project.html data-hours-project=34", "PASS",
    "Lesson hours data-hours from L01..L08: 9+10+8+9+8+10+10+12 = 76 (grep of each page). Project 34. 76+34 = 110 = hub tier hours. Page and hub agree on 34.")
row("proj-hours-estimate", "2.6-hours", f"{P} lines 266-277 (Time budget)", "PASS",
    "Declared components sum to 34 (1+2+6+5+2+5+4+4+5). My own estimate for a student who has passed the placement check: 26 to 34 h (standardize 5-7, ratios 4-5, accruals 2, modified_jones 3-4, Piotroski and Beneish 4-6, labs 2-3, failure reading 3-5). Midpoint 30 h; declared 34 is within +/-30 percent of both 30 and 26 to 34.")

# ---- hub ladder
row("proj-hub-ladder-claim", "2.9-structure", "course/modules/AC/AC2/index.html lines 155-164 ('The project ladder', worked example bullet) vs project.html Lab 1", "PASS",
    "Reworded bullet: 'A fully solved and annotated worked example of the as-of rule and tag priority for revenue on a small SIMULATED filer, with the reason for every rule at every step.' Lab 1 (project.html lines 54-171) is the as-of rule and the revenue tag priority on a SIMULATED filer with no blanks; annotations give the reason for the annual rule (test lines 125-131 comments), the as-of step and the tag step (lines 143-144, 158). Lab 1 does not annotate the print statements, which carry no rule.")
row("proj-placement-condition", "2.9-structure", "course/modules/AC/AC2/project.html line 42 ('If you met the placement bar ... go straight to rung 3') vs course/modules/AC/AC2/index.html line 70 ('Skip rungs 1 and 2 only if you reach the bar and answer all three skill checks') and index.html line 157", "FAIL",
    "The project page gives the skip condition as meeting the placement bar alone. The hub gives it as the bar AND all three skill checks, which is the condition the placement check itself states. A student who meets the bar but misses a skill check is told by the page to skip.",
    "Make project.html line 42 say 'reach the placement bar and answer all three skill checks, as the module hub states'.")

# ---- grader
row("proj-grader-reference-50", "2.6-autograder", "course/modules/AC/AC2/grader/reference.py; tools/run_graders.py --unit AC2 --seeds 0-49", "PASS",
    f"Command: tools/run_graders.py --unit AC2 --seeds 0-49 -> 'run_graders AC2: PASS (reference 50/50 seeds, slowest 0.3 s)' ({LOG}/run_graders.txt).")
row("proj-grader-instances-valid", "2.6-autograder", "course/modules/AC/AC2/grader/instance.py make_instance; {R2}/r2_checks.py sample", "PASS",
    f"Round 2 sample of 20 NEW seeds (random.Random(20261028) from range(50,1000); disjoint from round 1's 0-49 draw): seeds 57, 88, 96, 195, 267, 288, 319, 520, 561, 603, 621, 642, 647, 660, 682, 750, 755, 791, 891, 897. For each: reference standardize() equals the generator's truth (True 20/20) and the whole suite passes: '202 passed' 20/20 ({LOG}/sample_new_seeds.txt).")
row("proj-grader-instances-differ", "2.6-autograder", f"{R2}/r2_checks.py sample; {LOG}/sample_new_seeds.txt", "PASS",
    "Over the 20 new seeds: distinct latest revenue 20 of 20, distinct ROIC 20 of 20, distinct M-score 20 of 20, distinct modified-Jones a2 20 of 20, F-score values 4 to 9. Answers differ across seeds, not only labels.")
row("proj-grader-collect-count", "2.6-autograder", f"{T}; {R2}/r2_checks.py collect 0-11", "PASS",
    f"Page line 245 says 202 checks. pytest --collect-only on the reference: '202 tests collected' on each of seeds 0-11 ({LOG}/collect_0-11.txt) and the 20 new seeds run show '202 passed'.")
row("proj-grader-starter-fails", "2.6-autograder", "course/modules/AC/AC2/grader/starter.py; run_candidates.py 0-2 starter.py", "PASS",
    f"Starter on seeds 0-2: 'passed=16 failed=186' each seed ({LOG}/starter_0-2.txt). The 16 passing tests check constants, names and imports and call no function; every function test fails. Page line 241 ('every function raises NotImplementedError ... the suite fails on the starter') is true.")
row("proj-grader-pyodide", "2.6-autograder", f"tools/page_smoke.py --unit AC2 --pages project; {P} grader panel", "PASS",
    f"page_smoke: 'in-browser grader: All 202 tests pass on seed 1442944528' and 'page_smoke modules/AC/AC2/project.html: PASS' ({LOG}/page_smoke_project.txt).")
row("proj-grader-local-pytest", "2.6-autograder", f"{P} lines 291-294; {R2}/r2_checks.py", "PASS",
    "Local flags run through the same suite runner as the browser (sys.executable -I -m pytest with -p no:cacheprovider --assert=plain -W error). Reference passes 50/50 and candidates B, C, D pass 202/202 on seeds 0-9 and the 20 new seeds.")
row("proj-grader-overconstraint", "2.6-autograder", f"{T}; candidates {R2}/impls/D (verifier) and ledgers/AC2/scripts/project-r1/impls/A, B, C", "PASS",
    f"Four genuinely different correct implementations: B, C, D pass 202/202 on seeds 0-9 and on the 20 new seeds ({LOG}/candidates_0-9.txt, {LOG}/candidates_newseeds.txt: 30 + 60 PASS lines). D is written from the contract with a validator-first structure, an unscaled matrix_rank rank test, and a tie check on all candidates; it differs from the reference in each. Candidate A fails 7 tests, all test_overflowing_quotient_raises / test_overflowing_roic_raises, which require ValueError for a non-finite result, a rule stated in the contract (Conventions: 'Division ... so does a non-finite result'). A is wrong against the contract, so it is not an over-constraint. No over-constraint witness found.")
row("proj-grader-failure-messages", "2.6-autograder", f"{T} (all assertion messages; must_raise lines 62-68)", "PASS",
    "Read every assertion message in test_project.py (1138 lines). Messages name the property (e.g., 'roic with a tax rate of one'), never print expected values. The one message that makes a false claim about its check is recorded in proj-beneish-grader-honest.")
row("proj-grader-exception-type", "2.6-autograder", f"{T} must_raise lines 62-68; {P} line 243", "PASS",
    "must_raise catches ValueError only and fails otherwise; no test matches message text. The page's claim (exception type, not wording) is what the code does.")
row("proj-grader-integrity", "2.6-autograder", f"{P} lines 245 and 259; {T} line 43-48", "PASS",
    "Page: integrity comes from the seeded instance which changes answers, not only labels. Confirmed by the 20 new seeds (distinct answers, row proj-grader-instances-differ).")
row("proj-grader-rubric", "2.6-rubric", "curriculum/02-economics-finance-core.yaml lines 578-585 (AC2 project: grading autograder)", "PASS",
    "Curriculum block: grading: autograder, atlas: A15; page header says autograded. The curriculum block is unchanged since 0c14083 (git diff --stat empty for curriculum).")

# ---- mutants
row("proj-mut-p04", "2.6-mutation", f"{MUT}/p04_piotroski_cfo_scaled_by_year_end_assets.py", "PASS",
    "Round-2 run: tools/mutate_graders.py --unit AC2 --seeds 0-9 -> KILLED by test_piotroski_signals_match_the_definitions (seed 1).")
row("proj-mut-p05", "2.6-mutation", f"{MUT}/p05_as_of_cut_excludes_a_filing_made_on_the_as_of_date.py", "PASS",
    "Round-2 run -> KILLED by test_standardize_matches_each_as_of_cut (seed 0).")
row("proj-mut-p01", "2.6-mutation", f"{MUT}/p01_previous_year_without_the_350_380_window.py", "PASS",
    "Round-2 run -> KILLED by test_previous_year_window_edges[dupont-349-False] (seed 0). Was SURVIVED in round 1.")
row("proj-mut-p02", "2.6-mutation", f"{MUT}/p02_annual_duration_narrowed_to_360_370_days.py", "PASS",
    "Round-2 run -> KILLED by test_annual_flow_duration_window_edges[350-True] (seed 0). Was SURVIVED in round 1.")
row("proj-mut-p03", "2.6-mutation", f"{MUT}/p03_ratio_result_not_checked_for_finiteness.py", "PASS",
    "Round-2 run -> KILLED by test_overflowing_quotient_raises[current_ratio-edit0] (seed 0). Was SURVIVED in round 1.")
row("proj-mut-p06", "2.6-mutation", f"{MUT}/p06_missing_val_taken_as_zero.py", "PASS",
    "Round-2 run -> KILLED by test_observation_without_a_named_field_raises[val] (seed 0). Was SURVIVED in round 1.")
row("proj-mut-p07", "2.6-mutation", f"{MUT}/p07_prior_year_balance_filled_from_current_year.py", "PASS",
    "Round-2 run -> KILLED by test_missing_previous_year_item_raises[dupont-total_assets] (seed 0). Was SURVIVED in round 1.")
row("proj-mut-summary", "2.6-mutation", "tools/mutate_graders.py --unit AC2 --seeds 0-9 (output {LOG}/mutate_all_seeds0-9_fixed.txt)".replace("{LOG}", LOG), "FAIL",
    "Round-2 output: 'mutate_graders AC2: FAIL (11/13 killed)'. All 7 round-1 mutants and the 4 new p10-p13 die; two verifier-written mutants survive: p08 (rank test, proj-mut-p08) and p09 (Piotroski signal 1 weak inequality, proj-mut-p09).",
    "Add the tests for p08 and p09 (see proj-spec-named-error-covered and proj-mut-p09). Do not weaken the grader to pass.")
row("proj-mut-p08", "2.6-mutation", f"{MUT}/p08_rank_checks_only_zero_columns.py (generated by {R2}/make_mutants_r2.py)", "FAIL",
    f"Student error: the rank check rejects only identically zero regressor columns, not linear dependence. Survives seeds 0-9 (mutate tool) and seeds 0-49 (run_candidates.py: 50 PASS lines, 0 FAIL, {LOG}/p08_p09_seeds0-49.txt). Witness {LOG}/witness_r2.txt: reference raises ValueError, mutant returns coefficients [-7.0, 0.5, 0.5].",
    "Add a test in test_project.py for a rank-deficient design with no zero column, with an assertion on ValueError.")
row("proj-mut-p09", "2.6-mutation", f"{MUT}/p09_piotroski_roa_signal_weak_inequality.py", "FAIL",
    f"Student error: Piotroski signal 1 written as ROA >= 0 (weak) instead of ROA > 0. Survives seeds 0-9 and 0-49 ({LOG}/p08_p09_seeds0-49.txt). Witness: zero latest net income gives reference signal 1 = 0 and mutant signal 1 = 1 ({LOG}/witness_r2.txt). The suite's strict-tie tests cover signals 3, 4, 5 and 7 only (test_piotroski_ties_follow_the_strict_and_weak_inequalities, test_piotroski_strict_inequality_on_a_cfo_tie).",
    "Add a tie test for signal 1 (ROA_t exactly 0 must score 0) and for signals 2, 6, 8, 9 if the page's 'strict and weak ties' claim is kept.")
row("proj-mut-p10", "2.6-mutation", f"{MUT}/p10_tag_priority_last_tag_wins.py", "PASS",
    "Student error: tag priority read backwards (last tag wins). KILLED by test_standardize_matches_the_final_numbers (seed 0). Initial version of this mutant was equivalent (its last write restored the priority); replaced with a single-line change, recorded here so the equivalent version is not counted.")
row("proj-mut-p11", "2.6-mutation", f"{MUT}/p11_modified_jones_fit_with_intercept_returns_slopes.py", "PASS",
    "Student error: modified_jones fits with an intercept and returns the slopes. KILLED by test_modified_jones_coefficients_are_the_least_squares_fit (seed 0).")
row("proj-mut-p12", "2.6-mutation", f"{MUT}/p12_balance_sheet_accruals_adds_depreciation.py", "PASS",
    "Student error: depreciation sign flipped in accruals_balance_sheet. KILLED by test_accruals_balance_sheet_number (seed 0).")
row("proj-mut-p13", "2.6-mutation", f"{MUT}/p13_as_of_tie_on_filing_date_keeps_first_listed.py", "PASS",
    "Student error: as-of selection ignores accn and keeps the first listed on a same-day filing. KILLED by test_standardize_matches_each_as_of_cut (seed 0).")

# ---- labs
row("proj-lab-1", "2.5-labs", "tests/labs/AC2/lab-AC2-project-1.py; project.html lines 54-171", "PASS",
    f"Twin under python -I -W error: output matches the page's expected block. Hand prediction (by me, before running): known on 2023-03-01 gives 2021 = 1000 (amendment filed 2023-03-20). Output {{'2021-12-31': 1000.0, '2022-12-31': 1200.0}}. Latest knowledge 990 (10-K/A) and 2022-01-31 empty match my derivation.")
row("proj-lab-2", "2.5-labs", "tests/labs/AC2/lab-AC2-project-2.py; project.html lines 175-230", "PASS",
    "Twin output equals the expected block (DuPont identity True, roe 0.255814, net margin 0.091667, nopat 120.0, roic 0.230769, accruals -0.02). Re-derived by hand: roe 110/430, net margin 110/1200, asset turnover 1200/1000, leverage 1000/430, roic 120/520, accrual (110-130)/1000. The page's '§3, Ratios and Earnings quality' cross-reference is recorded in proj-section-refs.")
row("proj-lab-3", "2.5-labs", "tests/labs/AC2/lab-AC2-project-3.py; project.html lines 297-332", "PASS",
    f"Twin output: coefficients [25081.462105, -0.821498, -0.006263]; discretionary [0.002703, -0.004013, 0.006209, 0.000235, 0.004347, -0.009161]; rank 3. Matches the page. Reference modified_jones on the same sample gives the same numbers ({LOG}/...lab3 output in r2_checks.py lab3). The fifth firm-year's discretionary part is +0.004347, as predicted.")
row("proj-labs-run", "2.5-labs", "tools/run_labs.py --unit AC2; tests/test_labs.py tests/test_run_labs.py", "PASS",
    "run_labs AC2: PASS (11/11). pytest tests/test_labs.py tests/test_page_checks.py tests/test_run_labs.py tests/test_page_smoke.py: all passed.")

# ---- numbers and citations
row("proj-numbers-134", "2.2-numbers", f"{P} line 245 ('collects 202 checks')", "PASS",
    "Round 1 said 134 and 'collects 134 checks'. The page now says 202; pytest --collect-only gives 202 on seeds 0-11 (row proj-grader-collect-count). Count is class a (computed by collection).")
row("proj-numbers-lab", "2.2-numbers", f"{P} lab outputs (lines 169-171, 225-228, 329-331)", "PASS",
    "All numeric lab outputs on the page equal the twins' printed outputs (exp1, exp2, exp3 match) and were re-derived by hand for Lab 1 and Lab 2.")
row("proj-numbers-contract-quoted", "2.2-numbers", f"{P} lines 241-257", "PASS",
    "Quoted counts and windows: 17 items (contract table has 17 rows), nine Piotroski signals (contract lines 137-141), 350 to 380 days (contract lines 'annual', 'previous year'). All match the contract text.")
row("proj-cite-registry", "2.1-citations", "references/references.json (keys penman2013financial, sloan1996stock, dechow1995detecting, piotroski2000value, beneish1999detection); tools/verify_refs.py", "PASS",
    f"verify_refs.py --offline: 'offline integrity: 560 entries, 0 problems'. verify_refs.py --unit AC2 (live): '7 of 560 entries, 0 problems' ({LOG}/verify_refs_live_AC2.txt). Registry: dechow1995detecting Crossref lists two authors; the page names none (open question kept open).")
row("proj-cite-dechow", "2.1-attribution", f"{P} lines 53-56, 299-304, 346-349; tests/labs/AC2/lab-AC2-project-3.py lines 3-4", "PASS",
    "Round 1 FAIL fixed on the learner pages: the lab comment and hypothesis cite the key and the title 'Detecting Earnings Management' and name no authors. Authors question remains OPEN (plans/AC2-open-items.md line 24). Contract line 123 still names three authors: see proj-cite-dechow-contract.")
row("proj-cite-piotroski", "2.1-attribution", f"{C} lines 164-166 (paper-content claims); registry piotroski2000value (DOI 10.2307/2672906)", "UNVERIFIABLE",
    f"The paper is not readable. curl -s -o /dev/null -w '%{{http_code}}' -L --max-redirs 0 https://doi.org/10.2307/2672906 -> 302 to https://www.jstor.org/stable/2672906?origin=crossref; JSTOR is an access-controlled publisher, and round 1 recorded a JavaScript client challenge there, which was not bypassed. The contract's claims 'the paper uses income before extraordinary items', 'the paper tests whether the firm issued common equity' and 'the paper's total long-term debt' cannot be checked. The project page itself no longer asserts them.",
    "Read the paper through an accessible copy or leave the claim as an explicit 'the contract's stated departure, not verified against the paper' with grade C.")
row("proj-cite-beneish", "2.1-attribution", f"{P} line 258; {C} 'Beneish constants' paragraph; registry beneish1999detection (DOI 10.2469/faj.v55.n5.2296)", "PASS",
    f"Constants are labelled UNCONFIRMED and graded C at best on the page, which satisfies architect ruling (c). DOI curl -> 302 to tandfonline.com (not followed further, it is an access-controlled publisher). Paper locator not confirmed. The L08 contradiction is in proj-beneish-one-source.")
row("proj-cite-sloan-penman", "2.1-attribution", f"{P} Reading list lines 346-350; registry penman2013financial, sloan1996stock", "PASS",
    "Reading list entries resolve in references.json (penman2013financial verified_by openlibrary; sloan1996stock verified_by crossref). The page makes no content claim about them.")
row("proj-beneish-labelled", "2.3-grades", f"{P} line 258; grader/instance.py BENEISH_STATUS lines 74-78", "PASS",
    "Constants labelled UNCONFIRMED and graded C at most, on the page and in instance.BENEISH_STATUS. Reference and starter repeat the label.")
row("proj-beneish-grader-honest", "2.3-grades", f"{T} test_beneish_constants_are_exported lines 158-166 (message at line 166)", "FAIL",
    "The check compares sol.BENEISH_COEFFICIENTS with the copy in instance.py. Its failure message says 'a Beneish coefficient differs from the published table' (line 166). The suite never checks against a published table (none was read), so the message claims a verification it does not make. The test's line 160 message correctly says UNCONFIRMED.",
    "Change line 166 to 'differs from the shared (unconfirmed) table in instance.py'.")
row("proj-beneish-one-source", "2.1-attribution", f"{P} line 258 ('ONE secondary source ... reproduces the values'); course/modules/AC/AC2/L08.html lines 93, 537, 559", "FAIL",
    "The page and instance say ONE secondary source. My curl of https://en.wikipedia.org/wiki/Beneish_M-score (HTTP 200, 2026-10-27) confirms that page reproduces -4.84, 0.92, 0.528, 0.404, 0.892, 0.115, -0.172, 4.679, -0.327. But L08 line 93 says 'Secondary web sources give the following candidate values' (plural) and L08 line 537 says 'The TATA weight, on which two secondary sources disagree'; no second source is cited or read anywhere in the course. L08 is not this slice; the project page is correct and L08 contradicts it.",
    "L08 lines 93 and 537 must say one secondary source (the Wikipedia page), and drop 'two sources disagree' unless a second source is read and cited (not verified in this round).")
row("proj-beneish-values-match-wiki", "2.2-numbers", f"{T}; grader/instance.py lines 79-89; grader/reference.py lines 66-76; https://en.wikipedia.org/wiki/Beneish_M-score", "PASS",
    "Class b: quoted value check. Wikipedia (HTTP 200, plain curl, 2026-10-27) equation: M = -4.84 + 0.92 DSRI + 0.528 GMI + 0.404 AQI + 0.892 SGI + 0.115 DEPI - 0.172 SGAI + 4.679 TATA - 0.327 LVGI. instance.py and reference.py equal these values. 4.697 and -2.22 appear nowhere (grep count 0 across course/modules/AC/AC2, tests/labs/AC2, atlas, plans).")
row("proj-grades-paper-claims", "2.3-grades", f"{C} lines 164-166 (paper-level claims)", "FAIL",
    "The project page no longer makes paper-level claims (round-1 lines 255-256 changed). The contract still states what the Piotroski (2000) paper uses or tests (income before extraordinary items; equity issuance test; total long-term debt) with no grade and no locator, and the paper is unreadable (proj-cite-piotroski). Under BLUEPRINT grading this is an ungraded paper-level claim.",
    "Give the three statements a grade C or lower with 'not verified against the paper', or cite a locator read from an accessible copy.")

# ---- structure, prose, data
row("proj-structure", "2.9-structure", "tools/check_pages.py --unit AC2 (PASS); project.html sections (ladder, rungs, spec, hours, grader, local, lab 3, stretch, reading, references)", "PASS",
    f"check_pages AC2: PASS ({LOG}/check_pages.txt). Sections present in order.")
row("proj-banned-phrases", "2.9-prose", f"{P}; index.html", "PASS",
    "grep -F for 'roughly half', 'about 6%', 'historically', 'typically', 'most studies', 'well known', 'TBD', 'TODO', 'lorem': 0 hits on project.html and index.html. Ellipses on project.html: '(s1, ..., s9)' and '\"score\": ...' (line 241), which are notation defined in the same sentence (the nine signals; the score is their sum), not omitted content. index.html line 110 is a cloze stem.")
row("proj-dag", "2.9-dag", "tools/check_dag.py --unit AC2 (PASS); project.html prerequisites via the hub", "PASS",
    f"check_dag AC2: PASS ({LOG}/check_dag.txt). Hub prerequisites AC1, S0, S2 (index.html) and the project's concepts are the unit's.")
row("proj-pagesmoke", "2.9-structure", "tools/page_smoke.py --unit AC2 --pages project", "PASS",
    f"'page_smoke modules/AC/AC2/project.html: PASS'; labs under 0.1 s each; grader 1.0 s in browser ({LOG}/page_smoke_project.txt).")
row("proj-lint-types", "2.9-tooling", "ruff check and ruff format --check on course/modules/AC/AC2/grader and tests/labs/AC2; mypy --no-incremental", "PASS",
    f"ruff check: 'All checks passed!'; ruff format --check: exit 0; mypy --no-incremental: 'Success: no issues found in 112 source files' ({LOG}/ruff.txt, {LOG}/mypy.txt).")
row("proj-data-honest", "2.8-data", f"{P} lines 35, 239 (SIMULATED and EDGAR pending); grader/instance.py label", "PASS",
    "Every instance is labelled SIMULATED (instance.py line 324, 395). The page states real EDGAR files are not embedded and why. No real company figure appears on the project page or in the labs (labs use literal SIMULATED data).")

# ---- new rows (round 2)
row("proj-spec-asof-named-condition", "2.6-spec", f"{P} line 243 ('a period end or an as-of date that is not in the statements')", "FAIL",
    "The page lists 'an as-of date that is not in the statements' among the named ValueError conditions. Neither the contract nor the reference raises for it: standardize(FACTS, '1990-01-01') returns {} and standardize(facts, '2099-01-01') returns the five period ends with no error (run in this round). No test checks it. An as-of date is a cut-off, not a key.",
    "Remove 'or an as-of date' from the list; keep 'an as-of date that is not an ISO date' (tested by test_invalid_facts_raise bad-as-of and impossible-as-of).")
row("proj-cite-dechow-contract", "2.1-attribution", f"{C} line 123 (modified_jones comment 'Dechow, Sloan & Sweeney (1995)')", "FAIL",
    "The contract, which the page links as the readable reference, names three authors (Dechow, Sloan & Sweeney). The registry (Crossref) lists two (Dechow, Sloan) and the question is open (plans/AC2-open-items.md line 24). Architect ruling: pages cite by key and title, and the open question is not resolved here.",
    "Replace the author string in contract line 123 with 'Dechow et al. (1995), registry key dechow1995detecting' until the open question is closed.")
row("proj-contract-scale-grader-claim", "2.6-atlas", f"{C} 'Scale' row in the Conventions table ('The grader tests the invariants, not the scaling coefficient.'); {T} test_modified_jones_is_invariant_to_money_units lines 648-650", "FAIL",
    "The contract says the grader does not test the scaling coefficient of a1. The suite does: line 648 asserts b['coefficients'][0] == c * a['coefficients'][0] (a1 scales with currency). The scaling itself is right (1/lag scales by 1/k, so a1 scales by k), so the suite is correct and the contract sentence is false.",
    "Delete 'The grader tests the invariants, not the scaling coefficient.' from the contract's Scale row, or narrow the sentence to 'the grader tests a2 and a3 invariance and a1 scaling'.")
row("proj-lab1-inclusive-overreach", "2.5-labs", f"{P} line 172 (Lab 1 interpretation: 'the as-of cut-off is inclusive')", "FAIL",
    "The interpretation says the cut-off is inclusive, but Lab 1 contains no filing dated on a cut-off date: its cuts are 2023-03-01 (amendment filed 2023-03-20, excluded) and 2022-01-31 (nothing filed). The lab shows exclusion of a later filing, not inclusion. The inclusive rule is tested by the suite (test_as_of_cut_is_inclusive_and_excludes_the_latest_year), not by the lab.",
    "Change the sentence to 'a later filing cannot leak backwards'; state inclusivity only as the contract's rule (filed <= as_of).")
row("proj-section-refs", "2.9-structure", f"{P} line 46 (§3, §5, §7), line 177 ('§3, Ratios and Earnings quality')", "FAIL",
    "The project page's headings are not numbered (no section-number span; site.js TOC does not number), so '§3', '§5' and '§7' refer to nothing a reader can locate. '§3, Ratios and Earnings quality' names a subsection that does not exist anywhere on the page (grep 'Ratios and Earnings' = 0 hits outside line 177).",
    "Link the sections by anchor (#spec, #grader-section, #stretch) and replace '(§3, Ratios and Earnings quality)' in Lab 2 with 'the Conventions section (#conventions)'.")
row("proj-spec-proxy-claims", "2.6-spec", f"{P} line 256 (proxies; 'the lessons state the size of that omission')", "PASS",
    f"Proxies match contract lines 162-166 word for word in substance. 'the lessons state the size of that omission': L03 line 524-532 and line 765 state the 50 USD m short-term debt effect (ROIC 0.1349 to 0.1287, SIMULATED, grade C) (course/modules/AC/AC2/L03.html lines 524-571 and 765).")
row("proj-learner-process-words", "2.9-prose", f"{P}; index.html", "PASS",
    "grep -F for 'this build', 'builder', 'REQUESTS', 'unit report': 0 hits on project.html and index.html. 'plans/AC2-open-items.md' is referenced 0 times on the project page and once on the hub (index.html data section).")

# ---- mutants list
mutants = [
    ("p01_previous_year_without_the_350_380_window.py", "p01: previous year is the latest earlier period end, without the 350 to 380 day window.", "test_previous_year_window_edges[dupont-349-False] (seed 0)"),
    ("p02_annual_duration_narrowed_to_360_370_days.py", "p02: a flow item counts as annual only for a duration of 360 to 370 days.", "test_annual_flow_duration_window_edges[350-True] (seed 0)"),
    ("p03_ratio_result_not_checked_for_finiteness.py", "p03: a ratio whose quotient overflows to infinity is returned instead of raising ValueError.", "test_overflowing_quotient_raises[current_ratio-edit0] (seed 0)"),
    ("p04_piotroski_cfo_scaled_by_year_end_assets.py", "p04: Piotroski CFO_t scaled by year-end total assets instead of beginning-of-year assets.", "test_piotroski_signals_match_the_definitions (seed 1)"),
    ("p05_as_of_cut_excludes_a_filing_made_on_the_as_of_date.py", "p05: the as-of cut-off is exclusive.", "test_standardize_matches_each_as_of_cut (seed 0)"),
    ("p06_missing_val_taken_as_zero.py", "p06: an observation without val is taken as zero.", "test_observation_without_a_named_field_raises[val] (seed 0)"),
    ("p07_prior_year_balance_filled_from_current_year.py", "p07: a missing previous-year total assets or equity filled from the current year in DuPont.", "test_missing_previous_year_item_raises[dupont-total_assets] (seed 0)"),
    ("p08_rank_checks_only_zero_columns.py", "p08: the rank test rejects only an all-zero regressor column; linear dependence accepted.", None),
    ("p09_piotroski_roa_signal_weak_inequality.py", "p09: Piotroski signal 1 tests ROA >= 0 instead of ROA > 0.", None),
    ("p10_tag_priority_last_tag_wins.py", "p10: tag priority read backwards (last-listed tag wins).", "test_standardize_matches_the_final_numbers (seed 0)"),
    ("p11_modified_jones_fit_with_intercept_returns_slopes.py", "p11: modified_jones fits an intercept and returns the slope coefficients.", "test_modified_jones_coefficients_are_the_least_squares_fit (seed 0)"),
    ("p12_balance_sheet_accruals_adds_depreciation.py", "p12: accruals_balance_sheet adds depreciation instead of subtracting it.", "test_accruals_balance_sheet_number (seed 0)"),
    ("p13_as_of_tie_on_filing_date_keeps_first_listed.py", "p13: as-of selection ignores accn on a same-day filing and keeps the first listed.", "test_standardize_matches_each_as_of_cut (seed 0)"),
]
mut_out = [{"description": d, "killed_by": k, "file": f"ledgers/AC2/mutants/{f}"} for f, d, k in mutants]

statuses = [r["status"] for r in rows]
counts = {s: statuses.count(s) for s in ("PASS", "FAIL", "UNVERIFIABLE")}
killed = sum(1 for m in mut_out if m["killed_by"])
verdict = "PASS" if counts["PASS"] == len(rows) and killed == len(mut_out) else "FAIL"
ids = [r["id"] for r in rows]
assert len(ids) == len(set(ids)), "duplicate ids"

fragment = {
    "unit": "AC2",
    "slice": "project (course/modules/AC/AC2/project.html, grader/{reference,starter,instance,test_project}.py, tests/labs/AC2/lab-AC2-project-{1,2,3}.py, hub project/ladder text, A15 contract consistency)",
    "round": 2,
    "verifier": "Claude Haiku 5.5 (independent project-slice verifier, round 2; did not build AC2; fresh context)",
    "pin": "bc3226e (detached worktree /tmp/verify-ac2-p; untracked: ledgers/AC2, .venv symlink)",
    "base": "round 1 fragment at 0c14083 (context only; its PASS rows were not trusted)",
    "checkout": "/tmp/verify-ac2-p",
    "scratch": "/tmp/ac2-v/project-r2/ (logs/, impls/D, lab/, wiki.html)",
    "verified_at": dt.datetime.now(dt.UTC).replace(microsecond=0).isoformat(),
    "verdict": verdict,
    "rows": rows,
    "mutants": mut_out,
    "registry_flags": [
        "dechow1995detecting: authors are an OPEN question (Crossref two; curriculum three). Not resolved. The contract (atlas/A15.contract.md line 123) still names three authors (proj-cite-dechow-contract).",
        "beneish1999detection: L08 lines 93 and 537 describe two or more secondary sources; the project page and instance say one (Wikipedia). L08 needs correcting (proj-beneish-one-source). L08 line 97 and 559 also quote a threshold of -1.78 (grade D, unconfirmed); not in this slice, but architect ruling (c) allows no other numbers from that source; the orchestrator should decide.",
        "piotroski2000value: DOI 10.2307/2672906 302 to jstor.org (not followed); paper-content claims in the contract are unverifiable (proj-cite-piotroski).",
    ],
    "freshness_flags": [],
    "notes": [
        "Round-2 scope: the suite grew 134 to 202 checks; the page says 202; collect-only gives 202 on seeds 0-11.",
        "Candidate A (round-1 implementation) fails 7 overflow tests; they are correct contract requirements, so A is not evidence of over-constraint.",
        "Beneish source: my own curl of the Wikipedia page (HTTP 200) confirms the values; I did not read Springer, ScienceDirect, JSTOR, tandfonline or any access-controlled page and recorded their redirects only.",
        "Dechow authors: not resolved; I read no author list from any source in this round.",
        "Seeds: round 1 sampled random.Random(20261027).sample(range(50),20); round 2 used random.Random(20261028).sample(range(50,1000),20), disjoint.",
        "Not checked: the hours estimate depends on my judgement of student time (no student data); the L08 lesson itself (not this slice) was read only for the Beneish status text.",
    ],
    "summary": {
        "rows": len(rows),
        "pass": counts["PASS"],
        "fail": counts["FAIL"],
        "unverifiable": counts["UNVERIFIABLE"],
        "mutants": len(mut_out),
        "mutants_killed": killed,
        "round1_mutants_killed": 7,
        "new_mutants_written": 6,
        "new_mutants_killed": 4,
        "sentence": "Round 2 project: suite 202 checks (collect and run agree on 32 seeds); reference 50/50 seeds and the 20 new seeds; B, C, D pass all; A fails only contract-required non-finite checks. All 7 round-1 mutants now die. Two of six new student-error mutants survive (p08 rank check, p09 Piotroski signal 1), and they are FAIL rows. Page and contract have defects: unmet named-error claims (rank, as-of), '§' references, placement condition, Beneish source count (L08), Dechow author string in the contract, the contract's false scale sentence, contract real-file claim, and an overreached Lab 1 interpretation.",
    },
}
out = ROOT / "ledgers" / "AC2" / "project.json"
out.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("rows", len(rows), counts, "mutants", len(mut_out), "killed", killed, "verdict", verdict)
