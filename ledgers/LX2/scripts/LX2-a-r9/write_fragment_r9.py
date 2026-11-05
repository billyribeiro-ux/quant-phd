import json, subprocess
PIN = "c93dd526025c6dffd34c54cd2c89eb62a890f885"
BASE = "0dee921a33dc1275ff9b1babc6c2fdf3daac62c3"
prev = json.load(open("/Users/billyribeiro/.fanout/frags/E-LX2-a.round8.json"))
CARRY_IDX = "Carried from round 8 (course/modules/LX/LX2/index.html byte-identical since the previous pin 0dee921a, git diff empty): "
CARRY_L01 = "Carried from round 8 (course/modules/LX/LX2/L01.html and tests/labs/LX2/lab-LX2-L01-1.py byte-identical since the previous pin, git diff empty): "
RERUN = "Re-run round 9 at c93dd52: "
REVER = "Re-verified round 9 by full read of course/modules/LX/LX2/L02.html (lines 1-675) and the round-9 scripts: "
# id -> (status, prefix, evidence override or None)
over = {
 "LX2a-cmd-check_pages": ("PASS", RERUN, "check_pages LX2: PASS (ledgers/LX2/scripts/LX2-a-r9/out_commands_r9.txt)."),
 "LX2a-cmd-check_dag": ("PASS", RERUN, "check_dag LX2: PASS (out_commands_r9.txt)."),
 "LX2a-cmd-run_labs": ("PASS", RERUN, "run_labs LX2: PASS (7/7) (out_commands_r9.txt)."),
 "LX2a-lab-isolated": ("PASS", RERUN, "ledgers/LX2/scripts/LX2-a-r9/lab_twin_check_r9.py: lab-LX2-L01-1 page_code_equals_twin=True exit=0 stderr_bytes=0 expected_equals_output=True; lab-LX2-L02-1 same (out_lab_twin_r9.txt). Direct python3 -I -W error runs of both twins: exit 0."),
 "LX2a-cmd-page_smoke": ("PASS", RERUN, "page_smoke LX2 for index, L01 and L02, each run alone: PASS, exit 0 (out_commands_r9.txt)."),
 "LX2a-cmd-ruff-mypy": ("PASS", RERUN, "ruff check: All checks passed; ruff format --check: 2 files already formatted; mypy --no-incremental: Success, no issues in 2 source files (out_lint_r9.txt)."),
 "LX2a-cmd-pytest": ("PASS", RERUN, "pytest tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py: exit 0, 100% (out_pytest_r9.txt). The full tests/ directory was not run."),
 "LX2a-cmd-verify_refs": ("PASS", RERUN, "verify_refs.py --offline: 560 entries, 0 problems (out_verify_refs_offline_r9.txt); verify_refs.py --unit LX2 (live): 6 of 560 entries, 0 problems (out_verify_refs_live_r9.txt)."),
 "LX2a-quote-search": ("PASS", REVER, "The Thomas quotation at L02.html:109 is now “the Commission’s misappropriation theory fails to provide a coherent and consistent interpretation”. ohagan.txt line 1796 (fetched by curl, sha256 identical to round 8) reads “Because the Commission’s misappropriation theory fails to provide a coherent and consistent interpretation” (hyphenation at line end only). Page: ohagan.txt page header 680 at line 1782 precedes it, so p. 680 is correct. Scalia quotation at p. 679 (pdfpage 38) also verified. Script: out_quotecheck_L02_r9.txt and out_loccheck_L02_r9.txt."),
 "LX2a-L02-opinion-quotes": ("PASS", REVER, "quotecheck over all L02 quotations: every quotation found verbatim in dirks.txt or ohagan.txt except (a) quote-mark style (single quotes for nested double quotes) and (b) three lab or misconception labels that are not opinion quotations (out_quotecheck_L02_r9.txt). Bracketed alterations [A], [s], [T], [p], [u], [t], [I] checked by hand against dirks.txt and ohagan.txt."),
 "LX2a-L02-remark-3.3": ("PASS", REVER, "L02.html:97 now reads: the benefit test is at p. 662 (dirks.txt, pdfpage 17 = p. 662 contains 'Thus, the test is whether'); 'The tippee's knowledge is a separate condition, which the opinion states at p. 660' - 'knows or should know' is at p. 660 (dirks.txt pdfpage 15 = p. 660). 'the lab checks it as its own element': twin line 15 (docstring) and line 240 (Check 'tippee knew or should have known of the breach', key gpo1983dirks, p. 660) confirm. No contradiction remains."),
 "LX2a-counter-evidence": ("PASS", REVER, "L02.html:90 (Blackmun dissent, pdfpage 23 = p. 668 'engrafts'), :109 (Thomas p. 680, Scalia p. 679, both verified), :570-580 (key results rows) all re-checked against dirks.txt and ohagan.txt."),
 "LX2a-L02-B3-B1": ("PASS", REVER, "Whole-page read of L02.html lines 1-675 this round: lesson, lab, misconceptions, problems, key results and quiz agree with the twin output (out_lab_twin_r9.txt) and with the cards."),
 "LX2a-L02-E2-E3-scratch": ("PASS", REVER, "Scratch copies of the twin (ledgers/LX2/scripts/LX2-a-r9/ scratch run in /tmp/lx2a_r9_scratch): E3 P7 source_told False gives 'fired: P1, P3, P4, P6, P7 (5 of 8)', P7 at gpo1997united p. 652; E2 P2 reputational gives 'fired: P1, P2, P3, P4, P6 (5 of 8)' with P2 row at p. 660; both match L02.html:530 and :537. Scratch M3 (P3 benefit none) gives P3 not fired at p. 662, as at L02.html:487."),
 "LX2a-L02-M3-scratch": ("PASS", REVER, "Scratch run of P3 benefit none: P3 'fails: tipper's personal benefit (none)', gpo1983dirks p. 662, matching L02.html:487."),
 "LX2a-r8-delta": ("PASS", "Round 8 row kept for id continuity; superseded by LX2a-r9-delta: ", "The round-8 delta (06994db1..0dee921a) is no longer the delta under review. Its findings are re-verified above (quote and Remark rows now PASS)."),
}
rows = []
for r in prev["rows"]:
    rid = r["id"]
    if rid in over:
        st, pre, ev = over[rid]
        rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": st,
                     "evidence": pre + ev})
    elif r["location"].startswith("course/modules/LX/LX2/index.html") or r["location"].startswith("index"):
        rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": r["status"],
                     "evidence": CARRY_IDX + r["evidence"]})
    elif r["status"] == "PASS" and ("L01" in r["location"]) and not ("L02" in r["location"]):
        rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": "PASS",
                     "evidence": CARRY_L01 + r["evidence"]})
    else:
        rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": r["status"],
                     "evidence": ("Re-verified round 9 (L02.html read in full; scripts in ledgers/LX2/scripts/LX2-a-r9/): " + r["evidence"]) if r["status"] == "PASS" else r["evidence"]})
new = [
 {"id": "LX2a-r9-delta", "check": "Round-9 delta since the round-8 pin 0dee921a for the slice-a files (index.html, L01.html, L02.html, both twins) and the LX2 cards",
  "location": "git diff 0dee921a..c93dd52 -- course/modules/LX/LX2 tests/labs/LX2 (6 LX files changed: L02.html, cards.json, project.html in LX2; L03.html, cards.json, project.html in LX1)",
  "status": "PASS",
  "evidence": "index.html, L01.html, both lab twins: byte-identical (git diff empty). L02.html hunks read in full: line 97 (Remark 3.3), line 104 (Definition 4.1 quotation paragraph, unchanged quote), line 107 (paraphrase 'treats ... as the core of the theory'; quotation at p. 654 'central' verified), line 109 (Thomas quotation, verified), line 535 (E3 wording, verified by scratch run). cards.json hunks: c010, c016, c024 (L01, see rows below); c023 (L01, grade and basis); c054 (L03), c082 and c085 (L04), c100 (L04, new), and the L03 basis/grade lines (not slice a). glossary.json and program.json hunks concern M3 (not slice a)."},
 {"id": "LX2a-card-c010", "check": "Card agrees with the current L01 text and every card number appears in its lesson (rule 10)",
  "location": "course/modules/LX/LX2/cards.json LX2-c010 (back); L01.html:84 (§2, Section 8(b) paragraph)",
  "status": "FAIL",
  "evidence": "The card back was changed this round to 'after notice by personal service or the sending of confirmed telegraphic notice not later than ten days after the filing of the registration statement, and opportunity for hearing within ten days after such notice'. The statute text is accurate: comps1884.txt lines 1770-1776 read 'after notice by personal service or the sending of confirmed telegraphic notice not later than ten days after the filing of the registration statement, and opportunity for hearing (at a time fixed by the Commission) within ten days after such notice'. But the lesson (L01.html:84) says only 'after notice and opportunity for hearing', and the figure 'ten days' is not stated for section 8(b) anywhere in L01.html (the only 'ten' is 'These ten paths' at L01.html:328). Rule 10 requires every card number to appear in its lesson; the card now carries a figure the lesson does not.",
  "fix": "Either add the ten-day notice and hearing periods to the section 8(b) quotation in L01.html §2 (builder edit to the lesson, then regenerate cards), or revert the card back to the lesson's wording 'after notice and opportunity for hearing', with no figure. Do not edit cards.json by hand (BLUEPRINT rule: generated from sources)."},
 {"id": "LX2a-card-c016", "check": "Card agrees with the current L01 text and every card number appears in its lesson (rule 10)",
  "location": "course/modules/LX/LX2/cards.json LX2-c016 (back); L01.html:111 (§3, third sentence of section 15(d)(1))",
  "status": "FAIL",
  "evidence": "The card back now gives '1,200 persons' for a bank, savings and loan holding company or bank holding company. The statute supports it: comps1885.txt lines 11122-11126 read '...held of record by less than 300 persons, or, in the case of a bank, a savings and loan holding company ... or a bank holding company ... 1,200 persons'. But the lesson says only 'with a different count for certain banks' (L01.html:111) and the string '1,200' appears nowhere in course/modules/LX/LX2/*.html (grep, round 9; automated card-number check flagged only LX2-c016). Rule 10 is violated by the same mechanism as c010.",
  "fix": "Either state the 1,200-person count in L01.html §3 (builder edit to the lesson, then regenerate cards), or restore the card wording 'with a different count for certain banks'. Do not edit cards.json by hand."},
 {"id": "LX2a-cards-L01-other", "check": "L01 cards c001-c009, c011-c015, c017-c027, c090-c092, c095-c096 agree with the current L01 text, the lab output and the statute",
  "location": "course/modules/LX/LX2/cards.json (L01 cards except c010 and c016); L01.html §2-§6, Lab 1 printed output at L01.html:275-313",
  "status": "PASS",
  "evidence": "Read each card against L01.html and the statute text in comps1884.txt/comps1885.txt. Card c023 (grade C added, basis 'Lab 1 printed state table') matches lab rows effective/not_listed and effective/listed with sale yes (L01.html:285-286). Card c024 (grade C added) matches L01.html:373-374 (misconception 1) and the filed row 'offer yes, sale no' (L01.html:281). Card c020 (10 states) and c021 (22 transitions: 6x2 + 2x5) match L01.html:115-122. Cards c090-c092 quote the printed lines 'reachable from unregistered/not_listed: 10 of 10', 'states where both reporting duties apply: 0', 'states where a sale is permitted and an offer is not: 0' (L01.html:289-290, 277). Card c096 matches L01.html:111 ('other than the fiscal year in which the registration statement became effective'). Card c025 matches misconception 2 (L01.html:378). Propositions c017-c019 match L01.html:322-352. No duplicate card ids or fronts (automated check)."},
 {"id": "LX2a-cards-L02", "check": "L02 cards c028-c043 and c097-c099 agree with the current L02 text",
  "location": "course/modules/LX/LX2/cards.json (L02 cards); L02.html §2-§7 and key results",
  "status": "PASS",
  "evidence": "No L02 card changed in this delta. Each card was read against the current L02.html text, including the changed lines 97, 107, 109 and 535. Card c037 (scienter, Dirks p. 663 n. 23) matches L02.html:61. Card c039 (Dirks p. 654 quotation) matches L02.html:456 and dirks.txt pdfpage 9. Card c040 (p. 660) matches L02.html:457. Card c041 (p. 662 quotation) matches L02.html:458. Card c034 quotations 'a question of fact' and 'will not always be easy for courts' verified (dirks.txt pdfpage 19, p. 664). Card c042 and c043 match L02.html:459 and :448 (p. 653 n. 5; p. 655 n. 7). Cards c097 to c099 match L02.html:85, L02.html:122-123."},
 {"id": "LX2a-cards-dup", "check": "No duplicate card ids or fronts in LX2 cards.json",
  "location": "course/modules/LX/LX2/cards.json (100 cards)",
  "status": "PASS",
  "evidence": "Python check round 9: no duplicate ids, no duplicate fronts across all 100 cards (L01 32, L02 19, L03 22, L04 27)."},
 {"id": "LX2a-r9-quotes-L02", "check": "Every quotation in L02.html checked against the fetched opinions (verbatim, page printed)",
  "location": "course/modules/LX/LX2/L02.html (all claim spans with a quoted passage and a gpo key)",
  "status": "PASS",
  "evidence": "ledgers/LX2/scripts/LX2-a-r9/loccheck.py ran over every claim span of L02.html that carries a quoted passage and a gpo key: 43 quotation checks located on a page inside the cited locator. 5 checks did not match by script, for two reasons: quotation-mark style (single quotes for nested double quotes) or a quotation that runs across a page break. Each was checked by hand with pdftotext per page: O'Hagan p. 651 (ohagan.txt line 485) and p. 652 (line 513) for the classical and misappropriation quotations; Dirks p. 654 (dirks.txt lines 364-370, pdfpage 9) for the [A]n insider quotation; O'Hagan p. 655 (ohagan.txt lines 649-652, pdfpage 14) for the disclosure quotation, which appears twice (L02.html:107 and the quiz explanation at L02.html:622). All five pass."},
 {"id": "LX2a-r9-sources", "check": "The four primary sources read by this round are the same bytes as in round 8",
  "location": "/tmp/lx2a_r9_dl (fetched with plain curl by ledgers/LX2/scripts/LX2-a-r8/fetch_sources.sh)",
  "status": "PASS",
  "evidence": "out_sha256_sources_r9.txt: COMPS-1884.pdf, COMPS-1885.pdf, USREPORTS-463-646.pdf, USREPORTS-521-642.pdf hashes equal the round-8 values in ledgers/LX2/scripts/LX2-a-r8/out_sha256_sources_r8.txt (c67e5535..., c7a620b6..., cfc001ed..., 72db2418...). Page mapping: O'Hagan printed page = pdfpage + 641, Dirks printed page = pdfpage + 645 (checked against header lines 1782, 1737, 1689 and Dirks pdfpage 15 = p. 660)."},
 {"id": "LX2a-L02-E3-delta", "check": "E3 wording change (P7 matches P6 in every flag) is true of the twin",
  "location": "course/modules/LX/LX2/L02.html:535-537; tests/labs/LX2/lab-LX2-L02-1.py (label P6, P7)",
  "status": "PASS",
  "evidence": "Twin: P6 and P7 differ only in source_told_of_trade (False vs True); every other flag is equal. Scratch run with P7 source_told False (out in ledgers/LX2/scripts/LX2-a-r9/): P7 fires with gpo1997united p. 652, summary 'fired: P1, P3, P4, P6, P7 (5 of 8)'. The solution text at L02.html:537 matches."},
]
rows_all = rows + new
fails = [r for r in rows_all if r["status"] != "PASS"]
passes = [r for r in rows_all if r["status"] == "PASS"]
# the two FAIL rows need the fix field
frag = {
 "unit": "LX2", "slice": "LX2-a", "round": 9,
 "verifier": "Haiku independent verifier, LX2-a round 9 (did not build LX2; builder ledgers and scratch not read; round-8 fragment read as context only; every L02 row re-verified by reading the page, every card row re-derived, command rows re-run; PASS rows carried only for index.html and L01.html, byte-identical since the previous pin)",
 "pin": PIN, "base": BASE,
 "checkout": "/Users/billyribeiro/.fanout/wt/verifyE9-LX2-a",
 "scratch": "/tmp/lx2a_r9_dl (four primary sources re-fetched by plain curl, sha256 identical to round 8; pagefind.py, quotecheck.py, loccheck.py; /tmp/lx2a_r9_scratch scratch twins)",
 "verified_at": subprocess.run(["date", "-u", "+%Y-%m-%dT%H:%M:%S+00:00"], capture_output=True, text=True).stdout.strip(),
 "verdict": "FAIL",
 "rows": rows_all,
 "mutants": [],
 "registry_flags": prev["registry_flags"],
 "freshness_flags": [],
 "notes": "Round 9 at pin c93dd52 (delta from 0dee921a). Changed in slice a: L02.html (Remark 3.3, Thomas quotation, Definition 4.1 paragraph, E3 wording) and cards.json (L01 cards c010, c016, c024, c023). Both round-8 FAIL rows about the Thomas quotation and Remark 3.3 are now PASS. Two new FAIL rows: LX2a-card-c010 and LX2a-card-c016, where a card now carries a figure (ten days; 1,200 persons) that L01 does not state (rule 10). Non-slice changes: glossary.json, program.json (M3 concept rename), L03/L04 cards and LX1 files, not read beyond the hunk headers. Labs are demonstrations; no mutants are required for this slice (VERIFIER 2.6 applies to project graders only). Observation, not a row: L01.html:585 quiz option 'The model has no exemption states' is awkward (the word 'states' collides with the model's defined term 'state'); meaning is clear, so not graded. Observation: the word 'twin' appears in learner text at L02.html:528 (not on the banned list). The registry flags from round 8 still apply (gpo1983dirks title 1982 with year 1983 at references.json:10823-10835; live verify_refs passes).",
 "summary": f"Slice LX2-a round 9 verdict FAIL at c93dd52. {len(rows_all)} rows: PASS {len(passes)}, FAIL {len(fails)}, UNVERIFIABLE 0. FAIL rows: LX2a-card-c010 (cards.json LX2-c010 back gives ten-day notice and hearing periods that L01.html:84 does not state) and LX2a-card-c016 (cards.json LX2-c016 back gives 1,200 persons for banks, which appears nowhere in the LX2 lessons). Both are rule-10 violations; the statute text supports both figures (comps1884.txt:1770-1776; comps1885.txt:11122-11126). Round-8 FAIL rows LX2a-quote-search, LX2a-L02-opinion-quotes and LX2a-L02-remark-3.3 are PASS now. Mutants: none (slice a is not a project grader).",
}
for r in frag["rows"]:
    if r["status"] != "PASS":
        r["fix"] = r.get("fix", "")
json.dump(frag, open("/Users/billyribeiro/.fanout/wt/verifyE9-LX2-a/ledgers/LX2/LX2-a.json", "w"), indent=1, ensure_ascii=False)
print("rows", len(rows_all), "pass", len(passes), "fail", len(fails), [r["id"] for r in fails])
