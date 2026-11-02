import json, datetime
C = "Carried from round 17 (cited ranges byte-identical since pin 86c4a0b; delta hunks are project.html lines 237, 242, 362; grader/reference.py lines 4, 110; grader/test_project.py lines 561-571; tests/labs/M3/lab-M3-project-3.py line 73; cards.json ids c093, c102, c148, c182, c198, c199, c203 only):"
R = "Re-verified round 18 (run this round, see scripts/M3-d-r18/):"
rows = []
def row(i, check, loc, status, ev): rows.append({"id": i, "check": check, "location": loc, "status": status, "evidence": ev})
carry = [
 ("M3-d-R01","Lab 1 of project.html (interpretation and expected block) matches twin","course/modules/M/M3/project.html lines 131-137; tests/labs/M3/lab-M3-project-1.py","Lab 1 region untouched by the delta; run_labs M3 PASS (12/12) in ledgers/M3/scripts/M3-d-r18/v18_run_labs.log"),
 ("M3-d-R02","Project page rubric prose, lines 214-220","course/modules/M/M3/project.html lines 214-220","lines outside the delta hunks"),
 ("M3-d-R03","Lab 3 printed numbers recomputed independently","course/modules/M/M3/project.html lines 460-468","Lab 3 expected block unchanged; run_labs byte-identity PASS (v18_run_labs.log)"),
 ("M3-d-R04","Rubric line 289 claim","course/modules/M/M3/project.html line 289","line outside delta hunks"),
 ("M3-d-R05","Lab 1 and Lab 2 interpretation prose numbers","course/modules/M/M3/project.html interpretation paragraphs after Lab 1 and Lab 2","outside delta hunks"),
 ("M3-d-R06","Rubric line 469 claim","course/modules/M/M3/project.html line 469","outside delta hunks"),
 ("M3-d-R08","Rubric numbers and formulas at lines 481, 597, 635-637","course/modules/M/M3/project.html lines 481, 597, 635-637","outside delta hunks"),
 ("M3-d-R09","Rubric line 492 claim","course/modules/M/M3/project.html line 492","outside delta hunks"),
 ("M3-d-R10","Rubric lines 597, 622, 635-637","course/modules/M/M3/project.html lines 597, 622, 635-637","outside delta hunks"),
 ("M3-d-R11","Hours split and hub arithmetic","course/modules/M/M3/project.html lines 258-264; course/modules/M/M3/index.html","outside delta hunks; index.html unchanged"),
 ("M3-d-R13","Stopping-rule survivors r6d_m04, r11d_m02, r15d_m03 ruled non-violations","ledgers/M3/equivalent/*.py; project.html lines 233, 622, 660","equivalent folder unchanged; see R60 for the max_iter question"),
 ("M3-d-R18","Rubric lines 481, 492, 597, 635-637, 660","course/modules/M/M3/project.html lines 481, 492, 597, 635-637, 660","outside delta hunks"),
 ("M3-d-R19","Lesson 4 links, F1-F4 references, DAG","course/modules/M/M3/project.html Lesson 4 links","outside delta hunks; check_dag M3 PASS this round"),
 ("M3-d-R25","Project reading section and references/references.json","course/modules/M/M3/project.html reading section; references/references.json","outside delta hunks"),
 ("M3-d-R26","Rubric line 37 and lines 243-247","course/modules/M/M3/project.html line 37; lines 243-247","line 242 is in the delta; lines 243-247 unchanged (hunk is single line 242)"),
 ("M3-d-R28","Exemplar B annotations","course/modules/M/M3/project.html line 492","outside delta hunks"),
 ("M3-d-R34","Lab 2 docstring matches twin","course/modules/M/M3/project.html Lab 2 docstring (line 144)","outside delta hunks; run_labs PASS"),
 ("M3-d-R35","comparison_weights documented weights tests","course/modules/M/M3/grader/reference.py comparison_weights; grader/test_project.py","reference comparison_weights untouched; tests unchanged outside 561-571"),
 ("M3-d-R17","Grader test count and tolerance statements","course/modules/M/M3/grader/test_project.py lines 241-245, 319-326, 508, 552-560","outside the new test at 561-571; count itself re-verified in R46"),
 ("M3-d-R29","Cards c143, c145, c161, c165 unchanged and their cited lesson text unchanged","course/modules/M/M3/cards.json M3-c143, c145, c161, c165","card objects unchanged in the delta"),
 ("M3-d-R32","Card M3-c040 back vs L02 Misconception 1","course/modules/M/M3/cards.json M3-c040; course/modules/M/M3/L02.html","card unchanged in the delta"),
 ("M3-d-R36","Mutants r14d_m01..m03 killed","ledgers/M3/mutants/r14d_m01..m03","re-run: all 123 mutants killed (see R55)"),
 ("M3-d-R38","Card M3-c184 (Lab 1 composition claim) vs L02","course/modules/M/M3/cards.json M3-c184; course/modules/M/M3/L02.html","card unchanged in the delta"),
 ("M3-d-R39","Card M3-c183 vs L09 Proposition 3.3(a) and Example 3.6","course/modules/M/M3/cards.json M3-c183; course/modules/M/M3/L09.html","card unchanged in the delta"),
 ("M3-d-R41","Mutants r13d_m01, m02, m04, m05 killed","ledgers/M3/mutants","re-run in R55"),
 ("M3-d-R43","Mutant directory well formed","ledgers/M3/mutants","re-run in R61: new mutants are complete modules with one-line docstrings"),
 ("M3-d-R44","Labs twins run and match page code and expected blocks","tests/labs/M3/lab-M3-project-1..3.py; lab-M3-L01..L09","re-run: run_labs M3 PASS 12/12 (v18_run_labs.log); project-3 twin line 73 matches page code"),
 ("M3-d-R48","Mutants r15d_m01, r15d_m02 killed","ledgers/M3/mutants/r15d_m01, r15d_m02","re-run in R55"),
 ("M3-d-R50","Equivalent-mutant README and rubric statements","ledgers/M3/equivalent/README.md; project.html lines 233, 622, 660","README unchanged"),
 ("M3-d-R51","Mutants r16d_m01..m03 killed","ledgers/M3/mutants/r16d_m01..m03","re-run in R55"),
 ("M3-d-R52","Equivalence check of the three moved survivors","ledgers/M3/scripts/M3-d-r16/equiv_check.py","script unchanged"),
 ("M3-d-R53","Tolerance sensitivity check of the moved survivors","ledgers/M3/scripts/M3-d-r16/tol_check.py","script unchanged"),
 ("M3-d-R58","Changed and new cards (M3-c025, c031, c034, c050, c063, c064, c065, c067, c082, c119, c123, ...) vs lessons","course/modules/M/M3/cards.json; course/modules/M/M3/L02.html, L03.html, L04.html","these card objects unchanged in the delta"),
 ("M3-d-R59","No process words, notation conflicts, or DAG drift in changed cards","course/modules/M/M3/cards.json; notation/notation.json","cards c093, c182, c198, c199, c203 re-read in R22/R64/R65: no process words, F1-F4 and Definition/Theorem names exist in the lessons"),
 ("M3-d-R47","Card M3-c127 agrees with the current L07 misconception text","course/modules/M/M3/cards.json M3-c127; course/modules/M/M3/L07.html","unchanged"),
 ("M3-d-R49","Card M3-c175 front matches the current L09 Lab 1 criterion","course/modules/M/M3/cards.json M3-c175; course/modules/M/M3/L09.html","unchanged"),
 ("M3-d-R24","Lesson hunks cited by changed cards agree with card text","course/modules/M/M3/L07.html line 198","L07 not in the delta"),
]
for i, ch, loc, ev in carry:
    st = "PASS"
    row(i, ch, loc, st, ("Carried from round 17 (files byte-identical since the previous pin 86c4a0b for the cited subject): " if "re-" not in ev else "") + ev if not ev.startswith("re-") else ev)
row("M3-d-R12","Reference passes 50/50 seeds; slowest run","course/modules/M/M3/grader/reference.py; tools/run_graders.py","PASS",R+" run_graders M3 PASS reference 50/50 seeds, slowest 0.2 s (ledgers/M3/scripts/M3-d-r18/v18_run_graders.log)")
row("M3-d-R14","Six alternative correct implementations pass the grader","ledgers/M3/alternatives/alt1..alt6","PASS",R+" 6/6 alternatives pass 50/50 seeds with the current test file, alt2 (honours max_iter) included (ledgers/M3/scripts/M3-d-r18/v18_alts.log)")
row("M3-d-R15","Mutant files are complete modules, one-line docstring each","ledgers/M3/mutants/*.py","PASS",R+" 120 existing and 3 new mutants all open with a one-line docstring and run through mutate_graders (v18_mutate_all_new.log)")
row("M3-d-R16","Grader spec of is_psd, clip_repair, comparison_weights matches reference","course/modules/M/M3/grader/reference.py lines 96-131; project.html line 361","PASS",R+" signatures at project.html line 361 unchanged (only docstring line 362 changed); reference is_psd and weights bodies unchanged")
row("M3-d-R20","check_pages, check_dag, check_projects, page_smoke for the project page","tools/check_pages.py, check_dag.py, check_projects.py, page_smoke.py","PASS",R+" check_pages --all, check_dag --all, check_projects --all exit 0 with M3 PASS; page_smoke --unit M3 PASS (v18_check_*.log, v18_page_smoke.log)")
row("M3-d-R07","Rubric lines 233-237 claims","course/modules/M/M3/project.html lines 233-237","PASS",R+" line 233 signature projection_repair(matrix, tol=1e-10, max_iter=500) unchanged; line 237 test count now 155, matching collect-only (R46)")
row("M3-d-R21","cards.json structure: unique ids, lessons exist, cites","course/modules/M/M3/cards.json (200 cards)","PASS",R+" 200 cards, 0 duplicate ids, lessons L01-L09 only; card M3-c102 and M3-c148 removed with no dangling references in the delta")
row("M3-d-R22","Changed and carried cards: content matches the current lesson","course/modules/M/M3/cards.json M3-c093, c182, c198, c199, c203","PASS",R+" c093 eigenvalues 0,1,3 and (1,1,-1) null vector recomputed with numpy (v18 check: eigh gives [0,1,3]; G@(1,1,-1)=0); c182 eps=0 clipping matches L09 Definition 3.1 and Method 2 at L09 line 187; c198/c199 cite L08 Definition 1.3 and F1-F4 in L04; c203 cites L05 Proposition 1.5 (line 76), Theorem 2.2 (line 119, requires strictly positive eigenvalues, line 498) and Remark 3.2 (line 171)")
row("M3-d-R23","Grade counts and basis rule","course/modules/M/M3/cards.json grade counts","PASS",R+" grade counts now T=114, C=39, ungraded=47 (total 200); new c203 is T with a stated proposition and theorem")
row("M3-d-R30","Card numbers appear in their lesson text","course/modules/M/M3/cards.json (200 cards) against L01..L09","PASS",R+" cited numbers for changed cards exist: Remark 3.2 and Proposition 1.5 and Theorem 2.2 in L05; Definition 3.1 in L09 and L08; Definition 1.3 in L08; F1-F4 in L04")
row("M3-d-R33","Card M3-c093 back vs L05 text","course/modules/M/M3/cards.json M3-c093; course/modules/M/M3/L05.html line 177","PASS",R+" back now '0, 1 and 3 (Remark 3.2)'; L05 line 177 states Remark 3.2 has eigenvalues 0, 1 and 3; numpy eigh of B^T B gives [0,1,3]")
row("M3-d-R37","Alternatives pass and every mutant is killed","ledgers/M3/alternatives/; ledgers/M3/mutants","PASS",R+" 6/6 alternatives 50/50 seeds; mutate_graders M3 120/120 existing killed plus 3/3 new")
row("M3-d-R40","Mutation gate: every grader mutant fails the suite","tools/mutate_graders.py --unit M3","PASS",R+" mutate_graders --unit M3 --seeds 0-9: PASS 123/123 killed (v18_mutate_all_new.log); seeds 0-49 not re-run, each kill is at seed 0")
row("M3-d-R55","Mutation gate over the full M3 mutant set (current count)","tools/mutate_graders.py --unit M3; ledgers/M3/mutants","PASS",R+" 123 mutants (120 existing + v18_m01..m03) all killed")
row("M3-d-R56","Grader kills a projection_repair that ignores max_iter","course/modules/M/M3/grader/test_project.py lines 561-571; ledgers/M3/mutants/r17d_m02_*.py","PASS",R+" r17d_m02 now killed by test_projection_repair_honours_max_iter; v18_m02 (cap at max(max_iter,500)) also killed by the same test")
row("M3-d-R42","Alternatives pass 50/50","ledgers/M3/alternatives/","PASS",R+" 6/6 pass 50/50 (v18_alts.log)")
row("M3-d-R45","Repo ruff, mypy and targeted pytest","repo root; M3 files","PASS",R+" ruff check and ruff format --check on course/modules/M/M3/grader and tests/labs/M3 clean; mypy --no-incremental on reference.py and instance.py: no issues")
row("M3-d-R46","Test count on page equals collect-only count","course/modules/M/M3/project.html line 237 ('155 tests'); grader/test_project.py","PASS",R+" collect-only on reference-workspace: '155 tests collected' (v18_collect.log); page line 237 says 155")
row("M3-d-R57","Card M3-c182 states Method 2 as the lesson and the code do","course/modules/M/M3/cards.json M3-c182; course/modules/M/M3/L09.html line 187","PASS",R+" back now says eigenvalue-clip X at zero (Definition 3.1 with epsilon=0); L09 line 187 says 'Definition 3.1 with epsilon=0' and the reference clip step is an eigenvalue clip (reference.py _psd_projection)")
row("M3-d-R60","Test test_projection_repair_honours_max_iter must not reject a correct non-iterative implementation","course/modules/M/M3/grader/test_project.py lines 561-571; course/modules/M/M3/project.html line 233","FAIL","The new test requires projection_repair(corr, max_iter=1) to differ from projection_repair(corr) by more than 1e-6 on INST and INST2. project.html line 233 defines projection_repair(matrix, tol=1e-10, max_iter=500) only as 'an approximation of the matrix nearest to the input in the Frobenius distance ... symmetric, PSD, unit diagonal'; the page never says max_iter caps the alternating steps (only line 660 asks the learner to vary max_iter). A correct solver that computes the nearest matrix by another method and ignores max_iter yields gap 0 and fails. Not run: an exact non-iterative alternative was not built this round (reasoning only). Fix: state on project.html line 233 that max_iter is the maximum number of alternating-projection steps, or drop the test and rely on the iteration-count reading at line 660 only.")
row("M3-d-R61","Three new student-error mutants written and killed","ledgers/M3/mutants/v18_m01..v18_m03; ledgers/M3/scripts/M3-d-r18/v18_make_mutants.py","PASS",R+" v18_m01 is_psd by Cholesky refuses singular PSD (killed by test_non_square_is_refused[...-is_psd] at seed 0); v18_m02 loop cap max(max_iter,500) (killed by test_projection_repair_honours_max_iter); v18_m03 clip_repair skips rescaling on unit-diagonal input (killed by test_clip_repair_has_unit_diagonal_and_is_symmetric)")
row("M3-d-R62","Convention line 242 (unit-diagonal instances built by make_instance)","course/modules/M/M3/project.html line 242; course/modules/M/M3/grader/instance.py","PASS",R+" make_instance(seed) for seeds 0-49: 0 seeds with a non-unit corr diagonal (v18 check); the revised sentence says each instance built by make_instance is unit-diagonal, which holds")
row("M3-d-R63","Reference docstring and project-3 twin wording (Dykstra replaced) matches the code","course/modules/M/M3/grader/reference.py lines 4, 110; tests/labs/M3/lab-M3-project-3.py line 73; project.html line 362","PASS",R+" the algorithm keeps corr_s and corr_u correction terms (reference.py lines 112-127), so 'alternating projections with correction terms' is accurate; no 'Dykstra' string remains in course/modules/M/M3 or tests/labs/M3")
row("M3-d-R64","Project page count sentence and new max_iter test description agree","course/modules/M/M3/project.html line 237; test_project.py 561-571","PASS",R+" 155 tests and 'the use of its max_iter argument' match the collected test")
row("M3-d-R65","Hours and cross-references in changed hunks","course/modules/M/M3/project.html lines 237, 242, 362","PASS",R+" no hours or figure changed in these hunks")
mutants = [
 {"id":"v18_m01_is_psd_cholesky_refuses_singular","description":"is_psd decides by a Cholesky factorisation without tolerance, so a PSD matrix with a zero eigenvalue is refused.","killed_by":"test_non_square_is_refused[two_rows_three_columns-is_psd] (seed 0) and planted-zero-eigenvalue tests"},
 {"id":"v18_m02_projection_loop_cap_ignores_small_max_iter","description":"projection_repair runs max(max_iter, 500) iterations.","killed_by":"test_projection_repair_honours_max_iter (seed 0)"},
 {"id":"v18_m03_clip_skips_rescale_on_unit_diagonal","description":"clip_repair skips rescaling when the input diagonal is all ones.","killed_by":"test_clip_repair_has_unit_diagonal_and_is_symmetric[seed] (seed 0)"},
]
frag = {
 "unit":"M3","slice":"d","round":18,
 "verifier":"independent verifier (Claude Haiku 5.5), unit M3 slice d, round 18",
 "pin":"8f80909","base":"round-17 fragment /Users/billyribeiro/.fanout/frags/B-M3-d.round17.json (pin 86c4a0b)",
 "checkout":"/Users/billyribeiro/.fanout/wt/verifyB18-M3-d","scratch":"ledgers/M3/scripts/M3-d-r18/",
 "verified_at":datetime.datetime.now(datetime.timezone.utc).isoformat(),
 "verdict":"FAIL","rows":rows,"mutants":mutants,"registry_flags":[],"freshness_flags":[],
 "notes":"Delta 86c4a0b..8f80909 for slice d: project.html (lines 237, 242, 362), grader/reference.py (lines 4, 110), grader/test_project.py (new test lines 561-571), tests/labs/M3/lab-M3-project-3.py (line 73), cards.json (c093, c102 and c148 removed, c182, c198, c199 edited, c203 added). Not run this round: mutate_graders at seeds 0-49 (ran 0-9); a non-iterative exact-solver alternative (R60 reasoning only); card-level rechecks of unchanged cards relied on the round-17 carry.",
 "summary":"M3 slice d round 18: FAIL. One non-PASS row: M3-d-R60, the new test_projection_repair_honours_max_iter demands an iteration-cap meaning for max_iter that project.html line 233 does not state, so a correct non-iterative nearest-matrix solver would fail. Fix: state the max_iter meaning on line 233 or relax the test. All six alternatives pass 50/50 seeds (alt2 included), all 120 existing and 3 new mutants are killed, the page count 155 matches collect-only, and the cards c093, c182, c198, c199, c203 agree with their lessons. Fragment: ledgers/M3/M3-d.json."
}
json.dump(frag, open("ledgers/M3/M3-d.json","w"), indent=1, ensure_ascii=False)
print(len(rows), sum(r['status']=='PASS' for r in rows))
