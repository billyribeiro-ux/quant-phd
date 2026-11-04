"""Verifier r4: build ledgers/SC1/SC1-d.json (round 4) from the round-4 outputs. Written by the verifier."""
import json
import pathlib
import re

ROOT = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyE4-SC1-d")
OUT = ROOT / "ledgers/SC1/scripts/SC1-d-r4/out"
P = "course/modules/SC/SC1/project.html"
T = "course/modules/SC/SC1/grader/test_project.py"

R = []


def row(rid, check, location, status, evidence, fix=""):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    R.append(r)


# ---- round-3 FAILs, re-verified --------------------------------------------------------------------------------------
row("SC1-d-ladder", "2.6-ladder", f"{P}:40-49, 155, 297-300, 602-609", "PASS",
    "Re-read in round 4. Rung 1 = Lab 1 (:55-160), Rung 2 = Lab 2 (:164-210), Rung 3 = :213-265 and :299-430, Rung 4 = :608-615. Anchors ladder, rungs, spec, budget, grader-section, local, report, stretch, reading, references all exist (checked by grep). check_projects SC1 PASS (out/check_projects.txt).")
row("SC1-d-grading-mode", "2.6-grading", f"{P}:225; curriculum/03-markets.yaml (SC1 project grading: both)", "PASS",
    "Page :225 'Both the autograder and the rubric apply ... 129 tests'. curriculum/03-markets.yaml SC1 entry project.grading: both. check_projects SC1 PASS.")
row("SC1-d-spec-signatures", "2.6-spec", f"{P}:221 vs grader/starter.py:16-36", "PASS",
    "The five names and signatures on :221 (reflection_tail(a: float, t: float) -> float; discrete_max_exceedance(instance: dict, n_steps: int) -> tuple[float, float]; nested_grid_counts(instance: dict, n_fine: int, n_coarse: int) -> tuple[int, int]; srw_max_count(n: int, a: int) -> int; srw_terminal_count(n: int, a: int) -> int) equal starter.py:16, 21, 26, 31, 36.")
row("SC1-d-spec-rounding-statement", "2.2-numbers / 2.9-prose", f"{P}:223 vs :57-67, :142-160 and tests/labs/SC1/lab-SC1-project-1.py", "PASS",
    "Round-3 pass re-checked: :223 allows H and a as generated (three decimals) and a difference of computed values in exponent form to three significant digits. Lab 1 prints H = 2.083, a = 2.474 and 9.13e-15 (`{:.2e}`), which the statement allows (out/labs_check_r4.txt).")
row("SC1-d-hours", "2.6-hours", f"{P}:33, 274-280; course/modules/SC/SC1/index.html:29; index.html data-hours-lessons 72", "PASS",
    "data-hours-project=28; table 2+3+10+8+3+2 = 28 (:274-280); hub data-hours-lessons=72 (8 lessons x 9 h, index.html:152-159) + 28 = 100 = curriculum hours 100.")
row("SC1-d-spec-grid-table", "2.6-spec", f"{P}:213-265", "PASS",
    "No table is referenced by the brief or the spec. The grids 1, 4, 16, 64, 256 are listed in the brief (:438) with a standard error at each (:558 in exemplar B, :429 interpretation).")
row("SC1-d-spec-tolerance-statement", "2.6-spec", f"{P}:234; grader/test_project.py:145, 151", "PASS",
    "Closed-form tolerance 1e-10 stated at :234 and used at test_project.py:145; quadrature tolerance 1e-8 stated at :57 and used at test_project.py:151 (unchanged lines in the delta).")
row("SC1-d-ag-reference", "2.6-autograder", "course/modules/SC/SC1/grader/reference.py; tools/run_graders.py", "PASS",
    "`tools/run_graders.py --unit SC1 --seeds 0-49` -> 'run_graders SC1: PASS (reference 50/50 seeds, slowest 0.4 s)' (out/run_graders.txt). Beyond 0-49 see SC1-d-ag-draws-depend-overconstraint: the reference fails 18 of seeds 0-2999.")
row("SC1-d-ag-starter", "2.6-autograder", "course/modules/SC/SC1/grader/starter.py", "PASS",
    "starter copied as bm_checks.py with the 129-test suite, QF_SEED=0: '125 failed, 4 passed'. The 4 passing tests are instance-only (test_instance_is_labelled_and_valid x2, test_make_instance_is_deterministic, test_fifty_seeds_give_valid_instances_with_distinct_levels; `pytest -rA`). None calls the engine.")
row("SC1-d-ag-instances", "2.6-autograder", "course/modules/SC/SC1/grader/instance.py (byte-identical to round 3)", "PASS",
    "instance.py unchanged since 67a2d13e (git diff). Round-4 sweep of the reference over seeds 0-2999 (out/sweep_reference_all_failing_0_2999.txt) built every instance without error; the only failures are the draws test (SC1-d-ag-draws-depend-overconstraint). Second instance is seed + 7919 (test_project.py:37). Label SIMULATED asserted at :118.")
row("SC1-d-ag-count", "2.6-autograder", f"{T}; {P}:7, 225, 296", "PASS",
    "`pytest --collect-only -q` on a clean scratch copy with starter as bm_checks.py: '129 tests collected' (out/collect_only.txt). The page states 129 at :7, :225 and :296.")
row("SC1-d-ag-messages", "2.6-autograder", f"{T}:40-78, :109-473", "PASS",
    "Read every failure message in full. Helpers carry __tracebackhide__; no message prints an expected value. Messages echo inputs only (e.g. :431, :449). Named ValueError tests are limited to the conditions at :237. New text at :350-352 and :356-363 names the property.")
row("SC1-d-ag-overconstraint", "2.6-autograder", f"{T}:400-449; {P}:223", "PASS",
    "The n = 41 enumeration is excluded by the sentence at :223 ('a count by binomial coefficients, by the reflection identity or by a recurrence ... is allowed'). The only n = 41 test (:250) asks for srw_terminal_count(41, 1) == 2**40, which is method-agnostic.")
row("SC1-d-ag-alternatives-ok", "2.6-autograder", "ledgers/SC1/scripts/SC1-d-r4/alternatives/ (alt1-alt9)", "FAIL",
    "Run on the CURRENT suite over seeds 0-999 (out/alternatives_sweep_0_999.txt): alt1 995/1000, alt2 995/1000, alt3 995/1000, alt5 995/1000, alt6 995/1000, alt7 992/1000 (failing seeds include 88, 123, 146; all fail test_draws_depend_on_the_instance_seed). alt4 (Box-Muller, not gauss) fails 956/1000 and is non-conforming (project.html:232 names gauss). With the candidate fix (draws test patched in a scratch copy, out/alternatives_sweep_patched_0_999.txt; out/alt8_alt9_patched_0_999.txt) alt1, alt2, alt3, alt5, alt6, alt7, alt8 (1 - erf tail), alt9 (closed-form SE) all pass 1000/1000. alt2b (enumeration) is excluded: it cannot finish the n = 41 test.",
    "Fix SC1-d-ag-draws-depend-overconstraint; then re-run the sweep over seeds 0-2999 for alt1-alt3, alt5-alt9.")
row("SC1-d-ag-mutants-plan", "2.6-mutation", "ledgers/SC1/mutants/m01-m10", "PASS",
    "tools/mutate_graders.py --unit SC1 -> 'mutate_graders SC1: PASS (31/31 killed)' (out/mutate_graders_r4.txt); m01-m10 each KILLED on seed 0 or seed 1.")
row("SC1-d-ag-mutants-own", "2.6-mutation", "ledgers/SC1/mutants/m11-m15, m18, m19, m21", "PASS",
    "All KILLED in out/mutate_graders_r4.txt (m11 seed 1, m15 seed 0, m18 seed 1, m19 seed 0, m21 seed 0).")
row("SC1-d-ag-mutants-survivors", "2.6-mutation", f"{T}:418-425; ledgers/SC1/mutants/m16, m17", "PASS",
    "m16 KILLED by test_fine_grid_of_zero_steps_raises_value_error (seed 0); m17 KILLED by test_coarse_grid_of_zero_steps_raises_value_error (seed 0).")
row("SC1-d-ag-mutants-seed", "2.6-mutation", f"ledgers/SC1/mutants/m20; {T}:356-363", "PASS",
    "m20 (Random(0) for every instance) KILLED by test_draws_depend_on_the_instance_seed (seed 0). With the candidate fix m20 still fails 4 of 4 seeds checked (scratch /tmp/sc1d_r4_mut).")
row("SC1-d-ag-mutants-seed-offset", "2.6-mutation", "ledgers/SC1/mutants/m22_seed_offset_by_one.py; project.html:232; test_project.py:332-336", "PASS",
    "Round-3 FAIL resolved. m22 (Random(seed + 1)) is now KILLED deterministically by test_one_step_draws_are_the_seeded_gaussians (seed 0): the test requires discrete_max_exceedance(INST, 1)[0] == hits / N for the draws of random.Random(INST['seed']).gauss(0, sqrt(H)). The mutant fails it on seeds 0-3 (scratch, patched suite too). The round-3 kill by a zero-hit fluke is no longer the reason.")
row("SC1-d-ag-mutants-r3", "2.6-mutation", "ledgers/SC1/mutants/m23-m26", "PASS",
    "m23-m26 KILLED (out/mutate_graders_r4.txt): m23 by test_srw_counts_match_enumeration_for_n_up_to_12[1], m24 by test_standard_error_uses_divisor_n_minus_one (seed 0), m25 by test_one_step_coarse_grid_tracks_the_terminal_law (seed 1), m26 by test_srw_counts_match_enumeration_for_n_up_to_12[1].")
row("SC1-d-ag-mutants-r4-new", "2.6-mutation", "ledgers/SC1/mutants/m27-m31", "PASS",
    "Five new student-error mutants written by the verifier as single-change copies of grader/reference.py (ledgers/SC1/scripts/SC1-d-r4/make_mutants_r4.py): m27 coarse grid starts at the first step (values[0::stride]) KILLED by test_one_step_coarse_grid_tracks_the_terminal_law (seed 1); m28 RNG reseeded per path KILLED by test_one_step_estimate_matches_the_one_step_law_for_second_seed (seed 0); m29 srw_terminal_count drops the all-up walk (range(n)) KILLED by test_srw_counts_match_enumeration_for_n_up_to_12[1] (seed 0); m30 identity shifted down (a - 1) KILLED by test_srw_reflection_identity_holds_exactly[4] (seed 0); m31 coarse count on fresh paths KILLED by test_coarse_count_never_exceeds_the_fine_count[8-4] (seed 8).")
row("SC1-d-ag-page-smoke", "2.6-autograder", f"{P}; tools/page_smoke.py", "PASS",
    "`tools/page_smoke.py --unit SC1 --pages project.html` -> 'page_smoke SC1: PASS', exit 0 (out/page_smoke_project.txt). Pyodide run of the page; UI behaviour beyond that is not checked (see notes).")
row("SC1-d-ag-docstring", "2.6-autograder", f"{T}:1-18 vs tests :217-220, :309-315, :318-324, :328-335, :339-342, :385-388, :396-405", "PASS",
    "Docstring claims re-read: 'one test calls discrete_max_exceedance twice' (:350-353), 'one test pins the one-step draws to random.Random(seed).gauss' (:332-336), 'the band takes the target's standard error' (:82, :318, :327, :345, :423), 'never prints the expected value' (messages read in full). All hold.")
row("SC1-d-rubric-observable", "2.9-prose", f"{P}:446-457", "PASS",
    "Each cell describes a checkable element (named assumptions, named justifications, rounding statements, standard errors, grid list, partition of paths). Level 1 cells name an absence. No cell requires an unobservable judgment.")
row("SC1-d-calib-A", "2.9-prose / 2.2-numbers", f"{P}:464-516 (exemplar A)", "FAIL",
    "Calibration scores disagree with the rubric for C1. The official scoring at :466 and data-scores at :464 give C1 = 2. Exemplar A lists no numbered assumptions for any result (grep 'assum' in :464-516 finds only the annotations at :487 and :500, which say A3 and P1's assumptions are missing). The C1 level-2 cell (:452) requires listed assumptions of two results. The C1 level-1 cell ('No numbered assumptions') therefore holds. The other exemplar A numbers (0.0595, 0.0107, 1.52, 0.004361, -0.001799) match out/recompute_r4.txt.",
    "Set C1 to 1 in exemplar A: data-scores at :464 to '1,2,2,2,1' and the verdict at :466 to 'C1 1'; the annotation at :487 may stay. Or add numbered assumptions for two results to exemplar A so that level 2 is met.")
row("SC1-d-exemplarA-claim", "2.9-prose", f"{P}:470, 474-475, 482, 499, 503-508, 512", "PASS",
    "Claims re-checked against out/recompute_r4.txt: 'about 0.0865' (0.086497), '0.0595 ... standard error of 0.0107' (0.059548, 0.010735), '0.0163 above half the tail (0.0432)' (0.016300 above 0.043248), '1.52 printed standard errors (0.0163 / 0.0107)' = 1.523, 0.004361 at 256 steps and -0.001799 at 64 steps (lab output).")
row("SC1-d-exemplarB-onestep-claim", "2.9-prose / 2.2-numbers", f"{P}:558", "PASS",
    "Round-3 FAIL resolved. :558 now says: 'The one-step bias is tail/2 = 0.043248, so the printed figure 0.026948 estimates it with sampling error -0.016300, which is 1.52 standard errors.' Recomputed: tail - p = 0.026948406 (prints 0.026948); p - tail/2 = 0.016299924 (prints 0.016300); 0.0163/0.010735 = 1.518 (prints 1.52) (out/recompute_r4.txt).")
row("SC1-d-exemplarB-proof", "2.9-prose / 2.4-proof", f"{P}:583-590 (exemplar B appendix)", "FAIL",
    "P1 and P2 proofs re-derived line by line. Maths is correct: the decomposition A = {tau <= t}, P(tau = t) = 0, the freezing step with Z = (t - rho, A) and Y the restarted path, and P(A) = P(B_t >= a) + P(A)/2 all check. P2's erfc substitution is correct. The gap is in the justification, not the algebra: the step 'A and t - rho are F_rho-measurable' (:584) names no assumption, and A4(h) (L05 :A4(h)) gives only the measurability of rho and B_rho, not of A = {tau <= t}. The freezing step also applies A4(b) to the path B~ at the random time t - rho, which uses joint measurability (A4(g)), which P1's list does not name (:246). The rubric's C2 level-4 cell requires each step to name its justification, so the exemplar's level-4 C2 claim at :595 ('no step is skipped') is not met.",
    "Either name the justification of A in F_rho (A4(c) for tau, and the definition of F_rho in L05 Section 3) and add A4(g) to the assumption list of P1 (:246 and the statement at :249, and :583), or score exemplar B C2 at 3 and remove 'no step is skipped' from the annotation at :595.")
row("SC1-d-exemplarB-numbers", "2.2-numbers", f"{P}:524, 546, 558 vs lab output at :154-160 and :418-428", "PASS",
    "Every Exemplar B number is a printed Lab 1 or Lab 3 value (0.086497; 9.13e-15 -> 'within 10 to the minus 14'; 0.059548; 0.010735; 0.043248; 0.048142; 0.016300; 1588; 794; 35, 29, 27, 22; 40). Re-derived in out/recompute_r4.txt.")
row("SC1-d-lab1-run", "2.5-labs", f"{P}:55-160; tests/labs/SC1/lab-SC1-project-1.py", "PASS",
    "run_labs SC1: PASS (11/11); twin run under `python -I -W error`: exit 0, empty stderr; output equals the expected block (out/labs_check_r4.txt, out/run_labs.txt). Page code block equals the twin (only a trailing newline differs).")
row("SC1-d-lab1-docstring", "2.5-labs / 2.9-prose", f"{P}:58-68; tests/labs/SC1/lab-SC1-project-1.py:3-8", "PASS",
    "Docstring re-read: 'draws the same four numbers in the same order' (make_instance matches instance.py:23-27); 'rounded to six decimal places ... except the Simpson difference, in exponent form to three significant digits' (lines 146-149 use :.6f, :.2e); 'N is an integer' (line 144).")
row("SC1-d-lab2-run", "2.5-labs", f"{P}:164-210; tests/labs/SC1/lab-SC1-project-2.py", "PASS",
    "Page code has the two blanks (___) and the twin has the completed lines; with blanks filled the twin's output equals the expected block (29 / 22 / 7 / True) under python -I -W error (out/labs_check_r4.txt). Page and twin differ only in the two blank lines, as a completion problem requires.")
row("SC1-d-lab2-attribution", "2.9-prose / attribution", f"{P}:209 vs course/modules/SC/SC1/L06.html (Proposition 1.3, Corollary 1.4)", "PASS",
    "L06.html Proposition 1.3 (discrete reflection identity) and Corollary 1.4 (#{M_N>=a} = #{S_N>=a} + #{S_N>a}) match the Lab 2 identity: 22 + 7 = 29 for n = 6, a = 2 (recomputed, out/recompute_r4.txt: walk(6,2) = (29, 22); walk(6,3) end = 7).")
row("SC1-d-lab3-run", "2.5-labs", f"{P}:303-430; tests/labs/SC1/lab-SC1-project-3.py", "PASS",
    "Twin run under python -I -W error: exit 0, output equals the expected block line for line (out/labs_check_r4.txt). Recomputed independently in out/recompute_r4.txt: hits 29, 24, 32, 43, 40; estimates; SEs; tail-minus-estimate; nested 35/29/27/22; walks 1588/794.")
row("SC1-d-lab3-onestep-interp", "2.5-labs / 2.9-prose", f"{P}:429 vs tests/labs/SC1/lab-SC1-project-3.py:99", "PASS",
    "Round-3 FAIL resolved. The interpretation at :429 now says the one-step row prints tail minus estimate and its target is half the tail, which matches lab line 99 (tail - p for every grid, including n = 1) and the printed 'grid n = 1 ... tail minus estimate 0.026948'.")
row("SC1-d-lab3-docstring", "2.5-labs / 2.9-prose", "tests/labs/SC1/lab-SC1-project-3.py:3-11 (page :306-317)", "PASS",
    "Docstring read in full: 'drawn in the same fixed order' (make_instance matches), 'path by path and step by step from random.Random(seed)' (path_maxima :359-366), 'the sample standard deviation of the 0/1 indicators (divisor N - 1) divided by sqrt(N)' (estimate_and_se :375-379), 'every (256 / n)-th point' (:409), 'rounded to six decimal places' (format :.6f).")
row("SC1-d-labs-pytest", "2.5-labs / tooling", "tests/test_labs.py -k SC1; tests/test_run_labs.py; tests/test_page_checks.py; tests/test_memo_exemplars.py", "PASS",
    "`pytest -k SC1` over those four files: exit 0, 11 passed (out/pytest_relevant.txt). Lab twins are demonstrations; the lab-SC1-project-2 blanks are the completion design.")
row("SC1-d-calib-B", "2.9-prose / rubric scoring", f"{P}:518-599 (exemplar B)", "FAIL",
    "Exemplar B's official scoring (:520, data-scores :518) gives C2 = 4 and its annotation at :595 says 'no step is skipped'. The P1 appendix proof (:584) has steps whose justification is not named and whose hypotheses are not on the P1 list (see SC1-d-exemplarB-p1-assumptions). C2 level 4 ('each step names the assumption ... and every skipped step is named as a gap') is therefore not met as written. The other exemplar B scores (C1 4, C3 4, C4 3, C5 4) match the annotations and the numbers (SC1-d-exemplarB-numbers).",
    "Either name the justification of A in F_rho and add A4(g) to P1's list (see the P1 row), so that C2 level 4 holds, or set exemplar B C2 to 3 (data-scores :518 to '4,4,3,3,4', verdict :520 'C2 3') and remove 'no step is skipped' from the annotation at :595.")
row("SC1-d-statements", "2.6-statements", f"{P}:241-262", "PASS",
    "P1, P2, P3 statements re-read. Hypotheses now stated (a > 0, t > 0; P2 assumes P1 and the normal law; P3 first part uses continuity, second part uses P2). P2's 'this equals 2(1 - Phi(a/sqrt t))' checked by the substitution in exemplar B :587 and by erfc(x) = 2(1 - Phi(x sqrt 2)). The gap in P1's assumption list is recorded under SC1-d-exemplarB-p1-assumptions.")
row("SC1-d-exemplarB-p1-assumptions", "2.9-prose / 2.4-proof (hypotheses)", f"{P}:246, 249, 583-584", "FAIL",
    "The P1 statement lists A0, A3, A4(b), A4(c), A4(h) (:246, :249). The proof (exemplar B :584, the official calibration proof) needs two facts not on that list: (i) that A = {tau <= t} is F_rho-measurable, since A4(h) covers only rho and B_rho (L05 A4(h), :A4 list); (ii) joint measurability of the restarted path (A4(g), L05), which is needed to apply A4(b) to f(z, y) = 1{y(z_1) < 0} with Y the path. The page's own rule (:262) says a step using an assumption not listed must name it. A P1 whose statement omits those hypotheses is not graded T as written.",
    "Add A4(g) to the P1 assumption list (:246, :249, :583), and state A in F_rho with its justification (A4(c) and the definition of F_rho in L05 Section 3), or name the step as a stated gap.")
row("SC1-d-A1-label", "2.6-labels", f"{P}:236-242, 577-580; course/modules/SC/SC1/L01.html:58-63; L05.html", "PASS",
    "Definition 1.1 of Lesson 1 is (D1) B_0 = 0, (D2) normal increments with variance t - s, (D3) independent increments (L01.html:58-63), as P1-P2 cite. A3 is the strong Markov property for a bounded stopping time (L05 :270), A4 items (a)-(h) are listed at L05 (A4 list). The label 'A3 and A4 are Assumptions 3 and 4 of Lesson 5' matches.")
row("SC1-d-A3-A4-usage", "2.6-labels", f"{P}:242, 246, 249; course/modules/SC/SC1/L05.html (A3, A4 list)", "PASS",
    "Each cited part exists: A4(b) freezing (L05 :A4 list (b)), A4(c) hitting times (c), A4(h) measurability at a stopping time (h). A3 is stated only for bounded stopping times (L05 :278), which matches P1's bounded rho = tau_a wedge t.")
row("SC1-d-dag", "2.7-dag", f"{P}; tools/check_dag.py --unit SC1", "PASS",
    "`tools/check_dag.py --unit SC1` -> 'check_dag SC1: PASS' (out/check_dag.txt). Concept links stopping-time (concepts.html#stopping-time, present) and normal-distribution (present) resolve.")
row("SC1-d-notation", "2.8-notation", f"{P} passim; notation/notation.json", "PASS",
    "Macros used on the page: Normal and Prob (registered, notation.json macros), Phi (registered symbol '\\Phi, \\Phi^{-1}': standard normal CDF, same meaning here at :230). The horizon is H, not the registered T (T = number of return observations, S1), and the page says so (:230). N is a local letter (registry comment: N conventionally local) and means the path count throughout. No registered symbol is reused.")
row("SC1-d-define-before-use", "2.9-prose", f"{P}:37, 45, 53, 57", "PASS",
    "Running maximum and grid maximum defined at :37 and :53 before use; the level a and horizon H defined at :53 and :57; the one-step estimate defined at :57. Conventions (B, M_t, tau_a, H, Phi, erfc) at :230 precede the statements at :241.")
row("SC1-d-discretization-bias", "2.2-numbers / 2.9-prose", f"{P}:235, 225, 229", "PASS",
    "The discretization bias is defined as continuous tail minus grid probability (:235); its estimate is tail minus grid estimate; the sign statement ('can be negative through sampling noise, as Lab 3 shows at 64 steps') matches -0.001799 (lab output).")
row("SC1-d-monte-carlo-term", "2.9-prose", f"{P}", "PASS",
    "Terms estimate, standard error, path and sample are defined on the page before use (the grid maximum and the estimate at :231-232, :235; the standard error at :232) and in the Lab 3 code block (estimate_and_se, lines 375-379 of the page code, equal to the twin). No undefined Monte Carlo term is used.")
row("SC1-d-scope-words", "2.9-prose", f"{P}:223, 231-238, 449, 575 (scope words, passim)", "PASS",
    "Scope words (every, all, always, only, any, same, exactly) re-read in full. Each universal claim is either computed by the lab (every grid row, 'coarse at most fine on these paths') or follows from a stated hypothesis (every grid point lies in [0, H], so the grid maximum never exceeds M_H on the same path; P1-P3 for every case meeting their listed assumptions). No universal claim about the continuum is made without a hypothesis.")
row("SC1-d-process-words", "2.9-prose", f"{P}:619", "FAIL",
    "Learner text uses internal build vocabulary: 'The curriculum names two sources for this unit. One has a registry record ... The other has no registry record, so this page does not cite it.' 'Curriculum' and 'registry record' are process words that a learner reading the Reading section does not need. (The workspace-ID phrase at :219 is the autograder panel's own term and is not counted.)",
    "Rewrite :619-622 as: 'The reading for this unit is Shreve, Stochastic Calculus for Finance II (2004), cited at book level, with no passage or theorem number.' Remove the second source sentence or state it without build vocabulary.")
row("SC1-d-banned-structure", "2.6-structure", f"{P}; tools/check_pages.py --unit SC1", "PASS",
    "`tools/check_pages.py --unit SC1` -> 'check_pages SC1: PASS' (out/check_pages.txt).")
row("SC1-d-registry", "2.3-registry", f"{P}:619-622; references/references.json:20732", "PASS",
    "Key shreve2004stochastic exists at references/references.json:20732 (the page cites it at book level only, with no passage). verify_refs --offline: 'offline integrity: 560 entries, 0 problems' (out/verify_refs_offline.txt).")
row("SC1-d-privacy-claim", "2.9-prose / product claim", f"{P}:288, 603, 636", "PASS",
    "Claims 'Your code is saved in this browser shortly after you stop typing' and 'Your scores stay in this browser' are supported by course/assets/js/grader.js:61 (store.put of the draft after a 400 ms debounce) and rubric.js:8-9 and store.js:4 ('Nothing leaves the browser'). Not checked: the live storage behaviour in a browser (see notes).")
row("SC1-d-tools-gates", "2.6-gates", "ruff, mypy, pytest relevant, verify_refs", "PASS",
    "ruff check + ruff format --check on course/modules/SC/SC1/grader and tests/labs/SC1: 'All checks passed', 15 files formatted (out/ruff_slice.txt; ruff reports on my own scratch scripts under ledgers/SC1/scripts/SC1-d-r4 are not gate files). mypy --no-incremental: 'Success: no issues found in 385 source files' (out/mypy.txt). pytest -k SC1 (4 files): 11 passed (out/pytest_relevant.txt). verify_refs --offline: 0 problems.")
row("SC1-d-numbers-prose", "2.2-numbers", f"{P}:57, 154-160, 209, 219, 225, 305-317, 418-429, 470-512, 524-558", "PASS",
    "Every prose number re-derived from unrounded values in ledgers/SC1/scripts/SC1-d-r4/recompute_r4.py (out/recompute_r4.txt): tail 0.086497; SE 0.010735; target 0.043248; target SE 0.009218; band 0.048142; differences 0.016300 and 0.026948; grid estimates and SEs; nested counts; walk counts 1588/794; 0.14 SE for the 64-step row (0.001799/0.012870 = 0.140).")
row("SC1-d-spec-n41-method", "2.6-spec", f"{P}:223; grader/reference.py:79-85; ledgers/SC1/scripts/SC1-d-r4/alternatives/alt7_gauss_step_major.py", "PASS",
    "Round-3 FAIL resolved. :223 now allows 'a count by binomial coefficients, by the reflection identity or by a recurrence'. The reference's srw_terminal_count (binomial sum) is covered. alt7 (same binomial count) passes 1000/1000 on the patched suite. The unchanged n = 41 test (:250) is method-agnostic.")
row("SC1-d-ag-draws-depend-overconstraint", "2.6-autograder (over-constraint)", f"{T}:356-363 (test_draws_depend_on_the_instance_seed)", "FAIL",
    "The reference solution fails 18 of seeds 0-2999 (out/sweep_reference_all_failing_0_2999.txt; seeds 88, 123, 146, 440, 939, 1394, 1489, 1638, 1692, 1694, 1896, 2200, 2236, 2242, 2249, 2315, 2716, 2884), always in this test. Cause: the test builds other = with_(INST, seed + 7919), which keeps INST's horizon, level a and path count, and then requires some grid in {4, 8, 16, 32, 64} to give a different (estimate, se) for INST and other. For these seeds the level is far in the tail, so no path reaches it at any grid for either seed: seed 88 has H = 0.388, a = 2.435, N = 561, tail 9.26e-05, and both estimates are 0.0 at all five grids (checked with the reference, scratch /tmp/sc1d_r4_s88). Seeds 123 (tail 2.1e-05), 146 (2.7e-04), 440 (1.5e-04) behave the same. A correct engine therefore fails for a learner whose workspace seed is one of these, and the test does not test the seed. Mutants m20, m22 and m28 are still killed on the patched suite.",
    "In test_project.py:356-363 use a level where hits are nonzero: other = with_(INST, seed=INST['seed'] + 7_919, a=1e-9) and compare discrete_max_exceedance(with_(INST, a=1e-9), g) with discrete_max_exceedance(other, g). Candidate diff: ledgers/SC1/scripts/SC1-d-r4/draws_test_fix_candidate_r4.diff. Verified on a scratch copy: reference 3000/3000 seeds, alt1-3, alt5-9 1000/1000, m20/m22/m28 still killed. Re-run the 3000-seed sweep and the mutation tool after applying.")
row("SC1-d-ag-band-overconstraint", "2.6-autograder", f"{T}:76-82, 314-329, 418-425", "PASS",
    "Round-3 FAIL resolved. The band now uses the target's standard error (simulation_band(target, N) at :82, used at :318, :327, :423). The reference passes the round-3 failing seeds 252, 686, 1012, 54, 156, 633, 2569 (in the 0-2999 sweep, which lists only the draws-test failures).")

# ---- mutants and counts ----------------------------------------------------------------------------------------------
mutants = []
for line in (OUT / "mutate_graders_r4.txt").read_text(encoding="utf-8").splitlines():
    m = re.match(r"KILLED (\S+\.py): (.*) -> (.*)$", line)
    if not m:
        continue
    fname, desc, killed = m.groups()
    mid = fname[:-3]
    mutants.append({"id": mid, "name": mid, "description": desc, "killed_by": killed,
                    "file": f"ledgers/SC1/mutants/{fname}"})

counts = {}
for r in R:
    counts[r["status"]] = counts.get(r["status"], 0) + 1
fragment = {
    "unit": "SC1",
    "slice": "d",
    "round": 4,
    "verifier": "Claude Haiku 5.5, independent verifier (slice d, round 4)",
    "pin": "9a02b1af",
    "base": "1c1645f3",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE4-SC1-d",
    "scratch": "/tmp/sc1d_r4_collect, /tmp/sc1d_r4_s88, /tmp/sc1d_r4_patched, /tmp/sc1d_r4_mut",
    "verified_at": "2026-11-04T14:55:47+00:00",
    "verdict": "PASS" if counts.get("FAIL", 0) == 0 and counts.get("UNVERIFIABLE", 0) == 0 else "FAIL",
    "rows": R,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "Delta 67a2d13e -> 9a02b1af read in full: project.html (all hunks), grader/test_project.py (all), tests/labs/SC1/lab-SC1-project-1.py, "
        "ledgers/SC1/mutants/m22-m26, L01/L05/L06 hunks that the slice cites. grader/reference.py, instance.py, starter.py byte-identical to the round-3 pin and re-run. "
        "Could not check: in-browser UI of the grader panel, the self-assessment form and the storage behaviour beyond page_smoke's Pyodide run and the code; "
        "exemplar scoring is not blind (annotations read in the same pass); the 240-second hang of an enumeration solution at n = 41 (the suite has no per-test timeout; "
        "the panel's own timeout was not measured); the other slices (lessons, cards, hub); the Pyodide timing of 129 tests beyond page_smoke; "
        "seeds beyond 2999 for the draws test (the 18 failures in 0-2999 indicate a rate of about 0.6 per cent, so more seeds would fail); "
        "alt4 (Box-Muller) is non-conforming by the page's gauss statement, so its failures are not counted; alt2b (enumeration) is excluded because it cannot finish the n = 41 test in the browser."
    ),
    "summary": (
        f"SC1 slice d round 4 (project.html, grader, project labs, mutants, alternatives): FAIL. Rows: {len(R)} "
        f"({counts.get('PASS', 0)} PASS, {counts.get('FAIL', 0)} FAIL, {counts.get('UNVERIFIABLE', 0)} UNVERIFIABLE). "
        f"Mutants: {len(mutants)} in ledgers/SC1/mutants, all KILLED (31/31; m27-m31 new). "
        "Round-3 FAILs resolved: seed-offset, one-step claim, lab3 interpretation, band over-constraint, n=41 method. "
        "New FAILs: the draws-test over-constraint (18 of 3000 seeds), exemplar A C1 score, exemplar B P1 hypotheses and proof justification, and one process-word sentence. "
        "Alternatives 1-3, 5-9 pass 1000/1000 seeds once the draws test is fixed (candidate diff saved)."
    ),
}
out = ROOT / "ledgers/SC1/SC1-d.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(fragment, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("rows", len(R), counts, "mutants", len(mutants), "verdict", fragment["verdict"])
