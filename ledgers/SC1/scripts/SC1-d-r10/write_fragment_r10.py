"""Write the round-10 SC1 slice d verifier fragment (ledgers/SC1/SC1-d.json). Evidence cites the out/ files of this round."""
import json
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyE10-SC1-d")
O = "ledgers/SC1/scripts/SC1-d-r10/out/"
rows = []


def P(rid, check, location, evidence, status="PASS", fix=""):
    row = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        row["fix"] = fix
    rows.append(row)


# ---- round-9 row ids (all 94 kept). Every subject re-checked this round, see evidence.
P("SC1-d-ladder", "2.6-ladder", "course/modules/SC/SC1/project.html:40-49",
  "Re-read this round: rung 1 is Lab 1 (SIMULATED, one instance), rung 2 is Lab 2 (two ___ blanks, graded instantly), rung 3 is the specification, rung 4 is stretch. check_projects --unit SC1 PASS (" + O + "check_projects_SC1.txt).")
P("SC1-d-grading-mode", "2.6-grading", "course/modules/SC/SC1/project.html (Grading mode dd)",
  "Grading mode names both the autograder and the rubric; check_projects GRADING_WORDS check PASS (" + O + "check_projects_SC1.txt).")
P("SC1-d-spec-signatures", "2.6-spec", "course/modules/SC/SC1/project.html (Required outputs dd) vs course/modules/SC/SC1/grader/starter.py:16-33",
  "The five signatures in the page equal starter.py: reflection_tail(a, t), discrete_max_exceedance(instance, n_steps), nested_grid_counts(instance, n_fine, n_coarse), srw_max_count(n, a), srw_terminal_count(n, a). Starter fails the suite 3 of 3 seeds (" + O + "starter_fails_0_2.txt).")
P("SC1-d-spec-rounding-statement", "2.2-numbers / 2.9-prose", "course/modules/SC/SC1/project.html (Constraints dd, Conventions); Lab 1 and Lab 3 expected blocks",
  "Constraints rule (six decimals, exponent form to three significant digits for a difference, H and a to three decimals) matches every printed line: Lab 1 prints 9.13e-15 and six-decimal values; Lab 3 six-decimal values; " + O + "page_vs_twin_r10.txt shows each expected block equals the twin's output.")
P("SC1-d-hours", "2.6-hours", "course/modules/SC/SC1/project.html (table#hours, main data-hours-project=28)",
  "Rows 2+3+10+8+3+2 = 28 equals data-hours-project 28. Verifier estimate: rung 1 1-2 h, rung 2 1-3 h, proofs P1-P3 8-12 h (P1 needs A3, A4(b), A4(c), A4(g), A4(h) and the measurability step), engine 6-10 h, report 2-4 h, self-assessment 1-2 h; total within 30% of 28 h.")
P("SC1-d-spec-grid-table", "2.6-spec", "course/modules/SC/SC1/project.html Conventions bullets 'The grid for n steps', 'discrete_max_exceedance', 'nested_grid_counts'; grader/reference.py:27-76",
  "Grid t_k = kH/n, draw order random.Random(seed).gauss(0, sqrt(H/n)) path by path, and nested coarse points every n_fine/n_coarse steps match reference.py. Grid rows in Lab 3 recomputed independently (" + O + "recompute_r10.txt: estimates and SEs for n = 1, 4, 16, 64, 256 equal the printed values).")
P("SC1-d-spec-tolerance-statement", "2.6-spec", "course/modules/SC/SC1/project.html Conventions 'reflection_tail' bullet (10^-10) and 'simulated probability' bullet; grader/test_project.py:120-123, :186",
  "Page and test both use 1e-10 for the erfc agreement and 5 SE + 1/N for simulation bands; the simulation band matches the page formula. Deviation from plan section 5.5 (1e-12) recorded in notes (non-blocking).")
P("SC1-d-ag-reference", "2.6-autograder", "course/modules/SC/SC1/grader/reference.py; tools/run_graders.py",
  "run_graders --unit SC1 --seeds 0-49: reference 50/50 seeds (" + O + "run_graders_SC1_0-49.txt). Scratch pytest of reference: 132 passed on seeds 0, 1, 7, 49, and 0-3 under the proposed suite.")
P("SC1-d-ag-starter", "2.6-autograder", "course/modules/SC/SC1/grader/starter.py",
  "Every function raises NotImplementedError; run_candidates on starter.py: suite fails 3 of 3 seeds (" + O + "starter_fails_0_2.txt).")
P("SC1-d-ag-instances", "2.6-autograder", "course/modules/SC/SC1/grader/instance.py",
  "All 50 seeds recomputed independently (" + O + "recompute_r10.txt): steps in 4..256, paths in 400..800, max steps x paths 179172 <= 200000, 49 distinct levels (>= 45 required), 50 distinct horizons, label SIMULATED.")
P("SC1-d-ag-count", "2.6-autograder", "course/modules/SC/SC1/grader/test_project.py; course/modules/SC/SC1/project.html meta description, Grading mode dd, Running the suite locally",
  "pytest --collect-only: 132 tests collected. The page states 132 in three places (meta description, Grading mode, Running the suite locally).")
P("SC1-d-ag-messages", "2.6-autograder", "course/modules/SC/SC1/grader/test_project.py:58-117 (expect, must_raise, must_accept, within, within_budget)",
  "Helper messages are static or name the inputs (n = 0, n_coarse = 3 ...); none prints an expected value; grep finds 0 bare assert statements, so --assert=plain loses no comparison detail.")
P("SC1-d-ag-overconstraint", "2.6-autograder", "course/modules/SC/SC1/grader/test_project.py; ledgers/SC1/scripts/SC1-d-r10/alternatives/",
  "Five verifier alternatives pass seeds 0-49 (" + O + "alternatives_seeds_0_49.txt): alt_r10_a (NormalDist tail), alt_r10_b (Simpson-only tail), alt_r10_c (DP walk counts), alt_r10_d (step-major draw order), alt_r10_e (index subsampling). Over-constraint found in the plan's own alternative 4 (Box-Muller): see notes.")
P("SC1-d-ag-alternatives-ok", "2.6-autograder", "ledgers/SC1/scripts/SC1-d-r7/alternatives, SC1-d-r8/alternatives (repathed), SC1-d-r9/alternatives, SC1-d-r10/alternatives",
  "Re-run this round on seeds 0-49 against the current suite (" + O + "prior_alternatives_current_suite_0_49.txt; " + O + "alt_r8_bc_repathed_0_49.txt): all valid alternatives pass. Two are killed by design: alt2b (lists 2^41 walks, forbidden by the page's n = 41 rule) and alt4 (Box-Muller, violates the page's stated gauss draw order).")
P("SC1-d-ag-mutants-plan", "2.6-mutation", "ledgers/SC1/mutants/m01-m10",
  "mutate_graders --unit SC1 --seeds 0-9 (" + O + "mutate_graders_SC1_0-9_final.txt): 64/64 killed, m01-m10 each killed on seed 0 or 1; learner-seed coverage of each is 50/50 in " + O + "kill_rate_v3/.")
P("SC1-d-ag-mutants-own", "2.6-mutation", "ledgers/SC1/mutants/m11-m15, m18, m19, m21",
  "All killed on the seeds 0-9 gate. Learner-seed coverage below 50/50 for m11 (44), m18 (26), m19 (48), m21 (49): see SC1-d-r10-mutant-seed-coverage.")
P("SC1-d-ag-mutants-survivors", "2.6-mutation", "ledgers/SC1/mutants/m16, m17",
  "Killed 50/50 seeds (" + O + "kill_rate_v3/m16*, m17*).")
P("SC1-d-ag-mutants-seed", "2.6-mutation", "ledgers/SC1/mutants/m20",
  "Killed 50/50 seeds (" + O + "kill_rate_v3/m20*).")
P("SC1-d-ag-mutants-seed-offset", "2.6-mutation", "ledgers/SC1/mutants/m22_seed_offset_by_one.py",
  "Killed 50/50 seeds (" + O + "kill_rate_v3/m22*).")
P("SC1-d-ag-mutants-r3", "2.6-mutation", "ledgers/SC1/mutants/m23-m26",
  "Killed on the 0-9 gate; 50/50 seeds for m23, m24, m26; m25 killed on 44/50 seeds (see SC1-d-r10-mutant-seed-coverage).")
P("SC1-d-ag-mutants-r4-new", "2.6-mutation", "ledgers/SC1/mutants/m27-m31",
  "Killed on the 0-9 gate. m28, m29, m30 50/50 seeds; m27 44/50 and m31 15/50 (see SC1-d-r10-mutant-seed-coverage).")
P("SC1-d-ag-mutants-r5-new", "2.6-mutation", "ledgers/SC1/mutants/m32, m33, m34",
  "Killed on the 0-9 gate. m33 50/50; m32 49/50 and m34 44/50 (see SC1-d-r10-mutant-seed-coverage).")
P("SC1-d-ag-page-smoke", "2.6-autograder", "course/modules/SC/SC1/project.html; tools/page_smoke.py --unit SC1 --pages project",
  "PASS (" + O + "page_smoke_SC1_project.txt): in-browser grader 132 tests pass on seed 60449209 in 1.2 s; labs run; no console errors reported.")
P("SC1-d-ag-docstring", "2.6-autograder", "course/modules/SC/SC1/grader/test_project.py:1-20",
  "Docstring claims checked against the file: one test calls discrete_max_exceedance twice (test_estimate_is_reproducible_for_the_same_instance); one test pins the draws to random.Random(seed).gauss (test_one_step_draws_are_the_seeded_gaussians); two tests put the level on a path maximum (test_path_whose_maximum..., test_path_just_below...); the nested counts are compared with discrete_max_exceedance (test_fine_count_is_the_discrete_estimate_times_n).")
P("SC1-d-rubric-observable", "2.9-prose", "course/modules/SC/SC1/project.html rubric table#rubric (C1-C5, four levels)",
  "Each descriptor read and judged observable from the report: the numbered assumptions, the step reasons, the printed-value rule, the sample-versus-proof statement, the grid estimates with SE and nested inequality. C5 level 2 ('where single-seed noise can reverse it') is observable as a statement of one-seed direction plus a noise caveat.")
P("SC1-d-calib-A", "2.9-prose / rubric calibration", "course/modules/SC/SC1/project.html exemplar-a data-scores=1,2,2,2,1",
  "Scored from the rubric text: C1 1 (no numbered assumption for any result), C2 2 (P1 complete with symmetry only asserted; P2, P3 unproved), C3 2 (decimals with no rounding statement; 1.52 not printed), C4 2 (grid result presented as holding for every grid), C5 1 (discussion, no numbers). Equals the official 1,2,2,2,1, within one level. CAVEAT: calibration is not strictly blind: the whole page, including the official verdict lines, was read before scoring.")
P("SC1-d-exemplarA-claim", "2.2-numbers / 2.9-prose", "course/modules/SC/SC1/project.html exemplar A passages (summary, checks, discretization)",
  "Every exemplar-A number recomputed (" + O + "recompute_r10.txt): tail 0.0865 (0.086497), estimate 0.0595, half-tail 0.0432, difference 0.0163 = 1.52 SE (0.016300/0.010735 = 1.518), 1588 walks, 256-step gap 0.004361 vs 64-step -0.001799.")
P("SC1-d-exemplarB-onestep-claim", "2.2-numbers", "course/modules/SC/SC1/project.html exemplar B checks passage",
  "0.059548, SE 0.010735, 0.016300 above target 0.043248, 1.52 SE, band 0.048142: all equal the Lab 1 output (" + O + "twin_lab-SC1-project-1.txt) or the recomputation.")
P("SC1-d-exemplarB-numbers", "2.2-numbers", "course/modules/SC/SC1/project.html exemplar B summary, discretization, limitations",
  "Tail 0.086497; Simpson difference 9.13e-15 (within 1e-14); SEs 0.010735, 0.009819, 0.011239, 0.012870, 0.012455; tail-minus-estimate 0.026948, 0.037215, 0.020788, -0.001799, 0.004361; nested 35, 29, 27, 22 vs fine 40; all equal Lab 3 output (" + O + "twin_lab-SC1-project-3.txt).")
P("SC1-d-exemplarB-proof", "2.4-proof / 2.9-prose", "course/modules/SC/SC1/project.html exemplar B appendix (P1, P2, P3)",
  "P1 re-derived step by step: event A = {tau <= t} = {M_t >= a} by continuity and IVT; Prob(tau = t) = 0 since tau = t forces B_t = a; B~ independent of F_rho by A3; measurability by A4(h) and A4(g); freezing via A4(b) with f-bar(z) = 1/2 1{z2=1}1{z1>0}; P(A, B_t<a) = P(A)/2; P(A) = P(B_t>=a) + P(A)/2 gives P(M_t>=a) = 2P(B_t>=a). P2 erfc substitution w = z/sqrt2 checked. P3 limit erfc(0)=1 checked. No gap found.")
P("SC1-d-exemplarB-p1-assumptions", "2.9-prose / 2.4-proof", "course/modules/SC/SC1/project.html statements (P1 assumptions) and exemplar B appendix vs course/modules/SC/SC1/L05.html:59-70 (A4 items) and :265-279 (A3)",
  "A3 is for bounded stopping times (L05.html:271-279); A4(b) freezing (L05:61-63), A4(c) hitting times (L05:63), A4(g) joint measurability (L05:67), A4(h) measurability at a stopping time (L05:68) match the uses in the page.")
P("SC1-d-lab1-run", "2.5-labs", "course/modules/SC/SC1/project.html Lab 1; tests/labs/SC1/lab-SC1-project-1.py",
  "run_labs --unit SC1 --page project: PASS 3/3 (" + O + "run_labs_SC1_project.txt). Twin under python -I -W error exits 0 (" + O + "twin_lab-SC1-project-1.txt). Page code equals twin (" + O + "page_vs_twin_r10.txt; only the final newline differs).")
P("SC1-d-lab1-docstring", "2.5-labs / 2.9-prose", "tests/labs/SC1/lab-SC1-project-1.py:1-14 vs page Lab 1 hypothesis",
  "Docstring: six-decimal rounding, Simpson difference in exponent form to three significant digits, N draws, H and a to three decimals; the printed output has exactly these forms.")
P("SC1-d-lab2-run", "2.5-labs", "course/modules/SC/SC1/project.html Lab 2; tests/labs/SC1/lab-SC1-project-2.py",
  "Twin output 29 / 22 / 7 / True equals the page's expected block; page code differs from the twin only in the two ___ lines (identity = ___ and max_hits == ___), as the lab requires (" + O + "page_vs_twin_r10.txt).")
P("SC1-d-lab2-attribution", "2.9-prose / attribution", "course/modules/SC/SC1/project.html:209 vs course/modules/SC/SC1/L06.html (Corollary 1.4, Proposition 1.3)",
  "L06 defines Proposition 1.3 (discrete reflection identity) and Corollary 1.4 (discrete tail identity, 'proved from Proposition 1.3'); the page's citation is accurate.")
P("SC1-d-lab3-run", "2.5-labs", "course/modules/SC/SC1/project.html Lab 3; tests/labs/SC1/lab-SC1-project-3.py",
  "Twin output equals the page's expected block line for line (" + O + "twin_lab-SC1-project-3.txt); run_labs PASS; page code equals twin.")
P("SC1-d-lab3-onestep-interp", "2.5-labs / 2.9-prose", "course/modules/SC/SC1/project.html:429",
  "0.016300/0.010735 = 1.518 (1.52); 0.016300/0.009218 = 1.768 (1.77); 0.001799/0.012870 = 0.140 (0.14); numbers and attributions correct.")
P("SC1-d-lab3-docstring", "2.5-labs / 2.9-prose", "tests/labs/SC1/lab-SC1-project-3.py:3-11 (page Lab 3 hypothesis)",
  "Docstring: independent Gaussian increments drawn path by path, coarse grids are every 256/n-th point of the same paths, nested inequality, six-decimal rounding; all match the code and the output.")
P("SC1-d-labs-pytest", "2.5-labs / tooling", "tests/test_labs.py, tests/test_run_labs.py, tests/test_page_checks.py, tests/test_memo_exemplars.py",
  "pytest -k 'SC1 or sc1 or project or grader or labs' on the three lab/page modules: exit 0; tests/test_memo_exemplars.py: exit 0 (" + O + "pytest_sc1_related.txt).")
P("SC1-d-calib-B", "2.9-prose / rubric calibration", "course/modules/SC/SC1/project.html exemplar-b data-scores=4,4,4,3,4",
  "Scored from the rubric text: C1 4 (every assumption listed and tied to its step, A3 applied to rho <= t), C2 4 (every P1 step names its tool; P2, P3 complete), C3 4 (rounding stated, exact versus float labelled), C4 3 (no statement of what the nested comparison leaves open about the continuum), C5 4 (every grid, SE, direction from nested counts). Equals official 4,4,4,3,4. CAVEAT as calib-A: not strictly blind.")
P("SC1-d-statements", "2.6-spec / 2.4-proof", "course/modules/SC/SC1/project.html statements P1-P3 (lines ~241-262)",
  "P1 assumptions and statement match the proof in exemplar B; P2 and P3 statements re-derived (erfc form, 2(1 - Phi(a/sqrt t)), P(tau_a < infinity) = 1 by erfc(0) = 1).")
P("SC1-d-A1-label", "2.6-spec / attribution", "course/modules/SC/SC1/project.html Statements A0 bullet; course/modules/SC/SC1/L01.html:58; L02.html Theorem 2.5, Remark 2.6",
  "L01 Definition 1.1 is the standard Brownian motion definition; L02 Theorem 2.5 (continuous paths on [0,1]) and Remark 2.6 (extension to [0,infinity)) exist with those numbers.")
P("SC1-d-A3-A4-usage", "2.6-spec / attribution", "course/modules/SC/SC1/project.html statements; course/modules/SC/SC1/L05.html:59-70, :265-279",
  "The page's description of A3 (strong Markov for a bounded stopping time) and A4 (standard facts; A4(c) first hitting time of a closed set is a stopping time) matches L05.")
P("SC1-d-dag", "2.9-DAG", "course/modules/SC/SC1/project.html; tools/check_dag.py --unit SC1",
  "check_dag --unit SC1 PASS (" + O + "check_dag_SC1.txt). The only linked concepts are stopping-time and normal-distribution, both in the closure. No SC2/SC3 concept is named.")
P("SC1-d-notation", "2.8-notation", "course/modules/SC/SC1/project.html math (macros \\Prob, \\Normal, \\indic, \\Phi, \\tau, \\rho, \\mathcal F); notation/notation.json",
  "Every macro used is registered in notation.json macros. \\Phi used only as the normal CDF (registered meaning). The one bare T appears only in the note that the horizon is H, not T. No \\mathbb{Q}, R^*, R_f, gamma_3, gamma_4 used.")
P("SC1-d-define-before-use", "2.5-labs / 2.9-prose", "course/modules/SC/SC1/project.html (within the page)",
  "Within project.html every term is defined before its use: 'pathwise' (plain definition in the grid bullet, line 231, before uses at 429 and 455), 'filtration' (line 230), 'stopping time' (linked, closure). Cross-slice use of 'pathwise' before this definition is recorded in SC1-d-pathwise-define-before-use.")
P("SC1-d-discretization-bias", "2.9-prose / 2.4-proof", "course/modules/SC/SC1/project.html:235",
  "'The discretization bias ... is' is plain prose (no dfn, no data-concept) and is defined before its use at line 429 and in the Limitations.")
P("SC1-d-monte-carlo-term", "2.9-prose", "course/modules/SC/SC1/project.html",
  "grep for 'Monte Carlo' in project.html: no match (" + O + "grep_process_words_project_labs_grader.txt). The page uses 'simulated estimate' and 'seeded simulation' in plain words.")
P("SC1-d-scope-words", "2.9-prose (scope words)", "course/modules/SC/SC1/project.html:217, 223, 231-238, 429, 455",
  "Every 'every', 'always', 'never', 'any' and 'almost surely' occurrence was read: each is either a pathwise fact with its reason given ('the grid maximum never exceeds M_H on the same path'), a finite enumeration ('not a proof for every n and a'), a proved statement under named assumptions, or the disclaimer 'nothing about any statement that holds almost surely'.")
P("SC1-d-process-words", "2.9-prose (no process words)", "course/modules/SC/SC1/project.html; tests/labs/SC1/lab-SC1-project-{1,2,3}.py; course/modules/SC/SC1/grader/*.py",
  "grep -i builder|verifier|round|REQUESTS|unit report: only 'round' as in rounding (" + O + "grep_process_words_project_labs_grader.txt).")
P("SC1-d-banned-structure", "2.9-structure", "course/modules/SC/SC1/project.html; tools/check_pages.py --unit SC1",
  "check_pages --unit SC1 PASS (" + O + "check_pages_SC1.txt). Banned strings (TODO, TBD, lorem, clearly, obviously, ...) absent from the page prose; no ellipsis character.")
P("SC1-d-registry", "2.1-citations", "course/modules/SC/SC1/project.html reading list; references/references.json:20732",
  "Only shreve2004stochastic is cited, at book level. Registry record: title 'Stochastic Calculus for Finance II', year 2004, status verified. verify_refs --offline: 560 entries, 0 problems (" + O + "verify_refs_offline.txt).")
P("SC1-d-privacy-claim", "2.9-prose", "course/modules/SC/SC1/project.html:288 (Paste or load ... saved in this browser) and footer; course/assets/js/store.js:4, :113",
  "store.js documents browser storage with blocked-storage handling; grader.js:53 shows 'Your instance seed is ... derived from your workspace ID', matching the page. The 'saved in this browser' claim is consistent with store.js.")
P("SC1-d-tools-gates", "2.5/2.6 tooling", "repository; out/ folder of this round",
  "check_pages, check_dag, check_projects (SC1) PASS; run_labs project PASS; run_graders 0-49 PASS; page_smoke project PASS; ruff check . PASS; ruff format --check grader PASS; mypy --no-incremental PASS (385 files); pytest subset PASS; verify_refs --offline 0 problems (see SC1-d-r10-gates).")
P("SC1-d-numbers-prose", "2.2-numbers", "course/modules/SC/SC1/project.html (lines 57, 154-160, 209, 219, 225, 265, 305-317, 418-429, 524-558)",
  "All numbers in prose recomputed independently by recompute_r10.py (" + O + "recompute_r10.txt): 0.086497; 9.13e-15; 0.059548; 0.010735; 0.043248; 0.009218; 0.048142; 0.016300; 1.52; 1.77; 0.14; 1588; 794; 29/22/7; 40; nested 35/29/27/22; 132; H 2.083, a 2.474, N 487.")
P("SC1-d-spec-n41-method", "2.6-spec / 2.6-autograder", "course/modules/SC/SC1/project.html:223; grader/test_project.py:293-314",
  "The n = 41 rule (no walk listing): srw_terminal_count(41,1) = 2^40 and srw_max_count(41,1) = 2^41 - C(41,20) are checked inside a 1 s budget; r8_07 (brute force) killed 50/50 (" + O + "kill_rate_v3/r8_07*.txt); the DP alternative passes (alt_r10_c).")
P("SC1-d-ag-print-coverage", "2.6-autograder", "course/modules/SC/SC1/grader/test_project.py:40-44 (autouse _no_stray_output) and :562-592 (test_no_function_prints_or_warns)",
  "Autouse output check and the boundary sweep are present. Kill-rate over seeds 0-49 (" + O + "kill_rate_v3/): r8_01, r8_06, r9_01, r9_02, r9_03, r9_04 each killed 50 of 50 seeds. Print leaks no longer depend on the learner's seed.")
P("SC1-d-ag-walk-listing-stall", "2.6-autograder", "course/modules/SC/SC1/grader/test_project.py:293-314",
  "r8_07 (lists all 2^n walks) killed 50/50 seeds; reference passes the n = 41 test in the budget (run_graders 0-49 PASS).")
P("SC1-d-reading-disclosure", "2.9-prose / attribution", "course/modules/SC/SC1/project.html reading list; course/modules/SC/SC1/index.html:182-184",
  "Reading list says 'at book level, with no passage or theorem number attributed to it'; index.html:182-184 says the same for shreve2004stochastic and names the second source as not cited. Consistent.")
P("SC1-d-exemplar-naming", "2.9-structure (plan conformance)", "course/modules/SC/SC1/project.html exemplar-a data-level=2, exemplar-b data-level=4; plans/SC1-build-plan.md section 5.4",
  "Plan 5.4 names exemplar-a data-level 4 and exemplar-b data-level 2; the page has the reverse. Non-blocking plan deviation, recorded in notes for the architect; the rubric content is unaffected.")
P("SC1-d-r8-mutants-new", "2.6-mutation", "ledgers/SC1/mutants/r8_02..r8_07",
  "All killed on the 0-9 gate; kill-rate over seeds 0-49 is 50/50 for each (" + O + "kill_rate_v3/).")
P("SC1-d-r8-alternatives", "2.6-autograder", "ledgers/SC1/scripts/SC1-d-r8/alternatives (repathed copies under SC1-d-r10/alternatives_r8_repathed_r10)",
  "Round-8 quadrature and DP alternatives import the reference from the deleted round-8/9 checkouts and fail at import as stored. Repathed copies now load this checkout's reference and pass 50/50 (" + O + "alt_r8_bc_repathed_0_49.txt). alt_r8_a, d, e pass 50/50 (" + O + "prior_alternatives_current_suite_0_49.txt).")
P("SC1-d-r8-reference-sweep", "2.6-autograder", "course/modules/SC/SC1/grader/reference.py",
  "run_graders --unit SC1 --seeds 0-49: 50/50 (" + O + "run_graders_SC1_0-49.txt). Seeds beyond 49 not re-run this round (see notes).")
P("SC1-d-r8-proofs-trace", "2.4-proof", "course/modules/SC/SC1/project.html statements and exemplar B appendix",
  "Trace of P1 to P3 as in SC1-d-exemplarB-proof; no step skipped without a stated reason.")
P("SC1-d-ag-level-equality-survivors", "2.6-mutation", "ledgers/SC1/mutants/m35, m36; grader/test_project.py:415-428 and :506-513",
  "m35 and m36 (strict inequality at the level) killed 50/50 seeds (" + O + "kill_rate_v3/m35*.txt, m36*.txt).")
P("SC1-d-ag-mutants-r6-new", "2.6-mutation", "ledgers/SC1/mutants/m37_one_path_accepted_with_zero_error.py",
  "Killed on the gate and 50/50 seeds.")
P("SC1-d-ag-draws-depend-overconstraint", "2.6-autograder", "course/modules/SC/SC1/grader/test_project.py:448-456",
  "Over-constraint check: the test sets a = 1e-9 so that paths reach the level on every grid; alt_r10_a..e (all distinct draws) pass 50/50 seeds.")
P("SC1-d-ag-band-overconstraint", "2.6-autograder", "course/modules/SC/SC1/grader/test_project.py:120-123 and call sites",
  "Five-SE band with the target's SE: alt_r10_a..e pass 50/50 seeds, so no valid implementation is rejected. Single-seed false-failure probability per band is about 6e-7.")
P("SC1-d-delta-r5-read", "2.9-prose (delta read)", "course/modules/SC/SC1/project.html",
  "Whole file re-read this round (638 lines) after the delta c93dd526..00a84795.")
P("SC1-d-delta-r6-read", "2.9-prose (delta read)", "course/modules/SC/SC1/project.html; grader/test_project.py",
  "Whole files re-read this round, with the delta hunks in project.html and test_project.py (autouse output check, boundary sweep).")
P("SC1-d-r7-mutants-new", "2.6-mutation", "ledgers/SC1/mutants/m38-m41",
  "Killed on the gate; kill-rate 50/50 seeds for each (" + O + "kill_rate_v3/m38*, m39*, m40*, m41*).")
P("SC1-d-r7-mutants-all", "2.6-mutation", "ledgers/SC1/mutants/ (all grader mutants)",
  "mutate_graders --unit SC1 --seeds 0-9 (final): 64/64 listed mutants killed (" + O + "mutate_graders_SC1_0-9_final.txt). The six SC1a lab-twin files are counted by the tool; see SC1-d-r10-mutant-folder-hygiene.")
P("SC1-d-r7-alternatives-sweep", "2.6-autograder", "ledgers/SC1/scripts/SC1-d-r7/alternatives/*.py",
  "Re-run this round on seeds 0-49 against the current suite: alt1, alt2, alt3, alt5, alt6, alt7, alt8, alt9 pass 50/50; alt2b (enumerates 2^41 walks) and alt4 (Box-Muller) are killed by design (" + O + "prior_alternatives_current_suite_0_49.txt).")
P("SC1-d-r7-reference-sweep-500", "2.6-autograder", "course/modules/SC/SC1/grader/reference.py",
  "Scope narrowed this round: reference passes seeds 0-49 under the current suite (" + O + "run_graders_SC1_0-49.txt). The 500-seed sweep of round 7 was not re-run; see notes.")
P("SC1-d-r7-starter-fails", "2.6-autograder", "course/modules/SC/SC1/grader/starter.py",
  "Suite fails starter 3 of 3 seeds (" + O + "starter_fails_0_2.txt).")
P("SC1-d-r7-instances-sample", "2.6-autograder", "course/modules/SC/SC1/grader/instance.py",
  "All 50 seeds checked (not a sample): valid, 49 distinct levels (" + O + "recompute_r10.txt).")
P("SC1-d-r7-numbers-recompute", "2.2-numbers", "course/modules/SC/SC1/project.html:154-160, 418-428, 524-558",
  "Recomputed by recompute_r10.py; all equal to the printed and quoted values.")
P("SC1-d-r7-page-vs-twin", "2.5-labs", "course/modules/SC/SC1/project.html Labs 1-3; tests/labs/SC1/lab-SC1-project-{1,2,3}.py",
  "Page code equals twin (modulo final newline); expected blocks equal twin output (" + O + "page_vs_twin_r10.txt).")
P("SC1-d-r7-gates-full", "2.5/2.6 tooling", "repository root",
  "Gates run this round, see SC1-d-r10-gates and SC1-d-tools-gates.")
P("SC1-d-r7-registry-live", "2.1-citations", "references/references.json (shreve2004stochastic); openlibrary.org/books/OL51662040M",
  "Plain curl of the cited Open Library record: HTTP 200, title 'Stochastic Calculus for Finance II', publish_date 2004 (" + O + "openlibrary_shreve_r10.txt).")
P("SC1-d-r7-page-smoke", "2.9-structure", "course/modules/SC/SC1/project.html",
  "page_smoke --unit SC1 --pages project PASS (" + O + "page_smoke_SC1_project.txt).")
P("SC1-d-r7-alt4-ruling10", "2.6-autograder (alternatives, plan 5.7(4))", "plans/SC1-build-plan.md section 5.7(4); ledgers/SC1/scripts/SC1-d-r7/alternatives/alt4_box_muller_step_major.py; project.html Conventions (gauss draw order)",
  "The plan's alternative 4 (Box-Muller increments) is killed 50 of 50 seeds by test_one_step_draws_are_the_seeded_gaussians, because the page states the increments are drawn with random.Random(seed).gauss. The plan's alternative cannot be a correct implementation under the page. Substitute: alt_r10_d (gauss, step-major) passes. Recorded as a plan conflict for the architect (notes).")
P("SC1-d-hunk-standard-error-sentence", "2.9-prose", "course/modules/SC/SC1/project.html:53",
  "'A standard error is the estimated standard deviation of a simulated estimate, so it measures the sampling noise of one run' is accurate for the seeded estimator.")
P("SC1-d-hunk-no-more-often", "2.6-spec / 2.4-proof", "course/modules/SC/SC1/project.html:217",
  "'reaches a level no more often than the continuous maximum does' is true pathwise: the grid maximum is at most M_H on each path, so its exceedance event is contained in {M_H >= a}.")
P("SC1-d-hunk-filtration", "2.6-spec / attribution", "course/modules/SC/SC1/project.html:230",
  "F_t and F_rho are defined in Sections 1 and 3 of L05 (L05 section 1: filtration; section 3: stopping time and F_rho), as cited.")
P("SC1-d-hunk-one-step-target-se", "2.2-numbers / 2.5-labs", "course/modules/SC/SC1/project.html:429",
  "Target SE 0.009218 is the SE of the one-step target tail/2 (Lab 1 prints it); the 1.77 target SEs is 0.016300/0.009218 (recomputed).")
P("SC1-d-index-rung2-text", "2.9-prose (cross-check)", "course/modules/SC/SC1/index.html:168",
  "'Completion problem ... with the identity line and the final comparison line removed' matches Lab 2's two ___ lines.")
P("SC1-d-L05-A4-i", "2.6-spec / attribution", "course/modules/SC/SC1/L05.html:69 (A4(i)); project.html statements",
  "A4(i) exists (freezing for integrable functions) and the project does not use it.")
P("SC1-d-plan-tolerance", "2.6-spec (plan conformance)", "plans/SC1-build-plan.md section 5.5 ('within 1e-12'); project.html Conventions; grader/test_project.py:186",
  "Plan says 1e-12; page and test use 1e-10. The looser tolerance admits no student error the plan lists; recorded as a non-blocking plan deviation for the architect.")
P("SC1-d-numbers-target-se", "2.2-numbers", "course/modules/SC/SC1/project.html:429; Lab 1 output",
  "0.009218 target SE equals sqrt(0.043248 x 0.956752 / 487) = 0.009218 (recomputed).")

# ---- round-9 FAIL rows, re-verified this round
P("SC1-d-dfn-policy", "2.9-prose (architect policy: no dfn outside the closure)", "course/modules/SC/SC1/project.html (no <dfn> element)",
  "grep '<dfn' project.html: no match. 'pathwise' (line 231) and 'discretization bias' (line 235) are plain prose. Round-9 FAIL cleared.")
P("SC1-d-r9-mutants-new", "2.6-mutation", "ledgers/SC1/mutants/r9_01..r9_04",
  "Killed 50 of 50 seeds each (" + O + "kill_rate_v3/r9_0*.txt); the autouse output check and the boundary sweep catch the leftover prints regardless of seed. Round-9 FAIL cleared.")
P("SC1-d-exemplar-a-annotations", "2.9-prose (annotation accuracy, calibration)", "course/modules/SC/SC1/project.html exemplar A annotations (C2 at 499, C3 at 486-488)",
  "Round-9 fix applied: the C2 annotation now reads 'P2 and P3 are not proved ... level 3 needs all three proved in full' and the C3 note says 1.52 is derived from the printed 0.016300 and 0.010735. Both accurate. Round-9 FAIL cleared.")

# ---- round-9 row that stays FAIL
P("SC1-d-pathwise-define-before-use", "2.9-prose / define-before-use (rule 5, rule 14)",
  "course/modules/SC/SC1/L01.html:67 (first use, unchanged since round 9); project.html:231 (plain-prose definition); also L03.html:261,278,452,484; L07.html:164,303,367; L08.html:217-236,347",
  "grep 'pathwise' in SC1 lessons: L01.html:67 ('(D1) is pathwise only at time 0') is the first use in the unit's reading order, and the only definition is the plain sentence at project.html:231, the last page. L01 is unchanged since the round-9 pin (git diff c93dd526 00a84795). The term is used in L01 to L08 before its definition.",
  status="FAIL",
  fix="Define 'pathwise' once in L01 at its first use (plain <dfn> with id def-pathwise in L01.html near line 67, or reword L01.html:67 without the term), then change project.html:231 to link to that definition instead of redefining it. Owner: the L01 builder (slice a); the project slice follows the link.")

# ---- new round-10 rows
P("SC1-d-r10-mutant-seed-coverage", "2.6-autograder (rule 11: student-error mutants must fail for a learner's own seed)",
  "course/modules/SC/SC1/grader/test_project.py:493-528 (nested tests), :515-517 (equal grids), :500-503; ledgers/SC1/mutants/m07, m11, m18, m19, m21, m25, m27, m31, m32, m34, r10_06",
  "Kill counts over seeds 0-49 (" + O + "kill_rate_v3/*.txt): m07 49, m11 44, m18 26, m19 48, m21 49, m25 44, m27 44, m31 15, m32 49, m34 44, r10_06 24 (of 50). The plan gate (killed by some seed in 0-9) passes, but a learner whose seed is in the survivor list passes a buggy engine. m11, m25, m27, m34 survive seeds 0, 8, 9, 15, 32, 33 (seed 0 is the report seed); m31 survives 35 seeds; m18 survives 24; r10_06 (the coarse grid drops its first coarse point, which the page defines as every n_fine/n_coarse-th point on the same paths) survives 26. The page states the nested definition (Conventions 'nested_grid_counts' bullet) and the discrete definition, so these are stated-behaviour violations.",
  status="FAIL",
  fix="Add two deterministic tests to grader/test_project.py that regenerate the paths from random.Random(seed).gauss path by path, step by step (the page's stated draw order) and compare exactly: (i) discrete_max_exceedance(instance, n) estimate equals the explicit hit count / n_paths for n in (1, 3, 8, instance n_steps) on INST and INST2; (ii) nested_grid_counts(instance, n_fine, n_coarse) equals the explicit (fine, coarse) counts for every GRID_PAIRS pair on INST and INST2, with the coarse maximum over the points at indices k*stride-1. Verified in this round: ledgers/SC1/scripts/SC1-d-r10/proposed_test_project_v2.py passes reference 50/50 and alternatives a, b, c, e 50/50, and kills every one of the eleven mutants 50/50 (" + O + "proposed_v2_mutants/). Also narrow the page sentence 'An implementation that draws the same gauss values in another order can still pass the tests' (Conventions, discrete bullet), because the proposed test rejects a step-major order (alt_r10_d). m09 (hard-coded seed-0 answer) is killed only on seed 0 by construction and is not counted here (see notes).",
  )
P("SC1-d-r10-new-mutants", "2.6-mutation", "ledgers/SC1/mutants/r10_01..r10_05",
  "Five new student-error mutants: r10_01 factor 2 on the endpoint count (srw_max_count), r10_02 last path dropped, r10_03 continuity-correction level shift, r10_04 terminal count one level low, r10_05 horizon ignored. Each killed on 50 of 50 seeds (" + O + "r10_mutants_seeds_0_49.txt).")
P("SC1-d-r10-alternatives", "2.6-autograder (alternatives, plan 5.7)", "ledgers/SC1/scripts/SC1-d-r10/alternatives/alt_r10_a..e.py",
  "Five verifier-written correct engines, each passing seeds 0-49 (" + O + "alternatives_seeds_0_49.txt): NormalDist tail; Simpson-only tail; DP walk counts; step-major gauss order (replacing plan alternative 4); index-subsampled nested counts.")
P("SC1-d-r10-prior-alternatives", "2.6-autograder (earlier rounds' alternatives re-run against the current suite)", "ledgers/SC1/scripts/SC1-d-r7/alternatives, SC1-d-r8/alternatives, SC1-d-r9/alternatives, SC1-d-r10/alternatives_r8_repathed_r10",
  "All valid alternatives pass seeds 0-49 with the current suite (" + O + "prior_alternatives_current_suite_0_49.txt, " + O + "alt_r8_bc_repathed_0_49.txt). Killed by design: alt2b (lists 2^41 walks) and alt4 (Box-Muller). Stale-path hygiene: the round-8 and round-9 copies import the reference from deleted checkouts (verifyE8/verifyE9-SC1-d); the repathed copies are kept under SC1-d-r10/alternatives_r8_repathed_r10.")
P("SC1-d-r10-lab-twins", "2.5-labs", "tests/labs/SC1/lab-SC1-project-{1,2,3}.py; course/modules/SC/SC1/project.html",
  "run_labs --unit SC1 --page project PASS 3/3; each twin under python -I -W error exits 0; page code equals twin; expected blocks equal stdout (" + O + "page_vs_twin_r10.txt, " + O + "run_labs_SC1_project.txt).")
P("SC1-d-r10-gates", "2.5/2.6 tooling", "repository",
  "check_pages --unit SC1 PASS; check_dag --unit SC1 PASS; check_projects --unit SC1 PASS; run_graders --unit SC1 --seeds 0-49 PASS 50/50; ruff check . PASS; ruff format --check course/modules/SC/SC1/grader PASS; mypy --no-incremental PASS (385 files); pytest -q on test_labs, test_run_labs, test_page_checks (SC1 subset) and test_memo_exemplars exit 0; verify_refs --offline 560 entries 0 problems (" + O + "*.txt).")
P("SC1-d-r10-registry-live", "2.1-citations", "references/references.json; course/modules/SC/SC1/project.html reading list",
  "Open Library record for shreve2004stochastic read by plain curl: HTTP 200, title and year 2004 match the registry record (" + O + "openlibrary_shreve_r10.txt).")
P("SC1-d-r10-page-smoke", "2.9-structure / 2.6-autograder", "tools/page_smoke.py --unit SC1 --pages project",
  "PASS (" + O + "page_smoke_SC1_project.txt): in-browser (Pyodide) grader runs the 132 tests on seed 60449209 with the reference, all pass in 1.2 s.")
P("SC1-d-r10-mutant-folder-hygiene", "ledger hygiene (rule 11, lab twins are not grader mutants)", "ledgers/SC1/mutants/SC1a-lab-mut1..3 and SC1a-r6-lab-mut1..3 (six files)",
  "tools/mutate_graders.py reads every .py in ledgers/SC1/mutants, so the six SC1a lab-twin files are counted as grader mutants and 'killed' by the coverage test (the twins have no bm_checks functions). The count 64/64 therefore includes six non-grader files. No verdict effect; the grader's own mutant count is 58.",
  status="PASS")

notes = (
    "Verdict FAIL with two non-PASS rows. (1) SC1-d-pathwise-define-before-use: 'pathwise' is used in L01.html:67 before the unit defines it (project.html:231, plain prose on the last page); owner L01 builder. "
    "(2) SC1-d-r10-mutant-seed-coverage: eleven student-error mutants (m07, m11, m18, m19, m21, m25, m27, m31, m32, m34, r10_06) pass the suite on some seeds in 0-49 (survivor counts 1, 6, 24, 2, 1, 6, 6, 35, 1, 6, 26). The plan gate (each mutant killed by some seed in 0-9, which mutate_graders.py checks) passes 64/64, so this FAIL applies rule 11 at the learner's own seed; the architect may rule that the seeds 0-9 gate is the criterion, in which case this row becomes a NOTE. Proposed fix verified in scratch (see fix text). "
    "Calibration: exemplar A scores 1,2,2,2,1 and exemplar B 4,4,4,3,4 derived from the rubric text, equal to the official data-scores; CAVEAT: not strictly blind, because the whole page including the verdict lines was read before scoring. "
    "Plan deviations for the architect (non-blocking, recorded as PASS rows): (a) tolerance 1e-10 on the page and test vs plan 5.5 1e-12; (b) exemplar data-levels reversed vs plan 5.4; (c) plan 5.7 alternative 4 (Box-Muller) conflicts with the page's stated gauss draw order and is killed by design, so verifier alternative alt_r10_d (step-major gauss) replaces it; (d) alternatives stored under ledgers/SC1/scripts/SC1-d-r10/ rather than plan's ledgers/SC1/scripts/alternatives/. "
    "m09 (hard-coded answer for seed 0 only) is killed on seed 0 only by construction; a learner's seed is never 0 in practice, so it is inert for learners; the page's second-instance clause (INST2) addresses learner-level hard-codes, which no mutant here exercises. Not counted in SC1-d-r10-mutant-seed-coverage. "
    "Ledger hygiene: six SC1a lab-twin files sit in ledgers/SC1/mutants and are counted by mutate_graders (SC1-d-r10-mutant-folder-hygiene). Round-8/9 alternatives import deleted checkouts (repathed copies kept). "
    "Scope of 'pathwise': the page's own definition (project.html:231) is plain prose and is used correctly within the page. "
    "Not checked: the 500-seed reference sweep of round 7 (only 0-49 this round); the in-browser kill of the mutants (page_smoke runs only the reference in Pyodide); the 1-second budget under Pyodide for the n = 41 test (only CPython timing); the full repository pytest suite (only SC1-related modules); mypy covers tests/ and tools/ only, so grader files are covered by ruff and by the suite; verify_refs live for units other than SC1 (not run); the rubric blind calibration is not strictly blind (see above); lessons L01-L08 and cards are other slices, checked only where the project cites them."
)

mutants = []
for m in sorted((ROOT / "ledgers/SC1/mutants").glob("*.py")):
    if "SC1a" in m.name:
        continue
    import ast
    doc = ast.get_docstring(ast.parse(m.read_text(encoding="utf-8"))) or ""
    mutants.append({"name": m.name, "description": doc.splitlines()[0] if doc else m.name, "killed_by": "see out/mutate_graders_SC1_0-9_final.txt (seeds 0-9); kill counts over seeds 0-49 in out/kill_rate_v3/"})

fragment = {
    "unit": "SC1",
    "slice": "d",
    "round": 10,
    "verifier": "Claude Haiku 5.5, independent verifier for SC1-d, round 10 (did not build SC1; re-verified every round-9 row against the c93dd526..00a84795 delta)",
    "pin": "00a84795f276456fce19d4181373cc4efba11a36",
    "base": "c93dd526025c6dffd34c54cd2c89eb62a890f885 (round-9 pin)",
    "checkout": str(ROOT),
    "scratch": "/tmp/sc1d-r10/ (work copies); durable scripts and outputs under ledgers/SC1/scripts/SC1-d-r10/",
    "verified_at": "2026-11-05T09:30:00+00:00",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": notes,
    "summary": "SC1 slice d round 10: FAIL. Rows: %d (non-PASS 2: SC1-d-pathwise-define-before-use, SC1-d-r10-mutant-seed-coverage). Mutants: %d listed, %d killed on seeds 0-9 (mutate_graders gate), 11 of the grader mutants killed on fewer than 50 of seeds 0-49." % (len(rows), len(mutants), len(mutants)),
}
out = ROOT / "ledgers/SC1/SC1-d.json"
out.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out, "rows", len(rows), "mutants", len(mutants))
