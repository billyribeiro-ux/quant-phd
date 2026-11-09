"""Builds ledgers/FC1/FC1-b.json (round 3) from the verification rows. Evidence cites scripts under scripts/FC1-b-r3/."""
import datetime
import json
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
S = "ledgers/FC1/scripts/FC1-b-r3"
O = f"{S}/out"
P = "PASS"
rows = []


def row(id_, check, location, status, evidence, fix=""):
    rows.append({"id": id_, "check": check, "location": location, "status": status, "evidence": evidence, "fix": fix})


row("FC1-b-r1-gate-check-pages", "tools/check_pages.py --unit FC1 --page L04; --page L05; --unit FC1",
    "course/modules/FC/FC1/L04.html, L05.html, cards.json", P,
    f"Re-run at 8196077d: check_pages FC1 L04, L05 and unit FC1 each rc 0, final line 'check_pages FC1: PASS' ({O}/check_pages.out).")
row("FC1-b-r1-gate-check-dag", "tools/check_dag.py --unit FC1", "L04.html line 37; L05.html lines 38, 58, 63", P,
    f"'check_dag FC1: PASS' rc 0 ({O}/check_dag.out). L04 line 37 links L03#def-bid-ask-spread; L05 line 38 links "
    "L04#def-order-types, L04#def-limit-order-book and L01#def-financial-intermediary (all prerequisite-closure concepts); "
    "L05 defines clearing-and-settlement (line 58) and trade-lifecycle (line 63) in place.")
row("FC1-b-r1-gate-run-labs", "tools/run_labs.py --unit FC1 --page L04 / --page L05",
    "tests/labs/FC1/lab-FC1-L04-1.py, lab-FC1-L05-1.py", P,
    f"'run_labs FC1: PASS (1/1)' for L04 and for L05, rc 0 each ({O}/run_labs.out).")
row("FC1-b-r1-gate-twin-alone", "twin run alone under python -I -W error (CPython 3.14.8 from .venv); stdout vs pre.expected",
    "tests/labs/FC1/lab-FC1-L04-1.py, lab-FC1-L05-1.py", P,
    f"{S}/twin_vs_page_r3.py -> {O}/twin_vs_page_r3.out: L04 rc 0, stderr 0 bytes, 22 stdout lines; L05 rc 0, stderr 0 bytes, "
    "24 stdout lines; 'ALL OK'. Runs from /tmp, not from the repo, so no local module shadows the stdlib.")
row("FC1-b-r1-gate-page-code-equals-twin", "page code block equals twin (embed fidelity), markers absent",
    "L04.html lines 127-335; L05.html lines 110-365", P,
    f"{O}/twin_vs_page_r3.out: L04 page code 8554 bytes vs twin 8555 (trailing newline), identical after rstrip; L05 10551 vs "
    "10552, identical; '@@LAB'/'@@OUT' count 0 in both pages. git diff --quiet 9294b914 8196077d -- tests/labs/FC1 is clean.")
row("FC1-b-r1-gate-expected-equals-output", "pre.expected equals the twin's printed output",
    "L04.html lines 336-357; L05.html lines 366-389", P,
    f"{O}/twin_vs_page_r3.out: expected_equals_stdout=True for both twins after html unescape and strip of outer newlines.")
row("FC1-b-r1-gate-page-smoke", "tools/page_smoke.py --unit FC1 --pages L04 L05 (Chromium, Pyodide, console, math, 360 px, requests)",
    "L04.html, L05.html", P,
    f"{O}/page_smoke_L04_L05.out: 'page_smoke modules/FC/FC1/L04.html: PASS', '...L05.html: PASS', 'page_smoke FC1: PASS', rc 0; "
    "lab-FC1-L04-1 0.0 s, lab-FC1-L05-1 0.0 s; runtime boot 1.2 s.")
row("FC1-b-r1-gate-ruff", "ruff check and ruff format --check on the two twins", "tests/labs/FC1/lab-FC1-L04-1.py, lab-FC1-L05-1.py", P,
    f"{O}/lint_types_r3.out: 'All checks passed!', '2 files already formatted', rc 0. Repo-wide ruff not run (scope).")
row("FC1-b-r1-gate-mypy", "mypy --no-incremental on the two twins", "tests/labs/FC1/lab-FC1-L04-1.py, lab-FC1-L05-1.py", P,
    f"{O}/lint_types_r3.out: 'Success: no issues found in 2 source files', rc 0.")
row("FC1-b-r1-gate-pytest-labs", "pytest tests/test_labs.py tests/test_run_labs.py -k 'FC1 or L04 or L05'; tests/test_page_checks.py tests/test_curriculum.py",
    "tests/test_labs.py, tests/test_run_labs.py, tests/test_page_checks.py, tests/test_curriculum.py", P,
    f"{O}/pytest_labs_fc1_r3.out rc 0 (all selected passed); {O}/pytest_page_checks_curriculum_r3.out rc 0.")
row("FC1-b-r3-gate-build-site-check", "tools/build_site.py --check", "course/assets/data, course/index.html, course/concepts.html", P,
    f"{O}/build_site_check_r3.out: 'site data current: 6 outputs', rc 0 (run this round; the concept index depends on the L04/L05 dfn ids).")
row("FC1-b-r1-gate-verify-refs-offline", "tools/verify_refs.py --offline", "references/references.json", P,
    f"{O}/verify_refs_offline.out: 'offline integrity: 560 entries, 0 problems', rc 0.")
row("FC1-b-r2-gate-verify-refs-live-unit", "tools/verify_refs.py --unit FC1 (live re-resolution, cache bypassed)",
    "references/references.json: harris2002trading", P,
    f"Re-run this round: {O}/verify_refs_unit_FC1_live.out 'live re-verification of FC1: 2 of 560 entries, 0 problems', rc 0.")
row("FC1-b-r1-num-L04-prose", "2.2 numbers in prose re-derived by an independent book (own code, same RNG call order)",
    "L04.html lines 72, 77, 400, 407, 414, 432, 450, 464, 489, 501-505", P,
    f"{S}/l04_independent_r3.py -> {O}/l04_independent_r3.out: Fixture A 159000 = 60*1000+90*1100, avg 1060, 10 left at 1100; "
    "Fixture B fills (990,100),(985,100); E1 24+18 = 42 = 'kinds stop 42'; E3 5600/173 = 32.37 (exact 5600/173). "
    f"{S}/l04_problems_r3.py -> {O}/l04_problems_r3.out re-derives M3, P2 (G=250, X=100, C=50, R=0), R1 (fills (990,100),(985,100),(980,100)), "
    "R2 (crossed after the 999 buy), Example 1.4 (stop fires, fills 985). M1 99300/993, M2 remainders 10@1001 and 40@1003 are by hand against the same rules; R3 120 = 2*60.")
row("FC1-b-r1-num-L04-lab-output", "2.5 lab numbers, expected block and interpretation re-derived independently",
    "L04.html lines 336-357 (expected), 358 (interpretation), 505 (key result); twin", P,
    f"{O}/l04_independent_r3.out reproduces every expected line: trace events 0-7 (best bid 9984 after events 0-6, none after event 7, "
    "best ask none for events 0-1, 10015 at event 2); kinds 181 limit / 77 market / 42 stop; trades 173; traded 5600; "
    "activations 24; pending 18; cancelled 220; resting 4710; crossed 0; conservation failures 0; end best bid 9997, ask 10001.")
row("FC1-b-r1-num-L05-prose", "2.2 numbers in prose re-derived (own code, same RNG call order)",
    "L05.html lines 75, 109, 390, 438, 445, 452, 488, 495, 502, 544, 582, 605-607, 637", P,
    f"{S}/l05_independent_r3.py -> {O}/l05_independent_r3.out: consideration 216*10060 = 2172960; G 68398886; NP 14282414; "
    "ratio exact 7141207/34199443 = 0.20881062302681364 -> 8 dp 0.20881062, 5 dp 0.20881, 4 dp 0.2088, 3 dp half-up 0.209; "
    "P5 16.170380 % of gross (16.17) and 77.440410 % of NP (77.44); M1 100*10090 = 1009000; M2 Fri 2026-10-30 +2 bd = Tue 2026-11-03; "
    "E2 sums 7411991+6656379+214044 = 14282414 and 3222054+11060360 = 14282414; E3 +3 bd = Mon 2026-11-02; R2 c=-100; M3 ratio 1/2.")
row("FC1-b-r1-num-L05-lab-output", "2.5 lab output and hypothesis numbers vs independent re-derivation",
    "L05.html lines 109, 366-389; twin", P,
    f"{O}/l05_independent_r3.out reproduces: resting P2 10060/263, P3 10257/362, P4 10331/152; incoming P1 10117/216; one fill; "
    "consideration 2172960; batch gross 68398886, NP 14282414; net payers P1, P2, P4 (3); net positions -7411991, -6656379, 3222054, -214044, 11060360; sum 0; ratio milli 209.")
row("FC1-b-r1-lab05-parameter-claims", "2.5 sentences about what changing the lab's parameters does (E3 solution, interpretation, lab hypothesis)",
    "L05.html lines 66, 390, 502; cards FC1-c142", P,
    f"{S}/l05_sensitivity_r3.py -> {O}/l05_sensitivity_r3.out: SETTLEMENT_LAG=3 changes exactly the header, settlement and position_update "
    "lines (settlement offset 3 = Mon 2026-11-02), batch/netting lines identical, offsets_nondecreasing still True (matches line 502). "
    "CLEARING_OFFSET=3 makes offsets_nondecreasing False and changes header and clearing line (matches lines 66, 390, card c142). "
    "CLEARING_OFFSET=1 changes header and clearing line only.")
row("FC1-b-r1-lab04-invariant-claim", "2.5 lab claim that Lab 1 checks both invariants after each of 300 events",
    "L04.html lines 51, 126, 358, 505; twin main loop", P,
    f"{S}/l04_sensitivity_r3.py -> {O}/l04_sensitivity_r3.out: base run prints 0 crossed and 0 conservation failures; mutant A (limit "
    "orders never match) prints 3 crossed events; mutant B (traded term halved for even fills) prints 296 conservation failures. "
    "The two counters are live, so the claim holds. Lab mutants are demonstrations (ruling), not graded mutants.")
row("FC1-b-r1-math-L04-examples-problems", "2.4 Examples 1.3-1.4, Problems M1-M3, P1-P3, R1-R3, misconception arithmetic",
    "L04.html lines 72, 77, 400-491, 377-385", "FAIL",
    f"Re-derived: Examples 1.3/1.4, M1, M2, M3, P2, E1-E3, R1, R2, R3 all check out (see {O}/l04_problems_r3.out and the num rows). "
    "P1 (line 423 statement, line 425 solution) does not: its first step uses a pre-arrival fact that is not among the facts it allows. See FC1-b-r3-proof-P1-hypothesis.",
    "Fix FC1-b-r3-proof-P1-hypothesis (L04.html line 423).")
row("FC1-b-r1-math-L05-prop21-prop22", "2.4 Proposition 2.1 and 2.2 statements, assumptions and proofs",
    "L05.html lines 75-96, 100, 519-520 (R2), 470 (P2)", P,
    "Prop 2.1(i) telescopes to 0 (line 84); (ii) uses c_i >= 0 from A1 and max(-x_j,0) <= Pay_j (line 85), with each consideration paid by exactly one buyer. "
    "Prop 2.2 (lines 90, 95): under A2 the CCP's receipts and payments are both G, so net cash 0; legs with the CCP equal the original amounts, so the net position is x_j. "
    "Hypotheses complete (fee, outside trades, novation stated). P2 bracket argument checked: f(x)=max(-x,0) is non-increasing and 1-Lipschitz, so the brackets lie in [-c,0] and [0,c] (needs c>=0 from A1).")
row("FC1-b-r1-math-L04-prop22-empty-side", "2.4 Proposition 2.2 proof completeness (empty side, residual cases), re-verified after round-1 FAIL",
    "L04.html lines 99, 104", P,
    "Beta = -inf and alpha = +inf conventions cover empty sides (line 104). Buy limit with residual on an empty bid side gives new best bid p; "
    "residual filled gives the market case; sell side symmetric. Re-derived by hand; no gap in these cases.")
row("FC1-b-r1-math-L04-prop23-assumptions", "2.4 Proposition 2.3 hypotheses complete (numbered A2; proof uses only A2 and the matching rules)",
    "L04.html lines 92-95, 108-111, 114-117, 365; card FC1-c066", P,
    "A2 is numbered (line 93) and stated (line 94: no withdrawal, cancellations only from market orders). The proof (line 116) uses only A2 "
    "and fill accounting. Stops are counted at activation (line 109), matching the code's submitted counter, which is incremented at match time.")
row("FC1-b-r1-math-L04-remark-definitions", "2.4 Definitions 1.1, 2.1, Remark 1.2 and Assumption A1 against the lab code",
    "L04.html lines 56-67, 84-89, 197-220 (match), 222-246 (activate), 302-313 (main loop)", P,
    "Remark 1.2 fill price (resting), last trade price, stop check after finished matching, arrival order, repeat until none triggers; "
    "each matches match() (fills at best.price, line 213) and activate() (lines 222-246) and the main loop (match, then activate, lines 308-309).")
row("FC1-b-r1-grades", "2.3 grades re-graded against BLUEPRINT (T proofs and hand computations; C lab-read counts naming the lab)",
    "L04.html lines 98, 108, 501-505; L05.html lines 78-96, 539-544, 403; cards", P,
    "T: Examples 1.3/1.4, Props 2.2 and 2.3 (proved), L05 Props 2.1 and 2.2 (proved). C: L04 row 505 and L05 rows 542-544 name Lab 1 as basis. "
    "L05 line 403 C is a book-level citation with no finding. Card grades T/C agree with the key-results rows.")
row("FC1-b-r1-notation", "2.4 notation vs notation/notation.json (8 registered symbols: T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, Q)",
    "L04.html and L05.html inline math (93 and 118 expressions)", P,
    "Symbol scan of both pages: no registered symbol or macro (\\E, \\Prob, \\R, \\N, \\Var, \\Cov, \\Corr, \\indic, \\Normal, T, Phi, gamma, R_f, Q) appears. "
    "Local symbols are defined at point of use with one meaning per lesson: L04 G, R, X, C, alpha, beta, p, q, s, t (lines 84-117); L05 G, NP, Rec, Pay, J, n, q_i, p_i, c_i, x_j (line 75).")
row("FC1-b-r1-prose-process-words", "2.9 / 2.x no process words in learner text (builder, verifier, ledger, round, admitted, reference list, course's)",
    "L05.html lines 397, 513, 630, 632; cards FC1-c090", P,
    "grep (admit, admission, reference list, course's, verifier, builder, ledger, round) over both pages and cards: no hits. Round-2 wording is fixed: "
    "L05 397 'because it cites no source for one'; 513 'this lesson names none'; 630 distractor 'one of the lesson's references gives it'; 632 'the lesson gives no settlement period'; "
    "c090 'the lesson cites no source for a settlement cycle'. Judgement, not a defect: 'registry key'/'registry year' (L04 line 590) and 'the registry holds' (L05 line 403) "
    "are the architect-sanctioned key citation form (plan line 587) also used on 111 course pages.")
row("FC1-b-r1-prose-banned-phrases", "2.9 / BUILDER_RULES 1.3-1.4 banned phrases", "L04.html, L05.html, cards.json", P,
    "check_pages FC1 PASS (banned-string check in visible prose). grep for TODO, TBD, lorem, for brevity, details omitted, beyond the scope, left as an exercise, "
    "you can add more, it is important to note, studies show, experts agree, it is well known, obviously, clearly: 0 hits in visible prose.")
row("FC1-b-r1-structure-L04", "2.9 / BUILDER 4.2 template sections, counts and hours", "L04.html", P,
    "Order: why (115 words, <=120) line 51; s1 Definitions and Examples; s2 Definition 2.1, A1, A2, Props 2.2, 2.3, Remark 2.4, lab (line 124); "
    "s3 canon (361); s4 misconceptions (3, lines 375-385); s5 problems (3 per tier, 12 solutions); s6 key results (5 rows); s7 quiz (9 items, 9 explanations); s8 references. "
    "No debate brief: the FC1 curriculum entry has no debate field. data-hours 10 and 'Lesson 4 of 5'.")
row("FC1-b-r1-structure-L05", "2.9 / BUILDER 4.2 template sections, counts and hours", "L05.html", P,
    "Order: why (115 words) line 52; s1 Definitions 1.1 and 1.2 and Remark 1.3; s2 Props 2.1, 2.2, Remark 2.3; s3 lab (line 107); s4 canon (393); "
    "s5 misconceptions (4); s6 problems (3 per tier, 12 solutions); s7 key results (6 rows); s8 quiz (11 items, 11 explanations); s9 references. "
    "No debate brief required (no debate field in the curriculum entry).")
row("FC1-b-r1-scope-words", "2.3 / 2.4 scope words (all, every, only, exactly, always) need a computation, proof or explicit hypothesis",
    "L04.html lines 67, 126, 358, 364, 475, 505; L05.html lines 63, 70, 390, 399", P,
    "'all' L05 line 63 is preceded by 'In this model' (explicit model hypothesis). 'every run' (L04 line 358) is backed by Props 2.2/2.3 under A1/A2. "
    "'only' (L04 line 67) is a stated rule of this model. 'exactly' (L04 line 475) is checked: the rule gives that sequence (l04_problems_r3). No 'always' used.")
row("FC1-b-r1-attribution-harris", "2.1 / 2.2 citation: harris2002trading, book level, registry fields only",
    "L04.html line 590; L05.html line 403; references/references.json; curriculum/02-economics-finance-core.yaml line 385", P,
    "Registry: Harris, 'Trading and Exchanges: Market Microstructure for Practitioners', DOI 10.1093/oso/9780195144703.001.0001, year 2002 (Crossref), "
    "years [2002, 2023]. Curriculum string 'Harris, Trading and Exchanges (2003)' (yaml 385). Pages print registry title and registry year only, as the architect decision requires (plan line 587). "
    "No passage or finding is attributed to the book. verify_refs live PASS this round.")
row("FC1-b-r1-settlement-source-absence", "2.1 scope of 'no settlement period is stated' and the claim that the course has no admitted settlement source",
    "L05.html lines 52, 105, 397, 513, 632; card FC1-c090; references/references.json", P,
    "The only period in the lesson is the lab's SETTLEMENT_LAG = 2 (twin line 138), labelled a parameter. Registry titles scan for 'settle', 'clearing': "
    "no settlement-cycle source (hits: bisndbasel, bisndcpmi, bis2024market are not settlement-cycle records; duffie2011central is about CCP risk and is used_by BK4 only). "
    "The text no longer claims the course lacks an admitted source. L05 line 399 'reads no evidence' on CCP risk is accurate for FC1.")
row("FC1-b-r1-references-L05", "2.1 claim-level citation with data-locator", "L05.html line 403; course/assets/js/refs.js lines 71-85", P,
    "The data-cite span sits in a .claim with data-locator (yaml 383-386; registry year 2002; no passage read). renderCitations (refs.js line 72) collects every [data-cite]; "
    "the numbered list is rendered at runtime, so page_smoke's zero console errors and failed requests cover the fetch. Rendered text not screenshot-checked (see notes).")
row("FC1-b-r1-references-L04-empty-list", "2.9 references section renders what the text claims ('cited here at book level only')",
    "L04.html lines 590-591; course/assets/js/refs.js lines 71-85, 135-146", P,
    "Empty <ol data-references> at line 591 is filled at runtime from the data-cite span at line 590 by the same mechanism; page_smoke PASS (no failed requests).")
row("FC1-b-r1-cards-L04", "2.7 cards for L04 (29 cards, all read against the lesson)",
    "cards.json FC1-c056-c072, c099, c100, c119, c121, c132, c133, c135, c141, c143, c154-c156", P,
    f"All 29 read in full and checked against the cited lesson locator. {O}/cards_scan_r3.out: 'L04 card numbers not found in lesson text: []'. "
    "Grades: c061, c062, c066, c068 T (matches key rows and R2); c069 C (matches row 505).")
row("FC1-b-r1-cards-L05", "2.7 cards for L05 (28 cards, all read against the lesson)",
    "cards.json FC1-c073-c090, c101, c102, c109, c114, c118, c123, c124, c142, c144, c145", P,
    f"All 28 read in full. {O}/cards_scan_r3.out: 'L05 card numbers not found in lesson text: []'. c090 (round-2 FAIL) is fixed. "
    "c082-c084 C match key rows 542-544; c079, c080, c101, c102 T match Props 2.1/2.2.")
row("FC1-b-r1-cards-duplicates", "2.7 full scan for duplicate cards across the unit", "cards.json (155 cards)", P,
    f"{S}/cards_scan_r3.py -> {O}/cards_scan_r3.out: 155 ids unique, 155 fronts unique. Jaccard >= 0.45 scan gives 11 pairs; none is a duplicate question "
    "(c058 buy stop vs c121 sell stop; c132 best bid vs c133 best ask are different questions with different answers).")
row("FC1-b-r1-card-c066", "2.7 a T card must carry its proposition's hypotheses", "cards.json FC1-c066; L04.html lines 92-95, 108-111", P,
    "Back carries A2 and the identity G = R + 2X + C, with C defined as market-order cancellations (line 109). The 'after every event' reading is supported by the proof, which does not depend on time (line 116).")
row("FC1-b-r2-cards-c154-c156", "2.7 new round-2 cards are atomic, correct against the lesson and not duplicates", "cards.json FC1-c154, c155, c156", P,
    "c154 is the Remark 1.2 example (line 67: 1010 earlier fill, 1000 last fill, stop 1005); c155 matches 'repeats until no pending stop triggers' (line 67); "
    "c156 matches A2 (line 94) and Definition 1.1 market-order cancellations (line 59).")
row("FC1-b-r1-labs-runtime-seed-network", "2.5 labs: seeded RNG, no network, stdlib only, under 10 s, SIMULATED label",
    "tests/labs/FC1/lab-FC1-L04-1.py, lab-FC1-L05-1.py", P,
    "SEED 2026 in both twins; imports only random, collections, dataclasses, datetime, itertools, collections.abc, __future__ (grep); "
    "no socket, urllib or requests; run 0.0 s each in page_smoke; SIMULATED stated at L04 lines 126, 358 and L05 lines 105, 109, 390 and twin docstring line 112.")
row("FC1-b-r1-lab-prose-consistency", "2.9 lab hypothesis, code docstrings and interpretation agree with output",
    "L04.html lines 126, 127-136, 153, 164, 177, 189, 198, 223-228, 250, 277, 289, 358; L05.html lines 109, 110-125, 145-148, 159, 173-175, 189-193, 240-243, 259-263, 274, 390", P,
    "Each docstring claim checked against code and output: e.g. L04 'market order keeps no residual' (match, cancelled += residual); 'checked for uncrossed book and share conservation' (main loop counters); "
    "L05 'offset 0 returns start, negative raises' (business_day_after); 'ratio half up' (ratio_milli_half_up, (2*1000*N+D)//(2D)).")
row("FC1-b-r1-misconceptions-canon", "2.9 misconceptions and canon-break sections: wrong belief, why wrong, evidence", "L04.html lines 364-368, 375-386; L05.html lines 397-401, 409-425", P,
    "Each misconception's numbers match the output: L04 1000/1100/1060 and 985 fill; 10 vs 100 share priority; L05 settlement offset 2 (Fri 2026-10-30), 14282414 vs 68398886, limit 10117 vs trade 10060.")
row("FC1-b-r1-inline-style", "2.9 / 360 px layout: inline style on L04 quiz fieldsets", "L04.html lines 517, 526, 545, 555, 569, 578", P,
    "style=\"min-inline-size: 0\" on six fieldsets only; L05 has none; page_smoke at 360 px PASS for both pages.")
row("FC1-b-r2-math-L04-prop22-stop-arrival", "2.4 Proposition 2.2 proof covers stop arrivals and activations",
    "L04.html line 104", P,
    "Round-2 gap is closed: the proof now states 'A stop that arrives and does not activate is not in the book, so the book is unchanged and the hypothesis carries over. "
    "A buy stop that activates is a market buy, which the market case covers.' The code agrees: an arriving stop is appended to pending (L04.html lines 305-306), not to bids or asks.")
row("FC1-b-r2-def12-order-entry-offset", "2.4/2.9 Definition 1.2 offsets: every fact used is named or derivable",
    "L05.html line 63; quiz explanation line 562; lab states list", P,
    "Round-2 gap is closed: Definition 1.2 states 'In this model order entry, matching and trade capture all occur on the trade date, so each has offset 0.' "
    "Quiz explanation line 562 cites it. The lab prints offset 0 for order_entry, matching and trade_capture (output lines 374-376).")
row("FC1-b-r2-canon-needs-empty-start", "2.4 overstatement check: 'needs' must be necessary, not merely sufficient",
    "L04.html line 367", P,
    "Round-2 FAIL is fixed: 'Proposition 2.2 needs the book to be uncrossed at the start, which the empty start of A1 gives, and Proposition 2.3 needs A2.' "
    "Prop 2.2 (line 99) uses only the uncrossed start and the rules of Section 1, so the statement is accurate.")
row("FC1-b-r2-A2-consistency", "2.4 numbered A2 used consistently within each lesson",
    "L04.html lines 51, 92-95, 109, 116, 126, 358, 365, 504-505; L05.html line 90; cards c066, c135, c156", P,
    "L04 A2 means no withdrawals everywhere it appears. L05 A2 (line 90) is a separate, named novation assumption in its own lesson. "
    "Same label, different lesson: no wrong use found. Note only.")
row("FC1-b-r2-terms-before-definition", "2.5 / 2.9 terms used before definition", "L04.html lines 51, 60-61; L05.html lines 52, 63, 66", P,
    "Forward uses are explicit pointers: 'Definition 2.1; A1' (line 51), 'defined in Lesson 4, Remark 1.2' (lines 60-61). L05 'trade date' is defined at line 63 before line 66 uses it.")
row("FC1-b-r2-cross-reference-style", "2.9 cross-reference style (self-reference to own lesson)", "L04.html lines 51, 59-61; L05.html line 66", P,
    "Self-references use the unit's 'Lesson n' convention and point to an existing Definition, Remark or Proposition on the same page.")
row("FC1-b-r3-proof-P1-hypothesis", "2.4 proof completeness of the problem-set proof P1 (its statement must carry the hypothesis its solution uses)",
    "L04.html line 423 (statement), line 425 (solution)", "FAIL",
    "Statement: 'Under A1, prove that the book is not crossed after an arriving market buy order, using only the facts that a market buy removes asks and leaves bids unchanged.' "
    "Solution first step: 'Before the arrival, the best bid beta is below the best ask alpha.' That fact is not one of the allowed facts. A1 gives it only for the first event "
    "(empty book, beta = -inf); for a later arrival it is the induction hypothesis of Prop 2.2 (line 104), which the statement does not supply.",
    "In L04.html line 423, replace the statement with: 'Let the book be uncrossed before an arriving market buy order (A1 gives this for the first event, since the book starts empty). "
    "Prove that it is not crossed after the arrival, using only the facts that a market buy removes asks and leaves bids unchanged.'")
row("FC1-b-r3-hours", "2.9 / BUILDER 4.3 hours split and lesson hours arithmetic", "L04.html line 2 and 34; L05.html line 2 and 35; course/modules/FC/FC1/index.html line 29; curriculum yaml line 364", P,
    "data-hours 10 and '10 study hours' in both lessons; hub data-hours-lessons 50 = 5 x 10; data-hours-project 20; 50 + 20 = 70 = curriculum module hours (yaml 364). Lesson hours are design targets (ruling).")
row("FC1-b-r3-lesson-links", "2.9 lesson navigation links resolve", "L04.html lines 596-597; L05.html lines 649-650", P,
    "L04 prev L03.html, next L05.html; L05 prev L04.html, next project.html. All four targets exist in course/modules/FC/FC1/.")

ids = [r["id"] for r in rows]
assert len(ids) == len(set(ids)), "duplicate ids"
counts = {s: sum(1 for r in rows if r["status"] == s) for s in ("PASS", "FAIL", "UNVERIFIABLE")}
frag = {
    "unit": "FC1",
    "slice": "FC1-b",
    "round": 3,
    "verifier": "Claude Haiku 5.5, independent verifier for FC1-b round 3 (did not build FC1; read verifier-rules.md, VERIFIER_RULES.md, BUILDER_RULES.md, plans/FC1-build-plan.md, round-2 fragment as context only)",
    "pin": "8196077d5f56c3919d33e69888176d197d378ad4",
    "base": "9294b914a51647c66d2dee62c4a112c76ba04900 (round-2 pin, fragment /Users/billyribeiro/.fanout/frags/S-FC1-b.round2.json)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyS3-FC1-b",
    "scratch": "ledgers/FC1/scripts/FC1-b-r3/",
    "verified_at": datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat(),
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [
        "harris2002trading: curriculum yaml line 385 reads 'Harris, Trading and Exchanges (2003)'; registry record year 2002 (Crossref), years [2002, 2023]. "
        "The pages cite the key with registry fields only (plan line 587), so no page change is needed. The curriculum string should be corrected by its owner; no registry edit requested."
    ],
    "freshness_flags": [],
    "notes": (
        "Round 3 for slice FC1-b at pin 8196077d (delta from 9294b914). Changed subjects in the slice: L04.html (proof line 104 stop sentence; "
        "canon line 367; why-it-matters line 51; reference line 590 unchanged), L05.html (lines 52, 63, 397, 513, 562, 630, 632), cards.json (FC1-c090, FC1-c156 text; "
        "c025 and c050 are L02/L03 and out of slice). Lab twins, notation, references, tools and the FC1 curriculum were unchanged in the delta (git diff --quiet on tests/labs/FC1; "
        "git diff --stat on tools, references, notation shows no FC1-relevant change). Because both pages changed, every round-2 row is re-verified from scratch, none carried; "
        "all 49 round-2 ids are kept. Round-2 FAILs (prose-process-words, prop22-stop-arrival, def12-order-entry-offset, canon-needs-empty-start) are now PASS with evidence. "
        "New FAIL: problem P1 (L04.html line 423-425) uses an unstated pre-arrival hypothesis; it also makes math-L04-examples-problems FAIL. "
        "Scope: slice b has no autograder, so the three-mutant rule does not apply; mutants is []. Lab sensitivity mutants (l04_sensitivity_r3.py, l05_sensitivity_r3.py) "
        "show the lab's own counters are live; they are demonstrations, not graded mutants. "
        "Judgement calls recorded in evidence, not failed: 'registry key' and 'the curriculum lists' wording (architect-sanctioned key citation, used on 111 pages); "
        "'crossed' and 'A1' used in the why-it-matters preview with forward pointers; assumption label A2 reused across L04 and L05 with different content; the non-decreasing offsets convention "
        "in L05 line 66 is a model statement that no proof uses. "
        "Not checked: the rendered References list (refs.js output) was not screenshot-checked; no visual check of the pages beyond page_smoke; repo-wide ruff, mypy and full pytest "
        "were not run (scope); the hub, L01-L03 and project page are other slices; check_projects and run_graders do not apply to slice b; "
        "the Harris book was not read (book-level citation only, no passage claimed)."
    ),
    "summary": (
        f"Slice FC1-b (L04, L05, both lab twins, 57 cards) at 8196077d, round 3: {counts['PASS']} PASS, {counts['FAIL']} FAIL, "
        f"{counts['UNVERIFIABLE']} UNVERIFIABLE of {len(rows)} rows; mutants 0/0. All gates re-run and green (check_pages, check_dag, run_labs, twins alone, "
        "page_smoke, ruff, mypy, lab pytest, page/curriculum pytest, build_site --check, verify_refs offline and live). "
        "One FAIL: problem P1 (L04.html line 423-425) relies on a pre-arrival uncrossed-book fact its statement does not give. "
        "All four round-2 FAILs are fixed and verified."
    ),
}
out = ROOT / "ledgers/FC1/FC1-b.json"
out.write_text(json.dumps(frag, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out, counts, len(rows))
