"""Round-2 verifier: build ledgers/M7/M7-d.json (fragment) from the rows and the mutate log, then validate it."""
import json
import pathlib
import re
import sys
from datetime import UTC, datetime

REPO = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyD2-M7-d")
sys.path.insert(0, str(REPO / "tools"))
import ledger  # noqa: E402

rows = []


def row(rid, check, location, status, evidence, fix=None):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    rows.append(r)


row("PRJ-D1-01", "2.6 spec: Context and Inputs", "project.html:292-295", "PASS",
    "grader/instance.py:20-21 (SECTOR_COUNT=2, ASSET_COUNTS=(3,4,5)); instance.py:56-68 emits gamma, mu, sigma, w0, lower, upper, sector, sector_caps, turnover_limit and the SIMULATED label (line 57); reference.py:20 REQUIRED equals the page's field list. Whole instance.py read.")
row("PRJ-D1-02", "2.6 spec: Required outputs", "project.html:299-300", "PASS",
    "grader/test_project.py:129-150 checks exactly the keys weights, multipliers, certificate; the seven multiplier names (140-142); list lengths; four certificate keys (148). test_output_has_the_three_fields_and_frozen_names passes on the reference (run_graders_0-49.log).")
row("PRJ-D1-03", "2.4 maths: linearized turnover", "project.html:309", "PASS",
    "Re-derived: t_i >= |d_i| gives sum|d_i| <= sum t_i <= tau; t_i = |d_i| satisfies the three constraints. Matches reference.py:266-277 and test_project.py:62-64.")
row("PRJ-D1-04", "2.4 maths: stationarity residuals r^w, r^t", "project.html:311-312", "PASS",
    "Re-derived with L = f + sum lambda g + nu(sum w - 1), g <= 0 (the convention of L03.html:62): d/dw_i gives -lambda^l + lambda^u + eta + alpha - beta (d_i = w_i - w0_i, so dd_i/dw_i = 1); d/dt_i gives kappa - alpha - beta. Identical to test_project.py:84-102 and reference.py:304-309.")
row("PRJ-D1-05", "2.4 maths: four certificate definitions", "project.html:314-319", "PASS",
    "reference.py:262-315 and test_project.py:105-116 implement each field. The primal set also contains d_i - t_i and -d_i - t_i, which are <= 0 at t=|d| and so never change the maximum with 0 (re-derived). Dual uses min over lower, upper, sector, plus, minus, total; CS over the same six groups.")
row("PRJ-D1-06", "2.4 / 2.2: dual-residual floor claim (round-1 subject changed)", "project.html:320", "PASS",
    "Re-verified in round 2 on the changed wording ('0 to 49 (50 of 50 ...)'). scripts/M7-d-r2/ref_seeds.py: smallest inequality multiplier exactly 0 on 50 of 50 seeds 0-49 (ref_seeds_out.log). active_set_count.py: on seeds 0-299 the reference's working set has at most n-1 inequality rows, at least n+1 of the 2n bound multipliers are zero, and the smallest multiplier is exactly 0 (0 violations of each; active_set_count_out.log). The independence that bounds the working set is enforced at reference.py:204 and :229. The agreement check recomputes the dual residual with the floor (test_project.py:108, 356-362).")
row("PRJ-D1-07", "2.4: tolerances 1e-8 (fields) and 1e-9 (agreement, starting portfolio)", "project.html:321", "PASS",
    "test_project.py:36 TOL = 1e-8 for feasibility, stationarity, CS and dual; agreement 1e-9 at test_project.py:360 and :405; starting-portfolio tolerance Fraction(1, 10**9) at reference.py:21 and :102-108; boundary tests at test_project.py:461-485.")
row("PRJ-D1-08", "2.4 maths: Proposition (sufficiency of KKT), grade T", "project.html:323-324", "PASS",
    "Proof re-derived line by line: L convex in (w,t) since lambda_j >= 0 and g_j affine; grad L = 0 gives a global minimiser of L; for feasible (y,s): f(y) >= L(y,s) >= L(w,t) = f(w) using CS; the strict-convexity midpoint argument gives uniqueness of w; the feasible set is convex because the constraints are affine. Every hypothesis used is in the statement. Grade T is justified.")
row("PRJ-D1-09", "2.4: hypotheses paragraph (Sigma, 50 of 50)", "project.html:325", "PASS",
    "instance.py:38-41 builds Sigma = (A'A + I)/1000 with integer A (randint(-2,2)); x'Sigma x = (|Ax|^2 + |x|^2)/1000 > 0 for x != 0 (algebra checked). The 50 of 50 figure: run_graders_0-49.log and PRJ-D1-06.")
row("PRJ-D1-10", "2.6 spec: named ValueError conditions and boundary values", "project.html:326", "PASS",
    "Every named condition has a test. NAMED_CONDITIONS test_project.py:563-577 (sigma symmetric and PD incl. singular; gamma; turnover limit; lower above upper; start sum, bound and cap; sector label range; sector without asset; one entry per asset). OTHER_SIDE_REFUSED :680-703 (indefinite Sigma, negative Sigma, extra cap, label below range, gamma and turnover just below zero, lower over upper by 1e-12, list one too many). NaN or infinity :733-741; missing field :744-750; non-mapping :753-757; no assets :760-770; list one short or long :773-787. Valid boundaries: gamma 1e-6 (:566, :582), turnover 0 (:568), bound and cap equal to start (:587-598, :613-619), start sum inside 1e-9 on both sides (:470-477, :604). ValueError is demanded only for named conditions; other invalid inputs use Exception (:792-839). Reference passes all of them (run_graders_0-49.log). See PRJ-D1-38 for the gamma 1e-9 test.")
row("PRJ-D1-11", "2.6 spec: purity and silence; stdlib only", "project.html:327, 330", "PASS",
    "test_project.py:1032-1051 (argument unchanged, nothing printed, no warnings, deterministic); :268-282 (stdlib only, no grader import). The reference passes on seeds 0-49.")
row("PRJ-D1-12", "2.6 grading paragraph: 363 checks and the listed families", "project.html:332", "PASS",
    "pytest --collect-only: 363 on each of seeds 0-49 (collect_seeds.log; starter_and_counts_out.log reports one value over 50 seeds). Three comparators at 0.25, 0.5, 0.75 (test_project.py:372-384). Five hand-worked cases (:218-246, each with KKT and certificate checks :393-407). Non-finite values in the eight numeric fields (:733). Missing field, non-mapping, no assets, short and long lists (:744-790). Purity (:1032-1051).")
row("PRJ-D1-13", "2.5 Lab 1: output, prose, numbers", "project.html:53-168", "PASS",
    "Twin tests/labs/M7/lab-M7-project-1.py run alone under python -I -W error: exit 0, output equal to the page's expected block (twin_project-1.out; run_labs M7 PASS). Recomputed by hand: budget-only weights 54/65, 5/26, -3/130 sum to 1; asset 3 held; answer (9/11, 2/11, 0); nu = -21/1100; lower multiplier 9/1100; objective -3/220 = -0.013636... Interpretation sentences match the output. The round-2 insertion at line 167 ('(Proposition, in the Rung 3 specification below)') points to the Proposition at project.html:323, which is in the Rung 3 section.")
row("PRJ-D1-14", "2.5 Lab 2: completion problem", "project.html:170-285", "PASS",
    "Three blanks (lines 250, 261, 262), each matching the prose; the completed twin reproduces Lab 1 output line for line (twin_project-2.out); run_labs checks the blank lines against the twin (run_labs M7 PASS).")
row("PRJ-D1-15", "2.5 Lab 3: certificate numbers and prose", "project.html:372-445", "PASS",
    "Twin output: check A all zero; check B stationarity 9/550 and dual 9/1100; check C stationarity 1/6250, primal 0, dual 0, CS 0. Re-derived by hand: check B stationarity = 9/1100 - (-9/1100) = 9/550; check C gradient change = gamma*Sigma*(1/1000, -1/1000, 0) = (6e-5, -1.6e-4, -4e-5), largest 1.6e-4 = 1/6250. The interpretation sentences match (twin_project-3.out).")
row("PRJ-D1-16", "2.9 / 2.6: hours arithmetic", "project.html:33, 338-354; index.html:29, 39-42, 141; L01-L08 data-hours", "PASS",
    "Lessons 9+9+10+10+10+10+9+10 = 77 (L01..L08 data-hours). Hub data-hours-lessons=77, data-hours-project=33, 110 total (index.html:29, 141). Project table 2+3+10+6+7+5 = 33 (project.html:344-350) equals data-hours-project. curriculum/curriculum.json M7 hours = 110.")
row("PRJ-D1-17", "2.6 / BUILDER 5.1: four-rung ladder", "project.html:40-49", "PASS",
    "Rung 1 = Lab 1 (solved and annotated); Rung 2 = Lab 2 (three blanks, checked against the completed output); Rung 3 = specification, autograder and Lab 3; Rung 4 = three open-ended stretch items (project.html:455-459).")
row("PRJ-D1-18", "2.6 spec completeness (questions a student would ask)", "project.html:288-336", "PASS",
    "Questions a competent student would still have, each answered on the page: sign convention of the multipliers (line 310: Lagrangian of L03, g <= 0); which t the certificate uses (line 311: t_i = |d_i|); how multipliers of inactive constraints are set (lines 317-318: non-negative, zero unless the constraint binds); the result type ('numbers', line 299; 'exact arithmetic' permitted, line 330). The result-type gap between the page and the grader is a grader defect (PRJ-D2-01), not a spec gap.")
row("PRJ-D1-19", "BUILDER 1.3-1.4: banned strings and phrases", "project.html (whole)", "PASS",
    "scripts/M7-d-r2/scan_banned_r2.py (scan_banned_r2.log): no hits for TODO, TBD, lorem, ellipsis, for brevity, details omitted, beyond the scope, left as an exercise, you can add more, it is important to note, studies show, experts agree, it is well known, obviously, clearly, about N, roughly, historically, in summary.")
row("PRJ-D1-20", "2.5 / 2.9: page_smoke (console, requests, labs in Pyodide)", "project.html", "PASS",
    "tools/page_smoke.py --unit M7 --pages project: 'modules/M/M7/project.html: PASS' (page_smoke_project_r2.log). In-browser grader on the reference: 'All 363 tests pass on seed 336472356 (2.0 s)'. Labs in Pyodide 0.0 s each. Zero console errors and external requests reported. Note: the first attempt used --pages project.html, which matches no page and passed vacuously; it was re-run with the page name.")
row("PRJ-D1-21", "2.4: notation vs notation/notation.json", "project.html:292-336", "PASS",
    "notation.json registers T, Phi, gamma_3, gamma_4, R*, R^e*, R_f, Q. None appears on the page. The page uses only standard TeX commands (\\sum, \\le, \\Sigma, \\tau, \\gamma, \\lambda, \\nu, \\mu, \\alpha, \\beta, \\eta, \\kappa, \\top, \\tfrac, \\in, \\ne, \\square); no registered macro is needed. Local letters are defined on the page (line 295 for n and Z; line 305 for gamma, mu, Sigma, w0, l, u, c_k, S_k, tau, d_i, t_i; lines 309-310 for the multipliers).")
row("PRJ-D1-22", "2.9 / BUILDER 1.10: DAG and concept use", "project.html:292, 309-310, 456", "PASS",
    "check_dag.py --unit M7 PASS (gates_M7_r2.log). 'Lagrangian (defined in Lesson 3)': L03.html:62 gives L = f + sum lambda_i g_i + sum nu_j h_j for g_i <= 0, consistent with project.html:310. envelope-theorem link: defined in M2 (M2/L22.html), a prerequisite of M7 (curriculum prereqs M2, M3).")
row("PRJ-D1-23", "2.9 / rule 12: process words in learner text", "project.html:320, 325", "FAIL",
    "Learner text narrates the authoring QA: line 320 '(50 of 50, checked for this page against the reference's output)' and 'no mutant of the reference separates it from its absence; the mutation suite does not test it'; line 325 'A reference solution was checked on seeds 0 to 49 only'. Scan: scripts/M7-d-r2/scan_banned_r2.log.",
    fix="Replace the authoring frame with the fact it reports, for example at line 320: 'On seeds 0 to 49 the reference solution's smallest inequality multiplier is zero in 50 of 50 cases.' Drop 'the mutation suite does not test it' and 'no mutant of the reference separates it from its absence' (or state the equivalence as a mathematical fact). At line 325 replace 'A reference solution was checked on seeds 0 to 49 only' with 'On seeds 0 to 49 the reference solution's multipliers pass every check in 50 of 50 cases.'")
row("PRJ-D1-24", "2.6 local-run instructions and decode command", "project.html:364-366", "PASS",
    "Workspace with test_project.py, instance.py and the reference as constrained_allocator.py: QF_SEED=0 pytest -q -p no:cacheprovider --assert=plain -W error test_project.py runs and collects 363 (collect_seeds.log). The page's decode command run verbatim with seed 0 prints the case dictionary (decode_cmd_seed0.log, exit 0). Only the standard library and pytest are needed (instance.py imports json, random, typing).")
row("PRJ-D1-25", "2.6 autograder 1: run_graders on reference; starter fails", "grader/reference.py; grader/starter.py", "PASS",
    "tools/run_graders.py --unit M7 --seeds 0-49: 'run_graders M7: PASS (reference 50/50 seeds, slowest 3.3 s)' (run_graders_0-49.log). Starter: suite exit 1, 360 failed and 3 passed (starter_and_counts_out.log); the page says the suite fails on the starter (line 301).")
row("PRJ-D1-26", "2.6 autograder 2: instances valid and materially different", "grader/instance.py:34-68", "PASS",
    "Deterministic (run_graders). Seeds 0-19 give 20 distinct reference answers and 12 distinct (n, sector-label) structures (starter_and_counts_out.log). Valid: the reference's validation accepts every seed 0-299 (active_set_count.py calls _parse on each).")
row("PRJ-D1-27", "2.6 autograder: standard library only", "reference.py:11-18; test_project.py:268-282", "PASS",
    "reference.py imports math, collections.abc, dataclasses, fractions, itertools, typing. test_only_standard_library_imports passes on the reference on seeds 0-49. instance.py imports json, random, typing.")
row("PRJ-D1-28", "2.6 autograder 4: failure messages name the property and never leak the answer", "grader/test_project.py (all assert messages)", "PASS",
    "Every assert message read. Each names a property (budget, box, sector cap, turnover, dual feasibility, stationarity in weights or auxiliaries, complementary slackness, certificate field, named condition, refusal) and none prints an expected value. The suite runs with --assert=plain (test_project.py:5), so pytest shows only the failing source line.")
row("PRJ-D1-29", "2.6 autograder: mypy --strict and ruff", "grader/reference.py, instance.py, starter.py; tests/labs/M7/*.py", "PASS",
    "mypy_M7_r2.log: mypy --no-incremental --strict on reference.py, instance.py, starter.py and the three project-lab twins: 'Success: no issues found in 6 source files'; with MYPYPATH over all M7 lab twins and grader files: 'Success: no issues found in 14 source files'. ruff_M7_r2.log: ruff check and ruff format --check clean on grader and labs. test_project.py imports the learner's module, so it is outside the plan's mypy command (plans/M7-build-plan.md:378).")
row("PRJ-D1-30", "2.5 labs: pytest on lab twins", "tests/test_labs.py -k M7; tests/labs/M7/lab-M7-project-1..3.py", "PASS",
    "pytest tests/test_labs.py -k M7: 11 passed (pytest_labs_M7_r2.log). run_labs --unit M7: 11/11 PASS (gates_M7_r2.log).")
row("PRJ-D1-31", "2.6 autograder 5: same suite in Pyodide and locally", "project.html:359; test_project.py:3-5", "PASS",
    "Local: 363 pass on the reference for seeds 0-49. Browser: All 363 tests pass on seed 336472356 (page_smoke_project_r2.log). Same flags in both: -p no:cacheprovider --assert=plain -W error.")
row("PRJ-D1-32", "2.6 atlas milestone", "project.html; curriculum/curriculum.json M7", "PASS",
    "check_projects.py --unit M7 PASS (gates_M7_r2.log). The M7 curriculum entry declares no atlas milestone; project.html has no atlas reference.")
row("PRJ-D1-33", "2.1 / 2.6 reading list: registry keys", "project.html:465-466", "PASS",
    "boyd2004convex and stokey1989recursive exist in references/references.json. verify_refs.py --unit M7 (live): '2 of 560 entries, 0 problems' (verify_refs_M7_live_r2.log). verify_refs.py --offline: 560 entries, 0 problems (verify_refs_offline_r2.log). Plain curl to api.crossref.org for both DOIs (crossref_reading_r2.log): Convex Optimization, Boyd and Vandenberghe, 2004; Recursive Methods in Economic Dynamics, Stokey, Lucas and Prescott, 1989. The reading list makes no attributed claim.")
row("PRJ-D1-34", "2.6 hours: own estimate per component", "project.html:344-350", "PASS",
    "My estimates: Rung 1 about 2 h; Rung 2 about 2.5 h; core solver 8-12 h (about 10); linear constraints 5-8 h (about 6.5); certificate and own tests 5-8 h (about 6.5); self-check 4-6 h (about 5). Midpoint total 32.5 h against the declared 33 h, about 2% apart (threshold 30%).")
row("PRJ-D1-35", "2.6 autograder 3: every mutant killed", "ledgers/M7/mutants/*.py (129 files)", "PASS",
    "tools/mutate_graders.py --unit M7 --seeds 0-9 (mutate_M7_r2.log): 129/129 KILLED, 'mutate_graders M7: PASS (129/129 killed)'. Each kill is listed in the mutants array of this fragment.")
row("PRJ-D1-36", "2.6 autograder 3: at least three new student-error mutants by this verifier", "ledgers/M7/mutants/d2_01..d2_03", "PASS",
    "Round 2 wrote d2_01_sector_membership_taken_from_position_not_label (killed by test_named_condition_is_refused_with_value_error[start-within-sector-cap-invalid], seed 0), d2_02_complementary_slackness_turnover_rows_at_zero_displacement (test_certificate_agrees_with_the_recomputed_residuals, seed 0) and d2_03_negative_turnover_multipliers_never_dropped (test_named_condition_boundary_is_accepted[gamma-positive-zero-boundary], seed 1). Written by scripts/M7-d-r2/make_mutants.py, which asserts each edit matches once. Round 1 added d1_01..d1_04.")
row("PRJ-D1-37", "2.6 mutation: dual-residual floor not tested (project.html:320)", "grader/test_project.py:108, 356-362; reference.py:287", "PASS",
    "Equivalence argument, not a surviving mutant. (a) On every reference output the smallest inequality multiplier is exactly 0 (PRJ-D1-06), so a solver without the floor that reports -min equals the reference. (b) Every suite instance has an asset with lower < upper (instance.py:47-48 gives lower <= 0 < 0.35 <= upper; the hand cases also have lower < upper), and no KKT vector can make both its lower and upper multipliers positive, so every valid KKT output has smallest multiplier 0. (c) A student output whose smallest multiplier exceeds 1e-9 reports -min, which differs from the recomputed value (0) by more than the 1e-9 agreement tolerance, and fails test_certificate_agrees_with_the_recomputed_residuals. The page's sentence that the mutation suite does not test the floor is accurate.")
row("PRJ-D1-38", "2.6 autograder: five alternative correct implementations pass seeds 0-49", "ledgers/M7/scripts/M7-d-r2/alts/alt1..alt5.py", "PASS",
    "make_alts.py builds five stdlib-only allocators: alt1 float, sign forms, most-negative drop, pre-pass; alt2 float, sign forms, smallest-index drop, no pre-pass; alt3 float, explicit t (2n variables), most-negative drop; alt4 exact Fraction, sign forms, most-negative drop, no pre-pass; alt5 exact, explicit t, smallest-index drop. Each has its own solver and float certificate. Unchanged suite via run_alts.py on seeds 0-49: alt1 50/50, alt2 50/50, alt3 50/50, alt4 50/50, alt5 50/50 (alt_alt1..5_seeds_0-49.log). The float alternatives first failed on the gamma 1e-6, gamma 1e-9 and PD-boundary tests and on seeds 8 and 33 (the budget or turnover check failed beyond 1e-8 at gamma 1e-9). Those failures came from absolute pivot cutoffs, an unrefined solve and a blocking threshold that ignored the size of the step; with relative cutoffs, a relative threshold and two rounds of iterative refinement they pass, so the suite is satisfiable by a float method. The alternatives reuse the reference's validation (reference.py:1-124), so validation over-constraint is judged by reading (PRJ-D1-10).")
row("PRJ-D1-39", "2.9 / BLUEPRINT 7: reference.py excluded from deployment", "course/modules/M/M7/grader/reference.py; BLUEPRINT.md:400-401; plans/M7-build-plan.md:408 (T6)", "FAIL",
    "reference.py lies in the deployable course/ tree. The repository has no exclusion: no .vercelignore, no vercel.json, no package.json, and .github/workflows/ci.yml has no publish step that removes it (ls -la at the checkout root; grep for reference in .github and tools finds only run and check steps). BLUEPRINT.md:400-401 requires that deployment 'excludes every grader/reference.py'; plan T6 repeats it.",
    fix="Add the exclusion to the deployment configuration (for example a .vercelignore entry or a build step that removes course/**/grader/reference.py, and any alternates), and add a check to tools/check_projects.py that fails when the exclusion is missing. This is repo-wide (every autograded unit), not specific to M7.")
row("PRJ-D2-01", "2.6 autograder over-constraint: exact-arithmetic output rejected", "grader/test_project.py:136-138, 289-293; project.html:330", "FAIL",
    "project.html:330 allows 'exact arithmetic ... as long as the returned numbers satisfy the definitions'. The variant alts/alt4_fraction_output.py returns its Fraction weights and certificate. On seed 0 the suite gives 344 failed, 19 passed (alt4_fraction_output_pytest_seed0.log): 343 times 'every weight must be a real number.' (test_project.py:136-138) and once 'every returned number must be real.' (test_project.py:292) for the Fraction certificate. The same solver converted to float passes 50/50 (alt4, PRJ-D1-38).",
    fix="Accept numbers.Real (excluding bool) in test_project.py:136-138 and :292 (and in the certificate check), or narrow the permission at project.html:330 to int and float outputs and say so on the page.")
row("PRJ-D2-02", "2.9 scope claim", "project.html:450", "PASS",
    "'does not test the answer for any problem other than the cases it generates and the hand-worked cases it lists': the suite generates variants of the seed case (case_copy and changed, test_project.py:44-55) and checks KKT on them (boundary variants :587-606, :613-630, :713-718, :898-907). The sentence is accurate under that reading.")
row("PRJ-D2-03", "2.6 code comment: iteration cap", "grader/reference.py:206", "PASS",
    "The comment says the search uses at most 12 iterations on seeds 0-49. Instrumented count of loop passes over seeds 0-49: maximum 12 (iter_count_out.log).")
row("PRJ-D2-04", "2.4 test comments: hand-worked answers", "grader/test_project.py:219-244", "PASS",
    "Re-derived: budget only gives w = mu + 0.3 = (0.6, 0.4) with nu = -0.3; zero turnover gives w = w0; single asset gives w = 1; upper bound binding gives budget-only (0.35, 0.65), cut to (0.7, 0.3), turnover 0.2 <= 0.5 not binding; turnover binding gives budget-only (0.7, 0.3), cut to (0.6, 0.4), a change of 0.1 each way (the objective is 0.02 at (0.6, 0.4) and 0.10 at (0.4, 0.6)). All five pass the reference.")
row("PRJ-D2-05", "2.4 test comment: starting portfolio as the answer", "grader/test_project.py:376-378", "PASS",
    "ref_seeds.py: the exact answer equals the starting portfolio on seeds 162, 163, 182, 267 and no others among seeds 0-299 (ref_seeds_out.log).")
row("PRJ-D2-06", "2.4 test comments: eigenvalue and definiteness cases", "grader/test_project.py:426, 431, 440", "PASS",
    "All-0.01 Sigma has a zero second LDL pivot (singular). 0.01 J + 0.0001 I has smallest eigenvalue 0.0001 (J has eigenvalues N and 0). [[0.01, 0.02], [0.02, 0.01]] has eigenvalues 0.03 and -0.01 (indefinite). Each is refused by the reference (run_graders_0-49.log).")
row("PRJ-D2-07", "2.4 instance docstring", "grader/instance.py:1-11, 57", "PASS",
    "Every input has at most three decimals (instance.py:38-48, 54-55 and 66: divisions by 1000 or 100). Feasible by construction: the reference's _parse, which checks budget, box and sector caps, accepts every seed 0-299 (active_set_count.py). The label contains SIMULATED (instance.py:57).")
row("PRJ-D2-08", "2.4 cross-reference: Lagrangian sign convention", "project.html:310; course/modules/M/M7/L03.html:62", "PASS",
    "L03.html Definition 1.1 gives (P) with g_i(x) <= 0 and L = f + sum lambda_i g_i + sum nu_j h_j. The page's L = f + sum lambda g + nu(sum w - 1) with lambda >= 0 uses the same convention, and the residual formulas (PRJ-D1-04) follow from it.")

mutants = []
pat = re.compile(r"^KILLED (\S+)\.py: (.*) -> (.*)$")
for line in (REPO / "ledgers/M7/scripts/M7-d-r2/mutate_M7_r2.log").read_text(encoding="utf-8").splitlines():
    m = pat.match(line)
    if m:
        mutants.append({"id": m.group(1), "description": m.group(2), "killed_by": m.group(3)})
survivors = [line for line in (REPO / "ledgers/M7/scripts/M7-d-r2/mutate_M7_r2.log").read_text(encoding="utf-8").splitlines() if line.startswith("SURVIVED")]
assert len(mutants) == 129 and not survivors, (len(mutants), survivors)

fragment = {
    "unit": "M7",
    "slice": "M7-d",
    "round": 2,
    "verifier": "Claude Haiku 5.5, independent verifier for M7-d, round 2 (did not build M7-d; works in its own checkout)",
    "pin": "c737272f5bdef4a027417989cd52254555e8a0bb",
    "base": "d0f39c09598ffefaf0ec18d5d1077cfacd42998b (round-1 pin). Slice delta since that pin: course/modules/M/M7/project.html line 167 (inserted '(Proposition, in the Rung 3 specification below)') and line 320 (floor sentence now 'seeds 0 to 49 (50 of 50, checked for this page against the reference's output)'); ledgers/M7/mutants gained the round-1 files d1_01..d1_04. grader/, tests/labs/M7/, tools/ and the M7 lessons are unchanged in the slice. Round-1 PASS rows whose subject changed were re-verified; no row was carried.",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyD2-M7-d",
    "scratch": "/tmp/m7d-r2-collect-*, /tmp/m7d-r2-fraction, /tmp/m7d_dbg*.py (no row depends on them; every row's script is under ledgers/M7/scripts/M7-d-r2/)",
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "verdict": "FAIL",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "Round 2 on c737272. Read in full: project.html (483 lines), grader/test_project.py (1051 lines), grader/reference.py, grader/instance.py, grader/starter.py, and the three project-lab twins. "
        "Every round-1 row was re-verified from scratch (none carried). Fails: PRJ-D1-23 (process words, line 320/325), PRJ-D1-39 (reference.py not excluded from deployment; repo-wide, no config in repo), PRJ-D2-01 (grader rejects exact Fraction outputs that project.html:330 permits; 344 of 363 checks fail). "
        "Round-1 FAIL PRJ-D1-39 remains. Round-1 UNVERIFIABLE PRJ-D1-38 is now PASS (five alternatives, 50/50 each). "
        "Not checked: a live Pyodide run on seeds 0-49 (page_smoke ran the browser grader once, seed 336472356); the full repository CI gate (targeted per the user's testing rule, since only M7 project files changed); any deployment configuration outside this repository, so the PRJ-D1-39 exclusion cannot be confirmed from here; the hours estimate is the verifier's judgement, not a measurement. "
        "gamma 1e-9 (test_project.py:605) is stricter than the 1e-6 named on page line 326; it is accepted because the page says valid forms sit 'on the limit or just inside it'; the grading paragraph at page line 332 does not list it, so the page could say so explicitly."
    ),
    "summary": "",
}
counts = {"PASS": 0, "FAIL": 0, "UNVERIFIABLE": 0}
for r in rows:
    counts[r["status"]] += 1
fragment["summary"] = (
    f"M7-d round 2: verdict FAIL. Rows {len(rows)}: PASS {counts['PASS']}, FAIL {counts['FAIL']}, UNVERIFIABLE {counts['UNVERIFIABLE']}. "
    f"Mutants {len(mutants)}/{len(mutants)} killed (seeds 0-9). Alternatives 5/5 pass seeds 0-49. Non-PASS: PRJ-D1-23, PRJ-D1-39, PRJ-D2-01."
)
problems = ledger.validate(fragment, "M7-d")
print("validate:", problems)
out = REPO / "ledgers/M7/M7-d.json"
out.write_text(json.dumps(fragment, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("wrote", out, counts, "mutants", len(mutants))
