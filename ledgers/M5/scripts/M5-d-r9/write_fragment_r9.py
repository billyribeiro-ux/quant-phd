import json, re, datetime, pathlib
root = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyB9-M5-d")
S = root / "ledgers/M5/scripts/M5-d-r9"
mut_lines = (S / "mutate_M5_r9.out").read_text(encoding="utf-8").splitlines()
mutants = []
for line in mut_lines:
    m = re.match(r"^(KILLED|SURVIVED) (\S+?): (.*) -> (.*)$", line)
    if not m:
        continue
    status, name, desc, killed = m.groups()
    if status == "KILLED":
        mutants.append({"name": name, "description": desc, "killed_by": killed})
    else:
        mutants.append({"name": name, "description": desc, "killed_by": "SURVIVED: no test fails on seeds 0-9 (see F01)"})

def row(id_, check, location, status, evidence, fix=None):
    r = {"id": id_, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    return r

rows = [
 row("M5-d-R01", "project page rubric ladder, grading mode, time budget and hours (BUILDER_RULES 5)",
     "course/modules/M/M5/project.html; tools/check_projects.py", "PASS",
     "Fresh: `tools/check_projects.py --unit M5` -> `check_projects M5: PASS` (exit 0; ledgers/M5/scripts/M5-d-r9/check_projects.out)."),
 row("M5-d-R02", "page contract, banned strings, claims registry and DAG for the unit's pages",
     "course/modules/M/M5/*.html; tools/check_pages.py; tools/check_dag.py", "PASS",
     "Fresh, unit-scoped: `check_pages.py --unit M5` -> `check_pages M5: PASS`; `check_dag.py --unit M5` -> `check_dag M5: PASS` (check_pages.out, check_dag.out). Note: `--page` mode is for lessons only; project.html is checked by check_projects and page_smoke (page_smoke_project.out: PASS, in-browser grader 92/92)."),
 row("M5-d-R03", "project.html prose: whole page re-read; hunks at lines 53, 239, 416",
     "course/modules/M/M5/project.html:53, :239, :416", "PASS",
     "git diff ce7b382 b6865c7 -- project.html changes one line (:53, 'which the labs call its resources'); the labs print 'resources at k=' (twin-project-1.out line 1-3; tests/labs/M5/lab-M5-project-1.py:43). The full page text was read this round; numbers on :239 and :416 re-checked against twin-project-2/3 outputs."),
 row("M5-d-R04", "project labs 1-3: twin runs under python -I -W error; page code equals twin; expected block equals output",
     "tests/labs/M5/lab-M5-project-{1,2,3}.py; course/modules/M/M5/project.html:140-154, :213-217, :371-386", "PASS",
     "Fresh: `python -I -W error` on each twin -> exit 0, stderr 0 bytes (twin-project-{1,2,3}.err). `tools/run_labs.py --unit M5` -> `run_labs M5: PASS (13/13)` (run_labs.out; its check_lab asserts byte-identical page code and output equality, with the completion blanks of Lab 2 checked line by line)."),
 row("M5-d-R05", "grader reference, starter and instance: determinism, 50 seeds, lint and types",
     "course/modules/M/M5/grader/{reference,starter,instance}.py", "PASS",
     "Fresh: `tools/run_graders.py --unit M5 --seeds 0-49` -> `run_graders M5: PASS (reference 50/50 seeds, slowest 0.2 s)` (run_graders.out). `ruff check` on grader and the three project twins -> All checks passed (ruff.out); `ruff format --check` on grader and tests/labs/M5 -> 17 files already formatted (ruff_format.out); `mypy --no-incremental` on reference, instance, starter -> Success: no issues found in 3 source files (mypy.out)."),
 row("M5-d-R06", "page test count equals the real collect-only count",
     "course/modules/M/M5/project.html ('runs 92 checks'); course/modules/M/M5/grader/test_project.py", "PASS",
     "Fresh collect in scratch dir (test_project.py, instance.py, reference.py copied, reference as contraction_solver.py): `92 tests collected` (collect.out); `QF_SEED=0 pytest -W error --assert=plain` on the reference -> `92 passed` (pytest_reference.out)."),
 row("M5-d-R07", "lab 1 claims and numbers on project.html against the twin output",
     "course/modules/M/M5/project.html:57, :140-154, :159-217", "PASS",
     "Fresh twin-project-1.out: resources 0.707107, 0.948683, 1.183216; feasible {0.5}, {0.5,0.9}; V1 = (0.455090, 0.669838, 0.826569); sup|BV-BW| = 0.409581 <= 0.743912; first sweep change 0.826569, certified 7.439119; stop after sweep 146, certified 0.000000950 = actual error. Matches the page."),
 row("M5-d-R08", "lab 2 claims: ratio 0.3, 146 sweeps, certified 9.495e-07, last change 1.055e-07",
     "course/modules/M/M5/project.html:159, :215-217", "PASS",
     "Fresh twin-project-2.out: ratio 0.300000 at most beta; sweeps 146; certified 9.495e-07; values (4.550898, 4.765646, 4.922377). Recomputed unrounded (project_digits.py): ratio 0.3000000000000001, certified 9.495187356e-7, last change 1.0550208e-7; lab 1's change 1.0550208e-7 prints as 0.000000106, as the page says."),
 row("M5-d-R09", "lab 3 hypothesis and expected numbers (236 sweeps, 9.226e-11, a priori 242, residual, 200 pairs)",
     "course/modules/M/M5/project.html:287, :371-386, :387, :464", "PASS",
     "Fresh twin-project-3.out: smallest gap 0.021829 (clear of tie True); sweeps 236; last change 1.025e-11; certified 9.226e-11; a priori count 242; residual 9.226e-12 <= (1+beta) x certified True; 200 pairs largest ratio 0.900000 at most beta True; V(0.45)=5.804999 ... V(2.7)=6.171668."),
 row("M5-d-R10", "exemplar annotations and official scoring (project.html:418-480)",
     "course/modules/M/M5/project.html:418-480", "PASS",
     "Re-read this round. Exemplar A official scoring C1 2, C2 2, C3 1, C4 2, C5 2, C6 2 matches its 'Meets/Misses' annotations; Exemplar B C1-C5 4 and C6 3 matches its annotations. Exemplar A's 'about 240 sweeps' is annotated as not printed (lab prints 236)."),
 row("M5-d-R11", "rubric ladder rung claims and scope; time budget arithmetic and hours",
     "course/modules/M/M5/project.html:33, :256-262, time-budget table; course/modules/M/M5/index.html", "PASS",
     "Time budget 1+2+8+7+3+5 = 26 h; 26/130 = 20.0 %; hub: 130 h, 26 project h; lessons 6x10 + 4x11 = 104 h; 104 + 26 = 130 h (grep of data-hours and study-hours in L01-L10 and index.html)."),
 row("M5-d-R12", "specification and grader alignment (project.html:231-246; grader/test_project.py:482-601)",
     "course/modules/M/M5/project.html:231-246; course/modules/M/M5/grader/test_project.py", "PASS",
     "Carried from round 8 (grader/*.py byte-identical since the previous pin ce7b382, verified by git diff ce7b382 b6865c7 -- course/modules/M/M5/grader empty): the grader file was not re-read this round. Fresh evidence: 92/92 pass on the reference, 50/50 seeds, and 3 new student-error mutants (m101-m103) killed. Gap: the 27 KB test file was not read line by line this round."),
 row("M5-d-R13", "stopping rule and certified error as stated in the specification (reference solver)",
     "course/modules/M/M5/project.html 'Certified error' and 'Stopping' paragraphs; grader/reference.py solve", "PASS",
     "The reference solver stops at the first sweep with factor x sup-norm change <= tol, as stated: on the F01 witness it stops at sweep 170 (certified 8.649e-12); the sweep-169 certified value 1.0129660e-11 is above tol and does not stop (m64_kill_r9.py). The reference is correct; the gap is in the tests (F01)."),
 row("M5-d-R14", "instance.py fixed inputs and starter contract",
     "course/modules/M/M5/grader/instance.py, starter.py", "PASS",
     "Carried from round 8 (instance.py and starter.py byte-identical since ce7b382); fresh: 50-seed run (run_graders.out) and mypy (mypy.out) on both files pass."),
 row("M5-d-R15", "alternative correct implementations are not over-constrained",
     "ledgers/M5/alternatives/alt1..alt5", "PASS",
     "Fresh (alternatives_r9.out): alt3, alt4, alt5 pass 92/92. alt1 (in-place sweep) and alt2 (residual stop) fail 6 tests each; both violate the stated conventions: 'Each sweep is synchronous' and 'the certified error is beta/(1-beta) times the change' (project.html Conventions). Rejection is spec-driven."),
 row("M5-d-R16", "project mutants: every mutant fails at least one test (tools/mutate_graders.py --unit M5 --seeds 0-9)",
     "ledgers/M5/mutants/*.py; course/modules/M/M5/grader/test_project.py", "FAIL",
     "`mutate_graders.py --unit M5 --seeds 0-9` -> `mutate_graders M5: FAIL (102/103 killed)` (mutate_M5_r9.out). The survivor is m64_change_measured_at_the_last_point_only.py (see F01). New mutants m101, m103 and m102 were all killed.",
     "Add a grader test that kills m64 on the F01 witness instance (grid (0.23, 0.24, 0.98, 1.46), beta 0.8535397019795181, alpha 0.3276562928132905, tol 1.0119307470200622e-11: correct solve gives iterations 170, converged True; m64 gives 169). See F01."),
 row("M5-d-R17", "new sentences at project.html:53 are supported by the labs and specification",
     "course/modules/M/M5/project.html:53", "PASS",
     "The one changed sentence ('the output from capital k, which the labs call its resources') is supported by the twin prints 'resources at k=...' (twin-project-1.out; lab line 43)."),
 row("M5-d-R18", "DAG: concepts used on project.html are inside the prerequisite closure",
     "course/modules/M/M5/project.html; tools/check_dag.py", "PASS",
     "Fresh `check_dag M5: PASS` (check_dag.out)."),
 row("M5-d-R19", "DAG and concept prose at project.html:500-505 (Reading and References)",
     "course/modules/M/M5/project.html:499-510", "PASS",
     "Cites data-cite abbott2015understanding and rudin1976principles, both registry keys (references/references.json lines 51 and 20388); the sentence 'Neither source below is cited for a specific statement' is honest. verify_refs --offline: `offline integrity: 560 entries, 0 problems` (verify_refs_offline.out)."),
 row("M5-d-R20", "no process words in learner text (project.html, grader docstrings, labs, cards.json)",
     "course/modules/M/M5/project.html; grader/*.py; tests/labs/M5/lab-M5-project-*.py; course/modules/M/M5/cards.json", "PASS",
     "Full project.html text and all 208 card fronts/backs read this round; no process words (round, verifier, builder, draft) in learner text. Grader and labs unchanged since ce7b382."),
 row("M5-d-R21", "cards.json structure: unique ids, prefix, lesson exists, keys, ascending ids, numbers present",
     "course/modules/M/M5/cards.json", "PASS",
     "208 cards, 208 unique ids, sorted, prefix M5-c; every lesson in L01-L10; key sets: 141 with grade and basis, 67 without; no duplicate fronts (python check, this round)."),
 row("M5-d-R22", "every card agrees with the CURRENT lesson text and carries the proposition's hypotheses",
     "course/modules/M/M5/cards.json (M5-c051); course/modules/M/M5/L04.html:240, :369, :454", "FAIL",
     "M5-c051 says 'A set F is closed when its complement is open'. L04 (changed since ce7b382, git diff) now defines closed sets with K: 'A set K subseteq X is closed when its complement X minus K is open' (L04 Section 2, line 240; Research 2 and quiz at :369, :454 rename F to K). Meaning identical; the symbol disagrees with the current lesson. All other cards were checked against their current lesson text (changed lesson hunks in L02-L07 read in full).",
     "Change M5-c051 to 'A set K is closed when its complement is open' (or to the lesson's wording of Section 2)."),
 row("M5-d-R23", "changed cards: c056, c102, c104, c106, c138, c143, c160, c201, c203-c212",
     "course/modules/M/M5/cards.json (15 changed + 3 added since ce7b382)", "PASS",
     "Each checked against current lesson text and lab output: c056 (L04 Prop 1.7 uses ell-infinity(S), line 139); c102 (L07 Def 1.2 closed-interval paragraph); c104 and c210 (L07 Thm 2.1 (a) exactly one fixed point, (b) x_n -> xbar); c106 and c211 (L07 Lemma 2.2, both claims); c138 (L08 Lab 1 Part A: V*(0.5)=5.176097, policy 0.25); c143 (L09 Lemma 1.2 text); c160 (L09 Remark 2.5); c201 (L04 Def 3.2); c203 (twin-L07 part C 0.009999); c204 (twin-L08 residual 8.695e-13); c205 (recomputed: 0.9 + 5.55e-16, 5 ulp; lesson line states 5.6e-16); c206 (twin-L08 V=500.000000); c207 and c208 (twin-L09 certified_stop and naive_step_stop lines); c209 (twin-L10 all_within_2_mesh True, 200 partitions); c212 (L08 Section 3: F(2) empty, sqrt 2 = 1.414 below both grid points)."),
 row("M5-d-R24", "every card number appears in its lesson; graded results on cards carry grade and basis",
     "course/modules/M/M5/cards.json; L01-L10", "PASS",
     "Scripted check: numbers on changed cards appear in their lesson (0.009999 L07; 500.000000 L08; 5.6 x 10^-16 L08; 0.0000085808 L09; 5.176097 L08). Recomputed: 40, 257, 527 iterations at beta 0.5, 0.9, 0.95 (c139) by running the L08 twin with BETA changed (c139_counts.py); 1.067e-6 at n=151 and 9.60e-7 at n=152 (c154)."),
 row("M5-d-R25", "named changed cards: no duplicate cards (round-8 F03 and R25 items)",
     "course/modules/M/M5/cards.json (c114, c115, c120, c135, c150, c160)", "PASS",
     "c150 is removed; c114 (L07 canon-breaks item 1) and c115 (L07 misconception 1) and c120 (lab 1 part C) each check against their lesson. c135 asks whether the grid fixed point is the continuous value (answer: no, discretisation error); c160 asks which object the certificate bounds (answer: V*). Different questions, no duplicate fronts."),
 row("M5-d-R26", "graded results on cards carry their grade and basis (BUILDER_RULES 7)",
     "course/modules/M/M5/cards.json (M5-c117, M5-c180)", "FAIL",
     "BUILDER_RULES 7: a card stating a result other than a theorem (a lab result) names its grade and basis. M5-c117 states the Lab 1 Part A quantities (error 5.439523e-2, bound 2.661258, ratio about 48.9) with grade null and no basis. M5-c180 states the Lab 1 Part C sums (0 and 1 at meshes 0.1 and 0.01) with grade null and no basis. The lab-result cards c203-c209 (round-8 R26 items) now carry grade C and a basis: FIXED since round 8.",
     "Add \"grade\": \"C\" and \"basis\": \"Lab 1 Part A (printed error and bound)\" to M5-c117; add \"grade\": \"C\" and \"basis\": \"Lab 1 Part C (step-integrator sums)\" to M5-c180."),
 row("M5-d-R27", "card agrees with the current lesson notation (L04 Proposition 1.7 uses ell-infinity)",
     "course/modules/M/M5/cards.json (M5-c056); L04.html Prop 1.7 line 139", "PASS",
     "M5-c056 now reads '(ℓ∞(S), d∞) is a metric space', matching L04 Proposition 1.7 '(\\ell^{\\infty}(S),d_{\\infty})'. Round-8 R27 is fixed. Notation registry: no conflict (ℓ∞(S) is local, not registered; notation/notation.json has no B(S) or F entry)."),
 row("M5-d-R28", "card rationale agrees with the lesson (c143: Lemma 1.2 of L09)",
     "course/modules/M/M5/cards.json (M5-c143); L09.html Lemma 1.2", "PASS",
     "M5-c143 now says 'Its statement is the same as part (a) of Theorem 2.2 of Lesson 8, and Section 1 proves it again.' L09 Lemma 1.2: 'This is part (a) of Theorem 2.2 of Lesson 8, and its proof is repeated so that this chain of results is complete on this page.' Agrees. Round-8 R28 is fixed."),
 row("M5-d-R29", "notation: every symbol in the slice is consistent with notation/notation.json",
     "course/modules/M/M5/project.html; grader; labs; cards.json; notation/notation.json", "PASS",
     "Registered symbols checked (R^\\ast, \\Phi, macros \\R and \\N used as registered). Symbols used in the slice (V^\\ast, \\mathcal{B}, beta, alpha, k_i, F(k) on L08/L09 cards, K and F as local letters) are not registered; no conflict with a registered meaning."),
 row("M5-d-R30", "DAG and prerequisites for the cards and project (cards cite only lessons of this unit or prerequisite modules)",
     "course/modules/M/M5/cards.json; check_dag M5", "PASS",
     "check_dag M5 PASS. Cross-unit cites checked: M5-c013 'M1, Lesson 2, Corollary 2.6' (course/modules/M/M1/L02.html: 'Corollary 2.6 (no rational number has square 2)', verified) and M5-c167 'M2 Lesson 9, Darboux' (M2/L09.html contains 'Darboux', verified)."),
 row("M5-d-F01", "grader mutant m64 (change measured at the last grid point only) must be killed: the stated rule is the largest absolute difference",
     "ledgers/M5/mutants/m64_change_measured_at_the_last_point_only.py; course/modules/M/M5/project.html:53 and the 'Stopping' paragraph; grader/test_project.py", "FAIL",
     "m64 survives all tests on seeds 0-9 and 0-49. It is NOT equivalent: witness grid (0.23, 0.24, 0.98, 1.46), beta 0.8535397019795181, alpha 0.3276562928132905, tol 1.0119307470200622e-11. At sweep 169 the last-point certified value is 1.0119307e-11 (<= tol) while the sup-norm certified value is 1.0129660e-11 (> tol). Reference solve: 170 iterations, converged True, certified 8.649e-12. m64: 169 iterations (m64_kill_r9.py). The page states the change is the largest absolute difference (project.html:53) and that solve stops at the first sweep with certified_error <= tol ('Stopping'). Random search over 374k grids at change > 1e-4 found no last-point shortfall (m64_search_r9.py), which is why round 8 found no witness; the shortfall appears at change scale 1e-13 (m64_search_r9b.py).",
     "Add a grader test on the witness instance above: solve(params, grid, 1.0119307470200622e-11, 400) must give iterations 170, converged True, certified_error about 8.649e-12. Alternatively a test that compares solve's stop sweep with the sup-norm rule on the witness. Then m64 is killed on seed 0."),
 row("M5-d-F02", "tolerance 1e-10 stated in the specification (round-6 F02)",
     "course/modules/M/M5/project.html 'Inputs' and Lab 3; tests/labs/M5/lab-M5-project-3.py", "PASS",
     "Lab 3 prints at tolerance 1e-10 (twin-project-3.out); the spec and the report use 1e-10 (project.html Inputs)."),
 row("M5-d-F03", "no duplicate cards (round-8 F03: c114/c150 and c135/c160)",
     "course/modules/M/M5/cards.json", "PASS",
     "c150 removed; c135 and c160 now ask different questions (see R25). No duplicate fronts or ids (R21)."),
]

mut_extra = [
 {"name": "m101_certificate_compares_with_two_sweeps_back.py",
  "description": "Student-error mutant (round 9): the certified change compares the new sweep with the vector two sweeps back.",
  "killed_by": "test_certified_error_is_beta_over_one_minus_beta_times_the_last_change[2-0] (seed 0)"},
]
frag = {
 "unit": "M5",
 "slice": "d",
 "round": 9,
 "verifier": "Haiku independent verifier (round 9), no build context",
 "pin": "b6865c7d10020e31b9858a49edf751f4b814c031",
 "base": "44f1eb6",
 "checkout": str(root),
 "scratch": str(S),
 "verified_at": datetime.datetime.now(datetime.UTC).replace(microsecond=0).isoformat(),
 "verdict": "FAIL",
 "rows": rows,
 "mutants": mutants,
 "registry_flags": [
   "references: verify_refs --offline 560 entries, 0 problems (verify_refs_offline.out); the two cited keys exist",
   "notation: no symbol in the slice conflicts with notation/notation.json (R29)",
   "out of slice: tests/test_labs.py has 11 failures for unit E3 (missing tests/labs/E3 twins in this checkout); all M5 cases pass (pytest_M5.out)"],
 "freshness_flags": [
   "since ce7b382: project.html changed at line 53 only; grader/*.py, instance.py, starter.py, labs project twins unchanged; lesson pages L02-L07 and cards.json changed (re-read); mutants m98-m100 from round 8 present; m101-m103 added this round",
   "grader/test_project.py, instance.py, starter.py not re-read line by line this round (byte-identical since ce7b382; carried, see R12/R14)"],
 "notes": [
   "F01 is the only grader defect; the three new mutants are killed (mutate_M5_r9.out).",
   "Mutant m64 may look equivalent on seeds 0-49 and on random grids; the witness above shows it is not.",
   "alt1 and alt2 fail by specification (synchronous sweep; beta/(1-beta) times the change), not over-constraint.",
   "Not checked: the 120-second in-browser runtime claim; full line-by-line re-read of grader/test_project.py (carried by byte identity); lesson texts L01, L08-L10 read only at the card-referenced passages; the cited M1/M2 locators were checked only for existence and content keywords."
 ],
 "summary": "Slice d round 9: FAIL. 33 rows: 29 PASS, 4 FAIL (R16, R22, R26, F01). Mutants: 103 (102 killed; m64 survives). Fixes: kill m64 with the witness instance; c051 F->K; add grade/basis to c117 and c180. Project-side gates (check_projects, run_labs 13/13, run_graders 50/50, collect 92, page_smoke project, ruff, mypy, verify_refs offline) pass.",
}
out = root / "ledgers/M5/M5-d.json"
out.write_text(json.dumps(frag, ensure_ascii=False, indent=2), encoding="utf-8")
print("rows", len(rows), "mutants", len(mutants), "PASS", sum(r["status"]=="PASS" for r in rows))
