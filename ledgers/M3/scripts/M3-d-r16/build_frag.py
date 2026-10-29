import json, datetime
C = "Carried from round 15 (files byte-identical since the previous pin 448548f): "
rows = []
def row(id_, check, location, status, evidence, fix=None):
    r = {"id": "M3-d-" + id_, "check": check, "location": location, "status": status, "evidence": evidence}
    if fix: r["fix"] = fix
    rows.append(r)

carry_src = "project.html, grader/*, tests/labs/M3/lab-M3-project-*.py unchanged; round-15 evidence stands"
carried = {
 "R01": ("Lab 1 twin output equals page expected block; page code equals twin", "course/modules/M/M3/project.html lines 131-137; tests/labs/M3/lab-M3-project-1.py", "run_labs M3 re-run this round: PASS (12/12), see R44 evidence"),
 "R02": ("Lab 2 completion: blanks at Step 3 and Step 5; completed code and output match", "project.html lines 214-220", "round-15 hunk check; the Lab 2 block is untouched in 448548f..5e88c50"),
 "R03": ("Lab 3 printed numbers recomputed independently", "project.html lines 460-468; ledgers/M3/scripts/M3-d-r13/numbers_check.py", "numbers unchanged; equivalence check ledgers/M3/scripts/M3-d-r16/equiv_check.out agrees with the printed projection distance family"),
 "R04": ("Lab 3 hypothesis sentence", "project.html line 289", "project.html unchanged"),
 "R05": ("Lab 1 and Lab 2 interpretation prose numbers", "project.html interpretation paragraphs after Lab 1 and Lab 2", "project.html unchanged"),
 "R06": ("Lab 3 interpretation prose", "project.html line 469", "project.html unchanged"),
 "R07": ("Spec constants: test count; PSD tolerances; ValueError conditions", "project.html lines 233-237", "project.html unchanged; test count re-collected: see R46"),
 "R08": ("Convention and appendix math: A1 to A4", "project.html lines 481, 597, 635-637", "project.html unchanged"),
 "R09": ("Rubric row C1 and exemplar scores", "project.html line 492", "project.html unchanged"),
 "R10": ("Exemplar A and B passages and annotations", "project.html lines 597, 635-637, 622", "project.html unchanged"),
 "R11": ("Hours: hub split and lesson hours arithmetic", "project.html lines 258-264; course/modules/M/M3/index.html line 42", "project.html and index.html unchanged"),
 "R16": ("Docstrings and spec for comparison_weights and projection_repair", "grader/reference.py lines 109, 131; project.html line 361", "grader and project.html unchanged"),
 "R17": ("Grader tests on the page's 'what the suite checks' claims", "grader/test_project.py lines 241-245, 319-326, 508, 552-560; project.html line 237", "grader/test_project.py unchanged; 154 tests collected and passing this round (R46)"),
 "R18": ("Notation: symbols on changed page vs notation/notation.json", "project.html lines 481, 492, 597, 635-637, 660", "project.html unchanged"),
 "R25": ("Reading list and references: registry keys exist and verify offline", "project.html reading section; references/references.json", "verify_refs.py --offline re-run: '560 entries, 0 problems' (ledgers/M3/scripts/M3-d-r16/verify_refs_offline.log)"),
 "R26": ("Lede and conventions prose numbers and claims", "project.html line 37; lines 243-247", "project.html unchanged"),
 "R27": ("Lab 3 expected block equals twin output", "project.html Lab 3 expected block; tests/labs/M3/lab-M3-project-3.py", "run_labs M3 PASS (12/12) this round"),
 "R28": ("Rubric row C1 and exemplar B annotations", "project.html line 492; exemplar B annotations", "project.html unchanged"),
 "R29": ("Round-10 FAIL cards c143, c145, c161, c165 cleared", "cards.json M3-c143, c145, c161, c165", "cards unchanged for these ids in 448548f..5e88c50; c161 and c165 cite L09 text, which changed at L09 lines 206 and 320-343 but not at Proposition 3.3 or Example 2.3 (checked by diff)"),
 "R30": ("Cards carried from earlier rounds still match their lessons", "cards.json c094, c101, c104, c133, c142, c153 and others", "unchanged ids; card-number-in-lesson check re-run this round over all 186 cards: 0 numbers absent from their lesson (R54)"),
 "R31": ("Hours arithmetic and Lab 3 interpretation cross-references", "project.html lines 258-264 and 469", "project.html unchanged; hub split arithmetic unchanged (R11)"),
 "R32": ("Card M3-c040 back vs L02 Misconception 1", "cards.json M3-c040; course/modules/M/M3/L02.html", "L02.html and the card unchanged"),
 "R33": ("Card M3-c093 back lists the eigenvalues asked by its front", "cards.json M3-c093; course/modules/M/M3/L05.html", "L05.html and the card unchanged"),
 "R34": ("Process words in learner-visible Lab 2 docstring", "project.html Lab 2 docstring (line 144)", "project.html unchanged"),
 "R35": ("comparison_weights refuses a volatility not strictly greater than zero", "grader/reference.py comparison_weights; grader/test_project.py weights tests", "grader unchanged; mutants fx02, b2d_m07, r8d_m01 killed in the gate re-run (R15)"),
 "R38": ("Lab 1 composition claim in card M3-c184 and lesson text", "cards.json M3-c184 (line 1287); course/modules/M/M3/L02.html", "card and L02.html unchanged"),
 "R39": ("Card M3-c183 (new) vs L09 Proposition 3.3(a) and Example 3.6", "cards.json M3-c183 (line 1280); course/modules/M/M3/L09.html", "L09 hunks changed at lines 206 and 326-343 (Lab 1 description and its printed line); Proposition 3.3 and Example 3.6 text unchanged; card text 0.04 matches Example 3.6 entries -0.1 and 0.1"),
 "R41": ("New student-error grader mutants r13d_m01, m02, m04, m05: killed", "ledgers/M3/mutants/r13d_m01, m02, m04, m05", "re-run in the full mutation gate this round: all killed (R15 gate)"),
 "R43": ("Mutant r13d_m03 (sign-flipped unit-diagonal Dykstra correction) is equivalent", "ledgers/M3/mutants (file absent at 448548f)", "absent from mutants/ this round, unchanged ruling"),
}
for k, (chk, loc, ev) in carried.items():
    row(k, chk, loc, "PASS", C + ev if k not in ("R25","R30","R35") else C + ev)
# re-run or changed-subject rows
row("R12", "Reference solution passes the suite on 50 seeds; collect count", "course/modules/M/M3/grader/reference.py; tools/run_graders.py", "PASS",
    "tools/run_graders.py --unit M3 --seeds 0-49 -> 'run_graders M3: PASS (reference 50/50 seeds, slowest 0.2 s)' (ledgers/M3/scripts/M3-d-r16/run_graders_M3.log). Suite on reference: 154 passed (R46).")
row("R13", "Stopping-rule survivors r6d_m04, r11d_m02, r15d_m03: violation of a stated behaviour?", "ledgers/M3/equivalent/*.py (moved from mutants/ at 5e88c50); project.html lines 233, 622, 660", "PASS",
    "Ruling confirmed by measurement, not by assertion: equiv_check.py over 200 random unit-diagonal inputs (n=3..6) gives max entry difference from reference 3.0e-11 (r6d_m04), 2.3e-11 (r11d_m02), 4.7e-11 (r15d_m03); all outputs keep unit diagonal exactly and min eigenvalue >= -6.4e-11 (within is_psd tol 1e-10). The page states the output properties (line 233) and no stop criterion; project.html line 622 says 'The suite checks the result, not the stopping rule'. Honest limit: at tol=1e-3 on a 4x4 input the reference and r15d_m03 differ by 8.7e-5 entrywise (tol_check.out), so the stretch exercise at line 660 would show a tol effect the mutant does not have; no stated grader behaviour is violated, so the ruling stands.")
row("R14", "Six alternative correct implementations pass 50 seeds", "ledgers/M3/alternatives/alt1..alt6", "PASS",
    "run_alts16.sh over alt1..alt6, seeds 0-49, current grader: all 6 'pass=50 fail=0' (ledgers/M3/scripts/M3-d-r16/alts_r16.out).")
row("R15", "Every existing mutant is killed or ruled; kill records accurate", "ledgers/M3/mutants (117 files now)", "PASS",
    "mutate_graders.py --unit M3 --seeds 0-49 -> 'mutate_graders M3: PASS (117/117 killed)', exit 0 (ledgers/M3/scripts/M3-d-r16/mutate_m3_r16_with_new.out). The three ruled survivors are outside mutants/ in ledgers/M3/equivalent/ (README there).")
row("R19", "DAG and concept links from the page", "project.html Lesson 4 links, F1-F4 references; check_dag output", "PASS",
    "check_dag.py --unit M3: 'check_dag M3: PASS' (ledgers/M3/scripts/M3-d-r16/check_dag_M3.log).")
row("R20", "Structure gates: check_pages, check_dag, check_projects, page_smoke", "tools/check_pages.py, check_dag.py, check_projects.py, page_smoke.py", "PASS",
    "check_pages M3 PASS, check_dag M3 PASS, check_projects M3 PASS (ledgers/M3/scripts/M3-d-r16/*_M3.log); page_smoke --pages project --skip-labs: 'page_smoke modules/M/M3/project.html: PASS' (page_smoke_project.log). Browser run of the 120-second limit not measured.")
row("R21", "cards.json structure: unique ids, lesson names, cites, every lesson has cards", "course/modules/M/M3/cards.json (186 cards)", "PASS",
    "Python check: 186 cards, 186 unique ids, 0 duplicate fronts, 0 duplicate backs, lessons L01..L09 all present, keys as expected (108 with grade T, 39 with grade C plus basis, 39 without grade: definitions and misconceptions, which BUILDER_RULES section 7 does not require to carry a grade).")
row("R22", "Changed and carried cards: content matches the current lesson", "cards.json c126 (line 875), c127 (line 883), c175 (L09, see R49), c369, c936, c1022, c1290-1302", "PASS",
    "Re-verified c126 and c127 against L07.html current text (line 131 'does not check its rank', line 219 misconception, line 198 printed 0.8951): PASS. c054, c135, c147, c185, c186 bytes unchanged since the previous pin (diff shows only c126 and c127 changed).")
row("R23", "Grade C cards carry a basis or cite; grade rules", "cards.json (grade counts)", "PASS",
    "Re-counted: T 108, C 39, no grade 39; every C card has a basis (39 of 39). Matches BUILDER_RULES section 7.")
row("R24", "Lesson hunks cited by changed cards agree with the card text", "course/modules/M/M3/L07.html lines 131, 198, 219; cards c126, c127", "PASS",
    "L07.html line 131 ('does not check its rank') and line 219 (misconception rewording with 'Assuming F1 to F4 of Lesson 4') match c127 and c126. The old line 208/218 locators are stale; new locators used.")
row("R36", "New student-error grader mutants (at least three) are killed", "ledgers/M3/mutants/r14d_m01..m03", "PASS",
    "Re-run in the 117-mutant gate: r14d_m01..m03 KILLED (ledgers/M3/scripts/M3-d-r16/mutate_m3_r16_with_new.out).")
row("R37", "Alternatives and mutants re-run on the current grader", "ledgers/M3/alternatives; ledgers/M3/mutants (all)", "PASS",
    "Alternatives 6/6 pass 50/50 (R14); mutant gate 117/117 killed exit 0 (R15).")
row("R40", "mutate_graders M3 gate exit status", "tools/mutate_graders.py --unit M3 --seeds 0-49", "PASS",
    "Round-15 FAIL cleared: exit status 0 with 117/117 killed, because the three ruled survivors now sit in ledgers/M3/equivalent/ (ledgers/M3/scripts/M3-d-r16/mutate_m3_r16_with_new.out, last line 'mutate_graders M3: PASS (117/117 killed)' and 'exit=0').")
row("R42", "Six alternative correct implementations pass 50 seeds on the current grader", "ledgers/M3/alternatives/", "PASS",
    "Same run as R14: 6 of 6 implementations pass 50 of 50 seeds.")
row("R44", "Lab 3 and project labs run under -I -W error", "tests/labs/M3/lab-M3-project-1..3.py; lab-M3-L01..L09", "PASS",
    "run_labs.py --unit M3: 'run_labs M3: PASS (12/12)' (ledgers/M3/scripts/M3-d-r16/run_labs_M3.log). This covers the 9 lesson labs and the 3 project labs; the L07 and L09 twins changed since the previous pin and are re-run here.")
row("R45", "Gates: ruff, format, mypy strict, verify_refs, build_site, render_curriculum", "repo root; M3 files", "PASS",
    "ruff check . -> 'All checks passed!'; ruff format --check on grader and labs -> 16 files already formatted; run_graders M3 checks reference, starter and instance under mypy --strict (PASS). The repo mypy scope is tools and tests (pyproject.toml), so the grader is checked by run_graders. verify_refs --offline: 560 entries, 0 problems. build_site and render_curriculum not re-run (no M3 generator input changed except cards.json, which is not generated).")
row("R46", "Test-count and grader collection claim", "project.html line 237 ('154 tests'); grader/test_project.py", "PASS",
    "pytest --collect-only -q on the grader copy: '154 tests collected'; reference run 154 passed (ledgers/M3/scripts/M3-d-r16/collect.log).")
row("R47", "Card M3-c127 agrees with the current L07 misconception text", "cards.json line 883; course/modules/M/M3/L07.html line 219", "PASS",
    "Current L07 line 219 reads 'Assuming F1 to F4 of Lesson 4, the residual is orthogonal to the columns of A, not zero...', matching c127 back text.")
row("R48", "New student-error grader mutants (round 15): killed by the suite", "ledgers/M3/mutants/r15d_m01, r15d_m02 (r15d_m03 moved to equivalent/)", "PASS",
    "r15d_m01 and r15d_m02 KILLED in the current gate (ledgers/M3/scripts/M3-d-r16/mutate_m3_r16_with_new.out). r15d_m03 is a ruled non-violation (R13).")
# new rows
row("R49", "Card M3-c175 front matches the current L09 Lab 1 criterion", "course/modules/M/M3/cards.json M3-c175 (front); course/modules/M/M3/L09.html lines 206, 263-272, 326, 343",
    "FAIL",
    "Commit 5e88c50 changed L09 Lab 1 so that the lab counts 'passes is_correlation (symmetric and unit diagonal to 1e-12, smallest eigenvalue at least -1e-8)' (L09.html lines 206, 325-326, 343). Card M3-c175 front still asks whether the output 'is a correlation matrix to within 1e-8', a different criterion (tolerance 1e-8 for symmetry and diagonal, which the lesson no longer uses). Its back 'All 23 of 23' is still the printed value.",
    fix="Edit cards.json M3-c175 front to: 'Of the 23 non-PSD seeded matrices, how many have an alternating-projection output that passes is_correlation (symmetric and unit diagonal to 1e-12, smallest eigenvalue at least -1e-8)?' Keep the back. Re-run check_pages --unit M3 and the card-number check.")
row("R50", "Ruled survivors: is the ruling honest (no stated behaviour violated)", "ledgers/M3/equivalent/README.md; project.html lines 233, 622, 660", "PASS",
    "README rounds 6, 11 and 15 agree with R13 measurements. The exploratory line 660 asks the student to report how tol and max_iter change the answer, but states no stopping criterion or required value, so the moved mutants are not violations of a stated behaviour. Verifier judgment: the stretch item is the only place tol matters for the spec; recorded as a judgment in the notes.")
row("R51", "Three new student-error grader mutants authored and killed", "ledgers/M3/mutants/r16d_m01_is_psd_tolerance_scaled_by_spectrum.py; r16d_m02_min_eigenvalue_prints_its_value.py; r16d_m03_clip_repair_writes_back_into_argument.py", "PASS",
    "Each is a complete module derived from reference.py with one assertion-checked edit. r16d_m01 (tolerance scaled by largest |eigenvalue|) KILLED by test_is_psd_tolerance_is_not_scaled_by_the_diagonal (seed 0); r16d_m02 (print in min_eigenvalue) KILLED by test_functions_print_nothing (seed 0); r16d_m03 (clip_repair writes into its argument) KILLED by test_lab3_reference_numbers_are_matched (seed 0). Spec sentences: project.html line 233 (is_psd: at least -tol), line 235 ('No function prints or warns'; 'No function changes its arguments').")
row("R52", "Equivalence check of the ruled survivors on random inputs", "ledgers/M3/scripts/M3-d-r16/equiv_check.py", "PASS",
    "200 random unit-diagonal inputs (n in 3..6): entry differences to reference 3.0e-11, 2.3e-11, 4.7e-11; diag deviation 0; min eigenvalue >= -7.6e-11 (ledgers/M3/scripts/M3-d-r16/equiv_check.out).")
row("R53", "Stop-rule sensitivity at several tol values on one 4x4 input", "ledgers/M3/scripts/M3-d-r16/tol_check.py", "PASS",
    "tol 1e-10: diff 7.7e-12; tol 1e-6: diff 8.2e-8; tol 1e-3: diff 8.7e-5 (reference distance 0.863504 vs mutant 0.863670). Recorded so the ruling is not overstated; see R13.")
row("R54", "Card numbers appear in their lesson text; no duplicate cards", "cards.json (186 cards) against L01..L09.html", "PASS",
    "Python check over all decimals and integers >= 10 in card fronts and backs: 0 absent from the card's own lesson text (ledgers/M3/scripts/M3-d-r16 check output embedded in the round notes).")
row("R55", "Mutation gate and alternatives on the current pin (full M3 gate)", "tools/mutate_graders.py --unit M3 --seeds 0-49", "PASS",
    "Re-run: exit 0, 117/117 killed (R15). Alternatives 6/6 (R14). Reference 50/50 (R12).")

frag = {
 "unit": "M3", "slice": "d", "round": 16,
 "verifier": "independent verifier (Claude Haiku 5.5), unit M3 slice d, round 16",
 "pin": "5e88c50",
 "base": "round-15 fragment /Users/billyribeiro/.fanout/frags/B-M3-d.round15.json (pin 448548f)",
 "checkout": "/Users/billyribeiro/.fanout/wt/verifyB16-M3-d",
 "scratch": "ledgers/M3/scripts/M3-d-r16/",
 "verified_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
 "verdict": "FAIL",
 "rows": rows,
 "mutants": [
  {"id": "r16d_m01_is_psd_tolerance_scaled_by_spectrum", "description": "is_psd scales the tolerance by the largest absolute eigenvalue, so it is looser for large matrices.", "killed_by": "test_is_psd_tolerance_is_not_scaled_by_the_diagonal (seed 0)"},
  {"id": "r16d_m02_min_eigenvalue_prints_its_value", "description": "min_eigenvalue prints its result as a debugging aid, which the specification forbids.", "killed_by": "test_functions_print_nothing (seed 0)"},
  {"id": "r16d_m03_clip_repair_writes_back_into_argument", "description": "clip_repair overwrites the caller matrix with the repaired values, changing its argument.", "killed_by": "test_lab3_reference_numbers_are_matched (seed 0)"},
  {"id": "r6d_m04_projection_stops_on_gap_only (now ledgers/M3/equivalent/)", "description": "projection_repair stops on the gap test only.", "killed_by": "SURVIVES 50/50; ruled non-violation (R13, R52, R53)"},
  {"id": "r11d_m02_projection_stops_on_step_only (now ledgers/M3/equivalent/)", "description": "projection_repair stops on the step test only.", "killed_by": "SURVIVES 50/50; ruled non-violation (R13, R52)"},
  {"id": "r15d_m03_projection_repair_no_final_symmetry (now ledgers/M3/equivalent/)", "description": "projection_repair never stops on the tol test; runs to max_iter.", "killed_by": "SURVIVES 50/50; ruled non-violation (R13, R52, R53)"},
  {"id": "gate_mutate_graders_M3_r16", "description": "tools/mutate_graders.py --unit M3 --seeds 0-49 over 117 mutants in ledgers/M3/mutants", "killed_by": "117/117 KILLED, exit 0"},
  {"id": "alternatives_alt1_to_alt6_r16", "description": "six correct alternative implementations (numpy and Jacobi/Cholesky variants) on the current grader", "killed_by": "not a mutant (over-constraint check): 50/50 pass each"}
 ],
 "registry_flags": [],
 "freshness_flags": [
  "Round-16 delta from pin 448548f to 5e88c50 for slice d: course/modules/M/M3/cards.json (c126 line 875, c127 line 883); course/modules/M/M3/L07.html (lines 131, 219); course/modules/M/M3/L09.html (lines 206, 326, 343); tests/labs/M3/lab-M3-L07-1.py and lab-M3-L09-1.py (not project labs); ledgers/M3/equivalent/ (three mutants moved from mutants/); ledgers/M3/mutants/ (three new mutants r15d_m01..m02 kept, r16d_m01..m03 added). project.html, grader/*, tests/labs/M3/lab-M3-project-1..3.py byte-identical since 448548f (git diff --stat empty for those paths)."
 ],
 "notes": [
  "Verdict FAIL is driven by R49 only (card M3-c175 stale against the current L09 Lab 1 criterion). Every other row is PASS; the R40 gate failure from round 15 is cleared.",
  "Ruling on the three moved mutants is confirmed (R13, R50, R52, R53) as a judgment: no stated grader behaviour is violated, but the stretch item at project.html line 660 would show a tol effect (8.7e-5 at tol 1e-3 on a 4x4 input) that r15d_m03 does not show. Overrule only if the spec is amended to fix a stopping rule.",
  "Not checked: the 120-second browser run limit (project.html line 235) was not timed; page_smoke was run with --skip-labs for the project page only. Full repo pytest, the repo-wide mypy gate, build_site and render_curriculum were not run (outside the targeted set for this slice). The grader pytest suite was run in a scratch copy with reference.py as covariance_doctor.py because the checkout has no covariance_doctor.py.",
  "Lab 1 of L09 and Lab 1 of L07 were not verified as a slice owner; only their effect on cards in this slice (c126, c127, c175, c163, c183) was checked.",
  "Tool note: the first background run of mutate_graders wrote nothing because the redirect ran before mkdir; the reported runs are the foreground re-runs."
 ],
 "summary": "M3 slice d round 16: FAIL with 1 non-PASS row (R49, card M3-c175 front stale against the L09 Lab 1 is_correlation criterion; fix given). Mutation gate now exits 0 at 117/117 killed (round-15 R40 cleared). Three new student-error mutants (r16d_m01..m03) killed. Alternatives 6/6 at 50/50 seeds. Reference 50/50; collect 154 tests. Moved survivors r6d_m04, r11d_m02, r15d_m03 confirmed as non-violations with measured equivalence (1e-11 level at tol 1e-10), with the tol-sensitivity caveat recorded. Fragment: ledgers/M3/M3-d.json."
}
json.dump(frag, open("/Users/billyribeiro/.fanout/wt/verifyB16-M3-d/ledgers/M3/M3-d.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("rows", len(rows), "non-PASS", [r["id"] for r in rows if r["status"] != "PASS"])
