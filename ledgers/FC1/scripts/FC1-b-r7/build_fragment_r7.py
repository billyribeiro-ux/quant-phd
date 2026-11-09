import json
import sys

sys.path.insert(0, "/Users/billyribeiro/.fanout/wt/verifyS7-FC1-b/tools")
import ledger  # noqa: E402

OUT = "/Users/billyribeiro/.fanout/wt/verifyS7-FC1-b/ledgers/FC1/scripts/FC1-b-r7/out/"
rows = []


def row(rid, check, location, status, evidence, fix=""):
    rows.append({"id": rid, "check": check, "location": location, "status": status, "evidence": evidence, "fix": fix})


def carry(text):
    return "Carried from round 6 (subject byte-identical since the previous pin e896b7a4): " + text


P = "PASS"
F = "FAIL"

# ---- gate rows, re-run at aa659725 (out/*.rc all 0) ----
row("FC1-b-r1-gate-check-pages", "tools/check_pages.py --unit FC1 --page L04; --page L05; --unit FC1",
    "course/modules/FC/FC1/L04.html, L05.html, cards.json", P,
    "Re-run at aa659725: out/check_pages_L04.out 'check_pages FC1 L04: PASS', check_pages_L05.out 'check_pages FC1 L05: PASS', check_pages_unit.out 'check_pages FC1: PASS' (rc 0 each).")
row("FC1-b-r1-gate-check-dag", "tools/check_dag.py --unit FC1",
    "L04.html line 37; L05.html lines 38-39, 58, 63", P,
    "Re-run at aa659725: out/check_dag_FC1.out 'check_dag FC1: PASS' (rc 0). L04 line 37 links L03#def-bid-ask-spread; L05 lines 38-39 link L04#def-order-types, L04#def-limit-order-book, L01#def-financial-intermediary; def-clearing-and-settlement (line 58) and def-trade-lifecycle (line 63) are defined on the page.")
row("FC1-b-r1-gate-run-labs", "tools/run_labs.py --unit FC1 --page L04 / --page L05 / --unit FC1",
    "tests/labs/FC1/lab-FC1-L04-1.py, lab-FC1-L05-1.py", P,
    "Re-run at aa659725: out/run_labs_L04.out 'run_labs FC1: PASS (1/1)', run_labs_L05.out 'PASS (1/1)', run_labs_unit.out 'PASS (8/8)'; rc 0 each.")
row("FC1-b-r1-gate-twin-alone", "twin run alone: python3 -I -W error, cwd /tmp",
    "tests/labs/FC1/lab-FC1-L04-1.py, lab-FC1-L05-1.py", P,
    "out/twin_L04.err and twin_L05.err are 0 bytes; both runs rc 0 (out/twin_L04.out, twin_L05.out).")
row("FC1-b-r1-gate-page-code-equals-twin", "page data-run code (html-unescaped) equals twin, trailing newlines aside",
    "L04.html lines 127-335; L05.html lines 110-364", P,
    "Inline Python re-extraction at aa659725 (html.unescape of the data-run block, compared with the twin file): L04 page code == twin: True; L05 page code == twin: True.")
row("FC1-b-r1-gate-expected-equals-output", "expected block equals the twin's stdout",
    "L04.html lines 336-357; L05.html lines 366-389", P,
    "Re-extraction at aa659725: L04 expected == twin stdout: True (22 lines); L05 expected == twin stdout: True (24 lines).")
row("FC1-b-r1-gate-page-smoke", "tools/page_smoke.py --unit FC1 --pages L04 L05",
    "L04.html, L05.html", P,
    "Re-run at aa659725: out/page_smoke_L04_L05.out 'page_smoke modules/FC/FC1/L04.html: PASS', 'page_smoke modules/FC/FC1/L05.html: PASS', 'page_smoke FC1: PASS'; rc 0.")
row("FC1-b-r1-gate-ruff", "ruff check and ruff format --check on both twins",
    "tests/labs/FC1/lab-FC1-L04-1.py, lab-FC1-L05-1.py", P,
    "out/ruff_check_twins.out 'All checks passed!' (rc 0); out/ruff_format_twins.out '2 files already formatted' (rc 0). Twins unchanged since e896b7a4 (git diff empty).")
row("FC1-b-r1-gate-mypy", "mypy --no-incremental on both twins",
    "tests/labs/FC1/lab-FC1-L04-1.py, lab-FC1-L05-1.py", P,
    "out/mypy_twins.out 'Success: no issues found in 2 source files' (rc 0).")
row("FC1-b-r1-gate-pytest-labs", "pytest -q tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py tests/test_curriculum.py",
    "tests/test_labs.py, tests/test_run_labs.py, tests/test_page_checks.py, tests/test_curriculum.py", P,
    "out/pytest_labs.out: progress dots only, 100%, no failure lines; rc 0.")
row("FC1-b-r3-gate-build-site-check", "tools/build_site.py --check",
    "course/assets/data, course/index.html, course/concepts.html", P,
    "out/build_site_check.out 'site data current: 6 outputs' (rc 0).")
row("FC1-b-r1-gate-verify-refs-offline", "tools/verify_refs.py --offline",
    "references/references.json", P,
    "out/verify_refs_offline.out 'offline integrity: 560 entries, 0 problems' (rc 0).")
row("FC1-b-r2-gate-verify-refs-live-unit", "tools/verify_refs.py --unit FC1 (live)",
    "references/references.json: harris2002trading", P,
    "out/verify_refs_unit_live.out 'live re-verification of FC1: 2 of 560 entries, 0 problems' (rc 0).")
row("FC1-b-r4-gate-check-projects-unit", "tools/check_projects.py --unit FC1",
    "course/modules/FC/FC1/project.html (unit gate)", P,
    "Re-run at aa659725: out/check_projects_FC1.out 'check_projects FC1: PASS' (rc 0). project.html and grader/test_project.py changed in this delta; the gate passes, and their content is outside this slice.")
row("FC1-b-r7-gate-fetch-data-check", "tools/fetch_data.py --check (offline)",
    "course/assets/data/market/ (unit gate, CLAUDE.md gates list)", P,
    "out/fetch_data_check.out 'fetch_data: 3 datasets, 0 problems' (rc 0).")

# ---- numbers and prose (cited lines unchanged since e896b7a4 except L04 line 51, which no row cites) ----
row("FC1-b-r1-num-L04-prose", "every number in L04 prose re-derived",
    "L04.html lines 72, 77, 126, 377-385, 398-414, 423-439, 450-464, 475-489, 501-505, 536, 541, 563-565, 574", P,
    carry("L04.html cited lines unchanged. Re-derived this round with out/numbers_r7.out: 60*1000+90*1100=159000, 159000/150=1060, 100-90=10, 24+18=42, 5600/173, 2*60=120, 250=0+2*100+50, 99300/100=993 (ledgers/FC1/scripts/FC1-b-r7/numbers_r7.py)."))
row("FC1-b-r1-num-L04-lab-output", "L04 expected output, interpretation and key result agree with the twin",
    "L04.html lines 336-357 (expected), 358 (interpretation), 505 (key result)", P,
    carry("L04.html cited lines unchanged. Twin re-run (out/twin_L04.out) equals the expected block; 300 events, 0 crossed, 0 conservation failures, 173 trades, 5600 shares traded, 24 activated, 18 pending."))
row("FC1-b-r1-num-L05-prose", "every number in L05 prose re-derived",
    "L05.html lines 75, 109, 390, 438, 445, 452, 488, 495, 502, 544, 582, 605-607, 637", P,
    carry("L05.html cited lines unchanged. Re-derived this round (out/numbers_r7.out): 216*10060=2172960; NP/G=0.20881062, 0.20881 to five decimals, 0.209 half-up; 11060360/68398886=16.17%, /14282414=77.44%; negatives 7411991+6656379+214044=14282414=positives 3222054+11060360; 2026-10-28 Wed, +2 business days = Fri 2026-10-30, +3 = Mon 2026-11-02."))
row("FC1-b-r1-num-L05-lab-output", "L05 expected output, interpretation and key result agree with the twin",
    "L05.html lines 109 (hypothesis), 366-389 (expected), 390 (interpretation)", P,
    carry("L05.html cited lines unchanged. Twin re-run (out/twin_L05.out) equals the expected block (24 lines); 'net_to_gross_ratio 0.209', 'offsets_nondecreasing True', 'net_payers 3' printed."))
row("FC1-b-r1-lab05-parameter-claims", "L05 claims about CLEARING_OFFSET and SETTLEMENT_LAG vs the code",
    "L05.html line 66, line 390, lines 500-502 (E3); card FC1-c142", P,
    "Variants run from the twin (out/variants, numbers in ledgers/FC1/scripts/FC1-b-r7/variants/): SETTLEMENT_LAG=3 changes only the header line, the settlement and the position_update lines, and offsets_nondecreasing stays True; CLEARING_OFFSET=3 changes the header and the clearing line, and offsets_nondecreasing prints False. This matches L05 line 390 and E3 (lines 500-502) and card FC1-c142.")
row("FC1-b-r1-lab04-invariant-claim", "L04 claims that Lab 1 checks both invariants after each of 300 events",
    "L04.html lines 51, 126, 358, 505; L04.html code lines 293-332 (main())", P,
    "Line 51 (changed this delta, re-read): 'Lab 1 checks both invariants after each of 300 simulated events'. The page code main() (L04.html lines 293-332) loops over EVENTS=300 and counts crossed (bid >= ask) and conservation failures at every event (lines 302-314); out/twin_L04.out prints both counts as 0.")
row("FC1-b-r1-math-L04-examples-problems", "Examples 1.3, 1.4 and problems M1-M3, P2, R1-R3 re-derived",
    "L04.html lines 72, 77, 377-385, 398-491", P,
    carry("L04.html cited lines unchanged. Re-derived this round: Example 1.3 fills 60@1000 and 90@1100, cost 159000, average 1060, 10 left; Example 1.4 stop at 990 fills at 985; M1 fills 60@995 and 40@990, cost 99300, average 993, the 990 bid keeps 60; M2 fills 30@1000 and 20@1001, leaves 10@1001 and 40@1003; P2 250=0+200+50; R3 2*60=120; R1 cascade fills (990,100),(985,100),(980,100) by the rule of Remark 1.2."))
row("FC1-b-r1-math-L05-prop21-prop22", "Propositions 2.1, 2.2, Remark 2.3, P2, R2 agree with their statements",
    "L05.html lines 75-96, 100, 468-470, 518-520", P,
    "Line 100 (changed this delta, re-read): 'assuming A1 and A2, Proposition 2.2 gives the CCP's net cash in the model as zero', matching Proposition 2.2 (line 90: 'Assuming A1 and A2'). Proof of 2.1(ii) (line 85) uses A1 for non-negativity. P2 bound re-derived: each term lies in [-c, 0] and [0, c]. R2 re-derived: NP=100, G=-100, 100 <= -100 false.")
row("FC1-b-r1-math-L04-prop22-empty-side", "Proposition 2.2 empty-side convention and its use in the proof",
    "L04.html lines 99, 104, 425", P,
    carry("L04.html cited lines unchanged. Line 99 says 'Assuming A1 and the rules of Section 1'; the proof convention (beta = -inf, alpha = +inf) is stated at line 104 and used at line 425."))
row("FC1-b-r1-math-L04-prop23-assumptions", "Proposition 2.3 hypotheses and the card that states them",
    "L04.html lines 93-95, 107-117; card FC1-c066", P,
    carry("L04.html lines 93-95 (A2) and 107-117 unchanged; card FC1-c066 unchanged (cards.json line 432-433 region)."))
row("FC1-b-r1-math-L04-remark-definitions", "Remark 1.2 and Definition 2.1 agree with the matching code",
    "L04.html lines 56-67, 84-89, 197-220 (match), 222-246 (activate), 302-313 (main loop)", P,
    carry("L04.html cited lines unchanged. L04.html code lines 197-220 (match), 222-246 (activate) and 302-313 (main loop) implement the fill price rule, price-time priority and the repeated stop check of Remark 1.2 and Definition 2.1."))
row("FC1-b-r3-proof-P1-hypothesis", "Problem P1 hypothesis and its solution",
    "L04.html line 423 (statement), line 425 (solution)", P,
    carry("L04.html lines 423 and 425 unchanged; the solution uses the empty-side convention of Proposition 2.2."))
row("FC1-b-r4-key-result-NP-hypothesis", "L05 key result on net payments carries its hypothesis",
    "L05.html line 540 (key-results row); Proposition 2.1 line 79; Problem R2 lines 518-520; card FC1-c101", P,
    carry("L05.html line 540 says 'Assuming A1, in a batch, net payments lie between zero and gross payments', matching Proposition 2.1(ii) at line 79; card FC1-c101 unchanged."))
row("FC1-b-r4-key-result-L04-503-hypothesis", "L04 key result on the book carries A1",
    "L04.html line 503 (key-results row); Prop 2.2 line 99", P,
    carry("L04.html line 503 'Assuming A1, the book is never crossed after any event' matches Proposition 2.2 line 99."))
row("FC1-b-r4-key-result-L05-541-hypothesis", "L05 key result on the CCP carries A1 and A2",
    "L05.html line 541; Prop 2.2 line 90", P,
    carry("L05.html line 541 'Assuming A1 and A2, the CCP's net cash ... is zero' matches Proposition 2.2 line 90."))
row("FC1-b-r4-P1-empty-side-convention", "P1 solution uses the stated convention",
    "L04.html line 425", P,
    carry("L04.html line 425 unchanged; it takes beta = -inf or alpha = +inf as in the proof of Proposition 2.2."))
row("FC1-b-r1-grades", "grades of claims and cards",
    "L04.html lines 98, 108, 501-505; L05.html lines 78, 89, 539-544, 403; cards.json", P,
    "Re-read this round: L04 key results T/C as stated; L05 key results T/C as stated. Changed cards graded T (FC1-c089, FC1-c100, FC1-c173) or C with a lab basis (FC1-c125, FC1-c174) are consistent with their proofs and printed output.")
row("FC1-b-r1-notation", "symbols against notation/notation.json and within the lessons",
    "L04.html and L05.html inline math (95 and 120 expressions)", P,
    "Re-counted: L04 has 94 inline \\( \\) plus 1 display expression (95); L05 has 120 inline (120), unchanged from e896b7a4 (git show counts). Symbols in the changed card FC1-c089 (NP, G, Pay_j) are defined at L05.html line 75 (NP, G, Pay_j), not reused. notation/notation.json has no entry for NP or Pay; the symbols are lesson-local.")
row("FC1-b-r1-prose-process-words", "no process words in learner text",
    "L04.html, L05.html, cards.json", P,
    "Re-scanned the three full files at aa659725 for round, verif, builder, reviewer, fixed, ruling, audit, delta: only ordinary uses ('fixed seed', 'fixed demand', 'fixed by reference'). Added lines (out/added_lines_r7.txt) contain none.")
row("FC1-b-r1-prose-banned-phrases", "BUILDER_RULES 1.3-1.4 banned strings and phrases",
    "L04.html, L05.html, cards.json", P,
    "Grep at aa659725 for TODO, TBD, lorem, for brevity, details omitted, beyond the scope, left as an exercise, you can add more, it is important to note, studies show, experts agree, it is well known, obviously, clearly, can be shown, ellipsis: only tuple[str, ...] in the L05 twin code (L05.html line 139), a Python type annotation, not prose.")
row("FC1-b-r1-structure-L04", "L04 template sections in order",
    "L04.html", P,
    "Section order unchanged (why-it-matters, 1 Order types, 2 Limit order book, lab, 3 canon-breaks, 4 misconceptions, 5 problem set, 6 key results, 7 quiz, 8 references). The only changed line in the file is line 51 (text only).")
row("FC1-b-r1-structure-L05", "L05 template sections in order",
    "L05.html", P,
    "Section order unchanged (why-it-matters, 1, 2, 3 with lab, 4 canon-breaks, 5 misconceptions, 6 problem set, 7 key results, 8 quiz, 9 references). The only changed line in the file is line 100 (text only).")
row("FC1-b-r1-scope-words", "scope words (only, all, always, every, any, same, drives, exactly) are supported",
    "L04.html lines 51, 67, 126, 358, 364, 475, 505; L05.html lines 63, 70, 100, 390, 399, 401", P,
    "Line 51 'never crossed' is Proposition 2.2 under A1 (line 99). Line 100 'in the model' qualifies the zero. Other scope words were checked in round 6 and their cited lines are unchanged.")
row("FC1-b-r1-attribution-harris", "Harris attribution and locator",
    "L04.html line 590; L05.html line 403; references/references.json key harris2002trading; curriculum/02-economics-finance-core.yaml line 385", P,
    carry("L04.html line 590, L05.html line 403 unchanged; curriculum yaml unchanged (git diff empty). The yaml line 385 reads 'Harris, Trading and Exchanges (2003)' and the registry gives 2002; pages cite the key only, see registry_flags."))
row("FC1-b-r1-settlement-source-absence", "no settlement period is stated for any market without a source",
    "L05.html lines 52, 105, 397, 513, 632; card FC1-c090; references/references.json", P,
    carry("L05.html cited lines unchanged; line 397 'This lesson states no settlement period for any market, because it cites no source for one' matches card FC1-c090."))
row("FC1-b-r1-references-L05", "L05 references block and citation JS",
    "L05.html line 403 and line 644; course/assets/js/refs.js lines 68-90", P,
    carry("L05.html lines 403 and 644 unchanged; refs.js unchanged (git diff empty)."))
row("FC1-b-r1-references-L04-empty-list", "L04 references block with empty list and refs.js",
    "L04.html lines 588-592; course/assets/js/refs.js", P,
    carry("L04.html lines 588-592 unchanged; refs.js unchanged."))
row("FC1-b-r1-cards-L04", "L04 cards match the current L04 text",
    "course/modules/FC/FC1/cards.json (lesson L04: c056-c072, c099, c100, c119, c121, c132, c133, c135, c141, c143, c154-c156, c169, c171, c173)", P,
    "All L04 cards read this round. Changed cards checked against the current L04 text: FC1-c067 (Remark 2.4; Problem R3), FC1-c100 (Proposition 2.3 under A2), FC1-c173 (Problem R3, 2*60=120). Others unchanged and consistent.")
row("FC1-b-r1-cards-L05", "L05 cards match the current L05 text and carry the hypotheses",
    "course/modules/FC/FC1/cards.json (lesson L05: c073-c090, c101, c102, c109, c114, c118, c123, c124, c142, c144, c145, c164-c168, c172)", P,
    "All L05 cards read this round. FC1-c089 now answers 'Not necessarily' with the R2 counterexample (cards.json line 589), matching L05 R2 (lines 518-520) and the proof step at line 85. Each card number appears in L05 (e.g., 2172960 at line 373 and 577; 14282414 and 68398886 at lines 381, 390). Duplicate question addressed in FC1-b-r1-cards-duplicates.")
row("FC1-b-r1-cards-duplicates", "no duplicate cards",
    "course/modules/FC/FC1/cards.json (ids 172 unique; fronts unique; c174 at line 1118-1123 against c103 at lines 659-663)", F,
    "FC1-c174 ('Does the cumulative identity hold in Lab 1, Part B?' -> 'True. Cumulative reserves plus cumulative loans equal total deposits (Lab 1, Part B; Proposition 2.2).') restates FC1-c103 ('Under Assumption 2.0, do cumulative reserves plus cumulative loans equal total deposits after stages 0 to n?' -> 'Yes ... equals S_n (Proposition 2.2)'). The same proposition and the same answer appear twice, once graded T and once C. Judgement note: FC1-c125 (stage check, C) and FC1-c006 (stage balance, T) follow the same pattern and predate this delta; they are recorded in notes, not as a separate FAIL.",
    "Delete FC1-c174 from course/modules/FC/FC1/cards.json (c103 already carries the cumulative identity at grade T). If the lab basis is wanted, add '(Lab 1, Part B prints True)' to FC1-c103's back and keep one card.")
row("FC1-b-r1-card-c066", "card FC1-c066 matches Proposition 2.3 and its hypothesis",
    "cards.json FC1-c066 (line 432-433); L04.html lines 92-95, 108-111", P,
    carry("cards.json lines 430-435 unchanged; L04.html lines 92-95 (A2) and 108-111 (Proposition 2.3) unchanged."))
row("FC1-b-r4-card-c099-changed-text", "card FC1-c099 matches the current L04 Proposition 2.2 text",
    "cards.json FC1-c099 (line 697-702); L04.html line 99", P,
    carry("cards.json lines 697-702 and L04.html line 99 unchanged."))
row("FC1-b-r2-cards-c154-c156", "cards FC1-c154 to FC1-c156 match Remark 1.2 and A2",
    "cards.json (c154-c156); L04.html lines 67, 94", P,
    carry("cards.json c154-c156 unchanged (lines 997-1014); L04.html lines 67 and 94 unchanged."))
row("FC1-b-r1-labs-runtime-seed-network", "twins: seed, runtime, no network",
    "tests/labs/FC1/lab-FC1-L04-1.py, lab-FC1-L05-1.py", P,
    "Twins unchanged since e896b7a4 (git diff empty). Imports are standard library only (random, collections, dataclasses, datetime, itertools, collections.abc); seeds SEED=2026; the twin runs under -I -W error with no output on stderr.")
row("FC1-b-r1-lab-prose-consistency", "lab prose agrees with the printed output",
    "L04.html lines 126, 358; L05.html lines 109, 390", P,
    carry("L04.html lines 126 and 358 and L05.html lines 109 and 390 unchanged; each agrees with out/twin_L04.out and out/twin_L05.out."))
row("FC1-b-r1-misconceptions-canon", "misconception and canon-break sections against the lessons' results",
    "L04.html lines 364-368, 375-386; L05.html lines 397-401, 409-425", P,
    carry("L04.html and L05.html cited lines unchanged; figures in them re-derived above (99300/993; 14282414 vs 68398886; 10117 vs 10060)."))
row("FC1-b-r1-inline-style", "inline style attributes",
    "L04.html lines 517, 526, 545, 555, 569, 578", P,
    carry("cited lines unchanged; the cited elements are fieldsets with an inline min-inline-size style, which is presentational and not a rule breach."))
row("FC1-b-r2-math-L04-prop22-stop-arrival", "Proposition 2.2 stop-arrival case",
    "L04.html lines 99, 104", P,
    carry("L04.html lines 99 and 104 unchanged; the proof covers a stop arrival as a market buy (line 104)."))
row("FC1-b-r2-def12-order-entry-offset", "order entry offset 0 and the quiz explanation",
    "L05.html line 63; quiz explanation line 562; twin lines 205-217", P,
    carry("L05.html line 63 and 562 unchanged; the twin (lines 205-217) sets order entry, matching and trade capture to offset 0."))
row("FC1-b-r2-canon-needs-empty-start", "canon-break states the empty start is needed",
    "L04.html line 367; R2 lines 479-483", P,
    carry("L04.html line 367 and R2 lines 479-483 unchanged."))
row("FC1-b-r2-A2-consistency", "A2 is stated the same way wherever it is used",
    "L04.html lines 51, 92-95, 109, 116, 126, 358, 365, 504-505; L05.html line 90", P,
    "Line 51 (changed) says 'Assuming A2, no withdrawals, the entered shares equal ...', which matches A2 (lines 92-95) and Proposition 2.3 (line 109). Other cited lines unchanged.")
row("FC1-b-r2-terms-before-definition", "terms used before definition",
    "L04.html lines 51, 60-61; L05.html lines 52, 58, 63, 66", P,
    "Line 51 (changed) uses 'crossed', 'best bid' and 'best ask' before Definition 2.1 (line 84); it glosses them in the same sentence ('meaning its best bid is below its best ask'), so the term is explained where it first appears. L05 lines 52, 58, 63, 66 unchanged.")
row("FC1-b-r2-cross-reference-style", "cross-reference style and link targets",
    "L04.html lines 37, 51, 59-61; L05.html lines 38-39, 52, 66, 400", P,
    "Line 51 (changed) cites Proposition 2.2 and Proposition 2.3 with their assumptions; the form matches the other cross-references. Other cited links unchanged; check_dag PASS.")
row("FC1-b-r4-L05-why-market-claim", "L05 why-it-matters claim",
    "L05.html line 52", P,
    carry("L05.html line 52 unchanged."))
row("FC1-b-r4-L04-why-it-matters", "L04 why-it-matters: definition of the uncrossed book",
    "L04.html line 51", P,
    "Line 51 now reads 'The book is never crossed, meaning its best bid is below its best ask'. Definition 2.1 (line 84) says the book is crossed when the best bid is at least the best ask, so 'never crossed' is 'best bid below best ask', which matches Proposition 2.2 (line 99). The round-6 inverted wording is gone.")
row("FC1-b-r4-hours", "hours arithmetic and hub figures",
    "course/modules/FC/FC1/index.html line 29; L04.html lines 2 and 34; L05.html lines 2 and 35", P,
    carry("index.html line 29 and the data-hours and eyebrow lines (L04 lines 2, 34; L05 lines 2, 35) unchanged; check_pages PASS."))
row("FC1-b-r3-lesson-links", "lesson navigation links",
    "L04.html lines 596-597; L05.html lines 649-650", P,
    carry("L04.html lines 596-597 and L05.html lines 649-650 unchanged; check_pages PASS."))
row("FC1-b-r5-delta-L05-hunks", "every hunk of L05.html in the delta",
    "L05.html hunks at lines 52, 79, 90, 100, 540, 541 (delta e896b7a4..aa659725: one hunk, line 100)", P,
    "git diff e896b7a4 aa659725 -- L05.html: one hunk, line 100 (Remark 2.3 'assuming A1 and A2, Proposition 2.2 ...'). Re-read and verified against Proposition 2.2 (line 90). Lines 52, 79, 90, 540, 541 are unchanged in this delta.")
row("FC1-b-r5-delta-L04-hunks", "every hunk of L04.html in the delta",
    "L04.html hunks at lines 51, 99, 503, 551, 590", P,
    "git diff e896b7a4 aa659725 -- L04.html: one hunk, line 51 (why-it-matters), verified above. Lines 99, 503, 551 and 590 are unchanged in this delta and consistent with Proposition 2.2, the key result, the quiz explanation and the references block.")
row("FC1-b-r5-delta-cards-hunks", "cards changed in the delta (c050, c061, c075, c082, c090, c171, c172 in the round-5 delta)",
    "course/modules/FC/FC1/cards.json: c050 (line 324, L03), c061 (398), c075 (488), c082 (532), c090 (593), c171 (1096), c172 (1103)", P,
    carry("the e896b7a4..aa659725 diff hunks for cards.json are at lines 437, 586, 704, 822 and 1106 only; the cards in this row are not in them. Their content was re-read in the full scan."))
row("FC1-b-r5-quiz-L04-L05", "quiz items match the lessons",
    "L04.html lines 511-586 (9 items); L05.html lines 550-640 (11 items)", P,
    carry("quiz regions unchanged in the delta (no hunks at L04 511-586 or L05 550-640); answers re-checked above (1060, 10, 42, 120, 2172960, 30, 3, 0.2088, 1009000)."))
row("FC1-b-r5-lab05-printed-checks", "L05 prose lists the printed checks correctly",
    "tests/labs/FC1/lab-FC1-L05-1.py (print calls at twin lines 202-203 and 240); L05.html line 572", P,
    "Twin re-run at aa659725 (out/twin_L05.out) prints the checks listed on L05 line 572; the twin is unchanged.")
row("FC1-b-r5-cards-full-scan", "every card read; L04 and L05 cards read in full",
    "course/modules/FC/FC1/cards.json (all 172 cards read this round; 1125 lines)", P,
    "All 172 cards were read this round (ids unique, 172). Defects found by the scan are recorded in FC1-b-r1-cards-duplicates (FC1-c174) and in FC1-b-r7-delta-cards-c174. No other card defect found.")
row("FC1-b-r6-card-c089-negative-consideration", "card FC1-c089 answers the negative-consideration question correctly",
    "course/modules/FC/FC1/cards.json line 589 (FC1-c089)", P,
    "Line 589 now reads 'Not necessarily. The bound can fail: with one trade of consideration -100 cents, net payments are 100 cents and gross payments are -100 cents, so the bound 100 <= -100 is false (Problem R2). The step Pay_j >= 0 ... needs non-negative considerations, so the bound is not guaranteed.' Verified against L05 R2 (lines 518-520) and the proof step at line 85. Round-6 over-general 'No' is fixed.")

# ---- rows new in round 7 ----
row("FC1-b-r7-delta-L04-line51", "delta hunk L04.html line 51 (why-it-matters)",
    "course/modules/FC/FC1/L04.html line 51", P,
    "Hunk: 'its best bid is at least its best ask' changed to 'its best bid is below its best ask'. Matches Definition 2.1 (line 84) and Proposition 2.2 (line 99).")
row("FC1-b-r7-delta-L05-line100", "delta hunk L05.html line 100 (Remark 2.3)",
    "course/modules/FC/FC1/L05.html line 100", P,
    "Hunk: 'Proposition 2.2 gives' changed to 'assuming A1 and A2, Proposition 2.2 gives'. Matches Proposition 2.2 (line 90: 'Assuming A1 and A2'). The Proposition 2.1 identity and bound (lines 79, 85) are unchanged.")
row("FC1-b-r7-delta-cards-c067-c100", "delta hunks FC1-c067 and FC1-c100 (cards.json lines 437-440, 704-707)",
    "course/modules/FC/FC1/cards.json lines 437-440, 704-707", P,
    "c067: the single-fill example moved to c173; the remaining back cites Remark 2.4 and Problem R3, both present (L04 lines 120-122, 489). c100: 'Under A2' added; Proposition 2.3 (line 109) assumes A2.")
row("FC1-b-r7-delta-cards-c089", "delta hunk FC1-c089 (cards.json lines 586-590)",
    "course/modules/FC/FC1/cards.json lines 586-591", P,
    "Hunk replaces the over-general 'No' with 'Not necessarily' and the R2 counterexample. Verified in FC1-b-r6-card-c089-negative-consideration.")
row("FC1-b-r7-delta-cards-c125-c173", "delta hunks FC1-c125 (lab check, C) and FC1-c173 (single fill, T) (cards.json lines 822-829, 1111-1116)",
    "course/modules/FC/FC1/cards.json lines 822-829, 1111-1116", P,
    "c125 'Does each stage of Lab 1, Part B balance? True.' matches out of the L01 twin run (ledgers/FC1/scripts/FC1-b-r7/out/twin_L01.out 'each stage balances: True'); Proposition 2.2 of L01 (L01.html line 89) is the balance-sheet proposition. c173: 2 x 60 = 120, Problem R3 (L04 line 489) gives the 120 as the buyer's and seller's parts.")
row("FC1-b-r7-delta-cards-c174", "delta card FC1-c174 (cards.json lines 1117-1123)",
    "course/modules/FC/FC1/cards.json lines 1117-1123 against FC1-c103 (lines 659-663)", F,
    "FC1-c174 restates FC1-c103 (same question, same answer, same proposition). Its grade C with a lab basis does not add a distinct fact; the lab's printed line 'cumulative reserves plus cumulative loans equal total deposits: True' is already covered by the L01 twin output and by c103 at T.",
    "Delete FC1-c174 (cards.json lines 1117-1123). FC1-c103 carries the cumulative identity. If the lab line is to be cited, add it to FC1-c103's back as a second basis.")
row("FC1-b-r7-twins-unchanged", "tests/labs/FC1 has no delta",
    "tests/labs/FC1/*.py", P,
    "git diff --stat e896b7a4 aa659725 -- tests/labs/FC1 is empty. The twins were re-run (out/twin_L04.out, twin_L05.out, twin_L01.out) and the variants in ledgers/FC1/scripts/FC1-b-r7/variants/.")

frag = {
    "unit": "FC1",
    "slice": "FC1-b",
    "round": 7,
    "verifier": "Claude Haiku 5.5, independent verifier for FC1-b round 7 (did not build FC1; read verifier-rules.md, CLAUDE.md, BUILDER_RULES.md; round-6 fragment as context only)",
    "pin": "aa6597255304919b9c4e5e5ca07763ae3e13d45c",
    "base": "e896b7a45344d1bc17ebfbf7fb05d87698ec9d6a (round-6 pin; round-6 fragment /Users/billyribeiro/.fanout/frags/S-FC1-b.round6.json)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyS7-FC1-b",
    "scratch": "ledgers/FC1/scripts/FC1-b-r7/",
    "verified_at": "2026-11-09T12:30:00+00:00",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [
        "harris2002trading: curriculum/02-economics-finance-core.yaml line 385 reads 'Harris, Trading and Exchanges (2003)'; the registry record (Crossref) reads 2002. Pages cite the key with the registry's own fields only. The curriculum string should be corrected by its owner; no registry edit is requested."
    ],
    "freshness_flags": [],
    "notes": [
        "Delta since round 6 (e896b7a4..aa659725) in the slice: L04.html line 51 (text), L05.html line 100 (text), cards.json hunks at lines 437 (c067), 586 (c089), 704 (c100), 822 (c125), 1106 (c173 and c174 added). tests/labs/FC1 and curriculum/notation/references have no diff. Every line number in the slice is unchanged except after cards.json line 1106.",
        "Out of slice and not verified here: course/modules/FC/FC1/project.html and course/modules/FC/FC1/grader/test_project.py changed in this delta (two new accepted-input tests, 10**18 bps coupon and 10**18 cents price; project.html counts 99 -> 101). The unit gates check_projects and page_smoke for the project pages are covered by the project slices.",
        "Round-6 non-PASS rows re-verified from scratch: FC1-b-r4-L04-why-it-matters (fixed, PASS), FC1-b-r5-delta-L04-hunks (PASS), FC1-b-r6-card-c089-negative-consideration (fixed, PASS), FC1-b-r1-cards-L05 (PASS), FC1-b-r5-cards-full-scan (PASS; all 172 cards read). New non-PASS: FC1-b-r1-cards-duplicates and FC1-b-r7-delta-cards-c174 (FC1-c174 restates FC1-c103).",
        "Carried rows: a row is carried only when its cited lines are byte-identical since e896b7a4 (single-line hunks keep line numbers). Gate rows were re-run at aa659725 and are not carried.",
        "Judgement note: FC1-c125 (lab stage check, C) and FC1-c006 (stage balance, T) overlap in content. They predate this delta and were accepted in earlier rounds, so they are not a separate FAIL. A later round may choose to merge them.",
        "Judgement note: FC1-c173 repeats the factor-of-two point of FC1-c067 with a number; the questions differ (why vs. how much) so they are not duplicates.",
        "Mutants: none. The slice is lessons and cards; mutation testing applies to project graders only (ruling: lab twins are demonstrations).",
        "Commands that were not run: pytest on the full suite (only the four FC1-related test files, per the round-6 row list); tools/mutate_graders.py and run_graders (project slices, not this slice).",
        "No git commit or push was made. The file ledgers/FC1/FC1-b.json in this checkout was an older fragment and is overwritten by this round-7 fragment, as the instruction requires.",
    ],
    "summary": "FC1-b round 7 at aa659725: %d rows, %d PASS, %d FAIL, 0 UNVERIFIABLE. Non-PASS: FC1-b-r1-cards-duplicates and FC1-b-r7-delta-cards-c174 (LOW): FC1-c174 restates FC1-c103 (Proposition 2.2 cumulative identity). Round-6 FAILs are fixed and re-verified: FC1-b-r4-L04-why-it-matters, FC1-b-r6-card-c089-negative-consideration, FC1-b-r1-cards-L05, FC1-b-r5-delta-L04-hunks." % (
        len(rows), sum(1 for r in rows if r["status"] == P), sum(1 for r in rows if r["status"] == F)),
}

problems = ledger.validate(frag, "FC1-b")
print("validate:", problems)
with open("/Users/billyribeiro/.fanout/wt/verifyS7-FC1-b/ledgers/FC1/FC1-b.json", "w", encoding="utf-8") as fh:
    json.dump(frag, fh, ensure_ascii=False, indent=1)
    fh.write("\n")
print("rows", len(rows), "pass", sum(1 for r in rows if r["status"] == P), "fail", sum(1 for r in rows if r["status"] == F))
ids = [r["id"] for r in rows]
print("dup ids", len(ids) - len(set(ids)))
