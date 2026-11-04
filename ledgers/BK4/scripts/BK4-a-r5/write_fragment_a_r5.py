"""Build the round-5 BK4-a fragment: carried round-4 rows (subject byte-identical), fresh round-5 rows, new defects."""
import json, sys
from pathlib import Path

ROOT = Path(sys.argv[1])
S = ROOT / "ledgers/BK4/scripts/BK4-a-r5"
prev = json.load(open("/Users/billyribeiro/.fanout/frags/E-BK4-a.round4.json"))
PREV_PIN = "9a02b1af"

FRESH_EV = {
"BK4a-hub-placement-arithmetic": "Round 5 re-read of index.html:71-131 (raw markup): data-mastery 0.8 (index.html:71); 8 items Pq1-Pq8; 0.8 x 8 = 6.4 so 7 correct needed; 6/8 = 75%, 7/8 = 87.5% (index.html:73). Keys re-read: Pq1 correct 100.00 (110/1.1 = 100, index.html:79); Pq2 data-answer 1.75 (1+1/2+1/4, index.html:84); Pq3 data-answer 6 (lim 2x at 3, index.html:89); Pq4 correct c (index.html:97); Pq5 correct C (index.html:107, P0.1 evidence grade, matches BLUEPRINT.md:161 grade C); Pq6 correct Clearing (index.html:116). Rung-1 item data-answer 20: min(120-100,50)=20 (index.html:121). Rung-2 item correct first surviving member (index.html:129). Changed lines 122 and 127 (prompt parentheticals) read: 'Lesson 3 defines the layers' / 'Lesson 3 defines the survivor shares'.",
"BK4a-hub-prereq-chain": "Round 5, from the registry-of-record YAML read this round: curriculum/02-economics-finance-core.yaml:1075 BK4 prereqs [FC1]; :367 FC1 prereqs [P0.1, E1]; :22 E1 prereqs [M2]; curriculum/01-foundations.yaml:126 M2 prereqs [M1]; :91 M1 prereqs [P0.1]. So FC1 -> E1 -> M2 -> M1 -> P0.1: 'FC1, which assumes P0.1 and E1, and through them M1' (index.html:35) is correct and 'BK4 also uses M2 directly' is a separate claim (see BK4a5-hub-prereq-uses). Re-verified after the changed hunk at index.html:35.",
"BK4a-hub-P0.1-link": "Round 5: index.html:35 'P0.1 is not yet released in this program'; 'ls course/modules/P' -> 'No such file or directory' (this round); course/modules/FC/FC1/index.html exists (FC1 is the built prerequisite).",
"BK4a-hub-settlement-framing": "Round-4 FAIL cleared. index.html:33 now reads 'In this unit's model, a trade settles when its payment has moved between accounts. The payment systems that move it are defined in Lesson 1, and the clearing houses of the model are central counterparties, defined in Lesson 2.' The qualifier is the model's rule; the lesson pointers match L01.html:59 (payment system, Definition 1.1) and L02.html:64 (central counterparty, Definition 1.2). Read this round: ledgers/BK4/scripts/BK4-a-r5/index.txt.",
"BK4a-hub-process-words": "Round 5: stripped visible text of index.html (ledgers/BK4/scripts/BK4-a-r5/index.txt) and of L01-L03 scanned by scan_words_a_r5.py for round, build, builder, verifier, REQUESTS, unit report: zero process-word hits (scan_words_a_r5.out).",
"BK4a-hub-data-status": "Round 5: index.html:37 'Data: none' and :184 'No data is used in BK4' read this round (index.txt). Twins: grep for open(, urllib, socket, requests, http in tests/labs/BK4/lab-BK4-L0{1,2,3}-1.py: 0 hits. page_smoke.out: no external requests for index, L01-L03. tools/data_sources.yaml unchanged in the delta (not in the round-5 diff list).",
"BK4a-L01-numbers": "Round 5 re-derivation (rederive_a_r5.py -> rederive_a_r5.out, stdlib, python3 -I): seeded day (seed 20260) by its own generator; RTGS need by binary search on feasibility: A 112500, B 1533900, C 0; net positions +379800, -1533900, +1154100 (sum 0); DNS debits 0, 1533900, 0; gross 2841600; 1533900/2841600 = 0.53980152 -> 0.5398 (E3, L01.html:409 and the interpretation at L01.html:286). Block equality: block_compare.out (expected block = run output, 32 lines).",
"BK4a-L01-problems-M-P-E-R": "Round 5 re-read of L01.html:335-430 (changed hunk at 370 read): M1 Need 200, Debit 200 (running sums 0,300,-200); M2 Need 200, Debit 100 (doubling); M3 Need 30, Debit 20 (sums 0,40,-30,-20); P1 uses A1 and the 'each payment has one sender and one receiver' clause (now stated, L01.html:370), correct; P2 iff by cases (checked); P3 scaling; E1 Bank B 1533900 both (Part B); E2 1 of 3, Bank A (Part C/B); E3 0.5398 rounded half up from 0.539801 (1533900/2841600 = 0.53980152, rederive_a_r5.out); R1 Remark 3.1 inflows-first attains Debit; R2 sum Debit = sum max(0,Net) <= gross; R3 cycle sums 0,-100,-100,0 -> Need 100, all debits 0.",
"BK4a-L01-notation": "Round 5: math_symbols_a_r5.py over 734 math spans of index, L01, L02, L03 (math_symbols_a_r5.out): no registered symbol used (T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q}); no \\mathbb{R}, \\mathbb{E}, \\mathbb{P} (the registered \\R, \\E macros are used where needed); no bare T in math. Local symbols (S_{i,k}, Net_i, Debit_i, n_i, A, G, Rec, Pay, IM, DF, K, D, Z, u, x_i, ell, S, L_s, M, c(M), t, k, p_i) are defined on first use in the lesson where they appear.",
"BK4a-L01-structure": "Round 5: check_pages_L01.out 'check_pages BK4 L01: PASS' (exit 0). Sections s1-s9 (L01.html:53-540); three misconceptions (L01.html:321-330); problem sets M1-M3, P1-P3, E1-E3, R1-R3 (L01.html:335-430); key results (440-456); quiz 10 items (458-537); references (539, 'cites no registry source'). Canon breaks section (307-313).",
"BK4a-L01-FC1-claim": "L01.html:55 (changed hunk; read this round): 'FC1 Lesson 5 followed one trade through that sequence.' FC1 L05 is 'Clearing, Settlement and the Trade Lifecycle' (course/modules/FC/FC1/L05.html:6, :36); its line 63 lists six states in order: order entry, matching, trade capture, clearing, settlement, position update. Claim holds.",
"BK4a-L01-canon-breaks-wording": "Round 5 re-read of L01.html:307-313 (bullets): 'The model has no queues ... The lesson states no finding about any such design'; 'The day is given ...'; 'The settlement cycle is a parameter ... the T+1 rule is named, not stated'; 'The lesson does not say which real system uses which design ... the two designs are defined in Definitions 1.1 and 2.1'. The heading at :308 ('Four places where the analyst must act') is a separate FAIL row (BK4a5-L01-canon-heading); the bullets themselves PASS.",
"BK4a-L02-lab-numbers": "Round 5: block_compare.out: L02 page expected block (L02.html:241-269) equals the run output of tests/labs/BK4/lab-BK4-L02-1.py under python3 -I -W error (29 lines, exit 0, stderr 0 bytes). Numbers re-derived (rederive_a_r5.out): G 7596300; Rec (314500, 2067800, 3340300, 1873700); Pay (3941500, 314500, 0, 3340300); n (-3627000, 1753300, 3340300, -1466600); A 5093600; reduction 2502700; floor(10000*2502700/7596300) = 3294 (exact 3294.63). Interpretation L02.html:270 and E1-E3 (L02.html:365-381; the changed hunk at :365 now reads 'Using Lab 1, Part D, and the gross notional that Part B prints') match.",
"BK4a-L02-problems": "Round 5 re-read of L02.html:315-406 (changed hunks at 354 and 365 read): M1 n (-10,-20,50,-20), A 50, G 180, reduction 7222 bp (130/180 floored); M2 G 460, A 100, reduction 7826 (unchanged ratio); M3 n1 -200, n2=n3=100, A 200 = G, 0 bp; P1 uses A1 (part a) and the identity (part c); P2 hypotheses Pay>=0, Rec>=0, G = sum Rec; P3 cycle with i owes i+1 (changed hunk at :354), Rec=Pay=a, n=0, A=0, reduction 10000 bp (G = ka > 0); E1-E3 read against Part B/C/D printed values (Part D 5093600, reduction 2502700; Part C sums 1753300+3340300 = 5093600; Part B members 1,2,4 both receive and pay); R1 range 0..10000 with G>0; R2 X (A=100) vs Y (A=100, G=200); R3 changes by at most a.",
"BK4a-L02-why-structure": "Round 5: check_pages_L02.out PASS; misconceptions 3 (L02.html:289-305); problem sets M/P/E/R (307-406); key results (412-425); quiz 10 items (431-510); references section (512-518) states the one paper-level registry citation.",
"BK4a-L02-canon-misconceptions": "Carried from round 4 (byte-identical since the previous pin 9a02b1af for: L02.html:280-285, 293-302; the round-5 delta touches L02.html:354 and :365 only). Round 5 re-read: misconceptions at L02.html:289-305 (netting, CCP-as-payment-system, zero sum) are correct against Proposition 2.2(b), Example 2.4 (amount 50 dollars against 230) and Lab 1 Part D. The 'Four places' heading at L02.html:280 is a separate FAIL row (BK4a5-L02-canon-heading).",
"BK4a-L02-attribution": "Round 5 FAIL. L02.html:277: 'Duffie and Zhu (2011) <span class=\"ref\" data-cite=\"duffie2011central\"></span>.' The literal space before the citation marker renders as '(2011) .' (cosmetic). L02.html:285: 'Duffie and Zhu (2011) asks the question at paper level, and no source for the answer is on this program's reference list yet.' This is contradicted by the registry: references/references.json:7411 holds duffie2011central (doi 10.1093/rapstu/rar001, verified by crossref, used_by BK4, title 'Does a Central Clearing Counterparty Reduce Counterparty Risk?', which is the question at L02.html:277). Live check: 'verify_refs.py --unit BK4' -> 2 of 560 entries, 0 problems (verify_refs_live_BK4.out). The paper-level attribution (question = title) PASSES; the sentence about the list does not.",
"BK4a-L03-def-props-1.2-1.3": "Round 5 FAIL on Proposition 1.2 (L03.html:77-80). The displayed identity is a1+a2+a3+sum_{i in V} x_i+u = L, and x_i is the floor share of Definition 1.1 (x_i = floor(Z DF_i / D), L03.html:70-72); the leftover cent l is not in the sum, yet the proof (L03.html:85) uses 'sum x_i + l = Z'. Counterexample from Example 1.6 (L03.html:124-126): Z = 1, three survivors DF 1, no margin/fund/capital: a1=a2=a3=0, all x_i = 0, u = 0, so the displayed left side is 0, not L = 1 (lab Part A2 prints member 1 paying 1 cent). The statement calls x_i 'the survivor payments', which is not Definition 1.1's x_i. Definitions, Proposition 1.3, Remark 1.4 and Example 1.5 table re-verified (rederive_a_r5.out: fixture rows 80..300 match; 20000 random waterfall cases with leftover included: 0 violations). Fix: define y_i = x_i + 1 for the first l survivors with DF_i > 0 (y_i = x_i otherwise; y_i = DF_i when Z >= D) and state a1+a2+a3+sum_{i in V} y_i+u = L.",
"BK4a-gate-check-pages": "Round 5 re-run: check_pages.py --unit BK4 -> 'check_pages BK4: PASS' (check_pages_unit.out); --page L01, L02, L03 -> PASS (check_pages_L0*.out); check_pages.py --all -> 27 PASS lines, 0 FAIL (check_pages_all.out).",
"BK4a-gate-check-dag": "Round 5 re-run: check_dag.py --unit BK4 -> 'check_dag BK4: PASS' exit 0 (check_dag.out).",
"BK4a-gate-run-labs": "Round 5 re-run: run_labs.py --unit BK4 -> 'run_labs BK4: PASS (8/8)' exit 0 (run_labs.out). Twins alone: python -I -W error on lab-BK4-L01-1.py, L02-1, L03-1 from /tmp: exit 0, stderr 0 bytes each (twin_L0*.out, .err).",
"BK4a-gate-page-smoke": "Round 5 re-run: page_smoke.py --unit BK4 --pages index L01 L02 L03 -> 'page_smoke BK4: PASS' exit 0 (page_smoke.out); lab runtimes 0.0-0.1 s.",
"BK4a-gate-ruff-mypy": "Round 5 re-run on the three twins: ruff check -> 'All checks passed!' (ruff_check.out); ruff format --check -> '3 files already formatted' (ruff_format.out); mypy --no-incremental -> 'Success: no issues found in 3 source files' (mypy_twins.out).",
"BK4a-gate-pytest-labs": "Round 5 re-run: pytest -q tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py tests/test_page_smoke.py -> all dots, exit 0 (pytest_relevant.out).",
"BK4a-gate-verify-refs": "Round 5: verify_refs.py --offline -> 'offline integrity: 560 entries, 0 problems' (verify_refs_offline.out); live verify_refs.py --unit BK4 -> 'live re-verification of BK4: 2 of 560 entries, 0 problems' (verify_refs_live_BK4.out), exit 0.",
"BK4a-banned-and-process": "Round 5: check_pages BANNED list passes on all four pages (check_pages_unit.out PASS). scan_words_a_r5.out: no TODO/TBD/lorem/'for brevity'/'details omitted'/'beyond the scope'/'clearly'/'obviously'/'studies show' and no ellipsis in the visible text of index, L01, L02, L03 (the one hit for 'Tokenization' is a card title); no process-word hits.",
"BK4a-rederive-r4": "Round 5 independent re-derivation: ledgers/BK4/scripts/BK4-a-r5/rederive_a_r5.py -> rederive_a_r5.out (stdlib, run with python -I). L01 (seed 20260, binary-search need); L02 (seed 2026 trade set, all netting numbers, floor 3294); L03 (seed 2026 inputs; sized margins 2961 for 9900 and 2992 for 9975 bps by exact ceil and brute force; max loss 2992; Example 2.5 199.5 and 198; R3 boundary S=400 first with k<S; M2/M3 sizing values; waterfall 20000 random cases, 0 violations; fixture rows 80..300).",
"BK4a-lab-block-equality-r4": "Round 5: ledgers/BK4/scripts/BK4-a-r5/block_compare.py -> block_compare.out: for L01, L02, L03 the page code block equals the twin source (rstrip per line) and the expected block equals the output of python3 -I -W error on the twin (32, 29 and 28 lines); exit 0, stderr empty.",
"BK4a-gate-repo-ruff-mypy-r4": "Round 5 re-run, whole repository: ruff check . -> 'All checks passed!' (ruff_repo.out); ruff format --check . -> '553 files already formatted' (ruff_format_repo.out); mypy --no-incremental -> 'Success: no issues found in 385 source files' (mypy_repo.out); build_site.py --check -> 'site data current: 6 outputs' (build_site_check.out); check_pages.py --all -> 27 PASS, 0 FAIL (check_pages_all.out).",
}

NEW_ROWS = [
{"id": "BK4a5-L01-lede-settlement-framing", "check": "2.9-prose / B1 settlement facts", "location": "L01.html:51 (why-it-matters paragraph)", "status": "FAIL",
 "evidence": "L01.html:51 reads 'A trade is paid for when the payment behind it settles, and, in the model used here, a bank that sends a payment needs money in its account to make it.' The first clause is a general statement of how trades are paid, presented as fact; the only qualifier attaches to the second clause. The plan (section 2.2) and the Architect default allow settlement facts only from an admitted source (B1), and the registry has no settlement-mechanics record. This is the same defect class as round-4 row BK4a-hub-settlement-framing (index.html:33), which was fixed at the hub but not in the lesson lede.",
 "fix": "L01.html:51: move the model qualifier to the front, e.g. 'In the model used here, a trade is paid for when the payment behind it settles, and a bank that sends a payment needs money in its account to make it.'"},
{"id": "BK4a5-L01-designs-pointer", "check": "2.9-prose (cross-reference)", "location": "L01.html:59 (Definition 1.1 lead-in)", "status": "FAIL",
 "evidence": "L01.html:59 reads 'It has two designs, which the lesson defines in Section 2.' The two designs (RTGS and DNS) are defined in the text immediately after Definition 1.1 on the same page, and Section 2 defines their measures (peak need, net debit, Definition 2.1). L01.html:313 says the designs are 'defined in Definitions 1.1 and 2.1'. The pointer and the other two statements disagree. Round 4 accepted the pointer as accurate; on re-reading, the pointer is wrong.",
 "fix": "L01.html:59: replace 'which the lesson defines in Section 2' with 'which Definition 1.1 defines and Section 2 measures'."},
{"id": "BK4a5-L01-canon-heading", "check": "2.9-prose", "location": "L01.html:308 (canon-breaks lead-in)", "status": "FAIL",
 "evidence": "L01.html:308: 'The two designs are exact inside Assumption 1.3 and simplified outside it. Four places where the analyst must act:' The four items that follow (L01.html:309-312) state limits of the model (no queues, the day is given, the settlement cycle is a parameter, no claim about real systems). They do not tell the analyst to act, so the lead-in misdescribes its list.",
 "fix": "L01.html:308: replace 'Four places where the analyst must act:' with 'Four places where the model stops:'."},
{"id": "BK4a5-L02-canon-heading", "check": "2.9-prose", "location": "L02.html:280 (canon-breaks lead-in)", "status": "FAIL",
 "evidence": "L02.html:280: 'The netting identities are exact under Assumption 1.3 and simplified outside it. Four places where the analyst must act:' The four items (L02.html:281-285) are limits of the model (obligations fixed, CCP flat, default not modelled, no finding about real clearing houses), not actions for the analyst.",
 "fix": "L02.html:280: replace 'Four places where the analyst must act:' with 'Four places where the model stops:'."},
{"id": "BK4a5-hub-prereq-uses", "check": "2.9-prose / 2.11-dag (prerequisite use)", "location": "index.html:61 (prerequisites paragraph)", "status": "FAIL",
 "evidence": "index.html:61: 'BK4 also uses M2 directly, for the limit. It uses these concepts without redefining them:' followed (index.html:62-66) by 'From M1: the present value and the geometric series', 'From M2: the limit', 'From E1: Bertrand competition'. A text search of index.html, L01-L03, L04, L05 and project.html (ledgers/BK4/scripts/BK4-a-r5/scan_words_a_r5.py and the grep recorded in this round) finds no use of present value, geometric series, the limit as a concept, or Bertrand competition in any lesson or the project; these appear only in the placement diagnostic items (index.html:75-98). The sentence claims a use that does not exist in the content.",
 "fix": "index.html:61: change 'BK4 also uses M2 directly, for the limit. It uses these concepts without redefining them:' to 'The placement diagnostic below tests these prerequisites:' and keep the FC1 items that the lessons use (clearing and settlement and the trade lifecycle, L01 'Uses' line), or remove the M1, M2 and E1 items from the 'uses' list."},
{"id": "BK4a5-links-anchors", "check": "2.9-structure (links)", "location": "index.html, L01.html, L02.html, L03.html (all href)", "status": "PASS",
 "evidence": "Round 5 script (ledgers/BK4/scripts/BK4-a-r5/links_a_r5.out): 25 hrefs in index.html and 12 in each lesson; no missing local target, no missing fragment id, no external URL."},
{"id": "BK4a5-twins-alone", "check": "2.5-labs (twins alone)", "location": "tests/labs/BK4/lab-BK4-L01-1.py, lab-BK4-L02-1.py, lab-BK4-L03-1.py", "status": "PASS",
 "evidence": "Round 5: each twin run alone as python -I -W error from /tmp (twin_L01.out, twin_L02.out, twin_L03.out): exit 0, stderr 0 bytes; no open/urllib/socket/requests/http in the three twins (grep, this round)."},
]

rows = []
carried_ids = []
for r in prev["rows"]:
    rid = r["id"]
    if rid in FRESH_EV:
        status = "PASS"
        if rid == "BK4a-L02-attribution" or rid == "BK4a-L03-def-props-1.2-1.3":
            status = "FAIL"
        new = dict(r)
        new["status"] = status
        new["evidence"] = FRESH_EV[rid]
        if status != "PASS":
            if rid == "BK4a-L02-attribution":
                new["fix"] = ("L02.html:285: replace 'and no source for the answer is on this program's reference list yet' with 'and this lesson states no answer from it'. "
                              "L02.html:277: move the citation marker so it follows the closing parenthesis without a space, e.g. 'Duffie and Zhu (2011)<span class=\"ref\" data-cite=\"duffie2011central\"></span>.'")
            else:
                new["fix"] = ("L03.html:79-80: define y_i = x_i + 1 for the first l survivors with DF_i > 0 (y_i = x_i otherwise; y_i = DF_i when Z >= D), "
                              "and state the identity as a1+a2+a3+sum_{i in V} y_i+u = L (the proof's 'sum x_i + l = Z' is then the same identity).")
        rows.append(new)
    elif r["status"] == "PASS":
        carried_ids.append(rid)
        new = dict(r)
        new["evidence"] = (f"Carried from round 4 (byte-identical since the previous pin {PREV_PIN} for: {r['location']}; "
                           f"the round-5 delta touches index.html:33,35,56,61,122,127, L01.html:55,296,370, L02.html:354,365 and project.html:58,197-250,416,434, none of them cited here): "
                           + r["evidence"])
        rows.append(new)
    else:
        raise SystemExit(f"unexpected non-PASS carried row {rid}")

# the round-4 FAIL row is superseded by fresh evidence (cleared)
assert any(r["id"] == "BK4a-hub-settlement-framing" and r["status"] == "PASS" for r in rows)
rows.extend(NEW_ROWS)

fragment = {
  "unit": "BK4",
  "slice": "BK4-a",
  "round": 5,
  "round_note": ("Round 5 of BK4-a (hub index.html, L01, L02, L03, lab twins 1-3), pin 7376a5e (previous pin 9a02b1a, round-4 fragment /Users/billyribeiro/.fanout/frags/E-BK4-a.round4.json). "
                 "Delta 9a02b1a..7376a5e for the slice: index.html:33,35,56,61,122,127; L01.html:55,296,370; L02.html:354,365. L03.html and tests/labs/BK4/lab-BK4-L01-1.py, L02-1, L03-1 are byte-identical. "
                 "All four pages were read in full as stripped text (ledgers/BK4/scripts/BK4-a-r5/index.txt, L01.txt, L02.txt, L03.txt). Every round-4 row id is kept. Rows whose cited subject is byte-identical are carried with the prefix; rows that cite a changed line, or that failed, were re-verified from scratch this round."),
  "verifier": "Haiku independent verifier, BK4-a round 5 (did not build BK4)",
  "pin": "7376a5e216c1e6d99becc76b4cd64028f5b55d3f",
  "base": "9a02b1af9f92a060f7fabf7e1b3afb5ea95f45ba (round-4 pin)",
  "checkout": str(ROOT),
  "scratch": str(S),
  "verified_at": "2026-11-04",
  "verdict": "FAIL",
  "rows": rows,
  "mutants": [],
  "registry_flags": [
    "SEC T+1 settlement rule (curriculum yaml:1092): no record in references/references.json (no sec.gov key). Index and lessons state only that the rule is named, not stated (index.html:193; L01.html:46, :281). Admission via tools/add_reference.py is needed before any settlement-rule fact (B1).",
    "duffie2011central: live verify_refs --unit BK4 passes (2 of 560 entries, 0 problems). Registry title is the question L02 attributes at paper level (references.json:7411).",
    "bisndcpmi: issuer-level record (references.json:2853); used at index level only (index.html:193)."
  ],
  "freshness_flags": [],
  "notes": [
    "Verdict FAIL: seven rows are non-PASS (BK4a-L02-attribution, BK4a-L03-def-props-1.2-1.3, BK4a5-L01-lede-settlement-framing, BK4a5-L01-designs-pointer, BK4a5-L01-canon-heading, BK4a5-L02-canon-heading, BK4a5-hub-prereq-uses). All are wording or statement defects; no number is wrong (every number in the four pages re-derived this round).",
    f"Carried rows ({len(carried_ids)}): round-4 PASS rows whose cited lines are byte-identical since {PREV_PIN}; each keeps its round-4 id and check and carries the prefix. Fresh rows were re-verified this round against the round-5 files.",
    "Round-4 FAIL row BK4a-hub-settlement-framing is cleared by the edit at index.html:33 (PASS here, fresh evidence).",
    "Round-4 note on L01.html:59 ('defined in Section 2 ... not a defect') is overruled on re-reading: see BK4a5-L01-designs-pointer.",
    "Wording observation, not a row: Corollary 2.4 heading (L03.html) reads 'the sized margin rises with the target' for a non-strict inequality M(t) <= M(t'); the statement and the key-results row ('does not fall') are exact.",
    "Mutants: none. Slice a has no grader; the lab twins are demonstrations, and mutation applies to grader/ only (FINAL-ARCHITECT-RULINGS 9; plan section 11 item 11).",
    "Not checked by this slice: content of L04, L05, project.html, cards.json and the grader (other slices). The hub's L04 and L05 summaries were compared with those pages' titles and lab descriptions only. Duffie and Zhu (2011) abstract not read: no finding of the paper is stated in slice a (plan B2).",
    "No network bot checks or access blocks were encountered; the live verify_refs run succeeded with plain HTTP through the tool."
  ],
  "summary": {}
}
counts = {"rows": len(rows), "pass": sum(r["status"] == "PASS" for r in rows), "fail": sum(r["status"] == "FAIL" for r in rows), "unverifiable": sum(r["status"] == "UNVERIFIABLE" for r in rows)}
fragment["summary"] = counts
out = ROOT / "ledgers/BK4/BK4-a.json"
out.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("rows", counts, "carried", len(carried_ids))
