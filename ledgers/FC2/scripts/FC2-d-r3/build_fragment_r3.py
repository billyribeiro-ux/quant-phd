import json, re, pathlib, sys
ROOT = pathlib.Path(sys.argv[1])
S = "ledgers/FC2/scripts/FC2-d-r3"
D = f"{S}"
C = "Carried from round 2"
rows = []
def row(id_, check, location, status, evidence, fix=None):
    r = {"id": id_, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    rows.append(r)

# ---- gates (run this round on a007712f) ----
row("fc2d-r2-gate-mutate", "2.6 mutation gate: tools/mutate_graders.py --unit FC2 --seeds 0-9",
    "tools/mutate_graders.py; ledgers/FC2/mutants/ (59 files)", "PASS",
    f"{D}/mutate_graders_with_r3.out: 59 KILLED lines, 'mutate_graders FC2: PASS (59/59 killed)', rc=0 (run this round). "
    "The 55 prior mutants and the 4 new r3_a..d are all killed at seed 0 or 1.")
row("fc2d-r2-gate-run-graders", "2.6 run_graders --unit FC2 --seeds 0-49 on reference.py",
    "tools/run_graders.py; course/modules/FC/FC2/grader/", "PASS",
    f"{D}/run_graders.out: 'run_graders FC2: PASS (reference 50/50 seeds, slowest 0.3 s)', rc=0.")
row("fc2d-r2-gate-check-projects", "tools/check_projects.py --unit FC2 and --all",
    "tools/check_projects.py", "PASS",
    f"{D}/check_projects_unit.out: 'check_projects FC2: PASS', rc=0; {D}/check_projects_all.out: 'check_projects FC2: PASS', rc=0.")
row("fc2d-r2-gate-check-dag", "2.9 tools/check_dag.py --unit FC2 (and --all)",
    "tools/check_dag.py", "PASS",
    f"{D}/check_dag.out: 'check_dag FC2: PASS', rc=0; {D}/check_dag_all.out rc=0.")
row("fc2d-r2-gate-check-pages", "2.9 tools/check_pages.py --all",
    "tools/check_pages.py", "PASS",
    f"{D}/check_pages_all.out: 'check_pages FC2: PASS' among all units, rc=0 (the --all form; no unit-only run was used).")
row("fc2d-r2-gate-run-labs", "2.5 run_labs --unit FC2 --page project",
    "tools/run_labs.py; project.html lab-FC2-project-1..3", "PASS",
    f"{D}/run_labs_project.out: 'run_labs FC2: PASS (3/3)', rc=0.")
row("fc2d-r2-lab-twins-isolated", "2.5 twins alone under python -I -W error",
    "tests/labs/FC2/lab-FC2-L01-1.py .. lab-FC2-project-3.py (11 twins)", "PASS",
    f"Run this round: .venv/bin/python -I -W error on each of the 11 twins, rc=0 for all (outputs {D}/out_lab-FC2-*.out).")
row("fc2d-r2-lab-page-equals-twin", "2.5 page code equals twin; expected block equals output",
    "course/modules/FC/FC2/project.html lines 56-146, 169-257, 378-485", "PASS",
    f"{C} (project.html lines 56-146, 169-257, 378-485 and tests/labs/FC2/ byte-identical since c737272f; the only project.html hunks are at lines 289 and 509). "
    f"Re-run this round: run_labs FC2 project 3/3 ({D}/run_labs_project.out), which compares the expected block with the printed output.")
row("fc2d-r2-gate-page-smoke", "2.9 tools/page_smoke.py --unit FC2 --pages project (alone)",
    "tools/page_smoke.py", "PASS",
    f"{D}/page_smoke_project.out: 'page_smoke modules/FC/FC2/project.html: PASS', 'in-browser grader: All 91 tests pass on seed 1231039859', 'package preload', rc=0 (run this round, alone).")
row("fc2d-r2-gate-ruff-mypy", "ruff check, ruff format --check, mypy --no-incremental, mypy --strict on grader",
    "tests/labs/FC2; course/modules/FC/FC2/grader", "PASS",
    f"{D}/ruff_check.out 'All checks passed!', rc=0; {D}/ruff_format.out '15 files already formatted', rc=0; {D}/mypy_default.out 'Success: no issues found in 331 source files', rc=0; "
    f"{D}/mypy_labs.out 'Success: no issues found in 11 source files', rc=0; {D}/mypy_grader_strict_r3.out (mypy --strict on test_project.py, instance.py and reference.py as scanner.py in a scratch copy), 'Success: no issues found in 3 source files', rc=0.")
row("fc2d-r2-gate-pytest-fc2", "relevant pytest (FC2 filter; labs, run_labs, page checks, refs)",
    "tests/", "PASS",
    f"{D}/pytest_fc2.out: 'pytest tests -k FC2' rc=0 (12 selected, passed); {D}/pytest_relevant.out: tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py tests/test_refs.py rc=0, all passed. "
    "The round-2 count (321 passed) used a different selection and is not compared.")
row("fc2d-r2-gate-verify-refs", "2.1 verify_refs (offline whole registry; live FC2 entries)",
    "tools/verify_refs.py; references/references.json", "PASS",
    f"Run this round: {D}/verify_refs_offline.out 'offline integrity: 560 entries, 0 problems', rc=0. The live FC2 entries are {C}: references/ is byte-identical since c737272f (git diff empty); no live run was made this round (see notes).")

# ---- mutants ----
row("fc2d-r2-mut-r7-docstrings", "2.6 mutant format: each mutant opens with a one-line docstring describing the error",
    "ledgers/FC2/mutants/r7_a_duplicate_strikes_accepted.py; r7_b_parity_loop_skips_last_strike.py; r7_c_discounted_strike_floored.py", "PASS",
    f"{D}/mutate_graders_with_r3.out prints the docstring first line for every mutant and contains no '(no description)' (grep count 0). "
    "r7_a/b/c now open with '\"\"\"Student error: ...' docstrings and are KILLED (seed 0).")
row("fc2d-r2-mut-new-killed", "2.6 new v07-v10 mutants are killed",
    "ledgers/FC2/mutants/v07_convexity_indices_returned_in_decreasing_order.py; v08; v09; v10", "PASS",
    f"{D}/mutate_graders_with_r3.out: v07 KILLED by test_convexity_matches_oracle_on_an_uneven_grid (seed 0); v08 by test_convexity_finding_with_net_one_cent_is_returned (seed 0); v09 by test_scan_explanations_are_nonempty_and_name_the_rule (seed 1); v10 by test_convexity_half_cent_tie_rounds_once_up_at_any_discount_factor (seed 0).")
row("fc2d-r2-mut-r5d-resolved", "2.6 round-1 survivor r5_d is killed",
    "ledgers/FC2/mutants/r5_d_explanation_direction_reversed.py; course/modules/FC/FC2/grader/test_project.py:615-649", "PASS",
    f"{D}/mutate_graders_with_r3.out: r5_d KILLED by test_parity_explanation_states_the_trade_for_the_sign_of_the_gap (seed 0). The relaxed check proposed below in a scratch copy still kills r5_d (seed 0,1,2: 1 failed).")
row("fc2d-r2-mut-equivalents", "2.6 no surviving mutant (an equivalent mutant could not be killed)",
    "ledgers/FC2/mutants/", "PASS",
    f"{D}/mutate_graders_with_r3.out: 59/59 KILLED, so no mutant in the set survives and none is an unkilled equivalent.")
row("fc2d-r3-mut-new-killed", "2.6 four new student-error mutants of the verifier (r3_a..d)",
    "ledgers/FC2/mutants/r3_a_half_spread_halved_again.py; r3_b_puts_longer_than_strikes_accepted.py; r3_c_net_field_reports_gross.py; r3_d_parity_explanation_names_P5_for_P4.py", "PASS",
    f"{D}/mutate_graders_with_r3.out: r3_a KILLED by test_scan_matches_exhaustive_oracle_second_chain (seed 0); r3_b by test_puts_longer_than_strikes_is_rejected (seed 0); r3_c by test_scan_matches_exhaustive_oracle_second_chain (seed 0); r3_d by test_scan_explanations_are_nonempty_and_name_the_rule (seed 1). Each is one change against reference.py (diff in the session).")

# ---- starter, collect, numbers ----
row("fc2d-r2-starter-suite-fails", "2.6 the suite fails on the starter file",
    "course/modules/FC/FC2/grader/starter.py; project.html line 297", "PASS",
    f"Run this round: starter.py as scanner.py, seed 0: '83 failed, 8 passed' ({D}/starter_suite_r3.out). Each stub raises NotImplementedError (starter.py:19, 24, 29).")
row("fc2d-r2-collect-count", "page's collected-check count equals pytest --collect-only on the reference",
    "course/modules/FC/FC2/project.html line 320; grader/test_project.py", "PASS",
    f"{D}/collect_count_r3.out: 91 for each of seeds 0..49 (run this round with reference.py as scanner.py). The page states 91 at project.html:320. The changed test_project.py hunk adds helpers and no test function.")
row("fc2d-r2-numbers-lab1", "numbers in prose match Lab 1 output",
    "course/modules/FC/FC2/project.html:55-163", "PASS",
    f"{C} (project.html:55-163 byte-identical since c737272f). Lab output re-run this round (run_labs 3/3).")
row("fc2d-r2-numbers-lab3", "numbers in prose match Lab 3 output",
    "course/modules/FC/FC2/project.html:376-486", "PASS",
    f"{C} (project.html:376-486 byte-identical since c737272f).")
row("fc2d-r2-numbers-exemplars", "exemplar numbers and passages",
    "course/modules/FC/FC2/project.html:520-634", "PASS",
    f"{C} (project.html:520-634 byte-identical since c737272f). The level-2 wording change at line 509 does not touch the exemplars: exemplar A scores C2 1 and exemplar B scores C2 4 (data-scores at lines 520-634).")
row("fc2d-r2-hours", "hours arithmetic: hub split versus lesson hours",
    "course/modules/FC/FC2/project.html:33,35,339-356; course/modules/FC/FC2/index.html:31-41", "PASS",
    f"{C} (those lines and index.html are byte-identical since c737272f; the delta hunks are at project.html 289 and 509).")
row("fc2d-r2-banned-phrases", "2.9 banned phrases and process words absent from learner text",
    "project.html; cards.json; grader/*.py; lab-FC2-project-1..3.py", "PASS",
    f"Re-run this round over the changed and touched files: {D}/banned_scan_r3.py -> {D}/banned_scan_r3.out, 4 hits, all 'R[0-9]' matches inside card text (Problem R1 and r-variables in cards.json lines 213, 215, 510, 557), none a banned string or process word.")
row("fc2d-r2-notation", "notation: every symbol matches notation/notation.json",
    "notation/notation.json; project.html formulas lines 85-88, 335-336", "PASS",
    f"{C}: notation/ byte-identical since c737272f; the formula lines are unchanged; the new text adds no symbol (checked in the changed cards and the df_ppm sentence).")
row("fc2d-r2-dag", "2.9 DAG: concepts used by name or link are in the prerequisite closure",
    "course/modules/FC/FC2/project.html:37,333; curriculum/02-economics-finance-core.yaml:396-416", "PASS",
    f"Re-run this round: check_dag FC2 PASS ({D}/check_dag.out). The curriculum file is byte-identical since c737272f; project.html:37 and 333 unchanged.")
row("fc2d-r2-reading-keys", "reading-list keys resolve",
    "course/modules/FC/FC2/project.html:654-658", "PASS",
    f"{C} (project.html:654-658 unchanged; references/ identical).")
row("fc2d-r2-autograder-panel-claims", "autograder panel description matches the code",
    "course/assets/js/grader.js:33-80; course/assets/js/py-worker.js:111", "PASS",
    f"{C} (course/assets/js/ byte-identical since c737272f). No browser visual check was made this round.")
row("fc2d-r2-hub-placement-claim", "hub placement claim matches the project page",
    "course/modules/FC/FC2/project.html:42; course/modules/FC/FC2/index.html:148", "PASS",
    f"{C} (both lines unchanged; index.html byte-identical).")
row("fc2d-r2-scope-curriculum-brief", "2.6 Rung 3 input matches the curriculum scope exactly",
    "curriculum/02-economics-finance-core.yaml:427-429 (brief); project.html:285 (Inputs)", "FAIL",
    "Still open and unchanged this delta. The curriculum brief reads 'Given an embedded option-chain snapshot, detect put–call parity and convexity violations net of a stated cost model' (curriculum/02-economics-finance-core.yaml:427-429, byte-identical since c737272f). "
    "project.html:285 reads 'No market data is embedded.' and grades on a SIMULATED chain. plans/FC2-build-plan.md:449-458 records this as B1 with the architect to decide; plans/FC2-open-items.md:7 and 518-519 keep D1 open.",
    "Architect decision (not a builder fix): either supply a redistributable option-quote snapshot with a quoted licence (DATA_REQUEST D1, then embed it and rebuild the grader instances), or amend the curriculum brief at curriculum/02-economics-finance-core.yaml:427-429 to 'a SIMULATED option chain' so the scope matches the page.")
row("fc2d-r2-rubric-C2-level2", "2.6 rubric: every level descriptor observable",
    "course/modules/FC/FC2/project.html:509 (rubric C2, level 2 cell)", "PASS",
    "Re-verified on the revised cell: 'States the cost model, but does not say, for each finding, whether it survives the cost, or reports gross amounts without the cost.' "
    "A note that says only some findings survive, without naming each, is level 2; level 3 requires 'says for each finding whether it survives the cost'. The old first clause that a correct note could meet is gone. "
    "Residual, not blocking: a note that states the cost model and reports only gross amounts sits at level 2 under this cell and at level 1 under 'costs are ignored'.")
row("fc2d-r2-rubric-calibration", "rubric calibration: exemplar scores match the descriptors",
    "course/modules/FC/FC2/project.html:520-634", "PASS",
    f"{C} (lines 520-634 byte-identical). Exemplar A (C2 1: no cost model) and exemplar B (C2 4) are not scored at level 2, so the changed C2 level-2 cell cannot change either calibration.")
row("fc2d-r2-spec-questions", "spec questions match the page spec",
    "course/modules/FC/FC2/project.html:297-316", "PASS",
    f"{C} (lines 297-316 byte-identical).")
row("fc2d-r2-grader-messages", "2.6 each named error message names its condition; assertion messages",
    "course/modules/FC/FC2/grader/test_project.py (assert messages); grader/reference.py:24-47", "PASS",
    f"Carried for the messages outside the changed hunk (test_project.py lines 591-640 changed; reference.py byte-identical). The two changed explanation assertions (test_project.py lines 593-595 and 640-648) still name their condition ('the explanation names the rule...', 'a positive gap ... must explain the trade that sells the call').")
row("fc2d-r2-grader-named-conditions-only", "2.6 tests demand ValueError only for conditions the page names",
    "course/modules/FC/FC2/grader/test_project.py:283-561", "PASS",
    f"{C} (test_project.py lines 283-561 byte-identical; the changed hunk is at 591-640).")
row("fc2d-r2-instances", "2.6 generated instances: seed determinism, label, no half-cent tie, bounds",
    "course/modules/FC/FC2/grader/instance.py; grader/test_project.py:853-860", "PASS",
    f"Re-run this round: {D}/instance_compare_r3.out: make_instance output identical to c737272f for seeds 0..999 (1000 identical, 0 differing); accepted chains 0..999 have no half-cent tie in the gaps or second differences; planted kinds parity 341, convexity 341, none 318. The module-docstring wording defect is a separate row (fc2d-r3-instance-docstring-bounds).")
row("fc2d-r2-grader-over-constraint-case", "2.6 autograder item 1/3: correct alternatives must pass (rule name, case)",
    "course/modules/FC/FC2/grader/test_project.py:587-601 (test_scan_explanations_are_nonempty_and_name_the_rule)", "PASS",
    f"Re-verified: the check is now re.search(rf\"\\b{{rule}}\", text, re.IGNORECASE) (test_project.py lines 593-595). Alternatives with 'Parity:' and 'Convexity in strike:' pass 50/50 (alt_a_decimal, alt_d_lagrange and alt_c_slopes; {D}/alt_run_r3.out: failing_seeds=0/50 each).")
row("fc2d-r2-grader-over-constraint-trade-verb", "2.6 autograder item 1/3: correct alternatives must pass (sign wording)",
    "course/modules/FC/FC2/grader/test_project.py:602-611 (_names_side) and 640-648 (test_parity_explanation_states_the_trade_for_the_sign_of_the_gap)", "FAIL",
    "The round-2 failures are fixed (alt_c 'the call is rich' and 'Short the call' forms now pass 50/50). A residual over-constraint remains. Alternative E (alt_e_wording_probe.py) writes correct explanations that contrast the richness: positive gap 'the call is rich, not cheap ... so sell the call; buy the put and the underlying' and negative gap 'the call is cheap, not rich ... so buy the call; sell the put'. "
    f"{D}/alt_run_r3.out: alt_e_wording_probe failing_seeds=50/50 on test_parity_explanation_states_the_trade_for_the_sign_of_the_gap. Cause: the negated clauses are `not _names_side(text, _BUY_CALL, _CHEAP)` and `not _names_side(text, _SELL_CALL, _RICH)`, so any occurrence of 'cheap' or 'rich' in the other sign's clause rejects the text. "
    "The docstring at test_project.py:611 says 'richness or cheapness, of the call', but _RICH and _CHEAP match 'rich' and 'cheap' about any subject (for example 'the put is rich').",
    "Negate only the trade verbs, not the wording: positive gap `_names_side(text, _SELL_CALL, _RICH) and _BUY_CALL.search(text) is None`; negative gap `_names_side(text, _BUY_CALL, _CHEAP) and _SELL_CALL.search(text) is None`. "
    f"Validated in a scratch copy only ({D} is not changed; /tmp/fc2d-r3-fixcheck): alt_e passes seeds 0-2, alt_a and reference pass seeds 0-2, and r5_d and r7_b are still killed (1 and 9 failed tests). Re-run the full alternatives set after applying it.")
row("fc2d-r2-alternatives-pass", "2.6 five alternative correct implementations pass the suite on seeds 0-49",
    f"{D}/alt/alt_a_decimal.py, alt_b_integer.py, alt_c_slopes.py, alt_d_lagrange.py, alt_e_wording_probe.py", "FAIL",
    f"Written fresh this round, independent of earlier rounds. {D}/alt_run_r3.out (seeds 0-49, one pytest run per seed): alt_a_decimal 0/50 failing, alt_b_integer 0/50, alt_c_slopes 0/50, alt_d_lagrange 0/50, reference control 0/50; alt_e_wording_probe 50/50 failing (the trade-verb row). Four of five pass.",
    "Fix the trade-verb row (the negated clauses) and re-run /Users/billyribeiro/.fanout/wt/verifyD3-FC2-d/ledgers/FC2/scripts/FC2-d-r3/alt_run_r3.sh on all five alternatives; each must show failing_seeds=0/50.")

# ---- cards ----
row("fc2d-r2-cards-full-scan", "cards: every card checked against the current lesson text; no duplicates",
    "course/modules/FC/FC2/cards.json (146 cards)", "PASS",
    f"Re-run this round: {D}/cards_scan_r3.out: 146 cards, ids FC2-c001..FC2-c148 sorted with no duplicate id, front or back; keys consistent; every lesson file present; every T card with a basis has one; the only card number not found verbatim in its lesson is FC2-c100's '1/2', which L07.html:64 and 360 writes as \\tfrac12 (same value). "
    f"Changed cards are checked one by one in the rows fc2d-r3-card-* and fc2d-r2-card-c010, c132. The other 139 card objects are byte-identical to c737272f ({D}/cards_c737272f.json vs cards_a007712f.json) and the lesson pages are byte-identical, so the round-2 card evidence carries.")
row("fc2d-r2-cards-refs-numbers", "cards: card numbers and references appear in the lesson",
    "course/modules/FC/FC2/cards.json; L01-L08.html", "PASS",
    f"Re-run this round: {D}/cards_scan_r3.out (all card numbers checked against their lesson text; only c100's '1/2' rendering noted above). The references in the changed cards (Theorem 4.1, Remark 4.2, Proposition 2.2, Example 3.4, Theorem 3.3, Problem P3, Problem E2, Section 1) are found in the lesson text (see fc2d-r3-card rows).")
row("fc2d-r2-cards-lab-numbers", "cards: lab numbers match the lab output",
    "cards c021, c023, c024, c027, c038, c045, c093, c094, c109-c111, c115-c118, c123, c133, c134, c136, c137", "PASS",
    f"{C} for every listed card (card objects byte-identical since c737272f; lab twins identical; lab outputs {D}/out_lab-FC2-*.out re-run this round). c095 is in this list and was changed; it is re-verified in fc2d-r3-card-c095.")
for cid, lab_note, cite, desc in [
    ("c020", None, "L02.html", None),
    ("c030", None, "L02.html", None),
    ("c041", None, "L03.html", None),
    ("c051", None, "L04.html", None),
    ("c061", None, "L04.html", None),
    ("c071", None, "L05.html", None),
    ("c082", None, "L06.html", None),
    ("c092", None, "L06.html", None),
    ("c102", None, "L07.html", None),
    ("c112", None, "L07.html", None),
    ("c120", None, "L08.html", None),
    ("c142", None, "L04.html", None),
]:
    row(f"fc2d-r2-card-{cid}", f"card FC2-{cid} matches the lesson",
        f"course/modules/FC/FC2/cards.json (FC2-{cid}); course/modules/FC/FC2/{cite}", "PASS",
        f"{C} (card FC2-{cid} object byte-identical to c737272f; {cite} byte-identical; cards_scan_r3 re-run: no duplicate).")
row("fc2d-r2-card-c010", "card FC2-c010 matches the lesson (changed)",
    "course/modules/FC/FC2/cards.json (FC2-c010); course/modules/FC/FC2/L01.html", "PASS",
    "Re-verified. Back: 'No. ... the state prices 1/20 and 17/20 add to 9/10 ... (Problem P3). This lesson assigns no probabilities to the states.' "
    f"L01.txt:186 (extracted text) states 'this lesson assigns no probabilities to the states'; Problem P3 at L01.txt:213-216 gives 1/20, 17/20 and sum 18/20 = 9/10; lab output {D}/out_lab-FC2-L01-1.out Part A 'state prices (state u, state d): 1/20 17/20'.")
row("fc2d-r2-card-c132", "card FC2-c132 matches the lesson (changed)",
    "course/modules/FC/FC2/cards.json (FC2-c132); course/modules/FC/FC2/L05.html", "PASS",
    "Re-verified. Front and back: Theorem 4.1 gives a price equality at date 0 only, under A1 to A5, (N) and r ≥ 0. L05.txt:199-201 states the theorem under 'A1, A2, A3, A4, A5 and (N), with r ≥ 0'; L05.txt:219 says 'at date 0 only'; Remark 4.2 at L05.txt:205-206 says no rule for holding is proved (cited as Remark 4.2).")
row("fc2d-r3-card-c003", "card FC2-c003 matches the lesson (changed)",
    "course/modules/FC/FC2/cards.json (FC2-c003); course/modules/FC/FC2/L01.html", "PASS",
    "Front 'What does Assumption A3 (no arbitrage) say?' Back 'No portfolio is an arbitrage opportunity in the market under study (Assumption A3, Section 1).' L01.txt:27 names 'Assumption A3 (no arbitrage)' and L01.txt:28 states the no-portfolio sentence. Card has no grade, so no basis is needed.")
row("fc2d-r3-card-c146", "card FC2-c146 matches the lesson (new)",
    "course/modules/FC/FC2/cards.json (FC2-c146); course/modules/FC/FC2/L01.html", "PASS",
    "Back 'No. A3 is a hypothesis about the market, and a price set can violate it (Section 1; Lab 1, Part B).' L01.txt:29 'A3 is a no-arbitrage principle: a hypothesis about a market, not a fact that this lesson establishes'; L01.txt:188 and 292-294 name Lab 1, Part B, as the violating price set. Front and back are distinct from c003 (one asks what A3 says, the other whether it is established).")
row("fc2d-r3-card-c012", "card FC2-c012 matches Lab 1 Part B (changed)",
    "course/modules/FC/FC2/cards.json (FC2-c012); tests/labs/FC2/lab-FC2-L01-1.py:18-19; project lab output", "PASS",
    f"Back '1/2, with the bond at 9/10 (Lab 1, Part B).' Lab output {D}/out_lab-FC2-L01-1.out Part B: 'bond 9/10, stock 1/2, same payoffs'. Grade T with no basis; the card states a fact the lab prints exactly.")
row("fc2d-r3-card-c147", "card FC2-c147 matches Lab 1 Part B and Problem E2 (new)",
    "course/modules/FC/FC2/cards.json (FC2-c147); tests/labs/FC2/lab-FC2-L01-1.py:18 (BOX = range(-10, 11)); L01.html Problem E2", "PASS",
    f"Back '30, with holdings from −10 to 10 of each asset. ... (Lab 1, Part B; Problem E2).' {D}/out_lab-FC2-L01-1.out: 'arbitrage portfolios with holdings in the box: 30'. The twin's BOX is range(-10, 11) (lab-FC2-L01-1.py:18). L01.txt:222-228 (E2) says 'The count 30 counts only the integer holdings from minus 10 to 10 of the two assets'. Grade T, basis 'Lab 1, Part B (exact)'; L01.txt:302 says Lab 1 is not a simulation.")
row("fc2d-r3-card-c148", "card FC2-c148 matches Lab 1 time-0 holdings (new)",
    "course/modules/FC/FC2/cards.json (FC2-c148); tests/labs/FC2/lab-FC2-L06-1.py; L06.html", "PASS",
    f"Back '3/4 share and a bond position of −30, at cost 45 currency units (Lab 1).' {D}/out_lab-FC2-L06-1.out: 'time-0 holdings: shares 3/4, bond -30, cost 45'; lab text says positions are exact fractions in currency units. Hand check: Δ = (75−0)/(150−50) = 3/4, B = 45 − 3/4·100 = −30. Duplicate check: no other card states these holdings.")
row("fc2d-r3-card-c095", "card FC2-c095 matches Lab 1 self-financing check (changed)",
    "course/modules/FC/FC2/cards.json (FC2-c095); tests/labs/FC2/lab-FC2-L06-1.py", "PASS",
    f"Back 'Yes. Lab 1 prints True for the paths uu, ud, du and dd, and it reproduces each node value.' {D}/out_lab-FC2-L06-1.out: 'path uu/ud/du/dd: ... True' and 'self-financing strategy reproduces every node value and every payoff: True'. Grade T, basis 'Lab 1 (exact)'.")
row("fc2d-r3-card-c098", "card FC2-c098 arithmetic matches Example 3.4 (changed)",
    "course/modules/FC/FC2/cards.json (FC2-c098); course/modules/FC/FC2/L06.html Example 3.4", "PASS",
    "Back: E[S_2] = 156.25 = (5/4)^2·100, discounts to S_0 = 100; payoff at 156.25 is 56.25, discounted 56.25·(4/5)^2 = 36; price 45. L06.txt:221 states the same numbers (156.25, S_0 = 100, 56.25, 36, 45). Hand check: E^Q payoff = 125·(3/4)^2 = 70.3125, discounted by (5/4)^2 gives 45. Grade T, basis 'Example 3.4 (arithmetic on the page)'.")
row("fc2d-r3-card-c019", "card FC2-c019 matches Proposition 2.2 (changed front)",
    "course/modules/FC/FC2/cards.json (FC2-c019); course/modules/FC/FC2/L02.html Proposition 2.2", "PASS",
    "Back 'F = F* = S e^{rτ} (Proposition 2.2). If F > F*, sell the forward and buy the asset with a loan; if F < F*, buy the forward, sell the asset short and lend. Each gives a zero-cost portfolio with a strictly positive payoff in every state, which A3 excludes.' L02.txt:38-43 states Proposition 2.2 under 'Assume A1 to A4' with these two cases and the A3 exclusion. Front rewording preserves the question.")
row("fc2d-r3-instance-docstring-bounds", "2.6 instance.py docstring claim matches the code's bounds check",
    "course/modules/FC/FC2/grader/instance.py:17-18 (module docstring); instance.py:47-60 (_within_bounds, half-cent tolerance)", "FAIL",
    "Module docstring: 'A draw is also rejected when any quote breaks the model-free bounds of Lesson 5, Theorem 2.2, so no generated chain contains a quote that the lessons define as a violation.' The code checks the bounds only up to half a cent (instance.py:56-59: call > spot + 1/2, call < max(spot − K df, 0) − 1/2, put < −1/2, put > K df + 1/2), and the function's own docstring says 'up to half a cent' (instance.py:48). "
    f"A quote that breaks a bound by less than half a cent is accepted, which the module sentence says cannot happen. Observed: none in 2000 accepted chains ({D}/bounds_strict_scan.out: strict violations 0), so the defect is latent, not observed.",
    "State the tolerance in the module docstring (for example 'no quote breaks a bound by more than half a cent, which is the rounding slack of the puts'), or tighten the check where the integer quotes allow it. Do not claim 'no quote the lessons define as a violation' while the code allows a half-cent band.")

# ---- form of the delta ----
row("fc2d-r3-df-ppm-link", "project.html:289 df_ppm sentence and the new #conventions link resolve",
    "course/modules/FC/FC2/project.html:289 and :325 (h3 id=conventions)", "PASS",
    "Changed sentence: 'It is supplied, not computed, so the parity check is exact (assumption P4, defined under Conventions and assumptions, below).' The anchor <h3 id=\"conventions\"> is at project.html:325, and P4 is defined in that list (line 'P4 · Supplied discount factor').")
row("fc2d-r3-scope-changed-hunks", "delta: every hunk in the FC2 slice has been read",
    f"{D}/bounds_strict_scan.py; project.html:289, 509; grader/instance.py:13-18; grader/test_project.py:591-648; cards.json (10 objects)", "PASS",
    "The round delta a007712f vs c737272f in the slice is: project.html lines 289 and 509 (2 hunks); grader/instance.py docstring lines 13-18; grader/test_project.py lines 591-648 (the explanation checks and new helpers); cards.json objects c003, c010, c012, c019, c095, c098, c132 changed and c146, c147, c148 added. Every hunk was read and is covered by a row above.")

fragment = {
    "unit": "FC2",
    "slice": "FC2-d",
    "round": 3,
    "verifier": "Claude Haiku 5.5, independent verifier for FC2-d round 3 (did not build FC2)",
    "pin": "a007712f",
    "base": "c737272f (round-2 pin); the delta is listed in notes; rows carried from round 2 are marked 'Carried from round 2'",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyD3-FC2-d",
    "scratch": "/tmp/fc2d-r3-* (alt runs, fixcheck, starter, mypy, collect, instance copies); none of the evidence depends on them except the scratch fix check, which is cited as such",
    "verified_at": "2026-11-03T03:41:05+00:00",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": "",
    "summary": "",
}
# mutants from the mutate run
out = (ROOT / S / "mutate_graders_with_r3.out").read_text(encoding="utf-8").splitlines()
pat = re.compile(r"^(KILLED|SURVIVED) (\S+)\.py: (.*) -> (.*)$")
for line in out:
    m = pat.match(line)
    if m:
        status, name, desc, killed = m.groups()
        fragment["mutants"].append({"id": name, "description": desc, "killed_by": killed if status == "KILLED" else "SURVIVED"})
pass_n = sum(1 for r in rows if r["status"] == "PASS")
fail_n = sum(1 for r in rows if r["status"] != "PASS")
fragment["summary"] = (f"FC2-d round 3 on a007712f (round-2 pin c737272f): verdict FAIL. {len(rows)} rows: {pass_n} PASS, {fail_n} FAIL, 0 UNVERIFIABLE. "
    f"Mutants: {len(fragment['mutants'])} of {len(fragment['mutants'])} killed (55 prior, 4 new r3_a..d). "
    "Blocking FAILs: (1) fc2d-r2-scope-curriculum-brief (architect decision, unchanged); (2) fc2d-r2-grader-over-constraint-trade-verb, the relaxed check still rejects a correct contrastive explanation (alt_e, 50/50), and the fix is validated in scratch only; (3) fc2d-r2-alternatives-pass (4 of 5 pass); (4) fc2d-r3-instance-docstring-bounds (module docstring claims no half-cent breach, code tolerates one; latent).")
fragment["notes"] = (
    "Round 3 on a007712f; delta from c737272f inside the slice: project.html 289 (df_ppm sentence adds a link to #conventions) and 509 (C2 level-2 cell rewritten); "
    "grader/instance.py docstring lines 13-18 (tie sentence rewritten; code unchanged, output identical for seeds 0..999); grader/test_project.py 591-648 (rule name matched case-insensitively; parity trade check accepts rich/cheap wording, with negated clauses still matching the wording); "
    "cards.json: c003, c010, c012, c019, c095, c098, c132 changed, c146, c147, c148 added (143 to 146 cards); mutants r7_a..c given docstrings, v07..v10 added, r3_a..d added by this verifier. "
    "Lessons, lab twins, references, notation, curriculum, plans and JS are byte-identical to c737272f. Round-2 rows are re-verified where the subject changed and carried (prefix 'Carried from round 2') where the cited lines or objects are byte-identical. "
    "Not checked: the live verify_refs run (offline only this round; references/ unchanged); a browser check of the autograder panel; the full repo gate (outside this slice); a full line-by-line re-read of the unchanged 99% of project.html and of the 139 unchanged card objects (carried on byte identity, not re-read this round); the 'cheap'/'rich' fix was validated only on a scratch copy and is not applied to the checkout."
)
json.dump(fragment, open(ROOT / S.replace("scripts/FC2-d-r3", "") / "ledgers/FC2/FC2-d.json" if False else ROOT / "ledgers/FC2/FC2-d.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("rows", len(rows), "pass", pass_n, "fail", fail_n, "mutants", len(fragment["mutants"]))
