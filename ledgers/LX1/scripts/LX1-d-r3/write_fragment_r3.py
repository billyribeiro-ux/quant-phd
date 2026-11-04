"""Write the LX1-d round-3 ledger fragment (cards.json against the four lessons).

Run: .venv/bin/python -I ledgers/LX1/scripts/LX1-d-r3/write_fragment_r3.py <repo root>
Line numbers in evidence refer to ledgers/LX1/scripts/LX1-d-r3/out/L0n_text.txt, produced by html_text.py.
"""

import json
import sys
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(sys.argv[1])
LOC = "course/modules/LX/LX1/cards.json"
C = {}  # card id -> (lesson file, evidence)


def card(n: int, lesson: str, ev: str) -> None:
    C[f"LX1-c{n:03d}"] = (lesson, ev)


card(1, "L01", "L01_text.txt 22-24 (Definition 1.2): F_t = sum_k d_(t+k)/(1+r)^k whenever the series converges; benchmark, not a forecast (line 24). Ungraded definition; matches.")
card(2, "L01", "L01_text.txt 26-28 (Theorem 1.3 statement: F_t = d_1(1+g)^t/(r-g) = d_(t+1)/(r-g); F_0 = d_1/(r-g); series converges) with hypotheses A0, A1 at 17-19. Matches. recompute_r3.out: F0 = 20000/3, F2 = 7072.67 -> 7073.")
card(3, "L01", "L01_text.txt 28 (S_N(t) = F_t(1-q^N) exactly for every N>=1, q=(1+g)/(1+r)); basis Part A line 36 and printed Part A line 58 (identity True for N=10,60,200). Matches.")
card(4, "L01", "L01_text.txt 35 (0<q<1 under A0; q^N -> 0; S_N(t) -> F_t). recompute_r3.out: q = 103/109 = 0.944954. Matches.")
card(5, "L01", "L01_text.txt 38 (Proposition 1.4: (A1) d_1>0, 1+g>0; (A2) r>-1, g>=r; S_N(0) -> +inf; Theorem 1.3 does not apply) and proof 40. Hypotheses and conclusion match.")
card(6, "L01", "L01_text.txt 44 (Definition 2.1: B_t = P_t - F_t counted as bubble only when B_t > 0, in cents; B_t <= 0 no bubble). Ungraded definition; matches.")
card(7, "L01", "L01_text.txt 46-48 (A3 d_1>0; A4 g<g', r>g, r>g', 1+g>0, 1+g'>0; conclusion F_0(g)<F_0(g'); positive gap under g and non-positive under g' for F_0(g)<P_0<=F_0(g')) and proof 50. Matches.")
card(8, "L01", "L01_text.txt 62 (Definition 3.1: sudden collective demand to convert claims into money or safe assets; prices fall together or trading stops; names mechanism only, no frequency/trigger/size). Ungraded definition; matches.")
card(9, "L01", "L01_text.txt 56, 58 (Lab 1 Part B prints 'periods with price above fundamental: 9 of 13'), 118 (Empirical 1: 9 of 13 SIMULATED draw). recompute_r3.out: gaps from printed prices give 9 positive of 13. Matches; grade C correct.")
card(10, "L01", "L01_text.txt 58 (Part C: 'periods with price above the alternative fundamental: 13 of 13', 'the count changes ... True') and 59 (9 of 13 vs 13 of 13). recompute_r3.out: 13 positive gaps under 1%. Matches.")
card(11, "L01", "L01_text.txt 51 (witness: d_1=400, r=9%, g=1%/3%, F_0=5000 and 20000/3, P_0=6000 gives +1000 and -2000/3) and 79. recompute_r3.out reproduces both. Matches.")
card(12, "L01", "L01_text.txt 72 (d_1=400, d_2=0, d_s=0 for s>=3: 400/1.09 = 40000/109 -> 367 cents; closed form 6667 cents at g=3%) and 82. recompute_r3.out: 366.97->367; 6666.67->6667. Matches.")
card(13, "L01", "L01_text.txt 40 and 85 (each discounted dividend >= d_1/(1+r); partial sums grow without bound; closed form not finite; Theorem 1.3 does not apply) and misconception 3 at 84-86 (Section 6). Matches; hypotheses (A1) d_1>0, 1+g>0 and (A2) r>-1, g>=r restated at 38.")
card(14, "L02", "L02_text.txt 17 (Definition 1.1: parity kappa>0 grams per unit; convertible on demand at the parity). Ungraded definition; matches.")
card(15, "L02", "L02_text.txt 20-21 ((A1) parity kept at every date; one gram costs 1/kappa units at every date) and 23. Matches.")
card(16, "L02", "L02_text.txt 25 (Remark 1.3: one price; (A1) does not involve P_t, so conclusion holds whatever path P_t follows) and misconception 2 at 64-65. Matches.")
card(17, "L02", "L02_text.txt 27-28 (V_t = D P_0 / P_t, D nominal in cents, P_0 base). Ungraded definition; matches.")
card(18, "L02", "L02_text.txt 31 ((A2): D positive integer cents, same every date, paid in full, not renegotiated), 32 ((A3)), 35 (proof: V_t/V_(t-1) = P_(t-1)/P_t, D P_0 cancels). Matches; (A2) restated in full.")
card(19, "L02", "L02_text.txt 31-33, 36. FAIL: front restates (A2) as 'paid in full' and omits 'the contract is not renegotiated' (L02_text.txt 31) that the lesson's (A2) contains and that card c018 includes. Conclusion P_0/P_H is correct (telescoping, line 36).")
card(20, "L02", "L02_text.txt 41 (Definition 3.1: rise in V_t that a fall in P_t implies by the identity of Proposition 2.1, D fixed; arithmetic consequence). Ungraded definition; matches.")
card(21, "L02", "L02_text.txt 44 (Corollary 3.2: V_t > V_(t-1) iff P_t < P_(t-1)) and proof 46. Matches; hypotheses by label (A2),(A3) of Prop 2.1 at 43.")
card(22, "L02", "L02_text.txt 48 (Remark 3.3: factor P_(t-1)/P_t, larger than one in a fall; corollary gives direction, not size). Matches.")
card(23, "L02", "L02_text.txt 63 (misconception 1: falling prices; Corollary 3.2 gives the opposite direction; Lab Part C six falling and six rising periods equal). Matches.")
card(24, "L02", "L02_text.txt 67 (misconception 3: V_t = D P_0/P_t changes whenever P_t changes; Lab Part B prints a real value differing from its predecessor in each of the 12 periods). L02 twin output at 53: consecutive V_t all differ (recompute_r3.out). Matches; grade C.")
card(25, "L02", "L02_text.txt 53 (Lab Part B prints 'identity V_t / V_(t-1) = P_(t-1) / P_t holds exactly for t = 1 to 12: True'). Matches; grade C.")
card(26, "L03", "L03_text.txt 18-20 (Assumption 1.1: P_t = (1-delta)^min(t,m), P_0=1, 0<=m<=H, 0<delta<1; index falls by delta per period on parity, flat after m). Matches.")
card(27, "L03", "L03_text.txt 31 (Definition 2.1: L_t = V_t / N_t). Ungraded definition; matches.")
card(28, "L03", "L03_text.txt 26 (slope phi>0, beta>0 fixed) and 31 (psi_t = rise in extra cost above baseline; psi_t = phi(L_t - L_0) at 26). Matches.")
card(29, "L03", "L03_text.txt 33 (Definition 2.2 chain: fall in P_t raises V_t (A1,A2); rise lowers net worth one for one (A2); higher leverage raises premium (A3); premium lowers output by f_t (A3); describes the model only). Matches.")
card(30, "L03", "L03_text.txt 37 (Lemma 3.1: ell(x)=x/(C-x), C=N_0+D; L_t = ell(V_t) when V_t<C; L_0 = D/N_0; ell strictly increasing on [D,C)) and proof 39-41. Matches.")
card(31, "L03", "L03_text.txt 43-44 (Prop 3.2(a): V_t <= V_m; V_t = D(1-delta)^(-t) for t<=m strictly increasing when m>=1; V_t = V_m for t>=m; hypotheses include V_m < N_0+D at 23) and proof 48. Matches.")
card(32, "L03", "L03_text.txt 45 (Prop 3.2(b): depth(m) = beta phi(ell(V_m)-ell(D)) = beta phi(V_m/(N_0+D-V_m) - D/N_0)). recompute_r3.out reproduces depth(12)=0.092046, depth(4)=0.026867 from the formula. Matches.")
card(33, "L03", "L03_text.txt 46 and 50 (Prop 3.2(c): max first attained at t=m; no earlier period when m>=1). Matches.")
card(34, "L03", "L03_text.txt 46 (depth(0)=0 stated), 50 (m=0 proof: V_t=D, f_t=0) and P2 at 109-111. Matches.")
card(35, "L03", "L03_text.txt 53 (Corollary 3.3: depth(m') < depth(m) for 0<=m'<m<=H; X has m=12, Y has m'=4) and proof 55. Matches; hypotheses 'Assumptions 1.1 to 1.3' include 1.2 (V_m<N_0+D).")
card(36, "L03", "L03_text.txt 57-59 (Corollary 3.4: 1<=m'<m<=H; ratio = (ell(V_m)-ell(D))/(ell(V_m')-ell(D)); independent of beta, phi) and proof 61. Matches.")
card(37, "L03", "L03_text.txt 66 (Lab Part B printed: 'economy X depth 9.20 percent ... first reached at t = 12'); 64 (hypothesis 9.20, t=12). recompute_r3.out: exact 9.204597%, rounds to 9.20. Matches; grade C.")
card(38, "L03", "L03_text.txt 66 (Lab Part B: 'economy Y depth 2.69 percent ... first reached at t = 4'); 120 (exact 2.6867). recompute_r3.out: 2.686713% -> 2.69. Matches; grade C.")
card(39, "L03", "L03_text.txt 66 (Part D ratio 3.4260 for phi=beta=1); recompute_r3.out: exact X/Y = 3.425970 -> 3.4260. Matches; grade C.")
card(40, "L03", "L03_text.txt 70 (Definition 4.1: lender lends against collateral to institutions solvent but illiquid; solvent and illiquid defined). Ungraded definition; matches.")
card(41, "L03", "L03_text.txt 70 (Definition 4.1: central bank is the public institution that issues the monetary base). Ungraded definition; matches.")
card(42, "L03", "L03_text.txt 72 (Remark 4.2: Assumption 1.2 has no lending term; Assumption 1.3 has no term for a facility changing a solvent borrower's premium; Proposition 3.2 says nothing about a facility). Matches.")
card(43, "L03", "L03_text.txt 80-81 (misconception 1: model has no bank, no failure, no default; proof uses none of these events) and 22 (no default, no balance-sheet change). Matches; 'misconception 1, Section 6' reference correct.")
card(44, "L03", "L03_text.txt 82-83 (misconception 2: ordering follows from durations 12 and 4 set by Assumption 1.1; model cannot say whether holding parity causes deeper fall). Matches.")
card(45, "L03", "L03_text.txt 72 (Remark 4.2: model has no lending facility) and 84-85 (misconception 3; Definition 4.1 requires collateral and insolvency limit; no panic result follows). Matches.")
card(46, "L03", "L03_text.txt 86-87 (misconception 4: 9.20 percent is a SIMULATED model value, beta=1, no output series enters the lab; changing beta scales it via beta phi, Prop 3.2(b)) and 67. Matches.")
card(47, "L03", "L03_text.txt 28 (honest-pending note: no redistributable historical series for gold-standard adherence or output depth is embedded; lab is SIMULATED). Ungraded; matches.")
card(48, "L04", "L04_text.txt 18 (Definition 1.1: ell_t = ln(x_t/x_(t-1)); per month, not annualized). Ungraded definition; matches.")
card(49, "L04", "L04_text.txt 18 (dispersion: sample standard deviation with denominator n-1 about the mean; defined only when n>=2). Ungraded definition; matches.")
card(50, "L04", "L04_text.txt 21 and 23 (Proposition 1.2 (A1): sum of ell_t for t=a+1..b equals ln(x_b/x_a); b-a terms). Matches.")
card(51, "L04", "L04_text.txt 25 (Remark 1.3: exact in reals; Lab checks to 1e-12 and confirms only that tolerance) and 43 (code: SUM_TOLERANCE = 1e-12 and identity check against that tolerance). Matches; T grade.")
card(52, "L04", "L04_text.txt 33-34 (Proposition 2.2: (A2) x_t = kappa every month, kappa>0, n>=2; every monthly log change 0; dispersion 0) and proof 36-37. Matches.")
card(53, "L04", "L04_text.txt 29 (Definition 2.1: anchor currency, one foreign currency, parity kappa>0 anchor units per foreign unit, market rate x_t>0; fixed-parity model = model plus (A2)). Ungraded definition; matches.")
card(54, "L04", "L04_text.txt 44 (Lab Part B: 'months with an exactly zero change: 3: 1976-07, 2012-07, 2019-11') and 45. recompute_r3.out: exact zero changes at 1976-07, 2012-07, 2019-11. Matches. Basis lacks 'MANIFEST retrieved 2026-10-19' (see row card-basis-l04-manifest).")
card(55, "L04", "L04_text.txt 44-45 (window one 0.027935 from 668 changes, sample sd with denominator 667). recompute_r3.out: sd1 = 0.027935278 from 668 changes. Matches; grade C. Basis: see card-basis-l04-manifest.")
card(56, "L04", "L04_text.txt 44-45 (window two 0.024700 from 321 changes). recompute_r3.out: sd2 = 0.02469950 -> 0.024700 from 321. Matches; grade C. Basis: see card-basis-l04-manifest.")
card(57, "L04", "L04_text.txt 44 (ratio 0.8842). recompute_r3.out: 0.88416881 -> 0.8842. Matches; grade C. Basis: see card-basis-l04-manifest.")
card(58, "L04", "L04_text.txt 44-45 (largest absolute change window two 0.096575 at 2008-10, signed -0.096575). recompute_r3.out: 2008-10, -0.0965747. Matches; grade C. Basis: see card-basis-l04-manifest.")
card(59, "L04", "FAIL. Back says 'its monthly changes are generally nonzero' (cards.json line 498). The basis is one column (Lab 1 Part B: 665 of 668 nonzero), so the general claim is unsupported and carries no registry key (BUILDER_RULES 7: cite keys for an empirical claim). The same sentence is L04_text.txt line 14. Figures 3 zero months and 668 changes match (recompute_r3.out).")
card(60, "L04", "L04_text.txt 58-59 (misconception 2 and Part D: two sample sds and their difference; no test; no cause named; window start is a convention) and 104 (Problem E3: no standard error, no test). Matches; grade C.")
card(61, "L04", "L04_text.txt 61 (misconception 4: ln 1.1 = 0.095310; difference 0.004690) and 70 (Problem M1: ratio 1.1). recompute_r3.out: ln 1.1 = 0.0953101798; 0.1 - ln 1.1 = 0.0046898 -> 0.004690. Matches.")
card(62, "L04", "L04_text.txt 27, 30 and 63 (Definition 2.1 is a model class; Bretton Woods definition pending; no historical fact stated; Section 4 lists what is open). Matches.")
card(63, "L04", "L04_text.txt 46 and 52 (window two starts 2000-01; first available for other snapshots) and fx_daily/ust_daily MANIFEST entries: first = 2000-01-03 for both (course/assets/data/market/MANIFEST.json). Matches; ungraded.")
card(64, "L04", "L04_text.txt 42-43 (data: fx_monthly.csv, G.5/H.10 noon buying rates in New York, GBP column in US dollars per pound). MANIFEST fx_monthly citation and GBP=RXI$US_N.B.UK (direct quote, not inverted). Matches.")
card(65, "L04", "L04_text.txt 44 (Part D: difference -0.003236) and 45 (sds from unrounded values). recompute_r3.out: diff -0.0032358 -> -0.003236. Matches; grade C.")
card(66, "L02", "L02_text.txt 53 (Part C: 6 of 12 falling; 6 of 12 rising; equal True) and 63 (misconception 1). Matches; grade C.")
card(67, "L03", "L03_text.txt 66 (Part D: ratio 3.4260 for phi=1/2, 1 and 3 with beta=1; products 1/2, 1, 3) and 67 (Corollary 3.4). recompute_r3.out: ratio unchanged across products (depth scales linearly). Matches; grade C.")
card(68, "L04", "L04_text.txt 44-45 (Part B: 3 exact zeros; window one 668 changes) and 96 (E1: 668 - 3 = 665). recompute_r3.out: 665 nonzero. Matches; 665 is derived from printed counts; grade C.")
card(69, "L04", "L04_text.txt 42-43 (fx_monthly: 669 months, 1971-01 to 2026-09, retrieved 2026-10-19; month-end, each column's last value in the month). MANIFEST fx_monthly: rows 669, first 1971-01, last 2026-09, retrieved 2026-10-19, transform 'month-end (each column's last value in the month)'. Matches; ungraded.")
card(70, "L04", "L04_text.txt 43 and 50 (file holds exchange-rate columns only; no interest-rate or forward-rate column). MANIFEST columns AUD..SEK are all exchange rates. Matches; ungraded.")
card(71, "L03", "L03_text.txt 22 (Assumption 1.2: N_t = N_0 - (V_t - V_0); whole rise in real debt falls on net worth). Ungraded definition; matches.")
card(72, "L03", "L03_text.txt 26-27 (depth(m) = max over 0<=t<=H of f_t; f_t = beta psi_t, fall as fraction of baseline output). Ungraded definition; matches.")

NON_PASS = {
    "LX1-c019": (
        "FAIL",
        "cards.json line 159 (front) restates (A2) as 'paid in full' only. The lesson's (A2) (L02_text.txt line 31) also says the contract is not renegotiated, and card LX1-c018 (line 150) includes 'not renegotiated'. Hypotheses of Proposition 2.1 are not carried in full.",
        "cards.json line 159: change '(A2) D is a fixed positive integer number of cents, paid in full;' to '(A2) D is a fixed positive integer number of cents, paid in full and not renegotiated;' so it matches LX1-c018 and L02.html (A2).",
    ),
    "LX1-c059": (
        "FAIL",
        "cards.json line 498 (back): 'its monthly changes are generally nonzero'. The stated basis is one column (Lab 1 Part B: 665 of 668 changes nonzero, L04_text.txt lines 44-45). A general claim about recorded rates is an empirical claim with no registry key (BUILDER_RULES 7: cite keys where the card makes an empirical claim). The same sentence is at L04_text.txt line 14, so the card repeats an unsupported scope.",
        "cards.json line 498: replace 'its monthly changes are generally nonzero; Lab 1, Part B, counts the exactly zero changes in the recorded GBP column.' with 'in the recorded GBP column, 665 of the 668 monthly changes in window one are nonzero (Lab 1, Part B prints 3 exact zeros among 668 changes).' Builder must also narrow L04.html line 14 ('its monthly changes are generally nonzero') or cite a registry key for it; this verifier does not edit it.",
    ),
}

rows = []
for cid in sorted(C):
    lesson, ev = C[cid]
    if cid in NON_PASS:
        status, evidence, fix = NON_PASS[cid]
        row = {"id": f"card-{cid.split('-')[-1]}", "check": "2.7-card-vs-lesson",
               "location": f"{LOC} ({cid}); {lesson}.html", "status": status, "evidence": evidence, "fix": fix}
    else:
        row = {"id": f"card-{cid.split('-')[-1]}", "check": "2.7-card-vs-lesson",
               "location": f"{LOC} ({cid}); {lesson}.html", "status": "PASS", "evidence": ev}
    rows.append(row)

rows += [
    {"id": "card-basis-l04-manifest", "check": "2.7-card-vs-plan-s9", "location": f"{LOC} (LX1-c054, c055, c056, c057, c058, c059, c060, c065, c068); plans/LX1-build-plan.md section 9 (lines 516-517)",
     "status": "FAIL",
     "evidence": "plans/LX1-build-plan.md line 516-517 (section 9, binding): 'Cards for the L04 result name Lab 4 (fx_monthly, MANIFEST retrieved 2026-10-19)'. The nine L04 graded (C) result cards name the column only, e.g. 'Lab 1 Part C (embedded fx_monthly GBP column)' (cards.json lines 456-579 bases). None names the MANIFEST retrieved date. The lesson itself labels the lab 'Lab 1' (L04_text.txt 42), so the card should keep 'Lab 1', not the plan's 'Lab 4'.",
     "fix": "In the basis of cards LX1-c054, c055, c056, c057, c058, c059, c060, c065 and c068, add 'fx_monthly, MANIFEST retrieved 2026-10-19' (e.g. 'Lab 1 Part C (fx_monthly, MANIFEST retrieved 2026-10-19; GBP column)'). Keep the lesson's label 'Lab 1'."},
    {"id": "card-struct-ids-lessons", "check": "2.7-structure", "location": LOC,
     "status": "PASS",
     "evidence": "card_checks_r3.out: 72 cards; ids LX1-c001..c072 unique and in file order; per lesson L01 13, L02 13, L03 25, L04 21; all lesson values in {L01..L04}; cite arrays all empty (no registry key claimed); no empty front/back; keys identical on every card."},
    {"id": "card-check-pages", "check": "2.7-structure", "location": LOC,
     "status": "PASS",
     "evidence": "Re-run: .venv/bin/python tools/check_pages.py --unit LX1 -> 'check_pages LX1: PASS', exit 0 (out/check_pages_LX1.out). This includes check_cards: id prefix, lesson existence, grade values, registry keys."},
    {"id": "card-numeric-tokens", "check": "2.7-card-vs-lesson", "location": LOC,
     "status": "PASS",
     "evidence": "card_checks_r3.out: every decimal or integer token in every card front and back occurs in its own lesson's extracted text (html_text.py, out/L0n_text.txt). 'numeric tokens absent from their lesson text: none'."},
    {"id": "card-lab-outputs-verbatim", "check": "2.5-labs-vs-cards", "location": "tests/labs/LX1/lab-LX1-L01-1.py .. lab-LX1-L04-1.py; L01..L04.html",
     "status": "PASS",
     "evidence": "Each twin run alone: cd scratch && .venv/bin/python -I -W error tests/labs/LX1/lab-LX1-L0n-1.py exit 0 (out/twin_L0n.out, empty .err). card_checks_r3.out: every twin output line occurs verbatim (whitespace-normalised) in its lesson page text. L04 twin run with data/fx_monthly.csv copied from course/assets/data/market/."},
    {"id": "card-recomputed-numbers", "check": "2.2-numbers", "location": LOC,
     "status": "PASS",
     "evidence": "Independent recomputation, scripts/LX1-d-r3/recompute_r3.py -> out/recompute_r3.out: F_0 = 20000/3 -> 6667; 40000/109 -> 367; F_2 = 7072.67 -> 7073; q = 103/109; S_N(0) identity True for N=10,60,200; gaps from printed prices 9 of 13 (3%) and 13 of 13 (1%); V_t differ every period; falls = rises = {1,5,6,8,9,12} (6 of 12); depth X 9.204597 -> 9.20 (t=12), Y 2.686713 -> 2.69 (t=4), ratio 3.425970 -> 3.4260 for every product; window one sd 0.027935 (668 changes, 3 zero months, 665 nonzero), window two sd 0.024700 (321), ratio 0.8842, diff -0.003236, largest 1985-03 and 2008-10 -0.096575, ln 1.1 = 0.095310, 0.004690."},
    {"id": "card-duplicates", "check": "2.7-duplicates", "location": LOC,
     "status": "PASS",
     "evidence": "Full scan (card_checks_r3.out): no identical fronts or backs. Word-Jaccard >= 0.5 pairs judged distinct questions: c009/c010 (3% vs 1% counts), c018/c019 (parts a and b), c035/c036 (depth order vs ratio), c037/c038 (two economies), c055/c056/c057/c065 (different windows and statistics), c039/c067 (value at beta phi=1 vs invariance across products), c005/c013 (Proposition 1.4 proposition card vs its misconception 3 card, which BUILDER_RULES 7 requires), c001/c027/c002/c003 low overlap."},
    {"id": "card-grades-basis", "check": "2.3-grades", "location": LOC,
     "status": "PASS",
     "evidence": "card_checks_r3.out: grades T 33, C 18, ungraded 21 (definitions only: c001, c006, c014, c017, c020, c026-c029, c040, c041, c047-c049, c053, c063, c064, c069-c072). Every graded card has a basis. T cards cite a proof or derivation (BUILDER_RULES 7). C cards are lab outputs on SIMULATED or embedded-data lab results and say so in the basis (lesson 'Key results' grades agree: L01 counts C, L02 Lab 1 C, L03 Lab 1 C, L04 Lab 1 C). Cards cite no keys (none needed; no empirical attributed claim)."},
    {"id": "card-misconception-and-concept-coverage", "check": "2.9-coverage", "location": LOC,
     "status": "PASS",
     "evidence": "Introduced concepts (lesson 'Introduces:' lines): speculative bubble c006; financial panic c008; gold standard c014; debt deflation c020; credit channel c029; lender of last resort c040 (and central bank c041); Bretton Woods c062. Misconceptions: L01 3 (c011-c013), L02 3 (c023, c016, c024), L03 4 (c043-c046), L04 4 (c059-c062). Derivations: c001/c002, c017/c018, c035. Key results: each L0n key-results row has a card."},
    {"id": "card-notation", "check": "2.4-notation", "location": LOC,
     "status": "PASS",
     "evidence": "notation/notation.json registers T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q}. grep over L01-L04.html and cards.json: none of these appears in LX1 (T appears only as the grade field value). Symbols used (F_t, d_1, q, S_N, V_t, P_t, D, kappa, L_t, N_t, psi, phi, beta, delta, m, H, ell, depth, C) are conventionally local per notation.json 'about' and are defined in the lesson before use (e.g. L01 lines 17-24, L02 27-28, L03 18-27)."},
    {"id": "card-dag-concepts", "check": "2.9-dag", "location": LOC,
     "status": "PASS",
     "evidence": "check_dag.py --unit LX1 -> 'check_dag LX1: PASS' (out/check_dag_LX1.out). Cards name concepts only from their own lesson or earlier lessons (L03 uses L02's debt deflation, L04 uses L02's gold-standard framing only by the lesson's own link)."},
    {"id": "card-banned-words", "check": "1.3-1.4-banned", "location": LOC,
     "status": "PASS",
     "evidence": "Scan for TODO, TBD, lorem, ellipsis, 'for brevity', 'beyond the scope', 'studies show', 'experts agree', 'obviously', 'clearly', 'it is important to note', 'it is well known': none in any front or back (card_checks_r3.out 'banned or process words in cards: none')."},
    {"id": "card-scope-words", "check": "2.2-scope-words", "location": LOC,
     "status": "PASS",
     "evidence": "Scope words (only, all, every, any, same, exactly, generally, whatever) listed in card_checks_r3.out. Each theorem-scope use matches its lesson statement (e.g. 'for every N >= 1', 'whatever path P_t follows' from L02 Remark 1.3). The one unsupported scope ('generally nonzero') is card LX1-c059, failed above."},
    {"id": "card-check-dag-projects-gates", "check": "2.6-2.9-gates", "location": "tools/check_dag.py, tools/check_projects.py, tools/page_smoke.py, tools/run_labs.py, tools/mypy, ruff, pytest",
     "status": "PASS",
     "evidence": "Re-run: run_labs LX1 PASS (7/7); check_dag LX1 PASS; check_projects LX1 PASS; page_smoke LX1 PASS (every page and lab; the output reports PASS per page and does not itemise console errors, so this row claims the PASS verdict only); ruff check and ruff format --check PASS; mypy --no-incremental: no issues in 385 source files; pytest -k 'LX1 or card or check_pages' exit 0 (out/*.out)."},
    {"id": "card-registry-offline", "check": "2.1-citations", "location": "references/references.json (560 entries)",
     "status": "PASS",
     "evidence": "verify_refs.py --offline -> 'offline integrity: 560 entries, 0 problems', exit 0 (out/verify_refs_offline_all.out). verify_refs --unit LX1 is a live run and was not executed here: no card cites a key and the card slice makes no bibliographic claim; lesson citations are the L0n builder's rows."},
    {"id": "card-data-manifest", "check": "2.8-data", "location": "course/assets/data/market/MANIFEST.json; course/assets/data/market/fx_monthly.csv",
     "status": "PASS",
     "evidence": "fetch_data.py --check -> 'fetch_data: 3 datasets, 0 problems', exit 0 (out/fetch_data_check.out). MANIFEST fx_monthly: rows 669, first 1971-01, last 2026-09, retrieved 2026-10-19, month-end transform; fx_daily and ust_daily first 2000-01-03 (card c063, c064, c069, c070 facts)."},
]

fragment = {
    "unit": "LX1",
    "slice": "LX1-d",
    "round": 3,
    "verifier": "Claude Haiku 5.5, independent verifier for LX1-d (ALL cards.json against L01-L04), round 3. Did not build LX1; round-2 fragment read as context only; its PASS rows were not trusted and every card was re-read.",
    "pin": "67a2d13e7575608e95b2e34a9c7c2a82c61b117b",
    "base": "67c47689 (round-2 pin 67c4768 in the round-2 fragment)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE3-LX1-d",
    "scratch": "/tmp/lx1d3_scratch.K1rtpg (data/fx_monthly.csv copy for the L04 twin run only)",
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Delta since round-2 pin 67c47689 read in full: cards.json (83 changed lines: c003, c025, c039, c043, c047, c054-c056, c064 rewritten; c066-c072 added), L01-L04.html and tests/labs/LX1/lab-LX1-L04-1.py (spot->exchange-rate wording, Part B prints 'exchange rates', fx_monthly description), L03 text on Assumption 1.2, L02 debt-deflation definition. Every changed card was re-derived against its current lesson text.",
        "Mutants: none. This slice is cards, not a grader; no student-error mutant applies. The mutants directory was not used.",
        "Not checked: a live verify_refs --unit LX1 (network, not required for a card-only slice); the rendered page appearance of cards (cards are data, not rendered here); the SIMULATED page figures (other slices); the lesson-side notation of L04 'generally nonzero' beyond its effect on card c059.",
        "Lesson-side items found while checking cards, outside this fragment (builder fixes, not edited here): L04.html line 14 'its monthly changes are generally nonzero' (same unsupported scope as card c059).",
    ],
    "summary": "Round 3 of LX1-d: 72 cards read in full against L01-L04 and the current lab outputs. 70 card rows PASS. Non-PASS: card-c019 (A2 restated without 'not renegotiated'), card-c059 ('generally nonzero' beyond a single column, no key), card-basis-l04-manifest (plan section 9 requires the MANIFEST retrieved date in L04 result bases). Verdict FAIL.",
}

out = ROOT / "ledgers/LX1/LX1-d.json"
out.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out, "rows:", len(rows), "non-PASS:", [r["id"] for r in rows if r["status"] != "PASS"])
