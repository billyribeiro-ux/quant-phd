"""Round 13 (M7-d): writes ledgers/M7/M7-d.json from the round-13 logs and the row decisions made in this round."""
import json, pathlib, re, datetime

ROOT = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyB13-M7-d")
S = "ledgers/M7/scripts/M7-d-r13/"
CAR = "Carried from round 12 ({files} byte-identical since the previous pin ff38842): "

rows = []
def R(id_, check, location, status, evidence, fix=None):
    r = {"id": id_, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    rows.append(r)

GR = "grader/test_project.py, reference.py, instance.py, starter.py"
# ---- commands and gates re-run this round (PASS) ----
R("PRJ-R6-01", "2.6-gate", "tools/check_projects.py", "PASS", f"check_projects M7: PASS ({S}check_projects.log)")
R("PRJ-R6-02", "2.6-gate", "tools/check_pages.py", "PASS", f"check_pages M7: PASS, hours, ladder, data-hours ({S}check_pages.log)")
R("PRJ-R6-03", "2.9-dag", "course/modules/M/M7/project.html; tools/check_dag.py", "PASS", f"check_dag M7: PASS ({S}check_dag.log); concept links unchanged in the delta")
R("PRJ-R6-04", "2.6-autograder", "course/modules/M/M7/grader/reference.py", "PASS", f"run_graders.py --unit M7 --seeds 0-49: reference 50/50 seeds, slowest 3.3 s ({S}run_graders_0-49.log)")
R("PRJ-R6-05", "2.6-autograder", GR, "PASS", f"run_graders.py M7 PASS includes the starter-fails-suite check ({S}run_graders_0-49.log)")
R("PRJ-R6-06", "2.6-autograder", "grader/test_project.py; project.html (363 checks)", "PASS", f"collect-only: 363 tests for seed 0 and seed 49 ({S}collect_r13.log); page states 363")
R("PRJ-R6-07", "2.5-labs", "tests/labs/M7/", "PASS", f"run_labs.py --unit M7: PASS (11/11) ({S}run_labs_M7.log)")
R("PRJ-R6-08", "2.6-labs", "tests/labs/M7/lab-M7-project-1..3.py", "PASS", f"python -I -W error on each twin exit 0; stdout matches the page expected blocks under run_labs ({S}lab_project-1.out, lab_project-2.out, lab_project-3.out, run_labs_project_page.log)")
R("PRJ-R6-09", "2.5-labs", "course/modules/M/M7/project.html lines 56-154, 172-270, 372-434", "PASS", f"run_labs page-code-equals-twin check on project.html PASS ({S}run_labs_project_page.log); lab 3 twin docstring change is inside the same check")
R("PRJ-R6-10", "2.2-numbers", "course/modules/M/M7/project.html lines 155-166 (Lab 1)", "PASS", f"step outputs recomputed: budget-only 54/65, 5/26, -3/130; answer 9/11, 2/11, 0; nu -21/1100; held-asset multiplier 9/1100; objective -3/220 (~-0.013636) ({S}lab_project-1.out)")
R("PRJ-R6-11", "2.2-numbers", "course/modules/M/M7/project.html lines 435-438 (Lab 3 claims)", "PASS", f"Lab 3 output: check B stationarity 9/550 = 2 x 9/1100, dual 9/1100; check C stationarity 1/6250, primal 0; primal and CS 0 for all candidates ({S}lab_project-3.out)")
R("PRJ-R6-12", "2.4-definitions", "course/modules/M/M7/project.html lines 306-316; grader/test_project.py recomputed_certificate lines 105-116", "PASS", "page definitions (dual = max(0, -smallest inequality multiplier); CS = max |lambda_j g_j|) match recomputed_certificate; floor paragraph added at page line 318 and checked in R13-09")
R("PRJ-R6-13", "2.4-math", "course/modules/M/M7/project.html lines 320-322 (sufficiency proposition)", "PASS", "re-derived in this round for a budget multiplier of either sign: L is convex, stationary at (w,t), so minimal; feasibility gives f(y) >= L(y,s) >= L(w,t) = f(w); strict-convexity uniqueness by the midpoint argument. See PRJ-R13-10")
R("PRJ-R6-14", "2.4-math", "course/modules/M/M7/project.html line 307 (linearization)", "PASS", CAR.format(files="project.html line 307") + "linearization sentence unchanged; grader turnover rows agree with it")
R("PRJ-R6-15", "2.6-autograder", "grader/test_project.py lines 218-246", "PASS", CAR.format(files="grader/test_project.py") + "five hand-worked answers unchanged")
R("PRJ-R6-16", "2.6-autograder", "grader/test_project.py lines 553-567, 590-596, 670-693", "PASS", CAR.format(files="grader/test_project.py") + "named ValueError tests unchanged; page boundary sentence (line 330) unchanged")
R("PRJ-R6-17", "2.6-autograder", "grader/instance.py lines 3-6, 34-68", "PASS", CAR.format(files="grader/instance.py") + "SIMULATED, feasible-by-construction generator")
R("PRJ-R6-18", "2.6-autograder", "grader/test_project.py lines 268-282", "PASS", CAR.format(files="grader/test_project.py") + "standard library only rule unchanged")
R("PRJ-R6-19", "2.6-gate", "tests/labs/M7/; grader/", "PASS", f"ruff check and ruff format --check on tests/labs/M7 and grader: All checks passed; 15 files formatted ({S}ruff.log); mypy --strict on reference.py, instance.py, starter.py: Success ({S}run_graders_0-49.log typecheck)")
R("PRJ-R6-20", "2.9-refs", "course/modules/M/M7/project.html lines 465-466 (data-cite boyd2004convex, stokey1989recursive)", "PASS", "both keys present in references/references.json (grep \"key\"); verify_refs.py --offline: 560 entries, 0 problems")
R("PRJ-R6-21", "2.5-smoke", "course/modules/M/M7/project.html", "PASS", f"page_smoke.py --unit M7 --pages project.html: PASS, exit 0 ({S}page_smoke_project.log)")
R("PRJ-R6-22", "2.9-hours", "course/modules/M/M7/project.html lines 337-351", "PASS", CAR.format(files="project.html lines 337-351") + "hours split; check_pages hours arithmetic PASS this round")
R("PRJ-R6-23", "2.9-prose", "project.html (changed lines 164-166, 317-322, 330-331, 368-382); cards.json (changed and added cards)", "PASS", "banned-phrase and process-word scan of the delta: no TODO, TBD, lorem, 'for brevity', 'it is important to note', 'obviously', 'clearly'; ellipses in cards c122, c132, c143, c153 are sequence notation, not omitted content")
R("PRJ-R6-24", "2.4-notation", "course/modules/M/M7/project.html lines 303-308, 317-322", "PASS", "notation/notation.json registers T, \\gamma_3, \\gamma_4 and others; M7 page uses plain \\gamma, \\nu, \\lambda, \\tau, \\Sigma (none registered; the registry's 'about' says gamma is lesson-local); no registered symbol reused")
R("PRJ-R6-25", "2.7-cards", "course/modules/M/M7/cards.json (168 cards)", "PASS", f"cards_numbers_r13.py: 15 absent tokens were all TeX fractions; cards_fracs_r13.py after \\frac/\\tfrac normalisation: 0 absent ({S}cards_numbers_r13.log, cards_fracs_r13.log); ids and fronts unique")
R("PRJ-R6-26", "2.7-cards", "cards.json c112, c113, c114, c131, c175", "PASS", CAR.format(files="those cards") + "numbers matched in the previous round; cards_numbers_r13 finds no absent number on them")
R("PRJ-R6-27", "2.4-notation", "project.html lines 306, 313", "PASS", CAR.format(files="project.html lines 306, 313") + "glyph 1 is the all-ones vector as before")
R("PRJ-R6-28", "2.6-autograder-mutation", "grader/test_project.py lines 105-116, 365-369; grader/reference.py line 287; project.html lines 315, 318", "FAIL",
  "The floor at zero in the dual residual is stated on page line 315 and is now disclosed as inert on seeds 0-49 (new paragraph line 318). Re-verified: " + S + "minmult_r13.log shows all 50 reference seeds have min inequality multiplier 0, so no seed distinguishes the floor. Mutant q04 (no floor) survives run_graders-style mutate on seeds 0-9 (" + S + "mutate_all_r13_114.log). The disclosure does not kill it.",
  "Add a hand-worked case (or a test) whose correct certificate has every inequality multiplier strictly positive, then assert dual_residual = 0 there. Note: a box pair with lower_i < upper_i always has one multiplier zero by complementary slackness, so such a case needs lower_i = upper_i for every asset. Alternatively state on page line 315 that the floor is not tested and remove the claim that the suite checks the certificate definitions.")
R("PRJ-R6-29", "2.6-autograder", "grader/test_project.py lines 388-410", "PASS", CAR.format(files="grader/test_project.py") + "hand-worked certificate checks unchanged")
R("PRJ-R6-30", "2.6-autograder", "grader/test_project.py lines 372-383; project.html line 329", "PASS", CAR.format(files="grader/test_project.py; project.html line 329") + "three comparators unchanged")
R("PRJ-R6-31", "2.6-mutation", "ledgers/M7/mutants/ (114 files); tools/mutate_graders.py --unit M7 --seeds 0-9", "FAIL",
  f"mutate_graders M7: FAIL (106/114 killed) ({S}mutate_all_r13_114.log). Survivors: q04, v11_01 (distinguishable only on instances with every inequality multiplier positive; need a test); r02, r04, r05, v10_01, v10_02, s12_03 (equivalent on every instance the reference solves: primal gaps and budget are exact, turnover-total and CS products are exactly zero, all multipliers are non-negative by the active-set exit test in reference.py lines 213-215, so each is not a fault).",
  "Kill q04 and v11_01 with a test on a case whose inequality multipliers are all positive (see PRJ-R6-28). Remove r02, r04, r05, v10_01, v10_02 and s12_03 from ledgers/M7/mutants/ and record each equivalence argument as a row, as VERIFIER_RULES 2.6(3) requires.")
R("PRJ-R6-32", "2.6-alt-implementations", "grader suite; ledgers/M7/scripts/M7-d-r11/alt/alt_lu_solver.py, alt_slack_order.py", "PASS", f"re-run this round against the current grader, seeds 0-49: alt_lu_solver 50/50, alt_slack_order 50/50 ({S}alt_run_r13.log)")
R("PRJ-R6-33", "2.7-cards-full-scan", "course/modules/M/M7/cards.json (168) vs L01.html-L08.html", "UNVERIFIABLE",
  "Full line-by-line read of all 168 cards against the lessons was not completed in this round. This round checked the changed and added cards (PRJ-R13-03..08), the numbers on every back (PRJ-R6-25), and duplicates. The remaining cards were not re-read against their lesson text.",
  "Re-read every card against its lesson (rule 10) and record one row per 10 cards.")
R("PRJ-R6-34", "2.6-browser-claims", "course/modules/M/M7/project.html lines 355, 474", "PASS", CAR.format(files="project.html lines 355 and 474") + "storage and no-upload claims unchanged")
R("PRJ-R6-35", "2.5-labs", "course/modules/M/M7/project.html line 55 (Lab 1 hypothesis)", "PASS", CAR.format(files="project.html line 55") + "hypothesis unchanged; the interpretation (line 164-166) was re-checked in PRJ-R6-10")
R("PRJ-R6-36", "2.5-labs", "course/modules/M/M7/project.html line 438 (Lab 3 claims)", "PASS", "re-checked in PRJ-R6-11 against lab_project-3.out: the claims about responding residuals hold for candidates B and C and the primal and CS residuals stay zero")
R("PRJ-R6-37", "2.7-cards", "course/modules/M/M7/cards.json", "PASS", "ids unique (168 cards, no duplicates); id numbering has gaps (M7-c034, c035, ...), which is cosmetic and not a rule violation")
R("PRJ-R6-38", "2.6-typecheck", "grader/reference.py, instance.py, starter.py, test_project.py", "PASS", f"mypy --strict on reference, instance, starter: Success ({S}run_graders_0-49.log); test_project.py with a copy of reference.py as constrained_allocator stub: Success, no issues in 1 source file")
R("PRJ-R7-01", "historical", "project.html; grader/test_project.py; cards.json; tests/labs", "PASS", "historical row (delta since the round-7 pin); not re-asserted for the current pin")
R("PRJ-R8-01", "2.9-prose", "course/modules/M/M7/project.html line 37", "PASS", CAR.format(files="project.html line 37") + "lede unchanged")
R("PRJ-R8-02", "2.9-prose", "course/modules/M/M7/project.html line 290", "PASS", CAR.format(files="project.html line 290") + "spec context unchanged")
R("PRJ-R8-03", "2.7-cards", "cards.json c009, c165; L01.html", "PASS", "re-verified in PRJ-R13-03 (c009 and c165 changed in this delta): eigenvalues 3 and 1 of Q1, 3 and -1 of Q2; Example 3.3 in L01 gives the same eigenvectors")
R("PRJ-R8-04", "2.7-cards", "cards.json c042; L03.html", "PASS", CAR.format(files="cards.json c042 and L03.html") + "unchanged")
R("PRJ-R8-05", "2.7-cards", "cards.json c080, c166; L05.html", "PASS", "carried: c080 unchanged; numbers 11/4, 18/11, 4/11 found after TeX normalisation (cards_fracs_r13.log: 0 absent)")
R("PRJ-R8-06", "2.7-cards", "cards.json c084; L05.html", "PASS", CAR.format(files="cards.json c084 and L05.html") + "unchanged; c084 number 1/8 found after TeX normalisation")
R("PRJ-R8-07", "2.7-cards", "cards.json c100, M7-c167; L06.html", "PASS", CAR.format(files="cards.json c100 and c167 and L06.html") + "unchanged")
R("PRJ-R8-08", "2.7-cards", "cards.json c107; L06.html", "PASS", CAR.format(files="cards.json c107 and L06.html") + "unchanged")
R("PRJ-R8-09", "2.4-notation", "course/modules/M/M7/L06.html", "PASS", CAR.format(files="L06.html") + "notation change unchanged")
R("PRJ-R8-10", "historical", "grader; labs; tools; references", "PASS", "historical row: its claim concerns the round-7 pin; the grader was later renamed (PRJ-R12-02). Not re-asserted for the current pin.")
R("PRJ-R8-11", "2.5-labs", "tests/labs/M7/lab-M7-L06-1.py; L06.html", "PASS", "run_labs M7 11/11 (includes L06 twin) ({S}run_labs_M7.log)".replace("{S}", S))
R("PRJ-R8-12", "2.7-cards", "cards.json c113, c114; L06.html Part D and Part B", "PASS", CAR.format(files="cards.json c113 and c114") + "exact values match lab_L06-1.out (c113, c114 numbers not changed)")
R("PRJ-R8-13", "2.6-mutation", "ledgers/M7/mutants/r8_m01..r8_m06", "PASS", f"killed in {S}mutate_all_r13_114.log (none of the r8 files is in the survivor list)")
R("PRJ-R8-14", "2.6-alt-implementations", "ledgers/M7/scripts/M7-d-r8/alt/", "PASS", CAR.format(files="grader/ and the r8 alternatives") + "the three r8 alternatives were not re-run this round; current alternatives are re-run in PRJ-R6-32")
R("PRJ-R8-15", "2.6-autograder", "ledgers/M7/scripts/M7-d-r12/minmult_r12.log", "PASS", f"superseded by {S}minmult_r13.log: 50 of 50 seeds have min inequality multiplier 0, recomputed on the current checkout")
R("PRJ-R10-01", "2.9-prose", "course/modules/M/M7/project.html line 37", "PASS", CAR.format(files="project.html line 37") + "lede unchanged")
R("PRJ-R10-02", "2.5-labs", "course/modules/M/M7/project.html line 55", "PASS", CAR.format(files="project.html line 55") + "Lab 1 hypothesis unchanged")
R("PRJ-R10-03", "2.6-spec", "course/modules/M/M7/project.html line 293; grader/instance.py", "PASS", CAR.format(files="project.html line 293") + "instance text unchanged")
R("PRJ-R10-04", "2.4-definitions", "course/modules/M/M7/project.html line 315; grader/reference.py _certificate", "PASS", CAR.format(files="project.html line 315") + "definition bullet unchanged; the new floor paragraph is checked in PRJ-R13-09; the mutant gap is PRJ-R6-28")
R("PRJ-R10-05", "2.2-numbers", "course/modules/M/M7/project.html line 439", "PASS", "re-checked in PRJ-R6-11: Lab 3 interpretation numbers 9/550, 9/1100, 1/6250 match lab_project-3.out")
R("PRJ-R10-06", "2.6-mutation", "ledgers/M7/mutants/v10_01, v10_02, v11_01 (and v10_03, v11_02, v11_03)", "FAIL",
  f"In {S}mutate_all_r13_114.log v10_01 and v10_02 and v11_01 SURVIVE; v10_03, v11_02, v11_03 are killed. v11_01 is distinguishable only on instances with every inequality multiplier positive (see PRJ-R6-28). v10_01 and v10_02 are equivalent on every instance the reference solves (all multipliers non-negative; all CS products zero).",
  "Kill v11_01 with the test described in PRJ-R6-28; remove v10_01 and v10_02 from ledgers/M7/mutants/ with their equivalence arguments.")
R("PRJ-R10-07", "2.6-alt-implementations", "ledgers/M7/scripts/M7-d-r11/alt/ alt_lu_solver.py, alt_slack_order.py", "PASS", f"re-run this round: 50/50 seeds each ({S}alt_run_r13.log)")
R("PRJ-R10-08", "2.7-cards", "cards.json c168-c174", "PASS", CAR.format(files="cards.json c168-c174") + "unchanged; numbers pass cards_numbers_r13 check")
R("PRJ-R10-09", "2.5-labs", "cards.json M7-c175; tests/labs/M7/lab-M7-L08-1.py lines 107-121", "PASS", f"run_labs M7 11/11 includes L08 twin ({S}run_labs_M7.log); c175 unchanged")
R("PRJ-R10-10", "2.7-cards", "cards.json changed cards c003, c028, c049, c052, c063, c087, c089, c100, c102, c109, c112, ...", "PASS", "changed cards in this delta (c009, c028, c087, c110, c165) re-verified in PRJ-R13-03..06; the others are byte-identical since the previous pin (cards.json hunks only at lines 58, 194, 564, 711, 1061, 1164)")
R("PRJ-R10-11", "2.7-cards", "cards.json c113, c114; tests/labs/M7/lab-M7-L06-1.py", "PASS", f"lab_L06-1.out and cards c113, c114 exact values unchanged ({S}lab_L06-1.out)")
R("PRJ-R11-01", "2.4-notation", "course/modules/M/M7/project.html line 293 (symbol Z and K)", "PASS", CAR.format(files="project.html line 293") + "the K-to-Z rename is in the grader and the page text checked in PRJ-R6-24")
R("PRJ-R11-02", "2.7-cards", "cards.json c131, c175, c176; L02.html Theorem 2.2 and Remark 2.3; L07.html; L08.html", "PASS", CAR.format(files="those cards") + "unchanged")
R("PRJ-R12-01", "2.6-delta", "course/modules/M/M7/project.html, grader/test_project.py, cards.json, tests/labs/M7/lab-M7-project-1..3.py", "PASS", f"delta since the round-12 pin ff38842 is project.html, cards.json and lab-M7-project-3.py only (git diff --stat); all hunks read in this round (PRJ-R13-02..13)")
R("PRJ-R12-02", "2.6-autograder", "grader/test_project.py hunks at 42, 316, 521, 658, 670, 931", "PASS", CAR.format(files="grader/test_project.py") + "the rename is not in the delta since ff38842")
R("PRJ-R12-03", "2.6-mutation", "ledgers/M7/mutants/s12_01..s12_03", "FAIL",
  f"s12_01 and s12_02 killed ({S}mutate_all_r13_114.log). s12_03 (max(0, kappa)) survives and is equivalent: the reference returns kappa >= 0 exactly (reference.py lines 213-215 return only when all working multipliers are non-negative; minmult_r13.log min over all inequality multipliers is 0 on all 50 seeds), so max(0, kappa) = kappa on every instance it solves. It should be removed from the mutant set with this argument.",
  "Remove ledgers/M7/mutants/s12_03_turnover_total_multiplier_clipped_at_zero.py and record the equivalence argument as a row.")

R("PRJ-R12-04", "2.6-scope", "ledgers/M7/M7-d.json (round-12 checkout pin and scope)", "PASS", "round-13 checkout pinned at fca6bb1 (git rev-parse HEAD); the round-12 pin ff388424 is an ancestor; the delta is the three slice files (git diff --stat)")

# ---- new round-13 rows ----
R("PRJ-R13-01", "2.6-mutation", "ledgers/M7/mutants/r13_01, r13_02, r13_03", "PASS", f"three new student-error mutants written from grader/reference.py: r13_01 rounds weights to 6 places (killed by test_start_on_or_inside_a_bound_is_accepted_at_every_position[on-limit-lower-last-asset] seed 2); r13_02 includes the budget multiplier in dual feasibility (killed by test_certificate_agrees_with_the_recomputed_residuals seed 0); r13_03 drops the sector multiplier from stationarity (killed by test_certificate_agrees_with_the_recomputed_residuals seed 2) ({S}mutate_all_r13_114.log)")
R("PRJ-R13-02", "2.6-delta", "project.html (hunks at 164-166, 317-322, 330-331, 333-334, 368-382, 438); cards.json; lab-M7-project-3.py", "PASS", f"git diff ff388424..fca6bb1 read in full; every hunk checked in PRJ-R13-03..13 ({S})")
R("PRJ-R13-03", "2.7-cards", "cards.json c009, c165 (changed) vs L01.html Example 3.3", "PASS", "c009: eigenvalues of [[2,1],[1,2]] are 3 and 1; eigenvectors (1,1), (1,-1) (L01 Example 3.3). c165: [[1,2],[2,1]] has eigenvalues 3 and -1, with the same eigenvectors (L01 Example 3.3). Both cards state only eigenvalues now, and the numbers appear in L01.")
R("PRJ-R13-04", "2.7-cards", "cards.json c028/c181, c087/c182, c110/c183 (split) vs lab outputs", "PASS", f"L02 Lab 1 output: lambda 177/55 and w = (47/55, 17/55, -9/55) ({S}lab_L02-1.out line 6-8); L05 Lab 1 Part A: x = 13/19 3/19 3/19, lambda -36/19 11/19 ({S}lab_L05-1.out); L06 Part A gamma 1: return 0.113798, risk 0.123809, objective -0.051893, weights 0.434783 0.526836 0.562535 -0.524154 ({S}lab_L06-1.out)")
R("PRJ-R13-05", "2.7-cards", "cards.json c179, c180 (added) vs L01.html Proposition 3.2 and Problem P3", "PASS", "c179: L01 Proposition 3.2 states (iii) is equivalent to convexity under Assumption 1; eigenvalues 3 and 1 are non-negative, so it is convex. c180: Q2 eigenvalues 3 and -1 (L01 Hessian eigenvalues 6 and -2 are 2 times these); a negative eigenvalue refutes convexity without the assumption (L01: Problem P3 shows it).")
R("PRJ-R13-06", "2.7-cards", "cards.json c184 (|x| convex), c185 (positive definite) vs L01 Example 2.2, L02 Section 3", "PASS", "L01 Example 2.2 gives the triangle-inequality proof for |x| and says it is not differentiable at 0; L02 Section 3 defines positive definite as x'Sigma x > 0 for every x != 0 and says it excludes a zero value at a non-zero x. Both match the card text.")
R("PRJ-R13-07", "2.3-math", "cards.json c186 (T) vs L08.html Section 3 (negative discount)", "PASS", "recomputed by hand from L08 Definitions 1.1-1.2 with beta = -1, H = 2, r(x)=0, r(y)=1, B=0: plan totals 0, -1, 1, 0 so V_0 = 1; U_1 = max{0, 1} = 1; U_0 = max{0 + (-1)1, 1 + (-1)1} = 0 != 1. The card and L08 text agree.")
R("PRJ-R13-08", "2.2-numbers", "course/modules/M/M7/project.html line 164-166 (Lab 1 interpretation, step 5 change)", "PASS", f"lab_project-1.out: 'step 5 smallest weight: 0 largest weight: 9/11' and 'step 4 stationarity residuals 0,0,0'; the interpretation text matches ({S}lab_project-1.out)")
R("PRJ-R13-09", "2.4-math", "course/modules/M/M7/project.html line 318 (dual floor paragraph)", "PASS", f"claim 'inert on the seeds checked' verified: {S}minmult_r13.log, 50 of 50 seeds have min inequality multiplier 0 and none > 0. Logic: the floor changes max(0, -m) only when m > 0. The paragraph is accurate; the suite-coverage gap it describes is PRJ-R6-28.")
R("PRJ-R13-10", "2.4-math", "course/modules/M/M7/project.html lines 320-322 (proposition with budget multiplier nu of either sign)", "PASS", "re-derived: L(w,t) = f(w) + sum lambda_j g_j + nu(sum w_i - 1), convex in (w,t) because lambda_j >= 0 and g_j affine; gradient zero at (w,t) gives a global minimum; for feasible (y,s), f(y) >= L(y,s) >= L(w,t) = f(w) by complementary slackness and the budget term vanishing; uniqueness by midpoint feasibility and strict convexity. Hypotheses on the page include the budget multiplier and differentiability. Existence of multipliers on seeds 0-49 is stated only for those seeds.")
R("PRJ-R13-11", "2.2-numbers", "course/modules/M/M7/project.html lines 438-440 (Lab 3 interpretation) and the Lab 3 hypothesis", "PASS", f"lab_project-3.out: check B stationarity 9/550 = 2 * 9/1100, dual 9/1100; check C stationarity 1/6250, primal 0; all primal and CS residuals 0. The claims 'the dual residual responds to B', 'stationarity responds to B and C' and 'no candidate makes primal or CS non-zero' match.")
R("PRJ-R13-12", "2.5-labs", "tests/labs/M7/lab-M7-project-3.py docstring (changed) and page code", "PASS", f"run_labs M7 11/11 (page code equal to twin, expected block equal to output) ({S}run_labs_M7.log); twin under python -I -W error exit 0 ({S}lab_project-3.out). Docstring claim 'plus the check w_i <= 1 that the budget and those bounds imply' is true: sum w = 1 and w_i >= 0 give w_i <= 1.")
R("PRJ-R13-13", "2.7-cards", "cards.json full scan (168 cards): duplicates, numbers, grades, basis", "PASS", f"ids unique, fronts unique, grades T 119 / C 49, every C card has a basis; numbers on the backs appear in their own lessons after TeX fraction normalisation ({S}cards_fracs_r13.log: 0 absent)")
R("PRJ-R13-14", "2.9-prose", "project.html and changed cards: banned phrases and process words", "PASS", "scan for TODO, TBD, lorem, for brevity, beyond the scope, it is important to note, obviously, clearly, it is well known, studies show: no hits; 'this page does not show' in the floor paragraph is a scope statement, not a process word")
R("PRJ-R13-15", "2.4-notation", "project.html lines 303-322 (nu, lambda, tau, Sigma, gamma)", "PASS", "notation/notation.json: T, \\gamma_3, \\gamma_4 are the registered program-wide symbols; plain gamma, nu, lambda, tau, Sigma are lesson-local per the registry's 'about' text; no registered symbol is reused")
R("PRJ-R13-16", "2.6-gate", "grader/ and tests/labs/M7 lint and types", "PASS", f"ruff check and format: pass ({S}ruff.log); mypy --strict on test_project.py with a reference copy as constrained_allocator: Success ({S}run_graders_0-49.log; stub run recorded here)")
R("PRJ-R13-17", "2.9-refs", "references/references.json (560 entries)", "PASS", "verify_refs.py --offline: offline integrity: 560 entries, 0 problems (run this round)")
R("PRJ-R13-18", "2.6-autograder", "grader/reference.py seeds 0-49", "PASS", f"run_graders.py --unit M7 --seeds 0-49: PASS, 50/50 ({S}run_graders_0-49.log)")
R("PRJ-R13-19", "2.6-autograder", "grader/test_project.py collect count", "PASS", f"363 tests collected at seeds 0 and 49 ({S}collect_r13.log)")
R("PRJ-R13-20", "2.6-alt-implementations", "alternative correct implementations (rule 11)", "PASS", f"alt_lu_solver.py 50/50 and alt_slack_order.py 50/50 seeds pass ({S}alt_run_r13.log). Not new algorithms: both reuse the exact active-set family; a float-based alternative was not built this round.")
R("PRJ-R13-21", "2.5-smoke", "project.html in Chromium", "PASS", f"page_smoke.py --unit M7 --pages project.html: PASS ({S}page_smoke_project.log); the sweep was run as part of the default run")
R("PRJ-R13-22", "2.6-gate", "tools/check_projects.py, check_pages.py, check_dag.py for M7", "PASS", f"all three PASS ({S}check_projects.log, check_pages.log, check_dag.log)")

# ---- mutants from the round-13 run ----
mutants = []
log = (ROOT / S / "mutate_all_r13_114.log").read_text(encoding="utf-8").splitlines()
for line in log:
    m = re.match(r"^(KILLED|SURVIVED) (\S+): (.*?) -> (.*)$", line)
    if not m:
        continue
    status, name, desc, killed = m.groups()
    mutants.append({"id": name, "description": desc,
                    "killed_by": None if killed.strip() == "None" else killed.strip()})

statuses = [r["status"] for r in rows]
fragment = {
    "unit": "M7", "slice": "d", "round": 13,
    "verifier": "Haiku 5.5 independent verifier (round 13)",
    "pin": "fca6bb104984c6a724fc214d8073158e610e995a",
    "base": "ff388424d9d056b7a57868dab5ae7f7cdeef60f6 (round-12 pin)",
    "checkout": str(ROOT), "scratch": "/tmp/m7d_r13_* (logs copied into " + S + ")",
    "verified_at": datetime.datetime.now(datetime.UTC).replace(microsecond=0).isoformat(),
    "verdict": "PASS" if all(s == "PASS" for s in statuses) else "FAIL",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": ("Delta since ff388424: course/modules/M/M7/project.html, cards.json, tests/labs/M7/lab-M7-project-3.py; all hunks read. "
              "Not checked: a full line-by-line read of all 168 cards against L01-L08 (PRJ-R6-33 UNVERIFIABLE); "
              "the browser sweep (page_smoke --skip-sweep not used, but only project.html was swept); "
              "the three r8 alternatives were not re-run (PRJ-R8-14 carried); "
              "no new alternative algorithm was built, only the two r11 alternatives were re-run; "
              "the full repository test suite was not run. Six survivors are equivalent mutants that should be removed from ledgers/M7/mutants (see PRJ-R6-31)."),
    "summary": {"rows": len(rows), "pass": statuses.count("PASS"), "fail": statuses.count("FAIL"),
                "unverifiable": statuses.count("UNVERIFIABLE"), "mutants": len(mutants),
                "mutants_killed": sum(1 for m in mutants if m["killed_by"])},
}
out = ROOT / "ledgers/M7/M7-d.json"
out.write_text(json.dumps(fragment, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("rows", len(rows), "pass", statuses.count("PASS"), "fail", statuses.count("FAIL"), "unverifiable", statuses.count("UNVERIFIABLE"))
print("mutants", len(mutants), "killed", sum(1 for m in mutants if m["killed_by"]))
