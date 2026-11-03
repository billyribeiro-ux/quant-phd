"""Build ledgers/FC2/FC2-d.json (round 3, verifier D3) from the evidence files in ledgers/FC2/scripts/FC2-d-r3/ind/."""
import json
import re
import sys
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyD3-FC2-d")
IND = "ledgers/FC2/scripts/FC2-d-r3/ind"
C = "Carried from round 2 (course/assets/js/grader.js and py-worker.js byte-identical since the previous pin; git diff --quiet c737272f a007712f -- course/assets/js is empty):"
CARD = ("Carried from round 2 (course/modules/FC/FC2/L02.html byte-identical since the previous pin; cards.json object {id} byte-identical, "
        "git diff c737272f a007712f touching only c003, c010, c012, c019, c095, c098, c132 and appending c146-c148):")

rows = []


def row(id_, check, location, status, evidence, fix=None):
    r = {"id": id_, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    rows.append(r)


# ---- command gates (re-run on a007712f) ----
row("fc2d-r2-gate-mutate", "2.6 mutation gate: tools/mutate_graders.py --unit FC2 --seeds 0-9 must exit 0",
    "tools/mutate_graders.py; ledgers/FC2/mutants/ (63 files)", "PASS",
    f"{IND}/mutate_graders_r3x.out: 'mutate_graders FC2: PASS (63/63 killed)', rc=0 (run after adding q3_a..q3_d). Every mutant listed in the fragment mutants array is KILLED.")
row("fc2d-r2-gate-run-graders", "2.6 run_graders --unit FC2 --seeds 0-49 (reference, starter, typecheck, timing)",
    "tools/run_graders.py; course/modules/FC/FC2/grader/", "PASS",
    f"{IND}/run_graders.out: 'run_graders FC2: PASS (reference 50/50 seeds, slowest 0.2 s)', rc=0. The tool also runs the starter (fails the suite) and mypy --strict on reference, instance and starter.")
row("fc2d-r2-gate-check-projects", "tools/check_projects.py --unit FC2 and --all",
    "tools/check_projects.py", "PASS",
    f"{IND}/check_projects_fc2.out: 'check_projects FC2: PASS' rc=0; {IND}/check_projects_all.out line 15 'check_projects FC2: PASS'.")
row("fc2d-r2-gate-check-dag", "2.9 tools/check_dag.py --unit FC2",
    "tools/check_dag.py", "PASS", f"{IND}/check_dag_fc2.out: 'check_dag FC2: PASS' rc=0.")
row("fc2d-r2-gate-check-pages", "2.9 tools/check_pages.py --all (no single-unit run was needed)",
    "tools/check_pages.py", "PASS", f"{IND}/check_pages_all.out line 15: 'check_pages FC2: PASS' (22 lines, all units PASS).")
row("fc2d-r2-gate-run-labs", "2.5 tools/run_labs.py --unit FC2 --page project",
    "tools/run_labs.py; project.html lab-FC2-project-1..3", "PASS", f"{IND}/run_labs_project.out: 'run_labs FC2: PASS (3/3)'.")
row("fc2d-r2-lab-twins-isolated", "2.5 project twins alone under python -I -W error",
    "tests/labs/FC2/lab-FC2-project-1.py, -2.py, -3.py", "PASS",
    f"{IND}/project_labs_compare.out: 'twin rc=0' for labs 1, 2 and 3 (python -I -W error, run by the verifier).")
row("fc2d-r2-lab-page-equals-twin", "2.5 page code equals twin (blanks allowed); expected block equals twin output",
    "course/modules/FC/FC2/project.html lines 56-146, 169-257, 378-468 (expected blocks 147-162, 258-273, 469-485)", "PASS",
    f"{IND}/project_labs_compare.py output ({IND}/project_labs_compare.out): lab 1 and lab 3 page code equals twin on all 91 lines (0 differing lines); lab 2 differs from its twin on exactly three lines, the blanks (58 'gap = ___' vs 'gap = parity_gap(...)', 60 and 73 'net = ___' vs 'net = gross - cost'); expected block equals twin output for labs 1, 2 and 3.")
row("fc2d-r2-gate-page-smoke", "2.9 tools/page_smoke.py --unit FC2 --pages project (alone)",
    "tools/page_smoke.py", "PASS", f"{IND}/page_smoke_project.out: 'page_smoke modules/FC/FC2/project.html: PASS', 'in-browser grader: All 91 tests pass on seed 142714009', 'page_smoke FC2: PASS', rc=0.")
row("fc2d-r2-gate-ruff-mypy", "ruff check, ruff format --check, mypy --no-incremental",
    "tests/labs/FC2; course/modules/FC/FC2/grader", "PASS",
    f"ruff check tests/labs/FC2 course/modules/FC/FC2/grader: 'All checks passed!' ({IND}/ruff_check.out); ruff format --check: '15 files already formatted' ({IND}/ruff_format.out); .venv/bin/mypy --no-incremental: 'Success: no issues found in 331 source files', rc=0 ({IND}/mypy_default.out).")
row("fc2d-r2-gate-pytest-fc2", "relevant pytest (lab, page, refs, memo and FC2 filters)",
    "tests/labs/FC2; tests/test_labs.py; tests/test_run_labs.py; tests/test_page_checks.py; tests/test_memo_exemplars.py; tests/test_refs.py", "PASS",
    f"{IND}/pytest_relevant.out: all selected tests pass, rc=0 (this round ran the listed files with -k 'FC2 or fc2 or project or grader or lab or page or refs or memo'; not the full suite).")
row("fc2d-r2-gate-verify-refs", "2.1 verify_refs: offline integrity and live FC2 entries",
    "tools/verify_refs.py; references/references.json", "PASS",
    f"{IND}/verify_refs_offline.out: 'offline integrity: 560 entries, 0 problems', rc=0; {IND}/verify_refs_live_FC2.out: 'live re-verification of FC2: 3 of 560 entries, 0 problems', rc=0. references/ is byte-identical since c737272f (git diff empty).")
row("fc2d-r2-collect-count", "2.6 collected check count equals the page's 91, every seed 0..49",
    "course/modules/FC/FC2/project.html line 320; grader/test_project.py", "PASS",
    f"{IND}/collect_count.py (reference as scanner.py, pytest --collect-only per seed) -> {IND}/collect_count.out: 'distinct counts: [91]', seeds: 50.")
row("fc2d-r2-starter-suite-fails", "2.6 the suite fails on starter.py",
    "course/modules/FC/FC2/grader/starter.py; project.html line 297", "PASS",
    f"{IND}/starter_seed0.out: starter as scanner.py, seed 0: '83 failed, 8 passed', rc=1 (the 8 are the purity and import tests).")

# ---- numbers and hours ----
row("fc2d-r2-numbers-lab1", "2.2 numbers in prose: Lab 1 (project.html 55-163)",
    "course/modules/FC/FC2/project.html:55-163", "PASS",
    f"Re-derived by hand: parity gaps 0, 120, 0, 0, -20, 0 (C-P-(S-K df), df 0.99); nets 75 and -25; chord 625 = 0.5*800 + 0.5*450 at 10500; call 700; convexity gross 75, net 30; two findings kept. The page's expected block for lab 1 equals the output of its twin (tests/labs/FC2/lab-FC2-project-1.py) in {IND}/project_labs_compare.out.")
row("fc2d-r2-numbers-lab3", "2.2 numbers in prose: Lab 3 (project.html 376-486)",
    "course/modules/FC/FC2/project.html:376-486", "PASS",
    "Re-derived: cost 60; parity gap at 4500 = 820-155-(5000-4275) = -60 (gross 60, net 0, not kept); at 6500 gap 226 (net 166); at 7000 gap 540 (net 480); chord at 6000 through 5000 (500) and 6500 (151) = (500+2*151)/3 = 802/3, call 330, chord less call -188/3, gross round(62.67)=63, net 3; at 5000 chord less call 470/3 (1970/3-500) matches the printed line 479. Prose 'about minus 62.67' is correct to two decimals.")
row("fc2d-r2-numbers-exemplars", "2.2 numbers in prose: exemplars A and B (project.html 517-634)",
    "course/modules/FC/FC2/project.html:520-634", "PASS",
    "Re-derived: 6500*0.95 = 6175 and 151-1100-(5000-6175) = 226; 7000*0.95 = 6650 and 90-1200-(5000-6650) = 540; chord at 6000 through 5000 (500) and 6500 (151) with weights 1/3, 2/3 = 802/3; 802/3-330 = -188/3; gross 63, net 3; exemplar A's 'about 226/540/63' are rounded forms of the same values. Exemplar B's df derivative statement (each parity gap moves by K times the change in df) is correct (gap is linear in df with slope K).")
row("fc2d-r2-hours", "2.6 hours: arithmetic and consistency with the hub",
    "course/modules/FC/FC2/project.html:33,35,339-356; course/modules/FC/FC2/index.html (identical)", "PASS",
    "Rows 2+3+5+9+3+5+3 = 30 (project.html lines 345-352); data-hours-project=30 (line 33); eyebrow '30 hours' (line 35); hub index.html: '60 h lessons · 30 h project' (line 41) and data-hours-project 30 (line 29). Ruling: design targets, no arithmetic fault.")
row("fc2d-r2-banned-phrases", "2.9 banned phrases and process words in learner text",
    "project.html; cards.json; grader/*.py; tests/labs/FC2/lab-FC2-project-*.py", "PASS",
    "grep -n -i -E 'verifier|builder|todo|tbd|lorem|for brevity|details omitted|beyond the scope|left as an exercise|you can add more|it is important to note|studies show|experts agree|it is well known|obviously|clearly|\\bwe\\b|\\bour\\b' over those files: no hits (run this round on the changed files, and the twins).")
row("fc2d-r2-notation", "2.4 notation against notation/notation.json",
    "notation/notation.json; project.html formulas lines 85-88 (plain text), 333-336", "PASS",
    "The page writes formulas in plain text with C, P (put), S, K, df, D (lessons), and labels P1-P6; grep over project.html for registered symbols (T, Phi, gamma_3, gamma_4, R^*, R_f, Q) finds none in use. No symbol clash.")
row("fc2d-r2-dag", "2.9 check_dag and concepts outside the closure",
    "project.html lines 37, 55, 333-336; curriculum/02-economics-finance-core.yaml FC2 prereqs", "PASS",
    f"{IND}/check_dag_fc2.out PASS. Links: arbitrage-opportunity (L01), put-call-parity and option-arbitrage-bounds (L05). The curriculum now lists prereqs [M4, CF1, FC1] for FC2 (curriculum/02-economics-finance-core.yaml line 400), so FC1's bid-ask spread is inside the closure; the plain-prose use at project.html line 333 is allowed by the architect decision. The open-items DAG_DEFECT for bid-ask-spread is stale (plans/FC2-open-items.md; not in this slice).")
row("fc2d-r2-reading-keys", "2.1 reading list and the cited theorems",
    "project.html 653-658; L05.html", "PASS",
    "data-cite keys hull2021options, stoll1969relationship, cox1979option resolve (verify_refs live FC2: 3 of 560, 0 problems). The page quotes no locator. Theorem 1.2 (put-call parity, L05 line 25 of the text dump) and Theorem 3.2 (convexity in strike, L05 line 53) and Theorem 2.2 (model-free bounds, L05 line 35) are stated and proved in L05.html.")
row("fc2d-r2-autograder-panel-claims", "2.6 autograder panel statements (project.html 285, 360, 367)",
    "course/assets/js/grader.js:18, 33-80; course/assets/js/py-worker.js:3, 111", "PASS",
    C + " grader.js line 18 is a GET (fetch) of the grader's own suite files; no upload of learner code (grep for POST, upload, sendBeacon, WebSocket in grader.js and py-worker.js: none). py-worker.js line 3 states that Pyodide is vendored and 'nothing is fetched'. Round-2 evidence for the file-load and draft-save lines is carried.")
row("fc2d-r2-hub-placement-claim", "2.9 cross-page claim: placement bar and skip rule",
    "project.html:42; index.html:148", "PASS",
    "Both read this round: project.html line 42 'Rungs 1 and 2 are optional when you reach the placement bar on the module hub and answer both skill checks'; index.html line 148 'You may skip them when you reach the placement bar and answer both skill checks'. Rung 3 graded and not skippable (line 42). index.html is byte-identical to c737272f.")
row("fc2d-r2-scope-curriculum-brief", "2.6 Rung 3 matches the curriculum scope exactly",
    "curriculum/02-economics-finance-core.yaml:427-429 (brief); project.html:285 (Inputs)", "FAIL",
    "The brief still reads 'Given an embedded option-chain snapshot, detect put-call parity and convexity violations net of a stated cost model, and explain each one found.' (curriculum/02-economics-finance-core.yaml lines 427-429). project.html line 285 says 'No market data is embedded' and grades a SIMULATED chain. The page follows the binding architect decision in plans/FC2-build-plan.md (Architect decisions: 'the option chain is SIMULATED with a bring-your-own-chain schema and a DATA_REQUEST'), but the curriculum brief still names an embedded snapshot, so the unit scope and the page disagree. Open item D1 in plans/FC2-open-items.md confirms no licensed option-quote source.",
    fix="Architect: amend curriculum/02-economics-finance-core.yaml lines 427-429 to 'Given a SIMULATED option chain in a documented schema, detect ...' (the binding decision), or supply a redistributable snapshot with a quoted licence (DATA_REQUEST D1) and then embed it and rebuild the grader instances. The page does not change.")
row("fc2d-r2-rubric-C2-level2", "2.6 rubric: every level descriptor observable",
    "course/modules/FC/FC2/project.html:509 (rubric C2, level 2 cell)", "PASS",
    "Round-2 FAIL is fixed at a007712f: the level-2 cell now reads 'States the cost model, but does not say, for each finding, whether it survives the cost, or reports gross amounts without the cost.' Level 3 says 'says ... for each finding whether it survives the cost', so a note that tells survival per finding is level 3 and one that does not is level 2. Observable.")
row("fc2d-r2-rubric-calibration", "2.6 rubric calibration: blind scoring of exemplars A and B within one level",
    "course/modules/FC/FC2/project.html:520-634 (data-scores 4,4,3,3,3 and 2,1,1,2,1)", "PASS",
    "Exemplar data-scores and text unchanged apart from the rubric cell at line 509 (checked). Round-2 blind scores were within one on every criterion (B: 4,3,3,3,2 vs 4,4,3,3,3; A: exact). Note (not a fail): exemplar B's C2 level-4 annotation says the note states 'its gap from zero'; the note states each net (166, 480, 3), which is the gap from zero, so the annotation holds. Exemplar A's C4 annotation says 'without naming the input' while its text names the discount factor; the level-2 score stands.")
row("fc2d-r2-spec-questions", "2.6 spec completeness (questions a competent student would need to ask)",
    "project.html:297-316", "PASS",
    "Re-read the specification. Open points, none blocking: whether convexity_violations indices are zero-based (line 300 says only 'interior indices, in increasing order'); the strike_cents of a convexity record (the middle strike, shown in Lab 1 output, not stated in words); which named condition wins when two fail; empty and one-strike chains (one strike is valid per the tests); bool and float inputs (unspecified, untested).")
row("fc2d-r2-grader-messages", "2.6 item 4: failure messages name the property and never leak the answer",
    "grader/test_project.py (every assert message); grader/reference.py:24-47", "PASS",
    "Read every assert message in test_project.py (139-875). Messages name the property ('the list must hold every interior strike whose call lies above the chord of its neighbours'). --assert=plain prints only the message. The ValueError messages in reference.py name their condition.")
row("fc2d-r2-grader-named-conditions-only", "2.6 tests demand an exception type only for named conditions",
    "grader/test_project.py (pytest.raises sites)", "PASS",
    "Every pytest.raises(ValueError) (lines 283-298, 301-306, 437-475, 489-526, 531-561) is for a condition named in project.html:309-315 (strictly increasing or positive strikes, df_ppm range, lengths, non-negative cost). No type is required for booleans, floats or other inputs.")
row("fc2d-r2-instances", "2.6 autograder item 2: instances valid, answers change across seeds",
    "grader/instance.py; grader/test_project.py", "PASS",
    f"Generator output identical to c737272f for seeds 0..999 ({IND}/instance_compare.out: '0 []'). The changed docstring is checked in row fc2d-r3-instance-docstring-bounds. Planted kinds over seeds 0..999: convexity 341, parity 341, none 318 ({IND}/instance_bounds.out). Clean-draw convexity violations 0; parity residual on non-planted strikes at most 0.4995 cent (instance_bounds_wide.out, 20000 seeds); no half-cent exact gap (rejection rule holds).")
row("fc2d-r2-grader-over-constraint-case", "2.6 autograder items 1/3: correct alternatives pass with case-insensitive rule names",
    "course/modules/FC/FC2/grader/test_project.py:587-597 (test_scan_explanations_are_nonempty_and_name_the_rule)", "PASS",
    f"Round-2 FAIL fixed: line 594 now uses re.search(rf'\\b{{rule}}', text, re.IGNORECASE). {IND}/alts_run.out: alt_1_decimal, alt_2_integer and alt_4_lagrange pass seeds 0..49 with 91 of 91 checks; alt_3 and alt_5 (which write 'Convexity' and 'convexity' in other forms) fail only the trade-wording test below, not this one.")
row("fc2d-r2-grader-over-constraint-trade-verb", "2.6 autograder items 1/3: correct alternatives must pass (explanation wording)",
    "course/modules/FC/FC2/grader/test_project.py:615-648 (test_parity_explanation_states_the_trade_for_the_sign_of_the_gap; _SELL_CALL/_BUY_CALL/_RICH/_CHEAP at 604-607)", "FAIL",
    f"{IND}/alts_run.out and {IND}/alts/alt_3_slopes_expensive.py: its parity explanation for a positive gap says 'the call is expensive against the synthetic forward, so write the call and buy the put and the underlying'; it fails test_parity_explanation_states_the_trade_for_the_sign_of_the_gap on 50 of 50 seeds. {IND}/alts/alt_5_strict_wording.py states the rule and labels only ('P1 European exercise ... P6 cost: the parity gap is outside the no-arbitrage band'), and fails the same test on 50 of 50 seeds. Both are correct under project.html:301, which requires only that the explanation name the rule and the labels; project.html:336 states the meaning of the sign, not the wording of an explanation. The rich/cheap wording accepted at a007712f does not cover expensive, dear, write, or no-trade-wording explanations.",
    fix="Either delete the wording assertion (the spec does not require the trade in the explanation; the rubric and the label checks remain), or write the requirement into project.html:301 and accept the synonyms write, expensive, overpriced, underpriced, dear, as well as sell, short, rich, buy, long, cheap. Re-run ledgers/FC2/scripts/FC2-d-r3/ind/run_alts.sh: all five alternatives must report 50 pass seeds.")
row("fc2d-r2-alternatives-pass", "2.6 five alternative correct implementations pass seeds 0..49",
    f"{IND}/alts/alt_1_decimal.py .. alt_5_strict_wording.py (archived); {IND}/run_alts.sh; {IND}/alts_run.out", "FAIL",
    "Results: alt_1_decimal PASS 50/50 (91 checks each); alt_2_integer PASS 50/50; alt_4_lagrange PASS 50/50; alt_3_slopes_expensive FAIL 50/50 (one test: the trade-wording test); alt_5_strict_wording FAIL 50/50 (the same one test). Every other check passes for alt_3 and alt_5. The alternatives are correct under the spec (they use exact or integer arithmetic, the spec's rounding rule and the spec's named conditions). No alternative with exact arithmetic failed a numerical check.",
    fix="Fix the trade-wording test as stated in row fc2d-r2-grader-over-constraint-trade-verb, then re-run run_alts.sh: all five alternatives must pass seeds 0..49. The float alternative of plan 5.6(3) is not counted: project.html:308 requires exact fractions, and the hand-built tie tests (test_project.py:260-278, 757-784) correctly fail a float computation.")
row("fc2d-r2-mut-r7-docstrings", "2.6 mutants carry a one-line docstring (mutate_graders prints it)",
    "ledgers/FC2/mutants/r7_a_duplicate_strikes_accepted.py; r7_b_parity_loop_skips_last_strike.py; r7_c_discounted_strike_floored.py", "PASS",
    f"Round-2 FAIL fixed: ast.get_docstring is non-empty for r7_a..c, and {IND}/mutate_graders_r3x.out prints their descriptions (no '(no description)' line in the output).")
row("fc2d-r2-mut-new-killed", "2.6 round-2 new mutants v07..v10 killed",
    "ledgers/FC2/mutants/v07_..v10_ (4 files)", "PASS", f"{IND}/mutate_graders_r3x.out: v07, v08, v09, v10 each KILLED on seed 0 or 1.")
row("fc2d-r2-mut-r5d-resolved", "2.6 round-1 survivor r5_d killed",
    "ledgers/FC2/mutants/r5_d_explanation_direction_reversed.py", "PASS",
    f"{IND}/mutate_graders_r3x.out: 'KILLED r5_d_explanation_direction_reversed.py ... -> test_parity_explanation_states_the_trade_for_the_sign_of_the_gap (seed 0)'. The kill now depends on the trade-wording test that is FAILed above; the mutant itself is a valid student error.")
row("fc2d-r2-mut-equivalents", "2.6 no equivalent mutant in the set",
    "ledgers/FC2/mutants/ (63 files)", "PASS",
    f"{IND}/mutate_graders_r3x.out: 63 of 63 KILLED on seeds 0..9; a killed mutant is not equivalent to the reference.")
row("fc2d-r2-cards-full-scan", "2.7/2.8 cards: unique ids, fronts and backs; no duplicate; near-duplicate review",
    "course/modules/FC/FC2/cards.json (146 cards)", "PASS",
    f"Re-run this round: 146 cards, 0 duplicate ids (python -I scan), and difflib pairs with front ratio >= 0.6 or back ratio >= 0.6 reviewed: c003 vs c139, c136 vs c137 and c148, c012 vs c045, c013 vs c147, c057 vs c135 ask different questions with different claims. Id gaps (c031, c077 predate round 2) remain an observation, not a fail.")
row("fc2d-r2-cards-refs-numbers", "2.7 every card number appears in its lesson; every named label resolves",
    f"course/modules/FC/FC2/cards.json; L01-L08.html; {IND}/cards_numbers.out", "PASS",
    f"{IND}/cards_numbers.py over 146 cards: one literal miss, c100 '1/2' in L07 Lemma 1.1, which the lesson writes as \\tfrac12 (rendered '1/2' in the card: a faithful rendering, read in L07 text line 26). Eleven label references (for example 'Problem E2', 'Problem E3', 'Problem M1') are headings written as 'E2 · ...' in the lesson (L01 line 221 for E2), so they resolve.")
row("fc2d-r2-cards-lab-numbers", "2.7 card numbers that come from a lab agree with the lab output",
    f"cards c012, c013, c095, c147, c148 and the lab twins; {IND}/twin_lab-FC2-L01-1.out, twin_lab-FC2-L06-1.out", "PASS",
    "Lab output read this round: L01 twin prints 'arbitrage portfolios with holdings in the box: 30' (Part B) and first zero-cost portfolio (bond, stock) = (-5, 9), cost 0 (c147, c013); BOX = range(-10, 11) (lesson line 76). L06 twin prints 'time-0 holdings: shares 3/4, bond -30, cost 45', 'path uu/ud/du/dd ... True', 'self-financing strategy reproduces every node value and every payoff: True' (c095, c148). c012: Part B stock 1/2, bond 9/10 (lesson line 135 of the dump).")
row("fc2d-r2-card-c010", "2.7 card FC2-c010 agrees with the current lesson text",
    "course/modules/FC/FC2/cards.json FC2-c010; L01.html (text line 185)", "PASS",
    "Re-verified (object changed at a007712f). L01 text: 'the state prices are 1/20 and 17/20, which add to 9/10, the price of the bond ... this lesson assigns no probabilities to the states. Problem P3 makes the sum explicit.' The card's back matches; basis 'Problem P3 (exact)' is right.")
row("fc2d-r2-card-c132", "2.7 card FC2-c132 agrees with L05 Theorem 4.1 and Remark 4.2",
    "cards.json FC2-c132; L05.html Theorem 4.1 (text line 198-199), Remark 4.2 (204-205), 218", "PASS",
    "Re-verified (object changed). Theorem 4.1: 'Under A1, A2, A3, A4, A5 and (N), with r >= 0, an American call and a European call ... have the same price at date 0'; Remark 4.2: 'proved at date 0 only ... does not prove the equality at a date t > 0'; L05 line 218: 'this lesson proves no rule for holding against exercising at a later date (Remark 4.2)'. The card matches; grade T is supported by the proof on the page.")
for cid, rid in [("FC2-c020", "fc2d-r2-card-c020"), ("FC2-c030", "fc2d-r2-card-c030"), ("FC2-c041", "fc2d-r2-card-c041"),
                 ("FC2-c051", "fc2d-r2-card-c051"), ("FC2-c061", "fc2d-r2-card-c061"), ("FC2-c071", "fc2d-r2-card-c071"),
                 ("FC2-c082", "fc2d-r2-card-c082"), ("FC2-c092", "fc2d-r2-card-c092"), ("FC2-c102", "fc2d-r2-card-c102"),
                 ("FC2-c112", "fc2d-r2-card-c112"), ("FC2-c120", "fc2d-r2-card-c120"), ("FC2-c142", "fc2d-r2-card-c142")]:
    row(rid, f"2.7 card {cid} agrees with its lesson passage",
        f"course/modules/FC/FC2/cards.json {cid}", "PASS",
        CARD.format(id=cid) + " The round-2 evidence for this card (the cited lesson passage, read in the round-2 checkout) is unchanged.")

# ---- round 3 rows ----
row("fc2d-r3-instance-docstring-bounds", "2.6 instance.py docstring claim: no generated chain has a quote that breaks Theorem 2.2",
    "course/modules/FC/FC2/grader/instance.py:13-18 (docstring) vs :47-60 (_within_bounds, half-cent tolerance) and test_project.py:849-865", "FAIL",
    f"Docstring line 17-18: 'A draw is also rejected when any quote breaks the model-free bounds of Lesson 5, Theorem 2.2, so no generated chain contains a quote that the lessons define as a violation.' The code (instance.py lines 47-60 and its own docstring line 48) accepts a quote up to half a cent outside the bounds, and test_project.py:849-865 checks the bounds with the same -1/2 tolerance. So the rejection rule does not enforce the claim. Measured: no quote is strictly outside the bounds for seeds 0..19999 ({IND}/instance_bounds_wide.out), so the claim holds empirically but is not what the code guarantees. Changed at a007712f only in the docstring (lines 13-18); the code is byte-identical in behaviour (instance_compare.out).",
    fix="State the tolerance where the rule is stated: 'A draw is also rejected when a quote lies more than half a cent outside the bounds of Lesson 5, Theorem 2.2 (a quote within half a cent of a bound is kept, and none did so for seeds 0 to 19999)'; or make _within_bounds exact (Fraction comparison with no half-cent allowance), re-run instance_compare and the 50-seed suite, and drop the tolerance from the test. Severity low (no suite result changes on seeds 0..49).")
row("fc2d-r3-scope-changed-hunks", "2.2/2.6/2.7 every hunk changed since the round-2 pin is read",
    "project.html 289 and 509; grader/instance.py 13-18; grader/test_project.py 591-648; cards.json c003, c010, c012, c019, c095, c098, c132, c146-c148", "PASS",
    "git diff c737272f a007712f over the slice (4 files of course/modules/FC/FC2 plus cards.json; lessons L01-L08, index.html, labs twins, references, notation, curriculum, the FC2 plan and open items, and course/assets/js are byte-identical (git diff empty)). Each hunk read: project.html 289 (adds the link to #conventions, which exists at line 325), 509 (rubric C2 level 2, checked above); test_project.py 591-648 (case-insensitive rule name; the trade-wording change, FAILed above); instance.py docstring (checked above); cards (checked above).")
row("fc2d-r3-df-ppm-link", "2.9 link added to df_ppm input description (project.html 289)",
    "course/modules/FC/FC2/project.html:289; anchor id 'conventions' at line 325", "PASS",
    "href='#conventions' resolves to <h3 id=\"conventions\"> (project.html line 325). The P4 label it points to is defined there (line 331).")
row("fc2d-r3-mut-new-killed", "2.6 new student-error mutants of the verifier (at least three, each with a docstring)",
    "ledgers/FC2/mutants/q3_a_df_rounded_to_four_places.py, q3_b_gross_tie_toward_zero.py, q3_c_convexity_charges_two_legs.py, q3_d_convexity_explanation_omits_P5.py", "PASS",
    f"{IND}/mutate_graders_r3x.out: q3_a KILLED by test_parity_gap_matches_exact_rounding_second_chain[1]; q3_b by test_half_cent_gross_rounds_once_up; q3_c by test_scan_matches_exhaustive_oracle_second_chain; q3_d by test_scan_explanations_are_nonempty_and_name_the_rule (seed 0). Each mutant is the reference with one named student error (its docstring line 1).")
row("fc2d-r3-mut-prior-untracked", "2.6 mutants found untracked in the checkout (r3_a..r3_d, written by an earlier round-3 pass in this checkout) re-run",
    "ledgers/FC2/mutants/r3_a_half_spread_halved_again.py; r3_b_puts_longer_than_strikes_accepted.py; r3_c_net_field_reports_gross.py; r3_d_parity_explanation_names_P5_for_P4.py", "PASS",
    f"Not authored by this verifier and not in the pinned commit; kept and re-run in the gate, all KILLED ({IND}/mutate_graders_r3x.out). The fragment at ledgers/FC2/FC2-d.json (modified, uncommitted) that they came with was not relied on.")
row("fc2d-r3-footer-no-upload", "2.9 page footer and autograder text: nothing the learner writes leaves the browser",
    "project.html:671 footer; project.html:285 ('Nothing on this page uploads a file'); course/assets/js/grader.js:18", "PASS",
    "The only network calls in grader.js and py-worker.js are GETs of the grader's own files and the vendored Pyodide (grader.js line 18; py-worker.js line 3, 'nothing is fetched'). No POST or upload of the scanner source. The claim is consistent with the code (static read; no browser run).")
row("fc2d-r3-exemplar-scores-match-text", "2.6 rubric exemplars: scores agree with the annotations",
    "project.html:520-634 (exemplar A data-scores 2,1,1,2,1; exemplar B 4,4,3,3,3)", "PASS",
    "Each annotation (meets/misses with level) was compared with its passage. Exemplar B's C5 (level 3) and C3 (level 3) follow its own misses; exemplar A's C2 (1), C3 (1), C5 (1) follow its passages. The two annotation wordings noted in row fc2d-r2-rubric-calibration are not score errors.")

# ---- mutants (parsed from the gate output) ----
mutants = []
for line in (ROOT / IND / "mutate_graders_r3x.out").read_text(encoding="utf-8").splitlines():
    m = re.match(r"^(KILLED|SURVIVED) (\S+?)\.py: (.*) -> (.*)$", line)
    if m:
        status, name, desc, killed = m.groups()
        mutants.append({"id": name, "description": desc, "file": f"ledgers/FC2/mutants/{name}.py",
                        "killed_by": killed if status == "KILLED" else None})

surv = [m for m in mutants if not m["killed_by"]]
frag = {
    "unit": "FC2",
    "slice": "FC2-d",
    "round": 3,
    "verifier": "Claude Haiku 5.5, independent verifier for FC2-d round 3 (did not build FC2)",
    "pin": "a007712fdbfc8b4851123f4de76b5310ac5a9e64",
    "base": "c737272f (round-2 pin); delta inside the slice: project.html 289 and 509; grader/instance.py docstring 13-18; grader/test_project.py 591-648; cards.json c003, c010, c012, c019, c095, c098, c132 changed and c146-c148 added; mutants r7_a..c docstrings and v07..v10 added at a007712f",
    "checkout": str(ROOT),
    "scratch": "/tmp/fc2d-r3-ind (alternative runs, starter, instance bounds, card and lab checks); none of the evidence rests on scratch files alone: each scratch result is reproduced by a script archived under ledgers/FC2/scripts/FC2-d-r3/ind/",
    "verified_at": "2026-11-03T09:10:00+00:00",
    "verdict": "FAIL" if any(r["status"] != "PASS" for r in rows) else "PASS",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "Round 3 on a007712f. Read in full at a007712f: project.html (673 lines), grader/reference.py, instance.py, starter.py, "
        "test_project.py (875 lines), cards.json (1044 lines, 146 cards), the three project lab twins; the lesson texts "
        "(L01, L02, L05, L06, L07 as text dumps) read where the changed or cited cards point. Round-2 rows whose subject did not change are carried or re-run; "
        "rows whose subject changed were re-verified from scratch. Checkout state on arrival: ledgers/FC2/FC2-d.json modified and four untracked mutants (r3_a..d) and an "
        "FC2-d-r3 scripts folder were already present from an earlier round-3 pass in this checkout; this verifier did not rely on that fragment or its PASS rows, re-ran every mutant, and overwrote ledgers/FC2/FC2-d.json. "
        "No source, test, lesson, reference, curriculum, plan or JS file was edited; no commit. "
        "Observations (not fails): plans/FC2-open-items.md still lists bid-ask-spread as a DAG_DEFECT, but FC2 now lists FC1 as a prerequisite; "
        "the spec and the test count (91) hold for every seed 0..49; the instance generator's six-strike design means multi-finding ordering is exercised only by hand-built chains. "
        "Not checked: the browser autograder panel and the self-assessment form (no browser run; static read of grader.js only); the full repo gate outside the slice (tests/ other than the listed files, render_curriculum, build_site --check, fetch_data --check); "
        "the lesson pages L01-L08 line by line (unchanged since c737272f, read only where cards point); the full pytest suite; live verify_refs for the whole registry (FC2 entries only, which the rules require); the float alternative from plan 5.6(3) (not counted, as explained)."
    ),
    "summary": (
        f"FC2-d round 3 on a007712f (round-2 pin c737272f): verdict FAIL. {len(rows)} rows: "
        f"{sum(r['status']=='PASS' for r in rows)} PASS, {sum(r['status']=='FAIL' for r in rows)} FAIL, 0 UNVERIFIABLE. "
        f"Mutants: {len(mutants)} in ledgers/FC2/mutants, {len(mutants)-len(surv)} KILLED, {len(surv)} surviving. "
        "Blocking FAILs: (1) fc2d-r2-grader-over-constraint-trade-verb: the explanation-wording assertion rejects two correct alternatives (50 of 50 seeds each); "
        "(2) fc2d-r2-alternatives-pass: 3 of 5 alternatives pass, consequence of (1); "
        "(3) fc2d-r2-scope-curriculum-brief: the curriculum brief still says 'embedded option-chain snapshot' against the binding SIMULATED decision (architect action); "
        "(4) fc2d-r3-instance-docstring-bounds: docstring claims a rejection rule the code does not enforce (half-cent tolerance; low severity)."
    ),
}
out = ROOT / "ledgers/FC2/FC2-d.json"
out.write_text(json.dumps(frag, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("rows", len(rows), "statuses", {s: sum(r["status"] == s for r in rows) for s in ("PASS", "FAIL")}, "mutants", len(mutants), "surviving", len(surv))
