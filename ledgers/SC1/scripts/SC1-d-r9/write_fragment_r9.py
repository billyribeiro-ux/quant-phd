"""Writes ledgers/SC1/SC1-d.json for round 9 (SC1 slice d, pin c93dd52). Rows are the round-8 ids (kept) plus new ids.
Usage: python -I write_fragment_r9.py  (run from the checkout root)."""

import json
import re

OUT = "ledgers/SC1/SC1-d.json"
R = "ledgers/SC1/scripts/SC1-d-r9"
rows = []


def row(rid, check, location, status, evidence, fix=None):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        assert fix, rid
        r["fix"] = fix
    rows.append(r)


P = "PASS"
F = "FAIL"
PRINT_FIX = (
    "Add an autouse fixture to course/modules/SC/SC1/grader/test_project.py: def _no_stray_output(capsys) that yields and "
    "then expect(capsys.readouterr().out == '', 'no function may print'); and sweep every public function over its inputs "
    "in test_no_function_prints_or_warns (reflection_tail over t in 1e-9..4.0 and a in 1e-9..10; discrete_max_exceedance for "
    "n_steps 1..8; nested_grid_counts over GRID_PAIRS; srw_max_count and srw_terminal_count for 1 <= n <= 12 and 1 <= a <= n + 1). "
    "Verified in scratch: " + R + "/proposed_fix/test_project_fixed3.py passes the reference and the five new alternatives "
    "(seeds 0-9), and kills r8_01, r8_06, r9_01, r9_02, r9_03 and r9_04 on all 50 seeds 0-49 (" + R + "/out/fixed3/)."
)

row("SC1-d-ladder", "2.6-ladder", "course/modules/SC/SC1/project.html:40-49",
    P, "Read in full at c93dd52. Four rungs in order (Lab 1, Lab 2, specification and autograder, stretch). check_projects SC1: PASS (out/check_projects_all.txt).")
row("SC1-d-grading-mode", "2.6-grading", "course/modules/SC/SC1/project.html:225; curriculum/03-markets.yaml (SC1 project grading: both)",
    P, "project.html:225 says 'Both' and 132 tests. collect-only prints '132 tests collected' (run in scratch with the reference as bm_checks.py). curriculum/03-markets.yaml unchanged in the delta.")
row("SC1-d-spec-signatures", "2.6-spec", "course/modules/SC/SC1/project.html:221 vs grader/starter.py:16-36",
    P, "project.html:221 lists the five signatures; starter.py:16-36 byte-identical to 0dee921 (not in the delta).")
row("SC1-d-spec-rounding-statement", "2.2-numbers / 2.9-prose", "course/modules/SC/SC1/project.html:223 vs labs at :154-160, :206-208, :418-428",
    P, "project.html:223 states the rounding rule; every printed decimal in Labs 1-3 is :.6f or :.2e of an unrounded value (labs' code; twin output equals expected block, out/page_checks_r9.txt; recompute out/recompute_r9.txt).")
row("SC1-d-hours", "2.6-hours", "course/modules/SC/SC1/project.html:33, 274-280; course/modules/SC/SC1/index.html:29",
    P, "project.html:274-280 rows 2+3+10+8+3+2 = 28 (total 28). index.html:29 data-hours-project=28, data-hours-lessons=72 (index.html:29 unchanged; the delta changed only index.html:168). 72+28 = 100.")
row("SC1-d-spec-grid-table", "2.6-spec", "course/modules/SC/SC1/project.html:213-265, 433-445",
    P, "Read in full at c93dd52. Hunks at :217 (no more often), :227-230 (filtration, pathwise) and :429 re-checked against the engine, the labs and test_project.py.")
row("SC1-d-spec-tolerance-statement", "2.6-spec", "course/modules/SC/SC1/project.html:234, 238; grader/test_project.py:112-115 (simulation_band), :178 (1e-10)",
    P, "project.html:234 states 1e-10 and test_project.py reflection tests use 1e-10; project.html:238 '5 se + 1/N' equals simulation_band. Plan 5.5 says 1e-12 for the erfc test: see note NOTE-plan-tolerance.")
row("SC1-d-ag-reference", "2.6-autograder", "course/modules/SC/SC1/grader/reference.py; tools/run_graders.py",
    P, "run_graders SC1: 'PASS (reference 50/50 seeds)' (out/run_graders_SC1.txt). reference seeds 0-9 pass 10 of 10 (out/reference_seeds_0_9_r9.txt); seeds 1000-1199 give 200 of 200 pass (out/reference_sweep_1000_1199_r9.txt).")
row("SC1-d-ag-starter", "2.6-autograder", "course/modules/SC/SC1/grader/starter.py",
    P, "starter.py on seed 0: '128 failed, 4 passed' (out/instances_and_leaks_r9.txt). The 4 are instance tests (test_instance_is_labelled_and_valid x2, determinism, fifty seeds).")
row("SC1-d-ag-instances", "2.6-autograder", "course/modules/SC/SC1/grader/instance.py",
    P, "instance.py byte-identical to 0dee921. Seeds 0-19: all valid (H>0, a>0, 4<=n<=256, 400<=N<=800, n*N<=200000) and 20 distinct levels and 20 distinct reference estimates (out/instances_and_leaks_r9.txt). run_graders instance checks PASS for 0-49.")
row("SC1-d-ag-count", "2.6-autograder", "course/modules/SC/SC1/grader/test_project.py; course/modules/SC/SC1/project.html:7, 225, 296",
    P, "collect-only = 132; project.html meta :7, :225 and :296 each say 132.")
row("SC1-d-ag-messages", "2.6-autograder (failure messages never leak the answer)", "course/modules/SC/SC1/grader/test_project.py (within_budget :88-110, expect/must_raise/within helpers)",
    P, "New messages at :285-300 ('must follow from the symmetry of the steps ... not from listing the walks') carry no computed value. Pytest failure output for a wrong engine (m01, out/leak run in scratch, printed in out/instances_and_leaks_r9.txt) shows the test's own message and the learner's instance dict only, never the expected value.")
row("SC1-d-ag-overconstraint", "2.6-autograder", "course/modules/SC/SC1/grader/test_project.py; ledgers/SC1/scripts/SC1-d-r9/alternatives/*.py",
    P, "Five new correct alternatives (normal-cdf tail + (position,max) DP; erf tail + Pascal rows + sum-of-squares SE; scaled erfc + binomial split; list-comprehension draws + lru_cache + fsum; Welford one-pass SE): 50 of 50 seeds pass each, 250 of 250 (out/alternatives_sweep_0_49_r9.txt).")
row("SC1-d-ag-alternatives-ok", "2.6-autograder", "ledgers/SC1/scripts/SC1-d-r7/alternatives/ (alt1, alt2, alt3, alt5-alt9); ledgers/SC1/scripts/SC1-d-r8/alternatives/ (a, b, c, d, e)",
    P, "Round-7 alt1, alt2, alt3, alt5, alt6, alt7, alt8, alt9 pass 50/50 each; round-8 a-e pass 50/50 each on the current suite (out/alternatives_r7_r8_sweep_0_49_r9.txt; out/alternatives_r8_repathed_0_49_r9.txt). alt2b (enumeration over 2**n walks) is KILLED 50/50 by test_srw_integers_are_exact_for_a_long_odd_walk: correct behaviour under the page's 'must not list the walks' rule. alt4 (Box-Muller) KILLED 50/50 by test_one_step_draws_are_the_seeded_gaussians, consistent with ruling 10. NOTE: round-8 alt_r8_b and alt_r8_c hard-code the round-8 scratch path verifyE8-SC1-d and fail at collection in place; repathed copies (only the path changed) were used.")
row("SC1-d-ag-mutants-plan", "2.6-mutation", "ledgers/SC1/mutants/m01-m10",
    P, "tools/mutate_graders.py --unit SC1 --seeds 0-9 (out/mutate_graders_SC1_0-9_final.txt): m01-m10 KILLED (e.g. m01 by test_reflection_tail_is_the_erfc_closed_form, m09 by test_estimate_is_a_fraction_of_the_paths).")
row("SC1-d-ag-mutants-own", "2.6-mutation", "ledgers/SC1/mutants/m11-m15, m18, m19, m21",
    P, "KILLED in out/mutate_graders_SC1_0-9_final.txt.")
row("SC1-d-ag-mutants-survivors", "2.6-mutation", "ledgers/SC1/mutants/m16, m17",
    P, "KILLED by test_fine_grid_of_zero_steps_raises_value_error and test_coarse_grid_of_zero_steps_raises_value_error (out/mutate_graders_SC1_0-9_final.txt).")
row("SC1-d-ag-mutants-seed", "2.6-mutation", "ledgers/SC1/mutants/m20",
    P, "KILLED by test_draws_depend_on_the_instance_seed (out/mutate_graders_SC1_0-9_final.txt).")
row("SC1-d-ag-mutants-seed-offset", "2.6-mutation", "ledgers/SC1/mutants/m22_seed_offset_by_one.py",
    P, "KILLED by test_one_step_draws_are_the_seeded_gaussians (out/mutate_graders_SC1_0-9_final.txt).")
row("SC1-d-ag-mutants-r3", "2.6-mutation", "ledgers/SC1/mutants/m23-m26",
    P, "KILLED (out/mutate_graders_SC1_0-9_final.txt).")
row("SC1-d-ag-mutants-r4-new", "2.6-mutation", "ledgers/SC1/mutants/m27-m31",
    P, "KILLED (out/mutate_graders_SC1_0-9_final.txt).")
row("SC1-d-ag-mutants-r5-new", "2.6-mutation", "ledgers/SC1/mutants/m32, m33, m34",
    P, "KILLED (out/mutate_graders_SC1_0-9_final.txt).")
row("SC1-d-ag-page-smoke", "2.6-autograder", "course/modules/SC/SC1/project.html; tools/page_smoke.py --unit SC1 --pages project",
    P, "page_smoke SC1 project: PASS, exit 0 (out/page_smoke_SC1_project.txt); in-browser grader 'All 132 tests pass' (1.3 s).")
row("SC1-d-ag-docstring", "2.6-autograder (docstring matches the tests)", "course/modules/SC/SC1/grader/test_project.py:19",
    P, "Line 19: 'It never prints the expected value.' Verified by the leak probe (out/instances_and_leaks_r9.txt): no failure output prints an expected value. The docstring's 'names the property it checks' holds for the budget messages.")
row("SC1-d-rubric-observable", "2.9-prose", "course/modules/SC/SC1/project.html:446-457",
    P, "Rubric table read in full (C1-C5, four levels each). Every level descriptor names an element a report shows or omits; no vague qualifier other than 'some of the grids' (C5 level 2), which is a count against 'every grid' in level 3.")
row("SC1-d-calib-A", "2.9-prose / rubric calibration", "course/modules/SC/SC1/project.html:464-516 (exemplar A passages, annotations and verdict hidden; view in out/exemplars_blind_view.txt)",
    P, "Blind scores for exemplar A from the rubric only: C1 1, C2 2, C3 2, C4 2, C5 1. Official (1,2,2,2,1); all within one level. CAVEAT: before scoring I had read the official verdict line of exemplar A (:466) and the C5 annotation fragment (:512) in an earlier grep, so this is not a strictly blind score.")
row("SC1-d-exemplarA-claim", "2.2-numbers / 2.9-prose", "course/modules/SC/SC1/project.html:470, 474-475, 482, 499, 503-508, 512",
    P, "Numbers recomputed (out/recompute_r9.txt): tail 0.086497; 0.0595 with se 0.0107; 0.0163 = 0.059548 - 0.043248; 1.52 = 0.0163/0.0107; 1588 walks. Claim 'the results hold for every grid' is annotated (C4 miss) and 'finer grids closer' is annotated (C5 miss). Seed-0 tail minus estimate 0.037215, 0.020788, -0.001799, 0.004361 (non-monotone 64 to 256).")
row("SC1-d-exemplarB-onestep-claim", "2.2-numbers", "course/modules/SC/SC1/project.html:558",
    P, "0.016300 = 0.059548 - 0.043248; 1.52 = 0.016300/0.010735; band 0.048142 inside=True (out/recompute_r9.txt).")
row("SC1-d-exemplarB-numbers", "2.2-numbers", "course/modules/SC/SC1/project.html:524, 546, 558 vs Lab 1 and Lab 3 output",
    P, "0.086497; 9.13e-15 (Lab 1 prints); se list 0.010735, 0.009819, 0.011239, 0.012870, 0.012455; tail minus estimate 0.026948, 0.037215, 0.020788, -0.001799, 0.004361; nested counts 35, 29, 27, 22 against fine 40. All equal the recomputation (out/recompute_r9.txt) and the twin output (out/page_checks_r9.txt).")
row("SC1-d-exemplarB-proof", "2.4-proof / 2.9-prose", "course/modules/SC/SC1/project.html:582-595 (exemplar B appendix)",
    P, "P1 (A3 on rho = tau and t, IVT for {M_t >= a} = {tau <= t}, P(tau = t) = 0, freezing via A4(b) with the half indicator, P(A) = P(B_t >= a) + P(A)/2), P2 (erfc substitution gives 2(1 - Phi(x sqrt 2))), P3 (continuity from below) read step by step; no gap found.")
row("SC1-d-exemplarB-p1-assumptions", "2.9-prose / 2.4-proof", "course/modules/SC/SC1/project.html:246, 249, 583-584 vs course/modules/SC/SC1/L05.html A3 (:270), A4 list (:59-70), L01.html:58",
    P, "L05.html A4 list has (b) freezing, (c) hitting time of a closed set, (g) joint measurability, (h) measurability at a stopping time; the delta appended (i) only. L05.html:270 A3 unchanged. A0 = Definition 1.1 at L01.html:58 (unchanged label).")
row("SC1-d-lab1-run", "2.5-labs", "course/modules/SC/SC1/project.html:55-162; tests/labs/SC1/lab-SC1-project-1.py",
    P, "run_labs SC1: 11/11 PASS (out/run_labs_SC1.txt). Twin alone under python -I -W error: exit 0; output equals the page's expected block (out/page_checks_r9.txt, out/twin_lab1.txt).")
row("SC1-d-lab1-docstring", "2.5-labs / 2.9-prose", "course/modules/SC/SC1/project.html:58-68; tests/labs/SC1/lab-SC1-project-1.py:1-14",
    P, "Docstring matches the code: draw order horizon, level, grid size, path count (twin :34-37); six decimals by .6f; Simpson difference by .2e; H and a printed to three decimals.")
row("SC1-d-lab2-run", "2.5-labs", "course/modules/SC/SC1/project.html:164-210; tests/labs/SC1/lab-SC1-project-2.py",
    P, "run_labs PASS. Page code equals the twin except the two blanks (out/page_checks_r9.txt). Completed twin (identity = end_hits + end_above; max_hits == identity) prints 29 / 22 / 7 / True, equal to the recomputation.")
row("SC1-d-lab2-attribution", "2.9-prose / attribution", "course/modules/SC/SC1/project.html:209 vs course/modules/SC/SC1/L06.html:75, :87-88, :97",
    P, "L06.html:75 Proposition 1.3 (discrete reflection identity), :87 Corollary 1.4 (discrete tail identity), :88 'Those of Proposition 1.3', :97 proof uses it. Unchanged numbering.")
row("SC1-d-lab3-run", "2.5-labs", "course/modules/SC/SC1/project.html:303-430; tests/labs/SC1/lab-SC1-project-3.py",
    P, "run_labs PASS. Twin output equals the expected block. My recomputation (out/recompute_r9.txt) reproduces grid hits 29, 24, 32, 43, 40; se 0.010735, 0.009819, 0.011239, 0.012870, 0.012455; nested 35, 29, 27, 22; walk 1588 / 794.")
row("SC1-d-lab3-onestep-interp", "2.5-labs / 2.9-prose", "course/modules/SC/SC1/project.html:429 vs tests/labs/SC1/lab-SC1-project-3.py:99",
    P, "Changed hunk. 0.016300/0.010735 = 1.5184 (1.52); 0.016300/0.009218 = 1.7683 (1.77); 0.009218 = round(sqrt(0.0432483*0.9567517/487), 6) (out/recompute_r9.txt); 'the basis the band uses' matches Lab 1 band = 5 target se + 1/N. 0.001799/0.012870 = 0.1398 (0.14). Sentence 'sampling error -0.016300' is estimate minus target bias. All consistent.")
row("SC1-d-lab3-docstring", "2.5-labs / 2.9-prose", "tests/labs/SC1/lab-SC1-project-3.py:3-11 (page :306-317)",
    P, "Docstring: n Gaussian increments with sd sqrt(H/n), path by path from random.Random(seed); coarse grids are every 256/n point of the same 256-step paths. Matches the code (path_maxima).")
row("SC1-d-labs-pytest", "2.5-labs / tooling", "tests/test_labs.py -k SC1; tests/test_run_labs.py; tests/test_page_checks.py; tests/test_memo_exemplars.py",
    P, "pytest -k 'SC1 or sc1 or exemplar or memo or labs or run_labs or page' over those four modules: all pass (out/pytest_sc1_related.txt).")
row("SC1-d-calib-B", "2.9-prose / rubric calibration", "course/modules/SC/SC1/project.html:518-599 (exemplar B passages, verdict and annotations hidden)",
    P, "Blind scores from the rubric only: C1 4, C2 4, C3 4, C4 3, C5 4. Official (4,4,4,3,4). C4 is 3 blind because the limitations paragraph does not say what the nested comparison leaves open about the continuum. CAVEAT: the official verdict line of exemplar B (:520) was visible in my earlier grep, so this is not a strictly blind score.")
row("SC1-d-statements", "2.6-spec / 2.4-proof", "course/modules/SC/SC1/project.html:241-262",
    P, "Re-read in full. Each statement lists the hypotheses its proof uses: P1 from A0, A3, A4(b,c,g,h); P2 from P1 and the normal law; P3 from A0 with continuity and a > 0, and P2 for the second part. No used hypothesis is omitted.")
row("SC1-d-A1-label", "2.6-spec / attribution", "course/modules/SC/SC1/project.html:242, 249; course/modules/SC/SC1/L01.html:58; L02.html:289 (Theorem 2.5), :303 (Remark 2.6); L05.html:59, :270",
    P, "Labels exist with the cited content (L01 Definition 1.1 at :58; L02 Theorem 2.5 at :289 and Remark 2.6 at :303; L05 Assumptions 3 and 4 at :270 and :59). L02 unchanged in the delta.")
row("SC1-d-A3-A4-usage", "2.6-spec / attribution", "course/modules/SC/SC1/project.html:242, 246, 249; course/modules/SC/SC1/L05.html:59-70, :265-270",
    P, "A3 (bounded stopping time, L05.html:270); A4(b), A4(c), A4(g), A4(h) (L05.html:59-70, appended (i) not used by the page); 'Section 3 of Lesson 5' for stopping times and F_rho (L05.html:266-268). Usage matches each part.")
row("SC1-d-dag", "2.9-DAG", "course/modules/SC/SC1/project.html; tools/check_dag.py --all",
    P, "check_dag SC1: PASS; check_dag --all PASS for all 27 units (out/check_dag_all.txt). Concept links stopping-time and normal-distribution resolve.")
row("SC1-d-notation", "2.8-notation", "course/modules/SC/SC1/project.html passim; notation/notation.json",
    P, "notation.json symbols: T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, Q. The page uses Phi as the standard normal CDF (registry meaning, :230, :255) and T only as a named symbol that is not used (:230). H, N, a, tau, rho, F_t are not registry symbols.")
row("SC1-d-define-before-use", "2.5-labs / 2.9-prose (within the page)", "course/modules/SC/SC1/project.html:37, 45, 53, 57, 230, 231",
    P, "Within project.html: running and grid maximum defined in the lede (:37) and rungs (:53); simple random walk (:45) before Lab 2; filtration and stopping time by reference to Lesson 5 (:230); pathwise defined at :231 before its first use in the page. Cross-page use before definition is in SC1-d-pathwise-define-before-use.")
row("SC1-d-discretization-bias", "2.9-prose / 2.4-proof", "course/modules/SC/SC1/project.html:235",
    P, "Definition: P(M_H >= a) - P(max_{k<=n} B_{t_k} >= a); 'never negative' holds (grid max <= M_H on the same path); the sign of the estimate's noise at 64 steps is -0.001799 (out/recompute_r9.txt). The dfn policy question is in SC1-d-dfn-policy.")
row("SC1-d-monte-carlo-term", "2.9-prose", "course/modules/SC/SC1/project.html:231-238, 375-379, 455",
    P, "Pathwise statements (grid max <= M_H on the same path) are separated from simulated estimates (5 se + 1/N) in the text; rubric C4 separates sample results from continuum and almost-sure statements.")
row("SC1-d-scope-words", "2.9-prose (scope words)", "course/modules/SC/SC1/project.html:217, 223, 231-238, 429, 455",
    P, "Changed hunk :217 'no more often' and :231 'every path' are pathwise facts with the stated reason; 'every n up to 12' (:209) is test_srw_reflection_identity_holds_exactly and test_srw_counts_match_enumeration_for_n_up_to_12 (a in 1..n). No unbacked 'always' or 'every' quantifier found.")
row("SC1-d-process-words", "2.9-prose (no process words)", "course/modules/SC/SC1/project.html; tests/labs/SC1/lab-SC1-project-{1,2,3}.py; course/modules/SC/SC1/grader/*.py",
    P, "Grep for verifier, builder, architect, ruling, batch, round (as a process word), fixer, ledger, plan, TODO, placeholder, pending, draft, Q-numbers: no hits in prose. 'round(' hits are the Python builtin in code.")
row("SC1-d-banned-structure", "2.9-structure", "course/modules/SC/SC1/project.html; tools/check_pages.py --all",
    P, "check_pages --all: PASS for all units including SC1 (out/check_pages_all.txt). Banned strings (TODO, TBD, lorem, 'for brevity', 'beyond the scope', 'it is important to note', 'clearly', 'obviously') absent.")
row("SC1-d-registry", "2.1-citations", "course/modules/SC/SC1/project.html:619-622; references/references.json (key shreve2004stochastic)",
    P, "Only key cited: shreve2004stochastic (book level, no locator). Registry record: 'Stochastic Calculus for Finance II', Shreve, 2004, verified_by openlibrary. verify_refs --unit SC1 (live, plain run): 1 of 560 entries re-verified, 0 problems (out/verify_refs_unit_SC1_live.txt); offline 560 entries, 0 problems (out/verify_refs_offline.txt).")
row("SC1-d-privacy-claim", "2.9-prose", "course/modules/SC/SC1/project.html:288, 603; course/assets/js/grader.js:61",
    P, "'Your code is saved in this browser shortly after you stop typing': grader.js:61 is a 400 ms debounced store.put. Self-assessment kept in browser storage per the rubric store (unchanged).")
row("SC1-d-tools-gates", "2.5/2.6 tooling", "repository; ledgers/SC1/scripts/SC1-d-r9/gates.sh",
    P, "Round-9 gates at c93dd52 (out/_exits.txt): check_pages --all, check_dag --all, check_projects --all, run_labs SC1, run_graders SC1 0-49, page_smoke SC1 project, ruff check ., ruff format --check ., mypy --no-incremental (385 files), pytest on the related modules, verify_refs --offline: all exit 0. Not run: the full repository pytest suite (not needed for slice d; the changed files are covered by the related modules and the grader runs).")
row("SC1-d-numbers-prose", "2.2-numbers", "course/modules/SC/SC1/project.html:57, 154-160, 209, 219, 225, 265, 305-317, 418-429",
    P, "Every decimal and count in these prose lines equals out/recompute_r9.txt at the printed precision (2.083, 2.474, 487, 0.086497, 0.059548, 0.010735, 0.043248, 0.016300, 0.048142, 1.52, 1.77, 0.14, 0.001799, 0.012870, 1588, 794, 29/22/7, 40, 35/29/27/22).")
row("SC1-d-spec-n41-method", "2.6-spec / 2.6-autograder", "course/modules/SC/SC1/project.html:223; grader/test_project.py:285-300 (within_budget at :88-110)",
    P, "Round-8 FAIL resolved. The page says 'for n = 41 the counts must not list the walks' (:223). The suite now bounds the n = 41 calls to 1 s with a trace-based budget (test_project.py:285-300). The brute-force mutant r8_07 is KILLED in 1.3 s (out/r8_07_seed0_r9.txt; mutate tool KILLED). Reference passes 132 (0.16 s).")
row("SC1-d-ag-print-coverage", "2.6-autograder (print and warn rule, project.html:223)",
    "course/modules/SC/SC1/grader/test_project.py:554-575 (test_no_function_prints_or_warns); ledgers/SC1/mutants/r9_01, r9_02, r9_04 (r8_01, r8_06 now killed)",
    F,
    "The page states 'No function prints or warns' (project.html:223). The round-9 change enumerates more boundary inputs, but the check still covers only those inputs, so leak mutants that print on an input no test calls survive. Evidence: r9_01 (srw_max_count prints when a == n + 1) KILLED on 0 of seeds 0-49 (out/r9_mutants_seeds_0_49.txt); r9_02 (discrete_max_exceedance prints when n_steps == 3) KILLED on 0 of seeds 0-49; r9_04 (reflection_tail prints when t >= 2.5) KILLED on only 21 of seeds 0-49 (seeds 1, 4, 7 among 0-9), so a learner whose seed has H < 2.5 can leak prints unnoticed. The tool run (out/mutate_graders_SC1_0-9_final.txt) reports 56/58 killed, 2 survivors. r8_01 and r8_06 are now KILLED.",
    PRINT_FIX)
row("SC1-d-ag-walk-listing-stall", "2.6-autograder (time bound for n = 41)",
    "course/modules/SC/SC1/grader/test_project.py:285-300; course/modules/SC/SC1/project.html:223",
    P, "Round-8 FAIL resolved. r8_07 (brute force over 2**n walks) is KILLED by test_srw_integers_are_exact_for_a_long_odd_walk in 1.3 s (out/r8_07_seed0_r9.txt; mutate tool KILLED). Reference passes. NOT CHECKED: the same budget in Pyodide (the in-browser run of the reference is 1.3 s; the browser timeout is 120 s, python.js:4).")
row("SC1-d-reading-disclosure", "2.9-prose / attribution", "course/modules/SC/SC1/project.html:619-622; course/modules/SC/SC1/index.html:183",
    P, "Reading cites Shreve at book level, no theorem or passage number, consistent with the registry record.")
row("SC1-d-exemplar-naming", "2.9-structure (plan conformance)", "course/modules/SC/SC1/project.html:464 (exemplar-a data-level 2), :518 (exemplar-b data-level 4); plans/SC1-build-plan.md section 5.4",
    P, "NOTE (not a failure): the plan's section 5.4 names exemplar-a data-level 4 and exemplar-b data-level 2. The page's labels match the content (A scores 1-2, B scores 3-4). check_projects does not check the ids. Architect to confirm (see notes).")
row("SC1-d-r8-mutants-new", "2.6-mutation (round-8 mutants)", "ledgers/SC1/mutants/r8_02..r8_07",
    P, "r8_02, r8_03, r8_04, r8_05 KILLED (out/mutate_graders_SC1_0-9_final.txt). r8_01 and r8_06 now KILLED by test_no_function_prints_or_warns (round-8 FAIL resolved for these two inputs). r8_07 KILLED (see SC1-d-ag-walk-listing-stall). The print-leak class is still open: see SC1-d-ag-print-coverage.")
row("SC1-d-r8-alternatives", "2.6-autograder (alternatives)", "ledgers/SC1/scripts/SC1-d-r8/alternatives/alt_r8_a..e.py (re-pathed copies in SC1-d-r9/alternatives_r8_repathed)",
    P, "Round-8 a-e: 50/50 pass each on the current suite (out/alternatives_r8_repathed_0_49_r9.txt, 250 of 250 SURVIVED meaning pass). The round-8 files hard-code the verifyE8-SC1-d path and fail at collection as stored; the path was replaced in the copies only. Ledger hygiene: the stored round-8 files are not re-runnable as they are (VERIFIER section 3).")
row("SC1-d-r8-reference-sweep", "2.6-autograder", "course/modules/SC/SC1/grader/reference.py",
    P, "reference: run_graders 0-49 PASS 50/50; seeds 0-9 pass; seeds 1000-1199 pass 200/200 (out/reference_sweep_1000_1199_r9.txt). Seeds 0-499 of round 7 not re-run this round.")
row("SC1-d-r8-proofs-trace", "2.4-proof", "course/modules/SC/SC1/project.html:241-262 and exemplar B appendix (:582-595)",
    P, "Statements and proofs traced again at c93dd52 (see SC1-d-exemplarB-proof, SC1-d-statements). No gap.")
row("SC1-d-ag-level-equality-survivors", "2.6-mutation", "ledgers/SC1/mutants/m35, m36; grader/test_project.py:407 (level-equality test), :498 (nested level-equality test)",
    P, "KILLED by test_path_whose_maximum_equals_the_level_counts_as_reaching_it and test_nested_counts_include_a_path_whose_maximum_equals_the_level (out/mutate_graders_SC1_0-9_final.txt).")
row("SC1-d-ag-mutants-r6-new", "2.6-mutation", "ledgers/SC1/mutants/m37_one_path_accepted_with_zero_error.py",
    P, "KILLED by test_one_path_raises_value_error (out/mutate_graders_SC1_0-9_final.txt).")
row("SC1-d-ag-draws-depend-overconstraint", "2.6-autograder (over-constraint)", "course/modules/SC/SC1/grader/test_project.py:440 (test_draws_depend_on_the_instance_seed)",
    P, "Passes for the reference and all 10 correct alternatives tried on seeds 0-49 (out/alternatives_sweep_0_49_r9.txt; out/alternatives_r8_repathed_0_49_r9.txt).")
row("SC1-d-ag-band-overconstraint", "2.6-autograder (over-constraint)", "course/modules/SC/SC1/grader/test_project.py:112-115 (simulation_band), used at :374, :383, :429, :517",
    P, "simulation_band tests pass for the reference (seeds 0-49, 1000-1199) and for every correct alternative (out/alternatives_sweep_0_49_r9.txt, out/alternatives_r8_repathed_0_49_r9.txt, out/alternatives_r7_r8_sweep_0_49_r9.txt).")
row("SC1-d-delta-r5-read", "2.9-prose (delta read)", "course/modules/SC/SC1/project.html (whole file re-read at c93dd52)",
    P, "Round-5 hunks: re-read in the current page; the round-9 delta (four hunks at :53, :217, :230, :429) read in full (git diff 0dee921a c93dd526).")
row("SC1-d-delta-r6-read", "2.9-prose (delta read)", "course/modules/SC/SC1/project.html; grader/test_project.py",
    P, "Round-6 hunks re-read at c93dd52 with the round-9 changes; none of the round-6 text was reverted.")
row("SC1-d-r7-mutants-new", "2.6-mutation", "ledgers/SC1/mutants/m38-m41",
    P, "KILLED: m38 by test_reflection_tail_rejects_zero_level, m39 by test_standard_error_uses_divisor_n_minus_one, m40 by test_one_step_draws_are_the_seeded_gaussians, m41 by test_reflection_tail_is_the_erfc_closed_form (out/mutate_graders_SC1_0-9_final.txt).")
row("SC1-d-r7-mutants-all", "2.6-mutation", "ledgers/SC1/mutants/ (m01-m41 and all later mutants)",
    P, "All m01-m41 KILLED on seeds 0-9 in out/mutate_graders_SC1_0-9_final.txt. The two survivors are new this round (r9_01, r9_02), see SC1-d-ag-print-coverage.")
row("SC1-d-r7-alternatives-sweep", "2.6-autograder (alternatives)", "ledgers/SC1/scripts/SC1-d-r7/alternatives/*.py",
    P, "alt1, alt2, alt3, alt5-alt9 pass 50/50 each on the current suite (out/alternatives_r7_r8_sweep_0_49_r9.txt). alt2b and alt4 excluded as above.")
row("SC1-d-r7-reference-sweep-500", "2.6-autograder", "course/modules/SC/SC1/grader/reference.py",
    P, "Re-run this round: seeds 0-49 (run_graders) and 1000-1199 (200/200). Round-7 seeds 0-499 not re-run (scope note).")
row("SC1-d-r7-starter-fails", "2.6-autograder", "course/modules/SC/SC1/grader/starter.py",
    P, "128 failed, 4 passed on seed 0 (out/instances_and_leaks_r9.txt).")
row("SC1-d-r7-instances-sample", "2.6-autograder", "course/modules/SC/SC1/grader/instance.py",
    P, "Seeds 0-19 sampled and valid, 20 distinct levels (out/instances_and_leaks_r9.txt); run_graders instance checks PASS 0-49.")
row("SC1-d-r7-numbers-recompute", "2.2-numbers", "course/modules/SC/SC1/project.html:154-160, 418-428, 524-558",
    P, "Independent recomputation written from the page's specification, not from the lab code: ledgers/SC1/scripts/SC1-d-r9/recompute_r9.py -> out/recompute_r9.txt. Matches every printed value.")
row("SC1-d-r7-page-vs-twin", "2.5-labs", "course/modules/SC/SC1/project.html:55-210, 303-430; tests/labs/SC1/lab-SC1-project-{1,2,3}.py",
    P, "ledgers/SC1/scripts/SC1-d-r9/page_checks_r9.py -> out/page_checks_r9.txt: page code equals twin for labs 1 and 3; lab 2 differs in the two blanks only; twin output equals the expected block for all three.")
row("SC1-d-r7-gates-full", "2.5/2.6 tooling", "repository root; ledgers/SC1/scripts/SC1-d-r9/gates.sh",
    P, "ruff check . 'All checks passed!'; ruff format --check . '553 files already formatted'; mypy --no-incremental 'Success: no issues found in 385 source files' (out/ruff_check.txt, out/ruff_format.txt, out/mypy.txt).")
row("SC1-d-r7-registry-live", "2.1-citations", "references/references.json (shreve2004stochastic)",
    P, "Live verify_refs --unit SC1: 1 of 560 entries, 0 problems (out/verify_refs_unit_SC1_live.txt).")
row("SC1-d-r7-page-smoke", "2.9-structure", "course/modules/SC/SC1/project.html",
    P, "page_smoke SC1 project: PASS (out/page_smoke_SC1_project.txt), zero console errors reported by the tool.")
row("SC1-d-r7-alt4-ruling10", "2.6-autograder (alternatives, ruling 10)", "plans/SC1-build-plan.md section 5.7(4); project.html:232 (gauss draw order)",
    P, "Box-Muller alternative (alt4) is KILLED 50/50 by the one-step draw test, consistent with excluding it from the correct alternatives (ruling 10 as recorded in round 8).")

# ---- round-9 new rows
row("SC1-d-r9-mutants-new", "2.6-mutation (new mutants, at least 3 required)", "ledgers/SC1/mutants/r9_01..r9_04",
    F,
    "Four new student-error mutants (leftover prints in srw_max_count at a == n + 1, discrete_max_exceedance at n_steps == 3, nested_grid_counts at n_coarse >= 4, reflection_tail at t >= 2.5). r9_03 is KILLED by test_no_function_prints_or_warns (n_coarse = 6 is in its input list). r9_01 and r9_02 SURVIVE every seed 0-49; r9_04 is KILLED on 21 of 50 seeds. Each is a surviving-or-seed-dependent fault against the stated 'No function prints or warns' (project.html:223). Survivors make the mutant set FAIL under the rule that a surviving grader mutant violating a stated behaviour is a FAIL.",
    PRINT_FIX)
row("SC1-d-dfn-policy", "2.9-prose (architect decision: no dfn outside the prerequisite closure)",
    "course/modules/SC/SC1/project.html:231 (<dfn>pathwise</dfn>, new this round), :235 (<dfn>discretization bias</dfn>, present since 0dee921)",
    F,
    "The architect decisions (2026-11-03, binding) say: 'concepts outside the prerequisite closure are plain prose with no link and no dfn'. 'pathwise' is a new <dfn> and 'discretization bias' an existing <dfn>; neither is a curriculum concept (curriculum/03-markets.yaml SC1 introduces lists brownian-motion ... first-passage-time only). check_dag ignores un-tagged dfn, so the gate does not catch it.",
    "Replace both <dfn> elements with plain prose (for example <em>pathwise</em> without the dfn element, or plain text), or obtain an architect ruling that in-page definitions of non-curriculum terms are allowed and record it in plans/SC1-build-plan.md.")
row("SC1-d-pathwise-define-before-use", "2.9-prose / define-before-use (terms used before definition)",
    "course/modules/SC/SC1/L01.html:67 (new this round); also L03.html:261, :278, :452, :484; L07.html:164, :303, :367; L08.html:217-236, :347; project.html:231 (definition)",
    F,
    "'pathwise' is first used in L01.html:67 ('(D1) is pathwise only at time 0', new in the delta) and in L03/L07/L08 before the project's definition at project.html:231. Within project.html the term is defined before its uses (:231, :429, :455), so the page itself passes. This is a cross-slice define-before-use defect that this round's definition exposes.",
    "Define 'pathwise' once in the lesson that first uses it (Lesson 1, Section 1, with a dfn that has the lesson's own id) or reword L01.html:67 without the term, and make project.html link to that definition instead of redefining it. Owner: the slice that builds L01 (the lesson slices), with the project text following.")
row("SC1-d-exemplar-a-annotations", "2.9-prose (annotation accuracy, calibration)",
    "course/modules/SC/SC1/project.html:499 (C2 annotation on exemplar A), :486 (C3 annotation), :494-500 (exemplar A appendix)",
    F,
    "(a) The C2 annotation (:499) says 'the symmetry step is ... a step skipped without a stated gap'. The P1 symmetry step is not skipped: it is justified by 'by symmetry'. The real level-2 reason, which the annotation never states, is that exemplar A proves only P1: P2 and P3 have no proof, and level 3 requires each of P1, P2 and P3 to be proved in full. (b) The C3 annotation (:486) says 'with no number the run does not print', but exemplar A quotes 1.52, which Lab 1 and Lab 3 do not print (it is derived in the Lab 3 prose only, out/recompute_r9.txt). Scores are unaffected (C2 2, C3 2), so calibration still PASSES; the annotation reasons are wrong.",
    "Rewrite the C2 annotation at project.html:499 to say: 'Meets C2 level 2: P1 is proved with the symmetry step justified by symmetry, but P2 and P3 have no proof; level 3 needs all three proved in full.' Rewrite the C3 annotation at :486 to say that 1.52 is derived from the printed 0.016300 and 0.010735, not printed, and that the decimals lack a rounding statement.")

# ---- round-9 hunks (carried reads of the changed text)
row("SC1-d-hunk-standard-error-sentence", "2.9-prose", "course/modules/SC/SC1/project.html:53",
    P, "New sentence 'A standard error is the estimated standard deviation of a simulated estimate, so it measures the sampling noise of one run.' Consistent with the SE definitions at :230 and Lab 1 and Lab 3 printed SE columns.")
row("SC1-d-hunk-no-more-often", "2.6-spec / 2.4-proof", "course/modules/SC/SC1/project.html:217",
    P, "'reaches a level no more often than the continuous maximum does' is the pathwise inequality (grid max <= M_H on each path, so P(grid >= a) <= P(M_H >= a)). Consistent with the bias definition at :235 and the notice at :235 that the bias is never negative.")
row("SC1-d-hunk-filtration", "2.6-spec / attribution", "course/modules/SC/SC1/project.html:230",
    P, "F_t and F_rho 'as defined in Sections 1 and 3 of Lesson 5': L05.html:56 defines F_t = sigma(B_r, r <= t) in Section 1 and L05.html:268 defines F_rho in Section 3. Correct.")
row("SC1-d-hunk-one-step-target-se", "2.2-numbers / 2.5-labs", "course/modules/SC/SC1/project.html:429",
    P, "Changed hunk verified: 0.016300/0.009218 = 1.77 (1.7683), target se 0.009218 = Lab 1 printed target standard error; 'the basis the band uses' matches Lab 1 band = 5 target se + 1/N.")
row("SC1-d-index-rung2-text", "2.9-prose (cross-check of a changed neighbour file)", "course/modules/SC/SC1/index.html:168",
    P, "index.html:168 now says 'with the identity line and the final comparison line removed' (was 'cap line'). Matches Lab 2 (two blanks: the identity line and the comparison line). index.html is outside slice d; noted only.")
row("SC1-d-L05-A4-i", "2.6-spec / attribution", "course/modules/SC/SC1/L05.html:69 (A4(i) appended)",
    P, "A4 gained (i) in the delta; project.html cites only A4(b), (c), (g), (h), whose text is unchanged. No effect on the page's citations.")
row("SC1-d-plan-tolerance", "2.6-spec (plan conformance, tolerance)", "plans/SC1-build-plan.md section 5.5 ('within 1e-12'); course/modules/SC/SC1/project.html:234; grader/test_project.py:75-84 (erfc test uses 1e-10)",
    P, "NOTE (not a page defect): the plan says the erfc test is 1e-12; page and test both use 1e-10, a looser and internally consistent choice. No mutant depends on it. Architect to confirm (see notes).")

# ---- row-level check of the one-step SE and related numbers that were not in round 8
row("SC1-d-numbers-target-se", "2.2-numbers", "course/modules/SC/SC1/project.html:429; tests/labs/SC1/lab-SC1-project-1.py output",
    P, "target standard error 0.009218 = sqrt(p(1-p)/487) at p = 0.0432483 (out/recompute_r9.txt, '0.009218 matches: True').")

mutants = []
for line in open(f"{R}/out/mutate_graders_SC1_0-9_final.txt", encoding="utf-8"):
    m = re.match(r"^(KILLED|SURVIVED) (\S+): (.*) -> (.*)$", line.strip())
    if not m:
        continue
    status, name, desc, killed = m.groups()
    mutants.append({"name": name, "description": desc, "killed_by": None if killed.strip() == "None" else killed.strip()})

# the six SC1a lab twins are counted by the tool (note in notes); keep them listed as the tool counts them
frag = {
    "unit": "SC1",
    "slice": "d",
    "round": 9,
    "verifier": "Claude Haiku 5.5, independent verifier for SC1-d, round 9 (did not build SC1; re-verified every round-8 row against the c93dd52 pin and the 0dee921-to-c93dd52 delta)",
    "pin": "c93dd526025c6dffd34c54cd2c89eb62a890f885",
    "base": "0dee921a33dc1275ff9b1babc6c2fdf3daac62c3 (round-8 pin); delta read for the slice (project.html 4 hunks, grader/test_project.py 2 hunks, index.html:168, L01/L03/L04/L05/L06/L07/L08 prose, L05 A4(i))",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE9-SC1-d",
    "scratch": "/tmp/sc1d-r9-* (work copies; durable copies of every script and output are under ledgers/SC1/scripts/SC1-d-r9/)",
    "verified_at": "2026-11-05T05:35:42+00:00",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "Verdict FAIL with five non-PASS rows: SC1-d-ag-print-coverage and SC1-d-r9-mutants-new (leak mutants r9_01 and r9_02 survive; "
        "r9_04 is seed-dependent), SC1-d-dfn-policy (architect default: no dfn outside the closure), SC1-d-pathwise-define-before-use "
        "(term first used in L01.html:67, defined at project.html:231), SC1-d-exemplar-a-annotations (C2 and C3 annotation reasons). "
        "Round-8 FAIL rows SC1-d-spec-n41-method and SC1-d-ag-walk-listing-stall are now PASS: the n = 41 budget kills r8_07 in 1.3 s. "
        "Calibration: exemplar A scores 1,2,2,2,1 and exemplar B 4,4,4,3,4 derived blind from the rubric (out/exemplars_blind_view.txt, "
        "annotations and verdict paragraphs stripped), equal to the official lines; CAVEAT: the official verdict lines of exemplars A and B "
        "were visible in an earlier grep of project.html before scoring, so calibration is not strictly blind. "
        "Plan deviations for the architect (non-blocking, recorded as NOTE rows): tolerance 1e-10 on the page and test vs plan 1e-12; "
        "exemplar data-level labels reversed vs plan 5.4; alternatives stored under ledgers/SC1/scripts/SC1-d-r9/alternatives rather than the plan's ledgers/SC1/scripts/alternatives. "
        "Ledger hygiene: round-8 alternatives alt_r8_b and alt_r8_c hard-code the round-8 scratch path and fail at collection as stored (repathed copies used); "
        "tools/mutate_graders.py counts the six SC1a lab-twin files in ledgers/SC1/mutants as grader mutants (killed by a coverage test, not a grader check; plan 5.6/ruling 9 say lab twins are not mutation-tested). "
        "Seed dependence: r9_04 is killed on 21 of seeds 0-49, so a learner's own seed decides whether a print leak is caught. "
        "Not checked: the 1 s budget under Pyodide (only the CPython run and the in-browser reference run); the in-browser kill of r8_07; the full repository pytest suite; mypy covers tests/ and tools/ only, so the grader files are covered by ruff and the suite; seeds 0-499 not re-run this round; verify_refs for units other than SC1; the test-count claim is checked by collect-only only."
    ),
    "summary": "SC1 slice d round 9: FAIL. Rows: %d (non-PASS 5: SC1-d-ag-print-coverage, SC1-d-r9-mutants-new, SC1-d-dfn-policy, SC1-d-pathwise-define-before-use, SC1-d-exemplar-a-annotations). Mutants: 58 listed by the tool, 56 killed, 2 survived (r9_01, r9_02)." % len(rows),
}
json.dump(frag, open(OUT, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("rows", len(rows), "non-pass", sum(1 for r in rows if r["status"] != "PASS"), "mutants", len(mutants))
