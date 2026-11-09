import json

S = "ledgers/FC2/scripts/FC2-c-r5/"
P = "PASS"


def row(rid, check, location, status, evidence, fix=None):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != P:
        r["fix"] = fix
    return r


CARRY4 = "Carried from round 4 (the cited lines are not in the round 4 to round 5 delta hunks, and the file is otherwise unchanged in those lines): "

rows = [
    row("c-gate-check-pages", "2.9-structure-prose", "tools/check_pages.py --unit FC2; --unit FC2 --page L07; --unit FC2 --page L08; --all", P,
        "Run at pin dde0486b: 'check_pages FC2: PASS' (exit 0); 'check_pages FC2 L07: PASS' (exit 0); 'check_pages FC2 L08: PASS' (exit 0); --all exit 0 (scripts/FC2-c-r5 check_pages_*.out, check_pages_all.out)."),
    row("c-gate-check-dag", "2.6-dag", "tools/check_dag.py --unit FC2", P,
        "'check_dag FC2: PASS', exit 0 (check_dag_unit.out). The delta adds no concept link to L07 or L08."),
    row("c-gate-check-projects", "2.9-structure-prose", "tools/check_projects.py --unit FC2", P,
        "'check_projects FC2: PASS', exit 0 (check_projects_unit.out). project.html changed in the delta (lede sentence only); the check passes."),
    row("c-gate-run-labs", "2.2-labs", "tools/run_labs.py --unit FC2 --page L07; --page L08; --unit FC2", P,
        "'run_labs FC2: PASS (1/1)' for L07 and for L08; 'run_labs FC2: PASS (11/11)' for the unit (run_labs_L07.out, run_labs_L08.out, run_labs_unit.out; exit 0 each)."),
    row("c-gate-pytest-labs", "2.2-labs", "tests/test_labs.py -k 'FC2 and (L07 or L08)' -rA", P,
        "PASSED tests/test_labs.py::test_lab_runs_and_matches_its_page[lab-FC2-L07-1] and [lab-FC2-L08-1]; exit 0 (pytest_labs.out)."),
    row("c-gate-pytest-tooling", "2.2-labs", "tests/test_page_checks.py tests/test_run_labs.py", P,
        "pytest -q: all dots, no failures, exit 0 (pytest_tooling.out)."),
    row("c-gate-ruff", "2.4-math-notation", "ruff check . ; ruff format --check .", P,
        "'All checks passed!' (exit 0, ruff_check.out); '554 files already formatted' (exit 0, ruff_format.out)."),
    row("c-gate-mypy", "2.2-labs", "mypy --no-incremental (full repository; includes the two twins)", P,
        "'Success: no issues found in 385 source files', exit 0 (mypy_full.out)."),
    row("c-gate-verify-refs", "2.1-citations", "tools/verify_refs.py --offline; tools/verify_refs.py --unit FC2 (live)", P,
        "Offline: 'offline integrity: 560 entries, 0 problems', exit 0 (verify_refs_offline.out). Live FC2: 'live re-verification of FC2: 4 of 560 entries, 0 problems', exit 0 (verify_refs_unit_live.out). references/references.json is unchanged in the delta."),
    row("c-gate-page-smoke-L07", "2.9-structure-prose", "tools/page_smoke.py --unit FC2 --pages L07 L08 (Chromium, Pyodide)", P,
        "'page_smoke modules/FC/FC2/L07.html: PASS' (page_smoke.out line 5); 'page_smoke FC2: PASS'."),
    row("c-gate-page-smoke-L08", "2.9-structure-prose", "tools/page_smoke.py --unit FC2 --pages L07 L08 (Chromium, Pyodide)", P,
        "'page_smoke modules/FC/FC2/L08.html: PASS' (page_smoke.out line 9)."),
    row("c-lab-L07-1-twin", "2.2-labs", "tests/labs/FC2/lab-FC2-L07-1.py; course/modules/FC/FC2/L07.html lines 157-273", P,
        "Twin file unchanged in the delta (git diff --name-only edbb7aa8 dde0486b lists no change to it). Run alone: 'python -I -W error tests/labs/FC2/lab-FC2-L07-1.py' exit 0 (twin_L07_isolated.out). run_labs L07 PASS, so page code equals the twin and the expected block equals the output. Expected block lines 259-273 are outside the delta hunks (hunk at 271 has the changed interpretation at line 274 only)."),
    row("c-lab-L08-1-twin", "2.2-labs", "tests/labs/FC2/lab-FC2-L08-1.py; course/modules/FC/FC2/L08.html lines 126-268", P,
        "Twin unchanged in the delta. Run alone under python -I -W error: exit 0; output shows 'rejected: price outside the no-arbitrage bounds' for 4.00, 100.00 and 120.00 (twin_L08_isolated.out). run_labs L08 PASS."),
    row("c-lab-L07-1-hypothesis", "2.2-labs", "course/modules/FC/FC2/L07.html line 156 (hypothesis)", P,
        CARRY4 + "L07.html line 156 is outside every delta hunk (hunks at 48-51, 83-91, 140, 271-279, 360, 442, 453)."),
    row("c-lab-L08-1-hypothesis", "2.2-labs", "course/modules/FC/FC2/L08.html line 125 (hypothesis)", P,
        CARRY4 + "L08.html line 125 is outside every delta hunk (hunks at 52-58, 107-108, 271-278, 340-346, 355-361, 440, 451)."),
    row("c-lab-L07-1-interpretation", "2.2-labs", "course/modules/FC/FC2/L07.html line 274 (interpretation); expected block lines 259-273", P,
        "Changed line (A8 to A7′). Expected error column: +171, -91, +36, -20, +7, -4, -2, -1, 0 (cents). Sign changes among the nonzero values: 5 (1->2, 2->5, 5->10, 10->25, 25->50), matching 'changes five times'. Absolute errors 171, 91, 36, 20, 7, 4, 2, 1, 0 decrease strictly along the list, matching 'decreases along the list' (recompute_fc2c_r5.out)."),
    row("c-lab-L08-1-interpretation", "2.2-labs", "course/modules/FC/FC2/L08.html line 269 (interpretation)", P,
        CARRY4 + "L08.html line 269 is outside every delta hunk."),
    row("c-lab-L07-rounding", "2.2-labs", "course/modules/FC/FC2/L07.html lines 152, 166-169 (docstring); twin lines 10-13, 31-34", P,
        CARRY4 + "L07.html lines 152 and 166-169 and the twin (byte-identical) are outside the delta hunks; run_labs PASS."),
    row("c-lab-L08-bracket-claim", "2.2-labs", "course/modules/FC/FC2/L08.html line 121; twin lines 70, 78-82", P,
        CARRY4 + "L08.html line 121 and the twin are outside the delta hunks (the L08 hunk at 116-119 is not in the delta)."),
    row("c-num-L07-M1-M2", "2.1-numbers-unrounded", "course/modules/FC/FC2/L07.html lines 299-306 (M1, M2 solutions)", P,
        "Read in full this round. M1: d1 = 0.35, d2 = 0.15 (recompute: 0.350000000, 0.150000000). M2: C = 10.450584 with unrounded 10.4505836 (recompute 10.450583572); Ke^(-rtau) = 95.122942 (recompute 95.122942450); P = 5.573526 = 557 cents (recompute 5.573526022)."),
    row("c-num-L07-lab-table", "2.1-numbers-unrounded", "course/modules/FC/FC2/L07.html lines 259-273 (lab expected block); line 152", P,
        "Expected block rows n=1..400 (binomial_cents, error_cents) equal the independent recompute: 1216/171, 954/-91, 1081/36, 1025/-20, 1052/7, 1041/-4, 1043/-2, 1044/-1, 1045/0. Lab 1 output matches (run_labs L07 PASS). Lab-expected block lines are outside the delta hunks."),
    row("c-num-L07-misconceptions-E1-E2", "2.1-numbers-unrounded", "course/modules/FC/FC2/L07.html lines 288, 330, 334", P,
        "Read this round. Misconception 1: 171, -91, 36, -0.4998 cents at 400 steps (recompute -0.499773). E1: -0.0049977 currency units = -0.4998 cents; next smallest 200 steps -0.9992 (recompute -0.999231). E2 unrounded: 171.17, 35.54, 7.04 (positive); -91.01, -19.72, -3.99, -2.00, -1.00, -0.50 (negative), all match the recompute; the 'three positive, five negative, one zero' count matches the printed values."),
    row("c-num-L07-M3", "2.1-numbers-unrounded", "course/modules/FC/FC2/L07.html line 310 (M3 solution)", P,
        "Read this round. u = 1.105171, d = 0.904837, R = 1.012578 (recompute 1.105170918, 0.904837418, 1.012578452). q unrounded 0.5378084 -> 0.537808 (recompute 0.537808372); six-place inputs 0.107741/0.200334 = 0.537807 (recompute 0.537806863). h = 0.25 < 16 holds (0.04/0.0025)."),
    row("c-num-L07-E3", "2.1-numbers-unrounded", "course/modules/FC/FC2/L07.html line 338 (E3 solution)", P,
        "Read this round. u = e^0.2 = 1.221403 (recompute 1.221402758); d = 0.818731 (0.818730753); R = 1.051271 (1.051271096); q = 0.577493 (0.577493196); V_1 = 12.1623 = 1216 cents (recompute 12.162284965)."),
    row("c-num-L07-R2", "2.1-numbers-unrounded", "course/modules/FC/FC2/L07.html lines 345-348 (R2 solution)", P,
        CARRY4 + "R2 of L07 is outside every delta hunk."),
    row("c-num-L08-L-M1", "2.1-numbers-unrounded", "course/modules/FC/FC2/L08.html lines 57, 251-252, 297 (M1), 329 (E2)", P,
        "Read this round. L(K=100) = 100 - 100e^(-0.05) = 4.877058 (recompute 4.87705755, rounds to 4.877058 at 6 dp and 4.8771 at 4 dp). K=120: 120e^(-0.05) = 114.15 > 100, so L = 0 (recompute). Prices 4.00 (< L), 4.90 (in (L, 100)), 100.00 (= S) classify as stated."),
    row("c-num-L08-table", "2.1-numbers-unrounded", "course/modules/FC/FC2/L08.html lines 252-263 (lab expected block)", P,
        "run_labs L08 PASS (expected block equals output). Block lines are outside the delta hunks."),
    row("c-num-L08-E2-E3", "2.1-numbers-unrounded", "course/modules/FC/FC2/L08.html lines 329 (E2), 333 (E3)", P,
        CARRY4 + "L08.html lines 329 and 333 are outside every delta hunk."),
    row("c-num-L08-M3-halvings", "2.1-numbers-unrounded", "course/modules/FC/FC2/L08.html line 305 (M3); line 269", P,
        "Recompute: bracket [1e-6, 10], tol 1e-10: 37 halvings; width after 36 = 10/2^36 = 1.455e-10 (still above tol), after 37 = 7.28e-11 (recompute_fc2c_r5.out). ceil(log2(W/tol)) = 37."),
    row("c-num-L08-R2", "2.1-numbers-unrounded", "course/modules/FC/FC2/L08.html lines 340-343 (R2 problem and solution paragraph, line 343)", "FAIL",
        "The solution now says: 'At these inputs ..., a one-cent quote error moves the implied volatility by about 0.0267 volatility points to first order.' The exact first-order value is 0.01/37.524 = 0.000266496 in volatility units, that is 0.0266496 volatility points (recompute_fc2c_r5.out), which rounds to 0.0266 at 4 dp. The figure 0.0267 is the displayed-value route (0.01/37.52 = 0.0266524), which the same paragraph names as its first route. The paragraph's own parenthetical says the unrounded value gives 0.000266, which is 0.0266 points, so the new sentence contradicts the unrounded figure.",
        "Replace 'about 0.0267 volatility points' with 'about 0.0266 volatility points (0.000266)' (or 'about 0.027 volatility points'), and keep 0.0267 only in the sentence that explicitly uses the displayed 37.52."),
    row("c-math-L07-lemmas-1", "2.3-math", "course/modules/FC/FC2/L07.html lines 63-76 (Lemmas 1.1, 1.2 and proofs); P1 solution line 316", P,
        CARRY4 + "lines 63-76 and 316 are outside every delta hunk; Lemma 1.2 identity re-checked numerically (Phi(x)+Phi(-x)=1 line in the lab output)."),
    row("c-math-L07-prop1.4-1.5", "2.3-math", "course/modules/FC/FC2/L07.html lines 95-115 (Prop 1.4, 1.5 and proofs)", P,
        "Read this round. Prop 1.4 now states 'Under A1 to A5, A7 and A7′'; its proof uses parity (Lesson 5) and Lemma 1.2 with Definition 1.3, which is the A7′ premise, so the hypothesis list covers the proof. Prop 1.5 proof: (r + sigma^2/2) tau / (sigma sqrt tau) = (ln(S/K) + r tau)/(sigma sqrt tau) + sigma sqrt(tau)/2, matching card FC2-c112; the claim that C depends only on S, K, r tau and sigma sqrt(tau) follows (no drift term)."),
    row("c-math-L07-tree-lemma2.2-thm2.3", "2.3-math", "course/modules/FC/FC2/L07.html lines 119-141 (Def 2.1, Lemma 2.2, Thm 2.3); L06.html lines 128-141, 320-322", P,
        CARRY4 + "the statement and proof lines 119-141 are outside the delta hunks (the hunk at 140 is context and unchanged). Theorem 2.3 still states 'Under A1 to A5 and A7' and does not use A7′, as line 143 says."),
    row("c-math-L07-cross-refs", "2.4-math-notation", "course/modules/FC/FC2/L07.html lines 55, 103, 140, 281; L04.html lines 58-64, 90, 69; L05.html lines 63-64; L06.html lines 55-63, 110-141", P,
        "Read this round. Line 281 now cites 'the call payoff of Lesson 4 (Definition 1.1)'; L04.html line 69 is 'Definition 1.1 (call and put payoffs)' (the earlier citation of Definition 2.1 was the American/European exercise definition at L04 line 90, so the correction is right). Line 55 lists A1 to A5 of Lesson 4 with A7 and A7′. L06.html line 132 is Definition 3.2 (Backward induction), as cited."),
    row("c-math-L08-lemma2.1", "2.3-math", "course/modules/FC/FC2/L08.html lines 67-84 (Lemma 2.1 and proof)", P,
        CARRY4 + "lines 67-84 are outside every delta hunk. dC/dsigma = 100 phi(0.35) = 37.524035 re-computed (recompute_fc2c_r5.out)."),
    row("c-math-L08-lemma2.2", "2.3-math", "course/modules/FC/FC2/L08.html lines 86-93 (Lemma 2.2 and proof)", P,
        CARRY4 + "lines 86-93 are outside every delta hunk."),
    row("c-math-L08-thm2.3", "2.3-math", "course/modules/FC/FC2/L08.html lines 95-104 (Theorem 2.3, proof; line 104)", P,
        "Read this round. Statement (lines 96-97): exactly one sigma* > 0 with C(sigma*) = C* if L < C* < S, and none if C* <= L or C* >= S, unchanged. Hypothesis A1 to A5, A7 and A7′ is supplied by line 55 ('in force'), which now reads A7′. Line 104 is unchanged."),
    row("c-math-L08-prop3.2-bisection", "2.3-math", "course/modules/FC/FC2/L08.html lines 108-119 (Def 3.1, Prop 3.2 and proof)", P,
        CARRY4 + "lines 108-119 are outside every delta hunk; the halving count is re-derived under c-num-L08-M3-halvings."),
    row("c-math-L08-canon-and-scope", "2.4-math-notation", "course/modules/FC/FC2/L08.html lines 273-276 (Section 4), line 121", P,
        "Read this round. Line 274 now reads 'under A7 and A7′' and 'in A7′, or in the quote itself'; the Theorem 2.3 uniqueness claim matches the statement at lines 96-97. Lines 275-276 and 121 are unchanged."),
    row("c-grade-L07", "2.5-grades", "course/modules/FC/FC2/L07.html lines 358-366 (key results), 86 (Def 1.3 claim), 369", P,
        "Read this round. Key results rows: Phi identities T (lines 360-361), put from parity T under 'A1 to A5, A7 and A7′' (line 363, Prop 1.4 proof on the page), Prop 1.5 T, Lemma 2.2 T, Theorem 2.3 T. Line 86: the closed-form attribution is graded C with data-cite black1973pricing, the same grade as before. Line 369: Lab 1 comparison has no grade."),
    row("c-grade-L08", "2.5-grades", "course/modules/FC/FC2/L08.html lines 356-359 (key results), 55 (C attribution), 362", P,
        "Read this round. Key-results row 358 (Theorem 2.3) is T and now says 'A7 and A7′ of Lesson 7'; line 55 attribution is graded C with data-cite black1973pricing; line 362 states no grade for the lab comparison."),
    row("c-grade-lab-values", "2.5-grades", "course/modules/FC/FC2/L07.html line 369; L08.html line 362", P,
        "Both pages state that the Lab 1 comparison is not a graded row. Cards c110, c111, c117 and c129 carry no grade, consistent with that. Card c109 (T, basis 'Lab 1 (closed form under A7); Problem M2') is a numerical check of the closed form, which plan section 10 allows to be T with the lab as basis (compare c125 and c131)."),
    row("c-notation-L07-L08", "2.4-math-notation", "course/modules/FC/FC2/L07.html and L08.html math segments; notation/notation.json (unchanged in the delta)", P,
        "The delta adds no symbol to L07 or L08. A7′ is an assumption label, not a notation symbol, and follows the primed convention already used for A6′ (L06 line 141) and A8′ (L03). No reassigned symbol found in the changed lines; notation/notation.json is not in the delta."),
    row("c-dag-L07", "2.6-dag", "course/modules/FC/FC2/L07.html meta row (line 37), dfn (line 80), links (lines 37, 80, 103, 281)", P,
        "check_dag FC2 PASS. The delta adds no concept link or dfn to L07; the new cross-reference to Lesson 4 Definition 1.1 is plain text with no concept link."),
    row("c-dag-L08", "2.6-dag", "course/modules/FC/FC2/L08.html lines 37, 51-69, 341, 395-404; both twins; cards.json FC2-c120", P,
        "check_dag FC2 PASS. The delta adds no concept link to L08. Cards FC2-c120 unchanged."),
    row("c-prose-scope-words", "2.7-prose-scope", "L07.html and L08.html changed lines (scope words: every, all, only, exactly, same, any, each, unique, none, must)", P,
        "All changed sentences read in full (hunks at L07 48-51, 83-91, 140, 271-279, 360, 442, 453; L08 52-58, 107-108, 271-278, 340-346, 355-361, 440, 451). Scope words introduced or kept: 'for every spot', 'for every strike', 'does not say which assumption fails', 'exactly when' (Theorem 2.3). Each is backed by a theorem or stated hypothesis. The R2 'about 0.0267' hedge is handled in c-num-L08-R2."),
    row("c-prose-process-banned", "2.8-process-words", "L07.html and L08.html visible prose and lab docstrings", P,
        "No process words (builder, verifier, round, rule, ledger) in changed text. 'registry key black1973pricing' (L07 line 86, L08 line 55) and 'article level' (footers) use the unit's established phrasing (L01-L06 pages say 'cites no registry source' or 'registry key'); recorded in registry_flags."),
    row("c-struct-L07", "2.9-structure-prose", "course/modules/FC/FC2/L07.html (whole page; hunks read in full this round)", P,
        "Delta hunks read in full (lines 48-51, 83-91, 96, 140, 143, 274, 279, 281, 363, 442, 453-456). Hunk headers show no line shift, so section ids and cross-refs are unchanged. check_pages L07 PASS and page_smoke L07 PASS. The whole page was not re-read this round (delta protocol)."),
    row("c-struct-L08", "2.9-structure-prose", "course/modules/FC/FC2/L08.html (whole page; hunks read in full this round)", P,
        "Delta hunks read in full (lines 52-58, 107-108, 271-278, 340-346, 355-361, 440, 451). No line shift. check_pages L08 PASS and page_smoke L08 PASS. The whole page was not re-read this round (delta protocol)."),
    row("c-hours-L07-L08", "2.10-hours", "course/modules/FC/FC2/index.html lines 29, 41, 133-142; L07.html lines 2, 34; L08.html lines 2, 34", P,
        CARRY4 + "index.html hunks are at lines 33 and 150 (lede and ladder rung text), not at 29, 41 or 133-142; the L07/L08 meta rows at lines 2 and 34 are outside every hunk."),
    row("c-card-01-c099-c108", "2.10-cards", "course/modules/FC/FC2/cards.json FC2-c099..c108 (L07)", P,
        "Read this round (scripts/FC2-c-r5 cards_L07_L08_current.txt). c103 and c104 changed to A7′ and checked against L07 Prop 1.4 (line 96) and Prop 1.5 (lines 108-112). c099, c100, c101, c102, c105, c106, c107 and c108 are field-identical to round 4 (script comparison of card objects) and match their lesson lines."),
    row("c-card-02-c109-c117", "2.10-cards", "cards.json FC2-c109..c117 (L07)", P,
        "Round-4 FAIL on c111 is resolved: c111 back now carries the qualifier 'At 400 steps it is negative in the unrounded value, which prints as 0' (recompute: -0.499773 cents). c109: T with basis 'Lab 1 (closed form under A7); Problem M2'; value 10.450584 = 1045 cents matches the recompute; grade T with lab basis follows plan section 10 (compare c125). c110: '-91 cents, from an unrounded error of -91.01' matches (recompute -91.008223). c113: A7′ and T; Prop 1.4 'two forms agree' matches. c114, c115, c116 match (d1=0.35, d2=0.15; u=1.105171, d=0.904837, R=1.012578, q=0.537808 (unrounded) / 0.537807 (six-place); V_1 = 12.1623 = 1216 cents). c117: 400 steps, -0.0049977 currency units = -0.4998 cents (recompute -0.4997731), next 200 steps -0.9992; matches E1. Ungraded lab observations (c110, c111, c117) match the L07 line 369 rule."),
    row("c-card-03-c118", "2.10-cards", "cards.json FC2-c118 (L07): grade and basis", P,
        "Round-4 FAIL resolved: grade is now T with basis 'Problem M2 (Proposition 1.4)'. M2 solution (L07 lines 305-306) derives P = C - S + Ke^(-rtau) = 5.573526 = 557 cents from Proposition 1.4 and the call value; recompute P = 5.573526022 (557.35 cents)."),
    row("c-card-04-c119-c131", "2.10-cards", "cards.json FC2-c119..c131 (L08)", P,
        "Read this round. c122 now says 'under A1 to A5, A7 and A7′ of Lesson 7' and matches Theorem 2.3 (L08 lines 96-97). c129 is ungraded with basis 'Lab 1 (rejected prices)'; the twin run rejects 4.00, 100.00 and 120.00 with the no-arbitrage message (twin_L08_isolated.out). c125 (37 halvings) recomputed. c126 (L = 4.877058) recomputed. c127 (only 4.90 has a volatility) matches the bounds. c131 (L = 0 at strike 120) recomputed. c119, c120, c121, c123, c124, c128 and c130 are unchanged and match their lesson text."),
    row("c-card-05-c145-c151-c152-c167", "2.10-cards", "cards.json FC2-c145 (L07), FC2-c151, FC2-c152, FC2-c167 (L08)", P,
        "Round-4 FAIL resolved: c152 no longer carries grade T (it is a restatement of Definition 3.1 and is now ungraded, like c124 and c167). c145 now uses A7′ and matches L07 Section 4 ('stated as A7′ and used, not derived', line 279). c151 is T and matches Proposition 3.2 (L08 lines 108-119; the 'within tol/2' result). c167 ungraded, matches Definition 3.1."),
    row("c-card-06-c182-c183", "2.10-cards", "cards.json FC2-c182 (L07) and FC2-c183 (L08), both new in the delta", P,
        "c182 'What does Assumption A7′ of Lesson 7 state?' matches L07 lines 90-91 (for every spot S > 0, strike K > 0, rate r, maturity tau > 0 and volatility sigma > 0; a premise, not proved there). c183 matches L08 Section 4 (line 274): two quotes at one expiry with different implied volatilities cannot both be values of the A7 formula at one common volatility, because implied volatility is unique (Theorem 2.3); the lesson does not say which assumption fails. Each card tests one fact, and neither duplicates another card (no duplicate fronts or backs among 171 cards, script)."),
    row("c-card-numbers", "2.10-cards", "cards.json: all L07 and L08 cards (22 and 17) against their own lesson text and twins", P,
        "Every card number was recomputed (recompute_fc2c_r5.out) and found in its lesson: 10.450584 and 1045 (L07 lines 259-273, 299-306); 5.573526 and 557 (L07 305-306); 95.122942; 1216 and 12.1623 (L07 338, lab row); 0.537807 and 0.537808 (L07 310); 1.105171, 0.904837, 1.012578, 0.577493, 1.221403 (L07); -91.01 and -0.4998 and -0.0049977 (L07 288, 330, 334); 4.8771 and 4.877058 (L08); 37 halvings and 1.46e-10 (L08 305 region); 1.455e-10 derived. The only number not found in the card's lesson is the 0.0267 figure in L08 R2, which is handled in c-num-L08-R2."),
    row("c-card-duplicates", "2.10-cards", "cards.json (all 171 cards)", P,
        "Script: 171 cards, 0 duplicate ids, 0 duplicate fronts, 0 duplicate backs (case-insensitive, whitespace-trimmed). Round-4 count was 164; the 7 new cards are FC2-c177..c183, of which c182 and c183 are L07/L08."),
    row("c-card-coverage", "2.10-cards", "cards.json L07 (22 cards) and L08 (17 cards) vs BUILDER_RULES section 7 and plan section 10", P,
        "L07: c099-c118, c145, c182 (22 cards: definitions, Lemmas 1.1-1.2, Def 1.3, Prop 1.4-1.5, Def 2.1, Lemma 2.2, Thm 2.3, Def 3.1, misconceptions, lab items). L08: c119-c131, c151, c152, c167, c183 (17 cards: Def 1.1, Lemma 2.1-2.2, Thm 2.3, Def 3.1, Prop 3.2, misconception and lab items). check_pages reports no 'no cards for' problem."),
    row("c-ref-L07-L08-black1973", "2.1-citations", "L07.html line 86 (claim span, data-cite black1973pricing) and footer line 456; L08.html line 55 and footer line 454; references/references.json key black1973pricing", P,
        "Registry record (references/references.json): type journal-article, year 1973, container Journal of Political Economy, volume 81, issue 3, pages 637-654, DOI 10.1086/260062, authors Black and Scholes, used_by now includes FC2. Crossref by plain curl (https://api.crossref.org/works/10.1086/260062) returned HTTP 200 with the same title, container, volume, issue, pages, type and authors (scripts/FC2-c-r5 crossref_black1973_r5.json). Publisher page: plain curl of https://www.journals.uchicago.edu/doi/10.1086/260062 returned HTTP 403 with a 'Just a moment...' page (publisher_r5.out; the doi.org link returns HTTP 302 to that URL). This is an access statement with a reproduced URL, so the paper text is not read here and the pages claim only the attribution ('is attributed to ... this lesson does not check the paper's text'). The pages now say 'article level', which matches the registry field 'journal-article' and plan section 7 Q5 ('book or paper level'); plan Q4 text said 'book level'. Flagged in registry_flags, not a defect."),
    row("c-assumption-A8-collision", "2.4-math-notation", "L07.html lines 51-96, 143, 274, 279, 363; L08.html lines 55, 107-108, 274, 358; cards.json c103, c104, c113, c122, c145, c182, c183; L03.html line 104 (A8 single curve) and line 66 (A8′)", P,
        "Grep for 'A8' in L07.html, L08.html and the L07/L08 cards returns no match. The closed-form assumption is now A7′ everywhere in those pages and cards. A8 (single curve) and A8′ (margin) remain only in L03, where they are defined. The A7′ label follows the primed convention already used for A6′ (L06 line 141). Plan line 296 (A7, L07 and L08 only) does not number the closed form, so no plan label is contradicted."),
    row("c-twin-page-equal", "2.2-labs", "tests/labs/FC2/lab-FC2-L07-1.py vs course/modules/FC/FC2/L07.html lines 157-273; tests/labs/FC2/lab-FC2-L08-1.py vs L08.html lines 126-268", P,
        "run_labs FC2 PASS for L07 and L08 (11/11 for the unit), and pytest test_lab_runs_and_matches_its_page PASS for both labs. Neither twin is in the delta. The page code and expected blocks are outside the changed text (only L07 line 274 interpretation and the A7′ text changed)."),
]

mutants = []

fragment = {
    "unit": "FC2",
    "slice": "c",
    "round": 5,
    "round_note": "Round 5 DELTA verification of FC2 slice c (L07-L08, twins, cards) at pin dde0486b. Previous fragment: /Users/billyribeiro/.fanout/frags/S-FC2-c.round4.json (pin edbb7aa8). Delta edbb7aa8..dde0486b for the slice: L07.html, L08.html, cards.json (objects c103, c104, c109, c110, c111, c113, c117, c118, c122, c129, c145, c152 changed; c182 and c183 new), index.html and project.html (outside the slice, read for hunks that touch cited lines). tests/labs/FC2/lab-FC2-L07-1.py and lab-FC2-L08-1.py, references/, notation/, curriculum/ and tools/ are unchanged in the delta (git diff --name-only).",
    "verifier": "claude-haiku-5-5, independent verifier (round 5; did not build FC2; no shared context with the builders)",
    "pin": "dde0486beeb0312e4ac1cc03aaa02e56644adb24",
    "base": "edbb7aa8de20e6d2f3035c463a79a318c22623c4",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyS5-FC2-c",
    "scratch": "ledgers/FC2/scripts/FC2-c-r5/ (gate outputs, recompute_fc2c_r5.py and .out, cards_L07_L08_current.txt, curl outputs)",
    "verified_at": "2026-11-09T10:08:39Z",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [
        "black1973pricing: the pages now say 'article level' (registry type journal-article). Plan section 7 Q4 recommended 'book level', which conflicts with the registry type. The builders used the registry's own field (and plan Q5 allows 'book or paper level'), so no FAIL is raised; the architect may confirm the wording."
    ],
    "freshness_flags": [
        "Publisher page https://www.journals.uchicago.edu/doi/10.1086/260062 returned HTTP 403 to plain curl on 2026-11-09 (publisher_r5.out). The paper text was not read; the attribution is recorded as an access statement."
    ],
    "notes": [
        "Commands run at the pin (outputs in ledgers/FC2/scripts/FC2-c-r5/): check_pages (unit, L07, L08, --all), check_dag, check_projects, run_labs (L07, L08, unit), twins alone under python -I -W error, pytest test_labs (L07, L08) and tooling tests, ruff check and format, mypy --no-incremental, verify_refs offline and live (FC2), page_smoke (L07, L08). All PASS.",
        "Mutants: none. Slice c has no grader; lab twins are demonstrations and mutation testing does not apply (verifier-rules ruling). run_graders was not run for the same reason.",
        "Independent recomputation: recompute_fc2c_r5.py (Phi, d1, d2, put parity, the nine-row tree table with unrounded errors, the four-step tree parameters, the one-step price, bisection halvings, the bounds L, and the vega) run with python -I.",
        "Not checked: the cited paper black1973pricing (publisher page returns HTTP 403 to plain curl; the attribution is recorded as an access statement). Whole-page re-read of L07 and L08 was not repeated this round; the delta hunks were read in full and every changed claim was re-verified.",
        "Judgment calls, not FAIL rows: card c109 is graded T with a lab basis, which plan section 10 allows (compare c125 and c131); card c110, c111, c117 and c129 are ungraded lab observations, consistent with the L07 line 369 rule. The cards c152, c167 and c124 are ungraded restatements of definitions.",
    ],
    "summary": {},
}

counts = {"PASS": 0, "FAIL": 0, "UNVERIFIABLE": 0}
for r in rows:
    counts[r["status"]] += 1
fragment["summary"] = {"rows": len(rows), "pass": counts["PASS"], "fail": counts["FAIL"], "unverifiable": counts["UNVERIFIABLE"]}

with open("ledgers/FC2/FC2-c.json", "w", encoding="utf-8") as fh:
    json.dump(fragment, fh, ensure_ascii=False, indent=2)
    fh.write("\n")
print("written", len(rows), counts)
