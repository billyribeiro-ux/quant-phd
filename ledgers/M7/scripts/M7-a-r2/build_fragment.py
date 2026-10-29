"""Write the round-2 fragment for M7 slice a (hub, L01-L03, lab twins) and validate it with tools/ledger.py."""
import json
import sys
from pathlib import Path

sys.path.insert(0, "tools")
import ledger  # noqa: E402

ROOT = Path(sys.argv[1])
P = "PASS"
F = "FAIL"
rows = []


def row(rid, check, location, status, evidence, fix=None):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != P:
        r["fix"] = fix
    rows.append(r)


# ---- commands
row("M7a-cmd-check_pages", "2.9-structure", "tools/check_pages.py --unit M7", P,
    "Run this round: 'check_pages M7: PASS', exit 0.")
row("M7a-cmd-check_dag", "DAG", "tools/check_dag.py --all", P,
    "Run this round: exit 0; output line 'check_dag M7: PASS'.")
row("M7a-cmd-run_labs", "2.5-labs", "tools/run_labs.py --unit M7", P,
    "Run this round: 'run_labs M7: PASS (11/11)', exit 0.")
row("M7a-cmd-lab-twins", "2.5-labs", "tests/labs/M7/lab-M7-L01-1.py, lab-M7-L02-1.py, lab-M7-L03-1.py", P,
    "python -I -W error on each twin: exit 0; outputs 14, 13 and 22 lines (scratch /tmp/m7-v/a/out-L01-1.txt, out-L02-1.txt, out-L03-1.txt). Each output equals the page's embedded expected block (L01.html lines 289-302, L02.html lines 274-286, L03.html lines 287-308), compared line by line.")
row("M7a-cmd-page_smoke", "2.5-labs", "tools/page_smoke.py --unit M7 --pages index L01 L02 L03", P,
    "Run this round: 'page_smoke M7: PASS'; boot 1.1 s; lab runtimes 0.6 s (L01), 0.0 s (L02), 0.0 s (L03). Pyodide timing beyond this report not measured.")
row("M7a-cmd-ruff-twins", "2.5-labs", "tests/labs/M7 and course/modules/M/M7 (ruff); three slice twins (format)", P,
    "ruff check tests/labs/M7 course/modules/M/M7: 'All checks passed!'. ruff format --check on the three slice twins: '3 files already formatted'.")
row("M7a-cmd-mypy-twins", "2.5-labs", "tests/labs/M7/lab-M7-L01-1.py, lab-M7-L02-1.py, lab-M7-L03-1.py", P,
    "mypy --no-incremental on the three twins: 'Success: no issues found in 3 source files', exit 0.")
row("M7a-cmd-verify_refs", "2.1-citations", "tools/verify_refs.py --unit M7 (live); tools/verify_refs.py --offline", P,
    "Live: 'live re-verification of M7: 2 of 560 entries, 0 problems', exit 0. Offline: 'offline integrity: 560 entries, 0 problems', exit 0.")

# ---- numbers
row("M7a-num-L01-counts", "2.2-numbers", "course/modules/M/M7/L01.html Lab 1 printed block (lines 289-302) and paragraph line 303", P,
    "Independent recomputation (ledgers/M7/scripts/M7-a-r2/recheck_L01_L03_indep.py, run -I): 3125 cases; Q1 chord 3125; Q2 chord 2573; 184 negative ordered pairs; 3 x 184 = 552 = 3125 - 2573; example midpoint 3/2, chord 1, gap -1/2; discriminants 16 and 64 give eigenvalues 6, 2 and 6, -2. All match the printed block and the interpretation paragraph.")
row("M7a-num-L02-lab", "2.2-numbers", "course/modules/M/M7/L02.html Lab 1 printed block (lines 274-286), E1 (line 379), misconception (line 306)", P,
    "Independent Cramer-rule recomputation (recheck_L01_L03_indep.py): Sigma = [[4,2,5],[2,7,4],[5,4,14]] from seed-1 entries [1,2,3,1,-1,2,-1,-1,0]; s = 55/177; lambda = 177/55; w = (47,17,-9)/55; budget exact; Sigma w - lambda 1 = 0; f = 177/110 = lambda/2; 36 of 36 identity and 36 of 36 non-negativity. E1 first coordinate 4(47/55)+2(17/55)+5(-9/55) = 177/55 (page line 379 arithmetic correct).")
row("M7a-num-L02-rounding", "2.2-numbers", "course/modules/M/M7/L02.html quiz item data-answer 3.2182 (line 504) and explain line 507", P,
    "177/55 = 3.2181818...; to four places 3.2182 (python round(float(177/55), 4) = 3.2182); data-tolerance 0.00005 accepts 3.2182 (|3.2182 - 3.2181818| = 1.8e-5). The previous round's rounding defect (3.2181) is gone.")
row("M7a-num-L03-grid", "2.2-numbers", "course/modules/M/M7/L03.html Lab 1 printed block (lines 287-308) and interpretation (line 309)", P,
    "Recomputed with Fraction over k/100, k = 0..100 (101 points): active grid minimum -1/2 at w1 = 1; inactive -1/4 at w1 = 1/2; off-solution stationarity (-1/2, 1/2); flipped-sign dual residual 3/10. All match the printed lines.")
row("M7a-num-L03-examples", "2.2-numbers", "L03.html Examples 4.1, 4.2, Remark 4.3, Problems M2, M3, P3, E1, E3, Example 2.3, and L02.html Problems M2, M3, P3, R3", P,
    "Example 4.1: grad = (1/2, 4/5), lambda = (0, 3/10), nu = -1/2, p* = -1/2 (recomputed). Example 4.2: grad = (1/2,1/2), w'Sigma w = 3/2, f = -1/4. Remark 4.3: (14/15, -11/30), weight sum 17/30. M2: f(3/5,2/5) = -6/25 (= -0.24 > -0.25). M3: grad (0, 13/10), f(1/2,1/2) = -1/10. P3: f(w) >= -1/2 + (3/10) w2 checked at w2 = 0, 1/3, 1/2, 1. E1 norm 0.7071. Example 2.3 midpoint -1/8 vs average -1/2. L02 M2 2/3, 1/3, 1/3; M3 increase 3/2; P3 177/110.")
row("M7a-num-hub-placement", "2.2-numbers", "course/modules/M/M7/index.html placement paragraph (line 73)", P,
    "7/9 = 77.8 percent and 8/9 = 88.9 percent (recomputed). 80 percent of 9 items is 7.2, so eight correct is the bar. Nine items counted in lines 75-134, two marked data-skill (lines 118, 127).")
row("M7a-num-hub-quiz-decimal", "2.2-numbers", "course/modules/M/M7/index.html skill check rung 2 (line 127-129)", P,
    "lambda = 2/3 = 0.6667 to four places; data-answer 0.6667, tolerance 0.001. The previous round's decimal defect is gone.")

# ---- hours, grades, math
row("M7a-hours", "hours", "index.html lines 29, 42, 141, 143-145; data-hours on L01-L08", P,
    "Hub split 77 lesson + 33 project = 110 (data-hours-lessons=77, data-hours-project=33; 33/110 = 30 percent; bar widths 70/30). Lesson data-hours: L01 9, L02 9, L03 10, L04 10, L05 10, L06 10, L07 9, L08 10; sum 77. Card labels L01 9 h, L02 9 h, L03 10 h agree. Arithmetic only; pace not assessed.")
row("M7a-grades", "2.3-grades", "L01.html Prop 1.3, 2.3, 3.2, Lemma 3.1 (T); L02.html Thm 2.2, Props 2.4, 3.2, 3.3 (T); L03.html Lemma 1.4, 1.5, Thm 2.1 (T); L03.html Open item 3.2 (not graded); L03.html key-results row 463 (C)", P,
    "Each T claim has a proof on the page that was read in full (L01 lines 66-143; L02 lines 67-131; L03 lines 77-113). Theorem 2.2's implicit-function-theorem step is an M2 result used as stated and is disclosed as such (L02 line 78). Lab results are graded C where they are stated (L02 card M7-c027 etc.). Open item 3.2 is explicitly ungraded.")
row("M7a-math-L01", "2.4-math", "L01.html sections 1-3, Props 1.3, 2.3, 3.2, Lemma 3.1, Example 3.2a, 3.3, Problems M1-M3, P1-P3, E1-E3, R1-R3", P,
    "Lemma 3.1 algebra re-derived: lambda q(x) + (1-lambda) q(y) - q(z) = lambda(1-lambda)(q(x)+q(y)-2x'Qy) = lambda(1-lambda)(x-y)'Q(x-y). Prop 3.2 (i)-(iii) proofs re-read (spectral step, bijection z = V'x). Example 3.3 eigenvectors checked. M3 gap 6 = (1/4)*24. P1 witnesses 2, -2 with midpoint 0. R3 conditions (4 >= 0, 3 >= 0). M1 disk/circle witnesses. Union-of-disks witness: midpoint of (-2,0),(2,0) is (0,0), at distance 3 from both centres.")
row("M7a-math-L02", "2.4-math", "L02.html sections 1-3, Thm 2.2 proof, Examples 2.5, 2.6, Props 2.4, 3.2, 3.3, Problems M1-M3, P1-P3, E1-E3, R1-R3", P,
    "Thm 2.2 proof (lines 75-79): d = -r, p.d = -|r|^2 < 0, gamma'(0) = d via the IFT gradient, contradiction with local minimality; re-read. Example 2.5: h = y^2 - x^3, feasible set forces x >= 0. Prop 3.2 (a)-(d): s = u'Sigma u > 0, lambda w* identities, f(w) - f(w*) = (1/2) d'Sigma d. Prop 3.3 identity re-derived. Problems re-derived (e.g. M2 f = 1/3, M3 increase 3/2 = (1/2)(1+2), P3 f = lambda/2).")
row("M7a-math-L03", "2.4-math", "L03.html Lemma 1.4, Lemma 1.5, Thm 2.1, Examples 2.3, 3.1, 4.1, 4.2, Remark 4.3, Problems M1-M3, P2, P3, E1-E3, R2, R3", P,
    "Lemma 1.4 limit step re-read (lines 84-86). Lemma 1.5 identity re-expanded: theta/2 x'Sx + (1-theta)/2 y'Sy - z'Sz/2 = theta(1-theta)/2 (x-y)'S(x-y). Thm 2.1: phi = L convex (lambda_i >= 0 used for lambda_i g_i), phi(x*) = f(x*) by K4, K2. Example 3.1 (K1) reads 1 = 0. P2 identity (x-y)^2. Problem M1 KKT point x = y = 1/2, lambda = 1. R1 (maximizer) and R2 checked.")
row("M7a-P1-note", "2.4-math", "L03.html Problem P1 (line 381)", P,
    "Note only: the rest of the P1 solution (convexity of lambda g for lambda >= 0) is correct; the failing sentence is in row M7a-L03-P1-concave.")

# ---- lab claims
row("M7a-lab-L01-claims", "2.5-labs", "L01.html lab hypothesis (line 154), docstring (lines 155-171), interpretation (line 303)", P,
    "Hypothesis predictions match the printed output: identity 3125 of 3125 (both Q); Q1 chord 3125 of 3125; Q2 chord fails (2573 of 3125); count 3 x 184 = 552 matches the failure count. Docstring: 'four things' listed match the code (cases(): 625 ordered pairs x 5 weights); 'Proposition 3.2 of the lesson' is L01 Prop 3.2 (line 129). Grid-not-proof statement matches the interpretation.")
row("M7a-lab-L02-claims", "2.5-labs", "L02.html lab hypothesis (line 145), docstring (lines 147-165), interpretation (line 287)", P,
    "'six directions and six step sizes' matches directions() (6 entries) and steps (6 entries). 'Proposition 3.2 gives the minimizer under PD' and 'Proposition 3.3 shows A'A + I PD for every real square A' match L02 Props 3.2 and 3.3. 'The matrix is simulated' matches the SIMULATED docstring. The printed lines match the interpretation (177/55, 177/110, 36 of 36).")
row("M7a-lab-L03-claims", "2.5-labs", "L03.html lab hypothesis (line 161), docstring (lines 162-175), interpretation (line 309)", P,
    "Grid of 101 points (GRID_STEPS = 100) matches. 'The grid is numerical evidence and not a proof' matches the docstring and the interpretation. Hypothesis predictions (-1/2 at w1 = 1; -1/4 at w1 = 1/2; stationarity (-1/2, 1/2); dual residual 3/10) match the printed lines (287-308).")

# ---- prose
row("M7a-L02-example-2.6-local", "2.4-math", "L02.html line 55 and Example 2.6 (line 94)", P,
    "f = y^3, h = x; feasible points (0, -y) for y > 0 give f = -y^3 < 0 = f(0,0) and approach the origin, so the origin is not a local minimizer. The text no longer says 'not a minimizer' without the local qualifier. The previous round's defect is fixed.")
row("M7a-L03-remark-1.3", "2.4-math", "L03.html Remark 1.3 (line 74) and Section 4 (Examples 4.1, 4.2)", P,
    "Example x^2 subject to -x <= 0: x = 0 is active, the gradient of x^2 vanishes there, (K1) holds with lambda = 0. Section 4 uses the slack case (Example 4.2) and the active case with positive multiplier (Example 4.1, lambda_2 = 3/10). The previous defect is fixed.")
row("M7a-L03-P1-concave", "2.4-math", "L03.html Problem P1 solution (line 381)", F,
    "The sentence 'It is convex only when g is affine' is asserted without an argument, and 'only' is a scope word. The claim is true for lambda < 0 (lambda g is concave; it is convex exactly when lambda g is affine, i.e. when g is affine), but the page gives no argument for the 'only when' direction.",
    "Either prove it (for lambda < 0, lambda g convex and concave forces equality in the chord inequality for every pair, so lambda g and hence g is affine), or delete 'It is convex only when g is affine' and keep the concavity sentence.")
row("M7a-L03-boyd-attribution", "2.1-citations", "L03.html Sketch (lines 139-140), References (line 547); index.html line 176; registry boyd2004convex", P,
    "No locator is given anywhere; the sketch states that no source was read and the grade is C. The registry entry boyd2004convex (references/references.json) reads Boyd & Vandenberghe, Convex Optimization, Cambridge University Press, 2004, matching the page's bibliographic string. No passage was fetched (not attempted, so no claim of access is made).")
row("M7a-L03-constraint-qualification", "2.4-math", "L03.html Remark 2.2 (line 118), Theorem 2.1 proof (lines 109-113)", P,
    "The constraint qualification is defined inline before use in the remark. The proof of Theorem 2.1 invokes no CQ (only convexity, affineness, K1 to K4), as the remark says.")
row("M7a-hub-covariance", "DAG", "index.html line 167 (the Data status sentence); L01-L03 text", P,
    "'covariance' appears in L01-L03 only in index.html line 167, 'estimating a covariance matrix is outside M7', the disclaimer sentence permitted by the B1 architect decision. 'variance' appears in prose only ('minimum-variance', 'portfolio variance', L01 line 51), which plan section 8.2(5) allows as undeclared prose. No link.")
row("M7a-hub-seed-claim", "2.9-structure", "index.html line 37 (Data meta) and line 167 (Data status)", F,
    "The sentence 'each [input] is labelled SIMULATED on the page that uses it' is true for L01 (docstring line 160), L02 (line 152) and L03 (line 165), but L05.html contains no 'SIMULATED' label (grep count 0); its lab docstring says 'Inputs are small hand-chosen integers, not data' (tests/labs/M7/lab-M7-L05-1.py line 3; L05.html lines 183 and 186). The hub sentence is false as written for L05.",
    "Reword the hub sentence to 'each input is labelled SIMULATED or hand-chosen on the page that uses it', or add a SIMULATED label to L05 and then re-check the L05 row.")
row("M7a-hub-prose-scope", "2.9-structure", "index.html stretch rung (line 161)", P,
    "'a case computed in Lesson 2, Problem R3' points to L02 R3 (lines 415-419), which computes the minimum value c^2/(2s), its derivative c/s, and the multiplier at c = 1. The 'parametric frontier' example is prose only, not claimed as computed.")
row("M7a-banned-phrases", "2.9-structure", "index.html, L01.html, L02.html, L03.html (tags stripped)", P,
    "Scanner ledgers/M7/scripts/M7-a-r2/scan_text.py for roughly, about, historically, typically, usually, generally, often, mostly, ellipsis, etc., in learner text. Hits: 'about 0.6667' and 'about 0.3333' (L02 lines 465, 470), each with the exact fraction 2/3 or 1/3 in the same sentence (computation shown). The '...' hits are inside the lab code and its printed output ('{-2, ..., 2}'). 'in general' (L03 line 324) is a scope limit, not a hedge. No process words (builder, verifier, round, unit report) in learner text.")
row("M7a-scope-words", "2.9-structure", "index.html, L01.html, L02.html, L03.html scope words (only, all, always, every, any, same, drives, offsets, raises)", P,
    "Each 'every' / 'any' / 'all' hit is backed on the page: L01 'every ordered pair' (625 x 5 cases computed), 'Q1 passes every case' (3125 of 3125), 'one eigenvalue test decides convexity on the whole space' (Prop 3.2 proved); L02 'every direction' (Prop 3.2 (d) proof); L03 'every constraint' (K4 definition), 'for every x in F' (Thm 2.1 proof). The 'only' in L03 Example 2.3 is row M7a-r2-L03-example-2.3-only. The 'only when' in P1 is row M7a-L03-P1-concave (FAIL).")
row("M7a-dag-concepts", "DAG", "index.html, L01.html, L02.html, L03.html (dfn ids and data-concept links); check_dag", P,
    "check_dag M7: PASS. dfn ids in the slice: def-convex-set, def-convex-function (L01); def-lagrange-multiplier (L02); def-kkt-conditions (L03), each once. Links are to M1/M2/M3 closure concepts (gradient, hessian, implicit-function-theorem, positive-semidefinite-matrix, eigendecomposition, spectral-theorem) and to L01/L02 definitions only. No link to M4, M5, CS2, AP2, M8 or FI1 concepts. Undeclared prose 'variance' allowed (plan 8.2(5)).")
row("M7a-cards-L01-L03", "2.7-cards", "course/modules/M/M7/cards.json, cards M7-c001 to M7-c055 and M7-c160, M7-c161 (L01 16, L02 19, L03 21 cards)", P,
    "All 56 cards read against their lesson text this round. Numbers on the cards (552, 184, 2573, -1/2, 177/55, (47,17,-9)/55, 177/110, 36 of 36, 2/3, 1/3, -1/4, -9/55, 14/15, -11/30, 17/30, -1/8 vs -1/2) appear in the lesson text or the printed output. Grades match: C on lab-derived cards (c012, c016, c027, c028, c030, c049, c050), T on proved claims. Card M7-c011 states the symmetric-part fact and cites R1 as in the lesson (the R1 example issue is row M7a-r2-L01-R1-symmetric).")
row("M7a-cards-duplicates", "2.7-cards", "course/modules/M/M7/cards.json (all 147 cards)", P,
    "ledgers/M7/scripts/M7-a-r2/cards_dupes.py: 147 cards, no duplicate ids, fronts or backs. Id gap (c045, c056 to c159 unused) is cosmetic and not a defect.")
row("M7a-hub-M1-locator", "2.1-citations", "index.html placement item 5 (line 106): 'M1 Lesson 1, Theorem 3.1'", P,
    "course/modules/M/M1/L01.html line 79 is Theorem 3.1 (negation of a quantified statement, lines 89 and 100-101). The locator matches.")
row("M7a-registry-stokey", "2.1-citations", "index.html Core reading (line 176) vs references/references.json key stokey1989recursive", F,
    "The page writes 'Stokey and Lucas, Recursive Methods in Economic Dynamics (1989)'. The registry entry (verified via Crossref) lists three authors: Stokey, Lucas and Prescott (year 1989, Harvard University Press, title 'Recursive Methods in Economic Dynamics'). The page's bibliographic string omits Prescott and is not the registry's record. The previous round passed this row without comparing authors.",
    "Use the registry author list (Stokey, Lucas and Prescott) or cite only the registry key, as line 176 itself says lesson pages do.")
row("M7a-slater-forward-ref", "DAG", "L03.html Example 3.1 (line 130) and Remark 2.2 (line 118)", P,
    "Remark 2.2 points forward to Section 3 for Slater's condition, which is defined in Open item 3.2 (line 134). Example 3.1 says 'stated again in Open item 3.2'. The text no longer refers to Lesson 4. No link to a later lesson.")

# ---- new defects found this round
row("M7a-r2-hub-eigen-use", "DAG", "index.html line 65 (Prerequisites bullet)", F,
    "The hub says 'the eigenvalue test of Lesson 1 and the positive definiteness of the symmetric matrix Sigma in Lesson 2 use them' (positive semidefinite matrices, eigendecomposition, spectral theorem). L02.html uses no eigendecomposition or spectral theorem: grep finds neither term in L02, and its only M3 reference is 'positive semidefinite matrices' in the Uses line (line 37).",
    "Write 'use positive semidefinite matrices' for Lesson 2 and keep eigendecomposition and the spectral theorem for Lesson 1.")
row("M7a-r2-L01-R1-symmetric", "2.4-math", "L01.html line 106 ('Problem R1 shows this'); R1 (lines 417-421)", F,
    "The general claim (a non-symmetric Q gives the same quadratic form as (Q+Q')/2) is one line: x'Qx is a scalar, so it equals its transpose x'Q'x. R1 only checks one matrix, Q = [[1,1],[-1,1]], so 'R1 shows this' overstates the evidence. Card M7-c011 cites R1 in the same way.",
    "State the transposition argument on the page (or in R1's solution) and say R1 is an instance of it.")
row("M7a-r2-L01-forward-PD", "DAG", "L01.html line 312 (Canon breaks, third item)", F,
    "The sentence 'Proposition 3.2 of Lesson 2 supplies it for the minimum-variance problem, under positive definiteness' uses 'positive definiteness' before it is defined (defined in L02.html line 109). The term is not in L01's introduced concepts and not in the M3 closure list.",
    "Say 'under the positive definiteness defined in Lesson 2' or drop the forward reference.")
row("M7a-r2-L03-maximizer-claim", "2.4-math", "L03.html line 333 ('Without convexity, a KKT point can be a minimizer, a maximizer or neither')", F,
    "Maximizer: R1 (lines 428-432) shows x = 0 is a KKT point of -x^2 that is the global maximum. Neither: Example 2.3 (x^3, x = 0 is neither a minimizer nor a maximizer). Minimizer without convexity: no example on the page. The clause 'without convexity ... a minimizer' has no witness; the only minimizers shown (Examples 4.1 and 4.2, Problem M1) are for convex problems.",
    "Add a witness: f(x) = (x^2 - 1)^2 with no constraints is not convex, has KKT points x = -1 and x = 1 (f' = 0), and both are global minimizers (value 0).")
row("M7a-r2-L03-example-2.3-only", "2.4-math", "L03.html Example 2.3 (line 123): 'the only hypothesis of Theorem 2.1 that the example breaks'", P,
    "The example has no constraints, so the g_i and h_j hypotheses are vacuous; f = x^3 is differentiable (f' = 3x^2); convexity fails at (-1, 0) with midpoint -1/8 > average -1/2 (recomputed). The 'only' is therefore backed.")
row("M7a-r2-L02-proof-uses", "2.4-math", "L02.html line 287 (interpretation): 'its proof uses only the budget and d'Sigma d'", P,
    "The proof of Prop 3.2 (d) (lines 128-131) uses the budget (1'd = 0), the identity w*'Sigma d = lambda 1'd = 0 from (c), and d'Sigma d >= 0 with equality only at d = 0. The phrase is a fair summary of the quantities used; no hypothesis is hidden.")

# checks of this round's names
for r in rows:
    if r["status"] != P:
        assert r.get("fix"), r["id"]

frag = {
    "unit": "M7",
    "slice": "M7-a",
    "round": 2,
    "verifier": "independent verifier round 2, slice M7-a (hub index.html, L01-L03 and lab twins L01-1 to L03-1); did not build M7; shares no context with the builders",
    "pin": "1817191",
    "base": "c11ae01 (round-1 pin; delta computed with git diff c11ae01 1817191 on the slice files)",
    "previous_ledger": "/tmp/fanout-frags/B-M7-a.round1.json (context only; no round-1 PASS row carried: every slice file that the round-1 row cited changed, so every row was re-verified)",
    "checkout": "/tmp/verifyB2-M7-a (detached at 1817191; .venv symlink to /Users/billyribeiro/dev/quant-phd/.venv)",
    "scratch": "/tmp/m7-v/a",
    "verified_at": "2026-10-28T12:00:00+00:00",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [
        "index.html line 176: author list 'Stokey and Lucas' omits Prescott, who is in references/references.json key stokey1989recursive (row M7a-registry-stokey)."
    ],
    "freshness_flags": [],
    "notes": [
        "The brief names pin b4590f6 and the round-1 pin was c11ae01; this round's checkout is 1817191 as the task statement says, and HEAD was confirmed as 1817191. The brief's b4590f6 is not used.",
        "Changed since c11ae01 in this slice: course/modules/M/M7/index.html, L01.html, L02.html, L03.html, cards.json, tests/labs/M7/lab-M7-L02-1.py. Unchanged: tests/labs/M7/lab-M7-L01-1.py, lab-M7-L03-1.py. Shared tooling (tools/, references/, curriculum/, BUILDER_RULES, VERIFIER_RULES) shows no change in the git diff for this slice.",
        "Scripts backing numeric and text rows: ledgers/M7/scripts/M7-a-r2/recheck_L01_L03_indep.py (run -I from the checkout), scan_text.py, cards_dupes.py, build_fragment.py. Outputs in /tmp/m7-v/a/.",
        "Not checked: the project slice (grader, starter, reference, test_project, mutants), L04-L08 pages and cards, the project.html rung-1 claim cited by the placement explanation (index line 124), any Pyodide timing beyond page_smoke's report, and live fetches of Boyd & Vandenberghe or Stokey, Lucas & Prescott (no locator is claimed, so no fetch was needed; none was attempted).",
        "Mutant testing is not applicable to lab twins (architect ruling); the project mutants belong to the project slice.",
    ],
}

problems = ledger.validate(frag, "M7-a")
out = ROOT / "ledgers/M7/M7-a.json"
out.write_text(json.dumps(frag, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
counts = {"rows": len(rows), "pass": sum(r["status"] == P for r in rows), "fail": sum(r["status"] == F for r in rows)}
print("validate:", problems or "valid", counts)
