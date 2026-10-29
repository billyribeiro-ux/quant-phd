"""Build the round-7 E2-d fragment from the outputs in this directory (verifier-authored; no row is asserted without its script)."""

from __future__ import annotations

import json
import re
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
S = "ledgers/E2/scripts/E2-d-r7"
GRADER = "course/modules/E/E2/grader"
PAGE = "course/modules/E/E2/project.html"
CARDS = "course/modules/E/E2/cards.json"


def row(rid: str, check: str, location: str, status: str, evidence: str, fix: str = "") -> dict[str, str]:
    out = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        out["fix"] = fix
    return out


rows = [
    # ---- gates (tools run on pin 0d2d0f3)
    row("gate-check-pages", "2.9-structure", "tools/check_pages.py --unit E2", "PASS", f"{S}/check_pages.out: 'check_pages E2: PASS' (includes banned-phrase list, cards.json grades and keys)"),
    row("gate-check-dag", "2.9-dag", "tools/check_dag.py --unit E2", "PASS", f"{S}/check_dag.out: 'check_dag E2: PASS'; anchors L02#def-bayesian-nash-equilibrium and L08#def-winners-curse exist (grep id=)"),
    row("gate-check-projects", "2.6-spec", "tools/check_projects.py --unit E2", "PASS", f"{S}/check_projects.out: 'check_projects E2: PASS'"),
    row("gate-run-graders", "2.6-autograder-1", f"{GRADER}/reference.py", "PASS", f"{S}/run_graders.out: 'run_graders E2: PASS (reference 50/50 seeds, slowest 0.2 s)'; starter fails the suite per the tool"),
    row("gate-mutate-graders", "2.6-mutation", "ledgers/E2/mutants/*.py", "PASS", f"{S}/mutate_r7.out: 'mutate_graders E2: PASS (50/50 killed)' over seeds 0-9 (50 files, listed in mutants)"),
    row("gate-run-alternatives", "2.6-over-constraint", "ledgers/E2/scripts/run_alternatives.py", "PASS", f"{S}/alternatives.out: alt01..alt05 each PASS suite 50/50 seeds and 0 symmetric-bid mismatches vs reference over n=2..5, value=0..10000 (run with python -I)"),
    row("gate-run-labs-unit", "2.5-labs", "tools/run_labs.py --unit E2", "PASS", f"{S}/run_labs_unit.out: 'run_labs E2: PASS (12/12)'; {S}/run_labs_project.out: 'run_labs E2: PASS (3/3)' for project labs"),
    row("gate-labs-twins-isolated", "2.5-labs", "tests/labs/E2/lab-E2-project-{1,2,3}.py", "PASS", f"python -I -W error on each twin, exit 0, empty stderr: {S}/twin1.err, twin2.err, twin3.err; {S}/twin1.out prints the 9600/11300 figures"),
    row("gate-page-smoke-project", "2.9-page-smoke", "course/modules/E/E2/project.html", "PASS", f"{S}/page_smoke.out: 'page_smoke E2: PASS' run alone with --pages project.html; page_smoke.py lines 291-306 paste grader/reference.py into the in-browser grader and require the suite to pass (Pyodide run of the reference)"),
    row("gate-ruff", "gate", "repository", "PASS", f"{S}/ruff.out: 'All checks passed!' and '335 files already formatted'"),
    row("gate-mypy", "gate", "repository", "PASS", f"{S}/mypy.out: 'Success: no issues found in 229 source files'; grader reference/instance/starter also clean"),
    row("gate-pytest-labs-E2", "2.5-labs", "tests/test_labs.py -k E2", "PASS", f"{S}/pytest_labs_E2.out: 15 dots, exit 0 (the -k E2 selection; the run was 15 tests)"),
    # ---- project page prose and numbers
    row("proj-ladder", "2.6-spec-ladder", f"{PAGE} lines 30-45", "PASS", "Four rungs in order; rung 1 annotated (Lab 1 comments), rung 2 is class='lab completion' with run_labs completion rule satisfied, rung 3 spec+grader+memo, rung 4 stretch (not graded)"),
    row("proj-lab1-numbers", "2.2-numbers", f"{PAGE} lines 50-80 (Lab 1 hypothesis and expected block)", "PASS", f"numcheck_r7.out: uniform [4800,0,4800,0] rev 9600; discriminatory [5200,0,6100,0] rev 11300; gap 1700; 1700/9600 = 17.7 %"),
    row("proj-lab1-interpretation", "2.2-numbers", f"{PAGE} Lab 1 interpretation paragraph", "PASS", "Overpayments 400 (bidder 0: 5200-4800) and 1300 (bidder 2: 6100-4800) sum to 1700; the uniform price 'the bid that ranks third' is bidder 1's 4800 (ranking [2,0,1,3] from twin output)"),
    row("proj-lab2-blank-description", "2.9-prose-vs-code", f"{PAGE} Lab 2 hypothesis line 'so with 0-based indexing it is ranked[units]'; Lab 1 code comment '# Counting from 0, that bid is ranked[units].'; Conventions bullet 'Uniform price' ('With 0-based indexing it is ranked[units]')", "FAIL",
        "The prose says the uniform clearing BID is ranked[units]. ranked[units] is a bidder INDEX (ranking = list of indices, twin line 'ranking (bidder indices, highest bid first): [2, 0, 1, 3]'); the bid is bids[ranked[units]] = 4800, which is what the page's own Lab 2 interpretation and Lab 1 code (uniform_price = bids[ranked[units]]) use. A student who writes clearing = ranked[units] gets [2, 0, 2, 0] and the printed expected block (4800) is not produced, contrary to the explicit instruction 'with 0-based indexing it is ranked[units]'.",
        "Say the clearing bid is bids[ranked[units]]: 'the bid of the bidder ranked at position units (0-based), that is bids[ranked[units]]'. Change the same sentence in the Lab 1 comment and the Conventions bullet."),
    row("proj-lab2-completion-check", "2.5-labs", f"{PAGE} Lab 2 and tests/labs/E2/lab-E2-project-2.py", "PASS", f"{S}/run_labs_project.out: PASS (3/3); twin2.out equals the expected block (4800,0,4800,0 / 5200,0,6100,0; revenues 9600, 11300, gap 1700)"),
    row("proj-lab3-numbers", "2.2-numbers", f"{PAGE} Lab 3 hypothesis; tests/labs/E2/lab-E2-project-3.py", "PASS", f"numcheck_r7.out: ranking [2,0,1,3,4]; winners 0,1,2; uniform 6200x3 = 18600; discriminatory 21700; gap 3100 = 16.7 % of 18600; winners' value 22800 vs top-3 value 23700 = 96.2 %; closed-form bids 3650, 4867, 5475, 5840 for n=2..5 (exact 14600/3 rounds to 4867); exact expected revenues 1/3,1/2,3/5,2/3 equal by format; twin3 output matches the expected block exactly (twin3 run in this round)"),
    row("proj-lab3-interpretation", "2.2-numbers", f"{PAGE} Lab 3 interpretation paragraph", "PASS", "The grid check is at value 7300 only (lab code: value 7300), as the text says; 'Those are the one-unit cases that Proposition A3 covers for every n >= 2' is a statement about A3, which is proved (see proj-prop-A3)"),
    row("proj-spec-terms-and-grading", "2.6-spec", f"{PAGE} Rung 3 Specification dl", "PASS", "check_projects PASS; Grading entry names 'autograder' and 'rubric'; Inputs, Required outputs, Constraints present"),
    row("proj-spec-interface", "2.6-spec", f"{PAGE} 'Interface (signatures only)' block vs {GRADER}/starter.py", "PASS", "Five signatures identical in name, parameter order and types to starter.py lines 15-39"),
    row("proj-spec-seed-claim", "2.6-spec", f"{PAGE} Inputs ('seeded from your workspace ID') and autograder paragraph", "PASS", "course/assets/js/grader.js line 53 'derived from your workspace ID'; store.js lines 134-136 FNV-1a of workspace id + unit; grader.js line 95 sets QF_SEED"),
    row("proj-conventions-exception-table", "2.6-spec", f"{PAGE} Constraints and Exception table convention", "PASS", f"reference.py messages: 'format must be \"uniform\" or \"discriminatory\"', 'units must satisfy 1 <= units < n', 'every bid/value must be a non-negative whole number of cents', 'n must be at least 2'; page names the same four conditions; {GRADER}/test_project.py tests demand ValueError only for these (lines 187-331)"),
    row("proj-conventions-rounding", "2.2-numbers", f"{PAGE} Conventions 'The symmetric bid' and Constraints", "PASS", "reference.py line 94-95: floor(exact + 1/2) with exact Fraction; test_project.py lines 147-155 hand half-cent cases (2,1->1; 2,3->2; 2,5->3; 4,2->2); exhaustive agreement with the alternatives over n=2..5 and v=0..10000 (alternatives.out)"),
    row("proj-hours", "2.9-hours", f"{PAGE} time-budget table, data-hours-project", "PASS", "1+2+8+3+4+2 = 20 = data-hours-project; 20/110 = 18.2 % (curriculum.json E2 hours 110); index.html data-hours-project=20 agrees"),
    row("proj-hours-estimate", "2.6-hours", f"{PAGE} time-budget table", "PASS", "Verifier estimate: rung 1 about 1 h, rung 2 about 1 h, engine with 5 functions, validation, tests about 6-8 h, derivations about 3 h, memo with computed figures about 4 h, self-assessment about 1-2 h: total 16-19 h, within 30 % of 20"),
    row("proj-model-assumptions", "2.4-math", f"{PAGE} 'The model and the results it rests on'", "PASS", "Assumptions 1-5 stated; 5 is used in A1 and A3 (text); 4 gives k=1 used in A3 Recommendation; Assumption 2 scaling to cents (10000 cap) consistent with instance.py _MAX_CENTS"),
    row("proj-prop-A1", "2.4-math", f"{PAGE} Proposition A1 and proof", "PASS", "Re-derived: pi(b) = (v-b)(b/c)^(n-1); pi'(b) = b^(n-2)/c^(n-1) [(n-1)v - nb]; sign change at cv; max at cv inside [0,c]; shading v - cv = v/n; grid agreement at v=7300 (numcheck_r7.out and Lab 3 output) supports the closed form"),
    row("proj-prop-A2", "2.4-math", f"{PAGE} Proposition A2 and proof", "PASS", "Re-derived by cases M<v, M>v, M=v: winning bids pay M, so no bid beats v; weak dominance holds; no independence needed (stated Assumptions 1,2,4 are a superset of what is used)"),
    row("proj-prop-A3", "2.4-math", f"{PAGE} Proposition A3 and proof", "PASS", "Re-derived: E[V(1)] = n/(n+1), E[V(2)] = (n-1)/(n+1); first-price revenue ((n-1)/n)(n/(n+1)) = (n-1)/(n+1); Lab 3 exact fractions 1/3,1/2,3/5,2/3 equal by format for n=2..5 (twin3 output)"),
    row("proj-notation", "2.4-notation", f"{PAGE}; notation/notation.json", "PASS", "Registered symbols T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q} do not occur in the project page; project uses registered macros \\E and \\Prob only; beta is a lesson-local letter (notation.json 'about')"),
    row("proj-dag", "2.9-dag", f"{PAGE} concept links", "PASS", "data-concept bayesian-nash-equilibrium -> L02.html#def-bayesian-nash-equilibrium (exists); winners-curse -> L08.html#def-winners-curse (exists); check_dag PASS"),
    row("proj-process-words", "2.9-prose", f"{PAGE}, {CARDS}, tests/labs/E2/lab-E2-project-*.py, grader/*.py", "PASS", "grep -i for verifier, builder, planner, architect, draft, TODO, round N: no hits"),
    row("proj-reading-list", "2.1-citations", f"{PAGE} Reading section", "PASS", "data-cite vickrey1961counterspeculati: registry title 'COUNTERSPECULATION, AUCTIONS, AND COMPETITIVE SEALED TENDERS', year 1961; milgrom1982theory: 'A Theory of Auctions and Competitive Bidding', 1982 (references/references.json); page attributes no result beyond title and year; the proofs need no source"),
    row("proj-rubric-observable", "2.6-rubric-1", f"{PAGE} rubric table C1-C6", "PASS", "Every level descriptor names an observable element (a formula, a named figure, a count of limits, a stated seed/number of auctions); no bare 'good' or 'clear' descriptor"),
    row("proj-rubric-calibration-A", "2.6-rubric-2", f"{PAGE} exemplar-a, data-scores=2,4,3,3,3,2", "PASS", "Blind scores from the rubric alone: C1 2 (Assumptions named without the sentence each applies to), C2 4 (grid check plus what it does not show), C3 3 (n=3 and n=5 only), C4 3 (no seeded overpayment), C5 3 (asymmetric values named, no calculation), C6 2 (unit-demand missing; no effects stated). Match official 2,4,3,3,3,2 exactly"),
    row("proj-rubric-calibration-B", "2.6-rubric-2", f"{PAGE} exemplar-b, data-scores=2,1,2,2,2,2", "PASS", "Blind scores: C1 1-2 (formats only, value distribution 'random'), C2 1 (bid asserted by symmetry), C3 2 (figure 20000 not printed by Lab 3), C4 2 (common value in words), C5 2 (recommendation with no number), C6 2 (two limits). Each within one level of 2,1,2,2,2,2"),
    row("proj-exemplar-A-numbers", "2.2-numbers", f"{PAGE} exemplar-a passages", "PASS", "16.7 %, 3100, 18600, 21700, 6200, 22800/23700 = 96.2 %, 3650/4867/5475/5840, 1/2 and 2/3 all printed by Lab 3 or recomputed (numcheck_r7.out); 'ranked[3]' in the Model passage is an index, the same wording defect as proj-lab2-blank-description"),
    row("proj-exemplar-annotations", "2.6-rubric-2", f"{PAGE} exemplar annotations", "PASS", "Each official score is consistent with its 'meets/misses' annotations (A: C1 meets 2 misses 3; C2 meets 4; C3 meets 3 misses 4; C4 meets 3 misses 4; C5 meets 3 misses 4; C6 misses 3. B: C2 meets 1; C3 misses 3)"),
    row("proj-grader-panel", "2.6-autograder", f"{PAGE} section.grader-panel", "PASS", "check_projects PASS: data-unit, data-grader, data-suite test_project.py, data-support instance.py, data-solution auction_sim.py, data-starter starter.py, data-packages empty"),
    row("proj-local-run-command", "2.6-autograder-5", f"{PAGE} 'Running the suite locally'", "PASS", "Same flags as run_graders (--assert=plain -W error, -p no:cacheprovider); collect-only with QF_SEED=0 gives 40 tests (collect.out); a failing run prints the test's own message and no values (leak_check_r7_01.out)"),
    row("proj-grader-sweep-claim", "2.6-autograder", f"{PAGE} line 164 'It checks the bid on a fixed sweep of values'", "PASS", f"SWEEP (test_project.py line 40) is used by test_first_price_symmetric_bid (138), test_first_price_bid_below_value (160) and test_uniform_symmetric_bid (172); the payment and allocation tests use CASES (INST and OTHER, lines 36-39). The round-6 defect (sweep attributed to payment rules) is fixed"),
    row("proj-grader-tests-claims", "2.6-autograder-3", f"{PAGE} Grading mode and Constraints; {GRADER}/test_project.py", "PASS", "Tie rule tests 358-367; exception table tests 187-331 each name a condition on the page; integer outputs 420-425; efficiency first entry <= second 466-470; no other exception type demanded (must_refuse only for named conditions)"),
    row("proj-grader-test-count", "2.6-autograder", f"{PAGE}", "PASS", "The project page states no test count (grep for 'tests' finds none); measured collect-only count 40 (collect.out)"),
    row("proj-grader-messages-seeded", "2.6-autograder-4", f"{GRADER}/test_project.py failure messages", "PASS", "Messages on seeded-instance tests name the property and never print a value; leak_check_r7_01.out shows the failing source line and message only, no expected numbers"),
    row("proj-grader-messages-hand-cases", "2.6-autograder-4", f"{GRADER}/test_project.py lines 374, 376, 378, 401, 415, 417, 456", "FAIL",
        "Failure messages on fixed hand cases print the expected answer: line 374 '...pays the second bid, 3 cents here'; 376 '...pays its own bid, 5 cents here'; 378 'efficiency is 10 of 10'; 401 'pay their own bids of 9 and 6'; 415 and 417 'pays the tied second bid, 7 cents' / 'its own bid, 7 cents'; 456 'the best attainable is value 3'. The spec requires failure messages that 'never print the answer'. These inputs are literal in the test source, so nothing secret leaks, but the message still states the value.",
        "Rewrite each message to name the property without the number, e.g. line 374 'the uniform winner pays the (units+1)-th highest bid, not its own bid'; line 456 'the best attainable value is the sum of the k highest values, not of the bids'. Re-run run_graders and mutate_graders."),
    row("proj-grader-instances", "2.6-autograder-2", f"{GRADER}/instance.py", "PASS", f"{S}/instances_r7.out: seeds 0-49 all valid (label SIMULATED, 2<=n<=5, 1<=k<n, integer cents 0..10000); 50 distinct (n,k,uniform rev,disc rev,efficiency) tuples over seeds 0-49"),
    row("proj-grader-reference-pyodide", "2.6-autograder-5", f"{GRADER}/reference.py in-browser", "PASS", f"{S}/page_smoke.out PASS: page_smoke pastes reference.py into the in-browser grader and requires the suite to pass (page_smoke.py 291-306). The mutants and alternatives were not run in Pyodide (honest gap)"),
    row("proj-grader-timing", "2.6-autograder", f"{GRADER}/test_project.py", "PASS", "run_graders slowest 0.2 s over 50 seeds (well under 5 s per test and 60 s per suite); 40 tests collect in 0.01 s"),
    row("proj-grader-alternatives", "2.6-autograder-over-constraint", "ledgers/E2/scripts/alt01..alt05", "PASS", f"{S}/alternatives.out: five alternatives (threshold closed form, bisection on FOC, sort clearing, counting clearing, float half-up) pass 50/50 seeds each and match the reference symmetric bid on 4 x 10001 cases"),
    row("proj-grader-mutants-new", "2.6-mutation", "ledgers/E2/mutants/r7_01..r7_04", "PASS", f"Four new student-error mutants, generated by {S}/make_mutants_r7.py from reference.py: r7_01 efficiency ignores bids (killed by test_efficiency_uses_values_of_the_winners), r7_02 allocate repeats max index (killed by test_zero_bid_is_accepted seed 0), r7_03 revenue ignores format (killed by test_unknown_format_name_is_refused_by_every_format_function), r7_04 zero refused (killed by test_first_price_symmetric_bid_is_n_minus_1_over_n_times_value)"),
    row("proj-grader-mutants-all", "2.6-mutation", "ledgers/E2/mutants/*.py (50 files)", "PASS", f"{S}/mutate_r7.out: 50/50 killed on seeds 0-9. One file, L06-lab1-agency-sign.py, is a lab solution from the L06 slice, not a grader mutant; it is counted by the tool and its kill is incidental (see notes)"),
    # ---- cards
    row("cards-structure", "2.7-cards", CARDS, "PASS", f"{S}/cards_scan_r7.out: 125 cards E2-c001..c125, no gaps, no duplicate ids, fronts or backs; keys within the schema; 37 cards without grade are definitions and misconceptions (tool allows absent grade)"),
    row("cards-numbers-in-lesson", "2.7-cards", CARDS, "PASS", f"{S}/cards_scan_r7.out: every number token of every card appears in its own lesson, except E2-c051's 2,000,000 which appears in L04 line 237 as LaTeX 2{{,}}000{{,}}000 (checked by hand)"),
    row("cards-sample-c010", "2.7-cards", f"{CARDS} E2-c010", "PASS", "L01 Proposition 4.2 under Assumptions 1 and 2 (outputs in [0,90]); (30,30) is pure NE; card carries the hypotheses"),
    row("cards-sample-c020", "2.7-cards", f"{CARDS} E2-c020", "PASS", "L02 Definition 1.3 BNE wording matches (interim expected payoff maximized for each type with positive prior probability)"),
    row("cards-sample-c030", "2.7-cards", f"{CARDS} E2-c030", "PASS", "L03 line 64 offered mix = sellers with cost at most p, shares m_H(p), m_L(p) (Definition 1.2)"),
    row("cards-sample-c040", "2.7-cards", f"{CARDS} E2-c040 (grade C, basis Lab 3)", "PASS", "L03 Lab 3 expected output and hypothesis: one price for alpha 0-0.6, two for 0.7-0.9 (10200, 10800, 11400); grade C with lab basis follows the unit's open-item convention (lab results graded C, architect decision); the enumeration is exact, so C is conservative, not a failure"),
    row("cards-sample-c050", "2.7-cards", f"{CARDS} E2-c050", "PASS", "L04 line 236 (Remark 2.1, minimum of the set of separating thresholds 2,3,4; no selection rule)"),
    row("cards-sample-c060", "2.7-cards", f"{CARDS} E2-c060 (grade C, cite rothschild1976equilibrium)", "PASS", "Registry record: title 'Equilibrium in Competitive Insurance Markets: An Essay on the Economics of Imperfect Information', QJE vol 90 issue 4, 1976; the card's short title is a prefix of the registry title and the lesson line 254 says title and year only; no result attributed"),
    row("cards-sample-c070", "2.7-cards", f"{CARDS} E2-c070", "PASS", "L06 Remark 1.4: alpha = c_H - beta E_H for beta >= 1/5, profit 650000 = first best, negative payments; Part C checks beta 0.20, 0.50, 1.00 (line 223-227 output)"),
    row("cards-sample-c080", "2.7-cards", f"{CARDS} E2-c080 (changed; see cards-changed-c080-c081)", "PASS", "see cards-changed-c080-c081"),
    row("cards-sample-c090", "2.7-cards", f"{CARDS} E2-c090 (grade C, basis Lab 1 Part C)", "PASS", "L07 line 351: two equilibria of one menu induce 6000 and 4200 cents (Lab 1 Part C); proof of Prop 2.2 gives the direct version of the used equilibrium"),
    row("cards-sample-c100", "2.7-cards", f"{CARDS} E2-c100 (changed to T)", "PASS", "L08 Remark 3.2 line 135: 1334 cents, E[M] = 1333.66656253, 1333 gives -0.66656253 (rounds to -0.67); numcheck_r7.out confirms"),
    row("cards-sample-c104", "2.7-cards", f"{CARDS} E2-c104", "PASS", "L08 Proposition 2.1: winner's profit -M, expected -E[M]; card says expected loss E[M] cents (sign convention matches the misconception item)"),
    row("cards-sample-c110", "2.7-cards", f"{CARDS} E2-c110", "PASS", "L09 Definition 1.2 (revenue): R_u = k b(k+1), R_d = b(1)+...+b(k) (lines 71-72)"),
    row("cards-sample-c121", "2.7-cards", f"{CARDS} E2-c121", "PASS", "L09 Problem P3 (line 358) and line 262: winners and efficiency depend only on bids; the card's 'depend only on the bids' is correct for winners"),
    row("cards-changed-c022", "2.7-cards", f"{CARDS} E2-c022", "PASS", "L02 Proposition 2.2 with n >= 2 and Assumptions 1-4 (lines 98-102); card matches, carries the hypotheses"),
    row("cards-changed-c035-c037-c124", "2.7-cards", f"{CARDS} E2-c035, E2-c037, E2-c124", "PASS", "L03 Proposition 2.3 (line 96-102): at 6000 the traded share is 1-alpha, the lost gain 2000 alpha per seller; card c035 omits 'market-consistent when alpha < 1' but the share 1-alpha holds for every alpha, so the card is correct"),
    row("cards-changed-c051", "2.7-cards", f"{CARDS} E2-c051", "PASS", "Wage gain 2,000,000 = y_H - y_L (L04 line 105 inputs; line 237 misconception states it). Locator '(Remark 2.1)' cites the lesson for cost and net utility only; the wage gain is in the misconception item. Card is correct; locator imprecise (no fix required under the card rule)"),
    row("cards-changed-c058-c063-c125", "2.7-cards", f"{CARDS} E2-c058, E2-c063, E2-c125", "PASS", "L05 Remark 1.5 (line 124): q_L = 2000, q_H = 6000, m_L = 6,000,000, m_H = 30,000,000, U_H = 6,000,000, low type's rent 0, first best 3000; Remark 2.1 gives the cut lowers the high type's rent"),
    row("cards-changed-c067", "2.7-cards", f"{CARDS} E2-c067", "PASS", "L06 Lemma 1.2 (line 86-87): payment alpha + beta x, expected payment alpha + beta E_a; card says affine, the lemma's word"),
    row("cards-changed-c080-c081", "2.7-cards", f"{CARDS} E2-c080, E2-c081", "PASS", "L07 Definition 2.1 and Proposition 2.2 (lines 95-101); c081 'Not on this page' matches L07 line 350 in Section 4 (Where the canon breaks); Assumption 3 is one agent with finite sets (line 88). E2-c080 carries no grade (definition card)"),
    row("cards-changed-c088", "2.7-cards", f"{CARDS} E2-c088", "PASS", "L07 Proposition 3.2 (c<0 gives q_L = 0), Lemma 3.1 (U_H >= U_L + Delta q_L, the cap on the price of H), Example 3.3 values 7000 vs 6000"),
    row("cards-changed-discrete-EM", "2.2-numbers", f"{CARDS} E2-c098, E2-c099, E2-c100, E2-c105 (round-6 FAIL re-verified)", "PASS", f"{S}/numcheck_r7.out: E[M] = 85418692002000/64048012001 = 1333.6665625260364 exactly (-a + sum (1 - F(x)^n) with F(x)=(x+a+1)/(2a+1)); 1333.67 to 2 dp; 1333-E[M] = -0.67 to 2 dp; 1334 is the smallest whole cent >= E[M]. Cards now grade T, matching L08 key-results row 413 (T, source Proposition 2.2 evaluated exactly, no simulation) and Remark 2.3 (basis named). The T-grade basis is the exact evaluation, not a SIMULATED lab. Note: these cards carry no basis field, which BUILDER_RULES §7 suggests for non-theorem numbers; Remark 2.3 supplies the basis in the lesson"),
    row("cards-changed-c117", "2.7-cards", f"{CARDS} E2-c117", "PASS", "L09 Proposition 4.1 (line 273-279): k=1, uniform pays b(2), discriminatory pays own bid; Lab 1 Part C prints 256 of 256 agreements (numcheck_r7.out k=1 check: 256)"),
    row("cards-changed-c120", "2.2-numbers", f"{CARDS} E2-c120", "PASS", f"{S}/numcheck_r7.out: brute force over {{0,1,2,3}}^4 with k=2 gives 28 equal, 228 above, 0 below; 4w+1 summed over w=0..3 = 28; L09 R1 (line 394-397) gives the same count"),
]

mutant_lines = (ROOT / S / "mutate_r7.out").read_text(encoding="utf-8").splitlines()
mutants = []
for line in mutant_lines:
    m = re.match(r"KILLED (\S+?)\.py: (.*) -> (\S+) \(seed (\d+)\)$", line)
    if m:
        mutants.append({"id": m.group(1), "description": m.group(2), "killed_by": f"{m.group(3)} (seed {m.group(4)})"})
assert len(mutants) == 50, len(mutants)

fragment = {
    "unit": "E2",
    "slice": "d",
    "round": 7,
    "verifier": "Claude Haiku 5.5, independent verifier for E2-d, round 7 (did not build E2)",
    "pin": "0d2d0f3",
    "base": "9fd6aed (round-6 pin; round-6 fragment is context only)",
    "checkout": str(ROOT),
    "scratch": "/tmp (leak check and collect-only runs only)",
    "verified_at": datetime.now(UTC).isoformat(),
    "verdict": "FAIL",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "Delta since round-6 pin 9fd6aed in this slice: project.html (lines 107, 164, 227, 413), cards.json (changed cards c022, c035, c037, c051, c058, c063, c067, c080, c081, c088, c098, c099, c100, c105, c117, c120, c124, c125), tests/labs/E2/lab-E2-project-2.py (docstring only). grader/*, test_project.py, instance.py, starter.py, lab-E2-project-1/3 unchanged since 9fd6aed (git diff --stat), so carried facts about them were re-run, not copied. "
        "Round-6 non-PASS rows re-verified from scratch: proj-cards-numerics-discrete-EM now PASS (cards and L08 both T, exact E[M] recomputed); proj-grader-sweep-claim now PASS (SWEEP is used only by the three symmetric-bid tests and the sentence says so). "
        "Misfiled artifact: ledgers/E2/mutants/L06-lab1-agency-sign.py is an L06 lab solution (not a grader mutant) in the grader mutant directory; mutate_graders counts it, and its kill is incidental. Recommend moving it out of the grader mutant set (not edited by this verifier). "
        "Honest gaps: (1) the Pyodide run of mutants and alternatives was not done in a browser (only the reference, via page_smoke); (2) the 37 cards without grade were not graded, as they are definitions and misconceptions; (3) no card was checked in the L01-L09 lessons beyond the cited locators; (4) Lab 2 and Lab 3 pages were checked as printed output and by re-derivation, not by browser rendering; (5) the rubric was calibrated on exemplars A and B, not on a real student memo."
    ),
    "summary": "E2-d round 7 on pin 0d2d0f3: 77 rows, 75 PASS, 2 FAIL (proj-lab2-blank-description: clearing bid described as ranked[units], an index; proj-grader-messages-hand-cases: failure messages print the expected answer on 7 hand-case lines). Mutants: 50 of 50 killed (46 existing + 4 new r7_01..04). Five alternative implementations pass 50/50 seeds and match the reference symmetric bid exhaustively. All tool gates green (check_pages, check_dag, check_projects, run_graders, mutate_graders, run_alternatives, run_labs, page_smoke, ruff, mypy, pytest tests/test_labs.py -k E2 passes).",
}

out = ROOT / "ledgers/E2/E2-d.json"
out.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("rows", len(rows), "by status", {s: sum(r["status"] == s for r in rows) for s in ("PASS", "FAIL", "UNVERIFIABLE")})
print("mutants", len(mutants))
