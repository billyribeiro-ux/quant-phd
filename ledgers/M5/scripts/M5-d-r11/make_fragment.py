import json, pathlib, datetime
S = "ledgers/M5/scripts/M5-d-r11"
C = "Carried from round 10 (course/modules/M/M5/project.html lines cited are byte-identical since the round-10 pin e8b10b8; only :235 and :458 changed): "
rows = [
 ("M5-d-R01","project page rubric ladder, grading mode, time budget and hours (BUILDER_RULES 5)","course/modules/M/M5/project.html; tools/check_projects.py","PASS",
  f"`tools/check_projects.py --unit M5` -> 'check_projects M5: PASS', exit 0 on f42f432 ({S}/check_projects.out)."),
 ("M5-d-R02","page contract, banned strings, claims registry and DAG for the unit's pages","course/modules/M/M5/*.html; tools/check_pages.py; tools/check_dag.py","PASS",
  f"`check_pages.py --unit M5` -> PASS; `check_dag.py --unit M5` -> PASS ({S}/check_pages.out, check_dag.out); `page_smoke.py --unit M5` -> PASS ({S}/page_smoke.out)."),
 ("M5-d-R03","project.html prose: whole page re-read line by line (lines 1-522)","course/modules/M/M5/project.html:1-522","FAIL",
  "Not completed this round. Only the changed hunks (:235, :458, and the Setting paragraph around :458) and the exemplar annotations were re-read on f42f432; the other ~500 lines were not re-read in full, so the full-page row cannot be carried or asserted."),
 ("M5-d-R04","project labs 1-3: twin runs under python -I -W error; page code equals twin; expected block equals output","tests/labs/M5/lab-M5-project-{1,2,3}.py; course/modules/M/M5/project.html:140-154, :213-217, :371-386","PASS",
  f"Twins run `python -I -W error`: exit 0 for all three ({S}/lab-M5-project-{{1,2,3}}.out/.err); `tools/run_labs.py --unit M5` -> 'run_labs M5: PASS (13/13)' ({S}/run_labs.out). Lab twins unchanged since e8b10b8."),
 ("M5-d-R05","project grader reference, starter and instance: determinism, 50 seeds, lint and types","course/modules/M/M5/grader/{reference,starter,instance}.py","PASS",
  f"`tools/run_graders.py --unit M5 --seeds 0-49` -> 'PASS (reference 50/50 seeds, slowest 0.3 s)' ({S}/run_graders.out). `ruff check` and `ruff format --check` on grader and lab twins clean (17 files formatted, {S}/ruff.out); `mypy --no-incremental` on reference, starter, instance: no issues ({S}/mypy.out). reference.py, starter.py, instance.py byte-identical since e8b10b8; test_project.py changed (new test), re-run here."),
 ("M5-d-R06","page test count equals the real collect-only count","course/modules/M/M5/project.html:235 ('runs 94 checks'); course/modules/M/M5/grader/test_project.py","PASS",
  f"Round-10 FAIL closed. `pytest --collect-only -q test_project.py` in a scratch dir (test_project.py, instance.py, reference.py as contraction_solver.py) -> '94 tests collected' ({S}/collect.out); page :235 now says 94. Matches."),
 ("M5-d-R07","project.html:57 numbers and the Lab 1 expected block: recomputed values","course/modules/M/M5/project.html:57, :140-154, :159-217","PASS",
  C + "round-10 recomputation (ledgers/M5/scripts/M5-d-r10/recompute.py) reproduced in this round's run_labs PASS (13/13) and twin-1 output."),
 ("M5-d-R08","project.html:161 contraction ratio and Lab 2 expected block","course/modules/M/M5/project.html:161, :198-217","PASS",
  C + "twin-2 output reproduced by run_labs PASS (13/13)."),
 ("M5-d-R09","project.html Lab 3 numbers: 236 sweeps, cert 9.226e-11, a priori 242","course/modules/M/M5/project.html:289, :389, :466","PASS",
  C + "run_labs PASS (13/13) reproduces the lab-3 printed line; a priori count 242 unchanged (lab-3 instance unchanged)."),
 ("M5-d-R10","Exemplar B Setting names all five C1 items (utility on c >= 0) so its C1 level-4 score is supportable","course/modules/M/M5/project.html:458, :472, :452-454","PASS",
  "Round-10 FAIL closed. project.html:458 now reads 'utility is sqrt(k^0.3 - k') on consumption k^0.3 - k' >= 0'; the rubric C1 level-4 descriptor (:407) requires the utility sqrt(c) on c >= 0, and the Setting now states it. Official scoring at :452 ('4,4,4,4,4,3') and annotation at :472 agree."),
 ("M5-d-R11","time budget 26 h of 130 h; lesson hours 6x10 + 4x11 = 104","course/modules/M/M5/project.html:33, :256-264; course/modules/M/M5/index.html:29-31, :131","PASS",
  C + "26 = 1+2+8+7+3+5; 26/130 = 20.0 %; 104 + 26 = 130."),
 ("M5-d-R12","project.html conventions match reference.py (params, tolerance, budget, synchronous sweep, stop rule); 120 s limit","course/modules/M/M5/project.html:231-248; course/modules/M/M5/grader/reference.py:81-128; course/assets/js/python.js TIMEOUT_MS","PASS",
  "Re-verified this round: conventions lines 240-248 unchanged; only the :235 count changed (re-verified under R06). reference.py unchanged; TIMEOUT_MS = 120000 in python.js."),
 ("M5-d-R13","grader docstring claim: change at the last grid point alone certifies tol one sweep before the sup-norm change","course/modules/M/M5/grader/test_project.py (test body now shifted by +18 lines after the new test)","PASS",
  "Carried from round 10: the cited test body is byte-identical; the new test was inserted above it (test_project.py ~:403), only its line numbers moved. Round-10 recomputation: last-point stop 169, sup-norm stop 170."),
 ("M5-d-R14","grader instance.py and starter.py: lint, types, 50-seed run","course/modules/M/M5/grader/instance.py, starter.py","PASS",
  C + f"run_graders PASS, ruff and mypy clean ({S}/run_graders.out, ruff.out, mypy.out). Grid-range docstring claims in instance.py not re-derived; not asserted."),
 ("M5-d-R15","alternative correct implementations pass; spec-violating ones fail for stated spec reasons","ledgers/M5/alternatives/alt1..alt5","PASS",
  f"Re-run on f42f432 ({S}/alternatives.out): alt3, alt4, alt5 pass 94/94; alt1 (Gauss-Seidel in place) and alt2 (residual stop) fail 7 each, for the synchronous-sweep convention (:244) and the certified formula (:245-246) as before."),
 ("M5-d-R16","all existing grader mutants killed (round-10 survivor v10_03 closed)","ledgers/M5/mutants/*.py; course/modules/M/M5/grader/test_project.py","PASS",
  f"`tools/mutate_graders.py --unit M5` -> 'mutate_graders M5: PASS (106/106 killed)' ({S}/mutate.out). v10_03 is now killed by test_saving_above_the_current_capital_is_feasible_within_resources (new test, test_project.py ~:403-418). The new survivor is recorded separately as R31."),
 ("M5-d-R17","Lab 1 expected block line '<=' matches the printed line","course/modules/M/M5/project.html:133-136, :154-155; tests/labs/M5/lab-M5-project-1.py:79-82","PASS",
  C + "run_labs PASS (13/13) and twin-1 output reproduce the expected block."),
 ("M5-d-R18","DAG and concept closure for the project page","course/modules/M/M5/project.html; tools/check_dag.py","PASS",
  f"`tools/check_dag.py --unit M5` -> PASS ({S}/check_dag.out)."),
 ("M5-d-R19","stretch items and reading block (:491-510) prose","course/modules/M/M5/project.html:491-510","PASS",
  C + "no claim contradicted; DAG claims covered by R18."),
 ("M5-d-R20","no process words in learner-facing project prose; check_projects","course/modules/M/M5/project.html; grader/*.py; tests/labs/M5/lab-M5-project-*.py","PASS",
  f"check_projects PASS ({S}/check_projects.out). Read by eye: the new test docstring (test_project.py ~:403-406) contains no process words."),
 ("M5-d-R21","cards.json: count, duplicates, grade and basis consistency","course/modules/M/M5/cards.json","PASS",
  f"212 cards (was 211; new M5-c216). No duplicate ids, fronts or backs; key sets: 144 with grade+basis, 68 without ({S}/cards_check.out). Every grade C card has a basis."),
 ("M5-d-R22","closed-set definition cards agree with L04 Section 2","course/modules/M/M5/cards.json (M5-c051, M5-c215); course/modules/M/M5/L04.html:238-256","PASS",
  C + "M5-c215 'complement X \\ K is open' matches L04 Section 2."),
 ("M5-d-R23","C-grade cards cite a lab part that prints the number","course/modules/M/M5/cards.json (c117, c180, c191, c213-c215)","PASS",
  C + "c117, c180, c191, c213-c215 unchanged this round; re-checked against round-10 twin outputs."),
 ("M5-d-R24","every changed card agrees with the current lesson text","course/modules/M/M5/cards.json (changed: c003, c009, c015, c027, c043, c049, c085, c086, c142, c143, c145, c146, c175, c187, c189, c202, c203, c216)","PASS",
  "Each changed back/front read against the lesson: L01 Def 1.1 'taken as given' (L01.html:62), L01 Section 4 canon breaks incl. N (L01.html:254-262), L03 Lemma 1.3 (L03.html:67), L06 Def 1.1 and Lemma 1.2 (L06.html:59, :64), L07 Section 4 fixed-point example (L07.html:308-312), L09 Lemma 1.1 'G finite' (L09.html:65-66), Lemma 1.2 and Theorem 1.3 (L09.html:75-86), Lemma 2.3 hypotheses (L09.html:104-105), L10 Lemma 2.4 (L10.html:105), Prop 4.1 and Remark 4.2 (L10.html:360-371), Theorem 3.5 (L10.html:156-172). No contradiction found."),
 ("M5-d-R25","unchanged C-grade cards c114, c115, c120, c135, c160 agree with lab output","course/modules/M/M5/cards.json","PASS",
  C + "byte-identical cards; round-10 checks stand."),
 ("M5-d-R26","c117 and c180 carry grade C with a basis naming the lab part","course/modules/M/M5/cards.json (M5-c117, M5-c180)","PASS",
  C + "both entries unchanged since round 10 and carry grade 'C' with basis."),
 ("M5-d-R27","M5-c056 matches L04 Prop 1.7 and its hypothesis","course/modules/M/M5/cards.json (M5-c056); L04.html Prop 1.7","PASS",
  C + "card unchanged."),
 ("M5-d-R28","M5-c143 states Lemma 1.2 of L09 with its hypotheses and matches L08 Theorem 2.2(a)","course/modules/M/M5/cards.json (M5-c143); L09.html Lemma 1.2; L08.html Theorem 2.2","PASS",
  "Changed wording only ('its proof is repeated in Section 1'); L09 Section 1 proves Lemma 1.2 (L09.html:75-100). Hypothesis 0 < beta < 1 and the contraction inequality unchanged."),
 ("M5-d-R29","notation: registered symbols used with their registered meaning only","course/modules/M/M5/project.html; notation/notation.json","PASS",
  "The round-11 delta adds only k, k', \\ge and \\R-free arithmetic; no registered symbol is reused with another meaning. Local symbols beta, alpha, V, W unchanged from round 10."),
 ("M5-d-R30","DAG claims for cards and project prose","course/modules/M/M5/project.html; cards.json; tools/check_dag.py","PASS",
  f"check_dag M5 PASS ({S}/check_dag.out)."),
 ("M5-d-R31","every stated behaviour of converged is killed by the grader (project.html:246 'converged is True exactly when certified_error is at most tol')","course/modules/M/M5/grader/test_project.py:269-278, :336; course/modules/M/M5/project.html:246; ledgers/M5/mutants/v11_03_converged_means_budget_not_exhausted.py","FAIL",
  f"New student-error mutant v11_03 (converged = iterations < budget) SURVIVES: 94 passed under QF_SEED=0 ({S}/v11_mutants.out). Witness: instance.make_instance(0) (beta 0.82, alpha 0.52, tol 1e-8), reference solve converges at sweep 98 (certified 9.616e-9). With max_iter=98 reference gives converged=True and mutant gives converged=False, although certified_error <= tol. page :246 says 'exactly when', so the grader must catch this."),
 ("M5-d-R32","new student-error mutants v11_01 and v11_02 are killed","ledgers/M5/mutants/v11_01_utility_uses_capital_not_output.py; ledgers/M5/mutants/v11_02_operator_returns_the_best_successor_not_the_value.py","PASS",
  f"v11_01 (utility sqrt(k - k') with feasibility k**alpha) FAILED test_operator_matches_its_definition[0]/[1] and certified-error tests; v11_02 (operator returns argmax successor) FAILED test_operator_matches_its_definition and test_operator_is_monotone ({S}/v11_mutants.out)."),
 ("M5-d-R33","new test test_saving_above_the_current_capital_is_feasible_within_resources has correct arithmetic","course/modules/M/M5/grader/test_project.py (new test)","PASS",
  "Recomputed: 0.25**0.5 = 0.5; sqrt(0.5 - 0.4) + 0.9*10 = 0.316228 + 9 = 9.316228, matching the expected 9.316228 at 1e-6; reference passes 94/94."),
 ("M5-d-R34","new card M5-c216 (N has no upper bound) agrees with L01 and carries a basis","course/modules/M/M5/cards.json (M5-c216); course/modules/M/M5/L01.html:67, :254-262","PASS",
  "L01 Theorem 1.2 (L01.html:67) and the third canon break in Section 4 (L01.html:262) state that N is nonempty with no upper bound; card's answer and basis ('Section 4 (canon break 3), from Theorem 1.2') agree. Grade T."),
 ("M5-d-F01","mutant m64 (change measured at the last point only) is killed","ledgers/M5/mutants/m64_change_measured_at_the_last_point_only.py","PASS",
  f"Included in the 106/106 mutate run ({S}/mutate.out)."),
 ("M5-d-F02","lab 3 instance and a priori count 242","course/modules/M/M5/project.html:229, :289; tests/labs/M5/lab-M5-project-3.py","PASS",
  C + "lab-3 twin unchanged; run_labs PASS."),
 ("M5-d-F03","cards grade tallies","course/modules/M/M5/cards.json","PASS",
  f"Grades now T 102, C 42, none 68 (total 212); every C card has a basis ({S}/cards_check.out)."),
]
mutants = [
 {"name":"v11_01_utility_uses_capital_not_output.py","description":"utility is sqrt(k - k') while feasibility still uses k**alpha","killed_by":"test_operator_matches_its_definition[0]; test_certified_error_bounds_the_distance_to_the_fixed_point[0]"},
 {"name":"v11_02_operator_returns_the_best_successor_not_the_value.py","description":"the Bellman operator returns the argmax successor k' instead of the maximised value","killed_by":"test_operator_matches_its_definition[0]; test_operator_is_monotone[0]"},
 {"name":"v11_03_converged_means_budget_not_exhausted.py","description":"converged = iterations < budget instead of certified_error <= tol","killed_by":None,"status":"SURVIVED (94 passed); witness instance.make_instance(0), max_iter=98 gives converged False while certified 9.616e-9 <= 1e-8"},
 {"name":"existing m01..m103 + v10_01..v10_03 (106 mutants)","description":"round-9 and round-10 mutant set, unchanged","killed_by":"106/106 killed (tools/mutate_graders.py --unit M5)"},
]
frag = {
 "unit":"M5","slice":"d","round":11,
 "verifier":"Haiku independent verifier (round 11), no build context",
 "pin":"f42f4329dcb0b5c2257e40cd6c27e734fa700d46","base":"e8b10b8110923bd88c3b4bd0e36e1571be3e6725",
 "checkout":"/Users/billyribeiro/.fanout/wt/verifyB11-M5-d",
 "scratch":"/Users/billyribeiro/.fanout/wt/verifyB11-M5-d/"+S,
 "verified_at":datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
 "verdict":"FAIL",
 "rows":[],"mutants":mutants,"registry_flags":[],"freshness_flags":[],
 "notes":[
  "Delta since round-10 pin e8b10b8: project.html :235 (94 count) and :458 (Setting, utility domain); grader/test_project.py (+1 test); cards.json (212 cards; wording changes and new M5-c216); no lab twin, reference, starter or instance changes.",
  "Not checked: full line-by-line re-read of project.html 1-522 this round (R03 FAIL); grader instance.py grid-range docstring claims; lesson prose outside the cited lines; the verify_refs live run (offline only: 560 entries, 0 problems).",
  "alt1 and alt2 fail for spec reasons (synchronous-sweep convention; certified formula), so they are not over-constraint findings."],
 "summary":"Slice d round 11: FAIL. 35 rows: 33 PASS, 2 FAIL (R03 full-page re-read not completed; R31 surviving grader mutant v11_03 contradicting project.html:246). Mutants: 109 total, 108 killed (106 existing incl. v10_03, plus v11_01, v11_02), v11_03 survives. Fix: add a grader test with max_iter equal to the reference convergence sweep count (98 for make_instance(0)) asserting converged is True; re-run mutate_graders; re-read project.html 1-522 on the pin."
}
rows_out=[]
for rid,check,loc,status,ev in rows:
    r={"id":rid,"check":check,"location":loc,"status":status,"evidence":ev}
    if status!="PASS":
        r["fix"]={"M5-d-R03":"Re-read course/modules/M/M5/project.html lines 1-522 line by line on the pin and record each prose claim with its locator.",
                  "M5-d-R31":"Add a test in grader/test_project.py: run solve with max_iter equal to the reference's convergence sweep count and assert converged is True; then re-run tools/mutate_graders.py --unit M5 and confirm v11_03 is killed."}[rid]
    rows_out.append(r)
# R31 is a FAIL row; add the explicit witness row for the page sentence
frag["rows"]=rows_out
# drop the notes-only ids not present
pathlib.Path("ledgers/M5/M5-d.json").write_text(json.dumps(frag,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
print(len(rows_out), "rows")
