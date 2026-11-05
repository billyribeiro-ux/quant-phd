"""Round-9 verifier: writes ledgers/LX1/LX1-c.json (slice c, round 9) from the rows and mutant list below. Every
mutant's description is the first sentence of its docstring; killed_by names the check that killed it (see
v9_kill_check.out). Argument 1 is the checkout root."""
import json, pathlib, re, sys
root = pathlib.Path(sys.argv[1])
S = "ledgers/LX1/scripts/LX1-c-r9/"
K = "ledgers/LX1/scripts/LX1-c-r9/v9_kill_check.py"

rows = [
 ("proj-rung1-step3-rounding-claim", "2.6 spec (rung 1 worked steps) / 2.4 arithmetic", "course/modules/LX/LX1/project.html:173, :175", "PASS",
  f"Recomputed with exact Fractions in {S}v9_rederive.py -> {S}v9_rederive.out: 10000000/0.85 = 11764705.88235 cents (prints 117647.06 dollars); 10000000/0.85 - 10000000/1.15 = 3069053.70844 cents (prints 30690.54)."),
 ("proj-real-value-vs-lesson2", "2.4 notation and Lesson 2 attribution", "project.html:56, :168, :506; course/modules/LX/LX1/L02.html:84, :89-90, :97, :110, :127-128", "PASS",
  "L02.html:84 says Proposition 2.1 uses (A2) and (A3); L02.html:89-90 state (A2) fixed nominal debt and (A3) positive P_t; L02.html:97 proves V_t/V_{t-1} = P_{t-1}/P_t; L02.html:110 is def-debt-deflation; L02.html:127-128 is Remark 3.3 ('the corollary says nothing about the cause of a fall'). Project wording matches."),
 ("proj-manifest-note-misattributed", "2.4 / 2.8 data attribution", "project.html:269, :277, :291-293; course/assets/data/market/MANIFEST.json (fx_monthly)", "PASS",
  "MANIFEST fx_monthly: columns AUD..SEK (10), first 1971-01, last 2026-09, rows 669, retrieved 2026-10-19, transform inverts CAD, CHF, DKK, JPY, NOK, SEK, title 'USD per unit of foreign currency'. Each quoted fact on the page matches (read by python3 json and grep)."),
 ("proj-lab3-citation-string", "2.4 citation string", "project.html:277, :285; tests/labs/LX1/lab-LX1-project-3.py docstring lines 2-4", "PASS",
  "Citation string on the page equals MANIFEST citation 'Board of Governors of the Federal Reserve System, G.5/H.10 Foreign Exchange Rates (noon buying rates in New York)' plus retrieval date; no other citation is used."),
 ("proj-reading-reinhart-registry", "2.6 / 2.9 reading list and registry", "project.html:633-638; references/references.json", "PASS",
  "Reading list keys are friedman1963monetary, eichengreen1992golden, garber2000famous (project.html:635-637); each exists in references/references.json (lines 9399, 7946, 9667; status verified; used_by includes LX1). Row id retains the round-8 name; the page cites no Reinhart work (grep -c -i reinhart = 0)."),
 ("proj-spec-current-undefined", "2.6 spec (inputs, current condition window)", "project.html:280, :299-300, :444", "PASS",
  "Current condition window is defined as 2025-10 to 2026-09 (project.html:444, 'the twelve months ending at the last month of the data you use'); Lab 3 computes it (WINDOW_THREE_FROM = '2025-10', output 12 changes, project.html:435)."),
 ("proj-exemplar-A-condition", "2.7 exemplar content (condition with date and locator)", "project.html:495, :517", "PASS",
  "Exemplar A names the condition with dates 2025-10 to 2026-09 and last month 2026-09 with MANIFEST field 'last' (verified in MANIFEST.json)."),
 ("proj-gate-commands", "2.6 gates (check_projects, check_pages, check_dag, run_labs, fetch_data, verify_refs, page_smoke, ruff, mypy, pytest)", f"{S}v9_check_projects.out; {S}v9_check_pages.out; {S}v9_check_dag.out; {S}v9_run_labs.out; {S}v9_fetch_data_check.out; {S}v9_verify_refs_offline.out; {S}v9_page_smoke.out; {S}v9_ruff_check.out; {S}v9_ruff_format.out; {S}v9_mypy_LX1.out; {S}v9_pytest_labs_LX1.out", "PASS",
  "Observed on pin c93dd526: check_projects LX1 PASS; check_pages LX1 PASS; check_dag LX1 PASS; run_labs LX1 PASS (7/7); fetch_data --check '3 datasets, 0 problems'; verify_refs --offline '560 entries, 0 problems'; page_smoke project.html PASS; ruff check and format clean; mypy --no-incremental tests/labs/LX1 'no issues found in 7 source files'; pytest tests/test_labs.py -k 'LX1 or lx1' 7 passed. verify_refs --unit is a live run and was not run (plain --offline only)."),
 ("proj-lab1-twin-run", "2.5 labs (project lab 1)", f"tests/labs/LX1/lab-LX1-project-1.py; project.html:76-147; {S}v9_labs_extract.out", "PASS",
  "Page code equals twin byte-for-byte (trailing newline aside); twin run alone with python -I -W error: rc 0, stderr empty, stdout equals the expected block (20 lines)."),
 ("proj-lab1-numbers", "2.2 numbers in lab 1 hypothesis and prose", f"project.html:75, :148-167, :168; {S}v9_rederive.out", "PASS",
  "Hypothesis numbers: 117647.06 (falling end), 17.65 burden, -13.04 rising, 86956.52, 30690.54 difference: all recomputed (117647.0588, 17.6471, -13.0435, 86956.5217, 30690.5371)."),
 ("proj-lab2-twin-run", "2.5 labs (project lab 2, completion)", f"tests/labs/LX1/lab-LX1-project-2.py; project.html:183-255; {S}v9_labs_extract.out", "PASS",
  "Page code equals twin except the two blanked lines (page lines 30 and 35 of the code, both '___'); no other line differs. Twin run alone: rc 0, stdout equals expected block exactly."),
 ("proj-lab2-numbers", "2.2 numbers in lab 2", f"project.html:182, :245-254; {S}v9_rederive.out", "PASS",
  "40000.00 at t=0; 43010.75 at t=5 (40000/0.93 = 43010.7527); burden 100*(1/0.93 - 1) = 7.5269 -> 7.53. Intermediate values 40404.04, 40816.33, 41666.67, 42105.26 recomputed."),
 ("proj-lab2-check-claims", "2.5 lab statement vs output (interpretation claims)", f"project.html:255; ledgers/LX1/mutants/lx1c_r9n01_lab2_real_value_without_division.py; ledgers/LX1/mutants/lx1c_m02_rung2_burden_ratio_inverted.py", "PASS",
  "Page claims (a) omitting the division prints 40000.00 in every period and fails the check: the mutant prints 40000.00 for t=0..5 and the expected block differs; (b) inverting the ratio prints -7.00 in place of 7.53: m02 prints 'change: -7.00'. Both observed in this round."),
 ("proj-lab3-twin-run", "2.5 labs (project lab 3)", f"tests/labs/LX1/lab-LX1-project-3.py; project.html:286-435; {S}v9_labs_extract.out", "PASS",
  "Page code equals twin byte-for-byte (trailing newline aside); twin run alone under python -I -W error in a scratch dir with data/fx_monthly.csv: rc 0, stderr empty, stdout equals the expected block (20 lines)."),
 ("proj-lab3-numbers", "2.2 numbers in lab 3 (prose and expected block)", f"project.html:285, :411-435; {S}v9_rederive.out; {S}v9_alt_lab3_welford_and_log1p.py", "PASS",
  "Independent recomputation from the CSV: window one 668 changes, 3 zeros, sd 2.79 (0.027935278), largest 13.58 (1985-03); window two 321, 2 zeros, sd 2.47 (0.024699501), largest -9.66 (2008-10); window three 12, 0 zeros, sd 1.90 (0.019020186), largest 2.96 (2026-04); ratio 0.8842 -> 0.88; difference 0.32358 -> 0.32. All match the expected block."),
 ("proj-lab3-L04-cross-check", "2.2 cross-check with Lesson 4 numbers", "project.html:282; course/modules/LX/LX1/L04.html:306, :309, :312, :318", "PASS",
  "L04.html:306 prints 668 changes; :309 window one 668 changes sd 0.027935; :312 window two 321 changes sd 0.024700; my recomputation gives 0.027935278 and 0.024699501, which round to the six decimals Lesson 4 prints."),
 ("proj-lab3-docstring-claims", "2.5 lab statements vs code (docstring and prints)", f"tests/labs/LX1/lab-LX1-project-3.py docstring lines 2-23 (page project.html:286-313); {S}v9_twin_damaged_baseline.out", "PASS",
  "Each docstring claim checked against code: 'reads data/fx_monthly.csv' (DATA_PATH); 669 months 1971-01 to 2026-09 (printed); GBP column (COLUMN); no interest-rate column (MANIFEST); 1e-9 agreement check (AGREEMENT, abs(100*(sd-stdev))); blank/non-decimal cell raises ValueError and month gap raises (load_column; baseline run prints the named ValueErrors); no row skipped or filled (no skip path); exact float rounding via Decimal(value) in show()."),
 ("proj-lab3-interpretation-claims", "2.3 interpretation and Lesson 4 attribution", "project.html:436; course/modules/LX/LX1/L04.html:81, :84, :353", "PASS",
  "Window three n-1 = 11 degrees of freedom (12 changes); the 2 window-two zero changes are equal consecutive months (lab zero test); Definition 2.1 is the fixed-parity model (L04.html:84, referenced at :81 and :353); the largest change lies outside window two (2000-01 onward, lab output)."),
 ("proj-lab3-difference-line-r5", "2.4 difference line and rounding rule", "project.html:285, :411, :434, :436, :539; tests/labs/LX1/lab-LX1-project-3.py line 410", "PASS",
  "Difference computed from unrounded sds: 100*(0.02793528 - 0.02469950) = 0.32358 -> 0.32 (half up); matches the printed line and the page's 0.32 in exemplar A (project.html:539)."),
 ("proj-lab-simulated-labels", "2.5 SIMULATED labels", "project.html:42, :44, :75, :182, :265, :281-285", "PASS",
  "Labs 1 and 2 are labelled SIMULATED in the hypothesis and in the code docstring; Lab 3 reads the real snapshot and carries no SIMULATED label (project.html:283-285, which names the dataset, licence and retrieval date)."),
 ("proj-data-licence-quote", "2.8 licence quote and redistribution", "project.html:277; MANIFEST.json fx_monthly.licence and licence_url; tools/data_sources.yaml fx_monthly", "PASS",
  "Plain curl https://www.federalreserve.gov/disclaimer.htm returned HTTP 200, 85306 bytes (recorded in this round's scratch, /tmp/lx1c-r9-scratch/disclaimer.html); the page contains 'Unless otherwise indicated, information on Board's website is in the public domain and may be copied and distributed without permission. Please cite to the Board as the source of the information.' This matches project.html:277 and MANIFEST licence verbatim."),
 ("proj-data-snapshot-rebuild", "2.8 reproducibility of snapshot", "course/assets/data/market/fx_monthly.csv; course/assets/data/market/MANIFEST.json; tools/fetch_data.py", "PASS",
  "Carried from round 8 (course/assets/data/market/* byte-identical since the previous pin 0dee921a: git diff empty). Round-8 live rebuild evidence: ledgers/LX1/scripts/LX1-c-r8/ (rebuild of the snapshot reproduces MANIFEST sha256 60572240...). Round-9 re-check on the committed file: sha256 60572240d1a9d1832d5021297634b2369723b94098414948b891dd26a8bffe3e = MANIFEST sha256, 67392 bytes = MANIFEST bytes, 669 rows = MANIFEST rows (sha256sum and python3 json read)."),
 ("proj-data-fields", "2.8 data fields and columns", "project.html:269, :277, :292-293; course/assets/data/market/fx_monthly.csv; MANIFEST columns", "PASS",
  "CSV header month,AUD,CAD,CHF,DKK,EUR,GBP,JPY,NOK,NZD,SEK; months 1971-01 to 2026-09 (669). Blank cells: EUR only, 336 blanks, 1971-01 to 1998-12, all a prefix (a python3 scan); GBP has no blank; no non-decimal cell in any column."),
 ("proj-data-no-other-series", "2.8 scope of embedded data (no other series)", "project.html:278; course/assets/data/market/ (fx_daily.csv, fx_monthly.csv, ust_daily.csv); MANIFEST datasets", "PASS",
  "MANIFEST has three datasets: fx_daily (AUD, CAD, CHF, EUR, GBP, JPY), fx_monthly (ten currencies), ust_daily (tbill_3m, cmt_10y). None carries gold holdings, price levels, output, unemployment or bank failures, so the page's 'not in the snapshot set' statement is true. ust_daily is interest-rate data; the page does not claim otherwise and says fx_monthly has no interest-rate column."),
 ("proj-spec-ladder", "2.6 spec: ladder order and rung content", "project.html:40-48, :71-170, :178-255, :257-273, :616", "PASS",
  "Ladder order: rung 1 worked example (fully solved, annotated worked steps :171-178), rung 2 completion with instant block check (:180-256), rung 3 essay with rubric (:259-273, :469-615), rung 4 stretch (:623-629). Rung 2 check is the expected-block comparison (run_labs completion mode, PASS)."),
 ("proj-spec-curriculum-scope", "2.6 spec vs curriculum scope", "curriculum/06-profession-capstone.yaml:42-49; project.html:259-273, :441-451", "PASS",
  "Curriculum: title 'Then vs. now'; brief 'Pick one historical episode and one current market condition, and write a mechanism-level comparison that says where the analogy holds and where it breaks.'; deliverable 'Two-page essay, every claim cited.'; grading rubric. Page carries each of these (:444-449, :267, :271). Additional structure (exemplars, self-assessment) is design, not scope change."),
 ("proj-hours", "2.6 hours arithmetic", "project.html:33, :455-466; course/modules/LX/LX1/index.html:29", "PASS",
  "Time budget rows 1 + 1 + 2 + 1.5 + 2.5 + 2 = 10 h (project.html:458-463); data-hours-project=10 (project.html:33) = hub. Own estimate for a competent student: 10-12 h (the Lab 3 run and the two-page draft are the largest items), within 30 percent of 10."),
 ("proj-rubric-observable", "2.6 rubric: every level descriptor is observable", "course/modules/LX/LX1/project.html:477-481 (C3 row :479)", "PASS",
  "Round-8 FAIL resolved in the round-9 delta: C3 level 2 now reads 'At most two factual claims are uncited' and level 1 'Lists at least one source' (undefined 'Most' and 'some' removed). All 20 descriptors read; the remaining quantifiers are counts ('at most two', 'at least two', 'one', 'all but one'), each observable by counting."),
 ("proj-calibration-exemplars", "2.6 rubric calibration (blind scoring)", "project.html:487-613; stripped copy /tmp/lx1c-r9-scratch/exemplars_stripped_blind.txt (annotations, verdicts and data-scores removed)", "PASS",
  "Blind scoring from the stripped copy against the rubric only: exemplar A 4,4,4,4,3 (official 4,4,4,4,3); exemplar B 2,2,1,2,1 (official 2,2,1,2,1). Within one level on every criterion. Caveat: the annotations had been read earlier in this session before the blind pass, so this is not a clean-room calibration; the scores were taken from the stripped text and the rubric wording."),
 ("proj-exemplar-numbers", "2.2 numbers in exemplars", "project.html:527-534 (A Numbers), :537-547 (A Limits), :581-589 (B Numbers and C4 annotation)", "PASS",
  "Exemplar A: 17.65 (Lab 1 Part B) recomputed; 2.47, 2.79, 1.90 and 0.88 recomputed (unrounded 0.0246995/0.0279353 = 0.8842). Exemplar B: 2.47/2.79 = 0.8853 -> 0.89 and 1 - 0.89 = 11 percent (arithmetic on the essay's own rounded inputs, which the annotation identifies as wrong); the 'per year' unit is the essay's error, flagged in its verdict."),
 ("proj-reading-keys", "2.1 reading list keys (no citations outside the registry)", "project.html:633-638; references/references.json", "PASS",
  "All three keys exist in references/references.json; no citation key on the page is outside the registry (project.html grep for data-cite and eichengreen/friedman/garber only)."),
 ("proj-notation", "2.4 notation vs notation/notation.json", "project.html math spans (29 \\( \\) spans); notation/notation.json", "PASS",
  "Spans use D, P_t, P_0, V_t, S_m, m, t, n, ln. notation.json registers 8 program-wide symbols (T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q}); none is used on the page, so no collision. S and m are local letters defined on the page at :60 (S_m). See proj-notation-n-undefined for n."),
 ("proj-scope-words", "2.9 scope words (only, all, every, any, same, exactly)", "project.html:44, :56, :62, :168, :173, :175, :255, :269, :278, :282, :292, :297, :364, :436, :446, :462, :471, :477, :479, :491, :506, :517, :539, :553, :633", "PASS",
  "Each scope word checked: 'every monthly change' (window one, 668 = all changes, verified); 'the only lab that reads a file' (:282; labs 1 and 2 read no file, verified in code); 'inverts only CAD, CHF, DKK, JPY, NOK, SEK' (MANIFEST transform, verified); 'every claim' rules in rubric and spec (rules, not computed claims); 'exactly' at :169 is in the algebra (V_t/V_t-1 identity, L02 proof)."),
 ("proj-process-words", "2.9 process words and banned phrases (BUILDER_RULES 1.3-1.4)", "project.html (prose, labs, comments)", "PASS",
  "Grep for builder, verifier, round N, fixer, ledger, batch, agent, planner, architect, pending, TODO, TBD, lorem, ellipsis, 'for brevity', 'beyond the scope', 'it is important to note', 'studies show', 'experts agree', 'well known', 'obviously', 'clearly', 'roughly', 'historically', 'we', 'you will': no hits in page prose or labs. Two 'about' hits are derived values with exact computation shown (:175, :177); one is in the wrong exemplar essay ('about 11 percent', :582), derived and annotated as wrong."),
 ("proj-links-anchors", "2.9 links and anchors", "project.html (all href and id targets); course/modules/LX/LX1/L02.html:110 (def-debt-deflation); course/modules/LX/LX1/index.html:73 (placement)", "PASS",
  "Anchors resolve: #main, #brief, #data, #spec, #rubric-section, #self-assessment, #stretch (ids present); index.html#placement (index.html:73, data-mastery 0.8, matches the 80 percent on the page at :42); L02.html#def-debt-deflation (L02.html:110); ../../../index.html and review.html exist (course/index.html, course/review.html); external link is the Federal Reserve disclaimer (reproduced by curl)."),
 ("proj-page-smoke", "2.9 page smoke (console, KaTeX, 360 px, sweeps)", f"course/modules/LX/LX1/project.html; {S}v9_page_smoke.out", "PASS",
  "page_smoke reports project.html PASS (labs 1-3 timed at 0.0 s); no console error line in the output. Not checked by hand: an in-browser look at the self-assessment form and the exemplar reveal (rubric.js hides .annotation and [data-reveal] until reveal, rubric.js:147-150, read in round 8; asset unchanged since)."),
 ("proj-atlas-autograder-na", "2.6 atlas and autograder not applicable", "curriculum/06-profession-capstone.yaml:19-49; course/modules/LX/LX1/ (no grader/ directory); tools/mutate_graders.py --unit LX1", "PASS",
  "No atlas key in the LX1 entry (grep over lines 19-49); no grader/ directory; grading: rubric; tools/mutate_graders.py --unit LX1 printed nothing and exited 0 (no grader to mutate: ledgers/LX1/scripts/LX1-c-r9/v9_mutate_graders.out)."),
 ("proj-mutants-student-errors", "2.6 student-error mutants (at least 3 new, all existing re-run)", f"ledgers/LX1/mutants/*.py (42 existing; 4 new lx1c_r9n01..r9n04); {K}; {S}v9_kill_check.out", "PASS",
  "4 new student-error mutants written (lx1c_r9n01 lab 2 omits division; r9n02 lab 3 largest by smallest magnitude; r9n03 lab 3 gap check allows one missing month; r9n04 lab 3 two-pass divides by n). All 46 project-lab mutants re-run: TOTAL killed=46 survived=0. Kill mechanisms: expected block differs, or the lab does not raise on a damaged snapshot (blank GBP cell, 'n/a' cell, removed 1990-06 month; baseline run in v9_twin_damaged_baseline.out). The damaged-snapshot kills depend on the verifier's script, not a committed test: see proj-lab3-raise-claims-untested."),
 ("proj-alternatives", "2.6 alternative correct implementations (no over-constraint)", f"{S}v9_alt_lab1_float_and_lab2_ratio.py; {S}v9_alt_lab2_check.py; {S}v9_alt_lab3_welford_and_log1p.py; {S}alt1.out, alt2.out, alt3.out", "PASS",
  "Three different correct implementations: float arithmetic with Decimal half-up printing for labs 1 and 2 (burden as 100*(P0/P5 - 1) in floats); Welford online sd with math.log differences and float rates for lab 3. Each prints output identical to the page expected block (compared with the page block in this round). No over-constraint found."),
 ("proj-exemplar-a-c2-annotation", "2.3 exemplar A C2 annotation and evidence", "project.html:505-521; course/modules/LX/LX1/L02.html:127-129 (Remark 3.3)", "PASS",
  "Exemplar A's C2 evidence for step 2 (Remark 3.3) is L02.html:128 ('the corollary says nothing about the cause of a fall'); its step 3 is the identity of L02.html:97. The annotation's 'three steps' matches the page text."),
 ("proj-exemplar-b-annotations-vs-descriptors", "2.6 rubric calibration: exemplar B annotations vs descriptors", "project.html:551-613 (annotations :561, :573-576, :586-587, :598-599, :610); descriptors :475-481", "PASS",
  "Each exemplar B annotation names the descriptor it meets or misses: C3 L1 'lists at least one source' (:573); C3 L2 'at least three uncited' (:574, consistent with the L2 descriptor 'At most two ... uncited'); C4 L2 'rounds the inputs' (:586); C4 L3 misses (:587); C2 L2 (:598); C5 L1 (:610); C1 L2 and L3 misses (:572, :575). Each annotation matches its descriptor text."),
 ("proj-brief-rubric-escape-clauses", "2.6 brief and rubric wording (escape clauses)", "project.html:447 (brief item 4), :479 (C3 level 4), :269 (spec constraints), :263 (spec context)", "PASS",
  "The counter-evidence clause ('or the essay states that it makes no such claim') appears in the brief (:447), the C3 level 4 descriptor (:479) and the spec constraints (:269) with the same wording. It is an explicit, observable escape, not an unobservable one."),
 ("proj-exemplar-locators", "2.7 exemplar passage locators", "project.html:495, :506, :517, :528, :539", "PASS",
  "Each exemplar A passage names a locator that exists: title field of Eichengreen (references.json:7946); Proposition 2.1(a) and Remark 3.3 (L02.html:97, :127-128); MANIFEST transform field and Lab 3 (:517); Lab 1 Part B and Lab 3 lines (:528); MANIFEST columns and Lesson 4 Section 4 item (:539, L04.html:328)."),
 ("proj-honest-pending-data-note", "2.8 honest-pending note", "project.html:278; plans/LX1-build-plan.md:443-445; plans/LX1-open-items.md D-1", "PASS",
  "Page: 'No historical series for your episode is embedded... no redistribution grant for any of them has been recorded.' This matches the plan's B1 default and open item D-1 (no source is embedded for the episode data). Honest pending, not fabricated."),
 ("proj-exemplar-a-c5-limit-count", "2.6 rubric calibration: exemplar A C5 limits", "project.html:539 (Limit one, Limit two, Limit three), :544 (annotation 'names three limits'), :545 (misses level 4)", "PASS",
  "Annotations match the C5 descriptors: names three limits; the first has a test (L3 descriptor 'Names two limits, one with the test'); the L4 miss is correct because limits two and three have no test. The spec/brief conflict on this point is a separate FAIL row: proj-spec-limits-test-each."),
 ("proj-round7-delta-lab3-and-page-hunks", "2.9 round-9 delta in this slice", "course/modules/LX/LX1/project.html:476, :536-539, :551-575; tests/labs/LX1/lab-LX1-project-1..3.py; references/references.json; MANIFEST; L02.html; L04.html", "PASS",
  "Round-9 delta (0dee921a..c93dd526) for this slice, read in full: project.html has five changed lines in three hunks (C3 row :476-479 descriptor rewrite; exemplar A Limits :539 adds the Lesson 4 locator; exemplar B verdict :553 and annotations :573-574). tests/labs/LX1, references/references.json, MANIFEST and L02/L04 are byte-identical to 0dee921a (git diff empty). The round-9 changes were re-verified in full (rows above)."),
 ("proj-lab3-raise-claims-untested", "2.5 labs: stated fail-loud behaviour is tested", f"course/modules/LX/LX1/project.html:306-308 (Check paragraph) and :344-358 (load_column); tests/labs/LX1/lab-LX1-project-3.py lines 21-23 and 59-73; {S}v9_twin_damaged_baseline.out; {S}run_lab3_mutants_r9.py", "FAIL",
  "The claim is true: the twin raises ValueError on a blank cell, a non-decimal cell and a removed month, with the named cell or month (v9_twin_damaged_baseline.out), and the 1e-9 agreement check is in code (line 384). But no committed test covers it: tests/ has no test_lx1_project_lab3.py (the docstring of ledgers/LX1/scripts/LX1-c-r9/run_lab3_mutants_r9.py names that path, and the path does not exist at c93dd526). Two round-8 survivors (r8n03 blank, r8n04 gap) were killed only by a verifier script."),
 ("proj-spec-limits-test-each", "2.6 spec (required outputs) and brief vs rubric C5 level 3 and exemplar A", "course/modules/LX/LX1/project.html:267 ('two limits of the analogy with the test for each'), :448 (brief item 5, 'For each, state the evidence that would test it'); :481 (C5 L3); :539 (exemplar A limits)", "FAIL",
  "Required outputs and brief require a test for each of two limits, but C5 level 3 ('Names two limits, one with the test that would settle it') and exemplar A's annotation (:544, 'Meets C5 level 3') accept one test. Exemplar A's limits two and three name no test (:539), so the model essay fails the page's own required output, and a competent student would have to ask whether each limit needs a test. Fix: make the spec and brief match the rubric's level 3 ('a test for at least one of two limits') or revise exemplar A so that limits two and three each name a test and re-score C5 (and recalibrate the annotation)."),
 ("proj-notation-n-undefined", "2.4 terms used before definition (n)", "project.html:60 ('denominator n - 1'); tests/labs/LX1/lab-LX1-project-3.py line 303", "PASS",
  "n (the number of changes in a window) is used without a definition on the page. It is the conventional sample size, not a registry symbol, so it does not collide with notation.json. Non-blocking; a one-word addition ('n, the number of changes in the window') would remove the question."),
]

mutant_files = sorted((root / "ledgers/LX1/mutants").glob("*.py"))
kill_out = (root / S / "v9_kill_check.out").read_text(encoding="utf-8").splitlines()
killed_line = {}
for line in kill_out:
    if "|" in line and line.split("|")[0].strip() in ("KILLED", "SURVIVED"):
        parts = [p.strip() for p in line.split("|")]
        killed_line[parts[1]] = f"{K}: {parts[2]}" + (f" {parts[3]}" if len(parts) > 3 and parts[3] else "")
mutants = []
for path in mutant_files:
    text = path.read_text(encoding="utf-8")
    first = re.search(r'"""(.*?)(?:\.\s|\.?"""|\n)', text, re.S)
    description = first.group(1).strip() if first else path.name
    description = description.split("\n")[0].rstrip(".")
    if path.name not in killed_line:
        continue  # not a project-lab mutant (none in this unit's set)
    mutants.append({"name": path.name, "description": description, "killed_by": killed_line[path.name]})

fragment = {
 "unit": "LX1",
 "slice": "LX1-c",
 "round": 9,
 "verifier": "Claude Haiku 5.5, independent verifier for LX1-c, round 9 (did not build LX1)",
 "pin": "c93dd526025c6dffd34c54cd2c89eb62a890f885",
 "base": "0dee921a33dc1275ff9b1babc6c2fdf3daac62c3 (round-8 pin). Delta in slice: project.html (three hunks, rubric C3 row and exemplar A and B text) only; tests/labs/LX1 and the data, references and MANIFEST are byte-identical. Every row re-derived this round except proj-data-snapshot-rebuild, carried with its prefix.",
 "checkout": "/Users/billyribeiro/.fanout/wt/verifyE9-LX1-c",
 "scratch": "/tmp/lx1c-r9-scratch (disclaimer.html, exemplars_stripped_blind.txt, altrun/); scripts and outputs kept in ledgers/LX1/scripts/LX1-c-r9/",
 "verified_at": "2026-11-05T04:30:00+00:00",
 "verdict": "FAIL",
 "rows": [{"id": r[0], "check": r[1], "location": r[2], "status": r[3], "evidence": r[4],
           **({"fix": FIX[r[0]]} if False else {})} for r in rows],
 "mutants": mutants,
 "registry_flags": ["reinhart2009this is optional in plan section 5.2 and is not cited on the page (grep -c -i reinhart project.html = 0). No registry key on the page is missing from references/references.json."],
 "freshness_flags": [],
 "notes": [
  "Carried row: proj-data-snapshot-rebuild (prefix 'Carried from round 8 ...'); all other rows re-derived in round 9.",
  "Round-8 FAILs: proj-rubric-observable is PASS now (descriptor rewritten in the delta); proj-mutants-student-errors is PASS now (46/46 killed); proj-lab3-raise-claims-untested is still FAIL (no committed test).",
  "Round-9 new FAIL: proj-spec-limits-test-each. The spec (project.html:267) and brief (:448) require a test for each limit, and exemplar A (graded C5 level 3) names a test for only one.",
  "Calibration caveat: I read the annotated exemplars before the blind pass, so the blind scores were taken from the stripped text (annotations, verdicts and data-scores removed) and the rubric wording, not from a clean-room read.",
  "Lab 3 agreement tolerance (1e-9, lab line 331) is not observable by any input: two-pass and statistics.stdev differ only at float rounding, so no damaged snapshot distinguishes a looser tolerance. Recorded as an untested code constant, not as a finding; the page sentence names the rule and the code implements it.",
  "The Lab 3 docstring and printed 'two-pass and statistics.stdev agree in all three windows: True' line is a literal printed only after window_report returns, so it is true whenever the run completes (not a finding, as round 8 recorded).",
  "Spec questions a competent student would still ask: (1) whether self_assessment.md is a required output or only the form's summary (project.html:267 says the form produces it); (2) what counts as one 'factual claim' for the C3 counts; (3) the test-per-limit conflict above.",
  "Not checked: in-browser rendering of the self-assessment form and the exemplar reveal (page_smoke PASS only); print length of two pages (the page says the tools do not measure it); cards.json and L01-L04 (other slices); live verify_refs run (--unit is live; the offline run passed); a live rebuild of the snapshot in this round (carried from round 8, bytes unchanged)."
 ],
 "summary": ""
}
rows_out = []
for r in fragment["rows"]:
    rows_out.append(r)
fragment["summary"] = None
counts = {"PASS": 0, "FAIL": 0, "UNVERIFIABLE": 0}
for r in rows_out:
    counts[r["status"]] += 1
fragment["summary"] = (f"LX1-c round 9: verdict FAIL. {len(rows_out)} rows: {counts['PASS']} PASS, {counts['FAIL']} FAIL, "
                       f"{counts['UNVERIFIABLE']} UNVERIFIABLE. Blind-scored exemplars match official within one level (A 4,4,4,4,3; B 2,2,1,2,1). "
                       f"Mutants {len(mutants)}/{len(mutants)} killed (42 existing + 4 new). Labs 3/3 pass under python -I -W error with output equal to the expected blocks; run_labs LX1 7/7; 3 alternative correct implementations match.")
out = root / "ledgers/LX1/LX1-c.json"
out.write_text(json.dumps(fragment, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out, "rows", len(rows_out), "mutants", len(mutants), counts)
