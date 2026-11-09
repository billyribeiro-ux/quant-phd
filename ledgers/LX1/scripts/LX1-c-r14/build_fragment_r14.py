"""Round-14 verifier: writes the LX1-c fragment (ledgers/LX1/LX1-c.json) from the rows below and the mutant list
built from the kill-check outputs. Argument 1 is the checkout root. Validates with tools/ledger.validate."""
import json, pathlib, sys
from datetime import datetime, UTC
root = pathlib.Path(sys.argv[1])
S = "ledgers/LX1/scripts/LX1-c-r14/out/"
CARRY = "Carried from round 13 (%s byte-identical since the previous pin): "
R = []
def row(id_, check, loc, status, ev, fix=None):
    d = {"id": id_, "check": check, "location": loc, "status": status, "evidence": ev}
    if status != "PASS":
        d["fix"] = fix
    R.append(d)

row("proj-rung1-step3-rounding-claim", "2.5-labs", "course/modules/LX/LX1/project.html:177 (step 3), :175-179", "PASS",
    "Fresh. " + S + "rederive_r14.out: 10000000/0.85 = 11764705.88235... cents, prints 117647.06 dollars; 10000000/0.85 - 10000000/1.15 = 3069053.7084... cents, prints 30690.54; 100*(1/0.85-1) = 17.647 -> 17.65. The step text is unchanged since the pin.")
row("proj-real-value-vs-lesson2", "2.9-prose", "course/modules/LX/LX1/project.html:56, :58; course/modules/LX/LX1/L02.html:83-92", "PASS",
    "Fresh. L02.html:83 V_t = D P_0 / P_t; :84 names (A2) and (A3); :87-92 Proposition 2.1 with (a) V_t/V_{t-1} = P_{t-1}/P_t. Page :56 gives V_t = D/P_t as the P_0 = 1 case of that identity, and the labs' A1/A2 are stated as the labs' own.")
row("proj-manifest-note-misattributed", "2.2-numbers", "course/modules/LX/LX1/project.html:271, :279, :293; course/assets/data/market/MANIFEST.json (fx_monthly)", "PASS",
    "Fresh. MANIFEST fx_monthly: title 'Month-end foreign exchange rates, ten currencies, USD per unit of foreign currency'; transform 'each column's last value in the month', CAD/CHF/DKK/JPY/NOK/SEK inverted; columns AUD..SEK; first 1971-01, last 2026-09, rows 669. Page statements at :271, :279, :293 match these fields.")
row("proj-lab3-citation-string", "2.9-prose", "course/modules/LX/LX1/project.html:279, :287; MANIFEST.json citation", "PASS",
    "Fresh. MANIFEST citation 'Board of Governors of the Federal Reserve System, G.5/H.10 Foreign Exchange Rates (noon buying rates in New York)' equals the :279 citation and the :287 hypothesis text; retrieved 2026-10-19 on both.")
row("proj-reading-reinhart-registry", "2.9-prose", "course/modules/LX/LX1/project.html:633-640; references/references.json", "PASS",
    "Fresh. Reading list (:635-640) holds friedman1963monetary, eichengreen1992golden, garber2000famous; each is in references/references.json with used_by ['LX1']. reinhart2009this is absent from the page (grep count 0), so the registry-only reading list is consistent.")
row("proj-spec-current-undefined", "2.9-prose", "course/modules/LX/LX1/project.html:446 (brief item 1), :62, :300-301", "PASS",
    "Fresh. The current condition is defined as dated within the twelve months ending at the last month of the data (:446); for the snapshot that is 2025-10 to 2026-09, window three of Lab 3 (:62; Lab 3 code WINDOW_THREE_FROM = '2025-10', tests/labs/LX1/lab-LX1-project-3.py).")
row("proj-exemplar-A-condition", "2.6-rubric", "course/modules/LX/LX1/project.html:497, :519", "PASS",
    "Fresh. Exemplar A names window three, 2025-10 to 2026-09, with MANIFEST last = 2026-09 and retrieved 2026-10-19 (MANIFEST.json); " + S + "rederive_r14.out W3: n=12, first 2025-10, last 2026-09. Consistent with :62.")
row("proj-gate-commands", "2.9-prose", "ledgers/LX1/scripts/LX1-c-r14/out/", "PASS",
    "Fresh, all run on 8e5751c with .venv (Python 3.14.8). check_pages LX1 PASS (check_pages.out); check_dag LX1 PASS (check_dag.out); check_projects LX1 PASS (check_projects.out); run_labs --unit LX1 --page project PASS 3/3 (run_labs_project.out); run_labs --unit LX1 PASS 7/7 (run_labs_LX1_all.out); page_smoke --unit LX1 --pages project PASS (page_smoke_project.out); ruff check and ruff format --check on tests/labs/LX1 rc 0 (ruff_check_labs.out, ruff_format_labs.out); mypy --no-incremental tests/labs/LX1 'Success: no issues found in 7 source files' (mypy_labs.out); pytest tests/test_labs.py -k LX1 rc 0, 7 passed (pytest_labs_LX1.out); verify_refs --offline '560 entries, 0 problems' (verify_refs_offline.out); verify_refs --unit LX1 '4 of 560 entries, 0 problems' (verify_refs_unit_LX1.out); fetch_data --check '3 datasets, 0 problems' (fetch_data_check.out); build_site --check 'site data current' (build_site_check.out).")
row("proj-lab1-twin-run", "2.5-labs", "course/modules/LX/LX1/project.html:77-149; tests/labs/LX1/lab-LX1-project-1.py", "PASS",
    "Fresh. run_labs --page project: lab-LX1-project-1 PASS (run_labs_project.out); the twin runs under python -I -W error with empty stderr and its stdout equals the page expected block (:150-171). Twin unchanged since the pin (git diff e919577b..8e5751c empty for tests/labs/LX1/lab-LX1-project-1.py).")
row("proj-lab1-numbers", "2.2-numbers", "course/modules/LX/LX1/project.html:77, :150-171", "PASS",
    "Fresh. " + S + "rederive_r14.out: falling real debt 103092.78, 106382.98, 109890.11, 113636.36, 117647.06; rising 97087.38, 94339.62, 91743.12, 89285.71, 86956.52; burden +17.65 and -13.04; difference 30690.54. All equal :150-171 and the hypothesis at :77.")
row("proj-lab2-twin-run", "2.5-labs", "course/modules/LX/LX1/project.html:184-258; tests/labs/LX1/lab-LX1-project-2.py", "PASS",
    "Fresh. run_labs completion rule PASS: every page line equals the twin line or contains a blank; the completed twin's output equals the expected block (run_labs_project.out).")
row("proj-lab2-numbers", "2.2-numbers", "course/modules/LX/LX1/project.html:184, :247-256", "PASS",
    "Fresh. " + S + "rederive_r14.out: real debt 40404.04, 40816.33, 41666.67, 42105.26, 43010.75 at t=5; burden exact 7.526881... -> 7.53. Matches :184 and :247-256.")
row("proj-lab2-check-claims", "2.5-labs", "course/modules/LX/LX1/project.html:257", "PASS",
    "Fresh. Claim 'a real-value line that leaves out the division prints 40000.00 dollars in every period': 4000000 cents / 1 = 40000.00 at each t. Claim 'a burden line that inverts the ratio prints -7.00': 100*(P_5/P_0 - 1) = 100*(0.93 - 1) = -7.00. Both are the mutants the kill check reports as KILLED (kill_check_all_mutants_existing.out, r13 mutants).")
row("proj-lab3-twin-run", "2.5-labs", "course/modules/LX/LX1/project.html:287-437; tests/labs/LX1/lab-LX1-project-3.py", "PASS",
    "Fresh. run_labs --unit LX1 PASS 7/7 (run_labs_LX1_all.out); the twin runs under python -I -W error in a scratch data/ directory and its stdout equals the expected block (:411-437). Damaged-snapshot runs (blank, non-decimal GBP cell; removed month) raise with the named cell or month for every existing mutant that reaches them (kill_check_all_mutants_existing.out).")
row("proj-lab3-numbers", "2.2-numbers", "course/modules/LX/LX1/project.html:287, :411-437", "PASS",
    "Fresh. " + S + "rederive_r14.out (Decimal, 60 digits, independent of the lab code): W1 n=668, zeros 3, sd 0.02793528 -> 2.79, largest 13.58 at 1985-03; W2 n=321, zeros 2, sd 0.02469950 -> 2.47, largest -9.66 at 2008-10; W3 n=12, zeros 0, sd 0.01902019 -> 1.90; ratio W2/W1 0.884169 -> 0.88; difference W1-W2 0.323578 -> 0.32. All equal :411-437.")
row("proj-lab3-L04-cross-check", "2.9-prose", "course/modules/LX/LX1/L04.html:312-318; project.html:284", "PASS",
    "Fresh. L04.html expected block prints 'changes 668' and 'changes 321', 'standard deviation 0.027935' and '0.024700', ratio 0.8842. My re-derivation gives 0.0279353 and 0.0246995, which round at six places to 0.027935 and 0.024700 (rederive_r14.out). Project :284 statements are consistent.")
row("proj-lab3-docstring-claims", "2.9-prose", "course/modules/LX/LX1/project.html:288-315 (twin docstring mirrored); tests/labs/LX1/lab-LX1-project-3.py load_column, month_index", "PASS",
    "Fresh. load_column raises ValueError on a blank or non-decimal cell (DECIMAL_PATTERN) and on a month that does not follow the previous one (itertools.pairwise check); the damaged-snapshot runs in kill_check_all_mutants_existing.out confirm the messages. The Rounding paragraph (exact binary value, half up, ratio and difference from unrounded values) matches show() and lines 125-126 of the twin. The agreement-raise claim in the same paragraph is NOT covered by these runs; see proj-lab3-raise-claims-untested.")
row("proj-lab3-interpretation-claims", "2.5-labs", "course/modules/LX/LX1/project.html:438 (changed this delta); course/modules/LX/LX1/L04.html:85, :90-94", "PASS",
    "Fresh. Sentence now reads 'Under the fixed-exchange-rate model of Lesson 4 (Definition 2.1), and assuming its (A2) that the rate stays at its fixed exchange rate, Proposition 2.2 ... gives a zero change in every month'. L04.html:85 defines the fixed-exchange-rate model together with (A2) 'fixed rate held'; L04.html:90-94 Proposition 2.2(a) gives every monthly log change zero. The counts 321 and 2, the 13.58 at 1985-03 (outside window two, whose largest is 9.66 at 2008-10), the 11 degrees of freedom and the 0.32 difference all match Lab 3 output and rederive_r14.out. The parity wording of round 13 is gone (grep 'parity' on the page: 0 hits).")
row("proj-lab3-difference-line-r5", "2.2-numbers", "course/modules/LX/LX1/project.html:287, :411, :436, :438; tests/labs/LX1/lab-LX1-project-3.py:125", "PASS",
    "Fresh. Difference line prints 0.32; unrounded 100*(sd_1 - sd_2) = 0.323578 (rederive_r14.out). The twin computes it from unrounded sd_one and sd_two (line 125), so 'computed from unrounded dispersions' at :438 is true.")
row("proj-lab-simulated-labels", "2.8-data", "course/modules/LX/LX1/project.html:42, :44, :77, :184, :267, :282-440", "PASS",
    "Fresh. Labs 1 and 2 are labelled SIMULATED in their hypothesis lines (:77, :184) and their code headers. Lab 3 (:285-439) carries no SIMULATED label and names its file, the licence, and the retrieval date (:287). Lab 3 is the only page lab with data-files (project.html:285; grep count 1).")
row("proj-data-licence-quote", "2.8-data", "course/modules/LX/LX1/project.html:279; https://www.federalreserve.gov/disclaimer.htm (plain curl)", "PASS",
    "Fresh. curl -sS -L https://www.federalreserve.gov/disclaimer.htm returned HTTP 200 (" + S + "licence_page.html); the page contains 'Unless otherwise indicated, information on Board's website is in the public domain and may be copied and distributed without permission. Please cite to the Board as the source of the information.' The page's quoted sentence equals the MANIFEST licence string character for character.")
row("proj-data-snapshot-rebuild", "2.8-data", "course/assets/data/market/fx_monthly.csv; course/assets/data/market/MANIFEST.json (fx_monthly)", "PASS",
    "Fresh live rebuild (rebuild_fx_monthly_r14.sh, out/rebuild_fx_monthly_r14.out): tools/fetch_data.py --fetch --only fx_monthly in an empty scratch copy downloaded the H.10 feed and rebuilt the CSV: 669 rows, 67392 bytes, sha256 60572240d1a9d1832d5021297634b2369723b94098414948b891dd26a8bffe3e = MANIFEST sha256; cmp reports byte-identical to the committed CSV. The live raw file differs from the recorded raw_sha256 (1c312d2f... today versus 8f370f9c... recorded on 2026-10-19), as BUILDER_RULES 6.6 expects for a live file; the rebuild still matches byte-for-byte, and the committed MANIFEST was not refreshed. fetch_data --check: 3 datasets, 0 problems (fetch_data_check.out).")
row("proj-data-fields", "2.8-data", "course/modules/LX/LX1/project.html:271, :279-280, :293; fx_monthly.csv", "PASS",
    "Fresh. EUR blank in 336 rows, first non-blank month 1999-01 (336 = 28 years x 12); GBP blank count 0; 669 months 1971-01 to 2026-09 with no gaps (rederive_r14.out). Matches the page's blank-before-first-observation statement.")
row("proj-data-no-other-series", "2.8-data", "course/modules/LX/LX1/project.html:280; course/assets/data/market/MANIFEST.json ids; tools/data_sources.yaml ids (lines 19, 53, 91)", "PASS",
    "Fresh. The embedded set is fx_daily, fx_monthly and ust_daily only. None is a gold, price-level, output, unemployment or bank-failure series, so 'not in the snapshot set' is true, and the page records no redistribution grant for them.")
row("proj-spec-ladder", "2.6-spec", "course/modules/LX/LX1/project.html:40-48, :72-258, :261-275, :277-441, :443-453, :471-", "PASS",
    "Fresh. Ladder order rung 1 (Lab 1, worked), rung 2 (Lab 2, class 'lab completion'), rung 3 (spec, data, Lab 3, brief, rubric), rung 4 (stretch :625-631). check_projects LX1 PASS (check_projects.out).")
row("proj-spec-curriculum-scope", "2.6-spec", "curriculum/06-profession-capstone.yaml (LX1 project brief); course/modules/LX/LX1/project.html:443-453", "PASS",
    CARRY % "curriculum/06-profession-capstone.yaml and the brief section project.html:443-453" +
    "round-13 comparison of the brief with the curriculum brief. The brief section is unchanged in this delta; the Context/Inputs text that changed (:265-267) still says 'Every claim is cited, with a locator, to a source you have read, or is marked as your own inference', consistent with the curriculum brief.")
row("proj-hours", "2.6-hours", "course/modules/LX/LX1/project.html:33, :457-467; course/modules/LX/LX1/index.html:29", "PASS",
    "Fresh. Table rows 1 + 1 + 2 + 1.5 + 2.5 + 2 = 10 = data-hours-project (:33) = eyebrow '10 hours'. index.html:29 data-hours-lessons=40 and data-hours-project=10, so 40 + 10 = 50 = curriculum hours. My own estimate: rung 1 about 1 h, rung 2 about 1 h, selection and locators 2 to 3 h, outline 1.5 h, drafting 3 h, self-assessment 2 h, total 10.5 to 11.5 h, within 30% of 10.")
row("proj-rubric-observable", "2.6-rubric", "course/modules/LX/LX1/project.html:475-485 (rubric table)", "PASS",
    "Fresh. Each level cell names a checkable element: dates and locators (C1), steps and failure step (C2), citations, uncited count and counter-evidence (C3), rounding rule and lab line (C4), limits and tests (C5). Each cell re-read this round. Descriptor exhaustiveness is recorded under proj-rubric-exhaustive-r14.")
row("proj-calibration-exemplars", "2.6-rubric", "course/modules/LX/LX1/project.html:491-616 (exemplar articles; verdict lines :493, :555); ledgers/LX1/scripts/LX1-c-r14/blind_extract.py; out/blind_exemplars_r14.txt", "UNVERIFIABLE",
    "Blind scores from the essay text only: Exemplar A 4,4,4,4,3 (official 4,4,4,4,3); Exemplar B 2,2,1,2,1 (official 2,2,1,2,1). Both within one level. BUT the blind condition is not met in this session: the verdict lines at project.html:493 and :555 and several annotations were printed in this session's tool output (grep and sed reads) before the scoring, so the scores cannot count as blind. The static HTML also carries the official scoring and the annotations (rubric.js hides them only at runtime), which is the root cause.",
    "Keep the official scoring and annotations out of the static HTML (load them on reveal, as rubric.js already hides them), then a clean-room verifier must score from ledgers/LX1/scripts/LX1-c-r14/out/blind_exemplars_r14.txt before reading any verdict or annotation, and record the scores in a new round.")
row("proj-exemplar-numbers", "2.2-numbers", "course/modules/LX/LX1/project.html:530 (A numbers), :584 (B numbers), :588", "PASS",
    "Fresh. Exemplar A: 17.65 (Lab 1 Part B), 2.47, 2.79, 1.90 (Lab 3), ratio 0.88 (unrounded 0.884169, not 2.47/2.79 = 0.8853), 13.58 at 1985-03, 0.32 difference: all re-derived in rederive_r14.out and rounded half up as stated. Exemplar B: ratio from rounded inputs 0.885 -> 0.89 (annotated as an error). B's 'per year' unit slip is part of its designed failure (its verdict says the volatility is in the wrong unit) and no rubric descriptor depends on units.")
row("proj-reading-keys", "2.9-prose", "course/modules/LX/LX1/project.html:635-640; references/references.json", "PASS",
    "Fresh. data-cite keys friedman1963monetary, eichengreen1992golden, garber2000famous exist in references.json with used_by ['LX1']; the exemplar's Eichengreen title equals the registry title field 'Golden fetters: the gold standard and the Great Depression, 1919-1939'. verify_refs --unit LX1 4 of 560 entries, 0 problems (verify_refs_unit_LX1.out).")
row("proj-notation", "2.9-prose", "course/modules/LX/LX1/project.html (all TeX spans); notation/notation.json symbols", "PASS",
    "Fresh. Registered symbols in notation.json: R^*, R^{e*}, R_f, T, Phi and Phi^{-1}, gamma_3, gamma_4, Q. The project uses D, V_t, P_t, P_0, S_m, n, ln, t, m and none of the registered symbols or macros with another meaning.")
row("proj-scope-words", "2.9-prose", "course/modules/LX/LX1/project.html:62, :68, :177, :265-271, :284, :299, :438, :473, :493, :519, :541, :547", "PASS",
    "Fresh. 'every monthly change' (:62) is the 668 changes of window one (rederive_r14.out W1); 'every run prints the same lines' (Lab 1 has no RNG, :81); 'the only lab on this page that reads a file' (:284; grep count of data-files is 1); 'exact zero change' means a log change equal to 0.0 (Lab 3 code 'value == 0.0'); the zero months match rederive_r14.out (W1 1976-07, 2012-07, 2019-11; W2 2012-07, 2019-11); 'every computed number' (:68, :271) is a requirement, not a claim of coverage; 'every factual claim' in exemplar A (:541, :545) was checked claim by claim against locators.")
row("proj-process-words", "2.9-prose", "course/modules/LX/LX1/project.html (rendered text)", "PASS",
    "Fresh. Text scan (sed tag strip + grep -i for build, builder, verifier, verif*, round, REQUESTS, unit report): no process words in learner text. 'Round once, at print time' (:177) and 'Rounding' (:68, :312) are arithmetic terms.")
row("proj-links-anchors", "2.9-prose", "course/modules/LX/LX1/project.html (all href and id)", "PASS",
    "Fresh. All 10 in-page hash hrefs (main, spec, rubric-section, stretch, brief, data, self-assessment) resolve to ids (python check, missing = []). Cross-page links are checked by check_pages LX1 PASS (check_pages.out); page_smoke reports zero external requests (page_smoke_project.out).")
row("proj-page-smoke", "2.9-prose", "course/modules/LX/LX1/project.html; ledgers/LX1/scripts/LX1-c-r14/out/page_smoke_project.out", "PASS",
    "Fresh. page_smoke --unit LX1 --pages project: PASS, 3 labs run, boot 1.3 s; zero console errors, zero external requests, zero unrendered math (page_smoke_project.out).")
row("proj-atlas-autograder-na", "2.6-spec", "curriculum/06-profession-capstone.yaml:19-49 (grading: rubric); course/modules/LX/LX1/", "PASS",
    CARRY % "curriculum/06-profession-capstone.yaml and plans/LX1-build-plan.md" +
    "round-13 evidence: LX1 grading is rubric; no atlas key; no grader directory. Fresh check: check_projects LX1 PASS (check_projects.out).")
row("proj-mutants-student-errors", "2.6-mutation", "ledgers/LX1/mutants/ (r14n01-r14n03 new; 62 existing); ledgers/LX1/scripts/LX1-c-r14/kill_new_r14.py", "PASS",
    "Three new student-error mutants written this round, each a complete lab variant in ledgers/LX1/mutants/: r14n01_lab3_sd_without_centring_on_mean.py (sd taken about zero), r14n02_lab2_burden_percent_of_end_value.py (burden as percent of the end real value: prints 7.00 for 7.53), r14n03_lab3_difference_printed_in_decimal.py (difference printed in decimal: 0.00 for 0.32). All three KILLED (kill_new_r14.out). The 62 existing mutants re-run with the round-13 harness: 61 KILLED, 1 SURVIVED (r13n03_lab3_agreement_check_removed.py), recorded in proj-lab3-raise-claims-untested. Rulings: labs are demonstrations; a surviving mutant is a finding only where a lesson sentence claims the property, and :60 and :309 do.")
row("proj-alternatives", "2.6-mutation", "ledgers/LX1/scripts/LX1-c-r14/alts/ (alt1-alt3); out/alts_r14.out; ledgers/LX1/scripts/LX1-c-r13/alts/ (round 13 alternatives, not re-run)", "PASS",
    "Three new alternative correct implementations, each run alone under python -I -W error and compared with the page's expected block (run_alts_r14.py, alts_r14.out): alt1 lab 3 with Welford's online variance: MATCH; alt2 lab 1 in float arithmetic with Decimal half-up printing: MATCH; alt3 lab 2 with every rounding done by Decimal quantize (ROUND_HALF_UP): MATCH.")
row("proj-exemplar-b-annotations-vs-descriptors", "2.6-rubric", "course/modules/LX/LX1/project.html:553-616; out/blind_exemplars_r14.txt", "PASS",
    "Fresh. Each B annotation checked against the B essay text and the rubric cells at :475-485: C1 L2 (condition has no date, :574); C3 L1 (Eichengreen title for the episode, H.10 data without locator); C3 L2 miss (three uncited claims: the Summary's 'pound has been volatile' and 'gold standard was meant to stop volatility', and the Mechanism's 'both periods show falls in prices'); C1 L3 miss; C4 L2 (ratio from rounded inputs, 0.885 -> 0.89, unrounded 0.88); C4 L3 miss; C2 L2 (similarities and one difference, no chain); C3 L3 miss; C5 L1 (caveats, no limit). All consistent.")
row("proj-brief-rubric-escape-clauses", "2.6-rubric", "course/modules/LX/LX1/project.html:449 (brief item 4), :265 (context), :481 (C3 L4 and L3)", "PASS",
    "Fresh. Brief item 4 and C3 L4/L3 carry the same B-or-C counter-evidence clause with the 'states that it makes no such claim' escape. Consistent with the context at :265.")
row("proj-exemplar-locators", "2.6-rubric", "course/modules/LX/LX1/project.html:497, :508, :519, :530, :541; L02.html:87-92, :127-128; L04.html:333", "PASS",
    "Fresh. Lesson 2 Proposition 2.1(a) (L02.html:87-92, under (A2) and (A3)); Remark 3.3 (L02.html:127-128: the corollary says nothing about the cause of a fall); Lesson 4 Section 4 item 'Exchange rates only' (L04.html:333, under Section 4 at :329); the Eichengreen period from the title field; MANIFEST last 2026-09. Each locator resolves.")
row("proj-exemplar-a-c5-limit-count", "2.6-rubric", "course/modules/LX/LX1/project.html:541, :546-547, :491", "PASS",
    "Fresh. Exemplar A names three limits (:541); only limit one has a test (the interest-rate series, which the file lacks); limits two and three name none. Official C5 = 3 is consistent with C5 L3 ('names two limits, one with the test') and the miss at :547.")
row("proj-round11-delta-project-page", "2.9-prose", "course/modules/LX/LX1/project.html:62, :480, :541", "PASS",
    "Fresh re-check of the earlier edits: the windows definition at :62 is consistent with Lab 3 and Lesson 4; the C2 level-2 cell now contains the holding-step alternative; exemplar A's limit list (:541) is consistent with its C5 annotation.")
row("proj-spec-limits-test-each", "2.6-spec", "course/modules/LX/LX1/project.html:269, :449, :483-485, :491, :547", "PASS",
    "Fresh. Required outputs (:269) ask for two limits and the test that would settle at least one; brief item 5 (:449) says the same; C5 cells (:483-485) agree; exemplar A and its annotation (:547) apply the same test.")
row("proj-notation-n-undefined", "2.9-prose", "course/modules/LX/LX1/project.html:60, :438; tests/labs/LX1/lab-LX1-project-3.py", "PASS",
    "Fresh. 'n' appears as 'denominator n - 1' for the sample standard deviation of a window's changes (:60). It is the count of changes in that window (the sentence defines the dispersion of the window's changes), so n carries no registered meaning. Note only: a one-line definition of n at :60 would remove the reader's inference.")
row("proj-lab3-raise-claims-untested", "2.5-labs", "course/modules/LX/LX1/project.html:60 and :309 (claims 'the lab raises' at 1e-9), :386-387 (page code), tests/labs/LX1/lab-LX1-project-3.py:99-100", "FAIL",
    "Round 13 recorded this as PASS because the disagreement branch is not triggerable by the snapshot. That reasoning does not clear it under the ruling that a surviving lab mutant is a finding when a lesson sentence claims the lab checks the property. Both :60 ('the lab raises an error if the two differ by more than 1e-9 percent per month') and :309 ('or the lab raises') make that claim. The mutant r13n03_lab3_agreement_check_removed.py (check at twin lines 99-100 removed) exits 0 with stdout equal to the expected block (kill_check_all_mutants_existing.out: SURVIVED). No test in tests/ or in the kill harness exercises the raise, so the claim is untested.",
    "Add a test under tests/ (for example in tests/test_labs.py) that runs the lab-LX1-project-3 twin under python -I -W error with statistics.stdev replaced by a stub 1e-6 percent away from the two-pass value, and asserts ValueError 'the two-pass and statistics.stdev standard deviations disagree'; or delete the 'raises' claim at :60 and :309 if the check is to stay unexercised.")
row("proj-spec-window-start-must", "2.9-prose", "course/modules/LX/LX1/project.html:438 (window two start); tests/labs/LX1/lab-LX1-project-3.py (WINDOW_TWO_FROM)", "PASS",
    "Fresh. The sentence 'The lab computes no other start for window two, so the window start is a candidate limit' is true: the twin defines a single window-two start, WINDOW_TWO_FROM = '2000-01' (twin line 44), and no other start is computed. The window-start limit is named as a candidate, not as a finding.")
row("proj-rubric-c2-gap", "2.6-rubric", "course/modules/LX/LX1/project.html:480 (C2 row, level-2 cell and level-3/4 cells)", "PASS",
    "Fresh. Round-13 gap closed: the C2 level-2 cell now includes 'or gives a chain of at least three steps for each and names a failure step, but names no step at which the analogy holds'. Level 3 and 4 require the holding steps, so the alternatives are exclusive. Lower-floor cases (no chain and no similarity) are recorded under proj-rubric-exhaustive-r14, not counted, as in round 13.")
row("proj-rubric-c3-level3-gap", "2.6-rubric", "course/modules/LX/LX1/project.html:481 (C3 level 3 cell)", "PASS",
    "Fresh. The level-3 cell reads 'every claim graded B or C names its counter-evidence, or the essay states that it makes no such claim', so it is satisfiable without a B or C claim.")
row("proj-dag-concepts", "2.9-prose", "course/modules/LX/LX1/project.html:170 (one data-concept link); course/modules/LX/LX1/L02.html:110", "PASS",
    "Fresh. check_dag LX1 PASS (check_dag.out). The page's only concept link is debt-deflation (project.html:170), defined in L02.html:110 (dfn id def-debt-deflation, the L02 section 3 definition); L02 is a prerequisite lesson of the same unit.")
row("proj-exemplar-A-limit1-cip-locator", "2.6-rubric", "course/modules/LX/LX1/project.html:541; course/modules/LX/LX1/L04.html:329-333", "PASS",
    "Fresh. The item 'Exchange rates only' is at L04.html:333 under Section 4 'Where the canon breaks' (:329). It says the file has no interest-rate column and that the lab cannot test any relation between interest rates and exchange rates, as exemplar A states.")
row("proj-rubric-c3-inference-gap", "2.6-rubric", "course/modules/LX/LX1/project.html:481 (C3 level 3 and level 4)", "PASS",
    "Fresh. Round-13 gap closed: the C3 level-3 cell now reads 'Every claim is cited or marked as the writer's own inference, with at most two without a locator'. An inference-marked claim now satisfies levels 3 and 4 alike.")
row("proj-l04-model-name-stale", "2.9-prose", "course/modules/LX/LX1/project.html:438; course/modules/LX/LX1/L04.html:84-85", "PASS",
    "Fresh. Round-13 FAIL closed: 'parity' no longer appears on the project page (grep count 0). Line 438 names Lesson 4's Definition 2.1 as the fixed-exchange-rate model, and L04.html:84-85 uses that name.")
row("proj-exemplar-a-c2-annotation", "2.3-grades", "course/modules/LX/LX1/project.html:508 (episode step 3), :512 (annotation), :519 (condition step 3), :523 (annotation); definition at :64", "FAIL",
    "The round-13 defect is not fully closed. The definition at :64 holds an analogy at a step 'when the claim made at that step is true of both'. The new text at :508 and :519 names each chain's own step-3 claim (the real value is multiplied by P_{t-1}/P_t; the dispersion is the sample sd of the 12 changes), but the sentence that declares the step a holding step rests on a shared meta-claim, 'is an exact computation from the step before'. The episode's claim is not true of the condition (no real value), so the holding judgement is not 'the claim made at that step is true of both' as :64 defines it. The condition chain now sits under the measurement-chain clause at :64 (fixed), so that part is closed.",
    "At :508 and :519, name one claim that is literally true of both chains at step 3 (for example, 'the value at step 3 is an exact function of the step-2 quantity, with no estimate in between', if that is true of each chain as written), and make the holding sentence rest on that claim; or reword :64 to define a holding step by a shared property and say so there.")
row("proj-r14-delta-hunks", "2.9-prose", "git diff e919577b..8e5751c9 -- course/modules/LX/LX1/project.html (8 hunks): :37, :63-66, :267, :280, :438, :480-481, :508, :519", "PASS",
    "Read every hunk of the delta in full, against the current text. The delta changed only prose and two rubric cells, plus the exemplar A step-3 passages. The C2 cell (:480) and C3 cell (:481) were re-checked for exhaustiveness and exclusivity; the other hunks were checked against L02, L04, the MANIFEST, and Lab 3. Project labs, data, MANIFEST and references are byte-identical since the previous pin, except for L04.html:119-122 and the tests/labs/LX1/lab-LX1-L04-1.py docstring (not in this slice's rows; the L04 numbers were cross-checked).")
row("proj-rubric-exhaustive-r14", "2.6-rubric", "course/modules/LX/LX1/project.html:475-485 (all five criteria)", "PASS",
    "Exhaustiveness checked per criterion under the convention of rounds 11-13 ('names one limit' and 'one of them' read as at-least-one; 'except one' as at-most-one). Not counted, as in round 13 (rubric notes), but recorded: (a) C3 has no level for an essay that lists no source and leaves three or more factual claims uncited; (b) C5 has no level for an essay that names no caveat at all; (c) C4 level 4 is met vacuously by an essay that computes no number. The brief's 'every computed number' and required outputs make (c) unlikely, and (a) and (b) fail the required outputs at :269 and the brief.")


prev = json.load(open("/Users/billyribeiro/.fanout/frags/E-LX1-c.round13.json", encoding="utf-8"))
prev_ids = [r["id"] for r in prev["rows"]]
now_ids = [r["id"] for r in R]
missing = [i for i in prev_ids if i not in now_ids]
assert not missing, f"round-13 ids not kept: {missing}"
assert len(set(now_ids)) == len(now_ids), "duplicate ids"
counts = {s: sum(1 for r in R if r["status"] == s) for s in ("PASS", "FAIL", "UNVERIFIABLE")}
mutants = json.load(open(root / "ledgers/LX1/scripts/LX1-c-r14/out/mutants_r14.json", encoding="utf-8"))
killed = sum(1 for m in mutants if m["killed_by"])
verdict = "PASS" if counts["PASS"] == len(R) and killed == len(mutants) else "FAIL"
frag = {
    "unit": "LX1",
    "slice": "LX1-c",
    "round": 14,
    "verifier": "Claude Haiku 5.5 (claude-haiku-5-5), independent verifier for LX1-c, round 14 (did not build LX1)",
    "pin": "8e5751c903f0246115eba746afdf5d71f612bb37",
    "base": "e919577b45b431ce68e1e6533b00b8a301277937 (round-13 pin, per E-LX1-c.round13.json). Delta in slice: project.html only (8 hunks, listed in proj-r14-delta-hunks); L04.html:119-122 and the L04 twin docstring (cross-checked); project labs 1-3, data, MANIFEST, references and curriculum byte-identical.",
    "checkout": str(root),
    "scratch": "/tmp/lx1c_r14_rebuild (live rebuild, removed after the recorded run); ledgers/LX1/scripts/LX1-c-r14/out (all command outputs)",
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "verdict": verdict,
    "rows": R,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Blind calibration (proj-calibration-exemplars) is UNVERIFIABLE: this verifier printed the official scores and annotations before the blind scoring. The blind scores from essay text only are A 4,4,4,4,3 and B 2,2,1,2,1, matching the official scoring. A clean-room re-run needs the page to hold the official scoring out of its static HTML (rubric.js hides it only at runtime); blind_exemplars_r14.txt is ready for that run.",
        "Round-13 rows re-verified this round with fresh evidence: proj-lab3-interpretation-claims, proj-rubric-c2-gap, proj-rubric-c3-inference-gap, proj-l04-model-name-stale (all PASS now). proj-exemplar-a-c2-annotation stays FAIL (see row). Carried rows: proj-spec-curriculum-scope and proj-atlas-autograder-na only, both with byte-identical curriculum inputs.",
        "Mutants: 65 listed (62 existing re-run, 3 new r14n01-r14n03). 64 killed. The one survivor, r13n03_lab3_agreement_check_removed.py, is the subject of proj-lab3-raise-claims-untested. Round 13 called it advisory; this round applies the ruling that a surviving lab mutant is a finding where a lesson sentence claims the property (project.html:60, :309).",
        "Alternatives: three new correct implementations (alt1 Welford, alt2 float arithmetic, alt3 Decimal quantize) all match the expected blocks. The four round-13 alternatives were not re-run this round.",
        "Rubric lower-floor cases (an essay with no source; an essay with no caveat; an essay with no computed number, which meets C4 level 4 vacuously) match no descriptor or meet level 4 vacuously. Recorded under proj-rubric-exhaustive-r14, not counted, following rounds 12-13. A future round may decide these rows.",
        "Exemplar B states the monthly volatility as 2.47 percent per year. That is the designed failure of B (its verdict says the unit is wrong); no criterion depends on units. Not a finding.",
        "Lab 3 hypothesis (:287) and its printed 'True' line: the 'True' is printed only after the check passes, so the check's existence is what the raise claim depends on; see proj-lab3-raise-claims-untested.",
        "Not checked: an online verify_refs run of the whole registry (CI job scope, not this unit); the four round-13 alternatives; cards (outside this slice); the rubric descriptors under a student who writes an essay with no sources (see the lower-floor note); the exemplar pair under a real rater (only this verifier's reading).",
    ],
    "summary": (
        f"LX1-c round 14: verdict {verdict}. {len(R)} rows: {counts['PASS']} PASS, {counts['FAIL']} FAIL, "
        f"{counts['UNVERIFIABLE']} UNVERIFIABLE. Non-PASS: proj-calibration-exemplars (UNVERIFIABLE, blind condition not met in this session), "
        "proj-lab3-raise-claims-untested (FAIL, surviving mutant r13n03 with a page sentence claiming the raise), "
        "proj-exemplar-a-c2-annotation (FAIL, holding step rests on a meta-claim, not the claim made at the step as :64 defines). "
        "Round-13 FAILs proj-rubric-c2-gap, proj-rubric-c3-inference-gap, proj-l04-model-name-stale and proj-lab3-interpretation-claims are closed. "
        "Labs 1-3 pass run_labs (7/7) and pytest; page_smoke, check_pages, check_dag, check_projects, ruff, mypy, verify_refs (offline and LX1 online), fetch_data, build_site pass; a live rebuild of fx_monthly is byte-identical. "
        f"Mutants: {killed}/{len(mutants)} killed (3 new, all killed; 1 survivor). Alternatives: 3/3 match."
    ),
}
out = root / "ledgers/LX1/LX1-c.json"
out.write_text(json.dumps(frag, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out, "rows", len(R), counts, "mutants", killed, "/", len(mutants), "verdict", verdict)
