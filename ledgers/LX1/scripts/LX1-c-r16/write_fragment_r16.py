"""Round-16 LX1-c verifier: writes ledgers/LX1/LX1-c.json from the round-16 outputs (out/) and the mutant files.

Usage: python -I write_fragment_r16.py <checkout_root> <round15_fragment.json>
Every row's evidence names the command or script and the out/ file that backs it. Mutant killers are read from
out/kill_all_r16.out (intact-snapshot harness) and out/damaged_candidates_r16.out (damaged-snapshot differential).
"""
import json
import pathlib
import sys

ROOT = pathlib.Path(sys.argv[1]).resolve()
PREV = json.loads(pathlib.Path(sys.argv[2]).read_text(encoding="utf-8"))
OUT = ROOT / "ledgers/LX1/scripts/LX1-c-r16/out"
MUT = ROOT / "ledgers/LX1/mutants"
S = "ledgers/LX1/scripts/LX1-c-r16/"
def carry(files):
    return f"Carried from round 15 ({files} byte-identical since the previous pin d1e65a0): "


def row(rid, check, location, status, evidence, fix=None):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    return r


rows = [
    row("proj-rung1-step3-rounding-claim", "2.5-labs", "course/modules/LX/LX1/project.html:177",
        "PASS", f"Fresh. {S}out/rederive_r16.out: falling real debt at t=5 is 117647.06; exact 10000000/0.85 cents = "
        "11764705.882 (page_checks_r16.out prints line 177 for '11764705.882'). Twin output (out/twins.out from harness "
        "twins) equals the expected block."),
    row("proj-real-value-vs-lesson2", "2.9-prose",
        "course/modules/LX/LX1/project.html:56, :58; course/modules/LX/LX1/L02.html:83-92, :110, :127-128", "PASS",
        "Fresh read of project.html:56-58 this round. L02.html is byte-identical since d1e65a0 (not in the r15->r16 "
        "delta); L02:83-92 Proposition 2.1 with (A2) and (A3); :127-128 Remark 3.3 (carried from round 15 for L02)."),
    row("proj-manifest-note-misattributed", "2.2-numbers",
        "course/modules/LX/LX1/project.html:271, :279, :293; course/assets/data/market/MANIFEST.json (fx_monthly)",
        "PASS", f"Fresh. {S}out/data_checks_r16.out prints the fx_monthly MANIFEST title ('Month-end foreign exchange "
        "rates, ten currencies, USD per unit of foreign currency'), 669 rows, first 1971-01, last 2026-09, retrieved "
        "2026-10-19, and the transform text; the page statements at :271, :279, :293 match."),
    row("proj-lab3-citation-string", "2.9-prose", "course/modules/LX/LX1/project.html:279, :287; MANIFEST.json "
        "fx_monthly citation", "PASS", "Fresh. The MANIFEST citation equals the citation at :279, the Lab 3 "
        "hypothesis at :287 and the twin docstring (lab-LX1-project-3.py lines 1-20)."),
    row("proj-reading-reinhart-registry", "2.9-prose", "course/modules/LX/LX1/project.html:633-640; "
        "references/references.json", "PASS", "Fresh. Reading list (:637-639) holds friedman1963monetary, "
        "eichengreen1992golden, garber2000famous; registry entries each status 'verified', used_by ['LX1']. "
        "references/ unchanged since d1e65a0. verify_refs --unit LX1 (live) and --offline: out/verify_refs_*_r16.out."),
    row("proj-spec-current-undefined", "2.9-prose", "course/modules/LX/LX1/project.html:446 (brief item 1), :62, "
        ":300-301", "PASS", "Fresh. :62 (changed this round) defines window three as the twelve months to the last "
        "month of the embedded snapshot; :446 defines a current condition as dated within the twelve months ending at "
        "the last month of the data, 2025-10 to 2026-09 for the snapshot. rederive_r16.out: window three 12 changes."),
    row("proj-exemplar-A-condition", "2.6-rubric", "course/modules/LX/LX1/project.html:497, :519", "PASS",
        "Fresh. :497 names window three, 2025-10 to 2026-09, and the MANIFEST last month 2026-09, retrieved "
        "2026-10-19 (MANIFEST fx_monthly). rederive_r16.out window three: 12 changes, 1.90 percent per month."),
    row("proj-gate-commands", "2.9-prose", f"{S}out/",
        "PASS", "Fresh, all on 56cc575 with .venv (Python 3.14): check_pages_LX1 PASS (check_pages.out); check_dag "
        "PASS (check_dag.out); check_projects PASS (check_projects.out); run_labs --unit LX1 7/7 PASS "
        "(run_labs_LX1.out); run_labs --page project 3/3 PASS (run_labs_project.out); page_smoke --pages project PASS "
        "(page_smoke_project.out); ruff check and format --check tests/labs/LX1 (ruff_check_labs.out, "
        "ruff_format_labs.out); mypy --no-incremental: no issues in 385 files (mypy_full.out); pytest test_labs, "
        "test_run_labs, test_page_smoke, test_page_checks, test_curriculum: rc 0 (pytest_relevant.out); pytest "
        "test_refs rc 0 (pytest_refs.out); verify_refs --offline 560 entries 0 problems (verify_refs_offline.out); "
        "verify_refs --unit LX1 live 4 of 560, 0 problems (verify_refs_unit_LX1_online.out); fetch_data --check 3 "
        "datasets 0 problems (fetch_data_check.out); build_site --check current (build_site_check.out); "
        "mutate_graders and run_graders --unit LX1: no autograder, rc 0. Not run: render_curriculum --check and "
        "--all forms of check_pages/run_labs (outside this slice; no curriculum or other unit file changed)."),
    row("proj-lab1-twin-run", "2.5-labs", "course/modules/LX/LX1/project.html:77-149; "
        "tests/labs/LX1/lab-LX1-project-1.py", "PASS", "Fresh. harness.py twins (out/twins.out): page code equals "
        "the twin line for line (0 differing lines); twin under python -I -W error: rc 0, stderr 0 bytes, stdout equals "
        "the expected block (20 lines). page_smoke lab time 0.0 s."),
    row("proj-lab1-numbers", "2.2-numbers", "course/modules/LX/LX1/project.html:77, :150-171", "PASS",
        "Fresh. rederive_r16.out (Decimal, no lab code): falling 100000.00 ... 117647.06; rising ... 86956.52; burden "
        "17.65 and -13.04; difference 30690.54. Identical to the page expected block."),
    row("proj-lab2-twin-run", "2.5-labs", "course/modules/LX/LX1/project.html:184-258; "
        "tests/labs/LX1/lab-LX1-project-2.py", "PASS", "Fresh. twins.out: page differs from the twin only on the two "
        "'___' lines; twin rc 0, stderr 0 bytes, stdout equals the expected block (10 lines)."),
    row("proj-lab2-numbers", "2.2-numbers", "course/modules/LX/LX1/project.html:184, :247-256", "PASS",
        "Fresh. rederive_r16.out: real debt 40000.00, 40404.04, 40816.33, 41666.67, 42105.26, 43010.75; burden exact "
        "7.526882, prints 7.53."),
    row("proj-lab2-check-claims", "2.5-labs", "course/modules/LX/LX1/project.html:257", "PASS",
        "Fresh. 'leaves out the division prints 40000.00 in every period' is mutant lx1c_m01 (killed, kill_all_r16.out); "
        "'inverts the ratio prints -7.00' is lx1c_m02 (killed) and rederive_r16.out 'LAB2 burden ratio inverted: -7.00'."),
    row("proj-lab3-twin-run", "2.5-labs", "course/modules/LX/LX1/project.html:287-437; "
        "tests/labs/LX1/lab-LX1-project-3.py", "PASS", "Fresh. twins.out (r16): page code equals the twin line for "
        "line (0 differing lines, docstring line 22 changed this round and mirrored at page :309); twin run in a scratch "
        "directory holding data/fx_monthly.csv: rc 0, stderr 0 bytes, stdout equals the expected block (20 lines). "
        "The agreement check's own status is the separate FAIL row proj-lab3-raise-claims-untested."),
    row("proj-lab3-numbers", "2.2-numbers", "course/modules/LX/LX1/project.html:287, :411-437", "PASS",
        "Fresh. rederive_r16.out: changes 668/321/12; exact zeros 3/2/0; sd 2.79352779/2.46995014/1.90201858, printed "
        "2.79/2.47/1.90; ratio 0.884168808 -> 0.88; difference 0.323577653 -> 0.32; largest by size 13.58 (1985-03), "
        "-9.66 (2008-10), 2.96 (2026-04). All equal the expected block."),
    row("proj-lab3-L04-cross-check", "2.9-prose", "course/modules/LX/LX1/L04.html:312-318; "
        "course/modules/LX/LX1/project.html:284", "PASS", carry("course/modules/LX/LX1/L04.html") + "L04.html is outside the r15->r16 delta; project.html:284 unchanged). "
        "rederive_r16.out gives sd 0.027935 and 0.024700 (6 dp), changes 668 and 321, as L04's expected block prints; "
        "project.html:284 unchanged."),
    row("proj-lab3-docstring-claims", "2.9-prose", "course/modules/LX/LX1/project.html:288-315 (twin docstring "
        "mirrored); tests/labs/LX1/lab-LX1-project-3.py load_column, month_index", "PASS",
        f"Fresh. {S}out/damaged_candidates_r16.out (TWIN rows): the twin raises ValueError on a blank, 'n/a', '1.2e0' and "
        "'-1.2' GBP cell, on a dropped month (2000-07 does not follow 2000-05) and on a duplicated month; no row is "
        "skipped or filled. The raise statement at :309 is the one the twin implements. The agreement sentence at "
        ":308-309 is not covered here (see proj-lab3-raise-claims-untested)."),
    row("proj-lab3-interpretation-claims", "2.5-labs", "course/modules/LX/LX1/project.html:438; "
        "course/modules/LX/LX1/L04.html:84-94 (Definition 2.1, (A2); Proposition 2.2(a))", "PASS",
        "Fresh. L04.html:84-86 Definition 2.1 (fixed-exchange-rate model) with (A2); L04 Proposition 2.2(a) gives zero "
        "change under (A2). :438 is conditional on (A2); window two shows 2 zero changes against 321 changes "
        "(rederive_r16.out)."),
    row("proj-lab3-difference-line-r5", "2.2-numbers", "course/modules/LX/LX1/project.html:287, :411, :436, :438; "
        "tests/labs/LX1/lab-LX1-project-3.py (main, difference line)", "PASS",
        "Fresh. Twin main(): difference = show(100 * (sd_one - sd_two), 2) from unrounded sds; rederive_r16.out "
        "unrounded 0.323577653 -> 0.32."),
    row("proj-lab-simulated-labels", "2.8-data", "course/modules/LX/LX1/project.html:42, :77, :80, :184, :187 (code "
        "docstrings), :283-287 (Lab 3 section)", "PASS", "Fresh. Labs 1 and 2 carry SIMULATED in hypothesis lines and "
        "code docstrings; Lab 3 names its dataset, source and retrieval date and its licence is quoted at :279. "
        "Lines 42-80 and 184-187 unchanged this round."),
    row("proj-data-licence-quote", "2.8-data", "course/modules/LX/LX1/project.html:279; "
        "https://www.federalreserve.gov/disclaimer.htm (plain curl)", "PASS", "Fresh. curl -sS -L (out/curl_licence_r16.out): "
        "HTTP 200, saved as out/licence_page_r16.html; page text: 'Unless otherwise indicated, information on Board's "
        "website is in the public domain and may be copied and distributed without permission. Please cite to the Board "
        "as the source of the information.' Grants redistribution; matches MANIFEST licence and :279."),
    row("proj-data-snapshot-rebuild", "2.8-data", "course/assets/data/market/fx_monthly.csv; "
        "course/assets/data/market/MANIFEST.json (fx_monthly)", "PASS", carry("course/assets/data/market/ and MANIFEST.json, checked this round by git diff and sha256") + "Round 15 rebuilt fx_monthly from the live feed (fetch_data --fetch) "
        "byte-identical, sha256 60572240d1a9d1832d5021297634b2369723b94098414948b891dd26a8bffe3e; re-checked this round: "
        "sha256sum of fx_monthly.csv = the MANIFEST sha256; fetch_data --check 3 datasets 0 problems (fetch_data_check.out)."),
    row("proj-data-fields", "2.8-data", "course/modules/LX/LX1/project.html:271, :279-280, :293; "
        "course/assets/data/market/fx_monthly.csv", "PASS", "Fresh. data_checks_r16.out: header month, AUD, CAD, CHF, "
        "DKK, EUR, GBP, JPY, NOK, NZD, SEK; EUR blank in 336 rows, 1971-01 to 1998-12, first non-blank 1999-01; GBP "
        "blank cells 0; 669 months, contiguous; no interest-rate column."),
    row("proj-data-no-other-series", "2.8-data", "course/modules/LX/LX1/project.html:280 (sentence changed this round); "
        "course/assets/data/market/MANIFEST.json", "PASS", "Fresh. :280 names fx_daily, fx_monthly and ust_daily; "
        "MANIFEST datasets are exactly these three (fetch_data_check.out: 3 datasets). The three titles: FX daily, FX "
        "month-end, 3-month bill and 10-year yields: none is gold, price-level, output, unemployment or bank-failure. "
        "The universal sentence that was here at round 15 is removed (see proj-data-embedded-claim)."),
    row("proj-spec-ladder", "2.6-spec", "course/modules/LX/LX1/project.html:40-48, :72-258, :261-275, :277-441, "
        ":443-453, :471-631", "PASS", "Fresh. Ladder order: rung 1 worked example (Lab 1), rung 2 completion "
        "(Lab 2, class 'lab completion', two blanks), rung 3 spec, data, Lab 3, brief, rubric, rung 4 stretch. "
        "check_projects_LX1 PASS (check_projects.out). :46 changed (link to the data section) and checked."),
    row("proj-spec-curriculum-scope", "2.6-spec", "curriculum/06-profession-capstone.yaml:42-49; "
        "course/modules/LX/LX1/project.html:443-453", "PASS", "Fresh. curriculum/06 unchanged since d1e65a0; brief "
        "items at :446-452 cover the curriculum's brief and deliverable (two-page essay, every claim cited) and its "
        "rubric."),
    row("proj-hours", "2.6-hours", "course/modules/LX/LX1/project.html:33 (eyebrow), :457-467 (table#hours); "
        "course/modules/LX/LX1/index.html:29", "PASS", "Fresh. Table 1 + 1 + 2 + 1.5 + 2.5 + 2 = 10 = "
        "data-hours-project (index.html:29) and the eyebrow '10 hours'. Verifier estimate unchanged from round 15: "
        "about 10.5 to 11.5 h, inside 30 percent of 10."),
    row("proj-rubric-observable", "2.6-rubric", "course/modules/LX/LX1/project.html:479-483 (rubric rows, changed "
        "cells at :481 and :482)", "PASS", "Fresh. Every level cell names a checkable element: dates and locators (C1), "
        "chain steps and the failure step with evidence (C2), citation, locator and counter-evidence (C3), unrounded "
        "values, rule, formula, base and sign (C4), limits and tests (C5). 'Picks two events', 'Lists similarities' and "
        "'Mentions a caveat without naming what it limits' are countable. The count wording in C5 is a separate FAIL "
        "(proj-rubric-c5-count-wording)."),
    row("proj-calibration-exemplars", "2.6-rubric", "course/modules/LX/LX1/project.html:491-616 (exemplar memo prose); "
        f"{S}blind_extract_r16.py; out/blind_prose_r16.txt", "UNVERIFIABLE",
        f"Prose-only extraction (ruling 15) in {S}out/blind_prose_r16.txt. Prose-only scores by the rubric "
        "descriptors: Exemplar A C1 4, C2 4, C3 4, C4 4, C5 3 (official 4,4,4,4,3); Exemplar B C1 2, C2 2, C3 1, C4 2, "
        "C5 1 (official 2,2,1,2,1). All within one level. BLIND CONDITION NOT MET: this verifier read the annotations "
        "(:501-616) and verdict lines (:493, :555) and the annotation text of the changed hunks (:534, :588) before the "
        "extraction, so the scores are not blind. The same condition failed in round 15.",
        "Re-run in a fresh verifier: run blind_extract_r16.py first, score exemplar prose by the rubric descriptors "
        "only, record the scores, and only then read :493, :555 and the annotations."),
    row("proj-exemplar-numbers", "2.2-numbers", "course/modules/LX/LX1/project.html:530 (A numbers), :584 (B numbers), "
        ":588 (B annotation, changed)", "PASS", "Fresh. A: 17.65 (Lab 1 Part B), 2.47, 2.79, 1.90, ratio 0.88 from "
        "unrounded 0.884169 (rederive_r16.out). B: 2.47/2.79 = 0.8853 -> 0.89; fall 11.47 percent 'about 11 percent' "
        "from rounded inputs; from unrounded 0.884169 the fall is 11.58 percent, 'about 12' (B annotation at :588, "
        "corrected this round, consistent)."),
    row("proj-reading-keys", "2.9-prose", "course/modules/LX/LX1/project.html:635-640; references/references.json",
        "PASS", "Fresh. Keys exist in references.json with used_by ['LX1']; Eichengreen title 'Golden fetters: the gold "
        "standard and the Great Depression, 1919-1939', year 1992 (matches :497 and :555 period claim)."),
    row("proj-notation", "2.9-prose", "course/modules/LX/LX1/project.html (inline TeX spans); notation/notation.json",
        "PASS", f"Fresh. {S}out/page_checks_r16.out: 30 spans, symbols D, P_t, P_0, S_m, V_t, ln, m, n, t. notation.json "
        "unchanged since d1e65a0 and registers T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, Q: no collision."),
    row("proj-scope-words", "2.9-prose", "course/modules/LX/LX1/project.html:62, :280, :438, :473, :481, :482, :519, "
        ":541 (changed lines); page_checks_r16.out", "PASS", "Fresh scan of the changed lines. ':62' window three "
        "defined; ':280' universal 'None of the three' verified against MANIFEST titles; ':473' 'no level describes' "
        "is a total rule (0); ':481', ':482' 'Every' claims and percent changes are checkable by a rater; ':541' "
        "'every factual claim above carries its locator' checked against each claim of Exemplar A (Lesson 2, Lesson 4, "
        "MANIFEST, Lab 1 and Lab 3 locators)."),
    row("proj-process-words", "2.9-prose", "course/modules/LX/LX1/project.html (rendered prose); page_checks_r16.out",
        "PASS", "Fresh scan: build, builder, verif*, agent, REQUESTS, unit report, fixer, Claude, TODO, TBD: 0 hits. "
        "'round' occurs only as rounding."),
    row("proj-links-anchors", "2.9-prose", "course/modules/LX/LX1/project.html (href and id); page_checks_r16.out; "
        "course/modules/LX/LX1/index.html (id placement)", "PASS", "Fresh. In-page hash hrefs brief, data, main, "
        "rubric-section, self-assessment, spec, stretch resolve (missing []). The placement link resolves to index.html "
        "id 'placement' (data-mastery 0.8). check_pages_LX1 PASS."),
    row("proj-page-smoke", "2.9-prose", "course/modules/LX/LX1/project.html; out/page_smoke_project.out", "PASS",
        "Fresh. page_smoke --unit LX1 --pages project: PASS; 3 labs run; boot 1.1 s; each lab 0.0 s (under 10 s)."),
    row("proj-atlas-autograder-na", "2.6-spec", "curriculum/06-profession-capstone.yaml:11, :49, :86 (grading: "
        "rubric); plans/LX1-build-plan.md section 8", "PASS", "Fresh. Grading is 'rubric' (curriculum/06 lines 11, 49, "
        "86); no grader directory (run_graders: 'no autograder'); no atlas milestone for LX1 (plan section 8)."),
    row("proj-mutants-student-errors", "2.6-mutation", "ledgers/LX1/mutants/ (71 files); "
        f"{S}out/kill_all_r16.out; {S}out/damaged_candidates_r16.out", "PASS",
        "Lab mutants only (LX1 has no grader). Re-ran all 71 with harness.py cands and damaged_r16.py: 70 killed; "
        "the one survivor r13n03 (agreement check removed) is the open case of proj-lab3-raise-claims-untested, not "
        "an unlisted survivor. New this round: r16n01 (divides by the square of P, killed by expected block), r16n02 "
        "(burden starts at period 1, killed by expected block), r16n03 (standard error reported as the dispersion, "
        "killed by the lab's own agreement ValueError on the intact snapshot)."),
    row("proj-alternatives", "2.6-mutation", f"{S}alts/ (copies of the round-15 alternatives, re-run); out/alts_r16.out",
        "PASS", "Three correct alternatives for Lab 3 (log-difference, statistics.variance, Decimal rounding) and for "
        "Labs 1 and 2 re-run through harness.py cands: all three SURVIVED (stdout equals expected block, rc 0), as "
        "correct implementations must."),
    row("proj-exemplar-b-annotations-vs-descriptors", "2.6-rubric", "course/modules/LX/LX1/project.html:553-616 "
        "(exemplar B passages and annotations)", "PASS", "Fresh. Each B annotation checked against the descriptors: C1 L2 "
        "(condition has no date), C3 L1 (sources listed), C3 L2 miss (three uncited claims at :559, :596), C4 L2 (rounds "
        "inputs at :584), C4 L3 miss, C2 L2 (similarity and difference, no chain), C5 L1 (caveat, no limit named). "
        "Official 2,2,1,2,1 consistent with the descriptors."),
    row("proj-brief-rubric-escape-clauses", "2.6-rubric", "course/modules/LX/LX1/project.html:449 (brief item 4), :265, "
        ":481 (C3 L4 and L3, changed)", "PASS", "Fresh. Brief item 4 'names its counter-evidence, or the essay states "
        "that it makes no such claim' matches C3 L4 and L3; the escape clause is present in both."),
    row("proj-exemplar-locators", "2.6-rubric", "course/modules/LX/LX1/project.html:497, :508, :519, :530, :541; "
        "course/modules/LX/LX1/L02.html; L04.html", "PASS", "Fresh. Locators in Exemplar A: Eichengreen title field; "
        "MANIFEST last field; Lesson 2 Proposition 2.1(a) and Remark 3.3; Lab 1 Part B; Lab 3 lines; Lesson 4 Section 4 "
        "item 'Exchange rates only' (L04.html:333). Each resolves to the cited text."),
    row("proj-exemplar-a-c5-limit-count", "2.6-rubric", "course/modules/LX/LX1/project.html:491, :541, :546-547",
        "PASS", "Fresh. Exemplar A names three limits; limit one has a test (the interest-rate series); limits two and "
        "three name none. Under the 'at least' reading of C5 L3 this is level 3, the official score. The wording that "
        "makes this reading necessary is a separate FAIL (proj-rubric-c5-count-wording)."),
    row("proj-round11-delta-project-page", "2.9-prose", "course/modules/LX/LX1/project.html:62, :480, :541", "PASS",
        "Fresh. :62 and :541 re-read this round (changed); :480 (C2 row) unchanged since round 14 and re-read."),
    row("proj-spec-limits-test-each", "2.6-spec", "course/modules/LX/LX1/project.html:269, :449, :483, :491, :547",
        "PASS", "Fresh. The brief asks for two limits with a test for at least one; C5 L4 requires a test for each; the "
        "exemplar at :547 misses L4 accordingly."),
    row("proj-notation-n-undefined", "2.9-prose", "course/modules/LX/LX1/project.html:60, :438; "
        "tests/labs/LX1/lab-LX1-project-3.py", "PASS", "The symbol n (sample size in the n - 1 denominator) is not "
        "defined in words on the page. It is the standard sample-size symbol of the sample standard deviation formula, "
        "it is not registered in notation.json (no collision), and the lab computes it as the number of changes "
        "(len(values)). Judged a standard symbol, not a new term; the sentence at :438 uses n for the 12 changes of "
        "window three."),
    row("proj-spec-window-start-must", "2.9-prose", "course/modules/LX/LX1/project.html:438 (window two start); "
        "tests/labs/LX1/lab-LX1-project-3.py", "PASS", "Fresh. :438 says the lab computes no other start for window two "
        "and that the window start is a candidate limit; the lab computes exactly one window two (WINDOW_TWO_FROM = "
        "2000-01)."),
    row("proj-rubric-c2-gap", "2.6-rubric", "course/modules/LX/LX1/project.html:480 (C2 row)", "PASS",
        "Fresh. Descriptors checked for holes: chain of steps with no failure step (L2), two chains with failure and no "
        "holding step (L2), similarities only (L1), differences only with no chain meets no level (0 by the scoring "
        "rule at :473). Exclusive under the highest-level rule."),
    row("proj-rubric-c3-level3-gap", "2.6-rubric", "course/modules/LX/LX1/project.html:481 (C3 level 3 cell)", "PASS",
        "Fresh. L3 'at most two without a locator' and L2 'at most two uncited' are distinct (locator vs citation); the "
        "C3 L3 cell is exclusive with L4 and L2 under the highest-level rule. Its gap for a wrong locator is the "
        "separate FAIL proj-student-error-coverage."),
    row("proj-dag-concepts", "2.9-prose", "course/modules/LX/LX1/project.html:170 (one data-concept link); "
        "course/modules/LX/LX1/L02.html (def-debt-deflation)", "PASS", "check_dag_LX1 PASS (check_dag.out). The concept "
        "link debt-deflation at :170 resolves to L02's dfn with the same id."),
    row("proj-exemplar-A-limit1-cip-locator", "2.6-rubric", "course/modules/LX/LX1/project.html:541; "
        "course/modules/LX/LX1/L04.html:329-333", "PASS", "Fresh. Limit one unchanged; L04.html:329 'Where the canon "
        "breaks' section 4, item 'Exchange rates only' at :333 states the lab cannot test an interest-rate relation. "
        "L04.html unchanged this round."),
    row("proj-rubric-c3-inference-gap", "2.6-rubric", "course/modules/LX/LX1/project.html:481 (C3 L3 and L4, changed "
        "L4 cell)", "PASS", "Fresh. 'marked as the writer's own inference' appears in L4 and L3 and in the brief item 2; "
        "a factual claim neither cited nor marked as inference falls to L2 or lower by the uncited-count rule."),
    row("proj-l04-model-name-stale", "2.9-prose", "course/modules/LX/LX1/project.html:438; "
        "course/modules/LX/LX1/L04.html:84-85", "PASS", "Fresh. L04.html:84 'Definition 2.1 (fixed-exchange-rate model)' "
        "matches the name used at :438 ('the fixed-exchange-rate model of Lesson 4 (Definition 2.1)')."),
    row("proj-exemplar-a-c2-annotation", "2.3-grades", "course/modules/LX/LX1/project.html:508 (episode step 3), :519 "
        "(condition step 3); course/modules/LX/LX1/L02.html definition", "PASS", "Fresh. Step 3 holds, failure at step 2 "
        "for both mechanisms; the definitions at project.html:64 (failure step is the first step at which the analogy "
        "fails) match. Lines 508 and 519 unchanged this round."),
    row("proj-r14-delta-hunks", "2.9-prose", "git diff 8e5751c9 d1e65a0 -- course/modules/LX/LX1/project.html (3 hunks)",
        "PASS", carry("git range 8e5751c9..d1e65a0") + "the r14->r15 hunks were read and checked in round 15; the r15->r16 hunks are checked by proj-r15-delta-hunks."),
    row("proj-r15-delta-hunks", "2.9-prose", "git diff d1e65a0 56cc575 -- course/modules/LX/LX1/project.html "
        "(hunks :43-47, :57-62, :277-281, :306-310, :470-483, :531-541, :585-588); tests/labs/LX1/lab-LX1-project-3.py",
        "PASS", "Fresh. Every hunk read in full this round (git diff). Changes: :46 link text; :60 agreement sentence "
        "without 'or the lab raises' (checked: no remaining 'lab raises' claim, page_checks_r16.out); :62 window three "
        "text; :280 data paragraph (checked against MANIFEST); :309 Check paragraph (raise on cell and month: checked by "
        "damaged differential; agreement sentence: see proj-lab3-raise-claims-untested); :473 scoring sentence (checked: "
        "0 for no level; self-assessment records 'not scored', rubric.js plainSummary); :481 and :482 C3 and C4 cells "
        "(see proj-rubric-exhaustive-r14, proj-student-error-coverage); :534, :541, :588 annotations and Limit two "
        "(checked: 13.58 positive, window one largest; 0.884169 gives 11.58 percent, about 12). Twin docstring line 22 "
        "removed 'or the lab raises' (checked by harness twins)."),
    row("proj-rubric-exhaustive-r14", "2.6-rubric", "course/modules/LX/LX1/project.html:473 (scoring sentence), "
        ":479-483 (C1-C5 rows)", "PASS", "Fresh re-check of the round-14 FAIL. Fixes applied: :473 adds 'A criterion that "
        "no level describes scores 0 (not yet met)'; C4 L4 begins 'At least one number is computed'; C4 L1 'or computes "
        "none'; C4 L3 'except one, and that one does not round an input'. Re-checked for holes under the highest-level "
        "rule: C1 (names both; missing date or locator), C2, C3 (citation vs locator counts are distinct), C4 (L1 none, "
        "L2 rounds or some-not-all, L3 one exception, L4 every number), C5 (with 'at least' reading). Exhaustive with the "
        "0 rule; exclusive under the highest-level rule. The C5 count wording is a separate FAIL "
        "(proj-rubric-c5-count-wording)."),
    row("proj-student-error-coverage", "2.6-rubric", "course/modules/LX/LX1/project.html:481 (C3 L3 cell), :482 (C4 L3 "
        "cell); plans/LX1-build-plan.md section 5.4 (ten student-error patterns)", "FAIL",
        "Checked the plan's ten patterns against the current descriptors. Caught at level 4 only, and not at the bar: "
        "(1) real debt computed as nominal debt: C4 L4 now requires the formula the cited lab line prints (:482), but "
        "C4 L3 names no formula, so a student whose formula is wrong, with unrounded values and a rule, still scores 3 "
        "on C4 and meets the bar (3 on every criterion). (2) percent change with no base or direction: C4 L4 requires "
        "base and sign; C4 L3 does not, so it still scores 3. (4) citation whose locator does not contain the claim: C3 "
        "L4 now requires that each locator is a place where the claim is written; C3 L3 requires only a locator, so it "
        "scores 3. Caught: 5 (C2 L2 no failure step), 6 (C4 L2 rounds before computing), 7 and 8 (uncited claim lowers "
        "C3), 10 (C1 locator or date missing). Pattern 3 ('bubble') is not isolated by any descriptor: a three-step chain "
        "with no fundamental stated scores by the chain-presence rule only. Pattern 9 is a lab (outside the rubric).",
        "Move the correctness elements into the level-3 cells so that the errors fall below the bar: C4 L3 (:482) add "
        "'and every formula is the one the cited line prints or the essay derives, and every percent change names its "
        "base and sign'; C3 L3 (:481) add 'and each locator is a place where its claim is written'. Re-check exemplar A "
        "(C3 4, C4 4 unaffected) and exemplar B (C4 2 unaffected). For pattern 3, add to C2 L4 'and each step names the "
        "ground it rests on (a fundamental or a source)'."),
    row("proj-data-embedded-claim", "2.8-data", "course/modules/LX/LX1/project.html:280; "
        "course/assets/data/market/MANIFEST.json (fx_daily, fx_monthly, ust_daily)", "PASS",
        "Round-15 FAIL re-checked. :280 now reads 'The site embeds three series (fx_daily, fx_monthly, ust_daily; "
        "MANIFEST). This project reads fx_monthly. None of the three is a gold, price-level, output, unemployment or "
        "bank-failure series.' Matches MANIFEST (three datasets; titles FX daily, FX month-end, Treasury bill and "
        "yield). The term 'snapshot set' is removed from this paragraph."),
    row("proj-lab3-raise-claims-untested", "2.5-labs", "course/modules/LX/LX1/project.html:308-309 (Check paragraph), "
        ":437 (expected 'agree ... True' line); tests/labs/LX1/lab-LX1-project-3.py:99-100 (check), :127 (print of "
        "literal 'True')", "FAIL",
        f"Round-15 FAIL re-checked. The 'or the lab raises' claims at :60 and :309 are removed (fix b applied). Still "
        "open: the Check paragraph (:308-309) names the agreement as one of the lab's checks ('Each standard deviation "
        "is computed twice ... The two must agree to 1e-9 percent per month'), and the expected block (:437) prints "
        "'two-pass and statistics.stdev agree in all three windows: True', which the twin prints as a literal (:127). "
        f"Forced disagreement ({S}agreement_r16.py, out/agreement_r16.out): the twin exits 1 with 'ValueError: the "
        "two-pass and statistics.stdev standard deviations disagree'; mutant r13n03 (check removed) exits 0 with the "
        "same 20 lines (SURVIVED in kill_all_r16.out and damaged_candidates_r16.out). No test under tests/ runs this "
        "check (grep of tests/ finds none). The page still claims the check, so the survivor is a finding under the "
        "ruling.",
        "Either (a) add a test under tests/ that runs lab-LX1-project-3.py under python -I -W error with statistics.stdev "
        "replaced by a stub 1e-6 away from the two-pass value and asserts the ValueError 'the two-pass and "
        "statistics.stdev standard deviations disagree' (this kills r13n03); or (b) remove the agreement sentence from "
        ":308-309 and the agreement line from the twin and the expected block at :437, so the page claims no check the "
        "lab does not print. Also note: r13n03's first docstring line does not name the student error (ruling 9)."),
    row("proj-rubric-c5-count-wording", "2.6-rubric", "course/modules/LX/LX1/project.html:483 (C5 L3 'Names two "
        "limits', L2 'Names one limit'); :547 and :491 (Exemplar A C5 = 3)", "FAIL",
        "C5 L3 says 'Names two limits, one with the test that would settle it'; L2 says 'Names one limit'. Read as "
        "exact counts, Exemplar A (three limits, one with a test, official C5 = 3) matches neither L3 nor L2, and the "
        "highest-level rule gives 0 for it, not 3. Only the 'at least' reading (as L4's 'at least two' implies) gives "
        "the official score. Under the exact reading a two-limit essay with no test also matches no level.",
        "At :483 change 'Names two limits, one with the test that would settle it' to 'Names at least two limits, one "
        "with the test that would settle it' and 'Names one limit' to 'Names at least one limit'."),
]

# Mutants: description from round 15 for the carried ones; first docstring line for the new ones.
prev_desc = {m["id"]: m["description"] for m in PREV["mutants"]}
killed_intact = {}
for line in (OUT / "kill_all_r16.out").read_text(encoding="utf-8").splitlines():
    parts = line.split(" | ")
    if len(parts) >= 3 and parts[0] == "KILLED":
        killed_intact[parts[1]] = "harness.py intact-snapshot run (out/kill_all_r16.out): " + parts[2]
killed_damaged = {}
for line in (OUT / "damaged_candidates_r16.out").read_text(encoding="utf-8").splitlines():
    parts = line.split(" | ")
    if len(parts) >= 2 and parts[0] == "KILLED":
        killed_damaged[parts[1]] = "damaged-snapshot differential (out/damaged_candidates_r16.out): " + parts[2][:160]
mutants = []
for path in sorted(MUT.glob("*.py")):
    name = path.name
    first = path.read_text(encoding="utf-8").split('"""')[1].strip().splitlines()[0]
    desc = prev_desc.get(name) or first
    if name in killed_intact:
        killer = killed_intact[name]
    elif name in killed_damaged:
        killer = killed_damaged[name]
    else:
        killer = None
    mutants.append({"id": name, "description": desc, "killed_by": killer})

counts = {}
for r in rows:
    counts[r["status"]] = counts.get(r["status"], 0) + 1
verdict = "PASS" if all(r["status"] == "PASS" for r in rows) and all(m["killed_by"] for m in mutants) else "FAIL"
fragment = {
    "unit": "LX1",
    "slice": "LX1-c",
    "round": 16,
    "verifier": "Claude Haiku 5.5 (claude-haiku-5-5), independent verifier for LX1-c, round 16 (did not build LX1)",
    "pin": "56cc575a",
    "base": "d1e65a0 (round-15 pin, per E-LX1-c.round15.json)",
    "checkout": str(ROOT),
    "scratch": "ledgers/LX1/scripts/LX1-c-r16/ (scripts) and ledgers/LX1/scripts/LX1-c-r16/out/ (every command output)",
    "verified_at": "2026-11-09T00:00:00+00:00",
    "verdict": verdict,
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Delta d1e65a0 -> 56cc575 for LX1-c: project.html (hunks :43-47, :57-62, :277-281, :306-310, :470-483, :531-541, "
        ":585-588) and tests/labs/LX1/lab-LX1-project-3.py (docstring line 22). Every hunk was read. references/, "
        "notation/, tools/, curriculum/, course/assets/data/ and L02/L04 are byte-identical to d1e65a0, so the "
        "round-15 evidence for them is carried where the row names them.",
        "Blind calibration (ruling 15) is UNVERIFIABLE in this session: the annotation text of the changed hunks and "
        "the verdict lines were read before the prose extraction. Prose-only scores (out/blind_prose_r16.txt): A "
        "4,4,4,4,3; B 2,2,1,2,1, matching the official scores. A clean run must score before reading :493, :555 or any "
        "annotation.",
        "Mutants: 71 lab mutants listed (68 round-15 plus r16n01-r16n03). 70 have a recorded kill. r13n03 has none and is "
        "the open case of proj-lab3-raise-claims-untested. LX1 is rubric-only, so no grader mutation test applies; the "
        "lab mutants are run as the page's own claims require.",
        "Alternatives: the three round-15 alternatives for Labs 1-3 survive (correct), as required.",
        "Rubric: exhaustive and exclusive under the highest-level rule with the 0 rule, except the C5 count wording "
        "(FAIL). Student-error coverage: the plan's patterns 1, 2 and 4 still meet level 3 on C4 or C3 (FAIL).",
        "Not checked: the full gate (render_curriculum, run_graders --all, check_pages --all) was not run, because no "
        "curriculum, tool or other-unit file changed in the delta; live fx_monthly rebuild was not repeated (data "
        "byte-identical, sha256 matched)."
    ],
    "summary": {
        "rows": len(rows),
        "pass": counts.get("PASS", 0),
        "fail": counts.get("FAIL", 0),
        "unverifiable": counts.get("UNVERIFIABLE", 0),
        "mutants": len(mutants),
        "mutants_killed": sum(1 for m in mutants if m["killed_by"]),
    },
}
out = ROOT / "ledgers/LX1/LX1-c.json"
out.write_text(json.dumps(fragment, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
print(json.dumps(fragment["summary"]), verdict)
