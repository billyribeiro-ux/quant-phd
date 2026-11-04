import json, sys
sys.path.insert(0, "tools")
import ledger  # noqa: E402

CARDS = {
 "E3-c001": (3, "L01.html:58-60 (Definition 1.1): distinct real outcomes, p_i >= 0, sum 1; random-variable equivalence matches."),
 "E3-c002": (9, "L01.html:63-65 (Definition 1.2): E X = sum p_i x_i. Recomputed: EV of lottery A = 150 CU (recompute_r5.out)."),
 "E3-c003": (15, "L01.html:68-70 (Definition 1.3): E u(X) = sum p_i u(x_i); depends on u and on the lottery."),
 "E3-c004": (21, "L01.html:73-75 (Assumption A1) and Section 4 at L01.html:331-334 (finitely many outcomes; no result for a continuum)."),
 "E3-c005": (27, "L01.html:85-88 (Definition 2.1): mixture on the union of outcomes; p_L(x)=0 off the outcomes of L."),
 "E3-c006": (33, "L01.html:142-144 (Definition 3.2): u = bx with b > 0; E u = b E X by Proposition 3.1."),
 "E3-c007": (39, "L01.html:90-93 (Proposition 2.2, T, under A1) and proof L01.html:96-100: finite union, nonnegative weights, weights sum to 1."),
 "E3-c008": (46, "L01.html:104-108 (Proposition 2.3, T, under A1, u real-valued) and proof L01.html:113-121. Expected block L01.html:307-313 prints six 'equal True' lines and all_linearity_checks True."),
 "E3-c009": (53, "L01.html:125-127 (Remark 2.4): an identity about Definition 1.3; no claim on preference orderings."),
 "E3-c010": (60, "L01.html:132-134 (Proposition 3.1, T, under A1) and proof L01.html:138: E u = a + b E X; a=0, b=1 gives E X."),
 "E3-c011": (67, "L01.html:147-149 (Proposition 3.3, T, under A1, b > 0) and proof L01.html:153-154."),
 "E3-c012": (74, "L01.html:395-400 (Problem P2 statement and solution): b < 0 reverses the ranking; A1 is the standing finite-lottery setting (L01.html:73-75)."),
 "E3-c013": (81, "L01.html:437-443 (Problem R1 solution): E u(X) <= m, equality only when all probability sits on maximisers; key-results row L01.html:471."),
 "E3-c014": (88, "L01.html:78-80 (Example 1.4) and misconception 1 at L01.html:341-343: u(EX)=150^2=22500 CU^2, E u(X)=45000 CU^2, ratio 2 (recompute_r5.out)."),
 "E3-c015": (95, "L01.html:345-347 (misconception 2) with Definitions 1.2 and 3.2 (L01.html:63-65, 142-144): E u = b E X, probability-weighted."),
 "E3-c016": (102, "cards.json:102 (grade C, basis 'Lab 1, part A'). Expected block L01.html:303-305 prints EV 15000, 12500, 15000 and quadratic EU 45000, 21250, 37500; recomputed with Fraction (recompute_r5.out); twin stdout identical to the expected block (twin_L01.out vs L01.expected.txt)."),
 "E3-c017": (110, "cards.json:110 (grade C, basis 'Lab 1, part B'). Code Part B and expected block L01.html:307-313 print six 'equal True' lines; six comparisons (three weights, two utilities)."),
 "E3-c018": (118, "L02.html:73-75 (Assumption A2): twice differentiable on open I, u' > 0, u'' <= 0; concavity by the sign of u'' (L02.html:74)."),
 "E3-c019": (124, "L02.html:88-94 (Proposition 1.1, T) and proof: weighted average in u(I), an interval by F1; strictly increasing by F5; hypotheses F1, F5, A1 to A3 match."),
 "E3-c020": (131, "L02.html:98-100 (Definition 1.2): unique c with u(c) = E u(X), written CE(X; u)."),
 "E3-c021": (137, "L02.html:99: 'The phrase risk premium has other uses in finance ... On this page, the risk premium is the certainty-equivalent risk premium, and nothing else.' Card says 'on this page'. Round-4 FAIL is fixed."),
 "E3-c022": (143, "L02.html:103-106 (Proposition 1.3(a), T; F1, F2, F5; A1 to A3) and proof L02.html:109-127 (tangent line above u in Step 1, averaged in Step 2)."),
 "E3-c023": (150, "L02.html:103-106 (Proposition 1.3(b)); A4 at L02.html:83-85; strictness needs u'' < 0 and an outcome of positive probability differing from E X (proof L02.html:126)."),
 "E3-c024": (157, "L02.html:143-145 (Definition 2.1): r_A = -u''/u' in 1/CU where u' != 0; r_R = w r_A, dimensionless."),
 "E3-c025": (163, "L02.html:148-149 (Proposition 2.2, b > 0) and proof L02.html:153-154: v' = b u', v'' = b u''; b cancels."),
 "E3-c026": (170, "L02.html:158-160 (Example 2.3) with F6 (L02.html:63): r_A = 1/(2w), r_R = 1/2; at w = 100 r_A = 0.005, r_R = 0.5, matching the expected block L02.html:367. Values unchanged by this round's Example 2.3 edit; the forward-reference defect in the same paragraph is row E3f-dag-L02-crra-forward-use."),
 "E3-c027": (177, "L02.html:172-174 (Proposition 3.1, T; F1, F3, F4, F5; A1, A5) and proof L02.html:176-200; hypotheses match; A5 at L02.html:167-169."),
 "E3-c028": (184, "L02.html:203-205 (Remark 3.2): asymptotic statement; no bound at a fixed eps."),
 "E3-c029": (191, "L02.html:398-399 (misconception 1): half-variance 900 CU^2 (1/2 x 1800), Pratt 4.5 CU (1/2 x 0.005 x 1800), exact 5.065835 CU (recompute_r5.out). Units as the page writes them."),
 "E3-c030": (198, "L02.html:402-404 (misconception 2) and Example 2.3 (L02.html:158-160) with F6; r_A 0.005 per CU and r_R 0.5 at w = 100 recomputed (recompute_r5.out)."),
 "E3-c031": (205, "L02.html:406-407 (misconception 3): 'for every finite lottery with outcomes in I (A1 and A3)'. Card now carries the outcomes-in-I hypothesis; round-4 FAIL is fixed. CE(X;u) is defined under A1 to A3 (L02.html:78-80, 98-100)."),
 "E3-c032": (212, "cards.json:212 (grade C, basis 'Lab 1, part A'). Expected block L02.html:367 prints ce_cents 9493, premium_cents 507, r_A 0.005000, r_R 0.500000, exact 5.065835, Pratt 4.500000, error 0.565835. Recomputed: CE 94.934164903 -> 9493 cents; premium 5.065835097 -> 507 cents (recompute_r5.out)."),
 "E3-c033": (220, "cards.json:220 (grade C, basis 'Lab 1, part B'). Expected block L02.html:370-375 prints 5.065835 (eps 1) to 4.500046 (eps 0.01) and gaps_shrink_as_eps_falls True; all five ratios reproduced (recompute_r5.out)."),
 "E3-c034": (228, "cards.json:228 (grade C, basis 'Lab 1, part A'). 0.565835 / 5.065835 = 0.11170, i.e. 11.17 percent of the exact premium; the basis is stated on L02.html:387 and in E2 at L02.html:479. Recomputed 11.169631 percent (recompute_r5.out)."),
 "E3-c035": (236, "cards.json:236 (grade C, basis 'Lab 1, part C'). Code Part C and expected block L02.html:376-380: linear premium 0 cents at eps 1.0, 0.5, 0.1; linear_premium_zero_at_three_scales True."),
 "E3-c036": (244, "L03.html:72-73 (Definition 1.1): w^a = e^(a ln w) for w > 0."),
 "E3-c037": (250, "L03.html:77-78 (Proposition 1.2, T) and proof L03.html:82-84: (w^a)^b = w^(ab); (xy)^c = x^c y^c."),
 "E3-c038": (257, "L03.html:87-89 (Definition 1.3): u_gamma = (w^(1-gamma) - 1)/(1-gamma) for gamma != 1; u_1 = ln w; w > 0."),
 "E3-c039": (263, "L03.html:90: 'The subtracted 1 makes u_gamma(1) = 0 for every gamma.' Check: (1 - 1)/(1 - gamma) = 0 for gamma != 1, and ln 1 = 0 at gamma = 1. The card carries no A2 claim."),
 "E3-c040": (270, "L03.html:94-95 (Proposition 1.4, assuming A2) and proof L03.html:100-102: u_gamma(w) = L (e^h - 1)/h with h = s L, which tends to L = ln w."),
 "E3-c041": (277, "L03.html:116-117 (Proposition 1.7, assuming F2) and proof L03.html:121-123: u' = w^(-gamma), u'' = -gamma w^(-gamma-1), r_A = gamma/w, r_R = gamma."),
 "E3-c043": (284, "L03.html:128-129 (Theorem 2.1; F1, F2, A3, A4) and proof L03.html:133-135: u = K u_gamma + C with K > 0."),
 "E3-c044": (291, "L03.html:138-139 (Remark 2.2): the theorem does not say an investor has CRRA; no source is cited."),
 "E3-c045": (298, "L03.html:143-144 (Definition 2.3): positive outcomes, so each lies in the domain of A1 (wealth above zero, L03.html:58-59)."),
 "E3-c046": (304, "L03.html:148-149 (Proposition 2.4, T) and proof L03.html:153-155: gamma != 1 gives M^(1/s); gamma = 1 gives exp(sum p ln x)."),
 "E3-c047": (311, "L03.html:158-159 (Example 2.5): 1600 cents at gamma = 2 and 2000 cents at gamma = 1 (sqrt(4 000 000)); recomputed exactly (recompute_r5.out)."),
 "E3-c048": (318, "L03.html:163-164 (Proposition 2.6, T; positive outcomes, k > 0, every real gamma) and proof L03.html:168-170: (kx)^s = k^s x^s."),
 "E3-c049": (325, "L03.html:173-174 (Proposition 2.7; a > 0, real b; CE under u assumed to exist and be unique) and proof L03.html:178-180."),
 "E3-c050": (332, "L03.html:183-185 (Remark 2.8): compute once as a float, round half up, floor(v + 1/2) for v >= 0; not an intermediate value. Ungraded unit convention (as CU = 100 cents at L01.html:55 is). Judgement call recorded in notes."),
 "E3-c051": (338, "L03.html:344-345 (misconception 1) with Proposition 1.7 (L03.html:116-117): r_R constant; r_A = gamma/w falls when gamma > 0 (assumes F2, as the lesson does)."),
 "E3-c052": (345, "L03.html:106-107 (Example 1.5): u_0(w) = w - 1, affine with slope 1; ranks as w (L01.html:147-149, Proposition 3.3)."),
 "E3-c053": (352, "L03.html:326-328 (interpretation: finite checks) and Problem R3 (L03.html:454-457): six exponents for one lottery; a proof needs a general argument. Meta-claim graded T."),
 "E3-c054": (359, "cards.json:359 (grade C, basis 'Lab 1 (one fixed lottery, floating point)'). Expected block L03.html:309-314 prints 11250.0000, 10000.0000, 8888.8889, 7337.6161 at gamma 0, 1, 2, 4; falls-as-gamma-rises True at L03.html:319; recomputed (recompute_r5.out)."),
 "E3-c055": (367, "L03.html:148-149 (Proposition 2.4) and Problem E2 (L03.html:422-426, title 'Checking the exact gamma 2 value'): M = 9/80000, CE = 80000/9; expected block L03.html:315 prints 80000/9 cents."),
 "E3-c056": (374, "L04.html:64-65 (Definition 1.1): F_X(t) = P(X <= t) and I_X(t) = integral from minus infinity to t of F_X."),
 "E3-c057": (380, "L04.html:69-70 (Lemma 1.2, T, under A1) and proof L04.html:74-76: I_X(t) = E(t - X)^+."),
 "E3-c058": (387, "L04.html:79-80 (Definition 1.3): F_X(t) <= F_Y(t) for every real t; X at least as likely to exceed every level."),
 "E3-c059": (393, "L04.html:84-85 (Definition 1.4): u(s_j) <= u(s_{j+1}) for each j."),
 "E3-c060": (399, "L04.html:89-90 (Theorem 1.5, T, under A1) and proof L04.html:94-98."),
 "E3-c061": (406, "L04.html:102-103 (Lemma 1.6, T, under A1) and proof L04.html:107-108: support points suffice."),
 "E3-c062": (413, "L04.html:117-118 (Proposition 1.8, T, under A1, 'holds without A2') and proof L04.html:122-123."),
 "E3-c063": (420, "L04.html:129-130 (Definition 2.1): under A1 and A2, I_X(t) <= I_Y(t) for every real t."),
 "E3-c064": (426, "L04.html:134-135 (Lemma 2.2, T, under A1 and A2) and proof L04.html:139-140: D affine between support points, D = 0 for t >= s_m by A2."),
 "E3-c065": (433, "L04.html:144-145 (Theorem 2.3, T, under A1 and A2) and proofs L04.html:149-155 for nondecreasing concave u on S."),
 "E3-c066": (440, "L04.html:159-160 (Remark 2.4): the only-if proof uses concavity through c_j >= 0 and A2; no monotonicity; checked against the proof at L04.html:151-155."),
 "E3-c067": (447, "L04.html:164-166 (Example 2.5): I_X(3000,4000,5000) = 500, 1000, 2000; I_Y(2000,3000,4000,5000) = 250, 500, 1250, 2000; means 3000. Recomputed (recompute_r5.out); printed at expected block L04.html:445-446."),
 "E3-c068": (454, "L04.html:166-168 (Example 2.5): F_X(2000) = 1/2 > 1/4 = F_Y(2000) and F_Y(3000) = 3/4 > 1/2 = F_X(3000); second-order ranking X over Y. Recomputed (recompute_r5.out)."),
 "E3-c070": (461, "L04.html:112-113 (Example 1.7): F_X = (1/2, 1/2, 1), F_Y = (0, 1/2, 1) on 2000, 3000, 4000; Y dominates X in the first order (Lemma 1.6)."),
 "E3-c071": (468, "Problem R3 (L04.html:613-616; statement L04.html:614): unequal means, A2 not assumed, nondecreasing concave u on S; I_X(s_m) = s_m - E X gives E X >= E Y; slope b_1 = sigma_{m-1} >= 0 from monotonicity. Matches the card."),
 "E3-c072": (475, "L04.html:502-504 (misconception 1) with Example 2.6 (L04.html:172-173): X = (1000, 5000), Y = 3000, equal means, no first-order ranking."),
 "E3-c073": (482, "cards.json:482 (grade C, basis 'Lab 1 (SIMULATED)'). Expected block L04.html:472 and :475 print pairs 16 and 19 with 'SOSD no ranking'; L04.html:508 names them; 2 of 8 equal-mean pairs confirmed (twin output and l04_check_r5.out)."),
 "E3-c074": (490, "L04.html:511-512 (misconception 3) with Example 2.5: a second-order ranking without a first-order ranking, so the tests differ (section 4, third misconception)."),
 "E3-c075": (497, "cards.json:497 (grade C, basis 'Lab 1 (SIMULATED)'). Expected block L04.html:480-481 prints 'FOSD verdicts over the 24 pairs: {X dominates Y: 3, Y dominates X: 10, identical: 1, no ranking: 10}' and '24 of 24'; counts sum to 24 (l04_check_r5.out)."),
 "E3-c076": (505, "cards.json:505 (grade C, basis 'Lab 1 (SIMULATED)'). Expected block L04.html:483-484 prints SOSD verdicts {X dominates Y: 3, Y dominates X: 2, identical: 1, no ranking: 2} and '8 of 8' (l04_check_r5.out)."),
 "E3-c077": (513, "L04.html:492-495 (Section 3, canon): the expected-utility side checks a finite test set; Theorems 1.5 and 2.3 quantify over every nondecreasing or concave utility on S, which the lab does not check. Lab docstring L04.html:190-192 says the same."),
 "E3-c159": (1058, "L02.html:129-132 (Remark 1.4 'the hypotheses used') and proof L02.html:113-127: A2 (Step 1), F2 (Step 1), F1 (Step 3, existence), A1 (finite sums, Step 2), A3 (outcomes in I), F5 (strict increase). The card lists all six. Round-4 FAIL (missing A1) is fixed."),
 "E3-c160": (1064, "cards.json:1064 (grade C, basis 'Lab 1, gamma = 1 +/- 1e-6 line'). Code check gap <= 0.01 cents; expected block L03.html:321 prints True. The card states only floating-point agreement on one lottery."),
 "E3-c161": (1072, "cards.json:1072 (grade C, basis 'Lab 1, part B'). Interpretation L02.html:381 ('a check of the limit ... not a proof of that limit') and Problem R2 (L02.html:500-504)."),
 "E3-c162": (1080, "cards.json:1080. L02.html:131 (Remark 1.4, last sentence): for u'' >= 0 Steps 1 to 3 reverse, and 'this lesson does not state that case as a result'."),
 "E3-c167": (1113, "cards.json:1113. L04.html:84-85 (Definition 1.4): chord slopes sigma_j nonincreasing in j = 1 to m-1."),
 "E3-c168": (1119, "cards.json:1119. L03.html:183-185 (Remark 2.8): bound (k+1)/2 cents; proof |R(kv)-kv| <= 1/2, |kR(v)-kv| <= k/2, triangle inequality. k = 10 gives 5.5 cents (recompute_r5.out)."),
 "E3-c171": (1142, "cards.json:1142 (grade C, basis 'Lab 1, homogeneity line'). Code tests k = 2, 3, 10 at the six gammas; expected block L03.html:324-325 prints 'unrounded: True' and the cents bound True."),
 "E3-c173": (1156, "cards.json:1156. L01.html:349-351 (misconception 3): with b = 0, E v(L) = a for every lottery (probabilities sum to 1), so every pair ties."),
 "E3-c174": (1163, "cards.json:1163. L02.html:167-169 (Assumption A5): twice differentiable on open I containing w; u' > 0 on I; small eps keeps w + eps x_i in I."),
 "E3-c175": (1169, "cards.json:1169. L03.html:58-60 (Assumption A2): the limit (e^h - 1)/h -> 1 is taken as given. M1 Lesson 3 defines e as e^1 and does not derive the limit (checked in course/modules/M/M1/L03.html)."),
 "E3-c177": (1175, "cards.json:1175 (added this round; round-4 coverage FAIL is fixed). Misconception 2 at L03.html:347-349 says the logarithm is the gamma = 1 member and Proposition 1.4 gives the convergence; Definition 1.3 (L03.html:87-90) and Proposition 1.4 (L03.html:94-95) match; the lab check at gamma = 1 +/- 1e-6 is expected block L03.html:321, True."),
}
LESSON = {}
for k, (line, _) in CARDS.items():
    pass
cards = json.load(open("course/modules/E/E3/cards.json", encoding="utf-8"))
slice_ids = [c["id"] for c in cards if c["lesson"] in ("L01", "L02", "L03", "L04")]
assert sorted(slice_ids) == sorted(CARDS), (set(slice_ids) ^ set(CARDS))
lesson_of = {c["id"]: c["lesson"] for c in cards}
rows = []
for cid in slice_ids:
    line, ev = CARDS[cid]
    rows.append({"id": f"E3f-{cid}", "check": "2.7-cards", "location": f"cards.json:{line} ({cid}, {lesson_of[cid]})",
                 "status": "PASS", "evidence": ev})

def add(id_, check, location, status, evidence, fix=None):
    r = {"id": id_, "check": check, "location": location, "status": status, "evidence": evidence}
    if fix:
        r["fix"] = fix
    rows.append(r)

add("E3f-lesson-numbers-L01", "1-numbers", "L01.html:55, 79, 303-325, 341-353, 363-367, 371-383, 395-455, 488-557",
    "PASS", "Every number in L01 prose, misconceptions, problems and quiz recomputed with Fraction (ledgers/E3/scripts/E3-f-r5/recompute_r5.out, L01 lines): EV 150 CU; E u = 45000 CU^2; u(EX)=22500; M1 59, 4030, 3481, difference 549; M2 400/3 and 50 vs 175; M3 20 and 30 vs 65 and 95; E1 7500; E2 40000; E3 sums 1 and 5/6; R3 25000 vs 22500; quiz Q7 5/12. Part A-D expected values match.")
add("E3f-lesson-numbers-L02", "1-numbers", "L02.html:136-137, 159, 367-381, 387, 399-404, 436-437, 470-488",
    "PASS", "Example 1.5: E sqrt(W) = 9.743416, CE = 94.934165, premium 5.065835, cents 9493 and 507 (recompute_r5.out). Pratt 4.5 and half-variance 900 CU^2; error 0.565835 = 11.17 percent of the exact premium and 12.57 percent of the approximation (basis stated in E2). Part B gaps 0.565835, 0.119495, 0.028811, 0.004565, 0.000046 reproduced; E1 ratio 0.028811/0.004565 = 6.31 vs eps^2 ratio 6.25. E3: 94.934165 -> 9493.4165 cents; 5.065835 -> 506.5835 -> 507. M1 CE 9, premium 1; M3 r_A = a.")
add("E3f-lesson-numbers-L03", "1-numbers", "L03.html:159, 189, 309-325, 344-353, 368-383, 422-432",
    "PASS", "CE at gamma 0, 0.25, 0.5, 1, 2, 4 = 11250, 10931.7733, 10615.8009, 10000, 8888.8889, 7337.6161 (recompute_r5.out) with the page's rounding; 80000/9 and M = 9/80000; Example 2.5 1600 and 2000; M1 r_A(4) = 1/8, r_R = 1/2; M2 M = 1/3000, CE 3000, mean 7000; M3 9000; E1 10615.8009 -> 10616; E3 bound 5.5 cents.")
add("E3f-lesson-numbers-L04", "1-numbers", "L04.html:164-175, 445-484, 485, 494, 527-538, 556-584, 588-591",
    "PASS", "Example 2.5 integrated values I_X = 0, 0, 500, 1000, 2000 and I_Y = 0, 250, 500, 1250, 2000; means 3000 both (recompute_r5.out). Example 2.6 I_X = 0, 1000, 2000 and I_Y = 0, 0, 2000. Named pair B I_Y(4000) = 500. M1 means 2500 and 2000; M2 500 and 500; M3 500. Seeded-pair counts: l04_check_r5.out re-runs the lab's own construction (24 pairs; 8 equal-mean; FOSD 3/10/1/10; equal-mean SOSD 3/2/1/2); the page's '1/48' claim holds (second-lottery denominators 12, 24, 48 in the equal-mean kind, all dividing 48).")
for n in (1, 2, 3, 4):
    add(f"E3f-lab-L0{n}", "3-labs", f"course/modules/E/E3/L0{n}.html lab-E3-L0{n}-1 (code, expected block) and tests/labs/E3/lab-E3-L0{n}-1.py",
        "PASS", f"run_labs.py --unit E3 --page L0{n}: 'run_labs E3: PASS (1/1)', exit 0 (run_labs_L0{n}.out). Twin run alone under python -I -W error: exit 0, stderr 0 bytes (twin_L0{n}.err). Page code equals twin file (extract_check.py: page_code_equals_twin True). Expected block equals twin stdout ignoring the final newline (IDENTICAL, scripts/E3-f-r5/L0{n}.expected.txt vs twin_L0{n}.out).")
add("E3f-dag-L02-crra-forward-use", "2.9-define-before-use",
    "course/modules/E/E3/L02.html:159 (Example 2.3) and L02.html:429 (solution to M2)",
    "FAIL",
    "L02 uses the normalized CRRA power family before the lesson that defines it. L02.html:159: 'the function u_{1/2}(w) = (w^{1/2} - 1)/(1/2) that L03 Definition 1.3 defines with gamma = 1/2'. L02.html:429: 'L03 Definition 1.3 defines it as the case gamma = 1 of the power family that lesson introduces'. L03 introduces the family at L03.html:87-90 (concept crra-utility, dfn at L03.html:88). plans/E3-build-plan.md section 2 item 5 and BUILDER_RULES section 2 require that a lesson use a concept only after the lesson that defines it; VERIFIER_RULES 2.9 requires the verifier to confirm nothing is used before it is defined. The round-4 observation (1) is still open: the builder edited the wording of both sentences and kept the forward reference. The defining formula is not in L03 at the time L02 uses it.",
    fix="L02.html:159: delete 'that L03 Definition 1.3 defines with gamma = 1/2, because u_{1/2}(w) = 2 sqrt(w) - 2' and state the affine relation in L02's own terms (sqrt(w) = (u(w) + 2)/2 with u(w) = 2 sqrt(w) - 2 written out), or move the sentence to L03 as a remark after Definition 1.3. L02.html:429: delete 'and L03 Definition 1.3 defines it as the case gamma = 1 of the power family that lesson introduces' and replace 'constant relative risk aversion equal to 1' with 'relative risk aversion equal to 1 at every w > 0' (the Problem already derives it). Re-run check_dag.py --unit E3 and check_pages.py --unit E3 after the edit.")
add("E3f-dag-other-links", "2.9-define-before-use", "L01.html:37-38, 334; L02.html:37-38, 388; L03.html:37-38; L04.html:37-38; all data-concept links",
    "PASS", "Concept links point to closure concepts (concepts.html) or to earlier lessons (L03 links L02 #def-arrow-pratt-risk-aversion and #def-certainty-equivalent; L04 links L03 #def-crra-utility). Forward mentions in prose name later lessons as topics without using their concepts: L01.html:334 (Lesson L08 under ambiguity aversion) and L02.html:388 (L06 prospect theory, L07 probability weighting). Accepted as pointers, not uses. check_dag.py --unit E3 PASS.")
add("E3f-coverage-cards", "2.7-cards-coverage", "cards.json (all L01 to L04 definitions, propositions, lemmas, theorems, remarks, misconceptions)",
    "PASS", "Every Definition, Proposition, Lemma, Theorem, Remark and misconception block of L01 to L04 has a card: L01 Def 1.1-3.2 (c001-c003, c005, c006), A1 (c004), Prop 2.2/2.3/3.1/3.3 (c007, c008, c010, c011), Remark 2.4 (c009), Problems P2/R1 (c012, c013), misconceptions 1-3 (c014, c015, c173); L02 Def 1.2 (c020, c021), Def 2.1 (c024), Prop 1.1, 1.3(a)(b), 2.2, 3.1 (c019, c022, c023, c025, c027), Remarks 1.4, 3.2 (c159, c162, c028), Example 2.3 (c026), misconceptions (c029-c031); L03 Def 1.1, 1.3 (c036, c038), Prop 1.2, 1.4, 1.7 (c037, c040, c041), Theorem 2.1 (c043), Remark 2.2 (c044), Def 2.3 (c045), Prop 2.4, 2.6, 2.7 (c046, c048, c049), Remark 2.8 (c050), misconceptions 1-3 (c051, c177, c048), Problem R3 (c053), Example 2.5 (c047), Example 1.5 (c052); L04 Def 1.1, 1.3, 1.4, 2.1 (c056, c058, c059/c167, c063), Lemma 1.2, 1.6, 2.2 (c057, c061, c064), Theorem 1.5, 2.3, Prop 1.8, Remark 2.4 (c060, c065, c062, c066), Examples 1.7, 2.5, 2.6 (c070, c067/c068, c072), Problem R3 (c071), misconceptions 1-3 (c072, c073, c074). Definition 1.6 of L03 (recalled from L02 Definition 2.1) has no card of its own: its content is card c024, and a second card would duplicate it. Round-4 coverage FAIL (L03 misconception 2) is fixed by c177.")
add("E3f-cards-integrity", "2.7-cards-duplicates", "cards.json (169 cards; 86 in the slice)",
    "PASS", "card_checks_r5.out: 169 cards; 0 duplicate ids; 0 duplicate normalised fronts; 0 duplicate normalised backs. Near-pairs reviewed and distinct: c040 vs c177 (the limit value vs the misconception 'logarithm is outside the family'), c033 vs c161 (what Part B prints vs what it proves), c053 vs c077 vs c160 vs c171 (what each lab check does not prove), c061 vs c064 (Lemmas 1.6 and 2.2), c018 vs c174 vs c159 (A2, A5, and the hypotheses of Proposition 1.3).")
add("E3f-cards-numbers", "2.7-cards-numbers", "cards.json slice cards vs L01 to L04.html",
    "PASS", "card_checks_r5.py: every numeric token on the 86 slice cards (excluding 0 to 3) occurs in its own lesson; 'numeric tokens absent from own lesson: []' (card_checks_r5.out). Values recomputed in recompute_r5.out.")
add("E3f-cards-xrefs", "2.7-cards-refs", "cards.json labelled references (Proposition, Lemma, Theorem, Remark, Example, Problem, Definition, Assumption, section) in the slice",
    "PASS", "xref_r5.py resolves each labelled reference inside its named lesson: 'Problem E2' (c055) is L03.html:422; 'section 4' and 'section 5' (c014, c029, c031, c034, c051, c072, c073, c074, c173) are the canon and misconception sections of their lessons, which match (section 4 = Where the canon breaks in L02; section 4 = Misconceptions in L03 and L04; section 5 = Misconceptions in L01 and L02). Unresolved: [] (xref_r5.out). Cross-unit references (L01 Proposition 3.3 in c052; M1 Lesson 3 in c175) checked against L01.html:147-149 and course/modules/M/M1/L03.html.")
add("E3f-cards-grades", "2.7-cards-grades", "cards.json grade and basis fields for the slice",
    "PASS", "Every C card names a lab part (Lab 1 part A, B or C, or the gamma = 1 line, or the homogeneity line) or 'Lab 1 (SIMULATED)' and its printed line, as BUILDER_RULES 7 requires. Every T card carries the hypotheses of its proposition (checked card by card). Cards without a grade are definitions, assumptions, remarks, or the convention c050 (judgement recorded in notes).")
add("E3f-notation", "2.13-notation", "L01 to L04.html math; notation/notation.json",
    "PASS", "macros_r4 check repeated: lesson math uses only the registered macros \\E, \\Prob, \\Var, \\R, \\indic (notation.json macros). No registered symbol (T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q}) appears in L01 to L04 (grep of the four pages). Greek letters gamma, pi, upsilon, chi, varepsilon are local and not registered.")
add("E3f-banned-and-process", "1.3-1.4-banned", "L01 to L04.html text and cards",
    "PASS", "banned_r5.out: no TODO, TBD, lorem, 'for brevity', 'beyond the scope', 'obviously', 'clearly', 'studies show' and no prose ellipsis; the only three-dot tokens are Python type hints (tuple[int, ...]) inside lab code. process_words_r5.out: no builder, verifier, ledger, REQUESTS or audit wording; 'round' is the arithmetic verb.")
add("E3f-references", "2.4-attributions", "L02.html:616 (Pratt 1964); L01.html:564; L03.html:564; L04.html:716; L03.html:59 and 82-85 (M1 locators); course/modules/E/E3/index.html:166",
    "PASS", "references/references.json key pratt1964risk: Pratt, John W., 'Risk Aversion in the Small and in the Large', Econometrica 32 (1964), year 1964, used_by E3. L02 names 'Pratt (1964)' for the name only; the hub (index.html:166) says the same. M1 Lesson 3 locators checked in course/modules/M/M1/L03.html: Proposition 1.4 (ln(e^y) = y), Proposition 1.6(b) (ln(ab) = ln a + ln b), A2 (addition), A3 (exactly one x with e^x = y), e defined as e^1, and no derivation of the limit (e^h-1)/h. verify_refs.py --offline: '560 entries, 0 problems'. No card cites a key in the slice.")
add("E3f-hours", "2.12-hours", "L01 to L04.html data-hours; index.html:29 and :127",
    "PASS", "Each lesson data-hours=7 (eyebrow '7 study hours'); 8 lessons x 7 = 56 = data-hours-lessons; project 14; total 70, as the plan states. No arithmetic inconsistency.")
add("E3f-delta", "0-delta", "git diff 4eb6788..440ed3c for course/modules/E/E3",
    "PASS", "Delta read in full. Slice hunks: L02.html (why-it-matters 51; A4 84; Remark 1.4 131; Example 2.3 159; misconception 3 407; M2 solution 429), L04.html (interpretation 485; R2 609; R3 616; table 630 and 633; references 717), cards.json E3-c031 (205), E3-c159 (1058), and E3-c177 added (1175) with E3-c176 (L08) removed. L01 and L03 pages unchanged. Every slice card and every slice page was re-verified from scratch this round; no round-4 PASS row is carried.")
add("E3f-cmd-check_pages", "command", "course/modules/E/E3/",
    "PASS", "check_pages.py --unit E3: 'check_pages E3: PASS', exit 0 (check_pages_E3.out).")
add("E3f-cmd-check_dag", "command", "course/modules/E/E3/",
    "PASS", "check_dag.py --unit E3: 'check_dag E3: PASS', exit 0 (check_dag_E3.out). The define-before-use defect above is outside what check_dag checks (linked uses only), so it is a verifier row.")
add("E3f-cmd-page_smoke", "command", "course/modules/E/E3/L01.html to L04.html",
    "PASS", "page_smoke.py --unit E3 --pages L01 L02 L03 L04: each page PASS, labs run in the runtime, 'page_smoke E3: PASS', exit 0 (page_smoke_L01-L04.out).")
add("E3f-cmd-pytest-labs", "command", "tests/test_labs.py -k E3",
    "PASS", "pytest tests/test_labs.py -k E3 -q: all passed, exit 0 (pytest_labs_E3.out).")
add("E3f-cmd-ruff-labs", "command", "tests/labs/E3 and course/modules/E/E3/grader",
    "PASS", "ruff check tests/labs/E3 course/modules/E/E3/grader: 'All checks passed!', exit 0 (ruff_check_E3.out). No Python tool or test changed in the delta, so mypy --strict and the full pytest were not re-run.")

fragment = {
    "unit": "E3",
    "slice": "f",
    "round": 5,
    "verifier": "Claude Haiku 5.5, independent verifier for E3 slice f, round 5 (did not build E3; cards of L01 to L04 against their lessons, hypotheses, grades, bases, numbers, duplicates, define-before-use).",
    "pin": "440ed3c8216725d498d9c6d7c746907d4d418198 (440ed3c, detached)",
    "base": "4eb6788fe3b408bb6d90ac73addc6fb17af47b8b (round-4 pin; frags/D-E3-f.round4.json). Delta touching the slice: L02.html, L04.html, cards.json E3-c031, E3-c159 and new E3-c177 (E3-c176 removed from L08).",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyD5-E3-f",
    "scratch": "ledgers/E3/scripts/E3-f-r5/",
    "verified_at": "2026-11-03T17:00:00+00:00",
    "verdict": None,
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Mutants: not required. The slice is lessons and cards; lab twins are demonstrations and mutation testing applies to project graders only (ruling). No new grader mutants were written.",
        "Judgement call, not a FAIL: card E3-c050 (Remark 2.8, the cents rounding rule) carries no grade. It is a unit convention, not a claim; CU = 100 cents (L01.html:55) is also ungraded. If the architect wants every convention graded C with a basis, add grade C and basis 'unit convention, Remark 2.8' to c050.",
        "Observation for the architect (not a row): assumption labels are reused with different content across lessons. A1 is 'finite support' in L01, L02 and L04 and 'positive wealth' in L03; F1 is 'intermediate value' in L02 and 'zero derivative implies constant' in L03; A2 means concavity in L02, the exponential limit in L03, and equal means in L04. Every card qualifies its label with the lesson, so no card is wrong; unique labels would remove the ambiguity.",
        "Observation: card ids have gaps (E3-c042, E3-c069, and E3-c176 removed from L08 this round). check_pages accepts gaps; no row depends on them.",
        "Observation for the author of L02 (the FAIL row): the same paragraph of Example 2.3 still states the CRRA identification. Fixing it is a text change only; cards c026 and c030 remain correct after the fix.",
        "Lab twins are demonstrations; their outputs were checked against the expected blocks and recomputed independently, not graded for mutation strength.",
    ],
    "summary": {},
}
fragment["verdict"] = "PASS" if all(r["status"] == "PASS" for r in rows) else "FAIL"
out = "ledgers/E3/E3-f.json"
json.dump(fragment, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
probs = ledger.validate(json.load(open(out, encoding="utf-8")), "E3-f")
counts = {s: sum(1 for r in rows if r["status"] == s) for s in ("PASS", "FAIL", "UNVERIFIABLE")}
print("rows", len(rows), counts, "verdict", fragment["verdict"])
print("validate:", probs)
