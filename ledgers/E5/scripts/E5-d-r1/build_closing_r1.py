"""Builds ledgers/E5/E5-d.json (round 1, closing delta, pin 2a805c83) from the base fragment rows and the fresh checks
recorded in out/r1_*.out. Run with -I from the checkout root."""
import json, sys
CARRY = ("Carried from round 1 (course/modules/E/E5/project.html, tests/labs/E5/*, L01-L06.html and their cards, "
         "references/, notation/, curriculum/, tools/ byte-identical since the previous pin 95f3f8cb): ")
ROWS = []
def row(i, check, loc, status, ev, fix=""):
    r = {"id": i, "check": check, "location": loc, "status": status, "evidence": ev}
    if fix:
        r["fix"] = fix
    ROWS.append(r)
def carry(i, check, loc, ev):
    row(i, check, loc, "PASS", CARRY + ev)

carry("proj-lab2-gap-survivor", "Lab 2 hypothesis, rung-2 ladder and interpretation match the lab check (round-4 FAIL re-verified)",
      "project.html ladder item 2 (Rung 2) and Lab 2 interpretation; tests/labs/E5/lab-E5-project-2.py",
      "base evidence stands. Re-run now: ledgers/E5/scripts/E5-d-r1/out/r1_standing_mutants.out lists r4_m05_gap_percent_of_trend and m02_gap_percent_of_trend as PASSES_CHECK; out/r1_lab2_gap_check.out prints log_gap -0.183842 and pct_gap -0.183673, both -0.18 at two decimals; project.html line 45 still says the instant check does not separate the two gaps.")
carry("cards-c050-basis-fact-4-1", "E5-c050 basis cites Assumption 4.1, not Fact 4.1",
      "cards.json E5-c050; course/modules/E/E5/L03.html Assumption 4.1 and Proposition 4.2",
      "cards.json E5-c050 is byte-identical (the delta touches only E5-c033, c034, c120, c127, c132 and adds c141); grep -c 'Fact 4.1' L03.html is unchanged at 0.")
carry("cards-c095-holding-condition", "E5-c095 back states the holding condition and the units",
      "cards.json E5-c095; course/modules/E/E5/L06.html Proposition 2.1 and units sentence", "E5-c095 and L06.html byte-identical.")
carry("proj-honest-pending", "Honest-pending data note on the project page",
      "course/modules/E/E5/project.html section#data p.honest-pending", "project.html byte-identical; no E5 data file changed.")
row("cmd-check-projects", "tools/check_projects.py --all", "tools/check_projects.py --all", "PASS",
    "Fresh on 2a805c83: ledgers/E5/scripts/E5-d-r1/out/r1_check_projects.out line 14 'check_projects E5: PASS', exit 0.")
row("cmd-check-dag", "tools/check_dag.py --all", "tools/check_dag.py --all", "PASS",
    "Fresh: out/r1_check_dag.out line 14 'check_dag E5: PASS', exit 0 (covers the changed index.html concept links).")
row("cmd-check-pages", "tools/check_pages.py --all", "tools/check_pages.py --all", "PASS",
    "Fresh: out/r1_check_pages.out line 14 'check_pages E5: PASS', exit 0 (covers the changed L07, L08 and index.html).")
row("cmd-run-labs", "tools/run_labs.py --unit E5", "tests/labs/E5/*; course/modules/E/E5/*.html", "PASS",
    "Fresh: out/r1_run_labs_E5.out 'run_labs E5: PASS (11/11)', exit 0; each twin is byte-identical to its page code and its stdout matches the expected block.")
row("cmd-page-smoke-project", "tools/page_smoke.py --unit E5 --pages L02 L03 L04 L05 L06 project", "course/modules/E/E5 pages", "PASS",
    CARRY.replace("(course/", "(course/") + "L02-L06 and project byte-identical, so the base run stands. The changed pages were run fresh: see cmd-page-smoke-changed-pages.")
row("cmd-pytest", "pytest tests/test_labs.py -k E5; pytest tests/test_page_checks.py", "tests/", "PASS",
    "Fresh: out/r1_pytest_labs_E5.out (11 tests) and out/r1_pytest_page_checks.out (41 tests), both exit 0.")
row("cmd-verify-refs", "tools/verify_refs.py --offline; tools/verify_refs.py --unit E5", "references/references.json", "PASS",
    "Fresh: out/r1_verify_refs_offline.out 'offline integrity: 560 entries, 0 problems' exit 0; out/r1_verify_refs_E5.out 'live re-verification of E5: 4 of 560 entries, 0 problems' exit 0. The live check is the tool's own path; I did not run separate curl checks.")
row("proj-hours", "Hours arithmetic: hub split and lesson hours against the project", "index.html line 29 (data-hours-lessons=80, data-hours-project=30), line 31 (eyebrow '110 hours'), line 42 ('80 h lessons · 30 h project (27.3% of 110 h)'); project.html line 33 (data-hours-project=30) and #hours-table",
    "PASS", "Fresh: 8 lessons x 10 h = 80 h (index.html card-grid, 'Eight lessons of ten study hours each'); 80 + 30 = 110; 30/110 = 27.3%; the 72.7%/27.3% split bars match. The delta does not touch any hours value.")
row("proj-adversarial-and-mutants", "Grading mode, mutants and alternatives for the project",
    "course/modules/E/E5/project.html #spec Grading mode; tests/labs/E5; ledgers/E5/mutants; index.html and L02-L08 changed text",
    "PASS", "Fresh: out/r1_mutate_graders_E5.out 'exit 0' with no output (no grader mutant files directly under ledgers/E5/mutants/*.py); the lab-2 standing set is run in cmd-lab2-standing-mutants. grep of index.html and L02-L08 for mutant|grader|alternative|adversar|verifier|ledger|fixer finds no learner-facing process words (only 'round half to even').")
carry("proj-notation", "Notation of the project page against notation/notation.json",
      "course/modules/E/E5/project.html LaTeX spans; notation/notation.json",
      "project.html and notation/notation.json byte-identical. The changed L07, L08, index and card text introduces no new symbol (checked: L07 Part C wording, L08 why-it-matters, index objectives and meta rows, cards c127 and c132 use existing symbols c, G, Tax, Delta G).")
row("proj-dag", "Project page concept use and DAG", "course/modules/E/E5/project.html; tools/check_dag.py --all; course/modules/E/E5/index.html concept links",
    "PASS", "Fresh: check_dag E5 PASS (out/r1_check_dag.out). index.html concept links resolve: comparative-statics and competitive-equilibrium are defined in E1 L04 and E1 L03; derivative in M2 L04; implicit-function-theorem in M2 L21; exponential-and-logarithm in M1 L03 (course/concepts.html). evidence-grade, notation-conventions and project-ladder read 'not yet released' (concepts.html).")
carry("proj-reading-list", "Project reading list against references/references.json", "course/modules/E/E5/project.html #reading; references/references.json",
      "references/references.json and project.html byte-identical; verify_refs fresh PASS (cmd-verify-refs).")
row("proj-process-words", "No process words in learner text", "project.html whole page; index.html; L07, L08 changed text; tools/check_pages.py banned strings",
    "PASS", "Fresh: check_pages E5 PASS (banned strings); grep of the changed pages finds no process words.")
row("cards-scope-and-duplicates", "Card scope, ids and duplicates", "course/modules/E/E5/cards.json",
    "PASS", "Fresh: out/r1_card_structure.out: 140 cards, 140 unique ids, 140 unique fronts, no duplicate backs; ids are E5-c001..c141 with c135 absent (ruling 2 allows gaps); E5-c141 is new and not a duplicate.")
row("cards-numbers-in-lesson", "Every numeric token of each card appears in its lesson", "course/modules/E/E5/cards.json; course/modules/E/E5/L01-L08.html",
    "PASS", "Fresh: out/r1_card_numbers_strict.out 'tokens not in own lesson, not in any twin output: []'; out/r1_card_structure.out lists only E5-c102 '1.226' and '1.236', which appear as 1.226000 and 1.236000 in the L06 expected block (line 231), the same value at six decimals.")
carry("cards-sample-2", "E5-c020 against L01 Proposition 2.6 and misconception 4", "cards.json E5-c020; L01.html", "E5-c020 and L01.html byte-identical.")
carry("cards-sample-3", "E5-c030 against L02 Definition 2.2", "cards.json E5-c030; L02.html Definition 2.2", "E5-c030 byte-identical; L02.html carried (not in the delta).")
carry("cards-sample-4", "E5-c040 against L03 Remark 2.3", "cards.json E5-c040; L03.html Remark 2.3", "E5-c040 and L03.html byte-identical.")
carry("cards-sample-5", "E5-c050 against L03 Proposition 4.2 and Assumption 4.1", "cards.json E5-c050; L03.html", "E5-c050 and L03.html byte-identical.")
carry("cards-sample-6", "E5-c060 against L04 Definition 3.1", "cards.json E5-c060; L04.html Definition 3.1", "E5-c060 and L04.html byte-identical.")
carry("cards-sample-7", "E5-c070 against L04 Proposition 3.2 and Remark 1.2", "cards.json E5-c070; L04.html", "E5-c070 and L04.html byte-identical.")
carry("cards-sample-8", "E5-c080 against L05 Proposition 2.2", "cards.json E5-c080; L05.html", "E5-c080 and L05.html byte-identical.")
carry("cards-sample-9", "E5-c090 against L06 section 1", "cards.json E5-c090; L06.html section 1", "E5-c090 and L06.html byte-identical.")
carry("cards-sample-10", "E5-c100 against L06 Definition 1.2 and Lab 1 Part C", "cards.json E5-c100; L06.html", "E5-c100 and L06.html byte-identical.")
row("cards-sample-11", "E5-c110 (Taylor rule) against L07 Definition 1.4", "cards.json E5-c110; course/modules/E/E5/L07.html lines 73-76",
    "PASS", "Fresh: card formula i(t) = r^n + pi(t) + phi_pi (pi(t) - pi-bar) + phi_y y(t) and the real-rate equivalent match L07 Definition 1.4 (\\[i_t = r^{n} + \\pi_t + \\phi_{\\pi}(\\pi_t - \\bar\\pi) + \\phi_{y} y_t\\]). The changed L07 why-it-matters does not touch Definition 1.4.")
row("cards-sample-12", "E5-c120 (fiscal multiplier) against L08 Definition 1.2", "cards.json E5-c120; course/modules/E/E5/L08.html lines 71-74",
    "PASS", "Fresh: E5-c120 changed in the delta ('in cents, so it is a number with no unit'); L08 Definition 1.2 (line 71-74) says the same: ratio of the change in equilibrium output, in cents, to the change in government spending, in cents, a number with no unit.")
row("cards-sample-13", "E5-c130 (no estimate of the multiplier) against L08 page statement", "cards.json E5-c130; course/modules/E/E5/L08.html Proposition 2.2 (line 217-218) and the statement at line 274",
    "PASS", "Fresh: Proposition 2.2 is stated under A1 to A3 (line 217-218); line 274 says the page gives no estimate of any multiplier. L08 is changed only in why-it-matters, which does not alter either.")
row("cards-derivations", "Derivation-type cards: values and hypotheses",
    "cards.json E5-c014, c022, c035, c051, c052, c062, c064, c065, c079, c080, c099, c102, c122-c125, c128, c129",
    "PASS", "Fresh for the L08 subset (E5-c122, c123, c124, c125, c128, c129; L08 changed): S_N = dG(1-c^N)/(1-c) (Prop 2.1, line 82); multiplier dG/(1-c) under A1 to A3 (Prop 2.2, line 218); S_N = dG/(1-c) - dG c^N/(1-c) and c^N <= 1/(1+N(1/c-1)) (Prop 2.3, line 228, Bernoulli); tax multiplier -c dTax/(1-c) and balanced-budget 1 (Prop 2.4, line 238). Lab 1 prints tax change -15000 and balanced 10000, spend change 25000 (out via tests/labs/E5/lab-E5-L08-1.py). CARRY for the L01-L06 subset: " + "E5-c014, c022, c035, c051, c052, c062, c064, c065, c079, c080, c099, c102 and their lessons are byte-identical since 95f3f8cb.")
row("cards-lab-numbers", "Lab-number cards: numbers equal the printed lab values and appear in the lesson",
    "cards.json E5-c019-c021, c033-c034, c036, c048, c051-c052, c067-c069, c082-c087, c100-c104, c113-c117, c127-c129, c141",
    "PASS", "Re-verified (was FAIL in round 1 because E5-c034 printed 0.005589 as a C value). E5-c034 now has no lab number. E5-c141 (C, basis 'Lab 1 (SIMULATED, one seed)') gives 0.005589, 0.016254 and 0.010665, which L02.html prints in its expected block (lines 257-258) and states at lines 285 and 361. E5-c127 (25000) matches 'Y_before 162500 Y_after 187500 change 25000'; E5-c132 matches 'tax_stage_amounts -6000 -3600 -2160'; E5-c113 (-1/2 at pi 1, y -2) matches 'output_gap -2: pi_1=-1/2'; E5-c114 (5/2) matches 'phi_pi 3/2 nominal_response 5/2'; E5-c115 (False at phi_pi 0) matches; E5-c116 (3) and c117 (real 1) match the Part D lines; E5-c118 (second differences 0) matches; E5-c128 and c129 match (25000; -15000; 10000). Other lab-number cards are carried from round 1 (their cards and lessons are byte-identical); out/r1_card_numbers_strict.out shows every numeric token in them is in its lesson.")
row("cmd-ruff-mypy", "ruff check, ruff format --check, mypy --no-incremental", "repository; tests/labs/E5 twins", "PASS",
    "Fresh: out/r1_ruff_check.out 'All checks passed!' exit 0; out/r1_ruff_format.out '555 files already formatted' exit 0; out/r1_mypy.out 'Success: no issues found in 386 source files' exit 0.")
row("proj-lab2-student-errors", "Lab 2 student-error mutants fail; alternatives pass",
    "tests/labs/E5/lab-E5-project-2.py; ledgers/E5/mutants/project-2*/",
    "PASS", CARRY + "project.html and the lab-2 twin byte-identical. Fresh run of the full standing set (ledgers/E5/scripts/E5-d-r1/run_standing_mutants.py, out/r1_standing_mutants.out, total 21): 14 mutants KILLED; 5 correct alternatives PASS (project-2-r4 alt01, alt02; project-2/alt alt01-03); 2 documented survivors (r4_m05 and m02, percent-of-trend gap) which project.html line 45 documents as not separated by the instant check.")
row("cmd-build-site", "tools/build_site.py --check", "course/index.html, concepts.html, data", "PASS",
    "Fresh: out/r1_build_site_check.out 'site data current: 6 outputs', exit 0. git diff 95f3f8cb..2a805c83 shows no change to course/index.html or course/concepts.html.")
row("cmd-render-curriculum", "tools/render_curriculum.py and git diff --exit-code CURRICULUM.md curriculum/curriculum.json", "CURRICULUM.md; curriculum/curriculum.json", "PASS",
    "Fresh: render exit 0 and git diff --exit-code clean (out/r1_render_curriculum.out).")
row("cmd-fetch-data", "tools/fetch_data.py --check", "course/assets/data/market/", "PASS", "Fresh: out/r1_fetch_data_check.out 'fetch_data: 3 datasets, 0 problems', exit 0.")
carry("cards-changed-c014-c016", "E5-c014 and E5-c016 against L01 Propositions 2.4 and 2.6", "cards.json E5-c014, E5-c016; L01.html", "cards and L01.html byte-identical.")
carry("cards-changed-c041-c045", "E5-c041 to c045 against L03 Propositions and Remark 2.5", "cards.json E5-c041..c045; L03.html", "cards and L03.html byte-identical.")
row("cards-remark-labels", "Remark, Definition, Proposition, Assumption and Problem labels cited by cards exist in the card's lesson", "cards.json basis and back fields; L01-L08.html",
    "PASS", "Fresh: out/r1_card_structure.out 'cited labels absent from own lesson: []' (includes L07 Remark 2.3, L08 Remark 2.5 and Definitions 1.1-1.4 and 1.1-1.3 of L08).")
carry("proj-exA-c2-annotation", "Exemplar A Computation passage and annotation", "project.html #exemplar-a", "project.html byte-identical.")
carry("proj-exA-length", "Exemplar A word counts and Rung 3 constraints", "project.html #exemplar-a; Rung 3 Constraints; The brief item 1", "project.html byte-identical.")
carry("proj-lab2-one-pair", "Lab 2 hypothesis, Rungs 1-2 paragraph and interpretation", "project.html; tests/labs/E5/lab-E5-project-2.py docstring", "project.html and the twin byte-identical.")
carry("proj-spec-ladder", "Project ladder, spec, data, lab 3 section, brief, stretch", "project.html #ladder, #spec, #data, #lab-3-section, #brief, #stretch", "project.html byte-identical.")
carry("proj-rubric-observable", "Rubric observable levels", "project.html table#rubric", "project.html byte-identical.")
carry("proj-calib-exB", "Exemplar B calibration scores", "project.html #exemplar-b data-scores=2,2,2,2,1",
      "No E5 blind scorer file exists in ~/.fanout/blind/ (listing: BK4, CS2, E1, E3, E4, FC2, LX1, M5, PC3 only), so the base calibration row is carried (ruling 23).")
carry("proj-calib-exA-blind", "Exemplar A blind calibration", "project.html #exemplar-a data-scores=4,4,4,4,3",
      "No E5 blind scorer file exists in ~/.fanout/blind/ (ruling 23); base calibration carried.")
carry("proj-conventions-gaps", "Conventions: output gap, rounding, cycle flag, Taylor-rule value", "project.html #conventions", "project.html byte-identical.")
carry("proj-lab1-numbers", "Lab 1 hypothesis, expected block, interpretation", "project.html; tests/labs/E5/lab-E5-project-1.py", "project.html and the twin byte-identical; run_labs fresh PASS.")
carry("proj-lab3-table", "Lab 3 expected block against its twin", "project.html lines 527-541; tests/labs/E5/lab-E5-project-3.py with data/ust_daily.csv", "project.html, the twin and ust_daily.csv byte-identical; run_labs fresh PASS.")
carry("proj-lab3-expected-prose", "Lab 3 hypothesis paragraph and interpretation", "project.html lines 353 and 542", "project.html byte-identical.")
carry("proj-lab3-days-and-spread", "Lab 3 day counts and spread wording", "project.html #data-spread; course/assets/data/market/ust_daily.csv; MANIFEST.json", "data file, MANIFEST and project.html byte-identical; fetch_data fresh PASS.")
carry("proj-data-licence", "Embedded snapshot licence and source note", "project.html #data-spread; MANIFEST.json ust_daily; tools/data_sources.yaml", "project.html, MANIFEST.json and tools/data_sources.yaml byte-identical.")
carry("proj-basis-claims", "Basis paragraph and Exemplar A limits", "project.html #data-spread basis; Exemplar A Limits", "project.html byte-identical.")
carry("proj-taylor-exA", "Exemplar A policy reading and limits", "project.html #exemplar-a", "project.html byte-identical.")
carry("proj-exB-numbers", "Exemplar B numbers", "project.html #exemplar-b", "project.html byte-identical.")
carry("proj-atlas-disclosure", "Atlas-series disclosure in the project spec", "project.html #spec Inputs; curriculum/02-economics-finance-core.yaml lines 184-190", "project.html and curriculum/ byte-identical.")
carry("proj-page-length-and-voice", "Brief item count and exemplar headings", "project.html #brief; Exemplar A h5 headings", "project.html byte-identical.")
carry("proj-no-network-no-file-input", "No file input or network statement", "project.html #data", "project.html byte-identical.")
carry("proj-delta-window-definition", "Window and trend definition", "project.html #conventions 'Window and trend'", "project.html byte-identical.")
carry("proj-delta-exA-limits", "Exemplar A limits", "project.html #exemplar-a Limits", "project.html byte-identical.")
carry("cards-sample-1", "E5-c010 against L01 Definition 2.1", "cards.json E5-c010; L01.html Definition 2.1", "E5-c010 and L01.html byte-identical.")
row("cards-c033-missing-hypothesis", "E5-c033 carries the Proposition 2.4 hypothesis (round-1 FAIL re-verified)",
    "course/modules/E/E5/cards.json E5-c033 back; course/modules/E/E5/L02.html Proposition 2.4 (line 120-123), Lesson text line 131",
    "PASS", "Fresh: E5-c033 back now reads 'depends on that alpha whenever the average growth of capital and of labour differ (Proposition 2.4)'. L02 Proposition 2.4 (line 123): 'Given alpha != alpha', the two average residuals coincide if and only if the average growth of capital equals the average growth of labor'; its grade is T (line 120). The card's 'whenever' is the direction of that iff. Basis 'Definition 2.1; Proposition 2.4; Theorem 2.3' is unchanged in substance.")
row("cards-c034-missing-hypothesis", "E5-c034 carries the Proposition 2.4 hypothesis and is graded to match (round-1 FAIL re-verified)",
    "course/modules/E/E5/cards.json E5-c034 back, grade and basis; L02.html Proposition 2.4 and the key-results row at line 406",
    "PASS", "Fresh: E5-c034 is now T with basis 'Theorem 1.4; Proposition 2.4' and says 'a different number for each alpha whenever the average growth of capital and of labour differ'. Proposition 2.4 (line 123) gives the difference -(alpha - alpha')(avg dlnK - avg dlnL) exactly, so the card is T. The key-results row (line 406, T, 'Proposition 2.4; Lab 1 averages') agrees.")
carry("lessons-delta-hunks", "Changed lesson hunks of the round-1 delta (L02 emp-3 solution, honest-pending note, limitation bullet; L03 section 5 bullet and references; L04 why-it-matters, A3, Remark 1.2, Parts B-D)",
      "course/modules/E/E5/L02.html, L03.html, L04.html", "L02-L04 are byte-identical since 95f3f8cb (not in git diff 95f3f8cb..2a805c83).")
carry("lab-twins-L04-L06-delta", "Lab twins L04 to L06 and their pages", "tests/labs/E5/lab-E5-L04-1.py, lab-E5-L05-1.py, lab-E5-L06-1.py; L04-L06.html",
      "twins and pages byte-identical; run_labs fresh PASS 11/11.")
row("cards-delta-coverage", "Card ids are complete for the delta", "course/modules/E/E5/cards.json", "PASS",
    "Fresh: ids E5-c001..c141 with E5-c135 absent (ruling 2); the delta adds E5-c141 (C, Lab 1 averages); no id removed.")

row("cmd-page-smoke-changed-pages", "page_smoke for the pages changed in the delta", "course/modules/E/E5/L07.html, L08.html, index.html", "PASS",
    "Fresh: out/r1_page_smoke_L07_L08_index.out: page_smoke modules/E/E5/index.html PASS, L07.html PASS, L08.html PASS, 'page_smoke E5: PASS', exit 0 (light and dark, desktop and 360 px, console and link checks, labs lab-E5-L07-1 and lab-E5-L08-1 run).")
row("cmd-lab2-standing-mutants", "Standing lab-2 mutant and alternative set re-run (ruling 37)", "ledgers/E5/mutants/project-2*/; project.html lab-2 expected block (the second pre.expected in project.html, read by run_standing_mutants.py)", "PASS",
    "Fresh: out/r1_standing_mutants.out, total 21: 14 KILLED (r4_m01-m04, r5_m01-m03, m01, m03-m08), 5 correct alternatives PASS, 2 documented survivors (r4_m05, m02). Same result as round 1. No new mutant was authored (ruling 37).")
row("changed-hunks-L07-L08-index", "Changed hunks of L07, L08, index.html and cards (ruling 30 subject-changed rows)",
    "course/modules/E/E5/L07.html why-it-matters (line 52) and Part C interpretation (line 227); L08.html why-it-matters (line 52); index.html lines 33, 35, 37, 51, 60, 72, 147; cards E5-c033, c034, c120, c127, c132, c141",
    "PASS", "Fresh checks: L07 Part C prints first_differences 5/2 5/2 5/2 5/2 and second_differences 0 0 0 (the 'first differences' and 'second differences' wording and 'every line whose check name starts with equals_ or matches_ ... prints True' are accurate; the real_rate_rises False for phi_pi = 0 is stated). L07 'Definitions 1.1 to 1.4' exist (lines 59-74); 'affine at a fixed output gap' matches Problem P1 (line 289). L08 'Definitions 1.2, 1.3' and 'Definition 1.1' exist (lines 57-76); Lab 1 Part C prints 'change 25000'. L08 'Lab 1 checks both exactly': Part A closed-form check True for N 1-30. index line 60: E1 and M2 concept links open the entries that define them (see cmd-check-dag row); P0.1 concepts 'not yet released'. index line 51 objective matches Proposition 2.4. index line 147 card-body matches L02. index line 72 '#ladder' anchor exists (index.html line 157). index line 33 Solow recursion matches L03 (line 60) and adaptive expectations match L06 Assumption A3. Observation only: see notes (Definition 1.1 cited for 'between 0 and 1', which is A1).")
row("idx-prereq-build-status", "index.html prerequisite status of E1, M1, M2 and P0.1 (round-1 FAIL re-verified)",
    "course/modules/E/E5/index.html line 35 (Prerequisites meta-row) and line 60 (prerequisites paragraph)", "PASS",
    "Fresh: index.html line 35 now says P0.1 'is not yet released'; E1, M1 and P0.1 'are referred to by their concepts'. Line 60 says the P0.1 links open 'not yet released' entries and the E1 and M2 links 'open the entries that define them'. Verified: course/modules/E/E1 and course/modules/M/M2 exist (built); concepts.html defines comparative-statics (E1 L04), competitive-equilibrium (E1 L03), derivative (M2 L04), implicit-function-theorem (M2 L21); evidence-grade, notation-conventions, project-ladder read 'not yet released'; no course/modules/P directory. The round-1 false statement (E1 and M2 not built) is gone.")
row("idx-data-status-labs-simulated", "Index data-status sentence: 'The labs use SIMULATED numbers, which each lab generates or types in and labels as SIMULATED, or illustrative parameters.'",
    "course/modules/E/E5/index.html line 37 (Data meta-row); course/modules/E/E5/project.html line 351 (lab-E5-project-3 data-files='ust_daily.csv'), lines 353 and 358-361 (term spread labelled REAL)",
    "FAIL", "A lab statement the code does not support (ruling 26 kind). The sentence is universal over 'the labs', but project Lab 3 (tests/labs/E5/lab-E5-project-3.py) reads data/ust_daily.csv and project.html labels the term spread REAL (line 353: 'The term spread is REAL, read from the embedded snapshot'; line 360: 'REAL: the term spread is read from data/ust_daily.csv'). The course labs are SIMULATED or illustrative (L01-L08 hypotheses checked). Severity low: the same meta-row's next sentence discloses the project's embedded H.15 snapshot. ", fix="Replace the sentence with: 'The course labs use SIMULATED numbers or illustrative parameters, each labelled as such. Project Lab 3 reads the term spread from the embedded H.15 snapshot and labels it REAL.' (index.html line 37; no other change).")

mutants = [
 {"id": "r4_m01_spread_sign_reversed", "description": "spread sign reversed (round-4 mutant)", "killed_by": "KILLED fresh: out/r1_standing_mutants.out, token 27 -0.83 vs 0.83 beyond 1e-6"},
 {"id": "r4_m02_spread_previous_quarter", "description": "spread uses previous quarter (round-4 mutant)", "killed_by": "KILLED fresh: token 27 1.01 vs 0.83"},
 {"id": "r4_m03_gap_time_index_off_by_one", "description": "gap time index off by one (round-4 mutant)", "killed_by": "KILLED fresh: token 31 -0.67 vs -0.18"},
 {"id": "r4_m04_gap_trend_at_window_start", "description": "trend evaluated at window start (round-4 mutant)", "killed_by": "KILLED fresh: token 31 9.10 vs -0.18"},
 {"id": "r4_m05_gap_percent_of_trend", "description": "percent-of-trend gap instead of log gap: survives the instant check; documented on project.html line 45, so not a grader finding", "killed_by": ""},
 {"id": "r5_m01_spread_sum_not_difference", "description": "spread as sum, not difference", "killed_by": "KILLED fresh: token 27 3.83 vs 0.83"},
 {"id": "r5_m02_gap_growth_not_level", "description": "gap from growth not level", "killed_by": "KILLED fresh: token 31 0.05 vs -0.18"},
 {"id": "r5_m03_gap_trend_window_19", "description": "trend window 19 quarters", "killed_by": "KILLED fresh: token 31 0.30 vs -0.18"},
 {"id": "m01_gap_intercept_only", "description": "gap uses intercept only", "killed_by": "KILLED fresh: token 31 9.10 vs -0.18"},
 {"id": "m02_gap_percent_of_trend", "description": "percent-of-trend gap (earlier round copy): survives the instant check; documented on project.html line 45, not a grader finding", "killed_by": ""},
 {"id": "m03_gap_lagged_output", "description": "gap uses lagged output", "killed_by": "KILLED fresh: token 31 -0.24 vs -0.18"},
 {"id": "m04_gap_window_24", "description": "gap window 24 quarters", "killed_by": "KILLED fresh: token 31 -2.14 vs -0.18"},
 {"id": "m05_spread_reversed", "description": "spread reversed", "killed_by": "KILLED fresh: token 27 -0.83 vs 0.83"},
 {"id": "m06_spread_fixed_offset", "description": "spread with fixed offset", "killed_by": "KILLED fresh: token 27 0.80 vs 0.83"},
 {"id": "m07_gap_sign_flipped", "description": "gap sign flipped", "killed_by": "KILLED fresh: token 31 0.18 vs -0.18"},
 {"id": "m08_gap_log10", "description": "gap uses log10", "killed_by": "KILLED fresh: token 31 -0.08 vs -0.18"},
]

notes = [
 "Ruling 37: no new mutants were authored. The 16 standing lab-2 mutants and the 5 correct alternatives were re-run (out/r1_standing_mutants.out, total 21). Result: 14 killed, 5 alternatives pass, 2 documented survivors (r4_m05, m02) that project.html line 45 documents as not separated by the instant check.",
 "Round-1 FAIL rows re-verified from scratch and now PASS: cards-c033-missing-hypothesis, cards-c034-missing-hypothesis (Proposition 2.4 hypothesis now stated on the cards and the grades match), cards-lab-numbers (c034 no longer carries a C lab number), idx-prereq-build-status (E1 and M2 are built; the index now says only P0.1 is not released).",
 "New FAIL row idx-data-status-labs-simulated: index.html line 37 says 'The labs use SIMULATED numbers', but project Lab 3 reads the REAL H.15 term spread. Low severity; fix wording as in the row.",
 "Observation, not a row (not a ruling-26 kind): L08 why-it-matters (line 52) says 'a constant marginal propensity to consume between 0 and 1 (Definition 1.1)'. Definition 1.1 defines c as the MPC; the constraint 0 < c < 1 is Assumption A1 (line 64). Suggest '(Definition 1.1 and A1)'.",
 "Observation, not a row: E5-c033 and E5-c034 use 'whenever the average growth ... differ' as a sufficient condition. Proposition 2.4 (line 123) gives the exact iff for the average residuals given alpha != alpha'; the per-period residual may depend on alpha even when the averages match, so the cards are correct as stated (sufficient, not characterizing).",
 "Carried observations from round 1, unchanged subjects: E5-c099 says 'inflation is not stable (section 5)' where section 5 now reads 'inflation changes' (same claim); the L05 Part B line is printed as price_share while the docstring describes a price change per unit of a (value 1/(eta+nu)); E5-c135 is absent (ruling 2 allows gaps).",
 "Not checked: the blind rubric calibration (no E5 blind scorer file in ~/.fanout/blind/, ruling 23; base calibration rows carried); the live part of verify_refs was run only through the tool's own --unit E5 path; plain-curl access checks were not repeated; lesson prose of L01-L06 and cards not in the delta were not re-read (carried, byte-identical).",
 "tools/mutate_graders.py --unit E5 printed nothing and exited 0 (no grader mutant files directly under ledgers/E5/mutants/*.py); the lab-2 standing set is covered by run_standing_mutants.py.",
]
registry_flags = [
 "references/references.json blanchard2020macroeconomics: record year 2020 while curriculum yaml line 182 says '8th ed. (2021)'. The page prints no year in prose. Architect to decide; not verified here (the book cannot be read). Unchanged since the base pin.",
 "curriculum/02-economics-finance-core.yaml lines 186-187 still say the brief uses series 'from Atlas'; the page uses no Atlas series (architect decision B2). Unchanged since the base pin.",
 "plans/E5-open-items.md NOTATION_REQUESTS names u^{\\ast} for the natural rate of unemployment; the page and L06 use u^n. Stale planning note.",
 "i^{\\ast} is the IS-LM equilibrium rate in L04 and the Taylor-rule value on project.html; i^{\\ast} is not in notation.json, so this is not a registry violation. Architect to decide whether to rename one.",
]
freshness_flags = [
 "ledgers/E5/scripts/E5-d-r5/ and ledgers/E5/mutants/project-2-r5/ are cited as round-5 evidence and were added between 04626e9 and HEAD. Present and not re-run in this round (not in the closing delta's rows).",
 "plans/E5-open-items.md 'Slice b' log says the lab docstring round left printed output unchanged; the L04 print label did change. Plan log only.",
]
frag = {
 "unit": "E5", "slice": "E5-d", "round": 1,
 "verifier": "Claude Haiku 5.5, independent closing-delta verifier for E5-d, round 1 (ruling 30; did not build E5)",
 "pin": "2a805c83", "base": "95f3f8cb (round-1 fragment ~/.fanout/frags/F1-E5-d.round1.json; its own base 04626e9)",
 "checkout": "/Users/billyribeiro/.fanout/wt/verifyG1-E5-d",
 "scratch": "/tmp/e5d_r1",
 "verified_at": "2026-11-09",
 "verdict": "FAIL",
 "rows": ROWS, "mutants": mutants, "registry_flags": registry_flags, "freshness_flags": freshness_flags,
 "notes": notes,
 "summary": "",
}
n_pass = sum(1 for r in ROWS if r["status"] == "PASS"); n_fail = len(ROWS) - n_pass
frag["summary"] = (f"E5-d round 1 closing delta, pin 2a805c83 (base 95f3f8cb): verdict FAIL. {len(ROWS)} rows: {n_pass} PASS "
  f"(carried and fresh), {n_fail} FAIL. The four round-1 FAIL rows (cards-c033, cards-c034, cards-lab-numbers, idx-prereq-build-status) "
  "are re-verified PASS. One new FAIL (idx-data-status-labs-simulated): index.html line 37 says the labs use only SIMULATED numbers, "
  "but project Lab 3 reads the REAL term spread. All gates re-run on the pin pass. Standing mutants re-run: 14 killed, 5 alternatives pass, 2 documented survivors.")
out = sys.argv[1]
json.dump(frag, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("wrote", out, len(ROWS), "rows", n_pass, "pass", n_fail, "fail")
