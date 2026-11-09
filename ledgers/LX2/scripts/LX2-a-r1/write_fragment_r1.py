"""Build ledgers/LX2/LX2-a.json (round 1, closing delta from base pin 11d7077a) from the base fragment.

Rows re-verified this round carry new evidence; every other base row is carried with the carry prefix.
"""
import json
import sys
from datetime import datetime, UTC

BASE = "/Users/billyribeiro/.fanout/frags/E-LX2-a.round11.json"
OUT = "ledgers/LX2/LX2-a.json"
CARRY = ("Carried from round 11 (cited lines of course/modules/LX/LX2/{files} byte-identical since 11d7077a; "
         "the delta lines L01.html:69, :85, :109, :378, :565 and L02.html:77, :80 are not cited by this row):")
CARRY_IDX = "Carried from round 11 (course/modules/LX/LX2/index.html byte-identical since 11d7077a):"
CARRY_CMD = "Carried from round 11 (inputs byte-identical since 11d7077a; see the round-1 notes):"

base = json.load(open(BASE, encoding="utf-8"))
base_rows = {r["id"]: r for r in base["rows"]}

R1 = {}

def new(rid, check, location, evidence):
    R1[rid] = {"id": rid, "check": check, "location": location, "status": "PASS", "evidence": evidence}

# ---- command rows, re-run this round
new("LX2a-cmd-check_pages", "2.9 structure; tools/check_pages.py --unit LX2", "index, L01, L02",
    "Re-run round 1 at 95f3f8cb: .venv/bin/python tools/check_pages.py --unit LX2 -> 'check_pages LX2: PASS', exit 0 "
    "(ledgers/LX2/scripts/LX2-a-r1/out_check_pages_r1.txt).")
new("LX2a-cmd-check_dag", "2.9 DAG; tools/check_dag.py --unit LX2", "L01, L02, index",
    "Re-run round 1: 'check_dag LX2: PASS', exit 0 (ledgers/LX2/scripts/LX2-a-r1/out_check_dag_r1.txt).")
new("LX2a-cmd-run_labs", "2.5 labs; tools/run_labs.py --unit LX2", "tests/labs/LX2/*.py",
    "Re-run round 1: 'run_labs LX2: PASS (7/7)', exit 0 (ledgers/LX2/scripts/LX2-a-r1/out_run_labs_unit_r1.txt). "
    "The unit run includes the slice-b L03 twin, which changed in the delta; it passes (slice b is verified elsewhere).")
new("LX2a-lab-isolated", "2.5 labs; twin alone under python -I -W error; page code equals twin; expected block equals output",
    "course/modules/LX/LX2/L01.html:137-315 with tests/labs/LX2/lab-LX2-L01-1.py; L02.html:127-439 with tests/labs/LX2/lab-LX2-L02-1.py",
    "Re-run round 1: 'python -I -W error tests/labs/LX2/lab-LX2-L01-1.py' exit 0, stderr 0 bytes, 39 stdout lines, "
    "sha256 prefix 1ccac857139c4977; lab-LX2-L02-1.py exit 0, stderr 0 bytes, 25 stdout lines, prefix 4beca4fe8a6207be "
    "(ledgers/LX2/scripts/LX2-a-r1/out_twin_*.stdout). Both twins are byte-identical to 11d7077a (git diff empty). "
    "Page lab blocks L01.html:137-315 and L02.html:127-439 are outside every delta hunk, so the round-10 page-code and "
    "expected-output comparisons are carried.")
new("LX2a-cmd-page_smoke", "2.9 page_smoke; tools/page_smoke.py --unit LX2 --pages <page> (each run alone)", "index, L01, L02",
    "Re-run round 1, each page alone: 'page_smoke LX2: PASS', exit 0 for index, L01 and L02 "
    "(ledgers/LX2/scripts/LX2-a-r1/out_page_smoke_{index,L01,L02}_r1.txt).")
new("LX2a-cmd-ruff-mypy", "2.5 lint and types on the slice-a twins", "tests/labs/LX2/lab-LX2-L01-1.py, tests/labs/LX2/lab-LX2-L02-1.py",
    "Re-run round 1: ruff check and ruff format --check -> 'All checks passed!', '2 files already formatted' "
    "(out_ruff_r1.txt); mypy --no-incremental -> 'Success: no issues found in 2 source files' (out_mypy_r1.txt).")
new("LX2a-cmd-pytest", "tooling tests relevant to labs and page checks", "tests/",
    "Re-run round 1: .venv/bin/python -m pytest -q tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py "
    "tests/test_page_smoke.py tests/test_curriculum.py tests/test_refs.py tests/test_build_site.py -> exit 0 "
    "(ledgers/LX2/scripts/LX2-a-r1/out_pytest_r1.txt).")
new("LX2a-cmd-verify_refs", "2.1 citations; tools/verify_refs.py --offline (live LX2 part carried)",
    "references/references.json (LX2 keys gpondsecurities, gpondsecuritiesb, gpo1983dirks, gpo1997united, cfandcode, frb2026fed)",
    "Re-run round 1: tools/verify_refs.py --offline -> 'offline integrity: 560 entries, 0 problems', exit 0 "
    "(out_verify_refs_offline_r1.txt). references.json changed in the delta only at generated_at and at used_by of a DV1/FC2 "
    "entry (git diff 11d7077a..HEAD); no LX2 key changed, so the live LX2 re-verification of round 11 is carried: "
    "'Carried from round 11 (references/references.json LX2 entries byte-identical since 11d7077a)'.")

# ---- quote and attribution rows, re-verified against fresh primary text
new("LX2a-quote-search", "2.1 attribution: every curly-quoted passage searched in its primary text",
    "course/modules/LX/LX2/L02.html:575, :109 (carried); L01.html:69, :85, :109, :378, :565; L02.html:77, :80",
    "Re-fetched by plain curl (ledgers/LX2/scripts/LX2-a-r8/fetch_sources.sh into a new empty dir; sha256 of comps1884.txt "
    "eaf8af1a..., comps1885.txt ee89b02d..., dirks.txt d295f808..., ohagan.txt 90d1f156... equal the round-8 record). "
    "quote_check_r1.py (out_quote_check_r1.txt): Dirks p. 655 'Unlike insiders ... no such relationships.' True; Dirks p. 660 "
    "'Thus, a tippee assumes ... knows or should know that there has been a breach.' True; Dirks fn 23 'a mental state embracing "
    "intent to deceive, manipulate, or defraud' True; O'Hagan p. 652 'not only to officers ... temporarily become fiduciaries of a "
    "corporation.' True; 1933 Act 8(d) 'at a time fixed by the Commission ... within fifteen days after such notice ... issue a "
    "stop order' True and 'shall cease to be effective' True; 1934 Act 15(d)(1) second sentence True and third sentence "
    "'less than 300 persons ... 1,200 persons' True. The 8(d) phrase 'suspending the effectiveness of the registration statement' "
    "spans a printed page break in comps1884.txt (line 1796 to 1797); the quote is present. L02.html:575 is unchanged since base; "
    "its Dirks check is carried from round 11.")
new("LX2a-L01-amended", "2.1 attribution and 2.9 prose: amendment dates and the list of section numbers used in the lesson",
    "L01.html:65, :69 (and every section number in L01.html re-derived)",
    "Re-derived by grep of L01.html: section numbers 2, 2(a)(5), 2(a)(19), 3, 4, 5(a)-(d), 6(a)-(e)(1), 8(a),(b),(d),(e), 12(a),(b),(d), "
    "13(a), 15(d)(1); the delta adds 'section 2 (definitions)' as a locator at :69 and changes no section number, so the enumeration at "
    ":65 is still complete (section 2 is covered by 2(a)(5) and 2(a)(19); section 8 by 8(a),(b),(d),(e); section 15(d) by the 15(d)(1) "
    "sentences). Amendment dates unchanged: comps1884.txt 'As Amended Through P.L. 119-27, Enacted July 18, 2025'; comps1885.txt "
    "'As Amended Through P.L. 119-60, Enacted December 18, 2025' (primary_checks_r1.sh output).")
new("LX2a-L01-quotes-1933", "2.1 attribution: 1933 Act quotations and paraphrases",
    "L01.html:69-70, :80-85, :88",
    "Re-read: :69 span 'section 2 (definitions)' (new wording 'The definitions in section 2 do not define the phrase.'): primary "
    "'SEC. 2.' (comps1884.txt:34) has no 'in effect' phrase (grep of lines 34-391, out_primary_checks_r1.txt): True. :85 (8(d)) "
    "paraphrase 'after notice by personal service or the sending of confirmed telegraphic notice and after opportunity for hearing "
    "(at a time fixed by the Commission) within fifteen days after such notice by personal service or the sending of such telegraphic "
    "notice, issue a stop order ...' matches comps1884.txt:1794-1796 (quote_check sec8d_fifteen True). :70, :80-84 and :88 unchanged and "
    "checked in round 11 against comps1884.txt.")
new("LX2a-L01-quotes-1934", "2.1 attribution: 1934 Act quotations (15(d)(1))", "L01.html:100-111",
    "Re-checked at :109 (changed): 'shall be automatically suspended if and so long as any issue of securities of such issuer is "
    "registered pursuant to section 12' (quote_check sec15d_second True); 'shall also be automatically suspended as to any fiscal year' "
    "and 'held of record by less than 300 persons', 'or, in the case of a bank, a savings and loan holding company or a bank holding "
    "company, 1,200 persons' (sec15d_third_300_1200 True, comps1885.txt:11114 ff.). The lesson's 'fewer than 300' and '1,200 persons' "
    "match. Other lines in :100-111 unchanged.")
new("LX2a-L01-markup", "2.9 structure and prose: claim spans and markup", "L01.html:51-109, :359-386, :499-513, :604",
    "Changed claim spans at :69 (data-grade C, data-cite gpondsecurities, data-locator 'section 2 (definitions)'), :85 (gpondsecurities, "
    "'section 8(d)'), :109 (gpondsecuritiesb, 'section 15(d)(1), third sentence'), :378 (gpondsecurities, 'section 8(d)') and "
    ":565 (gpondsecuritiesb): each grade and key is valid (check_pages PASS, out_check_pages_r1.txt). Span nesting is well formed "
    "(page_smoke PASS, out_page_smoke_L01_r1.txt).")
new("LX2a-L01-in-effect-attribution", "2.1 attribution: the 'in effect' reading against section 2",
    "L01.html:69", "The delta moves 'The definitions in section 2 do not define the phrase.' into its own C span. "
    "grep -i 'in effect' over comps1884.txt lines 34-391 (SEC. 2) returns no match (out_primary_checks_r1.txt); the only "
    "'effect' words are 'effective', 'take effect' and 'no force or effect'. The statement is true of the primary text.")
new("LX2a-L01-misconceptions", "2.9 misconceptions: the wrong statement and its explanation", "L01.html:369-389 (changed :378)",
    "Re-read :378: the 8(d) explanation quotes 'issue a stop order suspending the effectiveness of the registration statement' "
    "and paraphrases the timing clause 'within fifteen days after such notice' which matches comps1884.txt:1794-1796 "
    "(sec8d_fifteen True); 'the stop order ... shall cease to be effective' (comps1884.txt:1810). Other misconceptions "
    "(:369-377, :379-389) unchanged and checked in round 11.")
new("LX2a-L01-quiz", "2.9 quiz: keys and explanations", "L01.html:517-600 (changed :565)",
    "Q6 (:558-562): options are 'the security is listed on a foreign exchange' (not a ground), 'the securities of each class ... held of "
    "record by fewer than 300 persons at the start of the year' (a ground stated in the third sentence, comps1885.txt:11114 ff.) and "
    "'a refusal order' (not a ground). The question asks which of the following grounds applies, so one true ground marked correct is "
    "a correct key. The explanation at :565 now names 300 persons and 1,200 persons for banks, bank holding and savings-and-loan holding "
    "companies, 'at the beginning of that year', matching the statute. Other quiz items unchanged.")
new("LX2a-L01-paraphrase-locators", "2.1 attribution: locators name the sentence paraphrased",
    "L01.html:65-70, :80-85, :96-111, :362-363, :483",
    "Changed locators re-checked: :69 'section 2 (definitions)' (negative statement about section 2, verified above); :85 'section 8(d)' "
    "(verified above); :109 'section 15(d)(1), third sentence' (verified above). Others unchanged and checked in round 11.")
new("LX2a-L01-unspanned-readings", "2.1 attribution: every reading the lesson attributes is spanned", "L01.html:51, :53, :69, :92, :96",
    "The sentence at :69 is now a C claim span with locator 'section 2 (definitions)' (L01.html:69). Other cited sentences unchanged.")
new("LX2a-L01-section-locators", "2.9 section locators name the statute text they paraphrase",
    "L01.html:51-111, :359-365, :483",
    "Changed spans at :69, :85, :109 checked against comps1884.txt / comps1885.txt (verified above). Other spans unchanged.")
new("LX2a-L01-section-locators-extra", "2.9 section locators name the statute text they paraphrase (extra)",
    "L01.html:51-111, :359-365, :483", "As LX2a-L01-section-locators: changed spans at :69, :85, :109 verified against primary text.")
new("LX2a-L01-structure", "2.9 structure: lesson elements and order", "course/modules/LX/LX2/L01.html:32-616",
    "Delta changes are inline text and spans inside existing elements (:69, :85, :109, :378, :565); no element is added, removed or "
    "reordered (git diff hunks). check_pages PASS and page_smoke PASS (round-1 runs).")
new("LX2a-L01-dag", "2.9 DAG: concepts used in L01 and their prerequisites", "L01.html:37-38, :63; L01.html (whole page)",
    "check_dag LX2 PASS (out_check_dag_r1.txt). The changed L01 lines contain no concept link or new dfn "
    "(grep of data-concept, class=\"concept\" and <dfn> on :69, :85, :109, :378, :565: the only dfn on :69 is the existing "
    "'in effect' definition).")
new("LX2a-IDX-lede-markup", "2.9 structure and prose: lede and markup", "index.html:33; L01.html:51, :59-65; L02.html:51-110",
    "Changed L02 claim spans at :77 (gpo1983dirks, p. 655) and :80 (gpo1983dirks, pp. 659-660) have valid grade and key and a "
    "locator that matches the primary pages (verified below). index.html:33 byte-identical; L01.html:51-65 unchanged. check_pages PASS.")
new("LX2a-IDX-objectives-1-3", "2.9 hub objectives match the lessons",
    "index.html:51-53; L01.html:55-130; L02.html:55-111, :113-425",
    "The changed lines (L01 :69, :85, :109; L02 :77, :80) are body prose and claim spans, not objective statements. Objectives unchanged "
    "in index.html:51-53 (byte-identical). The lessons' objectives still match.")
new("LX2a-L02-tippee-definition", "2.1 attribution and 2.9 prose: the tippee definition and its quotation",
    "L02.html:76-77 (changed :77), :80",
    "L02.html:77: 'the person who receives the information from an insider (the insider who gives it is the tipper)' is a definition "
    "parenthetical; the p. 655 quotation 'Unlike insiders who have independent fiduciary duties to both the corporation and its "
    "shareholders, the typical tippee has no such relationships.' is present in dirks.txt on printed p. 655 (PDF page 10, header "
    "'DIRKS v. SEC 655'), quote_check dirks_655_tippee True. Dirks uses 'tipper' for the insider who gives the information (Dirks "
    "text, Syllabus and Opinion of the Court, pp. 646-665).")
new("LX2a-L02-dag", "2.9 DAG: L02 concepts and prerequisites", "L02.html:37, :56, :66, :80, :103",
    "check_dag LX2 PASS (out_check_dag_r1.txt). The changed :80 text adds no concept link; the dfn id def-tipper-tippee-liability is unchanged.")
new("LX2a-L02-structure", "2.9 structure: lesson elements and order", "course/modules/LX/LX2/L02.html:32-674",
    "Delta changes are text inside existing paragraphs and spans at :77 and :80; no element changed. check_pages and page_smoke PASS (round-1 runs).")
new("LX2a-L02-opinion-quotes", "2.1 attribution: opinion quotations in L02", "L02.html:58-110, :424-431, :441-445, :482, :541-548, :617",
    "Changed quotations re-verified: :77 (p. 655, dirks_655_tippee True) and :80 (p. 660, dirks_660_test True, PDF page 15 header "
    "'660 OCTOBER TERM, 1982'). Other quotations unchanged since round 11.")
new("LX2a-L02-page-locators", "2.1 attribution: claim-span locators on L02 (whole page)", "course/modules/LX/LX2/L02.html (all claim-span locators)",
    "Changed spans: :77 locator 'p. 655' (PDF page 10); :80 locator 'pp. 659-660' with the statement 'the tippee's duty comes from the "
    "insider's breach ... (p. 660)' (the derivative theme runs from PDF page 14 (printed 659) to PDF page 15 (printed 660)). Other "
    "locators unchanged.")
new("LX2a-L02-B3-B1", "2.9 next-lesson navigation and forward references (whole page)", "course/modules/LX/LX2/L02.html; index.html:171",
    "grep -i 'dodd|mifid' over L02.html: one hit at :668 (the next-lesson link text 'Manipulation, Dodd–Frank and MiFID II'), as in "
    "round 11 (out_banned_years_symbols_r1.txt). No new forward reference from the delta. The round-11 navigation observation stands.")
new("LX2a-L02-years", "2.1 years and dates in L02 prose (whole page)", "course/modules/LX/LX2/L02.html (prose)",
    "Year tokens in L02.html: 1934 at :37 and :56 only (out_banned_years_symbols_r1.txt). The changed lines :77 and :80 contain no "
    "year. Unchanged.")
new("LX2a-notation", "2.9 notation: symbols against notation.json (L01, L02, index)",
    "course/modules/LX/LX2/L01.html:115-352 (math and labels); L02.html (whole page); index.html",
    "The changed lines (L01 :69, :85, :109, :378, :565; L02 :77, :80) contain no math markup or symbol (scan for $, \\, ^, _, {, }, "
    "&entities, sub/sup: none; out_banned_years_symbols_r1.txt). No new symbol is introduced by the delta.")
new("LX2a-r9-quotes-L02", "2.1 attribution: L02 claim spans with a quoted passage and a gpo key (whole page)",
    "course/modules/LX/LX2/L02.html (all claim spans with a quoted passage and a gpo key)",
    "The changed spans with quoted passages are :77 (p. 655 quote, verified) and the p. 660 test quotation in the next paragraph "
    "(dirks_660_test True). The span at :80 now carries a paraphrase, not a quotation; its locator pp. 659-660 is verified above. "
    "Other spans unchanged.")
new("LX2a-r8-delta", "2.9 round-8 delta rows (L02 :66-125 etc.)",
    "course/modules/LX/LX2/index.html:59-62, :168-171; course/modules/LX/LX2/L02.html:66-125 (changed :77, :80)",
    "The round-8 delta items in L02 :66-125 are re-checked where the delta touches them: :77 and :80 verified above. index.html:59-62 and "
    ":168-171 are byte-identical since 11d7077a.")
new("LX2a-r11-delta", "2.9 round-11 delta rows (cards and hub text)",
    "delta 00a84795..11d7077: index.html:148, :161; L01.html:65, :585; L02.html:575; cards.json (round-11 cards)",
    "index.html:148, :161, L01.html:65, :585 and L02.html:575 are byte-identical since 11d7077a (not in the delta). Card c004 changed "
    "again in the closing delta and is re-verified (LX2a-r1-card-c004). Other round-11 cards: byte-identical since 11d7077a.")
new("LX2a-card-c016", "2.9 card mirrors a lesson claim: LX2-c016 back against L01.html:111",
    "course/modules/LX/LX2/cards.json LX2-c016 (back); L01.html:111 (section 3, third sentence of section 15(d)(1))",
    "Card back: 'If, at the beginning of that year, ... less than 300 persons, or, in the case of a bank, a savings and loan holding "
    "company or a bank holding company, 1,200 persons.' The lesson at :109 and :111 and the statute (comps1885.txt:11114 ff.) say the "
    "same. The card is consistent with the changed :109 text.")
new("LX2a-cards-L01-other", "2.9 cards: L01 cards other than c010 and c016 against the current lesson text",
    "course/modules/LX/LX2/cards.json (L01 cards, 33 in total)",
    "Changed or dependent L01 cards re-verified: LX2-c003, c004, c025, c027 (changed backs, see LX2a-r1-card-*), LX2-c104 (new), "
    "and LX2-c024, c026, c096 (depend on section 5, 6(a), 15(d)(1) third sentence): consistent with the lesson and the statute "
    "(c096 'The third sentence excludes that fiscal year from the suspension' matches L01.html:109 and comps1885.txt). The other L01 "
    "cards are byte-identical since 11d7077a and do not depend on the changed sentences.")
new("LX2a-cards-L02", "2.9 cards: L02 cards against the current lesson text",
    "course/modules/LX/LX2/cards.json (L02 cards, 21 in total)",
    "Changed or dependent L02 cards re-verified: LX2-c029, c030, c097, c099 (changed), LX2-c105, c106 (new), and LX2-c033, c034, "
    "c037, c040, c041 (depend on Dirks pp. 660-664 and fn 23): consistent with the current lesson text and the primary pages. "
    "Other L02 cards are byte-identical since 11d7077a.")
new("LX2a-cards-dup", "2.9 cards: no duplicate cards (ids, fronts, backs)", "course/modules/LX/LX2/cards.json (100 cards)",
    "Recounted this round (out_cards_dup_r1.txt): 100 cards; no duplicate id; no duplicate normalised front; no duplicate normalised "
    "back. New ids LX2-c104, c105, c106 are unique. Every cite key is a registry key of the unit.")

# new per-card rows
new("LX2a-r1-card-c003", "2.9 card LX2-c003 back against L01.html:69", "cards.json LX2-c003; L01.html:69",
    "Back changed from '... (Section 2).' to '... under the 1933 Act.' The lesson's registration-statement definition (L01.html:69) "
    "describes the document an issuer files with the Commission to register a security under the 1933 Act. Consistent.")
new("LX2a-r1-card-c004", "2.9 card LX2-c004 back against L01.html:69", "cards.json LX2-c004; L01.html:69",
    "Back now reads 'the lesson reads the phrase as the statement having taken effect under section 8(a) and not having been suspended "
    "under section 8(d). Section 2 does not define the phrase.' This matches L01.html:69 and the primary text (SEC. 2 has no 'in effect'). "
    "Consistent.")
new("LX2a-r1-card-c025", "2.9 card LX2-c025 back against L01.html:378 and :85", "cards.json LX2-c025; L01.html:378, :85",
    "Back adds 'at a time fixed by the Commission within fifteen days after such notice by personal service or the sending of such "
    "telegraphic notice' which matches comps1884.txt:1794-1796 (sec8d_fifteen True) and L01.html:85 and :378. Stop-order statements "
    "match comps1884.txt:1796-1810.")
new("LX2a-r1-card-c027", "2.9 card LX2-c027 back against L01.html:109", "cards.json LX2-c027; L01.html:109",
    "Back now omits 'which is suspended if and so long as a section 12 registration applies' and states that the 1933 duty comes from "
    "section 15(d)(1). The lesson at :109 says the same, and the suspension is stated in the card LX2-c104 and in L01.html:106. Consistent.")
new("LX2a-r1-card-c029", "2.9 card LX2-c029 (front changed) against O'Hagan p. 652", "cards.json LX2-c029; L01/L02 lesson L02.html:69",
    "Front now asks 'temporarily become fiduciaries'; the back quotes O'Hagan p. 652 'not only to officers ... who temporarily become "
    "fiduciaries of a corporation' (ohagan.txt, PDF page 11 header '652', quote check ohagan_652_temporary True). Consistent with L02.html:69.")
new("LX2a-r1-card-c030", "2.9 card LX2-c030 (back changed) against L02.html:80 and Dirks p. 660", "cards.json LX2-c030; L02.html:80",
    "Back: 'the tippee assumes a fiduciary duty ... only when the insider has breached ... and the tippee knows or should know that there "
    "has been a breach (Dirks, p. 660)' matches dirks_660_test True (PDF page 15, printed 660). Consistent with L02.html:80.")
new("LX2a-r1-card-c097", "2.9 card LX2-c097 (front and basis) against L02.html:84-86 and :496", "cards.json LX2-c097; L02.html:84-86, :496",
    "The front and basis now name Assumption A1 of Lesson 2 Section 3; the back says the opinion does not state the reading, which "
    "matches L02.html:85 'It does not state this reading of a pattern's flag'. Consistent.")
new("LX2a-r1-card-c099", "2.9 card LX2-c099 (back changed) against L02.html:123 and the lab twin", "cards.json LX2-c099; L02.html:123; tests/labs/LX2/lab-LX2-L02-1.py:1-30",
    "Back: 'the lab reads the role issuer_insider to include a temporary fiduciary ... the classifier does not test that statement.' "
    "A3 (L02.html:123) and the twin docstring (classical branch, role issuer_insider; does not test the security or the person) match.")
new("LX2a-r1-card-c104", "2.9 new card LX2-c104 against L01.html:109 and comps1885.txt", "cards.json LX2-c104; L01.html:106, :109",
    "Back 'Automatically, if and so long as any issue of the issuer's securities is registered pursuant to section 12.' matches the "
    "second sentence of 15(d)(1) (sec15d_second True). Cite gpondsecuritiesb is a registry key (COMPS-1885, Securities Exchange Act of 1934).")
new("LX2a-r1-card-c105", "2.9 new card LX2-c105 against L02.html:61 and Dirks fn 23", "cards.json LX2-c105; L02.html:61, :445, :579",
    "Back: 'a mental state embracing intent to deceive, manipulate, or defraud' is the text of Dirks footnote 23 (PDF page 18, printed "
    "p. 663, dirks_fn23_scienter True). The locator 'p. 663 n. 23' appears in L02.html:61 (card number appears in its lesson).")
new("LX2a-r1-card-c106", "2.9 new card LX2-c106 against L02.html:77", "cards.json LX2-c106; L02.html:77",
    "Back 'The person who receives the information from an insider. The insider who gives it is the tipper.' matches L02.html:77.")
new("LX2a-r1-delta-hunks", "2.9 closing delta: every hunk of 11d7077a..HEAD in slice a was read",
    "L01.html:69, :85, :109, :378, :565; L02.html:77, :80; cards.json (slice-a cards c003, c004, c025, c027, c029, c030, c097, c099, c104-c106)",
    "git diff -U0 11d7077a..HEAD: L01 hunks at 69, 85, 109, 378, 565 (all read); L02 hunks at 77, 80 (read); cards.json hunks for "
    "L01 (c003, c004, c025, c027, c104 new) and L02 (c029, c030, c097, c099, c105, c106 new) read. The L03 page (L03.html), the L03 "
    "cards, the L04 cards and the L03 twin are slice b and are not verified here. curriculum/*.yaml, curriculum.json and "
    "references.json changed outside LX2 only (checked by git diff --stat).")

# ---- assemble
re_ids = set(R1)
rows = []
for r in base["rows"]:
    rid = r["id"]
    if rid in R1:
        rows.append(R1[rid])
        continue
    ev = r["evidence"]
    loc = r["location"]
    if "index.html" in loc and "L01" not in loc and "L02" not in loc and "cards" not in loc:
        pref = CARRY_IDX
    elif loc.startswith("tests/") or "references/references.json" in loc or "tools/" in loc:
        pref = CARRY_CMD
    else:
        files = "L01.html and L02.html" if ("L01" in loc or "L02" in loc) else "cards.json"
        if "cards.json" in loc and ("L01" in loc or "L02" in loc):
            files = "L01.html and L02.html and cards.json"
        pref = CARRY.format(files=files)
    rows.append({"id": rid, "check": r["check"], "location": loc, "status": "PASS", "evidence": f"{pref} {ev}"})
for rid in R1:
    if rid not in base_rows:
        rows.append(R1[rid])

notes = (
    "Closing delta (ruling 30) from base pin 11d7077a to 95f3f8cb. Delta in slice a: L01.html lines 69, 85, 109, 378, 565; "
    "L02.html lines 77, 80; cards.json slice-a cards c003, c004, c025, c027, c029, c030, c097, c099 (changed) and c104, c105, c106 "
    "(new). Every base row whose cited subject changed was re-verified from scratch (listed rows with new evidence); every other base "
    "row is carried under the carry prefix with its base evidence. No base row was non-PASS. No new mutants were written (ruling 37); "
    "labs are demonstrations, so there are no mutants for this slice (base mutants: none). Observations, not rows: (1) nine L01/L02 cards (c001, c002, c003, c005, c008, c022, c097, c098, c099) carry no grade field; "
    "the schema (tools/check_pages.py check_cards) allows a missing grade when cite or basis is present, so this is not a finding. (2) L01 quiz Q6's correct option is one true ground of three named, not the only ground; the question asks "
    "which grounds apply, so it is not a finding. (3) The round-11 note that L02.html:668 is navigation stands. (4) L03.html, the L03 "
    "twin and the L03/L04 cards changed in this delta and belong to slice b."
)
registry_flags = list(base.get("registry_flags", []))
fragment = {
    "unit": "LX2",
    "slice": "LX2-a",
    "round": 1,
    "verifier": "Haiku independent verifier, LX2-a round 1 (closing delta, ruling 30). Did not build LX2; the base fragment is the "
                "round-11 ledger, read for scope and carried where the cited subject is byte-identical.",
    "pin": "95f3f8cb21c2cd9fc904430bd30a6b734d01f672",
    "base": "11d7077a290f7960b183d3a5a6631af4773888f9",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyF31-LX2-a",
    "scratch": open("/tmp/lx2a_r1_dir.txt").read().strip() + " (plain-curl fetch of the four primary sources; sha256 matches the round-8 record)",
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "verdict": "PASS",
    "rows": rows,
    "mutants": [],
    "registry_flags": registry_flags,
    "freshness_flags": [],
    "notes": notes,
    "summary": f"Slice LX2-a closing delta round 1 at 95f3f8cb: {len(rows)} rows, all PASS. Re-verified from scratch: "
               f"{len(R1)} rows (commands re-run, changed hunks, changed cards). Carried from round 11: the rest.",
}
json.dump(fragment, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("rows", len(rows), "new-evidence", len(R1), "base", len(base_rows))
