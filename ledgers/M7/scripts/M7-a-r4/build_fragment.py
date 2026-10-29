import json, sys
sys.path.insert(0, "/tmp/verifyB4-M7-a/tools")
import ledger  # noqa: E402

P = "PASS"
rows = []
def R(id_, check, loc, status, ev):
    rows.append({"id": id_, "check": check, "location": loc, "status": status, "evidence": ev})

R("M7a-cmd-check_pages", "command", "tools/check_pages.py --unit M7", P,
  "Run on 2657ab5: 'check_pages M7: PASS', exit 0.")
R("M7a-cmd-check_dag", "command", "tools/check_dag.py --all", P,
  "Run on 2657ab5: 'check_dag CF1: PASS', 'check_dag AP1: PASS', 'check_dag M7: PASS', exit 0.")
R("M7a-cmd-run_labs", "command", "tools/run_labs.py --unit M7", P,
  "Run on 2657ab5: 'run_labs M7: PASS (11/11)', exit 0.")
R("M7a-cmd-lab-twins", "command", "tests/labs/M7/lab-M7-L01-1.py, lab-M7-L02-1.py, lab-M7-L03-1.py", P,
  "python -I -W error on each twin: exit 0, empty stderr, 14, 13 and 22 output lines (/tmp/m7v4/a/out-L0{1,2,3}.txt). "
  "ledgers/M7/scripts/M7-a-r4/cmp.py (run with -I): twin code equals the page's data-run block and the page's expected block equals the output, for L01, L02, L03.")
R("M7a-cmd-page_smoke", "command", "tools/page_smoke.py --unit M7 --pages index L01 L02 L03", P,
  "Run on 2657ab5: 'page_smoke M7: PASS', exit 0; lab-M7-L03-1 0.0 s. Pyodide timing beyond this report was not measured.")
R("M7a-cmd-ruff-twins", "command", "ruff check tests/labs/M7 course/modules/M/M7; ruff format --check tests/labs/M7", P,
  "'All checks passed!'; '11 files already formatted'.")
R("M7a-cmd-mypy-twins", "command", "mypy --no-incremental on lab-M7-L01-1.py, L02-1.py, L03-1.py", P,
  "'Success: no issues found in 3 source files', exit 0.")
R("M7a-cmd-verify_refs", "command", "tools/verify_refs.py --unit M7 (live); tools/verify_refs.py --offline", P,
  "Live: '2 of 560 entries, 0 problems', exit 0. Offline: '560 entries, 0 problems', exit 0. "
  "Registry records read: boyd2004convex (Boyd, Vandenberghe; 2004; Cambridge University Press) and stokey1989recursive (Stokey, Lucas, Prescott; 1989; Harvard University Press), both status verified.")

R("M7a-num-L01-counts", "numbers in prose and lab lines", "course/modules/M/M7/L01.html Lab 1 (lines 158-160), expected block and interpretation; E1 (line ~405 area, 'E1 · Why the failing count')", P,
  "Fresh recomputation, ledgers/M7/scripts/M7-a-r4/recheck.py (plain Python, Fractions): 3125 cases per function; Q1 identity 3125, Q2 identity 3125, Q1 chord 3125, Q2 chord 2573, fails 552; 184 negative ordered pairs; 3 x 184 = 552. "
  "Printed block in /tmp/m7v4/a/out-L01.txt matches the page. recheck.py aborts at its sympy import (line 29; sympy is not in .venv and was not installed); every value on the page was recomputed by the printed lines before that point and by hand.")
R("M7a-num-L02-lab", "lab numbers in prose", "L02.html Lab 1 (lines 149-151), E2 (line 388), misconception 2 (line ~330), interpretation paragraph after the lab", P,
  "ledgers/M7/scripts/M7-a-r4/recheck2.py: u = (47/177, 17/177, -3/59), s = 55/177, lambda = 177/55, w = (47/55, 17/55, -9/55), sum 1, Sigma w - lambda 1 = 0, f = 177/110; "
  "output /tmp/m7v4/a/out-L02.txt prints '36 of 36' twice (6 directions x 6 steps = 36). Page wording 'two 36-of-36 lines' matches.")
R("M7a-num-L02-rounding", "rounded displays", "L02.html quiz data-answer and explanation (lambda 3.2182; 0.6667; 0.3333)", P,
  "177/55 = 3.21818...; round to four places 3.2182. 2/3 = 0.66666...; 0.6667. 1/3 = 0.33333...; 0.3333. |3.2182 - 177/55| = 1.8e-5 within the stated tolerance.")
R("M7a-num-L03-grid", "lab grid numbers", "L03.html Lab 1 (lines 156-157), E2 (line 406 area), key results row", P,
  "ledgers/M7/scripts/M7-a-r4/recheck2.py, Fraction over w1 = k/100, k = 0..100 (101 points): minimum -1/2 at w1 = 1 for mu = (3/2, 1/5); -1/4 at w1 = 1/2 for mu = (1, 1). Output /tmp/m7v4/a/out-L03.txt matches.")
R("M7a-num-L03-examples", "worked numbers", "L03.html Examples 4.1 and 4.2, Remark 4.3, M2, M3, E1, E3, P3", P,
  "Example 4.1: grad f(1,0) = (1/2, 4/5), nu = -1/2, lambda2 = 3/10, f = -1/2. Example 4.2: grad (1/2,1/2), w'Sigma w = 3/2, f = -1/4. Remark 4.3: (14/15, -11/30), sum 17/30. "
  "M2: f(3/5,2/5) = -6/25 = -0.24 > -1/4. M3: grad (0, 13/10), f(1/2,1/2) = -1/10. E1: norm sqrt(1/2) = 0.70710678, displayed 0.7071. E3 f = 3/4 - 1 = -1/4. All recomputed in recheck2.py.")
R("M7a-num-hub-placement", "hub placement arithmetic", "course/modules/M/M7/index.html placement paragraph (line ~73-75) and items 7-8", P,
  "7/9 = 77.8 %, 8/9 = 88.9 %; 80 % of 9 = 7.2, so eight of nine is the bar; nine items, two skill checks.")
R("M7a-num-hub-quiz-decimal", "hub decimal", "index.html item 8 (lines 127-129)", P,
  "lambda = 2/3 = 0.6667 to four places; |0.6667 - 2/3| = 3.3e-5 within data-tolerance 0.001.")
R("M7a-hours", "hours arithmetic (pace not judged)", "index.html lines 29, 40-42, 141; data-hours on L01-L08", P,
  "Hub: 77 h lessons + 33 h project = 110 h; 33/110 = 30 %. Lesson hours L01 9, L02 9, L03 10 agree with the lesson meta lines ('9 study hours', '9', '10'). Sum over L01-L08 = 77 (9+9+10+10+10+10+9+10). Pace not judged (architect ruling).")
R("M7a-grades", "grades T/C/not graded", "L01 Prop 1.3, 2.3, 3.2, Lemma 3.1; L02 Thm 2.2, Props 2.4, 3.2, 3.3; L03 Lemma 1.4, 1.5, Thm 2.1; L03 Open item 3.2 (not graded); lab results C", P,
  "Each T result has a proof on its page, read in full. Prop 3.2 (iii) and Theorem 2.2 carry their hypothesis (Assumption 1) in the statement. Lab-derived results (cards c012, c016, c027-c030, c049, c050) are C with basis naming the lab. Open item 3.2 is not graded.")
R("M7a-math-L01", "mathematics, L01", "L01.html Lemma 3.1 (line ~47-52), Prop 1.3 (line ~28-31), Prop 2.3 (line ~40-43), Prop 3.2 (line ~60-69), Ex 3.2a, Ex 3.3, Problems M1-M3, P1-P3, E1-E3, R1-R3", P,
  "Re-derived by hand and recheck.py: Lemma 3.1 identity (expansion, symmetry); Prop 3.2 (i)-(iii) proofs incl. the eigenbasis step x = Ve_i; Ex 3.3 eigenvalues (Q1: 3,1; Q2: 3,-1; Hessians 6,2 and 6,-2); M2 gap 1; M3 gap 6 (= (1/4)*24); P3 gap (1/4)q(v) < 0; R1 (x1^2 + x2^2); R3 conditions 4 >= 0, 3 >= 0; E1 3 x 184 = 552. "
  "P1 solution (line ~211) now reads 'convex on S = R by Proposition 3.2, (ii) implies (i)': the round-3 defect (convexity from Lemma 3.1 without the sign step) is removed. No defect found.")
R("M7a-math-L02", "mathematics, L02", "L02.html Thm 2.2 proof (lines ~34-38), Remark 2.3, Examples 2.5, 2.6, Prop 2.4, Prop 3.2 (lines ~53-64), Prop 3.3, Problems M1-M3, P1-P3, E1-E3, R1-R3", P,
  "Thm 2.2: p.d = -|r|^2 < 0 with g.d = 0; gamma'(0) = d via the implicit-function step; contradiction with local minimality. Ex 2.5: grad h(0) = 0, feasible set forces x >= 0. Ex 2.6: (0,-y) feasible, f = -y^3 < 0, witness (0,-1). Prop 3.2 (a)-(d) re-derived (d: f(w) - f(w*) = 1/2 d'Sigma d). M1 (1/2,1/2); M2 f = 1/3; M3 3/2; P3 f = lambda/2 = 1/(2s); E1 first coordinate 177/55; E3 177/110. "
  "Misconception 1 (line ~82): 'Lab 1 shows the same' is supported by the printed residual line (all zero) and the printed lambda = 177/55 that together give Sigma w* = lambda 1 != 0. No defect found.")
R("M7a-math-L03", "mathematics, L03", "L03.html Lemma 1.4 (line ~34-38), Lemma 1.5 (line ~39-44), Thm 2.1 (line ~46-52), Remark 2.2, Example 2.3 (line ~55-57), Example 3.1, Examples 4.1, 4.2, Remark 4.3, M1-M3, P1-P3, E1-E3, R1-R3", P,
  "Lemma 1.5 identity: theta/2 x'Sx + (1-theta)/2 y'Sy - z'Sz/2 = theta(1-theta)/2 (x-y)'S(x-y), re-expanded. Thm 2.1 proof: lambda_i g_i convex by K3; nu_j h_j affine; phi(x) >= phi(x*) = f(x*) >= f(x). Ex 2.3: f(-1) = -1 < 0 = f(0), f(1) = 1 > 0 = f(0), midpoint -1/8 > -1/2. "
  "Ex 3.1: F = {0}, grad g1(0) = 0, (K1) reads 1 = 0. Ex 4.1 and 4.2 re-derived (see M7a-num-L03-examples). P1 sign step (lambda = -1, g = x^2: midpoint 0 > average -1). R1: 0 is the global maximum of -x^2 and no minimizer exists. No defect found.")
R("M7a-P1-note", "L03 problem P1 scope claim", "L03.html P1 solution (line ~374-377)", P,
  "The round-2 unargued scope claim is absent; the solution states the sign step and the lambda < 0 counterexample.")
R("M7a-lab-L01-claims", "lab claims vs code and output", "L01.html lab hypothesis (line 159), docstring (tests/labs/M7/lab-M7-L01-1.py lines 1-88), expected interpretation (line ~181)", P,
  "Docstring 'four things' matches main(): identity, chord, eigenvalues, explicit example. Printed 'Q1 identity holds in 3125 of 3125 cases', 'Q2 chord ... 2573 of 3125', 'Q2 failures equal 3 times that count: True', midpoint 3/2, chord 1, eigenvalues 6 and 2 (Q1), 6 and -2 (Q2), eigenvalue tests True/False: all match the page text. Grid 'five weights, 3125 cases' matches.")
R("M7a-lab-L02-claims", "lab claims vs code and output", "L02.html lab hypothesis (line ~70), docstring (lab-M7-L02-1.py lines 1-30), interpretation (line ~73) and E2 (line ~388)", P,
  "'six directions and six step sizes' matches directions() (6 entries, each sums to 0) and steps (6 entries). 'Proposition 3.2 ... Proposition 3.3' match the page. The printed 'in 36 of 36 tested cases' lines match the 6 x 6 loop. Residual and objective lines match the page text.")
R("M7a-lab-L03-claims", "lab claims vs code and output", "L03.html lab hypothesis (line 157), docstring (lab-M7-L03-1.py lines 1-20), interpretation (line ~406 E2, line ~305 area)", P,
  "101 grid points (GRID_STEPS = 100) match the output line 'on the 101 grid points'. 'The grid is numerical evidence and not a proof' matches the docstring. Printed: all four KKT conditions hold exactly True; grid minimum -1/2 at w1 = 1 and -1/4 at w1 = 1/2; off-solution residual (-1/2, 1/2); dual residual 3/10. All match.")
R("M7a-L02-example-2.6-local", "'not even a local minimizer' qualifier", "L02.html line 22 and Example 2.6 (line ~43-44)", P,
  "Witnesses (0,-y), y > 0, feasible, arbitrarily close to origin, f = -y^3 < 0 = f(0,0). Local qualifier is correct.")
R("M7a-L03-remark-1.3", "Remark 1.3 example", "L03.html Remark 1.3 (line ~31-32) and Section 4", P,
  "Minimize x^2 subject to -x <= 0: x = 0 active, grad 0, (K1) holds with lambda = 0. Section 4 uses the slack case (Ex 4.2) and the active case with a positive multiplier (Ex 4.1, lambda2 = 3/10).")
R("M7a-L03-P1-concave", "problem P1 concavity claim", "L03.html P1 solution (line ~374-377)", P,
  "'for lambda < 0 the inequality reverses, so lambda g satisfies the concavity inequality'; counterexample g = x^2, lambda = -1: midpoint at (1, -1) is 0, average -1, 0 > -1. Correct.")
R("M7a-L03-boyd-attribution", "attribution of Open item 3.2", "L03.html meta description (line 7), Open item 3.2 (line ~61-62), References (line 543)", P,
  "Round-3 defect fixed: the meta description now says necessity 'is stated as an open item, not proved'. The grep of 'cited' finds only 'This lesson cites no source' (line 543). No locator is claimed.")
R("M7a-L03-constraint-qualification", "constraint qualification defined before use", "L03.html Remark 2.2 (line 117), Theorem 2.1 proof (line ~48-52), Open item 3.2", P,
  "Remark 2.2 defines a constraint qualification inline before the Section 3 reference. The proof of Theorem 2.1 invokes no CQ.")
R("M7a-registry-stokey", "registry key stokey1989recursive", "index.html Core reading (line 176) vs references/references.json", P,
  "Registry authors Stokey, Lucas, Prescott; year 1989; Harvard University Press. The hub lists the three authors and says this page uses that record.")
R("M7a-slater-forward-ref", "Slater condition defined before use", "L03.html Example 3.1 (line 60), Open item 3.2 (line 62), Remark 2.2 (line 117)", P,
  "Slater's condition is defined inline in Example 3.1 (every inequality strictly, every equality) and restated in Open item 3.2 before Section 4 uses no Slater point.")
R("M7a-hub-M1-locator", "M1 locator", "index.html placement item 6 (M1 Lesson 1, Theorem 3.1)", P,
  "course/modules/M/M1/L01.html line 79: 'Theorem 3.1 (negating one quantifier)'. M1 is unchanged between aa3c26c and 2657ab5 (git diff empty).")
R("M7a-dag-concepts", "DAG and concept closure", "index.html, L01.html, L02.html, L03.html (data-concept links and dfn ids)", P,
  "check_dag M7: PASS. dfn ids: def-convex-set, def-convex-function (L01); def-lagrange-multiplier (L02); def-kkt-conditions (L03), each once. Links only to prerequisites (AC1, S0, S2 closure, M1-M3 prose) or to the unit's own earlier lessons. No L04-L08 concept used in L01-L03.")
R("M7a-hub-covariance", "covariance only in disclaimer", "index.html line ~167 (Data status); L01-L03 text", P,
  "'covariance' appears in L01-L03 nowhere; in index.html only in the disclaimer 'estimating a covariance matrix is outside M7', permitted by architect decision B1/Q1.")
R("M7a-r2-hub-eigen-use", "hub prerequisite wording", "index.html line ~65 (Prerequisites)", P,
  "Reads 'The eigenvalue test of Lesson 1 uses eigendecomposition and the spectral theorem, and Lesson 2 uses positive semidefinite matrices for its matrix Sigma', consistent with L01 and L02 uses.")
R("M7a-r2-L01-forward-PD", "no forward reference to Lesson 2", "L01.html canon-breaks (line ~315-320)", P,
  "'positive definite' does not occur in L01.")
R("M7a-hub-seed-claim", "data-status claim", "index.html line 37 (Data meta) and line 167 (Data status); L01 line ~159, L02 line ~150, L03 lines ~116-123", P,
  "Each input is labelled SIMULATED or hand-chosen on its page: L01 (docstring SIMULATED), L02 (docstring SIMULATED, interpretation), L03 (Section 4 'SIMULATED and are not market data').")
R("M7a-hub-prose-scope", "hub scope words", "index.html stretch rung (line ~161)", P,
  "'a case computed in Lesson 2, Problem R3' points to L02 R3 (c^2/(2s), derivative c/s, multiplier at c = 1; one case, labelled). Matches.")
R("M7a-banned-phrases", "banned phrases and process words", "index.html, L01.html, L02.html, L03.html (tags stripped; ledgers/M7/scripts/M7-a-r4/scan.py)", P,
  "scan.py over the four pages: no 'roughly', 'about <number>', 'historically', 'typically', 'usually', 'generally', 'often', 'mostly', ellipsis, TODO, TBD, lorem, 'for brevity', 'details omitted', 'beyond the scope', 'left as an exercise'. 'about' hits are the ordinary word ('Which statement about ...'). 'round' hits are 'rounding' and 'round to four places'. 'verif' hits are 'verify'.")
R("M7a-scope-words", "scope words", "index.html, L01-L03 (scan.py: 160 hits for only, all, always, every, any, same, drives, offsets, raises, as much as)", P,
  "Each 'every' and 'any' is backed by a computation or a named set: 'every ordered pair' (625 x 5 = 3125, recheck.py), 'Q1 passes every case' (3125 of 3125), 'for every feasible w' (P3 proof), 'for any multipliers' (L03 M3, shown), 'every direction' (L02 Prop 3.2 (d)). 'only' in L03 Example 2.3 ('the only hypothesis of Theorem 2.1 that the example breaks') is backed by the hypothesis list of Theorem 2.1 checked item by item; 'only' in L03 R2 is backed by the same list. 'Proposition 3.2 proves global minimality, and only for the budget problem' (L02 line ~78) is a statement of the lesson's scope and is correct.")
R("M7a-cards-L01-L03", "cards of L01-L03 against current lesson text", "course/modules/M/M7/cards.json cards M7-c001 to M7-c033, M7-c036 to M7-c053, M7-c160, M7-c161 (all read)", P,
  "Round-3 defect fixed: c008 now says 'Assuming Assumption 1 ... both are also equivalent to (iii)'; c009 says 'Under Assumption 1, Q1 has eigenvalues 3 and 1 ... so x'Q1x is convex'; c015 says 'Under Assumption 1, Proposition 3.2 (iii) requires every eigenvalue to be non-negative'; c031 says 'Theorem 2.2, under Assumption 1'. "
  "Card numbers and claims agree with their lesson text (c010, c012, c013, c016, c027-c030, c043, c044, c046-c053 re-read). Cards c034, c035 and c045 are absent; they were removed in round 3 (present at 1817191, absent at aa3c26c and 2657ab5). Removal is not a defect: ids need not be contiguous and no remaining card depends on them.")
R("M7a-cards-duplicates", "duplicate scan", "course/modules/M/M7/cards.json (143 cards)", P,
  "Inline Counter over cards.json (143 cards): 0 duplicate ids, 0 duplicate fronts, 0 duplicate backs. Run this round on 2657ab5.")
R("M7a-r2-L01-R1-symmetric", "R1 wording", "L01.html R1 (line ~423-427) and line 46", P,
  "R1 is an instance of the general argument, a one-line proof (x'Qx is a scalar). Wording matches.")
R("M7a-r2-L03-example-2.3-only", "Example 2.3 'only hypothesis' claim", "L03.html Example 2.3 (line ~56)", P,
  "No constraints; f = x^3 differentiable; convexity fails at (-1, 0) with midpoint -1/8 > average -1/2 (recomputed). The other hypotheses hold (differentiability; h_j vacuous).")
R("M7a-r2-L02-proof-uses", "Prop 3.2 proof-uses sentence", "L02.html interpretation paragraph (line ~73)", P,
  "Proof of Prop 3.2 (d) uses 1'd = 0, w*'Sigma d = lambda 1'd = 0 from (c), and d'Sigma d > 0 for d != 0 (PD).")
R("M7a-r2-L03-maximizer-claim", "KKT point can be minimizer, maximizer or neither", "L03.html misconception 1 (line ~85) with Example 2.3 (line ~56) and Problem R1 (line ~134-136)", P,
  "Round-3 defect fixed. Minimizer: f = (x^2-1)^2, KKT points x = +-1 are global minimizers with value 0. Maximizer: x = 0 is a local maximizer of (x^2-1)^2 and R1 gives a global maximizer (f = -x^2). Neither: Example 2.3 now states that x^3 at 0 is not a minimizer (f(-1) = -1 < 0) and not a maximizer (f(1) = 1 > 0), which is the witness for 'neither'.")
R("M7a-r3-hub-placement-rung", "hub placement item 7-8 and project rung references", "index.html items 7-8 (lines 118, 127) vs project.html Rung 1 (Lab 1, three assets, third weight held at zero) and Rung 2 (Lab 2, same problem with stationarity line blanked)", P,
  "Round-3 defect fixed. Item 7 'used in rungs 1 and 2' matches project.html (Rung 1 worked example; Rung 2 completion with the stationarity line blanked, lines 15-18, 24-25, 120). Item 8 says the two-asset value '(Sigma = diag(1,2)) is not an output of rung 2, which has three assets and bounds (project page, Lab 2)': project.html Lab 2 is a three-asset long-only problem (lines 25, 120).")
R("M7a-r3-L03-feasible-set", "terms defined at first appearance (plan 8.2 rule 5)", "L03.html why-it-matters (line 20) and Definition 1.1 (line 24)", P,
  "Round-3 defect fixed: the first appearance of 'feasible set' (line 20) reads 'the set of points that satisfy every constraint (the feasible set, Definition 1.1)', which states the definition at first use and points to the formal Definition 1.1. Accepted as a definition at first appearance.")
R("M7a-r4-L01-prop-remarks", "round-4 wording: L01 Prop 1.3 remark and Prop 2.3 remark", "L01.html lines 76 and 102", P,
  "Line 76: 'the feasible set, the set of points that satisfy every constraint, is their intersection' is correct. Line 102: 'Lesson 3 uses the convexity of each constraint function g_i directly, in Theorem 2.1, and does not use this set-level result' is correct: the proof of Theorem 2.1 (L03) uses convexity of g_i and not Proposition 2.3.")
R("M7a-r4-L02-changes", "round-4 wording: L02 Example 2.6 reference, Remark 2.3, misconceptions, E2, skill-check wording", "L02.html line 22, line 40, lines 82-86, 120-123", P,
  "Line 22: Example 2.6 'a point that satisfies the Lagrange condition ... and is not even a local minimizer' is correct. Line 40: the rest of the Theorem 2.2 argument forces the multiple. E2 (line 120): 'two 36-of-36 lines' matches the output. All re-derived.")
R("M7a-r4-L03-changes", "round-4 wording: L03 meta, why-it-matters, Theorem 2.1 hypothesis h_j affine, Example 2.3 maximizer clause, misconception 1", "L03.html line 7, line 20, line 47 (Thm 2.1), line 56 (Ex 2.3), line 85", P,
  "Theorem 2.1 now includes 'each h_j is affine', which the proof uses (nu_j h_j convex). Example 2.3 now says 0 is not a maximizer (f(1) = 1 > 0 = f(0)), correct. Meta and why-it-matters match the content.")
R("M7a-r4-hub-changes", "round-4 wording: hub items 7-8", "index.html lines 118-129", P,
  "Item 7 explanation and item 8 wording match project.html (see M7a-r3-hub-placement-rung). Item 8 computed value 2/3 = 0.6667 is re-derived.")

fragment = {
  "unit": "M7",
  "slice": "M7-a",
  "round": 4,
  "verifier": "independent verifier round 4, slice M7-a (hub index.html, L01-L03 and lab twins L01-1 to L03-1); did not build M7; shares no context with the builders",
  "pin": "2657ab5",
  "base": "aa3c26c (round-3 pin). Delta computed with git diff aa3c26c 2657ab5 on the slice files: changed index.html, L01.html, L02.html, L03.html, cards.json (all re-verified). Lab twins L01-1, L02-1, L03-1 unchanged (re-run). tests/labs/M7/L07-1 and project-3 changed but are outside this slice.",
  "previous_ledger": "/tmp/fanout-frags/B-M7-a.round3.json (context only; no PASS row carried, because every slice file that a row cites changed or the row was re-run)",
  "checkout": "/tmp/verifyB4-M7-a (detached at 2657ab5)",
  "scratch": "/tmp/m7v4/a",
  "verified_at": "2026-10-28T12:00:00+00:00",
  "verdict": "PASS",
  "registry_flags": [],
  "freshness_flags": [],
  "notes": [
    "Scripts: ledgers/M7/scripts/M7-a-r4/cmp.py, recheck.py, recheck2.py, scan.py (round-3 scripts re-pointed to this checkout), build_fragment.py (writes this fragment).",
    "recheck.py aborts at line 29 (import sympy; sympy is not in .venv and was not installed, per the toolchain policy). The values it prints before that line were used; the rest was recomputed in recheck2.py and by hand.",
    "Mutation testing does not apply to lab twins (architect ruling). No project mutants in this slice.",
    "Not checked: the project slice (grader, starter, reference, test_project, mutants), L04-L08 pages and cards (only the hub references to them), pace of hours (architect ruling), Pyodide timing beyond page_smoke's report, and any live fetch of Boyd & Vandenberghe or Stokey, Lucas & Prescott (no locator is claimed, so none was needed; no access to the publishers was attempted)."
  ],
  "mutants": [],
  "summary": "M7-a round 4: PASS. All 6 round-3 non-PASS rows (M7a-math-L01, M7a-L03-boyd-attribution, M7a-r3-L03-feasible-set, M7a-cards-L01-L03, M7a-r2-L03-maximizer-claim, M7a-r3-hub-placement-rung) are fixed and re-verified. No new defect found in the round-4 delta. Counts: see rows."
}
fragment["rows"] = rows
out = "/tmp/verifyB4-M7-a/ledgers/M7/M7-a.json"
with open(out, "w", encoding="utf-8") as f:
    json.dump(fragment, f, ensure_ascii=False, indent=2)
print(len(rows), "rows; non-PASS:", [r["id"] for r in rows if r["status"] != "PASS"])
