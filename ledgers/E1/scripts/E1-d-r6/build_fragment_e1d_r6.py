"""Build the round-6 E1 slice-d fragment (ledgers/E1/E1-d.json) from the round-6 command outputs and the mutant gate output."""

import json
import re
import sys
from pathlib import Path

CHK = Path(sys.argv[1]).resolve()
S = "ledgers/E1/scripts/E1-d-r6"
O = f"{S}/out"
P = "course/modules/E/E1/project.html"
PIN = "e896b7a45344d1bc17ebfbf7fb05d87698ec9d6a"
BASE = "dde0486beeb0312e4ac1cc03aaa02e56644adb24"

R = []


def row(rid, check, location, status, evidence):
    R.append({"id": rid, "check": check, "location": location, "status": status, "evidence": evidence})


row("E1d-r1-ladder", "2.6-spec", f"{P} lines 40-49 (ladder), 51-189 (rungs: Labs 1-2 only), 295-368 (check: Lab 3), 564 (stretch)", "PASS",
    "Re-read lines 40-49, 51-189, 295-368, 564 in round 6. Rung 1 and 2 are the labs of section#rungs; Lab 3 sits in section#check (line 295). The skip rule links index.html#placement; a script checked all 16 internal anchors of project.html against the ids of project.html and index.html (0 broken).")
row("E1d-r1-spec-precedence", "2.6-spec", f"{P} line 251; grader/test_project.py lines 251-291", "PASS",
    "Re-read in round 6. Each table case violates only the condition it names: (20,2,10), (19,2,10), (-3,1,1) only a<=bc; (10,0,5), (10,-1,5) only b; (10,2,0), (10,2,-1) only c; test_project.py lines 277-291 match. Reference passes seeds 0-49 (run_graders_0_49.out: 50/50).")
row("E1d-r1-spec-tests-align", "2.6-spec", f"{P} lines 251-253; grader/test_project.py lines 92-102, 214-222, 267-291", "PASS",
    "Re-read in round 6. The exception table (ValueError for structure, a<=bc, b<=0, c<=0) matches the must_raise calls; no other exception type is demanded. Message phrases in must_raise match the reference messages.")
row("E1d-r1-hours", "2.9-hours", f"{P} lines 33, 270-276; course/modules/E/E1/index.html lines 38-40", "PASS",
    "Component hours 2+3+8+8+6+3 = 30 (page 270-276); data-hours-project=30 (line 33); hub eyebrow '90 h lessons · 30 h project (25% of the 120 h)' (index.html line 40): 90+30=120, 30/120=25%. Arithmetic consistent.")
row("E1d-r1-lab1-run", "2.5-lab", f"{P} lines 55-128; tests/labs/E1/lab-E1-project-1.py", "PASS",
    f"run_labs E1: PASS (12/12) ({O}/run_labs_E1.out). {S}/twin_page_r6.py (python -I): 'lab-E1-project-1: page code == twin: True (61 lines)'; twin under python -I -W error exits 0 and its stdout equals the expected block (twin_page_r6.out).")
row("E1d-r1-lab2-completion", "2.5-lab", f"{P} lines 130-187 (blanks at lines 160, 165); tests/labs/E1/lab-E1-project-2.py", "PASS",
    "Re-run in round 6: twin_page_r6.out shows the page code differs from the twin only at the two blank lines (twin 'return (d - rival) / 2' vs page '___'; twin welfare line vs page '___'), as the completion rule allows. Twin exits 0 under -I -W error and its output equals the expected block. Completed welfare line: half_up((a*Q - Q*Q/2)/b - c*Q) = 4444.")
row("E1d-r1-lab3-run", "2.5-lab", f"{P} lines 298-367; tests/labs/E1/lab-E1-project-3.py", "PASS",
    "twin_page_r6.out: 'lab-E1-project-3: page code == twin: True (57 lines)'; twin exit 0 under -I -W error; output equals expected block. Printed values re-derived by rederive_r6.py (out/rederive_r6.out): a=120 rows 50/70/2500/1250/3750/1250, 67/53/2222/2222/4444/556, 100/20/0/5000/5000/0; a=121 rows 51/71/2550/1275/3825/1275, 67/54/2267/2267/4534/567, 101/20/0/5101/5101/0.")
row("E1d-r1-lab1-prose", "2.5-lab", f"{P} lines 57 (hypothesis), 127 (interpretation)", "PASS",
    "Round-5 FAIL is fixed. Line 127 now reads: 'It does not check optimality or equilibrium: Proposition 1 proves that the monopoly volume maximises profit, and Propositions 2 and 3 prove that the Cournot and Bertrand profiles are equilibria (the term is defined under Definitions).' Checks: (1) Proposition 1 (line 216) proves Q*=d/2 is the unique maximiser of the profit on Q>=0; (2) Proposition 2 (line 222) proves the unique equilibrium q1=q2=d/3 and Proposition 3 (line 226-227) proves (c,c) is the unique equilibrium; (3) 'equilibrium' is defined in Definitions ('Equilibrium, in words', line 205, #model-definitions exists at line 195); (4) lab-E1-project-1 code (lines 58-118) computes only the closed forms and prints values; it has no optimality or equilibrium test; (5) the printed numbers in line 127 match the expected block (lines 120-126). Math spans of the page are identical to dde0486b (355 vs 355, same list), so no symbol changed.")
row("E1d-r1-lab2-prose", "2.5-lab", f"{P} lines 132, 138-139, 186", "PASS",
    "Re-derived: iteration error after 60 steps is |e_60| = d/(3*2^60) = 100/(3*2^60) ~ 2.9e-17 < 1e-12 (matches the printed True); the error formula e_k = (-1/2)^k (-d/3) follows from e_{k+1} = -e_k/2 (Proposition 2, line 221). 40000/9 = 4444.44 -> 4444; 160/3 = 53.33 -> 53. 'Proposition 2' cited for (d-q_j)/2 exists (line 221).")
row("E1d-r1-lab3-prose", "2.5-lab", f"{P} lines 300, 366", "PASS",
    "Re-derived with exact Fractions (out/rederive_r6.out): a=120 monopoly welfare 3750 and Cournot welfare 4444; a=121 monopoly profit 10201/4 = 2550.25, printed 2550; 200/3 and 202/3 both lie in (66.5, 67.5), so Cournot volume prints 67 in both cases (line 366).")
for k, (prop, lines, hint) in enumerate([
    ("1", "215-218", "pi(Q)=-Q^2/b+(d/b)Q; pi'=(d-2Q)/b; pi'' = -2/b < 0; unique maximiser d/2; fee (a+bc)/(2b); profit d^2/(4b)"),
    ("2", "220-223", "reaction max(0,(d-q_j)/2); the case analysis excludes a zero quantity (q1=0 gives q2=d/2 and q1=d/4>0); symmetric point d/3; error d/(3*2^k)"),
    ("3", "225-228", "(c,c) equilibrium; each deviation (f1<c; f1>c with f2>f1; f1=f2>c; f1=c<f2) is profitable as the proof states"),
    ("4", "230-233", "CS = integral of (Q-t)/b = Q^2/(2b); W'(x)=(d-x)/b; W(d)-W(Q)=(d-Q)^2/(2b)"),
    ("5", "235-238", "exact identities d/(6b), 5d^2/(72b), d^2/(36b); printed-order claim for d>6b (rederive_r6.out: sweep 19440 cases, failures 0)"),
], start=1):
    row(f"E1d-r1-prop{prop}", "2.6-proof", f"{P} lines {lines} (Proposition {prop})", "PASS",
        f"Re-read the statement and proof in round 6 ({hint}). Numeric re-derivation: {S}/rederive_r6.py, out/rederive_r6.out: 'sweep cases 19440, failures 0'; identities d^2/(36b)=2500/9, 5d^2/(72b)=6250/9, d/(6b)=50/3 at the reference case.")
row("E1d-r1-conventions", "2.6-spec", f"{P} lines 258-260 (Conventions)", "PASS",
    "Re-read in round 6. Monopoly volume d/2 and fee (a+bc)/(2b), Cournot 2d/3 and (a+2bc)/(3b), Bertrand d and c match Propositions 1-3; Proposition 4 gives CS, welfare, DWL; Cournot profit as the total of the two exchanges matches (f-c)Q with Q=2d/3 (20000/9 at the reference case, Lab 1 line 123).")
row("E1d-r1-notation", "13-notation", f"{P} math spans (355); notation/notation.json", "PASS",
    "Math spans of project.html are identical to dde0486b (script: 355 spans before and after, identical list, including those on the changed line 127). Registered symbols T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q} do not occur in the page's math (round-5 grep; unchanged). The round-5 finding was a claim, not a symbol.")
row("E1d-r1-dag", "2.9-dag", f"{P} (no data-concept links); check_dag", "PASS",
    f"check_dag E1: PASS (round 6, {O}/check_dag.out). project.html has no data-concept links; the cross-reference is to Lessons 5 to 7 inside E1.")
row("E1d-r1-process-words", "2.9-prose", f"{P} (whole file)", "PASS",
    "Whole-file grep in round 6 for banned phrases (TODO, TBD, lorem, ellipsis, for brevity, details omitted, beyond the scope, you can add more, left as an exercise, it is important to note, studies show, experts agree, it is well known, obviously, clearly, roughly, historically) and process words (verifier, builder, ledger, fragment, agent, round N, pin, fixer, slice, blind): no learner-text hit except line 450, a deliberately weak exemplar sentence ('about 1250 cents') that the exemplar's own annotation at line 455 names as the C3 miss; it is not a builder claim (see notes).")
row("E1d-r1-citation", "2.1-citation", f"{P} lines 573-579 (Reading); references/references.json key varian2014intermediate", "PASS",
    f"verify_refs.py --offline (round 6, {O}/verify_refs_offline_r6.out): 'offline integrity: 560 entries, 0 problems', exit 0. references/references.json contains varian2014intermediate (1 hit). The Reading section states no passage locator is confirmed and attributes no statement. Live run not made (see could-not-check).")
row("E1d-r1-autograder-reference", "2.6-autograder", "course/modules/E/E1/grader/reference.py; tools/run_graders.py", "PASS",
    f"run_graders E1 --seeds 0-49: 'run_graders E1: PASS (reference 50/50 seeds, slowest 0.2 s)', exit 0 ({O}/run_graders_0_49.out). grader/* unchanged since dde0486b (git diff --quiet).")
row("E1d-r1-autograder-count", "2.6-autograder", f"{P} line 253; grader/test_project.py", "PASS",
    f"pytest --collect-only -q on a scratch copy (reference as market_structure.py): '124 tests collected' ({O}/pytest_collect_r6.out). Page line 253 says 124; page_smoke in-browser grader: 'All 124 tests pass on seed 1503370415' ({O}/page_smoke_project_r6.out).")
row("E1d-r1-autograder-instances", "2.6-autograder", f"{P} line 247; grader/instance.py", "PASS",
    "Script over seeds 0-19 (round 6): every instance satisfies a > b*c > 0, b in 1..3, c in 5..60, gap d in 60..400 and d > 6b; 20 of 20 (a,b,c) triples are distinct, so the answers change across seeds. Page line 247 states the same ranges.")
row("E1d-r1-autograder-messages", "2.6-autograder", "grader/test_project.py lines 50-54, 92-102, 114-131, 194-195, 214-222, 267-291; grader/reference.py lines 26-35", "PASS",
    "Re-read in round 6. check() and must_raise() messages name the property and never print the expected value; the phrases the tests require ('a must exceed b*c', 'b must be positive', 'c must be positive', the three structure names) appear in reference.check_inputs.")
row("E1d-r1-autograder-browser", "2.6-autograder", f"{P} lines 284, 291, 592; course/assets/js/grader.js line 53; py-worker.js line 111; python.js line 4", "PASS",
    "page_smoke --pages project (round 6): in-browser grader 'All 124 tests pass'; page_smoke E1: PASS. Flags in py-worker.js:111 (-q -p no:cacheprovider --assert=plain -W error) match line 291. python.js:4 TIMEOUT_MS = 120000 matches '120 seconds' (line 251). course/assets/js and css are byte-identical to dde0486b (git diff --quiet).")
row("E1d-r1-mutants-existing", "2.6-mutants", "ledgers/E1/mutants/ (154 files); tools/mutate_graders.py --unit E1 --seeds 0-9", "PASS",
    f"mutate_graders E1 --seeds 0-9 (round 6): 'mutate_graders E1: PASS (154/154 killed)', exit 0 ({O}/mutate_E1_0-9_r6.out, one KILLED line per file with the killing test and seed).")
row("E1d-r1-mutants-new", "2.6-mutants", "ledgers/E1/mutants/e1d_r1_m01..m06*.py", "PASS",
    "Re-run in the 154/154 gate above: each e1d_r1_* mutant KILLED.")
row("E1d-r2-mutants-new", "2.6-mutants", "ledgers/E1/mutants/e1d_r2_m01..m05*.py", "PASS",
    "Re-run in the 154/154 gate above: each e1d_r2_* mutant KILLED.")
row("E1d-r3-mutants-new", "2.6-mutants", "ledgers/E1/mutants/e1d_r3_m01..m06*.py", "PASS",
    "Re-run in the 154/154 gate above: each e1d_r3_* mutant KILLED.")
row("E1d-r4-mutants-new", "2.6-mutants", "ledgers/E1/mutants/e1d_r4_m01..m04*.py", "PASS",
    "Re-run in the 154/154 gate above: each e1d_r4_* mutant KILLED.")
row("E1d-r5-mutants-new", "2.6-mutants", "ledgers/E1/mutants/e1d_r5_m01..m04*.py (one line changed from reference.py, scripts/E1-d-r5/make_mutants_r5.py)", "PASS",
    "Re-run in the 154/154 gate above: e1d_r5_m01 (fee denominator), m02 (Bertrand volume gap/b), m03 (consumer surplus as fee*Q/2), m04 (Cournot fee from Bertrand formula) all KILLED.")
row("E1d-r6-mutants-new", "2.6-mutants", "ledgers/E1/mutants/e1d_r6_m01..m04*.py (generated by scripts/E1-d-r6/make_mutants_r6.py from reference.py, one line changed each)", "PASS",
    "Four new student-error mutants written this round, each a complete module whose first docstring line names the error: m01 consumer surplus Q^2/b without the half (killed by test_tie_rounds_up_for_each_output[bertrand-consumer_surplus_cents-8-1-1], seed 0); m02 Cournot profit as one exchange's share (killed by test_closed_form_matches[profit_cents-cournot], seed 0); m03 structure check as a substring test (killed by test_unknown_structure_raises_value_error[], seed 0); m04 Bertrand fee a/b (killed by test_closed_form_matches[fee_cents-bertrand], seed 0). All four KILLED in the 154/154 run.")
row("E1d-r1-alternatives", "2.6-alternatives", "ledgers/E1/scripts/E1-d-r2/alternatives/*, E1-d-r3/alternatives/*, E1-d-r4/alternatives/*, E1-d-r5/alternatives/*", "PASS",
    f"Re-run on seeds 0-49 (round 6, {O}/alternatives_all_seeds_0_49_r6.out, script {S}/run_alts_r6.py): PASS for alt_a..alt_e, alt_g (r2), alt_r3_a/b/c, alt_r4_a/b/c, alt_r5_b/c/d/e. Five or more correct alternatives of different styles pass seeds 0-49 (linear solve, Simpson, decimal, integer cutoff, validation reordering, Cramer, integer-scaled, Fraction vertex, best-response iteration).")
row("E1d-r2-alternatives-new", "2.6-alternatives", "ledgers/E1/scripts/E1-d-r2/alternatives/alt_f_cournot_iteration_200.py", "PASS",
    "Re-run on seeds 0-49: FAIL on test_tie_rounds_up_for_each_output[cournot-consumer_surplus_cents-31-4-1] (seed 0). alt_f is a float-based Cournot iteration, the designed inexact control; it is wrong on the page's exact rule, so it is a rejected method, not an over-constraint (ruling 10).")
row("E1d-r3-alternatives", "2.6-alternatives", "ledgers/E1/scripts/E1-d-r3/alternatives/alt_r3_a/b/c*.py", "PASS",
    f"Re-run on seeds 0-49: all three PASS ({O}/alternatives_all_seeds_0_49_r6.out).")
row("E1d-r4-alternatives", "2.6-alternatives", "ledgers/E1/scripts/E1-d-r4/alternatives/alt_r4_a/b/c*.py", "PASS",
    f"Re-run on seeds 0-49: all three PASS ({O}/alternatives_all_seeds_0_49_r6.out).")
row("E1d-r5-alternatives-new", "2.6-alternatives", "ledgers/E1/scripts/E1-d-r5/alternatives/alt_r5_a..e*.py", "PASS",
    "Re-run on seeds 0-49: alt_r5_b, c, d, e PASS. alt_r5_a (float arithmetic with floor(x+0.5)) FAILS test_large_exact_inputs_round_from_exact_values[monopoly] on seed 0 (and on the other seeds). Page Constraints (line 251): 'Each money output is an exact fraction'. Under architect ruling 10 a float-based alternative that is wrong on a stated exact rule is a mutant, not an alternative, so this is not an over-constraint and the five correct alternatives above stand.")
row("E1d-r1-rubric-structure", "2.6-rubric", f"{P} lines 388-402 (rubric table)", "PASS",
    "Re-read in round 6: six criteria rows C1-C6, each with four level cells (4 Exemplary, 3 Proficient, 2 Developing, 1 Beginning); the bar at level 3 is stated (line 386 and caption line 391).")
row("E1d-r1-rubric-C6-observable", "2.6-rubric", f"{P} line 399 (C6)", "PASS",
    "Re-read: level 3 requires, for each limit, what changes without it; level 2 needs only the names. Each level is observable in the memo text.")
row("E1d-r1-exemplar-annotations", "2.6-rubric", f"{P} lines 407-555 (Exemplars A and B)", "PASS",
    "Re-read in round 6 (lines 407-555 byte-identical to dde0486b). Official scores A 1,2,2,2,1,2 and B 4,4,4,4,3,2 (data-scores lines 407, 472) agree with the annotations. Exemplar B's numbers re-computed: 67/53/100 trades and 70/53/20 cents as printed; 50/3, 100/3 and d/(6b)=50/3; welfare +694 and +556; profit 2500 vs 2222 (diff 278, exact 277.8 = d^2/(36b)); DWL 1250 and 5000/9 -> 556.")
row("E1d-r4-exemplar-number-claim", "2.6-rubric", f"{P} line 405 (exemplar intro) vs line 522 (Comparison)", "PASS",
    "Line 405 states the printed integers are Lab 3's output and the exact fractions are closed forms, and that no lab prints 277.8. grep over tests/labs/E1/*.py and course/modules/E/E1/*.html finds no lab output containing '277' (only the exemplar text quotes 277.8). 2500/9 and 50/3 are not printed by any lab.")
row("E1d-r1-data-simulated", "2.8-data", f"{P} lines 53, 247; grader/instance.py line 3", "PASS",
    "Page line 53: 'No data file is read, and the case is not market data'; line 247: instance 'is SIMULATED'; instance.py docstring: 'It returns a SIMULATED case'. No E1 project lab reads a file (run_labs passes with no data).")
row("E1d-r1-gates", "gate", "repository gates on pin e896b7a4 (slice-scoped, plus the cheap repository-wide ones)", "PASS",
    f"check_pages E1 PASS; check_dag E1 PASS; check_projects E1 PASS; run_labs E1 12/12; run_graders E1 0-49 50/50; mutate_graders E1 0-9 154/154; page_smoke E1 --pages project PASS; verify_refs --offline 560 entries 0 problems; ruff check . PASS; ruff format --check . 554 files formatted; mypy --no-incremental: 'Success: no issues found in 385 source files'; pytest tests/test_memo_exemplars.py tests/test_page_checks.py tests/test_labs.py tests/test_run_labs.py exit 0 (out/pytest_relevant_r6.out). Outputs in {O}/.")
row("E1d-r1-structure-order", "2.9-structure", f"{P} section order (lines 40, 51, 191, 241, 264, 282, 288, 295, 370, 557, 564, 573, 581)", "PASS",
    "Re-read in round 6: ladder, rungs (Labs 1-2), model (Definitions, Propositions), spec, hours, grader, local run, check (Lab 3), report (memo, rubric, exemplars, self-assessment), stretch, reading, references. Matches the plan order.")
row("E1d-r1-atlas-studio", "2.6-atlas", f"{P} (whole file); course/modules/E/E1/index.html", "PASS",
    "grep -i atlas over project.html: no hits; check_projects E1 PASS. E1 has no atlas key and no STUDIO requirement (plan section 0).")
row("E1d-r1-docstring-units", "2.5-lab", f"{P} lines 58-68 (Lab 1), 133-141 (Lab 2), 301-310 (Lab 3); the twins' docstrings", "PASS",
    "Re-read in round 6. Lab 1 docstring: 'Consumer surplus is Q^2/(2b)', 'deadweight loss is (d - Q)^2/(2b)' match code lines 103-107 and output. Lab 2: 'welfare is the gross value (a Q - Q^2/2)/b less the cost c Q' matches welfare_cents. Lab 3: 'Every money value is rounded once from its exact value' matches closed_form_outcome.")
row("E1d-r3-lab3-placement", "2.9-structure", f"{P} lines 51-189 (rungs) and 295-368 (check)", "PASS",
    "Re-read in round 6: Labs 1-2 only in the skippable rungs section; Lab 3 in section#check (line 295); ladder line 46 points there.")
row("E1d-r3-run-report", "2.6-spec", f"{P} lines 249, 300, 303-305; lab-E1-project-3 code", "PASS",
    "Re-read: run_report.py is described as Lab 3 with closed_form_outcome replaced by outcome; the lab defines closed_form_outcome (line 332) and its docstring says the same (lines 303-306).")
row("E1d-r3-starter-signature", "2.6-spec", f"course/modules/E/E1/grader/starter.py; {P} line 249", "PASS",
    "starter.py defines outcome(structure: str, a: int, b: int, c: int) -> dict[str, int]; page line 249 states the same signature. On the unimplemented starter, pytest gives '121 failed, 3 passed' (NotImplementedError from outcome), as expected for a starter (pytest_starter_seed0_r6.out).")
row("E1d-r3-numbers-prose", "2.2-numbers", f"{P} lines 57, 127, 132, 186, 217-237, 300, 366", "PASS",
    "Re-verified against UNROUNDED values and printed digits: 200/3=66.67->67, 160/3=53.33->53, 20000/9=2222.2->2222, 40000/9=4444.4->4444, 5000/9=555.6->556, 10201/4=2550.25->2550. Proof numbers d^2/(4b), 2d^2/(9b), d^2/(36b), 5d^2/(72b) recomputed in rederive_r6.py. Line 127 is a claim, not a number, and its numbers are unchanged.")
row("E1d-r3-scope-words", "2.6-prose", f"{P} lines 37, 57, 213, 249, 251, 259, 366, 372, 385-386 and the new line 127", "PASS",
    "Re-verified in round 6 by a whole-file grep of scope words. 'Every money output is in whole cents' (37) and 'every money value' (57) hold for reference.py (each money key is half_up of an exact value). The new line 127 contains no scope word. 'No output is computed from another output's rounded value' (251) holds for reference.py (lines 56-66 use exact values).")
row("E1d-r3-terms-before-definition", "2.6-prose", f"{P} lines 37, 53, 57, 127, 133-140, 191-209", "PASS",
    "Re-read in round 6. Line 127 uses 'equilibria' and 'optimality' before the Definitions section; 'equilibrium' is flagged as defined under Definitions (its definition is line 205), and the Propositions are introduced in line 53 with a pointer to the model section. 'optimality' is an ordinary word, not a defined term. Lab 2's 'reaction' and 'iterate' are defined in the lab docstring and Definitions (line 203).")
row("E1d-r5-calibration-exemplars", "2.6-rubric-calibration", "~/.fanout/blind/E1-d.json (A, B vectors) vs project.html data-scores lines 407, 472", "PASS",
    "Calibration by the dedicated scorer's file (architect ruling 23). Blind A [1,1,2,2,2,2] vs official A [1,2,2,2,1,2]: C2 and C5 differ by one level, within one level. Blind B [4,4,4,4,3,2] equals official B [4,4,4,4,3,2]. Every criterion within one level. Note: this verifier had read the annotations before this round, so it did not score the exemplars itself.")

# mutants from the mutate gate output
mutants = []
for line in (CHK / O / "mutate_E1_0-9_r6.out").read_text(encoding="utf-8").splitlines():
    if not line.startswith("KILLED "):
        continue
    head, _, rest = line[len("KILLED "):].partition(": ")
    desc, _, killed = rest.rpartition(" -> ")
    mutants.append({"id": head[:-3] if head.endswith(".py") else head, "file": f"ledgers/E1/mutants/{head}",
                    "description": desc, "killed_by": killed})

notes = (
    "Round 6 (delta round, architect ruling 30) on pin e896b7a4. Base: round-5 pin dde0486b (fragment S-E1-d.round5.json). "
    "Delta in slice d: one line changed, course/modules/E/E1/project.html line 127 (Lab 1 interpretation: the sentence about "
    "equilibrium is replaced by a statement that Propositions 1 to 3 prove optimality and equilibrium). Changed in the same delta "
    "and outside slice d: cards.json, lessons, FC1, FC2 and M7 files, which are not verified here. "
    "Grader files, the Lab 1-3 twins, the references, notation, curriculum, tools and browser assets are byte-identical to dde0486b (git diff --quiet). "
    "Every row was re-verified from this pin with commands or a re-read; none was carried forward. "
    "The round-5 FAIL (E1d-r1-lab1-prose) is fixed and passes. "
    "Mutants: 154 files in ledgers/E1/mutants (150 earlier plus four new e1d_r6_m01..m04), all KILLED on seed 0 at mutate_graders E1 --seeds 0-9. "
    "Alternatives: 5+ correct alternatives pass seeds 0-49 (alt_r5_b, c, d, e and the earlier ones). "
    "Observation (LOW, not a row FAIL): ruling 10 classes the float-based alternatives alt_f (r2), alt_r5_a (r5) and alt_vx4 (r4) as mutants, not alternatives; they are rejected by the exact-rule tests and are kept in scripts/ directories, unchanged. "
    "Observation (LOW, not a row FAIL): exemplar A (line 450) quotes 'about 1250 cents', a deliberately weak sentence that its own annotation (line 455) names as the C3 miss; it is not a builder claim. "
    "Calibration: this verifier had read the exemplar annotations before this round, so it relied on the dedicated scorer's file (ruling 23). "
    "Could not check: the live verify_refs run (offline only); the full pytest suite and the repository-wide render_curriculum, build_site and fetch_data gates; the whole-page browser UI in a live Chrome session (page_smoke's Pyodide grader ran); cards.json (slice owned elsewhere); the claim 'Your code is saved in this browser as you type' beyond the store code paths."
)

fragment = {
    "unit": "E1",
    "slice": "d",
    "round": 6,
    "verifier": "verifyS6-E1-d (Haiku 5.5)",
    "pin": PIN,
    "base": BASE,
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyS6-E1-d",
    "scratch": "/tmp/e1d_r6",
    "verified_at": "2026-11-09T11:50:00+00:00",
    "verdict": "PASS" if all(r["status"] == "PASS" for r in R) else "FAIL",
    "rows": R,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": notes,
    "summary": (
        f"E1 slice d round 6 (delta from dde0486b to e896b7a4): verdict {'PASS' if all(r['status']=='PASS' for r in R) else 'FAIL'}. "
        f"{len(R)} rows, {sum(1 for r in R if r['status']=='PASS')} PASS, 0 non-PASS. Mutants: {sum(1 for m in mutants if m['killed_by'])}/{len(mutants)} killed. "
        "The round-5 FAIL (line 127 claim) is fixed; four new student-error mutants added and all killed."
    ),
}

out = CHK / "ledgers/E1/E1-d.json"
out.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out, "rows", len(R), "mutants", len(mutants), "verdict", fragment["verdict"])
