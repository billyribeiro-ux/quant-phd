"""Write ledgers/LX2/LX2-a.json (round 10) from the rows verified and recorded in this round.

Every row cites the script output or the file:line it was checked against. Run from the checkout root:
    python3 -I ledgers/LX2/scripts/LX2-a-r10/write_fragment_r10.py
"""
import json
import pathlib
from datetime import UTC, datetime

ROOT = pathlib.Path(__file__).resolve().parents[4]
R = "ledgers/LX2/scripts/LX2-a-r10/"
rows: list[dict[str, str]] = []


def row(rid: str, check: str, location: str, evidence: str, status: str = "PASS", fix: str | None = None) -> None:
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        assert fix, rid
        r["fix"] = fix
    rows.append(r)


# ---- commands (re-run this round at 00a84795) ----
row("LX2a-cmd-check_pages", "2.9 structure; tools/check_pages.py --unit LX2",
    "index, L01, L02",
    f"Run r10: `check_pages LX2: PASS`, exit 0 ({R}out_check_pages_r10.txt).")
row("LX2a-cmd-check_dag", "2.9 DAG; tools/check_dag.py --unit LX2", "L01, L02, index",
    f"Run r10: `check_dag LX2: PASS`, exit 0 ({R}out_check_dag_r10.txt). Unlinked uses of D1-D9 names grepped in index.html, L01.html, L02.html: none (grep, this round).")
row("LX2a-cmd-run_labs", "2.5 labs; tools/run_labs.py --unit LX2", "tests/labs/LX2/*.py",
    f"Run r10: `run_labs LX2: PASS (7/7)`, exit 0 ({R}out_run_labs_unit_r10.txt).")
row("LX2a-lab-isolated", "2.5 labs; twin alone under python -I -W error; page code equals twin; expected block equals output",
    "course/modules/LX/LX2/L01.html:137-315 with tests/labs/LX2/lab-LX2-L01-1.py; L02.html:127-439 with tests/labs/LX2/lab-LX2-L02-1.py",
    f"Run r10: twin_isolated_r10.sh: lab-LX2-L01-1 exit=0 stderr_bytes=0 stdout_lines=39; lab-LX2-L02-1 exit=0 stderr_bytes=0 stdout_lines=25 ({R}out_twin_isolated_r10.txt). lab_twin_check_r10.py: page_code_equals_twin=True and expected_equals_output=True for both labs ({R}out_lab_twin_r10.txt).")
row("LX2a-cmd-page_smoke", "2.9 page_smoke; tools/page_smoke.py --unit LX2 --pages <page> (each run alone)",
    "index, L01, L02",
    f"Run r10, one page per run: `page_smoke LX2: PASS`, exit 0 for index ({R}out_page_smoke_index_r10.txt), L01 ({R}out_page_smoke_L01_r10.txt), L02 ({R}out_page_smoke_L02_r10.txt).")
row("LX2a-cmd-ruff-mypy", "2.5 lint and types on the slice-a twins",
    "tests/labs/LX2/lab-LX2-L01-1.py, tests/labs/LX2/lab-LX2-L02-1.py",
    f"Run r10: `ruff check tests/labs/LX2`: All checks passed; `ruff format --check`: 7 files already formatted; `mypy --no-incremental tests/labs/LX2`: Success, no issues in 7 source files ({R}out_ruff_r10.txt, {R}out_mypy_r10.txt).")
row("LX2a-cmd-pytest", "tooling tests relevant to labs and page checks", "tests/",
    f"Run r10: `pytest tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py -q`: 100%, exit 0 ({R}out_pytest_r10.txt).")
row("LX2a-cmd-verify_refs", "2.1 citations; tools/verify_refs.py --offline and --unit LX2",
    "references/references.json (LX2 keys gpondsecurities, gpondsecuritiesb, gpo1983dirks, gpo1997united, cfandcode, frb2026fed)",
    f"Run r10: `verify_refs.py --offline`: offline integrity: 560 entries, 0 problems ({R}out_verify_refs_offline_r10.txt). `verify_refs.py --unit LX2` (live): 6 of 560 entries, 0 problems ({R}out_verify_refs_live_LX2_r10.txt). Each of the six keys has one record in references.json (grep -c, this round).")
row("LX2a-cmd-coursekit-closure", "2.9 DAG; prerequisite closure of LX2 recomputed", "course/modules/LX/LX2/index.html:35, :62",
    f"Run r10: coursekit.prerequisite_closure('LX2') = ['E1', 'FC1', 'M1', 'M2', 'P0.1'] ({R}out_closure_r10.txt); matches index.html:62 exactly.")
row("LX2a-quote-search", "2.1 attribution: every curly-quoted passage searched in its primary text",
    "course/modules/LX/LX2/L02.html:109 (Thomas dissent); L01.html and L02.html (all others)",
    f"Run r10: quotecheck_ci_r10.py (case-insensitive, whitespace-free fallback) over L01.html against comps1884.txt and comps1885.txt ({R}out_quotecheck_ci_L01_r10.txt): 56 OK. Non-OK lines were examined one by one: the 1934 title is an exact match in COMPS-1885_details.html:458 (python check, both titles True, this round); the 8(b) and 8(d) quotations (L01.html:84-85) are interrupted by a page header in comps1884.txt:1796-1809 and found in full; the remaining non-OK lines are misconception quotations and a lab output quotation, not statute text. Over L02.html, quotecheck_ci_r10.py ({R}out_quotecheck_ci_L02_r10.txt) and loccheck_r10.py ({R}out_loccheck_L02_r10.txt) located 58 quotations on the printed page inside the locator set, except four checked by hand against the opinions' text (pdftotext of USREPORTS-521-642.pdf pdf page 10 (p. 651), pdf page 11 (p. 652), pdf page 14 (p. 655), and USREPORTS-463-646.pdf pdf page 9 (p. 654)): each is printed on the cited page.")
row("LX2a-IDX-hours", "2.9 hours: hub split and lesson hours", "course/modules/LX/LX2/index.html:29, :41-44, :176-186; L01.html:2, :34; L02.html:2, :34",
    "index.html:29 data-hours-lessons=36 and data-hours-project=14; :42 widths 72% and 28% (36/50 and 14/50); :44 '36 h lessons · 14 h project (28% of 50 h)'; :180-186 table 9+9+9+9=36, 14, total 50. L01.html:2 data-hours=9 and :34 '9 study hours'; L02.html:2 and :34 likewise. Curriculum figure 50 (curriculum/06-profession-capstone.yaml:53, read in plans/LX2-build-plan.md §0.1).")
row("LX2a-IDX-structure", "2.9 structure: hub elements (BUILDER_RULES §4.1)", "course/modules/LX/LX2/index.html:1-207",
    "Read in full this round. Hub elements present: objectives (:47-58, six items; 4-8 required), prerequisite links (:60-71), placement diagnostic (:73-144), lesson map (:146-155), project ladder (:157-166), data status (:168-172), hours (:174-189), reading list (:191-202). Lesson sections of L01 and L02 follow BUILDER_RULES §4.2 (why it matters at 119 and 102 words, both within 120; core sections; labs inline; canon breaks §5; misconceptions §6 with 4 each; problem tiers with 3 problems each; key results §8; quiz §9 with 10 and 9 items, each with an explanation).")
row("LX2a-IDX-closure", "2.9 DAG; hub statement of the closure", "course/modules/LX/LX2/index.html:35, :62",
    "index.html:62 reads {E1, FC1, M1, M2, P0.1}; the recomputed closure is the same set ({R}out_closure_r10.txt).")
row("LX2a-IDX-FC1-title", "2.9 hub prerequisite title", "course/modules/LX/LX2/index.html:35",
    "index.html:35 'FC1 The Financial System, Markets & Instruments' = curriculum/02-economics-finance-core.yaml:364 title 'The Financial System, Markets & Instruments'.")
row("LX2a-IDX-SR4", "2.9 hub unlock claim", "course/modules/LX/LX2/index.html:39",
    "index.html:39 'SR4 Regulation's Market Footprint, which lists LX2 among its prerequisites'. curriculum/05-macro-alternatives.yaml:505 'id: SR4', :506 title \"Regulation's Market Footprint\", :509 prereqs [SR1, FI4, LX2].")
row("LX2a-IDX-lede-markup", "2.9 structure and prose: lede and markup", "course/modules/LX/LX2/index.html:33; L01.html:51, :59-65; L02.html:51-110",
    "index.html:33 lede read in full (changed sentence: 'a statement the module cannot source is marked not stated here or left out'). Markup of the claim spans and page-head checked by check_pages PASS and page_smoke PASS. No change to L01.html:51-65 except the :65 finding recorded in LX2a-L01-amended.")
row("LX2a-IDX-objectives-1-3", "2.9 hub objectives match the lessons", "course/modules/LX/LX2/index.html:51-53; L01.html:55-130; L02.html:55-111, :113-425",
    "Objective 1 (quote filing, effectiveness, stop-order and reporting sentences; L01 §2-§3, quoted at L01.html:80-106); objective 2 (trace statuses; L01 §4, the state table at lab output lines 279-288); objective 3 (classify under the elements; L02 Lab 1 table at 425-432 names the deciding element).")
row("LX2a-IDX-placement-arith", "2.2 numbers: placement diagnostic arithmetic", "course/modules/LX/LX2/index.html:95-141",
    "Recomputed: 100/1.1 = 90.909..., to two places 90.91 (item tolerance 0.01 accepts it). 6/8 = 0.75. Differences 10-11 = -1, 12-13 = -1, 9-8 = 1, sum -1, bias -1/3 = -0.3333 (tolerance 0.001). Items: ten `li.item` at index.html:77, 86, 95, 100, 109, 114, 119, 128, 133, 138; eight prerequisite and two skill (data-skill at :133 and :138). 7 of 10 = 70% < 80% as :75 states.")
row("LX2a-IDX-placement-items-1-8", "2.9 placement items and keys", "course/modules/LX/LX2/index.html:77-131",
    "Items 1-8 keys checked: T for a proved result (:80); the equilibria before and after a change (:90); PV 90.91 (:95-98); negation is an existential statement (:104); d/dx x^2 = 2x = 6 at 3 (:109-112); partial derivative 2xy = 12 at (2,3) (:114-117); OTC market (:122); spread 100.10 - 99.50 = 0.60 (:128-131). All keys match their explanations.")
row("LX2a-IDX-placement-cross-ref", "2.9 cross-reference from the hub to Lesson 4", "course/modules/LX/LX2/index.html:136; course/modules/LX/LX2/L04.html:114, :118",
    "index.html:136 says Lesson 4 defines the hit rate for the project's model case. L04.html:118 defines hit rate = (1/H) sum h_t and bias = (1/H) sum e_t, with e_t the forecast error (L04.html:114: forecast minus realised). The hub's bias (:139-141, forecast minus realised) uses the same sign.")
row("LX2a-IDX-skill-items", "2.9 skill checks for rungs 1 and 2", "course/modules/LX/LX2/index.html:133, :138",
    "index.html:133 (rung 1: 6 hits of 8 pairs, 0.75) and :138 (rung 2: bias -0.3333) are the skill checks (data-skill); their explanations at :136 and :141 give the same values as recomputed.")
row("LX2a-IDX-concept-anchors", "2.9 concept anchors resolve", "course/modules/LX/LX2/index.html:35, :64-68; L01.html:37-38, :63; L02.html:37, :56",
    "All eleven hub concept ids resolve in course/concepts.html: exchange-vs-otc (:478), limit-order-book (:481), order-types (:484), bid-ask-spread (:476), quantifiers (:78), present-value (:75), derivative (:120), partial-derivative (:129), comparative-statics (:302), evidence-grade (:39), project-ladder (:40). L01.html:37 and L02.html:37 link to the same ids or to L01.html#def-exchange-act-1934 (L01.html:96).")
row("LX2a-IDX-data-status", "2.8 data status statement", "course/modules/LX/LX2/index.html:170-171; L02.html:72, :87, :115, :118",
    "index.html:170 names HYPOTHETICAL (eight patterns, L02) and SIMULATED (L03, L04, project) inputs; L02.html:72 labels Example 2.2 'HYPOTHETICAL'; index.html:171 says the Dodd-Frank and MiFID II texts are not in the registry (grep of references.json for dodd, frank, mifid: 0 matches this round).")
row("LX2a-IDX-core-reading", "2.1 reading list cites registry keys only", "course/modules/LX/LX2/index.html:195-200",
    "index.html:195-200 lists gpondsecurities, gpondsecuritiesb, gpo1983dirks, gpo1997united, cfandcode, frb2026fed; each key occurs once in references/references.json (grep, this round).")
row("LX2a-IDX-banned", "2.9 banned phrases (BUILDER_RULES 1.3-1.4)", "course/modules/LX/LX2/index.html; L01.html; L02.html",
    f"check_pages LX2 PASS ({R}out_check_pages_r10.txt). Grep, this round, of index.html, L01.html and L02.html for TODO, TBD, lorem, clearly, obviously, 'it is important to note', 'studies show', 'experts agree', 'it is well known', 'for brevity', 'beyond the scope', 'left as an exercise', 'you can add more' and '...': no match outside code (the only 'debate' is the metadata 'Debate brief: none' at index.html:38).")
row("LX2a-IDX-cards-title", "2.9 lesson titles in the hub match each lesson h1", "course/modules/LX/LX2/index.html:150-153, :181; L01.html:35; L02.html:35; L03.html; L04.html",
    "h1 values: L01 'Registration, Disclosure and the Two Acts' (L01.html:35) = index.html:150; L02 'Insider trading and tipping' (L02.html:35) = index.html:151; L03 'Manipulation, Dodd–Frank and MiFID II' = index.html:152; L04 'Fiduciary Duty, Conflicts and Model-Risk Governance' = index.html:153 (grep of the four h1 elements, this round).")
row("LX2a-IDX-concept-link-hub-text", "2.9 hub text about concept links", "course/modules/LX/LX2/index.html:33, :62, :75, :170-171",
    "index.html:62 says prerequisite concepts link to the concept index and concepts of an earlier LX2 lesson link to that lesson; the links resolve (concept anchors and L01.html#def-; links check below). index.html:75 says P0.1 is not released; concepts.html carries 'not yet released' on 806 lines, including evidence-grade (:39) and project-ladder (:40).")
row("LX2a-L01-title-1933-1934", "2.1 attribution: titles of the two Acts", "L01.html:59, :61",
    "Both title quotations equal the GovInfo title fields: COMPS-1884_details.html (python, tags stripped, exact match True) and COMPS-1885_details.html:458 (exact match True), this round.")
row("LX2a-L01-amended", "2.1 attribution and 2.9 prose: amendment dates and the list of section numbers used in the lesson",
    "L01.html:65, :69",
    "The amendment dates match the statute headers: comps1884.txt 'As Amended Through P.L. 119-27, Enacted July 18, 2025'; comps1885.txt 'As Amended Through P.L. 119-60, Enacted December 18, 2025'. FAIL: the same sentence says 'The section numbers in this lesson are those printed ...: sections 2(a)(5), 3, 4, 5, 6 and 8 of the 1933 Act (with 5(d), 6(e)(1) and 8(e) in §5)', but L01.html:362 (the emerging-growth bullet added this round) cites section 2(a)(19) of the 1933 Act, which the list omits. The enumerative sentence is therefore false as written.",
    status="FAIL",
    fix="In L01.html:65 change 'sections 2(a)(5), 3, 4, 5, 6 and 8 of the 1933 Act' to 'sections 2(a)(5) and 2(a)(19), 3, 4, 5, 6 and 8 of the 1933 Act'. Nothing else in the sentence changes. Re-run check_pages LX2 and page_smoke for L01.")
row("LX2a-L01-quotes-1933", "2.1 attribution: 1933 Act quotations and paraphrases", "L01.html:69-70, :80-85, :88",
    "Read against comps1884.txt: 6(a) 'by filing a registration statement' (sentence located); 6(c) 'shall be deemed to have taken place upon the receipt thereof' and 'shall not be deemed to have taken place unless it is accompanied' with 'the fee required under subsection (b)' (comps1884.txt, 6(c)); 5(a) 'Unless a registration statement is in effect as to a security, it shall be unlawful' (located); 5(c) 'unless a registration statement has been filed as to such security, or while ... any public proceeding or examination under section 8' (located); 8(a) (located); 8(b) 'within ten days after such notice' and 'not later than ten days after the filing' (comps1884.txt:1766-1775, read in full, matches L01.html:84); 8(d) 'issue a stop order suspending the effectiveness of the registration statement' and 'the stop order shall cease to be effective' (comps1884.txt:1796-1810, page header between the words only).")
row("LX2a-L01-quotes-1934", "2.1 attribution: 1934 Act quotations and paraphrases", "L01.html:100-111",
    "Read against comps1885.txt: 12(a) 'to effect any transaction in any security (other than an exempted security) on a national securities exchange unless a registration is effective as to such security for such exchange' (located); 12(b) (located); 12(d) 'thirty days after the receipt of such certification by the Commission or within such shorter period' (located); 12(d) second sentence 'may be withdrawn or stricken from listing and registration in accordance with the rules of the exchange' and 'relieved from further compliance with the provisions of this section and section 13' (located); 13(a) (located); 15(d)(1) first sentence 'which has become effective pursuant to the Securities Act of 1933, as amended' (located); second sentence 'automatically suspended if and so long as any issue ... is registered pursuant to section 12' (located); third sentence 'held of record by less than 300 persons' and, for a bank, a savings and loan holding company (HOLA section 10) or a bank holding company (BHCA section 2), '1,200 persons' (comps1885.txt, located; the defined terms are cited to the two Acts that L01.html:111 says it does not read).")
row("LX2a-L01-5d", "2.1 attribution: section 5(d)", "L01.html:362",
    "5(d) in comps1884.txt: 'an emerging growth company ... may engage in oral or written communications with potential investors that are qualified institutional buyers or institutions that are accredited investors' (located). L01.html:362 paraphrases this with the same content.")
row("LX2a-L01-6e1-8e", "2.1 attribution: sections 6(e)(1) and 8(e)", "L01.html:362-363, :483",
    "6(e)(1) quotation 'for confidential nonpublic review by the staff of the Commission prior to public filing' (located); R2 quotation 'the initial confidential submission and all amendments thereto shall be publicly filed with the Commission not later than 15 days before the date on which the issuer conducts a road show' (located, quotecheck_ci_r10 OK). 8(e) 'The Commission is hereby empowered to make an examination in any case ... whether a stop order should issue under subsection (d)' (comps1884.txt:1812-1813) matches L01.html:363.")
row("LX2a-L01-headings", "2.1 attribution: headings before sections 3 and 4", "L01.html:360",
    "comps1884.txt prints 'EXEMPTED SECURITIES' directly before 'SEC. 3.' and 'EXEMPTED TRANSACTIONS' directly before 'SEC. 4.' (grep, this round; the headings are the compilation's own).")
row("LX2a-L01-markup", "2.9 markup and structure of L01", "L01.html:51-109, :359-386, :499-513, :604",
    "Claim spans carry data-grade and data-cite with keys in references.json; blocks, dfn ids and tables are well formed (check_pages PASS; page_smoke PASS: zero console errors; math renders). Read in full this round.")
row("LX2a-L01-why-decide", "2.1 attribution: why-it-matters statements", "L01.html:51",
    "5(a) and 5(c) use 'in effect' and 'filed' (comps1884.txt); 13(a) 'registered pursuant to section 12' and 15(d)(1) 'has become effective' (comps1884.txt/comps1885.txt). The sentence is a reading of those words and is graded C with locators.")
row("LX2a-L01-why-requirements", "2.1 attribution: requirement statements", "L01.html:51",
    "The statements 'the Securities Act of 1933 makes the status ... a condition of the offer and the sale' (5(a), 5(c)) and 'the Securities Exchange Act of 1934 sets a separate registration ... and periodic reporting' (12(a), 12(b), 13(a)) match the locators in the claim spans.")
row("LX2a-L01-in-effect-attribution", "2.1 attribution: 'in effect' is not defined in section 2", "L01.html:69",
    "The lesson states that the section 2 definitions do not define 'in effect'. Searched the text of comps1884.txt from 'SEC. 2.' to 'SEC. 3.' (this round): zero occurrences of 'in effect'. The lesson's reading is labelled as a reading.")
row("LX2a-L01-readings-para", "2.1 attribution and reasoning: §2 readings paragraph", "L01.html:88",
    "5(a) 'unless a registration statement is in effect' gives sale unlawful when filed only (statute read); R5c is the lesson's reading, labelled; 8(a) 'except as hereinafter provided' (located); 8(b) and 8(d) 'let the Commission hold a statement ... or suspend it afterwards' is a paraphrase of the located text.")
row("LX2a-L01-exchange-defined", "2.1 attribution and definitions: 'national securities exchange' and the exchange/OTC distinction", "L01.html:63, :96",
    "The phrase 'national securities exchange' is used in 12(a), 12(b), 12(d) and 13(a) (comps1885.txt) and the lesson says the statute does not define it (L01.html:96). The 1934 title names exchanges and over-the-counter markets (COMPS-1885_details.html:458). The exchange/OTC distinction is linked to FC1 concept exchange-vs-otc (concepts.html:478).")
row("LX2a-L01-model", "2.4 notation and 2.5 labs: the lifecycle model as the lab encodes it", "L01.html:113-135; tests/labs/LX2/lab-LX2-L01-1.py:13, :61-66, :88-108",
    "5 statuses x 2 listings = 10 states (L01.html:115). Transitions: 1933 events 6 x 2 = 12 (:119), 1934 events 2 x 5 = 10 (:120), total 22 (:122). Readings R13, R15, R5c, R5a (:126-129) match duty_13 (twin line 88), duty_15d (93-96), offer_permitted and sale_permitted (up to line 108) in the twin. A1 (:132-135) matches the twin docstring (line 13) and duty_15d.")
row("LX2a-L01-lab1-run", "2.5 labs: lab-LX2-L01-1 runs and its output matches the page", "L01.html:137-315; tests/labs/LX2/lab-LX2-L01-1.py",
    f"Twin alone: exit 0, stderr 0 bytes, 39 stdout lines; page code equals twin; expected block (L01.html:275-313) equals output ({R}out_lab_twin_r10.txt, {R}out_twin_isolated_r10.txt); run_labs PASS.")
row("LX2a-L01-lab1-hypothesis", "2.5 labs: the hypothesis states the printed result", "L01.html:139",
    "Printed: 10 states, 22 transitions (expected lines 275); 0 leave the state set (276); 10 of 10 reachable (277); 0 states with both duties (289); 0 with sale and no offer (290). State table counts (lines 279-288): sale yes in 2 states, offer yes in 4, R13 yes in 5, R15 yes in 2 -- the hypothesis gives the same four counts.")
row("LX2a-L01-lab1-interpretation", "2.2 interpretation claims versus the output", "L01.html:314",
    "The paragraph claims the 22 transitions connect the whole state set (line 277), that no state carries both duties (289) and that no state permits a sale without an offer (290). It names the R15 dependence on A1 and the model's own definitions as the only ground. It does not claim the statute has this structure.")
row("LX2a-L01-prop4.1", "2.4 mathematics: Proposition 4.1 and its proof", "L01.html:320-329",
    "H1 gives the 10 states, the start state and the 22 transitions. The proof's paths: (u,n) start; (u,l) by register; (f,n) by file; (f,l) by file, register; (r,n) by file, refuse; (r,l) by file, refuse, register; (e,n) by file, declare; (e,l) by file, declare, register; (s,n) by file, declare, stop; (s,l) by file, declare, stop, register. Each arrow is one of the 22 transitions in the twin's make_transitions (checked against the transition list at lab output lines 292-313). Ten states covered.")
row("LX2a-L01-prop4.2", "2.4 mathematics: Proposition 4.2 and its proof", "L01.html:332-341",
    "R13 holds only for listed, R15 only for not_listed (duty_13 and duty_15d in the twin). A state has one listing value, so no state satisfies both. The second sentence of 15(d)(1) (comps1885.txt) is quoted as the statute's version of the same non-overlap, which L01.html:340 states as consequence, not as the proof.")
row("LX2a-L01-prop4.3", "2.4 mathematics: Proposition 4.3 and its proof", "L01.html:344-353",
    "R5a permits a sale only in status effective (sale_permitted); R5c permits an offer in filed or effective (offer_permitted). Every state where R5a holds has status effective, which is one of the R5c statuses. The lab's state table has sale yes only in effective states (lines 285-286).")
row("LX2a-L01-canon-breaks", "2.2 claims about the model's limits (§5)", "L01.html:355-367",
    "Seven limits (timing, exemptions, independence, emerging growth companies, proceedings, fiscal-year suspension, A1). 12(d) thirty days (comps1885.txt, located); 8(a) (located); 8(e) (located); 5(c) 'any public proceeding or examination under section 8' (located); 5(d) (located); 2(a)(19) (comps1884.txt '(19) The term emerging growth company means ...'). A1 consequence 'the lab's output would change in one row, in its s15(d) column': with R15 requiring effective alone, stop_order/not_listed changes from yes to no (lab row line 287); the both-duties count stays 0 because the changed row is stop_order/not_listed, where R13 is already false (line 287 shows s13 no). Checked by hand.")
row("LX2a-L01-misconceptions", "2.2 misconceptions: statements and locators", "L01.html:369-389",
    "Misconception 1 (5(a), 8(a)), 2 (8(d), statute located; the model's stop_order row prints offer no and sale no, lab lines 287-288), 3 (6(a), 12(b), located), 4 (13(a) 'registered pursuant to section 12' and 15(d)(1) 'if and so long as', located). Four misconceptions, the minimum is three.")
row("LX2a-L01-problems", "2.2 problems: every solution and proof re-derived", "L01.html:391-494",
    "M1-M3: states and flags match lab rows 281, 285, 287-288 and the reading R15 under A1. P1: 6x2 + 2x5 = 22 (lab prints 22). P2: proof of 4.3. P3: non-overlap uses the listing requirement only. E1: 2 of 10 (rows 285-286). E2: section 8 lines 294-303 (10), section 12 lines 304-313 (10), section 6(a) lines 292-293 (2); total 22. E3: lab line 277. R1-R3: the statute quotations in R1 and R3 are located; R2 quotation located (quotecheck_ci_r10 OK).")
row("LX2a-L01-key-results", "2.3 grades and key results table", "L01.html:499-513",
    "Each statute row is grade C with a locator that holds the cited sentence (5(c), 5(a), 8(a), 8(d), 12(a), 13(a), 15(d)(1) second sentence; located). The two T rows are Propositions 4.1 and 4.2/4.3, and the lab row (511) is C, as the lab-result rule requires. Counts match the output (lines 275-290).")
row("LX2a-L01-quiz", "2.7 quiz items and explanations", "L01.html:517-600",
    "Ten items; each explanation checked against its lesson section. Numeric answers: 2 (E1), 30 (12(d) thirty days from day 0), 22 (6x2 + 2x5). Option sets: q1 5(a), q2 5(c), q4 8(a), q6 third sentence of 15(d)(1) (quoted with 300 persons), q7 5(c), q9 limits (seven listed at :588 match §5), q10 Proposition 4.2 hypothesis. No option is ambiguous with another.")
row("LX2a-L01-references", "2.1 references section", "L01.html:602-606",
    "The page cites only gpondsecurities and gpondsecuritiesb (grep data-cite, this round: no gpo or cfandcode key appears on L01.html). The text says no case is cited (:604), which holds.")
row("LX2a-L01-dag", "2.9 DAG: concept links and definitions in L01", "L01.html:37-38, :63; L01.html (whole page)",
    "L01 links to FC1 (exchange-vs-otc, concepts.html:478), P0.1 (evidence-grade, concepts.html:39) and M1 (quantifiers, concepts.html:78): all in the closure. L01 defines securities-registration (:74) and exchange-act-1934 (:96), each once. No later-lesson concept is linked or defined.")
row("LX2a-L01-hours", "2.9 hours: lesson hours", "L01.html:2, :34",
    "data-hours=9 (:2) and '9 study hours' (:34); lesson split 9 x 4 = 36 per index.html:176-186.")
row("LX2a-L01-paraphrase-locators", "2.1 paraphrases carry locators", "L01.html:65-70, :80-85, :96-111, :362-363, :483",
    "Each paraphrase sits in a claim span with data-locator. Checked against the statute: 8(b) paraphrase (:84) matches comps1884.txt:1766-1775; 15(d)(1) third-sentence paraphrase (:111) matches comps1885.txt; 12(d) paraphrase (:359) matches; 8(d) paraphrase (:85) states the notice and hearing condition without the 'within fifteen days' clause, which is a shortening, not a misstatement; not graded further.")
row("LX2a-L01-unspanned-readings", "2.1 sentences outside claim spans", "L01.html:51, :53, :69, :92, :96",
    "The unspanned sentences are readings of the lesson ('This lesson reads in effect as ...', 'the model ...') or definitions stated as the lesson's, and are labelled as such. No unspanned sentence states a statutory requirement that the text does not contain.")
row("LX2a-L01-section-locators", "2.1 locators: section numbers in claim spans exist in the statute", "L01.html:51-111, :359-365, :483",
    "Each section number in a locator is present in the compilation: 2(a)(5) ('The term Commission means the Securities and Exchange Commission', comps1884.txt), 2(a)(19) (comps1884.txt), 5(a)-(d), 6(a)-(c), 6(e)(1), 8(a), 8(b), 8(d), 8(e) (comps1884.txt); 12(a), 12(b), 12(d), 13(a), 15(d)(1) (comps1885.txt).")
row("LX2a-L01-lab1-run-extra", "2.5 labs: lab-LX2-L01-1 run (second check)", "L01.html:137-315",
    "Same run as LX2a-L01-lab1-run: run_labs PASS, twin isolated exit 0 with zero stderr, page code equals twin, expected equals output.")
row("LX2a-L01-structure", "2.9 structure of L01", "course/modules/LX/LX2/L01.html:32-616",
    "Read in full this round. Sections §1-§10 in order (lines 55, 67, 90, 113, 137 lab, 316-353 propositions, 355 canon breaks, 369 misconceptions, 391 problem set, 496 key results, 517 quiz, 602 references), nav to L02 (:610); §4.2 order satisfied (see LX2a-IDX-structure).")
row("LX2a-L01-title-1933-1934-extra", "2.9 L01 titles", "L01.html:6, :35",
    "<title> (:6) and h1 (:35) both read 'Registration, Disclosure and the Two Acts' as index.html:150 (title tag differs only by the lesson prefix).")
row("LX2a-L02-structure", "2.9 structure of L02", "course/modules/LX/LX2/L02.html:32-674",
    "Read in full this round. Sections §1-§10 in order: provision (55), classical theory (63), tipping (76), misappropriation (100), Lab 1 at 127-439 with assumptions 119-125 before it, canon breaks (441), misconceptions (453), problem set (463), key results (568), quiz (585), references (660); nav to L01 and L03 (:667-668). Why-it-matters 102 words.")
row("LX2a-L02-opinion-quotes", "2.1 attribution: every opinion quotation in L02", "course/modules/LX/LX2/L02.html:58-110, :424-431, :441-445, :482, :541-548, :617",
    "loccheck_r10.py over every claim span with a quotation and a gpo key (58 quotations): 54 located on a printed page inside the locator set. Four not reported as located by the script were checked by hand against the opinions (see LX2a-quote-search): O'Hagan pp. 651, 652 and 655 and Dirks p. 654. The Thomas dissent quotation (L02.html:109, p. 680) and Scalia (p. 679) are located.")
row("LX2a-L02-n23-attribution", "2.1 attribution: Dirks footnote 23 (p. 663 n. 23)", "course/modules/LX/LX2/L02.html:61, :445, :579, :631",
    "pdf page 18 of USREPORTS-463-646 (printed p. 663; offset 645) footnote 23: 'Scienter ... a mental state embracing intent to deceive, manipulate, or defraud ... is an independent element of a Rule 10b-5 violation' (located). p. 663 text: 'Scienter in some cases is relevant in determining whether the tipper has violated his Cady, Roberts duty' (the basis of L02.html:631).")
row("LX2a-L02-title-h1", "2.9 L02 h1 equals the hub title", "course/modules/LX/LX2/L02.html:35; index.html:151, :181",
    "L02.html:35 'Insider trading and tipping' (h1) = index.html:151 card title = index.html:181 hours table row 'Lesson 2, Insider trading and tipping' (text match on the lesson map).")
row("LX2a-L02-lab-run", "2.5 labs: lab-LX2-L02-1 runs alone", "course/modules/LX/LX2/L02.html:127-439; tests/labs/LX2/lab-LX2-L02-1.py",
    f"Twin alone: exit 0, stderr 0 bytes, 25 stdout lines; page code equals twin ({R}out_lab_twin_r10.txt); run_labs PASS.")
row("LX2a-L02-lab-output", "2.5 labs: printed output and the expected block", "course/modules/LX/LX2/L02.html:413-437; twin lines 226-283",
    "Expected block (413-437) equals the twin output (expected_equals_output=True, out_lab_twin_r10.txt). Rows recomputed from the twin's flags: P1-P8 decisions as printed; fired 4 of 8 (P1, P3, P4, P6); not fired 4 of 8.")
row("LX2a-L02-classical-element", "2.5 labs: classical branch elements and their locators", "course/modules/LX/LX2/L02.html:73, :459, :473; twin lines 226-231",
    "Twin lines 226-231: material information, nonpublic information, a trade (key gpo1997united, pp. 651-652), and no public disclosure before the trade (key gpo1983dirks, p. 654). L02.html:73 and M1 (:473) state the same four checks and locators.")
row("LX2a-L02-hypothesis", "2.5 labs: hypothesis states the printed result", "course/modules/LX/LX2/L02.html:129",
    "Hypothesis: fired P1, P3, P4, P6; unfired P2 (benefit), P5 (knowledge), P7 (disclosure to source), P8 (duty). Printed rows 425-432 agree on the deciding element of each pattern.")
row("LX2a-L02-example-3.2", "2.5 labs and examples: Example 3.2 (P2 to P5)", "course/modules/LX/LX2/L02.html:92-94",
    "P2 benefit none fails at p. 662 (row 426). P3 and P4 fire at p. 660 (rows 427-428). P5 knowledge fails at p. 660 (row 429; P5 has benefit pecuniary and knew_or_should_have_known False in the twin).")
row("LX2a-L02-example-2.2-4.2", "2.5 labs and examples: Examples 2.2 and 4.2 (P1, P6, P7)", "course/modules/LX/LX2/L02.html:72-74, :111-113",
    "P1 classical, fired with pp. 651-652 (row 425), four checks passing. P6 misappropriation fired at p. 652 (row 430). P7 disclosure element fails at p. 655 (row 431).")
row("LX2a-L02-canon-breaks", "2.2 canon breaks: five limits and their quotations", "course/modules/LX/LX2/L02.html:442-451",
    "Five limits (scienter, materiality, benefit, misappropriation's one source of duty, one trade per pattern). Scienter quotation at p. 663 n. 23 (located). Materiality quotation 'it may not be clear' at p. 662 (located). Benefit quotation 'objective facts and circumstances that often justify such an inference' at p. 664 (located). O'Hagan footnote 7 at p. 655 n. 7 (located).")
row("LX2a-L02-interpretation", "2.2 interpretation paragraph versus the output", "course/modules/LX/LX2/L02.html:438",
    "The paragraph names the printed table and the rules, says the lab does not assess materiality, benefit, knowledge, disclosure or scienter, and states 'four fired ... (P1, P3, P4, P6) and four unfired (P2, P5, P7, P8)' (matches rows 425-435). P2's non-firing is attributed to A1 and to Dirks p. 664 'a question of fact' (located).")
row("LX2a-L02-misconceptions", "2.2 misconceptions: statements and locators", "course/modules/LX/LX2/L02.html:453-461",
    "Four misconceptions. p. 654 (possession; located), p. 660 (tippee assumes duty only on breach and knowledge; located), p. 662 'Absent some personal gain' (located), p. 664 gift case (located), p. 652 and p. 653 n. 5 for the outsider (footnote 5 printed on p. 653 reads 'O'Hagan was not an insider of Pillsbury', checked by pdftotext layout). P8, P5, P2, P4, P6 outcomes match rows 425-432.")
row("LX2a-L02-problems", "2.2 problems: solutions, proofs and tiers", "course/modules/LX/LX2/L02.html:463-566",
    "Four tiers with three problems each. M1 (four checks, L02.html:473), M2 (P6 vs P7; P7 fails the source check at p. 655), M3 (P3 benefit none: fails tipper's benefit at p. 662; scratch run this round, see LX2a-L02-M3-scratch). Pr1, Pr2, Pr3 proofs read and checked against the twin code (Pr2 loop and final return match classify, twin lines 252-260). E1 (the four fired and four unfired patterns with their elements) matches the printed table; E2 and E3 match the printed table and the scratch runs. R1-R3 quotations located.")
row("LX2a-L02-pr1-A2", "2.1 item 6: assumptions used in a proof are declared", "course/modules/LX/LX2/L02.html:83-86, :496-498",
    "Pr1 cites Assumption A1 of §3 (declared at L02.html:83-86) and H1-H3 at p. 660 and p. 662 (located). The proof uses H1 in the necessity direction only, which the text says. A1 is declared before its use.")
row("LX2a-L02-markup", "2.9 markup of L02", "course/modules/LX/LX2/L02.html:53, :84, :92, :541, :548, :599, :608, :617",
    "66 claim spans with data-grade C, a data-cite key in references.json and a data-locator (grep and loccheck this round); dfn ids unique (check_dag PASS); quiz and problem markup closed (page_smoke PASS).")
row("LX2a-L02-E2-E3-scratch", "2.5 labs: scratch predictions E2 and E3", "course/modules/LX/LX2/L02.html:526-539",
    f"Scratch run this round ({R}scratch_r10.py, outputs {R}out_scratch_r10.txt): E2 (P2 benefit reputational): P2 fired, locator p. 660, summary 'fired: P1, P2, P3, P4, P6 (5 of 8)', no other row changes; prediction at L02.html:530 matches. E3 (P7 source-told false): P7 fired with gpo1997united p. 652, summary 'fired: P1, P3, P4, P6, P7 (5 of 8)'; prediction at :537 matches.")
row("LX2a-L02-key-results", "2.3 key-results table", "course/modules/LX/LX2/L02.html:568-583",
    "Each row's source checked: classical pp. 651-652 and dissent p. 672 (located); possession p. 654 (located); tippee p. 660 and dissent p. 671 'Accepting the Court's view of tippee liability' (read at p. 671); benefit pp. 662-663, dissent pp. 668, 674 (located); gift p. 664 and dissent p. 676 n. 13 (located); misappropriation pp. 652, 655, 656 and dissents p. 680 and p. 679 (located); scienter p. 663 n. 23 (located); Lab 1 four fired (output).")
row("LX2a-L02-quiz", "2.7 quiz items and explanations", "course/modules/LX/LX2/L02.html:585-657",
    "Nine items, each explained. Numeric answers: 4 fired (summary line), 3 outsiders (P6, P7, P8: roles outsider in the twin), 1 knowledge failure (P5). Keys: q1 classical insider and temporary fiduciary (p. 652), q2 'only when' at p. 660, q3 p. 662, q4 p. 655 (located), q5 p. 663 n. 23, q6 P4 (gift, fired) and P2 (no benefit), P7 (disclosure).")
row("LX2a-L02-dag", "2.9 DAG: links and definitions in L02", "course/modules/LX/LX2/L02.html:37, :56, :66, :80, :103",
    "L02 links only L01.html#def-exchange-act-1934 (L01.html:96 exists) and L03 as next lesson. Defines insider-trading-doctrine (:66), tipper-tippee-liability (:80) and misappropriation-theory (:103), each once. No concept outside the closure is linked (links_r10.py: 3 fragment links, 0 unresolved).")
row("LX2a-L02-B3-B1", "2.9 and 2.1: no Texas Gulf Sulphur, Dodd-Frank or MiFID II content in L02", "course/modules/LX/LX2/L02.html (whole page); index.html:171; L02.html:654",
    "grep of L02.html (this round) for Texas, Gulf, Sulphur, Dodd, MiFID: no match. index.html:171 says Dodd-Frank and MiFID II are not in the registry. L02 cites only the two opinions and the statute text quoted in Dirks.")
row("LX2a-L02-years", "2.9 prose years", "course/modules/LX/LX2/L02.html (prose)",
    "Grep (this round) of L02.html outside <pre> and <script>: the only four-digit years are inside the Act name 'Securities Exchange Act of 1934' (links to L01). No year is printed for Dirks or O'Hagan.")
row("LX2a-L02-why", "2.1 why-it-matters statements", "course/modules/LX/LX2/L02.html:51",
    "The claims about the three tests locate the duty with the printed pages Dirks pp. 654, 660 and O'Hagan p. 652 (located, loccheck this round). 'The lab does not say how a court would rule' is a limit statement.")
row("LX2a-L02-tippee-definition", "2.1 tippee definition and its quotation", "course/modules/LX/LX2/L02.html:76-77",
    "Dirks p. 655 'Unlike insiders who have independent fiduciary duties to both the corporation and its shareholders, the typical tippee has no such relationships' (located).")
row("LX2a-L02-page-locators", "2.1 every claim-span locator is a page inside the cited opinion", "course/modules/LX/LX2/L02.html (all claim-span locators and the decision rows of the table)",
    "loccheck_r10.py: every quotation with a locator reaches a printed page in the locator set (except the four checked by hand). Decision-row locators (rows 425-432) match the twin's BRANCH_RULE (twin lines 39-43) and Check locators (twin lines 228-247).")
row("LX2a-L02-scienter-composite", "2.1 scienter statement", "course/modules/LX/LX2/L02.html:437, :445, :579",
    "'Scienter is not checked.' (line 437) and the scienter claim at :445 match the lab (the lab reads 'Scienter is not checked' at its last print line) and Dirks p. 663 n. 23 (located).")
row("LX2a-scope-note", "2.2 scope words in the lede and scope notes", "course/modules/LX/LX2/index.html:33; L01.html:53; L02.html:53",
    "index.html:33 'every regulatory statement' is a stated requirement of the report (the project's rubric, not a fact about the statute); L01.html:53 and L02.html:53 state the educational and not-legal-advice reading and the HYPOTHETICAL label (L02). The scope words 'every' and 'all' in the lede describe the module's own requirements.")
row("LX2a-notation", "2.4 notation against notation/notation.json", "course/modules/LX/LX2/L01.html:115-352 (math and labels); L02.html (whole page); index.html (placement math)",
    "Symbols used on the three pages: x, S, P(x), f(x,y), y (index.html placement, generic variables), H (L01 and L02 do not use it), and the L01 proof's u, f, r, e, s, n, l abbreviations. notation/notation.json registers T, the statistical symbols and the macros \\E, \\R and others; none of x, S, P, f, y, u, r, e, s, n, l has a registered meaning. Registry flag only: \\blacksquare (L01.html, 3 uses) is not registered; it is a proof-end mark, not a symbol with a meaning, so it is recorded in registry_flags, not as a collision.")
row("LX2a-L01-section-locators-extra", "2.1 locators: second check", "course/modules/LX/LX2/L01.html:51-111, :359-365, :483",
    "Same check as LX2a-L01-section-locators: every locator names a section present in the compilation.")
row("LX2a-L02-M3-scratch", "2.5 labs: M3 scratch prediction (P3 benefit to none)", "course/modules/LX/LX2/L02.html:483-489",
    f"Scratch run this round ({R}out_scratch_r10.txt): P3 with tipper_benefit none: 'not fired', element 'fails: tipper's personal benefit (none)', key gpo1983dirks, locator p. 662. The M3 solution (L02.html:487) gives the same element and locator.")
row("LX2a-registry-keys", "2.1 registry keys cited in L01, L02 and the hub", "references/references.json; course/modules/LX/LX2/index.html:195-200; L01.html; L02.html",
    "Keys cited: gpondsecurities, gpondsecuritiesb (L01), gpo1983dirks and gpo1997united (L02 and the twin), cfandcode and frb2026fed (reading list only). grep (this round): each key occurs once in references.json.")
row("LX2a-counter-evidence", "2.3 grade C doctrine claims name the dissents that dispute the tests", "course/modules/LX/LX2/L02.html:90 (benefit test), :109 (misappropriation), :570-580 (key results)",
    "L02.html:90 names Blackmun, J., dissenting, from p. 667 (Dirks p. 667 'Blackmun, with whom Justice Brennan and Justice Marshall join, dissenting': located) and quotes pp. 668, 674, 676 n. 13. L02.html:109 names Thomas, J. (p. 680) and Scalia, J. (p. 679), both located.")
row("LX2a-lab-assumptions", "2.1 item 6: the lab declares its assumptions", "course/modules/LX/LX2/L02.html:83-86, :119-125, :127-129; tests/labs/LX2/lab-LX2-L02-1.py:19-21",
    "A1 (:83-86) for the benefit flag; 'Assumptions of Lab 1' lists A2 (facts as stated) and A3 (temporary fiduciary role) at :119-125; the hypothesis (:129) names A1, A2 and A3. The twin docstring (lines 19-21) states that the classifier reads materiality, confidentiality, benefit, knowledge and disclosure as stated, which is A2.")
row("LX2a-L02-remark-3.3", "2.1 Remark 3.3 against the cited pages", "course/modules/LX/LX2/L02.html:97",
    "Dirks p. 662 'the test for whether a tip is a breach' (located, p. 662). Knowledge as a separate condition at p. 660 (located). P5 fails the knowledge element (row 429).")
row("LX2a-r8-delta", "2.9 round 8 delta (06994db1..0dee921a): superseded",
    "course/modules/LX/LX2/index.html:59-62, :168-171; course/modules/LX/LX2/L02.html:66-125, :129, :430-446, :493-496, :570-580; tests/labs/LX2/lab-LX2-L02-1.py:6-7",
    "Round 8's delta is not the delta under review. Its hunks are inside the files re-read in full this round (index.html, L01.html, L02.html); the content at those lines was verified in this round (see the rows above). Kept for id continuity; no separate finding.")
row("LX2a-r9-delta", "2.9 round 9 delta (0dee921a..c93dd52): superseded by round 10 delta",
    "git diff 0dee921a..c93dd52 -- course/modules/LX/LX2 tests/labs/LX2",
    "Round 9's delta is kept for id continuity. The two round-9 FAIL rows (LX2a-card-c010, LX2a-card-c016) are re-verified in round 10 and now PASS. The L02 Remark 3.3, Thomas quotation and E3 wording hunks are re-read in full this round.")
row("LX2a-r10-delta", "2.9 round 10 delta (c93dd52..00a84795) for slice a: every hunk read",
    "git diff c93dd52..00a84795 -- course/modules/LX/LX2/index.html course/modules/LX/LX2/L01.html course/modules/LX/LX2/L02.html course/modules/LX/LX2/cards.json tests/labs/LX2",
    "Hunks read: index.html:33 (lede) and :96-98 (PV item wording, 100 without 'cents'; answer 90.91 unchanged: 100/1.1 = 90.909); L01.html:84 (8(b) ten days, verified against comps1884.txt:1766-1775), :111 (1,200 persons, verified against comps1885.txt, Prop. 15(d)(1) third sentence), :115 (model intro wording), :362 (2(a)(19) EGC bullet, verified against comps1884.txt '(19) The term emerging growth company' ), :65 unchanged (the enumeration FAIL is LX2a-L01-amended); cards.json LX2-c092 (Proposition 4.3 wording; verified against L01.html:344-353); L02.html:53 (HYPOTHETICAL scope sentence), :465 (problem-set intro), :505 (Pr2 solution wording; 'classify' is the function at twin line 252), :528 (E2 wording). tests/labs/LX2 and the twins are byte-identical to the round-9 pin (git diff empty). Verdict: all hunks PASS except the enumeration in L01.html:65 (LX2a-L01-amended).")
row("LX2a-card-c010", "2.7 card agrees with the current L01 text and the statute",
    "course/modules/LX/LX2/cards.json LX2-c010 (back); L01.html:84 (§2, Section 8(b) paragraph)",
    "Round 9 FAIL cleared. The card now gives the ten-day notice and ten-day hearing of 8(b), which L01.html:84 states. Read against comps1884.txt:1766-1775: 'not later than ten days after the filing' and 'within ten days after such notice' (matches). Every number in the card appears in L01.html:84.")
row("LX2a-card-c016", "2.7 card agrees with the current L01 text and the statute",
    "course/modules/LX/LX2/cards.json LX2-c016 (back); L01.html:111 (§3, third sentence of section 15(d)(1))",
    "Round 9 FAIL cleared. The card gives 1,200 persons for a bank, savings and loan holding company or bank holding company, which L01.html:111 states. comps1885.txt: 'in the case of a bank, a savings and loan holding company (as defined in section 10 of the Home Owners' Loan Act), or a bank holding company ... 1,200 persons'. Matches.")
row("LX2a-cards-L01-other", "2.7 L01 cards (sampled and full read)",
    "course/modules/LX/LX2/cards.json (L01 cards except c010 and c016; 32 L01 cards in total)",
    "All 30 remaining L01 cards read against L01.html and the statute: c001-c009, c011-c015, c017-c027, c090-c092, c095-c096. c092 (changed this round) matches L01.html:344-353. c017-c019 carry the propositions' hypotheses H1 and their conclusions. c023 and c090-c092 are grade C with basis naming Lab 1, as L01.html:511 and the lab-result rule require. c021 matches P1 and the lab count of 22.")
row("LX2a-cards-L02", "2.7 L02 cards and assumption cards",
    "course/modules/LX/LX2/cards.json (L02 cards; 19 in total)",
    "All 19 read against L02.html §2-§7 and key results: c028-c043 quotations and locators (c042 footnote 5 at p. 653 and c043 footnote 7 at p. 655 n. 7, both printed on those pages); c038 (four fired, P1, P3, P4, P6); c097-c099 (A1, A2, A3) match L02.html:83-86 and :119-125.")
row("LX2a-cards-dup", "2.7 duplicate scan", "course/modules/LX/LX2/cards.json (100 cards)",
    "Python check this round: 100 cards, no duplicate id, no duplicate front (L01 32, L02 19, L03 22, L04 27).")
row("LX2a-r9-quotes-L02", "2.1 quotations in L02 located in the fetched opinions",
    "course/modules/LX/LX2/L02.html (all claim spans with a quoted passage and a gpo key)",
    f"loccheck_r10.py over L02.html this round ({R}out_loccheck_L02_r10.txt): every claim-span quotation with a gpo key located on a printed page inside its locator set, except four quotations that the script reports CHK and that were then checked on the printed text (see LX2a-quote-search).")
row("LX2a-r9-sources", "2.1 the primary sources are the same bytes as in earlier rounds",
    "/tmp/lx2a_r10_dl_1793865981 (fetched by plain curl with ledgers/LX2/scripts/LX2-a-r8/fetch_sources.sh)",
    f"sha256 this round ({R}out_sha256_sources_r10.txt) for COMPS-1884.pdf, COMPS-1885.pdf, USREPORTS-463-646.pdf, USREPORTS-521-642.pdf and their text extracts equals the round 9 record ({R.replace('r10','r9')}out_sha256_sources_r9.txt) line for line (order differs only).")
row("LX2a-L02-E3-delta", "2.5 labs: E3 wording (P7 matches P6 in every flag) is true of the twin",
    "course/modules/LX/LX2/L02.html:533-539; tests/labs/LX2/lab-LX2-L02-1.py (labels P6, P7)",
    f"Twin: P6 and P7 differ only in label and source_told_of_trade (False vs True), checked by parsing the Pattern blocks this round. Scratch run e3 (P7 source-told False) fires P7 with gpo1997united p. 652 ({R}out_scratch_r10.txt), as E3 predicts.")

fragment = {
    "unit": "LX2",
    "slice": "LX2-a",
    "round": 10,
    "verifier": "Haiku independent verifier, LX2-a round 10 (did not build LX2; builder ledgers and scratch not read). Full read of index.html, L01.html and L02.html this round; every command row re-run at the pin; the round-9 FAIL rows re-verified.",
    "pin": "00a84795f276456fce19d4181373cc4efba11a36",
    "base": "c93dd526025c6dffd34c54cd2c89eb62a890f885",
    "checkout": str(ROOT),
    "scratch": "/tmp/lx2a_r10_dl_1793865981 (four primary sources by plain curl; loccheck/quotecheck scripts copied there); /tmp/lx2a_r10_scratch_* (L02 twin scratch copies, also in ledgers/LX2/scripts/LX2-a-r10/scratch_twins_r10/)",
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [
        "references/references.json key gpo1983dirks: title field reads 'Dirks v. SEC, 463 U.S. 646 (1982)' and year field reads 1983 (references.json:10823-10835). GovInfo USREPORTS-463-646 details: decided July 1, 1983. No slice-a page prints a year for Dirks. The architect corrects the record through add_reference.py.",
        "notation/notation.json does not register \\blacksquare, the proof-end mark used on L01.html (three uses) and on other course pages. A strict reading of BLUEPRINT notation rule 13 would make this a FAIL; it is recorded here as a registry flag because it is a typesetting mark, not a symbol with a meaning. The architect decides whether to register it.",
        "No registry key or source string exists for Dodd-Frank, MiFID II or Texas Gulf Sulphur (grep, references/references.json). L02 and the hub say so; the REFERENCE_REQUESTS stay open.",
    ],
    "freshness_flags": [],
    "notes": (
        "Round 10 at pin 00a84795 (delta from c93dd52). Changed in slice a: index.html (:33 lede, :96-98 PV item), L01.html (:84 8(b), :111 15(d)(1), :115 model intro, :362 EGC bullet), L02.html (:53, :465, :505, :528), cards.json (c092). "
        "Round-9 FAIL rows LX2a-card-c010 and LX2a-card-c016 are now PASS. One new FAIL: LX2a-L01-amended (the section-number enumeration in L01.html:65 omits 2(a)(19), which L01.html:362 now cites). "
        "Observations, not rows: L01.html:85 paraphrases 8(d) without the 'within fifteen days' timing clause (the quoted words are accurate); L01.html:585 option wording 'no exemption states' is awkward but not graded. "
        "Labs are demonstrations; no mutants are required for this slice (VERIFIER 2.6 applies to project graders only). "
        "The stale files from an earlier attempt in ledgers/LX2/scripts/LX2-a-r10/ (out_page_smoke_r10.txt, out_run_labs_L01/L02_r10.txt, out_quotecheck_L01/L02_r10.txt) are not cited by any row; the files cited here are the ones named out_*_r10.txt by round-10 runs and the *_ci_* and index/L01/L02 page-smoke outputs."
    ),
    "summary": "",
}
counts = {s: sum(1 for r in rows if r["status"] == s) for s in ("PASS", "FAIL", "UNVERIFIABLE")}
fragment["summary"] = (
    f"Slice LX2-a round 10 verdict FAIL at 00a84795. {len(rows)} rows: PASS {counts['PASS']}, FAIL {counts['FAIL']}, "
    f"UNVERIFIABLE {counts['UNVERIFIABLE']}. The single FAIL: LX2a-L01-amended (L01.html:65 section-number list omits 2(a)(19)); fix is one token in that sentence."
)
out = ROOT / "ledgers/LX2/LX2-a.json"
out.write_text(json.dumps(fragment, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(out, len(rows), counts)
