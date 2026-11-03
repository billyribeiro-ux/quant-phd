"""Build ledgers/E3/E3-f.json (round 4, E3 slice f) from the per-card verdicts below. Run with python -I from the checkout root."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
CARDS = {c["id"]: c for c in json.loads((ROOT / "course/modules/E/E3/cards.json").read_text(encoding="utf-8"))}
LINE = {}
for i, l in enumerate((ROOT / "course/modules/E/E3/cards.json").read_text(encoding="utf-8").splitlines(), 1):
    if '"id": "E3-c' in l:
        LINE[l.split('"id": "')[1].split('"')[0]] = i

S = "ledgers/E3/scripts/E3-f-r4/"
P = "PASS"
F = "FAIL"
# card id -> (status, evidence, fix)
V = {
 "E3-c001": (P, "cards.json:3 read in full. Lesson L01.html:58-60 (Definition 1.1): finite list, distinct real outcomes, p_i >= 0, sum 1; random-variable equivalence matches."),
 "E3-c002": (P, "cards.json:9. L01.html:63-65 (Definition 1.2): E X = sum p_i x_i. Recomputed exactly: EV of A = 150 CU (" + S + "recompute_numbers.out)."),
 "E3-c003": (P, "cards.json:15. L01.html:68-70 (Definition 1.3): E u(X) = sum p_i u(x_i); depends on u and on the lottery."),
 "E3-c004": (P, "cards.json:21. L01.html:73-75 (Assumption A1) and section 4 L01.html:329-334 (finitely many outcomes; no result for a continuum). Card matches."),
 "E3-c005": (P, "cards.json:27. L01.html:85-88 (Definition 2.1): mixture on the union of outcomes, p_L(x) = 0 off the outcomes of L. Matches."),
 "E3-c006": (P, "cards.json:33. L01.html:142-144 (Definition 3.2): u = bx, b > 0; E u = b E X by Proposition 3.1."),
 "E3-c007": (P, "cards.json:39. L01.html:90-93 (Proposition 2.2, T, under A1) and proof L01.html:95-101: finite union, non-negative weights, sum 1. Hypothesis A1 stated on card."),
 "E3-c008": (P, "cards.json:46. L01.html:104-109 (Proposition 2.3, T, under A1, u real-valued) and proof L01.html:112-121. Linearity in probabilities; hypotheses stated; Lab 1 Part B prints six True (expected block L01.html:302-310)."),
 "E3-c009": (P, "cards.json:53. L01.html:125-127 (Remark 2.4): identity about Definition 1.3, no claim on preference orderings. Matches."),
 "E3-c010": (P, "cards.json:60. L01.html:132-135 (Proposition 3.1, T, A1) and proof L01.html:137-140: E u = a + b E X; a = 0, b = 1 gives E X."),
 "E3-c011": (P, "cards.json:67. L01.html:147-150 (Proposition 3.3, T, A1, b > 0) and proof L01.html:152-155. Matches."),
 "E3-c012": (P, "cards.json:74. L01.html:395-400 (Problem P2): b < 0 reverses the ranking, proof by the sign of b; the card's A1 is the lesson's standing finite-lottery setting."),
 "E3-c013": (P, "cards.json:81. L01.html:438-443 (Problem R1 solution): E u(X) <= m with equality only when all probability sits on maximisers; finite set; key-results row L01.html:461-476."),
 "E3-c014": (P, "cards.json:88. L01.html:78-80 (Example 1.4) and misconception 1 at L01.html:341-343: u(E X) = 150^2 = 22500 CU^2, E u(X) = 45000 CU^2 (recomputed exactly; ratio 2 as the page says)."),
 "E3-c015": (P, "cards.json:95. L01.html:345-347 (misconception 2) and Definitions 1.2 and 3.2 (L01.html:63-65, 142-144): E u = b E X, probability-weighted."),
 "E3-c016": (P, "cards.json:102 (C, basis Lab 1 part A). Expected block L01.html:302-304 prints EV 15000, 12500, 15000 and quadratic EU 45000, 21250, 37500. Recomputed with Fractions (" + S + "recompute_numbers.out, lines c016). Twin output identical (" + S + "twins/expected_vs_twin.out)."),
 "E3-c017": (P, "cards.json:110 (C, basis Lab 1 part B). Code L01.html:164+ Part B alpha in 1/4, 1/3, 1/2 under linear and quadratic; expected block prints six 'equal True' lines and all_linearity_checks True (L01.html:302-313)."),
 "E3-c018": (P, "cards.json:118. L02.html:73-76 (Assumption A2): u twice differentiable on open I, u' > 0, u'' <= 0; concavity by the sign of u''."),
 "E3-c019": (P, "cards.json:124. L02.html:88-96 (Proposition 1.1, T) and proof: weighted average in u(I), an interval by F1; strictly increasing by F5; hypotheses F1, F5, A1 to A3 match."),
 "E3-c020": (P, "cards.json:131. L02.html:98-101 (Definition 1.2): unique c with u(c) = E u(X), written CE(X; u)."),
 "E3-c021": (P, "cards.json:137 (round-3 FAIL, now fixed). L02.html:98-101 (Definition 1.2) and L02.html:99: 'On this page, the risk premium is the certainty-equivalent risk premium, and nothing else.' Every use of 'risk premium' in L02.html (lines 51, 98-99, 162-164, 218, 398, 420, 511, 561) is in this sense. Card now reads 'on this page'; scope matches."),
 "E3-c022": (P, "cards.json:143. L02.html:103-108 (Proposition 1.3(a), T; Assuming F1, F2, F5, under A1 to A3) and proof L02.html:110-128 (tangent line above u, averaged). Matches."),
 "E3-c023": (P, "cards.json:150. L02.html:103-108 (Proposition 1.3(b)) and A4 at L02.html:83-85; strict inequality needs u'' < 0 and an outcome with positive probability differing from E X. Matches."),
 "E3-c024": (P, "cards.json:157. L02.html:143-146 (Definition 2.1): r_A = -u''/u' in 1/CU where u' != 0; r_R = w r_A dimensionless. Matches."),
 "E3-c025": (P, "cards.json:163. L02.html:148-151 (Proposition 2.2, T, b > 0) and proof L02.html:153-155: v' = b u', v'' = b u''; b cancels. Matches."),
 "E3-c026": (P, "cards.json:170. L02.html:158-160 (Example 2.3) with F6 (L02.html:56-66): r_A = 1/(2w), r_R = 1/2; at w = 100, r_A = 0.005, r_R = 0.5 (recomputed; expected block L02.html:365-367 prints 0.005000 and 0.500000)."),
 "E3-c027": (P, "cards.json:177. L02.html:172-175 (Proposition 3.1, T; F1, F3, F4, F5; A1, A5) and proof L02.html:177-201: pi/eps^2 -> (1/2) r_A s^2 with s^2 = Var(X) for E X = 0. Hypotheses match; A5 at L02.html:167-170."),
 "E3-c028": (P, "cards.json:184. L02.html:203-205 (Remark 3.2): asymptotic statement; no bound at a fixed eps. Matches."),
 "E3-c029": (P, "cards.json:191. L02.html:397-399 (misconception 1): half-variance 900 CU^2 (1/2 x 1800), Pratt 4.5 CU (1/2 x 0.005 x 1800), exact 5.065835 CU (recomputed in " + S + "recompute_numbers.out). Units as the page writes them."),
 "E3-c030": (P, "cards.json:198. L02.html:402-404 (misconception 2) and Example 2.3 (L02.html:158-160); F6 assumed (L02.html:56-66). r_A 0.005 per CU, r_R 0.5 at w = 100 recomputed."),
 "E3-c031": (F, "cards.json:205. Scope word 'every' ('CE(X; u) = E X for every finite lottery') without its hypothesis. The derivation (L02.html:451-456, Problem P2) takes X with outcomes in I, and CE(X; u) is defined only under A3 (L02.html:78-80: every outcome lies in I). The card drops that hypothesis; the same unqualified sentence is misconception 3 at L02.html:405-407. Card claim is correct only for finite lotteries with outcomes in I.",
     "Change the back to: 'For u(w) = w and a finite lottery with outcomes in I (A3), CE(X; u) = E X, so the premium is zero whatever the gamble (Problem P2).' Optionally make L02.html:407 say 'for every finite lottery with outcomes in I'."),
 "E3-c032": (P, "cards.json:212 (C, basis Lab 1 part A). Expected block L02.html:367 prints ce_cents 9493, premium_cents 507, r_A 0.005000, r_R 0.500000, exact 5.065835, Pratt 4.500000, error 0.565835. Recomputed: CE = 94.9341649 CU -> 9493 cents; premium 5.0658351 -> 507 half up."),
 "E3-c033": (P, "cards.json:220 (C, basis Lab 1 part B). Expected block L02.html:369-375 prints premium/eps^2 5.065835 (eps 1) to 4.500046 (eps 0.01) and gaps_shrink_as_eps_falls True. Recomputed at five scales (" + S + "recompute_numbers.out)."),
 "E3-c034": (P, "cards.json:228 (C, basis Lab 1 part A). 0.565835 / 5.065835 = 0.1116963 -> 11.17 percent of the exact premium (basis stated as the exact premium). L02.html:384-388 (section 4) and E2 solution L02.html:476-481 state the same. Recomputed (" + S + "recompute_numbers.out)."),
 "E3-c035": (P, "cards.json:236 (C, basis Lab 1 part C). Code Part C and expected block L02.html:376-380: linear premium 0 cents at eps 1.0, 0.5, 0.1; linear_premium_zero_at_three_scales True."),
 "E3-c159": (F, "cards.json:1058. The card answers 'which hypotheses does the proof of Proposition 1.3 use' with A2, F5, F2, F1, A3, and omits A1. Proposition 1.3 is stated under A1 to A3 (L02.html:103-104), and its proof uses A1 in Step 2 (the weighted average and 'sum_i p_i (x_i - m) = 0' are finite sums over the outcomes, L02.html:110-128). Remark 1.4 (L02.html:130-134) repeats the same omission. Card answer is incomplete.",
     "Add A1 to the back: '... and A1 for the finite sums in Step 2 (and A3 to place the outcomes and their mean in I).' Also add A1 to Remark 1.4 at L02.html:131 (lesson owner; out of slice)."),
 "E3-c161": (P, "cards.json:1072 (C, basis Lab 1 part B). Interpretation L02.html:381 and Part B code: five scales are a numerical check; the card says it is not a proof of the limit in Proposition 3.1 (Problem R2, L02.html:501-506)."),
 "E3-c162": (P, "cards.json:1080. L02.html:130-134 (Remark 1.4, last sentence): for u'' >= 0 Steps 1 to 3 reverse, and this lesson does not state that case as a result. Matches."),
 "E3-c174": (P, "cards.json:1163. L02.html:167-170 (Assumption A5): u twice differentiable on open I containing w, u' > 0 on I; small eps keeps w + eps x_i in I (A5 text 'every eps small enough'). Matches."),
 "E3-c036": (P, "cards.json:244. L03.html:72-75 (Definition 1.1): w^a = e^(a ln w) for w > 0, ln of M1 Lesson 3. Matches."),
 "E3-c037": (P, "cards.json:250. L03.html:77-80 (Proposition 1.2, T) and proof L03.html:82-85: (w^a)^b = w^(ab); (xy)^c = x^c y^c for positive x, y. Matches."),
 "E3-c038": (P, "cards.json:257. L03.html:87-90 (Definition 1.3): u_gamma = (w^(1-gamma) - 1)/(1-gamma) for gamma != 1, u_1 = ln w, w > 0. Matches."),
 "E3-c039": (P, "cards.json:263 (round-3 wording replaced). L03.html:87-92 (Definition 1.3 paragraph): 'The subtracted 1 makes u_gamma(1) = 0 for every gamma.' Derivation: (1 - 1)/(1 - gamma) = 0 for gamma != 1 and ln 1 = 0 at gamma = 1. The card no longer makes the A2 claim, so no hypothesis is needed. Matches."),
 "E3-c040": (P, "cards.json:270. L03.html:94-96 (Proposition 1.4, assuming A2) and proof L03.html:99-103: u_gamma(w) = ln w (e^h - 1)/h with h = s ln w -> ln w. Recomputed identity; card hypotheses match."),
 "E3-c041": (P, "cards.json:277. L03.html:116-118 (Proposition 1.7, assuming F2) and proof L03.html:121-123: u' = w^(-gamma), u'' = -gamma w^(-gamma-1), r_A = gamma/w, r_R = gamma. Matches."),
 "E3-c043": (P, "cards.json:284. L03.html:128-130 (Theorem 2.1; F1, F2, A3, A4) and proof L03.html:133-136: u = K u_gamma + C, K > 0. Hypotheses match."),
 "E3-c044": (P, "cards.json:291. L03.html:138-140 (Remark 2.2): the theorem does not say an investor has CRRA; no source cited. Matches."),
 "E3-c045": (P, "cards.json:298. L03.html:143-145 (Definition 2.3): positive outcomes so each lies in the domain of A1 (wealth above zero, L03.html:56-62). Matches the lesson's A1."),
 "E3-c046": (P, "cards.json:304. L03.html:148-151 (Proposition 2.4, T) and proof L03.html:153-156: gamma != 1: CE = M^(1/s); gamma = 1: exp(sum p ln x). Matches."),
 "E3-c047": (P, "cards.json:311. L03.html:158-160 (Example 2.5): 1600 cents at gamma = 2 (M = 1/1600) and 2000 cents at gamma = 1 (sqrt(4e6)). Recomputed exactly (" + S + "recompute_numbers.out)."),
 "E3-c048": (P, "cards.json:318. L03.html:163-166 (Proposition 2.6, T; positive outcomes, k > 0, every real gamma) and proof L03.html:168-171: (kx)^s = k^s x^s. Matches."),
 "E3-c049": (P, "cards.json:325. L03.html:173-175 (Proposition 2.7, T; a > 0, real b; CE under u exists and is unique) and proof L03.html:178-180. Matches."),
 "E3-c050": (P, "cards.json:332. L03.html:183-185 (Remark 2.8): compute once as a float, round half up, floor(v + 1/2) for v >= 0, not an intermediate value. Matches."),
 "E3-c051": (P, "cards.json:338. L03.html:344-346 (misconception 1) with Proposition 1.7 (L03.html:116-118): r_R constant; r_A = gamma/w falls when gamma > 0. Assumes F2 as the lesson does. Matches."),
 "E3-c052": (P, "cards.json:345. L03.html:106-109 (Example 1.5): u_0(w) = w - 1 affine with slope 1; ranks as w (L01.html:147-150, Proposition 3.3; L01 Definition 3.2 at L01.html:142-144). Matches."),
 "E3-c053": (P, "cards.json:352. L03.html:326-328 (interpretation: finite checks) and Problem R3 (L03.html:454-460): Lab 1 checks six exponents (GAMMAS has six values, code L03.html:190+) for one lottery; a proof needs a general argument. Grade T for the meta-claim, a logical point about finite checks."),
 "E3-c054": (P, "cards.json:359 (C, basis Lab 1). Expected block L03.html:307-318 prints gamma 0: 11250.0000; gamma 1: 10000.0000; gamma 2: 8888.8889; gamma 4: 7337.6161; recomputed (" + S + "recompute_numbers.out). Prints 'falls as gamma rises' True."),
 "E3-c055": (P, "cards.json:367. L03.html:148-151 (Proposition 2.4) and Problem E2 (L03.html:422-427, title 'E2 - Checking the exact gamma 2 value'): M = 9/80000, CE = 80000/9 = 8888.888... The lab prints 80000/9 (expected block L03.html:307-318). Recomputed exactly."),
 "E3-c160": (P, "cards.json:1064 (C, basis Lab 1 gamma = 1 +/- 1e-6 line). Code: gap <= 0.01 cents at gamma 1 +/- 1e-6; expected block prints True. Card says only floating-point agreement on one fixed lottery. Matches."),
 "E3-c168": (P, "cards.json:1119. L03.html:183-185 (Remark 2.8): rounding bound |R(kv) - kR(v)| <= (k+1)/2. Triangle inequality on the card's derivation is correct; k = 10 gives 5.5 cents (" + S + "recompute_numbers.out)."),
 "E3-c171": (P, "cards.json:1142 (C, basis Lab 1 homogeneity line). Code tests k = 2, 3, 10 at all six gammas with worst relative error <= 1e-12 and the cents bound; expected block prints 'homogeneity CE(kx) = k CE(x) ... unrounded: True' and the cents bound True (L03.html:307-318)."),
 "E3-c173": (P, "cards.json:1156 (L01). L01.html:349-351 (misconception 3): with b = 0, E v(L) = a for every lottery, every pair ties. Derivation from Definitions 1.1 and 1.3 (sum of p_i = 1). Matches."),
 "E3-c175": (P, "cards.json:1169 (L03). L03.html:56-62 (Assumption A2): the limit (e^h - 1)/h -> 1 is taken as given; M1 Lesson 3 defines e and does not derive the limit. Matches."),
 "E3-c056": (P, "cards.json:374. L04.html:64-66 (Definition 1.1): F_X(t) = P(X <= t) and I_X(t) = integral from minus infinity to t of F_X. Matches."),
 "E3-c057": (P, "cards.json:380. L04.html:69-72 (Lemma 1.2, T, under A1) and proof L04.html:74-77: I_X(t) = E(t - X)^+. Matches."),
 "E3-c058": (P, "cards.json:387. L04.html:79-81 (Definition 1.3): F_X(t) <= F_Y(t) for every real t. Matches."),
 "E3-c059": (P, "cards.json:393. L04.html:84-87 (Definition 1.4): u(s_j) <= u(s_{j+1}). Matches."),
 "E3-c060": (P, "cards.json:399. L04.html:89-92 (Theorem 1.5, T, under A1) and proof L04.html:94-100: F_X <= F_Y everywhere iff E u(X) >= E u(Y) for every nondecreasing u on S. Matches."),
 "E3-c061": (P, "cards.json:406. L04.html:102-105 (Lemma 1.6, T, under A1) and proof L04.html:107-110: enough to check at support points. Matches."),
 "E3-c062": (P, "cards.json:413. L04.html:117-120 (Proposition 1.8, T, under A1, 'holds without A2') and proof L04.html:122-125. Matches."),
 "E3-c063": (P, "cards.json:420. L04.html:129-131 (Definition 2.1): under A1 and A2, I_X(t) <= I_Y(t) for every real t. Matches."),
 "E3-c064": (P, "cards.json:426. L04.html:134-137 (Lemma 2.2, T, under A1 and A2) and proof L04.html:139-142 (D affine between support points; D = 0 for t >= s_m by A2). Matches."),
 "E3-c065": (P, "cards.json:433. L04.html:144-147 (Theorem 2.3, T, under A1 and A2) and proofs L04.html:149-158: for every nondecreasing concave u on S. Matches."),
 "E3-c066": (P, "cards.json:440. L04.html:159-161 (Remark 2.4): only-if proof uses concavity via c_j >= 0 and A2; does not use monotonicity; same conclusion for every concave u on S. Checked against the only-if proof L04.html:149-158. Matches."),
 "E3-c067": (P, "cards.json:447. L04.html:164-170 (Example 2.5): I_X(3000, 4000, 5000) = 500, 1000, 2000; I_Y(2000, 3000, 4000, 5000) = 250, 500, 1250, 2000; means 3000 each. Recomputed exactly (" + S + "recompute_numbers.out) and printed by the named-pair lines in the expected block L04.html:440-456."),
 "E3-c068": (P, "cards.json:454. L04.html:164-170 (Example 2.5): F_X(2000) = 1/2 > 1/4 = F_Y(2000) and F_Y(3000) = 3/4 > 1/2 = F_X(3000); second-order ranking X over Y. Recomputed (" + S + "recompute_numbers.out)."),
 "E3-c070": (P, "cards.json:461. L04.html:112-115 (Example 1.7): F_X = (1/2, 1/2, 1), F_Y = (0, 1/2, 1) on 2000, 3000, 4000; Y dominates X in the first order. Recomputed."),
 "E3-c071": (P, "cards.json:468. Problem R3 (L04.html:613-620): with unequal means, A2 not assumed, nondecreasing concave u: I_X(s_m) = s_m - E X, so I_X <= I_Y at s_m gives E X >= E Y; slope b1 = sigma_{m-1} >= 0 by monotonicity (telescoped slopes). Card statement matches R3."),
 "E3-c072": (P, "cards.json:475. L04.html:502-505 (misconception 1) with Example 2.6 (L04.html:172-175): X = (1000, 5000) and Y = 3000, both mean 3000, no first-order ranking. Matches."),
 "E3-c073": (P, "cards.json:482 (C, basis Lab 1 SIMULATED). Expected block L04.html:440-480 prints pair 16 and pair 19 (equal-mean) with 'SOSD no ranking'; the 8 equal-mean pairs are n = 1, 4, ..., 22 (code kinds cycle). Count 2 of 8 confirmed in the twin output " + S + "twins/L04.out."),
 "E3-c074": (P, "cards.json:490. L04.html:510-512 (misconception 3) with Example 2.5: a second-order ranking without a first-order ranking, so the tests differ. Matches."),
 "E3-c075": (P, "cards.json:497 (C, basis Lab 1 SIMULATED). Expected block prints 'FOSD verdicts over the 24 pairs: {X dominates Y: 3, Y dominates X: 10, identical: 1, no ranking: 10}' and 'agree on 24 of 24 pairs' (L04.html:440-480). Counts sum to 24."),
 "E3-c076": (P, "cards.json:505 (C, basis Lab 1 SIMULATED). Expected block prints 'equal-mean pairs: 8; SOSD verdicts {X dominates Y: 3, Y dominates X: 2, identical: 1, no ranking: 2}' and 'agree on 8 of 8' (L04.html:440-480)."),
 "E3-c077": (P, "cards.json:513. L04.html:489-498 (Section 3): the expected-utility side uses a finite test set; Theorems 1.5 and 2.3 quantify over every nondecreasing or concave utility on S, which the lab does not check. Lab docstring L04.html:179+ says the same. Matches."),
 "E3-c167": (P, "cards.json:1113. L04.html:84-87 (Definition 1.4): concave on S when chord slopes sigma_j are nonincreasing in j = 1..m-1. Matches."),
}
assert set(V) == set(CARDS_IDS := [i for i, c in CARDS.items() if c["lesson"] in ("L01", "L02", "L03", "L04")]), (set(CARDS_IDS) ^ set(V))

rows = []
for cid in sorted(V, key=lambda x: int(x.split("c")[-1])):
    status, evidence = V[cid][0], V[cid][1]
    c = CARDS[cid]
    row = {
        "id": f"E3f-{cid}",
        "check": "2.7-cards",
        "location": f"cards.json:{LINE[cid]} ({cid}, {c['lesson']})",
        "status": status,
        "evidence": evidence,
    }
    if status != P:
        row["fix"] = V[cid][2]
    rows.append(row)

rows.append({
    "id": "E3f-cards-coverage-L03-misconception-2",
    "check": "2.7-cards (BUILDER_RULES 7: one card per misconception)",
    "location": "L03.html:347-349 (misconception 2, 'The logarithm is a separate case that sits outside the family'); cards.json has no card for it",
    "status": F,
    "evidence": "Scan of cards.json for L03 (23 cards) against the three misconceptions of L03.html:343-353: misconception 1 is E3-c051 and misconception 3 is E3-c048; misconception 2 (the logarithm is the gamma = 1 member and the family converges to it, Proposition 1.4) has no card. Lessons L01, L02 and L04 each have a card for every misconception (L01 c014, c015, c173; L02 c029, c030, c031; L04 c072, c073, c074).",
    "fix": "Add a card with a new id (E3-c177; ids need not be sequential, architect ruling 2), lesson L03, front 'Is the logarithm a separate case outside the CRRA family?', back 'No. It is the member at gamma = 1, u_1(w) = ln w (Definition 1.3), and assuming A2 the family converges to it as gamma tends to 1 (Proposition 1.4). Lab 1 checks the certainty equivalent at gamma = 1 +/- 1e-6 numerically.', grade T.",
})

rows.append({"id": "E3f-cmd-check_pages", "check": "tools/check_pages.py --unit E3", "location": "course/modules/E/E3/ (index, L01-L08, cards.json)", "status": P,
  "evidence": "Run at 4eb6788: 'check_pages E3: PASS', exit 0 (" + S + "check_pages.out)."})
rows.append({"id": "E3f-cmd-check_dag", "check": "tools/check_dag.py --unit E3", "location": "course/modules/E/E3/", "status": P,
  "evidence": "Run at 4eb6788: 'check_dag E3: PASS', exit 0 (" + S + "check_dag.out). Out-of-slice DAG observation in notes."})
rows.append({"id": "E3f-cmd-check_projects", "check": "tools/check_projects.py --unit E3", "location": "course/modules/E/E3/project.html", "status": P,
  "evidence": "Run at 4eb6788: 'check_projects E3: PASS', exit 0 (" + S + "check_projects.out). Not a card row; run because it is in the mandatory command list."})
rows.append({"id": "E3f-cmd-run_labs", "check": "tools/run_labs.py --unit E3 --page L01..L04", "location": "course/modules/E/E3/L01.html..L04.html", "status": P,
  "evidence": "Run per page at 4eb6788: 'run_labs E3: PASS (1/1)' for L01, L02, L03, L04 (" + S + "run_labs_L01-L04.out)."})
rows.append({"id": "E3f-cmd-twins", "check": "lab twins under python -I -W error; page code equals twin; expected block equals output", "location": "tests/labs/E3/lab-E3-L01-1.py .. lab-E3-L04-1.py; expected blocks in L01-L04.html", "status": P,
  "evidence": "Each twin run alone with python -I -W error: exit 0, empty stderr (" + S + "twins/summary.out). Stdout diffed against each page's expected block: IDENTICAL for L01, L02, L03, L04 (" + S + "twins/expected_vs_twin.out, via diff_expected_r4.py)."})
rows.append({"id": "E3f-cmd-page_smoke", "check": "tools/page_smoke.py --unit E3 --pages L01 L02 L03 L04 (Chromium, Pyodide)", "location": "course/modules/E/E3/L01.html..L04.html", "status": P,
  "evidence": "'page_smoke E3: PASS' with every page PASS, labs in Pyodide PASS (" + S + "page_smoke_L01-L04.out). Run once; the page-level gate for this slice's pages."})
rows.append({"id": "E3f-cmd-verify_refs", "check": "tools/verify_refs.py --offline", "location": "references/references.json (560 entries)", "status": P,
  "evidence": "'offline integrity: 560 entries, 0 problems', exit 0 (" + S + "verify_refs_offline.out). No card cites a registry key, so the live run is not needed for this slice."})
rows.append({"id": "E3f-cmd-pytest_labs", "check": "pytest tests/test_labs.py -k E3", "location": "tests/test_labs.py (E3 labs)", "status": P,
  "evidence": "15 passed, exit 0 (" + S + "pytest_labs_E3.out)."})
rows.append({"id": "E3f-cards-duplicates", "check": "2.7-duplicates", "location": "cards.json (all 169 cards)", "status": P,
  "evidence": "Full scan (" + S + "card_checks_r4.out): 169 cards, 0 duplicate ids, 0 duplicate normalised fronts. Near-pairs reviewed: E3-c041/c051 (different questions), c018/c174/c175 (A2 of L02, A5 of L02, A2 of L03), c022/c159/c162 (proposition, hypotheses, not-a-result), c063/c064 (definition, lemma). None duplicates a slice card."})
rows.append({"id": "E3f-cards-refs", "check": "2.7-references", "location": "cards.json labelled references on the 85 slice cards", "status": P,
  "evidence": "cross_refs_r4.py (" + S + "cross_refs_r4.out): 89 labelled references (Proposition, Remark, Lemma, Theorem, Definition, Example, Problem, Assumption, section) resolved in the named lesson. The one script miss, 'Problem E2' in E3-c055, resolves by hand: L03.html:422-427 titles the problem 'E2 · Checking the exact gamma 2 value'."})
rows.append({"id": "E3f-cards-numbers", "check": "2.2-numbers (tokens on cards present in own lesson)", "location": "cards.json slice cards vs L01-L04.html", "status": P,
  "evidence": "card_checks_r4.py (" + S + "card_checks_r4.out): every numeric token on the 85 slice cards occurs in its own lesson text; 'numeric tokens absent from own lesson: []'."})
rows.append({"id": "E3f-numbers-recomputed", "check": "2.2-numbers (recomputed)", "location": "every number on slice cards", "status": P,
  "evidence": "recompute_numbers.py with Fraction and float (" + S + "recompute_numbers.out): L01 15000/12500/15000 and 45000/21250/37500, 22500, 39375/40000/41250; L02 CE 94.9341649 -> 9493 cents, premium 5.0658351 -> 507, Pratt 4.5, error 0.5658351, 11.1696 percent (basis: exact premium), 12.5741 percent (on approximation), premium/eps^2 at five scales, ratio 6.3116 for E1; L03 CE at gamma 0, 0.25, 0.5, 1, 2, 4 (11250, 10931.7733, 10615.8009, 10000, 8888.8889, 7337.6161), 80000/9, 9/80000, 3000, 9000, 1600, 2000, (k+1)/2 = 5.5; L04 I_X, I_Y, F_X, F_Y for Examples 1.7, 2.5, 2.6 and means 3000."})
rows.append({"id": "E3f-notation", "check": "2.4-notation", "location": "L01-L04.html math; notation/notation.json", "status": P,
  "evidence": "macros_r4.py (" + S + "macros_r4.out): lesson math uses only registered macros \\E, \\Var, \\R, \\indic (and \\mathrm{CE}, not a macro). No registered symbol (T, \\Phi, \\gamma_3, \\gamma_4, R^*, R^{e*}, R_f, \\mathbb{Q}) appears in L01-L04. Local letters (gamma, eps, S, pi for the premium, upsilon and chi in the L02 Prop 3.1 proof) are defined where used."})
rows.append({"id": "E3f-banned-and-process", "check": "2.9-prose (banned phrases; process words) on slice cards and L01-L04", "location": "cards.json slice cards; L01-L04.html", "status": P,
  "evidence": "card_checks_r4.py (" + S + "card_checks_r4.out): no BUILDER_RULES 1.3-1.4 phrase, no ellipsis, no process word (builder, verifier, round as a verification round, ledger, REQUESTS) on the slice cards. The only 'round' is the arithmetic verb in E3-c050."})

notes = (
 "Round 4 of E3 slice f: cards of L01 to L04 (85 cards: L01 18, L02 22, L03 23, L04 22). Pin 4eb6788 (round-3 fixes). "
 "Delta from the previous pin a007712f, read in full: course/modules/E/E3/cards.json hunks in the slice are E3-c021 (back now 'on this page') and E3-c039 (back now 'It makes u_gamma(1) = 0 for every gamma (Definition 1.3).'). "
 "The other cards.json hunks are L05 to L08 (out of slice). L01.html to L04.html and tests/labs/E3/lab-E3-L01-1.py to lab-E3-L04-1.py are byte-identical to a007712f (git diff empty). "
 "Every slice card was re-verified from scratch; no round-3 PASS row is carried. Round-3 FAIL E3f-E3-c021 is re-verified PASS. "
 "Hunt classes checked: numbers vs unrounded values (recompute_numbers.py); lab statements vs printed output (run_labs, twin-vs-expected diff, and the card's quotation of each printed value); attributions (no card cites a registry key, and no card attributes a result to a named source); scope words (E3-c031 FAIL); hypotheses of every T card (E3-c159 FAIL, and the rest carry the hypotheses of their proposition); grades and bases (every C card names a lab part, a SIMULATED lab, or Lab 1 with the printed line); duplicates (none); card coverage against BUILDER_RULES 7 (E3f-cards-coverage FAIL for L03 misconception 2); notation (macros_r4.py); process words and banned phrases (none). "
 "Out-of-slice observations for the L02 owner (not rows of this slice): (1) L02.html:159 (Example 2.3) and L02.html:429 (M2 solution) name the CRRA family and cite L03 Definition 1.3 before L03 introduces it; the concept crra-utility is defined in L03 (L03.html:87-90), so L02 uses it before its lesson. This breaks BUILDER_RULES 1.10 and the DAG order of section 4. Fix: state the power-form example without the CRRA name, or move it to L03. (2) L02.html:130-134 (Remark 1.4) omits A1 from the hypotheses the proof uses (the twin of E3f-E3-c159). (3) Assumption labels are reused with different content across lessons: F1 is 'intermediate value' in L02 (L02.html:58-60) and 'zero derivative implies constant' in L03 (L03.html:66); A1 is 'finite support' in L01, L02 and L04 and 'positive wealth' in L03 (L03.html:58-60). Every card qualifies the label by its lesson, so no card is wrong; the architect may want the labels made unique (the same pattern as the E3-a round-10 observation). "
 "Coverage observation (not a row): assumption blocks without a card are L02 A3, A4, F1 to F6 block, L03 A1 and F1/F2 block, L04 A1 and A2 (BUILDER_RULES 7 lists definitions, theorems, formulas, results and misconceptions; every 'Definition N' block in L01 to L04 has a card, so these are not counted). "
 "Not checked: the lessons' prose outside the cards was read for the locators the cards cite and for the labs, not graded against BLUEPRINT section 3 as a whole (hub, L05 to L08, project are not in this slice). ruff and mypy were not run: no Python tool, test or registry file changed in the slice delta (only the E3 L05 to L08 pages, cards.json for L05 to L08, and the L08 and project labs changed); the scripts I wrote live in ledgers/E3/scripts/E3-f-r4 and are not gated. "
 "Live verify_refs was not run (offline integrity only; no card cites a key)."
)
summary = (
 "E3 slice f round 4: verdict FAIL. 100 rows: 97 PASS, 3 FAIL. FAIL rows: E3f-E3-c031 (cards.json:205, scope 'every finite lottery' without outcomes-in-I hypothesis), "
 "E3f-E3-c159 (cards.json:1058, hypothesis list omits A1), E3f-cards-coverage-L03-misconception-2 (no card for L03 misconception 2). "
 "Round-3 FAIL E3f-E3-c021 is fixed and PASS. All numbers, lab statements, cross-references, grades and bases on the 85 slice cards re-derived; all command rows PASS."
)

fragment = {
    "unit": "E3",
    "slice": "f",
    "round": 4,
    "verifier": "Claude Haiku 5.5, independent verifier for E3 slice f, round 4 (did not build E3; cards of L01 to L04 against their lessons)",
    "pin": "4eb6788fe3b408bb6d90ac73addc6fb17af47b8b (4eb6788, detached)",
    "base": "a007712fdbfc8b4851123f4de76b5310ac5a9e64 (round-3 pin, frags/D-E3-f.round3.json). Delta touching the slice: cards.json E3-c021 and E3-c039 only.",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyD4-E3-f",
    "scratch": "ledgers/E3/scripts/E3-f-r4/",
    "verified_at": "2026-11-03T16:14:41+00:00",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": notes,
    "summary": summary,
}
out = ROOT / "ledgers/E3/E3-f.json"
out.write_text(json.dumps(fragment, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("rows", len(rows), "non-PASS", [r["id"] for r in rows if r["status"] != "PASS"])
