"""Round 6 (M7-d): assemble ledgers/M7/M7-d.json from the verifier's rows and the mutation log (no row is copied from
the round-5 fragment as a PASS; every row below cites a command, a file:line or a script output of this round)."""

import datetime
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(sys.argv[1])
S = "ledgers/M7/scripts/M7-d-r6/"
PIN = "142ecfc2bd27061de18bd67e83df81e69f5c249d"

mutant_rows = []
for line in (ROOT / S / "v6_mutate_M7_0-9.log").read_text(encoding="utf-8").splitlines():
    m = re.match(r"^(KILLED|SURVIVED) (\S+?): (.*) -> (.*)$", line)
    if not m:
        continue
    status, name, desc, killer = m.groups()
    if status != "KILLED":
        raise SystemExit(f"surviving mutant {name}")
    mutant_rows.append({
        "name": name,
        "description": desc.strip(),
        "killed_by": killer.strip(),
    })
mutants = [{"name": "ledgers/M7/mutants/" + r["name"], "description": r["description"], "killed_by": r["killed_by"]}
           for r in mutant_rows]
assert len(mutants) == 161, len(mutants)

R = []


def row(rid, check, location, status, evidence, fix=None):
    item = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        item["fix"] = fix
    R.append(item)


row("PRJ-D1-01", "2.6-spec", "project.html:292-295; grader/instance.py:21,39-44,57-66", "PASS",
    "Field list at project.html:295 (gamma, mu, sigma, w0, lower, upper, sector, sector_caps, turnover_limit, label) equals the "
    "keys make_instance writes (instance.py:57-66). Asset counts over seeds 0-49 {3: 18, 4: 14, 5: 18} and 50 distinct answers "
    f"(log {S}v6_instances_answers.log); SECTOR_COUNT = 2 (instance.py:20).")
row("PRJ-D1-02", "2.6-spec", "project.html:299-300; grader/test_project.py:126-149; grader/reference.py:330-334", "PASS",
    "Three output keys, seven multiplier names, list sizes and four certificate keys stated at project.html:299-300 are checked by "
    "output_shape (test_project.py:126-149, read in full this round) and returned by reference.allocate; "
    f"{S}run_graders_M7_0-49.log: PASS 50/50.")
row("PRJ-D1-03", "2.4-math", "project.html:309", "PASS",
    "Re-derived: if sum|d_i| <= tau then t_i = |d_i| satisfies t_i >= d_i, t_i >= -d_i and sum t_i <= tau; conversely "
    "sum|d_i| <= sum t_i <= tau. The equivalence and the linearization are correct.")
row("PRJ-D1-04", "2.4-math", "project.html:310-313; grader/test_project.py:85-103; grader/reference.py:305-309", "PASS",
    "Re-derived from L(w,t) of project.html:310: lower -lambda^l, upper +lambda^u, sector +eta_k, turnover +alpha_i - beta_i "
    "(from d_i - t_i and -d_i - t_i), budget +nu; t-stationarity kappa - alpha - beta. Matches test_project.py:92-102 and "
    "reference.py:305-308.")
row("PRJ-D1-05", "2.4-math", "project.html:314-319; grader/test_project.py:106-117; grader/reference.py:262-315", "PASS",
    "The four certificate definitions (primal: max of 0, |sum w - 1|, box and sector gaps, sum|d| - tau; stationarity: max of "
    "|r^w|, |r^t|; dual: max(0, -min m) over the six groups; CS: max |lambda g| at t = |d|) match test_project.py:106-117 and "
    "reference.py:272-315 line by line (read this round). d_i - t_i <= 0 adds nothing to the primal max.")
row("PRJ-D1-06", "2.4-math", "project.html:320 (first two sentences)", "PASS",
    "'The floor at zero ... changes its value only when every inequality multiplier is positive': if min m <= 0 then "
    "max(0, -min m) = -min m; if min m > 0 the unfloored value -min m is negative and the floor gives 0. True. 'The agreement "
    "check applies the floor to your own multipliers' matches test_project.py:109. The consequence sentence is row PRJ-D1-23.")
row("PRJ-D1-07", "2.4-math", "project.html:317-321; grader/test_project.py:37,179-203,364,371-373", "PASS",
    "Tolerances on the page (1e-8 certificate and feasibility, 1e-9 agreement and starting portfolio) match TOL = 1e-8 "
    "(test_project.py:37), the 1e-9 agreement (:364), the feasibility asserts at TOL (:179-203) and the certificate bound (:371-373).")
row("PRJ-D1-08", "2.4-math", "project.html:322-325 (Proposition, proof, hypotheses)", "PASS",
    "Proposition (323) and proof (324) re-derived this round: L convex in (w,t) (f convex, g_j affine, lambda_j >= 0); stationarity "
    "gives a minimizer of L; for feasible (y,s): f(y) >= L(y,s) >= L(w,t) = f(w) by g_j <= 0, lambda_j >= 0, budget term 0 and CS; "
    "uniqueness by the feasible midpoint and strict convexity. Hypotheses listed at :325; 'existence of multipliers ... is not proved' "
    "stated at :325. Strict convexity: gamma > 0 and Sigma PD (:322); instance.py:39-41 gives Sigma = (A'A + I)/1000 with integer A, "
    "so x'Sigma x = (|Ax|^2 + |x|^2)/1000 > 0 for x != 0 (:325).")
row("PRJ-D1-09", "2.4-math", "project.html:325; grader/instance.py:38-43", "PASS",
    "instance.py:40-43 builds sigma[i][j] = (sum_k factor[k][i] factor[k][j] + [i==j]) / 1000 with integer factor entries "
    "(rng.randint(-2, 2)), i.e. (A'A + I)/1000 as stated at project.html:325.")
row("PRJ-D1-10", "2.6-spec", "project.html:326; grader/reference.py:54-109; grader/test_project.py:567-707", "PASS",
    "Each named ValueError condition at project.html:326 is raised by reference._parse: not a mapping (:55-56), missing field "
    "(:57-59), NaN/inf (_scalar :42-43), no assets (:62-63), gamma <= 0 (:65-66), tau < 0 (:68-69), list lengths (:71-84), "
    "symmetry (:76-77, exact), positive definiteness by LDL pivots (:78-79, :112-124), lower > upper (:85-86), sector label "
    "range (:97-98), a cap with no asset (:100-101), starting sum, box and caps with 1e-9 (:102-108). The valid boundary forms "
    "are in test_project.py:567-707 (read this round).")
row("PRJ-D1-11", "2.6-spec", "project.html:327,330; grader/test_project.py:272-286,1036-1055; grader/reference.py:13-18", "PASS",
    "reference.py imports only math, collections, dataclasses, fractions, itertools, typing (:13-18); the AST import test "
    "(test_project.py:272-286) rejects non-stdlib and grader imports; purity, silence and determinism at :1036-1055.")
row("PRJ-D1-12", "2.6-spec", "project.html:332; grader/test_project.py", "PASS",
    f"{S}v6_collect_seeds_0-49.log: pytest --collect-only gives 363 tests for each of seeds 0-49. Every decorator argument list in "
    "test_project.py is a constant (POSITIONS, NAMED_CONDITIONS, HAND_CASES, WRONG_TYPES ...), so the count does not vary by seed.")
row("PRJ-D1-13", "2.5-lab", "project.html:53-168; tests/labs/M7/lab-M7-project-1.py", "PASS",
    f"{S}v6_labs_check.py: page code == twin; twin under python -I -W error exits 0 with empty stderr; output == expected block. "
    f"{S}v6_numbers_lab.py (independent Fraction recomputation): budget-only 54/65, 5/26, -3/130; held asset 2; weights 9/11, 2/11, 0; "
    "nu = -21/1100; lower multiplier 9/1100; objective -3/220 = -0.0136363... (page prints -0.013636). All match project.html:156-166.")
row("PRJ-D1-14", "2.5-lab", "project.html:170-285; tests/labs/M7/lab-M7-project-2.py", "PASS",
    f"{S}v6_labs_check.py and a unified diff: the page code differs from the twin only on the three blanked lines (page :250, :261, "
    ":262 vs twin's filled lines 78, 89, 90); the twin's output equals the expected block; the hypothesis text (:172) describes "
    "the filled expressions correctly (residual = gamma Sigma w - mu + nu, minus the bound multipliers; signs = [x >= 0 ...]; all).")
row("PRJ-D1-15", "2.5-lab", "project.html:372-445; tests/labs/M7/lab-M7-project-3.py", "PASS",
    f"{S}v6_numbers_lab.py: check A all 0; check B primal 0, stationarity 9/550, dual 9/1100, CS 0; check C primal 0, stationarity "
    "1/6250, dual 0, CS 0. Matches the expected block (:441-443). Interpretation: 9/550 = 2 x 9/1100 (:444) is correct; the "
    "statement that primal and CS do not respond to these candidates is true of these three numbers.")
row("PRJ-D1-16", "2.9-structure", "project.html:33,338-354; course/modules/M/M7/index.html:29; curriculum/01-foundations.yaml:298-301", "PASS",
    "Components 2+3+10+6+7+5 = 33 (:344-349), total 33 (:350), data-hours-project 33 (:33). Hub: data-hours-lessons 77, "
    "project 33 (index.html:29). Lesson data-hours L01..L08 = 9,9,10,10,10,10,9,10, summing to 77. 77 + 33 = 110 = curriculum hours.")
row("PRJ-D1-17", "2.9-structure", "project.html:40-49", "PASS",
    "Four rung-title spans in order (Rung 1 to 4) at :44-47; check_projects_M7.log PASS. Rung 1 text (:44, edited this round to "
    "'each weight at least zero') matches Lab 1's lower bound of zero.")
row("PRJ-D1-18", "2.9-structure", "project.html:288-336", "PASS",
    "Specification has the dl terms Context, Inputs, Required outputs, Constraints, Grading and Reading list (:290-335) in the "
    "order of BUILDER_RULES 5. The tolerance pointer at :292 ('the tolerance given under Conventions below') points at :321.")
row("PRJ-D1-19", "2.9-structure", "project.html; grader/*.py", "PASS",
    "grep (case-insensitive) for verifier, builder, round, ledger, batch, fixer, pin, TODO, TBD, placeholder over project.html: 0 hits. "
    "The grader and starter comments were read in full and contain no process wording addressed to the learner.")
row("PRJ-D1-20", "2.9-structure", "project.html; tools/page_smoke.py", "PASS",
    f"{S}v6_page_smoke_project.log (run with --pages project, the stem filter): 'page_smoke modules/M/M7/project.html: PASS', "
    "'in-browser grader: All 363 tests pass', lab timings 0.0 s, 'page_smoke M7: PASS'. An earlier invocation with a path matched no "
    "page and printed PASS vacuously; it is not used as evidence.")
row("PRJ-D1-21", "2.4-notation", "project.html:292-336,456; notation/notation.json", "PASS",
    "Registered symbols (T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q}) do not occur in the page's math (scan this "
    "round). Macros used on the page (\\Sigma, \\alpha, \\beta, \\eta, \\gamma, \\kappa, \\lambda, \\mu, \\nu, \\tau, \\top, \\tfrac, "
    "\\square, relations) are not in the registered macro list, so nothing is reused. Local symbols are defined in Conventions (:305-310) "
    "before use.")
row("PRJ-D1-22", "2.9-structure", "project.html:456; course/concepts.html:121; check_dag", "PASS",
    f"concepts.html:121 has id envelope-theorem (defined in M2/L22; M2 is in M7's prerequisite closure). L03.html:62 defines the "
    f"Lagrangian used at project.html:310. {S}v6_check_dag_M7.log: check_dag M7 PASS.")
row("PRJ-D1-23", "2.9-prose", "project.html:320 (last sentences of the paragraph)", "FAIL",
    "The sentence 'An answer whose inequality multipliers are all positive is the case in which it changes the value, and the agreement "
    "check then compares your reported residual with the floored value, so an unfloored report fails it' is false for smallest "
    f"multipliers in (0, 1e-9]. Experiment {S}v6_floor_sentence.py and {S}v6_floor_sentence.log: the reference's exact multipliers, "
    "each inequality multiplier raised by delta = 5e-10 (so min m = 5e-10 > 0), dual reported unfloored (-min m): the full suite gives "
    "363 passed on seeds 0-4. With delta = 2e-9 the agreement check fails on seeds 0-2 and the full suite on seed 0 gives 6 failed. The unfloored report "
    "is caught only when the smallest multiplier exceeds 1e-9 (test_project.py:364 tolerance).",
    fix="Replace 'so an unfloored report fails it.' with: 'so an unfloored report fails it only when the smallest inequality "
        "multiplier exceeds 10^-9.' Keep the rest of the paragraph.")
row("PRJ-D1-24", "2.6-spec", "project.html:359,364-366; grader/test_project.py:5", "PASS",
    "Flags of project.html:365 match test_project.py:5 and the runs. The decode command at :366, run in a scratch copy, prints the "
    "seed-7 case (gamma 8, four assets, sector [1, 0, 0, 1]). .venv/bin/python --version: 3.14.8; pyproject.toml:5 requires >= 3.14.")
row("PRJ-D1-25", "2.6-autograder", "grader/reference.py; grader/starter.py; grader/test_project.py", "PASS",
    f"{S}run_graders_M7_0-49.log: PASS (reference 50/50 seeds, slowest 3.1 s). {S}v6_starter_seed0.log: the starter gives "
    "'360 failed, 3 passed' (it raises NotImplementedError), so the suite fails on the starter.")
row("PRJ-D1-26", "2.6-autograder", "grader/instance.py:20-68", "PASS",
    f"{S}v6_instances_answers.log: 50 seeds; the reference solves every case (feasible); 50 distinct weight vectors; turnover binds on "
    "47 seeds; at least one non-zero multiplier on all 50; asset counts 3/4/5 occur. Instances are exact decimals with at most three "
    "digits (instance.py:9 and the constructions at :44-55).")
row("PRJ-D1-27", "2.6-autograder", "grader/reference.py:13-18; grader/test_project.py:272-286", "PASS",
    "Stdlib-only imports (PRJ-D1-11); ruff check and ruff format --check pass on the grader and labs; mypy --strict on reference, "
    f"instance, starter and the three project twins: 'Success: no issues found in 6 source files' ({S}v6_mypy_M7_grader_labs.log).")
row("PRJ-D1-28", "2.6-autograder", "grader/test_project.py (every assertion message)", "PASS",
    "Every assertion message in test_project.py was read this round. Each names the property (budget, box, sector cap, turnover, dual "
    "feasibility, stationarity in weights or auxiliaries, complementary slackness, certificate agreement, optimality). None prints "
    "an expected value; the hand-case message (:404) names the case only. The browser and local runs use --assert=plain.")
row("PRJ-D1-29", "2.6-autograder", "grader/*.py; tests/labs/M7/lab-M7-project-1..3.py", "PASS",
    f"{S}v6_mypy_M7_grader_labs.log (strict, 6 files). test_project.py is not in the repo's mypy files and imports the learner's "
    "module, so it is not type-checked by the gate; ruff passes on it. Pyodide run: 'All 363 tests pass' (page_smoke); local run: "
    "363 pass on seeds 0-49.")
row("PRJ-D1-30", "2.5-lab", "tests/labs/M7/lab-M7-project-1..3.py; tests/test_labs.py", "PASS",
    f"{S}v6_pytest_relevant.log: pytest tests/test_run_labs.py tests/test_page_checks.py tests/test_labs.py -> 352 passed; "
    f"{S}run_labs_M7.log: run_labs M7 PASS (11/11).")
row("PRJ-D1-31", "2.6-autograder", "project.html:359,365; grader/test_project.py:5", "PASS",
    "The same flags run locally (run_graders_M7_0-49.log) and in the browser (page_smoke), with the same suite and support files "
    "(data-suite, data-support, data-solution on the panel at :359).")
row("PRJ-D1-32", "2.6-atlas", "project.html; plans/M7-build-plan.md:3; curriculum/01-foundations.yaml:298-327", "PASS",
    "No atlas key on the panel (project.html:359). plans/M7-build-plan.md:3 says 'no Atlas milestone'; the M7 curriculum block "
    "(:298-327) has no atlas key. The solution file is unit-local.")
row("PRJ-D1-33", "2.1-citations", "project.html:465-466; references/references.json", "PASS",
    f"Live: {S}v6_verify_refs_M7_live.log: 'live re-verification of M7: 2 of 560 entries, 0 problems'. Offline whole registry: "
    f"{S}verify_refs_offline.log: 560 entries, 0 problems. The page cites the two keys only as reading (no claim is attributed to them).")
row("PRJ-D1-34", "2.9-structure", "project.html:344-350", "PASS",
    "2+3+10+6+7+5 = 33 and the total row says 33; the hub split (77 + 33) matches the lesson hours. Per-component hours are design "
    "targets under the ruling; the arithmetic is consistent.")
row("PRJ-D1-35", "2.6-mutation", "ledgers/M7/mutants/ (161 files)", "PASS",
    f"{S}v6_mutate_M7_0-9.log: 'mutate_graders M7: PASS (161/161 killed)', exit 0, on the current directory (157 existing + 4 new "
    "student-error mutants v6_03..v6_06). The two candidate equivalent mutants (v6_01, v6_02) are excluded, with a proof in PRJ-R6-01.")
row("PRJ-D1-36", "2.6-mutation", "ledgers/M7/mutants/x3_01..x3_03, r4_01..r4_06", "PASS",
    f"{S}v6_mutate_M7_0-9.log: every x3_* and r4_* file is KILLED (names and killers in the mutants list of this fragment).")
row("PRJ-D1-37", "2.6-mutation", "project.html:317,320; grader/reference.py:239-241,287; ledgers/M7/mutants (x3_04 absent)", "PASS",
    "ledgers/M7/mutants has no x3_04 file (ls | grep x3_04 is empty). The unfloored-dual candidate is re-derived as v6_01 and proved "
    "equivalent in PRJ-R6-01 (min multiplier is 0 on every valid input).")
row("PRJ-D1-38", "2.6-autograder", "ledgers/M7/scripts/M7-d-r6/v6_alts/*.py; ledgers/M7/scripts/M7-d-r5/alts/*.py", "PASS",
    f"Exact alternatives, written this round: alt1 (tight start, most-negative drop) and alt2 (empty start, latest-added drop) each pass "
    f"50/50 seeds 0-49 ({S}v6_alts_run_0-49.log). A float solver with relative cutoffs from the prior round, "
    "ledgers/M7/scripts/M7-d-r5/alts/alt_r4_reused_r3v_relative_float.py, passes 50/50 (run this round: "
    f"{S}v6_r5alt_alt_r4_reused_r3v_relative_float.log). This shows the suite accepts exact and relative-cutoff float methods, "
    "including the gamma = 1e-6 and 1e-9 boundaries. Three float variants written this round with absolute cutoffs (alt3-alt5, "
    "1e-10 to 1e-13) and two prior float variants with absolute cutoffs fail only the gamma-positive-zero/negative boundary and the "
    "gamma-just-inside-zero tests (singular KKT, cycling, or budget gap at gamma = 1e-6 and 1e-9). Those are defects of those "
    "variants, not over-constraint, and they are not counted as correct alternatives. Not run: projected-gradient, ADMM, barrier "
    "and dual-ascent alternatives named in plans/M7-build-plan.md section 7.4, item 2; the alternatives run here are "
    "active-set variants only.")
row("PRJ-D1-39", "2.9-structure", "course/modules/M/M7/grader/reference.py; BLUEPRINT.md:400-401; .github/workflows/ci.yml", "FAIL",
    "BLUEPRINT.md:400-401 requires deployment to exclude every grader/reference.py. The repo has no deploy configuration (find for "
    "vercel.json, .vercelignore, netlify.toml, wrangler.toml, Dockerfile, railway.json/toml returns nothing); ci.yml has checks and "
    "an artifact upload only; no tool excludes reference.py (grep over tools/). The file sits under course/, which BLUEPRINT names as "
    "the published tree. The deploy configuration, if it exists outside the repo, was not readable, so the rule is UNVERIFIABLE "
    "and counts as FAIL.",
    fix="Add the publication exclusion for course/modules/*/*/grader/reference.py to the deployment configuration (or a build step "
        "that copies course/ without it) and show the published artifact listing without reference.py.")
row("PRJ-R4-01", "2.9-prose", "grader/test_project.py:378-383 (docstring)", "PASS",
    "The docstring states the condition only (no seed census). Read this round; the claim 'every mix equals the answer' holds when "
    "the answer equals the starting portfolio.")
row("PRJ-R5-01", "2.4-math", "project.html:456 (frontier bullet)", "PASS",
    "b is the right-hand side of sum_i w_i = b; the page sets b = 1 (:306-308). The bullet asks the learner to state a sign convention "
    "and claims no sign.")
row("PRJ-R5-02", "2.6-spec", "grader/test_project.py:223 (comment); :348-349 (message)", "PASS",
    "Re-derived: stationarity w - mu + nu = 0 with sum(mu) = 0.4 and budget 0.4 - 2 nu = 1 gives nu = -0.3 and w = mu + 0.3 = (0.6, 0.4). "
    "The message at :348-349 is r^t = kappa - alpha - beta (test_project.py:102).")
row("PRJ-R5-03", "2.9-prose", "project.html:450", "PASS",
    "The only file read in the grader is the learner's own source (test_project.py:275). instance.py opens no file (read in full). "
    "'No case reads a data file' holds.")
row("PRJ-R5-04", "2.9-structure", "project.html:349-350", "PASS",
    "Rationale prose only; the hours figures are unchanged and sum as in PRJ-D1-16.")
row("PRJ-R5-05", "2.6-mutation", "ledgers/M7/mutants/r5_01..r5_05", "PASS",
    f"All five r5_* mutants are KILLED in {S}v6_mutate_M7_0-9.log.")
row("PRJ-R6-01", "2.6-mutation", "ledgers/M7/scripts/M7-d-r6/v6_equivalent/v6_01_*.py, v6_02_*.py; grader/reference.py:203-205,229-230,239-249,287", "PASS",
    "Equivalence of two candidates to the reference on every valid input (exact arithmetic). (a) v6_01 (dual reported without the "
    "floor) equals max(0,-min m) = -min m only when min m = 0. The reference's working set never holds both lower_i and upper_i: "
    "those rows are negatives of each other; the initial loop tests rank (reference.py:203-205) and a dependent blocking row "
    "raises (:229-230), so the pair cannot both be in the set; hence one of lambda^l_i, lambda^u_i is exactly 0 (mult.get default 0, :239-241), and dual feasibility "
    "makes min m = 0 exactly. Floored and unfloored values coincide. (b) v6_02 (turnover multipliers left out of the dual): the "
    "turnover multipliers plus_i = (kappa + net_i)/2, minus_i = (kappa - net_i)/2 with kappa = sum eta_s and eta_s >= 0 satisfy "
    "|net_i| <= kappa (reference.py:242-249), so they are >= 0; since min m = 0 over the bound and sector rows, adding them does not "
    f"change the minimum. Empirical: {S}v6_reference_multiplier_facts.log: min m = 0 on 50/50 seeds; no negative turnover multiplier; "
    "no asset with both bound multipliers non-zero. Both files are kept under v6_equivalent/, not in mutants/.")
row("PRJ-R6-02", "2.6-spec", "grader/test_project.py:126-149,167-171,293-297; project.html:300", "FAIL",
    "project.html:300 states: budget is a number; lower, upper, turnover_plus and turnover_minus are lists of n numbers; sector is a "
    "list of Z numbers; turnover_total is a number. The grader does not check these types: output_shape (:126-149) checks only "
    "container types and lengths, multipliers_of (:167-171) converts every value with float(), so text such as '0.5' is accepted, and "
    "the number check (:293-297) covers weights and certificate only. Learner = reference with every multiplier returned as str(value): "
    f"363/363 pass on seeds 0 and 7 ({S}v6_multiplier_types.log). The check fails for booleans (58 tests) only because the values change.",
    fix="In output_shape, assert is_real_number on budget, turnover_total and every element of the five lists and the sector list "
        "BEFORE any float() conversion; add a test that calls is_real_number on each multiplier of the seed output; add a mutant that "
        "returns multipliers as text to ledgers/M7/mutants/ so the regression stays killed.")
row("PRJ-R6-03", "2.6-mutation", "ledgers/M7/mutants/v6_03..v6_06", "PASS",
    "Four new student-error mutants, each a complete module copied from reference.py with one change: v6_03 complementary slackness "
    "of the bound rows at w0; v6_04 weight stationarity with 2 gamma Sigma w (the factor of one half dropped); v6_05 turnover sign forms "
    "that never limit a sale of the last asset; v6_06 a zero turnover limit read as no limit. All four KILLED on seeds 0-9 (killers in "
    f"the mutants list; {S}v6_mutate_M7_0-9.log).")

verdict = "PASS" if all(r["status"] == "PASS" for r in R) else "FAIL"
counts = {s: sum(1 for r in R if r["status"] == s) for s in ("PASS", "FAIL", "UNVERIFIABLE")}
now = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat()
fragment = {
    "unit": "M7",
    "slice": "M7-d",
    "round": 6,
    "verifier": "Claude Haiku 5.5, independent verifier for M7-d, round 6 (did not build M7-d; works in its own checkout)",
    "pin": PIN,
    "base": "440ed3c8216725d498d9c6d7c746907d4d418198 (round-5 pin). Slice delta since that pin: course/modules/M/M7/project.html "
            "lines 44, 320, 322, 324 (ladder text, floor sentence, convexity sentence, proof wording); ledgers/M7/mutants r5_01..r5_05 "
            "present; grader/*.py, tests/labs/M7/* and plans/M7-build-plan.md byte-identical to the round-5 pin. Every changed subject "
            "was re-read and re-verified from scratch; the round-5 fragment's PASS rows were not carried.",
    "checkout": str(ROOT),
    "scratch": "/tmp/m7d-r6-* (run, alt, c, floor, types, starter, tmp scratch dirs)",
    "verified_at": now,
    "verdict": verdict,
    "rows": R,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "Non-PASS rows: PRJ-D1-23 (floor sentence overstated; delta experiment in v6_floor_sentence.log), PRJ-D1-39 (no "
        "reference.py publication exclusion anywhere in the repo; UNVERIFIABLE counted as FAIL), PRJ-R6-02 (multipliers not type-"
        "checked; text multipliers pass 363/363). Mutation: 161/161 killed, including 4 new (v6_03..v6_06); equivalents v6_01 and "
        "v6_02 excluded with proof (PRJ-R6-01). Alternatives: exact alt1/alt2 50/50, prior relative-cutoff float 50/50; my absolute-"
        "cutoff float variants fail the gamma boundary tests and are treated as defective. Process note: the directory "
        f"{S} already held files from another checkout (tracked at 7aa909e9: q-mutants, labcheck and a README naming verifyB6); I did not "
        "run or rely on them. Not verified: a live Pyodide run beyond page_smoke's in-browser grader; the planned projected-gradient, "
        "ADMM, barrier and dual-ascent alternatives; the deployment artifact (no deploy configuration in repo)."
    ),
    "summary": (
        f"M7-d round 6 on {PIN[:7]}: verdict {verdict}. {len(R)} rows: PASS {counts['PASS']}, FAIL {counts['FAIL']}, "
        f"UNVERIFIABLE {counts['UNVERIFIABLE']}. Mutants {len(mutants)} listed, all killed on seeds 0-9."
    ),
}
out = ROOT / "ledgers/M7/M7-d.json"
out.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out, "rows", len(R), counts, "mutants", len(mutants), "verdict", verdict)
