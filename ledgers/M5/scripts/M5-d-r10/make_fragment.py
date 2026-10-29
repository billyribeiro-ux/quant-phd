import json, subprocess, datetime
S = "ledgers/M5/scripts/M5-d-r10"
sha = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
def row(i, check, loc, status, ev):
    return {"id": i, "check": check, "location": loc, "status": status, "evidence": ev}
R = []
R.append(row("M5-d-R01", "project page rubric ladder, grading mode, time budget and hours (BUILDER_RULES 5)",
  "course/modules/M/M5/project.html; tools/check_projects.py", "PASS",
  f"`tools/check_projects.py --unit M5` -> 'check_projects M5: PASS' exit 0 ({S}/check_projects.out)."))
R.append(row("M5-d-R02", "page contract, banned strings, claims registry and DAG for the unit's pages",
  "course/modules/M/M5/*.html; tools/check_pages.py; tools/check_dag.py", "PASS",
  f"`check_pages.py --unit M5` -> PASS; `check_dag.py --unit M5` -> PASS ({S}/check_pages.out, check_dag.out)."))
R.append(row("M5-d-R03", "project.html prose: whole page re-read line by line (lines 1-522)",
  "course/modules/M/M5/project.html:1-522", "PASS",
  "Whole page read this round. Delta since round-9 pin b6865c7: the lab-1 code block at :133-136 now prints 'actual error ... <= / >' via a relation variable; prose unchanged. No prose claim contradicted except R06 and R10."))
R.append(row("M5-d-R04", "project labs 1-3: twin runs under python -I -W error; page code equals twin; expected block equals output",
  "tests/labs/M5/lab-M5-project-{1,2,3}.py; course/modules/M/M5/project.html:140-154, :213-217, :371-386", "PASS",
  f"`python -I -W error` on each twin: exit 0, stderr 0 bytes ({S}/twin-{{1,2,3}}.out/.err). `tools/run_labs.py --unit M5` -> 'run_labs M5: PASS (13/13)' ({S}/run_labs.out)."))
R.append(row("M5-d-R05", "grader reference, starter and instance: determinism, 50 seeds, lint and types",
  "course/modules/M/M5/grader/{reference,starter,instance}.py", "PASS",
  f"`tools/run_graders.py --unit M5 --seeds 0-49` -> 'PASS (reference 50/50 seeds, slowest 0.3 s)' ({S}/run_graders.out). `ruff check` on grader and project twins: All checks passed; `ruff format --check`: 17 files formatted; `mypy --no-incremental` on reference, instance, starter: no issues ({S}/ruff.out, mypy.out)."))
R.append(row("M5-d-R06", "page test count equals the real collect-only count",
  "course/modules/M/M5/project.html:235 ('runs 92 checks'); course/modules/M/M5/grader/test_project.py", "FAIL",
  f"Real count is 93: `pytest --collect-only -q test_project.py` in a scratch dir holding test_project.py, instance.py, reference.py (as contraction_solver.py) -> '93 tests collected' ({S}/collect.out); `QF_SEED=0 pytest -W error --assert=plain` on reference -> '93 passed' ({S}/collect.out). Page line 235 still says 92. The new test test_stop_uses_the_largest_absolute_change_over_the_grid (test_project.py:457) is the 93rd. Also `tools/page_smoke.py --unit M5 --pages project` -> in-browser grader 'All 93 tests pass' ({S}/page_smoke_project.out). Fix: change 'runs 92 checks' to 'runs 93 checks' at project.html:235."))
R.append(row("M5-d-R07", "lab 1 claims and numbers on project.html against the twin output",
  "course/modules/M/M5/project.html:57, :140-154, :159-217", "PASS",
  f"Independent recomputation ({S}/recompute.py): V1=(0.455090, 0.669838, 0.826569); sup|BV-BW|=0.409581 <= 0.9*0.826569=0.743912; change 0.826569, cert 7.439119; stop sweep 146, change 1.0550e-7, cert 9.495187e-7; actual 9.495178e-7. All match :57 and the expected block."))
R.append(row("M5-d-R08", "lab 2 completion: ratio 0.300000 and the stop line at :161 and :215-217",
  "course/modules/M/M5/project.html:161, :198-217", "PASS",
  f"Recomputed ratio = 0.3000000000000001 for V=0, W=(0.1,0.2,0.3); stop 146, cert 9.495e-07, last change 1.055e-07 ({S}/recompute.py). Twin output matches ({S}/twin-2.out)."))
R.append(row("M5-d-R09", "lab 3 reference numbers and interpretation prose (:289, :389, :466)",
  "course/modules/M/M5/project.html:289, :389, :466", "PASS",
  f"Twin output ({S}/twin-3.out): 236 sweeps, cert 9.226e-11, last change 1.025e-11, a priori count 242 (recomputed: {S}/recompute.py / {S}/recompute.py-like loop gave 242), residual 9.226e-12, gap 0.021829 > 1e-6, ratio 0.900000."))
R.append(row("M5-d-R10", "exemplar annotations and official scoring (:418-480)",
  "course/modules/M/M5/project.html:458, :472, :452-454", "FAIL",
  "Exemplar B's Setting (:458) states utility sqrt(k**0.3 - k') and never states the consumption domain c >= 0. Its C1 annotation at :472 says 'Meets C1 level 4: names ... the utility on c>=0', and the official scoring at :452/:454 gives C1 4 (data-scores='4,4,4,4,4,3' at :452). The C1 descriptor at :407 requires the utility sqrt(c) on c >= 0, so the passage names four of the five items and scores 3, not 4. Fix: add 'on consumption c >= 0' to the Exemplar B Setting and keep the level-4 annotation, or change the annotation to level 3 and data-scores to '3,4,4,4,4,3'. Exemplar A and the other annotations were checked and are consistent with their data-scores."))
R.append(row("M5-d-R11", "hours arithmetic: hub split and project time budget",
  "course/modules/M/M5/project.html:33, :256-264; course/modules/M/M5/index.html:29-31", "PASS",
  "Time budget rows 1+2+8+7+3+5 = 26 (project.html:258-263); 26/130 = 20.0 % (:264). Hub: data-hours-lessons=104, data-hours-project=26, 'Tier U · 130 hours' (index.html:29-31). Lessons: 6x10 + 4x11 = 104 (index.html:131). 104+26 = 130."))
R.append(row("M5-d-R12", "spec, conventions and invalid-input contract vs grader",
  "course/modules/M/M5/project.html:231-248; course/modules/M/M5/grader/test_project.py", "PASS",
  "Conventions (:240-248) match reference.py: _params, _tolerance, _budget, _sweep (synchronous, reference.py:81-91), solve stop at certified<=tol (reference.py:101-128); a priori count formula checked (242). The 120 s browser limit matches course/assets/js/python.js TIMEOUT_MS = 120000."))
R.append(row("M5-d-R13", "certified error and stopping paragraphs vs grader docstrings",
  "course/modules/M/M5/project.html:245-246; grader/test_project.py:457-487", "PASS",
  "The new grader docstring claim (change at the last grid point alone certifies tol one sweep before the sup-norm change) was computed: last-point stop 169, sup-norm stop 170 ({S}/recompute.py-like run in session). Page statements at :245-246 match reference.py."))
R.append(row("M5-d-R14", "instance.py and starter.py contract",
  "course/modules/M/M5/grader/instance.py, starter.py", "PASS",
  "ruff and mypy clean; run_graders PASS; instance docstring grid claims (8 to 24 points, first point in [0.20, 0.90]) were not separately re-derived this round; the 50-seed run exercises instance draws."))
R.append(row("M5-d-R15", "alternative correct implementations must pass; wrong ones must fail for a spec reason",
  "ledgers/M5/alternatives/alt1..alt5", "PASS",
  f"alt3, alt4, alt5 pass 93/93 ({S}/alternatives.out). alt1 (Gauss-Seidel in place) fails 7: it violates the page's synchronous-sweep convention (:244) and the certified formula (:245). alt2 (residual stop) fails 7: it certifies a different quantity than beta/(1-beta) times the last change (:245-246). Both failures cite a spec sentence."))
R.append(row("M5-d-R16", "grader mutation testing: all mutants killed; new student-error mutants",
  "ledgers/M5/mutants/*.py; course/modules/M/M5/grader/test_project.py; course/modules/M/M5/project.html:53, :241, :395", "FAIL",
  f"`tools/mutate_graders.py --unit M5` -> 103/103 killed on the existing set (m64 is now killed; round-9 F01 is closed) ({S}/mutate.out). Three new student-error mutants: v10_01_double_discount_in_the_continuation (killed by test_operator_matches_its_definition), v10_02_tolerance_scaled_by_grid_size (killed by test_converged_means_certified_within_tolerance), and v10_03_savings_capped_by_capital (SURVIVES: 93 passed, {S}/new_mutants.out). v10_03 adds a rule k' <= k that the page does not state: feasibility is k' <= k**alpha only (project.html:53 'feasible ... when that consumption is nonnegative'; :241; :395). Witness: grid [0.25,0.4,1.0], values [0,10,0], beta 0.9, alpha 0.5: reference bellman_operator gives [9.316228, 9.482136, 9.774597], the mutant gives [0.5, 9.482136, 9.774597]. Fix: add a test with a grid point k' with k < k' <= k**alpha and a large V(k') (e.g. the witness above) asserting the operator value at k=0.25."))
R.append(row("M5-d-R17", "lab-1 expected-block hunk after the round-9 pin (project.html:133-136 and twin)",
  "course/modules/M/M5/project.html:133-136; tests/labs/M5/lab-M5-project-1.py:79-82", "PASS",
  "Relation variable prints '<=' here (actual 9.495e-7 <= cert 9.495e-7 at 9 decimals); expected block at :154-155 matches the printed line byte for byte (run_labs PASS, twin-1.out)."))
R.append(row("M5-d-R18", "DAG: concepts used outside the unit prerequisite closure", "course/modules/M/M5/project.html; tools/check_dag.py", "PASS",
  f"`tools/check_dag.py --unit M5` -> PASS ({S}/check_dag.out)."))
R.append(row("M5-d-R19", "stretch and reading sections", "course/modules/M/M5/project.html:491-510", "PASS",
  "Stretch items and reading block read; the statement that the proofs use Lessons 1, 2, 4, 7 and the geometric series of M1 is a DAG claim covered by check_dag (R18). No passage locator is claimed."))
R.append(row("M5-d-R20", "process words and banned phrasing in learner text", "course/modules/M/M5/project.html; grader/*.py; tests/labs/M5/lab-M5-project-*.py", "PASS",
  f"check_pages and check_projects PASS ({S}/check_projects.out). Read by eye: no process words in learner-facing prose."))
R.append(row("M5-d-R21", "cards.json structure: ids, fronts, backs, keys, grades", "course/modules/M/M5/cards.json", "PASS",
  f"211 cards; no duplicate ids, fronts or backs; key sets: 143 with grade+basis, 68 without (script {S}/cards_check.py). Every grade C card has a basis."))
R.append(row("M5-d-R22", "card M5-c051 agrees with L04 (formerly 'F closed' while the lesson says K)", "course/modules/M/M5/cards.json (M5-c051, M5-c215); course/modules/M/M5/L04.html:238-256", "PASS",
  "Re-verified on the current pin: M5-c051 back no longer mentions closed sets; the closed definition moved to M5-c215 ('complement X \\ K is open') and matches L04.html Section 2 ('A set K subseteq X is closed when its complement X\\setminus K is open')."))
R.append(row("M5-d-R23", "cards changed since round-9 pin (c051, c117, c180, c191, c213, c214, c215)", "course/modules/M/M5/cards.json", "PASS",
  "c117 (L07 Lab 1 Part A n=5 row: bound 48.92x error, L07.html:394) and c180 (L10 Lab 1 Part C meshes 0.1 and 0.01: twin output) grade C with basis. c191 matches L01 maximum definition. c213/c214 match L02 Section 2 text; c215 matches L04 Section 2."))
R.append(row("M5-d-R24", "every card statement vs the current lesson text and lab output",
  "course/modules/M/M5/cards.json; L01-L10", "PASS",
  f"All 211 cards read. C-grade numbers checked against the twin outputs ({S}/twins/): c010-012 (L01), c032-034 (L02), c047-049 (L03, grid x=2+k/200), c066-068 (L04), c082-084 (L05), c098-100 (L06), c118-120 and c203 (L07), c136-139 (L08; c139 recomputed 40/257/527), c155-158, c207-208 (L09; c154 recomputed n=152, 1.067e-6 at n=151, 9.60e-7 at n=152), c182-185, c209 (L10). c205 (excess 5.55e-16) recomputed with the twin's seeded draw. Card c150 does not exist in the file (ids run 148, 151)."))
R.append(row("M5-d-R25", "cards c114, c115, c120, c135, c150, c160", "course/modules/M/M5/cards.json", "PASS",
  "c114, c115, c120, c135, c160 checked by hand and against the lab output; c150 is absent from cards.json, so no check applies."))
R.append(row("M5-d-R26", "grade and basis on c117 and c180 (round-9 FAIL)", "course/modules/M/M5/cards.json (M5-c117, M5-c180)", "PASS",
  "Both now carry grade 'C' and a basis naming the lab part (c117 'Lab 1 Part A (cosine iteration, n = 5 row)'; c180 'Lab 1 Part C (step integrator, meshes 0.1 and 0.01)'). Both lab parts print the cited numbers (twins/lab-M5-L07-1.out, L10 Part C)."))
R.append(row("M5-d-R27", "card c056 (Proposition 1.7 and d-infinity real-valued)", "course/modules/M/M5/cards.json (M5-c056); L04.html Prop 1.7", "PASS",
  "Statement matches the lesson; boundedness is the hypothesis that makes every sup distance a real number."))
R.append(row("M5-d-R28", "card c143 (Lemma 1.2 is the same as Theorem 2.2(a) of Lesson 8)", "course/modules/M/M5/cards.json (M5-c143); L09.html Lemma 1.2; L08.html Theorem 2.2", "PASS",
  "Both statements are 0<beta<1 and ||BV-BW|| <= beta||V-W||; the lesson text states the match."))
R.append(row("M5-d-R29", "notation: every symbol vs notation/notation.json", "course/modules/M/M5/project.html; notation/notation.json", "PASS",
  "Registered macros in use: \\R (real numbers) with its meaning only. Unregistered local symbols: beta, alpha (local by notation.json 'about'), \\mathcal{B}, V, W, V^\\ast (not R^\\ast, which is registered to AP1). No registered symbol is reused with another meaning."))
R.append(row("M5-d-R30", "DAG and concept links on the project page and cards", "course/modules/M/M5/project.html; cards.json; tools/check_dag.py", "PASS",
  f"check_dag M5 PASS ({S}/check_dag.out)."))
R.append(row("M5-d-F01", "round-9 surviving mutant m64 (change measured at last point only)", "ledgers/M5/mutants/m64_change_measured_at_the_last_point_only.py; course/modules/M/M5/project.html", "PASS",
  f"Round-10 mutate run: m64 KILLED ({S}/mutate.out). The grader's new test test_stop_uses_the_largest_absolute_change_over_the_grid closes it."))
R.append(row("M5-d-F02", "round-9 F02 subject: Lab 3 inputs and printed reference numbers", "course/modules/M/M5/project.html:229, :289; tests/labs/M5/lab-M5-project-3.py", "PASS",
  "Lab 3 instance (beta 0.9, alpha 0.3, ten points 0.45 to 2.70, tol 1e-10) matches the recomputed a priori count 242 and twin output (R09)."))
R.append(row("M5-d-F03", "round-9 F03 subject: cards.json grades", "course/modules/M/M5/cards.json", "PASS",
  "Grades 'T' 101, 'C' 42, none 68; every 'C' has a basis (R21, R26)."))
mutants = [
 {"name": "v10_01_double_discount_in_the_continuation.py", "description": "the continuation is discounted twice (beta squared times V(k'))", "killed_by": "test_operator_matches_its_definition[0] (seed 0); 12 failed"},
 {"name": "v10_02_tolerance_scaled_by_grid_size.py", "description": "the stop test compares the certified error with tol times the number of grid points", "killed_by": "test_converged_means_certified_within_tolerance[0] (seed 0); 4 failed"},
 {"name": "v10_03_savings_capped_by_capital.py", "description": "a saving is feasible only if k' <= k as well as k' <= k**alpha; the page states only k' <= k**alpha", "killed_by": None, "status": "SURVIVED (93 passed); witness grid [0.25,0.4,1.0], values [0,10,0]: reference 9.316228 vs mutant 0.5 at k=0.25"},
 {"name": "existing m01..m99 + m100..m103 (103 mutants)", "description": "round-9 mutant set, unchanged", "killed_by": "103/103 killed (tools/mutate_graders.py --unit M5, seeds default)"},
]
alts = {"alt1_gauss_seidel_in_place": "7 failed (synchronous-sweep convention, :244)", "alt2_residual_stop": "7 failed (certified quantity, :245)", "alt3": "pass", "alt4": "pass", "alt5": "pass"}
frag = {
 "unit": "M5", "slice": "d", "round": 10,
 "verifier": "Haiku independent verifier (round 10), no build context",
 "pin": sha, "base": "44f1eb6", "checkout": "/Users/billyribeiro/.fanout/wt/verifyB10-M5-d",
 "scratch": f"/Users/billyribeiro/.fanout/wt/verifyB10-M5-d/{S}",
 "verified_at": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
 "verdict": "FAIL", "rows": R, "mutants": mutants,
 "registry_flags": [], "freshness_flags": [],
 "notes": [
  "Delta since round-9 pin b6865c7: project.html:133-136 (lab 1 expected code), grader/test_project.py (+1 test), tests/labs/M5/lab-M5-project-1.py, cards.json (c051, c117, c180, c191, c213-c215), index.html, L02-L04.html.",
  "Not checked: the instance.py tie and grid-draw claims beyond the 50-seed run; the 'M1 geometric series' DAG claim beyond check_dag; all page prose on lessons outside this slice.",
  "Alternatives alt1 and alt2 fail for spec reasons; they are not over-constraint findings.",
  "Scratch scripts: " + S + "/ (recompute.py, cards_check.py, l08_beta.py, make_fragment.py)."],
 "summary": "Slice d round 10: FAIL. 33 rows (R01-R30, F01-F03): 30 PASS, 3 FAIL (R06 count 92 vs 93; R10 exemplar B C1 scored 4 without c>=0; R16 surviving mutant v10_03). Mutants: 106 total, 105 killed, v10_03 survives. Fix list: project.html:235 -> 93; add a test killing v10_03 (witness grid [0.25,0.4,1.0], values [0,10,0]); add c>=0 to Exemplar B Setting or lower its C1 annotation to 3.",
}
json.dump(frag, open("ledgers/M5/M5-d.json", "w"), indent=2, ensure_ascii=False)
print("written", len(R), "rows")
