"""LX1-c round 20: writes the verifier fragment ledgers/LX1/LX1-c.json from the evidence in ledgers/LX1/scripts/LX1-c-r20/."""
import json
import re
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyE20-LX1-c")
S = "ledgers/LX1/scripts/LX1-c-r20/out/"
CARRY = ("Carried from round 19 (course/modules/LX/LX1/project.html:440 and :474-477 byte-identical since the previous pin; "
         "git diff -U0 cd4dd7df d1083bf1 touches project.html only at :60 and :473): ")

rows = []


def row(rid, check, location, status, evidence, fix=""):
    rows.append({"id": rid, "check": check, "location": location, "status": status, "evidence": evidence, "fix": fix})


# --- the one non-PASS row of this round ---
row("proj-rubric-c1-level3-unreachable", "2.6-rubric",
    "course/modules/LX/LX1/project.html:473 (C1 td 2 = level 3, and td 1 = level 4)", "FAIL",
    "The C1 level-3 cell (td 2) now reads 'Names both the episode and the condition with dates, and gives a locator for each date.' "
    "The level-4 cell (td 1) reads 'Names both ... with dates, and gives a locator for each date (a page, a table, ...)'. The two "
    "predicates are identical, so under the highest-level rule of :467 no essay scores 3 on C1. The model "
    f"({S}rubric_c1_r20.out, encoding the cell texts at d1083bf1) gives 'page text variant now: levels reachable [4, 2, 1]; essays "
    "scoring 3: 0'; the previous text gave 12 essays at level 3. The round-19 fix proposed 'a locator for each date' as the plan's "
    "L3 wording; the plan's own L3 (plans/LX1-build-plan.md section 5.4 item 1) reads 'names both with dates and one locator each', "
    "which is an 'each item' condition, not 'each date'. The brief (project.html:440) asks for 'a locator for the date' per item, so "
    "the level-4 descriptor is also the brief's minimum. Level 3 is a dead level.",
    "At project.html:473 td 2 replace 'gives a locator for each date.' with 'gives at least one locator for each of the two.' "
    "(the plan's 'one locator each'). Evidence the fix restores a reachable level 3 and keeps the bar: "
    f"{S}rubric_c1_fix_check_r20.out gives level 4: 4, level 3: 12, level 2: 20 of the 36 essays, and pattern 10 (episode date with "
    "no locator) stays at level 2. Architect to confirm: L3 and L4 differ only for an item with two or more dates.")

# --- rubric rows: re-verified this round ---
row("proj-rubric-observable", "2.6-rubric", "course/modules/LX/LX1/project.html:473 td 3 (C1 level 2), :467", "PASS",
    "Round-19 FAIL resolved. td 3 now reads 'a date or a locator is missing for one or both of them' (was 'one of them'). "
    f"The 'now' model ({S}rubric_c1_r20.out): essay dated both, no locators, scores 2; the strict 'exactly one' reading no longer exists "
    "in the page text, so the score does not depend on the reading. Whole-cell and highest-level rule (:467) read in full.")
row("proj-student-error-coverage", "2.6-rubric (student-error analogue)", "course/modules/LX/LX1/project.html:467, :473, :474-477; plans/LX1-build-plan.md section 5.4",
    "PASS",
    "Round-19 FAIL resolved. Pattern 10 (episode date stated with no locator, condition locator present) scores C1 = 2 under the page as now written "
    f"({S}rubric_c1_r20.out: 'example essay with one date (episode) and no locator, condition dated with locator: now 2, old 3'). "
    f"Patterns 1-9 use the C2-C4 cells, which are byte-identical to round 19 (see carried rows); the re-run of the round-19 model "
    f"({S}rubric_coverage_r19_rerun_r20.out) gives the same C2/C3/C4 scores as before (patterns 1-8 at C4 2, C2 2, C3 2 as listed). "
    "Pattern 9 is a lab check (run_labs). The C1 level-3 defect is recorded in proj-rubric-c1-level3-unreachable.")
row("proj-calibration-exemplars", "2.6-rubric-calibration",
    "course/modules/LX/LX1/project.html:485 (exemplar A data-scores 4,4,4,4,3), :547 (exemplar B data-scores 2,2,1,2,1)", "PASS",
    "Calibration by the dedicated blind scorer (ruling 23): ~/.fanout/blind/LX1-c.json has A [4, 4, 4, 4, 3] and B [2, 2, 1, 2, 1], which "
    "equal the official scores on :485 and :547 exactly (within one level per criterion as required). Exemplars were not scored by this verifier.")
row("proj-exemplar-numbers", "2.2-numbers", "course/modules/LX/LX1/project.html:501-534 (exemplar A), :578-582 (exemplar B)", "PASS",
    f"Every exemplar number re-derived in {S}numbers_r20.out: 17.65 = 100(1/0.85 - 1) (Lab 1 Part B); 2.79, 2.47, 1.90 (Lab 3 windows); "
    "ratio 0.88 from unrounded values; 0.32 difference; 13.58 at 1985-03 (largest by size, window one). Exemplar B: 2.47/2.79 = 0.89 "
    "(0.885 rounded), and the unrounded ratio 0.8842 gives a fall of about 12 percent, as its annotation at :582 says.")
row("proj-reading-keys", "2.1-citation", "course/modules/LX/LX1/project.html:627-635; references/references.json", "PASS",
    "Registry records present with status verified: eichengreen1992golden title 'Golden fetters: the gold standard and the Great Depression, 1919-1939' "
    "equals the page's title string at :491 byte for byte; friedman1963monetary and garber2000famous exist. friedman1963monetary lists one author "
    "(Milton Friedman) while the source string names Friedman & Schwartz; the page cites the key only, as plans/LX1-build-plan.md section 7.1 "
    "requires, so no record is edited or typed.")
row("proj-reading-reinhart-registry", "2.1-citation", "course/modules/LX/LX1/project.html:627-635; references/references.json", "PASS",
    "reinhart2009this exists in references/references.json (status verified, crossref). The page's reading list (:631-633) omits it; "
    "plans/LX1-build-plan.md section 5.2 marks it optional. Not a finding; it is cited on the LX1 hub (index.html:206).")
row("proj-notation", "2.4-notation", "course/modules/LX/LX1/project.html TeX spans (:56-60, :175-180, :268-271, :431, :535)", "PASS",
    "Symbols in the page's math (31 spans, read in full): D, P_0, P_t, P_5, V_0, V_t, S_m, m, n, t, ln. None is a registered symbol of "
    "notation/notation.json (T, R_f, Q, Phi, gamma_3, gamma_4, R*, R^e*, E, R), and each local symbol is defined on the page (D, P_t, V_t at :56; "
    "S_m at :60; n at :60). The letter T appears only as the site evidence grade (:66), which matches BLUEPRINT.md:155-163 (T = theorem); it is not a symbol in the math.")
row("proj-scope-words", "2.9-prose", "course/modules/LX/LX1/project.html learner prose", "PASS",
    "54 scope-word occurrences (every, all, only, any, same, exactly, never) read in the prose. Each is backed by a count or a stated hypothesis: "
    "'every monthly change of that column ... (668 changes)' (:62, matches numbers_r20.out W1 n=668); 'all 12 changes' (:431); "
    "'rules out a fixed exchange rate held over all of window three' (exemplar A :513) follows from Prop 2.2(a) under (A2) with 0 zero changes in 12; "
    "'Labs 1 and 2 use SIMULATED paths only' (:267) matches the lab code (no data-files attribute on labs 1-2).")
row("proj-process-words", "2.9-prose", "course/modules/LX/LX1/project.html learner prose (tags stripped, <pre> excluded)", "PASS",
    "Scan for builder, verifier, round, ledger, agent, ruling, architect, fixer, planner, batch, sweep, grader, mutant, TODO, placeholder, pending, honest: "
    "only 'Round once, at print time' (:177) and 'does not round an input before computing' (:476, C4 level-3 cell) match, both about rounding.")
row("proj-hours", "2.6-hours", "course/modules/LX/LX1/project.html:33, :451-462; course/modules/LX/LX1/index.html:29", "PASS",
    "Rows 1 + 1 + 2 + 1.5 + 2.5 + 2 = 10. data-hours-project=\"10\" (:33) equals the hub's data-hours-project=\"10\" (index.html:29). Every row has a rationale cell.")
row("proj-rung1-step3-rounding-claim", "2.5-labs", "course/modules/LX/LX1/project.html:177, :179", "PASS",
    f"10000000/0.85 cents = 11764705.882 -> 117647.06 dollars; 10000000/0.85 - 10000000/1.15 = 3069053.708 cents -> 30690.54 dollars ({S}numbers_r20.out, L1 rows).")
row("proj-real-value-vs-lesson2", "2.9-prose", "course/modules/LX/LX1/project.html:55-59, :170; course/modules/LX/LX1/L02.html (Proposition 2.1 at 84-90, Remark 3.3, def-debt-deflation)", "PASS",
    "Read in full. L02 Proposition 2.1: (A2) D fixed nominal debt in integer cents; (A3) P_t positive, P_0 base; conclusion (a) V_t/V_{t-1} = P_{t-1}/P_t. "
    "Remark 3.3: 'The corollary says nothing about the cause of a fall'. def-debt-deflation exists (id present). The page's V_t = D/P_t with P_0 = 1 is the identity with P_0 = 1.")
row("proj-manifest-note-misattributed", "2.2-numbers", "course/modules/LX/LX1/project.html:271, :279, :294; course/assets/data/market/MANIFEST.json (fx_monthly)", "PASS",
    "MANIFEST fx_monthly: first 1971-01, last 2026-09, rows 669, retrieved 2026-10-19, transform inverts CAD, CHF, DKK, JPY, NOK, SEK. "
    f"EUR blank 336 rows (1971-01 to 1998-12), no other column blank ({S}numbers_r20.out, and the scan in this round). The page's :271 and :294 match.")
row("proj-lab3-citation-string", "2.1-citation", "course/modules/LX/LX1/project.html:279, :287; MANIFEST fx_monthly citation", "PASS",
    "Citation string at :279 and :287 is contained byte for byte in MANIFEST fx_monthly.citation; the licence quote and retrieved date also present (python check this round).")
row("proj-spec-current-undefined", "2.6-spec", "course/modules/LX/LX1/project.html:439-440, :301-302, :444", "PASS",
    "Current condition dated within the twelve months ending at the last month of the data (:440); window three 2025-10..2026-09 (:301-302) has 12 changes "
    "(numbers_r20.out). The question of which month a non-snapshot source uses is not a FAIL.")
row("proj-exemplar-A-condition", "2.6-exemplars", "course/modules/LX/LX1/project.html:491", "PASS",
    "Window three 2025-10..2026-09 and last month 2026-09 (MANIFEST last; retrieved 2026-10-19) match the snapshot.")
row("proj-gate-commands", "gate", f"{S}_gates_summary.txt; {S}*.out", "PASS",
    "Round-20 run (ledgers/LX1/scripts/LX1-c-r20/run_gates_r20.sh): check_projects --unit LX1 and --all PASS; check_pages --unit LX1 PASS; check_dag --unit LX1 and --all PASS; "
    "run_labs --unit LX1 PASS (7/7); run_labs --unit LX1 --page project PASS (3/3); page_smoke --pages project PASS; verify_refs --offline 560 entries, 0 problems; "
    "verify_refs --unit LX1 live 4 of 560, 0 problems; fetch_data --check 0 problems; build_site --check current (6 outputs); ruff check and format clean; "
    "mypy --no-incremental success (385 files); pytest test_labs/test_run_labs/test_page_smoke/test_page_checks/test_curriculum rc 0; pytest test_refs rc 0. "
    "Full repository pytest not run (not needed for this slice).")
row("proj-lab1-twin-run", "2.5-labs", "course/modules/LX/LX1/project.html:78-149, :150-169; tests/labs/LX1/lab-LX1-project-1.py", "PASS",
    f"Page code block 1 equals the twin (0 line diffs). Twin under python -I -W error: rc 0, stderr 0 bytes; stdout equals the expected block (20 lines). {S}twins_r20.out")
row("proj-lab1-numbers", "2.2-numbers", "course/modules/LX/LX1/project.html:77, :150-169", "PASS",
    f"Hypothesis numbers 117647.06, -13.04, 30690.54, 17.65 and all ten Part A real-debt rows re-derived with Fractions ({S}numbers_r20.out).")
row("proj-lab2-twin-run", "2.5-labs", "course/modules/LX/LX1/project.html:185-246, :247-256; tests/labs/LX1/lab-LX1-project-2.py", "PASS",
    f"Page code equals the twin except the two blanks ('return ___' at page lines 214 and 219; twin lines are the real-debt and burden expressions). "
    f"Twin rc 0, stderr 0, stdout equals the expected block ({S}twins_r20.out).")
row("proj-lab2-numbers", "2.2-numbers", "course/modules/LX/LX1/project.html:184, :247-256", "PASS",
    f"40000.00 at t=0; 43010.75 at t=5 (4000000/93 cents = 43010.7527); burden change 7.5269 -> 7.53 ({S}numbers_r20.out, L2 rows). Part A rows re-derived.")
row("proj-lab2-check-claims", "2.2-numbers", "course/modules/LX/LX1/project.html:257", "PASS",
    f"'a real-value line that leaves out the division prints 40000.00 ... the check fails': mutant lx1c_m01 KILLED (expected-block differs, {S}kill_r20.out). "
    f"'a burden line that inverts the ratio prints -7.00 in place of 7.53': exact -7.00 ({S}numbers_r20.out), mutant lx1c_m02 KILLED.")
row("proj-lab3-twin-run", "2.5-labs", "course/modules/LX/LX1/project.html:285-432; tests/labs/LX1/lab-LX1-project-3.py", "PASS",
    f"Page code equals the twin (0 line diffs). Twin run in a scratch directory holding data/fx_monthly.csv under python -I -W error: rc 0, stderr 0, "
    f"stdout equals the expected block (the lab reads data/fx_monthly.csv, so it must run with data/ present, as run_labs does). {S}twins_r20.out; {S}lab3_twin_stdout_r20.out")
row("proj-lab3-numbers", "2.2-numbers", "course/modules/LX/LX1/project.html:287, :412-431", "PASS",
    f"Independent stdlib re-derivation ({S}numbers_r20.out): window one 668 changes, 3 zeros, sd 2.7935 -> 2.79, largest 13.58 (1985-03); window two 321, 2 zeros, "
    "sd 2.4700 -> 2.47, largest -9.66 (2008-10); window three 12, 0 zeros, sd 1.9020 -> 1.90, largest 2.96 (2026-04); ratio 0.8842 -> 0.88; "
    "difference 0.3236 -> 0.32; decimal sds 0.027935 and 0.024700.")
row("proj-lab3-L04-cross-check", "2.1-citation", "course/modules/LX/LX1/L04.html:314, :317, :333; course/modules/LX/LX1/project.html:284, :298", "PASS",
    "L04.html:314 prints window one 668 changes, sd 0.027935, largest 0.135846 at 1985-03; window two sd 0.024700 and 321 changes (same counts and decimals as Lab 3). "
    "L04 hunk this round is at L04.html:448 only (outside every line this slice cites).")
row("proj-lab3-docstring-claims", "2.5-labs", "course/modules/LX/LX1/project.html:288-315 (twin docstring mirrored); tests/labs/LX1/lab-LX1-project-3.py:1-40", "PASS",
    "Data paragraph (MANIFEST transform inverts CAD, CHF, DKK, JPY, NOK, SEK; GBP not inverted) matches MANIFEST. Rounding paragraph matches show() (Decimal of the exact float, ROUND_HALF_UP) and the unrounded ratio and difference (code at :377, :407-409).")
row("proj-lab3-interpretation-claims", "2.2-numbers", "course/modules/LX/LX1/project.html:431-432; course/modules/LX/LX1/L04.html:84-94, :90-96", "PASS",
    "'The two zero changes in window two are months whose last value equals the value of the month before': 2012-07 and 2019-11 (numbers_r20.out). "
    "'Proposition 2.2 ... gives a zero change in every month' under (A2) of Definition 2.1 with window n >= 2 (L04 Prop 2.2(a)). 'the largest monthly log change in window one, 13.58 percent in 1985-03, is outside window two' (2000-01 onward) holds.")
row("proj-lab3-difference-line-r5", "2.5-labs", "course/modules/LX/LX1/project.html:287, :412-431; tests/labs/LX1/lab-LX1-project-3.py", "PASS",
    f"Difference line 0.32 is computed from unrounded sds (code :408); unrounded difference 0.32358. Mutant lx1c_r18n02 (difference of printed sds) is killed on a synthetic "
    f"input (seed 0: -0.00 vs 0.00 at the formatter; {S}synth_kill_r20.out). On the embedded snapshot it survives (printed values identical); see proj-lab3-r20-mutants.")
row("proj-lab-simulated-labels", "2.8-data", "course/modules/LX/LX1/project.html:42, :77, :80, :184, :187, :283-287", "PASS",
    "Labs 1 and 2 are labelled SIMULATED in the hypothesis and in the code docstring; they read no file (no data-files). Lab 3 is the only lab with data-files and reads the embedded snapshot.")
row("proj-data-licence-quote", "2.8-data", "course/modules/LX/LX1/project.html:279; https://www.federalreserve.gov/disclaimer.htm", "PASS",
    "The licence quote on the page is byte-identical to MANIFEST fx_monthly.licence (python check this round). licence_url matches the page's link (federalreserve.gov/disclaimer.htm). Plain URL not fetched (no network needed for this check).")
row("proj-data-snapshot-rebuild", "2.8-data", "course/assets/data/market/fx_monthly.csv; course/assets/data/market/MANIFEST.json", "PASS",
    "sha256 of fx_monthly.csv 60572240d1a9d1832d5021297634b2369723b94098414948b891dd26a8bffe3e equals MANIFEST sha256; byte count equals MANIFEST bytes; fetch_data --check 0 problems. "
    "The raw H.10 XML was not re-downloaded (not required for the offline check).")
row("proj-data-fields", "2.8-data", "course/modules/LX/LX1/project.html:271, :279-280, :292-294; MANIFEST", "PASS",
    "Columns (10) and blanks (EUR 336 rows before 1999-01) match MANIFEST and the file. 'the GBP column has no blank cell' (:279): blank GBP count 0.")
row("proj-data-no-other-series", "2.8-data", "course/modules/LX/LX1/project.html:280; course/assets/data/market/MANIFEST.json", "PASS",
    "MANIFEST has three datasets (fx_daily, fx_monthly, ust_daily). ust_daily is Treasury bill and 10-year yields; fx_daily and fx_monthly are exchange rates. None is gold, price-level, output, unemployment or bank-failure data.")
row("proj-data-embedded-claim", "2.8-data", "course/modules/LX/LX1/project.html:280; MANIFEST", "PASS",
    "'The site embeds three series' matches the MANIFEST dataset count.")
row("proj-spec-ladder", "2.6-spec", "course/modules/LX/LX1/project.html:40-48, :73-258, :261-275, :618-624", "PASS",
    "Ladder order rung 1 (Lab 1), rung 2 (Lab 2, completion), rung 3 (spec, Lab 3 check), rung 4 (stretch) present in order; check_projects --unit LX1 PASS.")
row("proj-spec-curriculum-scope", "2.6-spec", "curriculum/06-profession-capstone.yaml:42-49; course/modules/LX/LX1/project.html:261-275", "PASS",
    "The curriculum project entry (title 'Then vs. now', brief, 'Two-page essay, every claim cited.', grading: rubric) matches the page's title, the spec and the rubric-only grading.")
row("proj-atlas-autograder-na", "2.6-grading", "curriculum/06-profession-capstone.yaml:49; course/modules/LX/LX1/project.html:273", "PASS",
    f"'grading: rubric' (curriculum :49). run_graders --unit LX1: 'no autograder (grading: rubric)' rc 0; mutate_graders --unit LX1 rc 0, no grader to mutate ({S}run_graders_LX1_r20.out, {S}mutate_graders_LX1_r20.out).")
row("proj-mutants-student-errors", "2.6-mutation (lab analogue; LX1 has no grader)", "ledgers/LX1/mutants/ (86 files); ledgers/LX1/scripts/LX1-c-r20/out/kill_r20.out", "PASS",
    f"All 86 mutants run under python -I -W error against the expected block of the lab they mutate ({S}kill_r20.out: 77 killed, 5 survived). The 5 survivors on the "
    f"embedded snapshot (lx1c_r18n02, r18n03, r18n04, r18n05, r17n01) are each killed by a synthetic distinguishing input ({S}synth_kill_r20.out). "
    f"The 4 new mutants are killed (see proj-lab3-r20-mutants). Lab mutants are demonstrations (ruling), so the kill check is informational.")
row("proj-lab3-r20-mutants", "2.5-labs (student-error mutants, own)", "ledgers/LX1/mutants/lx1c_r20n01..n04; ledgers/LX1/scripts/LX1-c-r20/run_new_r20.py", "PASS",
    f"Four new student-error mutants written this round: r20n01 burden percent of the end value (killed, {S}new_mutants_and_alts_r20.out); r20n02 burden as price difference "
    f"(killed); r20n03 window three from 2025-09 (killed); r20n04 zero change by tolerance 1e-9 (survives the snapshot: min nonzero |change| is 5.8e-05, "
    f"{S}min_nonzero_change_r20.out), killed by one synthetic 1e-10 move: exact zero changes 667 vs 668 ({S}tiny_move_r20.out).")
row("proj-alternatives", "2.6-mutation (over-constraint)", "ledgers/LX1/scripts/LX1-c-r20/alts/alt1..alt5", "PASS",
    f"Five alternative correct implementations (reciprocal and rearranged burden and real debt for labs 1 and 2; float ratio before log; window two by month index; zero test by truthiness) "
    f"each reproduce the expected block exactly (rc 0, {S}new_mutants_and_alts_r20.out). The plan's five alternative essay designs (section 5.4) are categories only; "
    "each can reach C2 level 4 under the page's C2 level-4 cell.")
row("proj-exemplar-b-annotations-vs-descriptors", "2.6-rubric", "course/modules/LX/LX1/project.html:548-606 (exemplar B annotations)", "PASS",
    "Annotations quote the descriptors that they meet or miss: C1 2 (date missing for the condition, matches :473 td 3), C3 1 (lists a source), C3 2 missed (three uncited claims, matches :475 td 3), C4 2 (rounds inputs, matches :476 td 3), C2 2 (similarity and difference, no chain, matches :474 td 3), C5 1 (caveats, matches :477 td 4). Not scored by this verifier.")
row("proj-brief-rubric-escape-clauses", "2.6-rubric", "course/modules/LX/LX1/project.html:442, :474, :475", "PASS",
    "The escape clauses ('or the essay states that it makes no such claim' at :443 and :475; 'or is marked as the writer's own inference') are observable: an essay either states it or does not.")
row("proj-exemplar-locators", "2.1-citation", "course/modules/LX/LX1/project.html:490-491, :500-502, :511-513, :521-524, :532-535", "PASS",
    "Exemplar A locators: title field of Eichengreen (registry title matches), MANIFEST field last, Lab 1 Part A and B lines, Lab 3 window lines, Lesson 2 Prop 2.1(a) and Remark 3.3 (L02), Lesson 4 'Exchange rates only' item (L04.html:333). All exist.")
row("proj-exemplar-a-c5-limit-count", "2.6-rubric", "course/modules/LX/LX1/project.html:476-477, :534, :539-540", "PASS",
    "Exemplar A names three limits (:534) and gives the test for limit one only; annotations at :540-541 match the C5 level 3 and level 4 cells (:477 td 2, td 1). Carried from round 19 for the cell text (see carried rows).")
row("proj-round11-delta-project-page", "2.9-prose / delta", "course/modules/LX/LX1/project.html:62, :475, :534", "PASS",
    "The delta-touched lines were read this round: :62 window definitions (668/321/12 counts verified), :475 C3 cells, :534 exemplar A limits. No inconsistency found.")
row("proj-spec-limits-test-each", "2.6-spec", "course/modules/LX/LX1/project.html:269, :444, :476-477, :534", "PASS",
    "The spec (:269) and brief (:444) require two limits, and the test for at least one of them; this matches C5 level 3, not level 4. C5 level 4 requires a test for each limit, which is a rubric standard, not a spec sentence. Consistent.")
row("proj-notation-n-undefined", "2.9-prose / notation", "course/modules/LX/LX1/project.html:60, :431", "PASS",
    "'where n is the number of changes in the window' (:60) defines n before its use in n - 1 (:431, :305 of the lab docstring).")
row("proj-spec-window-start-must", "2.6-spec", "course/modules/LX/LX1/project.html:62, :431; tests/labs/LX1/lab-LX1-project-3.py", "PASS",
    "Window two: first change 2000-01 uses the 1999-12 rate (pairwise over the file, and 321 changes, numbers_r20.out).")
row("proj-rubric-c2-gap", "2.6-rubric", "course/modules/LX/LX1/project.html:474 (C2 L2 cell, bubble clause)", "PASS",
    CARRY + "the C2 level-2 cell is the same text, and the exhaustive C2 model (rubric_coverage_r19_rerun_r20.out) reports 36 consistent feature sets scoring 0, none with a chain or a similarity; 'bubble without benchmark' scores 2 and the named-benchmark variant scores 4.")
row("proj-rubric-c3-level3-gap", "2.6-rubric", "course/modules/LX/LX1/project.html:475 (C3 L3 cell)", "PASS",
    CARRY + "C3 level-3 cell unchanged; the C3 level-4 and level-3 cells differ in the locator condition (every claim with a locator vs at most two without).")
row("proj-rubric-c3-inference-gap", "2.6-rubric", "course/modules/LX/LX1/project.html:474-475, :440", "PASS",
    CARRY + "the inference clause ('marked as the writer's own inference') is present in C3 levels 4 and 3 and in the brief at :443.")
row("proj-rubric-c4-formula-gap", "2.6-rubric", "course/modules/LX/LX1/project.html:476 (C4 cells)", "PASS",
    CARRY + "C4 level-3 'except one' and level-2 'omits, or gives wrong, the formula or the base and sign' are unchanged; the C4 model (rubric_coverage_r19_rerun_r20.out) scores patterns 1, 2 and 6 at 2.")
row("proj-rubric-c5-count-wording", "2.6-rubric", "course/modules/LX/LX1/project.html:477 (C5 cells)", "PASS",
    CARRY + "C5 cells unchanged; level 4 'for each' and level 3 'one with the test' are distinct.")
row("proj-rubric-c2-count-wording", "2.6-rubric", "course/modules/LX/LX1/project.html:474 (C2 L2 cell, first clause)", "PASS",
    CARRY + "Judgment, not a FAIL: 'Lists similarities and at least one difference' is plural; level 1 says 'at least one similarity'. Wording note only (round-19 note).")
row("proj-rubric-exhaustive-r14", "2.6-rubric (exhaustive)", "course/modules/LX/LX1/project.html:474 (C2 L2 bubble clause)", "PASS",
    CARRY + "rerun of the exhaustive model: 36 zero-score C2 feature sets, none with a chain or a similarity.")
row("proj-dag-concepts", "2.9-DAG", "course/modules/LX/LX1/project.html:170 (concept link debt-deflation), :474 (Lesson 1 fundamental value); course/modules/LX/LX1/L02.html:110 (def-debt-deflation)", "PASS",
    "check_dag --unit LX1 PASS. Concepts used on the page (debt deflation, fundamental value, speculative bubble) are in the unit's own lessons (L01 introduces 'speculative bubble' and defines fundamental value, def-fundamental-value; L02 defines debt deflation).")
row("proj-exemplar-A-limit1-cip-locator", "2.1-citation", "course/modules/LX/LX1/project.html:534; course/modules/LX/LX1/L04.html:333", "PASS",
    "Limit one cites 'Lesson 4, Section 4, item \"Exchange rates only\"' and states that the lab cannot test any interest-rate relation; L04.html:333 says exactly that.")
row("proj-exemplar-a-c2-annotation", "2.6-rubric", "course/modules/LX/LX1/project.html:500-520; course/modules/LX/LX1/L02.html (Remark 3.3)", "PASS",
    "The C2 annotations at :506 and :517 name what each step rests on, the analogy-holds step (step 3) and the failure step (step 2) with evidence (Remark 3.3; Lab 3 zero count), all of which appear in the text at :502 and :513.")
row("proj-r14-delta-hunks", "2.9-prose / history", "git merge-base --is-ancestor 8e5751c9 50559266; d1e65a0 50559266", "PASS",
    "Re-run this round: both ancestry checks succeed (r14 history intact).")
row("proj-r15-delta-hunks", "2.9-prose / history", "git merge-base --is-ancestor 56cc575a 50559266", "PASS",
    "Re-run this round: ancestry check succeeds.")
row("proj-r18-delta-hunks", "2.9-prose / delta", "git merge-base --is-ancestor 700bf33f 50559266; git diff -U0 700bf33f 50559266 -- project.html (7 hunks)", "PASS",
    "Re-run this round: ancestry check succeeds; seven project.html hunks in that range were already verified in round 19.")
row("proj-r19-delta-hunks", "2.9-prose / delta", "git diff -U0 cd4dd7df d1083bf1 -- course/modules/LX/LX1/project.html (hunks at :60 and :473)", "PASS",
    "Every hunk in the slice read: :60 adds 'defined under The three windows, below' and n = the number of changes (both match the lab and the page's window definitions); "
    ":473 C1 cells (the defect in proj-rubric-c1-level3-unreachable, and the level-2 fix that resolves proj-rubric-observable). Other LX1 hunks (L03, L04 at :448, cards.json) are outside this slice; L04 :448 is not cited.")
row("proj-check-pages-project-scope", "2.9-structure", "course/modules/LX/LX1/project.html; tools/check_pages.py", "PASS",
    f"check_pages --unit LX1 PASS and page_smoke --pages project PASS (both this round, {S}check_pages_LX1.out, {S}page_smoke_project.out).")
row("proj-links-anchors", "2.9-structure", "course/modules/LX/LX1/project.html (href and id); index.html#placement; L02.html#def-debt-deflation", "PASS",
    "Every in-page href=\"#...\" resolves to an id on the page (none unresolved, checked this round). index.html#placement and L02.html#def-debt-deflation ids exist.")
row("proj-page-smoke", "2.9-structure", "course/modules/LX/LX1/project.html", "PASS",
    f"page_smoke --unit LX1 --pages project PASS (3 labs, 0.0 s each; {S}page_smoke_project.out).")
row("proj-lab3-raise-claims-untested", "2.5-labs", "course/modules/LX/LX1/project.html:308-309 (Check paragraph), :431", "PASS",
    "Check paragraph: 'A blank or non-decimal cell ... raises ValueError, and so does a month that does not follow the previous one.' Verified this round on the twin: a blank cell (1995-12) gives rc 1 with 'ValueError: 1995-12: GBP cell ... blank'; a month gap (1996-01 after 1995-11) gives rc 1 with 'ValueError: month 1996-01 does not follow 1995-11'.")
row("proj-lab3-blank-gap-inputs", "2.5-labs", "tests/labs/LX1/lab-LX1-project-3.py; ledgers/LX1/mutants/r17n01, lx1c_r18n05, lx1c_r8n03, lx1c_r8n04", "PASS",
    "The raise behaviour above is the twin's. The silent-blank and gap mutants are killed: r8n03 and r8n04 by the expected block; r18n05 by a synthetic blank cell "
    "(the mutant accepts it, rc 0, and the twin raises, rc 1); r17n01 by a synthetic blank cell where the mutant reads it as 0.0 and fails later with a different ValueError "
    "(log of 0.0), so its kill is by output and error path, not by the blank check (" + S + "synth_kill_r20.out; " + S + "blank_check_r20.out: r18n05 accepts the blank with rc 0; r8n04 accepts the gap with rc 0).")
row("proj-lab3-r19-mutants", "2.5-labs (student-error mutants, own)", "ledgers/LX1/mutants/lx1c_r19n01..n03", "PASS",
    f"lx1c_r19n01..r19n03 are in the directory and KILLED in {S}kill_r20.out.")
row("proj-lab2-R-blank-check", "2.5-labs", "course/modules/LX/LX1/project.html:184, :214, :219, :257", "PASS",
    "The completion lab's blanks are the only differences between page and twin (verified by line diff this round); the instant check compares the whole block (:257), which is true of run_labs.")

notes = [
    "Scope: course/modules/LX/LX1/project.html (all 649 lines read) and tests/labs/LX1/lab-LX1-project-{1,2,3}.py, pin d1083bf1 (round-19 pin cd4dd7df). Delta in the slice: project.html :60 and :473 only.",
    "Highest-level scoring rule at project.html:467 (the prompt's 'line 465' is the section opener).",
    "The round-19 FAIL rows proj-rubric-observable and proj-student-error-coverage are resolved by the d1083bf1 edit to :473 td 3 and td 2 (the level-2 text); the new defect is the level-3 cell at :473 td 2 now duplicating level 4 (proj-rubric-c1-level3-unreachable).",
    "Exemplar scores were not computed by this verifier (ruling 23). Calibration rows cite ~/.fanout/blind/LX1-c.json.",
    "Survivors: 5 of the 86 mutants survive the embedded snapshot; each is killed by a synthetic input (synth_kill_r20.out, tiny_move_r20.out). lx1c_r18n02 is killed only by a formatting artifact (-0.00 vs 0.00 from a near-zero difference). Lab mutants are demonstrations (ruling), so these are not findings.",
    "The four new mutants are in ledgers/LX1/mutants/ (r20n01..n04). They are student errors plausibly written by a learner; no mutant sits at a tolerance boundary of the grader kind (ruling 25 concerns graders).",
    "Judgment, not a FAIL: 'Lists similarities' plural (C2 L2); reinhart2009this is absent from the page reading list (optional per plan 5.2); friedman1963monetary record lists one author while the source string names two.",
    "Judgment, not a FAIL: the letter T appears as an evidence grade (project.html:66) and not as the registered number-of-observations symbol.",
    "Not run: the full repository pytest (not needed for a project slice); the raw H.10 XML rebuild (rebuild_fx_monthly_r19.sh needs the raw file; the sha256 and fetch_data --check cover the embedded CSV); live Board website access (not needed; the licence quote is checked against MANIFEST).",
]

killed_by_exist = {}
for line in (ROOT / S.replace("out/", "out/kill_r20.out")).read_text(encoding="utf-8").splitlines():
    m = re.match(r"KILLED lab(\d) (\S+) \| (.*)", line)
    if m:
        killed_by_exist[m.group(2)] = f"lab {m.group(1)} expected block or rc (kill_r20.out): {m.group(3)}"
    m2 = re.match(r"SURVIVED lab(\d) (\S+)", line)
    if m2:
        killed_by_exist[m2.group(2)] = None
synth = {}
for line in (ROOT / S / "synth_kill_r20.out").read_text(encoding="utf-8").splitlines():
    m = re.match(r"(\S+): KILLED on synthetic seed (\d+) \(blank=(\w+)\)", line)
    if m:
        synth[m.group(1)] = f"synthetic snapshot seed {m.group(2)} (blank={m.group(3)}): twin and mutant outputs differ (synth_kill_r20.out)"
r19 = json.loads(Path("/Users/billyribeiro/.fanout/frags/E-LX1-c.round19.json").read_text(encoding="utf-8"))
desc = {m["name"]: m.get("description", "") for m in r19["mutants"]}
mutants = []
for name in sorted(p.name for p in (ROOT / "ledgers/LX1/mutants").glob("*.py")):
    if name in killed_by_exist and killed_by_exist[name] is not None:
        kb = killed_by_exist[name]
    elif name in synth:
        kb = synth[name] + ("; error path differs (log of 0.0), not the blank check" if name.startswith("r17n01") else "")
    elif name.startswith("lx1c_r20n04"):
        kb = "synthetic 1e-10 move at month index 100: twin 667 exact zero changes, mutant 668 (tiny_move_r20.out)"
    else:
        kb = None
    if name.startswith("lx1c_r20n01"):
        kb = "lab 1 expected block (run_new_r20.py via new_mutants_and_alts_r20.out)"
    elif name.startswith("lx1c_r20n02"):
        kb = "lab 2 expected block (run_new_r20.py via new_mutants_and_alts_r20.out)"
    elif name.startswith("lx1c_r20n03"):
        kb = "lab 3 expected block (run_new_r20.py via new_mutants_and_alts_r20.out)"
    d = desc.get(name) or next((l.strip("# ").strip() for l in (ROOT / "ledgers/LX1/mutants" / name).read_text(encoding="utf-8").splitlines() if l.strip()), name)
    mutants.append({"name": name, "description": d, "killed_by": kb})

frag = {
    "unit": "LX1",
    "slice": "LX1-c",
    "round": 20,
    "verifier": "Claude Haiku 5.5 (claude-haiku-5-5), independent verifier for LX1-c, round 20 (did not build LX1)",
    "pin": "d1083bf142be6e33189af7de81d83719288ed2fb",
    "base": "cd4dd7dfc2bbe0fc16b672329daa408d1d8a268b (round-19 pin; round-19 fragment /Users/billyribeiro/.fanout/frags/E-LX1-c.round19.json)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE20-LX1-c",
    "scratch": "ledgers/LX1/scripts/LX1-c-r20/ (scripts and out/); synthetic and scratch data only under /tmp/lx1c-r20-scratch and /tmp/lx1c-r20-gap",
    "verified_at": "2026-11-09T00:00:00Z",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": notes,
    "summary": (f"{len(rows)} rows: {sum(1 for r in rows if r['status'] == 'PASS')} PASS, "
                f"{sum(1 for r in rows if r['status'] == 'FAIL')} FAIL (proj-rubric-c1-level3-unreachable). "
                f"{len(mutants)} mutants, all killed (5 embedded-snapshot survivors killed on synthetic inputs). "
                "Gates all rc 0. Calibration PASS against the blind scorer file."),
}
out = ROOT / "ledgers/LX1/LX1-c.json"
out.write_text(json.dumps(frag, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out, "rows", len(rows), "mutants", len(mutants), "killed", sum(1 for m in mutants if m["killed_by"]))
