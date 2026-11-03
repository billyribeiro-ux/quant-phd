"""E3 slice f round 3: writes ledgers/E3/E3-f.json from the per-card verification notes below.

Run from the checkout root: python3 -I ledgers/E3/scripts/E3-f-r3/build_fragment.py
Every card row was checked by reading cards.json and the cited lesson lines in this round; the numeric,
reference and duplicate checks are scripts in this directory whose outputs are in out_*.txt.
"""
import json
import subprocess
from datetime import UTC, datetime

ROOT = "/Users/billyribeiro/.fanout/wt/verifyD3-E3-f/"
PIN = "a007712fdbfc8b4851123f4de76b5310ac5a9e64"

# id: (cards.json line, lesson, lesson locators read, what was checked)
CARDS = {
    "E3-c001": (3, "L01", "L01.html:59 (Definition 1.1)", "finite list, distinct outcomes, p_i >= 0, sum 1; random-variable equivalence matches"),
    "E3-c002": (9, "L01", "L01.html:63-64 (Definition 1.2)", "E X = sum p_i x_i matches"),
    "E3-c003": (15, "L01", "L01.html:67-69 (Definition 1.3)", "E u(X) = sum p_i u(x_i); depends on u as well as on the lottery"),
    "E3-c004": (21, "L01", "L01.html:72-74 (A1) and :331 (section 4)", "A1 finite outcomes; no result covers infinitely many outcomes"),
    "E3-c005": (27, "L01", "L01.html:86 (Definition 2.1)", "mixture on the union of outcomes with the p_L(x)=0 convention"),
    "E3-c006": (33, "L01", "L01.html:141-143 (Definition 3.2)", "u = bx with b > 0 is risk neutral; E u = b E X"),
    "E3-c007": (39, "L01", "L01.html:89-91 (Proposition 2.2, T) and :94-101 (proof)", "under A1 a mixture is a finite lottery; hypothesis A1 stated"),
    "E3-c008": (46, "L01", "L01.html:103-108 (Proposition 2.3, T, A1, u real-valued)", "linearity in the probabilities; hypotheses stated"),
    "E3-c009": (53, "L01", "L01.html:124-126 (Remark 2.4)", "identity about Definition 1.3; no claim on preference orderings"),
    "E3-c010": (60, "L01", "L01.html:131-133 (Proposition 3.1, T, A1)", "E u = a + b E X; a=0, b=1 gives the expected value"),
    "E3-c011": (67, "L01", "L01.html:146-148 (Proposition 3.3, T, A1, b > 0)", "positive affine transformation keeps the ranking"),
    "E3-c012": (74, "L01", "L01.html:395-398 (Problem P2)", "b < 0 reverses the ranking; P2 states it for finite lotteries"),
    "E3-c013": (81, "L01", "L01.html:437-441 (Problem R1) and :471 (key results)", "maximum at a sure best outcome; equality only on maximisers; finite set of outcomes"),
    "E3-c014": (88, "L01", "L01.html:77-79 (Example 1.4) and :342-343 (section 5, misconception 1)", "u(E X)=150^2=22500 against E u(X)=45000 CU squared; recomputed"),
    "E3-c015": (95, "L01", "L01.html:143 (Definition 3.2) and :346-347 (misconception 2)", "risk neutral EU = b E X, probability-weighted; probabilities enter"),
    "E3-c016": (102, "L01", "L01.html:302-305 (Lab 1 Part A expected output), code :260-265", "EV 15000, 12500, 15000; quadratic EU 45000, 21250, 37500; recomputed exactly; grade C basis is the lab"),
    "E3-c017": (110, "L01", "L01.html:267-276 (Part B code), :306-313 (output), :163 (hypothesis)", "six comparisons at alpha 1/4, 1/3, 1/2 under two utilities, all True in the output"),
    "E3-c173": (1162, "L01", "L01.html:350-352 (section 5, misconception 3)", "b = 0 gives E v(L) = a for every lottery, so every pair ties; grade T derivation"),
    "E3-c018": (118, "L02", "L02.html:73-75 (A2)", "u twice differentiable on open I, u' > 0, u'' <= 0; concavity defined by the sign of u''"),
    "E3-c019": (124, "L02", "L02.html:88-90 (Proposition 1.1, T) and :92-95 (proof)", "exactly one c in I; hypotheses F1, F5, A1 to A3 match"),
    "E3-c020": (131, "L02", "L02.html:97-100 (Definition 1.2)", "unique c with u(c) = E u(X), CE(X; u)"),
    "E3-c021": (137, "L02", "L02.html:99 (Definition 1.2)", "the page says 'The phrase risk premium has other uses in finance ... On this page, ... nothing else'; the card states the phrase is used only in this sense without the page scope"),
    "E3-c022": (143, "L02", "L02.html:102-107 (Proposition 1.3(a), T) and :109-127 (proof)", "CE <= E X under F1, F2, F5, A1 to A3; tangent-line proof matches"),
    "E3-c023": (150, "L02", "L02.html:102-107 (Proposition 1.3(b)) and :83-85 (A4)", "strict inequality under A4 and an outcome with positive probability differing from E X"),
    "E3-c024": (157, "L02", "L02.html:142-145 (Definition 2.1)", "r_A = -u''/u' in 1/CU where u' != 0; r_R = w r_A dimensionless"),
    "E3-c025": (163, "L02", "L02.html:147-150 (Proposition 2.2, T) and :152-155 (proof)", "b > 0 cancels; v' = b u', v'' = b u''; matches"),
    "E3-c026": (170, "L02", "L02.html:157-160 (Example 2.3)", "r_A = 1/(2w), r_R = 1/2; 0.005 per CU and 0.5 at w = 100; prefix 'Assuming F6' present"),
    "E3-c027": (177, "L02", "L02.html:171-174 (Proposition 3.1, T; F1, F3, F4, F5; A1, A5) and :176-199 (proof)", "pi/eps^2 -> (1/2) r_A s^2 for E X = 0; hypotheses match"),
    "E3-c028": (184, "L02", "L02.html:202-205 (Remark 3.2)", "asymptotic; no bound at a fixed eps"),
    "E3-c029": (191, "L02", "L02.html:397-400 (section 5, misconception 1)", "900 CU squared half-variance, 4.5 CU Pratt, 5.065835 CU exact; units are CU squared as the page writes them (round-2 unit defect fixed)"),
    "E3-c030": (198, "L02", "L02.html:144, :159 (Example 2.3), :401-404 (misconception 2)", "prefix 'Assuming F6' present; r_A 0.005 per CU and r_R 0.5 at w = 100 recomputed"),
    "E3-c031": (205, "L02", "L02.html:405-408 (misconception 3) and :452-455 (Problem P2)", "u(w) = w gives CE = E X for every finite lottery in I; premium zero"),
    "E3-c032": (212, "L02", "L02.html:367 (Part A expected output), code :338-341", "ce_cents 9493, premium_cents 507 (half-up of 9493.4165 and 506.5835), r_A 0.005000, r_R 0.500000, exact 5.065835, approximation 4.500000, error 0.565835; all recomputed; grade C basis is the lab"),
    "E3-c033": (220, "L02", "L02.html:370-375 (Part B expected output), code :344-353", "premium/eps^2 at five scales 5.065835 (eps 1) to 4.500046 (eps 0.01); gaps shrink; recomputed"),
    "E3-c034": (228, "L02", "L02.html:387 (section 4, first bullet), :479 (Problem E2), :367", "0.565835 / 5.065835 = 11.1696 percent, so 11.17; basis is the exact premium; recomputed"),
    "E3-c035": (236, "L02", "L02.html:376-380 (Part C expected output), code :355-361", "linear premium 0 cents at eps 1.0, 0.5, 0.1; linear_premium_zero_at_three_scales True"),
    "E3-c159": (1064, "L02", "L02.html:113-127 (proof) and :131 (Remark 1.4)", "A2 in Step 1, F2 in Step 1, F5 for strict increase, F1 in Step 3, A3 for the outcomes; matches Remark 1.4"),
    "E3-c161": (1078, "L02", "L02.html:381 (interpretation), :502-504 (Problem R2), :164-165 (Part B)", "Part B is a five-scale numerical check, not a proof of the limit; grade C"),
    "E3-c162": (1086, "L02", "L02.html:131 (Remark 1.4, last sentence)", "u'' >= 0 case not stated as a result"),
    "E3-c174": (1169, "L02", "L02.html:166-169 (A5)", "open I containing w, u' > 0 on I; finitely many outcomes give small eps with w + eps x_i in I"),
    "E3-c036": (244, "L03", "L03.html:72-73 (Definition 1.1)", "w^a = e^(a ln w) for w > 0"),
    "E3-c037": (250, "L03", "L03.html:77-78 (Proposition 1.2, T) and :82-83 (proof)", "(w^a)^b = w^(ab); (xy)^c = x^c y^c"),
    "E3-c038": (257, "L03", "L03.html:87-89 (Definition 1.3)", "normalised CRRA form for gamma != 1 and ln w at gamma = 1"),
    "E3-c039": (263, "L03", "L03.html:90 (normalisation text), :94-96 (Proposition 1.4, A2)", "u_gamma(1) = 0; finite limit at gamma = 1 under A2; constant changes no CE (Proposition 2.7); prefix 'Assuming A2' present (round-2 fix verified)"),
    "E3-c040": (270, "L03", "L03.html:94-96 (Proposition 1.4, A2) and :99-102 (proof)", "limit ln w; h = s ln w identity recomputed"),
    "E3-c041": (277, "L03", "L03.html:116-118 (Proposition 1.7, F2) and :121-122 (proof)", "u' = w^-gamma, u'' = -gamma w^(-gamma-1), r_A = gamma/w, r_R = gamma; prefix 'Assuming F2' present"),
    "E3-c043": (284, "L03", "L03.html:127-129 (Theorem 2.1, F1, F2, A3, A4) and :133-134 (proof)", "u = K u_gamma + C with K > 0; hypotheses match"),
    "E3-c044": (291, "L03", "L03.html:138-139 (Remark 2.2)", "theorem does not say an investor has CRRA; no source cited"),
    "E3-c045": (298, "L03", "L03.html:143-144 (Definition 2.3)", "positive outcomes so each lies in the domain of A1"),
    "E3-c046": (304, "L03", "L03.html:148-149 (Proposition 2.4, T) and :153-154 (proof)", "gamma != 1: CE = M^(1/s); gamma = 1: exp(sum p ln x); hypotheses match"),
    "E3-c047": (311, "L03", "L03.html:158-159 (Example 2.5)", "1600 cents at gamma = 2 and 2000 cents at gamma = 1; recomputed"),
    "E3-c048": (318, "L03", "L03.html:163-164 (Proposition 2.6, T) and :168-169 (proof)", "homogeneity for positive outcomes and k > 0; (kx)^s = k^s x^s"),
    "E3-c049": (325, "L03", "L03.html:173-174 (Proposition 2.7, T) and :178-179 (proof)", "a > 0 and real b; CE exists and is unique; matches"),
    "E3-c050": (332, "L03", "L03.html:183-184 (Remark 2.8)", "round half up, floor(v + 1/2), applied once to the unrounded value"),
    "E3-c051": (338, "L03", "L03.html:344-345 (section 4, misconception 1) and :116-118 (Proposition 1.7)", "prefix 'Assuming F2' present; r_R constant; r_A = gamma/w falls when gamma > 0"),
    "E3-c052": (345, "L03", "L03.html:105-108 (Example 1.5); L01.html:146-148 (Proposition 3.3)", "gamma = 0: u_0 = w - 1, affine with slope 1; ranks as w"),
    "E3-c053": (352, "L03", "L03.html:307-325 (lab output), :335 (section 3, third bullet), :454-457 (Problem R3)", "Lab 1 checks six exponents for one lottery; R3 says a general argument is not given; grade T for the meta-claim"),
    "E3-c054": (359, "L03", "L03.html:309-314 (Part output for gamma 0, 1, 2, 4), grid :207", "11250.0000, 10000.0000, 8888.8889, 7337.6161 recomputed; grade C basis is the lab"),
    "E3-c055": (367, "L03", "L03.html:315 (80000/9 output), :422-426 (Problem E2), :148-149 (Proposition 2.4)", "M = 9/80000, CE = 80000/9 about 8888.89; recomputed; grade T derivation"),
    "E3-c160": (1070, "L03", "L03.html:272-273 (code), :321 (output), :326 (interpretation)", "CE at gamma 1 +/- 1e-6 within 0.01 cents of gamma 1; floating point, one lottery; grade C basis"),
    "E3-c168": (1125, "L03", "L03.html:184 (Remark 2.8)", "bound (k + 1)/2 with the triangle-inequality proof; no grid violation (numbers_check.py)"),
    "E3-c171": (1148, "L03", "L03.html:290-303 (code), :324 (output), :326 (interpretation), :352-353 (misconception 3)", "unrounded homogeneity to 1e-12 relative for k = 2, 3, 10 on the gamma grid; grade C basis is the lab"),
    "E3-c175": (1175, "L03", "L03.html:59 (A2)", "limit of (e^h - 1)/h is 1, taken as given; M1 Lesson 3 does not derive it"),
    "E3-c056": (374, "L04", "L04.html:64-65 (Definition 1.1)", "F_X(t) = P(X <= t); I_X(t) = integral of F_X from minus infinity to t"),
    "E3-c057": (380, "L04", "L04.html:68-71 (Lemma 1.2, T) and :73-76 (proof)", "I_X(t) = E[(t - X)^+] under A1; checked on Example 2.5 values"),
    "E3-c058": (387, "L04", "L04.html:79-80 (Definition 1.3)", "F_X <= F_Y for every real t; X at least as likely to exceed every level"),
    "E3-c059": (393, "L04", "L04.html:84-85 (Definition 1.4)", "u(s_j) <= u(s_{j+1})"),
    "E3-c060": (399, "L04", "L04.html:88-91 (Theorem 1.5, T, A1) and :93-99 (proof)", "iff equivalence with nondecreasing u on S; hypothesis A1 matches"),
    "E3-c061": (406, "L04", "L04.html:101-104 (Lemma 1.6, A1) and :106-109 (proof)", "support points suffice under A1"),
    "E3-c062": (413, "L04", "L04.html:116-119 (Proposition 1.8, T; 'holds without A2') and :121-123", "integrated order follows with A2 not needed"),
    "E3-c063": (420, "L04", "L04.html:128-131 (Definition 2.1, A1, A2)", "second-order dominance defined by I_X <= I_Y for every real t"),
    "E3-c064": (426, "L04", "L04.html:133-136 (Lemma 2.2, T, A1, A2) and :138-141 (proof)", "support points suffice; hypotheses match"),
    "E3-c065": (433, "L04", "L04.html:143-146 (Theorem 2.3, T, A1, A2) and :148-156 (proof)", "nondecreasing concave u on S; hypotheses match"),
    "E3-c066": (440, "L04", "L04.html:158-161 (Remark 2.4) and :151-155 (only-if proof)", "only-if uses c_j >= 0 (concavity) and A2 (vanishing affine term), not monotonicity"),
    "E3-c067": (447, "L04", "L04.html:165-167 (Example 2.5); output :445-446 (integrated CDF lines)", "I_X(3000,4000,5000) = 500, 1000, 2000; I_Y(2000..5000) = 250, 500, 1250, 2000; means 3000; recomputed"),
    "E3-c068": (454, "L04", "L04.html:168 (Example 2.5, first-order comparison); output :445-446", "F_X(2000) = 1/2 > 1/4 = F_Y(2000); F_Y(3000) = 3/4 > 1/2 = F_X(3000); second-order X dominates Y"),
    "E3-c070": (461, "L04", "L04.html:112-113 (Example 1.7); output :447-448 (pair B)", "F_X = (1/2, 1/2, 1), F_Y = (0, 1/2, 1) on 2000, 3000, 4000; Y dominates X; recomputed"),
    "E3-c071": (468, "L04", "L04.html:613-616 (Problem R3 solution), :58-59 (A2 box), :493 (section 3)", "unequal means, nondecreasing concave u, A2 not assumed: E X >= E Y at s_m, b1 = sigma_(m-1) >= 0; matches R3"),
    "E3-c072": (475, "L04", "L04.html:171-173 (Example 2.6) and :503-504 (misconception 1)", "equal means of 3000 and no first-order ranking; matches"),
    "E3-c073": (482, "L04", "L04.html:507-508 (misconception 2); output :472-475 (pairs 16 and 19 no SOSD ranking)", "2 of 8 equal-mean pairs have no second-order ranking; grade C SIMULATED basis matches"),
    "E3-c074": (490, "L04", "L04.html:511-512 (misconception 3); Examples 1.7 and 2.5", "Example 2.5 is second-order ranked and not first-order ranked; different pairs"),
    "E3-c075": (497, "L04", "L04.html:480 (FOSD verdict counts), :481 (agreement 24 of 24), :494 (section 3)", "3, 10, 1, 10 sum to 24; agreement 24 of 24; grade C SIMULATED basis matches"),
    "E3-c076": (505, "L04", "L04.html:483-484 (SOSD counts and agreement)", "3, 2, 1, 2 sum to 8; agreement 8 of 8; grade C SIMULATED basis matches"),
    "E3-c077": (513, "L04", "L04.html:495 (section 3, fourth bullet), :485 (interpretation)", "finite test set (witnesses and three CRRA utilities); the theorems quantify over every utility, which the lab does not check"),
    "E3-c167": (1119, "L04", "L04.html:84-85 (Definition 1.4, concave on S)", "chord slopes sigma_j nonincreasing in j"),
}

rows = []
for cid, (line, lesson, locs, note) in CARDS.items():
    status = "PASS"
    fix = ""
    if cid == "E3-c021":
        status = "FAIL"
        fix = ("Change the back to 'The phrase risk premium is used only in this sense (Definition 1.2) on this page'; "
               "L02.html:99 says the phrase has other uses in finance, so the unqualified 'used only' overstates the page.")
    evidence = f"cards.json:{line} ({cid}, {lesson}) read in full. Lesson: {locs}. Check: {note}."
    row = {
        "id": f"E3f-{cid}",
        "check": "2.7-cards",
        "location": f"cards.json:{line} ({cid}, {lesson})",
        "status": status,
        "evidence": evidence,
    }
    if status != "PASS":
        row["fix"] = fix
    rows.append(row)

def cmd_row(rid, check, location, evidence, status="PASS", fix=None):
    row = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        row["fix"] = fix or "see evidence"
    return row

rows += [
    cmd_row("E3f-cmd-check_pages", "2.9-structure", "tools/check_pages.py --unit E3",
            "Ran at a007712f: 'check_pages E3: PASS' (ledgers/E3/scripts/E3-f-r3/out_check_pages_E3.txt). Covers cards.json ids, lesson existence, per-lesson counts."),
    cmd_row("E3f-cmd-check_dag", "2.9-DAG", "tools/check_dag.py --unit E3",
            "Ran: 'check_dag E3: PASS' (out_check_dag_E3.txt). Linked uses only; unlinked forward reference found by reading is reported in notes, not here."),
    cmd_row("E3f-cmd-run_labs", "2.5-labs", "tools/run_labs.py --unit E3 --page L01 (and L02, L03, L04)",
            "Each run: 'run_labs E3: PASS (1/1)' (out_run_labs_E3_L01..L04.txt). Twin byte-identical to page code and stdout matches expected block under the tool's rule."),
    cmd_row("E3f-cmd-twins", "2.5-labs", "tests/labs/E3/lab-E3-L01-1.py .. lab-E3-L04-1.py under python -I -W error",
            "Each twin exit 0 with 0 stderr bytes (out_twin_L0n.txt, err_twin_L0n.txt in the scripts directory)."),
    cmd_row("E3f-cmd-page_smoke", "2.9-render", "tools/page_smoke.py --unit E3 --pages L01 L02 L03 L04",
            "'page_smoke E3: PASS' with each of L01 to L04 PASS (out_page_smoke_E3_L01-L04.txt): zero console errors, math rendered, no external requests, 360 px."),
    cmd_row("E3f-cmd-verify_refs", "2.1-citations", "tools/verify_refs.py --offline",
            "'offline integrity: 560 entries, 0 problems' (out_verify_refs_offline.txt). The slice cites no registry key (cards carry no 'cite'), so no unit-level live run applies."),
    cmd_row("E3f-cards-duplicates", "2.7-duplicates", "cards.json full scan (170 cards); ledgers/E3/scripts/E3-f-r3/card_checks.py",
            "0 duplicate ids, 0 duplicate normalised fronts. 13 token-Jaccard pairs >= 0.6 read in full; none duplicates a slice card: E3-c059/c167 (nondecreasing vs concave), c018/c174/c175 (A2 of L02, A5 of L02, A2 of L03), c160/c171 (two check lines), c035/c127 (different lessons), c060/c065 (Theorems 1.5 and 2.3), c032/c035 (different parts of Lab 1). Overlapping content, distinct questions: c041/c051, c039/c049, c033/c161, c054/c055."),
    cmd_row("E3f-cards-refs", "2.7-references", "ledgers/E3/scripts/E3-f-r3/card_checks.py",
            "Every Proposition, Remark, Lemma, Theorem, Definition, Example, Problem, Assumption and bare A/F label in the slice cards occurs in its lesson (block title or problem title). 0 unresolved (rerun output 'unresolved references: 0')."),
    cmd_row("E3f-cards-numbers", "2.2-numbers", "ledgers/E3/scripts/E3-f-r3/card_numbers_in_lesson.py",
            "87 numeric tokens on slice cards; 0 absent from the card's own lesson text."),
    cmd_row("E3f-numbers-recomputed", "2.2-numbers", "ledgers/E3/scripts/E3-f-r3/numbers_check.py (output out_numbers_check.txt)",
            "53 OK, 0 MISMATCH: L01 EV and EU (15000, 12500, 15000; 45000, 21250, 37500), 22500, 7500, 4030, 3481, 549, 40000, 5/12, 50; L02 E W 100, Var 1800, r_A 0.005, CE 94.934165, premium 5.065835, cents 9493 and 507, Pratt 4.5, error 0.565835, share of premium 11.1696 percent (basis: exact premium), 12.5741 percent of approximation, gaps 0.565835 to 0.000046, 6.31 ratio; L03 CE at gamma 0, 0.25, 0.5, 1, 2, 4, 11250, 9/80000, 80000/9, 1600, 2000, 3000, 9000, 5.5 bound; L04 I_X, I_Y, F_X, F_Y, Example 1.7 and 2.6 values."),
    cmd_row("E3f-notation", "2.4-notation", "notation/notation.json macros and symbols vs L01 to L04 HTML",
            "Macros used on L01 to L04: \\E, \\Prob, \\Var, \\R, \\indic are registered. No registered symbol (T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, Q) appears in L01 to L04. Local letters (gamma, sigma, S, M, R for rounding, pi for premium in L02 line 164) are defined in the lesson before use."),
    cmd_row("E3f-banned-and-process", "2.9-prose", "grep of cards.json and L01 to L04 HTML",
            "No banned phrase of BUILDER_RULES 1.3-1.4, no ellipsis in cards, no process word (builder, verifier, round, ledger, REQUESTS). 'this unit' at L03.html:184 means the currency unit and is not a process word."),
]

out = {
    "unit": "E3",
    "slice": "f",
    "round": 3,
    "verifier": "Claude Haiku 5.5, independent verifier for E3 slice f, round 3 (did not build E3; cards of L01 to L04 against their lessons)",
    "pin": PIN + " (a007712f, detached)",
    "base": "c737272f (round-2 pin, frags/D-E3-f.round2.json). Delta touching the slice, c737272f..a007712f: cards.json (E3-c015, c024, c029, c030, c039, c051, c052, c074 edited; E3-c042 and E3-c069 deleted; E3-c173, c174, c175 added); L02.html, L03.html, L04.html edited; L01.html unchanged. Every slice card was re-verified from scratch; no round-2 row is carried.",
    "checkout": ROOT.rstrip("/"),
    "scratch": "/Users/billyribeiro/.fanout/scratch/E3-f-r3",
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "verdict": "FAIL" if any(r["status"] != "PASS" for r in rows) else "PASS",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "Round 3, cards of L01 to L04 (85 cards: L01 18, L02 22, L03 23, L04 22). Every card read in full, with its lesson "
        "locators read in full (L01.html to L04.html, all lines). Hunt classes checked: numbers vs unrounded values "
        "(numbers_check.py), lab statements vs printed output (run_labs and the expected blocks), attributions (none on cards; "
        "no registry key cited), scope words (one defect, E3-c021), hypotheses of every T card, grades and bases (every C card "
        "names the lab and part; grade T cards are derivations), duplicates (none), process words and banned phrases (none). "
        "Scripts: ledgers/E3/scripts/E3-f-r3/ (card_checks.py, numbers_check.py, card_numbers_in_lesson.py, build_fragment.py, out_*.txt). "
        "Out-of-slice observation for the L02 owner (not a row of this slice): L02.html:159 and L02.html:429 use the CRRA family by name "
        "('the CRRA utility u_{1/2} that L03 Definition 1.3 defines'; 'the CRRA family that L03 Definition 1.3 defines'). The concept "
        "crra-utility is introduced in L03, so L02 uses it before its lesson (VERIFIER section 2.9 and BUILDER_RULES DAG rule). "
        "Not checked by this slice: hub, project, lessons L05 to L08 and their cards; the lesson prose outside the cards was read "
        "for the locators the cards cite and for the labs, not graded against BLUEPRINT section 3 as a whole; pytest, ruff and mypy "
        "were not run because no Python tool, test or registry file changed in the slice delta (c737272f..a007712f touches E3 course files only); "
        "the live verify_refs run was not run (offline integrity only, and no card cites a key)."
    ),
    "summary": (
        f"E3 slice f round 3: verdict {'FAIL' if any(r['status'] != 'PASS' for r in rows) else 'PASS'}. "
        f"{len(rows)} rows: {sum(1 for r in rows if r['status']=='PASS')} PASS, {sum(1 for r in rows if r['status']!='PASS')} non-PASS. "
        "The one non-PASS row is E3f-E3-c021 (cards.json:137): the back states the phrase risk premium is used only in the certainty-equivalent sense, "
        "but L02.html:99 says the phrase has other uses in finance and limits the claim to this page."
    ),
}
path = ROOT + "ledgers/E3/E3-f.json"
with open(path, "w", encoding="utf-8") as fh:
    json.dump(out, fh, indent=1, ensure_ascii=False)
    fh.write("\n")
print("wrote", path, "rows", len(rows))
