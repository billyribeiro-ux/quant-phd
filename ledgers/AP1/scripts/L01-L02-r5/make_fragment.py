import json, sys
from datetime import datetime, UTC

CARRY = "Carried from round 4 (course/modules/AP/AP1/L01.html, L02.html and tests/labs/AP1/lab-AP1-L0[12]-*.py byte-identical since 9c8f3e4; git diff --quiet 9c8f3e4 33fd452 exit 0):"
R = []
def row(id_, check, location, status, evidence):
    R.append({"id": id_, "check": check, "location": location, "status": status, "evidence": evidence})

row("L01-L02-cmd-pin", "2.9-structure", "repository",
    "PASS",
    "Checkout HEAD 33fd452 (git rev-parse --short HEAD). `git diff --quiet 9c8f3e4 33fd452 -- course/modules/AP/AP1/L01.html course/modules/AP/AP1/L02.html tests/labs/AP1/lab-AP1-L01-1.py tests/labs/AP1/lab-AP1-L01-2.py tests/labs/AP1/lab-AP1-L02-1.py tests/labs/AP1/lab-AP1-L02-2.py` exit 0; `git diff --quiet 9c8f3e4 33fd452 -- course/assets/data` exit 0. Slice-relevant changed files since 9c8f3e4 (git diff --stat): course/modules/AP/AP1/cards.json (one line, AP1-c009), references/references.json (used_by AP1 added to hansen1991implications, kalyuga2003expertise, shleifer1997limits, tetzlaff2025cornerstone; generated_at), tools/data_sources.yaml (H.10 note text; licence quote unchanged), tools/page_smoke.py and tests/test_page_smoke.py, curriculum/curriculum.json (four sources added to AP1 module sources only), course/modules/AP/AP1/project.html and L03.html (not in slice). Python 3.14.8 (.venv/bin/python -c sys.version).")

row("L01-L02-cmd-run_labs", "2.5-lab", "tests/labs/AP1/lab-AP1-L01-*, lab-AP1-L02-*",
    "PASS",
    "Re-run on 33fd452: `.venv/bin/python tools/run_labs.py --unit AP1 --page L01` -> 'run_labs AP1: PASS (2/2)' rc 0; `--page L02` -> 'run_labs AP1: PASS (2/2)' rc 0 (logs /tmp/ap1-r5/L01-L02/run_labs_L01.log, run_labs_L02.log). run_labs compares stdout to the page's expected output (tools/run_labs.py docstring line 12).")

row("L01-L02-cmd-page_smoke", "2.9-structure", "course/modules/AP/AP1/L01.html, L02.html; tools/page_smoke.py",
    "PASS",
    "Re-run (changed tool): `.venv/bin/python tools/page_smoke.py --unit AP1 --pages L01 L02` (full run incl. figure sweep, both themes, both widths; log /tmp/ap1-r5/L01-L02/page_smoke.log) -> 'page_smoke modules/AP/AP1/L01.html: PASS', 'page_smoke modules/AP/AP1/L02.html: PASS', 'page_smoke AP1: PASS' rc 0. Lab timings: L01 lab-1 0.0 s, lab-2 0.0 s; L02 lab-1 0.0 s, lab-2 0.2 s (limit 10 s, tools/page_smoke.py LAB_LIMIT_S). The tool checks console errors, external requests, .katex-error and strict KaTeX re-parse (tools/page_smoke.py lines 103-122, 158). Unit tests of the changed preload: `.venv/bin/pytest tests/test_page_smoke.py -q` -> 7 passed.")

row("L01-L02-cmd-check_pages", "2.9-structure", "course/modules/AP/AP1/L01.html, L02.html",
    "PASS",
    "Re-run: `tools/check_pages.py --unit AP1 --page L01` -> 'check_pages AP1 L01: PASS' rc 0; `--page L02` -> 'check_pages AP1 L02: PASS' rc 0; `--unit AP1` -> 'check_pages AP1: PASS' rc 0.")

row("L01-L02-cmd-check_dag", "2.9-structure", "AP1 (curriculum.json, L01/L02 concept links)",
    "PASS",
    "Re-run: `tools/check_dag.py --unit AP1` -> 'check_dag AP1: PASS' rc 0. Independent closure check in row L01-L02-dag-closure.")

row("L01-L02-cmd-verify_refs-offline", "2.1-citation", "references/references.json",
    "PASS",
    "Re-run: `.venv/bin/python tools/verify_refs.py --offline` -> 'offline integrity: 560 entries, 0 problems' rc 0. `tools/fetch_data.py --check` -> 'fetch_data: 3 datasets, 0 problems' rc 0.")

row("L01-L02-cmd-verify_refs-live", "2.1-citation", "references/references.json (AP1 scope: 9 entries incl. shleifer1997limits)",
    "PASS",
    "Re-run live on 33fd452 from this sandbox: `.venv/bin/python tools/verify_refs.py --unit AP1` -> final line 'live re-verification of AP1: 9 of 560 entries, 0 problems', rc 0 (log /tmp/ap1-r5/L01-L02/verify_live_AP1.log). The 9 entries are exactly the registry entries whose used_by contains AP1 (cochrane2005asset, delbaen1994general, duffie2001dynamic, hansen1991implications, harrison1979martingales, harrison1981martingales, kalyuga2003expertise, shleifer1997limits, tetzlaff2025cornerstone). Round 4's network failure (403 Tunnel) did not recur.")

row("L01-L02-cmd-lint-twins", "2.5-lab", "tests/labs/AP1/lab-AP1-L0[12]-*.py",
    "PASS",
    "Re-run: `.venv/bin/ruff check tests/labs/AP1/lab-AP1-L01-1.py ... L02-2.py` -> 'All checks passed!'; `.venv/bin/ruff format --check tests/labs/AP1/lab-AP1-L0[12]-*.py` -> '4 files already formatted'; `.venv/bin/mypy` (strict, repo config) -> 'Success: no issues found in 101 source files'.")

row("L01-L02-cite-shleifer1997limits", "2.1-citation", "L01.html section 6 bullet 2 (line 329); L02.html section 5 bullet 2 (line 235); cards.json AP1-c009",
    "PASS",
    "Registry: references/references.json key shleifer1997limits, DOI 10.1111/j.1540-6261.1997.tb03807.x, Shleifer & Vishny, 'The Limits of Arbitrage', J. Finance 52(1) 35-55 (1997), status verified (Crossref); used_by now includes AP1 (round-4 registry flag resolved), and the live run above re-resolved it with 0 problems. Attribution re-read from the article itself: the publisher pages are 403 to WebFetch, so I read the JSTOR-stamped PDF copy at https://web.stanford.edu/~piazzesi/Reading/ShleiferVishny1997.pdf by page image. Abstract (p. 35): 'such professional arbitrage ... conducted by a relatively small number of highly specialized investors using other people's capital'. p. 38 and p. 40: arbitrageurs 'manage other people's money' and investors allocate funds on past returns. p. 41: G(x)=ax+1-a with a>=1, 'if a > 1, funds are actually withdrawn in response to poor performance'. p. 45 Proposition 3 (a>1, F2<D1, F2/p2<D1/p1 liquidation after noise-trader deepening). The locator 'pp. 38-41; Proposition 3, p. 45' is correct, and the claim in L01 line 329 and L02 line 235 is what the paper shows.")

row("L01-L02-scope-shleifer-a", "2.1-scope", "L01.html line 329; L02.html line 235; cards.json AP1-c009",
    "PASS",
    "Re-checked (changed). L01 line 329 states the condition in words ('when funds respond strongly enough to past performance') and says 'The model's conclusions about when arbitrage is cut back are results inside that model; whether it describes a given market is an empirical question the model does not settle.' L02 line 235 says 'a model ... in which such a trade may have to be cut back'. Card AP1-c009 back: 'In Shleifer and Vishny's model (Section 6), arbitrageurs ... can be cut back ... the model does not settle whether a market behaves this way.' The paper's result is for its own one-period, three-date model with a noise-trader shock and a linear G (p. 41, eq. 5); the pages and the card keep it inside that model. No generalization to markets in general remains.")

row("L01-L02-grade-shleifer1997limits", "2.3-grade", "L01.html section 6 bullet 2; L02.html section 5 bullet 2; key results",
    "PASS",
    "Round-3/4 FAIL re-checked. Regex `class=\"claim\"[^>]*data-cite=` count on L01.html and L02.html at 33fd452 -> 0 and 0; `data-grade=\"C\"` occurrences on L01/L02 -> only the legend rows (L01.html:47, L02.html:47). The shleifer span is an ungraded `<span class=\"ref\">` in a bullet, so no graded claim cites it and no Arnold 2009 counter-evidence rule binds it.")

row("L01-L02-grade-L01-ungraded-practice", "2.3-grade", "L01.html section 6 bullet 2 (line 329)",
    "PASS",
    "Re-read the whole bullet at 33fd452: it reports a model's conditional result and marks it as not settling practice. Its sentences state the page's own argument (closing a violation needs trading in size, and continuing when it widens), the model's assumption, and the explicit hedge. No ungraded claim is presented as a fact about markets.")

row("L01-L02-keyresult-shleifer-wording", "2.1-scope", "L01.html key results (6 rows); L02.html key results (5 rows)",
    "PASS",
    "Re-checked: grep -n 'shleifer' on L01.html and L02.html restricted to lines after 440 (key results start at L01 line 472) -> no hits; the citation appears only in the bullets above. The round-3 'Shleifer-Vishny' key-results rows are absent at 33fd452 (git diff 9bf6f33 9c8f3e4 from round 4 showed only '-' lines, unchanged since).")

row("L01-L02-cite-du2018deviations-removed", "2.1-citation", "L01.html, L02.html, cards.json",
    "PASS",
    "Re-run: `grep -c du2018 course/modules/AP/AP1/L01.html course/modules/AP/AP1/L02.html` -> 0, 0; `grep -c du2018 course/modules/AP/AP1/cards.json` -> 0 (grep at 33fd452). No Du-Tepper-Verdelhan text on the slice.")

row("L01-L02-cite-no-other-keys", "2.1-citation", "L01.html, L02.html",
    "PASS",
    "Re-run: `grep -o 'data-cite=\"[^\"]*\"' L01.html L02.html` -> one line each, 'data-cite=\"shleifer1997limits\"'. cards.json cite arrays (AP1-c009 only) -> ['shleifer1997limits']. No other registry key and no free-text reference on the slice.")

row("L01-L02-grade-L01-theorems", "2.3-grade", "L01.html Prop 2.2, Thm 2.4, Cor 2.5, Prop 2.6, Prop 3.1; key results rows 1-4",
    "PASS",
    "Re-run grep at 33fd452: `data-grade=\"T\"` count on L01.html = 12 (theorem/proposition title spans and key-results rows). Grade of each title span matches BLUEPRINT §3 for a theorem with a complete proof (T); proofs re-derived in rows math-L01-prop22, thm24, cor25, prop26, prop31.")

row("L01-L02-grade-L02-theorems", "2.3-grade", "L02.html Prop 1.2, Lemma 2.1, Thm 3.1, Cor 3.3, Prop 4.1; key results rows 1-5",
    "PASS",
    "Re-run grep at 33fd452: `data-grade=\"T\"` count on L02.html = 11. Title spans re-read (L02.html lines 70, 84, 97, 118, 220). Proofs re-derived in rows math-L02-prop12, lemma21, thm31, cor33-prop41.")

row("L01-L02-grade-L01-keyresult-lab2", "2.3-grade", "L01.html key results row (line 481); cards.json AP1-c008",
    "PASS",
    "Re-read at 33fd452: key-results row 'The one-month DKK and EUR spot payoffs ... R^2 of 0.99891 ... condition number 2.776 x 10^7' carries data-grade C with basis 'Lab 2 (single sample: H.10 month-end spot rates, retrieved 2026-10-19)'. Card AP1-c008 grade C with the same basis. Both numbers recomputed independently in row num-L01-lab2-out. Single-sample grade C is consistent with BLUEPRINT §3 (no second sample claimed).")

row("L01-L02-math-L01-ex32", "2.4-math", "L01.html Example 3.2 (lines 234-239), key results row 7, cards.json AP1-c010",
    "PASS",
    "Re-derived by hand: dollar bond costs 1/(1+r), foreign bond costs S0/(1+r~), forward = one foreign bond minus F dollar bonds in every state; zero cost gives F = S0(1+r)/(1+r~) with no dependence on S1. Exact fractions (lab1_indep.py, /tmp/ap1-r5/L01-L02/recompute/lab1_indep.py): S0=1.10, r=0.04, r~=0.02 -> F = 1.1215686274509804; cost at quote F+0.01 = -0.0096153846. Matches the page text 1.121569 and 'replica cost -0.009615'.")

row("L01-L02-lab-check-ex32", "2.4-math", "L01.html Lab 1 hypothesis (line 149) and lab output; tests/labs/AP1/lab-AP1-L01-1.py lines 38-53",
    "PASS",
    "Re-run: run_labs L01 PASS (above). Independent recomputation (exact fractions) reproduces 'forward price F = 1.121569' and 'quoted F = 1.131569: replica cost -0.009615'. The twin's last lines check the Example 3.2 identity against the page output.")

row("L01-L02-math-L01-R1", "2.4-math", "L01.html Problem R1 (lines 439-445); section 6 bullet 1 (line 328)",
    "PASS",
    "Re-read R1 statement and proof at 33fd452. (<=) direction (lines 443) re-derived: p^a t+ - p^b t- >= p~ t+ - p~ t- = p~ t, summed, and zero on ker X. Convexity and subadditivity of kappa (line 442) re-derived: t+ is convex, and p^a t+ - p^b t- = p^b t + (p^a - p^b) t+. The (=>) LP-duality step (line 444) is carried from round 4 (byte-identical since 9c8f3e4). Reading paragraph (line 445) re-derived: with p^a = p^b, p~ = p is forced, and kappa(theta)+kappa(-theta) = sum (p^a - p^b)|theta| (round-trip spread).")

row("L01-L02-math-L01-prop22", "2.4-math", "L01.html Proposition 2.2 (lines 79-87)",
    "PASS",
    "Re-derived at 33fd452 (text lines 80-89): (=>) theta in ker X gives X theta = 0 = X 0 so p'theta = 0; (<=) X theta = X theta' gives theta - theta' in ker X and p'(theta - theta') = 0. Equivalence with p perp ker X is the definition of perp. Closing claim on full column rank is correct (ker X = {0}).")

row("L01-L02-math-L01-thm24", "2.4-math", "L01.html Theorem 2.4 and proof (lines 102-118)",
    "PASS",
    "Re-derived at 33fd452 (lines 103-117): (i)=>(ii) q well defined by LOOP and linear; uniqueness since any linear pricing q' equals q on X theta. (ii)=>(iii): q o P extended to R^S, psi_s = q~(e_s), (X'psi)_n = q(X e_n) = p_n. (iii)=>(i): X theta = 0 gives p'theta = psi'X theta = 0. All three implications and the uniqueness claim hold.")

row("L01-L02-math-L01-cor25", "2.4-math", "L01.html Corollary 2.5 (lines 122-130)",
    "PASS",
    "Re-derived: Theorem 2.4 (i)<=>(iii) states LOOP iff p is in range(X'). Combined with Proposition 2.2 this gives range(X') = (ker X)-perp, which is the rank-nullity identity used in P1. Text at 33fd452 lines 124-129 matches.")

row("L01-L02-math-L01-prop26", "2.4-math", "L01.html Proposition 2.6 (lines 132-140)",
    "PASS",
    "Re-derived (text lines 134-139): psi - psi0 in ker X' iff X'psi = p; rank-nullity on X': R^S -> R^N gives dim ker X' = S - rank X; zero iff rank X = S iff M = R^S (since M = range X has dimension rank X). Statement correct.")

row("L01-L02-math-L01-prop31", "2.4-math", "L01.html Proposition 3.1 (lines 223-232)",
    "PASS",
    "Re-derived at 33fd452 (lines 224, 229): if z not in M, X theta + a z = 0 forces a = 0 (else z in M), so X theta = 0 and p'theta = 0; if z in M, (theta_z, -1) pays zero so LOOP requires c = p'theta_z; converse by X(theta + a theta_z) = 0 giving p'theta + a c = 0. Statement correct.")

row("L01-L02-math-L01-s5", "2.4-math", "L01.html section 5 (lines 318-322)",
    "PASS",
    "Re-derived: q(R) = q(z)/q(z) = 1 by linearity; q(1) = sum psi_s; R_f = 1/sum psi_s when the sum is nonzero. Example 5.1: 1/0.96 = 1.0416667 -> 1.041667 and 4.1667%; direction v = (-0.5, 0.8, -0.3) sums to 0, so the price of payoffs in M is unchanged along the line (recomputed: ker X' direction from np.cross and residual 4.4e-16 in lab1_indep.py).")

row("L01-L02-math-L01-P1-P3", "2.4-math", "L01.html Problems P1-P3 (lines 389-406)",
    "PASS",
    "Re-read at 33fd452. P1: (subset) y = A'u, x in ker A gives y'x = u'Ax = 0; (superset) dimension count rank A' = rank A = n - dim ker A. P2: psi'X theta = p'theta = q(z); M-perp = ker X' by P1 applied to X'; set is psi + M-perp of dimension S - rank X. P3: projection psi_M = P psi still prices X; uniqueness of the minimum-norm solution by Pythagoras. All three arguments hold as written.")

row("L01-L02-math-L01-E1", "2.4-math", "L01.html Problem E1 (line 415-417)",
    "PASS",
    "Recomputed in lab2_indep.py (numpy 2.4.6, Python 3.14.8, MANIFEST snapshot fx_monthly.csv): smallest eigenvalue 3.606846e-07, E_T[(DKK-EUR)^2]/2 = 3.8073e-07 (page prints 3.807e-7). Ratio (3.807-3.607)/3.807 = 5.25% -> '5% lower' correct. Rayleigh argument (u = (1,-1)/sqrt2) is a valid upper bound since lambda_min = min u'Au.")

row("L01-L02-math-L01-R2-R3-E2-E3", "2.4-math", "L01.html E2 (line 424), E3 (line 431), R2 (lines 449-459), R3 (lines 461-466)",
    "PASS",
    "Recomputed: E2 T = 332 payoff rows (lab2_indep.py: 'payoff rows (332, 10)'), 332-10 = 322 state-price dimension, rank 10 since the second-moment matrix is invertible (eig min 3.6e-7 > 0). E3: 1 - 0.9956 = 0.0044, 0.0044/0.9956 = 0.00442. R2 and R3 text re-read: no numbers beyond those, arguments consistent with Proposition 2.6 and Proposition 2.2.")

row("L01-L02-math-L01-notation", "2.4-math", "L01.html Example 3.2, Lab 1 hypothesis, key results row 7, Problem R3",
    "PASS",
    "Re-checked: notation uses r, r~, S0, S1, F, k=rank X, consistent with notation.json as carried from round 4 (no collision with the registry symbol r); grep for 'r = rank' -> none in L01.html; R3 uses k = rank X (line 465).")

row("L01-L02-math-L01-notation-a", "2.4-math", "L01.html, L02.html, cards.json AP1-c009",
    "PASS",
    "Re-run: grep -nE 'a &gt; 1|a > 1|equation \\(5\\)' on L01.html, L02.html and cards.json -> no hits. Symbol 'a' on the new c009 text is not used; the fund-flow parameter a appears only in the registry-cited paper, not in the course text.")

row("L01-L02-math-L02-prop12", "2.4-math", "L02.html Proposition 1.2 (lines 69-77)",
    "PASS",
    "Re-derived (L02.html lines 70-76): if X theta = 0 and p'theta != 0 then whichever of theta, -theta has negative cost is an arbitrage (its cash-flow vector (-p'theta, 0) is nonnegative, nonzero). Converse counterexample: one asset, one state, payoff 1, price -1: LOOP holds (ker X = {0}) and buying pays 1 today and 1 tomorrow, an arbitrage.")

row("L01-L02-math-L02-lemma21", "2.4-math", "L02.html Lemma 2.1 (lines 83-92)",
    "PASS",
    "Re-derived step by step (lines 85-91): w = Qk* with Q = I - P; w in L-perp; w != 0 since w = 0 puts k* = Pk* in L cap K; for k in K, f(t) = ||Q k_t||^2 minimized at t = 0 gives w'(k - k*) >= 0 (using Q symmetric, Qw = w); w'k* = ||w||^2 gives w'k >= ||w||^2 > 0.")

row("L01-L02-math-L02-thm31", "2.4-math", "L02.html Theorem 3.1 (lines 96-110)",
    "PASS",
    "Re-derived (lines 106-109): (<=) psi >> 0 gives sum psi_s (X theta)_s = 0 so all (X theta)_s = 0 and p'theta = 0, not an arbitrage. (=>) separation gives w >> 0 with w perp L (taking the unit vectors of K shows w_j > 0), X'w_{1:S} = w_0 p, so psi = w_{1:S}/w_0 >> 0 and X'psi = p. Both directions hold.")

row("L01-L02-math-L02-cor33-prop41", "2.4-math", "L02.html Corollary 3.3 (l.117-125), Proposition 4.1 (l.219-227), section 4 interval remark (l.229)",
    "PASS",
    "Re-derived: Cor 3.3: q(z) = psi'z > 0 for z >= 0, z != 0 with psi >> 0 (Problem P2 identity), R_f = 1/sum psi > 0. Prop 4.1: Theorem 3.1 applied to (X z) with prices (p, c) gives c = psi'z for some psi >> 0; converse by the same theorem. Text re-read at 33fd452.")

row("L01-L02-math-L02-problems", "2.4-math", "L02.html M1-M3 (lines 270-290), P1-P3 (lines 295-313), E1-E3 (lines 320-338), R2 (lines 340-364)",
    "PASS",
    "Recomputed M1: state prices (1.016667, -0.066667) from 0.3 psi1 = 0.305; largest arbitrage-free price 0.95*1.2 = 1.14; cost -1.16 + 1.14 = -0.02; cash flow (0, 0.3). M2: interval (0.686, 1.47). M3: sum 0.98, value 1.078, direction d = (1,-2,1,0) with sum 0 and x'd = 0, psi + 0.05d = (0.19, 0.1, 0.45, 0.24) sums to 0.98 and prices the stock at 1.078. P1 Stiemke argument, P2 positivity argument, P3 simplex argument re-read and consistent with Lemma 2.1 (compactness attains the distance). R2 carried from round 4 (byte-identical since 9c8f3e4).")

row("L01-L02-math-L02-notation", "2.4-math", "L02.html", "PASS",
    "Re-read at 33fd452: Lemma 2.1 (L, K, P, Q, w), Theorem 3.1 (psi, w_0, K, G), Proposition 4.1 (z, c, psi) use each symbol with one meaning; no redefinition in the statements read (L02 lines 84-125, 220-226).")

row("L01-L02-num-recompute", "2.2-number", "L01.html and L02.html: Examples 2.7, 3.2, 4.1, 5.1, 3.4; Lab outputs; M/E problems; quiz numerics",
    "PASS",
    "Full numeric recomputation under Python 3.14.8 / numpy 2.4.6 (scripts /tmp/ap1-r5/L01-L02/recompute/lab1_indep.py and lab2_indep.py, run with python -I): Example 2.7 cost -7/500 = -0.014, scale 71.42857, repriced fund 1.936; Example 3.2 F = 1.1215686, replica cost -0.0096153846; Lab 1 psi at t = 0, 0.25, 0.7 (0.302, 0.3167, 0.3412 / 0.177, 0.5167, 0.2662 / -0.048, 0.8767, 0.1312) and kernel direction (-0.5, 0.8, -0.3); Lab 2 SVD/eig cond 2.7759e7, DKK-on-EUR slope 0.9956, R^2 0.99891, sd 261.9 and 8.65 bp, halves R^2 0.99919 / 0.99870, without DKK cond 1.0082e5. All match the page.")

row("L01-L02-num-L01-ex27", "2.2-number", "L01.html Example 2.7 (line 144), Lab 1 hypothesis (line 149)",
    "PASS",
    "Recomputed exactly (fractions): 0.96 + 0.976 - 1.95 = -7/500 = -0.014; 1/0.014 = 71.428571; 0.96 + 0.976 = 1.936; kernel direction (1,1,1) x (1.4,1.1,0.6) = (-0.5, 0.8, -0.3), residual 4.4e-16 in numpy. Page values match.")

row("L01-L02-num-L01-lab1-out", "2.2-number", "L01.html Lab 1 expected output and interpretation (lines 203-215)",
    "PASS",
    "(a) computed live: run_labs L01 PASS (above) compares the page's expected output. Independent recomputation (lab1_indep.py) reproduces every printed value: 'scaled portfolio' (71.4286), 'LOOP price 1.936', psi rows, 'forward price F = 1.121569', 'quoted F = 1.131569: replica cost -0.009615'. Interpretation 'at t = 0.7 the first state price is -0.048' matches psi row 3.")

row("L01-L02-num-L01-ex51", "2.2-number", "L01.html Example 5.1 (line 322)",
    "PASS",
    "Recomputed: psi sums to 0.96 by the bond's price; 1/0.96 = 1.0416667 -> 1.041667; 4.1667% = 0.041667 rounded. Direction v sums to 0 (-0.5 + 0.8 - 0.3 = 0).")

row("L01-L02-num-L01-lab2-out", "2.2-number", "L01.html Lab 2 expected output (lines 273-281 region of lab output)",
    "PASS",
    "(a) computed live: run_labs L01 PASS and page_smoke Pyodide PASS. Independent recomputation from the MANIFEST-pinned fx_monthly.csv (lab2_indep.py): 332 payoffs 1999-02 to 2026-09; eig smallest 3.606846e-07 (page 3.607e-7), next 1.243880e-04 (page 1.244e-4), largest 10.0122; condition 2.7759e7 (page 2.776e7); DKK slope 0.9956, R^2 0.99891, sd 261.9 bp, residual 8.65 bp; Rayleigh 3.8073e-07 (page 3.807e-7).")

row("L01-L02-num-L01-lab2-interp", "2.2-number", "L01.html Lab 2 interpretation (line 282 region), section 6 bullet 4, Misconception 4",
    "PASS",
    "Recomputed: smallest eigenvalue is 'more than 300 times smaller than the next' -> 1.243880e-4 / 3.606846e-7 = 344.9 (correct). 'R^2 of 0.99891 and a residual s.d. under 9 basis points a month, against 262 for the payoff itself' -> 8.65 bp and 261.9 bp (correct). 'The fit is about as tight in the two halves' -> R^2 0.99919 and 0.99870 (correct). Section 6 bullet 4 '9 basis points' is consistent with 8.65 bp.")

row("L01-L02-num-L01-ex41", "2.2-number", "L01.html Example 4.1 (lines 312-313)",
    "PASS",
    "Recomputed: 2.776e7 / 1.008e5 = 275.4 -> '275' (page says 275). '2.776e7' and '1.008e5' match lab2_indep.py (2.7759e7 and 1.0082e5). 'factor of up to about 28 million' and 'about 100 thousand' are consistent with the printed values.")

row("L01-L02-num-L01-problems", "2.2-number", "L01.html M1-M3 (lines 364-381), E1-E3 (lines 414-431)",
    "PASS",
    "Recomputed by hand and numpy: M1 cost 2*0.95 - 1.00 - 0.92 = -0.02, scaled 1/0.02 = 50, portfolio (100,-50,-50) cost -1.00. M2 psi1 = (1 - 0.8*0.97)/0.5 = 0.448, psi2 = 0.522, R_f = 1/0.97 = 1.030928. M3 price 0.448*2.1 + 0.522*1.1 = 1.515; replication a = -0.5, b = 2 gives cost -0.485 + 2.00 = 1.515. E1, E2, E3 as in row num-L01 problems rows above.")

row("L01-L02-num-L01-quiz", "2.2-number", "L01.html quiz items 3, 4, 7 (lines 483-514 region)",
    "PASS",
    "Recomputed: data-answer values re-read: 0.448 (quiz line 513 explain: M2 psi1, 0.5 psi1 = 1 - 0.776), 2 (quiz lines 515-518: S - rank X = 5 - 3 = 2, Proposition 2.6), 1.515 (M3 price). All three recomputed.")

row("L01-L02-num-L02-ex34", "2.2-number", "L02.html Example 3.4 (line 129), Misconception 4 (line 258)",
    "PASS",
    "Recomputed exactly: 0.96*0.6 = 0.576, 0.96*1.4 = 1.344; at c = 0.576 the portfolio (buy one stock, sell 0.6 bonds) costs 0 and pays (0.8, 0.5, 0); at c = 1.344 (sell one stock, buy 1.4 bonds) costs 0 and pays (0, 0.3, 0.8). The nonnegative vector (0, 0, 0.96) in Misconception 4 (L02 line 258) gives X'psi = (0.96, 0.6*0.96) = (0.96, 0.576), matching c = 0.576.")

row("L01-L02-num-L02-lab1", "2.2-number", "L02.html Lab 1 output and interpretation (lines 160-171)",
    "PASS",
    "(a) live: run_labs L02 PASS (above). Independent analytic recomputation: with 0.8a + 0.5b = c - 0.576 and a = b = t, t = (c-0.576)/1.3: c = 0.5 -> -0.058462 (page -0.058462); c = 0.976 -> 0.307692 = 4/13 (page 0.307692); c = 1.40 -> -0.050909 via a = 0.96-2t binding the d-state (page -0.050909); c = 0.576 and 1.344 -> 0 (page -0.000000). Interpretation 'the optimum is 4/13' and the psi = (4/13, 4/13, 0.96-8/13) verified: 2.5(4/13) + 0.6(0.96 - 8/13) = 0.976. Peak claim (E1) 0.32 at c = 0.992: psi = (0.32,0.32,0.32) gives X'psi = (0.96, 0.992).")

row("L01-L02-num-L02-lab2", "2.2-number", "L02.html Lab 2 output and interpretation (lines 205-212)",
    "PASS",
    "(a) live: run_labs L02 PASS. Printed psi = (0.307692, 0.307692, 0.344615): w[1:]/w[0] = (0.072375, 0.072375, 0.08106)/0.235219 = (0.307692, 0.307692, 0.344616), consistent to printed precision; X'psi = (0.96, 0.976) matches quoted prices. 'one of infinitely many' statement consistent with Proposition 2.6 (rank 2 < 3).")

row("L01-L02-num-L02-problems", "2.2-number", "L02.html M1-M3, E1-E3 (lines 270-338)",
    "PASS",
    "Recomputed: M1 1.016667 and -0.066667, 0.95*1.2 = 1.14, cost -0.02. M2 (0.686, 1.47). M3 sum 0.98, value 1.078, psi + 0.05 d = (0.19, 0.1, 0.45, 0.24) with sum 0.98 and 0.133 + 0.09 + 0.495 + 0.36 = 1.078. E1 0.992 = 0.32*3.1 and optimum 0.32 = 0.96/3. E2 width 0.96*0.8 = 0.768, upper end 0.96*2.0 = 1.92. E3 -1.40 + 1.344 = -0.056, sum of (0.056, 0, 0.3, 0.8) = 1.156.")

row("L01-L02-num-L02-quiz", "2.2-number", "L02.html quiz items 3 and 7 (lines 415-450)",
    "PASS",
    "Recomputed: 0.96 * 0.6 = 0.576 (answer to the lowest arbitrage-free price, open left end); 0.98 * 1.5 = 1.47 (upper end, four-state market). Both match the data-answer values.")

row("L01-L02-num-L01-new-text", "2.2-number", "L01.html lines 68, 329; L02.html line 235; cards.json AP1-c009",
    "PASS",
    "Numbers introduced since round 4: the locator 'pp. 38-41; Proposition 3, p. 45' (class (b); verified on the page images in row cite-shleifer1997limits); 'Section 6', 'Section 5', 'Problem R2', 'Lesson 2', 'Lesson 6' (cross-references, checked against section headings: L01 s6 'Where the canon breaks', L02 s5 'Where the canon breaks' and Problem R2 at line 449). No new numeric claim without a locator.")

row("L01-L02-lab-AP1-L01-1", "2.5-lab", "L01.html #lab-AP1-L01-1; tests/labs/AP1/lab-AP1-L01-1.py",
    "PASS",
    "Twin byte-identical to 9c8f3e4 (git diff --quiet exit 0). run_labs L01 PASS (2/2 includes this lab); page_smoke lab-AP1-L01-1 0.0 s, no problems. Lab hypothesis (line 149) matches the code; RNGs not used (deterministic linear algebra); no network access (page_smoke external-request check).")

row("L01-L02-lab-AP1-L01-2", "2.5-lab", "L01.html #lab-AP1-L01-2; tests/labs/AP1/lab-AP1-L01-2.py",
    "PASS",
    "Twin and page code unchanged since 9c8f3e4 (git diff --quiet exit 0 for the twin); run_labs L01 PASS 2/2; page_smoke lab-AP1-L01-2 0.0 s with no problems. Lab reads data/fx_monthly.csv via data-files (licence row L01-L02-data-fx_monthly).")

row("L01-L02-lab-AP1-L02-1", "2.5-lab", "L02.html #lab-AP1-L02-1; tests/labs/AP1/lab-AP1-L02-1.py",
    "PASS",
    "Twin byte-identical to 9c8f3e4; run_labs L02 PASS 2/2; page_smoke lab-AP1-L02-1 0.0 s (preload now parsed via ast, tools/page_smoke.py lab_preload) with no problems. The lab's LP (scipy linprog highs) reproduces the analytic values in row num-L02-lab1.")

row("L01-L02-lab-AP1-L02-2", "2.5-lab", "L02.html #lab-AP1-L02-2; tests/labs/AP1/lab-AP1-L02-2.py",
    "PASS",
    "Twin unchanged since 9c8f3e4; run_labs L02 PASS 2/2; page_smoke lab-AP1-L02-2 0.2 s with no problems. The projected-gradient outputs are the run_labs-verified values in row num-L02-lab2.")

row("L01-L02-data-fx_monthly", "2.8-figure", "L01.html Lab 2 data-files='fx_monthly.csv'; course/assets/data/market/fx_monthly.csv; MANIFEST.json; tools/data_sources.yaml (fx_monthly)",
    "PASS",
    "Data: `tools/fetch_data.py --check` -> 'fetch_data: 3 datasets, 0 problems' (SHA-256 against MANIFEST). course/assets/data unchanged since 9c8f3e4. Licence (opened at the issuer's pages on this run): https://www.federalreserve.gov/disclaimer.htm contains 'Please cite to the Board as the source of the information.' (verbatim, WebFetch), and the data_sources.yaml quote 'Unless otherwise indicated, information on Board's website is in the public domain and may be copied and distributed without permission' matches the page's paragraph as summarised (the full sentence was not retrievable verbatim because of the 125-character quote limit; the closing sentence and the public-domain grant match). https://www.federalreserve.gov/releases/h10/about.htm contains 'The rates have been certified by the Federal Reserve Bank of New York for customs purposes' and 'as required by section 522 of the amended Tariff Act of 1930' (verbatim), 'Last Update: February 06, 2023', and no terms-of-use sentence, so the data_sources.yaml note's claim 'about.htm states no terms of its own' holds. The H.10 note's quote without the former ellipsis matches the page. Redistribution is granted by the Board's default public-domain grant.")

row("L01-L02-figures-none", "2.8-figure", "L01.html, L02.html",
    "PASS",
    "Re-run: `ls course/modules/AP/AP1 | grep figures` -> none for L01/L02; `grep -c '<svg\\|data-chart' L01.html L02.html` -> 0, 0 at 33fd452. No figure on the slice.")

row("L01-L02-struct-L01-order", "2.9-structure", "L01.html", "PASS",
    "Carried from round 4 (course/modules/AP/AP1/L01.html byte-identical since 9c8f3e4): h2 headings re-read at 33fd452: 1 The one-period market | 2 The law of one price | 3 Pricing redundant payoffs | 4 Near-redundancy in data | 5 Linear pricing and returns | 6 Where the canon breaks | 7 Misconceptions | 8 Problem set | 9 Key results | 10 Retrieval quiz | 11 References.")

row("L01-L02-struct-L02-order", "2.9-structure", "L02.html", "PASS",
    "Carried from round 4 (course/modules/AP/AP1/L02.html byte-identical since 9c8f3e4): h2 headings re-read at 33fd452: 1 Arbitrage | 2 Separating a subspace from a simplex | 3 The fundamental theorem for finitely many states | 4 Prices of new payoffs | 5 Where the canon breaks | 6 Misconceptions | 7 Problem set | 8 Key results | 9 Retrieval quiz | 10 References.")

row("L01-L02-struct-hours", "2.9-structure", "course/modules/AP/AP1/index.html; L01-L07 data-hours; project.html data-hours-project",
    "PASS",
    "Re-run grep at 33fd452: data-hours=\"12\" on L01..L07 (7 x 12 = 84); index data-hours-lessons=\"84\"; data-hours-project=\"36\" on index and project.html; 84 + 36 = 120 = curriculum.json AP1 hours 120 (parsed). project.html changed in this round (grader check count text only), hours unchanged.")

row("L01-L02-struct-L02-html", "2.9-structure", "L02.html E1, E3 solutions", "PASS",
    "Carried from round 4 (byte-identical since 9c8f3e4): grep -n '</p></p>' L01.html L02.html -> no hits at 33fd452.")

row("L01-L02-struct-L01-dangling-ref", "2.9-structure", "L01.html Problem R2 solution, Execution bullet (line 456)", "PASS",
    "Carried from round 4 (byte-identical since 9c8f3e4). Re-read at 33fd452 (line 456): the bullet ends 'and only after the funding and capital costs of holding the position (AP6 takes these up)'; AP6 is not a prerequisite of AP1, but it is a later module (curriculum.json topological_order: AP1 at index 49, AP6 at 82), so 'AP6 takes these up' is a forward pointer, not a dangling reference.")

row("L01-L02-struct-L01-remark12-ref", "2.9-structure", "L01.html Remark 1.2 (line 68)", "PASS",
    "Carried from round 4 (byte-identical since 9c8f3e4). Re-read at 33fd452: 'Section 6 takes up the spread and the limits on trading in size; Lesson 2 (Section 5 and Problem R2) takes up short-sale ...'; L02 section 5 is 'Where the canon breaks' and L02 has 'R2 · No arbitrage under a short-sale ban' (grep at 33fd452).")

row("L01-L02-banned-phrases", "2.9-banned", "L01.html, L02.html", "PASS",
    "Re-run at 33fd452 with BUILDER_RULES §1.3-1.4 strings: `grep -niE 'TODO|TBD|lorem|for brevity|details omitted|beyond the scope|left as an exercise|you can add more|it is important to note|studies show|experts agree|it is well known|obviously|clearly|it can be shown'` -> 0 hits on both pages. Ellipsis check: four ellipsis characters (U+2026) per page, all at the end of quiz prompts (L01.html lines 493, 502, 530, 544; L02.html lines 397, 406, 429, 461), each a cloze to be completed by the learner, with the completed statement in the explain block (e.g. L01 line 499). This is not an ellipsis standing for omitted content; recorded as a judgment call, not a FAIL.")

row("L01-L02-dag-closure", "2.9-structure", "L01.html and L02.html concept links and dfns; index.html prereq list", "PASS",
    "Recomputed independently (/tmp/ap1-r5/L01-L02/recompute/dag_indep.py): AP1 prereq closure = AP2, CF1, CS1, E1-E4, FC1, FC2, M1-M8, P0.1, S0, S1 (from curriculum.json parsed; the curriculum change is only in AP1 module sources). dfn ids defined more than once across course/modules: 0. Concept links on L01 (11 distinct) and L02 (7 distinct) resolve to concept keys whose module is in the closure or AP1 (e.g. bid-ask-spread FC1, forward-contract FC2, condition-number M8, convex-function M7, lagrangian-duality M7, linear-map M3, probability-space M6, simple-return CS1, vector-space M3, compactness M5, convex-set M7), and each href anchor exists in course/concepts.html (grep id=). Local dfns: L01 law-of-one-price, state-price; L02 fundamental-theorem-of-asset-pricing, all AP1 introduces. No use before definition.")

row("L01-L02-dag-unlinked-uses", "2.9-structure", "L01.html Problem R1 solution (lines 442, 444)", "PASS",
    "Carried from round 4 (byte-identical since 9c8f3e4): 'convex function' at line 442 is a concept link (<a class=\"concept\" data-concept=\"convex-function\">) and 'Lagrangian duality' in line 444 is linked too (grep -c data-concept=\"lagrangian-duality\" on L01 -> 1 link).")

row("L01-L02-cards-slice", "2.7-cards", "cards.json AP1-c008, c009, c010, c091 (L01); c014-c024 and c081 (L02) sampled; full scan for duplicates", "PASS",
    "Full scan of cards.json (92 cards): no duplicate ids, no duplicate fronts. Slice has 28 cards (L01: c001-c013, c082, c085, c091 = 16; L02: c014-c024, c081 = 12). Sampled and checked against lesson text: c002 (Prop 2.2), c004 (Thm 2.4), c005 (Prop 2.6), c006 (Prop 3.1), c007 (Example 5.1), c008 (Lab 2 numbers 0.99891, 8.65 bp, 261.9 bp, 2.776e7 match the recomputation), c010 (Example 3.2 forward), c015 (Prop 1.2 and its counterexample), c016 (Lemma 2.1), c017 (Thm 3.1), c019 (Problem P3), c020 (Example 3.4 interval (0.576, 1.344)), c021 (Prop 4.1), c081 (Cor 3.3), c082 (Cor 2.5), c085 (Prop 2.6), c091 (Definition 1.1). Misconception cards c011-c013 checked against L01 lines 340-352; c022 against L02 line 258; c023 against L02 lines 235 and 253 (the 'high expected return relative to its risk' wrong-answer item). c024 against L02 lines 249-251 (misconception 'no arbitrage means the state prices are unique and positive': some positive vector exists; uniqueness needs rank X = S). Cards are atomic and not trivia.")

row("L01-L02-card-c009", "2.7-cards", "cards.json AP1-c009 (lesson L01)", "PASS",
    "Round-4 FAIL resolved. Front: 'Why can a law-of-one-price violation persist even though the zero-payoff portfolio has no risk at the horizon?' Back: 'Closing it needs someone who can trade that portfolio in size and keep trading it if the mispricing first widens. In Shleifer and Vishny's model (Section 6), arbitrageurs who invest other people's money can be cut back when investors withdraw funds after poor performance, which happens when funds respond strongly enough to past performance; the model does not settle whether a market behaves this way.' Matches L01 section 6 bullet 2 (line 329) and the paper (pp. 40-41, a>1 withdrawal; Prop 3 p. 45); cite key shleifer1997limits is in the registry and used_by AP1. No generalization to arbitrageurs in general remains.")

summary = {"rows": len(R), "pass": sum(r["status"] == "PASS" for r in R),
           "fail": sum(r["status"] == "FAIL" for r in R),
           "unverifiable": sum(r["status"] == "UNVERIFIABLE" for r in R),
           "mutants": 0, "fail_ids": [r["id"] for r in R if r["status"] != "PASS"]}
frag = {
    "unit": "AP1",
    "slice": "L01-L02",
    "round": 5,
    "verifier": "independent round-5 verifier for slice L01-L02 (did not build AP1; shares no context with the builders or the round-4 verifier)",
    "pin": "33fd452",
    "base": "9c8f3e4",
    "previous_ledger": "ledgers/AP1/L01-L02.json at 9c8f3e4 (round 4: 71 rows, 69 PASS, 1 FAIL, 1 UNVERIFIABLE)",
    "checkout": "/tmp/verify-ap1-r5-a (detached worktree at 33fd452)",
    "scratch": "/tmp/ap1-r5/L01-L02",
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "verdict": "PASS" if summary["fail"] == 0 and summary["unverifiable"] == 0 and summary["pass"] == len(R) else "FAIL",
    "rows": R,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Round-4 FAIL row L01-L02-card-c009 is resolved: card text matches L01 section 6 bullet 2 and the Shleifer-Vishny paper (read by page image from https://web.stanford.edu/~piazzesi/Reading/ShleiferVishny1997.pdf, since the Wiley and Stanford-PDF text layers were not readable from WebFetch).",
        "Registry flag from round 4 (shleifer1997limits used_by lacked AP1) is resolved at 33fd452: references.json used_by now includes AP1 and verify_refs --unit AP1 re-resolved it.",
        "Live verify_refs now succeeds from this sandbox (round 4 could not reach Crossref); the offline and live runs both pass.",
        "Carry-forward: only rows whose subject files are byte-identical to 9c8f3e4 are carried, and every numeric row was recomputed under Python 3.14.8 / numpy 2.4.6 (scripts in /tmp/ap1-r5/L01-L02/recompute).",
        "Judgment call for the orchestrator: the ellipsis characters at the end of quiz prompts (L01 lines 493-544, L02 lines 397-461) are clozes, not omitted content; PASS recorded in banned-phrases row. If the reading is stricter, that row and only that row changes.",
        "Not checked live: the H.10 about.htm and disclaimer.htm were read via WebFetch summaries plus verbatim quoted fragments; the full disclaimer paragraph exceeded the tool's 125-character quote limit.",
    ],
    "summary": summary,
}
out = sys.argv[1]
json.dump(frag, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("rows", summary["rows"], "pass", summary["pass"], "verdict", frag["verdict"])
