import json, datetime, pathlib, sys
D = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyS6-FC1-b")
O = "ledgers/FC1/scripts/FC1-b-r6/out"
PASS, FAIL = "PASS", "FAIL"
rows = []
def R(id_, check, location, evidence, status=PASS, fix=""):
    rows.append({"id": id_, "check": check, "location": location, "status": status, "evidence": evidence, "fix": fix})

# ---- gates (all re-run at e896b7a4) ----
R("FC1-b-r1-gate-check-pages", "tools/check_pages.py --unit FC1 --page L04; --page L05; --unit FC1",
  "course/modules/FC/FC1/L04.html, L05.html, cards.json",
  f"Re-run at e896b7a4: {O}/check_pages_L04.out 'check_pages FC1 L04: PASS', check_pages_L05.out 'check_pages FC1 L05: PASS', check_pages_unit.out 'check_pages FC1: PASS' (rc 0 each in {O}/*.rc).")
R("FC1-b-r1-gate-check-dag", "tools/check_dag.py --unit FC1", "L04.html line 37; L05.html lines 38-39, 58, 63",
  f"{O}/check_dag_FC1.out 'check_dag FC1: PASS' (rc 0). L04 line 37 links L03#def-bid-ask-spread; L05 lines 38-39 link L04#def-order-types, L04#def-limit-order-book, L01#def-financial-intermediary and define def-clearing-and-settlement (line 58) and def-trade-lifecycle (line 63) on the page.")
R("FC1-b-r1-gate-run-labs", "tools/run_labs.py --unit FC1 --page L04 / --page L05 / --unit FC1", "tests/labs/FC1/lab-FC1-L04-1.py, lab-FC1-L05-1.py",
  f"{O}/run_labs_L04.out 'run_labs FC1: PASS (1/1)'; run_labs_L05.out 'PASS (1/1)'; run_labs_unit.out 'PASS (8/8)'; all rc 0.")
R("FC1-b-r1-gate-twin-alone", "twin run alone: python -I -W error, no network, cwd /tmp", "tests/labs/FC1/lab-FC1-L04-1.py, lab-FC1-L05-1.py",
  f"{O}/twin_r6.out: 'L04 twin rc=0 stderr_bytes=0' and 'L05 twin rc=0 stderr_bytes=0'. Twin imports are random, collections, dataclasses, datetime, itertools, collections.abc only (grep of import lines).")
R("FC1-b-r1-gate-page-code-equals-twin", "page code (unescaped) equals twin, trailing newlines aside", "L04.html lines 127-335; L05.html lines 110-364",
  f"{O}/twin_r6.out: 'L04 page code == twin (trailing newlines aside): True' (208 vs 209 lines incl. final newline), 'L05 ... True' (255 vs 256 lines).")
R("FC1-b-r1-gate-expected-equals-output", "expected block equals the twin's stdout", "L04.html lines 336-357; L05.html lines 366-389",
  f"{O}/twin_r6.out: 'L04 expected == output: True' (22 lines), 'L05 expected == output: True' (24 lines).")
R("FC1-b-r1-gate-page-smoke", "tools/page_smoke.py --unit FC1 --pages L04 L05", "L04.html, L05.html",
  f"{O}/page_smoke_L04_L05.out: 'page_smoke modules/FC/FC1/L04.html: PASS', 'page_smoke modules/FC/FC1/L05.html: PASS', 'page_smoke FC1: PASS'; rc 0.")
R("FC1-b-r1-gate-ruff", "ruff check and ruff format --check on both twins", "tests/labs/FC1/lab-FC1-L04-1.py, lab-FC1-L05-1.py",
  f"{O}/ruff_check.out 'All checks passed!' (rc 0); ruff_format.out '2 files already formatted' (rc 0).")
R("FC1-b-r1-gate-mypy", "mypy --no-incremental on both twins", "tests/labs/FC1/lab-FC1-L04-1.py, lab-FC1-L05-1.py",
  f"{O}/mypy_twins.out 'Success: no issues found in 2 source files' (rc 0).")
R("FC1-b-r1-gate-pytest-labs", "pytest tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py tests/test_curriculum.py", "tests/test_labs.py, tests/test_run_labs.py, tests/test_page_checks.py, tests/test_curriculum.py",
  f"{O}/pytest_labs.out: all tests reported as passing with no failure lines (the -q summary line is not printed by this configuration); rc 0.")
R("FC1-b-r3-gate-build-site-check", "tools/build_site.py --check", "course/assets/data, course/index.html, course/concepts.html",
  f"{O}/build_site_check.out 'site data current: 6 outputs' (rc 0).")
R("FC1-b-r1-gate-verify-refs-offline", "tools/verify_refs.py --offline", "references/references.json",
  f"{O}/verify_refs_offline.out 'offline integrity: 560 entries, 0 problems' (rc 0).")
R("FC1-b-r2-gate-verify-refs-live-unit", "tools/verify_refs.py --unit FC1 (live)", "references/references.json: harris2002trading",
  f"{O}/verify_refs_unit_live.out 'live re-verification of FC1: 2 of 560 entries, 0 problems' (rc 0).")
R("FC1-b-r4-gate-check-projects-unit", "tools/check_projects.py --unit FC1", "course/modules/FC/FC1/project.html (unit gate)",
  f"{O}/check_projects_FC1.out 'check_projects FC1: PASS' (rc 0).")

# ---- numbers and math ----
R("FC1-b-r1-num-L04-prose", "every number in L04 prose recomputed", "L04.html lines 72, 77, 126, 377-385, 398-414, 423-439, 450-464, 475-489, 501-505, 536, 541, 563-565, 574",
  f"{O}/numbers_r6.out (159000/150=1060; 60*995+40*990=99300, 993; 1000*60+1100*90=159000; {O}/l04_problems_r6.out: M1 fills (995,60),(990,40), bid 990 keeps 60; M2 fills (1000,30),(1001,20), asks left 10@1001 and 40@1003; M3 stop not active at last 1001, active at last 1000; P2 G=250, X=100, C=50, R=0; R1 fills (990,100),(985,100),(980,100), 2 activations; R2 crossed True (bid 1005, ask 1000); R3 traded 60, 2X=120. Event counts 42 = 24+18 match lab output lines 352-353.")
R("FC1-b-r1-num-L04-lab-output", "lab output and interpretation numbers", "L04.html lines 336-357 (expected), 358 (interpretation), 505 (key result)",
  f"Expected block equals twin stdout (twin_r6.out). Interpretation line 358: fills (1000,60),(1100,90), cost 159000, average 1060; fills (990,100),(985,100); best bid 9984 after events 0-6 and none after event 7 (expected lines 344-351); 0 crossed and 0 conservation failures (lines 355-356). Key-results line 505 matches.")
R("FC1-b-r1-num-L05-prose", "every number in L05 prose recomputed", "L05.html lines 75, 109, 390, 438, 445, 452, 488, 495, 502, 544, 582, 605-607, 637",
  f"{O}/numbers_r6.out: NP/G = 14282414/68398886 = 0.20881062302681364 (8dp 0.20881062; 5dp 0.20881; 3dp half-up 0.209); P5/G = 16.1704% -> 16.17; P5/NP = 77.4404% -> 77.44; 216*10060=2172960; net negatives 7411991+6656379+214044 = 14282414 = positives 3222054+11060360; 2026-10-28 Wednesday, 2026-10-30 Friday, 2026-11-02 Monday. M1 consideration 1009000; M2 and E3 date arithmetic checked against business_day_after logic.")
R("FC1-b-r1-num-L05-lab-output", "lab output and hypothesis numbers", "L05.html lines 109 (hypothesis), 366-389 (expected), 390 (interpretation)",
  f"Expected block equals twin stdout (twin_r6.out, 24 lines). Hypothesis line 109 numbers match output: P2 263 shares at 10060 resting, P1 216 at limit 10117, one fill of 216 at 10060, consideration 2172960, settlement 2026-10-30, gross 68398886, net 14282414, ratio 0.209, 3 net payers, sum 0.")
R("FC1-b-r1-lab05-parameter-claims", "claims about CLEARING_OFFSET and SETTLEMENT_LAG effects on printed output", "L05.html line 66, line 390, lines 500-502 (E3); card FC1-c142",
  f"Variants run from the twin with one constant changed (ledgers/FC1/scripts/FC1-b-r6/variants/): lag3.out changes only the header, the settlement and position_update lines (offset 3, Monday 2026-11-02), offsets_nondecreasing stays True. clr3.out changes the header and the clearing line (offset 3, Monday 2026-11-02) and prints offsets_nondecreasing False. clr2.out (clearing equal to lag) prints True. Matches lines 66, 390 and 500-502.")
R("FC1-b-r1-lab04-invariant-claim", "claim that Lab 1 checks both invariants after each of 300 events", "L04.html lines 51, 126, 358, 505; L04.html code lines 293-332 (main())",
  f"main() checks uncrossed (bid >= ask) and submitted == resting + 2*traded + cancelled after every event (L04.html code lines 299-314). Output lines 355-356 print 0 and 0; expected block equals output.")
R("FC1-b-r1-math-L04-examples-problems", "worked examples and problems re-derived by running the lab's own Book class", "L04.html lines 72, 77, 377-385, 398-491",
  f"{O}/l04_problems_r6.out (exec of the twin without its final main() call). Results match every printed fill, average and remaining quantity in Examples 1.3-1.4, Misconceptions 1-3, and problems M1-M3, P2, R1-R3.")
R("FC1-b-r1-math-L05-prop21-prop22", "proofs of Propositions 2.1 and 2.2 and Remark 2.3", "L05.html lines 75-96, 100, 468-470, 518-520",
  "Read line by line. Prop 2.1(i) telescopes to zero; (ii) uses A1 (positive integers, so c_i >= 0) for NP >= 0 and NP <= sum Pay_j = G. Prop 2.2 proof: CCP receives G, pays G; x_j = Rec_j - Pay_j. P2 (lines 467-470) bracket argument checked: f(x)=max(-x,0) is non-increasing and 1-Lipschitz. R2 counterexample: c=-100 gives NP=100 and G=-100 (out/c089_r6.out line 1).")
R("FC1-b-r1-math-L04-prop22-empty-side", "Proposition 2.2 empty-side convention", "L04.html lines 99, 104, 425",
  "Proof line 104 sets beta = -inf and alpha = +inf for empty sides, so 'crossed' is beta >= alpha; the market-buy and limit-buy cases use max(beta,p) < alpha' correctly. P1 (line 425) uses the same convention.")
R("FC1-b-r1-math-L04-prop23-assumptions", "Proposition 2.3 hypotheses", "L04.html lines 93-95, 107-117; card FC1-c066",
  "Statement line 109 is 'Assuming A2'; proof line 116 uses A2 (a resting order leaves the book only by trading). The stop clause (lines 111) excludes unactivated stops, consistent with the proof.")
R("FC1-b-r1-math-L04-remark-definitions", "Remark 1.2 and Definitions 1.1 and 2.1 against the code", "L04.html lines 56-67, 84-89, 197-220 (match), 222-246 (activate), 302-313 (main loop)",
  "Twin match() (197-220) fills at resting price, best price then earliest arrival; activate() (222-246) checks stops after matching with the last fill price, earliest arrival first, repeating until none triggers; main loop (302-313) activates after each event. All match Remark 1.2 and Definitions 1.1, 2.1 as stated.")
R("FC1-b-r3-proof-P1-hypothesis", "Problem P1 hypothesis", "L04.html line 423 (statement), line 425 (solution)",
  "P1 statement assumes the book is uncrossed before the arriving market buy (A1 gives it for the first event); solution uses only that a market buy removes asks and leaves bids unchanged, and states the empty-side convention.")
R("FC1-b-r4-key-result-NP-hypothesis", "key-results row for Prop 2.1 names its hypothesis", "L05.html line 540 (key-results row); Proposition 2.1 line 79; Problem R2 lines 518-520; card FC1-c101",
  "Line 540 reads 'Assuming A1, in a batch, net payments lie between zero and gross payments (Proposition 2.1(ii))' and matches the statement at line 79.")
R("FC1-b-r4-key-result-L04-503-hypothesis", "key-results row for Prop 2.2 (L04) names A1", "L04.html line 503 (key-results row); Prop 2.2 line 99",
  "Line 503 reads 'Assuming A1, the book is never crossed after any event (Proposition 2.2)', matching line 99.")
R("FC1-b-r4-key-result-L05-541-hypothesis", "key-results row for Prop 2.2 (L05) names A1 and A2", "L05.html line 541; Prop 2.2 line 90",
  "Line 541 reads 'Assuming A1 and A2 ... (Proposition 2.2)', matching the assumptions at line 90.")
R("FC1-b-r4-P1-empty-side-convention", "P1 empty-side convention", "L04.html line 425",
  "Solution at line 425 takes beta = -inf or alpha = +inf as in the proof of Proposition 2.2 (line 104).")
R("FC1-b-r1-grades", "grades on claims and cards", "L04.html lines 98, 108, 501-505; L05.html lines 78, 89, 539-544, 403; cards.json",
  "Proved statements graded T (Props 2.1-2.3, Prop 2.2 L04, Prop 2.2 L05); lab numbers graded C naming Lab 1 (SIMULATED); cards with grade T are proved or hand-computed; card FC1-c089 (grade T) is a counterexample card whose wording is the defect in its own row.")
R("FC1-b-r1-notation", "every symbol against notation/notation.json", "L04.html and L05.html inline math (95 and 120 expressions)",
  f"{O}/notation_process_r6.out: the 8 registered symbols (T, Phi, gamma_3, gamma_4, R*, R^e*, R_f, Q) occur 0 times in L04 or L05 math. Macros used are \\alpha, \\beta, \\infty (greek and infinity, not registry macros). Single-letter symbols (G, R, X, C, p, q, s, t in L04; A, B, C, G, J, K, c, f, n, x in L05) are defined locally where first used.")
R("FC1-b-r1-prose-process-words", "no process words in learner text", "L04.html, L05.html, cards.json",
  f"{O}/notation_process_r6.out: zero hits for we, round, verif, builder, draft, placeholder, TODO, lorem in L04, L05 and cards.json.")
R("FC1-b-r1-prose-banned-phrases", "banned phrases (BUILDER_RULES 1.3-1.4)", "L04.html, L05.html, cards.json",
  f"{O}/check_pages_L04.out and check_pages_L05.out PASS include the banned-string check; cards.json scan in {O}/cards_r6.out.")
R("FC1-b-r1-structure-L04", "page structure and quiz", "L04.html", "check_pages PASS; data-hours=10 (line 2); sections 1-8 in order; 9 quiz items (lines 511-585) with one correct option each and explanations.")
R("FC1-b-r1-structure-L05", "page structure and quiz", "L05.html", "check_pages PASS; data-hours=10 (line 2); sections 1-9 in order; 11 quiz items (lines 550-638) with one correct option each and explanations; section 4 is the 'Section 4' cited by quiz item L05q10.")
R("FC1-b-r1-scope-words", "scope words (only, all, always, every, any, exactly) backed by computation or hypothesis", "L04.html lines 67, 126, 358, 364, 475, 505; L05.html lines 63, 70, 390, 399, 401",
  "'Only the last trade price' (L04 67) is the Remark 1.2 rule and matches the code (activate uses self.last); 'every run from A1' (L04 358) is Prop 2.2 with its proof; 'exactly this sequence' (L04 475) is R1, reproduced by the twin Book class; L05 390 and 399 'no timing fact' and 'no finding' are scope limits, not universals.")
R("FC1-b-r1-attribution-harris", "bibliographic attribution against curriculum string and registry record",
  "L04.html line 590; L05.html line 403; references/references.json key harris2002trading; curriculum/02-economics-finance-core.yaml lines 383-386 (Harris at line 385)",
  "L04 line 590 attributes 'Harris, Trading and Exchanges' to the curriculum, which the yaml does (line 385 'Harris, Trading and Exchanges (2003)'); the subtitle and year 2002 are attributed to the registry record, whose title is 'Trading and Exchanges: Market Microstructure for Practitioners' and year 2002 (references.json). The round-5 defect (subtitle attributed to the curriculum) is fixed. L05 line 403 locator 'yaml 383-386' is correct; the registry year is cited as the registry's, not as the curriculum's. The curriculum-vs-registry year conflict is the registry flag below, not a page defect.")
R("FC1-b-r1-settlement-source-absence", "no settlement period stated for any market", "L05.html lines 52, 105, 397, 513, 632; card FC1-c090; references/references.json",
  "Each line presents the two-day lag as the lab's parameter (lines 52, 105, 397) and the R1 solution (513) says no source is named; quiz item L05q10 (line 629) answers 'No'. No registry key gives a settlement cycle.")
R("FC1-b-r1-references-L05", "L05 references render from registry", "L05.html line 403 and line 644; course/assets/js/refs.js lines 68-90",
  "L05 line 403 data-cite=harris2002trading resolves in references.json (verify_refs offline: 560 entries, 0 problems). Section 9 renders via refs.js renderCitations, which fetches references.json and fails on a missing key.")
R("FC1-b-r1-references-L04-empty-list", "L04 references section", "L04.html lines 588-592; course/assets/js/refs.js",
  "Section 8 holds <ol data-references></ol> (line 591) and the registry citation at line 590 with data-cite; refs.js fills it from references.json.")

# ---- cards ----
R("FC1-b-r1-cards-L04", "L04 cards agree with current lesson text", "course/modules/FC/FC1/cards.json (lesson L04: c056-c072, c099, c100, c119, c121, c132, c133, c135, c141, c143, c154-c156, c169, c171)",
  f"{O}/cards_r6.out lists each L04 card; each was compared with the lesson line it cites (Definition 1.1, Remark 1.2, Example 1.3-1.4, Definition 2.1, Proposition 2.2-2.3, Problems R2-R3, quiz). New card FC1-c171 (line 1096) asks for the average price 1060 cents, which appears in Example 1.3 (line 72). FC1-c061 (line 398) now asks the cost 159000 cents, which appears in Example 1.3. No card disagrees with the lesson.")
R("FC1-b-r1-cards-L05", "L05 cards agree with current lesson text", "course/modules/FC/FC1/cards.json (lesson L05: c073-c090, c101, c102, c109, c114, c118, c123, c124, c142, c144, c145, c164-c168, c172)",
  f"{O}/cards_r6.out lists each L05 card. FC1-c075 (line 488) now says matching and trade capture have offset 0, which matches Definition 1.2 (line 63). FC1-c082 (line 532) no longer states the consideration; FC1-c172 (line 1103) states 2172960 cents, which the twin prints as consideration_cents and the lesson states at lines 109, 541, 577. FC1-c090 (line 593) matches Section 4. FC1-c089 (line 586) is the defect in row FC1-b-r6-card-c089-negative-consideration.", status=FAIL,
  fix="See FC1-b-r6-card-c089-negative-consideration. The other L05 cards agree with the lesson.")
R("FC1-b-r1-cards-duplicates", "no duplicate card ids, fronts or backs", "course/modules/FC/FC1/cards.json",
  f"{O}/cards_r6.out: 170 cards; duplicate ids [], duplicate fronts [], duplicate backs []; key sets consistent (grade and basis present where graded C).")
R("FC1-b-r1-card-c066", "card FC1-c066 against Proposition 2.3", "cards.json FC1-c066 (line 1 of its entry); L04.html lines 92-95, 108-111",
  "Card: 'Under A2 (no withdrawals), G = R + 2X + C after every event, where C is the shares cancelled from market orders (Proposition 2.3).' Matches statement line 109-110 and assumption A2 lines 93-94. Grade T matches.")
R("FC1-b-r4-card-c099-changed-text", "card FC1-c099 against the changed Proposition 2.2 text", "cards.json FC1-c099 (line 697); L04.html line 99",
  "Card says 'Under A1, the book starts empty, and under the matching rules of Section 1 it is not crossed after any event, where an event is an arrival or an activation of a stop (Proposition 2.2).' Matches line 99 'Assuming A1 and the rules of Section 1 ... an event is an arrival or an activation of a stop'.")
R("FC1-b-r2-cards-c154-c156", "cards FC1-c154 to c156 against Remark 1.2 and A2", "cards.json; L04.html lines 67, 94",
  "c154 (1010 / 1005 / 1000 example) matches Remark 1.2 at line 67; c155 matches the repeat rule at line 67; c156 matches A2 at line 94 (only unfilled market-order shares are cancelled).")
R("FC1-b-r1-labs-runtime-seed-network", "labs use SIMULATED seeded data, no network", "tests/labs/FC1/lab-FC1-L04-1.py, lab-FC1-L05-1.py",
  f"Both twins import only standard-library modules (imports listed in twin_r6 run) and run with -I -W error and no network (twin_r6.out rc 0, stderr 0 bytes). Seed 2026 and SIMULATED labels present (L04 line 126; L05 line 109).")
R("FC1-b-r1-lab-prose-consistency", "lab prose matches printed output", "L04.html lines 126, 358; L05.html lines 109, 390",
  "Each printed fact named in prose (fills, counts, trace, ratio, offsets_nondecreasing, net_payments_at_most_gross) appears in the expected block (twin_r6.out).")
R("FC1-b-r1-misconceptions-canon", "misconceptions and canon-breaks", "L04.html lines 364-368, 375-386; L05.html lines 397-401, 409-425",
  "L04 misconceptions 1-3 match Example 1.3, Example 1.4 and Definition 2.1 with the 10-share example. L05 misconceptions 1-4 match the lab's printed values (SETTLEMENT_LAG, 14282414 vs 68398886, 10117 vs 10060). Canon-break text states no venue rule; no claim contradicts the printed output.")
R("FC1-b-r1-inline-style", "inline style attributes", "L04.html lines 517, 526, 545, 555, 569, 578",
  "Only fieldset style='min-inline-size: 0' is used, which is a layout reset on the quiz fieldset and does not change any learner-visible claim.")
R("FC1-b-r2-math-L04-prop22-stop-arrival", "Proposition 2.2 stop-arrival case", "L04.html lines 99, 104",
  "Proof line 104 covers 'a stop that arrives and does not activate' (unchanged book) and 'a buy stop that activates is a market buy'. Matches statement line 99 'An event is an arrival or an activation of a stop'.")
R("FC1-b-r2-def12-order-entry-offset", "order-entry offset 0 and trade-date definition", "L05.html line 63; quiz explanation line 562; twin lines 205-217",
  "Definition 1.2 (line 63): order entry, matching and trade capture on the trade date, offset 0. The lab's order_entry, matching and trade_capture states print offset 0 (expected block lines 374-376, twin_r6.out). Quiz explanation line 562 matches.")
R("FC1-b-r2-canon-needs-empty-start", "canon-break on the empty start", "L04.html line 367; R2 lines 479-483",
  "Line 367 states Proposition 2.2 needs the uncrossed start that A1's empty book gives; R2 (lines 479-483) shows the crossed-start counterexample, reproduced by the Book class (crossed True).")
R("FC1-b-r2-A2-consistency", "A2 used consistently", "L04.html lines 51, 92-95, 109, 116, 126, 358, 365, 504-505; L05.html line 90",
  "A2 is 'no withdrawals' in L04 (lines 93-94) and the CCP conditions in L05 (line 90); both uses match their statements. Line 51 'Assuming A2' is consistent with Proposition 2.3 at line 109.")
R("FC1-b-r2-terms-before-definition", "terms used before definition", "L04.html lines 51, 60-61; L05.html lines 52, 58, 63, 66",
  "Forward uses (limit book, last trade price, resting order, CCP, netting) carry an explicit pointer to the defining item (Definition 2.1, Remark 1.2, Definition 1.1, Definition 1.2). Netting is defined in Definition 1.1 text (line 58) before Section 2.")
R("FC1-b-r2-cross-reference-style", "cross-reference link style", "L04.html lines 37, 51, 59-61; L05.html lines 38-39, 52, 66, 400",
  "Concept links use class concept with data-concept and the defining page anchors; check_dag PASS (out/check_dag_FC1.out).")
R("FC1-b-r4-L05-why-market-claim", "L05 why-it-matters claim about trades not finished at agreement", "L05.html line 52",
  "Line 52: 'a trade is not finished when the two sides agree on a price', matched by Definitions 1.1-1.2 (lines 58-63) and the offsets in Section 1.")
R("FC1-b-r4-L04-why-it-matters", "L04 why-it-matters states the invariant and its definition", "L04.html line 51",
  "Line 51 now reads 'The book is never crossed, meaning its best bid is at least its best ask (Proposition 2.2, assuming A1).' This inverts Definition 2.1 (line 84: the book is crossed when the best bid is at least the best ask) and Proposition 2.2 (line 99). The sentence tells the learner the book is never at or above its best ask while defining 'crossed' as exactly that. The round-5 PASS is withdrawn because the text changed in this delta.",
  status=FAIL, fix="Change line 51 to: 'The book is never crossed, meaning its best bid is below its best ask (Proposition 2.2, assuming A1).'")
R("FC1-b-r4-hours", "hours arithmetic", "course/modules/FC/FC1/index.html line 29; L04.html lines 2 and 34; L05.html lines 2 and 35",
  "Hub data-hours-lessons=50 and data-hours-project=20 (index.html line 29), total 70 (line 31). Five lessons each data-hours=10 (L01-L05, grep of data-hours) gives 50; project 20 (project.html line 34 and time budget total 20). Arithmetic consistent.")
R("FC1-b-r3-lesson-links", "lesson navigation", "L04.html lines 596-597; L05.html lines 649-650",
  "L04 Previous -> L03.html and Next -> L05.html; L05 Previous -> L04.html and Next -> project.html. Links resolve (check_pages PASS).")

# ---- delta (dde0486b..e896b7a4) ----
R("FC1-b-r5-delta-L05-hunks", "every L05 hunk of the delta read", "L05.html hunks at lines 52, 79, 90, 100, 540, 541 (diff dde0486b..e896b7a4)",
  "All six hunks read and checked: 52 why-it-matters ('Assuming'/'(Definition 1.1)' wording is correct, the remaining sentences match Definitions 1.1-1.2); 79 and 90 'Assuming A1/A2' hypotheses match the proofs; 100 Remark 2.3 'Assuming A1' matches Proposition 2.1; 540-541 key-results rows match Propositions 2.1(ii) and 2.2.")
R("FC1-b-r5-delta-L04-hunks", "every L04 hunk of the delta read", "L04.html hunks at lines 51, 99, 503, 551, 590 (diff dde0486b..e896b7a4)",
  "Hunks 99, 503, 551 ('Assuming A1' wording) and 590 (references: curriculum 'Harris, Trading and Exchanges', registry title and year 2002) are correct. Hunk 51 is wrong: it states the book is never crossed 'meaning its best bid is at least its best ask', the inverse of Definition 2.1. See FC1-b-r4-L04-why-it-matters.",
  status=FAIL, fix="Fix line 51 as in FC1-b-r4-L04-why-it-matters; hunks 99, 503, 551, 590 need no change.")
R("FC1-b-r5-delta-cards-hunks", "every cards.json hunk of the delta read", "course/modules/FC/FC1/cards.json: c050 (line 324, L03), c061 (398), c075 (488), c082 (532), c090 (593), c171 (1096), c172 (1103)",
  "All hunks read. c050 (L03) checked against L03 Proposition 3.2 proof (L03.html line 158): undercut earns (k-1)N, tie earns kN/2, strict for k>2. c061 matches Example 1.3. c075, c082, c090 match Definition 1.2, the twin output and Section 4. c171 and c172 are new and agree with Example 1.3 and the twin's consideration_cents line. No hunk contradicts the lesson.")
R("FC1-b-r5-quiz-L04-L05", "quiz items and explanations", "L04.html lines 511-586 (9 items); L05.html lines 550-640 (11 items)",
  "Each correct option verified against the lesson (L04 q1 market order, q2 at-or-below, q5 crossed, q6 100-share sell, q8 2X, q9 A1; numeric 1060, 10, 42). L05 q1 order entry, q2 10060, q3 2172960, q4 30, q5 zero sum, q6 0<=NP<=G, q7 0.2088 (14282414/68398886 = 0.20881), q8 zero, q9 3, q10 no market, q11 1009000. Explanations match.")
R("FC1-b-r5-lab05-printed-checks", "L05 printed checks (trade_price_is_resting_price, consideration_check, offsets_nondecreasing) are true", "tests/labs/FC1/lab-FC1-L05-1.py (print calls at twin lines 202-203 and 240); L05.html line 572",
  f"{O}/twin_r6.out: expected block lines 372-373 and 380 print True, True, True; quiz explanation line 572 matches. The checks are true by construction (price is the resting price; consideration is quantity times price).")
R("FC1-b-r5-cards-full-scan", "full scan of cards.json for L03-L05 cards", "course/modules/FC/FC1/cards.json (all 170 cards read; L04/L05 cards read in full)",
  f"{O}/cards_r6.out (all L03-L05 cards printed and read); {O}/cards_numbers_r6.out 'scan complete' (every number on L03-L05 cards appears in its lesson text). One card is wrong: FC1-c089 (line 586), see FC1-b-r6-card-c089-negative-consideration.",
  status=FAIL, fix="See FC1-b-r6-card-c089-negative-consideration.")

# ---- new row this round ----
R("FC1-b-r6-card-c089-negative-consideration", "card FC1-c089 answers a general question with a single counterexample", "course/modules/FC/FC1/cards.json line 586 (FC1-c089)",
  f"Front: 'Does the bound NP <= G hold when one consideration is negative?' Back: 'No. With one trade of consideration -100 cents, ...'. {O}/c089_r6.out (run from the Section 2 definitions): one trade c=-100 gives NP=100, G=-100, bound false; but a trade of +100 and a trade of -50 between the same pair give NP=50, G=50, bound true. So a negative consideration does not always break the bound. The card's universal 'No' over-claims the scope of the R2 counterexample (scope-word defect, row category 4).",
  status=FAIL, fix="Change the back to: 'Not necessarily. The bound can fail: with one trade of consideration -100 cents, NP is 100 and G is -100 (Problem R2). The proof step Pay_j >= 0 is what needs non-negative considerations, so the bound is not guaranteed.'")

ids = [r["id"] for r in rows]
assert len(ids) == len(set(ids)), "duplicate ids"
nonpass = [r["id"] for r in rows if r["status"] != PASS]
verdict = "PASS" if not nonpass else "FAIL"
frag = {
  "unit": "FC1",
  "slice": "FC1-b",
  "round": 6,
  "verifier": "Claude Haiku 5.5, independent verifier for FC1-b round 6 (did not build FC1; read verifier-rules.md, CLAUDE.md, BUILDER_RULES.md via prior fragments and notation.json, plans/FC1-build-plan.md architect decisions; round-5 fragment as context only)",
  "pin": "e896b7a45344d1bc17ebfbf7fb05d87698ec9d6a",
  "base": "dde0486beeb0312e4ac1cc03aaa02e56644adb24 (round-5 pin; fragment /Users/billyribeiro/.fanout/frags/S-FC1-b.round5.json)",
  "checkout": "/Users/billyribeiro/.fanout/wt/verifyS6-FC1-b",
  "scratch": "ledgers/FC1/scripts/FC1-b-r6/",
  "verified_at": datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat(),
  "verdict": verdict,
  "rows": rows,
  "mutants": [],
  "registry_flags": ["harris2002trading: curriculum yaml line 385 reads 'Harris, Trading and Exchanges (2003)'; the registry record (Crossref) reads 2002. Pages cite the key with the registry's own fields only (architect decision). The curriculum string should be corrected by its owner; no registry edit is requested."],
  "freshness_flags": [],
  "notes": [
    "Delta since round 5 (dde0486b..e896b7a4) in the slice: L04.html (hunks 51, 99, 503, 551, 590), L05.html (hunks 52, 79, 90, 100, 540, 541), cards.json (c050 L03, c061, c075, c082, c090, c171 and c172 added). tests/labs/FC1 has no diff in this delta (twins byte-identical to the round-5 pin). Out of slice: project.html and grader/test_project.py changed in this delta; not verified here (slice b excludes them; FC1 project slices are covered elsewhere).",
    "No round-5 row was carried: every subject (L04.html, L05.html, cards.json) changed in the delta, so every row was re-derived this round from scratch. Row ids are kept; FC1-b-r1-attribution-harris is PASS again (fixed in e896b7a4).",
    "New defects found this round: FC1-b-r4-L04-why-it-matters (L04 line 51, inverted 'crossed' definition, MEDIUM) and FC1-b-r6-card-c089-negative-consideration (cards.json line 586, over-general 'No', LOW). Both are FAIL rows with fixes.",
    "Gates re-run at e896b7a4 (out/ directory): check_pages L04/L05/unit, check_dag, check_projects (unit), run_labs L04/L05/unit (8/8), twins alone under python -I -W error, page_smoke L04 L05, ruff check and format on the twins, mypy --no-incremental on the twins, pytest test_labs/test_run_labs/test_page_checks/test_curriculum, build_site --check, verify_refs --offline (560, 0 problems), verify_refs --unit FC1 live (2 of 560, 0 problems). All rc 0.",
    "Variants (ledgers/FC1/scripts/FC1-b-r6/variants/): SETTLEMENT_LAG=3, CLEARING_OFFSET=3, CLEARING_OFFSET=2 run from the twin; outputs diffed against the base run.",
    "Mutants: none. The slice is lessons and cards; mutation testing applies to project graders only (ruling: lab twins are demonstrations).",
    "The committed ledgers/FC1/FC1-b.json in this checkout (an older fragment) was overwritten by this round-6 fragment as the instruction requires. Nothing was committed or pushed.",
    "Judgement calls, not rows: 'Lesson 4, Definition 2.1' style self-references (L04 lines 37, 51, 59); lesson-local A1/A2 labels; the non-decreasing offsets convention (L05 line 66); card c087 has no grade (no claim is graded).",
  ],
  "summary": f"FC1-b round 6 at e896b7a4: {len(rows)} rows, {sum(1 for r in rows if r['status']==PASS)} PASS, {sum(1 for r in rows if r['status']==FAIL)} FAIL, 0 UNVERIFIABLE. Non-PASS: FC1-b-r4-L04-why-it-matters (MEDIUM, L04 line 51 inverted crossed definition), FC1-b-r6-card-c089-negative-consideration (LOW, cards.json line 586 over-general answer), and the two rows that cite them (FC1-b-r5-delta-L04-hunks, FC1-b-r5-cards-full-scan) and FC1-b-r1-cards-L05 (which lists c089). Mutants none.",
}
out = D / "ledgers/FC1/FC1-b.json"
out.write_text(json.dumps(frag, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("wrote", out, "rows", len(rows), "verdict", verdict, "nonpass", nonpass)
