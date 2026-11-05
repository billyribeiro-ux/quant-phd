"""Write the round 7 fragment ledgers/LX2/LX2-a.json for slice LX2-a (hub index.html, L01, L02, lab twins L01 and L02).

Usage: python -I ledgers/LX2/scripts/LX2-a-r7/write_fragment.py <checkout_root> <fragment_out>
Every row id of the round 6 fragment is kept. Each row states the command or script output that backs it, by its
repository path under ledgers/LX2/scripts/LX2-a-r7/. Validate afterwards with tools/ledger.py validate.
"""

import json
import sys
from datetime import UTC, datetime

S = "ledgers/LX2/scripts/LX2-a-r7/"


def row(rid: str, check: str, location: str, status: str, evidence: str, fix: str | None = None) -> dict:
    out = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        if not fix:
            raise SystemExit(f"{rid}: non-PASS row needs a fix")
        out["fix"] = fix
    return out


ROWS = [
    row("LX2a-cmd-check_pages", "tools/check_pages.py --unit LX2 (structure, banned phrases, hours, hub split)",
        "course/modules/LX/LX2/index.html, L01.html, L02.html", "PASS",
        f"Run this round at the pin: 'check_pages LX2: PASS', exit 0 ({S}out_check_pages.txt)."),
    row("LX2a-cmd-check_dag", "tools/check_dag.py --unit LX2 (linked uses and definitions)",
        "L01.html, L02.html, index.html", "PASS",
        f"Run this round: 'check_dag LX2: PASS', exit 0 ({S}out_check_dag.txt). Independent grep: each LX2 dfn id "
        "(securities-registration, exchange-act-1934, insider-trading-doctrine, tipper-tippee-liability, "
        "misappropriation-theory) is defined once in course/."),
    row("LX2a-cmd-run_labs", "tools/run_labs.py --unit LX2 (all seven twins)",
        "tests/labs/LX2/lab-LX2-L01-1.py, tests/labs/LX2/lab-LX2-L02-1.py and the other LX2 twins", "PASS",
        f"Run this round: 'run_labs LX2: PASS (7/7)', exit 0 ({S}out_run_labs.txt)."),
    row("LX2a-lab-isolated", "twin alone under python -I -W error; page code equals twin; expected block equals output",
        "L01.html:137-315 with tests/labs/LX2/lab-LX2-L01-1.py; L02.html:113-425 with tests/labs/LX2/lab-LX2-L02-1.py",
        "PASS",
        f"{S}lab_twin_check.py: 'lab-LX2-L01-1: page_code_equals_twin=True exit=0 expected_equals_output=True' "
        f"({S}out_lab_twin_L01.txt); 'lab-LX2-L02-1: page_code_equals_twin=True exit=0 expected_equals_output=True' "
        f"({S}out_lab_twin_L02.txt). Each twin run alone as python -I -W error exit 0, stderr empty; a second run is "
        f"byte-identical ({S}out_lab_L01_run.txt, {S}out_lab_L02_run.txt)."),
    row("LX2a-cmd-page_smoke", "tools/page_smoke.py --unit LX2 --pages <each page alone> (console errors, KaTeX, external requests, overflow, figures)",
        "course/modules/LX/LX2/index.html, L01.html, L02.html", "PASS",
        f"Run alone this round: 'page_smoke modules/LX/LX2/index.html: PASS' ({S}out_page_smoke_index.txt), "
        f"'...L01.html: PASS' ({S}out_page_smoke_L01.txt), '...L02.html: PASS' ({S}out_page_smoke_L02.txt); exit 0 each. "
        "The tool's own lab timings (0.0 s) are reported as printed; they were not measured against a quiet-machine budget."),
    row("LX2a-cmd-ruff-mypy", "ruff check, ruff format --check, mypy --no-incremental on the slice-a twins",
        "tests/labs/LX2/lab-LX2-L01-1.py, tests/labs/LX2/lab-LX2-L02-1.py", "PASS",
        f"'All checks passed!' ({S}out_ruff_check.txt); '7 files already formatted' ({S}out_ruff_format.txt); "
        f"'Success: no issues found in 2 source files' ({S}out_mypy.txt)."),
    row("LX2a-cmd-pytest", "pytest: tests/test_labs.py, tests/test_run_labs.py, tests/test_page_checks.py",
        "tests/", "PASS",
        f"{S}out_pytest_relevant.txt: 100%, exit 0. The full tests/ directory was not run; the rules ask for the relevant modules."),
    row("LX2a-cmd-verify_refs", "tools/verify_refs.py --unit LX2 (live) and --offline",
        "references/references.json (LX2 keys gpondsecurities, gpondsecuritiesb, gpo1983dirks, gpo1997united, cfandcode, frb2026fed)",
        "PASS",
        f"{S}out_verify_refs_unit_live.txt: 'live re-verification of LX2: 6 of 560 entries, 0 problems', exit 0; "
        f"{S}out_verify_refs_offline.txt: 'offline integrity: 560 entries, 0 problems', exit 0."),
    row("LX2a-cmd-coursekit-closure", "prerequisite closure of LX2 (tools/coursekit.py prerequisite_closure)",
        "course/modules/LX/LX2/index.html:35, :62", "PASS",
        f"{S}out_coursekit_closure.txt: {{'P0.1', 'M2', 'FC1', 'E1', 'M1'}} = {{E1, FC1, M1, M2, P0.1}}, the hub's statement at index.html:62."),
    row("LX2a-quote-search", "every curly-quoted passage on L01 and L02 searched in the primary text, with the printed page",
        "course/modules/LX/LX2/L01.html, L02.html", "PASS",
        f"Sources re-fetched this round with plain curl ({S}fetch_sources.sh into an empty scratch directory). The four PDFs and "
        f"their pdftotext files hash identical to round 6 ({S}out_sha256_sources_r7.txt vs ledgers/LX2/scripts/LX2-a-r6/out_sha256_sources.txt). "
        f"{S}quote_locate.py: L01 70 quotations, 51 FOUND ({S}out_quote_locate_L01.txt); L02 54 quotations, 39 FOUND with printed pages "
        f"({S}out_quote_locate_L02.txt). Every NOT FOUND row is either a NO-CLAIM label (a misconception heading or a printed output "
        "label, not a source quotation) or one of four source sentences that the script could not match, each checked by hand: "
        "the 1933 Act 8(d) sentence 'issue a stop order suspending the effectiveness of the registration statement' and the "
        "15(d)(1)/8(d) fragment, both split by a page footer (comps1884.txt:1796-1799); O'Hagan's classical-theory sentence, split "
        "across printed pp. 651-652 (ohagan.txt:485-497); O'Hagan footnote 5 with '[his]' for O'Hagan's (ohagan.txt:576, printed p. 653). "
        "Titles and the two amendment lines were also checked against the GovInfo details pages (see LX2a-L01-title-1933-1934)."),
    row("LX2a-IDX-hours", "hub hours split and lesson hours (36 lesson + 14 project = 50; 4 x 9)",
        "course/modules/LX/LX2/index.html:29, :44, :176-186; L01.html:2, :34; L02.html:2, :34", "PASS",
        f"index.html:29 data-hours-lessons=\"36\" data-hours-project=\"14\"; :44 '36 h lessons · 14 h project (28% of 50 h)'; "
        f"recomputed in {S}r7_checks.py section 2: 4 x 9 = 36, 36 + 14 = 50, 14/50 = 28%, 36/50 = 72% (the bar width at :42)."),
    row("LX2a-IDX-structure", "hub sections in BUILDER_RULES 4.1 order: lede, objectives, prerequisites, placement, lessons, ladder, data, hours, core reading",
        "course/modules/LX/LX2/index.html:1-207", "PASS",
        "Read in full this round (index.html lines 1-207). Order: header and meta-row 29-45; objectives 47-58; prerequisites 60-71; "
        "placement 73-144 (ten items, two skill checks marked data-skill); lessons 146-155; ladder 157-166; data 168-172; hours 174-189; "
        "core reading 191-202. check_pages LX2 PASS (out_check_pages.txt)."),
    row("LX2a-IDX-closure", "hub prerequisite-closure statement", "course/modules/LX/LX2/index.html:35, :62", "PASS",
        "index.html:62 states '{E1, FC1, M1, M2, P0.1}'; equals the coursekit output (out_coursekit_closure.txt)."),
    row("LX2a-IDX-FC1-title", "FC1 title as linked from the hub", "course/modules/LX/LX2/index.html:35", "PASS",
        "index.html:35 'FC1 The Financial System, Markets & Instruments' = curriculum/02-economics-finance-core.yaml:364 title "
        "'The Financial System, Markets & Instruments' (read this round)."),
    row("LX2a-IDX-SR4", "the later module that lists LX2 as a prerequisite", "course/modules/LX/LX2/index.html:39", "PASS",
        "index.html:39 'SR4 Regulation's Market Footprint, which lists LX2 among its prerequisites' = curriculum/05-macro-alternatives.yaml:506 "
        "title and :509 'prereqs: [SR1, FI4, LX2]' (read this round)."),
    row("LX2a-IDX-lede-markup", "lede promise: each quoted statute or holding carries its section or page locator and is graded C; statements the module cannot source are marked not stated here",
        "course/modules/LX/LX2/index.html:33; L01.html:51, :59-65; L02.html:51-110", "PASS",
        f"Re-read this round. index.html:33 makes the promise. Claim-span attribute check ({S}out_span_attr_and_xref.txt): index 0 spans, "
        "L01 62 spans, L02 59 spans, none lacking data-grade, data-cite or data-locator; L01 keys gpondsecurities and gpondsecuritiesb, "
        "L02 keys gpo1983dirks and gpo1997united, all in the registry. Not-sourced statements are marked 'not stated here' (L01.html:74, :476; index.html:33, :171)."),
    row("LX2a-IDX-objectives-1-3", "objectives 1-3 are delivered by the lessons they name", "course/modules/LX/LX2/index.html:51-53; L01.html:55-130; L02.html:55-111, :113-425", "PASS",
        "Objective 1 (quote filing, effectiveness, stop-order and reporting sentences): L01 §2-§3 quote 6(a), 8(a), 8(d), 13(a), 15(d)(1). "
        "Objective 2 (trace registration statuses): L01 §4 model and Lab 1. Objective 3 (classify a pattern under the elements): L02 Lab 1 and "
        "its twin's branch_checks (tests/labs/LX2/lab-LX2-L02-1.py:224-259)."),
    row("LX2a-IDX-placement-arith", "placement diagnostic answers and their arithmetic", "course/modules/LX/LX2/index.html:95-141", "PASS",
        f"Recomputed this round ({S}r7_checks.py section 2): PV 100/1.1 = 90.909 -> 90.91 (data-answer 90.91, tol 0.01); d/dx x^2 at 3 = 6; "
        "d/dx (x^2 y) at (2,3) = 12; spread 100.10 - 99.50 = 0.60 (tol 0.001); hit rate 6/8 = 0.75; differences -1, -1, 1, sum -1, bias -1/3 = -0.3333 (tol 0.001). "
        "'Seven of ten is 70 percent' (index.html:75) is arithmetic."),
    row("LX2a-IDX-placement-items-1-8", "placement items 1-8: one data-correct option that is right, and the explanation",
        "course/modules/LX/LX2/index.html:77-131", "PASS",
        "Read each item: item 1 T (proved on the page); item 2 equilibria before and after a parameter change; item 4 the existential negation; "
        "item 7 the over-the-counter market; items 3, 5, 6, 8 numeric answers checked above. Each explanation matches its item."),
    row("LX2a-IDX-placement-cross-ref", "the rung-1 skill check says Lesson 4 defines the hit rate", "course/modules/LX/LX2/index.html:136; course/modules/LX/LX2/L04.html:114", "PASS",
        "index.html:136 'Lesson 4 defines the hit rate for the project's model case.' L04.html:114 carries '<dfn>hit rate</dfn> is the share of hits in a window of \\(H\\) periods' (grep this round, out_span_attr_and_xref.txt)."),
    row("LX2a-IDX-skill-items", "skill checks: rung-1 hit rate and rung-2 bias are the measures Lesson 4 defines", "course/modules/LX/LX2/index.html:133, :138", "PASS",
        "index.html:133 defines the hit rate as hits divided by pairs (6 of 8 = 0.75); index.html:138 defines the bias as the mean of forecast minus realised. "
        "L04.html defines both (grep this round: hit rate dfn at L04.html:114; bias defined in L04)."),
    row("LX2a-IDX-concept-anchors", "every concept link on the hub and the lessons resolves to an anchor in course/concepts.html; local def links resolve",
        "course/modules/LX/LX2/index.html:35, :64-68; L01.html:37-38, :63; L02.html:37, :56", "PASS",
        f"{S}r7_checks.py section 7: all 11 hub concept anchors present in course/concepts.html. L01 links exchange-vs-otc, evidence-grade, quantifiers "
        "(all present); L02.html:37, :56 link exchange-act-1934 to L01.html#def-exchange-act-1934, which exists at L01.html:96."),
    row("LX2a-IDX-data-status", "hub data-status statements: which labs are HYPOTHETICAL and which are SIMULATED (slice-a portion)",
        "course/modules/LX/LX2/index.html:170-171; L02.html:72, :87, :115, :118", "PASS",
        "index.html:170 labels the eight Lesson 2 patterns HYPOTHETICAL; L02.html:72 (Example 2.2), :87 (Example 3.2), :115 (hypothesis) and the twin's "
        "docstring (tests/labs/LX2/lab-LX2-L02-1.py:3) agree. The Lesson 3 and 4 labs named as SIMULATED use a fixed seed: "
        "tests/labs/LX2/lab-LX2-L03-1.py:152 random.Random(SEED); tests/labs/LX2/lab-LX2-L04-1.py:7 seed 20261103."),
    row("LX2a-IDX-core-reading", "core reading lists the registry keys of plan 7.1 and nothing else", "course/modules/LX/LX2/index.html:195-200", "PASS",
        f"index.html:195-200 lists gpondsecurities, gpondsecuritiesb, gpo1983dirks, gpo1997united, cfandcode, frb2026fed (the six keys of plan §7.1). "
        f"All six present in references/references.json ({S}r7_checks.py section 6). Rendering is by course/assets/js/refs.js from the site data."),
    row("LX2a-IDX-banned", "banned phrases (BUILDER_RULES 1.3-1.4) absent from the hub and the two lessons", "course/modules/LX/LX2/index.html; L01.html; L02.html", "PASS",
        "check_pages LX2 PASS (BANNED list, tools/check_pages.py:58-72). Independent grep this round (case-insensitive, outside code): no TODO, TBD, "
        "lorem, 'for brevity', 'details omitted', 'beyond the scope', 'it is important to note', 'studies show', 'experts agree', 'well known', "
        "'obviously', 'clearly'. The only ellipses are inside Python code (L01.html:169-174; L02.html:201, :339)."),
    row("LX2a-IDX-cards-title", "lesson card titles on the hub match each lesson's h1", "course/modules/LX/LX2/index.html:150-153, :181; L01.html:35; L02.html:35; L03.html; L04.html", "PASS",
        "index.html card titles equal the h1 of L01 'Registration, Disclosure and the Two Acts', L02 'Insider trading and tipping', L03 'Manipulation, Dodd–Frank and MiFID II', L04 'Fiduciary Duty, Conflicts and Model-Risk Governance' (grep this round)."),
    row("LX2a-IDX-concept-link-hub-text", "hub text names the Acts, the lessons and the placement items it claims", "course/modules/LX/LX2/index.html:33, :75, :170-171", "PASS",
        "index.html:33 names the Securities Act of 1933 and the Securities Exchange Act of 1934 and the module's lessons; :75 the 80 percent bar and the two skill checks; :170-171 the data statements, which match the lab twins."),
    row("LX2a-L01-structure", "lesson template order (BUILDER_RULES 4.2): why, core sections, lab, canon breaks, misconceptions, problems, key results, quiz",
        "course/modules/LX/LX2/L01.html:32-616", "PASS",
        "Read in full this round (lines 1-616). Header 33-40; grade legend 42-49; why-it-matters 51 (119 words, within 120); scope note 53; §1-§4 55-135 "
        "with the lab inline at 137-315; Propositions 317-353; §5 canon breaks 355-367; §6 misconceptions 369-389 (four); §7 problem set 391-494 (three problems "
        "in each of mechanics, proof, empirical, research; twelve details.solution blocks); §8 key results 496-515 (ten rows); §9 quiz 517-600 (ten items, all with explain); "
        "§10 references 602-606. No debate brief (the curriculum entry has no debate key)."),
    row("LX2a-L01-title-1933-1934", "the Title field quoted for each Act", "course/modules/LX/LX2/L01.html:59, :61", "PASS",
        f"Both quoted titles are in the GovInfo details pages fetched this round: COMPS-1884 Title 'To provide full and fair disclosure of the character of "
        f"securities sold in interstate and foreign commerce and through the mails, and to prevent frauds in the sale thereof, and for other purposes.' and "
        f"COMPS-1885 'To provide for the regulation of securities exchanges and of over-the-counter markets ...' ({S}out_title_check.txt: both True, and both Public Law lines True). "
        "Both are also in the compilation text (out_quote_locate_L01.txt, FOUND)."),
    row("LX2a-L01-amended", "the amendment public law and enactment date quoted from each GovInfo record", "course/modules/LX/LX2/L01.html:65, :69", "PASS",
        "L01.html:65 'Public Law 119-27, enacted July 18, 2025' (1933) = COMPS-1884 details 'Amended Through ... Public Law 119-27, Enacted July 18, 2025' and "
        "comps1884.txt:1797 'As Amended Through P.L. 119-27, Enacted July 18, 2025'. L01.html:65 'Public Law 119-60, enacted December 18, 2025' (1934) = "
        "COMPS-1885 details and comps1885.txt 'As Amended Through P.L. 119-60, Enacted December 18, 2025'."),
    row("LX2a-L01-quotes-1933", "every 1933 Act quotation on L01 against the compilation text", "course/modules/LX/LX2/L01.html:69-70, :80-85, :88", "PASS",
        "out_quote_locate_L01.txt: 6(a) FOUND (comps1884.txt); 6(c) both sentences FOUND; 5(a) both FOUND; 5(c) FOUND; 8(a) FOUND; 8(b) both FOUND, and the "
        "paraphrase matches comps1884.txt:1768-1781; 8(d) 'the stop order shall cease to be effective' FOUND; 8(d) 'issue a stop order suspending the effectiveness "
        "of the registration statement' split by a page footer (comps1884.txt:1796-1799), verified by hand. The 6(c) paraphrase 'the fee that section 6(b) requires' "
        "matches comps1884.txt (subsection (c): 'the amount of the fee required under subsection (b)')."),
    row("LX2a-L01-quotes-1934", "every 1934 Act quotation on L01 against the compilation text", "course/modules/LX/LX2/L01.html:100-111", "PASS",
        "out_quote_locate_L01.txt: 12(a) FOUND (comps1885.txt:7002-7006); 12(b) FOUND (7010-7011); 12(d) first sentence FOUND (7100-7103; the statute reads "
        "'If the exchange authorities certify', the page's 'after the exchange certifies' is a paraphrase, and the thirty-day quotation is exact); 12(d) second sentence FOUND (7105-7112, "
        "'relieved' paraphrase matches); 13(a) FOUND; 15(d)(1) first FOUND (11110-11111), second FOUND (11113-11114), third sentence FOUND ('held of record by less than "
        "300 persons', comps1885.txt:11121-11122) with the bank count of 1,200 persons (11122-11124)."),
    row("LX2a-L01-5d", "section 5(d) statement (emerging growth company communications)", "course/modules/LX/LX2/L01.html:362", "PASS",
        "comps1884.txt:1388-1390: '(d) LIMITATION. Notwithstanding ... an emerging growth company ... may engage in oral or written communications with potential investors that are qualified institutional buyers or institutions that are accredited investors' (read this round)."),
    row("LX2a-L01-6e1-8e", "section 6(e)(1) and 8(e) statements (confidential draft; examination)", "course/modules/LX/LX2/L01.html:362-363, :483", "PASS",
        "comps1884.txt:1553-1555: 6(e)(1) 'may confidentially submit ... a draft registration statement, for confidential nonpublic review by the staff of the Commission prior to public filing' FOUND. The R2 quotation on 'not later than 15 days before ... a road show' is in the same subsection (FOUND, out_quote_locate_L01.txt). 8(e) (comps1884.txt:1811-1813) 'empowered to make an examination in any case ... whether a stop order should issue under subsection (d)' matches the page's paraphrase."),
    row("LX2a-L01-headings", "headings before sections 3 and 4 quoted as headings", "course/modules/LX/LX2/L01.html:360", "PASS",
        "comps1884.txt:390 'EXEMPTED SECURITIES' directly before 'SEC. 3.' (line 392); comps1884.txt:748 'EXEMPTED TRANSACTIONS' directly before 'SEC. 4.' (line 750). Both quotations FOUND (out_quote_locate_L01.txt)."),
    row("LX2a-L01-markup", "every claim span carries cite, locator and grade; cite keys limited to the lesson's sources",
        "course/modules/LX/LX2/L01.html:51-109, :359-386, :499-513, :604", "PASS",
        f"{S}out_span_attr_and_xref.txt: 62 claim spans in L01, none lacking data-grade, data-cite or data-locator; keys gpondsecurities and gpondsecuritiesb only; both are in the registry."),
    row("LX2a-L01-why-decide", "the 'why it matters' decision sentence: which statute governs which duty", "course/modules/LX/LX2/L01.html:51", "PASS",
        "The quoted words 'filed' and 'in effect' sit in a claim span with locators 5(a), 5(c), 13(a), 15(d)(1). 'in effect' is not defined in §2: comps1884.txt lines 34-391 (section 2) contain no 'in effect' (grep this round). 'registered pursuant to section 12' FOUND in 13(a); 'has become effective' FOUND in 15(d)(1)."),
    row("LX2a-L01-why-requirements", "statutory requirements in the why-it-matters paragraph carry spans and locators", "course/modules/LX/LX2/L01.html:51", "PASS",
        "Sentences 1 and 2 of the paragraph are claim spans (sections 5(a), 5(c); section 12, 13(a)). The 'offer and sale' condition reading is backed by 5(a) and 5(c) text (out_quote_locate_L01.txt)."),
    row("LX2a-L01-in-effect-attribution", "the 'in effect' reading and section 8 quotations: the span holds only what the statute says", "course/modules/LX/LX2/L01.html:69", "PASS",
        "The claim span (sections 8(a) and 8(d)) holds the two quotations only; 'the statement has taken effect under section 8(a) and has not been suspended under section 8(d)' is an un-spanned reading (scope note, L01.html:53)."),
    row("LX2a-L01-readings-para", "the paragraph stating two readings and their use in section 4", "course/modules/LX/LX2/L01.html:88", "PASS",
        "The two readings (a filed statement is not in effect, so 5(a) still bars a sale; R5c permits an offer once filed unless a refusal or stop order applies) match offer_permitted and sale_permitted in tests/labs/LX2/lab-LX2-L01-1.py:99-107 and the printed table."),
    row("LX2a-L01-exchange-defined", "the term national securities exchange is not defined by the lesson but used as the statute uses it", "course/modules/LX/LX2/L01.html:63, :96", "PASS",
        "L01.html:63 and :96 say the lesson does not define the term further; the statute's sections 12(a), 12(b) use it (out_quote_locate_L01.txt)."),
    row("LX2a-L01-model", "the finite-state model: states, transitions and readings match the lab twin", "course/modules/LX/LX2/L01.html:113-135; tests/labs/LX2/lab-LX2-L01-1.py:13, :30-72, :93-109", "PASS",
        f"Twin: STATUSES 5, LISTINGS 2 (10 states), EVENTS_1933 6 events x 2 listings = 12, EVENTS_1934 2 events x 5 statuses = 10, total 22 (out_lab_L01_run.txt: 'candidate states: 10, transitions: 22'). The printed transition list ({S}out_lab_L01_run.txt, 22 lines, each with its locator) matches the 12 + 10 events of §4 (L01.html:119-120). Readings R13, R15 (A1), R5c, R5a are the twin's duty_13, duty_15d, offer_permitted, sale_permitted."),
    row("LX2a-L01-lab1-run", "Lab 1 (L01) runs and its page code and expected block match the twin", "course/modules/LX/LX2/L01.html:137-315; tests/labs/LX2/lab-LX2-L01-1.py", "PASS",
        f"out_lab_twin_L01.txt: page_code_equals_twin=True, exit 0, expected_equals_output=True; twin alone under python -I -W error exit 0; run_labs LX2 PASS (7/7)."),
    row("LX2a-L01-lab1-hypothesis", "the hypothesis paragraph states the printed result", "course/modules/LX/LX2/L01.html:139", "PASS",
        f"Printed numbers (out_lab_L01_run.txt) and recomputed from its expected block by {S}r7_checks.py section 3: 10 states, 22 transitions, 0 leaving, "
        "10 of 10 reachable, 0 states with both duties, 0 sale-without-offer; sale 2, offer 4, R13 5, R15 2."),
    row("LX2a-L01-lab1-interpretation", "interpretation names only the printed checks", "course/modules/LX/LX2/L01.html:314", "PASS",
        "The paragraph names the two printed checks (no state carries both reporting duties; no state permits a sale without an offer), names the dependence on Assumption A1, and disclaims a finding about the statute or any filing."),
    row("LX2a-L01-prop4.1", "Proposition 4.1 (reachability) and its proof", "course/modules/LX/LX2/L01.html:320-329", "PASS",
        "The proof lists the ten states as (u,n), (u,l), (f,n), (f,l), (r,n), (r,l), (e,n), (e,l), (s,n), (s,l); each path uses arrows that are among the 22 printed transitions (out_lab_L01_run.txt). The lab prints 10 of 10 reachable. The statement is T and its hypothesis H1 lists the model."),
    row("LX2a-L01-prop4.2", "Proposition 4.2 (the reporting duties do not overlap) and its hypothesis", "course/modules/LX/LX2/L01.html:332-341", "PASS",
        "R13 requires listed and R15 requires not_listed (twin duty_13 at lines 88-90, duty_15d at lines 93-97). A state has one listing value, so no state satisfies both. Assumption A1 is not used (the proof needs only the listing requirement), as P3 states."),
    row("LX2a-L01-prop4.3", "Proposition 4.3 (a permitted sale implies a permitted offer) and its title", "course/modules/LX/LX2/L01.html:344-353", "PASS",
        "The title and conclusion match: sale_permitted holds only for effective (twin lines 105-107), and offer_permitted includes effective (twin lines 99-101). The printed table has sale yes only in the two effective rows, which have offer yes."),
    row("LX2a-L01-canon-breaks", "the seven limits in section 5 and their statute quotations", "course/modules/LX/LX2/L01.html:355-367", "PASS",
        "Seven limits (timing, exemptions, independence, emerging growth companies, proceedings, fiscal-year suspension, Assumption A1) match the quiz explanation (L01.html:588). Their quotations and paraphrases were checked (LX2a-L01-quotes-1933, -1934, -5d, -6e1-8e, -headings)."),
    row("LX2a-L01-misconceptions", "the four misconceptions and their corrections", "course/modules/LX/LX2/L01.html:369-389", "PASS",
        "Corrections cite 5(a) 'unless a registration statement is in effect' (FOUND), 8(a) (FOUND), 8(d) (FOUND, one fragment split by a footer), 6(a) and 12(b) (FOUND), 13(a) and 15(d)(1) 'if and so long as' (FOUND)."),
    row("LX2a-L01-problems", "the problem set: solutions agree with the lab output and the model", "course/modules/LX/LX2/L01.html:391-494", "PASS",
        "M1 (filed/not_listed offer yes, sale no; effective/not_listed offer yes, sale yes), M2 (stop_order rows: offer no, sale no, s15(d) yes), M3 (effective/listed R13 yes, R15 no; back to not_listed R15 yes) all match out_lab_L01_run.txt. P1 22 = 12 + 10. E1 2 of 10. E2: section 8 lines 10 (2 each of 8(b), 8(b), 8(a), 8(d), 8(d)), section 12 lines 10, section 6(a) 2, total 22 (counted in out_lab_L01_run.txt). E3, R1-R3 quotations FOUND or paraphrases of quoted text."),
    row("LX2a-L01-key-results", "key-results table: each row's grade and source", "course/modules/LX/LX2/L01.html:499-513", "PASS",
        "Ten rows: the statute rows are grade C with the section cited (5(c), 5(a), 8(a), 8(d), 12(a), 13(a), 15(d)(1)); the three model rows (Propositions 4.1-4.3) are grade T and proved in §4; the lab row is grade C naming Lab 1 and 'a check of the model'."),
    row("LX2a-L01-quiz", "retrieval quiz: each answer and explanation against the lesson text and the statute", "course/modules/LX/LX2/L01.html:517-600", "PASS",
        "Ten items: Q1 5(a) FOUND; Q2 5(c) FOUND, R5c answer; Q3 answer 2 (= E1); Q4 8(a) FOUND, answer 8(a); Q5 12(d) thirty days after receipt (answer 30); Q6 15(d)(1) third sentence, option wording matches comps1885.txt:11121; Q7 stop_order offer no (out_lab_L01_run.txt); Q8 22; Q9 seven limits, exemption option; Q10 Proposition 4.2 does not use A1."),
    row("LX2a-L01-references", "references section: keys cited on the page", "course/modules/LX/LX2/L01.html:602-606", "PASS",
        "grep this round: data-cite values on L01 are gpondsecurities and gpondsecuritiesb only; the page states no case and no commentary is cited, which matches."),
    row("LX2a-L01-dag", "concepts used on L01 are defined before use or linked to their owners; no out-of-closure concept used by name", "course/modules/LX/LX2/L01.html:37-38, :63; L01.html (whole page)", "PASS",
        "check_dag LX2 PASS (out_check_dag.txt). L01 links exchange-vs-otc (FC1), evidence-grade (P0.1) and quantifiers (M1) to concepts.html anchors, all in the closure {E1, FC1, M1, M2, P0.1}. Grep for the D1-D9 names of plan §4 in index, L01, L02 returns nothing."),
    row("LX2a-L01-hours", "lesson hours: data-hours 9 and the eyebrow", "course/modules/LX/LX2/L01.html:2, :34", "PASS",
        "L01.html:2 data-hours=\"9\"; L01.html:34 'LX2 · Lesson 1 of 4 · 9 study hours'; 9 x 4 = 36 at index.html:29."),
    row("LX2a-L01-paraphrase-locators", "statute statements in L01 that are paraphrases carry the right section locator",
        "course/modules/LX/LX2/L01.html:65-70, :80-85, :96-111, :362-363, :483", "PASS",
        "Paraphrases checked against the text: 2(a)(5) defines Commission (comps1884.txt:166); 6(c) fee clause under subsection (b); 8(b) refusal and amendment clauses; 8(d) notice and hearing; 12(d) certification and thirty days; 15(d)(1) third-sentence bank count; 5(d) communications; 8(e) examinations (all read this round in comps1884.txt and comps1885.txt, lines in the rows above)."),
    row("LX2a-L01-unspanned-readings", "sentences in L01 that are not claim spans are readings, not statute statements", "course/modules/LX/LX2/L01.html:51, :53, :69, :92, :96", "PASS",
        "The scope note (L01.html:53) says un-spanned sentences are readings of the quoted sections. The un-spanned sentences that carry a legal reading (for example L01.html:88 'A filed statement is not in effect') restate a span in the same paragraph; none states a holding."),
    row("LX2a-L02-structure", "lesson template order: why, core sections, lab, canon breaks, misconceptions, problems, key results, quiz",
        "course/modules/LX/LX2/L02.html:32-649", "PASS",
        "Read in full this round (lines 1-660; the page copy of the twin, lines 116-398, equals the twin by lab_twin_check). Header 32-40; grade legend 42-49; why-it-matters 51 (102 words); scope note 53; §1 55-61; §2 63-74; §3 76-93; §4 95-111; lab 113-425 inline after §4; canon breaks 427-437 (five limits); misconceptions 439-447 (four); problems 449-552 (three per tier, twelve solution blocks); key results 554-568 (eight rows); quiz 571-644 (nine items, all with explain); references 646-649."),
    row("LX2a-L02-opinion-quotes", "every quotation of Dirks and O'Hagan on L02 against the printed text, with the printed page",
        "course/modules/LX/LX2/L02.html:58-110, :424-431, :441-445, :482, :541-548, :617", "PASS",
        f"{S}out_quote_locate_L02.txt, with printed pages from the running head of each form-feed page ({S}r7_checks.py section 1). Every opinion quotation is FOUND at the page the claim cites, including: Dirks p. 651 n. 6 (operative 10(b) text); O'Hagan p. 651 ('does not extend beyond'); p. 663 n. 23 (scienter); O'Hagan p. 652 ('classical theory applies not only to officers'); Dirks p. 654 (two sentences); p. 655 (tippee sentence, 'Unlike insiders'); p. 660 ('Thus, a tippee assumes'); p. 659 (two); p. 657; p. 662 (two); p. 663 (benefit); p. 664 (two); O'Hagan p. 652 (misappropriation definition, 'In lieu of'); p. 654 ('Deception through nondisclosure'); p. 655 ('if the fiduciary discloses'); p. 656 (three); O'Hagan fn 7 at p. 655 n. 7. Two source sentences are not matched by the script, both checked by hand: the classical-theory sentence spans pp. 651-652 across a footer (ohagan.txt:485-497; the claim cites pp. 651-652) and footnote 5 at p. 653 uses '[his]' for O'Hagan's (ohagan.txt:576)."),
    row("LX2a-L02-n23-attribution", "footnote 23 of Dirks: scienter quotations", "course/modules/LX/LX2/L02.html:56, :431, :541, :617", "PASS",
        "dirks.txt:757-759: '23 Scienter—“a mental state embracing intent to deceive, manipulate, or defraud,” Ernst & Ernst v. Hochfelder ... —is an independent element of a Rule 10b-5 violation.' Printed page 663 (r7_checks §1). The quiz explanation's 'the text at p. 663 ... says scienter is relevant in some cases to whether the tipper has violated his duty' matches dirks.txt 'Scienter in some cases is relevant in determining whether the tipper has violated his Cady, Roberts duty', page 663."),
    row("LX2a-L02-title-h1", "lesson 2 title matches the hub card and the table row", "course/modules/LX/LX2/L02.html:35; index.html:151, :181", "PASS",
        "L02.html:35 'Insider trading and tipping' = index.html:151 card title and index.html:181 table row. The next-lesson link L02.html:654 reads 'Manipulation, Dodd–Frank and MiFID II' = L03.html h1."),
    row("LX2a-L02-lab-run", "Lab 1 (L02) runs and its page code and expected block match the twin", "course/modules/LX/LX2/L02.html:113-425; tests/labs/LX2/lab-LX2-L02-1.py", "PASS",
        "out_lab_twin_L02.txt: page_code_equals_twin=True, exit 0, expected_equals_output=True, 25 output lines; twin alone under python -I -W error exit 0; a second run is byte-identical (out_lab_L02_run.txt); run_labs LX2 PASS."),
    row("LX2a-L02-lab-output", "the printed decision table matches the rules in the twin and the page's claims about each pattern", "course/modules/LX/LX2/L02.html:399-423; twin lines 86-283", "PASS",
        "Printed rows (out_lab_L02_run.txt, = page lines 411-421): P1 fired pp. 651-652; P2 not fired, benefit none, p. 662; P3 fired p. 660; P4 fired p. 660; P5 not fired, knowledge, p. 660; P6 fired p. 652; P7 not fired, disclosure-to-source, p. 655; P8 not fired, duty, p. 652. The twin's classify() (lines 252-259) reproduces each row. Summary 'fired: P1, P3, P4, P6 (4 of 8)' (r7_checks §4)."),
    row("LX2a-L02-classical-element", "classical-branch check 'no public disclosure before the trade' and its citation", "course/modules/LX/LX2/L02.html:73, :459; twin lines 226-231, 40", "PASS",
        "Twin lines 226-231 check 'no public disclosure before the trade' against KEY_DIRKS at p. 654 (line 231); the M1 solution (L02.html:459) cites gpo1983dirks p. 654 for it; L02.html:73 cites gpo1997united pp. 651-652 for the classical branch as a whole, which matches the BRANCH_RULE entry at twin line 40."),
    row("LX2a-L02-hypothesis", "hypothesis paragraph states the printed decisions", "course/modules/LX/LX2/L02.html:115", "PASS",
        "The hypothesis names fired P1, P3, P4, P6 and unfired P2 (benefit), P5 (knowledge), P7 (disclosure-to-source), P8 (duty). Each matches the printed row (out_lab_L02_run.txt)."),
    row("LX2a-L02-example-3.2", "Example 3.2 (patterns P2 to P5) against the twin and the opinion", "course/modules/LX/LX2/L02.html:87-89, :92", "PASS",
        "P2 benefit none fails at p. 662 (twin NO_BENEFIT_LOCATOR, line 38; printed row). P3 pecuniary and P4 gift both fire, key gpo1983dirks, p. 660 (printed rows). P5 knowledge fails at p. 660 (printed row). Remark 3.3: the benefit test is p. 662 (FOUND) and the knowledge element is p. 660 (FOUND)."),
    row("LX2a-L02-example-2.2-4.2", "Example 2.2 (P1) and Example 4.2 (P6, P7) against the twin and the printed rows", "course/modules/LX/LX2/L02.html:72-74, :105-107", "PASS",
        "P1 fires the classical branch at pp. 651-652 (printed row; twin P1 flags material, nonpublic, traded, no public disclosure). P6 fires the misappropriation branch with key gpo1997united p. 652 (printed row). P7's disclosure element fails at p. 655 (printed row)."),
    row("LX2a-L02-canon-breaks", "the five limits in Section 5 and their citations", "course/modules/LX/LX2/L02.html:427-437", "PASS",
        "Five limits (scienter, materiality, benefit, misappropriation source, one trade per pattern). Scienter quotation FOUND at p. 663 n. 23; materiality quotation FOUND at p. 662; Dirks' objective facts at p. 664 (FOUND); O'Hagan footnote 7 at p. 655 n. 7 (FOUND). The limits match what Lab 1 does not model (twin docstring lines 20-23)."),
    row("LX2a-L02-interpretation", "the interpretation paragraph states only what the printed table shows", "course/modules/LX/LX2/L02.html:424", "PASS",
        "Printed counts (fired four, unfired four) match the paragraph. 'a question of fact' for benefit is FOUND at Dirks p. 664. The paragraph disclaims any statement about how a court would rule."),
    row("LX2a-L02-misconceptions", "the four misconceptions and their corrections", "course/modules/LX/LX2/L02.html:441-446", "PASS",
        "Corrections cite p. 654 (no duty from mere possession; 'disclose ... under § 10(b)' FOUND on p. 654, 'disclose or abstain' also on p. 654 by grep); p. 660 (tippee assumes duty only when breach and knowledge); p. 662 ('Absent some personal gain' FOUND p. 662); O'Hagan p. 652 and p. 653 n. 5 (O'Hagan 'was not an insider of Pillsbury', p. 653). These corrections are graded C and do not name the dissents; see LX2a-counter-evidence."),
    row("LX2a-L02-problems", "the problem set: solutions agree with the printed output and the twin", "course/modules/LX/LX2/L02.html:449-553", "PASS",
        "M1 four checks and locators match the twin (lines 226-231) and the printed row. M2: P6 and P7 differ only in source_told_of_trade (twin lines 170-203). M3 (P3 benefit none): run this round, not fired, element 'fails: tipper's personal benefit (none)', p. 662 (out_scratch_e2_e3.txt). Pr2 matches classify() lines 252-259. Pr3 cites p. 660 (twin line 239). E1 matches the printed table. E2 and E3 predictions: see LX2a-L02-E2-E3-scratch. R1-R3 quotations FOUND at p. 662, p. 663, p. 664, p. 656. Pr1 is handled by LX2a-L02-pr1-A2."),
    row("LX2a-L02-pr1-A2", "Pr1 proof: hypotheses, assumption, and the logic of the tippee argument", "course/modules/LX/LX2/L02.html:482, :484", "FAIL",
        "Pr1 invokes 'Assumption A1 of this lesson' (L02.html:482) and the solution cites 'Assumption A1 of this lesson, as stated in the problem' (L02.html:484). "
        "Grep this round: 'Assumption' and 'A1' appear in L02.html only on lines 482 and 484. The lesson body (§1-§4, Lab 1, canon breaks) declares no numbered Assumption, so "
        "the assumption that a value of none means no direct or indirect personal benefit exists only inside an exercise. Plan §2.1 item 6 and BLUEPRINT practice require "
        "every Definition that depends on a condition to list its numbered Assumptions; L01 does so (L01.html:132-134, Assumption A1). The proof itself is valid: H1 (p. 660), H2 "
        "(p. 662, FOUND) and H3 (p. 662, FOUND) are quoted correctly and only the necessity direction is used.",
        "Declare the assumption in the lesson body as a numbered block, for example 'Assumption A1 (not read from the opinion): a value of none for the tipper's benefit means the insider received no direct or indirect personal benefit', placed in §3 after Definition 3.1 where the tippee test is stated. Then cite it from Pr1 as 'Assumption A1 of §3' and leave the proof unchanged."),
    row("LX2a-L02-markup", "claim-span markup on L02 and the keys used", "course/modules/LX/LX2/L02.html:53, :84, :92, :541, :548, :599, :608, :617", "PASS",
        f"{S}out_span_attr_and_xref.txt: 59 claim spans, none lacking data-grade, data-cite or data-locator; keys gpo1983dirks and gpo1997united only; both in the registry. Grades C throughout (the page has no T claims on the opinions)."),
    row("LX2a-L02-E2-E3-scratch", "the scratch predictions in problems E2 and E3 (run on a copy, never the repo)", "course/modules/LX/LX2/L02.html:513-525", "PASS",
        f"{S}scratch_e2_e3.py ran two modified copies outside the repository under python -I -W error (out_scratch_e2_e3.txt). E2 (P2 benefit reputational): P2 fired, p. 660, 'fired: P1, P2, P3, P4, P6 (5 of 8)', as predicted. E3 (P7 source-told false): P7 fired, p. 652, 'fired: P1, P3, P4, P6, P7 (5 of 8)', as predicted."),
    row("LX2a-L02-key-results", "key-results table rows, grades and sources", "course/modules/LX/LX2/L02.html:557-567", "PASS",
        "Eight rows, each grade C with its key and printed page: pp. 651-652, p. 654, p. 660, pp. 662-663, p. 664, pp. 652, 655, 656, p. 663 n. 23 and Lab 1. Locators verified in LX2a-L02-opinion-quotes and LX2a-L02-page-locators. The counter-evidence omission in these grade-C rows is recorded in LX2a-counter-evidence."),
    row("LX2a-L02-quiz", "retrieval quiz: each answer and explanation against the opinions and the lab", "course/modules/LX/LX2/L02.html:574-643", "PASS",
        "Nine items. Q1 classical theory: pp. 651-652 and p. 652 (temporary fiduciaries, FOUND). Q2 'only when' at p. 660 (FOUND); payment is one form of benefit, reputational benefit at p. 663. Q3 p. 662 (FOUND). Q4 p. 655 (FOUND). Q5 p. 663 n. 23 (FOUND); p. 663 text (dirks.txt). Q6 P4 (printed row). Q7 4 of 8 (printed). Q8 P6, P7, P8 outsiders (twin). Q9 P5 only (printed)."),
    row("LX2a-L02-dag", "concepts used on L02 are defined before use or linked to their owners", "course/modules/LX/LX2/L02.html:37, :56, :66, :80, :98", "PASS",
        "check_dag LX2 PASS. L02 links only exchange-act-1934 (L01.html#def-exchange-act-1934, defined at L01.html:96). It defines insider-trading-doctrine (:66), tipper-tippee-liability (:80) and misappropriation-theory (:98), each once in course/. Grep for the D1-D9 names returns nothing on L02."),
    row("LX2a-L02-B3-B1", "no statement about Texas Gulf Sulphur, Dodd-Frank or MiFID II content on L02 (the unadmitted sources)", "course/modules/LX/LX2/L02.html (whole page); index.html:171; L02.html:654", "PASS",
        f"grep this round: no 'Texas', 'Gulf' or 'Sulphur' on L01.html or L02.html. 'Dodd' and 'MiFID' occur on L02 only in the next-lesson link text (L02.html:654). The registry has no key or source string for either instrument ({S}r7_checks.py §6, empty match list), and index.html:171 says so."),
    row("LX2a-L02-years", "no year is printed for a case whose registry record disagrees (Dirks N1)", "course/modules/LX/LX2/L02.html (prose)", "PASS",
        "grep this round: the only four-digit year in L02 prose is 1934 (L02.html:37, :56, the name of the Act). No year is printed for Dirks or O'Hagan. The registry Dirks record is inconsistent (title '(1982)', year 1983); the GovInfo details page reads 'Court Term 1982' and the decision date 'July 1, 1983' (out_r7_checks)."),
    row("LX2a-L02-why", "the why-it-matters claims are attributed to the opinions with locators", "course/modules/LX/LX2/L02.html:51", "PASS",
        "Claim 1 (no violation in itself from information others lack): Dirks p. 654 and O'Hagan p. 652 locators; the paraphrase matches Dirks p. 654 ('does not arise from the mere possession'). Claim 2 (three sources of duty): Dirks pp. 654, 660 and O'Hagan p. 652 locators, which match the three tests in §2-§4."),
    row("LX2a-L02-tippee-definition", "the unsourced tippee definition removed in the delta", "course/modules/LX/LX2/L02.html:77", "PASS",
        "L02.html:77 now reads 'Dirks states the difference between an insider and a tippee: “Unlike insiders who have independent fiduciary duties ...”' with locator p. 655 (FOUND at p. 655). No unsourced definition remains in that paragraph."),
    row("LX2a-L02-page-locators", "every printed page locator on L02 (Dirks and O'Hagan) agrees with the printed page of the source",
        "course/modules/LX/LX2/L02.html (all claim-span locators and the decision rows of the table)", "PASS",
        f"Page map from the running heads ({S}r7_checks.py §1; {S}out_quote_locate_L02.txt). Checked: 'Scienter in some cases' p. 663; 'Thus, a tippee assumes' p. 660 (syllabus p. 647 excluded); 'Absent some personal gain' p. 662; 'Determining whether an insider' p. 664; 'does not extend beyond' p. 651; 'classical theory applies not only' p. 652; 'Deception through nondisclosure' p. 654; 'if the fiduciary discloses' p. 655; 'uses the information to purchase' p. 656 (also p. 682, the dissent, not cited); 'does not catch all conceivable' p. 656; footnote 7 'may still be liable' p. 655 n. 7; fn 5 at p. 653. Syllabus pages (647, 643) are never cited."),
    row("LX2a-L02-scienter-composite", "composite sentence quoting two fragments of footnote 23 across an omitted citation", "course/modules/LX/LX2/L02.html:431", "PASS",
        "L02.html:431 quotes 'a mental state embracing intent to deceive, manipulate, or defraud' and 'an independent element of a Rule 10b-5 violation' from dirks.txt:757-759, omitting the Ernst & Ernst citation between them without an ellipsis. Both fragments are exact (FOUND p. 663). Whether a citation may be dropped silently is a style question the repository does not state (BUILDER_RULES and BLUEPRINT are silent), so it is ungraded here."),
    row("LX2a-scope-note", "every lesson and the hub state the educational reading, not legal advice", "course/modules/LX/LX2/index.html (lede), L01.html:53, L02.html:53", "PASS",
        "index.html:33 'The module is an educational reading of cited sources. It is not legal advice.'; L01.html:53 and L02.html:53 state the same; the footers of all three pages carry the same line."),
    row("LX2a-notation", "notation: every symbol and macro used on slice-a pages against notation/notation.json; no reuse with another meaning",
        "course/modules/LX/LX2/L01.html:115-352 (math and labels); L02.html (whole page); index.html (placement math)", "PASS",
        f"Macros on the pages: L01 uses \\blacksquare three times (proof-end marks, L01.html:328, :340, :352); index uses \\(x\\), \\(S\\), \\(P(x)\\), \\(f(x,y)\\), \\(\\partial\\), \\(H\\) in placement items; L02 uses no macros. The placement symbols x, S, P, f, y are not registered in notation/notation.json (grep: no matching key, out_span_attr_and_xref.txt), so nothing is reused with another meaning. \\blacksquare is not in notation.json, but course/assets/css/course.css:872 renders the proof-end mark ∎ and 117 course pages use it (grep this round); recorded as a registry flag, not a row failure."),
    row("LX2a-L01-section-locators", "subsection and sentence locators used on L01 (new this round)", "course/modules/LX/LX2/L01.html:51-111, :359-365, :483", "PASS",
        "Confirmed each subsection letter against the compilation text: 5(a), 5(c), 5(d) '(d) LIMITATION' (comps1884.txt:1388), 6(a), 6(c), 6(e)(1) (comps1884.txt:1553), 8(a), 8(b) (comps1884.txt:1768), 8(d) (1788), 8(e) (1811), 12(a), 12(b), 12(d) (comps1885.txt:7100-7113), 13(a), 15(d)(1) second and third sentences (comps1885.txt:11114-11124), and 2(a)(5) (comps1884.txt:166). 'in effect' does not occur in section 2 (comps1884.txt:34-391)."),
    row("LX2a-L02-M3-scratch", "M3 prediction: P3 with benefit none (new this round)", "course/modules/LX/LX2/L02.html:469-475", "PASS",
        "Run this round on a scratch copy (out_scratch_e2_e3.txt): P3 not fired, element 'fails: tipper's personal benefit (none)', key gpo1983dirks, p. 662, as M3 states. Fired set becomes P1, P4, P6 (3 of 8); the solution does not claim a count."),
    row("LX2a-registry-keys", "every registry key cited by slice a exists, and the keys the slice reads as unregistered are absent (new this round)", "references/references.json; course/modules/LX/LX2/index.html:195-200; L01.html; L02.html", "PASS",
        f"{S}r7_checks.py §6: gpondsecurities, gpondsecuritiesb, gpo1983dirks, gpo1997united, cfandcode, frb2026fed present; grep for dodd, mifid, texas, gulf, sulphur returns nothing. verify_refs offline 560 entries, 0 problems."),
    row("LX2a-counter-evidence", "BUILDER_RULES 1.5 and VERIFIER 2.3: a C-graded claim names published counter-evidence where it exists (new this round)",
        "course/modules/LX/LX2/L02.html:66-70, :80-85, :98-103 and key-results rows :559-564", "FAIL",
        "The doctrine claims are graded C and stated as the majority's tests, with no mention of a dissent in the same published opinion that disputes the same test. "
        "Dirks: 'Justice Blackmun ... dissenting' begins at printed p. 667 (dirks.txt, r7_checks §1b); its position on the tippee test is read and stated by the builder; L02 states the p. 660 and p. 662 tests without naming it. "
        "O'Hagan: Thomas, J., 'concurring in the judgment in part and dissenting in part', begins at p. 679 and criticises the misappropriation theory at p. 680 (ohagan.txt: 'misappropriation theory fails to provide a coherent and con-', hyphenated in the source). "
        "L02.html:98-103 states 'The misappropriation theory holds ...' as C without naming either. The scope of insider-trading liability is the plan's named contested claim (plan §11 item 2).",
        "For each C-graded span on the tippee and misappropriation tests (L02.html:80-85, :98-103) and each key-results row for them (:561-564), add the dissent with its key, first printed page and the position it takes, read from the page: Dirks, Blackmun, J., dissenting, from p. 667 (gpo1983dirks); O'Hagan, Thomas, J., concurring in part and dissenting in part, p. 679 and p. 680 (gpo1997united). Or grade those spans as the majority opinion's statement and name the dissent beside them. The builder reads the dissent before stating its position."),
    row("LX2a-lab-assumptions", "plan 2.1 item 6: every model result in the labs lists its numbered Assumptions (new this round)",
        "course/modules/LX/LX2/L02.html:113-115, :424; tests/labs/LX2/lab-LX2-L02-1.py:6-23", "FAIL",
        "Lab 1 is a rule-based model whose results depend on readings the lesson does not list: a value of none for the tipper's benefit means no personal benefit (the P2 row rests on it), the stated facts are taken as true (the lab reads them and does not assess them, twin docstring lines 20-23), and the classical branch treats a temporary fiduciary as an issuer_insider role (L02.html:69). The page states the hypothesis 'under the rules as coded' with no numbered Assumptions block before the lab. The only A1 on the page is the one inside Pr1 (see LX2a-L02-pr1-A2). L01's lab has its A1 block (L01.html:132-134); L02's does not.",
        "Before Lab 1 (L02.html:113), add a numbered Assumptions list, for example A1 (none means no direct or indirect personal benefit), A2 (the pattern's stated facts are true and are read, not assessed), A3 (a temporary fiduciary is stated in the pattern with the role issuer_insider, L02.html:69). Cite A1 from the hypothesis and the interpretation paragraph (L02.html:424), and from Pr1."),
]


def main() -> int:
    root, out = sys.argv[1], sys.argv[2]
    ids = [r["id"] for r in ROWS]
    if len(ids) != len(set(ids)):
        raise SystemExit("duplicate row id")
    fails = [r["id"] for r in ROWS if r["status"] != "PASS"]
    counts = {s: sum(1 for r in ROWS if r["status"] == s) for s in ("PASS", "FAIL", "UNVERIFIABLE")}
    prev = json.load(open("/Users/billyribeiro/.fanout/frags/E-LX2-a.round6.json", encoding="utf-8"))
    missing = [r["id"] for r in prev["rows"] if r["id"] not in ids]
    if missing:
        raise SystemExit(f"round-6 row ids not kept: {missing}")
    fragment = {
        "unit": "LX2",
        "slice": "LX2-a",
        "round": 7,
        "verifier": "Haiku independent verifier, LX2-a round 7 (did not build LX2; builder ledgers and scratch not read; round-6 fragment read as context only; no round-6 PASS row was carried, every row was re-checked this round)",
        "pin": "06994db16d1ab449bcf29898a7f56cfa999dce57",
        "base": "4bd8cb94 (round-6 pin). git diff 4bd8cb94 06994db over slice a: index.html, L01.html, L02.html, tests/labs/LX2/lab-LX2-L01-1.py and lab-LX2-L02-1.py are byte-identical (git diff --quiet). Shared inputs tools/, references/, notation/, curriculum/, atlas/, course/assets/ show no change in that range. Changed outside slice a: LX2 cards.json and project.html, LX1, E4, BK4, PC3, SC1 pages and twins, plans/FINAL-ARCHITECT-RULINGS.md (ruling 12, L08 concept; not a slice input).",
        "checkout": root,
        "scratch": "/tmp/lx2a_r7_dl (four primary sources re-fetched by plain curl through ledgers/LX2/scripts/LX2-a-r7/fetch_sources.sh); /tmp/lx2a_r7_scratch (scratch copies of the L02 twin for E2, E3, M3; nothing written into the repository)",
        "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "verdict": "PASS" if not fails else "FAIL",
        "rows": ROWS,
        "mutants": [],
        "registry_flags": [
            "references/references.json key gpo1983dirks: title field reads 'Dirks v. SEC, 463 U.S. 646 (1982)' and year field reads 1983 (references.json:10823-10835). GovInfo USREPORTS-463-646 details: Court Term 1982, decided July 1, 1983. No slice-a page prints a year for Dirks. The architect corrects the record through add_reference.py.",
            "notation/notation.json does not register \\blacksquare, the proof-end mark used on L01.html (three uses) and on 117 course pages; course/assets/css/course.css:872 renders it as ∎. The architect decides whether to register it.",
            "No registry key or source string exists for Dodd–Frank, MiFID II or Texas Gulf Sulphur (grep, references/references.json). L02 and the hub already say so; the REFERENCE_REQUESTS stay open.",
        ],
        "freshness_flags": [],
        "notes": (
            f"Round 7 at pin 06994db1. Every row was re-checked this round; no round-6 PASS row was carried, because the round-6 fragment is context only. All round-6 row ids are kept (86 rows) and new ids were added (5). "
            f"Fails: LX2a-L02-pr1-A2 (Assumption A1 referenced as 'of this lesson' but never declared in the lesson body), LX2a-lab-assumptions (Lab 1 has no numbered Assumptions block, plan 2.1 item 6), and LX2a-counter-evidence (grade-C doctrine claims omit the Dirks and O'Hagan dissents that dispute the same tests, BUILDER_RULES 1.5 and VERIFIER 2.3). "
            f"Scripts: {S} (fetch_sources.sh, quote_locate.py, lab_twin_check.py, scratch_e2_e3.py, r7_checks.py, write_fragment.py, and the out_* files). "
            "Labs are demonstrations, so no mutants are required for this slice (VERIFIER 2.6 applies to project graders only). The statute and opinion texts were re-fetched; the PDFs and pdftotext files hash identical to round 6, while the GovInfo details HTML pages are dynamic and differ in hash, so their fields were read from the current pages. "
            "Not checked by this slice: L03, L04, project.html and cards.json (other slices); the full tests/ suite (the relevant modules were run); the quiet-machine timing of page_smoke (the tool's own timings were recorded as printed); the content of the Dirks and O'Hagan dissents beyond their location and position (the builder reads them when fixing LX2a-counter-evidence); a style standard for omitting citations within quoted sentences (none is in the repository)."
        ),
        "summary": f"Slice LX2-a round 7 verdict {'PASS' if not fails else 'FAIL'} at 06994db1. {len(ROWS)} rows: PASS {counts['PASS']}, FAIL {counts['FAIL']}, UNVERIFIABLE {counts['UNVERIFIABLE']}. Mutants: none (slice a is not a project grader). Failing rows: {', '.join(fails)}.",
    }
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(fragment, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    print(json.dumps({"rows": len(ROWS), "counts": counts, "verdict": fragment["verdict"], "fails": fails}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
