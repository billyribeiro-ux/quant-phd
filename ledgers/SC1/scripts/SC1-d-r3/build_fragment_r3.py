"""Write the round-3 SC1 slice-d fragment (ledgers/SC1/SC1-d.json) and validate it with tools/ledger.py.

Run from the repo root: .venv/bin/python ledgers/SC1/scripts/SC1-d-r3/build_fragment_r3.py
"""

from __future__ import annotations

import json
import sys
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "tools"))
import ledger  # noqa: E402

R = "ledgers/SC1/scripts/SC1-d-r3/out"


def row(rid, check, location, status, evidence, fix=""):
    return {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence, "fix": fix}


ROWS = [
    row("SC1-d-ladder", "2.6-ladder", "course/modules/SC/SC1/project.html:40-49, 155, 297-300, 602-609",
        "PASS", "Read the ladder in round 3. Rung 1 = Lab 1 (annotated at :155), rung 2 = Lab 2 (completion, graded "
        f"instantly), rung 3 = :207-291 (spec, autograder, rubric), rung 4 = :602-609. check_projects SC1 PASS ({R}/check_projects.txt)."),
    row("SC1-d-grading-mode", "2.6-grading", "project.html:219; curriculum/03-markets.yaml (SC1 project grading: both)",
        "PASS", "project.html:219 'Both the autograder and the rubric apply', 128 tests; curriculum grading: both. check_projects PASS."),
    row("SC1-d-spec-signatures", "2.6-spec", "project.html:215 vs grader/starter.py:16-38", "PASS",
        "The five names, parameters and return types on :215 equal starter.py:16, 21, 26, 31, 36 (read in full)."),
    row("SC1-d-spec-rounding-statement", "2.2-numbers / 2.9-prose", "project.html:217 vs :57-67, :142 (Lab 1) and tests/labs/SC1/lab-SC1-project-1.py:141",
        "PASS", "Round-2 FAIL resolved. :217 now allows two kinds of non-six-decimal output: H and a as generated (three decimals), "
        "and a difference of computed values in exponent form to three significant digits. Lab 1 prints H = 2.083, a = 2.474 "
        "(lab line 140) and 9.13e-15 via {:.2e} (lab line 141), which is three significant digits. Lab 1 docstring (twin lines 3-8) matches."),
    row("SC1-d-hours", "2.6-hours", "project.html:33, 268-274; course/modules/SC/SC1/index.html:29-42", "PASS",
        "data-hours-project=28; table 2+3+10+8+3+2 = 28; hub data-hours-lessons 72 + project 28 = 100. My estimates: rung 1 1.5-2.5 h, "
        "rung 2 2-3 h, proofs 8-12 h, engine with tests 6-10 h, report 2-4 h, self-assessment 1-2 h; midpoint 27.0 h, 3.6% from 28."),
    row("SC1-d-spec-grid-table", "2.6-spec", "project.html:431, 449", "PASS",
        "The brief lists the grids 1, 4, 16, 64, 256 with a standard error at each; C5 level 4 says 'for every grid the brief lists'. No table is referenced."),
    row("SC1-d-spec-tolerance-statement", "2.6-spec", "project.html:228; grader/test_project.py:141, 147", "PASS",
        "project.html:228 states the closed-form tolerance 1e-10; test_project.py:141 uses 1e-10. The quadrature tolerance 1e-8 is stated at :57 and used at test_project.py:147."),
    row("SC1-d-ag-reference", "2.6-autograder", "course/modules/SC/SC1/grader/reference.py; tools/run_graders.py", "PASS",
        f"`tools/run_graders.py --unit SC1 --seeds 0-49` -> 'run_graders SC1: PASS (reference 50/50 seeds, slowest 0.4 s)' ({R}/run_graders.txt). "
        "The reference fails outside 0-49: see SC1-d-ag-band-overconstraint."),
    row("SC1-d-ag-starter", "2.6-autograder", "course/modules/SC/SC1/grader/starter.py", "PASS",
        f"starter copied as bm_checks.py with the suite (128 collected): '124 failed, 4 passed' ({R}/starter_run_r3.txt). The 4 passing tests "
        "are instance-only tests that never call the engine."),
    row("SC1-d-ag-instances", "2.6-autograder", "course/modules/SC/SC1/grader/instance.py; ledgers/SC1/scripts/SC1-d-r2/instance_survey_r2.py", "PASS",
        f"Re-run in round 3 (instance.py byte-identical to the round-2 pin): invalid seeds [], 49 distinct levels, 50 distinct horizons, 50 distinct "
        f"continuous tails at 6 dp, labels {{SIMULATED}} ({R}/instance_survey_r3.txt). Second instance is seed + 7919 (test_project.py:34)."),
    row("SC1-d-ag-count", "2.6-autograder", "course/modules/SC/SC1/grader/test_project.py; project.html:7, 219, 290", "PASS",
        f"`pytest --collect-only -q` in a clean scratch copy: 128 tests collected ({R}/collect_only.txt). The page states 128 at :7, :219 and :290."),
    row("SC1-d-ag-messages", "2.6-autograder", "course/modules/SC/SC1/grader/test_project.py:40-78, :109-463", "PASS",
        "Read every failure message. Helpers carry __tracebackhide__. No message prints an expected value; messages that echo inputs (e.g. :421, :439) "
        "echo parameters only. Named ValueError tests cover only the conditions in project.html:231. New message at :350-352 names the property."),
    row("SC1-d-ag-overconstraint", "2.6-autograder", "course/modules/SC/SC1/grader/test_project.py:245-246; project.html:217", "PASS",
        "The round-2 failure (enumeration of 2**41 walks for n = 41) is excluded by the new sentence at project.html:217, so the enumeration probe "
        f"(alt2b, TIMEOUT after 240 s at seed 0, {R}/alternatives_r3.txt) is no longer a conforming implementation. The new over-constraint that this "
        "sentence creates is SC1-d-spec-n41-method."),
    row("SC1-d-ag-alternatives-ok", "2.6-autograder", "ledgers/SC1/scripts/SC1-d-r3/alternatives/alt1-alt7", "PASS",
        f"run_alternatives_r3.py over seeds 0-49 against the current suite ({R}/alternatives_r3.txt): alt1 NormalDist 50/50; alt2 Simpson 4000 panels "
        "50/50; alt3 DP over (position, maximum) 50/50; alt4 Box-Muller step-major 50/50; alt5 cumsum and index subsample 50/50; alt6 Pascal-row "
        "srw_terminal_count 50/50; alt7 step-major gauss draws (order free per project.html:226) 50/50. Reference 50/50 (run_graders)."),
    row("SC1-d-ag-mutants-plan", "2.6-mutation", "ledgers/SC1/mutants/m01-m10", "PASS",
        f"`tools/mutate_graders.py --unit SC1 --seeds 0-9` ({R}/mutate_graders_r3.txt): m01-m10 each KILLED; killed_by in the mutants array."),
    row("SC1-d-ag-mutants-own", "2.6-mutation", "ledgers/SC1/mutants/m11-m15, m18, m19, m21", "PASS",
        "m11-m15, m18, m19, m21 KILLED in the round-3 run (out/mutate_graders_r3.txt)."),
    row("SC1-d-ag-mutants-survivors", "2.6-mutation", "course/modules/SC/SC1/grader/test_project.py:418-423; ledgers/SC1/mutants/m16, m17", "PASS",
        "m16 and m17 KILLED (out/mutate_graders_r3.txt)."),
    row("SC1-d-ag-mutants-seed", "2.6-mutation", "ledgers/SC1/mutants/m20; course/modules/SC/SC1/grader/test_project.py:345-352", "PASS",
        "Round-2 FAIL resolved. m20 (seed ignored, Random(0) for every instance) is KILLED by test_draws_depend_on_the_instance_seed (seed 0, "
        "out/mutate_graders_r3.txt). The seed-plus-one variant is a separate row (SC1-d-ag-mutants-seed-offset)."),
    row("SC1-d-ag-mutants-r3", "2.6-mutation", "ledgers/SC1/mutants/m23-m26; ledgers/SC1/scripts/SC1-d-r3/make_mutants_r3.py", "PASS",
        "Four new student-error mutants, each reference.py with one edit: m23 odd-length shortcut (2**(n-1) for every level) KILLED by "
        "test_srw_counts_match_enumeration_for_n_up_to_12[1]; m24 standard error divided by N KILLED by test_standard_error_uses_divisor_n_minus_one; "
        "m25 sd = sqrt(H)/n KILLED by test_one_step_coarse_grid_tracks_the_terminal_law; m26 srw_max counts the endpoint at a twice KILLED by "
        "test_srw_counts_match_enumeration_for_n_up_to_12[1] (out/mutate_graders_r3.txt)."),
    row("SC1-d-ag-mutants-seed-offset", "2.6-mutation", "ledgers/SC1/mutants/m22_seed_offset_by_one.py; project.html:226; test_project.py:310-325, :345-352",
        "FAIL", "m22 seeds the draws with Random(seed + 1). project.html:226 states the draws use random.Random(instance[\"seed\"]), so the behaviour is specified. "
        f"The suite passes m22 for seeds 0-7 and 9 (out/m22_seed_suite_r3.txt). Its only failure, at seed 8, is test_one_step_estimate_matches_the_one_step_law_for_second_seed "
        "on the instance of seed 7927, where the mutant's sample has 0 hits (estimate 0.0, target 0.011093, band 0.002062; P(0 hits) = 0.0045 under the true law). "
        "That is a sampling fluke, not a seed check. The tool's KILLED status is spurious.",
        "Add a test that pins the seed and the gauss draws for one grid step, where draw order cannot matter: "
        "hits = sum(random.Random(INST['seed']).gauss(0.0, sqrt(H)) >= a over N draws); require discrete_max_exceedance(INST, 1)[0] == hits / N. "
        f"Candidate in {R.replace('out', 'candidate_seed_draw_test_r3.py')}: reference passes 50/50 seeds, m22 fails 10/10 "
        f"({R}/candidate_seed_draw_m22.txt). Note that alt4 (Box-Muller, not gauss) fails it; alt1, alt5 and alt7 pass."),
    row("SC1-d-ag-page-smoke", "2.5/2.6-gate", "course/modules/SC/SC1/project.html; tools/page_smoke.py", "PASS",
        f"`tools/page_smoke.py --unit SC1 --pages project.html` -> 'page_smoke SC1: PASS' ({R}/page_smoke_project.txt)."),
    row("SC1-d-ag-docstring", "2.9-docstring", "course/modules/SC/SC1/grader/test_project.py:9-15 vs tests :217-220, :309-315, :318-324, :328-335, :339-342, :385-388, :396-405",
        "PASS", "Round-2 FAIL resolved. The docstring now says several tests check one engine function against another and that one test calls "
        "discrete_max_exceedance twice on the same instance. That matches the code: :339-342 is the only same-instance repeat. The sentence at :13-14 "
        "that the band keeps 'a target near zero' from a false failure is false, and is recorded in SC1-d-ag-band-overconstraint."),
    row("SC1-d-rubric-observable", "2.6-rubric", "course/modules/SC/SC1/project.html:446-450", "PASS",
        "All 20 cells read. Descriptors are observable: numbered assumptions per result (C1), each step gives its reason or a named gap (C2), rounding and "
        "its statement (C3), named sampling and assumption boundary (C4), grid list and nested direction (C5)."),
    row("SC1-d-calib-A", "2.6-rubric calibration", "course/modules/SC/SC1/project.html:458-510 (exemplar A)", "PASS",
        "Scores from the rubric and the passage text: C1 1, C2 2, C3 2, C4 2, C5 1. Official 2,2,2,2,1: every criterion within one level. "
        "Caveat: the annotations were in the same read, so the calibration is not strictly blind."),
    row("SC1-d-calib-B", "2.6-rubric calibration", "course/modules/SC/SC1/project.html:512-593 (exemplar B)", "PASS",
        "Scores from the rubric and the passage text (annotations seen in the same read): C1 4, C2 3 (the A4(g) joint-measurability step that evaluates B~ at t-rho "
        "is unnamed, L05.html:61), C3 4, C4 3, C5 4. Official 4,4,4,3,4: within one level on every criterion."),
    row("SC1-d-exemplarA-claim", "2.9-prose/2.2-numbers", "course/modules/SC/SC1/project.html:499, 503-508", "PASS",
        "Annotation at :506: tail minus estimate 0.004361 at 256 steps and -0.001799 at 64 steps; the 256-step gap is larger in absolute value. Matches Lab 3 output (lab lines 415-417). Exemplar A is annotated as flawed, so its wording is not a finding."),
    row("SC1-d-exemplarB-proof", "2.4-mathematics", "course/modules/SC/SC1/project.html:577-584 (exemplar B appendix)", "PASS",
        "Re-derived P1: A = {tau<=t} = {M_t>=a} by continuity and the intermediate value theorem; P(tau=t) <= P(B_t=a) = 0; B~_r = B_{rho+r} - B_rho is a standard BM independent of F_rho (A3); on A, B_t - a = B~_{t-rho}; freezing (A4(b)) and symmetry give P(A, B_t<a) = P(A)/2; {B_t>=a} subset of A gives P(A) = 2 P(B_t>=a). P2: erfc substitution checked. P3: continuity of probability and erfc(0) = 1."),
    row("SC1-d-exemplarB-numbers", "2.2-numbers", "course/modules/SC/SC1/project.html:527 vs :150, :142", "PASS",
        "Round-2 FAIL resolved: :527 now says 'three significant digits', matching Lab 1 {:.2e}. Other exemplar numbers recomputed in ledgers/SC1/scripts/SC1-d-r3/recompute_r3.py ({R}/recompute_r3.txt)."),
    row("SC1-d-exemplarB-onestep-claim", "2.9-prose / 2.2-numbers", "course/modules/SC/SC1/project.html:552",
        "FAIL", "The Discretization passage says: 'The 1-step row targets half the tail, so its tail-minus-estimate figure is not a discretization bias.' "
        "Under the page's own definition at :229 (bias = continuous tail minus grid probability; estimate = tail minus grid estimate), the one-step bias is "
        "tail - tail/2 = 0.043248. The printed figure 0.026948 = tail - 0.059548 is that bias estimate, with sampling error -0.016300 (1.52 se). "
        f"Lab 3 prints it at lab line 99 ({R}/recompute_r3.txt: 'tail-p = 0.026948').",
        "Replace the sentence with: 'The one-step bias is tail/2 = 0.043248, so the printed figure 0.026948 estimates it with sampling error -0.016300, "
        "which is 1.5 standard errors.' Keep the sentence about the separate paths."),
    row("SC1-d-lab1-run", "2.5-labs", "course/modules/SC/SC1/project.html:55-156; tests/labs/SC1/lab-SC1-project-1.py", "PASS",
        f"run_labs SC1 11/11 PASS ({R}/run_labs.txt). check_labs_r3.py: page code equals the twin, twin runs under python -I -W error (exit 0), "
        f"expected block equals stdout ({R}/check_labs_r3.txt)."),
    row("SC1-d-lab1-docstring", "2.9-prose", "project.html:58-68; tests/labs/SC1/lab-SC1-project-1.py:3-8", "PASS",
        "Round-2 FAIL resolved. The docstring says H and a are printed as generated (three decimals), N is an integer, and the Simpson difference is in "
        "exponent form to three significant digits. Printed output (:149-154) and format (:141-142) agree."),
    row("SC1-d-lab2-run", "2.5-labs", "course/modules/SC/SC1/project.html:158-204; tests/labs/SC1/lab-SC1-project-2.py", "PASS",
        "check_labs_r3.py: the page code differs from the twin only in the two blanks (identity = ___ and max_hits == ___; diff shown in round-3 check). "
        "The completed twin's stdout equals the expected block (29 / 22 / 7 / True)."),
    row("SC1-d-lab2-attribution", "2.1-attribution", "course/modules/SC/SC1/project.html:203 vs course/modules/SC/SC1/L06.html:75, 87, 376", "PASS",
        "Corollary 1.4 (discrete tail identity) and Proposition 1.3 (discrete reflection identity) exist in L06 with those numbers, and Corollary 1.4 is proved from Proposition 1.3 (L06:376)."),
    row("SC1-d-lab3-run", "2.5-labs", "course/modules/SC/SC1/project.html:297-423; tests/labs/SC1/lab-SC1-project-3.py", "PASS",
        "run_labs SC1 PASS; check_labs_r3.py PASS for lab 3. Printed values equal the reference engine (all grid rows, nested counts 35/29/27/22, walk 1588/794) "
        "and my independent recompute (recompute_r3.py). The hypothesis's 'within five standard errors' claim for 4, 16, 64, 256 steps holds on these numbers. "
        "The interpretation sentence is a separate FAIL row."),
    row("SC1-d-lab3-onestep-interp", "2.5-labs / 2.9-prose", "course/modules/SC/SC1/project.html:423 vs tests/labs/SC1/lab-SC1-project-3.py:99 and output line 'grid n = 1'",
        "FAIL", "The interpretation says: 'The one-step row targets half the tail, 0.043248, so its estimate is compared with that value and not with the tail.' "
        "The lab code (twin line 99, page line 398) computes tail - p for every grid, including n = 1, and the printed line is "
        "'grid n = 1: ... tail minus estimate 0.026948', i.e. against the full tail 0.086497. The sentence contradicts the lab's own output.",
        "Either change the lab so the n = 1 row prints tail/2 - p (and the printed line and expected block change with it), or rewrite :423 to say the "
        "one-step row prints tail minus estimate, which estimates the one-step bias tail/2 = 0.043248 with sampling error -0.016300."),
    row("SC1-d-lab3-docstring", "2.9-prose", "tests/labs/SC1/lab-SC1-project-3.py:3-11 (page :300-310)", "PASS",
        "Round-2 FAIL resolved: H and a printed as generated (three decimals), N and hit counts integers, computed values rounded to six decimals. Matches printed output."),
    row("SC1-d-labs-pytest", "2.5-labs", "tests/test_labs.py -k SC1; tests/test_run_labs.py; tests/test_page_checks.py; tests/test_memo_exemplars.py", "PASS",
        f"`.venv/bin/pytest -q -p no:cacheprovider tests/test_labs.py -k SC1 tests/test_run_labs.py tests/test_page_checks.py tests/test_memo_exemplars.py` -> exit 0 ({R}/pytest_relevant.txt)."),
    row("SC1-d-statements", "2.4-mathematics", "course/modules/SC/SC1/project.html:235-256", "PASS",
        "P1, P2, P3 each list numbered assumptions before the statement. A0 is standard Brownian motion (L01 Definition 1.1 includes the normal increments), so P(B_t = a) = 0 is covered for the '2 P(B_t > a) = 2 P(B_t >= a)' step. P3's first part uses only continuity."),
    row("SC1-d-A1-label", "2.4-mathematics", "course/modules/SC/SC1/project.html:236-242, 577-580", "PASS",
        "Assumptions are labelled A0, A3, A4 only; each names its source (L01 Definition 1.1; L05 A3 and A4 at L05.html:59-67 and :269-277). No unnamed assumption label."),
    row("SC1-d-A3-A4-usage", "2.4-mathematics", "course/modules/SC/SC1/project.html:236-242; course/modules/SC/SC1/L05.html:59-67, 269-277", "PASS",
        "A4(c) (first hitting time of a closed set is a stopping time) is the fact the page cites for tau_a; A3 is stated for bounded stopping times (L05.html:277), applied to rho = tau_a ^ t <= t as the page says."),
    row("SC1-d-notation", "2.4-notation", "course/modules/SC/SC1/project.html passim; notation/notation.json", "PASS",
        "Macros used: \\Prob, \\Normal (registered), \\Phi (standard normal CDF, program-wide), \\tau, \\rho, \\tilde, \\operatorname{erfc}; no unregistered macro. "
        "T appears only as 'not T' (:529). N is local and defined at :57 as the path count. No symbol changes its meaning."),
    row("SC1-d-define-before-use", "2.9-prose", "course/modules/SC/SC1/project.html:37, 45, 53, 57", "PASS",
        "Round-2 FAIL resolved. :37 defines 'running maximum' and 'grid maximum' in place. :45 glosses 'simple random walk' in place. :57 defines N as the path count at its first use."),
    row("SC1-d-discretization-bias", "2.4-definitions", "course/modules/SC/SC1/project.html:225, 229", "PASS",
        "The <dfn> at :229 is defined once. 'Never negative' holds pathwise (grid maximum <= M_H on the same path, :225). 'Can be negative through sampling noise, as Lab 3 shows at 64 steps' matches lab output tail - estimate = -0.001799."),
    row("SC1-d-monte-carlo-term", "2.9-prose", "course/modules/SC/SC1/project.html", "PASS",
        "'Monte Carlo' does not appear on the page (grep). The page uses 'seeded simulation'."),
    row("SC1-d-dag", "2.9-DAG", "course/modules/SC/SC1/project.html; tools/check_dag.py --unit SC1", "PASS",
        f"check_dag SC1 PASS ({R}/check_dag.txt). Concept links at :236 (stopping-time) and :247 (normal-distribution) resolve (check_pages PASS)."),
    row("SC1-d-scope-words", "2.9-prose", "course/modules/SC/SC1/project.html:225, 227, 229, 231, 232, 449, 564", "PASS",
        "'every' and 'never' are each proved or computed: :225 pathwise (grid in [0,H]); :227 coarse subset; :231 the listed ValueError conditions; 'almost surely' at :449 and :564 is used as an exclusion, not a claim."),
    row("SC1-d-process-words", "2.9-prose", "project.html; grader/*.py; tests/labs/SC1/lab-SC1-project-*.py", "PASS",
        "grep for builder, verifier, ledger, agent, round, fragment, AI, LLM, claude, TODO, TBD and placeholder: no hits in learner text."),
    row("SC1-d-banned-structure", "2.9-structure", "course/modules/SC/SC1/project.html; tools/check_pages.py --unit SC1", "PASS",
        f"check_pages SC1 PASS ({R}/check_pages.txt). Banned phrases (BUILDER_RULES 1.3-1.4) absent in learner text; the only 'about 0.0865' (:464, :469) is inside exemplar A, annotated as the flawed passage."),
    row("SC1-d-registry", "2.1-citations", "course/modules/SC/SC1/project.html:613-615; references/references.json:20732", "PASS",
        "shreve2004stochastic: book, title 'Stochastic Calculus for Finance II', year 2004, Open Library URL, verified_by openlibrary. The page cites it at book level with no locator. Karatzas & Shreve (curriculum sources) has no registry record (grep: 0 hits) and is not cited. verify_refs --offline: 560 entries, 0 problems (" + R + "/verify_refs_offline.txt)."),
    row("SC1-d-privacy-claim", "2.9-prose", "project.html:281, 596, 628",
        "PASS", "Carried from round 2 (project.html:281, 596, 628 byte-identical since the previous pin: none of these lines is in the 1c1645f3-to-67a2d13e or 67c47689-to-67a2d13e hunks). Claim is about browser storage; text re-read this round, panel code not re-read."),
    row("SC1-d-tools-gates", "2.9-gates", "ruff, mypy, pytest, verify_refs", "PASS",
        f"ruff check . exit 0 ({R}/ruff_all.txt); ruff format --check course/modules/SC/SC1/grader tests/labs/SC1: 15 files already formatted; "
        f"mypy --no-incremental: 'Success: no issues found in 385 source files' ({R}/mypy.txt); relevant pytest exit 0; verify_refs --offline: 0 problems."),
    row("SC1-d-numbers-prose", "2.2-numbers", "project.html:57, 154, 202, 258, 299, 423, 476, 518, 540, 552-553 (student prose, exemplars, Lab 3 figures)",
        "PASS", "Independent recompute (ledgers/SC1/scripts/SC1-d-r3/recompute_r3.py): H = 2.083, a = 2.474, N = 487, tail 0.086497, tail/2 0.043248, one-step p 0.059548, se 0.010735, band 0.055726, |p - tail/2| = 0.016300 = 1.518 se, grid rows, nested 40 vs 35/29/27/22, walk 1588/794 of 4096, Lab 2 29/22/7 all match to the displayed digit. Prose about the one-step row is a separate FAIL. My Simpson difference is 8.73e-15 against the printed 9.13e-15: both are float rounding residuals of the same order, and the page quotes the lab's printed value."),
    row("SC1-d-ag-band-overconstraint", "2.6-autograder", "course/modules/SC/SC1/grader/test_project.py:76-78, 310-325, 407-416 and docstring :13-14",
        "FAIL", "The reference fails the suite for seeds it was not run on. Tests: test_one_step_estimate_matches_the_one_step_gaussian_law (seeds 252, 686, 1012), "
        "test_one_step_estimate_matches_the_one_step_law_for_second_seed (seed 54, instance 7973), test_one_step_coarse_grid_tracks_the_terminal_law (seeds 156, 633, 2569). "
        f"Evidence: {R}/reference_failing_seeds_r3.txt. Cause: the band uses the sample SE, which is 0 when no path hits, so the band is 1/N; "
        "for targets with N*p around 2 to 5 a zero-hit sample is likely (P = (1-p)^N). scan_bands_r3.py: the reference fails 25 of 6000 one-step instances "
        f"and 13 of 3000 coarse-1 seeds with the sample SE; with the target's SE, 0 and 0 ({R}/scan_bands_r3.txt). The reference passes seeds 0-49 only, "
        "so run_graders does not show it. The docstring claim at :13-14 is therefore false for these tests.",
        "In the two tests, use the target's standard error: simulation_band(math.sqrt(t * (1 - t) / n_paths), n_paths) with t the target (tail/2). "
        "Then re-run the 6000-instance and 3000-seed scans (scan_bands_r3.py), the suite on seeds 252, 54, 686, 1012, 156, 633, 2569, and the grader's "
        "mutation test."),
    row("SC1-d-spec-n41-method", "2.6-spec", "course/modules/SC/SC1/project.html:217; grader/reference.py:79-85; ledgers/SC1/scripts/SC1-d-r3/alternatives/alt7_gauss_step_major.py",
        "FAIL", "project.html:217 says 'for n = 41 the counts must come from the reflection identity or from a recurrence over the walk's position and running maximum'. "
        "The reference's srw_terminal_count (reference.py:85) is sum(math.comb(n, j) ...), a binomial count that is neither named method; the reflection identity "
        "(reference.py:91) covers only the maximum count. alt7 uses the same binomial count and passes the suite 50/50, so the sentence excludes a method the "
        "reference uses.",
        "Reword :217 to: 'for n = 41 the counts must not list the 2**n walks; a count by binomial coefficients, the reflection identity or a recurrence is allowed.' "
        "The test at test_project.py:245-246 is method-agnostic and needs no change."),
]

MUTANTS = [
    ("m01_reflection_factor_dropped", "Reflection factor dropped: reflection_tail returns P(B_t >= a) with no factor 2.", "test_reflection_tail_is_the_erfc_closed_form (seed 0)"),
    ("m02_scale_sqrt_2t_became_sqrt_t", "Scale confusion: reflection_tail uses sqrt(t) in the erfc argument.", "test_reflection_tail_is_the_erfc_closed_form (seed 0)"),
    ("m03_horizon_off_by_one", "Horizon off by one: the grid maximum drops the final grid point.", "test_one_step_estimate_matches_the_one_step_gaussian_law (seed 0)"),
    ("m04_lookahead_extra_point", "Lookahead: the grid maximum includes one extra grid point beyond the horizon.", "test_fine_count_is_the_discrete_estimate_times_n (seed 0)"),
    ("m05_standard_error_ignored", "Standard error ignored: discrete_max_exceedance returns a standard error of 0.0.", "test_standard_error_uses_divisor_n_minus_one (seed 0)"),
    ("m06_divisor_n_not_n_minus_one", "Divisor error: the sample variance of the indicators uses divisor N.", "test_standard_error_uses_divisor_n_minus_one (seed 0)"),
    ("m07_nested_counts_swapped", "Nested grids reversed: nested_grid_counts returns the counts in swapped order.", "test_coarse_count_never_exceeds_the_fine_count (seed 0)"),
    ("m08_level_doubled_in_tail", "Level doubled: reflection_tail(a, t) is computed as reflection_tail(2a, t).", "test_reflection_tail_is_the_erfc_closed_form (seed 0)"),
    ("m09_seed_zero_hard_coded", "Hard-coded answer: discrete_max_exceedance returns the Lab 3 numbers when the seed is 0.", "test_estimate_is_a_fraction_of_the_paths (seed 0)"),
    ("m10_nonpositive_time_accepted", "Invalid input accepted: reflection_tail returns 0.0 for t <= 0.", "test_reflection_tail_rejects_zero_time (seed 0)"),
    ("m11_coarse_grid_shifted_by_one", "Coarse grid off by one: samples steps 1, 1+s, ... instead of s, 2s, ...", "test_one_step_coarse_grid_tracks_the_terminal_law (seed 0)"),
    ("m12_srw_strict_inequality", "Strict inequality: srw_terminal_count counts S_n > a.", "test_srw_counts_match_enumeration_for_n_up_to_12[1] (seed 0)"),
    ("m13_divisibility_check_omitted", "Divisibility check omitted: a coarse grid that does not divide the fine grid is accepted.", "test_coarse_grid_that_does_not_divide_fine_raises_value_error[4-3] (seed 0)"),
    ("m14_srw_max_forgets_reflection_term", "Reflection term forgotten: srw_max_count returns the endpoint count at a alone.", "test_srw_counts_match_enumeration_for_n_up_to_12[2] (seed 0)"),
    ("m15_increment_scale_missing_square_root", "Increment scale: the Gaussian standard deviation is H / n (square root missing).", "test_one_step_estimate_matches_the_one_step_gaussian_law (seed 0)"),
    ("m16_nested_fine_zero_not_rejected", "Named condition skipped: nested_grid_counts does not reject n_fine < 1.", "test_fine_grid_of_zero_steps_raises_value_error (seed 0)"),
    ("m17_nested_coarse_zero_not_rejected", "Named condition skipped: nested_grid_counts does not reject n_coarse < 1.", "test_coarse_grid_of_zero_steps_raises_value_error (seed 0)"),
    ("m18_nested_coarse_count_copies_fine", "Nested coarse count copied from the fine count.", "test_one_step_coarse_grid_tracks_the_terminal_law (seed 1)"),
    ("m19_grid_estimate_uses_endpoint_only", "Running maximum forgotten: discrete_max_exceedance tests only the last grid value.", "test_fine_count_is_the_discrete_estimate_times_n (seed 0)"),
    ("m20_draws_seeded_with_zero_for_every_instance", "Seed ignored: _grid_paths seeds the Gaussian draws with 0 for every instance.", "test_draws_depend_on_the_instance_seed (seed 0)"),
    ("m21_coarse_stride_uses_n_coarse", "Wrong subgrid: nested_grid_counts takes every n_coarse-th fine point.", "test_equal_grids_give_equal_counts (seed 0)"),
    ("m22_seed_offset_by_one", "Seed offset: _grid_paths draws from random.Random(seed + 1).",
     "test_one_step_estimate_matches_the_one_step_law_for_second_seed (seed 8; zero-hit sample fluke, not a seed check; see SC1-d-ag-mutants-seed-offset)"),
    ("m23_srw_terminal_odd_shortcut", "Odd-length shortcut: srw_terminal_count returns 2**(n-1) for every level when n is odd.", "test_srw_counts_match_enumeration_for_n_up_to_12[1] (seed 0)"),
    ("m24_standard_error_divided_by_n", "Standard error divided by N instead of sqrt(N).", "test_standard_error_uses_divisor_n_minus_one (seed 0)"),
    ("m25_increment_scale_sqrt_h_over_n_misplaced", "Increment scale: sd = sqrt(H) / n_steps instead of sqrt(H / n_steps).", "test_one_step_coarse_grid_tracks_the_terminal_law (seed 0)"),
    ("m26_srw_max_reflection_uses_endpoint_at_a", "Reflection term misplaced: srw_max_count adds the endpoint count at a twice.", "test_srw_counts_match_enumeration_for_n_up_to_12[1] (seed 0)"),
]

fragment = {
    "unit": "SC1",
    "slice": "d",
    "round": 3,
    "verifier": "Claude Haiku 5.5, independent verifier (slice d, round 3)",
    "pin": "67a2d13e",
    "base": "1c1645f3",
    "checkout": str(ROOT),
    "scratch": "/tmp/sc1d_r3_* (removed or left as mktemp dirs)",
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "verdict": "FAIL",
    "rows": ROWS,
    "mutants": [
        {"id": name, "name": name, "description": desc, "killed_by": killed, "file": f"ledgers/SC1/mutants/{name}.py"}
        for name, desc, killed in MUTANTS
    ],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Delta 67c47689 -> 67a2d13e read in full for project.html, grader/test_project.py, tests/labs/SC1/lab-SC1-project-1.py and -3.py, and ledgers/SC1/mutants/m18-m21. grader/reference.py, instance.py, starter.py and lab-SC1-project-2.py are byte-identical to the previous pin and were re-run.",
        "Round-2 FAILs resolved: spec-rounding-statement, ag-overconstraint (enumeration), ag-mutants-seed (m20), ag-docstring, exemplarB-numbers, lab1-docstring, lab3-docstring, define-before-use.",
        "Not counted as findings: the 'about 0.0865' in deliberately flawed exemplar A; the 240 s enumeration timeout of alt2b, which project.html:217 now excludes; alt4 (Box-Muller) passing the suite although project.html:226 names gauss, because the suite cannot tell the generator apart (see SC1-d-ag-mutants-seed-offset for the fix).",
        "Could not check: in-browser UI behaviour of the grader panel and the self-assessment form (only page_smoke's Pyodide run and the code); exemplar scoring is not strictly blind because the annotations were read in the same pass; the other slices (lessons, cards, hub); the Pyodide timing of the 128 tests beyond page_smoke's limit; whether the suite's behaviour matches for seeds above 2999 beyond the scans.",
    ],
    "summary": "SC1 slice d round 3 (project.html, grader, project labs, mutants, alternatives): FAIL. Rows: 54 (49 PASS, 5 FAIL, 0 UNVERIFIABLE). Mutants: 26 in ledgers/SC1/mutants; tools report 26/26 killed, but m22 is killed only by a zero-hit sampling fluke, so 25 of 26 are killed by a deterministic property. Alternatives: 7 pass 50/50 seeds; the enumeration probe (alt2b) times out and is excluded by the current spec.",
}

path = ROOT / "ledgers/SC1/SC1-d.json"
path.write_text(json.dumps(fragment, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
problems = ledger.validate(json.loads(path.read_text(encoding="utf-8")), "SC1-d")
print("rows:", len(ROWS), "statuses:", {s: sum(1 for r in ROWS if r["status"] == s) for s in ("PASS", "FAIL", "UNVERIFIABLE")})
print("validate:", problems if problems else "[] (valid)")
