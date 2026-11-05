"""Write the LX2-a round 8 fragment (ledgers/LX2/LX2-a.json). Evidence strings cite the scripts and outputs of LX2-a-r8.

Usage: python -I ledgers/LX2/scripts/LX2-a-r8/write_fragment_r8.py <checkout_dir>
"""

import json
import sys
from datetime import UTC, datetime

CHK = sys.argv[1]
S = "ledgers/LX2/scripts/LX2-a-r8"
R7_CARRY = "Carried from round 7 (course/modules/LX/LX2/L01.html and tests/labs/LX2/lab-LX2-L01-1.py byte-identical since the previous pin, verified by git diff --quiet 06994db1 0dee921a): "

CMD = {
    "check_pages": ("tools/check_pages.py --unit LX2", "index, L01, L02",
                    f"Run this round: 'check_pages LX2: PASS', exit 0 ({S}/out_commands_r8.txt)."),
    "check_dag": ("tools/check_dag.py --unit LX2", "L01, L02, index",
                  f"Run this round: 'check_dag LX2: PASS', exit 0 ({S}/out_commands_r8.txt)."),
    "run_labs": ("tools/run_labs.py --unit LX2", "tests/labs/LX2/*.py",
                 f"Run this round: 'run_labs LX2: PASS (7/7)', exit 0 ({S}/out_commands_r8.txt)."),
    "page_smoke": ("tools/page_smoke.py --unit LX2 --pages <page>", "index, L01, L02",
                   f"Run alone this round: 'page_smoke LX2: PASS' for index, L01 and L02, exit 0 each ({S}/out_commands_r8.txt). Timings not measured on a quiet machine."),
}
rows = [
    {"id": "LX2a-cmd-check_pages", "check": CMD["check_pages"][0], "location": CMD["check_pages"][1], "status": "PASS",
     "evidence": CMD["check_pages"][2]},
    {"id": "LX2a-cmd-check_dag", "check": CMD["check_dag"][0], "location": CMD["check_dag"][1], "status": "PASS",
     "evidence": CMD["check_dag"][2] + " Each LX2 dfn id defined once: grep of data-concept in course/ (r7 method, rerun not needed because shared inputs are unchanged in the delta)."},
    {"id": "LX2a-cmd-run_labs", "check": CMD["run_labs"][0], "location": CMD["run_labs"][1], "status": "PASS",
     "evidence": CMD["run_labs"][2]},
    {"id": "LX2a-lab-isolated", "check": "twin alone under python -I -W error; page code equals twin; expected block equals output",
     "location": "course/modules/LX/LX2/L01.html:137-315 with tests/labs/LX2/lab-LX2-L01-1.py; L02.html:127-425 with tests/labs/LX2/lab-LX2-L02-1.py",
     "status": "PASS",
     "evidence": f"{S}/lab_twin_check.py run this round: 'lab-LX2-L01-1: page_code_equals_twin=True exit=0 stderr_bytes=0 expected_equals_output=True' and 'lab-LX2-L02-1: page_code_equals_twin=True exit=0 stderr_bytes=0 expected_equals_output=True' ({S}/out_lab_twin_r8.txt). Direct runs with python -I -W error: exit 0 both."},
    {"id": "LX2a-cmd-page_smoke", "check": CMD["page_smoke"][0], "location": CMD["page_smoke"][1], "status": "PASS",
     "evidence": CMD["page_smoke"][2]},
    {"id": "LX2a-cmd-ruff-mypy", "check": "ruff check, ruff format --check, mypy --no-incremental on the slice-a twins",
     "location": "tests/labs/LX2/lab-LX2-L01-1.py, tests/labs/LX2/lab-LX2-L02-1.py", "status": "PASS",
     "evidence": f"Run this round: 'All checks passed!' ; '2 files already formatted' ; 'Success: no issues found in 2 source files' ({S}/out_commands2_r8.txt)."},
    {"id": "LX2a-cmd-pytest", "check": "pytest: tests/test_labs.py, tests/test_run_labs.py, tests/test_page_checks.py",
     "location": "tests/", "status": "PASS",
     "evidence": f"Run this round: exit 0, all dots, 100% ({S}/out_pytest_relevant_r8.txt). The full tests/ directory was not run."},
    {"id": "LX2a-cmd-verify_refs", "check": "tools/verify_refs.py --unit LX2 (live) and --offline",
     "location": "references/references.json (LX2 keys gpondsecurities, gpondsecuritiesb, gpo1983dirks, gpo1997united, cfandcode, frb2026fed)",
     "status": "PASS",
     "evidence": f"Run this round: 'offline integrity: 560 entries, 0 problems' and 'live re-verification of LX2: 6 of 560 entries, 0 problems', exit 0 ({S}/out_commands2_r8.txt). references/references.json is unchanged in the delta."},
    {"id": "LX2a-cmd-coursekit-closure", "check": "tools/coursekit.py prerequisite_closure('LX2')",
     "location": "course/modules/LX/LX2/index.html:35, :62", "status": "PASS",
     "evidence": f"Run this round: {{'M1', 'M2', 'FC1', 'P0.1', 'E1'}} = {{E1, FC1, M1, M2, P0.1}} ({S}/out_commands2_r8.txt), matching index.html:62."},
    {"id": "LX2a-quote-search", "check": "every curly-quoted passage on L01 and L02 searched in the primary text, with the printed page",
     "location": "course/modules/LX/LX2/L02.html:109 (Thomas dissent); L01.html and L02.html (all others)", "status": "FAIL",
     "evidence": f"{S}/quote_locate.py on the four sources re-fetched by {S}/fetch_sources.sh (PDF and txt hashes identical to round 7, {S}/out_sha256_sources_r8.txt): 140 quotations, output {S}/out_quote_locate_L01_L02.txt. Every claim-span quote is FOUND at the locator's page except the Thomas dissent quote 'the misappropriation theory fails to provide a coherent and consistent interpretation' (L02.html:109, locator p. 680), which is NOT FOUND. {S}/r8_checks.py section 1: the printed text reads 'Because the Commission’s misappropriation theory fails to provide a coherent and consistent interpretation' (ohagan.txt, p. 680). The quoted fragment begins with 'the misappropriation' and drops 'Commission’s' with no ellipsis, so it is not verbatim. The NOT FOUND results for the statute (section 8(d), 'suspending the effectiveness of the registration statement') are a page-footer artifact: the phrase is split by the statute's running footer (comps1884.txt:1796-1807), and was read in full by hand. The bracketed alteration '[his]' for O'Hagan's in footnote 5 (p. 653 n. 5) is an accepted alteration.",
     "fix": "L02.html:109: change the quoted fragment to the verbatim source wording: “the Commission’s misappropriation theory fails to provide a coherent and consistent interpretation” (O'Hagan p. 680, Thomas, J.), keeping the locator p. 680."},
    {"id": "LX2a-IDX-hours", "check": "hub hours split and lesson hours (36 + 14 = 50; 28%)", "location": "course/modules/LX/LX2/index.html:29, :44, :176-186; L01.html:2, :34; L02.html:2, :34", "status": "PASS",
     "evidence": f"Read in full this round (index.html:1-207). data-hours-lessons=36 and data-hours-project=14 (index.html:29); 14/50 = 28% (index.html:44, :176); 4 x 9 = 36 (index.html:176); lesson cards 9 h each (index.html:150-153); bar widths 72%/28% (index.html:42). check_pages PASS ({S}/out_commands_r8.txt)."},
    {"id": "LX2a-IDX-structure", "check": "hub template sections in order", "location": "course/modules/LX/LX2/index.html:1-207", "status": "PASS",
     "evidence": f"Read in full this round. Sections: objectives (47), prerequisites (60), placement (73), lessons (146), ladder (157), data (168), hours (174), reading (191). check_pages PASS ({S}/out_commands_r8.txt)."},
    {"id": "LX2a-IDX-closure", "check": "prerequisite closure statement and computed closure", "location": "course/modules/LX/LX2/index.html:35, :62", "status": "PASS",
     "evidence": f"index.html:62 reads {{E1, FC1, M1, M2, P0.1}}; coursekit prints the same set ({S}/out_commands2_r8.txt). The changed sentence at :62 links prerequisite-module concepts to concepts.html anchors (:64-68), all present in course/concepts.html (grep id= each anchor: count 1 each)."},
    {"id": "LX2a-IDX-FC1-title", "check": "FC1 title in the prerequisite link", "location": "course/modules/LX/LX2/index.html:35", "status": "PASS",
     "evidence": "index.html:35 'FC1 The Financial System, Markets & Instruments'; index.html:63 'the FC1 module' link to ../../FC/FC1/index.html. Read this round."},
    {"id": "LX2a-IDX-SR4", "check": "SR4 unlock claim", "location": "course/modules/LX/LX2/index.html:39", "status": "PASS",
     "evidence": "index.html:39 'SR4 Regulation's Market Footprint, which lists LX2 among its prerequisites'. curriculum/05-macro-alternatives.yaml:505-509 gives id SR4, title 'Regulation's Market Footprint', prereqs [SR1, FI4, LX2]. Read this round."},
    {"id": "LX2a-IDX-lede-markup", "check": "lede and markup of the hub", "location": "course/modules/LX/LX2/index.html:33; L01.html:51, :59-65; L02.html:51-110", "status": "PASS",
     "evidence": "Read this round. The hub lede (index.html:33) states grade C and the 'not legal advice' scope; its claim spans (L01:51-65, L02:51-110) carry data-cite and data-locator (all 128 claim spans in L01 (62) and L02 (66) carry a data-locator; grep count 0 without)."},
    {"id": "LX2a-IDX-objectives-1-3", "check": "objectives 1-3 match the lessons", "location": "course/modules/LX/LX2/index.html:51-53; L01.html:55-130; L02.html:55-111, :113-425", "status": "PASS",
     "evidence": "index.html:51 (filing, effectiveness, stop-order and reporting sentences) is covered by L01.html:69-106 (sections 8(a), 8(d), 12, 13, 15(d)); :52 (statuses, offer and sale conditions) by L01.html:113-135; :53 (classify, element) by L02.html:127-425. Read this round."},
    {"id": "LX2a-IDX-placement-arith", "check": "placement diagnostic arithmetic", "location": "course/modules/LX/LX2/index.html:95-141", "status": "PASS",
     "evidence": "Recomputed: 100/1.1 = 90.909 (answer 90.91, tol 0.01, index.html:96-98); d/dx x^2 at 3 = 6 (index.html:110-112); d/dx of x^2 y at (2,3) = 2xy = 12 (index.html:115-117); spread 100.10-99.50 = 0.60 (:129-131); 6/8 = 0.75 (:134-136); bias = (-1 -1 +1)/3 = -1/3 = -0.3333 (:139-141, forecast minus realised, matching L04 e_t = yhat - y, L04.html); 7/10 = 70% (:75). Read this round."},
    {"id": "LX2a-IDX-placement-items-1-8", "check": "placement items 1-8 and their keys", "location": "course/modules/LX/LX2/index.html:77-131", "status": "PASS",
     "evidence": "Read this round: items 1-8 (index.html:77-131) each have one data-correct option or an answer that matches the explanation; item 1 evidence grade T, item 2 comparative statics, item 4 negation, item 5 derivative, item 7 OTC. Explanations match their concepts (concepts.html anchors present)."},
    {"id": "LX2a-IDX-placement-cross-ref", "check": "placement cross-reference to L04 and the ladder", "location": "course/modules/LX/LX2/index.html:136; course/modules/LX/LX2/L04.html:114", "status": "PASS",
     "evidence": "index.html:136 'Lesson 4 defines the hit rate for the project's model case'; L04.html defines <dfn>hit rate</dfn> and <dfn>bias</dfn> (grep, this round); e_t = yhat - y (L04.html). Read this round."},
    {"id": "LX2a-IDX-skill-items", "check": "skill checks rungs 1 and 2", "location": "course/modules/LX/LX2/index.html:133, :138", "status": "PASS",
     "evidence": "index.html:133 (rung 1, hit rate 6/8 = 0.75) and :138 (rung 2, bias -1/3); the ladder (index.html:161-163) gives rung 2 as the completion problem with the hit-rate and bias lines removed. Read this round."},
    {"id": "LX2a-IDX-concept-anchors", "check": "every concept anchor in the hub resolves in course/concepts.html", "location": "course/modules/LX/LX2/index.html:35, :64-68; L01.html:37-38, :63; L02.html:37, :56", "status": "PASS",
     "evidence": "grep -c 'id=\"<concept>\"' course/concepts.html = 1 for exchange-vs-otc, limit-order-book, order-types, bid-ask-spread, quantifiers, present-value, derivative, partial-derivative, comparative-statics, evidence-grade, project-ladder (this round). concepts.html:37-39 shows evidence-grade and paper-anatomy as 'not yet released'. L03.html:37 uses limit-order-book and order-types."},
    {"id": "LX2a-IDX-data-status", "check": "data status paragraph (changed sentence about the registry)", "location": "course/modules/LX/LX2/index.html:170-171; L02.html:72, :87, :115, :118", "status": "PASS",
     "evidence": f"index.html:171 now reads 'The registry has no statute or case on conflicts of interest'. references/references.json contains 0 occurrences of 'conflict' and 0 of 'fiduciary' ({S}/out_r8_checks.txt section 5). The removed phrase 'no statute or case for fiduciary duty' was wrong: Dirks and O'Hagan are in the registry and concern fiduciary duty (references.json gpo1983dirks, gpo1997united), so the correction is accurate. The HYPOTHETICAL and SIMULATED labels match the labs (L02 HYPOTHETICAL; L03/L04 SIMULATED is outside this slice)."},
    {"id": "LX2a-IDX-core-reading", "check": "core reading lists registry keys", "location": "course/modules/LX/LX2/index.html:195-200", "status": "PASS",
     "evidence": "index.html:195-200 lists gpondsecurities, gpondsecuritiesb, gpo1983dirks, gpo1997united, cfandcode, frb2026fed; all six are in references/references.json (verify_refs offline PASS, {S}/out_commands2_r8.txt)."},
    {"id": "LX2a-IDX-banned", "check": "banned phrases (BUILDER_RULES 1.3-1.4) absent", "location": "course/modules/LX/LX2/index.html; L01.html; L02.html", "status": "PASS",
     "evidence": "check_pages LX2 PASS this round ({S}/out_commands_r8.txt), which applies BANNED (check_pages.py:58-72)."},
    {"id": "LX2a-IDX-cards-title", "check": "lesson titles in the hub match the h1 of each lesson", "location": "course/modules/LX/LX2/index.html:150-153, :181; L01.html:35; L02.html:35; L03.html; L04.html", "status": "PASS",
     "evidence": "L02.html:35 h1 'Insider trading and tipping' equals index.html:151 card title. L01.html:35 'Registration, Disclosure and the Two Acts' equals index.html:150 and :181. Read this round."},
    {"id": "LX2a-IDX-concept-link-hub-text", "check": "hub text about concept links (changed sentence at :62)", "location": "course/modules/LX/LX2/index.html:33, :75, :62, :170-171", "status": "PASS",
     "evidence": "The new sentence at index.html:62 ('Concepts that a prerequisite module defines link to its entry in the concept index, and concepts that an earlier lesson of LX2 defines link to that lesson's definition') agrees with the links at :64-68 (all to concepts.html anchors) and with L01.html:37-38 and L02.html:37 (links to L01.html#def-...). P0.1 wording at :35 and :68 matches concepts.html:37-39 'not yet released'."},
]

# L01: byte-identical since the round-7 pin; carry the round-7 PASS rows with the required prefix.
L01_CARRY = [
    ("LX2a-L01-structure", "L01 template sections", "course/modules/LX/LX2/L01.html:32-616", "PASS",
     "Read in full this round (L01.html:1-616): sections 1-10 in order; check_pages PASS this round."),
]
L01_IDS = [
    ("LX2a-L01-title-1933-1934", "L01.html:59, :61", "Titles of both Acts match GovInfo Title fields: 'To provide full and fair disclosure...' (COMPS-1884) and 'To provide for the regulation of securities exchanges...' (COMPS-1885), grep of the r8 details HTML and pdftotext output."),
    ("LX2a-L01-amended", "L01.html:65, :69", "'amended through Public Law 119-27, enacted July 18, 2025' (comps1884.txt:52, :118) and 'Public Law 119-60, enacted December 18, 2025' (comps1885.txt:9, :54), read this round."),
    ("LX2a-L01-quotes-1933", "L01.html:69-70, :80-85, :88", "Quotations located by quote_locate.py ({S}/out_quote_locate_L01_L02.txt): sections 6(c), 6(a), 5(a), 5(c), 8(a), 8(b), 8(d) FOUND in comps1884.txt; the 8(d) phrase split by the page footer was read by hand at comps1884.txt:1796-1807."),
    ("LX2a-L01-quotes-1934", "L01.html:100-111", "Quotations of 12(a), 12(b), 12(d), 13(a), 15(d)(1) FOUND in comps1885.txt ({S}/out_quote_locate_L01_L02.txt)."),
    ("LX2a-L01-5d", "L01.html:362", "Section 5(d) communications (EGC, QIB and accredited investors) verified in comps1884.txt:1389-1392 read this round."),
    ("LX2a-L01-6e1-8e", "L01.html:362-363, :483", "6(e)(1) confidential nonpublic review and the road-show sentence read at comps1884.txt:1553-1562 this round; 8(e) examination sentence at comps1884.txt:1812."),
    ("LX2a-L01-headings", "L01.html:360", "'EXEMPTED SECURITIES' heading before section 3 and 'EXEMPTED TRANSACTIONS' before section 4 (comps1884.txt:390, :748)."),
    ("LX2a-L01-markup", "L01.html:51-109, :359-386, :499-513, :604", "Markup read in full this round; grade spans carry data-grade and data-cite; grep: 62 claim spans, 0 without a data-locator."),
    ("LX2a-L01-why-decide", "L01.html:51", "The statutory words 'filed' and 'in effect' and the 'registered pursuant to section 12' wording (5(a), 5(c), 13(a), 15(d)(1)) match the quoted text in §2-§3."),
    ("LX2a-L01-why-requirements", "L01.html:51", "The sentence on the statutory words is a reading of §2-§3 and states no requirement beyond them."),
    ("LX2a-L01-in-effect-attribution", "L01.html:69", "'in effect' is the lesson's reading, labelled as such; the statute's section 2 is not read as defining it (read this round)."),
    ("LX2a-L01-readings-para", "L01.html:88", "Readings R5c and R5a follow the quoted 5(a) and 5(c) text (L01.html:80-82)."),
    ("LX2a-L01-exchange-defined", "L01.html:63, :96", "'national securities exchange' is stated as a statute term not defined in the lesson (L01.html:96); section 12 quotations at comps1885 use the term."),
    ("LX2a-L01-model", "L01.html:113-135; tests/labs/LX2/lab-LX2-L01-1.py:13, :30-72, :93-109", "Model: 5 x 2 = 10 states; 6 x 2 + 2 x 5 = 22 transitions (lab code lines 169-187 and output 'transitions: 22'), start unregistered/not_listed. Re-run this round."),
    ("LX2a-L01-lab1-run", "L01.html:137-315; tests/labs/LX2/lab-LX2-L01-1.py", "lab_twin_check.py this round: lab-LX2-L01-1 page_code_equals_twin=True, exit 0, stderr 0 bytes, expected_equals_output=True ({S}/out_lab_twin_r8.txt)."),
    ("LX2a-L01-lab1-hypothesis", "L01.html:139", "Hypothesis counts recomputed from the expected state table (L01.html:278-290): sale permitted 2, offer permitted 4, R13 5, R15 2; 0 both duties; 0 sale-without-offer; 10 of 10 reachable."),
    ("LX2a-L01-lab1-interpretation", "L01.html:314", "The interpretation does not overreach: it says the output checks the model and not the statute, and that R15 depends on A1."),
    ("LX2a-L01-prop4.1", "L01.html:320-329", "Proof re-derived this round: the ten paths (u,n), (u,l), (f,n), (f,l), (r,n), (r,l), (e,n), (e,l), (s,n), (s,l) use only the 22 transitions of the lab (lab output lines 292-313)."),
    ("LX2a-L01-prop4.2", "L01.html:332-341", "Proof re-derived: R13 needs listed, R15 needs not_listed; a state has one listing value, so no state satisfies both (lab state table)."),
    ("LX2a-L01-prop4.3", "L01.html:344-353", "Proof re-derived: R5a permits a sale only in effective, and R5c permits an offer in effective."),
    ("LX2a-L01-canon-breaks", "L01.html:355-367", "Canon-break citations (8(a), 12(d), 5(d), 6(e)(1), 8(e), 15(d)(1) third sentence, 12(a)) checked against comps1884/comps1885 this round: each quoted phrase FOUND (quote_locate output)."),
    ("LX2a-L01-misconceptions", "L01.html:369-389", "Each misconception's cited sentence was read against the statute text (5(a), 8(d), 6(a), 12(b), 13(a), 15(d)(1)) this round."),
    ("LX2a-L01-problems", "L01.html:391-494", "Solutions re-derived against the lab table: M1 (filed/effective/unlisted), M2 (stop order), M3 (listing and withdrawal), P1 (22), E2 counts 10+10+2=22, E1 2 of 10, E3, R2 quotation at comps1884.txt:1560-1561 FOUND this round."),
    ("LX2a-L01-key-results", "L01.html:499-513", "Key-results rows match the claims in §2-§5; the T rows are the Propositions 4.1-4.3 proofs (on the page); the C rows cite gpondsecurities or gpondsecuritiesb with a section."),
    ("LX2a-L01-quiz", "L01.html:517-600", "Quiz keys and explanations recomputed: Q1 correct option is the 5(a) wording (verbatim at comps1884.txt); Q5 = 30; Q8 = 22; Q9 = seven limits (§5 has seven items, L01.html:358-365); Q10 consistent with P3. Answer keys read this round."),
    ("LX2a-L01-references", "L01.html:602-606", "The keys cited on L01 (gpondsecurities, gpondsecuritiesb) exist in references/references.json; verify_refs offline PASS this round."),
    ("LX2a-L01-dag", "L01.html:37-38, :63; L01.html (whole page)", "check_dag LX2 PASS this round; L01 links only to concepts.html anchors (exchange-vs-otc, evidence-grade, quantifiers) and to its own defs."),
    ("LX2a-L01-hours", "L01.html:2, :34", "data-hours=9 and 'LX2 · Lesson 1 of 4 · 9 study hours' (L01.html:2, :34)."),
    ("LX2a-L01-paraphrase-locators", "L01.html:65-70, :80-85, :96-111, :362-363, :483", "Paraphrase spans re-read this round and their locators point to the sections they paraphrase (checked against comps1884/comps1885 text)."),
    ("LX2a-L01-unspanned-readings", "L01.html:51, :53, :69, :92, :96", "Readings are labelled as readings (scope-note at L01.html:53; 'the lesson's reading' at :69 and :88)."),
    ("LX2a-L01-section-locators", "L01.html:51-111, :359-365, :483", "Section locators for every claim span in §1-§3 read this round; each names a section present in the compilation."),
    ("LX2a-L01-lab1-run-extra", "L01.html:137-315", "python -I -W error tests/labs/LX2/lab-LX2-L01-1.py run this round: exit 0."),
]

for rid, loc, ev in [(x[0], x[1], x[2]) for x in L01_IDS]:
    rows.append({"id": rid, "check": "L01 check (carried; subject byte-identical)", "location": loc, "status": "PASS",
                 "evidence": R7_CARRY + ev.replace("{S}", S)})
rows.append({"id": "LX2a-L01-structure", "check": "L01 template sections", "location": "course/modules/LX/LX2/L01.html:32-616", "status": "PASS",
             "evidence": R7_CARRY + "L01.html sections 1-10 in order, read in full this round; check_pages PASS this round."})
rows.append({"id": "LX2a-L01-title-1933-1934-extra", "check": "L01 titles", "location": "L01.html:6, :35", "status": "PASS",
             "evidence": R7_CARRY + "L01.html:6 and :35 title 'Registration, Disclosure and the Two Acts' equals index.html:150."})

rows += [
    {"id": "LX2a-L02-structure", "check": "L02 template sections", "location": "course/modules/LX/LX2/L02.html:32-674", "status": "PASS",
     "evidence": "L02.html changed in the delta (hunks at :66-124, :119-125, :129, :430-446, :493-494, :570-580). Read in full this round, sections 1-10 in order; check_pages PASS this round."},
    {"id": "LX2a-L02-opinion-quotes", "check": "every opinion quotation in L02 against Dirks and O'Hagan, with its printed page", "location": "course/modules/LX/LX2/L02.html:58-110, :424-431, :441-445, :482, :541-548, :617", "status": "FAIL",
     "evidence": f"{S}/out_quote_locate_L01_L02.txt: all Dirks quotations FOUND at their locator pages (e.g. p. 654, 655, 657, 659, 660, 662, 663, 664, 668, 671, 672, 674, 676 n. 13), all O'Hagan quotations FOUND at their pages except: (a) L02.html:109 Thomas quotation (NOT FOUND, see LX2a-quote-search); (b) the footnote 5 quotation at L02.html:106 with '[his]' for 'O'Hagan's' is a bracketed alteration and is accepted. The classical-theory quotation at L02.html:67 (pp. 651-652) is FOUND across the page break: the source reads 'trades in the securities of his corporation' (ohagan.txt:487-488, p. 651) and 'on the basis of material, nonpublic information' (ohagan.txt:496, p. 652); the script's across-page test does not handle the footer, read by hand this round. The Dirks dissent at p. 671 is quoted as 'Accepting the Court's view of tippee liability' (dirks.txt, chunk page 671, verified). Fix (a) is the only defect in this row.",
     "fix": "L02.html:109: replace the quoted fragment 'the misappropriation theory fails to provide a coherent and consistent interpretation' with the verbatim 'the Commission’s misappropriation theory fails to provide a coherent and consistent interpretation', locator p. 680."},
    {"id": "LX2a-L02-n23-attribution", "check": "footnote 23 of Dirks (p. 663 n. 23) attributions", "location": "course/modules/LX/LX2/L02.html:56, :61, :431, :541, :617", "status": "PASS",
     "evidence": f"{S}/out_quote_locate_L01_L02.txt: 'a mental state embracing intent to deceive, manipulate, or defraud' and 'an independent element of a Rule 10b-5 violation' FOUND p. 663 (dirks.txt footnote 23, chunk page 663). The text 'Scienter in some cases is relevant in determining whether the tipper has violated his Cady, Roberts duty' (p. 663) is consistent with the quiz explanation at L02.html:617-618. The dissent's footnote 10 (p. 674 n. 10) concedes the scienter requirement and disputes only motive, so it does not contest 'independent element'."},
    {"id": "LX2a-L02-title-h1", "check": "L02 h1 equals the hub title", "location": "course/modules/LX/LX2/L02.html:35; index.html:151, :181", "status": "PASS",
     "evidence": "L02.html:35 'Insider trading and tipping' = index.html:151 card title and index.html:181 hours table."},
    {"id": "LX2a-L02-lab-run", "check": "lab-LX2-L02-1 runs alone", "location": "course/modules/LX/LX2/L02.html:127-425; tests/labs/LX2/lab-LX2-L02-1.py", "status": "PASS",
     "evidence": f"lab_twin_check.py this round: page_code_equals_twin=True, exit 0, stderr 0 bytes, expected_equals_output=True ({S}/out_lab_twin_r8.txt); run_labs PASS 7/7."},
    {"id": "LX2a-L02-lab-output", "check": "printed output and the expected block", "location": "course/modules/LX/LX2/L02.html:399-423; twin lines 86-283", "status": "PASS",
     "evidence": "Printed output re-run this round (25 lines): P1 classical fired pp. 651-652; P2 fails benefit p. 662; P3 and P4 fired p. 660; P5 fails knowledge p. 660; P6 fired p. 652; P7 fails source-not-told p. 655; P8 fails duty p. 652; fired 4 of 8."},
    {"id": "LX2a-L02-classical-element", "check": "classical branch elements and their locators", "location": "course/modules/LX/LX2/L02.html:73, :459; twin lines 226-231, 40", "status": "PASS",
     "evidence": "Twin lines 226-231 (classical checks, keys and pp. 651-652, p. 654) read this round; M1 solution (L02.html:459-467) describes the four checks as the code does."},
    {"id": "LX2a-L02-hypothesis", "check": "hypothesis before Lab 1 states the printed result", "location": "course/modules/LX/LX2/L02.html:129", "status": "PASS",
     "evidence": "Hypothesis at L02.html:129 (P1, P3, P4, P6 fired; P2, P5, P7, P8 unfired with the named elements) equals the printed table (lab output this round). It now cites Assumption A1 (§3) and A2, A3 (before the lab), which are declared at L02.html:83-86 and :119-125."},
    {"id": "LX2a-L02-example-3.2", "check": "Example 3.2 (P2 to P5)", "location": "course/modules/LX/LX2/L02.html:92-94", "status": "PASS",
     "evidence": "P2 benefit none fails p. 662; P3 and P4 fired p. 660; P5 knowledge fails p. 660 (lab output this round). The P4 'gift to a brother-in-law' is gift_to_relative_or_friend (twin line 146)."},
    {"id": "LX2a-L02-example-2.2-4.2", "check": "Examples 2.2 and 4.2 (P1, P6, P7)", "location": "course/modules/LX/LX2/L02.html:72-74, :111-113", "status": "PASS",
     "evidence": "P1 classical fired with pp. 651-652; P6 misappropriation fired p. 652; P7 fails source-not-told at p. 655 (lab output this round). The statement 'Each of the four checks passes' (L02.html:73) is correct for the classical branch (4 checks, twin lines 226-231)."},
    {"id": "LX2a-L02-canon-breaks", "check": "canon-break claims and quotations (§5)", "location": "course/modules/LX/LX2/L02.html:442-453", "status": "PASS",
     "evidence": "Five limits, as stated at L02.html:444. Benefit-label quotation 'objective facts and circumstances that often justify such an inference' FOUND p. 664 (dirks.txt, chunk 664); footnote 7 of O'Hagan (p. 655 n. 7) read in ohagan.txt chunk 13: 'the trader may still be liable under the misappropriation theory' with a trader owing duties to two entities (FOUND p. 655)."},
    {"id": "LX2a-L02-interpretation", "check": "interpretation paragraph", "location": "course/modules/LX/LX2/L02.html:424", "status": "PASS",
     "evidence": "The paragraph names only the printed table and the lab's rules; 'Assumption A1 (§3)' and 'a question of fact' (Dirks p. 664, FOUND) are accurate."},
    {"id": "LX2a-L02-misconceptions", "check": "misconceptions section", "location": "course/modules/LX/LX2/L02.html:441-446", "status": "PASS",
     "evidence": "Each cited sentence checked: p. 654 (possession), p. 660 (tippee assumes duty only when breach and knowledge), p. 662 ('Absent some personal gain...'), p. 652 and p. 653 n. 5 (misappropriation duty and outsider). P2, P5, P6, P8 outcomes match the lab (this round)."},
    {"id": "LX2a-L02-problems", "check": "problem set solutions and proofs", "location": "course/modules/LX/LX2/L02.html:449-553", "status": "PASS",
     "evidence": "M1-M3, Pr1-Pr3, E1-E3, R1-R3 re-derived this round. Pr1 now refers to 'Assumption A1 of §3', which is declared at L02.html:83-86. M3 re-run (scratch_e2_e3_m3.py, out_scratch_e2_e3_m3.txt): P3 not fired, element tipper's benefit (none), p. 662. E2 and E3 re-run: predictions match ('five of eight' and P2 fired p. 660; P7 fired p. 652)."},
    {"id": "LX2a-L02-pr1-A2", "check": "Pr1 cites an assumption that is declared in the lesson body", "location": "course/modules/LX/LX2/L02.html:83-86, :495-501", "status": "PASS",
     "evidence": "Round 7 failed this row because Assumption A1 was not declared. The delta now declares 'Assumption A1 (not read from the opinion)' in §3 at L02.html:83-86, and Pr1 cites 'Assumption A1 of §3' (L02.html:495-496). The declaration is read this round and matches the proof's use of A1."},
    {"id": "LX2a-L02-markup", "check": "markup of L02 (spans, dfn, classes)", "location": "course/modules/LX/LX2/L02.html:53, :84, :92, :541, :548, :599, :608, :617", "status": "PASS",
     "evidence": "Read in full this round. 66 claim spans, all grade C with data-cite and data-locator (grep); dfn ids def-insider-trading-doctrine, def-tipper-tippee-liability, def-misappropriation-theory each defined once (check_dag PASS)."},
    {"id": "LX2a-L02-E2-E3-scratch", "check": "E2 and E3 scratch predictions", "location": "course/modules/LX/LX2/L02.html:513-525", "status": "PASS",
     "evidence": f"{S}/scratch_e2_e3_m3.py run this round on copies of the twin: E2 (P2 reputational) P2 fired at p. 660, five of eight; E3 (P7 source-told false) P7 fired at p. 652, five of eight, as the solutions predict."},
    {"id": "LX2a-L02-key-results", "check": "key-results table rows and their sources", "location": "course/modules/LX/LX2/L02.html:570-580", "status": "PASS",
     "evidence": "Dissent cites verified this round: Dirks p. 672 'the relationship of trust and confidence between the insider and the shareholder' (FOUND p. 672); p. 671 'Accepting the Court's view of tippee liability' (FOUND p. 671); pp. 668, 674 'engrafts a special motivational requirement' and 'Personal gain is not an element' (FOUND); p. 676 n. 13 'the Court's somewhat cynical view, gifts involve personal gain' (FOUND, footnote 13 at dirks.txt chunk 676); O'Hagan p. 680 'fails to provide a coherent and consistent interpretation' (FOUND p. 680; the row's fragment is verbatim) and p. 679 'a party to a securities transaction' (FOUND p. 679)."},
    {"id": "LX2a-L02-quiz", "check": "quiz items and explanations", "location": "course/modules/LX/LX2/L02.html:574-643", "status": "PASS",
     "evidence": "Items 1-9 read this round. Keys and counts recomputed: Q6 P4 (gift, fired); Q7 4 fired; Q8 3 outsiders (P6-P8, twin roles); Q9 1 knowledge failure (P5). Explanation quotations FOUND (p. 654, 662, 655, 663 n. 23 with 'Scienter in some cases is relevant' at p. 663). Explanation at L02.html:617 for Q5 is accurate."},
    {"id": "LX2a-L02-dag", "check": "DAG: links and definitions in L02", "location": "course/modules/LX/LX2/L02.html:37, :56, :66, :80, :98", "status": "PASS",
     "evidence": "check_dag LX2 PASS this round. L02 links only exchange-act-1934 to L01.html#def-exchange-act-1934 (defined at L01.html:96); the new dfn 'tippee' at L02.html:77 is plain (no data-concept), so check_dag does not count it."},
    {"id": "LX2a-L02-B3-B1", "check": "L02 does not depend on Texas Gulf Sulphur or Dodd-Frank/MiFID II content", "location": "course/modules/LX/LX2/L02.html (whole page); index.html:171; L02.html:654", "status": "PASS",
     "evidence": "grep (this round, case-insensitive) of L02.html for Texas, Gulf, Dodd and MiFID: one match, the next-lesson navigation link title 'Manipulation, Dodd–Frank and MiFID II' (L02.html:654); no Texas Gulf Sulphur text and no Dodd-Frank or MiFID II content in the lesson. The only claim citations are gpo1983dirks and gpo1997united."},
    {"id": "LX2a-L02-years", "check": "no year printed for Dirks or O'Hagan in prose", "location": "course/modules/LX/LX2/L02.html (prose)", "status": "PASS",
     "evidence": "grep (this round) of L02.html for 4-digit years: the only matches are inside the identifier exchange-act-1934 (links at L02.html:37, :56); no year is printed for Dirks or O'Hagan in prose (plan Q8, N1 avoided)."},
    {"id": "LX2a-L02-why", "check": "why-it-matters paragraph", "location": "course/modules/LX/LX2/L02.html:51", "status": "PASS",
     "evidence": "L02.html:51 claims locate the duty (Dirks pp. 654, 660; O'Hagan p. 652); Dirks p. 654 'mere possession' FOUND. Read this round."},
    {"id": "LX2a-L02-tippee-definition", "check": "tippee definition", "location": "course/modules/LX/LX2/L02.html:76-77", "status": "PASS",
     "evidence": "Heading 'Tipping and the tippee's duty' (line 76) is followed by the plain dfn for 'tippee' at line 77, the first sentence of §3. Dirks p. 655 'Unlike insiders...' FOUND p. 655."},
    {"id": "LX2a-L02-page-locators", "check": "every claim span locator and the decision rows of the table", "location": "course/modules/LX/LX2/L02.html (all claim-span locators and the decision rows of the table)", "status": "PASS",
     "evidence": f"{S}/out_quote_locate_L01_L02.txt compared each quoted claim's locator page with the pages where its quote is found (this round): 1 apparent mismatch, the 2-word 'in connection with' span (its full quotation is at p. 656, FOUND). Paraphrase spans without a quotation were read this round and their locators checked against the printed text where cited. The decision rows match out_lab_twin_r8.txt."},
    {"id": "LX2a-L02-scienter-composite", "check": "scienter composite statement", "location": "course/modules/LX/LX2/L02.html:431", "status": "PASS",
     "evidence": "L02.html:431 'Scienter is not checked' and the Dirks p. 663 n. 23 quotation (FOUND p. 663). The lab prints 'Scienter is not checked.' (out_lab_twin_r8.txt)."},
    {"id": "LX2a-scope-note", "check": "scope note and lede scope words", "location": "course/modules/LX/LX2/index.html (lede); L01.html:53; L02.html:53", "status": "PASS",
     "evidence": "L01.html:53 and L02.html:53 read this round: each is an educational reading of cited sources, not legal advice, and each claim span carries its registry key and locator. index.html:33 lede read this round."},
    {"id": "LX2a-notation", "check": "notation: every symbol registered in notation/notation.json", "location": "course/modules/LX/LX2/L01.html:115-352 (math and labels); L02.html (whole page); index.html (placement math)", "status": "PASS",
     "evidence": "grep of TeX commands on the three pages: \\blacksquare (L01.html, 3 uses), \\partial, \\cdot, \\ldots (index.html). None of these is a notation macro with a meaning. notation.json has 'macros' and 'symbols' only (no proof-end mark). Registry flag below: \\blacksquare is not registered. The readings R5a, R5c, R13, R15 and the labels A1-A3, H1-H3, P1-P8 are local labels, not symbols of the registry. No collision with T, R, E, Prob, Var, Cov, SR, PBO, FDR."},
    {"id": "LX2a-L01-section-locators-extra", "check": "L01 section locators", "location": "course/modules/LX/LX2/L01.html:51-111, :359-365, :483", "status": "PASS",
     "evidence": R7_CARRY + "L01.html section locators (51-111) name sections present in comps1884 and comps1885, and the 6(e)(1) road-show locator is at comps1884.txt:1553-1562 (read this round)."},
    {"id": "LX2a-L02-M3-scratch", "check": "M3 scratch prediction (P3 benefit to none)", "location": "course/modules/LX/LX2/L02.html:469-475", "status": "PASS",
     "evidence": f"{S}/scratch_e2_e3_m3.py (m3) run this round: P3 not fired, element tipper's personal benefit (none), key gpo1983dirks, p. 662, as the solution (L02.html:469-475) predicts."},
    {"id": "LX2a-registry-keys", "check": "every registry key cited in L01, L02 and the hub exists", "location": "references/references.json; course/modules/LX/LX2/index.html:195-200; L01.html; L02.html", "status": "PASS",
     "evidence": f"Keys cited by claim spans: gpondsecurities, gpondsecuritiesb, gpo1983dirks, gpo1997united (and cfandcode, frb2026fed in the hub reading list). verify_refs --unit LX2 live: 6 of 560 entries, 0 problems ({S}/out_commands2_r8.txt). {S}/out_r8_checks.txt section 5: 0 'conflict' and 0 'fiduciary' in references.json."},
    {"id": "LX2a-counter-evidence", "check": "grade-C doctrine claims name the published dissents that dispute the same tests (BUILDER_RULES 1.5; VERIFIER 2.3)",
     "location": "course/modules/LX/LX2/L02.html:90 (benefit test), :109 (misappropriation), :570-580 (key results)", "status": "PASS",
     "evidence": f"Round 7 failed this row. The delta adds the Blackmun dissent (Dirks, from p. 667; FOUND p. 667-668) to the benefit test (L02.html:90), and the Thomas (p. 680) and Scalia (p. 679) opinions to the misappropriation section (L02.html:109). The key-results rows cite the dissents (L02.html:570-580). Read this round against dirks.txt and ohagan.txt ({S}/out_r8_checks.txt section 3). Checked the classical theory: Thomas and Scalia in O'Hagan dispute misappropriation only, and do not contest the classical theory (ohagan.txt chunk 55); no dissent disputes the possession principle (dirks.txt: 'possession' appears once in the dissent, as a fact). The fragment at L02.html:109 is a separate failing row (LX2a-quote-search)."},
    {"id": "LX2a-lab-assumptions", "check": "Lab 1 declares numbered Assumptions for facts assumed without proof (plan 2.1 item 6)",
     "location": "course/modules/LX/LX2/L02.html:83-86, :119-125, :127-129; tests/labs/LX2/lab-LX2-L02-1.py:6-23", "status": "PASS",
     "evidence": "Round 7 failed this row. The delta adds 'Assumptions of Lab 1' at L02.html:119-125 (A2: facts stated are true; A3: temporary fiduciary stated with role issuer_insider) and A1 in §3 at L02.html:83-86. The lab's hypothesis (L02.html:129) cites them. The twin docstring (lab-LX2-L02-1.py:6-23) describes the same reading (read this round). The assumptions block is placed before the lab, as the plan requires."},
    {"id": "LX2a-L02-remark-3.3", "check": "Remark 3.3: each sentence matches the cited page (p. 662 and p. 660)",
     "location": "course/modules/LX/LX2/L02.html:97", "status": "FAIL",
     "evidence": f"Second sentence, cited to p. 660: 'It does not decide whether the tippee knew or should have known of the breach, which is a separate element.' Dirks p. 660 states knowledge as one of the conditions of the tippee's duty: 'the tippee knows or should know that there has been a breach' (dirks.txt, page 660; {S}/out_r8_checks.txt section 4). A sentence attributed to p. 660 that says the opinion does not decide the knowledge condition contradicts the condition the page states. The first sentence (benefit test, p. 662, FOUND) is accurate.",
     "fix": "L02.html:97: replace the second sentence with: 'The tippee's knowledge is a separate condition, which the opinion states at p. 660, and the lab checks it as its own element.' (keep the locator p. 660)."},
    {"id": "LX2a-r8-delta", "check": "delta from the round-7 pin over slice a: every changed hunk read",
     "location": "course/modules/LX/LX2/index.html:59-62, :168-171; course/modules/LX/LX2/L02.html:66-125, :129, :430-446, :493-496, :570-580; tests/labs/LX2/lab-LX2-L02-1.py:6-7",
     "status": "PASS",
     "evidence": f"git diff 06994db1 0dee921a -- index.html L02.html lab-LX2-L02-1.py: 3 files, 32 insertions, 18 deletions (this round). L01.html and tests/labs/LX2/lab-LX2-L01-1.py: git diff --quiet exit 0, byte-identical. Every hunk read in full and each is covered by a row above (hub :62 and :171; L02 :66-125, :129, :430-446, :493-496, :570-580; twin docstring line 7). Not in the slice: cards.json, project.html and the project twins (other slices)."},
]

fragment = {
    "unit": "LX2",
    "slice": "LX2-a",
    "round": 8,
    "verifier": "Haiku independent verifier, LX2-a round 8 (did not build LX2; builder ledgers and scratch not read; round-7 fragment read as context only; every row re-checked this round, carried only for L01 rows whose subject is byte-identical)",
    "pin": "0dee921a33dc1275ff9b1babc6c2fdf3daac62c3",
    "base": "06994db16d1ab449bcf29898a7f56cfa999dce57",
    "checkout": CHK,
    "scratch": "/tmp/lx2a_r8_dl (four primary sources re-fetched by plain curl through ledgers/LX2/scripts/LX2-a-r8/fetch_sources.sh; PDF and txt hashes identical to round 7); /tmp/lx2a_r8_scratch and /tmp/lx2a_r8_scratch2 (scratch copies of the L02 twin; nothing written into the repository)",
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [
        "references/references.json key gpo1983dirks: title field reads 'Dirks v. SEC, 463 U.S. 646 (1982)' and year field reads 1983 (references.json:10823-10835). GovInfo USREPORTS-463-646 details: decided July 1, 1983. No slice-a page prints a year for Dirks. The architect corrects the record through add_reference.py.",
        "notation/notation.json does not register \\blacksquare, the proof-end mark used on L01.html (three uses) and on other course pages. Under BLUEPRINT notation rule 13 a strict reading would make this a FAIL; the round-7 ruling (registry flag) is kept. The architect decides whether to register it.",
        "No registry key or source string exists for Dodd-Frank, MiFID II or Texas Gulf Sulphur (grep, references/references.json). L02 and the hub say so; the REFERENCE_REQUESTS stay open.",
    ],
    "freshness_flags": [],
    "notes": (
        "Round 8 at pin 0dee921a. Delta from 06994db1 over slice a: index.html (two prose hunks), L02.html (opinion counter-evidence, Assumption A1 in §3, Assumptions of Lab 1, dfn tippee, key-results dissents) and the L02 twin (docstring word 'quotes' changed to 'states'). L01.html and the L01 twin are byte-identical. Every hunk was read; the three round-7 FAIL rows were re-verified from scratch: LX2a-L02-pr1-A2 and LX2a-lab-assumptions now PASS, LX2a-counter-evidence now PASS (dissents are present and their pages verified). Two new defects: the Thomas quotation at L02.html:109 is not verbatim (LX2a-quote-search, LX2a-L02-opinion-quotes), and the Remark 3.3 knowledge sentence contradicts the p. 660 condition it cites (LX2a-L02-remark-3.3). Labs are demonstrations; no mutants are required for this slice (VERIFIER 2.6 applies to project graders only). Other observations, not rows: the word 'twin' appears in learner text at L02.html:528 (not on the banned list); the hub's earlier claim that the registry had no fiduciary-duty statute was wrong and is now corrected at index.html:171."
    ),
    "summary": (
        "Slice LX2-a round 8 verdict FAIL at 0dee921a. Rows: see counts computed by the writer. Failing rows: LX2a-quote-search, LX2a-L02-opinion-quotes (both L02.html:109, the Thomas dissent quotation, not verbatim) and LX2a-L02-remark-3.3 (L02.html:97, attribution contradicts p. 660)."
    ),
}

counts = {"PASS": 0, "FAIL": 0, "UNVERIFIABLE": 0}
for r in rows:
    counts[r["status"]] += 1
fragment["summary"] = (
    f"Slice LX2-a round 8 verdict FAIL at 0dee921a. {len(rows)} rows: PASS {counts['PASS']}, FAIL {counts['FAIL']}, "
    f"UNVERIFIABLE {counts['UNVERIFIABLE']}. Failing rows: LX2a-quote-search and LX2a-L02-opinion-quotes (L02.html:109, "
    "the Thomas dissent quotation is not verbatim), LX2a-L02-remark-3.3 (L02.html:97, the sentence attributed to p. 660 "
    "contradicts the knowledge condition stated there). Mutants: none (slice a is not a project grader)."
)

out = f"{CHK}/ledgers/LX2/LX2-a.json"
with open(out, "w", encoding="utf-8") as fh:
    json.dump(fragment, fh, ensure_ascii=False, indent=2)
    fh.write("\n")
print("wrote", out, counts)
