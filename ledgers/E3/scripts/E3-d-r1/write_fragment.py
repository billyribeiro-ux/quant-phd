import json, re, pathlib
ROOT = pathlib.Path("/tmp/verifyC1-E3-d")
mut_lines = pathlib.Path("/tmp/e3d-v/d/mutate.out").read_text().splitlines()
mutants = []
for line in mut_lines:
    m = re.match(r"(KILLED|SURVIVED) (\S+): (.*) -> (.*)$", line)
    if not m:
        continue
    status, name, desc, killed = m.groups()
    mutants.append({
        "id": name.removesuffix(".py"),
        "description": desc,
        "killed_by": None if status == "SURVIVED" else killed,
        "origin": "verifier d (round 1)" if name.startswith("v0") else "builder (listed in ledgers/E3/mutants, run unchanged)",
    })

def row(id_, check, location, status, evidence, fix=None):
    r = {"id": id_, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    return r

R = []
# ---- PASS rows ----
R.append(row("E3d-labs-run", "2.5 labs: run_labs --unit E3 and the three project twins under python -I -W error",
  "tests/labs/E3/lab-E3-project-1.py, -2.py, -3.py; course/modules/E/E3/project.html lines 55-139, 141-188, 267-463",
  "PASS", "tools/run_labs.py --unit E3 printed 'run_labs E3: PASS (11/11)'. Each twin run directly: exit 0, no stderr; outputs in ledgers/E3/scripts/E3-d-r1/logs/lessonlabs.out and /tmp/e3d-v/d/lab-project-*.out, all equal to the page's expected blocks."))
R.append(row("E3d-lab1-numbers", "2.2 numbers in prose: Lab 1 hypothesis and interpretation recomputed",
  "course/modules/E/E3/project.html lines 57 and 138",
  "PASS", "Printed lines reproduced: CRRA 496/500 (pair 1), prospect -30/500, P(A)=0.480149, log -0.733658, total -2.302315. Pair 2: sure 3000 cents, prospect CE of B -762 cents (=lottery 4000 w.p. 1/4, -2000 w.p. 3/4). Hand check of pair-1 prospect CE for A: V=0.5(2000^0.6)-0.5*2*1000^0.6 = -15.3 CU-power units, c=-(V/-2)^(1/0.6) = -29.8, rounds to -30."))
R.append(row("E3d-lab2-numbers", "2.5 labs and numbers: Lab 2 completed lines and the sigmoid identity",
  "course/modules/E/E3/project.html lines 143, 183-186",
  "PASS", "Recomputed z = 2*(1500-2200)/10000 = -0.14; log(1/(1+exp(0.14))) = -0.765595182; log(1/(1+exp(-0.14))) = -0.625595182; P(A)=0.465057055 and P(B)=0.534942945 sum to 1. Matches run_labs and the page block."))
R.append(row("E3d-lab3-reproduced", "2.2 numbers: Lab 3 estimates and standard errors re-derived with the reference estimator on the twelve answers",
  "course/modules/E/E3/project.html lines 269-463; tests/labs/E3/lab-E3-project-3.py",
  "PASS", "Ran grader/reference.py estimate() (copied as elicit.py, /tmp/e3d-v/d/ref) on the 12 ANSWERS read from the lab twin: gamma_hat 0.635210, lambda_hat 6.150316, kappa_hat 2.020107, se_gamma 0.318970 (prints 0.32), se_lambda 9.593871 (9.59), se_kappa 1.863777 (1.86), log-likelihood -7.144517 (-7.1445). Caveat: the reference shares the lab's formulas, so this confirms the printed numbers, not the formulas; the formulas themselves were checked against the page's Conventions (rows E3d-conventions-formulas)."))
R.append(row("E3d-lab3-mixed-count", "2.2 numbers: 'eleven of the twelve pairs contain a mixed-sign lottery'",
  "course/modules/E/E3/project.html lines 269, 557-558 (exemplar B)",
  "PASS", "Recomputed by hand from the 12 ANSWERS: pair 4 is the only pair with no gain in either lottery (A: -10700,-5600,-7300; B: -13800,-9700), so 11 of 12 are mixed. Lab 3 prints 'mixed-sign answers: 11'."))
R.append(row("E3d-exemplar-B-numbers", "2.2 numbers: exemplar B instrument figures",
  "course/modules/E/E3/project.html lines 557 and 580",
  "PASS", "Prize range over the 12 answers: minimum -18700 (pair 10, B), maximum 19000 (pair 1, A): matches '-18 700 and 19 000'. Pair 0 (6200 w.p. 9/10, -15100 w.p. 1/10) and pair 3 (18800 w.p. 3/4, -12500 w.p. 1/4 against 16500 w.p. 2/5, -17700 w.p. 3/5) match the ANSWERS and both mix a gain and a loss. Standard errors 0.32, 9.59, 1.86 and log-likelihood -7.1445 match Lab 3."))
R.append(row("E3d-grader-count", "2.7/2.9 structure: '26 checks' on the page equals the real collect-only count",
  "course/modules/E/E3/project.html line 203; course/modules/E/E3/grader/test_project.py",
  "PASS", "cd to /tmp/e3d-v/d/ref; QF_SEED=0 python -I -m pytest --collect-only -q test_project.py -> '26 tests collected'. grep -c '^def test_' test_project.py = 26."))
R.append(row("E3d-grader-reference", "2.6 grader: reference passes the suite on seeds 0-49 under the browser flags",
  "course/modules/E/E3/grader/reference.py; test_project.py; instance.py",
  "PASS", "tools/run_graders.py --unit E3 --seeds 0-49 -> 'run_graders E3: PASS (reference 50/50 seeds, slowest 0.9 s)'. Log: ledgers/E3/scripts/E3-d-r1/logs/run_graders.out. Starter fails (run_graders checks it); mypy --strict clean on reference.py, instance.py, starter.py ('Success: no issues found in 3 source files')."))
R.append(row("E3d-grader-alt-correct", "2.6 grader over-constraint: three genuinely different correct implementations pass 50 seeds",
  "ledgers/E3/scripts/E3-d-r1/alt1_bisection_prospect_inverse.py; alt2_compass_search_optimiser.py; alt3_decimal_half_up.py",
  "PASS", "Built from reference.py by scripts make_variants.py and run_variants.sh. alt1: prospect certainty equivalent by 300-step bisection of the value function instead of the closed form; alt2: global grid then a 26-direction compass search instead of Newton; alt3: half-cent rounding by Decimal ROUND_FLOOR of repr(y)+0.5. Each: failing seeds 0 of 50."))
R.append(row("E3d-grader-mutants-listed", "2.6 mutation: every mutant in ledgers/E3/mutants run by tools/mutate_graders.py --unit E3 --seeds 0-9",
  "ledgers/E3/mutants/*.py",
  "FAIL", "15 mutants in total: builder m01-m10 killed 10/10; verifier v02-v05 killed 4/4 (see rows in 'mutants'). Only v01 survives: see E3d-fail-se-untested. Full output: ledgers/E3/scripts/E3-d-r1/logs/mutate.out.",
  "Fix the survivor: see E3d-fail-se-untested (add an SE oracle test)."))
R.append(row("E3d-cards-numbers", "2.7 cards: every card number recomputed or matched to a printed lab line",
  "course/modules/E/E3/cards.json (158 cards; numeric cards E3-c014, c016, c026, c029, c032-c035, c040-c041, c047, c050, c053-c055, c067-c068, c075-c076, c093-c096, c106-c108, c111, c116, c121-c123, c125-c127, c132, c144, c149-c153, c156)",
  "PASS", "Every numeric card was recomputed in Python from unrounded values, e.g. omega(3/10)=0.2857908849 (card 0.28579088), omega(3/5)=0.3912507700, omega(1/2)=0.3535533906; 2*omega(3/10)=0.5715817698 (card 0.57158177); omega(3/10)/omega(3/5)=0.7304544982 (card 0.73045450); weighted value for 100 w.p. 0.01 and 50 w.p. 0.99 at alpha=1 = 49.83277 (card 49.8328); CRRA CE at gamma=4 = 7337.6161; 0.565835/5.065835 = 11.17% and /4.5 = 12.57%; maxmin CE 99523.8095; prospect CE of the Section-4 gamble -1.072330 CU = 99892.7670 cents. Epstein-Zin tree (CE1 8/5, V0 80/49, U -49/80) and CE1 at gamma 0.5/2/3 (2.25, 1.6, 1.372) recomputed by hand. Every lab-derived card matches the output in logs/lessonlabs.out."))
R.append(row("E3d-cards-lesson-claims", "2.7 cards: card claims checked against lesson text and lab code",
  "course/modules/E/E3/cards.json; L01-L08.html",
  "PASS", "Spot-checked and recomputed: L04 Example 2.5 integrated CDFs (X: 500, 1000, 2000; Y: 250, 500, 1250, 2000) and FOSD ranks of Example 1.7 match; L07 Example 2.1 threshold 1/(1+2^-alpha) (2/3 and 0.5858) and identity-weighting values 45 and 60 match; L05 Epstein-Zin identities (psi=1/gamma) match; L07 Part D family is 5 powers + 5 indicators as in the lab code; L08 Example 2.5 known-urn CEs (103125, 106451.6129) match the lab. Lessons are not in this slice beyond the cards; these are the card-side reads only."))
R.append(row("E3d-cards-duplicates", "2.7 cards: full duplicate scan",
  "course/modules/E/E3/cards.json",
  "PASS", "158 cards; ids unique (0 duplicate ids), fronts unique (0), backs unique (0); every card has id, lesson, front, back; grade/cite/basis present where a graded result is stated (cards c016, c032-c035, c054, c073, c075-c076, c094-c096, c097, c115-c117, c122, c127-c128, c134, c153, c156-c158)."))
R.append(row("E3d-cards-cross-refs", "2.7 cards: parenthetical 'Definition/Proposition/Remark/Example/Problem/Lemma/Theorem' references exist in the cited lesson",
  "course/modules/E/E3/cards.json",
  "PASS", "Mechanical scan (inline Python regex, not saved; re-run it over cards.json and the cited lesson text) found 20 references not in their own lesson; 18 are 'Misconception n' (unnumbered in the lessons, see fail row) and 2 are 'Problem E2' (see fail row). Other references (e.g. 'Theorem 1.5 of Lesson 4' in c129, 'Section 4' in c004, 'Model 1' etc.) all present."))
R.append(row("E3d-conventions-formulas", "2.4 mathematics: the specification's formulas and conventions re-derived against the reference and the oracle",
  "course/modules/E/E3/project.html lines 210-213; grader/reference.py lines 71-128",
  "PASS", "CRRA CE: (sum p w^(1-g))^(1/(1-g)) - W equals the EU sure amount for u=W^(1-g)/(1-g) (the 1/(1-g) factor cancels). Prospect CE for V<0: c=-(-V/lambda)^(1/(1-gamma)), re-derived by v(c)=V. Half-cent rule floor(c+1/2) matches 2.5->3 and -0.5->0. Logit scale z=kappa*dCE/10000 (units of $100). Delta method: d gamma/dc = gamma(1-gamma), d lambda/d log lambda = lambda; reference SEs use exactly this. Reference passes 50/50 seeds."))
R.append(row("E3d-dag-concepts", "2.9 DAG: concepts linked on the project page are inside the prerequisite closure and defined earlier",
  "course/modules/E/E3/project.html lines 53 (loss-aversion, certainty-equivalent), 210 (prospect-theory)",
  "PASS", "check_dag --unit E3 PASS; check_pages --unit E3 PASS (link targets L06.html#def-loss-aversion, L02.html#def-certainty-equivalent, L06.html#def-prospect-theory exist). Epstein-Zin and maxmin appear in prose only (plan Architect rule), in the Reading section."))
R.append(row("E3d-tools-gates", "2.3 gates: check_projects, check_pages, check_dag, page_smoke, ruff for the slice",
  "course/modules/E/E3/project.html; grader/*; tests/labs/E3/lab-E3-project-*.py",
  "PASS", "check_projects --unit E3: PASS; check_pages --unit E3: PASS; check_dag --unit E3: PASS; page_smoke --unit E3: PASS (project.html in-browser grader 'All 26 tests pass on seed 170700745'; 360 px and dark theme included); ruff check and ruff format --check on grader and labs: all passed, 15 files formatted."))
R.append(row("E3d-references", "2.1 citations: E3 keys, live and offline",
  "references/references.json; course/modules/E/E3/project.html lines 630-637",
  "PASS", "tools/verify_refs.py --unit E3 (live): 5 of 560 entries, 0 problems. tools/verify_refs.py --offline: 560 entries, 0 problems. The five keys (pratt1964risk, kahneman1979prospect, epstein1989substitution, ellsberg1961risk, gilboa1989maxmin) exist with registry titles; the page attributes no passage to them. Titles read in the registry: e.g. Ellsberg 1961 'Risk, Ambiguity, and the Savage Axioms'; cards c157 'contains the word ambiguity' matches."))
R.append(row("E3d-grades", "2.3 grades: the project's graded claims (exemplar scoring, Lab results)",
  "course/modules/E/E3/project.html lines 496-611",
  "PASS", "Official scoring lines (exemplar A 2,2,1,2,2; exemplar B 3,4,4,3,4) match data-scores attributes. Annotation levels consistent with the rubric descriptors on lines 486-491 except the flagged rows. Grade for lab-printed numbers is covered by fail row E3d-fail-exemplar-B-grade."))
R.append(row("E3d-hours", "2.9 hours: budget components sum to the declared project hours",
  "course/modules/E/E3/project.html lines 238-244 and data-hours-project=14 (line 33)",
  "PASS", "1 + 1 + 3 + 4 + 3 + 2 = 14, equal to data-hours-project=14 and the plan's 14 h project share. No pace judgement made (architect ruling)."))
R.append(row("E3d-signatures", "2.4 contract: starter signatures and the three named functions match the specification",
  "course/modules/E/E3/grader/starter.py; project.html lines 197-199",
  "PASS", "starter.py defines certainty_equivalent_cents(model, prizes_cents, probabilities, params, wealth_cents) -> int, log_likelihood(responses, params) -> float and estimate(responses) -> dict[str, float], as the page lists them."))
# ---- FAIL rows ----
R.append(row("E3d-fail-se-untested", "2.6 grader: the page's claim that the checks compare standard errors with an oracle",
  "course/modules/E/E3/project.html line 203; course/modules/E/E3/grader/test_project.py lines 431-434",
  "FAIL", "project.html line 203: 'The checks compare the engine with oracles ... the score, the local maximum and the standard errors of the estimate.' test_project.py has no oracle test for se_gamma, se_lambda or se_kappa: test_standard_errors_are_positive_and_finite (lines 431-434) only checks positive and finite. Mutant ledgers/E3/mutants/v01_se_without_delta_method.py (se_gamma without the factor gamma(1-gamma)) SURVIVED seeds 0-9 (mutate.out). Reference SE_gamma = 0.3190; the mutant gives about 1.4 at the same estimate, with no test noticing.",
  "Add an oracle test: recompute the delta-method SEs from the observed information (tolerance stated, e.g. 1e-3 relative) and compare each se_* with it; or delete 'and the standard errors' from line 203."))
R.append(row("E3d-fail-unchosen-term", "2.4 mathematics: the likelihood is described as having a term for the unchosen alternative",
  "course/modules/E/E3/project.html lines 187, 471, 487, 521; course/modules/E/E3/grader/test_project.py lines 109-110, 385-386, 408; course/modules/E/E3/grader/reference.py lines 167-168",
  "FAIL", "project.html 187 (Lab 2 interpretation): log(1-P(A)) 'is the contribution of the unchosen alternative when B is chosen'. Under the page's own Conventions (line 212) the term is log(1-P(A)) for each response that chose B, i.e. the chosen alternative's probability; A is the unchosen one and contributes nothing. The same error is in project.html 471 ('its two terms'), 487 (rubric C2 level 3: 'its term for the chosen alternative and its term for the unchosen one'), 521 (exemplar A annotation), test_project.py 385-386 and 408 and in reference.py 167-168. A logit likelihood has one term per response, log P(chosen); the two branches are cases of that term.",
  "State that each response contributes log P(chosen): log P(A) when A is chosen and log(1-P(A)) when B is chosen. Replace 'unchosen' wording in lines 187, 471, 487, 521, test_project.py 385-386 and 408, and reference.py 167-168."))
R.append(row("E3d-fail-lab3-maximum", "2.2 claims about what the lab shows: 'a maximum' and 'the standard errors say how far they could be'",
  "course/modules/E/E3/project.html lines 269 ('so the search has stopped at a maximum'), 464 ('The lab shows that the estimate is a maximum of this questionnaire'; 'the standard errors say how far they could be')",
  "FAIL", "Lab 3 (tests/labs/E3/lab-E3-project-3.py, main()) prints only the largest score component, which is 3.55e-10: a stationary point. It computes no Hessian sign and no global check. Score zero does not establish a maximum (a saddle or a minimum also has zero score); the local-maximum property is checked only by test_project.py test_estimate_is_a_local_maximum, not by Lab 3. 'The standard errors say how far they could be' is not a bound: they are asymptotic scales, and the page's own limitation (line 591 exemplar B) treats them as rough at n=12.",
  "Say 'a stationary point (largest score component below 1e-6)'; drop 'a maximum' from lines 269 and 464, or print the Hessian's eigenvalues in Lab 3. Replace the 'how far they could be' sentence with what an SE is (one standard deviation of the asymptotic approximation)."))
R.append(row("E3d-fail-lab3-provenance", "2.9 honest data: provenance of the twelve Lab 3 answers",
  "course/modules/E/E3/project.html line 269; tests/labs/E3/lab-E3-project-3.py docstring lines 271-274",
  "FAIL", "Both say the answers were 'generated for this page from a stated participant (curvature 0.35, loss aversion 2.20, precision 1.20) with a fixed seed'. No seed is named; no generator for the 12 answers is in the repository. grader/instance.py make_instance draws 200 pairs and random parameters; for seeds 0-399 it never returns gamma 0.35, lambda 2.2, kappa 1.2 (scan in logs). So the claim cannot be re-generated.",
  "Name the generator script and seed, commit it under tests/labs or tools, or state that the twelve answers are hand-written SIMULATED data."))
R.append(row("E3d-fail-instance-docstring", "2.2 docstrings vs code: the logit scale in grader files",
  "course/modules/E/E3/grader/instance.py line 14; course/modules/E/E3/grader/reference.py line 167",
  "FAIL", "instance.py line 14 states P(A) = 1/(1+exp(-kappa(CE_A-CE_B)/100)); the code (line 125 and _CENTS_PER_UNIT = 10000, line 48) and the page (line 212) use /10000. reference.py line 167 gives z = kappa (CE_A - CE_B) without the /10000 scale that line 20 and the code use.",
  "Change instance.py line 14 to /10000 (units of $100), and add the scale to reference.py line 167."))
R.append(row("E3d-fail-notation-c", "2.5 notation: the letter c has two meanings on the project page",
  "course/modules/E/E3/project.html lines 210 (c = sure change with v(c)=V) and 213 (c = log(gamma/(1-gamma))); test_project.py line 446",
  "FAIL", "project.html line 210 uses c for the sure change; line 213 uses c for the log-odds coordinate of gamma. The same page has no registry symbol for either (notation/notation.json registers only T, Phi, gamma_3, gamma_4, R*, R^e*, R_f, Q). A reader substituting one meaning for the other gets the wrong formula.",
  "Rename the log-odds coordinate (for example eta = log(gamma/(1-gamma))) on lines 213 and 279-280 and in test_project.py line 446 and lab-E3-project-3.py line 280."))
R.append(row("E3d-fail-exemplar-B-grade", "2.3 grades: exemplar B grades lab-printed results T",
  "course/modules/E/E3/project.html line 603",
  "FAIL", "Exemplar B: 'Every number above is printed by Lab 3 ... and each is graded T as a computed result.' Ruling (e): results read off a SIMULATED lab are grade C with a basis naming the lab; T is for results proved on the page. Lab 3 uses SIMULATED answers (line 269).",
  "Grade these results C with basis 'Lab 3 (SIMULATED)'; keep T only for the derivations on the page."))
R.append(row("E3d-fail-unenforced-claims", "2.6 grader: requirements the page states that the suite does not enforce",
  "course/modules/E/E3/project.html line 201 ('No function prints or warns'; 'Standard library only; no network'; 'Every named invalid input raises ... with its message'), line 223 (table: 'the message names the two allowed names')",
  "FAIL", "No test checks printing or imports: grep of test_project.py for print, socket, urllib, requests finds no print call and no network import (only the word 'prints' in its docstring, line 11); the imports are elicit, pytest and instance. test_model_name_must_be_crra_or_prospect (test_project.py line 292) checks only the substring 'crra', not 'prospect' that the table requires. Ruling (a): a requirement the tests do not enforce must not be claimed as checked.",
  "Either enforce (capture stdout in a test; check both names in the model message) or reword: 'the suite checks the exception type, and for the model name that the message contains crra'."))
R.append(row("E3d-fail-message-overconstraint", "2.6 grader over-constraint: tests require message substrings the page does not state",
  "course/modules/E/E3/grader/test_project.py lines 514 (contains='identify'), 538 and 557 (contains='mixed-sign'); project.html line 226",
  "FAIL", "Page line 226 says the message names 'the condition, for example \"need mixed-sign lotteries to identify loss aversion\"'. Witness: /tmp/e3d-v/d/alt/alt4_messages_without_keywords.py (copy of reference with messages 'no answers given' and 'no lottery pays both a gain and a loss'): FAILED test_estimate_needs_responses on seeds 0-2 (ledgers/E3/scripts/E3-d-r1/run_variants.sh output). A correct engine that names the condition in other words fails.",
  "Test only the exception type for these conditions, or state the required words on the page (ruling (b)); the page's own table asks for 'the condition'."))
R.append(row("E3d-fail-recovery-criterion", "2.6 grader: recovery-within-five-SE assertion and its docstring reference",
  "course/modules/E/E3/grader/test_project.py lines 482-494 (test_estimate_recovers_the_true_parameters_within_five_standard_errors), docstring lines 483-485",
  "FAIL", "The test requires |estimate - true| <= 5 SE for each parameter. Neither the page's specification (project.html lines 195-203) nor the conventions (210-214) state a recovery criterion, so ruling (b) is not met. Its docstring says 'see the report's limitations': project.html has no statement on Wald calibration in the tail, so the cross-reference is empty.",
  "State the recovery criterion (and why 5 SE) in project.html Constraints, or drop the test; remove the reference to 'the report's limitations' or add the limitation to the page."))
R.append(row("E3d-fail-exemplar-B-causal", "2.4 causal and directional claims in exemplar B",
  "course/modules/E/E3/project.html lines 569 (identification claims), 591 ('A noisy choice confounds curvature with precision ... so a poor design would raise the standard error of curvature')",
  "FAIL", "No computation, lab or test in the slice supports 'precision is identified by the spread of the differences in certainty equivalent, and curvature by the pure and mixed pairs together', or the direction 'a poor design would raise the standard error of curvature'. Ruling and BUILDER_RULES call for causal and directional claims to be computed or flagged as untested.",
  "Support each claim with a printed computation (e.g. Fisher information by pair group) or mark it as a hypothesis for the learner to test."))
R.append(row("E3d-fail-cards-dangling-problem", "2.7 cards: cited 'Problem E2' is not in the lesson the card comes from",
  "course/modules/E/E3/cards.json E3-c034 (lesson L02) and E3-c055 (lesson L03)",
  "FAIL", "L02.html and L03.html contain no 'Problem E2' (L02 has Problems M1-M3, R1, R2; L03 has P3, R3). 'Problem E2' appears only in L06.html line 506 (about sqrt(5/3)) and L05/L06 exercise lists. The card claims are numerically right (verified), but the source named is wrong.",
  "Cite the problem that exists in the card's own lesson, or add the problem to that lesson."))
R.append(row("E3d-fail-cards-misconception-numbers", "2.7 cards: 'Misconception n' references do not match any numbering in the lessons",
  "course/modules/E/E3/cards.json E3-c029, c031, c051, c053, c072, c090, c092, c112-c114, c130-c132, c154-c156",
  "FAIL", "Each lesson's 'Misconceptions' block (e.g. L02.html id=misconceptions) is an unnumbered list; no lesson contains the text 'Misconception 1', 'Misconception 2' or 'Misconception 3' (only L01.html contains 'Misconception 1' in one place). The cards' ordinals must be guessed from list position, so they are not checkable against the lesson as BUILDER_RULES section 7 requires.",
  "Number the misconceptions in each lesson (for example '(Misconception 2)' in the heading), or cite them by their opening words."))
R.append(row("E3d-fail-exemplar-A-rounding", "2.9 numbers: exemplar A quotes parameters to two decimals against the page's four-decimal rule",
  "course/modules/E/E3/project.html line 516 (exemplar A) and line 477 (rule)",
  "FAIL", "Line 477: 'Quote each parameter to four decimals'. Exemplar A line 516 gives 0.64, 6.15 and 2.02 (correct roundings of 0.6352, 6.1503, 2.0201). The annotations (lines 516-523) do not mention the rule, so the exemplar teaches the violation without a note.",
  "Quote 0.6352, 6.1503 and 2.0201 in exemplar A, or annotate the rounding as a rubric miss."))
R.append(row("E3d-reference-deployment", "2.9 claim: reference.py is excluded from deployment",
  "course/modules/E/E3/grader/reference.py line 3; BLUEPRINT.md lines 400-401",
  "UNVERIFIABLE", "BLUEPRINT.md lines 400-401 state the rule ('excludes every grader/reference.py'). The publish step was not run in this checkout, and course/ is served as a static tree (reference.py sits under course/), so the exclusion could not be confirmed here."))
R.append(row("E3d-mutants-new", "2.6 mutation: the verifier's three or more new student-error mutants written and run",
  "ledgers/E3/mutants/v01-v05",
  "PASS", "Five verifier mutants written (v01 SE without delta, v02 prospect inverse forgets lambda, v03 wealth check off by one, v04 CRRA float output, v05 logit scale per dollar). Four killed; v01 is the survivor recorded in E3d-fail-se-untested."))

fragment = {
  "unit": "E3",
  "slice": "E3-d (project.html, grader/*, project labs lab-E3-project-1..3, cards.json; project slice with mutants)",
  "round": 1,
  "verifier": "Claude Haiku 5.5 (independent verifier, unit E3 slice d, round 1; did not build E3)",
  "pin": "55b5634 (detached checkout /tmp/verifyC1-E3-d; the brief text names b4590f6, the task text names 55b5634: the checkout pin 55b5634 was used)",
  "base": "none",
  "checkout": "/tmp/verifyC1-E3-d",
  "scratch": "/tmp/e3d-v/d",
  "verified_at": "2026-10-28T00:00:00+00:00",
  "verdict": None,
  "rows": R,
  "mutants": mutants,
  "registry_flags": [],
  "freshness_flags": [],
  "notes": ("Round 1. Command rows run on Python 3.14 in the checkout's .venv. Mutants: builder m01-m10 (run unchanged) and verifier v01-v05 (scratch generator make_variants.py). Alternatives: alt1-alt3 pass 50/50; alt4 (wording witness) fails. Not checked: live fetch and publish steps; the SEC source (not in this slice); the lesson pages L01-L08 themselves beyond the card-side reads (other verifiers' slices); exemplar scores were not re-scored blind (the self-assessment form is JavaScript-only)."),
  "summary": None,
}
passes = sum(1 for r in R if r["status"] == "PASS")
fails = sum(1 for r in R if r["status"] == "FAIL")
unv = sum(1 for r in R if r["status"] == "UNVERIFIABLE")
fragment["verdict"] = "PASS" if fails == 0 and unv == 0 and all(m["killed_by"] for m in mutants) else "FAIL"
fragment["summary"] = {"rows": len(R), "pass": passes, "fail": fails, "unverifiable": unv,
                       "mutants": len(mutants), "mutants_killed": sum(1 for m in mutants if m["killed_by"])}
out = ROOT / "ledgers/E3/E3-d.json"
out.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(json.dumps(fragment["summary"]), fragment["verdict"])
