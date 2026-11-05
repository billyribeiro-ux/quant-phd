"""Round-11 verifier: writes the LX1-c fragment from the round-11 evidence files (rows as checked this round) and the
mutant kill output. Argument 1 is the checkout root. Output: ledgers/LX1/LX1-c.json."""
import json, re, subprocess, sys
from datetime import datetime, timezone
from pathlib import Path

root = Path(sys.argv[1]).resolve()
S = "ledgers/LX1/scripts/LX1-c-r11/"
PIN = subprocess.run(["git", "rev-parse", "HEAD"], cwd=root, capture_output=True, text=True).stdout.strip()

kill = (root / S / "kill_check_all_mutants.out").read_text(encoding="utf-8").splitlines()
mutants = []
for line in kill:
    m = re.match(r"(KILLED|SURVIVED) \| (\S+) \| ?(.*)$", line)
    if not m:
        continue
    name, reason = m.group(2), m.group(3).strip()
    doc = (root / "ledgers/LX1/mutants" / name).read_text(encoding="utf-8").split("\n")[0].strip('"')
    if m.group(1) == "KILLED":
        mutants.append({"name": name, "description": doc, "killed_by": f"{S}kill_check_all_mutants.py: {reason}"})
    else:
        mutants.append({"name": name, "description": doc, "killed_by": None})

P = "PASS"
R = []
def row(i, check, loc, status, ev, fix=None):
    d = {"id": i, "check": check, "location": loc, "status": status, "evidence": ev}
    if status != P:
        d["fix"] = fix
    R.append(d)

row("proj-rung1-step3-rounding-claim", "2.5-numbers", "course/modules/LX/LX1/project.html:173, :175", P,
    f"{S}rederive_r11.out 'lab1 falling: t5 real debt exact=11764705.88235 dollars=117647.06'; page :175 prints 11764705.882 and 117647.06.")
row("proj-real-value-vs-lesson2", "2.4-mathematics", "project.html:56, :58, :168, :506; course/modules/LX/LX1/L02.html:84, :89-90, :97, :110, :123, :127-128", P,
    "Read this round: L02.html Proposition 2.1 (A2) fixed nominal debt, (A3) P_t positive with P_0 base; (a) V_t/V_{t-1} = P_{t-1}/P_t; Definition 3.1 debt deflation is arithmetic; Remark 3.3 says the corollary gives no cause of a fall. project.html:506 cites Proposition 2.1(a) under (A2) and (A3) and step 3 'multiplied by P_{t-1}/P_t' is the same identity. L02 is not in the round-11 delta.")
row("proj-manifest-note-misattributed", "2.2-numbers-data", "project.html:269, :277, :291-293; course/assets/data/market/MANIFEST.json (fx_monthly)", P,
    f"{S}manifest_fields_r11.out: title 'Month-end foreign exchange rates, ten currencies, USD per unit of foreign currency'; MANIFEST transform inverts CAD, CHF, DKK, JPY, NOK, SEK (rederive_r11.out manifest.transform); columns ten; first 1971-01; last 2026-09; rows 669; retrieved 2026-10-19. Page statements match.")
row("proj-lab3-citation-string", "2.2-numbers-data", "project.html:277, :285; tests/labs/LX1/lab-LX1-project-3.py docstring lines 288-289", P,
    f"{S}manifest_fields_r11.out: MANIFEST citation occurs in project.html 2 times (:277, :285); the lab-3 docstring contains it after whitespace normalisation (True).")
row("proj-reading-reinhart-registry", "2.1-citations", "project.html:633-638; references/references.json", P,
    "Reading-list keys friedman1963monetary, eichengreen1992golden, garber2000famous: all status 'verified' in references/references.json. grep -c reinhart project.html = 0 (this round). references.json (00a84795..11d7077) adds LX1 to the used_by of reinhart2009this; the page does not cite that key.")
row("proj-spec-current-undefined", "2.6-spec", "project.html:444, :299-300; tests/labs/LX1/lab-LX1-project-3.py WINDOW_THREE_FROM", P,
    "project.html:444 defines the current condition window as the twelve months ending at the last month of the data (2025-10 to 2026-09); lab 3 sets WINDOW_THREE_FROM = '2025-10' and its expected block prints 'Window three, 2025-10 to 2026-09' with 12 changes (expected_vs_output.out block 3).")
row("proj-exemplar-A-condition", "2.6-spec", "project.html:495, :517", P,
    f"{S}manifest_fields_r11.out: fx_monthly last '2026-09'; window three 12 changes (rederive_r11.out 'w3: n=12').")
row("proj-gate-commands", "2.9-gates", f"{S}*.out", P,
    f"At pin {PIN[:9]} this round: check_pages LX1 PASS (check_pages.out); check_dag LX1 PASS (check_dag.out); check_projects LX1 PASS (check_projects.out); run_labs --unit LX1 PASS 7/7 (run_labs.out); page_smoke --unit LX1 --pages project PASS (page_smoke_project.out); fetch_data --check '3 datasets, 0 problems' (fetch_data_check.out); verify_refs --offline '560 entries, 0 problems' (verify_refs_offline.out); verify_refs --unit LX1 live '4 of 560 entries, 0 problems' (verify_refs_unit_LX1.out); ruff check and ruff format --check on tests/labs/LX1 pass (ruff_check_labs.out, ruff_format_labs.out); mypy --no-incremental on the three project twins 'Success: no issues found in 3 source files' (mypy_project_labs.out); pytest tests/test_labs.py tests/test_run_labs.py -k LX1: 7 passed (pytest_labs_LX1.out); mutate_graders --unit LX1 --seeds 0-9 rc 0, no grader (mutate_graders_LX1.out). Not run: repository-wide ruff, mypy and pytest (outside this slice); run_graders (no grader).")
row("proj-lab1-twin-run", "2.5-labs", "tests/labs/LX1/lab-LX1-project-1.py; project.html:76-147", P,
    f"Twin run alone with python -I -W error in a scratch dir: rc 0, stderr 0 bytes, 20 lines; {S}expected_vs_output.out block 1 equal; run_labs PASS (page code equals twin).")
row("proj-lab1-numbers", "2.2-numbers", "project.html:75, :148-168", P,
    f"{S}rederive_r11.out (exact Fractions): 117647.06 (falling, t=5), 17.65 (burden), -13.04 (rising), 86956.52 (rising, t=5), 30690.54 (difference).")
row("proj-lab2-twin-run", "2.5-labs", "tests/labs/LX1/lab-LX1-project-2.py; project.html:183-255", P,
    f"Twin run alone with python -I -W error: rc 0, stderr empty, 10 lines; {S}expected_vs_output.out block 2 equal; run_labs PASS (page code equals twin except the two blanked lines).")
row("proj-lab2-numbers", "2.2-numbers", "project.html:182, :245-254", P,
    f"{S}rederive_r11.out: 40000.00 at t=0, 43010.75 at t=5, burden 7.53 (exact 7.526882); intermediate real values 40404.04, 40816.33, 41666.67, 42105.26 match the expected block.")
row("proj-lab2-check-claims", "2.5-labs", "project.html:255", P,
    f"Omitting the division: {S}m01_output.txt prints 40000.00 for t=0..5. Inverted ratio: {S}rederive_r11.out 'lab2 inverted burden: -7.00'. Both mutants KILLED in {S}kill_check_all_mutants.out.")
row("proj-lab3-twin-run", "2.5-labs", "tests/labs/LX1/lab-LX1-project-3.py; project.html:286-435", P,
    f"Twin run alone with python -I -W error in a scratch dir holding data/fx_monthly.csv: rc 0, stderr empty, 20 lines; {S}expected_vs_output.out block 3 equal.")
row("proj-lab3-numbers", "2.2-numbers", "project.html:285, :411-435", P,
    f"{S}rederive_r11.out: window one 668 changes, 3 zeros, sd 2.793528 -> 2.79, largest 13.58 (1985-03); window two 321 changes, 2 zeros, sd 2.469950 -> 2.47, largest -9.66 (2008-10); window three 12 changes, 0 zeros, sd 1.902019 -> 1.90, largest 2.96 (2026-04); ratio 0.884169 -> 0.88; difference 0.323578 -> 0.32; statistics.stdev agrees in all three windows.")
row("proj-lab3-L04-cross-check", "2.1-citations-numbers", "course/modules/LX/LX1/L04.html:306-318; project.html:282", P,
    "L04.html:306-318 read this round: 669 months; 668 changes; zero changes 1976-07, 2012-07, 2019-11; window one sd 0.027935; window two sd 0.024700; ratio 0.8842; difference -0.003236. Matches rederive_r11.out.")
row("proj-lab3-docstring-claims", "2.5-labs", "tests/labs/LX1/lab-LX1-project-3.py (docstring, page :286-313)", P,
    f"Docstring claims checked: reads data/fx_monthly.csv; GBP column; 669 months 1971-01 to 2026-09 (expected block line 2); no interest-rate column (csv header, rederive_r11.out). Damaged snapshots: {S}twin_damaged_r11.out: blank GBP cell, non-decimal GBP cell and removed month each rc 1, stdout empty, ValueError naming the cell or month.")
row("proj-lab3-interpretation-claims", "2.5-labs", "project.html:436; course/modules/LX/LX1/L04.html:81, :84, :92", P,
    "12 changes give n - 1 = 11 degrees of freedom. The two zero changes in window two are 2012-07 and 2019-11 (rederive_r11.out zero months). Under the L04 Definition 2.1 model with (A2), x_t = kappa from the month before the window's first change to the end, so a parity held over window two gives 321 zero changes against 2 observed. Claim holds.")
row("proj-lab3-difference-line-r5", "2.2-numbers", "project.html:285, :411, :434, :436, :539", P,
    f"{S}rederive_r11.out: 100*(sd1 - sd2) from unrounded sds = 0.323578 -> 0.32 (half up); matches the printed line, :436 and the exemplar A figure at :539.")
row("proj-lab-simulated-labels", "2.5-labs", "project.html:42, :44, :75, :182, :265, :281-285", P,
    "Labs 1 and 2 labelled SIMULATED at :42, :75, :182 and in their twin docstrings. Lab 3 section (page lines 280-438): grep -ci simulated = 0. Lab 3 is the only lab reading a file (data-files at :283).")
row("proj-data-licence-quote", "2.8-data", "project.html:277; MANIFEST fx_monthly licence and licence_url", P,
    f"{S}licence_curl.out: plain curl -sS -L https://www.federalreserve.gov/disclaimer.htm HTTP 200, 85306 bytes; the fetched page contains the quoted sentence 'Unless otherwise indicated, information on Board's website is in the public domain and may be copied and distributed without permission. Please cite to the Board as the source of the information.' This grants redistribution.")
row("proj-data-snapshot-rebuild", "2.8-data", "course/assets/data/market/fx_monthly.csv; course/assets/data/market/MANIFEST.json; tools/fetch_data.py", P,
    f"Carried from round 8 (course/assets/data/market/* byte-identical since the round-8 pin 0dee921a: git diff --quiet 0dee921a 11d7077 clean): live rebuild record ledgers/LX1/scripts/LX1-c-r8/out/curl_checks_r8.txt ('sha256 of snapshot rebuilt byte-identical'). Re-checked this round: sha256 60572240d1a9d1832d5021297634b2369723b94098414948b891dd26a8bffe3e = MANIFEST sha256; 67392 bytes = MANIFEST bytes (rederive_r11.out); fetch_data --check 0 problems.")
row("proj-data-fields", "2.8-data", "project.html:269, :277, :292-293; course/assets/data/market/fx_monthly.csv", P,
    f"{S}rederive_r11.out: header month,AUD,CAD,CHF,DKK,EUR,GBP,JPY,NOK,NZD,SEK; 669 rows 1971-01 to 2026-09; EUR blank cells 336, all 1971-01 to 1998-12; GBP blank cells 0; month gaps 0.")
row("proj-data-no-other-series", "2.8-data", "project.html:278; course/assets/data/market/MANIFEST.json datasets", P,
    f"{S}manifest_fields_r11.out: fx_daily (AUD..JPY), fx_monthly (ten currencies), ust_daily (tbill_3m, cmt_10y). No gold, price-level, output, unemployment or bank-failure column. plans/LX1-open-items.md:7 (D-1) records no redistributable historical series.")
row("proj-spec-ladder", "2.6-spec", "project.html:40-48, :71-170, :178-255, :257-273, :616, :623-629", P,
    "Read in full this round. Rung 1 (Lab 1) fully solved with annotated worked steps (:171-178); rung 2 two blanks ('return ___' in the page code), instant check; rung 3 specification (:259-273) with the Lab 3 check; rung 4 stretch (:623-629) open-ended. Order as stated.")
row("proj-spec-curriculum-scope", "2.6-spec", "curriculum/06-profession-capstone.yaml:42-49; project.html:259-273, :441-451", P,
    "Curriculum project title 'Then vs. now' matches page :6 and :36; curriculum brief (pick one episode and one current condition; mechanism-level comparison; where the analogy holds and breaks) matches page :444-445; curriculum deliverable 'Two-page essay, every claim cited' matches :267 and :447 with the own-inference exception (an inference is not a factual claim, so not a failure).")
row("proj-hours", "2.6-hours", "project.html:33, :455-466; course/modules/LX/LX1/index.html:29", P,
    "Component rows 1 + 1 + 2 + 1.5 + 2.5 + 2 = 10 (project.html:458-463); data-hours-project=10 at :33 and index.html:29; hub data-hours-lessons=40 sums with it to the curriculum's 50 hours. Own estimate: rung 1 about 1 h; rung 2 0.5-1 h; episode and condition with locators about 2 h; outline about 1.5 h; drafting two cited pages with formulas 2.5-3 h; Lab 3 run 0.25 h; self-assessment 1-2 h; total 9.25-11 h, within 30 percent of 10 h.")
row("proj-rubric-observable", "2.6-rubric", "course/modules/LX/LX1/project.html:478, :480 (C2 and C4 cells)", P,
    "C4 level 1 now reads 'States no rounding rule for any computed number.' and level 2 'Rounds an input before computing, or states a rounding rule for some computed numbers but not all.' Each names an element a reader can check, and level 1 is reachable (the round-10 unreachable-level defect is gone). C1, C3 and C5 descriptors are observable. The C2 gap is a separate row.")
row("proj-calibration-exemplars", "2.6-rubric", "course/modules/LX/LX1/project.html:489-614", "UNVERIFIABLE",
    "Blind scoring could not be done in this session: this verifier read the whole of project.html, including the annotations, verdicts and data-scores, before scoring. A non-blind rubric-only reading of the memo texts gives exemplar A 4,4,4,4,3 and exemplar B 2,2,1,2,1, equal to the official scores. That is consistency, not calibration.",
    "A clean-room verifier that has not read the annotations scores a copy of project.html with the verdict, annotation, data-scores and reveal text removed, then compares with the official scores within one level per criterion.")
row("proj-exemplar-numbers", "2.2-numbers", "project.html:527-534, :537-547, :581-589", P,
    f"Exemplar A: 17.65 (rederive), 2.47, 2.79, 1.90, ratio 0.88 (unrounded 0.884169), difference 0.32 (0.323578). Exemplar B: 2.47/2.79 = 0.8853 -> 0.89 as written; 0.88 from unrounded values as its C4 annotation says; 'per year' is the wrong unit, as its verdict says.")
row("proj-reading-keys", "2.1-citations", "project.html:633-638; references/references.json", P,
    "verify_refs --unit LX1 (live, plain Crossref): 4 of 560 entries, 0 problems (verify_refs_unit_LX1.out). The three reading keys are verified. No other citation key on the page (data-cite grep).")
row("proj-notation", "2.4-notation", "project.html TeX spans; notation/notation.json", P,
    "Page symbols: D, V_t, P_t, P_0, P_{t-1}, P_5, S_m, m, t, n, ln. notation.json registers T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q}; none of these appears on the page, so no collision.")
row("proj-scope-words", "2.9-prose", "project.html (scope-word hits; grep -w only|all|always|every|any|same|drives|exactly)", P,
    "72 hits, all read in context this round. Hits on the lines changed this round (:436, :478, :480, :506) are computed ('all 12 changes'), model-derived ('every month' under (A2)), a rubric element ('no rounding rule for any computed number') or a conditional ('applies only if a fall occurred').")
row("proj-process-words", "2.9-prose", "project.html (all prose, labs and comments); BUILDER_RULES.md 1.3-1.4", P,
    f"grep this round: no 'verifier', 'builder', 'audit', 'delta', 'TODO', 'TBD', 'lorem', 'clearly', 'obviously', 'it is important to note', 'historically', 'roughly'. 'round' appears only as the rounding verb; 'previous' only as the previous month. check_pages LX1 PASS (banned strings).")
row("proj-links-anchors", "2.9-structure", "project.html (19 hrefs); course/modules/LX/LX1/L02.html#def-debt-deflation", P,
    f"{S}links_r11.out: hrefs 19, problems []. Targets: local ids, review.html, index.html, L02.html#def-debt-deflation (L02.html:110).")
row("proj-page-smoke", "2.9-structure", "course/modules/LX/LX1/project.html", P,
    f"{S}page_smoke_project.out: 'page_smoke modules/LX/LX1/project.html: PASS'; labs lab-LX1-project-1/2/3 0.0 s each.")
row("proj-atlas-autograder-na", "2.6-autograder", "curriculum/06-profession-capstone.yaml:19-49; course/modules/LX/LX1/", P,
    "Curriculum entry grading: rubric. No grader directory under course/modules/LX/LX1/ and no run_graders target; the autograder items do not apply. The LX1 entry states no atlas milestone.")
row("proj-mutants-student-errors", "2.6-mutation", "ledgers/LX1/mutants/*.py (53 files: 50 existing, 3 new lx1c_r11n01-03)", P,
    f"{S}kill_check_all_mutants.out: TOTAL killed=53 survived=0 (each mutant run alone under python -I -W error: expected block differs, nonzero exit, or the damaged snapshot does not raise). New round-11 mutants (written by {S}make_mutants_r11.py): lx1c_r11n01 log10 for ln, lx1c_r11n02 window three read as calendar 2025, lx1c_r11n03 first month counted as a zero change; each KILLED by expected-block difference. Lab twins are demonstrations; these are kept as page-claim checks.")
row("proj-alternatives", "2.6-alternatives", f"{S}alt_compare_r11.out", P,
    "Five alternative correct implementations, each run alone under python -I -W error in a scratch dir: float arithmetic with Decimal half-up printing (lab 1); float ratio form of the burden (lab 2, two variants); Welford online variance with log difference (lab 3); numpy std with ddof=1 and a 1e-6 agreement tolerance (lab 3). All rc 0, stderr empty, equal to the page expected block.")
row("proj-exemplar-a-c2-annotation", "2.3-grades", "project.html:505-521; course/modules/LX/LX1/L02.html:127-128", P,
    "Episode passage: three steps, failure at step 2, evidence Remark 3.3 (L02.html:127-128, the corollary gives no cause). Condition passage: three steps, failure at step 2, evidence 0 exact zero changes in window three (rederive_r11.out). Annotations at :510 and :521 match.")
row("proj-exemplar-b-annotations-vs-descriptors", "2.6-rubric", "project.html:551-613; descriptors project.html:476-481", P,
    "Each exemplar B annotation matches its descriptor: C1 level 2 (both named, condition undated); C2 level 2 (similarities and one difference, no chain); C3 level 1 (one source) and miss at level 2 (three uncited claims); C4 level 2 (rounded input, unrounded 0.88); C5 level 1 (caveat, no limit). Official 2,2,1,2,1 consistent.")
row("proj-brief-rubric-escape-clauses", "2.6-spec", "project.html:269, :447, :479", P,
    "The 'own inference' exception in spec :269, brief item 4 :447 and C3 level 4 :479 is consistent: an inference is not a factual claim, so an essay that marks it is not uncited.")
row("proj-exemplar-locators", "2.1-citations", "project.html:495, :506, :517, :528, :539; course/modules/LX/LX1/L02.html:97, :128; course/modules/LX/LX1/L04.html Section 4 item 'Exchange rates only'; references/references.json (eichengreen1992golden)", P,
    "Locators resolve: the Eichengreen title field (references.json title 'Golden fetters: the gold standard and the Great Depression, 1919-1939'); MANIFEST field last = 2026-09; L02 Proposition 2.1(a) and Remark 3.3; L04 Section 4 item 'Exchange rates only' (L04.html:329 at this pin). The claim attached to the L04 locator fails; see proj-exemplar-A-limit1-cip-locator.")
row("proj-exemplar-a-c5-limit-count", "2.6-rubric", "project.html:491, :539, :544, :545", P,
    "Exemplar A names three limits; limit one has a test sentence ('A test would need the short rates of both countries over the same months'); limits two and three name none. Verdict C5 3 and annotations (meets level 3, misses level 4) match the C5 descriptors.")
row("proj-round11-delta-project-page", "2.9-prose", "project.html:436, :478, :480, :506 (diff 00a84795..11d7077)", P,
    "Every changed hunk read. :436 window start is now 'a candidate limit ... which the essay may name or not' (no longer a requirement; computed figures checked in proj-lab3-interpretation-claims). :478 C2 level 2 and :480 C4 levels 1-2 (see proj-rubric-c2-gap and proj-rubric-observable). :506 step 3 'the real value is multiplied by P_{t-1}/P_t' matches V_t/V_{t-1} = P_{t-1}/P_t (L02 Prop 2.1(a)). The hunks at :491 and :545 are unchanged. Lab twins and data byte-identical to the round-10 pin.")
row("proj-spec-limits-test-each", "2.6-spec", "project.html:267, :448, :481, :491, :545", P,
    "Spec :267 and brief item 5 :448 require two limits and a test for at least one; C5 level 4 requires a test for each; exemplar A's C5 verdict is consistent with these.")
row("proj-notation-n-undefined", "2.4-notation", "project.html:60 ('denominator n - 1'), :436", P,
    "n is the number of changes in the window (the sample-size symbol of the sample standard deviation). It is not in notation.json, so it cannot collide. The page uses it as the count only (window three: 12 changes, n - 1 = 11 at :436). Judged a clarity point, not a failure.")
row("proj-lab3-raise-claims-untested", "2.5-labs", "project.html:306-308 (lab-3 docstring Check paragraph); tests/", "FAIL",
    f"The three raise claims are true: {S}twin_damaged_r11.out (blank, non-decimal and removed month each raise ValueError naming the cell or month) and the stdev agreement claim (lx1c_r9n04 two-pass divides by n: KILLED, ValueError). But no committed test under tests/ runs them: grep -rn 'damag\\|is blank\\|does not follow' tests/*.py returns nothing and the only project-lab rows in tests/test_labs.py are for S7. They are checked only by kept scripts under ledgers/. Carried defect from rounds 9 and 10.",
    "Add a pytest under tests/ that runs the lab-LX1-project-3 twin on a copy of the snapshot with a blank GBP cell, a non-decimal GBP cell and a removed month, and asserts rc != 0 with a ValueError message naming the cell or month; and that a population-sd variant of the two-pass check raises.")
row("proj-spec-window-start-must", "2.6-spec", "course/modules/LX/LX1/project.html:436", P,
    "Round-10 FAIL cleared: the sentence now reads 'the window start is a candidate limit of the analogy, which the essay may name or not'. The essay is not required to name it; the spec (:267) and brief item 5 require two limits. Consistent with the lab, which computes no other start.")
row("proj-rubric-c2-gap", "2.6-rubric", "course/modules/LX/LX1/project.html:478 (C2 level 2 cell)", "FAIL",
    "C2 level 2 reads 'Lists similarities and one difference, or gives a chain of steps but names no failure step.' An essay with a chain of two steps for each mechanism that names the failure step with its evidence matches no descriptor: level 3 needs chains of at least three steps, level 2 needs no failure step (or a similarity-and-difference list), and level 1 needs no chain. Under the highest-level rule it is unscored.",
    "Change the C2 level 2 cell to: 'Lists similarities and one difference; or gives a chain of steps but names no failure step; or gives a chain of fewer than three steps for either mechanism.' Keep levels 1, 3 and 4.")
row("proj-exemplar-A-limit1-cip-locator", "2.1-citations", "course/modules/LX/LX1/project.html:539; course/modules/LX/LX1/L04.html:329", "FAIL",
    "Exemplar A limit one says the snapshot 'cannot test the relation between interest rates and exchange rates, such as covered interest parity, which Lesson 4 names but does not state or test (Lesson 4, Section 4, item \"Exchange rates only\")'. At this pin no LX1 lesson or page names covered interest parity (grep -ri 'covered interest' course/modules/LX/LX1/ returns only project.html:539). Commit 11d7077 rewrote L04.html:329 ('The lab cannot test any relation between interest rates and exchange rates, because the file has no interest-rate column, and this lesson states none'), which removed the naming (git diff 00a84795 11d7077). The attribution to Lesson 4 is false.",
    "In project.html:539 drop the attribution to Lesson 4 for covered interest parity (for example: 'so it cannot test any relation between interest rates and exchange rates, such as covered interest parity (Lesson 4, Section 4, item \"Exchange rates only\", which says the file has no interest-rate column and the lab tests no such relation)'), or restore the naming in L04.html:329 in its own slice. Re-run check_pages LX1 and page_smoke.")

verdict = "PASS" if all(r["status"] == P for r in R) and all(m["killed_by"] for m in mutants) else "FAIL"
counts = {s: sum(1 for r in R if r["status"] == s) for s in ("PASS", "FAIL", "UNVERIFIABLE")}
frag = {
    "unit": "LX1",
    "slice": "LX1-c",
    "round": 11,
    "verifier": "Claude Haiku 5.5 (claude-haiku-5-5), independent verifier for LX1-c, round 11 (did not build LX1)",
    "pin": PIN,
    "base": "00a84795f276456fce19d4181373cc4efba11a36 (round-10 pin). Delta in slice: project.html :436, :478, :480, :506; L04.html :222 (lab-4 docstring, not in slice) and :329 (cross-referenced by exemplar A); references.json (registry used_by only); lab-LX1-L04-1.py docstring. Project lab twins, data and MANIFEST byte-identical.",
    "checkout": str(root),
    "scratch": "/tmp/lx1c-r11-scratch (copies of fx_monthly.csv and kept alternatives' outputs); all scripts and outputs kept in ledgers/LX1/scripts/LX1-c-r11/",
    "verified_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
    "verdict": verdict,
    "rows": R,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Round-10 rows re-verified this round (all subjects read or re-run); none carried except proj-data-snapshot-rebuild, carried from round 8 with the byte-identity condition stated in its evidence.",
        "Blind calibration is UNVERIFIABLE because this verifier read the annotations before scoring (see proj-calibration-exemplars).",
        "Rubric reading convention: 'Names one limit' (C5 level 2) and 'except one' (C4 level 3) are read as at-least-one and at-most-one respectively, as the highest-level rule implies; under that reading C1, C3, C4 and C5 are exhaustive. C2 is not (proj-rubric-c2-gap).",
        "Registry observation (not a project-page finding): references.json adds LX1 to used_by of reinhart2009this at 11d7077; no LX1 page on the project slice cites that key.",
        "Spec questions a competent student would still ask: (1) whether self_assessment.md is submitted or only the form output (:267); (2) what counts as one factual claim for the C3 count; (3) whether two printed pages means the printer's default type size (:267); (4) whether a computed number includes a count such as 668 changes (not a rounded statistic).",
        "Lab 3 agreement tolerance (1e-9 percent, twin line 331) cannot be reached by any input (two-pass and statistics.stdev differ only at float rounding); recorded as an untested constant, not a finding.",
        "Lab 3 rounding: a banker's-rounding variant survives because no printed value is an exact binary tie; lab twins are demonstrations and no page sentence says the lab detects it.",
        "Observation, not a finding: rung 2's expected block shows the answer values on the page; a pedagogical choice.",
    ],
    "summary": f"LX1-c round 11: verdict {verdict}. {len(R)} rows: {counts['PASS']} PASS, {counts['FAIL']} FAIL, {counts['UNVERIFIABLE']} UNVERIFIABLE. Mutants {sum(1 for m in mutants if m['killed_by'])}/{len(mutants)} killed (50 existing plus 3 new). Labs 1-3 pass alone under python -I -W error with output equal to the expected blocks; run_labs LX1 7/7; five alternatives match.",
}
out = root / "ledgers/LX1/LX1-c.json"
out.write_text(json.dumps(frag, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out, "rows", len(R), counts, "mutants", len(mutants))
