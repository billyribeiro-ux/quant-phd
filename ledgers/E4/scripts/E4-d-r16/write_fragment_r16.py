"""Build ledgers/E4/E4-d.json (round 16, verifier) from the round-15 row ids plus round-16 rows.

Every round-15 row id is kept. Statuses and evidence are round-16 results (commands and outputs under
ledgers/E4/scripts/E4-d-r16/). The only carried rows are those whose cited files are byte-identical since the
round-15 pin d1e65a0; they carry the prefix required by VERIFIER_RULES. Usage: python -I write_fragment_r16.py <root>
"""
import json
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
OUT = "ledgers/E4/scripts/E4-d-r16/out/"
PREV = json.loads(Path("/Users/billyribeiro/.fanout/frags/E-E4-d.round15.json").read_text(encoding="utf-8"))
prev_rows = {r["id"]: r for r in PREV["rows"]}

P = "PASS"
F = "FAIL"
U = "UNVERIFIABLE"
CAL_NOTE = (
    "blind scoring of this round was contaminated: the first grep of project.html printed the data-scores and the "
    "official verdict lines of both exemplars before the stripping script ran (see notes). Blind stripped-prose scores "
    "(ledgers/E4/scripts/E4-d-r16/exemplar_prose_stripped.txt, rubric table project.html:523-527): A = C1 2, C2 2, C3 1, "
    "C4 2, C5 2; B = C1 4, C2 4, C3 4, C4 4, C5 4. Against the official scores A 2,2,1,2,1 and B 4,4,4,4,4 every "
    "criterion is within one level, but the blind property is not established, so no PASS is claimed. Fresh verifier needed."
)
ROWS = {
    "E4d-cmd-check-projects": (P, OUT + "check_projects.txt: 'check_projects E4: PASS', exit 0 (tools/check_projects.py --unit E4)."),
    "E4d-cmd-check-pages": (P, OUT + "check_pages.txt: 'check_pages E4: PASS', exit 0 (tools/check_pages.py --unit E4; includes the banned-string scan)."),
    "E4d-cmd-check-dag": (P, OUT + "check_dag.txt: 'check_dag E4: PASS', exit 0."),
    "E4d-cmd-run-labs": (P, OUT + "run_labs.txt: 'run_labs E4: PASS (12/12)', exit 0 (tools/run_labs.py --unit E4)."),
    "E4d-cmd-run-graders": (P, OUT + "run_graders_0_49.txt: 'run_graders E4: PASS (reference 50/50 seeds, slowest 0.2 s)', exit 0 (tools/run_graders.py --unit E4 --seeds 0-49)."),
    "E4d-cmd-page-smoke-project": (P, OUT + "page_smoke_project.txt: 'page_smoke E4: PASS', exit 0 (tools/page_smoke.py --unit E4 --pages modules/E/E4/project.html)."),
    "E4d-cmd-ruff": (P, OUT + "ruff_check.txt 'All checks passed!' and ruff_format.txt '16 files already formatted' (ruff check and format --check on course/modules/E/E4 and tests/labs/E4)."),
    "E4d-cmd-mypy-workspace": (P, OUT + "mypy_e4.txt: 'Success: no issues found in 16 source files', exit 0 (mypy --no-incremental tests/labs/E4 course/modules/E/E4/grader)."),
    "E4d-cmd-mypy-plan-command": (P, OUT + "mypy_e4.txt (same run; the plan command over tests/labs/E4 and the grader), exit 0."),
    "E4d-cmd-pytest-relevant": (P, OUT + "pytest_relevant_r16.txt: pytest -q on tests/test_memo_exemplars.py, test_page_checks.py, test_labs.py, test_run_labs.py, exit 0, all dots."),
    "E4d-cmd-verify-refs": (P, OUT + "verify_refs_offline.txt: 'offline integrity: 560 entries, 0 problems'; " + OUT + "verify_refs_E4_live.txt: 'live re-verification of E4: 3 of 560 entries, 0 problems' (keys muth1961rational, milgrom1982information among them)."),
    "E4d-cmd-collect": (P, OUT + "cand/collect_reference.txt: '48 tests collected', exit 0 (run_candidate_r16.py --collect on grader/reference.py; plain collect needs solver.py)."),
    "E4d-lab-project-1": (P, OUT + "run_labs.txt 12/12; " + OUT + "twin_project_1.out and .err (0 bytes) from run_twins_r16.sh: python -I -W error, exit 0. Printed lines equal the page expected block (Lab 1 hypothesis numbers 0.053092, -0.080731, 0.57937525, -3.45199422, 0.18904110, 0.15898618)."),
    "E4d-lab-project-2": (P, OUT + "run_labs.txt 12/12; twin_project_2.out and .err (0 bytes): exit 0; the four printed lines equal the Lab 2 expected block (+0.037435, -0.071386, 0.57052263, 0.12466375)."),
    "E4d-lab-project-3": (P, OUT + "run_labs.txt 12/12; twin_project_3.out: nine grid rows plus the 484/484 line and the 2.1e-13 difference line equal the Lab 3 expected block; exit 0, stderr 0 bytes."),
    "E4d-num-lab-hypotheses": (P, "project.html:57 (Lab 1 hypothesis), :176 (Lab 2 hypothesis), :376 (Lab 3 hypothesis): every number (Lab 1 gap +0.053092/-0.080731, root 0.57937525, ratio -3.45199422, tau_bar 0.18904110, informativeness 0.15898618; Lab 2 0.037435/-0.071386, 0.57052263, 0.12466375; Lab 3 0.5582/0.6978/0.8373, 0.1920/0.1420/0.0889, 1e-13 bound, 1e-12 bound, 484) equals " + OUT + "twin_project_{1,2,3}.out."),
    "E4d-num-exemplar-table": (P, "project.html:634-642 (Exemplar B table): all nine rows equal " + OUT + "twin_project_3.out rows (fractions, informativeness, gaps)."),
    "E4d-num-box-bounds": (P, "project.html:314 and grader/instance.py:14-17 (tau_bar 0.097623 to 0.237567; tau_y(1) >= 0.30769): recomputed in " + OUT + "recheck_numbers_r16.txt: tau_bar(0.150)=0.0976232722, tau_bar(0.120)=0.2375667836, 1/(1+4*0.75^2)=0.3076923077."),
    "E4d-prose-lede-directional": (P, "lede (project.html:37): with lambda fixed, tau_y = lambda^2 tau_e^2/(lambda^2 tau_e + a^2 sigma^2) falls in sigma (so informativeness falls); on the interior lambda* = a sigma k(tau_bar) rises with sigma (Prop 5); informativeness independent of sigma. Derived from Props 1, 2, 4, 5 (re-derived this round); no numeric claim."),
    "E4d-math-lemmas": (P, "project.html Lemmas 1-3 (lines ~265-270) re-derived by hand this round: Lemma 1 completes the square, g(xhat)=(m-p)^2/(2aV) and -a g = -(m-p)^2/(2V); Lemma 2 Gaussian integral; Lemma 3 law of total variance. Numeric support: the suite's oracles (test_project.py oracle_expect_exp, oracle_regressions, oracle_price) agree with reference.py on 50 seeds (" + OUT + "cand/reference_0_49.txt)."),
    "E4d-math-prop1": (P, "project.html Proposition 1 (line ~277-283): step (3) algebra re-derived (s-coefficient gives b_s; u-coefficient gives -lambda tau_e kappa = a); tau_y formula equals 1/(1/tau_e + kappa^2 sigma^2). Numeric: Lab 1 step 5 prints b_u/b_s = -3.45199422 = -a/(lambda* tau_e) and output equals twin_project_1.out."),
    "E4d-math-prop2": (P, "project.html Proposition 2: Corr^2 = (b_s^2/tau_v^2)/((1/tau_v) b_s^2 (1/tau_v+1/tau_y)) = tau_y/(tau_v+tau_y) re-derived; lambda=0 case re-derived. Numeric: test_informativeness_is_the_squared_correlation (oracle_informativeness) passes on both instances and 50 seeds (" + OUT + "cand/reference_0_49.txt)."),
    "E4d-math-prop3": (P, "project.html Proposition 3: sign rule and G(0+) formula re-derived (multiply by (tau_v+tau_y)(tau_v+tau_e)e^{-2ac}; Omega = V + S via Lemma 3; limit b_u -> -a/tau_v). Numeric: gap_at_zero agrees with the suite's oracle to 1.110e-16 (" + OUT + "recheck_numbers_r16.txt); interior gap oracle tests pass."),
    "E4d-math-prop4": (P, "project.html Proposition 4: closed form lambda* = a sigma sqrt(tau_bar/(tau_e(tau_e - tau_bar))) re-derived; informativeness identity tau_bar/(tau_v+tau_bar) = 1 - tau_v e^{2ac}/(tau_v+tau_e). Numeric: Lab 3 closed-form column equals bisection to 4 decimals, largest difference 2.1e-13 (twin_project_3.out)."),
    "E4d-math-prop5": (P, "project.html Proposition 5: d lambda*/d sigma = lambda*/sigma; monotone in c since tau_bar decreases in c and k(t) increases on (0, tau_e). Numeric: Lab 3 grid (fraction proportional to sigma: 0.5582, 0.6978, 0.8373 at cost 0.120); test_fraction_is_proportional_to_the_noise_volume and test_fraction_falls_with_the_cost pass (" + OUT + "cand/reference_0_49.txt)."),
    "E4d-math-assumptions": (P, "project.html A1-A6 (lines ~257-266) read in full: each assumption is used by a named result (A1 by Props 1-3, A3 by Lemma 1, A4 by Prop 1, A5 by Props 1-3, A6 by Props 4-5), and the page says where A6 is assumed, not proved."),
    "E4d-notation": (P, "notation/notation.json (8 registered symbols: T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, Q; macros \\E \\Var \\Corr \\Cov \\Normal among 26 registered) against the page: no registered symbol is used with another meaning; every macro the page uses is registered or standard LaTeX (command count in this round's grep)."),
    "E4d-banned-phrases": (P, OUT + "check_pages.txt PASS (banned-string scan of BUILDER_RULES 1.3-1.4 over visible prose); no process words found by grep (see E4d-process-words)."),
    "E4d-process-words": (P, "grep -i over project.html for verif, round, fixer, ruling, architect, builder, TODO, placeholder, previous: only 'Solver and verification' (rubric criterion C2 name, project.html:526). No process word in learner text; grader/*.py and tests/labs/E4/*.py also clean (docstrings read)."),
    "E4d-dag-links": (P, OUT + "check_dag.txt PASS; " + OUT + "scope_and_anchors_r16.txt: 18/18 in-page hrefs resolve; cross-page anchors resolve (concepts.html#expected-utility, L06.html#def-noisy-rational-expectations-equilibrium, L07.html#def-price-informativeness, index.html#placement)."),
    "E4d-registry-muth": (P, "references/references.json key muth1961rational: Crossref-verified, Econometrica 29(3), year 1961, title 'Rational Expectations and the Theory of Price Movements'; plain curl https://api.crossref.org/works/10.2307/1909635 returns the same container, volume, issue and page 315. verify_refs live E4: 0 problems (" + OUT + "verify_refs_E4_live.txt)."),
    "E4d-registry-milgrom": (P, "references/references.json key milgrom1982information: DOI 10.1016/0022-0531(82)90046-1, JET 26(1) 17-27, 1982, Milgrom & Stokey; verify_refs live E4: 0 problems (" + OUT + "verify_refs_E4_live.txt). Reading list states no attribution to either work."),
    "E4d-cites-only-registry": (P, "project.html:685-686 (data-cite items in the Reading list) are the only citations on the page; both keys exist in references/references.json with used_by E4."),
    "E4d-spec-context-sentences": (P, "project.html spec 'Context' dd (line ~312) read: states the payoff, the signal, the noise trader supply, the cost and the question; no numeric or empirical claim."),
    "E4d-spec-questions": (P, "project.html spec (Context, Inputs, Required outputs, Constraints, Grading mode, Reading list) read in full. Questions a competent student would have had to ask: (i) the grade scale T/A/B/C/D/X and what each grade means is not defined on this page (needed only for an empirical claim, which the page says it does not make; BLUEPRINT section 3 defines it); (ii) none that blocks the build. No row fails on this."),
    "E4d-spec-ladder": (F, "project.html:42 says 'Rungs 1 and 2 are at full length.' BUILDER_RULES 5.1 says 'From tier M upward, rungs 1-2 are kept to the minimum', and VERIFIER_RULES 2.6 says 'From tier M upward, rungs 1-2 are minimal'. E4 is tier M (hub 'Tier M'; curriculum/02-economics-finance-core.yaml tier M). The tier-M sister modules say 'Rungs 1 and 2 are short.' (M6, SC1 project.html). Rung 1 and rung 2 (project.html lines ~51-244) and rung 3 and rung 4 otherwise present and correct (check_projects PASS; ladder order verified)."),
    "E4d-prose-scope-words": (P, OUT + "scope_and_anchors_r16.txt lists all 115 scope-word hits in the prose and each was read. The one new universal claim in this round's delta, project.html:318 'Any reported fraction within 1e-10 times the oracle's root is accepted, whatever point of the final bracket the solver reports', is backed by the tolerance tests (test_project.py:540-587 use 1e-10 times the root) and by the three equivalence variants that report other bracket points and pass 50/50 (" + OUT + "cand/equiv_*.txt; " + OUT + "equiv_check_r16.txt, max relative deviation 4.97e-13)."),
    "E4d-prose-simulated-labs": (P, "SIMULATED marks at project.html Lab 1 hypothesis (line ~57), Lab 2 hypothesis (~176), Inputs (~314) and Lab 3 hypothesis (~376); grader/instance.py docstring says SIMULATED."),
    "E4d-prose-simulated-exemplars": (P, "project.html exemplar intro (line 535) states 'Two report excerpts on a SIMULATED instance' and that the numbers are the printed Lab 3 numbers (0.5567, 0.1420, +3.55e-14), equal to " + OUT + "twin_project_3.out."),
    "E4d-hours-project": (P, "project.html:33 data-hours-project 28; index.html:29 data-hours-lessons 72 and data-hours-project 28; 72 + 28 = 100 = curriculum hours (curriculum/02-economics-finance-core.yaml, E4 hours 100)."),
    "E4d-hours-estimate": (P, "Verifier estimate per component: rung 1 about 1 h; rung 2 about 1 h; model derivation 4-6 h; solver and local tests 5-7 h; grid 2-3 h; write-up 4-6 h; self-assessment 2-3 h; midpoint about 23 h (range 19-27 h). Declared 28 h is 18% above the midpoint, inside the 30% bar."),
    "E4d-rubric-observable": (F, "project.html rubric table (lines 517-529) read. C1-C4 descriptors are observable. C5 level 1 'Notes caveats without naming a limit.' is a vague descriptor: the word 'caveat' has no observable test, and the page's own annotation (project.html:595) and this verifier's blind reading of the same sentence (project.html:591, 'The results depend on the model, which is a simplified description of a market.') give C5 = 1 and C5 = 2 respectively. Fix: state level 1 as 'Names no limit of the model; hedges only with general remarks such as results may vary' and level 2 as 'Names one or two specific assumptions of the model (for example the exponential utility or the exogenous noise supply) as limits'."),
    "E4d-exemplar-A-calibration": (U, "project.html:537-600 (Exemplar A). " + CAL_NOTE),
    "E4d-exemplar-B-calibration": (U, "project.html:602-661 (Exemplar B). " + CAL_NOTE),
    "E4d-exemplar-annotations-hidden": (P, "project.html:539 and :604 mark the verdict paragraphs data-reveal; the annotations are aside.annotation; course/assets/js/rubric.js:147-151 setRevealed hides '.annotation, [data-reveal]' until the form reveals them."),
    "E4d-grader-exceptions": (P, "grader/test_project.py must_raise tests (lines ~191-240 and ~242-285 after the one-line docstring shift) and reference.py:26-34 raise ValueError with 'noise volume must be positive' and 'information cost must be nonnegative'; suite passes 50/50 (" + OUT + "cand/reference_0_49.txt)."),
    "E4d-grader-messages": (P, "every expect() and pytest.fail message read (test_project.py:60-68 and all test bodies): none prints an expected value; hints name the property (for example the boundary rule at test ~line 248, the bisection at ~345)."),
    "E4d-grader-oracle": (P, "test_project.py:79-170 read: oracle_price is a fixed-point iteration (lines ~118-131), oracle_regressions gives the moments (~90-115), oracle_expect_exp is a trapezoid quadrature (~85-87); they do not import reference.py and agree with it at lambda=0 to 1.110e-16 (" + OUT + "recheck_numbers_r16.txt)."),
    "E4d-grader-instances": (P, "grader/instance.py:32-36 deterministic from the seed; " + OUT + "instances_sample_r16.txt: 20 seeds valid, all inside [0.5,0.75] x [0.12,0.15], 20 distinct informed fractions."),
    "E4d-grader-instance-docstring": (P, "grader/instance.py:1-21 read: box bounds match lines 28-29; tau_bar bounds 0.097623 and 0.237567 and tau_y(1) >= 0.30769 recomputed (recheck_numbers_r16.txt)."),
    "E4d-grader-test-docstring": (P, "every test docstring read (test_project.py 191-588). Numbers in docstrings recomputed in " + OUT + "recheck_numbers_r16.txt: gap at 1e-12 differs from the limit by 1.02e-13 to 3.54e-13 (docstring: 1e-13 to 4e-13); oracle agrees with the limit to 1.110e-16 (docstring: at most 1.1e-16); corner tau_bar 1.012161e-2 and root 2.022385e-51; 200-halving width 6.2e-61 > 1e-10 times the root."),
    "E4d-grader-reference-docstring": (P, "grader/reference.py:21-23 read: 2^-240 = 5.6598e-73 (docstring 5.7e-73); 240 halvings reach the relative tolerance for roots above 5.66e-61 (docstring 'about 6e-61'); 200 halvings give width 6.22e-61 > 1e-10 root at 2.02e-51 (" + OUT + "recheck_numbers_r16.txt)."),
    "E4d-grader-stdlib": (P, "reference.py imports only math (line 16); test_solver_imports_only_the_standard_library passes for reference and for alt_1..alt_8 (" + OUT + "cand/*.txt)."),
    "E4d-runtime": (P, OUT + "run_graders_0_49.txt: slowest seed 0.2 s; page_smoke in-browser grader line for the project page PASS (" + OUT + "page_smoke_project.txt). Under the 10 s limit."),
    "E4d-browser-local-parity": (P, OUT + "page_smoke_project.txt PASS (Pyodide suite) and " + OUT + "cand/reference_0_49.txt (local pytest with --assert=plain -W error, 50/50 seeds)."),
    "E4d2-exemplar-B-C1-annotation": (P, "project.html:604-608 Exemplar B Model passage lists Assumptions 1-6 with numbers and the propositions that use them; the C1 level 4 annotation is consistent with the passage (checked this round; the official C1 4 is within one level of the blind 4)."),
    "E4d3-cara-defined-twice": (P, "Carried from round 15 (course/modules/E/E4/L06.html lines 57 and 66 byte-identical since the previous pin; the round-16 diff hunks of L06.html are at lines 86, 552 and 722): project.html A3 (line ~259) refers to CARA as Definition 6.2 of Lesson 6 and does not define it again."),
    "E4d3-anchors-links": (P, OUT + "scope_and_anchors_r16.txt: 18 in-page href targets all exist; 4 cross-page anchors exist."),
    "E4d3-no-figures-no-data": (P, "grep for <img, <svg, <canvas and data-file in project.html returns 0 matches; the page states 'No dataset' (Inputs, line ~314)."),
    "E4d3-spec-stop-rule-and-constraints": (P, "project.html Constraints (line 318) states the tolerance 1e-12 times the upper end and at most 240 halvings; reference.py:21-23 and :138 match; test_project.py tolerance tests (lines ~540-587) pass for reference and alternatives."),
    "E4d3-atlas-studios-na": (P, "curriculum/02-economics-finance-core.yaml E4 entry has no atlas key; E4 is a module (rung 3 plus the full ladder), not a studio; no atlas file is referenced by the E4 pages."),
    "E4d-mutants-existing": (P, OUT + "mutate_graders_E4_0_9_final_r16.txt: 'mutate_graders E4: PASS (130/130 killed)' (126 existing mutants plus the 4 new round-16 mutants), seeds 0-9."),
    "E4d-mutants-new": (P, OUT + "mutate_graders_E4_0_9_final_r16.txt: mutant_r7_02_rejects_noise_above_one.py and mutant_r7_03_rejects_cost_above_one.py KILLED."),
    "E4d2-mutants-r2": (P, OUT + "mutate_graders_E4_0_9_final_r16.txt: all mutant_r2_*.py KILLED."),
    "E4d3-mutants-r3": (P, OUT + "mutate_graders_E4_0_9_final_r16.txt: all mutant_r3_*.py KILLED."),
    "E4d3-mutant-tolerance-survives": (P, OUT + "mutate_graders_E4_0_9_final_r16.txt: mutant_r3_tolerance_1e-9.py KILLED (the page states 1e-12)."),
    "E4d-mutants-total": (P, OUT + "mutate_graders_E4_0_9_final_r16.txt: 130 mutants, 130 killed on seeds 0-9. The mutant_ast_profile.txt shows every file differs from reference.py in one code unit (or the intended multi-unit change)."),
    "E4d-equivalent": (P, "ledgers/E4/equivalent/: literal_price_sign.py (4000 random cases, zero bitwise mismatches, " + OUT + "equiv_check_r16.txt; proof in README section 'Proof that the three outputs do not change'); mutant_r6_08, mutant_r7_01, mutant_v9_02 (ruling 17, numeric check in equiv_check_r16.txt, max relative deviation 4.97e-13 against 1e-10). All four pass 50/50 (" + OUT + "cand/equiv_*.txt)."),
    "E4d-alternatives": (P, OUT + "cand/alt_1.txt .. alt_8.txt: each '50/50 seeds pass' on seeds 0-49 (run_candidate_r16.py)."),
    "E4d-starter": (P, "Carried from round 15 (course/modules/E/E4/grader/starter.py byte-identical since the previous pin; git diff d1e65a0..56cc575 empty for this file): signature solve_model(noise_sd: float, info_cost: float) -> dict[str, float] matches project.html Required outputs."),
    "E4d4-alt4-wrong-on-small-noise": (P, OUT + "cand/alt_4.txt: '50/50 seeds pass' (the secant alternative passes the small-noise and corner tests)."),
    "E4d4-alt1-docstring": (P, "ledgers/E4/alternatives/alt_1.py:1-3 docstring 'bisection with a relative bracket width of 1e-12, or at most 240 halvings' matches code line 80."),
    "E4d4-equivalent-price-slope": (P, OUT + "equiv_check_r16.txt: literal_price_sign.py gives bitwise identical solve_model outputs on 4000 cases (max abs diff 0.0)."),
    "E4d4-calibration-blind": (U, "project.html:537-600 (Exemplar A). " + CAL_NOTE),
    "E4d4-proposed-test-validated": (P, "test_project.py small-noise and corner tests (lines ~540-587) pass for reference.py and alt_1..alt_8 (" + OUT + "cand/*.txt)."),
    "E4d4-mutants-killed-r4": (P, OUT + "mutate_graders_E4_0_9_final_r16.txt: all mutant_r4*.py KILLED."),
    "E4d4-exemplar-B-results-numbers": (P, "project.html:634-642 table and Results passage equal " + OUT + "twin_project_3.out (see E4d-num-exemplar-table)."),
    "E4d5-mutant-bracket-floor": (P, OUT + "mutate_graders_E4_0_9_final_r16.txt: mutant_r5_bracket_floor_1e-12.py KILLED."),
    "E4d5-mutant-sixty-halvings": (P, OUT + "mutate_graders_E4_0_9_final_r16.txt: mutant_r5_sixty_halvings_no_tolerance.py KILLED."),
    "E4d5-mutant-uninformed-precision": (P, OUT + "mutate_graders_E4_0_9_final_r16.txt: mutant_r5_uninformed_posterior_precision_informed.py KILLED."),
    "E4d5-calibration-B-blind": (U, "project.html:602-661 (Exemplar B). " + CAL_NOTE),
    "E4d6-mutant-06": (P, OUT + "mutate_graders_E4_0_9_final_r16.txt: mutant_r6_06_cost_scales_whole_gap.py KILLED."),
    "E4d6-mutant-07": (P, OUT + "mutate_graders_E4_0_9_final_r16.txt: mutant_r6_07_unit_informativeness_discounted_by_cost.py KILLED."),
    "E4d6-mutants-new-killed": (P, OUT + "mutate_graders_E4_0_9_final_r16.txt: every mutant_r6_0*.py that remains in mutants/ KILLED (r6_08 is in equivalent/)."),
    "E4d6-spec-variants-08-09": (P, "ruling 17 (plans/FINAL-ARCHITECT-RULINGS.md lines 39-42) makes mutant_r6_08_reports_lower_end.py equivalent within the 1e-12 stop tolerance; it lives in ledgers/E4/equivalent/ with the README proof; numeric check " + OUT + "equiv_check_r16.txt; passes 50/50. mutant_r6_09_always_200_halvings.py is in mutants/ and KILLED (test_corner_root_meets_the_relative_accuracy_at_the_domain_edge)."),
    "E4d6-stop-rule-measured": (P, "Carried from round 15 (course/modules/E/E4/grader/reference.py byte-identical since the previous pin): reference.py:22-23 and the while condition (line ~138) use 1e-12 times the upper end and 240 halvings, as Constraints states."),
    "E4d6-rung1-why": (P, "project.html Lab 1 interpretation (line ~171) explains each step in the order the twin prints it (" + OUT + "twin_project_1.out)."),
    "E4d7-midpoint-untested": (P, "project.html:318 now says 'Any reported fraction within 1e-10 times the oracle's root is accepted, whatever point of the final bracket the solver reports', so the midpoint report is not a student error (ruling 17). The suite's tolerance tests accept any point within 1e-10 times the root; mutant_r7_01 is in equivalent/ and passes 50/50 (" + OUT + "cand/equiv_mutant_r7_01_reports_bracket_lower_end.txt)."),
    "E4d7-cost-above-one-rejected": (P, "test_project.py test_info_cost_above_one_is_accepted and test_info_cost_far_above_one_is_accepted (lines ~242-280) pass for reference and alt_1..alt_8 (" + OUT + "cand/*.txt); the page names no upper bound on the cost (exception table, project.html:326)."),
    "E4d7-noise-above-one-rejected": (P, "test_project.py test_noise_volume_far_above_one_is_accepted passes; mutant_r4f_rejects_noise_above_one.py KILLED (" + OUT + "mutate_graders_E4_0_9_final_r16.txt)."),
    "E4d7-lab1-bracket-width": (P, "Lab 1 prints 'after 60 halvings the bracket width is 1.110e-16' (twin_project_1.out) and the interpretation gives 2^-53 = 1.110e-16 (recheck: 1.1102e-16); the claim that the width stops at the 53rd halving is the floating-point argument of the page, consistent with the printed value."),
    "E4d7-lab2-blank": (P, "project.html Lab 2 (lines ~175-245): one blank, the return line 'return ___' in indifference_gap; the completed twin tests/labs/E4/lab-E4-project-2.py exit 0 (ruling 11 convention)."),
    "E4d7-instance-bound": (P, "grader/instance.py:28-29 bounds [0.500,0.750] and [0.120,0.150] and the page Inputs (line ~314) state the same box; 20-seed sample in " + OUT + "instances_sample_r16.txt."),
    "E4d7-lab3-closed-form-sentence": (P, "project.html Lab 3 interpretation (line ~504) and the printed closed-form column (twin_project_3.out) agree; largest difference 2.1e-13."),
    "E4d7-test-count": (P, OUT + "cand/collect_reference.txt: 48 tests collected; project.html Grading mode (line ~320) says 48 checks."),
    "E4d8-no-upper-bound": (P, "project.html exception table (line ~326) names no upper bound; reference.py:26-34 has none; far-above-one tests pass (" + OUT + "cand/*.txt)."),
    "E4d8-cap-100-survives": (P, OUT + "mutate_graders_E4_0_9_final_r16.txt: mutant_r8_01_cap_100_halvings.py KILLED."),
    "E4d8-noise-cap-10-survives": (P, OUT + "mutate_graders_E4_0_9_final_r16.txt: mutant_r8_02_noise_above_ten_rejected.py KILLED."),
    "E4d8-cost-cap-5-survives": (P, OUT + "mutate_graders_E4_0_9_final_r16.txt: mutant_r8_03_cost_above_five_rejected.py KILLED."),
    "E4d8-mutants-r8-killed": (P, OUT + "mutate_graders_E4_0_9_final_r16.txt: mutant_r8_04 and mutant_r8_05 KILLED."),
    "E4d8-tiny-root-reference": (P, "reference.py at sd=1e-50, cost 0.1707691121: informed fraction equals the closed form 2.022385e-51 (" + OUT + "recheck_numbers_r16.txt)."),
    "E4d8-lab3-twin-page": (P, "run_labs.txt PASS (page code equals twin); twin_project_3.out equals the page expected block."),
    "E4d9-mutant-v9-02": (P, "ledgers/E4/equivalent/mutant_v9_02_stop_rule_relative_to_lower_end.py (ruling 17): stop test 1e-12 times the lower end; max deviation in " + OUT + "equiv_check_r16.txt is 0.0; passes 50/50 (" + OUT + "cand/equiv_mutant_v9_02_stop_rule_relative_to_lower_end.txt)."),
    "E4d9-mutant-v9-06": (P, OUT + "mutate_graders_E4_0_9_final_r16.txt: mutant_v9_06_gap_at_zero_from_tiny_fraction.py KILLED (test_gap_at_zero_fraction_is_the_limit_to_full_precision)."),
    "E4d9-equivalent-r6-08-09-docstrings": (P, "ledgers/E4/equivalent/mutant_r6_08_reports_lower_end.py docstring names the variant; mutant_r6_09 docstring first line names its error and is KILLED (" + OUT + "mutate_graders_E4_0_9_final_r16.txt)."),
    "E4d9-mutants-v9-killed": (P, OUT + "mutate_graders_E4_0_9_final_r16.txt: mutant_v9_01, v9_03, v9_05, v9_07 KILLED."),
    "E4d9-mutant-docstrings": (P, OUT + "mutant_profile.txt: first docstring line of all 130 mutants read; each names a student error (the four new v16 files included)."),
    "E4d10-delta-A1-prior-mean": (P, "project.html A1 (lines ~257-262): the prior-mean remark (a common mean shifts payoff, signal, conditional means and price by mu; demand and utility depend on differences) re-derived; true."),
    "E4d10-delta-inputs-interior-root": (P, "project.html Inputs (line ~314) tau_bar bounds and tau_y(1) bound recomputed (" + OUT + "recheck_numbers_r16.txt); interior-root claim follows from Prop 4 as the page argues."),
    "E4d10-delta-constraints-gap-at-zero": (P, "project.html Constraints (line 318) gap-at-zero clause (1e-14 relative to the larger of 1 and |limit|) matches test_project.py gap-at-zero test (1e-14 * max(1, |limit|))."),
    "E4d10-delta-grading-mode-43": (P, "project.html Grading mode (line ~320) says 48 checks; collect-only 48 (" + OUT + "cand/collect_reference.txt); no stale 43."),
    "E4d10-delta-results-ratio": (P, "project.html:634-642 and Results passage: ratios 1.25 and 1.50 from the displayed values 0.6978/0.5582 = 1.2501 and 0.8373/0.5582 = 1.5000 (recomputed)."),
    "E4d10-new-test-numbers": (P, "test_project.py docstrings with numbers recomputed (see E4d-grader-test-docstring; " + OUT + "recheck_numbers_r16.txt)."),
    "E4d10-mutants-new-r10": (P, OUT + "mutate_graders_E4_0_9_final_r16.txt: mutant_r10_01..04 (7 files) KILLED."),
    "E4d10-alternatives-r10": (P, OUT + "cand/alt_1.txt .. alt_5.txt: 50/50 each."),
    "E4d10-l06-dependency": (P, "Carried from round 15 (course/modules/E/E4/L06.html lines 57, 66 and 169 byte-identical since the previous pin; round-16 hunks at lines 86, 552, 722 do not touch them; L07.html:62 unchanged): the cited Lesson 6 and Lesson 7 statements are outside the diff."),
    "E4d10-lab3-numbers": (P, "project.html Lab 3 block (lines ~376-503) output equals " + OUT + "twin_project_3.out."),
    "E4d11-delta-hunks": (P, "every round-16 delta hunk in slice d read: project.html:171 (Lab 1 interpretation wording), :318 (Constraints: new 'Any reported fraction' sentence), test_project.py:402-406 (docstring), ledgers/E4/mutants cap normalisation and 4 new mutants, equivalent README ruling-17 section, plans/FINAL-ARCHITECT-RULINGS.md rulings 17 and 18."),
    "E4d11-constraints-accuracy": (P, "project.html:318 accuracy clause (1e-10 times the root for noise >= 1e-50 and tau_bar >= 1e-2) matches test_project.py tests at lines ~540-587; passes for reference and alternatives."),
    "E4d11-constraints-wording": (P, "project.html:318 wording read in full; numbers 1e-14, 1e-12, 240, 1e-10, 1e-50, 1e-2 re-derived (recheck_numbers_r16.txt)."),
    "E4d11-oracle-precision": (P, "test_project.py oracle at lambda=0 agrees with reference limit to 1.110e-16 (" + OUT + "recheck_numbers_r16.txt)."),
    "E4d11-mutants-new-r11": (P, OUT + "mutate_graders_E4_0_9_final_r16.txt: mutant_r11_01..04 KILLED."),
    "E4d11-alt-closed-form": (P, OUT + "cand/alt_6.txt: closed-form alternative (no bisection) 50/50 seeds pass."),
    "E4d11-literal-price-sign-open": (P, "project.html Proposition 1 (line ~277) states b_u/b_s = -a/(lambda tau_e); re-derived (step 3 gives kappa = -a/(lambda tau_e)); the literal sign-flip variant is output-identical (" + OUT + "equiv_check_r16.txt). The README records the architect question; it is not a verifier defect."),
    "E4d11-lab-page-twin": (P, "run_labs.txt 12/12: page lab code equals each twin (run_labs byte-identical check) and the expected blocks equal twin outputs (" + OUT + "twin_project_{1,2,3}.out)."),
    "E4d11-plan-tolerance-documented": (P, "project.html:318 documents the tolerance and stop rule; plans/E4-build-plan.md unchanged since the pin."),
    "E4d11-mutant-r10-02": (P, OUT + "mutate_graders_E4_0_9_final_r16.txt: mutant_r10_02_cost_factor_relative_error.py KILLED by a test in test_project.py (gap at a fraction, 1e-14 tolerance)."),
    "E4d12-bisection-assumption": (P, "project.html:318 'the sign-change assumption' cites A6 (line ~265); A6 defined and assumed, not proved (the page says so)."),
    "E4d12-corner-test-docstring": (P, "test_project.py test_corner docstring (lines ~564-567): sd 1e-50, tau_bar just above 1e-2 (1.012161e-2), root about 2e-51 (2.022385e-51), 200-halving width 6.2e-61 wider than 1e-10 times the root (" + OUT + "recheck_numbers_r16.txt)."),
    "E4d12-equivalent-readme-numbers": (P, "ledgers/E4/equivalent/README.md stop-rule numbers re-run this round: corner scan over 90000 cases (script corner_scan_r16.py, outputs " + OUT + "corner_scan_cap240_r16.txt and " + OUT + "corner_scan_cap200_r16.txt): cap 240 gives 0 cases over 1e-10 and max relative error 5.142e-13; cap 200 result in the same files."),
    "E4d12-prose-2pow240": (P, "reference.py:23 and the README: 2^-240 = 5.6598e-73 (README and page say 5.7e-73), so the bound holds (" + OUT + "recheck_numbers_r16.txt)."),
    "E4d12-tiny-noise-informativeness": (P, "project.html exception table paragraph (line ~326): a positive noise volume below 1e-50 is not named invalid, and the page states that the solver may return an inaccurate value there (disclosed). Range check of finite outputs at sd 1e150 and cost 350 (" + OUT + "recheck_numbers_r16.txt)."),
    "E4d13-endpoint-gap-precision": (P, "test_project.py endpoint gap tests (lines ~420-460) pass for reference and alternatives (" + OUT + "cand/*.txt)."),
    "E4d13-readme-corner-domain": (P, "ledgers/E4/equivalent/README.md 'Stop-rule variants' paragraph 2: domain and numbers re-run with corner_scan_r16.py (see E4d12-equivalent-readme-numbers)."),
    "E4d13-independent-rederivation": (P, "project.html Props 1-5 and Lemmas 1-3 re-derived by this verifier this round (E4d-math-* rows); numerical cross-checks in the suite oracles and Lab 3."),
    "E4d13-accuracy-sweep": (P, "accuracy evidence: test_project.py tolerance tests (" + OUT + "cand/*.txt), recheck_numbers_r16.txt and corner_scan_r16.py (cap 240: 0 cases over 1e-10)."),
    "E4d13-extreme-inputs": (P, "project.html:316-318 and :326-327 read; recheck_numbers_r16.txt range check: sd 1e150 with cost 0.5 and 350 and sd 0.5 with cost 350 return three finite values; sd 1e-50 returns finite values."),
    "E4d13-instances-seeds-0-49": (P, "instance.py deterministic and in box; run_graders 50/50 (" + OUT + "run_graders_0_49.txt); 20-seed sample (" + OUT + "instances_sample_r16.txt)."),
    "E4d13-candidates-accepted": (P, OUT + "cand/alt_1..alt_8, equiv_*, reference: all 50/50 seeds pass (run_candidate_r16.py)."),
    "E4d13-new-mutants": (P, OUT + "mutate_graders_E4_0_9_final_r16.txt: mutant_r13_01..04 KILLED."),
    "E4d13-mutant-gate-final": (P, OUT + "mutate_graders_E4_0_9_final_r16.txt: 130/130 killed; tools/mutate_graders.py --unit E4 --seeds 0-9."),
    "E4d13-notation": (P, "see E4d-notation (notation/notation.json against project.html notation paragraph and Propositions)."),
    "E4d13-links": (P, "see E4d3-anchors-links and E4d-dag-links (" + OUT + "scope_and_anchors_r16.txt)."),
    "E4d13-hours-arithmetic": (P, "project.html hours table: 1+1+5+8+5+5+3 = 28 (lines ~343-352); hub 72 + 28 = 100 (index.html:29)."),
    "E4d13-exemplar-numbers-arith": (P, "project.html Exemplar B Results passage: ratios 1.25 and 1.50 (0.6978/0.5582 = 1.2501; 0.8373/0.5582 = 1.5000); max gap 3.55e-14 < 4e-14 (recomputed from twin_project_3.out)."),
    "E4d14-mutants-r14-new": (P, OUT + "mutate_graders_E4_0_9_final_r16.txt: mutant_r14_01..05 KILLED."),
    "E4d14-equivalent-literal-3000": (P, OUT + "equiv_check_r16.txt: literal_price_sign.py 4000 cases, zero bitwise mismatches."),
    "E4d15-grader-docstring-scale": (P, "FIXED since round 15: test_project.py:402-406 docstring now says 'relative to the larger of 1 and the oracle's gap at the reported fraction', and the code (lines ~412-416) uses limit = oracle_gap(lam) with max(1.0, abs(limit)). Consistent."),
    "E4d15-mutants-single-change": (P, "FIXED since round 15: " + OUT + "mutant_ast_profile.txt (AST, docstrings removed): every mutant differs from reference.py in one code unit; MAX_BISECTION_STEPS is 240 in every mutant except the four intended cap mutants (mutant_f11_01 200, mutant_f11_02 150, mutant_f12_10 120, mutant_r8_01 100), each KILLED."),
    "E4d15-mutants-new-r15": (P, OUT + "mutate_graders_E4_0_9_final_r16.txt: mutant_r15_01..04 KILLED."),
    "E4d15-alternatives-sweep": (P, OUT + "cand/alt_1..alt_8.txt: 50/50 each (run_candidate_r16.py)."),
    "E4d15-exemplar-verdicts": (P, "project.html:537 and :602 data-scores (2,2,1,2,1 and 4,4,4,4,4) equal the verdict lines at :539 and :604 (read this round). The verdict lines are the official scores; the blind process is recorded UNVERIFIABLE in E4d-exemplar-A/B-calibration."),
    "E4d15-stop-rule-variants-architect": (P, "RESOLVED by ruling 17 (plans/FINAL-ARCHITECT-RULINGS.md lines 39-42): the three stop-rule variants live in ledgers/E4/equivalent/ with the proof in README 'Decision: ruling 17'. Numeric check " + OUT + "equiv_check_r16.txt; all pass 50/50."),
    "E4d15-literal-price-sign": (P, "ledgers/E4/equivalent/literal_price_sign.py: output-identical (" + OUT + "equiv_check_r16.txt, 4000 cases, zero bitwise mismatches); equivalent mutant with proof, not a survivor in mutants/."),
    "E4d15-range-extremes": (P, OUT + "recheck_numbers_r16.txt range check: finite outputs at sd 1e150 (cost 0.5), at cost 350 (sd 0.5 and 1e150), and at sd 1e-50; project.html:326-327 exception table paragraph consistent."),
    "E4d15-plan-and-rulings": (P, "plans/FINAL-ARCHITECT-RULINGS.md read in full (rulings 1-18). Ruling 17 applied (equivalent folder); ruling 18 applied (alt_r8_* and alt_v9_* do not exist in ledgers/E4/alternatives/, verified by ls)."),
    "E4d15-reading-and-citations": (P, "project.html Reading section (lines ~683-687) and references/references.json entries (E4d-registry-muth, E4d-registry-milgrom, live verify_refs E4 0 problems)."),
    "E4d6-alt-extra-damped": (P, "ledgers/E4/scripts/E4-d-r6/candidates/damped_fixed_point_log_r6.py is a damped fixed-point candidate that stops on the step size (|du| <= 1e-13 relative). Re-run this round with run_candidate_r16.py: 0/50 seeds pass, failing test_tiny_noise_root_is_relatively_accurate[1e-40] and test_corner_root_meets_the_relative_accuracy_at_the_domain_edge (" + OUT + "cand/extra_damped_fixed_point_log_r6.txt). It is a wrong implementation under the page's accuracy clause (noise >= 1e-50, tau_bar >= 1e-2), so the suite correctly rejects it; it is a plausible student error, not an alternative, and it is not counted in mutants/."),
    "E4d7-alt5-docstring": (P, "ledgers/E4/alternatives/alt_5.py:1-2 docstring 'the same model parameterised by the noise precision, with the same bracket [0, 1]' matches the code (nu = 1/sd^2, bracket [0,1], line 42); alt_5 50/50 (" + OUT + "cand/alt_5.txt)."),
    "E4d12-alt-variants-new": (P, OUT + "cand/alt_6.txt, alt_7.txt, alt_8.txt: each 50/50 seeds pass (round-12 files, now in ledgers/E4/alternatives/)."),
    "E4d12-exemplar-B-sigma": (P, "project.html exemplar B Model passage (line ~608): 'the volume sigma appears in Propositions 1, 3 and 4'. Checked: sigma appears in the Prop 1 tau_y, in the Prop 3 G(0+) formula and Omega, and in the Prop 4 closed form; Prop 2 uses tau_y (which depends on sigma through Prop 1). The statement is consistent with the propositions."),
    "E4d12-mutant-gap-stop": (P, OUT + "mutate_graders_E4_0_9_final_r16.txt: mutant_r12_04_stops_when_midpoint_gap_is_tiny.py KILLED."),
    "E4d13-alternatives-plan-list": (P, "ledgers/E4/alternatives/alt_4.py docstring line 1 (secant steps, safeguarded by the sign change, relative stop) and alt_5.py docstring match the code; all eight alternatives 50/50 (" + OUT + "cand/alt_*.txt)."),
    "E4d13-lab-twins-direct": (P, "tests/labs/E4/lab-E4-project-1.py, -2.py, -3.py run alone under python -I -W error (run_twins_r16.sh): exit 0, stderr 0 bytes each; outputs " + OUT + "twin_project_{1,2,3}.out."),
    "E4d14-corner-scan": (P, "corner_scan_r16.py (copy of the round-15 scan over 90000 cases of the README domain): cap 240 gives 0 cases above 1e-10, max relative 5.142e-13 (" + OUT + "corner_scan_cap240_r16.txt); cap 200 gives 11598 cases above 1e-10, max relative 1.5322e-10 (" + OUT + "corner_scan_cap200_r16.txt). Both match the README."),
    "E4d14-accuracy-sweep": (P, "accuracy sweep re-run as the corner scan (" + OUT + "corner_scan_cap240_r16.txt and cap200) plus the tolerance tests on reference and alternatives (" + OUT + "cand/*.txt)."),
    "E4d14-delta-read": (P, "delta d1e65a0..56cc575 for slice d read hunk by hunk (git diff -- course/modules/E/E4 tests/labs/E4 ledgers/E4 plans; see the notes of this fragment)."),
    "E4d15-cmd-mutate": (P, OUT + "mutate_graders_E4_0_9_final_r16.txt: tools/mutate_graders.py --unit E4 --seeds 0-9: 'mutate_graders E4: PASS (130/130 killed)', exit 0."),
    "E4d-spec-questions-r16": (P, "not used"),
}
# Round-15 PASS rows whose cited subject is outside this round's review were re-run; the rows below are the
# round-15 non-PASS rows whose subjects changed or whose blocker was architect-resolved.
RESOLVED = {
    "E4d-equivalent": "see row text",
    "E4d6-spec-variants-08-09": "see row text",
    "E4d7-midpoint-untested": "see row text",
    "E4d9-mutant-v9-02": "see row text",
    "E4d15-stop-rule-variants-architect": "see row text",
    "E4d15-grader-docstring-scale": "see row text",
    "E4d15-mutants-single-change": "see row text",
}
RETIRED = {
    "E4d8-alternatives-r8": "Retired by ruling 18 (plans/FINAL-ARCHITECT-RULINGS.md lines 44-45): ledgers/E4/alternatives/alt_r8_a.py and alt_r8_b.py do not exist (ls of ledgers/E4/alternatives shows alt_1..alt_8 only). Row retired; the current alt_1..alt_8 are the verified set, all 50/50 (" + OUT + "cand/alt_*.txt).",
    "E4d9-alternatives-v9": "Retired by ruling 18: ledgers/E4/alternatives/alt_v9_1_interior_gap_zero.py, alt_v9_2_log_space.py and the other alt_v9_* files do not exist. Row retired; alt_1..alt_8 verified 50/50 (" + OUT + "cand/alt_*.txt).",
}
for k, v in RESOLVED.items():
    pass
ROWS["E4d8-alternatives-r8"] = (P, RETIRED["E4d8-alternatives-r8"])
ROWS["E4d9-alternatives-v9"] = (P, RETIRED["E4d9-alternatives-v9"])
ROWS.pop("E4d-spec-questions-r16", None)

# Round-16 new rows
NEW = [
    ("E4d16-mutants-v16-new", "mutants", P, OUT + "mutate_graders_E4_0_9_final_r16.txt: mutant_v16_01_boundary_zero_uses_exp_minus_ac_threshold KILLED by test_zero_fraction_is_reported_above_the_cost_threshold; mutant_v16_02_uninformed_term_reads_price_precision_at_one KILLED by test_gap_is_the_oracle_gap_at_the_reported_fraction; mutant_v16_03_unit_informativeness_uses_noise_volume_once KILLED by test_unit_fraction_is_reported_at_zero_cost; mutant_v16_04_informed_slope_uses_uninformed_precision KILLED by test_gap_is_the_oracle_gap_at_the_reported_fraction. Generated by " + OUT.replace("out/", "") + "make_mutants_r16.py from grader/reference.py with one block replaced each (asserted unique)."),
    ("E4d16-mutants-ast-profile", "mutation-form", P, OUT + "mutant_ast_profile.txt: AST profile against reference.py for all 130 mutants; one differing code unit each (the intended multi-unit ones: r2_grid_scan_no_refinement, r3_closed_form_cost_sign_flipped, r6_01_memorised_seed_answers and the 2-unit cap and boundary mutants). MAX_BISECTION_STEPS != 240 only in the four intended cap mutants."),
    ("E4d16-alt-sweep", "alternatives", P, OUT + "cand/alt_1.txt .. alt_8.txt: 50/50 seeds each. Styles: relative bisection (alt_1), Illinois on the gap (alt_2), grid scan then bisection (alt_3), safeguarded secant (alt_4), precision parameterisation (alt_5), closed form with no bisection (alt_6), bisection on the sign of tau_bar minus tau_y (alt_7), Illinois on tau_bar (alt_8). Ruling 10 satisfied."),
    ("E4d16-equiv-bitwise", "mutation", P, OUT + "equiv_check_r16.txt (equiv_check_r16.py): literal_price_sign.py gives bitwise identical solve_model outputs on 4000 random cases (3000 in [0.05,3]x[0,0.4], 1000 in the box). Proof in README: b_u enters only through b_u*b_u (reference.py informed_term)."),
    ("E4d16-equiv-ruling17-numeric", "mutation-ruling17", P, OUT + "equiv_check_r16.txt: for mutant_r6_08, mutant_r7_01 and mutant_v9_02 the reported fraction differs from the reference by at most 4.97e-13 relative (ruling 17 needs at most 1e-10) and the gap by at most 7.96e-14; the 4 corner points are included."),
    ("E4d16-constraints-any-sentence", "spec-vs-suite", P, "project.html:318 new sentence 'Any reported fraction within 1e-10 times the oracle's root is accepted, whatever point of the final bracket the solver reports' is consistent with test_project.py tolerance tests (1e-10 times the root) and with the equivalence checks (" + OUT + "equiv_check_r16.txt)."),
    ("E4d16-instances-20", "instances", P, OUT + "instances_sample_r16.txt: 20 seeds, deterministic, inside the box, 20 distinct informed fractions (instance.py)."),
    ("E4d16-exemplar-B-claims", "rubric", P, "project.html Exemplar B passage (lines ~607-660) re-read: numeric claims (table, ratios 1.25/1.50, max gap 3.55e-14 < 4e-14, informativeness constant across noise at each cost, fractions fall with cost) all match twin_project_3.out and the arithmetic; the model claims (Assumptions 1-6, A3 utility -exp(-2w)) match project.html A1-A6."),
    ("E4d16-hours-band", "hours", P, "hours band: rung-by-rung estimate midpoint 23 h against 28 h declared (18% below) inside the 30% bar (E4d-hours-estimate)."),
    ("E4d16-tier-M-ladder-sister", "spec", P, "tier-M sister modules M6 and SC1 project.html say 'Rungs 1 and 2 are short.'; E4 says 'at full length' (E4d-spec-ladder FAIL). Recorded as evidence for the architect decision on the program-wide convention; see notes."),
]
rows = []
for r in PREV["rows"]:
    rid = r["id"]
    if rid not in ROWS:
        raise SystemExit("missing evidence for round-15 id " + rid)
    status, text = ROWS[rid]
    rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": status, "evidence": text})
    if status != P:
        rows[-1]["fix"] = ""
extra = set(ROWS) - set(prev_rows)
if extra:
    raise SystemExit("evidence for ids not in round 15: " + ", ".join(sorted(extra)))
for rid, check, status, text in NEW:
    rows.append({"id": rid, "check": check, "location": "see evidence", "status": status, "evidence": text})

FIX = {
    "E4d-spec-ladder": "project.html:42: replace 'Rungs 1 and 2 are at full length.' with the tier-M wording used by M6 and SC1 ('Rungs 1 and 2 are short.') and trim Lab 1 and Lab 2 to the minimum, or record an architect ruling that the program-wide 'full length' wording supersedes BUILDER_RULES 5.1 for tier M.",
    "E4d-rubric-observable": "project.html rubric table, criterion C5, level 1 cell (line 529): replace 'Notes caveats without naming a limit.' with an observable descriptor, for example 'Names no limit of the model; hedges only with general remarks such as results may vary', and make level 2 name specific assumptions as limits ('Names one or two specific assumptions of the model, for example the exponential utility or the exogenous noise supply, as limits').",
    "E4d-exemplar-A-calibration": "Re-score Exemplar A blind by a verifier that has not read data-scores or the verdict lines (run strip_exemplars.py first, then score). Expect C5 to be compared on the sentence 'The results depend on the model, which is a simplified description of a market.'",
    "E4d-exemplar-B-calibration": "Re-score Exemplar B blind by a verifier that has not read data-scores or the verdict lines (run strip_exemplars.py first, then score).",
    "E4d4-calibration-blind": "As E4d-exemplar-A-calibration.",
    "E4d5-calibration-B-blind": "As E4d-exemplar-B-calibration.",
}
for r in rows:
    if r["status"] != P:
        r["fix"] = FIX.get(r["id"], FIX.get(r["id"].replace("E4d4-", "E4d-"), "")) or (
            "Blind re-score by a fresh verifier (see notes)." if r["status"] == U else "")
        if not r["fix"]:
            raise SystemExit("no fix for non-PASS row " + r["id"])

mutants = []
mut_out = (root / (OUT + "mutate_graders_E4_0_9_final_r16.txt")).read_text(encoding="utf-8").splitlines()
for line in mut_out:
    m = re.match(r"KILLED (\S+?\.py): (.*) -> (.*)$", line)
    if m:
        name, desc, killed = m.group(1), m.group(2), m.group(3)
        mutants.append({"id": name[:-3], "file": f"ledgers/E4/mutants/{name}", "description": desc,
                        "killed_by": killed})
if len(mutants) != 130:
    raise SystemExit(f"expected 130 killed mutants, got {len(mutants)}")

fragment = {
    "unit": "E4",
    "slice": "d",
    "round": 16,
    "verifier": "Haiku independent verifier, E4 slice d, round 16 (did not build E4; checkout pinned at 56cc575, detached)",
    "pin": "56cc575a774a66e9580d3182969eb7d6aa413731",
    "base": "d1e65a0203e386e3246429ba1cf7e723eb6cfbfa (round-15 pin); delta in slice d listed in notes",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE16-E4-d",
    "scratch": "/tmp/e4d16_scratch (recheck only; all evidence files are under ledgers/E4/scripts/E4-d-r16/out/)",
    "verified_at": "2026-11-09T03:10:00+00:00",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Blind exemplar scoring (ruling 15) is NOT clean this round: the first grep of project.html (for exemplar, data-score, verdict, annotation) printed the data-scores attributes and the official verdict lines of both exemplars before the stripping script existed. The stripping script (ledgers/E4/scripts/E4-d-r16/strip_exemplars.py) was then run, and the blind scores were taken from the stripped prose only (exemplar_prose_stripped.txt). Both calibration rows are UNVERIFIABLE for that reason, as in round 15. Blind-derived scores: A 2,2,1,2,2 (official 2,2,1,2,1: C5 differs by one level, within the bar); B 4,4,4,4,4 (official 4,4,4,4,4).",
        "Delta since the round-15 pin d1e65a0 in slice d: course/modules/E/E4/project.html (6 lines: Lab 1 interpretation wording at line 171, the Constraints sentence 'Any reported fraction within 1e-10 times the oracle's root is accepted' at line 318); grader/test_project.py (docstring lines 402-406 only; file grew by one line after 401, so later test line numbers in older rows shift by +1); ledgers/E4/mutants (cap normalisation of 87 files to MAX_BISECTION_STEPS = 240, and mutant_r15_01..04 retained); ledgers/E4/equivalent (ruling 17 proof README, three stop-rule variants and literal_price_sign.py); plans/FINAL-ARCHITECT-RULINGS.md (rulings 17 and 18). L03.html, L06.html and cards.json changed outside the cited lines (L06 hunks at 86, 552, 722; L03 and cards are other slices).",
        "Rulings applied: 15 (blind scoring procedure, not established this round), 17 (stop-rule variants accepted as equivalent with the README proof, numerically re-checked: 4.97e-13 maximum relative deviation against 1e-10), 18 (alt_r8_* and alt_v9_* retired; they do not exist). Ruling 9 is applied to literal_price_sign.py: an output-identical variant (4000 cases, zero bitwise mismatches) is an equivalent mutant with proof, not a survivor. The README records an architect question about Proposition 1's sign; this verifier treats it as a page-statement question, not a row defect.",
        "New student-error mutants written and killed (4, required at least 3): mutant_v16_01 to v16_04 in ledgers/E4/mutants/. All 130 mutants killed on seeds 0-9 (out/mutate_graders_E4_0_9_final_r16.txt). Existing mutants re-run; the AST profile confirms each differs from reference.py in one code unit.",
        "Alternatives: alt_1..alt_8 pass 50/50 on seeds 0-49 each (out/cand/); equivalents pass 50/50; reference passes 50/50; collect-only 48 (matches the page's 48 checks).",
        "Gate runs (out/): check_pages, check_dag, check_projects, run_labs 12/12, run_graders 0-49 PASS, page_smoke project PASS, mutate_graders 130/130, ruff check and format clean, mypy --no-incremental clean (16 files), verify_refs offline 560 entries 0 problems, verify_refs live E4 3 entries 0 problems, pytest on four relevant test files passed. Lab twins run alone under python -I -W error with empty stderr (run_twins_r16.sh).",
        "Hours: midpoint estimate 23 h against 28 h declared (18% below, inside the 30% bar). The ladder sentence 'at full length' conflicts with BUILDER_RULES 5.1 for tier M (row E4d-spec-ladder FAIL); M6 and SC1 use 'short', so E4 is the outlier, not the program convention.",
        "Rubric: C5 level 1 'Notes caveats without naming a limit.' is not observable enough: the official annotation scores the sentence 'The results depend on the model, which is a simplified description of a market.' as level 1, and this verifier's blind reading gave level 2. Two readers disagree, so the descriptor is vague (row E4d-rubric-observable FAIL).",
        "Not checked by this verifier: lessons L01-L09 and cards.json (other slices; cards are excluded from this round); tools/render_curriculum.py, build_site.py --check and fetch_data.py --check (no curriculum, site-data, market or reference input changed in slice d); the full pytest suite (only the four relevant files); the live verify_refs for all 560 entries (only the three E4 entries live); the Pyodide interpreter itself (page_smoke runs the repo harness); the 50-seed run of mutate_graders (the gate uses seeds 0-9 as the tool's default window); L03.html and L06.html outside the cited lines.",
        "Commands run from the checkout root with .venv (Python 3.14); scripts under ledgers/E4/scripts/E4-d-r16/ and outputs under ledgers/E4/scripts/E4-d-r16/out/.",
    ],
    "summary": "E4 slice d round 16 (pin 56cc575): verdict FAIL. Two FAIL rows: E4d-spec-ladder (project.html:42 'at full length' vs BUILDER_RULES 5.1 tier-M 'minimal'; tier-M sisters say 'short') and E4d-rubric-observable (C5 level 1 'caveats' is vague; two readers disagree). Four UNVERIFIABLE rows: the blind exemplar calibration of both exemplars (A and B, two ids each) is not clean because the verifier saw the official scores in the first grep; the blind-stripped scores are within one level. Resolved since round 15: grader docstring scale, mutant cap normalisation, stop-rule variants (ruling 17), literal price sign (equivalent, proof), alt_r8/alt_v9 retired (ruling 18). New mutants: 4 (v16_01..04), all killed; 130/130 killed. Alternatives 8/8 at 50/50; equivalents 4/4 at 50/50; reference 50/50; collect 48.",
}
fragment["rows"] = rows
(root / "ledgers/E4/E4-d.json").write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("rows", len(rows), "statuses", {s: sum(1 for r in rows if r["status"] == s) for s in (P, F, U)}, "mutants", len(mutants))
