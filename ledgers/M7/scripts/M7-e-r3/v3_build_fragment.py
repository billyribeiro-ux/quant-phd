"""Build ledgers/M7/M7-e.json (verifier round 3, slice e) from the per-card evidence below.

Usage: python -I ledgers/M7/scripts/M7-e-r3/v3_build_fragment.py   (run from the checkout root)
Every card row cites the lesson locator (line numbers of v3_extract_text.py output, reproduced in
ledgers/M7/scripts/M7-e-r3/v3_text/) and the script or command that backs any recomputed number.
"""
import json
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(".")
cards = json.loads((ROOT / "course/modules/M/M7/cards.json").read_text(encoding="utf-8"))
card_ids = [c["id"] for c in cards]
by_id = {c["id"]: c for c in cards}

PASS, FAIL = "PASS", "FAIL"
E = {}  # card number -> (status, evidence, fix)


def ok(n, ev):
    E[n] = (PASS, ev, "")


def bad(n, ev, fix):
    E[n] = (FAIL, ev, fix)


SIM_L05_FIX = ("Relabel the L05 lab as SIMULATED (see row E-S13), then set this card's basis to "
               "'Lab 1, Part X (SIMULATED), exact arithmetic' with the same part letter.")

# ---- L01 -----------------------------------------------------------------------------------------
ok(1, "L01 0022-0023 Definition 1.1 (convex set): front and back match in substance; T (definition).")
ok(2, "L01 0033-0036 Definition 2.1 (convex function on a stated convex S); 0036 'relative to S' sentence; T.")
ok(3, "L01 0024-0025 Example 1.2 disk: triangle-inequality chain ends at 1, as the back states; T.")
ok(4, "L01 0027-0030 Proposition 1.3: nonempty family of convex sets, intersection convex; proof 0030; T.")
ok(5, "L01 0039-0042 Proposition 2.3 hypotheses (S convex, f convex on S, c real) and proof; T.")
ok(6, "L01 0046-0048 Lemma 3.1 (symmetric Q, every real lambda) and 0054 'no restriction on lambda'; "
      "identity holds in 3125 of 3125 cases (v3_card_numbers.py, L01 section); T.")
ok(7, "L01 0055-0056 Example 3.2a: gradient 2Qx, constant Hessian 2Q; T.")
ok(8, "L01 0059-0069 Proposition 3.2: (i),(ii) equivalent; (iii) under Assumption 1 (0057-0058); "
      "the (ii)->(iii) step uses the spectral theorem (0068); card names Assumption 1; T.")
ok(9, "L01 0072 Example 3.3: Q1(1,1)=3(1,1), Q1(1,-1)=1(1,-1), recomputed; T.")
ok(11, "L01 0045 and 0052 (symmetry used in Lemma 3.1), R1 0250-0252 (x'Qx = x1^2+x2^2); T.")
ok(12, "L01 0184 prints 2573 of 3125 Q2 chord cases; 3125-2573=552 recomputed (v3_card_numbers.py); "
       "docstring 0078 labels Q1/Q2 SIMULATED; grade C with 'Lab 1 (SIMULATED)' basis.")
ok(13, "L01 0253-0256 Problem R2 and 0332 quiz: one failing triple refutes convexity on the set; T.")
ok(14, "L01 0201-0202 misconception 1 (curved boundary) and Example 1.2 0024-0025; T.")
ok(15, "L01 0203-0204 misconception 2; Q2 eigenvalue -1 (0072) and Problem P3 (0231-0234); T.")
ok(16, "L01 0205-0206 misconception 3 and Definition 2.1 (every pair and weight); T.")
ok(165, "L01 0072 Example 3.3: Q2(1,1)=3(1,1), Q2(1,-1)=-1(1,-1), eigenvalues 3 and -1; T.")
ok(177, "L01 0201-0202 misconception 1 second half; circle midpoint (1/2,1/2) has squared norm 1/2 "
        "(0026, 0202 'strictly inside'); T.")
ok(178, "L01 0185 (184 negative ordered pairs), 0199, E1 0237-0239 (3 x 184 = 552); recomputed by "
        "v3_card_numbers.py; grade C with 'Lab 1 (SIMULATED)' basis.")
ok(179, "L01 0070 and 0072 with Proposition 3.2 (iii) at 0063: eigenvalues 3 and 1 non-negative under "
        "Assumption 1; T.")
ok(184, "L01 0037-0038 Example 2.2 |x| convex, not differentiable at 0; T.")
ok(189, "L01 0187-0188 lab output: midpoint 3/2, chord 1, chord minus midpoint -1/2, identity term -1/2; "
        "recomputed by v3_card_numbers.py; quiz answer 0302 agrees; grade C with 'Lab 1 (SIMULATED)' basis.")
ok(190, "L01 0023 Definition 1.1 wording of convex combination and segment; T.")
ok(191, "L01 0047 names the left side of Lemma 3.1 the chord gap; card expression matches; T.")

# ---- L02 -----------------------------------------------------------------------------------------
ok(17, "L02 0025-0027 Definition 2.1 (Lagrange multiplier, sign grad f = lambda grad h); T.")
ok(18, "L02 0028-0032 Assumption 1 (0028-0029) and Theorem 2.2 hypotheses and conclusion; T.")
ok(19, "L02 0041-0042 Example 2.5: feasible set forces x >= 0, origin minimizer; T.")
ok(20, "L02 0043-0044 Example 2.6: points (0,-y) feasible, f = -y^3 < 0 = f(0,0); T.")
ok(21, "L02 0045-0048 Proposition 2.4 statement and proof; T.")
ok(22, "L02 0053-0056 and 0058-0064 Proposition 3.2 (u, s, lambda, w*, parts a-d); T.")
ok(23, "L02 0062-0064 proof of 3.2(d): f(w)-f(w*) = (1/2)d'Sigma d; T.")
ok(24, "L02 0065-0068 Proposition 3.3 statement and proof; T.")
ok(25, "L02 0224-0227 Problem P3 (f(w*)=lambda/2=1/(2s)); E3 0237-0240 agrees with 177/110; T.")
ok(26, "L02 0207-0210 Problem M2: u=(1,1/2), s=3/2, lambda=2/3, w*=(2/3,1/3); recomputed "
       "(v3_card_numbers.py, L02 section); T.")
ok(27, "L02 0173-0177 lab output: A entries and Sigma rows 4 2 5 / 2 7 4 / 5 4 14; A'A+I recomputed "
       "(v3_card_numbers.py); docstring 0075 SIMULATED; grade C.")
ok(28, "L02 0178 prints lambda = 177/55; recomputed 1'Sigma^-1 1 = 55/177; grade C, lab SIMULATED basis.")
ok(29, "L02 0180 w3 = -9/55 < 0; R1 0242-0245 states the closed form has no sign constraint; grade C.")
ok(30, "L02 0184-0185 counts 36 of 36 (six directions, six steps, docstring 0082-0083); E2 0233-0236 "
       "scope sentence matches; grade C.")
ok(31, "L02 0194-0195 misconception 1 and Example f = x^2+y^2 on x+y=1 (minimizer (1/2,1/2), grad (1,1)); T.")
ok(32, "L02 0196-0197 misconception 2 and Example 2.6; T.")
ok(33, "L02 0198-0199 misconception 3 and Example 2.5 (no multiplier where grad h = 0); T.")
ok(168, "L02 0183 prints f(w) = 177/110 = lambda/2 (P3, 0227); recomputed; grade C, lab basis.")
ok(169, "L02 0181-0182 budget = 1 and residual Sigma w - lambda 1 exactly zero (exact fractions); "
        "Proposition 3.2 (b),(c); grade C.")
ok(176, "L02 0039-0040 Remark 2.3: feasible curve with each prescribed tangent; minimality rules out "
        "first-order decrease; T.")
ok(181, "L02 0179-0180 printed weights (47/55, 17/55, -9/55), recomputed (v3_card_numbers.py); grade C.")
ok(185, "L02 0050 definition of positive definite (x'Sigma x > 0 for x != 0) and the sentence on zero "
        "values; T.")
ok(192, "L02 0026 Definition 2.1 stationary point; 0189 and Example 2.6 0043-0044 (not sufficient); T.")
ok(193, "L02 0022 local minimizer (open ball) definition; T.")

# ---- L03 -----------------------------------------------------------------------------------------
ok(36, "L03 0023 Definition 1.1 feasible set; T.")
ok(37, "L03 0023 Definition 1.1 active and slack; T.")
ok(38, "L03 0025-0029 Definition 1.2 (K1)-(K4); T.")
ok(39, "L03 0029 (K4) and Remark 1.3 0031-0032 ('does not say which one'); T.")
ok(40, "L03 0034-0038 Lemma 1.4 statement and proof; T.")
ok(41, "L03 0040-0044 Lemma 1.5 (symmetric PSD Sigma, any c, gradient Sigma w - c); T.")
ok(42, "L03 0046-0047 Theorem 2.1 hypotheses and conclusion; 0053-0054 Remark 2.2 (no further hypothesis); T.")
ok(43, "L03 0055-0056 Example 2.3: f'(0)=0, f(-1)=-1<0; midpoint -1/8 exceeds average -1/2; T.")
ok(44, "L03 0058-0060 Example 3.1: feasible set {0}; (K1) reads 1 = 0; Slater fails; T.")
ok(46, "L03 0065-0066 Example 4.1 (mu=(3/2,1/5)): w*=(1,0), nu=-1/2, lambda=(0,3/10), p*=-1/2; "
       "recomputed (v3_card_numbers.py, L03 section); T.")
ok(47, "L03 0067-0068 Example 4.2 (mu=(1,1)): w*=(1/2,1/2), nu=-1/2, lambda=0, value -1/4; recomputed; T.")
ok(49, "L03 0172-0188 lab output: all four residuals zero at both candidates; docstring 0073-0074 and "
       "lesson 0064 label inputs SIMULATED; grade C.")
ok(50, "L03 0192-0193 lab output: stationarity (-1/2,1/2) and dual residual 3/10 for flipped sign; "
       "code 0163-0170; SIMULATED label 0064; grade C.")
ok(51, "L03 0204-0205 misconception 1 with Theorem 2.1 and Example 2.3; T.")
ok(52, "L03 0206-0207 misconception 2; Example 4.1 slack constraint w1 >= 0 with g1 = -1 (0066); T.")
ok(53, "L03 0208-0209 misconception 3 and Remark 4.3 0196; (14/15, -11/30) and sum 17/30 recomputed; T.")
ok(160, "L03 0025 Lagrangian L = f + sum lambda g + sum nu h; T.")
ok(161, "L03 0030 KKT residual definition; T.")
ok(173, "L03 0180 and 0190 grid minima -1/2 at w1=1 and -1/4 at w1=1/2 (101 points); interpretation 0194; "
        "grade C, SIMULATED lab basis.")
ok(187, "L03 0023 optimal point definition; T.")
ok(194, "L03 0023 problem (P) definition; T.")
ok(195, "L03 0023 optimal value p* definition; T.")

# ---- L04 -----------------------------------------------------------------------------------------
ok(56, "L04 0024 Definition 1.1 dual function and dual feasible pairs; T.")
ok(57, "L04 0025-0030 Proposition 1.2 (affine in (lambda,nu), concave; no convexity used); T.")
ok(58, "L04 0031-0036 Proposition 1.3 weak duality, no convexity assumption; T.")
ok(59, "L04 0037-0042 Proposition 1.4 grid bound; finiteness used in P2 0198; T.")
ok(60, "L04 0226-0228 Problem R3: grid values -157/300 at nu=-3/5 and -7/10, grid gap 7/300; "
       "recomputed (v3_card_numbers.py, L04 section); Remark 1.5 0043-0044; T.")
ok(61, "L04 0046-0051 Proposition 2.1 hypotheses, conclusion and proof; T.")
ok(62, "L04 0052-0055 Example 2.2: r=(2,1) at the KKT point, g = -1/2 = f(1,0); recomputed; T.")
ok(63, "L04 0143-0145 lab output 1331 dual, 21 primal, 27951 of 27951 pairs; recomputed; "
       "docstring 0061 SIMULATED; grade C.")
ok(64, "L04 0151 prints -199/300; M3 0189 gives mu'Sigma^-1 mu = 199/150; recomputed; 49/300 gap; T.")
ok(65, "L04 0155-0156 Definition 3.1 Slater point and Slater's condition; T.")
ok(67, "L04 0158-0159 Remark 3.3: (1/2,1/2) strictly feasible; T.")
ok(68, "L04 0160-0161 Example 3.4: p*=0, g(lambda)=-1/(4 lambda), supremum not attained; T.")
ok(69, "L04 0169-0170 misconception 1; g(0,0)=-199/300, 49/300 below p*; recomputed; T.")
ok(70, "L04 0171-0172 misconception 2; Definition 1.1 (dual problem maximizes g); T.")
ok(71, "L04 0173-0174 misconception 3; exact arithmetic (0153), Remark 1.5 (0043-0044); T.")
ok(170, "L04 0146-0149 lab output: largest dual -1/2 at lambda=(0,3/10), nu=-1/2, attained once; "
        "smallest primal -1/2 at (1,0); gap 0; recomputed; grade C, SIMULATED basis.")
ok(196, "L04 0024 defines the dual problem and d*; T.")
ok(197, "L04 0157 strong duality = zero gap, Slater result not stated; T.")

# ---- L05 -----------------------------------------------------------------------------------------
ok(73, "L05 0023-0026 Definition 1.1 quadratic program and feasible set; T.")
ok(74, "L05 0027-0028 Remark 1.2 (only the symmetric part of Q matters); T.")
ok(75, "L05 0029-0032 Lemma 1.3 expansion, gradient Qx+c, constant Hessian Q; T.")
ok(76, "L05 0035-0038 Lemma 1.4 (PSD tangent plane and convexity clause); T.")
ok(77, "L05 0042-0045 Proposition 2.1 hypotheses (Q PD, A full row rank) and proof; T.")
ok(78, "L05 0046-0047 Remark 2.2: K rows (1,0,1,1),(0,1,0,0),(1,0,0,0),(1,0,0,0) recomputed by hand, det 0; T.")
ok(79, "L05 0048-0051 Theorem 2.3 hypotheses and conclusion; T.")
ok(80, "L05 0052-0053 Remark 2.4 completing-square identity; checked over integer triples in "
       "v3_card_numbers.py (True); T.")
ok(81, "L05 0061-0064 Theorem 3.1 hypotheses (Q PSD, mu >= 0, complementary slackness) and proof; T.")
ok(82, "L05 0065-0066 Remark 3.2: mu=-1 from x-1-mu=0, f(0)=0, f(1)=-1/2; T.")
ok(83, "L05 0067-0068 Definition 3.3 S-candidate and its independence hypotheses; T.")
ok(84, "L05 0069-0072 Proposition 3.4 hypotheses (Q PD, midpoint convex) and midpoint identity; T.")
ok(85, "L05 0073-0074 Remark 3.5: midpoint of nonnegative vectors feasible; Q of Part B PD (checked by hand); T.")
ok(86, "L05 0075-0076 Example 3.6: xbar=(3/2,0), mu=(0,5/2), f=-9/4; recomputed (v3_card_numbers.py); T.")
bad(87, "L05 0239 prints x = (13/19, 3/19, 3/19), recomputed exactly; card basis 'Lab 1, Part A (exact "
        "arithmetic)' omits SIMULATED while L01 0078 and L03 0064 label the same kind of hand-chosen inputs; "
        "see E-S13.", SIM_L05_FIX)
bad(88, "L05 0243 prints 0.7631578947; 551/722 = 29/38 recomputed; E1 0302-0304 agrees; basis lacks SIMULATED "
        "while the same kind of inputs are labelled elsewhere in M7; see E-S13.", SIM_L05_FIX)
bad(89, "L05 0246-0251 lab output: only {2} passes both tests; recomputed by v3_card_numbers.py; basis lacks "
        "SIMULATED; see E-S13.", SIM_L05_FIX)
ok(90, "L05 0067-0068 Definition 3.3 'all 2^p sets'; 0262 four candidates for p = 2; T.")
ok(91, "L05 0266-0267 misconception 1, Q = diag(1,-1): f(0,t) = -t^2/2; T.")
ok(92, "L05 0268-0269 misconception 2 with Remark 3.2 and Theorem 3.1 (mu >= 0 needed); T.")
bad(93, "L05 0270-0271 misconception 3; gradient -A'lambda with lambda = (-36/19, 11/19) recomputed "
        "(grad = (36/19, 25/19, 47/19)); card basis 'Lab 1, Part A (exact arithmetic)' lacks SIMULATED; "
        "see E-S13.", SIM_L05_FIX)
ok(166, "L05 0053 Remark 2.4: v=(-2,1,1), Av = 0, v'Qv = 19 recomputed; T.")
bad(171, "L05 0238 prints kkt_determinant 19 (recomputed); basis 'Lab 1, Part A (exact arithmetic)' lacks "
         "SIMULATED; see E-S13.", SIM_L05_FIX)
bad(172, "L05 0255-0257 lab output 1089 grid points, 0 below -9/4 (recomputed); basis "
         "'Lab 1, Part B (...)' lacks SIMULATED; see E-S13.", SIM_L05_FIX)
bad(182, "L05 0240 prints lambda = (-36/19, 11/19) (recomputed); basis lacks SIMULATED; see E-S13.", SIM_L05_FIX)
ok(198, "L05 0055 active set of a feasible point; T.")

# ---- L06 -----------------------------------------------------------------------------------------
ok(97, "L06 0022 and 0024 Definition 1.1 f_gamma and the risk-term sentence; T.")
ok(98, "L06 0026 Definition 1.2 and QP data Q = gamma Sigma, c = -mu, A = 1', b = 1; T.")
ok(99, "L06 0022 (inputs given, not estimated), 0063 and 0065 (SIMULATED, seeded); T.")
ok(100, "L06 0027-0032 Theorem 1.3 statement and proof (0031-0032); the KKT solve for the same problem, "
        "recomputed exactly at five gammas by v3_l06_numbers.py, gives the printed weights; T.")
ok(101, "L06 0033-0034 Remark 1.4: Sigma = M'M/16 + I/10 positive definite; T.")
ok(102, "L06 0037-0042 Proposition 2.1 monotonicity of V and R; proof checked; T.")
ok(103, "L06 0045-0048 Proposition 2.3 (F+ subset of F0 gives inf over F+ >= inf over F0); T.")
ok(104, "L06 0050-0051 Definition 3.1 (linear constraint, box, sector, nonnegativity as box with l=0); T.")
ok(105, "L06 0052-0053 Definition 3.2 turnover and turnover constraint; T.")
ok(106, "L06 0054-0055 Remark 3.3 (absolute value is a pair of linear inequalities); T.")
ok(107, "L06 0060-0061 Remark 3.5 (variables (w,t) enter linearly; PSD Hessian on w block); T.")
ok(108, "L06 0240 printed mu 7/100 1/20 3/25 1/50 (decimals 0.07, 0.05, 0.12, 0.02 recomputed); "
        "docstring 0065 SIMULATED; grade C.")
ok(109, "L06 0241 printed diagonal 49/40, 27/20, 103/80, 103/80 recomputed (v3_l06_numbers.py); grade C.")
ok(110, "L06 0244-0245 printed return 0.113798 and risk 0.123809 at gamma=1, recomputed; grade C.")
ok(111, "L06 0245, 0247, 0249, 0251, 0253 weight on A4 negative at all five gammas (recomputed); grade C.")
ok(112, "L06 0255, 0258, 0261, 0264, 0267 zero set {A4} at every gamma (recomputed); grade C.")
ok(113, "L06 0257, 0260, 0263, 0266, 0269 'True' and recomputed objectives at each gamma; grade C.")
ok(114, "L06 0271 prints 0.558861; exact turnover 67597/120955 = 0.55886073 recomputed "
        "(v3_l06_numbers.py); six-place weights give 0.55886 (E3 0326-0328); grade C.")
ok(115, "L06 0282-0283 misconception 1; returns 0.113798 (0244) and 0.106241 (0252) recomputed; grade C.")
ok(116, "L06 0284-0285 misconception 2; weights at gamma=1 (0245, 0256) recomputed; grade C.")
ok(117, "L06 0286-0287 misconception 3; Proposition 3.4 (0056-0057) and Part D lines 0272-0273; T.")
ok(118, "L06 0243-0253 lab output 'True True' at all five gammas; KKT solve recomputed at five gammas "
        "(v3_l06_numbers.py) gives the printed weights; grade C.")
ok(163, "L06 0056-0057 Proposition 3.4 'no sign assumption on w, w0 or tau'; T.")
ok(164, "L06 0043-0044 Remark 2.2 (argument covers the w >= 0 problem); T.")
ok(167, "L06 0028-0030 Theorem 1.3, proof 0032 (1'z = z'Sigma z > 0); P2 0308-0311; T.")
ok(174, "L06 0255, 0258, 0261, 0264, 0267 candidates_passing = 1 at each gamma (recomputed kept = 1); grade C.")

# ---- L07 -----------------------------------------------------------------------------------------
ok(121, "L07 0023-0024 Definition 1.1 data of the finite-horizon problem; T.")
ok(122, "L07 0025-0030 Definition 1.2 (plans, total reward J_t, value V_t, optimal plan); T.")
ok(123, "L07 0031-0032 Remark 1.3 (A(s)=(0,1), value 1 not attained); T.")
ok(124, "L07 0033-0034 Definition 1.4 continuation; T.")
ok(125, "L07 0037-0041 Theorem 2.1 (backward recursion) and proof 0043-0052; T.")
ok(126, "L07 0053-0061 Theorem 2.2 (principle of optimality) and proof; T.")
ok(127, "L07 0062-0069 Theorem 2.3 (i) and (ii) and proof; T.")
ok(128, "L07 0070-0073 Corollary 2.4 and induction proof; T.")
ok(129, "L07 0217-0218 Remark 2.5: V_0(x)=1 attained only by b; (a,c) earns 0; recomputed by hand; T.")
ok(130, "L07 0197-0201 Part A W400 column 240, 220, 200, 130, 4; DP table recomputed "
        "(v3_card_numbers.py); grade C, SIMULATED basis.")
ok(131, "L07 0203-0204 recursion_matches_brute_force True; loop over t = 0..3 and five states = 20 pairs "
        "(0172-0177); grade C.")
ok(132, "L07 0203 prints 70; feasible sequences from 400 counted = 70 = C(8,4) (v3_card_numbers.py); "
        "E3 0268-0271; grade C.")
ok(133, "L07 0206-0209 lab output: optimal consumption 100 x4, path 400..0, total 240, tails optimal; "
        "total 240 agrees with the DP table recomputed in v3_card_numbers.py (L07 section); grade C.")
ok(135, "L07 0225-0226 misconception 1; REWARD[400] = 130 and greedy total 130 (0211); grade C.")
ok(136, "L07 0227-0228 misconception 2, Remark 2.5 and Part C greedy tails 0212-0215; grade C.")
ok(137, "L07 0229-0230 misconception 3; wealth-400 values 240 (t=0) and 130 (t=3) at 0197 and 0200; grade C.")

# ---- L08 -----------------------------------------------------------------------------------------
ok(142, "L08 0024-0028 Definition 1.1 discounted total and value; T.")
ok(143, "L08 0029-0034 Definition 1.2 Bellman equation system (U_H = B, max recursion); T.")
ok(144, "L08 0035-0042 Theorem 1.3 statement (beta >= 0) and proof; T.")
ok(145, "L08 0043-0050 Theorem 1.4 statement (uniqueness with terminal condition) and proof; T.")
ok(147, "L08 0055-0060 Definition 2.1 Bellman operator G and value iteration; T.")
ok(148, "L08 0061-0064 Lemma 2.2 time shift and proof; T.")
ok(149, "L08 0065-0068 Proposition 2.3 statement and induction proof; T.")
ok(150, "L08 0182-0183 code compares iterates[n] with values[H-n] for n = 0..6; output 0210 "
        "'iterate_equals_n_period_recursion True'; grade C.")
ok(151, "L08 0186 prints V0 = 13.948890; recomputed as 1394889/100000 (v3_card_numbers.py); grade C.")
ok(152, "L08 0199 tied_pairs_t0_to_5 0; grade C.")
ok(153, "L08 0201 plans_enumerated 378 = 3(2^6+...+2^1) recomputed; E3 0263-0265; grade C.")
ok(154, "L08 0204-0209 changes 6.0, 3.6, 2.74, 2.466, 2.2194, 1.99746 recomputed exactly; ratio 0.9 from n=3 on "
        "(E2 0259-0261); grade C.")
ok(155, "L08 0219-0220 misconception 1 with Definition 2.1; U^1 = 1 + U^0 recomputed; T.")
ok(156, "L08 0221-0222 misconception 2 with Remark 1.5 (0052) and Theorem 1.4; T.")
ok(157, "L08 0223-0224 misconception 3; policy lines 0193-0198 (s2 repair t=0..3, run t=4,5); grade C.")
ok(162, "L08 0069-0070 Remark 2.4 and Problem R3 0275-0278; T.")
ok(175, "L08 0202 recursion_matches_brute_force True over 18 (t,s) pairs (code 0167-0171); grade C.")
bad(186, "L08 0216 gives the beta = -1 counterexample: V_0 = 1 while U_0 = 0, which refutes Theorem 1.3 only. "
         "The card's answer 'No' for Theorem 1.4 and its 'They need beta >= 0' are not shown on the page. "
         "(Checked by hand: (U_0,U_1,U_2) = (0,1,0) solves the system with U_2 = B and U_0 != V_0, so the "
         "claim is true but not supported by the lesson text.)",
    "Narrow the back to Theorem 1.3, or add to L08 section 3 (after 0216) the solution (0,1,0) of the Bellman "
    "system with U_2 = B for beta = -1, which differs from V_0 = 1, and cite it on the card.")
ok(199, "L08 0193-0198 policy lines print s0=run and s1=run for t = 0..5; grade C.")

# ---- removed in round 3 (ids carried from round 2) ----------------------------------------------
REMOVED = [10, 48, 134, 146, 180, 188]
removed_ev = ("Card removed at pin a007712f: no entry with this id in course/modules/M/M7/cards.json "
              "(v3_card_scan.py lists the ids present); nothing remains to verify. Round-2 row kept.")

rows = []
for c in cards:
    n = int(c["id"].split("c")[1])
    if n not in E:
        raise SystemExit(f"no evidence entry for {c['id']}")
    status, ev, fix = E[n]
    row = {
        "id": f"E-c{n:03d}",
        "check": "card-vs-lesson: front, back, grade, basis, locator, numbers, SIMULATED label",
        "location": f"course/modules/M/M7/cards.json ({c['id']}, lesson {c['lesson']}, grade {c['grade']})",
        "status": status,
        "evidence": ev,
    }
    if status != PASS:
        row["fix"] = fix
    rows.append(row)
for n in REMOVED:
    rows.append({
        "id": f"E-c{n:03d}",
        "check": "card-vs-lesson (round-2 id; card removed in round 3)",
        "location": f"course/modules/M/M7/cards.json (M7-c{n:03d}: absent at pin a007712f)",
        "status": PASS,
        "evidence": removed_ev,
    })

slice_rows = [
    ("E-S01", "unit gate: check_pages", "course/modules/M/M7/ (check_pages.py --unit M7)", PASS,
     "ran .venv/bin/python tools/check_pages.py --unit M7 -> 'check_pages M7: PASS' (v3_outputs/check_pages.out)."),
    ("E-S02", "unit gate: check_dag, check_projects, run_labs", "tools/check_dag.py, check_projects.py, run_labs.py --unit M7", PASS,
     "outputs 'check_dag M7: PASS', 'check_projects M7: PASS', 'run_labs M7: PASS (11/11)' (v3_outputs/*.out)."),
    ("E-S03", "lab twins under python -I -W error; expected block equals output",
     "tests/labs/M7/lab-M7-L01-1.py .. lab-M7-L08-1.py; course/modules/M/M7/L01..L08.html expected blocks", PASS,
     "all eight twins exit 0 under python -I -W error; v3_expected_vs_output.py: every page expected block MATCHes the twin output (v3_outputs/expected_vs_output.out). Page code vs twin not compared here (lab slice)."),
    ("E-S04", "every number a card states recomputed independently",
     "ledgers/M7/scripts/M7-e-r3/v3_card_numbers.py; v3_l06_numbers.py", PASS,
     "L01-L08 figures (3125, 2573, 552, 184, 177/55, 177/110, 47/55, 17/55, -9/55, 36 of 36, 27951, 7/300, -199/300, 199/150, 19, 13/19, 3/19, -36/19, 11/19, 551/722, 1089, 70, 378, 240/220/200/130/4, 13.948890, 0.558861 from exact 0.5588607) match the cards (outputs in v3_outputs/card_numbers.out and l06_numbers.out)."),
    ("E-S05", "every number on a card occurs in its lesson page",
     "ledgers/M7/scripts/M7-e-r3/v3_card_numbers_in_lesson.py", PASS,
     "one token '00' flagged from 'W400' is a regex artefact; every other numeric token occurs in the card's own lesson HTML (v3_outputs/card_numbers_in_lesson.out)."),
    ("E-S06", "banned phrases and process words in cards",
     "ledgers/M7/scripts/M7-e-r3/v3_card_scan.py", PASS,
     "no banned phrase (TODO, TBD, lorem, studies show, clearly, ...); 'round' occurs only in 'rounds' and 'around'; '...' occurs only as mathematical sequence notation, e.g. (a_t, ..., a_{H-1}) (v3_outputs/card_scan.out)."),
    ("E-S07", "duplicates and near-duplicates in cards",
     "ledgers/M7/scripts/M7-e-r3/v3_card_scan.py", PASS,
     "174 unique ids; no identical fronts; token-Jaccard >= 0.5 pairs reviewed one by one: each pair asks a different fact (different lesson, different instance, or the definition versus the identity). Ids 10, 34, 35, ... are absent: allowed by Architect ruling 2."),
    ("E-S08", "grade and basis rules (BLUEPRINT 3; BUILDER_RULES 7)",
     "cards.json grades: 126 T (no basis), 48 C (all with basis)", PASS,
     "every C card names its lab in basis; no T card carries a basis; C cards from L01-L04 and L06-L08 carry SIMULATED (rows above); L05 handled in E-S13."),
    ("E-S09", "coverage: each definition, theorem, proposition, lemma, remark, misconception and key-results row has a card",
     "course/modules/M/M7/L01..L08.html sections 4-7 (key-results tables)", PASS,
     "checked lesson by lesson: every Definition, Theorem, Proposition, Lemma, Remark and Example in the key-results tables, all three misconceptions of each lesson, and each lab's key-result row has at least one card (e.g. L05 Lemma 1.3 c075, Prop 2.1 c077, Thm 2.3 c079, Thm 3.1 c081, Prop 3.4 c084, Example 3.6 c086)."),
    ("E-S10", "theorem and proposition cards carry the lesson's hypotheses",
     "theorem-type cards (c004-c008, c018, c021, c022, c024, c040-c042, c057-c061, c075-c081, c084, c100-c103, c125-c128, c144-c149)", PASS,
     "each card states the stated hypotheses (for example Prop 3.4 'Q positive definite, F midpoint convex'; Thm 2.1 'f and g_i convex and differentiable, h_j affine'; Thm 1.3 (L08) 'beta >= 0')."),
    ("E-S11", "round-2 failing rows (M7-c012, c049, c050, c063, c170, c173, c178, c189)",
     "cards.json entries listed", PASS,
     "round 2 failed these for a missing SIMULATED label; each now carries '(SIMULATED)' in basis and is re-verified above (rows E-c012, E-c049, E-c050, E-c063, E-c170, E-c173, E-c178, E-c189)."),
    ("E-S12", "lab SIMULATED labels in the lesson pages that cards cite",
     "course/modules/M/M7/L01.html (docstring line 0078), L02 (0075), L03 (lesson 0064, docstring 0073-0074), L04 (0061), L06 (0063, 0065), L07 (0077), L08 (0072, 0074)", PASS,
     "each of these labs states SIMULATED for its hand-chosen or generated inputs, so the cards that cite them may carry SIMULATED."),
    ("E-S13", "SIMULATED label consistency for the L05 lab (hand-chosen integers)",
     "course/modules/M/M7/L05.html lab hypothesis line 0079 and docstring line 0081", FAIL,
     "L05 says 'The inputs are small integers chosen for this lab, not data' (0079) and 'Inputs are small hand-chosen integers, not data' (0081). L01 (docstring 0078) and L03 (lesson 0064; docstring 0073-0074) label hand-chosen illustrative inputs SIMULATED. BLUEPRINT 5.3 ('Simulated data is always labelled SIMULATED') and BUILDER_RULES 1.7 ('Simulated data carries a visible SIMULATED label') apply. The same kind of input is labelled differently inside M7. Round 2 passed this; round 3 fails it on the unit's own convention (judgment, stated in notes)."),
    ("E-S14", "notation against notation/notation.json",
     "notation/notation.json (macros, symbols)", PASS,
     "cards are plain text; they use none of the registered symbols (T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, Q-blackboard) and none with another meaning. The registry's 'about' field makes mu, gamma, beta and sigma local to each lesson, so the L05 mu (inequality multiplier) and the L03/L06 mu (return vector) are local, not a registry collision."),
    ("E-S15", "DAG: cards use only prerequisite or own-unit concepts",
     "cards.json (concept words) against the M7 prerequisite closure in plans/M7-build-plan.md section 2", PASS,
     "cards name Hessian, PSD matrix, spectral theorem, implicit function theorem only as Assumption 1 from M2/M3 (c008, c018, c179); no card names covariance, dynamic programming, contraction or efficient frontier."),
    ("E-S16", "atomicity: one fact per card (BUILDER_RULES 7)",
     "cards.json fronts with compound questions (listed by a front scan)", PASS,
     "compound fronts (for example c122, c142, c041, c147) each draw on one lesson block (one definition or one lemma); no card asks two unrelated facts. Judgment; the single defect in this class is c186 (two theorems, row E-c186)."),
    ("E-S17", "registry keys cited by cards",
     "cards.json cite field", PASS,
     "all 174 cards have cite None; no registry key is cited by any card, so verify_refs has no card-level subject. verify_refs was not run."),
]
for rid, check, loc, st, ev in slice_rows:
    row = {"id": rid, "check": check, "location": loc, "status": st, "evidence": ev}
    if st != PASS:
        row["fix"] = ("Relabel the L05 lab as SIMULATED in its hypothesis (line 0079) and docstring (line 0081), "
                      "stating that the integers are hand-chosen illustrative inputs; then add SIMULATED to "
                      "the seven L05 card bases (M7-c087, c088, c089, c093, c171, c172, c182). Alternatively, if the "
                      "architect rules that hand-chosen integers are not simulated data, record that ruling and "
                      "make L01 and L03 consistent with it.")
    rows.append(row)

from collections import Counter

counts = Counter(r["status"] for r in rows)
now = datetime.now(UTC).replace(microsecond=0).isoformat()
fragment = {
    "unit": "M7",
    "slice": "e",
    "round": 3,
    "verifier": "Claude Haiku 5.5, independent verifier for M7-e, round 3 (did not build M7; read all eight lessons line by line and every card of cards.json at a007712f)",
    "pin": "a007712f",
    "base": "c737272f (round-2 pin). Delta for this slice: cards.json only (6 entries removed: M7-c010, c048, c134, c146, c180, c188; 10 added: c190-c199; 21 entries changed). L01.html to L08.html, tests/labs/M7 and notation/ are byte-identical to c737272f.",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyD3-M7-e",
    "scratch": "/tmp/m7e-r3-v (lesson text extracts; regenerable with ledgers/M7/scripts/M7-e-r3/v3_extract_text.py; copies in ledgers/M7/scripts/M7-e-r3/v3_text/)",
    "verified_at": now,
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "Every card of the current cards.json (174) was read against its lesson text and re-checked; no round-2 PASS row was carried. "
        "Locators 'Lnn 0023' are line numbers of v3_extract_text.py output for L0n.html (copies in v3_text/). "
        "Lab outputs were produced by running each twin under python -I -W error (copies in v3_labout/). "
        "Round-2 FAIL rows are fixed: the basis of M7-c012, c049, c050, c063, c170, c173, c178 and c189 now carries SIMULATED. "
        "Judgment call (E-S13): round 2 treated the L05 lab's hand-chosen integers as not needing a SIMULATED label. This round "
        "fails the seven L05 lab-result cards because L01 and L03 label the same kind of input SIMULATED. The pre-existing, untracked "
        "ledgers/M7/M7-e.json and ledgers/M7/scripts/M7-e-r3/ (non-v3_ files) in this checkout came from an earlier run; they were not used as evidence, and this file overwrites that fragment. "
        "Not checked: page_smoke (Chromium/Pyodide, lesson gate); page code versus twin text; verify_refs (no card cites a key); ruff and mypy (no Python file in slice e); pytest; the rendered card deck (course/review.html); the mutation test (not applicable: slice e is cards and lessons, not a project grader)."
    ),
    "summary": (
        f"M7-e round 3 (pin a007712f): {len(rows)} rows (pass={counts['PASS']}, fail={counts['FAIL']}). "
        "FAIL: M7-c186 (Theorem 1.4 claim not supported by the lesson text) and the SIMULATED label on the seven L05 lab-result cards "
        "(M7-c087, c088, c089, c093, c171, c172, c182), with the root cause at L05.html lines 0079/0081 (row E-S13)."
    ),
}

out = ROOT / "ledgers/M7/M7-e.json"
out.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out, "rows", len(rows), dict(counts))
