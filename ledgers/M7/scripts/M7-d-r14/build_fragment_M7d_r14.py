"""Build the round-14 fragment ledgers/M7/M7-d.json for slice d (project.html, grader, project labs, mutants).

Run from the repository root after every command output in ledgers/M7/scripts/M7-d-r14/ exists:
    python -I ledgers/M7/scripts/M7-d-r14/build_fragment_M7d_r14.py
The mutant list is parsed from mutate_graders_M7_0-9_all205_r14.log (one KILLED line per mutant).
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
S = "ledgers/M7/scripts/M7-d-r14/"
CARRY = "Carried from round 12 (grader/*.py, tests/labs/M7/lab-M7-project-*.py byte-identical since 329c1d7; git diff empty): "
ALTS_CARRY = "Carried from round 12 (ledgers/M7/scripts/M7-d-r10 and M7-d-r11 byte-identical since 329c1d7; git diff empty): "

MUTATE = f"{S}mutate_graders_M7_0-9_all205_r14.log"
LABS = f"{S}run_labs_M7_r14.log"
SWEEP = f"{S}seed_sweep_r14.log"
RECHECK = f"{S}recheck_project_numbers_r14.log"
ALTS = f"{S}alts_five_seeds0-49_r14.log"
RALTS = f"{S}alts_repaired_float_seeds0-49_r14.log"
OALTS = f"{S}alts_original_r10_seeds0-49_r14.log"
PATHS = f"{S}path_stats_frontends_r14.log"
SMOKE = f"{S}page_smoke_project_r14.log"
RUNG = f"{S}run_graders_M7_seeds0-49_r14.log"
EQUIV = f"{S}equiv_witness_r14.log"
NEWM = f"{S}recheck_new_mutants_r14.log"
PROBE = f"{S}wrong_w0_probe_output_r14.log"
STARTER = f"{S}starter_suite_seed0_r14.log"

R = []


def row(rid, check, location, status, evidence, fix=""):
    R.append({"id": rid, "check": check, "location": location, "status": status, "evidence": evidence, "fix": fix})


# ---- Round-12 rows, re-decided in round 14 -------------------------------------------------------------------------
row("PRJ-D1-01", "2.6-spec", "course/modules/M/M7/grader/instance.py (make_instance)", "PASS",
    CARRY + f"instance.py:57 builds the label unconditionally; {SWEEP}: label on 50 of 50 seeds, instances valid on 50 of 50, "
    "deterministic per seed (run_graders determinism check).")
row("PRJ-D1-02", "2.6-spec", "project.html:299-300; grader/test_project.py output_shape (174-201)", "PASS",
    "Re-read project.html:299-300 (three keys; seven multiplier keys; four certificate keys; list lengths n, Z) against "
    "test_project.py:174-201 line by line; they match.")
row("PRJ-D1-03", "2.4-math", "project.html:309", "PASS",
    "Re-derived the linearization equivalence both ways: sum|d_i| <= tau implies t_i=|d_i| satisfies t_i>=d_i, t_i>=-d_i, "
    "sum t_i<=tau; any feasible t gives t_i>=|d_i| so sum|d_i|<=sum t_i<=tau.")
row("PRJ-D1-04", "2.4-math", "project.html:310-313", "PASS",
    "Re-derived r^w_i and r^t_i from L = f + sum lambda_j g_j + nu(sum w - 1) with g_j <= 0 as listed at project.html:310: "
    "d/dw_i of l_i-w_i gives -lambda^l_i; of w_i-u_i gives +lambda^u_i; of sum_S w - c_k gives +eta_k; of d_i-t_i gives +alpha_i; "
    "of -d_i-t_i gives -beta_i; d/dt_i of d_i-t_i gives -alpha_i, of -d_i-t_i gives -beta_i, of sum t - tau gives +kappa. "
    "Matches project.html:312-313, reference.py:305-308 and test_project.py:139-150.")
row("PRJ-D1-05", "2.4-math", "project.html:310,314-319; grader/test_project.py inequality_pairs (116-130)", "PASS",
    "The six constraint families and their multipliers at project.html:310 and 314-319 are the pairs in inequality_pairs; checked line by line.")
row("PRJ-D1-06", "2.4-math", "project.html:320; grader/test_project.py recomputed_certificate (154-165)", "PASS",
    "The floor claim holds: max(0,-min m) differs from -min m only when min m > 0 (every inequality multiplier positive); the "
    "agreement check then fails only when min m exceeds 1e-9 (project.html:320 and test_project.py:157, 434).")
row("PRJ-D1-07", "2.4-math", "project.html:317-321; test_project.py recomputed_certificate (154-165)", "PASS",
    "Primal, stationarity, dual and complementary-slackness definitions (project.html:315-318) equal recomputed_certificate "
    "(test_project.py:154-165) and reference.py _certificate (262-315).")
row("PRJ-D1-08", "2.4-math", "project.html:323-325 (Proposition, T, and proof)", "PASS",
    "Re-proved: L is convex and differentiable in (w,t), so the stationarity point minimizes it; for feasible (y,s) with s_i=|y_i-w0_i| "
    "f(y) >= L(y,s) >= L(w,t) = f(w) by sign of lambda, feasibility and complementary slackness; uniqueness by strict convexity "
    "and the feasible midpoint. Every step is supported by the stated hypotheses.")
row("PRJ-D1-09", "2.4-math", "project.html:325; grader/instance.py:3-4,39-43", "PASS",
    "instance.py:39-43 builds Sigma=(A'A+I)/1000 exactly as stated; x'Sigma x=(|Ax|^2+|x|^2)/1000>0 for x!=0 (arithmetic checked). "
    "The page states that existence of multipliers is not proved (project.html:325); no such claim is made.")
row("PRJ-D1-10", "2.6-spec", "project.html:326; grader/reference.py _parse (54-109)", "PASS",
    "Each named ValueError condition on project.html:326 raises ValueError in _parse (lines 56-108); other invalid inputs raise TypeError "
    "with a message (lines 40, 50, 96), which the page permits.")
row("PRJ-D1-11", "2.6-spec", "grader/test_project.py NAMED_CONDITIONS (637-651), OTHER_SIDE_REFUSED (754-777)", "PASS",
    "Each named condition has an invalid case refused with ValueError and a valid case accepted; the other side is also refused "
    f"(test run: {RUNG}, collected 364).")
row("PRJ-D1-12", "2.6-spec", "project.html:326,332; test_project.py EXACT_BOUNDARIES (674-680), NAMED_CONDITIONS (637-651)", "PASS",
    "The exact boundaries named on the page (bound or cap equal to the start, start sum inside 1e-9 low side, gamma 1e-6 and 1e-9, "
    "turnover limit zero) are in EXACT_BOUNDARIES and NAMED_CONDITIONS and pass on the reference (run_graders 50 of 50).")
row("PRJ-D1-13", "2.5-lab", "project.html:53-168; tests/labs/M7/lab-M7-project-1.py", "PASS",
    f"{LABS}: run_labs M7 PASS (11/11), twin byte-identical to the page code, expected block equals output. "
    f"{RECHECK}: step 1-7 values (54/65, 5/26, -3/130; 9/11, 2/11, 0; nu=-21/1100; lambda=9/1100; objective -3/220) re-derived with Fractions.")
row("PRJ-D1-14", "2.5-lab", "project.html:170-285; tests/labs/M7/lab-M7-project-2.py", "PASS",
    f"{LABS}: completion lab PASS; page lines 250, 261, 262 are the three blanks named in the hypothesis (project.html:172); every other "
    "line equals the twin (diff checked this round).")
row("PRJ-D1-15", "2.5-lab", "project.html:372-445; tests/labs/M7/lab-M7-project-3.py", "PASS",
    f"{LABS}: PASS, twin byte-identical; {RECHECK}: check A all zero, check B stationarity 9/550 and dual 9/1100, check C stationarity 1/6250 "
    "(all re-derived).")
row("PRJ-D1-16", "2.9-hours", "project.html:33,338-354; course/modules/M/M7/index.html:29; curriculum/01-foundations.yaml M7 hours 110", "PASS",
    "Hub data-hours-lessons=77 and data-hours-project=33 (index.html:29); lesson data-hours 9+9+10+10+10+10+9+10=77; project components "
    "2+3+10+6+7+5=33 (project.html:344-350); 77+33=110 equals curriculum hours 110 (curriculum/01-foundations.yaml:298-302).")
row("PRJ-D1-17", "2.9-structure", "project.html:40-49", "PASS",
    "Ladder has four li entries with rung titles 'Rung 1 · Worked example', 'Rung 2 · Completion problem', 'Rung 3 · Independent project', "
    "'Rung 4 · Stretch' in order (project.html:44-47); check_projects --unit M7 PASS.")
row("PRJ-D1-18", "2.6-spec", "project.html:288-336", "PASS",
    "Spec contains Context, Inputs, Required outputs, Conventions, Constraints, Grading and Reading list (dt elements 291-334); "
    "the inputs and outputs match instance.py and test_project.py (see PRJ-R12-11).")
row("PRJ-D1-19", "2.9-structure", "course/modules/M/M7/grader/ (instance.py, reference.py, starter.py, test_project.py)", "PASS",
    "All four files present; reference, starter, instance and suite checked by run_graders (reference 50 of 50, starter fails), mypy --strict on reference, starter, instance: no issues.")
row("PRJ-D1-20", "2.9-structure", "project.html; tools/page_smoke.py --unit M7 --pages project", "PASS",
    f"{SMOKE}: page_smoke modules/M/M7/project.html PASS (zero console errors, labs in Pyodide, grader in Pyodide: All 364 tests pass in 3.8 s).")
row("PRJ-D1-21", "2.4-notation", "project.html symbols vs notation/notation.json (8 registered symbols, 8 macros)", "PASS",
    "The page uses no registered macro (\\R, \\E, \\Phi etc.) and none of the 8 registered symbols (T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, Q). "
    "Its local symbols (gamma, mu, Sigma, nu, lambda, eta, alpha, beta, kappa, tau, w_0, l, u, c_k, S_k, d, t, Z, n) are defined in the "
    "Conventions or the Inputs paragraph (project.html:292-310), as the registry allows for local letters.")
row("PRJ-D1-22", "2.9-dag", "project.html:456 (envelope-theorem link); course/modules/M/M7/index.html", "PASS",
    "The only concept link is envelope-theorem (project.html:456). curriculum/01-foundations.yaml:130-141 shows M2 introduces it and M2 is a prerequisite "
    "of M7 (closure). course/concepts.html has id envelope-theorem (grep count 1). check_dag --unit M7 PASS.")
row("PRJ-D1-23", "2.9-prose", "project.html; tools/check_pages.py BANNED list", "PASS",
    "grep (case-insensitive) for every banned phrase in BUILDER_RULES 1.3-1.4 and the process words round, builder, verifier, fixer: 0 hits; check_pages --unit M7 PASS.")
row("PRJ-D1-24", "2.6-spec", "project.html:364-366 (local run and decode commands)", "PASS",
    "Ran the decode command from the grader folder: prints the label of seed 7. The pytest command uses the flags of run_graders (-q -p no:cacheprovider --assert=plain -W error) and QF_SEED (test_project.py:36).")
row("PRJ-D1-25", "2.6-autograder", "grader/starter.py:18-20; project.html:301", "PASS",
    f"starter.py:20 raises NotImplementedError; {STARTER}: suite on the starter gives 361 failed, 3 passed (the page says the suite fails on the starter).")
row("PRJ-D1-26", "2.6-autograder", "grader/instance.py (make_instance)", "PASS",
    f"{SWEEP}: seeds 0-49 give 18 three-asset, 14 four-asset and 18 five-asset cases; all valid (symmetric, PD, feasible start, caps, labels); "
    "50 distinct reference answers, and the active sets vary by seed (answers change, not only labels).")
row("PRJ-D1-27", "2.6-autograder", "grader/test_project.py:37; grader/reference.py:21", "PASS",
    "TOL=1e-8 in the suite (test_project.py:37) and TOL=1e-9 for the starting checks in the reference (reference.py:21), as project.html:320-321 states.")
row("PRJ-D1-28", "2.6-autograder", "grader/test_project.py assert and pytest.fail messages", "PASS",
    f"Failure messages name the property, not the value. Probe {PROBE}: a wrong allocator fails 338 tests; every printed E line is a message such as "
    "'stationarity fails in the weights...' or 'DID NOT RAISE'; no expected value appears.")
row("PRJ-D1-29", "2.6-autograder", "grader/test_project.py under Pyodide (page_smoke) and CPython (run_graders)", "PASS",
    f"{SMOKE}: All 364 tests pass in the browser; {RUNG}: reference 50 of 50 under -W error in CPython.")
row("PRJ-D1-30", "2.5-lab", "tests/labs/M7/lab-M7-project-1..3.py; tests/test_labs.py -k M7", "PASS",
    f"{S}pytest_labs_M7_r14.log: 11 passed (tests/test_labs.py -k M7, includes the three project labs).")
row("PRJ-D1-31", "2.6-spec", "project.html:332; grader/test_project.py HAND_CASES (274-312)", "PASS",
    "Re-derived each hand case in the comments: budget only (0.6,0.4); zero turnover (0.5,0.5); upper bound binding (0.7,0.3), "
    "and without that bound (0.55,0.45); turnover binding (0.6,0.4). Also the reference returns those answers (recheck_project_numbers_r14.log, 4 hand claims).")
row("PRJ-D1-32", "2.6-atlas", "project.html; curriculum/01-foundations.yaml M7 entry; check_projects --unit M7", "PASS",
    "M7 entry has no atlas key and meta.yaml names no M7 milestone (plan section 10); check_projects PASS, Atlas branch not run.")
row("PRJ-D1-33", "2.1-citations", "project.html:465-466 (reading list); references/references.json", "PASS",
    f"Reading list keys boyd2004convex and stokey1989recursive; {S}verify_refs_M7_live_r14.log: live re-verification of M7: 2 of 560 entries, 0 problems; "
    f"{S}verify_refs_offline_r14.log: 560 entries, 0 problems. The page attributes no claim to them.")
row("PRJ-D1-34", "2.9-structure", "project.html:338-354; tools/check_pages.py --unit M7", "PASS",
    f"{S}check_pages_M7_r14.log: check_pages M7 PASS.")
row("PRJ-D1-35", "2.6-mutation", "ledgers/M7/mutants/ (all files)", "PASS",
    f"{MUTATE}: mutate_graders M7 PASS (205/205 killed, seeds 0-9). The folder holds 205 mutants (202 from earlier rounds, 3 new round-14 mutants).")
row("PRJ-D1-36", "2.6-mutation", "ledgers/M7/mutants/ (all families)", "PASS",
    f"Same run as PRJ-D1-35 ({MUTATE}); every family (d, f, g, m, p, q, r, s, v, w, x, y, z and the r/v/w round families) is killed, including the families of the earlier rounds.")
row("PRJ-D1-37", "2.6-mutation", "ledgers/M7/mutant_equivalence_r14.json; ledgers/M7/mutants/", "FAIL",
    f"The eight equivalent mutants removed in d2b4a874 are recorded only in ledgers/M7/mutant_equivalence_r14.json. Their structural "
    f"arguments hold (re-checked: the reference always has at least one zero inequality multiplier, since the working set has at most n-1 inequality rows; "
    f"{EQUIV}: 0 differences on seeds 0-49 for all eight, and 50 of 50 seeds have a zero minimum). But ruling 9 and ruling 22 require the mutants and "
    "their proofs under ledgers/M7/equivalent/ with a README. That folder does not exist, and the sources are absent from the tree (recoverable only from git d2b4a874^). "
    f"The witness script ledgers/M7/scripts/M7-d-r14/equiv.py loads /tmp/m7d_r14/removed/ and a different worktree, so a later verifier cannot re-run it.",
    "Create ledgers/M7/equivalent/ with a README.md that gives, for each of the eight mutants, its source file (copy from git d2b4a874^) and the structural argument from "
    "mutant_equivalence_r14.json. Replace the /tmp and quant-b2 paths in the witness with repo-relative paths (ledgers/M7/equivalent/*.py) and re-run it.")
row("PRJ-D1-38", "2.6-autograder", "ledgers/M7/scripts/M7-d-r11/alts/alt1..alt9 (alts_suite_r11*.log, r10alt_rerun_*.log)", "PASS",
    ALTS_CARRY + "ledgers/M7/scripts/M7-d-r11/alts/ nine solvers passed on seeds 0-49 in round 11; this round re-ran five of them (see PRJ-R14-16).")
row("PRJ-D1-39", "2.9-structure", "BLUEPRINT.md:400-401 (section 7); course/modules/M/M7/grader/reference.py; .github/workflows/ci.yml", "PASS",
    "Ruling 4: the repository has no deploy step (ci.yml has no deploy job; grep for deploy/pages/vercel/railway: none), no deployment config "
    "(vercel.json, railway.json, netlify.toml, wrangler.toml absent), and no tool excludes grader/reference.py. Ruling 4 says this rule must not fail a slice; recorded for the owner.")
row("PRJ-R4-01", "2.9-prose", "grader/test_project.py docstrings and messages", "PASS",
    "Re-read every docstring and assertion message (test_project.py 1-1127): none prints an expected value; none uses banned process words.")
row("PRJ-R5-01", "2.4-math", "project.html:456 frontier bullet", "PASS",
    "The frontier bullet asks the reader to state the sign convention and check it numerically; it claims no result.")
row("PRJ-R5-02", "2.6-spec", "grader/test_project.py comments and messages (275, 277, 295-296, 301, 303-305)", "PASS",
    "Each hand-case comment matches its arithmetic (see PRJ-D1-31 and recheck_project_numbers_r14.log).")
row("PRJ-R5-03", "2.9-prose", "project.html:450 ('does not test' paragraph)", "PASS",
    "project.html:450: the suite does not test the method, nor any problem other than the generated and hand-worked cases; the claim is consistent with test_project.py.")
row("PRJ-R5-04", "2.9-structure", "project.html:349-350", "PASS",
    "Total row: 33 hours; the text 77 + 33 = 110 matches index.html and curriculum (see PRJ-D1-16).")
row("PRJ-R5-05", "2.6-mutation", "ledgers/M7/mutants/r5_01..r5_05", "PASS",
    f"{MUTATE}: KILLED for each r5_* mutant.")
row("PRJ-R6-01", "2.6-gate", "tools/check_projects.py --all", "PASS",
    f"{S}check_projects_M7_r14.log: check_projects M7 PASS.")
row("PRJ-R6-02", "2.6-gate", "tools/check_pages.py --all", "PASS",
    f"{S}check_pages_M7_r14.log: check_pages M7 PASS (the --all run is the repo gate; the M7 run is the one that reads this unit).")
row("PRJ-R6-03", "2.9-dag", "tools/check_dag.py --all", "PASS",
    f"{S}check_dag_M7_r14.log: check_dag M7 PASS; DAG reading in PRJ-D1-22.")
row("PRJ-R7-01", "2.6-mutation", "grader/test_project.py degenerate box hand case (306-311); mutants r7_06_*", "PASS",
    f"r7_06 is KILLED in {MUTATE}; the degenerate case is in HAND_CASES (test_project.py:306-311).")
row("PRJ-R7-02", "2.9-prose", "grader/test_project.py:295-296 comment", "PASS",
    "The comment at 295-296 matches the arithmetic (see PRJ-D1-31).")
row("PRJ-R7-03", "2.9-prose", "grader/test_project.py:916-921 comment", "PASS",
    "The comment at 916-921 describes _make_room and the four positions; the code (929-933, 935-1013) matches.")
row("PRJ-R7-04", "2.6-mutation", "ledgers/M7/mutants/r7_01..r7_05", "PASS",
    f"{MUTATE}: KILLED for each r7_* mutant.")
row("PRJ-R7-05", "2.6-autograder", "grader/test_project.py under Pyodide (page_smoke)", "PASS",
    f"{SMOKE}: All 364 tests pass in the browser.")
row("PRJ-R7-06", "2.8-data", "project.html; grader/instance.py", "PASS",
    "No dataset, no data-files attribute; instance.py:57 labels every case SIMULATED; project.html:450 says so; no MANIFEST entry is needed.")
row("PRJ-R7-07", "2.6-hours", "project.html:344-350", "PASS",
    "Verifier estimate (PRJ-R14-13) falls inside 30 percent of 33 hours; the component arithmetic is 33.")
row("PRJ-R8-01", "2.6-autograder", "grader/test_project.py:60-77, 1114-1121 and purity fixture (80-104)", "PASS",
    f"The purity fixture runs every allocate call twice (test_project.py:80-104); probe and suite runs show no printed or warned output.")
row("PRJ-R8-02", "2.6-autograder", "grader/test_project.py:1108-1112 and purity fixture", "PASS",
    "test_allocate_does_not_change_its_argument (1108-1112) and the purity fixture (_observed_call, 60-77) both check the argument.")
row("PRJ-R8-03", "2.6-mutation", "ledgers/M7/mutants/v8_03_budget_multiplier_zero_when_start_is_optimal.py", "PASS",
    f"{MUTATE}: KILLED.")
row("PRJ-R8-04", "2.6-spec", "grader/test_project.py:302-311", "PASS",
    "The degenerate-box comment (302-305) and the case (306-311) agree with the page's floor rule (project.html:320).")
row("PRJ-R9-01", "2.6-autograder", "grader/test_project.py:60-77 (_observed_call) vs pytest.raises(Exception) tests", "PASS",
    "The Exception-typed tests are only for conditions the page does not name (wrong types, a number where a list belongs, empty caps); "
    "the named conditions use ValueError (test_project.py 686-692, 783, 812-831).")
row("PRJ-R9-02", "2.9-prose", "grader/test_project.py:82-89 docstring", "PASS",
    "The docstring states the checks exactly as the code makes them (run twice, purity, same output or same refusal).")
row("PRJ-R9-03", "2.6-autograder", "grader/test_project.py:92 (@wraps) and 319-326", "PASS",
    "The wrapper preserves the signature; test_module_defines_allocate_with_one_argument (320-326) checks it.")
row("PRJ-R9-04", "2.9-prose", "project.html:167 (Lab 1 interpretation)", "PASS",
    "Lab 1 interpretation (project.html:167) says what the output shows; the checks it names (steps 4-6) are printed by the code; no unprinted claim.")
row("PRJ-R9-05", "2.4-math", "project.html:324 (proof)", "PASS",
    "Re-proved (PRJ-D1-08); the proof uses only the hypotheses stated at project.html:325.")
row("PRJ-R9-06", "2.6-autograder", "ledgers/M7/scripts/M7-d-r11/alts/ and alts_suite_r11*.log", "PASS",
    ALTS_CARRY + "the round-11 alternatives suite; re-run this round for five of the solvers (PRJ-R14-16).")
row("PRJ-R9-07", "2.6-mutation", "ledgers/M7/mutants/ (final folder)", "PASS",
    f"{MUTATE}: 205 of 205 killed.")
row("PRJ-R9-08", "2.9-structure", "grader/test_project.py (collected count); project.html:332", "PASS",
    f"{S}seed_sweep_r14.log: collected count 364 on each of seeds 0-49 (one value). The count is constant by construction: POSITIONS and FIELDS are fixed tuples and N>=3, Z=2.")
row("PRJ-R9-09", "2.5-lab", "project.html:53-285, 372-445; tests/labs/M7/lab-M7-project-1..3.py", "PASS",
    f"{LABS}: PASS (11 of 11).")
row("PRJ-R9-10", "2.6-autograder", "grader/test_project.py under Pyodide (page_smoke)", "PASS",
    f"{SMOKE}: All 364 tests pass in the browser in 3.8 s.")
row("PRJ-R9-11", "2.9-prose", "grader/test_project.py:274-311 hand-case comments", "PASS",
    "Each comment is checked against its case (PRJ-D1-31).")
row("PRJ-R10-01", "2.6-autograder", "ledgers/M7/scripts/M7-d-r10/alts/alt_B, alt_G, alt_H, alt_I, alt_J (exact Fraction active sets)", "PASS",
    ALTS_CARRY + "exact Fraction active-set alternatives passed on seeds 0-49 in round 12; the round-14 exact alternative (alt1, PRJ-R14-16) passes too.")
row("PRJ-R10-02", "2.6-autograder", "ledgers/M7/scripts/M7-d-r10/alts/alt_A, alt_C, alt_D, alt_E, alt_F (float alternatives)", "PASS",
    f"{OALTS}: the round-10 float alternatives fail 0 of 50 seeds, every time on the page's stated gamma boundary (gamma = 1e-6 and 1e-9 are valid, project.html:326): "
    "under ruling 10 they are student errors, not alternatives, and the suite rejects them. Their repaired same-method versions "
    f"({RALTS}: alt A, C, D, E, F each pass 50 of 50 seeds) are the alternatives. Note: the originals should be filed as killed mutants (ruling 10); not a grader defect.")
row("PRJ-R10-03", "2.6-mutation", "ledgers/M7/mutants/r10_01..r10_03", "PASS",
    f"{MUTATE}: KILLED for each r10_* mutant.")
row("PRJ-R10-04", "2.6-autograder", "ledgers/M7/mutants/ full set", "PASS",
    f"{MUTATE}: 205 of 205 killed.")
row("PRJ-R10-05", "2.6-autograder", "tools/run_graders.py --unit M7 --seeds 0-49; mypy --strict on grader", "PASS",
    f"{RUNG}: run_graders M7 PASS (reference 50/50, slowest 6.5 s); {S}mypy_strict_m7_grader_r14.log: strict mypy on reference, instance, starter and the three project labs: no issues.")
row("PRJ-R10-06", "2.9-structure", "repo gates: ruff check ., ruff format --check ., mypy --no-incremental, verify_refs --offline", "PASS",
    f"{S}ruff_check_r14.log: All checks passed; {S}ruff_format_r14.log: 553 files already formatted; {S}mypy_r14.log: Success, 385 source files; "
    f"{S}verify_refs_offline_r14.log: 560 entries, 0 problems.")
row("PRJ-R11-01", "2.6-autograder", "over-constraint: ledgers/M7/scripts/M7-d-r11/alts/ (nine solvers)", "PASS",
    ALTS_CARRY + "the nine round-11 solvers passed on seeds 0-49; round 14 adds five more (PRJ-R14-16).")
row("PRJ-R11-02", "2.6-mutation", "ledgers/M7/mutants/r11_01, r11_03, r11_05, r11_06", "PASS",
    f"{MUTATE}: KILLED for each.")
row("PRJ-R11-03", "2.6-spec", "project.html:326 (gamma valid form) vs test_project.py EXACT_BOUNDARIES (gamma 1e-9) and NAMED_CONDITIONS (gamma 1e-6)", "PASS",
    "project.html:326 names gamma of 1e-6 and 1e-9 as valid; the suite accepts both (test_project.py:640, 656, 679), and the original float alternatives that fail them are documented under PRJ-R10-02.")
row("PRJ-R11-04", "2.6-autograder", "grader/test_project.py assertion style under default pytest mode", "PASS",
    f"The suite runs with --assert=plain (run_graders flags, {RUNG}); no assertion depends on pytest rewriting.")
row("PRJ-R12-01", "2.6-autograder", "grader/instance.py (make_instance) seeds 0-49", "PASS",
    f"{SWEEP}: all 50 seeds valid; the seed sweep is the evidence.")
row("PRJ-R12-02", "2.6-autograder", "plans/M7-build-plan.md section 7.4 item 2 (five alternatives, different methods)", "PASS",
    f"Five alternatives on seeds 0-49 ({ALTS}): alt1 exact Fraction active set 50/50; alt2 projected gradient, alt3 ADMM, alt4 log-barrier interior point, alt5 dual ascent: each 50/50. "
    f"Ruling 19 applies: the four front-end solvers return via a float KKT solve accepted only if feasible and dual feasible (tolerances 1e-9, 1e-10), otherwise via the exact active set. "
    f"{PATHS}: front-end answers 13, 45, 45, 41 of 50 seeds for alt2..alt5. Caveat: the front-end check is a float tolerance check, not exact arithmetic; the suite certifies every returned answer on seeds 0-49.")
row("PRJ-R12-03", "2.6-autograder", "over-constraint check: exact and float active-set alternatives on seeds 0-49", "PASS",
    f"{ALTS} (exact alt1: 50/50) and {RALTS} (repaired float A, C, D, E, F: 50/50 each).")
row("PRJ-R12-04", "2.6-autograder", "over-constraint check: float alternatives r12 alt 3-7 (solver defects on valid gamma inputs)", "PASS",
    f"The float alternatives that failed on the gamma boundary (originals, {OALTS}) are replaced by the repaired versions, which pass 50 of 50 ({RALTS}).")
row("PRJ-R12-05", "2.6-mutation", "new student-error mutants v12_02, v12_03, v12_04, v12_05 (ledgers/M7/mutants/)", "PASS",
    f"{MUTATE}: KILLED for each v12_* mutant.")
row("PRJ-R12-06", "2.6-mutation", "equivalence proof: v12_01 (dual residual reported without the floor at zero)", "FAIL",
    "The argument holds: the working set holds at most n-1 inequality rows, so one of the n lower-bound multipliers is zero and the minimum over all inequality multipliers is zero on every reference output "
    f"(scripts/M7-d-r12/alts_v12/equiv_v12_01.py, 10/10 seeds and 400 random cases, per its log). But the candidate sits only under ledgers/M7/scripts/M7-d-r12/alts_v12/equivalent_candidates/. "
    "Ruling 9 and ruling 22 require ledgers/M7/equivalent/ with a README proof, and that folder does not exist.",
    "Move ledgers/M7/scripts/M7-d-r12/alts_v12/equivalent_candidates/v12_01_dual_residual_reported_without_the_floor_at_zero.py to ledgers/M7/equivalent/ "
    "and add a README.md section with the structural argument and the random-check log.")
row("PRJ-R12-07", "2.6-autograder", "grader/test_project.py collect-only, seeds 0-49", "PASS",
    f"{SWEEP}: 364 collected on each of seeds 0-49 (pytest --collect-only, same flags).")
row("PRJ-R12-08", "2.5-lab", "project.html lab code and expected blocks vs tests/labs/M7/lab-M7-project-1..3.py", "PASS",
    f"{LABS}: run_labs PASS; the page code equals each twin, except the three completion blanks in lab 2.")
row("PRJ-R12-09", "2.4-math", "project.html Lab 1 and Lab 3 printed numbers", "PASS",
    f"{RECHECK}: 27 of 27 claims hold, including each printed number in Labs 1 and 3 and the prose in the interpretations.")
row("PRJ-R12-10", "2.4-math", "project.html:323-325 Proposition (grade T)", "PASS",
    "Re-proved (PRJ-D1-08); grade T is correct because the statement is derived in the proof with its hypotheses.")
row("PRJ-R12-11", "2.6-spec", "project.html:292-300 inputs and outputs vs instance.py and test_project.py", "PASS",
    "Inputs (n in 3-5, Z=2, nine fields, label) match instance.py:34-68 and test_project.py FIELDS; outputs match output_shape (174-201).")
row("PRJ-R12-12", "2.6-spec", "project.html:326 named conditions vs test_project.py NAMED_CONDITIONS, OTHER_SIDE_REFUSED, EXACT_BOUNDARIES, non-finite, missing field, non-mapping, no assets, one entry short/long", "PASS",
    "Every named condition on project.html:326 has tests in the lists listed; NaN, infinity, missing field, non-mapping, no assets, one entry short or long are all tested (PRJ-D1-11, D1-12).")
row("PRJ-R12-13", "2.6-autograder", "Pyodide timing (plan 7.4; BUILDER_RULES 5.3.4)", "PASS",
    f"{SMOKE}: the whole suite (364 tests) in the browser takes 3.8 s, so no single test takes 5 s or more. The 60 s suite limit is met.")
row("PRJ-R12-14", "2.1-citations", "project.html:465-466 reading list keys", "PASS",
    "Both keys are verified in references/references.json (PRJ-D1-33).")
row("PRJ-R12-15", "2.9-dag", "project.html:310 'defined in Lesson 3' link", "PASS",
    "course/modules/M/M7/L03.html:62 (Definition 1.2) defines the Lagrangian with g_i(x) <= 0, the convention of project.html:310.")

# ---- Round-14 rows --------------------------------------------------------------------------------------------------
row("PRJ-R14-01", "2.6-mutation", "ledgers/M7/mutant_equivalence_r14.json; ledgers/M7/equivalent/ (absent)", "FAIL",
    "Umbrella row for ruling 9 and 22: every equivalent-mutant proof in this unit must live in ledgers/M7/equivalent/ with a README. Two sets are not there: "
    "the eight removed mutants (PRJ-D1-37) and the v12_01 candidate (PRJ-R12-06). The folder does not exist.",
    "Create ledgers/M7/equivalent/README.md and move both sets there with their sources (see the fixes on PRJ-D1-37 and PRJ-R12-06).")
row("PRJ-R14-02", "2.4-math", "project.html:167, 172, 310 (multiplier references) vs project.html:310 Conventions", "PASS",
    "Lab 2 hypothesis (project.html:172) says 'Both multipliers are defined in the Conventions of the specification below'; project.html:310 defines nu and lambda^l_i there. Lab 1 interpretation (167) carries the same reference.")
row("PRJ-R14-03", "2.5-lab", "project.html:444 (Lab 3 interpretation) vs project.html:412 and the printed line", "PASS",
    f"The new sentence: the lab prints the largest absolute stationarity residual over the three assets, which is 1/6250. The code (project.html:412) takes max of abs; "
    f"{RECHECK} confirms the signed residuals (+3/50000, -1/6250, -1/25000) and the printed max 1/6250.")
row("PRJ-R14-04", "2.5-lab", "project.html:169-285 (Lab 2) completion blanks vs twin tests/labs/M7/lab-M7-project-2.py", "PASS",
    "The blanks are exactly the three named lines (residual, signs, dual_feasible; project.html:250, 261, 262); every other line equals the twin (diff this round).")
row("PRJ-R14-05", "2.6-mutation", "ledgers/M7/mutants/w14d_01..w14d_03 (new round-14 student-error mutants)", "PASS",
    f"Three new complete student-error modules (w14d-01 complementary slackness on the raw sector sum; w14d-02 active-set gradient at w0; w14d-03 zero turnover treated as no limit). "
    f"Killed in {MUTATE} (seeds 0-9) and re-run after reformatting in {NEWM} (killed at seeds 2, 0, 0).")
row("PRJ-R14-06", "2.6-autograder", "grader/test_project.py: 364 checks, identical for every seed (project.html:332)", "PASS",
    f"{SWEEP}: 364 on each of seeds 0-49; constant by construction (fixed parametrization; N in {{3,4,5}}, Z=2).")
row("PRJ-R14-07", "2.6-autograder", "project.html:450 'every case carries the SIMULATED label'", "PASS",
    f"instance.py:57 labels every case unconditionally; {SWEEP}: label on 50 of 50 seeds.")
row("PRJ-R14-08", "2.6-autograder", "project.html:326 'other invalid inputs... raise an exception that carries a message'", "PASS",
    "Reference raises TypeError (with messages) for wrong types, ValueError for named conditions; the suite accepts any exception with a message for the other inputs (test_project.py 866-913), so the page statement matches.")
row("PRJ-R14-09", "2.6-rubric", "curriculum/01-foundations.yaml:327 (grading autograder); tools/check_projects.py rubric block", "PASS",
    "Grading is autograder only, so no rubric, exemplar or question-bank row applies (plan T5). Blind exemplar scoring (ruling 23) is not required for this unit: there are no exemplars.")
row("PRJ-R14-10", "2.6-atlas", "curriculum/meta.yaml atlas block; project.html", "PASS",
    "No atlas milestone names M7 (plan section 10) and the M7 entry has no atlas key; the Atlas branch of check_projects is not run.")
row("PRJ-R14-11", "2.9-hours", "project.html:344-350 (verifier estimate)", "PASS",
    "Verifier estimate of each component: rung 1 read and annotate 1.5-2 h; rung 2 three blanks 1-2 h; core solver with active-set search 10-14 h; "
    "turnover and sector linearization 4-6 h; certificate with seven multipliers 4-6 h; self-check and own tests 4-7 h. Total 24.5-37 h, which lies inside 30 percent of 33 h (23.1-42.9 h).")
row("PRJ-R14-12", "2.6-gate", "tools/check_pages.py --unit M7; tools/check_dag.py --unit M7; tools/check_projects.py --unit M7", "PASS",
    f"{S}check_pages_M7_r14.log, {S}check_dag_M7_r14.log, {S}check_projects_M7_r14.log: all PASS.")
row("PRJ-R14-13", "2.6-autograder", "Pyodide per-test time (plan 7.3: under 5 s each, 60 s per suite)", "PASS",
    f"{SMOKE}: the whole suite runs in 3.8 s in the browser, so each test is below 5 s.")
row("PRJ-R14-14", "2.6-autograder", "run_labs --unit M7; pytest tests/test_labs.py -k M7", "PASS",
    f"{LABS}: PASS 11/11; {S}pytest_labs_M7_r14.log: 11 passed.")
row("PRJ-R14-15", "2.6-autograder", "over-constraint: the five alternatives of plan 7.4.2 (ruling 19)", "PASS",
    f"{ALTS}: alt1 exact active set 50/50, alt2 projected gradient 50/50, alt3 ADMM 50/50, alt4 interior point 50/50, alt5 dual ascent 50/50; {PATHS} gives the path counts. "
    "The five files are copies in ledgers/M7/scripts/M7-d-r14/alts/.")
row("PRJ-R14-16", "2.6-autograder", "over-constraint: ledgers/M7/scripts/M7-d-r14/alts/ (five and five repaired)", "PASS",
    f"{RALTS}: the repaired float alternatives A, C, D, E, F pass 50 of 50; {OALTS}: the originals fail 50 of 50 on the gamma boundary and are student errors under ruling 10.")
row("PRJ-R14-18", "2.1-citations", "references/references.json (boyd2004convex, stokey1989recursive)", "PASS",
    f"{S}verify_refs_M7_live_r14.log: 2 of 560 entries re-verified live, 0 problems.")

MUTANTS = []
for line in Path(ROOT, MUTATE).read_text(encoding="utf-8").splitlines():
    m = re.match(r"^KILLED (\S+): (.*?) -> (.*)$", line)
    if m:
        MUTANTS.append({"id": m.group(1), "description": m.group(2), "killed_by": m.group(3)})

fragment = {
    "unit": "M7",
    "slice": "d",
    "round": 14,
    "verifier": "Haiku 5.5 independent verifier (round 14, slice d); did not build M7-d",
    "pin": "1431aa1d (1431aa1d842a5d2d05fd5953c098500bf78a4307)",
    "base": "329c1d7 (round-12 pin, 329c1d7feac5479403c351e64587c867278452cc). Slice delta: project.html (lines 172 and 444), references/references.json (not M7), 7 mutants added in round 12 (already counted), equivalence records, and the three round-14 mutants",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyD14-M7-d",
    "scratch": "ledgers/M7/scripts/M7-d-r14/",
    "verified_at": "2026-11-09T06:55:28+00:00",
    "verdict": "FAIL",
    "rows": R,
    "mutants": MUTANTS,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "Slice d read in full this round: project.html 1-482, grader/instance.py, reference.py, starter.py, test_project.py 1-1127. "
        "The round-13 fragment named in the brief (frags/D-M7-d.round13.json) does not exist; the round-12 fragment (frags/D-M7-d.round12.json) was used as context and its PASS rows were not trusted. "
        "ledgers/M7/M7-d.json at the pin is another lineage (round 15, pin 448548f) and was replaced by this fragment. "
        "Ruling 19 is applied to the four front-end solvers; their 'exact KKT check' is a float feasibility and dual-feasibility check with tolerances, not exact arithmetic, and the suite certifies each answer. "
        "The original round-10 float alternatives fail the page's gamma boundary (student errors under ruling 10); they are not in ledgers/M7/mutants and should be filed there. "
        "Not checked: full repository pytest (only tests/test_labs.py -k M7); the Chromium page_smoke for L01-L08 (other slices); verify_refs live for the whole registry (scheduled job); cards (out of slice)."
    ),
    "summary": {},
}
counts = {"PASS": 0, "FAIL": 0, "UNVERIFIABLE": 0}
for r in R:
    counts[r["status"]] += 1
fragment["summary"] = {
    "rows": len(R),
    "pass": counts["PASS"],
    "fail": counts["FAIL"],
    "unverifiable": counts["UNVERIFIABLE"],
    "mutants": len(MUTANTS),
    "mutants_killed": sum(1 for m in MUTANTS if m["killed_by"]),
    "mutate_summary": "mutate_graders M7 --seeds 0-9: PASS (205/205 killed)",
}
out = ROOT / "ledgers/M7/M7-d.json"
out.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out, fragment["summary"])
