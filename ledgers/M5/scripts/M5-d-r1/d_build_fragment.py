"""Build the slice-d round-1 fragment ledgers/M5/M5-d.json from the evidence written this round.

Mutant records are parsed from the saved output of tools/mutate_graders.py (mutate_M5_seeds0-9.out), so every
listed mutant is one the gate actually ran. Six pre-existing mutants whose first docstring line is the reference
docstring take their description from the '#' comment line that names the error (see row M5-d-r1-08).
Usage (from the checkout root): python3 -I ledgers/M5/scripts/M5-d-r1/d_build_fragment.py
"""

import json
import os
from datetime import UTC, datetime
import re

ROOT = os.getcwd()
S = "ledgers/M5/scripts/M5-d-r1"
PIN = "aeb512b65b7774b59b84f836a13984fcfe9d0d1f"
GRADER = "course/modules/M/M5/grader"


def row(rid, check, location, status, evidence, fix=None):
    out = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        out["fix"] = fix
    return out


ROWS = [
    row("M5-d-r1-01", "2.6-autograder-reference", GRADER + "/reference.py", "PASS",
        "tools/run_graders.py --unit M5 --seeds 0-49 printed 'run_graders M5: PASS (reference 50/50 seeds, slowest 0.3 s)' with exit 0 (" + S + "/run_graders_M5_0-49.out)."),
    row("M5-d-r1-02", "2.6-instances", GRADER + "/instance.py", "PASS",
        "All 50 seeds (a superset of the required sample of 20) checked by " + S + "/d_survivor_and_instances.py: every draw lies in the ranges of the instance.py docstring (beta 0.80-0.95, alpha 0.30-0.70, 8-24 points, first point in [0.20,0.90], steps in [0.05,0.40], last point > 1, tol in {1e-6,1e-8,1e-10}) and is clear of ties. Output: invalid seeds [], 15 distinct betas, 27 alphas, 17 sizes, 50 of 50 distinct solved value vectors (" + S + "/d_survivor_and_instances.out)."),
    row("M5-d-r1-03", "2.6-mutation-existing", "ledgers/M5/mutants/ (112 pre-existing files)", "PASS",
        "tools/mutate_graders.py --unit M5 --seeds 0-9: all 112 pre-existing mutants KILLED (" + S + "/mutate_M5_seeds0-9.out). The gate exits 1 only because of the new survivor d1_01 (row M5-d-r1-05)."),
    row("M5-d-r1-04", "2.6-mutation-new-killed", "ledgers/M5/mutants/d1_02_continuation_reads_the_current_state.py; ledgers/M5/mutants/d1_03_value_is_the_penultimate_iterate.py", "PASS",
        "Written this round as complete modules derived from reference.py by " + S + "/d_make_mutants.py. d1_02 (continuation term beta*V at the current state) is killed by test_operator_matches_its_definition[0], with 14 failing tests over seeds 0-9 (" + S + "/d_mutant_d1_02_seeds0-9.out). d1_03 (solve returns the penultimate iterate while certified_error refers to the last sweep) is killed by test_certified_error_bounds_the_distance_to_the_fixed_point[0] on seed 0 (" + S + "/d_mutant_d1_03_seeds0-9.out)."),
    row("M5-d-r1-05", "2.6-mutation-survivor", GRADER + "/test_project.py (no test on a grid wholly in (0,1]); ledgers/M5/mutants/d1_01_top_grid_point_never_a_successor.py", "FAIL",
        "Mutant d1_01 drops the top grid point from the successor loop (zip(grid[:-1], values[:-1])). It passes all 96 tests on seeds 0-9 (" + S + "/d_mutant_d1_01_seeds0-9.out) and the gate reports it SURVIVED (" + S + "/mutate_M5_seeds0-9.out). Why the suite cannot see it on its own instances: make_instance always has last point > 1 (instance.py:51), and for every state k <= k_m, k**alpha <= k_m**alpha < k_m, so the top point is never feasible. Mutant and reference agree on 50 instances x 5 random vectors (" + S + "/d_survivor_and_instances.out). The page says the maximum is over the grid points of the feasible set (project.html:243), and a grid wholly in (0,1] is valid: project.html:240 allows any positive grid with k_1 <= 1, and the invalid-grid list at project.html:248 does not exclude it. The behaviour is specified and the suite does not test it. Observed differences on valid (0,1] grids: bellman_operator([0.5,1.0], beta 0.9, alpha 0.5, values [0,10]) gives [0.455090, 9.0] by the reference and [0.455090, 0.707107] by d1_01; solve on [0.06,0.07,0.24], beta 0.83, alpha 0.53 gives V(0.24) = 2.8171887 by the reference and by an independent loop (" + S + "/d_top_point_fixed_point.out), and 2.6702295 by d1_01 (" + S + "/d_search_solver_diff.out).",
        "Add a test to " + GRADER + "/test_project.py that checks bellman_operator and solve against the test's own ref_sweep and ref_fixed_point on a grid wholly in (0,1]: for example grid [0.5, 1.0] with beta 0.9, alpha 0.5 and values [0.0, 10.0] (top entry 9.0 by ref_sweep), and grid [0.06, 0.07, 0.24] with beta 0.83, alpha 0.53 (V(0.24) = 2.8171887 by ref_fixed_point). d1_01 must then fail it. Then re-run run_graders --unit M5 --seeds 0-49 and mutate_graders --unit M5 --seeds 0-9."),
    row("M5-d-r1-06", "2.6-alternatives", "ledgers/M5/alternatives/alt1..alt5", "PASS",
        "Run by " + S + "/d_run_candidate.py on seeds 0-9 (" + S + "/d_alternatives_seeds0-9.out). alt3 (comprehension over feasible index lists), alt4 (bisection for feasible successors) and alt5 (reverse-order synchronous sweep) pass 96/96 on every seed. alt1 (in-place Gauss-Seidel sweep) and alt2 (stop on the residual, bound residual/(1-beta)) fail 6-9 tests per seed. Neither is a conforming implementation under the page: project.html:244 says each sweep is synchronous, and project.html:245 says 'No other bound is accepted'. Their failures follow from those sentences and are not over-constraint."),
    row("M5-d-r1-07", "2.6-failure-message-leak", GRADER + "/test_project.py:440", "FAIL",
        "The message of test_saving_above_the_current_capital_is_feasible_within_resources reads 'the operator must take the feasible successor 0.4 at k = 0.25, which the resources 0.25**0.5 = 0.5 allow'. It names the optimal successor of the check, which VERIFIER_RULES 2.6(4) forbids ('never leak the answer'). The check uses a hand-picked grid, so the leak is of a toy answer, but it is still the answer.",
        "Replace the message at test_project.py:439-440 with: 'the operator must choose the feasible successor with the largest value at this state, and every saving k' with k' <= k**alpha is feasible'. Remove the named successor and the numbers."),
    row("M5-d-r1-08", "2.6-mutant-docstring", "ledgers/M5/mutants/v11_01_utility_uses_capital_not_output.py; v11_02_operator_returns_the_best_successor_not_the_value.py; v11_03_converged_means_budget_not_exhausted.py; v12_01_stop_test_uses_beta_times_change.py; v12_02_continuation_read_in_reverse_order.py; v12_03_value_returned_is_beta_times_the_iterate.py", "FAIL",
        "In all six files the first docstring line is the reference module docstring ('Reference solution for the M5 project: ...'). tools/mutate_graders.py:47-60 therefore reports the reference text as each mutant's description (" + S + "/mutate_M5_seeds0-9.out, the six KILLED lines for v11_* and v12_*). The error sentence is only in a '#' comment on line 1. VERIFIER_RULES 2.6(3) requires the docstring's first line to describe the error. The six are killed, so this is a record defect and not a grader defect.",
        "In each of the six files, move the error sentence from the '#' comment into the first docstring line, e.g. '\"\"\"Student-error mutant (verifier-written, M5 slice d round 11): <error>.\"\"\"', keeping the reference text after it. Then re-run tools/mutate_graders.py --unit M5 --seeds 0-9."),
    row("M5-d-r1-09", "2.6-test-count", "course/modules/M/M5/project.html:235; " + GRADER + "/test_project.py", "PASS",
        "Collect-only in a scratch copy (instance.py, test_project.py, and reference.py as contraction_solver.py): '96 tests collected' (" + S + "/d_collect_only.out). project.html:235 says the suite runs 96 checks."),
    row("M5-d-r1-10", "2.6-same-suite-browser-and-local", "course/modules/M/M5/project.html:272-281; course/assets/js/python.js", "PASS",
        "tools/page_smoke.py --unit M5 --pages project: PASS, zero console errors, 'in-browser grader: All 96 tests pass' (" + S + "/d_page_smoke_M5_project.out). The local command on project.html:279 (QF_SEED=4242 pytest -q -p no:cacheprovider --assert=plain -W error test_project.py) gives 96 passed with reference.py as contraction_solver.py, and 96 failed with starter.py."),
    row("M5-d-r1-11", "2.6-rubric-observable", "course/modules/M/M5/project.html:412 (C6, level-4 cell)", "FAIL",
        "The level-4 descriptor for C6 ends 'and says in what sense the bound is certified'. No content can be checked against it, so a pass and a fail cannot be told apart. VERIFIER_RULES 2.6 Rubric (1) requires observable descriptors.",
        "Replace 'and says in what sense the bound is certified' at project.html:412 with 'and states the inequality the bound certifies, ||V_n - V*|| <= beta/(1-beta) * ||V_n - V_(n-1)||, and the fixed point it refers to'."),
    row("M5-d-r1-12", "2.9-prose-dangling-reference", "course/modules/M/M5/project.html:404 (rubric caption)", "FAIL",
        "The caption says the six criteria are 'scored by the rule above'. No scoring rule is stated above the table (project.html:393-403). The scoring form is the self-assessment section at project.html:484. The reference points at nothing.",
        "Replace 'scored by the rule above' at project.html:404 with 'scored with the self-assessment form below'."),
    row("M5-d-r1-13", "2.6-rubric-calibration-exemplar-a", "course/modules/M/M5/project.html:420-450", "PASS",
        "Blind scores from the descriptors (project.html:407-412) applied to the passage: C1 2, C2 2, C3 1, C4 2, C5 2, C6 2. Official data-scores 2,2,1,2,2,2 (project.html:420). All six agree within one level. Caveat: the reveal line (project.html:422) was visible when I read the file before scoring, so the blindness is partial. I scored from the descriptors and the passage text."),
    row("M5-d-r1-14", "2.6-rubric-calibration-exemplar-b", "course/modules/M/M5/project.html:452-482", "PASS",
        "Blind scores: C1 4 (all five named), C2 4 (each step names its property), C3 4 (coordinatewise step), C4 4 (geometric sum shown), C5 4 (every number printed by Lab 3, with instance and tolerance), C6 3 (grid limitation and scope, no direction of the error). Official data-scores 4,4,4,4,4,3. Match on all six. Same caveat as M5-d-r1-13."),
    row("M5-d-r1-15", "2.6-hours-arithmetic", "course/modules/M/M5/project.html:33,258-264; course/modules/M/M5/index.html:29", "PASS",
        "Components 1+2+8+7+3+5 = 26 = data-hours-project (project.html:33). Hub 104 + 26 = 130 (index.html:29). 26/130 = 20.0%. My own estimates: rung 1 about 1 h, rung 2 1.5-2 h, proof write-up 6-10 h, solver and tests 3-7 h, self-check 2-3 h, revision 3-5 h. The midpoint sum is about 22 h, and 26 h is about 17% above it, inside the 30% band."),
    row("M5-d-r1-16", "2.5-labs-twins-run", "course/modules/M/M5/project.html:55-220,287-390; tests/labs/M5/lab-M5-project-1..3.py", "PASS",
        "tools/run_labs.py --unit M5 --page project: 'run_labs M5: PASS (3/3)' (" + S + "/d_run_labs_M5_project.out). Twins run under python -I -W error; page code equals the twin; completion-lab lines equal the twin or contain blanks; expected blocks equal the output. pytest tests/test_labs.py -k M5: 13 passed (" + S + "/d_pytest_labs_M5.out)."),
    row("M5-d-r1-17", "2.5-lab1-numbers", "course/modules/M/M5/project.html:57,148-155", "PASS",
        "Recomputed by " + S + "/d_numbers_project.py in full precision: resources 0.7071067811865476, 0.9486832980505138, 1.1832159566199232; V1 = 0.4550898605622274, 0.6698382626056186, 0.8265687851715204; sup|BV-BW| = 0.4095808745 <= beta*sup|V-W| = 0.7439119067; sweep-1 certified error 7.439119066543685 (prints 7.439119); stop at sweep 146; certified 9.495187356e-7 and actual 9.495177729e-7, both printing 0.000000950 (" + S + "/d_numbers_project.out)."),
    row("M5-d-r1-18", "2.5-lab2-numbers", "course/modules/M/M5/project.html:161,215-219", "PASS",
        "Completed lines recomputed (" + S + "/d_numbers_project.out): ratio 0.3000000000000001 prints 0.300000 and is <= beta; 146 sweeps; certified 9.495187356e-07 prints 9.495e-07 and matches the prose value 9.495187e-7 (difference 3.6e-14); last change 1.0550208e-07 prints 1.055e-07; values 4.550898, 4.765646, 4.922377."),
    row("M5-d-r1-19", "2.5-lab3-numbers", "course/modules/M/M5/project.html:289,373-388; exemplar text :432,:464,:466", "PASS",
        "Recomputed (" + S + "/d_numbers_project.out): smallest gap 0.0218289 (> 1e-6; prints 0.021829); 236 sweeps; last change 1.0251355e-11 (prints 1.025e-11); certified 9.226220e-11 (prints 9.226e-11); a priori count 242 (U = 1.1606588); residual 9.226397e-12 (prints 9.226e-12) <= (1+beta)*certified = 1.753e-10; worst ratio over 200 pairs 0.9000000000000001, 1.1e-16 above beta and inside the stated 1e-12 margin; V values match the printed table. The exemplar numbers 1.025e-11, 9.226e-11, 242 and 9.226e-12 all match. Exemplar A's '240 sweeps' is the annotated miss (236 printed)."),
    row("M5-d-r1-20", "2.6-proof-A1-A4", "course/modules/M/M5/project.html:393-399; exemplar proofs :459-466", "PASS",
        "Re-derived by hand. A1 (hypotheses: positive grid with k_1 <= 1, alpha in (0,1), beta in (0,1)) makes every feasible set nonempty (k^alpha >= k >= k_1 for k <= 1; k^alpha > 1 >= k_1 for k > 1). The inequality |max f - max g| <= max|f - g| then gives the contraction with modulus beta. A2 is the finite-dimensional completeness argument. A3 follows from A1 by the Banach argument, and uniqueness uses beta < 1. A4 is the geometric-sum bound beta/(1-beta) times the last change. No counterexample found. The seeded pairs of Lab 3 also show ratio <= beta. Scope disclaimers are present (project.html:219, :389)."),
    row("M5-d-r1-21", "2.6-spec-vs-grader-invalid-inputs", "course/modules/M/M5/project.html:240-248; " + GRADER + "/test_project.py:557-673", "PASS",
        "Every named invalid input has a test that expects ValueError: beta/alpha (lines 557-570), tol (580-585), max_iter (601-607), grid (616-651), values length (669-673). The ValueError demands match only page-named conditions, and the non-real, boolean and non-finite cases fall under the page's 'not a real number' wording. The certified-error formula is checked on sweeps 1, 2 and 3 (lines 312-331), as project.html:245 states."),
    row("M5-d-r1-22", "2.6-signatures", GRADER + "/starter.py:18,23; " + GRADER + "/reference.py:94,101; project.html:231", "PASS",
        "bellman_operator(params, grid, values) and solve(params, grid, tol, max_iter) match in starter.py, reference.py and the page. solve returns value, iterations, certified_error and converged (reference.py:123-128). The starter fails all 96 tests (row M5-d-r1-10)."),
    row("M5-d-r1-23", "2.6-browser-timeout-claim", "course/modules/M/M5/project.html:233; course/assets/js/python.js:4,36", "PASS",
        "python.js:4 sets TIMEOUT_MS = 120000 and python.js:36 prints 'Stopped after 120 s', which matches 'stops after 120 seconds' (project.html:233)."),
    row("M5-d-r1-24", "2.2-notation", "course/modules/M/M5/project.html; notation/notation.json", "PASS",
        "Symbols used: beta, alpha, k, k', V, W, u, c, m, n (local, as the notation.json 'about' text allows), \\R (registered: real numbers), \\mathcal{B} (not registered; defined at project.html:243 and forward-referenced at :227 as 'defined in the conventions below'). No registered symbol (T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q}) is used with another meaning (grep of project.html)."),
    row("M5-d-r1-25", "2.9-dag-and-concepts", "course/modules/M/M5/project.html:37,227,495,502", "PASS",
        "Links: contraction-mapping -> L07.html#def-contraction-mapping (L07 defines it) and value-function-iteration -> L09.html#def-value-function-iteration (L09 defines it). Both are M5 lessons, inside the closure. No bellman-equation, dynamic-programming or policy-iteration link. 'Howard policy iteration' (:495) is prose only. The reading list uses M1 Lesson 6 (Geometric Series and Proof by Induction) and M5 L01, L02, L04, L07 (titles verified). tools/check_dag.py --unit M5: PASS (" + S + "/d_check_dag_M5.out)."),
    row("M5-d-r1-26", "2.9-banned-and-process-words", "course/modules/M/M5/project.html", "PASS",
        "tools/check_pages.py --unit M5: PASS, which includes the BUILDER_RULES 1.3-1.4 banned strings (" + S + "/d_check_pages_M5.out). grep for builder, verifier, planner, architect, ruling, slice, round, TODO and agent finds only 'planner' as the savings-model role (project.html:37, :227), which is domain language."),
    row("M5-d-r1-27", "2.9-page-smoke", "course/modules/M/M5/project.html", "PASS",
        "tools/page_smoke.py --unit M5 --pages project: PASS (" + S + "/d_page_smoke_M5_project.out). Zero console errors, math renders, no external requests, and the in-browser grader passes 96 of 96."),
    row("M5-d-r1-28", "2.6-references", "course/modules/M/M5/project.html:500-512; references/references.json", "PASS",
        "tools/verify_refs.py --unit M5: '2 of 560 entries, 0 problems' (" + S + "/d_verify_refs_M5_live.out). Offline integrity: 560 entries, 0 problems (" + S + "/d_verify_refs_offline.out). abbott2015understanding (DOI 10.1007/978-1-4939-2712-8) and rudin1976principles (Open Library) are registry keys. The page cites no locator and no theorem number, and says no passage was checked."),
    row("M5-d-r1-29", "2.6-gates-lint-type-test", GRADER + "; tests/labs/M5", "PASS",
        "ruff check and ruff format --check on grader and labs: clean, 17 files (" + S + "/d_ruff.out). mypy --no-incremental: 'Success: no issues found in 385 source files' (" + S + "/d_mypy.out). pytest tests/test_memo_exemplars.py tests/test_page_checks.py tests/test_run_labs.py: all pass (" + S + "/d_pytest_exemplars_pagechecks.out)."),
    row("M5-d-r1-30", "2.6-ladder-and-structure", "course/modules/M/M5/project.html:40-49,223-250,270-281,283-288,491-498", "PASS",
        "Four rungs in order (worked example, completion, independent project, stretch). Rung 1 is solved and annotated. Rung 2 is class 'lab completion'. Rung 3 spec names context, inputs, outputs, constraints and grading mode (both). The grader panel is present. Stretch items are open-ended. tools/check_projects.py --unit M5: PASS (" + S + "/d_check_projects_M5.out)."),
    row("M5-d-r1-31", "2.6-instance-label", GRADER + "/instance.py:3; project.html:229", "PASS",
        "instance.py:3 says 'All values are SIMULATED.' and instance.py:18 says 'Nothing here is a real economy'. project.html:229 says 'All of it is SIMULATED: generated parameters, not data.' The plan's wording 'generated parameters; not data' (plan 5.3) is not used verbatim, but the SIMULATED label is present, as required."),
    row("M5-d-r1-32", "2.6-scope-words", "course/modules/M/M5/project.html:156,219,389", "PASS",
        "Scope is stated: Lab 3's contraction check is on 200 pairs and 'not a proof' (:389); 'the printed values ... say nothing about any other grid' (:389); Lab 1's agreement to nine decimals is 'a property of this instance' (:156); Lab 2 'proves nothing else' (:219). The lab hypotheses state their numbers before the run, and those numbers match the outputs (M5-d-r1-17 to M5-d-r1-19)."),
]


def load_mutants():
    records = []
    with open(os.path.join(ROOT, S, "mutate_M5_seeds0-9.out"), encoding="utf-8") as handle:
        for line in handle:
            match = re.match(r"^(KILLED|SURVIVED) (\S+?): (.*) -> (.*)$", line.rstrip("\n"))
            if not match:
                continue
            _, name, description, killer = match.groups()
            killed_by = None if killer.strip() == "None" else re.sub(r" \(seed \d+\)$", "", killer.strip())
            if name.startswith(("v11_0", "v12_0")):
                with open(os.path.join(ROOT, "ledgers/M5/mutants", name), encoding="utf-8") as src:
                    description = src.readline()[2:].strip()
            records.append({"name": name, "description": description, "killed_by": killed_by})
    return records


MUTANTS = load_mutants()
fragment = {
    "unit": "M5",
    "slice": "d",
    "round": 1,
    "verifier": "Haiku independent verifier (round 1), no build context",
    "pin": PIN,
    "base": PIN,
    "checkout": ROOT,
    "scratch": os.path.join(ROOT, S),
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "verdict": "FAIL" if any(r["status"] != "PASS" for r in ROWS) else "PASS",
    "rows": ROWS,
    "mutants": MUTANTS,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Round 1 of the fanout. The file ledgers/M5/M5-d.json previously held a round-12 fragment (pin ff388424, verdict PASS, rows M5-d-R01..R12). This round-1 fragment replaces it at the path the orchestrator named. The prior file stays in git history.",
        "Surviving grader mutant d1_01 (row M5-d-r1-05) contradicts the prior round-12 PASS on the same slice. The evidence is reproducible with the scripts listed in the row.",
        "Blind exemplar scoring is partial: the reveal lines were visible when the file was read before scoring (M5-d-r1-13, M5-d-r1-14).",
        "Alternatives: 3 of 5 conforming alternatives pass; alt1 (in-place sweep) and alt2 (residual bound) fail on conventions the page states explicitly (M5-d-r1-06).",
        "Gate outputs: tools/mutate_graders.py --unit M5 --seeds 0-9 exits 1 with 114 of 115 killed. tools/run_graders.py --unit M5 --seeds 0-49 exits 0.",
        "tools/check_pages.py --page project is not a valid project-page check (it applies lesson rules and fails on every unit). The unit-level run, tools/check_pages.py --unit M5, passes and is the one recorded.",
    ],
    "summary": "Slice d round 1 (project.html, grader, project labs, mutants, alternatives). FAIL: one surviving grader mutant (d1_01: successor set omits the top grid point, undetectable on the grader's instances), one failure-message leak of a toy answer, six mutant files with a reference docstring as their description, two rubric wording defects (C6 level 4 not observable; dangling 'the rule above'). Passing: reference 50/50 seeds, 96 tests, instances valid and varied, 112 pre-existing mutants killed, labs 3/3, lab numbers recomputed, exemplars calibrated within one level, hours, DAG, notation, references, page smoke.",
    "what_not_checked": [
        "The Abbott and Rudin books were not read: the page asserts no passage locator and no theorem number from them, so nothing is attributed to them (plan 0.1; project.html:502).",
        "Interactive browser use of the self-assessment form and the grader panel was not exercised by hand; page_smoke ran the in-browser grader on Chromium.",
        "Lessons L01-L10, the hub and the cards are other slices and were not verified here, except for the titles and anchors that the project page links to.",
        "The live reference registry was checked for M5's 2 entries only (verify_refs --unit M5); the other 558 entries were checked offline.",
        "The full CI gate was not run (it belongs to the orchestrator before a push). Only the gates for this slice were run.",
        "Mutant killing is shown on seeds 0-9 as the gate runs it; seeds 10-49 were not separately mutation-tested.",
    ],
}

with open(os.path.join(ROOT, "ledgers/M5/M5-d.json"), "w", encoding="utf-8") as handle:
    json.dump(fragment, handle, indent=2, ensure_ascii=False)
    handle.write("\n")
print("wrote ledgers/M5/M5-d.json:", len(ROWS), "rows,", len(MUTANTS), "mutants, verdict", fragment["verdict"])
