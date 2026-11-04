"""Build the round-3 ledger fragment ledgers/E4/E4-d.json for slice d (verifier-authored; every row cites a log or script).

Usage: python3 -I ledgers/E4/scripts/E4-d-r3/write_fragment_r3.py <repo-root>
Mutant rows are read from logs/mutate_graders_E4_r3.txt (seeds 0-49), so the mutant list is the one the gate ran.
"""

import json
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
logs = root / "ledgers/E4/scripts/E4-d-r3/logs"
L = "ledgers/E4/scripts/E4-d-r3/logs/"
S = "ledgers/E4/scripts/E4-d-r3/"

rows = []


def row(rid, check, location, status, evidence, fix=None):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix or ""
    rows.append(r)


# ---- commands and gates
row("E4d-cmd-check-projects", "2.6", "course/modules/E/E4/project.html; grader/",
    "PASS", f"tools/check_projects.py --unit E4 -> 'check_projects E4: PASS', exit 0 ({L}check_projects.txt).")
row("E4d-cmd-check-pages", "2.9", "course/modules/E/E4/project.html",
    "PASS", f"tools/check_pages.py --unit E4 -> 'check_pages E4: PASS', exit 0 ({L}check_pages.txt; repeat {L}check_pages_E4_r3.txt).")
row("E4d-cmd-check-dag", "2.9", "course/modules/E/E4/project.html",
    "PASS", f"tools/check_dag.py --unit E4 -> 'check_dag E4: PASS', exit 0 ({L}check_dag.txt).")
row("E4d-cmd-run-labs", "2.5", "tests/labs/E4/lab-E4-project-1.py, -2.py, -3.py",
    "PASS", f"tools/run_labs.py --unit E4 -> 'run_labs E4: PASS (12/12)', exit 0 ({L}run_labs.txt).")
row("E4d-cmd-run-graders", "2.6 item 1", "course/modules/E/E4/grader/reference.py",
    "PASS", f"tools/run_graders.py --unit E4 --seeds 0-49 -> 'reference 50/50 seeds', exit 0 ({L}run_graders.txt); "
            f"{S}workspace_check.sh reference.py as solver.py: 0 failing seeds 0-49 ({L}workspace_check.txt).")
row("E4d-cmd-page-smoke-project", "2.6 item 5; 2.9", "course/modules/E/E4/project.html",
    "PASS", f"tools/page_smoke.py --unit E4 --pages project, run alone: labs 1-3 run in Pyodide; 'in-browser grader: All 30 tests "
            f"pass'; 'page_smoke E4: PASS', exit 0 ({L}page_smoke_project.txt).")
row("E4d-cmd-ruff", "gate", "tests/labs/E4; grader; repo",
    "PASS", f"ruff check tests/labs/E4 grader and ruff format --check on the same: exit 0 ({L}ruff_check.txt, {L}ruff_format.txt); "
            f"repo-wide ruff check . and ruff format --check . exit 0 ({L}ruff_repo_check.txt, {L}ruff_repo_format.txt).")
row("E4d-cmd-mypy-workspace", "2.6 / BUILDER_RULES 6.2 strict", "grader/test_project.py:32-33, :175",
    "PASS", f"{S}workspace_check.sh: strict mypy --no-incremental in the local layout (test_project.py, solver.py = reference.py, "
            f"instance.py): 'Success: no issues found in 3 source files', exit 0 ({L}workspace_check.txt). The round-2 unused-ignore "
            "and redundant-cast errors are gone (importlib.import_module and a typed local).")
row("E4d-cmd-mypy-plan-command", "gate", "tests/labs/E4; grader",
    "PASS", f"mypy --no-incremental tests/labs/E4 course/modules/E/E4/grader: 'Success: no issues found in 16 source files', exit 0 ({L}mypy_plan.txt).")
row("E4d-cmd-pytest-relevant", "gate", "tests/test_page_checks.py, test_labs.py, test_run_labs.py, test_memo_exemplars.py",
    "PASS", f"pytest -q on the four modules: exit 0 ({L}pytest_relevant_r3.txt).")
row("E4d-cmd-verify-refs", "2.1", "references/references.json (E4 keys)",
    "PASS", f"tools/verify_refs.py --unit E4: 'live re-verification of E4: 3 of 560 entries, 0 problems', exit 0 ({L}verify_refs_E4_r3.txt).")
row("E4d-cmd-collect", "2.6 grader count", "course/modules/E/E4/grader/test_project.py",
    "PASS", f"In the local layout (solver.py = reference.py): '30 tests collected' ({L}workspace_check.txt). project.html:319 states 30 checks. "
            f"A collect-only in the repository folder fails by design (no solver.py; {L}collect_only.txt), so the count was taken in the local layout.")

# ---- labs
row("E4d-lab-project-1", "2.5", "course/modules/E/E4/project.html #lab-E4-project-1; tests/labs/E4/lab-E4-project-1.py",
    "PASS", f"{S}cmp_project_labs.py: page code equals the twin line by line (only trailing newline differs); twin run as python -I -W error "
            f"exits 0; stdout equals the expected block ({L}cmp_project_labs.txt). Printed values reproduced by {S}indep_model.py §1 "
            f"({L}indep_model.txt).")
row("E4d-lab-project-2", "2.5 completion", "course/modules/E/E4/project.html #lab-E4-project-2 (line 217); tests/labs/E4/lab-E4-project-2.py",
    "PASS", f"{S}cmp_project_labs.py: the only differing line is line 40 of the page, 'return ___' (project.html:217); twin exits 0; stdout equals "
            f"the expected block ({L}cmp_project_labs.txt). {S}indep_model.py §2 reproduces +0.037435, -0.071386, 0.57052263, 0.12466375.")
row("E4d-lab-project-3", "2.5", "course/modules/E/E4/project.html #lab-E4-project-3; tests/labs/E4/lab-E4-project-3.py",
    "PASS", f"{S}cmp_project_labs.py: page code equals twin; exit 0; stdout equals expected block, including the nine rows and the 2.1e-13 "
            f"largest difference ({L}cmp_project_labs.txt). indep_model.py §3 reproduces all nine rows; props_check.py P4 max |closed form - "
            f"independent root| 2.7e-14 ({L}props_check.txt). The round-2 docstring 'T' is now tau_bar (lab-E4-project-3.py:51).")

# ---- numbers
row("E4d-num-lab-hypotheses", "2.2 (a)", "project.html:57, :176, :375 (Lab hypothesis paragraphs)",
    "PASS", f"Each stated number equals the printed twin output ({L}cmp_project_labs.txt) and the independent model ({L}indep_model.txt): Lab 1 "
            "+0.053092, -0.080731, 0.57937525, -3.45199422, 0.18904110, 0.15898618; Lab 2 +0.037435, -0.071386, 0.57052263, 0.12466375; "
            "Lab 3 fractions 0.5582/0.6978/0.8373 at cost 0.120 (0.558203, 0.697753, 0.837304 unrounded) and informativeness 0.1920, 0.1420, "
            "0.0889 (0.191963, 0.141997, 0.088941).")
row("E4d-num-exemplar-table", "2.2 (c)", "project.html:629-637 (Results table) and :625 (Results passage)",
    "PASS", f"Nine rows equal the Lab 3 printed output (project.html:488-496) and indep_model.py §3. Displayed ratios: 0.6978/0.5582 = "
            "1.250090 -> 1.2501, 0.8373/0.5582 = 1.500000 -> 1.5000; unrounded ratios are exactly 1.25 and 1.50 because lambda* is proportional "
            "to sigma at fixed cost (Prop 5). Max printed |gap| 3.55e-14 < 4e-14 (project.html:625).")
row("E4d-num-box-bounds", "2.2 (c)", "project.html:313 (Inputs); grader/instance.py:14-17",
    "PASS", f"{S}box_bounds_r3.txt (run of logs-cited r2 script ledgers/E4/scripts/E4-d-r2/box_bounds.py): tau_bar(0.120)=0.237567 -> 0.2376; "
            "tau_bar(0.150)=0.097623 -> 0.0976; min tau_y(1)=0.307692 -> 0.3077; worst corner 0 < tau_bar < tau_y(1) True. "
            f"{L}oracle_vs_independent.txt: 121-point 11x11 box grid, interior condition violated at 0 points.")
row("E4d-prose-lede-directional", "2.9 / 1.2 (scope)", "project.html:37 (lede)",
    "PASS", f"Lede now qualifies the claim: 'on the interior where the informed fraction lies strictly between 0 and 1'. "
            f"ledgers/E4/scripts/E4-d-r2/lede_fraction_check.py re-run on this pin ({L}lede_fraction_r3.txt): at cost 0.00 and 0.05 the fraction "
            "is 1.0 at every noise volume (outside the interior); at cost 0.13 it rises with the noise (0.482813 -> 1.0), as Prop 5 says on the interior.")

# ---- math
row("E4d-math-lemmas", "2.4", "project.html:266-273 (Lemmas 1-3)",
    "PASS", f"Re-derived by hand: Lemma 1 maximiser x*=(m-p)/(aV), g(x*)=(m-p)^2/(2aV); Lemma 2 Gaussian integral (V/(V+S))^(1/2); Lemma 3 "
            f"law of total variance. {L}indep_model.txt (gap by Gaussian quadratic-form determinant from the definitions, no lemma used) agrees "
            "with the page's closed forms to 1e-14.")
row("E4d-math-prop1", "2.4", "project.html:276-278 (Proposition 1)",
    "PASS", f"Re-derived steps (1)-(4): s-coefficient gives D b_s = lam tau_e + (1-lam) tau_y; u-coefficient gives -lam tau_e kappa = a. "
            f"{L}props_check.txt P1: max |b_s, b_u - closed form| 4.4e-16 over 20 (sigma, lambda) points. {L}indep_model.txt §4: clearing "
            "solution unique from 25 starts at 6 (lambda, sigma) pairs.")
row("E4d-math-prop2", "2.4", "project.html:284-285 (Proposition 2)",
    "PASS", f"Re-derived: Cov(v,p)=b_s/tau_v, Var(p)=b_s^2(1/tau_v+1/tau_y). {L}props_check.txt P2: max |Corr^2 - tau_y/(tau_v+tau_y)| 5.6e-17 "
            "from the Gaussian covariance matrix.")
row("E4d-math-prop3", "2.4", "project.html:287-291 (Proposition 3)",
    "PASS", f"Re-derived: sign G = sign(V_U - e^(2ac) V_I) times (tau_v+tau_y)(tau_v+tau_e)e^(-2ac) = sign(tau_bar - tau_y). {L}props_check.txt P3: "
            "sign rule holds at 168 (sigma, c, lambda) points, 0 violations. G(0+) closed form matches the independent gap at lambda=1e-7 "
            "(Lab 1 +0.053092, Lab 2 +0.037435).")
row("E4d-math-prop4", "2.4", "project.html:294-296 (Proposition 4)",
    "PASS", f"Re-derived: lam^2 tau_e(tau_e - tau_bar)=tau_bar a^2 sigma^2 gives the interior formula; tau_y(1)=tau_e^2/(tau_e+a^2 sigma^2). "
            f"{L}props_check.txt P4: 56 (sigma, c) cases including both boundary branches, max |closed form - independent root| 2.7e-14. "
            "Informativeness identity tau_bar/(tau_v+tau_bar) = 1 - e^(2ac) tau_v/(tau_v+tau_e) re-derived.")
row("E4d-math-prop5", "2.4", "project.html:299-300 (Proposition 5) and :302",
    "PASS", f"{L}props_check.txt P5: on the interior at sigma 0.5, 0.625, 0.75 (9 costs each) lambda* and informativeness strictly decrease in c. "
            "d lambda*/d sigma = lambda*/sigma follows from lambda* = a sigma k(tau_bar). Page line 302 closed forms (2e^(-4c)-1, 2 sigma "
            "sqrt(.), 1 - e^(4c)/2) re-derived with tau_v = tau_e = 1, a = 2.")
row("E4d-math-assumptions", "2.4", "project.html:257-261 (A1-A5); :603 (exemplar B Model passage)",
    "PASS", "Each proposition's proof was checked against the assumption numbers: A1 (zero mean of m-p, independence), A2 (clearing), A3 (CARA "
            "demand, Lemma 1), A4 (b_s != 0 so that y = p/b_s), A5 (price taking). The listing in exemplar B (project.html:603) is consistent with those uses.")
row("E4d-notation", "2.4 / notation", "project.html math spans; tests/labs/E4/lab-E4-project-3.py:51",
    "PASS", f"{S}notation_and_instances.py ({L}notation_and_instances.txt): registered macros used are \\Corr \\Cov \\E \\Normal \\Var only; no "
            "other macro used is registered-looking; no registered symbol (T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, Q) occurs in any project "
            "math span, and no lab twin has a standalone T. The round-2 'T' collision is fixed.")

# ---- prose, structure, scope
row("E4d-banned-phrases", "1.3-1.4", "course/modules/E/E4/project.html",
    "PASS", f"ledgers/E4/scripts/E4-d-r2/banned_and_process.sh on this pin ({L}banned_and_process.txt): every banned string 0 hits, ellipsis 0.")
row("E4d-process-words", "2.9 / learner text", "course/modules/E/E4/project.html",
    "PASS", f"banned_and_process.sh: builder, verifier, REQUEST, planner, fixer, architect, unit report 0 hits; the only 'round' substrings are "
            "'unrounded' and 'rounded' (project.html:317, 512, 523, 567, 625).")
row("E4d-dag-links", "2.9 / DAG", "course/modules/E/E4/project.html",
    "PASS", f"check_dag.py PASS ({L}check_dag.txt). Links: L06.html#def-noisy-rational-expectations-equilibrium (L06 defines it), "
            "L07.html#def-price-informativeness (L07 defines it), concepts.html#expected-utility (index entry pointing to E3/L01 def). All anchors resolve.")
row("E4d-registry-muth", "2.1", "course/modules/E/E4/project.html reading list (line 680)",
    "PASS", "references/references.json unchanged since 67c47689 (git diff --quiet); verify_refs E4 live 0 problems; the page gives the title only.")
row("E4d-registry-milgrom", "2.1", "course/modules/E/E4/project.html:678, :681",
    "PASS", "Page attributes no statement to either work (line 678). references.json: milgrom1982information title 'Information, trade and common "
            "knowledge' (JET 26(1), 1982). Nothing in the page rests on the paper.")
row("E4d-cites-only-registry", "2.1", "course/modules/E/E4/project.html data-cite (lines 680-681)",
    "PASS", "The only data-cite keys are muth1961rational and milgrom1982information; both are in references.json.")
row("E4d-spec-context-sentences", "2.6 spec", "course/modules/E/E4/project.html:311 (Context)",
    "PASS", "Context paragraph has 4 sentences (counted), within 2-4 (BUILDER_RULES 5.2).")
row("E4d-spec-questions", "2.6 spec", "project.html:314-321 (Required outputs, Constraints, Grading mode)",
    "PASS", "No blocking clarifying question. Non-blocking: where report/ lives relative to solver.py; self_assessment.md is produced by a browser form, "
            "which a local run does not have.")
row("E4d-spec-ladder", "2.6 ladder", "project.html:40-49 (ladder), :51-305 (rungs 1-2), :308 (rung 3), :668-674 (rung 4)",
    "PASS", "Four rungs in order. Rung 1 Lab 1 is solved and annotated (six printed steps with interpretation). Rung 2 Lab 2 has one blank and an "
            "instant check. Rung 4 has two open-ended items. Tier M (curriculum E4): rungs 1-2 are one lab each.")
row("E4d-prose-scope-words", "2.9 / 1.2 scope", "course/modules/E/E4/project.html",
    "PASS", "Scope words: 'on the interior' (lede, Prop 5), 'at every point of the box' (Inputs; box_bounds and the 11x11 grid), 'every printed gap' "
            "(max printed 3.55e-14), 'over the costs c at which the interior holds' (Prop 5, props_check P5). Each is computed or scoped.")
row("E4d-prose-simulated-labs", "2.8 SIMULATED", "project.html Labs 1-3; grader/instance.py",
    "PASS", "Hypothesis or header of Labs 1-3 states SIMULATED (project.html:57, :176, :375); instance.py:1 states SIMULATED; no data-files attribute.")
row("E4d-prose-simulated-exemplars", "2.8 SIMULATED", "project.html:530",
    "PASS", "Line 530: 'Two report excerpts on a SIMULATED instance'.")
row("E4d-hours-project", "2.6 hours", "project.html:33, :343-350 (#hours); index.html:29",
    "PASS", "Components 1+1+5+8+5+5+3 = 28 = data-hours-project (project.html:33; index.html:29). Hub 72 + 28 = 100 = curriculum.json E4 hours 100.")
row("E4d-hours-estimate", "2.6 hours", "project.html #hours table",
    "PASS", "Verifier estimate 22.5 h: rung 1 1; rung 2 0.5; Propositions 1-5 with lemmas 7.5; solver 5; grid 1.5; report 5; self-assessment 2. "
            "That is 19.6% below 28, inside the 30% band. Judgement, not a measurement.")
row("E4d-rubric-observable", "2.6 rubric", "project.html:516-526 (#rubric)",
    "PASS", "All 20 level descriptors name a checkable element; the C3 level-1 example 'prices become more informative' is quoted as a failing example.")
row("E4d-exemplar-A-calibration", "2.6 rubric calibration", "project.html:532-595 (exemplar A, data-scores 2,2,1,2,1)",
    "PASS", "Descriptor scores C1 2, C2 2, C3 1, C4 2, C5 1 (checked against the rubric table, project.html:520-524) match the official scores. "
            "Not blind: the annotations were read before scoring (honest gap).")
row("E4d-exemplar-B-calibration", "2.6 rubric calibration", "project.html:597-659 (exemplar B, data-scores 4,4,4,4,4)",
    "PASS", "Descriptor scores 4 on C1 (A1-A5 each with its results, project.html:603), C2 (method, bracket, tolerance, stop rule, boundary rule, gap "
            "table at :625-637), C3 (signs and points), C4 (display rule), C5 (limits; 'No registry key is attached ... none is claimed', project.html:651, "
            "a paraphrase of the level-4 phrase). Within one level on every criterion. Not blind (honest gap).")
row("E4d-exemplar-annotations-hidden", "2.6 rubric", "course/assets/js/rubric.js:147-150",
    "PASS", "rubric.js is byte-identical since 1c1645f (git diff --quiet): setRevealed() hides .annotation and [data-reveal] until revealed.")

# ---- grader
row("E4d-grader-exceptions", "2.6 item 3", "grader/test_project.py:190-240; grader/reference.py:23-31; project.html:330-331",
    "PASS", "ValueError tests for noise zero, negative, +inf, NaN ('noise volume must be positive') and cost -0.01, -1e-12 ('information cost must be "
            "nonnegative'), as in the table. Cost 0 and noise 1e-12 are accepted. No test demands an exception for a condition the table does not name.")
row("E4d-grader-messages", "2.6 item 4", "grader/test_project.py:48-67 (expect, must_raise) and every expect() message",
    "PASS", "expect() uses pytest.fail(..., pytrace=False); must_raise messages are static text; the messages in the suite name the property and carry "
            "no expected value. A mutant run prints only test names, no values (" + L + "mutate_graders_E4_r3.txt).")
row("E4d-grader-oracle", "2.6 item 3", "grader/test_project.py:9-14, 79-170",
    "PASS", f"The oracle uses regressions, fixed point and a normal-quadrature trapezoid, and does not import reference.py. "
            f"{S}oracle_vs_independent.py ({L}oracle_vs_independent.txt): over 100 instances the oracle gap at the reference fraction differs from the "
            "independent model by 4.4e-16, the oracle root by 2.8e-14, the oracle informativeness by 1.1e-16.")
row("E4d-grader-instances", "2.6 item 2", "grader/instance.py; grader/test_project.py:37-39",
    "PASS", f"seeds 0-49 give 50 distinct (noise, cost) pairs, noise 0.503-0.741 and cost 0.120-0.149, all inside the stated box; deterministic "
            f"({L}notation_and_instances.txt). Interior condition holds at all instances (oracle_vs_independent).")
row("E4d-grader-instance-docstring", "1.4 docstring claims", "grader/instance.py:14-17",
    "PASS", "Docstring says the bound is derived here and the suite does not re-check it; true (no test asserts the box bound). Arithmetic matches box_bounds_r3.txt.")
row("E4d-grader-test-docstring", "1.4 / 2.2 sentence vs assertion", "grader/test_project.py:365 and :369-373",
    "PASS", "Docstring 'does not rise' matches the non-strict assertion lam_dearer <= lam + 1e-9.")
row("E4d-grader-reference-docstring", "1.4 docstring claims", "grader/reference.py:3-6, :35-87",
    "PASS", "Pointer names the section 'The model and its equilibrium' (project.html:249), which exists, and Propositions 1 to 4; the formulas match them (checked against props_check.txt).")
row("E4d-grader-stdlib", "2.6 item 4 / ruling 10 (over-constraint)", "grader/test_project.py:403-412",
    "PASS", f"Round-2 FAIL resolved: the allowlist is replaced by sys.stdlib_module_names (test_project.py:411). The two round-2 stdlib-only solvers "
            f"(ledgers/E4/scripts/E4-d-r2/candidates/stdlib_collections_solver.py, stdlib_decimal_statistics_solver.py) PASS seeds 0-49 "
            f"({L}run_candidates_alts_r3.txt).")
row("E4d-mutants-existing", "2.6 item 3", "ledgers/E4/mutants/mutant_01..mutant_10",
    "PASS", f"mutate_graders E4 --seeds 0-9 and --seeds 0-49: mutants 01-10 KILLED ({L}mutate_graders_E4_seeds0-9.txt, {L}mutate_graders_E4_r3.txt). "
            f"{L}mutant_ast_diffs.txt: each differs from grader/reference.py by one edit (ignoring docstrings).")
row("E4d-mutants-new", "2.6 item 3", "ledgers/E4/mutants/mutant_d11..mutant_d18",
    "PASS", f"d11-d18 KILLED in both seed windows ({L}mutate_graders_E4_r3.txt). One edit each ({L}mutant_ast_diffs.txt).")
row("E4d2-mutants-r2", "2.6 item 3", "ledgers/E4/mutants/mutant_r2_*.py",
    "PASS", f"The four round-2 verifier mutants are KILLED in both seed windows ({L}mutate_graders_E4_r3.txt); one edit each ({L}mutant_ast_diffs.txt).")
row("E4d3-mutants-r3", "2.6 item 3", "ledgers/E4/mutants/mutant_r3_*.py (written by make_r3_mutants.py)",
    "PASS", f"Four new student-error mutants KILLED: boundary rule swapped (test_zero_fraction_is_reported_above_the_cost_threshold), cost discounted "
            "in the gap (test_gap_is_the_oracle_gap_at_the_reported_fraction), price precision linear in lambda (same test), closed-form fraction "
            f"with the cost sign flipped (test_boundary_rule_holds). ({S}make_r3_mutants.py; {L}mutate_graders_E4_r3.txt.)")
row("E4d3-mutant-tolerance-survives", "2.6 item 3; stated stop rule project.html:317",
    "grader/test_project.py:44 (TOL_ROOT); mutant ledgers/E4/mutants/mutant_r3_tolerance_1e-9.py",
    "FAIL", f"mutant_r3_tolerance_1e-9 (bisection stops at a relative bracket width of 1e-9) SURVIVES all 30 tests on seeds 0-9 and 0-49 "
            f"({L}mutate_graders_E4_seeds0-9.txt; {L}mutate_graders_E4_r3.txt). The page states the stop rule (project.html:317: 'stops when the bracket is "
            "narrower than 10^{-12} times its upper end'), so the 1e-9 stop violates a stated constraint, and the suite cannot see it: the root test uses "
            "TOL_ROOT = 1e-6 and the gap test TOL_GAP = 1e-8, while a 1e-9 bracket moves the root by under 1e-9.",
    "Set test_project.py:44 to TOL_ROOT = 1e-10 (keep the comment). Verified on a scratch copy of grader/ (" + L + "tol1e-10_probe.txt): "
    "reference.py and all seven correct alternatives pass seeds 0-49 (ledgers/E4/alternatives/alt_1..alt_5 and ledgers/E4/scripts/E4-d-r3/candidates/"
    "alt_r3_*.py), and the 1e-9 mutant then fails on 37 seeds. Re-run mutate_graders --seeds 0-49 after the change.")
row("E4d-mutants-total", "2.6 item 3", "ledgers/E4/mutants/ (27 mutants)",
    "FAIL", f"tools/mutate_graders.py --unit E4 --seeds 0-9 -> 'mutate_graders E4: FAIL (26/27 killed)', exit 1 ({L}mutate_graders_E4_seeds0-9.txt); "
            "--seeds 0-49 -> same (" + L + "mutate_graders_E4_r3.txt). The only survivor is mutant_r3_tolerance_1e-9.",
    "Apply the fix in E4d3-mutant-tolerance-survives; the count becomes 27/27.")
row("E4d-equivalent", "2.6 item 3 (equivalence proof)", "ledgers/E4/equivalent/literal_price_sign.py; ledgers/E4/equivalent/README.md",
    "PASS", "b_u enters the solver only as b_u*b_u (reference.py:70), so the sign of b_u cannot change any output. "
            f"ledgers/E4/scripts/E4-d-r2/check_equivalent.py on this pin: 3000 pairs, largest difference 0.0, b_u sign in variant True ({L}check_equivalent_r3.txt). "
            "Not counted as a mutant, as the README says.")
row("E4d-alternatives", "2.6 item 3 (ruling 10)", "ledgers/E4/alternatives/alt_1..alt_5.py; ledgers/E4/scripts/E4-d-r3/candidates/alt_r3_*.py",
    "PASS", f"run_candidates.py on seeds 0-49: alt_1 (bisection), alt_2 (Illinois), alt_3 (grid then bisection), alt_4 (damped fixed point), alt_5 "
            f"(precision parameterisation): all PASS ({L}run_candidates_alts_r3.txt). Two new correct alternatives written this round: "
            f"alt_r3_closed_form (Prop 4 closed form, no bisection) and alt_r3_absolute_bracket (absolute width 1e-13): both PASS ({L}run_candidates_r3_alts.txt).")
row("E4d-starter", "2.6 item 1", "grader/starter.py",
    "PASS", f"starter.py raises NotImplementedError; the signature equals project.html:315. run_graders starter check passed ({L}run_graders.txt).")
row("E4d-browser-local-parity", "2.6 item 5", "grader/test_project.py",
    "PASS", f"30 collected locally and 30 pass in Pyodide on the reference ({L}page_smoke_project.txt; {L}workspace_check.txt).")
row("E4d-runtime", "2.5 / 2.6 runtime", "grader/test_project.py",
    "PASS", "Slowest local suite run 0.2 s (run_graders); 0.8 s in Pyodide (page_smoke). Limits 5 s per test, 60 s per suite (BUILDER_RULES 5.3.4).")
row("E4d2-exemplar-B-C1-annotation", "2.6 rubric (annotation accuracy)", "project.html:603 (Model passage) and :607 (annotation)",
    "PASS", "Round-2 FAIL resolved: the Model passage lists A1 to A5 with their numbers and names the results that use them. The stated uses are consistent "
            "with the proofs (see E4d-math-assumptions). Level 4 claim is met.")

# ---- new structural rows
row("E4d3-cara-defined-twice", "1.10 (no concept defined twice)", "course/modules/E/E4/project.html:259 (A3)",
    "FAIL", "project.html:259 wraps 'constant absolute risk aversion (CARA) utility' in <dfn>, which defines it again. The same term is already defined "
            "in course/modules/E/E4/L06.html:67 (Definition 6.2, '<dfn>constant absolute risk aversion (CARA) utility</dfn>'). It has no data-concept, "
            "so check_dag.py does not see it, but BUILDER_RULES 1.10 forbids a second definition. Severity low.",
    "In project.html:259 remove the <dfn> wrapper and keep the words, referring to 'Definition 6.2 of Lesson 6' with a link to L06.html. "
    "(No change to the L06 file is needed from this slice.)")
row("E4d3-anchors-links", "2.9", "course/modules/E/E4/project.html (all href targets)",
    "PASS", "Every local #anchor resolves to an id on the page; every relative file link resolves (grader/test_project.py, instance.py, starter.py; "
            "L06, L07, L09, index.html; ../../../concepts.html, review.html, css and vendor paths). page_smoke: no external requests.")
row("E4d3-no-figures-no-data", "2.8", "course/modules/E/E4/project.html",
    "PASS", "The page has no <svg>, no <img>, and no data-files attribute, so 2.8 figure and dataset rows do not apply. Instances are SIMULATED (instance.py:1).")
row("E4d3-spec-stop-rule-and-constraints", "2.6 spec", "project.html:317 (Constraints)",
    "PASS", "Stop rule (1e-12 relative, 200 halvings) matches reference.py:19-20 and :135; 'standard library only' is enforced by "
            "test_solver_imports_only_the_standard_library. 'with no network' is not tested by any test; no plausible wrong solution needs the network, so "
            "this is recorded as a note, not a finding.")
row("E4d3-atlas-studios-na", "2.6 atlas and studios", "atlas/; project.html",
    "PASS", "E4 has no atlas milestone and is not a studio (grep: no E4 reference under atlas/). Not applicable.")

# ---- mutants from the gate log
mutants = []
for line in (logs / "mutate_graders_E4_r3.txt").read_text(encoding="utf-8").splitlines():
    m = re.match(r"(KILLED|SURVIVED) (\S+)\.py: (.*?) -> (.*)$", line)
    if not m:
        continue
    status, name, desc, killed = m.groups()
    killed_by = None if killed.strip() == "None" else re.sub(r"\s*\(seed \d+\)$", "", killed.strip())
    mutants.append({"id": name, "description": desc, "killed_by": killed_by})

ids = [r["id"] for r in rows]
assert len(ids) == len(set(ids)), "duplicate row id"
counts = {"PASS": 0, "FAIL": 0, "UNVERIFIABLE": 0}
for r in rows:
    counts[r["status"]] += 1
verdict = "PASS" if counts["FAIL"] == 0 and counts["UNVERIFIABLE"] == 0 and all(m["killed_by"] for m in mutants) else "FAIL"
fragment = {
    "unit": "E4",
    "slice": "d",
    "round": 3,
    "round_note": "Round 3 of slice d. Every round-2 row id is kept. Nothing was carried: every row was re-checked on pin 67a2d13.",
    "verifier": "Haiku independent verifier, E4 slice d round 3 (did not build E4)",
    "verdict": verdict,
    "pin": "67a2d13",
    "base": "67c47689 (round-2 pin). Delta: course/modules/E/E4/project.html, grader/instance.py, grader/test_project.py, tests/labs/E4/lab-E4-project-3.py, and ledgers/E4/mutants/mutant_r2_*.py. Lesson pages, cards and lab twins other than project-3 are outside this slice.",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE3-E4-d",
    "scratch": "/tmp/e4d3/ (temporary workspaces only, plus /tmp/e4d3-ws-* and /tmp/e4d3-seed-* removed or left empty; every script that backs a row is under ledgers/E4/scripts/E4-d-r3/)",
    "verified_at": "2026-11-04",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [
        "muth1961rational: record verified (title, Econometrica 29(3), 1961; DOI 10.2307/1909635); live verify_refs E4 0 problems.",
        "milgrom1982information: record title 'Information, trade and common knowledge' (JET 26(1), 1982). The page attributes no statement to it.",
    ],
    "freshness_flags": [],
    "notes": [
        "Scripts: ledgers/E4/scripts/E4-d-r3/ (indep_model.py, props_check.py, oracle_vs_independent.py, cmp_project_labs.py, workspace_check.sh, run_candidates.py, make_r3_mutants.py, make_r3_alternatives.py, notation_and_instances.py, write_fragment_r3.py; logs/ and candidates/).",
        "Independent model: Gaussian conditioning and clearing solved from the definitions; expected utilities by the Gaussian quadratic-form determinant. It reproduces every printed number in Labs 1-3 and Propositions 1-5 numerically.",
        "Calibration is not blind: the exemplars and annotations were read before scoring, so E4d-exemplar-*-calibration are descriptor checks only.",
        "Not checked: the 350-800 word limit of the brief (no report exists in the repository to count); the browser self-assessment form and its JavaScript beyond page_smoke; the Milgrom and Stokey paper (not read; the page attributes nothing to it); the repository-wide strict mypy and the full CI gate (only the E4 files and the four relevant test modules were run).",
        "Stated constraint not enforced by any test: 'with no network' (project.html:317). Not counted as a finding because no plausible wrong solution needs the network.",
        "Lab 3 docstring (tests/labs/E4/lab-E4-project-3.py) says the closed-form fraction belongs to the report's appendix; the appendix is 'Evidence and derivations' (project.html:510), so the reference is accepted as a pointer, not a defect.",
        "Not run: tools/ledger.py merge (the orchestrator merges fragments). The fragment was validated with ledger.validate (see the summary of this round).",
    ],
    "summary": {
        "rows": len(rows),
        "pass": counts["PASS"],
        "fail": counts["FAIL"],
        "unverifiable": counts["UNVERIFIABLE"],
        "mutants_killed": sum(1 for m in mutants if m["killed_by"]),
        "mutants": len(mutants),
    },
}
out = root / "ledgers/E4/E4-d.json"
out.write_text(json.dumps(fragment, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out, counts, "mutants", len(mutants), "killed", fragment["summary"]["mutants_killed"])
