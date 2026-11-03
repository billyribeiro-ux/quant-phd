"""Builds ledgers/M7/M7-e.json (round 2, slice e) from the per-card reading recorded below.

Each card row cites the lesson extract line numbers (extract_text.py output, regenerate with
`python3 -I ledgers/M7/scripts/M7-e-r2/extract_text.py course/modules/M/M7/LXX.html /tmp/m7e-r2/LXX.txt`).
Numbers are backed by verify_numbers_r2.py, verify_l07_l08_r2.py, scan_cards_r2.py and card_checks_r2.py,
and by the lab-twin outputs in labout/.
Usage: python3 -I build_fragment_r2.py <checkout-root>
"""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

root = Path(sys.argv[1])
CARDS = json.loads((root / "course/modules/M/M7/cards.json").read_text(encoding="utf-8"))
by_id = {c["id"]: c for c in CARDS}

# id -> (lesson locator, evidence). Evidence states the match checked for that card.
E = {
 "001": ("L01 0017", "Definition 1.1 wording (convex set, every lambda in [0,1], segment) matches the card; T."),
 "002": ("L01 0028-0030", "Definition 2.1 (convex function on a stated convex S) matches; the 'relative to S' sentence is line 0030."),
 "003": ("L01 0019", "Example 1.2 disk: triangle-inequality chain and bound 1 match the card text; T."),
 "004": ("L01 0022-0024", "Proposition 1.3: nonempty family, each S_i convex, intersection convex; proof lines 0024 match."),
 "005": ("L01 0034-0036", "Proposition 2.3 hypotheses (S convex, f convex on S, c real) and conclusion match lines 0034, 0036."),
 "006": ("L01 0041-0048", "Lemma 3.1 identity for symmetric Q and every real lambda; no restriction on lambda (line 0048)."),
 "007": ("L01 0050", "Example 3.2a: gradient 2Qx, Hessian constant 2Q (line 0050)."),
 "008": ("L01 0054-0062", "Proposition 3.2 (i),(ii) equivalent; (iii) under Assumption 1; step (ii)->(iii) uses spectral theorem (0062)."),
 "009": ("L01 0066", "Example 3.3: eigenvalues of Q1 are 3 and 1, eigenvectors (1,1),(1,-1) (line 0066)."),
 "010": ("L01 0172-0174", "Gap -1/2 for Q2 at x=(1,0), y=(0,1), lambda=1/2 via Lemma 3.1 with (1,-1)Q2(1,-1)'=-2 (line 0174). Derived on page, so T is correct; the lab-printed midpoint/chord values were removed from this card."),
 "011": ("L01 0039, 0048, 0130", "Symmetry needed for y'Qx=x'Qy in Lemma 3.1 (line 0048); symmetric part argument (line 0039); Problem R1 (line 0130)."),
 "012": ("L01 0070-0071", "Lab 1 prints 'Q2 chord inequality holds in 2573 of 3125 cases' (labout/L01.out). 3125-2573=552 cases fail. Card basis is Lab 1, but the lesson labels the Q1/Q2 inputs SIMULATED (lab header line 0069), so the basis lacks the label the page carries."),
 "013": ("L01 0172-0174, 0192", "Refutation logic: one failing triple refutes convexity on the set (line 0192). Gap -1/2 for Q2 at the example points via Lemma 3.1 (line 0174) matches the card's 'chord minus midpoint'. Derived, T."),
 "014": ("L01 0079-0080", "Misconception 1: closed disk has a curved boundary and is convex; circle is not (Example 1.2). Matches."),
 "015": ("L01 0081-0082, 0112", "Misconception 2: Q2 diagonal entries 1,1 positive yet not convex; P3 negative eigenvalue refutes convexity (line 0112). Matches."),
 "016": ("L01 0083-0084", "Misconception 3: passing many pairs proves nothing (line 0084). Card is now T and carries no lab number, which matches its derivation from Definition 2.1."),
 "165": ("L01 0066, 0171", "Example 3.3 gives eigenvalues 3 and -1 of Q2 with eigenvectors (1,1),(1,-1) (line 0066); quiz line 0171 repeats 3 and -1."),
 "177": ("L01 0080", "Misconception: circle midpoint of (1,0),(0,1) is (1/2,1/2), squared norm 1/2 != 1, strictly inside (line 0080 and 0020). Matches."),
 "178": ("L01 0115-0117", "E1: 184 ordered pairs with negative form, 3 x 184 = 552, gap vanishes at weights 0 and 1 (line 0117). Numbers match labout/L01.out. Lab 1 basis; the lesson labels Q1/Q2 SIMULATED (line 0069), so the card basis lacks the label."),
 "179": ("L01 0064, 0066", "Under Assumption 1 eigenvalues 3,1 non-negative give convexity of Q1 (line 0066, Prop 3.2 at 0064). Matches; T."),
 "180": ("L01 0064, 0112", "Q2 not convex without Assumption 1 because P3 (line 0112) shows a negative eigenvalue refutes convexity with no assumption. Matches."),
 "184": ("L01 0031-0032", "Example 2.2: |x| convex on R via triangle inequality; not differentiable at 0 (line 0032). Matches."),
 "189": ("L01 0070, 0071, 0174", "Lab 1 prints midpoint value 3/2, chord 1, chord minus midpoint -1/2 (labout/L01.out line 'Q2 at x = (1, 0)...'). Lemma 3.1 gives the same gap (line 0174). Card is C with a basis, but the lesson labels Q1/Q2 SIMULATED (line 0069) and the card basis lacks the label."),
 "017": ("L02 0020-0021", "Definition 2.1 Lagrange multiplier with sign convention grad f = lambda grad h (line 0021). Matches."),
 "018": ("L02 0023-0025", "Theorem 2.2 hypotheses (U open, C^1, feasible, grad h != 0, local minimizer) and conclusion match lines 0025-0026."),
 "019": ("L02 0036", "Example 2.5: h=y^2-x^3, f=x, origin minimizer, grad h=0 so no multiplier (line 0036). Matches."),
 "020": ("L02 0038", "Example 2.6: feasible (0,-y), f=-y^3<0=f(0,0); witness (0,-1) refutes global minimality (line 0038). Matches."),
 "021": ("L02 0039-0042", "Proposition 2.4 uniqueness with grad h != 0 and the regularity step (line 0042). Matches."),
 "022": ("L02 0046-0050, 0055-0058", "Proposition 3.2 closed form: u=Sigma^-1 1, s=1'u, lambda=1/s, w*=lambda u, unique minimizer; no sign condition (line 0050). Matches."),
 "023": ("L02 0056-0058", "Proposition 3.2(d): f(w)-f(w*)=(1/2)d'Sigma d, linear term vanishes via lambda 1'd=0 (line 0058). Matches."),
 "024": ("L02 0060-0062", "Proposition 3.3: A'A+I symmetric, x'(A'A+I)x=||Ax||^2+||x||^2 > 0 for x != 0 (line 0062). Matches."),
 "025": ("L02 0106-0108", "P3: f(w*)=lambda/2 and 1/(2s) via w*'Sigma w* = lambda 1'w* = lambda (line 0108). Matches."),
 "026": ("L02 0091", "M2: u=(1,1/2), s=3/2, lambda=2/3, w*=(2/3,1/3), f=1/3 (line 0091). Recomputed in verify_numbers_r2.out (L02 M2 line). Matches."),
 "027": ("L02 0066", "Lab 1 prints Sigma rows 4 2 5 / 2 7 4 / 5 4 14 from A entries 1,2,3,1,-1,2,-1,-1,0 (line 0066); recomputed in verify_numbers_r2.out (L02 Sigma). SIMULATED basis carried."),
 "028": ("L02 0066", "Lab 1 prints lambda = 177/55 (line 0066); recomputed as 1/(1'Sigma^-1 1) = 177/55 in verify_numbers_r2.out (L02 line)."),
 "029": ("L02 0066, 0126", "w = (47/55, 17/55, -9/55) (line 0066); negative third weight stated in R1 (line 0126). Recomputed in verify_numbers_r2.out."),
 "030": ("L02 0066-0067, 0115-0117", "36 of 36 counts over six directions and six steps (labout/L02.out); E2 (line 0117) states what they do and do not show. Matches."),
 "031": ("L02 0076", "Misconception 1: f=x^2+y^2 on x+y=1 has minimizer (1/2,1/2) and grad f=(1,1)=1 grad h (line 0076). Matches."),
 "032": ("L02 0078", "Misconception 2: Example 2.6 shows stationarity is not sufficient (line 0078). Matches."),
 "033": ("L02 0080", "Misconception 3: Example 2.5 minimizer with grad h=0 and no multiplier (line 0080). Matches."),
 "168": ("L02 0066, 0121", "Objective 177/110 = lambda/2 (line 0121, E3) and labout/L02.out 'objective f(w) = 177/110'. Matches."),
 "169": ("L02 0066-0067", "Budget exactly 1 and gradient residual exactly 0 (labout/L02.out lines 'budget ... True', 'all exactly zero: True'). Matches."),
 "176": ("L02 0034", "Remark 2.3: each tangent direction gives a feasible curve; minimality rules out first-order decrease (line 0034). Matches."),
 "181": ("L02 0066", "Lab 1 minimum-variance weights (47/55, 17/55, -9/55) (line 0066). Matches; SIMULATED basis carried."),
 "185": ("L02 0044", "Positive definite: x'Sigma x>0 for x != 0; stronger than non-negativity because it excludes zero at non-zero x (line 0044). Matches."),
 "036": ("L03 0017", "Definition 1.1 feasible set F of all constraints (line 0017). Matches."),
 "037": ("L03 0017", "Definition 1.1: active when g_i(x)=0, slack when g_i(x)<0 (line 0017). Matches."),
 "038": ("L03 0019-0023", "Definition 1.2 KKT point with (K1) to (K4) (lines 0020-0023). Matches."),
 "039": ("L03 0023, 0026", "Remark 1.3: (K4) says one of lambda_i and g_i is zero; slack implies zero multiplier; active may have zero multiplier (line 0026). Matches."),
 "040": ("L03 0028-0030", "Lemma 1.4 gradient inequality and the zero-gradient corollary (lines 0028, 0030). Matches."),
 "041": ("L03 0032-0034", "Lemma 1.5: symmetric Sigma with x'Sigma x >= 0 gives q convex for every c, gradient Sigma w - c (line 0032). Matches."),
 "042": ("L03 0036-0042", "Theorem 2.1 hypotheses (f, g_i convex and differentiable; h_j affine) and conclusion; Remark 2.2 says no further hypothesis is used (line 0042). Matches."),
 "043": ("L03 0044", "Example 2.3: f'(0)=0, f(-1)=-1<0=f(0); midpoint -1/8 exceeds average -1/2 so not convex (line 0044). Matches; hand check: f(-1/2)=-1/8, average (1/2)f(-1)+(1/2)f(0)=-1/2, and -1/8 > -1/2 so convexity fails."),
 "044": ("L03 0047-0048", "Example 3.1: F={0}, grad g_1(0)=0 so (K1) reads 1=0; Slater fails (line 0047). Matches."),
 "046": ("L03 0054", "Example 4.1: w*=(1,0), nu=-1/2, lambda=(0,3/10), optimal value -1/2 (line 0054). Recomputed: stationarity (1/2+nu-lambda_1=0, 4/5+nu-lambda_2=0). Matches."),
 "047": ("L03 0056", "Example 4.2: w*=(1/2,1/2), nu=-1/2, lambda=0, value -1/4 (line 0056). Recomputed in verify_numbers_r2.out. Matches."),
 "048": ("L03 0063", "Remark 4.3: Sigma^-1 mu=(14/15,-11/30), weights sum 17/30 (line 0063). Recomputed in verify_numbers_r2.out. Matches."),
 "049": ("L03 0058, 0060", "Lab 1 prints zero residuals for both candidates (labout/L03.out 'all four KKT conditions hold exactly: True'). Lesson labels Sigma and mu SIMULATED (line 0052); card basis lacks the label."),
 "050": ("L03 0060-0061", "Lab 1 prints stationarity residual (-1/2,1/2) and dual residual 3/10 for lambda_2=-3/10 (labout/L03.out). Recomputed in verify_numbers_r2.out. Lesson labels inputs SIMULATED (line 0052); card basis lacks the label."),
 "051": ("L03 0072", "Misconception 1: KKT point not automatically optimal without convexity (Example 2.3, line 0072). Matches."),
 "052": ("L03 0074", "Misconception 2: Example 4.1, w_1>=0 slack with multiplier zero, binding w_2>=0 has 3/10 (line 0074). Matches."),
 "053": ("L03 0076", "Misconception 3: (14/15,-11/30) violates budget and w_2>=0 (line 0076). Matches."),
 "160": ("L03 0019", "Lagrangian L = f + sum lambda_i g_i + sum nu_j h_j (Definition 1.2, line 0019). Matches."),
 "161": ("L03 0024", "KKT residual: amount by which a candidate fails a condition; zero means holds (line 0024). Matches."),
 "173": ("L03 0060-0061, 0072", "Grid minima -1/2 at w1=1 and -1/4 at w1=1/2 on 101 points: verify_numbers_r2.out (L03 grid min lines) and labout/L03.out. Lesson labels inputs SIMULATED (line 0052); card basis lacks the label."),
 "187": ("L03 0017", "Definition 1.1 optimal: x* in F and f(x*) <= f(x) for every x in F (line 0017). Matches."),
 "056": ("L04 0018", "Definition 1.1 dual function as an infimum and dual feasibility (line 0018). Matches."),
 "057": ("L04 0020-0022", "Proposition 1.2 concavity from affineness in (lambda,nu); proof uses no convexity (line 0022). Matches."),
 "058": ("L04 0024-0026", "Proposition 1.3 weak duality, no convexity needed; proof lines 0026 match card text."),
 "059": ("L04 0028-0030", "Proposition 1.4 bound min over F~ minus max over D~ >= p*-d* >= 0; finiteness (line 0030 and P2 line 0089). Matches."),
 "060": ("L04 0031-0032, 0117-0119", "Remark 1.5 (grid gap is an upper bound) and R3 (grid gap 7/300, true gap 0). verify_numbers_r2.out 'L04 R3 restricted ... grid gap=7/300 ... True' recomputes 7/300. Matches."),
 "061": ("L04 0035-0037", "Proposition 2.1 hypotheses (f, g_i convex differentiable, h_j affine, KKT point) and conclusion (line 0035). Matches."),
 "062": ("L04 0039", "Example 2.2: g=-(1/2)r'Sigma^-1 r - nu, r=(2,1) at KKT point, g=-1/2=f(1,0) (line 0039). Recomputed in verify_numbers_r2.out (L04 g at KKT). Matches."),
 "063": ("L04 0041, 0043", "Lab 1 prints 1331 dual, 21 primal, 27951 pairs (labout/L04.out). Recomputed in verify_numbers_r2.out (L04 dual grid=1331 ... weak_ok=27951). Lesson labels the inputs SIMULATED in the lab header (line 0042); card basis lacks the label."),
 "064": ("L04 0078-0080", "M3: g(0,0)=-199/300 via mu'Sigma^-1 mu=199/150 (line 0080). Recomputed in verify_numbers_r2.out (L04 g(0,0)=-199/300 True). Matches; T."),
 "065": ("L04 0047", "Definition 3.1 Slater point strict inequalities, exact equalities (line 0047). Matches."),
 "067": ("L04 0050", "Remark 3.3: wbar=(1/2,1/2) is a Slater point with g_i=-1/2 (line 0050). Matches."),
 "068": ("L04 0051-0052", "Example 3.4: F={0}, g(0)=-inf, g(lambda)=-1/(4 lambda), gap 0, supremum not attained (line 0052). Matches."),
 "069": ("L04 0060-0061", "Misconception 1: g(0,0)=-199/300 is 49/300 below p*=-1/2 (line 0061); verify_numbers_r2.out confirms 49/300. Matches; T."),
 "070": ("L04 0062-0063", "Misconception 2: dual problem maximizes g; best lower bound is the largest (line 0063). Matches."),
 "071": ("L04 0064-0065", "Misconception 3: exact arithmetic, grid gap bounds from above (Remark 1.5), weak duality non-negativity (line 0065). Matches."),
 "170": ("L04 0043-0044", "Lab 1 prints largest dual -1/2 at one point, grid gap 0 (labout/L04.out 'dual grid points attaining that value: 1'). Lesson labels the inputs SIMULATED in the lab header (line 0042); card basis lacks the label."),
 "073": ("L05 0018-0020", "Definition 1.1 QP data, feasible set, equality-only and inequality-only cases (lines 0018-0020). Matches."),
 "074": ("L05 0022", "Remark 1.2: only the symmetric part of Q matters (line 0022). Matches."),
 "075": ("L05 0024-0026", "Lemma 1.3 exact expansion with gradient Qx+c and Hessian Q (lines 0025-0026). Matches."),
 "076": ("L05 0030-0032", "Lemma 1.4 tangent-plane inequality for Q psd via Lemma 1.3 with d=y-x (line 0032). Matches."),
 "077": ("L05 0036-0039", "Proposition 2.1 KKT matrix nonsingular for Q pd and A full row rank (lines 0037-0039). Matches."),
 "078": ("L05 0041", "Remark 2.2: two equal rows of A give singular K (line 0041). Matches; verify_numbers_r2 check not needed (structural)."),
 "079": ("L05 0042-0045", "Theorem 2.3 unique minimiser via KKT solve; proof uses Lemma 1.3 and the first block row (line 0045). Matches."),
 "080": ("L05 0046-0047", "Remark 2.4 identity xQx=(2x1+x2/2)^2+(11/4)(x2+4x3/11)^2+(18/11)x3^2 checked by expansion (matches Q); positive definite. Matches."),
 "081": ("L05 0055-0058", "Theorem 3.1 sufficiency for convex QP with mu>=0 and complementary slackness (lines 0056-0058). Matches."),
 "082": ("L05 0059-0060", "Remark 3.2: mu=-1 at x=0, f(0)=0 > f(1)=-1/2 (line 0060). Matches."),
 "083": ("L05 0061-0062", "Definition 3.3 S-candidate and the Theorem 2.3 linear independence condition (line 0062). Matches."),
 "084": ("L05 0063-0066", "Proposition 3.4 midpoint-convex F, at most one minimiser; identity f(z)=(f(x)+f(y))/2-(1/8)(x-y)'Q(x-y) (line 0066). Matches."),
 "085": ("L05 0067-0068", "Remark 3.5: x'Qx=(x1+x2)^2+x1^2+x2^2 and nonnegative midpoint coordinates (line 0068). Matches."),
 "086": ("L05 0069-0070", "Example 3.6: xbar=(3/2,0), mubar=(0,5/2), f=-9/4 (line 0070); recomputed in verify_numbers_r2.out (L05 Part B S=(1,)). Matches."),
 "087": ("L05 0075-0076", "Lab 1 Part A prints x = 13/19, 3/19, 3/19 and zero residuals (labout/L05.out). Recomputed in verify_numbers_r2.out (L05 Part A solve)."),
 "088": ("L05 0075-0076, 0122", "Objective 551/722 = 0.7631578947 (line 0122); recomputed as 29/38 = 551/722 in verify_numbers_r2.out (L05 Part A objective)."),
 "089": ("L05 0075-0076, 0126", "Lab 1 Part B: only {2} passes both tests, passing_candidates 1 (labout/L05.out). Recomputed in verify_numbers_r2.out (L05 Part B S lines)."),
 "090": ("L05 0061-0062", "Definition 3.3 enumerates 2^p sets; p=2 gives four candidates (line 0062 and 0080). Matches."),
 "091": ("L05 0084-0085", "Misconception 1: Q=diag(1,-1) gives f(0,t)=-t^2/2, no minimiser (line 0085). Matches."),
 "092": ("L05 0086-0087", "Misconception 2: stationarity alone not sufficient; mu-bar >= 0 needed (line 0087). Matches."),
 "093": ("L05 0088-0089", "Misconception 3: gradient = -A'lambda*, lambda* = (-36/19, 11/19) printed by Lab 1 (line 0089). Recomputed: Qx+c=(36/19,25/19,47/19)=-A'lambda. Matches."),
 "166": ("L05 0047", "Remark 2.4: Av=0 for v=(-2,1,1) (line 0047); linear term vanishes since Qx+c=-A'lambda. Matches; Qv=(-7,2,3), v'Qv=19 in verify_numbers_r2.out."),
 "171": ("L05 0075-0076, 0176", "Lab 1 Part A prints kkt_determinant 19 (labout/L05.out); recomputed det(K)=19 in verify_numbers_r2.out. Matches."),
 "172": ("L05 0075-0076", "Lab 1 Part B grid: 1089 points, grid_points_below_candidate 0 (labout/L05.out); recomputed 0 of 1089 in verify_numbers_r2.out. Matches."),
 "182": ("L05 0075, 0089", "Lab 1 Part A lambda = -36/19, 11/19 (labout/L05.out); recomputed in verify_numbers_r2.out (L05 Part A lambda). Matches."),
 "097": ("L06 0016-0018", "Definition 1.1 mean-variance objective f_gamma = (gamma/2) w'Sigma w - mu'w (line 0018). Matches."),
 "098": ("L06 0020", "Definition 1.2: QP of L05 with Q=gamma Sigma, c=-mu, A=1', b=1 (line 0020). Matches."),
 "099": ("L06 0016, 0058", "Section 1 says M7 does not estimate mu or Sigma (line 0016); Lab 1 inputs seeded and SIMULATED (lab header line 0058). Matches."),
 "100": ("L06 0022-0026", "Theorem 1.3 closed form w(gamma)=(y-lambda z)/gamma, lambda=(1'y-gamma)/(1'z); proof line 0026. Matches."),
 "101": ("L06 0028", "Remark 1.4: Sigma = M'M/16 + I/10 is positive definite (line 0028). Matches."),
 "102": ("L06 0032-0036", "Proposition 2.1: V(gamma1) <= V(gamma2) and R(gamma1) <= R(gamma2) for gamma1>gamma2; proof lines 0036 check. Matches."),
 "103": ("L06 0040-0042", "Proposition 2.3: F+ subset F0, so infimum over F+ >= infimum over F0 (lines 0040-0042). Matches."),
 "104": ("L06 0044-0045", "Definition 3.1 linear constraints; box and sector constraint and nonnegativity as box with l=0 (line 0045). Matches."),
 "105": ("L06 0046-0047", "Definition 3.2 turnover sum |w_i - w0_i| <= tau with tau >= 0 (line 0047). Matches."),
 "106": ("L06 0049", "Remark 3.3: |w_i-w0_i|<=s is a pair of linear inequalities (line 0049). Matches."),
 "107": ("L06 0055", "Remark 3.5: (w,t) linear in constraints, Hessian psd on w block and zero on t block (line 0055). Matches."),
 "108": ("L06 0059-0060", "Lab 1 mu = 7/100, 1/20, 3/25, 1/50 (labout/L06.out 'mu 7/100 1/20 3/25 1/50'); recomputed from simulate_inputs in verify_numbers_r2.out. SIMULATED basis carried."),
 "109": ("L06 0059-0060", "Lab 1 Sigma diagonal 49/40, 27/20, 103/80, 103/80 (labout/L06.out); recomputed in verify_numbers_r2.out (L06 inputs diag). SIMULATED basis carried."),
 "110": ("L06 0059, 0069", "Equality row gamma=1: return 0.113798, risk 0.123809, weights (0.434783,0.526836,0.562535,-0.524154). Recomputed exactly in verify_numbers_r2.out (L06 eq gamma=1). Matches."),
 "111": ("L06 0059-0060", "Weight on A4 negative at gamma=1,2,4,8,16 (-0.524154,-0.462816,-0.432147,-0.416813,-0.409145); recomputed in verify_numbers_r2.out. Matches."),
 "112": ("L06 0059-0060, 0166", "Zero set {A4} at each gamma; recomputed by independent Part B enumeration (verify_numbers_r2.out, passing-set (4,) for every gamma). Matches."),
 "113": ("L06 0059, 0110", "Objectives 0.820002 vs 1.392257 at gamma=16; exact difference 0.5722548315 recomputed in verify_numbers_r2.out (L06 E2). Matches."),
 "114": ("L06 0059, 0114", "Turnover at gamma=4 exact 0.5588607333, rounded 0.558861; from printed six-place weights 0.558860 (verify_numbers_r2.out L06 E3). Matches line 0114."),
 "115": ("L06 0068-0069", "Misconception 1: return falls as gamma rises (Proposition 2.1, lab return column 0.113798 to 0.106241). Matches."),
 "116": ("L06 0070-0071", "Misconception 2: at gamma=1 all four weights change (values match lab table, line 0071). Matches."),
 "117": ("L06 0072-0073", "Misconception 3: auxiliary variables give linear inequalities with sum t_i <= tau (Proposition 3.4, line 0073). Matches."),
 "118": ("L06 0059, 0144-0146", "Lab 1 Part A kkt_matches_closed_form True at each gamma (labout/L06.out); identity is Theorem 1.3. Matches."),
 "163": ("L06 0051-0052", "Proposition 3.4 holds with no sign assumption on w, w0 or tau (lines 0051-0052). Matches."),
 "164": ("L06 0038", "Remark 2.2: Proposition 2.1 needs no property of F' beyond minimisation, so it covers the w>=0 problem (line 0038). Matches."),
 "167": ("L06 0026", "Proof of Theorem 1.3: 1'z = z'Sigma z > 0 since Sigma z = 1 nonzero (line 0026). Matches."),
 "174": ("L06 0059", "Lab 1 Part B: candidates_passing 1 in every gamma row (labout/L06.out); independent enumeration gives one passing set per gamma. Matches."),
 "188": ("L06 0032", "Proposition 2.1: R(gamma1) <= R(gamma2) for gamma1 > gamma2, i.e. the return does not rise (line 0032). Matches."),
 "121": ("L07 0018", "Definition 1.1 data: finite S, nonempty finite A(s), deterministic f, r, B (line 0018). Matches."),
 "122": ("L07 0020", "Definition 1.2 plan, total reward J_t(p), value V_t(s), optimal plan (line 0020). Matches."),
 "123": ("L07 0022", "Remark 1.3: A(s)=(0,1), r=a, H=1: supremum 1 not attained (line 0022). Matches."),
 "124": ("L07 0024", "Definition 1.4 continuation of a plan from time k (line 0024). Matches."),
 "125": ("L07 0027-0028", "Theorem 2.1 backward recursion V_H=B, V_t = max{r + V_{t+1}(f)} (line 0028). Matches."),
 "126": ("L07 0033", "Theorem 2.2 principle of optimality (line 0033). Matches."),
 "127": ("L07 0038", "Theorem 2.3 (i) and (ii) characterise an optimal plan (line 0038). Matches."),
 "128": ("L07 0042", "Corollary 2.4: forward plan choosing maximizing actions is optimal (line 0042). Matches."),
 "129": ("L07 0051", "Remark 2.5: V_0(x)=1 attained only by b; plan (a,c) earns 0; its continuation (c) is optimal (line 0051). Matches."),
 "130": ("L07 0049", "Lab 1 Part A W400 column 240, 220, 200, 130, 4 (labout/L07.out); recomputed in verify_l07_l08_r2.out (L07 t lines). SIMULATED basis carried."),
 "131": ("L07 0049", "Lab 1 Part B recursion_matches_brute_force True over t=0..3, five states; independently recomputed in verify_l07_l08_r2.out (brute-force matches at all t<H, all w). Matches."),
 "132": ("L07 0049, 0100-0104", "70 feasible plans from (0,400) (labout/L07.out); binom(8,4)=70 (line 0104); verify_l07_l08_r2.out 'feasible plans from (0,400): 70'. Matches."),
 "133": ("L07 0048", "Optimal plan 100 each period, path 400,300,200,100,0, total 240 (labout/L07.out). Recomputed in verify_l07_l08_r2.out. Matches."),
 "134": ("L07 0048", "Greedy plan 400,0,0,0 total 130, not optimal; tails from t=1,2,3 optimal (labout/L07.out). Recomputed greedy total 130 in verify_l07_l08_r2.out. Matches."),
 "135": ("L07 0059", "Misconception 1: largest period reward 130 at consumption 400; greedy total 130 vs optimal 240 (line 0059). Matches."),
 "136": ("L07 0061", "Misconception 2: Remark 2.5 and Part C greedy plan with greedy_plan_optimal False (line 0061). Matches."),
 "137": ("L07 0063", "Misconception 3: wealth-400 values 240 at t=0 and 130 at t=3 (line 0063; Part A). Matches."),
 "142": ("L08 0018", "Definition 1.1 discounted total with beta^{k-t} and beta^{H-t}B(s_H) (line 0018). Matches; beta>=0 is the range stated in line 0016."),
 "143": ("L08 0020", "Definition 1.2 Bellman equation U_H=B, U_t = max{r + beta U_{t+1}} (line 0020). Matches."),
 "144": ("L08 0022-0024", "Theorem 1.3 for beta>=0 (line 0022; proof line 0024). Matches."),
 "145": ("L08 0026-0028", "Theorem 1.4 uniqueness given terminal condition for beta>=0 (lines 0026-0028). Matches."),
 "146": ("L08 0030, 0089-0090", "Remark 1.5 with B=0: value (U_0,U_1)=(1,0) since c=B=0 (Problem P3 lines 0089-0090). Matches."),
 "147": ("L08 0034", "Definition 2.1 Bellman operator G and value iteration U^{n+1}=G U^n (line 0034). Matches."),
 "148": ("L08 0036-0038", "Lemma 2.2 time shift V^(H)_t = V^(H-t)_0 with same terminal reward (lines 0036-0038). Matches."),
 "149": ("L08 0040-0042", "Proposition 2.3 U^n = W^(n)_0 for beta>=0, induction using Theorem 1.3 and Lemma 2.2 (lines 0040-0042). Matches."),
 "150": ("L08 0048; lab code range(7)", "Lab 1 Part C prints iterate_equals_n_period_recursion True (labout/L08.out); tests/labs/M7/lab-M7-L08-1.py line 131 checks range(7), i.e. n=0..6; independently recomputed for n=0..6 in verify_l07_l08_r2.out. Matches."),
 "151": ("L08 0048", "Lab 1 Part A V0 for state 0 = 13.948890 with run policy (labout/L08.out); recomputed exactly 1394889/100000 in verify_l07_l08_r2.out. Matches."),
 "152": ("L08 0048", "tied_pairs_t0_to_5 0; states 0 and 1 run at every t (labout/L08.out); recomputed ties 0 in verify_l07_l08_r2.out. Matches."),
 "153": ("L08 0048-0049", "plans_enumerated 378 = 3 x (2^6+...+2^1) (labout/L08.out, line 0103); recomputed 378 in verify_l07_l08_r2.out. Matches."),
 "154": ("L08 0048-0049, 0099", "Changes 6.0, 3.6, 2.74, 2.466, 2.2194, 1.99746; ratio 0.9 from n=3 on (line 0099). Recomputed exactly and ratios in verify_l07_l08_r2.out. Matches."),
 "155": ("L08 0058", "Misconception 1: one-state example U^1 = 1 + U^0 (line 0058). Matches."),
 "156": ("L08 0060", "Misconception 2: Remark 1.5 gives a solution for every c; terminal condition fixes it for beta>=0 (line 0060). Matches."),
 "157": ("L08 0049, 0062", "Policy in state 2 is repair for t=0..3 and run for t=4,5 (labout/L08.out; recomputed in verify_l07_l08_r2.out). Matches."),
 "162": ("L08 0044", "Remark 2.4: changes alone do not bound the error; no infinite-horizon claim (line 0044). Matches."),
 "175": ("L08 0049", "Lab 1 Part B: recursion matches brute force at each of 18 (t,s) pairs (line 0049; labout/L08.out). Recomputed in verify_l07_l08_r2.out. Matches."),
 "186": ("L08 0054", "Negative discount beta=-1 example: V_0=1, U_0=0 so (V_0,V_1,V_2) is not a solution (line 0054). Recomputed in verify_l07_l08_r2.out (beta=-1 U0=0). Matches."),
}

rows = []
for cid, card in sorted(by_id.items()):
    num = cid.split("-c")[1]
    key = num
    if key not in E:
        raise SystemExit(f"no reading recorded for {cid}")
    loc, ev = E[key]
    rid = f"E-c{num}"
    sim_fail = cid in {"M7-c012", "M7-c178", "M7-c189", "M7-c049", "M7-c050", "M7-c173", "M7-c063", "M7-c170"}
    status = "FAIL" if sim_fail else "PASS"
    row = {
        "id": rid,
        "check": "card-vs-lesson: front, back, grade, basis, locator, numbers, duplicates, process words, SIMULATED label",
        "location": f"course/modules/M/M7/cards.json ({cid}, lesson {card['lesson']}, grade {card['grade']}); course/modules/M/M7/{card['lesson']}.html text lines {loc}",
        "status": status,
        "evidence": ev,
    }
    if sim_fail:
        row["evidence"] = ev + " Card is grade C and carries no SIMULATED label, although the lesson labels this lab's inputs SIMULATED (see location)."
        row["fix"] = f"Append ' (SIMULATED)' to the basis field, which currently reads {card.get('basis', '')!r}."
    rows.append(row)

# slice-level rows (kept ids E-S01..E-S11 from round 1, plus new round-2 rows)
S = []
def srow(rid, check, location, status, evidence, fix=None):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if fix:
        r["fix"] = fix
    S.append(r)

srow("E-S01", "2.6-gate (check_pages)", "tools/check_pages.py --unit M7; cards.json", "PASS",
     "`.venv/bin/python tools/check_pages.py --unit M7` -> 'check_pages M7: PASS', exit 0 (ledgers/M7/scripts/M7-e-r2/gates/check_pages.log). check_cards: unique ids, lessons exist, grades valid, basis present for every non-T card.")
srow("E-S02", "2.9-gate (check_dag)", "tools/check_dag.py --all", "PASS",
     "`check_dag.py --all` exit 0 (gates/check_dag.log); `check_dag.py --unit M7` -> 'check_dag M7: PASS'. No card uses a concept outside the M7 prerequisite closure by name (M2, M3 cited as Assumption sources).")
srow("E-S03", "2.6-gate (check_projects)", "tools/check_projects.py --unit M7", "PASS",
     "`check_projects.py --unit M7` -> 'check_projects M7: PASS', exit 0 (gates/check_projects.log). Slice is cards only; project slices belong to other fragments.")
srow("E-S04", "2.5-labs (run_labs)", "tools/run_labs.py --unit M7; tests/labs/M7/*.py", "PASS",
     "`run_labs.py --unit M7` -> 'run_labs M7: PASS (11/11)', exit 0 (gates/run_labs.log). Each L01-L08 twin also run alone under `python3 -I -W error`, exit 0 for all eight (labout/L01.out..L08.out); the printed values match each lesson's expected block.")
srow("E-S05", "2.7-cards (banned and process phrases)", "cards.json front/back; scan_cards_r2.py", "PASS",
     "scan_cards_r2.out: 'banned/process hits: []' over all 170 cards (TODO, TBD, lorem, for brevity, beyond the scope, obviously, clearly, it is important, we/our/let us). Ellipses in cards (M7-c122, c124, c132, c143, c144, c145, c153) are math ranges a_t, ..., a_{H-1} or sum-index ranges, not omitted content.")
srow("E-S06", "2.7-cards (duplicates)", "cards.json; card_checks_r2.py", "PASS",
     "card_checks_r2.out: 170 cards, 170 unique ids, no duplicate fronts or backs. 12 pairs have a similarity ratio above 0.75 (e.g. c009/c165, c046/c047, c133/c134); each pair asks about a different matrix, sample, plan or quantity, so none is a duplicate card.")
srow("E-S07", "2.7-cards (basis and grade)", "cards.json front/back/basis; scan_cards_r2.out", "PASS",
     "Every C card has a non-empty basis (card_checks_r2.out 'C cards without basis []'); T cards have no basis field. Grades: T 122, C 48. Cards naming 'Lab' while graded T (M7-c060, c069, c085, c090, c099, c101, c117) cite the lab only for descriptions or for values that the page derives (7/300 by R3, -199/300 by M3).")
srow("E-S08", "2.2-numbers (numbers in cards vs lesson text)", "cards.json numbers; card_checks_r2.out; LXX.txt extracts", "PASS",
     "card_checks_r2.out: 15 numeric tokens are absent as plain text, all present in the lesson as LaTeX (\\tfrac{..}{..}, e.g. 2/3 as \\tfrac23 at L02 line 0091, 1/8 at L03 line 0044, 7/300 at L04 line 0119, 4/11 and 18/11 at L05 line 0046). 0 references missing (every 'Definition/Theorem/Proposition/Lemma/Remark/Example/Problem' label in a card occurs in its lesson). Card numbers recomputed in verify_numbers_r2.out and verify_l07_l08_r2.out.")
srow("E-S09", "2.8 / notation (notation/notation.json)", "notation/notation.json (8 symbols); cards.json", "PASS",
     "notation.json registers T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, \\mathbb{Q}. No card uses T as a count, Phi, gamma_3, gamma_4, R^*, R^{e*} or R_f. The M7 cards use plain Q for quadratic-form matrices (distinct glyph from \\mathbb{Q}), gamma for risk aversion (the macro \\emgamma keeps plain gamma free), and R(gamma) for return; none conflicts with a registered meaning.")
srow("E-S10", "2.1-references (verify_refs offline)", "tools/verify_refs.py --offline", "PASS",
     "`verify_refs.py --offline` -> 'offline integrity: 560 entries, 0 problems', exit 0 (gates/verify_refs_offline.log). Cards carry no 'cite' field, so no card cites a key. (`--unit` is not valid with --offline in this tool.)")
srow("E-S11", "2.3-grades (rule 9: T cards carrying lab-printed numbers)", "cards.json T cards; scan_cards_r2.out", "PASS",
     "scan_cards_r2.out 'T-graded cards carrying lab-printed values: []'. Round 1 flagged M7-c010 and M7-c013 for this; both were rewritten (c010 back has no 3/2 or 1; c013 back uses the Lemma 3.1 gap -1/2) and M7-c016 was regraded T without lab numbers. Re-checked here: no T card carries a value printed only by a lab.")
srow("E-S12", "2.8-smoke (page_smoke)", "tools/page_smoke.py --unit M7", "PASS",
     "`page_smoke.py --unit M7` -> 'page_smoke M7: PASS', exit 0 (gates/page_smoke.log), covering index.html, concepts.html, review.html and every lesson and project page.")
srow("E-S13", "code gates (ruff, format, mypy, pytest)", "ruff check .; ruff format --check .; mypy --no-incremental; pytest", "PASS",
     "ruff check: 'All checks passed!' (gates/ruff_check.log); ruff format --check: '473 files already formatted'; mypy --no-incremental: 'Success: no issues found in 331 source files' (gates/mypy.log); pytest tests/test_curriculum.py tests/test_docs_figures.py: 29 passed (gates/pytest_relevant.log); pytest tests/test_page_checks.py: all passed (gates/pytest_page_checks.log).")
srow("E-S14", "2.5-labs (independent recomputation)", "verify_numbers_r2.py; verify_l07_l08_r2.py", "PASS",
     "Both scripts run with `python3 -I` (outputs verify_numbers_r2.out, verify_l07_l08_r2.out). They recompute every number the cards state (L01 2573/184/552; L02 55/177, 177/55, 177/110; L03 grid minima; L04 27951, -199/300, 7/300, -157/300; L05 det 19, 551/722, 1089 grid, Part B candidates; L06 every printed row, 0.5722548315, 0.5588607333, the 1-passing-set enumeration; L07 and L08 recursions, brute force, 70, 378, change sequence and ratios).")
srow("E-S15", "2.5-mutants (not applicable)", "cards.json", "PASS",
     "Slice e is cards.json only: it has no executable grader or code, so no mutant applies to this slice. The mutant rules (2.6) belong to the project slices, which other fragments cover. Ledger 'mutants' is empty.")
srow("E-S16", "2.2-count (card count vs task)", "cards.json (170 entries); plans/M7-open-items.md; round-1 pin d0f39c09 (169 entries)", "PASS",
     "The checkout holds 170 cards: the 169 round-1 cards plus M7-c189 (added after pin d0f39c09, lesson L01, grade C). The task text's 169 is the round-1 count. Card-id gaps (c035, c045, c054, c055, ...) are stable ids, not defects.")

fragment = {
    "unit": "M7",
    "slice": "e",
    "round": 2,
    "verifier": "Claude Haiku 5.5, independent verifier for M7-e, round 2 (did not build M7; read all 8 lessons line by line and every card)",
    "pin": "c737272f",
    "base": "d0f39c09 (round-1 pin). Delta: cards.json (M7-c010, c013, c016 regraded T and rewritten, c089 front/back, c157 back, c189 added); L05.html and L06.html macro-only (\\mathbb{R} to \\R); project.html macro-only; tools/, tests/labs/M7, notation/ unchanged.",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyD2-M7-e",
    "scratch": "/tmp/m7e-r2 (lesson text extracts, regenerable with ledgers/M7/scripts/M7-e-r2/extract_text.py)",
    "verified_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
    "verdict": "FAIL",
    "rows": rows + S,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "Every one of the 170 cards was read against the current lesson text (L01-L08 extracts, line-numbered) and every number was recomputed "
        "(verify_numbers_r2.py, verify_l07_l08_r2.py, outputs in ledgers/M7/scripts/M7-e-r2/). No card content error, numeric error, duplicate, banned phrase, "
        "reference or grade defect was found. The one non-PASS class is labelling: 8 grade-C cards report results of lab instances whose lesson labels "
        "the inputs SIMULATED (L01, L03, L04), but the card basis omits that label; the L02, L06, L07 and L08 cards carry it. L05 inputs are labelled "
        "'not data' only, so its cards need no SIMULATED label. Not checked: rendered visual layout of cards (cards are not drawn on a page in this slice); "
        "the 3 alternative correct implementations and 3 student-error mutants (project slices, not in this slice); the full repository pytest suite "
        "(only the modules listed in E-S13 were run); the L05 'not data' versus SIMULATED wording was judged by reading, not by a rule in BUILDER_RULES."
    ),
    "summary": f"M7-e round 2: {len(rows)} card rows ({sum(1 for r in rows if r['status']=='PASS')} PASS, {sum(1 for r in rows if r['status']=='FAIL')} FAIL) and {len(S)} slice rows (all PASS). Verdict FAIL on the SIMULATED labelling of 8 lab-result cards only.",
}
out = root / "ledgers/M7/M7-e.json"
out.write_text(json.dumps(fragment, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("wrote", out, "rows", len(fragment["rows"]), "FAIL", sum(1 for r in fragment["rows"] if r["status"] == "FAIL"))
