"""Builds ledgers/LX2/LX2-c.json (LX2-c closing delta, round 1) from the base fragment and this round's outputs.

Rows: every base row id is kept. A base row is carried (its subject byte-identical since the base pin) unless it is
in FRESH, which lists the rows re-verified this round, or it is the new FAIL row. Mutants: the 62 lab-2 files, from the
harness output (out/r1_lab2_harness.txt). Run from the checkout root.
"""

from __future__ import annotations

import json
import os
import re

ROOT = os.getcwd()
OUT = os.path.join(ROOT, "ledgers/LX2/scripts/LX2-c-r1/out")
BASE = "/Users/billyribeiro/.fanout/frags/E-LX2-c.round12.json"
CARRY_FILES = (
    "course/modules/LX/LX2/project.html, tests/labs/LX2/lab-LX2-project-1.py, -2.py, -3.py, "
    "course/assets/js/labs.js, course/assets/js/rubric.js, course/modules/LX/LX2/index.html, "
    "course/modules/LX/LX2/L04.html, notation/notation.json, curriculum/06-profession-capstone.yaml, "
    "plans/LX2-build-plan.md"
)
CARRY_HEAD = (
    f"Carried from round 12 ({CARRY_FILES} byte-identical 5db69a9b..95f3f8cb; "
    "checked this round by git diff --name-only, empty output: out/r1_identity.txt): "
)

FRESH: dict[str, str] = {
    "proj-gates-tooling": (
        "Re-run this round at 95f3f8cb (commands in scripts/LX2-c-r1/run_gates_r1.sh). ruff check . 'All checks passed!' "
        "(out/r1_ruff_check.txt); ruff format --check . '555 files already formatted' (out/r1_ruff_format.txt); "
        "mypy --no-incremental 'Success: no issues found in 386 source files' (out/r1_mypy.txt); check_pages --unit LX2 "
        "'check_pages LX2: PASS' (out/r1_check_pages_LX2.txt); check_dag --all 'check_dag LX2: PASS' exit 0 "
        "(out/r1_check_dag.txt); check_projects --unit LX2 'check_projects LX2: PASS' (out/r1_check_projects_LX2.txt); "
        "run_labs --unit LX2 'run_labs LX2: PASS (7/7)' (out/r1_run_labs_LX2.txt); run_graders --unit LX2 'no autograder "
        "(grading: rubric)' exit 0 (out/r1_run_graders_LX2.txt); pytest tests/test_labs.py tests/test_run_labs.py "
        "tests/test_page_checks.py tests/test_page_smoke.py -k 'LX2 or project' '85 passed, 329 deselected' "
        "(out/r1_pytest_subset.txt, out/r1_pytest_subset_summary.txt)."
    ),
    "proj-page-smoke": (
        "page_smoke.py --unit LX2 --pages project, run alone: 'page_smoke modules/LX/LX2/project.html: PASS' and "
        "'page_smoke LX2: PASS', exit 0 (out/r1_page_smoke_project.txt)."
    ),
    "proj-labs-twins-alone": (
        "Each twin run alone as python3 -I -W error: exit 0 and stderr size 0 for lab-LX2-project-1, -2, -3 "
        "(out/r1_twin_project_N.stderr). Stdout token-equal to the page's expected blocks: 101, 91 and 206 tokens "
        "(out/r1_page_vs_twin.txt, script scripts/LX2-c-r1/page_vs_twin_r1.py)."
    ),
    "proj-page-code-equals-twin": (
        "page_vs_twin_r1.py (out/r1_page_vs_twin.txt): lab 1 page code 86 lines, 0 differing; lab 3 109 lines, 0 "
        "differing; lab 2 79 lines, 2 differing: code line 71 'hit_rate = ___' (page line 312) and code line 73 "
        "'bias = ___' (page line 314) against the twin's Fraction(hits, horizon) and Fraction(sum(errors), horizon)."
    ),
    "proj-rung1-hypothesis-and-steps": (
        "Lab 1 twin output (out/r1_twin_project_1.stdout): hits 4 of 8, hit rate 0.5000, bias 0.2500, edge months "
        "[15, 19]; errors per month t=13..20 are +1, -3, +2, 0, -4, +3, -2, +5 (the list the page gives). Re-derived by "
        "rederive_r12.py re-run (out/r1_rederive_r12_rerun.txt, 'L1: errors [1, -3, 2, 0, -4, 3, -2, 5] hits 4 hit rate "
        "0.5000 bias 0.2500 edge [15, 19]') and identical to the base output."
    ),
    "proj-rung2-numbers-and-claims": (
        "Lab 2 twin output (out/r1_twin_project_2.stdout): hits 4 of 6, 0.6667, 0.1667, edge months [14, 17]. "
        "rederive_r12.py re-run: 'L2: errors [-1, 2, 6, 1, -2, -5] hits 4', 'L2 mean absolute error (claim 2.8333): "
        "2.8333', 'L2 hit count over 8 (claim 0.5000): 0.5000' (out/r1_rederive_r12_rerun.txt). project.html lines 241 "
        "and 321-331 agree."
    ),
    "proj-rung2-instant-check-mutants": (
        "scripts/LX2-c-r1/lab2_harness_r1.py (labs.js compareOutput rule as read at course/assets/js/labs.js lines "
        "22-58; labs.js byte-identical) over all 62 files ledgers/LX2/mutants/*lab2*.py: 'files 62', KILLED 46, "
        "SURVIVED 16 = 7 correct alternatives + 9 student-error survivors (out/r1_lab2_harness.txt). Page examples at "
        "project.html line 332 reproduce: mut-lab2-hit-over-8 prints 0.5000 (token 70), mut-lab2-bias-mean-abs prints "
        "2.8333 (token 74). The 46 kills match the base partition (base: 46 killed, 9 student-error survivors, 7 "
        "alternatives)."
    ),
    "proj-rung2-student-error-mutants": (
        "Survivors this round (out/r1_lab2_harness.txt): r10_lab2_bias_absolute_error_sum.py and "
        "r10_lab2_bias_absolute_value_of_sum_per_H.py (abs of the error sum; the window sum is +1, so the printed block "
        "is identical; the second's output diffed token-equal to the twin, out/r1_twin_project_2.stdout), "
        "r10_lab2_hit_band_three.py (no error of size 3 in this window), r6_lab2_float_format_ties_even.py, "
        "r6_lab2_round_half_even_ties.py, r6_lab2_round_half_toward_plus_infinity.py, r7_lab2_rounds_through_python_round.py "
        "(tie rules: project.html line 332 names them), r6_lab2_hard_coded_printed_values.py (line 332: 'a blank typed as "
        "the value it prints passes'), r8_lab2_hit_rate_ceiling_four_places.py (printed-output limit; line 45 'compares "
        "the printed output only'). Judgment carried from rounds 8 to 12: these are the disclosed printed-output-only "
        "limits, so no FAIL on their own. The page's claim that contradicts them is the separate FAIL row "
        "proj-rung2-table-wrong-blank-claim (line 535)."
    ),
    "proj-rung2-alternatives": (
        "The seven correct alternatives all survive the harness (exit 0, whole-block compare passes, "
        "out/r1_lab2_harness.txt): alt-lab2-float-division.py, alt_r9_lab2_fmean_bias_error_list_hits.py, "
        "alt_r10_lab2_squared_error_band.py, alt_r10_lab2_decimal_half_up_quantize.py, alt_r12_lab2_bias_sum_over_len.py, "
        "alt_r12_lab2_hit_rate_generator_sum.py, alt_r12_lab2_statistics_fmean_bias.py. Also ledgers/LX2/scripts/LX2-c-r8/"
        "alt_r8_a1_len_float_decimal.py: exit 0 and token-identical to the twin's stdout (out/r1_alt_r8_run.txt)."
    ),
    "proj-rung2-alt-fixture": (
        "All 62 lab-2 files were run as complete modules by the harness (python -I -W error; every alternative exits 0). "
        "The r12 files (line 1 read this round) carry one-line docstrings: 'Student error (bias): ...' (4 files) and "
        "'Alternative (correct): ...' (3 files). Caveat, not a finding: 45 older lab-2 files (mut-*, r3-r8) open with a "
        "multi-line docstring; the one-line docstring rule in the mutate_graders docstring is for grader mutants, and LX2 "
        "has no autograder (out/r1_run_graders_LX2.txt)."
    ),
    "proj-lab3-numbers": (
        "rederive_r12.py re-run output identical to the base's rederive_r12.out (out/r1_rederive_r12_rerun.txt): 'H 24 "
        "hits 13 hit rate 0.5417', 'bias 2.1250 sum 51', 'L3 edge months [14, 15, 16, 19, 22, 24, 26]', 'largest |e| 8 "
        "month 34 | months with |e|=8: [34, 35]', 'calibration ... sum 11 bias 0.9167'. Lab 3 twin output (out/"
        "r1_twin_project_3.stdout) prints the same 'Part B', 'Part C', 'Part D', 'Part E' and 'Part F' lines. Expected "
        "block token-equal to twin stdout (206 tokens, out/r1_page_vs_twin.txt)."
    ),
    "proj-exemplar-a-numbers": (
        "rederive_r12.py re-run: 'errors 28-36 all positive: True min 3 max 8' (line 572); 'integers s with "
        "round(s/12,4)==0.9167: [11]' (line 572); 'split 13-27: sum -3 n 15 hits 13 ... hit rate 0.8667' (line 585); "
        "'split 28-36: sum 54 n 9 hits 0 bias 6.0000' (line 585); 'errors 25-36 sum: 56 /12 = 4.6667' (line 610); 'strict "
        "band hits: 6 rate 0.2500' (line 586). The twin's Part A (out/r1_twin_project_3.stdout) gives the same months 28 to "
        "36 errors 7, 6, 4, 3, 7, 6, 8, 8, 5."
    ),
    "proj-exemplar-b-numbers": (
        "rederive_r12.py re-run: 'errors 13-27 within [-3,3]: True' (line 638); 'H 24 hits 13 hit rate 0.5417' (line 650); "
        "'bias 2.1250 sum 51' (line 650); window of 24 months (line 662) from the lab 3 twin output."
    ),
    "proj-citations-registry": (
        "references/references.json changed in the delta: generated_at, and used_by of black1973pricing gained FC2. The six "
        "data-cite keys of project.html (cfandcode, frb2026fed, gpo1983dirks, gpo1997united, gpondsecurities, "
        "gpondsecuritiesb) are present at both pins and their entries are identical (python compare of git show "
        "5db69a9b vs HEAD). verify_refs.py --offline: 'offline integrity: 560 entries, 0 problems' exit 0 "
        "(out/r1_verify_refs_offline.txt). Live verify_refs not run: no cited record changed."
    ),
    "proj-r10-sources-refetch": (
        "Re-fetched by plain curl on 2026-11-09 (HTTP 200) from https://www.federalreserve.gov/supervisionreg/srletters/: "
        "SR2602a1.pdf sha256 209ce4c1... and SR2602.pdf sha256 956b3bc6... (both identical to the base's recorded values); "
        "sr2602.htm sha256 d7ef6c9a... (base recorded 05af406d... in round 10 and b5c0e0a9... in round 12; the htm changed, "
        "and every cited sentence is present in it, see proj-source-supersession). registry frb2026fed url sr2602.htm, "
        "verified_by issuer, record identical at both pins."
    ),
    "proj-dag-and-links": (
        "check_dag.py --all: 'check_dag LX2: PASS', exit 0 (out/r1_check_dag.txt); check_pages --unit LX2 PASS "
        "(out/r1_check_pages_LX2.txt) for link targets. project.html and L04.html byte-identical 5db69a9b..95f3f8cb; "
        "curriculum.json changed in another unit's brief only (see r12-delta-scope)."
    ),
    "proj-source-supersession": (
        "Sources re-fetched this round (proj-r10-sources-refetch). pdftotext -layout of SR2602.pdf (combined.txt) contains "
        "'supersedes and replaces SR letter 11-7' (cover letter, PDF page 1); sr2602.htm contains 'which supersedes and "
        "replaces SR letter 11-7, Guidance on Model Risk Management (issued April 4, 2011) and SR letter 21-8' and the "
        "'Supersedes:' list after the signature. Page line 363 claim matches."
    ),
    "proj-source-applicability": (
        "sr2602.htm: 'Applicability: This letter is expected to be most relevant to banking organizations with over $30 "
        "billion in total assets regulated by the Federal Reserve.' Page line 364 (data-locator 'cover letter, paragraph "
        "headed Applicability') and its paraphrase match."
    ),
    "proj-source-attachment": (
        "scripts/LX2-c-r1/sources_check_r1.py (out/r1_sources_check.txt): 'Validating "
        "conceptual soundness' PDF page 8; 'Outcomes analysis compares' 9; 'established performance thresholds' 9; 'Sound "
        "validation identifies' 7; 'Ongoing model monitoring involves' 9; 'includes an assessment of a model' 7; headings "
        "'Conceptual Soundness' 8, 'Outcomes Analysis' 9, 'Ongoing Model Monitoring' 9; grep 'Limitations' returns nothing. "
        "Printed page = PDF page as the base recorded."
    ),
    "proj-exemplar-b-unread-requirement": (
        "SR2602a1.pdf PDF page 2 contains 'This guidance does not set forth enforceable standards or prescriptive "
        "requirements' (section I). Page line 691 annotation consistent."
    ),
    "proj-attachment-quote-locators": (
        "Locators at project.html lines 350-353, 364, 622 and 686 checked against the attachment page map and the cover "
        "letter sentences re-fetched this round (proj-source-attachment, proj-source-supersession)."
    ),
    "proj-rung3-sr26-standard": (
        "project.html lines 347-360 and 363-367 against the re-fetched SR 26-2 files: attachment pages and cover-letter "
        "sentences as in proj-source-attachment, proj-source-applicability and proj-source-supersession."
    ),
    "proj-claim-span-paraphrase": (
        "project.html line 363 paraphrase 'supersedes and replaces SR letter 11-7 and SR letter 21-8' matches the cover "
        "letter in sr2602.htm and combined.txt (proj-source-supersession)."
    ),
    "proj-mutate-graders-na": (
        "tools/mutate_graders.py --unit LX2: exit 0 with no output (out/r1_mutate_graders_LX2.txt); LX2's project grading is "
        "rubric ('no autograder (grading: rubric)' from run_graders.py), so the tool selects no unit."
    ),
    "proj-r7-new-mutants": (
        "Harness (out/r1_lab2_harness.txt): r7_lab2_edge_months_at_or_beyond_band KILLED (expected 91 tokens, got 93); "
        "r7_lab2_one_sided_band KILLED (token 61 'hit=yes' vs 'hit=no'); r7_lab2_rounds_through_python_round SURVIVES "
        "(tie rule, line 332); r7_lab2_window_one_month_early KILLED (expected 91 tokens, got 90)."
    ),
    "proj-r8-new-mutants": (
        "Harness: r8_lab2_bias_hit_errors_only KILLED (token 74 0.0000 vs 0.1667); r8_lab2_bias_truncated_to_whole_units "
        "KILLED (token 74); r8_lab2_hit_rate_ceiling_four_places SURVIVES (printed-output limit, carried); "
        "r8_lab2_hit_rate_counts_edge_months KILLED (token 70 0.3333 vs 0.6667); r8_lab2_hit_rate_over_horizon_plus_one "
        "KILLED (token 70 0.5714 vs 0.6667)."
    ),
    "proj-r9-new-mutants": (
        "Harness: r9_lab2_bias_mean_of_squared_errors KILLED (token 74 11.8333); r9_lab2_bias_negated_when_error_sum_positive "
        "KILLED (token 74 -0.1667); r9_lab2_edge_list_tests_one_unit KILLED (token 90 '[13,' vs '[14,'); "
        "r9_lab2_hit_band_half_open_upper KILLED (token 41 'hit=no' vs 'hit=yes')."
    ),
    "proj-r10-new-mutants": (
        "Harness: r10_lab2_hit_rate_integer_division KILLED (token 70 0.0000 vs 0.6667); r10_lab2_edge_list_prints_all_hits "
        "KILLED (93 tokens vs 91); r10_lab2_bias_subtracts_hit_count KILLED (token 74 -0.5000 vs 0.1667); "
        "r10_lab2_bias_absolute_error_sum and r10_lab2_bias_absolute_value_of_sum_per_H SURVIVE (abs of the error sum; "
        "see proj-rung2-student-error-mutants); r10_lab2_hit_band_three SURVIVES (no |e| = 3 in this window); "
        "r10_lab2_forecast_slope_one KILLED (90 tokens); r10_lab2_window_starts_month_twelve KILLED (90 tokens)."
    ),
    "proj-r9-alternative": (
        "alt_r9_lab2_fmean_bias_error_list_hits.py SURVIVES the harness (exit 0, whole-block compare passes; "
        "out/r1_lab2_harness.txt)."
    ),
    "proj-r10-alternative": (
        "alt_r10_lab2_squared_error_band.py and alt_r10_lab2_decimal_half_up_quantize.py SURVIVE the harness "
        "(out/r1_lab2_harness.txt)."
    ),
    "proj-rung2-alt-decimal": (
        "ledgers/LX2/scripts/LX2-c-r8/alt_r8_a1_len_float_decimal.py: python -I -W error exit 0; stdout token-identical to the "
        "twin's stdout (out/r1_alt_r8_run.txt)."
    ),
    "proj-r8-alternative-lab2-len-float-decimal": (
        "Same file as proj-rung2-alt-decimal: exit 0 and token-identical to the twin's stdout (out/r1_alt_r8_run.txt)."
    ),
    "r12-delta-scope": (
        "git diff --name-only 5db69a9b HEAD over project.html, the three project twins, labs.js, rubric.js, index.html, "
        "L04.html, notation.json, 06-profession-capstone.yaml and LX2-build-plan.md: empty (out/r1_identity.txt). Changed "
        "inputs outside the slice: references/references.json (proj-citations-registry); curriculum/curriculum.json (JSON "
        "leaf diff: only /parts[1]/modules[2]/project/brief, the 01-foundations 'Covariance-matrix doctor' project, not "
        "LX2; LX2's project entry unchanged); pyproject.toml (ruff extend-exclude adds ledgers/*/lab-mutants; ruff PASS). "
        "LX2 lesson files and cards (L01-L03, cards.json, lab-LX2-L03-1.py) changed in the delta and belong to slices a and b; "
        "not covered here."
    ),
    "r12-gates-pages-dag-projects-labs": (
        "Same commands as proj-gates-tooling, re-run this round: check_pages LX2 PASS, check_dag --all exit 0, check_projects "
        "LX2 PASS, run_labs LX2 PASS (7/7) (out/r1_check_pages_LX2.txt, out/r1_check_dag.txt, out/r1_check_projects_LX2.txt, "
        "out/r1_run_labs_LX2.txt)."
    ),
    "r12-page-smoke-project": (
        "page_smoke --unit LX2 --pages project alone: PASS, exit 0 (out/r1_page_smoke_project.txt)."
    ),
    "r12-twins-alone": (
        "Twins alone under python3 -I -W error: exit 0, stderr 0 bytes, stdout token-equal to expected blocks (out/r1_twin_project_N.*, "
        "out/r1_page_vs_twin.txt)."
    ),
    "r12-page-code-vs-twin": (
        "page_vs_twin_r1.py (out/r1_page_vs_twin.txt): lab 1 and lab 3 0 differing lines; lab 2 differs in code lines 71 and 73 "
        "(the two blanks), as the base recorded."
    ),
    "r12-rederive-numbers": (
        "rederive_r12.py re-run at this pin (ledgers/LX2/scripts/LX2-c-r12/rederive_r12.py); output diffed against the committed "
        "rederive_r12.out: identical (out/r1_rederive_r12_rerun.txt; diff empty)."
    ),
    "r12-attachment-quotes": (
        "Quotes in project.html lines 350-353 and 364 re-checked this round against SR2602a1.pdf (pdftotext page map) and "
        "sr2602.htm (proj-source-attachment, proj-source-applicability)."
    ),
    "r12-cover-letter-sentences": (
        "project.html lines 363-364 and 622 re-checked this round against sr2602.htm: 'supersedes and replaces SR letter 11-7, "
        "Guidance on Model Risk Management (issued April 4, 2011) and SR letter 21-8'; 'Applicability: ... over $30 billion in "
        "total assets regulated by the Federal Reserve'; Supersedes list after the signature."
    ),
    "r12-mutants-existing-rerun": (
        "Harness over all 62 files (out/r1_lab2_harness.txt): KILLED 46, SURVIVED 16 (7 alternatives + 9 student-error "
        "survivors). Partition as in proj-rung2-instant-check-mutants."
    ),
    "r12-mutants-new-student-error": (
        "The four r12 student errors, one-line docstrings (line 1): r12_lab2_bias_uses_mean_realised_value KILLED (token 74 "
        "130.8333 vs 0.1667); r12_lab2_hit_count_adds_edge_months KILLED (token 70 1.0000 vs 0.6667); "
        "r12_lab2_hit_count_counts_only_upper_side KILLED (token 70 0.8333 vs 0.6667); "
        "r12_lab2_hit_rate_denominator_excludes_edge_months KILLED (token 70 1.0000 vs 0.6667). Each diffed against the twin "
        "(one changed expression each)."
    ),
    "r12-alternatives-new": (
        "The three r12 alternatives (diffed against the twin): alt_r12_lab2_bias_sum_over_len.py divides by len(errors), which "
        "is 6 = H here (the errors list is the six-month window); alt_r12_lab2_hit_rate_generator_sum.py sums a generator and "
        "divides by H; alt_r12_lab2_statistics_fmean_bias.py uses statistics.fmean for the bias (a float that prints the same "
        "under half-up). All three SURVIVE the harness (exit 0, out/r1_lab2_harness.txt)."
    ),
    "r12-verify-refs": (
        "verify_refs.py --offline: 'offline integrity: 560 entries, 0 problems' exit 0 (out/r1_verify_refs_offline.txt). "
        "Live run not repeated: no cited record changed (proj-citations-registry)."
    ),
    "r12-ruff-mypy-pytest": (
        "ruff check . 'All checks passed!'; ruff format --check . '555 files already formatted'; mypy --no-incremental 'Success: "
        "no issues found in 386 source files'; pytest subset '85 passed, 329 deselected' (out/r1_ruff_*.txt, out/r1_mypy.txt, "
        "out/r1_pytest_subset_summary.txt). pyproject.toml changed in the delta (ruff exclude); the ruff gate was re-run."
    ),
    "r12-run-graders-mutate": (
        "run_graders.py --unit LX2: 'run_graders LX2: no autograder (grading: rubric)' exit 0; mutate_graders.py --unit LX2 "
        "exit 0, no output (out/r1_run_graders_LX2.txt, out/r1_mutate_graders_LX2.txt)."
    ),
    "r12-curriculum-brief-scope": (
        "curriculum/06-profession-capstone.yaml byte-identical; curriculum.json LX2 project entry unchanged (JSON leaf diff, only "
        "/parts[1]/modules[2]/project/brief differs). render_curriculum.py re-run: 'wrote curriculum/curriculum.json and "
        "CURRICULUM.md', then git diff --exit-code clean (exit 0, out/r1_render_curriculum.txt). build_site.py --check: "
        "'site data current: 6 outputs' exit 0 (out/r1_build_site_check.txt)."
    ),
}

NEW_FAIL = {
    "id": "proj-rung2-table-wrong-blank-claim",
    "check": "2.6 claim about the rung-2 instant check (hours table cell): what a wrong blank prints",
    "location": "course/modules/LX/LX2/project.html line 535 (table#hours, row 'Rung 2, completion problem and its instant check')",
    "status": "FAIL",
    "evidence": (
        "The cell says: 'Two blanks; the time goes into explaining why each wrong blank prints a different block.' On this "
        "window that is false. The student error r10_lab2_bias_absolute_value_of_sum_per_H.py fills the bias blank with "
        "Fraction(abs(sum(errors)), horizon) (mutant line 53); run alone it prints the same block token for token as the "
        "twin and the expected block (exit 0; diff against out/r1_twin_project_2.stdout empty; harness line "
        "'SURVIVES r10_lab2_bias_absolute_value_of_sum_per_H.py' in out/r1_lab2_harness.txt). r10_lab2_bias_absolute_error_sum.py "
        "(abs of the error sum), r6_lab2_round_half_even_ties.py, r7_lab2_rounds_through_python_round.py and "
        "r8_lab2_hit_rate_ceiling_four_places.py also print the identical block. The page contradicts the cell at line 332 "
        "('a blank typed as 0.6667 or 0.1667 prints the same block and passes, so the check does not grade the expression') "
        "and line 45 ('compares the printed output only'). No other 'different block' or 'wrong blank' sentence exists in "
        "course/modules/LX/LX2/*.html (grep). The arithmetic of table#hours is not affected (proj-hours carried)."
    ),
    "fix": (
        "Replace the cell text with a true statement, for example: 'Two blanks; the check compares the printed output only, "
        "so a wrong expression that prints the same block passes (see the rung 2 note).' Then re-run check_pages --unit LX2, "
        "page_smoke --unit LX2 --pages project and the lab-2 harness (scripts/LX2-c-r1/lab2_harness_r1.py) in a new round."
    ),
    "verdict_note": "Found by re-running the standing mutant set against the page's claims (ruling 37); not a new-defect hunt.",
}


def mutant_rows(harness_path: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    with open(harness_path, encoding="utf-8") as fh:
        for line in fh:
            m = re.match(r"^(KILLED|SURVIVES)\s+(\S+\.py)\s*(.*)$", line.rstrip("\n"))
            if not m:
                continue
            status, name, detail = m.group(1), m.group(2), m.group(3).strip()
            mut_path = os.path.join(ROOT, "ledgers/LX2/mutants", name)
            first = open(mut_path, encoding="utf-8").read().split("\n")[0].strip()
            description = first.strip('"').strip()
            if status == "KILLED":
                killed_by = f"KILLED by lab2_harness_r1.py: {detail or 'exit non-zero'}"
            elif name.startswith(("alt", "alt_")):
                killed_by = "SURVIVES (correct alternative; over-constraint check passes)"
            else:
                killed_by = (
                    "SURVIVES (student error on this window; disclosed printed-output-only limit, project.html lines 45 and "
                    "332; carried judgment, see proj-rung2-student-error-mutants)"
                )
            rows.append({"name": name, "description": description, "killed_by": killed_by})
    return rows


def main() -> int:
    base = json.load(open(BASE, encoding="utf-8"))
    base_ids = {r["id"] for r in base["rows"]}
    assert set(FRESH) <= base_ids, sorted(set(FRESH) - base_ids)
    rows: list[dict[str, str]] = []
    carried = 0
    fresh_n = 0
    for r in base["rows"]:
        rid = r["id"]
        if rid in FRESH:
            text = FRESH[rid]
            rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": "PASS", "evidence": text})
            fresh_n += 1
            continue
        base_ev = re.sub(r"^Carried from round \d+ \(.*?\):\s*", "", r["evidence"])
        base_ev = re.sub(r"\s*Round 12: .*$", "", base_ev)
        if rid == "r12-blind-exemplar-scoring":
            prefix = (
                "Carried from round 12 (course/modules/LX/LX2/project.html byte-identical; ruling 23: no dedicated blind "
                "scorer file for LX2 exists in ~/.fanout/blind/, so the base calibration result is carried. The stripped "
                "text ledgers/LX2/scripts/LX2-c-r12/exemplars_stripped_r12.txt was added after 5db69a9b, so this carries the "
                "result, not that file's bytes): "
            )
        elif rid in ("proj-exemplar-calibration",):
            prefix = (
                "Carried from round 12 (course/modules/LX/LX2/project.html byte-identical 5db69a9b..95f3f8cb; ruling 23: no "
                "dedicated blind scorer file for LX2 in ~/.fanout/blind/, so the base calibration rows are carried): "
            )
        else:
            prefix = CARRY_HEAD
        rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": "PASS", "evidence": prefix + base_ev})
        carried += 1
    rows.append(
        {
            "id": NEW_FAIL["id"],
            "check": NEW_FAIL["check"],
            "location": NEW_FAIL["location"],
            "status": NEW_FAIL["status"],
            "evidence": NEW_FAIL["evidence"],
            "fix": NEW_FAIL["fix"],
        }
    )
    mutants = mutant_rows(os.path.join(OUT, "r1_lab2_harness.txt"))
    counts = {"PASS": sum(1 for r in rows if r["status"] == "PASS"), "FAIL": 1}
    frag = {
        "unit": "LX2",
        "slice": "LX2-c",
        "round": 1,
        "verifier": "Claude Haiku 5.5, independent verifier for LX2-c, closing delta round 1 (did not build LX2)",
        "pin": "95f3f8cb21c2cd9fc904430bd30a6b734d01f672",
        "base": (
            "E-LX2-c.round12.json (pin 5db69a9bee460736c318ebfacc7200ee5a6eb0f0, verdict PASS, 101 rows). Delta "
            "5db69a9b..95f3f8cb over the slice paths and the inputs the base rows cite. The base's round 12 files "
            "(ledgers/LX2/scripts/LX2-c-r12/*, mutants r12_lab2_* and alt_r12_lab2_*) are not in the 5db69a9b tree; they were "
            "added later and are re-verified here."
        ),
        "checkout": "/Users/billyribeiro/.fanout/wt/verifyF31-LX2-c (detached at 95f3f8cb; .venv symlinked; vendor copied)",
        "scratch": "/tmp/lx2c-r1-src-closing (SR2602a1.pdf, SR2602.pdf, sr2602.htm fetched by plain curl 2026-11-09; a1.txt, combined.txt)",
        "verified_at": "2026-11-09T16:25:40+00:00",
        "verdict": "FAIL",
        "rows": rows,
        "mutants": mutants,
        "registry_flags": [],
        "freshness_flags": [
            "sr2602.htm changed again: sha256 d7ef6c9a2834181ed3070d38b863818a3f19715baaeb10cc6051a5594b8c0bb9 on 2026-11-09 "
            "(base recorded 05af406d... in round 10 and b5c0e0a9... in round 12). The PDFs are byte-identical to the recorded "
            "hashes. Every cited sentence is present in the current htm and PDF, so no page change is needed.",
            "references/references.json generated_at moved to 2026-11-09T03:40:24+00:00; the cited frb2026fed record is identical.",
        ],
        "notes": [
            "Verdict FAIL: one row, proj-rung2-table-wrong-blank-claim (project.html line 535). Every other row PASS, carried or "
            "re-verified this round. Fix is one clause in project.html; the slice then needs one more delta round.",
            "Scope (rulings 30 and 37): rows of the base whose subject changed were re-verified (references, the gate rows, the "
            "mutant set incl. the seven r12 files added after the base pin, the source rows); all other base rows are carried "
            "with the carry prefix. No new mutants were written; the standing set of 62 lab-2 files was re-run.",
            "Standing-set result: 46 KILLED, 16 SURVIVED = 7 correct alternatives + 9 student-error survivors. The 9 are the "
            "same as the base. Their judgment (disclosed printed-output-only limits, project.html lines 45 and 332) is carried "
            "from rounds 8 to 12 and is not re-litigated here. Caveat: the carried judgment is what keeps these 9 from being "
            "FAIL rows; the line 535 cell contradicts it, which is why the FAIL row exists.",
            "Ledger format note: tools/ledger.py counts any non-empty killed_by as killed, so the SURVIVES entries in mutants "
            "are counted by mutants_killed. The base fragment used the same format. Read the killed_by text, not the count.",
            "Exemplar calibration: ruling 23 requires a dedicated blind scorer; none exists for LX2 in ~/.fanout/blind/ (files "
            "present: BK4, CS2, E1, E3, E4, FC2, LX1, M5, PC3). The base calibration rows are carried, with the base's own caveat "
            "(annotations were seen earlier in that round; stripped-text pass, not a dedicated blind scorer).",
            "Provenance: the base pin 5db69a9b does not contain the base round's r12 mutants (7 files), the LX2-c-r12 scripts (23 "
            "files) or the r12 evidence named in its rows. git ls-tree at 5db69a9b shows 55 lab-2 mutant files. This verifier "
            "re-verified those rows at 95f3f8cb.",
            "Not checked: lesson pages, cards and lab twins of L01-L03 (slices a and b); the live verify_refs run; a browser "
            "run of the self-assessment form (rubric.js stores scores locally and was not executed); the lab-2 harness is a "
            "reimplementation of the labs.js compare rule, not the browser code path (page_smoke runs the labs in Pyodide, PASS).",
            "Scope limit: this round did not hunt for new defects outside the listed rows and the standing mutant set. The line "
            "535 FAIL was surfaced by the standing-set rerun against the page's own claims.",
            "Not run: mutants authored this round (none, ruling 37); no commits; no edits to course, tool, test or reference files.",
        ],
        "summary": (
            f"LX2-c closing delta round 1: FAIL. Rows {len(rows)}: PASS {counts['PASS']}, FAIL 1 "
            f"(proj-rung2-table-wrong-blank-claim, project.html line 535). Re-verified this round: {fresh_n} rows; carried: "
            f"{carried} rows. Mutants: 62 lab-2 files, 46 KILLED, 16 SURVIVED (7 correct alternatives, 9 disclosed "
            "student-error survivors). Gates at 95f3f8cb: ruff, format, mypy, check_pages, check_dag, check_projects, run_labs, "
            "run_graders, mutate_graders, page_smoke (project), verify_refs --offline, pytest subset, render_curriculum, "
            "build_site --check all PASS or exit 0."
        ),
    }
    out_path = os.path.join(ROOT, "ledgers/LX2/LX2-c.json")
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(frag, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    print("rows", len(rows), "fresh", fresh_n, "carried", carried, "mutants", len(mutants))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
