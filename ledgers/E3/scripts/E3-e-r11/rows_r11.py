"""Round-11 E3-e rows. Builds the fragment ledgers/E3/E3-e.json (read by tools/ledger.py)."""
import json, sys
PIN = "ccaeeaf4"
BASE = "47a36d8c (round-10 pin)"
C = "Carried from round 10 (%s byte-identical since 47a36d8c): "
R = lambda files, text: C % files + text
ROWS = []
def row(i, check, loc, status, ev, fix=None):
    r = {"id": i, "check": check, "location": loc, "status": status, "evidence": ev}
    if status != "PASS":
        r["fix"] = fix
    ROWS.append(r)
S = "ledgers/E3/scripts/E3-e-r11/out/"
LESSON_NOT_REREAD = ("UNVERIFIABLE: the lesson file changed since 47a36d8c (hunks listed in the notes) and the cited passage was not "
                     "re-read end to end by this verifier; this is a checking gap, not a finding")
LESSON_FIX = "Re-verify the cited passages of the changed lesson file in the lesson slices, then re-run this row."

# ---- FAIL rows (re-verified this round) ----
row("E3e4-exemplar-B-level", "Exemplar levels match the binding plan (exemplar-a level 2, exemplar-b level 4)",
    "course/modules/E/E3/project.html:701 (data-level=\"3\" on exemplar-b); plans/E3-build-plan.md:392 (exemplar-b data-level=\"4\")",
    "FAIL",
    "grep data-level: exemplar-a=2, exemplar-b=3 (project.html:648, :701). Plan 6.6 (plans/E3-build-plan.md:392) says exemplar-b is data-level 4. "
    "The page's own verdict for B (project.html:703) says it falls short of level 4 on C1, C2, C4 and C5, and data-scores is 3,3,4,3,3. "
    "plans/E3-open-items.md:145-149 amends only the word count, not the level.",
    "Either make exemplar-b a level-4 exemplar (score 4 on every criterion, with annotations that meet every level-4 descriptor), or obtain an architect ruling that exemplar-b is level 3 and amend plan 6.6 and the data-level.")
row("E3e5-03", "Lab-E3-project-3 calls the engine on the reference case (plan 6.1 item 3, binding)",
    "tests/labs/E3/lab-E3-project-3.py (whole file); course/modules/E/E3/project.html:393-398; plans/E3-build-plan.md:290-292",
    "FAIL",
    "The twin imports only math and fractions.Fraction and defines its own grid_start, second_order_search, log_likelihood and estimate; "
    "it calls no elicit module and no grader/reference.py. Plan 6.1 item 3 (binding) says lab-E3-project-3 'calls the engine on the reference case'. "
    "plans/E3-open-items.md section 3 item 2 records the builder's deviation, but the architect ruling of round 9 covers only plan 6.5 items 6, 7 and 9.",
    "Architect ruling: either accept the twin as the rung-3 check and amend plan 6.1 item 3 to say so, or change the lab so it calls the engine it is meant to check.")
row("E3e-r11-lab3-estimate-keys", "Lab 3 instruction (replace estimate with your module's estimate; main must print the same lines) is satisfiable under the spec",
    "course/modules/E/E3/project.html:391-395 (instruction), :587 (main reads result['largest_score']), :209 (spec: estimate returns seven keys)",
    "FAIL",
    "main() prints result['largest_score'] (project.html:591 and twin). The spec at project.html:209 lists exactly seven keys for estimate, and the suite asserts 'estimate must return exactly the seven named fields' at grader/test_project.py:533 (test_estimate_returns_the_named_fields_as_finite_floats, present since round 10) and at :895 (new this round). "
    "A student who follows the Lab 3 instruction cannot print the score line without a key the spec and the suite forbid. reference.estimate returns the seven keys only "
    "(run on the twelve Lab 3 answers, see " + S + "lab3_crosscheck_r11.out).",
    "Compute the largest score component in a separate function from log_likelihood inside run_case.py (as largest_score() does in the lab), and drop largest_score from the lab's estimate dict.")
row("E3e-r11-rubric-C1-level4", "Rubric C1 level-4 descriptor matches the binding plan 6.6 descriptor",
    "course/modules/E/E3/project.html:636 (C1 level 4); plans/E3-build-plan.md:375-395 (6.6 item 1)",
    "FAIL",
    "Plan 6.6 item 1, level 4: 'lists the pairs with cents and exact probabilities and shows the mixed-sign pairs'. Page level 4: 'lists the pairs with prizes in cents and exact "
    "probabilities, and states how many pairs mix a gain and a loss'. 'Shows the mixed-sign pairs' is replaced by a count, so a memo that only counts mixed pairs meets level 4.",
    "Restore the plan's level-4 descriptor ('shows the mixed-sign pairs') on the page, or record an architect ruling that changes plan 6.6 and then update exemplar annotations that cite it.")
row("E3e-32", "Five alternative correct implementations pass (over-constraint check)",
    "ledgers/E3/scripts/E3-d-r10/alts/alt1..alt5 (fixtures); course/modules/E/E3/grader/test_project.py (suite run with each as elicit.py)",
    "FAIL",
    "Full suite, QF_SEED=0, run this round (" + S + "out/alts/*_seed0_full.txt): alt5_exp_log_float 48 passed; alt4_bisection_ce 1 failed "
    "(test_half_cent_goes_up_on_exact_halves: alt4 returns 2 for prospect, gamma 0, prizes [2,3] at 1/2 each, whose exact CE is 2.5; direct call in the same folder); "
    "alt2_pure_newton_fd1e-6 3 failed (RuntimeError 'observed information not positive definite' in the recovery loop, the seed-30 check and the seed-49 check); "
    "alt1_grid_zoom_newton fails the recovery loop and the seed-49 check the same way (" + S + "alt1_diag_r11.py: alt loglik -126.038268 at seed 49 vs reference -126.031539, so the alternative stops short of the maximum). "
    "alt3_nelder_mead: 2 failed, 46 passed (the two mixed-lottery fixture tests test_estimate_accepts_a_mixed_lottery_on_the_b_side_alone and ..._on_the_a_side_alone; RuntimeError from the fixture's observed information; not diagnosed further). Coverage note: each full-suite run used QF_SEED=0 only; the 50-seed recovery loop and the fixed participants 30 and 49 are covered, the seed-specific tests for seeds 1-9 were not run for alt2 to alt5 (run time), and alt1 seeds 1-2 partial files were killed and are not evidence.",
    "(a) Over-constraint: test_half_cent_goes_up_on_exact_halves (test_project.py:265-285) requires exact half-cent recognition for the PROSPECT model at gamma 0, but project.html:221 grants the exact-fraction exception only to the CRRA model at gamma 0; a conforming float bisection (plan 6.4 item 4) gives 2. Architect ruling: extend the exception on the page to prospect at gamma 0 and make the reference and the fixture agree, or drop the prospect assertions and keep the CRRA one. (b) Fixture defects: alt1 and alt2 do not reach the maximum on seed 49 (and alt2 on seed 30 and in the recovery loop), and alt3 raises on the two mixed-lottery fixtures; repair or replace them (the round-10 damped variants are candidates) and re-run seeds 0-49.")
row("E3e-r11-half-cent-prospect-gamma0", "Whole-cents convention vs the grader's exact-half test for the prospect model",
    "course/modules/E/E3/project.html:221 (Whole cents); course/modules/E/E3/grader/test_project.py:265-285",
    "FAIL",
    "project.html:221: 'The one exception is gamma = 0 under the crra model, where the expected prize is summed as an exact fraction'. The suite's exact-half test also asserts prospect gamma=0 results (got_up == 3 for [2,3]; 1 for [0,1]; 0 for [-1,0]), which the page does not promise for a float-computed prospect value. Same root cause as E3e-32 (b).",
    "Decide with the architect (see E3e-32 fix a): page and suite must state the same exception.")

# ---- PASS rows re-verified this round ----
row("E3e-01", "Banned strings in learner-visible prose; ellipsis outside code", "course/modules/E/E3/project.html (whole file); grader/*.py; tests/labs/E3/lab-E3-project-*.py", "PASS",
    "tools/check_pages.py --unit E3: PASS (" + S + "out/check_pages.out); project.html re-read in full this round.")
row("E3e-02", "Process words in learner text", "course/modules/E/E3/project.html; grader/*.py; tests/labs/E3/lab-E3-project-*.py", "PASS",
    "Visible-text scan of project.html for builder, verifier, architect, orchestrator, planner, round, slice, ledger, mutant, fixture, batch: no hits (only the course term 'the brief'). grep over grader and labs: no hits.")
row("E3e-03", "Process references in learner-visible code and docstrings", "course/modules/E/E3/grader/*.py; tests/labs/E3/lab-E3-project-*.py", "PASS",
    "grep -i 'process|builder|verifier|architect' over grader/*.py and the three project twins: no hits.")
row("E3e-04", "Links and anchors on project and hub pages; concept links resolve", "course/modules/E/E3/project.html (all href); index.html", "PASS",
    "ledgers/E3/scripts/E3-e-r11/links_r11.py over project.html: 31 hrefs, all files and ids resolve, BAD: []. Concept links L02/L03/L04/L06 ids present (" + S + "links_r11.out).")
row("E3e-05", "Project structure and ladder order", "course/modules/E/E3/project.html:40-48 (ladder), :201 (spec), :243 (questionnaire)", "PASS",
    "Read in full: rungs 1-4 in order at :44-47; spec at :201; questionnaire at :243; the rung-3 items (engine, instrument, report) in order.")
row("E3e-06", "Hours arithmetic: hub split and project table", "project.html:33 (data-hours-project=14), :362-370 (table id=hours); index.html:29-31, :40, :127", "PASS",
    "Project table 1+1+3+4+3+2 = 14 = data-hours-project. Hub: 8 lessons x 7 h (data-hours=7 on L01-L08) = 56, plus 14 = 70 (index.html:31 '70 hours'). No arithmetic inconsistency.")
row("E3e-07", "Rung 3 scope matches the curriculum brief", "project.html:205-215; curriculum/02-economics-finance-core.yaml (E3 entry)", "PASS",
    "The E3 entry of the curriculum is byte-identical to the round-10 pin (the only curriculum change in this round is in another unit's brief, option-chain text). Spec re-read: engine, instrument and report, rubric grading.")
row("E3e-08", "Spec completeness: a competent student needs no clarifying question", "project.html:200-225 (spec and conventions), :230-238 (exception table)", "PASS",
    "Read in full. The conventions, models, exception table, probability forms and questionnaire file format are stated. The Lab 3 key mismatch is a separate row (E3e-r11-lab3-estimate-keys).")
row("E3e-09", "Rubric C1 observable", "project.html:636 (C1 row)", "PASS",
    "Each C1 level names observable content (count, scale, pairs). The level-4 wording deviation from plan 6.6 is a separate FAIL row (E3e-r11-rubric-C1-level4).")
row("E3e-10", "Rubric C5 observable; exemplar B annotations match descriptors", "project.html:641 (C5 row), :735-736, :758-759 (annotations)", "PASS",
    "C5 level descriptors name grade, key, derivation and invented locators (observable). Exemplar B annotations at :758-759 match the level-3 and level-4 C5 descriptors.")
row("E3e-11", "Rubric structure: five criteria, four levels; data-criterion and data-level present", "project.html:632-642 (table id=rubric); :648-765 (exemplars)", "PASS",
    "Five rows C1-C5 with data-criterion (:636-640); four level columns; exemplar articles carry data-level and data-scores (:648, :701); annotation li carry data-criterion and data-level.")
row("E3e-12", "Calibration: exemplar scores within one level of annotations (blind scoring)", "project.html:650 (A verdict), :703 (B verdict), :648/:701 (data-scores)", "PASS",
    "Limitation: blind scoring was not achieved, because the official scoring sat in the same file read. The re-score from the rubric text and the memo text gives A = 2,2,1,2,1 and B = 3,3,4,3,3 (C1 needs all twelve pairs for level 4; C2 needs a stated precision identification; C4 needs a direction of bias; C5 needs a key or derivation), the same as the page.")
row("E3e-13", "Word counts quoted for exemplars (memo text, headings included, tags removed)", "course/modules/E/E3/project.html:646 (quoted counts); memo blocks :652-762", "PASS",
    "Re-counted: " + S + "exemplar_words_r11.out: exemplar-a memo text 117 words, exemplar-b 450 words (whitespace runs, tags removed, headings included). The page quotes 117 and 450. The round-10 figure 603 is gone from the page (grep for 603 finds nothing). Note: plans/FINAL-ARCHITECT-RULINGS.md item 7 and plans/E3-open-items.md say 103 and 375; those numbers are stale and do not match the page, but they are not page text and are not a page defect.")
row("E3e-14", "Numbers in prose, exemplars, lab expected blocks and grader docstrings re-derive", "project.html:53, :57, :138-147, :148, :383-395, :607-614, :646-731; grader/test_project.py:1071-1073", "PASS",
    "Lab 1 and 2 expected blocks equal the twins' output (run_labs PASS, 3/3). Lab 1 prose: CRRA 496/500, prospect -30/500, -762 for pair 2 B re-derived by hand. Lab 2: z = -0.14, log P(A) = -0.765595182, log P(B) = -0.625595182 re-derived. Lab 3 numbers re-derived by " + S + "lab3_crosscheck_r11.out (reference.estimate on the 12 answers copied from the page: gamma 0.6352101, lambda 6.150316, kappa 2.020107, SE 0.319, 9.594, 1.864, loglik -7.144517; mixed count 11). Grader docstring numbers at test_project.py:1071-1073 are carried (lines byte-identical in content; file changed only at :665-668 and :870-900).")
row("E3e-15", "Reading list: registry keys and which lessons cite which key", "project.html:782-789 (reading); L02.html:616; L05.html:609; L06.html:531; L07.html:80; L08.html:133, :67", "PASS",
    "Read this round. kahneman1979prospect cited with data-cite in L07.html:80; ellsberg1961risk in L08.html:133; gilboa1989maxmin in L08.html:67 (claim span). pratt1964risk named in L02.html:616 with no claim span; epstein1989substitution named in L05.html:609 with no claim span. Matches 'three of five keys attached to a graded claim, in Lessons 7 and 8'.")
row("E3e-16", "Attribution: titles and keys match registry records", "project.html:782-789; L02.html:616; L07.html:80; L08.html:67, :133, :619-620; references/references.json", "PASS",
    "Registry (references/references.json, entries): pratt1964risk 'Risk Aversion in the Small and in the Large', Econometrica 32(1-2) 1964; kahneman1979prospect 'Prospect Theory: An Analysis of Decision under Risk', Econometrica 1979; ellsberg1961risk 'Risk, Ambiguity, and the Savage Axioms', QJE 1961; gilboa1989maxmin 'Maxmin expected utility with non-unique prior', JME 1989; epstein1989substitution 'Substitution, Risk Aversion, and the Temporal Behavior...', Econometrica 1989. Each lesson sentence matches its title (e.g. L08:619 'contains the word ambiguity' matches 'Ambiguity'). tools/verify_refs.py --offline: 560 entries, 0 problems.")
row("E3e-17", "Definitions and results cited from the project page exist", "project.html:53, :210, :213, :220, :222; L02.html (def-certainty-equivalent); L03.html:173 (Proposition 2.7); L06.html:61 (Def 1.2), :68 (Def 1.3)", "PASS",
    "Link check: L02#def-certainty-equivalent, L03#def-crra-utility, L06#def-prospect-theory, L04#def-first-order-stochastic-dominance all resolve. L03.html:173 'Proposition 2.7 (affine transformations leave certainty equivalents unchanged)' grade T. L06.html:61 Definition 1.2 value function, :68 Definition 1.3 prospect value W = sum p_i v(x_i) (probabilities used as they are).")
row("E3e-18", "Lab 1 prose vs code and output", "project.html:55-149; tests/labs/E3/lab-E3-project-1.py", "PASS",
    "page code == twin (" + S + "page_vs_twin_r11.out); run_labs PASS; twin under python -I -W error exit 0, no stderr. Pair 2 B prospect CE by hand: 0.25*4000^0.6 - 0.75*2*2000^0.6 = -107.2 -> CE = -(53.6)^(1/0.6) = -762.")
row("E3e-19", "Lab 1 hypothesis numbers vs expected block", "project.html:57, :141-147", "PASS",
    "Hypothesis: CRRA 496/500, prospect -30/500, P(A)=0.480149, log P = -0.733658, total -2.302315; expected block (:141-147) identical; -0.733658 - 1.014598 - 0.554059 = -2.302315 re-added.")
row("E3e-20", "Lab 2 hypothesis numbers and completed formulas", "project.html:153-197; tests/labs/E3/lab-E3-project-2.py", "PASS",
    "Hypothesis numbers -0.765595182 and -0.625595182 re-derived (z = 2*(1500-2200)/10000 = -0.14). page code equals the twin except the two blanks (convention, FINAL-ARCHITECT-RULINGS item 11). Twin runs clean under -I -W error.")
row("E3e-21", "Lab 3 estimates, standard errors, score, log-likelihood, interpretation", "project.html:391-614; tests/labs/E3/lab-E3-project-3.py", "PASS",
    "run_labs PASS (3/3); page code == twin (11050 chars each). Independent cross-check with grader/reference.py on the 12 page answers: gamma_hat 0.6352, lambda_hat 6.1503, kappa_hat 2.0201, se 0.32/9.59/1.86, loglik -7.1445, 11 mixed pairs. The largest-score value 3.55e-10 is the lab's own output (not re-derived independently; the reference does not compute it).")
row("E3e-22", "Lab and code gates for project labs and grader", "tests/labs/E3/lab-E3-project-1..3.py; course/modules/E/E3/grader/", "PASS",
    "run_labs E3: PASS (3/3); twins under python -I -W error: exit 0; ruff check and ruff format --check on tests/labs/E3 and grader: PASS; mypy --no-incremental (repo gate): Success, 385 files; run_graders typecheck in the workspace (mypy --strict --ignore-missing-imports on test_project.py, elicit.py, instance.py): clean. Standalone mypy on the grader file alone shows import-not-found and unused-ignore, which is the workspace, not a defect.")
row("E3e-23", "Mathematics on the page: conventions, identification, delta-method SE convention", "project.html:213, :220-225", "PASS",
    "Re-derived: CE closed forms (V^(1/(1-g)) for V>=0; -(-V/lambda)^(1/(1-g)) otherwise); identification (a one-sided lottery's CE does not depend on lambda, so a pair identifies lambda only if one lottery is mixed); se_gamma = g(1-g) sqrt(cov) and se_lambda = lambda sqrt(cov) (reference.py:306-321, same chain rule).")
row("E3e-24", "Notation: symbols and macros vs notation/notation.json", "course/modules/E/E3/*.html (all math spans); notation/notation.json", "PASS",
    "Scan of all E3 page math (" + S + "out/): custom macros used are \\E, \\Var, \\Prob, \\R, \\indic, all registered; no \\mathbb{R}; no unregistered custom macro. Registered symbols: Phi appears only in project.html stretch (P(A)=Phi(...)) with the registry meaning 'standard normal CDF'; T, R^\\ast, R_f, gamma_3/4, Q: unused in E3 pages; \\ast appears only as lambda^\\ast (L06, local). Note (not a registry violation): kappa is a CARA coefficient in L01 and the choice precision in the project; kappa is not registered, so this is recorded here, not failed.")
row("E3e-25", "DAG in prose: concepts outside the prerequisite closure", "project.html (visible text, meta description); L02-L08", "PASS",
    "tools/check_dag.py --unit E3: PASS. project.html concept links: prospect-theory (L06), certainty-equivalent (L02), crra-utility (L03), first-order-stochastic-dominance (L04), all in the closure.")
row("E3e-26", "Terms used before definition on the project page", "project.html:53, :205, :213, :220, :223-224, :393-395", "PASS",
    "Certainty equivalent, CRRA, prospect value, logit rule, observed information and identification are each linked to or defined at or before first use (Rung 1 forward references point to the Rung 3 conventions and the lessons).")
row("E3e-27", "Scope words carry a computation or hypothesis (changed prose)", "project.html:45, :213, :221, :224, :602-605, :617, :680, :684, :689, :696, :735", "PASS",
    "'only', 'every', 'any' in the spec and conventions are either exception-table conditions (any set with no mixed lottery is refused) or are re-derived (identification: only mixed lotteries identify lambda; exact-fraction exception at gamma 0). Exemplar hypotheses are marked as hypotheses.")
row("E3e-28", "Autograder claims stated on the page (tolerances, oracles, local-maximum check)", "project.html:213 (grading mode); grader/test_project.py:41-42, :561-598, :601-614, :619-694", "PASS",
    "Constants checked in the file: 1e-9 move and likelihood tolerance (:587-598), score below 2e-5 at steps 1e-5 and 1e-6 (:561-584), 1e-7 reported likelihood (:554), 0.1 percent moves, seed 30 with kappa below 1 (:36), seed 49 with lambda above 10 (:37), 47 of 50 seeds within four standard errors (:601-614). All match the page.")
row("E3e-29", "Reference passes the suite on seeds 0-49", "course/modules/E/E3/grader/reference.py; tools/run_graders.py --unit E3 --seeds 0-49", "PASS",
    "run_graders E3: PASS (reference 50/50 seeds, slowest 23.6 s) (" + S + "out/run_graders_0_49.out).")
row("E3e-30", "Re-run all existing mutants (seeds 0-9)", "ledgers/E3/mutants/ (150 pre-existing files); tools/mutate_graders.py --unit E3 --seeds 0-9", "PASS",
    "tools/mutate_graders.py --unit E3 --seeds 0-9 (" + S + "out/mutate_E3_seeds0-9.out): 150 of 150 pre-existing mutants KILLED (r7_*, r9e_*, r10e_*, v*, w*, plus the rest). The run also listed the three round-11 files, but it enumerated them before they were corrected (first versions had a SyntaxError), so their entries in that log are invalid and are replaced by " + S + "out/kill_r11.txt in E3e-31.")
row("E3e-31", "At least three NEW student-error mutants of the verifier, each killed (window 0-9)", "ledgers/E3/mutants/r11_01_prospect_root_of_a_negative_value_raises_value_error.py; r11_02_crra_certainty_equivalent_reported_as_final_wealth.py; r11_03_gamma_hat_clamped_below_one_minus_1e3.py", "FAIL",
    "Three new single-change mutants of reference.py written this round. Kill check on seeds 0-9 (" + S + "out/kill_r11.txt): r11_01 KILLED on seed 0 by test_prospect_matches_oracle_for_instance_lotteries; r11_02 KILLED on seed 0 by test_crra_within_half_cent_of_oracle_for_instance_lotteries; r11_03 (reported gamma_hat = min(gamma, 0.999)) SURVIVED seeds 0-9. The seed-49 and recovery participants have gamma well below 0.999, and the page states that the estimate is maximum-likelihood (project.html:7 meta description). A survivor that violates a stated behaviour is a FAIL (VERIFIER rules, ruling 9).",
    "Add a grader test on a fixed participant whose maximum-likelihood gamma exceeds 0.999 (a generator seed with gamma near 0.95, or a hand-built response set whose likelihood increases in gamma) and assert the local-maximum check and gamma_hat within 4 standard errors of the reported value. Then re-run r11_03 and confirm KILLED.")
row("E3e-33", "Test count on the page equals the collect-only count", "project.html:213 ('runs 48 checks'); grader/test_project.py", "PASS",
    "pytest --collect-only -q on the grader (copied to scratch with elicit.py = reference): '48 tests collected' (" + S + "out/collect_only_r11.out); page says 48. Round 10 recorded 47 and a 48th test was added in this round.")
row("E3e-34", "Exception table: conditions, types and message text", "project.html:230-238; grader/reference.py:28-60, :116-121; test_project.py:287-400", "PASS",
    "Table rows match reference.py: model check ValueError (:28-31), probability check 'probabilities must sum to 1' (:45-61), crra wealth check 'wealth plus prize must stay positive' (:116-121), estimate's empty and mixed-sign refusals (:281-291). Suite tests cover each row.")
row("E3e-35", "Figures on the page", "course/modules/E/E3/project.html; course/modules/E/E3/L02-L08 (grep)", "PASS",
    "grep for figures-*.js and chart.js across course/modules/E/E3/*.html: no hits. The project page has no figure script (BUILDER_RULES 6 not triggered). Lesson figure scripts not re-read this round.")
row("E3e-36", "Registry integrity for the five E3 keys", "references/references.json; tools/verify_refs.py --offline", "PASS",
    "verify_refs --offline: 560 entries, 0 problems (" + S + "out/verify_refs_offline.out). The five E3 keys verified above (E3e-16). references.json changed in this round only for BK4/LX1 used_by and generated_at; E3 records unchanged.")
row("E3e-37", "Questionnaire and privacy claims", "project.html:245, :247, :273-353, :376, :778", "PASS",
    "The inline questionnaire script passes node --check (" + S + "out/questionnaire_node_check_r11.out). No fetch, XMLHttpRequest, sendBeacon or navigator call in project.html (grep count 0). Export happens only when every pair has a choice (:333-343). The probability regex accepts '0', '1' and 'a/b' with a nonzero denominator digit (" + S + "rx_r11.js: 0 mismatches); it checks format only, so '2/1' passes the page and is refused by the engine.")
row("E3e-38", "Rung 4 is open-ended and not graded", "project.html:772-778 (stretch)", "PASS",
    "Stretch section lists two open-ended items with no grading link; no rubric or autograder reference.")
row("E3e-39", "Suite gap: named probability condition for log_likelihood", "course/modules/E/E3/grader/test_project.py:473-507", "PASS",
    "Tests for log_likelihood refusals (sum below one, sum above one, negative) exist; code unchanged in this round.")
row("E3e-40", "Numbers in grader docstrings (seed-49 standard errors and reverse-order shifts)", "course/modules/E/E3/grader/test_project.py:1064-1073", "PASS",
    R("course/modules/E/E3/grader/test_project.py", "the lines :1064-1073 are content-identical; the file changed only at :665-668 and :870-900 (read in full, see the diff in notes)") + "numbers 135.05/97.67, 136.78, 0.09474/0.07983 were not re-derived this round.")
row("E3e-41", "Equivalent-mutant README for a survivor", "ledgers/E3/equivalent/ (directory)", "PASS",
    "ledgers/E3/equivalent does not exist at this pin. No survivor is moved there; r11_03 is handled in E3e-31 / mutants section.")
row("E3e-42", "Rename consistency (zeta, kappa, lambda, gamma, xi)", "project.html:203, :213-214, :224; grader/*.py; tests/labs/E3/lab-E3-project-3.py", "PASS",
    "Parameter names consistent across spec, conventions, grader (gamma, lambda, kappa, zeta, xi as coordinates) and lab 3.")
row("E3e-43", "Instance docstring vs code", "course/modules/E/E3/grader/instance.py", "PASS",
    R("course/modules/E/E3/grader/instance.py", "instance.py is identical to the round-10 pin; its docstring and code were checked in round 10 and the suite passes on seeds 0-49 this round."))
row("E3e-44", "Dominance witnesses and verdict oracle (FOSD and SOSD)", "course/modules/E/E3/grader/test_project.py:1204-1236 (FOSD and SOSD tests)", "PASS",
    R("course/modules/E/E3/grader/test_project.py", "the dominance tests (now at :1204-1236) are content-identical; both run and pass in the seed-0 suite run (48 passed on reference)."))
row("E3e-45", "Failure messages name the property and do not leak the answer", "course/modules/E/E3/grader/test_project.py:44-63 and every expect()/must_raise call", "PASS",
    "Re-read the messages of the new round-11 test (:870-900): 'estimate must return exactly the seven named fields' and 'a set with a mixed A lottery is valid: every field must be a finite float' name the property and do not print values. Other messages carried.")
row("E3e-46", "Same suite passes in Pyodide and locally", "tools/page_smoke.py --unit E3 --pages project", "PASS",
    "page_smoke E3 project: PASS; in-browser grader 'All 48 tests pass on seed 100489051' (" + S + "out/page_smoke_project.out).")
row("E3e-47", "Hours: verifier estimate of each deliverable vs declared 14 h", "project.html:362-370", "PASS",
    "Hours are design targets (ruling); only arithmetic inconsistencies fail. The table sums to 14 (E3e-06). No inconsistency found.")
row("E3e-48", "SIMULATED labels where generated data is used; no real data", "project.html:44, :53, :57, :207, :376, :393, :396; grader/instance.py docstring", "PASS",
    "Rung 1 and Lab 3 labelled SIMULATED or 'not a real person'; grader instance is SIMULATED (instance.py unchanged). No real dataset read or embedded.")
row("E3e-49", "Page smoke: console errors, unrendered math, external requests, 360 px", "course/modules/E/E3/project.html; L02-L08", "UNVERIFIABLE",
    "project page: page_smoke PASS this round (" + S + "out/page_smoke_project.out). L02-L08 page_smoke was not re-run this round although those files changed (" + "not re-run this round).",
    "Run tools/page_smoke.py --unit E3 --pages L02 L03 L04 L05 L06 L07 L08 and record the output.")
row("E3e4-gates", "Repository gates for the E3 project slice", "tools/check_pages.py; check_dag.py; check_projects.py; run_labs.py; verify_refs.py; page_smoke.py; ruff; mypy", "PASS",
    "check_pages E3 PASS; check_dag E3 PASS; check_projects E3 PASS; run_labs E3 PASS (3/3); verify_refs --offline 0 problems; page_smoke project PASS; ruff PASS; mypy --no-incremental PASS; run_graders 0-49 PASS (" + S + "out/).")
row("E3e4-C2-observability", "Rubric level descriptors observable (C2)", "project.html:630-639 (C2 row), :670-675, :723-724 (annotations)", "PASS",
    "C2 descriptors name the value function formulas, the logit rule, the per-response likelihood term, the simplification and the identification pairs: all observable in a memo.")
row("E3e4-lab3-rederive", "Lab 3 numbers re-derived independently", "project.html:391-614; tests/labs/E3/lab-E3-project-3.py", "PASS",
    "Same as E3e-21: independent cross-check with grader/reference.py (" + S + "out/lab3_crosscheck_r11.out).")
row("E3e4-prizes-mixed", "Exemplar B instrument facts (prize range, prizes per lottery, probabilities sum to 1, eleven mixed)", "project.html:705-707 (exemplar B instrument)", "PASS",
    "Re-derived (" + S + "out/exemplar_b_facts_r11.out): min prize -18700, max 19000; prize counts per lottery are 2 or 3; every probability vector sums to exactly 1; pair 0 A = 6200 @ 9/10, -15100 @ 1/10 vs three prizes in B; pair 3 A = 18800 @ 3/4, -12500 @ 1/4 vs B = 16500 @ 2/5, -17700 @ 3/5 (both mixed); mixed count 11.")
row("E3e4-identification", "Identification claims (lambda identified only by mixed lotteries; precision claim is a hypothesis)", "project.html:213, :223, :719, :742", "PASS",
    "Identification convention (:223) is re-derived (see E3e-23). Exemplar B states the precision identification as 'I expect ... that is a hypothesis for you to test' (:719), so it is not asserted.")
row("E3e4-cross-refs", "Cross-references to lessons (Lesson 3 Proposition 2.7; Lesson 6 Definitions 1.2 and 1.3; Lesson 2 CE)", "project.html:53, :210, :220; L03.html:173; L06.html:61, :68; L02.html (def-certainty-equivalent)", "PASS",
    "Same as E3e-17. The L03 and L06 cited blocks were read this round.")
row("E3e4-attribution-titles", "Attribution of lesson statements about reading-list papers (title-only claims)", "course/modules/E/E3/L07.html:80; L08.html:67, :133, :619-620", "PASS",
    "Read this round: each claim names the registry title or the year, with data-locator 'registry record: title only; paper not read'. No locator, page or theorem attributed.")
row("E3e4-stretch-phi", "Stretch probit link: Phi against the registry", "project.html:775; notation/notation.json (Phi, module M4)", "PASS",
    "Phi in the stretch = standard normal distribution function, which is the registry meaning ('standard normal CDF and its inverse', M4).")
row("E3e4-ruling-392", "Plan's exemplar wording agrees with the architect ruling on excerpts", "plans/E3-build-plan.md:392; plans/E3-open-items.md:145-149; plans/FINAL-ARCHITECT-RULINGS.md item 7", "PASS",
    "Excerpts: the plan's wording says excerpts (line 392 area) and the page says excerpts (:646). The level mismatch (B level 3 vs plan 4) is E3e4-exemplar-B-level, not this row. The ruling's word counts (103, 375) do not match the page (117, 450); noted in E3e-13.")
row("E3e5-01", "Rung 1 worked example: each step carries a why note (plan 6.1 item 1)", "tests/labs/E3/lab-E3-project-1.py:58-137; project.html:55-57, :138", "PASS",
    "Each step in main() and the helper functions carries a comment and docstring (verified by reading the twin; page code equals twin).")
row("E3e5-02", "Grader test file type-clean under mypy --strict", "course/modules/E/E3/grader/test_project.py", "PASS",
    "run_graders typecheck in the workspace (mypy --strict --ignore-missing-imports with elicit.py and instance.py): PASS. Standalone run of the file alone reports import-not-found and three unused-ignore lines; that is the missing sibling module, not a defect of the gate.")
row("E3e5-04", "Prospect model extends Lesson 6 Definition 1.3 (p_i > 0) to zero-probability prizes", "project.html:220, :225; L06.html:68-69", "PASS",
    "L06.html:68-69 requires p_i > 0; project.html:225 says 'A probability of exactly zero is allowed' and the engine's prospect sum ignores zero-probability terms (a zero term adds 0), so the value is the same. Stated as an extension on the page.")
row("E3e5-05", "Hub ladder text agrees with the spec", "course/modules/E/E3/index.html:146; project.html:207, :213", "PASS",
    "index.html is byte-identical to the round-10 pin; its ladder text describes the same engine, instrument, report and autograder as the spec.")
row("E3e6-01", "Lab-E3-project-3 docstring describes code that exists", "tests/labs/E3/lab-E3-project-3.py:4-6 (embedded at project.html:398-399)", "PASS",
    "Docstring (page :398-402) says the estimates are printed and the file is copied as run_case.py; the replace-the-body instruction is inconsistent with main's largest_score key (E3e-r11-lab3-estimate-keys).")
row("E3e-r8-01", "Rung 1 text: 'answers written into the lab ... not generated from the parameters'", "course/modules/E/E3/project.html:44; tests/labs/E3/lab-E3-project-1.py:54-58", "PASS",
    "Lab 1 answers are literal lists in pairs (:111-115); the text states they are not generated from the parameters.")
row("E3e-r8-02", "Whole-cents exception at gamma = 0 (CRRA): exact Fraction sum before the single rounding", "course/modules/E/E3/project.html:221; grader/reference.py:122-124", "PASS",
    "reference.py:121-124: at gamma 0 the expected change is summed as a Fraction and rounded with floor(x + 1/2): exact. The page states the same. Prospect gamma 0 is NOT in the exception (see E3e-r11-half-cent-prospect-gamma0).")
row("E3e-r8-03", "Exemplar B C4 misses text (round-8 change at :720)", "course/modules/E/E3/project.html:745-749", "PASS",
    "Annotation at :747 states the miss (no direction of bias) and matches the C4 level-4 descriptor.")
row("E3e-r8-04", "Grader test messages changed at :251-288", "course/modules/E/E3/grader/test_project.py:251-288", "PASS",
    R("course/modules/E/E3/grader/test_project.py", "the passage is content-identical (the round-11 hunks are at :665-668 and :870-900); messages name the property and do not print the answer."))
row("E3e-r8-05", "Lesson 2 hypothesis (:209): \\Var macro, numbers and predictions", "course/modules/E/E3/L02.html:209; tests/labs/E3/lab-E3-L02-1.py", "UNVERIFIABLE", LESSON_NOT_REREAD, LESSON_FIX)
row("E3e-r8-06", "Lesson 4 hypothesis and :493 bullet", "course/modules/E/E3/L04.html:98, :150, :176, :493; tests/labs/E3/lab-E3-L04-1.py", "UNVERIFIABLE", LESSON_NOT_REREAD, LESSON_FIX)
row("E3e-r8-07", "FINAL-ARCHITECT-RULINGS item 11 (rung 2 completion blanks) and the lab twin", "plans/FINAL-ARCHITECT-RULINGS.md:24-25; tests/labs/E3/lab-E3-project-2.py; course/modules/E/E3/project.html:151-196", "PASS",
    R("plans/FINAL-ARCHITECT-RULINGS.md and tests/labs/E3/lab-E3-project-2.py", "the ruling file and the twin are identical; the page shows the blanked code and the twin is the completed solution (verified by page_vs_twin_r11.out)."))
row("E3e-r9-01", "Dominance and identification sentences on the page match the suite", "project.html:213, :223; grader/test_project.py:1204-1236", "PASS",
    "The dominance sentence matches the FOSD and SOSD tests (both pass); the identification sentence matches the test file's mixed-lottery tests (run pass).")
row("E3e-r9-02", "Grader docstring claim: lambda 'has kinks where a certainty equivalent changes sign'", "course/modules/E/E3/grader/test_project.py:586-598", "PASS",
    R("course/modules/E/E3/grader/test_project.py", "the local-maximum test passage is content-identical; the claim is not a page statement."))
row("E3e-r9-03", "Suite coverage of large lambda (lambda_hat above 10)", "course/modules/E/E3/grader/test_project.py:645-695 (test_estimate_on_a_large_loss_aversion_participant_is_also_a_maximum)", "PASS",
    "The test exists and runs on the reference (seed-0 suite: passes). Its docstring at :665-668 changed in this round (the sentence about the bracketing search was removed); the coverage is unchanged. The test also fails alt1 and alt2 (E3e-32), which is the intended kill behaviour for a clamp at 10.")
row("E3e-r9-04", "Questionnaire regex accepts and rejects the stated probability forms", "project.html:273 (isProbability)", "PASS",
    "Re-tested in node (" + S + "rx_r11.js): '0', '1', '1/2', '9/10', '10/20' accepted; '1/0', '0/0', '-1/2', '1.0', '1/2/3', '', '01', '1/' rejected.")
row("E3e-r9-05", "Ladder placement sentence matches the hub's placement rule", "project.html:42; index.html:66-67, :142", "PASS",
    "index.html:66 is the placement section (id placement, eight questions, mastery 80 percent); :142 states the skip rule; project.html:42 matches.")
row("E3e-r9-06", "Lab 1 nearest_cent docstring matches the twin", "project.html:74; tests/labs/E3/lab-E3-project-1.py:17", "PASS",
    "Docstring 'The nearest whole cent of a float amount in cents, with an exact half going up' matches the code math.floor(amount + 0.5) and the twin (page == twin).")
row("E3e-51", "Docstring numbers in the new grader test (whether-or-not-chosen fixture)", "course/modules/E/E3/grader/test_project.py:903-928", "PASS",
    R("course/modules/E/E3/grader/test_project.py", "the passage is content-identical (the round-11 insertion is at :870-900, above it)."))
row("E3e-52", "New grader fixture facts: the B-side lotteries are mixed", "course/modules/E/E3/grader/test_project.py:845-871 (fixture B_SIDE_LOTTERIES)", "PASS",
    R("course/modules/E/E3/grader/test_project.py", "the fixture is content-identical; the round-11 insertion reuses it (A-side test at :873-900) and passes on the reference."))
row("E3e-53", "New zero-prize test: a gain and a zero prize is not mixed", "course/modules/E/E3/grader/test_project.py:703-795, :797-843", "PASS",
    R("course/modules/E/E3/grader/test_project.py", "the passage is content-identical."))
row("E3e-54", "Round-7 verifier mutants: three new student-error mutants, each killed", "ledgers/E3/mutants/r7_01_*.py, r7_02_*.py, r7_03_*.py", "PASS",
    "Files byte-identical to the round-10 pin (git diff --quiet 47a36d8c ccaeeaf); killed in " + S + "out/mutate_E3_seeds0-9.out (e.g. r7_01 by test_crra_requires_wealth_plus_every_prize_to_stay_positive, seed 0).")
row("E3e-55", "Round-7 Lesson 2 prose", "course/modules/E/E3/L02.html:84, :136, :381, :399, :616", "UNVERIFIABLE", LESSON_NOT_REREAD + " (L02.html:616 read this round and verified in E3e-15)", LESSON_FIX)
row("E3e-56", "Round-7 Lesson 3 references (Module M1 results cited)", "course/modules/E/E3/L03.html:564; course/modules/M/M1/L03.html", "UNVERIFIABLE", LESSON_NOT_REREAD, LESSON_FIX)
row("E3e-57", "Round-7 Lesson 4 prose", "course/modules/E/E3/L04.html:52, :165-172, :176, :485, :493, :573-579, :591", "UNVERIFIABLE", LESSON_NOT_REREAD, LESSON_FIX)
row("E3e-58", "Round-7 Lesson 7 numbers", "course/modules/E/E3/L07.html:86, :88, :92, :98, :127, :334, :336-338, :505", "UNVERIFIABLE", LESSON_NOT_REREAD, LESSON_FIX)
row("E3e-59", "Round-7 Lesson 8 prose", "course/modules/E/E3/L08.html:142-160, :412-419, :425, :477, :496, :683, :697", "UNVERIFIABLE", LESSON_NOT_REREAD, LESSON_FIX)
row("E3e-60", "Round-7 hub reading paragraph and the Lesson 2 and 3 'name only' statements", "course/modules/E/E3/index.html:166; L01.html; L02.html:616; L03.html:564", "UNVERIFIABLE", LESSON_NOT_REREAD + " (index.html:166 and L02.html:616 read; L01.html and L03.html:564 not)", LESSON_FIX)
row("E3e-r11-hunks-lessons", "Every changed lesson, hub, reference and notation hunk since 47a36d8c read for prose, notation, attribution and links", "course/modules/E/E3/L01-L08.html; index.html; references/references.json; notation/", "PASS",
    "The 70 changed lines in those files were read (git diff -U0 47a36d8c ccaeeaf). Notation: kappa as CARA coefficient (L01), phi/eta (L03), alpha (L02 F6): no registered symbol. Attribution: no new citation; the only key change is in BK4/LX1 used_by. Links: E3 links resolve (E3e-04). Numbers inside the changed lesson lines were not re-derived (lesson slices).")

row("E3e-50", "Over-constraint: a correct implementation that the SE or suite wrongly rejects", "course/modules/E/E3/grader/test_project.py:1064-1120 (SE oracle); ledgers/E3/scripts/E3-e-r11/out/alts/", "PASS",
    "The standard-error test (test_standard_errors_match_the_coordinate_change_oracle) passes on the reference and on alt5_exp_log_float (full suite, seed 0: 48 passed). No alternative failed the SE test; the failing alternatives fail on the optimiser or the exact-half test (E3e-32, E3e-r11-half-cent-prospect-gamma0).")

json.dump(ROWS, sys.stdout, ensure_ascii=False, indent=1)
