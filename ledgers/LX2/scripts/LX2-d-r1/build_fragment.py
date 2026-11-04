"""LX2-d round 1: writes ledgers/LX2/LX2-d.json (the verifier's fragment). Run from the checkout root."""
import json, sys
S = "ledgers/LX2/scripts/LX2-d-r1/"
CARDS = "course/modules/LX/LX2/cards.json"
L01 = "course/modules/LX/LX2/L01.html"; L02 = "course/modules/LX/LX2/L02.html"
L03 = "course/modules/LX/LX2/L03.html"; L04 = "course/modules/LX/LX2/L04.html"
rows = []
def row(id_, check, location, status, evidence, fix=None):
    r = {"id": id_, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    rows.append(r)

# ---- defects (FAIL) -------------------------------------------------------------------------
row("d-c010-8b-trigger", "2.6 statute attribution (card vs statute text)",
    CARDS + " LX2-c010 (back); " + L01 + " line 84 (same paraphrase)", "FAIL",
    "Card: the Commission may issue a refusal order under section 8(b) with no condition stated. Statute text (COMPS-1884, section 8(b), fetched; "
    "scripts/LX2-d-r1/opinion_statute_locators.py prints 'STATUTE c010 8(b) trigger (card omits it): FOUND') conditions the order on "
    "'if it appears to the commission that a registration statement is on its face incomplete or inaccurate in any material respect', "
    "after notice and opportunity for hearing. The card and L01 line 84 state the power without that trigger.",
    "Add the trigger and procedure to the card back: the order issues only if it appears that the statement is on its face incomplete or inaccurate "
    "in any material respect, after notice and opportunity for hearing (section 8(b)). Same change to L01.html line 84 (L01 owner).")
row("d-c016-abs-class", "2.6 statute attribution (card vs statute text)",
    CARDS + " LX2-c016 (back); " + L01 + " line 111 (same omission)", "FAIL",
    "Card: the duty is suspended if 'the securities of each class are held of record by less than 300 persons'. Statute (COMPS-1885, section 15(d)(1), "
    "third sentence, fetched) reads 'the securities of each class, other than any class of asset-backed securities, to which the registration statement "
    "relates are held of record by less than 300 persons' (opinion_statute_locators.py: FOUND). The asset-backed carve-out is omitted, so the card "
    "misstates the test for an asset-backed class.",
    "In the card back, after 'the securities of each class' insert '(other than any class of asset-backed securities)'. Same fix to L01.html line 111 (L01 owner).")
row("d-c025-8d-trigger", "2.6 statute attribution (card vs statute text)",
    CARDS + " LX2-c025 (back); " + L01 + " line 85 and line 377-378 (same paraphrase)", "FAIL",
    "Card: 'Under section 8(d), after notice and an opportunity for hearing, the Commission may issue a stop order'. Statute (COMPS-1884, section 8(d), fetched) "
    "conditions the power on 'if it appears to the commission at any time that the registration statement includes any untrue statement of a material fact or "
    "omits ...' and requires notice by personal service or confirmed telegraphic notice (opinion_statute_locators.py: trigger FOUND). The card omits the trigger.",
    "Add the trigger to the card back: the stop order follows a finding that the statement includes an untrue statement of a material fact or omits a "
    "required or necessary material fact, after notice and opportunity for hearing (section 8(d)). Same change to L01.html lines 85 and 378 (L01 owner).")
row("d-dup-c056-c057", "2.7 duplicate scan",
    CARDS + " LX2-c056 and LX2-c057", "FAIL",
    "Backs are byte-identical: 'Only its name, as one of the unit's concepts. Its provisions are not stated here. No provision is cited, because the registry "
    "holds no primary text for it, and no statement about its scope is made.' (scripts/LX2-d-r1/cards_structure.out, 'duplicate backs'). The fronts ask about "
    "different instruments, so the back of each card names neither; a learner cannot tell the two answers apart. This breaks 'no duplicate cards'.",
    "Rewrite each back to name its own instrument: c056 'Only its name, the Dodd–Frank Act, as one of the unit's concepts ...'; c057 'Only its name, MiFID II, as one "
    "of the unit's concepts ...'. Keep the 'not stated here' sentence in each.")
row("d-c058-grade", "2.3 grades (SIMULATED lab output)",
    CARDS + " LX2-c058", "FAIL",
    "No grade field; basis 'Lab 1 printed output (SIMULATED flow, seed 2026); not graded'. The result is read off a SIMULATED lab (" + L03 + " lab output "
    "lines 330-334: 'events with a crossed book: 0', 'events where entered != ...: 0'). VERIFIER_RULES 2.2/9 and BUILDER_RULES 7: a key empirical result read off a "
    "SIMULATED lab is grade C naming the lab, and every key result carries its grade. 'not graded' is not an allowed grade.",
    "Set \"grade\": \"C\" and basis to 'Lab 1 printed output (SIMULATED flow, seed 2026)'. L03 key-results rows (" + L03 + " lines 505-506) use the same 'not graded' (L03 owner).")
row("d-c059-grade", "2.3 grades (SIMULATED lab output)",
    CARDS + " LX2-c059", "FAIL",
    "No grade field; basis 'Lab 1 printed output; not graded' and the basis does not name SIMULATED. Output " + L03 + " line 343 'traders flagged: 0 of 6' and "
    "line 344 'largest ratio 21/37' come from the SIMULATED flow (lab header line 328). Same rule as d-c058.",
    "Set \"grade\": \"C\" and basis to 'Lab 1 printed output (SIMULATED flow, seed 2026; demonstration threshold)'.")
row("d-c085-grade", "2.3 grades (SIMULATED lab output)",
    CARDS + " LX2-c085; " + L04 + " line 429 (lesson key-results row carries the same T)", "FAIL",
    "Card grade 'T', basis 'Lab 1, Part A (computed)'. Lab 1 Part A runs on a SIMULATED path from seed 20261103 (" + L04 + " hypothesis line 148 and "
    "docstring line 151). The printed values (hits = 9 of 24, hit rate 3/8, bias 41/12) are reproduced independently by "
    "scripts/LX2-d-r1/recompute_card_numbers.py. A result read off a SIMULATED lab is C naming the lab (VERIFIER_RULES 9), not T.",
    "Set \"grade\": \"C\" and basis to 'Lab 1, Part A (SIMULATED path, seed 20261103)'. Change " + L04 + " line 429 from T to C (L04 owner).")

# ---- sampled rows, one per 10 cards (all 89 read individually) ------------------------------
row("d-cards-001-010", "2.7 cards sample", CARDS + " LX2-c001..c010", "FAIL",
    "Read every card against L01.html (lines 55-115, 137-313, 319-353). Quotations, labels, numbers and grades pass (cards_vs_lessons.out, cards_labels.out, "
    "quotes.out). c010 fails: the 8(b) trigger is omitted (row d-c010-8b-trigger).",
    "See d-c010-8b-trigger.")
row("d-cards-011-020", "2.7 cards sample", CARDS + " LX2-c011..c020", "FAIL",
    "Read against L01.html §3-§4 and the Proposition 4.1-4.3 proofs (lines 319-353) and the Lab 1 output (lines 275-313). Counts 10 states and 22 transitions, the 2/4/5/2 "
    "state-table counts and the reachability proof reproduce (recompute_card_numbers.out). c016 fails: the asset-backed carve-out is omitted (d-c016-abs-class).",
    "See d-c016-abs-class.")
row("d-cards-021-030", "2.7 cards sample", CARDS + " LX2-c021..c030", "FAIL",
    "Read against L01.html §5-§6 and L02.html §1-§3. Misconception cards c024-c027 match L01 §6 lines 372-387; c028-c030 match the O'Hagan and Dirks quotes at "
    "the printed pages (opinion_statute_locators.out). c025 fails: the 8(d) trigger is omitted (d-c025-8d-trigger).",
    "See d-c025-8d-trigger.")
row("d-cards-031-040", "2.7 cards sample", CARDS + " LX2-c031..c040", "PASS",
    "Read against L02.html §2-§4 and Lab 1 printed table (lines 399-423). c038 matches the printed fired/not-fired rows (P1,P3,P4,P6 fire; P2,P5,P7,P8 do not). "
    "Dirks p. 662, 663, 664 and O'Hagan pp. 651-656 quotes found at the printed pages (opinion_statute_locators.out, quotes.out). Grades C with keys or lab basis.")
row("d-cards-041-050", "2.7 cards sample", CARDS + " LX2-c041..c050", "PASS",
    "Read against L02.html misconceptions (lines 441-446), L02 §4 footnotes 5 and 7 (O'Hagan p.653 n.5; p.655 n.7; quotes in quotes.out) and L03.html §1 "
    "Definitions 1.1, 1.3, Remark 1.2, Assumption A1 (lines 56-78). Definition wording matches the lesson.")
row("d-cards-051-060", "2.7 cards sample", CARDS + " LX2-c051..c060", "FAIL",
    "Read against L03.html §2 (Proposition 2.2, Remarks 2.3-2.4, lines 80-99), misconceptions (377-392) and Lab 1 output (328-344). c051 and c054 proofs reproduce; "
    "c053 arithmetic (3x97=291 < 6x104=624) and c059 (21/37 < 2) reproduce (recompute_card_numbers.out). c056 and c057 have identical backs (d-dup-c056-c057). "
    "c058 and c059 lack grade C (d-c058-grade, d-c059-grade).",
    "See d-dup-c056-c057, d-c058-grade, d-c059-grade.")
row("d-cards-061-070", "2.7 cards sample", CARDS + " LX2-c061..c070", "PASS",
    "Read against L03.html §4 (canon-breaks, lines 363-374) and L04.html §1-§3 (lines 55-111). The L04 Definitions 3.1 (model; model risk) and 3.2 quote the attachment: "
    "the model definition and its spreadsheet exclusion are at lines 114-117 and the model-risk definition at line 134 of att.txt, between the footers for pages 2-3 and 3-4 (sr_locators.out), so p.3. c068 paraphrases 'responsible for adopting ... practices' without quote marks; the words are "
    "the attachment's own (pp.1-2 section I), so it passes (see notes).")
row("d-cards-071-080", "2.7 cards sample", CARDS + " LX2-c071..c080", "PASS",
    "Read against L04.html §4 (Definition 4.1, lines 116-124; Theorems 4.2-4.3 and Proposition 4.4 with proofs, lines 126-142). Every displayed number reproduces: "
    "44/117 = 0.3761 (6 dp 0.376068), 8x5+4 = 44, E[e_t] = 1 (recompute_card_numbers.out). Theorem hypotheses are stated on cards c076 and c077.")
row("d-cards-081-089", "2.7 cards sample", CARDS + " LX2-c081..c089", "FAIL",
    "Read against L04.html §1-§6 (lines 56-111, 372-380, 382-392). The CFA quotation in c088 is found on the fetched Standards III(A) page, c081 paraphrases the same Guidance (paragraph 2, 'must comply with any legally imposed fiduciary duty'), and the Example 3 sentences behind c087 are on the VI(A) page (quotes.out; cfa pages). SR 26-2 quotations c089 and the 'supersedes' and '$30 billion' claims in c082-c083 are found in the fetched attachment and letter. c084's "
    "search claim (no 'hit' or 'bias' in the attachment) reproduces (sr_pages.out). c085 fails: over-graded T on a SIMULATED result (d-c085-grade).",
    "See d-c085-grade.")

# ---- cross-card rows ---------------------------------------------------------------------------
row("d-dup-scan", "2.7 full scan for duplicates", CARDS + " (all 89 cards)", "FAIL",
    "Full scan: no duplicate ids, no duplicate fronts, no duplicate backs except c056 and c057 (scripts/LX2-d-r1/cards_structure.out 'duplicate backs'). No two cards "
    "carry the same question. c055 overlaps c056 and c057 in theme (naming the Acts) but asks a different question.",
    "Fix c056 and c057 backs (d-dup-c056-c057).")
row("d-schema", "2.7 structure of cards.json", CARDS, "PASS",
    "scripts/LX2-d-r1/cards_structure.out: 89 cards; ids LX2-c001..LX2-c089 unique and sequential; lessons L01 27, L02 16, L03 20, L04 26 (all four present); "
    "fields id, lesson, front, back, cite, grade, basis; every cite key exists in references/references.json (560 keys; 0 unknown); grades only T or C; every T card "
    "has a basis; every graded non-T card has a cite or basis.")
row("d-coverage", "2.7 every definition, theorem, misconception has a card", CARDS, "PASS",
    "Definitions: L01 2.1, 3.1, 'national securities exchange', registration statement, filed/in effect, A1 (c001-c005, c022); L02 2.1, 3.1, 4.1 (c028, c030, c031); "
    "L03 1.1, 1.3, Remark 1.2, A1, Prop 2.2, Remarks 2.3-2.4, 3.1-3.2 (c044-c057); L04 1.1, 2.1, 3.1, 3.2, 3.3, 4.1, A1, A2, Thm 4.2, Thm 4.3, Prop 4.4 "
    "(c064-c079). Propositions 4.1-4.3 (c017-c019). Misconceptions: L01 4 (c024-c027), L02 4 (c039-c042), L03 3 (c053-c055), L04 4 (c086-c089). Key-result "
    "rows of each lesson are covered (cards c020-c023, c058-c059, c085 for the labs).")
row("d-quotes-in-lesson", "2.7 cards agree with lesson text (quotations)", CARDS + " (every curly-quoted string)", "PASS",
    "scripts/LX2-d-r1/cards_vs_lessons.py: every quoted string on every card occurs in its lesson text (no 'quote-not-in-lesson' line). Its only residual line "
    "(c030 'p. 659' number) is a locator inside a data-locator attribute, confirmed by cards_labels.py.")
row("d-labels-locators", "2.7 cards agree with lesson text (labels, pages, footnotes)", CARDS + " (all labels)", "PASS",
    "scripts/LX2-d-r1/cards_labels.py checks every 'Section N', 'Problem X', 'Lab N', 'Definition/Proposition/Theorem/Remark/Assumption', 'p. N' and 'p. N n. M' against "
    "the raw lesson markup including attributes: 0 failing (cards_labels.out).")
row("d-numbers", "2.2 numbers on cards (recomputed)", CARDS + " (every number)", "PASS",
    "scripts/LX2-d-r1/recompute_card_numbers.py recomputes every card number with its own code (not the lab's): L04 Part A hits 9/24, rate 3/8, bias 41/12, sum 82, "
    "first/last 12-period values 1/4, 11/3, 1/2, 19/6; Part C bias 0 and MAE 3; Part D 117 pairs, 44/117, E[e]=1, band counts 9/27/44/60; L01 10 states, 22 transitions, "
    "2 sale, 4 offer, 5 R13, 2 R15, 0 both, 10 of 10 reachable; L03 291 < 624, 21/37 < 2, C_t = 240, 59/986; L02 4 fired, 3 outsider, 1 knowledge failure. All match the cards.")
row("d-run-labs", "2.5 labs whose outputs the cards quote", "tests/labs/LX2 twins via tools/run_labs.py --unit LX2", "PASS",
    "scripts/LX2-d-r1/run_labs.out: 'run_labs LX2: PASS (7/7)', exit 0 (L01, L02, L03, L04 and project labs 1-3). The tool runs each twin as python -I -W error (tools/run_labs.py line 55). "
    "The printed output the cards cite is the expected block in each page.")
row("d-attrib-opinions", "2.1 attribution (Dirks, O'Hagan)", CARDS + " c028-c043", "PASS",
    "Both opinions fetched as GovInfo PDFs (USREPORTS-463-646, USREPORTS-521-642). 18 locator checks (opinion_statute_locators.out) all OK: e.g. Dirks p.664 'a question of fact', "
    "p.663 n.23 'an independent element of a Rule 10b-5 violation', p.662 'Absent some personal gain', p.660 tippee duty; O'Hagan p.652 'not only to officers ...', p.653 n.5 "
    "'does not escape Exchange Act sanction', p.655 n.7 'may still be liable under the misappropriation theory', p.656 'does not catch all conceivable forms'. "
    "Quotations: quotes.out (every curly-quoted string FOUND).")
row("d-attrib-statute", "2.1 attribution (1933 and 1934 Acts)", CARDS + " c001-c027", "FAIL",
    "GovInfo COMPS-1884 (1933 Act) and COMPS-1885 (1934 Act) fetched. Verified against the text (opinion_statute_locators.out): 6(a), 6(c), 5(a), 5(c), 8(a), 8(b) later-date, "
    "8(d) cease, 12(a), 12(b), 12(d) thirty days and withdrawal, 13(a), 15(d)(1) first, second and third sentences. Failing: c010, c016, c025 (rows above). "
    "c014 omits the 'upon such terms as the commission may deem necessary' clause of 12(d); that clause qualifies the Commission's terms, not whether withdrawal is possible, so it passes (see notes).",
    "See d-c010-8b-trigger, d-c016-abs-class, d-c025-8d-trigger.")
row("d-attrib-sr2026", "2.1 attribution (SR 26-2 letter and attachment)", CARDS + " c066-c069, c082-c084, c089", "PASS",
    "Letter (sr2602.pdf) and attachment (sr2602a1.pdf, linked from the registry page) fetched. Quotations FOUND (quotes.out). Printed pages from the footers (sr_locators.out): model definition and "
    "spreadsheet exclusion p.3 (section II); model-risk definition p.3 (section III); 'does not set forth enforceable standards' and 'will not result in supervisory "
    "criticism' p.2 section I; footnote 1 p.2; outcomes analysis p.9; 'persistent deviations' p.9; ongoing monitoring p.9; Components of Model Validation p.8. "
    "Letter: 'supersedes and replaces SR letter 11-7 ... and SR letter 21-8' and 'over $30 billion in total assets regulated by the Federal Reserve' (quotes.out). "
    "'hit' and 'bias' occur nowhere in the attachment or letter (sr_pages.out), so c084 holds.")
row("d-attrib-cfa", "2.1 attribution (CFA Code and Standards)", CARDS + " c064, c065, c080, c081, c087, c088", "PASS",
    "CFA Standards pages for III(A) and VI(A) fetched from cfainstitute.org (the registry URL is the landing page that links them). Quotations c064 and c088 FOUND "
    "(quotes.out). c065, c080, c081 and c087 paraphrase or quote the Standards: 'any matter that could reasonably be expected to impair independence' (VI(A) guidance), "
    "'duty of loyalty to their clients' (III(A)), 'must comply with any legally imposed fiduciary duty' (III(A) guidance para. 2), and Example 3 ('At minimum ... disclose ... "
    "Best practice is to avoid') all FOUND in the pages.")
row("d-grades", "2.3 grades", CARDS + " (all graded cards)", "FAIL",
    "T cards: c017-c019 (proved on the page), c020-c021 (counts from the definitions), c051 (proof), c052 (remark, follows from the definitions), c054 (follows from Prop 2.2), "
    "c076-c079 (proofs), c086 (hand-built Part C path, arithmetic, not SIMULATED): PASS. C cards: statute, opinion, CFA, SR letter and lab results with a key or lab basis: PASS. "
    "FAIL: c058, c059 (no grade on SIMULATED output), c085 (T on SIMULATED output). See d-c058-grade, d-c059-grade, d-c085-grade.",
    "See d-c058-grade, d-c059-grade, d-c085-grade.")
row("d-notation", "2.4 notation (notation/notation.json)", CARDS + " (symbols)", "PASS",
    "Symbols on cards: H (horizon, LX2 plan 2.4; never T), h_t, e_t, ŷ_t, y_t, U_t, V_t, n (window size), G, R, X, C_m, C_t (Prop 2.2, defined in L03 §2), E[...] "
    "(expectation; registered \\E), 44/117. No registered symbol (T, R^*, Phi, gamma_3, ...) is used with another meaning (cards_structure.out symbol list; notation/notation.json 'symbols' and 'macros').")
row("d-banned-process", "2.9 banned phrases and process words", CARDS, "PASS",
    "cards_structure.out: no BANNED-HIT line (TODO, TBD, lorem, for brevity, details omitted, beyond the scope, left as an exercise, you can add more, it is important to note, "
    "studies show, experts agree, it is well known, obviously, clearly, ellipses) and no PROCESS-WORD line (builder, build, verifier, round, REQUEST).")
row("d-dag", "2.9 DAG: concepts used outside the closure", CARDS + " (all text)", "PASS",
    "Scanned for D1-D9 names (efficient markets, information content, agency, moral hazard, adverse selection, Kyle, Glosten, model integrity, value-at-risk, backtest, "
    "clearing, hypothesis test, t-statistic, statistical power): none on any card. The cards' 'earnings' (c033) is Dirks' phrase at p.663. Cards use only LX2 concepts and FC1-level vocabulary.")
row("d-tools", "gate: targeted tools", "tools/check_pages.py, check_dag.py, check_projects.py --unit LX2", "PASS",
    "scripts/LX2-d-r1/check_pages.out 'check_pages LX2: PASS' (includes check_cards), check_dag.out 'PASS', check_projects.out 'PASS'.")

# ---- notes rows (carried as PASS with the reason) ---------------------------------------------
row("d-note-c014-12d-terms", "2.1 attribution (note)", CARDS + " LX2-c014", "PASS",
    "12(d) withdrawal: the statute adds 'upon such terms as the commission may deem necessary ... upon application by the issuer or the exchange'. The card keeps "
    "'on application by the issuer or the exchange to the Commission' and answers how a security may be removed; the terms clause is not a condition of removal.")
row("d-note-c068-paraphrase", "2.1 attribution (note)", CARDS + " LX2-c068", "PASS",
    "Unquoted paraphrase of the attachment's pp.1-2 sentence ('responsible for adopting model risk management practices that are appropriate and effective for managing the "
    "specific risks the banking organization faces or is likely to face'). Substance and pages match (sr_pages.out; sr_locators.out).")
row("d-note-c053-track", "2.1 wording (note)", CARDS + " LX2-c053", "PASS",
    "Card says the ratio 'does not track the cancel rates'; L03 line 381 says 'does not track ... exactly'. The card's example (3/104 below 6/97) supports the weaker claim, so PASS.")

# ---- validation of stated scripts -----------------------------------------------------------
frag = {
 "unit": "LX2",
 "slice": "LX2-d",
 "round": 1,
 "verifier": "Claude Haiku 5.5, independent verifier for LX2-d, round 1 (did not build LX2; no shared context with builders)",
 "pin": "1c1645f3b00eada2fb54d39c86d5d949e15b4fbc",
 "base": "none (round 1: first independent verification of slice d; no previous fragment)",
 "checkout": "/Users/billyribeiro/.fanout/wt/verifyE1-LX2-d",
 "scratch": "/tmp/lx2d-src (source texts fetched with plain curl; recreate with ledgers/LX2/scripts/LX2-d-r1/fetch_sources.sh)",
 "verified_at": "2026-11-04T04:55:00+00:00",
 "verdict": "FAIL",
 "rows": rows,
 "mutants": [],
 "registry_flags": [
  "gpo1983dirks: registry title field reads 'Dirks v. SEC, 463 U.S. 646 (1982)' and year is 1983. The GovInfo opinion text reads 'Argued March 21, 1983-Decided July 1, 1983' (scratch USREPORTS-463-646.txt line 12). The title's '(1982)' is the term year; correction via add_reference.py by the architect (no builder edits a record).",
  "frb2026fed: the registry URL is the letter page (sr2602.htm). The 'Attachment' the lesson quotes is sr2602a1.pdf, which that page links (href '/supervisionreg/srletters/SR2602a1.pdf'). The key covers both; the architect should confirm the attachment is part of the record.",
  "cfandcode: the registry URL is the CFA landing page; the quoted Standards text is on the Standards of Practice pages it links (III(A), VI(A)). The 2024 Code PDF it also links is a condensed text without the Guidance quoted in the lesson."
 ],
 "freshness_flags": [],
 "notes": (
  "Round 1 on pin 1c1645f. Read all 89 cards and every line of the four lesson bodies (L01 and L02 from line 1; L03 and L04 from line 30, the site head above it is template markup not cited by any card). "
  "Verdict FAIL: 7 defect rows (c010, c016, c025 statute triggers and ABS carve-out; c056/c057 identical backs; c058, c059, c085 grades on SIMULATED output) plus the sample and scan rows that point to them. "
  "Lesson-level defects found while reading (owned by the L01, L03 and L04 slices; not charged to slice d): L01.html line 84 (8(b) trigger omitted), line 85 and line 378 (8(d) trigger omitted), "
  "line 111 (ABS carve-out omitted); L04.html line 429 (T grade on SIMULATED Lab 1 Part A); L03.html lines 505-506 ('not graded (SIMULATED output)' should be C under VERIFIER_RULES 9). "
  "Checked and not defects: the Dirks and O'Hagan locators, every quotation, the SR 26-2 pages and supersession, the CFA quotations, and every number on the cards (independently recomputed). "
  "Not checked by this slice: ruff, mypy --no-incremental and pytest (no Python tool or test file in the cards slice; the twins were run by run_labs only); verify_refs --unit LX2 (the reference slice's run; "
  "I read the six keys' pages directly); page_smoke (pages slice, rendering; not card content); index.html and project.html (outside the cards slice); run_graders (rubric unit, no autograder); fetch_data (no dataset)."
 ),
 "summary": "",
}
pass_n = sum(r["status"] == "PASS" for r in rows); fail_n = sum(r["status"] == "FAIL" for r in rows)
frag["summary"] = (f"LX2-d round 1 on 1c1645f: verdict FAIL. {len(rows)} rows: {pass_n} PASS, {fail_n} FAIL, 0 UNVERIFIABLE. "
  "All 89 cards read against their lessons; 7 card defects (3 statute attributions, 1 duplicate pair, 3 grades) and the blocks and scans that contain them.")
json.dump(frag, open("ledgers/LX2/LX2-d.json", "w", encoding="utf-8"), indent=2, ensure_ascii=False)
open("ledgers/LX2/LX2-d.json", "a", encoding="utf-8").write("\n")
print("rows", len(rows), "pass", pass_n, "fail", fail_n)
