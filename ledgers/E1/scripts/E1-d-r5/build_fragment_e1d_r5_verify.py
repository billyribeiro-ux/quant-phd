"""Build the round-5 E1-d fragment (ledgers/E1/E1-d.json) from this round's outputs. Verdicts are computed, not asserted."""

import json
import re
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path

CHK = Path("/Users/billyribeiro/.fanout/wt/verifyS5-E1-d")
OUT = CHK / "ledgers/E1/scripts/E1-d-r5/out"
sys.path.insert(0, str(CHK / "tools"))
import ledger  # noqa: E402

mutants = []
for line in (OUT / "mutate_E1_0-9_r5.out").read_text(encoding="utf-8").splitlines():
    m = re.match(r"^(KILLED|SURVIVED) (\S+): (.*)$", line)
    if not m:
        continue
    body, _, killed = m.group(3).rpartition(" -> ")
    mutants.append({
        "name": m.group(2),
        "description": body.strip(),
        "killed_by": killed.strip() if m.group(1) == "KILLED" else None,
    })

R = []


def row(id_, check, location, status, evidence, fix=None):
    r = {"id": id_, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    R.append(r)


PAGE = "course/modules/E/E1/project.html"
row("E1d-r1-ladder", "2.6-spec", f"{PAGE} lines 40-49 (ladder), 51-189 (rungs: Labs 1-2 only), 295-368 (check: Lab 3), 564 (stretch)", "PASS",
    "Re-verified in round 5 from a full read of the page (project.html changed since edbb7aa8). Line 42 skip-rule points to #placement, which exists at course/modules/E/E1/index.html:68. Rungs section ends at line 189; Lab 3 (line 298) sits in section#check (line 295). check_projects.out: PASS.")
row("E1d-r1-spec-precedence", "2.6-spec", f"{PAGE} line 251; grader/test_project.py lines 251-291", "PASS",
    "Re-verified. Each table case violates only the condition it names: (20,2,10), (19,2,10), (-3,1,1) only a<=bc; (10,0,5), (10,-1,5) only b; (10,2,0), (10,2,-1) only c. Reference passes seeds 0-49 (run_graders.out: 50/50).")
row("E1d-r1-spec-tests-align", "2.6-spec", f"{PAGE} lines 251-253; grader/test_project.py lines 92-102, 214-222, 267-291", "PASS",
    "Re-verified. Spec's exception table (ValueError for structure, a<=bc, b<=0, c<=0) matches the must_raise calls; no other exception type is demanded.")
row("E1d-r1-hours", "2.9-hours", f"{PAGE} lines 33, 270-276; course/modules/E/E1/index.html lines 38-40", "PASS",
    "Re-verified. Component hours 2+3+8+8+6+3 = 30 (page 270-276); data-hours-project=30 (page line 33); hub reads '90 h lessons · 30 h project (25% of the 120 h)' (index.html line 40): 30/120 = 25%, 90+30 = 120. The round-5 hub edit is arithmetically consistent.")
row("E1d-r1-lab1-run", "2.5-lab", f"{PAGE} lines 55-128; tests/labs/E1/lab-E1-project-1.py", "PASS",
    "Re-verified. run_labs E1: PASS (12/12). Page code block == twin (python twin_page_r5.py: 'page code == twin: True', 61 lines). Twin under python -I -W error exits 0 and its stdout equals the expected block.")
row("E1d-r1-lab2-completion", "2.5-lab", f"{PAGE} lines 130-187 (blanks at lines 160, 165); tests/labs/E1/lab-E1-project-2.py", "PASS",
    "Re-verified. Page code differs from the twin only at the two blank lines (diff: twin 'return (d - rival) / 2' vs page '___'; twin welfare line vs page '___'), as the completion rule allows. Twin exits 0 under -I -W error; its output equals the expected block (3 lines). Completed solution: reaction (d-rival)/2, welfare half_up((a*Q - Q*Q/2)/b - c*Q) = 4444.")
row("E1d-r1-lab3-run", "2.5-lab", f"{PAGE} lines 298-367; tests/labs/E1/lab-E1-project-3.py", "PASS",
    "Re-verified. Page code == twin (57 lines); twin exits 0; output equals expected block. Every printed value re-derived in rederive_r5.out / by hand: a=120 rows 50/70/2500/1250/3750/1250, 67/53/2222/2222/4444/556, 100/20/0/5000/5000/0; a=121 rows 51/71/2550/1275/3825/1275, 67/54/2267/2267/4534/567, 101/20/0/5101/5101/0.")
row("E1d-r1-lab1-prose", "2.5-lab", f"{PAGE} lines 57 (hypothesis), 127 (interpretation)", "FAIL",
    "Line 57 and the numbers in line 127 (50 trades, 70 cents, 200/3 printed 67, 160/3 printed 53, 20000/9 printed 2222, Bertrand fee 20, volume 100) are correct against the output. Defect in line 127: 'It does not check that the closed forms are equilibria (...); Propositions 2 and 3 prove that they are.' The monopoly closed form is a profit maximiser (Proposition 1, line 216), not an equilibrium under the page's own 'Equilibrium, in words' definition (line 205, which needs another exchange's choice). So the sentence says the monopoly closed form is an equilibrium and names only Propositions 2 and 3 as proving it. Checked by reading lines 202-205 and 215-218 and by the output of lab-E1-project-1.",
    fix="In project.html line 127 replace the tail with: 'It does not check optimality or equilibrium: Proposition 1 proves that the monopoly volume maximises profit, and Propositions 2 and 3 prove that the Cournot and Bertrand profiles are equilibria (the term is defined under Definitions).' Builder owning project.html (Builder E); no change to the printed output.")
row("E1d-r1-lab2-prose", "2.5-lab", f"{PAGE} lines 132, 138-139, 186", "PASS",
    "Re-verified. Iteration error after 60 steps is d/(3*2^60) = 100/(3*2^60) ~ 2.9e-17 < 1e-12 (matches the printed True). 40000/9 = 4444.44 -> 4444; 160/3 = 53.33 -> 53. 'Proposition 2' cited for (d-q_j)/2 exists (line 221).")
row("E1d-r1-lab3-prose", "2.5-lab", f"{PAGE} lines 300, 366", "PASS",
    "Re-verified. 'monopoly welfare 3750 and Cournot welfare 4444' (a=120) and 'profit 10201/4 = 2550.25 prints 2550' (a=121) match the output and rederive_r5.out. 200/3 and 202/3 both lie in (66.5, 67.5) so Cournot prints 67 in both cases (line 366 claim correct).")
row("E1d-r1-prop1", "2.6-proof", f"{PAGE} lines 215-218 (Proposition 1)", "PASS",
    "Re-derived. pi(Q) = -Q^2/b + (d/b)Q; pi' = (d-2Q)/b; max at d/2; profit d^2/(4b); fee (a+bc)/(2b). rederive_r5.py sweep: 19,440 (a,b,c) cases (b 1..3, c 1..60, d 1..59 and 60..400 step 7): profit at d/2 equals d^2/(4b); strict maximum checked at d/2 +/- offsets. 0 failures.")
row("E1d-r1-prop2", "2.6-proof", f"{PAGE} lines 220-223 (Proposition 2)", "PASS",
    "Re-derived. Reaction max(0,(d-q_j)/2); case analysis excludes q_i = 0 (if q_1 = 0 then q_2 = d/2 and q_1 = d/4 > 0); symmetric point d/3; fee (a+2bc)/(3b); profit each d^2/(9b), total 2d^2/(9b). Iteration error magnitude d/(3*2^k) checked for k=1..8 in 19,440 cases (0 failures). brute_r5.out: grid best response equals (d-q_j)/2, max deviation 0.0 over 7 cases.")
row("E1d-r1-prop3", "2.6-proof", f"{PAGE} lines 225-228 (Proposition 3)", "PASS",
    "Re-derived case by case (f_1<c; f_1>c with f_2>f_1; f_1=f_2>c; f_1=c<f_2; (c,c) is an equilibrium). Each deviation is profitable as the proof states; I found no gap. brute_r5.out: on a fee grid (coarse step 1/4, deviations step 1/200) the only equilibrium profile is (c,c) in 5 cases (a=9,12,20,31,11).")
row("E1d-r1-prop4", "2.6-proof", f"{PAGE} lines 230-233 (Proposition 4)", "PASS",
    "Re-derived. CS = integral (Q-t)/b = Q^2/(2b); W' = (d-x)/b; W(d)-W(Q) = (d-Q)^2/(2b); welfare = CS + profit. Numeric Simpson checks of CS, DWL and welfare identity over 19,440 cases: 0 failures (rederive_r5.out).")
row("E1d-r1-prop5", "2.6-proof", f"{PAGE} lines 235-238 (Proposition 5)", "PASS",
    "Re-derived. Exact identities: d/(6b) fee gap, 5d^2/(72b) welfare gap (= 6250/9 at the reference case, computed), d^2/(36b) profit gap (= 2500/9 at the reference case). The printed-integer claim (d > 6b, half-up rounding moves each value by at most 1/2, every exact difference > 1) holds: rederive_r5.py checks the printed order of volumes, fees, DWL, welfare and profit over all cases with d > 6b: 0 failures. The proof's inequalities (d/6 > b, d/3 > 2b, d^2/(18b) > 2b, 5d^2/(72b) > 5b/2, d^2/(36b) > b, 2d^2/(9b) > 8b) each check out.")
row("E1d-r1-conventions", "2.6-spec", f"{PAGE} lines 258-260 (Conventions)", "PASS",
    "Re-verified. Monopoly, Cournot and Bertrand closed forms (volume, fee) match Propositions 1-3; Proposition 4 gives CS, welfare and DWL; 'Cournot profit is the total of the two exchanges' matches (f-c)Q with Q = 2d/3 (20000/9 at the reference case, per Lab 1).")
row("E1d-r1-notation", "13-notation", f"{PAGE} math spans; notation/notation.json symbols and macros", "PASS",
    "Re-verified. TeX commands on the page: \\ge \\int \\max \\pi \\square \\cdot \\big \\le \\mapsto \\in \\lfloor \\rfloor (standard, none registered). Registered symbols T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q} do not occur as math on the page (grep: 0 hits for Phi, gamma, R_f, R^, ast, mathbb). The 5 'T' hits are data-grade=\"T\" on the five propositions, not a symbol. Letters a, b, c, d, Q, q, f, W, G, pi are local and not registered.")
row("E1d-r1-dag", "14-dag", f"{PAGE} (no data-concept links); check_dag.out", "PASS",
    "check_dag E1: PASS (round-5 run). project.html has 0 data-concept attributes, so no concept outside the closure is linked. Cross-lesson reference is to 'Lessons 5 to 7' inside E1, within the unit.")
row("E1d-r1-process-words", "12-process-words", f"{PAGE} (whole file)", "PASS",
    "Re-verified by grep for verifier, builder, ledger, checker, round, TODO, draft: no learner-text hits. 'memo draft' (line 274) is a learner task.")
row("E1d-r1-citation", "3-attribution", f"{PAGE} lines 573-579 (Reading); references/references.json key varian2014intermediate", "PASS",
    "Re-verified. Reading section states no passage locator is confirmed and attributes no statement. verify_refs.py --offline: 560 entries, 0 problems (verify_refs_offline_r5.out). The only cite is data-cite varian2014intermediate.")
row("E1d-r1-autograder-reference", "2.6-autograder", "course/modules/E/E1/grader/reference.py; tools/run_graders.py", "PASS",
    "run_graders E1 --seeds 0-49: PASS (reference 50/50 seeds, run_graders_0_49.out). grader/* unchanged since edbb7aa8 (git diff --name-only: 0 files), and reference.py is the solution used.")
row("E1d-r1-autograder-count", "2.6-autograder", f"{PAGE} line 253; grader/test_project.py", "PASS",
    "pytest --collect-only on a scratch copy (reference as market_structure.py): 124 tests collected (collect_only.txt). Page line 253 says 124. page_smoke reports 'All 124 tests pass' in the in-browser grader (page_smoke_project_r5.out).")
row("E1d-r1-autograder-instances", "2.6-autograder", f"{PAGE} line 247; grader/instance.py lines 1-27", "PASS",
    "Re-verified. instance.py: b = randint(1,3), c = randint(5,60), gap = randint(60,400) (lines 23-25), labelled SIMULATED (line 3). Page line 247 states the same ranges. Gap >= 60 > 6b on every seed, as the docstring (lines 10-11) says.")
row("E1d-r1-autograder-messages", "2.6-autograder", "grader/test_project.py lines 50-54, 92-102, 114-131, 194-195, 214-222, 267-291; grader/reference.py lines 26-35", "PASS",
    "Re-verified. Failure messages name the property and never print the expected value (check() and must_raise()). Reference messages 'a must exceed b*c', 'b must be positive', 'c must be positive' and the structure message name the conditions the tests require.")
row("E1d-r1-autograder-browser", "2.6-autograder", f"{PAGE} lines 284, 291, 592; course/assets/js/grader.js line 53; course/assets/js/py-worker.js line 111; course/assets/js/python.js line 4", "PASS",
    "Re-verified. Browser flags (py-worker.js:111: -q -p no:cacheprovider --assert=plain -W error) match the page's local command (line 291). python.js line 4: TIMEOUT_MS = 120000, matching '120 seconds' (line 251). grader.js line 53 shows the seed from the workspace ID (line 33 via store.unitSeed), matching line 247. Footer 'nothing you write leaves it' (line 592): store.js header says nothing leaves the browser; I did not trace every network path.")
row("E1d-r1-mutants-existing", "2.6-mutants", "ledgers/E1/mutants/ (150 files at dde0486b); tools/mutate_graders.py --unit E1 --seeds 0-9", "PASS",
    "Re-run this round: mutate_graders E1 --seeds 0-9: PASS (150/150 killed; mutate_E1_0-9_r5.out). Killing tests are listed per mutant in the fragment.")
row("E1d-r1-mutants-new", "2.6-mutants", "ledgers/E1/mutants/e1d_r1_m01..m06*.py", "PASS", "Re-run: all six killed (see mutants list).")
row("E1d-r2-mutants-new", "2.6-mutants", "ledgers/E1/mutants/e1d_r2_m01..m05*.py", "PASS", "Re-run: all five killed (see mutants list).")
row("E1d-r3-mutants-new", "2.6-mutants", "ledgers/E1/mutants/e1d_r3_m01..m06*.py", "PASS", "Re-run: all six killed (see mutants list).")
row("E1d-r4-mutants-new", "2.6-mutants", "ledgers/E1/mutants/e1d_r4_m01..m04*.py (committed in 55d171e9, after edbb7aa8)", "PASS",
    "Re-run: all four killed (see mutants list). These files are in the round-5 delta, so they were re-verified rather than carried.")
row("E1d-r5-mutants-new", "2.6-mutants", "ledgers/E1/mutants/e1d_r5_m01..m04*.py (written by scripts/E1-d-r5/make_mutants_r5.py from reference.py, one line changed each)", "PASS",
    "Four new student-error mutants: monopoly fee without b in the denominator (killed by test_closed_form_matches[fee_cents-monopoly]); Bertrand volume gap/b (killed by test_closed_form_matches[volume_trades-bertrand]); consumer surplus as fee*Q/2 (killed by test_tie_rounds_up_for_each_output[bertrand-welfare_cents-8-1-1]); Cournot fee from (a-d)/b (killed by test_closed_form_matches[fee_cents-cournot]).")
row("E1d-r1-alternatives", "2.6-alternatives", "ledgers/E1/scripts/E1-d-r2/alternatives/*, E1-d-r3/alternatives/*, E1-d-r4/alternatives/*, E1-d-r4/alt_vx4_float_cutoff_order.py, E1-d-r5/alternatives/*", "PASS",
    "Re-run this round on seeds 0-49 (alternatives_all_seeds_0_49.out; vx4 run in a scratch copy). Correct implementations all PASS: alt_a..alt_g (r2), alt_r3_a/b/c, alt_r4_a/b/c, alt_r5_b/c/d/e. Rejected by design: alt_f (inexact control, expected) and the two float variants alt_r5_a and alt_vx4, which fail only the exact-large-input test (see E1d-r5-alternatives-new).")
row("E1d-r2-alternatives-new", "2.6-alternatives", "ledgers/E1/scripts/E1-d-r2/alternatives/alt_f_cournot_iteration_200.py; alternatives_all_seeds_0_49.out", "PASS",
    "Re-run on seeds 0-49. alt_f is the designed inexact control (Cournot by 200 floating-point iterations); it is rejected by test_tie_rounds_up_for_each_output[cournot-consumer_surplus_cents-31-4-1] on seed 0, which is the expected behaviour for an inexact method against the exact rule. Not an over-constraint.")
row("E1d-r3-alternatives", "2.6-alternatives", "ledgers/E1/scripts/E1-d-r3/alternatives/alt_r3_a/b/c*.py", "PASS", "Re-run on seeds 0-49: all three PASS (alternatives_all_seeds_0_49.out).")
row("E1d-r4-alternatives", "2.6-alternatives", "ledgers/E1/scripts/E1-d-r4/alternatives/alt_r4_a/b/c*.py", "PASS", "Re-run on seeds 0-49: all three PASS (alternatives_all_seeds_0_49.out). The round-4 float variant scripts/E1-d-r4/alt_vx4_float_cutoff_order.py was re-run this round: it fails only test_large_exact_inputs_round_from_exact_values (monopoly and cournot, all 50 seeds), the same class as alt_r5_a (see E1d-r5-alternatives-new).")
row("E1d-r5-alternatives-new", "2.6-alternatives", "ledgers/E1/scripts/E1-d-r5/alternatives/alt_r5_a..e*.py", "PASS",
    "Four new correct implementations PASS on seeds 0-49: alt_r5_b (Cournot best-response iteration to convergence, closed form as stop check), alt_r5_c (2x2 Cramer solve of the reaction system), alt_r5_d (integers only, half-up by (2p+q)//(2q)), alt_r5_e (Fraction vertex formulas). alt_r5_a (float arithmetic with floor(x+0.5)) fails only test_large_exact_inputs_round_from_exact_values (3 parametrisations, all seeds); with -k 'not large' it passes all 121 other tests on all 50 seeds. That test enforces the page's 'exact fraction' Constraint for whole-number inputs up to 1.5e16, which the page allows (no upper bound). So the float variant is not a conforming implementation, not an over-constraint. Plan section 6 item (5) should say 'exact arithmetic' instead of 'float'. Architect to rule.")
row("E1d-r1-rubric-structure", "2.6-rubric", f"{PAGE} lines 388-402 (rubric table)", "PASS",
    "Re-verified. Six criteria rows (C1-C6), each with four level cells (4 Exemplary, 3 Proficient, 2 Developing, 1 Beginning); the bar at level 3 is stated (line 386).")
row("E1d-r1-rubric-C6-observable", "2.6-rubric", f"{PAGE} line 399 (C6)", "PASS", "Re-verified. Level 3 requires, for each limit, what changes without it; level 2 needs only the names. Observable.")
row("E1d-r1-exemplar-annotations", "2.6-rubric", f"{PAGE} lines 407-555 (Exemplars A and B)", "PASS",
    "Re-verified. Official scores (A 1,2,2,2,1,2; B 4,4,4,4,3,2; data-scores lines 407, 472) agree with the annotations: each 'meets' and 'misses' line names the level it grades, and the rubric text (lines 393-399) supports each level. Exemplar B's numbers were recomputed: 67/53/100 trades and 70/53/20 cents as printed; 50/3, 100/3 and d/(6b) = 50/3; welfare +694 and +556; profit 2500 vs 2222 (diff 278, exact 277.8); DWL 1250 and 556; tie at a=121 gives 71 and 51.")
row("E1d-r4-exemplar-number-claim", "2.2-numbers", f"{PAGE} line 405 (exemplar intro) vs line 522 (Comparison)", "PASS",
    "Round-4 FAIL is fixed. Line 405 now says the printed integers are Lab 3's output and the exact fractions are closed forms, and that no lab prints 277.8. Checked: all 12 E1 twin outputs (rederive/labs) contain no '277', '2500/9', '50/3' or '100/3' (grep over /tmp/e1d_r5/*.out). Exemplar B's 50/3 and 100/3 are differences of Lab 1-derivable closed forms, not printed values, and the sentence does not claim they are printed.")
row("E1d-r1-data-simulated", "11-data", f"{PAGE} lines 53, 247; grader/instance.py line 3; tests/labs/E1/lab-E1-project-1.py docstring", "PASS",
    "Re-verified. Page: 'No data file is read, and the case is not market data' (line 53); instance SIMULATED (line 247). No file is read by any E1 project lab (run_labs passes with no data).")
row("E1d-r1-gates", "gates", "repository gates on pin dde0486b (slice-scoped, plus the repository-wide ones that are cheap)", "PASS",
    "Run this round: check_pages E1, check_dag E1, check_projects E1 PASS; run_labs E1 12/12; run_graders E1 0-49 50/50; mutate E1 0-9 150/150; ruff check and ruff format --check on tests/labs/E1 and grader: clean; mypy --no-incremental (repo strict): no issues in 385 files; relevant pytest modules (test_memo_exemplars, test_page_checks, test_run_labs, test_labs filtered): exit 0; page_smoke E1 --pages project: PASS; verify_refs --offline: 0 problems. Not run: full pytest suite, render_curriculum, build_site --check, fetch_data --check (architect's gates; outside slice d).")
row("E1d-r1-structure-order", "2.5-structure", f"{PAGE} section order (lines 40, 51, 191, 241, 264, 282, 288, 295, 370, 557, 564, 573, 581)", "PASS",
    "Re-verified. Sections in plan order: ladder, rungs (Labs 1-2), model (Definitions, Propositions), spec, hours, grader, local run, check (Lab 3), report (memo, rubric, exemplars, self-assessment), stretch, reading, references.")
row("E1d-r1-atlas-studio", "2.5-structure", f"{PAGE} (whole file); course/modules/E/E1/index.html", "PASS",
    "check_projects E1: PASS. Plan section 0 records that E1 has no atlas key and no STUDIO requirement; the project page carries neither.")
row("E1d-r1-docstring-units", "2.5-lab", f"{PAGE} lines 58-68 (Lab 1), 133-141 (Lab 2), 301-310 (Lab 3); the twins' docstrings", "PASS",
    "Re-verified. Lab 1 docstring: 'Consumer surplus is Q^2/(2b)', 'deadweight loss is (d - Q)^2/(2b)' match code and output. Lab 2: 'welfare is the gross value (a Q - Q^2/2)/b less the cost c Q', matches code. Lab 3: 'Every money value is rounded once', matches closed_form_outcome.")
row("E1d-r3-lab3-placement", "2.5-structure", f"{PAGE} lines 51-189 (rungs) and 295-368 (check)", "PASS",
    "Re-verified. Labs 1-2 only in the skippable rungs section; Lab 3 in section#check; ladder line 46 points there. Round-3 FAIL is fixed.")
row("E1d-r3-run-report", "2.5-lab", f"{PAGE} lines 249, 300, 303-305", "PASS",
    "Re-verified. run_report.py is described as Lab 3 with closed_form_outcome replaced by outcome; the lab's code defines closed_form_outcome (line 332) and its docstring says the same (lines 303-306).")
row("E1d-r3-starter-signature", "2.6-autograder", f"course/modules/E/E1/grader/starter.py line 16; {PAGE} line 249", "PASS",
    "Re-verified. Starter signature outcome(structure: str, a: int, b: int, c: int) -> dict[str, int] matches the page line 249 signature exactly.")
row("E1d-r3-numbers-prose", "2.2-numbers", f"{PAGE} lines 57, 127, 132, 186, 300, 366, 217-237", "PASS",
    "Re-verified against UNROUNDED values and printed digits: 200/3=66.67->67, 160/3=53.33->53, 20000/9=2222.2->2222, 40000/9=4444.4->4444, 5000/9=555.6->556, 10201/4=2550.25->2550. Proof numbers (d^2/(4b), 2d^2/(9b), d^2/(36b), 5d^2/(72b)) recomputed in rederive_r5.py. The line 127 defect is a claim, not a number (row E1d-r1-lab1-prose).")
row("E1d-r3-scope-words", "2.4-scope", f"{PAGE} lines 37, 57, 213, 249, 251, 259, 366, 372, 385-386", "PASS",
    "Re-verified: 'Every money output is in whole cents' (37) and 'every money value' (57) hold for the reference (reference.py lines 56-66: each money key is half_up of an exact value). 'Each proposition lists the assumptions its proof uses' (213): proofs use only hypotheses listed (checked each proof). 'No output is computed from another output's rounded value' (251) holds for the reference (exact values in reference.py). 'Every integer in the table' (366) holds.")
row("E1d-r3-terms-before-definition", "2.4-defs", f"{PAGE} lines 37, 53, 57, 133-140, 191-209", "PASS",
    "Re-verified. Terms in the lede and rungs (fee, volume, gap d) are defined in Definitions (lines 195-208) or the spec; Lab 2's 'reaction' and 'iterate' are defined in the lab docstring and Definitions (line 203). No undefined term found.")
row("E1d-r5-calibration-exemplars", "2.6-rubric-calibration", "~/.fanout/blind/E1-d.json (A, B score vectors) vs project.html lines 407, 472", "PASS",
    "Calibration per the round-5 instruction. Blind A [1,1,2,2,2,2] vs official [1,2,2,2,1,2]: C2 and C5 differ by one level, within one level, accepted. Blind B [4,4,4,4,3,2] equals official B [4,4,4,4,3,2]. Both within one level on every criterion, as the instruction allows.")

verdict = "FAIL" if any(r["status"] != "PASS" for r in R) else "PASS"
fragment = {
    "unit": "E1",
    "slice": "d",
    "round": 5,
    "verifier": "verifyS5-E1-d (Haiku 5.5)",
    "pin": "dde0486beeb0312e4ac1cc03aaa02e56644adb24",
    "base": "aeb512b65b7774b59b84f836a13984fcfe9d0d1f",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyS5-E1-d",
    "scratch": "/tmp/e1d_r5",
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "verdict": verdict,
    "rows": R,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [
        "course/modules/E/E1/cards.json changed in the E1 delta since edbb7aa8 (68 lines); cards are outside slice d and were not verified here",
    ],
    "notes": (
        "Delta since previous pin edbb7aa8 (round 4). Changed in slice d: project.html (12 lines: lede, rungs text, Lab 1 step-5 comment, memo and exemplar prose, exemplar A/B text), tests/labs/E1/lab-E1-project-1.py (one comment), tests/labs/E1/lab-E1-L04-1.py (docstring rename S->delta; output unchanged). Unchanged in slice d: grader/* (reference, instance, starter, test_project), lab-E1-project-2/3, all alternatives from r2-r4, the round-1 to round-3 mutants. Every row was re-verified from this pin; none was carried forward. "
        "Outside slice d but read because they changed and are cross-referenced by the project: L02 interpretation (line 246 changed), L04 why-it-matters and twin (Definitions 1.1/2.1 and 5.1 exist), L06 proof note and Proposition 4.1 explain (20000/9 rounds to 2222), L07 R1 solution (other root Q = d(1+sqrt2/4); in [0,a] iff d <= 2sqrt2 bc: 0 mismatches in 20,000 random (a,b,c)), index.html hub eyebrow (arithmetic consistent). Their Lab/Lesson verdicts belong to the lesson slices. "
        "Could not check: cards.json (147 cards; slice owned elsewhere); the full pytest suite and the repository-wide render_curriculum/build_site/fetch_data gates; live verify_refs (offline only); a live Chrome UI pass (page_smoke's in-browser grader ran); the Your-code-is-saved-as-you-type claim beyond the store and grader code paths. "
        "Summary of the one FAIL: project.html line 127 says the closed forms are equilibria, proved by Propositions 2 and 3; the monopoly closed form is an optimum (Proposition 1), not an equilibrium. Low severity, wording only; the printed output is correct."
    ),
    "summary": (
        f"Slice d round 5 at dde0486b: verdict {verdict}. {len(R)} rows: "
        f"{sum(1 for r in R if r['status'] == 'PASS')} PASS, {sum(1 for r in R if r['status'] != 'PASS')} FAIL. "
        f"One FAIL: E1d-r1-lab1-prose (project.html line 127, low). The round-4 exemplar number FAIL is fixed. "
        f"Grader: 124 tests collected, reference 50/50 seeds, 150/150 mutants killed (4 new, all killed). "
        f"Alternatives: all r3-r5 correct implementations PASS seeds 0-49 except the float variant alt_r5_a, which fails only the exact-large-input test (rule-consistent, see row E1d-r5-alternatives-new); alt_f is the designed inexact control and is rejected. "
        f"Props 1-5 re-derived over 19,440 cases; labs run 12/12; twins equal the page code; calibration within one level."
    ),
}

problems = ledger.validate(fragment, "E1-d")
print("validate:", problems)
out_path = CHK / "ledgers/E1/E1-d.json"
out_path.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out_path, "rows", len(R), "mutants", len(mutants), "verdict", verdict)
