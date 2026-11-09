"""LX1-c round 19 fragment writer (verifier-written). Writes ledgers/LX1/LX1-c.json from the evidence gathered in
ledgers/LX1/scripts/LX1-c-r19/ and the mutant outputs. Run from the checkout root: python -I <this file>.
"""
import json
import pathlib
import re

ROOT = pathlib.Path(".").resolve()
S = "ledgers/LX1/scripts/LX1-c-r19"
OUT = ROOT / S / "out"
PAGE = "course/modules/LX/LX1/project.html"

R = []


def row(rid, check, location, status, evidence, fix=""):
    R.append({"id": rid, "check": check, "location": location, "status": status, "evidence": evidence, "fix": fix})


def carried(rid, check, location, evidence, fix=""):
    row(rid, check, location, "PASS", "Carried from round 18 (" + evidence + ")", fix)


# ---- Lab 1, Lab 2 and Lab 3 (run and recomputed) ----
row("proj-rung1-step3-rounding-claim", "2.5-labs", f"{PAGE}:177, :179", "PASS",
    f"Re-derived by python -I arithmetic in project_claims_r19.py: 10000000/0.85 cents = 11764705.882 (prints 117647.06); "
    f"10000000/0.85 - 10000000/1.15 = 3069053.708 cents (prints 30690.54). {S}/out/project_claims_r19.out")
row("proj-real-value-vs-lesson2", "2.9-prose", f"{PAGE}:55-59; course/modules/LX/LX1/L02.html:84-90, :123, :127-131",
    "PASS", "Definition :56 V_t = D P_0/P_t with P_0 = 1 matches L02 identity (Proposition 2.1, hypotheses (A2),(A3) at "
    "L02.html:84-90); :170 debt-deflation sentence matches L02.html:110 (Definition); Remark 3.3 at L02.html:127-129 "
    "says the corollary gives no cause, which the exemplar A chain cites.")
row("proj-manifest-note-misattributed", "2.2-numbers", f"{PAGE}:271, :279, :294; course/assets/data/market/MANIFEST.json (fx_monthly)",
    "PASS", "MANIFEST fx_monthly: first 1971-01, last 2026-09, rows 669, retrieved 2026-10-19, transform inverts only "
    "CAD,CHF,DKK,JPY,NOK,SEK (matches :294 and the Lab 3 docstring). Blank counts by column: "
    f"{S}/out/scan_r19.out (EUR blank 1971-01..1998-12, 336 rows; no other column blank).")
row("proj-lab3-citation-string", "2.1-citation", f"{PAGE}:279, :287; MANIFEST fx_monthly citation",
    "PASS", "Citation string at :279 and :287 is byte-identical to MANIFEST fx_monthly.citation (G.5/H.10 ... noon "
    "buying rates in New York); retrieved date matches.")
row("proj-reading-reinhart-registry", "2.1-citation", f"{PAGE}:626-640; references/references.json",
    "PASS", "Reading list keys (friedman1963monetary, eichengreen1992golden, garber2000famous) and reinhart2009this "
    "are registry entries (references/references.json entries with those keys; used_by includes LX1). Friedman "
    "record lists one author; the page cites the key only (plans/LX1-open-items.md).")
row("proj-spec-current-undefined", "2.6-spec", f"{PAGE}:439, :301-302, :444", "PASS",
    "Current condition defined as dated within the twelve months ending at the last month of the data (:439); the "
    "snapshot window 2025-10..2026-09 is stated at :301-302 and matches Lab 3 window three (12 changes). Question a "
    "student could ask (not a FAIL): for a source outside the snapshot, which month is 'the last month of the data'.")
row("proj-exemplar-A-condition", "2.6-exemplars", f"{PAGE}:490-491", "PASS",
    "Exemplar A condition: window three 2025-10..2026-09; last month 2026-09 from MANIFEST field last "
    "(course/assets/data/market/MANIFEST.json), retrieved 2026-10-19 (matches).")
row("proj-gate-commands", "gate", f"{S}/run_gates_r19.sh; {S}/out/*.out", "PASS",
    "check_projects --unit LX1 PASS; check_projects --all PASS; check_pages --unit LX1 PASS; check_dag --unit LX1 PASS "
    "and --all PASS; run_labs --unit LX1 PASS (7/7); run_labs --unit LX1 --page project PASS (3/3); "
    "page_smoke --unit LX1 --pages project PASS; verify_refs --offline 560 entries, 0 problems; verify_refs --unit LX1 "
    "live 4 of 560 entries, 0 problems; fetch_data --check 0 problems; build_site --check current; ruff check and "
    "format clean; mypy --no-incremental success (385 files); pytest test_labs/test_run_labs/test_page_smoke/"
    "test_page_checks/test_curriculum rc 0; pytest test_refs rc 0. Not run: full repository pytest (see notes).")
row("proj-lab1-twin-run", "2.5-labs", f"{PAGE}:78-149, :150-169; tests/labs/LX1/lab-LX1-project-1.py", "PASS",
    f"Page code equals twin (harness twins mode: page-vs-twin diffs=0). Twin under python -I -W error: rc 0, "
    f"stderr 0 bytes, stdout equals expected block (20 lines). {S}/out/twins_r19.out; {S}/out/project_claims_r19.out")
row("proj-lab1-numbers", "2.2-numbers", f"{PAGE}:77, :150-169", "PASS",
    "Hypothesis numbers 117647.06, -13.04, 30690.54, 17.65 and the Part A table re-derived (unrounded values in "
    f"{S}/out/project_claims_r19.out); all match the printed block.")
row("proj-lab2-twin-run", "2.5-labs", f"{PAGE}:185-246, :247-256; tests/labs/LX1/lab-LX1-project-2.py", "PASS",
    f"Page completion code equals completed twin except the two blank lines (:214, :219). Twin: rc 0, stderr 0, stdout "
    f"equals expected block (10 lines). {S}/out/twins_r19.out")
row("proj-lab2-numbers", "2.2-numbers", f"{PAGE}:184, :247-256", "PASS",
    "40404.04, 40816.33, 41666.67, 42105.26, 43010.75 and 7.53 re-derived (unrounded in "
    f"{S}/out/project_claims_r19.out); hypothesis sentence states 43010.75 and 7.53 and matches.")
row("proj-lab2-check-claims", "2.2-numbers", f"{PAGE}:257", "PASS",
    "Claim 'a real-value line that leaves out the division prints 40000.00 in every period' is arithmetic (D/1 = D). "
    "Claim 'a burden line that inverts the ratio prints -7.00' re-derived: 100*(0.93/1 - 1) = -7.000000. "
    "Compare is whole-block (course/assets/js/labs.js:133-137, compareOutput on the completion block).")
row("proj-lab3-twin-run", "2.5-labs", f"{PAGE}:285-432; tests/labs/LX1/lab-LX1-project-3.py", "PASS",
    f"Page code equals twin (diffs=0). Twin run from scratch dir with data/fx_monthly.csv under python -I -W error: "
    f"rc 0, stderr 0, stdout equals expected block (19 lines). {S}/out/twins_r19.out")
row("proj-lab3-numbers", "2.2-numbers", f"{PAGE}:287, :412-431", "PASS",
    "Independent Decimal ln + two-pass Decimal sd (lab3_indep_r19.py, out/lab3_indep_r19.out): window one n=668 zeros=3 "
    "sd 0.027935 -> 2.79, largest 13.58 (1985-03); window two n=321 zeros=2 sd 0.024700 -> 2.47, largest -9.66 "
    "(2008-10); window three n=12 zeros=0 sd 0.019020 -> 1.90, largest 2.96 (2026-04); ratio 0.884169 -> 0.88; "
    "difference 0.323578 -> 0.32. Matches printed block and the hypothesis.")
row("proj-lab3-L04-cross-check", "2.1-citation", f"course/modules/LX/LX1/L04.html:314, :317; {PAGE}:284, :298",
    "PASS", "L04.html:314 'window one ... changes 668; standard deviation 0.027935' and :317 'window two ... 321; "
    "0.024700' match :284 and the docstring :297-298. L04 prints the same counts (668, 321).")
row("proj-lab3-docstring-claims", "2.5-labs", f"{PAGE}:288-315 (twin docstring mirrored); tests/labs/LX1/lab-LX1-project-3.py:1-40",
    "PASS", "Each docstring statement checked against code: log change ln(S_m/S_(m-1)) (log_changes); n-1 denominator "
    "(sample_sd_two_pass); windows by month string (WINDOW_TWO_FROM, WINDOW_THREE_FROM); blank or non-decimal cell "
    "raises ValueError and a gap raises ValueError (load_column). Verified by "
    f"{S}/gap_and_text_r19.py -> out/gap_and_text_r19.out: dropped month rc1 ValueError; 'n/a' GBP cell rc1 ValueError; "
    "repeated month rc1 ValueError. MANIFEST transform list matches :294.")
row("proj-lab3-interpretation-claims", "2.2-numbers", f"{PAGE}:431-432; course/modules/LX/LX1/L04.html:84-94 (Definition 2.1, (A2), Proposition 2.2)",
    "PASS", "Proposition 2.2(a) gives zero log change under (A2) (L04.html:94, 99); Definition 2.1 contains (A2) fixed rate "
    "held (L04.html:85). The 321-zero counterfactual at :432 is the (A2) consequence over window two (321 changes). "
    "Interpretation names only printed numbers and their definitions.")
row("proj-lab3-difference-line-r5", "2.5-labs", f"{PAGE}:287, :412-431; tests/labs/LX1/lab-LX1-project-3.py (difference line)",
    "PASS", "Difference printed as 0.32 is 100*(sd1 - sd2) from unrounded values (0.323578); the difference of printed "
    "values would be 0.32 too, so the lab's rule is tested by mutant r18n02 (out/alts and kill outputs).")
row("proj-lab-simulated-labels", "2.8-data", f"{PAGE}:42, :77, :80, :184, :187, :283-287", "PASS",
    "Labs 1 and 2 state SIMULATED in hypothesis and docstring; both read no file (grep open( in twins: 0). Lab 3 reads "
    "the embedded snapshot (data-files=\"fx_monthly.csv\", :285) and is not labelled SIMULATED.")
row("proj-data-licence-quote", "2.8-data", f"{PAGE}:279; https://www.federalreserve.gov/disclaimer.htm",
    "PASS", "Plain curl (HTTP 200, 2026-11-09) of licence_url; the quoted sentence 'Unless otherwise indicated, information "
    "on Board's website is in the public domain and may be copied and distributed without permission. Please cite to "
    f"the Board as the source of the information.' is present verbatim. {S}/licence_check_r19.sh; {S}/out/licence_check_r19.out")
row("proj-data-snapshot-rebuild", "2.8-data", "course/assets/data/market/fx_monthly.csv; course/assets/data/market/MANIFEST.json (fx_monthly)",
    "PASS", f"{S}/rebuild_fx_monthly_r19.sh (tools/fetch_data.py --fetch --only fx_monthly in a new scratch copy) rebuilt the CSV "
    "from the live feed: cmp identical to the committed CSV; sha256 60572240d1a9d1832d5021297634b2369723b94098414948b891dd26a8bffe3e "
    "equals MANIFEST sha256. Raw download sha256 1c312d2f... differs from MANIFEST raw_sha256 8f370f9c... (issuer's live file "
    "changed since retrieved 2026-10-19); recorded as provenance, MANIFEST not refreshed (BUILDER_RULES §6.6).")
row("proj-data-fields", "2.8-data", f"{PAGE}:271, :279-280, :292-294; course/assets/data/market/fx_monthly.csv", "PASS",
    "669 rows 1971-01..2026-09; GBP has no blank cell; EUR blank 1971-01..1998-12 (336 rows) and value from 1999-01 "
    f"(page :271 and :279 say so). Columns and titles match MANIFEST. {S}/out/scan_r19.out")
row("proj-data-no-other-series", "2.8-data", f"{PAGE}:280; course/assets/data/market/MANIFEST.json", "PASS",
    "MANIFEST datasets: fx_daily (daily FX), fx_monthly (month-end FX), ust_daily (Treasury yields). None has a gold, "
    "price-level, output, unemployment or bank-failure title or column (titles read from MANIFEST).")
row("proj-spec-ladder", "2.6-spec", f"{PAGE}:40-48, :73-258, :261-275, :618-624", "PASS",
    "Rung 1 worked example with annotated steps (:173-180); rung 2 completion lab graded instantly (labs.js:133-141); rung 3 "
    "spec with context, inputs, outputs, constraints, grading mode (:263-275); rung 4 open-ended stretch (:619-624). "
    "check_projects --unit LX1 PASS.")
carried("proj-spec-curriculum-scope", "2.6-spec", f"curriculum/06-profession-capstone.yaml:42-49; {PAGE}:263-273, :436-446",
        "curriculum/06-profession-capstone.yaml and the spec and brief lines 263-273 and 437-446 are byte-identical since the "
        "previous pin (git diff 505592668894..cd4dd7df lists no hunk there); the brief matches curriculum lines 43-49.")
carried("proj-hours", "2.6-hours", f"{PAGE}:33, :35, :448-461; course/modules/LX/LX1/index.html:29",
        "hours block lines 449-463 and hub index.html are byte-identical since the previous pin. Re-added: components "
        "1+1+2+1.5+2.5+2 = 10 (sum equals :460 and data-hours-project=10). Estimates: the ruling says hours are design "
        "targets, so only the arithmetic is a gate. Not timed; no sub-30% estimate check was made beyond the arithmetic.")
row("proj-rubric-observable", "2.6-rubric", f"{PAGE}:467, :473-477", "FAIL",
    "Descriptor quantifier ambiguity in C1 level 2 (:473, td 3): 'a date or a locator is missing for one of them'. An essay "
    "that dates both the episode and the condition and gives no locator for either is missing a locator for both. Read as "
    "'for at least one' it scores 2; read as 'for exactly one' it fails L2 and falls to L1 ('Picks two events'), so the "
    "score is 1. Both readings are reproduced by the scoring model "
    f"({S}/rubric_coverage_r19.py, out/rubric_coverage_r19.out: 'dated both, no locators -> 2' lenient, '-> 1' strict). "
    "The other descriptors (C2 L2 'Lists similarities' at :474) were read; the plural is a wording point only (see notes).",
    "At :473 td 3 change 'a date or a locator is missing for one of them' to 'a date or a locator is missing for one or both "
    "of them', so that the score does not depend on the reading.")
row("proj-calibration-exemplars", "2.6-rubric-calibration",
    f"{PAGE}:485 (exemplar A data-scores 4,4,4,4,3), :547 (exemplar B data-scores 2,2,1,2,1); blind scorer ~/.fanout/blind/LX1-c.json",
    "PASS", "Ruling 23: exemplars scored by the blind scorer, not by this verifier. Blind scores A [4,4,4,4,3] and B [2,2,1,2,1] "
    "(/Users/billyribeiro/.fanout/blind/LX1-c.json, keys A and B). Official scores at :485 and :547 are identical, so each "
    "criterion is within one level. The scorer applied the highest-level rule of :467 (the file notes the rubric.txt copy "
    "it read has no scoring paragraph; the rule was taken from the coordinator message, which matches :467).")
row("proj-exemplar-numbers", "2.2-numbers", f"{PAGE}:501-534 (exemplar A), :523, :534; :552-605 (exemplar B), :577, :581",
    "PASS", "Exemplar A: 17.65 = 100(1/0.85-1) (unrounded 17.647059); 2.47, 2.79, 1.90 from Lab 3 printed lines; 0.88 ratio "
    "(unrounded 0.884169); 13.58 (1985-03) and 0.32 difference from Lab 3. Exemplar B: 2.47/2.79 = 0.8853 -> 0.89 and 1-0.88 = 12 "
    "percent, which the B annotation correctly flags (:582); the 2.47 'per year' claim is the intended error, flagged at :582-583.")
carried("proj-reading-keys", "2.1-citation", f"{PAGE}:627-635; references/references.json",
        "reading list lines 627-635 and references/references.json are byte-identical since the previous pin (no references "
        "hunk in git diff 505592668894..cd4dd7df); keys eichengreen1992golden (title '1919-1939' at its title field), "
        "friedman1963monetary, garber2000famous are present.")
row("proj-notation", "2.4-notation", f"{PAGE} TeX spans (lines 56-60, 175-180, 431, 502-535)", "PASS",
    "TeX symbols on the page: D, P_t, P_0, P_5, P_{t-1}, S_m, S_{m-1}, V_0, V_t, \\ln, m, n, t "
    f"({S}/out/scan_r19.out). The registered program-wide symbols in notation/notation.json are T, Phi, gamma_3, gamma_4, R^ast, "
    "R^{e ast}, R_f and Q: none collides with a page symbol. Local letters are allowed by BUILDER_RULES §3.")
row("proj-scope-words", "2.9-prose", f"{PAGE} learner prose (counts in {S}/out/scan_r19.out)", "PASS",
    "Counts: every 28, only 9, same 7, any 7, the first 7, all 4, the last 4, always/never/exactly/drives 0. Spot-checked the "
    "universal claims: 'every value is an exact Fraction' (Lab 1 twin, Fraction throughout), 'window one holds every monthly "
    "change' (668 computed), 'it is the only lab on this page that reads a file' (only twin 3 opens a file), 'every run prints "
    "the same lines' (no RNG; grep random: docstring only).")
row("proj-process-words", "2.9-prose", f"{PAGE} learner prose", "PASS",
    f"Scan for builder, verifier, round, ruling, architect, fixer, coordinator, agent, TODO, placeholder: 0 hits except "
    f"'Round once, at print time' (:68 and :177, a rounding instruction). {S}/out/scan_r19.out")
row("proj-links-anchors", "2.9-structure", f"{PAGE} (href and id); course/modules/LX/LX1/index.html; L02.html",
    "PASS", "37 ids; no internal href without a target; no relative href whose file is missing "
    f"({S}/out/scan_r19.out). Concept link data-concept=debt-deflation -> L02.html#def-debt-deflation exists (L02.html:110).")
row("proj-page-smoke", "2.9-structure", f"{PAGE}", "PASS",
    f"page_smoke --unit LX1 --pages project: PASS (labs 1-3 timed under 0.1 s; no console errors; no external requests). "
    f"{S}/out/page_smoke_project.out")
carried("proj-atlas-autograder-na", "2.6-grading", "curriculum/06-profession-capstone.yaml:49; course/modules/LX/LX1/ (no grader/ directory)",
        "curriculum line 49 'grading: rubric' and the module directory (no grader/ or atlas entry) are byte-identical since the previous "
        "pin; mutate_graders --unit LX1 --seeds 0-9 rc 0 with no grader to run (ledgers/LX1/scripts/LX1-c-r19/out/mutate_graders_LX1_r19.out).")
row("proj-mutants-student-errors", "2.6-mutation (lab analogue; LX1 has no grader)", "ledgers/LX1/mutants/ (82 files); "
    f"{S}/out/kill_all_r19.out; {S}/out/kill_r19_new.out", "PASS",
    "All 82 lab mutants are killed. Of the 79 existing mutants, 74 are killed on the shipped run (kill_all_r19.out); the other "
    "5 survivors of the shipped run are killed by distinguishing inputs: r18n02 (rounding seeds, out/lab3_synth_rerun_r19.out), r18n03 "
    "(tiny_moves, drift seeds), r18n04 (rounding_seed8 and others), r18n05 (mid-series blank accepted, rc 0, while the page's "
    "Check paragraph says a blank raises ValueError: out/blank_cell_survivors_r19.out), r17n01 (first-row blank raises "
    "ZeroDivisionError, not the ValueError the Check paragraph states: out/blank_first_row_survivors_r19.out). Three new "
    "student-error mutants (r19n01 truncated dispersion, r19n02 largest change taken as last change, r19n03 window-two "
    "population sd) are killed: r19n01 by the 2.46 line, r19n02 by -2.11 (2026-09), r19n03 by the difference line 0.33 vs 0.32.",
    )
row("proj-alternatives", "2.6-mutation (over-constraint)", f"{S}/alts/alt_r19_A_lab2_float_negated_burden.py; "
    f"{S}/alts/alt_r19_B_lab3_statistics_slices.py; ledgers/LX1/scripts/LX1-c-r18/alts/*.py", "PASS",
    "Four alternative correct implementations pass the shipped checks (out/alts_r19.out, out/alts_r18_rerun_r19.out): Lab 2 with float "
    "division and -100(1 - start/end); Lab 3 with statistics.stdev, slice windows and format(); the round-18 Decimal Lab 1 and "
    "statistics Lab 3 versions. No over-constraint found.")
carried("proj-exemplar-b-annotations-vs-descriptors", "2.6-rubric", f"{PAGE}:548-606 (exemplar B annotations)",
        "exemplar B block lines 547-610 is byte-identical since the previous pin (no hunk there); re-read this round: each "
        "annotation matches the descriptor it names (C3 L2 at least three uncited, C4 L2 rounds an input).")
row("proj-brief-rubric-escape-clauses", "2.6-rubric", f"{PAGE}:442, :474, :475", "PASS",
    "No escape clause makes a descriptor unreachable: the L2 C2 bubble clause (:474) is reachable by an essay that calls a "
    "price move a bubble without a benchmark; the highest-level rule (:467) resolves overlaps.")
row("proj-exemplar-locators", "2.1-citation", f"{PAGE}:490, :500, :511, :522, :534; course/modules/LX/LX1/L02.html; L04.html:333",
    "PASS", "Exemplar locators checked: title field of Eichengreen (registry title contains 1919-1939); MANIFEST last field; "
    "Lab 3 window and difference lines; Proposition 2.1(a) and Remark 3.3 (L02.html:84-90, :127-129); Lab 1 Part A; Lesson 4 "
    "Section 4 item 'Exchange rates only' (L04.html:333, under the Section 4 header at :329).")
row("proj-exemplar-a-c5-limit-count", "2.6-rubric", f"{PAGE}:476-477, :534, :539-540", "PASS",
    "Exemplar A names three limits; only limit one names a test (an interest-rate series). Limit two states it is not a test "
    "(:535). C5 level 3 is the highest met, as the calibration confirms.")
row("proj-round11-delta-project-page", "2.9-prose / delta", f"{PAGE}:62, :475, :534 (delta-touched lines)", "PASS",
    "The round-19 delta touched :311-314, :467, :474, :502, :506, :524, :535 (git diff -U0 505592668894 cd4dd7df, 7 hunks, all read). "
    "Lines :62 and :475 are unchanged; :534 and :535 read in full (exemplar A limits).")
row("proj-spec-limits-test-each", "2.6-spec", f"{PAGE}:269, :443, :476-477, :534", "PASS",
    "Brief (:443) and Required outputs (:269) ask for two limits and the test for at least one; C5 L4 requires a test for each "
    "limit. Consistent with the cells and exemplar A (C5 3).")
row("proj-notation-n-undefined", "2.9-prose / notation", f"{PAGE}:60, :431; tests/labs/LX1/lab-LX1-project-3.py:305",
    "PASS", "n (count of changes in the window) is used in 'denominator n - 1' (:60, :305) without an explicit definition on the page. "
    "n is not a registered symbol, so no registry collision (BUILDER_RULES §3 allows local letters). Judgment, not a FAIL: the "
    "reader can read n as the change count; a 'where n is the number of changes' clause would remove the doubt (see notes).")
row("proj-spec-window-start-must", "2.6-spec", f"{PAGE}:62, :431; tests/labs/LX1/lab-LX1-project-3.py (WINDOW_TWO_FROM)",
    "PASS", "Window two start 2000-01 (first change uses 1999-12) matches the lab constant and the 321 count; the lab computes no other start.")
row("proj-rubric-c2-gap", "2.6-rubric", f"{PAGE}:474 (C2 L2 cell, clause for 'does not name what some step rests on')", "PASS",
    "C2 L2 includes 'does not name what some step rests on' and 'names no failure step' and 'fewer than three steps'; "
    "a complete chain with an unevidenced failure step reaches L3, and the gap clause is reachable.")
row("proj-rubric-c3-level3-gap", "2.6-rubric", f"{PAGE}:475 (C3 L3 cell)", "PASS",
    "C3 L3 requires every claim cited or inference, at most two without a locator, and counter-evidence for B or C claims; "
    "an essay with one uncited claim falls to L2 (at most two uncited), so the level is reachable and ordered.")
row("proj-dag-concepts", "2.9-DAG", f"{PAGE}; course/modules/LX/LX1/L02.html:110; course/modules/LX/LX1/L01.html:65",
    "PASS", "check_dag --unit LX1 PASS and --all PASS. The only concept link (debt-deflation) targets an L02 definition (L02.html:110). "
    "Fundamental value (Lesson 1 Definition 1.2, dfn id def-fundamental-value at L01.html) is named in prose at :474.")
row("proj-exemplar-A-limit1-cip-locator", "2.1-citation", f"{PAGE}:534; course/modules/LX/LX1/L04.html:333", "PASS",
    "Limit one cites Lesson 4 Section 4 item 'Exchange rates only' (L04.html:333), and L04 says the lab cannot test an "
    "interest-rate relation, which matches.")
row("proj-rubric-c3-inference-gap", "2.6-rubric", f"{PAGE}:474-475, :440", "PASS",
    "C3 L4 accepts 'marked as the writer's own inference' (:475), so an essay with an unsourced claim marked as inference "
    "still reaches L4; the brief (:443) requires the marking. Consistent.")
carried("proj-l04-model-name-stale", "2.9-prose", f"{PAGE}:431; course/modules/LX/LX1/L04.html:84-85",
        "L04.html (not in the round-19 delta) and project.html:431 'fixed-exchange-rate model of Lesson 4 (Definition 2.1)'; "
        "L04.html:84 is titled 'Definition 2.1 (fixed-exchange-rate model)'. The name matches.")
row("proj-exemplar-a-c2-annotation", "2.6-rubric", f"{PAGE}:500-520; course/modules/LX/LX1/L02.html (Definition, Proposition 2.1(a), Remark 3.3)",
    "PASS", "The exemplar A chain for the episode cites Lab 1 Part A, Proposition 2.1(a) (under (A2),(A3)) and Remark 3.3; each "
    "is at the stated locator. Annotation at :506 matches the chain.")
carried("proj-r14-delta-hunks", "2.9-prose / history", "git merge-base --is-ancestor 8e5751c9 50559266 and d1e65a0 50559266",
        "history check re-run this round: 505592668894 (round-18 pin) and 56cc575a are ancestors of cd4dd7df; the round-14 and "
        "round-15 hunks are inside that history.")
carried("proj-r15-delta-hunks", "2.9-prose / history", "git merge-base --is-ancestor d1e65a0 50559266 and 56cc575a 50559266",
        "history check re-run this round: 56cc575a is an ancestor of cd4dd7df.")
row("proj-rubric-exhaustive-r14", "2.6-rubric (exhaustive)", f"{PAGE}:474 (C2 L2 cell, new bubble clause)", "PASS",
    "Round-18 gap closed: the L2 cell now includes 'gives a chain of at least three steps for each, each step naming what it "
    "rests on, names the steps at which the analogy holds and the first step at which it fails, and calls a price move a bubble "
    "without naming the benchmark'. Scoring model (rubric_coverage_r19.py): the bubble essay with the old cell scores 0 when "
    "no similarity or difference is listed (c2_old), and 2 with the new cell (out/rubric_coverage_r19.out). Every consistent C2 "
    "feature combination scores 0 only when it has no chain and no similarity (36 combinations, 0 with a chain or similarity).")
row("proj-student-error-coverage", "2.6-rubric (student-error analogue)", f"{PAGE}:473 (C1 L3 cell), :472-477; plans/LX1-build-plan.md §5.4",
    "FAIL",
    "Scoring model, exemplar A essay (C1 4, C2 4, C3 4, C4 4) with one defect per pattern. Scores after the defect: pattern 1 C4 2, "
    "pattern 2 C4 2, pattern 3 C2 2, pattern 4 C3 2, pattern 5 C2 2, pattern 6 C4 2, pattern 7 C3 2, pattern 8 C3 2, pattern 10 C1 3. "
    "Pattern 10 (an episode date stated with no locator, condition locator "
    "present) scores C1 = 3 because the C1 L3 cell reads 'gives a locator for all but one date' (:473, td 2). The plan's own L3 "
    "(§5.4 item 1) reads 'names both with dates and one locator each', and its L2 reads 'a date or a locator is missing for one'. "
    "Under the plan, pattern 10 is L2, below the bar (3); under the page it meets the bar. Pattern 9 is a lab check, caught by "
    "run_labs (completion whole-block compare). Output: rubric_coverage_r19.out.",
    "At :473 td 2 change 'gives a locator for all but one date' to 'gives a locator for each date' (the plan's wording, §5.4 "
    "item 1). The exemplars are unaffected: exemplar A is C1 4 and exemplar B is C1 2.")
row("proj-data-embedded-claim", "2.8-data", f"{PAGE}:280; course/assets/data/market/MANIFEST.json (fx_daily, fx_monthly, ust_daily)",
    "PASS", "MANIFEST lists exactly three embedded series; the page names all three ids, and the fx_monthly sha256 matches (see "
    "proj-data-snapshot-rebuild).")
row("proj-lab3-raise-claims-untested", "2.5-labs", f"{PAGE}:308-309 (Check paragraph), :431 (no agreement line); tests/labs/LX1/lab-LX1-project-3.py",
    "PASS", "The Check paragraph claims are tested: blank, non-decimal and gap inputs raise ValueError (gap_and_text_r19.py). "
    "The page prints no agreement line, and the lab computes none (grep: no 'agree' in the twin or the page's Lab 3 text).")
carried("proj-rubric-c5-count-wording", "2.6-rubric", f"{PAGE}:477 (C5 cells)",
        "C5 row (line 477 now, 476 in the previous pin) is byte-identical in content; the cells read 'at least two limits' (L4), "
        "'two limits, one with the test' (L3), 'at least one limit' (L2), 'caveat without naming what it limits' (L1).")
carried("proj-rubric-c4-formula-gap", "2.6-rubric", f"{PAGE}:476 (C4 cells)",
        "C4 row (line 476) is byte-identical since the previous pin; L2 clause 3 omits formula or base and sign, L3 requires them.")
row("proj-rubric-c2-count-wording", "2.6-rubric", f"{PAGE}:474 (C2 L2 cell first clause)", "PASS",
    "The first L2 clause 'lists similarities and at least one difference' is a count the rater can check. The plural 'similarities' "
    "is read as at least one similarity, the L1 wording is 'at least one similarity' (:474 td 4); see notes.")
row("proj-r18-delta-hunks", "2.9-prose / delta", f"git diff -U0 700bf33f 50559266 -- {PAGE} (the previous round's delta)", "PASS",
    "History re-checked: 700bf33f (round-16 pin), 50559266 (= 505592668894, the round-18 pin and this round's base) and "
    "9294b914 are ancestors of cd4dd7df (git merge-base --is-ancestor). The previous round's delta (700bf33f..50559266) was "
    "read in round 18 and is not re-read here; this round's delta starts at 505592668894.")
row("proj-lab3-blank-gap-inputs", "2.5-labs", "tests/labs/LX1/lab-LX1-project-3.py; " + f"{S}/out/gap_and_text_r19.out; {S}/out/blank_first_row_survivors_r19.out",
    "PASS", "Blank GBP cell mid-series (1985-03) raises ValueError on the twin; a blank in the first row (1971-01) raises ValueError on "
    "the twin; the two blank-accepting survivors are distinguished (out/blank_cell_survivors_r19.out, out/blank_first_row_survivors_r19.out).")

# ---- delta, new rows ----
row("proj-r19-delta-hunks", "2.9-prose / delta", f"{PAGE} (git diff -U0 505592668894 cd4dd7df: 7 hunks); tests/labs/LX1/lab-LX1-project-3.py (docstring)",
    "PASS", "All seven hunks read: :311-314 (rounding text; code matches: counts printed as is, decimals half up from unrounded "
    "values), :467 (highest-level rule with 'does not lower that score'), :474 (new bubble clause, FAIL-to-PASS for the r14 row), "
    ":502 and :506 (exemplar A step 2 now cites Lab 1 Part A, a SIMULATED path; prices 1.00 to 0.85 match Lab 1), :524 (ratio "
    "rounded from unrounded values; prints 0.88 matching Lab 3), :535 (limit two no longer claims a test). The Lab 3 docstring "
    "hunk equals page :311-314 (run_labs page-vs-twin diffs=0). tests/labs/LX1/lab-LX1-L01-1.py is not in this slice.")
row("proj-check-pages-project-scope", "2.9-structure", f"tools/check_pages.py:25; {S}/out/check_pages_project_r19.out", "PASS",
    "check_pages --unit LX1 PASS (unit-wide, the gate form). check_pages --unit LX1 --page project exits 1 with lesson-template "
    "problems (11, e.g. 'missing section why-it-matters'); check_pages.py:25 says project pages are checked by check_projects.py, "
    "so the per-page form is a tool-scope note, not a page defect. check_projects --unit LX1 PASS.")
row("proj-lab3-r19-mutants", "2.5-labs (student-error mutants, own)", f"ledgers/LX1/mutants/r19n01..r19n03; {S}/out/kill_r19_new.out",
    "PASS", "Three new student-error mutants written from the project twin, each with a docstring first line naming the error, "
    "all killed (r19n01 2.46 vs 2.47, r19n02 -2.11 (2026-09) as largest, r19n03 difference 0.33 vs 0.32).")

ids = [r["id"] for r in R]
dups = sorted({i for i in ids if ids.count(i) > 1})
if dups:
    raise SystemExit(f"duplicate ids {dups}")
prev = json.loads(pathlib.Path("/Users/billyribeiro/.fanout/frags/E-LX1-c.round18.json").read_text(encoding="utf-8"))
missing_prev = [x["id"] for x in prev["rows"] if x["id"] not in ids]
if missing_prev:
    raise SystemExit(f"round-18 ids dropped: {missing_prev}")

# ---- mutants ----
kills = {}
for f in (OUT / "kill_all_r19.out", OUT / "kill_r19_new.out"):
    for line in f.read_text(encoding="utf-8").splitlines():
        m = re.match(r"(KILLED|SURVIVED) \| (\S+) \| (.*)", line)
        if m:
            kills[m.group(2)] = (m.group(1), m.group(3))
distinguished_by = {
    "lx1c_r18n02_": f"{S}/out/lab3_synth_rerun_r19.out (rounding seeds, e.g. rounding_seed11)",
    "lx1c_r18n03_": f"{S}/out/lab3_synth_rerun_r19.out (tiny_moves, drift2000_sig)",
    "lx1c_r18n04_": f"{S}/out/lab3_synth_rerun_r19.out (rounding_seed8)",
    "lx1c_r18n05_": f"{S}/out/blank_cell_survivors_r19.out (mid-series blank accepted, rc 0; claim says ValueError)",
    "r17n01_": f"{S}/out/blank_first_row_survivors_r19.out (first-row blank raises ZeroDivisionError, claim says ValueError)",
}
mutants = []
for path in sorted((ROOT / "ledgers/LX1/mutants").glob("*.py")):
    name = path.name
    doc = path.read_text(encoding="utf-8").split('"""', 2)[1].strip().splitlines()[0]
    status, reason = kills.get(name, (None, None))
    if status == "KILLED":
        killed_by = f"lab-LX1-project-3 or -2 expected block (harness cands; {S}/out/kill_all_r19.out): {reason}"
        if name.startswith("r19n"):
            killed_by = f"{S}/out/kill_r19_new.out: {reason}"
    elif status == "SURVIVED":
        key = next(k for k in distinguished_by if name.startswith(k))
        killed_by = "distinguishing input: " + distinguished_by[key]
    else:
        raise SystemExit(f"no kill record for {name}")
    mutants.append({"name": name, "description": doc, "killed_by": killed_by})

fail = [r for r in R if r["status"] != "PASS"]
counts = {s: sum(1 for r in R if r["status"] == s) for s in ("PASS", "FAIL", "UNVERIFIABLE")}
notes = [
    "Scope: course/modules/LX/LX1/project.html and tests/labs/LX1/lab-LX1-project-{1,2,3}.py, delta 505592668894..cd4dd7df (round-18 pin).",
    "The highest-level scoring rule is at project.html:467 (the prompt said line 465, which is the section opener).",
    "Judgment, not a FAIL: 'Lists similarities' (C2 L2, :474) is plural; L1 says 'at least one similarity'. A 1-similarity, 1-difference essay "
    "scores 2 under the at-least-one reading and 1 under the plural reading. Suggested wording: 'at least one similarity and at least one difference'.",
    "Judgment, not a FAIL: symbol n (window change count) is used at :60 and :305 without a definition on the page; not a registered symbol.",
    "Check_pages --page project is a tool-scope note (proj-check-pages-project-scope).",
    "Blind calibration: ~/.fanout/blind/LX1-c.json (A 4,4,4,4,3; B 2,2,1,2,1) equals the official scores at :485 and :547.",
    "Not checked: a repository-wide pytest run (only the labs, page smoke, checks and refs suites); 'two printed pages' length (no tool; "
    "rubric judges content); hours were checked by arithmetic only (ruling); exemplar scores beyond the blind file.",
    "Two student essays were not written (rubric-only unit): the student-error analogue uses the scoring model on feature vectors "
    "derived from the exemplar A essay, and the model's cell predicates are transcriptions of :473-477 (reviewable in rubric_coverage_r19.py).",
]
frag = {
    "unit": "LX1",
    "slice": "LX1-c",
    "round": 19,
    "verifier": "Claude Haiku 5.5 (claude-haiku-5-5), independent verifier for LX1-c, round 19 (did not build LX1)",
    "pin": "cd4dd7dfc2bbe0fc16b672329daa408d1d8a268b",
    "base": "505592668894eff518befad086df192000dc86c0 (round-18 pin; the round-18 fragment is /Users/billyribeiro/.fanout/frags/E-LX1-c.round18.json)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE19-LX1-c",
    "scratch": f"{S}/ (scripts and out/); scratch copies under /tmp were removed after each run",
    "verified_at": "2026-11-09T06:30:00Z",
    "verdict": "FAIL" if fail else "PASS",
    "rows": R,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": notes,
    "summary": (f"LX1-c round 19 on cd4dd7d: verdict {'FAIL' if fail else 'PASS'}. {len(R)} rows: {counts['PASS']} PASS, "
                f"{counts['FAIL']} FAIL, {counts['UNVERIFIABLE']} UNVERIFIABLE. Non-PASS: "
                + ", ".join(r["id"] for r in fail) + f". Mutants: {len(mutants)} lab mutants, all killed "
                "(74 on the shipped run; 5 by distinguishing inputs; 3 new student-error mutants killed on the shipped run). "
                "Alternatives: 4 pass."),
}
dest = ROOT / "ledgers/LX1/LX1-c.json"
dest.write_text(json.dumps(frag, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", dest, counts, "mutants", len(mutants))
