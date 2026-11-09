"""FC1-b round 5: writes ledgers/FC1/FC1-b.json from the evidence in ledgers/FC1/scripts/FC1-b-r5/out/."""

import datetime
import json
from pathlib import Path

ROOT = Path(".").resolve()
S = "ledgers/FC1/scripts/FC1-b-r5"
O = f"{S}/out"
P = "PASS"

rows = []


def row(rid, check, location, status, evidence, fix=""):
    rows.append({"id": rid, "check": check, "location": location, "status": status, "evidence": evidence, "fix": fix})


row("FC1-b-r1-gate-check-pages", "tools/check_pages.py --unit FC1 --page L04; --page L05; --unit FC1",
    "course/modules/FC/FC1/L04.html, L05.html, cards.json", P,
    f"Re-run at dde0486b: {O}/check_pages_L04.out 'check_pages FC1 L04: PASS', check_pages_L05.out and check_pages_unit.out 'check_pages FC1: PASS' (rc 0 each, {O}/_rc.txt).")
row("FC1-b-r1-gate-check-dag", "tools/check_dag.py --unit FC1", "L04.html line 37; L05.html lines 38-39, 58, 63", P,
    f"{O}/check_dag_FC1.out 'check_dag FC1: PASS' (rc 0). L04 line 37 links L03#def-bid-ask-spread; L05 line 38 links L04#def-order-types, L04#def-limit-order-book, L01#def-financial-intermediary; L05 line 39 dfn targets are defined at lines 58 and 63 (def-clearing-and-settlement, def-trade-lifecycle).")
row("FC1-b-r1-gate-run-labs", "tools/run_labs.py --unit FC1 --page L04 / --page L05 / --unit FC1",
    "tests/labs/FC1/lab-FC1-L04-1.py, lab-FC1-L05-1.py", P,
    f"{O}/run_labs_L04.out, run_labs_L05.out, run_labs_FC1.out: 'run_labs FC1: PASS (8/8)', rc 0 each.")
row("FC1-b-r1-gate-twin-alone", "python -I -W error on each twin, alone", "tests/labs/FC1/lab-FC1-L04-1.py, lab-FC1-L05-1.py", P,
    f"{O}/twin_L04_isolated.out and twin_L05_isolated.out: rc 0, empty stderr (numbers_r5.out lines 'L04 rc 0 stderr ''' and 'L05 rc 0 stderr '''). Run with env -i PATH=/usr/bin:/bin in gates.sh.")
row("FC1-b-r1-gate-page-code-equals-twin", "page code block equals twin source", "L04.html lines 127-335; L05.html lines 110-365", P,
    f"{S}/numbers_r5.py (out/numbers_r5.out): 'L04 page code == twin: True', 'L05 page code == twin: True' after html.unescape and rstrip of trailing newlines.")
row("FC1-b-r1-gate-expected-equals-output", "pre.expected block equals twin output", "L04.html lines 336-357; L05.html lines 366-389", P,
    f"{S}/numbers_r5.py (out/numbers_r5.out): 'L04 expected == output: True', 'L05 expected == output: True' (stdout of python -I -W error on each twin).")
row("FC1-b-r1-gate-page-smoke", "tools/page_smoke.py --unit FC1 --pages L04 L05", "L04.html, L05.html", P,
    f"{O}/page_smoke_L04_L05.out: 'page_smoke modules/FC/FC1/L04.html: PASS', 'page_smoke modules/FC/FC1/L05.html: PASS', 'page_smoke FC1: PASS'; lab lab-FC1-L05-1 0.0 s.")
row("FC1-b-r1-gate-ruff", "ruff check and ruff format --check tests/labs/FC1", "tests/labs/FC1/lab-FC1-L04-1.py, lab-FC1-L05-1.py", P,
    f"{O}/ruff_labs.out 'All checks passed!'; {O}/ruff_format_labs.out rc 0 (_rc.txt).")
row("FC1-b-r1-gate-mypy", "mypy --no-incremental on both twins", "tests/labs/FC1/lab-FC1-L04-1.py, lab-FC1-L05-1.py", P,
    f"{O}/mypy_labs.out 'Success: no issues found in 2 source files'.")
row("FC1-b-r1-gate-pytest-labs", "pytest tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py tests/test_curriculum.py",
    "tests/test_labs.py, tests/test_run_labs.py, tests/test_page_checks.py, tests/test_curriculum.py", P,
    f"{O}/pytest_targeted_r5.out: all dots, rc 0 (pytest 9.0.2).")
row("FC1-b-r3-gate-build-site-check", "tools/build_site.py --check", "course/assets/data, course/index.html, course/concepts.html", P,
    f"{O}/build_site_check.out 'site data current: 6 outputs', rc 0.")
row("FC1-b-r1-gate-verify-refs-offline", "tools/verify_refs.py --offline (whole registry)", "references/references.json", P,
    f"{O}/verify_refs_offline.out 'offline integrity: 560 entries, 0 problems', rc 0. (The --unit flag selects a live run only.)")
row("FC1-b-r2-gate-verify-refs-live-unit", "tools/verify_refs.py --unit FC1 (live)", "references/references.json: harris2002trading", P,
    f"Re-run this round with network: {O}/verify_refs_unit_FC1_live_r5.out 'live re-verification of FC1: 2 of 560 entries, 0 problems', rc 0.")
row("FC1-b-r4-gate-check-projects-unit", "tools/check_projects.py --unit FC1", "course/modules/FC/FC1/project.html (unit gate)", P,
    f"{O}/check_projects_FC1.out 'check_projects FC1: PASS' (rc 0). Project content itself is slice c.")
row("FC1-b-r1-num-L04-prose", "every number in L04 prose recomputed", "L04.html lines 72, 77, 126, 377-385, 398-414, 423-439, 450-464, 475-489, 501-505, 536, 541, 563-565, 574",
    P, f"{S}/numbers_r5.py recomputes 159000/150 = 1060; 60*995+40*990 = 99300, avg 993; 150+100 = 250 = 2*100+50; 24+18 = 42; 181+77+42 = 300; 5600/173 exact; A1/A2 cases of R2 (999 buy rests, best bid 1005 >= ask 1000). Stop-activation and cascade values (990, 985, 980) re-derived from the Remark 1.2 rule in the twin (match/activate, twin lines 71-120) and from out/numbers_r5.out.")
row("FC1-b-r1-num-L04-lab-output", "L04 lab interpretation numbers vs printed output", "L04.html lines 336-357 (expected), 358 (interpretation), 505 (key result)", P,
    f"{O}/twin_L04_isolated.out prints: fills (1000,60),(1100,90); cost 159000; average 1060; 10 left; fills (990,100),(985,100); events 0-6 best bid 9984, event 7 bid none; 300 events 181/77/42; trades 173; shares traded 5600; stops 24 activated, 18 pending; crossed 0; conservation failures 0. Interpretation line 358 agrees.")
row("FC1-b-r1-num-L05-prose", "every number in L05 prose recomputed", "L05.html lines 75, 109, 390, 438, 445, 452, 488, 495, 502, 544, 582, 605-607, 637", P,
    f"{S}/numbers_r5.py (out/numbers_r5.out): NP/G = 7141207/34199443 = 0.20881062302681364; 8 dp 0.20881062; 5 dp 0.20881; half-up 3 dp 0.209; P5/G = 16.17 %; P5/NP = 77.44 %; 216*10060 = 2172960; 100*10090 = 1009000 (10090.00 units); Wed 2026-10-28 +1 Thu 10-29, +2 Fri 10-30, +3 Mon 11-02; Fri 10-30 +1 Mon 11-02, +2 Tue 11-03.")
row("FC1-b-r1-num-L05-lab-output", "L05 lab output numbers vs printed output", "L05.html lines 109, 366-389, 390", P,
    f"{O}/twin_L05_isolated.out and numbers_r5.out: header 2026-10-28 Wednesday; resting P2 10060x263, P3 10257x362, P4 10331x152; incoming P1 10117x216; one fill; consideration 2172960; settlement offset 2 Friday 2026-10-30; batch 20 trades, gross 68398886, net 14282414, ratio 0.209, 3 net payers, sum 0; net P1 -7411991, P2 -6656379, P3 3222054, P4 -214044, P5 11060360. E2 sums 7411991+6656379+214044 = 14282414 = 3222054+11060360 (numbers_r5.out).")
row("FC1-b-r1-lab05-parameter-claims", "L05 claims about changing the lab's parameters", "L05.html line 66, line 390, lines 500-502 (E3); card FC1-c142", P,
    f"{O}/l05_variants_r5.out (scratch copies of the twin, python -I -W error, default vs each variant): SETTLEMENT_LAG=3 changes exactly the header, the settlement line and the position_update line (3 lines), settlement moves to 2026-11-02 Monday, offsets True; CLEARING_OFFSET=1 changes the header and the clearing line only, offsets True; CLEARING_OFFSET=3 changes the clearing line and prints offsets_nondecreasing False; SETTLEMENT_LAG=0 changes three lines. Matches line 390, E3 solution (502) and card c142.")
row("FC1-b-r1-lab04-invariant-claim", "L04 claims that the lab checks both invariants after each event", "L04.html lines 51, 126, 358, 505; twin main() lines 176-188", P,
    f"Twin main() increments uncrossed_failures when bid >= ask and conservation_failures when submitted != resting + 2*traded + cancelled, after activate() for each of the 300 events (twin lines 179-188). Output lines 355-356: both 0 ({O}/twin_L04_isolated.out). 'Lab checks after each arrival, with activations' matches the code; no claim about intermediate single activations is made.")
row("FC1-b-r1-math-L04-examples-problems", "L04 examples and problems re-derived", "L04.html lines 72, 77, 377-385, 398-491", P,
    "Re-derived by hand and in numbers_r5.out: Example 1.3 (159000, 1060, 10 left), Example 1.4 (fills 990 then 985 via twin fixture B, lines 136-147), M1 (99300, 993, 60 left), M2 (fills 30@1000, 20@1001; left 10@1001, 40@1003), M3 (sell stop 1000: 1005 and 1001 no; 1000 yes), P2 (G=250, X=100, C=50, R=0), P3 (activation t>=s), R1 (fills 990,985,980), R2 (rests as bid; crossed), R3 (120 = 2*60).")
row("FC1-b-r1-math-L05-prop21-prop22", "L05 Propositions 2.1 and 2.2 with proofs, and P2 and R2", "L05.html lines 75-96, 100, 468-470, 518-520", P,
    "Prop 2.1(i): telescoping sum of c_i - c_i = 0 (line 84) holds with no assumption; (ii) under A1 c_i >= 0, Rec_j, Pay_j >= 0, max(-x_j,0) <= Pay_j, sum Pay_j = G (line 85). Prop 2.2 proof (line 95) under A2 gives CCP net cash G - G = 0 and net position x_j. P2 (lines 468-470): f(x)=max(-x,0) 1-Lipschitz and non-increasing, brackets in [-c,0] and [0,c], so |change| <= c_t, using A1 for c_t >= 0. R2 (518-520) numeric: x_A=100, x_B=-100, NP=100, G=-100; bound fails at Pay_j >= 0 step.")
row("FC1-b-r1-math-L04-prop22-empty-side", "L04 Proposition 2.2 empty-side conventions", "L04.html lines 99, 104, 425", P,
    "Prop 2.2 proof (line 104) states beta = -inf for an empty bid side and alpha = +inf for an empty ask side; buy-market case gives alpha' >= alpha; buy-limit residual case gives new best bid max(beta, p) and p < alpha' because every remaining ask is above p; all cases re-derived. P1 solution (line 425) uses the same convention and is consistent.")
row("FC1-b-r1-math-L04-prop23-assumptions", "L04 Proposition 2.3 with A2", "L04.html lines 93-95, 107-117; card FC1-c066", P,
    "A2 (lines 93-94) excludes withdrawals; Prop 2.3 (line 109) assumes A2; proof (line 116) splits each entered quantity into filled, cancelled (market only) and resting, sums to G = sum filled + C + R, and sum filled = 2X. Twin counts submitted at match() entry (twin line 73), stops at activation (line 117/183).")
row("FC1-b-r1-math-L04-remark-definitions", "L04 Definitions 1.1, 2.1, Remark 1.2 vs twin rules", "L04.html lines 56-67, 84-89, 197-220 (match), 222-246 (activate), 302-313 (main loop)", P,
    "Twin match() (lines 71-94): price-time best_resting, fill at resting price, market residual cancelled, limit residual rests. activate() (lines 96-120): buy stop >= s, sell stop <= s, repeat, earliest first. main() (lines 179-183): stops checked after the arriving order's match. Matches Definition 1.1, Definition 2.1 and Remark 1.2 text.")
row("FC1-b-r3-proof-P1-hypothesis", "L04 P1 hypothesis statement and solution", "L04.html line 423 (statement), line 425 (solution)", P,
    "Statement (line 423) assumes the book uncrossed before the arrival (A1 for the first event). Solution (line 425) now states the empty-side convention beta = -inf / alpha = +inf as in Prop 2.2; re-derived in full (row FC1-b-r1-math-L04-prop22-empty-side).")
row("FC1-b-r4-key-result-NP-hypothesis", "L05 key-results row for net payments bound carries A1", "L05.html line 540 (key-results row); Proposition 2.1 line 79; Problem R2 lines 518-520; card FC1-c101", P,
    "FIXED since round 4. Line 540 now reads 'Under A1, in a batch, net payments lie between zero and gross payments (Proposition 2.1(ii))', matching the Assumptions of Prop 2.1 (line 79). Card c101 states 'Under A1'. No T-graded row omits its hypothesis.")
row("FC1-b-r4-key-result-L04-503-hypothesis", "L04 key-results row for non-crossing carries A1", "L04.html line 503 (key-results row); Prop 2.2 line 99", P,
    "FIXED. Line 503 now reads 'Under A1, the book is never crossed after any event (Proposition 2.2)', matching the statement at line 99 ('Under A1 and the rules of Section 1').")
row("FC1-b-r4-key-result-L05-541-hypothesis", "L05 key-results row for CCP net cash carries A1 and A2", "L05.html line 541; Prop 2.2 line 90", P,
    "FIXED. Line 541 now reads 'Under A1 and A2, the CCP's net cash over a batch is zero ...', matching the Assumptions at line 90.")
row("FC1-b-r4-P1-empty-side-convention", "L04 P1 solution handles the empty side", "L04.html line 425", P,
    "FIXED. Solution now says 'if one side is empty, take beta = -inf or alpha = +inf, as in the proof of Proposition 2.2'. Each case re-derived (see row FC1-b-r1-math-L04-prop22-empty-side).")
row("FC1-b-r1-grades", "grades of every claim span vs BLUEPRINT §3 and the lesson's own grade legend", "L04.html lines 98, 108, 501-505; L05.html lines 78, 89, 539-544, 403; cards.json", P,
    "Re-graded against BLUEPRINT §3 (T theorem, C single study or single run): Prop 2.1, 2.2, Prop 2.3 and Prop 2.2 of L04 are T and proved on the page; lab-read counts and lab-read lines (L04 505; L05 542-544) are C naming Lab 1; Example rows are T computed on the page. Card grades agree (c061, c062, c066, c068, c079, c080, c089, c099-c102 T; c069, c082-c088 C with basis). No B/A/D claim in slice.")
row("FC1-b-r1-notation", "symbols and macros vs notation/notation.json", "L04.html and L05.html inline math (95 and 120 expressions)", P,
    "ledgers/FC1/scripts/FC1-b-r5/textscan_r5.py (out/textscan_r5.out): L04 single-letter symbols C,G,R,X,o,p,q,s,t; L05 A,B,C,G,J,K,b,c,f,i,j,n,p,q,s,t,x; macros used are standard KaTeX only (\\alpha \\beta \\cdot \\infty \\ge \\le \\max \\sum \\text \\times \\mathrm \\blacksquare). registered macros used: none. The 'T' hit in the text is the grade letter, not a math symbol. No math use of T, R_f, R^*, R^{e*}, Q, Phi, gamma_3, gamma_4. Lesson-local letters only (notation.json 'about').")
row("FC1-b-r1-prose-process-words", "no process words in learner text", "L04.html, L05.html, cards.json", P,
    "ledgers/FC1/scripts/FC1-b-r5/textscan_r5.py (out/textscan_r5.out): process-word regex over both lessons (outside code) and cards.json returns no hits. Learner-visible text carries no process words.")
row("FC1-b-r1-prose-banned-phrases", "banned strings and phrases", "L04.html, L05.html, cards.json", P,
    "textscan_r5.py (out/textscan_r5.out): banned-string regex (TODO, TBD, lorem, for brevity, details omitted, beyond the scope, left as an exercise, you can add more, it is important to note, studies show, experts agree, it is well known, obviously, clearly, and ellipses) over L04, L05 outside code and over cards.json: no hits. check_pages PASS (out/check_pages_unit.out).")
row("FC1-b-r1-structure-L04", "L04 template order and minimum counts", "L04.html", P,
    "Order: why-it-matters (116 words, numbers_r5.out <=120), §1-§2 core with Definitions, Assumptions A1-A2, Propositions 2.2-2.3, Remarks, lab (line 124), canon-breaks (361), misconceptions (3, 372), problem set (4 tiers x 3 problems, 390-493) with solutions, key-results (495-509, 9 rows), quiz (511-586, 9 items with explanations), references (588-592), lesson nav (595). data-hours=10.")
row("FC1-b-r1-structure-L05", "L05 template order and minimum counts", "L05.html", P,
    "Order: why-it-matters (119 words, <=120), §1 Definitions 1.1-1.2, Remark 1.3, §2 Propositions 2.1-2.2 with Assumptions, Remark 2.3, §3 lab (107-391), canon-breaks (393-404), misconceptions (4, 406-426), problem set (4 tiers x 3, 428-531), key-results (533-548, 6 rows), quiz (550-640, 11 items with explanations), references (642-646), lesson nav (648). data-hours=10.")
row("FC1-b-r1-scope-words", "scope words need a computation or a hypothesis", "L04.html lines 67, 126, 358, 364, 475, 505; L05.html lines 63, 70, 390, 399, 401", P,
    "textscan_r5.py (out/textscan_r5.out) lists every only/all/every/always/never/any/exactly/same/across/none hit in prose and quiz text. Universal claims are backed by a proof with an explicit hypothesis (Prop 2.2 under A1; Prop 2.3 under A2; Prop 2.1 under A1; Prop 2.2 under A1 and A2), by the printed run ('in this run', 'SIMULATED'), or by a definition ('a market order never rests'). L05 line 399 disclaims findings on central clearing.")
row("FC1-b-r1-attribution-harris", "bibliographic attribution of harris2002trading", "L04.html line 590; L05.html line 403; references/references.json; curriculum/02-economics-finance-core.yaml lines 383-386",
    "FAIL",
    "L04 line 590: 'The curriculum lists <span data-cite=harris2002trading>Harris, <em>Trading and Exchanges: Market Microstructure for Practitioners</em></span> among this unit's sources'. curriculum/02-economics-finance-core.yaml line 385 reads 'Harris, Trading and Exchanges (2003)' with no subtitle (read this round). The subtitle is the registry record's title (references/references.json entry harris2002trading, title 'Trading and Exchanges: Market Microstructure for Practitioners', year 2002). The page therefore attributes to the curriculum a title the curriculum does not state. L05 line 403 ('The curriculum lists Harris, Trading and Exchanges ... the registry holds that book under the year 2002') is accurate.",
    "L04.html line 590: change the clause to 'The curriculum lists Harris, Trading and Exchanges among this unit's sources (registry key harris2002trading; the registry record gives the title Trading and Exchanges: Market Microstructure for Practitioners and the year 2002).' Then re-run check_pages --page L04 and numbers_r5.py. LOW: wording only.")
row("FC1-b-r1-settlement-source-absence", "no settlement-period fact without a source", "L05.html lines 52, 105, 397, 513, 632; card FC1-c090; references/references.json", P,
    "The only settlement timing is the lab parameter SETTLEMENT_LAG = 2 (twin line 138, comment 'a parameter'). L05 line 397 and line 632 disclaim any market period; line 513 (R1) names no source and grades nothing; card c090 says so. No settlement-cycle key is cited (references.json has none used here).")
row("FC1-b-r1-references-L05", "L05 references and data-cite", "L05.html line 403 and line 646; course/assets/js/refs.js lines 68-90", P,
    "Line 403 claim: data-cite harris2002trading, data-locator 'Curriculum sources list for FC1 (yaml 383-386); registry record year 2002; no passage read for this lesson', grade C. yaml 383-386 holds the source string (verified this round). Reference list at line 646 populated by refs.js from data-cite.")
row("FC1-b-r1-references-L04-empty-list", "L04 references section", "L04.html lines 588-592; course/assets/js/refs.js", P,
    "Section cites harris2002trading via data-cite (line 590) and an empty ol[data-references] (591) filled by refs.js. The title wording in line 590 is the subject of FC1-b-r1-attribution-harris.")
row("FC1-b-r1-cards-L04", "L04 cards (30) against the lesson text", "course/modules/FC/FC1/cards.json (lesson L04: c056-c072, c099, c100, c119, c121, c132, c133, c135, c141, c143, c154-c156, c169)", P,
    f"Each of the 30 L04 cards re-read against L04 lines 56-67 (Def 1.1, Remark 1.2), 82-95 (Def 2.1, A1, A2), 97-117 (Props 2.2 and 2.3), 119-122 (Remark 2.4), 363-387 (misconceptions), 501-505 (key results), 595. Numbers in each card (for example 60, 150, 1000, 1100, 159000, 1060, 990, 985, 1005, 999, 10, 42, 120) appear in the lesson. {S}/cards_scan_r5.py (out/cards_scan_r5.out): every card's numbered locator appears in its lesson.")
row("FC1-b-r1-cards-L05", "L05 cards (33) against the lesson text", "course/modules/FC/FC1/cards.json (lesson L05: c073-c090, c101, c102, c109, c114, c118, c123, c124, c142, c144, c145, c164-c168)", P,
    f"Each of the 33 L05 cards re-read against L05 lines 56-70 (Defs 1.1-1.2, Remark 1.3), 75-101 (Section 2, Props 2.1-2.2, Remark 2.3), 105-110, 358-389 (lab), 397-425 (canon, misconceptions), 501-544 (E3, key results). Locators 'Definition 1.2', 'Remark 1.3', 'Proposition 2.1(i)', 'Section 4' (the canon-breaks section, s4), 'misconception 1-4' all appear in the lesson ({O}/cards_scan_r5.out).")
row("FC1-b-r1-cards-duplicates", "no duplicate cards, full file", "course/modules/FC/FC1/cards.json", P,
    f"{O}/cards_scan_r5.out: 168 cards; 0 duplicate ids; 0 duplicate fronts. Near-duplicate pairs (front Jaccard > 0.5 or back > 0.6) inspected; the L04/L05 pairs (c058/c121 buy vs sell stop; c080/c102; c132/c133; c114/c124; c118/c142; c165/c166; c109/c166) are distinct facts. Cross-lesson pairs (L01-L03) are out of slice and distinct.")
row("FC1-b-r1-card-c066", "card FC1-c066 vs Prop 2.3", "cards.json FC1-c066; L04.html lines 92-95, 108-111", P,
    "Card: 'Under A2 (no withdrawals), G = R + 2X + C after every event, where C is the shares cancelled from market orders (Proposition 2.3).' Agrees with line 109-110 and A2 at 93-94.")
row("FC1-b-r4-card-c099-changed-text", "card FC1-c099 (changed text this delta)", "cards.json FC1-c099; L04.html line 99", P,
    "Card: 'Under A1, the book starts empty, and under the matching rules of Section 1 it is not crossed after any event, where an event is an arrival or an activation of a stop (Proposition 2.2).' Agrees with line 99 word for word in substance.")
row("FC1-b-r2-cards-c154-c156", "cards FC1-c154, c155, c156", "cards.json; L04.html lines 67, 94", P,
    "c154 (earlier fill at 1010, last fill 1000, stop 1005): Remark 1.2 line 67 example. c155 (check repeats until no stop triggers): Remark 1.2 line 67. c156 (only unfilled shares of market orders are cancelled): A2 line 94.")
row("FC1-b-r1-labs-runtime-seed-network", "labs seeded, no network, under 10 s", "tests/labs/FC1/lab-FC1-L04-1.py, lab-FC1-L05-1.py", P,
    "L04 SEED = 2026 (twin line 18), L05 SEED = 2026 (line 135), random.Random(SEED) only; no file or network I/O (grep import list: random, collections, dataclasses, datetime, itertools, collections.abc). page_smoke lab timing 0.0 s each; numbers_r5.out shows both twins run.")
row("FC1-b-r1-lab-prose-consistency", "lab hypothesis and interpretation vs output", "L04.html lines 126, 358; L05.html lines 109, 390", P,
    "Hypotheses (L04 126: fixtures A and B, 300 events, both counts zero; L05 109: 10117, 216, 10060, 2172960, offset 0/2, Friday 2026-10-30, 68398886, 14282414, 0.209, three payers, sum zero) match printed output line by line (numbers_r5.out). Interpretations (L04 358, L05 390) name only printed numbers and model rules.")
row("FC1-b-r1-misconceptions-canon", "misconceptions and canon-breaks text", "L04.html lines 364-368, 375-386; L05.html lines 397-401, 409-425", P,
    "Each misconception's correction re-derived: L04 (market order 1000/1100/1060; stop fills at 985; size plays no part, 10-share first); L05 (settlement at offset 2 in the lab only; net payments 14282414 vs gross 68398886; CCP zero is an identity under A2; trade at 10060, not 10117). Canon-breaks claims (no venue rules, A2 needed, no margin/default) are statements about the model and match the code.")
row("FC1-b-r1-inline-style", "inline style on quiz fieldsets", "L04.html lines 517, 526, 545, 555, 569, 578", P,
    "Inline style 'min-inline-size: 0' on fieldsets; no change in this delta (diff between edbb7aa8 and dde0486b touches L04 lines 423, 501, 551 only). check_pages and page_smoke (360 px, no horizontal scroll) PASS.")
row("FC1-b-r2-math-L04-prop22-stop-arrival", "Prop 2.2 covers stop activations", "L04.html lines 99, 104", P,
    "Proof (line 104): a stop that arrives and does not activate leaves the book unchanged; an activated buy stop is a market buy and the market case covers it. Twin activate() calls match() with kind 'market' (twin line 117-118). Consistent.")
row("FC1-b-r2-def12-order-entry-offset", "order entry, matching and trade capture at offset 0", "L05.html line 63; quiz explanation line 562; twin lines 205-217", P,
    f"Definition 1.2 line 63 states offset 0 for order entry, matching and trade capture; twin states list (205-217) uses offset 0 for those three; printed lines 374-376 of expected block agree; quiz line 562 explanation cites Definition 1.2.")
row("FC1-b-r2-canon-needs-empty-start", "canon-breaks: crossed start fails", "L04.html line 367; R2 lines 479-483", P,
    "Line 367 says Prop 2.2 needs an uncrossed start that A1 gives. R2 (480-482) book with bid 1005 and ask 1000, buy 5 at 999 rests (no trade since 1000 > 999), best bid stays 1005 >= 1000: crossed. Re-derived.")
row("FC1-b-r2-A2-consistency", "A2 and A1 labels used consistently inside each lesson", "L04.html lines 51, 92-95, 109, 116, 126, 358, 365, 504-505; L05.html line 90", P,
    "Within L04, A1 is the empty start and A2 the no-withdrawal rule everywhere they are used (lines 51, 93-94, 99, 109, 365, 367). Within L05, A1 is the distinct-parties and positive-integer rule and A2 the novation rule (lines 79, 90, 399, 419). Labels are lesson-local; notation.json only registers program-wide symbols. Cards c066, c135, c156 agree with L04; c079, c080 agree with L05.")
row("FC1-b-r2-terms-before-definition", "terms used before definition", "L04.html lines 51, 60-61; L05.html lines 52, 58, 63, 66", P,
    "L04: 'resting order' (60) and 'last trade price' (61) are pointed to Remark 1.2 explicitly; 'crossed' defined at line 84 and used in the why-it-matters overview (51) as a forward summary. L05: 'CCP' pointed to Definition 1.1 at line 52 and defined at 58; 'settlement lag' pointed to Definition 1.2 at 52 and defined at 63; 'business day' defined at 63 before use in the same definition.")
row("FC1-b-r2-cross-reference-style", "cross-reference style and self-references", "L04.html lines 37, 51, 59-61; L05.html lines 38-39, 52, 66, 400", P,
    "Self-references such as 'Lesson 4, Definition 2.1' (L04 lines 51, 59) and 'Lesson 4, Definition 2.1' (L05 lines 66, 400) name the lesson and item and point to an earlier or same-lesson definition; links to other lessons point backwards only (check_dag PASS).")
row("FC1-b-r4-L05-why-market-claim", "L05 why-it-matters claim about markets", "L05.html line 52", P,
    "FIXED since round 4. Line 52 now opens 'In this lesson's model, a trade is not finished when the two sides agree on a price'; the settlement lag is stated as a parameter and the lesson 'states no settlement period for any market'. No market fact is asserted.")
row("FC1-b-r4-L04-why-it-matters", "L04 why-it-matters: word count and claims", "L04.html line 51", P,
    f"116 words (numbers_r5.out, limit 120). Claims: order types and the book under price-time priority; Prop 2.2 (under A1); Prop 2.3 (with A2); Lab 1 checks both invariants after each of 300 simulated events (twin main lines 176-188).")
row("FC1-b-r4-hours", "lesson hours and hub split", "course/modules/FC/FC1/index.html line 29; L04.html lines 2 and 34; L05.html lines 2 and 35", P,
    "L04 and L05 data-hours=10 and eyebrow '10 study hours'. Hub main data-hours-lessons=50 data-hours-project=20 (index.html line 29), so 5 x 10 = 50 and 50 + 20 = 70 = curriculum. Hub edit in this delta (prerequisites wording) does not touch hours. check_pages hours rule PASS.")
row("FC1-b-r3-lesson-links", "lesson navigation links", "L04.html lines 596-597; L05.html lines 649-650", P,
    "L04 line 596 Previous L03.html, line 597 Next L05.html; L05 line 649 Previous L04.html, line 650 Next project.html. All targets exist.")
row("FC1-b-r5-delta-L05-hunks", "delta: every L05 hunk since edbb7aa8 read and re-derived", "L05.html 11 hunks at new lines 50-52, 64-66, 98-100, 398-400, 417-419, 466-470, 486-488, 538-546, 593-595, 600-602, 608-610 (diff edbb7aa8..dde0486b)", P,
    f"git diff edbb7aa8 dde0486b -- course/modules/FC/FC1/L05.html (16 insertions, 16 deletions, 11 hunks) read in full. Each changed sentence re-derived: rows FC1-b-r4-L05-why-market-claim, FC1-b-r4-key-result-L05-541-hypothesis, FC1-b-r4-key-result-NP-hypothesis, FC1-b-r1-math-L05-prop21-prop22, FC1-b-r1-num-L05-prose, FC1-b-r2-A2-consistency. L05 lab twin unchanged (git diff shows no change to tests/labs/FC1/lab-FC1-L05-1.py).")
row("FC1-b-r5-delta-L04-hunks", "delta: every L04 hunk since edbb7aa8 read and re-derived", "L04.html hunks at lines 423, 501-505, 551 (diff edbb7aa8..dde0486b)", P,
    "git diff edbb7aa8 dde0486b -- course/modules/FC/FC1/L04.html (3 insertions, 3 deletions, 3 hunks) read in full: P1 solution convention (425), key-result row 503 'Under A1' and 'Under A1, Proposition 2.2' explanation (551). Re-derived in rows FC1-b-r4-P1-empty-side-convention, FC1-b-r4-key-result-L04-503-hypothesis. The L04 twin is unchanged (tests/labs/FC1 changes in this delta are lab-FC1-project-2.py only, not in this slice).")
row("FC1-b-r5-delta-cards-hunks", "delta: cards.json hunks since edbb7aa8", "course/modules/FC/FC1/cards.json (120 changed lines; L04 c099 and c169; L05 c164-c168; L02/L03 c157-c162, c170 and text edits)", P,
    f"git diff edbb7aa8 dde0486b -- cards.json read in full. In-slice changes verified: c099 (row FC1-b-r4-card-c099-changed-text), c169 (L04, row FC1-b-r1-cards-L04: 10 shares, 90 filled, Example 1.3), c164-c168 (L05, row FC1-b-r1-cards-L05). Out-of-slice (L01-L03) hunks were read for duplicates and locators only ({O}/cards_scan_r5.out); their content belongs to slices a and c.")
row("FC1-b-r5-quiz-L04-L05", "retrieval quiz keys and explanations", "L04.html lines 511-586 (9 items); L05.html lines 550-640 (11 items)", P,
    "Keys re-derived: L04 Q1 market order; Q2 sell stop at or below 990; Q3 1060 (159000/150); Q4 10 (100-90); Q5 crossed; Q6 100-share sell (earlier arrival); Q7 42 (24+18); Q8 two orders; Q9 A1. L05 Q1 order entry offset 0; Q2 10060; Q3 2172960; Q4 30 (Friday 2026-10-30); Q5 zero sum; Q6 between zero and gross; Q7 0.2088 (true 0.2088106, tolerance 0.00005); Q8 zero; Q9 3; Q10 no market period; Q11 1009000. Explanations cite existing items (Definition 1.1, 2.1, 1.2, Example 1.3, Problem R2/R3, Section 4, Remark 2.3 via 'Proposition 2.1').")
row("FC1-b-r5-lab05-printed-checks", "printed 'check' lines in L05 that are true by construction", "tests/labs/FC1/lab-FC1-L05-1.py lines 189-203; L05.html line 572 (quiz explanation)", P,
    "Twin prints trade_price_is_resting_price and consideration_check (lines 202-203). Both are True by construction: the Trade is built with best.price_cents (line 198) and cash = trade.consideration_cents (line 199). These lines are not evidence of the matching rule beyond the code. No page sentence presents them as a test; the quiz explanation (572) only quotes the printed True alongside the rule. Recorded as a note, not a defect.")
row("FC1-b-r5-cards-full-scan", "full card file scan (168 cards)", "course/modules/FC/FC1/cards.json", P,
    f"{O}/cards_scan_r5.out: 168 cards, unique ids and fronts. Locator misses for 'Assumption A1/A3' in L03 cards c038/c106 and 'Assumption A2/A3' in L01 cards c110/c111 are grouped labels ('Assumptions A1 to A3' at L03 line 78; 'Assumptions A1 to A3 below hold' at L01 line 73), not defects. Out of slice; recorded only.")

fragment = {
    "unit": "FC1",
    "slice": "FC1-b",
    "round": 5,
    "verifier": "Claude Haiku 5.5, independent verifier for FC1-b round 5 (did not build FC1; read verifier-rules.md, VERIFIER_RULES.md, BUILDER_RULES.md, notation.json, plans/FC1-build-plan.md incl. architect decisions; round-4 fragment as context only)",
    "pin": "dde0486beeb0312e4ac1cc03aaa02e56644adb24",
    "base": "edbb7aa8d20e6d2f3035c463a79a318c22623c4 (round-4 pin, fragment /Users/billyribeiro/.fanout/frags/S-FC1-b.round4.json)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyS5-FC1-b",
    "scratch": "ledgers/FC1/scripts/FC1-b-r5/",
    "verified_at": datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat(),
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [
        "harris2002trading: curriculum yaml line 385 reads 'Harris, Trading and Exchanges (2003)'; the registry record (Crossref) reads 2002. Pages cite the key with registry fields only (architect decision). The curriculum string should be corrected by its owner; no registry edit is requested."
    ],
    "freshness_flags": [],
    "notes": [
        "Delta since round 4 (edbb7aa8..dde0486b) in the slice: L04.html (6 lines, 3 hunks), L05.html (32 lines, 11 hunks), cards.json (120 lines). tests/labs/FC1/lab-FC1-L04-1.py and lab-FC1-L05-1.py are byte-identical to the round-4 pin (only lab-FC1-project-2.py changed in tests/labs/FC1). notation/, references/references.json and tools/ are unchanged in the delta.",
        "All four round-4 non-PASS rows (FC1-b-r4-key-result-NP-hypothesis, FC1-b-r4-key-result-L04-503-hypothesis, FC1-b-r4-key-result-L05-541-hypothesis, FC1-b-r4-P1-empty-side-convention) and FC1-b-r4-L05-why-market-claim were re-verified from scratch and are fixed (PASS). No row was carried from round 4: every subject was re-run this round.",
        "New FAIL this round: FC1-b-r1-attribution-harris (LOW, wording). The L04 line 590 sentence attributes a subtitle to the curriculum that the curriculum string does not contain. The round-4 verifier passed this row; this round's full read found it.",
        "Ruling 26: the single non-PASS row is LOW (wording). No blocking row.",
        "Gates re-run at dde0486b: check_pages (L04, L05, unit), check_dag, check_projects (unit), run_labs (L04, L05, unit: 8/8), twins alone under python -I -W error, page_smoke (--pages L04 L05), ruff check and format, mypy --no-incremental on both twins, pytest test_labs/test_run_labs/test_page_checks/test_curriculum (all pass), build_site --check, verify_refs --offline (560 entries, 0 problems) and verify_refs --unit FC1 live (2 of 560, 0 problems). Scripts under ledgers/FC1/scripts/FC1-b-r5/ (gates.sh, numbers_r5.py, l05_variants_r5.py, cards_scan_r5.py, build_fragment_r5.py).",
        "Lab statements vs code: both labs' statements match their code and printed output. The L05 lab's trade_price_is_resting_price and consideration_check lines are true by construction (row FC1-b-r5-lab05-printed-checks, note only).",
        "Mutants: none. The slice is lessons and cards; mutation testing applies to project graders only (ruling: lab twins are demonstrations).",
        "Judgement calls recorded, not rows: 'Lesson 4, Definition 2.1' self-references in L04/L05; lesson-local A1/A2 labels; the non-decreasing offsets convention (L05 line 66); key-result row L05 line 539 states Prop 2.1(i) without A1 (its proof uses no assumption, so the weaker statement is true and graded T correctly).",
        "Out-of-slice items read only for duplicates and locators: L01-L03 cards and hub edits (slices a and c). Hub index.html line 29 hours were checked here because the hours row is in this slice.",
        "ledgers/FC1/scripts/FC1-b-r5/ already held tracked files from an earlier campaign (commit 9fd6aedd: base_L05.out, build_fragment.py, check_L04_r5.py, check_L05_r5.py, compare_twin.py, gates.out, variant_*.py/out, etc.). They were left untouched; this round's scripts and outputs are the untracked files named in the rows (gates.sh, numbers_r5.py, l05_variants_r5.py, cards_scan_r5.py, textscan_r5.py, build_fragment_r5.py, out/).",
        "The committed ledgers/FC1/FC1-b.json in this checkout (an older round-7 fragment) was overwritten by this round-5 fragment, as the round-5 instruction requires. Nothing was committed or pushed.",
    ],
    "summary": "",
}
counts = {"PASS": 0, "FAIL": 0, "UNVERIFIABLE": 0}
for r in rows:
    counts[r["status"]] += 1
fragment["summary"] = (
    f"FC1-b round 5 at dde0486b: {len(rows)} rows, {counts['PASS']} PASS, {counts['FAIL']} FAIL, "
    f"{counts['UNVERIFIABLE']} UNVERIFIABLE. Non-PASS: FC1-b-r1-attribution-harris (LOW, wording). "
    "Round-4 non-PASS rows (NP hypothesis, L04-503, L05-541, P1 empty side, L05 why-it-matters) re-verified and fixed. "
    "All gates re-run and green. Mutants: none (lessons)."
)
out = ROOT / "ledgers/FC1/FC1-b.json"
out.write_text(json.dumps(fragment, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("wrote", out, counts, len(rows))
