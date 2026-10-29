import json, datetime
CARRY = "Carried from round 16 (files byte-identical since the previous pin 5e88c50): "
RERUN = "Re-run this round at pin 86c4a0b: "
rows = []
def row(id_, check, location, status, evidence, fix=None):
    r = {"id": id_, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    rows.append(r)

P = "course/modules/M/M3/"
carry_specs = {
 "M3-d-R01": ("Lab 1 of project.html (interpretation and expected block) matches twin", P+"project.html lines 131-137; tests/labs/M3/lab-M3-project-1.py", "project.html and lab-M3-project-1.py unchanged; run_labs M3 re-run PASS 12/12 (ledgers/M3/scripts/M3-d-r17/run_labs_M3.log)"),
 "M3-d-R02": ("Project page rubric prose, lines 214-220", P+"project.html lines 214-220", "project.html unchanged since 5e88c50 (git diff --stat empty)"),
 "M3-d-R03": ("Lab 3 printed numbers recomputed independently", P+"project.html lines 460-468", "project.html and lab-M3-project-3.py unchanged; numbers_check.py from round 13 unchanged"),
 "M3-d-R04": ("Rubric line 289 claim", P+"project.html line 289", "project.html unchanged"),
 "M3-d-R05": ("Lab 1 and Lab 2 interpretation prose numbers", P+"project.html interpretation paragraphs after Lab 1 and Lab 2", "project.html unchanged"),
 "M3-d-R06": ("Rubric line 469 claim", P+"project.html line 469", "project.html unchanged"),
 "M3-d-R07": ("Rubric lines 233-237 claims", P+"project.html lines 233-237", "project.html unchanged; line 233 signatures re-read this round (projection_repair(matrix, tol=1e-10, max_iter=500))"),
 "M3-d-R08": ("Rubric numbers and formulas at lines 481, 597, 635-637", P+"project.html lines 481, 597, 635-637", "project.html unchanged"),
 "M3-d-R09": ("Rubric line 492 claim", P+"project.html line 492", "project.html unchanged"),
 "M3-d-R10": ("Rubric lines 597, 622, 635-637", P+"project.html lines 597, 622, 635-637", "project.html unchanged; line 622 'The suite checks the result, not the stopping rule' re-read"),
 "M3-d-R11": ("Hours split and hub arithmetic", P+"project.html lines 258-264; "+P+"index.html line 42", "project.html and index.html unchanged"),
 "M3-d-R13": ("Stopping-rule survivors r6d_m04, r11d_m02, r15d_m03 ruled non-violations", "ledgers/M3/equivalent/*.py; project.html lines 233, 622, 660", "equivalent/ and project.html unchanged; the ruling covers tol only; the separate max_iter defect is M3-d-R56"),
 "M3-d-R14": ("Six alternative correct implementations pass the grader", "ledgers/M3/alternatives/alt1..alt6", RERUN+"run_alts17.sh over alt1..alt6 with the current grader: pass=50 fail=0 for each (ledgers/M3/scripts/M3-d-r17/alts_r17.out)"),
 "M3-d-R12": ("Reference passes 50/50 seeds; slowest run", P+"grader/reference.py; tools/run_graders.py", RERUN+"tools/run_graders.py --unit M3 --seeds 0-49 -> 'run_graders M3: PASS (reference 50/50 seeds, slowest 0.2 s)' exit 0 (run_graders_M3.log)"),
 "M3-d-R15": ("Mutant files are complete modules, one-line docstring each", "ledgers/M3/mutants/*.py", RERUN+"120 files now (117 earlier plus r17d_m01..m03); each opens with a one-line docstring (checked by reading the 3 new files)"),
 "M3-d-R16": ("Grader spec of is_psd, clip_repair, comparison_weights matches reference", P+"grader/reference.py lines 96-131; project.html line 361", "grader and project.html unchanged since 5e88c50"),
 "M3-d-R17": ("Grader test count and tolerance statements", P+"grader/test_project.py lines 241-245, 319-326, 508, 552-560; project.html line 237", "grader and project.html unchanged"),
 "M3-d-R18": ("Rubric lines 481, 492, 597, 635-637, 660", P+"project.html lines 481, 492, 597, 635-637, 660", "project.html unchanged"),
 "M3-d-R19": ("Lesson 4 links, F1-F4 references, DAG", P+"project.html Lesson 4 links; check_dag output", RERUN+"tools/check_dag.py --all -> check_dag M3: PASS (ledgers/M3/scripts/M3-d-r17/check_dag.log)"),
 "M3-d-R20": ("check_pages, check_dag, check_projects, page_smoke for the project page", "tools/check_pages.py, check_dag.py, check_projects.py, page_smoke.py", RERUN+"check_pages --all, check_dag --all, check_projects --all all exit 0 with M3 PASS; page_smoke --unit M3 --pages modules/M/M3/project.html --skip-labs: 'page_smoke M3: PASS' exit 0"),
 "M3-d-R25": ("Project reading section and references/references.json", P+"project.html reading section; references/references.json", "project.html and references unchanged"),
 "M3-d-R26": ("Rubric line 37 and lines 243-247", P+"project.html line 37; lines 243-247", "project.html unchanged"),
 "M3-d-R27": ("Lab 3 expected block equals twin output", P+"project.html Lab 3 expected block; tests/labs/M3/lab-M3-project-3.py", "project.html and twin unchanged; run_labs M3 PASS"),
 "M3-d-R28": ("Exemplar B annotations", P+"project.html line 492", "project.html unchanged"),
 "M3-d-R31": ("Hours arithmetic and Lab 3 interpretation cross-references", P+"project.html lines 258-264 and 469", "project.html unchanged"),
 "M3-d-R32": ("Card M3-c040 back vs L02 Misconception 1", P+"cards.json M3-c040; "+P+"L02.html", "cards.json entry and L02.html unchanged (not in the 5e88c50..86c4a0b diff)"),
 "M3-d-R33": ("Card M3-c093 back vs L05 text", P+"cards.json M3-c093; "+P+"L05.html", "cards.json entry and L05.html unchanged"),
 "M3-d-R34": ("Lab 2 docstring matches twin", P+"project.html Lab 2 docstring (line 144)", "project.html unchanged"),
 "M3-d-R35": ("comparison_weights documented weights tests", P+"grader/reference.py comparison_weights; grader/test_project.py weights tests", "grader unchanged"),
 "M3-d-R36": ("Mutants r14d_m01..m03 killed", "ledgers/M3/mutants/r14d_m01..m03", RERUN+"mutate_graders.py --unit M3 --seeds 0-49 (ledgers/M3/scripts/M3-d-r17/mutate_m3_r17_with_new.out): all three KILLED"),
 "M3-d-R38": ("Card M3-c184 (Lab 1 composition claim) vs L02", P+"cards.json M3-c184; "+P+"L02.html", "cards.json entry and L02.html unchanged; L02 twin not changed"),
 "M3-d-R39": ("Card M3-c183 vs L09 Proposition 3.3(a) and Example 3.6", P+"cards.json M3-c183; "+P+"L09.html", "card unchanged; L09.html diff (5e88c50..86c4a0b) touches only line 391 (Problem M2 solution), not Proposition 3.3 or Example 3.6; 0.04 matches entries -0.1 and 0.1"),
 "M3-d-R41": ("Mutants r13d_m01, m02, m04, m05 killed", "ledgers/M3/mutants", RERUN+"full mutate run: all four KILLED"),
 "M3-d-R42": ("Alternatives pass 50/50", "ledgers/M3/alternatives/", RERUN+"alt1..alt6 pass=50 fail=0 each"),
 "M3-d-R43": ("Mutant directory well formed (file absent at earlier pin)", "ledgers/M3/mutants", "directory present with 120 files; mutate gate loads all of them"),
 "M3-d-R44": ("Labs twins run and match page code and expected blocks", "tests/labs/M3/lab-M3-project-1..3.py; lab-M3-L01..L09", RERUN+"run_labs.py --unit M3 -> 'run_labs M3: PASS (12/12)'; lab-M3-L07-1 and lab-M3-L09-1 twins re-run under python -I -W error, exit 0 (twin_L07.out, twin_L09.out)"),
 "M3-d-R45": ("Repo ruff, mypy and targeted pytest", "repo root; M3 files", RERUN+"ruff check . -> All checks passed; ruff format --check on M3 grader and labs -> 16 files already formatted; mypy --no-incremental -> Success, 255 source files; pytest tests/test_labs.py tests/test_page_smoke.py tests/test_page_checks.py tests/test_run_labs.py -> exit 0"),
 "M3-d-R46": ("Test count on page equals collect-only count", P+"project.html line 237 ('154 tests'); grader/test_project.py", RERUN+"collect-only in a scratch copy with reference.py as covariance_doctor.py: 154 tests collected; project.html line 237 says 154"),
 "M3-d-R48": ("Mutants r15d_m01, r15d_m02 killed", "ledgers/M3/mutants/r15d_m01, r15d_m02", RERUN+"full mutate run: both KILLED"),
 "M3-d-R50": ("Equivalent-mutant README and rubric statements", "ledgers/M3/equivalent/README.md; project.html lines 233, 622, 660", "equivalent/ and project.html unchanged"),
 "M3-d-R51": ("Mutants r16d_m01..m03 killed", "ledgers/M3/mutants/r16d_m01_is_psd_tolerance_scaled_by_spectrum.py; r16d_m02_min_eigenvalue_prints_its_value.py; r16d_m03_clip_repair_writes_back_into_argument.py", RERUN+"full mutate run: all three KILLED (seed 0)"),
 "M3-d-R52": ("Equivalence check of the three moved survivors", "ledgers/M3/scripts/M3-d-r16/equiv_check.py", "script unchanged since round 16; its output is not reproduced this round, so the 1e-11 figures are carried, not re-measured"),
 "M3-d-R53": ("Tolerance sensitivity check of the moved survivors", "ledgers/M3/scripts/M3-d-r16/tol_check.py", "script unchanged since round 16; carried"),
}
for id_, (check, loc, ev) in carry_specs.items():
    if ev.startswith("Re-run") or ev.startswith(RERUN):
        row(id_, check, loc, "PASS", ev)
    else:
        row(id_, check, loc, "PASS", CARRY + ev)

# Rows whose subject changed this round: re-verified
row("M3-d-R21", "cards.json structure: unique ids, lessons exist, cites, every lesson has cards", P+"cards.json (201 cards)", "PASS",
    RERUN+"python check over course/modules/M/M3/cards.json: 201 cards, 201 unique ids, 0 duplicate fronts, 0 duplicate backs; lessons L01..L09 each have 15 to 28 cards; grades T 114, C 39, none 48; every C card has a basis (39 of 39)")
row("M3-d-R22", "Changed and carried cards: content matches the current lesson", P+"cards.json c126, c127, c175 and the 16 new cards M3-c187..c202; carried cards c054, c135, c147, c185", "PASS",
    RERUN+"c126 and c127 re-read against L07.html (line 198: printed 0.8951; line 219-area misconception text) and the twin output; c175 against L09 Lab 1 (see R49); byte-identical carried cards not in the diff.")
row("M3-d-R23", "Grade counts and basis rule", P+"cards.json (grade counts)", "PASS",
    RERUN+"Counter over 201 cards: T 114, C 39, no grade 48; C cards without basis: none")
row("M3-d-R24", "Lesson hunks cited by changed cards agree with card text", P+"L07.html line 198 (Lab 1 interpretation, changed this round), line 131; cards c126, c127, c124, c125, c177", "PASS",
    RERUN+"L07 line 198 now reads 'assuming F1 to F4 ... the proofs above cover every full-column-rank design' and 'A^T A has rank 2 of 3'; the twin prints rank 2 (of 3), 1.3325 0.8488 -0.4120, residual 0.8951 (twin_L07.out); cards c124-c127 and c177 agree")
row("M3-d-R29", "Cards c143, c145, c161, c165 unchanged and their cited lesson text unchanged", P+"cards.json M3-c143, c145, c161, c165; "+P+"L09.html", "PASS",
    CARRY+"cards byte-identical in 5e88c50..86c4a0b; c161 cites Lab 1 printed output, which twin_L09.out reproduces (eigenvalues -0.800000 1.900000 1.900000, distance 0.6400000000); c165 cites Example 3.6 and Proposition 3.2(a), unchanged")
row("M3-d-R30", "Card numbers appear in their lesson text", P+"cards.json (201 cards) against L01..L09 text", "PASS",
    RERUN+"script over every decimal and integer >= 10 in front, back and basis of all 201 cards, mapped to its own lesson text (10^-k accepted as 1e-k): 0 absent; script ledgers/M3/scripts/M3-d-r17/card_refs.py also checks Definition/Theorem/Lemma/Proposition/Corollary/Remark/Problem/Fact references: the only literal misses are 'Section 1' on M3-c130, M3-c197 and M3-c115, which name the numbered section headings '1 Centred data...' (L08) and of L07, read by hand; no other changed or new card has a missing reference")
row("M3-d-R47", "Card M3-c127 agrees with the current L07 misconception text", P+"cards.json M3-c127; "+P+"L07.html", "PASS",
    RERUN+"c127 back ('residual is orthogonal to the columns of A, not zero'; norm 0.8951) matches L07 text (line 127 area: 'the residual is orthogonal to the columns of A, not zero ... Lab 1 prints a residual norm of 0.8951')")
row("M3-d-R49", "Card M3-c175 front matches the current L09 Lab 1 criterion", P+"cards.json M3-c175 (front); "+P+"L09.html Lab 1 description and printed line", "PASS",
    RERUN+"c175 front now states is_correlation (symmetric and unit diagonal to 1e-12, smallest eigenvalue at least -1e-8); twin lab-M3-L09-1.py defines is_correlation with TOL=1e-12, FEASIBLE_TOL=1e-8 and prints '...passes is_correlation (...): 23 of 23' with 23 non-PSD (threshold -1e-9); c175 back 'All 23 of 23' matches")
row("M3-d-R54", "Card numbers appear in their lesson; no duplicate cards", P+"cards.json (201 cards)", "PASS",
    RERUN+"duplicate-id and duplicate-front check: none; numeric-token check over 201 cards: 0 absent (same script as R30)")

# New FAIL rows and gate rows
row("M3-d-R37", "Alternatives pass and every mutant is killed", "ledgers/M3/alternatives/; ledgers/M3/mutants (120 files)", "FAIL",
    RERUN+"alternatives 6/6 at 50/50 seeds PASS; but mutate_graders --unit M3 --seeds 0-49 reports 'mutate_graders M3: FAIL (119/120 killed)': r17d_m02_projection_repair_ignores_max_iter_argument SURVIVED (ledgers/M3/scripts/M3-d-r17/mutate_m3_r17_with_new.out line 87)",
    "Add a grader test that projection_repair honours max_iter (see M3-d-R56 fix); then re-run tools/mutate_graders.py --unit M3 --seeds 0-49 and require 120/120 killed.")
row("M3-d-R40", "Mutation gate: every grader mutant fails the suite", "tools/mutate_graders.py --unit M3 --seeds 0-49", "FAIL",
    RERUN+"exit 1, 119/120 killed; sole survivor r17d_m02 (see M3-d-R56)",
    "Kill r17d_m02 with a max_iter test (M3-d-R56 fix), then re-run the gate to 120/120.")
row("M3-d-R55", "Mutation gate over the full M3 mutant set (current count)", "tools/mutate_graders.py --unit M3 --seeds 0-49; ledgers/M3/mutants", "FAIL",
    RERUN+"'mutate_graders M3: FAIL (119/120 killed)'; the 117 earlier mutants and r17d_m01 and r17d_m03 are KILLED",
    "See M3-d-R56.")
row("M3-d-R56", "Grader kills a projection_repair that ignores max_iter", P+"grader/reference.py line 109 (signature max_iter=500) and line 367 (range(max_iter)); "+P+"grader/test_project.py lines 552-557; "+P+"project.html line 233 (signature) and line 660 (stretch exercise: report how the repair changes with max_iter)", "FAIL",
    RERUN+"ledgers/M3/mutants/r17d_m02_projection_repair_ignores_max_iter_argument.py (loop hard-coded to range(500)) passes all tests on seeds 0-49 (SURVIVED). The max_iter parameter is stated in the signature at project.html line 233 and the stretch at line 660 asks the student to report how the repair changes with max_iter. Measured: reference projection_repair(max_iter=1) differs from max_iter=500 by 0.056, 0.119, 0.079 on seeds 0, 1, 2 and by up to 0.155 over seeds 0-49, so a max_iter test can kill the mutant.",
    "Add a test in grader/test_project.py: on a seeded instance where max_iter=1 does not converge, assert that projection_repair(corr, max_iter=1) differs from projection_repair(corr, max_iter=500) by more than 1e-6 (or equals one Dykstra pass). Then re-run run_graders and mutate_graders and confirm r17d_m02 is KILLED.")
row("M3-d-R57", "Card M3-c182 states Method 2 as the lesson and the code do", P+"cards.json M3-c182; "+P+"L09.html line 92 (Method 2); tests/labs/M3/lab-M3-L09-1.py alternating_projections", "FAIL",
    "The card says 'clip X at zero to get Y'. The lesson says 'eigenvalue-clip X at zero (Definition 3.1 with epsilon = 0)' and the twin's clip_eigenvalues takes the spectral decomposition. Entrywise clipping at zero is a different operation, so the card as written describes a different algorithm. The stopping rule (below 1e-12 or 500 steps, MAX_ITER = 500, TOL = 1e-12) and 'unit diagonal by construction' agree with the lesson and code.",
    "Change the back of M3-c182 to: 'it starts from X = A and repeats: eigenvalue-clip X at zero (Definition 3.1 with epsilon = 0) to get Y, and set every diagonal entry of Y to 1, stopping when the largest entrywise change from X to Y is below 10^-12 or after 500 steps. The output W has unit diagonal by construction.'")
row("M3-d-R58", "Changed and new cards (M3-c025, c031, c034, c050, c063, c064, c065, c067, c082, c119, c123, c130, c133, c134, c136, c175, c187..c202) agree with their lessons", P+"cards.json; "+P+"L02.html, L03.html, L04.html, L05.html, L07.html, L08.html, L09.html", "PASS",
    RERUN+"each card read against its lesson's definition, theorem, proposition or corollary: statements, hypotheses (F1 to F4, independence of columns, bases), numbering and grades agree; the one exception, M3-c182, is recorded at M3-d-R57. The split cards are consistent: M3-c025 (kernel) and M3-c187 (image); M3-c050 and M3-c188; M3-c063 and c189; M3-c064 and c190; M3-c065 and c190/c189 with no duplicate fact; M3-c082 and c193; M3-c119 with c194/c195; M3-c123 with c196; M3-c130 and c197; M3-c133 with c198/c199; M3-c134 and c200; M3-c136 and c201; M3-c175 (see R49); M3-c182 and c202")
row("M3-d-R59", "No process words, notation conflicts, or DAG drift in changed cards", P+"cards.json; notation/notation.json", "PASS",
    RERUN+"grep for process words (verif, round, builder, agent, reviewer, fix, previous) in all card text: no matches; symbols used in changed cards (T, M, X~, Z, Lambda, W, P, G, C0, R, v_k, s_k) checked against notation/notation.json: registered symbols T (number of observations) used consistently; no other registered symbol used; check_dag M3: PASS")

frag = {
 "unit": "M3", "slice": "d", "round": 17,
 "verifier": "independent verifier (Claude Haiku 5.5), unit M3 slice d, round 17",
 "pin": "86c4a0b",
 "base": "round-16 fragment /Users/billyribeiro/.fanout/frags/B-M3-d.round16.json (pin 5e88c50)",
 "checkout": "/Users/billyribeiro/.fanout/wt/verifyB17-M3-d",
 "scratch": "ledgers/M3/scripts/M3-d-r17/",
 "verified_at": datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat(),
 "verdict": "FAIL",
 "rows": rows,
 "mutants": [
  {"id": "r17d_m01_comparison_weights_normalised_by_largest_entry", "description": "comparison_weights normalises by the largest solution entry instead of by the sum, so the weights do not sum to one.", "killed_by": "test_lab3_reference_numbers_are_matched (seed 0)"},
  {"id": "r17d_m02_projection_repair_ignores_max_iter_argument", "description": "projection_repair hard-codes 500 iterations and ignores its max_iter argument.", "killed_by": ""},
  {"id": "r17d_m03_rescale_divides_only_by_row_diagonal", "description": "_rescale divides entry (i, j) by the square root of the diagonal of row i alone, so the result is not symmetric.", "killed_by": "test_clip_repair_has_unit_diagonal_and_is_symmetric (seed 0)"},
 ],
 "registry_flags": [],
 "freshness_flags": [
  "Round-17 delta from pin 5e88c50 to 86c4a0b for slice d: course/modules/M/M3/cards.json (rewritten and split: 16 new cards M3-c187..c202; changed c025, c031, c034, c050, c063, c064, c065, c067, c082, c119, c123, c130, c133, c134, c136, c175, c182); course/modules/M/M3/L07.html (lines 198, 121-area canon-breaks paragraph); course/modules/M/M3/L09.html (line 391, Problem M2 solution). project.html, grader/*, tests/labs/M3/lab-M3-project-1..3.py and tools/* are byte-identical since 5e88c50 (git diff --stat empty). ledgers/M3/mutants gained r16d_m01..m03 (already in the r16 gate) and this round adds r17d_m01..m03 in my checkout only."
 ],
 "notes": [
  "Verdict FAIL is driven by R56 (grader survivor r17d_m02: projection_repair ignores max_iter; the signature at project.html line 233 and the stretch at line 660 state max_iter as a working parameter), and by R57 (card M3-c182 says 'clip X at zero' where the lesson and code eigenvalue-clip). The mutation gate, alternatives and R40/R55/R37 follow from R56.",
  "Card M3-c162 (not-PSD count 23) does not state the -1e-9 threshold the lab uses; the card is unchanged since round 16 and is carried PASS, with the note that the threshold appears only in the printed lab line and the lab code.",
  "The round-16 mutants r6d_m04, r11d_m02, r15d_m03 remain under ledgers/M3/equivalent/ and their ruling is not revisited here; the new max_iter survivor is a separate defect.",
  "Not checked: the 120-second browser run limit (project.html line 235) was not timed; the full repo pytest suite, build_site and render_curriculum and verify_refs were not run (outside the targeted set for this slice); equiv_check.py and tol_check.py were not re-executed this round (carried from round 16); L01 and L06 cards were not re-read, they are byte-identical and their lessons unchanged.",
  "Tool note: the first run of the mutation gate in this round was launched in the background; its reported output is the foreground-equivalent re-run in mutate_m3_r17_with_new.out (119/120, exit 1)."
 ],
 "summary": "M3 slice d round 17: FAIL. 2 gate-level defects: M3-d-R56 (grader survivor r17d_m02, max_iter ignored; fix: max_iter test) and M3-d-R57 (card M3-c182 'clip X at zero' vs lesson's eigenvalue clipping; fix given). Changed/new cards otherwise agree with their lessons (M3-d-R58); M3-c175 PASS (R49 cleared). Reference 50/50, 154 tests, alternatives 6/6 at 50/50, run_labs 12/12, ruff/mypy/pytest targeted clean, check_pages/dag/projects PASS, page_smoke PASS.",
}
out = "/Users/billyribeiro/.fanout/wt/verifyB17-M3-d/ledgers/M3/M3-d.json"
json.dump(frag, open(out, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
print("rows", len(rows), "non-pass", [r["id"] for r in rows if r["status"] != "PASS"])
