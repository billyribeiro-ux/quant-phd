"""Serialise the E4 slice-d round-2 verification fragment (ledgers/E4/E4-d.json) from the recorded results.

Usage: python -I ledgers/E4/scripts/E4-d-r2/write_fragment_r2.py <repo-root>
Every evidence string cites the command, script or log that produced it (logs under ledgers/E4/scripts/E4-d-r2/logs/).
Mutant rows are parsed from the mutate_graders log, not typed by hand.
"""

import json
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
P = "course/modules/E/E4/project.html"
G = "course/modules/E/E4/grader"
S = "ledgers/E4/scripts/E4-d-r2"
L = f"{S}/logs"

rows: list[dict[str, str]] = []


def row(rid: str, check: str, location: str, status: str, evidence: str, fix: str = "") -> None:
    item = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        item["fix"] = fix
    rows.append(item)


# ---- commands ----
row("E4d-cmd-check-projects", "2.6", f"{P}; {G}", "PASS",
    "tools/check_projects.py --unit E4 -> 'check_projects E4: PASS', exit 0 (logs/check_projects_E4.txt).")
row("E4d-cmd-check-pages", "2.9", P, "PASS",
    "tools/check_pages.py --unit E4 -> 'check_pages E4: PASS', exit 0 (logs/check_pages_E4.txt).")
row("E4d-cmd-check-dag", "2.9", P, "PASS",
    "tools/check_dag.py --unit E4 -> 'check_dag E4: PASS', exit 0 (logs/check_dag_E4.txt).")
row("E4d-cmd-run-labs", "2.5", "tests/labs/E4/lab-E4-project-1.py, -2.py, -3.py", "PASS",
    "tools/run_labs.py --unit E4 -> 'run_labs E4: PASS (12/12)', exit 0 (logs/run_labs_E4.txt).")
row("E4d-cmd-run-graders", "2.6 item 1", f"{G}/reference.py", "PASS",
    "tools/run_graders.py --unit E4 --seeds 0-49 -> 'run_graders E4: PASS (reference 50/50 seeds, slowest 0.2 s)', "
    "exit 0; starter check raised no problem (logs/run_graders_E4.txt).")
row("E4d-cmd-page-smoke-project", "2.6 item 5; 2.9", P, "PASS",
    "Run alone: tools/page_smoke.py --unit E4 --pages project -> labs 1-3 run in Pyodide; 'in-browser grader: All 30 tests "
    "pass on seed 374642645'; 'page_smoke E4: PASS', exit 0 (logs/page_smoke_project.txt).")
row("E4d-cmd-ruff", "gate", "tests/labs/E4; grader", "PASS",
    "ruff check tests/labs/E4 course/modules/E/E4/grader -> 'All checks passed!'; ruff format --check -> '16 files already "
    "formatted'; repo-wide ruff check . -> 'All checks passed!' (logs/ruff_check.txt, logs/ruff_format.txt).")
row("E4d-cmd-mypy-workspace", "2.6 / BUILDER_RULES 6.2 (strict)", f"{G}/test_project.py:27, :28, :175", "FAIL",
    "Strict mypy in the local-run layout (test_project.py, solver.py = reference.py, instance.py in one directory): "
    "scripts/E4-d-r2/workspace_mypy.sh -> 'test_project.py:27: error: Unused \"type: ignore\" comment', ':28' the same, "
    "':175: error: Redundant cast' -> 'Found 3 errors in 1 file' (logs/workspace_mypy.txt). The round-1 type-ignore comments "
    "only silence the import-not-found error in the repo layout.",
    "Remove the two '# type: ignore[import-not-found]' comments and the cast(...) at line 175. Load the solver and the "
    "instance with importlib.import_module into names annotated Any, and assign the solver result to a typed local "
    "(out: dict[str, float] = sol.solve_model(...)) before returning it, so test_project.py is strict-clean both beside "
    "solver.py and in the repo layout.")
row("E4d-cmd-mypy-plan-command", "gate", "tests/labs/E4; grader", "PASS",
    "mypy --no-incremental tests/labs/E4 course/modules/E/E4/grader -> 'Success: no issues found in 16 source files', exit 0 "
    "(logs/mypy_plan_command.txt). Repo-path mypy on the 3 twins and grader files also passes (logs/mypy_repo_paths.txt). "
    "The pass depends on the ignore comments that row E4d-cmd-mypy-workspace shows are unused in the local layout.")
row("E4d-cmd-pytest-relevant", "gate", "tests/test_page_checks.py, test_labs.py, test_run_labs.py, test_memo_exemplars.py",
    "PASS", "pytest -q on the four modules -> 'exit 0' (logs/pytest_relevant.txt). No E4-specific pytest module exists.")
row("E4d-cmd-verify-refs", "2.1", "references/references.json (E4 keys)", "PASS",
    "tools/verify_refs.py --unit E4 (live) -> 'live re-verification of E4: 3 of 560 entries, 0 problems' (logs/verify_refs_E4.txt).")
row("E4d-cmd-collect", "2.6 grader", f"{G}/test_project.py", "PASS",
    "pytest --collect-only -q on test_project.py with reference.py as solver.py -> '30 tests collected' (logs/collect_only.txt); "
    "project.html:319 states 30 checks, so the count matches.")

# ---- labs ----
row("E4d-lab-project-1", "2.5", "course/modules/E/E4/project.html #lab-E4-project-1; tests/labs/E4/lab-E4-project-1.py", "PASS",
    "scripts/E4-d-r2/cmp_project_labs.py: page code == twin True; twin run as python -I -W error exits 0; stdout == expected block "
    "True (logs/cmp_project_labs.txt). Printed values re-derived by scripts/E4-d-r2/indep_model.py (logs/indep_model.txt): gap at 0 "
    "+0.053092, gap at 1 -0.080731, root 0.57937525, b_u/b_s -3.45199422, tau_y at root 0.18904110, informativeness 0.15898618.")
row("E4d-lab-project-2", "2.5 completion", "course/modules/E/E4/project.html #lab-E4-project-2 (line 217); tests/labs/E4/lab-E4-project-2.py",
    "PASS", "cmp_project_labs.py: 63 page lines and 63 twin lines, non-blank differences [] (logs/cmp_project_labs.txt); the only "
    "blank is 'return ___' at project.html:217; twin stdout == expected block; indep_model.py §3 reproduces +0.037435, -0.071386, "
    "root 0.57052263, informativeness 0.12466375.")
row("E4d-lab-project-3", "2.5", "course/modules/E/E4/project.html #lab-E4-project-3; tests/labs/E4/lab-E4-project-3.py", "PASS",
    "cmp_project_labs.py: page code == twin True (but the twin's docstring carries the notation error in row E4d-notation); twin "
    "stdout == expected block True. indep_model.py §4 reproduces all nine rows to 4 decimals; max |bisection - closed form| "
    "2.13e-13 (prints 2.1e-13); props_grid.py (b): 48 points, no mismatch.")

# ---- numbers ----
row("E4d-num-lab-hypotheses", "2.2 (a)", f"{P} Labs 1-3 hypothesis paragraphs (lines 57, 176, 375)", "PASS",
    "Each stated number equals the printed output of its twin (logs/cmp_project_labs.txt) and the independent recomputation "
    "(logs/indep_model.txt §2-§4): Lab 1 +0.053092, -0.080731, 0.57937525, 0.18904110, 0.15898618; Lab 2 +0.037435, -0.071386, "
    "0.57052263, 0.12466375; Lab 3 nine grid values and 484 points.")
row("E4d-num-exemplar-table", "2.2 (c)", f"{P} Results table (lines 629-637) and Results passage (line 625)", "PASS",
    "The nine rows equal the Lab 3 printed output (lab output in project.html:487-498). Displayed digits: 0.6978/0.5582 = 1.2501 and "
    "0.8373/0.5582 = 1.5000; the unrounded ratios are 1.25 and 1.50 (Proposition 5, indep_model.txt §4). The gap column is the "
    "lab's printed value; the independent quadrature gap differs only at the 1e-14 noise level, and the page claims only "
    "|gap| < 4e-14 (max printed 3.55e-14).")
row("E4d-num-box-bounds", "2.2 (c)", f"{P} Inputs paragraph (line 313); {G}/instance.py:14-17", "PASS",
    "scripts/E4-d-r2/box_bounds.py (logs/box_bounds.txt): tau_bar(0.120) = 0.237567 -> 0.2376; tau_bar(0.150) = 0.097623 -> 0.0976; "
    "min tau_y(1) = 0.307692 -> 0.3077; worst-corner tau_bar < tau_y(1) True.")

# ---- mathematics ----
row("E4d-math-lemmas", "2.4", f"{P} Lemmas 1-3 (lines 266-273)", "PASS",
    "Re-derived by hand: Lemma 1 maximiser x* = (m-p)/(aV) and g(x*) = (m-p)^2/(2aV), so -a g(x*) = -(m-p)^2/(2V); Lemma 2 integral "
    "(2 pi S)^(-1/2) sqrt(2 pi SV/(S+V)) = (V/(V+S))^(1/2); Lemma 3 law of total variance. indep_model.py clearing residual 4.4e-16 "
    "and quadrature gaps agree with the page's closed forms (logs/indep_model.txt).")
row("E4d-math-prop1", "2.4", f"{P} Proposition 1 (lines 276-282)", "PASS",
    "Re-derived: the s-coefficient gives D b_s = lam tau_e + (1-lam) tau_y; the u-coefficient gives -lam tau_e kappa = a, so kappa = -a/(lam tau_e); "
    "tau_y = 1/Var(eps + kappa u) = lam^2 tau_e^2/(lam^2 tau_e + a^2 sd^2). Clearing residual over 18 (lam, sd) points: 4.441e-16 "
    "(logs/indep_model.txt §1). Existence and uniqueness are proved within the A4 family by step (4).")
row("E4d-math-prop2", "2.4", f"{P} Proposition 2 (line 284)", "PASS",
    "Re-derived: Cov(v,p) = b_s/tau_v; Var(p) = b_s^2 (1/tau_v + 1/tau_y); Corr^2 = tau_y/(tau_v+tau_y). lam = 0 case: p = -a u/tau_v, "
    "independent of v (Corr 0).")
row("E4d-math-prop3", "2.4", f"{P} Proposition 3 (lines 287-291)", "PASS",
    "Re-derived: sign G = sign(V_U - e^{2ac} V_I) = sign(tau_bar - tau_y) after multiplying by (tau_v+tau_y)(tau_v+tau_e) e^{-2ac}; "
    "G(0+) limits of Omega, V_U and b_u re-derived. props_grid.py (a): sign rule holds at 125 (sd, c, lam) points, no violation "
    "(logs/props_grid.txt).")
row("E4d-math-prop4", "2.4", f"{P} Proposition 4 (lines 294-297)", "PASS",
    "Re-derived: lam^2 tau_e (tau_e - tau_bar) = tau_bar a^2 sd^2 and the interior formula; props_grid.py (b): closed form equals the "
    "quadrature bisection root within 1e-9 at 48 (sd, c) points, boundary cases included (logs/props_grid.txt).")
row("E4d-math-prop5", "2.4", f"{P} Proposition 5 (line 299)", "PASS",
    "props_grid.py (c1): lam* strictly decreasing in c on the interior, no violation; (c2): finite-difference d lam*/d sigma equals "
    "lam*/sigma at 9 interior points; (d): informativeness identical at the three noise volumes per cost (logs/props_grid.txt). "
    "The restated sentence 'over the costs c at which the interior holds' matches (c1).")
row("E4d-math-assumptions", "2.4", f"{P} A1-A5 (lines 257-261); Lemma 1; Propositions 1-5", "PASS",
    "A1 prior-mean normalisation re-derived: demands depend on E[v|F] - p, and shifting v, s and p by m leaves that difference and "
    "the clearing condition unchanged. A3 positive factor exp(-a W0) re-derived. Proposition 1 uses A1-A5, Proposition 3 uses A1 "
    "for the zero mean of m_I - p and of m_U - p; the cited assumption numbers match the uses.")
row("E4d-notation", "2.4 / notation", f"{P}:426; tests/labs/E4/lab-E4-project-3.py:51 (learner-visible docstring)", "FAIL",
    "The Lab 3 docstring writes 'tau_y(lam) = T = (tau_v + tau_e) exp(-2 a c) - tau_v'. notation/notation.json registers the symbol "
    "T as 'number of return observations (periods) in a sample' (module S1; symbols list). The same quantity is written tau-bar in "
    "the prose (project.html:253, 296, 302). Other math-span symbols are local per notation.json 'about' (S, m, sigma) or not "
    "registered; no \\Phi, \\gamma, \\mathbb, R^* hits (scripts/E4-d-r2/logs/text_checks.txt).",
    "In tests/labs/E4/lab-E4-project-3.py line 51 replace 'T' with '\\bar\\tau' in prose form, e.g. 'tau_bar' (the docstring "
    "is the twin's code, so edit the twin, then re-embed with tools/embed_labs.py project.html --refresh lab-E4-project-3 and rerun "
    "run_labs). Do not reuse T.")
row("E4d-banned-phrases", "1.3-1.4", P, "PASS",
    "scripts/E4-d-r2/banned_and_process.sh (logs/banned_and_process.txt): every banned string 0 hits, ellipsis 0 hits.")
row("E4d-process-words", "2.9 / learner text", P, "PASS",
    "banned_and_process.sh: builder, verifier, REQUEST, planner, fixer, architect, unit report 0 hits; 'round' appears only in "
    "'unrounded' and 'rounding' (lines 317, 512, 523, 567, 625).")
row("E4d-dag-links", "2.9 / DAG", P, "PASS",
    "check_dag.py --unit E4 PASS (logs/check_dag_E4.txt). Links: L06.html#def-noisy-rational-expectations-equilibrium (project.html:250), "
    "L07.html#def-price-informativeness (250), concepts.html#expected-utility (263). Concepts are defined once.")

# ---- registry ----
row("E4d-registry-muth", "2.1", f"{P} reading list (line 680)", "PASS",
    "references/references.json:17659-17664: key muth1961rational, title 'Rational Expectations and the Theory of Price Movements', "
    "DOI 10.2307/1909635; verify_refs live 0 problems (logs/verify_refs_E4.txt). The page gives the title only and attributes "
    "no statement.")
row("E4d-registry-milgrom", "2.1", f"{P} Reading (line 678, 681)", "PASS",
    "The round-1 characterisation ('no-trade result') is gone: line 678 says each work is given by its registry title, that the "
    "page attributes no statement to either work and does not characterise either one. references.json:17291-17296: title "
    "'Information, trade and common knowledge' (Milgrom, Stokey, JET 26(1), 1982). No claim rests on the paper.")
row("E4d-cites-only-registry", "2.1", f"{P} lines 680-681", "PASS",
    "The only data-cite keys on the page are muth1961rational and milgrom1982information (grep 'data-cite'); both are in references.json. "
    "mascolell1995microeconomic is not cited.")

# ---- structure and prose ----
row("E4d-spec-context-sentences", "2.6 spec", f"{P} Rung 3 Context (line 311)", "PASS",
    "scripts/E4-d-r2/text_checks.py (logs/text_checks.txt): the Context paragraph has 4 sentences, within the 2-4 rule.")
row("E4d-spec-questions", "2.6 spec", f"{P} Rung 3 Required outputs (315); Local (362-367)", "PASS",
    "No blocking clarifying question found. Non-blocking question I would have asked: where report/ lives relative to solver.py "
    "(the local run copies only test_project.py and instance.py next to solver.py).")
row("E4d-spec-ladder", "2.6 ladder", f"{P} ladder (40-49), Rungs 1-4", "PASS",
    "Four rungs in order; rung 1 is Lab 1 with six printed steps; rung 2 is Lab 2 with one blank; rung 3 is the spec with the 30-test "
    "suite and rubric; rung 4 has two open-ended extensions (stretch).")
row("E4d-prose-lede-directional", "2.9 / 1.2 (scope)", f"{P} lede (line 37)", "FAIL",
    "The lede says 'in the model here the informed fraction itself rises with the noise'. That is false outside the interior. "
    "scripts/E4-d-r2/lede_fraction_check.py (logs/lede_fraction_check.txt): at cost 0.00 and 0.05 the informed fraction is 1.0 at "
    "every noise volume 0.5, 0.6, 0.75, 1.0, 2.0 (Proposition 4's upper case). Proposition 5 gives the rise only on the interior "
    "(0 < tau_bar < tau_y(1)). The first clause, with the informed fraction held fixed, is correct (Proposition 1 formula for tau_y "
    "decreases in sd).",
    "Qualify the sentence in the lede: 'on the interior, where the fraction is strictly between 0 and 1, the informed fraction rises "
    "with the noise, and there the informativeness does not depend on the noise volume' (or drop the clause).")
row("E4d-prose-scope-words", "2.9 / 1.2 (scope)", P, "PASS",
    "Scope words in the changed text: 'on the interior' (lede, Prop 5), 'over the costs c at which the interior holds' (Prop 5), "
    "'every point of the box' (Inputs, backed by box_bounds.py and logs/sample check and the 484-point count), 'every printed gap' "
    "(max 3.55e-14 printed). Each is computed or scoped.")
row("E4d-prose-simulated-labs", "2.8 SIMULATED", f"{P} Labs 1-3; {G}/instance.py", "PASS",
    "Labs 1-3 hypothesis or header state SIMULATED (lines 57, 176, 375); instance.py:1 states SIMULATED; no data-files attribute; "
    "no dataset read.")
row("E4d-prose-simulated-exemplars", "2.8 SIMULATED", f"{P} Exemplars intro (line 530)", "PASS",
    "Line 530 now reads 'Two report excerpts on a SIMULATED instance'.")
row("E4d-hours-project", "2.6 hours", f"{P} #hours table (lines 340-350); index.html:29", "PASS",
    "Components 1+1+5+8+5+5+3 = 28 = data-hours-project (project.html:33); hub data-hours-lessons 72 + data-hours-project 28 = 100 = "
    "curriculum.json E4 hours (line 7461). Every row has a rationale.")
row("E4d-hours-estimate", "2.6 hours", f"{P} #hours table", "PASS",
    "Verifier estimate: rung 1 1.5 h; rung 2 1 h; derivation of Propositions 1-5 7 h; solver 4 h; grid 2 h; report 4 h; "
    "self-assessment 2.5 h = 22 h, which is 21% below 28 h (inside the 30% band). Judgement, not measurement.")
row("E4d-rubric-observable", "2.6 rubric", f"{P} #rubric table (lines 516-526)", "PASS",
    "All 20 level descriptors name a checkable element; C3 level 1 'prices become more informative' is named as a failing example.")
row("E4d-exemplar-A-calibration", "2.6 rubric calibration", f"{P} exemplar-a (data-scores 2,2,1,2,1, lines 532-595)", "PASS",
    "Descriptor-based scores: C1 2, C2 2, C3 1, C4 2, C5 1, matching the annotations. Not blind: I had read the annotations and the "
    "official scoring before scoring, so this is a descriptor check, not a blind calibration.")
row("E4d-exemplar-B-calibration", "2.6 rubric calibration", f"{P} exemplar-b (data-scores 4,4,4,4,4, lines 597-659)", "PASS",
    "C4 is now supported: the Results passage states the display rule (line 625, 'Display rule: four decimals ... three significant "
    "digits ... unrounded solver output'). Descriptor scores: C2 4, C3 4, C4 4, C5 4, C1 3 (within one level of the official 4; the "
    "annotation problem is row E4d2-exemplar-B-C1-annotation). Not blind.")
row("E4d-exemplar-annotations-hidden", "2.6 rubric", "course/assets/js/rubric.js:147-150", "PASS",
    "setRevealed() sets hidden on .annotation and [data-reveal] until revealed; rubric.js is unchanged since the round-1 pin.")

# ---- grader ----
row("E4d-grader-exceptions", "2.6 item 3 / exception table", f"{G}/test_project.py:186-220; reference.py:23-31", "PASS",
    "ValueError tests for noise zero, negative, infinite, NaN (added in round 2, message 'noise volume must be positive'), and cost "
    "-0.01 and -1e-12; the cost 0.0 and noise 1e-12 cases are accepted. The table names only these two conditions.")
row("E4d-grader-messages", "2.6 item 4", f"{G}/test_project.py:44-63", "PASS",
    "expect() uses pytest.fail(..., pytrace=False); must_raise messages are labelled static text; no expected value appears in any message.")
row("E4d-grader-oracle", "2.6 item 3", f"{G}/test_project.py:9-14, 66-166", "PASS",
    "The oracle uses regressions and quadrature and does not import reference.py. Five alternatives and the reference pass seeds 0-49 "
    "(logs/alternatives_seeds0-49.txt), so the oracle does not over-constrain them.")
row("E4d-grader-instances", "2.6 item 2", f"{G}/instance.py; scripts/E4-d-r2/sample_instances.py", "PASS",
    "logs/sample_instances.txt: 50 distinct (noise, cost) pairs; all seeds 0-49 in range and interior; informed fractions 0.3755 to "
    "0.8273; deterministic across two calls per seed.")
row("E4d-grader-instance-docstring", "1.4 (docstring claims)", f"{G}/instance.py:14-17", "PASS",
    "The round-1 claim 'the suite re-checks the interior condition' is removed; the docstring now says the bound is derived and the "
    "suite does not re-check it (true: no test asserts the box bound).")
row("E4d-grader-test-docstring", "1.4 / 2.2 (sentence vs assertion)", f"{G}/test_project.py:361, 367", "PASS",
    "The docstring now says 'does not rise', matching the non-strict assertion lam_dearer <= lam + 1e-9.")
row("E4d-grader-reference-docstring", "1.4 (docstring claims)", f"{G}/reference.py:3-6, 35-87", "PASS",
    "The pointer now names the section 'The model and its equilibrium' and Propositions 1 to 4; no 'derivation step' or 'Rung 3' "
    "pointer remains in reference.py (grep).")
row("E4d-grader-stdlib", "2.6 item 4 / ruling 10 (over-constraint)", f"{G}/test_project.py:41, 399-408", "FAIL",
    "test_project.py:41 allows only eight modules ('__future__', 'math', 'fractions', 'random', 'itertools', 'functools', 'typing', "
    "'dataclasses'), and test_solver_imports_only_the_standard_library rejects any other import. The page says 'Standard library "
    "only' (project.html:317). Two correct solvers that use only the standard library fail that test with 'the solver may use only "
    "the standard library: remove the import of a package outside it': scripts/E4-d-r2/candidates/stdlib_collections_solver.py "
    "and stdlib_decimal_statistics_solver.py (logs/stdlib_allowlist_seed0.txt; a pytest run printed 'FAILED ... "
    "test_solver_imports_only_the_standard_library', '1 failed, 29 passed').",
    "Reject only names outside the standard library: replace the ALLOWED_IMPORTS set with "
    "'extra = sorted(n for n in names if n not in sys.stdlib_module_names)' (import sys; Python 3.10+ provides the set), or keep the "
    "allowlist and say on the page which modules are allowed.")
row("E4d-mutants-existing", "2.6 item 3", "ledgers/E4/mutants/mutant_01..10", "PASS",
    "tools/mutate_graders.py --unit E4 --seeds 0-49: mutants 01-10 KILLED (logs/mutate_graders_E4_r2.txt). mutant_10 is killed "
    "only by a math-domain crash (test_info_cost_zero_is_accepted); it is a real fault, not an equivalent.")
row("E4d-mutants-new", "2.6 item 3", "ledgers/E4/mutants/mutant_d11..d18", "PASS",
    "Round-1 mutants d11-d18 re-run: all KILLED (logs/mutate_graders_E4_r2.txt).")
row("E4d2-mutants-r2", "2.6 item 3", "ledgers/E4/mutants/mutant_r2_*.py (scripts/E4-d-r2/make_r2_mutants.py)", "PASS",
    "Four new student-error mutants written by the verifier: grid scan without refinement (killed by the indifference test), "
    "fraction rounded to four decimals (killed by the gap oracle test), cost must be positive (killed by test_info_cost_zero_is_accepted), "
    "informativeness as posterior variance (killed by test_informativeness_is_the_squared_correlation). All KILLED.")
row("E4d-mutants-total", "2.6 item 3", "ledgers/E4/mutants/", "PASS",
    "tools/mutate_graders.py --unit E4 --seeds 0-49 -> 'mutate_graders E4: PASS (22/22 killed)', exit 0.")
row("E4d-equivalent", "2.6 item 3 (equivalence proof)", "ledgers/E4/equivalent/literal_price_sign.py; README.md", "PASS",
    "Algebraic argument: b_u enters the solver only as b_u*b_u (reference.py:70), so the sign of b_u cannot change any output for any "
    "input. scripts/E4-d-r2/check_equivalent.py: 3000 pairs, largest difference 0.0 (logs/check_equivalent.txt). The architect's "
    "open decision on Proposition 1's sign (README) is recorded, not a grader gap.")
row("E4d-alternatives", "2.6 item 3 (ruling 10)", "ledgers/E4/alternatives/alt_1..alt_5.py", "PASS",
    "run_candidates.py on seeds 0-49: alt_1 (bisection), alt_2 (Illinois), alt_3 (grid then bisection), alt_4 (damped fixed point), "
    "alt_5 (precision parameterisation): each PASS, failing=0 (logs/alternatives_seeds0-49.txt). Reference also PASS.")
row("E4d-starter", "2.6 item 1", f"{G}/starter.py", "PASS",
    "starter.py raises NotImplementedError; run_graders.py starter check reported no problem (logs/run_graders_E4.txt).")
row("E4d-browser-local-parity", "2.6 item 5", f"{G}/test_project.py", "PASS",
    "Same suite: 30 collected locally and 30 pass in Pyodide on the reference (logs/page_smoke_project.txt; logs/collect_only.txt).")
row("E4d-runtime", "2.5 / 2.6 runtime", f"{G}/test_project.py", "PASS",
    "Slowest local suite run 0.2 s (run_graders); 0.8 s in Pyodide (page_smoke); limits 5 s per test and 60 s per suite.")

# ---- round-2 additions ----
row("E4d2-exemplar-B-C1-annotation", "2.6 rubric (annotation accuracy)", f"{P} exemplar-b Model passage (line 603) and annotation (line 607)",
    "FAIL",
    "The annotation says 'Meets C1 level 4: lists each assumption with its number and names the results that use it'. The Model "
    "passage lists Assumptions 1 to 4 only (A5 is defined at project.html:261 and is not in the excerpt), and names the results for Assumptions 1 and 4 only "
    "(Assumptions 2 and 3 name no result). Level 4 is therefore not met as written. The official C1 score 4 is within one level "
    "of the descriptor reading (3), so calibration itself passes.",
    "Add Assumption 5 (types and price taking) to the Model passage with the results that use it (Propositions 1 and 3), and name "
    "the results for Assumptions 2 and 3; or change the C1 annotation to level 3 and the score (data-scores line 597 and the "
    "verdict on line 599) to 3.")

# ---- mutants (parsed from the log) ----
mutants = []
for line in (root / L / "mutate_graders_E4_r2.txt").read_text(encoding="utf-8").splitlines():
    m = re.match(r"KILLED (\S+)\.py: (.*?) -> (\S+) \(seed", line)
    if m:
        mutants.append({"id": m.group(1), "description": m.group(2), "killed_by": m.group(3)})
assert len(mutants) == 22, len(mutants)

fails = [r for r in rows if r["status"] != "PASS"]
verdict = "PASS" if not fails else "FAIL"
fragment = {
    "unit": "E4",
    "slice": "d",
    "round": 2,
    "round_note": "Round 2 of slice d. The round-1 fragment was not trusted; every round-1 row id is kept and re-verified on pin 67c47689.",
    "verifier": "Haiku independent verifier, E4 slice d round 2 (did not build E4)",
    "pin": "67c47689",
    "base": "1c1645f (round 1). Round-2 delta: course/modules/E/E4/project.html, grader/instance.py, grader/reference.py, grader/test_project.py and the E4 grader ledgers; lab twins and shared assets unchanged.",
    "checkout": str(root),
    "scratch": "/tmp/e4d2-* (temporary workspaces only; every script that backs a row is under ledgers/E4/scripts/E4-d-r2/)",
    "verified_at": "2026-11-04",
    "verdict": verdict,
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [
        "muth1961rational: record verified (title, Econometrica 29(3), 1961; DOI 10.2307/1909635); live Crossref agrees.",
        "milgrom1982information: record title 'Information, trade and common knowledge' (JET 26(1), 1982). The page now gives only the title and attributes no statement (row E4d-registry-milgrom)."
    ],
    "freshness_flags": [],
    "notes": [
        "Scripts: ledgers/E4/scripts/E4-d-r2/ (cmp_project_labs.py, indep_model.py, props_grid.py, sample_instances.py, run_candidates.py, check_equivalent.py, text_checks.py, lede_fraction_check.py, box_bounds.py, banned_and_process.sh, workspace_mypy.sh, make_r2_mutants.py, make_stdlib_candidates.py, candidates/, write_fragment_r2.py); logs in logs/.",
        "Calibration is not blind: the annotations and official scores were read before scoring (descriptor check only).",
        "Mutant_10 (existing) is killed only by a math-domain crash, not by a numeric difference; that is a fault, not a grader gap.",
        "The plan's mutant 10 ('price sign error changes informativeness') is output-equivalent by the algebra in ledgers/E4/equivalent/README.md; the plan sentence is wrong, the page makes no such claim.",
        "Hours are a judgement (22 h estimate vs 28 h declared); HOURS ruling makes them design targets, and the arithmetic is checked.",
        "Could not check: the Milgrom and Stokey text (no abstract on Crossref; not read, not claimed); the 350-800 word limit of the brief (no report exists to count); the browser self-assessment form beyond rubric.js; the blind calibration (the annotations were read first).",
        "Not run: tools/ledger.py merge (the orchestrator merges fragments); tools/ledger.validate applied to this fragment.",
    ],
    "summary": {
        "rows": len(rows),
        "pass": sum(1 for r in rows if r["status"] == "PASS"),
        "fail": len(fails),
        "unverifiable": 0,
        "mutants_killed": len(mutants),
        "mutants": len(mutants),
    },
}
out = root / "ledgers/E4/E4-d.json"
out.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out, "rows", len(rows), "fail", len(fails), "mutants", len(mutants), "verdict", verdict)
