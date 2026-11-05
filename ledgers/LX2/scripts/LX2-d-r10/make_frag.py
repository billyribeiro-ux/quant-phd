import json
CARRY = "Carried from round 9 (course/modules/LX/LX2/L03.html and L04.html byte-identical since the pin c93dd52; L02.html and cards.json entries cited here byte-identical, the changed L02 lines are 53, 465, 505, 528 and the changed cards.json line is 706):"
CARRY_CARDS = "Carried from round 9 (cards.json entries cited here byte-identical since c93dd52; changed cards.json line is 706 = LX2-c092; L03.html and L04.html byte-identical):"
rows = []
def R(id, check, location, status, evidence, fix=None):
    r = {"id": id, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    rows.append(r)

R("d-cards-001-010",
  "2.7 card vs current lesson; 2.6 statute attribution (LX2-c001..c010)",
  "course/modules/LX/LX2/cards.json LX2-c001..c010; course/modules/LX/LX2/L01.html lines 74-86",
  "PASS",
  "Re-verified from scratch. Statute text: plain-curl COMPS-1884.pdf re-fetched 2026-11-05, sha256 c67e553505b0329d7c00c49efc2503685cbb2b107883b025025320478522bfc8 (same as round 9); pdftotext normalised file scratch .../src/c1884.norm.txt. c010 back now matches L01.html line 84 and the statute's 8(b) sentence ('not later than ten days after the filing ... and opportunity for hearing (at a time fixed by the Commission) within ten days after such notice'), so the round-9 FAIL is closed. c001-c009 checked against L01 lines 74-96 and the 8(a), 5(a), 5(c), 6(a), 6(c) statute quotes: each quoted phrase FOUND by ledgers/LX2/scripts/LX2-d-r10/statute_check.py and the paraphrases match.")

R("d-cards-011-020",
  "2.7 card vs current lesson; 2.6 statute attribution (LX2-c011..c020)",
  "course/modules/LX/LX2/cards.json LX2-c011..c020; course/modules/LX/LX2/L01.html lines 100-111 and 115-122",
  "PASS",
  "Re-verified from scratch. c016 back ('... or, in the case of a bank, a savings and loan holding company or a bank holding company, 1,200 persons') now matches L01.html line 111, which carries the same '1,200 persons' clause; COMPS-1885.pdf (plain curl, sha256 c7a620b624baa99bbe9edfbe7444081a6b6c838acc085464451192566b43ad8, same as round 9) 15(d)(1) third sentence reads 'held of record by less than 300 persons, or, in the case of a bank, a savings and loan holding company ..., or a bank holding company ..., 1,200 persons' (FOUND, statute_check.py). The round-9 FAIL is closed. c011-c015 re-checked against 12(a), 12(b), 12(d) (both sentences) and 13(a): FOUND in normalised text. c017-c020 re-derived against L01 lines 320-352 and the model enumeration output (10 states, 22 transitions).")

R("d-cards-021-030",
  "2.7 card vs current lesson; 2.6 statute attribution (LX2-c021..c030)",
  "course/modules/LX/LX2/cards.json LX2-c025 back; course/modules/LX/LX2/L01.html lines 85 and 378 (section 8(d))",
  "FAIL",
  "c021-c024, c026, c027 re-verified: 22 transitions (6x2 + 2x5), Lab 1 table rows (filed/not_listed offer yes sale no; stop_order offer no sale no), 5(a), 8(a), 6(a), 12(b), 15(d)(1) second sentence all agree with L01 lines 119-122, 374-386 and the statute. c028-c030 carried (L02 spans unchanged). c025 FAILS: its back says 'after notice by personal service or the sending of confirmed telegraphic notice and after opportunity for hearing', and L01.html line 85 ('Section 8(d): ...') and line 378 ('... and an opportunity for hearing') say the same. The statute, COMPS-1884.pdf 8(d) sentence (normalised text, FOUND by statute_check.py), reads 'after notice by personal service or the sending of confirmed telegraphic notice, and after opportunity for hearing (at a time fixed by the Commission) within fifteen days after such notice by personal service or the sending of such telegraphic notice'. The 15-day timing is stated for 8(b) at L01.html line 84 (fixed in this batch) but omitted for 8(d), so the lesson and the card omit a statutory condition they attribute to section 8(d).",
  "Add '(at a time fixed by the Commission) within fifteen days after such notice' to the opportunity-for-hearing clause of L01.html line 85 and line 378, and to the back of cards.json LX2-c025, then re-run tools/check_pages.py --unit LX2. This is the same ruling that moved the 8(b) timing into the lesson.")

R("d-attrib-statute",
  "2.6 statute attribution: every statute-attributed claim span carries the conditions the statute states",
  "course/modules/LX/LX2/L01.html line 109 (third sentence of 15(d)(1), first paragraph of section 3 after the 13(a) sentence), lines 85 and 378 (8(d)); cards.json LX2-c025",
  "FAIL",
  "Re-verified from scratch. Fixed since round 9 and PASS now: 8(b) timing (L01.html line 84 vs statute 8(b); c010), and the 15(d)(1) third-sentence bank clause (L01.html line 111 and c016 vs statute). Still open: (1) L01.html line 109, claim span data-locator 'section 15(d)(1), third sentence', says the fiscal-year suspension applies to holders 'fewer than 300 persons' and omits the alternative that the statute states for a bank, a savings and loan holding company or a bank holding company ('1,200 persons', COMPS-1885.pdf 15(d)(1) third sentence, FOUND by statute_check.py). Line 111 of the same section states the alternative, so the two sentences disagree. (2) 8(d) timing omitted at L01.html lines 85 and 378 and cards.json LX2-c025, as in d-cards-021-030.",
  "L01.html line 109: add 'or, in the case of a bank, a savings and loan holding company or a bank holding company, 1,200 persons' to the claim, as line 111 does. L01.html lines 85 and 378 and cards.json LX2-c025: add the 8(d) timing clause quoted in d-cards-021-030. Re-run tools/check_pages.py --unit LX2.")

R("d-numbers",
  "numbers in prose, cards and labs (all numeric tokens)",
  "course/modules/LX/LX2/cards.json (all 100 cards); course/modules/LX/LX2/L01.html line 111; tests/labs/LX2/*.py run output",
  "PASS",
  "ledgers/LX2/scripts/LX2-d-r10/cards_mech.py output: 'numeric tokens absent from own lesson text: []' (every numeric token of every card appears in its own lesson's visible text). The round-9 gap ('1,200' absent from L01) is closed: L01.html line 111 contains '1,200 persons'. Lab numbers re-derived by me: run_labs output Part A 'hits = 9 of 24', 'hit rate = 3/8 (rounded 0.3750)', 'bias = 41/12 (rounded 3.4167)', with the printed errors summing to 82 (python: sum = 82, 82/24 = 41/12 = 3.41666...) and sum of |e| = 104 (104/24 = 13/3). Part D 'P(hit) = 44/117 (rounded 0.3761)' re-derived by hand: for each V in -4..4 the U count with -3 <= V-U <= 1 is 5 for V = -4..3 and 4 for V = 4, total 8x5+4 = 44 of 9x13 = 117. L03 run output: ratios 6/97 and 3/104, 3x97 = 291 < 6x104 = 624; largest ratio 21/37 (below threshold 2). L01 counts 10 states, 22 transitions, 2 sale states, 4 offer states, 0 both-duty states.")

R("d-cards-031-040",
  "2.7 card vs current lesson; 2.6 statute/opinion attribution (LX2-c031..c040)",
  "cards.json LX2-c031..c040; course/modules/LX/LX2/L02.html lines 56-112, 425-435, 445-459",
  "PASS",
  CARRY + " the cited spans contain none of lines 53, 465, 505, 528. Changed-line check: L02.html line 505 (the classify solution) and 528 (E2) are outside every cited span. Carried PASS.")

R("d-cards-041-050",
  "2.7 card vs current lesson; attribution (LX2-c041..c050)",
  "cards.json LX2-c041..c050; course/modules/LX/LX2/L02.html lines 106-107, 112-116; course/modules/LX/LX2/L03.html lines 58-78",
  "PASS",
  CARRY + " no changed line in the cited spans. Carried PASS.")

R("d-cards-051-060",
  "2.7 card vs current lesson; grades (LX2-c051..c060)",
  "cards.json LX2-c051..c060; course/modules/LX/LX2/L03.html lines 80-98, 338-354, 355, 362-371, 377-380, 391-395, 514-516",
  "PASS",
  CARRY_CARDS + " L03.html fully byte-identical. Also re-checked by me: c051 matches L03 key row 514 (grade T); c053 matches the L03 printed table (SIMULATED flow, grade C); c059 matches key row 516 and the printed 'traders flagged: 0 of 6' (grade C).")

R("d-cards-061-070",
  "2.7 card vs current lesson; attribution (LX2-c061..c070)",
  "cards.json LX2-c060..c070; course/modules/LX/LX2/L03.html lines 377-379; course/modules/LX/LX2/L04.html lines 63-111; attachment sr2602a1.txt",
  "PASS",
  CARRY + " L04.html byte-identical. The SR 26-2 attachment text is carried from round 9 (not re-fetched this round; see notes).")

R("d-cards-071-080",
  "2.7 card vs current lesson; theorem and definition cards (LX2-c071..c080)",
  "cards.json LX2-c071..c080; course/modules/LX/LX2/L04.html lines 114-146; expected block lines 345-365",
  "PASS",
  CARRY_CARDS + " L04.html byte-identical. Re-derived by me: E[e_t] = 1 (e_t = 1 + V_t - U_t, E[U]=E[V]=0); hit set -3 <= V-U <= 1 gives 44/117 (see d-numbers).")

R("d-cards-081-089",
  "2.7 card vs current lesson; attribution and grades (LX2-c081..c089)",
  "cards.json LX2-c081..c089; course/modules/LX/LX2/L04.html lines 56-111, 318-365; SR 26-2 letter; attachment SR2602a1.pdf; CFA pages",
  "PASS",
  CARRY + " L04.html byte-identical. External pages carried from round 9, see notes.")

R("d-cards-090-094",
  "2.7 card vs current lesson; lab-printed results (LX2-c090..c094)",
  "cards.json LX2-c090..c094 (c092 changed at line 706); course/modules/LX/LX2/L01.html lines 275-290 and 509-511; course/modules/LX/LX2/L03.html line 515",
  "PASS",
  "Re-verified from scratch (c092 changed this round). c092 back now reads 'Proposition 4.3 proves that a permitted sale implies a permitted offer in the model'; Proposition 4.3 (L01.html line 344-352) states that in every state where R5a permits a sale, R5c permits an offer, so the card matches. Lab output (run_labs and the twin run, exit 0): 'reachable from unregistered/not_listed: 10 of 10', 'states where both reporting duties apply: 0', 'states where a sale is permitted and an offer is not: 0' match c090-c092. c093 'events where entered != resting + 2 * traded + market cancelled + trader cancelled: 0' and c094 'tally from the event log disagrees with the book in 0 trader counts' match L03 twin output. Grades C with basis as in key rows L01.html 511 and L03.html 515.")

R("d-c058-grade",
  "grade and basis of LX2-c058 (SIMULATED flow)",
  "cards.json LX2-c058; course/modules/LX/LX2/L03.html line 515",
  "PASS",
  CARRY_CARDS + " Re-run: twin output 'events with a crossed book: 0' on the seed-2026 SIMULATED flow; basis names SIMULATED; grade C as key row L03.html 515.")

R("d-c059-grade",
  "grade and basis of LX2-c059 (demonstration threshold)",
  "cards.json LX2-c059; course/modules/LX/LX2/L03.html line 516",
  "PASS",
  CARRY_CARDS + " Re-run: 'traders flagged: 0 of 6', 'largest ratio 21/37' (21/37 < 2). Basis names SIMULATED and the demonstration value; grade C as key row 516.")

R("d-c085-grade",
  "grade and basis of LX2-c085 and LX2-c100 (SIMULATED path)",
  "cards.json LX2-c085, LX2-c100; course/modules/LX/LX2/L04.html Part A key rows 434",
  "PASS",
  "Re-verified from scratch by me: run output Part A 'hits = 9 of 24', 'hit rate = 3/8 (rounded 0.3750)', 'sum of errors = 82; sum / H = 41/12', 'bias = 41/12 (rounded 3.4167)'. Both cards name SIMULATED in basis and grade C as L04.html key row 434.")

R("d-cards-no-grade",
  "grade rule: a graded result carries a grade and a basis; definitions and assumptions carry none",
  "cards.json all 100 cards (grade counts: T 11, C 58, none 31)",
  "PASS",
  "Re-run this round: ledgers/LX2/scripts/LX2-d-r10/cards_mech.py: grades T 11, C 58, none 31. Every card with a statute or opinion statement (LX2-c001-c003 definitions excepted) or a lab result has grade C or T with a basis; the 31 ungraded cards are definitions, assumptions, remarks and misconceptions whose back is a lesson sentence, which matches BUILDER_RULES section 7. c053, c058, c059, c085, c090-c094, c100 grade C, which the lesson's key rows state. Note for the architect (not a row FAIL): build plan section 9 says lab-derived cards are grade T, but verifier rule 9 and the lesson key rows grade SIMULATED or lab-printed results C; cards follow the lesson.")

R("d-cards-schema",
  "card schema: id, lesson, front, back, basis or cite, grade",
  "course/modules/LX/LX2/cards.json",
  "PASS",
  "cards_mech.py: 100 cards, 100 unique ids LX2-c001..c100, lesson values L01-L04, every cite key present in references/references.json (keys: cfandcode, frb2026fed, gpo1983dirks, gpo1997united, gpondsecurities, gpondsecuritiesb); check_pages.py --unit LX2 PASS.")

R("d-cards-coverage",
  "coverage: each lesson's definitions, theorems, key results and misconceptions have cards",
  "cards.json lesson counts; course/modules/LX/LX2/L01.html..L04.html headings",
  "PASS",
  CARRY_CARDS + " Lesson headings unchanged (changed lines 84, 111, 115, 362 in L01 and 53, 465, 505, 528 in L02 are body text).")

R("d-dup-scan",
  "duplicate cards: fronts and backs across all 100 cards",
  "course/modules/LX/LX2/cards.json",
  "PASS",
  "cards_mech.py: dup fronts 0, dup backs 0 (re-run this round on the new pin).")

R("d-atomic-split",
  "atomic cards: one fact per card, split where two facts were joined",
  "cards.json LX2-c058, LX2-c085, LX2-c100, LX2-c090..c094",
  "PASS",
  CARRY_CARDS + " LX2-c058, c085, c100 carried; LX2-c090..c094 re-read this round (c092 changed) and each card states one printed result.")

R("d-attrib-opinions",
  "opinion attribution: holdings and quotes in LX2-c028..c043, c097 (Dirks, O'Hagan)",
  "cards.json LX2-c028..c043, LX2-c097; course/modules/LX/LX2/L02.html lines 55-115, 441-451, 561-617",
  "PASS",
  CARRY + " the changed L02 lines 53 and 465 lie outside 55-115 and 441-451; line 505 and 528 lie outside 561-617. The opinion texts (USREPORTS-463-646, USREPORTS-521-642) were not re-fetched this round; see notes.")

R("d-attrib-sr2026",
  "SR 26-2 attribution (LX2-c066..c069, c082..c084, c089)",
  "cards.json LX2-c066..c069, c082..c084, c089; course/modules/LX/LX2/L04.html lines 85-111",
  "PASS",
  CARRY + " L04.html byte-identical. The attachment text is carried from round 9, see notes.")

R("d-attrib-cfa",
  "CFA Code attribution (LX2-c064, c065, c080, c081, c087, c088)",
  "cards.json LX2-c064, c065, c080, c081, c087, c088; course/modules/LX/LX2/L04.html lines 56-82",
  "PASS",
  CARRY + " L04.html byte-identical. CFA pages carried from round 9, see notes.")

R("d-labs-run",
  "labs: run_labs, twins alone under python -I -W error, page code equals twin, expected block equals output",
  "tests/labs/LX2/lab-LX2-L01-1.py..L04-1.py; course/modules/LX/LX2/L01.html..L04.html expected blocks",
  "PASS",
  "Re-run this round: '.venv/bin/python tools/run_labs.py --unit LX2' exit 0, output 'run_labs LX2: PASS (7/7)' (ledgers/LX2/scripts/LX2-d-r10 has the scratch output path). Each L01-L04 twin run alone with .venv/bin/python -I -W error: exit 0, stderr 0 bytes, stdout 39, 25, 17, 48 lines. The twin outputs match the card numbers cited in d-numbers and d-cards-090-094.")

R("d-l02-quiz-scienter-p663",
  "L02 quiz (scienter and the p. 663 benefit) and key row",
  "course/modules/LX/LX2/L02.html lines 579, 615-631",
  "PASS",
  CARRY + " quiz lines 579 and 615-631 unchanged (changed lines 53, 465, 505, 528).")

R("d-l03-dodd-mifid",
  "L03 Dodd-Frank and MiFID II wording: named, content not stated; no source",
  "course/modules/LX/LX2/L03.html lines 358-371, 399, 514-518; references/references.json",
  "PASS",
  CARRY + " the lesson states nothing about either text. Registry check this round: grep -ci 'dodd|mifid' references/references.json = 0, references/authorities.yaml = 0. The card side of this topic is the separate FAIL row d-dodd-mifid-cards.")

R("d-dodd-mifid-cards",
  "plan section 9: cards for Dodd-Frank and MiFID II are not written until B1 and B2 are resolved",
  "course/modules/LX/LX2/cards.json LX2-c055, LX2-c056, LX2-c057; plans/LX2-build-plan.md section 0.3 (B1, B2), section 9, section 12 Q3-Q4",
  "FAIL",
  "Plan section 9: 'Cards for Dodd–Frank and MiFID II are not written until B1 and B2 are resolved.' B1 (no source for either text) and B2 (no allow-listed EU domain) are open: references/references.json has no Dodd or MiFID record (grep count 0), references/review_queue.json has one unrelated match, references/authorities.yaml has 0 matches for europa, eur-lex or esma, and the binding architect decisions (plan lines 619-620) say L03 names both with 'content not stated here' and that no legal source is admitted in this batch. Three cards take the two texts as their subject: LX2-c055 (misconception about naming them), LX2-c056 ('What does Lesson 3 state about the Dodd–Frank Act and MiFID II'), LX2-c057 ('Does the order pattern ... connect to the Dodd–Frank Act or MiFID II'). Each back matches L03.html Section 3 (lines 358-371), so card and lesson agree; the failure is the builder rule.",
  "Delete LX2-c055, LX2-c056 and LX2-c057, or replace each with a card on a Lab 1 or L03 fact that no card yet covers (re-number the ids so LX2-c001..c100 stays contiguous if check_pages requires it). Do not write any card on Dodd-Frank or MiFID II until the architect resolves B1 and B2 through tools/add_reference.py.")

R("d-dag",
  "DAG: concepts used outside the prerequisite closure",
  "tools/check_dag.py --unit LX2; course/modules/LX/LX2/*.html",
  "PASS",
  "Re-run this round: '.venv/bin/python tools/check_dag.py --unit LX2' exit 0, output 'check_dag LX2: PASS'. Cards carry no concept links.")

R("d-notation",
  "notation: every symbol in cards vs notation/notation.json",
  "course/modules/LX/LX2/cards.json symbols (G, R, X, C_m, C_t, H, n, q, U_t, V_t, y_t, e_t, h_t); notation/notation.json",
  "PASS",
  "notation/notation.json registers T, Phi, gamma_3, gamma_4, R^ast, R^{e ast}, R_f, Q only. Grep this round of cards.json and L01-L04 for those symbols: none used in cards; 'T' appears only as the grade letter; the cards' local letters (R for resting shares in LX2-c051, G, X, C_m, C_t, H, q, U_t, V_t, y_t, e_t, h_t) are each defined in the card or the lesson where used, as notation section 'letters whose meaning is conventionally local' allows.")

R("d-process-banned",
  "no process words or banned phrases in learner text",
  "course/modules/LX/LX2/L01.html..L04.html text (changed lines 84, 111, 115, 362 in L01; 53, 465, 505, 528 in L02); cards.json",
  "PASS",
  "Re-run this round on the full text of L01-L04 and cards.json: no 'twin', 'builder', 'verifier', 'ledger', 'rubric', 'round N', 'TODO', 'TBD', 'lorem', 'for brevity', 'beyond the scope', 'it is important to note', 'clearly', 'obviously'. Only matches are code, math ellipses and the statute word 'process' in LX2-c066 (quoted SR 26-2 definition). The changed L02 text removed 'twin' from learner text (E2 and the Pr2 solution now say 'Lab 1's code').")

R("d-gates-structure",
  "gates: check_pages, check_dag, check_projects, verify_refs, page_smoke for LX2",
  "tools/check_pages.py --unit LX2; tools/check_dag.py --unit LX2; tools/check_projects.py --unit LX2; tools/verify_refs.py --offline; tools/page_smoke.py --unit LX2",
  "PASS",
  "Run this round, exit codes and outputs: check_pages LX2: PASS (exit 0); check_dag LX2: PASS (exit 0); check_projects LX2: PASS (exit 0); verify_refs --offline: 'offline integrity: 560 entries, 0 problems' (exit 0); page_smoke --unit LX2: PASS for L01-L04, project, index, concepts, review (exit 0). Outputs in ledgers scratch .../scratch-LX2-d-r10/*.out. Also ruff check . PASS, ruff format --check PASS (553 files), mypy --no-incremental PASS (385 files), pytest tests/test_page_checks.py tests/test_page_smoke.py PASS. 'pytest -k LX2 tests/labs' collected no tests (exit 5); the labs are run by run_labs.py instead.")

R("d-grade-key-consistency",
  "each card grade matches its lesson key row",
  "cards.json grades; course/modules/LX/LX2/L01.html key rows 509-511; L03.html key rows 514-516; L04.html key rows 434-437",
  "PASS",
  "Re-verified this round: L01 key row 509 (T) vs c017 (T); 510 (T) vs c018, c019 (T); 511 (C, Lab 1 output) vs c090-c092 (C). L03 514 (T) vs c051 (T); 515 (C, SIMULATED) vs c093, c094 (C); 516 (C) vs c059 (C). L04 434 (C) vs c085, c100 (C); 435 (T) vs c086 (T); 436 (T) vs c076, c077 (T); 437 (T) vs c078, c079 (T).")

R("d-delta-read",
  "delta since the round-9 pin c93dd52 read in full, every hunk",
  "git diff c93dd52 00a8479 -- course/modules/LX/LX2/ (files: L01.html, L02.html, cards.json, index.html, project.html)",
  "PASS",
  "Hunks read in full (new-file line numbers): L01.html 84 (8(b) timing, quote checked against COMPS-1884 8(b)), 111 (15(d)(1) third sentence, bank clause, checked against COMPS-1885), 115 (Section 4 lead-in sentence; no card cites the changed wording), 362 (emerging growth companies; 2(a)(19), 6(e)(1), 5(d) checked). L02.html 53 (scope note, no card cites it), 465 (problem set lead, no card), 505 (Pr2 solution wording, no card), 528 (E2 wording, no card). cards.json 706 (LX2-c092 back, verified against L01 Proposition 4.3). index.html and project.html changes are outside this slice (not read for claims beyond the cards).")

R("d-r2-lesson-delta",
  "L02 problem E2 and E3 text and solution after the delta",
  "course/modules/LX/LX2/L02.html lines 527-539 (E2 line 528 changed)",
  "PASS",
  "Re-read this round. E2 now says 'Copy Lab 1's code to a scratch file and change P2's tipper benefit to reputational.' The predicted outputs match the classifier: P2 with a reputational benefit passes every tippee check (its only failing element was the benefit, 'fails: tipper's personal benefit (none)' in the twin output), so the row fires and the summary count goes from four of eight to five of eight. E3 unchanged.")

R("d-l01-line63-s3-defined",
  "L01 line 63 vs line 96 and c005 (term 'national securities exchange')",
  "course/modules/LX/LX2/L01.html lines 63 and 96; cards.json LX2-c005",
  "PASS",
  CARRY + " lines 63 and 96 unchanged; c005 unchanged.")

R("d-l01-line88-spacing",
  "L01 line 88 wording and spacing",
  "course/modules/LX/LX2/L01.html line 88",
  "PASS",
  CARRY + " line 88 unchanged (changed lines 84, 111, 115, 362 only).")

R("d-grade-legend",
  "grade legend lines in L01-L04",
  "course/modules/LX/LX2/L01.html..L04.html lines 42-49",
  "PASS",
  CARRY + " lines 42-49 unchanged in all four lessons.")

R("d-l04-quiz-five-places",
  "L04 quiz (five places) lines 508-518",
  "course/modules/LX/LX2/L04.html quiz lines 508-518",
  "PASS",
  CARRY_CARDS.replace("cards.json entries byte-identical since c93dd52;", "") + " L04.html byte-identical.")

R("d-l04-line82-locator",
  "L04 line 82 locator",
  "course/modules/LX/LX2/L04.html line 82",
  "PASS",
  "Carried from round 9 (course/modules/LX/LX2/L04.html byte-identical since the pin c93dd52): L04.html line 82 unchanged.")

R("d-quote-fidelity",
  "quotation fidelity: every quoted statute phrase in L01 (lines 51-111, 134, 360-382) and L02 spans carries the exact words",
  "course/modules/LX/LX2/L01.html lines 51-111, 134, 360-382; L02.html lines 56-112, 445-448, 507-524, 573-578",
  "PASS",
  "Re-verified from scratch this round for all quoted phrases in L01 lines 80-86, 100-106, 111, 362, 378: each quotation FOUND in the normalised COMPS-1884 or COMPS-1885 text (ledgers/LX2/scripts/LX2-d-r10/statute_check.py, and the phrase list in the run: 6(a), 5(a), 5(c), 8(a), 8(b), 8(d) 'suspending the effectiveness of the registration statement' (a page header splits the words), 'the stop order shall cease to be effective', 12(a), 12(b), 12(d) both sentences, 13(a), 15(d)(1) first, second and third sentences, 6(e)(1), 5(d), 8(e), 2(a)(19)). Quotation marks are accurate. The omissions of statutory conditions (8(d) timing, 15(d)(1) bank clause at line 109) are not quote errors and are recorded in d-attrib-statute. L02 spans carried.")

R("d-l03-hypothesis-claims",
  "L03 hypothesis claims (line 103, line 355)",
  "course/modules/LX/LX2/L03.html lines 103, 355",
  "PASS",
  CARRY + " lines 103 and 355 unchanged.")

R("d-l04-e3-arithmetic",
  "L04 Problem E3 arithmetic and Section 5 (lines 411, 373)",
  "course/modules/LX/LX2/L04.html lines 373, 411",
  "PASS",
  CARRY + " L04.html byte-identical.")

R("d-l01-sec5-statute",
  "L01 section 5 (lines 355-366) statute statements",
  "course/modules/LX/LX2/L01.html section 5 lines 355-366 (changed line 362)",
  "PASS",
  "Re-verified this round for the changed line 362: 'Emerging growth company is a term the statute defines in section 2(a)(19)' FOUND in COMPS-1884 normalised text ('(19) The term emerging growth company means an issuer ...' after SEC. 2.), 6(e)(1) quote FOUND, 5(d) communications clause FOUND ('qualified institutional buyers or institutions that are accredited investors'), 8(e) quote FOUND. Lines 359 (8(a), 12(d) quotes), 360 (exempted security), 363 (5(c), 8(e)), 364 (15(d)(1) third sentence) re-read: quotes FOUND; the 15(d)(1) bank clause is the omission recorded in d-attrib-statute line 109, not repeated here.")

R("d-cards-096-097",
  "LX2-c096 (15(d)(1) third sentence, section 3) and LX2-c097 (L02 section 3 Assumption A1)",
  "cards.json LX2-c096, LX2-c097; course/modules/LX/LX2/L01.html section 3 (line 111); course/modules/LX/LX2/L02.html lines 85-86",
  "PASS",
  "c096 re-verified this round: 'No. The third sentence excludes that fiscal year from the suspension' matches the statute ('other than the fiscal year within which such registration statement became effective') and L01.html line 111. c097 carried: L02.html lines 85-86 byte-identical; Assumption A1 of §3 (L02.html line 496 reading) says 'none' means no direct or indirect personal benefit.")

R("d-cards-098-099",
  "LX2-c098 (Lab 1 Assumption A2) and LX2-c099 (Assumption A3)",
  "cards.json LX2-c098, LX2-c099; course/modules/LX/LX2/L02.html lines 119-125",
  "PASS",
  CARRY + " lines 119-125 unchanged. A2 and A3 wording (L02.html lines 122-123) re-read this round.")

R("d-card-labels-current",
  "card labels and lesson text current (LX2-c017..c019, c074..c078, c086; L01 lines 319-348; L04 lines 123-143)",
  "cards.json LX2-c017..c019, c074..c078, c086; course/modules/LX/LX2/L01.html lines 319-348; course/modules/LX/LX2/L04.html lines 123-143",
  "PASS",
  CARRY_CARDS + " L01.html lines 319-348 unchanged (changed lines 84, 111, 115, 362 lie outside). c017-c019 re-verified this round (see d-cards-011-020).")

R("d-c054-hypothesis",
  "LX2-c054 hypothesis wording (L03 lines 80-84, 393-395)",
  "cards.json LX2-c054; course/modules/LX/LX2/L03.html lines 80-84, 393-395",
  "PASS",
  CARRY + " L03.html byte-identical.")

R("d-cards-095",
  "LX2-c095 (8(b) effective date at the later of 8(a) and the declaration)",
  "cards.json LX2-c095; course/modules/LX/LX2/L01.html section 5 Timing bullet (line 359) and line 84",
  "PASS",
  "Re-verified this round: statute 8(b) 'the registration shall become effective at the time provided in subsection (a) or upon the date of such declaration, whichever date is the later' FOUND (COMPS-1884 normalised text). L01.html line 359 says the model treats the declaration as an event with no date. The changed line 84 adds the notice and hearing timing, which c095 does not state, so the card remains exact.")

R("d-c100-new",
  "LX2-c100 (new card, Part A bias 41/12)",
  "cards.json LX2-c100; tests/labs/LX2/lab-LX2-L04-1.py Part A printed block; course/modules/LX/LX2/L04.html Part A expected block",
  "PASS",
  CARRY_CARDS + " L04.html byte-identical. Re-derived: 'bias = 41/12 (rounded 3.4167)' and 'sum of errors = 82' by my sum of the twin's printed errors (82/24 = 41/12 = 3.41666..., half-up to 3.4167).")

frag = {
  "unit": "LX2",
  "slice": "d",
  "round": 10,
  "verifier": "Claude Haiku 5.5, independent verifier for LX2-d, round 10 (did not build LX2; shares no context with the builders)",
  "pin": "00a84795f276456fce19d4181373cc4efba11a36",
  "base": "c93dd526025c6dffd34c54cd2c89eb62a890f885 (round-9 pin)",
  "checkout": "/Users/billyribeiro/.fanout/wt/verifyE10-LX2-d",
  "scratch": "/Users/billyribeiro/.fanout/scratch-LX2-d-r10 (statute PDFs re-fetched by plain curl this round, sha256 identical to round 9; normalised text src/c1884.norm.txt and src/c1885.norm.txt)",
  "verified_at": "2026-11-05T08:15:00+00:00",
  "verdict": "FAIL",
  "rows": rows,
  "mutants": [],
  "registry_flags": ["B1/B2 open: references/references.json has no Dodd-Frank or MiFID II record (grep count 0); see d-dodd-mifid-cards"],
  "freshness_flags": [],
  "notes": [
    "Delta c93dd52..00a8479 read in full (d-delta-read). Changed subjects re-verified from scratch: L01 lines 84, 111, 115, 362; L02 lines 53, 465, 505, 528 (no card cites them); cards.json LX2-c092.",
    "Round-9 FAIL rows: d-cards-001-010 and d-cards-011-020 and d-numbers are now PASS (the lesson gained the 8(b) timing at line 84 and the 1,200-persons clause at line 111). d-cards-021-030 and d-attrib-statute stay FAIL: the 8(d) hearing timing (fifteen days) is omitted at L01 lines 85 and 378 and in LX2-c025, and the bank clause is omitted at L01 line 109.",
    "New FAIL d-dodd-mifid-cards: plan section 9 forbids cards on Dodd-Frank and MiFID II until B1 and B2 are resolved; LX2-c055, c056, c057 are such cards.",
    "Observation, not a row: plan section 9 says lab-derived cards are grade T; verifier rule 9 and the lesson key rows grade SIMULATED or lab-printed results C, and the cards follow the lesson key rows.",
    "Carried rows carry the round-9 PASS only where the cited lesson and card spans are byte-identical since c93dd52 (L03.html and L04.html are byte-identical; L02.html and cards.json are identical outside the lines listed above).",
    "Mutation testing: not applicable. The slice has no grader; ledgers/LX2/mutants was not written to. run_graders and mutate_graders were not run for this slice.",
  ],
  "summary": {},
}
pass_n = sum(1 for r in rows if r["status"] == "PASS")
fail_n = sum(1 for r in rows if r["status"] != "PASS")
frag["summary"] = {
  "slice": "LX2-d (all 100 cards.json cards against L01-L04)",
  "verdict": "FAIL",
  "rows": len(rows), "pass": pass_n, "fail": fail_n, "unverifiable": 0,
  "mutants": "0/0 (no grader in slice)",
  "failing_rows": [r["id"] for r in rows if r["status"] != "PASS"],
}
import os
out = "/Users/billyribeiro/.fanout/wt/verifyE10-LX2-d/ledgers/LX2/LX2-d.json"
os.makedirs(os.path.dirname(out), exist_ok=True)
json.dump(frag, open(out, "w"), indent=2, ensure_ascii=False)
print("rows", len(rows), "pass", pass_n, "fail", fail_n)
