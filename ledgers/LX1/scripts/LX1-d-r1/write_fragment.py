"""Build the LX1-d round-1 fragment from the rows the verifier recorded (slice d: cards.json).

Every card row cites the lesson locator read in full (extract_text.py output, text line numbers),
the lab twin output (run under python -I -W error) or the recomputation (recompute_cards.py).
"""
import json

ROOT = "/Users/billyribeiro/.fanout/wt/verifyE1-LX1-d"
CARDS = f"{ROOT}/course/modules/LX/LX1/cards.json"
cards = json.load(open(CARDS, encoding="utf-8"))
by_id = {c["id"]: c for c in cards}

# (card id) -> (locator read in full, extra evidence). FAIL entries are handled separately.
PASS = {
    "LX1-c001": ("L01 Definition 1.2 (extract line 22-24)", "wording and the 'not a forecast' sentence match"),
    "LX1-c002": ("L01 Theorem 1.3 statement (extract 26-28) and proof (35)", "F_t = d_1(1+g)^t/(r-g) = d_(t+1)/(r-g) matches; hypotheses A0 and A1 carried"),
    "LX1-c003": ("L01 Theorem 1.3 statement (extract 28)", "identity S_N(t) = F_t(1-q^N) matches the statement; the lab sentence in its back is the FAIL row card-c003"),
    "LX1-c004": ("L01 Theorem 1.3 proof (extract 35)", "0 < q < 1 under A0; q^N -> 0"),
    "LX1-c005": ("L01 Proposition 1.4 (extract 37-38) and proof (40)", "hypotheses d_1>0, 1+g>0, r>-1, g>=r and (A1) carried; conclusion matches"),
    "LX1-c006": ("L01 Definition 2.1 (extract 43-44)", "B_t = P_t - F_t, bubble only when B_t > 0, integer cents"),
    "LX1-c007": ("L01 Proposition 2.2 (extract 45-46) and proof (48)", "hypotheses and F_0(g) < F_0(g') and the sign consequence match"),
    "LX1-c008": ("L01 Definition 3.1 (extract 59-60)", "mechanism wording matches; no frequency, trigger or size stated"),
    "LX1-c009": ("L01 Lab 1 twin output 'periods with price above fundamental: 9 of 13'; extract 116 (Empirical 1)", "count 9 of 13 reproduced by python -I -W error twin run"),
    "LX1-c010": ("L01 Lab 1 twin Part C output '13 of 13'; extract 57", "count 13 of 13 and 'changes with the growth rate: True' reproduced"),
    "LX1-c011": ("L01 Proposition 2.2 witness (extract 49) and misconception (77)", "6000 cents: gap +1000 under 1%, -2000/3 under 3%; recomputed F_0(1%)=5000, F_0(3%)=6666.67"),
    "LX1-c012": ("L01 Section 5 (extract 70) and misconception (80)", "400/1.09 = 366.97 -> 367; 400/0.06 = 6666.67 -> 6667 (recompute_cards.py)"),
    "LX1-c014": ("L02 Definition 1.1 (extract 17)", "parity kappa > 0 and convertibility wording match"),
    "LX1-c015": ("L02 Proposition 1.2 (extract 20-21) and proof (23)", "(A1) and conclusion 1/kappa at every date match"),
    "LX1-c016": ("L02 Remark 1.3 (extract 25) and Section 2 remark", "the hypothesis (A1) does not involve P_t: matches"),
    "LX1-c017": ("L02 Section 2 (extract 27-28)", "V_t = D P_0 / P_t in base-date cents matches"),
    "LX1-c018": ("L02 Proposition 2.1 hypotheses (extract 31-32) and part (a) (35)", "(A2) and (A3) carried; V_t/V_(t-1) = P_(t-1)/P_t matches"),
    "LX1-c019": ("L02 Proposition 2.1 conclusion (extract 33) and part (b) proof (36)", "V_T/V_0 = P_0/P_T for T >= 1 matches"),
    "LX1-c020": ("L02 Definition 3.1 (extract 41)", "rise in V_t produced by a fall in P_t with D fixed: matches"),
    "LX1-c021": ("L02 Corollary 3.2 (extract 43-44) and proof (46)", "(A2),(A3) carried; V_t > V_(t-1) iff P_t < P_(t-1) matches"),
    "LX1-c024": ("L02 Section 2 definition of V_t (extract 27-28); Lab 1 twin Part B values", "all 12 real values differ from predecessor: the twin's Part A changes are all nonzero (-1,+1,+1,+3,-4,-1,+2,-4,-3,+3,+2,-4)"),
    "LX1-c025": ("L02 Lab 1 twin output 'identity ... for t = 1 to 12: True', 'falling ... 6 of 12', 'rises ... 6 of 12', 'exactly where the index falls: True'", "reproduced by python -I -W error run; extract 127 key-results row agrees (grade C)"),
    "LX1-c026": ("L03 Assumption 1.1 (extract 18-20)", "P_t = (1-delta)^min(t,m), 0 <= m <= H, 0 < delta < 1 match"),
    "LX1-c027": ("L03 Definition 2.1 (extract 31)", "L_t = V_t / N_t matches"),
    "LX1-c028": ("L03 Assumption 1.3 (extract 26)", "psi_t = phi (L_t - L_0), phi > 0 matches"),
    "LX1-c029": ("L03 Definition 2.2 (extract 33-34)", "four-step chain with A1, A2, A3 labels matches; model-only scope stated"),
    "LX1-c030": ("L03 Lemma 3.1 statement (extract 37) and proof (39-41)", "C = N_0 + D; ell strictly increasing on [D, C); L_0 = D/N_0 match"),
    "LX1-c031": ("L03 Proposition 3.2(a) (extract 43-44) and proof (48)", "hypotheses incl. V_m < N_0 + D carried; V_t <= V_m, monotone to m, flat after m match"),
    "LX1-c032": ("L03 Proposition 3.2(b) (extract 45) and proof (49)", "closed form beta phi (ell(V_m) - ell(D)) matches; recomputed depth(12)=9.2046%, depth(4)=2.6867%"),
    "LX1-c033": ("L03 Proposition 3.2(c) (extract 46) and proof (50)", "first attained at t = m; no earlier period when m >= 1 matches"),
    "LX1-c034": ("L03 Proposition 3.2(c) proof (50); Problem P2 (111)", "m = 0 gives P_t = 1, V_t = D, premium 0, depth 0 matches"),
    "LX1-c035": ("L03 Corollary 3.3 (extract 52-53) and proof (55); Lab 1 twin Part C", "depth(m') < depth(m) for 0 <= m' < m <= H; twin prints depth 2.69 (m=4) < 9.20 (m=12)"),
    "LX1-c036": ("L03 Corollary 3.4 statement (extract 57-59) and proof (61)", "ratio of (ell differences), independent of beta and phi, matches"),
    "LX1-c037": ("L03 Lab 1 twin Part B output 'economy X depth 9.20 percent ... first reached at t = 12'; extract 64 hypothesis", "reproduced; recompute_cards.py depth(12) = 9.204597% -> 9.20, first at t = 12"),
    "LX1-c038": ("L03 Lab 1 twin Part B output 'economy Y depth 2.69 percent ... t = 4'", "reproduced; recompute_cards.py depth(4) = 2.686713% -> 2.69, first at t = 4"),
    "LX1-c039": ("L03 Lab 1 twin Part D output (three lines, each 3.4260); Corollary 3.4 (extract 57-59)", "reproduced; recompute_cards.py ratio = 3.425970 for phi = 1/2, 1, 3 (beta = 1) -> 3.4260"),
    "LX1-c040": ("L03 Definition 4.1 (extract 70)", "lender of last resort, solvent, illiquid wording matches"),
    "LX1-c041": ("L03 Definition 4.1 (extract 70)", "central bank: public institution issuing the monetary base matches"),
    "LX1-c042": ("L03 Remark 4.2 (extract 72)", "no lending term in A2 and no facility term in A3: matches"),
    "LX1-c043": ("L03 Misconception 1 (extract 81); Assumption 1.2 (extract 22)", "no bank, failure or default; proof of Prop 3.2 uses none: matches"),
    "LX1-c044": ("L03 Misconception 2 (extract 83)", "ordering from durations 12 and 4 set by Assumption 1.1; no causal claim: matches"),
    "LX1-c045": ("L03 Definition 4.1 (extract 70) and misconception 3 (85)", "collateral and solvent-but-illiquid restriction matches"),
    "LX1-c046": ("L03 misconception 4 (extract 87); Proposition 3.2(b)", "SIMULATED model value; depth proportional to beta phi: matches"),
    "LX1-c047": ("L03 honest-pending note (extract 28)", "no redistributable series embedded, stylised model labelled SIMULATED: matches"),
    "LX1-c048": ("L04 Definition 1.1 (extract 18)", "ell_t = ln(x_t/x_(t-1)), per month, not annualized: matches"),
    "LX1-c049": ("L04 Definition 1.1 (extract 18)", "sample SD with n-1, defined for n >= 2: matches"),
    "LX1-c050": ("L04 Proposition 1.2 (extract 21) and proof (23)", "(A1) carried; sum = ln(x_b/x_a) with b-a terms: matches"),
    "LX1-c051": ("L04 Remark 1.3 (extract 25); tests/labs/LX1/lab-LX1-L04-1.py line 46 (SUM_TOLERANCE = 1e-12)", "floating-point check to 10^-12, not exact: matches"),
    "LX1-c052": ("L04 Proposition 2.2 (extract 32-33) and proof (35-36)", "(A2), kappa > 0, n >= 2 carried; zero changes and zero dispersion: matches"),
    "LX1-c053": ("L04 Definition 2.1 (extract 29) and Section 2 (extract 27)", "model class; no historical parity, participant or end: matches"),
    "LX1-c054": ("L04 Lab 1 twin Part B output 'months with an exactly zero change: 3: 1976-07, 2012-07, 2019-11'", "reproduced; recompute_cards.py exact-zero months (Fraction and float) agree; 668 - 3 = 665"),
    "LX1-c055": ("L04 Lab 1 twin Part C output 'window one ... changes 668; standard deviation 0.027935'", "reproduced; recompute_cards.py sd = 0.02793528 -> 0.027935; n = 668 (denominator 667)"),
    "LX1-c056": ("L04 Lab 1 twin Part C output 'window two ... changes 321; standard deviation 0.024700'", "reproduced; recompute_cards.py sd = 0.02469950 -> 0.024700; n = 321"),
    "LX1-c057": ("L04 Lab 1 twin Part D output (-0.003236; 0.8842)", "reproduced; recompute_cards.py: w2-w1 = -0.00323578 -> -0.003236; ratio 0.88417 -> 0.8842"),
    "LX1-c058": ("L04 Lab 1 twin Part C output 'largest absolute change 0.096575 at 2008-10 (signed -0.096575)'", "reproduced; recompute_cards.py signed change -0.0965747 at 2008-10"),
    "LX1-c059": ("L04 Misconception 1 (extract 56); Lab 1 twin Part B count 3", "665 nonzero of 668 in window one; Proposition 2.2 zero change is model-only: matches"),
    "LX1-c060": ("L04 Misconception 2 (extract 58); Problem E3 (103)", "lab computes two SDs and a difference, no test or cause: matches the code (no test in twin)"),
    "LX1-c061": ("L04 Misconception 3 (extract 60); Problem M1 (69)", "ln 1.1 = 0.0953102 -> 0.095310; 0.1 - ln 1.1 = 0.0046898 -> 0.004690 (recompute_cards.py)"),
    "LX1-c062": ("L04 Definition 2.1 (extract 29) and Section 4 (53); Misconception 4 (62)", "no historical fact stated: matches"),
    "LX1-c063": ("MANIFEST.json entries fx_daily and ust_daily ('first': '2000-01-03'); L04 extract line 45", "both begin 2000-01-03 in the MANIFEST: matches; start is a convention (line 51)"),
    "LX1-c064": ("MANIFEST.json entry fx_monthly (citation, retrieved 2026-10-19, rows 669, first 1971-01, last 2026-09); tools/data_sources.yaml lines 61-64 ('Spot rates only')", "all fields match; the 'no interest or forward rates' statement follows the note 'Spot rates only'"),
}

FAIL = {
    "LX1-c003": (
        "Back says 'Lab 1 Part A checks this' for the identity S_N(t) = F_t(1 - q^N) for every t; Part A checks only t = 0.",
        "L01 lab twin tests/labs/LX1/lab-LX1-L01-1.py Part A (f0 = fundamental(..., 0); identity = s_n == f0 * (1 - q**terms)); output 'N = 10 ... identity ... True' is for S_N(0); L01 extract line 36 says 'checks the identity S_N(0) = F_0 (1 - q^N)'.",
        "Back: 'Lab 1 Part A checks the t = 0 case, S_N(0) = F_0 (1 - q^N), in exact arithmetic for N = 10, 60 and 200; the identity for every t is the proof of Theorem 1.3.'",
    ),
    "LX1-c013": (
        "Card states the no-finite-benchmark claim with d_1 > 0 and g >= r only; the claim 'each discounted dividend is at least d_1/(1+r)' needs (A1) (dividends fixed by d_1 and g) and r > -1, as in Proposition 1.4 (A1, A2).",
        "L01 Proposition 1.4 hypotheses (extract line 38): '(A1) with d_1 > 0 and 1 + g > 0, and (A2) r > -1 and g >= r'; proof (extract line 40) uses (A1) at every term. Without (A1) a stream with d_2 = d_3 = ... = 0 has bounded partial sums, so the card's claim is false.",
        "Front: 'Under (A1) d_s = d_1 (1 + g)^(s-1) and (A2) r > -1, with d_1 > 0 and g >= r, is the benchmark a finite value?'",
    ),
    "LX1-c022": (
        "Card states the factor P_(t-1)/P_t 'which is larger than one' under a fixed nominal debt without stating (A2) or (A3), though its basis is Proposition 2.1(a).",
        "L02 Proposition 2.1 (extract lines 31-33): hypotheses (A2) D fixed, paid in full and (A3) P_t positive; Remark 3.3 (extract line 48) states the factor for a fall. Division by P_t and 'larger than one' need P_t > 0.",
        "Front: 'Under (A2) and (A3) of Proposition 2.1, when the price index falls from P_(t-1) to P_t, by what factor does the real value change?'",
    ),
    "LX1-c023": (
        "Card's answer 'A fall in P_t raises V_t' cites Corollary 3.2 but does not carry its hypotheses (A2) and (A3).",
        "L02 Corollary 3.2 (extract lines 42-44): hypotheses (A2) and (A3) of Proposition 2.1; the card front says only 'a fixed nominal debt'. Lab 1 Part C counts (6 of 12, 6 of 12, True) reproduced by the twin run.",
        "Front: 'Under (A2) and (A3) of Proposition 2.1, when prices fall, does a fixed nominal debt become cheaper to repay?'",
    ),
}

rows = []
for cid in [c["id"] for c in cards]:
    if cid in FAIL:
        summary, evidence, fix = FAIL[cid]
        rows.append({
            "id": f"card-{cid.split('-')[-1]}",
            "check": "2.7-card-vs-lesson",
            "location": f"course/modules/LX/LX1/cards.json ({cid}); {by_id[cid]['lesson']}.html",
            "status": "FAIL",
            "evidence": f"{summary} Evidence: {evidence}",
            "fix": fix,
        })
    elif cid in PASS:
        loc, extra = PASS[cid]
        rows.append({
            "id": f"card-{cid.split('-')[-1]}",
            "check": "2.7-card-vs-lesson",
            "location": f"course/modules/LX/LX1/cards.json ({cid}); {by_id[cid]['lesson']}.html",
            "status": "PASS",
            "evidence": f"Read in full against {loc}; {extra}.",
        })
    else:
        raise SystemExit(f"no verdict recorded for {cid}")

rows += [
    {"id": "scan-ids-sequence", "check": "2.7-structure", "location": "cards.json (64 cards)",
     "status": "PASS",
     "evidence": "scripts/LX1-d-r1/card_audit.py: ids LX1-c001..LX1-c064 in file order, unique (64 unique); lessons L01 13, L02 12, L03 22, L04 17; all four lessons covered."},
    {"id": "scan-duplicates", "check": "2.7-duplicates", "location": "cards.json (full scan)",
     "status": "PASS",
     "evidence": "card_audit.py jaccard scan of fronts (threshold 0.6): no duplicate card. Near pairs c018/c019 (0.79: parts (a),(b) of Prop 2.1), c035/c036 (0.69: Cor 3.3 vs 3.4), c037/c038 (0.88: economy X vs Y depth), c055/c056 (0.70: window one vs two) are distinct facts; read individually."},
    {"id": "scan-numbers-in-lesson", "check": "2.7-numbers", "location": "cards.json fronts and backs",
     "status": "PASS",
     "evidence": "card_audit.py: every decimal or integer token in each card's front and back appears in its lesson's visible text (0 problems)."},
    {"id": "scan-grades-basis", "check": "2.7-grades", "location": "cards.json",
     "status": "PASS",
     "evidence": "Every grade-T card has a basis; grade C cards (c009, c010, c023, c024, c025, c037-c039, c054-c060) name the lab; grades match the lesson key-results tables (L01 lines 144, L03 lines 147-148, L04 lines 121-122, L02 line 127). check_pages.py check_cards passes."},
    {"id": "scan-banned-process-words", "check": "2.9-prose", "location": "cards.json",
     "status": "PASS",
     "evidence": "grep -n -i -E 'todo|tbd|lorem|verif|builder|round|request|studies show|obviously|clearly|it is well known|\\.\\.\\.|beyond the scope|experts agree' cards.json: no match."},
    {"id": "gate-check-pages", "check": "2.9-structure", "location": "tools/check_pages.py --unit LX1",
     "status": "PASS",
     "evidence": "Run: .venv/bin/python tools/check_pages.py --unit LX1 -> 'check_pages LX1: PASS' (includes check_cards)."},
    {"id": "gate-check-dag", "check": "2.9-dag", "location": "tools/check_dag.py --unit LX1",
     "status": "PASS",
     "evidence": "Run: .venv/bin/python tools/check_dag.py --unit LX1 -> 'check_dag LX1: PASS'."},
    {"id": "gate-run-labs", "check": "2.5-labs", "location": "tests/labs/LX1/*.py (cards citing Lab 1 of L01-L04)",
     "status": "PASS",
     "evidence": "Run: .venv/bin/python tools/run_labs.py --unit LX1 -> 'run_labs LX1: PASS (7/7)'. Each L01-L04 twin also run directly: .venv/bin/python -I -W error tests/labs/LX1/lab-LX1-L0n-1.py exit 0, empty stderr; outputs in scratch /tmp/lx1d_out_*.txt."},
    {"id": "gate-recompute", "check": "2.2-numbers", "location": "scripts/LX1-d-r1/recompute_cards.py",
     "status": "PASS",
     "evidence": "Independent recomputation (Fraction, math, fx_monthly.csv): depths 9.2046 / 2.6867, ratio 3.42597, F_0 6666.67, 40000/109 = 366.97, 0.027935, 0.024700, 0.88417, -0.0032358, 0.0965747, ln 1.1 = 0.0953102; all match the cards."},
]

fragment = {
    "unit": "LX1",
    "slice": "LX1-d",
    "round": 1,
    "verifier": "Claude Haiku 5.5, independent verifier for LX1-d, round 1 (did not build LX1; read verifier-rules.md, VERIFIER_RULES.md, the LX1 plan and its Architect decisions)",
    "pin": "1c1645f",
    "base": None,
    "checkout": ROOT,
    "scratch": "/tmp/lx1d_scratch (fx_monthly.csv copy); kept copies of twin outputs, lesson text, card_audit.out and recompute_cards.out in ledgers/LX1/scripts/LX1-d-r1/out/",
    "verified_at": "2026-11-03T00:00:00+00:00",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "Slice d covers all 64 cards in course/modules/LX/LX1/cards.json against the four lessons (L01-L04), read in full. "
        "Every card was read against its lesson locator; every number was recomputed or matched to a twin output. "
        "Four FAIL rows: card-c003 (lab sentence overstates Part A, which checks only t = 0), card-c013 (omits (A1) and (A2) of Proposition 1.4), "
        "card-c022 and card-c023 (Proposition 2.1 / Corollary 3.2 results stated without (A2) and (A3)). "
        "Not run for this slice: page_smoke.py (the cards slice has no page of its own; the lesson pages belong to the other slices), ruff, mypy, pytest, verify_refs, run_graders (rubric-graded unit, no grader), "
        "render/fetch/build_site checks (no curriculum, site-data or market input is in this slice; the MANIFEST was read, not re-hashed). "
        "No mutants: cards carry no grader. Lesson-text issues outside the cards were not graded in this slice."
    ),
    "summary": "LX1-d round 1: verdict FAIL. 73 rows: 64 card rows (60 PASS, 4 FAIL: c003, c013, c022, c023) plus 9 structure, numbers and gate rows (all PASS).",
}

out = f"{ROOT}/ledgers/LX1/LX1-d.json"
with open(out, "w", encoding="utf-8") as fh:
    json.dump(fragment, fh, ensure_ascii=False, indent=1)
    fh.write("\n")
from collections import Counter
print(out, Counter(r["status"] for r in rows), len(rows))
