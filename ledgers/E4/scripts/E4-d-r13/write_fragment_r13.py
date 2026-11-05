"""Writes the round-13 fragment ledgers/E4/E4-d.json (slice d, verifier round 13). Row ids are the round-12 ids plus new ones."""

from __future__ import annotations

import ast
import json
import re
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyE13-E4-d")
S = "ledgers/E4/scripts/E4-d-r13/"
PREV = json.loads(Path("/Users/billyribeiro/.fanout/frags/E-E4-d.round12.json").read_text(encoding="utf-8"))

OVERRIDE: dict[str, tuple[str, str, str | None]] = {}  # id -> (status, evidence, fix)


def ok(evidence: str) -> tuple[str, str, None]:
    return ("PASS", evidence, None)


OVERRIDE.update({
    "E4d-notation": ok("Re-checked: project.html has no \\ast, \\mathbb or \\Phi/\\gamma/\\Q symbols (grep); Lemma 1 now writes the demand as \\hat{x} (project.html:267-268). notation.json registers no \\sigma, \\tau, \\Omega or \\hat."),
    "E4d-grader-reference-docstring": ok("reference.py:23 now reads '(2^-240 is about 5.7e-73)'; 2^-240 = 5.6598e-73 (rederive_r13.txt section 6). The 6.2e-73 text is gone from ledgers/E4/equivalent and mutants (grep)."),
    "E4d3-spec-stop-rule-and-constraints": ok("Accuracy clause (project.html:318) now tested at cost 1e-6 and 1e-4 (test_project.py:568-578) and at sd 1e-11..1e-40 (:543-553); mutant_r12_04 KILLED by test_root_is_relatively_accurate_at_a_cost_near_zero[1e-50-1e-06] (mutate_E4_0_9_final.txt). Reference accuracy sweep: 4.95e-13 max over 3706 interior points (accuracy_sweep_r13.txt)."),
    "E4d-mutants-total": ok("tools/mutate_graders.py --unit E4 --seeds 0-9 (final): 116/116 KILLED, exit 0 (mutate_E4_0_9_final.txt)."),
    "E4d11-constraints-accuracy": ok("Same as E4d3-spec-stop-rule-and-constraints: the cost-near-zero accuracy tests (test_project.py:568-578) exist and kill mutant_r12_04; the accuracy sweep confirms the clause on the reference."),
    "E4d12-bisection-assumption": ok("A6 'Sign change and continuity (bisection)' is numbered at project.html:262 and cited from Constraints (:318) and Lab 1/Lab 2 hypotheses; the plan's Q14/D4 requirement (numbered sign-change assumption) is met."),
    "E4d12-exemplar-B-sigma": ok("Exemplar B Model passage now says the volume sigma appears in Propositions 1, 3 and 4 (project.html Exemplar B Model, around :607). Proposition 1 (tau_y), Proposition 3 (G(0+)) and Proposition 4 (lambda*) contain sigma (project.html:276-298)."),
    "E4d12-mutant-gap-stop": ok("ledgers/E4/mutants/mutant_r12_04_stops_when_midpoint_gap_is_tiny.py KILLED by test_root_is_relatively_accurate_at_a_cost_near_zero[1e-50-1e-06] (seed 0) in mutate_E4_0_9_final.txt."),
    "E4d12-prose-2pow240": ok("No '6.2e-73' remains in course/modules/E/E4/grader/reference.py, ledgers/E4/equivalent/*.py or ledgers/E4/mutants/*.py (grep, round 13); reference.py:23 reads 5.7e-73."),
    "E4d12-tiny-noise-informativeness": ok("Scope is now stated: project.html:316 (Required outputs) and :318 (Constraints) state the accuracy requirement only for noise volume >= 1e-50; :327 (exception table) says a positive noise volume below 1e-50 is not named invalid and the solver 'may return an inaccurate value there'. Reproduced: sd=1e-300 gives lambda 2.83e-73 and informativeness 0.5 (extremes_r13.txt), which is the disclosed inaccuracy. Architect note: fail-loud below 1e-50 is an option (see notes)."),
    "E4d12-equivalent-readme-numbers": ("FAIL", "ledgers/E4/equivalent/README.md states the round-11 corner domain as 'noise volume 1e-50 to 1.06e-50, cost with tau-bar at least 1e-2' and the cited cost as 0.17076911209. The round-11 scan (E4-d-fix-r11/check_corner_accuracy_fix11.py) spans sd 1.000e-50..1.598e-50 and tau-bar 0.010000..0.012022; the truncated cost gives a cap-200 error of 8.0e-12, not 1.53e-10 (readme_corner_repro_r13.txt). Its 11598, 1.5322e-10 (full cost) and 5.142e-13 (cap 240) figures reproduce (readme_grid_cap240_r13.txt). See E4d13-readme-corner-domain.", "Correct the README domain to sd 1e-50..1.598e-50 and tau-bar 0.0100..0.0121 (or extend the scan), and write the cost as 0.17076911209224613. Full fix in E4d13-readme-corner-domain."),
    "E4d-exemplar-A-calibration": ("UNVERIFIABLE", "Blind scoring impossible: this verifier read the Exemplar A verdicts and annotations (project.html:533-597) in round 12 and again in round 13. Not scored.", "An independent verifier who has not read the annotations must score Exemplar A blind, within one level per criterion."),
    "E4d-exemplar-B-calibration": ("UNVERIFIABLE", "Same reason: the Exemplar B verdict and annotations (project.html:598-661) were read in round 13. Not scored.", "An independent verifier who has not read the annotations must score Exemplar B blind."),
    "E4d4-calibration-blind": ("UNVERIFIABLE", "Same blind-scoring limit as E4d-exemplar-A-calibration (Exemplar A annotations read). Not scored.", "Independent blind scoring of Exemplar A."),
    "E4d5-calibration-B-blind": ("UNVERIFIABLE", "Same blind-scoring limit as E4d-exemplar-B-calibration (Exemplar B annotations read). Not scored.", "Independent blind scoring of Exemplar B."),
    "E4d8-alternatives-r8": ("UNVERIFIABLE", "ledgers/E4/alternatives/ holds alt_1.py..alt_8.py only at this pin; alt_r8_a/alt_r8_b are absent. No current slice file cites them (grep over ledgers/E4, course/modules/E/E4, plans/E4-build-plan.md); only historical round-8 records do.", "Retire the round-8 citation or restore alt_r8_a/alt_r8_b at a pin."),
    "E4d9-alternatives-v9": ("UNVERIFIABLE", "alt_v9_1_interior_gap_zero.py, alt_v9_2_log_space.py, alt_v9_3_grid_then_bisect.py are absent at this pin. Only round-9 logs (ledgers/E4/scripts/E4-d-r9/logs/alternatives_v9_seeds0-49.txt) mention them, and the round-9 mutant_v9_04 file is gone from mutants/.", "Retire the round-9 citation or restore the files at a pin."),
})

PASS_EVIDENCE: dict[str, str] = {
    "E4d-cmd-check-projects": "`tools/check_projects.py --unit E4` -> 'check_projects E4: PASS', exit 0 (" + S + "check_projects_E4.txt).",
    "E4d-cmd-check-pages": "`tools/check_pages.py --unit E4` -> 'check_pages E4: PASS', exit 0 (" + S + "check_pages_E4.txt).",
    "E4d-cmd-check-dag": "`tools/check_dag.py --unit E4` -> 'check_dag E4: PASS', exit 0 (" + S + "check_dag_E4.txt).",
    "E4d-cmd-run-labs": "`tools/run_labs.py --unit E4 --page project` -> 'run_labs E4: PASS (3/3)'; whole unit 12/12 (" + S + "run_labs_E4_project.txt, run_labs_E4_all.txt). Twins also run directly as `python -I -W error` with exit 0 and empty stderr.",
    "E4d-cmd-run-graders": "`tools/run_graders.py --unit E4 --seeds 0-49` -> 'run_graders E4: PASS (reference 50/50 seeds)', exit 0 (" + S + "run_graders_E4_0_49.txt).",
    "E4d-cmd-page-smoke-project": "`tools/page_smoke.py --unit E4 --pages project` (the stem, not the file name; the file name matched nothing and was rerun) -> 'page_smoke modules/E/E4/project.html: PASS' with 'All 48 tests pass' in-browser (" + S + "page_smoke_E4_project_alone.txt).",
    "E4d-cmd-ruff": "`.venv/bin/ruff check .` -> 'All checks passed!', exit 0; `ruff format --check .` -> '559 files already formatted' (" + S + "ruff_check.txt, ruff_format.txt).",
    "E4d-cmd-mypy-workspace": "`.venv/bin/mypy --no-incremental` -> 'Success: no issues found in 385 source files', exit 0 (" + S + "mypy.txt).",
    "E4d-cmd-mypy-plan-command": "The same mypy run covers tools and tests (pyproject files); the grader is type-checked by run_graders (strict mypy on reference, starter, instance) in run_graders_E4_0_49.txt.",
    "E4d-cmd-pytest-relevant": "`.venv/bin/pytest -q tests/test_labs.py tests/test_page_checks.py tests/test_memo_exemplars.py tests/test_run_labs.py -k 'E4 or project or memo or run_labs or page_checks'` -> exit 0 (" + S + "pytest_E4_relevant.txt).",
    "E4d-cmd-verify-refs": "`tools/verify_refs.py --offline` -> 'offline integrity: 560 entries, 0 problems', exit 0; `tools/verify_refs.py --unit E4` (live) -> '3 of 560 entries, 0 problems', exit 0 (" + S + "verify_refs_offline_all.txt, verify_refs_E4_live.txt).",
    "E4d-cmd-collect": "`pytest --collect-only -q test_project.py` in a scratch copy of grader/ -> '48 tests collected'; the suite on the reference: '48 passed' (seed 0).",
    "E4d-lab-project-1": "run_labs (" + S + "run_labs_E4_project.txt): page code equals the twin and the expected block equals the output. Twin run `python -I -W error` exit 0 (" + S + "twin_p1.out).",
    "E4d-lab-project-2": "run_labs completion rule passes (" + S + "run_labs_E4_project.txt); completed twin exit 0 with the page's printed numbers (" + S + "twin_p2.out).",
    "E4d-lab-project-3": "run_labs passes; twin output (" + S + "twin_p3.out) equals the page expected block line by line (9 grid rows, largest difference 2.1e-13, 484 of 484).",
    "E4d-num-lab-hypotheses": "Recomputed independently (" + S + "rederive_r13.txt sections 3-5): Lab 1 G(0+)=+0.053092, G(1)=-0.080731, root 0.57937525, b_u/b_s -3.45199422, tau_y 0.18904110, informativeness 0.15898618; Lab 2 +0.037435, -0.071386, 0.57052263, 0.12466375; Lab 3 0.5582/0.6978/0.8373 and informativeness 0.1920/0.1420/0.0889; 484 of 484.",
    "E4d-num-exemplar-table": "Exemplar B table rows equal Lab 3 printed rows (" + S + "twin_p3.out); unrounded ratios 1.250000000000 and 1.500000000000 (rederive_r13.txt section 4); printed gaps max 3.55e-14 < 4e-14.",
    "E4d-num-box-bounds": "tau_bar(0.150)=0.0976232722, tau_bar(0.120)=0.2375667836, 1/(1+4*0.75^2)=0.3076923077 (rederive_r13.txt section 6); 484 of 484 box points have an interior fraction (rederive_r13.txt section 5).",
    "E4d-prose-lede-directional": "Lede (project.html:37): tau_y = lambda^2 tau_e^2/(lambda^2 tau_e + a^2 sigma^2) falls with sigma at fixed lambda; on the interior the fraction rises with sigma and the informativeness is constant in sigma (Proposition 5; Lab 3 printed grid; rederive_r13.txt section 4).",
    "E4d-math-lemmas": "Lemmas 1-3 re-derived by hand; expected utilities recomputed from Gaussian quadratic forms det(I+2a Sigma S)^(-1/2) (rederive_r13.py section 1) agree with Proposition 3 to 3.3e-16.",
    "E4d-math-prop1": "Steps (0)-(4) re-derived by hand (clearing brackets give kappa = -a/(lambda tau_e) and tau_y); numerical clearing root (rederive_r13.txt section 3): b_u/b_s = -3.45199422 = -a/(lambda* tau_e).",
    "E4d-math-prop2": "Cov(v,p) = b_s/tau_v and Var(p) = b_s^2(1/tau_v+1/tau_y) re-derived; independent Corr^2 from the covariance matrix equals tau_y/(tau_v+tau_y) to 5.6e-17 (rederive_r13.txt section 1). The lambda = 0 argument (p proportional to u, so b_s = 0 and beta = 0) re-read: consistent.",
    "E4d-math-prop3": "Sign rule, Omega decomposition and G(0+) re-derived by hand; independent G matches the page formula to 3.3e-16; G(1e-7) - G(0+) = 3e-9, linear in lambda (rederive_r13.txt section 2).",
    "E4d-math-prop4": "Three cases and the interior closed form re-derived (lambda^2(tau_e^2 - tau_bar tau_e) = tau_bar a^2 sigma^2); bisection equals the closed form to 2.1e-13 on the Lab 3 grid and to 4.95e-13 relative over 3706 interior points (accuracy_sweep_r13.txt).",
    "E4d-math-prop5": "d lambda*/d sigma = lambda*/sigma and the cost monotonicity re-derived by hand; the unrounded grid ratios are exactly 1.25 and 1.50 (rederive_r13.txt section 4).",
    "E4d-math-assumptions": "A1-A6 read in full (project.html:257-262). A1's prior-mean shift invariance re-derived: demand and expected utility depend on v-p and E[v|F]-p only.",
    "E4d-banned-phrases": "check_pages (BANNED list) passes (" + S + "check_pages_E4.txt); grep of project.html and grader/*.py for TODO, TBD, lorem, obviously, clearly, studies show, experts agree, '...' gives no hit.",
    "E4d-process-words": "grep of project.html and grader/*.py for build, builder, round, verifier, REQUESTS, planner, ruling: no hit; 'verification' appears only in the rubric label 'Solver and verification' (a learner term).",
    "E4d-dag-links": "check_dag E4 PASS (" + S + "check_dag_E4.txt); 39 links checked, 0 problems (" + S + "links_r13.txt); the concept links to L06 and L07 resolve (L06.html:169, L07.html:62).",
    "E4d-registry-muth": "references/references.json has muth1961rational (line 17660); live verify_refs --unit E4 covers the unit's 3 entries with 0 problems.",
    "E4d-registry-milgrom": "references/references.json has milgrom1982information (line 17292); live verify_refs --unit E4: 0 problems.",
    "E4d-cites-only-registry": "The page's data-cite values (project.html reading list) are muth1961rational and milgrom1982information only (grep data-cite); both are registry keys.",
    "E4d-spec-context-sentences": "Context has four sentences (project.html Context dd), within plan 5.2 (2 to 4 sentences).",
    "E4d-spec-questions": "Inputs, Required outputs, Constraints, Grading mode and Reading list (project.html:314-322) state the interface, both named conditions, the accuracy domain, the stop rule and the report files. No clarifying question needed beyond those stated.",
    "E4d-spec-ladder": "Rung 1 solved and annotated (Lab 1 with step notes); rung 2 completion (blank return line, run_labs completion rule); rung 3 specification; rung 4 stretch open-ended (project.html:669-675).",
    "E4d-prose-scope-words": "Exception table paragraph (project.html:327) states the accuracy domain and the not-named range. Scope words at lines 37, 53, 62, 171, 244, 257-262, 287, 315, 317, 377, 608, 630, 656 each have a computation, a derivation or an explicit hypothesis (checked by reading).",
    "E4d-prose-simulated-labs": "project.html lines 57, 176, 314 and 375 label the labs and the instance SIMULATED; the lab code uses stated inputs, not draws.",
    "E4d-prose-simulated-exemplars": "The exemplar intro (project.html:530) states the instance is SIMULATED.",
    "E4d-hours-project": "data-hours-project=28 (project.html:33); hub index.html:29 data-hours-project=28 and data-hours-lessons=72; hub 'Tier M · 100 hours'; curriculum.json E4 hours 100 = 72 + 28.",
    "E4d-hours-estimate": "Own estimate: rung 1 1 h, rung 2 1 h, derivation 5-8 h, solver and tests 6-10 h, grid 2-4 h, write-up 4-6 h, self-assessment 2-3 h: 21-33 h; declared 28 h is within 30%.",
    "E4d-rubric-observable": "All 20 level descriptors (project.html rubric table, #rubric) read: each names something a grader can see; none vague.",
    "E4d-exemplar-annotations-hidden": "Exemplar verdicts and annotations carry data-reveal or class annotation (project.html exemplars); rubric.js setRevealed() hides '.annotation, [data-reveal]' (course/assets/js/rubric.js:147-150).",
    "E4d-grader-exceptions": "must_raise is used only for the two named conditions (test_project.py:191-233); reference._check_inputs raises the named ValueErrors (reference.py:26-34).",
    "E4d-grader-messages": "Every expect() and pytest.fail() message names the property and carries no expected value (test_project.py:49-68 and all call sites read).",
    "E4d-grader-oracle": "oracle_* functions (test_project.py:79-170) do not import the solver; the oracle gap at 0 equals the closed-form limit to 1.11e-16 (" + S + "check_docstrings_out.txt).",
    "E4d-grader-instances": "instance.py draws within [0.500,0.750] and [0.120,0.150] rounded to 3 dp; seeds 0-49: 50/50 valid, interior, distinct, deterministic (" + S + "instances_r13.txt).",
    "E4d-grader-instance-docstring": "instance.py:14-17 numbers recomputed: 0.09762327..., 0.23756678..., 0.30769... (rederive_r13.txt section 6).",
    "E4d-grader-test-docstring": "gap-at-zero docstring (test_project.py:383-386): |gap(1e-12) - limit| = 1.02e-13..3.54e-13 and oracle-limit <= 1.11e-16 (" + S + "check_docstrings_out.txt). Tiny-root docstring: root 2.0224e-51 at tau_bar 0.010122 (same file).",
    "E4d-grader-stdlib": "test_solver_imports_only_the_standard_library passes for the reference and all alternatives (" + S + "candidates_0_49.txt).",
    "E4d-runtime": "run_graders slowest 0.3 s (run_graders_E4_0_49.txt); in-browser suite 0.8 s (page_smoke_E4_project_alone.txt).",
    "E4d-browser-local-parity": "Local pytest: 48 passed (reference, scratch copy); page_smoke in-browser: 'All 48 tests pass'.",
    "E4d2-exemplar-B-C1-annotation": "Exemplar B Model passage lists Assumptions 1 to 6 with the propositions that use them (project.html Exemplar B); the C1 level 4 annotation matches.",
    "E4d3-cara-defined-twice": "A3 cites Definition 6.2 of Lesson 6 (project.html:259); L06.html:57 and :66 hold the definition. The project does not redefine it.",
    "E4d3-anchors-links": "links_r13.txt: 39 links checked, 0 missing files or anchors.",
    "E4d3-no-figures-no-data": "grep of project.html: no <svg>, <img> or data-files; the labs read no file.",
    "E4d3-atlas-studios-na": "atlas/ and studios: git diff 5db69a9..e919577 empty; the E4 page has no atlas path (plan section 8).",
    "E4d-mutants-existing": "tools/mutate_graders.py --unit E4 --seeds 0-9 (final): 116/116 KILLED, exit 0 (" + S + "mutate_E4_0_9_final.txt).",
    "E4d-mutants-new": "mutant_r7_02 and mutant_r7_03 KILLED (mutate_E4_0_9_final.txt).",
    "E4d2-mutants-r2": "mutant_r2_* KILLED (mutate_E4_0_9_final.txt).",
    "E4d3-mutants-r3": "mutant_r3_* KILLED (mutate_E4_0_9_final.txt).",
    "E4d3-mutant-tolerance-survives": "mutant_r3_tolerance_1e-9 KILLED (mutate_E4_0_9_final.txt). The old survivor note is historical.",
    "E4d-equivalent": "literal_price_sign.py and the three stop-rule variants pass seeds 0-49 50/50 (" + S + "equivalent_candidates_0_49.txt); each differs from reference.py by a one-line edit (diff read).",
    "E4d-alternatives": "alt_1.py..alt_5.py PASS 50/50 seeds 0-49 (" + S + "candidates_0_49.txt). Plan-list coverage is a separate FAIL row (E4d13-alternatives-plan-list).",
    "E4d-starter": "starter.py fails 0/50 seeds (" + S + "candidates_0_49.txt): the suite fails on the empty implementation.",
    "E4d4-alt4-wrong-on-small-noise": "alt_4.py PASS 50/50 seeds 0-49 (" + S + "candidates_0_49.txt): the round-4 small-noise problem no longer appears.",
    "E4d4-alt1-docstring": "alt_1.py docstring (lines 1-3): bisection with relative width 1e-12 or at most 240 halvings; matches the code (lines 78-87).",
    "E4d4-equivalent-price-slope": "literal_price_sign.py differs from reference.py only at line 58 (sign of b_u); b_u enters only as b_u*b_u (reference.py:73). Passes 50/50.",
    "E4d4-proposed-test-validated": "test_project.py:531-578 (small-noise, tiny-noise, corner and near-zero-cost accuracy tests) pass on the reference (48 passed) and kill mutant_r12_04.",
    "E4d4-exemplar-B-results-numbers": "Exemplar B results (project.html Exemplar B, 'Results and comparative statics') equal the Lab 3 output (" + S + "twin_p3.out).",
    "E4d4-mutants-killed-r4": "mutant_r4_* (mutant_r4_absolute_bracket_tolerance, r4_informed_precision_signal_only, r4_uninformed_variance_uses_signal_precision, r4_unit_fraction_reports_precision, r4f_*) KILLED (mutate_E4_0_9_final.txt).",
    "E4d5-mutant-bracket-floor": "mutant_r5_bracket_floor_1e-12 KILLED (mutate_E4_0_9_final.txt).",
    "E4d5-mutant-sixty-halvings": "mutant_r5_sixty_halvings_no_tolerance KILLED (mutate_E4_0_9_final.txt).",
    "E4d5-mutant-uninformed-precision": "mutant_r5_uninformed_posterior_precision_informed KILLED (mutate_E4_0_9_final.txt).",
    "E4d6-mutant-06": "mutant_r6_06_cost_scales_whole_gap KILLED (mutate_E4_0_9_final.txt).",
    "E4d6-mutant-07": "mutant_r6_07_unit_informativeness_discounted_by_cost KILLED (mutate_E4_0_9_final.txt).",
    "E4d6-mutants-new-killed": "mutant_r6_0* KILLED (mutate_E4_0_9_final.txt).",
    "E4d6-spec-variants-08-09": "equivalent/mutant_r6_08 (lower end) passes 50/50 and is inside the 1e-10 requirement; mutants/mutant_r6_09_always_200_halvings KILLED by the corner test (mutate_E4_0_9_final.txt).",
    "E4d6-stop-rule-measured": "Round-11 log (logs/check_corner_cap200_fix11.txt: 1.5322e-10 at sd=1e-50, c=0.17076911209224613) reproduced at full cost digits (" + S + "readme_corner_repro_r13.txt).",
    "E4d6-alt-extra-damped": "scripts/E4-d-r6/candidates/damped_fixed_point_log_r6.py FAILS 0/50 (" + S + "prior_alts_0_49_r13.txt) on the near-zero-cost, corner and tiny-root accuracy tests, as recorded. It is a documented wrong damped iteration, not an accepted alternative.",
    "E4d6-rung1-why": "Lab 1 interpretation (project.html Lab 1, interpretation paragraph) names the reason for each step and the proposition it checks.",
    "E4d7-midpoint-untested": "The Constraints (project.html:318) do not require the midpoint; the lower-end variant meets the 1e-10 requirement (equivalent/README.md). Exemplar B's method text names the midpoint; recorded as an architect item in notes, not a failing grader row.",
    "E4d7-cost-above-one-rejected": "test_info_cost_above_one_is_accepted and test_info_cost_far_above_one_is_accepted[10.0, 50.0] pass on the reference; mutant_r7_03 KILLED.",
    "E4d7-noise-above-one-rejected": "test_noise_volume_far_above_one_is_accepted[50.0, 1000.0] pass on the reference; mutant_r7_02 KILLED.",
    "E4d7-alt5-docstring": "alt_5.py docstring (lines 1-2) says precision parameterisation with the same bracket [0,1]; accurate to the code (bracket at alt_5 solve_model).",
    "E4d7-lab1-bracket-width": "Lab 1 interpretation: width 2^-53 = 1.110e-16 from the 53rd halving, the ulp of [0.5,1); printed width 1.110e-16 (run_labs passes).",
    "E4d7-lab2-blank": "Lab 2: only the return line is blank; completion rule passes (run_labs_E4_project.txt); the interpretation (project.html Lab 2) is consistent.",
    "E4d7-instance-bound": "instance.py:14-17 and project.html:315 bounds recomputed (rederive_r13.txt section 6); instances_r13.txt 50/50 interior.",
    "E4d7-lab3-closed-form-sentence": "Lab 3 hypothesis (project.html Lab 3): largest bisection-closed form difference 2.1e-13 (twin_p3.out) <= 1e-12 as claimed.",
    "E4d7-test-count": "project.html:320 says 48 checks; pytest --collect-only = 48.",
    "E4d8-no-upper-bound": "The page names no upper noise bound (project.html:327); tests use sd 50 and 1000; the reference returns finite outputs at sd=1e150 and cost 350 (extremes_r13.txt).",
    "E4d8-cap-100-survives": "mutant_r8_01_cap_100_halvings KILLED (mutate_E4_0_9_final.txt).",
    "E4d8-noise-cap-10-survives": "mutant_r8_02_noise_above_ten_rejected KILLED (mutate_E4_0_9_final.txt).",
    "E4d8-cost-cap-5-survives": "mutant_r8_03_cost_above_five_rejected KILLED (mutate_E4_0_9_final.txt).",
    "E4d8-mutants-r8-killed": "mutant_r8_04_integer_zero_fraction and mutant_r8_05 KILLED (mutate_E4_0_9_final.txt).",
    "E4d8-tiny-root-reference": "Reference at sd 1e-40 and 1e-50 matches the closed form (accuracy_sweep_r13.txt; check_docstrings_out.txt corner root 2.02238544e-51).",
    "E4d8-lab3-twin-page": "Lab 3 page code equals the twin (run_labs passes); expected output equals twin output (twin_p3.out).",
    "E4d9-mutant-v9-02": "equivalent/mutant_v9_02_stop_rule_relative_to_lower_end.py passes 50/50 (equivalent_candidates_0_49.txt).",
    "E4d9-mutant-v9-06": "mutants/mutant_v9_06_gap_at_zero_from_tiny_fraction.py KILLED (mutate_E4_0_9_final.txt).",
    "E4d9-equivalent-r6-08-09-docstrings": "equivalent/mutant_r6_08 docstring says it reports the lower end; mutants/mutant_r6_09 docstring says 200 halvings; both accurate.",
    "E4d9-mutants-v9-killed": "mutant_v9_01, _03, _05, _07 KILLED (mutate_E4_0_9_final.txt).",
    "E4d9-mutant-docstrings": "All 116 mutant docstrings are non-empty and their first lines name an error (" + S + "mutant_docstrings_r13.txt).",
    "E4d10-delta-A1-prior-mean": "A1 read (project.html:257) and its shift argument re-derived (utility depends on v-p only).",
    "E4d10-delta-inputs-interior-root": "project.html Inputs: the interior-root claim for the generator box is re-derived (rederive_r13.txt section 6) and holds for seeds 0-49 (instances_r13.txt).",
    "E4d10-delta-constraints-gap-at-zero": "project.html:318 gap-at-zero clause (1e-14) is enforced by test_gap_at_zero_fraction_is_the_limit_to_full_precision and the reference passes (check_docstrings_out.txt).",
    "E4d10-delta-grading-mode-43": "project.html:320 says 48 checks; pytest --collect-only = 48.",
    "E4d10-delta-results-ratio": "project.html Exemplar B ratios: unrounded 1.25 and 1.50 exact; displayed 0.6978/0.5582 = 1.250090 -> 1.2501 (rederive_r13.txt section 4).",
    "E4d10-new-test-numbers": "test_project.py docstring numbers verified (check_docstrings_out.txt; readme_corner_repro_r13.txt).",
    "E4d10-mutants-new-r10": "mutant_r10_01..04 KILLED (mutate_E4_0_9_final.txt).",
    "E4d10-alternatives-r10": "alt_1..alt_5 PASS 50/50 (candidates_0_49.txt).",
    "E4d10-l06-dependency": "L06.html:169 (def-noisy-rational-expectations-equilibrium), L06.html:57 and :66 (Definition 6.2), L07.html:62 (def-price-informativeness) exist; links_r13.txt 0 problems.",
    "E4d10-lab3-numbers": "Lab 3 printed numbers equal rederive_r13.txt section 4 (unrounded lambda* 0.5582027280, 0.6977534100, 0.8373040920 ...).",
    "E4d11-delta-hunks": "Full project.html, test_project.py, reference.py and instance.py read in round 13; every number in the hunks named here re-derived (rederive_r13.txt; check_docstrings_out.txt).",
    "E4d11-constraints-wording": "project.html:318 numbers (1e-14, 1e-12, 240 halvings, 1e-10, 1e-50, 1e-2) match tests and reference; accuracy_sweep_r13.txt worst 4.95e-13.",
    "E4d11-oracle-precision": "oracle_gap at 0 agrees with the closed form to 1.11e-16 (check_docstrings_out.txt).",
    "E4d11-mutants-new-r11": "mutant_r11_01..04 KILLED (mutate_E4_0_9_final.txt).",
    "E4d11-alt-closed-form": "scripts/E4-d-r11/alts/alt_r11_a.py PASS 50/50 (prior_alts_0_49_r13.txt); file unchanged since 5db69a9.",
    "E4d11-literal-price-sign-open": "literal_price_sign.py: only b_u's sign differs (reference.py:58); b_u enters only as b_u*b_u (reference.py:73); passes 50/50. Open architect item recorded in notes; not a grader fault.",
    "E4d11-lab-page-twin": "run_labs: each project page lab equals its twin byte for byte and its expected block equals the output (run_labs_E4_project.txt).",
    "E4d11-plan-tolerance-documented": "project.html:318 states the tolerance 1e-12 and 240 halvings; plan rule 12 (E4-build-plan section 2.1 item 12) asks for bracket, tolerance, stop rule and sign-change assumption: all present with A6 (project.html:262).",
    "E4d11-mutant-r10-02": "mutant_r10_02_cost_factor_relative_error KILLED (mutate_E4_0_9_final.txt).",
    "E4d12-alt-variants-new": "scripts/E4-d-r12/alts/alt_r12_a.py, alt_r12_b.py, alt_r12_c.py PASS 50/50 (prior_alts_0_49_r13.txt); the files changed between 5db69a9 and e919577, so re-run.",
    "E4d12-corner-test-docstring": "test_corner_root docstring: root about 2e-51 (2.0223854e-51 reproduced) and 200 halvings give a bracket 6.2e-61 > 1e-10 times the root 2.0e-61 (rederive_r13.txt section 6).",
}

NEW_ROWS: list[dict[str, str]] = []


def new(rid: str, check: str, location: str, status: str, evidence: str, fix: str | None = None) -> None:
    row = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        row["fix"] = fix or ""
    NEW_ROWS.append(row)


new("E4d13-endpoint-gap-precision", "2.6-grader", "course/modules/E/E4/grader/test_project.py:419-450 (test_unit_fraction_is_reported_at_zero_cost, ..._with_a_positive_cost); course/modules/E/E4/project.html:316 and :318", "FAIL",
    "Probe " + S + "probe_endpoint_gap_r13.py (reference with the gap at lambda* = 1 read at 1 - 1e-12) PASSES 10/10 seeds (probe_endpoint_gap_r13.txt): the tests use TOL_GAP 1e-8 at fraction 1. project.html:316 says indifference_gap is 'the gap of Proposition 3 at lambda*' and :318 says 'the solver works in floating point at full precision'. The reference's gap at 1 agrees with the oracle to 1.11e-16 (endpoint_oracle_check_r13.txt), so a 1e-14 check is passable. The same deviation at an interior root (probe_interior_gap_zero_r13.txt) IS killed, so the precision requirement is enforced in the interior only.",
    "Add to both fraction-1 tests: abs(out['indifference_gap'] - oracle_gap(1.0, sd, cost)) <= 1e-14 * max(1.0, abs(oracle_gap(1.0, sd, cost))). Add the same bar to the informativeness at 1 (the reference matches). Re-run the mutate gate with probe_endpoint_gap_r13.py as a new mutant once it is written into ledgers/E4/mutants/.")
new("E4d13-alternatives-plan-list", "2.6-alternatives", "ledgers/E4/alternatives/alt_4.py (docstring line 1); ledgers/E4/alternatives/alt_5.py (docstring lines 1-2); plans/E4-build-plan.md section 5.5 items 2, 4, 5", "FAIL",
    "Plan 5.5 lists five alternatives: 1 bisection, 2 Brent or secant with a sign check, 3 grid then bisection, 4 damped fixed-point iteration with a convergence check, 5 precision parameterisation with a DIFFERENT bracket. Present: alt_1 (bisection), alt_2 (Illinois), alt_3 (grid then bisection), alt_4 (safeguarded secant, so a second item-2 member), alt_5 (precision parameterisation with the SAME bracket [0,1]). Item 4 is absent. A naive damped fixed-point (" + S + "alts/alt_r13_damped_fixed_point.py, with Aitken) FAILS 0/50 (candidate_damped_0_49.txt): relative error 1.8e-7 at (sd 1e-50, cost 1e-6) and 1.2e-5 at (1e-40, 1e-4) (alt_damped_error_probe.txt). The round-6 damped candidate also fails 0/50 (prior_alts_0_49_r13.txt). The suite correctly rejects both; the plan's item 4 is not implementable as written without acceleration near tau_bar = 1.",
    "Architect ruling needed: either record that alt_4 (secant) substitutes for item 4 and that alt_5 uses bracket [0,1] (amend plan 5.5), or add a damped fixed-point alternative with acceleration that passes seeds 0-49 and the 1e-10 clause at cost near 0, as ledgers/E4/alternatives/alt_9.py.")
new("E4d13-readme-corner-domain", "2.2-numbers", "ledgers/E4/equivalent/README.md (section 'Stop-rule variants', paragraph 2)", "FAIL",
    "README: 'Measured on 90000 cases in the domain's corner (noise volume 1e-50 to 1.06e-50, cost with tau-bar at least 1e-2)'. The round-11 scan (ledgers/E4/scripts/E4-d-fix-r11/check_corner_accuracy_fix11.py) covers sd = 1e-50*(1+0.002 i), i < 300, i.e. 1.000e-50..1.598e-50, and costs with tau-bar in 0.010000..0.012022 (" + S + "readme_corner_repro_r13.txt). The cited cost '0.17076911209' is truncated: at full digits 0.17076911209224613 the cap-200 error is 1.5322e-10 (as stated), but at the truncated value it is 8.0e-12 (" + S + "readme_corner_repro_r13.txt). Confirmed: 11598 cases, cap-200 max 1.5322e-10, cap-240 max 5.1420e-13 (" + S + "readme_grid_cap240_r13.txt). Also 209 halvings to reach 1e-12 relative at 2e-51 (readme_claims_r13.txt).",
    "Change '1.06e-50' to '1.598e-50' and 'tau-bar at least 1e-2' to 'tau-bar from 0.0100 to 0.0121' (or extend the scan to the stated domain and re-log), and write the cited cost as 0.17076911209224613.")
new("E4d13-independent-rederivation", "2.2-numbers", "course/modules/E/E4/project.html (Labs 1-3, Propositions 1-5, lede); course/modules/E/E4/grader/instance.py:14-17", "PASS",
    "ledgers/E4/scripts/E4-d-r13/rederive_r13.py (output rederive_r13.txt): gap from Gaussian quadratic forms and covariance-based clearing agrees with the page formula to 3.3e-16; Corr^2 to 5.6e-17; Lab 1, Lab 2 and Lab 3 numbers reproduced; box bounds reproduced; 2^-240 = 5.6598e-73.")
new("E4d13-accuracy-sweep", "2.6-autograder", "course/modules/E/E4/grader/reference.py; course/modules/E/E4/project.html:318", "PASS",
    "ledgers/E4/scripts/E4-d-r13/accuracy_sweep_r13.py (accuracy_sweep_r13.txt): 4000 random inputs, sd log-uniform in [1e-50, 1e3], cost in [0, 0.1725]; 3961 with tau_bar >= 1e-2, 3706 interior; worst relative error 4.95e-13 < 1e-10. The page's accuracy clause holds for the reference over a wider domain than the round-11 grid.")
new("E4d13-extreme-inputs", "2.4-scope", "course/modules/E/E4/project.html:316-318, :327; grader/reference.py", "PASS",
    "ledgers/E4/scripts/E4-d-r13/extremes_r13.py (extremes_r13.txt): sd 1e150 at cost 0.13 gives lambda 1 (tau_bar > tau_y(1)), finite outputs; sd 1e150 at cost 350 gives lambda 0, finite gap -3.6e153; sd 1 at cost 350 finite. Below 1e-50 the outputs are inaccurate (sd 1e-300 gives lambda 2.83e-73, informativeness 0.5, gap -0.297), which the page discloses (:327: 'may return an inaccurate value'). Pass on the stated scope; see notes for the fail-loud option.")
new("E4d13-instances-seeds-0-49", "2.6-autograder", "course/modules/E/E4/grader/instance.py; course/modules/E/E4/grader/test_project.py:37-40", "PASS",
    "ledgers/E4/scripts/E4-d-r13/instances_r13.py (instances_r13.txt): seeds 0-49 are valid, deterministic, within the documented ranges, interior at the reference (50/50), with 50/50 distinct instances and 50/50 distinct fractions. Sample of 20 printed.")
new("E4d13-candidates-accepted", "2.6-autograder", "ledgers/E4/alternatives/alt_1..alt_8.py; ledgers/E4/equivalent/*.py; course/modules/E/E4/grader/starter.py", "PASS",
    "ledgers/E4/scripts/E4-d-r13/run_candidates.py (candidates_0_49.txt; equivalent_candidates_0_49.txt; prior_alts_0_49_r13.txt): reference, alt_1..alt_8 pass 50/50 each; starter fails 0/50; the four equivalent variants pass 50/50. The grader does not reject any correct implementation it was given.")
new("E4d13-new-mutants", "2.6-mutation", "ledgers/E4/mutants/mutant_r13_01..04_*.py", "PASS",
    "Four new student-error mutants written from reference.py by ledgers/E4/scripts/E4-d-r13/make_mutants_r13.py: r13_01 closed-form root drops the CARA factor (KILLED by test_indifference_holds_at_an_interior_fraction[first]); r13_02 informativeness omits the price-noise variance (KILLED by test_informativeness_is_the_squared_correlation[first]); r13_03 boundary fraction returned as int (KILLED by test_info_cost_zero_is_accepted); r13_04 informed demand price sign flipped (KILLED by test_gap_is_the_oracle_gap_at_the_reported_fraction[first]). Run on seeds 0-9 (new_mutants_0_9.txt) and in the full gate.")
new("E4d13-mutant-gate-final", "2.6-mutation", "ledgers/E4/mutants/ (116 files); tools/mutate_graders.py", "PASS",
    "tools/mutate_graders.py --unit E4 --seeds 0-9 (mutate_E4_0_9_final.txt): 116/116 KILLED, exit 0. The round-12 survivor mutant_r12_04 is now killed by test_root_is_relatively_accurate_at_a_cost_near_zero[1e-50-1e-06].")
new("E4d13-notation", "2.4-notation", "course/modules/E/E4/project.html (notation paragraph, Lemmas, Propositions); notation/notation.json", "PASS",
    "grep: no \\ast, \\mathbb, \\Phi, \\gamma (plain or subscripted), \\Q, R_f or R^{e\\ast} on the page; \\E, \\Var, \\Cov, \\Corr, \\Normal are the registered macros; sigma, tau, Omega, lambda, V_I, V_U, hat x are not registered symbols, and no registered symbol is reused with another meaning.")
new("E4d13-links", "2.9-structure", "course/modules/E/E4/project.html", "PASS",
    "links_r13.txt: 39 href/src values checked; 0 missing files, anchors or target ids.")
new("E4d13-hours-arithmetic", "2.9-hours", "course/modules/E/E4/project.html #hours (:341-352); course/modules/E/E4/index.html:29-31", "PASS",
    "Hours table 1+1+5+8+5+5+3 = 28 equals data-hours-project=28; hub 72 lesson + 28 project = 100 = 'Tier M · 100 hours' and curriculum.json hours 100.")
new("E4d13-lab-twins-direct", "2.5-labs", "tests/labs/E4/lab-E4-project-1.py, -2.py, -3.py", "PASS",
    "Each twin run as `.venv/bin/python -I -W error <twin>`: exit 0 (twin_p1.out, twin_p2.out, twin_p3.out). Twin output equals the page expected block (run_labs passes).")
new("E4d13-exemplar-numbers-arith", "2.2-numbers", "course/modules/E/E4/project.html Exemplar B Results passage (table and ratios)", "PASS",
    "Table values equal Lab 3 printed rows; sigma-proportionality holds exactly unrounded (1.25, 1.50); the lambda-equals-closed-form claim holds to 2.1e-13 (rederive_r13.txt section 4).")

# ---------- assemble
rows: list[dict[str, str]] = []
for prev in PREV["rows"]:
    rid = prev["id"]
    if rid in OVERRIDE:
        status, evidence, fix = OVERRIDE[rid]
    elif prev["status"] == "PASS":
        if rid not in PASS_EVIDENCE:
            raise SystemExit(f"no round-13 evidence for PASS row {rid}")
        status, evidence, fix = "PASS", PASS_EVIDENCE[rid], None
    else:
        raise SystemExit(f"non-PASS row without override: {rid}")
    row = {"id": rid, "check": prev["check"], "location": prev["location"], "status": status, "evidence": evidence}
    if status != "PASS":
        row["fix"] = fix or ""
    rows.append(row)
rows += NEW_ROWS

# mutants from the final gate
mutants = []
for line in (ROOT / S / "mutate_E4_0_9_final.txt").read_text(encoding="utf-8").splitlines():
    m = re.match(r"^(KILLED|SURVIVED) (\S+?): (.*) -> (.*)$", line)
    if not m:
        continue
    name, desc, killed = m.group(2), m.group(3), m.group(4)
    if m.group(1) != "KILLED":
        raise SystemExit("survivor: " + name)
    mutants.append({"name": name, "description": desc, "killed_by": killed.strip()})
if len(mutants) != 116:
    raise SystemExit(f"expected 116 mutants, got {len(mutants)}")

counts = {"PASS": 0, "FAIL": 0, "UNVERIFIABLE": 0}
for r in rows:
    counts[r["status"]] += 1
verdict = "PASS" if counts["FAIL"] == 0 and counts["UNVERIFIABLE"] == 0 else "FAIL"

frag = {
    "unit": "E4",
    "slice": "d",
    "round": 13,
    "verifier": "Haiku independent verifier, E4 slice d, round 13 (did not build E4; checkout pinned at e919577)",
    "pin": "e919577b45b431ce68e1e6533b00b8a301277937",
    "base": "5db69a9bee460736c318ebfacc7200ee5a6eb0f0 (round-12 pin). Delta in slice d: project.html (35 lines), grader/instance.py, grader/reference.py, grader/test_project.py (13 added lines), ledgers/E4/alternatives/alt_6..8.py (new), equivalent/literal_price_sign.py and three stop-rule variants (one line each), mutants f11_* and r6_09 (comment lines), mutants f12_* and r12_* (new). Every hunk read.",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE13-E4-d",
    "scratch": "/tmp/e4d13-* (removed after use)",
    "verified_at": "2026-11-05T17:10:00+00:00",
    "verdict": verdict,
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Gates re-run at e919577: run_graders E4 0-49 PASS (50/50); mutate_graders E4 0-9 116/116 KILLED; check_projects, check_pages, check_dag PASS; run_labs project 3/3 and unit 12/12 PASS; page_smoke project PASS (48 in-browser tests); ruff check and format PASS; mypy --no-incremental PASS (385 files); pytest relevant subset PASS; verify_refs offline 0 problems and live E4 0 problems; collect-only 48.",
        "Calibration (blind scoring of Exemplars A and B) is UNVERIFIABLE again: the verifier has read the annotations. This is the only reason the exemplar rows are not PASS.",
        "Architect item (not a row): the stop-rule variants in ledgers/E4/equivalent (lower-end reporting) are inside the 1e-10 requirement, but Exemplar B's method text (project.html Exemplar B, Method) says 'the reported fraction is the midpoint of the final bracket'. Architect to decide whether the page should pin the reported point.",
        "Architect item (not a row): the literal_price_sign variant is output-identical (b_u enters only as b_u*b_u). Proposition 1's sign is stated on the page but cannot be tested; the architect decides whether to keep the sign statement or remove it (equivalent/README.md).",
        "Architect item (not a row): below sigma = 1e-50 the solver silently returns inaccurate outputs (e.g. sigma 1e-300: informativeness 0.5, gap -0.297). The page discloses this (project.html:327); a fail-loud rule below 1e-50 is a design choice for the architect.",
        "Plan drift noted in E4d13-alternatives-plan-list: alt_5's bracket differs from plan 5.5 item 5, and item 4 is missing; the naive damped fixed point fails the accuracy clause at cost near zero.",
        "Round-8 and round-9 alternative citations (E4d8-alternatives-r8, E4d9-alternatives-v9) are UNVERIFIABLE because those files do not exist at this pin and no current file cites them.",
        "Not checked: Lessons L01-L05 and L07-L09, cards.json and the other pages (outside slice d); the Pyodide interpreter itself (page_smoke runs the repo's in-browser harness); a blind score of the two exemplars (impossible for this verifier); the length of the report (350-800 words) and the human-readability of the rubric; live Crossref for the whole registry (only the unit's entries).",
    ],
    "summary": {
        "rows": len(rows),
        "pass": counts["PASS"],
        "fail": counts["FAIL"],
        "unverifiable": counts["UNVERIFIABLE"],
        "mutants": len(mutants),
        "mutants_killed": len(mutants),
    },
}
out = ROOT / "ledgers/E4/E4-d.json"
out.write_text(json.dumps(frag, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("rows", len(rows), counts, "mutants", len(mutants), "verdict", verdict)
