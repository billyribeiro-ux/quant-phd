"""Writes the LX1-c round-12 ledger fragment from the rows and the kill-check output of this round."""
import glob, json, os, re, sys
from datetime import datetime, timezone
root = sys.argv[1]
os.chdir(root)
S = "ledgers/LX1/scripts/LX1-c-r12"
R = "ledgers/LX1/scripts/LX1-c-r12/out/"
rows = []
def row(id_, check, location, status, evidence, fix=None):
    r = {"id": id_, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    rows.append(r)

row("proj-rung1-step3-rounding-claim", "2.5-numbers", "course/modules/LX/LX1/project.html:175", "PASS",
    f"{R}rederive_r12.out: 10000000/0.85 = 11764705.88235294 cents, prints 117647.06 dollars; page :175 prints 11764705.882 cents and 117647.06.")
row("proj-real-value-vs-lesson2", "2.4-mathematics", "course/modules/LX/LX1/project.html:56, :58; course/modules/LX/LX1/L02.html:83-84, :97", "PASS",
    "L02.html:83 states V_t = D P_0 / P_t; :84 names (A2) and (A3); :97 proves V_t/V_{t-1} = P_{t-1}/P_t. Page :56 and :58 use the same identity with P_0 = 1 and V_t/V_0 = P_0/P_t, as stated.")
row("proj-manifest-note-misattributed", "2.2-numbers-data", "course/modules/LX/LX1/project.html:269, :277, :293; course/assets/data/market/MANIFEST.json (fx_monthly); tools/data_sources.yaml:64", "PASS",
    "MANIFEST fx_monthly: title 'USD per unit of foreign currency', transform 'each column's last value in the month', columns AUD..SEK with no interest-rate column, first 1971-01, last 2026-09, rows 669. data_sources.yaml:64 says 'Spot rates only'. Page :269, :277, :293 match each field.")
row("proj-lab3-citation-string", "2.2-numbers-data", "course/modules/LX/LX1/project.html:277, :285; tests/labs/LX1/lab-LX1-project-3.py docstring", "PASS",
    "Page citation and lab docstring equal MANIFEST citation field 'Board of Governors of the Federal Reserve System, G.5/H.10 Foreign Exchange Rates (noon buying rates in New York)' (python -I read of MANIFEST.json, this round).")
row("proj-reading-reinhart-registry", "2.1-citations", "course/modules/LX/LX1/project.html:633-638; references/references.json", "PASS",
    "Reading list holds friedman1963monetary, eichengreen1992golden, garber2000famous; all three records exist with used_by LX1. reinhart2009this is not on the project page; it is cited in index.html:206 and its used_by LX1 is correct. tools/verify_refs.py --unit LX1 live: 4 of 560 entries, 0 problems (out/verify_refs_unit_LX1.out).")
row("proj-spec-current-undefined", "2.6-spec", "course/modules/LX/LX1/project.html:444, :62; lab-LX1-project-3 WINDOW_THREE_FROM", "PASS",
    "The brief item 1 (:444) defines the current condition as dated within the twelve months ending at the last month of the data, i.e. 2025-10 to 2026-09, matching window three (:62; lab twin WINDOW_THREE_FROM='2025-10').")
row("proj-exemplar-A-condition", "2.6-spec", "course/modules/LX/LX1/project.html:494-495, :516-517", "PASS",
    "Exemplar A names the condition with dates 2025-10 to 2026-09 and the MANIFEST last month; the condition meets the spec's dating rule.")
row("proj-gate-commands", "2.9-gates", f"{S}/out/", "PASS",
    "check_pages.py --unit LX1: PASS; check_dag.py --unit LX1: PASS; check_projects.py --unit LX1: PASS; run_labs.py --unit LX1: PASS (7/7); fetch_data.py --check: 3 datasets, 0 problems; verify_refs.py --offline: 0 problems. Outputs in out/check_pages_LX1.out, out/check_dag_LX1.out, out/check_projects_LX1.out, out/run_labs_LX1.out, out/fetch_data_check.out, out/verify_refs_offline.out.")
row("proj-lab1-twin-run", "2.5-labs", "course/modules/LX/LX1/project.html:73-147; tests/labs/LX1/lab-LX1-project-1.py", "PASS",
    f"{S}/twin_vs_page.py: page code equals twin (0 differing lines); twin under python -I -W error exits 0; stdout equals the expected block (trailing whitespace ignored). out/twin_vs_page.out.")
row("proj-lab1-numbers", "2.2-numbers", "course/modules/LX/LX1/project.html:75, :148-168", "PASS",
    f"{S}/rederive_r12.py (exact Fractions): falling 117647.06 / 17.65; rising 86956.52 / -13.04; difference 3069053.7084 cents = 30690.54 dollars; all period values match. out/rederive_r12.out.")
row("proj-lab2-twin-run", "2.5-labs", "course/modules/LX/LX1/project.html:180-255; tests/labs/LX1/lab-LX1-project-2.py", "PASS",
    "twin_vs_page.py: page code differs from the twin on exactly the two blank lines (return ___ for real value and burden); completed twin exits 0 and its stdout equals the expected block (out/twin_vs_page.out).")
row("proj-lab2-numbers", "2.2-numbers", "course/modules/LX/LX1/project.html:182, :245-254", "PASS",
    "rederive_r12.out: real values 40000.00, 40404.04, 40816.33, 41666.67, 42105.26, 43010.75; burden 7.53 (exact 7.5269).")
row("proj-lab2-check-claims", "2.5-labs", "course/modules/LX/LX1/project.html:255", "PASS",
    "rederive_r12.out: inverted-ratio burden prints -7.00 (page: '-7.00 in place of 7.53'). Removing the division gives 40000.00 in every period (kill_check_all_mutants.out: lx1c_r9n01 KILLED, expected-block differs).")
row("proj-lab3-twin-run", "2.5-labs", "course/modules/LX/LX1/project.html:283-435; tests/labs/LX1/lab-LX1-project-3.py", "PASS",
    "twin_vs_page.py: page code equals twin; twin run from a scratch dir holding data/fx_monthly.csv exits 0 under -I -W error; stdout equals the 20-line expected block (out/twin_vs_page.out).")
row("proj-lab3-numbers", "2.2-numbers", "course/modules/LX/LX1/project.html:285, :411-435", "PASS",
    "rederive_r12.out (own script, plain csv and Fractions): window one n=668, zeros 3, sd 2.79 (0.027935); window two n=321, zeros 2, sd 2.47 (0.024700), largest -9.66 (2008-10); window three n=12, zeros 0, sd 1.90, largest 2.96 (2026-04); ratio 0.8842 -> 0.88; difference 0.3236 -> 0.32; two-pass and stdev agree within 1e-9 in all windows.")
row("proj-lab3-L04-cross-check", "2.1-citations-numbers", "course/modules/LX/LX1/L04.html:306-318, :310, :313; course/modules/LX/LX1/project.html:282", "PASS",
    "L04.html:310 window one 668 changes, sd 0.027935; :313 window two 321 changes, sd 0.024700. Both match rederive_r12.out, and page :282 states the same values.")
row("proj-lab3-docstring-claims", "2.5-labs", "course/modules/LX/LX1/project.html:288-313 (lab-3 docstring)", "PASS",
    "Each docstring claim checked: 669 months 1971-01 to 2026-09 (MANIFEST rows, first, last); retrieved 2026-10-19; transform inverts only CAD, CHF, DKK, JPY, NOK, SEK (MANIFEST transform, so GBP is USD per pound); no interest-rate column (MANIFEST columns); windows as in rederive_r12.out; rounding half up from exact binary value (show() uses Decimal(float)). No claim contradicted.")
row("proj-lab3-interpretation-claims", "2.5-labs", "course/modules/LX/LX1/project.html:436; course/modules/LX/LX1/L04.html:81, :84, :92", "PASS",
    "13.58 percent in 1985-03 is the largest window-one change (rederive_r12.out) and is outside window two; 12 changes give 11 degrees of freedom; 321 zero changes under a parity versus 2 observed (window two count, rederive_r12.out). The 'Definition 2.1' reference matches L04.html:84.")
row("proj-lab3-difference-line-r5", "2.2-numbers", "course/modules/LX/LX1/project.html:285, :411, :434, :436, :539", "PASS",
    "Difference window one minus window two = 0.32358 percent per month (unrounded), printed 0.32 (rederive_r12.out). Page :436 says the difference is computed from unrounded dispersions, matching the code (difference = sd_one - sd_two).")
row("proj-lab-simulated-labels", "2.5-labs", "course/modules/LX/LX1/project.html:42, :44, :75, :182, :265, :281-285", "PASS",
    "Labs 1 and 2 print 'SIMULATED' in their first output line and their hypothesis; lab 3 (real data) carries no SIMULATED label and names dataset, licence and MANIFEST retrieval date (:277, :285).")
row("proj-data-licence-quote", "2.8-data", "course/modules/LX/LX1/project.html:277; MANIFEST fx_monthly licence_url", "PASS",
    f"curl -sS -L https://www.federalreserve.gov/disclaimer.htm -> HTTP 200 (out/fed_disclaimer.html, 85306 bytes). The page contains 'Unless otherwise indicated, information on Board's website is in the public domain and may be copied and distributed without permission. Please cite to the Board as the source of the information.' (grep count 1); the quote on the project page is identical to the MANIFEST licence field.")
row("proj-data-snapshot-rebuild", "2.8-data", "course/assets/data/market/fx_monthly.csv; course/assets/data/market/MANIFEST.json; tools/fetch_data.py", "PASS",
    "Rebuilt in a scratch copy with tools/fetch_data.py --fetch --only fx_monthly on 2026-11-05 (log /tmp/lx1c_r12_fetch/fetch.log): built 669 rows, 67392 bytes; snapshot sha256 60572240d1a9d1832d5021297634b2369723b94098414948b891dd26a8bffe3e equals the committed CSV and MANIFEST sha256 byte for byte. Today's raw download sha256 1c312d2fc1de99f174c26178a2cb1f0f0f6a4a08b6dce25b043603fec9a3f24a differs from the committed raw_sha256 8f370f9c57b73e1c0b68a2ee72ddecd3abaffb21fa627fcfd4f8a3612798c6a8; the live file changed, so the difference is recorded, and retrieved and raw_sha256 were not refreshed in the repository.")
row("proj-data-fields", "2.8-data", "course/modules/LX/LX1/project.html:277-278, :293; course/assets/data/market/fx_monthly.csv", "PASS",
    "rederive_r12.out: GBP 0 blank cells; EUR 336 blank cells, all before 1999-01 (last blank 1998-12, first value 1999-01); consecutive months (no gap). Page :277 states both facts correctly.")
row("proj-data-no-other-series", "2.8-data", "course/modules/LX/LX1/project.html:278; tools/data_sources.yaml ids (lines 19, 53, 91)", "PASS",
    "data_sources.yaml lists only fx_daily, fx_monthly and ust_daily; grep for gold, unemploy, bank fail, price level, cpi and output returns 0 matches. The page's 'no historical series embedded' statement is consistent with the registry.")
row("proj-spec-ladder", "2.6-spec", "course/modules/LX/LX1/project.html:40-48, :71-170, :178-255, :257-273, :616-629", "PASS",
    "Order: rung 1 worked example with step annotations (:71-170); rung 2 completion lab with class 'lab completion' (:178-255); rung 3 spec, rubric and labs (:257-615); rung 4 stretch (:616-629). check_projects.py --unit LX1: PASS.")
row("proj-spec-curriculum-scope", "2.6-spec", "curriculum/06-profession-capstone.yaml:44-47; course/modules/LX/LX1/project.html:263 (Context), :445 (brief item 2), :478 (C2 level 4)", "FAIL",
    "The curriculum brief says the comparison 'says where the analogy holds and where it breaks' (06-profession-capstone.yaml:44-47). The page's Context (:263) and brief item 2 (:445) require only the failure step ('name the step at which the analogy fails'); the lede (:37) says 'the step where the analogy breaks'. No page sentence requires the student to state where the analogy holds, and C2 level 4 (:478) scores only the failure step. Scope does not match the curriculum.",
    "Add to the Context (project.html:263) and to brief item 2 (:445) a requirement to state the steps at which the analogy holds as well as the first step at which it fails; change C2 level 4 (:478) to require both, with the evidence for the failure step; keep level 3 to 1 consistent. Re-run check_projects.py --unit LX1 and page_smoke.")
row("proj-hours", "2.6-hours", "course/modules/LX/LX1/project.html:454-466 (table#hours); course/modules/LX/LX1/index.html:29", "PASS",
    "Table rows 1 + 1 + 2 + 1.5 + 2.5 + 2 = 10 h, equal to data-hours-project=10. Verifier estimate: rung 1 about 1 h, rung 2 about 0.75 h, selection and sourcing about 2.5 h, mechanism outline about 1.5 h, drafting about 3.5 h, self-assessment about 2 h, total about 11.25 h, which is 12.5 percent above 10 h (inside the 30 percent band).")
row("proj-rubric-observable", "2.6-rubric", "course/modules/LX/LX1/project.html:477-481 (rubric table)", "PASS",
    "Each level cell is observable: a reader can check the named element (locator, chain of steps, failure step with evidence, rounding rule, limits with tests). C2 level 2 now includes the 'fewer than three steps' case (:478). check_projects.py rubric_problems: PASS (four td cells per row).")
row("proj-calibration-exemplars", "2.6-rubric", "course/modules/LX/LX1/project.html:489-614 (exemplar articles); ledgers/LX1/scripts/LX1-c-r12/blind_extract.py; blind_scores.txt", "UNVERIFIABLE",
    "Exemplar B was scored blind: the essay text was extracted by blind_extract.py and scored from the rubric only, before its annotations or data-scores were read, giving C1 2, C2 2, C3 1, C4 2, C5 1, equal to the official scores (data-scores at :551). Exemplar A was NOT scored blind: its data-scores attribute (project.html:489, '4,4,4,4,3') was visible in this session before scoring. My essay-text scoring of A gave C1 4, C2 4, C3 4, C4 4, C5 3, equal to the official scores, but that is not clean-room calibration.",
    "A clean-room verifier that has not read project.html's annotations, data-scores, verdict or reveal text scores a copy of exemplar A (memo text only) and must match the official scores within one level on every criterion. Re-run this row from that score sheet.")
row("proj-exemplar-numbers", "2.2-numbers", "course/modules/LX/LX1/project.html:527-534, :537-547, :581-589", "PASS",
    "A: 17.65 percent (Lab 1 Part B, exact 17.647 rounded half up); 2.47, 2.79, 1.90 percent per month (Lab 3); ratio 0.88 from unrounded values (0.8842). B: '2.47 percent per year' is the wrong unit (the figure is per month); 2.47/2.79 = 0.8853 -> 0.89 is computed from rounded inputs, as the annotation says; 11 percent fall follows from 0.89. All verified in rederive_r12.out.")
row("proj-reading-keys", "2.1-citations", "course/modules/LX/LX1/project.html:633-638; references/references.json", "PASS",
    "Keys exist in references/references.json; the exemplar's title string 'Golden fetters: the gold standard and the Great Depression, 1919-1939' equals the registry title for eichengreen1992golden. No page passage attributes content to Friedman or Garber.")
row("proj-notation", "2.4-notation", "course/modules/LX/LX1/project.html TeX spans (19 distinct); notation/notation.json", "PASS",
    "notation.json registers T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f and Q. None appears on the project page. Local symbols used: D, P_t, V_t, S_m, n, m, t, 1/0.85 expressions; the macro set used is the standard \\ln and \\, only.")
row("proj-scope-words", "2.9-prose", f"{S}/scope_scan.py -> {R}scope_scan.out", "PASS",
    "Every scope-word sentence checked (scope_scan.out, 50 sentences): 'every monthly change' (668 of 668 changes, 0 blank GBP cells); 'every log change would be zero' (derivation); 'all 12 changes' (window three n=12); 'the only lab that reads a file' (labs 1 and 2 contain no file reads); 'the same debt' and 'SIMULATED ... only' are definitional. No unsupported universal.")
row("proj-process-words", "2.9-prose", "course/modules/LX/LX1/project.html (all prose, labs, comments)", "PASS",
    "Search for build, builder, round (process sense), verifier, REQUESTS, fixer, planner, architect, TODO, TBD, lorem, 'for brevity', 'details omitted', '...' outside code: no hit. The only 'Round' (:175, 'Round once, at print time') is arithmetic. BUILDER_RULES 1.3-1.4 phrases are absent.")
row("proj-links-anchors", "2.9-structure", f"course/modules/LX/LX1/project.html (16 href); {R}links_r12.out", "PASS",
    "links_r12.py: 16 hrefs, 0 missing file, 0 missing fragment id (index.html#placement exists at index.html:73 with data-mastery 0.8; L02.html#def-debt-deflation exists at L02.html:110). One external link (federalreserve.gov/disclaimer.htm) is the licence page, cited in prose.")
row("proj-page-smoke", "2.9-structure", f"course/modules/LX/LX1/project.html; {R}page_smoke_project.out", "PASS",
    "Run: tools/page_smoke.py --unit LX1 --pages project (stem, not file name; an earlier run with 'project.html' matched no page and was discarded). Result: 'page_smoke modules/LX/LX1/project.html: PASS' and 'page_smoke LX1: PASS'; lab timings 0.0 s.")
row("proj-atlas-autograder-na", "2.6-autograder", "curriculum/06-profession-capstone.yaml:19-49; course/modules/LX/LX1/", "PASS",
    "LX1 has no atlas key and no debate key; grading is rubric, so no grader directory is required. check_projects.py --unit LX1 skips the contract check and passes.")
row("proj-mutants-student-errors", "2.6-mutation", f"ledgers/LX1/mutants/ (58 files); {R}kill_check_all_mutants.out", "PASS",
    "kill_check_all_mutants.py over all 58 project-lab mutants: TOTAL killed=58 survived=0. Five new student-error mutants written this round (r12n01 window three strict inequality; r12n02 largest change printed as magnitude; r12n03 zero test with 1e-4 tolerance; r12n04 price level in percent; r12n05 Part C sign reversed). A first r12n03 variant (1e-6 tolerance) survived because no GBP change is below 1e-6 in absolute value (smallest nonzero 5.8e-5, near_zero_r12.out); it was replaced by the 1e-4 variant that changes the window-one zero count.")
row("proj-alternatives", "2.6-alternatives", f"{S}/make_alts_r12.py; {R}alt_compare_r12.out; {R}alt_compare_r11_rerun.out", "PASS",
    "Four new valid alternatives match their page expected blocks: pstdev rescaled by sqrt(n/(n-1)) (lab 3); log change as difference of logs (lab 3); burden from inverse prices with exact Fractions (lab 2); round half up via Decimal (lab 1). Five prior alternatives (r10 and r11) re-run and match (alt_compare_r11_rerun.out).")
row("proj-exemplar-a-c2-annotation", "2.3-grades", "course/modules/LX/LX1/project.html:505-521 (exemplar A mechanism passages); L02.html:127-128 (Remark 3.3)", "PASS",
    "Blind C2 score for A is 4 (both chains have three steps; failure named with evidence: Remark 3.3 at L02.html:127-128 for episode, and the window-three zero count from Lab 3 for condition). Annotations at :510 and :521 agree.")
row("proj-exemplar-b-annotations-vs-descriptors", "2.6-rubric", "course/modules/LX/LX1/project.html:551-613", "PASS",
    "Each B annotation names a descriptor that the passage meets or misses: C1 level 2 (condition undated); C2 level 2 (similarities and one difference, no chain); C3 level 1 and level 2 miss (at least three uncited claims); C4 level 2 and level 3 miss (rounded inputs, 0.88 not 0.89); C5 level 1. Each cited descriptor exists at :476-481.")
row("proj-brief-rubric-escape-clauses", "2.6-spec", "course/modules/LX/LX1/project.html:447 (brief item 4), :263, :479 (C3 level 4)", "PASS",
    "Brief item 4 (:447) and C3 level 4 (:479) both accept 'the essay states that it makes no such claim' for B or C claims. The level 3 cell lacks this escape clause; the defect is recorded in proj-rubric-c3-level3-gap.")
row("proj-exemplar-locators", "2.1-citations", "course/modules/LX/LX1/project.html:494-495, :505-506, :516-517, :527-528, :538-539; course/modules/LX/LX1/L02.html:127-128; course/modules/LX/LX1/L04.html:329", "PASS",
    "Exemplar locators checked: Eichengreen title field (references/references.json title, exact); MANIFEST field 'last' (2026-09) and retrieved 2026-10-19 (MANIFEST); Lab 3 window and difference lines (rederive_r12.out); L02 Remark 3.3 and Proposition 2.1(a) (L02.html:123, :127-128); L04 'Exchange rates only' item (L04.html:329).")
row("proj-exemplar-a-c5-limit-count", "2.6-rubric", "course/modules/LX/LX1/project.html:538-545, :491, :539", "PASS",
    "Exemplar A names three limits (:539). Limit one gives the test that would settle it (interest-rate series); limits two and three name none. C5 level 3 is the correct reading (annotation :545 agrees).")
row("proj-round11-delta-project-page", "2.9-prose", "course/modules/LX/LX1/project.html:59-62, :478, :539 (diff 11d7077a..5db69a9b)", "PASS",
    "Every hunk of project.html in the delta read: :62 'which is the US dollar price of one pound sterling' (MANIFEST transform: GBP not inverted, so USD per GBP: verified); :478 C2 level 2 cell (now includes 'fewer than three steps'; see proj-rubric-c2-gap); :539 limit one (now attributes the no-interest-rate statement to Lesson 4 Section 4 item, matching L04.html:329). L04.html delta (:51, line 'why-it-matters') and cards.json (new card LX1-c082) are outside this slice.")
row("proj-spec-limits-test-each", "2.6-spec", "course/modules/LX/LX1/project.html:265, :447, :481, :491, :545", "PASS",
    "Spec and brief require two limits and the test that would settle at least one; C5 level 3 requires the same; level 4 requires a test for each limit. Consistent.")
row("proj-notation-n-undefined", "2.4-notation", "course/modules/LX/LX1/project.html:60 ('denominator n - 1'), :436", "PASS",
    "n is not defined by a sentence; it is the sample size, i.e. the number of monthly changes in the window (the lab's code uses len(values)). Standard symbol for a sample standard deviation; no collision with notation.json. Not a finding.")
row("proj-lab3-raise-claims-untested", "2.5-labs", "course/modules/LX/LX1/project.html:306-308 (lab-3 Check paragraph); tests/labs/LX1/lab-LX1-project-3.py", "PASS",
    f"Changed from round 11. {S}/twin_damaged_r12.py ran the committed twin on damaged copies: blank GBP 2000-06 -> ValueError \"2000-06: GBP cell '' is blank or not a decimal number\"; 'n/a' -> same ValueError naming the cell; removed 1990-06 -> ValueError 'month 1990-07 does not follow 1990-05'; blank EUR control runs and prints (out/twin_damaged_r12.out). The population-sd variant is killed (kill_check_all_mutants.out, lx1c_r9n04). Advisory, not a row: no committed pytest under tests/ runs these cases (grep returns nothing), so the check lives only in the kept script; a test under tests/ would make it durable.")
row("proj-spec-window-start-must", "2.6-spec", "course/modules/LX/LX1/project.html:436", "PASS",
    "'The lab computes no other start for window two' is true: lab 3 has one WINDOW_TWO_FROM = '2000-01' (twin). The sentence names the window start as a candidate limit, which the essay may use.")
row("proj-rubric-c2-gap", "2.6-rubric", "course/modules/LX/LX1/project.html:478 (C2 level 2 cell)", "PASS",
    "Round-11 FAIL fixed: level 2 now reads 'Lists similarities and one difference; or gives a chain of steps but names no failure step; or gives a chain of fewer than three steps for either mechanism.' A two-step chain with a named failure now matches level 2. Under the highest-level rule (:471), every essay with a chain, a failure step, or a similarity and one difference matches exactly one level. An essay that names only differences, with no similarity and no chain, matches no descriptor; that is below the level-1 floor, as an essay naming no caveat is under C5, and is not counted.")
row("proj-exemplar-A-limit1-cip-locator", "2.1-citations", "course/modules/LX/LX1/project.html:539; course/modules/LX/LX1/L04.html:329", "PASS",
    "Round-11 FAIL fixed. Page :539 now says 'Lesson 4 says the lab cannot test any such relation, because the file has no interest-rate column (Lesson 4, Section 4, item \"Exchange rates only\")'. L04.html:329 says 'The lab cannot test any relation between interest rates and exchange rates, because the file has no interest-rate column, and this lesson states none.' No covered-interest-parity attribution remains (grep returns none on LX1 pages except none).")
row("proj-rubric-c3-level3-gap", "2.6-rubric", "course/modules/LX/LX1/project.html:479 (C3 level 3 cell); cf. :447 (brief item 4) and :479 (C3 level 4)", "FAIL",
    "C3 level 3 requires 'the counter-evidence is named for at least one claim graded B or C'. An essay with no claim graded B or C and no statement that it makes none (brief item 4, :447, allows that statement) can never meet this element. Example: 12 claims, 11 with locators and one uncited, none graded B or C: level 4 fails (uncited claim), level 3 is unsatisfiable, so the essay scores level 2 under 'at most two factual claims are uncited' (:479). The level-3 cell contradicts the brief's escape clause.",
    "In C3 level 3 (project.html:479) replace 'the counter-evidence is named for at least one claim graded B or C' with 'every claim graded B or C names its counter-evidence, or the essay states that it makes no such claim', matching brief item 4 (:447) and level 4. Keep the citation element unchanged.")
row("proj-dag-concepts", "2.9-dag", "course/modules/LX/LX1/project.html (one data-concept link, :168); course/modules/LX/LX1/L02.html:110; check_dag.py --unit LX1", "PASS",
    "check_dag.py --unit LX1: PASS. The only concept link on the page is debt-deflation, linked to L02.html#def-debt-deflation (defined at L02.html:110, an earlier lesson). No other data-concept appears on the page.")

mutants = []
kill_lines = open(R + "kill_check_all_mutants.out", encoding="utf-8").read().splitlines()
reason = {}
for ln in kill_lines:
    m = re.match(r"(KILLED|SURVIVED) \| (\S+) \| ?(.*)$", ln)
    if m:
        reason[m.group(2)] = (m.group(1), m.group(3))
for path in sorted(glob.glob("ledgers/LX1/mutants/*.py")):
    name = os.path.basename(path)
    first = open(path, encoding="utf-8").readline().strip().strip('"')
    status, why = reason.get(name, ("MISSING", ""))
    killed_by = (f"{S}/kill_check_all_mutants.py: {why}" if status == "KILLED" else None)
    mutants.append({"name": name, "description": first, "killed_by": killed_by})

fragment = {
    "unit": "LX1",
    "slice": "LX1-c",
    "round": 12,
    "verifier": "Claude Haiku 5.5 (claude-haiku-5-5), independent verifier for LX1-c, round 12 (did not build LX1)",
    "pin": "5db69a9bee460736c318ebfacc7200ee5a6eb0f0",
    "base": "11d7077a290f7960b183d3a5a6631af4773888f9 (round-11 pin). Delta in slice: project.html :59-62 (windows dd), :478 (C2 level 2), :539 (limit one); L04.html:51 and cards.json (outside slice). Lab twins, data, MANIFEST, references byte-identical.",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE12-LX1-c",
    "scratch": "/tmp/lx1c_r12_scratch (snapshot copy); /tmp/lx1c_r12_fetch (live rebuild of fx_monthly); /tmp/lx1c_r12_scratch damaged copies made in temporary directories",
    "verified_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
    "verdict": "FAIL",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Blind calibration (proj-calibration-exemplars) is UNVERIFIABLE: exemplar A's data-scores were visible before scoring. Exemplar B was scored clean and matches.",
        "C2 below-floor (names only differences, no similarity, no chain) and below-floor cases of C1, C3, C5 match no descriptor; not counted as a FAIL, consistent across criteria. Recorded for the builder.",
        "Rubric reading convention (as round 11): 'Names one limit' (C5 level 2) and 'one of them' (C1 level 2) read as at-least-one; 'except one' (C4 level 3) read as at-most-one. Under this reading C1, C2, C4 and C5 are exhaustive at mid-levels and every mid-level performance matches exactly one level under the highest-level rule (:471).",
        "The agreement tolerance 1e-9 percent (lab 3, AGREEMENT) cannot be reached by any input (two-pass and statistics.stdev differ only at float rounding); recorded as an untested constant, not a finding.",
        "Lab 3 rounding: a banker's-rounding variant survives on this data because no printed value is an exact binary tie; lab twins are demonstrations and no page sentence says the lab detects it. Not a finding.",
        "Spec questions a competent student would still ask: (1) how many characters or words count as one factual claim for C3; (2) whether the essay must reuse Lab 3's numbers. Neither is a blocking gap; the spec answers submission (:618 keep self_assessment.md) and page length (:265).",
        "Registry: reinhart2009this used_by ['E9','LX1'] is correct (cited in index.html:206); no registry flag.",
        "Round-11 FAIL rows fixed at 5db69a9: proj-rubric-c2-gap and proj-exemplar-A-limit1-cip-locator now PASS. proj-lab3-raise-claims-untested re-verified and PASS (advisory test suggestion only).",
        "Cards (LX1-c082 added at 5db69a9) and L04.html are outside this slice and were not verified here.",
    ],
    "summary": "",
}
counts = {"PASS": 0, "FAIL": 0, "UNVERIFIABLE": 0}
for r in rows:
    counts[r["status"]] += 1
killed = sum(1 for m in mutants if m["killed_by"])
fragment["summary"] = (f"LX1-c round 12: verdict FAIL. {len(rows)} rows: {counts['PASS']} PASS, {counts['FAIL']} FAIL, "
    f"{counts['UNVERIFIABLE']} UNVERIFIABLE. Mutants {killed}/{len(mutants)} killed (53 existing plus 5 new). Labs 1-3 pass alone under python -I -W error with stdout equal to the expected blocks; run_labs LX1 7/7; four new and five prior alternatives match. Failing rows: proj-spec-curriculum-scope (holds not required), proj-rubric-c3-level3-gap (level-3 cell unsatisfiable without a B or C claim), proj-calibration-exemplars (UNVERIFIABLE, exemplar A not clean-room).")
os.makedirs("ledgers/LX1", exist_ok=True)
json.dump(fragment, open("ledgers/LX1/LX1-c.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("rows", len(rows), counts, "mutants", len(mutants), "killed", killed)
