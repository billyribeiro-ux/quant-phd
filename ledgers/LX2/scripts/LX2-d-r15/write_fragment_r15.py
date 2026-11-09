"""Write the round-15 LX2-d fragment from the round-14 fragment and the round-15 checks.

Usage: python3 -I write_fragment_r15.py <round14_fragment.json> <out_fragment.json>
Rows whose subject is byte-identical since the round-14 pin (8e5751c9) are carried with the required prefix.
Rows that touch a changed object (LX2-c027, c030, c081, new c104) or a changed check are re-verified and written fresh.
"""
import json
import sys

prev = json.load(open(sys.argv[1], encoding="utf-8"))
out_path = sys.argv[2]
PREV_PIN = "8e5751c9"
CARRY = [
    "d-cards-001-010", "d-cards-011-020", "d-attrib-statute", "d-cards-031-040", "d-cards-041-050",
    "d-cards-051-060", "d-cards-061-070", "d-cards-071-080", "d-cards-090-094", "d-cards-095",
    "d-cards-096-097", "d-cards-098-099", "d-cards-101-103", "d-attrib-sr2026", "d-l03-dodd-mifid",
    "d-c058-grade", "d-c059-grade", "d-c085-grade", "d-c100-new", "d-card-labels-current",
    "d-c054-hypothesis", "d-grade-legend", "d-l03-hypothesis-claims", "d-l04-e3-arithmetic",
    "d-l01-sec5-statute", "d-l01-line63-s3-defined", "d-l01-line88-spacing", "d-r2-lesson-delta",
    "d-c003-locator", "d-proposition-hypotheses-r13", "d-basis-simulated-hypothetical",
]
prev_rows = {r["id"]: r for r in prev["rows"]}
rows = []
for rid in CARRY:
    r = prev_rows[rid]
    assert r["status"] == "PASS", rid
    rows.append({
        "id": rid,
        "check": r["check"],
        "location": r["location"],
        "status": "PASS",
        "evidence": f"Carried from round 14 ({r['location']} byte-identical since the previous pin {PREV_PIN}; "
                    f"card objects unchanged per card_delta_r15.out): " + r["evidence"],
    })
FRESH = {
    "d-cards-081-089": ("2.7 card vs current lesson; 2.1 attribution; 2.2 numbers (LX2-c081..c089)",
        "cards.json LX2-c081..c089 (c081 changed); course/modules/LX/LX2/L04.html Sections 1-3, 5-6; cfa-iii-a.norm.txt",
        "PASS c081 (changed) re-verified fresh: back 'Comply with it. The Code does not set a legal fiduciary duty, and members "
        "must comply with any legally imposed one (Standard III(A), Guidance, subheading Understanding the Application of Loyalty, "
        "Prudence, and Care, the paragraph beginning Fiduciary duties are often imposed)'. Source: cfa-iii-a.norm.txt offset 6029 "
        "is the subheading 'Understanding the Application of Loyalty, Prudence, and Care'; offset 7360 'members and candidates must "
        "comply with any legally imposed fiduciary duty, the Code and Standards neither impose such a legal responsibility'; no "
        "other subheading lies between 6029 and 7405 (python -I scan, round 15). L04.html line 67 and Section 1 carry the same "
        "statement. c082-c089 unchanged since 8e5751c9 (card_delta_r15.out); their quotations re-checked this round "
        "(quotes_cards_r15.out: c084, c088, c089 FOUND; statute_cfa_r15.out: SR 26-2 supersedes, applicability, footnote 1 FOUND; "
        "word search 'hit' and 'bias' 0 matches in the attachment)."),
    "d-numbers": ("2.2 numbers in cards: computed, quoted or derived; every card number in its lesson",
        "cards.json (101 cards); L01-L04 stripped text; run-lab-LX2-L0{1..4}-1.out",
        "PASS card_numbers_r15.py over 101 cards: 0 number tokens absent from every LX2 lesson text and lab output "
        "(scratch-LX2-d-r15/card_numbers_r15.out: 'total misses 0'). Re-derived fresh in "
        "ledgers/LX2/scripts/LX2-d-r15/card_arithmetic_check_r15.py (scratch-LX2-d-r15/card_arithmetic_check_r15.out): c079 44/117 "
        "(pairs 117, hits 44, 0.3761); c078 E[e]=1; c086 bias 0, MAE 3 from errors +3,-3,+3,-3; c100 82/24=41/12=3.4167; c085 9/24=3/8=0.3750; "
        "c053 3x97=291 < 6x104=624. Part A printed errors re-summed: 24 rows, sum 82, 9 hits (run-lab-LX2-L04-1.out)."),
    "d-attrib-cfa": ("2.1 attribution; quotes and locators (LX2-c064, c065, c080, c081, c087, c088)",
        "cards.json LX2-c064, c065, c080, c081, c087, c088; scratch-LX2-d-r11/src/cfa-iii-a.norm.txt, cfa-vi-a.norm.txt; L04.html Sections 1-2",
        "PASS c081 fresh (see d-cards-081-089). Other cards carried: statute_cfa_r15.out FOUND for III(A) duty of loyalty; "
        "Guidance 'often imposed by law or regulation'; 'legally imposed duty'; 'neither impose'; VI(A) definition, the standard, "
        "best practice, Example 3 (minimum, best practice). Quotations in c064 and c088 re-found this round (quotes_cards_r15.out)."),
    "d-cards-090-094-lab-basis": ("2.5 lab output named in basis (LX2-c023, c038, c053, c058, c059, c085, c093, c094, c100)",
        "cards.json basis fields; run-lab-LX2-L01..L04-1.out (re-run this round)",
        "PASS labs re-run under python3 -I -W error; outputs byte-identical to round 14 (diff, four files). c058 'events with a "
        "crossed book: 0' (L03 line 3); c093 entered identity 0 (line 4); c094 tally disagreements 0 (line 7); c059 traders flagged 0 of 6, "
        "largest 21/37 (lines 16-17); c053 trader 1 3/104 at cancel_pct 10, trader 0 6/97 at 5 (table rows 0-1); c085 hits 9 of 24, rate 3/8 (L04 line 28-29); "
        "c100 bias 41/12, 3.4167 (lines 30-31). Basis strings name SIMULATED or HYPOTHETICAL as the lab docstrings do."),
    "d-cards-no-grade": ("2.7 grade and citation coverage",
        "cards.json (101 cards)",
        "PASS fresh count (python -I, round 15): 31 cards carry no grade, 70 carry a grade (T 11, C 59). Every card has a cite list or a basis; "
        "every grade C or T card has a cite or a basis (check_pages.py line 392-394 rule). Four cite-only cards without a grade (c001, c002, c003, c005) "
        "are definition cards; BUILDER_RULES section 7 and plan section 9 ask for a grade on doctrine and statute results, not on definitions. Noted for the architect, not a FAIL."),
    "d-cards-schema": ("2.7 card schema (tools/check_pages.py cards.json rules)",
        "cards.json; tools/check_pages.py --unit LX2",
        "PASS fresh: 'check_pages LX2: PASS' (exit 0) with 101 cards: unique ids, valid lessons, valid grades, cite keys exist, grade-C results have a cite or basis."),
    "d-cards-coverage": ("2.7 coverage of lesson definitions, propositions, assumptions, misconceptions, key results by cards",
        "cards.json vs L01-L04",
        "PASS fresh counts per lesson (python -I): L01 33 cards, L02 19, L03 22, L04 27 (total 101). c104 adds the second sentence of section 15(d)(1) "
        "(L01.html line 106, Section 3). Coverage of the lesson's definitions, propositions, assumptions and misconceptions is unchanged otherwise."),
    "d-dup-scan": ("2.7 duplicate cards",
        "cards.json (101 cards)",
        "PASS fresh (python -I): 101 distinct ids; 0 duplicate fronts; 0 duplicate backs. c104 is a question about the second sentence of section 15(d)(1), "
        "distinct from c016 (third sentence ground), c015 (first sentence issuers) and c096 (fiscal-year exception)."),
    "d-atomic-split": ("2.7 one fact per card",
        "cards.json LX2-c027, c030, c041, c053, c058, c081, c090..c094, c100, c104",
        "PASS fresh on the changed cards: c027 back gives two statute facts answering one misconception; c030 and c081 backs each answer one question "
        "(c030 is one derivative claim; c081 is 'comply with it' plus the Code's floor); c104 is one fact. Other multi-clause cards as round 14."),
    "d-labs-run": ("2.5 labs: run, deterministic, twin under python -I -W error",
        "tests/labs/LX2/lab-LX2-L01..L04-1.py; tools/run_labs.py --unit LX2",
        "PASS fresh: 'run_labs LX2: PASS (7/7)' (exit 0). Each twin under python3 -I -W error exits 0 and its output is byte-identical to round 14 (scratch-LX2-d-r15/run-lab-LX2-L0{1..4}-1.out)."),
    "d-dodd-mifid-cards": ("2.7 removed and added cards for Dodd-Frank and MiFID concepts",
        "cards.json (LX2-c101..c103); course/modules/LX/LX2/L03.html Section 3",
        "PASS fresh: card_delta_r15.py: added ['LX2-c104'], removed [], changed c027, c030, c081. c101-c103 unchanged and still match Definitions 3.1, 3.2 "
        "(no provision stated). The registry holds no Dodd-Frank or MiFID record (round-14 scan, references.json unchanged since 8e5751c9)."),
    "d-dag": ("2.9 check_dag; no concept used before definition or outside closure (cards)",
        "tools/check_dag.py --unit LX2; cards.json",
        "PASS fresh: 'check_dag LX2: PASS' (exit 0). No card in cards.json contains a concept link or code; c104 cites only a registry key."),
    "d-gates-structure": ("2.9 structure gates run on this pin",
        "tools/check_pages.py --unit LX2; tools/check_dag.py --unit LX2; tools/run_labs.py --unit LX2; tools/verify_refs.py --offline",
        "PASS fresh on d1e65a02: check_pages LX2 PASS; check_dag LX2 PASS; run_labs LX2 PASS (7/7); verify_refs.py --offline "
        "'offline integrity: 560 entries, 0 problems'. check_projects and page_smoke not run (outside the cards delta; lesson pages unchanged)."),
    "d-notation": ("2.4 notation: cards' symbols against notation/notation.json",
        "cards.json (changed cards c027, c030, c081, c104 and the rest); notation/notation.json",
        "PASS fresh: changed cards introduce no symbol. c027 no longer names R13/R15 (readings, not notation). Symbols in cards remain G, R, X, C_m, C_t, e_t, h_t, y-hat_t, V_t, U_t, H, n, b1, b2; none is a registered symbol with another meaning."),
    "d-process-banned": ("2.9 process words and banned phrases in learner text (cards)",
        "cards.json; tools/check_pages.py --unit LX2",
        "PASS fresh scan of every front, back and basis (round-15 regex over verif, round, builder, architect, reviewer, audit, ledger, fragment, fixed, "
        "corrected, draft, TODO, TBD, lorem, for brevity, beyond the scope, obviously, clearly, plan, ellipsis): hits are legitimate uses only "
        "('fixed by the Commission', c025; 'draft the follow-up report', c087; 'rounded', c073, c085, c100; the lesson's Research problems R1, R2, R13, R15 and Lab 1 names)."),
    "d-mutants-r14": ("2.7 mutation check of the cards by planted errors (r13, r14 and r15 card mutants)",
        "ledgers/LX2/mutants/r13_card_mut1..5, r14_card_mut1..4, r15_card_mut1..4 (JSON card sets)",
        "PASS fresh. numeric check card_numbers_r15.py flags r13_mut1, r13_mut2, r13_mut4, r14_mut1, r14_mut4 (MISS). Manual kills against the current sources: "
        "r13_mut3 (c016 300 vs statute 15(d)(1) 300), r14_mut2 (c010 ten days vs 8(b)), r14_mut3 (c096 No vs 15(d)(1) 'other than the fiscal year'), "
        "r15_mut1 (c104 'automatically' vs statute), r15_mut2 (c027 13(a) vs 15(d)(1)), r15_mut3 (c081 'comply' vs III(A)), r15_mut4 (c086 MAE 2 vs 3). "
        "r13_mut5 changes a locator string that the current c003 no longer carries (moot)."),
    "d-registry-keys-r14": ("2.1 cite keys exist; no primary text invented for Dodd-Frank, MiFID II, SR 11-7/21-8",
        "references/references.json (560 entries, unchanged since 8e5751c9); cards.json cite arrays",
        "PASS fresh: check_pages cite check passes for all cite keys, including gpondsecuritiesb on c104 and c027. verify_refs --offline: 560 entries, 0 problems. "
        "Dodd/MiFID/SR 11-7/21-8 absence re-checked as in round 14 (registry unchanged)."),
    "d-quote-fidelity": ("2.1 quotes in cards match the sources",
        "cards.json curly-quoted passages; scratch-LX2-d-r11/src (statute, Dirks, O'Hagan, CFA, SR 26-2)",
        "PASS fresh (quotes_cards_r15.out): 18 curly-quoted passages; 17 FOUND verbatim. The one MISS, c068 'responsible for adopting model risk management practices ...', "
        "is a page-break split: sr2602a1.txt offset 1827 reads 'adopting model' then the page footer '1' and a form feed, then 'risk management practices'. "
        "The words are contiguous across the page break, so the quotation is accurate."),
    "d-delta-read": ("delta read: every hunk of the LX2 slice since the round-14 pin 8e5751c9",
        "git diff 8e5751c9 d1e65a02 -- course/modules/LX/LX2 curriculum references tests/labs/LX2 notation tools",
        "PASS: changed hunks are cards.json only (c027 back, c030 back, c081 front and back, new c104). curriculum/01-foundations.yaml and curriculum.json "
        "change only module M3's project brief (Covariance-matrix doctor), not LX2. All hunks read in full."),
    "d-grade-key-consistency": ("2.3 grades: card grades vs lesson key-results tables",
        "cards.json grades; L01-L04.html key-results tables",
        "PASS fresh: T cards (c017-c021, c051, c076-c079, c086) = 11, matching the T rows of the key-results tables. C cards carry C rows. "
        "c104 is C (statute quotation, as the second sentence of section 15(d)(1) is C in L01 section 3). No lab-only result is graded T."),
}
for rid, (check, loc, ev) in FRESH.items():
    rows.append({"id": rid, "check": check, "location": loc, "status": "PASS", "evidence": ev})

rows.append({
    "id": "d-cards-021-030", "check": "2.7 card vs current lesson; 2.6 statute and Model (LX2-c021..c030)",
    "location": "course/modules/LX/LX2/cards.json LX2-c030 back; course/modules/LX/LX2/L02.html line 80 (claim span, pp. 659-660)",
    "status": "FAIL",
    "evidence": "c021-c026, c028, c029 unchanged since 8e5751c9 and PASS (carried). c027 (changed) PASS, fresh: back 'Section 13(a) applies to an issuer of a "
                "security registered pursuant to section 12. The duty for an issuer with only an effective 1933 registration comes from section 15(d)(1).' "
                "matches L01.html line 386 and the misconception text (stripped L01 line 250) and the 1934 Act s15(d)(1) text in c1885.norm.txt. "
                "c030 (changed) FAIL: back 'In Dirks it is derivative: the tippee's duty comes from the insider's breach, and it arises only when the breach is established.' "
                "The opinion at Dirks p. 660 (dirks.norm.txt offset 34020, footnote 20 follows) reads: a tippee assumes a fiduciary duty 'only when the insider has breached "
                "his fiduciary duty to the shareholders by disclosing the information to the tippee and the tippee knows or should know that there has been a breach'. "
                "The card drops the tippee-knowledge limb and substitutes 'established', a proof-status term the source does not use. The same wording is in L02.html line 80.",
    "fix": "Replace the c030 back with: 'It is the liability of a tippee for trading on material nonpublic information received from an insider. In Dirks it is derivative: "
           "the tippee assumes the insider's duty only when the insider has breached by disclosing the information to the tippee and the tippee knows or should know that "
           "there has been a breach (Dirks, p. 660).' Make the same change to the claim span in course/modules/LX/LX2/L02.html line 80, so card and lesson agree, then re-run check_pages --unit LX2.",
})
rows.append({
    "id": "d-attrib-opinions", "check": "2.1 attribution; quotes and pinpoints (LX2-c028..c043)",
    "location": "cards.json LX2-c030 back (changed); LX2-c028..c043; course/modules/LX/LX2/L02.html line 80",
    "status": "FAIL",
    "evidence": "Quotations in c029, c031, c032, c034, c035, c037, c039, c041, c043 FOUND verbatim (quotes_cards_r15.out) and the printed pages re-read in round 14 are unchanged. "
                "c030 has no quotation, but its paraphrase is attributed to Dirks at pp. 659-660 and is not what p. 660 says (same defect as d-cards-021-030: "
                "'only when the breach is established' for 'only when the insider has breached ... and the tippee knows or should know').",
    "fix": "Same change as d-cards-021-030 (c030 back and L02.html line 80 claim span): state the Dirks p. 660 condition, both limbs, and cite the page.",
})
rows.append({
    "id": "d-l02-derivative-sentence", "check": "2.1 attribution; 2.3 grade (lesson claim span behind c030)",
    "location": "course/modules/LX/LX2/L02.html line 80 (claim span data-cite gpo1983dirks, data-locator pp. 659-660)",
    "status": "FAIL",
    "evidence": "The lesson sentence 'In Dirks it is derivative: the tippee's duty comes from the insider's breach, and it arises only when the breach is established.' "
                "is the wording behind c030. The quotation in the next sentence (Dirks p. 660, 'knows or should know that there has been a breach') states the second limb, "
                "which the paraphrase omits. Read in full against dirks.norm.txt (opinion text, offset 34020).",
    "fix": "Rewrite the sentence as in d-cards-021-030 so that the paraphrase states both conditions the opinion at p. 660 states. This row belongs to the L02 builder; the card follows the lesson.",
})
rows.append({
    "id": "d-l01-sec2-registration-ungraded", "check": "2.6 / 2.9 statute-content sentences need a claim span with a locator (L01 convention)",
    "location": "course/modules/LX/LX2/L01.html line 69 (Section 2, opening paragraph)",
    "status": "FAIL",
    "evidence": "Re-verified from the HTML this round. Line 69: 'A <dfn>registration statement</dfn> is the document that an issuer files with the Commission "
                "<span class=\"claim\" data-cite=\"gpondsecurities\" data-locator=\"section 2(a)(5)\">(the term “Commission” means ...)</span> to register a security under the 1933 Act.' "
                "The only claim span covers the parenthetical; the meaning sentence has no data-grade or data-locator. Statute: 1933 s2(a)(8) reads "
                "'The term registration statement means the statement provided for in section 6, and includes any amendment thereto' (c1884.norm.txt; statute_cfa_r15.out FOUND). "
                "The same line continues 'The definitions in section 2 do not define the phrase.' with no claim span. The statute check finds no 'in effect' definition in section 2 "
                "(statute_cfa_r15.out: ABSENT, section 2 length 18383 characters), so the sentence is true but ungraded. BUILDER_RULES section 2.1 requires a claim span on every substantive claim.",
    "fix": "Wrap the meaning sentence in a claim span with data-grade=\"C\" data-cite=\"gpondsecurities\" data-locator=\"section 2(a)(8); section 6\". Wrap 'The definitions in section 2 do not define the phrase.' "
           "in a claim span with data-grade=\"C\" data-cite=\"gpondsecurities\" data-locator=\"section 2\". Re-run check_pages --unit LX2.",
})
rows.append({
    "id": "d-c027-changed", "check": "2.7 card vs current lesson (LX2-c027, changed since 8e5751c9)",
    "location": "cards.json LX2-c027; course/modules/LX/LX2/L01.html lines 250 (misconception 4), 386 and 106",
    "status": "PASS",
    "evidence": "Fresh. The new back is a subset of the lesson's misconception 4: Section 13(a) applies to a section 12 registered issuer; the 15(d)(1) duty comes from an effective 1933 registration. "
                "The lesson's section 3 quotes 15(d)(1) first and second sentences (L01.html lines 105-106); c1885.norm.txt confirms both quotations. The removed sentences (R13/R15 pointer) "
                "are covered by Proposition 4.2 and c018; nothing in the new back is unsupported.",
})
rows.append({
    "id": "d-c081-changed", "check": "2.1 attribution; 2.7 card vs lesson (LX2-c081, changed since 8e5751c9)",
    "location": "cards.json LX2-c081; course/modules/LX/LX2/L04.html line 67 and Section 1",
    "status": "PASS",
    "evidence": "Fresh. Front 'Under the Code, what must a member do about a legally imposed fiduciary duty?' and back 'Comply with it ...' state the Guidance sentence "
                "'members and candidates must comply with any legally imposed fiduciary duty' (cfa-iii-a.norm.txt offset 7360, subheading at 6029, no intervening subheading). "
                "L04.html line 67 quotes the same guidance. 'The Code does not set a legal fiduciary duty' matches 'the Code and Standards neither impose such a legal responsibility' (offset 7405).",
})
rows.append({
    "id": "d-c104-new", "check": "2.1 statute quotation; 2.7 card vs lesson (LX2-c104, new since 8e5751c9)",
    "location": "cards.json LX2-c104; course/modules/LX/LX2/L01.html line 106 (Section 3 quote of 15(d)(1) second sentence)",
    "status": "PASS",
    "evidence": "Fresh. The back 'Automatically, if and so long as any issue of the issuer's securities is registered pursuant to section 12.' matches the 1934 Act s15(d)(1) second sentence "
                "in c1885.norm.txt: 'The duty to file under this subsection shall be automatically suspended if and so long as any issue of securities of such issuer is registered pursuant to section 12 of this title.' "
                "Lesson section 3 quotes the same sentence (L01.html line 106, claim span section 15(d)(1), second sentence). Grade C with cite gpondsecuritiesb is correct for a statute result. No duplicate of c016 or c096.",
})

ids_prev = set(prev_rows)
ids_new = {r["id"] for r in rows}
missing = ids_prev - ids_new
extra = ids_new - ids_prev
print("round-14 ids missing:", sorted(missing))
print("new ids:", sorted(extra))
assert not missing, missing

summary_rows = len(rows)
n_pass = sum(1 for r in rows if r["status"] == "PASS")
n_fail = sum(1 for r in rows if r["status"] == "FAIL")
MUTANTS = [
    {"name": "r13_card_mut1_c079_44_to_45", "description": "LX2-c079 back 44/117 changed to 45/117", "killed_by": "card_numbers_r15.py (MISS 45/117)"},
    {"name": "r13_card_mut2_c100_bias_41_12_to_41_13", "description": "LX2-c100 bias 41/12 changed to 41/13", "killed_by": "card_numbers_r15.py (MISS 41/13)"},
    {"name": "r13_card_mut3_c016_300_to_250", "description": "LX2-c016 holder count 300 changed to 250", "killed_by": "manual: statute 15(d)(1) third sentence, 300 persons (statute_cfa_r15.out)"},
    {"name": "r13_card_mut4_c053_3_104_to_3_105", "description": "LX2-c053 trader 1 fills 104 changed to 105", "killed_by": "card_numbers_r15.py (MISS 3/105)"},
    {"name": "r13_card_mut5_c003_2a8_to_2a5", "description": "LX2-c003 locator section 2(a)(8) changed to 2(a)(5)", "killed_by": "moot: the current c003 carries no locator (planted text absent)"},
    {"name": "r14_card_mut1_c079_44_to_45", "description": "LX2-c079 back 44/117 changed to 45/117", "killed_by": "card_numbers_r15.py (MISS 45/117)"},
    {"name": "r14_card_mut2_c010_ten_to_fifteen", "description": "LX2-c010 notice 'ten days' changed to 'fifteen days'", "killed_by": "manual: statute 8(b) ten days (statute_cfa_r15.out)"},
    {"name": "r14_card_mut3_c096_no_to_yes", "description": "LX2-c096 answer 'No' changed to 'Yes'", "killed_by": "manual: statute 15(d)(1) third sentence 'other than the fiscal year within which ... became effective'"},
    {"name": "r14_card_mut4_c085_3_8_to_3_9", "description": "LX2-c085 hit rate 3/8 changed to 3/9", "killed_by": "card_numbers_r15.py (MISS 3/9)"},
    {"name": "r15_card_mut1_c104_automatically_to_on_application", "description": "LX2-c104 'Automatically' changed to 'Only on the issuer's application'", "killed_by": "manual: statute 15(d)(1) second sentence 'automatically suspended'"},
    {"name": "r15_card_mut2_c027_15d_to_13a", "description": "LX2-c027 back: the 1933-only reporting duty attributed to section 13(a)", "killed_by": "manual: L01.html line 386 and statute 13(a) vs 15(d)(1)"},
    {"name": "r15_card_mut3_c081_comply_to_optional", "description": "LX2-c081 back: compliance with a legal fiduciary duty made optional", "killed_by": "manual: cfa-iii-a.norm.txt offset 7360 'must comply with any legally imposed fiduciary duty'"},
    {"name": "r15_card_mut4_c086_mae_3_to_2", "description": "LX2-c086 back: mean absolute error 3 changed to 2 (errors are +/-3)", "killed_by": "manual: run-lab-LX2-L04-1.out Part C errors +3 -3 +3 -3 (MAE 3, recomputed by card_arithmetic_check_r15.py)"},
]
frag = {
    "unit": "LX2",
    "slice": "d",
    "round": 15,
    "verifier": "Claude Haiku 5.5, independent verifier for LX2-d, round 15 (did not build LX2; shares no context with the builders)",
    "pin": "d1e65a0203e386e3246429ba1cf7e723eb6cfbfa",
    "base": "8e5751c903f0246115eba746afdf5d71f612bb37 (round-14 pin). Delta 8e5751c9..d1e65a02: course/modules/LX/LX2/cards.json only (changed c027, c030, c081; added c104); lessons, labs, registry, notation and tools byte-identical; curriculum.json changes only module M3.",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE15-LX2-d",
    "scratch": "/Users/billyribeiro/.fanout/scratch-LX2-d-r15 (stripped lessons scratch-LX2-d-r15-L0{1..4}.txt; card_numbers_r15.out; card_delta_r15.out; quotes_cards_r15.out; statute_cfa_r15.out; arith_r15.out; card_arithmetic_check_r15.out; run-lab-LX2-L0{1..4}-1.out; check_pages.out; check_dag.out; run_labs_all.out; verify_refs_offline.out)",
    "verified_at": "2026-11-09T01:25:25+00:00",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": MUTANTS,
    "registry_flags": prev["registry_flags"],
    "freshness_flags": [],
    "notes": [
        "Checkout: the worktree was at 9ca1d8cb on arrival; moved detached to the pin d1e65a02 (git checkout --detach) before any check.",
        "Scripts behind the rows are in ledgers/LX2/scripts/LX2-d-r15/: strip_lessons_r15.py, card_numbers_r15.py, card_delta_r15.py, quote_check_cards_r15.py, statute_cfa_attachment_checks_r15.py, page_locate_r15.py, card_arithmetic_r15.py (round-14 copies with paths), card_arithmetic_check_r15.py (new), write_fragment_r15.py.",
        "Carried rows (prefix 'Carried from round 14') are those whose cited card objects, lesson files, registry and labs are byte-identical since 8e5751c9. Every row touching c027, c030, c081 or c104 was re-verified from scratch.",
        "Grade observation (not a row): c001, c002, c003, c005 cite statute keys but carry no grade. They are definition cards; plan section 9 asks for grade C on doctrine and statute results. Architect to confirm.",
        "Lab-derived cards are graded C naming the lab (verifier rule 9); plan section 9 says 'grade T with basis' for lab-derived cards. Carried from round 14; architect to confirm.",
        "Not checked: the statute and opinion texts were read from the round-11 extractions (scratch-LX2-d-r11/src), not re-downloaded; the Dirks and O'Hagan printed pages come from those copies; check_projects and page_smoke were not run (no LX2 page or project change). Live CFA and Federal Reserve pages were not fetched.",
        "Round-15 new mutants (r15_card_mut1..4) were killed by manual reading and by the arithmetic script, not by the automated number check; the automated check cannot see wording errors.",
    ],
    "summary": {
        "slice": "LX2-d (all 101 cards.json cards against L01-L04)",
        "rows": summary_rows,
        "pass": n_pass,
        "fail": n_fail,
        "unverifiable": 0,
        "mutants_killed": len(MUTANTS),
        "mutants": len(MUTANTS),
    },
}
json.dump(frag, open(out_path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
open(out_path, "a", encoding="utf-8").write("\n")
print("rows", summary_rows, "pass", n_pass, "fail", n_fail, "mutants", len(MUTANTS))
