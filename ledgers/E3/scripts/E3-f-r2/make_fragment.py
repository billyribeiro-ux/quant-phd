"""Writes the round-2 verifier fragment ledgers/E3/E3-f.json for E3 slice f (cards of L01 to L04).

Every card row's evidence was written after reading the card and the lesson text (L01.html to L04.html, extracted
to plain text) and after running ledgers/E3/scripts/E3-f-r2/rederive_cards_L01_L04.py. Non-PASS rows give the fix.
Run with: python3 -I ledgers/E3/scripts/E3-f-r2/make_fragment.py
"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
CARDS_PATH = ROOT / "course/modules/E/E3/cards.json"
OUT = ROOT / "ledgers/E3/E3-f.json"
cards = json.loads(CARDS_PATH.read_text(encoding="utf-8"))
line_of: dict[str, int] = {}
for n, text in enumerate(CARDS_PATH.read_text(encoding="utf-8").splitlines(), start=1):
    if '"id": "E3-c' in text:
        line_of[text.split('"')[3]] = n

# card id -> evidence (PASS unless listed in FAILS)
EV: dict[str, str] = {
    "E3-c001": "L01.html Definition 1.1 (finite lottery): distinct outcomes, p_i >= 0, sum 1, equivalently a random variable; matches.",
    "E3-c002": "L01.html Definition 1.2 (E X = sum p_i x_i); matches. Definition, no grade.",
    "E3-c003": "L01.html Definition 1.3 (E u(X) = sum p_i u(x_i), a number depending on u); matches.",
    "E3-c004": "L01.html Assumption A1 and Section 4 ('Every sum in this lesson is finite (A1)'); matches.",
    "E3-c005": "L01.html Definition 2.1 (mixture, p_L(x)=0 convention); matches.",
    "E3-c006": "L01.html Definition 3.2 (risk neutral u=bx, b>0; EU = b E X); matches.",
    "E3-c007": "L01.html Proposition 2.2 under A1 (mixture is a finite lottery; weights >= 0 summing to 1); proof on page; T correct.",
    "E3-c008": "L01.html Proposition 2.3 under A1, u real-valued on outcomes of L and M, alpha in [0,1]; identity re-derived; T correct.",
    "E3-c009": "L01.html Remark 2.4: Prop 2.3 is an identity about Definition 1.3 and says nothing about preference orderings; matches; T.",
    "E3-c010": "L01.html Proposition 3.1 under A1: E u(X) = a + b E X; a=0,b=1 gives EX; matches; T.",
    "E3-c011": "L01.html Proposition 3.3 under A1 with b>0: E v(L)-E v(M) = b(E u(L)-E u(M)); matches; T.",
    "E3-c012": "Round-1 FAIL cured: cards.json grade T now present. L01.html Problem P2 (b<0 reverses ranking; solution identical to card); re-derived; hypothesis A1 carried; T correct.",
    "E3-c013": "L01.html Problem R1 solution: max attained by a pays-for-certain outcome with u=m; equality iff p_i=0 wherever u(x_i)<m; matches; T with fixed finite set carried.",
    "E3-c014": "L01.html Section 5 misconception 1: u(EX)=150^2=22500 CU^2 vs E u(X)=45000 CU^2 for lottery A (Example 1.4); re-derived; T correct.",
    "E3-c015": "L01.html Section 5 misconception 2 contains the 'probability-weighted average' phrase; Definition 3.2 gives only EU = b E X. The card's locator attaches the phrase to Definition 3.2 only; content true.",
    "E3-c016": "L01.html Lab 1 Part A output: A 15000/15000/45000, B 12500/12500/21250, C 15000/15000/37500 (expected value, linear EU, quadratic EU); re-derived exactly (rederive_cards_L01_L04.py); grade C basis matches; exact, no data.",
    "E3-c017": "L01.html Lab 1 Part B output: six 'equal True' lines (alpha 1/4,1/3,1/2 x linear/quadratic); re-derived count 6; basis 'Lab 1, part B' matches; C correct.",
    "E3-c018": "L02.html Assumption A2: u twice differentiable on open I, u'>0, u''<=0; concavity defined by sign of u''; matches.",
    "E3-c019": "L02.html Proposition 1.1 'Assuming F1 and F5, under A1 to A3': exactly one c with u(c)=E u(X); card carries hypotheses and conclusion; T.",
    "E3-c020": "L02.html Definition 1.2 (CE is the unique c with u(c)=E u(X), CE(X;u)); matches.",
    "E3-c021": "L02.html Definition 1.2 (risk premium E X - CE; 'the risk premium is the certainty-equivalent risk premium, and nothing else'); matches.",
    "E3-c022": "L02.html Proposition 1.3(a) 'Assuming F1, F2 and F5, under A1 to A3' with tangent-line proof (Steps 1-3); card matches; T.",
    "E3-c023": "L02.html Proposition 1.3(b) with A4 (u''<0) and an outcome of positive probability differing from E X; matches; T.",
    "E3-c024": "L02.html Definition 2.1: r_A = -u''/u' (1/CU), r_R = w r_A (dimensionless); matches.",
    "E3-c025": "L02.html Proposition 2.2 (b>0; v'=bu', v''=bu''; factor b cancels where u'(w)!=0); matches; T.",
    "E3-c026": "L02.html Example 2.3 ('by F6'): r_A=1/(2w), r_R=1/2; at w=100 r_A=0.005, r_R=0.5; re-derived; card carries 'Assuming F6'; T.",
    "E3-c027": "L02.html Proposition 3.1 'Assuming F1, F3, F4 and F5, under A1 and A5', E X=0: pi(eps)/eps^2 -> (1/2) r_A s^2; card matches; T.",
    "E3-c028": "L02.html Remark 3.2: asymptotic statement, error/eps^2 -> 0, no bound at fixed eps; matches; T.",
    "E3-c029": "L02.html Section 5 misconception 1 (line 399) and cards.json: 'half of Var(X) gives 900 CU'. Var(X)=1800 CU^2 (Lab header variance_cu2 1800), so 1/2 Var(X) = 900 CU^2, not CU. Pratt 4.5 CU and exact 5.065835 CU are correct; ratio 177.66 re-derived.",
    "E3-c030": "L02.html Example 2.3 derives r_A=0.005 and r_R=0.5 at w=100 'by F6'; the T card states them without 'Assuming F6'. Numbers re-derived correct; the hypothesis is omitted.",
    "E3-c031": "L02.html Section 5 misconception 3: u(w)=w gives CE=EX for every finite lottery (u(c)=c=E X); matches; T.",
    "E3-c032": "L02.html Lab 1 Part A output: ce_cents 9493, premium_cents 507, r_A 0.005000, r_R 0.500000, exact 5.065835, Pratt 4.500000, error 0.565835; re-derived; grade C basis 'Lab 1, part A' matches.",
    "E3-c033": "L02.html Lab 1 Part B output: premium/eps^2 5.065835 at eps=1 to 4.500046 at eps=0.01, gaps_shrink True; re-derived 4.500045564 (printed 4.500046); C correct.",
    "E3-c034": "L02.html Section 4 (line 'which is 11.17 percent'): 0.565835/5.065835 = 0.111696 -> 11.17 percent of the exact premium (basis stated); re-derived; C basis 'section 4; Lab 1, part A' matches.",
    "E3-c035": "L02.html Lab 1 Part C output: linear premium 0 cents at eps 1.0, 0.5, 0.1; linear_premium_zero_at_three_scales True; re-derived; C basis matches.",
    "E3-c036": "L03.html Definition 1.1: w^a = e^(a ln w), w>0; matches.",
    "E3-c037": "L03.html Proposition 1.2 for w>0, real a,b and positive x,y, real c; proof on page; matches; T.",
    "E3-c038": "L03.html Definition 1.3: u_gamma = (w^(1-gamma)-1)/(1-gamma) for gamma != 1, u_1 = ln w; matches.",
    "E3-c039": "L03.html Proposition 1.4 is 'Assuming A2' (line 94-95): the card's T claim 'it gives a finite limit at gamma = 1' omits A2. Other claims verified (u_gamma(1)=0, Prop 2.7 with a=1>0). Round-1 grade-None FAIL is cured (grade T present).",
    "E3-c040": "L03.html Proposition 1.4 'Assuming A2': lim u_gamma(w) = ln w; card carries A2; identity u_gamma = L (e^h-1)/h with h=sL re-checked; T.",
    "E3-c041": "L03.html Proposition 1.7 'Assuming F2': u'=w^(-gamma), u''=-gamma w^(-gamma-1), r_A=gamma/w, r_R=gamma; re-derived; card carries F2; T.",
    "E3-c042": "L03.html Definition 1.6 recalled; points to L02 Definition 2.1 (confirmed L02.html Definition 2.1). Definition, no grade. Content duplicates c024 (see dup row).",
    "E3-c043": "L03.html Theorem 2.1 'Assuming F1 and F2', A3 and A4: u = K u_gamma + C with K>0; proof uses F1 on ln u'; card matches; T.",
    "E3-c044": "L03.html Remark 2.2: Theorem 2.1 does not say any investor has CRRA; no source cited; matches.",
    "E3-c045": "L03.html Definition 2.3: 'every outcome is positive, so each x_i lies in the domain of Assumption A1'; matches.",
    "E3-c046": "L03.html Proposition 2.4 (gamma != 1: CE = M^(1/s), M = sum p x^s; gamma=1: exp(sum p ln x)); re-derived; T.",
    "E3-c047": "L03.html Example 2.5: CE_2 = 1600 cents, CE_1 = 2000 cents for 1000/4000 lottery; re-derived exactly; T.",
    "E3-c048": "L03.html Proposition 2.6 (k>0, every real gamma, (kx)^s = k^s x^s); matches; T.",
    "E3-c049": "L03.html Proposition 2.7 (a>0, real b, CE under u exists and is unique); matches; T.",
    "E3-c050": "L03.html Remark 2.8 rounding rule: value computed once as float, half up, floor(v+1/2) for v>=0, no intermediate rounding; matches; convention, definitional, no grade needed.",
    "E3-c051": "L03.html Section 4 misconception 1 cites Proposition 1.7, which is 'Assuming F2'. The T card states r_R = gamma without 'Assuming F2'. Content otherwise true (d/dw of gamma/w is negative for gamma>0).",
    "E3-c052": "L03.html Section 4 misconception 2 and Proposition 1.4 ('Assuming A2', carried). Content matches; duplicates c040 (see dup row).",
    "E3-c053": "L03.html Section 3 ('The numbers in Lab 1 are one lottery') and Problem R3 exist; Lab 1 checks six GAMMAS values; card matches; T as a statement about the lab's scope.",
    "E3-c054": "L03.html Lab 1 output: gamma 0 11250.0000, gamma 1 10000.0000, gamma 2 8888.8889, gamma 4 7337.6161 cents; re-derived to 5e-5; 'falls as gamma rises' True; C basis matches.",
    "E3-c055": "L03.html Problem E2 and Lab 1 output '80000/9': M = sum p/x = 9/80000 (re-derived), CE = 1/M = 80000/9 = 8888.89; T via Proposition 2.4.",
    "E3-c056": "L04.html Definition 1.1: F_X(t)=P(X<=t), I_X(t)=integral of F_X from minus infinity to t; matches.",
    "E3-c057": "L04.html Lemma 1.2 under A1: I_X(t)=E[(t-X)^+]; proof on page; T.",
    "E3-c058": "L04.html Definition 1.3 (first-order dominance: F_X<=F_Y for every t; 'at least as likely to exceed every level'); matches.",
    "E3-c059": "L04.html Definition 1.4 nondecreasing: u(s_j)<=u(s_{j+1}); matches.",
    "E3-c060": "L04.html Theorem 1.5 under A1 (FOSD iff E u(X)>=E u(Y) for nondecreasing u on S); proof on page (summation by parts; indicator witnesses); T.",
    "E3-c061": "L04.html Lemma 1.6 under A1: support points suffice; proof on page for t between support points; T.",
    "E3-c062": "L04.html Proposition 1.8 under A1, 'This holds without A2'; integration of pointwise inequality; matches; T.",
    "E3-c063": "L04.html Definition 2.1 under A1 and A2: I_X(t)<=I_Y(t) for every real t; matches.",
    "E3-c064": "L04.html Lemma 2.2 under A1 and A2: D affine on each support interval; matches; T.",
    "E3-c065": "L04.html Theorem 2.3 under A1 and A2: I_X<=I_Y for every t iff E u(X)>=E u(Y) for nondecreasing concave u on S; matches; T.",
    "E3-c066": "L04.html Remark 2.4: only-if proof uses concavity (c_j>=0) and A2 (vanishing affine term), not monotonicity; re-read proof; correct.",
    "E3-c067": "L04.html Example 2.5 integrated values X: 500,1000,2000 at 3000,4000,5000; Y: 250,500,1250,2000 at 2000..5000; means 3000 and 3000; re-derived exactly; T.",
    "E3-c068": "L04.html Example 2.5: F_X(2000)=1/2>1/4=F_Y(2000) and F_Y(3000)=3/4>1/2=F_X(3000), so no FOSD ranking; re-derived. Content correct; overlaps c074 (see dup row).",
    "E3-c069": "L04.html Example 2.6: X 1/2 on 1000 and 5000, Y 3000 certain, equal means; no FOSD ranking; I_Y<=I_X on support; re-derived. Content correct; overlaps c072 (see dup row).",
    "E3-c070": "L04.html Example 1.7: F_X=(1/2,1/2,1), F_Y=(0,1/2,1) on 2000,3000,4000; Y dominates X in FOSD; re-derived exactly; T.",
    "E3-c071": "L04.html Problem R3 solution: I_X(s_m)=s_m-EX gives EX>=EY; slope b_1=sigma_{m-1}>=0 for nondecreasing u; decomposition re-derived by hand; card hypotheses (A1, nondecreasing concave, A2 not assumed) carried; T.",
    "E3-c072": "L04.html Section 4 misconception 1 ('Equal means make one lottery dominate the other'); Example 2.6 equal means and no FOSD ranking; content correct; overlaps c069 (see dup row).",
    "E3-c073": "L04.html Lab 1 output: SOSD 'no ranking' for pairs 16 and 19 (2 of 8 equal-mean pairs); Section 4 misconception 2 names pairs 16 and 19; C basis 'Lab 1 (SIMULATED)' matches.",
    "E3-c074": "L04.html Section 4 misconception 3 (Example 2.5 has SOSD ranking, no FOSD ranking); content correct; overlaps c068 (see dup row).",
    "E3-c075": "L04.html Lab 1 output: FOSD over 24 pairs X dom 3, Y dom 10, identical 1, no ranking 10 (sum 24); agree 24 of 24; SIMULATED basis matches; C.",
    "E3-c076": "L04.html Lab 1 output: SOSD on 8 equal-mean pairs X dom 3, Y dom 2, identical 1, no ranking 2; agree 8 of 8; C basis matches.",
    "E3-c077": "L04.html Section 3 (Where the canon breaks: test set is finite) and Lab 1 docstring (finite test set); the 'No' answer is correct; T as a statement about the lab's scope.",
    "E3-c159": "L02.html Remark 1.4 lists A2 (u''(xi)<=0, u'>0), F2 (Step 1), F1 (Step 3), A3 (outcomes in I); card matches; proof-structure card, no grade.",
    "E3-c160": "L03.html Lab 1 check 'gamma 1 +/- 1e-6 within 0.01 cents' (code and printed True); card's 'not a proof' caveat matches; C basis matches.",
    "E3-c161": "L02.html Lab 1 Part B and Section 3 ('the lab checks five scales ... not a proof of that limit'); matches; C.",
    "E3-c162": "L02.html Remark 1.4 last sentence: u''>=0 case, Steps 1-3 reversed, 'this lesson does not state that case as a result'; matches.",
    "E3-c167": "L04.html Definition 1.4: chord slopes sigma_1>=...>=sigma_{m-1}; card 'nonincreasing in j for j=1 to m-1' matches; definition, no grade.",
    "E3-c168": "L03.html Remark 2.8: |R(kv)-kR(v)| <= (k+1)/2; re-derived proof (|R(kv)-kv|<=1/2, |kR(v)-kv|<=k/2, triangle inequality); grid check ratio<=1; T.",
    "E3-c171": "L03.html Lab 1 homogeneity line (k=2,3,10 at six gammas, unrounded True); caveat 'not a proof for all lotteries' matches; C basis matches.",
}
FAILS: dict[str, tuple[str, str]] = {
    "E3-c015": (
        "Section 5 misconception 2 introduces the 'probability-weighted average' phrase; Definition 3.2 says only EU = b E X. "
        "The card attaches the averaging claim to Definition 3.2 alone; the true locator is Definition 1.2 and Section 5 misconception 2.",
        "Change the locator to '(Definitions 1.2 and 3.2)' or to 'Definition 1.2' for the averaging phrase.",
    ),
    "E3-c029": (
        "L02.html line 399 (Section 5) and the card say the half-variance rule gives 900 CU. Var(X)=1800 CU squared, so half of it is 900 CU squared. "
        "The unit is wrong in both places; the card repeats the lesson's error.",
        "Change the card to 'the half-variance rule gives 900 CU squared' and fix L02.html line 399 the same way (owner: L02 builder).",
    ),
    "E3-c030": (
        "Card is graded T and gives r_A = 0.005 per CU and r_R = 0.5 at w = 100 for u = sqrt(w), which Example 2.3 derives 'by F6'. "
        "The card omits the assumption. Numbers verified correct.",
        "Prefix the back with 'Assuming F6,' (as card E3-c026 does).",
    ),
    "E3-c039": (
        "Card is graded T and claims 'it gives a finite limit at gamma = 1'. That limit is Proposition 1.4, which is 'Assuming A2' (L03.html line 94-95). "
        "The card omits A2. Other parts verified; the round-1 grade FAIL is cured.",
        "Change the back to 'Assuming A2, it gives a finite limit at gamma = 1 (Proposition 1.4)'.",
    ),
    "E3-c051": (
        "Card is graded T and states r_R = gamma from Proposition 1.7, which is 'Assuming F2' (L03.html Proposition 1.7). The card omits F2.",
        "Prefix the statement with 'Assuming F2,' (as card E3-c041 does).",
    ),
}
DUP_FAILS: list[tuple[str, str, str, str]] = [
    (
        "E3f-dup-c024-c042",
        "E3-c024 (L02) and E3-c042 (L03) test the same definition of the Arrow-Pratt measures (Definition 2.1 of L02) with the same answer.",
        "Delete E3-c042, or change it to test a fact L03 adds (for example r_A = gamma/w for CRRA, already E3-c041).",
    ),
    (
        "E3f-dup-c040-c052",
        "E3-c040 and E3-c052 both assert the Proposition 1.4 limit u_gamma(w) -> ln w as gamma -> 1 under A2.",
        "Keep one. Reword the other to a different fact, or merge them into one card.",
    ),
    (
        "E3f-dup-c068-c074",
        "E3-c068 and E3-c074 both test that Example 2.5 has no first-order ranking and a second-order ranking.",
        "Keep E3-c068; reword E3-c074 to a conceptual question without restating the Example 2.5 comparison, or delete it.",
    ),
    (
        "E3f-dup-c069-c072",
        "E3-c069 and E3-c072 both test that Example 2.6 has equal means and no first-order ranking.",
        "Keep E3-c072 (the general misconception); drop the Example 2.6 detail from E3-c069 or delete it.",
    ),
]

rows: list[dict[str, str]] = []
for card in cards:
    if card["lesson"] not in {"L01", "L02", "L03", "L04"}:
        continue
    cid = card["id"]
    row_id = "E3f-" + cid.replace("-c", "-c")
    loc = f"cards.json:{line_of[cid]} ({cid}, {card['lesson']})"
    if cid in FAILS:
        evidence, fix = FAILS[cid]
        rows.append({"id": f"E3f-{cid}", "check": "2.7-cards", "location": loc, "status": "FAIL",
                     "evidence": evidence, "fix": fix})
    else:
        rows.append({"id": f"E3f-{cid}", "check": "2.7-cards", "location": loc, "status": "PASS",
                     "evidence": EV[cid]})
    del row_id
for row_id, evidence, fix in [(d[0], d[1], d[2]) for d in DUP_FAILS]:
    rows.append({"id": row_id, "check": "2.7-duplicates", "location": "cards.json (slice L01-L04)",
                 "status": "FAIL", "evidence": evidence, "fix": fix})

COMMANDS = [
    ("E3f-cmd-check-pages", "2.9-structure",
     "tools/check_pages.py --unit E3 -> 'check_pages E3: PASS', exit 0 (scripts/E3-f-r2/out/check_pages_E3.txt); covers cards.json unique ids, lessons, grades, keys."),
    ("E3f-cmd-check-dag", "2.9-dag",
     "tools/check_dag.py --unit E3 -> 'check_dag E3: PASS', exit 0 (out/check_dag_E3.txt)."),
    ("E3f-cmd-run-labs-L01", "2.5-labs",
     "tools/run_labs.py --unit E3 --page L01 -> 'run_labs E3: PASS (1/1)', exit 0 (out/run_labs_L01.txt)."),
    ("E3f-cmd-run-labs-L02", "2.5-labs",
     "tools/run_labs.py --unit E3 --page L02 -> 'run_labs E3: PASS (1/1)', exit 0 (out/run_labs_L02.txt)."),
    ("E3f-cmd-run-labs-L03", "2.5-labs",
     "tools/run_labs.py --unit E3 --page L03 -> 'run_labs E3: PASS (1/1)', exit 0 (out/run_labs_L03.txt)."),
    ("E3f-cmd-run-labs-L04", "2.5-labs",
     "tools/run_labs.py --unit E3 --page L04 -> 'run_labs E3: PASS (1/1)', exit 0 (out/run_labs_L04.txt)."),
    ("E3f-cmd-twins-python-I-W-error", "2.5-labs",
     "python3 -I -W error tests/labs/E3/lab-E3-L0n-1.py for n=1..4: exit 0 each, stderr 0 bytes; stdout in out/twin_L0n.stdout; outputs match the page's expected blocks read in the text extraction."),
    ("E3f-cmd-page-smoke", "2.9-structure",
     "tools/page_smoke.py --unit E3 --pages L01.html L02.html L03.html L04.html --skip-labs -> 'page_smoke E3: PASS', exit 0 (out/page_smoke_L01_L04.txt). Run alone, not with other slices."),
    ("E3f-cmd-rederive-cards", "2.7-cards",
     "python3 -I ledgers/E3/scripts/E3-f-r2/rederive_cards_L01_L04.py -> 51 OK lines, 0 FAIL, 'ALL OK'. Independent Fraction and float re-derivation of every number on the L01-L04 cards."),
    ("E3f-cmd-scan-cards", "2.7-cards",
     "python3 -I ledgers/E3/scripts/E3-f-r2/scan_cards.py (out/scan_cards.txt): 168 cards, 84 in slice; no exact duplicate front, back or id over the file; one near-duplicate pair above 0.6 (c060/c065, FOSD vs SOSD characterisations, distinct); grade C all with basis; grade T none with basis; no slice card cites a registry key; registered symbols absent (local S, m, sigma only)."),
    ("E3f-cmd-verify-refs-offline", "2.1-citations",
     "tools/verify_refs.py --offline -> 'offline integrity: 560 entries, 0 problems', exit 0 (out/verify_refs_offline.txt). Slice cards cite no keys, so no entry of the registry is used by slice f; this is the unit-independent integrity run."),
    ("E3f-cmd-ruff-script", "2.9-structure",
     "ruff check ledgers/E3/scripts/E3-f-r2/ -> 'All checks passed!' (scripts under ledgers/*/scripts are excluded from the repo lint; checked anyway)."),
]
for cid, check, ev in COMMANDS:
    rows.append({"id": cid, "check": check, "location": "tools and ledgers/E3/scripts/E3-f-r2/", "status": "PASS", "evidence": ev})

non_pass = [r for r in rows if r["status"] != "PASS"]
fragment = {
    "unit": "E3",
    "slice": "f",
    "round": 2,
    "verifier": "Claude Haiku 5.5, independent verifier for E3 slice f, round 2 (did not build E3; cards of L01 to L04)",
    "pin": "c737272 (checkout detached at c737272f5bdef4a027417989cd52254555e8a0bb)",
    "base": "round-1 pin not recorded in frags/D-E3-f.round1.json. Delta to the slice from c737272: cards.json E3-c004, c009, c012, c018, c021, c039 (grade added), c042, c162, c167; L01-L04 HTML unchanged by c737272 (git show --stat).",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyD2-E3-f",
    "scratch": "/Users/billyribeiro/.fanout/scratch/E3-f-r2",
    "verified_at": datetime.now(UTC).isoformat(timespec="seconds"),
    "verdict": "PASS" if not non_pass else "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "Round 2. All 84 slice cards re-verified from scratch; no PASS row carried from round 1 (the round-1 rows E3f-E3-c012 and E3f-E3-c039 "
        "re-verified: c012 now PASS, c039 now FAIL on the omitted A2). Every card row cites the lesson locator and the command or script that backs it. "
        "Scripts: ledgers/E3/scripts/E3-f-r2/ (rederive_cards_L01_L04.py, scan_cards.py, make_fragment.py, out/). Not run: pytest (no Python tool changed in the slice), "
        "mypy (no tools/ change), render_curriculum, build_site, fetch_data (no curriculum, site-data or market input changed in the slice); the mutation suite "
        "(no grader in slice f); the live verify_refs run (offline only). Not checked: the seeded-pair counts of L04 Lab 1 were confirmed by running the lab's own code, "
        "not by an independent generator; hours; the lesson-level prose outside the cards (L01-L04 section texts were read in full, but only as the source the cards cite)."
    ),
    "summary": (
        f"E3 slice f round 2: verdict {'PASS' if not non_pass else 'FAIL'}. {len(rows)} rows: "
        f"{len(rows) - len(non_pass)} PASS, {len(non_pass)} non-PASS ({sum(1 for r in non_pass if r['check'] == '2.7-duplicates')} duplicate, "
        f"{sum(1 for r in non_pass if r['check'] == '2.7-cards')} card). Non-PASS: E3-c015 locator, E3-c029 units (900 CU vs CU^2, also in L02.html line 399), "
        "E3-c030, E3-c051 (omitted F-assumptions), E3-c039 (omitted A2), and four near-duplicate card pairs."
    ),
}
OUT.write_text(json.dumps(fragment, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"wrote {OUT} rows={len(rows)} non_pass={len(non_pass)} verdict={fragment['verdict']}")
