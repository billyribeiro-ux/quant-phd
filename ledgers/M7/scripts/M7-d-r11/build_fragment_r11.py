"""Round 11 (M7-d): writes ledgers/M7/M7-d.json from the commands and logs of this round's scripts directory."""
import json, pathlib, re, datetime

ROOT = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyB11-M7-d")
S = "ledgers/M7/scripts/M7-d-r11/"
S_R10 = "ledgers/M7/scripts/M7-d-r10/"
C = "Carried from round {n} ({what}):"

def carry(n, what, text):
    return C.format(n=n, what=what) + " " + text

rows = []
def row(id_, check, location, status, evidence, fix=None):
    r = {"id": id_, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    rows.append(r)

# --- structure and gates (fresh this round)
row("PRJ-R6-01", "tools/check_projects.py --unit M7", "tools/check_projects.py", "PASS",
    "check_projects M7: PASS, exit 0 (" + S + "check_projects.log)")
row("PRJ-R6-02", "tools/check_pages.py --unit M7 (hours, ladder, data-hours)", "tools/check_pages.py", "PASS",
    "check_pages M7: PASS, exit 0 (" + S + "check_pages.log)")
row("PRJ-R6-03", "tools/check_dag.py --unit M7 (concept links)", "course/modules/M/M7/project.html", "PASS",
    "check_dag M7: PASS, exit 0 (" + S + "check_dag.log)")
row("PRJ-R6-04", "run_graders reference, seeds 0-49", "course/modules/M/M7/grader/reference.py", "PASS",
    "run_graders M7: PASS (reference 50/50 seeds, slowest 3.3 s), exit 0 (" + S + "run_graders.log)")
row("PRJ-R6-05", "starter fails the suite", "course/modules/M/M7/grader/starter.py", "PASS",
    "starter.py as constrained_allocator.py, seed 0: '360 failed, 3 passed' (" + S + "starter_fails.log)")
row("PRJ-R6-06", "collected test count equals the page's 363 for every seed", "course/modules/M/M7/project.html line 329; grader/test_project.py", "PASS",
    "pytest --collect-only with reference solution in scratch copies, seeds 0-9: '363 tests collected' for every seed (" + S + "collect_r11.log)")
row("PRJ-R6-07", "all M7 lab twins via run_labs", "tests/labs/M7/", "PASS",
    "run_labs M7: PASS (11/11), exit 0 (" + S + "run_labs.log)")
row("PRJ-R6-08", "project twins under python -I -W error; stdout equals page expected block", "course/modules/M/M7/project.html; tests/labs/M7/lab-M7-project-1..3.py", "PASS",
    "run_labs M7 (11/11) covers the three project twins against their expected blocks; tools/embed_labs.py --refresh on a copy of project.html leaves it IDENTICAL (" + S + "embed_refresh_copy.log)")
row("PRJ-R6-09", "page code equals twin (lab 1, lab 2, lab 3)", "course/modules/M/M7/project.html lines 56-154, 172-270, 372-434", "PASS",
    "embed_labs --refresh on a copy of project.html: diff against the page empty (" + S + "embed_refresh_copy.log)")
row("PRJ-R6-10", "Lab 1 numbers re-derived", "course/modules/M/M7/project.html lines 155-166", "PASS",
    carry(10, "project.html lines 155-166 byte-identical since e8b10b8; changed hunks are 293, 355, 474", "round-10 PRJ-R6-10 numbers (budget-only 54/65, 5/26, -3/130; objective -3/220) re-run this round in the lab twin by run_labs PASS"))
row("PRJ-R6-11", "Lab 3 residual claims re-derived", "course/modules/M/M7/project.html lines 435-438", "PASS",
    carry(10, "lines 435-438 byte-identical since e8b10b8", "lab-M7-project-3 output this round: check B dual 9/1100 and stationarity 9/550; check C stationarity 1/6250 (" + S + "embed_refresh_copy.log plus run_labs)"))
row("PRJ-R6-12", "certificate definitions (page 306-316) match the grader recomputation", "project.html lines 306, 313, 315; grader/test_project.py lines 85-115", "PASS",
    carry(10, "project.html lines 306, 313, 315 and grader/ byte-identical since e8b10b8", "definitions match reference.py _certificate and test_project.py recomputed_certificate (lines 85-115); reference agrees, 50 of 50 seeds (run_graders PASS)"))
row("PRJ-R6-13", "sufficiency proposition and uniqueness proof (page 320-322)", "project.html lines 320-322", "PASS",
    carry(10, "project.html lines 320-322 byte-identical since e8b10b8", "no hunk touches them in e8b10b8..f42f432"))
row("PRJ-R6-14", "linearization of turnover constraint", "project.html line 307", "PASS",
    carry(10, "line 307 byte-identical since e8b10b8", "no hunk touches it"))
row("PRJ-R6-15", "five hand-worked answers are correct", "course/modules/M/M7/grader/test_project.py lines 218-246", "PASS",
    carry(10, "grader/ byte-identical since e8b10b8", "the five hand cases pass for reference and for the five correct alternatives on seeds 0-49 (PRJ-R6-32)"))
row("PRJ-R6-16", "named ValueError conditions have refused and accepted tests", "grader/test_project.py lines 553-567, 590-596, 670-693, 697-", "PASS",
    carry(10, "grader/ byte-identical since e8b10b8", "collect count 363 and reference pass re-run this round (PRJ-R6-06, PRJ-R6-04)"))
row("PRJ-R6-17", "instances SIMULATED, feasible by construction, <=3 decimals, both sectors non-empty", "course/modules/M/M7/grader/instance.py lines 34-68", "PASS",
    carry(10, "instance.py byte-identical since e8b10b8", "fresh check this round: n in {3,4,5} and K = 2 over seeds 0-1999 (" + S + "n_k_range.log)"))
row("PRJ-R6-18", "solution may use standard library only; no grader import", "grader/test_project.py lines 268-282", "PASS",
    carry(10, "grader/ byte-identical since e8b10b8", "suite passes for the five alternatives, each of which imports only the standard library (" + S + "alt_lu_0-49.log)"))
row("PRJ-R6-19", "ruff check and format on the labs and grader; mypy strict", "tests/labs/M7; course/modules/M/M7/grader", "PASS",
    "ruff check tests/labs/M7 course/modules/M/M7/grader: All checks passed; ruff format --check: 15 files already formatted; mypy --no-incremental (whole repo, strict config): Success, 255 source files (" + S + "ruff.log, " + S + "mypy.log)")
row("PRJ-R6-20", "reading-list keys resolve in the registry (offline integrity)", "course/modules/M/M7/project.html lines 459-460; references/references.json", "PASS",
    "tools/verify_refs.py --offline: '560 entries, 0 problems', exit 0 (" + S + "verify_refs.log)")
row("PRJ-R6-21", "page_smoke M7 project (render and in-browser grader)", "course/modules/M/M7/project.html", "PASS",
    "page_smoke.py --unit M7 --pages project.html --skip-sweep: PASS, exit 0 (" + S + "page_smoke_project.log); sweep not run this round")
row("PRJ-R6-22", "hours: project components sum to 33; lessons 77 + project 33 = 110", "project.html lines 337-351; index.html data-hours", "PASS",
    "check_pages M7 PASS (" + S + "check_pages.log); hour lines unchanged in e8b10b8..f42f432")
row("PRJ-R6-23", "no process words in learner text", "project.html (changed lines 293, 355, 474); cards.json (changed cards)", "PASS",
    "grep over project.html and cards.json for round, verifier, builder, TODO, draft, we, our, pending: no match in the current files; changed sentences read in full")
row("PRJ-R6-24", "notation: symbols vs notation/notation.json", "project.html lines 303-308", "PASS",
    "lines 303-308 byte-identical since e8b10b8; symbols there are in notation/notation.json or macros (the new symbol K on line 293 is handled by PRJ-R11-01)")
row("PRJ-R6-25", "cards: numbers on each back appear in the card's own lesson; no duplicate ids or fronts", "course/modules/M/M7/cards.json (158 cards)", "PASS",
    "cards_numbers_r11.py (" + S + "cards_numbers_r11.log): 15 tokens absent as literal text, all present in their lesson as LaTeX \\tfrac forms (e.g. c026 '2/3' as \\tfrac23 in L02; c043 '1/8' as \\tfrac18 in L03); no duplicate ids or fronts; grades T and C, every C has a basis")
row("PRJ-R6-26", "cards: numeric claims re-derived or matched to lab output", "course/modules/M/M7/cards.json (c113, c114, c112, c131, c175)", "PASS",
    "c113 difference of exact objectives at gamma 16 = 45792167194081/80020586406000 = 0.5722548315, card says 0.5722548; c114 exact turnover at gamma 4 = 67597/120955 = 0.5588607333, card says 0.5588607 (" + S + "exact_c113_c114.log, computed with the L06 twin's own Fraction functions; the lab still prints only six places)")
row("PRJ-R6-27", "notation glyph 1 (all-ones) vs registry macro", "course/modules/M/M7/project.html lines 306, 313", "PASS",
    carry(10, "lines 306 and 313 byte-identical since e8b10b8", "no change"))
row("PRJ-R6-28", "dual residual floor at zero is exercised by the suite (spec line 315)", "grader/test_project.py lines 105-116, 365-369; grader/reference.py line 287; project.html line 315", "FAIL",
    "minimum inequality multiplier of the reference certificate is 0.0 on 50 of 50 seeds (" + S + "minmult_r11.log); so max(0, -min) = 0 on every reference output and the floor branch is never active on any output the suite can produce from a correct solution. Mutant q04 (no floor) survives (PRJ-R6-31). The line-315 floor is only observable on a student output whose inequality multipliers are all strictly positive, which the suite never requests.",
    "Either state on page 315 that the dual residual is -min over the inequality multipliers with dual feasibility checked separately (the floor is then a no-op for any answer that passes dual feasibility), or add an instance on which every inequality multiplier is forced to be strictly positive (none exists for the non-degenerate instances the generator makes; a hand case would need degenerate bounds) and check the floor there. Then re-run mutate_graders.")
row("PRJ-R6-29", "hand-worked cases: certificate fields checked against the recomputation", "grader/test_project.py lines 388-410", "PASS",
    carry(10, "grader/ byte-identical since e8b10b8", "reference agrees with the recomputation on seeds 0-49 (run_graders PASS)"))
row("PRJ-R6-30", "objective against three feasible comparators (page line 329)", "grader/test_project.py lines 372-383; project.html line 329", "PASS",
    carry(10, "grader/ and line 329 byte-identical since e8b10b8", "no change"))
row("PRJ-R6-31", "mutant suite: every grader mutant killed (ledgers/M7/mutants, seeds 0-9)", "ledgers/M7/mutants/ (108 files); tools/mutate_graders.py --unit M7 --seeds 0-9", "FAIL",
    "mutate_graders M7: FAIL, 101 of 108 killed (" + S + "mutate_all108.log). Survivors: q04_dual_residual_without_zero_floor, r02_turnover_total_residual_dropped_from_primal, r04_budget_left_out_of_primal_residual, r05_turnover_total_slackness_term_zeroed, v10_01_dual_residual_ignores_sector_and_turnover_multipliers, v10_02_complementary_slackness_signed_not_absolute, v11_01_dual_residual_sign_flipped_in_certificate. Each is a certificate-term bug that the reference never triggers (its min multiplier is 0 and its budget and turnover gaps are <= 0 to rounding), so the suite cannot see it on any output it reaches from the reference; the page's definitions (project.html lines 313-315) state the behaviour each one violates.",
    "Make each survivor observable: add a test where the certificate's term is nonzero on a valid output (for example a case whose turnover constraint is slack with kappa > 0 is impossible at a KKT point, so use a hand-worked output with a reported multiplier of the wrong sign and check the reported residual against the page's formula), or change the page's definition of the term so that the suite's agreement test covers it. Then re-run mutate_graders.")
row("PRJ-R6-32", "five alternative correct implementations pass the suite (rule 11)", "ledgers/M7/scripts/M7-d-r11/alt_*_0-49.log", "PASS",
    "five correct alternatives pass on seeds 0-49, 50 of 50 each: alt_lu_solver (" + S + "alt_lu_0-49.log), alt_slack_order (" + S + "alt_slack_0-49.log), alt_empty_start, alt_nullspace, alt_reverse_order (" + S + "alt_alt_*_0-49.log). Note, not a grader finding: a float alternative (alt_float, round 7) fails 15 of 50 seeds with RuntimeError or refusal on spec-valid gamma = 1e-6 and 1e-9 (" + S + "alt_float_0-49.log, " + S + "alt_float_failures.log); its absolute pivot thresholds (1e-12) are its own defect, and the suite's gamma boundary tests are stated on the page (line 315: gamma of 10^-6 is valid).")
row("PRJ-R6-33", "cards: every card agrees with the CURRENT lesson text (rule 10, full read)", "course/modules/M/M7/cards.json (158) vs L01.html-L08.html", "UNVERIFIABLE",
    "Not completed this round. Read this round: the 10 changed cards and 1 added card (PRJ-R11-02 and rows below); all 147 unchanged cards were not re-read line by line against their lessons. The number-presence check (PRJ-R6-25) is mechanical only.",
    "A full card-by-lesson read of all 158 cards against L01-L08, with the lesson sentence cited for each card.")
row("PRJ-R6-34", "browser-only claims: storage and nothing you write leaves the browser", "project.html line 355 and footer line 474", "PASS",
    "static code read: store.js opens IndexedDB with a memory fallback ('Nothing here ever leaves the browser'); grader.js lines 61 and 79 write the draft to store 'files'; grader.js line 18 is a GET of the suite. Claim is conditional ('where the browser allows storage'); the storage behaviour itself was not exercised in a browser this round (page_smoke does not test persistence).")
row("PRJ-R6-35", "Lab 1 prose: code prints the four KKT quantities in steps 4 to 6", "course/modules/M/M7/project.html line 55", "PASS",
    carry(10, "line 55 byte-identical since e8b10b8", "no change"))
row("PRJ-R6-36", "Lab 3 prose claims about which residuals respond", "course/modules/M/M7/project.html line 438", "PASS",
    carry(10, "line 438 byte-identical since e8b10b8", "lab-M7-project-3 output re-run this round"))
row("PRJ-R6-37", "card ids unique; gaps in the id sequence", "course/modules/M/M7/cards.json", "PASS",
    "cards_numbers_r11.log: duplicate ids none; 158 cards; id M7-c176 added and unique")
row("PRJ-R6-38", "pyflakes/type checks of the grader", "grader/test_project.py, reference.py, instance.py, starter.py", "PASS",
    "mypy --no-incremental: Success, 255 source files (" + S + "mypy.log); ruff check on grader: All checks passed")
row("PRJ-R7-01", "delta since pin 44f1eb6 read in full (round-7 row)", "project.html; grader/test_project.py; cards.json; tests/labs", "PASS",
    "Carried from round 7 (historical row): this round's delta e8b10b8..f42f432 was read in full: cards.json (10 changed: c046, c047, c057, c099, c102, c112, c131, c148, c162, c175; 1 added: c176), project.html (lines 293, 355, 474), no grader, lab or tool change")
row("PRJ-R8-01", "delta since 7aa909e: project.html lede (line 39) wording", "course/modules/M/M7/project.html line 37", "PASS",
    carry(10, "line 37 byte-identical since e8b10b8", "no change"))
row("PRJ-R8-02", "delta since 7aa909e: spec context (line 290) 'checks the four KKT conditions'", "course/modules/M/M7/project.html line 290", "PASS",
    carry(10, "line 290 byte-identical since e8b10b8", "no change"))
row("PRJ-R8-03", "cards c009 and c165 (Q1, Q2 eigenvalues) against L01", "cards.json c009, c165; L01.html", "PASS",
    carry(10, "c009 and c165 unchanged since e8b10b8 (card-object comparison)", "no change"))
row("PRJ-R8-04", "card c042 (sufficiency theorem) against L03 Theorem 2.1 and Remark 2.2", "cards.json c042; L03.html", "PASS",
    carry(10, "c042 and L03.html unchanged since e8b10b8", "no change"))
row("PRJ-R8-05", "cards c080 and c166 (Remark 2.4) against L05", "cards.json c080, c166; L05.html", "PASS",
    carry(10, "c080, c166 and L05.html unchanged since e8b10b8", "no change"))
row("PRJ-R8-06", "card c084 (midpoint uniqueness) against L05 Proposition 3.4", "cards.json c084; L05.html", "PASS",
    carry(10, "c084 and L05.html unchanged since e8b10b8", "no change"))
row("PRJ-R8-07", "cards c100 and c167 (budget closed form, 1'z > 0) against L06 Theorem 1.3 and P2", "cards.json c100, c167; L06.html", "PASS",
    carry(10, "c100, c167 and L06.html unchanged since e8b10b8", "no change"))
row("PRJ-R8-08", "card c107 (QP with turnover) against L06 Proposition 3.4 and Remark 3.5", "cards.json c107; L06.html", "PASS",
    carry(10, "c107 and L06.html unchanged since e8b10b8", "no change"))
row("PRJ-R8-09", "L06 notation change a,b -> y,z: no stale meaning left", "course/modules/M/M7/L06.html", "PASS",
    carry(10, "L06.html unchanged since e8b10b8", "no change"))
row("PRJ-R8-10", "grader, twins, tools, references unchanged since the round-7 pin", "course/modules/M/M7/grader/; tests/labs/M7/; tools/; references/", "PASS",
    "git diff e8b10b8..f42f432 over these paths is empty (checked this round)")
row("PRJ-R8-11", "L06 lab twin change (tests/labs/M7/lab-M7-L06-1.py) still runs and matches its block", "tests/labs/M7/lab-M7-L06-1.py; L06.html", "PASS",
    "run_labs M7 PASS (11/11) this round; twin unchanged since e8b10b8")
row("PRJ-R8-12", "L06 numbers in cards c113 and c114 (unrounded values)", "cards.json c113, c114; L06.html Part D and Part B", "PASS",
    "re-derived this round: 0.5722548315 and 0.5588607333 (" + S + "exact_c113_c114.log); same as PRJ-R6-26")
row("PRJ-R8-13", "new student-error mutants r8_m01..r8_m06 (verifier's own, >= 3 required)", "ledgers/M7/mutants/r8_m01..r8_m06", "PASS",
    "all six run in mutate_graders M7 (" + S + "mutate_all108.log): all KILLED, none in the survivor list")
row("PRJ-R8-14", "three exact alternatives pass the suite, seeds 0-49", "ledgers/M7/scripts/M7-d-r8/alt/ (alt_empty_start, alt_nullspace, alt_reverse_order)", "PASS",
    "run_alts_r11.py: alt_empty_start 50 of 50, alt_nullspace 50 of 50, alt_reverse_order 50 of 50 (" + S + "alt_alt_*_0-49.log)")
row("PRJ-R8-15", "reference multiplier scan (supports PRJ-R6-28)", "ledgers/M7/scripts/M7-d-r8/minmult_r8.py", "PASS",
    "minmult_r11.py: 50 of 50 seeds have minimum inequality multiplier 0.0 (" + S + "minmult_r11.log)")
row("PRJ-R10-01", "lede stationarity wording (project.html line 37)", "course/modules/M/M7/project.html line 37", "PASS",
    carry(10, "line 37 byte-identical since e8b10b8", "no change"))
row("PRJ-R10-02", "Lab 1 hypothesis (project.html line 55): steps 4 to 6 print the KKT checks", "course/modules/M/M7/project.html line 55", "PASS",
    carry(10, "line 55 byte-identical since e8b10b8", "no change"))
row("PRJ-R10-03", "instance text (project.html line 293): n and K", "course/modules/M/M7/project.html line 293; grader/instance.py", "PASS",
    "line 293 changed this round to 'n ... three, four or five ... K ... two on every seed'; fresh check: n in {3,4,5} (696/650/654 over seeds 0-1999), K = 2 on all 2000 seeds (" + S + "n_k_range.log); the symbol K itself is handled by PRJ-R11-01")
row("PRJ-R10-04", "certificate definitions (project.html line 315): complementary slackness is the largest |lambda g|", "course/modules/M/M7/project.html line 315; grader/reference.py _certificate", "PASS",
    carry(10, "line 315 and grader/ byte-identical since e8b10b8", "no change"))
row("PRJ-R10-05", "Lab 3 interpretation (project.html line 439) numbers", "course/modules/M/M7/project.html line 439", "PASS",
    carry(10, "line 439 byte-identical since e8b10b8", "lab-M7-project-3 output re-run this round"))
row("PRJ-R10-06", "new student-error grader mutants (>= 3 required) and their kills", "ledgers/M7/mutants/v10_01..v10_03, v11_01..v11_03", "FAIL",
    "three further mutants written this round (v11_01..v11_03, " + S + "build_fragment_r11.py lists them). v11_02 and v11_03 KILLED (test_certificate_agrees_with_the_recomputed_residuals). v11_01 SURVIVED. Re-run: v10_01 and v10_02 still SURVIVE (" + S + "mutate_all108.log); v10_03 KILLED.",
    "Make v10_01, v10_02 and v11_01 observable (see PRJ-R6-31).")
row("PRJ-R10-07", "exact alternative implementations pass on seeds 0-49 (rule 11)", "ledgers/M7/scripts/M7-d-r8/alt/; ledgers/M7/scripts/M7-d-r11/alt/", "PASS",
    "re-run this round: alt_lu_solver 50/50, alt_slack_order 50/50, alt_empty_start 50/50, alt_nullspace 50/50, alt_reverse_order 50/50 (" + S + "alt_*_0-49.log)")
row("PRJ-R10-08", "cards c168 to c174 (added): numbers and claims against lab output", "cards.json c168-c174", "PASS",
    carry(10, "c168-c174 unchanged since e8b10b8 (card-object comparison)", "no change"))
row("PRJ-R10-09", "card c175 (added): 'the lab prints recursion_matches_brute_force True at all 18 pairs'", "cards.json M7-c175; tests/labs/M7/lab-M7-L08-1.py lines 107-121", "PASS",
    "c175 reworded to 'prints one aggregate line ... which is the conjunction ... over the 18 (t, s) pairs'. lab-M7-L08-1.py lines 107-121: HORIZON = 6 (t = 0..5), STATES = (0, 1, 2), all_match = all_match and ..., one print of recursion_matches_brute_force {all_match}. Matches.")
row("PRJ-R10-10", "changed cards c003, c028, c049, c052, c063, c087, c089, c100, c102, c109, c112, c153, c163", "cards.json (those ids)", "PASS",
    "c003, c028, c049, c052, c063, c087, c089, c100, c109, c153, c163 unchanged since e8b10b8 (card-object comparison): carried. c102 (Proposition 2.1 hypothesis 'any set of weights over which the minimum exists') and c112 (zero set {A4} at every gamma, " + S + "lab output) re-verified this round against L06.html lines 36-44 and the L06 twin: PASS")
row("PRJ-R10-11", "changed cards c113 and c114: the exact-fraction values", "cards.json c113, c114; tests/labs/M7/lab-M7-L06-1.py", "PASS",
    "same as PRJ-R6-26: 0.5722548315 and 0.5588607333 recomputed (" + S + "exact_c113_c114.log)")
row("PRJ-R11-01", "notation: symbol K on project.html line 293 vs the same unit's use of K", "course/modules/M/M7/project.html line 293; course/modules/M/M7/L05.html (K as the KKT matrix, 10 occurrences)", "FAIL",
    "project.html line 293 defines K as the number of sectors (new wording this round, same meaning as before). L05.html uses \\(K\\) for the nonsingular (n+m)x(n+m) KKT matrix. K is not an entry of notation/notation.json, so the registry check has nothing to compare, but the unit reuses one letter for two meanings, which rule 13 forbids in spirit.",
    "Rename the project's sector count to a letter the unit does not use elsewhere (for example J or Q_count, checked against L01-L08 and the registry) on project.html lines 293 and in the grader's documented field names only if the page wording changes; re-run check_pages and the notation check.")
row("PRJ-R11-02", "new cards c175 reword and c176 (added) against lessons", "cards.json c131, c175, c176; L02.html Theorem 2.2 and Remark 2.3; L07.html; L08.html", "PASS",
    "c176: L02.html lines 29-39 Theorem 2.2 proof constructs gamma(t) with gamma(0) = x*, gamma'(0) = d, h(gamma(t)) = 0 and minimality rules out first-order decrease; Remark 2.3 (line 39) states this for each prescribed tangent d in the tangent space. c131 (L07 lab, range(HORIZON) with HORIZON = 4 and 5 wealth states = 20 pairs) and c175 (L08, 18 pairs) conjunction wording matches lab code. c046, c047 match L03 lines 268-269; c057 matches L04 line 25; c099 matches L06 line 62; c148 matches L08 Lemma 2.2 (line 60); c162 matches L08 lines 68 and 211 ('infinite horizon').")

fragment = {
    "unit": "M7",
    "slice": "d",
    "round": 11,
    "verifier": "Haiku 5.5 independent verifier (round 11)",
    "pin": "f42f4329dcb0b5c2257e40cd6c27e734fa700d46",
    "base": "e8b10b8110923bd88c3b4bd0e36e1571be3e6725 (round-10 pin)",
    "checkout": str(ROOT),
    "scratch": "/tmp/m7d_r11_* (alt runs, collect copies, starter, page copy, exact values)",
    "verified_at": datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat(),
}
counts = {}
for r in rows:
    counts[r["status"]] = counts.get(r["status"], 0) + 1
fragment["verdict"] = "PASS" if counts.get("PASS", 0) == len(rows) else "FAIL"
fragment["rows"] = rows

mut_lines = (ROOT / S / "mutate_all108.log").read_text(encoding="utf-8").splitlines()
mutants = []
for line in mut_lines:
    m = re.match(r"^(KILLED|SURVIVED) ([^:]+): (.*)$", line)
    if not m:
        continue
    status, fname, rest = m.groups()
    desc = rest.split(" -> ")[0]
    killed_by = None
    if status == "KILLED":
        killed_by = rest.split(" -> ", 1)[1].strip()
    mutants.append({"name": fname.replace(".py", ""), "description": desc, "killed_by": killed_by})
fragment["mutants"] = mutants
fragment["registry_flags"] = []
fragment["freshness_flags"] = [
    "project.html changed at lines 293, 355, 474; cards.json: 10 changed (c046, c047, c057, c099, c102, c112, c131, c148, c162, c175), 1 added (c176); grader/, tests/labs/M7, tools/, references/, notation/ unchanged since e8b10b8"
]
fragment["notes"] = (
    "Round 11 re-ran every gate command and every alternative and mutant this round. Surviving grader mutants (7) and "
    "the 0.0 minimum multiplier on 50 of 50 seeds point to one root cause: the certificate's floor and certificate-term "
    "checks are never triggered by a correct solution. Not checked: a full card-by-lesson read of the 147 unchanged cards "
    "(PRJ-R6-33); the browser storage behaviour (PRJ-R6-34 static only); sweep part of page_smoke."
)
fragment["summary"] = (
    f"{len(rows)} rows: {counts.get('PASS',0)} PASS, {counts.get('FAIL',0)} FAIL, {counts.get('UNVERIFIABLE',0)} UNVERIFIABLE. "
    f"Mutants {len(mutants)}, killed {sum(1 for m in mutants if m['killed_by'])}. Verdict FAIL."
)
out = ROOT / "ledgers/M7/M7-d.json"
out.write_text(json.dumps(fragment, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("wrote", out, counts, "mutants", len(mutants), "killed", sum(1 for m in mutants if m["killed_by"]))
