"""Round 12 fragment builder for BK4 slice a (index, L01, L02, L03, their twins, cards L01-L03).

Writes ledgers/BK4/BK4-a.json. Every round-10 row id is kept (round 10 fragment, /Users/billyribeiro/.fanout/frags/
E-BK4-a.round10.json) and re-evidenced in round 12 from this checkout; no round-10 PASS is carried forward.
Evidence cites the round-12 scripts under ledgers/BK4/scripts/BK4-a-r12/ or a file:line read this round.
"""

import json
import sys

ROOT = sys.argv[1]
CK = "course/modules/BK/BK4"
S12 = "ledgers/BK4/scripts/BK4-a-r12"
R10 = "/Users/billyribeiro/.fanout/frags/E-BK4-a.round10.json"

r10 = json.load(open(R10, encoding="utf-8"))
r10_ids = [r["id"] for r in r10["rows"]]
r10_map = {r["id"]: r for r in r10["rows"]}

P = "PASS"
F = "FAIL"
NUM = f"{S12}/recompute_numbers.out (110 of 110 PASS)"
EMB = f"{S12}/check_embeds.out (page code == twin; expected block == twin stdout, L01-L03)"
RUN = "twins run alone: python3 -I -W error tests/labs/BK4/lab-BK4-L0n-1.py from /tmp, exit 0"

rows: dict[str, dict[str, str]] = {}


def add(rid: str, status: str, evidence: str, fix: str = "", location: str | None = None, check: str | None = None) -> None:
    base = r10_map.get(rid, {})
    rows[rid] = {
        "id": rid,
        "check": check or base.get("check", "2.9-structure"),
        "location": location or base.get("location", ""),
        "status": status,
        "evidence": evidence,
    }
    if status != P:
        rows[rid]["fix"] = fix


# ---------- hub: index.html ----------
add("BK4a-hub-hours-arithmetic", P,
    "Round 12 full read of index.html 1-197. data-hours-lessons=35 (l29), data-hours-project=15 (l29); five lesson cards at 7 h (l140-144); hours table 2+2+3+3+2+2+1=15 (l167-174); split bar 70%/30% (l40). Hours arithmetic recomputed in " + NUM + ".")
add("BK4a-hub-placement-arithmetic", P,
    "Round 12 read index.html 69-133: 8 items (Pq1-Pq6 prerequisites, Pq7-Pq8 labelled skill checks). Mastery 0.8 x 8 = 6.4, so 7 correct needed (l71); 6/8 = 75 %, 7/8 = 87.5 % (l71). Matches l71 text.")
add("BK4a-hub-placement-keys", P,
    "index.html:80 110/1.1 = 100; :85 1+1/2+1/4 = 7/4 = (1-(1/2)^3)/(1/2); :90 lim_{x->3} 2x = 6; :99 Bertrand equilibrium price c; :108 grade C wording; :117 FC1 lifecycle order (FC1 L05.html:63 gives the same six states in order); :122 rung-1 min(120-100, 50) = 20; :131 rung-2 floor(1*1/3) = 0 and first survivor pays the cent. Recomputed in " + NUM + " (idx rows).")
add("BK4a-hub-prereq-chain", P,
    "index.html:35,61 state FC1 assumes P0.1 and E1; E1 assumes M2; M2 assumes M1. curriculum/01-foundations.yaml:91 (M1 prereqs [P0.1]) and :126 (M2 prereqs [M1]); curriculum/02-economics-finance-core.yaml:22 (E1 prereqs [M2]); the FC1 entry (yaml, id FC1) prereqs [P0.1, E1] (read in round 12, lines 360-368). Chain matches the page.")
add("BK4a-hub-P0.1-link", P,
    "index.html:35 gives P0.1 as plain text with no href. course/modules has no P directory (ls: AC AP BK CF CS E FC LX M PC S SC), so 'not yet released in this program' is consistent with the tree.")
add("BK4a-hub-financial-intermediary", P,
    "index.html:61-66: the three FC1 concept links (clearing-and-settlement, trade-lifecycle, bank-money-creation) have dfn ids in FC1: course/modules/FC/FC1/L05.html:58 and :63, FC1 L01.html:81. href ../../../concepts.html#<id> pattern as BUILDER_RULES 4.1. Link check in " + S12 + "/link_check.out (57 internal hrefs, 0 bad, this round).")
add("BK4a-hub-bertrand-trade-fee", P,
    "index.html:65 says no lesson or project uses present value, the geometric series, the limit or Bertrand competition. Round 12 case-insensitive grep (scope_bertrand_limit_grep.out) over index, L01-L05 and project.html for 'present value', 'geometric', 'bertrand', '\\lim', 'limit of': no mathematical hit. The English word 'limit' occurs only as 'a stated limit' (L04.html:52) and 'Limits' (project.html:416,427,440,450,469,478); not the concept.")
add("BK4a-hub-concept-anchors", P,
    "Round 12 link script " + S12 + "/link_check.out (57 internal hrefs in index.html, L01-L03; every href file exists and every #fragment is an id in the target page): 0 bad. Concept hrefs: index.html:63-66; L01.html:37; L02.html:37,275; L03.html:37 resolve to dfn ids.")
add("BK4a-hub-ladder-vs-project", P,
    "index.html:152 rung 1 = four-member clearing house with 40 seeded SIMULATED losses; project.html:54 (four members, set of 40 scenarios). index.html:154 clearing_house.py matches project.html:47,201. index.html:171 'seeds 0 to 9' matches project.html:380. index.html:122,131 layer order and remainder rule match project.html:219,220.")
add("BK4a-hub-data-status", P,
    "index.html:37,182 say no data is used. course/assets/data/market/MANIFEST.json datasets: fx_daily, fx_monthly, ust_daily only (python -I read this round). tools/data_sources.yaml ids at :19 (fx_daily), :53 (fx_monthly), :91 (ust_daily). No data-files attribute in index, L01, L02 or L03.")
add("BK4a-hub-reading-list", P,
    "index.html:186-194 cites duffie2011central and bisndcpmi. references/references.json duffie2011central: DOI 10.1093/rapstu/rar001, title 'Does a Central Clearing Counterparty Reduce Counterparty Risk?', Review of Asset Pricing Studies 1(1), verified_by crossref. Plain curl https://api.crossref.org/works/10.1093/rapstu/rar001 (saved " + S12 + "/crossref_duffie.json) returns the same title and container. bisndcpmi: issuer-verified index page (bis.org/committees/cpmi/publications). The SEC rule has no record (registry_flags).")
add("BK4a-hub-process-words", P,
    "Round 12 case-insensitive grep over index.html, L01-L03 and the three twins for build, builder, verifier, round N, fixer, ruling, architect, REQUEST, unit report, plan N, plans/: 0 hits.")
add("BK4a-hub-settlement-framing", P,
    "index.html:33 'a trade settles when its payment has moved between accounts' is the model's definition; L01.html:55 uses the same model statement, and L01 Definition 1.1 (l59) defines the designs.")
add("BK4a-hub-P0.1-grade-source", P,
    "index.html:108 grade C text 'working paper, practitioner research or single-sample evidence' matches the BLUEPRINT.md section 3 table row for C (read this round). Its reference to P0.1 is a placement explanation, consistent with the unreleased-module note at index.html:35.")
add("BK4a-hub-card-L02", P,
    "index.html:141 L02 card (novation, CCP, net obligations sum to zero, netted amount against gross notional, Lab 1 on seeded SIMULATED trades) matches L02.html:1-40 (title, meta description, Lab 1 section at l121-127).")

# ---------- L01 ----------
add("BK4a-L01-numbers", P,
    "Round 12 full read of L01.html 1-554. Every number re-derived from the page's expected block: need A 112500, B 1533900, C 0; net A +379800, B -1533900, C +1154100; debit B 1533900; gross 2841600; moved 1533900; ratio 1533900/2841600 = 0.53980152 -> 0.5398 and 53.98 % (l286, l409, l452). 2841600 cents = 28416 dollars (l525). " + NUM + ".")
add("BK4a-L01-prop-2.2-2.4", P,
    "L01.html:84-111. Prop 2.2 (need = max(0, -min_k S_ik)), Prop 2.3 (net positions sum to zero) and Prop 2.4 (need >= debit, strict in Example 2.6) proofs re-derived line by line: min-of-constraint step, k=m in the minimum, max(0,.) nondecreasing. All sound under Assumption 1.3.")
add("BK4a-L01-P2-iff", P,
    "L01.html:375-377 (P2) re-derived: cases mu>=0 (both zero); mu<0 and S_m=mu (both -mu); mu<0 and S_m>mu (Need=-mu, Debit is 0 or -S_m < -mu, so unequal). Iff holds; hypotheses listed (l377) are the ones used.")
add("BK4a-L01-examples-remarks", P,
    "L01.html:119-126. Example 2.6 running sums A 0,-100,-100,-50; B 0,100,20,20; C 0,0,80,30; minima -100,0,0; Net -50,20,30; Debit_A 50; gross 230. Remark 2.7 sums A 0,50,-50,-50, need 50. " + NUM + " (Example 2.6 and Remark 2.7 rows).")
add("BK4a-L01-problems-M-P-E-R", P,
    "L01.html:343-434 (M1-M3, P1-P3, E1-E3, R1-R3) each re-derived: M1 need 200 debit 200; M2 200/100; M3 need 30 debit 20 (dip 10); P1 sum argument, A1 finite list and one sender/receiver used; P3 scaling; E1 Bank B 1533900; E2 Bank A only, 1 of 3; E3 ratio 0.5398 base gross; R1 inflows-first equality; R2 sums; R3 zero debit, need 100. " + NUM + ".")
add("BK4a-L01-remark-3.1-order", P,
    "L01.html:298-301 and :420. Inflows-first gives running sums rising then falling monotonically to Net_i, so the running minimum is min(0, Net_i) and Need = max(0,-Net_i) = Debit (re-derived). Ordering claim 'no order gives a lower need' holds since Need >= Debit always (Prop 2.4).")
add("BK4a-L01-R3", P,
    "L01.html:432-434. Payments A->B 100, B->C 100, C->A 100: every net position 0 so every debit 0 (Def 2.1); A running sums 0,-100,-100,0 so need 100. Re-derived in " + NUM + " (R3 rows).")
add("BK4a-L01-remark-2.8", P,
    "L01.html:289-292. Part B prints the Prop 2.4 inequality per bank (lab line 'RTGS need at least DNS net debit: True' x3) and Part C prints the zero sum ('net positions sum to zero: True'). Both are printed in the expected block (L01.html:269-275). The claim that the checks test the printed day only is accurate.")
add("BK4a-L01-interp-three-inequalities", P,
    "L01.html:286 interpretation. Bank B need 1533900 = debit 1533900 (expected block l270); Bank A net +379800, debit 0, need 112500 (l269); Bank C 0 under both (l271). Ratio 0.5398 rounded from 0.53980152; the lab does not print it (lab line 233-243 has no ratio). Statements match.")
add("BK4a-L01-misconception-1", P,
    "L01.html:320-322: Bank A need 112500 vs debit 0 (expected block l269); Bank B net -1533900, debit 1533900 and need 1533900 (l270). 'Under DNS it must fund the whole net debit at settlement, by Definition 2.1 and A2' matches Def 2.1 (l80) and A2 (l71).")
add("BK4a-L01-misconceptions-2-3", P,
    "L01.html:324-331. Bank A net +379800, debit 0, need 112500, Prop 2.4 strict (l326). Remark 2.7: A's need falls 100 -> 50 dollars, net debit stays 50 (l330), matching Example 2.6 and Remark 2.7 arithmetic.")
add("BK4a-L01-quiz", P,
    "L01.html:458-537, 10 items. Keys recomputed: debit of -200 net is 200 (Def 2.1); need 200 (Prop 2.2); Prop 2.4 inequality; doubled Example 2.6 need 200; Remark 2.7 need 50; zero sum; net +50 gives debit 0; lag is a lab parameter; 2841600 cents = 28416 dollars; T+1 named, not stated. Each explanation cites a definition or proposition that exists (l469, l474, l483, l488, l493, l502, l511, l520, l525, l534).")
add("BK4a-L01-lab-twin", P,
    "L01.html:128-287 and tests/labs/BK4/lab-BK4-L01-1.py. " + EMB + ". " + RUN + ". tools/run_labs.py --unit BK4: 8/8 PASS (" + S12 + "/run_labs.out).")
add("BK4a-L01-notation", P,
    "Round 12 scan of every inline and display math in index, L01, L02, L03 for registered symbols (notation/notation.json: T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, Q) and registered macros (\\E, \\R, \\Prob, \\Var, ... ): none used. Local symbols (S, m, o_i, Net, Debit, Need, d, mu, k) are defined where first used.")
add("BK4a-L01-dag-defs", P,
    "L01.html:37 uses FC1 clearing-and-settlement and trade-lifecycle (in closure, FC1 defines them). Defs payment-system (l59) and settlement-cycle (l64) are the only data-concept dfns in L01; check_dag --unit BK4: PASS (" + S12 + "/check_dag.out).")
add("BK4a-L01-why-words", P,
    "L01.html:51 why-it-matters: 107 words (<= 120, BUILDER_RULES 4.2); says the lesson defines payment system and settlement cycle, compares designs, and that the lab uses SIMULATED data. Matches the lesson.")
add("BK4a-L01-structure", P,
    "L01.html 34-552 read in full: header, grade legend, sections 1-9 in BUILDER_RULES 4.2 order; why-it-matters 107 words; 3 misconceptions; problem set 3 per tier (M, P, E, R); key-results table; 10 quiz items; references. check_pages --unit BK4: PASS (" + S12 + "/check_pages.out).")
add("BK4a-L01-grades", P,
    "L01.html:84-104 T rows (Props 2.2-2.4) with proofs on page; key rows 446-450 T (proved or worked by hand; Example 2.6 and Remark 2.7 at l450); rows 451-452 C naming Lab 1 Parts B and C (SIMULATED, one seed), as ruling 13 requires for lab-only values.")
add("BK4a-L01-FC1-claim", P,
    "L01.html:55 'FC1 Lesson 5 followed one trade through that sequence': course/modules/FC/FC1/L05.html title 'Clearing, Settlement and the Trade Lifecycle', meta description 'a SIMULATED trace of one seeded trade from order entry to settlement'. The six states in order are at FC1 L05.html:63.")
add("BK4a-L01-canon-breaks-wording", P,
    "L01.html:307-315 (canon-breaks): four bullets, each a model limit (no queues; day given; d a parameter with no market value; no claim about which real system uses which design). 'the lesson states no result outside it' is consistent with Sections 2-4.")
add("BK4a-L01-A2-forward-ref", F,
    "L01.html:71 (Assumption 1.3, A2) uses 'the net debit, defined in Definition 2.1' before the term is defined. First in-body use of 'net debit' is l71 (grep: l71 is the first hit outside the meta description l7); the dfn is at l80. Plan 2.1 item 5 requires a term outside the 9 concepts to be 'defined in prose at first use with a plain <dfn>'. A hypothesis that uses an undefined term is not well formed when stated.",
    fix="At L01.html:71, replace 'the net debit, defined in Definition 2.1,' with the definition in words, e.g. 'the amount max(0, minus its net position) (the net debit of Definition 2.1)', or move the net-debit sentence of Definition 2.1 into Definition 1.1 and give the term a plain <dfn> there.")
add("BK4a-L01-canon-bullet-only-designs", P,
    "L01.html:313 'the lesson states no fact about which design any real system uses; the two designs are defined in Definitions 1.1 and 2.1' matches Definition 1.1 (l59) and Definition 2.1 (l80).")
add("BK4a-L01-R1-order-claim", P,
    "L01.html:420 R1 solution: equality attained by inflows-first order (re-derived, see BK4a-L01-remark-3.1-order); the hypothesis used (net position independent of order) is stated.")

# ---------- L02 ----------
add("BK4a-L02-prop-2.2", P,
    "L02.html:85-99. Prop 2.2 (a)-(d) and proofs re-derived: (a) each trade enters one Rec and one Pay by A2; (b) sum n_i = G - G; (c) max(0,x)-max(0,-x)=x; (d) 0 <= A <= G. Sound under A1-A3 as stated.")
add("BK4a-L02-prop-2.3-title", P,
    "L02.html:101-103 title 'no netting reduction is achieved exactly when no member both receives and pays' matches the statement at l103 (A = G iff for every i, Rec_i = 0 or Pay_i = 0).")
add("BK4a-L02-prop-2.3-proof", P,
    "L02.html:106-109 and P2 at 348-349: three-case proof re-derived (Rec=0 gives term 0 = Rec; Rec>0, Pay=0 gives Rec; Rec>0, Pay>0 gives term < Rec). Both directions covered.")
add("BK4a-L02-example-2.4", P,
    "L02.html:112-113 Example 2.4: Rec (50,100,80), Pay (100,80,50), n (-50,20,30), A 50, reduction 180 of G 230, floor(10000*180/230) = 7826 (l113, l270, l294). Re-derived in " + NUM + " (Ex2.4 rows).")
add("BK4a-L02-lab-claims", P,
    "L02.html:123,127: lab checks the Prop 2.2 identities on the printed set (receivables = G; n sum to zero; paid after netting equals paid by net payers and is at most G). Lab prints each (tests/labs/BK4/lab-BK4-L02-1.py Parts B-D; expected block l255-269).")
add("BK4a-L02-lab-numbers", P,
    "L02.html:241-269 expected block parsed; trades re-summed to G 7596300; receivables 314500/2067800/3340300/1873700; payables 3941500/314500/0/3340300; nets -3627000/+1753300/+3340300/-1466600; A 5093600; reduction 2502700; floor(10000*2502700/7596300)=3294 (exact 3294.63). Interpretation l270 matches. " + NUM + ".")
add("BK4a-L02-lab-numbering", P,
    "L02.html:121-127 section 3 'Lab 1: netting for one seeded set of trades' and lab id lab-BK4-L02-1; the lab's printed Parts A-D match the page's references in l270 and l365-382.")
add("BK4a-L02-attribution", P,
    "L02.html:277 'The question of whether a CCP reduces counterparty risk is asked by Duffie and Zhu (2011)'; l277 says the question is their title. Title from Crossref (" + S12 + "/crossref_duffie.json): 'Does a Central Clearing Counterparty Reduce Counterparty Risk?'. The DOI landing page returns HTTP 403 to plain curl (reproduced this round: doi.org -> academic.oup.com/raps/article-lookup/doi/10.1093/rapstu/rar001), so the paper's findings are NOT read and NOT stated (l285, l425 state no answer). No finding is attributed.")
add("BK4a-L02-canon-misconceptions", P,
    "L02.html:280-285 canon (four bullets) and :293-302 misconceptions 1-3. Netted amount 0 iff every n_i <= 0 and then all n_i = 0 (Prop 2.2(b)); Lab 1 Part D prints a positive netted amount (5093600); CCP is not a payment system; zero sum says nothing about default.")
add("BK4a-L02-problems", P,
    "L02.html:315-406 (M1-M3, P1-P3, E1-E3, R1-R3) re-derived: M1 n (-10,-20,50,-20), A 50, G 180, 7222 bp; M2 G 460, A 100, 7826 bp; M3 n (-200,100,100), A = G = 200, 0 bp; P3 cycle A=0, 10000 bp; E1 5093600 + 2502700 = 7596300; E2 member 3 +3340300, member 1 -3627000; E3 members 1,2,4 both receive and pay (Part B); R1 range; R2 X and Y both A = 100; R3 |change| <= a. " + NUM + " for the numbers.")
add("BK4a-L02-key-results", P,
    "L02.html:416-425: T rows 418-422 each proved or worked on the page (Prop 2.2, 2.3, Problem R1, Problem P3, Example 2.4 at l423); row 424 C naming Lab 1 Parts B to D (SIMULATED set, one seed); row 425 C 'question only' naming the registry key. Grades match ruling 13.")
add("BK4a-L02-quiz", P,
    "L02.html:431-510, 10 items recomputed: member 2 net 20; netted 50; sum zero; 7826 bp; equality iff no member both receives and pays; member 2 net 100; central counterparty does not move money; zero sum does not show no default; 5093600 cents = 50936 dollars; cycle netted zero. Explanations name existing definitions/propositions.")
add("BK4a-L02-lab-twin", P,
    "L02.html:121-271 and tests/labs/BK4/lab-BK4-L02-1.py. " + EMB + ". " + RUN + ".")
add("BK4a-L02-why-structure", P,
    "L02.html 1-527 read in full: header, sections 1-9 in order, why-it-matters 96 words, lab section, canon-breaks (4 bullets, 'Four places' count matches), misconceptions (3), problem set 3 per tier, key results (8 rows), quiz (10 items), references.")
add("BK4a-L02-meta-description", P,
    "L02.html:7 meta description: novation, CCP, netting identities, bound that netted amount never exceeds gross notional (Prop 2.2(d)), Lab 1 on four members and six trades in integer cents. Matches the page.")

# ---------- L03 ----------
add("BK4a-L03-legend", P,
    "L03.html:43-48 grade legend (template shared with L01, L02). Only T and C grades are used in the slice body; B is not used (grep data-grade=B: legend only). Template wording 'published, not settled' is a shared gloss, not a slice claim; see notes.")
add("BK4a-L03-four-resources", P,
    "L03.html:55,66-73: 'Three resources pay a loss in this lesson' (initial margin, the defaulter's default fund, CCP capital) and survivors' default funds pay what remains. Definition 1.1 (l69-72) has the three layers and the survivor step (l73). Consistent.")
add("BK4a-L03-notation-d", P,
    "L03.html:61,67-73,100,139,152,480-482: local symbols IM_i, DF_i, K, L, Z, D, u, ell, n+, p_i, x_i, c(M), S, k, t are each defined on first use (l61, l67, l73, l90, l133, l145). None is a registered symbol (notation.json). \\mathcal{V} is local (survivors).")
add("BK4a-L03-def-props-1.2-1.3", P,
    "L03.html:66-96. Def 1.1 layers and survivor rule re-derived (a1=min(L,IM), a2=min(L-a1,DF), a3=min(L-a1-a2,K), Z, D, x_i=floor(Z DF_i/D), leftover to first survivors with DF>0). Prop 1.2 conservation and Prop 1.3 bound (0 <= ell <= n+ - 1, x_i + 1 <= DF_i) proofs checked line by line; sound.")
add("BK4a-L03-remark-1.4", P,
    "L03.html:100-101. a2 > 0 implies a1 = IM (since a1 < L forces a1 = IM); a3 > 0 implies a2 = DF; Z > 0 implies a3 = K. Each proof re-derived from the min definitions.")
add("BK4a-L03-example-1.5", P,
    "L03.html:104-121. Text derivations re-computed: L=200 (8, 12, residual 20); L=300 (40, 60, uncovered 20); L=180 (Z=0); L=181 (leftover to member 1). The table rows 80, 120, 170 and 205 are NOT derived in the text: l105 says 'Lab 1, Part A1 prints these rows, which are the table below'. Their arithmetic is correct (recompute_numbers.out 'table row' rows, 8 of 8 PASS), but the grade question is recorded in BK4a-L03-key-results.")
add("BK4a-L03-example-1.6", P,
    "L03.html:124-126: Z=1 gives member 1 one cent; Z=2 gives members 1 and 2 one cent each (p_i = 1/3, 2/3). Re-derived (recompute_numbers.out 'ex1.6' rows PASS).")
add("BK4a-L03-def-2.1-prop-2.3", P,
    "L03.html:133-165. Def 2.1 cover(M) = floor(10000 c(M)/S) and Prop 2.3 (k = ceil(tS/10000), k in 1..S, cover(M) >= t iff M >= L_(k), smallest margin L_(k)) re-derived; proof Part 2 floor/ceiling steps sound for integer t. Re-derived in " + NUM + " (L03 M2/M3 k rows).")
add("BK4a-L03-cor-2.4-ex-2.5", P,
    "L03.html:168-181. Corollary 2.4 proof (ceil monotone, sorted losses nondecreasing). Example 2.5: 9900*200/10000 = 198 exactly (k=198); 9975*200/10000 = 199.5 so k=200 (largest loss). Lab Part B output 2961 and 2992 in the expected block (l405-410).")
add("BK4a-L03-R1-note", P,
    "L03.html:530-533 (Problem R1, real margins): Prop 2.3 Part 2 uses only that M is real; set of margins with cover >= t is [L_(k), infinity); smallest L_(k) attained. Sound.")
add("BK4a-L03-canon-bullet-6", P,
    "L03.html:422 'A low target leaves a tail': cover 10000c/200 = 50c; 9900 bp means c = 198 and two scenarios above the margin (exact because the printed cover is 9900). 'two only when L_(198) < L_(199); ties leave fewer' re-derived. Changing a scenario above the margin that stays >= L_(198) leaves the 198th order statistic unchanged. Margin pays all M cents of its layer (a1 = min(L,M) = M for L > M). Correct.")
add("BK4a-L03-misconceptions", P,
    "L03.html:430-443: (1) loss = margin is counted (Def 2.1, Remark 2.2); (2) 9900 bp is a count share, Example 2.5 k=198; (3) Remark 1.4 and Lab 1 Part A3 scenario 1529 with DF 0 and capital 0; (4) survivors pay by DF_i only (Def 1.1). All four match the page and the lab output.")
add("BK4a-L03-problems", P,
    "L03.html:455-546 (M1-M3, P1-P3, E1-E3, R1-R3) re-derived: M1 layers 100,50,30, residual 20, 8 and 12, total 200; M2 cover(4000)=7500, k=3, margin 3000, cover(2999)=5000; M3 margins 40, 50, 50; P1-P3 proofs sound; E1 3160 = 3058 + 102; E2 857 = 312+381+164, DF/2 with no leftover; E3 floor(50c)=9900 only at c=198; R1 real margins; R2 k=99 and 100 for S=100; R3 k=S iff S<=399 (checked for S in 1..401). recompute_numbers.out rows PASS.")
add("BK4a-L03-key-results", F,
    "L03.html:565 grades 'The fixture rows of Example 1.5 and the remainder cases of Example 1.6 hold in exact integer cents' as T with basis 'Examples 1.5 and 1.6 (worked on the page ...); Lab 1 Parts A1 and A2 reproduce them'. Ruling 13 (plans/FINAL-ARCHITECT-RULINGS.md:28-31): a value appearing only in lab output is graded C naming the lab. Example 1.5 derives in the text only L=200, 300, 180 and 181; table rows L=80, 120, 170 and 205 appear only in the table that l105 attributes to 'Lab 1, Part A1 prints these rows'. Those four rows are not derived on the page. Other T rows (l559-564) are proved on the page. Row 566 (C naming Lab 1 Part B) is correct.",
    fix="Either (a) add one hand derivation line each for L=80 (a1=80, Z=0), L=120 (a1=100, a2=20, Z=0), L=170 (a1=100, a2=50, a3=20, Z=0) and L=205 (a1=100, a2=50, a3=30, Z=25, shares 10 and 15) to Example 1.5 and keep row 565 at T; or (b) split row 565: T for the rows derived in Example 1.5 (L=180, 181, 200, 300) and Example 1.6, and C naming Lab 1 Part A1 for the table rows 80, 120, 170 and 205. Then make card BK4-c043 and the row say the same thing.")
add("BK4a-L03-quiz", P,
    "L03.html:572-647 (10 items). Keys re-derived: layer after margin = defaulter's DF (Def 1.1 step 2); 8 and 20 cents (Example 1.5); equality counted in cover (Def 2.1, Remark 2.2); 7500; k=3; 50 cents for 8001 bp (Problem M3); member 1 pays 1 cent (residual 2, three DF 1); 198 of 200 (50c=9900); k=399 for 400 scenarios (9975*400/10000). Explanations match.")
add("BK4a-L03-lab-twin", P,
    "L03.html:187-411 and tests/labs/BK4/lab-BK4-L03-1.py. " + EMB + ". " + RUN + ". Expected block includes 'layers sum to the loss: True' (x13: 8 fixture rows, 2 remainder rows, 3 Part A3 rows), 'every fixture row sums to its loss: True', and 'agrees with the sized margin: True' (x2), as the hypothesis at l189 predicts.")
add("BK4a-L03-why-structure", P,
    "L03.html 1-664 read in full: header, sections 1-8 in order, lab with interpretation, canon-breaks (6 bullets), misconceptions (4), problem set 3 per tier, key results (8 rows), quiz (10 items), references. why-it-matters 118 words (<= 120).")
add("BK4a-L03-uses-meta", P,
    "L03.html:37 'Uses: central counterparty and multilateral netting (L02)' with links to L02.html#def-central-counterparty and #def-multilateral-netting, which exist (l64, l81). Both are L02 concepts, earlier in the DAG.")
add("BK4a6-L03-lab-docstring-seed", P,
    "tests/labs/BK4/lab-BK4-L03-1.py:1-10 docstring: inputs of Parts A3 and B come from a fixed seed and are SIMULATED; Parts A1 and A2 are the stated fixtures. The code (SEED=2026, rng for im, df, capital, losses) matches. The docstring says 'checks each sized margin by a brute-force search over the integer margins 0, 1, 2, and so on', matching brute_force_margin.")
add("BK4a6-L03-corollary-heading", P,
    "L03.html:167-169 heading 'Corollary 2.4 (the sized margin does not fall as the target rises)' matches the statement at l169 (M(t) <= M(t') for t <= t').")

# ---------- cards and gates ----------
add("BK4a9-cards-L01-L03", P,
    "course/modules/BK/BK4/cards.json: all 66 cards of L01 (17: BK4-c001..c015, c091, c101), L02 (25) and L03 (24) read in full this round and checked against the lesson text (definitions, propositions, example values, lab values). Ids not sequential (ruling 2; gap at c042). Card grades: T rows cite a proof or an example on the page; C rows (c010-c012, c014, c031, c032, c049, c050, c092) cite Lab 1 parts. No card cites a value only the lab prints without the C grade.")
add("BK4a10-cards-all", P,
    "Full-file scan of cards.json (100 cards, all lessons): 0 duplicate ids, 0 duplicate fronts (python -I). Per lesson counts L01 17, L02 25, L03 24, L04 19, L05 15.")
add("BK4a10-recheck-status", P,
    "Round 12 carried NO PASS row from round 10 (the round-10 PASS rows were not trusted, per the round-12 task). Every row here was re-evidenced from the round-12 checkout. Delta 00a8479..5db69a9 touches only L03.html:565 and cards.json (L01-L03 cards c043, c044, c047; L05 cards c086, c091, c094 out of this slice). Row ids kept from round 10.")
add("BK4a10-delta-hunks", F,
    "Delta 00a8479..5db69a9 (git diff) read hunk by hunk. L03.html:565 (key row 565) T regrade and cards.json hunks (c043 and c044 basis text, c047 wording, plus L05 cards not in this slice). The card hunks are consistent with the lesson text (see BK4a12-cards-delta). The L03.html:565 regrade is not supported for the four table rows of Example 1.5 (see BK4a-L03-key-results).",
    fix="See BK4a-L03-key-results: either derive L=80, 120, 170, 205 in Example 1.5 or split row 565 into T (derived rows) and C (table rows naming Lab 1 Part A1).",
    location="course/modules/BK/BK4/L03.html:565; course/modules/BK/BK4/cards.json (delta 00a8479..5db69a9; hunk @@ -562 changes line 565)")
add("BK4a10-lab-run", P,
    "run_labs --unit BK4: 8/8 PASS (" + S12 + "/run_labs.out). Each slice twin run alone under python3 -I -W error from /tmp: exit 0 (L01, L02, L03). page_smoke alone on index L01 L02 L03: PASS (" + S12 + "/page_smoke.log).")
add("BK4a10-full-read-index", P,
    "Full read of course/modules/BK/BK4/index.html, all 197 lines, line by line (hub header, objectives, prerequisites, placement quiz 8 items, lessons, ladder, hours, data status, reading list). Evidence per row above.")
add("BK4a10-full-read-L01", P,
    "Full read of L01.html 1-554 including lab code (l131-253), expected block (l254-285), interpretation (l286), remarks, examples, problem set, key results (l440-456), quiz (l458-537), references. Every number and sentence checked; findings: row BK4a-L01-A2-forward-ref.")
add("BK4a10-full-read-L02", P,
    "Full read of L02.html 1-527 including lab code (l128-240), expected block (l241-269), interpretation (l270), canon-breaks, misconceptions, problem set (l307-410), key results (l412-429), quiz (l431-510), references. Every number and sentence checked.")
add("BK4a10-full-read-L03", P,
    "Full read of L03.html 1-664 including lab code (l190-382), expected block (l383-410), interpretation (l411), canon-breaks (l414-424), misconceptions (l426-446), problem set (l448-551), key results (l553-570), quiz (l572-647), references. Findings: row BK4a-L03-key-results.")
add("BK4a10-recompute", P,
    "Independent recomputation: " + NUM + ". Every number re-derived with fractions/integers from the page's own expected blocks; zero failures.")
add("BK4a10-lab-embed", P,
    EMB + ". Page code equals the twin (after the final newline that embed_labs.py strips); expected block equals twin stdout for L01, L02, L03.")
add("BK4a10-duffie-abstract-access", P,
    "Access statement: plain curl https://doi.org/10.1093/rapstu/rar001 with redirects returns HTTP 403 at academic.oup.com (reproduced this round; " + S12 + "/check_embeds.out not involved). Crossref returns no abstract. No bypass attempted. No finding of the paper is attributed on the page, so the abstract is not needed for the slice.")
add("BK4a10-bis-index", P,
    "Plain curl https://www.bis.org/committees/cpmi/publications: HTTP 200 re-run in round 12 (bis_curl.out); index page. The slice cites bisndcpmi only at index level (index.html:191 'an index and supports only index-level statements').")
add("BK4a10-registry-no-waterfall", P,
    "references/references.json: no title, container or record mentions waterfall, CCP, central counterparty (other than Duffie and Zhu), margin, T+1 or settlement cycle (Python scan this round: no hits). L03.html:417,651 state the registry holds no source on CCP waterfalls: consistent.")
add("BK4a10-data-manifest", P,
    "course/assets/data/market/MANIFEST.json: datasets fx_daily, fx_monthly, ust_daily only (python -I read). No payment, settlement, clearing or stablecoin dataset.")
add("BK4a10-notation", P,
    "notation/notation.json: symbols T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, Q; macros include \\E, \\R, \\Prob, \\Var, \\Cov, \\Corr. Round 12 math scan of slice pages: none used. Local symbols defined on first use.")
add("BK4a10-process-and-banned", P,
    "Banned-phrase scan (BUILDER_RULES 1.1-1.4 strings: TODO, TBD, lorem, for brevity, details omitted, beyond the scope, left as an exercise, you can add more, it is important to note, studies show, experts agree, it is well known, obviously, clearly) and ellipsis outside code/pre: 0 hits in index, L01-L03. Process-word scan: 0 hits.")
add("BK4a10-scope-words", P,
    "Scope words (only, all, every, always, never, same, exactly, any) read in context across index, L01-L03: each is a proof step, a stated hypothesis (Assumption 1.3, A3, A4), a printed lab check, or a definitional sentence. No unsupported universal claim found. Two notes in the notes field.")
add("BK4a10-links", P,
    "Round 12 link script: 57 internal hrefs across index.html, L01, L02, L03; 0 missing files or ids. External links: none in the slice.")
add("BK4a10-concept-closure", P,
    "Round 12: no concept name owned outside {E1, FC1, M1, M2, P0.1, BK4} (curriculum/curriculum.json concepts, 1138 entries, name field) occurs by name in the slice text. Concepts linked: clearing-and-settlement, trade-lifecycle, bank-money-creation (FC1); payment-system, settlement-cycle, central-counterparty, multilateral-netting, ccp-default-waterfall, margin-cover (BK4).")
add("BK4a10-gates", P,
    "Round 12 gate runs (outputs in " + S12 + "/): check_pages --unit BK4 PASS; check_dag --unit BK4 PASS; check_projects --unit BK4 PASS; run_labs --unit BK4 8/8 PASS; page_smoke alone PASS; pytest tests/test_labs.py -k BK4 (8 passed) and tests/test_page_checks.py (41 passed); ruff check and format --check on repo PASS; mypy --no-incremental repo: 385 files PASS.")
add("BK4a10-mutants-na", P,
    "Slice a has no project grader; ruling 9 mutation requirement applies to project graders only (FINAL-ARCHITECT-RULINGS.md:9). Lab twins are demonstrations (verifier rules 2.5). No mutant is required for slice a.")

# ---------- round-10 PASS rows kept (ids unchanged), re-evidenced ----------
add("BK4a-gate-check-pages", P, "check_pages --unit BK4: 'check_pages BK4: PASS' (" + S12 + "/check_pages.out, round 12).")
add("BK4a-gate-check-dag", P, "check_dag --unit BK4: 'check_dag BK4: PASS' (" + S12 + "/check_dag.out, round 12).")
add("BK4a-gate-run-labs", P, "run_labs --unit BK4: 'run_labs BK4: PASS (8/8)' (" + S12 + "/run_labs.out, round 12).")
add("BK4a-gate-page-smoke", P, "page_smoke --unit BK4 --pages index L01 L02 L03, run alone: 'page_smoke BK4: PASS' (" + S12 + "/page_smoke.log, round 12).")
add("BK4a-gate-ruff-mypy", P, "ruff check tests/labs/BK4: 'All checks passed!'; ruff format --check tests/labs/BK4: '8 files already formatted'; mypy --no-incremental tests/labs/BK4: 'Success: no issues found in 8 source files' (" + S12 + "/ruff_check.out, ruff_format.out, mypy_labs.out).")
add("BK4a-gate-pytest-labs", P, "pytest tests/test_labs.py -k BK4 -q: 8 passed, exit 0; pytest tests/test_page_checks.py -q: exit 0 (" + S12 + "/pytest_labs.out, pytest_page_checks.out).")
add("BK4a-gate-verify-refs", P, "verify_refs.py --offline: 'offline integrity: 560 entries, 0 problems', exit 0; verify_refs.py --unit BK4: 'live re-verification of BK4: 3 of 560 entries, 0 problems', exit 0 (" + S12 + "/verify_refs_offline.out, verify_refs_unit.out).")
add("BK4a-gate-repo-ruff-mypy-r4", P, "Repository-wide: ruff check . 'All checks passed!' and ruff format --check . '559 files already formatted'; mypy --no-incremental: 'Success: no issues found in 385 source files' (" + S12 + "/ruff_repo.out, mypy_repo.out).")
add("BK4a-rederive-r4", P, NUM + ". Supersedes round-9 and round-10 recompute scripts.")
add("BK4a-lab-block-equality-r4", P, EMB + ". Supersedes round-9 and round-10 check_lab_embeds scripts.")
add("BK4a9-recompute-r9", P, NUM + ". Supersedes round-9 and round-10 recompute runs.")
add("BK4a9-lab-embed-r9", P, EMB + ".")
add("BK4a9-duffie-access", P, "https://doi.org/10.1093/rapstu/rar001 returns HTTP 403 to plain curl (redirect to academic.oup.com/raps/article-lookup/doi/10.1093/rapstu/rar001), reproduced this round. Access statement recorded, not bypassed. Title read from Crossref.")
add("BK4a9-notation-local-symbols", P, "L01.html:76 (S_{i,k}, Net_i, Debit_i), L02.html:69,75 (A_t, G, Rec_i, Pay_i), L03.html:133-152 (S, M, c(M), mu, d, t, k, C) each defined on first use and not redefined. No registered symbol used.")
add("BK4a9-L03-margin-pays-whole-amount", P, "L03.html:422: 'the margin pays all M cents of its layer' for a scenario above the margin: a1 = min(L, M) = M when L > M (Definition 1.1). Correct.")
add("BK4a9-grade-legend-B-template", P, "L01.html:45 shared grade legend, same as L02.html:45 and L03.html:45. The slice uses no B grade. Template gloss noted in notes; not a slice claim.")
add("BK4a9-registry-bisndbasel", P, "references/references.json bisndbasel: used_by ['BK1', 'BK4'] (round 12 read). BK4 cites it in L05.html:348 (not in slice). Index, L01-L03 do not cite bisndbasel. Consistent.")
add("BK4a-banned-and-process", P, "Banned-phrase list of BUILDER_RULES 1.1-1.4 (TODO, TBD, lorem, for brevity, details omitted, beyond the scope, left as an exercise, you can add more, it is important to note, studies show, experts agree, it is well known, obviously, clearly) and ellipsis outside code: 0 hits in index.html, L01-L03; process-word scan 0 hits; the three twins also scanned (" + S12 + "/scope_process_scan.out).")
add("BK4a-scope-words", P, "Scope words (only, all, every, always, never, same, exactly, any) read in context across index.html and L01-L03; each use is a proof step, a stated hypothesis (Assumption 1.3, A1-A4), a printed lab check, or a definitional sentence; no unsupported universal claim found (see notes).")
add("BK4a7-hub-skip-rule-vs-project", P, "index.html:71,150 (skip rule: placement bar and both skill checks) matches project.html:43 ('which needs the mastery bar and both skill checks, skip rungs 1 and 2').")
add("BK4a7-L03-scenario-intro-before-def", P, "L03.html:51: 'the share of scenario losses (one simulated loss per scenario)' introduces scenario with a plain dfn-like parenthetical in the same sentence; the defined term is then used in Def 2.1. Not a use-before-definition.")
add("BK4a7-L01-legend-B-template", P, "L01.html:45 shared legend (template). Slice uses no B grade. Noted, not a slice defect.")
add("BK4a7-L02-duffie-attribution-abstract", P, "L02.html:277,285,425 attribute only the question of the title (Crossref title, " + S12 + "/crossref_duffie.json). Abstract not read (HTTP 403, recorded). No finding attributed.")
add("BK4a7-gate-check-projects", P, "check_projects --unit BK4: 'check_projects BK4: PASS' (" + S12 + "/check_projects.out, round 12).")
add("BK4a8-L01-E2-only-scope", P, "L01.html:400-402 E2: 'Using Lab 1, Parts B and C' answers from printed Part C (1 of 3) and Part B (Bank A). Scope word is answered by the printed output.")
add("BK4a8-L02-E2-only-scope", P, "L02.html:370-374 E2 uses Lab 1 Parts C and D: largest positive net obligation 3340300 (member 3) and largest negative -3627000 (member 1); sum of positive nets 5093600 equals Part D. Verified.")
add("BK4a5-L01-lede-settlement-framing", P, "L01.html:51 why-it-matters: settlement framing matches Definitions 1.1 and 2.1 and the lab.")
add("BK4a5-L01-designs-pointer", P, "L01.html:59 Definition 1.1 pointer 'Section 2 measures' matches Section 2 (l74-111).")
add("BK4a5-L01-canon-heading", P, "L01.html:307-308 canon-breaks heading and first sentence read; claim 'states no result outside it' matches Sections 2-4.")
add("BK4a5-L02-canon-heading", P, "L02.html:279-280 canon-breaks heading and first sentence read; matches Sections 2-3.")
add("BK4a5-hub-prereq-uses", P, "index.html:61-66 prerequisite sentence and FC1 concept list match curriculum yaml (FC1 introduces clearing-and-settlement, trade-lifecycle, bank-money-creation) and the FC1 pages.")
add("BK4a5-links-anchors", P, "Round 12 link script: index.html, L01-L03 hrefs and fragments resolve (57, 0 bad). Dfn ids referenced by the slice exist.")
add("BK4a5-twins-alone", P, "tests/labs/BK4/lab-BK4-L01-1.py, lab-BK4-L02-1.py, lab-BK4-L03-1.py each run alone with python3 -I -W error from /tmp: exit 0 (round 12). Page code equals each twin.")

# carry any remaining round-10 ids not yet written: they are re-evidenced by the blanket gate and structure rows above
missing = [i for i in r10_ids if i not in rows]
if missing:
    print("MISSING (not yet evidenced):", missing, file=sys.stderr)

# ---------- new round-12 rows ----------
add("BK4a12-cards-delta", P,
    "Delta cards hunks (5db69a9 vs 00a8479) for slice cards: BK4-c043 (T, Example 1.5 at L=200, text l105), BK4-c044 (T, Example 1.6 at Z=2, text l125), BK4-c047 (T, Corollary 2.4 wording matches L03.html:169). Basis texts name the Example and the Lab part that prints the value. All consistent with the lesson text. The grade of key row 565 is the open question (BK4a-L03-key-results).",
    check="2.7-cards", location="course/modules/BK/BK4/cards.json:349-377")
add("BK4a12-L02-why-forward-pointer", P,
    "L02.html:51 'A central counterparty (defined in Definition 1.2)' is a pointer in the why-it-matters overview, not an assumption or proposition statement. Not a use-before-definition defect for this slice; the dfn is at L02.html:64, the first formal use is l69+ after it. Recorded so the rule is applied consistently with BK4a-L01-A2-forward-ref.",
    check="2.9-structure DAG", location="course/modules/BK/BK4/L02.html:51,64")
add("BK4a12-registry-sec-t1", P,
    "SEC T+1 settlement rule: no registry record (references/references.json has no sec.gov T+1 key; references/review_queue.json lists it for manual admission). L01.html:64 and index.html:191 state the rule is named, not stated, and no lesson states it as fact. Consistent with BUILDER_RULES 2.4. Registry flag only.",
    check="2.1-citations", location="course/modules/BK/BK4/L01.html:64; index.html:191; references/review_queue.json")
add("BK4a12-L03-canon-no-register", P,
    "L03.html:651 'The registry holds no source on CCP waterfalls or on margin behaviour in stress': references.json has no such title (Python scan, round 12). Consistent.",
    check="2.1-citations", location="course/modules/BK/BK4/L03.html:651")
add("BK4a12-grade-legend-template", P,
    "Shared grade legend (L01.html:45, L02.html:45, L03.html:45) glosses B as 'published, not settled'; BLUEPRINT.md section 3 defines B as 'published in a top peer-reviewed venue, but not robustly replicated or actively contested'. The slice uses no B grade. Shared template across all modules; flagged in notes for the owner, not a slice defect.",
    check="2.3-grades template", location="course/modules/BK/BK4/L01.html:45; BLUEPRINT.md section 3")
add("BK4a12-checkout-hygiene", P,
    "The round-12 verifier ran tools/render_curriculum.py once inadvertently; git status after the run shows no tracked change (only untracked .venv and ledgers/BK4/scripts/BK4-a-r12/). No generated file was altered.",
    check="2.9-structure gate", location="CURRICULUM.md; curriculum/curriculum.json (unchanged)")

# ---------- assemble ----------
ordered = []
seen = set()
for rid in r10_ids:
    if rid in rows and rid not in seen:
        ordered.append(rows[rid]); seen.add(rid)
for rid, row in rows.items():
    if rid not in seen:
        ordered.append(row); seen.add(rid)

for row in ordered:
    if row["status"] != "PASS" and not row.get("fix"):
        raise SystemExit(f"no fix for {row['id']}")

fragment = {
    "unit": "BK4",
    "slice": "a",
    "round": 12,
    "verifier": "independent verifier (Haiku 5.5), round 12",
    "pin": "5db69a9bee460736c318ebfacc7200ee5a6eb0f0",
    "base": "00a84795f276456fce19d4181373cc4efba11a36 (round-10 pin); delta 00a8479..5db69a9 touches only course/modules/BK/BK4/L03.html:565 and course/modules/BK/BK4/cards.json",
    "checkout": ROOT,
    "scratch": "/tmp (twin runs); " + S12 + " (scripts and outputs, kept)",
    "verified_at": "2026-11-05T13:40:00Z",
    "verdict": "FAIL",
    "rows": ordered,
    "mutants": [],
    "registry_flags": [
        "SEC T+1 settlement rule (primary): no references/references.json record; review_queue entry 'add manually with an authoritative URL'. Blocks any statement of the rule as a fact (none in slice).",
    ],
    "freshness_flags": [],
    "notes": [
        "Slice: course/modules/BK/BK4/index.html, L01.html, L02.html, L03.html; tests/labs/BK4/lab-BK4-L01-1.py, lab-BK4-L02-1.py, lab-BK4-L03-1.py; cards.json entries for L01-L03 (66 cards, all read in full).",
        "Full read this round, line by line: index.html (197 lines), L01.html (554), L02.html (527), L03.html (664), the three twins, and all 66 slice cards. The delta since round 10 was read hunk by hunk.",
        "Round-12 FAILs: BK4a-L01-A2-forward-ref (L01.html:71 uses 'net debit' before its definition at l80) and BK4a-L03-key-results (L03.html:565 grades four lab-only table rows of Example 1.5 as T; ruling 13 requires C). BK4a10-delta-hunks is FAIL for the same reason.",
        "No round-10 PASS row was carried forward. The task said not to trust them; every row was re-evidenced in this checkout. Round-11 fragment E-BK4-a.round11.json does not exist in /Users/billyribeiro/.fanout/frags; round-10 fragment was used as the context file.",
        "Grade legend B gloss ('published, not settled') differs in wording from BLUEPRINT section 3 (B: published in a top peer-reviewed venue, not robustly replicated or contested). The legend is a shared template in every module; the slice uses no B grade. Not counted as a slice FAIL; flagged for the template owner.",
        "Overview pointer at L02.html:51 ('central counterparty (defined in Definition 1.2)') is treated as acceptable; the defect is only flagged where a term is needed to state an assumption or proposition.",
        "Index scope claim at index.html:65 ('no lesson or project uses present value, the geometric series, the limit or Bertrand competition') checked in L01-L05 and project.html by grep and reading; 'limit' appears only as English.",
        "Could not check: Duffie and Zhu (2011) abstract (publisher HTTP 403 to plain curl, recorded; no bypass). Nothing about the paper's findings is stated on the slice pages, so no row depends on it.",
        "Could not check: Pyodide-level test of the twin code beyond page_smoke (page_smoke ran the three lab boots and the runs; its PASS covers index, L01-L03).",
        "Not in slice and not judged: L04, L05, project.html, grader/, the cards of L04 and L05, lab-BK4-L04/L05 twins, the L05 lines of the delta (cards c086, c091, c094).",
        "Not run: run_graders (no grader in slice); render_curriculum was run once inadvertently with no tracked change; build_site --check not run (generated site outputs belong to the unit gate, not this slice).",
    ],
    "summary": "slice a, round 12, FAIL: 2 FAIL rows (BK4a-L01-A2-forward-ref, BK4a-L03-key-results) plus the delta row BK4a10-delta-hunks pointing at the same L03 grade.",
}

with open(f"{ROOT}/ledgers/BK4/BK4-a.json", "w", encoding="utf-8") as fh:
    json.dump(fragment, fh, ensure_ascii=False, indent=2)
    fh.write("\n")

counts = {}
for r in ordered:
    counts[r["status"]] = counts.get(r["status"], 0) + 1
print("rows", len(ordered), counts)
