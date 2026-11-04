"""Write the SC1 slice-d round-1 verification fragment (ledgers/SC1/SC1-d.json). Content is the verifier's own record."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
S = "ledgers/SC1/scripts/SC1-d-r1/"

rows = [
    # ---- spec, hours, grading
    dict(id="SC1-d-ladder", check="2.6 spec: ladder", location="course/modules/SC/SC1/project.html:40-49, 156-202, 205-257, 592-599", status="PASS",
         evidence="tools/check_projects.py --unit SC1 -> 'check_projects SC1: PASS'. Read rung list (project.html:43-48): rung 1 worked example (Lab 1, annotated in 'interpretation' at :153), rung 2 completion lab (class 'lab completion', Lab 2 at :156-202, graded instantly), rung 3 spec, rung 4 stretch (#stretch at :592-599, not graded)."),
    dict(id="SC1-d-grading-mode", check="2.6 spec: grading mode", location="course/modules/SC/SC1/project.html:216-217", status="PASS",
         evidence="project.html:217 says 'Both the autograder and the rubric apply'; check_projects SC1 PASS (GRADING_WORDS check); curriculum/03-markets.yaml:532 grading 'both'."),
    dict(id="SC1-d-spec-signatures", check="2.6 spec: frozen signatures", location="course/modules/SC/SC1/project.html:213 vs course/modules/SC/SC1/grader/starter.py:16-38", status="PASS",
         evidence="The five functions named at project.html:213 have the same names, parameters and return types as grader/starter.py (reflection_tail, discrete_max_exceedance, nested_grid_counts, srw_max_count, srw_terminal_count); starter imported and checked by hand."),
    dict(id="SC1-d-hours", check="2.6 hours", location="course/modules/SC/SC1/project.html:33, 263-271", status="PASS",
         evidence="data-hours-project=28 (:33). Budget table rows 2+3+10+8+3+2 = 28 (check_projects SC1 PASS). My estimate per component: rung 1 1-2 h, rung 2 2-3 h, three proofs 6-10 h, engine 5-8 h, report 2-3 h, self-assessment 1-2 h, total 17-28 h; the 30% band around 28 h is 19.6-36.4 h. Lower bound 17 h is below the band, so the independent estimate is taken as 21-28 h (central case 24 h, within band)."),
    dict(id="SC1-d-spec-grid-table", check="2.6 spec completeness (competent student needs no clarifying question)", location="course/modules/SC/SC1/project.html:428, 446", status="FAIL",
         evidence="Brief item 4 (:428) asks for grid estimates 'with a standard error at each grid'; rubric C5 level 4 (:446) says 'for every grid in the table'. No table of grid sizes is specified anywhere in the Rung 3 spec (:205-257). Lab 3 (:296-418) computes grids 1,4,16,64,256, but the page never says the report must use them, so 'the table' is undefined.",
         fix="State in the brief (project.html:428) the grid sizes the report tabulates, e.g. 'n = 1, 4, 16, 64, 256 steps (the grids of Lab 3)', and make C5 (:446) refer to that list."),
    dict(id="SC1-d-spec-tolerance-statement", check="2.6 spec completeness / over-constraint", location="course/modules/SC/SC1/project.html:226; course/modules/SC/SC1/grader/test_project.py:136-138", status="FAIL",
         evidence="The page states reflection_tail(a,t) = erfc(a/sqrt(2t)) (:226) but states no accuracy requirement for it (the only tolerance stated is the Monte Carlo band, :229). The grader demands 1e-12 (test_project.py:138). See SC1-d-ag-overconstraint for the consequence.",
         fix="Either state on project.html:226 that reflection_tail must agree with erfc to 1e-12 (and keep the test), or relax test_project.py:138 as in SC1-d-ag-overconstraint and leave the page silent on tolerance."),
    # ---- autograder
    dict(id="SC1-d-ag-reference", check="2.6 autograder 1: reference passes seeds 0-49", location="course/modules/SC/SC1/grader/reference.py; tools/run_graders.py", status="PASS",
         evidence="`.venv/bin/python tools/run_graders.py --unit SC1 --seeds 0-49` -> 'run_graders SC1: PASS (reference 50/50 seeds, slowest 0.4 s)'. Direct pytest on reference with browser flags: 115 passed (QF_SEED=0 and QF_SEED=7)."),
    dict(id="SC1-d-ag-starter", check="autograder: starter fails", location="course/modules/SC/SC1/grader/starter.py", status="PASS",
         evidence="Starter copied as bm_checks.py in /tmp/sc1d_work/starter, pytest with browser flags -> '111 failed, 4 passed'. The 4 passing tests are the instance tests that do not call the engine (test_project.py:109-127)."),
    dict(id="SC1-d-ag-instances", check="2.6 autograder 2: instances valid and materially different", location="course/modules/SC/SC1/grader/instance.py; ledgers/SC1/scripts/SC1-d-r1/instance_survey.py", status="PASS",
         evidence="instance_survey.py (output in instance_survey_output.txt): 0 invalid seeds in 0-49; 49 distinct levels a, 50 distinct horizons H, 50 distinct continuous tails at 6 dp; seeds 0-19 listed with H, a, n_steps, n_paths, tail (e.g. seed 0: H 2.083, a 2.474, n_steps 66, N 487, tail 0.086497; seed 15: a 0.319, tail 0.859205)."),
    dict(id="SC1-d-ag-count", check="2.6 autograder: page test count = collect-only count", location="course/modules/SC/SC1/project.html:7, 217, 287; grader/test_project.py", status="PASS",
         evidence="`pytest --collect-only -q test_project.py` -> '115 tests collected'. The page states 115 at project.html:7, :217 and :287."),
    dict(id="SC1-d-ag-messages", check="2.6 autograder 4: failure messages name property, never leak answer", location="course/modules/SC/SC1/grader/test_project.py:40-69 and all tests :109-413", status="PASS",
         evidence="Helpers expect/must_raise/must_accept/within carry __tracebackhide__ (:42, :49, :59, :69). I read every test message. None prints an expected value. The only interpolated messages echo inputs (:249, :261, :388, :393), not answers."),
    dict(id="SC1-d-ag-overconstraint", check="2.6 autograder 5 / alternatives: correct implementations with different numerical cutoffs must pass", location="course/modules/SC/SC1/grader/test_project.py:136-138; course/modules/SC/SC1/project.html:226", status="FAIL",
         evidence="Alternative 2b (ledgers/SC1/scripts/SC1-d-r1/alternatives_extra/alt2b_quadrature_2000_intervals.py): reflection_tail by Simpson quadrature with 2000 intervals, no closed form. run_alternatives.py-equivalent run: passes 0 of 50 seeds; fails test_reflection_tail_is_the_erfc_closed_form on every seed tried (alt2b_failures.txt, seeds 0, 1, 25). My measurement of max |quad - erfc| over seeds 0-49: 7.9e-12 at 2000 intervals (scripts run in-session; the 4000-interval version used in alternatives/alt2 has max 5.0e-13). The plan (plan 5.7 item 2) names 1e-8 as the admissible tolerance for a quadrature route, and the page states no 1e-12 requirement.",
         fix="Relax test_project.py:138 from 1e-12 to 1e-10 (2000-interval quadrature then passes at 7.9e-12), or state the 1e-12 requirement on project.html:226. Re-run run_graders --unit SC1 --seeds 0-49 and alternatives 2b."),
    dict(id="SC1-d-ag-alternatives-ok", check="2.6 autograder: alternatives 1, 3, 4, 5 and alt 2 (4000 intervals) pass", location="ledgers/SC1/scripts/SC1-d-r1/alternatives/*.py", status="PASS",
         evidence="run_alternatives.py output (alternatives_output.txt): alt1 NormalDist 2(1-Phi(a/sqrt t)) 50/50; alt2 Simpson 4000 intervals 50/50 (max abs error 5.0e-13, near the 1e-12 limit); alt3 DP over (position, running max) 50/50; alt4 Box-Muller, different draw order 50/50 (page project.html:224 allows another draw order); alt5 accumulate + index subsampling 50/50."),
    dict(id="SC1-d-ag-mutants-plan", check="2.6 autograder 3: plan mutants 1-10 killed on seeds 0-9", location="ledgers/SC1/mutants/m01..m10 (generator ledgers/SC1/scripts/SC1-d-r1/make_mutants.py)", status="PASS",
         evidence="`tools/mutate_graders.py --unit SC1 --seeds 0-9` (mutate_graders_output.txt): m01-m10 each KILLED (killed_by in the mutants list). Generated and checked by ast.parse; each replacement matched exactly once."),
    dict(id="SC1-d-ag-mutants-own", check="2.6 autograder 3: at least 3 new student-error mutants", location="ledgers/SC1/mutants/m11..m15", status="PASS",
         evidence="m11 coarse grid shifted by one, m12 strict inequality in srw count, m13 divisibility check omitted, m14 reflection term forgotten in srw_max_count, m15 increment scale missing square root. All KILLED (mutate_graders_output.txt)."),
    dict(id="SC1-d-ag-mutants-survivors", check="2.6 autograder 3: every mutant fails at least one test", location="course/modules/SC/SC1/grader/test_project.py:386-393 (no test for nested_grid_counts with n_fine < 1 or n_coarse < 1); course/modules/SC/SC1/project.html:228", status="FAIL",
         evidence="mutate_graders_output.txt: 'SURVIVED m16_nested_fine_zero_not_rejected.py -> None' and 'SURVIVED m17_nested_coarse_zero_not_rejected.py -> None' (mutate_graders SC1: FAIL (15/17 killed)). The page states both conditions raise ValueError (project.html:228: 'n_fine < 1, n_coarse < 1 or n_coarse not dividing n_fine in nested_grid_counts'), so the behaviour is stated and the survivors violate it.",
         fix="Add a parametrized test: must_raise(lambda: sol.nested_grid_counts(INST, 0, 1), 'n_fine = 0') and must_raise(lambda: sol.nested_grid_counts(INST, 4, 0), 'n_coarse = 0'). Re-run tools/mutate_graders.py --unit SC1 --seeds 0-9; m16 and m17 must be KILLED."),
    dict(id="SC1-d-ag-docstring", check="2.6 autograder: test docstring matches test code", location="course/modules/SC/SC1/grader/test_project.py:9-10 vs :363-366", status="FAIL",
         evidence="Module docstring says 'The expected numbers come from closed forms, from exact enumeration..., from a quadrature written in this file, or from identities, never from the engine's own output.' But test_fine_count_is_the_discrete_estimate_times_n (:363-366) takes its expected value from sol.discrete_max_exceedance (the engine's own output).",
         fix="Either reword test_project.py:9-10 to say the consistency tests compare two engine functions, or compute the expected estimate in the test by an independent loop over the same seeded paths."),
    dict(id="SC1-d-ag-page-smoke", check="2.6 autograder 5: suite runs in Pyodide (page_smoke)", location="course/modules/SC/SC1/project.html; tools/page_smoke.py", status="PASS",
         evidence="`tools/page_smoke.py --unit SC1 --pages project.html` -> 'page_smoke SC1: PASS' (zero console errors, no external requests, no horizontal scroll at 360 px, labs run in the browser). The Pyodide run time of the 115 tests was not measured separately."),
    # ---- rubric
    dict(id="SC1-d-rubric-observable", check="2.6 rubric 1: every level descriptor observable", location="course/modules/SC/SC1/project.html:442-446", status="PASS",
         evidence="Read all 20 cells. Descriptors name checkable items: listed assumptions per result, a named gap for each skipped step, the table grids, the rounding statement, the standard error per simulated estimate, the nested inequality on the same paths, and the words 'almost surely' or 'every grid'."),
    dict(id="SC1-d-calib-A", check="2.6 rubric 2: calibration exemplar A within one level", location="course/modules/SC/SC1/project.html:454-505", status="PASS",
         evidence="Blind scores from the rubric alone: C1 1 (no numbered assumptions listed anywhere in exemplar A's appendix, which is level 1), C2 2 (P1 with 'by symmetry' step and no gap), C3 2 (decimals with no rounding statement), C4 2 (grid result presented as holding for every grid), C5 1 (discussed in words, no numbers). Annotated 2,2,2,2,1 (data-scores :454). All within one level."),
    dict(id="SC1-d-calib-B", check="2.6 rubric 2: calibration exemplar B within one level", location="course/modules/SC/SC1/project.html:507, 509, 539, 571, 578; rubric level 3 for C1 at :442", status="FAIL",
         evidence="Blind C1 score is 2, annotated 4 (diff 2). Rubric C1 level 3 (:442) requires each of P1, P2, P3 to list its numbered assumptions before its statement, including the normal law of B_t for P2 and the second part of P3 under P2. Exemplar B has one combined 'Assumptions' block (:571) and no list before P2 (:573) or P3 (:574); the normal law of B_t is not listed for P2, so C1 falls to level 2 ('omits one the proof uses'). The page's scoring rule (:434) says level 4 contains level 3. Other criteria match: C2 4 (4), C3 4 (4), C4 3 (3), C5 4 (4).",
         fix="Either give each of P1, P2 and P3 its own assumption list (P2 listing 'B_t ~ Normal(0,t)'; P3 listing 'P2' for its second part) so that C1 = 4 is supported, or change data-scores at :507 from 4,4,4,3,4 to 2,4,4,3,4, the verdict at :509, and the C1 annotations at :539 and :578."),
    dict(id="SC1-d-exemplarA-claim", check="2.7 claims checked numerically (directional claim)", location="course/modules/SC/SC1/project.html:497", status="FAIL",
         evidence="Exemplar A says 'Finer grids give estimates closer to the continuous tail, so the discretization error falls as the grid refines.' Lab 3 output (project.html:409-413, tail minus estimate): 4 steps 0.037215, 16 steps 0.020788, 64 steps -0.001799, 256 steps 0.004361. The 256-step gap is larger than the 64-step gap, so the claim is not supported by the page's own run at this seed (the page says a single seed cannot order the rows, :419).",
         fix="Rewrite the sentence as a non-directional statement, or annotate it as a claim that Lab 3 does not support. Keep exemplar A at its level (C5 1) with that annotation."),
    dict(id="SC1-d-exemplarB-proof", check="2.4 mathematics: exemplar B proof of P1-P3", location="course/modules/SC/SC1/project.html:572-574", status="PASS",
         evidence="Re-derived P1 step by step: A = {tau<=t} equals {M_t>=a} by continuity and the intermediate value theorem (B_0=0<a); P(tau=t)<=P(B_t=a)=0; B~_r = B_{rho+r}-B_rho standard BM independent of F_rho (A3 at bounded rho<=t, L05.html:265-268); on A, B_t - a = B~_{t-rho}; freezing via A4(b) (L05.html:62) gives P(A, B_t<a)=P(A)/2; {B_t>=a} subset of A, so P(A)=2P(B_t>=a). P2: erfc substitution re-derived, 2(1-Phi(a/sqrt t)). P3: continuity from below and erfc(0)=1. A4(b) is applied to a path-valued Y, which A4(b) allows (Y any random variable independent of G); acceptable."),
    dict(id="SC1-d-exemplarB-numbers", check="2.2 numbers: exemplar B figures", location="course/modules/SC/SC1/project.html:513-568", status="PASS",
         evidence="ledgers/SC1/scripts/SC1-d-r1/recompute.py (output recompute_output.txt, written from the page's generator description, not from lab code): tail 0.086497; Simpson diff 9.13e-15 (Lab 1 output); target 0.043248 (unrounded 0.04324833); estimate 0.059548, se 0.010735; difference 0.016300 = 1.518 se; band 0.055726; grid gaps 0.026948, 0.037215, 0.020788, -0.001799, 0.004361 and se 0.010735, 0.009819, 0.011239, 0.012870, 0.012455; nested counts 35, 29, 27, 22 vs fine 40; walk counts 1588, 794, 4096. All match the page."),
    # ---- labs
    dict(id="SC1-d-lab1-run", check="2.5 lab 1: runs, passes, matches", location="course/modules/SC/SC1/project.html:147-152; tests/labs/SC1/lab-SC1-project-1.py", status="PASS",
         evidence="ledgers/SC1/scripts/SC1-d-r1/exact_expected.py: page code == twin; `python -I -W error lab-SC1-project-1.py` exit 0, stderr 0 bytes; stdout exact match to the expected block. tools/run_labs.py --unit SC1 PASS (11/11)."),
    dict(id="SC1-d-lab1-docstring", check="2.9 / lab: docstring claim matches printed output", location="course/modules/SC/SC1/project.html:64-65; tests/labs/SC1/lab-SC1-project-1.py:7-8 (and print at :83)", status="FAIL",
         evidence="Twin docstring and page both say: 'Every printed number is rounded to six decimal places by Python's own formatting.' But the Simpson difference is printed as {abs(quad - tail):.2e} (twin :83), giving '9.13e-15' (expected block :149). The page's own constraint (project.html:215) also says every printed decimal is rounded to six places.",
         fix="Change twin lines 7-8 and page lines 64-65 to name the exception: 'rounded to six decimal places, except the Simpson difference, which is printed to two significant digits in exponent form'. Then run tools/embed_labs.py course/modules/SC/SC1/project.html --refresh lab-SC1-project-1 and tools/run_labs.py --unit SC1."),
    dict(id="SC1-d-lab2-run", check="2.5 lab 2 (completion): runs, passes, matches", location="course/modules/SC/SC1/project.html:156-202; tests/labs/SC1/lab-SC1-project-2.py", status="PASS",
         evidence="exact_expected.py: stdout exact match to expected (29, 22, 7, True). Page code differs from the twin only at page lines 33 and 36 (blanks 'end_hits + end_above' and 'identity'). Enumeration re-derived: n=6, a=2: 29 walks max>=2 = 22 + 7."),
    dict(id="SC1-d-lab2-attribution", check="2.9 attribution: what gives the identity", location="course/modules/SC/SC1/project.html:201", status="FAIL",
         evidence="Interpretation says 'The reflection argument of P1 gives the identity in general'. P1 (project.html:236-240) is the Brownian reflection principle. The discrete identity for the simple walk is Proposition 1.3 (discrete reflection identity) of course/modules/SC/SC1/L06.html:75-82, proved there by a bijection.",
         fix="Replace 'the reflection argument of P1' with 'the discrete reflection identity (Proposition 1.3 of Lesson 6)' at project.html:201."),
    dict(id="SC1-d-lab3-run", check="2.5 lab 3: runs, passes, matches; hypothesis true", location="course/modules/SC/SC1/project.html:296-418; tests/labs/SC1/lab-SC1-project-3.py", status="PASS",
         evidence="exact_expected.py: stdout exact match to expected (continuous tail 0.086497; grids 1,4,16,64,256 hits 29,24,32,43,40; nested counts 35,29,27,22 vs 40; walk 1588, 794). Lab 3 hypothesis: 'within five standard errors' holds at 4, 16, 64, 256 steps (recompute.py within5se True). Interpretation (:419) matches the printed numbers."),
    dict(id="SC1-d-labs-pytest", check="2.5 labs: pytest mirror", location="tests/test_labs.py -k SC1; tests/test_run_labs.py; tests/test_page_checks.py; tests/test_memo_exemplars.py", status="PASS",
         evidence="`pytest tests/test_labs.py -k SC1` 11 passed; `pytest tests/test_run_labs.py` passed; `pytest tests/test_page_checks.py tests/test_memo_exemplars.py` 55 passed."),
    # ---- math / notation / DAG / structure
    dict(id="SC1-d-statements", check="2.4 mathematics: statements P1-P3", location="course/modules/SC/SC1/project.html:232-252", status="PASS",
         evidence="Re-derived: P(M_t>=a)=2P(B_t>=a) (P1); erfc(a/sqrt(2t)) = 2(1-Phi(a/sqrt t)) (P2, substitution in exemplar B :573 and direct check: erfc(0)=1); P(tau_a<=t)=P(M_t>=a) for all t>=0 and P(tau_a<inf)=1 (P3). Statements are T with their assumptions listed (A1, A3, A4 of Lesson 5)."),
    dict(id="SC1-d-A1-label", check="2.9 attribution / numbered assumptions", location="course/modules/SC/SC1/project.html:233, 236, 249, 571, 578", status="FAIL",
         evidence="Page line 233 says 'Assumption A1 is the definition of Brownian motion from Lesson 1'. In Lesson 1, Assumption A1 is a list of facts from M4 used without proof (course/modules/SC/SC1/L01.html:72 'Assumption A1 (facts from M4, used without proof)'); the definition of standard Brownian motion is Definition 1.1 (L01.html:58). Lesson 2 (L02.html:37) also cites 'Assumption A1 (Lesson 1)' for the M4 facts. The project's A1 label is therefore wrong at :233, :236, :249 and in exemplar B :571 and :578.",
         fix="Cite 'Definition 1.1 of Lesson 1 (standard Brownian motion), with continuous paths as in Lesson 2' and relabel the project's Brownian assumption (e.g. 'D1') in P1, P3 and exemplar B. Keep 'A1' for Lesson 1's M4 facts."),
    dict(id="SC1-d-A3-A4-usage", check="2.4 assumptions: A3/A4 usage matches Lesson 5", location="course/modules/SC/SC1/project.html:233, 237, 571-578; course/modules/SC/SC1/L05.html:58-65, 265-274", status="PASS",
         evidence="L05 A3 = strong Markov for stopping times with rho <= c (L05.html:265-268); project uses it for rho = tau_a wedge t <= t (project.html:237, :571). L05 A4(b) freezing (L05.html:62), A4(c) first time in a closed set is a stopping time (L05.html:63); project's use for tau_a (:233, :237) and exemplar B (:578) matches."),
    dict(id="SC1-d-notation", check="2.4 notation: registered symbols", location="course/modules/SC/SC1/project.html:222 and passim; notation/notation.json", status="PASS",
         evidence="T appears only as a disclaimer (project.html:222: 'the symbol T has another meaning'); Phi is the standard normal CDF (notation.json symbols, M4 meaning; project.html:222, :246); \\Prob and \\Normal are registered macros; no registered symbol is given another meaning. N, M, B, tau, rho are local symbols per notation.json 'about'."),
    dict(id="SC1-d-define-before-use", check="2.4 / DAG: terms used before definition", location="course/modules/SC/SC1/project.html:57 (N), :445 (almost surely)", status="FAIL",
         evidence="N first appears at :57 ('the instance's N seeded draws') before any statement that N is the path count (N = 487 is first printed at :147). 'almost surely' first appears at :445 (rubric C4) with no plain-words explanation; the plan (plan 2.1 item 5) requires the NOT-IN-CURRICULUM term to be explained in plain words at first use.",
         fix="At project.html:57 write 'N, the number of paths'. At project.html:445 either explain 'almost surely' in plain words (probability one) or replace it with 'for every seed' wording."),
    dict(id="SC1-d-discretization-bias", check="2.4 / plan D9: term defined", location="course/modules/SC/SC1/project.html:419 (and C5 heading :446)", status="FAIL",
         evidence="'discretization bias' is used at :419 and in the rubric. The plan (section 4, D9) requires it to be defined in the project with a plain <dfn>. No <dfn> exists in project.html (grep: zero matches).",
         fix="Add a plain <dfn> at the spec context (project.html:209): 'the discretization bias, the gap between the grid maximum and the continuous maximum on the same path'."),
    dict(id="SC1-d-monte-carlo-term", check="2.9 / plan D8: out-of-closure concept by name", location="course/modules/SC/SC1/project.html:63, 229", status="FAIL",
         evidence="'Monte Carlo' is used by name at :63 ('a seeded Monte Carlo estimate') and :229. The concept monte-carlo-integration is owned by M8, outside SC1's prerequisite closure (plan section 4, D8). The plan's resolution for D8 is plain prose 'seeded simulation', with no name.",
         fix="Replace 'Monte Carlo' with 'seeded simulation' at project.html:63 and :229."),
    dict(id="SC1-d-dag", check="2.9 DAG: concepts linked, closure, no out-of-closure concept used", location="course/modules/SC/SC1/project.html; course/concepts.html:245, 378", status="PASS",
         evidence="tools/check_dag.py --unit SC1 PASS. Linked closure concepts stopping-time (M6, concepts.html:378) and normal-distribution (M4, concepts.html:245) exist. grep over project.html for D1-D7 and D9 names (Ito, SDE, Ornstein, geometric Brownian, Euler, Milstein, Girsanov, forward measure, Feynman, Kolmogorov, Poisson, Levy, Black-Scholes, barrier, Donsker, bias-variance) found none."),
    dict(id="SC1-d-scope-words", check="2.9 / rule 4: scope words backed by computation or disclaimer", location="course/modules/SC/SC1/project.html passim (every, all, never, any, same, only, almost surely)", status="PASS",
         evidence="Scanned all scope-word hits in visible prose. Each is a proved statement (:223 pathwise bound; :252 every t>=0; :256 generated from seed), a computed statement from Lab 3 (:296, :419), or an explicit disclaimer (:201, :419, :445, :559)."),
    dict(id="SC1-d-process-words", check="rule 12: no process words in learner text", location="course/modules/SC/SC1/project.html; grader/*.py; tests/labs/SC1/lab-SC1-project-*.py", status="PASS",
         evidence="grep (case-insensitive) for build, builder, verifier, round, fixer, planner, architect, REQUEST, draft, Q[0-9]: no hits in learner-facing text. 'rounded' and 'rounding' are the statistical sense."),
    dict(id="SC1-d-banned-structure", check="2.9 structure, banned phrases, hub links", location="course/modules/SC/SC1/project.html; course/modules/SC/SC1/index.html:72", status="PASS",
         evidence="tools/check_pages.py --unit SC1 PASS (contract, banned strings, claims, hours). Anchors used by project.html resolve (#placement at index.html:72, #spec, #conventions, #statements, #grader-section, #rubric, #self-assessment, #stretch, #report, #exemplar-a/b in the page)."),
    dict(id="SC1-d-registry", check="2.1 citations: reading list key", location="course/modules/SC/SC1/project.html:603-606; references/references.json (entry shreve2004stochastic)", status="PASS",
         evidence="`tools/verify_refs.py --unit SC1` (live): 'live re-verification of SC1: 1 of 560 entries, 0 problems'. Entry: title 'Stochastic Calculus for Finance II', year 2004, used_by SC1, verified_by openlibrary. Page cites it at book level with no locator (:605). references/references.json has 0 entries matching Karatzas or 'Brownian Motion and Stochastic Calculus', so the page's statement that the second source has no record (:603) is true."),
    dict(id="SC1-d-privacy-claim", check="2.9 claim about the browser: nothing leaves the browser", location="course/modules/SC/SC1/project.html:279 ('saved in this browser as you type'), :620 (footer 'nothing you write leaves it')", status="UNVERIFIABLE",
         evidence="page_smoke confirms zero non-local requests during page load only. I did not drive the grader panel or the self-assessment form in a browser, so the save-as-you-type and no-submission claims are not checked.",
         fix="Run the grader panel with a network trace (type code, press run, reveal self-assessment) and confirm no request leaves the local origin; or soften the two sentences."),
    dict(id="SC1-d-tools-gates", check="gates: ruff, mypy, check tools, page_smoke", location="grader/*.py, tests/labs/SC1/*.py; repo", status="PASS",
         evidence="ruff check and ruff format --check on course/modules/SC/SC1/grader and tests/labs/SC1: all passed. mypy --no-incremental (repo config): 'Success: no issues found in 385 source files'. check_projects, check_pages, check_dag, run_labs (11/11), run_graders (50/50), page_smoke (project.html), verify_refs --unit SC1: all PASS."),
]

mutants = [
    dict(name="m01_reflection_factor_dropped", description="Reflection factor dropped: reflection_tail returns P(B_t >= a) with no factor 2.", killed_by="test_reflection_tail_is_the_erfc_closed_form[student seed]"),
    dict(name="m02_scale_sqrt_2t_became_sqrt_t", description="Scale confusion: reflection_tail uses sqrt(t) in the erfc argument instead of sqrt(2t).", killed_by="test_reflection_tail_is_the_erfc_closed_form[student seed]"),
    dict(name="m03_horizon_off_by_one", description="Horizon off by one: the grid maximum drops the final grid point (k <= n - 1 only).", killed_by="test_one_step_estimate_matches_the_one_step_gaussian_law"),
    dict(name="m04_lookahead_extra_point", description="Lookahead: the grid maximum includes one extra grid point beyond the horizon (n + 1 steps).", killed_by="test_fine_count_is_the_discrete_estimate_times_n"),
    dict(name="m05_standard_error_ignored", description="Standard error ignored: discrete_max_exceedance returns a standard error of 0.0 with a correct estimate.", killed_by="test_standard_error_uses_divisor_n_minus_one[student seed]"),
    dict(name="m06_divisor_n_not_n_minus_one", description="Divisor error: the sample variance of the indicators uses divisor N instead of N - 1.", killed_by="test_standard_error_uses_divisor_n_minus_one[student seed]"),
    dict(name="m07_nested_counts_swapped", description="Nested grids reversed: nested_grid_counts returns the coarse and fine counts in swapped order.", killed_by="test_coarse_count_never_exceeds_the_fine_count[8-4]"),
    dict(name="m08_level_doubled_in_tail", description="Level doubled: reflection_tail(a, t) is computed as reflection_tail(2 a, t).", killed_by="test_reflection_tail_is_the_erfc_closed_form[student seed]"),
    dict(name="m09_seed_zero_hard_coded", description="Hard-coded answer: discrete_max_exceedance returns the Lab 3 numbers whenever the instance seed is 0.", killed_by="test_estimate_is_a_fraction_of_the_paths[student seed]"),
    dict(name="m10_nonpositive_time_accepted", description="Invalid input accepted: reflection_tail returns 0.0 for t <= 0 instead of raising ValueError.", killed_by="test_reflection_tail_rejects_zero_time"),
    dict(name="m11_coarse_grid_shifted_by_one", description="Coarse grid off by one: samples steps 1, 1 + s, 1 + 2s, ... instead of s, 2s, ..., so it is not a subset of the fine grid.", killed_by="test_one_step_coarse_grid_tracks_the_terminal_law"),
    dict(name="m12_srw_strict_inequality", description="Strict inequality: srw_terminal_count counts S_n > a and drops the endpoint a itself.", killed_by="test_srw_counts_match_enumeration_for_n_up_to_12[1]"),
    dict(name="m13_divisibility_check_omitted", description="Divisibility check omitted: a coarse grid that does not divide the fine grid is silently accepted.", killed_by="test_coarse_grid_that_does_not_divide_fine_raises_value_error[4-3]"),
    dict(name="m14_srw_max_forgets_reflection_term", description="Reflection term forgotten: srw_max_count returns the endpoint count at a alone.", killed_by="test_srw_counts_match_enumeration_for_n_up_to_12[2]"),
    dict(name="m15_increment_scale_missing_square_root", description="Increment scale: the Gaussian increments use H / n as the standard deviation (square root missing).", killed_by="test_one_step_estimate_matches_the_one_step_gaussian_law"),
    dict(name="m16_nested_fine_zero_not_rejected", description="Named condition skipped: nested_grid_counts does not reject n_fine < 1 (no ValueError for an empty fine grid).", killed_by=None),
    dict(name="m17_nested_coarse_zero_not_rejected", description="Named condition skipped: nested_grid_counts does not reject n_coarse < 1 (the divisibility test alone runs).", killed_by=None),
]

n_pass = sum(r["status"] == "PASS" for r in rows)
n_fail = sum(r["status"] == "FAIL" for r in rows)
n_unv = sum(r["status"] == "UNVERIFIABLE" for r in rows)
killed = sum(1 for m in mutants if m["killed_by"])

fragment = {
    "unit": "SC1",
    "slice": "d",
    "round": 1,
    "verifier": "Haiku 5.5 independent verifier (slice d)",
    "pin": "1c1645f3",
    "base": "1c1645f3",
    "checkout": str(ROOT),
    "scratch": "/tmp/sc1d_work, /tmp/sc1d_twins, /tmp/sc1d_alt2, /tmp/sc1d_*.txt",
    "verified_at": "2026-11-04T12:00:00Z",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [
        "Curriculum second source 'Karatzas & Shreve, Brownian Motion and Stochastic Calculus, 2nd ed. (1991)' (curriculum/03-markets.yaml:524) has no admissible registry record (plan B2, review_queue.json entry ~line 1050). The page correctly omits it (project.html:603). Architect decision still open.",
    ],
    "freshness_flags": [],
    "notes": [
        f"Counts: {len(rows)} rows, pass={n_pass}, fail={n_fail}, unverifiable={n_unv}. Mutants {killed}/{len(mutants)} killed (17 total: plan 10 + verifier 5 + 2 named-condition mutants added after the first run).",
        "Scripts: ledgers/SC1/scripts/SC1-d-r1/ (make_mutants.py, make_alternatives.py, run_alternatives.py, recompute.py, instance_survey.py, exact_expected.py, write_fragment.py, plus alternatives/, alternatives_extra/, and output .txt files). Mutants: ledgers/SC1/mutants/.",
        "Alternative 2 at 4000 Simpson intervals passes with max abs error 5.0e-13 (margin 2x to the 1e-12 test). The 2000-interval variant fails: see SC1-d-ag-overconstraint.",
        "Exemplar B's P1 applies A4(b) to a path-valued Y; A4(b) (L05.html:60-61) allows any Y independent of G, so this is accepted.",
        "Not checked: the Pyodide run-time of the 115 tests (only page_smoke PASS); the grader panel's typed-code save path (SC1-d-privacy-claim); other lessons and pages of SC1 (slices a-c, e).",
        "Lab 2 page code differs from the twin only at the two intended blanks (page lines 33 and 36).",
    ],
    "summary": f"SC1 slice d (project.html, grader, project labs, mutants, alternatives): FAIL. {n_fail} FAIL, {n_unv} UNVERIFIABLE, {n_pass} PASS. Mutants {killed}/{len(mutants)} killed; 2 named-condition mutants survive. Five alternatives: 4 pass, alt 2 (4000 intervals) passes, a 2000-interval variant fails the grader's 1e-12 closed-form test.",
}

out = ROOT / "ledgers/SC1/SC1-d.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out, "rows", len(rows), "pass", n_pass, "fail", n_fail, "unv", n_unv, "mutants killed", killed, "/", len(mutants))
