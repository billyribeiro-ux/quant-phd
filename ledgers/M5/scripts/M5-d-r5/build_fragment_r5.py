"""Builds ledgers/M5/M5-d.json (round 5, slice M5-d). Verifier-written; every status is a finding of the round-5 checks.

Inputs: outputs/mutate.out (tools/mutate_graders.py --unit M5, run by the verifier), the mutant docstrings,
and the killed_by test names recorded in outputs/ and names.sh runs. Run from the checkout root with .venv.
"""
import json
import re
from pathlib import Path

ROOT = Path("/tmp/verifyB5-M5-d")
OUT = ROOT / "ledgers/M5/scripts/M5-d-r5/outputs"
MUT = ROOT / "ledgers/M5/mutants"

mutants = []
for line in (OUT / "mutate.out").read_text().splitlines():
    m = re.match(r"^(KILLED|SURVIVED) (\S+?\.py): (.*) -> (\S.*)$", line)
    if not m:
        continue
    status, fname, desc, killer = m.groups()
    killed_by = None if killer.strip() == "None" else killer.strip()
    mutants.append({"file": f"ledgers/M5/mutants/{fname}", "description": desc.strip(), "killed_by": killed_by})

new = {
    "m79_relative_change_certificate.py": "test_certified_error_bounds_the_distance_to_the_fixed_point[1] (seed 0)",
    "m80_stops_at_the_a_priori_count.py": "test_certified_error_exactly_at_tol_stops_the_first_sweep (seed 0)",
    "m81_first_grid_point_never_a_successor.py": "test_tolerance_above_one_is_accepted (seed 0)",
}
for fname, killer in new.items():
    doc = (MUT / fname).read_text().split('"""')[1].split("\n")[0]
    mutants.append({"file": f"ledgers/M5/mutants/{fname}", "description": doc.strip(), "killed_by": killer})

seen = {m["file"] for m in mutants}
assert len(mutants) == 81 and len(seen) == 81, (len(mutants), len(seen))
assert all((ROOT / m["file"]).exists() for m in mutants)

S = "scripts/M5-d-r5/"
rows = [
 ("d-lab1-output", "Lab 1 printed output recomputed independently", "course/modules/M/M5/project.html lines 140-153, 58-137; " + S + "nums_r5.py",
  "PASS", f"{S}outputs/nums_r5.out recomputes from unrounded values: V1 (0.4550898606, 0.6698382626, 0.8265687852), sup|BV-BW| 0.4095808745 vs beta*sup 0.7439119067, first certified 7.4391190665, stop sweep 146, certified 9.495187e-07 and actual 9.495177e-07 (both print 0.000000950). run_labs --unit M5 --page project: 3/3 PASS (outputs/run_labs.out)."),
 ("d-lab2-output", "Lab 2 completed lines and printed output", "course/modules/M/M5/project.html lines 157-218; tests/labs/M5/lab-M5-project-2.py",
  "PASS", f"{S}outputs/nums_r5.out: ratio 0.3000000000 (V=0, W=(0.1,0.2,0.3)); sweeps 146; cert 9.4951873564e-07 -> '9.495e-07'; last change 1.0550208174e-07 -> '1.055e-07'; the page's '9.495187e-7' matches the unrounded value. Embedded code equals the twin except the two ___ blanks (diff checked)."),
 ("d-lab3-output", "Lab 3 printed output recomputed, including the grid values and the 200-pair ratio", "course/modules/M/M5/project.html lines 285-388; tests/labs/M5/lab-M5-project-3.py",
  "PASS", f"{S}outputs/nums_r5.out: gap 0.0218288721 (prints 0.021829); sweeps 236; last change 1.025135532e-11; cert 9.226219788e-11; a priori 242; residual 9.226397e-12 <= (1+beta)*cert = 1.753e-10; residual/cert 0.100002; worst ratio over 200 pairs 0.900000000000000 (minus beta 1.1e-16); V(0.45)..V(2.7) match the printed six decimals (V(1.7)=6.074533546->6.074534, V(1.95)=6.103036803->6.103037, V(2.45)=6.151012775->6.151013, V(2.7)=6.171667733->6.171668)."),
 ("d-lab-code-twin", "Embedded lab code equals its twin", "course/modules/M/M5/project.html data-run blocks; tests/labs/M5/lab-M5-project-1..3.py", "PASS",
  "Python difflib of each data-run block against its twin: Lab 1 and Lab 3 identical; Lab 2 differs only in the two ___ blanks (the completed lines are the twin's lines)."),
 ("d-lab-run-gate", "Lab gates: run_labs, page_smoke, check_pages, check_projects", "tools/run_labs.py --unit M5 --page project; tools/page_smoke.py --unit M5 --pages project; tools/check_pages.py --unit M5; tools/check_projects.py --unit M5",
  "PASS", "outputs/run_labs.out 'run_labs M5: PASS (3/3)'; outputs/page_smoke.out 'page_smoke M5: PASS' (in-browser grader 86 tests pass on seed 973103070, 0.9 s); outputs/check_pages.out and check_projects.out PASS; check_dag PASS (outputs/check_dag.out)."),
 ("d-lab-claims-prose", "Prose claims about what the labs print and check", "course/modules/M/M5/project.html lines 53, 57, 154, 159, 217, 287, 357-388",
  "PASS", "Each sentence checked against outputs/nums_r5.out and the lab code: the 'agree to nine decimals' claim (line 154) holds on the printed 0.000000950 pair; 'the printed check confirms' (line 464) holds; 'about 9.5e-7' (line 154) is the value printed in Lab 2 and the unrounded 9.495e-7 is shown; the Lab 3 tie claim covers every feasibility pair (min over all k, k' in GRID); 'printed values say nothing about any other grid' is true of a printed output."),
 ("d-grader-count", "Test count on the page equals the collected count", "course/modules/M/M5/project.html line 233; grader/test_project.py",
  "PASS", f"{S}suite_on.py --collect with the reference: '86 tests collected' (matches 'runs 86 checks')."),
 ("d-grader-reference-seeds", "Reference passes on seeds 0-49; starter fails; time limit", "tools/run_graders.py --unit M5 --seeds 0-49; grader/reference.py", "PASS",
  "outputs/run_graders.out: 'run_graders M5: PASS (reference 50/50 seeds, slowest 0.3 s)'; the starter is refused by the same run."),
 ("d-grader-alternatives", "Alternative correct implementations pass the suite (over-constraint check)", S + "alt/alt5c_euclidean_change.py; " + "course/modules/M/M5/grader/test_project.py",
  "FAIL", f"{S}outputs/alt5c_euclidean_change.out: 35 of 50 seeds FAIL. Tally over seeds 0-49: test_iterations_within_the_a_priori_count[0] 22 seeds, [1] 25 seeds. Witness: seed 1, instance 0 (beta 0.95, alpha 0.3, 21 points, tol 1e-8): a priori count 423, Euclidean-certificate solver stops after 426 sweeps (limit 424); the reference stops after 396. The certificate beta/(1-beta)*||V_n - V_(n-1)||_2 is valid (it dominates the sup-norm bound), which page line 243 allows ('another is any bound your proof establishes'), but page line 245 and the test demand the a priori count plus one."),
 ("d-grader-alt-valid", "Alternative correct implementations that do pass", S + "alt/alt5a_reference_style_precomputed.py, alt5b_min_of_sweep_and_apriori.py, alt5d_apriori_only.py, alt5e_relative_cutoff.py, alt5f_doubled_certificate_valid.py", "PASS",
  f"{S}outputs/alt5a_*.out, alt5b_*.out, alt5d_*.out, alt5e_*.out: 50/50 seeds PASS each (precomputed feasible lists and x**0.5; min of the sweep bound and the a priori bound; a priori bound alone; relative feasibility cutoff 1e-12). alt5f (certificate doubled, valid but looser) passes all 50 seeds because its extra sweeps stay within the count; it is therefore not a student error the page forbids and was removed from the mutant list."),
 ("d-grader-existing-mutants", "All existing mutants under tools/mutate_graders.py --unit M5 --seeds 0-49", "tools/mutate_graders.py --unit M5 --seeds 0-49; ledgers/M5/mutants/ (78 files, m01-m78)", "FAIL",
  f"{S}outputs/mutate.out: 'mutate_graders M5: FAIL (77/78 killed)'. The one survivor is m64 (row d-grader-survivor-m64)."),
 ("d-grader-new-mutants-killed", "Mutants m48-m51 (round-3 verifier student errors) are killed", "ledgers/M5/mutants/m48..m51", "PASS",
  f"{S}outputs/mutate.out: KILLED m48 (test_operator_matches_its_definition[0]), m49, m50, m51 (test_certified_error_bounds...[0])."),
 ("d-grader-r2-mutants", "Mutants m32-m37 are killed", "ledgers/M5/mutants/m32..m37", "PASS", f"{S}outputs/mutate.out: KILLED m32..m37."),
 ("d-grader-new-mutants-r4", "Mutants m62-m67 are killed, except m64 (separate row)", "ledgers/M5/mutants/m62..m67", "PASS",
  f"{S}outputs/mutate.out: KILLED m62, m63, m65, m66, m67 (m64 SURVIVED, see d-grader-survivor-m64)."),
 ("d-grader-builder-mutants-r4", "Mutants m68-m78 added by the builder are killed", "ledgers/M5/mutants/m68..m78", "PASS",
  f"{S}outputs/mutate.out: KILLED m68..m78 (m76 grid whose last point is at most one; m78 feasibility with tie tolerance)."),
 ("d-grader-new-mutants-r5", "Three new student-error mutants written by the verifier are killed", "ledgers/M5/mutants/m79_relative_change_certificate.py, m80_stops_at_the_a_priori_count.py, m81_first_grid_point_never_a_successor.py", "PASS",
  f"{S}outputs/m79_relative_change_certificate.out: FAIL on 48 of 50 seeds (killed on seed 0 by test_certified_error_bounds...[1]); {S}outputs/m80_stops_at_the_a_priori_count.out: FAIL on 50 of 50 seeds; m81 (first grid point never a successor): 25 failing tests on seed 0 (names.sh run), including test_operator_matches... family and test_certified_error_bounds...[0]. A relative-change certificate and a stop at the a priori count are plausible student errors; the page's Stopping and Certified-error conventions (lines 243-244) forbid both."),
 ("d-grader-survivor-m64", "m64 (change measured at the last grid point only) is killed", "ledgers/M5/mutants/m64_change_measured_at_the_last_point_only.py; course/modules/M/M5/project.html line 243", "FAIL",
  f"{S}outputs/mutate.out: SURVIVED m64 on seeds 0-49. Numerical check {S}monotone_change_r5.py ({S}outputs/monotone_change_r5.out): over 708,000 sweeps on random instances (beta 0.5-0.99, alpha 0.05-0.95, 2-12 points) the change vector is never negative and never decreases in k, so its sup is at the last point and m64 computes the same certificate on every tested instance. No proof of this monotonicity is in the material, so the survivor cannot be classed as equivalent (VERIFIER_RULES section 3). Fix: prove the monotone change (or that the sup change sits at the last grid point) and move m64 out of the mutant list with the proof row; a test cannot kill a mutant that is equivalent on the operator."),
 ("d-grader-exceptions", "ValueError only for conditions the page names", "grader/test_project.py lines 440-547; project.html line 246", "PASS",
  "must_raise is used only for beta, alpha, tol, max_iter, grid and values-length (each named at page line 246); the other conditions are plain checks. Boolean and float budgets and NaN/inf tolerances are named there."),
 ("d-grader-instance", "instance.py matches its docstring ranges", "grader/instance.py lines 1-62", "PASS",
  "beta randrange(80,96)/100 = 0.80-0.95; alpha randrange(30,71)/100 = 0.30-0.70; size 8-24; first point 0.20-0.90; steps 0.05-0.40; last point above 1; tol in {1e-6,1e-8,1e-10}; the tie test uses the 1e-6 margin as documented."),
 ("d-grader-time-limit", "120-second browser limit", "project.html line 231; course/assets/js/python.js line 4", "PASS", "python.js TIMEOUT_MS = 120000 matches 'stops after 120 seconds'."),
 ("d-grader-tie-boundary", "Exact feasibility k' <= k**alpha and tie stop", "grader/test_project.py lines 341-360", "PASS", "tests are named at page lines 242-243 and the feasibility convention; reference passes; m15/m26/m72 killed."),
 ("d-grader-start-zero", "Iteration starts from V0 = 0 and is synchronous", "grader/test_project.py lines 363-376; project.html line 242", "PASS", "test_the_first_sweep... and m16, m29, m63, m74 killed (outputs/mutate.out)."),
 ("d-grader-converged-boundary", "converged iff certified_error <= tol; tie stops the first sweep", "grader/test_project.py lines 379-398; project.html line 243-244", "PASS", "m18, m28, m32, m42, m69 killed; reference passes."),
 ("d-grader-tolerance-just-below", "Tolerance just below the first certified error does not stop", "grader/test_project.py lines 401-416", "PASS", "alt5a, alt5b, alt5d, alt5e, alt5f pass it; m77 killed (outputs/mutate.out)."),
 ("d-grader-instance-seeds", "Two instances per seed (SEED and SEED+7919)", "grader/test_project.py line 35; project.html line 233", "PASS", "page line 233 and the test header agree (SEED and SEED + 7919)."),
 ("d-hours", "Hub hours split against lesson hours and the project table", "project.html lines 251-266 (table: 1+2+8+7+3+5 = 26); course/modules/M/M5/index.html data-hours-lessons=104, data-hours-project=26; lessons L01-L06 10 h, L07-L10 11 h",
  "PASS", "6*10 + 4*11 = 104 = data-hours-lessons; 104 + 26 = 130 (the module); 26/130 = 20.0% as printed. Pace not judged (architect ruling)."),
 ("d-tools-structure", "Structure: check_projects, check_pages, check_dag", "tools/check_projects.py --unit M5; tools/check_pages.py --unit M5; tools/check_dag.py --unit M5", "PASS", "outputs/check_projects.out, check_pages.out, check_dag.out: PASS. The page links to concepts only inside the M5 closure (contraction-mapping at L07, value-function-iteration at L09) and to index.html#placement, which exists."),
 ("d-references", "Reading section and references", "project.html Reading section (line 500); references/references.json", "PASS",
  "tools/verify_refs.py --unit M5: live, '2 of 560 entries, 0 problems' (outputs/verify_live.out); --offline '560 entries, 0 problems'. The reading section attributes nothing to Abbott or Rudin and names no locator."),
 ("d-cards-integrity", "cards.json: 200 cards, unique ids, lesson fields, grades", "course/modules/M/M5/cards.json; " + S + "cards_check.py",
  "PASS", f"200 cards, 200 unique ids (M5-c001..c200), 132 graded (98 T, 34 C); {S}cards_check.py: 3 number tokens not literally in the lesson, all LaTeX-form matches checked by hand (c137 '5.6 x 10^-16' is written as \\(5.6 \\times 10^{{-16}}\\) in L08; c154 '1.067 x 10^-6' and '9.60 x 10^-7' are written in L09 Problem R2)."),
 ("d-cards-L07-L09-numbers", "L07, L09 card numbers against the lab outputs", "cards.json M5-c112..c120, c153..c158, c196..c198; L07 and L09 Lab 1 outputs", "PASS",
  "L07: c118 x*=0.739085 and the 31-value bound check; c119 0.840117 < sin 1 = 0.841471; c120 0.999798 and 0.009999 (window [-50,50], 201 points); c117 2.661258/0.05439523 = 48.9. L09: c153 1, 9, 99; c154 1.067e-6 at n=151 and 9.60e-7 at n=152 (recomputed, least n = 152); c155 278 iterations, 9.512e-13, policy 0.25 everywhere; c156 59/103/147 with equal actual and certified errors; c157 126 steps, 0.0000085808; c158 1.7433922005."),
 ("d-cards-L08-c137", "L08 card c137 and the lab's unrounded contraction ratio", "cards.json M5-c137; L08 Lab 1 Part B text; " + S + "l08_r5.py", "PASS",
  f"{S}l08_r5.py with the seed 20261028 and 2000 pairs: largest ratio 0.9000000000000006, minus beta = 5.55e-16 = 5 units in the last place of 0.9 (ulp 1.11e-16); c137 says 'about five units' and 5.6e-16 (rounds 5.55e-16 to 5.6e-16). Also c138 (V=500 at beta=1), c136 (257 iterations, residual 8.695e-13) and c139 (40, 257, 527 iterations at beta 0.5, 0.9, 0.95; recomputed) hold."),
 ("d-cards-semantic", "Every card that changed, checked against the current lesson text", "cards.json (changed cards: c004, c024-c027, c086, c099, c127, c137, c154, c155, c157, c162, c175, c181, c188-c190 and the L02-L10 text edits)", "PASS",
  "Round 4's failing card c175 now states Proposition 4.1's hypotheses (f = 0 below 1/2, f = 1 from 1/2 on [0,1]; G the step integrator at 1/2) and Remark 4.2 (monotonicity does not rescue the integral): PASS. Every changed card was re-read against the current text in this round."),
 ("d-cards-L01-L03-carried", "Cards c001-c049 against L01-L03 (re-verified, not carried)", "cards.json M5-c001..c049; course/modules/M/M5/L01.html, L02.html, L03.html", "PASS",
  "L01, L02, L03 changed since the previous pin, so all 49 cards were re-verified this round: definitions, theorem hypotheses and conclusions, Lab 1 printed values (c010-c012, c032-c034, c047-c049) and misconception cards match the current text. Recomputed: c010 bracket [181/128, 2897/2048], c011 step 11, c012 13 of 13; c033 N=10; c034 1830 pairs."),
 ("d-cards-L04-L10-unchanged", "Cards c050-c200 against L04-L10 text (re-verified from scratch)", "cards.json M5-c050..c200; course/modules/M/M5/L04.html to L10.html", "PASS",
  "Every card of L04-L10 was re-read against its lesson this round (previous UNVERIFIABLE status not carried). Number checks: c066-c068, c082-c084, c098-c100, c136-c139, c170 (exact formulas), c182-c185 (n=1000 values recomputed), c154 (recomputed). Attributions read: M1 Lesson 2 Corollary 2.6 (c013, 'no rational number has square 2'), M2 Lesson 9 Definition 1.3 and Lemma 1.2, M2 Lesson 10 Theorem 2.1, M2 Lesson 11 Lemma 1.1 (c167, c169 via page)."),
 ("d-exemplars-scores", "Exemplar data-scores match the official scoring text", "project.html lines 418-480 (data-scores attributes and the official-scoring lines)", "PASS",
  "Exemplar A data-scores 2,2,1,2,2,2 = 'C1 2 · C2 2 · C3 1 · C4 2 · C5 2 · C6 2'; Exemplar B data-scores 4,4,4,4,4,3 = 'C1 4 · ... C5 4 · C6 3'. The rubric-consistency of those scores is a separate row."),
 ("d-exemplarA-printed-only", "Exemplar A: 'quotes one number that Lab 3 does not print'", "project.html line 416 and Exemplar A lines 424-432", "FAIL",
  "Exemplar A quotes 'about 240' sweeps (not printed; Lab 3 prints 236) and the tolerance 10^{-10} (an input; Lab 3's printed lines never show it). The intro claims exactly one number that Lab 3 does not print, so the intro is inaccurate. Fix: say 'quotes numbers that Lab 3 does not print (240, and the tolerance input)', or remove the count."),
 ("d-exemplarB-printed-only", "Exemplar B quotes only numbers that Lab 3 prints", "project.html line 416, Exemplar B lines 456-466", "PASS",
  "Round 4's 9 and 1.9 are removed. Every number in Exemplar B's text is printed by Lab 3 (236, 242, 1.025e-11, 9.226e-11, 9.226e-12, 0.900000, 200 pairs, 0.9 and 0.3, 0.45 and 2.7) or is a symbol; the tolerance is not quoted."),
 ("d-exemplarB-A4-gap", "Exemplar B A4 derivation steps", "project.html lines 461-462", "PASS", "d_{k+1} <= beta d_k by A1; induction gives d_{n+j} <= beta^j d_n; ||V_n - V*|| <= sum_{j>=1} d_{n+j} by the triangle inequality and the limit (A3); sum beta^j = beta/(1-beta). Each step checked."),
 ("d-exemplarB-scores-consistency", "Exemplar B official scores against the rubric's level-4 descriptors", "project.html lines 452, 459-476 (rubric lines 405-410)", "FAIL",
  "C5 level 4 requires 'the unit, the instance and the tolerance stated' and a named printed line for each number; Exemplar B states no tolerance (no 10^{-10} in lines 450-480) and names only 'Lab 3', so by the rubric it is level 2 at most, not 4 (annotation line 474 says 'with its instance and tolerance'). C1 level 4 names 'the parameters beta, alpha in (0,1)'; Exemplar B states beta in (0,1) only (line 456), so C1 is level 3 by the descriptor. Fix: state the tolerance and alpha in (0,1) in B, or lower the scores to C1 3 and C5 2 (official total changes)."),
 ("d-exemplarB-C6-annotation", "Exemplar B annotation for C6 level 4 quotes text the passage no longer has", "project.html line 476 vs Exemplar B line 466", "FAIL",
  "Annotation 476: 'the passage says only that a finer grid is needed'. Exemplar B's Limitations (line 466) says the grid's spacing is part of the error the bound does not measure, and does not mention a finer grid. Fix: correct the annotation to the current text."),
 ("d-A1-hypotheses", "Proof A1 hypotheses (nonempty feasible sets) and the contraction statement", "project.html line 393 (A1), line 239 (conventions use alpha < 1)", "FAIL",
  "A1 claims 'a grid of positive points whose first point is at most 1, so that every feasible set is nonempty' and lists only beta in (0,1) as the parameter hypothesis. Nonemptiness needs alpha in (0,1): with alpha = 2 and grid (0.4, 1.0) (first point 0.4 <= 1), F(0.4) is empty because 0.4^2 = 0.16 < 0.4, so the operator of A1 is undefined. Fix: add alpha in (0,1) to A1's hypothesis list (the page's C1 already names it)."),
 ("d-conventions-243-245", "Conventions 243 and 245 are inconsistent: a valid bound allowed by 243 fails the count required by 245", "project.html lines 243 and 245; grader/test_project.py test_iterations_within_the_a_priori_count", "FAIL",
  "Line 243 allows 'another [bound] is any bound your proof establishes'; line 245 says 'A correct solver stops within the a priori count plus one'. The Euclidean-norm certificate (valid, see d-grader-alternatives) satisfies 243 and fails 245 on 35 of 50 seeds (witness seed 1 instance 0: 426 > 424). Fix: restrict 245 to the sup-norm certificate of line 243's first form, or restrict 243 to bounds that meet the count."),
 ("d-line53-definition", "Lesson text line 53 defines the certified error the conventions do not state that way", "project.html line 53 vs line 243", "FAIL",
  "Line 53 says 'the certified error after a sweep is beta/(1-beta) times that change; the conventions below state these formally'. Line 243 gives beta/(1-beta)*||V_n - V_{n-1}|| only as 'one valid choice'. Fix: say 'the labs use beta/(1-beta) times that change; the conventions below define the certified error and give this as one valid choice'."),
 ("d-scope-words", "Scope words (only, all, every, any, same, always, drives) in project prose", "project.html: 78 hits by regex (scripted list, prose only)", "FAIL",
  "Traced each hit: 'every state has a feasible saving' (239) and 'every state is updated' (242) are proved or defined; 'the same feasible sets' (154), 'the same loop' (387), 'one pair cannot prove it for every pair' (154) and 'say nothing about any other grid' (387) are sound; 'every feasible set is nonempty' (393) depends on alpha < 1 (d-A1-hypotheses); 'a correct solver stops within...' (245) conflicts with 243 (d-conventions-243-245). 'Exemplar B quotes only numbers Lab 3 prints' (416) holds."),
 ("d-terms-before-definition", "Terms used before definition", "project.html lines 37-57 (lede, rungs), lines 53-57", "PASS",
  "'sup norm', 'operator', 'certified error' are defined in the conventions the lede and Lab 1 point to (lines 44, 53, 237-245); 'contraction' links to L07; 'placement bar' links to index.html#placement. No concept is used before it is defined."),
 ("d-reading-lessons", "Reading line: which lessons the proofs use", "project.html line 500; A1-A4 (lines 391-396); Exemplar B proofs (lines 456-470)", "PASS",
  "A2 uses completeness of R (L01 Definition 1.1), Cauchy sequences (L02) and metric spaces (L04); A3 uses L07 (contraction, Banach) and continuity of a contraction; A4 uses the geometric series of M1 (M1 L06 Theorem 2.2 is the finite geometric sum). No proof uses L05 (uniform convergence) or L06 (compactness); the line now lists 1, 2, 4, 7 and M1. Round 4's failing list is corrected."),
 ("d-browser-grader", "The autograder runs in the browser", "project.html grader panel (line 271); tools/page_smoke.py", "PASS", "outputs/page_smoke.out: 'in-browser grader: All 86 tests pass on seed 973103070'."),
 ("d-banned-phrases", "Banned phrases and vague approximations", "project.html text", "PASS",
  "'about' occurs at line 154 ('about 9.5e-7', backed by the printed Lab 2 value), in Exemplar A (lines 430, 442, 443: deliberately weak example, annotated), and at line 466 ('about m^2 operations per sweep', the double loop of the code). No 'roughly', 'historically', ellipsis, TODO or TBD in the page."),
 ("d-process-words", "No process words in learner text", "project.html text", "PASS", "grep: no 'round', 'builder', 'verifier', 'unit report' or 'REQUESTS' in the page text."),
]
ids = [r[0] for r in rows]
assert len(ids) == len(set(ids))
out_rows = []
for rid, check, loc, status, evidence in rows:
    row = {"id": rid, "check": check, "location": loc, "status": status, "evidence": evidence}
    if status != "PASS":
        row["fix"] = "see evidence; the fix is named in the evidence text"
    out_rows.append(row)

counts = {s: sum(1 for r in out_rows if r["status"] == s) for s in ("PASS", "FAIL", "UNVERIFIABLE")}
killed = sum(1 for m in mutants if m["killed_by"])
verdict = "PASS" if counts["PASS"] == len(out_rows) and killed == len(mutants) else "FAIL"
frag = {
    "unit": "M5",
    "slice": "M5-d",
    "round": 5,
    "verifier": "Claude Haiku 5.5 (independent verifier, M5 slice d, round 5; did not build M5; no shared context with the builders)",
    "pin": "09b8751 (detached, /tmp/verifyB5-M5-d); previous pin 2657ab5 (round 4)",
    "base": "2657ab5 (round-4 pin). Delta: git diff 2657ab5 09b8751 -- course/modules/M/M5 tests/labs/M5 ledgers/M5/mutants",
    "checkout": "/tmp/verifyB5-M5-d",
    "scratch": "/tmp/M5-v/d5",
    "verified_at": "2026-10-28",
    "verdict": verdict,
    "rows": out_rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": "Scripts: ledgers/M5/scripts/M5-d-r5/ (nums_r5.py, l08_r5.py, cards_check.py, suite_on.py, names.sh, monotone_change_r5.py, alt/ alternatives alt5a-alt5f, build_fragment_r5.py; outputs/). Mutants m79-m81 are verifier-written student errors in ledgers/M5/mutants/. The builder's mutant m82 (certificate doubled) was valid and passes the suite on 50 seeds, so it was moved to scripts/alt/alt5f (not a mutant). Not checked: (1) no live sec.gov or Crossref access beyond verify_refs; (2) mypy on the grader folder fails on import of contraction_solver/instance because the grader is outside the repo's mypy target (tools, tests), so it is not a gate; (3) the L07/L08 flattened text truncates passages that contain '<' characters, so card-text checks for L07 misconception items used the raw HTML wording where it was legible; (4) hours pace not judged (architect ruling); (5) the monotone-change property behind m64 is supported numerically only.",
    "summary": {"rows": len(out_rows), "pass": counts["PASS"], "fail": counts["FAIL"], "unverifiable": counts["UNVERIFIABLE"], "mutants": len(mutants), "mutants_killed": killed},
}
Path(ROOT / "ledgers/M5/M5-d.json").write_text(json.dumps(frag, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("rows", len(out_rows), counts, "mutants", len(mutants), "killed", killed, "verdict", verdict)
