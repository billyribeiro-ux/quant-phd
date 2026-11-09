"""Writes the round-1 fragment for M7 slice c (L07, L08, their twins and cards). Rows carry evidence; no row is asserted without a check."""
import json
from datetime import datetime, timezone
from pathlib import Path

S = "ledgers/M7/scripts/M7-c-r1"
SC = f"{S}/"
rows = [
    ("M7c-r1-cmd-check_pages", "tools/check_pages.py --unit M7", "index, L01-L08, project, cards", "PASS",
     f"Run at aeb512b6: `python tools/check_pages.py --unit M7` -> 'check_pages M7: PASS', exit 0 ({SC}commands_output.txt)."),
    ("M7c-r1-cmd-check_dag", "tools/check_dag.py --unit M7", "DAG of M7", "PASS",
     f"Run at aeb512b6: `python tools/check_dag.py --unit M7` -> 'check_dag M7: PASS', exit 0 ({SC}commands_output.txt)."),
    ("M7c-r1-cmd-run_labs-L07", "tools/run_labs.py --unit M7 --page L07", "L07.html lab-M7-L07-1", "PASS",
     f"Run: 'run_labs M7: PASS (1/1)', exit 0 ({SC}commands_output.txt)."),
    ("M7c-r1-cmd-run_labs-L08", "tools/run_labs.py --unit M7 --page L08", "L08.html lab-M7-L08-1", "PASS",
     f"Run: 'run_labs M7: PASS (1/1)', exit 0 ({SC}commands_output.txt)."),
    ("M7c-r1-twins-alone-python-I-W-error", "python3 -I -W error on tests/labs/M7/lab-M7-L07-1.py and lab-M7-L08-1.py", "tests/labs/M7/lab-M7-L07-1.py, lab-M7-L08-1.py", "PASS",
     f"Both exit 0 under -I -W error (commands_output.txt). Stdout compared to page expected blocks by {SC}cmp_twin_page.py: 'expected == twin stdout: True' for L07 (page lines 299-318) and L08 (page lines 285-310) ({SC}cmp_twin_page_output.txt)."),
    ("M7c-r1-page-code-equals-twin", "course/modules/M/M7/L07.html:150-298, L08.html:150-284 vs twins", "L07.html, L08.html", "PASS",
     f"{SC}cmp_twin_page.py: page code equals twin after stripping the twin's final newline (True for both; the page embeds no trailing newline). No @@ markers remain on the pages (embedded). Pytest lab cases pass."),
    ("M7c-r1-expected-equals-output", "page expected blocks vs twin stdout", "L07.html:299-318, L08.html:285-310", "PASS",
     f"Compared line by line in {SC}cmp_twin_page_output.txt ('expected == twin stdout: True' both). Printed values also re-derived in {SC}indep_L07_L08_output.txt (exact Fraction and int arithmetic written from the prose)."),
    ("M7c-r1-cmd-ruff", "ruff check / ruff format --check on the two twins", "tests/labs/M7/lab-M7-L07-1.py, lab-M7-L08-1.py", "PASS",
     "'All checks passed!' and '2 files already formatted', exit 0 (commands_output.txt)."),
    ("M7c-r1-cmd-mypy-strict", "mypy --no-incremental --strict on the two twins", "tests/labs/M7/lab-M7-L07-1.py, lab-M7-L08-1.py", "PASS",
     "'Success: no issues found in 2 source files', exit 0 (commands_output.txt)."),
    ("M7c-r1-cmd-pytest-lab-cases", "pytest tests/test_labs.py -k 'lab-M7-L07-1 or lab-M7-L08-1'", "test_labs parametrization", "PASS",
     f"'2 passed, 357 deselected'; re-run exit 0 ({SC}pytest_output.txt)."),
    ("M7c-r1-cmd-page_smoke", "tools/page_smoke.py --unit M7 --pages L07 L08", "L07.html, L08.html (Pyodide, light/dark, 360 px)", "PASS",
     f"'page_smoke modules/M/M7/L07.html: PASS', 'page_smoke modules/M/M7/L08.html: PASS', 'page_smoke M7: PASS', exit 0; lab runtime 0.0 s each ({SC}page_smoke_output.txt)."),
    ("M7c-r1-cmd-verify_refs-offline", "tools/verify_refs.py --offline", "registry", "PASS",
     "'offline integrity: 560 entries, 0 problems', exit 0. The slice pages cite no registry key (`<ol data-references></ol>` empty at L07.html:556 and L08.html:539; no Boyd/Stokey text on either page), so no citation row is needed. Live Crossref run not repeated (no citation in slice)."),
    ("M7c-r1-numbers-L07-prose", "L07.html prose and tables", "L07.html:52,56,60-75,87-145,149,319,324,333,342,346,350,415,422,427-429,365,372,379,390,404,447,454", "PASS",
     f"Each number re-derived with {SC}indep_L07_L08.py (output {SC}indep_L07_L08_output.txt): V_t(400) column 240,220,200,130,4 (class a, lab-printed L07.html:300-304); V0-V3=110; diffs 20,20,70,126; 13/24=0.5417; C(8,4)=70; greedy 130; optimal 240; M1 values 5,3,10; M3 totals 6,9,10; R2 totals max{10,5}=max{10,3}=10; Remark 2.5 values 0 and 1. (a)/(b)/(c) classes all match."),
    ("M7c-r1-numbers-L08-prose", "L08.html prose, tables and solutions", "L08.html:52,56,62-64,149,285-310,311,320,345-419,428,442,454-462", "PASS",
     f"Re-derived in {SC}indep_L07_L08_output.txt with Fraction: V_0(0)=1394889/100000=13.948890, V_1(0)=13.3584, V_4(0)=9.6, V_5(0)=6.0, V_5(1)=4, V_5(2)=1; V_4(0)=9.6 (run) vs 1.4 (repair); changes 6, 18/5, 137/50, 1233/500, 11097/5000, 99873/50000 printed as 6.0,3.6,2.74,2.466,2.2194,1.99746; ratios 0.6, 0.7611, 0.9, 0.9, 0.9; 378 = 3*126; 18 pairs; tie count 0; V0(0)-V1(0)=0.590490; V4(0)-V5(0)=3.6; M2 V0(x)=7/2, V0(y)=9/2; M3 3.5; negative-beta totals 0,-1,1,0, V0=1, U1=1, U0=0 (L08.html:320). All match."),
    ("M7c-r1-math-L07-theorems", "L07.html Def 1.1-1.4, Remark 1.3, Thm 2.1-2.3, Cor 2.4, Remark 2.5", "L07.html:58-145, 322-325", "PASS",
     "Re-derived every proof line by line: downward induction (Thm 2.1, 96-105), continuation splitting with feasibility (Thm 2.2, 115-120), chain J<=r+V<=V_t with both equalities (Thm 2.3, 130-134), induction on H-t (Cor 2.4, 143-144). Remark 1.3 witness and Remark 2.5 counterexample checked (values match). Hypotheses stated: finiteness for maxima; the infinite-action caveat is explicit."),
    ("M7c-r1-math-L08-theorems", "L08.html Def 1.1-1.2, Thm 1.3-1.4, Remark 1.5, Lemma 2.2, Def 2.1, Prop 2.3, Remark 2.4, Section 3", "L08.html:58-145, 320", "PASS",
     "Re-derived: split of discounted total with beta multiplying the tail (Thm 1.3, 85-87) and the only sign use stated; uniqueness by downward induction (Thm 1.4, 97-101); Remark 1.5 family (1+c,c) verified; Lemma 2.2 index shift (129) and Prop 2.3 induction (139) verified; Section 3 counterexample at beta=-1 verified (totals 0,-1,1,0; U_0=0 != V_0=1). Hypothesis beta>=0 stated where used (Thm 1.3, 1.4, Prop 2.3, Key results)."),
    ("M7c-r1-math-problem-sets-L07", "L07.html problem set M1-M3, P1-P3, E1-E3, R1-R3", "L07.html:361-456", "PASS",
     "Each solution recomputed (M1 5/3/10; M2 optimal (v,v) total 10; M3 plans 6,9,10 and (u,v) infeasible; P1-P3 proofs; E1 126; E2 13/24; E3 C(8,4); R2 counterexample verified by enumeration of both plans; R3 m^(H-t) count). R1 is a research answer whose sup-argument is valid (definition of sup). Wording note only (see notes)."),
    ("M7c-r1-math-problem-sets-L08", "L08.html problem set M1-M3, P1-P3, E1-E3, R1-R3", "L08.html:349-444", "PASS",
     "M1 V_4(0)=9.6 and repair 1.4; M2 3.5, 4.5, 2, 3; M3 3.5; P1 unique solution at H=1; P2 identical totals; P3 c=0 gives U_0=1; E1 0.590490 and 3.6; E2 ratios; E3 378; R1 sign analysis (beta enters algebraically; only max-times-beta step uses sign); R2 U^2 formula (exponents beta^0, beta^1, beta^2); R3 u_n=1/n: |u_n-0| = (n+1)*|u_{n+1}-u_n|, unbounded ratio, so no constant bound. All verified."),
    ("M7c-r1-lab-L07-claims", "L07.html:149 hypothesis, 163-165 docstring, 319 interpretation, 342/346/350 misconceptions", "L07.html:149-165, 319, 342-350", "PASS",
     f"Every printed-line claim checked against the expected block (L07.html:299-318): V0(400)=240 (line 300-304 table; Part C optimal_total 240); plans_checked 70; recursion True; optimal_consumption 100 100 100 100; tails True; greedy 400 0 0 0, greedy_total 130; greedy_tail t=1,2,3 True; greedy_plan_optimal False. Code docstrings match code (tail loop L286, greedy tails L292-294). The 20 pairs (L07.html:149) = 4 times x 5 wealth values, matching loops L273-276."),
    ("M7c-r1-lab-L08-claims", "L08.html:149 hypothesis, 158-164 docstring, 311 interpretation, 321 ties, 330-338 misconceptions", "L08.html:149-164, 311, 321, 330-338", "PASS",
     "Expected block (L08.html:285-310) matches the claims: t=0 state 0 = 13.948890; policy s2 repair t=0..3, run t=4,5; tied_pairs 0; plans_enumerated 378; recursion True (18 pairs in code, loop L264-268); changes 6.0..1.99746; iterate_equals True. Docstrings (L158-164) match code: value table t=0..6, policy t=0..5 with ties, Part C from U^0=0 checks U^n = V_(H-n) (L280). 'does not show the iteration converges' is consistent with no limit printed."),
    ("M7c-r1-lab-L07-check-probe", "lab-M7-L07-1 mutation probe (lab checks named in L07.html:163-165, 319)", f"{SC}lab_mutants.py, {SC}lab_mutants_output.txt", "PASS",
     "Five mutants of the L07 twin (min for max; brute force drops bequest; recursion ignores future; tail check hard-coded True; greedy check inverted). Killed by output change: min-for-max (recursion False), recursion ignores future (False), inverted greedy check (greedy_plan_optimal True). Survived with identical printed output: brute force drops bequest (bequest never binds on this instance: consumption dominates), hard-coded True tail check (the computed value is also True). Neither survivor contradicts a lesson sentence; the lab is a demonstration (verifier ruling), and the lesson claims the comparison and the tail check, not detection of every fault."),
    ("M7c-r1-lab-L08-check-probe", "lab-M7-L08-1 mutation probe (lab checks named in L08.html:158-164, 311, 321)", f"{SC}lab_mutants.py, {SC}lab_mutants_output.txt", "PASS",
     "Five mutants of the L08 twin: min for max in bellman_step (recursion False); brute force without discount weight (False); iterate starts from 1 (iterate False); discount 1 in iteration only (False); tie count forced to 0 (output identical). The tie-count survivor is output-identical on this instance because no tie exists; L08.html:321 says Lab 1 prints no tie and does not illustrate that case, so no sentence claims detection."),
    ("M7c-r1-lab-seeded-no-network", "twins imports and RNG use", "tests/labs/M7/lab-M7-L07-1.py:168-170, lab-M7-L08-1.py:167-170", "PASS",
     "Imports are __future__, itertools, fractions only; no random module; no network; both labs labelled SIMULATED (L07.html:149, L08.html:149). Runtime 0.0 s in page_smoke."),
    ("M7c-r1-grades-L07", "BLUEPRINT grades on L07 claims and key-results table", "L07.html:87-140 (theorem blocks), 466-470 (key results), cards.json L07 ids", "PASS",
     "Theorems 2.1-2.3, Cor 2.4, Remark 2.5, Remark 1.3 are proved on the page: grade T is correct. Lab-read numbers and lab-read misconception answers are C naming Lab 1 (verifier ruling 9). No claim is graded above its evidence."),
    ("M7c-r1-grades-L08", "BLUEPRINT grades on L08 claims and key-results table", "L08.html:76-145, 448-462", "PASS",
     "Theorems 1.3, 1.4, Remark 1.5, Lemma 2.2, Prop 2.3 proved on page (T). Lab numbers C naming Lab 1. Infinite-horizon result not stated (architect Q2); the statement 'not treated here' appears at L08.html:52, 144, 317, 538. No graded claim relies on a source."),
    ("M7c-r1-dag-concept-links", "concept links and dfn in L07/L08", "L07.html:38-39, 84, 52; L08.html:38-39, 69, 84", "PASS",
     "Links: mathematical-induction (M1, in closure, link to concepts.html#mathematical-induction, anchor present) and principle-of-optimality/bellman-equation (own dfn: L07 line 79, L08 line 69). No link to any out-of-closure concept. dynamic programming appears only in the L07 title and nav text (prose, no link or dfn, Q12). 'value iteration' is defined on-page at L08.html:119 (Def 2.1) with no link; its curriculum namesake value-function-iteration (curriculum/01-foundations.yaml:249) is an M5 concept with a certified error bound, which L08 does not claim. Treated as on-page prose per plan 3/B2. Flagged for architect Q12 confirmation (notes)."),
    ("M7c-r1-forward-reference-bellman", "L07.html:52, 84 forward reference to L08 Def 1.2", "L07.html:52,84", "PASS",
     "L07 uses 'Bellman equation' before L08 defines it, but only as an explicit pointer ('Lesson L08 calls ... the Bellman equation (its Definition 1.2)'), not a link or a use without definition. Verified that L08 Definition 1.2 (L08.html:67-74) is the Bellman equation."),
    ("M7c-r1-notation", "notation/notation.json vs symbols used on L07/L08", "L07.html, L08.html math", "PASS",
     "Registered symbols (T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q}) do not appear on either page (token extraction in notes). Only the registered macro \\R is used. Conventional local letters (S, A, f, r, B, H, V, J, W, m, U, G, C, beta, Sigma) are defined in the lesson where used (L07 Def 1.1, L08 line 56 and Lemma 2.2 line 124, R3 m, Def 2.1 G). No symbol is reused with a second meaning within a lesson."),
    ("M7c-r1-banned-process-words", "BUILDER_RULES 1.3-1.4 banned phrases and process words", "L07.html, L08.html", "PASS",
     "Grep for TODO, TBD, lorem, 'for brevity', 'details omitted', 'beyond the scope', 'left as an exercise', 'you can add more', 'it is important to note', 'studies show', 'experts agree', 'it is well known', obviously, clearly, builder, verifier, ledger, round, architect, draft: no hits. check_pages BANNED check PASS."),
    ("M7c-r1-scope-words", "scope words (every, all, always, any, only) on L07/L08", "L07.html:153,264,319,331-333; L08.html:129,144,311,319,336,428,506", "PASS",
     "'every' claims checked: 'every instance of Definition 1.1' is covered by the finite-problem proofs; 'every value is exact' is true for integer code; 'every (t,s)' loops and the 18 and 20 pair counts match code; 'for every real c' verified (Remark 1.5, P3). 'The lab does not show convergence' is an honest limit. No unsupported universal."),
    ("M7c-r1-attribution", "attributions on L07/L08", "L07.html:555, L08.html:538", "PASS",
     "Both pages state they cite no outside source; `data-references` is empty; no author or year appears. Nothing to verify against the registry; no locator is asserted."),
    ("M7c-r1-structure-counts", "quiz, misconceptions, problem tiers, Why-it-matters, hours", "L07.html:52,337-353,355-458,476-551; L08.html:52,325-341,343-446,464-534", "PASS",
     "L07: quiz 10 items (480-549), 3 misconceptions, 3 problems in each tier (M, P, E, R), Why-it-matters under 120 words. L08: quiz 9 items, 3 misconceptions, 3 problems per tier. Solutions present for every problem (<details class=solution>). check_pages PASS covers the code-enforced counts."),
    ("M7c-r1-hours", "data-hours and hub hours split", "L07.html:2 (data-hours=9), L08.html:2 (data-hours=10); index.html:149-150", "PASS",
     "L07 9 h and L08 10 h match the hub cards (index.html:149 'L07 · 9 h', 150 'L08 · 10 h') and the plan (9, 10). Hub data-hours-lessons=77 is the sum of 9+9+10+10+10+10+9+10 from the plan; the other six lessons are outside this slice and not re-summed here."),
    ("M7c-r1-B2-infinite-horizon", "architect decision Q2 (B2): infinite horizon not stated", "L08.html:52, 144, 317, 320, 538", "PASS",
     "No infinite-horizon result, citation or limit is stated. Statements are: 'The infinite-horizon case is not treated here' (52), 'the lesson states no limit' (144), 'This lesson states no infinite-horizon result' (317), references (538). Matches the binding decision."),
    ("M7c-r1-figures-data", "figures and data files on L07/L08", "L07.html, L08.html", "PASS",
     "No svg, img, chart, data-files or MANIFEST reference on either page (grep count 0). No figure or data row applies."),
    ("M7c-r1-cards-L07-theorems", "cards c121-c129 (L07 T)", "course/modules/M/M7/cards.json (ids M7-c121..c129)", "PASS",
     "All nine read in full and matched to L07 Def 1.1, 1.2, Remark 1.3, Def 1.4, Thm 2.1, 2.2, 2.3, Cor 2.4, Remark 2.5. Each card atomic, correct, T grade with page citation; c129 V_0(x)=1 re-derived."),
    ("M7c-r1-cards-L07-lab-and-misconceptions", "cards c130-c137, c211, c212, c224 (L07)", "cards.json (ids M7-c130..c137, c211, c212, c224)", "PASS",
     "Each lab-read number is C with basis naming Lab 1 (verifier ruling 9); values match L07.html:300-318 (240,220,200,130,4; 70 = C(8,4); optimal 100 x4; greedy 130; V_3(400)=130). Misconception cards match L07.html:340-347. c211/c212 match Def 1.2 (no beta). c224 matches Remark 2.5 (plan earns 0 < 1). Numbers present on the lesson page (scan)."),
    ("M7c-r1-cards-L08-theorems", "cards c142-c149, c155, c156, c162, c186, c214 (L08 T)", "cards.json (L08 T cards)", "PASS",
     "Each card matches L08 Def 1.1, 1.2, Thm 1.3, 1.4, Lemma 2.2, Def 2.1, Prop 2.3, Remark 1.5, Remark 2.4, Section 3 and Remark 2.4 (no limit). c186 numbers (beta=-1, V_0=1, U_0=0) re-derived. c215's 0.9 ratios appear in L08.html:311 and E2. Read in full."),
    ("M7c-r1-cards-L08-lab", "cards c150-c154, c157, c175, c199, c215 (L08 C)", "cards.json (L08 C cards)", "PASS",
     "Lab-read values match L08.html:285-310 (13.948890; 378; 18 pairs; 6.0..1.99746; policy s2 repair t0-3 run t4-5; no tie; run for states 0,1 at all t). Each has basis 'Lab 1 (SIMULATED)...'. Read in full."),
    ("M7c-r1-cards-duplicates-and-numbers", "full cards.json duplicate scan; card numbers present in lesson", f"course/modules/M/M7/cards.json (198 cards); {SC}cards_scan.py", "PASS",
     f"{SC}cards_scan_output.txt: 198 cards, 0 duplicate ids, 0 duplicate fronts, 0 duplicate backs. Shared 8-word runs across the 40 L07/L08 cards are the common hypothesis and formula wording (not duplicate cards). Every number token on a slice card appears in its lesson page text (no missing numbers printed)."),
    ("M7c-r1-hub-L08-card-error-claim", "hub card text for L08 vs lesson and lab output", "course/modules/M/M7/index.html:150", "FAIL",
     "index.html:150 says L08 covers 'value iteration on a finite-state problem with the error reported'. The lab prints only the change between successive iterates (L08.html:304-309 expected block; tests/labs/M7/lab-M7-L08-1.py:278-279 computes max|U^(n+1)-U^n|), and the lesson says the changes 'are not a bound on the error of the iterates' (L08.html:144). No error quantity is printed. Defect class 2 (lab output vs prose)."),
]
rows_out = []
for rid, check, loc, status, ev in rows:
    r = {"id": rid, "check": check, "location": loc, "status": status, "evidence": ev}
    if status != "PASS":
        r["fix"] = ("In course/modules/M/M7/index.html line 150 replace 'with the error reported' with "
                    "'with the change between successive iterates reported' (the hub, not this slice's pages, owns "
                    "that line; the lesson text and the twin are correct and must not change).")
    rows_out.append(r)

notes = [
    "Slice: course/modules/M/M7/L07.html, course/modules/M/M7/L08.html, tests/labs/M7/lab-M7-L07-1.py, tests/labs/M7/lab-M7-L08-1.py, and the 40 cards in course/modules/M/M7/cards.json with lesson L07 or L08 (ids c121-c137, c142-c157, c162, c175, c186, c199, c211, c212, c214, c215, c224). Every card read in full (sampling not needed). The project slice, the hub other than line 150, and the other lessons were not judged, except the one hub line that restates L08 (row M7c-r1-hub-L08-card-error-claim, owned by the hub builder).",
    "Round 1 for this slice. A fragment from a previous campaign (round 7, pin 7aa909e, verifier B7) was present at ledgers/M7/M7-c.json in this checkout; this round-1 fragment replaces it as the task instructed. No row was carried from it; every row was re-derived here. Its L07/L08 files are byte-identical to aeb512b6 (git diff 7aa909e..HEAD empty for the four slice files).",
    "ledgers/M7/scripts/M7-c-r1/ already contained two git-tracked files from commit 18171917 (recheck_L07_L08.py, strip_html_text.py). They were not run or edited by this verifier; the scripts behind this round's rows are indep_L07_L08.py, cmp_twin_page.py, cards_scan.py, lab_mutants.py, and commands_output.txt, pytest_output.txt, page_smoke_output.txt, cmp_twin_page_output.txt, cards_scan_output.txt, indep_L07_L08_output.txt, lab_mutants_output.txt.",
    "Mutants: the list is empty by design. Labs are demonstrations (verifier ruling), and the ledger counts every listed mutant as a must-kill fault. The lab-check probes are rows M7c-r1-lab-L07-check-probe and M7c-r1-lab-L08-check-probe: 7 of 10 probe mutants changed the printed output; the 3 survivors are output-identical on this instance (see those rows). The project grader mutation rule does not apply to this slice.",
    "Non-blocking wording (no row, not a FAIL): L07.html R1 solution repeats 'so Theorem 2.2 has no optimal plan to start from' twice (around line 440). Could be shortened by the builder.",
    "Naming observation for architect Q12 (not a FAIL): 'value iteration' (L08 Def 2.1) is an on-page definition of a finite-horizon algorithm. Its curriculum namesake value-function-iteration (curriculum/01-foundations.yaml:249, M5) carries a 'certified error bound' that L08 does not claim. Confirm it is acceptable as prose. The concept is not linked; check_dag passes.",
    "Token extraction for the notation row: math tokens on L07 are A, B, H, J, S, V, W, a, b, c, f, j, k, m, p, q, r, s, t, u, v, w, x, y and \\R, \\Sigma, \\binom, \\beta absent; on L08 A, B, C, G, H, J, S, U, V, W, a, b, c, f, k, n, p, q, r, s, t, u_n, x, y, and \\beta, \\R, \\mathcal{G}. None is a registered symbol.",
    "Hours arithmetic: L07 9 h and L08 10 h match the hub. The lesson-hours total (77) depends on six other lessons, not checked here.",
    "Could not check in this slice: render_curriculum, build_site --check, fetch_data --check (outside slice; curriculum unchanged in aeb512b6); check_projects, run_graders, mutate_graders (project slice); the full pytest suite (only test_labs for the two M7 cases); live verify_refs (no citation); visual inspection of rendered pages beyond page_smoke's geometry checks (no figures on these pages).",
]

fragment = {
    "unit": "M7",
    "slice": "c",
    "round": 1,
    "verifier": "independent verifier (Haiku), slice c, round 1",
    "pin": "aeb512b6",
    "base": "none: first independent verification of slice c (no previous fragment carried)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyS1-M7-c",
    "scratch": f"{S}/",
    "verified_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "verdict": "FAIL",
    "rows": rows_out,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": notes,
    "summary": ("M7 slice c (L07, L08, twins, 40 cards). 41 rows: 40 PASS, 1 FAIL. Every number, proof, lab "
                "claim and card re-derived; all gates and runs pass. The single FAIL is the hub card line index.html:150, "
                "which promises an 'error reported' that the L08 lab does not print (it prints iterate changes, and the lesson says they are not an error bound)."),
}
Path(f"ledgers/M7/M7-c.json").write_text(json.dumps(fragment, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("rows", len(rows_out), "pass", sum(r["status"] == "PASS" for r in rows_out))
