"""Writes ledgers/BK4/BK4-a.json for round 6 (slice a). Evidence strings cite the round-6 scripts and outputs under
ledgers/BK4/scripts/BK4-a-r6/ and the raw line numbers of the pages at pin 4bd8cb9."""
import json
import sys
from pathlib import Path

root = Path(sys.argv[1])
S = "ledgers/BK4/scripts/BK4-a-r6/"
R = []


def row(id_, check, location, status, evidence, fix=None):
    r = {"id": id_, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    R.append(r)


P = "PASS"
# ---- hub index.html (raw lines per ledgers/BK4/scripts/BK4-a-r6/index.txt)
row("BK4a-hub-hours-arithmetic", "2.9-structure hours", "index.html:42,138,140-144,167-174",
    P, "index.txt:42 '35 h lessons · 15 h project (30% of the 50 module hours)'; index.txt:138 five lessons of seven hours; "
       "hours table rows 167-173 are 2+2+3+3+2+2+1 = 15 (row 174 'Total 15'); L01/L02/L03 line 34 '7 study hours' (L01.txt:34, "
       "L02.txt:34, L03.txt:34); check_pages_unit.out 'check_pages BK4: PASS'.")
row("BK4a-hub-placement-arithmetic", "2.9-structure placement bar", "index.html:71-131",
    P, "index.txt:71: eight questions, bar 80 percent, 8 x 0.8 = 6.4 so seven correct needed; 6/8 = 75 %, 7/8 = 87.5 %. Eight items "
       "present: prerequisite items at 74, 83, 88, 93, 102, 111 (six) and skill checks at 120, 125 (two). data-mastery=\"0.8\" "
       "and two data-skill items in index.html (grep).")
row("BK4a-hub-placement-keys", "2.9-prose answer keys", "index.html:74-131",
    P, "Re-derived each key: 110/1.1 = 100 (index.txt:80); 1+1/2+1/4 = 1.75 (line 85); lim 2x at 3 = 6 (line 90); Bertrand "
       "equilibrium = c (line 99); grade C = working paper / single sample, matching BLUEPRINT.md:161 (line 108); FC1 lifecycle "
       "order entry, matching, trade capture, clearing, settlement, position update (line 117) matches FC1 L05 text "
       "(course/modules/FC/FC1/L05.html 'This lesson uses six states, in this order'); rung 1: min(120-100, 50) = 20 (line 122); "
       "rung 2: remainder to the first survivor (line 131) matches L03.txt Definition 1.1 rule.")
row("BK4a-hub-prereq-chain", "2.11-dag prerequisites", "index.html:35,61; curriculum/02-economics-finance-core.yaml:367,1075",
    P, "yaml:1075 BK4 prereqs [FC1]; yaml:367 FC1 prereqs [P0.1, E1]; yaml:18-22 E1 prereqs [M2]; curriculum/01-foundations.yaml:126 "
       "M2 prereqs [M1]. So FC1 -> E1 -> M2 -> M1 holds, and index.txt:35 'which assumes P0.1 and E1, and through them M1' is true.")
row("BK4a-hub-P0.1-link", "2.9-prose status", "index.html:35", P,
    "index.txt:35 'P0.1 is not yet released in this program'; 'ls course/modules/P' -> No such file or directory (round 6, "
    "ls of course/modules at pin 4bd8cb9).")
row("BK4a-hub-financial-intermediary", "2.11-dag prerequisite list", "index.html:61-66",
    P, "The round-5 hub list item on financial intermediaries is no longer present (index.txt:61-66 lists three FC1 concepts: "
       "clearing and settlement, the trade lifecycle, bank money creation). Each is used: L01.txt:37 'Uses: clearing and "
       "settlement and the trade lifecycle from FC1' and L04.html:38 'Uses: settlement cycle, bank money creation'. No claim "
       "about financial intermediaries remains.")
row("BK4a-hub-bertrand-trade-fee", "2.11-dag prerequisite use", "index.html:65 against index.html:92-99",
    P, "The round-5 sentence that Bertrand competition is used by placement item 4 was removed (index.txt:61-66 now says the "
       "placement diagnostic tests M1, M2 and E1). grep -c Bertrand over index.txt: 4 hits, all in the hub (lines 65, 93, 97, 99); "
       "L01.txt, L02.txt, L03.txt: 0; L04.html, L05.html, project.html: 0 (ledgers/BK4/scripts/BK4-a-r6/checks_a_r6.out, [dag]).")
row("BK4a-hub-concept-anchors", "2.11-dag links", "index.html:63-66; L01.html:37,59,64; L02.html:51,64,81; L03.html:37,67,134",
    P, "links_a_r6.py over 69 hrefs/srcs of the four pages: 0 missing files, 0 missing fragments (links_a_r6.out: 'links checked: 69 "
       "problems: 0'); concepts.html ids clearing-and-settlement, trade-lifecycle, "
       "bank-money-creation exist.")
row("BK4a-hub-ladder-vs-project", "2.6-project ladder (hub description)", "index.html:150-156; project.html:45,54 (changed "
    "in delta at output blocks only)",
    P, "Hub ladder: four-member clearing house with 40 scenario losses (index.txt:152) matches tests/labs/BK4/lab-BK4-project-1.py:9 "
       "(four members, MARGIN dict) and :49-51 (40 losses from a seeded generator). Rung 2 completion with two blanks (index.txt:153) "
       "matches project.html ladder text (sed of project.html lines 40-56: 'two blanks, the survivor share and the sizing index'). "
       "The project.html delta (7376a5e..4bd8cb9) touches only lab output blocks, lines 200-464, not the ladder.")
row("BK4a-hub-data-status", "2.8-data", "index.html:37,182; tools/data_sources.yaml:19,53,91",
    P, "index.txt:37 'Data: none ...'; index.txt:182 'No data is used in BK4'. grep of tests/labs/BK4/lab-BK4-L01-1.py, "
       "L02-1, L03-1 for open(, urllib, socket, requests, http: no hits (round 6). tools/data_sources.yaml unchanged since pin "
       "7376a5e (git diff --quiet).")
row("BK4a-hub-reading-list", "2.1 citations", "index.html:186-194,193; references/references.json:2853,7411,2815",
    P, "references.json: bisndcpmi (issuer, index page, used_by BK4), duffie2011central (Duffie, Zhu; 2011; Review of Asset Pricing "
       "Studies 1(1), pages 74-95; DOI 10.1093/rapstu/rar001; crossref; title 'Does a Central Clearing Counterparty Reduce "
       "Counterparty Risk?'), bisndbasel (BK1 only). index.txt:191 says the curriculum lists three sources, two on the list, and the "
       "SEC rule is not stated. references.json unchanged since 7376a5e.")
row("BK4a-hub-process-words", "2.9-banned / process words", "index.html (visible text)", P,
    "checks_a_r6.out [words] index: no banned or process hits (TODO, TBD, lorem, builder, verifier, fixer, planner, REQUEST, "
    "ledger, round). Ellipsis count 0.")
# ---- L01
row("BK4a-L01-numbers", "2.2-numbers", "L01.html:254-285; 286; 409; 55", P,
    "rederive_a_r6.py (seed 20260 generator reproduced; need by brute-force scan; net, debit, gross) -> rederive_a_r6.out: "
    "B1 need 112500 net +379800 debit 0; B2 need 1533900 net -1533900 debit 1533900; B3 need 0 net +1154100 debit 0; "
    "gross 2841600; moved 1533900; ratio 0.5398015202... (0.5398; 53.98 %). Every printed value equals the lab output block "
    "(block_compare_a_r6.out). The sentence 'Their ratio ... 0.5398 rounded to four places from 0.53980152' is correct.")
row("BK4a-L01-prop-2.2-2.4", "2.4-mathematics", "L01.html:84-111; 114-126", P,
    "Prop 2.2 (need = max(0, -min_k S_{i,k})) proof re-read (L01.txt:85-90); Prop 2.3 proof (L01.txt:95-100) uses A1 and s != r; "
    "Prop 2.4 proof (L01.txt:105-110): k = m in the minimum gives mu <= Net, so Need >= Debit; strictness via Example 2.6 "
    "(Need_A 100 > Debit_A 50) checked by hand.")
row("BK4a-L01-P2-iff", "2.4-mathematics", "L01.html:375-377", P,
    "P2 claim Need = Debit iff (min S >= 0) or (S_m = min S) re-derived by cases on mu: mu >= 0 -> both 0; mu < 0 and S_m = mu -> both -mu; "
    "mu < 0 and S_m > mu -> Need -mu, Debit 0 or -S_m < -mu. Hypotheses listed (mu <= S_m, Prop 2.2, Assumption 1.3). L01.txt:377.")
row("BK4a-L01-examples-remarks", "2.4-mathematics", "L01.html:119-126", P,
    "Example 2.6 (L01.txt:120): running sums A: 0,-100,-100,-50; B: 0,100,20,20; C: 0,0,80,30; Need_A 100, Debit_A 50, DNS total 50, gross 230 "
    "- all re-derived. Remark 2.7 (L01.txt:125): A sums 0,50,-50,-50, Need 50.")
row("BK4a-L01-problems-M-P-E-R", "2.4/2.5 problem solutions", "L01.html:343-434", P,
    "M1 (300,-500: need 200, debit 200), M2 (doubled: 200, 100), M3 (0,40,-30,-20 with 40/70/10: need 30, debit 20), P1, P3 (scaling), "
    "E1 (Bank B 1533900), E2 (1 of 3, Bank A 112500 vs 0), E3 (1533900/2841600 = 53.98 %, base gross, half-up), R1, R2 "
    "(Debit sum = Net^+ sum; each Net^+ <= inflow, inflows sum to gross), R3 (100/100/100 cycle: Need_A 100, all debits 0). "
    "Each re-derived by hand and cross-checked with rederive_a_r6.out.")
row("BK4a-L01-remark-3.1-order", "2.4-mathematics", "L01.html:300; 432-434", P,
    "Remark 3.1 (L01.txt:300): inflows first gives running minimum min(0,Net), so Need = Debit; S_{i,k} changes only at payments "
    "to or from i. Consistent with R1 (L01.txt:420).")
row("BK4a-L01-R3", "2.4-mathematics", "L01.html:432-434", P,
    "R3 (L01.txt:432-434): Net_i = 0 for all three banks; A's sums 0,-100,-100,0; Need_A = 100; each debit 0.")
row("BK4a-L01-remark-2.8", "2.5-lab statements", "L01.html:291 against lab output L01.html:269-279", P,
    "L01.txt:291 says Part B prints the inequality of Prop 2.4 per bank and Part C the zero sum (lab lines 233-235, 274-275 print "
    "'net positions sum to zero: True' and 'RTGS need is at least ...: True').")
row("BK4a-L01-interp-three-inequalities", "2.5-lab interpretation", "L01.html:286 against lab output 269-279", P,
    "L01.txt:286: Bank B need = debit = 1533900 (output line 270); Bank A net +379800, debit 0, need 112500 (line 269); Bank C 0 (line 271); "
    "Part C totals 1533900 and 2841600 (lines 276-277); 'banks with positive debit: 1 of 3' (line 278); all re-derived.")
row("BK4a-L01-misconception-1", "2.9-misconceptions", "L01.html:322 against lab Part B L01.html:269-271", P,
    "L01.txt:322: 'cannot raise the need of a net receiver' (DNS debit 0 <= RTGS need by Prop 2.4) and 'can lower' (Bank A 112500 vs 0); "
    "'does not remove the need for a net payer' (Bank B need = debit = 1533900, Def 2.1 and A2). Matches output lines 269-270.")
row("BK4a-L01-misconceptions-2-3", "2.9-misconceptions", "L01.html:326,330", P,
    "L01.txt:326: Bank A net +379800, debit 0, RTGS need 112500 (output line 269) and Prop 2.4 strict. L01.txt:330: Remark 2.7 "
    "A's need 100 -> 50, net debit 50 unchanged (Example 2.6, Remark 2.7 re-derived).")
row("BK4a-L01-quiz", "2.9-quiz", "L01.html:463-534", P,
    "All ten quiz keys re-derived: 200 (net -200); 200 (receive 300 then pay 500); the inequality (Prop 2.4); doubling 200 "
    "(Problem M2/P3); 50 (Remark 2.7); sum of nets zero; debit of +50 is 0; lag 'one business day, a lab parameter'; "
    "2841600 cents = 28416 dollars; T+1 'named, not made'. Ten items (L01.txt:463-534).")
row("BK4a-L01-lab-twin", "2.5-labs", "L01.html:128-287; tests/labs/BK4/lab-BK4-L01-1.py", P,
    "block_compare_a_r6.py -> block_compare_a_r6.out: L01 code==twin True; expected==output True (32 lines); twin run "
    "python3 -I -W error from /tmp: exit 0, stderr 0 bytes; last line main(); no __name__ guard. run_labs_a_r6 (gates "
    "run_labs.out) 'run_labs BK4: PASS (8/8)'.")
row("BK4a-L01-notation", "2.4 notation (notation.json)", "L01.html, L02.html, L03.html, index.html math spans", P,
    "checks_a_r6.out [notation]: 740 math spans; macros used exclude every registered symbol; no \\mathbb{R}, T, \\Phi, \\gamma, "
    "\\Var, \\E, \\Cov, \\Corr, \\Prob, \\mathbb{Q}, R^\\ast, R_f, \\SR, \\N, \\emgamma hits (all 0). Local symbols (S_{i,k}, Net, Debit, "
    "Need, o_i, mu, m, d, k, L_s, IM, DF, K, delta, ell, V) are defined on the lesson where they first appear.")
row("BK4a-L01-dag-defs", "2.11-dag / define before use", "L01.html:37,59,64; index.html:68", P,
    "checks_a_r6.out [dag] L01: no out-of-closure concept name in visible text (D1-D13 terms). data-concept on L01 only payment-system "
    "and settlement-cycle dfn (L01.html:59,64) and two concept links (clearing-and-settlement, trade-lifecycle, L01.html:37).")
row("BK4a-L01-why-words", "2.9-prose length", "L01.html:51", P,
    "checks_a_r6.out [why] L01: 107 words (limit 120). Text read at L01.txt:51.")
row("BK4a-L01-structure", "2.9-structure", "L01.html:34-545", P,
    "check_pages_L01.out (round 6): 'check_pages BK4 L01: PASS'. Sections 1-9 present; three misconceptions (L01.txt:321-330); "
    "problem sets M1-M3, P1-P3, E1-E3, R1-R3; key results table (446-452); quiz 10 items (463-534); references (541).")
row("BK4a-L01-grades", "2.3-grades", "L01.html:43-48, 84, 94, 104, 446-452", P,
    "Legend (L01.txt:43-48) matches BLUEPRINT.md:156-163 (T theorem, A replicated, B published, C working paper/practitioner/single "
    "sample, D lore, X refuted). Claims: T for proved results (446-449), T for hand examples (450), C with lab named for lab "
    "results (451-452).")
row("BK4a-L01-FC1-claim", "2.9-prose cross-reference", "L01.html:55", P,
    "L01.txt:55 'FC1 Lesson 5 followed one trade through that sequence.' course/modules/FC/FC1/L05.html:36 title 'Clearing, Settlement "
    "and the Trade Lifecycle'; L05 section 3 'Tracing one trade' lists order entry, matching, trade capture, clearing, settlement, "
    "position update (grep, round 6).")
row("BK4a-L01-canon-breaks-wording", "2.9-prose", "L01.html:308-313", P,
    "L01.txt:308 now 'Four places where the model stops:'; items 310-313 are limits (no queues, the day is given, d is a parameter, "
    "no real-system claim). Re-read in full this round.")
# ---- L02
row("BK4a-L02-prop-2.2", "2.4-mathematics", "L02.html:85-99", P,
    "Prop 2.2 (a)-(d) and proofs (L02.txt:85-98) re-derived: (a) each trade enters one Rec and one Pay (A2); (b) sum n = G - G = 0; "
    "(c) max(0,x) - max(0,-x) = x; (d) 0 <= A <= G since Pay >= 0 and Rec >= 0.")
row("BK4a-L02-prop-2.3-title", "2.4-mathematics", "L02.html:102-103", P,
    "L02.txt:102-103 statement 'A = G iff for every member Rec_i = 0 or Pay_i = 0' and its heading are consistent with the proof (L02.html:108).")
row("BK4a-L02-prop-2.3-proof", "2.4-mathematics", "L02.html:106-109; 348-349 (P2)", P,
    "Full raw text of L02.html:108 read (cases Rec=0; Rec>0 & Pay=0; Rec>0 & Pay>0 with strict inequality); P2 solution (L02.html:349) "
    "gives both directions with hypotheses Pay>=0, Rec>=0 and Prop 2.2(a). Re-derived.")
row("BK4a-L02-example-2.4", "2.2-numbers", "L02.html:113; 270; 294", P,
    "rederive_a_r6.out: Ex2.4 (G 230 dollars, A 50, n = -50, 20, 30, reduction 180, 10000*180/230 = 7826.08 -> 7826). Lab numbers "
    "at L02.html:270 re-derived (rederive_a_r6.out, L02 section). Ex2.4 'Member 1 both receives and pays ... A < G' (L02.html:113) "
    "is consistent with Prop 2.3.")
row("BK4a-L02-lab-claims", "2.5-lab statements", "L02.html:123,127; tests/labs/BK4/lab-BK4-L02-1.py main()", P,
    "L02.txt:127 expected-before-run list equals the printed checks (page output lines 255, 262, 266, 267 read 'True'); twin main() "
    "prints these checks; L02.txt:123 'six trades among four members' matches MEMBERS = 4, TRADES = 6 (twin lines 149-150).")
row("BK4a-L02-lab-numbers", "2.2/2.5 lab numbers", "L02.html:241-269 (expected); 270 (interpretation); 365-381 (E1-E3)", P,
    "block_compare_a_r6.out: L02 expected block equals run output (29 lines). rederive_a_r6.out: trades, receivables, payables, net obligations "
    "-3627000, 1753300, 3340300, -1466600; A = 5093600; reduction 2502700; floor(10000 * 2502700 / 7596300) = 3294 (exact 3294.63). "
    "Interpretation sentences checked against these.")
row("BK4a-L02-lab-numbering", "2.9-structure", "L02.html:121,123,125-127,270", P,
    "Section 3 heading 'Lab 1: netting for one seeded set of trades' and the lab block id lab-BK4-L02-1 agree; the Lab 1 "
    "statements and output labels match.")
row("BK4a-L02-attribution", "2.1 attribution", "L02.html:277,285; references/references.json:7411-7416", P,
    "Round-5 FAIL cleared. L02.txt:277 now reads 'asked by Duffie and Zhu (2011).' with the citation marker directly after the closing "
    "parenthesis (raw L02.html:277 '(2011)<span class=\"ref\" data-cite=\"duffie2011central\">'). L02.txt:285 now reads 'poses the question "
    "at paper level, and this lesson states no answer from it.' The registry (references.json:7411; unchanged since pin 7376a5e) has "
    "authors Duffie, Zhu, year 2011, title 'Does a Central Clearing Counterparty Reduce Counterparty Risk?', so the attribution of the "
    "question to the paper's title is supported at paper level. The claim that no answer is stated is true (no finding in L02). "
    "live verify_refs was not re-run this round (offline integrity only; see BK4a-gate-verify-refs).")
row("BK4a-L02-canon-misconceptions", "2.9-misconceptions", "L02.html:280-285, 293-302", P,
    "L02.txt:280 now 'Four places where the model stops:'; 282-285 are four limits (obligations fixed, CCP flat, default not modelled, no "
    "finding on real clearing houses). Misconceptions 293-302: 'Lab 1, Part D prints a positive netted amount' (5093600), "
    "'Lab 1 prints the amount and moves no money', 'Lab 1, Part C sums to zero' - each matches the output.")
row("BK4a-L02-problems", "2.4/2.2 problem solutions", "L02.html:315-406", P,
    "M1 (n = -10,-20,50,-20; A 50; G 180; 7222 bp), M2 (G 460, A 100, 7826 bp), M3 (n = -200,100,100; A = G = 200; 0 bp), P1, P2, "
    "P3 (cycle: n = 0, A = 0, bp 10000), E1 (5093600; 2502700; 3294), E2 (member 3 +3340300, member 1 -3627000), E3 (members 1, 2, 4 both "
    "receive and pay; A < G; reduction 2502700 > 0), R1 (0 <= bp <= 10000; 10000 iff A = 0), R2 (X: A 10000, G 10000; Y: A 10000, G 20000), "
    "R3 (adding one trade moves A by at most a). All re-derived in rederive_a_r6.out and by hand.")
row("BK4a-L02-key-results", "2.3-grades", "L02.html:416-425", P,
    "L02.txt:418-425: T rows are proved in Section 2 or Problems R1/P3 or hand-worked Example 2.4; C rows name the lab (Lab 1, Parts B to D) "
    "or are question-only (L02.txt:425) and state no answer.")
row("BK4a-L02-quiz", "2.9-quiz", "L02.html:432-510", P,
    "Ten items re-derived: n2 = 20 (Example 2.4); A = 50; 'sum to zero'; 'no member both receives and pays'; reduction 7826; n2 = 100; "
    "A's 'zero sum does not show no default'; 50936 dollars; cycle netted amount zero (Problem P3). L02.txt:436-507.")
row("BK4a-L02-lab-twin", "2.5-labs", "L02.html:121-271; tests/labs/BK4/lab-BK4-L02-1.py", P,
    "block_compare_a_r6.out: L02 code==twin True; expected==output True; twin run python3 -I -W error: exit 0, stderr 0 bytes; main() unconditional.")
row("BK4a-L02-why-structure", "2.9-structure", "L02.html:34-518", P,
    "check_pages_L02.out: PASS; why-it-matters 96 words (checks_a_r6.out [why]); three misconceptions; problem sets M/P/E/R; key results; "
    "quiz 10 items; references (513-514: one registry source at paper level).")
row("BK4a-L02-meta-description", "2.9-prose", "L02.html:7", P,
    "Meta description: 'Novation, the central counterparty and multilateral netting: ... the bound that the netted amount never exceeds the "
    "gross notional. Lab 1 on a seeded SIMULATED set of four members' - consistent with Prop 2.2(d) and Lab 1.")
# ---- L03
row("BK4a-L03-legend", "2.3-grades", "L03.html:43-48", P, "L03.txt:43-48 legend matches BLUEPRINT.md:156-163.")
row("BK4a-L03-four-resources", "2.9-prose", "L03.html:55; 418", P,
    "L03.txt:55 defines the four resources and says the loss is one input; the close-out limit is named in Section 3 (L03.txt:418 "
    "'No close-out period is modelled').")
row("BK4a-L03-notation-d", "2.4 notation", "L03.html:61,69-71,100,139,480-482", P,
    "checks_a_r6.out [notation] L03: 375 math spans, no registered symbol. Local symbols IM_i, DF_i, K, L_s, S, k, c, t, delta, ell, "
    "V are defined where first used (L03.txt:55-61, 66-71, 134-146).")
row("BK4a-L03-def-props-1.2-1.3", "2.4-mathematics", "L03.html:66-96 (Def 1.1, Prop 1.2, Prop 1.3)", P,
    "Round-5 FAIL cleared. Prop 1.2 (L03.txt:76-80) now states a1+a2+a3+sum_{i in V} y_i+u = L with y_i defined: DF_i when Z>=D; x_i+1 "
    "for the first ell survivors with DF_i>0 and x_i otherwise when Z<D. Definition 1.1 (L03.txt:66-73) gives the same leftover rule "
    "(first ell survivors in ascending id with DF_i>0). Proof (L03.txt:85): Z<D case sums y_i = sum x_i + ell = Z. Prop 1.3 (L03.txt:90-95) "
    "re-read in full: ell >= 0 (fractional parts), ell <= n+ - 1 (integer, each part < 1), x_i + 1 <= DF_i. Round-5 counterexample "
    "(Z=1, three DF=1 survivors) now gives y = (1,0,0), sum 1 = L (rederive_a_r6.out 'remainder 1').")
row("BK4a-L03-remark-1.4", "2.4-mathematics", "L03.html:100-101", P,
    "Remark 1.4 (L03.txt:100): a2>0 => a1 = IM; a3>0 => a2 = DF; Z>0 => a3 = K. Proof checks out (min below L forces second argument).")
row("BK4a-L03-example-1.5", "2.2-numbers", "L03.html:104-121; table 108-117; lab Part A1 output L03.html:386-393", P,
    "Example 1.5 values (a1 100, a2 50, a3 30, Z 20; 8 and 12; L=300 uncovered 20; L=181 leftover to member 1) and the eight table rows "
    "(loss, margin, DF, capital, member 1, member 2, uncovered) equal rederive_a_r6.out 'fixture' rows and lab Part A1 output.")
row("BK4a-L03-example-1.6", "2.2-numbers", "L03.html:124-126; lab Part A2 output L03.html:397-398", P,
    "Example 1.6 (D = 3; Z=1 -> member 1 pays 1; Z=2 -> members 1 and 2 pay 1 each) equals lab output and rederive_a_r6.out 'remainder 1/2'.")
row("BK4a-L03-def-2.1-prop-2.3", "2.4-mathematics", "L03.html:133-165", P,
    "Def 2.1 (count basis, floor in bp, not dollar-weighted). Prop 2.3 proof Parts 1-3 (L03.txt:162-164) re-derived: k in [1,S]; "
    "floor(y) >= t iff y >= t; c(M) >= k iff M >= L_(k) by sorting. Statement and proof agree.")
row("BK4a-L03-cor-2.4-ex-2.5", "2.4-mathematics; 2.2-numbers", "L03.html:168-181; lab Part B output L03.html:404-409", P,
    "Corollary 2.4 proof (L03.txt:173-175) and the weak inequality M(t) <= M(t') are correct (ceil does not decrease). Example 2.5: "
    "9900*200/10000 = 198 exactly, 9975*200/10000 = 199.5 (k = 200), printed margins 2961 and 2992 (rederive_a_r6.out: k 198, sorted[197] = 2961; "
    "k 200, sorted[199] = 2992; brute-force agreement). The heading wording is a separate row (BK4a6-L03-corollary-heading).")
row("BK4a-L03-R1-note", "2.4-mathematics", "L03.html:529-533", P,
    "R1 (real margins): the argument of Prop 2.3 Part 2 uses only that M is real; the answer is L_(k) and is attained. Re-derived.")
row("BK4a-L03-canon-bullet-6", "2.9-prose / 2.4 scope", "L03.html:421", "FAIL",
    "L03.txt:421 (canon-breaks bullet 'A low target leaves a tail'): 'At 9900 basis points and S = 200, the two largest scenarios are above "
    "the sized margin.' This is not true for every sample: the sized margin is L_(198), and the two largest are above it only when "
    "L_(198) < L_(199). Counterexample: 200 losses where the 198th, 199th and 200th smallest are all 1000 cents (others smaller): the sized "
    "margin is 1000, the cover at 1000 is 10000 bps, and no scenario lies above the margin. Lab 1's seed happens to give L(198)=2961 < "
    "L(199)=2981 (rederive_a_r6.out), so the claim holds for the printed draw only. The sentence states a general claim without its hypothesis "
    "(BUILDER_RULES 2.1 item 6; VERIFIER 2.4).",
    "L03.html:421: qualify the sentence, e.g. 'At 9900 basis points and S = 200, the sized margin is L_(198), and the number of scenarios above "
    "it is 200 minus the count at that margin: exactly two when L_(198) < L_(199), as in Lab 1 Part B, and fewer when the two losses tie'. "
    "Regenerate the page; the lab is unchanged.")
row("BK4a-L03-misconceptions", "2.9-misconceptions", "L03.html:426-445", P,
    "Four misconceptions (L03.txt:429-442): Remark 2.2 at L=M; cover is a count (Example 2.5 k = 198); Remark 1.4 and Lab Part A3 scenario "
    "1529 (margin only, default fund 0, capital 0) match output line 400; Def 1.1 uses DF_i, survivors' IM do not appear.")
row("BK4a-L03-problems", "2.4/2.2 problem solutions", "L03.html:454-546", P,
    "M1 (200: layers 100/50/30, Z 20, 8 and 12, total 200); M2 (cover 7500 bp; k = 3; margin 3000; cover(2999) = 5000); M3 (k = 4, 5, 5; "
    "margins 40, 50, 50); P1 (Remark 1.4 steps), P2 (ceil in range), P3 (monotone c(M); cover 10000 at max loss), E1 (3160: margin 3058, "
    "DF 102), E2 (857 = D/2; 312/381/164 = DF/2; no leftover), E3 (c = 198; 2 above), R1, R2 (S = 100: k = 99 or 100; at most one above), R3 "
    "(S < 400 gives k = S; S = 400 gives k = 399). All re-derived.")
row("BK4a-L03-key-results", "2.3-grades", "L03.html:556-565", P,
    "Rows 558-563 T (proved); 564 C (Lab 1 Parts A1, A2, fixed fixture, not seeded); 565 C (Lab 1 Part B seeded SIMULATED). Row 563 "
    "'does not fall' is correct (Cor 2.4 is non-strict). Row 564 'fixed fixture, not seeded' contradicts the twin docstring (see BK4a6-L03-lab-docstring-seed).")
row("BK4a-L03-quiz", "2.9-quiz", "L03.html:571-646", P,
    "Ten items re-derived: 'the default fund' after the margin (Def 1.1); 8 cents (Example 1.5); 'two survivors pay 20' (residual 20); "
    "'Yes, because the count uses L_s <= M'; cover(4000) = 7500; k = 3; 50 cents for 8001 (k = 5), 40 for 8000; first survivor 1 cent; "
    "198 of 200 (the margin covers 198 in full); k = 399 for 9975 at 400 scenarios. L03.txt:576-643.")
row("BK4a-L03-lab-twin", "2.5-labs", "L03.html:187-411; tests/labs/BK4/lab-BK4-L03-1.py", P,
    "block_compare_a_r6.out: L03 code==twin True; expected==output True (28 lines); twin run python3 -I -W error exit 0, stderr 0 bytes; "
    "main() unconditional. The twin docstring defect is a separate row (BK4a6-L03-lab-docstring-seed).")
row("BK4a-L03-why-structure", "2.9-structure", "L03.html:34-657", P,
    "check_pages_L03.out PASS; why-it-matters 118 words (limit 120); canon-breaks section (L03.txt:416-420); misconceptions 4; problem "
    "sets M1-M3, P1-P3, E1-E3, R1-R3; key results; quiz 10 items; references (650: no registry key).")
row("BK4a-L03-uses-meta", "2.9-DAG", "L03.html:37", P,
    "'Uses: central counterparty and multilateral netting (L02); the algebra of integer sums and floors' - both defined in L02 (links "
    "resolve, links_a_r6.out).")
# ---- gates
row("BK4a-gate-check-pages", "gate", "tools/check_pages.py --unit BK4; --page L01/L02/L03", P,
    "check_pages_unit.out: 'check_pages BK4: PASS' (exit 0, covers index, L01-L03, project). --page L01, L02, L03: PASS. "
    "A '--page index' run was made by mistake: --page selects lesson pages only and reported the hub as lesson content (check_pages_index.out, "
    "exit 1); the hub is checked by the unit run, which passes.")
row("BK4a-gate-check-dag", "gate", "tools/check_dag.py --unit BK4", P, "check_dag.out: 'check_dag BK4: PASS' (exit 0).")
row("BK4a-gate-run-labs", "gate", "tools/run_labs.py --unit BK4", P, "run_labs.out: 'run_labs BK4: PASS (8/8)' (exit 0).")
row("BK4a-gate-page-smoke", "gate", "tools/page_smoke.py --unit BK4 --pages index L01 L02 L03", P,
    "page_smoke_a_r6.out (run alone): index, L01, L02, L03 each PASS; lab runtimes 0.0 s; 'page_smoke BK4: PASS' (exit 0).")
row("BK4a-gate-ruff-mypy", "gate", "tests/labs/BK4 ruff and mypy", P,
    "ruff_check_labs.out 'All checks passed!'; ruff_format_labs.out '8 files already formatted'; mypy_labs.out 'Success: no issues found in "
    "8 source files' (mypy --no-incremental). Repository-wide ruff/mypy were not re-run this round (outside slice a).")
row("BK4a-gate-pytest-labs", "gate", "tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py", P,
    "pytest_a_r6.out: all dots, exit 0.")
row("BK4a-gate-verify-refs", "gate", "tools/verify_refs.py --offline", P,
    "verify_refs_offline.out: 'offline integrity: 560 entries, 0 problems'. A live '--unit BK4' run was not repeated this round.")
row("BK4a-banned-and-process", "2.9-banned", "index.html, L01-L03", P,
    "checks_a_r6.out [words]: no banned or process-word hits on the four pages; ellipsis count 0.")
row("BK4a-scope-words", "2.4 scope words", "L01-L03, index (about 300 scope-word hits)", P,
    "Every universal or scope word in visible text was listed by context (round 6) and each is covered by a computation, a proof or a "
    "stated hypothesis, except the one at L03.html:421 (row BK4a-L03-canon-bullet-6). Examples checked: 'for every bank' (Prop 2.4, "
    "proved); 'every payment is an inflow to exactly one bank' (A2); 'the basis-point figure is unchanged when every amount is multiplied' "
    "(scaling; L02.txt:194); 'every net obligation is zero' for cycles (P3).")
row("BK4a-hub-settlement-framing", "2.9-prose / B1 settlement facts", "index.html:33", P,
    "index.txt:33 'In this unit's model, a trade settles when its payment has moved between accounts.' The payment systems are "
    "defined in Lesson 1 and the clearing houses in Lesson 2; no settlement rule is stated as a fact (no admitted source, B1). "
    "Round-4 FAIL cleared; round-5 PASS re-verified on the same line.")
row("BK4a-hub-P0.1-grade-source", "2.3-grades / prose", "index.html:108", P,
    "index.txt:108 'Grade C is the grade for a working paper, practitioner research or single-sample evidence (P0.1, evidence grade).' "
    "matches BLUEPRINT.md:161. (Round 5 cited line 110; the hub lost two lines in the round-5 fix, so the line is now 108.)")
row("BK4a-hub-card-L02", "2.9-hub lesson map", "index.html:141", P,
    "index.txt:141 'L02 · 7 h Central Counterparties and Multilateral Netting ... checked in Lab 1 on seeded SIMULATED trades' matches "
    "L02.html title and lab description.")
row("BK4a-L01-canon-bullet-only-designs", "2.9-prose", "L01.html:313", P,
    "L01.txt:313 'the two designs are defined in Definitions 1.1 and 2.1' now agrees with L01.txt:59 (the rest of Definition 1.1 defines the "
    "designs; Section 2 measures them).")
row("BK4a-L01-A2-forward-ref", "2.9-prose", "L01.html:71; 79-80", P,
    "A2 (L01.txt:71) refers forward to Definition 2.1 for the net debit, with a pointer, not a use before definition.")
row("BK4a-L01-R1-order-claim", "2.4-mathematics", "L01.html:420", P,
    "R1 solution (L01.txt:420) cites Remark 3.1 and Prop 2.4; the order-independence of the debit (Remark 2.5) is used correctly.")
row("BK4a-rederive-r4", "2.2 independent re-derivation", "ledgers/BK4/scripts/BK4-a-r6/rederive_a_r6.py -> rederive_a_r6.out", P,
    "Independent round-6 re-derivation (stdlib, python3 -I): L01 day from seed 20260 (need by brute force, net, debit), L02 trades from seed "
    "2026 (rec, pay, n, A, bp), the netting examples (Ex 2.4, M1, M2, M3, P3, R2), L03 fixtures (Example 1.5 table, Example 1.6), A3 "
    "scenarios (1529, 3160, 5850 with layers and survivor shares), Part B margins 2961 and 2992 with brute-force agreement. Every printed "
    "number on the four pages in slice a was compared with this output.")
row("BK4a-lab-block-equality-r4", "2.5 lab blocks", "ledgers/BK4/scripts/BK4-a-r6/block_compare_a_r6.py -> .out", P,
    "block_compare_a_r6.out: for L01, L02, L03 the page code block equals the twin (rstrip per line) and the expected block equals the "
    "output of python3 -I -W error on the twin; exit 0; stderr 0 bytes; main() unconditional.")
row("BK4a-gate-repo-ruff-mypy-r4", "gate", "tests/labs/BK4 (slice-scope ruff/mypy)", P,
    "Covered by BK4a-gate-ruff-mypy: twins only. Whole-repository ruff and mypy were not re-run in round 6 because no file outside "
    "tests/labs/BK4 and course/modules/BK/BK4 is in slice a.")
row("BK4a5-L01-lede-settlement-framing", "2.1 / B1 settlement facts", "L01.html:51", P,
    "Round-5 FAIL cleared. L01.txt:51 now reads 'In the model used here, a trade is paid for when the payment behind it settles, and a bank "
    "that sends a payment needs money in its account to make it.' The qualifier now governs the first clause.")
row("BK4a5-L01-designs-pointer", "2.9-prose cross-reference", "L01.html:59", P,
    "Round-5 FAIL cleared. L01.txt:59 now reads 'It has two designs, which the rest of this definition defines and Section 2 measures.' "
    "The same definition defines RTGS and DNS (L01.txt:59) and Section 2 defines the measures (Definition 2.1). Consistent with L01.txt:313.")
row("BK4a5-L01-canon-heading", "2.9-prose", "L01.html:308", P,
    "Round-5 FAIL cleared. L01.txt:308 now 'Four places where the model stops:'; the four items (310-313) state limits, not actions.")
row("BK4a5-L02-canon-heading", "2.9-prose", "L02.html:280", P,
    "Round-5 FAIL cleared. L02.txt:280 now 'Four places where the model stops:'; the four items (282-285) state limits.")
row("BK4a5-hub-prereq-uses", "2.9-prose / 2.11-dag", "index.html:61-66", P,
    "Round-5 FAIL cleared. index.txt:61 now 'BK4 uses these FC1 concepts without redefining them:' and lists only FC1 concepts, each used "
    "(see BK4a-hub-financial-intermediary). index.txt:65 says the placement diagnostic tests M1, M2 and E1 and that no lesson or project "
    "uses present value, the geometric series, the limit or Bertrand competition. checks_a_r6.out [dag] (index, L01-L03) and [hub-claim] (L04, L05, project): present value, geometric and Bertrand have 0 hits outside the hub; 'limit' occurs only as the ordinary word (a stated limit; limits of the simulator), not the concept.")
row("BK4a5-links-anchors", "2.9-links", "index.html; L01.html; L02.html; L03.html (all hrefs)", P,
    "links_a_r6.py: 'links checked: 69 problems: 0' (every local target and fragment resolves; concepts.html ids exist).")
row("BK4a5-twins-alone", "2.5-labs", "tests/labs/BK4/lab-BK4-L01-1.py, lab-BK4-L02-1.py, lab-BK4-L03-1.py", P,
    "block_compare_a_r6.out: each twin run alone as python3 -I -W error from /tmp: exit 0, stderr 0 bytes. grep for open(, urllib, socket, "
    "requests, http in the three twins: no hits (round 6).")
# ---- new row: twin docstring
row("BK4a6-L03-lab-docstring-seed", "2.5 labs (docstring claim vs code)", "tests/labs/BK4/lab-BK4-L03-1.py:3 (docstring); "
    "course/modules/BK/BK4/L03.html:192 (copy in page code block)", "FAIL",
    "The twin docstring line 3 says 'Every input is generated from a fixed seed, so the inputs are SIMULATED'. Part A1 uses literal "
    "fixture dicts fixture_im = {1: 0, 2: 0, 3: 100} and fixture_df = {1: 40, 2: 60, 3: 50} and the literal loss list (80, 120, 170, 180, 181, "
    "200, 205, 300); Part A2 uses literal {1: 1, 2: 1, 3: 1, 4: 0} and losses (1, 2). The page at L03.txt:189 correctly says Part A1 runs "
    "'the fixture of Example 1.5', and the docstring itself says Part A runs 'a fixture with hand-checkable amounts'. The claim in the "
    "docstring is contradicted by the code (grep of the twin: fixture_im, fixture_df, literal loss tuples).",
    "tests/labs/BK4/lab-BK4-L03-1.py lines 3-4: replace 'Every input is generated from a fixed seed, so the inputs are SIMULATED and "
    "every run prints the same numbers.' with 'The inputs of Parts B and A3 come from a fixed seed, so they are SIMULATED and every run "
    "prints the same numbers; the inputs of Parts A1 and A2 are the fixtures stated on the page.' Then re-embed the twin with "
    "tools/embed_labs.py course/modules/BK/BK4/L03.html --refresh lab-BK4-L03-1 so that the page code block equals the twin (the expected "
    "block does not change, because printed output is unchanged).")
# ---- new row: corollary heading
row("BK4a6-L03-corollary-heading", "2.9-prose (heading vs statement)", "course/modules/BK/BK4/L03.html:168", "FAIL",
    "Heading 'Corollary 2.4 (the sized margin rises with the target)' claims an increase, but the statement at L03.html:169 is the "
    "non-strict inequality M(t) <= M(t'), and the proof (L03.txt:173-175) gives only non-decreasing sizes. Key-results row 563 "
    "(L03.txt:563) correctly says 'does not fall'. The heading claims more than the statement proves (a constant margin for two targets "
    "is allowed by the statement, e.g. two targets with equal k-th losses).",
    "L03.html:168: change the heading to 'Corollary 2.4 (the sized margin does not fall as the target rises)'.")

assert len(R) == len({r["id"] for r in R}), "duplicate ids"
nonpass = [r["id"] for r in R if r["status"] != "PASS"]
counts = {"rows": len(R), "pass": sum(r["status"] == "PASS" for r in R), "fail": len(nonpass), "unverifiable": 0}
frag = {
    "unit": "BK4",
    "slice": "BK4-a",
    "round": 6,
    "round_note": ("Round 6 of BK4-a (hub index.html, L01, L02, L03, lab twins 1-3), pin 4bd8cb9 (previous pin 7376a5e, round-5 "
                   "fragment /Users/billyribeiro/.fanout/frags/E-BK4-a.round5.json). Delta 7376a5e..4bd8cb9 for the slice: index.html "
                   "lines 61-66 (prerequisite list), L01.html 51, 59, 64, 308, 330; L02.html 273, 277, 280, 285; L03.html 51, 76-80 "
                   "(Prop 1.2), and the L03/L01/L02 changed-only prose. The three twins are byte-identical to the previous pin (not in "
                   "the delta). Every page in the slice was read in full as raw-line text (ledgers/BK4/scripts/BK4-a-r6/index.txt, L01.txt, "
                   "L02.txt, L03.txt) and every number and claim was re-derived; no row relies on the round-5 PASS without a fresh "
                   "citation. The round-5 non-PASS rows are re-verified and now PASS (BK4a-L02-attribution, BK4a-L03-def-props-1.2-1.3, "
                   "BK4a5-L01-lede-settlement-framing, BK4a5-L01-designs-pointer, BK4a5-L01-canon-heading, BK4a5-L02-canon-heading, "
                   "BK4a5-hub-prereq-uses). Every round-5 id is kept."),
    "verifier": "Haiku independent verifier, BK4-a round 6 (did not build BK4)",
    "pin": "4bd8cb94a8e171e80c4c34da1b3f32be7cb93f07",
    "base": "7376a5e216c1e6d99becc76b4cd64028f5b55d3f (round-5 pin)",
    "checkout": str(root),
    "scratch": str(root / "ledgers/BK4/scripts/BK4-a-r6"),
    "verified_at": "2026-11-04",
    "verdict": "PASS" if not nonpass else "FAIL",
    "rows": R,
    "mutants": [],
    "registry_flags": [
        "SEC T+1 settlement rule (curriculum yaml:1092): no record in references/references.json (no sec.gov key). Index and lessons state only "
        "that the rule is named, not stated (index.html:191; L01.html:64, :312). Admission via tools/add_reference.py is needed before any "
        "settlement-rule fact (B1).",
        "duffie2011central: the registry title is the question L02 attributes at paper level (references.json:7411). Live verify_refs --unit BK4 "
        "was run in round 5; round 6 ran the offline integrity check only.",
        "bisndcpmi: issuer-level index record (references.json:2853); used at index level only (index.html:191).",
    ],
    "freshness_flags": [],
    "notes": [
        "Verdict FAIL: three rows are non-PASS: BK4a-canon-bullet-6 (L03.html:421, general claim about the two largest scenarios that is false "
        "when L_(198) = L_(199)), BK4a6-L03-corollary-heading (L03.html:168, heading 'rises' for a non-strict inequality), and "
        "BK4a6-L03-lab-docstring-seed (tests/labs/BK4/lab-BK4-L03-1.py:3, 'every input is generated from a fixed seed' contradicted by the Part A1/A2 fixtures).",
        "Row id note: the non-PASS row for L03.html:421 keeps the round-5 id BK4a-L03-canon-bullet-6.",
        "Mutants: none. Slice a has no grader; the lab twins are demonstrations, and mutation testing applies to grader/ only "
        "(FINAL-ARCHITECT-RULINGS 9; plan section 11 item 11). Student-error mutants are not required for this slice.",
        "Hours: arithmetic only (hub 35 + 15 = 50; lessons 7 h each; project components sum to 15). Hours are design targets.",
        "Not checked by this slice: content of L04, L05, project.html, cards.json and the grader (other slices). L04 and L05 are used only "
        "for the hub's prerequisite-use and the 'no lesson uses' scope checks (grep). project.html changed in the delta only in lab output "
        "blocks (lines 200-464); its ladder text is unchanged and was read via sed.",
        "Duffie and Zhu (2011) abstract not read in round 6 (plan B2): the lessons state no finding of the paper, so no statement depends on it.",
        "No network bot checks, logins or access blocks were encountered. Live verify_refs was not repeated in round 6.",
        "Tool note: check_pages --page index is not a valid selector (the hub is checked in unit mode); its exit 1 is an invocation artifact.",
        "Whole-repository ruff/mypy and the full gate were not run by this slice (targeted gates only, per the BK4 slice scope).",
    ],
    "summary": counts,
}
out = root / "ledgers/BK4/BK4-a.json"
out.write_text(json.dumps(frag, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out, counts, "non-pass:", nonpass)
