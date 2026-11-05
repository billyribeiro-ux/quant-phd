"""Compose ledgers/E4/E4-d.json (round 10) from the round-9 rows, the round-10 re-checks and the mutation log.

Run: python3 -I compose_fragment_r10.py <repo-root>
"""
import datetime
import json
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
prev = json.load(open("/Users/billyribeiro/.fanout/frags/E-E4-d.round9.json", encoding="utf-8"))
LOG = root / "ledgers/E4/scripts/E4-d-r10/logs"
CARRY_PIN = "project.html lines byte-identical since the previous pin (delta hunks at :257, :314, :318, :320, :629 only)"

fresh = {}   # id -> (status, evidence, fix)
def F(i, ev, status="PASS", fix=None):
    fresh[i] = (status, ev, fix)

def C(i, files, ev=None, status="PASS", fix=None):
    """carry a round-9 PASS row: the subject is byte-identical since the previous pin"""
    base = ev or next(r["evidence"] for r in prev["rows"] if r["id"] == i)
    fresh[i] = (status or "PASS", f"Carried from round 9 ({files} byte-identical since the previous pin): " + base, fix)

# ---- command rows: re-run this round ----
F("E4d-cmd-check-projects", "`.venv/bin/python tools/check_projects.py --unit E4` -> 'check_projects E4: PASS', exit 0 (ledgers/E4/scripts/E4-d-r10/logs/check_projects.txt).")
F("E4d-cmd-check-pages", "`tools/check_pages.py --unit E4` -> 'check_pages E4: PASS', exit 0 (logs/check_pages.txt).")
F("E4d-cmd-check-dag", "`tools/check_dag.py --unit E4` -> 'check_dag E4: PASS', exit 0 (logs/check_dag.txt).")
F("E4d-cmd-run-labs", "`tools/run_labs.py --unit E4` -> 'run_labs E4: PASS (12/12)', exit 0 (logs/run_labs.txt).")
F("E4d-cmd-run-graders", "`tools/run_graders.py --unit E4 --seeds 0-49` -> 'run_graders E4: PASS (reference 50/50 seeds, slowest 0.5 s)', exit 0 (logs/run_graders.txt).")
F("E4d-cmd-page-smoke-project", "`tools/page_smoke.py --unit E4 --pages project` run alone -> 'in-browser grader: All 43 tests pass on seed 792521633. (0.9 s)', 'page_smoke E4: PASS', exit 0 (logs/page_smoke_project.txt). Round 9 said 42 tests; the new test is in the suite.")
F("E4d-cmd-ruff", "`.venv/bin/python -m ruff check course/modules/E/E4 tests/labs/E4` -> 'All checks passed!', exit 0; `ruff format --check` -> '16 files already formatted', exit 0 (logs/ruff_check.txt, logs/ruff_format.txt).")
F("E4d-cmd-mypy-workspace", "`.venv/bin/python -m mypy --no-incremental course/modules/E/E4/grader tests/labs/E4` -> 'Success: no issues found in 16 source files', exit 0 (logs/mypy.txt).")
F("E4d-cmd-mypy-plan-command", "Same mypy run as E4d-cmd-mypy-workspace (logs/mypy.txt).")
F("E4d-cmd-pytest-relevant", "`.venv/bin/python -m pytest -q tests/test_memo_exemplars.py tests/test_page_checks.py tests/test_labs.py tests/test_run_labs.py` -> all dots, exit 0 (logs/pytest_relevant.txt).")
F("E4d-cmd-verify-refs", "`tools/verify_refs.py --offline` -> 'offline integrity: 560 entries, 0 problems', exit 0 (logs/verify_refs_offline.txt). references/ is byte-identical since the previous pin, so no live run was needed.")
F("E4d-cmd-collect", "Scratch copy /tmp/e4r10ref (instance.py, test_project.py, reference.py as solver.py): `pytest --collect-only -q` -> '43 tests collected' (logs/collect.txt). Equals the page's '43 checks' (project.html:320). Round 9 counted 42; the delta added one test.")
F("E4d-lab-project-1", "Page code equals the twin line for line (98 vs 98 lines, 0 differing); twin run `python -I -W error` exit 0, stderr 0 bytes; output equals the expected block (logs/lab_twin_check_r10.txt).")
F("E4d-lab-project-2", "Page code (63 lines) differs from the twin only at the blanked return line (`return ___` vs `return f_u - math.exp(A * COST) * f_i`); twin run `-I -W error` exit 0; output equals the expected block (logs/lab_twin_check_r10.txt).")
F("E4d-lab-project-3", "Page code equals the twin (114 vs 114 lines, 0 differing); twin run `-I -W error` exit 0; output equals the expected block (logs/lab_twin_check_r10.txt).")
F("E4d-num-lab-hypotheses", "Lab 1 hypothesis values (+0.053092, -0.080731, 0.57937525, -3.45199422, 0.18904110, 0.15898618) equal the Lab 1 expected block (project.html:156-170). Lab 2 values (+0.037435, -0.071386, 0.57052263, 0.12466375) equal its expected block (:240-243). Lab 3 hypothesis values equal its expected block (:491-502). Re-run through the twins this round (logs/lab_twin_check_r10.txt).")
F("E4d-num-exemplar-table", "Exemplar B table (project.html:633-641) equals the Lab 3 printed rows (logs/lab_twin_check_r10.txt). Ratios from the unrounded fractions: 1.249999999999898 and 1.500000000000611 (logs/numbers_r10.txt, script ledgers/E4/scripts/E4-d-r10/numbers_r10.py). Displayed-value ratios 0.6978/0.5582 = 1.25009 -> 1.2501 and 0.8373/0.5582 = 1.50000 -> 1.5000, as the sentence at :629 says. Largest gap printed 3.55e-14 < 4e-14.")
F("E4d-num-box-bounds", "Recomputed this round (logs/numbers_r10.txt): tau_bar(0.150) = 2e^-0.6 - 1 = 0.0976232722, tau_bar(0.120) = 2e^-0.48 - 1 = 0.2375667836, 1/(1+4*0.75^2) = 0.30769231 (logs/numbers_r10.txt). Matches project.html:314 to the printed digits and instance.py:1-21.")

# ---- math: re-derived this round ----
F("E4d-prose-lede-directional", "Lede (project.html:37, byte-identical since the previous pin) re-checked this round against Prop 4 (lambda* = a sigma k(tau_bar), linear in sigma, so the fraction rises with the noise on the interior) and Prop 2/4 (informativeness tau_bar/(tau_v+tau_bar) has no sigma), and against Lab 3: at each cost the informativeness is the same at every noise volume (0.1920, 0.1420, 0.0889). Holding lambda fixed, tau_y = lambda^2 tau_e^2/(lambda^2 tau_e + a^2 sigma^2) falls in sigma, so the price is less informative for more noise at a fixed fraction, as the lede says.")
F("E4d-math-lemmas", "Re-derived by hand this round (project.html:265-273): Lemma 1 (g(x*) = (m-p)^2/(2aV), -a g(x*) = -(m-p)^2/(2V)); Lemma 2 (integral gives (V/(V+S))^(1/2)); Lemma 3 (law of total variance). Lines byte-identical since the previous pin.")
F("E4d-math-prop1", "Re-derived this round (project.html:276-283): step (3) coefficient on u is -lambda tau_e kappa - a, so kappa = -a/(lambda tau_e); tau_y = lambda^2 tau_e^2/(lambda^2 tau_e + a^2 sigma^2) from Var(eps + kappa u); b_s formula reproduces Lab 1 b_s = 0.39718750.")
F("E4d-math-prop2", "Re-derived this round (:285-287): Corr(v,p)^2 = (b_s^2/tau_v^2)/((1/tau_v) b_s^2 (1/tau_v + 1/tau_y)) = tau_y/(tau_v+tau_y); lambda = 0 gives b_s = 0 and Corr = 0.")
F("E4d-math-prop3", "Re-derived this round (:288-293): sign G = sign(V_U - e^{2ac} V_I); times (tau_v+tau_y)(tau_v+tau_e)e^{-2ac} gives tau_bar - tau_y; G(0+) formula from Omega -> 1/tau_v + a^2 sigma^2/tau_v^2, V_U -> 1/tau_v. Independent Omega-form solver (ledgers/E4/alternatives/alt_r10_a.py) agrees with the reference's gap at 0 and in the interior on seeds 0-49 (50/50 pass).")
F("E4d-math-prop4", "Re-derived this round (:295-298): lambda* = a sigma sqrt(tau_bar/(tau_e(tau_e - tau_bar))) from tau_y(lambda*) = tau_bar; interior informativeness 1 - e^{2ac} tau_v/(tau_v+tau_e) = tau_bar/(tau_v+tau_bar). Max |bisection - closed form| on the 3x3 grid 2.13e-13 (logs/numbers_r10.txt).")
F("E4d-math-prop5", "Re-derived this round (:300-301): d lambda*/d sigma = lambda*/sigma; k(t)^2 = t/(tau_e(tau_e-t)) strictly increasing; tau_bar strictly decreasing in c; informativeness has no sigma.")
F("E4d-math-assumptions", "All five read in full. A1 was changed this round (project.html:257: 'a common prior mean mu', 'For an information set F (Lemma 1)'). Checked: the mu-shift argument is correct (demand depends on E[v|F]-p, utility on v-p; the zero-mean economy with each variable less mu). A3 wealth-shift argument checked (common w_0 multiplies every expected utility by exp(-a w_0) > 0). A4 b_s != 0 for lambda > 0 consistent with Prop 1 (b_s > 0 on (0,1]). Note: V (the conditional variance) appears in A1 before Lemma 1 defines it at :266; A1 cites Lemma 1 for that formula, so this is a pointer, not an undefined term.")

# ---- notation / prose / structure ----
F("E4d-notation", "Registered symbols (notation/notation.json: T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, Q) do not occur in project.html (grep this round). New local symbols mu (A1, :257) and F (\\mathcal F, A1 and Lemma 1) are defined on the page; mu is not a registry symbol (it appears in notation.json only inside the meanings of \\Normal and gamma_3/gamma_4, always as a mean), so no collision.")
F("E4d-banned-phrases", "Grep this round for TODO, TBD, lorem, for brevity, details omitted, beyond the scope, left as an exercise, you can add more, it is important to note, studies show, experts agree, it is well known, obviously, clearly, 'about <n>', roughly, historically, ellipsis, in project.html text: no hit (only 'fixed in your module' as plain English).")
F("E4d-process-words", "Grep this round for round, verifier, builder, ruling, architect, audit, previous (nav link only), fixed in, fixer, mutant, alternative in project.html text: no process word in learner text (the 'previous' hit is the lesson-nav link at :695).")
F("E4d-dag-links", "check_dag PASS (E4d-cmd-check-dag). Links resolve: L06.html#def-noisy-rational-expectations-equilibrium (L06.html:169 anchor present this round, after the L06 delta), L07.html#def-price-informativeness (L07.html:62), ../../../concepts.html#expected-utility (concepts.html:447), index.html#placement (index.html:66). Tool-checked: no missing anchors in project.html.")
C("E4d-registry-muth", "references/references.json and project.html:684")
C("E4d-registry-milgrom", "references/references.json and project.html:685")
C("E4d-cites-only-registry", "project.html data-cite lines :684-685", None)
C("E4d-spec-context-sentences", "project.html:312", None)
F("E4d-spec-questions", "Read in full this round (project.html:314-322). Questions a competent student would still ask: (1) whether solve_model must accept integer or numpy inputs (not stated; no test depends on it); (2) the gap at lambda* = 1 (answered: hypothetical uninformed agent, Prop 3); (3) the stop rule and tolerance (answered in Constraints, :318). Round 10 adds none: the new gap-at-zero precision sentence (:318) answers the question of which gap a zero fraction reports.")
C("E4d-spec-ladder", "project.html:40-49, :51-305, :308, :669-675", None)
C("E4d-prose-scope-words", "project.html:326 (exception paragraph)", None)
F("E4d-prose-simulated-labs", "grep this round: each lab hypothesis says its inputs are SIMULATED or stated values (project.html:57, :176, :314, :375); no open( in the three project twins.")
C("E4d-prose-simulated-exemplars", "project.html:530", None)
F("E4d-hours-project", "project.html:33 data-hours-project=28, :35 eyebrow '28 hours', #hours total 28 (:351); index.html:29 data-hours-lessons=72 and data-hours-project=28 (72 + 28 = 100 = curriculum.json E4 hours 100, grep this round). Lessons 9 x 8 = 72 (index.html:139).")
F("E4d-hours-estimate", "My own estimate this round: rung 1 1 h, rung 2 1 h, derivation of Props 1-5 with Lemmas 5 to 6 h, solver with the local tests 6 h, 3x3 grid and closed-form comparison 3 h, report 5 h, self-assessment 3 h = 25 h. Declared 28 h is 12% above 25 h, within 30%. Component sum of the page table (:344-351) = 28 (recomputed).")
C("E4d-rubric-observable", "project.html:517-527 (#rubric)", None)
F("E4d-exemplar-A-calibration", "Blind scoring not possible for this verifier: the official scoring line (project.html:538) and the annotations were displayed by this round's full read before any score was given. Not scored.", "UNVERIFIABLE", "Calibration must be done by a verifier that has not read the annotations; the page cannot be blind-scored by this agent.")
F("E4d-exemplar-B-calibration", "Blind scoring not possible: the official scoring line (project.html:603) and the Model annotation were displayed by this round's full read.", "UNVERIFIABLE", "As E4d-exemplar-A-calibration: a fresh verifier must score Exemplar B without the annotations.")
F("E4d-exemplar-annotations-hidden", "rubric.js unchanged since 0dee921a (git diff --stat over course/assets/js empty); project.html has data-reveal on the two exemplar verdicts (grep this round); the annotations are hidden by the form (rubric.js:147-150, read).")

# ---- grader ----
F("E4d-grader-exceptions", "Named conditions tested in both directions (test_project.py:191-234, plus the new gap test at :382-398 does not touch them). noise 0, -SD, inf, nan rejected; 1e-12 accepted; cost -0.01 and -1e-12 rejected; cost 0 accepted. Only the two named conditions demand ValueError (six must_raise calls). Reference 43/43 on seeds 0, 7, 49 under python -I -W error (logs/ref_seeds_0_7_49_r10.txt; collect 43).")
F("E4d-grader-messages", "Read in full this round (test_project.py, every expect() and pytest.fail call, including the new test at :389-397). Each hint names the property; no hint prints a value. The only f-strings are in must_raise, where the label, not a value, is printed.")
C("E4d-grader-oracle", "test_project.py:79-170 (oracle block)", None)
F("E4d-grader-instances", "Exhaustive check of the generator's domain this round: noise_sd = round(U[0.5,0.75], 3) takes 251 values and info_cost = round(U[0.12,0.15], 3) takes 31 values, so 7781 possible instances. Interior sign pattern (gap positive at 0, negative at 1) holds at all 7781 (logs/domain_and_bitwise_r10.txt: 0 points not interior). Seeds 0-49: 50/50 interior, 50 distinct instances, noise_sd 0.503-0.741, cost 0.120-0.149 (logs/*). run_graders instance checks PASS.")
F("E4d-grader-instance-docstring", "Docstring numbers recomputed this round: tau_bar in [0.097623, 0.237567] and tau_y(1) >= 0.30769 (E4d-num-box-bounds). The docstring says the bound is derived there and not re-checked by the suite; the suite has no bound test, which is accurate.")
C("E4d-grader-test-docstring", "grader/test_project.py tiny-root docstring (now at :526-528 after the +19-line insert at :379; the text is byte-identical)", None)
C("E4d-grader-reference-docstring", "grader/reference.py:21-23", None)
F("E4d-grader-stdlib", "test_solver_imports_only_the_standard_library (now test_project.py:480-489) passes on reference.py and on alt_1..alt_5, alt_r10_a and alt_r10_b, 50/50 seeds each (logs/alternatives_equiv_seeds0-49_r10.txt, logs/alt_r10_seeds0-49.txt).")
F("E4d-runtime", "run_graders slowest reference seed 0.5 s (logs/run_graders.txt); in-browser suite 0.9 s (logs/page_smoke_project.txt). Under the 5 s per-test and 60 s suite limits.")
F("E4d-browser-local-parity", "In-browser: 43 of 43 pass (page_smoke). Local: `python -I -W error -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py` in a scratch copy with QF_SEED 0, 7, 49 on the reference: '43 passed' each (logs/ref_seeds_0_7_49_r10.txt).")
F("E4d2-exemplar-B-C1-annotation", "Partly checked: Props 1 to 5 each state 'Assume A1 to A5' (project.html:279-301). The exemplar's proposition-by-proposition mapping of A1 to A5 was not checked against each proof in this round, and the exemplar is part of the blind calibration, which is itself UNVERIFIABLE.", "UNVERIFIABLE", "Check the mapping against each proof with a verifier that has not read the annotation (E4d-exemplar-B-calibration).")
F("E4d3-cara-defined-twice", "CARA is cited as Definition 6.2 of Lesson 6 at project.html:259 and not defined with <dfn> there (grep). L06.html:66-67 is the definition, present this round after the L06 delta (L06.html changed by 6 insertions, 5 deletions; the Definition 6.2 block is intact).")
F("E4d3-anchors-links", "Tool and grep check this round: every href='#...' in project.html has a matching id (no missing anchors); no external href or src.")
F("E4d3-no-figures-no-data", "project.html contains no svg, img, figure or iframe element (grep this round); no data file is read by the page.")
F("E4d3-spec-stop-rule-and-constraints", "Constraints (project.html:318) still states the bisection stop rule ('stops when the bracket is narrower than 1e-12 times its upper end, or after 200 halvings'; 'The reported lambda* lies in the final bracket'). The round-10 change to this line added only the gap-at-zero precision sentence. The stop rule is not enforced by any test: alt_4 (secant, relative-step stop) passes 50/50 seeds (logs/alternatives_equiv_seeds0-49_r10.txt); the mutant v9_02 (stop rule measured against the lower end) survives seeds 0-9 (logs/mutate_graders_seeds0-9_r10_final.txt). The difference is about 1e-13 at most, not observable at the suite's tolerances. The stop-rule clause is stated behaviour the suite cannot see.", "FAIL", "Either reword Constraints (:318) to the observable requirement (the reported lambda* is within 1e-10 of the root and the gap changes sign across the reported bracket), or add a test that separates the stated rule from alternatives. Until one of these holds, the stop-rule clause is untested. Do not change the page without an architect decision on which is wanted.")
F("E4d3-atlas-studios-na", "No atlas contract for E4 (atlas/ has no E4 file, ls this round); the project is not an atlas milestone. Not applicable.")
C("E4d-mutants-existing", "ledgers/E4/mutants/ (68 pre-round-9 files)", "All 68 pre-round-9 mutants are KILLED in the round-10 run (logs/mutate_graders_seeds0-9_r10_final.txt, 78 lines; the only survivor is mutant_v9_02).", None)
F("E4d-mutants-new", "mutant_r7_02_rejects_noise_above_one.py and mutant_r7_03_rejects_cost_above_one.py: KILLED (logs/mutate_graders_seeds0-9_r10_final.txt).")
F("E4d2-mutants-r2", "mutant_r2_* (4 files): KILLED (logs/mutate_graders_seeds0-9_r10_final.txt).")
F("E4d3-mutants-r3", "mutant_r3_* (5 files): KILLED (logs/mutate_graders_seeds0-9_r10_final.txt).")
F("E4d3-mutant-tolerance-survives", "mutant_r3_tolerance_1e-9.py: KILLED this round (logs/mutate_graders_seeds0-9_r10_final.txt, 'Bisection stops at a relative bracket width of 1e-9'). The round-9 row id is kept; the mutant no longer survives.")
F("E4d-mutants-total", "`tools/mutate_graders.py --unit E4 --seeds 0-9` (round 10, 78 mutants, 13 s) -> 'mutate_graders E4: FAIL (77/78 killed)', exit 1 (logs/mutate_graders_seeds0-9_r10_final.txt). Only survivor: mutant_v9_02_stop_rule_relative_to_lower_end.py (E4d9-mutant-v9-02).", "FAIL", "Resolve E4d9-mutant-v9-02 (see E4d3-spec-stop-rule-and-constraints).")
F("E4d-equivalent", "ledgers/E4/equivalent/literal_price_sign.py: b_u enters only through b_u*b_u (reference.py informed_term), so the sign of b_u cannot change an output. Randomized check this round (logs/domain_and_bitwise_r10.txt), 3000 inputs (sd in [0.05, 3], c in [0, 0.4]): 0 bitwise-different outputs, worst abs diff 0.0 (logs/domain_and_bitwise_r10.txt). Also passes 50/50 seeds. mutant_r7_01 (reports the lower end of the bracket) passes 50/50 seeds and differs from the reference only inside the stated tolerance. Both are documented in ledgers/E4/equivalent/README.md and kept out of mutants/.")
F("E4d-alternatives", "alt_1.py .. alt_5.py: each passes 50/50 seeds on the suite (logs/alternatives_equiv_seeds0-49_r10.txt).")
C("E4d-starter", "course/modules/E/E4/grader/starter.py", None)
F("E4d4-alt4-wrong-on-small-noise", "alt_4 passes 50/50 seeds this round, including the tiny-root tests (logs/alternatives_equiv_seeds0-49_r10.txt). Its stop rule is a secant step size, not the page's bracket rule; that is recorded under E4d3-spec-stop-rule-and-constraints.")
C("E4d4-alt1-docstring", "ledgers/E4/alternatives/alt_1.py:1-3", None)
C("E4d4-equivalent-price-slope", "ledgers/E4/scripts/E4-d-r4/check_equivalence_r4.py", None)
F("E4d4-calibration-blind", "Same as E4d-exemplar-A-calibration: not scored blind.", "UNVERIFIABLE", "As E4d-exemplar-A-calibration.")
C("E4d4-proposed-test-validated", "grader/test_project.py small-noise tests (now :513-534; byte-identical)", None)
F("E4d4-mutants-killed-r4", "every mutant_r4* file: KILLED (logs/mutate_graders_seeds0-9_r10_final.txt).")
F("E4d4-exemplar-B-results-numbers", "Round 10 changed the results paragraph at project.html:629 (ratio sentence). Re-checked: the nine table rows equal the Lab 3 printed rows (logs/lab_twin_check_r10.txt); the displayed ratios 1.2501 and 1.5000 are right (E4d-num-exemplar-table).")
F("E4d5-mutant-bracket-floor", "mutant_r5_bracket_floor_1e-12.py: KILLED (logs/mutate_graders_seeds0-9_r10_final.txt).")
F("E4d5-mutant-sixty-halvings", "mutant_r5_sixty_halvings_no_tolerance.py: KILLED (logs/mutate_graders_seeds0-9_r10_final.txt).")
F("E4d5-mutant-uninformed-precision", "mutant_r5_uninformed_posterior_precision_informed.py: KILLED (logs/mutate_graders_seeds0-9_r10_final.txt).")
F("E4d5-calibration-B-blind", "Same as E4d-exemplar-B-calibration: not scored blind.", "UNVERIFIABLE", "As E4d-exemplar-B-calibration.")
F("E4d6-mutant-06", "mutant_r6_06_cost_scales_whole_gap.py: KILLED (logs/mutate_graders_seeds0-9_r10_final.txt).")
F("E4d6-mutant-07", "mutant_r6_07_unit_informativeness_discounted_by_cost.py: KILLED (logs/mutate_graders_seeds0-9_r10_final.txt).")
F("E4d6-mutants-new-killed", "mutant_r6_01 .. r6_07 (7 files): KILLED (logs/mutate_graders_seeds0-9_r10_final.txt).")
F("E4d6-spec-variants-08-09", "mutant_r6_08_reports_lower_end.py and mutant_r6_09_always_200_halvings.py (ledgers/E4/equivalent/): both PASS the whole suite, 50/50 seeds (logs/alternatives_equiv_seeds0-49_r10.txt). r6_08 is allowed by 'The reported lambda* lies in the final bracket' (:318). r6_09 never applies the relative stop and violates the first limb of the stated stop rule (:318), and no output test can see the number of halvings. Same class as E4d3-spec-stop-rule-and-constraints. Docstrings are now correct (E4d9-equivalent-r6-08-09-docstrings).", "FAIL", "As E4d3-spec-stop-rule-and-constraints: make the stop-rule clause observable, or drop the step-count wording from Constraints.")
C("E4d6-stop-rule-measured", "grader/reference.py:22-23, :138 and ledgers/E4/alternatives/alt_5.py", None)
C("E4d6-alt-extra-damped", "ledgers/E4/scripts/E4-d-r6/candidates/damped_fixed_point_log_r6.py", None)
F("E4d6-rung1-why", "Each of the six Lab 1 steps is given a reason (project.html:171, byte-identical). The 2^-53 claim re-derived this round: after 53 halvings the bracket width is 2^-53 = 1.110e-16 and it stays there (ledgers/E4/scripts/E4-d-r9/logs/lab1_width_check_r9.txt, and the round-10 twin run prints 1.110e-16 after 60 halvings, logs/lab_twin_check_r10.txt).")
C("E4d7-midpoint-untested", "project.html:318 and ledgers/E4/equivalent/mutant_r7_01_reports_bracket_lower_end.py", None)
C("E4d7-cost-above-one-rejected", "grader/test_project.py:242-253 (unchanged lines) and project.html:326", None)
C("E4d7-noise-above-one-rejected", "grader/test_project.py:357-370 (unchanged lines; the insert is at :379)", None)
C("E4d7-alt5-docstring", "ledgers/E4/alternatives/alt_5.py:1-2", None)
C("E4d7-lab1-bracket-width", "project.html:171", None)
F("E4d7-lab2-blank", "project.html:244 names the blank; the twin differs from the page code only at the blank line (lab_twin_check_r10.txt: 2 differing lines, the blank pair).")
F("E4d7-instance-bound", "Re-derived this round: the bound in the Inputs claim (project.html:314) and instance.py:1-21 agree; the exhaustive check over 7781 generator draws shows the interior sign pattern holds at each (E4d-grader-instances).")
F("E4d7-lab3-closed-form-sentence", "Largest bisection-vs-closed-form difference printed 2.13e-13 (logs/numbers_r10.txt reproduces 2.13e-13); 'to within 1e-12' holds.")
F("E4d7-test-count", "project.html:320 says 43 checks; collect-only count is 43 (logs/collect.txt). The round-9 row said 42 and is superseded.")
F("E4d8-no-upper-bound", "project.html:326 (unchanged) with the new tests test_noise_volume_far_above_one_is_accepted (sd 50, 1000) and test_info_cost_far_above_one_is_accepted (c 10, 50), which pass on the reference (43 passed). Probe this round (logs/domain_and_bitwise_r10.txt): solve_model returns finite outputs in range for sd in {1e-300, 1e-12, 0.6, 1, 50, 1e75, 1e150} x c in {0, 0.13, 1, 10, 350}: 35 of 35 OK.")
F("E4d8-cap-100-survives", "mutant_r8_01_cap_100_halvings.py: KILLED this round (logs/mutate_graders_seeds0-9_r10_final.txt). The round-9 row id is kept.")
F("E4d8-noise-cap-10-survives", "mutant_r8_02_noise_above_ten_rejected.py: KILLED this round (logs/mutate_graders_seeds0-9_r10_final.txt).")
F("E4d8-cost-cap-5-survives", "mutant_r8_03_cost_above_five_rejected.py: KILLED this round (logs/mutate_graders_seeds0-9_r10_final.txt).")
F("E4d8-mutants-r8-killed", "mutant_r8_04_integer_zero_fraction.py and mutant_r8_05_informativeness_at_unit_precision.py: KILLED this round (logs/mutate_graders_seeds0-9_r10_final.txt).")
F("E4d8-alternatives-r8", "ledgers/E4/alternatives/alt_r8_a.py and alt_r8_b.py (cited by round 8) do not exist at pin 00a8479 (ls ledgers/E4/alternatives: alt_1..alt_5 only). Not re-verified; not carried.", "UNVERIFIABLE", "Re-create the two alternatives in ledgers/E4/alternatives/ and re-run them, or drop the citation.")
C("E4d8-tiny-root-reference", "course/modules/E/E4/grader/reference.py (unchanged); solve_model(1e-30, 0.13) relative error vs closed form 2.93e-13 in round 9", None)
F("E4d8-lab3-twin-page", "Page code equals the Lab 3 twin (114 vs 114 lines, 0 differing); twin runs `-I -W error` exit 0; output equals the expected block (logs/lab_twin_check_r10.txt).")
F("E4d9-mutant-v9-02", "mutant_v9_02_stop_rule_relative_to_lower_end.py: SURVIVED seeds 0-9 this round (logs/mutate_graders_seeds0-9_r10_final.txt). The mutant runs while width > 1e-12*low, so it stops later than the reference; its outputs differ from the reference by at most about 1e-12 relative and only when a dyadic bracket width falls between 1e-12*low and 1e-12*high. No test observes it. The page states this stop rule (project.html:318).", "FAIL", "As E4d3-spec-stop-rule-and-constraints.")
F("E4d9-mutant-v9-06", "mutant_v9_06_gap_at_zero_from_tiny_fraction.py: now KILLED by test_gap_at_zero_fraction_is_the_limit_to_full_precision (seed 0) (logs/mutate_graders_seeds0-9_r10_final.txt). The new test is the round-10 change: the gap at 1e-12 differs from the limit by 1.02e-13 to 3.54e-13 at the six test inputs (logs/numbers_r10.txt), above the 1e-14 threshold.")
F("E4d9-equivalent-r6-08-09-docstrings", "The first docstring lines of ledgers/E4/equivalent/mutant_r6_08_reports_lower_end.py and mutant_r6_09_always_200_halvings.py now read 'Variant of the reference: ...' and describe their one edit (fixed in round 10; checked this round).")
F("E4d9-mutants-v9-killed", "mutant_v9_01, _03, _05, _07: KILLED (logs/mutate_graders_seeds0-9_r10_final.txt).")
F("E4d9-mutant-docstrings", "ledgers/E4/mutants/*.py (78 files): mutate_graders prints each first docstring line (logs/mutate_graders_seeds0-9_r10_final.txt). Checked this round for the four new files: r10_01 (price precision drops lam squared), r10_02 (uninformed limit drops a^2), r10_03 (gap rounded to nine places), r10_04 (noise message 'finite and positive'), each matching its one edit.")
F("E4d9-alternatives-v9", "The cited files ledgers/E4/alternatives/alt_v9_1_interior_gap_zero.py, alt_v9_2_log_space.py and alt_v9_3 are not at pin 00a8479 (ls). The round-9 claim that they pass 50/50 is not re-verified this round.", "UNVERIFIABLE", "Commit the three alternatives to ledgers/E4/alternatives/ and re-run them, or drop the row.")

# ---- new rows for round 10 ----
F("E4d10-delta-A1-prior-mean", "project.html:257 (A1 changed): the common prior mean mu normalization and the 'For an information set F (Lemma 1)' pointer. The shift argument is checked (demand depends on E[v|F]-p; utility on v-p). Pointer to Lemma 1 for V and F is a forward reference, not an undefined term. PASS.")
F("E4d10-delta-inputs-interior-root", "project.html:314 (Inputs, changed sentence 'every instance the generator draws has one interior root'): checked over all 7781 generator draws (0 exceptions), the box bounds 0.097623 <= tau_bar <= 0.237567 < 0.30769 <= tau_y(1) (logs/numbers_r10.txt), and (logs/domain_and_bitwise_r10.txt).")
F("E4d10-delta-constraints-gap-at-zero", "project.html:318 (changed sentence: the gap at fraction 0 agrees with the limit to 1e-14 relative to max(1, |limit|)). Reference agrees with the limit to <= 1.1e-16 at the six test inputs (oracle, reference and Decimal-precision limit computed this round). The sentence is consistent with reference.py gap_at_zero and with the new test.")
F("E4d10-delta-grading-mode-43", "project.html:320 says 43 checks; collect-only on the grader gives 43 (logs/collect.txt); 43 pass on the reference for seeds 0, 7, 49.")
F("E4d10-delta-results-ratio", "project.html:629 (changed sentence): 'from the displayed values, 0.6978/0.5582 = 1.2501 and 0.8373/0.5582 = 1.5000'. 0.6978/0.5582 = 1.25009 and 0.8373/0.5582 = 1.50000 (logs/numbers_r10.txt); unrounded ratios 1.2499999999999 and 1.5000000000006 agree with 1.25 and 1.50.")
F("E4d10-new-test-numbers", "test_gap_at_zero_fraction_is_the_limit_to_full_precision (test_project.py:382-398): docstring numbers recomputed (gap at 1e-12 minus the limit: 1.020e-13, 1.090e-13, 1.108e-13, 3.262e-13, 3.485e-13, 3.541e-13, so '1e-13 to 4e-13' is correct) and the oracle-limit difference is at most 1.11e-16. All six inputs have a nonpositive gap at 0 (lambda* = 0), so the informed_fraction assertion is consistent with the boundary rule.")
F("E4d10-mutants-new-r10", "Four new student-error mutants written this round (ledgers/E4/mutants/mutant_r10_01 .. r10_04): price precision drops the squared fraction, uninformed limit drops a^2, gap rounded to nine places, noise-volume message wording. All four KILLED at seed 0 (logs/mutate_graders_seeds0-9_r10_final.txt): r10_01 by test_gap_is_the_oracle_gap_at_the_reported_fraction[first], r10_02 by test_info_cost_above_one_is_accepted, r10_03 by test_gap_at_zero_fraction_is_the_limit_to_full_precision, r10_04 by test_noise_volume_zero_is_rejected.")
F("E4d10-alternatives-r10", "Two new correct alternatives, ledgers/E4/alternatives/alt_r10_a.py (Prop 3 in its Omega form, sqrt of V_U and V_I over sqrt(Omega)) and alt_r10_b.py (same formulas with 1/sqrt(1+x) and a for-loop with break): each passes 50/50 seeds (logs/alt_r10_seeds0-49.txt). The gap-at-zero precision test accepts both, so the new test does not over-constrain the arithmetic.")
F("E4d10-l06-dependency", "L06.html changed in this delta (6 insertions, 5 deletions). The two lesson anchors and the Definition 6.2 this page cites are intact at this pin: L06.html:66 (Definition 6.2, CARA), :169 (def-noisy-rational-expectations-equilibrium), L07.html:62 (def-price-informativeness).")
F("E4d10-lab3-numbers", "Lab 3 grid (nine points) re-derived this round by an independent float implementation (logs/numbers_r10.txt): informed fractions 0.558203, 0.445328, 0.328914, 0.697753, 0.556660, 0.411143, 0.837304, 0.667993, 0.493371; informativeness 0.1920/0.1420/0.0889; gaps |g| <= 3.55e-14; max |bisection - closed form| 2.13e-13; 484 of 484 box points with the interior sign pattern.")

# ---- assemble ----
rows = []
for r in prev["rows"]:
    i = r["id"]
    if i in fresh:
        status, ev, fix = fresh.pop(i)
    else:
        raise SystemExit(f"no round-10 decision for {i}")
    row = {"id": i, "check": r["check"], "location": r["location"], "status": status, "evidence": ev}
    if status != "PASS":
        row["fix"] = fix
    rows.append(row)
for i, (status, ev, fix) in fresh.items():
    row = {"id": i, "check": "round-10 re-check", "location": "see evidence", "status": status, "evidence": ev}
    if status != "PASS":
        row["fix"] = fix
    rows.append(row)

# mutants from the round-10 mutation log
mutants = []
for line in (LOG / "mutate_graders_seeds0-9_r10_final.txt").read_text(encoding="utf-8").splitlines():
    m = re.match(r"^(KILLED|SURVIVED) (\S+?): (.*) -> (.*)$", line)
    if not m:
        continue
    status, name, desc, killed = m.groups()
    mutants.append({
        "name": name,
        "description": desc,
        "killed_by": None if killed.strip() == "None" else killed.strip(),
        "status": status,
    })

counts = {"PASS": 0, "FAIL": 0, "UNVERIFIABLE": 0}
for r in rows:
    counts[r["status"]] += 1
killed = sum(1 for m in mutants if m["killed_by"])
frag = {
    "unit": "E4",
    "slice": "d",
    "round": 10,
    "verifier": "Haiku independent verifier, E4 slice d, round 10 (did not build E4; fresh checkout of 00a8479)",
    "pin": "00a84795f276456fce19d4181373cc4efba11a36",
    "base": "c93dd526025c6dffd34c54cd2c89eb62a890f885 (round-9 pin). Delta in the slice: project.html (10 lines: A1, Inputs, Constraints, Grading mode, the results paragraph), grader/test_project.py (+19 lines: one new test), equivalent/mutant_r6_08 and r6_09 docstrings, and the round-10 mutants and alternatives. Every hunk read.",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE10-E4-d",
    "scratch": "scratch copies in /tmp (reference as solver.py with copies of instance.py and test_project.py); the scripts that produced every logged number are in ledgers/E4/scripts/E4-d-r10/",
    "verified_at": datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat(),
    "verdict": "FAIL",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Full read of project.html (702 lines), grader/test_project.py (534), reference.py, instance.py, starter.py, and the three project labs and twins. Lab twins compared with the page code (logs/lab_twin_check_r10.txt).",
        "Mutation gate: 78 mutants in ledgers/E4/mutants, 77 killed (logs/mutate_graders_seeds0-9_r10_final.txt). The only survivor is mutant_v9_02 (E4d9-mutant-v9-02), which is the stop-rule clause of Constraints.",
        "Alternatives: alt_1..alt_5, alt_r10_a, alt_r10_b pass 50/50 seeds. Equivalents (r6_08, r6_09, r7_01) pass 50/50 but are the stop-rule cases above.",
        "Not checked: blind scoring of Exemplars A and B (not possible after the full read); the Pyodide interpreter itself (page_smoke runs the in-browser suite through the repo tool); a live verify_refs run (references unchanged); the two alternatives cited by rounds 8 and 9 (alt_r8_a/b, alt_v9_1..3) because they are absent at the pin.",
        "Questions the spec leaves open for a student (none blocks a grader): integer inputs to solve_model; numpy inputs; the value at lambda* = 1 is explained (hypothetical uninformed agent) so not open.",
    ],
    "summary": {
        "rows": len(rows),
        "pass": counts["PASS"],
        "fail": counts["FAIL"],
        "unverifiable": counts["UNVERIFIABLE"],
        "mutants": len(mutants),
        "mutants_killed": killed,
    },
}
out = root / "ledgers/E4/E4-d.json"
out.write_text(json.dumps(frag, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("rows", len(rows), counts, "mutants", len(mutants), "killed", killed)
