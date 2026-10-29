"""Assemble the round-10 M7-d fragment from logs written in this checkout (evidence strings name the log or source)."""
import json
import pathlib
import re
import sys
from datetime import UTC, datetime

ROOT = pathlib.Path(sys.argv[1])
S = "ledgers/M7/scripts/M7-d-r10"
mut = []
for line in (ROOT / S / "mutate_all105.log").read_text(encoding="utf-8").splitlines():
    m = re.match(r"^(KILLED|SURVIVED) (\S+?): (.*) -> (.*)$", line)
    if not m:
        continue
    status, name, desc, killed = m.groups()
    desc = re.sub(r"^Student error \S+?:\s*", "", desc).strip()
    mut.append({"name": name, "description": desc,
                "killed_by": None if killed == "None" else killed, "status": status})
assert len(mut) == 105, len(mut)
survivors = [m["name"] for m in mut if m["killed_by"] is None]
assert sorted(survivors) == sorted([
    "q04_dual_residual_without_zero_floor.py", "r02_turnover_total_residual_dropped_from_primal.py",
    "r04_budget_left_out_of_primal_residual.py", "r05_turnover_total_slackness_term_zeroed.py",
    "v10_01_dual_residual_ignores_sector_and_turnover_multipliers.py",
    "v10_02_complementary_slackness_signed_not_absolute.py"]), survivors

def C(prev, ids, subject):
    return f"Carried from round 8 ({subject} byte-identical since ce7b382): "

R8 = "ce7b382"
rows = [
 # --- fresh gates, this round
 ("PRJ-R6-01", "tools/check_projects.py --unit M7", "tools/check_projects.py", "PASS", f"check_projects M7: PASS ({S}/check_projects.log, exit 0)"),
 ("PRJ-R6-02", "tools/check_pages.py --unit M7 (hours, ladder, data-hours)", "tools/check_pages.py", "PASS", f"check_pages M7: PASS ({S}/check_pages.log, exit 0)"),
 ("PRJ-R6-03", "tools/check_dag.py --unit M7 (concept links)", "course/modules/M/M7/project.html", "PASS", f"check_dag M7: PASS ({S}/check_dag.log, exit 0)"),
 ("PRJ-R6-04", "run_graders reference, seeds 0-49", "course/modules/M/M7/grader/reference.py", "PASS", f"run_graders M7: reference 50/50 seeds PASS ({S}/run_graders.log)"),
 ("PRJ-R6-05", "starter fails the suite", "course/modules/M/M7/grader/starter.py", "PASS", f"starter.py as constrained_allocator.py, seed 0: 360 failed, 3 passed ({S}/starter_fails.log)"),
 ("PRJ-R6-06", "collected test count equals the page's 363 for every seed", "course/modules/M/M7/project.html line 329; grader/test_project.py", "PASS", f"pytest --collect-only, seeds 0-9: 363 tests collected for every seed ({S}/collect.log)"),
 ("PRJ-R6-07", "all M7 lab twins via run_labs", "tests/labs/M7/", "PASS", f"run_labs M7: PASS (11/11) ({S}/run_labs.log); lesson twins L01-L08 run under python -I -W error, exit 0 (lab_L0*.out)"),
 ("PRJ-R6-08", "project twins under python -I -W error; stdout equals page expected block", "project.html; tests/labs/M7/lab-M7-project-1..3.py", "PASS", f"project twins exit 0 under -I -W error ({S}/lab_project-*.out); tools/embed_labs.py on a copy with --refresh reproduces project.html byte-for-byte, so the five expected blocks equal the twin output ({S}/embed_refresh_copy.log)"),
 ("PRJ-R6-09", "page code equals twin (lab 1, lab 2, lab 3)", "course/modules/M/M7/project.html lines 56-154, 172-270, 372-434", "PASS", f"embed_labs --refresh on a copy of project.html leaves it identical (diff empty), so every lab code block equals its twin ({S}/embed_refresh_copy.log)"),
 ("PRJ-R6-10", "Lab 1 numbers re-derived", "course/modules/M/M7/project.html lines 155-166", "PASS", f"project-1 output: budget-only 54/65, 5/26, -3/130; held asset 2; weights 9/11, 2/11, 0; nu -21/1100; lower multiplier 9/1100; objective -3/220 ({S}/lab_project-1.out)"),
 ("PRJ-R6-11", "Lab 3 residual claims re-derived", "course/modules/M/M7/project.html lines 435-438", "PASS", f"project-3 output: check B dual 9/1100 and stationarity 9/550; check C stationarity 1/6250 ({S}/lab_project-3.out)"),
 ("PRJ-R6-12", "certificate definitions (page 306-316) match the grader recomputation", "project.html lines 306, 313, 315; grader/test_project.py lines 85-115", "PASS", "Carried from round 8 (project.html lines 306, 313, 315 and grader/ byte-identical since ce7b382; the changed project.html hunks are lines 37, 55, 166, 293, 376): definitions match reference.py _certificate and test_project.py recomputation (lines 108-114)"),
 ("PRJ-R6-13", "sufficiency proposition and uniqueness proof (page 320-322)", "project.html lines 320-322", "PASS", "Carried from round 8 (project.html lines 320-322 byte-identical since ce7b382; no hunk touches them)"),
 ("PRJ-R6-14", "linearization of turnover constraint", "project.html line 307", "PASS", "Carried from round 8 (project.html line 307 byte-identical since ce7b382)"),
 ("PRJ-R6-15", "five hand-worked answers are correct", "grader/test_project.py lines 218-246", "PASS", "Carried from round 8 (grader/ byte-identical since ce7b382); exact alternatives and reference pass all hand cases on seeds 0-49 (PRJ-R10-07)"),
 ("PRJ-R6-16", "named ValueError conditions have refused and accepted tests", "grader/test_project.py lines 553-567, 590-596, 670-693, 697-", "PASS", "Carried from round 8 (grader/ byte-identical since ce7b382); collect count and reference pass re-run this round (PRJ-R6-06, PRJ-R6-04)"),
 ("PRJ-R6-17", "instances SIMULATED, feasible by construction, <=3 decimals, both sectors non-empty", "course/modules/M/M7/grader/instance.py lines 34-68", "PASS", "Carried from round 8 (grader/instance.py byte-identical since ce7b382)"),
 ("PRJ-R6-18", "solution may use standard library only; no grader import", "grader/test_project.py lines 268-282", "PASS", "Carried from round 8 (grader/ byte-identical since ce7b382)"),
 ("PRJ-R6-19", "ruff check and format on the labs and grader; mypy", "tests/labs/M7; course/modules/M/M7/grader", "PASS", f"ruff check and format --check: All checks passed, 15 files formatted ({S}/ruff.log); mypy --no-incremental: Success, 255 files ({S}/mypy.log)"),
 ("PRJ-R6-20", "reading-list keys resolve in the registry (offline integrity)", "course/modules/M/M7/project.html lines 459-460; references/references.json", "PASS", "Carried from round 8 (references/ and tools/ byte-identical since ce7b382; project.html lines 459-460 not in any hunk)"),
 ("PRJ-R6-21", "page_smoke M7 project (render and in-browser grader)", "course/modules/M/M7/project.html", "PASS", f"page_smoke M7: PASS, in-browser grader 363 tests pass on the sample seed ({S}/page_smoke.log)"),
 ("PRJ-R6-22", "hours: project components sum to 33; lessons 77 + project 33 = 110", "project.html lines 337-351; index.html data-hours", "PASS", f"check_pages M7 PASS ({S}/check_pages.log), which reads the hours and data-hours"),
 ("PRJ-R6-23", "no process words in learner text", "project.html (changed hunks lines 37, 55, 166, 293, 376); cards.json (changed cards)", "PASS", "grep of the five changed project.html lines and of the 24 changed or added cards finds no process word (round, verifier, builder, draft, fixed)"),
 ("PRJ-R6-24", "notation: symbols vs notation/notation.json", "project.html lines 303-308", "PASS", "Carried from round 8 (project.html lines 303-308 byte-identical since ce7b382); the K change at line 293 uses the existing symbol K"),
 ("PRJ-R6-25", "cards: numbers on each back appear in the card's own lesson; no duplicate ids or fronts", "course/modules/M/M7/cards.json (157 cards)", "PASS", f"cards_numbers_r10.py ({S}/cards_numbers_r10.log) flags 15 tokens; each is a TeX-encoded fraction in the card's own lesson (for example \\tfrac23 in L02 for 2/3, \\tfrac18 in L03 for 1/8, \\tfrac{{11}}{{30}} in L03), so the checker reports false absences; duplicate ids []; duplicate fronts []"),
 ("PRJ-R6-26", "cards: numeric claims re-derived or matched to lab output", "course/modules/M/M7/cards.json", "UNVERIFIABLE", "Changed and added cards were re-read this round (PRJ-R10-08 to PRJ-R10-10). Not re-derived: the exact-fraction values 0.5722548 (card M7-c113) and 0.5588607 (card M7-c114) are not printed by the L06 lab, and no exact recomputation was run. Unchanged cards were not re-derived this round. Fix: print the exact values in the L06 lab, or cite the lab line that prints them."),
 ("PRJ-R6-27", "notation glyph 1 (all-ones) vs registry macro", "course/modules/M/M7/project.html lines 306, 313", "PASS", "Carried from round 8 (project.html lines 306, 313 byte-identical since ce7b382)"),
 ("PRJ-R6-28", "dual residual floor at zero is exercised by the suite (spec line 315)", "grader/test_project.py lines 105-116, 365-369; grader/reference.py line 287", "FAIL", f"Spec line 315 says the dual residual is max(0, -min) over the inequality multipliers. Reference min multiplier over seeds 0-49 is 0.0 on 50 of 50 seeds ({S}/minmult_r10.log), because every inactive inequality has multiplier 0 under complementary slackness. The floor branch is therefore never exercised, and mutant q04 (no floor) survives seeds 0-9 ({S}/mutate_all105.log). Fix: add a case whose inequality multipliers are all strictly positive (every inequality active) and assert the certificate's dual_residual equals max(0, -min) with that minimum, or assert the value on a hand case where the minimum is positive."),
 ("PRJ-R6-29", "hand-worked cases: certificate fields checked against the recomputation", "grader/test_project.py lines 388-410", "PASS", "Carried from round 8 (grader/ byte-identical since ce7b382)"),
 ("PRJ-R6-30", "objective against three feasible comparators (page line 329)", "grader/test_project.py lines 372-383; project.html line 329", "PASS", "Carried from round 8 (grader/ and project.html line 329 byte-identical since ce7b382)"),
 ("PRJ-R6-31", "mutant suite: every grader mutant killed (ledgers/M7/mutants, seeds 0-9)", "ledgers/M7/mutants/ (105 files); tools/mutate_graders.py --unit M7 --seeds 0-9", "FAIL", f"mutate_graders M7: FAIL, 99/105 killed ({S}/mutate_all105.log). Survivors: q04 (PRJ-R6-28); r02_turnover_total_residual_dropped_from_primal, r04_budget_left_out_of_primal_residual, r05_turnover_total_slackness_term_zeroed (certificate-term mutants of the reference, unchanged since ce7b382); v10_01 and v10_02 (PRJ-R10-06). Fix: add certificate-term tests for the turnover-total term in the primal residual, the budget term in the primal residual and the turnover-total complementary-slackness term, each on a student output that is otherwise KKT-consistent."),
 ("PRJ-R6-32", "five alternative correct implementations pass the suite (rule 11)", "ledgers/M7/scripts/M7-d-r8/alt/ (3 exact); ledgers/M7/scripts/M7-d-r7/alt/alt_float.py", "FAIL", f"Exact alternatives: 150 of 150 runs pass ({S}/alts_exact_r10.log). Float alternative alt_float.py fails 15 of 50 seeds ({S}/alt_float_0-49.log), all on valid tiny-gamma cases: gamma-positive-zero-boundary (10 seeds), gamma-positive-negative-boundary (10 seeds), gamma-just-inside-zero (9 seeds), each raising RuntimeError 'the working set lost independence' from the active-set test with an absolute tolerance of 1e-9. The page says gamma is a positive number, so the grader demands an answer at gamma = 1e-9; whether a float solver must meet that is not stated. Fix: the planner rules whether a scale-aware float solver must pass; if yes, the alternative is a student error and the row becomes PASS after the ruling; if not, state the numerical requirement on the page."),
 ("PRJ-R6-33", "cards: every card agrees with the CURRENT lesson text (rule 10, full read)", "course/modules/M/M7/cards.json (157) vs L01.html-L08.html", "UNVERIFIABLE", "Not completed. Read this round: the 16 changed cards and 8 added cards (PRJ-R10-08 to PRJ-R10-10); card M7-c175 fails (PRJ-R10-09). The other 133 cards were not re-read line by line against their lessons this round. Two claims in the changed set are unverified (PRJ-R6-26). Fix: a full card-by-lesson read."),
 ("PRJ-R6-34", "browser-only claims: autosave; nothing you write leaves the browser", "project.html line 355 and footer line 474", "UNVERIFIABLE", "Static evidence only: course/assets/js/store.js opens indexedDB; grader.js and python.js make GET fetches of the suite and the runtime, and no POST or beacon was found in assets/js. The autosave timing and the 'where the browser allows storage' condition were not exercised in a browser. Honest gap."),
 ("PRJ-R6-35", "Lab 1 prose: code prints the four KKT quantities in steps 4 to 6", "course/modules/M/M7/project.html line 55", "PASS", f"Superseded by the changed line 55, verified: steps 4 (stationarity residuals), 5 (budget gap, smallest and largest weight), 6 (multiplier sign, weight times multiplier) print in project-1 output ({S}/lab_project-1.out)"),
 ("PRJ-R6-36", "Lab 3 prose claims about which residuals respond", "course/modules/M/M7/project.html line 438", "PASS", f"Carried from round 8 (project.html line 438 byte-identical since ce7b382): check B changes only dual and stationarity, check C only stationarity; matches project-3 output ({S}/lab_project-3.out)"),
 ("PRJ-R6-37", "card ids unique; gaps in the id sequence", "course/modules/M/M7/cards.json", "PASS", "157 ids, all distinct (python check this round); id range M7-c001..M7-c175 with gaps as reported by cards_numbers_r10.log"),
 ("PRJ-R6-38", "pyflakes/type checks of the grader", "grader/test_project.py, reference.py, instance.py, starter.py", "PASS", f"mypy --no-incremental over 255 files: Success ({S}/mypy.log); ruff check passes ({S}/ruff.log)"),
 # --- delta rows from rounds 7-8 (ids kept)
 ("PRJ-R7-01", "delta since pin 44f1eb6 read in full (round-7 row)", "project.html; grader/test_project.py; cards.json; tests/labs", "PASS", "Historical delta row. Superseded: every file it covered is re-verified in this round by the rows above and by PRJ-R10-01 to PRJ-R10-11"),
 ("PRJ-R8-01", "delta since 7aa909e: project.html lede (line 39) wording", "course/modules/M/M7/project.html line 37", "PASS", "Superseded: the lede moved to line 37 and was re-worded; the current wording is verified in PRJ-R10-01"),
 ("PRJ-R8-02", "delta since 7aa909e: spec context (line 290) 'checks the four KKT conditions'", "course/modules/M/M7/project.html line 293", "PASS", "Superseded: the instance text moved to line 293 and was changed (K as the length of sector_caps); verified in PRJ-R10-03"),
 ("PRJ-R8-03", "cards c009 and c165 (Q1, Q2 eigenvalues) against L01", "cards.json c009, c165; L01.html", "PASS", "Carried from round 8 (cards c009 and c165 and L01.html byte-identical since ce7b382: neither id is in the changed or added set)"),
 ("PRJ-R8-04", "card c042 (sufficiency theorem) against L03 Theorem 2.1 and Remark 2.2", "cards.json c042; L03.html", "PASS", "Carried from round 8 (card c042 and L03.html byte-identical since ce7b382)"),
 ("PRJ-R8-05", "cards c080 and c166 (Remark 2.4) against L05", "cards.json c080, c166; L05.html", "PASS", "Carried from round 8 (cards c080, c166 and L05.html byte-identical since ce7b382)"),
 ("PRJ-R8-06", "card c084 (midpoint uniqueness) against L05 Proposition 3.4", "cards.json c084; L05.html", "PASS", "Carried from round 8 (card c084 and L05.html byte-identical since ce7b382); its 1/8 is TeX \\tfrac{1}{8} in L05 (PRJ-R6-25)"),
 ("PRJ-R8-07", "cards c100 and c167 (budget closed form, 1'z > 0) against L06 Theorem 1.3 and P2", "cards.json c100, c167; L06.html", "PASS", "Superseded for c100: the card changed and now states its hypotheses (gamma > 0, Sigma symmetric positive definite); Theorem 1.3 exists in L06 (grep). c167 carried from round 8 (byte-identical since ce7b382)"),
 ("PRJ-R8-08", "card c107 (QP with turnover) against L06 Proposition 3.4 and Remark 3.5", "cards.json c107; L06.html", "PASS", "Carried from round 8 (card c107 and L06.html byte-identical since ce7b382)"),
 ("PRJ-R8-09", "L06 notation change a,b -> y,z: no stale meaning left", "course/modules/M/M7/L06.html", "PASS", "Carried from round 8 (L06.html byte-identical since ce7b382)"),
 ("PRJ-R8-10", "grader, twins, tools, references unchanged since the round-7 pin", "course/modules/M/M7/grader/; tests/labs/M7/lab-M7-project-1.py, -2.py; tools/; references/", "PASS", "Carried from round 8 (grader/, lab-M7-project-1.py, lab-M7-project-2.py, tools/, references/ byte-identical since ce7b382); lab-M7-project-3.py changed and is re-verified by PRJ-R6-08 and PRJ-R6-11"),
 ("PRJ-R8-11", "L06 lab twin change (tests/labs/M7/lab-M7-L06-1.py) still runs and matches its block", "tests/labs/M7/lab-M7-L06-1.py; L06.html", "PASS", f"lab-M7-L06-1.py exit 0 under -I -W error ({S}/lab_L06.out); twin and L06.html byte-identical since ce7b382"),
 ("PRJ-R8-12", "L06 numbers in cards c113 and c114 (unrounded values)", "cards.json c113, c114; L06.html Part D and Part B", "UNVERIFIABLE", "Changed cards. The printed values (0.820002, 1.392257, 0.558861) match the lab; the exact-fraction values (0.5722548, 0.5588607) are not printed by the lab and were not recomputed. See PRJ-R6-26."),
 ("PRJ-R8-13", "new student-error mutants r8_m01..r8_m06 (verifier's own, >= 3 required)", "ledgers/M7/mutants/r8_m01..r8_m06", "PASS", "Six r8_ mutant files present in ledgers/M7/mutants (ls); they are part of the 105 run in PRJ-R6-31"),
 ("PRJ-R8-14", "three exact alternatives pass the suite, seeds 0-49", "ledgers/M7/scripts/M7-d-r8/alt/alt_reverse_order.py, alt_nullspace.py, alt_empty_start.py", "PASS", f"Re-run this round: 150 of 150 runs pass 363 ({S}/alts_exact_r10.log)"),
 ("PRJ-R8-15", "reference multiplier scan (supports PRJ-R6-28)", "ledgers/M7/scripts/M7-d-r8/minmult_r8.py", "PASS", f"Re-run this round against this checkout's reference: 50 of 50 seeds have minimum multiplier 0.0 ({S}/minmult_r10.log)"),
 # --- new round-10 delta rows
 ("PRJ-R10-01", "lede stationarity wording (project.html line 37)", "course/modules/M/M7/project.html line 37", "PASS", "Stationarity 'the gradient, plus each multiplier times the gradient of its constraint, is zero' matches reference.py r_w: gradient + budget - lower + upper + sector + plus - minus (signs follow g = lower - w, g = w - upper, h = 1'w - 1)"),
 ("PRJ-R10-02", "Lab 1 hypothesis (project.html line 55): steps 4 to 6 print the KKT checks", "course/modules/M/M7/project.html line 55", "PASS", f"project-1 output prints stationarity residuals (step 4), budget gap and bounds (step 5), multiplier sign and product (step 6) ({S}/lab_project-1.out)"),
 ("PRJ-R10-03", "instance text (project.html line 293): K equals the length of sector_caps", "course/modules/M/M7/project.html line 293; grader/reference.py line 87; grader/instance.py line 51", "PASS", "reference.py _parse takes K from the length of sector_caps (caps list); instance.py builds one cap per sector; the page sentence matches"),
 ("PRJ-R10-04", "certificate definitions (project.html line 315): complementary slackness is the largest |lambda_j g_j|", "project.html line 315; grader/reference.py _certificate; tests/labs/M7/lab-M7-project-3.py docstring", "PASS", f"reference computes max(abs(m * g)); the lab-3 docstring (changed) says primal, stationarity and dual are largest violations and CS is the largest absolute product; project-3 output shows complementary 0 in all three checks ({S}/lab_project-3.out)"),
 ("PRJ-R10-05", "Lab 3 interpretation (project.html line 439) numbers", "course/modules/M/M7/project.html line 439", "PASS", f"check B dual 9/1100 and stationarity 9/550; check C stationarity 1/6250 match project-3 output ({S}/lab_project-3.out)"),
 ("PRJ-R10-06", "new student-error grader mutants (>= 3 required) and their kills", "ledgers/M7/mutants/v10_01..v10_03", "FAIL", f"Three new mutants written ({S}/make_mutants_r10.py). v10_03 (turnover stationarity sign) killed by test_certificate_agrees_with_the_recomputed_residuals (seed 0). v10_01 (dual residual ignores sector and turnover multipliers) and v10_02 (complementary slackness signed, not absolute) survive: on the reference output the omitted terms and the sign coincide (every dual or CS term is 0 on a KKT answer), so the mutants are equivalent on valid outputs. The spec states both definitions (project.html line 315), and the grader only catches them if an output carries a negative sector or turnover multiplier (test_multipliers_are_non_negative) or a slack constraint with positive multiplier (test_complementary_slackness_holds), which the grader does catch in those outputs, but no test checks the certificate's dual and CS fields on such an output. Fix: add a certificate-agreement test on a non-KKT output where a sector or turnover multiplier is negative and where a slack constraint carries a positive multiplier, asserting dual_residual and complementary_slackness equal the spec definitions."),
 ("PRJ-R10-07", "exact alternative implementations pass on seeds 0-49 (rule 11)", "ledgers/M7/scripts/M7-d-r8/alt/ (3 files)", "PASS", f"alt_empty_start, alt_nullspace, alt_reverse_order: 150 of 150 runs 363 passed ({S}/alts_exact_r10.log)"),
 ("PRJ-R10-08", "cards c168 to c174 (added): numbers and claims against lab output", "cards.json c168-c174; lab-M7-L02-1 to L06-1 outputs", "PASS", f"c168 f(w) = 177/110 = lambda/2 (lab-L02 line 'objective f(w) = 177/110'; P3 in L02); c169 budget and residual exact, Prop 3.2 (b),(c) in L02; c170 largest dual -1/2 at (0, 3/10), -1/2 at (1,0), gap 0, Prop 1.4 in L04 (lab-L04); c171 det 19, Prop 2.1 in L05 (lab-L05); c172 0 of 1089 below -9/4 (lab-L05); c174 candidates_passing 1 at every gamma (lab-L06). Outputs in {S}/lab_L0*.out"),
 ("PRJ-R10-09", "card c175 (added): 'the lab prints recursion_matches_brute_force True at all 18 pairs'", "cards.json M7-c175; tests/labs/M7/lab-M7-L08-1.py lines 115-121", "FAIL", "The lab prints one aggregate line, 'recursion_matches_brute_force True' (lab-L08 output), computed as a conjunction over the t and s pairs; it prints no per-pair result. Fix: reword the card to say the lab prints one True that is the conjunction over the 18 (t, s) pairs, or print the 18 results."),
 ("PRJ-R10-10", "changed cards c003, c028, c049, c052, c063, c087, c089, c100, c102, c109, c112, c153, c163, c164 against their lessons and lab output", "cards.json (those ids); L01-L06, L08 lessons and outputs", "PASS", f"c003 Example 1.2 in L01; c028 lambda and w from lab-L02 output; c049 'hold exactly: True' printed per candidate (lab-L03); c052 Example 4.1 text in L03 (w1 >= 0 slack, multiplier 0; w2 >= 0 multiplier 3/10); c063 counts 1331, 21, 27951 (lab-L04); c087 x and lambda (lab-L05); c089 only {2}, x-hat (3/2, 0), -9/4 (lab-L05); c100 Theorem 1.3 in L06; c102 and c164 Proposition 2.1 (V(gamma1) <= V(gamma2)) and Remark 2.2 in L06; c109 sigma diagonal (lab-L06); c112 zero set {{A4}} at five gammas (lab-L06); c153 378 = 3 x 126 (lab-L08); c163 Proposition 3.4 in L06 statement. Outputs in {S}/lab_L0*.out"),
 ("PRJ-R10-11", "changed cards c113 and c114: the exact-fraction values", "cards.json c113, c114; tests/labs/M7/lab-M7-L06-1.py", "UNVERIFIABLE", "The printed values match (1.392257 and 0.820002 at gamma 16; turnover 0.558861 at gamma 4; 0.558860 recomputed by hand from the printed six-place weights against the equal-weight portfolio). The exact values 0.5722548 and 0.5588607 are not printed and were not recomputed. Fix: print them in the lab, or cite the printing line."),
]
out_rows = []
for rid, check, loc, status, ev in rows:
    out_rows.append({"id": rid, "check": check, "location": loc, "status": status, "evidence": ev})
    if status != "PASS":
        out_rows[-1]["fix"] = "see evidence"
mutants = []
for m in mut:
    mutants.append({"name": m["name"], "description": m["description"], "killed_by": m["killed_by"], "status": m["status"]})
counts = {}
for r in out_rows:
    counts[r["status"]] = counts.get(r["status"], 0) + 1
fragment = {
    "unit": "M7", "slice": "d", "round": 10, "verifier": "Haiku 5.5 independent verifier (round 10)",
    "pin": "e8b10b8110923bd88c3b4bd0e36e1571be3e6725", "base": "ce7b3821c288da3dbba5dd4c90fb87dfd6d30089 (round-8 pin)",
    "checkout": str(ROOT), "scratch": "/tmp/m7d_r10_* (alt, minmult, collect, float, page copies)",
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "verdict": "FAIL" if any(r["status"] != "PASS" for r in out_rows) else "PASS",
    "rows": out_rows, "mutants": mutants, "registry_flags": [],
    "freshness_flags": ["cards.json: 16 changed (c003, c028, c049, c052, c063, c087, c089, c100, c102, c109, c112, c113, c114, c153, c163, c164) and 8 added (c168-c175) since ce7b382; project.html hunks at lines 37, 55, 166, 293, 376; lab-M7-project-3.py docstring"],
    "notes": ("Delta ce7b382..e8b10b8 read in full: project.html (5 hunks), cards.json (16 changed, 8 added), lab-M7-project-3.py docstring, round-8/9 ledger and mutant files. "
              "The grader/ directory and tools/references are byte-identical to ce7b382. The round-9 fragment (B-M7-d.round9.json) is not present in /Users/billyribeiro/.fanout/frags; round-8 (B-M7-d.round8.json) was used as context. "
              "Not checked: a full card-by-lesson read of the unchanged cards, the browser storage behaviour, and the 'five correct alternatives' requirement beyond 3 exact + 1 float."),
    "summary": {"rows": len(out_rows), "pass": counts.get("PASS", 0), "fail": counts.get("FAIL", 0),
                "unverifiable": counts.get("UNVERIFIABLE", 0), "mutants": len(mutants),
                "mutants_killed": sum(1 for m in mutants if m["killed_by"])},
}
path = ROOT / "ledgers/M7/M7-d.json"
path.write_text(json.dumps(fragment, ensure_ascii=False, indent=2), encoding="utf-8")
print("wrote", path, fragment["summary"], fragment["verdict"])
