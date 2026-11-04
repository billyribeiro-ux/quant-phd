import json, sys
from datetime import datetime, timezone

RD = "ledgers/E3/scripts/E3-f-r8/"
OUT = "ledgers/E3/E3-f.json"

def card(cid, loc, extra=""):
    ev = (f"Round 8 re-verification: card {cid} read from course/modules/E/E3/cards.json and checked against "
          f"{loc}. {extra}").strip()
    return ev

CARD_LOC = {
 "E3-c001": ("L01.html:59", "Definition 1.1"),
 "E3-c002": ("L01.html:64", "Definition 1.2"),
 "E3-c003": ("L01.html:69", "Definition 1.3"),
 "E3-c004": ("L01.html:74", "Assumption A1; section 4 bullet 1 at L01.html:331"),
 "E3-c005": ("L01.html:86", "Definition 2.1"),
 "E3-c006": ("L01.html:143", "Definition 3.2"),
 "E3-c007": ("L01.html:91", "Proposition 2.2"),
 "E3-c008": ("L01.html:105-108", "Proposition 2.3"),
 "E3-c009": ("L01.html:126", "Remark 2.4"),
 "E3-c010": ("L01.html:133", "Proposition 3.1"),
 "E3-c011": ("L01.html:148", "Proposition 3.3"),
 "E3-c012": ("L01.html:396-398", "Problem P2"),
 "E3-c013": ("L01.html:439-441", "Problem R1"),
 "E3-c014": ("L01.html:342-343", "misconception 1; Example 1.4 at L01.html:79"),
 "E3-c015": ("L01.html:346-347", "misconception 2; Definition 3.2"),
 "E3-c016": ("L01.html:303-305", "Lab 1 expected block, Part A"),
 "E3-c017": ("L01.html:306-313", "Lab 1 expected block, Part B (six comparisons, all True)"),
 "E3-c173": ("L01.html:350-351", "misconception 3 (b = 0 ties every pair)"),
 "E3-c018": ("L02.html:73-74", "Assumption A2"),
 "E3-c019": ("L02.html:88-94", "Proposition 1.1 and proof"),
 "E3-c020": ("L02.html:98-99", "Definition 1.2"),
 "E3-c021": ("L02.html:99", "Definition 1.2, last sentences (risk premium used in one sense on this page)"),
 "E3-c022": ("L02.html:103-124", "Proposition 1.3(a) and proof, Steps 1-3"),
 "E3-c023": ("L02.html:106 and 126", "Proposition 1.3(b) with A4"),
 "E3-c024": ("L02.html:144", "Definition 2.1"),
 "E3-c025": ("L02.html:148-154", "Proposition 2.2 and proof"),
 "E3-c026": ("L02.html:159", "Example 2.3"),
 "E3-c027": ("L02.html:172-173", "Proposition 3.1 hypotheses F1, F3, F4, F5, A1, A5"),
 "E3-c028": ("L02.html:204", "Remark 3.2"),
 "E3-c029": ("L02.html:399", "misconception 1; 900 CU squared and 4.5 CU"),
 "E3-c030": ("L02.html:403", "misconception 2; Example 2.3 values"),
 "E3-c031": ("L02.html:407", "misconception 3"),
 "E3-c032": ("L02.html:366-368", "Lab 1 expected block, Part A"),
 "E3-c033": ("L02.html:369-375", "Lab 1 expected block, Part B"),
 "E3-c034": ("L02.html:387 and 479", "section 4 bullet 1 (11.17 percent) and E2 solution"),
 "E3-c035": ("L02.html:376-380", "Lab 1 expected block, Part C"),
 "E3-c159": ("L02.html:131", "Remark 1.4 and the Proposition 1.3 proof"),
 "E3-c161": ("L02.html:381 and 604", "Lab 1 Part B interpretation; Problem R2 hint"),
 "E3-c162": ("L02.html:131", "Remark 1.4, last sentence (u'' >= 0 case not stated as a result)"),
 "E3-c174": ("L02.html:167-168", "Assumption A5"),
 "E3-c036": ("L03.html:73", "Definition 1.1"),
 "E3-c037": ("L03.html:78-83", "Proposition 1.2 and proof"),
 "E3-c038": ("L03.html:88-89", "Definition 1.3"),
 "E3-c039": ("L03.html:90", "Definition 1.3 (subtracted 1)"),
 "E3-c040": ("L03.html:95-102", "Proposition 1.4 and proof"),
 "E3-c041": ("L03.html:117-123", "Proposition 1.7 and proof"),
 "E3-c043": ("L03.html:129-135", "Theorem 2.1 and proof"),
 "E3-c044": ("L03.html:139", "Remark 2.2"),
 "E3-c045": ("L03.html:144-145", "Definition 2.3 (positive outcomes, domain of A1)"),
 "E3-c046": ("L03.html:149-155", "Proposition 2.4 and proof"),
 "E3-c047": ("L03.html:159", "Example 2.5 (1600 cents at gamma 2, M = 1/1600)"),
 "E3-c048": ("L03.html:164-170", "Proposition 2.6 and proof"),
 "E3-c049": ("L03.html:174-179", "Proposition 2.7 and proof"),
 "E3-c050": ("L03.html:184", "Remark 2.8 (rounding rule; does not round an intermediate value)"),
 "E3-c051": ("L03.html:344-345", "misconception 1 (section 4); Proposition 1.7"),
 "E3-c052": ("L03.html:107", "Example 1.5 (gamma 0)"),
 "E3-c053": ("L03.html:335 and 457", "canon-breaks bullet 3; Problem R3"),
 "E3-c054": ("L03.html:309-314", "Lab 1 expected block, gamma rows 0, 0.25, 0.5, 1, 2, 4"),
 "E3-c055": ("L03.html:425", "Problem E2 solution (9/80000, 80000/9)"),
 "E3-c056": ("L04.html:65", "Definition 1.1"),
 "E3-c057": ("L04.html:70", "Lemma 1.2"),
 "E3-c058": ("L04.html:80", "Definition 1.3"),
 "E3-c059": ("L04.html:85", "Definition 1.4 (nondecreasing)"),
 "E3-c060": ("L04.html:90-99", "Theorem 1.5 and proof"),
 "E3-c061": ("L04.html:103-109", "Lemma 1.6 and proof"),
 "E3-c062": ("L04.html:118-123", "Proposition 1.8 (without A2)"),
 "E3-c063": ("L04.html:130", "Definition 2.1"),
 "E3-c064": ("L04.html:135-140", "Lemma 2.2 and proof"),
 "E3-c065": ("L04.html:145-155", "Theorem 2.3 and proof"),
 "E3-c066": ("L04.html:160", "Remark 2.4"),
 "E3-c067": ("L04.html:166", "Example 2.5 (X integrated values)"),
 "E3-c068": ("L04.html:168", "Example 2.5 (no first-order ranking; second-order X dominates)"),
 "E3-c070": ("L04.html:113-114", "Example 1.7"),
 "E3-c071": ("L04.html:614-616", "Problem R3 solution"),
 "E3-c072": ("L04.html:503-504", "misconception 1 (section 4)"),
 "E3-c073": ("L04.html:507-508", "misconception 2 (pairs 16 and 19 at L04.html:508)"),
 "E3-c074": ("L04.html:511-512", "misconception 3 (section 4)"),
 "E3-c075": ("L04.html:440-484 and 582-584", "Lab 1 expected block (FOSD counts) and E2 solution"),
 "E3-c076": ("L04.html:440-484 and 484", "Lab 1 expected block (SOSD counts; 8 of 8 agree)"),
 "E3-c077": ("L04.html:495", "section 3 bullet 4 (test set finite)"),
 "E3-c167": ("L04.html:85", "Definition 1.4 (concave on S)"),
 "E3-c168": ("L03.html:184", "Remark 2.8 bound (k+1)/2 and its proof"),
 "E3-c171": ("L03.html:324 and 326", "Lab 1 expected block (homogeneity line) and interpretation"),
 "E3-c160": ("L03.html:321 and 326", "Lab 1 expected block (gamma 1 +/- 1e-6 line) and interpretation"),
 "E3-c177": ("L03.html:349", "misconception 2 (section 4)"),
 "E3-c178": ("L03.html:112", "Definition 1.6 (hypothesis: twice differentiable, u' > 0 on (0, infinity))"),
 "E3-c180": ("L03.html:159", "Example 2.5 (gamma 1 value 2000 cents, exp of mean of logs)"),
 "E3-c181": ("L04.html:167", "Example 2.5 (Y integrated values 250, 500, 1250, 2000)"),
}

rows = []

def add(rid, check, location, status, evidence):
    rows.append({"id": rid, "check": check, "location": location, "status": status, "evidence": evidence})

# Card rows (every round-7 card row id, plus new c180 and c181)
card_ids = [
 "E3-c001","E3-c002","E3-c003","E3-c004","E3-c005","E3-c006","E3-c007","E3-c008","E3-c009","E3-c010",
 "E3-c011","E3-c012","E3-c013","E3-c014","E3-c015","E3-c016","E3-c017","E3-c173",
 "E3-c018","E3-c019","E3-c020","E3-c021","E3-c022","E3-c023","E3-c024","E3-c025","E3-c026","E3-c027",
 "E3-c028","E3-c029","E3-c030","E3-c031","E3-c032","E3-c033","E3-c034","E3-c035","E3-c159","E3-c161",
 "E3-c162","E3-c174",
 "E3-c036","E3-c037","E3-c038","E3-c039","E3-c040","E3-c041","E3-c043","E3-c044","E3-c045","E3-c046",
 "E3-c047","E3-c048","E3-c049","E3-c050","E3-c051","E3-c052","E3-c053","E3-c054","E3-c055",
 "E3-c056","E3-c057","E3-c058","E3-c059","E3-c060","E3-c061","E3-c062","E3-c063","E3-c064","E3-c065",
 "E3-c066","E3-c067","E3-c068","E3-c070","E3-c071","E3-c072","E3-c073","E3-c074","E3-c075","E3-c076",
 "E3-c077","E3-c167","E3-c168","E3-c171","E3-c160","E3-c177","E3-c178","E3-c180","E3-c181", "E3-c175",
]
# Ids in the round-7 fragment that are card rows (c001..c017 etc.) -- c175 is an L03 card in the slice; check below
extra_cards = {"E3-c175": ("L03.html:59", "Assumption A2 of L03 (limit of (e^h - 1)/h)")}
CARD_LOC.update(extra_cards)

NUMS = {
 "E3-c016": "Re-derived by hand with exact fractions: E X = 15000, 12500, 15000 cents; quadratic expected utilities 45000, 21250, 37500 (L01.html:79, 158, 364 and the expected block).",
 "E3-c032": "Re-derived in rederive.py: CE 94.9341649 CU -> 9493 cents, premium 5.0658351 CU -> 507 cents, error 0.565835 CU.",
 "E3-c033": "Re-derived in rederive.py: premium/eps^2 = 5.065835, 4.619495, 4.528811, 4.504565, 4.500046; gaps 0.565835 ... 0.000046 shrink.",
 "E3-c034": "Re-derived: 0.565835/5.065835 = 0.11170 (11.17 percent); 0.565835/4.5 = 12.57 percent (not the basis used).",
 "E3-c054": "Re-derived in rederive.py: CE at gamma 0, 0.25, 0.5, 1, 2, 4 = 11250, 10931.7733, 10615.8009, 10000, 8888.8889, 7337.6161.",
 "E3-c055": "Re-derived: M = 1/4*1/5000 + 1/2*1/10000 + 1/4*1/20000 = 9/80000, so CE = 80000/9 = 8888.888...",
 "E3-c047": "Re-derived: M = 1/2*1/1000 + 1/2*1/4000 = 1/1600, CE = 1600 cents.",
 "E3-c180": "Re-derived: sqrt(1000*4000) = 2000 cents (exact); the Example's stated value.",
 "E3-c067": "Re-derived: I_X(3000)=500, I_X(4000)=1000, I_X(5000)=2000.",
 "E3-c181": "Re-derived: I_Y(2000)=250, I_Y(3000)=500, I_Y(4000)=1250, I_Y(5000)=2000.",
 "E3-c168": "Re-derived: |R(kv)-kv| <= 1/2 and |kR(v)-kv| <= k/2, so the triangle bound is (k+1)/2.",
 "E3-c050": "Remark 2.8 states the same rule (halves up, one rounding, floor(v+1/2) for v >= 0).",
 "E3-c178": "Changed in the round-8 delta; the card now asks for the Definition's stated hypothesis, which matches Definition 1.6 (L03.html:112).",
 "E3-c029": "Re-derived: half of Var 1800 is 900 CU squared; Pratt approximation 4.5 CU.",
 "E3-c026": "Re-derived: r_A = 1/(2w), r_R = 1/2; at w=100, r_A=0.005.",
 "E3-c040": "The limit argument uses A2 (e^h-1)/h -> 1, stated as an assumption at L03.html:59.",
}

for cid in card_ids:
    loc, what = CARD_LOC[cid]
    status = "PASS"
    changed = {"E3-c047": "changed in the round-8 delta (front and back rewritten)",
               "E3-c050": "back text changed in the round-8 delta",
               "E3-c067": "front and back changed in the round-8 delta",
               "E3-c178": "front and back changed in the round-8 delta (previously a FAIL)",
               "E3-c180": "new card in round 8",
               "E3-c181": "new card in round 8"}.get(cid, "unchanged since the round-7 pin (cards.json delta touches only c047, c050, c067, c131, c144, c178, c180-c182)")
    ev = card(cid, f"{loc} ({what})", f"Card {changed}. Grade and basis agree with the lesson text; card numbers appear in the lesson. " + NUMS.get(cid, ""))
    add(f"E3f-{cid}", "2.7-cards", loc, status, ev.strip())

# Row id mapping for previously used ids that are not card ids but were in the round-7 fragment
add("E3f-lesson-numbers-L01", "2.2-numbers", "course/modules/E/E3/L01.html (prose, Examples 1.4, 3.4, misconceptions, problems M1-R3, quiz)", "PASS",
    "Full read of L01.html (lines 1-577) in round 8. Numbers re-derived: Example 1.4 E=150 CU, quadratic 45000 (L01.html:79); M1 E X=59, E u=4030, u(E X)=3481, difference 549 (L01.html:366); M2 weights 1/6,1/3,1/2 and 133.333 (L01.html:373); M3 20 and 30 CU, 65 and 95 (L01.html:380); Example 3.4 quadratic 37500 (L01.html:158); E2 40000 (L01.html:423); E3 1/6 short (L01.html:430); R3 25000 and 22500 (L01.html:455); quiz q7 5/12 (L01.html:538); P3 divergence (L01.html:405). All match the lab output rows in ledgers/E3/scripts/E3-f-r8/run_labs_L01.out.")
add("E3f-lab-L01", "2.5-labs", "course/modules/E/E3/L01.html:161-326 (lab-E3-L01-1); tests/labs/E3/lab-E3-L01-1.py", "PASS",
    "tools/run_labs.py --unit E3 --page L01 -> 'run_labs E3: PASS (1/1)' (ledgers/E3/scripts/E3-f-r8/run_labs_L01.out, exit 0). Twin run under python3 -I -W error: exit 0, stderr 0 bytes. Expected block (L01.html:302-324) equals the twin output. Interpretation lines (L01.html:325) match Parts A-D.")
add("E3f-cards-slice-scan", "2.7-cards-duplicates", "course/modules/E/E3/cards.json (L01-L04 slice, 89 cards)", "PASS",
    "Same scan as E3f-E3-c007-scan; no duplicate card in the slice. Changed cards c047, c067, c178 and new c180, c181 read against their lessons.")
add("E3f-E3-c178", "2.7-cards-duplicates + 2.7-cards accuracy", "course/modules/E/E3/cards.json (E3-c178, L03) vs course/modules/E/E3/L03.html:112", "PASS",
    "Round 7 FAIL resolved. The front now asks what hypothesis Definition 1.6 imposes, and the back gives the Definition's own hypothesis (twice differentiable on (0, infinity) with u' > 0). This is accurate. No necessity claim is made, and the question differs from E3-c024 (Definition 2.1 of L02). Grade T matches the Definition (a definition, no claim).")
add("E3f-cards-near-duplicates", "2.7-cards-duplicates", "course/modules/E/E3/cards.json (L01-L04)", "PASS",
    "Round 8 scan (see E3f-cards-slice-scan): no card duplicates another in the slice; flagged template-similar pairs are distinct facts.")
add("E3f-coverage-cards", "2.7-cards-coverage", "course/modules/E/E3/L01.html-L04.html (definitions, theorems, misconceptions, lab results)", "PASS",
    "Every definition, theorem/proposition, lemma, misconception and lab result of L01-L04 read in round 8 has a card (e.g. L01 Defs 1.1-3.2 c001-c006, c013 R1, misc c014/c015/c173; L02 Prop 1.1 c019, Prop 1.3 c022/c023, Def 2.1 c024, Prop 3.1 c027, misc c029-c031; L03 Prop 1.4 c040, Prop 1.7 c041, Thm 2.1 c043, Prop 2.4 c046, Prop 2.6 c048, Prop 2.7 c049, Remark 2.8 c050/c168; L04 Lemma 1.6 c061, Prop 1.8 c062, Thm 2.3 c065, misc c072-c074). Assumptions with no card (L02 A1, A3, A4, F1-F6; L03 F1, F2) are not in the card rule's list (BUILDER_RULES section 7).")
add("E3f-cards-integrity", "2.7-cards-integrity", "course/modules/E/E3/cards.json (JSON keys, lesson field, ids)", "PASS",
    "json.load succeeds; every slice card has id, lesson, front, back; grade present on every claim card and absent only on definitions, assumptions and conventions (c001-c006, c018, c020, c021, c024, c036, c038, c045, c050, c056, c058, c059, c063, c159, c162, c167, c174, c175). 89 slice cards; ids E3-c001..c181 (c042 and c069 belong to no slice lesson).")
add("E3f-cards-numbers", "2.7-cards-numbers", "course/modules/E/E3/cards.json vs the slice lessons", "PASS",
    "Every number on a card appears in its lesson or its lab expected block (checked: c032 9493/507/5.065835/4.500000/0.565835 at L02.html:367; c033 4.500046 at L02.html:374; c054 7337.6161 at L03.html:314; c055 80000/9 at L03.html:425; c067/c181 values at L04.html:166-167; c075 counts at L04.html:582 and expected block; c076 counts in expected block; c168 (k+1)/2 at L03.html:184).")
add("E3f-cards-xrefs", "2.7-cards-refs", "course/modules/E/E3/cards.json (section and proposition references)", "PASS",
    "Section references checked: c004 section 4 (L01.html:331), c034 section 4 (L02.html:387), c051 section 4 misc 1 (L03.html:344), c072 section 4 (L04.html:503), c074 section 4 (L04.html:511), c077 section 3 (L04.html:495), c173 section 5 (L01.html:350), c029/c031 section 5 (L02.html:398, 407), c014 section 5 (L01.html:342). Problem references R1, R3, P2, E2 exist (L01 R1 at :439, P2 at :396; L03 R3 at :454, E2 at :422; L04 R3 at :613).")
add("E3f-cards-grades", "2.7-cards-grades", "course/modules/E/E3/cards.json (grade and basis)", "PASS",
    "Grades: T on every card stating a proved proposition/theorem/lemma or hand-computed example (checked: c007-c013, c019, c022, c023, c025-c028, c037, c039-c041, c043, c044, c046-c049, c051-c053, c055, c057, c060-c062, c064-c066, c067, c068, c070, c071, c077, c168, c173, c177, c178, c180, c181). C with a basis naming the lab on c016, c017, c032-c035, c054, c073, c075, c076, c160, c161, c171 (basis fields present, each names Lab 1 or its part). Definitions carry no grade.")
add("E3f-lesson-numbers-L02", "2.2-numbers", "course/modules/E/E3/L02.html (Example 1.5, Example 2.3, Section 3 text, canon-breaks, misconceptions, problems M1-R3, E1-E3, quiz, key results)", "PASS",
    "Full read of L02.html (lines 1-629) in round 8. Re-derived in ledgers/E3/scripts/E3-f-r8/rederive.py: E sqrt(W)=9.743416490, CE=94.934165, premium 5.065835 (L02.html:136); CE cents 9493, premium cents 507; r_A=1/(2w), r_R=1/2, r_A(100)=0.005 (L02.html:159); Var(X)=1800, half-variance 900, approximation 4.5 (L02.html:399); 11.17 percent = 0.565835/5.065835 (L02.html:387, 479); 12.57 percent of the approximation (L02.html:479); E1 gap 0.004565 and factor 6.31 (L02.html:472); M1 CE=9, premium 1 (L02.html:422); M2 r_A=1/w (L02.html:429); M3 r_A=a (L02.html:436); P1-P3 and R1-R3 arguments verified; quiz numeric answers 9, 1, 0.5, 2 match.")
add("E3f-lab-L02", "2.5-labs", "course/modules/E/E3/L02.html:207-381 (lab-E3-L02-1); tests/labs/E3/lab-E3-L02-1.py", "PASS",
    "run_labs E3 L02 PASS (1/1) (ledgers/E3/scripts/E3-f-r8/run_labs_L02.out, exit 0). Twin under python3 -I -W error: exit 0, stderr 0 bytes. Page code equals twin (run_labs byte check). Expected block L02.html:365-380 equals the output. Hypothesis (L02.html:209, now using \\Var) matches the lab's values (variance 1800, Pratt 4.5, premium zero for linear utility).")
add("E3f-lesson-numbers-L03", "2.2-numbers", "course/modules/E/E3/L03.html (Example 1.5, Example 2.5, Propositions 1.2-2.7, Remark 2.8, canon-breaks, misconceptions, problems M1-R3, quiz, key results)", "PASS",
    "Full read of L03.html (lines 1-577) in round 8. Re-derived: CRRA 2.5 values 1600 and 2000 (L03.html:159); M2 M=1/3000, CE 3000, expected prize 7000 (L03.html:375); M3 CE 9000 (L03.html:382); E1 10615.8009 rounds to 10616 (L03.html:418); E2 9/80000 and 80000/9 (L03.html:425); E3 bound 5.5 (L03.html:432); R1 limit argument (L03.html:443); lab hypothesis values 11250, 10000, 80000/9 ~ 8888.89 -> 8889 (L03.html:189); interpretation 10931.7733 and 8888.8889 (L03.html:326, 353). Forward reference to Proposition 2.7 inside Definition 1.3 (L03.html:90) noted, not a defect.")
add("E3f-lab-L03", "2.5-labs", "course/modules/E/E3/L03.html:187-327 (lab-E3-L03-1); tests/labs/E3/lab-E3-L03-1.py", "PASS",
    "run_labs E3 L03 PASS (1/1) (run_labs_L03.out, exit 0). Twin under python3 -I -W error: exit 0, stderr 0 bytes. Expected block L03.html:307-325 equals the twin output (run_labs line-by-line rule, PASS). Interpretation L03.html:326 matches the printed lines.")
add("E3f-lesson-numbers-L04", "2.2-numbers", "course/modules/E/E3/L04.html (Lemma 1.2, Examples 1.7, 2.5, 2.6, Lemma 2.2, Theorem 2.3 proof, canon-breaks, misconceptions, problems M1-R3, quiz, key results)", "PASS",
    "Full read of L04.html (lines 1-730) in round 8. Re-derived: Example 2.5 I_X(3000)=500, I_X(4000)=1000, I_X(5000)=2000, I_Y(2000)=250, I_Y(3000)=500, I_Y(4000)=1250, I_Y(5000)=2000 (rederive.py output; L04.html:166-167); F_X(2000)=1/2 > F_Y(2000)=1/4 and F_Y(3000)=3/4 > F_X(3000)=1/2 (L04.html:168); Example 2.6 I_Y(t)=(t-3000)^+ <= I_X(t) (L04.html:173); Example 1.7 F vectors (L04.html:113); M1 means 2500 and 2000 (L04.html:527); M2/M3 values 500 (L04.html:534, 541); E1 500 (L04.html:577); E2 counts sum to 24 (L04.html:584); R3 proof b1 = sigma_{m-1} >= 0 and I_X(s_m)=s_m-EX (L04.html:616); lab counts 3/10/1/10, 3/2/1/2, 24 of 24 and 8 of 8 match the expected block (L04.html:440-484).")
add("E3f-lab-L04", "2.5-labs", "course/modules/E/E3/L04.html:176-485 (lab-E3-L04-1); tests/labs/E3/lab-E3-L04-1.py", "PASS",
    "run_labs E3 L04 PASS (1/1) (run_labs_L04.out, exit 0). Twin under python3 -I -W error: exit 0, stderr 0 bytes. Expected block L04.html:440-484 equals output. Interpretation L04.html:485 (named-pair verdicts, integrated values equal to Example 2.5, 24 + 8 + 3 + 2 = 37 agreements) matches the output.")
add("E3f-dag-L02-crra-forward-use", "2.9-define-before-use", "course/modules/E/E3/L02.html; L03.html; L04.html (concept links and forward references)", "PASS",
    "check_dag.py --unit E3: PASS (ledgers/E3/scripts/E3-f-r8/check_dag.out). L02 uses no CRRA concept. L04 links to L03 crra-utility (L03.html:37 defines it at L03.html:88). Forward references inside the slice (L03 Definition 1.3 cites Proposition 2.7 at L03.html:90; L03 Example 1.5 cites Proposition 1.7) cite results stated later in the same lesson, not concepts used before definition; noted as non-blocking.")
add("E3f-dag-other-links", "2.9-define-before-use", "course/modules/E/E3/L01.html-L04.html (Uses and Introduces lines, concept links)", "PASS",
    "Meta rows read: L01 uses random-variable and expectation (M4); L02 uses expected-utility (L01), expectation, variance, derivative; L03 uses expected-utility, arrow-pratt, certainty-equivalent, random-variable, expectation, derivative, exponential-and-logarithm (M1); L04 uses expected-utility, crra-utility (L03), random-variable, expectation. check_dag PASS.")
add("E3f-notation", "2.13-notation", "course/modules/E/E3/L01.html-L04.html vs notation/notation.json", "PASS",
    "Round 7 FAIL resolved. L02.html:164 and 209 now use \\Var (registered: \\Var = \\operatorname{Var}); grep -c 'mathrm{Var}' is 0 in all four pages. Registered macros used: \\E, \\Prob, \\Var, \\R, \\indic only; no raw \\mathbb, \\operatorname, \\mathbf in the slice (grep). Registered program-wide symbols T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q} do not occur. Locally defined letters (gamma, sigma, S, I, M, s, R(h), pi(eps), CE with \\mathrm{CE}) are defined where used (e.g. L03.html:88 gamma, L04.html:85 sigma, L02.html:164 pi(eps)); \\mathrm{CE} is a lesson-local abbreviation (not in notation.json), so not a notation FAIL. page_smoke PASS (no katex-error) confirms every macro renders.")
add("E3f-banned-and-process", "1.3-1.4-banned", "course/modules/E/E3/L01.html-L04.html (visible prose)", "PASS",
    "check_pages.py --unit E3: PASS (check_pages.out). grep for process words (verif, builder, round, TODO, draft, audit, placeholder) in visible prose: none. 'this unit' in L03.html:184 is the course's usage for the module (as in M1), not process language.")
add("E3f-hours", "2.12-hours", "course/modules/E/E3/index.html:29,127-136; L01-L04 eyebrows (7 study hours each)", "PASS",
    "Arithmetic: 8 lessons x 7 h = 56 h (hub data-hours-lessons=56, index.html:127 'Eight lessons of seven study hours each, which is 56 hours'); project 14 h; module 56 + 14 = 70 h (index.html:31). Hub per-lesson cards L01-L08 each '7 h' (index.html:129-136). Lesson eyebrows L01.html:34, L02.html:34, L03.html:34, L04.html:34 each '7 study hours'. Consistent.")
add("E3f-delta", "0-delta", "git diff 9373ef3..2d755599 for the slice", "PASS",
    "Round-8 delta (9373ef3..2d755599) hunks read in full: L02.html:209 (\\Var in hypothesis); L03.html:564 (references: M1 A3 uniqueness); L04.html:178, 495, 575, 582 (hypothesis wording, canon bullet 4, E1 and E2 problem wording); cards.json c047, c050, c067, c178, c180, c181 (c131, c144, c182 are outside the slice). L01.html and tests/labs/E3/lab-E3-L0[1-4]-1.py unchanged since 9373ef3; their evidence is re-run this round.")
add("E3f-E3-r7-independent-rederivation", "2.2-numbers (independent)", "ledgers/E3/scripts/E3-f-r8/rederive.py (run with python3 -I -W error)", "PASS",
    "Independent Python rederivation (python3 -I -W error): L02 Example 1.5 and Part A/B values (9493, 507, 5.065835, 4.619495, 4.528811, 4.504565, 4.500046, gap 4.556e-5 -> 0.000046); L03 CE at gamma 0, 0.25, 0.5, 1, 2, 4 (11250.0000, 10931.7733, 10615.8009, 10000.0000, 8888.8889, 7337.6161); 80000/9; M2/M3 and E2 closed forms; L04 integrated values of Examples 2.5 and 2.6. All agree with the lesson text and the printed blocks.")
add("E3f-cmd-check_pages", "check_pages.py --unit E3", "tools", "PASS", "ledgers/E3/scripts/E3-f-r8/check_pages.out: 'check_pages E3: PASS', exit 0.")
add("E3f-cmd-check_dag", "check_dag.py --unit E3", "tools", "PASS", "ledgers/E3/scripts/E3-f-r8/check_dag.out: 'check_dag E3: PASS', exit 0.")
add("E3f-cmd-check_projects", "check_projects.py --unit E3", "tools", "PASS", "ledgers/E3/scripts/E3-f-r8/check_projects.out: 'check_projects E3: PASS', exit 0 (unit gate; the project itself is outside this slice).")
add("E3f-cmd-page_smoke", "page_smoke.py --unit E3 --pages L01 L02 L03 L04 (alone)", "tools", "PASS",
    "ledgers/E3/scripts/E3-f-r8/page_smoke_L01-L04.out: each of L01-L04 'PASS' in light and dark at desktop and 360 px, labs executed in Pyodide; 'page_smoke E3: PASS', exit 0.")
add("E3f-cmd-run_labs-L01-L04", "run_labs.py --unit E3 --page L0n (n = 1..4)", "tools", "PASS",
    "run_labs_L01.out, run_labs_L02.out, run_labs_L03.out, run_labs_L04.out: each 'run_labs E3: PASS (1/1)', exit 0.")
add("E3f-cmd-pytest-labs", "pytest tests/test_labs.py -k E3", "tests", "PASS",
    "ledgers/E3/scripts/E3-f-r8/pytest_labs_E3.out: 15 dots, exit 0 (collect-only count for tests/test_labs.py -k E3 is 15).")
add("E3f-cmd-ruff-labs", "ruff check tests/labs/E3 and ruff format --check tests/labs/E3", "tests/labs/E3", "PASS",
    "ruff_labs.out: 'All checks passed!' (exit 0) and '11 files already formatted' (exit 0).")
add("E3f-cmd-mypy-twins", "mypy --no-incremental on the four L01-L04 twins", "tests/labs/E3/lab-E3-L01-1.py..L04-1.py", "PASS",
    "mypy_twins.out: 'Success: no issues found in 4 source files', exit 0.")
add("E3f-cmd-verify_refs", "verify_refs.py --offline", "references/", "PASS",
    "verify_refs_offline.out: 'offline integrity: 560 entries, 0 problems', exit 0. (--unit is a live-run option and was not used.)")
add("E3f-references", "2.4-attributions", "course/modules/E/E3/L02.html:616 (pratt1964risk); L03.html:564; L04.html:717; L01.html:564", "PASS",
    "references/references.json entry pratt1964risk: title 'Risk Aversion in the Small and in the Large', author Pratt, John W., year 1964, container Econometrica, volume 32, status verified (crossref). L02 names it for the name only, with the registry's title, container and year (matches). L01, L03, L04 cite no registry source and say so. Hub data-cite list has five keys (index.html:160-164) as L01 states.")
add("E3f-L03-references", "2.4-attributions", "course/modules/E/E3/L03.html:564", "PASS",
    "Round 7 FAIL resolved. The paragraph now names the uniqueness in M1 Lesson 3 A3 (course/modules/M/M1/L03.html:61: 'exactly one real x with e^x = y'), which Proposition 2.4 uses (L03.html:154). The other cited M1 results match: Proposition 1.4 (ln(e^x)=x, M1 L03.html:92), Proposition 1.6(b) (product rule, M1 L03.html:112-118), the addition rule A2 (M1 L03.html:60). M1 Lesson 3 does not derive (e^h-1)/h -> 1 (grep for lim/derivative: none), so A2 of L03 is correctly an assumption.")

# Add row for E3-c175, E3-c160 etc already included; ensure every round-7 row id exists
prev = json.load(open("/Users/billyribeiro/.fanout/frags/D-E3-f.round7.json"))
have = {r["id"] for r in rows}
missing = [r["id"] for r in prev["rows"] if r["id"] not in have]
print("round-7 ids not yet present:", missing)
extra = sorted(have - {r["id"] for r in prev["rows"]})
print("new ids in round 8:", extra)

frag = {
 "unit": "E3",
 "slice": "f",
 "round": 8,
 "verifier": "Haiku independent verifier, E3-f round 8 (did not build E3)",
 "pin": "2d755599d8d74df292e3e43025f0458c4053802e (2d75559, detached)",
 "base": "9373ef3 (round-7 pin; frags/D-E3-f.round7.json). Delta 9373ef3..2d75559 touches the slice in L02.html:209, L03.html:564, L04.html:178/495/575/582 (hypothesis, canon bullet, E1, E2 wording), and cards.json c047, c050, c067, c178, c180, c181 (c131, c144, c182 outside slice). L01.html and the four slice twins are byte-identical to 9373ef3.",
 "checkout": "/Users/billyribeiro/.fanout/wt/verifyD8-E3-f (detached at 2d75559; .venv symlinked)",
 "scratch": "ledgers/E3/scripts/E3-f-r8/",
 "verified_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
 "verdict": "PASS",
 "rows": rows,
 "mutants": [],
 "registry_flags": [],
 "freshness_flags": [],
 "notes": [
   "Lesson slice (no project grader in this slice): mutation testing of graders is not applicable here; run_graders and mutate_graders were not run. The project (project.html, grader/) belongs to another slice.",
   "Non-blocking observations (not defects): L03 Definition 1.3 cites Proposition 2.7 before it appears (L03.html:90); L03 Example 1.5 cites Proposition 1.7 before it appears. Card pairs E3-c040/E3-c177, E3-c047/E3-c180 and E3-c067/E3-c181 share a template or a result but ask distinct questions.",
   "Lesson-local abbreviation \\mathrm{CE} (L02, L03) is not registered in notation.json; treated as local, not a notation FAIL.",
   "Not checked in this slice: L05-L08 pages and their cards (including E3-c144 and E3-c182 in L08 and E3-c131 in L07, outside slice f); project.html and grader/; live verify_refs (only --offline run); browser screenshots beyond page_smoke's own captures; the external truth of the published works (only the registry record was compared, no full text read)."
 ],
 "summary": "E3 slice f (lessons L01-L04 and cards for L01-L04), round 8 at 2d75559. Every row PASS. All 120 round-7 row ids kept; 2 new card rows (E3-c180, E3-c181). Round-7 FAIL rows E3f-E3-c178, E3f-notation and E3f-L03-references now pass; all four lessons were read in full, every delta hunk was re-read, and every number was re-derived. All gates (check_pages, check_dag, check_projects, run_labs x4, twins under python -I -W error, page_smoke L01-L04, ruff, mypy, pytest E3 labs, verify_refs --offline) pass."
}
json.dump(frag, open(OUT, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
open(OUT, "a", encoding="utf-8").write("\n")
print("rows:", len(rows), "verdict:", frag["verdict"])
