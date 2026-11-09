"""Build the E1-d round-4 ledger fragment from this round's command outputs (verifier checkout, pin edbb7aa8)."""

import json
import re
import sys
from pathlib import Path

CHK = Path(sys.argv[1]).resolve()
S = CHK / "ledgers/E1/scripts/E1-d-r4"
P = "course/modules/E/E1/project.html"

rows = [
    ("E1d-r1-ladder", "2.6-spec", f"{P} lines 40-49 (ladder), 51-189 (rungs), 191 (model), 241 (spec), 295-368 (check), 564 (stretch)", "PASS",
     "Line 42: skip rungs 1 and 2 for placement. The rungs section (line 51) closes at line 189 and holds only Labs 1 and 2. Lab 3 (line 298) now sits in section id=check (line 295), outside the skippable part. Lines 46 and 297 point to it. check_projects.out: 'check_projects E1: PASS'."),
    ("E1d-r1-spec-precedence", "2.6-spec", f"{P} line 251; grader/test_project.py lines 251-291", "PASS",
     "Line 251: 'When more than one of these conditions holds, a ValueError whose message names any one of them is accepted.' Each table case in test_project.py violates only the condition it names: (20,2,10), (19,2,10), (-3,1,1) only a<=bc; (10,0,5), (10,-1,5) only b; (10,2,0), (10,2,-1) only c. Reference passes 124/124 on seeds 0-9 (ref_seeds_0_9.out)."),
    ("E1d-r1-spec-tests-align", "2.6-spec", f"{P} lines 251-253; grader/test_project.py", "PASS",
     "Each stated check maps to a test: exact keys (line 111), int types (118), closed forms (125-131), orderings (134-184), exact cent ties (198-222), half-cent values (333-350), large exact inputs (323-330), standard-library rule (353-364), purity (235-240, 367-381), smallest b and c (294-319), second instance (390-398), ValueError table (251-291). collect_only.out: 124 tests collected."),
    ("E1d-r1-hours", "2.9-hours", f"{P} lines 33, 35, 270-276; course/modules/E/E1/index.html lines 29, 31", "PASS",
     "Table rows 2+3+8+8+6+3 = 30 (lines 270-276). data-hours-project=30 (line 33), eyebrow '30 hours' (line 35). index.html line 29 data-hours-lessons=90, data-hours-project=30; line 31 '120 hours'. 90+30=120 and line 276 '30 of the module's 120' agree."),
    ("E1d-r1-lab1-run", "2.5-lab", f"{P} lines 55-128; tests/labs/E1/lab-E1-project-1.py", "PASS",
     "run_labs_project.out: 'run_labs E1: PASS (3/3)', exit 0 (run_labs.py --unit E1 --page project). Twin under python -I -W error with expected block match is checked by the same tool. Expected block lines 119-126 equal the twin output."),
    ("E1d-r1-lab2-completion", "2.5-lab", f"{P} lines 130-187 (blanks at 160, 165); tests/labs/E1/lab-E1-project-2.py lines 28, 33", "PASS",
     "Page line 160 'return ___' vs twin line 28 '(d - rival) / 2'; page line 165 'return half_up(___)' vs twin line 33. Every other page line equals its twin line (run_labs PASS 3/3, which enforces 'equal or contains a blank')."),
    ("E1d-r1-lab3-run", "2.5-lab", f"{P} lines 298-367; tests/labs/E1/lab-E1-project-3.py", "PASS",
     "run_labs_project.out PASS (3/3). Page code equals twin; expected block (12 lines: a=120 and a=121) equals twin output. rederive_r4.out reproduces all 12 lines by exact Fractions (lab3 rows)."),
    ("E1d-r1-lab1-prose", "2.5-lab", f"{P} lines 57, 127", "PASS",
     "rederive_r4.out 'lab1 exact': cournot volume 200/3 (67), fee 160/3 (53), profit 20000/9 (2222), CS 20000/9, welfare 40000/9 (4444), DWL 5000/9 (556); monopoly 50, 70, 2500, 1250, 3750, 1250. Line 127 'the total of the two exchanges' matches profit=(fee-c)*Q over both exchanges (Definitions line 200, Conventions line 259)."),
    ("E1d-r1-lab2-prose", "2.5-lab", f"{P} lines 132, 138-139, 186", "PASS",
     "rederive_r4.out lab2: |q60 - d/3| = 25/864691128455135232 = 2.891e-17 < 1e-12 (True). Error recurrence e_{k+1} = -e_k/2 (Prop 2 proof, line 222). Welfare exact 40000/9 -> 4444; fee 160/3 -> 53 (rederive_r4.out lab2 lines)."),
    ("E1d-r1-lab3-prose", "2.5-lab", f"{P} lines 300, 366", "PASS",
     "rederive_r4.out lab3: a=121 monopoly fee 141/2 -> 71, volume 101/2 -> 51, profit 10201/4 = 2550.25 -> 2550. Cournot volume 200/3 and 202/3 both in (66.5, 67.5) -> 67 (line 366)."),
    ("E1d-r1-prop1", "2.6-proof", f"{P} lines 215-218 (Proposition 1)", "PASS",
     "Re-derived by hand: pi(Q) = -Q^2/b + (d/b)Q, pi' = (d-2Q)/b, pi'' = -2/b, maximiser d/2, fee (a+bc)/(2b), profit (d/(2b))(d/2) = d^2/(4b). Hypotheses a>bc>0, b>0 stated (line 216). rederive_r4.out agrees at a=120."),
    ("E1d-r1-prop2", "2.6-proof", f"{P} lines 220-223 (Proposition 2)", "PASS",
     "Re-derived: pi_i' = (d - 2q_i - q_j)/b; case q_1=0 gives q_2=d/2 and q_1=d/4>0, contradiction; symmetric solution d/3; fee (a+2bc)/(3b) since a-2d/3 = (a+2bc)/3; each exchange earns d^2/(9b); error e_{k+1} = -e_k/2 so |e_k| = d/(3*2^k). Hypotheses q_i >= 0 and a>bc>0 stated (line 221)."),
    ("E1d-r1-prop3", "2.6-proof", f"{P} lines 225-228 (Proposition 3)", "PASS",
     "Re-derived all cases of f1 <= f2: f1<c (raise to c gains); c<=f1<f2 (undercut to (c+f1)/2 gains, and for f1=c<f2 raise to g in (c,f2) gains); f1=f2=f>c (undercut to (f+c)/2 gains since (f-c)/2 * (a-bg) > (f-c)/2 * (a-bf)); (c,c) is an equilibrium. Feasible fee range [0,a/b] respected since c < a/b when a > bc."),
    ("E1d-r1-prop4", "2.6-proof", f"{P} lines 230-233 (Proposition 4)", "PASS",
     "Re-derived: CS = integral of (Q-t)/b = Q^2/(2b); G(x) = (ax - x^2/2)/b; W' = (d-x)/b; W(d)-W(Q) = (d-Q)^2/(2b); G(Q)-cQ = Q^2/(2b) + (f(Q)-c)Q via f(Q)Q = G(Q) - Q^2/(2b). All identities check symbolically (exact Fraction cross-check in rederive_r4.out)."),
    ("E1d-r1-prop5", "2.6-proof", f"{P} lines 235-238 (Proposition 5)", "PASS",
     "Re-derived every difference: fee diff d/(6b), (a+2bc)/(3b)-c = d/(3b), DWL d^2/(8b) and d^2/(18b), W(2d/3)-W(d/2) = 5d^2/(72b), profit diff d^2/(36b). Half-up rounding argument (printed diff >= exact diff - 1) is valid. Brute force (rederive_r4.out 'prop5'): 37,296 whole-number cases with b<=6, c<=24, 6b < d < 6b+260 and d>6b: 0 printed-order violations. instance_family_r4.out: 57,288 cases in the grader family: 0 violations. Statement hypotheses (whole numbers, d>6b, tie up) are all used in the proof."),
    ("E1d-r1-conventions", "2.6-spec", f"{P} lines 258-260 (Conventions)", "PASS",
     "Propositions 1-3 give volume, fee and profit; Proposition 4 gives CS, welfare, DWL (checked against the proof statements at lines 216, 221, 226, 231). Monopoly d/2 and (a+bc)/(2b); Cournot 2d/3 and (a+2bc)/(3b); Bertrand d and c. Profit (f-c)Q, Cournot profit total (line 259)."),
    ("E1d-r1-notation", "13-notation", f"{P} math spans (348 \\(...\\) spans); notation/notation.json symbols and macros", "PASS",
     "Symbols used in page math (token count from the 348 spans): a, b, c, d, Q, f, W, x, q, q_1, q_2, q_i, q_j, q_k, f_1, f_2, t, g, G, k, e_k, i, n, pi. notation.json registers T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q} and macros \\E, \\Prob, \\Var, \\Cov, \\Corr, \\R, \\N, \\indic, \\Normal, ... None is used. Plain Q (volume) is not the registered \\mathbb{Q}, and the page does not write \\mathbb{Q}."),
    ("E1d-r1-dag", "14-dag", f"{P} (no data-concept links); check_dag.out", "PASS",
     "grep 'data-concept' in project.html: none. check_dag E1: PASS. Named prerequisites: calculus, derivatives, integrals (hub line 'Prerequisites: M2'); the brief's 'Lessons 5 to 7' (line 375) refers to this unit's own lessons, not a concept."),
    ("E1d-r1-process-words", "12-process-words", f"{P} (whole file)", "PASS",
     "grep -i for verif, builder, agent, ledger, ruling, fragment, TODO, TBD, placeholder, draft, Claude, round N: one hit, line 274 'memo draft' (a learner task). No process words."),
    ("E1d-r1-citation", "3-attribution", f"{P} lines 573-579 (Reading); references/references.json key varian2014intermediate", "PASS",
     "Reading section (line 575) says no passage locator is confirmed and attributes no statement. Registry record varian2014intermediate: status verified, verified_by openlibrary, used_by E1. verify_refs_offline: 'offline integrity: 560 entries, 0 problems'."),
    ("E1d-r1-autograder-reference", "2.6-autograder", "course/modules/E/E1/grader/reference.py; tools/run_graders.py", "PASS",
     "run_graders.out: 'run_graders E1: PASS (reference 50/50 seeds, slowest 0.3 s)'. Seeds 0-9 also rerun by hand: 124 passed each (reference copied as market_structure.py in /tmp/e1d_r4/ref)."),
    ("E1d-r1-autograder-count", "2.6-autograder", f"{P} line 253; grader/test_project.py", "PASS",
     "Page says 124 checks (line 253). collect_only.out: '124 tests collected'."),
    ("E1d-r1-autograder-instances", "2.6-autograder", "course/modules/E/E1/grader/instance.py lines 3-13, 21-27; " + f"{P} line 247", "PASS",
     "Page ranges (b 1-3, c 5-60, d 60-400) match instance.py lines 23-25. Gap >= 60 > 6b on every seed (b<=3). instance_family_r4.out: all 57,288 family cases (b 1..3, c 5..60, d 60..400) satisfy every printed strict order of Proposition 5. instance.py and test_project.py are byte-identical to 8196077d."),
    ("E1d-r1-autograder-messages", "2.6-autograder", "course/modules/E/E1/grader/test_project.py lines 50-54, 92-102, 114-131, 194-195", "PASS",
     "check() and must_raise() fail with a message naming the property and never with an expected value. Ids of parametrised cases show inputs and key names only. The only bare assert in the suite (line 217, the denominator check of the tie test) prints its message only."),
    ("E1d-r1-autograder-browser", "2.6-autograder", f"{P} lines 284, 291, 592; course/assets/js/grader.js line 53; course/assets/js/python.js line 4", "PASS",
     "grader.js line 53 shows seed 'derived from your workspace ID' and the same local command as page line 291. python.js line 4 TIMEOUT_MS = 120000 matches line 251 ('stops after 120 seconds'). The only fetch in grader.js (line 18) loads the grader's own files."),
    ("E1d-r1-mutants-existing", "2.6-mutants", "ledgers/E1/mutants/ (146 files at this pin: 142 existing and 4 new in round 4); tools/mutate_graders.py --unit E1 --seeds 0-49", "PASS",
     "mutate_all_0_49.out: 'mutate_graders E1: PASS (146/146 killed)', rc 0, no SURVIVED line. Every existing mutant is killed on at least one seed in 0-49."),
    ("E1d-r1-mutants-new", "2.6-mutants", "ledgers/E1/mutants/e1d_r1_m01..m06*.py", "PASS",
     "All six round-1 mutants are KILLED in mutate_all_0_49.out."),
    ("E1d-r2-mutants-new", "2.6-mutants", "ledgers/E1/mutants/e1d_r2_m01..m05*.py", "PASS",
     "All five round-2 mutants are KILLED in mutate_all_0_49.out."),
    ("E1d-r3-mutants-new", "2.6-mutants", "ledgers/E1/mutants/e1d_r3_m01..m06*.py", "PASS",
     "All six round-3 mutants are KILLED in mutate_all_0_49.out."),
    ("E1d-r4-mutants-new", "2.6-mutants", "ledgers/E1/mutants/e1d_r4_m01..m04*.py (generated by scripts/E1-d-r4/make_mutants_e1d_r4_verify.py)", "PASS",
     "Four new student-error mutants, each one edit of the reference: m01 invalid input returns six zeros (silent fallback); m02 volume rounded by Python round() (ties to even); m03 Cournot priced for three exchanges (3d/4, (a+3bc)/(4b)); m04 monopoly profit halved. All KILLED on seed 0 (mutate_all_0_49.out). Per ruling 25 no boundary-only mutant is added: an earlier draft that warned only when the gap was exactly one trade was discarded before the run."),
    ("E1d-r1-alternatives", "2.6-alternatives", "ledgers/E1/scripts/E1-d-r2/alternatives/*, E1-d-r3/alternatives/*, E1-d-r4/alternatives/* (alt_r4_a/b/c, new); scripts/E1-d-r4/run_alts_e1d_r4_verify.py", "PASS",
     "alternatives_seeds_0_49.out: PASS on seeds 0-49 for alt_a, alt_b, alt_c, alt_d_decimal_quantize, alt_d_iterate_cutoff, alt_e, alt_g (r2), alt_r3_a, alt_r3_b, alt_r3_c and the three new alt_r4_a (integer pairs only), alt_r4_b (keyed dispatch and reordered checks), alt_r4_c (surpluses from the integral). The only FAIL is alt_f_cournot_iteration_200, whose docstring says it is inexact and must be rejected; it fails on the Cournot tie row, as intended."),
    ("E1d-r2-alternatives-new", "2.6-alternatives", "ledgers/E1/scripts/E1-d-r2/alternatives/alt_f_cournot_iteration_200.py", "PASS",
     "Rejected on seeds 0-49 at test_tie_rounds_up_for_each_output[cournot-consumer_surplus_cents-31-4-1] (the exact value 40.5 is missed by the 200-step iterate). This is correct: the page requires exact fractions (line 251)."),
    ("E1d-r3-alternatives", "2.6-alternatives", "ledgers/E1/scripts/E1-d-r3/alternatives/alt_r3_a/b/c", "PASS",
     "All three PASS on seeds 0-49 (alternatives_seeds_0_49.out)."),
    ("E1d-r4-alternatives", "2.6-alternatives", "ledgers/E1/scripts/E1-d-r4/alternatives/alt_r4_a_integer_only.py, alt_r4_b_keyed_validation.py, alt_r4_c_surplus_by_integral.py", "PASS",
     "All three correct, independent implementations PASS on seeds 0-49 (alternatives_seeds_0_49.out). Their validation orders differ from the reference (b, c checks before a in alt_r4_b), which the spec allows."),
    ("E1d-r1-rubric-structure", "2.6-rubric", f"{P} lines 388-402 (rubric table, six criteria, four levels)", "PASS",
     "Rubric table has rows C1-C6 each with four level cells (lines 394-399). Criterion levels are cumulative ('Everything in level 3...'). Structure only; no exemplar is scored (ruling 23)."),
    ("E1d-r1-rubric-C6-observable", "2.6-rubric", f"{P} line 399 (C6 levels)", "PASS",
     "C6 level 3 asks for linear demand, constant cost and two exchanges, and for each the outcome without it; level 4 adds the direction of change. Each level names checkable items."),
    ("E1d-r1-exemplar-annotations", "2.6-rubric", f"{P} lines 407-555 (Exemplars A and B), consistency only", "PASS",
     "Consistency of attributes with the official-scoring text (not scored, ruling 23): exemplar-a data-scores '1,2,2,2,1,2' vs line 409 'C1 1, C2 2, C3 2, C4 2, C5 1, C6 2'; exemplar-b data-scores '4,4,4,4,3,2' vs line 474 'C1 4, C2 4, C3 4, C4 4, C5 3, C6 2'. Exemplar numbers were re-derived in rederive_r4.out (see E1d-r4-exemplar-number-claim)."),
    ("E1d-r4-exemplar-number-claim", "2.2-numbers", f"{P} line 405 vs exemplar B line 522 (Comparison)", "FAIL",
     "Line 405: 'Their numbers are Lab 3's printed output, for the reference case'. Lab 3 prints integers only (lines 358-365). Exemplar B line 522 quotes exact values that no lab prints: 'exact differences 50/3 and 100/3', and 'd^2/(36b) = 10000/36 = 277.8'. The fractions 200/3, 160/3, 20000/9 and 5000/9 are printed by Lab 1 (line 122-123), not Lab 3. The value 277.8 appears in no lab. The claim as written is inaccurate; the numbers themselves are correct (rederive_r4.out: profit diff 2500/9 = 277.78, 50/3, 100/3, welfare diffs 6250/9 and 5000/9)."),
    ("E1d-r1-data-simulated", "11-data", f"{P} lines 53, 247; grader/instance.py line 3", "PASS",
     "Line 53 'No data file is read ... not market data'. Line 247 'It is SIMULATED ... None of it is exchange data'. instance.py line 3 'SIMULATED case ... not data from any exchange'. Labs read no data file (run_labs data-files check)."),
    ("E1d-r1-gates", "gates", "repository gates on pin edbb7aa8 (slice-scoped and full where cheap)", "PASS",
     "check_pages/check_dag/check_projects E1: PASS. run_labs --page project: 3/3. run_graders E1 0-49: PASS. page_smoke --pages project.html: PASS. mutate_graders E1 0-49: 146/146. ruff check and format --check on the grader and labs: clean. mypy --no-incremental: 'Success: no issues found in 385 source files'. Relevant pytest (test_labs, test_memo_exemplars, test_page_checks, test_run_labs, test_page_smoke, test_refs, test_curriculum, -k E1/project/memo/exemplar/refs/curriculum/page): all pass. verify_refs --offline: 0 problems."),
    ("E1d-r1-structure-order", "2.5-structure", f"{P} section order (lines 40, 51, 191, 241, 264, 282, 288, 295, 370, 557, 564)", "PASS",
     "Ladder, rungs (labs 1-2), model (definitions, propositions), specification, hours, autograder, local run, check (lab 3), memo, self-assessment, stretch, reading, references. Each section opens and closes once; check_pages PASS."),
    ("E1d-r1-atlas-studio", "2.5-structure", f"{P} (whole file)", "PASS",
     "grep -i 'atlas|studio' on project.html: 0 hits."),
    ("E1d-r1-docstring-units", "2.5-lab", f"{P} lines 58-68, 133-141, 301-310; tests/labs/E1/lab-E1-project-2.py docstring", "PASS",
     "Docstrings state units (trades, cents, trades per (cent per trade)) and match the code: volume_and_fee and reaction return trades, fees and welfare are cents; lab 2 docstring 'rounded once, a tie going up' matches half_up."),
    ("E1d-r3-lab3-placement", "2.5-structure", f"{P} lines 51-189 (rungs) and 295-368 (check)", "PASS",
     "Previous round FAIL is fixed at this pin: Lab 3 is no longer inside the skippable rungs section. Lines 46 and 297 cite the check section. Verified by section ids (grep output above)."),
    ("E1d-r3-run-report", "2.5-lab", f"{P} lines 249, 300, 303-305", "PASS",
     "run_report.py is specified as Lab 3 with the closed-form call replaced by outcome (line 249). Lab 3 names closed_form_outcome (line 353) and says what to replace it with (line 300, docstring 304-305). The printed lines are the same as the page output."),
    ("E1d-r3-starter-signature", "2.6-autograder", "course/modules/E/E1/grader/starter.py line 16; " + f"{P} line 249", "PASS",
     "starter.py line 16: outcome(structure: str, a: int, b: int, c: int) -> dict[str, int]; page line 249 gives the same signature. run_graders checks that the starter fails the suite."),
    ("E1d-r3-numbers-prose", "2.2-numbers", f"{P} prose numbers: lab prose lines 57, 127, 132, 186, 300, 366; proof numbers lines 217-237", "PASS",
     "Every prose number in the body is re-derived in rederive_r4.out (see E1d-r1-lab*-prose). Exemplar prose is checked separately (E1d-r4-exemplar-number-claim)."),
    ("E1d-r3-scope-words", "2.4-scope", f"{P} lines 67, 213, 216, 222, 249, 251, 259, 366, 385-386", "PASS",
     "'only' (line 67 'reference case only') is true: the lab uses the constants A, B, C only. 'unique' (lines 216, 222) is proved in the proofs. 'every' (line 366) is true of the table. 'exactly' (line 249) matches the test and reference dict keys. 'any' (line 251) matches the 'any other invalid input' sentence and the grader's must_raise scope. Each has a proof, a computation or an explicit hypothesis."),
    ("E1d-r3-terms-before-definition", "2.4-defs", f"{P} lines 37, 53, 57, 133-140, 201-208", "PASS",
     "Terms (Cournot, Bertrand, deadweight loss, exact fraction, tie going up) are used in the lede and labs and defined in Definitions (lines 197-208) or the Constraints (line 251) before any proposition relies on them. Lab 2 cites Proposition 2 in the model section (line 132)."),
]

FIXES = {
    "E1d-r4-exemplar-number-claim": (
        f"{P} line 405: replace 'Their numbers are Lab 3's printed output, for the reference case' with "
        "'Their printed integers are Lab 3's output; their exact values are the closed forms of Propositions 1-4, "
        "and the ones Lab 1 prints (200/3, 160/3, 20000/9, 5000/9) are printed there'. Or quote 277.8 only as a "
        "derived value of d^2/(36b)."
    ),
}

mutants = []
for line in (S / "mutate_all_0_49.out").read_text().splitlines():
    m = re.match(r"^KILLED (\S+)\.py: (.*)$", line)
    if not m:
        continue
    name, rest = m.group(1), m.group(2)
    desc, killed = rest.rsplit(" -> ", 1)
    mutants.append({
        "id": name,
        "description": desc,
        "file": f"ledgers/E1/mutants/{name}.py",
        "killed_by": killed,
    })
assert len(mutants) == 146, len(mutants)

frag = {
    "unit": "E1",
    "slice": "d",
    "round": 4,
    "verifier": "verifyS4-E1-d (Haiku 5.5)",
    "pin": "edbb7aa8de20e6d2f3035c463a79a318c22623c4",
    "base": "aeb512b65b7774b59b84f836a13984fcfe9d0d1f",
    "checkout": str(CHK),
    "scratch": "/tmp/e1d_r4",
    "verified_at": "2026-11-09T07:54:46+00:00",
    "verdict": "FAIL",
    "rows": [dict({"id": r[0], "check": r[1], "location": r[2], "status": r[3], "evidence": r[4]}, **({"fix": FIXES[r[0]]} if r[3] != "PASS" else {})) for r in rows],
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "Round 4 on edbb7aa8. Previous pin 8196077d (round 3, FAIL on E1d-r3-lab3-placement). Delta in slice: "
        "course/modules/E/E1/project.html only (Lab 3 moved from the rungs section into the check section; Lab 2 "
        "prose and Lab 1 lede/ladder wording changed; Proposition 5 hypothesis now names the tie rule; the spec's "
        "ValueError sentence reworded). grader/*, tests/labs/E1/lab-E1-project-1..3.py and the existing mutants and "
        "alternatives are byte-identical to 8196077d. Because project.html changed, every project.html row was "
        "re-verified from a full read of the page this round; nothing was carried forward. Exemplars were not scored "
        "(ruling 23); only their numbers and attributes were checked. Not run: the full pytest suite and the full "
        "repository gate (only the relevant subset above); live verify_refs (only --offline); a live Chrome UI pass "
        "(page_smoke used the repository's Chromium run). Housekeeping: the checkout initially had tracked files "
        "ledgers/E1/scripts/E1-d-r4/make_mutants_r4.py and run_alts_r4.py overwritten by this round's scripts; they "
        "were restored from HEAD with git checkout, and this round's scripts are "
        "make_mutants_e1d_r4_verify.py, run_alts_e1d_r4_verify.py, rederive_r4.py, instance_family_r4.py and "
        "build_fragment_e1d_r4_verify.py. No commit or push."
    ),
    "summary": (
        "Slice d round 4 at edbb7aa8: verdict FAIL. One FAIL row: E1d-r4-exemplar-number-claim (low): line 405 says "
        "the exemplars' numbers are Lab 3's printed output, but exemplar B quotes exact values and 277.8 that no lab "
        "prints. All other rows PASS: placement fix confirmed; Propositions 1-5 re-derived; Prop 5 brute force "
        "0 violations over 37,296 cases plus 57,288 instance-family cases; grader 124 tests, reference 50/50 seeds; "
        "146/146 mutants killed; all 13 correct alternatives (round 2 x7, round 3 x3, round 4 x3) pass seeds 0-49 "
        "(alt_f is the deliberate inexact control and is rejected). Rows: "
        f"{len(rows)} (PASS {sum(1 for r in rows if r[3] == 'PASS')}, FAIL {sum(1 for r in rows if r[3] == 'FAIL')})."
    ),
}
bad = [r["id"] for r in frag["rows"] if r["status"] != "PASS" and not r.get("fix")]
out = CHK / "ledgers/E1/E1-d.json"
out.write_text(json.dumps(frag, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out, "rows", len(frag["rows"]), "mutants", len(mutants), "non-PASS without fix", bad)
