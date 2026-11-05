"""Writes the PC3 slice d round-12 verifier fragment (verifier-authored; standard library only)."""
import json
from datetime import UTC, datetime

S = "ledgers/PC3/scripts/PC3-d-r12"
R = "/tmp/pc3d_r12"
RED = f"{S}/out/rederive_r12.txt"
SCAN = f"{S}/out/cards_scan_r12.txt"
DUMPS = f"{S}/strip.py (dumps regenerated into {R}/L01.txt .. L06.txt)"
rows = []


def row(rid, check, location, evidence, status="PASS", fix=""):
    item = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        item["fix"] = fix
    rows.append(item)


ALL_CARDS = "course/modules/PC/PC3/cards.json (174 objects, read in full this round)"
L01 = "course/modules/PC/PC3/L01.html"
L02 = "course/modules/PC/PC3/L02.html"
L03 = "course/modules/PC/PC3/L03.html"
L04 = "course/modules/PC/PC3/L04.html"
L05 = "course/modules/PC/PC3/L05.html"
L06 = "course/modules/PC/PC3/L06.html"

row("cards-schema", "cards.json is valid JSON; 174 objects; keys id, lesson, front, back, cite; grade and basis on graded cards; ids unique",
    ALL_CARDS,
    f"{S}/cards_scan_r12.py -> {SCAN}: 174 cards, unique ids; key sets {{back,basis,cite,front,grade,id,lesson}} x130 and "
    "{back,cite,front,id,lesson} x44; grade T 90, C 40, none 44; ids strictly increasing; cite empty for all 174. "
    "tools/check_pages.py --unit PC3 -> 'check_pages PC3: PASS' (out/check_pages_PC3.txt).")
row("cards-coverage", "every card names an existing lesson; every lesson has cards; card counts per lesson",
    ALL_CARDS,
    "scan output: per lesson L01 24, L02 23, L03 29, L04 37, L05 26, L06 35 (total 174); all six lesson files exist; "
    "every card's lesson field is one of L01..L06; check_pages PC3 PASS (no 'no cards for' problem).")
row("cards-dup-scan", "no duplicate front or back text across the 174 cards",
    ALL_CARDS,
    f"{SCAN}: duplicate fronts [] and duplicate backs []. Full read for near-duplicates: pairs with shared basis "
    "(c026/c027/c028; c030/c031/c032/c037; c072/c078; c123/c124) ask different questions.")
row("cards-block-001-010", "cards PC3-c001..c010 against L01 text",
    f"{L01} Def 1.1 (l.59), A1 (l.63-64), Thm 1.2 (l.68-73), Prop 1.3 (l.85-89), Ex 1.4 (l.98-100), Sec 2 (l.105-107), Sec 4 (l.317-318), Sec 5 (l.327-332); {R}/L01.txt",
    "c001 matches Def 1.1 l.59; c002 matches A1 l.64; c003 ln(u/l) as used in Prop 1.3 (l.89) and the lab's log-width definition; "
    "c004 (T) matches Thm 1.2 conclusion l.73 with its hypotheses (H1)-(H2) l.70-71; c005 matches l.317-318 and R2 (l.440-443); "
    "c006 matches Prop 1.3 l.89; c007 12 000 and 234 000 (l.99; rederive_r12 L01 checks); c008 matches Prop 1.3 use at l.105; "
    "c009 (C) 0.1754 = 5.9 % of 2.9704 and 0.9163 = 30.8 % (l.107, l.328; rederive_r12 narrowing shares); c010 matches l.332. "
    f"Script: {S}/rederive_r12.py -> {RED} (142 OK).")
row("cards-block-011-020", "cards PC3-c011..c020 against L01/L02 text",
    f"{L01} Thm 1.5 (l.119-125), Rem 1.6 (l.134-135), Ex 1.7 (l.139-141), Rem 1.6 and Part 3 (l.146); {L02} Def 2.1 (l.56-57), Def 2.2 (l.66-67), Rem 2.3 (l.71-72)",
    "c011 hypotheses (H1)-(H3) and bound match Thm 1.5 l.121-125 (A2 used for x>0); c012 n=2 equality (l.135); c013 1.1046221254 (l.140; "
    "rederive (1.01)^10 = 1.10462212541...); c014 1.6289 and miss 0.1289 (l.141, l.336; rederive); c015 x>=0 (l.319); "
    "c016 (T) ln(3/2)=0.4055, ln(2.5/1.01)=0.9063, ln2.5=0.9163, ln3=1.0986 and the B-width/reduction comparison (l.447; rederive R3 checks); "
    "c017-c020 match Def 2.1 (l.57), Def 2.2 (l.67), Rem 2.3 (l.72).")
row("cards-block-021-030", "cards PC3-c021..c030 against L02 text (c022 basis re-read after the round-10 fix)",
    f"{L02} Prop 2.4 (l.76-80), Prop 2.5 (l.89-99, proof l.99), Ex 2.6 (l.111), Ex 2.7 (l.116-117); cards.json PC3-c022 (line 180; basis line ~186)",
    "c021 Bayes hypotheses A1, P(A)>0, P(B)>0 and conclusion match l.78-80; c022 basis 'B is the disjoint union of the sets B ∩ C_i' matches the proof l.99; "
    "c023 1/3 and 1/2 with probabilities 3/4, 1/2, 1/4 (l.111; rederive P(HH|one head)=1/3, P(HH|first H)=1/2); c024 event sets {HH,HT,TH} and {HH,HT} (l.111); "
    "c025 1/3 vs 1 (l.111, l.386; rederive); c026-c028 3/5, 3/5, 3/10 (l.116; rederive by enumerating 20 ordered pairs); c029 3/4 (l.117; rederive).")
row("cards-block-031-040", "cards PC3-c031..c040 against L02 and L03 text",
    f"{L02} Ex 2.8 (l.122-124), Sec 4 (l.366-368, l.378-382), Lab Part 1 output (l.340), M2 (l.406-408); {L03} Def 3.1 (l.62), Prop 3.2 (l.68-75), Ex 3.3 (l.80)",
    "c030 rule A 1/3 and 2/3 (l.123; rederive mh_rule('A')); c031 rule B both 1/2 (l.124; rederive mh_rule('B')); c032 matches l.378; "
    "c033 bag example 3/4 with P(red)=1/2 (l.129; rederive); c034 matches H1 l.78; c035 P(B)=29/100 and P(A|B)=15/29 (l.408; rederive); "
    "c036 12 of 12 agreement (l.340, l.134; my own generator reproduces 12 of 12); c037 matches l.366; c038 Def 3.1 (l.62); c039 Prop 3.2 (l.68-75); c040 350 cents (l.80; rederive).")
row("cards-block-041-050", "cards PC3-c041..c050 against L03 text",
    f"{L03} Ex 3.3 (l.80), Def 3.4 (l.87), Def 3.5 (l.92), A2 (l.97), Ex 3.6 (l.102-104), Def 3.7 (l.109), Thm 3.8 (l.297-303), Rem 3.9 (l.316)",
    "c041 E[X+Y]=7 (l.80; rederive); c042 Def 3.4 (l.87); c043 Def 3.5 (l.92; ungraded, definition); c044 A2 fair game (l.97); "
    "c045 250 = 350-100 (l.102); c046 1150/3 = 2300/6 (l.103; rederive); c047 lab 64 policies 1150/3 (l.269, l.191); c048 Def 3.7 (l.109); "
    "c049 hypotheses A1, A3, (H2), (H3) and E[W]=0 (l.299-303, proof l.311); c050 Rem 3.9 (l.316).")
row("cards-block-051-060", "cards PC3-c051..c060 against L03 text (c057 fixed in round 10 and re-read)",
    f"{L03} Ex 3.10 (l.321-322), Ex 3.6 (l.102-104), Thm 3.8 (l.299-301), R1 (l.443), P3 (l.407), Sec 5 (l.345, l.349), Sec 4 (l.336), lab output (l.273-285)",
    "c051 150 = 6 x 25 (l.322; output l.281); c052 1575/32 (output l.282; rederive by exact enumeration); c053 zero for five rules (output l.273-279); "
    "c054 Thm 3.8 with A2 over N=6 (l.321); c055 50 cents, paths 200, 100, 0, -100 (l.443; rederive); c056 faces 1 and 2, threshold 3 (l.407; rederive); "
    "c057 (H1)-(H3) of Thm 3.8 (l.299-301, l.345); c058 100/3 (l.104, l.349; rederive); c059 mean 350, not fair (l.336, l.349); c060 (H2) fails at the first turn (l.450).")
row("cards-block-061-070", "cards PC3-c061..c070 against L03 and L04 text",
    f"{L03} Ex 3.11 (l.327-328), Sec 4 (l.336), Sec 5 (l.352-353); {L04} Def 1.1 (l.59-65), A1 (l.72), A5 (l.76), Def 2.1 (l.97), Prop 2.2 (l.102-107), Rem 2.4 (l.122), Prop 2.3 (l.112-117), Prop 3.1 (l.129-131), Ex 3.2 (l.143)",
    "c061 matches Ex 3.11 and l.353; c062 Def 1.1 steps (l.62-65); c063 1/4, 1/4, 1/2 (l.72); c064 A5 fill test with L=10 (l.76); "
    "c065 Def 2.1 (l.97); c066 Prop 2.2 hypotheses and conclusion (l.102); c067 (C, SIMULATED) mid 9990, settlement 9980, one unit: 40 vs 30 cents (l.122, l.581-583; "
    "Part 1 output l.446-451; rederive P&L 30 and mark-at-mid 40); c068 Prop 2.3 (l.112); c069 Prop 3.1 hypotheses and conclusion, and the not-claimed cases (l.129-132); c070 5, 0, 5/2 (l.143; rederive).")
row("cards-block-071-080", "cards PC3-c071..c080 against L04 text and Lab 1 printed output",
    f"{L04} Cor 3.3 (l.147-153), Ex 3.2 (l.143), Rem 3.4 (l.158), Prop 4.1 (l.164-170), Rem 4.2 (l.175), Lab Part 1 output (l.446-458), Part 2 output (l.460-469), Part 3 output (l.471-475), Sec 6 (l.491-500)",
    "c071 zero iff v = a+h with v >= a (l.148, l.152); c072 (1-p)h and h/2 at p=1/2 (l.158); c073 mean 0, variance 25I^2 (l.165, l.170); "
    "c074 15 and 50 cents (l.175; rederive 5|I|); c075 nine values 9980..10020 step 5 (lab l.389, output l.460-468); c076 every fair value by Prop 3.1 proof, lab checks nine grid values (l.200-202); "
    "c077 (C) 9 fills (output l.446; rederive 9); c078 zero at v=a+h (l.492, Cor 3.3); c079 10 cents (l.496, l.519; rederive W=10); c080 2500 cents^2 at 10 units (l.500, output l.475).")
row("cards-block-081-090", "cards PC3-c081..c090 against L04, L05 text",
    f"{L04} A3 (l.74), Problem R1 (l.594), R3 (l.606-608), Misc (l.504); {L05} Def 1.1 (l.57-65), Rem 1.2 (l.71), Def 1.3 (l.78), Prop 2.1 (l.86-92), Rem 2.2 (l.97), Def 3.1 (l.106), Prop 3.2 (l.125-132)",
    "c081 A3 and the 'not a quote from v_t' misconception (l.74, l.504); c082 d = (1-p)h/p and 20/3 (l.594; rederive; the r11 wording fixed in the round-12 pin matches R1's criterion); "
    "c083 |I|=1 with variance 25 and strict bound at 2 (l.606-608; rederive); c084 six steps in order (l.60-65); c085 no timer, no length fixed (l.71); c086 Def 1.3 (l.78); "
    "c087 (T) (n-k+1)(k-1), basis 'no comparison is shared between windows' matches proof l.92; c088 (T) k=n/2+1, n^2/4 (l.97; rederive over n=200); c089 surviving index (l.106); c090 Prop 3.2 output and invariant (l.125-132).")
row("cards-block-091-100", "cards PC3-c091..c100 against L05 text (round-11 FAIL on c092 re-verified)",
    f"{L05} Prop 3.3 (l.137-142), Rem 3.4 (l.147; 'At step k+1' in the current text), Ex 3.5 (l.152), M2 (l.376-378), P3 (l.408-410), Lab Part 1 output (l.313), Part 3 output (l.330), Sec 4 (l.339), Sec 5 (l.348, l.352, l.356); cards.json PC3-c092 (line 784)",
    "c091 n appends, at most n removals, at most 2n while-loop comparisons (l.137-142; rederive randomized check over 300 sequences); "
    "c092 (T) now asks about step k+1 and l.147 says 'At step k+1' for the same removal, so card and lesson agree; the mathematics re-derived: after step k the deque is k..1 indices, step k+1 removes all k "
    "(rederive, pseudocode order); c093 (4,4,5) (l.152; rederive); c094 (5,5,1,3) (l.376-378; rederive); c095 n-1 for every k (l.408-410; rederive all k for n<40); "
    "c096 1351 = 193 x 7 (l.312, l.259; rederive); c097 5239 = 169 x 31 (l.330; rederive); c098 matches l.339 and l.348; c099 counts, no run times (l.169-170, l.352); c100 (T) matches l.340 and l.356.")
row("cards-block-101-110", "cards PC3-c101..c110 against L05 and L06 text",
    f"{L05} Lab Part 2 output (l.319); {L06} Prop 1.1 (l.59-64), Rem 1.2 (l.70), NPV (l.73), A1 (l.82), A2 (l.83), Prop 2.1 (l.91-97), Rem 2.2 (l.103), Prop 3.1 (l.111-117)",
    "c101 True for window sizes 1..20 on seed 5 (l.319; rederive); c102 (s-K)^+ - (K-s)^+ = s-K (l.59-64); c103 price form from prerequisite module, not re-derived (l.70); "
    "c104 NPV formula (l.73); c105 A1 no income (l.82); c106 A2 lending/borrowing at S/D with D in (0,1] (l.83); c107 Prop 2.1(i) pays F'-S/D (l.92, l.97); "
    "c108 Prop 2.1(ii) F'=S/D with both arbitrage directions (l.98); c109 Rem 2.2 S e^{r tau} (l.103); c110 NPV(u) = -I + mAu, strictly increasing, u* = I/(mA) (l.112, l.117; rederive A=3310/1331).")
row("cards-block-111-117", "cards PC3-c111..c117 against L06 text and lab output",
    f"{L06} Prop 3.2 (l.122-127), Cor 3.3 (l.132-137), Def 4.1 (l.144), Ex 4.2 (l.149), Rem 4.3 (l.154), Lab Part 2 output (l.293-304)",
    "c111 product bounds with both ends attained (l.122, l.127); c112 nothing fixed when the bounds straddle the break-even (l.132-137); c113 five steps (l.144); "
    "c114 [200, 1600] (l.149; rederive 2000*1*(1/10) and 4000*2*(1/5)); c115 A = 3310/1331 (l.149; rederive); c116 (C) about 1164.10 at 8% (l.154, output l.302; rederive 1164.1005); "
    "c117 (C) -12513148 cents, exact -16655000000/1331 (output l.298; rederive).")
row("cards-block-119-123", "cards PC3-c119..c123 against L06 text and lab output",
    f"{L06} Lab Part 1 output (l.287-290), Part 2 output (l.302-304), Sec 6 misconceptions (l.320-332), Ex 4.2 (l.149), Rem 4.3 (l.154); Lab Part 1 code spot list (l.221)",
    "c119 (C) 0 cents at 10000 and 100 cents at 10100 at each of five spot values 8000..12000, output True (l.221, l.287-290); c120 misconception matches l.320; "
    "c121 break-evens 1164.10, 1206.34, 1249.05 (l.302-304; rederive); c122 'buy only if ... above 1206.34' matches l.149; c123 sign negative at 200 and positive at 1600 at all three rates (output l.302-304; rederive); misconception matches l.331-332.")
row("cards-block-124-130", "cards PC3-c124..c130 against L06 and L01 text",
    f"{L06} Rem 4.3 (l.154), Prop 3.1 (l.112-117), Prob M2 (l.352-354), M3 (l.359-361), R3 (l.434-436); {L01} Ex 1.4 (l.99), Prop 1.3 (l.89), Lab Part 3 output (l.306)",
    "c124 1200 units above the 8% break-even (rederive: NPV at 1200, 8% > 0); c125 500/121 (l.352-354; rederive); c126 33275/331 = 100.53 (l.359-361; rederive); "
    "c127 margin ratio 0.7540 and fall 24.6 % (l.434-436; rederive); c128 ln 19.5 (l.99; rederive); c129 ln3, ln5, ln1.3 with 3*5*1.3 = 19.5 (l.99); c130 0.0046221254 (l.306; rederive).")
row("cards-block-131-135", "cards PC3-c131..c135 against L01 and L03 text and lab output",
    f"{L01} Thm 1.5 (l.125), Ex 1.7 (l.140-141), Lab Part 3 output (l.306-307); {L03} Lab Part 3b output (l.282-285)",
    "c131 0.0048728552 = 45 x 1.01^8 x 1e-4 (l.306; rederive); c132 remainder below bound (l.306; rederive); c133 bound 0.1662 and miss 0.1289 (l.307; rederive); "
    "c135 (C) 575/8 for 'stop when the total reaches 100 cents' (l.284; rederive exact enumeration).")
row("cards-block-136-142", "cards PC3-c136..c142 against L03, L04 and L05 text and lab output",
    f"{L03} Part 3b output (l.285); {L04} Part 1 output (l.446-452), SIMULATED label (l.476, l.180, l.183); {L05} Part 1 output (l.312-313)",
    "c136 (C) 625/8 for 'stop at 200 cents' (l.285; rederive); c137 (C, SIMULATED) cash flow -9950 (l.447; rederive); c138 inventory 1 (l.448); c139 settlement 9980 (l.449; rederive); "
    "c140 P&L 30 = -9950 + 9980 (l.451; rederive); c141 identity True (l.452); c142 (C) 354 deque comparisons (l.313; rederive, extra_seed_checks_r12.py).")
row("cards-block-143-150", "cards PC3-c143..c150 against L04, L05 and L06 text and lab output",
    f"{L05} Part 1 output (l.313), Part 2 output (l.319-324), Part 3 output (l.330-331); {L06} Ex 4.2 (l.149), Rem 4.3 (l.154), Part 2 output (l.298-304)",
    "c143 200 pushes, 199 pops (l.313; rederive); c144 387 <= 400, largest Part 3 count (l.331; rederive: counts 199, 263, 354, 382, 387); c145 382 (l.330; rederive); "
    "c146 five edge-case checks True (l.319-324); c147 399300/331 about 1206.34 (l.149; rederive); c148 1249.05 at 12% (l.154, l.304; rederive); "
    "c149 sign pattern at 8, 10, 12 % (l.302-304; rederive); c150 4894816 cents at 1600 units (l.299; rederive).")
row("cards-block-151-168", "cards PC3-c151..c168 against L01 to L06 text",
    f"{L06} Prob E3 (l.411), Sec 6 misc (l.320); {L04} Rem 1.2 (l.82), A5 (l.76), Ex 1.3 (l.88), A3 (l.74), A2 (l.73), A4 (l.75), A6 (l.77); {L01} Lab Part 1 output (l.288), A2 Lagrange (l.115); {L02} A1 (l.61-62), A2 (l.106); {L03} A1 (l.56-57), A3 (l.292-293)",
    "c151 (T) (1249.0469 - 1164.1005)/4 = 21.2366, displays 21.24 (l.411; rederive); c153 constants are model choices (l.82); c154 a fill is always one unit (l.76, l.82); "
    "c156 (C) ln 19.5 = 2.9704144656 (l.288; rederive); c157 A2 Lagrange (l.115); c158 A1 finite spaces (l.61-62); c159 A2 flips, 1/4 each (l.106); c160 A1 integer cents (l.56-57); "
    "c161 A3 finite horizon and fairness (l.292-293); c162 A2 fair path (l.73); c163 A4 informed trader (l.75); c164 A6 quote form (l.77); c165 A3 no costs (l.84); c166 A4 no arbitrage (l.85); "
    "c167 A5 short sale (l.86); c168 Ex 1.3 quoting rule (l.88).")
row("cards-block-169-171", "cards PC3-c169..c171 against L05 and L04 text",
    f"{L05} Rem 3.6 (l.156-158); {L04} A3 (l.74), Sec 2 inventory (l.93)",
    "c169 hash map keeps no order on values (l.157); c170 3n floor(log2 n) = 4200 for n=200 and the 2n = 400 deque bound (l.158; rederive); c171 A3 public history, not v_t (l.74).")
row("cards-block-172-179", "cards PC3-c173..c179 against L03, L04, L05 and L06 text",
    f"{L03} Def 3.7 (l.109), Def 3.5 (l.92), A3 (l.292-293), Rem 3.9 (l.315-316), Ex 3.11 (l.327); {L04} Sec 2 (l.93-97), Rem 3.4 (l.158), Prop 4.1 (l.164-170); {L05} Def 3.1 (l.106); {L06} Cor 3.3 (l.132-137), Prob E2 (l.405-407)",
    "c173 W(h) and the stopping total (l.109); c174 sign and cash change of a fill (l.93); c175 inventory and fill sign (l.93); c176 adverse selection in this model (l.158); "
    "c177 deque after step i, increasing index (l.106); c178 bounds do not fix the sign when the break-even is between them (l.132-137, l.328); "
    "c179 -105000000/1331 = -78888.05 at 1200 units (l.405-407; rederive). Ids c172 is absent from cards.json (stable id gap).")
row("cards-block-round3-id-carry", "carried id-gap and round-3 cards: stable ids, prop references",
    f"{ALL_CARDS}; {L01} Prop 1.3 (l.85-89); {L04} Rem 2.4 (l.122) and Sec 3 (l.125-131)",
    "Ids 118, 134, 152, 155, 172 are absent and are stable identifiers, not defects (cards_scan_r12.txt 'id gaps'). Prop 1.3 cited by c006-c008 exists (l.85-89). Rem 2.4 cited at L04 l.122 exists.")
row("cards-atomicity", "each card tests one fact (BUILDER_RULES §7)",
    ALL_CARDS,
    "Read all 174 cards. Compound fronts that ask two linked things: c123 (sign and what it leaves open, one misconception), c174 and c175 (a symbol and its effect, both defined in one sentence of L04 Section 2). "
    "These test one definition or one misconception each and are not trivia; no card carries a second unrelated fact.")
row("cards-c119-basis", "c119 basis and lab reference",
    f"cards.json PC3-c119 (line 1006); {L06} Lab Part 1 (l.221, l.287-290)",
    "basis 'Lab 1, Part 1 (five spot states, 8000 to 12000 cents)' matches the lab's five spot values (l.221) and the printed output (l.287-290).")
row("cards-c122-referent", "c122 refers to the lesson's recommendation",
    f"cards.json PC3-c122 (line 1033); {L06} Ex 4.2 (l.149)",
    "card back 'buy only if the firm's evidence puts units above 1206.34 per year at this rate, and measure units before committing' matches the recommendation at l.149.")
row("cards-c146-grade", "c146 grade C matches the lab-only result",
    f"cards.json PC3-c146 (line 1240); {L05} Lab Part 2 (l.176-177, output l.319-324)",
    "the five edge-case checks are printed True in the lab output (l.320-324); the grade C (single lab result) is consistent with the key-results table.")
row("cards-misconception-coverage", "every misconception in each lesson has a card",
    f"{ALL_CARDS}; {L01} Sec 5 (l.327-336); {L02} Sec 4 (l.377-386); {L03} Sec 5 (l.344-353); {L04} Sec 6 (l.491-504); {L05} Sec 5 (l.347-356); {L06} Sec 6 (l.319-332)",
    "L01: c009, c010, c014. L02: c024, c025, c032. L03: c057, c058, c061. L04: c078, c079, c080, c081. L05: c098, c099, c100. L06: c120, c121, c123, c178. All misconceptions in the six lessons are covered.")
row("cards-number-presence", "every card number appears in its own lesson text",
    ALL_CARDS,
    "strict scan (inline check, tags stripped, thousands spaces joined): 0 numeric tokens of two or more digits in a card's front or back are absent from that card's own lesson; "
    "0 absent from all six lessons (out/cards_scan_r12.txt).")
row("cards-lab-printed-values", "card values for lab output equal the printed lesson values and the twin output",
    f"tests/labs/PC3/lab-PC3-L01-1.py .. L06-1.py; {L01}..{L06} printed blocks",
    "each twin run alone under python3 -I -W error exits 0 (out/twin_L0*.exit); every line of each twin's stdout appears verbatim in its lesson's text (L01 26, L02 32, L03 30, L04 52, L05 25, L06 21 lines, 0 missing); the cards' C values match those lines.")
row("cards-rederive", "every number in the cards re-derived by independent code",
    f"{S}/rederive_r12.py; {S}/extra_seed_checks_r12.py",
    f"{RED}: 142 checks, ALL OK (exact Fraction enumeration of stopping rules, Monty Hall, urn, bag, drill set; deque with the lesson's pseudocode order; NPV and break-even at 8, 10, 12 percent; "
    "Prop 3.1 closed form equals brute enumeration on a grid). extra_seed_checks_r12.py: seed 1 summary (16, 20100, -2, 10020, 60), seed 5 and 6 deque counts (354, 199 pops; 350, 197 pops): ALL OK.")
row("gates-structural", "structural gates on the pin, run by this verifier",
    f"tools/check_pages.py --unit PC3; tools/check_dag.py --all; tools/check_projects.py --all; tools/run_labs.py --unit PC3; tools/page_smoke.py --unit PC3; tools/run_graders.py --unit PC3 --seeds 0-49; ruff; mypy; pytest; verify_refs",
    "check_pages PC3 PASS; check_dag PC3 PASS; check_projects PC3 PASS; run_labs PC3 PASS (9/9); page_smoke PC3 PASS (zero console errors reported); "
    "run_graders PC3 PASS (reference 50/50 seeds); ruff check and ruff format --check tests/labs/PC3 PASS; mypy --no-incremental PASS (385 files); "
    "pytest -k PC3 PASS; pytest tests/test_docs_figures.py PASS; verify_refs.py --offline PASS (560 entries, 0 problems; --unit needs a live run). Outputs under out/.")
row("cards-grade-agreement", "every graded card agrees with its lesson's key-results table",
    f"{ALL_CARDS}; key-results tables {L01} l.456-465, {L02} l.499-508, {L03} l.466-475, {L04} l.618-625, {L05} l.470-477, {L06} l.446-453",
    "T cards match the T rows (L01 c004-c008, c016; L02 c021-c025, c030-c031, c033; L03 c039, c046, c049, c054, c055; L04 c066, c068, c069, c071, c073; L05 c087, c088, c090, c091, c095; L06 c102, c107-c108, c110-c112, c114). "
    "C cards match the C rows (L01 c009, c013, c014, c130-c133, c156; L02 c036; L03 c047, c051-c053, c135-c136; L04 c067, c075, c077, c137-c141; L05 c096-c097, c101, c142-c146; L06 c116-c117, c119, c121, c123-c124, c148-c150). "
    "c043 is ungraded (a definition, which the key-results table does not list).")
row("cards-plan-grade-c043", "plan §9 grade wording for the fair-game definition",
    "cards.json PC3-c043 (line 365); plans/PC3-build-plan.md §9 (grade T list)",
    "plan §9 lists 'the fair-game definition as a definition' among the T-graded items, while BUILDER_RULES §7 grades results and gives definitions cards with no grade. c043 has no grade, and the L03 key-results table has no row for it, so no card contradicts a lesson. Noted for the orchestrator as a plan-wording question, not a card defect.")
row("cards-process-words", "no process words in learner text",
    f"{ALL_CARDS}; {L01}..{L06} visible text",
    "grep (case-insensitive) for round, verifier, fragment, audit, builder, pending, placeholder, TODO, TBD, lorem, 'for brevity', 'beyond the scope', 'it is important to note', 'clearly', 'obviously', 'it can be shown': no hits in cards or lessons.")
row("cards-simulated-label", "SIMULATED results carry the label; generated inputs are not called data",
    f"{L04} Lab header (l.180) and docstring (l.183); {L05} Lab header (l.163) and docstring (l.166); {L02} Lab (l.134, l.137-139)",
    "c067, c077 and c137-c141 name the SIMULATED lab (L04 l.180, l.183). The L05 and L02 items are seeded generated inputs labelled 'generated test input, not data' (L05 l.163, l.166) and 'generated items, not data' (L02 l.134, l.139), not simulated market data, so no SIMULATED label is required.")
row("cards-notation", "no registered symbol reused with another meaning (notation/notation.json)",
    "notation/notation.json (macros and 8 symbols); cards.json; L01-L06 macros",
    "registered symbols T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, Q (blackboard) do not occur in PC3 math. Macros used (\\Prob, \\E, \\Var, \\R, \\indic) are registered; all other macros are standard LaTeX. "
    "Lesson-local letters (N, L, I, A, p) are defined where used, as notation.json allows. Non-blocking observation: L06 uses A for the annuity factor, and A1-A5 name assumptions there.")
row("cards-block-titles", "block titles quoted on cards match the lesson headings",
    f"{ALL_CARDS}; {L02} l.56-57 (Definition 2.1), {L05} l.106 (Definition 3.1)",
    "c018 'Definition 2.1 (events on a finite probability space)' matches l.56; c089 and c177 'Definition 3.1 (the deque and its invariant)' match l.105-106; c084 and c086 titles match l.57 and l.77.")
row("lesson-numbers-prose", "prose numbers in the lessons that the cards quote agree with unrounded values",
    f"{L01} Ex 1.4 (l.99-100), Ex 1.7 (l.140-141), Sec 2 (l.107-109), Sec 5 (l.328); {L04} Rem 2.4 (l.122), E2 (l.576); {L06} Rem 4.3 (l.154), E2 (l.403-404), E3 (l.411)",
    "rederive_r12.py: 2.9704, 2.5649, 2.0541, 0.9163 (30.8 %), 0.1754 (5.9 %), 19.5, 52 990.57, 1.1046, 1.6289, 0.1289 (7.9 %), 0.9485, 5.4 %, 1164.10, 1206.34, 1249.05, 42.24, 42.70, 42.71 (displayed difference, not the answer), 21.24; "
    "L04 l.576 1.96 and 1.959964 (97.5th percentile of the standard normal) is the stated value.")
row("lesson-scope-words", "scope words in cards claim no more than the proofs and labs show",
    f"{ALL_CARDS}; {L01}-{L06} scope sentences",
    "read all cards: c050 (no unbounded rule), c076 (every fair value, by Prop 3.1's proof), c100 (every sequence, by Prop 3.2), c154 (a fill is always one unit, A5), c158 and c160 (every sample space is finite, A1), c161 (fairness at every history, A3). Each generalisation is a stated proof or a stated hypothesis.")
row("lesson-dag-and-attribution", "uses lines and attributions, DAG (check_dag) and no unread citation",
    f"{L01} Uses (l.37); {L02} Uses (l.37), Introduces (l.38); {L03} Uses (l.37); {L04} Uses (l.38); {L05} Uses (l.38); {L06} Uses (l.38); tools/check_dag.py --all",
    "check_dag PC3 PASS. Cards cite no registry key (cite [] for all 174) and the lessons cite no registry source, so no bibliographic attribution is made. Concepts named on cards (M1, M2, M4, Lesson 1-3 links) appear in each lesson's Uses or Introduces line.")
row("lesson-L02-introduces-metadata", "L02 Introduces line names the concepts its cards test",
    f"{L02} l.38",
    "l.38 'Introduces: conditional probability (Definition 2.2), Bayes' rule (Proposition 2.4) and the law of total probability (Proposition 2.5)', matching the cards that test those items (c019, c021, c022).")
row("adjacent-lesson-numbers", "cross-lesson numbers (M4 Lesson 1, Remark 2.3, Definition 3.5) point to existing items",
    f"cards.json PC3-c017, c020, c043; {L02} Def 2.1 (l.57), Rem 2.3 (l.72); {L03} Def 3.5 (l.92)",
    "c017 'as in M4 Lesson 1' matches L02 l.57 and the Uses line; c020 Remark 2.3 (l.72); c043 Definition 3.5 (l.92) and its use of Lesson 2 Definition 2.2 (l.92).")

verdict = "PASS" if all(r["status"] == "PASS" for r in rows) else "FAIL"
notes = (
    "Slice d = ALL 174 cards in course/modules/PC/PC3/cards.json against L01-L06, round 12, pin 5db69a9b (base 11d7077a = round-11 pin). "
    "Delta since the base: cards.json (PC3-c082 front reworded; PC3-c087 basis reworded), L04.html (l.181 lab docstring, l.576 E2 solution), "
    "L05.html (l.147 Remark 3.4, now 'At step k+1'), L06.html (l.52, l.91 Prop 2.1 name, l.149 Example 4.2, l.165-168 lab docstring, l.320 misconception), "
    "tests/labs/PC3 L04-1 and L06-1, plans/PC3-build-plan.md. The round-11 FAIL (cards-block-091-100, PC3-c092 vs L05 l.147) is fixed in this pin and re-verified PASS. "
    "L01-L03, index, project.html and the grader were not part of the slice's text; their hashes were not used for any card. "
    "Because cards.json and L04-L06 changed, every row was re-verified from scratch by reading all 174 cards and all six lessons in full. No row is carried from round 11. "
    "No published fact is cited, so no UNVERIFIABLE row arises. Mutants: none, because slice d holds no grader; grader mutation is for project slices. "
    "Not run: the full pytest suite and the curriculum/site gates (render_curriculum, build_site --check, fetch_data --check), which are outside cards-vs-lessons; live verify_refs (offline only). "
    "Non-blocking observations for other slices: (a) L05 quiz l.508-512 states 'a single step of the deque removes k-1 entries' as the premise; Remark 3.4 shows a step can remove k, so the premise is wording to check; "
    "(b) L06 uses A for the annuity factor while A1-A5 are assumption labels; (c) plan §9 grade wording for the fair-game definition (see cards-plan-grade-c043)."
)
ledger = {
    "unit": "PC3",
    "slice": "PC3-d",
    "round": 12,
    "verifier": "Claude Haiku 5.5, independent verifier, slice d (ALL cards.json against the lessons), round 12; did not build PC3",
    "pin": "5db69a9bee460736c318ebfacc7200ee5a6eb0f0",
    "base": "11d7077a290f7960b183d3a5a6631af4773888f9 (round-11 pin; round-11 fragment /Users/billyribeiro/.fanout/frags/E-PC3-d.round11.json read as context only)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE12-PC3-d",
    "scratch": "/tmp/pc3d_r12 (stripped line-numbered lesson dumps L01.txt..L06.txt; regenerated by ledgers/PC3/scripts/PC3-d-r12/strip.py)",
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "verdict": verdict,
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": notes,
    "summary": {
        "rows": len(rows),
        "pass": sum(1 for r in rows if r["status"] == "PASS"),
        "fail": sum(1 for r in rows if r["status"] == "FAIL"),
        "unverifiable": sum(1 for r in rows if r["status"] == "UNVERIFIABLE"),
        "mutants_killed": 0,
        "mutants": 0,
    },
}
with open("ledgers/PC3/PC3-d.json", "w", encoding="utf-8") as fh:
    json.dump(ledger, fh, ensure_ascii=False, indent=1)
    fh.write("\n")
print("rows", len(rows), "verdict", verdict)
