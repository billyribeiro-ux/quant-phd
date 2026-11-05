"""Build ledgers/LX2/LX2-a.json (round 11) from the round-10 fragment.

Rows whose cited lines are byte-identical since the previous pin 00a84795 are carried
with the required prefix. Rows whose subject changed in the round-11 delta, and the
command rows, carry new evidence from this round's outputs under ledgers/LX2/scripts/LX2-a-r11/.
"""
import json
import sys
from datetime import UTC, datetime
from pathlib import Path

PREV = "/Users/billyribeiro/.fanout/frags/E-LX2-a.round10.json"
OUT = Path(sys.argv[1])
SCR = "ledgers/LX2/scripts/LX2-a-r11/"
DELTA = ("delta 00a84795..11d7077: index.html:148, :161; L01.html:65, :585; L02.html:575; "
         "cards.json LX2-c002, c004, c005, c023, c090, c091, c092 (L01 cards)")

prev = json.load(open(PREV, encoding="utf-8"))
old = {r["id"]: r for r in prev["rows"]}

carry_files = "course/modules/LX/LX2/index.html, L01.html, L02.html, tests/labs/LX2/*.py"
def carried(rid, note=""):
    r = old[rid]
    cite = note or f"cited lines of {carry_files} are byte-identical since the previous pin 00a84795"
    return {"id": rid, "check": r["check"], "location": r["location"], "status": "PASS",
            "evidence": f"Carried from round 10 ({cite}; round-11 delta is outside these lines, see LX2a-r11-delta): "
                        + r["evidence"]}

def fresh(rid, evidence, location=None):
    r = old[rid]
    return {"id": rid, "check": r["check"], "location": location or r["location"],
            "status": "PASS", "evidence": evidence}

rows = []
R = {}  # id -> row (fresh or carried), filled below, order follows round 10

R["LX2a-cmd-check_pages"] = fresh("LX2a-cmd-check_pages",
    f"Re-run round 11 at 11d7077: .venv/bin/python tools/check_pages.py --unit LX2 -> 'check_pages LX2: PASS', exit 0 ({SCR}out_check_pages_r11.txt).")
R["LX2a-cmd-check_dag"] = fresh("LX2a-cmd-check_dag",
    f"Re-run round 11: .venv/bin/python tools/check_dag.py --unit LX2 -> 'check_dag LX2: PASS', exit 0 ({SCR}out_check_dag_r11.txt).")
R["LX2a-cmd-run_labs"] = fresh("LX2a-cmd-run_labs",
    f"Re-run round 11: .venv/bin/python tools/run_labs.py --unit LX2 -> 'run_labs LX2: PASS (7/7)', exit 0 ({SCR}out_run_labs_unit_r11.txt).")
R["LX2a-lab-isolated"] = fresh("LX2a-lab-isolated",
    f"Re-run round 11: {SCR}twin_isolated_r11.sh (out {SCR}out_twin_isolated_r11.txt): lab-LX2-L01-1 exit 0, stderr 0 bytes, 39 stdout lines, sha256 1ccac857...; lab-LX2-L02-1 exit 0, stderr 0 bytes, 25 stdout lines, sha256 4beca4fe...; both stdout hashes equal the round-10 values. `git diff --name-only 00a84795 HEAD -- tests/labs/LX2` is empty, so the twins are byte-identical (sha256 d50ca604... and d615f8cd...). Page lab code at L01.html:137-315 and L02.html:127-439 is outside the round-11 delta, so the page-code-equals-twin and expected-equals-output results from round 10 stand.")
R["LX2a-cmd-page_smoke"] = fresh("LX2a-cmd-page_smoke",
    f"Re-run round 11, each page alone: .venv/bin/python tools/page_smoke.py --unit LX2 --pages course/modules/LX/LX2/{{index,L01,L02}}.html -> 'page_smoke LX2: PASS', exit 0 for each ({SCR}out_page_smoke_index_r11.txt, out_page_smoke_L01_r11.txt, out_page_smoke_L02_r11.txt).")
R["LX2a-cmd-ruff-mypy"] = fresh("LX2a-cmd-ruff-mypy",
    f"Re-run round 11: ruff check and ruff format --check on tests/labs/LX2/lab-LX2-L01-1.py and lab-LX2-L02-1.py -> 'All checks passed!', '2 files already formatted' ({SCR}out_ruff_r11.txt); mypy --no-incremental on both -> 'Success: no issues found in 2 source files' ({SCR}out_mypy_r11.txt).")
R["LX2a-cmd-pytest"] = fresh("LX2a-cmd-pytest",
    f"Re-run round 11, targeted to the changed pages and cards: .venv/bin/python -m pytest -q tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py tests/test_page_smoke.py tests/test_curriculum.py tests/test_refs.py tests/test_build_site.py -> exit 0 ({SCR}out_pytest_r11.txt). The full tests/ run of round 10 (out_pytest_r10.txt) is carried for the other test files, which do not read this slice.")
R["LX2a-cmd-verify_refs"] = fresh("LX2a-cmd-verify_refs",
    f"Re-run round 11: tools/verify_refs.py --offline -> 'offline integrity: 560 entries, 0 problems' ({SCR}out_verify_refs_offline_r11.txt); tools/verify_refs.py --unit LX2 (live) -> 'live re-verification of LX2: 6 of 560 entries, 0 problems', exit 0 ({SCR}out_verify_refs_live_LX2_r11.txt). The flag `--unit` is live-only, so the offline and live runs are separate commands.")
R["LX2a-cmd-coursekit-closure"] = carried("LX2a-cmd-coursekit-closure", "index.html:35, :62 byte-identical; the prerequisite DAG is unchanged in the delta")
R["LX2a-quote-search"] = fresh("LX2a-quote-search",
    f"Round-10 search results carried for the entries not in the delta. Re-checked in round 11: the changed quotation at L02.html:575 (Dirks dissent) against the Dirks text (sha256 d295f808..., /tmp/lx2a_r10_dl_1793865981/dirks.txt, and the Dirks PDF extract). The passage reads 'Accepting the Court's view of tippee liability,5 it appears that Dirks' knowledge of this breach makes him liable as a participant in the breach after the fact' (ws-normalised check, footnote marker 5 included: True; {SCR}out_dirks_quote_r11.txt). It is on the printed page 671: pdftotext of USREPORTS-463-646.pdf places the passage after the page-671 running head and before the page-672 head (line 1071 vs line 1089 vs line 1112 of the extract). The round-10 Thomas and Scalia checks (L02.html:109) and the O'Hagan and Dirks p. 654 checks are unchanged.",
    location="course/modules/LX/LX2/L02.html:575 (changed quote), :109; L01.html and L02.html (other entries carried)")
R["LX2a-IDX-hours"] = carried("LX2a-IDX-hours", "index.html:41-44, :176-186 and L01.html:2, :34 byte-identical")
R["LX2a-IDX-structure"] = fresh("LX2a-IDX-structure",
    f"Re-read in full this round, index.html:1-207. The round-11 delta changes two sentences (:148 'the same main parts', :161 'The model case is SIMULATED.'). Neither changes an element, a heading or an order. check_pages LX2 PASS ({SCR}out_check_pages_r11.txt). Elements present as in round 10: objectives, prerequisite links, placement diagnostic, lesson map, project ladder, data status, hours, reading list.")
R["LX2a-IDX-closure"] = carried("LX2a-IDX-closure", "index.html:35, :62 byte-identical")
R["LX2a-IDX-FC1-title"] = carried("LX2a-IDX-FC1-title", "index.html:35 byte-identical")
R["LX2a-IDX-SR4"] = carried("LX2a-IDX-SR4", "index.html:39 byte-identical")
R["LX2a-IDX-lede-markup"] = fresh("LX2a-IDX-lede-markup",
    "Re-verified: index.html:33 byte-identical. L01.html:51-65 contains the changed line 65, which is plain prose with the claim spans at :65 unchanged (data-grade C, data-cite gpondsecurities and gpondsecuritiesb, data-locator Amended Through field of COMPS-1884 and COMPS-1885). check_pages LX2 PASS and page_smoke LX2 PASS (round-11 runs).")
R["LX2a-IDX-objectives-1-3"] = fresh("LX2a-IDX-objectives-1-3",
    "Re-verified: index.html:51-53 byte-identical. L01.html:55-130 contains the changed line 65 (the section-number list), which is not an objective and states no objective claim. L02.html:55-1xx unchanged except :575, which is a table row. The objectives match the lessons.")
R["LX2a-IDX-placement-arith"] = carried("LX2a-IDX-placement-arith", "index.html:95-141 byte-identical")
R["LX2a-IDX-placement-items-1-8"] = carried("LX2a-IDX-placement-items-1-8", "index.html:77-131 byte-identical")
R["LX2a-IDX-placement-cross-ref"] = carried("LX2a-IDX-placement-cross-ref", "index.html:136 byte-identical; L04.html:1 not in this slice's delta")
R["LX2a-IDX-skill-items"] = carried("LX2a-IDX-skill-items", "index.html:133, :138 byte-identical")
R["LX2a-IDX-concept-anchors"] = carried("LX2a-IDX-concept-anchors", "index.html:35, :64-68; L01.html:37-38, :63; L02 concept lines byte-identical")
R["LX2a-IDX-data-status"] = carried("LX2a-IDX-data-status", "index.html:170-171; L02.html:72, :87, :115, :118 byte-identical")
R["LX2a-IDX-core-reading"] = carried("LX2a-IDX-core-reading", "index.html:195-200 byte-identical")
R["LX2a-IDX-banned"] = fresh("LX2a-IDX-banned",
    f"Re-run round 11: grep -n -i -E 'TODO|TBD|lorem|for brevity|details omitted|beyond the scope|left as an exercise|you can add more|it is important to note|studies show|experts agree|it is well known|obviously|clearly|\\.\\.\\.|…' over index.html, L01.html, L02.html. The only hits are Python annotations in code (L01.html:169-184 and L02.html:215, :353: 'tuple[Pattern, ...]'), which are not an ellipsis for omitted content. The new prose (index.html:148, :161) contains none of these. Output: ledgers/LX2/scripts/LX2-a-r11/out_banned_and_cards_r11.txt (script banned_and_cards_r11.sh).")
R["LX2a-IDX-cards-title"] = carried("LX2a-IDX-cards-title", "index.html:150-153, :181; L01.html:35 byte-identical")
R["LX2a-IDX-concept-link-hub-text"] = carried("LX2a-IDX-concept-link-hub-text", "index.html:33, :62, :75, :170-171 byte-identical")
R["LX2a-L01-title-1933-1934"] = carried("LX2a-L01-title-1933-1934", "L01.html:59, :61 byte-identical")
R["LX2a-L01-amended"] = fresh("LX2a-L01-amended",
    "Round-10 FAIL is cured. L01.html:65 now reads 'sections 2(a)(5) and 2(a)(19), 3, 4, 5, 6 and 8 of the 1933 Act (with 5(d), 6(e)(1) and 8(e) in §5), and sections 12, 13 and 15(d) of the 1934 Act'. Re-derived every section number cited in L01.html by grep (section 2, 2(a)(5), 2(a)(19), 3, 4, 5(a)-(d), 6(a)-(e)(1), 8(a),(b),(d),(e), 12(a),(b),(d), 13(a), 15(d)(1); no section 1, 7, 9-11, 14 or 16). The enumeration covers all of them; 'section 2' is covered by 2(a)(5) and 2(a)(19). Primary text (comps1884.txt, sha256 eaf8af1a..., /tmp/lx2a_r10_dl_1793865981): 'SEC. 2.' at line 34, '(5) The term ‘‘Commission’’' at 166, '(19) The term ‘‘emerging growth company’’' at 299, 'SEC. 3.' at 392, so 2(a)(5) and 2(a)(19) are in section 2. 'SEC. 4.' at 750, 'SEC. 5.' at 1356 with '(d) LIMITATION' inside, 'SEC. 6.' at 1423 with '(e) EMERGING GROWTH COMPANIES' inside, 'SEC. 8.' at 1753 with '(e) The Commission is hereby empowered to make an examination' inside, 'SEC. 12.' at 2368, 'SEC. 13.' at 2411, 'SEC. 15.' at 2430. Amendment dates unchanged (comps1884.txt 'As Amended Through P.L. 119-27, Enacted July 18, 2025'; comps1885.txt 'As Amended Through P.L. 119-60, Enacted December 18, 2025').")
R["LX2a-L01-quotes-1933"] = carried("LX2a-L01-quotes-1933", "L01.html:69-70, :80-85, :88 byte-identical")
R["LX2a-L01-quotes-1934"] = carried("LX2a-L01-quotes-1934", "L01.html:100-111 byte-identical")
R["LX2a-L01-5d"] = carried("LX2a-L01-5d", "L01.html:362 byte-identical")
R["LX2a-L01-6e1-8e"] = carried("LX2a-L01-6e1-8e", "L01.html:362-363, :483 byte-identical")
R["LX2a-L01-headings"] = carried("LX2a-L01-headings", "L01.html:360 byte-identical")
R["LX2a-L01-markup"] = fresh("LX2a-L01-markup",
    f"Re-verified: L01.html:51-109 contains the changed line 65, which adds plain text and no markup; the claim spans on that line are unchanged. The changed quiz option at :585 keeps its data-correct attribute and its label/input/span markup. check_pages LX2 PASS and page_smoke LX2 PASS (round 11, {SCR}out_check_pages_r11.txt, {SCR}out_page_smoke_L01_r11.txt). Lines :359-386, :499-513 and :604 are byte-identical.")
R["LX2a-L01-why-decide"] = carried("LX2a-L01-why-decide", "L01.html:51 byte-identical")
R["LX2a-L01-why-requirements"] = carried("LX2a-L01-why-requirements", "L01.html:51 byte-identical")
R["LX2a-L01-in-effect-attribution"] = carried("LX2a-L01-in-effect-attribution", "L01.html:69 byte-identical")
R["LX2a-L01-readings-para"] = carried("LX2a-L01-readings-para", "L01.html:88 byte-identical")
R["LX2a-L01-exchange-defined"] = carried("LX2a-L01-exchange-defined", "L01.html:63, :96 byte-identical")
R["LX2a-L01-model"] = carried("LX2a-L01-model", "L01.html:113-135 and tests/labs/LX2/lab-LX2-L01-1.py byte-identical")
R["LX2a-L01-lab1-run"] = carried("LX2a-L01-lab1-run", "L01.html:137-315 and the twin byte-identical; run again this round by run_labs (out_run_labs_unit_r11.txt)")
R["LX2a-L01-lab1-hypothesis"] = carried("LX2a-L01-lab1-hypothesis", "L01.html:139 byte-identical")
R["LX2a-L01-lab1-interpretation"] = carried("LX2a-L01-lab1-interpretation", "L01.html:314 byte-identical")
R["LX2a-L01-prop4.1"] = carried("LX2a-L01-prop4.1", "L01.html:320-329 byte-identical")
R["LX2a-L01-prop4.2"] = carried("LX2a-L01-prop4.2", "L01.html:332-341 byte-identical")
R["LX2a-L01-prop4.3"] = carried("LX2a-L01-prop4.3", "L01.html:344-353 byte-identical")
R["LX2a-L01-canon-breaks"] = carried("LX2a-L01-canon-breaks", "L01.html:355-367 byte-identical (the changed option at :585 is the quiz item that cites §5, re-verified under LX2a-L01-quiz)")
R["LX2a-L01-misconceptions"] = carried("LX2a-L01-misconceptions", "L01.html:369-389 byte-identical")
R["LX2a-L01-problems"] = carried("LX2a-L01-problems", "L01.html:391-494 byte-identical")
R["LX2a-L01-key-results"] = carried("LX2a-L01-key-results", "L01.html:499-513 byte-identical")
R["LX2a-L01-quiz"] = fresh("LX2a-L01-quiz",
    "Re-verified the changed option at L01.html:585: 'The model has no state for exemptions, although sections 3 and 4 and section 12(a) refer to exempt securities and transactions' is the one data-correct option. §5 (L01.html:357-365) states 'The model has no exemption' (:360), and the model's state set is the pair (status, listing) of §4 (L01.html:115-122), which has no exemption component, so the option is true. The other two options are not limits of the model in §4 stated in §5. The explanation at :588 lists seven limits: timing, exemptions, independence, emerging growth companies, proceedings, fiscal-year suspension and Assumption A1; §5 has exactly seven bullets (L01.html:359-365). Other items at :517-600 are byte-identical.")
R["LX2a-L01-references"] = carried("LX2a-L01-references", "L01.html:602-606 byte-identical")
R["LX2a-L01-dag"] = fresh("LX2a-L01-dag",
    f"Re-verified against the round-11 delta: the changed lines (:65, :585) add no concept link and no defined term. The concept links in L01 (FC1 exchange-vs-otc, P0.1 evidence-grade, M1 quantifiers) and the two definitions (securities-registration at :74, exchange-act-1934 at :96) are unchanged. check_dag LX2 PASS ({SCR}out_check_dag_r11.txt).")
R["LX2a-L01-hours"] = carried("LX2a-L01-hours", "L01.html:2, :34 byte-identical")
R["LX2a-L01-paraphrase-locators"] = fresh("LX2a-L01-paraphrase-locators",
    "Re-verified: the changed line :65 is the section-number sentence, which carries no claim span and no paraphrase. The paraphrases at :70, :80-85, :96-111, :362-363 and :483 are byte-identical and carry their locators. (Observation, not a row: the paraphrase at :85 of section 8(d) omits the timing clause of the statute's hearing sentence; the quoted words are accurate. Unchanged since round 10.)")
R["LX2a-L01-unspanned-readings"] = carried("LX2a-L01-unspanned-readings", "L01.html:51, :53, :69, :92, :96 byte-identical")
R["LX2a-L01-section-locators"] = fresh("LX2a-L01-section-locators",
    "Re-verified with the enumeration in LX2a-L01-amended: every section number that appears in the claim spans of L01.html:51-111, :359-365 and :483 exists in comps1884.txt or comps1885.txt (sections 2, 2(a)(5), 2(a)(19), 3, 4, 5, 6, 8, 12, 13, 15(d); subsections checked against the text as above). The changed line :65 names only sections already located.")
R["LX2a-L01-section-locators-extra"] = fresh("LX2a-L01-section-locators-extra",
    "Second check, same subject as LX2a-L01-section-locators: the enumeration of section numbers in L01.html (grep -o -i 'sections\\? [0-9]...') lists section 2, 2(a)(5), 2(a)(19), 3, 4, 5(a)-(d), 6(a)-(e)(1), 8(a),(b),(d),(e), 12(a),(b),(d), 13(a), 15(d)(1); all are in comps1884.txt or comps1885.txt at the headings recorded in LX2a-L01-amended. The changed line :65 adds 2(a)(19), which is at comps1884.txt:299.")
R["LX2a-L01-lab1-run-extra"] = carried("LX2a-L01-lab1-run-extra", "L01.html:137-315 byte-identical; run_labs re-run this round")
R["LX2a-L01-structure"] = fresh("LX2a-L01-structure",
    f"Re-verified: L01.html:32-616. Sections §1-§10 in the same order and at the same lines as round 10 (the delta changes only lines 65 and 585, so no heading moves). check_pages LX2 PASS and page_smoke LX2 PASS ({SCR}out_check_pages_r11.txt, {SCR}out_page_smoke_L01_r11.txt).")
R["LX2a-L01-title-1933-1934-extra"] = carried("LX2a-L01-title-1933-1934-extra", "L01.html:6, :35 byte-identical")
R["LX2a-L02-structure"] = fresh("LX2a-L02-structure",
    f"Re-verified: L02.html:32-674. The delta changes one table cell at :575, which keeps its row, grade C and locator. Sections §1-§10 are in the same order and at the same lines. check_pages LX2 PASS ({SCR}out_check_pages_r11.txt); page_smoke LX2 PASS for L02 ({SCR}out_page_smoke_L02_r11.txt).")
R["LX2a-L02-opinion-quotes"] = fresh("LX2a-L02-opinion-quotes",
    "Re-verified: the one quotation changed in this round is the Dirks dissent at L02.html:575 (see LX2a-quote-search). It matches dirks.txt (footnote marker 5 included) and lies on printed page 671. The other opinion quotations in the listed ranges are byte-identical and carry the round-10 evidence (loccheck_r10.py, 58 quotations, 54 located by script and 4 checked by hand).")
R["LX2a-L02-n23-attribution"] = carried("LX2a-L02-n23-attribution", "L02.html:61, :445, :579, :631 byte-identical")
R["LX2a-L02-title-h1"] = carried("LX2a-L02-title-h1", "L02.html:35 and index.html:151, :181 byte-identical")
R["LX2a-L02-lab-run"] = carried("LX2a-L02-lab-run", "L02.html:127-439 and tests/labs/LX2/lab-LX2-L02-1.py byte-identical; run_labs re-run this round")
R["LX2a-L02-lab-output"] = carried("LX2a-L02-lab-output", "L02.html:413-437 and twin lines 226-283 byte-identical")
R["LX2a-L02-classical-element"] = carried("LX2a-L02-classical-element", "L02.html:73, :459, :473 byte-identical")
R["LX2a-L02-hypothesis"] = carried("LX2a-L02-hypothesis", "L02.html:129 byte-identical")
R["LX2a-L02-example-3.2"] = carried("LX2a-L02-example-3.2", "L02.html:92-94 byte-identical")
R["LX2a-L02-example-2.2-4.2"] = carried("LX2a-L02-example-2.2-4.2", "L02.html:72-74, :111-113 byte-identical")
R["LX2a-L02-canon-breaks"] = carried("LX2a-L02-canon-breaks", "L02.html:442-451 byte-identical")
R["LX2a-L02-interpretation"] = carried("LX2a-L02-interpretation", "L02.html:438 byte-identical")
R["LX2a-L02-misconceptions"] = carried("LX2a-L02-misconceptions", "L02.html:453-461 byte-identical")
R["LX2a-L02-problems"] = carried("LX2a-L02-problems", "L02.html:463-566 byte-identical (the changed table row at :575 is in the key results, not here)")
R["LX2a-L02-pr1-A2"] = carried("LX2a-L02-pr1-A2", "L02.html:83-86, :496-498 byte-identical")
R["LX2a-L02-markup"] = carried("LX2a-L02-markup", "L02.html:53, :84, :92, :541, :548, :599, :608, :617 byte-identical")
R["LX2a-L02-E2-E3-scratch"] = carried("LX2a-L02-E2-E3-scratch", "L02.html:526-539 byte-identical")
R["LX2a-L02-key-results"] = fresh("LX2a-L02-key-results",
    f"Re-verified: L02.html:568-583 contains the changed cell at :575. The row keeps grade C and the locator 'gpo1983dirks p. 660; dissent gpo1983dirks p. 671'. Its statement 'A tippee assumes the insider's duty only when the insider breached and the tippee knows or should know of the breach' is the majority's test (p. 660, unchanged); the dissent quotation supports the after-the-fact liability clause (p. 671, verified). Other key-result rows are byte-identical.")
R["LX2a-L02-quiz"] = carried("LX2a-L02-quiz", "L02.html:585-657 byte-identical")
R["LX2a-L02-dag"] = carried("LX2a-L02-dag", "L02.html:37, :56, :66, :80, :103 byte-identical")
R["LX2a-L02-B3-B1"] = fresh("LX2a-L02-B3-B1",
    "Re-verified with a fresh grep this round (ledgers/LX2/scripts/LX2-a-r11/out_banned_and_cards_r11.txt): grep -n 'Texas|Gulf|Dodd|MiFID' L02.html returns one line, L02.html:668, the next-lesson navigation link 'Manipulation, Dodd–Frank and MiFID II' (the title of L03, L03.html:35). It is a link label, not a statement of content, and L02 states no provision of either text. No Texas Gulf Sulphur content. Round 10 recorded 'no match' for this grep, which missed the nav label; the row is PASS because the label is navigation, not content. Observation for the slice-b verifier: the L03 title names Dodd–Frank and MiFID II, while cards LX2-c055 to c057 that said the lesson states nothing about them are removed in this round.",
    location="course/modules/LX/LX2/L02.html (whole page; the one hit is :668); index.html:171")
R["LX2a-L02-years"] = fresh("LX2a-L02-years",
    "Re-verified: the changed cell at L02.html:575 contains no four-digit year (its locator is 'gpo1983dirks p. 671'). Grep of L02.html prose outside <pre> and <script> returns only the Act name 'Securities Exchange Act of 1934' (linked to L01). No year is printed for Dirks or O'Hagan.")
R["LX2a-L02-why"] = carried("LX2a-L02-why", "L02.html:51 byte-identical")
R["LX2a-L02-tippee-definition"] = carried("LX2a-L02-tippee-definition", "L02.html:76-77 byte-identical")
R["LX2a-L02-page-locators"] = fresh("LX2a-L02-page-locators",
    "Re-verified including the changed cell: the locator of the changed row (L02.html:575, dissent gpo1983dirks p. 671) is the page on which the passage prints (pdftotext of USREPORTS-463-646.pdf, see LX2a-quote-search). The round-10 check of all other claim-span locators (loccheck_r10.py; decision rows 425-432 against the twin's BRANCH_RULE and Check locators) is carried, the lines being byte-identical.")
R["LX2a-L02-scienter-composite"] = carried("LX2a-L02-scienter-composite", "L02.html:437, :445, :579 byte-identical")
R["LX2a-scope-note"] = carried("LX2a-scope-note", "index.html:33; L01.html:53; L02.html:53 byte-identical")
R["LX2a-notation"] = fresh("LX2a-notation",
    "Re-verified against the round-11 delta: the changed text (L01.html:65, :585; L02.html:575) adds no mathematical symbol; '2(a)(19)' is a section label and the quote contains no symbol. The symbols and macros of L01.html:115-352 are byte-identical; notation/notation.json is unchanged. Registry flag carried (\\blacksquare, see registry_flags).")
R["LX2a-L02-M3-scratch"] = carried("LX2a-L02-M3-scratch", "L02.html:483-489 byte-identical")
R["LX2a-registry-keys"] = carried("LX2a-registry-keys", "references/references.json (LX2 keys) byte-identical; verify_refs re-run this round (offline 0 problems; live LX2 0 problems)")
R["LX2a-counter-evidence"] = carried("LX2a-counter-evidence", "L02.html:90, :109 byte-identical")
R["LX2a-lab-assumptions"] = carried("LX2a-lab-assumptions", "L02.html:83-86, :119-125, :127-129 and the twin byte-identical")
R["LX2a-L02-remark-3.3"] = carried("LX2a-L02-remark-3.3", "L02.html:97 byte-identical")
R["LX2a-r8-delta"] = carried("LX2a-r8-delta", "historical delta (06994db1..0dee921a); superseded")
R["LX2a-r9-delta"] = carried("LX2a-r9-delta", "historical delta (0dee921a..c93dd52); superseded by the round-10 and round-11 deltas")
R["LX2a-r10-delta"] = carried("LX2a-r10-delta", "historical delta (c93dd52..00a84795); superseded by LX2a-r11-delta")
R["LX2a-card-c010"] = carried("LX2a-card-c010", "cards.json LX2-c010 byte-identical since 00a84795 (cards delta lists c002, c004, c005, c023, c049, c053, c055-c057, c082, c086, c090-c092 only)")
R["LX2a-card-c016"] = carried("LX2a-card-c016", "cards.json LX2-c016 byte-identical since 00a84795")
R["LX2a-cards-L01-other"] = fresh("LX2a-cards-L01-other",
    "Re-verified this round: all 32 L01 cards (cards.json, lesson 'L01': LX2-c001 to c027, c090 to c092, c095, c096) read in full; 7 changed cards re-checked against the current L01 text: c002 ('Definition 3.1' at L01.html:95, 'In Lesson 1' is a rewording of 'In this lesson', sections 12, 13, 15(d) at :96); c004 (L01.html:69 'taken effect under section 8(a) and ... not been suspended under section 8(d)'; 'the definitions in section 2 do not define the phrase'; 'test the status, not the document itself' at :69); c005 (L01.html:96 'the lesson does not define it further'); c023 (state table in the printed lab output, L01.html:280-289: sale yes only for effective with not_listed and effective with listed; R5a at :129); c090, c091, c092 (printed lines 'reachable from unregistered/not_listed: 10 of 10', 'states where both reporting duties apply: 0', 'states where a sale is permitted and an offer is not: 0' at L01.html:277, :289, :290, equal to the lab output). Cards c010 and c016 are PASS as in round 10 (byte-identical).")
R["LX2a-cards-L02"] = carried("LX2a-cards-L02", "cards.json lesson 'L02' (19 cards) byte-identical since 00a84795; the round-11 cards delta has no L02 card")
R["LX2a-cards-dup"] = fresh("LX2a-cards-dup",
    "Re-run this round (python over course/modules/LX/LX2/cards.json): 97 cards (L01 32, L02 19, L03 19, L04 27), 0 duplicate ids, 0 duplicate fronts (case-insensitive). Round 10 recorded 100 cards; the delta removes LX2-c055, c056 and c057 and adds none. Output: ledgers/LX2/scripts/LX2-a-r11/out_banned_and_cards_r11.txt (script banned_and_cards_r11.sh).")
R["LX2a-r9-quotes-L02"] = fresh("LX2a-r9-quotes-L02",
    "Re-verified: the one quotation changed in round 11 (L02.html:575) is located on its printed page (p. 671) in dirks.txt; the other quotations with a gpo key were located in round 10 (loccheck_r10.py, out_loccheck_L02_r10.txt) and their lines are byte-identical since 00a84795.")
R["LX2a-r9-sources"] = fresh("LX2a-r9-sources",
    f"Re-run round 11: shasum -a 256 of /tmp/lx2a_r10_dl_1793865981 files: COMPS-1884.pdf c67e5535..., COMPS-1885.pdf c7a620b6..., USREPORTS-463-646.pdf cfc001ed..., USREPORTS-521-642.pdf 72db2418...; comps1884.txt eaf8af1a..., comps1885.txt ee89b02d..., dirks.txt d295f808..., ohagan.txt 90d1f156.... These equal ledgers/LX2/scripts/LX2-a-r10/out_sha256_sources_r10.txt line for line. The sources are the same bytes as in rounds 9 and 10. The extracts were fetched by plain curl in round 9 (fetch_sources.sh); no access barrier was met in round 11, and no network fetch was repeated.")
R["LX2a-L02-E3-delta"] = carried("LX2a-L02-E3-delta", "L02.html:533-539 and tests/labs/LX2/lab-LX2-L02-1.py byte-identical")

R["LX2a-r11-delta"] = {"id": "LX2a-r11-delta", "check": "2.9 round 11 delta (00a84795..11d7077) for slice a",
    "location": DELTA,
    "status": "PASS",
    "evidence": "git diff 00a84795 11d7077 -- course/modules/LX/LX2 tests/labs/LX2: 4 files changed. index.html:148 ('Each lesson page has the same main parts', replacing 'same structure') and :161 ('The model case is SIMULATED.', replacing 'Every number is from simulated data.'); L01.html:65 (adds 2(a)(19) to the section list; verified in LX2a-L01-amended); L01.html:585 ('no state for exemptions', verified in LX2a-L01-quiz); L02.html:575 (dissent quotation now complete; verified in LX2a-quote-search); cards.json: LX2-c002, c004, c005, c023, c090, c091, c092 (L01; verified in LX2a-cards-L01-other), c049 and c053 (L03), c082 and c086 (L04), and c055-c057 removed (L03), which are outside slice a and are for the slice-b verifier. tests/labs/LX2/*.py byte-identical. Every hunk in slice a was read and checked."}

rows = []
missing=[rid for rid in old if rid not in R]
assert not missing, missing
for rid in old:
    rows.append(R[rid])
for rid, r in R.items():
    if rid not in old:
        rows.append(r)

fails = [r["id"] for r in rows if r["status"] != "PASS"]
frag = {
    "unit": "LX2",
    "slice": "LX2-a",
    "round": 11,
    "verifier": "Haiku independent verifier, LX2-a round 11 (did not build LX2; builder ledgers and scratch not read). Delta verification from the round-10 pin with full re-run of every command row at the pin; every hunk of the round-11 delta in slice a read; every round-10 non-PASS row (LX2a-L01-amended) re-verified from scratch; every row whose cited subject changed re-verified.",
    "pin": "11d7077a290f7960b183d3a5a6631af4773888f9",
    "base": "00a84795f276456fce19d4181373cc4efba11a36",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE11-LX2-a",
    "scratch": "/tmp/lx2a_r10_dl_1793865981 (round-10 primary-source bytes, hash-checked this round); /tmp/lx2_dirks_r11.txt (pdftotext of USREPORTS-463-646.pdf); /tmp/lx2a_r11_twin_* (twin runs)",
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "verdict": "PASS" if not fails else "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [
        "references/references.json key gpo1983dirks: title field reads 'Dirks v. SEC, 463 U.S. 646 (1982)' and year field reads 1983 (references.json:10823-10835). GovInfo USREPORTS-463-646 details: decided July 1, 1983. No slice-a page prints a year for Dirks. The architect corrects the record through add_reference.py.",
        "notation/notation.json does not register \\blacksquare, the proof-end mark used on L01.html (three uses) and on other course pages. Recorded as a registry flag: a typesetting mark, not a symbol with a meaning. The architect decides whether to register it.",
        "No registry key or source string exists for Dodd-Frank, MiFID II or Texas Gulf Sulphur (grep, references/references.json). L02 and the hub say so; the REFERENCE_REQUESTS stay open. The L03 title (L03.html:35) and the L02 next-lesson link (L02.html:668) name Dodd-Frank and MiFID II; this is for the slice-b verifier."
    ],
    "freshness_flags": [],
    "notes": "Round 11 at pin 11d7077 (delta from 00a84795). Delta in slice a: index.html:148, :161; L01.html:65, :585; L02.html:575; cards.json L01 cards c002, c004, c005, c023, c090-c092 (other cards in the file are outside slice a: L03 c049, c053, c055-c057; L04 c082, c086). Twins tests/labs/LX2/lab-LX2-L01-1.py and lab-LX2-L02-1.py are byte-identical since 00a84795. The round-10 FAIL LX2a-L01-amended is PASS. Observations, not rows: (1) L01.html:85 paraphrases 8(d) without the statute's timing clause (quoted words accurate; unchanged since round 10). (2) The round-10 'no Dodd-Frank/MiFID' grep of L02 missed the next-lesson link at L02.html:668; the link is navigation, so LX2a-L02-B3-B1 stays PASS. (3) The registry now holds 97 cards, not 100 (round 10 count). (4) Labs are demonstrations; no mutants are required for this slice (VERIFIER 2.6 applies to project graders only). Commands run this round are in ledgers/LX2/scripts/LX2-a-r11/ (out_*_r11.txt, twin_isolated_r11.sh, write_fragment_r11.py).",
    "summary": f"Slice LX2-a round 11 verdict {'PASS' if not fails else 'FAIL'} at 11d7077. {len(rows)} rows: PASS {sum(1 for r in rows if r['status']=='PASS')}, FAIL {sum(1 for r in rows if r['status']=='FAIL')}, UNVERIFIABLE {sum(1 for r in rows if r['status']=='UNVERIFIABLE')}. The round-10 FAIL LX2a-L01-amended is cured (L01.html:65 now lists 2(a)(19)); every command row re-run this round."
}
OUT.write_text(json.dumps(frag, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("rows", len(rows), "fails", fails)
