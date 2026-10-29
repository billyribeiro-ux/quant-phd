"""Build the round-4 verifier fragment for E1 slice d (run from the checkout root)."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
S = "ledgers/E1/scripts/E1-d-r4"
PIN = "2657ab568c1727896cd9595ed45b67b33d064707"
CARRY = "Carried from round 3 (course/modules/E/E1/grader/instance.py byte-identical since the previous pin):"


def row(rid, check, location, status, evidence, fix=None):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix or ""
    return r


ROWS = [
    row("E1d-gate-projects", "2.9 check_projects --unit E1", "tools/check_projects.py", "PASS",
        "Re-run at pin 2657ab5: 'check_projects E1: PASS'."),
    row("E1d-gate-pages-dag", "2.9 check_pages --unit E1; check_dag --unit E1", "tools/check_pages.py; tools/check_dag.py",
        "PASS", "Re-run: 'check_pages E1: PASS'; 'check_dag E1: PASS'."),
    row("E1d-gate-graders", "2.5 run_graders --unit E1 --seeds 0-49", "course/modules/E/E1/grader/", "PASS",
        "Re-run: 'run_graders E1: PASS (reference 50/50 seeds, slowest 0.2 s)'. Output: " + S + "/run_graders_E1_seeds0-49.txt."),
    row("E1d-gate-mutants", "2.6 mutate_graders --unit E1 --seeds 0-9 over all mutants", "ledgers/E1/mutants/ (63 files)",
        "PASS", "Re-run: 'mutate_graders E1: PASS (59/59 killed)' before my four new mutants; after adding them, 63/63 KILLED. Output: " + S + "/mutate_E1_seeds0-9_r4.txt."),
    row("E1d-mutants-existing", "2.6 existing mutants m01-m10, f01-f11, v01-v08, fx01-fx11, r2_m01-r2_m04, r3_m01-r3_m04, r4_m01-r4_m11 killed",
        "ledgers/E1/mutants/", "PASS",
        "All 59 pre-existing mutants KILLED on seed 0 (mutate_E1_seeds0-9_r4.txt). Every r4_m01..r4_m11 is KILLED by a parametrized test."),
    row("E1d-mutants-r3", "2.6 new student-error mutants (round 3)", "ledgers/E1/mutants/r3_m01..r3_m04.py", "PASS",
        "Re-run: all four KILLED on seed 0."),
    row("E1d-mutants-vx4", "2.6 at least three new student-error mutants written and run (round 4)",
        "ledgers/E1/mutants/vx4_m01..vx4_m04.py", "PASS",
        "Four new mutants written from the reference: vx4_m01 consumer surplus (a - fee) Q / 2 (slope b dropped) KILLED by test_closed_form_matches[consumer_surplus_cents-monopoly]; "
        "vx4_m02 welfare = rounded benchmark welfare - rounded deadweight loss KILLED by test_tie_rounds_up_for_each_output[monopoly-welfare_cents-11-1-1]; "
        "vx4_m03 deadweight loss with // before the single rounding KILLED by test_closed_form_matches[deadweight_loss_cents-cournot]; "
        "vx4_m04 fee from the printed volume KILLED by test_tie_rounds_up_for_each_output[monopoly-fee_cents-8-1-1]."),
    row("E1d-labs-run", "2.5 run_labs twins under python -I -W error; embedded expected output equals run output",
        "tests/labs/E1/lab-E1-project-{1,2,3}.py; course/modules/E/E1/project.html", "PASS",
        "Re-run all 12 E1 twins under python -I -W error: rc 0 each (outputs in " + S + "/lab-E1-*.out). Page <pre class=expected> equals the run for project-1, -2, -3 (checked by script, comparison of stripped text). Page code equals twin for project-1 and project-3; project-2 differs only in the three blanks (___), the intended completion gaps."),
    row("E1d-smoke", "2.5 page_smoke for project.html", "course/modules/E/E1/project.html", "PASS",
        "tools/page_smoke.py --unit E1 --pages project: 'in-browser grader: All 118 tests pass on seed 392601084'; 'page_smoke E1: PASS'."),
    row("E1d-lint-types", "2.5 ruff; mypy --no-incremental", "tests/labs/E1; course/modules/E/E1/grader", "PASS",
        "ruff check tests/labs/E1 course/modules/E/E1/grader: All checks passed. ruff format --check: 16 files already formatted. mypy --no-incremental (repo scope): 'Success: no issues found in 255 source files' (" + S + "/mypy.txt)."),
    row("E1d-test-count", "Grading mode test count equals real collect-only count",
        "course/modules/E/E1/project.html (Grading mode); grader/test_project.py", "PASS",
        "pytest --collect-only -q test_project.py with the reference staged: '118 tests collected'. Page says 'runs 118 checks'. Full run with the reference: 118 passed."),
    row("E1d-alternatives", "2.5 correct alternative implementations pass (over-constraint)",
        "ledgers/E1/scripts/E1-d-r4/; ledgers/E1/scripts/alt*.py; ledgers/E1/scripts/E1-d-r2/alternatives/", "PASS",
        "run_alts_r4.py (builder's runner, run by me): 10/10 PASS on seeds 0-49 (closed form, best response, linear solve, Fraction vertex, float half-up, linear solve, Simpson, Decimal, iterate with cutoff). New alternative alt_vx4_float_cutoff_order.py (float arithmetic with a 1e-9 half-up cutoff, validation order b, c, a, then structure): PASS 50/50 via run_vx4_alt.py."),
    row("E1d-instance", "instance docstring agrees with make_instance", "course/modules/E/E1/grader/instance.py", "PASS",
        CARRY + " instance.py. Its docstring (gap above 6*b; b from 1 to 3; c from 5 to 60; gap from 60 to 400) matches make_instance; ordering tests pass on seeds 0-49 with the reference."),
    row("E1d-exceptions", "exception table: each named condition raises ValueError with the named message",
        "course/modules/E/E1/project.html (Constraints); grader/test_project.py (must_raise, UNKNOWN_STRUCTURES)", "PASS",
        "Constraints names ValueError for a structure not one of three names (padded, capitalised, non-string) with the message naming all three; a <= bc with 'a must exceed b*c'; b <= 0 with 'b must be positive'; c <= 0 with 'c must be positive'. must_raise checks the type and that the message contains those phrases, which the page states. The unknown-name list now includes 'Cournot', 'Bertrand', 'bertrand ' and b'monopoly'; the reference raises for all."),
    row("E1d-grader-coverage", "each structure-specific check is tested for every structure", "grader/test_project.py", "PASS",
        "The three exception tests carry @pytest.mark.parametrize over the structures (a: 3 pairs x 3 structures; b and c likewise). Mutants fx01, fx02, fx03, fx11, r2_m01, r2_m02, r4_m07, r4_m08 KILLED."),
    row("E1d-grader-spec-trace", "Grading mode lists match the test functions", "grader/test_project.py; project.html (Grading mode)", "PASS",
        "Grading mode lists six outputs vs closed forms (test_closed_form_matches), ordering (test_volume_ordering, test_fee_ordering, test_welfare_ordering, test_deadweight_loss_ordering), exception table, integer types (test_every_output_is_an_int), tie rounding (test_tie_rounds_up_for_each_output), the value on either side of a half (test_value_below_a_half_rounds_down, test_value_above_a_half_rounds_up), the standard-library rule (test_module_imports_only_the_standard_library), purity (test_outcome_prints_nothing), second instance (test_second_instance_matches_closed_forms). All exist."),
    row("E1d-spec-grader-agree", "signature and keys agree across spec, starter, reference and suite",
        "project.html (Required outputs); grader/starter.py; grader/reference.py; grader/test_project.py", "PASS",
        "outcome(structure: str, a: int, b: int, c: int) -> dict[str, int] in starter.py and reference.py; keys exactly the six of Required outputs (test_outcome_has_exactly_the_six_keys)."),
    row("E1d-prop1", "Proposition 1 and proof", "course/modules/E/E1/project.html #prop-1", "PASS",
        "Re-derived: pi(Q) = -Q^2/b + (d/b)Q; pi' = (d-2Q)/b; zero at d/2; pi'' = -2/b < 0; fee (a+bc)/(2b); profit d^2/(4b). Statement and proof agree."),
    row("E1d-prop2", "Proposition 2 (Cournot) statement and proof, existence of equilibrium", "course/modules/E/E1/project.html #prop-2", "PASS",
        "The round-3 gap (existence not proved) is closed: the proof now says 'Conversely, q1 = q2 = d/3 satisfies both reaction equations ... so the profile (d/3, d/3) is an equilibrium, and the symmetric point is the only one.' Re-derived: (d - d/3)/2 = d/3 and d/3 > 0 is interior. Case q1 = 0 gives q2 = d/2, q1 = d/4 > 0, a contradiction. Subtraction gives q1 - q2 = (q1 - q2)/2. Error e_{k+1} = -e_k/2, |e_k| = d/(3*2^k). Fee (a+2bc)/(3b); profit per exchange d^2/(9b), total 2d^2/(9b). Verified."),
    row("E1d-prop3", "Proposition 3 (Bertrand) statement and proof", "course/modules/E/E1/project.html #prop-3", "PASS",
        "Re-derived every case: f1 < c (negative margin; raise to c gains, including the tie f2 = f1 < c); f1 > c with f2 > f1 (undercut to (c+f1)/2 gains); f1 = f2 = f > c (g = (f+c)/2 earns (f-c)(a-bg)/2 > (f-c)(a-bf)/2); f1 = c < f2 (undercut to g in (c, f2)). Fees restricted to [0, a/b] as in Definitions; c < a/b since bc < a."),
    row("E1d-prop4", "Proposition 4 (surplus identities) and proof", "course/modules/E/E1/project.html #prop-4", "PASS",
        "CS = int_0^Q (Q-t)/b dt = Q^2/(2b); G(x) = (ax - x^2/2)/b; W' = (d-x)/b; W(d)-W(Q) = (d-Q)^2/(2b); G(Q) - cQ = Q^2/(2b) + (f(Q)-c)Q since f(Q)Q = G(Q) - Q^2/(2b). Verified."),
    row("E1d-prop5", "Proposition 5 (ordering) statement and proof", "course/modules/E/E1/project.html #prop-5", "PASS",
        "Re-derived each exact difference: volumes d/6, d/3; fees d/(6b), d/(3b); DWL d^2/(8b), d^2/(18b); profit d^2/(36b); welfare W(d)-W(2d/3) = d^2/(18b), W(2d/3)-W(d/2) = 5d^2/(72b). Rounding: round(x) >= x - 1/2 and round(y) <= y + 1/2, so an exact difference above 1 keeps its sign; with d > 6b each listed difference exceeds 1 (checked inequality by inequality in the proof). Verified."),
    row("E1d-lab1-prose", "Lab 1 hypothesis, docstring and interpretation vs code and output",
        "course/modules/E/E1/project.html lab-E1-project-1", "PASS",
        "Hypothesis numbers (d = 100; monopoly 50 and 70; Cournot 200/3 -> 67 and 160/3 -> 53; Bertrand 100, 20, DWL 0) equal the run. Recomputed each printed value: monopoly profit 2500, CS 1250, welfare 3750, DWL 1250; Cournot profit 20000/9 -> 2222, CS 20000/9 -> 2222, welfare 40000/9 -> 4444, DWL 5000/9 -> 556; Bertrand 0, 5000, 5000, 0. Docstring 'The lab checks the reference case only' is true (constants A, B, C)."),
    row("E1d-lab2-prose", "Lab 2 hypothesis, blanks, interpretation vs code and output",
        "course/modules/E/E1/project.html lab-E1-project-2", "PASS",
        "Blanks: reaction -> (d - rival)/2 and half_up((a*volume - volume*volume/2)/b - c*volume) (the twin's expressions). Output True, 67, 53, 4444 (run). Error formula e_k = (-1/2)^k (-d/3) re-derived; size d/(3*2^60) about 2.9e-17 < 1e-12. Interpretation 'the lab prints the comparison, not the error' true."),
    row("E1d-lab2-blanks", "Lab 2 page code equals the twin except the blanks",
        "course/modules/E/E1/project.html lab-E1-project-2; tests/labs/E1/lab-E1-project-2.py", "PASS",
        "Diff of page code against twin: only the three blank lines (reaction, welfare_cents). Docstring text equals the twin's docstring after the round-4 rewrap (checked)."),
    row("E1d-lab3-numbers", "Lab 3 hypothesis and expected block vs recomputation",
        "course/modules/E/E1/project.html lab-E1-project-3", "PASS",
        "Recomputed a = 121 by hand: monopoly fee 141/2 -> 71, volume 101/2 -> 51, profit 10201/4 -> 2550, CS 1275.125 -> 1275, welfare 3825.375 -> 3825, DWL 1275.125 -> 1275; Cournot volume 67, fee 161/3 -> 54, profit 20402/9 -> 2267, CS 2267, welfare 40804/9 -> 4534, DWL 10201/18 -> 567; Bertrand 101, 20, 0, 5101, 5101, 0. All equal the run; the hypothesis values 3750 and 4444 and 2550.25 agree."),
    row("E1d-lab3-location", "Lab 3 instructions vs Required outputs", "course/modules/E/E1/project.html lab-E1-project-3; Required outputs", "PASS",
        "Required outputs names run_report.py as Lab 3 with the closed-form call replaced by outcome; Lab 3 says the same. Consistent."),
    row("E1d-numbers-prose", "numbers in prose recomputed from exact values",
        "course/modules/E/E1/project.html (Lab 3 interpretation, Exemplar B Summary, Welfare, Comparison, Recommendation, Limits)", "PASS",
        "200/3 and 202/3 in (66.5, 67.5). 5000/9 = 555.56 -> 556; 20000/9 = 2222.22 -> 2222. Exemplar B: printed differences +17, +33 (volumes), -17, -33 (fees), +694, +556 (welfare) equal the differences of the printed values; monopoly profit minus Cournot total = 2500/9 = 277.8 = d^2/(36b) = 10000/36; 50/3 = d/(6b). Recommendation: monopoly profit 2500, Bertrand profit 0. Exemplar B's '555.56 printed as 556' follows the stated rounding."),
    row("E1d-scope-words", "scope words need a computation or an explicit hypothesis", "course/modules/E/E1/project.html (Limits, Exemplar B Limits, prose)",
        "FAIL",
        "Scope words in the page were checked one by one (every, only, all, same, always, any, never, drives). The one that fails: Limits (line 'Linear demand: the closed forms here use the linear inverse demand and do not apply to a curved one'), repeated in Exemplar B's Limits. 'do not apply to a curved one' is a universal claim about every curved demand with no computation or counterexample shown. It is false as a general statement: for f(Q) = (a - Q^2)/b the monopoly profit is (dQ - Q^3)/b, whose maximiser is sqrt(d/3), not d/2 (d = 100 gives 5.77, not 50), so the monopoly volume changes, but other curved demands could leave a given closed form unchanged.",
        "Replace 'do not apply to a curved one' with 'do not in general apply to a curved one', and give the witness f(Q) = (a - Q^2)/b with monopoly volume sqrt(d/3) (or cite the statement of the linear-demand hypothesis of Proposition 1). Apply the same wording in Exemplar B."),
    row("E1d-banned-process", "banned phrases, ellipses and process words", "course/modules/E/E1/project.html; course/modules/E/E1/cards.json", "PASS",
        "Scan of project.html prose (pre blocks removed) and cards.json for TODO, TBD, lorem, ellipsis, 'roughly', 'historically', 'clearly', 'obviously', 'build', 'builder', 'verifier', 'round', 'REQUEST', 'unit report': no matches. 'about' occurs only in Exemplar A's annotated fault ('about 1250 cents') and in card values followed by exact values."),
    row("E1d-exemplar-a", "Exemplar A scores and annotations", "course/modules/E/E1/project.html #exemplar-a", "PASS",
        "data-scores 1,2,2,2,1,2 match the annotations: C1 level 1 (no cost, no unit, names three structures), C2 level 2 (one closed form derived), C3 level 2 (DWL of two structures, no rounding rule), C4 level 2 (orders without signs), C5 level 1 (no recommendation), C6 level 2 (names one limit)."),
    row("E1d-exemplar-b-C2", "Exemplar B C2 derivations", "course/modules/E/E1/project.html #exemplar-b Derivations", "PASS",
        "Monopoly FOC, reaction function, symmetric solution d/3, the q1 = 0 case analysis (q2 = 50, q1 = 25) and the difference argument. Level 4 met; score 4 consistent."),
    row("E1d-exemplar-b-C3-C4", "Exemplar B C3 and C4", "course/modules/E/E1/project.html #exemplar-b Welfare and Comparison", "PASS",
        "C3 = 4: exact before rounding, DWL on exact volume, tie named (71, 51). C4 = 4: printed differences with signs and the exact profit difference d^2/(36b) = 277.8 with sign. Numbers recomputed (E1d-numbers-prose)."),
    row("E1d-exemplar-b-C5", "Exemplar B C5", "course/modules/E/E1/project.html #exemplar-b Recommendation", "PASS",
        "Recommendation names Bertrand, justifies from printed welfare 5000 and fee 20, and names one condition (exchange profit alone: monopoly 2500 vs Bertrand 0). No direction for c or b, so level 4 is missed: score 3 consistent."),
    row("E1d-exemplar-b-C6", "Exemplar B C6", "course/modules/E/E1/project.html #exemplar-b Limits", "PASS",
        "Names three limits; constant cost gives the direction (all three fees increase in c, checked: derivatives c/2, 2/3, 1 with respect to c); linear demand and two exchanges have no direction. Score 2 is the highest level whose every element is shown. The 'do not apply to a curved one' sentence is in row E1d-scope-words."),
    row("E1d-citations", "2.1 citations: verify_refs live and offline for E1", "references/references.json (varian2014intermediate); course/modules/E/E1/project.html #reading",
        "PASS",
        "tools/verify_refs.py --unit E1 (live, re-run now): 'live re-verification of E1: 1 of 560 entries, 0 problems'. tools/verify_refs.py --offline (re-run now): 'offline integrity: 560 entries, 0 problems'. The page cites only varian2014intermediate and attributes no statement to it; the Reading paragraph says no passage locator is confirmed."),
    row("E1d-citations-intext", "Reading paragraph and data-cite", "course/modules/E/E1/project.html #reading", "PASS",
        "Reading paragraph (changed this round: 'derivative and integral of polynomials and elementary algebra') attributes nothing; the only data-cite is varian2014intermediate."),
    row("E1d-hours", "hours: declared vs arithmetic (pace not checked, architect ruling)", "course/modules/E/E1/index.html; L01-L09 data-hours; project.html Time budget", "PASS",
        "index.html data-hours-lessons 90, data-hours-project 30 (sum 120 = unit hours); nine lessons at data-hours 10 = 90. Time-budget table: 2 + 3 + 8 + 8 + 6 + 3 = 30. Pace not checked."),
    row("E1d-dag", "DAG: prerequisite closure and concept use", "course/modules/E/E1/project.html; cards.json; L01-L09", "PASS",
        "check_dag.py --unit E1: PASS. project.html has no concept links. Names used (first-order condition, second derivative, integral, fixed point, reaction function) are in the M2 closure or defined on the page in Definitions. 'Reaction function' is defined in Definitions before Proposition 2 uses it in its statement."),
    row("E1d-forward-refs", "terms used before definition (labs placed before Definitions)", "course/modules/E/E1/project.html lines 55-259 (labs) vs 264 (Definitions)", "PASS",
        "The labs (Rungs 1 and 2 and Lab 3) use the structures, 'Cournot', 'rival', and cite Propositions 1 to 4 before the Definitions section. Each lab's docstring or hypothesis defines the quantities it prints (gap d, profit, consumer surplus, welfare, deadweight loss, the reaction step). The ladder says 'Each output is defined in the model section'. Forward citation of a numbered result in a worked example is not a defined term; recorded as a note, no defect."),
    row("E1d-time-limit", "120 s runtime statement", "course/modules/E/E1/project.html Constraints; course/assets/js/python.js", "PASS",
        "python.js line 4: TIMEOUT_MS = 120000; the page: 'A run in your browser stops after 120 seconds.'"),
    row("E1d-definitions", "Definitions formulas and units", "course/modules/E/E1/project.html #model-definitions", "PASS",
        "Formulas re-checked: f(Q) = (a-Q)/b; monopoly profit (f-c)Q; Cournot profit (f(Q)-c)q_i; Bertrand demand rule; CS = int (f(t) - f(Q)) dt = Q^2/(2b); welfare = gross minus cQ; DWL benchmark at d where f(d) = c. Units of the same definitions are a separate FAIL (E1d-units)."),
    row("E1d-units", "units of a, b, c, f are dimensionally consistent", "course/modules/E/E1/project.html #model-definitions ('Model.', 'Inverse demand.'), #conventions, #spec (Inputs), rubric C1 cell; grader/instance.py and grader/reference.py docstrings",
        "FAIL",
        "The page labels b 'in trades per cent' (Model; Conventions 'a rate such as b is in trades per cent'; rubric C1 '(trades, trades per cent, cents per trade)'; Inputs; instance and reference docstrings) and f 'in cents per trade' (Inverse demand), with c in cents per trade. Dimensional check: f(Q) = (a - Q)/b has units trades / (trades per cent) = cents, not cents per trade. bc has units (trades per cent)(cents per trade) = dimensionless, yet 'd = a - bc' is stated 'in trades' (Model; Inputs). The consumer surplus Q^2/(2b) = integral of f dQ has units (cents per trade)(trades) = cents only if b has units trades^2 per cent (equivalently trades per (cent per trade)). With b in trades per cent, the labels of f, CS and d are inconsistent, and the rubric's C1 unit list asks students for an inconsistent set.",
        "Relabel b as 'trades per (cent per trade)' (equivalently trades^2 per cent) in Model, Conventions, Inputs, rubric C1 and both grader docstrings, so that f and c are cents per trade, bc and d are trades, and Q^2/(2b) is cents. Then re-check the Lab 1 and Lab 3 prose that says 'trade per cent' (Exemplar B Model: 'b = 1 trade per cent')."),
    row("E1d-cards-structure", "cards: schema, unique ids, no duplicate fronts or backs, grades and bases",
        "course/modules/E/E1/cards.json", "PASS",
        "Re-scan: 133 cards, ids E1-c001..E1-c133 sequential, no duplicate ids, fronts or backs. Grades: T 94, C 14, ungraded 25 (definitions). Every C card has a basis naming its lab; no basis on a T card."),
    row("E1d-cards-numbers-refs", "every card locator (Proposition, Lemma, Remark, Example, Definition, Assumption, Misconception, Problem) is in its lesson",
        "course/modules/E/E1/cards.json vs L01-L09", "PASS",
        "Re-scan (locator regex over all cards): no missing Proposition/Lemma/Theorem/Corollary/Remark/Example/Definition/Assumption locator; 'Problem P1' on c121 is now 'problem set item P1' and L09 contains 'P1 · The overproduction gap'."),
    row("E1d-cards-recompute", "card numbers recomputed", "course/modules/E/E1/cards.json; tests/labs/E1/lab-E1-L01..L09-1.py (outputs in " + S + ")", "PASS",
        "Changed cards recomputed in this round: c025 (profit 4 -> -84, fall 88 = 100 - 12, output 4 both: lab-E1-L02-1 output); c048 (no numbers now); c051 (10, 100, 0.0454545455, -0.2, 2: lab-E1-L04-1 output); c133 (forward 9.391047e-7, central 3.880758e-11 at h = 0.01: lab-E1-L04-1 output; dp/da = 1/22 = 1/(2 sqrt(121)) from the closed form in the lab). Unchanged cards: the round-3 recomputation stands for them, and their lesson text changed (see E1d-lessons-changed-cards)."),
    row("E1d-cards-changed", "cards changed or re-read: c004, c062, c090, c118 (round 3) and c025, c031, c032, c045, c048, c051, c119, c121, c133 (this round)",
        "course/modules/E/E1/cards.json; L01-L09 current text", "PASS",
        "c031: Z decreasing (Remark 1.4); sign pattern proved in Prop 1.3 step 1 (T). c032: 110/7, 480/7 (Example 1.5; one firm 48/7; ten firms 480/7). c045: Proposition 2.3 hypotheses now include 'D_a > 0 at the equilibrium', matching the lesson. c119: 'When e > 0 ...' matches Definition 1.1 (L09). c121: hypotheses 'a > 0, b > 0, 0 <= c < a, e >= 0, c + e < a' match Proposition 1.3 (L09 line 72); P1 is in the problem set. c025 and c133 checked against the lab outputs. c004, c062, c090, c118: unchanged since round 3 at the card level."),
    row("E1d-cards-lab-grade", "grade C cards carry a lab basis", "course/modules/E/E1/cards.json (14 C cards)", "PASS",
        "C cards: c014, c025, c027, c036, c051, c066, c084, c085, c105, c115, c129, c131, c132, c133. Each carries a basis naming its lab part (e.g. 'Lab 1, Part C (50-digit Decimal arithmetic)'). BUILDER_RULES 7 satisfied."),
    row("E1d-cards-basis", "grade T cards are proved on the page or in the lesson", "course/modules/E/E1/cards.json (94 T cards)", "PASS",
        "T cards state a theorem or a formula proved on the page or in the lesson (c004 Prop 1.2; c048 Prop 3.1 and Misconception 3 (L04 line 304); c056 Prop 5.2; c093 Theorem 1.2; c097-c099 Corollary 2.1; c120 Prop 1.3). Numbers derived from those formulas (see E1d-cards-recompute)."),
    row("E1d-cards-c048-basis", "E1-c048 T basis (round-3 FAIL)", "course/modules/E/E1/cards.json E1-c048", "PASS",
        "The round-3 defect (lab numbers on a T card) is removed: c048 now reads 'The forward error is of order h and the central error of order h^2 (Proposition 3.1), so the central quotient is the better check (Misconception 3).' Proposition 3.1 is in L04 line 255 with its proof section; Misconception 3 is L04 line 304 (the third item of Section 5)."),
    row("E1d-cards-duplicates", "full duplicate scan (round-3 FAIL on c019 and c025)", "course/modules/E/E1/cards.json E1-c019, E1-c025", "PASS",
        "No duplicate fronts or backs (scan). c025 is now a different question ('In Lab 1 cases 1 and 4, what does the grid maximiser give when the fixed cost rises from 12 to 100?') graded C with a lab basis; c019 asks the general question and is graded T. The two cards cover the same proposition (Prop 1.5) at different grades; this is a teaching overlap, not a duplicate, so no defect is recorded."),
    row("E1d-cards-locators", "'Problem P1' locator (round-3 FAIL)", "course/modules/E/E1/cards.json E1-c121; course/modules/E/E1/L09.html problem set", "PASS",
        "c121 now reads 'Proposition 1.3, and problem set item P1'. L09 contains 'P1 · The overproduction gap' (line 340) in the problem set. Round-3 locator defect closed."),
    row("E1d-cards-qualitative", "all 133 cards read against the current lesson text (qualitative)", "course/modules/E/E1/cards.json vs L01-L09", "UNVERIFIABLE",
        "Not completed in full. Done: every card read; every card number checked against lab output or recomputed; every locator checked; the cards changed since the round-3 pin were read against the current lesson text (see E1d-cards-changed). Not done: a sentence-by-sentence comparison of the other cards with the lesson bodies changed since the pin (see E1d-lessons-changed-cards).",
        "Finish the card-by-card comparison with the current lesson text of L01-L09 (cards on the changed lesson statements listed in E1d-lessons-changed-cards)."),
    row("E1d-lessons-changed-cards", "cards that quote a lesson statement changed since the round-3 pin",
        "course/modules/E/E1/L01.html ... L09.html (9 files changed, 72 insertions, 69 deletions)", "UNVERIFIABLE",
        "Changed lesson statements include: L01 Remark 1.7 wording, Proposition 1.4 (x* renamed x-bar), Proposition 2.3 wording (\"gives the equality at the optimum\"); L02 'Lab 1' cross-references; L04 Misconception 3 and Lab 1 Part C figure (9.39104696 and 3.88075828 unrounded); L05 Lemma/Remark wording; L06 reaction slope sentence; L07 Undercutting sentence and Lemma 3.2 wording; L08 Pareto Proposition 2.3 and table row wording; L09 Proposition 1.3 hypotheses and Proposition 1.6 hypotheses ('Assume a > 0, b > 0, e >= 0 and c + e < a'). Cards on these statements were re-read only where listed above; the rest were not compared sentence by sentence.",
        "Compare each card on L01-L09 with the current lesson text, and re-grade any card whose hypotheses were changed in those lessons."),
    row("E1d-starter", "starter fails the suite; the page makes no count claim about it", "course/modules/E/E1/grader/starter.py; grader/test_project.py", "PASS",
        "Re-run with starter.py staged: 112 failed, 6 passed (the round-3 count of 106/4 was for an earlier suite). The page does not state a count; the claim 'starter fails the suite' holds. The six passes do not call outcome."),
    row("E1d-citations-note", "Reading and references: no locator, no bibliographic data typed", "course/modules/E/E1/project.html #reading, #references", "PASS",
        "No page or table locator is typed for varian2014intermediate; the references section is generated from data-cite."),
]

MUTANTS = []
for line in (ROOT / S / "mutate_E1_seeds0-9_r4.txt").read_text(encoding="utf-8").splitlines():
    m = re.match(r"^(KILLED|SURVIVED) (\S+?\.py): (.*?) -> (.*)$", line)
    if not m:
        continue
    name = m.group(2)[:-3]
    MUTANTS.append({
        "id": name,
        "description": m.group(3),
        "result": "KILLED" if m.group(1) == "KILLED" and m.group(4) != "None" else m.group(1),
        "killed_by": m.group(4),
    })

counts = {"PASS": 0, "FAIL": 0, "UNVERIFIABLE": 0}
for r in ROWS:
    counts[r["status"]] += 1
verdict = "PASS" if counts["PASS"] == len(ROWS) and all(m["result"] == "KILLED" for m in MUTANTS) else "FAIL"
fragment = {
    "unit": "E1",
    "slice": "E1-d",
    "round": 4,
    "verifier": "independent verifier (Haiku 5.5), round 4 for slice E1-d (project.html, grader, project labs, cards.json, project mutants)",
    "pin": PIN,
    "base": "round-3 pin aa3c26c (previous fragment /tmp/fanout-frags/B-E1-d.round3.json); the round-4 delta touched project.html, test_project.py, cards.json, L01-L09, index.html, the lab twins L01 and project-2, and mutants; rows re-verified where the subject changed",
    "checkout": "/tmp/verifyB4-E1-d",
    "scratch": "/tmp/e1d-v/r4",
    "verified_at": "2026-10-28",
    "verdict": verdict,
    "rows": ROWS,
    "mutants": MUTANTS,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "Round 4 result: the round-3 FAIL on prop-2 (existence) is closed; the c048 basis, the c121 locator and the c019/c025 duplicate rows are closed. "
        "New FAIL: units of b (E1d-units), and the scope claim 'do not apply to a curved one' (E1d-scope-words). "
        "Not completed: the card-by-card comparison with the changed lesson text (E1d-cards-qualitative, E1d-lessons-changed-cards). "
        "Not run: the full repository gate (architect's), render_curriculum, build_site, live EDGAR (none used). The starter count changed; the page does not state it."
    ),
    "summary": {
        "rows": len(ROWS),
        "pass": counts["PASS"],
        "fail": counts["FAIL"],
        "unverifiable": counts["UNVERIFIABLE"],
        "mutants": len(MUTANTS),
        "mutants_killed": sum(1 for m in MUTANTS if m["result"] == "KILLED"),
        "fail_ids": [r["id"] for r in ROWS if r["status"] == "FAIL"],
        "unverifiable_ids": [r["id"] for r in ROWS if r["status"] == "UNVERIFIABLE"],
    },
}
out = ROOT / "ledgers/E1/E1-d.json"
out.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out, counts, len(MUTANTS))
