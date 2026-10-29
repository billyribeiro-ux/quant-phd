"""Assemble ledgers/M6/M6-d.json (round 2) from the verifier's observations. Mutant kill data is read from the
mutate_graders output saved at /tmp/M6-v/d/mutate3.txt; mutant descriptions are read from the mutant files."""
import ast
import json
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
mut_dir = root / "ledgers/M6/mutants"
kills = {}
for line in Path("/tmp/M6-v/d/mutate3.txt").read_text().splitlines():
    m = re.match(r"(KILLED|SURVIVED) (\S+?): .* -> (.*)$", line)
    if m:
        kills[m.group(2)] = (m.group(1), m.group(3))
mutants = []
for f in sorted(mut_dir.glob("*.py")):
    doc = ast.get_docstring(ast.parse(f.read_text(encoding="utf-8"))) or ""
    status, where = kills.get(f.name, ("MISSING", ""))
    entry = {"description": doc.splitlines()[0], "file": f"ledgers/M6/mutants/{f.name}"}
    if status == "KILLED":
        entry["killed_by"] = where
    else:
        entry["survived"] = True
    mutants.append(entry)

F = "course/modules/M/M6/project.html"
G = "course/modules/M/M6/grader/test_project.py"
rows = [
 ("proj-lede-engine-scope", "2.6-spec", f"{F} line 37 (lede) against lines 174-178 and 188", "PASS",
  "Lede now says the engine checks the doubling strategy with a capital limit and that the uncapped case is argued in the stopping-rule section. The engine signature and ValueError list (lines 174-188) require a capital, and tests/grader test_project.py contains no uncapped doubling test (82 tests, grep). Round-1 defect (uncapped engine claim) is fixed."),
 ("proj-spec-dangling-table", "2.9-structure", f"{F} line 174", "PASS",
  "Line 174 now reads 'with the five functions listed in this paragraph'; the functions are listed in the same paragraph. grep for 'table below' in project.html returns nothing."),
 ("proj-statements-tests-claim", "2.6-spec", f"{F} line 191; {G}", "PASS",
  "Line 191 now says the tests check instances of P1 and P2 and the closed forms of the dyadic martingale, and P3 is graded by the rubric only. test_project.py checks P1 (test_fair_walk_bounded_stopping_keeps_expectation, test_stopped_value_matches_enumeration) and P2 (test_doob_probability_and_bound_match_enumeration) and the dyadic closed form (test_dyadic_mean_square_error_closed_form); no P3 test exists (grep)."),
 ("proj-conventions-raise-table", "2.6-spec", f"{F} line 188; {G} lines 220-236, 287-301, 388-398, 433-441", "PASS",
  "The five named ValueError conditions (horizon N<1 in stopped and Doob, cap>N, lambda<=0, capital<=0, base>capital) each have a must_raise or must_accept test; no test demands a ValueError for an unnamed condition (the reference's extra raises for n<0, p outside (0,1), x outside [0,1], base<=0 are not required by any test). Suite 82/82 on seed 0 and 50/50 reference seeds."),
 ("proj-hours", "2.10-hours", f"{F} lines 228-234 and 33; course/modules/M/M6/index.html data-hours-lessons=108 data-hours-project=42; curriculum/01-foundations.yaml:264", "PASS",
  "Recomputed: 12 lessons x 9 h = 108 (each Lnn.html data-hours=9, grep); project 42; 108+42=150 equals curriculum hours 150; project share 42/150 = 28%, inside the 10-40% rule. Time-budget rows 3+4+17+10+5+3 = 42 (page lines 228-234)."),
 ("proj-browser-claims", "2.9-structure", f"{F} lines 178, 180, 242; course/assets/js/python.js:4 (TIMEOUT_MS = 120000)", "PASS",
  "The 120-second run limit matches python.js:4 (const TIMEOUT_MS = 120000). Autosave claim matches page line 242. Assets unchanged between round-1 pin and e22feb3 (git diff --stat, empty)."),
 ("proj-statements-math", "2.4-math", f"{F} statement block (P1-P3) and appendix proofs lines 581-583", "PASS",
  "Statements unchanged since round 1. Re-derived appendix proofs: P1 (indicator telescoping with {tau>k} in F_k, sum of E[1_A(M_{k+1}-M_k)]=0) valid; P2 (disjoint first-exceedance sets A_k in F_k, chained submartingale inequality, E[X_N]>=E[X_N 1_A]>=lambda P(A), X_N>=0) valid; P3 (orthogonality, E[(M_n-M_m)^2]=v_n-v_m, Doob on squared increments, Cauchy null-set argument with 4j^2(L*-v_m)->0) valid. Cited lemmas exist: L12 Lemma 12.1 (orthogonality), Lemma 12.3 (square of increments), Proposition 12.8 (dyadic); L11 Corollary 11.4 and Theorem 11.3; L10 Proposition 10.7 and 10.9. Dyadic error 1/(12*4^n) re-derived by the cell integral (lab 3 prints equality for n=0,1,2,3,10)."),
 ("proj-exemplarB-P2-one-case", "2.4-math", f"{F} line 582 (Exemplar B, Appendix, P2)", "PASS",
  "Line 582 now says the bound is attained in some cases and gives the one case (|S|, N=1, lambda=1: probability 1, bound 1). No claim that one case is the only attainment remains; the L11 statement it cites is the same case."),
 ("proj-exemplarB-P3-measurability", "2.4-math", f"{F} line 583 (Exemplar B, Appendix, P3)", "PASS",
  "Line 583 now states that each M_n is a random variable, so G = union_j intersect_m union_{k,l>=m}{|M_k-M_l|>=1/j} is an event; the countable-union and null-set steps are then explicit. Re-derived: the set identity and the inclusion G subset of union_j intersect_m D_m(1/(2j)) hold."),
 ("rubric-descriptors-observable", "2.9-structure", f"{F} lines 464-466 (rubric table)", "PASS",
  "Descriptors C1 (level 4: doubling without capital limit, P(tau>N)=2^-N) and C5 (level 4: Lesson 11 case N=1, lambda=1) match the stopping-rule section and L11 Corollary 11.4 example; each level is observable."),
 ("rubric-calibration", "2.9-structure", f"{F} lines 471-592; data-scores=2,1,2,2,2 (line 473) and 4,4,4,3,4 (line 528)", "PASS",
  "Official scoring equals the annotations: Exemplar A misses (C1 level 3, C2 level 2, C3 level 3, C4 level 3, C5 level 3) give 2,1,2,2,2; Exemplar B meets and misses give 4,4,4,3,4. Every 'Meets' or 'Misses' item in the annotations was checked against the descriptor levels."),
 ("rubric-exemplarA-C3-annotation", "2.2-numbers", f"{F} lines 484 and 497 (Exemplar A annotations)", "PASS",
  "The C3 annotation now cites 'about 95 cents' and Lab 3's printed 69533/729 and cent amount 95 (lab output). The C5 annotation cites 5/8, which Lab 3 prints. The round-1 unprinted value (the bound 2 for E[X_N^2]/3) was removed; no value in the annotations is absent from Lab 3 output."),
 ("lab-project-1", "2.5-labs", "tests/labs/M6/lab-M6-project-1.py; project.html lines 55-123 (unchanged since round 1)", "PASS",
  "Twin unchanged since 55b5634; run python -I -W error: exit 0. Printed lines (8 paths, E[S_tau]=0, E[S_(tau and k)]=0 for k=0..3) match the page's output block and the interpretation (1/2 and -1/2 contributions recomputed by hand)."),
 ("lab-project-2", "2.5-labs", "tests/labs/M6/lab-M6-project-2.py; project.html lines 125-165 (unchanged)", "PASS",
  "Twin run: exit 0. Output lines 'capital 100: 6 bets, 37 left', 'capital 1: 1 bet, 0 left', 'capital 1000 cap 6: 6 bets, 937 left' match the page; 1+2+4+8+16+32=63 and 100-63=37 re-derived."),
 ("lab-project-3-scope", "2.5-labs", "project.html line 259 (hypothesis) and twin line 7 (docstring) against the loop 'for n in (0, 1, 2, 3, 10)' in lab-M6-project-3.py", "PASS",
  "Round-1 defect fixed: the hypothesis (line 259) and the twin docstring both list levels 0, 1, 2, 3 and 10, matching the loop that prints five levels. No claim of levels 0 to 10 remains."),
 ("lab-project-3-numbers", "2.2-numbers", f"{F} lines 423-436 (expected block), 437 (interpretation); tests/labs/M6/lab-M6-project-3.py output", "PASS",
  "Run output equals the page block: E[S_tau]=0; control -79/81 (not used on the page as a number except as its own statement); Doob 7/16 <= 5/8; fair doubling 100; control 69533/729 = 95.381344 (recomputed: 729*95=69255, remainder 278, 278/729=0.381344) and 95 cents; dyadic 1/12, 1/48, 1/192, 1/768, 1/12582912 = 1/(12*4^n); M_10(1/3)=683/2048 (cell index floor(1024/3)=341, midpoint 683/2048). Decimals are six places, stated as display rounding."),
 ("lab-project-interpretation-claims", "2.2-numbers", f"{F} lines 122, 164, 437", "PASS",
  "The interpretation of Lab 3 now says the lab does not test the engine and the suite does; the lab does not claim to test it (lab 3 contains no engine call). Lab 1 and 2 interpretations unchanged and consistent with their printed output."),
 ("grd-reference-suite", "2.5-labs", "course/modules/M/M6/grader/reference.py; tools/run_graders.py --unit M6 --seeds 0-49", "PASS",
  "Command output: 'run_graders M6: PASS (reference 50/50 seeds, slowest 0.3 s)', exit 0."),
 ("grd-instances", "2.5-labs", "course/modules/M/M6/grader/instance.py (unchanged); tools/run_graders.py check_instances", "PASS",
  "instance.py unchanged since 55b5634; run_graders check_instances passes for seeds 0-49; test_instance_is_labelled_and_valid passes for both seeds."),
 ("grd-collect-count", "2.9-structure", f"{G}; {F} line 180 ('82 tests')", "PASS",
  "pytest --collect-only -q test_project.py: '82 tests collected'. Page says 82 (line 180). Round-1 count 64 is superseded."),
 ("grd-messages-leak", "2.6-spec", f"{G} line 465 and line 511 (print expected values); line 209 borderline", "FAIL",
  "The expect() docstring and module docstring say a failure message never holds a value / never prints the expected value. Line 465 says 'must round down to 0 cents' (the expected cent amount) and line 511 says 'so the level-1 value is 1/4' (the expected value). Line 209 names the fair value 0 ('must differ from S_0 = 0')."),
 ("grd-docstring-enumeration-claim", "2.6-spec", f"{G} lines 6-10 against the test bodies", "PASS",
  "The docstring now says expected numbers come from exact enumeration, closed forms, or hand-worked values, never from the engine. Checked each section: enumeration tests call enum_stopped/enum_doob/enum_doubling; dyadic tests use Fraction(1, 12*4**n) closed forms and hand values (1/4, 3/4, 3/8); doubling edge tests use hand values (2/5, 1/2). None uses sol.* as its expected value."),
 ("grd-alternatives-pass", "2.5-labs", "ledgers/M6/scripts/alternatives/alt1..alt5 (run unchanged); ledgers/M6/scripts/M6-d-r1/alternatives/alt_v1_stop_level_sums.py, alt_v2_matrix_chain.py; ledgers/M6/scripts/M6-d-r1/run_candidates.py 0-9", "PASS",
  "run_candidates.py 0-9 against the e22feb3 grader: alt1 10/10, alt2 10/10, alt3 10/10, alt4 10/10, alt5 10/10, alt_v1 10/10, alt_v2 10/10 (no failing seed). These use different enumeration, DP, matrix, float-cutoff, and recursion formulations."),
 ("grd-mutants-run", "2.6-mutation", "tools/mutate_graders.py --unit M6 --seeds 0-9; ledgers/M6/mutants/*.py (36 files)", "FAIL",
  "Output /tmp/M6-v/d/mutate3.txt: 35 of 36 KILLED. m01 and m02 (changed this round) and the 30 earlier mutants are killed; the six verifier mutants m31-m36 are killed except m36_probabilities_rounded_before_expectation, which SURVIVED all 82 tests on 10 seeds (see grd-rounding-once-witness)."),
 ("grd-local-pytest-and-pyodide", "2.5-labs", f"{G}; tools/page_smoke.py --unit M6 --pages project", "PASS",
  "QF_SEED=0 pytest -q -p no:cacheprovider --assert=plain -W error test_project.py: 82 passed. page_smoke --unit M6 --pages project: 'page_smoke modules/M/M6/project.html: PASS', 'in-browser grader: All 82 tests pass on seed 2055106663 (1.0 s)', exit 0."),
 ("grd-ruff-mypy", "2.9-structure", "tests/labs/M6; course/modules/M/M6/grader", "PASS",
  "ruff check and ruff format --check on tests/labs/M6 and grader: 'All checks passed!', '19 files already formatted'. Repo mypy gate (.venv/bin/mypy --no-incremental): 'Success: no issues found in 229 source files'. Direct mypy on the grader folder reports import-not-found for its sibling modules; the grader is not in the repo mypy file list, so this is not a gate failure."),
 ("proj-exemplar-B-other-claims", "2.4-math", f"{F} lines 533, 544, 555, 568-569", "PASS",
  "Summary: 7/16 < 5/8, expected 100 cents, control 95 cents (69533/729), dyadic 1/(12*4^n) at 0,1,2,3,10: all printed by lab 3. Limitations: 'within half a cent' is the half-up rule; 69533/729 cents below 100 cents is printed. Recomputed numbers match."),
 ("proj-notation", "2.9-structure", f"{F} (all math); notation/notation.json", "PASS",
  "Macros used are \\E, \\Prob, \\indic (registered in notation.json macros) plus standard LaTeX. None of the reserved symbols T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q} occurs in the page (grep count 0). L^\\ast denotes the P3 limit and does not collide with the registered R^\\ast. Symbols S, tau, N, lambda, p, s, K, J, M, X, Y, L, v_n, D_m, G, Omega_0 are defined in the page before use."),
 ("proj-banned-phrases", "2.9-structure", f"{F}; cards.json; tests/labs/M6/lab-M6-project-*.py; {G}", "PASS",
  "Scan for TODO, TBD, lorem, for brevity, details omitted, beyond the scope, left as an exercise, you can add more, it is important to note, studies show, experts agree, it is well known, obviously, clearly, roughly half, about 6%, historically: no hit. Ellipses found are mathematical sequences (1, 2, 3, ...; N = {1, 2, 3, ...}; K = 1, 3, 7, 15, ...) or code arguments, not omitted content."),
 ("proj-dag-structure", "2.8-dag", "tools/check_dag.py --unit M6; tools/check_projects.py --unit M6", "PASS",
  "check_dag.py --unit M6: 'check_dag M6: PASS'. check_projects.py --unit M6: 'check_projects M6: PASS'. The project page declares no data-concept or dfn element (grep), so no concept is used or defined on it outside the closure."),
 ("proj-references", "2.1-citations", f"{F} lines 603-615 (Reading, References); references/references.json", "PASS",
  "Reading section unchanged since round 1 (byte-identical lines, git diff hunks do not touch it). It attributes no statement to the two registry keys and says no passage was read, which matches the page text."),
 ("cards-numbers", "2.2-numbers", "course/modules/M/M6/cards.json (c007, c017, c030, c032, c037, c040, c049, c053, c061, c071, c090, c098, c100, c102, c112, c113, c121)", "PASS",
  "Changed cards re-derived: c032 (I_1 = 0.1464466, gap 0.1868867, bound 0.5) in lab L03 output; c037 (2 - 1/n) re-derived by integral; c049 (error 1.30e-07 against pi/4) in lab L05 output; c061 (2, 1/2, 2, 1/3) in lab L06 output; c081 (1023 of 1023; 0 of 1023; increment -1/3 = 2p-1) in lab L08 output; c105 (K+1-2^m, zero at K+1 a power of two) re-derived. Unchanged cards carried from round 1 (byte-identical objects)."),
 ("cards-cited-headings", "2.1-citations", "course/modules/M/M6/cards.json; ledgers/M6/scripts/M6-d-r2/card_locators.py", "PASS",
  "Scan of all 122 cards: every 'Definition/Proposition/Lemma/Theorem/Corollary/Example/Remark/Assumption/Problem/Result' locator resolves to an item in its lesson or the cited lesson HTML: 0 unresolved (script output 'checked 122 cards; unresolved: 0')."),
 ("cards-duplicates", "2.7-cards", "course/modules/M/M6/cards.json (near-duplicate scan)", "PASS",
  "The five round-1 pairs are resolved: c009, c019, c033, c041 and c109 are removed. A full pairwise scan (ledgers/M6/scripts/M6-d-r2/cards_scan.py) lists similar wording but each pair asks a different question (e.g. c097 vs c098, c110 vs c111, c112 vs c113)."),
 ("cards-grades", "2.7-cards", "course/modules/M/M6/cards.json", "PASS",
  "Every card with grade C has a basis (15 of 15); no T card carries a basis; c081 is now grade C with basis 'Lab 1, Part B'. The 34 cards without a grade are definitions or structural prompts; scan for lab-result claims without a grade returns nothing. Round-1 defect fixed."),
 ("cards-agree-lesson-text", "2.7-cards", "course/modules/M/M6/cards.json (all 122) against L01-L12", "UNVERIFIABLE",
  "Read in full: the 17 changed or added cards (c006, c016, c032, c037, c039, c049, c054, c061, c062, c075, c080, c081, c105, c125-c128) against their lesson text, and all card locators (0 unresolved). Not completed: a line-by-line agreement read of the remaining ~105 unchanged cards against each lesson's current text (the card wording was not compared with every lesson sentence). Fix: complete that comparison for L01-L12."),
]
rows = [r for r in rows]
new_rows = [
 ("proj-downstream-ap1-sc1", "2.1-citations", f"{F} line 37 (lede) and line 172 (Context); curriculum/03-markets.yaml:264-290 (AP1 core) and :505-512 (SC1 core)", "FAIL",
  "The lede says the three results are 'the results that the later modules AP1 and SC1 use for martingales', and Context says 'the curriculum names the later modules AP1 and SC1 as users of the three martingale results'. The curriculum records only the prerequisite edge M6 -> AP1 and M6 -> SC1; the AP1 core text names no martingale result, and the SC1 core names continuous-time martingales and stopping times, not the three discrete results. The claim is not in the curriculum."),
 ("grd-rounding-once-witness", "2.6-spec", f"{G} (no test covers rounding order); course/modules/M/M6/project.html line 178 ('computed from the exact value and rounded once, half up') and line 188 ('E[final wealth] rounded once, half up')", "FAIL",
  "Witness run (ledgers/M6/scripts/M6-d-r2/rounding_witness.py): capital 1 cent, base 1 cent, p = 1/4 - 10^-7. Exact expectation 2p = 2499999/5000000 = 0.4999998 cents. Reference doubling_outcome gives expected_final_wealth_cents 0; mutant m36 (probability rounded to six decimals first) gives 1. All 82 tests pass on m36, so the suite does not enforce the rounding-once rule that the page states. Fix: add a test that uses this instance and expects 0 cents, and state the rule in the test."),
]
allrows = rows + new_rows
FIX = {
 "grd-messages-leak": "Reword the two messages so they name the property and not the value: line 465 'the expected cent amount must follow the half-up rule' and line 511 'the point lies in the first cell, so the value is that cell's midpoint'. Remove the value from line 209 too ('must differ from the fair value').",
 "grd-mutants-run": "Add a test that pins the rounding-once rule: the witness instance of grd-rounding-once-witness, expecting 0 cents. Then m36 is killed and the suite gives 36/36.",
 "cards-agree-lesson-text": "Complete a line-by-line comparison of all 122 cards with the current text of L01-L12 (the 17 changed cards are done) and record each card's agreement row.",
 "proj-downstream-ap1-sc1": "Line 37: replace 'the results that the later modules AP1 and SC1 use for martingales' with 'the three results that the martingale tools of this unit rest on'. Line 172: delete the sentence 'The curriculum names the later modules AP1 and SC1 as users of the three martingale results of this unit.'",
 "grd-rounding-once-witness": "Add to test_project.py a test with capital 1, base 1, win_probability 1/4 - 1/10**7 that asserts expected_final_wealth_cents == 0, with the message 'the expectation is rounded once, half up, from the exact value'.",
}
for r in allrows:
    pass

frag = {
 "unit": "M6",
 "slice": "M6-d",
 "round": 2,
 "verifier": "Claude Haiku 5.5 (independent verifier, round 2, M6 project slice; did not build M6; no shared context with the builders)",
 "pin": "e22feb3 (detached checkout /tmp/verifyC2-M6-d; round-1 pin 55b5634; delta for this slice from 55b5634 to e22feb3)",
 "base": "55b5634 (round-1 verified pin for M6-d)",
 "checkout": "/tmp/verifyC2-M6-d",
 "scratch": "/tmp/M6-v/d",
 "verified_at": "2026-10-28",
 "verdict": "FAIL",
 "rows": [{"id": i, "check": c, "location": l, "status": s, "evidence": e, **({} if s == "PASS" else {"fix": FIX[i]})} for i, c, l, s, e in allrows],
 "mutants": mutants,
 "registry_flags": [],
 "freshness_flags": [],
 "notes": "Delta since 55b5634 for this slice: project.html (35 lines), grader/test_project.py, cards.json (cards removed c009 c019 c033 c041 c063 c109; added c125-c128; changed c006 c016 c032 c037 c039 c049 c054 c061 c062 c075 c080 c081 c105), tests/labs/M6/lab-M6-project-3.py, ledgers/M6/mutants m01 and m02 changed, m11-m30 added in e22feb3. index.html (hub hours) changed and was re-checked. Unchanged and re-run: grader reference.py, instance.py, starter.py, lab-project-1 and -2, assets/js, notation, references. Not checked: line-by-line agreement of the unchanged cards with the lessons (see cards-agree-lesson-text); lab L01-L12 twins (other slices).",
 "summary": "Project slice of M6, round 2: verdict FAIL. 36 round-1 rows re-checked and 2 new rows: PASS 33, FAIL 4, UNVERIFIABLE 1. FAILs: AP1/SC1 downstream overclaim in the lede and Context; grader failure messages that state expected values (lines 465, 511); mutant m36 survives the suite and a witness instance (p = 1/4 - 1e-7) separates it from the rule the page states; cards-agree-lesson-text not completed for unchanged cards (UNVERIFIABLE).",
}
out = root / "ledgers/M6/M6-d.json"
out.write_text(json.dumps(frag, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("rows", len(allrows), "mutants", len(mutants))
