"""Writes the round-2 fragment ledgers/LX1/LX1-d.json for slice LX1-d (verifier-rules section 3 format).

Run from the checkout root: python -I ledgers/LX1/scripts/LX1-d-r2/write_fragment_r2.py
Every row's evidence cites a script under ledgers/LX1/scripts/LX1-d-r2/ or an observed command output
saved under its out/ directory. Lesson line numbers refer to out/lx1d2_L0n.txt (extract_text.py output).
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
CARDS = json.loads((ROOT / "course/modules/LX/LX1/cards.json").read_text(encoding="utf-8"))
LOC = {"L01": "L01.html", "L02": "L02.html", "L03": "L03.html", "L04": "L04.html"}
RC = "recompute_cards_r2.out"

EV = {
    "LX1-c001": "L01 extract 23-25 (Definition 1.2): F_t = sum_k d_(t+k)/(1+r)^k whenever the series converges; benchmark, not a forecast. Card matches.",
    "LX1-c002": "L01 extract 27-29 (Theorem 1.3 statement) and 31-36 (proof): F_t = d_1(1+g)^t/(r-g) = d_(t+1)/(r-g); hypotheses A0, A1 carried. " + RC + ": F_0 = 20000/3 at d_1=400, r=9%, g=3%.",
    "LX1-c003": "ROUND-1 FAIL FIXED. L01 extract 29 (identity for every N>=1) and 37 (Part A checks S_N(0) = F_0(1-q^N) for N=10, 60, 200). Twin code (lab-LX1-L01-1.py, Part A) uses f0 only, so the check is t=0. Card back now says t=0 and that the every-t identity is the Theorem 1.3 proof. Twin out/twin_L01.out Part A line 'identity ... True' for N=10,60,200 (checks L01 lab exit 0).",
    "LX1-c004": "L01 extract 36 (proof of Theorem 1.3): 0<q<1 under A0, q^N -> 0, partial sums converge. " + RC + ": q = 103/109.",
    "LX1-c005": "L01 extract 39 (Proposition 1.4): (A1) d_1>0, 1+g>0; (A2) r>-1, g>=r; S_N(0) -> +inf, Theorem 1.3 does not apply; proof 41 (q>=1, each term >= d_1/(1+r)). Card matches.",
    "LX1-c006": "L01 extract 45 (Definition 2.1): B_t = P_t - F_t, a bubble only when B_t > 0, in cents; B_t <= 0 no bubble. Card matches.",
    "LX1-c007": "L01 extract 47-49 (Proposition 2.2, (A3) d_1>0, (A4) g<g', r>g, r>g', 1+g>0, 1+g'>0; conclusion F_0(g)<F_0(g') and sign consequence) and proof 51. Card hypotheses match.",
    "LX1-c008": "L01 extract 63 (Definition 3.1): mechanism only; states no frequency, trigger or size. Card matches.",
    "LX1-c009": "L01 twin output (out/twin_L01.out) 'periods with price above fundamental: 9 of 13'; lesson extract 59 and 119 (Empirical 1). Independent recomputation in " + RC + ": gaps [-200,68,141,146,301,0,-398,2050,676,2175,2151,-92,285], 9 positive.",
    "LX1-c010": "L01 twin output Part C '13 of 13' and 'the count changes with the assumed growth rate: True'; lesson extract 59-60. Independent recomputation in " + RC + ": 13 of 13 under 1%.",
    "LX1-c011": "L01 extract 52 (Proposition 2.2 witness, d_1=400, r=9%, g=1%/3%, P_0=6000: gap +1000 and -2000/3) and misconception 80. " + RC + ": F_0(1%) = 5000, F_0(3%) = 6666.67.",
    "LX1-c012": "L01 extract 73 (Section 5, d_2=d_3=0 stream: 400/1.09 = 40000/109 -> 367 cents; closed form 6667 cents at g=3%) and misconception 83. " + RC + ": 366.97 -> 367; 6666.67 -> 6667.",
    "LX1-c013": "ROUND-1 FAIL FIXED. Card front now carries (A1) d_1>0, 1+g>0 and (A2) r>-1, g>=r. L01 extract 39 (Proposition 1.4 hypotheses), 41 (proof lower bound d_1/(1+r)), 86-87 (misconception 3). Card back matches; basis names the proof and misconception 3.",
    "LX1-c014": "L02 extract 18 (Definition 1.1): kappa>0 grams per unit; convertible on demand at the parity. Card matches.",
    "LX1-c015": "L02 extract 21-22 (Proposition 1.2 (A1) and conclusion 1/kappa at every date) and proof 24. Card matches.",
    "LX1-c016": "L02 extract 26 (Remark 1.3): (A1) does not involve P_t, so the conclusion holds whatever path P_t follows. Card matches.",
    "LX1-c017": "L02 extract 28-29 (Section 2): V_t = D P_0 / P_t, D in cents, P_0 base value. Card matches.",
    "LX1-c018": "L02 extract 32-34 (Proposition 2.1 (A2), (A3); part (a)) and proof 36: V_t/V_(t-1) = P_(t-1)/P_t, D P_0 cancels. Card hypotheses match.",
    "LX1-c019": "L02 extract 34 and 37: conclusion (b) V_H/V_0 = P_0/P_H. The card uses H, as the conclusion does; the proof body on extract line 37 still writes T as an index, which is the separate notation row notation-L02-T.",
    "LX1-c020": "L02 extract 42 (Definition 3.1): rise in V_t produced by a fall in P_t with D fixed. Card matches.",
    "LX1-c021": "L02 extract 44-45 (Corollary 3.2 (A2),(A3) of Proposition 2.1; V_t > V_(t-1) iff P_t < P_(t-1)) and proof 47. Card hypotheses match.",
    "LX1-c022": "ROUND-1 FAIL FIXED. Card front now states (A2) and (A3) of Proposition 2.1. L02 extract 34 and 49 (Remark 3.3): factor P_(t-1)/P_t is larger than one for a fall; P_t > 0 is (A3), so the division is defined. Card back matches.",
    "LX1-c023": "ROUND-1 FAIL FIXED. Card front now states (A2) and (A3) of Proposition 2.1. L02 extract 44 (Corollary 3.2 hypotheses), 64 (misconception 1): opposite direction for V_t, same nominal payment buys more goods. Card no longer depends on the lab count; grade T with basis Corollary 3.2 and misconception 1.",
    "LX1-c024": "L02 extract 29 (V_t definition) and Lab Part B output (out/twin_L02.out): 13 values, all 12 consecutive pairs differ (" + RC + " 'all consecutive real values differ: True'). Card matches.",
    "LX1-c025": "L02 twin output (out/twin_L02.out): 'identity ... for t = 1 to 12: True', '6 of 12', '6 of 12', 'coincide: True'; recomputed falls [1,5,6,8,9,12] = rises (" + RC + "). Compound front, accepted as one printed lab result (see notes).",
    "LX1-c026": "L03 extract 18-21 (Assumption 1.1): P_t = (1-delta)^min(t,m), P_0 = 1, 0<=m<=H, 0<delta<1; flat after m. Card matches.",
    "LX1-c027": "L03 extract 32 (Definition 2.1): L_t = V_t/N_t. Card matches.",
    "LX1-c028": "L03 extract 27 (Assumption 1.3): phi>0, beta>0; psi_t = phi(L_t - L_0). Card matches.",
    "LX1-c029": "L03 extract 34-35 (Definition 2.2 chain with A1, A2, A3; 'describes the model'). Card matches.",
    "LX1-c030": "L03 extract 38 (Lemma 3.1 hypotheses C = N_0 + D, ell(x) = x/(C-x)) and 42 (L_t = ell(V_t), L_0 = D/N_0); strict increase on [D, C) in the same lemma and proof 40-41. Card matches.",
    "LX1-c031": "L03 extract 24 (V_m < N_0 + D in Assumption 1.2), 45 (Proposition 3.2(a)) and proof 49. Card hypotheses and bound match.",
    "LX1-c032": "L03 extract 46 (Proposition 3.2(b)) and " + RC + " (ell closed form): depth(12) = 9.204597%, depth(4) = 2.686713%, both from the formula; card matches.",
    "LX1-c033": "L03 extract 47 (Proposition 3.2(c)) and proof 51: first attained at t = m; for m>=1 no earlier period attains it. Card matches.",
    "LX1-c034": "L03 extract 47 (depth(0) = 0) and proof 51; problem P2 extract 112 (m=0: P_t=1, V_t=D, premium 0). Card matches.",
    "LX1-c035": "L03 extract 54 (Corollary 3.3 hypotheses 0<=m'<m<=H, conclusion) and proof 56; L03 twin output (out/twin_L03.out) depths 2.69 (m=4) < 9.20 (m=12). Card matches.",
    "LX1-c036": "L03 extract 58-60 (Corollary 3.4, 1<=m'<m<=H, ratio of ell differences, independent of beta and phi) and proof 62. Card matches.",
    "LX1-c037": "L03 twin output (out/twin_L03.out): 'economy X depth 9.20 percent of baseline output, first reached at t = 12'; " + RC + " 9.204597 -> 9.20, first at t = 12. Grade C with the lab named.",
    "LX1-c038": "L03 twin output: 'economy Y depth 2.69 percent ... first reached at t = 4'; " + RC + " 2.686713 -> 2.69, first at t = 4. Grade C with the lab named.",
    "LX1-c039": "L03 twin output Part D: three lines, each ratio 3.4260 for products 1/2, 1, 3; " + RC + " ratio 3.425970 for all three -> 3.4260. Grade C with the lab named.",
    "LX1-c040": "L03 extract 71 (Definition 4.1): central bank lends against collateral to solvent but illiquid institutions; solvent and illiquid defined. Card matches.",
    "LX1-c041": "L03 extract 71 (Definition 4.1, first sentence): public institution that issues the monetary base. Card matches.",
    "LX1-c042": "L03 extract 73 (Remark 4.2): no lending term in Assumption 1.2, no facility term in Assumption 1.3. Card matches.",
    "LX1-c043": "L03 extract 17 (one good, one borrower), 23 (Assumption 1.2: no default, no change to the balance sheet), 82 (misconception 1: no bank, no failure). Card matches.",
    "LX1-c044": "L03 extract 84 (misconception 2): ordering from durations 12 and 4 set by Lab 1 under Assumption 1.1; the model cannot say whether holding parity causes a deeper fall. Card matches.",
    "LX1-c045": "L03 extract 73 (Remark 4.2) and 71 (Definition 4.1): model has no lending facility; no claim about a panic. Card matches.",
    "LX1-c046": "L03 extract 88 (misconception 4), 46 (Proposition 3.2(b) factor beta phi) and 68 (no output series enters the lab). Card matches.",
    "LX1-c047": "L03 extract 29 (honest-pending note): no redistributable historical series embedded; lab runs the stylised model, labelled SIMULATED. Card matches.",
    "LX1-c048": "L04 extract 19 (Definition 1.1): ell_t = ln(x_t/x_(t-1)), per month, not annualized. Card matches.",
    "LX1-c049": "L04 extract 19 (Definition 1.1): sample standard deviation with denominator n-1; defined only for n>=2. Card matches.",
    "LX1-c050": "L04 extract 22 (Proposition 1.2, (A1), sum over t=a+1..b equals ln(x_b/x_a), b-a terms) and proof 24. Card matches.",
    "LX1-c051": "L04 extract 26 (Remark 1.3: exact in reals, checked to tolerance 1e-12) and tests/labs/LX1/lab-LX1-L04-1.py line 47 (SUM_TOLERANCE = 1e-12). Card matches.",
    "LX1-c052": "L04 extract 34 (Proposition 2.2 (A2), kappa>0, n>=2) and 35-38 (conclusion and proof: every change 0, dispersion 0). Card matches.",
    "LX1-c053": "L04 extract 30 (Definition 2.1: anchor currency, one foreign currency, kappa>0 anchor units per foreign unit, x_t>0; model plus (A2)). Card matches.",
    "LX1-c054": "L04 twin output (out/twin_L04.out) and lesson output line 45: 'months with an exactly zero change: 3: 1976-07, 2012-07, 2019-11'; " + RC + ": exact-rate zero months identical (1976-07, 2012-07, 2019-11); 668 - 3 = 665.",
    "LX1-c055": "L04 twin output: window one 'standard deviation 0.027935', 668 changes; " + RC + " sd = 0.0279353 -> 0.027935; denominator 667.",
    "LX1-c056": "L04 twin output: window two 'standard deviation 0.024700', 321 changes; " + RC + " sd = 0.0246995 -> 0.024700.",
    "LX1-c057": "L04 twin output Part D: ratio 0.8842; " + RC + " ratio 0.8841688 -> 0.8842. Grade C with the lab named.",
    "LX1-c058": "L04 twin output: window two largest absolute change 0.096575 at 2008-10, signed -0.096575; " + RC + " signed -0.0965747 at 2008-10.",
    "LX1-c059": "L04 extract 40 (Remark 2.3), 58 (misconception 1, counts 3 zeros among 668, 665 nonzero), 46 (Part B). Card matches.",
    "LX1-c060": "L04 extract 60 (misconception 2: Part D computes two SDs and a difference, no test, window start a convention) and 105 (Problem E3). Card matches.",
    "LX1-c061": "L04 extract 62 (misconception 3: ln 1.1 = 0.095310; difference 0.004690) and 71 (Problem M1). " + RC + ": ln 1.1 = 0.0953102; 0.1 - ln 1.1 = 0.0046898 -> 0.004690.",
    "LX1-c062": "L04 extract 31 (Bretton Woods system: definition pending a registry source), 55 (Section 4 historical arrangement) and 64 (misconception 4). Card matches.",
    "LX1-c063": "course/assets/data/market/MANIFEST.json: fx_daily 'first': '2000-01-03' and ust_daily 'first': '2000-01-03' (both read with a python json walk); L04 extract 44 (lab docstring) and 47 (window two start). Card matches.",
    "LX1-c064": "course/assets/data/market/MANIFEST.json fx_monthly: citation G.5/H.10 noon buying rates in New York, retrieved 2026-10-19, rows 669, first 1971-01, last 2026-09; fx_monthly.csv has 670 lines (header + 669) and sha256 60572240... equal to the MANIFEST (fetch_data --check: 0 problems); tools/data_sources.yaml fx_monthly note 'Spot rates only' and 'last noon rate of its month'. Card matches. Four facts in one card (see notes).",
    "LX1-c065": "NEW IN ROUND 2 (no round-1 row). L04 extract 46 (Section 3: numbers rounded half away from zero from unrounded values; difference -0.003236) and out/twin_L04.out Part D. " + RC + ": unrounded difference -0.0032358 -> -0.003236 (rounded-SD difference would be -0.003235). Card matches.",
}
assert set(EV) == {c["id"] for c in CARDS}, "evidence map must cover every card"

rows = []
for c in CARDS:
    cid = c["id"]
    rows.append({
        "id": "card-" + cid.split("-")[1],
        "check": "2.7-card-vs-lesson",
        "location": f"course/modules/LX/LX1/cards.json ({cid}); {LOC[c['lesson']]}",
        "status": "PASS",
        "evidence": EV[cid],
    })

rows += [
    {
        "id": "notation-L02-T",
        "check": "2.4-notation",
        "location": "course/modules/LX/LX1/L02.html, Proposition 2.1(b) proof (extract line 37)",
        "status": "FAIL",
        "evidence": "The proof writes 'Multiply the equalities of (a) for t = 1, ..., T' and 'V_T / V_0', 'P_0 / P_T', using T as a time index. notation/notation.json symbols[0] registers T as 'number of return observations (periods) in a sample' (module S1), and plans/LX1-build-plan.md section 2.3 says T is not used in LX1 and a time horizon is H. The conclusion (b) and the card use H.",
        "fix": "In the proof of Proposition 2.1(b) (L02.html, the paragraph beginning '(b) Multiply the equalities'), replace T by H throughout: 'for t = 1, ..., H', 'V_H / V_0', 'P_0 / P_H'. Then grep L02.html for \\(T\\) and confirm none remains.",
    },
    {
        "id": "prose-L02-misc2",
        "check": "2.2-numbers-and-labs",
        "location": "course/modules/LX/LX1/L02.html, misconception 2 (extract line 66)",
        "status": "FAIL",
        "evidence": "Misconception 2 says 'while the model contains no gold price at all, so the lab itself does not link the two prices'. The same lab's Part E (out/twin_L02.out) prints 'currency price of one gram = 1 / kappa = 5/2 currency units', and Definition 1.1 and Proposition 1.2 (extract 18-22) state a gold price. The sentence contradicts the lab and the proposition it cites.",
        "fix": "Replace 'while the model contains no gold price at all' with 'while the index model of Lab 1, Parts A to D, contains no gold price, so the lab does not link the two prices; Part E computes the gold price separately'.",
    },
    {
        "id": "data-fx-monthly-licence",
        "check": "2.8-data-licence",
        "location": "course/assets/data/market/MANIFEST.json fx_monthly; licence_url https://www.federalreserve.gov/disclaimer.htm",
        "status": "PASS",
        "evidence": "Plain curl (HTTP 200, ledgers/LX1/scripts/LX1-d-r2/out/curl_disclaimer.out) returns the page. The quoted text 'Unless otherwise indicated, information on Board's website is in the public domain and may be copied and distributed without permission. Please cite to the Board as the source of the information.' is on that page, and it matches the MANIFEST licence string. Grants redistribution.",
    },
    {
        "id": "scan-notation-other",
        "check": "2.4-notation",
        "location": "L01-L04 extract math spans (ledgers/LX1/scripts/LX1-d-r2 scan, round 2)",
        "status": "PASS",
        "evidence": "Scanned all math spans for the registered symbols and macros of notation/notation.json: \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q}, \\E, \\Prob, \\Var, \\Cov, \\SR, \\se: none used. \\ast appears only as F^{\\ast}_t in L01 (a different symbol from R^\\ast). T appears only in the L02 proof (row notation-L02-T).",
    },
    {
        "id": "scan-dag-outside-closure",
        "check": "2.9-dag",
        "location": "L01-L04 visible text; check_dag output",
        "status": "PASS",
        "evidence": "Grepped visible text for the D1-D15 names of the plan (bank run, fire sale, covered interest parity, efficient markets, moral hazard, expectation, etc.). Only 'covered interest' appears (L04 extract 51, named and not stated, plain prose as plan D5 allows). ledgers/LX1/out check_dag_LX1.out: check_dag LX1: PASS.",
    },
    {
        "id": "gate-check-pages",
        "check": "2.9-structure",
        "location": "tools/check_pages.py --unit LX1",
        "status": "PASS",
        "evidence": "ledgers/LX1/scripts/LX1-d-r2/out/check_pages_LX1.out: 'check_pages LX1: PASS' (includes check_cards, exit 0).",
    },
    {
        "id": "gate-check-dag",
        "check": "2.9-dag",
        "location": "tools/check_dag.py --unit LX1",
        "status": "PASS",
        "evidence": "out/check_dag_LX1.out: 'check_dag LX1: PASS', exit 0.",
    },
    {
        "id": "gate-run-labs",
        "check": "2.5-labs",
        "location": "tools/run_labs.py --unit LX1; tests/labs/LX1/lab-LX1-L01-1..L04-1.py",
        "status": "PASS",
        "evidence": "out/run_labs_LX1.out: 'run_labs LX1: PASS (7/7)', exit 0. Each twin run directly with python -I -W error (L04 from a scratch directory holding a copy of data/fx_monthly.csv): exit 0, empty stderr (out/twin_L0n.out, .err). page_smoke for LX1 also PASS (out/page_smoke_LX1.out).",
    },
    {
        "id": "gate-recompute",
        "check": "2.2-numbers",
        "location": "ledgers/LX1/scripts/LX1-d-r2/recompute_cards_r2.py",
        "status": "PASS",
        "evidence": "out/recompute_cards_r2.out (exit 0): Fraction and math recomputation from the CSV and the closed forms: F_0 6666.67 -> 6667; 40000/109 -> 367; 7072.67 -> 7073; q = 103/109; S_N identities True at N=10,60,200; 9 and 13 positive gaps; depth 9.204597% and 2.686713%; ratio 3.425970; falls=rises at [1,5,6,8,9,12]; window SDs 0.0279353 and 0.0246995; ratio 0.8841688; difference -0.0032358; ln 1.1 = 0.0953102; tanh(0.0679228) = 0.067819; ln(1.0678/0.9322) = 0.135808. Every card number matches.",
    },
    {
        "id": "scan-ids-sequence",
        "check": "2.7-structure",
        "location": "cards.json (65 cards)",
        "status": "PASS",
        "evidence": "out/card_checks_r2.out: ids LX1-c001..LX1-c065 in file order, unique; lessons L01 13, L02 12, L03 22, L04 18 (65 total). Round 1 counted 64; c065 is new and checked.",
    },
    {
        "id": "scan-duplicates",
        "check": "2.7-duplicates",
        "location": "cards.json (full scan of fronts)",
        "status": "PASS",
        "evidence": "out/card_checks_r2.out: front Jaccard >= 0.6 pairs c018/c019 (0.79), c035/c036 (0.83), c037/c038 (0.89), c055/c056 (0.90), c057/c065 (0.67). Each pair asks different facts (Prop 2.1 parts (a) and (b); Cor 3.3 and 3.4; economy X and Y; window one and two; the ratio and the difference). No duplicate card.",
    },
    {
        "id": "scan-numbers-in-lesson",
        "check": "2.7-numbers",
        "location": "cards.json fronts and backs",
        "status": "PASS",
        "evidence": "out/card_checks_r2.out: every decimal or integer token in each card's front and back appears in its lesson's extracted text ('number tokens ... absent: none').",
    },
    {
        "id": "scan-grades-basis",
        "check": "2.7-grades",
        "location": "cards.json",
        "status": "PASS",
        "evidence": "out/card_checks_r2.out: all 48 cards with grade have a basis; grades T 33, C 15. The 17 cards with no grade are definitions, conventions or the data and honest-pending notes (c001, c006, c014, c017, c020, c026-c029, c040, c041, c047, c048, c049, c053, c063, c064), which state no graded result (BUILDER_RULES section 7). C grades (c009, c010, c024, c025, c037-c039, c054-c060, c065) name the lab. Lesson key-results tables (L01 145-160, L02 127-136, L03 147-160, L04 123-132) agree with the card grades.",
    },
    {
        "id": "scan-banned-process-words",
        "check": "2.9-prose",
        "location": "cards.json",
        "status": "PASS",
        "evidence": "out/card_checks_r2.out: 'banned or process words in cards: none' (todo, tbd, lorem, verif*, builder, round, request, obviously, clearly, studies show, experts agree, ellipsis).",
    },
    {
        "id": "gate-ruff",
        "check": "2.5-labs",
        "location": "tests/labs/LX1",
        "status": "PASS",
        "evidence": "out/ruff_check.out: 'All checks passed!' and '7 files already formatted'.",
    },
    {
        "id": "gate-mypy",
        "check": "2.5-labs",
        "location": "tests/labs/LX1",
        "status": "PASS",
        "evidence": "out/mypy_LX1.out: 'Success: no issues found in 7 source files' (mypy --no-incremental).",
    },
    {
        "id": "gate-check-projects",
        "check": "2.6-projects",
        "location": "tools/check_projects.py --unit LX1",
        "status": "PASS",
        "evidence": "out/check_projects_LX1.out: 'check_projects LX1: PASS', exit 0 (outside this slice; run because the lab twins changed).",
    },
    {
        "id": "gate-verify-refs",
        "check": "2.1-citations",
        "location": "tools/verify_refs.py --offline",
        "status": "PASS",
        "evidence": "out/verify_refs_offline_all.out: 'offline integrity: 560 entries, 0 problems'. The cards cite no registry key (cite: [] on all 65 cards). The live run 'verify_refs.py --unit LX1' was NOT run here (it needs Crossref); the three lesson keys are not part of this card slice (see notes).",
    },
    {
        "id": "gate-page-smoke",
        "check": "2.9-structure",
        "location": "tools/page_smoke.py --unit LX1",
        "status": "PASS",
        "evidence": "out/page_smoke_LX1.out: 'page_smoke LX1: PASS' with modules/LX/LX1/L01-L04 and project PASS, index and concepts PASS; exit 0 (run alone).",
    },
    {
        "id": "gate-fetch-data",
        "check": "2.8-data",
        "location": "tools/fetch_data.py --check",
        "status": "PASS",
        "evidence": "out/fetch_data_check.out: 'fetch_data: 3 datasets, 0 problems', exit 0. sha256sum course/assets/data/market/fx_monthly.csv = 60572240d1a9d1832d5021297634b2369723b94098414948b891dd26a8bffe3e, equal to MANIFEST sha256. Live rebuild (--fetch) not run.",
    },
]

fragment = {
    "unit": "LX1",
    "slice": "LX1-d",
    "round": 2,
    "verifier": "Claude Haiku 5.5, independent verifier for LX1-d, round 2 (did not build LX1; round-1 fragment read as context only, its PASS rows not trusted)",
    "pin": "67c4768",
    "base": "1c1645f",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE2-LX1-d",
    "scratch": "/tmp/lx1d2_scratch (fx_monthly.csv copy for the L04 twin run); /tmp/lx1d2_L0n.txt (copied to ledgers/LX1/scripts/LX1-d-r2/out/)",
    "verified_at": "2026-11-04T07:45:34+00:00",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "Slice d: all 65 cards of course/modules/LX/LX1/cards.json against L01-L04 (extract_text.py output), read in full. "
        "Delta since round-1 pin 1c1645f: cards.json (c003, c005, c007, c012, c013, c019, c022, c023, c035, c043-c045, c051, c053, c057, c059, c062, c064 changed; c065 added), L01-L04 pages, lab twins L02 and L04. "
        "Every card was re-verified from scratch; no round-1 PASS row was carried. Round-1 FAIL rows c003, c013, c022, c023 are fixed and re-verified PASS. "
        "Two FAIL rows, both in lesson text the cards cite: notation-L02-T (T used as an index in L02 Prop 2.1(b) proof) and prose-L02-misc2 (misconception 2 says the model has no gold price while Part E computes one). "
        "Judgement calls, stated: compound fronts whose parts come from one printed lab line (c025, c037, c038, c054-c056) are accepted as one result; c064 bundles four dataset facts into one dataset-description card and is accepted, but a builder may split it. "
        "Not run or not checkable here: live verify_refs --unit LX1 (Crossref not contacted; the three lesson keys are outside the card slice; offline integrity 560/0 run instead); live rebuild of fx_monthly.csv from the Federal Reserve feed (fetch_data --fetch not run; sha256 and MANIFEST checks pass); pytest (no test file references LX1 cards or lessons); project graders, mutation tests and alternative implementations (LX1 is rubric-only, no grader). "
        "The card verdicts depend on the lesson text read through extract_text.py; if the page markup changes, rerun it and the card_checks_r2.py script."
    ),
    "summary": "LX1-d round 2: verdict FAIL. 65 card rows (65 PASS, round-1 FAILs c003/c013/c022/c023 now PASS) plus 2 FAIL lesson rows (notation-L02-T, prose-L02-misc2) and 19 PASS structure, data and gate rows.",
}

out = ROOT / "ledgers/LX1/LX1-d.json"
out.write_text(json.dumps(fragment, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out, "rows", len(rows))
