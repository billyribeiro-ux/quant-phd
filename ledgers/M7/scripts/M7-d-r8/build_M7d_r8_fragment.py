"""Round-8 M7-d fragment builder (verifier-written). Parses the mutant log and writes ledgers/M7/M7-d.json.

Usage: python -I build_M7d_r8_fragment.py <repo-root>
"""
import json
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
S = root / "ledgers/M7/scripts/M7-d-r8"
G = "course/modules/M/M7/grader/test_project.py"
P = "course/modules/M/M7/project.html"

rows = [
 dict(id="PRJ-D1-01", check="2.6-spec", location="course/modules/M/M7/grader/instance.py:14-68; project.html:292-295", status="PASS",
      evidence=f"{S}/instances_labs_r8.py output: asset counts {{3: 18, 4: 14, 5: 18}} over seeds 0-49, 50 of 50 distinct payloads, invalid seeds []; each case checked for symmetric Sigma, positive definite pivots, box and budget and sector caps feasibility, two sectors each non-empty; run_graders.py --unit M7 --seeds 0-49 PASS (reference 50/50, log run_graders_M7_0-49.log)."),
 dict(id="PRJ-D1-02", check="2.6-spec", location=f"{P}:299-300; {G}:127-154", status="PASS",
      evidence="output_shape keys/lengths/types re-read (test_project.py:127-154); reference passes 50/50 seeds (run_graders_M7_0-49.log); collect-only 364 on each seed (collect_all_seeds.log)."),
 dict(id="PRJ-D1-03", check="2.4-math", location=f"{P}:309", status="PASS",
      evidence="Re-derived both directions of the linearization: t_i = |d_i| satisfies t_i >= d_i, t_i >= -d_i and sum t_i <= tau when sum|d_i| <= tau; conversely sum|d_i| <= sum t_i <= tau. Checked by hand; no numeric claim on this line."),
 dict(id="PRJ-D1-04", check="2.4-math", location=f"{P}:310-313", status="PASS",
      evidence="Re-derived from the Lagrangian of L03 Definition 1.2 (L = f + sum lambda_j g_j): w-stationarity gamma(Sigma w)_i - mu_i + nu - lambda^l_i + lambda^u_i + eta_k(i) + alpha_i - beta_i; t-stationarity kappa - alpha_i - beta_i; the page's g_j list (page:310) gives these signs. Matches reference.py:305-308 and test_project.py stationarity() (lines 86-104)."),
 dict(id="PRJ-D1-05", check="2.4-math", location=f"{P}:310, 314-319; {G}:69-83", status="PASS",
      evidence="Inequality list g_j (page:310: l-w, w-u, sector minus cap, d-t, -d-t, sum t - tau) matches inequality_pairs() exactly; four certificate definitions (page:315-318) match recomputed_certificate() (test_project.py:107-118)."),
 dict(id="PRJ-D1-06", check="2.4-math", location=f"{P}:320", status="PASS",
      evidence="Claim 'the floor changes its value only when every inequality multiplier is positive' re-derived: unfloored value is -min(multipliers); it differs from the floor only when min > 0. 'Fails only when the smallest multiplier exceeds 1e-9': the agreement tolerance is 1e-9 (test_project.py:387). Degenerate multiplier set with all inequality multipliers positive: lower (0.5, 0.5), upper (0.55, 0.35), sector 0.05, alpha = beta = 1, kappa = 2 satisfies all stationarity equations for the case of test_project.py:259-264 (exact check in ledgers/M7/scripts/M7-d-r8/degenerate_multipliers_r8.log: r_w = r_t = 0, all multipliers positive, smallest 1/20)."),
 dict(id="PRJ-D1-07", check="2.4-math", location=f"{P}:317-321; {G}:107-118", status="PASS",
      evidence="Primal, dual (with floor), complementary-slackness and stationarity definitions re-derived; reference.py _certificate (lines 262-315) computes the same four quantities in exact arithmetic; the suite recomputes them independently; reference agreement within 1e-9 on 50 seeds (run_graders log)."),
 dict(id="PRJ-D1-08", check="2.4-math", location=f"{P}:322-325 (Proposition and proof, now line 324 for the extension step)", status="PASS",
      evidence="Round-7 gap closed: page:324 now states that every feasible y extends to (y, s) with s_i = |y_i - w0_i|, by the linearization equivalence of page:309, and applies the bounds to (w', t') in the uniqueness step. Each step re-derived: L convex (f convex, lambda >= 0, constraints affine), stationarity gives the minimum of L, f(y) >= L(y,s) >= L(w,t) = f(w), midpoint argument for uniqueness. Non-blocking nit: the clause 'Since f is differentiable and convex, each g_j is affine' attributes affineness to f; it comes from the affine-constraints hypothesis, so the proof is complete."),
 dict(id="PRJ-D1-09", check="2.4-math", location=f"{P}:325; course/modules/M/M7/grader/instance.py:38-43", status="PASS",
      evidence="Sigma = (A'A + I)/1000 with integer A (instance.py:38-41) gives x'Sigma x = (|Ax|^2 + |x|^2)/1000 > 0 for x != 0, so the instances are strictly convex as the page states; the page's 'existence of multipliers is not proved here' is an honest scope statement."),
 dict(id="PRJ-D1-10", check="2.6-spec", location=f"{P}:326; course/modules/M/M7/grader/reference.py:54-109", status="PASS",
      evidence="Each refusal condition on page:326 is coded in reference._parse (ValueError for mapping, missing field, no assets, list length, symmetry, positive definiteness, gamma, turnover limit, bound order, starting-portfolio checks, sector label range, sector without asset); bool and float sector labels and non-numbers raise TypeError (other invalid input, accepted by any exception)."),
 dict(id="PRJ-D1-11", check="2.6-spec", location=f"{G}:590-604 (NAMED_CONDITIONS), :707-730 (OTHER_SIDE_REFUSED)", status="PASS",
      evidence="Each named condition has an invalid mutation refused with ValueError and a valid mutation accepted (tests run 50/50 on reference; the other-side list covers the opposite direction and later positions)."),
 dict(id="PRJ-D1-12", check="2.6-spec", location=f"{P}:326, 332; {G}:627-633 (EXACT_BOUNDARIES), :940-1053", status="PASS",
      evidence="Boundary values named on the page (bound or cap equal to start, start sum inside 1e-9 on either side, turnover limit 0, gamma 1e-6) are exercised as accepted inputs; reference passes all of them."),
 dict(id="PRJ-D1-13", check="2.5-lab", location=f"{P}:53-168; tests/labs/M7/lab-M7-project-1.py", status="PASS",
      evidence="run_labs.py --unit M7: PASS 11/11 (run_labs_M7.log); page_labs_r8.py: page code == twin (True), twin exit 0 under python -I -W error, output == expected block (True). Interpretation claims (budget-only 54/65, 5/26, -3/130; answer 9/11, 2/11, 0; nu -21/1100; lambda 9/1100; objective -3/220) re-derived in instances_labs_r8.py."),
 dict(id="PRJ-D1-14", check="2.5-lab", location=f"{P}:170-285; tests/labs/M7/lab-M7-project-2.py", status="PASS",
      evidence="page_labs_r8.py diff: page code differs from the twin only at the three blanks (step 4 residual, step 6 signs and dual_feasible), as the hypothesis states; the twin's output equals the expected block (True); interpretation sentences consistent with the code."),
 dict(id="PRJ-D1-15", check="2.5-lab", location=f"{P}:372-445; tests/labs/M7/lab-M7-project-3.py", status="PASS",
      evidence="page_labs_r8.py: page code == twin, output == expected block. Independent recomputation (instances_labs_r8.py): check A all zero; check B stationarity 9/550 and dual 9/1100; check C stationarity 1/6250; the interpretation's 'twice the multiplier' (9/550 = 2 x 9/1100) holds."),
 dict(id="PRJ-D1-16", check="2.9-structure", location=f"{P}:33, 338-354; course/modules/M/M7/index.html:29-42; curriculum/curriculum.json (M7 hours 110)", status="PASS",
      evidence="Hub data-hours-lessons=77 and data-hours-project=33; 77+33 = 110 = curriculum M7 hours; 33/110 = 30%. Hub lesson split (three lessons 9 h, five 10 h) sums to 77."),
 dict(id="PRJ-D1-17", check="2.9-structure", location=f"{P}:40-49", status="PASS",
      evidence="Ladder: rung 1 solved and annotated (Lab 1), rung 2 completion (Lab 2), rung 3 spec plus autograder (Lab 3 check), rung 4 open-ended stretch (page:453-460)."),
 dict(id="PRJ-D1-18", check="2.9-structure", location=f"{P}:288-336", status="PASS",
      evidence="Spec sections Context, Inputs, Required outputs, Conventions, Constraints, Grading, Reading list present. Questions a student would have: (a) the tolerance for the symmetry test of sigma is not stated; the suite refuses an asymmetry of 1e-4 and accepts exact symmetry, so any tolerance below 1e-4 passes; recorded in notes, not a row failure."),
 dict(id="PRJ-D1-19", check="2.9-structure", location="course/modules/M/M7/grader/ (instance.py, reference.py, test_project.py, starter.py)", status="PASS",
      evidence="All four files exist and are referenced by the grader panel (project.html:359, data-suite/support/starter/solution); check_projects.py --unit M7 PASS (check_projects_M7.log)."),
 dict(id="PRJ-D1-20", check="2.9-structure", location=f"{P}; tools/page_smoke.py", status="PASS",
      evidence="page_smoke.py --unit M7 --pages project: PASS (page_smoke_project.log): zero errors on the page, lab timings 0.0 s each, in-browser grader on the reference: 'All 364 tests pass'."),
 dict(id="PRJ-D1-21", check="2.4-notation", location=f"{P}; notation/notation.json; labs", status="PASS",
      evidence="notation_check_r8.py: project.html and the three project labs use no registered macro (\\\\E, \\\\R, \\\\Prob, ...) and no registered symbol (T, \\\\Phi, \\\\gamma_3, \\\\gamma_4, R^\\\\ast, R^{e\\\\ast}, R_f, \\\\mathbb{Q}); the Greek letters used (gamma, mu, Sigma, nu, lambda, eta, alpha, beta, kappa, tau) are locally defined on page:305-310, as notation.json 'about' allows."),
 dict(id="PRJ-D1-22", check="2.9-structure", location=f"{P}:456; course/concepts.html; curriculum M2 introduces", status="PASS",
      evidence="envelope-theorem is introduced by M2 (curriculum.json M2 introduces list; plans/M7-build-plan.md:47) and M2 is a prerequisite of M7 (curriculum M7 prereqs ['M2','M3']); check_dag.py --all PASS (check_dag_all.log)."),
 dict(id="PRJ-D1-23", check="2.9-prose", location=f"{P}; tests/labs/M7/lab-M7-project-*.py", status="PASS",
      evidence="grep for process words (round, verifier, builder, agent, Claude, LLM) over project.html and the project labs: no hits; check_pages.py --unit M7 PASS (check_pages_M7.log)."),
 dict(id="PRJ-D1-24", check="2.6-spec", location=f"{P}:364-366", status="PASS",
      evidence="Ran the page's local command on a copy of the reference: QF_SEED=7 pytest -q -p no:cacheprovider --assert=plain -W error test_project.py -> 364 passed (run in a scratch dir with the page's file names)."),
 dict(id="PRJ-D1-25", check="2.6-autograder", location="course/modules/M/M7/grader/starter.py:18-20", status="PASS",
      evidence="starter.allocate raises NotImplementedError as the page states (starter.py:20); run_graders.py --unit M7 reports no 'starter passes the suite' problem (run_graders_M7_0-49.log)."),
 dict(id="PRJ-D1-26", check="2.6-autograder", location="course/modules/M/M7/grader/instance.py:14-68", status="PASS",
      evidence="make_instance is deterministic (random.Random seeded by string) and returns valid cases for seeds 0-49 (instances_labs_r8.py); test_instance_is_simulated_and_deterministic passes."),
 dict(id="PRJ-D1-27", check="2.6-autograder", location=f"{G}:36-44; reference.py:20-21", status="PASS",
      evidence="TOL = 1e-8 (test_project.py:37), agreement 1e-9 (lines 387, 432), starting-portfolio tolerance 1e-9 (reference.py:21) match page:321 and page:326."),
 dict(id="PRJ-D1-28", check="2.6-autograder", location=f"{G} (every assert message)", status="PASS",
      evidence="Every assert message is a fixed property sentence, with the case name or asset index only (e.g. test_project.py:427); no message interpolates an expected value; with --assert=plain only the message and the source line are shown."),
 dict(id="PRJ-D1-29", check="2.6-autograder", location=f"{G}; course/assets/js/py-worker.js", status="PASS",
      evidence="Same suite passes in the in-browser Pyodide grader (page_smoke: 364 pass), in a Node-hosted copy of the vendored Pyodide (pyodide_durations_r8.mjs: 364 passed) and locally (pytest, 364 passed)."),
 dict(id="PRJ-D1-30", check="2.5-lab", location="tests/labs/M7/lab-M7-project-1..3.py; tests/test_labs.py", status="PASS",
      evidence="pytest -q tests/test_labs.py -k M7: 11 passed (pytest_M7_r8.log)."),
 dict(id="PRJ-D1-31", check="2.6-spec", location=f"{P}:332; {G}:227-265", status="PASS",
      evidence="Collect-only on seeds 0-49 with reference copied to scratch: '364 tests collected' on every seed (collect_all_seeds.log); HAND_CASES has six entries (budget only, zero turnover, single asset, upper bound binding, turnover binding, degenerate box). The round-7 count of 363 is corrected."),
 dict(id="PRJ-D1-32", check="2.6-atlas", location=f"{P}; curriculum.json M7 entry", status="PASS",
      evidence="Not applicable: the curriculum M7 entry has no atlas key or link (grep 'atlas' over the M7 entry: no match) and project.html has no atlas reference (grep count 0)."),
 dict(id="PRJ-D1-33", check="2.1-citations", location=f"{P}:465-466; references/references.json", status="PASS",
      evidence="verify_refs.py --unit M7 (live): 'live re-verification of M7: 2 of 560 entries, 0 problems' (verify_refs_M7_online_r8.log); verify_refs --offline: 560 entries, 0 problems (verify_refs_offline.log). The reading list makes no claim about content (page:334), so no locator is required."),
 dict(id="PRJ-D1-34", check="2.9-structure", location=f"{P}:344-350", status="PASS",
      evidence="Hours table: 2 + 3 + 10 + 6 + 7 + 5 = 33; 'Total 33' row matches data-hours-project=33. Design-target ruling: only arithmetic consistency is checked; the independent estimate (about 30 to 38 h) is within 30 percent."),
 dict(id="PRJ-D1-35", check="2.6-mutation", location="ledgers/M7/mutants/ (177 pre-existing files)", status="PASS",
      evidence="mutate_graders.py --unit M7 --seeds 0-9 (mutate_M7_0-9_r8.log): 177/177 KILLED, 0 SURVIVED, exit 0. Run before the three new mutants were added (see the v8 rows)."),
 dict(id="PRJ-D1-36", check="2.6-mutation", location="ledgers/M7/mutants/f6_*, g2_*, m*, p*, q*, r*, r13_*, r14_*", status="PASS",
      evidence="Every family killed in mutate_M7_0-9_r8.log (e.g. f6_01..f6_10 killed by test_output_has_the_three_fields_and_frozen_names and multiplier-type tests; r7_06 killed by the degenerate hand case, see PRJ-R7-01)."),
 dict(id="PRJ-D1-37", check="2.6-mutation", location="ledgers/M7/mutants/ (equivalence)", status="PASS",
      evidence="No mutant in the folder is marked equivalent; v6_01 and v6_02 are absent from the folder (ls), and no page sentence depends on them. Nothing to prove."),
 dict(id="PRJ-D1-38", check="2.6-autograder", location="ledgers/M7/scripts/M7-d-r8/alt/ (altA, altB, altC..altH, alt_float); altr8/ (altV1..altV5)", status="PASS",
      evidence="Five correct alternatives pass 50/50 seeds: exact altA and altB (alts_run_0-49.log) and float relative-cutoff altV1, altV2, altV4 (altr8_run_0-49.log, 50 of 50 clean each), including gamma 1e-6 and 1e-9 boundaries. Defective alternatives fail page-named valid inputs through their own cutoffs or missing polish (clean seeds of 50: altC 38, altD 43, altE 42, altG 41, altH 44, alt_float 35, altV3 41, altV5 42; e.g. alts_run_0-49.log 'altC_float_tight_1e-12.py seed=7 :: 2 failed' with gamma 1e-6 rows). Relative-scaled float methods altV1, altV2, altV4 pass gamma 1e-9 and 1e-6 on all 50 seeds, so the grader does not over-constrain."),
 dict(id="PRJ-D1-39", check="2.9-structure", location="course/modules/M/M7/grader/reference.py; BLUEPRINT.md:400-401; plans/M7-build-plan.md:408 (T6); .github/workflows/ci.yml; tools/build_site.py", status="FAIL",
      evidence="BLUEPRINT.md:400-401 and plan T6 require deployment to exclude every grader/reference.py. The repo still has no such exclusion: no deployment configuration (no vercel.json, netlify.toml, wrangler.toml, Dockerfile, railway config), ci.yml has no deploy job, .gitignore excludes only course/assets/vendor/*, build_site.py has no exclusion, and course/modules/M/M7/grader/reference.py sits in the published course/ tree. Repo-level gap, outside this unit.",
      fix="Add the publication exclusion for course/**/grader/reference.py to the deployment configuration, or a build step that removes it from the published tree, and state it in the repo (BLUEPRINT.md:400-401; plan T6)."),
 dict(id="PRJ-R4-01", check="2.9-prose", location=f"{G} (docstrings and messages, e.g. :383-389, :401-405)", status="PASS",
      evidence="Re-read every docstring and assert message this round; no claim that the suite does not make, no value leak."),
 dict(id="PRJ-R5-01", check="2.4-math", location=f"{P}:456 (frontier bullet)", status="PASS",
      evidence="The stretch asks the student to state the sign convention; the page asserts no numeric result. With the page's Lagrangian convention (nu(sum w - b)), the envelope relation would be df*/db = -nu; the page does not assert it, so there is no error."),
 dict(id="PRJ-R5-02", check="2.6-spec", location=f"{G} (comments and messages; comment near :248, message near :346-348)", status="PASS",
      evidence="Every test comment and message re-read; only the two comments fixed in round 7 (PRJ-R7-02, PRJ-R7-03) were wrong, and both are now correct."),
 dict(id="PRJ-R5-03", check="2.9-prose", location=f"{P}:450", status="PASS",
      evidence="'No case reads a data file, and every case carries the SIMULATED label': instance.py:57 label string; no data reads in test_project.py or reference.py."),
 dict(id="PRJ-R5-04", check="2.9-structure", location=f"{P}:349-350", status="PASS",
      evidence="Hours total sentence and the 77 + 33 = 110 statement match the hub (index.html:29, 39-42) and curriculum (110)."),
 dict(id="PRJ-R5-05", check="2.6-mutation", location="ledgers/M7/mutants/r5_01..r5_05", status="PASS",
      evidence="All five killed in mutate_M7_0-9_r8.log (177/177)."),
 dict(id="PRJ-R6-01", check="2.6-gate", location="tools/check_projects.py", status="PASS",
      evidence="check_projects.py --unit M7: 'check_projects M7: PASS', exit 0 (check_projects_M7.log). Re-run this round."),
 dict(id="PRJ-R6-02", check="2.6-gate", location="tools/check_pages.py", status="PASS",
      evidence="check_pages.py --unit M7: 'check_pages M7: PASS', exit 0 (check_pages_M7.log). Re-run this round."),
 dict(id="PRJ-R6-03", check="2.9-dag", location=f"{P}; tools/check_dag.py", status="PASS",
      evidence="check_dag.py --all: every unit PASS, exit 0 (check_dag_all.log). Re-run this round."),
 dict(id="PRJ-R7-01", check="2.6-mutation", location=f"{G}:259-264 (degenerate box hand case); ledgers/M7/mutants/r7_06_*.py", status="PASS",
      evidence="Round-7 surviving mutant r7_06 is now KILLED (mutate_M7_0-9_r8.log: 'KILLED r7_06 ... -> test_hand_case_matches_its_worked_answer[degenerate ...]'). The degenerate hand case is present in HAND_CASES."),
 dict(id="PRJ-R7-02", check="2.9-prose", location=f"{G}:248-249 (comment on the upper bound binding case)", status="PASS",
      evidence="Re-derived: with the second upper bound removed the budget-only answer (0.35, 0.65) has turnover 0.9 > 0.5, so the turnover limit binds at (0.55, 0.45); with the bound, (0.7, 0.3), turnover 0.2 slack. The comment now says exactly this."),
 dict(id="PRJ-R7-03", check="2.9-prose", location=f"{G}:872-875 (comment before POSITIONS)", status="PASS",
      evidence="Checked against the code: only the starting-sum and lower-bound tests call _make_room or raise the upper bound; upper-bound tests change only the bound (test_project.py:912-937). The comment now matches."),
 dict(id="PRJ-R7-04", check="2.6-mutation", location="ledgers/M7/mutants/r7_01..r7_05", status="PASS",
      evidence="All five killed (mutate_M7_0-9_r8.log)."),
 dict(id="PRJ-R7-05", check="2.6-autograder", location=f"{G} (per-test time in Pyodide)", status="PASS",
      evidence="Measured this round: pyodide_durations_r8.mjs loads the vendored course/assets/vendor/pyodide, installs pytest, runs the suite with the reference on seed 0: 364 passed, total 1.27 s, max single-test call 0.008 s (slowest 0.008 s). Under BUILDER_RULES 5.3 (5 s per test, 60 s per suite). Caveat: Node-hosted Pyodide, not the browser."),
 dict(id="PRJ-R7-06", check="2.8-data", location=f"{P}; course/modules/M/M7/grader/instance.py", status="PASS",
      evidence="No dataset, download or figure on the page; the case is generated and labelled SIMULATED (instance.py:57)."),
 dict(id="PRJ-R7-07", check="2.6-hours", location=f"{P}:344-350", status="PASS",
      evidence="Same arithmetic as PRJ-D1-34: 33 = 2+3+10+6+7+5; design-target ruling applies."),
 dict(id="PRJ-R8-01", check="2.6-autograder", location=f"{G}:1068-1074 (test_allocate_prints_nothing_and_warns_nothing); {P}:327 (page sentence 'It does not print, does not emit warnings')", status="FAIL",
      evidence="Student error v8_01 (ledgers/M7/mutants/v8_01_prints_a_debug_line_on_zero_turnover.py) prints a debug line when the turnover limit is zero. It SURVIVES seeds 0-9 (v8_mutants_r8.log). Page:327 states the silence property for every input, but the silence test runs allocate only on the seed case (case_copy()), so an input-specific print is never seen. Captured-output check: the hand-case and boundary tests do not capture stdout.",
      fix="Make the silence check cover every allocate call: run each hand case (HAND_CASES), each named and boundary case, and the wrong-type and non-finite cases inside contextlib.redirect_stdout and warnings.catch_warnings(record=True) and assert the buffer is empty and no warning was recorded; or wrap allocate in one helper used by all the tests that call it."),
 dict(id="PRJ-R8-02", check="2.6-autograder", location=f"{G}:1061-1065 (test_allocate_does_not_change_its_argument); {P}:327 ('does not change its argument')", status="FAIL",
      evidence="Student error v8_02 (ledgers/M7/mutants/v8_02_normalizes_the_starting_weights_in_place.py) rescales instance['w0'] in place when the starting sum is not exactly one. It SURVIVES seeds 0-9 (v8_mutants_r8.log). The purity test runs only on the seed case, and all 50 seed cases have float sum(w0) == 1 exactly (instances_labs_r8.log: 'seed cases with float sum(w0) == 1 exactly: 50 of 50'), so the mutation never fires there; it fires on the starting-sum boundary inputs (test_project.py:901-908, 890-899) whose arguments are never compared with a copy. Page:327 is universal.",
      fix="In the boundary and named-condition tests (test_named_condition_boundary_is_accepted, test_named_exact_boundary_is_accepted, test_start_sum_inside_tolerance_is_accepted_at_every_position, test_start_on_or_inside_a_bound_is_accepted_at_every_position, test_start_sector_cap_on_or_inside_its_limit_is_accepted, the hand cases) deep-copy the argument before the call and assert it is unchanged afterwards, as test_allocate_does_not_change_its_argument does for the seed case."),
 dict(id="PRJ-R8-03", check="2.6-mutation", location="ledgers/M7/mutants/v8_03_budget_multiplier_zero_when_start_is_optimal.py", status="PASS",
      evidence="Student error v8_03 (hard-codes the budget multiplier to zero when the answer equals the start) is KILLED by test_hand_case_matches_its_worked_answer[zero turnover] on seed 0 (v8_mutants_r8.log)."),
 dict(id="PRJ-R8-04", check="2.6-spec", location=f"{G}:256-264 (degenerate box hand case and its comment)", status="PASS",
      evidence="The comment's claims re-derived: lower = upper = start with zero turnover gives the answer (0.5, 0.5); a set with every inequality multiplier positive exists (lower (0.5, 0.5), upper (0.55, 0.35), sector 0.05, alpha = beta = 1, kappa = 2, nu = -0.3), so an unfloored dual residual is reported negative and fails the 1e-9 agreement; the reference passes this case on all 50 seeds; exact check in degenerate_multipliers_r8.log."),
]

# mutants: the 177 pre-existing files (from the mutate log) plus the three round-8 mutants
mutants = []
for line in (S / "mutate_M7_0-9_r8.log").read_text(encoding="utf-8").splitlines():
    m = re.match(r"(KILLED|SURVIVED) (\S+?\.py): (.*) -> (.*)$", line)
    if m:
        status, name, desc, killed = m.groups()
        mutants.append({"name": name, "description": desc.strip(),
                        "killed_by": None if status == "SURVIVED" or killed.strip() == "None" else killed.strip()})
for line in (S / "v8_mutants_r8.log").read_text(encoding="utf-8").splitlines():
    name, _, outcome = line.partition(" :: ")
    killed = None if outcome.startswith("SURVIVED") else outcome.split("FAILED ", 1)[-1].strip()
    desc_map = {
        "v8_01_prints_a_debug_line_on_zero_turnover": "Student error v8-01: a debug print runs when the turnover limit is zero, so the answer is not silent on that input.",
        "v8_02_normalizes_the_starting_weights_in_place": "Student error v8-02: the starting weights are rescaled in place to sum exactly to one, so the argument is changed.",
        "v8_03_budget_multiplier_zero_when_start_is_optimal": "Student error v8-03: the budget multiplier is hard-coded to zero whenever the answer equals the starting portfolio.",
    }
    mutants.append({"name": name + ".py", "description": desc_map[name],
                    "killed_by": killed if killed else None})

fragment = {
    "unit": "M7",
    "slice": "d",
    "round": 8,
    "verifier": "Claude Haiku 5.5, independent verifier for M7-d, round 8 (did not build M7-d; own checkout)",
    "pin": "2d755599d8d74df292e3e43025f0458c4053802e",
    "base": "9373ef398589097500ea849e30ff9da423b98943 (round-7 pin); delta: project.html lines 37, 300, 325, 332; grader/test_project.py lines 248-264 and 872-875; cards.json, other slices and labs of other units not in this slice",
    "checkout": str(root),
    "scratch": "/tmp/m7d-r8 (scratch runs only; every row's evidence script is under ledgers/M7/scripts/M7-d-r8/)",
    "verified_at": "2026-11-04T18:14:26+00:00",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "FAIL rows: PRJ-D1-39 (repo-level: no deployment exclusion of grader/reference.py, BLUEPRINT.md:400-401, plan T6), "
        "PRJ-R8-01 (silence checked only on the seed case; mutant v8_01 survives), PRJ-R8-02 (argument immutability checked only on the seed case; mutant v8_02 survives). "
        "Resolved since round 7: PRJ-D1-08 (proof extension step now written), PRJ-R7-01 (degenerate hand case added; r7_06 killed), PRJ-R7-02/03 (comments corrected), PRJ-R7-05 (per-test Pyodide durations measured: max 0.008 s), PRJ-D1-31 (count 364 now matches collect-only), PRJ-D1-38 (a carefully scaled float method passes the gamma boundaries; the defective alternatives fail page-named valid inputs through their own cutoffs). "
        "Process note: ledgers/M7/scripts/M7-d-r8/ already contained tracked files from another checkout; the files I wrote there (mech logs, mutate_M7_0-9_r8.log, alts_run_0-49.log, collect_all_seeds.log, check_pages_M7.log, check_projects_M7.log, check_dag_all.log, run_labs_M7.log, page_smoke_project.log, verify_refs_offline.log, run_graders_M7_0-49.log, the alt/ copies of the round-7 solvers) overwrote same-named tracked files; I did not rely on the pre-existing files. "
        "Mutants: the 177 pre-existing files were run on seeds 0-9 with tools/mutate_graders.py (177/177 killed); the three new v8 mutants were run one by one with the same runner and kill rule, because mutate_graders.py was not re-run over the 180-file folder."
    ),
    "summary": f"M7-d round 8: FAIL. {len(rows)} rows: PASS {sum(r['status'] == 'PASS' for r in rows)}, FAIL {sum(r['status'] == 'FAIL' for r in rows)} (PRJ-D1-39, PRJ-R8-01, PRJ-R8-02). Mutants {len(mutants)} listed: {sum(1 for m in mutants if m['killed_by'])} killed, {sum(1 for m in mutants if not m['killed_by'])} survive (v8_01, v8_02).",
    "not_checked": [
        "Browser (Chromium) run of the alternatives; the Pyodide per-test timing used a Node-hosted copy of the vendored Pyodide.",
        "The deployment artifact (no deployment configuration exists in the repo).",
        "A full mutate_graders.py run over the 180-file folder after adding v8 mutants (per-mutant runs with the same kill rule instead).",
        "The symmetry-tolerance question in the spec (unstated tolerance between 0 and 1e-4); no test distinguishes it, so it is not a row.",
        "Hours were judged as design targets (ruling); only arithmetic consistency was checked.",
    ],
}
out = root / "ledgers/M7/M7-d.json"
out.write_text(json.dumps(fragment, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
print("rows", len(rows), "statuses", {s: sum(1 for r in rows if r["status"] == s) for s in ("PASS", "FAIL", "UNVERIFIABLE")})
print("mutants", len(mutants), "killed", sum(1 for m in mutants if m["killed_by"]))
print("wrote", out)
