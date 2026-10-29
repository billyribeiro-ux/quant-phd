"""Writes ledgers/E3/E3-d.json (round 2, verifier for E3 slice d). Rows carry the evidence named in each row.

Run from the checkout: .venv/bin/python ledgers/E3/scripts/E3-d-r2/write_fragment_r2.py
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OUT = ROOT / "ledgers" / "E3" / "E3-d.json"
D = "ledgers/E3/scripts/E3-d-r2"
MUT_LOG = ROOT / D / "logs" / "mutate_E3.out"

ROWS = [
    ("E3d-labs-run", "2.5 labs: run_labs --unit E3 and the three project twins under python -I -W error",
     "tests/labs/E3/lab-E3-project-1.py, -2.py, -3.py; course/modules/E/E3/project.html lines 55-188, 267-463",
     "PASS", "tools/run_labs.py --unit E3: 'run_labs E3: PASS (11/11)'. Each project twin run with python -I -W error: exit 0, "
     "stdout equal to the page's expected blocks (project.html lines 131-137, 183-186, 457-463). Page smoke PASS (E3d-r2-page-smoke)."),
    ("E3d-lab1-numbers", "2.2 lab 1 printed numbers and the prose claims about them",
     "course/modules/E/E3/project.html lines 57, 138; tests/labs/E3/lab-E3-project-1.py",
     "PASS", "Lab 1 output: CRRA cents 496/500 and prospect -30/500 (pair 1); P(A) 0.480149; log P -0.733658; total -2.302315. "
     "The pair-2 claim 'a sure $30.00 gain ... loses $20.00 with probability 3/4 ... -762 cents' matches the output (3000 both; -762)."),
    ("E3d-lab2-numbers", "2.5 lab 2 completed lines and the interpretation",
     "course/modules/E/E3/project.html lines 143, 183-187; tests/labs/E3/lab-E3-project-2.py",
     "PASS", "Run output -0.765595182 (A) and -0.625595182 (B); probabilities 0.465057055 and 0.534942945; z = -0.14 "
     "(2*(1500-2200)/10000). Recomputed by hand: -log(1+e^0.14) = -0.765595; -log(1+e^-0.14) = -0.625595."),
    ("E3d-lab3-reproduced", "2.5 lab 3 reference case reproduces the printed estimates",
     "tests/labs/E3/lab-E3-project-3.py; course/modules/E/E3/project.html lines 269-463",
     "PASS", "Run (python -I -W error): answers 12, mixed 11, gamma_hat 0.6352 (se 0.32), lambda_hat 6.1503 (se 9.59), kappa_hat "
     "2.0201 (se 1.86), log-likelihood -7.1445, largest score 3.55e-10, domain True: exactly the page's expected block "
     "(project.html lines 457-463). Output saved at /tmp/e3d-v2/lab3.out."),
    ("E3d-lab3-mixed-count", "2.2 'eleven of the twelve pairs contain a mixed lottery'; 'one pair ... gain and loss'",
     "course/modules/E/E3/project.html lines 269, 557, 569; lab-E3-project-3.py mixed_pair()",
     "PASS", "Lab 3 prints 'mixed-sign answers: 11' (line 457). Pair 3 of exemplar B (line 557) matches ANSWERS[3]: 18800/3/4, "
     "-12500/1/4 vs 16500/2/5, -17700/3/5, both mixed."),
    ("E3d-lab3-provenance", "2.5/1.3 honest data: 'SIMULATED' label on the twelve Lab 3 answers",
     "course/modules/E/E3/project.html lines 265, 269; tests/labs/E3/lab-E3-project-3.py lines 271-275 and ANSWERS (lines 288-301)",
     "FAIL", "The twelve answers are not reproducible from the stated generator. Script ledgers/E3/scripts/E3-d-r2/match_lab3.py "
     "ran make_instance(s) for seeds 0 to 199 and compared the first 12 responses (pair, choice, prizes, probabilities) "
     "with the lab data: no seed matches (output []). The lab text says 'this file does not record how they were drawn', "
     "while project.html line 269 and the lab docstring call them SIMULATED. A SIMULATED label needs its generator (seed and script) "
     "or the data must be called hand-written illustrative data.",
     "Either record the seed and generator that produced the twelve answers (and cite make_instance or a named generator) "
     "or state on the page that the twelve answers are fixed illustrative data, not SIMULATED output; then reword lines 265 and 269."),
    ("E3d-exemplar-B-numbers", "2.2 exemplar B numbers (prize range, pairs, estimates, score component)",
     "course/modules/E/E3/project.html lines 557, 580, 591",
     "PASS", "Prize range computed over the 12 answers: min -18700 (pair 10, B), max 19000 (pair 1, A): matches '-18 700 and 19 000'. "
     "Each lottery has two or three prizes. Pair 0 and pair 3 values match ANSWERS. Estimates, SEs, score 3.55e-10, log-likelihood -7.1445 match Lab 3."),
    ("E3d-grader-count", "2.9 'the suite runs 35 checks' (project.html line 203)",
     "course/modules/E/E3/project.html line 203; course/modules/E/E3/grader/test_project.py",
     "PASS", "grep -c '^def test_' = 35; pytest -q on the reference, seed 0: '35 passed in 0.70s'."),
    ("E3d-grader-reference", "2.5 grader: reference passes all seeds 0 to 49; instance and starter clean",
     "course/modules/E/E3/grader/reference.py, test_project.py, instance.py, starter.py",
     "PASS", "tools/run_graders.py --unit E3 --seeds 0-49: 'run_graders E3: PASS (reference 50/50 seeds, slowest 1.8 s)'."),
    ("E3d-grader-alt-correct", "Architect ruling (b): five correct alternative implementations must pass; witness for any over-constraint",
     "ledgers/E3/scripts/E3-d-r2/logs/alternatives_seeds_0_49.out; ledgers/E3/scripts/run_alternatives.py (alt1 to alt5); "
     "ledgers/E3/scripts/E3-d-r2/run_alt_one.py; ledgers/E3/scripts/E3-d-r2/zero_prob_witness.py",
     "FAIL", "Seeds 0 to 49, each alternative built from grader/reference.py by function replacement and the suite run unchanged: "
     "alt1 (grid, compass search, Newton) 50/50; alt2 (grid, Newton) 50/50; alt3 (grid, Nelder-Mead, Newton) 50/50; alt5 (Decimal "
     "half-up) 50/50; alt4 (bisection inversion of the prospect value) 46/50. alt4 fails "
     "test_zero_probability_prize_contributes_nothing_to_the_likelihood on seeds 26, 29, 44 and 45 because the test asserts exact "
     "float equality (test_project.py: 'sol.log_likelihood(with_zero, TRUE) == sol.log_likelihood(without, TRUE)'). Witness "
     "(zero_prob_witness.py): seed 26 with_zero -0.686057491958889, without -0.6860574919588889, difference -1.1e-16. Page line 214 "
     "requires only that a zero-probability prize is allowed; no bit-exact equality is stated.",
     "In test_project.py replace the exact equality at the zero-probability test (around line 605) with abs difference <= 1e-9, "
     "as the other likelihood tests do."),
    ("E3d-grader-mutants-listed", "2.5/2.7 mutation testing of the project grader: every mutant in ledgers/E3/mutants is killed",
     "ledgers/E3/mutants/*.py (32 files); tools/mutate_graders.py --unit E3",
     "PASS", "tools/mutate_graders.py --unit E3: 'mutate_graders E3: PASS (32/32 killed)' (full output logs/mutate_E3.out). "
     "Builder mutants f01-f10 and m01-m10 killed; verifier round-1 v01-v05 killed; round-2 student errors w01-w07 killed (see mutants list)."),
    ("E3d-cards-numbers", "2.2 numbers on cards (cards.json) against their lesson text",
     "course/modules/E/E3/cards.json; L01-L08.html; ledgers/E3/scripts/E3-d-r2/card_numbers.py",
     "PASS", "Every number on every card (158 cards) is found literally in its own lesson (tag-stripped text), except E3-c150's "
     "1.072330, which is present in L08.html line 438 with a tag split; recomputed by hand: 5 - sqrt(50) = -2.071068; "
     "Model 2 gives c = -((2.071068)/2)^2 = -1.072330 and wealth 100000 - 107.233 = 99892.7670 cents. Also E3-c014 (45000, 22500) "
     "matches L01 line 343; E3-c034 (11.17%, 12.57%) recomputed 11.1696% and 12.5741%; E3-c055 1/M = 80000/9 = 8888.89 with "
     "M = 9/80000 recomputed; the L07 weight cards (cards.json lines 901 and 908) 0.57158177 and 0.39125077 recomputed from the L07 closed form; card at cards.json line 915 "
     "49.8328 = sum omega(p_i) x_i recomputed."),
    ("E3d-cards-lesson-claims", "2.7 every card checked against the current lesson text it comes from",
     "course/modules/E/E3/cards.json (158 cards); L01-L08.html",
     "UNVERIFIABLE", "Checked this round: all 158 section/proposition/remark/definition/problem references in cards resolve in "
     "their own lesson (ledgers/E3/scripts/E3-d-r2/cards_xref.py); all 16 'section N, ordinal misconception' references resolve to a list item; "
     "the semantic claim was checked against the lesson for 12 cards (c014, c034, c055, c150, c-misconception cards, the L07 "
     "weights and the L07 c915 example, L05 and L06 cards changed this round). The remaining cards' prose was not re-read line by line.",
     "Re-read the remaining cards against their lesson sections, one lesson at a time."),
    ("E3d-cards-duplicates", "2.7 full duplicate scan of cards",
     "course/modules/E/E3/cards.json",
     "PASS", "difflib pairwise on fronts: only pair with ratio > 0.85 is E3-c004 / E3-c018 (0.94), which are assumptions A1 and A2 "
     "of different lessons (different content); no duplicate ids (check_pages E3 PASS)."),
    ("E3d-cards-cross-refs", "2.7 card cross-references to lessons, cards and problems",
     "course/modules/E/E3/cards.json; L0*.html",
     "PASS", "158 references of kind Proposition/Remark/Theorem/Definition/Corollary/Example/Lemma/Problem/Assumption resolve in the "
     "named lesson text, except 'Problem E2' (E3-c034 L02, E3-c055 L03), which exist as problem E2 in the problem set of each "
     "lesson (L02 line 463 'E2 · The approximation error...'; L03 line 411 'E2 · Checking the exact gamma 2 value'). Card "
     "numbers match those problems. The round-1 dangling-reference failure is resolved."),
    ("E3d-conventions-formulas", "2.4 conventions and formulas of project.html against reference.py",
     "course/modules/E/E3/project.html lines 210-214; grader/reference.py lines 71-128, 156-166",
     "PASS", "Half cent: floor(c+1/2) (reference _half_up line 73; alt5 Decimal). Choice probability with /10000 (reference line 20). "
     "Logit log P(A) and log(1-P(A)) for B (reference line 162). Standard errors by delta method in (eta, log lambda, log kappa) "
     "(reference docstring; test_project.py lines 694-714). Value and inverse of the prospect model match lines 85-97. "
     "Notation: c used only as the sure change on page line 210, eta for the log-odds on line 213."),
    ("E3d-dag-concepts", "DAG: concepts used in the project and their links; unlinked names",
     "course/modules/E/E3/project.html lines 53, 201, 213, 623 and 630; L02, L06 and L07 definitions",
     "PASS", "Links resolve: certainty-equivalent -> L02 #def-certainty-equivalent; loss-aversion and prospect-theory -> L06 "
     "#def-loss-aversion and #def-prospect-theory (all present in L0*.html). check_dag E3 PASS. Unlinked names (logit, probit, "
     "probability weighting) are E3's own or plain prose per plan section 7; probability weighting is defined in L07."),
    ("E3d-tools-gates", "2.5 gate scripts for the slice: check_pages, check_dag, check_projects, ruff",
     "tools/check_pages.py --all; tools/check_dag.py --all; tools/check_projects.py --all; ruff on grader and labs",
     "PASS", "check_pages E3: PASS; check_dag E3: PASS; check_projects E3: PASS; ruff check and ruff format --check on "
     "course/modules/E/E3/grader and tests/labs/E3: 'All checks passed!', '15 files already formatted'."),
    ("E3d-references", "2.1 the five registry keys the page names and the lessons cite",
     "references/references.json; course/modules/E/E3/project.html lines 628-637; L02 references section; L05-L08 data-cite",
     "FAIL", "The five keys exist in references.json (kahneman1979prospect, pratt1964risk, epstein1989substitution, "
     "ellsberg1961risk, gilboa1989maxmin, status verified). But the page says 'The lessons cite five registry keys', and no "
     "lesson carries data-cite=\"pratt1964risk\": L02 names Pratt (1964) by name only (L02 section 9 says it 'cites that work for "
     "the name only'). The sentence also describes the Epstein-Zin, maxmin, prospect and certainty-equivalent uses but not "
     "Ellsberg (1961), which L08 cites.",
     "Change the sentence to 'The lessons cite four registry keys, and Pratt (1964) by name' and list Ellsberg (1961) with its use in Lesson 8."),
    ("E3d-grades", "2.3 grades on the project page",
     "course/modules/E/E3/project.html lines 496-611 (exemplars), 603 (exemplar B evidence)",
     "PASS", "Exemplar B evidence line 603 now grades the Lab 3 numbers C with basis 'Lab 3 (SIMULATED)' (ruling e); no T for "
     "results read off the lab. Exemplar A and B annotations cite grade and key or derivation."),
    ("E3d-hours", "2.8 hours: declared and arithmetic",
     "course/modules/E/E3/project.html lines 238-244 and data-hours-project=14 (line 33); index.html line 127; lesson data-hours",
     "PASS", "Project rows 1+1+3+4+3+2 = 14 = data-hours-project. Hub: 8 lessons x 7 h (data-hours=7 in L01-L08) = 56, plus project 14 = 70. "
     "Pace not judged (architect ruling)."),
    ("E3d-hub-mixed-pairs", "2.4 project specification against the hub's description of the project",
     "course/modules/E/E3/index.html line 146; project.html line 197",
     "FAIL", "index.html line 146: 'design an instrument of at least 12 mixed-sign pairs'. project.html line 197 requires 'at least 12 "
     "pairs ... and at least one pair in the instrument has a lottery that mixes a gain and a loss'. The hub asks for 12 mixed-sign pairs, "
     "which the project does not require.",
     "Change the hub to 'at least 12 pairs, with at least one mixed-sign lottery' (the hub is outside this slice; the owner of index.html must edit it)."),
    ("E3d-signatures", "2.4 starter signatures against the spec",
     "course/modules/E/E3/grader/starter.py lines 9-35; project.html lines 197-199",
     "PASS", "certainty_equivalent_cents(model, prizes_cents, probabilities, params, wealth_cents) -> int; log_likelihood(responses, params); "
     "estimate(responses): identical to project.html line 199 and the starter."),
    ("E3d-fail-se-untested", "2.5 round-1 FAIL: standard errors had no oracle test",
     "course/modules/E/E3/grader/test_project.py lines 694-714 (test_standard_errors_match_the_delta_method_oracle)",
     "PASS", "The delta-method oracle test now exists and is run (seeds 0-49 pass for the reference). Mutant v01 (no delta factor) is "
     "killed (logs/mutate_E3.out)."),
    ("E3d-fail-unchosen-term", "2.4 round-1 FAIL: log(1-P(A)) described as the unchosen alternative's term",
     "project.html lines 187, 471, 487, 521; test_project.py lines 388-413; reference.py lines 166-168",
     "PASS", "All four statements now say log(1-P(A)) is the log-probability of B for a response that chose B. The oracle test (line 408-412) "
     "checks log P(A) for A and log(1-P(A)) for B."),
    ("E3d-fail-lab3-maximum", "2.4 round-1 FAIL: Lab 3 claimed a maximum",
     "project.html lines 269, 464",
     "PASS", "Line 269 now says the search stopped at a stationary point; line 464 says the lab does not check that the point is a maximum."),
    ("E3d-fail-instance-docstring", "2.4 round-1 FAIL: instance.py docstring used /100",
     "course/modules/E/E3/grader/instance.py lines 14-15; reference.py line 166 docstring",
     "PASS", "instance.py line 14 now reads 'kappa (CE_A - CE_B) / 10000 ... the difference is taken in units of $100'; "
     "the code uses _CENTS_PER_UNIT = 10_000.0 (line 49, 126). reference.py docstring line 167 now has /10000."),
    ("E3d-fail-notation-c", "2.4 round-1 FAIL: symbol c with two meanings",
     "project.html lines 210, 213",
     "PASS", "c is now used once (the sure change, line 210); the log-odds coordinate is eta (line 213). notation/notation.json "
     "registers none of these symbols."),
    ("E3d-fail-exemplar-B-grade", "2.3 round-1 FAIL: exemplar B graded T", "project.html line 603",
     "PASS", "Line 603 grades the lab-derived numbers C with basis 'Lab 3 (SIMULATED)'."),
    ("E3d-fail-unenforced-claims", "2.4 round-1 FAIL: claims about checks the suite does not enforce",
     "project.html lines 201, 223; test_project.py lines 286-297 and 722-747",
     "PASS", "Printing is checked (capsys in test_engine_imports_only...), imports are checked (ast), warnings are errors (pytestmark "
     "filterwarnings and -W error). The model-name test now requires both 'crra' and 'prospect' in the message, as the table says."),
    ("E3d-fail-message-overconstraint", "2.4 round-1 FAIL: message wording over-constrained",
     "test_project.py lines 515-563; project.html line 226",
     "PASS", "Witness run: ledgers/E3/scripts/E3-d-r2/msg_variant.py (reference with 'no answers given' and 'no lottery pays both a gain and "
     "a loss'): 35 passed on seeds 0, 1 and 2."),
    ("E3d-fail-recovery-criterion", "2.4 round-1 FAIL: recovery within five SE not stated",
     "project.html line 203 ('The five-standard-error tolerance of the recovery check is a tolerance of this suite'); test_project.py lines 486-497",
     "PASS", "The page now states the tolerance and that it is not a coverage claim. Alternatives pass the check on seeds 0-49."),
    ("E3d-fail-exemplar-B-causal", "2.4 causal and directional claims in exemplar B",
     "project.html line 591 ('A noisy choice can confound curvature with precision when the pairs are close.')",
     "FAIL", "The round-1 forecast is now hedged ('I expect ... a hypothesis for you to test'), but the preceding sentence states a "
     "directional confounding claim as fact ('can confound ... when the pairs are close') with no computation, lab or test behind it; "
     "Lab 3 does not compute a correlation or a design comparison.",
     "Hedge the sentence as a hypothesis for the reader to test, as the next sentence does, or give the computation."),
    ("E3d-fail-cards-dangling-problem", "2.7 round-1 FAIL: cards named a problem that did not exist",
     "cards.json E3-c034 (L02), E3-c055 (L03)",
     "PASS", "Problem E2 exists in both lessons (L02 line 463; L03 line 411); the numbers are the problem solutions (see E3d-cards-numbers)."),
    ("E3d-fail-cards-misconception-numbers", "2.7 round-1 FAIL: misconception ordinals not checkable",
     "cards.json (16 cards: E3-c014, c029, c031, c051, c053, c072, c090, c092, c112-c114, c130-c132, c154-c156)",
     "PASS", "Each card now reads 'section N, <ordinal> misconception'; each lesson section N (s4/s5/s6 headed 'Misconceptions') has an ordered "
     "ol with at least that many items (scripted check of all 16)."),
    ("E3d-fail-exemplar-A-rounding", "2.2 round-1 FAIL: exemplar A rounded parameters to two decimals",
     "project.html lines 477, 516",
     "PASS", "Line 516 now gives 0.6352, 6.1503 and 2.0201, the four-decimal values printed by Lab 3, as line 477 requires."),
    ("E3d-fail-exemplar-A-c1-basis", "2.3 exemplar A annotation cites a level-2 descriptor the rubric does not contain",
     "project.html line 508 (annotation for C1 level 2) and line 486 (rubric C1 level 2)",
     "FAIL", "Rubric C1 level 2 reads 'States the number of pairs or the scale, but not both, or gives the reason for the losses without an "
     "example pair'. The annotation says exemplar A 'meets C1 level 2: states the count and the scale', which is the first clause with "
     "'not both' removed. Exemplar A meets level 2 only through the second clause (the reason for the losses, no example pair).",
     "Change the annotation to cite the second clause: 'gives the reason for the losses without an example pair'."),
    ("E3d-reference-deployment", "2.10 BLUEPRINT: grader/reference.py excluded from deployment",
     "course/modules/E/E3/grader/reference.py line 1-3; BLUEPRINT.md lines 400-401",
     "UNVERIFIABLE", "No deployment or publish configuration in this repository excludes grader/reference.py (grep over tools/ and the root: "
     "only check_projects.py line 132 and page_smoke.py line 297, which reads the reference from the course tree). The publish step is outside "
     "this checkout, so the exclusion could not be confirmed.",
     "Show the publish step's exclusion rule for grader/reference.py, or add one."),
    ("E3d-mutants-new", "2.5 project mutants: at least three new student-error mutants, all killed",
     "ledgers/E3/mutants/w01-w07 (generated by ledgers/E3/scripts/E3-d-r2/make_mutants.py from grader/reference.py)",
     "PASS", "Seven new mutants: w01 CRRA uses the prize as final wealth; w02 B-response uses log P(A); w03 estimate needs every response mixed; "
     "w04 prospect loss inverse multiplies by lambda; w05 half cent away from zero; w06 likelihood uses rounded cents; w07 gamma_hat is eta. "
     "All killed on seed 0 (logs/mutate_E3.out)."),
    ("E3d-r2-half-cent-margins", "2.4 the grader docstrings claim the instance keeps every value clear of a half cent",
     "course/modules/E/E3/grader/test_project.py lines 150-152, 212-213; ledgers/E3/scripts/E3-d-r2/halfcent.py",
     "PASS", "Over seeds 0-49, first 40 responses, both lotteries: closest CRRA certainty equivalent to a half-cent boundary is 6.6e-6 cents "
     "(seed 41); closest prospect value 8.5e-5 cents (seed 35). Far above float error, so the claim holds."),
    ("E3d-r2-page-smoke", "2.5 page_smoke for the project page in Chromium", "tools/page_smoke.py --unit E3 --pages project.html",
     "PASS", "'page_smoke E3: PASS' (logs in this round)."),
    ("E3d-r2-notation", "2.4 notation conformity against notation/notation.json",
     "notation/notation.json (8 registered symbols); project.html and L01-L08 math", "PASS",
     "Scanned every TeX segment (ledgers/E3/scripts/E3-d-r2/math_scan.py): no use of T (number of observations), R^ast, R^{e ast}, R_f, "
     "Q as a measure, gamma_3, gamma_4 in the E3 pages; \\Phi is used only as the standard normal CDF (stretch, project.html line 623), the "
     "registered meaning. Other symbols are local (gamma, lambda, kappa, CE, V, W, P, eta). Note (outside this slice): L05.html uses plain Q for a plan, "
     "not the registered \\mathbb{Q}; it is not the same symbol."),
    ("E3d-fail-estimate-not-global-mle", "2.4 estimate is described as the maximum-likelihood estimate; the reference is not the global maximum on seed 49",
     "course/modules/E/E3/project.html line 7 (meta description); grader/starter.py line 34; grader/reference.py line 282; ledgers/E3/scripts/E3-d-r2/se49b.py",
     "FAIL", "On seed 49 the reference estimate has log-likelihood -126.03154 (gamma 0.70625, lambda 20.686, kappa 2.2797, se_lambda 135.0). "
     "alt1 (grid, compass search, Newton) on the same responses has log-likelihood -125.93152 (gamma 0.68656, lambda 7.2176, kappa 2.3587, "
     "se_lambda 3.57), which is higher. Both pass all 35 checks on seed 49 (run in a temp directory). The suite checks only a local maximum "
     "(test_estimate_is_a_local_maximum), so it accepts either, but the page's meta description and the starter and reference docstrings "
     "say 'maximum-likelihood estimates', which the reference does not deliver on seed 49.",
     "Either make the reference search from several starts and return the highest likelihood, and say so on the page, or state on the page and in "
     "the starter that the estimate is a local maximum from the grid start."),
    ("E3d-fail-seed49-docstring-number", "2.2 number in a grader docstring: 'two correct engines differ by about 4% in se_lambda' on seed 49",
     "course/modules/E/E3/grader/test_project.py lines 698-701 (_observed_information docstring of the delta-method test)",
     "FAIL", "Measured on seed 49: the reference se_lambda is 135.009 and alt2 is 138.354 (2.5% apart), alt4 140.117 (3.8%), but alt1 and alt3 "
     "(both passing correct engines) report se_lambda 3.573 and 3.573, which is 97% below the reference, at a different local maximum. "
     "The sentence understates the disagreement between correct engines (ledgers/E3/scripts/E3-d-r2/se49.py output).",
     "Replace the sentence with the measured fact: on seed 49 correct engines reach different local maxima, and standard errors differ by up to "
     "an order of magnitude; or remove the number."),
]

FAILED_ALTS = None


def mutants() -> list[dict[str, str]]:
    out = []
    pattern = re.compile(r"^(KILLED|SURVIVED) (\S+?)\.py: (.*?) -> (.*)$")
    for line in MUT_LOG.read_text(encoding="utf-8").splitlines():
        m = pattern.match(line)
        if not m:
            continue
        status, name, desc, killed = m.groups()
        origin = "builder" if name[0] in "fm" and name[1:3].isdigit() and name[0] in "fm" else "verifier"
        if name.startswith("w"):
            origin = "verifier round 2 (new)"
        elif name.startswith("v"):
            origin = "verifier round 1"
        entry = {"id": name, "description": desc, "status": status}
        if status == "KILLED":
            entry["killed_by"] = killed
        entry["origin"] = origin
        out.append(entry)
    return out


def main() -> None:
    rows = []
    for item in ROWS:
        rid, check, location, status, evidence, *fix = item
        row = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
        if status != "PASS":
            row["fix"] = fix[0] if fix else ""
        rows.append(row)
    muts = mutants()
    killed = sum(1 for m in muts if m["status"] == "KILLED")
    verdict = "PASS" if all(r["status"] == "PASS" for r in rows) and killed == len(muts) else "FAIL"
    fragment = {
        "unit": "E3",
        "slice": "E3-d",
        "round": 2,
        "verifier": "Claude Haiku 5.5 (independent verifier, unit E3 slice d, round 2; did not build E3)",
        "pin": "e22feb3 (detached checkout /tmp/verifyC2-E3-d)",
        "base": "55b5634 (round-1 pin; delta: project.html, grader/instance.py, grader/reference.py, grader/test_project.py, cards.json, tests/labs/E3/lab-E3-project-3.py)",
        "checkout": "/tmp/verifyC2-E3-d",
        "scratch": "/tmp/e3d-v2",
        "verified_at": "2026-10-28T19:30:00-04:00",
        "verdict": verdict,
        "rows": rows,
        "mutants": muts,
        "registry_flags": [],
        "freshness_flags": [],
        "notes": (
            "Round 2. Counts: rows {n}, PASS {p}, FAIL {f}, UNVERIFIABLE {u}; mutants {mk}/{mt} killed (builder f01-f10 and m01-m10, "
            "verifier round 1 v01-v05, verifier round 2 w01-w07). Alternatives: alt1, alt2, alt3, alt5 pass 50/50 seeds; alt4 46/50 "
            "(zero-probability exact-equality test). Reference 50/50. Not checked: the cards' prose beyond the sampled cards "
            "(E3d-cards-lesson-claims); the publish step (E3d-reference-deployment); the lesson pages L01-L08 beyond the card-side "
            "reads (other slices); live registry fetch (verify_refs.py was not run in this slice); exemplar scores were not re-scored "
            "blind (the self-assessment form is JavaScript-only). The seed-49 engine disagreement (E3d-fail-estimate-not-global-mle) is "
            "recorded below as an extra row."
        ).format(
            n=len(rows),
            p=sum(r["status"] == "PASS" for r in rows),
            f=sum(r["status"] == "FAIL" for r in rows),
            u=sum(r["status"] == "UNVERIFIABLE" for r in rows),
            mk=killed,
            mt=len(muts),
        ),
        "summary": {},
    }
    fragment["summary"] = {
        "rows": len(rows),
        "pass": sum(r["status"] == "PASS" for r in rows),
        "fail": sum(r["status"] == "FAIL" for r in rows),
        "unverifiable": sum(r["status"] == "UNVERIFIABLE" for r in rows),
        "mutants_killed": killed,
        "mutants": len(muts),
    }
    OUT.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("wrote", OUT, fragment["summary"], "verdict", verdict)


if __name__ == "__main__":
    main()
