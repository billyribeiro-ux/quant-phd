"""Writes ledgers/FC1/FC1-b.json (FC1-b round 4). Evidence strings cite scripts and outputs by repository path."""
import json
import sys
from datetime import datetime, timezone

root = sys.argv[1]
S = "ledgers/FC1/scripts/FC1-b-r4"
O = f"{S}/out"
rows = []


def row(rid, check, location, status, evidence, fix="", severity=None):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence, "fix": fix}
    if severity:
        r["severity"] = severity
    rows.append(r)


# ---- gates (all re-run at edbb7aa8 this round) ----
row("FC1-b-r1-gate-check-pages", "tools/check_pages.py --unit FC1 --page L04; --page L05; --unit FC1",
    "course/modules/FC/FC1/L04.html, L05.html, cards.json", "PASS",
    f"Re-run at edbb7aa8: '{O}/check_pages.out' shows check_pages FC1 L04 PASS, L05 PASS, unit FC1 PASS, rc 0 each.")
row("FC1-b-r1-gate-check-dag", "tools/check_dag.py --unit FC1", "L04.html line 37; L05.html lines 38, 58, 63", "PASS",
    f"'{O}/check_dag.out': check_dag FC1: PASS, rc 0. Links used: L04 line 37 to L03#def-bid-ask-spread; L05 line 38 to L04#def-order-types, L04#def-limit-order-book, L01#def-financial-intermediary.")
row("FC1-b-r1-gate-run-labs", "tools/run_labs.py --unit FC1 --page L04 / --page L05",
    "tests/labs/FC1/lab-FC1-L04-1.py, lab-FC1-L05-1.py", "PASS",
    f"'{O}/run_labs.out': run_labs FC1: PASS (1/1) for L04 and for L05, rc 0 each.")
row("FC1-b-r1-gate-twin-alone", "twin run alone under python -I -W error from a scratch dir; stdout vs pre.expected",
    "tests/labs/FC1/lab-FC1-L04-1.py, lab-FC1-L05-1.py", "PASS",
    f"'{S}/twin_vs_page_r4.py' -> '{O}/twin_vs_page_r4.out': L04 rc 0, stderr 0 bytes, 22 stdout lines; L05 rc 0, stderr 0 bytes, 24 stdout lines; 'ALL OK'.")
row("FC1-b-r1-gate-page-code-equals-twin", "page code block equals twin; @@LAB/@@OUT markers absent",
    "L04.html lines 127-335; L05.html lines 110-365", "PASS",
    f"'{O}/twin_vs_page_r4.out': L04 page code 8554 bytes vs twin 8555 (trailing newline), equal after rstrip; L05 10551 vs 10552, equal; markers 0 in both pages. Twins unchanged since round 3 (git diff of tests/labs/FC1 between 8196077d and edbb7aa8 is empty).")
row("FC1-b-r1-gate-expected-equals-output", "pre.expected equals the twin's printed output",
    "L04.html lines 336-357; L05.html lines 366-389", "PASS",
    f"'{O}/twin_vs_page_r4.out': expected_equals_stdout True for both, after html unescape and strip.")
row("FC1-b-r1-gate-page-smoke", "tools/page_smoke.py --unit FC1 --pages L04 L05 (Chromium, Pyodide, 360 px, console, requests)",
    "L04.html, L05.html", "PASS",
    f"'{O}/page_smoke_L04_L05.out': page_smoke modules/FC/FC1/L04.html: PASS; L05.html: PASS; page_smoke FC1: PASS; rc 0. Labs 0.0 s each.")
row("FC1-b-r1-gate-ruff", "ruff check and ruff format --check on the two twins", "tests/labs/FC1/lab-FC1-L04-1.py, lab-FC1-L05-1.py", "PASS",
    f"'{O}/lint_types_r4.out': All checks passed!; 2 files already formatted; rc 0.")
row("FC1-b-r1-gate-mypy", "mypy --no-incremental on the two twins", "tests/labs/FC1/lab-FC1-L04-1.py, lab-FC1-L05-1.py", "PASS",
    f"'{O}/lint_types_r4.out': Success: no issues found in 2 source files; rc 0.")
row("FC1-b-r1-gate-pytest-labs", "pytest tests/test_labs.py tests/test_run_labs.py -k 'FC1 or L04 or L05'; tests/test_page_checks.py tests/test_curriculum.py tests/test_docs_figures.py",
    "tests/test_labs.py, tests/test_run_labs.py, tests/test_page_checks.py, tests/test_curriculum.py, tests/test_docs_figures.py", "PASS",
    f"'{O}/pytest_labs_fc1_r4.out' rc 0 (all selected passed); '{O}/pytest_page_checks_curriculum_r4.out' rc 0 (all passed).")
row("FC1-b-r3-gate-build-site-check", "tools/build_site.py --check", "course/assets/data, course/index.html, course/concepts.html", "PASS",
    f"'{O}/build_site_check.out': site data current: 6 outputs; rc 0.")
row("FC1-b-r1-gate-verify-refs-offline", "tools/verify_refs.py --offline", "references/references.json", "PASS",
    f"'{O}/verify_refs_offline.out': offline integrity: 560 entries, 0 problems; rc 0.")
row("FC1-b-r2-gate-verify-refs-live-unit", "tools/verify_refs.py --unit FC1 (live)", "references/references.json: harris2002trading", "PASS",
    f"'{O}/verify_refs_unit_FC1_live.out': live re-verification of FC1: 2 of 560 entries, 0 problems; rc 0.")
row("FC1-b-r4-gate-check-projects-unit", "tools/check_projects.py --unit FC1", "course/modules/FC/FC1/project.html (unit gate)", "PASS",
    f"'{O}/check_projects.out': check_projects FC1: PASS, rc 0. Slice b has no project or grader; run_graders does not apply to this slice.")

# ---- numbers and labs ----
row("FC1-b-r1-num-L04-prose", "2.2 numbers in L04 prose re-derived by own code (fresh book, same RNG order)",
    "L04.html lines 72, 77, 400, 407, 414, 432, 450, 464, 489, 501-505", "PASS",
    f"'{S}/l04_independent_r4.py' -> '{O}/l04_independent_r4.out': Fixture A fills [(1000,60),(1100,90)], cost 159000, avg 1060.0, 10 left at 1100; Fixture B fills [(990,100),(985,100)], 1 activation, stop filled at 985; E1 24+18=42; E3 5600/173 = 32.37 (exact 5600/173). M1 99300/993, M2 and M3 and P2 and R1 and R3 and P3 re-derived by hand (P2 G=250, X=100, C=50, R=0; R3 120 = 2*60; M3 fills 1 activation pattern checked by hand).")
row("FC1-b-r1-num-L04-lab-output", "2.5 lab numbers and expected block re-derived independently",
    "L04.html lines 336-357 (expected), 358 (interpretation), 505 (key result)", "PASS",
    f"'{O}/l04_independent_r4.out' reproduces every expected line: trace events 0-7 (best bid 9984 after events 0-6, none after event 7; best ask none for events 0-1; 10015 at event 2); kinds 181 limit / 77 market / 42 stop; trades 173; traded 5600; activations 24; pending 18; cancelled 220; resting 4710; crossed 0; conservation failures 0; end best bid 9997, ask 10001. Event 7 is a market sell of 60 with no activation, which empties the bid side (supports E2 solution, line 457).")
row("FC1-b-r1-num-L05-prose", "2.2 numbers in L05 prose re-derived by own code (exact Fractions, own calendar walk)",
    "L05.html lines 75, 109, 390, 438, 445, 452, 488, 495, 502, 544, 582, 605-607, 637", "PASS",
    f"'{S}/l05_independent_r4.py' -> '{O}/l05_independent_r4.out': consideration 216*10060 = 2172960; G 68398886; NP 14282414; ratio 7141207/34199443 = 0.20881062302681364 -> 8dp 0.20881062, 5dp 0.20881, 4dp 0.2088, 3dp half-up 0.209; P5 16.170380 % of gross (16.17) and 77.440410 % of NP (77.44); 2026-10-28 is Wednesday, +2 bd = Fri 2026-10-30, +2 bd from Fri 10-30 = Tue 2026-11-03 (M2), +3 bd = Mon 2026-11-02 (E3); E2 positives 3222054+11060360 = 14282414 = negatives 7411991+6656379+214044; net payers P1, P2, P4 (3); sum 0; M1 100*10090 = 1009000; M3 ratio 0.500.")
row("FC1-b-r1-num-L05-lab-output", "2.5 lab output and hypothesis numbers vs independent re-derivation",
    "L05.html lines 109, 366-389; twin", "PASS",
    f"'{O}/l05_independent_r4.out' reproduces: resting P2 10060/263, P3 10257/362, P4 10331/152; incoming P1 limit 10117 qty 216; one fill 216 at 10060; consideration 2172960; batch gross 68398886, NP 14282414; net P1 -7411991, P2 -6656379, P3 3222054, P4 -214044, P5 11060360; sum 0; ratio milli 209.")
row("FC1-b-r1-lab05-parameter-claims", "2.5 sentences about what changing the lab's parameters does (L05 lines 66, 390, 502; card FC1-c142)",
    "L05.html lines 66, 390, 502; cards FC1-c142", "PASS",
    f"'{O}/l05_sensitivity_r4.out' (script FC1-b-r3/l05_sensitivity_r3.py run on edbb7aa8): SETTLEMENT_LAG=3 changes exactly the header, settlement and position_update lines, batch and netting lines identical, offsets_nondecreasing still True (matches line 502 and E3); CLEARING_OFFSET=3 makes offsets_nondecreasing False and changes header and clearing line (matches lines 66, 390 and card FC1-c142); CLEARING_OFFSET=1 changes header and clearing line only.")
row("FC1-b-r1-lab04-invariant-claim", "2.5 lab claim that Lab 1 checks both invariants after each of 300 events (L04 lines 51, 126, 358, 505)",
    "L04.html lines 51, 126, 358, 505; twin main loop", "PASS",
    f"'{S}/../FC1-b-r3/l04_sensitivity_r3.py' run on edbb7aa8 -> '{O}/l04_sensitivity_r4.out': base run prints 0 crossed and 0 conservation failures; mutant A (limit orders never match) prints 3 crossed events; mutant B (traded term halved for even fills) prints 296 conservation failures. Counters are live. The check is after each arrival with its activations; Proposition 2.2 covers the intermediate states, which the lab does not print separately (not a defect: the lab's events are its 300 arrivals).")

# ---- mathematics ----
row("FC1-b-r1-math-L04-examples-problems", "2.4 Examples 1.3-1.4, Problems M1-M3, P2-P3, E1-E3, R1-R3, misconception arithmetic",
    "L04.html lines 72, 77, 377-385, 398-491", "PASS",
    "Re-derived each: M1 (60@995 then 40@990: 99300, avg 993, 60 left at 990); M2 (30@1000 + 20@1001 fills; left 10@1001, 40@1003); M3 (sell stop 1000: 1005 no, 1001 no, 1000 triggers); P2 (G=250, X=100, C=50, R=0, 0+200+50=250); P3 (t>=s activates, t=s activates, t<s pending); E1 (24+18=42); E2 (best ask first printed at event 2, best bid none after event 7, verified by l04_independent_r4.out); E3 (5600/173); R1 (fills 990,985,980 in that order, checked against Remark 1.2); R2 (crossed 1005 vs 1000, buy 999 rests, still crossed); R3 (120). Problem P1 handled by FC1-b-r3-proof-P1-hypothesis and FC1-b-r4-P1-empty-side-convention.")
row("FC1-b-r1-math-L05-prop21-prop22", "2.4 Propositions 2.1 and 2.2: statements, assumptions, proofs",
    "L05.html lines 75-96, 100, 518-520 (R2), 470 (P2)", "PASS",
    "Prop 2.1(i) telescopes to 0 (line 84). (ii): NP>=0 from max; NP<=sum Pay_j = G uses c_i>=0 (A1) and that each consideration has one buyer (line 85). Prop 2.2 (line 95): CCP receives G and pays G, net 0; legs with the CCP equal the original amounts, so the net position is x_j. P2 bracket argument (line 470) checked: f(x)=max(-x,0) is non-increasing and 1-Lipschitz; brackets lie in [-c,0] and [0,c]; buyer != seller (A1) makes the two brackets independent. R2 (line 520) checked with c=-100: x_A=+100, x_B=-100, NP=100, G=-100.")
row("FC1-b-r1-math-L04-prop22-empty-side", "2.4 Proposition 2.2 proof completeness: empty side, residual cases",
    "L04.html lines 99, 104", "PASS",
    "Convention beta=-inf, alpha=+inf (line 104) covers empty sides; buy limit with residual on an empty bid side gives new best bid p; residual filled gives market case; sell side symmetric. Re-derived by hand; no gap.")
row("FC1-b-r1-math-L04-prop23-assumptions", "2.4 Proposition 2.3 hypotheses complete (A2 numbered, proof uses A2 and fill accounting)",
    "L04.html lines 92-95, 107-117; card FC1-c066", "PASS",
    "A2 numbered (line 93), stated (line 94). Proof (line 116): each order's entered quantity = filled + cancelled + resting, resting only changes by trading under A2, sum of filled = 2X. Stops counted at activation (line 109).")
row("FC1-b-r1-math-L04-remark-definitions", "2.4 Definition 1.1, Remark 1.2, Definition 2.1, A1 against the lab code",
    "L04.html lines 56-67, 84-89, 197-220 (match), 222-246 (activate), 302-313 (main loop)", "PASS",
    "Remark 1.2 (fill at resting price; last trade price; stop check after finished matching; arrival order; repeat until none triggers) matches twin match() (fill at best.price), activate() (repeat while last is not None; first triggered in arrival order) and the main loop (match, then activate).")
row("FC1-b-r3-proof-P1-hypothesis", "2.4 Problem P1 (L04 line 423 statement, line 425 solution): hypotheses complete",
    "L04.html line 423 (statement), line 425 (solution)", "PASS",
    "Round-3 FAIL is fixed: the statement (line 423) now grants 'the book uncrossed before an arriving market buy order' with the source in A1 for the first event. The solution uses only the stated facts: a market buy removes asks, leaves bids unchanged, so alpha' >= alpha. The residual empty-side convention is a separate LOW row.")
row("FC1-b-r4-key-result-NP-hypothesis", "2.3/2.4 key-results row graded T: stated hypotheses complete (Proposition 2.1(ii) needs A1)",
    "L05.html line 540 (key-results row); Proposition 2.1 line 79; Problem R2 lines 518-520; card FC1-c089", "FAIL",
    "Row 540 reads 'In a batch, net payments lie between zero and gross payments (Proposition 2.1(ii))', grade T, source 'Proved in §2'. Proposition 2.1(ii) is stated under A1 (line 79). Without A1 the claim is false: Problem R2 (line 520) gives one trade with consideration -100 cents, NP=100 and G=-100, so 100 <= -100 fails. The row names A1 in neither its claim nor its source.",
    "Change row 540's claim to 'Under A1, in a batch, net payments lie between zero and gross payments (Proposition 2.1(ii))' and its source to 'Proved in §2 from A1'.", severity="blocking")
row("FC1-b-r4-key-result-L04-503-hypothesis", "2.3 key-results row graded T: hypothesis in the claim (Proposition 2.2 needs A1)",
    "L04.html line 503 (key-results row); Problem R2 lines 480-482", "FAIL",
    "Row 503 claim 'The book is never crossed after any event (Proposition 2.2)' omits A1 (stated at line 89 and in Proposition 2.2, line 99). The source column says 'from A1 and the matching rules', so the hypothesis is present. Without A1 the claim is false (Problem R2). Wording only.",
    "Change the claim to 'Under A1, the book is never crossed after any event (Proposition 2.2)'.", severity="LOW")
row("FC1-b-r4-key-result-L05-541-hypothesis", "2.3 key-results row graded T: hypothesis list matches Proposition 2.2",
    "L05.html line 541 (key-results row); Proposition 2.2 line 90", "FAIL",
    "Row 541 reads 'Under A2, the CCP's net cash over a batch is zero ...' and omits A1, which Proposition 2.2 lists (line 90). The claim is true without A1 (proof line 95 uses only A2), so this is a wording gap, not a false claim.",
    "Change the claim to 'Under A1 and A2, ...' to match Proposition 2.2.", severity="LOW")
row("FC1-b-r4-P1-empty-side-convention", "2.4 Problem P1 solution: the empty-side convention is stated",
    "L04.html line 425 (solution)", "FAIL",
    "The solution's first sentence, 'Before the arrival, the best bid beta is below the best ask alpha', is undefined when one side is empty (Definition 2.1, line 84, defines crossed through best bid and best ask). The conclusion still holds with the beta=-inf, alpha=+inf convention of Proposition 2.2 (line 104), which the solution does not state. Presentation gap in a worked solution.",
    "Add to the solution: 'If one side is empty, take beta = -inf or alpha = +inf, as in the proof of Proposition 2.2.'", severity="LOW")

# ---- grades, notation, prose, structure ----
row("FC1-b-r1-grades", "2.3 grades re-graded against BLUEPRINT §3 (T proofs and hand computations; C lab-read counts naming the lab)",
    "L04.html lines 98, 108, 501-505; L05.html lines 78-96, 539-544, 403; cards", "PASS",
    "T: Examples 1.3-1.4, Props 2.2 and 2.3 (L04), Props 2.1 and 2.2 (L05), computed-by-hand problems. C: L04 row 505 and L05 rows 542-544 name Lab 1 as basis. L05 line 403 (C, bibliographic statement, no finding) is noted, not failed. Grade letters agree with the table rows (the hypothesis omissions are the separate FAIL rows).")
row("FC1-b-r1-notation", "2.4 notation vs notation/notation.json (T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, Q)",
    "L04.html and L05.html inline math", "PASS",
    "Single-letter scan of the inline math (regex over \\(...\\) and \\[...\\]): L04 uses C, G, R, X, p, q, s, t, o (summation index); L05 uses A, B, C, G, J, b, c, f, i, j, n, p, q, s, t, x. None is a registered symbol; no registered macro is used. Local symbols defined at point of use.")
row("FC1-b-r1-prose-process-words", "2.9 no process words in learner text", "L04.html, L05.html, cards FC1-c056..c156", "PASS",
    "grep over both pages (verifier, builder, ledger, round, admitted, reference list, REQUEST, course's): no process-word hit. The only 'round' tokens are 'rounded' (L05 lines 124, 272, 390, 486, 488). Card scan (cards_scan_r4.py): 'round' appears in cards only as 'rounded' (c010-c012 in L01, c084 in L05).")
row("FC1-b-r1-prose-banned-phrases", "2.9 / BUILDER 1.3-1.4 banned phrases", "L04.html, L05.html, cards.json", "PASS",
    "grep for TODO, TBD, lorem, for brevity, details omitted, beyond the scope, left as an exercise, you can add more, it is important to note, studies show, experts agree, it is well known, obviously, clearly and ellipsis: 0 hits in visible prose. check_pages FC1 PASS (banned-string check).")
row("FC1-b-r1-structure-L04", "2.9 / BUILDER 4.2 template order, counts, hours", "L04.html", "PASS",
    "Order: why-it-matters (116 words, <=120) line 51; s1 Definitions 1.1 and Examples 1.3-1.4; s2 Definition 2.1, A1, A2, Props 2.2, 2.3, Remark 2.4, lab (line 124); s3 canon (361); s4 misconceptions (3); s5 problems (3 per tier, 12 solutions); s6 key results (5 rows); s7 quiz (9 items, 9 explanations); s8 references. data-hours 10; 'Lesson 4 of 5'. No debate field in the curriculum entry.")
row("FC1-b-r1-structure-L05", "2.9 / BUILDER 4.2 template order, counts, hours", "L05.html", "PASS",
    "Order: why-it-matters (115 words) line 52; s1 Definitions 1.1, 1.2, Remark 1.3; s2 Props 2.1, 2.2, Remark 2.3; s3 lab (line 107); s4 canon (393); s5 misconceptions (4); s6 problems (3 per tier, 12 solutions); s7 key results (6 rows); s8 quiz (11 items, 11 explanations); s9 references. data-hours 10.")
row("FC1-b-r1-scope-words", "2.3 / 2.4 scope words need a computation, proof or explicit hypothesis", "L04.html lines 67, 126, 358, 364, 475, 505; L05.html lines 63, 70, 390, 399", "PASS",
    "'every' (L04 358) backed by Props 2.2/2.3 under A1/A2 and by the lab's counts; 'only' (L04 67, 364) is a stated rule of the model; 'exactly' (L04 475) checked by R1 fills; 'all' (L05 63) follows 'In this model'; 'never decrease' (L05 lines 109, 502) is backed by the lab's offsets_nondecreasing check for its parameters (true at lag 2; prints False when the clearing offset exceeds the lag, line 66).")
row("FC1-b-r1-attribution-harris", "2.1 / 2.2 citation: harris2002trading, book level, registry fields only", "L04.html line 590; L05.html line 403; references/references.json; curriculum/02-economics-finance-core.yaml line 385", "PASS",
    "references.json record: title 'Trading and Exchanges: Market Microstructure for Practitioners', author Harris, DOI 10.1093/oso/9780195144703.001.0001, year 2002 (Crossref, print_year 2002). Pages print the registry title and registry year only, as the architect decision requires. No passage or finding is attributed to the book. Book not read; no locator claimed.")
row("FC1-b-r1-settlement-source-absence", "2.1 scope of 'no settlement period is stated' (L05 lines 52, 105, 397, 513, 632; card FC1-c090)",
    "L05.html lines 52, 105, 397, 513, 632; card FC1-c090; references/references.json", "PASS",
    "The only period in the lesson is SETTLEMENT_LAG = 2 in the twin (line 138), labelled a parameter. Registry title scan (560 entries, 'settle' or 'clearing'): hits are bisndbasel, bisndcpmi and duffie2011central; none is a settlement-cycle record, so the 'no settlement-cycle source' statement holds for the registry. The Harris book is not read, so nothing is claimed about its content.")
row("FC1-b-r1-references-L05", "2.1 reference list renders the cited key (renderCitations)", "L05.html line 403 and line 644; course/assets/js/refs.js lines 68-90", "PASS",
    "refs.js renderCitations collects [data-cite] keys and fills ol[data-references]; L05 line 403 cites harris2002trading, so the list renders one entry. Rendered list not screenshot-checked; page_smoke PASS.")
row("FC1-b-r1-references-L04-empty-list", "2.1 reference list on L04", "L04.html lines 590-591; course/assets/js/refs.js", "PASS",
    "L04 line 590 cites harris2002trading via data-cite; refs.js fills the empty ol[data-references] at line 591.")

# ---- cards ----
row("FC1-b-r1-cards-L04", "2.7 cards for L04 (FC1-c056..c072, c099, c100, c119, c121, c132, c133, c135, c141, c143, c154-c156): each card checked against the lesson text",
    "course/modules/FC/FC1/cards.json (29 L04 cards)", "PASS",
    f"Every card read and checked against L04 text: '{S}/cards_scan_r4.py' -> '{O}/cards_scan_r4.out' (29 L04 cards; every number on the card appears in L04.html; no duplicate ids). Graded cards: c061, c062, c066, c068, c069 (C, basis Lab 1), c099 (T), c100 (T) all agree with the lesson text.")
row("FC1-b-r1-cards-L05", "2.7 cards for L05 (FC1-c073..c090, c101, c102, c109, c114, c118, c123, c124, c142, c144, c145): each card checked",
    "course/modules/FC/FC1/cards.json (28 L05 cards)", "PASS",
    f"'{O}/cards_scan_r4.out': 28 L05 cards; every number on each card appears in L05.html. c082-c086 are C with basis (Lab 1 SIMULATED); c079, c080, c089, c101, c102 are T with hypotheses stated (A1, A2 or the sign condition). c089 counterexample checked (R2).")
row("FC1-b-r1-cards-duplicates", "2.7 full scan for duplicate cards across the FC1 deck (155 cards)", "course/modules/FC/FC1/cards.json", "PASS",
    f"'{O}/cards_scan_r4.out': 155 cards, no duplicate ids; no identical fronts. Near-identical stems (ratio >= 0.9) are distinct facts across lessons (e.g. c058 buy stop vs c121 sell stop; c132 best bid vs c133 best ask; c114 gross vs c124 net payments).")
row("FC1-b-r1-card-c066", "2.7 card FC1-c066 vs Proposition 2.3 hypotheses", "cards.json FC1-c066; L04.html lines 92-95, 108-111", "PASS",
    "Card states 'Under A2 (no withdrawals), G = R + 2X + C after every event', with C defined as the cancelled shares of market orders. Matches Proposition 2.3 (line 108-111).")
row("FC1-b-r4-card-c099-changed-text", "2.7 card FC1-c099 changed since round 3: agrees with current Proposition 2.2 text",
    "cards.json FC1-c099; L04.html line 99", "PASS",
    "Card now reads 'Under A1, the book starts empty, and under the matching rules of Section 1 it is not crossed after any event, where an event is an arrival or an activation of a stop (Proposition 2.2)'. Matches Proposition 2.2 (line 99) and its 'event' definition (line 99). Grade T with hypothesis present.")
row("FC1-b-r2-cards-c154-c156", "2.7 cards FC1-c154, c155, c156 against Remark 1.2 and A2", "cards.json FC1-c154..c156; L04.html lines 67, 94", "PASS",
    "c154: 1010/1005/1000 example matches Remark 1.2 (line 67). c155: repeat until none triggers (line 67). c156: under A2 only unfilled market-order shares are cancelled (line 94).")
row("FC1-b-r1-labs-runtime-seed-network", "2.5 seeds, no network, runtime, standard library only", "tests/labs/FC1/lab-FC1-L04-1.py, lab-FC1-L05-1.py", "PASS",
    "Imports: L04 random, collections.Counter, dataclasses; L05 datetime, itertools, random, collections.abc, dataclasses (grep of import lines: no socket, urllib or requests). Seeds SEED=2026 (both). page_smoke lab runtimes 0.0 s each.")
row("FC1-b-r1-lab-prose-consistency", "2.5 lab hypothesis and interpretation match code and output", "L04.html lines 126, 358; L05.html lines 109, 390", "PASS",
    "L04 line 126 hypothesis: fixtures, seed 2026, 300 events within 20 cents of 10000, counts zero (matches twin fixture_walk, lines 123-147, and main, lines 167-206). L05 line 109: 216 at 10060, 2172960, offset 2 Friday, 0.209, 3 net payers, sum 0 (matches the expected block). Interpretation statements match the output.")
row("FC1-b-r1-misconceptions-canon", "2.9 misconceptions and canon sections", "L04.html lines 364-368, 375-386; L05.html lines 397-401, 409-425", "PASS",
    "L04 misconceptions 1-3 correct (Example 1.3 average 1060; Example 1.4 stop fills 985; priority example). L05 misconceptions 1-4 correct (2026-10-30 Friday, 14282414 vs 68398886, CCP identity conditional on A2, limit 10117 vs price 10060). Canon sections state no venue fact.")
row("FC1-b-r1-inline-style", "2.9 inline style attributes on quiz fieldsets", "L04.html lines 517, 526, 545, 555, 569, 578", "PASS",
    "Only min-inline-size: 0 on fieldsets (layout), no colour or content. Judgement call, not a defect.")
row("FC1-b-r2-math-L04-prop22-stop-arrival", "2.4 Proposition 2.2 covers stop arrivals that do not activate", "L04.html line 104", "PASS",
    "The proof's sentence 'A stop that arrives and does not activate is not in the book, so the book is unchanged' is correct: a pending stop is not in the bid or ask side (twin Book.pending).")
row("FC1-b-r2-def12-order-entry-offset", "2.4 Definition 1.2 offsets: order entry, matching and capture at offset 0", "L05.html line 63; quiz explanation line 562; lab state list", "PASS",
    "Definition 1.2 (line 63) states offset 0 for order entry, matching, trade capture. Twin states list lines 205-217 use offset 0 for these three. Quiz explanation line 562 agrees.")
row("FC1-b-r2-canon-needs-empty-start", "2.9 canon: the invariants depend on A1 and A2", "L04.html line 367", "PASS",
    "Line 367 says Proposition 2.2 needs the uncrossed start that A1 gives, and Proposition 2.3 needs A2; R2 shows the failure from a crossed start. Correct.")
row("FC1-b-r2-A2-consistency", "2.4 assumption A2 used consistently across L04 (no withdrawals) and its statement elsewhere", "L04.html lines 51, 92-95, 109, 116, 126, 358, 365, 504-505; L05.html line 90; cards c066, c135, c156", "PASS",
    "Same statement of A2 wherever cited in L04. L05 A2 is a separate assumption with its own numbering (lesson-local, the label is reused with different content; recorded as a judgement call, not a defect).")
row("FC1-b-r2-terms-before-definition", "2.9 / BUILDER 2.x terms used before definition", "L04.html lines 51, 60-61; L05.html lines 52, 63, 66", "PASS",
    "Forward references are explicit: L04 line 60 'defined in Lesson 4, Remark 1.2' (resting order), line 61 (last trade price); L05 line 52 'defined in Lesson 5, Definition 1.1' (CCP). Netting and novation are defined in L05 Definition 1.1 before Section 2 uses them.")
row("FC1-b-r2-cross-reference-style", "2.9 self-references 'Lesson 4, Definition 2.1' inside L04 (and similar) are unambiguous", "L04.html lines 51, 59-61; L05.html line 66", "PASS",
    "Style choice; each reference names a numbered item, so no ambiguity. Judgement call, not a defect.")
row("FC1-b-r4-L05-why-market-claim", "2.1 / BUILDER 2.x: substantive claim about trade practice carries a grade and a key",
    "L05.html line 52 (why-it-matters)", "FAIL",
    "The why-it-matters paragraph says 'Between execution and the transfer of cash and instruments, the terms are confirmed, the obligations are computed, and, where a central counterparty is used, the trade is replaced by two trades'. This is a general statement about how trades are processed, with no grade and no registry key. BLUEPRINT §3 requires a grade and a key for each substantive claim. Remark 1.3 (line 70) says the six states are a model and not a description of any venue, which is in tension with this sentence. Not a false statement; a grading gap.",
    "Rephrase as the model's definition ('In this lesson's model, ...'), or grade it C or D with a registry key that supports it.", severity="LOW")
row("FC1-b-r4-L04-why-it-matters", "2.9 why-it-matters changed since round 3 (line 51): word count, claim, hypothesis",
    "L04.html line 51", "PASS",
    "116 words (<=120). Claim 'the book never rests crossed (Proposition 2.2, under A1)' matches Proposition 2.2 (line 99) and A1 (line 89). 'with no withdrawals (A2)' matches Proposition 2.3 (line 108). 'Lab 1 checks both invariants after each of 300 simulated events' matches the twin (see FC1-b-r1-lab04-invariant-claim).")
row("FC1-b-r4-hours", "2.9 / BUILDER 4.3 hours split (lessons 50 + project 20 = 70)", "course/modules/FC/FC1/index.html line 29; L04.html line 2 and 34; L05.html line 2 and 35", "PASS",
    "index.html line 29: data-hours-lessons=50, data-hours-project=20 (sum 70, curriculum 70). Each lesson data-hours 10 (five lessons, 50). check_pages FC1 PASS.")
row("FC1-b-r3-lesson-links", "2.9 nav links (previous/next)", "L04.html lines 596-597; L05.html lines 649-650", "PASS",
    "L04 previous L03.html, next L05.html; L05 previous L04.html, next project.html. Titles match the lesson h1s.")

registry_flags = [
    "harris2002trading: curriculum yaml line 385 reads 'Harris, Trading and Exchanges (2003)'; the registry record (Crossref) reads 2002. The pages cite the key with registry fields only (architect decision). The curriculum string should be corrected by its owner; no registry edit is requested."
]
frag = {
    "unit": "FC1",
    "slice": "FC1-b",
    "round": 4,
    "verifier": "Claude Haiku 5.5, independent verifier for FC1-b round 4 (did not build FC1; read verifier-rules.md, VERIFIER_RULES.md, BUILDER_RULES.md, plans/FC1-build-plan.md, the round-3 fragment as context only)",
    "pin": "edbb7aa8de20e6d2f3035c463a79a318c22623c4",
    "base": "8196077d5f56c3919d33e69888176d197d378ad4 (round-3 pin, fragment /Users/billyribeiro/.fanout/frags/S-FC1-b.round3.json)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyS4-FC1-b",
    "scratch": "ledgers/FC1/scripts/FC1-b-r4/",
    "verified_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": registry_flags,
    "freshness_flags": [],
    "notes": [
        "Delta since round 3 (8196077d..edbb7aa8) in the slice: L04.html line 51 (why-it-matters) and line 423 (P1 statement), cards.json FC1-c099 (plus L01-L03 cards and index.html, out of slice). L05.html, both twins, and L05 cards are byte-identical to round 3; L05 rows were nevertheless re-derived in this round with fresh scripts, so no row is carried.",
        "tests/labs/FC1, notation/notation.json, references/references.json and tools/ are unchanged in the FC1 delta (git diff --stat over those paths shows no FC1 change).",
        "Round-3 FAIL FC1-b-r3-proof-P1-hypothesis is fixed and verified (row PASS). Its residual empty-side convention is a LOW row.",
        "Ruling 26 classification: one blocking row (FC1-b-r4-key-result-NP-hypothesis: a T-graded key result states NP <= G without A1). Four LOW rows (wording or presentation): FC1-b-r4-key-result-L04-503-hypothesis, FC1-b-r4-key-result-L05-541-hypothesis, FC1-b-r4-P1-empty-side-convention, FC1-b-r4-L05-why-market-claim. The verdict field is FAIL because a non-PASS row exists (VERIFIER_RULES §3). Ruling 26 says LOW rows are fixed or listed in plans/KNOWN-ISSUES.md with their ids.",
        "Lab statements vs code: both labs' statements match their code and printed output. The L04 'checks after each event' claim is verified as a check after each arrival with its activations; the intermediate states after each single activation are not printed by the lab (covered by Proposition 2.2, not a lab defect).",
        "Not a row: L05 line 403 grades a bibliographic statement C (no finding). Harmless; noted only. Registry key duffie2011central ('Does a Central Clearing Counterparty Reduce Counterparty Risk?') is relevant to L05 misconception 3 but is not cited; L05 line 399 states no finding on that question, so no counter-evidence duty arises. Noted only.",
        "Judgement calls recorded: 'registry key' and 'the curriculum lists' citation wording (architect-sanctioned); self-references 'Lesson 4, ...' in L04; 'A2' label reused in L04 and L05 with different content (lesson-local); the non-decreasing offsets convention (L05 line 66) is a model statement no proof uses.",
        "The committed ledgers/FC1/FC1-b.json at edbb7aa8 (round 7 fragment, pin 0d2d0f3) was overwritten in this checkout only, as the round-4 instruction requires. Nothing was committed or pushed.",
    ],
    "summary": "",
}
counts = {"PASS": 0, "FAIL": 0, "UNVERIFIABLE": 0}
for r in rows:
    counts[r["status"]] += 1
blocking = [r["id"] for r in rows if r.get("severity") == "blocking"]
low = [r["id"] for r in rows if r.get("severity") == "LOW"]
frag["summary"] = (
    f"FC1-b round 4 at edbb7aa8: {len(rows)} rows, {counts['PASS']} PASS, {counts['FAIL']} FAIL, "
    f"{counts['UNVERIFIABLE']} UNVERIFIABLE. Blocking (ruling 26 kinds): {blocking}. LOW: {low}. "
    "All gates re-run and green (check_pages, check_dag, check_projects, run_labs, twins alone, page_smoke, ruff, mypy, lab pytest, page and curriculum pytest, build_site --check, verify_refs offline and live). "
    "Round-3 P1 FAIL fixed. Mutants: none (lessons; mutation testing applies to project graders only)."
)
with open(f"{root}/ledgers/FC1/FC1-b.json", "w", encoding="utf-8") as fh:
    json.dump(frag, fh, indent=2, ensure_ascii=False)
    fh.write("\n")
print("rows", len(rows), counts, "blocking", blocking, "low", low)
