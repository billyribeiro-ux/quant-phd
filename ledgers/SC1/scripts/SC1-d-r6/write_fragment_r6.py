"""Verifier round 6 (SC1 slice d): write the ledger fragment ledgers/SC1/SC1-d.json from the round-6 evidence.

Rows keep every round-5 id (VERIFIER_RULES: keep all row ids). Mutant entries are read from the mutate_graders
output of this round, so each killed_by is the test name the tool printed.
"""

import json
import re
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyE6-SC1-d")
OUT = ROOT / "ledgers/SC1/SC1-d.json"
G = "ledgers/SC1/scripts/SC1-d-r6/out"
MUT_TXT = (ROOT / G / "mutate_graders_SC1_0-9_r6.txt").read_text(encoding="utf-8")

mutants = []
for m in re.finditer(r"^(KILLED|SURVIVED) (m\d\d_\S+?\.py): (.*?) -> (.*)$", MUT_TXT, re.M):
    status, fname, desc, killed = m.groups()
    killed_by = None if killed.strip() == "None" else killed.strip()
    mutants.append({
        "id": fname[:-3],
        "description": desc.strip(),
        "file": f"ledgers/SC1/mutants/{fname}",
        "killed_by": killed_by,
    })
assert len(mutants) == 37, len(mutants)

R5_ROWS = [
    ("SC1-d-ladder", "2.6-ladder", "course/modules/SC/SC1/project.html:40-49, 155, 297-300, 602-609", "PASS",
     f"Re-read round 6. Four rungs in order at project.html:43-48; Lab 1 at :55; Lab 2 is <section class=\"lab completion\"> at :164; rung 3 spec at :213; stretch at :608. check_projects.py --unit SC1 -> 'check_projects SC1: PASS' ({G}/check_projects_SC1.txt)."),
    ("SC1-d-grading-mode", "2.6-grading", "course/modules/SC/SC1/project.html:225; curriculum/03-markets.yaml SC1 grading: both", "PASS",
     "project.html:225 'Both the autograder and the rubric apply'; check_projects.py (grading mode checked against the curriculum and the entry names both) PASS in " + G + "/check_projects_SC1.txt."),
    ("SC1-d-spec-signatures", "2.6-spec", "course/modules/SC/SC1/project.html:221 vs grader/starter.py:16-36", "PASS",
     "project.html:221 lists the five signatures; starter.py:16, 21, 26, 31, 36 carry the same names, parameter names and return types. Confirmed by reading both files in round 6."),
    ("SC1-d-spec-rounding-statement", "2.2-numbers / 2.9-prose", "course/modules/SC/SC1/project.html:223 vs :57-67, :142-160 and tests/labs/SC1/lab-SC1-project-1.py", "PASS",
     "project.html:223 states the rule (six decimals by Python formatting from the unrounded value; exponent form to three significant digits for a difference). Lab 1 prints with .6f and .2e (lab-SC1-project-1.py:145-149); recompute_r6.py (" + G + "/recompute_r6.txt) reproduces every printed value."),
    ("SC1-d-hours", "2.6-hours", "course/modules/SC/SC1/project.html:33, 274-280; course/modules/SC/SC1/index.html:29; L01-L08 data-hours", "PASS",
     "Table at project.html:274-280 sums to 2+3+10+8+3+2 = 28 (= data-hours-project 28 at :33 and index.html:29); hub lessons 72 = 8 x 9 (each L01-L08 line 2 is data-hours=9); 72+28=100. Own estimate: rung 1 about 1.5 h, rung 2 about 1 h, three proofs 8-10 h, engine 5-6 h, report 3 h, self-assessment 2 h; total about 22-26 h, within 30 % of 28."),
    ("SC1-d-spec-grid-table", "2.6-spec", "course/modules/SC/SC1/project.html:213-265, 433-445", "PASS",
     "Spec dl has context, inputs, required outputs, constraints, grading (213-226). Every question a student would ask was checked against the text: grid t_k (231), the draw call and order (232), nested grid (233), ValueError list (237), the n = 41 counting rule (223), instance keys (219, matching grader/instance.py:29-34). No clarifying question found."),
    ("SC1-d-spec-tolerance-statement", "2.6-spec", "course/modules/SC/SC1/project.html:234, 238; grader/test_project.py:145, 151, 305", "PASS",
     "project.html:234 states 1e-10 for the closed form; test_project.py:145 uses 1e-10; :151 uses 1e-8 for the quadrature (stated in the plan); :305 uses 1e-12 for the SE identity, a float identity not stated numerically on the page, which is consistent with the rule that the SE is the N-1 formula at :232."),
    ("SC1-d-ag-reference", "2.6-autograder", "course/modules/SC/SC1/grader/reference.py; tools/run_graders.py", "PASS",
     f"run_graders.py --unit SC1 --seeds 0-49 -> 'run_graders SC1: PASS (reference 50/50 seeds, slowest 0.5 s)' ({G}/run_graders_SC1_0-49.txt). reference_vs_lab3_r6.py reproduces every Lab 3 printed value ({G}/reference_vs_lab3_r6.txt)."),
    ("SC1-d-ag-starter", "2.6-autograder", "course/modules/SC/SC1/grader/starter.py", "PASS",
     "Starter run in a scratch copy of the grader: QF_SEED=0 pytest -q -p no:cacheprovider --assert=plain -W error test_project.py -> '125 failed, 4 passed' (out/suite_starter_seed0_r6.txt; the reference gives '129 passed', out/suite_reference_seed0_r6.txt). The four passes are instance tests that do not call the engine; the run_graders gate also checks that the starter fails."),
    ("SC1-d-ag-instances", "2.6-autograder", "course/modules/SC/SC1/grader/instance.py", "PASS",
     f"instances_r6.py ({G}/instances_r6.txt): 21 sampled seeds (20 random from 0-49, plus seed 0) all valid (label, ranges, n_steps*n_paths <= 200000); 21 distinct continuous tails; 49 distinct levels over seeds 0-49 (test requires >= 45)."),
    ("SC1-d-ag-count", "2.6-autograder", "course/modules/SC/SC1/grader/test_project.py; course/modules/SC/SC1/project.html:7, 225, 296", "PASS",
     f"pytest --collect-only -q on test_project.py: '129 tests collected' ({G}/collect_test_project_r6.txt). project.html:7, 225 and 296 each say 129."),
    ("SC1-d-ag-messages", "2.6-autograder", "course/modules/SC/SC1/grader/test_project.py:1-474", "PASS",
     "Read all 474 lines. Every ValueError test is for a condition the page names (must_raise: lines 179-197, 254-280, 373-394, 430-450); must_accept only for valid named inputs. Failure messages state the property (e.g. :145, :217, :305) and hold no computed value; no bare assert; __tracebackhide__ in the helpers."),
    ("SC1-d-ag-overconstraint", "2.6-autograder", "course/modules/SC/SC1/grader/test_project.py:400-449, 249-250; course/modules/SC/SC1/project.html:223", "PASS",
     f"Alternatives 1, 2, 3, 5, 6, 7, 8, 9 each pass seeds 0-49 ({G}/alternatives_sweep_0_49_r6.txt). Carried from round 5 (grader files and reference.py byte-identical between 7376a5e and 4bd8cb9): reference passes 3000/3000 seeds (ledgers/SC1/scripts/SC1-d-r5/out/sweep_reference_0_2999.txt). The n = 41 counts are tested without enumeration (:249-250)."),
    ("SC1-d-ag-alternatives-ok", "2.6-autograder", "ledgers/SC1/scripts/SC1-d-r6/alternatives/ (alt1, alt2, alt3, alt5, alt6, alt7, alt8, alt9)", "PASS",
     f"sweep_r6.py over seeds 0-49: each of the eight conforming alternatives 50/50 ({G}/alternatives_sweep_0_49_r6.txt). Different styles: statistics.NormalDist (alt1), Simpson-only tail (alt2), DP over (position, max) (alt3), cumsum with index subsampling (alt5), Pascal-row recurrence (alt6), step-major gauss draws (alt7), 1 - erf (alt8), closed-form SE (alt9). alt2b (enumeration at n = 41) is excluded: project.html:223 forbids listing the walks. alt4 (Box-Muller) is excluded as a mutant under FINAL-ARCHITECT-RULINGS 10, because project.html:232 states the gauss draw and test_project.py:332-336 pins it."),
    ("SC1-d-ag-mutants-plan", "2.6-mutation", "ledgers/SC1/mutants/m01-m10", "PASS",
     "Re-run mutate_graders.py --unit SC1 --seeds 0-9 (" + G + "/mutate_graders_SC1_0-9_r6.txt): m01-m10 KILLED, each with the test named there."),
    ("SC1-d-ag-mutants-own", "2.6-mutation", "ledgers/SC1/mutants/m11-m15, m18, m19, m21", "PASS",
     "Re-run: all KILLED (" + G + "/mutate_graders_SC1_0-9_r6.txt)."),
    ("SC1-d-ag-mutants-survivors", "2.6-mutation", "course/modules/SC/SC1/grader/test_project.py:440-455; ledgers/SC1/mutants/m16, m17", "PASS",
     "m16 killed by test_fine_grid_of_zero_steps_raises_value_error, m17 by test_coarse_grid_of_zero_steps_raises_value_error (" + G + "/mutate_graders_SC1_0-9_r6.txt)."),
    ("SC1-d-ag-mutants-seed", "2.6-mutation", "ledgers/SC1/mutants/m20; course/modules/SC/SC1/grader/test_project.py:356-365", "PASS",
     "m20 KILLED by test_draws_depend_on_the_instance_seed (seed 0) in the r6 run."),
    ("SC1-d-ag-mutants-seed-offset", "2.6-mutation", "ledgers/SC1/mutants/m22_seed_offset_by_one.py; project.html:232; test_project.py:332-336", "PASS",
     "m22 KILLED by test_one_step_draws_are_the_seeded_gaussians (seed 0) in the r6 run."),
    ("SC1-d-ag-mutants-r3", "2.6-mutation", "ledgers/SC1/mutants/m23-m26", "PASS", "All four KILLED in the r6 run."),
    ("SC1-d-ag-mutants-r4-new", "2.6-mutation", "ledgers/SC1/mutants/m27-m31", "PASS", "All five KILLED in the r6 run (m31 on seed 8)."),
    ("SC1-d-ag-mutants-r5-new", "2.6-mutation", "ledgers/SC1/mutants/m32, m33, m34", "PASS", "All three KILLED in the r6 run."),
    ("SC1-d-ag-page-smoke", "2.6-autograder", "course/modules/SC/SC1/project.html; tools/page_smoke.py --unit SC1 --pages project", "PASS",
     f"page_smoke.py alone on the project page -> 'page_smoke modules/SC/SC1/project.html: PASS'; in-browser grader 'All 129 tests pass on seed 1328640451' ({G}/page_smoke_SC1_project_r6.txt)."),
    ("SC1-d-ag-docstring", "2.6-autograder", "course/modules/SC/SC1/grader/test_project.py:1-18 vs the tests it describes", "PASS",
     "Each claim in the docstring checked against its test: shared-engine cross-checks (identity, one-step vs reflection_tail, nested vs discrete, coarse vs fine), the seed-0 draw pin (:332), the same-estimate repeat (:350), the band with the target SE (:79-82, :16-17). No claim is false."),
    ("SC1-d-rubric-observable", "2.9-prose", "course/modules/SC/SC1/project.html:446-457", "PASS",
     "Every level descriptor was read as an observable element. Descriptors that use a stated term (basis, separate paths, samples from the grid's law) are defined in the same rubric or the brief (C3 level 4 at :454 defines the basis). No vague descriptor found."),
    ("SC1-d-calib-A", "2.9-prose / 2.2-numbers", "course/modules/SC/SC1/project.html:464-466, 470-516 (exemplar A)", "PASS",
     "Scored blind from the passages with the rubric only: C1 1 (no numbered assumptions anywhere), C2 2 (the P1 symmetry step has no named reason), C3 2 (0.0865 and 0.0595 have no rounding statement), C4 2 (grid result presented as holding for every grid), C5 1 (no numbers). Official 1,2,2,2,1: within one level on every criterion."),
    ("SC1-d-exemplarA-claim", "2.9-prose", "course/modules/SC/SC1/project.html:470, 474-475, 482, 499, 503-508, 512", "PASS",
     "Exemplar A's numbers recomputed: tail 0.086497; one-step 0.059548 (se 0.010735), 0.0163 above 0.0432 = 1.52 se; 256-step tail-minus-estimate 0.004361 and 64-step -0.001799 (recompute_r6.txt). Its claims are the ones the annotations call wrong; the annotations are correct."),
    ("SC1-d-exemplarB-onestep-claim", "2.9-prose / 2.2-numbers", "course/modules/SC/SC1/project.html:558", "PASS",
     "Recomputed one-step bias 0.043248 = tail/2 (0.0432483); 0.026948 + 0.016300 = 0.043248; 0.016300 / 0.010735 = 1.518, printed 1.52 (recompute_r6.txt)."),
    ("SC1-d-exemplarB-numbers", "2.2-numbers", "course/modules/SC/SC1/project.html:524, 546, 558 vs lab output at :154-160 and :418-428", "PASS",
     "Every number in exemplar B equals a printed value of Lab 1 or Lab 3 (" + G + "/reference_vs_lab3_r6.txt and recompute_r6.txt): 0.086497; 9.13e-15 is Lab 1's printed Simpson difference (my own Simpson differs in the last digits, which the page does not claim); 0.059548, 0.010735, 0.048142; the five grid rows; nested 40, 35, 29, 27, 22; 1588 and 794."),
    ("SC1-d-exemplarB-proof", "2.4-proof / 2.9-prose", "course/modules/SC/SC1/project.html:582-595 (exemplar B appendix)", "PASS",
     "Re-derived every step of P1 (stopping-time property of rho, A = {tau <= t} = {M_t >= a} via IVT on [0,s], P(tau = t) = 0, B~ independent of F_rho by A3, A in F_rho, freezing by A4(b) with the bounded measurable f, P(B~_u < 0) = 1/2, and the final algebra P(A) = P(B_t >= a) + P(A)/2). P2 erfc substitution re-derived; P3 by continuity from below and erfc(0) = 1. No gap found."),
    ("SC1-d-exemplarB-p1-assumptions", "2.9-prose / 2.4-proof", "course/modules/SC/SC1/project.html:246, 249, 583-584 vs course/modules/SC/SC1/L05.html (A3, A4 block) and L06.html (Proposition 2.3 hypothesis)", "PASS",
     "Re-read in round 6 after the lesson delta: L05 A3 is for a bounded stopping time and states the conclusion the project uses (L05 Assumption A3 block, after the section 3 heading); A4(b) freezing, A4(c) hitting time, A4(g) joint measurability, A4(h) measurability at a stopping time, each as the project names them (L05 A4 block). L06 Proposition 2.3 is assumed for A3 and A4(b), A4(c), A4(g), A4(h) (L06.html:130)."),
    ("SC1-d-lab1-run", "2.5-labs", "course/modules/SC/SC1/project.html:55-160; tests/labs/SC1/lab-SC1-project-1.py", "PASS",
     f"run_labs.py --unit SC1 -> 'run_labs SC1: PASS (11/11)' ({G}/run_labs_SC1.txt). Twin is byte-identical to the page code (run_labs checks it); twin runs under python -I -W error with no stderr; output matches expected at 1e-6."),
    ("SC1-d-lab1-docstring", "2.5-labs / 2.9-prose", "course/modules/SC/SC1/project.html:58-68; tests/labs/SC1/lab-SC1-project-1.py:3-8", "PASS",
     "Docstring claims (four numbers drawn in the same order; closed form, Simpson and one-step estimate; six-decimal rounding; exponent form for the difference; H and a printed as generated) match the code (:90-95, :144-149) and the output."),
    ("SC1-d-lab2-run", "2.5-labs", "course/modules/SC/SC1/project.html:164-210; tests/labs/SC1/lab-SC1-project-2.py", "PASS",
     f"run_labs SC1 PASS ({G}/run_labs_SC1.txt). The page differs from the twin only at the two blanks (project.html:199 and :202 vs twin lines 33 and 36), which is the completion-lab convention (FINAL-ARCHITECT-RULINGS 11). Twin output equals the expected block (29, 22, 7, True)."),
    ("SC1-d-lab2-attribution", "2.9-prose / attribution", "course/modules/SC/SC1/project.html:209 vs course/modules/SC/SC1/L06.html (Proposition 1.3 at :75, Corollary 1.4 at :87, proof at :97)", "PASS",
     "Re-read after the L06 delta: Proposition 1.3 (discrete reflection identity) and Corollary 1.4 (discrete tail identity, proved from Proposition 1.3 at :97) are unchanged in statement. 'Tests check every n up to 12': test_project.py:213-238 parametrize n = 1..12. Identity re-checked for n <= 12 and all a (recompute_r6.txt: no failures)."),
    ("SC1-d-lab3-run", "2.5-labs", "course/modules/SC/SC1/project.html:303-430; tests/labs/SC1/lab-SC1-project-3.py", "PASS",
     f"run_labs SC1 PASS. Expected block (project.html:418-428) equals the twin output; recompute_r6.py and reference_vs_lab3_r6.py reproduce each value ({G}/recompute_r6.txt, reference_vs_lab3_r6.txt). Seeded RNG; no network; page_smoke lab time 0.2 s."),
    ("SC1-d-lab3-onestep-interp", "2.5-labs / 2.9-prose", "course/modules/SC/SC1/project.html:429 vs tests/labs/SC1/lab-SC1-project-3.py:99", "PASS",
     "Line 99 prints the tail minus each grid's estimate, including the one-step row (n = 1). project.html:429's reading (0.026948 estimates the one-step bias 0.043248 with error -0.016300, 1.52 se) is the arithmetic of those printed values (recompute_r6.txt)."),
    ("SC1-d-lab3-docstring", "2.5-labs / 2.9-prose", "tests/labs/SC1/lab-SC1-project-3.py:3-11 (page :306-317)", "PASS",
     "Docstring: draws per grid from random.Random(seed), path by path, step by step (code :359-369); estimate and SE definition (:375-379); coarse grids are every (256/n)-th point (:406-410); decimals to six places; integers for N and counts. All match the code."),
    ("SC1-d-labs-pytest", "2.5-labs / tooling", "tests/test_labs.py -k SC1; tests/test_run_labs.py; tests/test_page_checks.py; tests/test_memo_exemplars.py", "PASS",
     f"pytest -q tests/test_labs.py -k SC1 tests/test_run_labs.py tests/test_page_checks.py tests/test_memo_exemplars.py -> 11 passed, exit 0 ({G}/pytest_related_r6.txt)."),
    ("SC1-d-calib-B", "2.9-prose / rubric scoring", "course/modules/SC/SC1/project.html:518-599 (exemplar B)", "PASS",
     "Scored blind from the passages: C1 4 (each assumption listed and tied to its step, A3 applied to rho <= t), C2 4 (each step's reason named; no skipped step), C3 4 (each value's type and rounding rule stated), C4 3 (no statement of what the nested comparison leaves open about the continuum), C5 4 (every grid, direction from nested counts, SE at each). Official 4,4,4,3,4: within one level on every criterion."),
    ("SC1-d-statements", "2.6-spec / 2.4-proof", "course/modules/SC/SC1/project.html:241-262", "PASS",
     "P1, P2, P3 statements re-checked against L05 (A0 is Definition 1.1 of L01; A3 and A4 of L05) and L06 (Proposition 2.3, Theorem 2.5, Corollary 2.6) and L08 (Proposition 1.2, Corollary 1.3): each statement's hypotheses are listed and the claimed identities hold (P2 erfc form re-derived)."),
    ("SC1-d-A1-label", "2.6-spec / attribution", "course/modules/SC/SC1/project.html:236-242, 577-580; course/modules/SC/SC1/L01.html:58-63; L05.html", "PASS",
     "Definition 1.1 of Lesson 1 is at L01.html:58-63 (D1 B_0 = 0, D2 normal increments with variance equal to length, D3 independent increments), unchanged by the round-5-to-6 delta (the delta changed L01 lines 51, 77, 115, 215, 329, 336, 353, 434). project.html:242 'continuous paths as in Lesson 2' matches L02 (construction with continuous paths)."),
    ("SC1-d-A3-A4-usage", "2.6-spec / attribution", "course/modules/SC/SC1/project.html:242, 246, 249; course/modules/SC/SC1/L05.html (A3 block; A4 block items a-h)", "PASS",
     "Re-read in round 6 (L05 changed at lines 7, 63, 68, 94, 110, 147, 288, 350; the cited items are the same in substance). A3: strong Markov for stopping times, bounded case, conclusion matches (L05 section 3). A4(c) hitting-time stopping time, (h) measurability at a stopping time, (g) joint measurability, (b) freezing: as the project describes them. A4 'includes that the first hitting time of a closed set is a stopping time' (A4(c))."),
    ("SC1-d-dag", "2.7-DAG", "course/modules/SC/SC1/project.html; tools/check_dag.py --unit SC1", "PASS",
     f"check_dag.py --unit SC1 -> 'check_dag SC1: PASS' ({G}/check_dag_SC1.txt). Concept links on project.html (stopping-time, normal-distribution) are in the closure; no SDE, martingale or Brownian-bridge name is used by name (grep)."),
    ("SC1-d-notation", "2.8-notation", "course/modules/SC/SC1/project.html passim; notation/notation.json", "PASS",
     "Math macros used on the page (scan in round 6): Prob, Normal, indic, Phi, operatorname, mathcal, tilde, tau, rho, ... All registered macros are used with their registered meaning (Prob = probability measure; Normal; indic; Phi = standard normal CDF, notation.json symbol list). T appears only in the two sentences that say the horizon is not T (:230, :535). N (path count) is a lesson-local letter (notation.json 'about': N is defined where used)."),
    ("SC1-d-define-before-use", "2.5-labs / 2.9-prose", "course/modules/SC/SC1/project.html:37, 45, 53, 57, 230", "PASS",
     "Terms re-checked in order: running maximum (:37), simple random walk (:45), grid maximum (:37, :53), the statement of the Lab 1 band (:57 uses 'target standard errors', defined in the Lab 1 interpretation at :161 and in the twin, so the phrase is used before its formal definition on the page; the meaning is clear from the same sentence)."),
    ("SC1-d-discretization-bias", "2.9-prose", "course/modules/SC/SC1/project.html:225, 229, 235", "PASS",
     "The discretization bias is defined once, with a plain dfn at :235 (plan D9: no link, no concept). Its first use on the page is at :429 (Lab 3 interpretation), and the rubric criterion label 'C5 · Discretization' at :456 follows the definition. The phrase does not occur before :235."),
    ("SC1-d-monte-carlo-term", "2.9-prose", "course/modules/SC/SC1/project.html:231-232, 235, 375-379 (Lab 3 code)", "PASS",
     "Monte Carlo is not used as a named term on the page beyond 'simulation' and 'seeded simulation'; the estimates are described in plain words (:235, :238)."),
    ("SC1-d-scope-words", "2.9-prose", "course/modules/SC/SC1/project.html:217, 223, 231-238, 449, 570", "PASS",
     "Each scope word ('every', 'all', 'always', 'only', 'never') was checked: 'every grid point lies in [0,H]' (:231) and 'the coarse count is never larger ... pathwise' (:233) hold; 'every instance is SIMULATED' (:238) holds by construction; 'every case that meets their assumptions' (:570) matches P1-P3's hypotheses; no 'for every grid' claim is made as a statement on the page (only in the exemplar A that is marked wrong)."),
    ("SC1-d-process-words", "2.9-prose / 12", "course/modules/SC/SC1/project.html:619-622 (former round-4 location)", "PASS",
     "grep of the page's visible prose for verifier, builder, round, fixer, ledger, architect, ruling, planner, audit: no hit in learner text. 'I do not order them by bias' (:558) is the exemplar student's first-person report voice, not a process word."),
    ("SC1-d-banned-structure", "2.9-prose / structure", "course/modules/SC/SC1/project.html; tools/check_pages.py --unit SC1", "PASS",
     f"check_pages.py --unit SC1 -> 'check_pages SC1: PASS' ({G}/check_pages_SC1.txt): page contract, banned strings, claims, hub, lessons, cards."),
    ("SC1-d-registry", "2.8-references", "course/modules/SC/SC1/project.html:619-622; references/references.json (shreve2004stochastic)", "PASS",
     f"Registry record: title 'Stochastic Calculus for Finance II', author Shreve, year 2004, verified_by openlibrary (references/references.json). Reading line at project.html:621 matches. verify_refs.py --offline: 560 entries, 0 problems ({G}/verify_refs_offline_all.txt). verify_refs.py --unit SC1 (live): 1 of 560 entries, 0 problems ({G}/verify_refs_live_SC1_r6.txt)."),
    ("SC1-d-privacy-claim", "2.9-prose / attribution", "course/modules/SC/SC1/project.html:288, 603, 636", "PASS",
     "project.html:288 and :636 describe browser storage: grader.js:53 shows the seed 'derived from your workspace ID' (matching :219 and the page's claim); store.js:2 and :122-136 keep the workspace id and files in IndexedDB in the browser."),
    ("SC1-d-tools-gates", "tooling", "course/modules/SC/SC1/grader; tests/test_labs.py -k SC1 and the three related files; references", "PASS",
     f"Round-6 gates: run_labs SC1 (11/11), check_pages SC1, check_dag SC1, check_projects SC1, run_graders SC1 0-49, mutate_graders SC1 0-9 (40 files: 37 slice mutants plus 3 lab mutants SC1a-*, see notes), verify_refs offline and live, ruff check, ruff format --check (553 files), mypy --no-incremental (385 files, strict), pytest related files (11 passed). Outputs in {G}/."),
    ("SC1-d-numbers-prose", "2.2-numbers", "course/modules/SC/SC1/project.html:57, 154-160, 209, 219, 225, 305-317, 418-429, 470-512, 524-558", "PASS",
     f"Every number in prose recomputed independently by recompute_r6.py ({G}/recompute_r6.txt): tail, tail/2, Simpson closed-form agreement (both within 1e-14), grid estimates and SEs, nested counts, walk counts 29/22/7 and 1588/794, band 0.048142, ratios 1.52 and 0.14, 0.0163/0.0107 = 1.52."),
    ("SC1-d-spec-n41-method", "2.6-spec / 2.6-autograder", "course/modules/SC/SC1/project.html:223; grader/reference.py:79-85; ledgers/SC1/scripts/SC1-d-r6/alternatives/alt7_gauss_step_major.py", "PASS",
     "reference.py:79-85 uses math.comb for the terminal count; srw_max_count uses the reflection identity (:88-97). The page's 'n = 41 must not list the walks' (:223) is met: test_project.py:249-250 checks n = 41 without enumeration, and the reference passes it (run_graders 0-49)."),
    ("SC1-d-ag-draws-depend-overconstraint", "2.6-autograder", "course/modules/SC/SC1/grader/test_project.py:356-365 (test_draws_depend_on_the_instance_seed)", "PASS",
     "Passes for the reference and for every conforming alternative on seeds 0-49 (" + G + "/alternatives_sweep_0_49_r6.txt). The test is not over-constrained: any seed change alters at least one of five grid estimates at a = 1e-9."),
    ("SC1-d-ag-band-overconstraint", "2.6-autograder", "course/modules/SC/SC1/grader/test_project.py:76-82, 314-329, 418-425", "PASS",
     "The band uses the target SE (the docstring at :14-17 explains why). Alternatives 1-9 pass seeds 0-49 (" + G + "/alternatives_sweep_0_49_r6.txt), so the band is not too tight for conforming engines."),
    ("SC1-d-reading-disclosure", "2.9-prose / attribution", "course/modules/SC/SC1/project.html:619-622; course/modules/SC/SC1/index.html:183", "PASS",
     "index.html:183 (unchanged by the delta) says the second curriculum source is not cited; project.html:619-622 cites only shreve2004stochastic at book level, no passage or theorem number. Judgement row (round 5), re-read in round 6."),
    ("SC1-d-delta-r5-read", "2.9-prose / 2.6 (round-5 delta)", "course/modules/SC/SC1/project.html (hunks at :217, :232, :233, :246, :249, :261, :466, :570, :583, :590, :619); course/modules/SC/SC1/grader/test_project.py:356-365", "PASS",
     "The round-5 hunks are carried in project.html and grader/test_project.py, which are byte-identical between 7376a5e and 4bd8cb9 (git diff --quiet on those paths). Re-read in round 6 at each of the cited lines (project.html:217, 232, 233, 246, 249, 261, 466, 570, 583, 590, 619; test_project.py:356-365): the current text matches the round-5 reading."),
]

R6_NEW = [
    {
        "id": "SC1-d-ag-level-equality-survivors",
        "check": "2.6-mutation",
        "location": "course/modules/SC/SC1/grader/test_project.py (no test); ledgers/SC1/mutants/m35_grid_exceedance_strictly_above_level.py, m36_nested_counts_strictly_above_level.py",
        "status": "FAIL",
        "evidence": (
            "Two new student-error mutants written this round (ledgers/SC1/scripts/SC1-d-r6/make_mutants_r6.py), each a one-change copy of reference.py: m35 uses '>' for the grid indicator (discrete_max_exceedance), m36 uses '>' in both nested counts. "
            "mutate_graders.py --unit SC1 --seeds 0-9 (" + G + "/mutate_graders_SC1_0-9_r6.txt): 'SURVIVED m35_grid_exceedance_strictly_above_level.py ... -> None' and 'SURVIVED m36_nested_counts_strictly_above_level.py ... -> None'. "
            "The rule is stated at project.html:232 ('the fraction of paths whose grid maximum is at least a') and :233 ('the number of paths whose fine grid maximum is at least a and the number whose coarse maximum is'). "
            "They survive because no test puts the level exactly on a path's maximum. The probe " + G + "/tie_probe_r6.py sets a to the first draw v of random.Random(seed).gauss(0, sqrt(H)) (0.0 + v == v exactly) and requires the count of draws >= v: reference.py and all eight conforming alternatives pass seeds 0-19; m35 and m36 fail seeds 0-19 (" + G + "/tie_probe_r6.txt)."
        ),
        "fix": (
            "Add a test to course/modules/SC/SC1/grader/test_project.py (discrete_max_exceedance section): with level = the first draw v = random.Random(INST['seed']).gauss(0.0, sqrt(H)), and one grid step, assert that discrete_max_exceedance({**INST, 'a': v}, 1)[0] equals the count of the N draws >= v divided by N (within 1e-12), and that nested_grid_counts({**INST, 'a': v}, 1, 1)[0] equals that count. "
            "Then re-run tools/mutate_graders.py --unit SC1 --seeds 0-9: m35 and m36 must be KILLED; and re-run run_graders.py --unit SC1 --seeds 0-49 (reference and alternatives must still pass; tie_probe_r6.py is the reference check for this)."
        ),
    },
    {
        "id": "SC1-d-ag-mutants-r6-new",
        "check": "2.6-mutation",
        "location": "ledgers/SC1/mutants/m37_one_path_accepted_with_zero_error.py",
        "status": "PASS",
        "evidence": (
            "m37 (new this round): discrete_max_exceedance accepts one path and returns standard error 0.0, skipping the named n_paths < 2 check (project.html:237). KILLED by test_one_path_raises_value_error (seed 0) in " + G + "/mutate_graders_SC1_0-9_r6.txt. "
            "m35 and m36 are the failing row SC1-d-ag-level-equality-survivors."
        ),
    },
    {
        "id": "SC1-d-exemplar-naming",
        "check": "2.9-prose / plan naming",
        "location": "course/modules/SC/SC1/project.html:464, 518; plans/SC1-build-plan.md section 5.4",
        "status": "PASS",
        "evidence": (
            "The page labels exemplar-a as data-level=\"2\" (:464) and exemplar-b as data-level=\"4\" (:518). plans/SC1-build-plan.md section 5.4 names exemplar-a data-level 4 and exemplar-b data-level 2. "
            "Both exemplars are at two levels (check_projects SC1 PASS requires two or more), the scores match the passages (calibration rows), and no learner-facing requirement depends on the names. Recorded as a note for the builder; not a failing row."
        ),
    },
    {
        "id": "SC1-d-delta-r6-read",
        "check": "2.9-prose / 2.6 (round-6 delta)",
        "location": "course/modules/SC/SC1/project.html; grader/*; tests/labs/SC1/lab-SC1-project-*.py; tools/; references/; notation/; ledgers/SC1/mutants/m01-m31",
        "status": "PASS",
        "evidence": (
            "git diff --name-only 7376a5e 4bd8cb9: the slice's own subjects (project.html, grader/ four files, the three project labs, the test infrastructure, tools/, references/, notation/, mutants m01-m31) are byte-identical (git diff --quiet on those paths, excluding files added after 7376a5e). "
            "Files that changed and are cited by this slice were read in full at their cited lines: L01.html (51, 58-63, 77), L05.html (A3 and A4 blocks, 63, 68), L06.html (75, 87, 97, 130), L08.html (63, 77, 83), index.html (33, 72, 183). None of the cited statements changed in substance."
        ),
    },
]


def fix_for(row_id: str) -> str:
    return ""


rows = []
for rid, check, loc, status, ev in R5_ROWS:
    rows.append({"id": rid, "check": check, "location": loc, "status": status, "evidence": ev})
rows += R6_NEW

for r in rows:
    if r["status"] != "PASS":
        assert r.get("fix"), r["id"]

fragment = {
    "unit": "SC1",
    "slice": "d",
    "round": 6,
    "verifier": "Claude Haiku 5.5, independent verifier for SC1-d, round 6 (did not build SC1; re-verified the round-5 pin delta and every command row on 4bd8cb9)",
    "pin": "4bd8cb94a8e171e80c4c34da1b3f32be7cb93f07",
    "base": "7376a5e216c1e6d99becc76b4cd64028f5b55d3f (round-5 pin); delta 7376a5e..4bd8cb9 read for the slice",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE6-SC1-d",
    "scratch": "/tmp/sc1d_r6_suite (grader copy for collect and starter runs); /tmp/sc1d-r6-* (probe and sweep scratch, removed after each run)",
    "verified_at": "2026-11-04T20:43:19+00:00",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "Verdict FAIL: one row (SC1-d-ag-level-equality-survivors). Two new mutants (m35, m36) that use a strict '>' where project.html:232-233 says 'at least a' survive the suite; a probe (" + G + "/tie_probe_r6.py) shows the reference and all eight conforming alternatives pass a tie test that m35 and m36 fail. "
        "Alternatives: eight conforming alternatives pass seeds 0-49 (50/50 each); alt2b (enumeration at n = 41) is excluded because project.html:223 forbids listing walks at n = 41; alt4 (Box-Muller) is excluded as a mutant under FINAL-ARCHITECT-RULINGS 10, since project.html:232 states the gauss draw and test_project.py:332-336 pins it. The plan's section 5.7(4) asks for a Box-Muller alternative; the architect should confirm that the exclusion stands. "
        "Mutants: mutate_graders.py reports 40 files in ledgers/SC1/mutants: the 37 listed here (m01-m37) plus three lab-twin mutants SC1a-lab-mut1..3 (slice a's files; all three KILLED by the project suite, not counted in this fragment). Lab twins are not mutation-tested (FINAL-ARCHITECT-RULINGS 9; project.html has no claim that a lab checks those properties). "
        "Reference sweeps: 0-49 re-run this round; 0-2999 carried from round 5 (byte-identical grader and reference). "
        "Not checked: the in-browser grader panel UI and self-assessment form (only page_smoke's Pyodide run); live localStorage; exemplar scoring was done from the passages with the rubric, not blind to the annotations in a separate reader; the 240 s enumeration timing for alt2b was not repeated; seeds beyond 2999 for the draws test; the Box-Muller alternative as a conforming engine (excluded as above)."
    ),
    "summary": "",
}

n_pass = sum(1 for r in rows if r["status"] == "PASS")
n_fail = sum(1 for r in rows if r["status"] == "FAIL")
n_unv = sum(1 for r in rows if r["status"] == "UNVERIFIABLE")
killed = sum(1 for m in mutants if m["killed_by"])
fragment["summary"] = (
    f"SC1 slice d round 6 (project.html, grader, project labs, mutants, alternatives): FAIL. Rows: {len(rows)} "
    f"({n_pass} PASS, {n_fail} FAIL, {n_unv} UNVERIFIABLE). Mutants: {killed}/{len(mutants)} killed; m35 and m36 survive "
    "(strict '>' against 'at least a', project.html:232-233). Round-5 PASS rows re-verified this round, with the same ids."
)
OUT.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", OUT, "rows", len(rows), "mutants", len(mutants), "killed", killed)
