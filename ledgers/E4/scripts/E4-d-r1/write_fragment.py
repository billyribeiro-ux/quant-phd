"""Write the E4 slice-d round-1 verification fragment (ledgers/E4/E4-d.json) from the rows recorded during verification.

Usage: python -I ledgers/E4/scripts/E4-d-r1/write_fragment.py <repo-root>
The script only serialises the verifier's recorded results; every evidence string cites the command, script or
log file that produced it (logs under ledgers/E4/scripts/E4-d-r1/logs/).
"""

import json
import sys
from pathlib import Path

root = Path(sys.argv[1])
P = "course/modules/E/E4/project.html"
G = "course/modules/E/E4/grader"
S = "ledgers/E4/scripts/E4-d-r1"

rows = [
    # ---- commands (gates, targeted) ----
    ("E4d-cmd-check-projects", "2.6", f"{P}; {G}", "PASS",
     "tools/check_projects.py --unit E4 -> 'check_projects E4: PASS', exit 0 (log logs/check_projects_E4.txt)."),
    ("E4d-cmd-check-pages", "2.9", P, "PASS",
     "tools/check_pages.py --unit E4 -> 'check_pages E4: PASS'."),
    ("E4d-cmd-check-dag", "2.9", P, "PASS",
     "tools/check_dag.py --unit E4 -> 'check_dag E4: PASS'."),
    ("E4d-cmd-run-labs", "2.5", "tests/labs/E4/lab-E4-project-1.py, -2.py, -3.py", "PASS",
     "tools/run_labs.py --unit E4 -> 'run_labs E4: PASS (12/12)' (log logs/run_labs_E4.txt); includes the three project labs."),
    ("E4d-cmd-run-graders", "2.6 item 1", f"{G}/reference.py", "PASS",
     "tools/run_graders.py --unit E4 --seeds 0-49 -> 'run_graders E4: PASS (reference 50/50 seeds, slowest 0.2 s)'; "
     "starter failure check raised no problem (logs/run_graders_seeds0-49.txt)."),
    ("E4d-cmd-page-smoke-project", "2.6 item 5; 2.9", P, "PASS",
     "Run alone: tools/page_smoke.py --unit E4 --pages project -> labs 1-3 in Pyodide 0.0 s each; 'in-browser grader: "
     "All 29 tests pass on seed 890196192. (0.8 s)'; 'page_smoke E4: PASS' (logs/page_smoke_project.txt)."),
    ("E4d-cmd-ruff", "2.5", "tests/labs/E4; grader", "PASS",
     "ruff check tests/labs/E4 course/modules/E/E4/grader -> 'All checks passed!'; ruff format --check -> '16 files already formatted' (logs/ruff_E4.txt)."),
    ("E4d-cmd-mypy-workspace", "2.5", "tests/labs/E4 twins; grader instance.py, reference.py, starter.py", "PASS",
     "mypy --no-incremental on the 3 project twins and instance.py, reference.py, starter.py -> 'Success: no issues found in 6 source files'; "
     "mypy --strict --ignore-missing-imports on test_project.py + solver.py (= reference) + instance.py in a scratch copy -> 'Success: no issues found in 3 source files' (logs/mypy_E4.txt, logs/mypy_strict_workspace_and_collect.txt)."),
    ("E4d-cmd-mypy-plan-command", "2.5", f"{G}/test_project.py:26, :27, :174", "FAIL",
     "The plan's command 'mypy tests/labs/E4 course/modules/E/E4/grader' reports 3 errors in test_project.py: import-not-found 'solver' (line 26), "
     "import-not-found 'instance' (line 27), and no-any-return (line 174, caused by the unresolved solver import). The repository gate is unaffected "
     "(pyproject [tool.mypy] files = tools, tests) and run_graders type-checks reference/instance/starter, so this is a planned-command defect, not a gate failure (logs/mypy_E4.txt)."),
    ("E4d-cmd-pytest-relevant", "2.9", "tests/test_page_checks.py, test_labs.py, test_run_labs.py, test_memo_exemplars.py", "PASS",
     "pytest -q on those four modules -> exit 0 (logs/pytest_relevant.txt). No E4-specific pytest module exists; test_memo_exemplars covers S7 only."),
    ("E4d-cmd-verify-refs", "2.1", "references/references.json (E4 keys)", "PASS",
     "tools/verify_refs.py --unit E4 -> 'live re-verification of E4: 3 of 560 entries, 0 problems' (logs/verify_refs_E4.txt)."),
    ("E4d-cmd-collect", "2.6 (test count)", f"{G}/test_project.py", "PASS",
     "pytest --collect-only -q with reference.py as solver.py -> '29 tests collected'; project.html 'Grading mode' states 29 checks."),
    # ---- labs ----
    ("E4d-lab-project-1", "2.5", f"{P} #lab-E4-project-1; tests/labs/E4/lab-E4-project-1.py", "PASS",
     "Page code equals the twin (scripts/E4-d-r1/cmp_project_labs.py); twin run as python -I -W error exits 0 with stdout equal to the expected block. "
     "Printed values re-derived by indep_model.py: gap at 0 +0.053092, gap at 1 -0.080731, root 0.57937525, b_u/b_s -3.45199422, tau_y at root 0.18904110, "
     "informativeness 0.15898618. Hypothesis numbers match. SIMULATED label present."),
    ("E4d-lab-project-2", "2.5", f"{P} #lab-E4-project-2 (class completion); tests/labs/E4/lab-E4-project-2.py", "PASS",
     "Completion check: every non-blank page line equals the twin line (cmp_project_labs.py, 63 lines each); the only blank is the return of indifference_gap. "
     "Twin output equals the expected block. indep_model.py: +0.037435, -0.071386, root 0.57052263, informativeness 0.12466375 (match hypothesis). SIMULATED label present."),
    ("E4d-lab-project-3", "2.5", f"{P} #lab-E4-project-3; tests/labs/E4/lab-E4-project-3.py", "PASS",
     "Page code equals the twin; twin output equals the expected block. indep_model.py section 4 reproduces all nine rows (root 0.5582/0.6978/0.8373 at cost 0.120 etc., informativeness 0.1920/0.1420/0.0889 constant across noise volumes); "
     "max |bisection - closed form| 2.13e-13 (page prints 2.1e-13); box 22x22 interior 484 of 484 (props_grid.py, quadrature). Printed gaps |g| <= 3.56e-14."),
    # ---- numbers in prose ----
    ("E4d-num-lab-hypotheses", "2.2", f"{P} Lab 1-3 hypothesis paragraphs", "PASS",
     "Each number stated before the run (Lab 1 +0.053092/-0.080731/0.57937525/0.18904110/0.15898618; Lab 2 +0.037435/-0.071386/0.57052263/0.12466375; Lab 3 grid values and 484 points) equals the printed output of its twin and the independent recomputation."),
    ("E4d-num-exemplar-table", "2.2", f"{P} exemplar-b Results table", "PASS",
     "The nine-row table (fraction, informativeness, gap) matches the Lab 3 output row by row. Ratios 0.6978/0.5582 = 1.2501 and 0.8373/0.5582 = 1.5001 from displayed digits; exact 1.25 and 1.50 from unrounded values (indep_model.py); the 2-decimal prose is correct."),
    ("E4d-num-box-bounds", "2.2", f"{P} Inputs paragraph; grader/instance.py docstring", "PASS",
     "tau_bar(0.120) = 0.237566 -> '0.2376'; tau_bar(0.150) = 0.097623 -> '0.0976'; min tau_y(1) over the box = 1/(1+4*0.75^2) = 0.307692 -> '0.3077'; the instance docstring's (0, 0.2377] bound holds."),
    # ---- mathematics ----
    ("E4d-math-lemmas", "2.4", f"{P} 'Three lemmas' (Lemma 1-3)", "PASS",
     "Re-derived by hand: Lemma 1 optimal demand x* = (m-p)/(aV) and g(x*) = (m-p)^2/(2aV); Lemma 2 Gaussian integral = (V/(V+S))^(1/2); Lemma 3 law of total variance. "
     "indep_model.py quadrature of the expectations agrees with the page's closed forms to printed digits (Lab 1-3 gaps)."),
    ("E4d-math-prop1", "2.4", f"{P} Proposition 1", "PASS",
     "Algebra re-derived: s-coefficient gives D*b_s = lam*tau_e + (1-lam)*tau_y; u-coefficient gives lam*tau_e*kappa + a = 0, so kappa = -a/(lam*tau_e); tau_y = reciprocal of Var(eps + kappa u). "
     "indep_model.py section 1: regression-based demands at the closed-form price clear the market, residuals <= 4.44e-16 at 18 (lam, sd) points."),
    ("E4d-math-prop2", "2.4", f"{P} Proposition 2", "PASS",
     "Cov(v,p) = b_s/tau_v, Var(p) = b_s^2 (1/tau_v + 1/tau_y), so Corr^2 = tau_y/(tau_v+tau_y); lam = 0 case gives x_U = -tau_v p/a = u and p = -a u/tau_v, uncorrelated with v. Re-derived."),
    ("E4d-math-prop3", "2.4", f"{P} Proposition 3", "PASS",
     "Re-derived: G = Omega^(-1/2)(V_U^(1/2) - e^(ac) V_I^(1/2)), sign G = sign(tau_bar - tau_y) via (tau_v+tau_e)(tau_v+tau_y) e^(-2ac) > 0; G(0+) limit with Omega -> 1/tau_v + a^2 sd^2/tau_v^2 and b_u -> -a/tau_v. "
     "props_grid.py (a): sign rule holds at 125 (sd, c, lam) points; quadrature gap at lam = 1e-9 = +0.053092 for Lab 1, equal to the closed-form G(0+)."),
    ("E4d-math-prop4", "2.4", f"{P} Proposition 4", "PASS",
     "Boundary cases and interior formula re-derived (lam^2 tau_e (tau_e - tau_bar) = tau_bar a^2 sd^2). props_grid.py (b): closed form equals the quadrature bisection root to 1e-9 at 48 (sd, c) points including the c = 0 and c = 0.3 boundary cases."),
    ("E4d-math-prop5", "2.4", f"{P} Proposition 5", "PASS",
     "props_grid.py (c1): lam* strictly decreasing in c across the interior (3 noise volumes x 7 costs); (c2): finite-difference d lam*/d sigma = lam*/sigma at 9 interior points; (d): informativeness identical at the three noise volumes for each cost. "
     "The monotonicity statements are local to the interior, which is the proposition's stated hypothesis (not a defect)."),
    ("E4d-math-assumptions", "2.4", f"{P} Assumptions A1-A5; Lemma 1; Propositions 1-5", "PASS",
     "Each lemma and proposition names the assumptions it uses. A1 normalisation (common prior mean shifts price and conditional means equally, so demands and utilities are unchanged) and A3 positive-factor claim (initial wealth multiplies utilities by exp(-a W0)) re-derived."),
    ("E4d-notation", "2.4 / BUILDER 3.2", f"{P} math spans", "PASS",
     "Macros used: \\E, \\Var, \\Cov, \\Corr, \\Normal, \\mathcal (all registered or local). Not used: \\mathbb{E}, \\Phi, \\gamma, \\mathbb{Q}, R^*, bare T (scripts/E4-d-r1/text_checks.py, logs/text_checks.txt: trap hits empty). Single letters S, D, F, G, I, U, V, X, Z are local (notation.json 'about' lists S as local); sigma and Omega are local."),
    # ---- prose ----
    ("E4d-banned-phrases", "2.9", P, "PASS",
     "grep for TODO, TBD, lorem, for brevity, details omitted, beyond the scope, left as an exercise, you can add more, it is important to note, studies show, experts agree, it is well known, obviously, clearly and any '...' -> no hits."),
    ("E4d-process-words", "2.9", P, "PASS",
     "grep for builder, verifier, round, REQUEST, planner, fixer, architect, build -> only 'unrounded' (false positive); no process words in learner text."),
    ("E4d-dag-links", "2.9 DAG", P, "PASS",
     "check_dag PASS. Links resolve: L06.html#def-noisy-rational-expectations-equilibrium (L06.html:167), L07.html#def-price-informativeness (L07.html:62), concepts.html#expected-utility (concepts.html:447). Out-of-closure names (posterior, noise traders, sign change) are plain prose with no link."),
    ("E4d-registry-muth", "2.1", f"{P} reading list (muth1961rational)", "PASS",
     "Registry record title 'Rational Expectations and the Theory of Price Movements', Econometrica 29(3), 1961; live Crossref record for 10.2307/1909635 agrees (verify_refs: 0 problems). The description 'reading on rational expectations' matches the title."),
    ("E4d-registry-milgrom", "2.1 attribution", f"{P} line 678 (Reading section); milgrom1982information", "UNVERIFIABLE",
     "Registry record: 'Information, trade and common knowledge', Milgrom and Stokey, JET 26(1), 1982, DOI 10.1016/0022-0531(82)90046-1; verify_refs 0 problems. The page calls it the reading 'on ... the no-trade result'. The live Crossref record (plain curl) has title, volume and pages but no abstract, and the article is not readable from a permitted source, so the topic characterisation cannot be confirmed by reading it. Not attempted: any publisher access."),
    ("E4d-cites-only-registry", "2.1", f"{P} lines 680-681", "PASS",
     "The only data-cite keys on the page are muth1961rational and milgrom1982information, both in references/references.json with used_by E4; no free-text bibliographic data; mascolell1995microeconomic is not cited (B3 open)."),
    ("E4d-spec-context-sentences", "2.6 spec (BUILDER 5.2: Context in 2-4 sentences)", f"{P} Rung 3 'Context'", "FAIL",
     "Sentence count of the Context paragraph by scripts/E4-d-r1/text_checks.py (logs/text_checks.txt) = 5: 'A risky asset pays...'; 'Some investors pay a cost c...'; 'A noise-trader supply u moves the price.'; 'The question is how informative...'; 'The fraction solves an indifference condition...'. "
     "Required: 2 to 4 sentences."),
    ("E4d-spec-questions", "2.6 spec", f"{P} Rung 3 'Required outputs'; 'Local' section", "PASS",
     "No blocking clarifying question. Non-blocking question I would have asked: where report/ lives relative to solver.py (the local run copies only test_project.py and instance.py next to solver.py)."),
    ("E4d-spec-ladder", "2.6 ladder", f"{P} ladder and Rungs 1-4", "PASS",
     "Four rungs in order; rung 1 fully solved and annotated (Lab 1, six printed steps); rung 2 completion lab graded by the lab check; rung 3 spec with 29-test autograder and rubric; rung 4 two open-ended extensions; rungs 1-2 at 1 h each."),
    ("E4d-prose-lede-directional", "2.3 / 2.4 (causal and directional claims)", f"{P} line 37 (lede)", "FAIL",
     "The lede says the price 'reveals less about it as the noise grows'. In the page's own equilibrium the informed fraction responds to the noise (lam* proportional to sigma at fixed c, Prop. 5) and the informativeness does not depend on sigma (Prop. 5(d); Lab 3 constant 0.1920/0.1420/0.0889 across noise volumes; props_grid.py (d)). "
     "The claim holds only at a fixed informed fraction, which the model does not assume."),
    ("E4d-prose-scope-words", "2.4 scope", P, "PASS",
     "every/all/any/only/always/exactly/same: 'every instance has one interior root' (box bound, Prop. 4 proof); '484 points' computed; 'the only equilibrium family the page treats' scoped by A4; 'same at every noise volume' scoped to the grid and interior; no unsupported universal."),
    ("E4d-prose-simulated-labs", "2.5 / 2.8", f"{P} Labs 1-3; grader/instance.py", "PASS",
     "Each lab hypothesis or header and instance.py state SIMULATED; Labs 1-2 state their inputs are stated values, not draws; no data-files attribute; no dataset is read."),
    ("E4d-prose-simulated-exemplars", "2.8 / plan 2.2 (SIMULATED on exemplars)", f"{P} exemplars intro (line 530)", "FAIL",
     "The exemplar introduction ('Two report excerpts, at different levels, on the grid point of Lab 3 ...') has no SIMULATED label, although plan 2.2 requires the label on exemplars and plan 5.6 describes them as excerpts on a SIMULATED instance. The numbers come from the SIMULATED Lab 3 grid."),
    # ---- hours ----
    ("E4d-hours-project", "2.9 hours", f"{P} #hours table (lines 336-351); index.html:29", "PASS",
     "Components 1+1+5+8+5+5+3 = 28 = data-hours-project (project.html:33; index.html:29). Hub 72 lesson + 28 project = 100 = curriculum.json E4 hours. Every row has a rationale."),
    ("E4d-hours-estimate", "2.6 hours", f"{P} #hours table", "PASS",
     "Verifier estimate: rung 1 1.5 h; rung 2 1 h; derivation of Props 1-4 7 h; solver 3 h; grid 2 h; report 4 h; self-assessment 2.5 h = 21 h, which is 25% below 28 h (inside the 30% band). Largest differences: solver (declared 8, estimate 3) and derivation (declared 5, estimate 7). Judgement, not measured."),
    # ---- rubric and exemplars ----
    ("E4d-rubric-observable", "2.6 rubric 1", f"{P} #rubric table", "PASS",
     "All 20 level descriptors name a checkable element (for example 'states each assumption with its number', 'names the significant digits', 'states a sign with no grid'). C1 level 1 'in general terms' is tied to 'with no payoff, signal or utility function written down'."),
    ("E4d-exemplar-A-calibration", "2.6 rubric 2", f"{P} exemplar-a (data-scores 2,2,1,2,1)", "PASS",
     "Descriptor-based scores: C1 2, C2 2, C3 1, C4 2, C5 1, matching the annotations within one level. Not a blind score: I had read the annotations and official scoring before scoring."),
    ("E4d-exemplar-B-calibration", "2.6 rubric 2", f"{P} exemplar-b Results passage and C4 annotation (data-scores 4,4,4,4,4)", "FAIL",
     "Exemplar B's C4 is scored 4 with the annotation 'names the significant digits (...) and the rule'. The exemplar text never states a display rule, names significant digits, or says numbers come from unrounded output "
     "(search of the exemplar-b text for decimal/significant/unrounded/round/rule finds only the annotation and verdict). Descriptor-based C4 = 2 ('gives numbers with a fixed number of decimals and no rule'); divergence 2 exceeds one level."),
    ("E4d-exemplar-annotations-hidden", "2.6 rubric (self-assessment)", "course/assets/js/rubric.js:147-150", "PASS",
     "setRevealed() sets hidden on .annotation and [data-reveal] until the official scoring is revealed, as the page text (line 530) says."),
    # ---- grader ----
    ("E4d-grader-exceptions", "2.6 item 7 (grader rule)", f"{G}/test_project.py:185-219", "PASS",
     "ValueError tests only for the two named conditions: noise_sd = 0, -1e-12 (rejected), 1e-12 (accepted), -SD, inf (rejected); info_cost = -0.01, -1e-12 (rejected), 0.0 (accepted). Messages match the table text. Reference passes all 50 seeds."),
    ("E4d-grader-messages", "2.6 item 4", f"{G}/test_project.py:43-62", "PASS",
     "Failure text is static or prefixed with a condition label (f-strings at lines 58, 61, 62 carry only the label); expect() uses pytest.fail(..., pytrace=False); no expected value is printed; --assert=plain."),
    ("E4d-grader-oracle", "2.6 item 3 (oracle independence)", f"{G}/test_project.py:9-14, 66-165", "PASS",
     "Oracle uses regression on moments and quadrature over the normal density; it does not import reference.py. Five alternatives and the equivalent variant pass, so the suite is not over-constrained."),
    ("E4d-grader-instances", "2.6 item 2", f"{G}/instance.py; scripts/E4-d-r1/sample_instances.py", "PASS",
     "Seeds 0-49: deterministic, inside the documented ranges, all interior by independent quadrature; 50 distinct (noise, cost) pairs; informed fractions span 0.3755 to 0.8273 (script output)."),
    ("E4d-grader-instance-docstring", "2.6 (docstring vs code)", f"{G}/instance.py:16-17", "PASS",
     "'The suite re-checks the interior condition on each seed it runs': test_boundary_rule_holds (test_project.py:265-281) requires the solver's branch to match the oracle gap signs on every seed, so an interior instance cannot be answered with a boundary value. Loosely true; noted, not a defect."),
    ("E4d-grader-test-docstring", "2.9 (docstring vs code)", f"{G}/test_project.py:352 (docstring) and :357-360 (assertion)", "FAIL",
     "Docstring says 'Proposition 5: the informed fraction is strictly decreasing in the information cost on the interior'. The assertion is lam_dearer <= lam + 1e-9, which is non-strict. "
     "Fix: say 'non-increasing' in the docstring, or make the assertion strict."),
    ("E4d-grader-reference-docstring", "2.9 (cross-reference)", f"{G}/reference.py:4-5, 34, 46, 58, 73, 85", "FAIL",
     "reference.py says the model's derivation 'is stated on project.html, section Rung 3 Specification, and ... numbered there' and cites 'derivation step 2/3/5/6'. project.html has no derivation steps; the derivation is in 'The model and its equilibrium' (Lemmas 1-3, Propositions 1-5). "
     "Fix: point to Propositions 1 to 4 of the model section and cite the proposition numbers."),
    ("E4d-grader-stdlib", "2.6 spec constraint", f"{G}/reference.py:14-18; test_project.py:390-399", "PASS",
     "Solver imports only math; test_solver_imports_only_the_standard_library passes for the reference and all candidates."),
    # ---- mutants, alternatives, equivalence ----
    ("E4d-mutants-existing", "2.6 item 3", "ledgers/E4/mutants/mutant_01..10", "PASS",
     "tools/mutate_graders.py --unit E4 --seeds 0-49 -> 10 of 10 KILLED (logs/mutate_graders_seeds0-49.txt)."),
    ("E4d-mutants-new", "2.6 item 3 (>= 3 own mutants)", "ledgers/E4/mutants/mutant_d11..d18 (written by scripts/E4-d-r1/make_d_mutants.py)", "PASS",
     "Eight new student-error mutants, each one edit of reference.py, all KILLED: d11 gap sign reversed; d12 informativeness as correlation; d13 informed ignore price noise; d14 negative cost clamped; d15 bisection update inverted; d16 zero-fraction gap reported as 0; d17 bisection tolerance 1e-6; d18 tolerance 1e-4 (both violate the page's stated 1e-12 stop rule)."),
    ("E4d-mutants-total", "2.6 item 3", "ledgers/E4/mutants/", "PASS",
     "tools/mutate_graders.py --unit E4 --seeds 0-49 -> 'mutate_graders E4: PASS (18/18 killed)'."),
    ("E4d-equivalent", "2.6 item 3; ruling 9", "ledgers/E4/equivalent/literal_price_sign.py and README.md", "PASS",
     "Only difference from reference is the sign of b_u; b_u enters solely as b_u*b_u (reference.py:68) and is unpacked as _ in uninformed_term. check_equivalent.py: 3000 random (sd, cost) pairs, largest |difference| over the three outputs 0.0. Equivalent, so not a grader gap. The sign is an open architect item in the README."),
    ("E4d-alternatives", "2.6 item 3; ruling 10", "ledgers/E4/alternatives/alt_1..alt_5.py", "PASS",
     "Five separately written implementations (194 to 220 diff lines from reference.py); each passes the suite on seeds 0-49 (scripts/E4-d-r1/run_candidates.py; logs/alternatives_seeds0-49.txt)."),
    ("E4d-starter", "2.6 autograder", f"{G}/starter.py", "PASS",
     "run_graders.py starter check (seed 0): the starter does not pass the suite, so no problem was reported."),
    ("E4d-browser-local-parity", "2.6 item 5", f"{G}/test_project.py", "PASS",
     "Same suite: 29 tests collected locally; 29 pass in Pyodide on the reference (page_smoke); reference passes locally on seeds 0-49."),
    ("E4d-runtime", "2.6 (suite time)", f"{G}/test_project.py", "PASS",
     "Slowest local suite run 0.2 s (run_graders); 0.8 s in Pyodide (page_smoke); limits 5 s per test and 60 s per suite."),
]

mutants = [
    ("mutant_01_informed_uses_uninformed_utility", "Informed branch uses the uninformed utility.",
     "test_indifference_holds_at_an_interior_fraction[first] (seed 0)"),
    ("mutant_02_cost_in_levels", "Information cost enters in levels, not as exp(a c).",
     "test_gap_is_the_oracle_gap_at_the_reported_fraction[first] (seed 0)"),
    ("mutant_03_sd_as_variance", "Noise volume used as a variance.",
     "test_indifference_holds_at_an_interior_fraction[first] (seed 0)"),
    ("mutant_04_informativeness_is_precision", "Informativeness reported as tau_y, not the squared correlation.",
     "test_informativeness_is_the_squared_correlation[first] (seed 0)"),
    ("mutant_05_no_sign_check_upper_bracket", "No sign-change check: returns the upper bracket when the gap at 0 is nonpositive.",
     "test_zero_fraction_is_reported_above_the_cost_threshold (seed 0)"),
    ("mutant_06_boundary_dropped_half", "Boundary dropped: returns 0.5 instead of the boundary value 0.",
     "test_zero_fraction_is_reported_above_the_cost_threshold (seed 0)"),
    ("mutant_07_uninformed_ignore_price", "Uninformed investors ignore the price.",
     "test_gap_is_the_oracle_gap_at_the_reported_fraction[first] (seed 0)"),
    ("mutant_08_hard_coded_seed0", "Hard-coded answer for the seed-0 instance returned for every input.",
     "test_gap_is_the_oracle_gap_at_the_reported_fraction[second] (seed 0)"),
    ("mutant_09_fixed_20_steps", "Bisection stopped after a fixed 20 steps with no tolerance check.",
     "test_indifference_holds_at_an_interior_fraction[first] (seed 0)"),
    ("mutant_10_price_noise_minus_sign", "Price-noise variance enters the informed conditional variance with a minus sign (raises math domain error on every valid input tested; a weak kill, see notes).",
     "test_info_cost_zero_is_accepted (seed 0)"),
    ("mutant_d11_gap_sign_reversed", "Gap sign reversed: returns exp(a c) F_I minus F_U.",
     "test_gap_is_the_oracle_gap_at_the_reported_fraction[first] (seed 0)"),
    ("mutant_d12_informativeness_is_correlation", "Informativeness reported as the correlation, not its square.",
     "test_informativeness_is_the_squared_correlation[first] (seed 0)"),
    ("mutant_d13_informed_ignores_price_noise", "Informed investors ignore the noise in the price (b_u^2 sd^2 term omitted).",
     "test_indifference_holds_at_an_interior_fraction[first] (seed 0)"),
    ("mutant_d14_negative_cost_clamped", "Negative information cost clamped to zero instead of rejected with ValueError.",
     "test_info_cost_negative_is_rejected (seed 0)"),
    ("mutant_d15_bisection_update_inverted", "Bisection brackets updated on the wrong side.",
     "test_indifference_holds_at_an_interior_fraction[first] (seed 0)"),
    ("mutant_d16_zero_fraction_gap_reported_as_zero", "Gap at a zero fraction reported as 0.0 instead of the Proposition 3 limit.",
     "test_zero_fraction_is_reported_above_the_cost_threshold (seed 0)"),
    ("mutant_d17_tolerance_1e-6", "Bisection stops at relative width 1e-6 instead of the stated 1e-12.",
     "test_indifference_holds_at_an_interior_fraction[first] (seed 0)"),
    ("mutant_d18_tolerance_1e-4", "Bisection stops at relative width 1e-4 instead of the stated 1e-12.",
     "test_indifference_holds_at_an_interior_fraction[first] (seed 0)"),
]

FIXES = {
    "E4d-cmd-mypy-plan-command": "Type-check test_project.py in its workspace layout (solver.py and instance.py beside it, as tools/run_graders.py does), where it reports no issues; or add '# type: ignore[import-not-found]' to lines 26-27 and an explicit cast at line 174.",
    "E4d-registry-milgrom": "Describe milgrom1982information only by its registry title ('Information, trade and common knowledge', Milgrom and Stokey, 1982) and say the page attributes no statement to it, or cite a readable source for the no-trade characterisation.",
    "E4d-spec-context-sentences": "Cut the Context paragraph to four sentences: join 'A noise-trader supply u moves the price.' to the cost sentence and join the last two sentences.",
    "E4d-prose-lede-directional": "Rewrite the lede sentence so it does not claim the price reveals less as noise grows: state that at a fixed informed fraction more noise reveals less, and that here the fraction responds so that Proposition 5 gives an informativeness independent of the noise volume.",
    "E4d-prose-simulated-exemplars": "Add the word SIMULATED to the exemplar introduction (project.html line 530), for example 'Two report excerpts on a SIMULATED instance, at different levels, ...'.",
    "E4d-exemplar-B-calibration": "Add the display rule to exemplar B's Results passage (four decimals for the fraction and the informativeness, three significant digits for the gap, each from unrounded solver output and rounded once for display), so the level-4 C4 annotation is supported; otherwise re-score C4 at 2 and correct the annotation and data-scores.",
    "E4d-grader-test-docstring": "Change the docstring of test_fraction_falls_with_the_cost to 'non-increasing in the information cost' (the assertion is non-strict), or make the assertion strict and keep the docstring.",
    "E4d-grader-reference-docstring": "In reference.py replace the pointer to 'Rung 3 Specification' and the 'derivation step N' references with the proposition numbers of project.html's model section (Propositions 1 to 4).",
}

fragment = {
    "unit": "E4",
    "slice": "d",
    "round": 1,
    "verifier": "Haiku independent verifier, E4 slice d round 1 (did not build E4)",
    "pin": "1c1645f",
    "base": "1c1645f (first verification of this slice; no previous fragment)",
    "checkout": str(root),
    "scratch": "/tmp/e4d-scratch-collect (collect-only and mypy workspace); /tmp/e4d_*.txt (raw logs, copied into the logs folder)",
    "verified_at": "2026-11-03",
    "verdict": "FAIL",
    "rows": [
        {"id": i, "check": c, "location": loc, "status": st, "evidence": ev, **({"fix": FIXES[i]} if st != "PASS" else {})}
        for (i, c, loc, st, ev) in rows
    ],
    "mutants": [{"id": n, "description": d, "killed_by": k} for (n, d, k) in mutants],
    "registry_flags": [
        "muth1961rational: record verified (title, Econometrica 29(3), 1961); live Crossref agrees.",
        "milgrom1982information: record verified (title, JET 26(1), 1982); Crossref has no abstract, so the page's 'no-trade result' characterisation is unread (row E4d-registry-milgrom).",
    ],
    "freshness_flags": [],
    "notes": [
        "Scripts: ledgers/E4/scripts/E4-d-r1/ (cmp_project_labs.py, indep_model.py, props_grid.py, sample_instances.py, run_candidates.py, check_equivalent.py, make_d_mutants.py, write_fragment.py); logs in logs/.",
        "Mutants: ten existing (mutant_01..10) and eight written by the verifier (mutant_d11..d18), all under ledgers/E4/mutants/. mutate_graders E4 --seeds 0-49: 18/18 killed.",
        "The plan's mutant 10 (price noise sign) is output-equivalent (equivalent/literal_price_sign.py). The existing mutant_10 is a different variance-sign error that raises math domain error on every valid input, so it is killed only by a crash. Not a FAIL; a non-crashing sign error would test the grader harder.",
        "Exemplar calibration is not blind: the annotations and official scores were read before scoring.",
        "Hours are a verifier estimate (21 h vs declared 28 h). The HOURS ruling makes them design targets; the arithmetic is the checked item.",
        "Could not check: the text of the Milgrom and Stokey article (no abstract on Crossref; no bypass attempted); browser behaviour of the self-assessment form beyond reading rubric.js; the 350-800 word limit of the brief (no report exists to count).",
        "Not run: tools/ledger.py merge (the orchestrator merges fragments). Only tools/ledger.validate was applied to this fragment.",
        "Carried-over checks from earlier campaigns applied: unrounded numbers, lab text vs output, attribution, scope words, causal claims, notation, DAG, process words, banned phrases, mutants, alternatives, equivalence.",
    ],
    "summary": {
        "rows": len(rows),
        "pass": sum(1 for r in rows if r[3] == "PASS"),
        "fail": sum(1 for r in rows if r[3] == "FAIL"),
        "unverifiable": sum(1 for r in rows if r[3] == "UNVERIFIABLE"),
        "mutants_killed": len(mutants),
        "mutants": len(mutants),
    },
}

out = root / "ledgers/E4/E4-d.json"
out.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out, "rows", len(rows), "mutants", len(mutants))
