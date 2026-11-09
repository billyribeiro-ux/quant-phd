"""Verifier round 1 (slice d): writes ledgers/E1/E1-d.json from the mutation run output and the row evidence below.

Reads ledgers/E1/scripts/E1-d-r1/mutate_all_seeds_0_9.out (output of: .venv/bin/python tools/mutate_graders.py --unit E1
--seeds 0-9) for the mutant list. Every row's evidence names the script or command that produced it (repository path or exact command).
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
PIN = "aeb512b65b7774b59b84f836a13984fcfe9d0d1f"
S = "ledgers/E1/scripts/E1-d-r1"

rows = [
    {"id": "E1d-r1-ladder", "check": "2.6-spec", "location": "course/modules/E/E1/project.html lines 40-49, 55-257, 558-565",
     "status": "PASS",
     "evidence": "Rung 1 (Lab 1, lines 58-118) has a comment on every step. Rung 2 is a completion lab (line 130, class 'lab completion') whose in-browser run button compares output with the expected block (tools/page_smoke.py line 272-283 fills the twin and requires 'matches the expected result'). Rung 3 scope matches curriculum/02-economics-finance-core.yaml E1 project brief (monopoly vs Cournot vs Bertrand; welfare and fee outcomes; grading both). Rung 4 is open-ended (lines 558-565). Observation only: the rung-2 blurb at line 45 says 'compare its printed lines', while sibling projects (AC1, AC2) say 'graded instantly'; the in-browser check is the same, so this is wording, not a finding."},
    {"id": "E1d-r1-spec-precedence", "check": "2.6-spec", "location": "course/modules/E/E1/project.html line 320 (Constraints)", "status": "FAIL",
     "evidence": "The Constraints list the ValueError conditions (structure name; a <= b*c; b <= 0; c <= 0) and say 'the message states the condition', but do not say which message applies when two or more conditions fail at once (e.g. b = 0 and a <= 0: 'a must exceed b*c' or 'b must be positive'). A competent student would have to ask this. The suite does not depend on the answer: every parametrized invalid case in grader/test_project.py lines 276-291 violates exactly one condition (e.g. (10,0,5): a=10 > bc=0), and the structure cases use valid a,b,c (lines 251-273). Checked by reading those lines and by the reference (grader/reference.py lines 26-35) which uses the listed order.",
     "fix": "Add to the Constraints sentence: 'When more than one of these conditions holds, the message of any one of them is accepted.' No test change is needed."},
    {"id": "E1d-r1-spec-tests-align", "check": "2.6-spec", "location": "course/modules/E/E1/project.html lines 318-322; grader/test_project.py", "status": "PASS",
     "evidence": "Each stated constraint has a test: exact keys (line 111), int types (118-120), closed forms (125-131), ordering (134-171), exact-half ties (198-222), below/above half (333-350), large exact inputs (323-330), stdlib-only (353-364), no print/warn (235-240, 367-381), smallest b and c (294-319), second instance (391-398), ValueError table (251-291). pytest --collect-only reports 124 (see E1d-r1-autograder-count)."},
    {"id": "E1d-r1-hours", "check": "2.9-hours", "location": "course/modules/E/E1/project.html lines 336-348; course/modules/E/E1/index.html line 29; curriculum/02-economics-finance-core.yaml line 18-21",
     "status": "PASS",
     "evidence": "Table rows 2+3+8+8+6+3 = 30 = data-hours-project (index.html line 29: data-hours-lessons 90, data-hours-project 30; 90+30 = 120 = curriculum hours). Verifier estimate: rung 1 about 2 h, rung 2 about 3 h, five proofs about 8-10 h (Prop 3 case analysis and Prop 5 rounding argument are the long ones), engine plus 124-test iteration about 5-8 h, welfare analysis and memo with five-section body and restated appendix about 4-6 h, self-assessment about 2-3 h. Total about 24-34 h, within 30 +/- 30%."},
    {"id": "E1d-r1-lab1-run", "check": "2.5-lab", "location": "course/modules/E/E1/project.html lines 55-128; tests/labs/E1/lab-E1-project-1.py",
     "status": "PASS",
     "evidence": "tools/run_labs.py --unit E1 --page project: 'run_labs E1: PASS (3/3)'. ledgers/E1/scripts/E1-d-r1/check_labs.py (saved as check_labs.out): page code equals the twin (check_lab_trailing.py: equal after the final newline, which the page omits); twin run with python -I -W error exits 0 with empty stderr; stdout equals the expected block (output 'expected == output: True')."},
    {"id": "E1d-r1-lab2-completion", "check": "2.5-lab", "location": "course/modules/E/E1/project.html lines 130-187; tests/labs/E1/lab-E1-project-2.py",
     "status": "PASS",
     "evidence": "Page code differs from the twin only at lines 160 (return ___) and 165 (return half_up(___)); every other line equals the twin (unified diff in ledgers/E1/scripts/E1-d-r1/check_labs.py output). Blank-filled code equals the twin (check_lab_trailing.py: 0 ___ remain after filling). Twin output: 'True / 67 / 53 / 4444', equal to the expected block. page_smoke --unit E1 --pages project: 'lab lab-E1-project-2: 0.0 s' and the in-browser run passes."},
    {"id": "E1d-r1-lab3-run", "check": "2.5-lab", "location": "course/modules/E/E1/project.html lines 189-257; tests/labs/E1/lab-E1-project-3.py",
     "status": "PASS",
     "evidence": "run_labs E1 page project PASS (3/3). Page code equals the twin (equal after final newline). Twin output (12 lines for a=120 and a=121) equals the expected block (check_labs.py: 'expected == output: True'). Every value re-derived by ledgers/E1/scripts/E1-d-r1/rederive_numbers.py (a=121 block: 51/71/2550/1275/3825/1275, 67/54/2267/2267/4534/567, 101/20/0/5101/5101/0 all PASS)."},
    {"id": "E1d-r1-lab1-prose", "check": "2.5-lab", "location": "course/modules/E/E1/project.html lines 57, 64-65, 127", "status": "PASS",
     "evidence": "Hypothesis and interpretation claims checked against the output: d=100; monopoly 50 trades, 70 cents; Cournot 200/3 -> 67, 160/3 -> 53; Bertrand 100, 20, DWL 0; profit 20000/9 -> 2222 (total of two exchanges, (fee-c)*volume); last line prints 'True | True'. rederive_numbers.py 'ref ...' checks PASS."},
    {"id": "E1d-r1-lab2-prose", "check": "2.5-lab", "location": "course/modules/E/E1/project.html lines 132, 138-139, 186", "status": "PASS",
     "evidence": "Error recurrence e_{k+1} = -e_k/2 with e_0 = -d/3 (line 186) re-derived by hand; size d/(3*2^60) = 2.9e-17 < 1e-12 (rederive_numbers.py prop2 iteration check for k=1..7 over the grid: PASS). 40000/9 = 4444.44 and 160/3 = 53.33 match the printed values (rederive_numbers.py)."},
    {"id": "E1d-r1-lab3-prose", "check": "2.5-lab", "location": "course/modules/E/E1/project.html lines 191, 256", "status": "PASS",
     "evidence": "a=121: fee 141/2 -> 71, volume 101/2 -> 51, monopoly profit 10201/4 = 2550.25 -> 2550 (rederive_numbers.py PASS). Line 256: 200/3 = 66.67 and 202/3 = 67.33 both lie in (66.5, 67.5), so Cournot volume prints 67 in both cases (exact arithmetic)."},
    {"id": "E1d-r1-prop1", "check": "2.4-math", "location": "course/modules/E/E1/project.html lines 285-286 (Proposition 1)", "status": "PASS",
     "evidence": "Re-derived by hand: pi(Q) = (d-Q)Q/b, pi' = (d-2Q)/b, pi'' = -2/b, maximiser d/2, fee (a+bc)/(2b), profit d^2/(4b); f-c = d/(2b). Exact identity profit = d^2/(4b) checked on a grid b<=5, c<=39, gap<=119 (rederive_numbers.py 'grid identities', PASS)."},
    {"id": "E1d-r1-prop2", "check": "2.4-math", "location": "course/modules/E/E1/project.html lines 289-292 (Proposition 2)", "status": "PASS",
     "evidence": "Re-derived by hand: pi_i = (d-q_i-q_j)q_i/b, BR = max(0,(d-q_j)/2); case q_1=0 gives q_2=d/2 and then q_1=d/4 (contradiction); subtraction gives q_1=q_2; q=d/3; iteration error recurrence verified. Grid identity 2d^2/(9b) and iteration error d/(3*2^k) PASS (rederive_numbers.py). Brute-force grid (ledgers/E1/scripts/E1-d-r1/grid_equilibria.py, saved as grid_equilibria.out) shows the symmetric point d/3 on grid; the asymmetric grid points it also lists are midpoint ties of the grid-restricted best response, a grid artifact, not a counterexample."},
    {"id": "E1d-r1-prop3", "check": "2.4-math", "location": "course/modules/E/E1/project.html lines 294-297 (Proposition 3)", "status": "PASS",
     "evidence": "Hand proof checked case by case: f_1 < c; f_1 = c (f_2 = c or > c); f_1 > c with f_2 = f_1 or > f_1; each deviation (to c, to (c+f_1)/2, to (f+c)/2, to g in (c,f_2)) strictly gains and stays in [0, a/b] because c < f_1 <= a/b. Complete. Brute force (grid_equilibria.py) gives (c,c) on every grid tested; a second symmetric grid point just above c appears only at the grid's resolution because the deviation (c+f)/2 is off-grid. The proof, not the grid, is the evidence here."},
    {"id": "E1d-r1-prop4", "check": "2.4-math", "location": "course/modules/E/E1/project.html lines 299-301 (Proposition 4)", "status": "PASS",
     "evidence": "CS = int_0^Q (Q-t)/b dt = Q^2/(2b); G(x) = (ax - x^2/2)/b; W' = (d-x)/b; W(d)-W(Q) = (d-Q)^2/(2b); f(Q)Q = G(Q) - Q^2/(2b). Identity welfare = CS + profit and the DWL formula checked on the grid (rederive_numbers.py, PASS)."},
    {"id": "E1d-r1-prop5", "check": "2.4-math", "location": "course/modules/E/E1/project.html lines 304-306 (Proposition 5)", "status": "PASS",
     "evidence": "Exact differences checked (d/6, d/3, d/(6b), d/(3b), d^2/(8b)-d^2/(18b) = 5d^2/(72b), d^2/(36b)). Rounding claim: exact adjacent differences > 1 whenever d > 6b; printed order checked with explicit directions on 304,940 cases (b<=10, c<=79, gap in (6b, 420)): 0 failures; minimum exact adjacent difference 1.017 (fee). Script: ledgers/E1/scripts/E1-d-r1/rederive_numbers.py, output rederive_numbers.out (line 'Prop 5 printed order ... cases=304940 failures=[]')."},
    {"id": "E1d-r1-conventions", "check": "2.9-prose", "location": "course/modules/E/E1/project.html line 328 (Conventions)", "status": "FAIL",
     "evidence": "Line 328 reads 'The closed forms of Propositions 1 to 3 are the values the module reports.' The module reports six outputs (grader/reference.py lines 60-67; starter lines 16-19). Consumer surplus, welfare and deadweight loss come from Proposition 4 (lines 299-301), and the page elsewhere says Propositions 1 to 4 (lines 53, 256, 281-282). The sentence omits Proposition 4 and gives no surplus values.",
     "fix": "Replace 'Propositions 1 to 3' with 'Propositions 1 to 4' and add that consumer surplus, welfare and deadweight loss are the values of Proposition 4."},
    {"id": "E1d-r1-notation", "check": "2.9-notation", "location": "course/modules/E/E1/project.html (all math); notation/notation.json",
     "status": "PASS",
     "evidence": "notation.json registers 8 symbols (T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, \\mathbb{Q}) and 26 macros. Symbols used on the page (token scan of every \\( \\) expression): a, b, c, d, f, q, Q, W, G, pi, e, g, i, j, k, n, t, x and the LaTeX commands. None is a registered symbol. The plain Q (volume) is not \\mathbb{Q} (the probability measure). No registered macro is used."},
    {"id": "E1d-r1-dag", "check": "2.9-dag", "location": "course/modules/E/E1/project.html; curriculum/02-economics-finance-core.yaml lines 18-37; check_dag E1", "status": "PASS",
     "evidence": "tools/check_dag.py --unit E1: PASS. The page's concepts (monopoly, Cournot, Bertrand, consumer surplus, deadweight loss, welfare, equilibrium, best response) are introduced in E1 (curriculum 'introduces' keys monopoly, cournot-competition, bertrand-competition, economic-surplus, deadweight-loss) and taught in lessons L05-L07 (Monopoly Pricing; Oligopoly: Cournot and Bertrand; Surplus and Deadweight Loss). The page has no class='concept' links (grep count 0). No later-unit concept appears."},
    {"id": "E1d-r1-process-words", "check": "2.9-prose", "location": "course/modules/E/E1/project.html (whole file)", "status": "PASS",
     "evidence": "grep -i for verifier, ledger, fragment, builder, agent, round N, TODO, TBD, lorem, for brevity, details omitted, beyond the scope, left as an exercise, you can add more, it is important to note, studies show, experts agree, it is well known, obviously, clearly, roughly, historically, ellipsis: no hits. 'just' occurs once (line 296, 'the case just excluded'), which is not a banned phrase."},
    {"id": "E1d-r1-citation", "check": "2.1-citations", "location": "course/modules/E/E1/project.html lines 567-573 (Reading, data-cite varian2014intermediate); references/references.json entry varian2014intermediate",
     "status": "PASS",
     "evidence": "Registry entry: title 'Intermediate Microeconomics: A Modern Approach', author Varian, Hal R., year 2014, ISBN 9780393919677, verified_by openlibrary, used_by E1. tools/verify_refs.py --unit E1 (live, run in this checkout): 'live re-verification of E1: 1 of 560 entries, 0 problems'. tools/verify_refs.py --offline: 560 entries, 0 problems. The page attributes no statement to the source (line 569: 'No passage locator from it has been confirmed'), so no locator is needed."},
    {"id": "E1d-r1-autograder-reference", "check": "2.6-autograder", "location": "course/modules/E/E1/grader/reference.py; tools/run_graders.py",
     "status": "PASS",
     "evidence": "tools/run_graders.py --unit E1 --seeds 0-49: 'run_graders E1: PASS (reference 50/50 seeds, slowest 0.2 s)'. The same run checks the starter fails and that instance.py is deterministic and varies across seeds."},
    {"id": "E1d-r1-autograder-count", "check": "2.6-autograder", "location": "course/modules/E/E1/project.html line 322; grader/test_project.py",
     "status": "PASS",
     "evidence": "Collect-only run in a scratch copy of grader/test_project.py + instance.py + reference.py as market_structure.py: '124 tests collected'. Page says 124 checks (line 322)."},
    {"id": "E1d-r1-autograder-instances", "check": "2.6-autograder", "location": "course/modules/E/E1/grader/instance.py; ledgers/E1/scripts/E1-d-r1/rederive_numbers.py",
     "status": "PASS",
     "evidence": "make_instance(seed) for seeds 0-19 (rederive_numbers.py): every case has a > bc > 0, 1<=b<=3, 5<=c<=60, 60<=d<=400 and d > 6b; the 20 (a,b,c) triples are distinct; Cournot welfare varies from 1423 (seed 7) to 56327 (seed 9), so answers change, not just labels. Matches the page spec at line 316."},
    {"id": "E1d-r1-autograder-messages", "check": "2.6-autograder", "location": "course/modules/E/E1/grader/test_project.py lines 50-102, 114-398", "status": "PASS",
     "evidence": "Every failure message was read. Each names a property (e.g. 'the ValueError for ... must state the condition it checks', 'welfare for ... must be consumer surplus plus exchange profit'). None prints an expected value. The Bertrand-fee message names the rule (fee equals the cost), which is the property, not a number."},
    {"id": "E1d-r1-autograder-browser", "check": "2.6-autograder", "location": "course/modules/E/E1/project.html (grader panel line 354); tools/page_smoke.py",
     "status": "PASS",
     "evidence": "tools/page_smoke.py --unit E1 --pages project: 'in-browser grader: All 124 tests pass on seed 630076010. (0.9 s)'; labs 0.0 s each; 'page_smoke modules/E/E1/project.html: PASS'."},
    {"id": "E1d-r1-mutants-existing", "check": "2.6-mutation", "location": "ledgers/E1/mutants/ (125 mutants from earlier rounds)", "status": "PASS",
     "evidence": "tools/mutate_graders.py --unit E1 --seeds 0-9 (run before this round's additions): 'mutate_graders E1: PASS (125/125 killed)'. Re-run after adding the six mutants below: 131/131 killed (/tmp/e1d-r1-mutate2.txt, output recorded in the mutants list)."},
    {"id": "E1d-r1-mutants-new", "check": "2.6-mutation", "location": "ledgers/E1/mutants/e1d_r1_m01..m06*.py", "status": "PASS",
     "evidence": "Six new student-error mutants, each killed: m01 Cournot volume d/3 (killed by test_closed_form_matches[consumer_surplus_cents-cournot] at seed 0); m02 dict lookup gives KeyError (test_unknown_structure_raises_value_error[duopoly]); m03 Cournot profit doubled (test_closed_form_matches[profit_cents-cournot]); m04 monopoly profit on gap d (test_closed_form_matches[profit_cents-monopoly]); m05 Cournot fee from printed volume (test_reference_case_matches_closed_forms[profit_cents-cournot]); m06 Cournot volume from 61 iteration steps (test_tie_rounds_up_for_each_output[cournot-deadweight_loss_cents-10-1-1]). Killed by the test named in the mutants list."},
    {"id": "E1d-r1-alternatives", "check": "2.6-over-constraint", "location": "ledgers/E1/scripts/E1-d-r1/alternatives/ (alt1-alt5 from earlier rounds; alt_a, alt_b, alt_c this round); ledgers/E1/scripts/E1-d-r1/run_alt_seeds_0_9.py",
     "status": "PASS",
     "evidence": "Eight candidate implementations with different algorithms run through the repository test_project.py and instance.py for seeds 0-9 (run_alt_seeds_0_9.py, saved as alternatives_seeds_0_9.out: 'ok' on all seeds for alt1-alt4, alt_a (Decimal at 60 digits, checks reordered), alt_b (integer numerator rounding (2p+q)//(2q)), alt_c (Cramer solve and exact Simpson)). No correct alternative fails, so no over-constraint. alt5 (float arithmetic) fails 3 tests on every seed, all test_large_exact_inputs_round_from_exact_values; that is the right rejection, since the Constraints require exact fractions."},
    {"id": "E1d-r1-rubric-structure", "check": "2.6-rubric", "location": "course/modules/E/E1/project.html lines 384-396 (rubric table)", "status": "PASS",
     "evidence": "Six criteria C1-C6, four levels each, rows data-criterion C1..C6 (lines 388-393). Level descriptors read; each contains the one below it under the page's scoring rule (line 380). Observability: all descriptors are observable except C6 level 2 (separate row)."},
    {"id": "E1d-r1-rubric-C6-observable", "check": "2.6-rubric", "location": "course/modules/E/E1/project.html line 393 (C6 level 2); line 460 (Exemplar A annotation)", "status": "FAIL",
     "evidence": "C6 level 2 reads 'Names one or more of the limits, and states what changes for fewer than three of them.' Zero is fewer than three, so a memo naming a limit and stating no change meets level 2 on the literal reading; level 1 reads 'No limit is stated.' Exemplar A names one limit and states no change (line 456), and its annotation (line 460) says it 'meets C6 level 2 ... without what changes'. The descriptor therefore does not separate level 1 from level 2 for the case the exemplar shows. Calibration is not broken (level 1 vs 2 is within one level), but the descriptor is not observable as the rule demands.",
     "fix": "Change C6 level 2 to 'states what changes for at least one and fewer than three of them', then re-score Exemplar A's C6 (currently 2, data-scores on line 401 and the annotation on line 460) to the level the clarified descriptor gives, or state explicitly that a limit named without a change meets level 2."},
    {"id": "E1d-r1-rubric-calibration", "check": "2.3-rubric-calibration", "location": "course/modules/E/E1/project.html lines 401-549 (Exemplars A and B, memo texts)", "status": "PASS",
     "evidence": "Scored both exemplars from the rubric descriptors (lines 386-393) against the memo passages. Exemplar A: C1 1, C2 2, C3 2, C4 2, C5 1, C6 2 (C6 read literally; 1 on the stricter reading). Exemplar B: C1 4, C2 4, C3 4, C4 4, C5 3, C6 2. Official: A 1,2,2,2,1,2; B 4,4,4,4,3,2. All within one level on every criterion. Caveat: this was not blind; I had read the annotations and official scores before scoring. The within-one-level result therefore counts as weaker evidence than a blind run."},
    {"id": "E1d-r1-exemplar-annotations", "check": "2.6-rubric", "location": "course/modules/E/E1/project.html lines 401, 466, 411-546 (data-scores, annotations)", "status": "PASS",
     "evidence": "data-scores 1,2,2,2,1,2 and 4,4,4,4,3,2 agree with the official scoring text (lines 403, 468). Annotated numeric claims re-derived: Exemplar B C4 gives d^2/(36b) = 10000/36 = 277.8 (rederive_numbers.py 'exB' checks, PASS); the Exemplar B Derivations and Welfare passages match the closed forms."},
    {"id": "E1d-r1-data-simulated", "check": "2.8-data", "location": "course/modules/E/E1/project.html lines 53, 316; course/modules/E/E1/grader/instance.py line 3",
     "status": "PASS",
     "evidence": "No dataset is read (grep data-files: 0 hits in project.html). The autograder instance is labelled SIMULATED (project.html line 316; instance.py docstring line 3). The memo's reference case is stated as an input, not data (line 53, line 316)."},
    {"id": "E1d-r1-docstring-units", "check": "2.9-code-quality", "location": "tests/labs/E1/lab-E1-project-2.py line 27 (reaction docstring); course/modules/E/E1/project.html line 158-159", "status": "FAIL",
     "evidence": "BUILDER_RULES section 6.2 requires docstrings that state units. The docstring of reaction() reads 'The best quantity of one exchange against a rival quantity: q_i = (d - q_j) / 2.' and gives no unit for the quantities (trades). The other lab functions state units or are dimensionless (volume_and_fee, welfare_cents).",
     "fix": "Add the unit to the reaction docstring, e.g. 'q_i = (d - q_j) / 2, in trades.' Make the same change in the page code block at line 159 so that run_labs still finds the page equal to the twin (the completion blank on line 160 stays)."},
    {"id": "E1d-r1-gates", "check": "2.5-gates", "location": "repository gates on the checkout at aeb512b",
     "status": "PASS",
     "evidence": ".venv/bin/ruff check and ruff format --check on tests/labs/E1 and the grader: 'All checks passed', '12 files already formatted'. .venv/bin/mypy --no-incremental: 'Success: no issues found in 385 source files'. mypy --strict on grader reference, starter, instance and the three twins: no issues. pytest tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py tests/test_page_smoke.py: 414 passed. tools/check_pages.py --unit E1: PASS. tools/check_dag.py --unit E1: PASS. tools/check_projects.py --unit E1: PASS. tools/run_labs.py --unit E1 --page project: PASS (3/3)."},
    {"id": "E1d-r1-structure-order", "check": "2.9-structure", "location": "course/modules/E/E1/project.html (section order)", "status": "PASS",
     "evidence": "Order: ladder, rungs with labs, model (definitions, propositions), specification (dl spec, conventions), hours, autograder panel, running locally, memo (brief, rubric, exemplars, self-assessment), stretch, reading, references, module navigation. tools/check_pages.py --unit E1: PASS."},
    {"id": "E1d-r1-atlas-studio", "check": "2.6-atlas", "location": "course/modules/E/E1/project.html", "status": "PASS",
     "evidence": "Not applicable to this module project: grep -c 'atlas|data-files' course/modules/E/E1/project.html = 0; the unit is a module, not a studio or Atlas milestone."},
]

mutants = []
for line in (ROOT / S / "mutate_all_seeds_0_9.out").read_text(encoding="utf-8").splitlines():
    if not (line.startswith("KILLED ") or line.startswith("SURVIVED ")):
        continue
    head, _, rest = line.partition(": ")
    name = head.split(" ", 1)[1]
    description, _, killed = rest.rpartition(" -> ")
    mutants.append({"id": name.removesuffix(".py"), "description": description,
                    "killed_by": None if killed.startswith("None") or line.startswith("SURVIVED") else killed})

fragment = {
    "unit": "E1",
    "slice": "d",
    "round": 1,
    "verifier": "verifyS1-E1-d (Haiku 5.5)",
    "pin": PIN,
    "base": PIN,
    "checkout": str(ROOT),
    "scratch": "/tmp",
    "verified_at": "2026-11-09T03:05:15+00:00",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "Scope: project.html, grader/, project labs (tests/labs/E1/lab-E1-project-1..3), mutants, alternatives (seeds 0-9), "
        "per the slice definition. Cards, lessons L01-L09 and notation/DAG of the whole unit are outside this slice and "
        "are not verified here. Overwrite notice: ledgers/E1/E1-d.json previously held the round-11 fragment of slice d "
        "(83 rows, including E1d-cards-* rows and an E1d-notation-r11/E1d-dag-r11 pair). This round-1 fragment replaces it "
        "as instructed; the round-11 file remains in git (HEAD: ledgers/E1/E1-d.json). The round-11 cards rows are not "
        "carried here. The orchestrator must decide whether the merged E1 ledger still needs them. The round-1 "
        "instruction says 'first verification', but the repository already holds rounds 2-11 of this slice; the "
        "round number was taken from the instruction. Calibration (E1d-r1-rubric-calibration) was not blind. "
        "Grid checks (grid_equilibria.py) are artifacts-limited and were used only to refute, not to prove, Props 2-3. "
        "Hours: estimate by the verifier, not a measurement."
    ),
    "summary": (
        "Slice d (project page, grader, project labs, mutants, alternatives). 4 FAIL rows: spec precedence of ValueError "
        "conditions (E1d-r1-spec-precedence), Conventions cites Propositions 1 to 3 for all reported values "
        "(E1d-r1-conventions), C6 level-2 descriptor not observable (E1d-r1-rubric-C6-observable), reaction() docstring "
        "lacks units (E1d-r1-docstring-units). All numbers, five propositions, three labs, the 124-test suite, the 50-seed "
        "reference run, the 131 mutants and eight alternatives pass."
    ),
}

out = ROOT / "ledgers/E1/E1-d.json"  # round-1 fragment for slice d
out.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out, "rows", len(rows), "mutants", len(mutants), "killed", sum(1 for m in mutants if m["killed_by"]))
