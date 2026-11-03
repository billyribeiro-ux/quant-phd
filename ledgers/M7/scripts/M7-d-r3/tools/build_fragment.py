"""Builds ledgers/M7/M7-d.json (round 3) from the logs of this verifier's round-3 runs. Written by the verifier."""
import json, re, sys
from pathlib import Path

R = Path(sys.argv[1])
S = R / "ledgers/M7/scripts/M7-d-r3"
brute_status = sys.argv[2]  # e.g. "PASS 50/50" or "FAIL k/50"
brute_evidence = sys.argv[3]

mutants = []
for line in (S / "mutate_all_r3_0-9.log").read_text(encoding="utf-8").splitlines():
    m = re.match(r"KILLED (\S+?): (.*) -> (.*)$", line)
    if m:
        name, desc, killed = m.group(1), m.group(2), m.group(3)
        mutants.append({"id": name[:-3], "description": desc, "file": f"ledgers/M7/mutants/{name}",
                        "killed_by": killed})
    elif line.startswith("SURVIVED"):
        raise SystemExit("unexpected survivor in the full mutation run: " + line)
for line in (S / "x3_mutants_kill.log").read_text(encoding="utf-8").splitlines():
    m = re.match(r"KILLED (\S+\.py) seed (\d+): (.*?) \(", line)
    if m:
        mutants.append({"id": m.group(1)[:-3], "description": "round-3 student error (see mutant file docstring)",
                        "file": f"ledgers/M7/mutants/{m.group(1)}",
                        "killed_by": f"seed {m.group(2)}: {m.group(3)}"})
    elif line.startswith("SURVIVED"):
        name = line.split()[1]
        mutants.append({"id": name[:-3], "description": "round-3 student error: the dual residual is reported "
                        "without the floor at zero (see mutant file docstring)",
                        "file": f"ledgers/M7/mutants/{name}", "killed_by": None,
                        "note": "survives seeds 0-9 (x3_mutants_kill.log); the page states the floor (project.html:317, 320)"})
assert len(mutants) == 147, len(mutants)

NOW = __import__("datetime").datetime.now(__import__("datetime").timezone.utc).replace(microsecond=0).isoformat()
L = "ledgers/M7/scripts/M7-d-r3/"
rows = [
 {"id": "PRJ-D1-01", "check": "2.6 spec: Context and Inputs", "location": "course/modules/M/M7/project.html:292-295",
  "status": "PASS", "evidence": "Read in full this round. grader/instance.py:20-21 (SECTOR_COUNT=2, ASSET_COUNTS=(3,4,5)), :56-68 (gamma, mu, sigma, w0, lower, upper, sector, sector_caps, turnover_limit, label), :68 payload is json.dumps; reference.py:20 REQUIRED equals the page's field list; test_project.py:40 decodes the payload."},
 {"id": "PRJ-D1-02", "check": "2.6 spec: Required outputs", "location": "project.html:299-300",
  "status": "PASS", "evidence": "test_project.py:126-149 checks exactly the keys weights, multipliers, certificate; the seven multiplier names (139-141); list lengths (142-146); the four certificate keys (147-149). run_graders_0-49.log: reference passes 50/50."},
 {"id": "PRJ-D1-03", "check": "2.4 maths: linearized turnover", "location": "project.html:309",
  "status": "PASS", "evidence": "Re-derived: t_i >= |d_i| gives sum|d_i| <= sum t_i <= tau; t_i = |d_i| satisfies the three constraints. Matches reference.py:189-191 (sign forms) and test_project.py:63-65 (turnover_gap)."},
 {"id": "PRJ-D1-04", "check": "2.4 maths: stationarity residuals r^w, r^t", "location": "project.html:311-312",
  "status": "PASS", "evidence": "Re-derived with L = f + sum lambda_j g_j + nu(sum w - 1), g_j <= 0 (L03.html:62 convention): d/dw_i gives gamma(Sigma w)_i - mu_i + nu - lambda^l_i + lambda^u_i + eta_k(i) + alpha_i - beta_i; d/dt_i gives kappa - alpha_i - beta_i. Identical to test_project.py:85-103 and reference.py:303-308."},
 {"id": "PRJ-D1-05", "check": "2.4 maths: four certificate definitions", "location": "project.html:314-319",
  "status": "PASS", "evidence": "test_project.py:106-117 and reference.py:262-315 implement each field. The primal set also holds d_i - t_i and -d_i - t_i, which are <= 0 at t = |d| and so never change the maximum with 0. Dual and complementary slackness run over the same six groups."},
 {"id": "PRJ-D1-06", "check": "2.4: dual-residual floor, mathematical claim at project.html:320", "location": "project.html:320; test_project.py:109",
  "status": "PASS", "evidence": "The claim is true: dual = max(0, -min m) changes its value only when every inequality multiplier is positive. Reference smallest inequality multiplier is exactly 0 on 50 of 50 seeds 0-49 (" + L + "seed_facts_r3.log, dual_residual 0 in 50 of 50). The testability of the floor is a separate row (PRJ-D1-37)."},
 {"id": "PRJ-D1-07", "check": "2.4: tolerances 1e-8 (fields) and 1e-9 (agreement, starting portfolio)", "location": "project.html:321",
  "status": "PASS", "evidence": "test_project.py:37 TOL = 1e-8 (feasibility, stationarity, CS, dual); :364 agreement 1e-9; reference.py:21 TOL = 1e-9 for the starting-portfolio checks (:102-108)."},
 {"id": "PRJ-D1-08", "check": "2.4 maths: Proposition (sufficiency of KKT), grade T", "location": "project.html:323-324",
  "status": "PASS", "evidence": "Proof re-derived line by line: L convex in (w,t) (lambda_j >= 0, g_j affine); grad L = 0 gives a minimiser of L; for feasible (y,s): f(y) >= L(y,s) >= L(w,t) = f(w) (budget term 0, CS); strict-convexity midpoint gives uniqueness of w; feasible set convex because constraints are affine. Every hypothesis used is in the statement. Grade T justified."},
 {"id": "PRJ-D1-09", "check": "2.4: hypotheses paragraph (Sigma, 50 of 50)", "location": "project.html:325; grader/instance.py:38-41",
  "status": "PASS", "evidence": "instance.py:41 builds Sigma = (A'A + I)/1000 with integer A (randint(-2,2) at :38); x'Sigma x = (|Ax|^2 + |x|^2)/1000 > 0 for x != 0. Existence of multipliers is disclosed as unproved (honest). The 50 of 50 figure: seed_facts_r3.log and run_graders_0-49.log."},
 {"id": "PRJ-D1-10", "check": "2.6 spec: named ValueError conditions and boundary values", "location": "project.html:326; grader/test_project.py:567-707",
  "status": "PASS", "evidence": "Each named condition is mapped to a reference.py check (mapping :55-56, field :58-59, non-finite :42-43, no assets :62-63, one entry per asset :71-72, :83-84, :91-92, symmetric :76-77, PD :78-79, gamma :65-66, turnover :68-69, lower>upper :85-86, start :102-108, sector label and no asset :97-101) and to a test: NAMED_CONDITIONS :567-581, OTHER_SIDE_REFUSED :684-707, EXACT_BOUNDARIES :604-610. Suite passes on the reference (run_graders_0-49.log)."},
 {"id": "PRJ-D1-11", "check": "2.6 spec: purity, silence, stdlib only", "location": "project.html:327, 330; test_project.py:272-286, 1036-1055",
  "status": "PASS", "evidence": "test_project.py:272-286 (AST walk: stdlib only; no grader import); :1036-1040 (argument unchanged); :1043-1049 (no stdout, no warnings); :1052-1055 (determinism). reference.py:13-18 imports are stdlib only."},
 {"id": "PRJ-D1-12", "check": "2.6 grading paragraph: 363 checks and the listed families", "location": "project.html:332",
  "status": "PASS", "evidence": L + "collect_all_seeds_0-49.log: 363 collected for every seed 0-49. Families: outputs 289-303; KKT 305-357; three comparators 376-388 (0.25/0.5/0.75); five hand cases 222-250 and 397-411; named ValueError conditions 567-710; non-finite 737-745; missing field 748-754; non-mapping 757-761; no assets 764-774; one entry short/long 787-791 and 691-698; purity and silence 1036-1055; warnings as errors pytestmark :34."},
 {"id": "PRJ-D1-13", "check": "2.5 Lab 1: output, prose, numbers", "location": "project.html:53-168",
  "status": "PASS", "evidence": "Twin tests/labs/M7/lab-M7-project-1.py run as python -I -W error exits 0, stderr 0 bytes (" + L + "twin_lab-M7-project-1.out). run_labs --unit M7: PASS 11/11 (run_labs_M7.log), page code equals twin, expected equals output. Independent recomputation (" + L + "lab_indep_r3.log): budget-only 54/65, 5/26, -3/130; nu = -21/1100; lower multiplier 9/1100 on asset 3; residuals 0; objective -3/220 = -0.013636; grid minimum on the simplex at (0.82, 0.18, 0) matches 9/11, 2/11. Prose numbers in the interpretation verified."},
 {"id": "PRJ-D1-14", "check": "2.5 Lab 2: completion problem", "location": "project.html:170-285",
  "status": "PASS", "evidence": "run_labs --unit M7 PASS 11/11 applies the completion rule (page lines equal twin line or contain ___, twin output matches). diff of twin_lab-M7-project-2.out and twin_lab-M7-project-1.out: identical. Hypothesis and interpretation prose match the code of steps 4 and 6."},
 {"id": "PRJ-D1-15", "check": "2.5 Lab 3: certificate numbers and prose", "location": "project.html:372-445",
  "status": "PASS", "evidence": "Twin output (twin_lab-M7-project-3.out) equals the page expected block: check A zeros; check B stationarity 9/550, dual 9/1100; check C stationarity 1/6250. " + L + "lab_indep_r3.log reproduces A, B, C. 9/550 = 2 x 9/1100 (prose at :444). Prose 'primal and complementary-slackness residuals do not respond' matches the candidates (B complementary 0, C primal 0)."},
 {"id": "PRJ-D1-16", "check": "2.9 / 2.6: hours arithmetic", "location": "project.html:33, 338-354; course/modules/M/M7/index.html:29",
  "status": "PASS", "evidence": "Components 2+3+10+6+7+5 = 33 (project.html:344-349); total 33 at :350. index.html:29 data-hours-lessons=77 and data-hours-project=33: 77 + 33 = 110 (curriculum M7 hours 110). check_pages --unit M7 PASS (check_pages_unit.log) includes the hours split."},
 {"id": "PRJ-D1-17", "check": "2.6 / BUILDER 5.1: four-rung ladder", "location": "project.html:40-49",
  "status": "PASS", "evidence": "Four span.rung-title entries in order (Rung 1-4) at :44-47; check_projects --unit M7 PASS (check_projects.log)."},
 {"id": "PRJ-D1-18", "check": "2.6 spec completeness (questions a student would ask)", "location": "project.html:288-336",
  "status": "PASS", "evidence": "Read in full: inputs (:294-295), outputs (:299-300), conventions (:305-313), certificate (:315-319), tolerances (:321), proposition (:323-325), refusal list (:326), purity (:327), constraints (:330), grading (:332), reading (:334). Every item a student needs to write allocate() is stated; the seed-level local run is at :362-367."},
 {"id": "PRJ-D1-19", "check": "BUILDER 1.3-1.4: banned strings and phrases", "location": "project.html (whole)",
  "status": "PASS", "evidence": "check_pages --unit M7 PASS (check_pages_unit.log); check_common runs the banned-string scan on project.html. Process-word scan (see PRJ-D1-23 for the two real hits)."},
 {"id": "PRJ-D1-20", "check": "2.5 / 2.9: page_smoke (console, requests, labs, in-browser grader)", "location": "project.html",
  "status": "PASS", "evidence": "page_smoke.py --unit M7 --pages project.html: PASS (" + L + "page_smoke_project.log). The run includes the in-browser grader: it pastes grader/reference.py into the panel and requires every test to pass (tools/page_smoke.py:291-306)."},
 {"id": "PRJ-D1-21", "check": "2.4: notation vs notation/notation.json", "location": "project.html:292-336",
  "status": "PASS", "evidence": "Macros used on the page: \\sum \\le \\ge \\ne \\in \\Sigma \\tau \\gamma \\lambda \\nu \\mu \\alpha \\beta \\eta \\kappa \\top \\tfrac \\square. None is a registered macro (notation/notation.json macros: \\E \\Prob \\Var \\Cov \\Corr \\R \\N \\indic \\Normal ...) and none is a registered symbol (T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, Q). Local letters (w, t, d, f, L, g, r, n, Z, S_k, c_k, l, u) are defined on first use (:294-305). No reuse of a registered symbol."},
 {"id": "PRJ-D1-22", "check": "2.9 / BUILDER 1.10: DAG and concept use", "location": "project.html:292, 309-310, 456",
  "status": "PASS", "evidence": "check_dag.py --unit M7 PASS (check_dag.log). Concept link envelope-theorem (:456) resolves to course/concepts.html id=envelope-theorem (anchor present). Lagrangian is taught in L03 (in closure); positive definiteness is M3."},
 {"id": "PRJ-D1-23", "check": "2.9 / rule 12: process words and build narration in learner text", "location": "project.html:320, 325",
  "status": "FAIL", "evidence": "Learner text narrates the build's verification: :320 'On seeds 0 to 49 the reference solution's smallest inequality multiplier is zero in 50 of 50 cases'; :325 'On seeds 0 to 49 the reference solution's multipliers pass every check in 50 of 50 cases; this covers those seeds only'. The reference solution is grader/reference.py, which BLUEPRINT.md:401 says is not public, so a learner cannot read it. Same finding as round 2 (PRJ-D1-23 there); the wording changed but the narration did not. No other hit: scan for round, fixer, builder, verifier, ledger, architect, TODO, draft, planner, audit, mutant, shim in project.html and grader/ and labs returns none (rounding is 'rounded').",
  "fix": "Delete the two census sentences from project.html:320 and :325 (keep the mathematical statement that the floor changes the value only when every inequality multiplier is positive). The 50-of-50 census belongs in the ledger, not on the page."},
 {"id": "PRJ-D1-24", "check": "2.6 local-run instructions and decode command", "location": "project.html:364-366",
  "status": "PASS", "evidence": "The QF_SEED pytest command with the page's flags was run on seeds 0 and 49 (collect_seed0.log, collect_seed49.log, run_graders_0-49.log). Decode command run in a scratch copy of instance.py: prints 'SIMULATED constrained allocation, seed 7: 4 assets, not a real portfolio' (the page command prints the full mapping; it is the same json.loads path)."},
 {"id": "PRJ-D1-25", "check": "2.6 autograder 1: run_graders on reference; starter fails", "location": "grader/reference.py; grader/starter.py",
  "status": "PASS", "evidence": "run_graders --unit M7 --seeds 0-49: PASS (reference 50/50 seeds, slowest 2.8 s) (" + L + "run_graders_0-49.log). Starter on seed 0: 360 failed, 3 passed; the 3 passing tests are the structure tests that never call allocate (" + L + "starter_seed0.log)."},
 {"id": "PRJ-D1-26", "check": "2.6 autograder 2: instances valid and materially different", "location": "grader/instance.py:34-68",
  "status": "PASS", "evidence": "Seeds 0-49: n in {3,4,5} (18, 14, 18 seeds) (seed_sizes_0-49.log). Reference active sets (" + L + "variety_0-49.log): 12 distinct active-set patterns across the 50 seeds; sector caps bind on 19 seeds, turnover on 47, upper bounds on 6, lower bounds on 4. Seeds change which constraints bind, as BUILDER_RULES 5.3 requires."},
 {"id": "PRJ-D1-27", "check": "2.6 autograder: standard library only", "location": "reference.py:13-18; test_project.py:272-286",
  "status": "PASS", "evidence": "reference.py imports math, collections.abc, dataclasses, fractions, itertools, typing (stdlib). test_project.py:272-286 walks the AST of the learner file and rejects non-stdlib imports."},
 {"id": "PRJ-D1-28", "check": "2.6 autograder 4: failure messages name the property and never print the expected value", "location": "grader/test_project.py (all assert messages)",
  "status": "PASS", "evidence": "Every assert message read (test_project.py:129-1055). Messages name a property (budget, box, sector cap, turnover, dual feasibility, stationarity, complementary slackness, certificate field, named condition). No message formats an expected value; run with --assert=plain, so pytest shows the assert source line only."},
 {"id": "PRJ-D1-29", "check": "2.6 autograder: mypy --strict and ruff", "location": "grader/reference.py, instance.py, starter.py; tests/labs/M7/lab-M7-project-1..3.py",
  "status": "PASS", "evidence": "MYPYPATH=grader .venv/bin/mypy --no-incremental --strict reference.py instance.py starter.py lab-M7-project-1..3.py: 'Success: no issues found in 6 source files' (mypy_project.log). ruff check grader and tests/labs/M7: 'All checks passed!' (ruff_check.log); ruff format --check: 15 files already formatted (ruff_format.log)."},
 {"id": "PRJ-D1-30", "check": "2.5 labs: pytest on lab twins", "location": "tests/test_labs.py -k M7; tests/labs/M7/lab-M7-project-1..3.py",
  "status": "PASS", "evidence": "pytest -q tests/test_labs.py -k M7: 11 passed, exit 0 (pytest_labs_M7.log). tests/test_run_labs.py and tests/test_page_checks.py -k 'M7 or project' select no test (exit 5, pytest_pagechecks_M7.log); not a finding."},
 {"id": "PRJ-D1-31", "check": "2.6 autograder 5: same suite in Pyodide and locally", "location": "project.html:359; grader/test_project.py:3-7",
  "status": "PASS", "evidence": "Local: the page's flags (-p no:cacheprovider --assert=plain -W error) on seeds 0-49. Browser: page_smoke PASS runs the grader panel in Chromium with the reference (PRJ-D1-20). Panel attributes data-suite, data-support, data-solution, data-starter present at project.html:359."},
 {"id": "PRJ-D1-32", "check": "2.6 atlas milestone", "location": "project.html; curriculum/01-foundations.yaml M7; plans/M7-build-plan.md T1",
  "status": "PASS", "evidence": "No atlas key in the panel; no Atlas branch applies (plan T1 says no Atlas milestone). check_projects --unit M7 PASS (check_projects.log)."},
 {"id": "PRJ-D1-33", "check": "2.1 / 2.6 reading list: registry keys", "location": "project.html:465-466",
  "status": "PASS", "evidence": "boyd2004convex and stokey1989recursive are entries in references/references.json and are listed in the M7 curriculum sources (curriculum/01-foundations.yaml, M7 sources). verify_refs.py --offline: '560 entries, 0 problems' (verify_refs_offline.log). The page says no reading is needed to pass (:334), which is consistent with the specification being self-contained."},
 {"id": "PRJ-D1-34", "check": "2.6 hours: own estimate per component", "location": "project.html:344-350",
  "status": "PASS", "evidence": "Sum 2+3+10+6+7+5 = 33 (see PRJ-D1-16). Per-component hours are design targets (ruling), and the arithmetic is consistent."},
 {"id": "PRJ-D1-35", "check": "2.6 autograder 3: every mutant killed", "location": "ledgers/M7/mutants/*.py (147 files)",
  "status": "PASS", "evidence": "mutate_graders.py --unit M7 --seeds 0-9 over the 143 mutants present at the start: 143/143 KILLED, exit 0 (" + L + "mutate_all_r3_0-9.log). The four round-3 mutants x3_01..x3_04 run through the same procedure (seeds 0-9, stop at first failure, " + L + "x3_mutants_kill.log): x3_01, x3_02, x3_03 KILLED; x3_04 SURVIVED (see PRJ-D1-37)."},
 {"id": "PRJ-D1-36", "check": "2.6 autograder 3: at least three new student-error mutants by this verifier", "location": "ledgers/M7/mutants/x3_01..x3_04",
  "status": "PASS", "evidence": "Four new mutants written this round (" + L + "make_x3.py generates them from grader/reference.py with one change each, asserting each replacement matches exactly once): x3_01 memoised by asset count, x3_02 sector cap sign reversed (a floor), x3_03 box upper bounds loosened by 1e-7, x3_04 dual residual without the floor. Each is a complete module with a docstring first line naming the error."},
 {"id": "PRJ-D1-37", "check": "2.6 mutation: dual-residual floor is tested", "location": "project.html:317, 320; grader/test_project.py:108-109, 356-362; ledgers/M7/mutants/x3_04_dual_residual_reported_without_the_floor.py",
  "status": "FAIL", "evidence": "x3_04 (dual residual = -min m with no floor) SURVIVES seeds 0-9 (" + L + "x3_mutants_kill.log). The page states the floor as a checked property: project.html:317 defines dual residual as the larger of 0 and the negative of the smallest multiplier, and :320 says an answer whose smallest multiplier exceeds 1e-9 is checked against the floor. Round 2 disclosed that no mutant separates the floor; round 3 removed that disclosure. The reason it survives: every reference multiplier vector has smallest entry exactly 0 (PRJ-D1-06; the working set has at most n-1 inequality rows, so at least n+1 of the 2n bound multipliers are zero), so the unfloored report agrees with the floored recomputation on every output the suite can produce. The page's rule 'a surviving mutant that violates a stated behaviour is a FAIL' applies.",
  "fix": "Either (a) add a hand case whose correct multipliers are unique and all inequality multipliers are strictly positive (degenerate fixed-bound case; the verifier did not find one with unique multipliers), and assert the reported dual residual against the floored recomputation there; or (b) restate :320 so it does not claim that answers with a positive smallest multiplier are checked, and say the floor is part of the definition that the suite does not separate from its absence."},
 {"id": "PRJ-D1-38", "check": "2.6 autograder: five alternative correct implementations pass seeds 0-49", "location": L + "alts_run/*.log; " + L + "brute_vs_reference_0-49.log",
  "status": "UNVERIFIABLE", "evidence": "Four alternatives pass 50 of 50 seeds 0-49 (alts_run/: alt_empty_start, alt_nullspace, alt_lu_solver, alt_float_active_set_r3v; exact or float active-set variants, the last two from an earlier round-3 attempt in this checkout and re-run here) and alt_fraction_output (reference with Fraction outputs) passes 50 of 50. The fifth, alt_brute_float (exhaustive working-set enumeration in floats, a genuinely different method, sources in " + L + "alts/), agrees with the reference to 5e-16 on weights and certificate fields <= 2.2e-16 on all 50 seeds (brute_vs_reference_0-49.log), passes the full suite on all 18 three-asset seeds and all 14 four-asset seeds (brute_tol_n3_seeds.log, brute_tol_n4_seeds.log), but on five-asset seeds the suite run timed out at 600 s per seed (brute_tol_n5_seeds.log: seed 1 TIMEOUT; 17 further seeds not run, the run was stopped). Status: " + brute_status + "."},
 {"id": "PRJ-D1-39", "check": "2.9 / BLUEPRINT 7: reference.py excluded from deployment", "location": "course/modules/M/M7/grader/reference.py; BLUEPRINT.md:400-401; plans/M7-build-plan.md:408 (T6)",
  "status": "UNVERIFIABLE", "evidence": "BLUEPRINT.md:400-401 requires deployment to exclude every grader/reference.py. The repository has no deployment config that does so: no vercel.json, no deploy workflow (.github/workflows/ci.yml only uploads screenshots), no .vercelignore; .gitignore does not exclude it. The publishing path is outside this repository, so the exclusion cannot be read. Counts as a failure until the deploy config is shown."},
 {"id": "PRJ-D2-01", "check": "2.6 autograder over-constraint: exact-arithmetic output accepted (round-2 FAIL, re-verified)", "location": "grader/test_project.py:136-138, 293-297; project.html:330",
  "status": "PASS", "evidence": "Round 2 FAIL resolved: is_real_number (test_project.py:162-164) accepts Fraction. The reference with every float( replaced by an identity, returning Fractions (alts/alt_fraction_output.py), passes 50 of 50 seeds (alts_run/alt_fraction_output_0-49.log). project.html:330 says ints, floats or Fractions."},
 {"id": "PRJ-D2-02", "check": "2.9 scope claim", "location": "project.html:450",
  "status": "PASS", "evidence": "'Under the hypotheses of the proposition, exact multipliers and an exactly feasible answer make the answer the minimizer' is the proposition (T). 'Nothing else' claims are limited to what the suite does not test; no file reads; every case carries the SIMULATED label (instance.py:57, hand cases test_project.py:209, 230)."},
 {"id": "PRJ-D2-03", "check": "2.6 code comment: iteration cap", "location": "grader/reference.py:206",
  "status": "PASS", "evidence": "Comment: 'a cap far above the iterations the search uses on seeds 0 to 49 (at most 12)'. Counted the active-set steps per seed on seeds 0-49: maximum 12 (" + L + "iterations_and_variety_0-49.log)."},
 {"id": "PRJ-D2-04", "check": "2.4 test comments: hand-worked answers", "location": "grader/test_project.py:223-248",
  "status": "PASS", "evidence": "Re-derived by hand: budget only w = mu + 0.3 = (0.6, 0.4); zero turnover w = w0; single asset w = 1; upper bound binding (0.35, 0.65) cut to (0.7, 0.3) with lambda^u = 0.7 >= 0; turnover binding: 2|d| <= 0.2 gives |d| = 0.1, w = (0.6, 0.4). The reference passes assert_kkt on all five (run_graders_0-49.log)."},
 {"id": "PRJ-D2-05", "check": "2.4 test comment: starting portfolio as the answer", "location": "grader/test_project.py:376-382",
  "status": "PASS", "evidence": "Comment lists seeds 162, 163, 182, 267 among seeds 0 to 299. Computed with the reference: exactly [162, 163, 182, 267] (seed_facts_r3.log)."},
 {"id": "PRJ-D2-06", "check": "2.4 test comments: eigenvalue and definiteness cases", "location": "grader/test_project.py:430-444",
  "status": "PASS", "evidence": "All-0.01 matrix: second LDL pivot 0.01 - 0.0001/0.01 = 0 (singular). 0.01 J + 0.0001 I has smallest eigenvalue 0.0001 (> 0). Negative-diagonal matrix is negative definite. Leading block [[0.01, 0.02], [0.02, 0.01]] has determinant 0.0001 - 0.0004 < 0."},
 {"id": "PRJ-D2-07", "check": "2.4 instance docstring", "location": "grader/instance.py:1-11, 57",
  "status": "PASS", "evidence": "'at most three digits after the point': divisions at instance.py:41 (/1000), :44 (/1000), :46/:47/:48/:54 (/100), :55 (/100). 'feasible by construction': w0 in box (lower <= 0 <= w0 <= upper), caps >= start sector sums, turnover >= 0. The SIMULATED label is at :57. The word 'covariance' at :4 is a separate row (PRJ-D3-02)."},
 {"id": "PRJ-D2-08", "check": "2.4 cross-reference: Lagrangian sign convention", "location": "project.html:310; course/modules/M/M7/L03.html:57, 62",
  "status": "PASS", "evidence": "L03.html:57 defines g_i(x) <= 0 and :62 writes L = f + sum lambda_i g_i + sum nu_j h_j with lambda >= 0. project.html:310 uses the same convention (each inequality written g_j <= 0)."},
 {"id": "PRJ-D3-01", "check": "BLUEPRINT/B1: covariance appears only in a no-link disclaimer (architect decision)", "location": "course/modules/M/M7/grader/instance.py:4; plans/M7-build-plan.md:479-480 (B1/Q1)",
  "status": "FAIL", "evidence": "The architect's binding decision (plans/M7-build-plan.md B1/Q1) says covariance appears only in a no-link disclaimer. project.html:292 keeps that disclaimer. But grader/instance.py:4 says 'a covariance matrix equal to (A-transpose A plus the identity) over 1000', and project.html:359-366 links instance.py for the learner to copy and run. So the word appears in learner-visible code outside the disclaimer.",
  "fix": "Change instance.py:4 to 'a risk matrix Sigma equal to (A-transpose A plus the identity) over 1000'."},
 {"id": "PRJ-D3-02", "check": "over-constraint probe: float solver with absolute cutoffs (stale alt_float_r3)", "location": L + "alts/alt_float_r3.py; alts_run/alt_float_r3_0-49.log",
  "status": "PASS", "evidence": "This float alternative (absolute 1e-12 rank and pivot cutoffs, not scaled) passes 0 of 50 seeds. Each failure is a RuntimeError ('the working set lost independence', 'did not converge') raised on a page-valid input: bounds equal to the start (project.html:326 says valid), gamma = 1e-6 (project.html:326, 332). The suite is right to demand acceptance of these inputs; the alternative's cutoffs are the defect. Not a suite over-constraint. Other correct alternatives with the same method and scaled tolerances pass 50 of 50."},
]
# mutant ids for the x3 round-3 set are in mutants (already appended)
verdict = "PASS" if all(r["status"] == "PASS" for r in rows) and all(m.get("killed_by") for m in mutants) else "FAIL"
counts = {s: sum(1 for r in rows if r["status"] == s) for s in ("PASS", "FAIL", "UNVERIFIABLE")}
fragment = {
 "unit": "M7", "slice": "M7-d", "round": 3,
 "verifier": "Claude Haiku 5.5, independent verifier for M7-d, round 3 (did not build M7-d; works in its own checkout)",
 "pin": "a007712fdbfc8b4851123f4de76b5310ac5a9e64",
 "base": "c737272f5bdef4a027417989cd52254555e8a0bb (round-2 pin). Slice delta since that pin: project.html (Lab 1 hypothesis; Lab 1 and Lab 2 step-2 comment; Conventions 'A point w that meets all of these constraints is feasible' and 'multipliers of the linearized problem'; the floor sentence at :320; the Proposition-intro sentence at :322; the Hypotheses and seeds sentence at :325; the Constraints item at :330); grader/test_project.py (is_real_number, Fraction-tolerant output checks); tests/labs/M7/lab-M7-project-1.py and -2.py (step-2 comment). grader/reference.py, instance.py, starter.py and lab-M7-project-3.py are byte-identical. Every subject that changed was re-verified from scratch; no row is carried.",
 "checkout": "/Users/billyribeiro/.fanout/wt/verifyD3-M7-d",
 "scratch": "/tmp/m7d-r3-indep (scripts, alternatives), /tmp/m7d-r3-ref, /tmp/m7d-r3-collect-*, /tmp/m7d-r3-run-* (alternative suite runs), /tmp/m7d-r3-stale (earlier attempt's scripts, moved aside, not relied on)",
 "verified_at": NOW,
 "verdict": verdict,
 "rows": rows,
 "mutants": mutants,
 "registry_flags": [],
 "freshness_flags": ["checkout at start held an earlier round-3 attempt's untracked scripts and ledger; moved aside to /tmp/m7d-r3-stale; the untracked mutants d3_01..d3_04 were kept, re-run, and are killed"],
 "notes": "Round 3 on a007712 (round-2 pin c737272). Counts: rows %d (PASS %d, FAIL %d, UNVERIFIABLE %d); mutants %d (%d killed). Non-PASS: PRJ-D1-23 (build census in learner text), PRJ-D1-37 (dual-residual floor not separated by any suite test; x3_04 survives), PRJ-D1-38 (five-alternative check incomplete: brute n=5 seeds timed out), PRJ-D1-39 (no deploy exclusion in repo), PRJ-D3-01 (covariance word in instance.py:4). Round-2 FAIL PRJ-D2-01 (Fraction outputs) is now PASS. Round-2 PASS PRJ-D1-37 is now FAIL because the page no longer discloses the untested floor. Not checked: the in-browser Pyodide run beyond page_smoke's own run; hours re-estimate (ruling); cards.json (not in this slice); the five-asset seeds for the brute alternative (timed out). The ps-visible pytest workers of the brute alternative's killed n=5 run may still be running in /tmp/m7d-r3-run-alt_brute_float_tol1e-8 (the user should stop them; the verifier's attempt to kill them was denied)." % (len(rows), counts["PASS"], counts["FAIL"], counts["UNVERIFIABLE"], len(mutants), sum(1 for m in mutants if m.get("killed_by"))),
 "summary": "M7-d round 3: verdict FAIL. Rows %d: PASS %d, FAIL %d, UNVERIFIABLE %d. Mutants %d: %d killed (seeds 0-9); x3_04 survives. Alternatives: 4 of 5 pass 50/50; brute alternative agrees with the reference on 50/50 seeds and passes the suite on 32 of 32 seeds with n in {3,4}; n=5 seeds not finished." % (len(rows), counts["PASS"], counts["FAIL"], counts["UNVERIFIABLE"], len(mutants), sum(1 for m in mutants if m.get("killed_by"))),
}
out = R / "ledgers/M7/M7-d.json"
out.write_text(json.dumps(fragment, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out, "rows", len(rows), counts, "mutants", len(mutants), "verdict", verdict)
