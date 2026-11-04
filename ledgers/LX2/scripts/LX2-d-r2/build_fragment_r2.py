"""Build the round 2 fragment ledgers/LX2/LX2-d.json from the rows the verifier established (see the scripts in this folder)."""
import json
import sys
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(sys.argv[1])
S = "ledgers/LX2/scripts/LX2-d-r2"

R = []


def row(id_, check, location, status, evidence, fix=""):
    R.append({"id": id_, "check": check, "location": location, "status": status, "evidence": evidence, "fix": fix})


ATTRIB = "2.6 statute attribution (card vs statute text)"
row("d-c010-8b-trigger", ATTRIB,
    "course/modules/LX/LX2/cards.json LX2-c010 (back, line 73); course/modules/LX/LX2/L01.html line 84", "FAIL",
    f"Card back: the Commission may issue a refusal order under section 8(b) with no condition. COMPS-1884 section 8(b) "
    f"(text in {S}/sources_checks_r2.out, phrase 'If it appears to the Commission that a registration statement is on its "
    f"face incomplete or inaccurate in any material respect' matches=1) conditions the order on that finding, after notice "
    f"and opportunity for hearing. grep -o 'incomplete or inaccurate' over cards.json and L0*.html returns nothing. The "
    f"round-2 commit 67c47689 reworded the back but kept the omission.",
    "Add to the back: the order issues only if it appears to the Commission that the registration statement is on its face "
    "incomplete or inaccurate in any material respect, after notice and opportunity for hearing (section 8(b)). Same change "
    "to L01.html line 84 (L01 owner).")
row("d-c016-abs-class", ATTRIB,
    "course/modules/LX/LX2/cards.json LX2-c016 (back, line 121); course/modules/LX/LX2/L01.html line 111", "FAIL",
    f"Card back: the duty is suspended if 'the securities of each class are held of record by less than 300 persons'. COMPS-1885 "
    f"section 15(d)(1), third sentence (text in {S}/sources_checks_r2.out): '... the securities of each class, other than any "
    f"class of asset-backed securities, to which the registration statement relates are held of record by less than 300 "
    f"persons'. grep 'asset-backed' over cards.json and L0*.html finds nothing in LX2 text.",
    "In the card back insert '(other than any class of asset-backed securities)' after 'the securities of each class'. "
    "Same insertion at L01.html line 111 (L01 owner).")
row("d-c025-8d-trigger", ATTRIB,
    "course/modules/LX/LX2/cards.json LX2-c025 (back, line 192); course/modules/LX/LX2/L01.html lines 85 and 378", "FAIL",
    f"Card back: 'after notice and an opportunity for hearing, the Commission may issue a stop order'. COMPS-1884 section 8(d) "
    f"(sources_checks_r2.out): the power arises 'If it appears to the Commission at any time that the registration statement "
    f"includes any untrue statement of a material fact or omits ...', after notice 'by personal service or the sending of "
    f"confirmed telegraphic notice'. The trigger is absent from the card and from both lesson passages.",
    "Add to the back the trigger: the stop order follows a finding that the statement includes an untrue statement of a material "
    "fact or omits a required or necessary material fact to make the statements not misleading, after notice by personal service "
    "or confirmed telegraphic notice and opportunity for hearing (section 8(d)). Same change to L01.html lines 85 and 378 (L01 owner).")
row("d-attrib-statute", ATTRIB, "course/modules/LX/LX2/cards.json LX2-c001..c027", "FAIL",
    f"All 27 L01 cards read against COMPS-1884/1885 (sources_checks_r2.out; sections 5(a), 5(c), 6(a), 6(c), 8(a), 12(a), 12(b), "
    f"12(d), 13(a), 15(d)(1) first and third sentences). Matches for c001-c009, c011-c015, c017-c024, c026, c027. Failures are "
    f"c010, c016 and c025.",
    "Apply the three rows d-c010-8b-trigger, d-c016-abs-class and d-c025-8d-trigger.")
row("d-cards-001-010", "2.7 card vs lesson and statute", "course/modules/LX/LX2/cards.json LX2-c001..c010", "FAIL",
    "c001-c009 agree with L01 lines 69-109 and section 5 (read in full, lab and text). c001 back now matches L01 line 74. c010 FAILS: d-c010-8b-trigger.",
    "See d-c010-8b-trigger.")
row("d-cards-011-020", "2.7 card vs lesson and statute", "course/modules/LX/LX2/cards.json LX2-c011..c020", "FAIL",
    "c011-c015 match 12(a), 12(b), 12(d) and 15(d)(1) first sentence; c017-c020 match Propositions 4.1-4.3 and the state and transition counts (lab printout: 10 states, 22 transitions, L01 twin). c016 FAILS: d-c016-abs-class.",
    "See d-c016-abs-class.")
row("d-cards-021-030", "2.7 card vs lesson and statute", "course/modules/LX/LX2/cards.json LX2-c021..c030", "FAIL",
    "c021-c024, c026-c029 match L01 lines 119-129, 134, 176-184, 200 and L02 lines 65-69. c025 FAILS: d-c025-8d-trigger. c022 and c030 edits in commit 67c47689 verified against L01 line 134 and L02 line 80.",
    "See d-c025-8d-trigger.")
row("d-cards-031-040", "2.7 card vs lesson and opinions", "course/modules/LX/LX2/cards.json LX2-c031..c040", "PASS",
    f"Opinion quotations and pages verified with {S}/opinion_pages.py over USREPORTS-521-642 and 463-646 (c029 p.652, c033 p.663, c034 p.664, c035 p.655, c036 p.656, c039 p.654, c040 p.660, c037 p.663 n.23). Lesson L02 lines 66-103 read in full. c038 counts (4 of 8) match the lab printout.")
row("d-cards-041-050", "2.7 card vs lesson and opinions", "course/modules/LX/LX2/cards.json LX2-c041..c050", "PASS",
    "c041 p.662 quotation verified; c042 footnote 5 'O'Hagan was not an \"insider\" of Pillsbury' verified in USREPORTS-521-642 (page 653); c043 footnote 7 at p.655 verified. c044-c050 match L03 Definition 1.1, Remark 1.2, Definition 1.3 and Assumption A1 (L03 lines 58-77).")
row("d-cards-051-060", "2.7 card vs lesson and lab", "course/modules/LX/LX2/cards.json LX2-c051..c060", "FAIL",
    "c051 (identity re-derived; the proof sums per-order routes and uses A1), c052, c053 (3/104 vs 6/97; 3*97=291<624 in recompute_cards_r2.out), c054-c057 (c056/c057 backs now name distinct instruments) PASS. c058 and c059 are correct cards whose grade disagrees with the lesson's key-results rows: d-c058-grade and d-c059-grade.",
    "Apply d-c058-grade and d-c059-grade.")
row("d-cards-061-070", "2.7 card vs lesson and sources", "course/modules/LX/LX2/cards.json LX2-c061..c070", "PASS",
    "c064 quotation verified in cfa-standards-of-practice-iii-a.html (Guidance paragraph 2, sources_checks_r2.out); c065 VI(A) Guidance; c066-c067 attachment p.3 (pdf_pages_r2.py); c068 'pp. 1-2' (phrase on pdf pages 1 and 2); c069 p.9 (Outcomes Analysis on pdf page 9); c070 band 2 inclusive matches L04 Definition 4.1.")
row("d-cards-071-080", "2.7 card vs lesson and mathematics", "course/modules/LX/LX2/cards.json LX2-c071..c080", "PASS",
    "c071-c075 match L04 Definition 4.1 and Assumptions A1/A2 (L04 line 123; A2 used in Problem E3 and Section 5, L04 line 373). c073 rounding rule matches the lab's round_half_away. c076-c078 theorems re-proved on the page (triangle inequality and P,N argument checked). c078 expectation 1 and c079 44/117 recomputed by enumeration (recompute_cards_r2.out).")
row("d-cards-081-089", "2.7 card vs lesson and sources", "course/modules/LX/LX2/cards.json LX2-c081..c089", "FAIL",
    "c081 (Guidance paragraph 2), c082 (letter first body paragraph and Supersedes list), c083 (Applicability line), c084 (no 'hit' or 'bias' in att.txt or letter.txt), c086 (Part C by hand), c087 (Example 3), c088 and c089 (page 2, footnote 1) PASS. c085 values verified (3/8, 41/12, 0.3750, 3.4167) but its grade disagrees with L04 key results: d-c085-grade.",
    "Apply d-c085-grade.")
row("d-dup-scan", "2.7 duplicate scan", "course/modules/LX/LX2/cards.json (89 cards)", "PASS",
    f"{S}/cards_checks_r2.out: exact duplicate fronts or backs: none. Near-duplicate pairs: c056/c057 (backs differ only by the instrument name, fronts differ) and c071/c072 (hit rate vs bias).")
row("d-dup-c056-c057", "2.7 duplicate scan", "course/modules/LX/LX2/cards.json LX2-c056, LX2-c057", "PASS",
    "Round 1 failure (identical backs) is fixed: c056 back 'Only its name, the Dodd–Frank Act, as one of the unit's concepts...', c057 back 'Only its name, MiFID II, as ...'. Both match L03 lines 259 and 261.")
row("d-c058-grade", "2.3 grade vs lesson key results", "course/modules/LX/LX2/cards.json LX2-c058 (grade C); course/modules/LX/LX2/L03.html line 505", "FAIL",
    f"Card grade is C with basis 'Lab 1 printed output (SIMULATED flow, seed 2026)', which is the correct grade for a SIMULATED lab result (VERIFIER_RULES 2.2 and 9). The lesson's key-results row says 'not graded (SIMULATED output)', so card and lesson disagree, and 'not graded' is not an allowed grade. Printed lines 'events with a crossed book: 0' and 'events where entered != ...: 0' confirmed in the lesson ({S}/lab_output_in_lesson.out).",
    "L03.html line 505 grade cell: change 'not graded (SIMULATED output)' to 'C' (L03 owner). The card needs no change.")
row("d-c059-grade", "2.3 grade vs lesson key results", "course/modules/LX/LX2/cards.json LX2-c059 (grade C); course/modules/LX/LX2/L03.html line 506", "FAIL",
    "Card grade C with basis naming the SIMULATED flow and the demonstration threshold. Lesson key-results row says 'not graded (demonstration value)'. The printed 'traders flagged: 0 of 6' and 'largest ratio 21/37' come from the SIMULATED flow (L03 lines 343-344 match the twin output in lab_output_in_lesson.out).",
    "L03.html line 506 grade cell: change 'not graded (demonstration value)' to 'C' with the SIMULATED basis (L03 owner). The card needs no change.")
row("d-c085-grade", "2.3 grade vs lesson key results", "course/modules/LX/LX2/cards.json LX2-c085 (grade C); course/modules/LX/LX2/L04.html line 434", "FAIL",
    "Card grade C with basis 'Lab 1, Part A (SIMULATED path, seed 20261103)'. Correct under VERIFIER_RULES 9. The lesson key-results row at L04.html line 434 says 'not graded (SIMULATED output)', so card and lesson disagree. Values 3/8 and 41/12 recomputed from the Part A printout (recompute_cards_r2.out).",
    "L04.html line 434 grade cell: change 'not graded (SIMULATED output)' to 'C' (L04 owner). The card needs no change.")
row("d-schema", "2.7 schema and ids", "course/modules/LX/LX2/cards.json", "PASS",
    f"{S}/cards_checks_r2.out: 89 cards, ids LX2-c001..c089 contiguous and unique; lesson in range (L01 c001-027, L02 c028-043, L03 c044-063, L04 c064-089); every grade in T/A/B/C/D/X; every graded card has cite or basis. check_pages.py --unit LX2 (ledgers/LX2/scripts/LX2-d-r2/check_pages.out) PASS.")
row("d-coverage", "2.7 coverage", "course/modules/LX/LX2/cards.json", "PASS",
    "Each lesson has cards for its definitions, propositions, lab results and misconceptions (L01 27, L02 16, L03 20, L04 26 cards). Every key definition of L01-L04 read in the lesson has a card.")
row("d-quotes-in-lesson", "2.7 quotations", "course/modules/LX/LX2/cards.json (every curly-quoted span)", "PASS",
    f"{S}/cards_checks_r2.out: every “...” span in the cards occurs in the lesson text or in a fetched source. The single-quote hits in that output are apostrophe artefacts of the regex and are not quotations.")
row("d-labels-locators", "2.1 locators", "course/modules/LX/LX2/cards.json (every basis and locator)", "PASS",
    "Pages checked with opinion_pages.py: p.651, 652, 654, 655, 656, 660, 662, 663, 664, footnotes 5 (653), 7 (655), 23 (663). SR 26-2 attachment: pp. 1-2 (c068), p.2 (c089), p.9 (c069) by pdf_pages_r2.py. Lab basis names match the twin outputs.")
row("d-numbers", "2.2 numbers in cards", "course/modules/LX/LX2/cards.json (every digit token)", "PASS",
    f"cards_checks_r2.out: every digit token in a card occurs in its lesson. recompute_cards_r2.out recomputes 3/8, 41/12, 0.3750, 3.4167, 9 hits, 82 summed errors, 44/117 ~ 0.3761 (117 pairs, 44 hits), E[e]=1, 6/97 and 3/104, 21/37 largest, 5/34 vs 6/29, Part C bias 0 and MAE 3, rounding 41/12 -> 3.4167.")
row("d-run-labs", "2.5 labs", "tests/labs/LX2 twins L01-L04", "PASS",
    f"tools/run_labs.py --unit LX2: 'run_labs LX2: PASS (7/7)' ({S}/run_labs.out). Each L01-L04 twin run alone with python -I -W error: exit 0 (outputs saved as {S}/lx2d-r2-lab-LX2-L0x-1.py.out). lab_output_in_lesson.py: 39, 22, 17, 48 printed lines, 0 missing from the lesson text.")
row("d-attrib-opinions", "2.1 attribution (opinions)", "course/modules/LX/LX2/cards.json LX2-c028..c043", "PASS",
    "All opinion quotations on these cards located in USREPORTS-463-646 (Dirks) and USREPORTS-521-642 (O'Hagan) with the printed page (opinion_pages.py). Round 2 re-check of pages 651-656, 660-664 and footnotes 5, 7, 23.")
row("d-attrib-sr2026", "2.1 attribution (SR 26-2)", "course/modules/LX/LX2/cards.json LX2-c066..c069, c082..c084, c089", "PASS",
    "letter.txt: 'supersedes and replaces SR letter 11-7 ... and SR letter 21-8' (first body paragraph, line 30) and Supersedes list (line 57); Applicability 'over $30 billion in total assets regulated by the Federal Reserve'. att.txt: model definition (p.3), model-risk definition (p.3), 'responsible for adopting model risk management practices that are appropriate and effective' (pp.1-2), Outcomes Analysis p.9, footnote 1 and enforceable-standards sentence p.2. 'hit' and 'bias' absent from att.txt and letter.txt.")
row("d-attrib-cfa", "2.1 attribution (CFA Code)", "course/modules/LX/LX2/cards.json LX2-c064, c065, c080, c081, c087, c088", "PASS",
    "cfa-standards-of-practice-iii-a.html and -vi-a.html (plain curl, sources_checks_r2.out): 'often imposed by law or regulation...' (III(A) Guidance para 2); 'neither impose such a legal responsibility'; 'does not render all members and candidates fiduciaries'; VI(A) definition of conflict; Example 3 (Fargmon) with 'Best practice is to avoid the conflict by asking his employer to assign another analyst'.")
row("d-grades", "2.3 grades of cards", "course/modules/LX/LX2/cards.json (every grade)", "PASS",
    "Re-graded against BLUEPRINT §3: T on the theorems and counts proved on the page (c017-c021, c051, c052, c054, c076-c079, c086); C on statute, Code, SR and lab-output cards; no card grades a lab output as T. The cross-document grade disagreements are separate rows (d-c058-grade, d-c059-grade, d-c085-grade).")
row("d-notation", "2.4 notation", "course/modules/LX/LX2/cards.json (symbols)", "PASS",
    "notation/notation.json registers T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, Q. No card uses those symbols with another meaning. R (resting shares, c051) and H, h_t, e_t, b, U_t, V_t are not registered and are defined locally in L03/L04.")
row("d-banned-process", "2.9 banned phrases", "course/modules/LX/LX2/cards.json", "PASS",
    "Scan for TODO, TBD, lorem, 'for brevity', 'beyond the scope', 'it is important to note', 'clearly', 'obviously', ellipses and process words (round, verifier, builder, ledger, pin): none (the one 'round' hit is inside 'ground').")
row("d-dag", "2.9 DAG and concepts", "course/modules/LX/LX2/cards.json", "PASS",
    f"tools/check_dag.py --unit LX2: PASS ({S}/check_dag.out). Cards name only concepts defined in their own lesson or the lesson's stated uses.")
row("d-tools", "gates", "tools/check_pages.py --unit LX2; tests/test_page_checks.py", "PASS",
    f"check_pages.py --unit LX2: PASS (includes the cards.json schema check, {S}/check_pages.out). pytest tests/test_page_checks.py: all pass.")
row("d-refs-keys", "2.1 registry keys", "references/references.json; cards cite gpondsecurities, gpondsecuritiesb, gpo1997united, gpo1983dirks, frb2026fed, cfandcode", "PASS",
    f"All six keys present (560 entries). verify_refs.py --offline: '560 entries, 0 problems' ({S}/verify_refs_offline.out). verify_refs.py --unit LX2 (live): '6 of 560 entries, 0 problems' ({S}/verify_refs_unit_live.out).")
row("d-c051-prop22", "2.4 mathematics", "course/modules/LX/LX2/cards.json LX2-c051; L03 Proposition 2.2", "PASS",
    "Identity G = R + 2X + C_m + C_t re-derived from A1 (each order's shares partition into filled, cancelled, resting; each execution adds q to two distinct orders; market and trader cancels disjoint). Card front now quantifies over a moment after an event, matching L03 line 82.")
row("d-c086-hand-path", "2.3 grade and numbers (hand-built path)", "course/modules/LX/LX2/cards.json LX2-c086", "PASS",
    "Errors +3, -3, +3, -3: sum 0 (bias 0), |e|=3 > 2 (hit rate 0), mean absolute error 3, matching the Part C printout. Grade T is defensible: the numbers are arithmetic on a hand-built path, not a SIMULATED output, and Theorem 4.3 is proved on the page.")
row("d-r2-delta-cards", "2.7 round 2 delta of cards.json", "course/modules/LX/LX2/cards.json (67c47689 edits)", "PASS",
    "Changed cards c001, c022, c030, c032, c051, c053, c056, c057, c058, c059, c068, c069, c075, c085, c088, c089 were re-verified in this round (rows above). c010 was reworded but still omits the 8(b) trigger (row d-c010-8b-trigger).")
row("d-r2-lesson-delta", "2.9 round 2 delta of lesson text", "course/modules/LX/LX2/L01.html..L04.html (text delta)", "PASS",
    f"{S}/lesson_delta_r2.out: changed text lines L01 40, L02 32, L03 18, L04 34. Every changed line read (diff of tag-stripped text). Card-facing changes checked: L02 line 101 (footnote 5), L03 lines 259-261, L03 line 82 and 93 (Prop 2.2), L04 lines 62 and 297-302 (A2; key-results rows, see d-c085-grade).")

PRIMARY = {
    "unit": "LX2",
    "slice": "LX2-d",
    "round": 2,
    "verifier": "Claude Haiku 5.5, independent verifier for LX2-d, round 2 (did not build LX2; shares no context with the builders)",
    "pin": "67c47689c49435bc0e6639e3de4feded5eefdd64",
    "base": "1c1645f3b00eada2fb54d39c86d5d949e15b4fbc (round 1 pin; delta read in full)",
    "checkout": str(ROOT),
    "scratch": "/tmp/lx2d-r2-src (sources fetched by ledgers/LX2/scripts/LX2-d-r2/fetch_sources_r2.sh); /tmp/lx2d-r2-*.txt (tag-stripped lesson text from strip_lines.py)",
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "verdict": "FAIL",
    "rows": R,
    "mutants": [],
    "registry_flags": [
        "gpo1983dirks: registry title reads 'Dirks v. SEC, 463 U.S. 646 (1982)' and year is 1983; the opinion reads 'Argued March 21, 1983-Decided July 1, 1983' (USREPORTS-463-646.txt line 14). The citation year should be 1983. Architect to correct via add_reference.py.",
        "frb2026fed: the registry URL is the letter page (sr2602.htm). The attachment statements the cards quote (model definitions, Outcomes Analysis p.9, footnote 1) are in sr2602a1.pdf, which the letter links. Architect to confirm the attachment is part of the record.",
        "cfandcode: the registry URL is the CFA landing page. The quoted Guidance and Example 3 are on the Standards of Practice III(A) and VI(A) pages it links. Architect to confirm.",
    ],
    "freshness_flags": [],
    "notes": (
        "Round 2 on pin 67c47689. Read cards.json (89 cards) in full and all four lesson pages in full (tag-stripped text, "
        "L01 49 KB, L02 43 KB, L03 32 KB, L04 41 KB), plus the round 1 to round 2 text delta of each. Three statute defects "
        "from round 1 remain unfixed (c010, c016, c025; lesson owners L01 lines 84, 85, 111, 378). The round 1 grade defects "
        "on the cards are fixed, but the lesson key-results rows still say 'not graded' where the cards say C "
        "(L03.html lines 505-506, L04.html line 434). Lesson-level defects outside this slice, for the owners: "
        "L02.html line 617 (quiz explanation for option 3) says the text at p. 663 says scienter 'is relevant in some cases to "
        "whether the tipper has violated his duty'; Dirks n.23 says only that 'motivation is not irrelevant to the issue of "
        "scienter' (opinion_pages.py, USREPORTS-463-646). Not checked: footnote placement of the 10(b) quotation in Dirks (c032, "
        "the lesson's statement 'in a footnote' was taken as read); the CFA Guidance paragraph count is by <p> index in the "
        "fetched HTML; no later version of SR 26-2 searched; ruff, mypy --no-incremental and the full pytest suite not run (no "
        "Python source in this slice changed; only test_page_checks.py was run); page_smoke, run_graders, fetch_data not run "
        "(rendering, grader and dataset slices). No mutants: this slice has no grader."
    ),
    "summary": (
        "LX2-d round 2 on 67c47689: verdict FAIL. Rows: see counts below. Open FAILs: three statute attributions (c010 8(b) "
        "trigger, c016 asset-backed carve-out, c025 8(d) trigger) that the 67c47689 commit did not fix; three grade cells in "
        "L03 and L04 key-results tables that contradict the cards (c058, c059, c085). All other cards PASS on re-verification: "
        "the round 1 duplicate, grade and wording defects are fixed."
    ),
}
counts = {"PASS": 0, "FAIL": 0, "UNVERIFIABLE": 0}
for r in R:
    counts[r["status"]] += 1
PRIMARY["summary"] += f" Rows: {len(R)} (pass={counts['PASS']} fail={counts['FAIL']} unverifiable={counts['UNVERIFIABLE']})."
PRIMARY["verdict"] = "PASS" if counts["FAIL"] == 0 and counts["UNVERIFIABLE"] == 0 else "FAIL"
out = ROOT / "ledgers/LX2/LX2-d.json"
out.write_text(json.dumps(PRIMARY, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("wrote", out, "rows", len(R), counts)
