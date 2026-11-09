"""Round-15 verifier: writes the LX1-c fragment (ledgers/LX1/LX1-c.json) from the outputs in out/.

Usage: python -I write_fragment_r15.py <checkout_root>. Mutant killed_by values are read from the harness outputs."""
import json
import pathlib
import re
import sys

root = pathlib.Path(sys.argv[1]).resolve()
S = "ledgers/LX1/scripts/LX1-c-r15/out/"
out = root / S
M = root / "ledgers/LX1/mutants"

# ---- mutants -------------------------------------------------------------
def outcomes(path):
    res = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        m = re.match(r"(KILLED|SURVIVED) \| ([^|]+?) \|", line)
        if m:
            res[m.group(2).strip()] = m.group(1)
    return res

intact = outcomes(out / "kill_existing_r15.out")
new = outcomes(out / "kill_new_r15.out")
damaged_names = {"lx1c_m10_lab3_blank_cell_skipped.py", "lx1c_r8n03_lab3_blank_cell_skipped_silently.py",
                 "lx1c_r8n04_lab3_month_gap_not_checked.py", "lx1c_r9n03_lab3_gap_allows_one_missing_month.py"}
prev = json.loads(pathlib.Path("/Users/billyribeiro/.fanout/frags/E-LX1-c.round14.json").read_text(encoding="utf-8"))
prev_desc = {m["id"]: m["description"] for m in prev.get("mutants", [])}
mutants = []
for p in sorted(M.glob("*.py")):
    name = p.name
    text = p.read_text(encoding="utf-8")
    m = re.search(r"Student[^\n]*", text)
    desc = (m.group(0) if m else text.strip().splitlines()[0]).strip().strip('"')
    desc = re.sub(r"\s+", " ", desc)[:230]
    if name in damaged_names:
        killed = "damaged-snapshot differential (scripts/LX1-c-r15/damaged_r15.py; out/damaged_existing_r15.out)"
    elif name == "r13n03_lab3_agreement_check_removed.py":
        killed = ("script only, not a test in tests/: agreement_r15.py forces a disagreement; twin raises, mutant exits 0 "
                  "(out/agreement_r15.out). See row proj-lab3-raise-claims-untested")
    elif name.startswith("r15n"):
        assert new[name] == "KILLED", name
        killed = "harness.py intact-snapshot run (out/kill_new_r15.out): expected-block differs or rc!=0"
    else:
        assert intact[name] == "KILLED", name
        killed = "harness.py intact-snapshot run (out/kill_existing_r15.out): expected-block differs or rc!=0"
    overrides = {
        "r13n03_lab3_agreement_check_removed.py": "Student deletes the two-pass versus statistics.stdev agreement check, so a disagreement between the two standard deviations is never reported.",
        "r14n03_lab3_difference_printed_in_decimal.py": "Student takes the window-one-minus-window-two difference in decimal units without the factor 100, so the difference line prints 0.00 in place of 0.32 percent per month.",
    }
    if name in overrides:
        desc = overrides[name]
    elif "Student" not in desc and name in prev_desc:
        desc = prev_desc[name]
    mutants.append({"id": name, "description": desc, "killed_by": killed})

# ---- rows ----------------------------------------------------------------
def row(i, check, loc, status, ev, fix=None):
    r = {"id": i, "check": check, "location": loc, "status": status, "evidence": ev}
    if status != "PASS":
        r["fix"] = fix
    return r

R = []
R.append(row("proj-rung1-step3-rounding-claim", "2.5-labs",
  "course/modules/LX/LX1/project.html:177 (worked step 3 and step 5 text)", "PASS",
  "Fresh. out/rederive_r15.out: LAB1 real debt falling ends 117647.06 (exact 10000000/0.85 cents = 11764705.88 cents). out/twins.out: twin prints 'real debt=117647.06'. Step 5 difference: exact 30690.537... rounds to 30690.54, same as difference of printed values."))
R.append(row("proj-real-value-vs-lesson2", "2.9-prose",
  "course/modules/LX/LX1/project.html:56, :58; course/modules/LX/LX1/L02.html:83-92, :110, :127-128", "PASS",
  "Fresh (line 56 changed this round, read in full). L02.html:83 V_t = D P_0 / P_t; :84-92 Proposition 2.1 with (A2) and (A3), conclusion (a) V_t/V_{t-1} = P_{t-1}/P_t; :110 debt deflation definition; :127-128 Remark 3.3 (corollary gives no cause). Page :56 'the labs' A1 and A2 are their own' matches Lab 1 docstring (Assumptions A1, A2). L02.html unchanged since round-14 pin."))
R.append(row("proj-manifest-note-misattributed", "2.2-numbers",
  "course/modules/LX/LX1/project.html:271, :279, :293; course/assets/data/market/MANIFEST.json (fx_monthly)", "PASS",
  "Fresh. MANIFEST fx_monthly: title 'Month-end foreign exchange rates, ten currencies, USD per unit of foreign currency'; transform: 'each column's last value in the month'; CAD, CHF, DKK, JPY, NOK, SEK inverted; rows 669; first 1971-01; last 2026-09; retrieved 2026-10-19. Each statement on the page matches."))
R.append(row("proj-lab3-citation-string", "2.9-prose",
  "course/modules/LX/LX1/project.html:279, :287; MANIFEST.json fx_monthly citation", "PASS",
  "Fresh. MANIFEST citation string equals the citation in project.html:279 and in the Lab 3 hypothesis (:287) and docstring."))
R.append(row("proj-reading-reinhart-registry", "2.9-prose",
  "course/modules/LX/LX1/project.html:633-640; references/references.json", "PASS",
  "Fresh. Reading list (:635-640) holds friedman1963monetary, eichengreen1992golden, garber2000famous. Registry records read this round: each has used_by ['LX1'] and status 'verified'. references/ byte-identical to round-14 pin (git diff --stat 8e5751c9 d1e65a0 empty for references)."))
R.append(row("proj-spec-current-undefined", "2.9-prose",
  "course/modules/LX/LX1/project.html:446 (brief item 1), :62, :300-301", "PASS",
  "Fresh. Current condition defined as dated within the twelve months ending at the last month of the data (:446); for the snapshot, 2025-10 to 2026-09 (:62, :300-301; Lab 3 window three in out/rederive_r15.out: 12 changes)."))
R.append(row("proj-exemplar-A-condition", "2.6-rubric",
  "course/modules/LX/LX1/project.html:497, :519", "PASS",
  "Fresh. Exemplar A names window three, 2025-10 to 2026-09; MANIFEST last 2026-09, retrieved 2026-10-19 (MANIFEST.json fx_monthly). Window three in rederive_r15.out: 12 changes, 1.90 percent per month."))
R.append(row("proj-gate-commands", "2.9-prose",
  "ledgers/LX1/scripts/LX1-c-r15/out/", "PASS",
  "Fresh, all run on d1e65a0 with .venv (Python 3.14.8). check_pages LX1 PASS (check_pages.out); check_dag LX1 PASS (check_dag.out); check_projects LX1 PASS (check_projects.out); run_labs --unit LX1 PASS 7/7 (run_labs_LX1.out); run_labs --page project PASS 3/3 (run_labs_project.out); page_smoke --pages project PASS (page_smoke_project.out); ruff check and format --check tests/labs/LX1 PASS (ruff_check_labs.out, ruff_format_labs.out); mypy --no-incremental: no issues in 385 files (mypy_full.out); pytest test_labs/test_run_labs/test_page_smoke/test_page_checks/test_curriculum: rc 0 (pytest_relevant.out); verify_refs --offline: 560 entries 0 problems (verify_refs_offline.out); verify_refs --unit LX1 live: 4 of 560, 0 problems (verify_refs_unit_LX1_online.out); fetch_data --check: 3 datasets 0 problems (fetch_data_check.out); build_site --check: current (build_site_check.out); mutate_graders --unit LX1 and run_graders --unit LX1: no autograder (mutate_graders_LX1.out, run_graders_LX1.out)."))
R.append(row("proj-lab1-twin-run", "2.5-labs",
  "course/modules/LX/LX1/project.html:77-149; tests/labs/LX1/lab-LX1-project-1.py", "PASS",
  "Fresh. scripts/LX1-c-r15/harness.py twins (out/twins.out): page code equals twin line for line (0 differing lines); twin run as python -I -W error: rc 0, stderr 0 bytes, stdout equals the page expected block (20 lines). Runtime 0.0 s in page_smoke."))
R.append(row("proj-lab1-numbers", "2.2-numbers",
  "course/modules/LX/LX1/project.html:77, :150-171", "PASS",
  "Fresh. out/rederive_r15.out (Decimal, 60 digits, no lab code): falling real debt 100000.00, 103092.78, 106382.98, 109890.11, 113636.36, 117647.06; rising 100000.00, 97087.38, 94339.62, 91743.12, 89285.71, 86956.52; burden 17.65 and -13.04; difference 30690.54. Identical to the page expected block."))
R.append(row("proj-lab2-twin-run", "2.5-labs",
  "course/modules/LX/LX1/project.html:184-258; tests/labs/LX1/lab-LX1-project-2.py", "PASS",
  "Fresh. out/twins.out: page code differs from the twin only on the two '___' lines (the completion blanks); the twin runs under python -I -W error with rc 0, empty stderr, and stdout equal to the expected block (10 lines)."))
R.append(row("proj-lab2-numbers", "2.2-numbers",
  "course/modules/LX/LX1/project.html:184, :247-256", "PASS",
  "Fresh. out/rederive_r15.out: real debt 40000.00, 40404.04, 40816.33, 41666.67, 42105.26, 43010.75; burden exact 7.526882, rounds to 7.53."))
R.append(row("proj-lab2-check-claims", "2.5-labs",
  "course/modules/LX/LX1/project.html:257", "PASS",
  "Fresh. Claim 'leaves out the division prints 40000.00 in every period': 4000000 cents / 1 = 40000.00 at each t (mutant lx1c_m01 killed by the expected-block comparison, out/kill_existing_r15.out). Claim 'inverts the ratio prints -7.00': out/rederive_r15.out 'LAB2 burden ratio inverted %: -7.00'; mutant lx1c_m02 killed (out/kill_existing_r15.out)."))
R.append(row("proj-lab3-twin-run", "2.5-labs",
  "course/modules/LX/LX1/project.html:287-437; tests/labs/LX1/lab-LX1-project-3.py", "PASS",
  "Fresh. out/twins.out: twin run under python -I -W error in a scratch directory holding data/fx_monthly.csv: rc 0, stderr 0 bytes, stdout equals the expected block (20 lines); page code equals the twin line for line."))
R.append(row("proj-lab3-numbers", "2.2-numbers",
  "course/modules/LX/LX1/project.html:287, :411-437", "PASS",
  "Fresh. out/rederive_r15.out (independent Decimal code): changes 668 / 321 / 12; exact zeros 3 / 2 / 0; sd percent per month 2.79352779 / 2.46995014 / 1.90201858, printed 2.79 / 2.47 / 1.90; ratio w2/w1 unrounded 0.884168808 -> 0.88; difference w1-w2 0.323577653 -> 0.32; largest by size: 13.58 (1985-03) in window one, -9.66 (2008-10) in window two, 2.96 (2026-04) in window three. All equal the expected block."))
R.append(row("proj-lab3-L04-cross-check", "2.9-prose",
  "course/modules/LX/LX1/L04.html:312-318; course/modules/LX/LX1/project.html:284", "PASS",
  "Fresh. L04.html expected block prints changes 668 and 321, sd 0.027935 and 0.024700, largest 0.135846 at 1985-03; out/rederive_r15.out cross-check gives 0.027935 and 0.024700 (6 dp). L04.html changed only at :334 (monthly-sampling bullet), outside the cited lines."))
R.append(row("proj-lab3-docstring-claims", "2.9-prose",
  "course/modules/LX/LX1/project.html:288-315 (twin docstring mirrored); tests/labs/LX1/lab-LX1-project-3.py load_column, month_index", "PASS",
  "Fresh. out/damaged_existing_r15.out and out/twins.out: twin raises ValueError on a blank, 'n/a', '1.2e0' and '-1.2' GBP cell, on a dropped month (2000-07 does not follow 2000-05), and on a duplicated month; no row is skipped or filled. The statement about the agreement raise is the separate FAIL row proj-lab3-raise-claims-untested."))
R.append(row("proj-lab3-interpretation-claims", "2.5-labs",
  "course/modules/LX/LX1/project.html:438; course/modules/LX/LX1/L04.html:84-94 (Definition 2.1, (A2); Proposition 2.2(a))", "PASS",
  "Fresh. L04.html:84-86 Definition 2.1 fixed-exchange-rate model with (A2) fixed rate held over the window; L04.html:88-94 Proposition 2.2 (a) every monthly log change zero under (A2). Page :438 conditional on (A2): 321 zero changes if held, window two shows 2 (out/rederive_r15.out). Hypothesis and interpretation are conditional as stated."))
R.append(row("proj-lab3-difference-line-r5", "2.2-numbers",
  "course/modules/LX/LX1/project.html:287, :411, :436, :438; tests/labs/LX1/lab-LX1-project-3.py (main, difference line)", "PASS",
  "Fresh. Twin main(): difference = show(100 * (sd_one - sd_two), 2) from unrounded sds. out/rederive_r15.out: unrounded 0.323577653 -> 0.32 (printed 0.32)."))
R.append(row("proj-lab-simulated-labels", "2.8-data",
  "course/modules/LX/LX1/project.html:42, :77, :80, :184, :187 (code docstrings), :283-287 (Lab 3 hypothesis and section)", "PASS",
  "Fresh. Labs 1 and 2 carry SIMULATED in hypothesis lines (:77, :184) and code docstrings. Lab 3 (:283-287) carries no SIMULATED label and names its dataset, source, and retrieval date (MANIFEST); its licence is quoted in the same section (:279)."))
R.append(row("proj-data-licence-quote", "2.8-data",
  "course/modules/LX/LX1/project.html:279; https://www.federalreserve.gov/disclaimer.htm (plain curl)", "PASS",
  "Fresh. curl -sS -L https://www.federalreserve.gov/disclaimer.htm: HTTP 200 (out/curl_licence_r15.out; saved as out/licence_page_r15.html). Page contains: 'Unless otherwise indicated, information on Board's website is in the public domain and may be copied and distributed without permission. Please cite to the Board as the source of the information.' Grants redistribution. Quote matches MANIFEST licence field."))
R.append(row("proj-data-snapshot-rebuild", "2.8-data",
  "course/assets/data/market/fx_monthly.csv; course/assets/data/market/MANIFEST.json (fx_monthly)", "PASS",
  "Fresh live rebuild in a scratch copy of git archive d1e65a0: tools/fetch_data.py --fetch --only fx_monthly (out/rebuild_fx_monthly_r15.out): built 669 rows, 67392 bytes, 1971-01 to 2026-09. Rebuilt file sha256 60572240d1a9d1832d5021297634b2369723b94098414948b891dd26a8bffe3e equals MANIFEST sha256 and cmp reports byte-identical to the committed CSV. raw_sha256 not compared (provenance only, BUILDER_RULES 6.6)."))
R.append(row("proj-data-fields", "2.8-data",
  "course/modules/LX/LX1/project.html:271, :279-280, :293; course/assets/data/market/fx_monthly.csv", "PASS",
  "Fresh (scripts/LX1-c-r15/data_checks_r15.py, out/data_checks_r15.out). CSV header: month, AUD, CAD, CHF, DKK, EUR, GBP, JPY, NOK, NZD, SEK (no interest-rate column; the script finds no rate or yield column). EUR blank in 336 rows, 1971-01 to 1998-12; first non-blank 1999-01. GBP blank cells 0. 669 months 1971-01 to 2026-09, contiguous."))
R.append(row("proj-data-no-other-series", "2.8-data",
  "course/modules/LX/LX1/project.html:280 (list sentence); tools/data_sources.yaml ids (lines 19, 53, 91)", "PASS",
  "Fresh. The list sentence is accurate: the three embedded series are fx_daily, fx_monthly and ust_daily (data_sources.yaml ids; MANIFEST datasets). None is a gold, price-level, output, unemployment or bank-failure series. The universal sentence 'No historical series for your episode is embedded' in the same paragraph is a separate FAIL row (proj-data-embedded-claim)."))
R.append(row("proj-spec-ladder", "2.6-spec",
  "course/modules/LX/LX1/project.html:40-48, :72-258, :261-275, :277-441, :443-453, :471-631", "PASS",
  "Fresh. Ladder order: rung 1 (Lab 1, worked, annotated steps), rung 2 (Lab 2, class 'lab completion', two blanks), rung 3 (spec, data, Lab 3 check, brief, rubric), rung 4 (stretch, :625-631). check_projects LX1 PASS (check_projects.out)."))
R.append(row("proj-spec-curriculum-scope", "2.6-spec",
  "curriculum/06-profession-capstone.yaml:42-49; course/modules/LX/LX1/project.html:443-453", "PASS",
  "Fresh. Curriculum: title 'Then vs. now'; brief 'Pick one historical episode and one current market condition, and write a mechanism-level comparison that says where the analogy holds and where it breaks'; deliverable 'Two-page essay, every claim cited.'; grading rubric. Page brief (:443-453) and spec (:265-275) cover each element; the page adds the evidence-grade, counter-evidence and rounding constraints of the same brief."))
R.append(row("proj-hours", "2.6-hours",
  "course/modules/LX/LX1/project.html:33 (eyebrow), :457-467 (table#hours); course/modules/LX/LX1/index.html:29", "PASS",
  "Fresh. Table rows 1 + 1 + 2 + 1.5 + 2.5 + 2 = 10 = data-hours-project (index.html:29) and eyebrow '10 hours'. Verifier estimate: Lab 1 read and annotate about 1 h; Lab 2 two blanks and check about 0.75 h; selecting two episodes and finding a locator for each dated claim about 3 h (reading two sources); mechanism outlines about 1.5 h; two-page drafting with citations and rules about 2.5 to 3 h; self-assessment with exemplars about 1.5 to 2 h. Total about 10.5 to 11.5 h, inside 30 percent of 10."))
R.append(row("proj-rubric-observable", "2.6-rubric",
  "course/modules/LX/LX1/project.html:479-483 (rubric rows)", "PASS",
  "Fresh. Every level cell names a checkable element: dates and locators (C1), steps and the failure step (C2), citations, uncited count and counter-evidence statement (C3), rounding rule and formula or lab line (C4), limits and their tests (C5). No vague descriptor found. Presence-versus-correctness gaps are in row proj-student-error-coverage."))
R.append(row("proj-calibration-exemplars", "2.6-rubric",
  "course/modules/LX/LX1/project.html:491-616 (exemplar memo prose; verdict lines :493 and :555); ledgers/LX1/scripts/LX1-c-r15/blind_extract_r15.py; out/blind_prose_r15.txt", "UNVERIFIABLE",
  "Prose-only extraction (ruling 15: annotations, verdict lines and data-score attributes dropped) produced out/blind_prose_r15.txt. Scored from prose and rubric descriptors only: Exemplar A C1 4, C2 4, C3 4, C4 4, C5 3 (official 4,4,4,4,3); Exemplar B C1 2, C2 2, C3 1, C4 2, C5 1 (official 2,2,1,2,1). All within one level. BUT the blind condition is not met in this session: this verifier read the verdict lines (:493, :555) and the annotations (:501-:616) with sed before the extraction, so the scores cannot count as blind. The page's static HTML also carries the official scores and annotations, which ruling 15 keeps for learners."))
R.append(row("proj-exemplar-numbers", "2.2-numbers",
  "course/modules/LX/LX1/project.html:530 (A numbers), :584 (B numbers), :588", "PASS",
  "Fresh. Exemplar A: 17.65 (Lab 1 Part B), 2.47, 2.79, 1.90 (Lab 3), ratio 0.88 from unrounded 0.884169 (not 2.47/2.79 = 0.8853), 13.58 at 1985-03, difference 0.32 (out/rederive_r15.out). Exemplar B: 2.47/2.79 = 0.8853 -> 0.89 and fall of 11.47 percent 'about 11 percent': both match the B annotation (rounded inputs)."))
R.append(row("proj-reading-keys", "2.9-prose",
  "course/modules/LX/LX1/project.html:635-640; references/references.json", "PASS",
  "Fresh. data-cite keys friedman1963monetary, eichengreen1992golden, garber2000famous exist in references.json with used_by ['LX1']. Eichengreen title 'Golden fetters: the gold standard and the Great Depression, 1919-1939' matches the exemplar's period claim."))
R.append(row("proj-notation", "2.9-prose",
  "course/modules/LX/LX1/project.html (30 inline TeX spans); notation/notation.json", "PASS",
  "Fresh. notation.json has 8 registered entries (T, Phi and Phi^-1, gamma_3, gamma_4, R^*, R^{e*}, R_f, Q). The page's spans use D, P_t, P_0, V_t, S_m, t, m, n, ln; none is registered, so no collision. V_t and P_t match Lesson 2 and the plan's notation rule."))
R.append(row("proj-scope-words", "2.9-prose",
  "course/modules/LX/LX1/project.html:62, :68, :177, :265-271, :284, :299, :438, :473, :493, :519, :541, :547; scripts/LX1-c-r15/page_checks_r15.py (out/page_checks_r15.out)", "PASS",
  "Fresh scan. 'every monthly change' (:62) = 668 changes (rederive); 'the only lab that reads a file' (:284) = labs 1 and 2 have no open(); 'the same two windows and change counts' = L04 expected block; 'every run prints the same lines' (Lab 1, no RNG); 'all 12 changes' (:438) = window three; 'rules out ... over all of window three' follows from (A2) and 0 zero changes in 12 (:541/:519 chain). The universal 'No historical series ... is embedded' (:280) is the separate FAIL row proj-data-embedded-claim."))
R.append(row("proj-process-words", "2.9-prose",
  "course/modules/LX/LX1/project.html (rendered prose); scripts/LX1-c-r15/page_checks_r15.py (out/page_checks_r15.out)", "PASS",
  "Fresh scan (page_checks_r15.py) of rendered prose for build, builder, verif*, agent, REQUESTS, unit report, fixer, Claude: zero hits. 'round' occurs only as rounding ('Round once, at print time', 'rounded half up'), a learner operation, not a process word."))
R.append(row("proj-links-anchors", "2.9-prose",
  "course/modules/LX/LX1/project.html (all href and id); scripts/LX1-c-r15/page_checks_r15.py (out/page_checks_r15.out)", "PASS",
  "Fresh (page_checks_r15.py). In-page hash hrefs (brief, data, main, rubric-section, self-assessment, spec, stretch) all resolve to ids (missing = []). check_pages LX1 PASS covers the cross-page links (check_pages.out)."))
R.append(row("proj-page-smoke", "2.9-prose",
  "course/modules/LX/LX1/project.html; out/page_smoke_project.out", "PASS",
  "Fresh. page_smoke --unit LX1 --pages project: PASS; 3 labs run; boot 1.2 s; each lab 0.0 s (under 10 s)."))
R.append(row("proj-atlas-autograder-na", "2.6-spec",
  "curriculum/06-profession-capstone.yaml:19-49 (grading: rubric); course/modules/LX/LX1/ (no grader/ directory)", "PASS",
  "Fresh. The LX1 entry has no atlas key (grep for atlas/contract in curriculum/06-profession-capstone.yaml: no match); no grader directory; run_graders --unit LX1 prints 'no autograder (grading: rubric)' (run_graders_LX1.out). Rubric-only, consistent with the plan's section 11."))
R.append(row("proj-mutants-student-errors", "2.6-mutation",
  "ledgers/LX1/mutants/ (r15n01-r15n03 new; 65 existing); ledgers/LX1/scripts/LX1-c-r15/make_mutants_r15.py", "PASS",
  "Three new student-error lab mutants written this round, each a complete variant of its twin: r15n01_lab1_burden_percent_of_end_real_value (burden base is the period-5 real value), r15n02_lab3_window_three_year_on_year_changes (twelve-month changes in window three), r15n03_lab3_two_pass_sd_scaled_by_sqrt_n_minus_one_over_n (wrong scaling). All three are killed by the expected-block comparison (out/kill_new_r15.out). Of the 65 existing, 60 are killed by the intact-snapshot run, 4 by the damaged-snapshot differential, and r13n03 by a forced-disagreement script only (no test in tests/); r13n03 is recorded under proj-lab3-raise-claims-untested."))
R.append(row("proj-alternatives", "2.6-mutation",
  "ledgers/LX1/scripts/LX1-c-r15/alts/ (alt_r15_A, alt_r15_B, alt_r15_C); out/alts_r15.out", "PASS",
  "Three new alternative correct implementations, each run under python -I -W error against the expected block: A lab 1 in Decimal at 60 digits; B lab 2 in Decimal; C lab 3 with log changes as differences of logs, dispersion by statistics.variance, and the page's agreement check. All three match the expected blocks exactly (out/alts_r15.out). The round-14 alternatives were not re-run."))
R.append(row("proj-exemplar-b-annotations-vs-descriptors", "2.6-rubric",
  "course/modules/LX/LX1/project.html:553-616 (exemplar B passages and annotations)", "PASS",
  "Fresh read. Each B annotation checked against the B prose (out/blind_prose_r15.txt) and the rubric cells at :479-483: C1 L2 (condition has no date), C3 L1 (sources listed, H.10 without locator), C4 L2 (rounded inputs; no rule), C2 L2 (similarities and one difference, no chain), C3 misses (at least three uncited claims), C5 L1 (caveat only). Official 2,2,1,2,1 agree with the descriptors."))
R.append(row("proj-brief-rubric-escape-clauses", "2.6-rubric",
  "course/modules/LX/LX1/project.html:449 (brief item 4), :265 (context), :481 (C3 L4 and L3)", "PASS",
  "Fresh. Brief item 4, C3 L4 and C3 L3 carry the same counter-evidence clause with the 'the essay states that it makes no such claim' alternative. Consistent with the spec."))
R.append(row("proj-exemplar-locators", "2.6-rubric",
  "course/modules/LX/LX1/project.html:497, :508, :519, :530, :541; course/modules/LX/LX1/L02.html:87-92, :127-128; course/modules/LX/LX1/L04.html:329-333", "PASS",
  "Fresh. Each exemplar locator resolves: L02 Proposition 2.1(a) (:87-92), Remark 3.3 (:127-128), L04 Section 4 'Exchange rates only' (:329-333), MANIFEST fields, Lab 3 lines."))
R.append(row("proj-exemplar-a-c5-limit-count", "2.6-rubric",
  "course/modules/LX/LX1/project.html:541, :546-547, :491", "PASS",
  "Fresh. Exemplar A names three limits (:541); only limit one has a test (interest-rate series, which the file lacks); limits two and three name none (:546-547). Official C5 = 3 consistent with 'names two limits, one with the test'."))
R.append(row("proj-round11-delta-project-page", "2.9-prose",
  "course/modules/LX/LX1/project.html:62, :480, :541", "PASS",
  "Fresh. Window definitions at :62 agree with Lab 3 and Lesson 4; C2 level-2 cell (:480) and exemplar A limit text (:541) agree with the lab output."))
R.append(row("proj-spec-limits-test-each", "2.6-spec",
  "course/modules/LX/LX1/project.html:269, :449, :483, :491, :547", "PASS",
  "Fresh. Required outputs (:269) ask for two limits and the test that would settle at least one; brief item 5 (:449) says the same; C5 cells (:483) agree; exemplar A (:541, :547) consistent."))
R.append(row("proj-notation-n-undefined", "2.9-prose",
  "course/modules/LX/LX1/project.html:60, :438; tests/labs/LX1/lab-LX1-project-3.py", "PASS",
  "Fresh. 'n' in 'denominator n - 1' (:60) is the number of changes in the window, as the Lab 3 code sets n = len(values) and :438 says 12 changes with 11 degrees of freedom. The page does not define n in words at :60; treated as the standard sample-size symbol, not a defect."))
R.append(row("proj-lab3-raise-claims-untested", "2.5-labs",
  "course/modules/LX/LX1/project.html:60 and :309 (claims 'the lab raises' at 1e-9 percent); project.html:386-387 (page code); tests/labs/LX1/lab-LX1-project-3.py:99-100 (check and raise)", "FAIL",
  "Still untested. Forced disagreement (scripts/LX1-c-r15/agreement_r15.py, out/agreement_r15.out): the twin, with statistics.stdev 1e-6 away, exits 1 with 'ValueError: the two-pass and statistics.stdev standard deviations disagree'; mutant r13n03_lab3_agreement_check_removed.py exits 0 with 20 lines of stdout (the expected block). grep of tests/ finds no test of this raise (only the lab code itself). Under the ruling, a surviving lab mutant is a finding where a lesson sentence claims the lab checks the property, and :60 and :309 make that claim. Round 14's FAIL is unchanged; the text at :60 and :309 is unchanged in the round-15 delta."
  , "Either (a) add a test under tests/ (for example in tests/test_labs.py) that runs the lab-LX1-project-3 twin under python -I -W error with statistics.stdev replaced by a stub 1e-6 away from the two-pass value and asserts ValueError 'the two-pass and statistics.stdev standard deviations disagree'; or (b) delete 'the lab raises' from :60 and :309."))
R.append(row("proj-spec-window-start-must", "2.9-prose",
  "course/modules/LX/LX1/project.html:438 (window two start); tests/labs/LX1/lab-LX1-project-3.py (WINDOW_TWO_FROM)", "PASS",
  "Fresh. Twin defines one window-two start (WINDOW_TWO_FROM = '2000-01'); the sentence 'The lab computes no other start for window two' is true; the window start is then a candidate limit (:438)."))
R.append(row("proj-rubric-c2-gap", "2.6-rubric",
  "course/modules/LX/LX1/project.html:480 (C2 row, level-2 cell and level-3/4 cells)", "PASS",
  "Fresh. The C2 level-2 cell lists the cases: similarities and one difference; a chain without a failure step; a chain under three steps; a chain with a failure step and no holding step. Each is observable."))
R.append(row("proj-rubric-c3-level3-gap", "2.6-rubric",
  "course/modules/LX/LX1/project.html:481 (C3 level 3 cell)", "PASS",
  "Fresh. The level-3 cell reads 'every claim graded B or C names its counter-evidence, or the essay states that it makes no such claim', satisfiable with no B or C claim."))
R.append(row("proj-dag-concepts", "2.9-prose",
  "course/modules/LX/LX1/project.html:170 (one data-concept link); course/modules/LX/LX1/L02.html:110 (def-debt-deflation)", "PASS",
  "Fresh. check_dag LX1 PASS (check_dag.out). The page's only concept link is debt-deflation (:170), defined in L02.html:110 inside the unit's prerequisite closure. Gold standard and fixed-exchange-rate model are plain prose or cited as Lesson 4 definitions."))
R.append(row("proj-exemplar-A-limit1-cip-locator", "2.6-rubric",
  "course/modules/LX/LX1/project.html:541; course/modules/LX/LX1/L04.html:329-333", "PASS",
  "Fresh. L04.html:329 Section 4 'Where the canon breaks'; :333 item 'Exchange rates only' states the snapshot has no interest-rate column and the lab cannot test such a relation."))
R.append(row("proj-rubric-c3-inference-gap", "2.6-rubric",
  "course/modules/LX/LX1/project.html:481 (C3 level 3 and level 4)", "PASS",
  "Fresh. C3 level 3 reads 'Every claim is cited or marked as the writer's own inference, with at most two without a locator'; level 4 requires a locator or inference marker for every claim. Consistent."))
R.append(row("proj-l04-model-name-stale", "2.9-prose",
  "course/modules/LX/LX1/project.html:438; course/modules/LX/LX1/L04.html:84-85", "PASS",
  "Fresh. grep 'parity' in project.html: 0 matches. Line 438 names Lesson 4's Definition 2.1 as the fixed-exchange-rate model, which L04.html:84-85 defines."))
R.append(row("proj-exemplar-a-c2-annotation", "2.3-grades",
  "course/modules/LX/LX1/project.html:508 (episode step 3), :519 (condition step 3); definition at :64", "PASS",
  "Closed this round. Round-14 fix option 1 is applied: the holding sentence now rests on one claim that is literally true of both chains at step 3, 'the claim each chain makes there is an exact function of its step-2 quantity, with no estimate in between'. Checked against each chain as written: episode step 3 (real value multiplied by P_{t-1}/P_t) is an exact function of the two price levels that step 2 describes; condition step 3 (dispersion = sample sd of the 12 changes) is an exact function of the 12 log changes of step 2. The definition at :64 is unchanged. Residual judgement: the step-3 claims differ in content and the holding is judged by the shared property, which round 14 named as an acceptable fix."))
R.append(row("proj-r14-delta-hunks", "2.9-prose",
  "git diff 8e5751c9 d1e65a0 -- course/modules/LX/LX1/project.html (3 hunks: :53-56, :505-508, :516-519)", "PASS",
  "Read every hunk in full against the current text. The round-15 delta changes only: Conventions 'Nominal debt and real value' wording (:56: labs' A1 and A2 named as Lab 1's assumptions, which the Lab 1 docstring confirms); exemplar A 'Mechanism, episode one' (:508) and 'Mechanism, condition' (:519) holding sentences (see proj-exemplar-a-c2-annotation). Labs 1-3 and the data are byte-identical to the round-14 pin; L04.html changed only at :334, outside the cited lines."))
R.append(row("proj-rubric-exhaustive-r14", "2.6-rubric",
  "course/modules/LX/LX1/project.html:473 (scoring sentence), :479-483 (C1-C5 rows)", "FAIL",
  "The descriptors are not exhaustive at the floor and one criterion is not exclusive. (1) C1: an essay naming only one event meets no level (L1 needs two events). (2) C2: an essay with no similarity and no chain (only differences) meets no level. (3) C3: an essay that lists no source and has three or more uncited factual claims meets no level (L1 needs a source; L2 allows at most two uncited). (4) C5: an essay with no caveat or limit meets no level. The scoring sentence (:473) assigns 'the highest level whose every element the essay shows', which has no answer for these essays. (5) C4: an essay that computes no number meets L4 vacuously ('each computed number ...') and L1 vacuously ('states no rounding rule for any computed number'), so C4 is not exclusive for it and the highest-level rule gives 4. (6) C4 L3 ('unrounded values and a rule for every number but one') admits one rounded input, which L2 names as a level-2 trait ('rounds an input before computing'); the two cells disagree about the same essay. Overlaps C1 L2/L3 and C4 L2/L3 are otherwise resolved by the highest-level rule."
  , "(a) Add to the scoring sentence at :473: 'A criterion that no level describes scores 0 (not yet met).' (b) C4 L4 (:482): begin 'At least one computed number, and each comes from unrounded values, ...'; C4 L1: 'States no rounding rule for any computed number, or computes none.' (c) C4 L3: 'unrounded values and a stated rule for every number but one, and that one does not round an input before computing.' Then re-run the exemplar scoring (exemplar B's C4 stays 2)."))
R.append(row("proj-student-error-coverage", "2.6-rubric",
  "course/modules/LX/LX1/project.html:479-483 (rubric cells); plans/LX1-build-plan.md section 5.4 (ten student-error patterns the rubric must catch)", "FAIL",
  "Checked each of the plan's ten student-error patterns against the descriptors. Caught: 5 (C2 L2 'names no failure step'), 6 (C4 L2 'rounds an input before computing'), 7 and 8 (C3 uncited claim lowers the level), 10 (C1 locator or date missing). Not caught: (1) real debt computed as nominal debt, no division by P: C4 L4 accepts any formula that is cited, and no descriptor checks the mechanism's arithmetic; (2) a percent change with no base or direction: C4 does not require the base or direction of a percent change; (4) a citation whose locator does not contain the claim: C3 L4 requires a locator to be present, not to contain the claim. Pattern 3 ('bubble' for any price rise) is caught only if the chain happens to be missing. Pattern 9 is a lab (instant check), outside the rubric."
  , "(a) C4 L4 (:482): add 'the formula is the one the cited line prints or derives, and every percent change names its base and sign'. (b) C3 L4 (:481): add 'each locator is a place where the claim is written, so a reader who opens it finds the claim'. (c) Mirror (a) and (b) in the C4 L3 and C3 L3 cells, or name in the scoring note that the rubric scores presence, and that the rater checks correctness."))
R.append(row("proj-data-embedded-claim", "2.8-data",
  "course/modules/LX/LX1/project.html:280 ('No historical series for your episode is embedded.'); course/assets/data/market/MANIFEST.json (fx_daily 2000-01 to 2026-09; fx_monthly 1971-01 to 2026-09; ust_daily 2000-01 to 2026-09, H.15 Treasury yields); scripts/LX1-c-r15/data_checks_r15.py (out/data_checks_r15.out)", "FAIL",
  "The universal sentence is contradicted by the site's own embedded data. MANIFEST lists three historical series: fx_daily (2000-01-03 to 2026-09-30, six currencies), fx_monthly (1971-01 to 2026-09) and ust_daily (2000-01-03 to 2026-09-30, 3-month bill and 10-year yield). For an episode about exchange rates or US interest rates, the sentence is false. The Data section never mentions ust_daily, and 'the snapshot set' is undefined. Lab 3 and the spec are unaffected."
  , "Replace the sentence at :280 with: 'The site embeds three series (fx_daily, fx_monthly, ust_daily; MANIFEST). This project reads fx_monthly. None of the three is a gold, price-level, output, unemployment or bank-failure series. A series for your episode that none of the three holds, you source yourself, with a locator, from a source you have read.' and define 'snapshot set' at its first use."))

# ---- fragment ------------------------------------------------------------
statuses = [r["status"] for r in R]
counts = {s: statuses.count(s) for s in ("PASS", "FAIL", "UNVERIFIABLE")}
frag = {
    "unit": "LX1",
    "slice": "LX1-c",
    "round": 15,
    "verifier": "Claude Haiku 5.5 (claude-haiku-5-5), independent verifier for LX1-c, round 15 (did not build LX1)",
    "pin": "d1e65a0203e386e3246429ba1cf7e723eb6cfbfa",
    "base": "8e5751c903f0246115eba746afdf5d71f612bb37 (round-14 pin, per E-LX1-c.round14.json)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE15-LX1-c",
    "scratch": "ledgers/LX1/scripts/LX1-c-r15/ (scripts) and ledgers/LX1/scripts/LX1-c-r15/out/ (every command output); a /tmp copy of the repository for the live fx_monthly rebuild was removed after its recorded run",
    "verified_at": "2026-11-09T01:40:00+00:00",
    "verdict": "FAIL",
    "rows": R,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Checkout: the worktree arrived at 9ca1d8cb (an ancestor of the stated pin). It was moved to the stated pin d1e65a0 with git checkout --detach (clean tree, only .venv untracked). Delta round 14 -> round 15 for LX1-c: project.html only (3 hunks at :53-56, :505-508, :516-519); L04.html changed at :334 (outside cited lines); labs 1-3, data, MANIFEST, references, notation, tools and curriculum/06 byte-identical.",
        "Blind calibration (ruling 15) is UNVERIFIABLE in this session: the verdict lines and annotations were read before the prose extraction. Prose-only scores, for the next clean run: A 4,4,4,4,3; B 2,2,1,2,1 (both match the official scores). A clean-room verifier must run blind_extract_r15.py first and score before reading :493 or :555.",
        "Lab 3 agreement raise: the mutant r13n03 survives every test in tests/. It is detected only by the forced-disagreement script agreement_r15.py, which is not a test. The page states the raise at :60 and :309. Round 14's FAIL is unchanged.",
        "Mutants: 68 listed (65 existing, 3 new). Every one has a recorded kill: 60 existing by the intact-snapshot expected-block comparison, 4 existing by the damaged-snapshot differential (blank cell, month gap, duplicate month), 3 new by the intact run, and r13n03 by the forced-disagreement script only, which is not a test in tests/. Lab mutants are not graded under the architect ruling unless a lesson sentence claims the property; that applies to r13n03 only, and the FAIL row keeps it open.",
        "Alternatives: 3 new correct lab implementations (Decimal lab 1, Decimal lab 2, log-difference and statistics.variance lab 3) all match the expected blocks. Round-14 alternatives were not re-run.",
        "Rubric (proj-rubric-exhaustive-r14, proj-student-error-coverage): round 14 left floor cases uncounted and said a future round may decide them. This round decides them: the floor gaps and the C4 vacuous case are FAIL because the descriptors do not place those essays (exhaustiveness), and three of the plan's ten student-error patterns are not caught by any descriptor. Reviewers may overrule these two rows, but they are recorded as FAIL under fail-closed.",
        "Rung 2 blanks: the page's two '___' lines are the completion blanks; the twin is the completed solution (ruling 11, not a defect).",
        "Process words: 'round' appears only as the rounding operation in learner text ('Round once, at print time'); not a process word.",
        "Not checked: a clean-room blind score (see UNVERIFIABLE row); the cards (outside this slice); the round-14 alternatives; the Pyodide run is page_smoke's own run, not a separate browser session; the registry records for references beyond the three cited keys; a full online verify_refs for the whole registry (CI job scope).",
    ],
    "summary": (f"LX1-c round 15: verdict FAIL. {len(R)} rows: {counts['PASS']} PASS, {counts['FAIL']} FAIL, "
                f"{counts['UNVERIFIABLE']} UNVERIFIABLE. Non-PASS: proj-calibration-exemplars (UNVERIFIABLE: blind condition broken in this session); "
                "proj-lab3-raise-claims-untested (FAIL, unchanged from round 14); proj-rubric-exhaustive-r14 (FAIL, floor cases and C4 vacuous/overlap); "
                "proj-student-error-coverage (FAIL, plan's student errors 1, 2, 4 not caught); proj-data-embedded-claim (FAIL, 'No historical series ... is embedded' contradicted by ust_daily/fx_daily). "
                "Closed this round: proj-exemplar-a-c2-annotation (PASS). Mutants: 68 with a recorded kill (r13n03 by script only, no test). Alternatives: 3/3 match. "
                "Gates all pass: check_pages, check_dag, check_projects, run_labs (7/7 and 3/3), page_smoke, ruff, mypy, pytest, verify_refs (offline and live LX1), fetch_data, build_site, live fx_monthly rebuild byte-identical."),
}
(root / "ledgers/LX1/LX1-c.json").write_text(json.dumps(frag, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
print("rows", len(R), counts, "mutants", len(mutants), "killed", sum(1 for m in mutants if m["killed_by"]))
