"""Round-10 verifier (LX1-c): assembles ledgers/LX1/LX1-c.json from the round-10 outputs under this directory.
Argument 1 is the checkout root. Validates the fragment with tools/ledger.py before writing."""
import json, re, sys, pathlib
sys.path.insert(0, "tools")
import ledger  # noqa: E402

root = pathlib.Path(sys.argv[1])
S = root / "ledgers/LX1/scripts/LX1-c-r10"
SP = "ledgers/LX1/scripts/LX1-c-r10/"
kill = (S / "v10_kill_check_all.out").read_text(encoding="utf-8").splitlines()
killed_line = {}
for line in kill:
    if line.startswith(("KILLED", "SURVIVED")):
        parts = line.split(" | ")
        killed_line[parts[1]] = (parts[0], parts[2] if len(parts) > 2 else "")
mutants = []
for path in sorted((root / "ledgers/LX1/mutants").glob("*.py")):
    first = path.read_text(encoding="utf-8").split("\n")[0]
    doc = re.sub(r'^"""|"""$', "", first).strip()
    status, why = killed_line[path.name]
    mutants.append({
        "name": path.name,
        "description": doc,
        "killed_by": f"{SP}v10_kill_check.py: {why or 'expected-block differs'}" if status == "KILLED" else None,
    })

R = lambda i, check, loc, status, ev, fix=None: dict(
    [("id", i), ("check", check), ("location", loc), ("status", status), ("evidence", ev)]
    + ([("fix", fix)] if fix else []))

rows = [
 R("proj-rung1-step3-rounding-claim", "2.5-numbers", "course/modules/LX/LX1/project.html:173, :175", "PASS",
   f"Re-derived with exact Fractions: {SP}v10_rederive.py -> v10_rederive.out line 'lab1 falling real debt t=5': 10000000/0.85 = 11764705.88235 cents, prints 117647.06 dollars; page :175 says 11764705.882 cents and 117647.06."),
 R("proj-real-value-vs-lesson2", "2.4-mathematics", "project.html:56, :58, :168, :506; course/modules/LX/LX1/L02.html:84, :89-90, :97, :110, :128", "PASS",
   "Read this round: L02.html:84 says Proposition 2.1 uses (A2) and (A3); :89 (A2) fixed nominal debt, :90 (A3) P_t positive with P_0 base; :97 proof (a): V_t/V_{t-1} = P_{t-1}/P_t; :110 debt deflation is arithmetic, not cause; :128 Remark 3.3 says the corollary says nothing about the cause of a fall. The round-10 L02 delta (:309, :535) is not cited on this page."),
 R("proj-manifest-note-misattributed", "2.2-numbers-data", "project.html:269, :277, :291-293; course/assets/data/market/MANIFEST.json (fx_monthly)", "PASS",
   f"MANIFEST fx_monthly read with python json this round: title 'Month-end foreign exchange rates, ten currencies, USD per unit of foreign currency'; transform inverts CAD, CHF, DKK, JPY, NOK, SEK; columns AUD..SEK (10); first 1971-01, last 2026-09, rows 669, retrieved 2026-10-19. Page :277, :291-293 match. Evidence script: {SP}v10_checks_misc.out."),
 R("proj-lab3-citation-string", "2.2-numbers-data", "project.html:277, :285; tests/labs/LX1/lab-LX1-project-3.py docstring lines 288-289", "PASS",
   f"Citation string on page equals MANIFEST citation (string match at :277 and :285, {SP}v10_checks_misc.out line (1)); lab docstring matches after whitespace normalisation (the docstring wraps the string across lines 288-289; checked in round 10)."),
 R("proj-reading-reinhart-registry", "2.1-citations", "project.html:633-638; references/references.json", "PASS",
   "Reading list data-cite keys (project.html:635-637): friedman1963monetary, eichengreen1992golden, garber2000famous. Each exists in references/references.json with status 'verified' (eichengreen1992golden title 'Golden fetters: the gold standard and the Great Depression, 1919-1939'; garber2000famous DOI 10.7551/mitpress/2958.001.0001). No reinhart key appears on the page (grep count 0). Read by python this round."),
 R("proj-spec-current-undefined", "2.6-spec", "project.html:444, :299-300; tests/labs/LX1/lab-LX1-project-3.py WINDOW_THREE_FROM", "PASS",
   "Current condition window defined at :444 as the twelve months ending at the last month of the data used, 2025-10 to 2026-09 for the snapshot; lab 3 sets WINDOW_THREE_FROM = '2025-10' and prints window three 2025-10 to 2026-09 (12 changes, expected block)."),
 R("proj-exemplar-A-condition", "2.6-spec", "project.html:495, :517", "PASS",
   "Exemplar A names window three, 2025-10 to 2026-09, and the last month 2026-09 with MANIFEST field 'last' = '2026-09' (read this round); the 12-change window matches Lab 3 output."),
 R("proj-gate-commands", "2.9-gates", f"{SP}v10_*.out", "PASS",
   "Run this round on pin 00a84795: check_projects LX1 PASS; check_pages LX1 PASS; check_dag LX1 PASS (v10_check_*.out, rc 0); run_labs --unit LX1: PASS (7/7) rc 0; page_smoke --unit LX1 --pages project: PASS, labs 0.0 s, no console error (v10_page_smoke_project.out); fetch_data --check: '3 datasets, 0 problems' (v10_fetch_data_check.out); verify_refs --offline: '560 entries, 0 problems' (v10_verify_refs_offline.out); ruff check and ruff format --check on tests/labs/LX1: pass (v10_ruff_*_labs.out); mypy --no-incremental on the three project twins: 'Success' (v10_mypy_project_labs.out); pytest tests/test_labs.py tests/test_run_labs.py -k LX1: rc 0 (v10_pytest_labs_LX1.out); mutate_graders --unit LX1: no output, rc 0 (no autograder). Not run: repository-wide ruff, mypy and pytest (outside this slice)."),
 R("proj-lab1-twin-run", "2.5-labs", "tests/labs/LX1/lab-LX1-project-1.py; project.html:76-147", "PASS",
   f"{SP}v10_labs_extract.out: page code equals twin (True). Twin run alone with python -I -W error: rc 0, stderr empty, stdout equals the expected block token-for-token (20 lines)."),
 R("proj-lab1-numbers", "2.2-numbers", "project.html:75, :148-167, :168; " + SP + "v10_rederive.out", "PASS",
   "Hypothesis numbers recomputed exactly: 117647.06 (falling, t=5), 17.65 (burden), -13.04 (rising), 86956.52 (rising, t=5), 30690.54 (difference)."),
 R("proj-lab2-twin-run", "2.5-labs", "tests/labs/LX1/lab-LX1-project-2.py; project.html:183-255", "PASS",
   f"{SP}v10_labs_extract.out: page code equals twin except the two blanked lines (page lines 30 and 35, both '___'); mismatches []. Completed twin run alone with python -I -W error: rc 0, stdout equals the expected block (10 lines)."),
 R("proj-lab2-numbers", "2.2-numbers", "project.html:182, :245-254; " + SP + "v10_rederive.out", "PASS",
   "40000.00 at t=0; 43010.75 at t=5 (exact 40000/0.93 = 43010.7527); burden 100*(1/0.93 - 1) = 7.5269 -> 7.53. Intermediate real values 40404.04, 40816.33, 41666.67, 42105.26 match the expected block."),
 R("proj-lab2-check-claims", "2.5-labs", "project.html:255; ledgers/LX1/mutants/lx1c_r9n01_lab2_real_value_without_division.py; lx1c_m02_rung2_burden_ratio_inverted.py", "PASS",
   "Page claims that omitting the division prints 40000.00 in every period (run this round: t=0..5 all 40000.00, expected block differs) and that inverting the ratio prints -7.00 in place of 7.53 (run this round on the twin with the ratio inverted: 'change: -7.00'). Both mutants are KILLED in " + SP + "v10_kill_check_all.out."),
 R("proj-lab3-twin-run", "2.5-labs", "tests/labs/LX1/lab-LX1-project-3.py; project.html:286-435", "PASS",
   f"{SP}v10_labs_extract.out: page code equals twin (True). Twin run alone with python -I -W error in a scratch dir holding data/fx_monthly.csv: rc 0, stderr empty, stdout equals the expected block (20 lines)."),
 R("proj-lab3-numbers", "2.2-numbers", "project.html:285, :411-435; " + SP + "v10_rederive.out", "PASS",
   "Independent recomputation from the CSV with float log changes and an independent sample-sd formula: window one 668 changes, 3 exact zeros (1976-07, 2012-07, 2019-11), sd 2.7935 -> 2.79, largest 13.58 (1985-03); window two 321 changes, 2 zeros (2012-07, 2019-11), sd 2.4700 -> 2.47, largest -9.66 (2008-10); window three 12 changes, 0 zeros, sd 1.9020 -> 1.90, largest 2.96 (2026-04); ratio 0.88417 -> 0.88; difference 0.32358 -> 0.32; statistics.stdev agrees to 1e-9 in all three windows."),
 R("proj-lab3-L04-cross-check", "2.1-citations-numbers", "course/modules/LX/LX1/L04.html:306, :309, :312, :318; project.html:282", "PASS",
   "Read this round: L04.html:306 monthly log changes 668; :309 window one 668 changes, sd 0.027935; :312 window two 321 changes, sd 0.024700; :318 ratio 0.8842 and difference -0.003236 (0.024700-0.027935 = -0.003235 from printed figures). Recomputed unrounded sd 0.02793528 and 0.02469950 (v10_rederive.out)."),
 R("proj-lab3-docstring-claims", "2.5-labs", "tests/labs/LX1/lab-LX1-project-3.py lines 1-28 (page project.html:286-313)", "PASS",
   f"Each docstring claim checked against code and output: reads data/fx_monthly.csv (DATA_PATH line 327); GBP column (COLUMN line 328); 669 months 1971-01 to 2026-09 (printed line 398; CSV rows 669, v10_rederive.out); no interest-rate column (CSV header, v10_rederive.out); blank/non-decimal/gap damage raises ValueError naming the cell or month ({SP}v10_twin_damaged_baseline.out, all three rc 1 with the named message)."),
 R("proj-lab3-interpretation-claims", "2.5-labs", "project.html:436; course/modules/LX/LX1/L04.html:81, :84, :353", "PASS",
   f"Page claims: 12 changes give 11 degrees of freedom (n - 1); the two window-two zero changes (2012-07, 2019-11) are months whose last value equals the previous month's value ({SP}v10_rederive.out zero list); a parity held over window two would give 321 zero changes against 2 observed. L04.html:84 (Definition 2.1, changed this round) now sets x_t = kappa from the month before the window's first change to its last change, so a parity held over window two gives all 321 changes zero. Claim holds under the new definition."),
 R("proj-lab3-difference-line-r5", "2.2-numbers", "project.html:285, :411, :434, :436, :539; tests/labs/LX1/lab-LX1-project-3.py line 125", "PASS",
   "Difference computed from unrounded sds: 100*(0.02793528 - 0.02469950) = 0.32358 -> 0.32 (half up); matches the printed line, the page's 0.32 at :436 and the exemplar A figure at :539."),
 R("proj-lab-simulated-labels", "2.5-labs", "project.html:42, :44, :75, :182, :265, :281-285", "PASS",
   f"Labs 1 and 2 are labelled SIMULATED at :42 and :75 (Lab 1) and :182 (Lab 2) and in the twin docstrings (lab 1 line 78; lab 2 line 185). Lab 3 reads the real snapshot (data-files=\"fx_monthly.csv\", :283) and its section contains 0 occurrences of 'simulated' ({SP}v10_checks_misc.out line (5))."),
 R("proj-data-licence-quote", "2.8-data", "project.html:277; MANIFEST.json fx_monthly.licence and licence_url; tools/data_sources.yaml", "PASS",
   f"Plain curl -sS -L https://www.federalreserve.gov/disclaimer.htm: HTTP 200, 85306 bytes (round 10; {SP}v10_licence_curl.out). The page's quotation ('Unless otherwise indicated, information on Board's website is in the public domain and may be copied and distributed without permission. Please cite to the Board as the source of the information.') is on the page, and it grants redistribution."),
 R("proj-data-snapshot-rebuild", "2.8-data", "course/assets/data/market/fx_monthly.csv; course/assets/data/market/MANIFEST.json; tools/fetch_data.py", "PASS",
   f"Carried from round 8 (course/assets/data/market/* byte-identical since the round-8 pin 0dee921a and the round-9 pin c93dd526: git diff --quiet clean for both ranges): round-8 live rebuild evidence in ledgers/LX1/scripts/LX1-c-r8/. Re-checked this round on the committed file: sha256 60572240d1a9d1832d5021297634b2369723b94098414948b891dd26a8bffe3e = MANIFEST sha256, 67392 bytes = MANIFEST bytes, 669 rows = MANIFEST rows ({SP}v10_snapshot_sha.out); fetch_data --check: 3 datasets, 0 problems."),
 R("proj-data-fields", "2.8-data", "project.html:269, :277, :292-293; course/assets/data/market/fx_monthly.csv", "PASS",
   "CSV header month,AUD,CAD,CHF,DKK,EUR,GBP,JPY,NOK,NZD,SEK; 669 rows 1971-01 to 2026-09; blank cells: EUR 336 only, all in the prefix 1971-01 to 1998-12; GBP 0 blanks; month gaps 0 (" + SP + "v10_rederive.out)."),
 R("proj-data-no-other-series", "2.8-data", "project.html:278; course/assets/data/market/MANIFEST.json datasets", "PASS",
   "MANIFEST datasets this round: fx_daily, fx_monthly, ust_daily. None carries gold holdings, price levels, output, unemployment or bank failures (column lists read by python). project.html:278 says none is in the snapshot set and no redistribution grant for them is recorded; the plan's open item D-1 (plans/LX1-open-items.md:7) records no redistributable historical series."),
 R("proj-spec-ladder", "2.6-spec", "project.html:40-48, :71-170, :178-255, :257-273, :616, :623-629", "PASS",
   "Ladder order as stated: rung 1 worked example, fully solved (lab 1 has no blank; annotated steps :171-178); rung 2 completion with two blanks (:180-256; the site's lab.js outputsMatch with data-tolerance 1e-6 compares the printed block with the expected block); rung 3 specification (:259-273) with the check of Lab 3; rung 4 stretch (:623-629). Read in full this round."),
 R("proj-spec-curriculum-scope", "2.6-spec", "curriculum/06-profession-capstone.yaml:42-49; project.html:259-273, :441-451", "PASS",
   "Curriculum project title 'Then vs. now' (yaml :42-49) matches page :36 and :6. The curriculum brief sentence (pick one episode and one condition; mechanism-level comparison; where the analogy holds and breaks) is in page :444-445. The curriculum deliverable 'every claim cited' is stated at :267 and :447 with the own-inference exception; the exception applies to inferences, which are not factual claims, so this is consistent. Note, not a failure."),
 R("proj-hours", "2.6-hours", "project.html:33, :455-466; course/modules/LX/LX1/index.html:29", "PASS",
   "Time budget rows 1 + 1 + 2 + 1.5 + 2.5 + 2 = 10 h (project.html:458-463); data-hours-project=10 at project.html:33 and index.html:29 agree. Own estimate for a competent student: rung 1 about 1 h; rung 2 about 0.5 h; episode and condition with locators about 2 h; outline about 1.5 h; drafting two cited pages with formulas about 3 h; Lab 3 run and reading about 0.25 h; self-assessment about 2 h; total about 10.25 h, within 30 percent of 10 h."),
 R("proj-rubric-observable", "2.6-rubric", "course/modules/LX/LX1/project.html:480 (C4 level 1 cell 'Rounds the numbers.')", "FAIL",
   "C4 level 1 'Rounds the numbers.' names no element a reader can check. The level is also unreachable as the highest level: level 2 ('Rounds the inputs before computing, or states no rule') is satisfied by every essay that fails level 3 (a rounded input, or a computed number with no rule), and an essay with unrounded inputs and a rule for every number meets level 3 or 4. Under the highest-level rule no essay with computed numbers scores level 1 on C4. Other descriptors checked: C1, C2 (levels 1, 2, 3, 4 except the gap in proj-rubric-c2-gap), C3 (levels 1-4), C5 (levels 1-4) are observable; C5 level 2 'Names one limit' is read as 'at least one' (not a failure).",
   "Replace the two lower C4 cells: level 2 'Rounds an input before computing, or states a rounding rule for some computed numbers but not all.'; level 1 'States no rounding rule for any computed number.' Keep level 3 and level 4 unchanged. Re-run the blind calibration for exemplars A and B after the change (proj-calibration-exemplars)."),
 R("proj-calibration-exemplars", "2.6-rubric", "project.html:487-613; stripped text not produced", "UNVERIFIABLE",
   "Blind scoring could not be done in this session: the whole of project.html, including the exemplar annotations, verdicts and data-scores, was read before scoring, so the scores below are not a clean-room calibration. Rubric-only scoring from the exemplar passages gives exemplar A 4,4,4,4,3 (official 4,4,4,4,3) and exemplar B 2,2,1,2,1 (official 2,2,1,2,1), within one level on every criterion. This is a match, not a blind pass.",
   "A clean-room verifier that has not read the annotations scores a copy of project.html with the verdict, annotation, data-scores and reveal text removed, then compares with the official scores, within one level per criterion."),
 R("proj-exemplar-numbers", "2.2-numbers", "project.html:527-534 (A Numbers), :537-547 (A Limits), :581-589 (B Numbers and C4 annotation)", "PASS",
   "Exemplar A: 17.65 (Lab 1 Part B, recomputed), 2.47, 2.79, 1.90 (Lab 3 expected block), ratio 0.88 (unrounded 0.88417), difference 0.32 (unrounded 0.32358). Exemplar B: 2.47/2.79 = 0.8853 -> 0.89 as the essay says, and 0.88 from unrounded values as its C4 annotation says; 'per year' is the wrong unit, as its verdict says."),
 R("proj-reading-keys", "2.1-citations", "project.html:633-638; references/references.json", "PASS",
   "All three reading-list keys exist in references/references.json (status verified). No other citation key appears on the page (grep of data-cite and key-like tokens). verify_refs --offline: 560 entries, 0 problems (" + SP + "v10_verify_refs_offline.out)."),
 R("proj-notation", "2.4-notation", "project.html TeX spans (29 spans, " + SP + "v10_math_spans.out); notation/notation.json", "PASS",
   "Spans use D, P_t, P_0, V_t, S_m, m, t, n, ln, P_{t-1}, P_5. notation/notation.json registers program-wide symbols T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q}; none is used on the page with another meaning. Local symbols are defined at :56, :58, :60 and :517; n is not defined (row proj-notation-n-undefined)."),
 R("proj-scope-words", "2.9-prose", "project.html (scope words; " + SP + "v10_scope_words.out lists 129 hits)", "PASS",
   "Prose hits checked line by line, including the round-10 delta lines. Examples: :282 'It is the only lab on this page that reads a file' (labs 1 and 2 read no file; " + SP + "v10_checks_misc.out line (4)); :265 'Labs 1 and 2 use SIMULATED paths only'; :436 'none of them says why it moved'; :539 'the largest absolute monthly log change of the GBP column' (window one holds every change, so it is the column's largest). The 'must' at :436 is a separate row (proj-spec-window-start-must)."),
 R("proj-process-words", "2.9-prose", "project.html (all prose, labs and comments); BUILDER_RULES.md §1.3-1.4", "PASS",
   "Grep for TODO, TBD, lorem, ellipsis, 'for brevity', 'beyond the scope', 'details omitted', 'left as an exercise', 'you can add more', builder, verifier, round, fixer, ledger, batch, agent, planner, architect, pending, studio, 'it is important to note', 'studies show', 'experts agree', 'it is well known', 'obviously', 'clearly': zero hits (" + SP + "v10_banned_grep.out is empty). No rhetorical-question transitions in prose."),
 R("proj-links-anchors", "2.9-structure", "project.html (all href targets); course/modules/LX/LX1/L02.html:110 (def-debt-deflation); index.html:73 (placement)", "PASS",
   f"{SP}v10_checks_misc.out line (2): no href problems (fragment ids present in project.html; target files exist; L02 and index fragments present). index.html:73 is the placement section with data-mastery 0.8 (index.html:73)."),
 R("proj-page-smoke", "2.5-labs-2.9-structure", "course/modules/LX/LX1/project.html; " + SP + "v10_page_smoke_project.out", "PASS",
   "page_smoke --unit LX1 --pages project: 'page_smoke modules/LX/LX1/project.html: PASS'; labs 1-3 timed at 0.0 s; no console error line; math rendered by the check. Not done: an in-browser look at the self-assessment form and the exemplar reveal (the form needs JavaScript)."),
 R("proj-atlas-autograder-na", "2.6-atlas-autograder", "curriculum/06-profession-capstone.yaml:19-49; course/modules/LX/LX1/ (no grader directory)", "PASS",
   "No atlas key in the LX1 entry (yaml lines 19-49); grading: rubric (yaml project block); no grader/ directory; tools/mutate_graders.py --unit LX1 --seeds 0-9 printed nothing and exited 0 (" + SP + "v10_mutate_graders_LX1.out). Autograder and Atlas checks therefore do not apply."),
 R("proj-mutants-student-errors", "2.6-mutation", "ledgers/LX1/mutants/*.py (50 files); " + SP + "v10_kill_check_all.out", "PASS",
   "All 50 project-lab mutants run alone under python -I -W error against the page expected blocks and the damaged-snapshot checks: TOTAL killed=50 survived=0. New this round (student errors not in earlier rounds): lx1c_r10n01 lab 3 reads GBP inverted (1/S), expected block differs; lx1c_r10n02 lab 2 real debt floor-divided (truncates the cent), expected block differs at t=2; lx1c_r10n03 lab 1 burden without subtracting one, expected block differs; lx1c_r10n04 lab 1 cents printed without zero padding (100000.0), expected block differs."),
 R("proj-alternatives", "2.6-alternatives", SP + "v9_alt_*.py (re-run), " + SP + "v10_make_alt_lab2_float.py", "PASS",
   "Four correct alternatives re-run this round, each output equal to the page expected block: lab 1 float arithmetic with Decimal printing (v9_alt_lab1_float_and_lab2_ratio.py); lab 2 ratio and check (v9_alt_lab2_check.py); lab 3 Welford online sd and log via math.log(v) - math.log(prev) (v9_alt_lab3_welford_and_log1p.py); lab 2 completion in floats with the burden written as 100*(start - end)/end (v10_alt2float_lab2.py, output v10_alt2float_lab2.out, equal to the expected block by v10_alt_expected_compare.out). Output files: ledgers/LX1/scripts/LX1-c-r10/v10_v9_alt_*.out."),
 R("proj-exemplar-a-c2-annotation", "2.2-cites", "project.html:505-521; course/modules/LX/LX1/L02.html:97, :127-128", "PASS",
   "Exemplar A's C2 evidence for step 2 is L02.html:128 ('The corollary says nothing about the cause of a fall'); step 3 identity is L02.html:97. Read this round."),
 R("proj-exemplar-b-annotations-vs-descriptors", "2.6-rubric", "project.html:551-613 (annotations :561, :573-576, :586-587, :598-599, :610); descriptors :476-481", "PASS",
   "Each exemplar B annotation names a descriptor it meets or misses and the text matches the cell: C1 level 2 (:477 'a date or a locator is missing for one of them'); C1 level 3 miss (:477 'all but one date'); C2 level 2 (:478 'Lists similarities and one difference, with no chain of steps'); C3 level 1 (:479 'Lists at least one source'); C3 level 2 miss (:479 'At most two factual claims are uncited'; three uncited claims); C3 level 3 miss; C4 level 2 (:480); C4 level 3 miss; C5 level 1 (:481 'Mentions a caveat without naming what it limits')."),
 R("proj-brief-rubric-escape-clauses", "2.6-rubric", "project.html:269 (spec constraints), :447 (brief item 4), :479 (C3 level 4)", "PASS",
   "The counter-evidence clause ('a claim graded B or C names its counter-evidence, or the essay states that it makes no such claim') is at :269, :447 and :479, identical in substance. Round 9 also cited :263 for it; :263 (spec context) does not contain the clause, so that citation is withdrawn."),
 R("proj-exemplar-locators", "2.6-rubric", "project.html:495, :506, :517, :528, :539; L02.html:97, :128; L04.html:328; references/references.json (eichengreen title)", "PASS",
   "Each exemplar A locator exists: title field of Eichengreen (references.json entry eichengreen1992golden); Proposition 2.1(a) and Remark 3.3 (L02.html:97, :128); MANIFEST transform field (fx_monthly); Lab 1 Part B and Lab 3 printed lines; MANIFEST columns and Lesson 4 Section 4 item 'Exchange rates only' (L04.html:328, which names covered interest parity)."),
 R("proj-honest-pending-data-note", "2.8-data", "project.html:278; plans/LX1-build-plan.md (B1 default); plans/LX1-open-items.md:7 (D-1)", "PASS",
   "Page: 'No historical series for your episode is embedded ... no redistribution grant for any of them has been recorded.' Matches the open-items D-1 record (no redistributable historical series; none read) and the snapshot set (three datasets, no historical series)."),
 R("proj-exemplar-a-c5-limit-count", "2.6-rubric", "project.html:491, :539, :544, :545; :267, :448", "PASS",
   "Re-verified after the round-10 delta: exemplar A names three limits (:539); verdict at :491 'limit one has a test, but limits two and three name none'; the C5 level 3 annotation (:544) and the level 4 miss (:545) match that; C5 level 3 descriptor (:481) 'Names two limits, one with the test' is met; spec :267 and brief :448 require two limits with the test for at least one, consistent with the rubric."),
 R("proj-round10-delta-project-page", "2.9-structure", "course/modules/LX/LX1/project.html:267, :448, :491, :545; tests/labs/LX1/*project*; course/assets/data/market; references; notation", "PASS",
   "Delta c93dd526..00a84795 read in full for this slice: project.html four changed lines (:267 required outputs, :448 brief item 5, :491 exemplar A verdict, :545 exemplar A C5 aside); lab twins, data, references, notation, MANIFEST and the curriculum entry byte-identical (git diff --quiet). Changed L02/L04 lines were read where cited (L04.html:84). The four r9n01-04 mutants are present and counted."),
 R("proj-lab3-raise-claims-untested", "2.5-labs", "course/modules/LX/LX1/project.html:306-308; tests/labs/LX1/lab-LX1-project-3.py lines 21-23, 59-74; no committed test at the pin", "FAIL",
   f"The claim is true: the twin raises ValueError on a blank cell, a non-decimal cell and a removed month, naming the cell or month ({SP}v10_twin_damaged_baseline.out, all four checks). But the pin 00a84795 has no committed test for it (git ls-files tests | grep -c test_lx1_project_lab3 = 0). Two round-8 mutants (r8n03 blank cell, r8n04 month gap) survived the builder's checks and were killed only by verifier scripts, so the raise behaviour is a regression risk that no repository test guards. An untracked tests/test_lx1_project_lab3.py exists in the primary checkout and is not part of this pin.",
   "Commit tests/test_lx1_project_lab3.py that runs tests/labs/LX1/lab-LX1-project-3.py under python -I -W error on copies of fx_monthly.csv with (a) the 2000-06 GBP cell blanked, (b) it set to 'n/a', (c) the 1990-06 row removed, and asserts rc != 0, empty stdout, and stderr containing 'ValueError: 2000-06: GBP cell' or 'ValueError: month 1990-07 does not follow 1990-05'. Then re-run the mutant kill check."),
 R("proj-spec-limits-test-each", "2.6-spec", "course/modules/LX/LX1/project.html:267, :448, :481, :491, :545", "PASS",
   "Round-9 FAIL resolved in the round-10 delta: :267 and :448 now require two limits and the test for at least one ('For at least one of them'); C5 level 3 (:481) 'Names two limits, one with the test' is consistent; exemplar A's verdict (:491) and aside (:545) say limits two and three name no test. Spec, brief, rubric and exemplar agree."),
 R("proj-notation-n-undefined", "2.4-notation", "project.html:60 ('denominator n - 1'), :303 (Lab 3 docstring); tests/labs/LX1/lab-LX1-project-3.py lines 18 and 84", "PASS",
   "n (the number of changes in a window) is used without a definition on the page. It is the conventional sample size, not a registry symbol, so it does not collide with notation.json. Recorded as a judgment, not a failure; a one-line definition would remove the question."),
 R("proj-spec-window-start-must", "2.6-spec", "course/modules/LX/LX1/project.html:436", "FAIL",
   "The Lab 3 interpretation says 'so the essay must name the window start as a limit'. The spec (:267, :448) lets the student choose two limits; this sentence makes one of them mandatory, which a competent student would have to ask about. Not a rubric defect: the rubric does not require it.",
   "Replace 'so the essay must name the window start as a limit' with 'so the window start is a candidate limit of the analogy, which the essay may name or not.'"),
 R("proj-rubric-c2-gap", "2.6-rubric", "course/modules/LX/LX1/project.html:478 (C2 cells, levels 2 and 1)", "FAIL",
   "Rubric not exhaustive for C2: an essay that gives a chain of at least three steps for each mechanism but names no failure step fits no level. Level 3 needs the failure step; level 2 ('Lists similarities and one difference, with no chain of steps') and level 1 ('Names at least one similarity, with no chain of steps') both require the absence of a chain. The same gap arises when the chain is given for only one mechanism and the failure step is named for neither.",
   "Change the C2 level 2 cell to 'Lists similarities and one difference, or gives a chain of steps but names no failure step.' Leave levels 1, 3 and 4 unchanged."),
]

ids = [r["id"] for r in rows]
assert len(ids) == len(set(ids)), "duplicate ids"
counts = {s: sum(1 for r in rows if r["status"] == s) for s in ("PASS", "FAIL", "UNVERIFIABLE")}
verdict = "PASS" if counts["PASS"] == len(rows) else "FAIL"
fragment = {
    "unit": "LX1",
    "slice": "LX1-c",
    "round": 10,
    "verifier": "Claude Haiku 5.5 (claude-haiku-5-5), independent verifier for LX1-c, round 10 (did not build LX1)",
    "pin": "00a84795f276456fce19d4181373cc4efba11a36",
    "base": "c93dd526025c6dffd34c54cd2c89eb62a890f885 (round-9 pin). Delta in slice: project.html four changed lines (:267, :448, :491, :545); four mutants r9n01-04 already present at the round-9 pin's successor commit. Lab twins, data, references, notation, MANIFEST, curriculum entry byte-identical.",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE10-LX1-c",
    "scratch": "/tmp/lx1c-r10-scratch (disclaimer.html, alt runs, alt2float.py); scripts and outputs kept in ledgers/LX1/scripts/LX1-c-r10/",
    "verified_at": "2026-11-05T07:50:00+00:00",
    "verdict": verdict,
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Round-9 FAIL proj-spec-limits-test-each is PASS now (wording changed at :267 and :448 and consistent in exemplar A). Round-9 FAIL proj-lab3-raise-claims-untested is still FAIL (no committed test at the pin). Round-9 PASS proj-rubric-observable is FAIL now: the C4 level-1 descriptor is vague and unreachable (new analysis of the highest-level rule).",
        "Round-9 cited :263 for the counter-evidence clause; :263 does not contain it. Corrected in proj-brief-rubric-escape-clauses (status unchanged).",
        "Calibration: the exemplars were not scored blind in this session (annotations read first), so proj-calibration-exemplars is UNVERIFIABLE; the rubric-only scores match the official ones within one level.",
        "Floor note (not a row): an essay that meets no level-1 element of some criterion (for example, no source at all for C3) gets no score under the highest-level rule; the rubric has no level 0. Applies to all five criteria; the author may want a stated floor.",
        "Observation, not a finding: rung 2's expected block shows the answer values (40000.00, 43010.75, 7.53) on the page, so a student can match the printed values without deriving the formulas. This is a pedagogical choice, not a defect of the check.",
        "Lab 3 agreement tolerance (1e-9 percent, twin line 331) is not observable by any input (two-pass and statistics.stdev differ only at float rounding); recorded as an untested constant, not as a finding.",
        "Lab 3 rounding by Decimal ROUND_HALF_UP is equivalent to the page's rule on this data; a banker's-rounding mutant survives on the data because no printed value is an exact binary tie. Lab twins are demonstrations, so this is not a finding (no page sentence says the lab detects it).",
        "Spec questions a competent student would still ask: (1) whether self_assessment.md must be submitted or is only the form's output (:267); (2) what counts as one factual claim for the C3 counts; (3) whether the window-start sentence at :436 is a requirement (row proj-spec-window-start-must).",
        "Not checked: in-browser rendering of the self-assessment form and of the exemplar reveal; the printed length of the two pages (the page says the tools do not measure it); cards.json and L01-L04 (other slices); the live verify_refs run (offline run only; no reference changed); a fresh live snapshot rebuild (carried from round 8, bytes unchanged since round 8); the repository-wide gates outside this slice.",
    ],
    "summary": (f"LX1-c round 10: verdict {verdict}. {len(rows)} rows: {counts['PASS']} PASS, {counts['FAIL']} FAIL, {counts['UNVERIFIABLE']} UNVERIFIABLE. "
                f"Mutants {sum(1 for m in mutants if m['killed_by'])}/{len(mutants)} killed (46 existing + 4 new r10n01-04). "
                "Labs 1-3 pass under python -I -W error with output equal to the expected blocks; run_labs LX1 7/7; three round-9 alternatives and one new float alternative match."),
}
problems = ledger.validate(fragment, "LX1-c")
print("validate:", problems)
(root / "ledgers/LX1/LX1-c.json").write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote ledgers/LX1/LX1-c.json", counts, "mutants", len(mutants))
