"""Assemble the FC2-d round-4 fragment from the verifier's command outputs and the rows it checked.

Usage: python -I build_fragment_FC2d_r4.py <checkout> <output_json>
Mutant descriptions and killers are parsed from ledgers/FC2/scripts/FC2-d-r4/mutate_fc2_with_u4.out.
"""

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

checkout = Path(sys.argv[1]).resolve()
out_path = Path(sys.argv[2]).resolve()
S = "ledgers/FC2/scripts/FC2-d-r4"
mut_out = (checkout / S / "mutate_fc2_with_u4.out").read_text(encoding="utf-8")

mutants = []
for line in mut_out.splitlines():
    m = re.match(r"KILLED (\S+?\.py): (.*)$", line)
    if not m:
        continue
    name, rest = m.group(1), m.group(2)
    desc, _, killer = rest.partition(" -> ")
    killed_by = killer.split(" (seed")[0].strip() if killer else None
    mutants.append({"id": name[:-3], "description": desc.strip(), "file": f"ledgers/FC2/mutants/{name}",
                    "killed_by": killed_by or "NONE"})
assert len(mutants) == 65, len(mutants)
assert all(m["killed_by"] != "NONE" for m in mutants)

CARRY = "Carried from round 3 (course/modules/FC/FC2/cards.json object and its lesson text byte-identical since the previous pin a007712f; the round-4 delta changed only c093, c123, c124, c149-c153): "
CARRY_J = "Carried from round 3 (course/assets/js byte-identical since a007712f; git diff --quiet a007712f 4eb6788f -- course/assets/js is empty): "

rows = [
 # gates, re-run on 4eb6788
 ("fc2d-r2-gate-mutate", "2.6", "tools/mutate_graders.py --unit FC2 --seeds 0-9", "ledgers/FC2/mutants/ (65 files)", "PASS",
  f"Command: .venv/bin/python tools/mutate_graders.py --unit FC2 --seeds 0-9, rc=0, output {S}/mutate_fc2_with_u4.out: 'mutate_graders FC2: PASS (65/65 killed)'. 62 prior mutants plus u4_a..u4_c (three new student-error mutants written this round). Mutant r5_d no longer exists (see fc2d-r2-mut-r5d-resolved)."),
 ("fc2d-r2-gate-run-graders", "2.5/2.6", "tools/run_graders.py --unit FC2 --seeds 0-49", "course/modules/FC/FC2/grader/", "PASS",
  f"Command: run_graders.py --unit FC2 --seeds 0-49, rc=0, {S}/run_graders.out: 'run_graders FC2: PASS (reference 50/50 seeds, slowest 0.2 s)'. Includes the typecheck of reference, starter and instance and the starter-fails check."),
 ("fc2d-r2-gate-check-projects", "2.6", "tools/check_projects.py --unit FC2 and --all", "tools/check_projects.py", "PASS",
  f"{S}/gates_a.out: 'check_projects FC2: PASS' and 'check_projects FC2: PASS' in the --all run (21 units PASS)."),
 ("fc2d-r2-gate-check-dag", "2.9", "tools/check_dag.py --all (FC2 line)", "tools/check_dag.py", "PASS",
  f"{S}/gates_a.out: 'check_dag FC2: PASS' (--all, 21 units)."),
 ("fc2d-r2-gate-check-pages", "2.9", "tools/check_pages.py --all", "tools/check_pages.py", "PASS",
  f"{S}/gates_a.out: 'check_pages FC2: PASS', rc=0 for the --all run (21 units PASS)."),
 ("fc2d-r2-gate-run-labs", "2.5", "tools/run_labs.py --unit FC2", "course/modules/FC/FC2/project.html lab-FC2-project-1..3", "PASS",
  f"Command: run_labs.py --unit FC2, rc=0, {S}/run_labs_fc2.out: 'run_labs FC2: PASS (11/11)'."),
 ("fc2d-r2-lab-twins-isolated", "2.5", "project twins alone under python -I -W error", "tests/labs/FC2/lab-FC2-project-1.py, -2.py, -3.py", "PASS",
  f"{S}/twins_isolated.out: each twin copied alone into an empty temp directory and run with python -I -W error: 'twin 1 rc=0 stderr_bytes=0', 'twin 2 rc=0 stderr_bytes=0', 'twin 3 rc=0 stderr_bytes=0'."),
 ("fc2d-r2-lab-page-equals-twin", "2.5", "page code equals twin; expected block equals output", "course/modules/FC/FC2/project.html lines 56-146, 169-257, 378-468 (expected blocks 147-162, 258-273, 469-485)", "PASS",
  f"run_labs --unit FC2 checks byte identity of each page lab to its twin and the expected block to the twin output (see fc2d-r2-gate-run-labs, 11/11 PASS). The round-4 delta does not touch those line ranges (hunks at project.html 297, 317, 483, 496 only)."),
 ("fc2d-r2-gate-page-smoke", "2.9", "tools/page_smoke.py --unit FC2 --pages project", "course/modules/FC/FC2/project.html", "PASS",
  f"{S}/page_smoke_project.out: 'page_smoke modules/FC/FC2/project.html: PASS', 'in-browser grader: All 90 tests pass on seed 488384069', labs 1-3 timed. Note: the first attempt used --pages project.html, which matches no page stem and printed a vacuous PASS; it was discarded and the run repeated with --pages project."),
 ("fc2d-r2-gate-ruff-mypy", "2.6", "ruff check, ruff format --check, mypy --no-incremental", "tests/labs/FC2; course/modules/FC/FC2/grader", "PASS",
  f"{S}/ruff_check.out 'All checks passed!'; {S}/ruff_format.out '15 files already formatted'; {S}/mypy_labs.out 'Success: no issues found in 11 source files' (mypy --no-incremental tests/labs/FC2); {S}/mypy_grader_strict_scratch.out 'Success: no issues found in 3 source files' (mypy --strict on scanner.py=reference.py, instance.py, test_project.py in a scratch copy, since test_project imports scanner)."),
 ("fc2d-r2-gate-pytest-fc2", "2.5/2.6", "relevant pytest (FC2 filter)", "tests/labs/FC2; tests/test_labs.py; tests/test_run_labs.py; tests/test_page_checks.py; tests/test_memo_exemplars.py", "PASS",
  f"Command: .venv/bin/python -m pytest tests/labs/FC2 tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py tests/test_memo_exemplars.py -k 'FC2 or fc2 or project or grader' -q, rc=0 ({S}/pytest_fc2.out). Full suite not run."),
 ("fc2d-r2-gate-verify-refs", "2.1", "verify_refs --offline and --unit FC2", "tools/verify_refs.py; references/references.json", "PASS",
  f"{S}/verify_refs_offline.out: 'offline integrity: 560 entries, 0 problems' rc=0. {S}/verify_refs_unit_FC2.out: 'live re-verification of FC2: 3 of 560 entries, 0 problems' rc=0 (network reachable from this checkout)."),
 ("fc2d-r2-collect-count", "2.6", "collected checks equal the page count, every seed 0..49", "course/modules/FC/FC2/project.html line 320; grader/test_project.py", "PASS",
  f"{S}/collect_count.py run with python -I over seeds 0..49 with reference.py as scanner.py: {S}/collect_count.out, 'distinct counts: [90]', rc=0 on every seed. Page line 320 says 90 and 'the count is 90 for each of the seeds 0 to 49'. Matches. (Round-3 said 91; the test removed at 4eb6788 is the reason.)"),
 ("fc2d-r2-starter-suite-fails", "2.6", "the suite fails on starter.py", "course/modules/FC/FC2/grader/starter.py; project.html line 297", "PASS",
  f"Starter copied as scanner.py with test_project.py and instance.py, QF_SEED=0, pytest -q --assert=plain -W error: '82 failed, 8 passed' ({S}/twins_isolated.out last lines). The 8 passing tests are the purity, import and no-print tests."),
 # numbers
 ("fc2d-r2-numbers-lab1", "2.2", "Lab 1 numbers (project.html 55-163)", "course/modules/FC/FC2/project.html:55-163", "PASS",
  "Re-derived by hand from the chain at line 70-77: parity gaps 0, 120, 0, 0, -20, 0 at strikes 9000..11500 (C-P-(S-Kdf), df 0.99); costs 45; nets 75 (9500) and -25 (11000); convexity 10500: chord 0.5*800+0.5*450=625, call 700, chord-less-call -75, gross 75, net 30; kept findings 2. Matches the expected block lines 147-162 and the prose at 163. Lab run passes (run_labs)."),
 ("fc2d-r2-numbers-lab3", "2.2", "Lab 3 numbers (project.html 376-486)", "course/modules/FC/FC2/project.html:376-486", "PASS",
  "Re-derived: parity gap at 4500 = 820-155-(5000-4275) = -60 (gross 60, net 0, dropped); 6500: 151-1100-(5000-6175)=226, net 166; 7000: 90-1200-(5000-6650)=540, net 480; convexity chord less call at 4500 = 35, at 5000 = 470/3, at 6000 = -188/3 (gross 63 after one half-up rounding, net 3), at 6500 = 59. Cost 60 = 3*(8+12). Kept = 3. Matches the expected block 469-485 and the interpretation text at 486 (the exact fraction 188/3 = 62.67)."),
 ("fc2d-r2-numbers-exemplars", "2.2", "exemplar numbers (project.html 520-634)", "course/modules/FC/FC2/project.html:520-634", "PASS",
  "Re-derived: 6500*0.95 = 6175 and 151-1100-(5000-6175)=226; 7000*0.95=6650 and 90-1200-(5000-6650)=540; chord at 6000 = (500+2*151)/3 = 802/3 and 802/3-330 = -188/3; gross 63, net 3. Exemplar B's numbers match Lab 3; exemplar A's 'about' values (226, 540, 63) are Lab 3 outputs rounded to whole cents."),
 ("fc2d-r2-hours", "2.6", "hours arithmetic and hub consistency", "course/modules/FC/FC2/project.html:33,35,339-356; course/modules/FC/FC2/index.html:29-41,133; L01-L08 data-hours", "PASS",
  "Project table rows 2+3+5+9+3+5+3 = 30 (project.html 345-352); data-hours-project=30 (line 33); eyebrow '30 hours' (line 35). Hub: data-hours-lessons=60, data-hours-project=30, '90 hours' (index.html 29-31, 41). Lessons data-hours 6+8+9+7+8+8+8+6 = 60. Ruling (rules file): hours are design targets, only arithmetic is checked; arithmetic consistent."),
 ("fc2d-r2-banned-phrases", "2.9", "banned phrases and process words", "project.html; cards.json; grader/*.py; tests/labs/FC2/lab-FC2-project-1..3.py", "PASS",
  "grep -i -E for TODO, TBD, lorem, for brevity, details omitted, beyond the scope, left as an exercise, you can add more, it is important to note, studies show, experts agree, it is well known, obviously, clearly, ellipses, verifier, builder, it can be shown, roughly, historically, simply, trivially: no hit in the learner-facing files. Two 'about' hits (project.html 486 and 590) are an exact fraction rounded for display (188/3 = 62.67) and an exemplar's deliberately vague wording."),
 ("fc2d-r2-notation", "2.4", "notation against notation/notation.json", "notation/notation.json; project.html formulas lines 85-88, 331-336", "PASS",
  "Registered symbols: T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, Q (and macros). The project page uses only the local letters C, P, S, K, df, D (and the labels P1-P6, which the page explicitly distinguishes from P, the put price, at line 335); none of the registered symbols occurs in project.html or the grader. Cards c149 and c150 use R_f with the registered meaning (gross riskless return, reciprocal of the price of a sure payoff of 1; L06 Definition 1.1)."),
 ("fc2d-r2-dag", "2.9", "check_dag and concepts outside the closure", "project.html lines 37, 55, 333-336; curriculum/02-economics-finance-core.yaml:400 (FC2 prereqs [M4, CF1, FC1])", "PASS",
  f"{S}/gates_a.out: check_dag FC2 PASS. Links resolve: L01.html#def-arbitrage-opportunity, L05.html#def-put-call-parity, L05.html#def-option-arbitrage-bounds (all three anchors exist). FC1 is now a prerequisite of FC2 (curriculum line 400), so the FC1 concept bid-ask-spread used in prose at project.html line 333 is inside the closure. The plan's open-items DAG_DEFECT note for bid-ask-spread is stale (observation; no row fails)."),
 ("fc2d-r2-reading-keys", "2.1", "reading list and cited theorems", "project.html 653-658; L05.html", "PASS",
  "data-cite keys hull2021options, stoll1969relationship, cox1979option are in references/references.json and verify_refs --unit FC2 re-resolved them (3 of 560 entries, 0 problems). Theorem 1.2 (put-call parity) and Theorem 3.2 (convexity in strike) of Lesson 5 exist (L05.html). The page quotes no locator. Freshness of the Hull edition: not checked (no source beyond the registry record)."),
 ("fc2d-r2-autograder-panel-claims", "2.6", "autograder panel statements", "course/assets/js/grader.js:18, 46, 74-82; course/assets/js/py-worker.js:1-4", "PASS",
  "Re-read this round: grader.js line 18 fetches the grader's own files (GET), line 46 is a file input accepting .py, lines 76-79 read the chosen file with file.text() into the editor, and py-worker.js says nothing is fetched from a CDN. course/assets/js is byte-identical between a007712f and 4eb6788f (git diff empty), so the round-3 reading also stands."),
 ("fc2d-r2-hub-placement-claim", "2.9", "cross-page claim: placement bar and skip rule", "project.html:42; course/modules/FC/FC2/index.html:146-148", "PASS",
  "Both read this round. project.html line 42: 'Rungs 1 and 2 are optional when you reach the placement bar on the module hub and answer both skill checks'; index.html line 148: 'You may skip them when you reach the placement bar and answer both skill checks.' Consistent."),
 ("fc2d-r2-scope-curriculum-brief", "2.6", "Rung 3 matches the curriculum scope exactly", "curriculum/02-economics-finance-core.yaml:427-429 (brief); course/modules/FC/FC2/project.html:285", "FAIL",
  "Still FAIL. The curriculum brief reads 'Given an embedded option-chain snapshot, detect put-call parity and convexity violations net of a stated cost model...' (yaml lines 427-429). The curriculum file is byte-identical between a007712f and 4eb6788f, so the round-3 FAIL is unchanged. The binding architect decision (plans/FC2-build-plan.md line 634, and B1 at line 449: 'the project uses a SIMULATED chain generated by instance.py') and the page (project.html line 285: 'No market data is embedded') contradict the brief's 'embedded snapshot'. The page's Inputs section is correct; the scope string is not.",
  "Architect action (the verifier does not edit curriculum files): change curriculum/02-economics-finance-core.yaml brief for FC2 project (lines 427-429) to a SIMULATED-chain statement, e.g. 'Given a SIMULATED option chain (bring-your-own-chain schema), detect ...', then run .venv/bin/python tools/render_curriculum.py and regenerate CURRICULUM.md and curriculum/curriculum.json, and rerun tools/build_site.py --check."),
 ("fc2d-r2-rubric-C2-level2", "2.6", "rubric descriptors observable", "course/modules/FC/FC2/project.html:508-512 (rubric rows C1-C5)", "PASS",
  "Read every level cell. Each descriptor names an element the note either shows or does not (e.g. 'says, for each finding, whether it survives the cost', 'names, for each finding, the labels P1 to P6', 'says which direction each settling check would move the finding, and by how many cents'). C2 level 2 at line 509 is the round-2 fix: observable. No vague descriptor found."),
 ("fc2d-r2-rubric-calibration", "2.6", "blind calibration of exemplars A and B", "course/modules/FC/FC2/project.html:520-634 (data-scores 4,4,3,3,3 and 2,1,1,2,1)", "PASS",
  "Scored blind from the rubric only. Exemplar B: my C1 4, C2 3, C3 3, C4 3, C5 3 against annotated 4,4,3,3,3 (all within one). Exemplar A: my C1 2, C2 1, C3 1, C4 2, C5 1 against annotated 2,1,1,2,1 (exact). Every criterion within one level."),
 ("fc2d-r2-spec-questions", "2.6", "spec completeness: questions a competent student would ask", "project.html:297-316", "PASS",
  "Read the spec. Questions I would have had to ask, none blocking: (a) whether the named condition for df_ppm applies to every function (the tests require convexity_violations and parity_gap_cents, which do not use df, to raise; spec says only 'df_ppm is not in 1 to 1000000'); (b) whether a strike of zero or less is refused by parity_gap_cents (tests require it; spec's condition is stated for 'the strikes'); (c) whether the explanation must write each label as its own token (test requires 'P1' etc. as tokens, so 'P1 to P4' fails; spec says 'names P1, P2, P3, P4 and P6'); (d) index base: answered at line 300 (zero-based). Observations, not rows; the page's wording is consistent with the tests in each case."),
 ("fc2d-r2-grader-messages", "2.6", "failure messages name the property and never leak the answer", "grader/test_project.py (every assert message); grader/reference.py:24-47", "PASS",
  "Read every assert and pytest.raises message in test_project.py. Messages name the violated property (e.g. 'the list must hold every interior strike whose call lies above the chord of its neighbours'). Seeded answers are never printed (--assert=plain). Hand-built tie tests state the rule's integer for a public input (e.g. 'an exact tie of 2.5 cents must round up to 3'); those inputs are in the test source, so no seeded answer is leaked."),
 ("fc2d-r2-grader-named-conditions-only", "2.6", "exception types demanded only for named conditions", "grader/test_project.py pytest.raises sites (lines 283-306, 437-475, 489-526, 531-561)", "PASS",
  "Every pytest.raises(ValueError) is for a condition named in project.html 309-315: strikes strictly increasing or positive; df_ppm in 1..1000000; calls or puts one per strike (the message names the lengths); fee or half-spread negative. The bare pytest.raises(ValueError) at lines 509-531 are length conditions, named at 313."),
 ("fc2d-r2-instances", "2.6", "autograder item 2: instance validity and seed variation", "grader/instance.py; grader/test_project.py; " + f"{S}/instance_check_v4b.py", "PASS",
  f"{S}/instance_check_v4b.out: seeds 0..999 checked: 'problems: 0' (ranges as documented, six evenly spaced strikes, no half-cent gap, parity residual at most half a cent off the planted strike, no unplanted convexity violation, clean chains have no findings, planted gross equals the reported gross). Twenty sample seeds: 'distinct finding lists among the 20 sample seeds: 11'."),
 ("fc2d-r2-grader-over-constraint-case", "2.6", "correct alternatives pass with case-insensitive rule names", "course/modules/FC/FC2/grader/test_project.py:587-599", "PASS",
  "Read lines 587-599: the rule is matched with re.search(rf'\\b{rule}', text, re.IGNORECASE) on 'parity' or 'convex'; labels are matched as tokens. The round-2 case is fixed."),
 ("fc2d-r2-grader-over-constraint-trade-verb", "2.6", "explanation wording over-constraint removed", "course/modules/FC/FC2/grader/test_project.py (diff a007712f..4eb6788f: -49 lines, the test test_parity_explanation_states_the_trade_for_the_sign_of_the_gap and its helpers removed)", "PASS",
  "The rejected test is gone; no residual _names_side, _SELL_CALL, _BUY_CALL, _RICH or _CHEAP in the file (grep). The page does not require the explanation to state the trade direction: project.html line 301 requires only that the explanation name the rule and the labels. So the removal is correct and no requirement is lost."),
 ("fc2d-r2-alternatives-pass", "2.6", "five alternative correct implementations pass seeds 0..49", f"{S}/alts/alt1..alt6 (scripts); {S}/alts_run.out; {S}/run_alts_r4.py", "PASS",
  "Run each alternative as scanner.py through the suite for seeds 0..49: alt1 (Fraction, independent) 50/50; alt2 (integer-only, half-up helper) 50/50; alt4 (adjacent-slope comparison, unequal spacing) 50/50; alt5 (parity through the forward S/df) 50/50; alt6 (exact Decimal, replaces the float alternative) 50/50. Each agrees with reference.py on 3000 random chains (unequal spacing, ties, zero costs): 3000/3000. The plan's float alternative (plan 5.5(3)) is NOT counted: it fails only test_parity_exact_tie_at_a_non_dyadic_discount_factor (df 0.58, exact tie 14.5 must round to 15), and project.html line 308 requires money 'computed from exact fractions', so float is not a correct implementation under the page's rules. Its other failure, the length message, was fixed in the alternative so that the exact-tie failure is the only one."),
 ("fc2d-r2-mut-r7-docstrings", "2.6", "mutant docstrings (first line describes the error)", "ledgers/FC2/mutants/r7_a..r7_c", "PASS",
  f"{S}/mutate_fc2_with_u4.out prints each mutant's description (65 of 65 lines carry a description, including r7_a..c)."),
 ("fc2d-r2-mut-new-killed", "2.6", "round-2 new mutants v07..v10 killed", "ledgers/FC2/mutants/v07..v10", "PASS",
  f"{S}/mutate_fc2_with_u4.out: KILLED v07 (test_convexity_matches_oracle_on_an_uneven_grid, seed 0), v08 (test_convexity_finding_with_net_one_cent_is_returned, seed 0), v09 (test_scan_explanations_are_nonempty_and_name_the_rule, seed 1), v10 (test_convexity_half_cent_tie_rounds_once_up_at_any_discount_factor, seed 0)."),
 ("fc2d-r2-mut-r5d-resolved", "2.6", "former survivor r5_d", "ledgers/FC2/mutants/ (r5_d absent; the file was renamed to r3_b at 4eb6788f)", "PASS",
  "r5_d (explanation direction reversed) is no longer in the mutant set. Its only killer was the removed explanation-wording test. The spec does not require the explanation to state the trade direction (project.html line 301), so a reversed direction violates no stated behaviour and is not a finding; the removal is not a survivor. Recorded so the mutant count change is explained: 63 (round 3) minus r5_d plus u4_a..c = 65."),
 ("fc2d-r2-mut-equivalents", "2.6", "no equivalent mutant in the set", "ledgers/FC2/mutants/ (65 files)", "PASS",
  f"Every one of the 65 mutants is KILLED on seeds 0..9 ({S}/mutate_fc2_with_u4.out). A killed mutant differs from the reference on some tested input, so none is equivalent to it."),
 ("fc2d-r2-cards-full-scan", "2.7", "cards: unique ids, fronts, backs; near-duplicate review", "course/modules/FC/FC2/cards.json (151 cards)", "PASS",
  "Python -I scan: 151 cards, 0 duplicate ids, 0 duplicate fronts, 0 duplicate backs. difflib pairs with front or back ratio >= 0.6: 35 pairs, reviewed (e.g. c069 convexity vs c070 monotonicity; c126 vs c131 two different strikes; c102 vs c145 formula vs derivation status; c124 vs c152 what it does vs where it starts). None is a duplicate fact. Id gaps FC2-c031 and FC2-c077 predate this round and are not a fault."),
 ("fc2d-r2-cards-refs-numbers", "2.7", "every card number appears in its lesson", "course/modules/FC/FC2/cards.json; L01-L08 text (/tmp dumps from strip_text.py)", "PASS",
  f"{S}/cards_numbers_r4.py over 151 cards: {S}/cards_numbers_r4.out: 'tokens missing: 0 cards: 151'."),
 ("fc2d-r2-cards-lab-numbers", "2.7", "card numbers from labs agree with lab output", "cards c012, c013, c095, c147, c148; tests/labs/FC2 twins", CARRY + "cards c012, c013, c095, c147, c148 unchanged in the delta; the round-3 verification (twin_lab-FC2-L01-1.out, twin_lab-FC2-L06-1.out) stands, lab twins and L01/L06 text byte-identical since a007712f.", "PASS",
  "Carried from round 3 (cards.json object FC2-c012, c013, c095, c147, c148 byte-identical since a007712f; lab twins and L01/L06 text byte-identical since a007712f): the round-3 verification (twin_lab-FC2-L01-1.out, twin_lab-FC2-L06-1.out) stands."),
 ("fc2d-r2-card-c010", "2.7", "card FC2-c010 agrees with the current lesson text", "course/modules/FC/FC2/cards.json FC2-c010; L01.html", CARRY + "FC2-c010.", "PASS",
  "Carried from round 3: object FC2-c010 byte-identical since a007712f (the round-4 delta changed only c093, c123, c124 and c149-c153)."),
 ("fc2d-r2-card-c132", "2.7", "card FC2-c132 agrees with L05 Theorem 4.1 and Remark 4.2", "cards.json FC2-c132; L05.html", CARRY + "FC2-c132.", "PASS",
  "Carried from round 3: object FC2-c132 byte-identical since a007712f; L05 text byte-identical."),
 ("fc2d-r2-card-c020", "2.7", "card FC2-c020 agrees with its lesson passage", "course/modules/FC/FC2/cards.json FC2-c020", CARRY + "FC2-c020.", "PASS", "Carried from round 3: object byte-identical since a007712f."),
 ("fc2d-r2-card-c030", "2.7", "card FC2-c030 agrees with its lesson passage", "course/modules/FC/FC2/cards.json FC2-c030", CARRY + "FC2-c030.", "PASS", "Carried from round 3: object byte-identical since a007712f."),
 ("fc2d-r2-card-c041", "2.7", "card FC2-c041 agrees with its lesson passage", "course/modules/FC/FC2/cards.json FC2-c041; L03.html Proposition 3.2 (L03.txt lines 33-38)", "PASS",
  "Re-verified this round against L03 text: Proposition 3.2 gives the floating leg as 1 - DF_n; the coupon's present value is DF_i L_i = DF_{i-1} - DF_i and the sum telescopes with DF_0 = 1 (L03.txt lines 36-38). Card says the same."),
 ("fc2d-r2-card-c051", "2.7", "card FC2-c051 agrees with its lesson passage", "course/modules/FC/FC2/cards.json FC2-c051; L04.txt Definition 1.1 (lines 18-20)", "PASS",
  "Re-verified: L04 Definition 1.1: call pays (S_tau - K)^+, put pays (K - S_tau)^+; in the money at S_t > K (call) and S_t < K (put). Card matches."),
 ("fc2d-r2-card-c061", "2.7", "card FC2-c061 agrees with its lesson passage", "course/modules/FC/FC2/cards.json FC2-c061; L04.txt lines 129, 145-156", "PASS",
  "Re-verified: the lab table prints 25.00 payoff and 17.00 profit at spot 125 (L04.txt line 129); the text says the 8.00 premium is subtracted only in the profit column (line 145); the call's premium is 8.00 (line 156). Card matches."),
 ("fc2d-r2-card-c071", "2.7", "card FC2-c071 agrees with its lesson passage", "course/modules/FC/FC2/cards.json FC2-c071; L05.txt Theorem 4.1, Remark 4.2 (lines 187-194, 304)", "PASS",
  "Re-verified: Theorem 4.1 hypotheses A1-A5, (N), r >= 0; equality V_A(0) = V_E(0) at date 0 only (L05.txt line 304; Remark 4.2 at line 194 says the proof is at date 0 only). The card's 'a remark, not a proved result' matches Remark 4.2."),
 ("fc2d-r2-card-c082", "2.7", "card FC2-c082 agrees with its lesson passage", "course/modules/FC/FC2/cards.json FC2-c082", CARRY + "FC2-c082.", "PASS", "Carried from round 3: object byte-identical since a007712f."),
 ("fc2d-r2-card-c092", "2.7", "card FC2-c092 agrees with its lesson passage", "course/modules/FC/FC2/cards.json FC2-c092", CARRY + "FC2-c092.", "PASS", "Carried from round 3: object byte-identical since a007712f."),
 ("fc2d-r2-card-c102", "2.7", "card FC2-c102 agrees with its lesson passage", "course/modules/FC/FC2/cards.json FC2-c102", CARRY + "FC2-c102.", "PASS", "Carried from round 3: object byte-identical since a007712f."),
 ("fc2d-r2-card-c112", "2.7", "card FC2-c112 agrees with its lesson passage", "course/modules/FC/FC2/cards.json FC2-c112", CARRY + "FC2-c112.", "PASS", "Carried from round 3: object byte-identical since a007712f."),
 ("fc2d-r2-card-c120", "2.7", "card FC2-c120 agrees with its lesson passage", "course/modules/FC/FC2/cards.json FC2-c120", CARRY + "FC2-c120.", "PASS", "Carried from round 3: object byte-identical since a007712f."),
 ("fc2d-r2-card-c142", "2.7", "card FC2-c142 agrees with its lesson passage", "course/modules/FC/FC2/cards.json FC2-c142", CARRY + "FC2-c142.", "PASS", "Carried from round 3: object byte-identical since a007712f."),
 # round-3 FAIL rows that changed
 ("fc2d-r3-instance-docstring-bounds", "2.6", "instance.py docstring matches the bounds check", "course/modules/FC/FC2/grader/instance.py:13-18 vs :47-60; test_project.py:800-816", "PASS",
  "The docstring (lines 16-18) now says a draw is rejected when a quote lies more than half a cent outside the Theorem 2.2 bounds, and that a quote within half a cent is kept. _within_bounds (lines 47-60) applies exactly that tolerance (call > spot + 1/2, call < max(S - Kdf, 0) - 1/2, put < -1/2, put > Kdf + 1/2, put < max(Kdf - S, 0) - 1/2). L05 Theorem 2.2 bounds (L05.txt line 265) are the four bounds in the docstring. 1000 seeds: no quote outside the tolerance (instance_check_v4b.out, problems 0)."),
 ("fc2d-r3-scope-changed-hunks", "2.2/2.6/2.7", "every hunk changed since the previous pin is read", "project.html 297, 317, 483, 496; grader/instance.py 13-18; grader/test_project.py 599-648; cards.json c093, c123, c124, c149-c153; mutants r3_b rename, r5_d removal, q3/r3/u4 additions", "PASS",
  "git diff a007712f 4eb6788f over the slice: project.html four hunks (convexity wording and zero-based index at 297, the 90-check count at 317, the Lab 3 interpretation at 483, the brief's numbers line at 496) all read; instance.py docstring read; test_project.py removal (lines 599-648) read; cards.json changed c093, c123, c124 and added c149-c153, all read against the lesson text. No hunk in the lab code, the JS or the lesson pages."),
 ("fc2d-r3-df-ppm-link", "2.9", "df_ppm link resolves", "course/modules/FC/FC2/project.html:289; anchor id conventions at line 325", "PASS",
  "href='#conventions' resolves to <h3 id=\"conventions\"> (project.html line 325); the P4 label it points to is defined at line 331."),
 ("fc2d-r3-mut-new-killed", "2.6", "round-3 student-error mutants q3_a..q3_d killed", "ledgers/FC2/mutants/q3_a..q3_d", "PASS",
  f"{S}/mutate_fc2_with_u4.out: KILLED q3_a, q3_b, q3_c, q3_d (each with the test named in the output)."),
 ("fc2d-r3-mut-prior-untracked", "2.6", "round-3 mutants r3_a..r3_d re-run", "ledgers/FC2/mutants/r3_a..r3_d", "PASS",
  f"Now committed at 4eb6788f. {S}/mutate_fc2_with_u4.out: KILLED r3_a, r3_b, r3_c, r3_d."),
 ("fc2d-r3-footer-no-upload", "2.9", "footer and autograder text: no learner data leaves the browser", "project.html:671 footer; project.html:285; course/assets/js/grader.js:18, 46, 76-79", "PASS",
  "Re-read this round: footer (line 671) says nothing you write leaves the browser; grader.js fetches only the grader's own files (line 18, GET), reads a chosen file locally (file.text(), line 76-79). No POST or beacon in grader.js or py-worker.js (grep for fetch, XMLHttpRequest, sendBeacon, upload)."),
 ("fc2d-r3-exemplar-scores-match-text", "2.6", "exemplar scores agree with their annotations", "project.html:520-634", "PASS",
  "Each annotation (meets or misses, with its level) checked against its passage: exemplar B's C1 4, C2 4, C3 3, C4 3, C5 3 and exemplar A's C1 2, C2 1, C3 1, C4 2, C5 1 each follow from the annotations listed under them."),
 # round-4 new rows
 ("fc2d-r4-card-c093", "2.7", "card FC2-c093 agrees with L06 Theorem 3.3 and Definition 3.2", "course/modules/FC/FC2/cards.json FC2-c093; L06.html Definition 3.2, Theorem 3.3 (L06.txt lines 51-57)", "PASS",
  "Changed at 4eb6788f. Front states the hypotheses A1, A2, A3, A5, A6, A6' (Theorem 3.3 states the same). Back: V(n,k) is the backward-induction value of Definition 3.2 (which defines V(N,k) = f(S(N,k)) and V(n,k) = (qV(n+1,k+1) + (1-q)V(n+1,k))/R_f) and Theorem 3.3 says that is the arbitrage-free price. Matches."),
 ("fc2d-r4-card-c123", "2.7", "card FC2-c123 agrees with L08 Proposition 3.2", "course/modules/FC/FC2/cards.json FC2-c123; L08.txt Proposition 3.2 (line 48)", "PASS",
  "Changed at 4eb6788f. Back: first k with W/2^k <= tau_tol, equal to ceil(log2(W/tau_tol)) when W > tau_tol (Proposition 3.2), with the bracket condition and C* in (L,S) stated. Matches Proposition 3.2's hypotheses and conclusion."),
 ("fc2d-r4-card-c124", "2.7", "card FC2-c124 agrees with L08 Definition 3.1", "course/modules/FC/FC2/cards.json FC2-c124; L08.txt Definition 3.1 (line 46)", "PASS",
  "Changed at 4eb6788f. Definition 3.1: while width > tau_tol, m = midpoint, keep the half that still brackets C*; report the midpoint when the loop ends. Card says the same; 'stops when width at most tau_tol' is the loop's negation."),
 ("fc2d-r4-card-c149", "2.7", "card FC2-c149 agrees with L06 Definition 3.1 (A6')", "course/modules/FC/FC2/cards.json FC2-c149; L06.txt line 50", "PASS",
  "Added at 4eb6788f. L06 Definition 3.1: A6 applies at every node n < N with the same u, d, R_f; 'This is assumption A6''. Card matches."),
 ("fc2d-r4-card-c150", "2.7", "card FC2-c150 agrees with L06 Theorem 3.3 formula", "course/modules/FC/FC2/cards.json FC2-c150; L06.html line 143", "PASS",
  "Added at 4eb6788f. Theorem 3.3 display (L06.html line 143): V(0,0) = R_f^{-N} sum_{k=0}^{N} C(N,k) q^k (1-q)^{N-k} f(S_0 u^k d^{N-k}). Card's formula is the same; the hypotheses are in the front."),
 ("fc2d-r4-card-c152", "2.7", "card FC2-c152 agrees with L08 Definition 3.1", "course/modules/FC/FC2/cards.json FC2-c152; L08.txt line 46", "PASS",
  "Added at 4eb6788f. Definition 3.1 begins from sigma_lo < sigma_hi with C(sigma_lo) < C* and C(sigma_hi) >= C*. Card matches."),
 ("fc2d-r4-card-c153", "2.7", "card FC2-c153 agrees with L05 Remark 3.3", "course/modules/FC/FC2/cards.json FC2-c153; L05.txt lines 41, 51-52", "PASS",
  "Added at 4eb6788f. Remark 3.3: with K2-K1 = K3-K2, lambda = 1/2 and the condition reads C(K1) - 2C(K2) + C(K3) >= 0, a second difference (L05.txt line 52). The condition itself is defined at line 41. Matches; no proposition hypotheses are needed for an algebraic reduction."),
 ("fc2d-r4-card-c151", "2.7", "card FC2-c151 carries Proposition 3.2's hypotheses", "course/modules/FC/FC2/cards.json FC2-c151; L08.txt Proposition 3.2 (line 48)", "FAIL",
  "Added at 4eb6788f. The front asks how close the midpoint is to sigma* for 'the bisection of Definition 3.1 stopped at tolerance tau_tol', and the back says 'the final bracket contains sigma*'. Proposition 3.2 has the hypothesis 'a bracket satisfying the bracket condition of Definition 3.1 with C* in (L, S)'. The card omits C* in (L, S), the hypothesis that makes sigma* exist (Theorem 2.3). Card c123 states it; c151 does not. Rule 10 of the verifier rules (cards carry a proposition's hypotheses) fails.",
  "Add the hypothesis to the front, as c123 does, e.g. front: 'For the bisection of Definition 3.1 on a bracket with C(sigma_lo) < C* <= C(sigma_hi) and C* in (L, S), stopped at tolerance tau_tol, how close is the reported midpoint to the implied volatility sigma*?' (the back's wording otherwise stands)."),
 ("fc2d-r4-cards-sample", "2.7", "one card in ten sampled, plus the changed cards", "course/modules/FC/FC2/cards.json ids FC2-c001, c011, c021, c032, c041, c051, c061, c071, c081, c091, c101, c111, c121, c141", "PASS",
  "Checked against lesson text: c001 (L01 Definition 1.1), c011 (L01 example: stock 1, two short bonds at 9/10 cost -4/5, payoff (1,-1), L01.txt line 172 and 244), c021 (L02 Example 2.4: 50e^{0.025}=51.2658, Lab 2 Part A prints 5126.58), c032 (L02 Definition 1.1: no payment at date 0), c041 (L03 Prop 3.2 and telescoping, L03.txt 36-38), c051 (L04 Definition 1.1), c061 (L04 lab 25.00/17.00/8.00), c071 (L05 Theorem 4.1 and Remark 4.2), c081 (L06 Definition 1.1), c091 (L06 Example 1.5, q=3/4, u=3/2, Definition 2.1), c101 (L07 Lemma 1.2), c111 (L07 Lab 1 sign pattern 1,5,25 vs 2,10,50,100,200,400, L07.txt line 169), c121 (L08 Lemma 2.2 limits), c141 (L02 Proposition 2.2 and 3.1 dates, L02.txt line 20). All agree."),
 ("fc2d-r4-mut-u4-new-killed", "2.6", "three new student-error mutants written by this verifier", "ledgers/FC2/mutants/u4_a..u4_c", "PASS",
  f"u4_a (parity explanation omits P6): killed by test_scan_explanations_are_nonempty_and_name_the_rule (seed 1). u4_b (cost ignores the half-spread): killed by test_scan_matches_exhaustive_oracle_second_chain (seed 0). u4_c (discounted strike by floor division): killed by test_half_cent_gross_rounds_once_up (seed 0). Output in {S}/mutate_fc2_with_u4.out."),
]

fragment = {
    "unit": "FC2",
    "slice": "FC2-d",
    "round": 4,
    "verifier": "Claude Haiku 5.5, independent verifier for FC2-d round 4 (did not build FC2)",
    "pin": "4eb6788fe3b408bb6d90ac73addc6fb17af47b8b",
    "base": "a007712fdbfc8b4851123f4de76b5310ac5a9e64 (round-3 pin); delta inside the slice: project.html 297, 317, 483, 496; grader/instance.py 13-18; grader/test_project.py 599-648 removed; cards.json c093, c123, c124 changed and c149-c153 added; mutants r3_b renamed from r5_d, r3_a..d committed; no curriculum, lesson, labs or JS change",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyD4-FC2-d",
    "scratch": "/tmp/fc2d-r4-mypy, /tmp/fc2d-r4 (lesson text dumps), /tmp/fc2d-twin-*, /tmp/fc2d-starter-* (removed after use); every number cited in a row is reproduced by a script under ledgers/FC2/scripts/FC2-d-r4/",
    "verified_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    "verdict": "",
    "rows": [],
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": "",
    "summary": "",
}
for t in rows:
    if t[4] in ("PASS", "FAIL"):  # (id, check, location, extra location, status, evidence[, fix])
        rid, check, location, _extra, status, evidence = t[:6]
        fix = [t[6]] if len(t) == 7 else []
    else:  # carried rows: (id, check, check text, location, carry prefix, status, detail)
        rid, check, _text, location, prefix, status, detail = t
        evidence = prefix  # the carry statement names the subject; the detail repeats it
        fix = []
    row = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        row["fix"] = fix[0]
    fragment["rows"].append(row)
fragment["verdict"] = "PASS" if all(r["status"] == "PASS" for r in fragment["rows"]) else "FAIL"
counts = {s: sum(1 for r in fragment["rows"] if r["status"] == s) for s in ("PASS", "FAIL", "UNVERIFIABLE")}
fragment["summary"] = (
    f"FC2-d round 4 on 4eb6788 (round-3 pin a007712): verdict {fragment['verdict']}. {len(fragment['rows'])} rows: "
    f"{counts['PASS']} PASS, {counts['FAIL']} FAIL, {counts['UNVERIFIABLE']} UNVERIFIABLE. Mutants: "
    f"{len(mutants)} in ledgers/FC2/mutants, {sum(m['killed_by'] != 'NONE' for m in mutants)} killed. Blocking FAILs: "
    "(1) fc2d-r2-scope-curriculum-brief: curriculum brief still says 'embedded option-chain snapshot' (architect action); "
    "(2) fc2d-r4-card-c151: card omits Proposition 3.2's hypothesis C* in (L, S)."
)
fragment["notes"] = (
    "Round 4 on 4eb6788. Read in full at 4eb6788: project.html (673 lines), grader/reference.py, starter.py, instance.py, "
    "test_project.py (826 lines), the three project lab twins; cards.json (151 cards) by full scan for duplicates and "
    "numbers, sampled 14 cards and every changed card against L05, L06, L08 text. The round-3 PASS rows whose subject was "
    "byte-identical are carried with the 'Carried from round 3' prefix; rows whose subject changed were re-verified from scratch. "
    "Round-3 FAIL rows: fc2d-r2-grader-over-constraint-trade-verb and fc2d-r2-alternatives-pass now PASS (test removed; five "
    "exact alternatives pass); fc2d-r3-instance-docstring-bounds now PASS (docstring matches code); fc2d-r2-scope-curriculum-brief "
    "still FAIL (curriculum yaml unchanged). Checkout note: ledgers/FC2/scripts/FC2-d-r4 already held tracked files from an earlier "
    "batch (instance_check_r4.py/.out, write_fragment_r4.py, gen_mutants.py, etc.); I restored instance_check_r4.py and .out after "
    "overwriting them by mistake, and wrote my scripts under new names. Observations (not rows): plans/FC2-open-items.md still "
    "calls bid-ask-spread a DAG_DEFECT although FC1 is now a prerequisite; the explanation-label check requires each label as a "
    "token, so 'P1 to P4' fails (consistent with the spec's 'names P1, P2, P3, P4 and P6'); the spec does not say which functions "
    "raise on df_ppm or strike errors (the tests require all three). Mutant count: 65 (62 prior less r5_d plus three new) all killed. "
    "Not checked: the full repo gate (render_curriculum, build_site --check, fetch_data --check, full pytest, full mypy); the "
    "self-assessment form (needs JavaScript; static read only); freshness of the Hull 2021 edition (no source beyond the registry "
    "record); lessons L01-L04 and L07 read only where cards or the project point to them; the figure sweep (no figures on the page)."
)
out_path.write_text(json.dumps(fragment, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("rows", len(fragment["rows"]), counts, "verdict", fragment["verdict"], "mutants", len(mutants))
