# Round-5 fragment builder for FC2 slice b. Fresh rows carry round-5 evidence; PASS rows whose subject is byte-identical
# since the previous pin are carried from the round-4 fragment with the required prefix.
import json, re
ROOT = "/Users/billyribeiro/.fanout/wt/verifyS5-FC2-b"
PREV = "/Users/billyribeiro/.fanout/frags/S-FC2-b.round4.json"
prev = json.load(open(PREV, encoding="utf-8"))
prev_rows = {r["id"]: r for r in prev["rows"]}
PFX = ("Carried from round 4 (course/modules/FC/FC2/L05.html, tests/labs/FC2/lab-FC2-L05-1.py byte-identical since the "
       "previous pin edbb7aa8; re-read in full this round): ")
CARRY = [
    "FC2b-lab-L05-twin", "FC2b-lab-L05-hypothesis", "FC2b-lab-L05-D-claim", "FC2b-lab-L05-named-errors",
    "FC2b-math-L05-thm1.2", "FC2b-math-L05-remark1.3-hypotheses", "FC2b-math-L05-thm2.2",
    "FC2b-math-L05-thm3.2-cor3.4", "FC2b-math-L05-thm4.1-remark4.2", "FC2b-math-L05-problems",
    "FC2b-math-L05-why-it-matters-rate", "FC2b-num-L05", "FC2b-struct-L05", "FC2b-misconception-L05-1",
]
rows = []
def R(id_, check, location, status, evidence, fix=None):
    r = {"id": id_, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    rows.append(r)
S = "ledgers/FC2/scripts/FC2-b-r5/"
# ---- commands (run this round on the pin)
R("FC2b-cmd-check_pages", "gate", "index, L01-L08, cards.json (unit gate)", "PASS",
  f"tools/check_pages.py --unit FC2 -> 'check_pages FC2: PASS', exit 0 ({S}check_pages.txt; gate_exit_codes.txt).")
R("FC2b-cmd-check_dag", "gate", "L04-L06 links and dfn", "PASS",
  f"tools/check_dag.py --unit FC2 -> 'check_dag FC2: PASS', exit 0 ({S}check_dag.txt).")
R("FC2b-cmd-check_projects", "gate", "project.html (unit gate, outside slice)", "PASS",
  f"tools/check_projects.py --unit FC2 -> 'check_projects FC2: PASS', exit 0 ({S}check_projects.txt).")
R("FC2b-cmd-run_graders", "gate", "grader/ (unit gate, outside slice)", "PASS",
  f"tools/run_graders.py --unit FC2 --seeds 0-49 -> 'run_graders FC2: PASS (reference 50/50 seeds, slowest 0.5 s)', exit 0 ({S}run_graders_fc2.txt).")
R("FC2b-cmd-run_labs", "gate", "tests/labs/FC2 (unit, and L04, L05, L06 separately)", "PASS",
  f"tools/run_labs.py --unit FC2 exit 0 ({S}run_labs_unit.txt); --page L04, L05, L06 each 'run_labs FC2: PASS (1/1)' ({S}run_labs_L04.txt, run_labs_L05.txt, run_labs_L06.txt).")
R("FC2b-cmd-page_smoke", "gate", "L04.html, L05.html, L06.html (each run alone)", "PASS",
  f"tools/page_smoke.py --unit FC2 --pages L04, then L05, then L06, each 'page_smoke FC2: PASS' ({S}page_smoke_L04.txt, page_smoke_L05.txt, page_smoke_L06.txt).")
R("FC2b-cmd-twins-isolated", "gate", "tests/labs/FC2/lab-FC2-L04-1.py, lab-FC2-L05-1.py, lab-FC2-L06-1.py", "PASS",
  f"python -I -W error on each twin, run alone: exit 0 each ({S}twin_L04_isolated.txt, twin_L05_isolated.txt, twin_L06_isolated.txt).")
R("FC2b-cmd-ruff", "gate", "tests/labs/FC2 twins", "PASS",
  f"ruff check tests/labs/FC2 -> 'All checks passed!'; ruff format --check -> '11 files already formatted' ({S}ruff_check.txt, ruff_format.txt).")
R("FC2b-cmd-mypy", "gate", "repository mypy configuration", "PASS",
  f"mypy --no-incremental -> 'Success: no issues found in 385 source files' ({S}mypy.txt).")
R("FC2b-cmd-pytest", "gate", "tests/test_labs.py -k FC2; tests/test_page_checks.py; tests/test_run_labs.py", "PASS",
  f"pytest tests/test_labs.py -k FC2 -q exit 0, 11 dots ({S}pytest_fc2.txt); pytest tests/test_page_checks.py tests/test_run_labs.py -q exit 0, 47 dots ({S}pytest_page_checks.txt).")
R("FC2b-cmd-verify_refs", "gate", "references/references.json; L04-L06 carry no data-cite", "PASS",
  f"tools/verify_refs.py --offline -> 'offline integrity: 560 entries, 0 problems', exit 0 ({S}verify_refs_offline.txt). The live run is not made; no L04-L06 page cites a key.")
# ---- labs
R("FC2b-lab-L04-twin", "lab", "L04.html:123-244; tests/labs/FC2/lab-FC2-L04-1.py", "PASS",
  f"{S}twin_vs_page_v5.out: page data-run block == twin file (True); expected block (L04.html:220-242, 23 lines) == twin stdout under python -I -W error (True).")
R("FC2b-lab-L06-twin", "lab", "L06.html:165-318; tests/labs/FC2/lab-FC2-L06-1.py", "PASS",
  f"{S}twin_vs_page_v5.out: page data-run block == twin file (True); expected block (L06.html:294-316, 23 lines) == twin stdout (True). Twin docstring (lines 1-12) edited this delta; the code body is unchanged.")
R("FC2b-lab-L04-hypothesis", "lab", "L04.html:125 vs expected block L04.html:220-242", "PASS",
  "Edited hypothesis (L04.html:125): 'zero at each grid spot up to 100 USD and equals the spot minus 100 USD at each grid spot above it'. "
  "Printed call payoffs (L04.html:222-230) are 0.00 at 0..100 and 25.00, 50.00, 75.00, 100.00 at 125..200, i.e. spot minus 100 above 100. "
  "Put payoff 100, 75, 50, 25, 0 at 0..100 and 0 above; put break-even 93.00 (L04.html:232); call break-even 108.00 (L04.html:231); "
  "path best call date 1 (L04.html:240), best put date 3 (L04.html:241), call held 6.56 (L04.html:242). Twin docstring: no random numbers (twin line 12; page L04.html:137). "
  "Grid and premiums read from tests/labs/FC2/lab-FC2-L04-1.py lines 15-24.")
R("FC2b-lab-L06-hypothesis", "lab", "L06.html:167 vs expected block L06.html:294-316", "PASS",
  "Hypothesis: one-period price 30 (3000 cents) = discounted expectation (L06.html:299-300); two-period 45 (4500 cents) = closed form (306-307); "
  "one-period check True (301); four path checks True (312-315); self-financing True (316). All match.")
R("FC2b-lab-L06-docstring", "lab", "tests/labs/FC2/lab-FC2-L06-1.py:1-12 (shown on L06.html:170-178); printed lines L06.html:297-309", "PASS",
  "Round-4 FAIL resolved. The docstring now says stock prices, payoffs and values after one move are printed in currency units, "
  "shares and bond positions as exact Fractions, and only time-0 values also in integer cents (V0 one period, one-period discounted expectation, two-period V0). "
  "Output: cents appear only on time-0 lines L06.html:299, 300, 306, 307; after-move and expiry values print without cents (297, 303-305, 309); "
  "positions print as Fractions (298, 308, 310, 311). Matches the code (round-up half rule, Fraction types).")
R("FC2b-lab-L06-hypothesis-note", "lab", "L06.html:167", "PASS", "placeholder")
rows.pop()
# ---- math (L04 and L06 changed this delta; L05 carried below)
R("FC2b-math-L04-s1-s2", "math", "L04.html:57-112 (A1-A5, Def 1.1, Lemma 1.2, Def 2.1, Prop 2.2, Prop 2.3, Remark 2.4)", "PASS",
  "Re-read in full. Lemma 1.2 cases (L04.html:80) re-derived. Prop 2.2 (L04.html:99) and Prop 2.3 (L04.html:107) proofs re-derived: A3 excludes the zero-cost, non-negative-payoff position, and A5 is used in Prop 2.3. "
  "Remark 2.4 (L04.html:111) statement about the inequality is right; its sentence about Theorem 4.1 is a separate defect (row FC2b-plan-L04-no-L05-result), not a math error.")
R("FC2b-math-L04-example-2.5", "math", "L04.html:115-121 (Example 2.5, Remark 2.6)", "PASS",
  f"{S}numbers_v5.out: ln(10/9)=0.105361; 10(9/10)^4=6.561; 20(9/10)=18; 20(9/10)^3=14.58; intrinsic call 0,20,0,0,10; put 0,0,10,20,0. Remark 2.6 cites Prop 2.2 correctly.")
R("FC2b-math-L04-problems", "math", "L04.html:281-377 (M1-M3, P1-P3, E1-E3, R1-R3)", "PASS",
  f"Re-derived: M1 payoff 12, profit 8, break-even 54; M2 break-even 77, profit 17; E2 put PV 10(9/10)^4=6.56, call best date 1 (18.00), put best date 3 (14.58) ({S}numbers_v5.out); E3 10(9/10)^2=8.10 vs 0; R1 S=100+20000/729=127.43484 ({S}numbers_v5.out); R3 path 100,90,95,110,150: exercise at 3 gives 7.29, hold gives 32.805. P1-P3 proofs re-checked.")
R("FC2b-math-L06-thm1.4", "math", "L06.html:76-90 (Def 1.3, Theorem 1.4 (a)-(c), proof); Example 1.5 L06.html:92-95; Example 1.6 L06.html:97-100", "PASS",
  f"Theorem 1.4 (a) uniqueness (u != d, S0 > 0), (b) V0 formula and 0<q<1 (R_f > d, u > R_f), (c) arbitrage with surplus (pi-V0)R_f re-derived. Example 1.5: Delta=1/2, B=-20, V0=30, q=3/4, 3000 cents ({S}numbers_v5.out: q=3/4). Example 1.6: cash 35-50+20=5, lent to 25/4; shares and loan give 50 (up) and 0 (down); with the sold call the total is 25/4 in both states (re-derived by hand).")
R("FC2b-math-L06-thm2.2-thm3.3", "math", "L06.html:116-158 (Theorem 2.2; Definitions 3.1-3.2; Theorem 3.3 and closed-form induction; Example 3.4)", "PASS",
  f"Theorem 2.2 proof (L06.html:121) re-derived. Theorem 3.3 closed-form induction (L06.html:148-152): Pascal step and R_f^(-1) R_f^(-m) re-checked. Example 3.4 (L06.html:157): S=225,75,25; payoffs 125,0,0; V(1,1)=75; V(1,0)=0; V(0,0)=45; closed form (16/25)(9/16)125=45 ({S}numbers_v5.out).")
R("FC2b-math-L06-examples", "math", "L06.html:93-99 (Ex 1.5, 1.6), 155-158 (Ex 3.4)", "PASS",
  "Example 1.5 numbers as in FC2b-math-L06-thm1.4; Example 1.6 quoted values (cash 5, lent 25/4, shares and loan 50 up and 0 down) re-derived; Example 3.4 values as above.")
R("FC2b-math-L06-remarks-misconceptions", "math", "L06.html:101-105 (Remark 1.7), 114 (Remark on q), 327-336 (misconceptions)", "PASS",
  f"Remark 1.7 consistent with Theorem 1.4 (b). Remark at L06.html:114: E^Q[S1]=q u S0+(1-q) d S0 equals R_f S0 exactly when q=(R_f-d)/(u-d): identity, re-derived. Misconception 3 (L06.html:335): E[S(2,.)]=156.25 (625/4), discounted 100, payoff at 156.25 is 56.25, discounted 36, correct 45, expected payoff 70.3125=1125/16 ({S}numbers_v5.out). Misconception 1 (L06.html:331) and 2 (L06.html:333) correct.")
R("FC2b-plan-L06-A2", "math", "L06.html:55 (A2) vs plans/FC2-build-plan.md section 5.2 A2 (plan lines 287-288)", "PASS",
  "Round-5 change: L06.html:55 adds 'no bid-ask spread', matching plan A2 ('no transaction costs, no bid-ask spread, no short-sale constraint, and unlimited borrowing and lending'). A6 at L06.html:55 refers to Definition 1.2 of this lesson, which states 0<d<R_f<u (L06.html:64).")
# ---- the defect rows (fresh)
R("FC2b-plan-L04-no-L05-result", "structure / architect decision", "L04.html:51, 111, 120, 243, 248, 258, 262", "FAIL",
  "Plan lines 105 ('the theorem waits for L05') and 431-432 ('the result that early exercise of a non-dividend call is never optimal is proved in L05 ... not stated in L04') bind the content. "
  "L04 states the Theorem 4.1 result: L04.html:51 ('Lesson 5 ... shows that an American call on a stock with no income, at a non-negative rate, has the same value as the European call at date 0'); "
  "L04.html:111 (Remark 2.4, 'Lesson 5 proves equality at date 0 for a call on an underlying with no income and a non-negative rate'); L04.html:120; L04.html:243 (Lab 1 interpretation); L04.html:248 (canon breaks); "
  "L04.html:258 (misconception 1, 'Lesson 5 (Theorem 4.1) proves equality ... so the date-0 early-exercise premium ... is zero'); L04.html:262 (misconception 2). "
  "Each statement also omits hypothesis (N) of Theorem 4.1 (L05.html:301) and cites a result whose hypotheses L04 does not define. Not caught in round 4.",
  "Remove the Theorem 4.1 result from L04 at the seven locations: keep only a pointer ('Lesson 5 treats the date-0 comparison'), with no equality claim, and remove the Theorem 4.1 sentence from card FC2-c059. "
  "If the architect instead permits a forward statement in L04, record that ruling in plans/FINAL-ARCHITECT-RULINGS.md and state (N) and r >= 0 in each statement.")
R("FC2b-cards-hypotheses", "cards", "cards.json FC2-c059 (L04 hypotheses) and the other slice cards", "FAIL",
  "Card FC2-c059 back: 'For a call on an underlying with no income and r >= 0, Lesson 5 proves equality at date 0 (Theorem 4.1 there).' Theorem 4.1 (L05.html:301) has hypotheses A1, A2, A3, A4, A5, (N) and r >= 0; the card omits (N), so it does not carry the proposition's hypotheses (VERIFIER rule 10). "
  "All other slice cards that state a proposition carry its hypotheses: c054, c055, c066-c067, c069-c071, c078, c160-c162, c084-c085, c089, c093, c163 (checked against L04-L06 and L05 hypotheses lines).",
  "Either remove the Theorem 4.1 sentence from FC2-c059 (see FC2b-plan-L04-no-L05-result), or state its full hypotheses: 'under A1 to A5, (N) and r >= 0, Lesson 5 proves V_A(0) = V_E(0) for a call (Theorem 4.1)'.")
R("FC2b-cards-delta-round1", "cards", "cards.json delta edbb7aa8..dde0486b for L04-L06: FC2-c052, c059, c060, c064, c159, c179, c180, c181", "FAIL",
  f"Delta hunks read in full ({S}cards_slice_r5.out; git diff edbb7aa8 HEAD -- course/modules/FC/FC2/cards.json). PASS for c052 (Lemma 1.2), c060 (Prop 2.2; Remark 4.2 pointer), c064 (Remark 1.3), c159 (L04.html:61 A2), c179 (Lemma 1.2; Remark 1.3), c180 (proof of Theorem 1.2 uses A1, A2, A3, A5 and the rate of A4; Remark 1.3), c181 (Definition 2.1 and the Remark, L06.html:114). "
  "FAIL for c059: its new sentence (i) states the L05 Theorem 4.1 result inside an L04 card, contrary to plan lines 105 and 431-432 (row FC2b-plan-L04-no-L05-result), and (ii) omits hypothesis (N) (row FC2b-cards-hypotheses).",
  "Apply the fix of the two rows above to FC2-c059; all other delta hunks in the slice are PASS.")
R("FC2b-cards-coverage", "cards", "cards.json: 71 cards with lesson L04 (19), L05 (25), L06 (27)", "PASS",
  f"{S}cards_slice_r5.out: deck 171 cards, 171 unique ids; slice 71 cards (L04 19, L05 25, L06 27). Round 4 had 68; delta adds FC2-c179 (L04), FC2-c180 (L05), FC2-c181 (L06).")
R("FC2b-cards-duplicates", "cards", "cards.json whole deck, pairwise scan", "PASS",
  f"{S}cards_dup_r5.out: 171 unique ids; all 14,535 pairs scanned with difflib ratios; the 68 pairs above the threshold were read. No pair is a duplicate: different questions, different facts (e.g. FC2-c066 call bounds vs c161 put bounds; c057 put vs c135 call; c071 equality vs c132 no rule). "
  "Two same-identity pairs are judged distinct, not duplicates: FC2-c052 vs c179 (Lemma 1.2 asked as an identity vs as a synthetic-forward question) and FC2-c084 vs c089 (one-period cost in the q form vs the expectation form).")
R("FC2b-cards-near-duplicate", "cards", "L05 c066/c160/c161/c162; L04 c057/c135; L05 c071/c132; L06 c084/c163; L06 c084/c089; L04 c052/c179; L04 c143 vs L02 c017", "PASS",
  f"{S}cards_dup_r5.out. Each listed pair asks a different question with a different answer. Judgement noted, not failed: c084/c089 and c052/c179 restate one fact in a second form (as round 4 accepted for c084/c089).")
R("FC2b-cards-grade-ruling9", "cards", "cards.json grades for L04-L06", "PASS",
  f"{S}cards_slice_r5.out: C-graded slice cards c058, c061, c072, c073, c074, c079, c095, c148, c155, c171 each name Lab 1 or a lab output; T-graded cards cite page results (Example, Theorem, Lemma, Remark). c075 (T, Problem E1 exact) is accepted as in round 4: its values are page formulas.")
R("FC2b-cards-L04-grades", "cards", "cards.json FC2-c051..c062, c135, c142, c143, c158, c159, c176, c179", "PASS",
  f"{S}cards_slice_r5.out lists 19 L04 cards; grades match content: T for Lemma/Prop/Example facts (c052, c054-c057, c059, c060, c062, c135, c179); C for lab output (c058, c061).")
R("FC2b-cards-L04-rest", "cards", "L04 cards without grade", "PASS",
  f"{S}cards_slice_r5.out: ungraded L04 cards c051, c053, c142, c143, c158, c159, c176 are definitions or restatements of hypotheses, which BUILDER_RULES section 7 does not require to carry a grade.")
R("FC2b-cards-L05-C-grades", "cards", "cards.json L05 C-graded cards c072, c073, c074, c079, c155, c171", "PASS",
  f"{S}cards_slice_r5.out. Each cites Lab 1 (SIMULATED) and its numbers match the printed lines: L05.html:268 (parity 0), 273-274 (-300, payoff 0), 278 (0 residuals), 281-284 (3 triples, middle 90), 270-271 (no violation), 269 (0 of 40).")
R("FC2b-cards-L05-c064", "cards", "cards.json FC2-c064 (Theorem 1.2 card)", "PASS",
  "Front states A1 to A5; back: 'Every strike ... C - P = S - e^{-rtau}K ... does not say that the put and the call are equal at any strike (Remark 1.3)'. Remark 1.3 (L05.html:71) says the same. The proof-hypothesis sentence moved to c180.")
R("FC2b-cards-L05-rest", "cards", "cards.json L05 cards c063-c070, c071, c075, c076, c078, c080, c132, c153, c160-c162, c180", "PASS",
  "Each back matches the current L05 text: c063 (Def 1.1); c065 (Def 2.1, (N) at L05.html:76); c066 (Thm 2.2(a)); c067 (Remark 2.3); c068 (Def 3.1); c069 (Thm 3.2); c070 (Cor 3.4); c071 (Thm 4.1 with (N) and r >= 0, Remark 4.2); c075 (E1 solution, L05.html:402); c076 (Section 5, 40.48); c078 (Thm 2.2(a)); c080 (Remark 4.2, R2); c132 (Remark 4.2); c153 (Remark 3.3); c160-c162 (Thm 2.2(b),(c),(d)); c180 (Remark 1.3 and the proof of Thm 1.2 at L05.html:67, which use A1, A2, A3, A5 and the rate of A4).")
R("FC2b-cards-L06-grades", "cards", "cards.json FC2-c081..c098, c136, c137, c148-c150, c163, c166, c174, c181", "PASS",
  f"{S}cards_slice_r5.out. T for theorem, definition-derived and page-computed facts; C for c095 and c148 (lab output). c181 new (T): E^Q[S1] = q u S0 + (1-q) d S0 and the condition for R_f S0 is the Remark at L06.html:114 (identity, re-derived).")
R("FC2b-cards-L06-rest", "cards", "L06 cards without grade", "PASS",
  f"{S}cards_slice_r5.out: ungraded c081, c082, c083, c088, c090, c092, c166, c174 are definitions. Each back matches L06.html (Def 1.1, 1.2, 1.3, 2.1, 3.1, 3.2, 1.2, 3.5).")
R("FC2b-cards-key-mirror", "cards", "key-results tables L04.html:383-393, L05.html:450-460, L06.html:401-410 vs cards", "PASS",
  "Each key-results row has a card with the same number and grade: L04 rows (c052, c054, c055, c056, c057, c135); L05 rows (c064, c066/c160-c162, c069, c070, c071, c072-c074/c155); L06 rows (c084, c085, c089, c093, c094).")
R("FC2b-cards-c176-added", "cards", "cards.json FC2-c176", "PASS",
  "c176 unchanged in the delta; back restates A1 (L04.html:60): no dividend, coupon or storage cost.")
# ---- quiz, misconceptions, notation, process, DAG, hours
R("FC2b-quiz-L04-L06", "quiz", "L04.html:396-466 (9 items), L05.html:464-534 (9 items), L06.html:412-481 (10 items)", "PASS",
  "Keyed answers re-checked: L04 25, 17, V_A(0)>=V_E(0), 20, expiry only, 77, 6.56, date 1, long call minus long put = S-K; L05 C-P=S-DK, 9.85, sell call and buy share, 12, (K3-K2)/(K3-K1), 1, equality at date 0, (N), 40.48; "
  "L06 Theorem 1.4(b) inputs, 0.5, 30, d<R_f<u, 0.75, arbitrage (sell call, buy 1/2 share, borrow 20, lend 5), 45, 'none', 75, 100 (E^Q[S2]/R_f^2). Each item has an explanation. The L06 \\E edits do not change any answer.")
R("FC2b-misconception-L04-L06-other", "misconception", "L04.html:256-271, L05.html:327-337, L06.html:327-335", "PASS",
  "Each wrong statement is wrong and each correction is right (L04: misc 1 and 2 correct but restate the L05 result, row FC2b-plan-L04-no-L05-result; misc 3 (payoff vs profit, 108 vs 100) and 4 correct; L05 misc 2-4 correct; L06 misc 1-3 correct).")
R("FC2b-hours", "hours", "L04-L06 data-hours; index.html:29 and the hub hour cards", "PASS",
  f"Lesson data-hours L01 6, L02 8, L03 9, L04 7, L05 8, L06 8, L07 8, L08 6: sum 60 = index.html data-hours-lessons=\"60\" (line 29), project 30 (line 29), 90 total. Hub cards 'L04 · 7 h', 'L05 · 8 h', 'L06 · 8 h'.")
R("FC2b-banned-process", "prose", "L04-L06 visible prose and changed twin docstrings", "PASS",
  f"grep -i for verifier, builder, ledger, ruling, architect, round N, slice, TODO, placeholder, reviewer, audit on L04-L06 and the twins: no match (grep run this round; no output lines).")
R("FC2b-notation", "notation", "L04-L06 math vs notation/notation.json (unchanged since the previous pin)", "PASS",
  "Registered: macro \\E = \\mathbb{E} (notation.json line 5-6); symbols R_f (AP1) and \\mathbb{Q} (AP1, 'by default an equivalent martingale (risk-neutral) measure'), T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}. "
  "Round-5 change: L06 uses \\E in place of the raw \\mathbb{E} (grep of L04-L06 for raw mathbb{E}: 0 matches); L06 uses \\mathbb{Q} for the binomial risk-neutral measure, whose registered meaning allows that. "
  "No registered symbol with another meaning appears in L04-L06 (grep for T, Phi, gamma, R^ast: none).")
R("FC2b-dag-links", "dag", "L04-L06 concept links and definitions", "PASS",
  f"tools/check_dag.py --unit FC2 PASS ({S}check_dag.txt). L06 links: risk-neutral-probability and binomial-option-pricing defined on the page; expectation and discount-factor (M4, M1 in the closure). L04 and L05 links unchanged.")
R("FC2b-define-before-use-self-financing", "define-before-use", "L06.html:161-162 (Definition 3.5), first use L06.html:167", "PASS",
  "'self-financing' is defined in Definition 3.5 before the lab hypothesis (L06.html:167) and interpretation (317) use it.")
R("FC2b-scope-words", "scope", "L04-L06 'every', 'all', 'never', 'any', 'always', 'only', 'exactly', 'same' in the changed hunks and full reads", "PASS",
  "'exactly when' (L06.html:114, c181) is an identity proved by algebra; 'never better than selling' (c060) follows from Prop 2.2; 'only the time-0 values' (L06 docstring) matches output lines 299, 300, 306, 307 (cents only on time-0 lines); 'every state' (A3, Theorem 1.4) is the stated hypothesis; 'does not say ... any strike' (c064, Remark 1.3) matches L05.html:71.")
R("FC2b-simulated-labels", "data", "L04 Example 2.5 (L04.html:115), L04 lab (L04.html:124-128), L05 lab (L05.html:132-136), L06 lab (L06.html:167-178)", "PASS",
  "L04 Example 2.5 and Lab 1 are labelled SIMULATED (L04.html:115, 124, twin line 3 'SIMULATED: the price path is a fixed list'); L05 lab 'SIMULATED: every price is generated ... from a formula' (twin line 3); L06 inputs are model values, 'not market data' (twin docstring lines 8-10; L06.html:167).")
R("FC2b-figures", "figures", "L04-L06 (no figures, data-files or data-cite)", "PASS",
  "grep for data-files, data-cite, <figure, figures-L0, data/ in L04-L06: no match.")
R("FC2b-lab-rng-network", "lab-hygiene", "tests/labs/FC2 L04/L05/L06 twins (read in full)", "PASS",
  "Twin imports: __future__, fractions, itertools, math only; no random, socket, urllib, http or open. The word 'random' appears only in 'draws no random numbers' statements.")
# ---- numbers and structure
R("FC2b-num-L04", "numbers", "L04.html prose numbers (lines 51, 73, 116, 120, 125, 243, 258-266, 335-377, 389-390)", "PASS",
  f"Every number recomputed exactly ({S}numbers_v5.out): 108, 93, 6.56, 7.29, 8.10, 9.00, 14.58, 18, 20(9/10)^3, 127.43484 (R1), 32.805 (R3), 0.10536 (ln(10/9)), 17, 77, 25.00 and 17.00 at 125 USD, 8.00 premium.")
R("FC2b-num-L06", "numbers", "L06.html prose numbers (lines 94, 99, 157, 319, 332, 335, 342-388, 441-476)", "PASS",
  f"Every number recomputed ({S}numbers_v5.out): q=3/4, 1/2 (M1, R2), V0 30, 40, 48, 45, 60, 75, 120, 25/4, 5/2, 156.25, 56.25, 36, 70.3125 (1125/16), 3/4 share and bond -30, 5/6 share and bond -50, 4000 cents, 4800 cents, 6000 cents.")
R("FC2b-num-L04-why-locator", "numbers", "L04.html:51, 116, 360, 374 (locators for derived numbers)", "PASS",
  "Locators: L04.html:116 (Example 2.5 values), 360 (R1 value 127.43484), 374 (R3 values 7.29, 32.805) match the recomputation.")
R("FC2b-struct-L04", "structure", "L04.html (BUILDER_RULES 4.2 order and counts)", "PASS",
  "why-it-matters 120 words (L04.html:51, limit 120); sections 1-2 with Definition, Lemma, Proposition, Remark, Example blocks; inline lab (123-244); canon breaks (247-251); misconceptions 4 (256-271); problem set 3 tiers x 3 (281-377); key results 5 rows (383-393); quiz 9 items (396-466); references (468-472).")
R("FC2b-struct-L06", "structure", "L06.html (BUILDER_RULES 4.2 order and counts)", "PASS",
  "why-it-matters 113 words (L06.html:51); sections 1-3 with Definition, Theorem, Proof, Example, Remark blocks; inline lab (165-318); canon breaks (320-325); misconceptions 3 (327-337); problem set 4 tiers, 3 each (339-397); key results 5 rows (399-411); quiz 10 items (413-481); references (484-488).")
# ---- carried L05 rows (subject byte-identical)
for cid in CARRY:
    pr = prev_rows[cid]
    assert pr["status"] == "PASS", cid
    rows.append({"id": cid, "check": pr["check"], "location": pr["location"], "status": "PASS",
                 "evidence": PFX + pr["evidence"]})
# ---- a row for every round-4 id not yet present (kept ids)
have = {r["id"] for r in rows}
missing = [i for i in prev_rows if i not in have]
print("round-4 ids not reproduced:", missing)
# ---- fragment envelope
n_pass = sum(1 for r in rows if r["status"] == "PASS")
n_fail = sum(1 for r in rows if r["status"] != "PASS")
frag = {
    "unit": "FC2",
    "slice": "b",
    "round": 5,
    "verifier": "Haiku independent verifier, FC2 slice b round 5 (did not build FC2)",
    "pin": "dde0486beeb0312e4ac1cc03aaa02e56644adb24",
    "base": "edbb7aa8de20e6d2f3035c463a79a318c22623c4 (round-4 pin; previous fragment /Users/billyribeiro/.fanout/frags/S-FC2-b.round4.json). Delta edbb7aa8..dde0486b read in full for the slice: course/modules/FC/FC2/L04.html:125, L06.html (A2, Def 2.1 macro, Thm 2.2 proof, misconception 3, quiz Q10, references, lab docstring and interpretation), tests/labs/FC2/lab-FC2-L06-1.py (docstring only), cards.json (c052, c059, c060, c064, c159, c179, c180, c181).",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyS5-FC2-b",
    "scratch": "none outside the checkout; all scripts and outputs are under ledgers/FC2/scripts/FC2-b-r5/",
    "verified_at": "2026-11-09T00:00:00+00:00",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Scope: slice b = L04.html, L05.html, L06.html; lab twins tests/labs/FC2/lab-FC2-L04-1.py, lab-FC2-L05-1.py, lab-FC2-L06-1.py; the 71 slice cards (L04 19, L05 25, L06 27) in course/modules/FC/FC2/cards.json.",
        "Carry rule: 14 L05 PASS rows carried from round 4 because L05.html, lab-FC2-L05-1.py, notation.json, references.json, tools/, plans/FC2-build-plan.md, BUILDER_RULES.md and VERIFIER_RULES.md are byte-identical since edbb7aa8 (git diff --quiet). Every other row was re-verified from scratch this round, including the round-4 FAIL (FC2b-lab-L06-docstring), now PASS.",
        "Round 4 PASSed L04 rows that state the Lesson 5 Theorem 4.1 result inside L04 (L04.html:51, 111, 120, 243, 248, 258, 262). Plan lines 105 and 431-432 say that result waits for L05 and is not stated in L04. Round 5 records this as FAIL (row FC2b-plan-L04-no-L05-result). Both L04 and the card FC2-c059 carry this defect; the page text is unchanged by the delta, so it is pre-existing.",
        "Judgement, accepted and not failed: c075 (T, basis Problem E1 exact) reads values from the page's own formula for the Lab 1 synthetic calls (as round 4). c084/c089 and c052/c179 restate one fact in a second form. Theorem 1.4 (c) and Theorem 2.2 (b) hypotheses are carried by their cards.",
        "Mutation testing: not applicable. Slice b has no project grader; per the rulings, mutants apply only to project graders. mutants is empty.",
        "Notation: L06 now uses the registered macro \\E for expectation (notation.json line 5-6); no raw \\mathbb{E} remains in L04-L06. \\mathbb{Q} (a registered symbol, AP1 meaning 'by default an equivalent martingale (risk-neutral) measure') is used for the binomial risk-neutral measure as plan section 5.3 item 5 prescribes.",
        "Not checked: a browser screenshot of L04-L06 (page_smoke geometry and console checks passed; no visual review); the live verify_refs run (needs network; no L04-L06 page cites a key); the hub, L01-L03, L07-L08 and project pages except where the gates cover them; the full curriculum source for the lesson hours (only the hub split and data-hours were checked).",
    ],
    "summary": (f"FC2 slice b round 5 (pin dde0486b): {len(rows)} rows, {n_pass} PASS, {n_fail} FAIL. "
                "FAIL rows: FC2b-plan-L04-no-L05-result (L04 states the Lesson 5 Theorem 4.1 result, contrary to plan lines 105 and 431-432, and omits hypothesis (N)); "
                "FC2b-cards-hypotheses (card FC2-c059 omits hypothesis (N) of Theorem 4.1); FC2b-cards-delta-round1 (the delta hunk is c059, failing for both reasons). "
                "The round-4 FAIL (FC2b-lab-L06-docstring) is fixed and PASSes. All gates pass: check_pages, check_dag, check_projects, run_graders, run_labs (unit, L04, L05, L06), page_smoke (L04, L05, L06 alone), twins under python -I -W error, ruff, mypy, pytest, verify_refs --offline. Page code equals the twins and every expected block equals the twin output."),
}
out = ".../ledgers/FC2/FC2-b.json".replace("...", ROOT)
json.dump(frag, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("wrote", out, "rows", len(rows), "pass", n_pass, "fail", n_fail)
