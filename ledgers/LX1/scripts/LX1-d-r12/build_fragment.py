"""Write the LX1-d round-12 ledger fragment from the evidence gathered in this round.

Every row cites a file and line (lesson HTML line numbers as printed by the page-text dump, cards.json ids) or a
script under ledgers/LX1/scripts/LX1-d-r12/ with its recorded output in out/.
Run with: python3 -I -W error ledgers/LX1/scripts/LX1-d-r12/build_fragment.py
"""

import json
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path("ledgers/LX1")
S = "ledgers/LX1/scripts/LX1-d-r12"
rows: list[dict[str, str]] = []


def row(rid: str, check: str, location: str, evidence: str, status: str = "PASS", fix: str | None = None) -> None:
    item = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        item["fix"] = fix or ""
    rows.append(item)


CARDS = "course/modules/LX/LX1/cards.json"

# Gate and script rows (re-run this round; outputs saved under out/).
row("gate-check-pages", "2.9 structure + cards schema", CARDS,
    f"Command: .venv/bin/python tools/check_pages.py --unit LX1 -> 'check_pages LX1: PASS', exit 0 ({S}/out/check_pages_LX1.txt). check_cards covers ids, lessons, grades, cite keys, basis.")
row("gate-check-dag", "2.9 DAG", "course/modules/LX/LX1/L01-L04.html; " + CARDS,
    f"Command: .venv/bin/python tools/check_dag.py --unit LX1 -> 'check_dag LX1: PASS', exit 0 ({S}/out/check_dag_LX1.txt).")
row("gate-run-labs", "2.5 labs", "tests/labs/LX1/lab-LX1-L01-1.py .. lab-LX1-L04-1.py, project labs",
    f"Command: .venv/bin/python tools/run_labs.py --unit LX1 -> 'run_labs LX1: PASS (7/7)', exit 0 ({S}/out/run_labs.txt).")
row("gate-page-smoke", "2.9 page smoke", "course/modules/LX/LX1/L01.html .. L04.html",
    f"Command: .venv/bin/python tools/page_smoke.py --unit LX1 --pages L01 L02 L03 L04 --skip-labs -> L01..L04 PASS, 'page_smoke LX1: PASS', exit 0 ({S}/out/page_smoke.txt).")
row("gate-verify-refs-offline", "2.1 registry integrity", "references/references.json",
    f"Command: .venv/bin/python tools/verify_refs.py --offline -> 'offline integrity: 560 entries, 0 problems', exit 0 ({S}/out/verify_refs.txt). (--unit needs a live run and was not run.)")
row("gate-mypy-ruff-pytest", "tooling gate for the checked files", "tests/labs/LX1/*.py; tests/test_page_checks.py; tests/test_run_labs.py",
    "Commands: .venv/bin/ruff check course tools tests/labs/LX1 -> 'All checks passed!'; .venv/bin/ruff format --check tests/labs/LX1 -> '7 files already formatted'; .venv/bin/pytest -q tests/test_page_checks.py tests/test_run_labs.py -> exit 0 (collected count and tail line recorded in out/pytest_page_checks_run_labs.txt). mypy not run: no Python tooling file in this slice changed since round 10.")
row("gate-notation", "2.4/2.9 notation", "notation/notation.json; course/modules/LX/LX1/L0[1-4].html; " + CARDS,
    "notation/notation.json holds 8 registered symbols (T, Phi, gamma_3, gamma_4, R*, R^{e*}, R_f, Q); none occurs in cards.json or in the LX1 pages (grep of the card text). Cards use F_t, d_s, r, g, q, N, P_t, B_t, V_t, N_t, L_t, psi_t, phi, beta, delta, m, H, C, kappa, D, ell, depth; all are defined in the lesson the card cites. Observation, not a registry collision: 'ell' is used as ell(x) in L03 Lemma 3.1 and as ell_t (log change) in L04 Definition 1.1; each card names its lesson.")
row("gate-dag", "2.9 DAG, cards side", CARDS,
    "check_dag.py --unit LX1 PASS (see gate-check-dag). Card terms defined in-lesson or in an earlier lesson of the unit: 'price index' (L02 Section 2), 'parity duration' (L03 Assumption 1.1), 'Bretton Woods' (L04 Definition 2.1 pending note line 86), 'lender of last resort' (L03 Definition 4.1 line 390). No card names a concept from another unit (grep of cards.json front and back for E5, M1-M3, E1-E3 returns nothing; the M1 mention at cards c061 is in basis, a worked problem of this lesson).")
row("data-manifest-facts", "2.8 data", "course/assets/data/market/MANIFEST.json (fx_monthly, fx_daily, ust_daily)",
    f"sha256sum course/assets/data/market/*.csv: fx_daily.csv 02872dd7...d59 = MANIFEST sha256; fx_monthly.csv 60572240...e3 = MANIFEST sha256; ust_daily.csv dd70e1a2...a0 = MANIFEST sha256. MANIFEST: fx_monthly first 1971-01, last 2026-09, rows 669, transform 'month-end (each column's last value in the month)', GBP=RXI$US_N.B.UK, retrieved 2026-10-19; fx_daily and ust_daily first 2000-01-03. The three SHAs match the MANIFEST on this pin. The byte-for-byte rebuild from the live feed was not run (plain curl and fetch are outside this slice).")
row("data-register-note", "2.8 licence / register", "tools/data_sources.yaml:50-66",
    "fx_monthly note: 'Each value is the last noon rate of its month ... Spot rates only, as for fx_daily.' This supports L04.html:329 (spot-only) and card c070 (no interest-rate or forward-rate column). Licence text 'public domain ... cite to the Board' quoted in MANIFEST and the register.")
row("lesson-curriculum-claims", "2.9 curriculum claims", "curriculum/06-profession-capstone.yaml:25, :41",
    "Re-verified this round: sed -n '25p;41p' curriculum/06-profession-capstone.yaml prints the Dutch Republic-to-2008 episode sentence (line 25) and the lab title 'Gold-standard adherence vs. depression depth on embedded data' (line 41). git diff 00a84795 HEAD on that file is empty. Cards cite no curriculum line.")
row("registry-citations", "2.1 citations (cards side)", "references/references.json; course/modules/LX/LX1/L01.html:488, L02.html:537, L03.html:640, L04.html:569",
    "Recomputed from references/references.json entries: eichengreen1992golden 'Golden fetters: the gold standard and the Great Depression, 1919-1939' (1992); friedman1963monetary 'A monetary history of the United States 1867-1960' (1963); garber2000famous 'Famous First Bubbles: The Fundamentals of Early Manias' (2000). Lesson citations: L01.html:488 (Garber, 2000), L02.html:537 (Eichengreen, 1992; 'Cited for its title only'), L03.html:640 (Friedman, 1963; 'at book level only'); each title and year matches the registry. L04.html:567 cites no registry key (it names the Board dataset as the MANIFEST records it). No card cites a registry key (cite is [] on all 79 cards). This round's registry hunks: generated_at bumped; reinhart2009this used_by gained LX1, matching the hub reading list index.html:206 (hub, not in this slice).")
row("card-coverage", "2.7 coverage", CARDS,
    f"Per lesson: L01 13 cards, L02 17, L03 29, L04 20 (79 total). Every definition, theorem/proposition/lemma/corollary, key empirical result and misconception of L01 (Defs 1.2, 2.1, 3.1; Thm 1.3; Props 1.4, 2.2; misconceptions 1-3; Key results rows), L02 (Defs 1.1, 3.1; Props 1.2, 2.1; Cor 3.2; Remark 2.2; misconceptions 1-3), L03 (Assumptions 1.1-1.3; Defs 2.1, 2.2, 4.1; Lemma 3.1; Props 3.2(a)-(c); Cors 3.3, 3.4; misconceptions 1-4) and L04 (Defs 1.1, 2.1; Props 1.2, 2.2; misconceptions 1-4) has at least one card. Assumption 1.1 of L01 has no card of its own; its content is carried by c001 and c002 (the closed form under A0, A1).")
row("scan-duplicates", "2.7 duplicate scan", CARDS,
    f"{S}/cards_scan.py (output out/cards_scan.txt): 79 cards, 79 unique ids; no identical fronts. Near-duplicate pairs (difflib ratio > 0.5) reviewed: c037/c038 (economy X vs Y), c055/c056 (window one vs two), c041/c076, c035/c036 (Cor 3.3 vs 3.4), c057/c065 (ratio vs difference), c018/c019 (parts a, b), c009/c010 (two counts), c040/c080, c020/c080, c039/c067 (value vs invariance). Each pair asks a different fact.")
row("scan-process-words", "2.9 / 12 process words", CARDS,
    f"{S}/cards_scan.py: banned/process-word regex over all front+back text. Hits: 'fixed' (domain sense: fixed nominal debt, fixed parity, fixed-parity model), 'fixes' and 'fix' (c012, c014, c016: 'what does a gold standard fix'), 'US' (c064: 'US dollars per pound'). No hit is a process word (no 'round', 'batch', 'revised', 'verifier', 'builder').")
row("grade-scan", "2.3 grades and basis", CARDS,
    "All 17 cards with grade C name a SIMULATED lab output in basis (c009, c010, c025, c037, c038, c039, c054-c058, c060, c065-c068, c081) or an embedded-data output with its MANIFEST entry. All 36 cards with grade T name a proof, a proposition, a worked calculation or a remark in basis (basis present on every T card). The 26 cards without grade are definitions, or factual claims about the code and data (c047, c063, c064, c070) that cite the data source in the lesson.")
row("card-lesson-term-monetary-base", "2.7 term used before definition", "course/modules/LX/LX1/L03.html:390 (Definition 4.1); cards c040, c041, c076, c080",
    "The round-9 defect (monetary base term) is absent from cards.json on this pin: grep of 'monetary base' in cards.json returns no hit; the L03 solvency and illiquidity terms are defined in Definition 4.1, line 390, which is where cards c040, c041, c076, c080 take them.")
row("card-numbers", "2.7 card numbers appear in lesson", CARDS,
    f"{S}/card_numbers.py (output out/card_numbers.txt): 156 number tokens across the 79 cards; 0 absent from the card's own lesson HTML (after tag stripping). Individual values re-derived in {S}/card_claims_check.py (out/card_claims_check.txt).")
row("lab-text-compare", "2.5 lab output vs page text", "course/modules/LX/LX1/L01.html .. L04.html; tests/labs/LX1/lab-LX1-L0[1-4]-1.py",
    f"{S}/lab_text_compare.py (out/lab_text_compare.txt): each twin run under python -I -W error exits 0 with empty stderr; output lines L01 38, L02 41, L03 56, L04 17; 0 lines missing from the page text (whitespace-normalised). Every number a card quotes from a lab (c009, c010, c025, c037-c039, c054-c058, c060, c065-c068, c081) is on a printed line.")
row("recompute-l04-cards", "2.2 numbers, 2.8 data", "course/assets/data/market/fx_monthly.csv (GBP column); cards c054-c058, c063-c065, c068",
    f"{S}/recompute_l04_cards.py -I -W error on the embedded CSV (out/recompute_l04_cards.txt): 669 rows 1971-01..2026-09; 668 changes; exact-zero months 1976-07, 2012-07, 2019-11 (3; nonzero 665); window one sd 0.027935277917784617 (n=668); window two sd 0.024699501387683342 (n=321, first change 2000-01 from 1999-12); ratio 0.8841688 -> 0.8842; difference unrounded -0.0032357765 -> -0.003236 (printed-figure difference -0.003235); largest window-two |change| 0.0965747 at 2008-10, signed -0.096575; largest window-one 0.135846 at 1985-03. All cited values reproduce.")
row("card-claims-recompute", "2.2 numbers (cards not from a lab)", "course/modules/LX/LX1/L01.html:120, :310; L03.html:110, :395; L04.html:350",
    f"{S}/card_claims_check.py (out/card_claims_check.txt): F(1%)=5000, F(3%)=20000/3, 6000 lies above under 1% and below under 3% (c011); PV of 400 at date 1 at 9% = 40000/109 = 366.97 -> 367 (c012); ln 1.1 = 0.095310, 0.1 - ln 1.1 = 0.004690 (c061); V_m = 1084165.78 < N_0 + D = 5000000 (c082); depth X 9.2046 -> 9.20, depth Y 2.6867 -> 2.69, ratio 3.42597 -> 3.4260 (c037-c039, c067).")

# Per-card rows. Each row: lesson locator (page-text line numbers) and what was re-derived.
CARD = {
 "c001": "L01.html:65-67 Definition 1.2: F_t = sum d_(t+k)/(1+r)^k, 'whenever the series converges', 'not a forecast' (line 67). Card front/back match.",
 "c002": "L01.html:71-74 Theorem 1.3 statement (A0, A1; F_t = d_1(1+g)^t/(r-g) = d_(t+1)/(r-g); F_0 = d_1/(r-g)); proof 79-84.",
 "c003": "L01.html:74 S_N(t) = F_t(1-q^N) for every N>=1; proof 82-83; Part A check lines 246-248 (identity True for N=10, 60, 200; output verbatim per lab_text_compare).",
 "c004": "L01.html:83-84 proof: 1-q = (r-g)/(1+r) > 0 and 0<q<1 under A0; q^N -> 0.",
 "c005": "L01.html:90-91 Proposition 1.4: (A1) d_1>0, 1+g>0; (A2) r>-1, g>=r; S_N(0) -> +inf, series does not converge; proof 96.",
 "c006": "L01.html:104-105 Definition 2.1: B_t = P_t - F_t counted only when B_t>0; measured in cents; B_t<=0 has no bubble.",
 "c007": "L01.html:109-114 Proposition 2.2 hypotheses (A3) d_1>0; (A4) g<g', r>g, r>g', 1+g>0, 1+g'>0; conclusion line 114 F_0(g)<F_0(g'); proof 119.",
 "c008": "L01.html:288-289 Definition 3.1: mechanism only; 'does not say how often', 'what triggers', 'how large' (line 289).",
 "c009": "L01 lab Part B output line 264 'periods with price above fundamental: 9 of 13' (twin run output identical; lab_text_compare).",
 "c010": "L01 lab Part C output lines 280-281: '13 of 13' and 'the count changes with the assumed growth rate: True'; 9 of 13 at line 264.",
 "c011": "L01.html:120 witness: F_0(1%)=5000, F_0(3%)=20000/3; gap +1000 and -2000/3 at P_0=6000. Re-derived in card_claims_check.py.",
 "c012": "L01.html:310 Section 5: d_1=400, d_2=0, d_s=0 for s>=3, r=9%: 400/1.09 = 40000/109 -> 367 cents (re-derived 366.97). Misconception 2 at line 322.",
 "c013": "L01.html:96 proof of Proposition 1.4 (q>=1 so each term >= d_1/(1+r)); misconception 3 at line 323 (cited in basis).",
 "c014": "L02.html:57 Definition 1.1: parity kappa>0, grams of gold per unit, convertibility on demand.",
 "c015": "L02.html:65-67 Proposition 1.2: (A1) parity kept at every date; conclusion one gram costs 1/kappa; proof 71-72.",
 "c016": "L02.html:77 Remark 1.3 (conclusion holds whatever P_t does, since (A1) does not involve P_t); misconception 2 at line 323 (cited in basis).",
 "c017": "L02.html:82-83 V_t = D P_0/P_t; D nominal amount in integer cents; P_0 base value.",
 "c018": "L02.html:89-92 Proposition 2.1 hypotheses (A2) D fixed positive integer cents, paid in full; (A3) P_t>0; conclusion (a) line 92; proof 97 (D P_0 cancels).",
 "c019": "L02.html:92 conclusion (b) V_H/V_0 = P_0/P_H; proof 98 telescopes.",
 "c020": "L02.html:109-110 Definition 3.1 debt deflation: rise in V_t implied by a fall in P_t with D fixed; 'not a claim about the cause'.",
 "c021": "L02.html:116-118 Corollary 3.2: (A2),(A3); V_t > V_(t-1) iff P_t < P_(t-1); proof 123.",
 "c022": "L02.html:89-90 Proposition 2.1 hypotheses are (A2) and (A3) only; Remark 2.2 at 102-103 (holds for every index path satisfying (A3)).",
 "c023": "L02.html:118 Corollary 3.2 direction; misconception 1 at lines 318-319 (falling prices and cheaper debt).",
 "c024": "L02.html:83 identity V_t = D P_0/P_t; misconception 3 at lines 326-327 (constant only when P_t is constant).",
 "c025": "L02 lab Part B output line 287 'identity V_t / V_(t-1) = P_(t-1) / P_t holds exactly for t = 1 to 12: True'.",
 "c026": "L03.html:57-60 Assumption 1.1: 0<delta<1, 0<=m<=H, P_t = (1-delta)^min(t,m), P_0=1; flat after m.",
 "c027": "L03.html:82 Definition 2.1: leverage L_t = V_t/N_t.",
 "c028": "L03.html:72 Assumption 1.3: phi>0, beta>0; psi_t = phi(L_t - L_0); Definition 2.1 line 82 (external-finance premium).",
 "c029": "L03.html:87 Definition 2.2: chain A1/A2 then A2 then A3 then f_t = beta psi_t; 'describes the model'. Card matches line for line.",
 "c030": "L03.html:95-103 Lemma 3.1: C = N_0 + D, ell(x) = x/(C-x) strictly increasing on [D,C); L_t = ell(V_t) when V_t<C; L_0 = D/N_0.",
 "c031": "L03.html:108-109 Proposition 3.2(a): hypotheses Assumptions 1.1-1.3 incl. V_m < N_0+D (line 66); V_t <= V_m for every t; proof 116.",
 "c032": "L03.html:110 Proposition 3.2(b) closed form depth(m) = beta phi (ell(V_m)-ell(D)) = beta phi (V_m/(N_0+D-V_m) - D/N_0); proof 117.",
 "c033": "L03.html:111 Proposition 3.2(c): maximum first attained at t=m; proof 118 (m>=1 strictly increasing V before m).",
 "c034": "L03.html:118 proof (m=0 gives V_t=D, f_t=0); Problem P2 solution line 473 (depth(0)=0).",
 "c035": "L03.html:125 Corollary 3.3 (0<=m'<m<=H; X m=12, Y m'=4); proof 130; L03 lab Part B output line 361 'X is deeper than Y: True'.",
 "c036": "L03.html:135-137 Corollary 3.4 (1<=m'<m<=H; ratio formula, independent of beta and phi); proof 142.",
 "c037": "L03 lab Part B output line 359 'economy X depth 9.20 percent ... first reached at t = 12' (twin verbatim); re-derived 9.2046 in card_claims_check.py.",
 "c038": "L03 lab Part B output line 360 'economy Y depth 2.69 percent ... first reached at t = 4'; re-derived 2.6867.",
 "c039": "L03 lab Part D output line 380-382: ratio 3.4260 at product 1 (line 381); re-derived 3.42597.",
 "c040": "L03.html:390 Definition 4.1: central bank lending against collateral to solvent but illiquid institutions.",
 "c041": "L03.html:390 Definition 4.1 illiquid: cannot meet payments from own resources in time available.",
 "c042": "L03.html:395 Remark 4.2: Assumption 1.2 has no lending term; Assumption 1.3 has no facility term; 'says nothing about what such a facility would do'.",
 "c043": "L03.html:413-414 misconception 1 ('model has no bank and no failure'); Assumption 1.2 line 65 (no default, no other balance-sheet change).",
 "c044": "L03.html:417-418 misconception 2: ordering from durations 12 and 4; 'cannot say whether holding parity causes a deeper fall'.",
 "c045": "L03.html:421-422 misconception 3: Definition 4.1 requires collateral; Remark 4.2 line 395 'no such facility, so no panic result'.",
 "c046": "L03.html:425-426 misconception 4: SIMULATED, beta=1, no output series; depth changes in proportion through beta phi (Proposition 3.2(b), line 110).",
 "c047": "L03.html:76 honest-pending note (no redistributable historical series for gold-standard adherence or output depth is embedded; lab stays SIMULATED); lab docstring lines 152-155 ('uses no data').",
 "c048": "L04.html:59 Definition 1.1: ell_t = ln(x_t/x_(t-1)), per month, not annualised.",
 "c049": "L04.html:59 Definition 1.1: dispersion = sample sd with denominator n-1 about the mean; defined only for n>=2.",
 "c050": "L04.html:65-66 Proposition 1.2 (A1): positive rates a..b, a<b; sum ell_t = ln(x_b/x_a); b-a terms; proof 71.",
 "c051": "L04.html:76 Remark 1.3 (exact in reals, checked to 1e-12); lab code line 47 of tests/labs/LX1/lab-LX1-L04-1.py: SUM_TOLERANCE = 1e-12 (grep re-run this round).",
 "c052": "L04.html:90-94 Proposition 2.2 hypothesis line 92 (A2 for the model with kappa>0, n>=2, x_t = kappa at the month before the first change and every later month); conclusion 94 (a) zero changes, (b) zero dispersion; proof 98-100.",
 "c053": "L04.html:85 Definition 2.1: anchor, one foreign currency, kappa>0, x_t>0; fixed-parity model = plus (A2) 'x_t = kappa from the month before the first change to the last'.",
 "c054": "L04 lab Part B output line 308 'months with an exactly zero change: 3: 1976-07, 2012-07, 2019-11'; recompute_l04_cards.py reproduces the same three months.",
 "c055": "L04 lab Part C output line 310 'window one ... changes 668; standard deviation 0.027935'; recompute sd 0.0279353 (n-1=667).",
 "c056": "L04 lab Part C output line 313 'window two ... changes 321; standard deviation 0.024700'; recompute 0.0246995.",
 "c057": "L04 lab Part D output line 318 'ratio ... 0.8842'; recompute 0.8841688.",
 "c058": "L04 lab Part C output line 314 'largest absolute change 0.096575 at 2008-10 (signed -0.096575)'; recompute -0.0965747.",
 "c059": "L04.html:94 Proposition 2.2 (A2) is a model statement; Remark 2.3 at line 105: 'says nothing about a recorded rate, which need not equal its parity at any month'.",
 "c060": "L04 lab Part D output lines 316-317; misconception 2 lines 345-346 ('computes no test ... names no cause'); Problem E3 lines 431-433 ('No ... computes no standard error, no test statistic').",
 "c061": "L04.html:350 misconception 3 (ln 1.1 = 0.095310; difference 0.004690); Problem M1 lines 367-369 (1.25 to 1.375 gives the same ratio 1.1). Re-derived in card_claims_check.py.",
 "c062": "L04.html:81, 86 (Bretton Woods definition pending), 333 (Section 4 list), 353-354 misconception 4 ('states no historical fact about the arrangement').",
 "c063": "L04.html:110, 127-129 (window two starts 2000-01, first month where fx_daily and ust_daily have data); MANIFEST.json fx_daily and ust_daily 'first': '2000-01-03'.",
 "c064": "L04.html:117-121 lab docstring (fx_monthly.csv, G.5/H.10 noon buying rates in NY, GBP, last value of month); MANIFEST.json fx_monthly citation and transform.",
 "c065": "L04 lab Part D output line 317 '-0.003236'; L04.html:319 'computed from the unrounded standard deviations'; recompute -0.0032357765 -> -0.003236.",
 "c066": "L02 lab Part C output lines 289-291: 6 of 12 falling, 6 of 12 rising, 'exactly ... True'; rises and falls both at t=1,5,6,8,9,12 (re-derived from Part B values).",
 "c067": "L03 lab Part D output lines 380-382: same ratio 3.4260 for beta*phi 1/2, 1, 3; L03.html:383 text 'the printed ratio is the same in all three cases'.",
 "c068": "L04 lab Part B output line 308 (3 zeros of 668); L04.html:51 and 342 (665 nonzero); Problem E1 line 419 (668 - 3 = 665). The 665 is derived from the printed count, as E1 shows.",
 "c069": "No LX1-c069 exists in cards.json (ids are not required to be contiguous; check_pages PASS; no duplicate). Nothing to verify.",
 "c070": "L04.html:122 docstring 'holds exchange-rate columns only ... no interest-rate column and no forward-rate column'; L04.html:329 (spot-only, cannot test interest-rate relation); MANIFEST fx_monthly columns list (ten exchange-rate columns only).",
 "c071": "L03.html:65 N_t = N_0 - (V_t - V_0); 'whole rise in the real debt falls on net worth' (Assumption 1.2). L03.html:232 (lab code leverage()) uses the same N.",
 "c072": "L03.html:73 depth(m) = max over 0<=t<=H of f_t (Assumption 1.3); L03.html:260 (lab code depth()) = max(depth_path(...)).",
 "c073": "L02.html:82 nominal debt: owed amount in currency units, not indexed to prices; here D cents.",
 "c074": "L02.html:82 price index P_t at date t, base date 0, positive values, P_0 the base value.",
 "c075": "No LX1-c075 exists in cards.json (absent id, not a defect; no duplicate). Nothing to verify.",
 "c076": "L03.html:390 Definition 4.1 'Solvent means that the institution's assets, valued as the lender values them, cover its liabilities.'",
 "c077": "No LX1-c077 exists in cards.json (absent id, not a defect; no duplicate). Nothing to verify.",
 "c078": "L02.html:57 Definition 1.1 convertibility: 'the issuer stands ready to buy and sell gold at the parity on demand.'",
 "c079": "L03.html:109 Proposition 3.2(a) real-debt path: V_t = D(1-delta)^(-t) for t<=m, strictly increasing when m>=1; V_t = V_m for t>=m; proof 116.",
 "c080": "L03.html:390 Definition 4.1 'A central bank is the public institution that issues the currency.'",
 "c081": "L02 lab Part B output lines 274-286: real values 1000000, 1010101, 1000100, ... 1055909; every consecutive pair differs (checked over the 12 steps this round); misconception 3 line 327.",
 "c082": "L03.html:65-66 Assumption 1.2 (V_m = D(1-delta)^(-m) < N_0 + D); L03.html:109 Proposition 3.2(a); L03.html:395 Remark 4.2: 'V_t < N_0 + D and N_t > 0 in every period' (the citation is accurate). N_t = N_0 + D - V_t since V_0 = D. Numeric: V_4 = 1084165.78 < 5000000 (card_claims_check.py).",
}
for n in range(1, 83):
    cid = f"c{n:03d}"
    if cid in CARD:
        where = "" if CARD[cid].startswith("No LX1-") else "; " + CARD[cid].split(" ")[0]
        row(f"card-{cid}", "2.7 card vs lesson", f"{CARDS} (LX1-{cid}){where}",
            f"Card checked against the current lesson text. {CARD[cid]}")
rows = [r for r in rows]  # keep order

# Structure and lesson-side rows: the delta and whole-unit notes.
row("delta-hunks", "delta since round-10 pin 00a84795 (3 commits to 5db69a9b)",
    "course/modules/LX/LX1/cards.json; L03.html; L04.html; project.html; tests/labs/LX1/lab-LX1-L04-1.py",
    "git diff 00a84795 HEAD read in full for every LX1 file in the slice's scope. cards.json: c012 (d_2=0 wording), c022 (front/back), c052 (hypothesis wording), c053 (A2 wording), c082 added: each checked against L01 line 310, L02 lines 89-92 and 97-103, L04 lines 85 and 92, L03 line 395. L03.html and L04.html hunks are prose (why-it-matters, honest-pending, Definition 2.1 wording, Assumption 1.3 'Definition 2.1' link, Corollary 3.3 name, 'exchange rates only' bullet): none changes a number or claim cited by a card. project.html and lab-LX1-L04-1.py docstring hunks read; outside the cards slice.")
row("round11-fragment", "round-11 context fragment", "/Users/billyribeiro/.fanout/frags/E-LX1-d.round11.json",
    "The file named in the task does not exist in /Users/billyribeiro/.fanout/frags/ (the latest LX1-d fragment is E-LX1-d.round10.json, PASS). Round-10 row ids are kept where the subject is re-verified on this pin; no PASS row is carried from round 10 without re-reading its subject.")
row("mutants", "2.6 mutation", "not a project slice",
    "Slice d is the cards slice; the 2.6 mutation rule applies to project graders. No mutants are written for this slice (mutants []).")

for r in rows:
    if r["status"] == "PASS" and r["evidence"].strip() == "":
        raise SystemExit(f"empty evidence {r['id']}")

fragment = {
    "unit": "LX1",
    "slice": "LX1-d",
    "round": 12,
    "verifier": "Claude Haiku 5.5, independent verifier for LX1-d (ALL cards.json against L01-L04), round 12. Did not build LX1.",
    "pin": "5db69a9bee460736c318ebfacc7200ee5a6eb0f0",
    "base": "00a84795f276456fce19d4181373cc4efba11a36 (round-10 pin; the round-11 fragment named in the task is absent, so the delta is taken from the last available pin)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE12-LX1-d",
    "scratch": "/Users/billyribeiro/.fanout/scratch-LX1-d-r12 (plain-text lesson dumps L01-L04.txt, lab-twin outputs out_L0x.txt, labcmp/)",
    "scripts": "ledgers/LX1/scripts/LX1-d-r12/",
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "verdict": "PASS" if all(r["status"] == "PASS" for r in rows) else "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Round 12 of LX1-d: 79 cards (c001-c068, c070-c074, c076, c078-c082; c069, c075, c077 absent). Every card read against its lesson text with line citations; every lab-quoted number matched to a printed line of the twin run; every L04 data number recomputed from the embedded CSV.",
        "Card c082 (new since round 10) checked: Assumption 1.2 inequality and Remark 4.2 wording match.",
        "Changed since round 10 and re-verified: c012, c022, c052, c053 (wording only; numbers unchanged).",
        "Not checked: the full gate chain (mypy --no-incremental, the complete pytest suite, verify_refs live run, fetch_data --check, render_curriculum, build_site --check, run_graders, mutate_graders, check_projects) because they cover other slices; the lab twin versus the page code (a labs-slice row); the MANIFEST rebuild from the live feed (plain curl not run; sha256 of the embedded CSVs matches MANIFEST).",
        "Observation, not a fail: ell is used for two different objects in L03 (Lemma 3.1, ell(x)) and L04 (Definition 1.1, ell_t); no notation.json entry covers LX1 symbols.",
    ],
    "summary": f"Round 12 of LX1-d: {len(rows)} rows; every row PASS. Cards c001-c082 (79 present) checked against L01-L04 with line citations; lab numbers matched to printed output; L04 data numbers recomputed; gates re-run on this pin.",
}
out = ROOT / "LX1-d.json"
out.write_text(json.dumps(fragment, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("wrote", out, "rows", len(rows), "verdict", fragment["verdict"])
