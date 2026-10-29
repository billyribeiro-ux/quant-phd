import json, sys
R9 = "Carried from round 9 (cited subject byte-identical since pin 33744e5; "
ROOT = "/Users/billyribeiro/.fanout/wt/verifyC10-E3-a/"
rows = []
def row(i, check, loc, status, ev):
    rows.append({"id": i, "check": check, "location": loc, "status": status, "evidence": ev})

# command rows (re-run on pin fa61d6e)
row("E3a-cmd-check_pages", "tools/check_pages.py --unit E3", "course/modules/E/E3/index.html, L01.html, L02.html, L03.html", "PASS",
    "Re-run at fa61d6e: 'check_pages E3: PASS', exit 0 (ledgers/E3/scripts/E3-a-r10/check_pages.out).")
row("E3a-cmd-check_dag", "tools/check_dag.py --all", "course/modules/E/E3/*.html", "PASS",
    "Re-run: 'check_dag E3: PASS' (check_dag.out line 5), all 14 units PASS, exit 0.")
row("E3a-cmd-run_labs", "tools/run_labs.py --unit E3", "L01.html, L02.html, L03.html", "PASS",
    "Re-run: 'run_labs E3: PASS (11/11)', exit 0 (run_labs.out).")
row("E3a-cmd-twin-isolated", "python -I -W error on each twin", "tests/labs/E3/lab-E3-L01-1.py, L02-1.py, L03-1.py", "PASS",
    "Re-run from /tmp with python3 -I -W error: exit 0 for all three; stderr 0 bytes (twin_L0{1,2,3}.out/.err).")
row("E3a-cmd-pytest-labs", "pytest tests/test_labs.py -k E3 -q", "tests/test_labs.py", "PASS",
    "Re-run: 15 dots, [100%], exit 0 (pytest_labs.out).")
row("E3a-cmd-ruff-mypy", "ruff check and ruff format --check on tests/labs/E3; mypy --no-incremental on the three slice twins", "tests/labs/E3/*.py", "PASS",
    "Re-run: 'All checks passed!', '11 files already formatted', 'Success: no issues found in 3 source files'; all exit 0 (ruff.out, mypy.out).")
row("E3a-cmd-offline-registry", "tools/verify_refs.py --offline", "references/references.json", "PASS",
    "Re-run: 'offline integrity: 560 entries, 0 problems', exit 0 (verify_refs_offline.out).")
row("E3a-cmd-page_smoke", "tools/page_smoke.py --unit E3", "index.html, L01-L03 and rest of E3", "PASS",
    "Re-run: 'page_smoke E3: PASS', exit 0 (page_smoke.out, 45 lines).")
row("E3a-cmd-verify_refs-live", "plain curl of the five registry DOIs cited by the hub and L02", "references/references.json", "PASS",
    R9 + "references/ byte-identical 33744e5..fa61d6e, checked with git diff --quiet). Not re-run live in this round.")

# page vs twin, re-run
row("E3a-page-vs-twin", "page code equals twin; expected block equals isolated twin output", "L01.html, L02.html, L03.html vs tests/labs/E3/lab-E3-L0{1,2,3}-1.py", "PASS",
    "Re-run page_vs_twin.py (copied from E3-a-r9): L01/L02/L03 code==twin True, expected==output True (page_vs_twin.out).")

# hub
row("E3a-hub-structure", "hub structure, hours, placement, ladder, data status, reading list, prerequisites and unlocks", "course/modules/E/E3/index.html", "PASS",
    R9 + "index.html and tests/labs/E3/lab-E3-L0{1,2,3}-1.py byte-identical; git diff --quiet 33744e5 fa61d6e).")
row("E3a-numbers-hub", "numbers in hub prose, placement answers and explanations", "course/modules/E/E3/index.html", "PASS",
    R9 + "index.html byte-identical).")

# numbers and math on changed text
row("E3a-numbers-L01", "numbers in L01 prose, Example 1.4, Example 3.4, Lab 1 claims, problems, quiz", "course/modules/E/E3/L01.html (delta hunk line 405, P3 solution); tests/labs/E3/lab-E3-L01-1.py", "PASS",
    "Re-verified the changed P3 solution: x_i = 2^i, p_i = 2^-i for i>=1 gives sum p_i = 1 (geometric series) and sum p_i u(x_i) = sum 1, which diverges for u(x)=x. Unchanged numbers in Example 3.4 (E = 150 CU, 37500 CU^2) match twin_L01.out lines 4-11.")
row("E3a-numbers-L02", "numbers in L02 prose, Example 1.5, Example 2.3, Prop 3.1 approximation, Lab 1 claims, problems E1-E3", "course/modules/E/E3/L02.html lines 51, 159, 209; ledgers/E3/scripts/E3-a-r10/rederive.out, twin_L02.out", "PASS",
    "Re-verified changed text: Example 2.3 r_A = 1/(2w) = 0.005 and r_R = 0.5 at w = 100 (twin_L02.out line 2); pratt 4.500000 = 0.5*0.005*1800 (rederive.out); 'five scales' = Part B eps 1, 0.5, 0.25, 0.1, 0.01 (twin_L02.out lines 7-11); CE 94.934 < 100 and premium 5.066 > 4.5 (rederive.out lines 2-3).")
row("E3a-numbers-L03", "numbers in L03 prose, Example 2.5, Lab 1 printed values, E1-E3, misconceptions", "course/modules/E/E3/L03.html line 90 (Def 1.3 paragraph); ledgers/E3/scripts/E3-a-r10/rederive.out", "PASS",
    "Changed Def 1.3 paragraph has no numeric claim beyond u_gamma(1)=0 (exact) and the constant -1/(1-gamma). Lab values rederived: CE 11250, 10000, 8888.8889, 7337.6161 (rederive.out lines 8-13); 80000/9 and 9/80000 (rederive.out lines 14-15).")
row("E3a-math-L01", "L01 proofs and statements: Props 2.2, 2.3, 3.1, 3.3, Def 3.2, Problems P1-P3, R1-R3", "course/modules/E/E3/L01.html (P3 solution, line 405; Prop 2.3 proof; Def 3.2 line 143)", "PASS",
    "Changed P3 solution checked: the step that fails is the split of the sum into two series (needs convergence); the counterexample is valid. Def 3.2 (line 143) matches card E3-c006 after the edit. Other L01 proofs byte-identical in the delta.")
row("E3a-math-L02-proofs", "L02 proofs and statements: Props 1.1, 1.3 (a) and (b), 2.2, 3.1, Remark 3.2, Problems M1-M3, P1-P3, R1-R3", "course/modules/E/E3/L02.html lines 51 (Prop 1.3 hypotheses), 159 (Example 2.3)", "PASS",
    "Changed statements re-checked: 'Given F1, F2 and F5 and A1 to A3 ... it proves u'' <= 0 (A2) gives CE <= E X' matches Prop 1.3(a) hypotheses at line 104. Example 2.3 algebra: u' = w^(-1/2)/2, u'' = -w^(-3/2)/4, r_A = 1/(2w), r_R = 1/2. Unchanged proofs carried from round 9 (cited hunks outside 48-51, 156-159, 206-209).")
row("E3a-math-L03-proofs", "L03 proofs and statements: Props 1.2, 1.4, 1.7, 2.4, 2.6, 2.7, Thm 2.1, Remark 2.8, Problems M1-M3, P1-P3, E1-E3, R1-R3", "course/modules/E/E3/L03.html line 90 (Def 1.3 paragraph)", "PASS",
    "Changed Def 1.3 paragraph: (w^(1-g)-1)/(1-g) = w^(1-g)/(1-g) - 1/(1-g), a positive-coefficient (a=1) affine shift, so Prop 2.7 (line 173, a>0, b real) applies and CE is unchanged; Prop 1.4 uses the subtracted form for the limit (line 95, 102). Other proofs carried (delta hunks outside them).")

# lab rows
row("E3a-lab-L01", "L01 lab and expected block", "tests/labs/E3/lab-E3-L01-1.py; L01.html Lab 1 section", "PASS",
    R9 + "lab-E3-L01-1.py byte-identical; the L01 delta is line 405 only, outside the lab). Re-run twin and page_vs_twin PASS.")
row("E3a-lab-L02", "L02 lab and expected block", "tests/labs/E3/lab-E3-L02-1.py; L02.html lines 207-382 (hypothesis paragraph line 209)", "PASS",
    "Re-verified changed hypothesis line 209: 'Under u(w)=w the premium is zero at each printed scale' matches Part C (three scales 1.0, 0.5, 0.1, twin_L02.out lines 13-16). 'Shrinks at each printed scale' matches gaps_shrink_as_eps_falls True. Expected block equals twin output (page_vs_twin).")
row("E3a-lab-L03", "L03 lab and expected block", "tests/labs/E3/lab-E3-L03-1.py; L03.html lines 187-324", "PASS",
    R9 + "lab-E3-L03-1.py byte-identical; the L03 delta is line 90 only). Re-run page_vs_twin PASS.")

row("E3a-grades", "grades on hub and L01-L03", "index.html, L01.html, L02.html, L03.html", "PASS",
    "Carried: grade markup in the delta hunks is unchanged (no data-grade attributes changed in L01 line 405, L02 lines 51/159/209, L03 line 90). Tables at L02 lines 523-527 unchanged.")
row("E3a-citations-pratt", "Pratt citation and reading list", "L02.html References section; index.html reading list", "PASS",
    R9 + "index.html byte-identical; L02 References not in the delta).")
row("E3a-notation", "every symbol and macro against notation/notation.json", "index.html, L01-L03", "PASS",
    "Re-checked new symbols: u_{1/2} (gamma local, allowed per notation.json 'about'), 2^i, 2^{-i}, A2 as a lesson-local label. No registered symbol takes a new meaning. Note (not a row FAIL): assumption labels A1/A2 are lesson-local and reused across lessons with different content (L02 A2 = concavity, L03 A2 = limit of (e^h-1)/h); cards E3-c018 and E3-c052 qualify them by lesson. Flagged for Architect ruling only.")
row("E3a-dag-crossunit", "concepts used outside the prerequisite closure", "index.html, L01-L03", "PASS",
    "check_dag E3: PASS. New L02 Example 2.3 names L03 Definition 1.3 (same unit, explicit lesson pointer, not a DAG link; grep shows no data-concept link to crra-utility in L02).")
row("E3a-banned-phrases", "check_pages banned strings", "index.html, L01.html, L02.html, L03.html", "PASS",
    "Re-run check_pages --unit E3: PASS.")
row("E3a-prose-process-words", "no process words in learner text", "index.html (lines 63, 111-120), L01.html line 55, L02.html line 51, L03.html lines 95, 467", "PASS",
    "Re-read the changed sentences (L01 line 405, L02 lines 51, 159, 209, L03 line 90): no process words; 'Before running it, the hypothesis is this' is the existing lab template in L02 line 209 and is unchanged in wording.")
row("E3a-L03-remark-2.2-sentence", "L03 Remark 2.2 does not claim an investor has CRRA", "course/modules/E/E3/L03.html line 139", "PASS",
    R9 + "L03 line 139 not in the delta hunk at line 90).")
row("E3a-L02-key-result-hypothesis", "L02 key-results hypotheses", "course/modules/E/E3/L02.html key-results table (lines 523-527)", "PASS",
    R9 + "lines 523-527 outside the delta hunks 48-51, 156-159, 206-209).")
row("E3a-L02-unnumbered-calculus-facts", "calculus facts used without a label", "course/modules/E/E3/L02.html F1-F6 (lines 56-62)", "PASS",
    R9 + "F1-F6 block outside the delta hunks).")
row("E3a-L03-unnumbered-mvt", "mean value theorem used as a fact", "course/modules/E/E3/L03.html lines 66, 134", "PASS",
    R9 + "lines 66, 134 outside the delta hunk at line 90).")
row("E3a-L02-uses-standard-deviation", "standard deviation usage", "course/modules/E/E3/L02.html, L01/L03, index.html", "PASS",
    R9 + "no changed hunk uses or defines standard deviation; hunks at 51, 159, 209 checked).")
row("E3a-L02-F1-hypothesis-omitted", "Prop 1.1 and Prop 1.3 hypotheses carry F1/F2/F5", "course/modules/E/E3/L02.html lines 88-106", "PASS",
    "Re-verified: Prop 1.1 (line 89) 'Assuming F1 and F5, under A1 to A3'; Prop 1.3 (line 104) 'Assuming F1, F2 and F5, under A1 to A3'; the new why-it-matters line 51 carries the same hypotheses.")
row("E3a-L02-quiz-q7-distractor", "L02 quiz q7 explanation for v = e^u", "course/modules/E/E3/L02.html line 586", "PASS",
    R9 + "line 586 outside the delta hunks).")

# cards
row("E3a-cards-hypotheses-omitted", "cards carry the hypotheses of the proposition they cite (rule 10)", "course/modules/E/E3/cards.json E3-c052 (L03 Prop 1.4); all grade-T cards of L01-L03", "PASS",
    "Round-9 FAIL fixed. E3-c052 back now begins 'Assuming A2 (the limit of (e^h - 1)/h at 0 is 1)', matching L03.html line 95 ('Assuming A2') and A2 at line 59. All 23 grade-T L01-L03 cards were read in full: c007-c015, c019, c022, c023, c025-c027, c029-c031, c037, c040, c041, c043, c046-c049, c051, c053, c055 carry their hypotheses or a precise front-stated domain (c013 'on a fixed finite set'; c043 'Assuming F1 and F2 ... A3 and A4'; c040 front 'Assuming A2').")
row("E3a-cards-agree-current-text", "cards agree with the current L01-L03 text", "course/modules/E/E3/cards.json (59 L01-L03 cards)", "PASS",
    "Re-verified the three changed L01-L03 cards against current text: c006 (L01 Def 3.2 line 143, now a subset of it); c017 (L01 Part B, six True lines, twin_L01.out lines 6-12); c052 (L03 Prop 1.4). The other 56 L01-L03 cards are byte-identical (git diff 33744e5..fa61d6e touches only cards c006, c017, c052 in L01-L03; other hunks are L04, L07 and new c167). Cards c026, c030, c039 re-checked against changed Example 2.3 and Def 1.3 text: still agree.")
row("E3a-cards-count", "card count and per-lesson coverage", "course/modules/E/E3/cards.json", "PASS",
    "Re-counted: L01 17, L02 21, L03 21 (59 total); no duplicate ids across the 163-card file (checked by script).")
row("E3a-prose-L02-F1-space", "L02 Prop 1.1 proof uses F1 correctly", "course/modules/E/E3/L02.html lines 92-95", "PASS",
    R9 + "lines 92-95 outside the delta hunks).")
row("E3a-hub-logit-before-definition", "logit is defined before use", "course/modules/E/E3/index.html lines 114-120; project.html lines 53, 103, 212", "PASS",
    R9 + "index.html byte-identical; project.html delta hunks are at lines 141, 202, 376, 741, outside 53, 103, 212).")
row("E3a-cards-c035-stale", "card E3-c035 matches Lab 1 Part C output", "course/modules/E/E3/cards.json E3-c035; tests/labs/E3/lab-E3-L02-1.py; ledgers/E3/scripts/E3-a-r10/twin_L02.out", "PASS",
    "Re-verified against twin_L02.out lines 13-16: linear premium 0 cents at eps 1.0, 0.5, 0.1 and linear_premium_zero_at_three_scales True. Card agrees.")
row("E3a-cards-c037-letters", "card E3-c037 and L03 line 77 agree on letters and statement", "course/modules/E/E3/cards.json E3-c037; L03.html line 77", "PASS",
    R9 + "card E3-c037 and L03 line 77 outside the delta hunk at line 90).")
row("E3a-cards-c017-grade", "card E3-c017 grade matches its basis (rule 9)", "course/modules/E/E3/cards.json E3-c017; L01.html lines 161-163 and 325", "PASS",
    "Round-9 FAIL fixed. E3-c017 now has grade C with basis 'Lab 1, part B'. Its 'All six comparisons print True' is read off the Part B output (twin_L01.out lines 6-12; interpretation at L01.html line 325). The identity itself is cited as Proposition 2.3 but is not the graded claim, which is the printed output. Grade C matches rule 9.")
row("E3a-cards-c055-source", "card E3-c055 cites Problem E2 and Lab 1 for 80000/9 and 9/80000", "course/modules/E/E3/cards.json E3-c055; L03.html Problem E2 (lines 419-423) and Lab 1 output (line 312)", "PASS",
    R9 + "E3-c055 and L03 lines 312, 419-423 outside the delta hunk at line 90). Rederived 80000/9 and 9/80000 (rederive.out lines 14-15).")
row("E3a-hub-privacy-claim", "hub claim that the project page says nothing sends answers anywhere", "course/modules/E/E3/index.html line 154; course/modules/E/E3/project.html line 197", "PASS",
    R9 + "index.html byte-identical; project.html line 197 'nothing on this page sends them anywhere.' is outside the delta hunks at 141, 202, 376, 741).")
row("E3a-rederive-prose-numbers", "every prose number in the slice re-derived from Python and exact arithmetic", "index.html, L01-L03", "PASS",
    "Re-ran rederive.py (copied from E3-a-r9): sqrt CE 94.9342, premium 5.0658, ratios 5.065835, 4.619495, 4.528811, 4.504565, 4.500046; CRRA CE 11250.0000, 10931.7733, 10615.8009, 10000.0000, 8888.8889, 7337.6161; 80000/9 and 9/80000 exact; r_A(100) = 0.005. All match the prose.")

# new rows for this round's delta
row("E3a-r10-delta-L01-P3-countable-counterexample", "the new P3 solution's counterexample is a valid countable lottery with divergent expected utility", "course/modules/E/E3/L01.html line 405", "PASS",
    "x_i = 2^i, p_i = 2^-i for i >= 1: p_i >= 0 and sum p_i = 1 (geometric series with ratio 1/2 summing from i = 1 to 1). With u(x) = x, p_i u(x_i) = 1 for each i, so the series diverges. Valid.")
row("E3a-r10-delta-L02-example-2.3", "new Example 2.3 wording: sqrt is an affine image of CRRA u_{1/2}, so it is the CRRA case gamma = 1/2", "course/modules/E/E3/L02.html line 159", "PASS",
    "u_{1/2}(w) = (w^{1/2} - 1)/(1/2) = 2 sqrt(w) - 2, so sqrt(w) = (u_{1/2}(w) + 2)/2, an affine image with positive coefficient 1/2 (Def 1.3 at L03 line 90). The gamma = 1/2 identification is correct.")
row("E3a-r10-delta-L02-lab-hypothesis", "new Lab 1 hypothesis: 'premium is zero at each printed scale' and 'shrinks at each printed scale' match the printed output", "course/modules/E/E3/L02.html line 209; ledgers/E3/scripts/E3-a-r10/twin_L02.out", "PASS",
    "Part C prints three scales (1.0, 0.5, 0.1) with linear premium 0; Part B prints five scales (1, 0.5, 0.25, 0.1, 0.01) with gaps 0.565835, 0.119495, 0.028811, 0.004565, 0.000046, which shrink; gaps_shrink_as_eps_falls True.")
row("E3a-r10-delta-L03-def1.3-cross-refs", "new Def 1.3 cross-references: Prop 2.7 of this lesson (affine a>0) and L02 Prop 2.2 with b = 1", "course/modules/E/E3/L03.html line 90", "PASS",
    "L03 line 173 is Prop 2.7 (affine transformations leave CE unchanged, a > 0); L02 line 148 is Prop 2.2 (invariance under positive affine transformations, b > 0, b = 1 case). Both references resolve to the stated results.")
row("E3a-r10-cards-c006-definition", "card E3-c006 agrees with L01 Definition 3.2 after the edit", "course/modules/E/E3/cards.json E3-c006; L01.html line 143", "PASS",
    "Card now states only 'u(x) = b x with b > 0. Its expected utility is b times the expected value (Definition 3.2)', which is the first half of Definition 3.2's statement at line 143. No claim was removed that the page does not also make.")

frag = {
    "unit": "E3", "slice": "a", "round": 10,
    "verifier": "Haiku independent verifier, E3-a round 10 (did not build E3)",
    "pin": "fa61d6e",
    "base": "33744e5 (round-9 pin). Delta 33744e5..fa61d6e touches for this slice: L01.html line 405 (P3 solution), L02.html lines 51, 159, 209, L03.html line 90 (Def 1.3 paragraph), cards.json (c006 and c017 in L01, c052 in L03; other hunks are L04, L07 and new c167). index.html and tests/labs/E3/lab-E3-L0{1,2,3}-1.py are byte-identical (git diff --quiet). references/ byte-identical. Not in slice and changed: project.html, tests/labs/E3/lab-E3-project-2.py, plans/E3-open-items.md, grader/test_project.py.",
    "checkout": ROOT.rstrip("/") + " (detached at fa61d6e)",
    "scratch": "ledgers/E3/scripts/E3-a-r10/ (scripts and outputs; rederive.py and page_vs_twin.py copied from E3-a-r9)",
    "verified_at": "2026-10-29",
    "verdict": "PASS",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": "Mutation testing not required: slice a holds the hub and lab twins (demonstrations), and mutation applies only to project graders (verifier rules ruling). Round-9 FAIL rows E3a-cards-hypotheses-omitted and E3a-cards-c017-grade are fixed and re-verified PASS. Observation for Architect (not a row FAIL): assumption labels A1 and A2 are lesson-local and reused across L02/L03 with different content; the cards qualify them by lesson. Not checked: verify_refs live curl run (carried, references/ unchanged); browser rendering beyond page_smoke; run_graders and check_projects (project slice, not this slice); the full text of every non-changed L01-L03 proof was carried from round 9, not re-read in this round.",
    "summary": "",
}
n = sum(1 for r in rows if r["status"] == "PASS")
frag["summary"] = f"E3-a round 10: verdict PASS. {len(rows)} rows; {n} PASS, 0 FAIL. Round-9 FAILs E3a-cards-hypotheses-omitted and E3a-cards-c017-grade fixed and re-verified. Commands re-run at fa61d6e: check_pages, check_dag, run_labs, twin isolation, pytest E3 labs, ruff, mypy, verify_refs offline, page_smoke, page_vs_twin, rederive."
json.dump(frag, open(ROOT + "ledgers/E3/E3-a.json", "w"), indent=2, ensure_ascii=False)
print("written", len(rows))
