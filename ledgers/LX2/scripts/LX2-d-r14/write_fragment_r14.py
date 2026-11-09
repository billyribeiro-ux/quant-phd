"""Writes the round-14 fragment ledgers/LX2/LX2-d.json (rows, mutants, flags). Evidence strings cite the
scripts under ledgers/LX2/scripts/LX2-d-r14/ and the scratch outputs they print."""

import json
from datetime import UTC, datetime

CARRY = (
    "Carried from round 13 (cited card objects JSON-identical to e919577b per card_delta_r14.out, and the cited "
    "lesson files byte-identical since e919577b): "
)
S = "ledgers/LX2/scripts/LX2-d-r14/"
rows = []


def row(rid, check, location, status, evidence, fix=None):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    rows.append(r)


row(
    "d-cards-001-010",
    "2.7 card vs current lesson; 2.6 statute attribution (LX2-c001..c010)",
    "course/modules/LX/LX2/cards.json LX2-c001..c010; course/modules/LX/LX2/L01.html sections 2-5 (stripped text: scratch-LX2-d-r14/scratch-LX2-d-r14-L01.txt, whole file)",
    "PASS",
    "Read every card in full against L01 §2 (Def 2.1, quotes of 6(a), 5(a), 5(c), 8(a), 8(b), 8(d)), §3 and §4 (R5c, A1). c002 and c005 match Def 3.1 and the 'national securities exchange' sentence. c004 back matches §2's reading of 'in effect' and the statute check that section 2 has no 'in effect' definition (statute_cfa_attachment_checks_r14.py: ABSENT inside section 2). c007 and c010 match the statute text (statute_cfa_attachment_checks_r14.py: FOUND s5(c) clause list; s8(b) ten days notice and hearing). c008 restates R5c (model status filed or effective). c003 has no locator now, so no locator can disagree with the statute. The lesson-side defect is row d-l01-sec2-registration-ungraded.",
)
row(
    "d-cards-011-020",
    "2.7 card vs current lesson; 2.6 statute (LX2-c011..c020)",
    "cards.json LX2-c011..c020; L01.html lines 96-134, 470-476",
    "PASS",
    CARRY + "statute quotes for c011-c016 re-found this round in c1884/c1885 by statute_cfa_attachment_checks_r14.py (FOUND 12(a), 12(b), 12(d) thirty days, 12(d) withdrawn or stricken, 15(d)(1) first sentence, second sentence, third sentence 300 and 1,200).",
)
row(
    "d-cards-021-030",
    "2.7 card vs current lesson; 2.6 statute and Model (LX2-c021..c030)",
    "cards.json LX2-c021..c030 (c025, c027 changed since e919577b); L01.html Section 4, Section 5, Section 6, Lab 1 printed output",
    "PASS",
    "Fresh read. c021 (22 = 6x2 + 2x5) matches §4 and P1; c023 (2 sale-permitted states) matches the lab table (run-lab-LX2-L01-1.out: effective rows sale yes); c024 'filed row prints offer yes and sale no' and c025 'stop_order rows print offer no and sale no' match the printed table; c026 matches §6 (6(a) vs 12(b)); c027 matches §4 readings R13/R15 and Prop 4.2; c025 wording of 8(d) matches the statute (statute_cfa_attachment_checks_r14.py: FOUND 'issue a stop order suspending the effectiveness of the registration' and 'fifteen days'). Lab rows reproduced by tests/labs/LX2/lab-LX2-L01-1.py (exit 0; re-run identical to the first run, see d-labs-run).",
)
row(
    "d-attrib-statute",
    "2.1 attribution; 2.6 statute locators (L01 claim spans)",
    "course/modules/LX/LX2/L01.html line 109 (claim span data-locator 'section 15(d)(1), third sentence'), line 111, line 565, line 562",
    "PASS",
    CARRY + "L01.html byte-identical; the statute quotations behind them are re-found this round (statute_cfa_attachment_checks_r14.py, all 1934 s15(d)(1), s12 and s8 phrases FOUND).",
)
row(
    "d-cards-031-040",
    "2.7 card vs current lesson; 2.1 attribution (LX2-c031..c040)",
    "cards.json LX2-c031..c040; course/modules/LX/LX2/L02.html lines 56-112, 425-435",
    "PASS",
    CARRY + "card objects c031-c040 unchanged. Quotations in c031, c032, c034, c035, c037 re-found this round by the quote script (ledgers/LX2/scripts/LX2-d-r14/quote_check_cards_r14.py, output scratch-LX2-d-r14/quotes_cards_r14.out) and their printed pages by page_locate_r14.py.",
)
row(
    "d-cards-041-050",
    "2.7 card vs current lesson (LX2-c041..c050)",
    "cards.json LX2-c041..c050; course/modules/LX/LX2/L02.html lines 119-125, 441-451; L03.html Section 1 (c044-c050)",
    "PASS",
    CARRY + "c041 quote (Dirks p. 662) and c043 quote (O'Hagan p. 655 n. 7) re-found this round (quote_check_cards_r14.py; page_locate_r14.py: Dirks 662, O'Hagan 655 n.7). c044-c050 match Definitions 1.1, 1.3, Remark 1.2 and Assumption A1 of L03 (read in full this round).",
)
row(
    "d-cards-051-060",
    "2.7 card vs current lesson; 2.4 Proposition 2.2 hypotheses (LX2-c051..c060; c055-c057 absent)",
    "cards.json LX2-c051, c053, c054, c058, c059; course/modules/LX/LX2/L03.html Section 2 (Prop 2.2, Remarks 2.3-2.4), Lab 1 output",
    "PASS",
    "c051 now carries A1's 'each at its arrival quantity' and reproduces G = R + 2X + C_m + C_t exactly as Prop 2.2 states it. c053 cites R2 ('probabilities per selected turn') and the printed rows 3/104 (trader 1, rate 10) and 6/97 (trader 0, rate 5): run-lab-LX2-L03-1.out lines 10-11. The exactness claim 3 x 97 = 291 < 624 = 6 x 104 is recomputed in card_arithmetic_r14.py. c054 matches Prop 2.2 and Remark 2.3. c058 and c059 match run-lab-LX2-L03-1.out ('events with a crossed book: 0'; 'traders flagged: 0 of 6'; largest ratio 21/37). c055-c057 are absent (no gap in the id scheme is a defect because the ids are unique).",
)
row(
    "d-cards-061-070",
    "2.7 card vs current lesson; 2.2 numbers (LX2-c061..c070)",
    "cards.json LX2-c061..c070 (c064, c065 changed); course/modules/LX/LX2/L03.html Section 4; L04.html Sections 1-4",
    "PASS",
    "c060-c063 match L03 §4 (broker, venue, latency, ratio counts events; R1 for reprice vs withdraw). c064 quotation re-found in cfa-iii-a.norm.txt (FOUND 'often imposed by law or regulation...'), with the Standard III(A) Guidance subheading; c065 matches Standard VI(A) Guidance first paragraph (cfa-vi-a.norm.txt, FOUND). c066-c070 match the attachment: model definition and spreadsheet exclusion on p. 3 (page image read), model risk on p. 3, model-risk management pp. 1-2 (the quote spans the page break; the extracted text's '1' is the page footer, page 1 image), outcomes analysis p. 9 (page image read). Hit threshold and definitions match §4 Definition 4.1.",
)
row(
    "d-cards-071-080",
    "2.7 card vs current lesson; 2.4 Theorems 4.2-4.3, Prop 4.4 hypotheses (LX2-c071..c080)",
    "cards.json LX2-c071..c080 (c071, c072, c077, c078, c079, c080 changed); course/modules/LX/LX2/L04.html Sections 1, 4",
    "PASS",
    "Definitions 4.1 (c071-c073) match the lesson and the lab's round_half_away (lab code: floor(|x|*10^4 + 1/2)). A1 (c074) is y_t = 100 + U_t, yhat_t = 101 + V_t with U in -6..6 and V in -4..4 (the lab's REALISED_SPREAD = 6, FORECAST_SPREAD = 4). A2 (c075) matches the lesson's sentence. Theorem 4.2 (c076) has the lesson's hypotheses (n >= 1, 0 <= b1 <= b2). Theorem 4.3 (c077) has the lesson's bound and equality case, and the proof's P/N argument is consistent. Prop 4.4 (c078, c079) matches the proof: E[e_t]=1 (lab Part D prints E[error] = 1), P(hit)=44/117 (card_arithmetic_r14.py: 44 of 117 pairs; 8*5+4=44). c080 matches the Standard III(A) text (cfa-iii-a.norm.txt FOUND).",
)
row(
    "d-cards-081-089",
    "2.7 card vs current lesson; 2.1 attribution; 2.2 numbers (LX2-c081..c089)",
    "cards.json LX2-c081..c089 (c084, c086, c088 changed); course/modules/LX/LX2/L04.html Sections 1-3, 5-6; Lab 1 Part C output",
    "PASS",
    "c081 matches Standard III(A) Guidance (FOUND 'must comply with any legally imposed fiduciary duty'; 'neither impose such a legal responsibility'). c082 and c083 match the letter (sr2602.htm: 'supersedes and replaces SR letter 11-7 ... and SR letter 21-8'; Applicability 'over $30 billion in total assets regulated by the Federal Reserve'). c084: whole-word search of the attachment (att_raw.txt) and of the letter text finds 0 matches for 'hit' and 0 for 'bias' (statute_cfa_attachment_checks_r14.py). c086: Part C prints bias 0 and hit rate 0 for errors +3,-3,+3,-3 (run-lab-LX2-L04-1.out lines 41-44); MAE 3 recomputed (card_arithmetic_r14.py). c087 matches Standard VI(A) and Example 3 (cfa-vi-a.norm.txt: Example 3 heading, 'at minimum, Fargmon must disclose', 'best practice is to avoid the conflict by asking his employer to assign another analyst'). c088 matches Standard III(A) quotations. c089 matches the attachment p. 2 quote and footnote 1 (page 2 image read).",
)
row(
    "d-cards-090-094",
    "2.5 lab output vs card; 2.7 card vs lesson (LX2-c090..c094)",
    "cards.json LX2-c090..c094 (c094 changed); run-lab-LX2-L01-1.out, run-lab-LX2-L03-1.out (regenerated this round)",
    "PASS",
    "c090 ('reachable from unregistered/not_listed: 10 of 10'), c091 ('states where both reporting duties apply: 0'), c092 ('states where a sale is permitted and an offer is not: 0') match the L01 lab printout exactly. c093 (identity failures 0) matches run-lab-LX2-L03-1.out line 4 'events where entered != resting + 2 * traded + market cancelled + trader cancelled: 0'. c094 matches 'tally from the event log disagrees with the book in 0 trader counts'. c094 says the lab 'recomputes' the tally where L03 says 'rebuilds': same meaning, not a fact conflict (noted, not a fail).",
)
row(
    "d-cards-095",
    "2.7 card vs current lesson (LX2-c095)",
    "cards.json LX2-c095; L01.html line 84 and Section 5 (timing)",
    "PASS",
    CARRY + "card object unchanged; statute 8(b) 'whichever date is the later' re-found this round (statute_cfa_attachment_checks_r14.py FOUND).",
)
row(
    "d-cards-096-097",
    "2.7 card vs current lesson (LX2-c096, LX2-c097)",
    "cards.json LX2-c096, LX2-c097; L01.html section 3; L02.html Section 3 Assumption A1",
    "PASS",
    CARRY + "statute 15(d)(1) third sentence 'other than the fiscal year within which such registration statement became effective' re-found this round (FOUND).",
)
row(
    "d-cards-098-099",
    "2.7 card vs current lesson (LX2-c098, LX2-c099)",
    "cards.json LX2-c098, LX2-c099; L02.html lines 119-125 (Assumptions A2, A3)",
    "PASS",
    CARRY + "A2 and A3 text of L02 identical; the quote 'as quoted at p. 652' for the temporary-fiduciary clause re-found in ohagan.txt (page_locate_r14.py: 652).",
)
row(
    "d-cards-101-103",
    "2.7 card vs current lesson; 2.6 no provision invented (LX2-c101..c103, new since e919577b)",
    "cards.json LX2-c101, LX2-c102, LX2-c103; course/modules/LX/LX2/L03.html §3 Definitions 3.1 and 3.2, §5 misconception 3",
    "PASS",
    "Each card matches the lesson: Definition 3.1 and 3.2 name the Act and the directive and state no provision, scope or duty; the registry holds no Dodd-Frank or MiFID entry (python -I scan of references/references.json: no key or title match for dodd, frank, mifid; the only 'dodd' hit is a review_queue entry, not the registry), so 'no primary text' and 'no provision is cited' are true. c103 matches the third misconception of L03 §5.",
)
row(
    "d-numbers",
    "2.2 numbers in cards: computed, quoted or derived; every card number in its lesson",
    "cards.json (all 100 cards); L01-L04 stripped text; run-lab-LX2-L0{1,3,4}-1.out",
    "PASS",
    "ledgers/LX2/scripts/LX2-d-r14/card_numbers_r14.py over all 100 cards: 0 number tokens absent from every LX2 lesson text and lab output (scratch-LX2-d-r14/card_numbers_r14.out). Recomputed in ledgers/LX2/scripts/LX2-d-r14/card_arithmetic_r14.py (scratch-LX2-d-r14/card_arithmetic_r14.out): 44/117 = 0.3761; 9/24 = 3/8 = 0.3750; 82/24 = 41/12 = 3.4167; 0 and 0 and MAE 3 for Part C; 3/104 = 0.0288, 6/97 = 0.0619; largest 21/37 = 0.5676; E[e] = 1; Var(e) = 62/3 and gap/se = 2.604 (L04 E3 'about 2.60').",
)
row(
    "d-attrib-opinions",
    "2.1 attribution; quotes and pinpoints (LX2-c028..c043)",
    "cards.json LX2-c028..c043; course/modules/LX/LX2/L02.html lines 55-115, 441-451, 561-617; scratch-LX2-d-r11/src/dirks.txt and ohagan.txt",
    "PASS",
    "ledgers/LX2/scripts/LX2-d-r14/quote_check_cards_r14.py: every curly-quoted passage in c029, c031, c032, c034, c035, c037, c039, c041, c043 is FOUND verbatim in the opinion text (quotes_cards_r14.out). page_locate_r14.py gives the printed page of each: Dirks n.6 651; 654 (mere possession, fiduciary relationship); 659 (derivative); 660 (tippee test); 662 (purpose; absent personal gain); 663 (personal benefit; n.23 scienter); 664 (gift; question of fact; not always easy); 672 (dissent); 676 n.13. O'Hagan: 652 (classical quote, misappropriation holding, 'in connection with'); 653 n.5 (not an insider; escape); 655 (disclosure to source; n.7); 656 (uses the information; does not catch all; coincide); 679, 680 (dissents). The O'Hagan classical-theory and misappropriation passages match the lesson's quotations word for word (whitespace and curly quotes normalised).",
)
row(
    "d-attrib-sr2026",
    "2.1 attribution; 2.2 numbers and locators (LX2-c066..c069, c082..c084, c089)",
    "cards.json LX2-c066..c069, c082..c084, c089; course/modules/LX/LX2/L04.html Section 3; scratch-LX2-d-r11/src/SR2602a1.pdf pages 1-3 and 8-9 (page images read); sr2602.htm; att_raw.txt",
    "PASS",
    "Page images read: p. 1-2 (the 'responsible for adopting model risk management practices' sentence runs from p. 1 to p. 2), p. 2 (enforceable-standards sentence and footnote 1), p. 3 (model definition, model risk definition), p. 8 (Conceptual Soundness), p. 9 (Outcomes Analysis: 'compares model outputs to corresponding real-world outcomes...'). The c068 quotation is not found contiguously in the extracted text only because the page footer '1' sits between 'model' and 'risk'; the page image confirms the words. Whole-word search of the attachment and of the letter finds no 'hit' or 'bias' (statute_cfa_attachment_checks_r14.py). Supersedes and Applicability lines of the letter match c082 and c083.",
)
row(
    "d-attrib-cfa",
    "2.1 attribution; quotes and locators (LX2-c064, c065, c080, c081, c087, c088)",
    "cards.json LX2-c064, c065, c080, c081, c087, c088; scratch-LX2-d-r11/src/cfa-iii-a.norm.txt, cfa-vi-a.norm.txt; course/modules/LX/LX2/L04.html Sections 1-2",
    "PASS",
    "statute_cfa_attachment_checks_r14.py: FOUND for every quotation and paraphrase cited (III(A) duty of loyalty; Guidance 'often imposed by law or regulation'; 'must comply with any legally imposed fiduciary duty'; 'neither impose such a legal responsibility'; VI(A) definition, the standard, 'best practice is to avoid actual conflicts', Example 3 heading, 'At minimum, Fargmon must disclose', 'best practice is to avoid the conflict by asking his employer to assign another analyst to draft the follow-up report'). The Code text is the saved 2024 HTML of the CFA Institute page (cfa-*.html) read as text.",
)
row(
    "d-cards-090-094-lab-basis",
    "2.5 lab output named in basis (LX2-c023, c038, c053, c058, c059, c085, c093, c094, c100)",
    "cards.json basis fields; run-lab-LX2-L01-1.out, run-lab-LX2-L02-1.out, run-lab-LX2-L03-1.out, run-lab-LX2-L04-1.out",
    "PASS",
    "Each basis names the lab output it reads and the output says so: c023 (L01 state table: 2 sale-permitted), c038 (L02 fired P1, P3, P4, P6; not fired P2, P5, P7, P8), c053, c058, c059, c093, c094 (L03 run), c085, c100 (L04 Part A: hits 9 of 24, bias 41/12, rounded 3.4167 and 0.3750). The SIMULATED/HYPOTHETICAL labels are present in those basis strings where the lab is SIMULATED (seed 2026, seed 20261103) or HYPOTHETICAL (L02 patterns). c086 is graded T on a hand-built path (lab Part C is 'hand-built, with fixed values' by its docstring), which is a computation on printed errors, so T is consistent with rule 9.",
)
row(
    "d-cards-no-grade",
    "2.7 grade and citation coverage",
    "cards.json (100 cards)",
    "PASS",
    "python -I count: 31 cards carry no grade, 69 carry a grade; every card has a cite list or a basis (no card with neither). Every grade C or T card has a cite or basis (check_pages.py line 394 rule passes, see d-cards-schema).",
)
row(
    "d-cards-schema",
    "2.7 card schema (tools/check_pages.py cards.json rules)",
    "cards.json; tools/check_pages.py (check_cards)",
    "PASS",
    "tools/check_pages.py --unit LX2: 'check_pages LX2: PASS' (unique ids LX2-c001..c103 with gaps c055-c057 that are absent, valid lessons, valid grades, cite keys exist, grade-C result has cite or basis). Registry keys: cfandcode, frb2026fed, gpo1983dirks, gpo1997united, gpondsecurities, gpondsecuritiesb all present in references/references.json (entries list), all verified_by 'issuer'.",
)
row(
    "d-cards-coverage",
    "2.7 coverage of lesson definitions, propositions, assumptions, misconceptions, key results by cards",
    "cards.json vs L01-L04",
    "PASS",
    "Per lesson: L01 32 cards (Defs 2.1, 3.1; A1; Props 4.1-4.3; states and transitions; misconceptions 4; Lab 1 outputs), L02 19 (Defs 2.1, 3.1, 4.1; misconceptions 4; A1-A3; Lab 1 output), L03 22 (Defs 1.1, 1.3; Remark 1.2; A1; Prop 2.2; Remarks 2.3-2.4; misconceptions 3; Lab 1 outputs; Defs 3.1, 3.2), L04 27 (Defs 1.1, 2.1, 3.1-3.3, 4.1; A1, A2; Thms 4.2, 4.3; Prop 4.4; misconceptions 4; Lab 1 outputs). No lesson definition, proposition, assumption or misconception was found without a card.",
)
row(
    "d-dup-scan",
    "2.7 duplicate cards",
    "cards.json",
    "PASS",
    "python -I: 100 distinct ids; 0 duplicate fronts; 0 duplicate backs. Pairs that test the same lesson result from different angles (c017 vs c090, c018 vs c091, c019 vs c092) have different questions (the proposition's conclusion vs the lab's printed count) and are not duplicates.",
)
row(
    "d-atomic-split",
    "2.7 one fact per card",
    "cards.json LX2-c041, c053, c058, c090..c094, c100",
    "PASS",
    "Multi-clause cards (c041: a tip to a friend plus the P4 gift contrast; c053: the ratio plus the exact comparison) each answer one misconception question and their clauses support that one answer. The other lab-output cards test one printed value each.",
)
row(
    "d-labs-run",
    "2.5 labs: run, deterministic, twin under python -I -W error",
    "tests/labs/LX2/lab-LX2-L01-1.py, L02-1, L03-1, L04-1; tools/run_labs.py --unit LX2",
    "PASS",
    "run_labs.py --unit LX2: 'run_labs LX2: PASS (7/7)'. Each of the four lab twins run under python3 -I -W error: exit 0. All four lab twins' re-run outputs are identical to the first run (diff, all 'deterministic'). Outputs in scratch-LX2-d-r14/run-lab-LX2-L0{1,2,3,4}-1.out.",
)
row(
    "d-l03-dodd-mifid",
    "2.6 / 2.9 L03 §3 and cards for named-only concepts",
    "course/modules/LX/LX2/L03.html §3 (Definitions 3.1, 3.2), §5 misconception 3; cards.json LX2-c101..c103",
    "PASS",
    "Re-read: §3 states no provision of either text; the registry has no entry for either (d-cards-101-103). The lesson's sentence that the curriculum lists the two concepts is a statement about the program, not the statute.",
)
row(
    "d-dodd-mifid-cards",
    "2.7 removed and added cards for the Dodd-Frank and MiFID concepts",
    "cards.json (former LX2-c055..c057 absent; LX2-c101..c103 present)",
    "PASS",
    "card_delta_r14.out: added LX2-c101, c102, c103; removed none since e919577b. The round-13 removal of c055-c057 stands (absent). c101-c103 verified in d-cards-101-103.",
)
row(
    "d-dag",
    "2.9 check_dag; no concept used before definition or outside closure (cards)",
    "tools/check_dag.py --unit LX2; cards.json (no concept links)",
    "PASS",
    "tools/check_dag.py --unit LX2: 'check_dag LX2: PASS'. cards.json contains no concept link or code and no reference to another unit's lesson, so no card uses a concept outside the closure.",
)
row(
    "d-gates-structure",
    "2.9 structure gates run on this pin (scope: the four gates this round's delta can change)",
    "tools/check_pages.py --unit LX2; tools/check_dag.py --unit LX2; tools/run_labs.py --unit LX2; tools/verify_refs.py --offline",
    "PASS",
    "check_pages LX2: PASS; check_dag LX2: PASS; run_labs LX2: PASS (7/7); verify_refs.py --offline (whole registry, the verifier's offline run): 'offline integrity: 560 entries, 0 problems'. Not run in this round: check_projects, page_smoke (the only change since e919577b is cards.json; the lesson pages, project page and figures are byte-identical). Live verify_refs was not run (offline only).",
)
row(
    "d-notation",
    "2.4 / rule 13 notation: cards' symbols against notation/notation.json",
    "cards.json symbols; notation/notation.json (8 registered symbols: T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, Q)",
    "PASS",
    "Symbols in the cards: G, R, X, C_m, C_t (Prop 2.2), e_t, h_t, y-hat_t, V_t, U_t, E[e_t] (Section 4), H and n (windows), b1, b2 (bands), 44/117. None is a registered symbol, and none is used with a registered meaning. 'R' is the shares resting in the book (L03), not R^* (the return on the SDF); the R13, R15, R5a, R5c labels are reading names, not symbols.",
)
row(
    "d-c058-grade",
    "2.5 / 2.3 grade of LX2-c058 vs key-results row",
    "cards.json LX2-c058; course/modules/LX/LX2/L03.html Section 7 key results; run-lab-LX2-L03-1.out line 3",
    "PASS",
    "c058 is C with basis 'Lab 1 printed output (SIMULATED flow, seed 2026)'; the L03 key-results row 'Lab 1: zero crossed-book events ...' is C (SIMULATED basis). Output line 'events with a crossed book: 0' re-run this round.",
)
row(
    "d-c059-grade",
    "2.3 grade of LX2-c059 vs key-results row",
    "cards.json LX2-c059; L03.html Section 7 key results; run-lab-LX2-L03-1.out lines 16-17",
    "PASS",
    "c059 is C (demonstration threshold, lab output). The key row 'Lab 1: no trader flagged at the demonstration threshold 2' is C. Output: 'traders flagged: 0 of 6', largest ratio 21/37.",
)
row(
    "d-c085-grade",
    "2.3 grade of LX2-c085, LX2-c100 vs key rows",
    "cards.json LX2-c085, LX2-c100; L04.html Section 8 key results",
    "PASS",
    "Both C with SIMULATED seed 20261103 basis, matching the key row 'Exact hit rate 3/8 and bias 41/12 on the SIMULATED path of Lab 1, Part A' (C). Printed values re-run and recomputed (card_arithmetic_r14.py).",
)
row(
    "d-c100-new",
    "2.5 card vs printed block (LX2-c100)",
    "cards.json LX2-c100; tests/labs/LX2/lab-LX2-L04-1.py Part A printed block (run-lab-LX2-L04-1.out lines 28-31)",
    "PASS",
    "'Bias 41/12 (errors summing to 82 over 24 periods), rounded 3.4167': the printed bias is 41/12 and rounded 3.4167 (line 30), the errors sum to 82 (line 31, recomputed from the 24 printed errors in card_arithmetic_r14.py).",
)
row(
    "d-card-labels-current",
    "2.7 card labels agree with current lesson labels",
    "cards.json LX2-c017..c019, c074..c078, c086; L01.html Section 4; L04.html Section 4",
    "PASS",
    "Labels 'Proposition 4.1', 'Proposition 4.2', 'Proposition 4.3', 'Theorem 4.2', 'Theorem 4.3', 'Proposition 4.4', 'Assumption A1' (L04), 'Definition 4.1' and 'Problem E3' occur in the current lessons (grep of L01-L04 stripped text). No card uses a label that the lesson has renamed.",
)
row(
    "d-c054-hypothesis",
    "2.4 hypothesis of the cited proposition (LX2-c054)",
    "cards.json LX2-c054; course/modules/LX/LX2/L03.html Section 2 (Prop 2.2, Remark 2.3) and misconception 2",
    "PASS",
    "c054 says Prop 2.2 needs C_t under A1 and the identity fails after a trader cancels a resting order; Remark 2.3 says 'without the term C_t, the identity fails whenever a trader cancels a resting order' and the proof of Prop 2.2 uses A1 (each cancelled share in exactly one cancel total). Hypothesis A1 is stated in the card.",
)
row(
    "d-grade-key-consistency",
    "2.3 grades: card grades vs lesson key-results tables",
    "cards.json grades; L01-L04.html key-results tables",
    "PASS",
    "T cards (c017-c019, c020, c021, c051, c076-c079, c086) match T rows (Props 4.1-4.3, Prop 2.2, Thms 4.2-4.3, Prop 4.4, Part C row). C cards (statute, CFA, SR letter, lab outputs) match C rows. No card is graded T for a lab-only result (c085, c100, c058, c059, c090-c094 are C).",
)
row(
    "d-grade-legend",
    "2.9 grade legend in each lesson header",
    "course/modules/LX/LX2/L01..L04.html headers",
    "PASS",
    "Each lesson header prints the legend T (proved on the page), A, B, C (single source or lab result), D, X. Cards use only T and C, which the legend defines.",
)
row(
    "d-quote-fidelity",
    "2.1 quotes in cards match the sources",
    "cards.json quoted passages; scratch-LX2-d-r11/src (statute, Dirks, O'Hagan, CFA, SR 26-2)",
    "PASS",
    "ledgers/LX2/scripts/LX2-d-r14/quote_check_cards_r14.py: 18 curly-quoted passages in cards (quotes_cards_r14.out); 17 FOUND verbatim; c068 is not contiguous in the extracted text because the page-footer digit sits between 'model' and 'risk', and the page image confirms the words (see d-attrib-sr2026). The two 'hit' and 'bias' FOUND lines are not evidence of absence; the whole-word search is (statute_cfa_attachment_checks_r14.py).",
)
row(
    "d-l03-hypothesis-claims",
    "2.4 lab hypothesis and interpretation claims (L03)",
    "course/modules/LX/LX2/L03.html lines 103 (Lab 1 hypothesis), 355 (interpretation), Section 3 (393-395)",
    "PASS",
    CARRY + "L03.html byte-identical; the lab output it quotes (zero crossed-book events, zero identity failures, zero tally disagreements) re-run this round.",
)
row(
    "d-l04-e3-arithmetic",
    "2.2 numbers in Problem E3 (L04)",
    "course/modules/LX/LX2/L04.html Problem E3 (around line 411); Section 5 (A2 remark)",
    "PASS",
    "Recomputed in card_arithmetic_r14.py: Var(V) = (81-1)/12 = 20/3; Var(U) = (169-1)/12 = 14; Var(e) = 62/3; se = sqrt((62/3)/24) = 0.9280; gap 41/12 - 1 = 29/12 = 2.4167; gap/se = 2.604, which the lesson rounds to 'about 2.60'.",
)
row(
    "d-l01-sec5-statute",
    "2.6 L01 §5 statute statements",
    "course/modules/LX/LX2/L01.html lines 355-366 (section 5); lines 74-111",
    "PASS",
    CARRY + "L01.html byte-identical; the §5 claim spans re-read this round (8(a), 12(d), 5(d), 6(e)(1), 8(e) quoted passages unchanged).",
)
row(
    "d-l01-line63-s3-defined",
    "2.9 section 3 defined before use (L01) and card LX2-c005",
    "course/modules/LX/LX2/L01.html lines 63 and 96; cards.json LX2-c005",
    "PASS",
    CARRY + "L01.html byte-identical and LX2-c005 unchanged; 'national securities exchange' is not defined further, as c005 says.",
)
row(
    "d-l01-line88-spacing",
    "2.9 prose spacing and structure (L01 line 88)",
    "course/modules/LX/LX2/L01.html line 88",
    "PASS",
    CARRY + "L01.html byte-identical.",
)
row(
    "d-r2-lesson-delta",
    "2.9 L02 delta lines 527-539 (round-2 record)",
    "course/modules/LX/LX2/L02.html lines 527-539",
    "PASS",
    CARRY + "L02.html byte-identical.",
)
row(
    "d-delta-read",
    "delta read: every hunk of the LX2 slice since the round-13 pin e919577b",
    "git diff e919577b 8e5751c9 -- course/modules/LX/LX2 curriculum references tests/labs/LX2 notation tools",
    "PASS",
    "Only cards.json changed (one commit 8e5751c9). Every hunk read: c003 back (locator removed), c004 back (reading wording), c027 back (R13/R15 reading names), c051 front (each at its arrival quantity), c053 back (generator cancel rates; R2), c064/c065/c080/c088 back (Standard locators added), c071/c072/c077/c078/c079 back (e_t, h_t, V_t, U_t defined in the card), c084 back ('full text'), c086 back (MAE definition), c094 back ('recomputes'), c101-c103 added. Per-object comparison in card_delta_r14.out: changed c003, c004, c027, c051, c053, c064, c065, c071, c072, c077, c078, c079, c080, c084, c086, c088, c094; added c101-c103; removed none; 80 unchanged. Lessons, index, project, references, labs, notation, curriculum and tools are byte-identical to e919577b.",
)
row(
    "d-process-banned",
    "2.9 process words and banned phrases in learner text (cards)",
    "cards.json; tools/check_pages.py --unit LX2",
    "PASS",
    "Scan of every card front, back and basis for process words (verif*, round, builder, architect, reviewer, audit, ledger, fragment, fixed, corrected, draft, TODO, TBD, lorem, for brevity, beyond the scope, obviously, clearly, plan): two hits, both legitimate ('fixed by the Commission' in c025; 'draft the follow-up report' in c087, the Code's own word). No ellipsis in any card. check_pages LX2 PASS.",
)
row(
    "d-l01-sec2-registration-ungraded",
    "2.6 / 2.9 statute-content sentences need a claim span with a locator (L01 lesson convention, carried from round 13 and still open)",
    "course/modules/LX/LX2/L01.html line 69 (§2 opening paragraph): 'A registration statement is the document that an issuer files with the Commission [claim: (the term “Commission” means ...), section 2(a)(5)] to register a security under the 1933 Act.' and 'The definitions in section 2 do not define the phrase.' (both outside any claim span)",
    "FAIL",
    "Re-verified this round from the HTML: the only claim span on the sentence covers the Commission parenthetical (section 2(a)(5)). The sentence giving the meaning of 'registration statement' and the sentence that section 2 does not define 'in effect' carry no grade or data-locator. Statute text (scratch-LX2-d-r11/src/c1884.norm.txt): section 2(a)(8) reads 'the term registration statement means the statement provided for in section 6, and includes any amendment thereto', which the lesson does not cite; a search of section 2 alone (statute_cfa_attachment_checks_r14.py) finds no 'in effect' definition, and the 2(a)(8) wording is FOUND. The lesson header (line 53) says statute statements in claim spans carry a locator; these two sentences are statute statements without one. Card LX2-c003 no longer carries a locator (fixed in 8e5751c9), and LX2-c004 agrees with the statute, so the card side is closed; the lesson side is open.",
    "In course/modules/LX/LX2/L01.html line 69 wrap 'A registration statement is the document that an issuer files with the Commission ... under the 1933 Act' in a claim span with data-grade=\"C\", data-cite=\"gpondsecurities\" and data-locator=\"section 2(a)(8)\", and quote the statute's words ('the statement provided for in section 6, and includes any amendment thereto'). Wrap 'The definitions in section 2 do not define the phrase' in a claim span with data-locator=\"section 2 (no definition of 'in effect' among the definitions of section 2(a))\" or mark it explicitly as this lesson's reading. Rebuild, then re-run tools/check_pages.py --unit LX2. Cards LX2-c003 and LX2-c004 need no change.",
)
row(
    "d-c003-locator",
    "2.1 card locator vs statute (LX2-c003)",
    "cards.json LX2-c003 back; course/modules/LX/LX2/L01.html line 69",
    "PASS",
    "The round-13 failure (locator 'Section 2' on c003) is closed: the back now reads 'The document an issuer files with the Commission to register a security under the 1933 Act.' with no locator, so no locator can disagree with the statute. The lesson-side sentence is row d-l01-sec2-registration-ungraded.",
)
row(
    "d-proposition-hypotheses-r13",
    "2.4 proposition hypotheses carried into cards (LX2-c017, c018, c019, c051, c076, c077, c078, c079)",
    "cards.json; L01.html Section 4 (Props 4.1-4.3); L03.html Section 2 (Prop 2.2); L04.html Section 4 (Thms 4.2-4.3, Prop 4.4)",
    "PASS",
    "Each card's hypotheses match the lesson's: Prop 4.1 H1 (10 states, start unregistered/not_listed, 22 transitions, nothing else); Prop 4.2 H1 (R13, R15 used; R15 requires not_listed); Prop 4.3 H1 (R5a, R5c); Prop 2.2 (A1, any moment of a run after an event); Thm 4.2 (n >= 1, 0 <= b1 <= b2); Thm 4.3 (n >= 1); Prop 4.4 (A1); c079 (A1, band 2). The proofs use no hypothesis beyond these (checked against the proof text).",
)
row(
    "d-basis-simulated-hypothetical",
    "2.3 / rule 9: SIMULATED and HYPOTHETICAL labels in card basis fields",
    "cards.json basis fields for c038, c053, c058, c059, c085, c093, c094, c100",
    "PASS",
    "c038 says HYPOTHETICAL (L02 patterns are authored, per lab docstring); c053, c058, c059, c093, c094 say SIMULATED flow, seed 2026 (L03 lab docstring: 'SIMULATED'); c085 and c100 say SIMULATED path, seed 20261103 (L04 lab docstring). Graded C, as rule 9 requires for lab-read results.",
)
row(
    "d-mutants-r14",
    "rule 2.7 mutation check of the cards by planted errors",
    "ledgers/LX2/mutants/r14_card_mut1..mut4 (JSON copies of cards.json, one change each)",
    "PASS",
    "Four planted card errors (see mutants). Automated: card_numbers_r14.py flags mut1 (LX2-c079 '45/117' MISS) and mut4 (LX2-c085 '3/9' MISS) and reports 0 misses on the baseline cards.json. Manual: mut2 (c010 'fifteen days', against statute 8(b) 'ten days'), mut3 (c096 'Yes', against L01 §3 and statute 15(d)(1) 'other than the fiscal year'). All four killed.",
)
row(
    "d-registry-keys-r14",
    "2.1 cite keys exist; no primary text is invented for Dodd-Frank, MiFID II or SR 11-7 / 21-8",
    "references/references.json (560 entries); cards.json cite arrays; course/modules/LX/LX2/L04.html Section 3; cards LX2-c082, c101, c102",
    "PASS",
    "All cite keys used by the cards exist in the registry. A case-insensitive scan of the whole registry JSON for 11-7, 21-8, 'SR letter', Dodd, MiFID and Frank returns only edwards1999hedge (author 'Franklin R') and frb2026fed (the SR 26-2 letter, on 'model risk'). So 'no registry record' for SR 11-7 and 21-8 and 'no primary text' for Dodd-Frank and MiFID II are true.",
)

mutants = [
    {
        "name": "r14_card_mut1_c079_44_to_45",
        "file": "ledgers/LX2/mutants/r14_card_mut1_c079_44_to_45.json",
        "description": "LX2-c079 back 44/117 changed to 45/117 (wrong count of the Prop 4.4 hit set)",
        "killed_by": "card_numbers_r14.py (MISS 45/117 not in L04 text or lab output)",
    },
    {
        "name": "r14_card_mut2_c010_ten_to_fifteen",
        "file": "ledgers/LX2/mutants/r14_card_mut2_c010_ten_to_fifteen.json",
        "description": "LX2-c010 back: 8(b) notice 'not later than ten days' changed to 'fifteen days'",
        "killed_by": "manual reading against statute 8(b) (statute_cfa_attachment_checks_r14.py: FOUND 's8(b) ten days notice'); not caught by the number check",
    },
    {
        "name": "r14_card_mut3_c096_no_to_yes",
        "file": "ledgers/LX2/mutants/r14_card_mut3_c096_no_to_yes.json",
        "description": "LX2-c096 back answer 'No' changed to 'Yes' (the fiscal year of effectiveness is not suspended)",
        "killed_by": "manual reading against L01 §3 and statute 15(d)(1) 'other than the fiscal year within which such registration statement became effective'; not caught by the number check",
    },
    {
        "name": "r14_card_mut4_c085_3_8_to_3_9",
        "file": "ledgers/LX2/mutants/r14_card_mut4_c085_3_8_to_3_9.json",
        "description": "LX2-c085 back hit rate 3/8 changed to 3/9 (9 hits in 24 periods)",
        "killed_by": "card_numbers_r14.py (MISS 3/9 not in L04 text or lab output)",
    },
]

fragment = {
    "unit": "LX2",
    "slice": "d",
    "round": 14,
    "verifier": "Claude Haiku 5.5, independent verifier for LX2-d, round 14 (did not build LX2; shares no context with the builders)",
    "pin": "8e5751c903f0246115eba746afdf5d71f612bb37",
    "base": "e919577b45b431ce68e1e6533b00b8a301277937 (round-13 pin). Delta: cards.json only (commit 8e5751c9); 17 objects changed, 3 added (LX2-c101..c103), none removed.",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE14-LX2-d",
    "scratch": "/Users/billyribeiro/.fanout/scratch-LX2-d-r14 (stripped lessons scratch-LX2-d-r14-L0{1..4}.txt; quotes_cards_r14.out; page_locate_r14.out; card_numbers_r14.out; card_delta_r14.out; statute_cfa_attachment_checks_r14.out; card_arithmetic_r14.out; run-lab-LX2-L0{1..4}-1.out; cards_r13pin.json). Source copies read from /Users/billyribeiro/.fanout/scratch-LX2-d-r11/src (round-11 extraction; SR 26-2 pages 1-3 and 8-9 read as page images).",
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "verdict": "FAIL",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [
        "gpo1983dirks: references/references.json title reads 'Dirks v. SEC, 463 U.S. 646 (1982) - USREPORTS-463-646 | Content Details | GovInfo' while its year field and source_strings give 1983; the opinion text (scratch-LX2-d-r11/src/dirks.txt) reads 'Decided July 1, 1983'. No year is printed in LX2 cards or lessons (the 1982/1983 strings are inside cite keys only). Correction belongs to the architect through tools/add_reference.py.",
        "cfandcode: record type 'primary' against the curriculum's '(practitioner)' label (plan N2, carried from round 13; not a card defect).",
    ],
    "freshness_flags": [],
    "notes": [
        "Repository scripts behind the rows (all in ledgers/LX2/scripts/LX2-d-r14/): strip_lessons_r14.py, quote_check_cards_r14.py, page_locate_r14.py, card_numbers_r14.py, card_delta_r14.py, statute_cfa_attachment_checks_r14.py, card_arithmetic_r14.py, write_fragment_r14.py. Their printed outputs are kept in the scratch directory named in 'scratch' and are reproducible from the scripts and the round-11 source copies.",
        "Scope: slice d is every card in course/modules/LX/LX2/cards.json (100 cards: c001-c103 with c055-c057 absent) read against L01-L04. All 100 cards were read in full this round; the lessons were read in full (stripped text).",
        "Delta-driven carry: only cards.json changed since the round-13 pin. Rows whose cited card objects and lesson files are unchanged are carried with the prefix; every row touching a changed card object was re-verified this round.",
        "Lesson-side verification of the lesson claim spans beyond card needs was not re-scoped this round (other slices own them); where a lesson sentence was needed to check a card, it was read.",
        "C vs T: lab-read results (SIMULATED or HYPOTHETICAL) are graded C naming the lab, per verifier rule 9. The plan's section 9 wording ('grade T with basis' for lab-derived cards) conflicts with that rule; no row fails on it. Architect to confirm (carried from round 13).",
        "c094 says the lab 'recomputes' the tally where L03 says 'rebuilds'; same meaning, recorded as wording, not a fail.",
        "c086 is graded T on Lab 1 Part C, a hand-built path with fixed values (not SIMULATED); the T rests on the printed errors and the stated Theorem 4.3, consistent with rule 9.",
        "Not checked: Standards and opinions beyond the quoted passages; the Dirks and O'Hagan pages were located by printed page marker in the round-11 text copies, not re-read against the bound reporter; the statute text is the round-11 GovInfo extraction (COMPS-1884/1885 PDFs present; not re-extracted this round). Live verify_refs and check_projects, page_smoke not run (outside the cards delta). Live CFA Institute and Federal Reserve pages were not fetched (saved copies used). No ruff/mypy on ledgers/*/scripts: excluded by pyproject extend-exclude.",
    ],
    "summary": {
        "slice": "LX2-d (all 100 cards.json cards against L01-L04)",
        "rows": len(rows),
        "pass": sum(1 for r in rows if r["status"] == "PASS"),
        "fail": sum(1 for r in rows if r["status"] == "FAIL"),
        "unverifiable": sum(1 for r in rows if r["status"] == "UNVERIFIABLE"),
        "mutants_killed": len(mutants),
        "mutants": len(mutants),
    },
}

with open("ledgers/LX2/LX2-d.json", "w", encoding="utf-8") as fh:
    json.dump(fragment, fh, indent=2, ensure_ascii=False)
    fh.write("\n")
print("rows", len(rows), "mutants", len(mutants))
