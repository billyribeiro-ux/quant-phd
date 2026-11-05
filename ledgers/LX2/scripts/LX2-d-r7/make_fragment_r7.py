"""LX2-d round 7: writes ledgers/LX2/LX2-d.json (fragment). Run with python -I from the checkout root."""
import json
import sys

CARRY = ("Carried from round 6 (course/modules/LX/LX2/L01.html, L02.html, L03.html, L04.html, index.html, "
         "tests/labs/LX2 twins, references/, notation/, tools/ byte-identical since the round-6 pin 4bd8cb94; "
         "the round-7 delta touches only cards.json and project.html):")
R7_SRC = "cards.json at 06994db (sha of file in git); scripts in ledgers/LX2/scripts/LX2-d-r7/"

rows = []


def row(rid, status, check, location, evidence, fix="none"):
    rows.append({"id": rid, "status": status, "check": check, "location": location, "evidence": evidence, "fix": fix})


row("d-cards-001-010", "FAIL",
    "2.7 card vs current lesson; 2.6 statute attribution (LX2-c001..c010)",
    "course/modules/LX/LX2/cards.json LX2-c010 back; course/modules/LX/LX2/L01.html line 84 (section 8(b) paragraph); "
    "statute COMPS-1884.txt lines 1766-1774 (section 8(b))",
    "Re-verified (cards.json unchanged for c010; L01.html unchanged since the round-6 pin). c010 back says the Commission "
    "may refuse 'after notice and opportunity for hearing'. Section 8(b) text (grep -n 'not later than ten days' "
    "/tmp/lx2d-r6-src/COMPS-1884.txt, lines 1771-1773) attaches two timing conditions: notice 'not later than ten days "
    "after the filing of the registration statement' and hearing 'within ten days after such notice'. The card and L01 "
    "line 84 both drop them. c001-c009 are carried from round 6 (statute_1933_check_r6.out; cards unchanged); they contain no "
    "double-quoted passage, so the mechanical quote check (quote_check_cards_r7.out) does not cover them.",
    "LX2-c010 back: after 'after notice' add 'by personal service or confirmed telegraphic notice not later than ten days "
    "after the filing of the registration statement, and opportunity for hearing within ten days after that notice'. "
    "Make the same change to L01.html line 84 (builder's file), then re-run check_pages --unit LX2.")

row("d-cards-011-020", "FAIL",
    "2.7 card vs current lesson; 2.6 statute attribution (LX2-c011..c020)",
    "course/modules/LX/LX2/cards.json LX2-c016 back; course/modules/LX/LX2/L01.html line 111; statute COMPS-1885.txt lines 11117-11127",
    "c016 changed in this round: the back now reads 'held of record by less than 300 persons, with a different count for "
    "certain banks'. The question asks on what ground, and the card still does not state the bank ground. Statute "
    "(COMPS-1885.txt lines 11117-11127, third sentence of 15(d)(1)): 'less than 300 persons, or, in the case of a bank, a "
    "savings and loan holding company ... or a bank holding company ... 1,200 persons'. The figure 1,200 appears nowhere in "
    "L01.txt (grep -n '1,200' /tmp/lx2d-r7/L01.txt returns nothing), so the lesson does not state it either; L01 line 111 "
    "gives only 'a different count' and line 109 gives 'fewer than 300 persons' with no bank exception. "
    "c011-c015 and c020-c021 are carried from round 6 (cards and L01 unchanged); c017-c018 (T, Propositions 4.1 and 4.2) are carried from round 6 "
    "with key rows L01.txt lines 509-510 unchanged; c019 changed and PASSes (see d-card-labels-current).",
    "State the 1,200 ground in LX2-c016 back and in L01.html line 111, and state the bank exception in L01.html line 109 "
    "(otherwise the 300-person statement there is incomplete). Then re-run check_pages --unit LX2.")

row("d-cards-021-030", "PASS",
    "2.7 card vs current lesson; 2.6 statute attribution (LX2-c021..c030)",
    "course/modules/LX/LX2/cards.json LX2-c021..c030; L01.html lines 119-122, 139, 364-378, 451",
    CARRY + " cards c021-c030 unchanged in the delta (git diff 4bd8cb94 06994db touches only c016, c019, c054 in cards.json). "
    "Round-6 evidence stands; the cards_scan_r7.out numeric-token check (every numeric token in each card occurs in its own "
    "lesson text) also passes for these cards.")

row("d-cards-031-040", "PASS",
    "2.3 grades; 2.6/2.7 attribution, page locators and lesson agreement (LX2-c028..c040)",
    "cards.json LX2-c028..c040; L02.html lines 55-115, 441-447, 611-617",
    CARRY + " Re-run this round: lab-LX2-L02-1.py under python3 -I -W error exits 0 with no stderr; its printed table fires "
    "P1, P3, P4, P6 and not P2, P5, P7, P8 (4 of 8), matching c038, c039, c040, c041, c042 and c037 ('Scienter is not "
    "checked').")

row("d-cards-041-050", "PASS",
    "2.3 grades; 2.6/2.7 attribution, page locators and lesson agreement (LX2-c041..c050)",
    "cards.json LX2-c041..c050; L02.html lines 441-447; L03.html lines 58-77",
    CARRY + " c044-c050 match L03 Definition 1.1, Remark 1.2, Definition 1.3 and Assumption A1 (L03.txt lines 17-26); ungraded.")

row("d-cards-051-060", "PASS",
    "2.3 grades; 2.7 card vs lesson (LX2-c051..c059)",
    "cards.json LX2-c051..c059; L03.html line 82 (Proposition 2.2), line 93 (Remark 2.3), lines 355, 514-516; "
    "twin output `python3 -I -W error tests/labs/LX2/lab-LX2-L03-1.py`",
    "Re-verified from scratch (c054 changed). c051: G = R + 2X + C_m + C_t under A1 matches Proposition 2.2 (L03.txt line 82), "
    "key row L03.txt line 514 (T). c054 is now ungraded (grade field absent; the round-6 grade-T defect on Remark 2.3 is fixed), "
    "and its back begins 'Under A1,' (the hypothesis of Proposition 2.2 per L03.txt line 82). Its claim 'fails at each moment "
    "after a trader cancels a resting order' is consistent with Remark 2.3 ('fails whenever a trader cancels a resting order', "
    "L03.txt line 93). c052 matches Remark 2.4 (L03.txt line 98). c053 numbers match the twin output table: trader 0 cancel_pct 5, "
    "6/97; trader 1 cancel_pct 10, 3/104; 3*97=291 < 6*104=624. c055-c057 match Definitions 3.1/3.2 (L03.txt lines 361-366, 399) "
    "and Section 3. c058: twin prints 'events with a crossed book: 0'. c059: twin prints 'traders flagged: 0 of 6' and "
    "'largest ratio 21/37'.")

row("d-cards-061-070", "PASS",
    "2.7 card vs lesson; 2.6 attribution (LX2-c061..c070)",
    "cards.json LX2-c061..c070; L03.html Section 4 (lines 377-382); L04.html lines 63-111; SR 26-2 attachment pages 1-3",
    CARRY + " c068 (locator pp. 1-2) re-checked this round: the attachment sentence 'responsible for adopting model risk "
    "management practices that are appropriate and effective for managing the specific risks the banking organization faces "
    "or is likely to face' spans attachment page 1 to page 2 with the page-1 footer '1' between (/tmp/lx2d-r6-src/att.txt "
    "lines 44-50); the mechanical quote check reports NOMATCH only because of that footer (quote_check_cards_r7.out), so the "
    "quotation is verbatim and the pages are correct.")

row("d-cards-071-080", "PASS",
    "2.3 grades; 2.7 card vs lesson; numbers (LX2-c071..c080)",
    "cards.json LX2-c071..c080; L04.html lines 116-142; L04.txt lines 116-138, 435-437",
    CARRY + " Re-derived this round: numbers_r7.out gives E[e]=1, P(hit)=44/117=0.37607, hits 9 of 24, hit rate 3/8, bias 41/12, "
    "Part C bias 0 and MAE 3. c076/c077 match Theorems 4.2/4.3 and key rows L04.txt lines 436-437 (T); c078/c079 match Proposition "
    "4.4 and key row L04.txt line 437.")

row("d-cards-081-089", "PASS",
    "2.3 grades; 2.6/2.7 attribution, locators, lesson agreement (LX2-c081..c089)",
    "cards.json LX2-c081..c089; L04.html lines 56-111; L04.txt key rows lines 430-433; SR 26-2 letter and attachment; CFA III(A), VI(A)",
    CARRY + " Quotations c087, c088, c089 re-checked this round by the mechanical quote check plus source lines: cfa3a.txt line 138 "
    "('Standard III(A) does not render all members and candidates fiduciaries.'; card ends with a comma inside the quotation marks, "
    "a trivial punctuation difference), att.txt lines 67-69 ('does not set forth enforceable standards or prescriptive "
    "requirements; ... will not result in supervisory criticism', with a page break).")

row("d-cards-090-094", "PASS",
    "2.7 card vs lesson; 2.3 grades (LX2-c090..c094)",
    "cards.json LX2-c090..c094; L01.html key row line 511; L03.html key row line 515",
    CARRY + " Re-run this round: twin L01 prints 'reachable from unregistered/not_listed: 10 of 10', 'states where both reporting "
    "duties apply: 0', 'states where a sale is permitted and an offer is not: 0'; twin L03 prints 'events where entered != resting + "
    "2 * traded + market cancelled + trader cancelled: 0' (c093) and 'tally from the event log disagrees with the book in 0 trader "
    "counts' (c094). c093-c094 are ungraded or C with basis naming the SIMULATED run.")

row("d-c058-grade", "PASS",
    "2.3 grade consistency: LX2-c058 vs L03 key row",
    "cards.json LX2-c058 (C); L03.html line 515 key row",
    CARRY + " Twin L03 this round prints 'events with a crossed book: 0' (python3 -I -W error run, exit 0).")

row("d-c059-grade", "PASS",
    "2.3 grade consistency: LX2-c059 vs L03 key row",
    "cards.json LX2-c059 (C); L03.html line 516 key row",
    CARRY + " Twin L03 this round prints 'traders flagged: 0 of 6' and 'largest ratio 21/37'.")

row("d-c085-grade", "PASS",
    "2.3 grade consistency: LX2-c085 vs L04 key row",
    "cards.json LX2-c085 (C); L04.html line 434 key row",
    CARRY + " numbers_r7.out: hits 9 of 24, hit rate 3/8, bias 41/12, sum 82.")

row("d-cards-no-grade", "PASS",
    "cards without a grade field",
    "cards.json: 31 ungraded cards (cards_near_dup_ungraded_r7.out): c001-c003, c005, c008, c022, c023, c044-c050, c052-c057, c060-c063, c070-c075, c094",
    "Re-computed this round. c054 moved from T to ungraded (the round-6 fix), so the ungraded count is 31 (round 6 recorded 30, "
    "which was a miscount of the same set). Ungraded cards are definitions, conventions, readings, misconception cards restating "
    "lesson text, and three printed-output cards (c023, c053, c094) whose basis names the lab; the round-5 null-grade fix is "
    "accepted. No ungraded card states a theorem (c054 now restates Proposition 2.2 under its hypothesis A1 without grading).")

row("d-cards-schema", "PASS",
    "card schema and counts",
    "cards.json (97 cards)",
    "cards_scan_r7.out (python3 -I ledgers/LX2/scripts/LX2-d-r7/cards_scan_r7.py): 97 cards, 97 unique ids, ids LX2-c001..c097 "
    "sequential, fronts and backs unique; grades C 55, T 11, ungraded 31.")

row("d-cards-coverage", "PASS",
    "cards against L01..L04 section headings",
    "cards.json against L01.html..L04.html section headings and Lab blocks",
    CARRY + " Coverage is unchanged: the delta changed the text of c016, c019 and c054 only, and each remains attached to its "
    "lesson section.")

row("d-dup-scan", "PASS",
    "duplicate and near-duplicate fronts and backs",
    "cards.json, all 97 fronts and backs",
    "cards_near_dup_ungraded_r7.out: no exact duplicates. difflib ratio >= 0.75 gives eight pairs, each a different fact: "
    "c058/c093 and c058/c094 and c093/c094 (crossed-book count, identity failures, tally disagreements); c060/c062 (broker, latency); "
    "c066/c067 and c067/c069 (model, model risk, outcomes analysis); c071/c072 (hit rate, bias); c091/c092 (backs: count of "
    "states with both duties, count with sale and no offer).",
    "none")

row("d-atomic-split", "PASS",
    "atomicity of round-4 splits",
    "cards.json LX2-c058, LX2-c090..c094",
    CARRY + " Each card tests one printed count or one fact (c090-c092 one count each; c093, c094 one count each; c058, c059 separate facts).")

row("d-attrib-statute", "FAIL",
    "statute attribution and locators (1933 and 1934 Acts)",
    "cards.json LX2-c010, LX2-c016; L01.html lines 84, 109, 111",
    "Statute quotations re-checked this round. Passing: c001-c009, c011-c015, c024-c027 carried from round 6 "
    "(statute_1933_check_r6.out, statute_1934_check_r6.out; cards unchanged). c095 ('whichever date is the later', COMPS-1884 "
    "section 8(b), read this round). c096 ('other than the fiscal year within which such registration statement became effective', "
    "COMPS-1885.txt lines 11117-11121, read this round). Failing: c010 (section 8(b) ten-day notice and "
    "hearing timing dropped; see d-cards-001-010) and c016 (1,200-person bank ground still not stated; see d-cards-011-020).",
    "See d-cards-001-010 and d-cards-011-020.")

row("d-attrib-opinions", "PASS",
    "opinion attributions (Dirks, O'Hagan)",
    "cards.json LX2-c028..c043, c097; L02.html lines 55-115, 441-451, 561-617",
    CARRY + " Opinion quotations unchanged; the mechanical quote check matches each Dirks and O'Hagan quotation in the cards to the "
    "fetched USREPORTS texts (quote_check_cards_r7.out: c029, c031, c032, c034, c035, c037, c039, c041, c043, c097 MATCH).")

row("d-attrib-sr2026", "PASS",
    "SR 26-2 attribution (frb2026fed)",
    "cards.json LX2-c066..c069, c082..c084, c089; L04.html lines 85-111",
    CARRY + " c068 quotation and page locator (pp. 1-2) re-checked this round (att.txt lines 44-50).")

row("d-attrib-cfa", "PASS",
    "CFA Code and Standards attribution",
    "cards.json LX2-c064, c065, c080, c081, c087, c088; L04.html lines 56-82",
    CARRY + " c088 and c089 quotations re-checked (cfa3a.txt line 138; att.txt lines 67-69).")

row("d-numbers", "PASS",
    "numbers in prose, cards and labs (all numeric tokens)",
    "cards.json numeric tokens; L01.html state counts; L03/L04 printed values",
    "Fresh this round: cards_scan_r7.out reports no numeric token in any card's front or back that is absent from its own lesson "
    "text. numbers_r7.out (numbers_r6.py re-run with python -I): Part A hits 9/24, hit rate 3/8, bias 41/12; windows 1/4, 11/3, 1/2, "
    "19/6; Part C bias 0, MAE 3; E[e]=1, P(hit)=44/117=0.376068; Var(e)=62/3; gap 29/12.")

row("d-labs-run", "PASS",
    "labs: twins under python -I -W error; run_labs; expected output",
    "tests/labs/LX2/lab-LX2-L01-1.py..L04-1.py; project labs; L01..L04 printed blocks",
    "run_labs.py --unit LX2: PASS (7/7) (labs_smoke_LX2_r7.out). Each twin run alone under python3 -I -W error exits 0 with empty "
    "stderr (L01, L02, L03, L04 this round). page_smoke --unit LX2 PASS (smoke_refs_LX2_r7.out).")

row("d-l02-quiz-scienter-p663", "PASS",
    "L02 quiz footnote 23 and page locators",
    "course/modules/LX/LX2/L02.html quiz lines 611-617; key row line 565",
    CARRY + " Footnote 23 (USREPORTS-463-646.txt lines 757-759, p.663) unchanged.")

row("d-l03-dodd-mifid", "PASS",
    "L03 Dodd-Frank and MiFID II content and registry",
    "course/modules/LX/LX2/L03.html lines 358-371, 399, 514-518; references/references.json",
    CARRY + " verify_refs.py --offline: 'offline integrity: 560 entries, 0 problems' this round (smoke_refs_LX2_r7.out). No "
    "primary-text entry for Dodd-Frank or MiFID II.")

row("d-dag", "PASS",
    "DAG and concept links",
    "tools/check_dag.py --unit LX2; course/modules/LX/LX2/*.html",
    "check_dag.py --unit LX2: PASS this round (gates_LX2_r7.out).")

row("d-notation", "PASS",
    "notation registry (notation/notation.json)",
    "course/modules/LX/LX2/L01..L04.html math; cards.json",
    CARRY + " notation/ unchanged. The changed cards introduce no new symbol (c054 uses C_t, A1 already defined in L03).")

row("d-process-banned", "PASS",
    "process words in learner text",
    "course/modules/LX/LX2/L01..L04.html text; cards.json; project.html is outside this slice",
    "check_pages --unit LX2: PASS this round, including its banned-string scan of visible prose (gates_LX2_r7.out). The three "
    "changed cards (c016, c019, c054) read as learner text with no process word.")

row("d-gates-structure", "PASS",
    "structure gates",
    "tools/check_pages.py --unit LX2; check_projects; build_site --check; check_dag --unit LX2; ruff; mypy; pytest; verify_refs",
    "Fresh this round: check_pages LX2 PASS, check_dag LX2 PASS, check_projects LX2 PASS (gates_LX2_r7.out); build_site --check: "
    "'site data current: 6 outputs' (build_site_check_r7.out); ruff check . 'All checks passed!' and ruff format --check '553 files "
    "already formatted' (static_r7.out); mypy --no-incremental 'Success: no issues found in 385 source files'; pytest "
    "tests/test_page_checks.py tests/test_run_labs.py tests/test_labs.py -k 'LX2 or cards or check_cards or lx2' 7 passed; "
    "verify_refs --offline 0 problems.")

row("d-grade-key-consistency", "PASS",
    "every card grade matches a lesson grade or key row",
    "cards.json grades; L01.html key rows 509-511; L03.html key rows 514-516; L04.html key rows 434-437",
    "Fresh this round: T cards are c017-c021, c051, c076-c079, c086 (11, cards_scan_r7.out). c017-c021 map to L01 key rows 509-510 "
    "(Propositions 4.1-4.3, 10 states and 22 transitions); c051 to L03 key row 514 (Proposition 2.2); c076-c079 and c086 to L04 key "
    "rows 435-437. c054 is no longer graded, so the round-6 failure (T on Remark 2.3, which the lesson does not grade) is resolved. "
    "C cards with lab results (c038, c058, c059, c085, c090-c093) have key rows or the basis names the SIMULATED run; c023, c053, "
    "c094 are ungraded per the round-5 fix.")

row("d-delta-read", "PASS",
    "round-7 delta read in full (hunks in the slice)",
    "git diff 4bd8cb94 06994db -- course/modules/LX/LX2/cards.json",
    "Read every hunk: cards.json has three hunks: c016 back (adds 'with a different count for certain banks'), c019 front "
    "(adds 'a permitted sale implies a permitted offer in the model'), c054 (grade T and basis removed; back begins 'Under A1,' and "
    "says 'at each moment after'). The project.html hunks (rung 2, Lab 2 text, the time table, a not-documented entry) are outside "
    "slice d and were not read here.")

row("d-r2-lesson-delta", "PASS",
    "L02 E2/E3 narration (round-4 defect)",
    "course/modules/LX/LX2/L02.html lines 514-523 (E2, E3)",
    CARRY + " E2 and E3 blocks unchanged.")

row("d-l01-line63-s3-defined", "PASS",
    "L01 section 1 says the term is defined in section 3 (round-4 defect)",
    "course/modules/LX/LX2/L01.html line 63 vs line 96 and cards.json LX2-c005",
    CARRY + " L01 identical since round 6; LX2-c005 unchanged.")

row("d-l01-line88-spacing", "PASS",
    "L01 line 88 spacing (round-4 defect)",
    "course/modules/LX/LX2/L01.html line 88",
    CARRY + " L01.html identical since round 6.")

row("d-grade-legend", "PASS",
    "grade legend consistent across the unit",
    "course/modules/LX/LX2/L01.html..L04.html lines 43-48",
    CARRY + " Legends unchanged.")

row("d-l04-quiz-five-places", "PASS",
    "L04 quiz precision (round-4 defect)",
    "course/modules/LX/LX2/L04.html quiz prompt (line 513)",
    CARRY + " L04.html identical since round 6.")

row("d-l04-line82-locator", "PASS",
    "L04 VI(B) quote locator (round-4 defect)",
    "course/modules/LX/LX2/L04.html line 82",
    CARRY + " L04.html identical since round 6.")

row("d-quote-fidelity", "PASS",
    "every double-quoted passage in the changed lines of L01 and L02 against the fetched sources",
    "course/modules/LX/LX2/L01.html lines 51, 92, 96, 139, 344, 360; L02.html lines 51, 56, 61, 77, 84-85, 92",
    CARRY + " The card-side quotations were re-checked this round by quote_check_cards_r7.out (18 quoted passages: 15 MATCH; the "
    "3 that did not match mechanically were read by hand: c068 page break, c088 and c089 trailing punctuation inside the quote).")

row("d-l03-hypothesis-claims", "PASS",
    "L03 round-5 hypothesis paragraph (claims: crossed-book count zero, cancel selection rule)",
    "course/modules/LX/LX2/L03.html line 103, line 355",
    CARRY + " Printed values re-run: crossed book 0, identity failures 0, tally disagreements 0 (twin L03).")

row("d-l04-e3-arithmetic", "PASS",
    "L04 problem E3 and section 5 (standard error under A1, A2)",
    "course/modules/LX/LX2/L04.html Problem E3 and Section 5",
    CARRY + " numbers_r7.out: Var(e)=62/3, gap 29/12, gap/se^2 = 2.604 (the lesson says about 2.60).")

row("d-l01-sec5-statute", "PASS",
    "L01 section 5 statute statements (exemptions, 5(d), 6(e)(1), 8(e), 12(d), 15(d))",
    "course/modules/LX/LX2/L01.html section 5 (lines ~588-600)",
    CARRY + " Section 5 is unchanged. Its 15(d) statement is the source of the c016 defect and is noted in d-cards-011-020.")

row("d-cards-096-097", "PASS",
    "2.7 card vs lesson; 2.6 statute/opinion attribution (LX2-c096, LX2-c097; new since round 5)",
    "cards.json LX2-c096, c097; L01.html Section 3; COMPS-1885.txt fiscal-year sentence; USREPORTS-463-646.txt lines 757-759",
    CARRY + " c096 'other than the fiscal year within which such registration statement became effective' matches COMPS-1885.txt "
    "(read this round, lines ~11117-11121). c097 'a mental state embracing intent to deceive, manipulate, or defraud' is a quotation "
    "that the quote check matches in the Dirks text.")

row("d-card-labels-current", "PASS",
    "cards carry the current lesson labels for propositions and assumptions",
    "cards.json LX2-c017..c019, c076..c078, c086; L01.txt lines 319, 331, 343; L04.txt lines 126-138",
    "Fresh this round: the round-6 stale label is fixed. c019 front now reads 'Proposition 4.3 (a permitted sale implies a permitted "
    "offer in the model)', identical to L01.txt line 343. c017 'Proposition 4.1 (reachability)' is a shortened form of L01 line 319 "
    "'(reachability in the model)', not a stale label. c076 and c077 match Theorems 4.2 and 4.3 (L04.txt lines 126, 132); c078 "
    "matches Proposition 4.4 (L04.txt line 138). Every other 'Definition', 'Remark', 'Assumption', 'Problem' label in the cards "
    "matches a lesson heading (grep of cards.json against L0*.txt headings).")

row("d-c054-hypothesis", "PASS",
    "round-7 card c054: grade removal and Proposition 2.2 hypothesis",
    "cards.json LX2-c054; L03.html line 82 and line 93",
    "c054 back now begins 'Under A1,' (the Proposition 2.2 hypothesis, L03.txt line 82) and carries no grade, so it is a "
    "misconception card restating the lesson's Remark 2.3 (ungraded, L03.txt line 93). Verified by reading both lines.")

fragment = {
    "unit": "LX2",
    "slice": "LX2-d",
    "round": 7,
    "verifier": "Claude Haiku 5.5, independent verifier for LX2-d, round 7 (did not build LX2; shares no context with the builders)",
    "pin": "06994db16d1ab449bcf29898a7f56cfa999dce57",
    "base": "4bd8cb94a8e171e80c4c34da1b3f32be7cb93f07 (round-6 pin). Delta 4bd8cb94..06994db touching the slice: cards.json (c016, c019, c054) and project.html (outside slice d). L01..L04.html, index.html, tests/labs/LX2 twins, references/, notation/, tools/ byte-identical.",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE7-LX2-d",
    "scratch": "/tmp/lx2d-r7 (lesson plain text L01-L04.txt, card lines); statute and opinion sources in /tmp/lx2d-r6-src (fetched in round 6 by plain curl; hashes in ledgers/LX2/scripts/LX2-d-r6/sha256_sources_r6.txt)",
    "verified_at": "2026-11-04T21:30:00+00:00",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [
        "references/references.json: 560 entries; no Dodd-Frank Act or MiFID II primary-text entry (the L03 'no registry key' statements hold). verify_refs --offline: 0 problems (smoke_refs_LX2_r7.out).",
    ],
    "freshness_flags": [
        "Statute compilations and opinion texts are the round-6 plain-curl fetches (COMPS-1884, COMPS-1885, USREPORTS-463-646, USREPORTS-521-642); not re-fetched this round.",
    ],
    "notes": [
        "Round 7 on pin 06994db. Delta read in full for cards.json (c016, c019, c054). Rows whose cited subject is unchanged are carried from round 6 with the prefix 'Carried from round 6'; all others were re-run this round.",
        "c019 PASS: label now matches L01 line 343. c054 PASS: grade removed, Under-A1 hypothesis added. c016 remains FAIL: the bank ground (1,200 persons, COMPS-1885.txt lines 11117-11127) is still not stated in the card or in L01.txt, which says only 'a different count for certain banks'.",
        "c010 remains FAIL: the section 8(b) ten-day notice and hearing timing is not stated (COMPS-1884.txt lines 1771-1773); unchanged since round 6.",
        "Mutation testing: not applicable. The slice is cards and lessons; there is no grader and no project lab in it. No mutants are listed.",
        "Ungraded set is 31 cards; the round-6 note of 30 was a miscount. T set is 11.",
    ],
    "summary": {
        "slice": "LX2-d (all 97 cards.json cards against L01-L04)",
        "verdict": "FAIL",
        "rows": len(rows),
        "pass": sum(1 for r in rows if r["status"] == "PASS"),
        "fail": sum(1 for r in rows if r["status"] == "FAIL"),
        "unverifiable": 0,
        "mutants": "0/0 (no grader in slice)",
        "failing_rows": [r["id"] for r in rows if r["status"] != "PASS"],
        "text": "Two cards need a fix: c010 (section 8(b) ten-day notice and hearing timing omitted) and c016 (the 1,200-person bank ground for the 15(d)(1) fiscal-year suspension not stated). Both need the matching sentence in L01.html (line 84 and line 111; line 109 also says '300 persons' without the bank exception).",
    },
}

out = sys.argv[1]
with open(out, "w", encoding="utf-8") as fh:
    json.dump(fragment, fh, ensure_ascii=False, indent=1)
    fh.write("\n")
print("rows", len(rows), "pass", fragment["summary"]["pass"], "fail", fragment["summary"]["fail"])
