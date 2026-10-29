"""Builds ledgers/E2/E2-a.json for round 6 (slice a). Standard library only."""
import json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
O = "ledgers/E2/scripts/E2-a-r6/"
P = "Round 6 re-verified at 9fd6aed (full re-read of L01, L02, L03, index; " + O

def row(rid, check, location, status, evidence, fix=""):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    return r

rows = [
 row("E2a-r4-cmd-check_pages", "2.9 structure; tools/check_pages.py", "index, L01-L03", "PASS",
     P + "check_pages.out, check_pages_L01/L02/L03.out): unit run 'check_pages E2: PASS' rc 0; per-page L01, L02, L03 PASS rc 0. index is checked by the unit run only; '--page index' is not a valid use (--page takes lesson pages), so its 13 failures are a misuse, not a finding."),
 row("E2a-r4-cmd-check_dag", "2.9 DAG; tools/check_dag.py", "index, L01-L03", "PASS",
     P + "check_dag.out): 'check_dag E2: PASS' rc 0. Covers L02.html:37 and L01.html:37/107."),
 row("E2a-r4-cmd-check_projects", "2.6 project gate (unit-level)", "unit E2", "PASS",
     P + "check_projects.out): 'check_projects E2: PASS' rc 0. No project file in slice a; project not verified here."),
 row("E2a-r4-cmd-run_labs", "2.5 labs; tools/run_labs.py", "lab-E2-L01-1, lab-E2-L02-1, lab-E2-L03-1", "PASS",
     P + "run_labs_L01/L02/L03.out, run_labs_unit.out): 'run_labs E2: PASS (1/1)' rc 0 for each page; unit 'PASS (12/12)' rc 0."),
 row("E2a-r4-lab-isolated", "2.5 labs: twin alone under python -I -W error", "tests/labs/E2/lab-E2-L01-1.py, lab-E2-L02-1.py, lab-E2-L03-1.py", "PASS",
     P + "twin_L01/L02/L03.stderr): rc 0 for all three, stderr 0 bytes each."),
 row("E2a-r4-lab-page-equals-twin-and-expected", "2.5 labs: page code equals twin; expected equals stdout", "course/modules/E/E2/L01.html:167-274, L02.html:146-239, L03.html:117-199", "PASS",
     "Re-run at 9fd6aed: `.venv/bin/python ledgers/E2/scripts/E2-a-r5/embed_and_expected_r3.py` -> 'lab-E2-L01-1: page code == twin: True ... expected == stdout: True; twin rc=0; stderr bytes=0' (same for L02, L03), 'ALL OK'. Length difference of 1 is the trailing newline only."),
 row("E2a-r4-page-smoke", "2.9 page_smoke", "index, L01, L02, L03", "PASS",
     P + "page_smoke.out): smoke_system_chrome.py (tools/page_smoke.py with installed Chrome channel) --unit E2 --pages index L01 L02 L03 -> 'page_smoke E2: PASS' rc 0."),
 row("E2a-r4-ruff-mypy", "build gate: ruff, mypy strict", "repository", "PASS",
     P + "ruff_check.out, ruff_format.out, mypy.out): 'All checks passed!'; '335 files already formatted'; 'Success: no issues found in 229 source files'."),
 row("E2a-r4-pytest", "tooling tests for labs and page checks", "tests/test_labs.py, tests/test_run_labs.py, tests/test_page_checks.py", "PASS",
     P + "pytest.out): all dots, rc 0."),
 row("E2a-r4-verify_refs", "2.1 citations; verify_refs --offline", "references/references.json", "PASS",
     P + "verify_refs.out): 'offline integrity: 560 entries, 0 problems' rc 0. Live Crossref not run. fetch_data.out: 'fetch_data: 3 datasets, 0 problems' rc 0."),
 row("E2a-r4-recompute", "2.2/2.4 numbers and formulas", "index.html; L01.html; L02.html; L03.html", "PASS",
     "ledgers/E2/scripts/E2-a-r6/recompute_r6.py (independent Fraction and integer re-derivation, output recompute_r6.out): 57 of 57 PASS. Covers Ex 2.3, Ex 4.1 (119/4), Prop 4.2 identity (q(60-q) = 900-(q-30)^2) and 1/100 grid, Ex 4.3 (870/930), grid equilibria [(29,31),(30,30),(31,29)] and strict [(30,30)], profits, 1201-bid grid for n=2..5, Prop 2.5 revenue and second-highest mean for n=2..5, density mass 1, Ex 2.3 0.32, M1 0.072, M3 1/16, R1 scaled support (H=5/2, n=3), Step 3/4 maximum, L03 consistent prices for alpha=k/10 and an exact 0.1-cent grid, threshold 2/3, gains lost 2000*alpha."),
 row("E2a-r4-banned-process-words", "2.9 BUILDER_RULES 1.3-1.4 banned phrases", "index.html, L01-L03", "PASS",
     "Round 6 grep -i for TODO|TBD|lorem|for brevity|beyond the scope|left as an exercise|obviously|clearly|it can be shown|roughly|historically|verifier|builder|audit|slice|round [0-9] over index.html and L01-L03: no hits."),
 row("E2a-r4-macros-registered", "2.9 notation: macros and symbols", "index.html, L01-L03", "PASS",
     "Round 6 scan of every \\(...\\) and \\[...\\] expression: macros used are \\R (L01), \\E (L02), plus standard KaTeX. Letters used as symbols are lesson-local (alpha, beta, m, n, H, L, c, u, v, b, W, U_i, theta, sigma, f_v, pi in L01 and index). T occurs only in the L02.html:60 disclaimer, and X only as an action label in L01.html:322-324. Nothing in notation/notation.json is redefined. notation/ unchanged 04626e9..9fd6aed."),
 row("E2a-r3-notation-T-as-action-label", "2.9 notation: T not reused as an action label", "course/modules/E/E2/L01.html:322-324", "PASS",
     "Re-read at 9fd6aed: L01.html:322 'Player 1 chooses S or X', :324 'Definition 2.1 asks for u_1(S, a_2) > u_1(X, a_2)'. Lines 322-324 byte-identical since 04626e9 (not in the delta hunks). Payoffs 4, 3, 3, 2 unchanged; S dominant, X not."),
 row("E2a-r5-L01-M3-solution-paragraph-markup", "2.9 structure: well-formed paragraph markup", "course/modules/E/E2/L01.html:406 (and :331)", "PASS",
     "Round-5 FAIL is fixed at 9fd6aed. L01.html:406 is now one <p> ... </p> ('...and fewer when a check fails early. For large m and n ...'). `.venv/bin/python ledgers/E2/scripts/E2-a-r5/p_balance.py` on L01, L02, L03, index: 'stray </p> lines: []  unclosed <p> starts: []' for all four."),
 row("E2a-r5-L01-M3-lab-comparison-count", "2.4 numbers: lab comparison count claim", "course/modules/E/E2/L01.html:331 and :406 vs tests/labs/E2/lab-E2-L01-1.py equilibria()", "PASS",
     "The lab's row check is all(payoff[(k,j)][0] <= u1 for k in range(len(rows))) and the column check is the analogue, so each check stops at the first action that does better (all() short-circuits) and makes at most m + n comparisons per profile: 3 + 4 = 7 for a 3 by 4 game. My counter (recompute_r6.py) over 300 random 3x4 games gives max <= 84 = mn(m+n), and an all-ties game gives exactly 84. M3's 60 = 12 x 5 is the exhaustive count. Claim holds."),
 row("E2a-r5-L01-R2-assumption-reference", "2.2 cross-reference: Assumption number", "course/modules/E/E2/L01.html:399 vs L01.html:94", "PASS",
     "L01.html:399 cites 'Assumption 2 of Proposition 2.2'. L01.html:94 is 'Assumption 2. Players choose simultaneously and in pure actions, and each player's payoff is its objective.' Match. Line unchanged since 04626e9."),
 row("E2a-r5-L01-285-hedge", "2.2 prose claim", "course/modules/E/E2/L01.html:285", "PASS",
     "L01.html:285 'Sequential games ... can change the set of profiles that are stable, and they are not treated here.' Hedged ('can'), no numeric or uniqueness claim. Line unchanged since 04626e9."),
 row("E2a-r5-L02-248-symmetric-bullet", "2.2 prose vs assumptions", "course/modules/E/E2/L02.html:245, 248 vs L02.html:100", "PASS",
     "L02.html:248 'Assumption 3 considers only the profile in which every bidder uses the same bid function' matches L02.html:100 'Assumption 3. Every bidder uses the same strategy b(.) ... Only the symmetric profile is considered'. L02.html:245 'Assumption 4, which covers one unit per bidder and a zero probability of tied bids' matches L02.html:101 'Each bidder wants one unit, and the probability that two bids are equal is 0.'"),
 row("E2a-r5-L03-282-price-cases", "2.4 mathematics: price cases at alpha=1", "course/modules/E/E2/L03.html:282 vs Def 1.2 (L03.html:63-66) and Prop 2.1 (L03.html:72-87)", "PASS",
     "L03.html:282 at alpha = 1: M(6000) = m_L(6000) = 0, so 6000 fails Definition 1.2 (M(p) > 0). For p >= 10000 the offered mix is H only and the expected value is 12000 = 6000 + 6000 x 1. Matches Prop 2.1 (the second set gives 12000) and the lab's output line 'alpha = 1: market-consistent prices [12000]' (run_labs output, L03.html:198)."),
 row("E2a-r3-L03-misconceptions-problems-quiz", "2.2/2.4 L03 problems and quiz", "course/modules/E/E2/L03.html:218-230, 237-431", "PASS",
     "Re-read in full. Misconceptions at :220 (traded share 1 - alpha, loss alpha, high-quality sellers leave), :224 (Example 2.2: 9000 vs 6000), :228 (alpha 0.7: 6000 share 3/10 and 10200 share 1). Mechanics M1-M3 (2/3; 10800; 1/4 gives 3/4 and 500), proofs P1-P3, empirical E1-E3 (1800 at 0.9; threshold 2/3), research R1-R3, quiz numbers 0.6667 (tol 0.001), 200, 10800, 9000 all recomputed (recompute_r6.py). R2 at :325 'ratio 0 at the full-trade price' consistent with Prop 2.3."),
 row("E2a-r3-L02-canon-uniqueness-heading", "2.2 L02 assumption bullets", "course/modules/E/E2/L02.html:247, 249", "PASS",
     "L02.html:247 'The proof does not establish uniqueness ... the lesson makes no uniqueness claim' is consistent with Prop 2.2 (only 'an equilibrium') at L02.html:102 ('The proof does not claim that it is the only one'). L02.html:249 winner's curse referenced as L08 (plain prose, no link, as the Architect decisions require for out-of-closure concepts)."),
 row("E2a-r3-DAG-forward-mentions", "2.9 DAG: forward mentions", "L01.html:37, L02.html:37, L02.html:249, L03.html:51, index.html:55-56", "PASS",
     "check_dag E2 PASS. Forward mentions L02.html:249 (winner's curse, L08), L03.html:51 (signaling L04, screening L05) are plain prose with no link and no dfn, as the Architect decision requires for concepts outside the prerequisite closure. Links that exist: L01.html#def-nash-equilibrium and L02.html#def-bayesian-nash-equilibrium (each one anchor, grep -c = 1), index.html:56."),
 row("E2a-r3-hub-meta-M4-title", "2.2 hub meta", "course/modules/E/E2/index.html:35", "PASS",
     "index.html:35 'Prerequisites: E1 Microeconomics and M4 Probability, with M2 and M1 through them'. index.html byte-identical since 04626e9 (empty git diff). Consistent with L02 meta-row (M4) and L03 meta-row (M4, E1)."),
 row("E2a-r3-hub-dangling-reference", "2.9 hub", "course/modules/E/E2/index.html:56", "PASS",
     "Both anchors resolve: L01.html has id=\"def-nash-equilibrium\" (count 1); L02.html has id=\"def-bayesian-nash-equilibrium\" (count 1). index.html unchanged since 04626e9."),
 row("E2a-r3-hub-placement-item-1-ambiguous-key", "2.9 hub placement", "course/modules/E/E2/index.html:64-70", "PASS",
     "Placement item 1: 'uniform-price auction that sells two identical units ... third-highest bid' with k = 2 gives the (k+1)-th highest bid, which is the third-highest. Correct."),
 row("E2a-r3-hub-cards-titles", "2.9 hub cards", "course/modules/E/E2/index.html:110-118 vs L01-L09 h1", "PASS",
     "Round 6: card titles L01 'Strategic Form and Nash Equilibrium', L02 'Bayesian Games and Bayesian–Nash Equilibrium', L03 'Adverse Selection', L04 'Signaling', L05 'Screening', L06 'Moral hazard', L07 'Mechanism design and the revelation principle', L08 'Common-value auctions, the winner's curse and bid shading', L09 'Uniform-price versus discriminatory auctions' equal the h1 of each page (ledgers/E2/scripts/E2-a-r6/hours_h1.out). L08.html changed 9fd6aed vs 04626e9 but its h1 is unchanged."),
 row("E2a-r3-hub-L08-simulated-claim", "2.5 simulated claim", "course/modules/E/E2/index.html:117 vs L08.html:139-140", "PASS",
     "index.html:117 'the winner's curse in a seeded simulation labelled SIMULATED'. L08.html:139 'Lab 1 · Winner's profit in a seeded common-value simulation (SIMULATED)' and :140 'SIMULATED. The values, signals and errors ... are generated by a seeded pseudo-random generator'. Matches (L08 is slice b/c; only the label was checked here)."),
 row("E2a-r3-hub-prereq-unlocks", "2.9 hub", "course/modules/E/E2/index.html:35-36", "PASS",
     "index.html:36 'Unlocks: E4 and CF3 (curriculum prerequisites)'. check_dag E2 PASS covers the unit's edges. index.html unchanged since 04626e9."),
 row("E2a-r3-hub-objectives", "2.9 hub", "course/modules/E/E2/index.html:44-49", "PASS",
     "Objective 2 'a game with no pure equilibrium exists' is Proposition 3.2 (L01). Objective 3 '(n-1)/n · v' is Proposition 2.2 (L02). Objective 4 'market-consistent prices ... gains lost' is Prop 2.1 and 2.3 (L03). Each lesson-level claim is present on its page."),
 row("E2a-r3-hub-placement-items-2-5", "2.9 hub", "course/modules/E/E2/index.html:72-103", "PASS",
     "Item 2 discriminatory pays own bid (correct). Item 3 FOC a - c - 2q1 - q2 = 0 from q1(a-c-q1-q2) (correct). Item 4 E[V | V > 0.5] = 0.75 (correct). Item 5 'Nash equilibrium: each action is a best response' (correct; L01 Def 1.3)."),
 row("E2a-r3-hub-core-reading", "2.1 hub reading", "course/modules/E/E2/index.html:137-144", "PASS",
     "Each entry matches a verified registry record in references/references.json (year and container checked): nash1950equilibrium 1950; akerlof1970market 1970 'The Market for \"Lemons\": Quality Uncertainty and the Market Mechanism'; spence1973job 1973; rothschild1976equilibrium 1976; holmstrom1979moral 1979; vickrey1961counterspeculati 1961; milgrom1982theory 1982; fudenberg1991game 1991. Typographic note only (not a finding): the registry stores the Vickrey title in capitals and Nash's as 'n -person'; the hub uses sentence-case and 'n-person'. Substance identical."),
 row("E2a-r3-hours-arithmetic", "2.2 hours", "course/modules/E/E2/index.html:28-29; L01-L03 data-hours", "PASS",
     "index.html:29 data-hours-lessons=90, data-hours-project=20, sum 110 = module hours (line 31). Lesson data-hours L01..L09 are all 10 (hours_h1.out): 9 x 10 = 90. Project 20/110 = 18% (inside the 10-40% comment)."),
 row("E2a-r3-L01-printed-continuous-line", "2.5 lab prints", "tests/labs/E2/lab-E2-L01-1.py; L01.html:262-274", "PASS",
     "Expected block equals run output (embed check ALL OK). Printed lines: 'profiles checked 4, 4, 9', 'cournot grid 0 to 90 units: quantity pairs checked 8281', tie-allowed [(29,31),(30,30),(31,29)], profits [(870,930),(900,900),(930,870)], strict [(30,30)]; all re-derived in recompute_r6.py."),
 row("E2a-r3-L01-key-result-unique-best-response", "2.4 claims", "course/modules/E/E2/L01.html:392-393, 422", "PASS",
     "R1 solution at :392 (strict test removes (29,31) and (31,29); Prop 4.2 holds under strict test since 900 - pi_1 = (q1-30)^2 > 0 for q1 != 30 and pi_1 < 900 in Case 2) and key result at :422 (30 is the unique best response on [0,90]) recomputed: strict grid result [(30,30)] (recompute_r6.py)."),
 row("E2a-r3-L01-prop-2.2-3.2-4.2", "2.4 statements/proofs", "course/modules/E/E2/L01.html:91-103, 119-128, 142-155", "PASS",
     "Prop 2.2 proof (both directions) matches Def 2.1 and Def 1.3. Prop 3.2 proof: matching -> player 2 gains +1 > -1 by mismatching; mismatching -> player 1 gains +1 by matching. Prop 4.2: Case 1 identity 900 - q(60-q) = (q-30)^2 checked on rationals (recompute_r6.py, identity PASS); Case 2 profit -10q < -700 < 900. Assumptions 1-2 cited in the statement."),
 row("E2a-r3-L01-examples-remarks-numbers", "2.2 numbers", "course/modules/E/E2/L01.html:76, 81, 107, 132, 139, 159", "PASS",
     "Remark 1.4 'nash1950equilibrium ... 1950 ... Equilibrium points in n-person games' matches registry (PNAS 36(1) 1950). Example 2.3 payoffs and Pareto sentence at :107 (both players 3 at (C,C), 1 at (D,D)). Example 4.1 q1 = 1/2, q2 = 30: price 139/2, profit 119/4 (recompute PASS). Example 4.3 ties at 870 and 930 (recompute PASS)."),
 row("E2a-r3-L01-misconceptions", "2.9 misconceptions", "course/modules/E/E2/L01.html:293-309", "PASS",
     "Misconception 1: (C,C) gives 3 each vs (D,D) 1 each. Misconception 2: matching pennies, four profiles. Misconception 3: payoffs 5, 3, 6 for player 1 (the single-deviation claim is correct because the check is over all actions)."),
 row("E2a-r3-L01-quiz", "2.9 quiz", "course/modules/E/E2/L01.html:434-508", "PASS",
     "Answers and explanations re-checked: 900 (price 40, profit 30 x 30); 3 pure equilibria; 60 comparisons; 12 profiles; 'no, not in general' with totals 2 vs 6; 870 ties; 'Proposition 3.2 no pure equilibrium'. Items with data-answer match the derivations."),
 row("E2a-r3-L02-prop-2.5-proof-gap", "2.4 proof", "course/modules/E/E2/L02.html:127-135", "PASS",
     "Prop 2.5 proof: first-price payment beta * n * int x^n = (n-1)/(n+1) (recompute PASS). Second-highest CDF x^n + n(1-x)x^{n-1}, density n(n-1)x^{n-2}(1-x), mass 1 and mean (n-1)/(n+1) all recomputed for n=2..5. Assumption 4 (ties probability 0) used where stated."),
 row("E2a-r3-L02-R1-solution-gap", "2.4 solution", "course/modules/E/E2/L02.html:355-359", "PASS",
     "R1 (V_j = H Z_j, c = b/H, u = v/H): win probability (c/beta)^{n-1} for c <= beta and 1 for c >= beta; payoff H(u-c)(c/beta)^{n-1} and H(u-c). Step 3 and 4 transfer. Brute-force check at H = 5/2, n = 3 over 401 bids per value (recompute_r6.py): PASS. The ratio/scaling claim 'b = beta v' holds."),
 row("E2a-r3-L02-prop-claims-lab-prints", "2.5 lab claims", "course/modules/E/E2/L02.html:145, 231-240", "PASS",
     "Hypothesis says 21 of 21 and 1201 grid bids; printed lines '21 of 21 values' for n=2..5 and 'equal True, density mass 1' with 1/3, 1/2, 3/5, 2/3 for n=2..5 (run output). Recomputed exactly in recompute_r6.py (closed form best on the 1201-point grid for all 21 values, n=2..5)."),
 row("E2a-r3-L02-misconceptions-quiz-problems", "2.9 problems", "course/modules/E/E2/L02.html:257-270, 278-355, 358-375, 397-466", "PASS",
     "M1 0.072, M2 0.32 vs 0, M3 1/16 (0.0625), P1-P3, E1-E3 (1/2 and 3/5 recomputed), R1-R3, quiz answers 0.4, 0.072, 0.0625, 0.5, 1201 and explanations re-checked. Misconception 'Lab 2 proves ...' correctly limited to a finite check."),
 row("E2a-r3-L03-def-prop-2.1", "2.4 definitions/proofs", "course/modules/E/E2/L03.html:55-88", "PASS",
     "Def 1.1 values 12000, 6000, costs 10000, 4000, gains 2000 each (recompute PASS). Def 1.2 and Prop 2.1 set {6000: alpha<1} union {6000+6000 alpha: alpha >= 2/3}: exact check on a 0.1-cent grid over [0, 15000] (recompute_r6.py) reproduces the set for alpha = k/10. Range analysis at :83-87 matches (4000 threshold, 10000 threshold, 2/3 algebra)."),
 row("E2a-r3-L03-prop-2.3-remark-2.4", "2.4 statements", "course/modules/E/E2/L03.html:96-107", "PASS",
     "Prop 2.3: traded share 1 - alpha and gains lost 2000 alpha at 6000 (recompute PASS); full trade at 6000 + 6000 alpha for alpha >= 2/3, no loss; full-information gain 2000 for every alpha. Remark 2.4 threshold (c_H - w_L)/(w_H - w_L) = 2/3 (recomputed)."),
 row("E2a-r3-L03-lab-hypothesis-and-output", "2.5 lab", "course/modules/E/E2/L03.html:116, 184-199", "PASS",
     "Hypothesis: alpha 0-0.6 one price 6000; 0.7, 0.8, 0.9 two prices 10200, 10800, 11400; alpha = 1 only 12000; threshold 2/3; gains lost 2000 alpha. Printed output (run_labs) matches each item; 6000 + 6000 alpha values recomputed."),
 row("E2a-r3-L03-akerlof-attribution", "3 attribution", "course/modules/E/E2/L03.html:212, 437", "PASS",
     "registry akerlof1970market: 'The Market for \"Lemons\": Quality Uncertainty and the Market Mechanism', 1970, status verified. L03.html:437 quotes that title and year and states that no passage or result is attributed. L03.html:212 says the same. No other attribution on the page."),
 row("E2a-r6-L02-def-1.1-finite-types-contradiction", "2.2 prose vs definitions: Definition 1.1 finite type sets vs the auction", "course/modules/E/E2/L02.html:94 (and :85)", "FAIL",
     "L02.html:94 reads 'The auction fits Definition 1.1 with each bidder's type equal to its value. Definition 1.1 requires finite type sets, and the values are continuous, so the auction is not a finite Bayesian game.' Definition 1.1 (L02.html:57) requires 'a finite nonempty set of types Theta_i', so the first sentence asserts a fit that the next sentence denies. Introduced by the round-6 edit: the 04626e9 text was 'The auction is a Bayesian game in which each bidder's type is its value.' L02.html:85 ('The rest of the lesson concerns games with a continuum of types') carries the same tension with Definition 1.1. Fix: replace the first sentence of L02.html:94 with 'The auction is a Bayesian game in which each bidder's type is its value, but Definition 1.1 requires finite type sets and the values are continuous, so the auction lies outside Definition 1.1.' and reword L02.html:85 so it says the continuum case is treated by extending Definitions 1.2 and 1.3. Then re-run check_pages, check_dag, run_labs (no lab change).",
     fix="Edit L02.html:94 and :85 as stated in the evidence; re-run check_pages --unit E2, check_dag --unit E2 and run_labs --unit E2."),
 row("E2a-r6-L01-cournot-tie-grid", "2.2/2.4 grid and tie claims", "course/modules/E/E2/L01.html:159, 166, 272-274, 392, 422", "PASS",
     "Independent enumeration over the 91 x 91 grid (recompute_r6.py): tie-allowed set [(29,31),(30,30),(31,29)], profits [(870,930),(900,900),(930,870)], strict set [(30,30)]; Ex 4.3 ties at 870 (q1 = 29, 30 against 31) and 930 (q2 = 30, 31 against 29) PASS."),
 row("E2a-r6-L02-R1-and-L03-price-set", "2.4 mathematics", "course/modules/E/E2/L02.html:358; L03.html:72-87", "PASS",
     "L02 R1 scaled-support closed form brute-checked at H = 5/2, n = 3 (PASS). L03 Prop 2.1 set checked on a 0.1-cent grid over [0, 15000] for alpha = k/10 (PASS)."),
]

frag = {
 "unit": "E2",
 "slice": "a",
 "round": 6,
 "round_note": "Round 6 independent verification of E2-a at pin 9fd6aed (checkout /Users/billyribeiro/.fanout/wt/verifyC6-E2-a). Previous pin 04626e9 (round-5 fragment /Users/billyribeiro/.fanout/frags/C-E2-a.round5.json, used as context only).",
 "verifier": "Haiku independent verifier, E2-a round 6 (did not build E2)",
 "pin": "9fd6aed",
 "base": "04626e9 (round-5 pin). Delta for slice a: course/modules/E/E2/L01.html (lines 107, 331, 392-399, 406), L02.html (37, 51, 60, 85, 94, 102, 107-113 unchanged text, 245, 251, 268, 358), L03.html (220, 325). index.html, all three twins and lab-E2-L0{1,2,3}-1.py are byte-identical since 04626e9.",
 "checkout": "/Users/billyribeiro/.fanout/wt/verifyC6-E2-a",
 "scratch": "ledgers/E2/scripts/E2-a-r6/",
 "verified_at": "2026-10-29T00:00:00+00:00",
 "verdict": "FAIL",
 "rows": rows,
 "mutants": [],
 "registry_flags": [
   "references/references.json, notation/notation.json, tools/** unchanged 04626e9..9fd6aed (git diff --stat empty for these paths). verify_refs --offline: 560 entries, 0 problems. Live Crossref not run.",
   "Hub reading list titles checked against registry: the Vickrey registry title is stored in capitals and the Nash title as 'n -person'; the hub uses sentence case and 'n-person'. Typographic only, recorded as a note, not a finding."
 ],
 "freshness_flags": [
   "index.html byte-identical since 04626e9 (git diff empty). L08.html changed in the delta (2 lines); it is outside slice a, only its h1 and the SIMULATED label, which the hub cites, were re-read.",
   "--page index is not a valid check_pages use (it treats index as a lesson); the unit-level check_pages run is authoritative for index."
 ],
 "notes": [
   "Delta re-read in full: L01 M3 solution (:331) now says the lab 'stops a check at the first action that does better' (verified against all() in the twin); L01 R3 (:406) fixed the round-5 stray </p> (FAIL row closed); L01 Example 2.3 Pareto sentence (:107); L01 :392 R1 solution.",
   "L02: why-it-matters (:51) now names L03 and L04; the R1 solution uses Z_j for the unit-uniform variable (no clash with V_j); Step 4 'at most ... with equality only at b = beta' correct; Assumption-4 description matches Assumption 4 text.",
   "L03: misconception :220 wording and R2 :325 now name the full-trade price as the zero-loss case; both recomputed.",
   "Mutants: none. Slice a has no project graders; lab twins are demonstrations (VERIFIER_RULES ruling). Lab-twin mutation not required.",
   "Not checked: live verify_refs (network not used); cards.json (slice b/c); build_site.py and render_curriculum.py (not in slice a gate list); project.html and grader (not in slice a); L08 and L04-L09 content beyond the hub cross-references; no mutation or alternative-implementation run (no graders in slice)."
 ],
 "summary": "E2-a round 6 at 9fd6aed (delta since 04626e9): FAIL on one new row. The round-5 FAIL (stray </p> at L01.html:406) is fixed and verified. The round-6 edit to L02.html:94 introduces a contradiction: it says the auction 'fits Definition 1.1' and then that Definition 1.1 (finite type sets) is not met; L02.html:85 has the same tension. All gates re-run at 9fd6aed pass (check_pages unit, check_dag, check_projects, run_labs 12/12, isolated twins rc 0 with empty stderr, page code == twin and expected == stdout, page_smoke 4 pages, ruff, ruff format, mypy strict, pytest 3 files, verify_refs offline, fetch_data). Recomputation 57/57 PASS (recompute_r6.py)."
}

out = ROOT / "ledgers/E2/E2-a.json"
out.write_text(json.dumps(frag, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out, "rows", len(rows), "fail", sum(r["status"]!="PASS" for r in rows))
