"""Verifier r5 (SC1-d): build ledgers/SC1/SC1-d.json from the commands and outputs recorded under SC1-d-r5/out/."""
import json, re, datetime
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyE5-SC1-d")
S = "ledgers/SC1/scripts/SC1-d-r5"
OUT = ROOT / S / "out"
CARRY = "Carried from round 4 (%s byte-identical since the previous pin):"
PIN = "9a02b1af"

def fresh(i, check, location, evidence):
    return {"id": i, "check": check, "location": location, "status": "PASS", "evidence": evidence}

def carry(i, check, location, files, evidence):
    return {"id": i, "check": check, "location": location, "status": "PASS",
            "evidence": (CARRY % files) + " " + evidence}

rows = [
 carry("SC1-d-ladder", "2.6-ladder", "course/modules/SC/SC1/project.html:40-49, 155, 297-300, 602-609",
       "project.html lines 40-49, 155, 297-300, 602-609 (no hunk of the 9a02b1af..7376a5e delta touches them)",
       "Anchors and rung structure re-read; check_projects SC1 PASS (out in gates1.txt)."),
 carry("SC1-d-grading-mode", "2.6-grading", "course/modules/SC/SC1/project.html:225; curriculum/03-markets.yaml SC1 grading: both",
       "project.html:225 and curriculum/03-markets.yaml (curriculum/ unchanged in the delta)",
       "Page :225 still says 'Both the autograder and the rubric apply ... 129 tests'; collect-only gives 129 (see SC1-d-ag-count)."),
 carry("SC1-d-spec-signatures", "2.6-spec", "course/modules/SC/SC1/project.html:221 vs grader/starter.py:16-36",
       "project.html:221 and grader/starter.py (starter.py unchanged in the delta)",
       "The five signatures on :221 equal starter.py:16, 21, 26, 31, 36."),
 carry("SC1-d-spec-rounding-statement", "2.2-numbers / 2.9-prose", "course/modules/SC/SC1/project.html:223 vs :57-67, :142-160 and tests/labs/SC1/lab-SC1-project-1.py",
       "project.html:223 and the Lab 1 code and expected block (lines 57-67, 142-160; twin unchanged)",
       "Lab 1 prints H = 2.083, a = 2.474 and 9.13e-15 (`{:.2e}`), which :223 allows; labs_check_r5 output equal to the expected block."),
 carry("SC1-d-hours", "2.6-hours", "course/modules/SC/SC1/project.html:33, 274-280; course/modules/SC/SC1/index.html:29; index.html data-hours-lessons 72",
       "project.html:33, 274-280 (the hours table is unchanged); index.html only changed at its reading paragraph (hunk at :183)",
       "Eight L0n.html carry data-hours=9 (grep), so 72 lesson hours; 72 + data-hours-project 28 = 100 = curriculum hours 100 (curriculum/03-markets.yaml:508). Table 2+3+10+8+3+2 = 28."),
 fresh("SC1-d-spec-grid-table", "2.6-spec", "course/modules/SC/SC1/project.html:213-265, 433-445",
       "grep -i table on :213-265 and :433-445 returns no match (`awk`/`grep` run this round). The grids 1, 4, 16, 64, 256 are listed at :438."),
 carry("SC1-d-spec-tolerance-statement", "2.6-spec", "course/modules/SC/SC1/project.html:234; grader/test_project.py:145, 151",
       "project.html:234 and test_project.py:145, 151 (the delta's test hunk is at :356-365)",
       "Closed-form tolerance 1e-10 at :234 is used at test_project.py:145; the 1e-8 quadrature tolerance (:57) at :151."),
 fresh("SC1-d-ag-reference", "2.6-autograder", "course/modules/SC/SC1/grader/reference.py; tools/run_graders.py",
       "tools/run_graders.py --unit SC1 --seeds 0-49 -> 'run_graders SC1: PASS (reference 50/50 seeds, slowest 0.7 s)' (gates1.txt). Seeds 0-2999 with the current suite: ledgers/SC1/scripts/SC1-d-r5/out/sweep_reference_0_2999.txt = '3000/3000 seeds pass; failing: 0'."),
 fresh("SC1-d-ag-starter", "2.6-autograder", "course/modules/SC/SC1/grader/starter.py",
       "starter copied as bm_checks.py, QF_SEED=0, current suite: '125 failed, 4 passed'. pytest -rA: PASSED test_instance_is_labelled_and_valid[student seed], [second seed], test_make_instance_is_deterministic, test_fifty_seeds_give_valid_instances_with_distinct_levels (none calls the engine)."),
 carry("SC1-d-ag-instances", "2.6-autograder", "course/modules/SC/SC1/grader/instance.py",
       "grader/instance.py (no hunk in the delta)",
       "Round-5 sweep of the reference over seeds 0-2999 built every instance (3000/3000 pass); label SIMULATED asserted at test_project.py:118."),
 fresh("SC1-d-ag-count", "2.6-autograder", "course/modules/SC/SC1/grader/test_project.py; course/modules/SC/SC1/project.html:7, 225, 296",
       "Clean scratch copy (test_project.py, instance.py, reference.py as bm_checks.py): `pytest --collect-only -q` -> '129 tests collected'. Page states 129 at :7, :225 and :296. QF_SEED=0 run of reference: '129 passed'."),
 fresh("SC1-d-ag-messages", "2.6-autograder", "course/modules/SC/SC1/grader/test_project.py:1-474",
       "Whole file re-read this round, including the changed draws test (:356-365). Failure messages echo inputs or name the property only; the new message at :362-364 holds no value. Named ValueError tests (:373-455) cover only the conditions at project.html:237."),
 fresh("SC1-d-ag-overconstraint", "2.6-autograder", "course/modules/SC/SC1/grader/test_project.py:400-449, 249-250; course/modules/SC/SC1/project.html:223",
       "The n = 41 test (:249-250) asks only srw_terminal_count(41, 1) == 2**40, which any method in :223 gives; no test lists the 2^41 walks. alt3 (DP) and alt7 pass the n = 41 test on seeds 0-999 (alternatives sweep)."),
 fresh("SC1-d-ag-alternatives-ok", "2.6-autograder", "ledgers/SC1/scripts/SC1-d-r5/alternatives/ (alt1, alt2, alt3, alt5, alt6, alt7, alt8, alt9)",
       "Current suite (fixed draws test), seeds 0-999, tools in sweep_r5.py: alt1 1000/1000, alt2 1000/1000, alt3 1000/1000, alt5 1000/1000, alt6 1000/1000, alt7 (step-major gauss order) 1000/1000, alt8 (1 - erf tail) 1000/1000, alt9 (closed-form SE) 1000/1000 (out/alternatives_sweep_0_999.txt). Excluded and why: alt2b enumerates the n = 41 walks, which project.html:223 forbids; alt4 (Box-Muller, not gauss) is non-conforming with project.html:232, which names gauss."),
 fresh("SC1-d-ag-mutants-plan", "2.6-mutation", "ledgers/SC1/mutants/m01-m10",
       "tools/mutate_graders.py --unit SC1 --seeds 0-9 -> 'mutate_graders SC1: PASS (34/34 killed)' (out/mutate_graders_r5.txt); m01-m10 KILLED."),
 fresh("SC1-d-ag-mutants-own", "2.6-mutation", "ledgers/SC1/mutants/m11-m15, m18, m19, m21",
       "All KILLED in out/mutate_graders_r5.txt (m11 seed 1, m15 seed 0, m18 seed 1, m19 seed 0, m21 seed 0)."),
 fresh("SC1-d-ag-mutants-survivors", "2.6-mutation", "course/modules/SC/SC1/grader/test_project.py:440-455; ledgers/SC1/mutants/m16, m17",
       "m16 KILLED by test_fine_grid_of_zero_steps_raises_value_error (seed 0); m17 KILLED by test_coarse_grid_of_zero_steps_raises_value_error (seed 0)."),
 fresh("SC1-d-ag-mutants-seed", "2.6-mutation", "ledgers/SC1/mutants/m20; course/modules/SC/SC1/grader/test_project.py:356-365",
       "m20 KILLED by test_draws_depend_on_the_instance_seed (seed 0) with the new level a = 1e-9 (out/mutate_graders_r5.txt)."),
 fresh("SC1-d-ag-mutants-seed-offset", "2.6-mutation", "ledgers/SC1/mutants/m22_seed_offset_by_one.py; project.html:232; test_project.py:332-336",
       "m22 KILLED by test_one_step_draws_are_the_seeded_gaussians (seed 0), not by a zero-hit fluke."),
 fresh("SC1-d-ag-mutants-r3", "2.6-mutation", "ledgers/SC1/mutants/m23-m26",
       "m23 and m26 by test_srw_counts_match_enumeration_for_n_up_to_12[1] (seed 0); m24 by test_standard_error_uses_divisor_n_minus_one (seed 0); m25 by test_one_step_coarse_grid_tracks_the_terminal_law (seed 1)."),
 fresh("SC1-d-ag-mutants-r4-new", "2.6-mutation", "ledgers/SC1/mutants/m27-m31",
       "m27 KILLED (seed 1), m28 KILLED (seed 0), m29 KILLED (seed 0), m30 KILLED (seed 0), m31 KILLED (seed 8); out/mutate_graders_r5.txt."),
 fresh("SC1-d-ag-mutants-r5-new", "2.6-mutation", "ledgers/SC1/mutants/m32, m33, m34 (written this round by ledgers/SC1/scripts/SC1-d-r5/make_mutants_r5.py)",
       "m32 coarse stride = n_coarse KILLED by test_equal_grids_give_equal_counts (seed 0); m33 srw_max = 2 * terminal KILLED by test_srw_counts_match_enumeration_for_n_up_to_12[1] (seed 0); m34 step sd = sqrt(H)/n KILLED by test_one_step_coarse_grid_tracks_the_terminal_law (seed 1). Each a single-change copy of reference.py; ast.parse OK. m32 duplicates m21 in effect (both take every n_coarse-th point)."),
 fresh("SC1-d-ag-page-smoke", "2.6-autograder", "course/modules/SC/SC1/project.html; tools/page_smoke.py",
       "`tools/page_smoke.py --unit SC1 --pages project` -> 'page_smoke modules/SC/SC1/project.html: PASS', 'in-browser grader: All 129 tests pass' (out/page_smoke_project_r5.txt, exit 0)."),
 fresh("SC1-d-ag-docstring", "2.6-autograder", "course/modules/SC/SC1/grader/test_project.py:1-18 vs the tests it describes",
       "Module docstring claims re-read against tests: 'one test calls discrete_max_exceedance twice' (:350-353), 'one test pins the one-step draws to random.Random(seed).gauss' (:332-336), 'the band takes the target's standard error' (:79-82, :314-329, :418-425), 'never prints the expected value' (messages read). All hold."),
 fresh("SC1-d-rubric-observable", "2.9-prose", "course/modules/SC/SC1/project.html:446-457",
       "Rubric cells re-read (unchanged in the delta). Each cell names a checkable element; level-1 cells name an absence."),
 fresh("SC1-d-calib-A", "2.9-prose / 2.2-numbers", "course/modules/SC/SC1/project.html:464-466, 470-516 (exemplar A)",
       "Round-4 FAIL resolved. The delta sets data-scores to 1,2,2,2,1 (:464) and the verdict to 'C1 1' (:466). Exemplar A has no numbered assumptions for any result (checked by reading :468-515: summary, checks, P1 appendix, discretization). The rubric's C1 level-2 cell needs the assumptions of two results, so C1 = 1 holds. The other scores (C2 2 by the skipped 'by symmetry' step, C3 2 by no rounding statement, C4 2 by 'hold for every grid', C5 1 by a discussion with no numbers) match the annotations."),
 carry("SC1-d-exemplarA-claim", "2.9-prose", "course/modules/SC/SC1/project.html:470, 474-475, 482, 499, 503-508, 512",
       "project.html:470, 474-475, 482, 499, 503-508, 512 (no hunk touches them)",
       "Numbers re-derived this round: tail 0.086497 ('about 0.0865'); SE 0.010735; target 0.043248; 0.059548 - 0.043248 = 0.016300; 0.016300/0.010735 = 1.518 -> 1.52; 0.004361 at 256 steps and -0.001799 at 64 steps, lab output (labs_check_r5)."),
 fresh("SC1-d-exemplarB-onestep-claim", "2.9-prose / 2.2-numbers", "course/modules/SC/SC1/project.html:558",
       "Recomputed: tail - p = 0.086497 - 0.059548 = 0.026948 (printed 0.026948); tail/2 - 0.026948 = -0.016300; 0.016300/0.010735 = 1.52 standard errors. Sentence at :558 matches Lab 3 output at 'grid n = 1'."),
 fresh("SC1-d-exemplarB-numbers", "2.2-numbers", "course/modules/SC/SC1/project.html:524, 546, 558 vs lab output at :154-160 and :418-428",
       "Every Exemplar B number is a printed Lab 1 or Lab 3 value: 0.086497; 9.13e-15 (< 1e-14); 0.059548; 0.010735; 0.016300; 0.043248; 0.048142; 0.026948; 0.037215; 0.020788; -0.001799; 0.004361; 0.012870; 0.012455; 0.011239; 0.009819; nested 35, 29, 27, 22 with fine 40; walks 1588 and 794."),
 fresh("SC1-d-exemplarB-proof", "2.9-prose / 2.4-proof", "course/modules/SC/SC1/project.html:582-595 (exemplar B appendix)",
       "Round-4 FAIL resolved. P1 re-derived step by step: decomposition A = {tau <= t} = {M_t >= a} (continuity, IVT on [0,s] with B_0 = 0 < a); P(tau = t) = 0 (B_t normal, variance t); rho is a stopping time ({rho <= r} = {tau <= r} for r < t, Omega for r >= t; A4(c)); A is F_rho-measurable (A cap {rho <= r} = A in F_t for r >= t, = {tau <= r} in F_r for r < t); A4(h) for rho and t - rho; A4(b) with Z = (t - rho, 1_A), Y = tilde B independent of F_rho by A3, f jointly measurable by A4(g) (L05.html A4 list (b), (g), (h) text read); bar f(z) = 1/2 1{z2=1} 1{z1 > 0}; P(A, B_t < a) = 1/2 P(A) with P(tau = t) = 0; {B_t >= a} subset of A. Algebra and conclusion P(M_t >= a) = 2 P(B_t >= a) correct. Assumption list :583 now names A4(g) and A4(h). Residual unnamed steps are definitional (for example {B_t >= a} subset of A because M_t >= B_t) and carry their reason inline; accepted as not skipped."),
 fresh("SC1-d-exemplarB-p1-assumptions", "2.9-prose / 2.4-proof", "course/modules/SC/SC1/project.html:246, 249, 583-584",
       "Round-4 FAIL resolved. :246 and :249 and :583 list A4(b), A4(c), A4(g), A4(h). L05.html A4 list: (b) freezing, (c) hitting times, (g) joint measurability for continuous paths, (h) measurability at a stopping time (read at L05 lines 14-22). The P1 proof's justification steps each name one of these."),
 fresh("SC1-d-lab1-run", "2.5-labs", "course/modules/SC/SC1/project.html:55-160; tests/labs/SC1/lab-SC1-project-1.py",
       "run_labs SC1 -> 'run_labs SC1: PASS (11/11)' (gates1.txt). labs_check_r5: page code == twin, twin under `python -I -W error` exit 0, empty stderr, output == expected block."),
 carry("SC1-d-lab1-docstring", "2.5-labs / 2.9-prose", "course/modules/SC/SC1/project.html:58-68; tests/labs/SC1/lab-SC1-project-1.py:3-8",
       "project.html:58-68 and the Lab 1 twin lines 3-8 (no hunk touches them)",
       "Docstring re-read: 'draws the same four numbers in the same order' (make_instance matches instance.py:23-27); six-decimal rounding and the .2e Simpson difference match lines 145-149."),
 fresh("SC1-d-lab2-run", "2.5-labs", "course/modules/SC/SC1/project.html:164-210; tests/labs/SC1/lab-SC1-project-2.py",
       "labs_check_r5: page code differs from the twin only in the two `___` blanks (count 2); the twin under -I -W error exits 0 with output equal to the expected block (29 / 22 / 7 / True)."),
 fresh("SC1-d-lab2-attribution", "2.9-prose / attribution", "course/modules/SC/SC1/project.html:209 vs course/modules/SC/SC1/L06.html (Proposition 1.3, Corollary 1.4)",
       "L06.html Corollary 1.4 (discrete tail identity) reads #{M_N >= a} = #{S_N >= a} + #{S_N > a} with assumptions 'those of Proposition 1.3, for every integer a >= 1' (L06 lines 85-100, read this round). Lab 2 prints 29 = 22 + 7 for n = 6, a = 2."),
 fresh("SC1-d-lab3-run", "2.5-labs", "course/modules/SC/SC1/project.html:303-430; tests/labs/SC1/lab-SC1-project-3.py",
       "labs_check_r5: twin under -I -W error exits 0, empty stderr, output equals the expected block line for line (hits 29, 24, 32, 43, 40; nested 35/29/27/22; walks 1588/794). Page code == twin."),
 fresh("SC1-d-lab3-onestep-interp", "2.5-labs / 2.9-prose", "course/modules/SC/SC1/project.html:429 vs tests/labs/SC1/lab-SC1-project-3.py:99",
       "The :429 interpretation prints tail minus estimate for the one-step row and its target as half the tail (0.043248), matching lab line 99 (tail - p)."),
 carry("SC1-d-lab3-docstring", "2.5-labs / 2.9-prose", "tests/labs/SC1/lab-SC1-project-3.py:3-11 (page :306-317)",
       "the Lab 3 twin lines 3-11 and page :306-317 (no hunk touches them)",
       "Docstring read in full: 'drawn in the same fixed order' (make_instance matches), path-by-path draws (path_maxima), divisor N - 1 (estimate_and_se), every (256/n)-th point, six-decimal rounding."),
 fresh("SC1-d-labs-pytest", "2.5-labs / tooling", "tests/test_labs.py -k SC1; tests/test_run_labs.py; tests/test_page_checks.py; tests/test_memo_exemplars.py",
       "`pytest -q -k SC1` over those four files -> 11 passed (run this round)."),
 fresh("SC1-d-calib-B", "2.9-prose / rubric scoring", "course/modules/SC/SC1/project.html:518-599 (exemplar B)",
       "Round-4 FAIL resolved. Exemplar B's scores (C1 4, C2 4, C3 4, C4 3, C5 4) match its annotations: C2 level 4 now has the P1 freezing, stopping-time, measurability and joint-measurability justifications named. C4 3 matches the 'Misses C4 level 4' annotation at :575. Exemplar B's :520 verdict and data-scores :518 agree."),
 fresh("SC1-d-statements", "2.6-spec / 2.4-proof", "course/modules/SC/SC1/project.html:241-262",
       "Re-read after the delta: P1 assumptions (:245-247) and statement (:249); P2 (:251-255) and its erfc form (checked: erfc(x) = 2(1 - Phi(x sqrt 2)), so erfc(a/sqrt(2t)) = 2(1 - Phi(a/sqrt t))); P3 (:257-261) now states a > 0 and continuity. P3 second part: tau_a < inf is an increasing union, and erfc(0) = 1."),
 fresh("SC1-d-A1-label", "2.6-spec / attribution", "course/modules/SC/SC1/project.html:236-242, 577-580; course/modules/SC/SC1/L01.html:58-63; L05.html",
       "L01.html:58-63 Definition 1.1: (D1) B_0 = 0, (D2) normal increments with mean 0 and variance t - s, (D3) independent increments; matches how P1-P2 cite it. L05.html A3 and A4 list read (lines 14-22, 152-158). 'A3 and A4 are Assumptions 3 and 4 of Lesson 5' matches."),
 fresh("SC1-d-A3-A4-usage", "2.6-spec / attribution", "course/modules/SC/SC1/project.html:242, 246, 249; course/modules/SC/SC1/L05.html (A3, A4 list)",
       "Each cited part exists in L05.html: A3 (bounded stopping time, conclusion: B_{rho+r} - B_rho standard BM independent of F_rho), A4(b) freezing, A4(c) hitting times, A4(g) joint measurability, A4(h) measurability at a stopping time (bounded by c). P1's bounded rho = tau_a wedge t matches L05 Lesson 6 use."),
 fresh("SC1-d-dag", "2.7-DAG", "course/modules/SC/SC1/project.html; tools/check_dag.py --unit SC1",
       "`tools/check_dag.py --unit SC1` -> 'check_dag SC1: PASS' (gates1.txt). No new concept link in the delta; stopping-time and normal-distribution links resolve."),
 fresh("SC1-d-notation", "2.8-notation", "course/modules/SC/SC1/project.html passim; notation/notation.json",
       "Registry macros used: \\Prob, \\Normal, \\indic (all registered). Registered symbol \\Phi (standard normal CDF) used with the same meaning at :230. T is registered (number of return observations, S1) and the page avoids it (:230 says H is used). New local letters in the delta (Z, Y, f, G, \\bar f, \\tilde B, \\mathcal G, rho, tau) are not registry symbols. No reuse."),
 fresh("SC1-d-define-before-use", "2.5-labs / 2.9-prose", "course/modules/SC/SC1/project.html:37, 45, 53, 57, 230",
       "Running maximum, grid maximum, level a, horizon H and the one-step estimate are defined at :37, :53, :57 and the conventions at :230 precede the statements at :241. The new terms (grid maximum, discretization bias) are defined before the new text uses them (:231, :235)."),
 fresh("SC1-d-discretization-bias", "2.9-prose", "course/modules/SC/SC1/project.html:225, 229, 235",
       "The discretization bias is the continuous tail minus the grid probability (:235); its estimate is the tail minus the grid estimate; 'can be negative through sampling noise, as Lab 3 shows at 64 steps' matches -0.001799 (lab output)."),
 fresh("SC1-d-monte-carlo-term", "2.9-prose", "course/modules/SC/SC1/project.html:231-232, 235, 375-379 (Lab 3 code)",
       "Terms estimate, standard error, path and sample are defined before use (:231-232, :235); the Lab 3 estimate_and_se at page lines 375-379 equals the twin."),
 fresh("SC1-d-scope-words", "2.9-prose", "course/modules/SC/SC1/project.html:217, 223, 231-238, 449, 570",
       "Scope words re-read, including the new :217 ('less often ... by an amount') and the new :570 ('holds on every path', 'any statement that holds almost surely'). Each universal claim is computed by a lab row, follows from a stated hypothesis (grid points lie in [0, H]; P1-P3 for every case meeting their assumptions), or is a negative scope limit."),
 fresh("SC1-d-process-words", "2.9-prose / 12", "course/modules/SC/SC1/project.html:619-622 (former round-4 location)",
       "Round-4 FAIL resolved. The Reading section no longer says 'curriculum' or 'registry record' (grep -i curricul|registry over project.html returns nothing). The one remaining build-style term is 'workspace ID' at :219, the autograder panel's own term, which round 4 also did not count. Judgement: the Reading paragraph now lists only the admissible key, with no claim that it is the curriculum's full list; accepted as not a process word and not a completeness claim about learner text."),
 fresh("SC1-d-banned-structure", "2.9-prose / structure", "course/modules/SC/SC1/project.html; tools/check_pages.py --unit SC1",
       "`tools/check_pages.py --unit SC1` -> 'check_pages SC1: PASS' (gates1.txt)."),
 fresh("SC1-d-registry", "2.8-references", "course/modules/SC/SC1/project.html:619-622; references/references.json (shreve2004stochastic)",
       "shreve2004stochastic present (status verified, used_by SC1, origin manual). `tools/verify_refs.py --offline` -> 'offline integrity: 560 entries, 0 problems' (this round). The page cites it at book level with no locator."),
 carry("SC1-d-privacy-claim", "2.9-prose / attribution", "course/modules/SC/SC1/project.html:288, 603, 636",
       "project.html:288, 603, 636 and course/assets/js/grader.js, rubric.js, store.js (no hunk in the delta touches assets/)",
       "grader.js:61 stores the draft after a 400 ms debounce (setTimeout ... store.put); the claims 'saved in this browser' and 'stay in this browser' hold by the code. Live browser storage not exercised."),
 fresh("SC1-d-tools-gates", "tooling", "course/modules/SC/SC1/grader; tests/test_labs.py -k SC1 and the three related files; references",
       "ruff check and ruff format --check on course/modules/SC/SC1/grader: 'All checks passed', '4 files already formatted' (this round). mypy --no-incremental: 'Success: no issues found in 385 source files' (exit 0). pytest -k SC1 (four files): 11 passed. verify_refs --offline: 0 problems. check_projects, check_pages, check_dag, run_labs (11/11), run_graders all PASS (gates1.txt)."),
 fresh("SC1-d-numbers-prose", "2.2-numbers", "course/modules/SC/SC1/project.html:57, 154-160, 209, 219, 225, 305-317, 418-429, 470-512, 524-558",
       "Every prose number re-derived from the lab output and arithmetic on the unrounded values: tail 0.086497, SE 0.010735, target 0.043248, band 0.048142, differences 0.016300 and 0.026948, 0.14 SE for the 64-step row (0.001799 / 0.012870), 1.52 SE (0.016300 / 0.010735), 4096 walks of 12 steps, 2^40 for n = 41 (exact). Changed hunks of the delta contain no new numbers."),
 fresh("SC1-d-spec-n41-method", "2.6-spec / 2.6-autograder", "course/modules/SC/SC1/project.html:223; grader/reference.py:79-85; ledgers/SC1/scripts/SC1-d-r5/alternatives/alt7_gauss_step_major.py",
       "project.html:223 allows binomial coefficients, the reflection identity or a recurrence for n = 41. reference.py srw_terminal_count is a binomial sum. The n = 41 test is method-agnostic and alt3 (DP) passes it on seeds 0-999."),
 fresh("SC1-d-ag-draws-depend-overconstraint", "2.6-autograder", "course/modules/SC/SC1/grader/test_project.py:356-365 (test_draws_depend_on_the_instance_seed)",
       "Round-4 FAIL resolved. The new test uses a = 1e-9 for both instances. Current reference: 3000/3000 seeds pass (sweep_reference_0_2999.txt). The old test's failure mode is confirmed: zero_estimate_seeds_r5.py finds exactly 18 seeds in 0-2999 (88, 123, 146, 440, 939, 1394, 1489, 1638, ...) where every grid estimate is 0 at the instance's own level for both seeds, so the docstring's 'for some seeds ... both estimates are 0' holds. All alternatives pass (SC1-d-ag-alternatives-ok)."),
 carry("SC1-d-ag-band-overconstraint", "2.6-autograder", "course/modules/SC/SC1/grader/test_project.py:76-82, 314-329, 418-425",
       "test_project.py:76-82, 314-329, 418-425 (the delta's test hunk is at :356-365)",
       "The band is 5 target standard errors plus one path for the target p; the one-step and one-step coarse tests use it with the target's SE; the reference and all alternatives pass it on seeds 0-999 (sweep)."),
 fresh("SC1-d-reading-disclosure", "2.9-prose / attribution (judgement row, round 5)", "course/modules/SC/SC1/project.html:619-622; course/modules/SC/SC1/index.html:183",
       "The round-4 process-word fix removed the sentence that the curriculum lists a second source with no admissible record. The hub index.html still discloses it. The project page's 'The reading for this unit is listed below' lists the one admissible key, cites it at book level, and does not claim the curriculum's list is complete. PASS as a judgement; restoring the sentence would reintroduce the build vocabulary the round-4 process-word rule removed."),
 fresh("SC1-d-delta-r5-read", "2.9-prose / 2.6 (round-5 delta)", "course/modules/SC/SC1/project.html (hunks at :217, :232, :233, :246, :249, :261, :466, :570, :583, :590, :619); course/modules/SC/SC1/grader/test_project.py:356-365",
       "Every hunk of the 9a02b1af..7376a5e delta to project.html and test_project.py read in full and checked against L01, L05, L06 and the grader: the stronger Context sentence; the grid-maximum bias sentence; the rewritten draw-order sentence (alt7 passes, Lab 3 numbers differ: grid 4 0.049281 vs 0.071869; grid 16 0.065708 vs 0.075975); the A4(g), A4(h) additions; the P1 proof and its justification; P2/P3 assumption additions; the exemplar A verdict and data-scores; the exemplar B annotation and appendix; the Reading paragraph; the draws test."),
]

mut_txt = (OUT / "mutate_graders_r5.txt").read_text(encoding="utf-8").splitlines()
mutants = []
for line in mut_txt:
    m = re.match(r"KILLED (\S+?)\.py: (.*?) -> (.*)$", line)
    if m:
        name, desc, killed = m.group(1), m.group(2), m.group(3)
        mutants.append({"id": name, "description": desc, "killed_by": killed})
assert len(mutants) == 34, len(mutants)

counts_pass = sum(1 for r in rows if r["status"] == "PASS")
frag = {
    "unit": "SC1",
    "slice": "d",
    "round": 5,
    "verifier": "Claude Haiku 5.5, independent verifier (slice d, round 5)",
    "pin": "7376a5e216c1e6d99becc76b4cd64028f5b55d3f",
    "base": "1c1645f3",
    "checkout": str(ROOT),
    "scratch": "/tmp/sc1d_r5_collect, /tmp/sc1d_r5 (logs only)",
    "verified_at": datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat(),
    "verdict": "PASS" if counts_pass == len(rows) else "FAIL",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "Delta 9a02b1af -> 7376a5e (previous pin, round 4) read in full for slice d: project.html hunks at :217, :232, :233, :246, :249, :261, :466, :570, :583, :590, :619; grader/test_project.py :356-365 only. "
        "Other delta files (lessons, cards, hub index.html, labs of other slices, references, notation, curriculum, assets) are outside this slice; only cited lines were checked. "
        "Not checked: the in-browser grader panel UI and self-assessment form (only page_smoke's Pyodide run); live localStorage; the exemplar scoring is read as annotated, not blind; "
        "the 240 s hang of the enumeration alternative at n = 41 was not timed (alt2b excluded as spec-forbidden); seeds beyond 2999 for the draws test; "
        "alt4 (Box-Muller) excluded as non-conforming with the gauss statement. Judgement calls, accepted: (1) exemplar B C2 level 4 with a few definitional steps carrying their reason inline; "
        "(2) the Reading paragraph no longer names the second curriculum source (see SC1-d-reading-disclosure). mutate_graders was run with its default --seeds 0-9 (the seed window of the tool); the reference sweep used 0-2999."
    ),
    "summary": (
        "SC1 slice d round 5 (project.html, grader, project labs, mutants, five-plus alternatives): %s. Rows: %d (%d PASS, %d FAIL, 0 UNVERIFIABLE). "
        "Mutants: %d in ledgers/SC1/mutants, all KILLED (34/34; m32-m34 new this round). Round-4 FAILs resolved: draws-test over-constraint (reference 3000/3000 seeds; alternatives 1000/1000), exemplar A C1 score, exemplar B P1 hypotheses and proof justification, exemplar B C2 score, process word at the Reading section."
    ) % ("PASS" if counts_pass == len(rows) else "FAIL", len(rows), counts_pass, len(rows) - counts_pass, len(mutants)),
}
dest = ROOT / "ledgers/SC1/SC1-d.json"
dest.write_text(json.dumps(frag, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", dest, "rows", len(rows), "mutants", len(mutants), "verdict", frag["verdict"])
