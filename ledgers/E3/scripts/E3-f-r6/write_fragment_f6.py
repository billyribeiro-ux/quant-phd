"""Builds ledgers/E3/E3-f.json (verifier E3-f, round 6). Every evidence string cites a file in this repo or a script here."""
import json, re, datetime

ROOT = "."
S = "ledgers/E3/scripts/E3-f-r6"
cards_path = "course/modules/E/E3/cards.json"
line_of = {}
for i, l in enumerate(open(cards_path, encoding="utf-8").read().split("\n"), 1):
    x = re.search(r'"id": "(E3-c\d+)"', l)
    if x:
        line_of[x.group(1)] = i
cards = {c["id"]: c for c in json.load(open(cards_path, encoding="utf-8"))}

T = f"{S}/text/L0"  # text dumps: T + "1.txt" etc.
def tx(lesson, a, b=None):
    return f"{S}/text/{lesson}.txt:{a}" + (f"-{b}" if b else "")

# evidence per card: (lesson, text-dump locator, what was checked)
EV = {
 "E3-c001": ("L01", "45", "Definition 1.1 (distinct real outcomes, p_i >= 0, sum 1; random-variable equivalence in the same sentence)"),
 "E3-c002": ("L01", "48", "Definition 1.2 E X = sum p_i x_i; EV of A = 15000 cents = 150 CU (text:248; numbers_L01_L04.out)"),
 "E3-c003": ("L01", "51", "Definition 1.3 E u(X) = sum p_i u(x_i); depends on u and on the lottery"),
 "E3-c004": ("L01", "54", "A1 text: 'no result here allows a lottery with infinitely many outcomes'; card cites Section 4 (text:275), which says 'continuum'; the statement matches A1, the locator should add A1"),
 "E3-c005": ("L01", "62", "Definition 2.1 mixture on the union of outcomes, p_L(x)=0 off the outcomes of L"),
 "E3-c006": ("L01", "100-103", "Definition 3.2 u(x)=bx, b>0; E u = b E X from Proposition 3.1 (text:100)"),
 "E3-c007": ("L01", "65-72", "Proposition 2.2 under A1; finitely many outcomes, weights >= 0 summing to 1 (proof text:68-72)"),
 "E3-c008": ("L01", "74-89", "Proposition 2.3 under A1 with u real-valued; proof text:81-89; exact identity 400/3 = 400/3 in M2 (numbers_L01_L04.out)"),
 "E3-c009": ("L01", "91-92", "Remark 2.4: Proposition 2.3 is an identity about the formula and says nothing about preference orderings"),
 "E3-c010": ("L01", "96-100", "Proposition 3.1 under A1, u = a + bx gives E u = a + b E X; a=0, b=1 gives the expected value"),
 "E3-c011": ("L01", "105-109", "Proposition 3.3 under A1 with b > 0; proof text:109 gives the equivalence"),
 "E3-c012": ("L01", "333-338", "Problem P2 solution text:338: for b<0 the ranking reverses (E v(L) >= E v(M) iff E u(M) >= E u(L))"),
 "E3-c013": ("L01", "372-377", "Problem R1 solution text:377: E u <= m, equality iff p_i = 0 off the outcomes attaining m. The question says 'which one' (singular); several lotteries attain m (observation, not a row defect)"),
 "E3-c014": ("L01", "285-287", "Misconception 1: u(EX)=150^2=22500, E u(A)=45000 CU^2 (recomputed, numbers_L01_L04.out)"),
 "E3-c015": ("L01", "289-291", "Misconception 2: risk-neutral E u = b E X; probabilities enter the calculation"),
 "E3-c016": ("L01", "247-250", "Lab 1 Part A output: EV 15000, 12500, 15000; quadratic EU 45000, 21250, 37500; recomputed exactly (numbers_L01_L04.out)"),
 "E3-c017": ("L01", "251-258", "Lab 1 Part B output: six lines (alpha 1/4, 1/3, 1/2 x linear, quadratic), all 'equal True', and all_linearity_checks True (text:258)"),
 "E3-c173": ("L01", "293-295", "Misconception 3 (text:295): at b = 0 every pair ties, so the ordering is lost; v is constant"),
 "E3-c018": ("L02", "59-60", "A2 text: u twice differentiable on open I, u'(y) > 0, u''(y) <= 0; concavity by the sign of u''"),
 "E3-c019": ("L02", "68-72", "Proposition 1.1 under F1, F5, A1-A3; proof text:72 (image of I is an interval, unique c by strict monotonicity)"),
 "E3-c020": ("L02", "74-75", "Definition 1.2: CE is the unique c with u(c) = E u(X)"),
 "E3-c021": ("L02", "75", "Definition 1.2: risk premium = E X - CE; text:75 says the phrase has this single meaning on the page"),
 "E3-c022": ("L02", "77-98", "Proposition 1.3(a) under F1, F2, F5, A1-A3; Steps 1-3 at text:85-96"),
 "E3-c023": ("L02", "79-80, 98", "Proposition 1.3(b) with A4 and an outcome of positive probability differing from E X; strict proof text:98"),
 "E3-c024": ("L02", "108-109", "Definition 2.1: r_A = -u''/u' (1/CU) where u'(w) != 0; r_R = w r_A (dimensionless)"),
 "E3-c025": ("L02", "111-115", "Proposition 2.2 with b > 0 and proof text:115 (b cancels)"),
 "E3-c026": ("L02", "117-118", "Example 2.3: r_A = 1/(2w), r_R = 1/2; at w = 100, 0.005 and 0.5 (Lab 1 Part A prints these, text:304)"),
 "E3-c027": ("L02", "127-152", "Proposition 3.1 under F1, F3, F4, F5, A1, A5; E X = 0; limit 1/2 r_A s^2 (proof Steps 1-3, text:136-152)"),
 "E3-c028": ("L02", "154-155", "Remark 3.2: asymptotic statement, no bound at a fixed eps"),
 "E3-c029": ("L02", "333-335", "Misconception 1: half variance 900 CU^2 is not a premium; approximation 4.5 CU; exact 5.065835 CU (numbers_L01_L04.out)"),
 "E3-c030": ("L02", "337-339", "Misconception 2: r_A and r_R differ by w; sqrt at 100 gives 0.005 per CU and 0.5"),
 "E3-c031": ("L02", "341-343", "Misconception 3: u(w)=w gives CE = E X for every finite lottery in I (A1, A3)"),
 "E3-c032": ("L02", "304", "Lab 1 Part A output: ce_cents 9493, premium_cents 507, r_A 0.005000, r_R 0.500000, exact 5.065835, approx 4.500000, error 0.565835 (recomputed)"),
 "E3-c033": ("L02", "306-312", "Lab 1 Part B output: 5.065835 at eps 1.0 to 4.500046 at 0.01; gaps shrink True (recomputed to 6 dp)"),
 "E3-c034": ("L02", "323, 407-409", "11.17 percent = 0.565835/5.065835 (0.111696, recomputed); Section 4 text:323 and E2 text:407-409 use the exact premium as basis"),
 "E3-c035": ("L02", "313-317", "Lab 1 Part C output: linear premium 0 at eps 1.0, 0.5, 0.1; linear_premium_zero_at_three_scales True (text:317)"),
 "E3-c159": ("L02", "100-101", "Remark 1.4 lists A2 (u''(xi) <= 0), u' > 0 via F5, F2 in Step 1, F1 in Step 3, A1 sums, A3 placement; the card matches it"),
 "E3-c161": ("L02", "312, 319", "Lab 1 Part B checks five scales; text:319 says it is a check of the limit, not a proof; Problem R2 text:430-432"),
 "E3-c162": ("L02", "101", "Remark 1.4: the u'' >= 0 case holds with inequalities reversed and is not stated as a result"),
 "E3-c174": ("L02", "124-125", "A5 text: u twice differentiable on open I containing w, u' > 0, every small eps puts w + eps x_i in I"),
 "E3-c036": ("L03", "54-55", "Definition 1.1: w^a = e^{a ln w} for w > 0"),
 "E3-c037": ("L03", "57-61", "Proposition 1.2 statement and proof (text:61)"),
 "E3-c038": ("L03", "63-68", "Definition 1.3 normalized CRRA: (w^{1-g}-1)/(1-g) for g != 1, ln w at g = 1"),
 "E3-c039": ("L03", "68", "u_gamma(1) = 0 for every gamma from the subtracted 1 (text:68)"),
 "E3-c040": ("L03", "70-78", "Proposition 1.4 assuming A2; proof text:74-78 with h = s ln w and u = L (e^h-1)/h"),
 "E3-c041": ("L03", "86-90", "Proposition 1.7 assuming F2: u' = w^{-g}, u'' = -g w^{-g-1}, r_A = g/w, r_R = g"),
 "E3-c043": ("L03", "94-98", "Theorem 2.1 assuming F1, F2, A3, A4: u = K u_g + C with K > 0 (proof text:98)"),
 "E3-c044": ("L03", "100-101", "Remark 2.2: the theorem does not say any investor has CRRA"),
 "E3-c045": ("L03", "104", "Definition 2.3: every outcome positive so each x_i lies in the domain of A1"),
 "E3-c046": ("L03", "106-110", "Proposition 2.4: g != 1 gives M^{1/s}, g = 1 gives exp(sum p ln x); proof text:110"),
 "E3-c047": ("L03", "112-113", "Example 2.5: 1600 cents (g=2) and 2000 cents (g=1); recomputed (numbers_L01_L04.out)"),
 "E3-c048": ("L03", "115-119", "Proposition 2.6 for k > 0, all real g; proof uses (k x)^s = k^s x^s"),
 "E3-c049": ("L03", "121-125", "Proposition 2.7 for a > 0 and real b; proof text:125"),
 "E3-c050": ("L03", "127-128", "Remark 2.8 rounding rule (floor(v+1/2) for v >= 0, one rounding). Ungraded convention; see notes"),
 "E3-c051": ("L03", "282-284", "Misconception 1: utility changes with w; r_R = g constant; r_A = g/w falls for g > 0"),
 "E3-c052": ("L03", "80-81", "Example 1.5: g = 0 gives u_0 = w - 1, affine with slope 1; ranking as w does via L01 Proposition 3.3 and Definition 3.2"),
 "E3-c053": ("L03", "276, 383-388", "Lab 1 checks six exponents for one lottery; Problem R3 text:388 says a proof needs a general argument not given here"),
 "E3-c054": ("L03", "248-253", "Lab 1 output: 11250.0000, 10000.0000, 8888.8889, 7337.6161 cents (recomputed to 4 dp, numbers_L01_L04.out); values fall over the six grid values (text:258 ff.)"),
 "E3-c055": ("L03", "358, 254", "Problem E2 text:358: M = 9/80000 so CE = 80000/9 = 8888.888...; Lab 1 prints 80000/9 (text:254)"),
 "E3-c168": ("L03", "128", "Remark 2.8 proof: |R(kv)-kv| <= 1/2, |kR(v)-kv| <= k/2, triangle inequality gives (k+1)/2; 20000 random draws give ratio <= 0.91 of the bound (card_checks_f6.out, numbers_L01_L04.out)"),
 "E3-c171": ("L03", "231-232, 263-264", "Homogeneity line in Lab 1 for k = 2, 3, 10 at the six gamma values; output True (text:263)"),
 "E3-c160": ("L03", "211-212, 260", "Lab 1 gamma = 1 +/- 1e-6 line: within 0.01 cents (text:260 True); the card says only floating-point agreement"),
 "E3-c175": ("L03", "46", "A2 text: limit (e^h-1)/h = 1 taken as given; M1 L03 defines e = e^1 (course/modules/M/M1/L03.html) and has no derivation of the limit (text/M1-L03.txt; grep 'lim' finds none)"),
 "E3-c177": ("L03", "70-78, 82-83, 211", "Proposition 1.4 (limit to ln w), Definition 1.3 (g = 1 member), Lab 1 gamma=1 +/- 1e-6 line (text:211)"),
 "E3-c056": ("L04", "48-49", "Definition 1.1: F_X(t) = P(X <= t), I_X(t) = integral of F_X from minus infinity to t"),
 "E3-c057": ("L04", "51-55", "Lemma 1.2 statement (I_X(t) = E(t-X)^+, z^+ = max(z,0)) and proof text:55"),
 "E3-c058": ("L04", "57-58", "Definition 1.3: F_X <= F_Y for all t; text:58 'at least as likely as Y to exceed every level t' (P(X>t) >= P(Y>t))"),
 "E3-c059": ("L04", "60-61", "Definition 1.4: u(s_j) <= u(s_{j+1}) for each j"),
 "E3-c060": ("L04", "63-73", "Theorem 1.5 under A1 (statement text:64, proof text:67-73)"),
 "E3-c061": ("L04", "75-79", "Lemma 1.6 under A1: all real t reduce to support points (proof text:79)"),
 "E3-c062": ("L04", "84-88", "Proposition 1.8: FOSD implies I_X <= I_Y, without A2 (text:85, proof text:88)"),
 "E3-c063": ("L04", "92-93", "Definition 2.1 under A1 and A2: I_X(t) <= I_Y(t) for every real t"),
 "E3-c064": ("L04", "95-99", "Lemma 2.2 under A1 and A2; affine on each interval, equal means at the top (text:99)"),
 "E3-c065": ("L04", "101-115", "Theorem 2.3 under A1, A2 for nondecreasing concave u on S (statement text:102; proof text:105-115)"),
 "E3-c066": ("L04", "118", "Remark 2.4: the only-if proof uses concavity (c_j >= 0) and A2, not monotonicity"),
 "E3-c067": ("L04", "121-125, 379-383", "Example 2.5 integrated values; named pair A output text:382-383 match; recomputed (numbers_L01_L04.out)"),
 "E3-c068": ("L04", "127", "Example 2.5: F_X(2000)=1/2 > 1/4 = F_Y(2000) and F_Y(3000)=3/4 > 1/2 = F_X(3000); SOSD X dominates Y (named pair A output text:381)"),
 "E3-c070": ("L04", "81-82", "Example 1.7: F_X = (1/2, 1/2, 1), F_Y = (0, 1/2, 1) on 2000, 3000, 4000; Y dominates X (recomputed)"),
 "E3-c071": ("L04", "540-545", "Problem R3 statement text:541 and solution text:545: b_1 = sigma_{m-1} >= 0 by monotonicity; I(s_m) = s_m - mean gives E X >= E Y, so A2 is not needed"),
 "E3-c072": ("L04", "439-441", "Misconception 1: equal means are a hypothesis of Theorem 2.3, not a ranking; Example 2.6 has equal means and no FOSD"),
 "E3-c073": ("L04", "443-445, 409, 412", "Misconception 2 (text:445) with lab pairs 16 and 19 SOSD 'no ranking' (text:409, 412); applies only to equal means"),
 "E3-c074": ("L04", "447-449", "Misconception 3: the two tests compare different objects; Example 2.5 is SOSD without FOSD"),
 "E3-c075": ("L04", "417-418", "Lab 1 FOSD counts 3/10/1/10 and 24 of 24 agreement (text:417-418); recounted from the 24 pair lines (text:393-416)"),
 "E3-c076": ("L04", "420-421", "Lab 1 SOSD counts 3/2/1/2 on 8 equal-mean pairs and 8 of 8 agreement (text:420-421)"),
 "E3-c077": ("L04", "425-435, 522", "Section 3: the test set is finite and the lab does not check the quantifier over all nondecreasing or concave utilities"),
 "E3-c167": ("L04", "60-61", "Definition 1.4 concavity by nonincreasing chord slopes sigma_j on the support"),
}
assert len(EV) == 86, len(EV)  # 87 slice cards minus c178 (FAIL row written separately)

def card_row(cid):
    lesson = cards[cid]["lesson"]
    lsn, loc, what = EV[cid]
    assert lsn == lesson, (cid, lsn, lesson)
    grade = cards[cid].get("grade")
    kind = {"T": "T", "C": "C"}.get(grade, "definition/convention")
    ev = (f"{what}. Card text: cards.json:{line_of[cid]}. Lesson locator {tx(lesson, loc)} (text dump of {lesson}.html, see {S}/strip.py)."
          f" Grade {grade}, basis {cards[cid].get('basis')!r}.")
    return {"id": f"E3f-{cid}", "check": "2.7-cards", "location": f"course/modules/E/E3/cards.json:{line_of[cid]} ({cid}, {lesson})",
            "status": "PASS", "evidence": ev}

slice_ids = sorted(c for c in cards if cards[c]["lesson"] in ("L01", "L02", "L03", "L04"))
assert len(slice_ids) == 87, len(slice_ids)
rows = []
for cid in slice_ids:
    if cid == "E3-c178":
        continue
    rows.append(card_row(cid))

rows.append({
 "id": "E3f-E3-c178", "check": "2.7-cards-duplicates",
 "location": f"course/modules/E/E3/cards.json:{line_of['E3-c178']} (E3-c178, L03); duplicates E3-c024 at cards.json:{line_of['E3-c024']} (L02)",
 "status": "FAIL",
 "evidence": ("E3-c178 (new in this delta) asks 'What are the Arrow-Pratt measures ... as recalled in L03 Definition 1.6?' and answers r_A = -u''/u' and r_R = w r_A. "
   "E3-c024 (L02) asks 'What are the Arrow-Pratt absolute and relative risk aversion?' with the same two formulas (Definition 2.1, text/L02.txt:108-109). "
   "Same question, same answer (a semantic duplicate that string similarity misses): a duplicate card, which VERIFIER_RULES 2.7 and BUILDER_RULES 7 do not allow. The one fact Definition 1.6 adds, the domain condition (twice differentiable on (0, infinity) with u' > 0), is not on the card. "
   f"Lesson text: text/L03.txt:83-84. Scan: {S}/dup_scan_f6.out (the automatic string scan does not flag c024/c178: front similarity 0.29, back 0.56; the duplicate is semantic, found by reading the two cards side by side)."),
 "fix": ("Delete E3-c178 from course/modules/E/E3/cards.json (E3-c024 already carries the definition), or replace it with the fact Definition 1.6 adds: "
   "front 'Which hypothesis must u satisfy for the Arrow-Pratt measures of Definition 1.6 to be defined on (0, infinity)?'; back 'u is twice differentiable on (0, infinity) with u'(w) > 0 for every w > 0, so r_A = -u''/u' is defined at every w; r_R = w r_A.'; grade T. Then run check_pages.py --unit E3."),
})

rows.append({
 "id": "E3f-cards-near-duplicates", "check": "2.7-cards-duplicates",
 "location": "course/modules/E/E3/cards.json (all 171 cards; slice cards L01-L04)",
 "status": "FAIL",
 "evidence": (f"Exact check PASS: 0 duplicate ids, 0 duplicate normalised fronts or backs ({S}/card_checks_f6.out). Near-duplicate scan ({S}/dup_scan_f6.py, output {S}/dup_scan_f6.out) reviewed for slice cards: "
   "c024 vs c178 is the same fact asked twice (FAIL, row E3f-E3-c178). c006 vs c015 share the risk-neutral identity E u = b E X but ask different questions (definition vs misconception): PASS. "
   "c040 vs c177 share Proposition 1.4 (the limit to ln w) but ask different questions (limit vs whether log is a separate case): PASS. Other scan hits are cross-lesson with other slices or are different facts."),
 "fix": "Resolve E3f-E3-c178 (delete or replace the card as stated there). No other change required by this row.",
})

rows.append({
 "id": "E3f-references", "check": "2.4-attributions",
 "location": "course/modules/E/E3/L02.html:616 (References paragraph, 'Pratt (1964) is one of the core readings of E3...')",
 "status": "FAIL",
 "evidence": ("Round 5 passed this row on the ground that the name is used for the name only. On re-check the sentence writes a reference in free text: 'Pratt (1964)'. "
   "BUILDER_RULES 1.1 says 'Cite only keys that exist in references/references.json. Never write a reference in free text.' The lesson names no key; the other E3 and E2 reference paragraphs list keys (E2 lesson 1: 'Registry keys cited on this page: nash1950equilibrium, ...'). "
   "The content is correct: references/references.json record key pratt1964risk (lines 19433-19465) has Pratt, John W., 'Risk Aversion in the Small and in the Large', Econometrica, volume 32, issue 1/2, year 1964, used_by E3; the year and venue in the prose match. The defect is the form of the citation. "
   "Lesson text: text/L02.txt:535. The L02 text does not attribute any result to Pratt; the Section 9 sentence 'attributes no passage or result to it' is consistent with the record."),
 "fix": ("In course/modules/E/E3/L02.html References paragraph, replace the bare 'Pratt (1964)' with the key: 'Registry keys cited on this page: pratt1964risk, the registry entry for Pratt, Risk Aversion in the Small and in the Large, Econometrica (1964), which this lesson names for the name only; no passage, page or result is attributed to it.' "
   "Keep the grade-T sentence. Then run check_pages.py --unit E3 and check_dag.py --unit E3."),
})

rows.append({"id": "E3f-lesson-numbers-L01", "check": "2.2-numbers", "location": "course/modules/E/E3/L01.html (prose, misconceptions, problems, quiz, key results)",
 "status": "PASS", "evidence": (f"Independent recomputation with exact Fractions and floats in {S}/numbers_L01_L04.py (output {S}/numbers_L01_L04.out): EV 15000/12500/15000; EU linear = EV; EU quadratic 45000/21250/37500; Example 3.4 37500 CU^2; M1 59, 4030, 3481, 549; M2 400/3 both sides; M3 65 and 95; E2 40000; R3 25000 vs 22500; mixture weight 5/12. Prose matches (text:57, 116, 271, 287, 308-323 of L01)."
   " Lab output Parts A-D (text:247-269) match the recomputed values.")})
rows.append({"id": "E3f-lesson-numbers-L02", "check": "2.2-numbers", "location": "course/modules/E/E3/L02.html (Example 1.5, Example 2.3, Lab 1 prose, Section 4, E1-E3, misconceptions)",
 "status": "PASS", "evidence": (f"{S}/numbers_L01_L04.out: E sqrt(W) = 9.743416490, CE = 94.9341649 (prints 94.934165), premium 5.065835 (cents 9493.4165 -> 9493, 506.5835 -> 507); variance 1800; Pratt 4.5; half-variance 900; error 0.565835 = 11.17 percent of the exact premium (0.11170, text:323) and 12.57 percent of the approximation; ratios at eps 1, 0.5, 0.25, 0.1, 0.01 = 5.065835, 4.619495, 4.528811, 4.504565, 4.500046; E1 gap ratio 6.31 vs eps^2 factor 6.25. All match text:304-318 and the prose.")})
rows.append({"id": "E3f-lesson-numbers-L03", "check": "2.2-numbers", "location": "course/modules/E/E3/L03.html (Lab 1 prose, Example 2.5, M1-M3, E1-E3, misconceptions)",
 "status": "PASS", "evidence": (f"{S}/numbers_L01_L04.out: CE at gamma 0, 0.25, 0.5, 1, 2, 4 = 11250.0000, 10931.7733, 10615.8009, 10000.0000, 8888.8889, 7337.6161, cents 11250, 10932, 10616, 10000, 8889, 7338; 80000/9 and M = 9/80000; Example 2.5 1600 and 2000; M1 r_A(4)=1/8, r_R=1/2; M2 CE = 3000 and E = 7000; M3 CE = 9000; (k+1)/2 = 5.5; A2 limit check. All match text:246-264, 292, 347-365.")})
rows.append({"id": "E3f-lesson-numbers-L04", "check": "2.2-numbers", "location": "course/modules/E/E3/L04.html (Examples 1.7, 2.5, 2.6; M1-M3; E1; lab counts)",
 "status": "PASS", "evidence": (f"{S}/numbers_L01_L04.out: Example 2.5 I_X = 0, 0, 500, 1000, 2000 and I_Y = 0, 250, 500, 1250, 2000, means 3000 and 3000; F_X, F_Y at support points as printed; Example 2.6 I_X = 0, 500, 1000, 1500, 2000 and I_Y = 0, 0, 0, 1000, 2000; Example 1.7 F; pair B I_Y(4000) = 500; means 3000 and 3500; M1 means 2500 and 2000. Seeded-pair counts 3/10/1/10 and 2/8 agree with text:393-421 (per-pair lines tallied by hand).")})

rows.append({"id": "E3f-lab-L01", "check": "2.5-labs", "location": "course/modules/E/E3/L01.html lab-E3-L01-1; tests/labs/E3/lab-E3-L01-1.py",
 "status": "PASS", "evidence": f"run_labs.py --unit E3: 'run_labs E3: PASS (11/11)', rc 0 ({S}/run_labs_E3.out). Twin run alone: python -I -W error exit 0, stderr 0 bytes ({S}/stderr_lab-E3-L01-1.py.txt, {S}/twin_L01.out). Page code equals twin and expected block equals output under run_labs; ruff and format clean ({S}/ruff_twins_L01_L04.out); mypy --strict --no-incremental on the twin clean ({S}/mypy_twins_L01_L04.out). Output checked against text:247-269."})
rows.append({"id": "E3f-lab-L02", "check": "2.5-labs", "location": "course/modules/E/E3/L02.html lab-E3-L02-1; tests/labs/E3/lab-E3-L02-1.py",
 "status": "PASS", "evidence": f"run_labs E3 PASS (11/11) ({S}/run_labs_E3.out); twin alone under -I -W error exit 0, stderr 0 bytes ({S}/stderr_lab-E3-L02-1.py.txt, {S}/twin_L02.out); ruff, format and mypy clean ({S}/ruff_twins_L01_L04.out, {S}/mypy_twins_L01_L04.out). Hypothesis text:159 matches the printed results (text:304-317)."})
rows.append({"id": "E3f-lab-L03", "check": "2.5-labs", "location": "course/modules/E/E3/L03.html lab-E3-L03-1; tests/labs/E3/lab-E3-L03-1.py",
 "status": "PASS", "evidence": f"run_labs E3 PASS (11/11) ({S}/run_labs_E3.out); twin alone under -I -W error exit 0, stderr 0 bytes ({S}/stderr_lab-E3-L03-1.py.txt, {S}/twin_L03.out); ruff, format, mypy clean. Hypothesis (text:132) predicts 11250, 10000, 8888.89 -> 8889 and the falling order; all printed (text:246-264)."})
rows.append({"id": "E3f-lab-L04", "check": "2.5-labs", "location": "course/modules/E/E3/L04.html lab-E3-L04-1; tests/labs/E3/lab-E3-L04-1.py",
 "status": "PASS", "evidence": f"run_labs E3 PASS (11/11) ({S}/run_labs_E3.out); twin alone under -I -W error exit 0, stderr 0 bytes ({S}/stderr_lab-E3-L04-1.py.txt, {S}/twin_L04.out); ruff, format, mypy clean. Seeded pairs are SIMULATED and labelled (text:138); counts 24/24 and 8/8 agree with the printed lines (text:393-421). Named pairs match Examples 1.7, 2.5, 2.6 (text:379-392)."})

rows.append({"id": "E3f-dag-L02-crra-forward-use", "check": "2.9-define-before-use",
 "location": "course/modules/E/E3/L02.html:159 (Example 2.3) and L02.html:429 (solution to M2) (both re-read at 142ecfc)",
 "status": "PASS",
 "evidence": ("Round-5 FAIL re-verified on this pin. The subject changed (Example 2.3 and M2 solution edited in 6de369ce..142ecfc), so it was re-checked from scratch. "
   "Example 2.3 now reads 'The function v(w) = 2 sqrt(w) - 2 is a positive affine image of the square root ... by Proposition 2.2 with b = 2' (text/L02.txt:118): no L03 Definition, no u_{1/2}, no power family. "
   "M2 solution now reads 'relative risk aversion equal to 1 at every w > 0' (text/L02.txt:363). grep of L02.html: the only 'L03' is the nav link (NextL03, href L03.html); the only 'Definition 1.3' refers to L01 (line 454). "
   f"check_dag.py --unit E3: PASS ({S}/check_dag_E3.out)."),
})

rows.append({"id": "E3f-dag-other-links", "check": "2.9-define-before-use",
 "location": "course/modules/E/E3/L01.html..L04.html data-concept links and <dfn> tags",
 "status": "PASS",
 "evidence": ("Links: L01 uses random-variable, expectation (concepts.html); L02 uses expected-utility (L01.html#def-expected-utility), derivative, expectation, variance (concepts.html); L03 links L01 expected-utility, L02 arrow-pratt-risk-aversion and certainty-equivalent, concepts random-variable, expectation, derivative, exponential-and-logarithm; L04 links L01 expected-utility and L03 crra-utility (#def-crra-utility, defined at L03.html:88). "
   "No link points to a later lesson. Each dfn id is defined once: expected-utility (L01), certainty-equivalent and arrow-pratt-risk-aversion (L02), crra-utility (L03), first- and second-order-stochastic-dominance (L04). "
   f"Forward prose: L02 text:325 names L06 and L07 by lesson, not by concept (allowed). check_dag.py PASS ({S}/check_dag_E3.out).")})

rows.append({"id": "E3f-coverage-cards", "check": "2.7-cards-coverage",
 "location": "course/modules/E/E3/cards.json (cards for L01-L04)",
 "status": "PASS",
 "evidence": ("Every Definition, Proposition, Lemma, Theorem, Remark and misconception block of L01-L04 has a card (text dumps of each lesson, with the lesson's own headings). L01: Def 1.1-1.3, A1, Def 2.1, Prop 2.2, 2.3, Remark 2.4, Def 3.2, Prop 3.1, 3.3, Misc 1-3, P2, R1, Lab 1 A and B (c001-c017, c173). "
   "L02: A2, Prop 1.1, Def 1.2, Prop 1.3(a)(b), Remark 1.4, Def 2.1, Prop 2.2, Example 2.3, Prop 3.1, Remark 3.2, A5, Misc 1-3, Lab 1 A, B, C (c018-c035, c159, c161, c162, c174). "
   "L03: Def 1.1, Prop 1.2, Def 1.3, Prop 1.4, Ex 1.5 (c052), Prop 1.7, Thm 2.1, Remark 2.2, Def 2.3, Prop 2.4, Ex 2.5, Prop 2.6, Prop 2.7, Remark 2.8, Def 1.6 (c178, see FAIL), Misc 1-3, Lab 1 (c053, c054, c055, c160, c168, c171, c175, c177). "
   "L04: Def 1.1, Lemma 1.2, Def 1.3, Def 1.4, Thm 1.5, Lemma 1.6, Ex 1.7, Prop 1.8, Def 2.1, Lemma 2.2, Thm 2.3, Remark 2.4, Ex 2.5, Ex 2.6 (c068), Problem R3 (c071), Misc 1-3, Lab 1 (c056-c077). Assumptions A1-A4 of L02 and F1-F6 are not separate cards (not required).")})

rows.append({"id": "E3f-cards-integrity", "check": "2.7-cards-integrity", "location": "course/modules/E/E3/cards.json (171 cards, all lessons)",
 "status": "PASS",
 "evidence": f"{S}/card_checks_f6.out: cards 171, duplicate ids [], duplicate normalised fronts [], duplicate normalised backs []. JSON parses; every slice card has front, back, lesson in {{L01..L04}}, and an id of the form E3-cNNN. Near-duplicate defect is separate (row E3f-cards-near-duplicates)."})
rows.append({"id": "E3f-cards-numbers", "check": "2.7-cards-numbers", "location": "course/modules/E/E3/cards.json slice cards vs L01-L04.html",
 "status": "PASS",
 "evidence": f"{S}/card_checks_f6.py: every numeric token (excluding 0-6 and 10) in the 87 slice cards occurs in its own lesson text or HTML; 'numeric tokens absent from own lesson: []' ({S}/card_checks_f6.out). Values checked by recomputation (numbers_L01_L04.out)."})
rows.append({"id": "E3f-cards-xrefs", "check": "2.7-cards-refs",
 "location": "course/modules/E/E3/cards.json labelled references in the slice",
 "status": "PASS",
 "evidence": "Labelled references resolve inside the named lesson: Definitions 1.1-3.2, Propositions 1.1-3.3 and Theorem/Lemma numbers (text dumps), Problems P2 (L01 text:333), R1 (L01 text:372), R2 (L02 text:427), R3 (L03 text:383; L04 text:540), E2 (L03 text:353), Example 1.5 / 2.3 / 2.5 / 2.6 / 1.7, Remarks 1.4, 2.2, 2.4, 2.8, 3.2, and 'section 4' / 'section 5' / 'section 3' (sections present in each lesson; text:275, 319, 343, 425). L01 card E3-c004 cites Section 4 for a statement A1 makes (observation in notes)."})
rows.append({"id": "E3f-cards-grades", "check": "2.7-cards-grades", "location": "course/modules/E/E3/cards.json grade and basis fields for the slice",
 "status": "PASS",
 "evidence": "Every C card in the slice names a lab part or line with its printed output: E3-c016, c017 (L01 Part A, B), c032-c035 (L02 Parts A, B, C), c054, c160, c171 (L03 lab lines), c073, c075, c076 (L04 lab counts), c161 (L02 Part B). Each has grade C and a basis (check_pages.py enforces cite-or-basis for non-T grades; PASS: {S}/check_pages_E3.out). Every T card is a theorem, proposition, derivation, definition or a statement proved on the page; proofs sit at the locators given per card. Grade-C lab results are not promoted to T anywhere in the slice."})
rows.append({"id": "E3f-notation", "check": "2.13-notation", "location": "course/modules/E/E3/L01.html..L04.html math; notation/notation.json",
 "status": "PASS",
 "evidence": f"{S}/notation_macros_f6.py ({S}/notation_macros_f6.out): slice macros used are only registered ones (\\E, \\Prob, \\Var, \\R, \\indic); none of the registered symbols T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{{e\\ast}}, R_f, \\mathbb{{Q}} appears in math. Local letters (gamma, s, L, M, C, K, I, S, sigma, u, v, w, pi) are defined where first used, as BLUEPRINT and the plan permit; no registered meaning is reused. Assumption labels are reused across lessons (observation in notes)."})
rows.append({"id": "E3f-banned-and-process", "check": "1.3-1.4-banned", "location": "course/modules/E/E3/L01.html..L04.html and slice cards",
 "status": "PASS",
 "evidence": f"Banned-phrase and process-word grep over the four text dumps and cards ({S}/banned_process_f6.out): no TODO, TBD, lorem, 'for brevity', 'details omitted', 'beyond the scope', 'left as an exercise', 'you can add more', 'it is important to note', 'studies show', 'experts agree', 'well known', 'obviously', 'clearly', 'verifier', 'builder', 'architect', 'round N', 'revised'. The seven hits are 'fixed' in mathematical sense (fixed lottery, fixed w) and are not process words."})
rows.append({"id": "E3f-hours", "check": "2.12-hours", "location": "course/modules/E/E3/L01.html..L04.html data-hours; index.html",
 "status": "PASS", "evidence": "Each lesson data-hours=\"7\" (grep of L01-L04.html, output in this round's check); the study-hours eyebrow reads 7 for each. The hub split (56 lesson hours + 14 project = 70) is outside this slice and was checked by round 5 and by the unchanged index.html for these lessons."})
rows.append({"id": "E3f-delta", "check": "0-delta", "location": "git diff 440ed3c..142ecfc for course/modules/E/E3 (slice files)",
 "status": "PASS", "evidence": "Every slice hunk read: L01.html:453 (R3 wording: 'check, for that pair'); L02.html:149 (Prop 2.2 wording), L02.html:159 (Example 2.3, forward reference removed), L02.html:209 (Lab 1 hypothesis: 'each scale that Part A and Part C print'), L02.html:429 (M2 solution); L03.html:393 (P1 solution: hypotheses a>0 and existence/uniqueness); cards.json:1169-1172 (E3-c175 wording), cards.json:1182 (E3-c178 new, FAIL row). Outside this slice: cards.json:587-590 (E3-c088, L05), E3-c148/c151/c152 (L08), E3-c179 (L08, cards.json:1188). The round-5 FAIL was fixed and is re-verified (row E3f-dag-L02-crra-forward-use)."})
rows.append({"id": "E3f-cmd-check_pages", "check": "command", "location": "course/modules/E/E3/", "status": "PASS",
 "evidence": f"check_pages.py --unit E3: 'check_pages E3: PASS' ({S}/check_pages_E3.out). Card rule for C-grade basis holds."})
rows.append({"id": "E3f-cmd-check_dag", "check": "command", "location": "course/modules/E/E3/", "status": "PASS",
 "evidence": f"check_dag.py --unit E3: 'check_dag E3: PASS' ({S}/check_dag_E3.out). The unrelated define-before-use is verified by row E3f-dag-L02-crra-forward-use."})
rows.append({"id": "E3f-cmd-page_smoke", "check": "command", "location": "course/modules/E/E3/L01.html..L04.html", "status": "PASS",
 "evidence": f"page_smoke.py --unit E3 --pages L01 L02 L03 L04 (stems, not .html names; the first attempt with .html names matched no page and was discarded): each page PASS, labs run in the runtime, 'page_smoke E3: PASS' ({S}/page_smoke_L01_L04.out)."})
rows.append({"id": "E3f-cmd-pytest-labs", "check": "command", "location": "tests/test_labs.py -k E3", "status": "PASS",
 "evidence": f"pytest tests/test_labs.py -k E3 -q: 15 passed, rc 0 ({S}/pytest_labs_E3.out). pytest tests/test_page_checks.py tests/test_run_labs.py -q: passed, rc 0 ({S}/pytest_page_checks.out)."})
rows.append({"id": "E3f-cmd-ruff-labs", "check": "command", "location": "tests/labs/E3/lab-E3-L01-1.py..L04-1.py", "status": "PASS",
 "evidence": f"ruff check on the four twins: 'All checks passed!' rc 0; ruff format --check: '4 files already formatted' rc 0 ({S}/ruff_twins_L01_L04.out)."})
rows.append({"id": "E3f-cmd-mypy-twins", "check": "command", "location": "tests/labs/E3/lab-E3-L01-1.py..L04-1.py", "status": "PASS",
 "evidence": f"mypy --no-incremental on the four twins: 'Success: no issues found in 4 source files' rc 0 ({S}/mypy_twins_L01_L04.out). Whole-project mypy not re-run (no Python tool changed in the delta)."})
rows.append({"id": "E3f-cmd-verify_refs", "check": "command", "location": "references/references.json (key pratt1964risk)", "status": "PASS",
 "evidence": f"verify_refs.py --offline: 'offline integrity: 560 entries, 0 problems', rc 0 ({S}/verify_refs_offline.out). verify_refs.py --unit E3 (live Crossref): '5 of 560 entries, 0 problems', rc 0 ({S}/verify_refs_E3_live.out). git status after both runs shows no tracked change."})
rows.append({"id": "E3f-cmd-check_projects", "check": "command", "location": "course/modules/E/E3/project.html", "status": "PASS",
 "evidence": f"check_projects.py --unit E3: 'check_projects E3: PASS' rc 0 ({S}/check_projects_E3.out). Project is outside this slice; run because it is in the unit gate."})

fragment = {
 "unit": "E3", "slice": "f", "round": 6,
 "verifier": "Claude Haiku 5.5, independent verifier for E3 slice f, round 6 (did not build E3; cards of L01-L04 against their lessons: hypotheses, grades, bases, numbers, duplicates, define-before-use).",
 "pin": "142ecfc2bd27061de18bd67e83df81e69f5c249d (142ecfc, detached)",
 "base": "440ed3c8216725d498d9c6d7c746907d4d418198 (round-5 pin; frags/D-E3-f.round5.json). Delta touching the slice: L01.html R3, L02.html Prop 2.2, Example 2.3, Lab 1 hypothesis, M2 solution, L03.html P1 solution, cards.json E3-c175 (wording), E3-c178 (new, L03).",
 "checkout": "/Users/billyribeiro/.fanout/wt/verifyD6-E3-f",
 "scratch": "ledgers/E3/scripts/E3-f-r6/",
 "verified_at": datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat(),
 "verdict": None,
 "rows": [r for r in rows if r],
 "mutants": [],
 "registry_flags": [],
 "freshness_flags": [],
 "notes": [
   "Mutants: not required. The slice is lessons and cards; the lab twins are demonstrations and mutation testing applies to project graders only (ruling). No mutants were written, so mutants is empty.",
   "Observation (not a row): E3-c050 (Remark 2.8 rounding rule) has no grade. It is a unit convention; if the architect wants every convention graded C with a basis, grade it 'C' with basis 'unit convention, Remark 2.8'.",
   "Observation (not a row): E3-c013 asks 'which one maximizes expected utility' (singular); R1 shows several lotteries attain the maximum. The answer is one maximizer and is correct as stated.",
   "Observation (not a row): E3-c004 cites Section 4 for 'no result covers infinitely many outcomes'; Section 4 (text:275) says 'continuum' and A1 (text:54) says 'infinitely many'. Adding A1 to the locator would make the card exact.",
   "Observation (not a row, plan §7): the convex-function row asks for no M7 name in L02 and L04. L04.html:669 (quiz option 'Nonincreasing convex utilities') uses the name. The architect default allows plain-prose names outside the closure, so this is not a FAIL; replacing the option with 'Nonincreasing concave utilities' would keep the distractor and meet the plan row. L01 uses 'convex' in plain prose (L01.html:236, 452, 508) under the same default.",
   "Observation (not a row): assumption labels are reused with different content across lessons (A1 is finite support in L01, L02 and L04 and positive wealth in L03; A2 is concavity in L02, the exponential limit in L03, equal means in L04). Every card qualifies its label with the lesson, so no card is wrong.",
   "Observation (not a row): the hub text (text/hub.txt:142) says 'Lesson 2 names Pratt (1964) for the name only'; it is outside this slice, and the FAIL row E3f-references asks for the key markup in L02 only.",
   "Pairs judged distinct (not rows): c006/c015 (definition and misconception share E u = b E X), c040/c177 (limit and misconception share Proposition 1.4), c160/c177.",
   "Carried or re-verified: every round-5 PASS row id is kept. Rows were re-derived from the pin on this round, not carried, because the slice's text and cards changed in the delta (L01 R3, L02 Prop 2.2, Example 2.3, M2, Lab 1 hypothesis, L03 P1, cards c175 and c178).",
 ],
 "summary": {},
}
statuses = [r["status"] for r in fragment["rows"]]
fragment["verdict"] = "PASS" if all(s == "PASS" for s in statuses) else "FAIL"
fragment["summary"] = {"rows": len(statuses), "pass": statuses.count("PASS"), "fail": statuses.count("FAIL"), "unverifiable": statuses.count("UNVERIFIABLE")}
with open("ledgers/E3/E3-f.json", "w", encoding="utf-8") as fh:
    json.dump(fragment, fh, indent=1, ensure_ascii=False)
    fh.write("\n")
print(json.dumps(fragment["summary"]), fragment["verdict"])
