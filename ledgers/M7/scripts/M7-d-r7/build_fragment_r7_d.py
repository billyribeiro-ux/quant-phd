"""Build ledgers/M7/M7-d.json (round 7, slice d) from the round-7 evidence in this checkout. Run with python -I."""
import json, re, datetime, sys
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyD7-M7-d")
S = "ledgers/M7/scripts/M7-d-r7"
rows = []

def row(id_, check, location, status, evidence, fix=None):
    r = {"id": id_, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    rows.append(r)

P = "project.html"
G = "course/modules/M/M7/grader"

row("PRJ-D1-01", "2.6-spec", f"course/modules/M/M7/{P}:292-295; {G}/instance.py:14-68",
    "PASS", f"{S}/instances_check.py + instances_check.log: all 50 seeds 0-49 valid (n=3:18, n=4:14, n=5:18; Z=2 with both sectors occupied; w0 sums to one, lies in box and caps; Sigma symmetric and positive definite); 50 distinct answers. test_instance_is_simulated_and_deterministic passes.")
row("PRJ-D1-02", "2.6-spec", f"course/modules/M/M7/{P}:299-300; {G}/test_project.py:127-154",
    "PASS", "output_shape checks keys, lengths and types of weights, seven multiplier names, four certificate keys (test_project.py:127-154); run_graders.log: reference passes 50/50 seeds; collect-only 363 on each seed (collect_all_seeds.log).")
row("PRJ-D1-03", "2.4-math", f"course/modules/M/M7/{P}:309",
    "PASS", "Re-derived by hand: if sum|d_i| <= tau then t_i=|d_i| meets t_i>=d_i, t_i>=-d_i, sum t_i<=tau; converse sum|d_i| <= sum t_i <= tau. Equivalence holds in both directions.")
row("PRJ-D1-04", "2.4-math", f"course/modules/M/M7/{P}:310-313; {G}/test_project.py:86-104; {G}/reference.py:303-309",
    "PASS", "Signs re-derived from L = f + sum lambda_j g_j with g = l-w, w-u, sum_S w - c, d-t, -d-t, sum t - tau: w-stationarity gives -lambda^l, +lambda^u, +eta, +alpha, -beta; t-stationarity gives kappa-alpha-beta. test_project.py stationarity() and reference.py _certificate implement the same; both pass 50/50 seeds.")
row("PRJ-D1-05", "2.4-math", f"course/modules/M/M7/{P}:314-319; {G}/test_project.py:107-118; {G}/reference.py:262-315",
    "PASS", "recomputed_certificate (test_project.py:107-118) and reference _certificate (reference.py:262-315) implement the four definitions as written; reference passes the agreement test on seeds 0-49 (run_graders.log).")
row("PRJ-D1-06", "2.4-math", f"course/modules/M/M7/{P}:320 (first two sentences)",
    "PASS", "dual residual = max(0, -min m) (test_project.py:110) changes its value only when the smallest inequality multiplier is positive (every multiplier positive), as stated.")
row("PRJ-D1-07", "2.4-math", f"course/modules/M/M7/{P}:317-321; {G}/test_project.py:37,184-208,377-386; {G}/reference.py:21",
    "PASS", "TOL = 1e-8 for feasibility, stationarity, complementary slackness and the certificate bound (test_project.py:37, 382-386); agreement 1e-9 (test_project.py:377); starting-portfolio tolerance 1e-9 (reference.py:21, _parse lines 102-108). Values match the page text.")
row("PRJ-D1-08", "2.4-math", f"course/modules/M/M7/{P}:322-325 (Proposition, proof, hypotheses)",
    "FAIL", "Proposition and proof are otherwise sound (checked: L convex, stationarity gives global minimum of L, f(y) >= L(y,s) >= L(w,t) = f(w), midpoint argument for uniqueness). But the proof proves the bound for feasible PAIRS (y,s) and concludes f(y) >= f(w) for feasible y. The step that every feasible weight vector y has a feasible s (s_i = |y_i - w0_i|, from the linearization equivalence in Conventions, project.html:309) is not written in the proof; the uniqueness argument has the same implicit step when it forms (w',t').",
    fix="Add one sentence to the proof before 'For any feasible (y, s)': 'Every feasible weight vector y extends to a feasible pair, namely s_i = |y_i - w_{0,i}|, by the linearization equivalence above; so the bounds below apply to every feasible y, and in the uniqueness step to (w', t').'")
row("PRJ-D1-09", "2.4-math", f"course/modules/M/M7/{P}:325; {G}/instance.py:38-43",
    "PASS", "instance.py:38-43 builds factor entries as randint(-2,2) and Sigma = (A'A + I)/1000, so x'Sigma x = (|Ax|^2 + |x|^2)/1000 > 0; instances_check.log: Sigma positive definite on all 50 seeds (LDL pivots). The page's 'existence of multipliers is not proved' sentence is honest and matched by the reference finding multipliers on 50/50 seeds.")
row("PRJ-D1-10", "2.6-spec", f"course/modules/M/M7/{P}:326; {G}/reference.py:54-109; {G}/test_project.py:580-720",
    "PASS", "Each named condition (not a mapping, missing field, NaN/inf, no assets, list length, Sigma symmetric and PD, gamma>0, turnover<0, lower>upper, start sum/bounds/caps, sector label range, sector without asset or cap) has a refused test with ValueError (NAMED_CONDITIONS 12 entries and OTHER_SIDE_REFUSED 22 entries; pytest collect count 363 and passing). reference.py raises at the named lines.")
row("PRJ-D1-11", "2.6-spec", f"course/modules/M/M7/{P}:326-327; {G}/test_project.py:617-660,1049-1068",
    "PASS", "Valid forms accepted: boundary tests for bound/cap equal to start, turnover 0, gamma 1e-6 and 1e-9, start sum inside 1e-9 both sides; purity and silence tests (test_project.py:1049-1068) pass for reference and for alternatives A and B.")
row("PRJ-D1-12", "2.6-spec", f"course/modules/M/M7/{P}:332; {G}/test_project.py:389-401,409-420",
    "PASS", "collect_all_seeds.log: 363 tests on every seed 0-49 (equal to the page's 363). Comparators at 0.25, 0.5, 0.75 (test_project.py:389); five hand cases (HAND_CASES, 5 entries, test_project.py:227-255); -W error in pytestmark (test_project.py:34).")
row("PRJ-D1-13", "2.5-lab", f"course/modules/M/M7/{P}:53-168; tests/labs/M7/lab-M7-project-1.py",
    "PASS", "extract_page_labs.log: page code equals the twin. twin run under python -I -W error exits 0; its output equals the page's expected block (diff empty). Numbers in interpretation (54/65, 5/26, -3/130, 9/11, 2/11, -21/1100, 9/1100, -3/220, about -0.013636) match the output.")
row("PRJ-D1-14", "2.5-lab", f"course/modules/M/M7/{P}:170-285; tests/labs/M7/lab-M7-project-2.py",
    "PASS", "Page code differs from the twin only at the three blanks (___ at residual, signs, dual_feasible); twin output equals the expected block; interpretation claims about the blanks (sign test, gradient plus budget multiplier) match the code.")
row("PRJ-D1-15", "2.5-lab", f"course/modules/M/M7/{P}:372-445; tests/labs/M7/lab-M7-project-3.py",
    "PASS", "Page code equals twin; twin output equals expected block. Hand check: candidate B stationarity = 2*(-9/1100) = -9/550, dual = 9/1100; candidate C: gradient change (6e-5, -16e-5, -4e-5) gives max 1.6e-4 = 1/6250; primal and complementary residuals zero in B and C.")
row("PRJ-D1-16", "2.9-structure", f"course/modules/M/M7/{P}:33,338-354; course/modules/M/M7/index.html; curriculum/curriculum.json (M7 hours 110)",
    "PASS", "Time-budget rows 2+3+10+6+7+5 = 33 = data-hours-project. Lessons declare 9,9,10,10,10,10,9,10 (= 77, per the hub). 77 + 33 = 110 = curriculum M7 hours.")
row("PRJ-D1-17", "2.9-structure", f"course/modules/M/M7/{P}:40-49",
    "PASS", "Ladder has four rungs: Rung 1 worked example (lab 1, long-only), Rung 2 completion (lab 2), Rung 3 independent project (spec, autograder, lab 3), Rung 4 stretch. Each rung text matches the content it names.")
row("PRJ-D1-18", "2.9-structure", f"course/modules/M/M7/{P}:288-336",
    "PASS", "Spec sections present in the order Context, Inputs, Required outputs, Constraints, Grading, Reading list (project.html:291-334). Context is four sentences (BUILDER_RULES 5.2). check_pages M7: PASS.")
row("PRJ-D1-19", "2.9-structure", f"course/modules/M/M7/grader/*.py",
    "PASS", "grader/ contains instance.py, reference.py, starter.py, test_project.py. starter.py: allocate raises NotImplementedError; running the suite on it gives 360 failures (grader_suite.sh starter run).")
row("PRJ-D1-20", "2.9-structure", f"course/modules/M/M7/{P}; tools/page_smoke.py",
    "PASS", "page_smoke.py --unit M7 --pages project: PASS (log page_smoke_project.log); in-browser grader: 363 tests pass on the seed it used; labs run 0.0 s each.")
row("PRJ-D1-21", "2.4-notation", f"course/modules/M/M7/{P}; notation/notation.json",
    "PASS", "TeX macros on the page: sum, Sigma, le, gamma, tau, ge, lambda, top, tfrac, mu, nu, in, alpha, beta, eta, kappa, ne, square. None is a registered macro (\\E, \\R, \\N, ...). Registered symbols T, Phi, gamma_3, gamma_4, R*, R^{e*}, R_f, Q do not occur. Local letters (gamma, mu, Sigma, N) are local per notation.json 'about'.")
row("PRJ-D1-22", "2.9-structure", f"course/modules/M/M7/{P}:456; course/concepts.html (envelope-theorem)",
    "PASS", "check_dag M7: PASS (check_dag_all.log). The only concept link is envelope-theorem; the anchor exists in course/concepts.html and is defined in M2 L22; M2 is in M7's prerequisite closure {M1, M2, M3, P0.1}.")
row("PRJ-D1-23", "2.9-prose", f"course/modules/M/M7/{P}:320 (last sentences)",
    "PASS", "Round-6 FAIL is resolved. The sentence now reads 'an unfloored report fails it only when the smallest inequality multiplier exceeds 1e-9'. Agreement test is |reported - recomputed| <= 1e-9 (test_project.py:377), recomputed = 0 when all multipliers are positive, so an unfloored report -m fails exactly when m > 1e-9 (necessary-condition claim holds). Experiment: floor_sentence_r7.log (no reference answer on seeds 0-49 has all multipliers positive; the sentence is the arithmetic of the test).")
row("PRJ-D1-24", "2.6-spec", f"course/modules/M/M7/{P}:358-366; {G}/test_project.py:5",
    "PASS", "The page's local command runs (QF_SEED=0 with the same flags, 363 passed). The decode command 'python3 -c ... make_instance(...)' prints the case when run without -I (run from the grader folder).")
row("PRJ-D1-25", "2.6-autograder", f"{G}/reference.py; {G}/starter.py; {G}/test_project.py",
    "PASS", "run_graders.log: reference 50/50 seeds PASS; starter fails 360 tests; mutate_graders run killed every mutant.")
row("PRJ-D1-26", "2.6-autograder", f"{G}/instance.py:20-68",
    "PASS", "Deterministic per seed (test_instance_is_simulated_and_deterministic); decimals with at most 3 places (mu /1000, sigma /1000, w0 /100, caps /100); label contains SIMULATED; 50/50 seeds valid.")
row("PRJ-D1-27", "2.6-autograder", f"{G}/reference.py:20-21; {G}/test_project.py:37-43",
    "PASS", "REQUIRED fields and TOL in reference.py match the page; the constants TOL, FIELDS and CERTIFICATE_KEYS in the suite match the spec.")
row("PRJ-D1-28", "2.6-autograder", f"{G}/test_project.py (every assert message)",
    "PASS", "Read every assertion message: each names the property (budget, box, sector cap, turnover, dual feasibility, stationarity, complementary slackness, certificate, optimality) and none formats an expected or computed value (--assert=plain prints no locals). Hints name the concept to revisit.")
row("PRJ-D1-29", "2.6-autograder", f"{G}/*.py; tests/labs/M7/lab-M7-project-1..3.py",
    "PASS", "run_graders M7 seeds 0-49 PASS (reference 50/50); mypy --no-incremental (strict, whole project) reports no issues in 385 files (mypy_r7.log); ruff check and format clean on the grader and lab twins (ruff_slice_r7.log).")
row("PRJ-D1-30", "2.5-lab", "tests/labs/M7/lab-M7-project-1..3.py; tests/test_labs.py",
    "PASS", "run_labs M7: PASS (11/11) (run_labs_M7.log). pytest tests/test_labs.py tests/test_page_checks.py -k M7 exit 0 (pytest_M7_relevant_r7.log).")
row("PRJ-D1-31", "2.6-spec", f"course/modules/M/M7/{P}:359,365; {G}/test_project.py:5",
    "PASS", "The panel's data attributes name the suite, support and starter files that exist (instance.py, starter.py, test_project.py). The local-run instructions match the header of the suite.")
row("PRJ-D1-32", "2.6-atlas", f"course/modules/M/M7/{P}; atlas/ (A8, A15 contracts)",
    "PASS", "No atlas contract cites M7 (grep of atlas/*.contract.md for M7 returns nothing); the project is not an atlas milestone and the page does not claim one.")
row("PRJ-D1-33", "2.1-citations", f"course/modules/M/M7/{P}:465-466; references/references.json",
    "PASS", "Reading-list keys boyd2004convex and stokey1989recursive exist in references/references.json; verify_refs --offline: 560 entries, 0 problems (verify_refs_offline.log). The page gives no bibliographic data or locator from memory. The registry is not read per entry in this round (not in slice).")
row("PRJ-D1-34", "2.9-structure", f"course/modules/M/M7/{P}:344-350",
    "PASS", "Hours arithmetic: 2+3+10+6+7+5 = 33 = total row = data-hours-project (see PRJ-D1-16).")
row("PRJ-D1-35", "2.6-mutation", "ledgers/M7/mutants/ (all M7 mutants, 176 files)",
    "PASS", "mutate_graders.py --unit M7 --seeds 0-9 (mutate_M7_0-9_final_r7.log): 176/176 killed, exit 0. Includes the 171 existing mutants and r7_01..r7_05. (r7_06 is listed under PRJ-R7-01.)")
row("PRJ-D1-36", "2.6-mutation", "ledgers/M7/mutants/f6_01..f6_10, g2_*, m*, r13_*, r14_*, r15_*",
    "PASS", "Included in the 176/176 run (mutate_M7_0-9_final_r7.log); each is killed on seeds 0-9. The round-6 text-multiplier mutants f6_01..f6_10 are killed by the new type checks.")
row("PRJ-D1-37", "2.6-mutation", f"{G}/reference.py:203-241,287; ledgers/M7/mutants/v6_01, v6_02 (equivalents)",
    "PASS", "v6_01 (dual residual reported without the floor) is equivalent to the reference: the reference's working set has rank at most n including the budget, so at most n-1 inequality rows are active; at least n+1 lower/upper/sector rows have zero multipliers, so min <= 0 on every reference output and the floor is inactive. v6_02 omits turnover multipliers, which are non-negative, and min is zero whenever a box or sector multiplier is zero, so the dual residual is unchanged. Both are equivalent to the reference, not to a different valid answer (see PRJ-R7-01).")
row("PRJ-D1-38", "2.6-autograder", f"{S}/alt/altA..altE, altG, altH; {S}/alts_run_0-49.log, altG_run_0-49.log, altH_run_0-49.log",
    "PASS", "Two exact Fraction active-set solvers (A: tight start, last-added drop, last tie-break; B: empty start, most-negative drop) pass 50/50 seeds (363 passed each). Float variants with absolute or scaled cutoffs (C 1e-12, D 1e-10, E float search plus exact polish, G gamma-scaled, H budget-refined) fail only the three gamma boundary tests (alt_failing_tests_r7.log: 56 failing rows = gamma-just-inside-zero 28, gamma-positive-zero-boundary 14, gamma-positive-negative-boundary 14; causes: singular KKT pivots or budget residual above 1e-8 from rounding in steps of order 1/gamma). Verdict: the grader does not force an exact method; the page allows any method meeting the stated tolerances, and the failing variants are defective at valid inputs, not correct implementations. Not established: that a carefully scaled float method passes gamma = 1e-9.")
row("PRJ-D1-39", "2.9-structure", f"{G}/reference.py; BLUEPRINT.md:400-401; .github/workflows/ci.yml",
    "FAIL", "BLUEPRINT.md:400-401 requires deployment to exclude every grader/reference.py. The repo has no deployment configuration (find for vercel.json, .vercelignore, netlify.toml, wrangler.toml, Dockerfile, railway.* returns nothing), and ci.yml only runs checks and uploads screenshots. Nothing excludes reference.py from course/, which is the published tree; page_smoke.py:297 loads reference.py into the in-browser grader.",
    fix="Add the publication exclusion for course/**/grader/reference.py to the deployment configuration (or a build step that removes it from the published tree), and state it in the repo. This is a repo-level change outside this unit.")
row("PRJ-R4-01", "2.9-prose", f"{G}/test_project.py:378-386 (docstring and message)",
    "PASS", "Docstring of test_certificate_agrees_with_the_recomputed_residuals and the residual-within-tolerance message match the definitions (certificate is compared with the recomputation, not trusted).")
row("PRJ-R5-01", "2.4-math", f"course/modules/M/M7/{P}:456 (frontier bullet)",
    "PASS", "The bullet asks the learner to state the sign convention and check numerically; it makes no sign claim of its own.")
row("PRJ-R5-02", "2.6-spec", f"{G}/test_project.py:223 (comment); :346-348 (message)",
    "PASS", "Comment on the budget-only case (w = mu + 0.3 with nu = -0.3) is correct; the message names the dual-feasibility property.")
row("PRJ-R5-03", "2.9-prose", f"course/modules/M/M7/{P}:450",
    "PASS", "'No case reads a data file, and every case carries the SIMULATED label': every make_instance case and every hand case carries the label (checked in the grader code).")
row("PRJ-R5-04", "2.9-structure", f"course/modules/M/M7/{P}:349-350",
    "PASS", "Hours rows match the arithmetic in PRJ-D1-16.")
row("PRJ-R5-05", "2.6-mutation", "ledgers/M7/mutants/r5_01..r5_05",
    "PASS", "Included in the 176/176 killed run (mutate_M7_0-9_final_r7.log).")
row("PRJ-R6-01", "2.6-mutation", "ledgers/M7/mutants/v6_01, v6_02 (equivalent)",
    "PASS", "Equivalence proof re-derived under PRJ-D1-37.")
row("PRJ-R6-02", "2.6-spec", f"{G}/test_project.py:148-151,300-311; {P}:300",
    "PASS", "Type checks now in place: budget, turnover_total, and every entry of lower, upper, sector, turnover_plus, turnover_minus must be a real non-bool number (test_project.py:148-151, 300-311). The round-6 failure (text, boolean and complex multipliers passed) is resolved; f6_01..f6_10 are killed in the 176/176 run.")
row("PRJ-R6-03", "2.6-mutation", "ledgers/M7/mutants/v6_03..v6_06",
    "PASS", "Included in the 176/176 killed run (mutate_M7_0-9_final_r7.log).")
row("PRJ-R7-01", "2.6-mutation", f"{G}/test_project.py:227-255 (HAND_CASES) and :410-424 (test_hand_case_matches_its_worked_answer); ledgers/M7/mutants/r7_06_unfloored_dual_residual_on_degenerate_positive_multipliers.py",
    "FAIL", f"Surviving student error r7_06 (reports the unfloored dual residual, with all-positive multipliers on a valid degenerate case: two assets, lower = upper = start, zero turnover, sector cap = start). project.html:320 states that an unfloored report fails the agreement check when the smallest multiplier exceeds 1e-9. r7_06 passes the suite on seeds 0 and 9 (grader_suite.sh run, both 'passed'). The suite never contains an instance on which a valid answer has all-positive inequality multipliers, so the floor path is never exercised. Verified: with the degenerate hand case added to HAND_CASES in a scratch copy, r7_06 fails ('1 failed, 363 passed') and reference.py passes ('364 passed'). See {S}/floor_degenerate_r7.py and the patched run.",
    fix="Add the degenerate hand case to HAND_CASES in test_project.py: hand_case(mu=[0.3, 0.1], w0=[0.5, 0.5], lower=[0.5, 0.5], upper=[0.5, 0.5], turnover_limit=0.0, sector_caps=[1.0]) with expected weights [0.5, 0.5]. The collected count becomes 364; update the 363 on project.html:332 (and the count sentence) in the same change and re-run the collect-only count.")
row("PRJ-R7-02", "2.9-prose", f"{G}/test_project.py:248 (comment on the 'upper bound binding' hand case)",
    "FAIL", "The comment says 'the unconstrained answer (0.35, 0.65) is cut to (0.7, 0.3)'. With the turnover limit 0.5 kept and the upper bound removed, the reference answer is (0.55, 0.45) (hand_cases_r7.log); (0.35, 0.65) is the answer with both the upper bound and the turnover limit removed (turnover 0.9 > 0.5 at (0.35, 0.65)). The comment misattributes which constraint produces the cut.",
    fix="Reword the comment: 'The second upper bound (0.3) binds: with it removed, the turnover limit stops the answer at (0.55, 0.45); the bound moves asset 2 to 0.3, and the answer is (0.7, 0.3).'")
row("PRJ-R7-03", "2.9-prose", f"{G}/test_project.py:862-863 (comment before POSITIONS)",
    "FAIL", "The comment says 'the starting-sum and box tests also give the asset room in its box and its sector cap'. Only the starting-sum tests and the lower-bound box tests call _make_room; the upper-bound box tests (test_start_outside_a_bound..., test_start_on_or_inside_a_bound...) do not. The sentence that the named condition is the only one broken remains true.",
    fix="Reword to: 'the starting-sum tests and the lower-bound box tests also give the asset room in its box and its sector cap (the upper-bound tests change only the bound, so they break only that condition).'")
row("PRJ-R7-04", "2.6-mutation", "ledgers/M7/mutants/r7_01..r7_05",
    "PASS", "Five new student-error mutants written from reference.py: r7_01 sector cap measured from start sector weight (killed by test_named_condition_boundary_is_accepted[start-within-sector-cap-boundary], seed 0); r7_02 start box checked to 1e-8 (killed by [start-within-upper-invalid], seed 0); r7_03 gamma refused below 1e-6 (killed by [gamma-just-inside-zero], seed 0); r7_04 active set drops the first working row (killed by test_output_has_the_three_fields..., seed 1); r7_05 sector caps reversed (killed by test_stationarity_holds_in_the_weights, seed 0). Evidence: r7_mutants_kill.log.")
row("PRJ-R7-05", "2.6-autograder", f"{G}/test_project.py (per-test time in Pyodide)",
    "UNVERIFIABLE", "The suite runs in 0.42 s locally and the Pyodide page smoke finishes the whole suite in 7.3 s (page_smoke_project.log), so no test is near 5 s in that run; but per-test Pyodide durations were not recorded, so the 5-second limit of BUILDER_RULES 5.3.4 is not shown per test.",
    fix="Have page_smoke.py record per-test durations in Pyodide and fail above 5 s; re-run and attach the log.")
row("PRJ-R7-06", "2.8-data", f"course/modules/M/M7/{P}; {G}/instance.py",
    "PASS", "No dataset or figure on this page; no download; the case is generated (instance.py) and labelled SIMULATED in the lede, spec, instance label and every lab docstring.")
row("PRJ-R7-07", "2.6-hours", f"course/modules/M/M7/{P}:344-350",
    "PASS", "Own estimate of components: Rungs 1-2 about 4-6 h; core active-set solver 10-14 h; linear constraints and linearization 4-6 h; certificate 4-6 h; self-check and own tests 4-6 h. Total 26-38 h, which lies within 30% of 33 h (23.1-42.9).")

# Mutants
mut_lines = [l for l in (ROOT / S / "mutate_M7_0-9_final_r7.log").read_text().splitlines() if l.startswith(("KILLED", "SURVIVED"))]
mutants = []
for l in mut_lines:
    m = re.match(r"(KILLED|SURVIVED) (\S+?): (.*) -> (.*)$", l)
    if not m:
        raise SystemExit("unparsed: " + l)
    status, name, desc, killer = m.groups()
    mutants.append({"id": name, "description": desc, "killed_by": None if killer == "None" else killer})
mutants.append({"id": "r7_06_unfloored_dual_residual_on_degenerate_positive_multipliers.py",
                "description": "Student error r7_06: on a degenerate two-asset case the answer reports the dual residual without the floor, with all-positive multipliers.",
                "killed_by": None})
survivors = [m["id"] for m in mutants if not m["killed_by"]]
frag = {
    "unit": "M7",
    "slice": "M7-d",
    "round": 7,
    "verifier": "Claude Haiku 5.5, independent verifier for M7-d, round 7 (did not build M7-d; own checkout)",
    "pin": "9373ef398589097500ea849e30ff9da423b98943",
    "base": "142ecfc2bd27061de18bd67e83df81e69f5c249d (round-6 pin). Slice delta since that pin: course/modules/M/M7/project.html (lines 164, 317-324), grader/test_project.py (lines 37-44, 128-151, 300-311), ledgers/M7/mutants (f6_01..f6_10, v6_03..v6_06 added). grader/reference.py, instance.py, starter.py, tests/labs/M7/* and the M7 plan are byte-identical to the round-6 pin. Round-6 PASS rows were not carried: all rows were re-derived this round, keeping the round-6 ids.",
    "checkout": str(ROOT),
    "scratch": "/tmp/m7d-r7",
    "verified_at": datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat(),
    "verdict": "FAIL",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": ("Non-PASS rows: PRJ-D1-08 (proof step that every feasible weight vector extends to a feasible (w,t) is not written), PRJ-D1-39 (no publication exclusion of grader/reference.py anywhere in the repo), PRJ-R7-01 (surviving mutant r7_06: the dual-floor path is never exercised by any suite instance; fixed by adding one degenerate hand case), PRJ-R7-02 and PRJ-R7-03 (two test comments misdescribe the constraints or the room given), PRJ-R7-05 (per-test Pyodide durations not recorded). "
              "Mutation: 176/176 killed on seeds 0-9 (mutate_M7_0-9_final_r7.log); r7_06 run separately on seeds 0 and 9 and passes (survives). Alternatives: exact A and B pass 50/50; float variants C, D, E, G, H fail the gamma 1e-6 and 1e-9 boundary rows, treated as defective variants (PRJ-D1-38), not a grader finding. Collect count 363 on all seeds 0-49. Labs: twins under python -I -W error all exit 0 and match their expected blocks. "
              "Process note: ledgers/M7/scripts/M7-d-r7/ already held tracked files from another checkout before this round (cards_numbers_r7.py, checks.log, collect.log, mutate_existing.log, alt/alt_float.py, and similar); I did not run or rely on them and wrote only the files named in this fragment. Not verified: a live browser run of the alternatives; the deployment artifact (no deployment configuration in the repo); per-test Pyodide durations; whether a carefully scaled float method passes gamma = 1e-9; the Stokey reading-list entry against its registry record beyond the offline integrity check; the hours estimate is my own estimate."),
    "summary": None,
}
n_total = len(rows)
counts = {s: sum(1 for r in rows if r["status"] == s) for s in ("PASS", "FAIL", "UNVERIFIABLE")}
frag["summary"] = (f"M7-d round 7 on 9373ef3: verdict FAIL. {n_total} rows: PASS {counts['PASS']}, FAIL {counts['FAIL']}, "
                   f"UNVERIFIABLE {counts['UNVERIFIABLE']}. Mutants {len(mutants)} listed, {len(mutants)-len(survivors)} killed (survivors: {survivors or 'none'}; r7_06 survives the suite and is counted under PRJ-R7-01).")
out = ROOT / "ledgers/M7/M7-d.json"
out.write_text(json.dumps(frag, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out, counts, "mutants", len(mutants), "survivors", survivors)
