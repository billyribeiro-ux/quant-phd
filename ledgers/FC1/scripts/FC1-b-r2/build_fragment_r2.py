# Round-2 FC1-b fragment builder (verifier-authored). Writes ledgers/FC1/FC1-b.json and validates it with tools/ledger.py.
import json, sys
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(sys.argv[1])
S = "ledgers/FC1/scripts/FC1-b-r2/"
R = []

def row(rid, check, location, status, evidence, fix=None):
    d = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        d["fix"] = fix
    R.append(d)

# ---- gates (re-run this round at pin 9294b914) ----
row("FC1-b-r1-gate-check-pages", "tools/check_pages.py --unit FC1 --page L04; --page L05; --unit FC1",
    "course/modules/FC/FC1/L04.html, L05.html, cards.json", "PASS",
    f"Re-run at 9294b914: 'check_pages FC1 L04: PASS' rc 0, 'check_pages FC1 L05: PASS' rc 0, 'check_pages FC1: PASS' rc 0 ({S}check_pages.out).")
row("FC1-b-r1-gate-check-dag", "tools/check_dag.py --unit FC1", "L04.html, L05.html and the unit", "PASS",
    f"Re-run: 'check_dag FC1: PASS' rc 0 ({S}check_dag.out). L04 links to L03 def-bid-ask-spread (Uses line, L04.html line 37); L05 links to L01 def-financial-intermediary (L05.html line 38, 58) and L04 def-order-types and def-limit-order-book.")
row("FC1-b-r1-gate-run-labs", "tools/run_labs.py --unit FC1 --page L04 / --page L05", "tests/labs/FC1/lab-FC1-L04-1.py, lab-FC1-L05-1.py", "PASS",
    f"Re-run: 'run_labs FC1: PASS (1/1)' rc 0 for each page ({S}run_labs.out).")
row("FC1-b-r1-gate-twin-alone", "twin run alone: .venv (CPython 3.14.8) python -I -W error <twin>; stdout compared with the page's pre.expected",
    "tests/labs/FC1/lab-FC1-L04-1.py, lab-FC1-L05-1.py", "PASS",
    f"{S}v2_twin_vs_page.out: L04 twin rc 0, stderr 0 bytes, expected == stdout; L05 twin rc 0, stderr 0 bytes, expected == stdout; 'ALL OK'. Note: the first attempt used /usr/bin/python3 (3.9.6) and failed on itertools.pairwise; the project pins 3.14 (CLAUDE.md), so the venv interpreter is the valid runtime, and the twin is not at fault.")
row("FC1-b-r1-gate-page-code-equals-twin", "page code block equals twin (embed fidelity), markers absent",
    "L04.html code block (lines 127-335); L05.html code block (lines 110-365)", "PASS",
    f"{S}v2_twin_vs_page.out: L04 page code 8554 bytes = twin 8554, identical; L05 10551 = 10551, identical; '@@LAB'/'@@OUT' count 0 in both pages. Twin files unchanged since aeb512b (git diff --quiet on tests/labs/FC1).")
row("FC1-b-r1-gate-expected-equals-output", "pre.expected equals the twin's printed output", "L04.html lines 336-357; L05.html lines 366-389", "PASS",
    f"{S}v2_twin_vs_page.out: 'expected == stdout' True for both twins (after html unescape and outer-newline strip).")
row("FC1-b-r1-gate-page-smoke", "tools/page_smoke.py --unit FC1 --pages L04 L05 (Chromium, Pyodide, console, math, 360 px, external requests)",
    "L04.html, L05.html", "PASS",
    f"Re-run: 'page_smoke modules/FC/FC1/L04.html: PASS', 'modules/FC/FC1/L05.html: PASS', 'page_smoke FC1: PASS' rc 0; lab-FC1-L04-1 0.0 s, lab-FC1-L05-1 0.0 s ({S}page_smoke_L04_L05.out).")
row("FC1-b-r1-gate-ruff", "ruff check and ruff format --check on the two twins", "tests/labs/FC1/lab-FC1-L04-1.py, lab-FC1-L05-1.py", "PASS",
    f"'All checks passed!' rc 0; '2 files already formatted' rc 0 ({S}lint_types.out). Repo-wide ruff not run (scope).")
row("FC1-b-r1-gate-mypy", "mypy --no-incremental on the two twins", "tests/labs/FC1/lab-FC1-L04-1.py, lab-FC1-L05-1.py", "PASS",
    f"'Success: no issues found in 2 source files' rc 0 ({S}lint_types.out).")
row("FC1-b-r1-gate-pytest-labs", "pytest tests/test_labs.py tests/test_run_labs.py -k 'FC1 or L04 or L05' -q", "tests/test_labs.py", "PASS",
    f"rc 0, all selected tests passed ({S}pytest_labs_fc1.out).")
row("FC1-b-r1-gate-verify-refs-offline", "tools/verify_refs.py --offline", "references/references.json", "PASS",
    f"'offline integrity: 560 entries, 0 problems' rc 0 ({S}verify_refs_offline.out). references.json changed since aeb512b only in generated_at and used_by (FC2 added to the used_by list of abadie2010synthetic); no FC1 record changed.")
row("FC1-b-r2-gate-verify-refs-live-unit", "tools/verify_refs.py --unit FC1 (live Crossref/Open Library/landing re-resolution, cache bypassed)",
    "references/references.json: harris2002trading, mishkin2021economics", "PASS",
    f"'live re-verification of FC1: 2 of 560 entries, 0 problems' rc 0 ({S}verify_refs_unit_FC1_live.out). This re-resolves the record behind the L04/L05 Harris citation, which the round-1 fragment left unverified.")

# ---- numbers ----
row("FC1-b-r1-num-L04-prose", "2.2 numbers in prose re-derived by an independent book (own code, same RNG draw order)",
    "L04.html lines 72, 77, 400, 407, 414, 432, 450, 464, 476, 489, 501-505", "PASS",
    f"{S}v2_l04_numbers.py / .out and {S}v2_l04_problems.py / .out: Fixture A fills (1000,60),(1100,90), cost 159000, average 1060, 10 left at 1100; Fixture B (990,100),(985,100), one activation. M1: fills (995,60),(990,40), cost 99300, average 993, bid 990 keeps 60. M2: fills (1000,30),(1001,20), asks left 10@1001 and 40@1003, bids empty. P2: G=250, X=100, C=50, R=0, R+2X+C=250. R1 cascade (990,100),(985,100),(980,100) with 2 activations. R2: bid 1005 >= ask 1000 after the 999 buy. R3: 60+60=120. E1: 24+18=42. E3: 5600/173 = 32.3699... (exact fraction 5600/173). All equal the page.")
row("FC1-b-r1-num-L04-lab-output", "2.5 lab numbers, expected block and interpretation, re-run independently and under mutation",
    "tests/labs/FC1/lab-FC1-L04-1.py; L04.html lines 351-358 (interpretation), 505 (key result)", "PASS",
    f"{S}v2_l04_numbers.out reproduces every expected line: 181 limit, 77 market, 42 stop; 173 trades; 5600 shares; 24 activated; 18 pending; 220 cancelled; 4710 resting; 0 crossed; 0 conservation failures; end 9997/10001; trace events 0-7 (best bid 9984 for events 0-6, none after event 7). {S}v2_l04_sensitivity.out: halving the traded term gives 296 conservation failures; withdrawing one resting bid at event 100 gives 200. The counters are live, and A2 is needed.")
row("FC1-b-r1-num-L05-prose", "2.2 numbers in prose re-derived (own code, same RNG call order)",
    "L05.html lines 109, 366-389, 390, 396-400, 442-452, 484-504, 544, 607", "PASS",
    f"{S}v2_l05_numbers.py / .out: fill 216 at 10060 (P2's 263-share sell), consideration 2172960; limit 10117 >= 10060; settlement at lag 2 = Friday 2026-10-30 (Wed 2026-10-28 + 2 business days); gross 68398886; net 14282414; net payers P1, P2, P4; positions sum to 0. Ratio exact 0.20881062302681364; 8 dp 0.20881062; 5 dp 0.20881; half-up 3 dp 0.209 (integer method gives 209). E1: 11060360/68398886 = 0.1617038 (16.17%); 11060360/14282414 = 0.7744041 (77.44%). E2: 7411991+6656379+214044 = 14282414 = 3222054+11060360. M1 = 1009000. M2: Monday 2026-11-02 offset 1, Tuesday 2026-11-03 offset 2. M3: 1000000/2000000 = 0.500. R2: 100 <= -100 is false. Weekdays checked with datetime.")
row("FC1-b-r1-num-L05-lab-output", "2.5 lab output and hypothesis numbers vs. independent re-derivation", "tests/labs/FC1/lab-FC1-L05-1.py; L05.html lines 109, 366-389", "PASS",
    f"{S}v2_l05_numbers.out reproduces resting book (P2 10060x263, P3 10257x362, P4 10331x152), incoming P1 10117x216, one fill, the state dates and offsets, and the 20-trade batch: 68398886 gross, 14282414 net, 3 net payers, net positions -7411991, -6656379, 3222054, -214044, 11060360, sum 0.")
row("FC1-b-r1-lab05-parameter-claims", "2.5 lesson sentences about what changing the parameters does (E3 solution, interpretation, card c142, canon-break)",
    "L05.html lines 390 (interpretation), 502 (E3 solution), 66; cards.json FC1-c142", "PASS",
    f"{S}v2_l05_sweep.py / .out on scratch copies of the twin: SETTLEMENT_LAG=3 changes exactly 3 lines (header, settlement -> Mon 2026-11-02 offset 3, position_update) and offsets_nondecreasing stays True, as E3 says. CLEARING_OFFSET=1 changes the header and the clearing line only; =2 (equal to lag) keeps True; =3 (above lag) prints False, as the interpretation and card c142 say. The E2 and E3 solution texts were re-read against this output.")
row("FC1-b-r1-lab04-invariant-claim", "2.5 lab claim that Lab 1 checks both invariants after each event",
    "L04.html lines 51, 126, 358; lab lines 302-314", "PASS",
    f"The counters are live: {S}v2_l04_sensitivity.out (296 and 200 failures under two injected faults) and {S}v2_l04_problems.out (200 seeded flows x 300 events: 0 crossed, 0 conservation failures).")

# ---- mathematics ----
row("FC1-b-r1-math-L04-examples-problems", "2.4 Examples 1.3-1.4, Problems M1-M3, P1-P3, R1-R3 and misconception arithmetic",
    "L04.html lines 72, 77, 377-385, 400-491", "PASS",
    f"Each worked solution re-run through the independent book ({S}v2_l04_problems.out): M1, M2, P2, R1, R2, R3, Remark 1.2 stop trigger (last 1000 no, last 1010 yes), misconception 3 and L04q6 (earlier 100-share sell fills 10). Hand arithmetic re-checked: M3 stop reasoning (1005 > 1000 no; 1001 > 1000 no; 1000 at stop yes); E1, E3.")
row("FC1-b-r1-math-L05-prop21-prop22", "2.4 Proposition 2.1 and 2.2 statements, assumptions and proofs",
    "L05.html lines 75-96", "PASS",
    f"Proofs re-read step by step: 2.1(i) telescoping with c_i - c_i = 0; 2.1(ii) NP >= 0, -x_j <= Pay_j, sum Pay_j = G under A1 (c_i > 0). 2.2: CCP receives G, pays G, net cash 0; legs give x_j. Property checks ({S}v2_l05_numbers.out): 0 failures of sum x = 0 and 0 <= NP <= G over 2000 random batches; P2's |NP(B) - NP(B')| <= c_t bound: 0 failures over 2000 batches.")
row("FC1-b-r1-math-L04-prop22-empty-side", "2.4 Proposition 2.2 proof completeness (empty side), re-verified after the round-1 FAIL",
    "L04.html lines 99 (statement), 104 (proof)", "PASS",
    f"Round-1 FAIL is fixed. The proof now sets beta = -inf for an empty bid side and alpha = +inf for an empty ask side, so 'crossed' is exactly beta >= alpha, and the chains hold: market buy gives beta < alpha <= alpha'; buy limit residual rests with new best bid max(beta, p) (= p when the bid side was empty), alpha' > p and alpha' >= alpha, so max(beta, p) < alpha'. Empty-ask case: alpha' = +inf. Both-empty: -inf < +inf. The stop-arrival case is still missing: see FC1-b-r2-math-L04-prop22-stop-arrival.")
row("FC1-b-r1-math-L04-prop23-assumptions", "2.4 Proposition 2.3 hypotheses complete (numbered Assumption A2; proof needs no hypothesis the statement omits)",
    "L04.html lines 92-95 (A2), 108-111 (statement), 115-117 (proof), 365 (canon-break), cards.json FC1-c066", "PASS",
    f"Round-1 FAIL is fixed. A2 (no withdrawals) is numbered at L04.html lines 92-95 and the statement begins 'Assuming A2' (line 109). The proof begins 'Under A2 a resting order leaves the book only by trading' (line 116). Pending stops are in neither G nor R, so their absence needs no term (Book.pending is excluded from resting(), page line 178). The identity fails without A2 ({S}v2_l04_sensitivity.out: 200 failures after one withdrawal). Card FC1-c066 now says 'Under A2'.")
row("FC1-b-r1-math-L04-remark-definitions", "2.4 Definitions 1.1, 2.1, Remark 1.2 and Assumption A1 against the lab code",
    "L04.html lines 56-67, 83-89; L04.html code block lines 166-175 (Book.__init__), 197-220 (match), 222-246 (activate), 299-313 (main loop)", "PASS",
    "Re-read against the page code block (identical to the twin): limit buy trades at best ask <= p, sell at best bid >= p (line 205); fill at resting price (line 212); market residual cancelled (lines 218-220); activate runs after match (line 309) and repeats until none triggers (lines 230-246); buy stop triggers at last >= stop, sell stop at last <= stop (line 236); crossed is bid >= ask (line 311); empty start (Book.__init__, lines 166-170; A1 at line 89). The Remark 1.2 sentences on earlier fills and arrival order match the code.")
row("FC1-b-r1-grades", "BLUEPRINT grades: T on proofs and hand computations; C on lab-read counts with the lab named and a basis",
    "L04.html lines 93-115, 499-505; L05.html lines 78-96, 539-544; cards.json", "PASS",
    "T: Props 2.2, 2.3 (L04) and 2.1, 2.2 (L05), Examples 1.3, 1.4 (hand computation). Cards graded T carry their hypotheses: c066 'Under A2', c079 and c101 'Under A1', c080 'Under A1 and A2', c102 'Under A1 and A2', c089 with the A1 sign step. C: lab-read counts naming Lab 1 with a basis: c069, c082, c083, c084, c085, c086, c088 (each has a basis field).")
row("FC1-b-r1-notation", "2.4 notation vs notation/notation.json (T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, Q, and registered macros)",
    "L04.html and L05.html inline math (93 and 115 expressions)", "PASS",
    f"Extracted all \\(...\\) and \\[...\\] expressions with {S}v2_notation.py (output {S}v2_notation.out). Registry symbols T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{{e\\ast}}, R_f, \\mathbb{{Q}} and registry macros (\\E, \\R, \\N, \\Prob, ...) do not occur as tokens. The scan's only hit is the bare letter R, which the crude matcher paired with R^\\ast; the lesson's R is the resting-share count defined at L04.html line 109 and is not the registered R^\\ast, so there is no collision. Local symbols: L04 G, R, X, C, p, q, s, t, alpha, beta, infty (Prop 2.2 proof, defined there); L05 G, J, B, NP, Rec, Pay, x_j, c_i, q_i, p_i, f, b, s (P2), c_t (P2), x_A, x_B, x_C (M3). None reuses a registry meaning.")
row("FC1-b-r1-prose-process-words", "2.9 / 2.x no process words in learner text (builder, verifier, ledger, round, admission and registry-state words)",
    "L05.html lines 397, 513, 630; cards.json FC1-c090 (back)", "FAIL",
    f"Learner text describes the course's admission state of its reference list: L05.html line 397 'no settlement-cycle source is yet admitted to the course's reference list'; line 513 (R1 solution) 'The course has not admitted a settlement-cycle source, so the study must first admit one'; line 630 (quiz option) 'Yes, a source in the reference list gives it'; FC1-c090 back 'no settlement-cycle source is yet admitted to the course's reference list'. These describe the build's sourcing state, not the subject. Scan: {S}v2_prose_scan.out. Other process words absent; 'round' occurs only as 'rounded'. The round-1 check missed the admission wording.",
    "L05.html line 397: replace with 'This lesson states no settlement period for any market, because it cites no source for one. The lag in Lab 1 is a parameter.' Line 513: replace the solution's first sentence with 'The study needs a primary record of the venue, the clearing house or the regulator, with a stated page; this lesson names none.' Line 630: replace the option text with 'Yes, one of the lesson\\'s references gives it' (false: the lesson cites Harris only, and the registry scan finds no settlement-cycle record). FC1-c090 back: 'Because the lesson cites no source for a settlement cycle. The two-day lag of Lab 1 is a parameter, not a period for any market (Section 4).' Rebuild cards with the card rules; keep grade absent.")
row("FC1-b-r1-prose-banned-phrases", "2.9 / BUILDER 1.3-1.4 banned phrases", "L04.html, L05.html, cards.json", "PASS",
    f"Python scan ({S}v2_prose_scan.out) for TODO, TBD, lorem, for brevity, details omitted, beyond the scope, left as an exercise, you can add more, it is important to note, studies show, experts agree, it is well known, obviously, clearly and ellipses outside code: no hit. check_pages banned-string rule PASS ({S}check_pages.out).")
row("FC1-b-r1-structure-L04", "2.9 / BUILDER 4.2 template sections, counts and hours", "L04.html", "PASS",
    "Order: why-it-matters (113 words, max 120; counted this round); s1 Definition 1.1, Remark 1.2, Examples 1.3-1.4; s2 Definition 2.1, A1, A2, Proposition 2.2 with proof, Proposition 2.3 with proof, Remark 2.4, Lab 1; s3 canon-breaks; s4 misconceptions (3); s5 problems (Mechanics M1-M3, Proof P1-P3, Empirical E1-E3, Research R1-R3: 12 details.solution blocks); s6 key results (5 rows); s7 quiz (9 items, each with explain block, one correct option per mc item); s8 references. data-hours=10 matches the plan.")
row("FC1-b-r1-structure-L05", "2.9 / BUILDER 4.2 template sections, counts and hours", "L05.html", "PASS",
    "Order: why-it-matters (113 words); s1 Definitions 1.1-1.2, Remark 1.3; s2 Proposition 2.1 and 2.2 with numbered A1, A2, proofs, Remark 2.3; s3 Lab 1; s4 canon-breaks; s5 misconceptions (4); s6 problems (12 details.solution blocks); s7 key results (6 rows); s8 quiz (11 items with explain blocks); s9 references. data-hours=10.")
row("FC1-b-r1-scope-words", "2.3 / 2.4 scope words (every, all, any, never, only, exactly) need a computation, proof or explicit hypothesis", "L04.html lines 51, 59, 94, 99, 353, 358, 505; L05.html lines 70, 390, 399, 419", "PASS",
    "'every run that starts from the empty book (A1)' is Proposition 2.2 under A1 (induction, lines 104-105). 'every run with no withdrawals (A2)' is Proposition 2.3 under A2. 'at every one of the 300 events in this run' is backed by the counters ({S}v2_l04_numbers.out). 'only the last trade price at the check counts' is the model rule of Remark 1.2 (code line 309 and activate). L05 'states no finding on whether central clearing reduces counterparty risk' is a scope limit.")
row("FC1-b-r1-attribution-harris", "2.1 / 2.2 citation attribution: harris2002trading (book level, registry year only)", "L04.html line 590; L05.html line 403; references/references.json; curriculum/02-economics-finance-core.yaml line 385", "PASS",
    "Registry record: key harris2002trading, Oxford University Press, DOI 10.1093/oso/9780195144703.001.0001, year 2002 (notes.year curriculum 2003, crossref 2002). Curriculum yaml line 385 lists 'Harris, Trading and Exchanges (2003)' among the FC1 sources (the FC1 concept block is lines 378-382). Both pages cite by key with the registry year only and claim no passage. Live Crossref check PASS (FC1-b-r2-gate-verify-refs-live-unit). Architect decision (plan line 587 block) followed.")
row("FC1-b-r1-settlement-source-absence", "2.1 scope of 'no settlement period is stated' and the claim that no settlement-cycle source is admitted", "L05.html lines 58-59, 397; cards.json FC1-c090", "PASS",
    f"Registry scan over 560 records ({S}v2_registry_settlement_scan.out): the only record matching settlement-cycle, settlement period, T+n, clearing or counterparty terms is duffie2011central (a counterparty-risk paper); none gives a settlement cycle. The lesson states no settlement period and treats the lag as a parameter. The 'admitted' wording itself is the separate FAIL row FC1-b-r1-prose-process-words.")
row("FC1-b-r1-references-L05", "2.1 claim-level citation with data-locator", "L05.html line 403", "PASS",
    "Span carries data-cite=harris2002trading and a data-locator naming the curriculum sources list (yaml 383-386) and the registry year; the span says 'no passage read for this lesson'. The locator is a curriculum listing, not a book passage, and is labelled as such.")
row("FC1-b-r1-references-L04-empty-list", "2.9 references section renders what the text claims ('cited here at book level only')", "L04.html lines 590-591; course/assets/js/refs.js lines 71-85, 135-146", "PASS",
    "Round-1 FAIL is fixed. L04.html line 590 now wraps the Harris title in span data-cite=\"harris2002trading\". refs.js collects every [data-cite] key into the order list (lines 71-85) and fills ol[data-references] with it (lines 135-146), so the References list at line 591 is no longer empty. Rendering was exercised by page_smoke (PASS).")

# ---- cards ----
row("FC1-b-r1-cards-L04", "2.7 cards for L04 (29 cards, all read against the lesson)", "course/modules/FC/FC1/cards.json: FC1-c056-c072, c099, c100, c119, c121, c132, c133, c135, c141, c143, c154-c156", "PASS",
    f"All 29 read against L04.html. Changed this round and re-checked: c060 (when stops are checked, Remark 1.2), c066 (Under A2), c135 (A2 withdrawal), c141 (arrival order), c154-c156 (new; c154 uses 1010/1005/1000 as Remark 1.2 does). {S}v2_cards_check.out: every 'Definition/Remark/Proposition/Assumption/Example/Problem/Section' label and every 3+ digit number in each card appears in L04.html or L05.html; no failures.")
row("FC1-b-r1-cards-L05", "2.7 cards for L05 (28 cards, all read against the lesson)", "course/modules/FC/FC1/cards.json: FC1-c073-c090, c101, c102, c109, c114, c118, c123, c124, c142, c144, c145", "PASS",
    f"All 28 read against L05.html. c075 matches Definition 1.2 (trade date has offset 0); c084 matches the rounding; c142 matches the sweep. {S}v2_cards_check.out: no label or number failures. c090 is FAILed under the process-words row (admission wording), not for its content.")
row("FC1-b-r1-cards-duplicates", "2.7 full scan for duplicate cards across the unit", "course/modules/FC/FC1/cards.json (155 cards)", "PASS",
    f"{S}v2_cards_check.out: 155 cards; no duplicate ids, fronts or backs. Near-duplicates read and judged distinct: c060 vs c154 (when stops are checked vs which price counts); c141 vs c155 (order of activations vs whether the check repeats); c135 vs c156 (both state A2's no-withdrawal content, but c135 asks whether a withdrawal term exists and c156 asks what A2 fixes).")
row("FC1-b-r1-card-c066", "2.7 a T card must carry its proposition's hypotheses", "course/modules/FC/FC1/cards.json FC1-c066 (back); L04.html lines 92-95, 108-111", "PASS",
    "Round-1 FAIL is fixed. The back reads 'Under A2 (no withdrawals), G = R + 2X + C after every event ... (Proposition 2.3).' Grade T kept; matches A2 and Proposition 2.3 as stated.")
row("FC1-b-r2-cards-c154-c156", "2.7 new cards (round 2) are atomic, correct against the lesson and not duplicates", "course/modules/FC/FC1/cards.json FC1-c154, c155, c156", "PASS",
    "c154: buy stop at 1005, earlier fill 1010, last fill 1000: not triggered (Remark 1.2 says the same). c155: each activation can move the last price, so the check repeats (Remark 1.2). c156: what A2 fixes (A2 text, L04.html lines 92-95). Each is checkable against the lesson text.")
row("FC1-b-r1-labs-runtime-seed-network", "2.5 labs: seeded RNG, no network, under 10 s, standard library only", "tests/labs/FC1/lab-FC1-L04-1.py line 18 (SEED = 2026); tests/labs/FC1/lab-FC1-L05-1.py line 26 (SEED = 2026)", "PASS",
    "Imports only from the standard library (L04: random, collections, dataclasses, __future__; L05: datetime, itertools, random, collections.abc, dataclasses, __future__). Fixed seed 2026 in both. Twins run under python -I -W error (FC1-b-r2-gate-twin-alone). page_smoke lab times 0.0 s.")
row("FC1-b-r1-lab-prose-consistency", "2.9 lab hypothesis, code docstrings and interpretation agree with output", "L04.html lines 126, 127-136 (docstring), 358; L05.html lines 109, 110-125 (docstring), 390", "PASS",
    "Hypotheses state the printed numbers (checked above). L04 docstring: fill at resting price, ties by arrival, cancelled market residual, stop checked after matching, conservation exact (code matches). L05 docstring: business day Monday-Friday with no holiday calendar (business_day_after), ratio rounded half up in integers (ratio_milli_half_up, verified), SIMULATED labels present.")
row("FC1-b-r1-misconceptions-canon", "2.9 misconceptions and canon-break sections: wrong belief, why wrong, evidence", "L04.html lines 364-368, 375-386; L05.html lines 397-401, 409-425", "PASS",
    "Each misconception names a worked example (L04 Examples 1.3, 1.4 and the 10/100 share case; L05 printed numbers 14282414 and 68398886, and 10117 vs 10060). The canon-break overstatement about 'needs the empty start' is a separate FAIL row (FC1-b-r2-canon-needs-empty-start).")
row("FC1-b-r1-inline-style", "2.9 / 360 px layout (inline style on L04 quiz fieldsets)", "L04.html lines 517, 526, 545, 555, 569, 578 (style min-inline-size: 0)", "PASS",
    f"page_smoke 360 px check PASS for both pages ({S}page_smoke_L04_L05.out). Inline style is the per-page workaround noted in the open items; not a rule violation.")

# ---- new round-2 findings ----
row("FC1-b-r2-math-L04-prop22-stop-arrival", "2.4 Proposition 2.2 proof covers every event; an event is 'an arrival or an activation of a stop' (L04.html line 99)",
    "L04.html line 104 (proof of Proposition 2.2)", "FAIL",
    "The proof's cases are an arriving buy order (market or limit), and sell orders and sell-side activations 'by the same argument'. An arriving stop order that does not activate is an arrival, hence an event by the proposition's own definition, and no case treats it. It leaves the book unchanged, so the claim holds from the hypothesis, but the step is absent and the proof is not complete as written.",
    "In the proof of Proposition 2.2, before 'Sell orders and sell-side activations', add: 'A stop that arrives and does not activate is not in the book, so the book is unchanged and the hypothesis carries over.'")
row("FC1-b-r2-def12-order-entry-offset", "2.4/2.9 Definition 1.2 offsets: every fact used is named or derivable from the definitions",
    "L05.html line 63 (Definition 1.2), line 562 (quiz L05q1 explanation), line 317 (lab state order_entry offset 0)", "FAIL",
    "Round 2 makes the trade date the business day of matching and says each state's offset counts business days after the trade date. The lesson never states order entry's offset, yet the quiz explanation says order entry 'has offset 0, the trade date' and the lab hard-codes 0. An order that arrived on an earlier business day would need a negative offset, which the definition's wording does not admit and which the lab's business_day_after rejects ('no state of a trade precedes its trade date', code lines 175-178). The fact that order entry, matching and trade capture all fall on the trade date is assumed without being named.",
    "In Definition 1.2 add: 'In this model order entry, matching and trade capture all occur on the trade date, so each has offset 0.' (Or name it as a numbered assumption and cite it in the quiz explanation.)")
row("FC1-b-r2-canon-needs-empty-start", "2.4 overstatement check: 'needs' claims must be necessary, not merely sufficient",
    "L04.html line 367 (Section 3 bullet 'The invariants depend on A1 and A2')", "FAIL",
    "The text says 'Proposition 2.2 needs the empty start in A1'. The proof uses only that the book is not crossed before an event (line 104), which any uncrossed start gives. The empty start is sufficient, not necessary, so the 'needs' claim is false as stated. Problem R2 shows what fails from a crossed start, which is the true contrast.",
    "Replace the sentence with: 'Proposition 2.2 needs the book to be uncrossed at the start, which the empty start of A1 gives, and Proposition 2.3 needs A2.'")
row("FC1-b-r2-A2-consistency", "2.4 the new numbered Assumption A2 is used consistently and nothing relies on an unnumbered 'no withdrawals' hypothesis",
    "L04.html lines 51, 92-95, 109, 116, 126, 358, 365, 504-505; cards.json FC1-c066, c135, c156", "PASS",
    f"A2 appears in the why-it-matters (51), its definition (92-95), the Proposition 2.3 statement (109) and proof (116), the lab hypothesis (126), interpretation (358), canon-break (365), key results (504-505), and cards c066, c135, c156. Grep for 'withdraw' in L04.html (lines 51, 93, 94, 126, 358, 365, 505): every occurrence is in the A2 context (the A2 gloss, its definition, the lab hypothesis, the interpretation, the canon-break and the key-results row). No unnumbered use. The lab flow generates no withdrawals ('The flow generates no withdrawals, so A2 holds for it', line 126), and the code has no cancel or modify path (page code block lines 197-246 and 299-313).")
row("FC1-b-r2-terms-before-definition", "2.5 / 2.9 terms used before definition (round-2 prose)",
    "L04.html line 51 ('crossed', 'A1', 'A2'); L05.html line 63 ('trade date')", "PASS",
    "L04 line 51 names Lesson 4, Definition 2.1 in the same paragraph, where 'crossed' is defined; A2 is glossed as 'no withdrawals' and numbered at line 92. L05 line 63 defines the trade date in the sentence that uses its offsets, and the paragraph is one definition. No term is used before a definition in a way that prevents reading.")
row("FC1-b-r2-cross-reference-style", "2.9 cross-reference style (self-reference to own lesson)",
    "L04.html lines 51, 59-61; L05.html line 66", "PASS",
    "Style only, no truth effect: L04 cites its own definitions as 'Lesson 4, Definition 2.1' and 'Lesson 4, Remark 1.2' inside Lesson 4, while L05 writes 'Lesson L04' (line 66). Not a verifier FAIL; noted for the builder.")

rows = R
fragment = {
    "unit": "FC1",
    "slice": "FC1-b",
    "round": 2,
    "verifier": "Claude Haiku 5.5, independent verifier for FC1-b round 2 (did not build FC1; read verifier-rules.md, VERIFIER_RULES.md, BUILDER_RULES.md, plans/FC1-build-plan.md, round-1 fragment)",
    "pin": "9294b914a51647c66d2dee62c4a112c76ba04900",
    "base": "aeb512b65b7774b59b84f836a13984fcfe9d0d1f (round-1 pin, fragment /Users/billyribeiro/.fanout/frags/S-FC1-b.round1.json)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyS2-FC1-b",
    "scratch": "ledgers/FC1/scripts/FC1-b-r2/",
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "verdict": "PASS" if all(r["status"] == "PASS" for r in rows) else "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [
        "harris2002trading: curriculum string 'Harris, Trading and Exchanges (2003)' (curriculum yaml line 385) vs registry year 2002 (notes.year). Both pages print the registry year only, as the architect decision requires; no registry edit requested by this slice.",
        "references/references.json has no settlement-cycle source (scan in ledgers/FC1/scripts/FC1-b-r2/v2_registry_settlement_scan.out). L05 states no settlement period; the lesson should not say the course lacks an admitted source (see FC1-b-r1-prose-process-words).",
    ],
    "freshness_flags": [
        "harris2002trading record years [2002, 2023]; no L04 or L05 claim depends on an edition, so no update is needed here.",
    ],
    "notes": (
        "Round 2 for slice FC1-b at pin 9294b914 (delta from aeb512b: commits 56cc575a, 700bf33f, 9294b914). Changed subjects re-read in full: L04.html (every line), L05.html (every line), cards.json FC1-c060, c066, c135, c141 and new c154-c156, L05 cards and lab twins (twins and notation unchanged since aeb512b). All 41 round-1 row ids are kept and re-verified this round; no row is carried. Round-1 FAILs: prop22-empty-side and prop23-assumptions, card-c066 and references-L04-empty-list are now PASS; prose-process-words is FAIL again (the admission wording was missed in round 1). New FAILs: stop-arrival case in the Proposition 2.2 proof, order-entry offset in Definition 1.2, and the 'needs the empty start' overstatement. "
        "Interpreter: the twins run under the venv CPython 3.14.8 (CLAUDE.md pins 3.14); the first run under /usr/bin/python3 3.9 failed on itertools.pairwise, which is not a lab defect. "
        "Scope: slice b has no autograder, so the mutation rule (three new student-error mutants, ledger mutants list) does not apply; mutants is []. Lab sensitivity mutants (ledgers/FC1/scripts/FC1-b-r2/v2_l04_sensitivity.py) are demonstrations and are not listed. "
        "Not run or not checked: check_projects and run_graders (project files are outside slice b); the hub, L01-L03 and the project page (other slices); repo-wide ruff, mypy and pytest (only the twins and the FC1 lab tests were run, as scoped); build_site --check; a visual screenshot of the References list (the mechanism was read in refs.js and the page passed page_smoke). "
        "Note on the old ledgers/FC1/FC1-b.json: it was a round-7 fragment; it is overwritten by this round-2 fragment as instructed. Pre-existing ledgers/FC1/scripts/FC1-b-r2/r2_checks.py was not modified. "
        "Style notes (not rows that fail): L04 cites its own lesson as 'Lesson 4' while L05 writes 'Lesson L04' (cross-reference style); card c135 and c156 overlap in content (judged distinct)."
    ),
    "summary": "",
}
counts = {s: sum(1 for r in rows if r["status"] == s) for s in ("PASS", "FAIL", "UNVERIFIABLE")}
fragment["summary"] = (
    f"Slice FC1-b (L04, L05, both lab twins, and their 57 cards) at 9294b914, round 2: {counts['PASS']} PASS, {counts['FAIL']} FAIL, "
    f"{counts['UNVERIFIABLE']} UNVERIFIABLE of {len(rows)} rows; mutants 0/0. All gates re-run and green (check_pages, check_dag, run_labs, twins alone, page_smoke, ruff, mypy, lab pytest, verify_refs offline and live FC1). "
    "Four FAILs: (1) process/admission wording in learner text (L05 lines 397, 513, 630; c090); (2) Proposition 2.2 proof omits an arriving non-activating stop (L04 line 104); (3) Definition 1.2 assumes order entry at offset 0 without naming it (L05 line 63, quiz L05q1); (4) 'Proposition 2.2 needs the empty start' overstates (L04 line 367)."
)
out = ROOT / "ledgers/FC1/FC1-b.json"
out.write_text(json.dumps(fragment, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("wrote", out, "rows", len(rows), counts, "verdict", fragment["verdict"])
