"""FC2-d round 2 fragment builder (verifier output; every evidence string cites a file in ledgers/FC2/scripts/FC2-d-r2/)."""
import json, re, datetime, sys
root = sys.argv[1]
S = f"{root}/ledgers/FC2/scripts/FC2-d-r2"
mut_lines = open(f"{S}/mutate_graders_after_new.out", encoding="utf-8").read().splitlines()
mutants = []
for line in mut_lines:
    m = re.match(r"^(KILLED|SURVIVED) (\S+\.py): (.*) -> (.*)$", line)
    if not m:
        continue
    name, desc, killer = m.group(2)[:-3], m.group(3), m.group(4)
    if desc == "(no description)":
        desc = "(no docstring: the file opens with # comments; mutate_graders prints '(no description)')"
    mutants.append({"id": name, "description": desc, "killed_by": killer if m.group(1) == "KILLED" else None})

def card_row(cid, what):
    return {"id": f"fc2d-r2-card-{cid}", "check": "2.7 retrieval card (sampled 1 in 10)",
            "location": f"course/modules/FC/FC2/cards.json ({cid}); lesson {what}",
            "status": "PASS", "evidence": f"{what}"}

rows = [
 {"id": "fc2d-r2-gate-mutate", "check": "2.6 mutation gate: tools/mutate_graders.py --unit FC2 --seeds 0-9",
  "location": "tools/mutate_graders.py; ledgers/FC2/mutants/ (55 files)", "status": "PASS",
  "evidence": f"{S}/mutate_graders_after_new.out ends 'mutate_graders FC2: PASS (55/55 killed)', exit 0. The 51 prior mutants (earlier run {S}/mutate_graders.out, 51/51) and the 4 new v07-v10 are all KILLED. r5_d, the round-1 survivor, is now killed by test_parity_explanation_states_the_trade_for_the_sign_of_the_gap."},
 {"id": "fc2d-r2-gate-run-graders", "check": "2.6 run_graders --seeds 0-49 on reference.py",
  "location": "tools/run_graders.py; course/modules/FC/FC2/grader/", "status": "PASS",
  "evidence": f"{S}/run_graders.out: 'run_graders FC2: PASS (reference 50/50 seeds, slowest 0.2 s)', rc=0."},
 {"id": "fc2d-r2-gate-check-projects", "check": "tools/check_projects.py --unit FC2 and --all",
  "location": "tools/check_projects.py", "status": "PASS",
  "evidence": f"{S}/check_projects.out ('check_projects FC2: PASS', rc=0); {S}/check_projects_all.out (FC2 line PASS, rc=0)."},
 {"id": "fc2d-r2-gate-check-dag", "check": "2.9 tools/check_dag.py --unit FC2", "location": "tools/check_dag.py", "status": "PASS",
  "evidence": f"{S}/check_dag.out: 'check_dag FC2: PASS', rc=0."},
 {"id": "fc2d-r2-gate-check-pages", "check": "2.9 tools/check_pages.py --all", "location": "tools/check_pages.py", "status": "PASS",
  "evidence": f"{S}/check_pages.out: 'check_pages FC2: PASS', rc=0 (the --all run; no single-unit form was used)."},
 {"id": "fc2d-r2-gate-run-labs", "check": "2.5 run_labs --unit FC2 --page project", "location": "tools/run_labs.py; project.html lab-FC2-project-1..3", "status": "PASS",
  "evidence": f"{S}/run_labs_project.out: 'run_labs FC2: PASS (3/3)', rc=0."},
 {"id": "fc2d-r2-lab-twins-isolated", "check": "2.5 twins alone under python -I -W error",
  "location": "tests/labs/FC2/lab-FC2-project-1.py, -2.py, -3.py", "status": "PASS",
  "evidence": f"Run by hand: {S}/out/lab-FC2-project-1.out, -2.out, -3.out end rc=0 (python -I -W error). Each twin's output is the expected block (see next row)."},
 {"id": "fc2d-r2-lab-page-equals-twin", "check": "2.5 page code equals twin; expected block equals output",
  "location": "course/modules/FC/FC2/project.html lines 56-146, 169-257, 378-485", "status": "PASS",
  "evidence": f"{S}/project_labs_compare.py output in {S}/project_labs_compare.out: lab 1 and lab 3 page code == twin; lab 2 page code differs from its twin only in the three blanks (diff: 'gap = ___' vs 'gap = parity_gap(...)', 'net = ___' twice vs 'gross - cost'), the completion problem by design; expected block == twin output for labs 1, 2 and 3."},
 {"id": "fc2d-r2-gate-page-smoke", "check": "2.9 tools/page_smoke.py --unit FC2 --pages project (alone)", "location": "tools/page_smoke.py", "status": "PASS",
  "evidence": f"{S}/page_smoke_project.out: 'page_smoke modules/FC/FC2/project.html: PASS', 'in-browser grader: All 91 tests pass on seed 826166900', rc=0 (Pyodide)."},
 {"id": "fc2d-r2-gate-ruff-mypy", "check": "ruff check + format --check; mypy", "location": "tests/labs/FC2; course/modules/FC/FC2/grader", "status": "PASS",
  "evidence": f"{S}/ruff.out: 'All checks passed!' and '15 files already formatted', rc=0. {S}/mypy_default.out (default config, files = tools, tests incl. tests/labs/FC2): 'Success: no issues found in 331 source files', rc=0. {S}/mypy_grader_scratch.out: strict mypy on test_project.py, instance.py and scanner.py (reference copy) in a scratch dir: 'Success', rc=0. Explicit mypy on the grader directory in the checkout fails only because scanner.py is absent (import-not-found); it is not a configured gate target."},
 {"id": "fc2d-r2-gate-pytest-fc2", "check": "relevant pytest (FC2 and lab, page and project filters)", "location": "tests/", "status": "PASS",
  "evidence": f"{S}/pytest_fc2_full.out: '321 passed, 346 deselected in 45.50s', rc=0."},
 {"id": "fc2d-r2-gate-verify-refs", "check": "2.1 verify_refs (offline whole registry; live FC2 entries)", "location": "tools/verify_refs.py; references/references.json", "status": "PASS",
  "evidence": f"{S}/verify_refs_offline.out: 'offline integrity: 560 entries, 0 problems', rc=0. {S}/verify_refs_live_unit.out: 'live re-verification of FC2: 3 of 560 entries, 0 problems', rc=0 (the three keys hull2021options, stoll1969relationship and cox1979option exist in references.json)."},
 {"id": "fc2d-r2-collect-count", "check": "2.6 collected test count equals the page's count (91)",
  "location": "course/modules/FC/FC2/project.html line 320; grader/test_project.py", "status": "PASS",
  "evidence": f"{S}/collect_count.sh run on the reference as scanner.py: {S}/collect_count.out shows 91 for every seed 0..49 (grep -c '::' on pytest --collect-only -q). Page line 320 says 91 for each seed 0 to 49."},
 {"id": "fc2d-r2-starter-suite-fails", "check": "2.6/Rung 3 spec: the suite fails on starter.py",
  "location": "course/modules/FC/FC2/grader/starter.py; project.html line 297", "status": "PASS",
  "evidence": f"{S}/starter_suite.out: on the starter as scanner.py (seed 0), 83 failed, 8 passed (the purity and import tests), exit 1."},
 {"id": "fc2d-r2-numbers-lab1", "check": "2.2 numbers in prose: Lab 1 (project.html lines 55-163)", "location": "course/modules/FC/FC2/project.html:55-163", "status": "PASS",
  "evidence": f"Each number (cost 45; parity gaps 120, -20, zeros; net 75, -25; chord 625 and call 700; convexity gross 75, net 30; two findings) equals the printed block of lab-FC2-project-1 ({S}/out/lab-FC2-project-1.out is the twin's own output) and was recomputed by hand from the chain (chord weights 0.5/0.5 at 10500: 0.5*800+0.5*450=625)."},
 {"id": "fc2d-r2-numbers-lab3", "check": "2.2 numbers in prose: Lab 3 (project.html lines 375-486)", "location": "course/modules/FC/FC2/project.html:376-486", "status": "PASS",
  "evidence": f"Recomputed in a scratch run: cost 60; parity gap at 4500 = -60 (gross 60, net 0, dropped); at 6500 gap 226 (net 166); at 7000 gap 540 (net 480); convexity at 6000 chord less call = -188/3 (chord 802/3, call 330), gross round(62.67)=63, net 3. Matches {S}/out/lab-FC2-project-3.out."},
 {"id": "fc2d-r2-numbers-exemplars", "check": "2.2 numbers in prose: exemplars A and B (project.html lines 518-634)", "location": "course/modules/FC/FC2/project.html:520-634", "status": "PASS",
  "evidence": "Recomputed: 151-1100-(5000-6175)=226 (6175=6500*0.95); 90-1200-(5000-6650)=540 (6650=7000*0.95); (500+2*151)/3=802/3; 330 call; -188/3; 3 cent net; 'about 226/540/63' in exemplar A are approximations of the same values. Exemplar B's K df change statement (strike times change in factor) is the derivative of C-P-S+K df with respect to df, correct."},
 {"id": "fc2d-r2-hours", "check": "2.6 hours: arithmetic and a component estimate",
  "location": "course/modules/FC/FC2/project.html:33,35,339-356; course/modules/FC/FC2/index.html:31-41", "status": "PASS",
  "evidence": "Table rows 2+3+5+9+3+5+3 = 30 = data-hours-project=30 = eyebrow '30 hours' = hub '30 h project' (index.html line 41). Ruling: hours are design targets; only arithmetic inconsistencies fail. My estimate for a competent student is about 17 h (reading and labs 2.5, derivations 3, scanner.py 6, edge cases 2, findings note 3.5, self-assessment 1.5), so the declared 30 h is on the high side; not a fail under the ruling."},
 {"id": "fc2d-r2-banned-phrases", "check": "2.9 banned phrases (BUILDER_RULES 1.3-1.4) and process words",
  "location": "project.html; cards.json; grader/*.py; lab-FC2-project-1..3.py", "status": "PASS",
  "evidence": "grep -rn -i over those files for TODO, TBD, lorem, for brevity, details omitted, beyond the scope, left as an exercise, you can add more, it is important to note, studies show, experts agree, it is well known, obviously, clearly, ellipsis, we, our, verifier, builder: no hits."},
 {"id": "fc2d-r2-notation", "check": "2.4 notation vs notation/notation.json",
  "location": "notation/notation.json; project.html formulas lines 85-88, 335-336", "status": "PASS",
  "evidence": "Registered symbols: T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q}. The project page uses C, P (put), S, K, D and df (df_ppm/10^6) and the labels P1-P6; none is a registered symbol with another meaning. No symbol clash."},
 {"id": "fc2d-r2-dag", "check": "2.9 check_dag and concept use outside closure", "location": "project.html:37,333; curriculum/02-economics-finance-core.yaml:396-416", "status": "PASS",
  "evidence": "Links: arbitrage-opportunity (L01), put-call-parity and option-arbitrage-bounds (L05), all defined in FC2 (check_dag FC2 PASS). FC1 concept bid-ask spread used in plain prose with no link (line 333), as the Architect decisions allow. No undefined link."},
 {"id": "fc2d-r2-reading-keys", "check": "2.1 reading list and cited theorems", "location": "project.html:654-658", "status": "PASS",
  "evidence": "data-cite keys hull2021options, stoll1969relationship, cox1979option present in references.json (grep; live FC2 verify 3/0). The page quotes no locator. Theorem 1.2 (put-call parity, L05 line 63) and Theorem 3.2 (convexity in strike, L05 line 115) exist in FC2 L05.html with proofs."},
 {"id": "fc2d-r2-autograder-panel-claims", "check": "2.6 autograder panel statements (project.html lines 285, 360, 367)",
  "location": "course/assets/js/grader.js:33-80; js/py-worker.js:111", "status": "PASS",
  "evidence": "grader.js saves the draft on input (editor 'input' listener, line 59-61); the file input reads the .py with file.text() in the page (lines 75-80) and does not upload; the local command string matches the page (grader.js line 53: pytest -q -p no:cacheprovider --assert=plain -W error); py-worker.js line 111 runs --assert=plain -W error."},
 {"id": "fc2d-r2-hub-placement-claim", "check": "2.9 cross-page claim: placement bar and skip rule", "location": "project.html:42; index.html:148", "status": "PASS",
  "evidence": "Hub index.html line 148 and project.html line 42 both say rungs 1 and 2 may be skipped at the placement bar with both skill checks answered; Rung 3 is graded and cannot be skipped."},
 {"id": "fc2d-r2-scope-curriculum-brief", "check": "2.6 Rung 3 matches the curriculum scope exactly",
  "location": "curriculum/02-economics-finance-core.yaml:428-430 (brief); project.html:285 (Inputs)", "status": "FAIL",
  "evidence": "The curriculum brief reads 'Given an embedded option-chain snapshot, detect put-call parity and convexity violations net of a stated cost model, and explain each one found.' The page says 'No market data is embedded' and grades on a generated SIMULATED chain (project.html line 285; open item D1 in plans/FC2-open-items.md; plan section 7 B1). Parity, convexity, cost netting and explanation match; the input does not.",
  "fix": "Architect decision (not a builder fix): either supply a redistributable option-quote snapshot with a quoted licence (DATA_REQUEST D1, then embed it and rebuild the grader instances), or amend the curriculum brief at curriculum/02-economics-finance-core.yaml:428 to 'a SIMULATED option chain' so the scope matches the page."},
 {"id": "fc2d-r2-rubric-C2-level2", "check": "2.6 rubric: every level descriptor observable",
  "location": "course/modules/FC/FC2/project.html:509 (rubric C2, level 2 cell)", "status": "FAIL",
  "evidence": "The level-2 cell reads 'States the cost model, but says whether only some findings survive it, or reports gross amounts without the cost.' The first clause is not observable as an error: a note that correctly says that only some findings survive (Lab 3 keeps three of four) reads as level 2, while level 3 requires that each finding's survival be stated. The descriptor is vague as written.",
  "fix": "Rewrite the first clause as 'says whether the cost removes some findings but does not say, for each finding, whether it survives' (or similar) so that correct statements of survival are not penalised."},
 {"id": "fc2d-r2-rubric-calibration", "check": "2.6 rubric calibration: blind scoring of exemplars A and B within one level",
  "location": "course/modules/FC/FC2/project.html:520-634 (exemplar data-scores)", "status": "PASS",
  "evidence": "Blind scores from the rubric alone (no annotations read first): exemplar B C1 4, C2 3, C3 3, C4 3, C5 2 vs official 4,4,3,3,3 (within one on every criterion; C2 3 because 'gap between the net and zero' is not stated in words); exemplar A C1 2, C2 1, C3 1, C4 2, C5 1 vs official 2,1,1,2,1 (exact)."},
 {"id": "fc2d-r2-spec-questions", "check": "2.6 spec completeness (questions a competent student would need to ask)", "location": "project.html:297-316", "status": "PASS",
  "evidence": "Questions I would have asked, none blocking: (1) convexity_violations returns 'interior indices': is the index zero-based (the suite and the reference use zero-based, e.g. [1, 3])? (2) the strike_cents of a convexity finding is the middle strike (Lab 1 prints 'convexity at strike 10500'), not stated in the spec; (3) which named condition wins when two fail; (4) empty chains or zero-length lists are unspecified; (5) bool and float inputs are unspecified (open items note 8)."},
 {"id": "fc2d-r2-grader-messages", "check": "2.6 item 4: failure messages name the property and never leak the answer",
  "location": "grader/test_project.py (assert messages); grader/reference.py:24-47", "status": "PASS",
  "evidence": "All assert messages describe the property (e.g. 'the list must hold every interior strike whose call lies above the chord'); --assert=plain prints only the message, so no expected value appears. Named ValueError messages name the condition (strictly increasing, df_ppm, lengths, non-negative)."},
 {"id": "fc2d-r2-grader-named-conditions-only", "check": "2.6 tests demand an exception type only for named conditions",
  "location": "grader/test_project.py:283-561", "status": "PASS",
  "evidence": "Every pytest.raises(ValueError) is for a condition the spec names (strictly increasing / positive strikes, df_ppm 1..1000000, one quote per strike, non-negative cost terms). No test requires an exception for booleans, floats or other inputs."},
 {"id": "fc2d-r2-instances", "check": "2.6 autograder item 2: instances valid, sample 20 seeds, answers change",
  "location": "grader/instance.py; grader/test_project.py:853-860", "status": "PASS",
  "evidence": f"{S}/instances_check.out and {S}/instances_check_seeds.out: all 50 seeds have strictly increasing strikes, df in 1..1000000, non-negative costs, six strikes; parity residual <= 1/2 cent except at a planted parity strike; convex calls unless a convexity violation is planted. Planted kinds over seeds 0-49: none 17, convexity 21, parity 12. 29 distinct finding sets over 50 seeds, so the answers change. Observation (not a fail): findings per seed are only 0 (22 seeds) or 1 (28 seeds), so multi-finding ordering is exercised by hand-built chains only."},
 {"id": "fc2d-r2-grader-over-constraint-case", "check": "2.6 autograder item 1/3: correct alternatives must pass (case-sensitive rule names)",
  "location": "course/modules/FC/FC2/grader/test_project.py:587-597 (test_scan_explanations_are_nonempty_and_name_the_rule)", "status": "FAIL",
  "evidence": f"Alternatives in {S}/alt/ run as scanner.py over seeds 0-49 ({S}/alt_run.sh, {S}/alt_run.out, tally {S}/alt_tally.out): alt1_decimal.py fails this test on 26 of 50 seeds, alt3_slopes.py on 40 of 50, alt5_wording_probe.py on 40 of 50. Cause: line 593 sets rule = 'convex' or 'parity' and line 594 asserts 'rule in text' case-sensitively, so a correct explanation beginning 'Convexity in strike ...' or 'Parity: ...' fails. Spec project.html:301 requires only that the explanation names the rule and the labels, not its case.",
  "fix": "Match the rule name case-insensitively (for example re.search(rule, text, re.IGNORECASE) or text.lower()); keep the label checks."},
 {"id": "fc2d-r2-grader-over-constraint-trade-verb", "check": "2.6 autograder item 1/3: correct alternatives must pass (literal trade verb)",
  "location": "course/modules/FC/FC2/grader/test_project.py:600-633 (test_parity_explanation_states_the_trade_for_the_sign_of_the_gap; regexes at lines 625 and 630)", "status": "FAIL",
  "evidence": f"{S}/alt_tally.out: alt3_slopes.py fails this test on 50 of 50 seeds (its explanation says 'the call is rich'); alt5_wording_probe.py fails it on 50 of 50 (it says 'Short the call'). Lines 625 and 630 require the literal regex \\bsell\\w*\\s+the\\s+call\\b for a positive gap and \\bbuy\\w*\\s+the\\s+call\\b for a negative gap. project.html:301 (spec) requires only the rule and labels; project.html:336 states the sign meaning, not the explanation's wording.",
  "fix": "Accept sell or short (and buy or long) for the trade, or check the sign through the rich/cheap wording as well. The test still kills r5_d, which states the call-cheap trade for a rich gap, so mutation strength is kept."},
 {"id": "fc2d-r2-alternatives-pass", "check": "2.6 five alternative correct implementations pass the suite on seeds 0-49",
  "location": f"{S}/alt/alt1_decimal.py, alt2_integer.py, alt3_slopes.py, alt4_lagrange.py, alt5_wording_probe.py", "status": "FAIL",
  "evidence": f"Results ({S}/alt_run.out): alt2_integer.py PASS 50/50; alt4_lagrange.py PASS 50/50; alt1_decimal.py, alt3_slopes.py and alt5_wording_probe.py fail only the two over-constraint tests in the two rows above (alt1 is an exact Decimal implementation, alt3 uses slope comparison, alt5 is the reference arithmetic with reworded explanations). Only two of five alternatives pass.",
  "fix": "Fix the two over-constraint tests as stated in those rows; re-run {S}/alt_run.sh 0 49 (it must report 0 failing seeds for all five)."},
 {"id": "fc2d-r2-mut-r7-docstrings", "check": "2.6 mutant format: each mutant opens with a one-line docstring describing the error",
  "location": "ledgers/FC2/mutants/r7_a_duplicate_strikes_accepted.py; r7_b_parity_loop_skips_last_strike.py; r7_c_discounted_strike_floored.py", "status": "FAIL",
  "evidence": f"ast.get_docstring returns None for all three; they open with '# Student error mutant (round 7 ...)' and '# Student error: ...' comments. {S}/mutate_graders_after_new.out prints '(no description)' for each. VERIFIER_RULES 2.6 item 3 and tools/mutate_graders.py require a one-line docstring.",
  "fix": "Replace the leading comment lines with a module docstring whose first line describes the error, for example '\"\"\"Student error: the strike check accepts equal neighbouring strikes (b < a instead of b <= a).\"\"\"'. The mutate gate stays 55/55 killed."},
 {"id": "fc2d-r2-mut-new-killed", "check": "2.6 item 3: at least three new student-error mutants of my own, each killed",
  "location": "ledgers/FC2/mutants/v07_convexity_indices_returned_in_decreasing_order.py; v08_convexity_scan_skips_first_interior_strike.py; v09_parity_explanation_omits_P3_no_income.py; v10_convexity_gross_from_rounded_chord.py", "status": "PASS",
  "evidence": f"Four new mutants written this round from the reference. {S}/mutate_graders_after_new.out: v07 killed by test_convexity_matches_oracle_on_an_uneven_grid (seed 0); v08 by test_convexity_finding_with_net_one_cent_is_returned (seed 0); v09 by test_scan_explanations_are_nonempty_and_name_the_rule (seed 1); v10 by test_convexity_half_cent_tie_rounds_once_up_at_any_discount_factor (seed 0)."},
 {"id": "fc2d-r2-mut-r5d-resolved", "check": "2.6 item 3: round-1 survivor r5_d",
  "location": "ledgers/FC2/mutants/r5_d_explanation_direction_reversed.py; grader/test_project.py:600-633", "status": "PASS",
  "evidence": f"Round-1 FAIL (mut-survivor) is resolved: {S}/mutate_graders_after_new.out shows r5_d KILLED by test_parity_explanation_states_the_trade_for_the_sign_of_the_gap (seed 0). Re-verified from scratch this round."},
 {"id": "fc2d-r2-mut-equivalents", "check": "2.6 item 3: equivalent mutants are proved and left out of the list",
  "location": "ledgers/FC2/mutants/", "status": "PASS",
  "evidence": "No mutant in the list is equivalent: each of the 55 is killed on some seed in 0-9 ({S}/mutate_graders_after_new.out). No equivalence proof is needed or recorded."},
 {"id": "fc2d-r2-cards-full-scan", "check": "2.7 full scan for duplicates and card integrity (143 cards)",
  "location": "course/modules/FC/FC2/cards.json", "status": "PASS",
  "evidence": f"{S}/cards_check.py (python -I) on 143 cards: 143 unique ids, 143 unique fronts, 143 unique backs; no duplicate. Id gaps FC2-c031 and FC2-c077 predate this round (open observation, not a fail). Topically close pairs (c055/c059 on V_A(0) >= V_E(0) and its strictness; c060, c071, c132 on early exercise) ask different questions with different claims; not duplicates."},
 {"id": "fc2d-r2-cards-refs-numbers", "check": "2.7 card references and numbers appear in their lesson",
  "location": "course/modules/FC/FC2/cards.json; L01-L08.html", "status": "PASS",
  "evidence": f"{S}/cards_check.out: every multi-digit number on every card appears in its lesson text (no NUM-MISS). Every Definition/Theorem/Proposition/Lemma/Corollary/Remark/Example/Problem label resolves: 'Problem E3', 'Problem P2', 'Problem M1..M3' exist as id attributes in their lessons; 'Section 5' is a lesson section; L04 assumptions A3 and A4 appear as 'A3 (no arbitrage).' and 'A4 (constant rate).' (wording, not a missing label)."},
 {"id": "fc2d-r2-cards-lab-numbers", "check": "2.7 cards quoting lab output: values match the twin output and a recomputation",
  "location": "cards c021, c023, c024, c027, c038, c045, c093-c095, c109-c111, c115-c118, c123, c133, c134, c136, c137",
  "status": "PASS", "evidence": f"{S}/out/*.out (twin outputs) and recomputation {S}/*.out: 5126.58 (c021); -2126.58/-626.58/873.42/2373.42 and 73.42 (c023, c024; L02 out); 237.11 with 0.25 years left, recomputed 237.1077 (c027); margin 84 and days 4,6,7,10 with -35,-13,-36,-22 (c038, c133; L03 out); -4415468 and 4902625 (c045, c134; L03 out); True x4, holdings 3/4 and -30, cost 45 (c093-c095; L06 out); -91 cents from -91.0082, and sign pattern +,-,+,-,+,-,-,-,- (c110, c111; L07 recomputed); 4-step u,d,R,q (c115); one-step 12.1623 and 1216 cents (c116); 400-step error -0.4998 cents (c117); put 5.573526 (c118); 37 halvings (c123; L08 out)."},
]
card_samples = [
 ("FC2-c010", "L01 Problem P3 and Example 3.4: 1/20 and 17/20 sum to 9/10 (checked: psi_u=(q-9/10)/2, psi_d=(27/10-q)/2 at q=1)"),
 ("FC2-c020", "L02 Remark 2.3: forward price depends only on S, r, tau"),
 ("FC2-c030", "L02 Problem R1: band [S e^{r_l tau}, S e^{r_b tau}] when r_l <= r_b"),
 ("FC2-c041", "L03 Proposition 3.2 proof: telescoping sum to 1 - DF_n"),
 ("FC2-c051", "L04 Definition 1.1: call (S-K)^+ and put (K-S)^+ payoffs"),
 ("FC2-c061", "L04 lab output: call pays 25.00 at 125, profit 17.00 after 8.00 premium (out/lab-FC2-L04-1.out)"),
 ("FC2-c071", "L05 Theorem 4.1 and Remark 4.2: date-0 equality only"),
 ("FC2-c082", "L06 Assumption A6: 0 < d < R_f < u; Definition 1.2 payoffs"),
 ("FC2-c092", "L06 Definition 3.2 backward induction"),
 ("FC2-c102", "L07 Definition 1.3 Black-Scholes call formula"),
 ("FC2-c112", "L07 Proposition 1.5 proof: d1 split"),
 ("FC2-c120", "L08 Lemma 2.1 vega = S phi(d1) sqrt(tau)"),
 ("FC2-c132", "L05 Theorem 4.1 and Remark 4.2: no early-exercise rule at later dates"),
 ("FC2-c142", "L04 A3 (no arbitrage): V0 <= 0 and X >= 0 imply V0 = 0 and X = 0"),
]
cards = json.load(open(f"{root}/course/modules/FC/FC2/cards.json", encoding="utf-8"))
byid = {c["id"]: c for c in cards}
for cid, what in card_samples:
    c = byid[cid]
    rows.append({"id": f"fc2d-r2-card-{cid.split('-')[1]}", "check": "2.7 retrieval card (sampled 1 in 10): correct against the lesson text",
                 "location": f"course/modules/FC/FC2/cards.json ({cid}); {c['lesson']}.html",
                 "status": "PASS",
                 "evidence": f"Read the cited passage in {c['lesson']}.html (scripts/card_sample_context.py): {what}. Card back: '{c['back'][:90]}...'"})
for r in rows:
    assert r.get("evidence"), r["id"]
    if r["status"] != "PASS":
        assert r.get("fix"), r["id"]
for r in rows:
    if r["status"] == "FAIL" and "{S}" in r["evidence"]:
        r["evidence"] = r["evidence"].replace("{S}", S)
    if "{S}" in r.get("fix", ""):
        r["fix"] = r["fix"].replace("{S}", S)
counts = {k: sum(1 for r in rows if r["status"] == k) for k in ("PASS", "FAIL", "UNVERIFIABLE")}
verdict = "PASS" if counts["PASS"] == len(rows) else "FAIL"
frag = {
 "unit": "FC2", "slice": "FC2-d", "round": 2,
 "verifier": "Claude Haiku 5.5, independent verifier for FC2-d round 2 (did not build FC2)",
 "pin": "c737272f", "base": "c737272f (this round's pin); round-1 fragment carries no PASS rows and records no pin, so every row was re-verified from scratch",
 "checkout": "/Users/billyribeiro/.fanout/wt/verifyD2-FC2-d",
 "scratch": "/tmp/fc2d-r2-* (alt scanners, starter, collect, mypy); none of the evidence depends on them",
 "verified_at": datetime.datetime.now(datetime.UTC).isoformat(timespec="seconds"),
 "verdict": verdict, "rows": rows, "mutants": mutants,
 "registry_flags": [], "freshness_flags": [],
 "notes": ("Round 2 on c737272f. Read the whole slice: project.html (57 KB, all lines), grader/reference.py, instance.py, starter.py and test_project.py (all lines), "
           "labs twins 1-3, the 143 cards (dump in " + S + "/cards_dump.txt), and the 13 sampled card passages. Round-1 FAIL mut-survivor (r5_d) resolved by the explanation test. "
           "New this round: over-constraint probes (5 alternatives), 4 new mutants, mutant docstring check, scope check against the curriculum brief, rubric calibration. "
           "Not checked: the full repo gate (outside slice); the live verify_refs for the whole registry; a visual check of the autograder panel in a browser; check_pages for the project alone (only --all exists in use)."),
 "summary": (f"FC2-d round 2: verdict {verdict}. {len(rows)} rows: {counts['PASS']} PASS, {counts['FAIL']} FAIL, {counts['UNVERIFIABLE']} UNVERIFIABLE. "
             f"Mutants: {sum(1 for m in mutants if m['killed_by'])}/{len(mutants)} killed (55 with 4 new this round). Blocking FAILs: grader over-constraints (case-sensitive rule names; literal 'sell' wording), "
             "2 of 5 alternatives pass, three r7 mutants without docstrings, rubric C2 level 2 vague, Rung 3 input differs from the curriculum brief (architect decision)."),
}
path = f"{root}/ledgers/FC2/FC2-d.json"
json.dump(frag, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("wrote", path, "rows", len(rows), counts, "mutants", len(mutants), "verdict", verdict)
