import json
P = "PASS"; F = "FAIL"; U = "UNVERIFIABLE"
S = "ledgers/M2/scripts/M2-e-r1/"
rows = []
def row(id_, check, location, status, evidence, fix=None):
    r = {"id": id_, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != P:
        r["fix"] = fix or ""
    rows.append(r)

# ---- project.html: labs and spec ----
row("m2e-lab1-numbers", "2.5-labs", "course/modules/M/M2/project.html lines 57-76 (Lab 1 hypothesis, twin tests/labs/M2/lab-M2-project-1.py)", P,
    "Re-derived with exact Fractions (" + S + "recompute_lab_bond.py): price 1081108.9577935503, dP/dy -8514667.395285616, d2P/dy2 83766485.11919491, duration 7.875864. Every 'stated before running' figure matches (1081108.96, -8514667.40, 83766485.12, 7.88). Relative agreements 1.8e-9 and 1.0e-7 match the stated 2e-9 and 1e-7. Twin run under python -I -W error prints the same lines as the page expected block.")
row("m2e-lab2-completion", "2.5-labs", "course/modules/M/M2/project.html Lab 2 (lines ~96-140), tests/labs/M2/lab-M2-project-2.py", P,
    "run_labs --unit M2: PASS (27/27 including lab-M2-project-2). Completed blanks: Dual.__mul__ dot = a*b.dot + a.dot*b; second_difference = (f(x+h)-2f(x)+f(x-h))/h**2. Analytic checks recomputed by hand: f''=6+3x0=8.4, f'=-2+6x0+1.5x0^2=3.76 at x0=0.8. Printed differences 5.11e-08 and 4.44e-16 match the page's 'better than 1e-7' and '1e-15' claims. Interpretation that the central second difference of a cubic is exact up to round-off is consistent with the printed 5.11e-08 (round-off ~ eps*f/h^2 ~ 7e-8).")
row("m2e-lab3-numbers", "2.5-labs", "course/modules/M/M2/project.html Lab 3 (lines ~268-300), tests/labs/M2/lab-M2-project-3.py", P,
    "Twin output (python -I -W error) equals the page expected block. Recomputed: exact dP/dy = -23407826.805475 (Fraction); unrounded price 2721581.2909; central minimum 7.111207e-04 at 1e-6; observed orders log10(1.249698e6/1.297200e5)=0.984 and log10(5.485760e4/5.480170e2)=2.000; kink forward +1, backward -1, central 0; cancellation errors 5.32e-05, 1.33e-01, 8.78e-01. All hypothesis figures in the Lab 3 paragraph match. Interpretation 'Below that step the central error is larger than that minimum at every printed step' checked against the table.")
row("m2e-lab3-report-lines", "2.6-spec", "course/modules/M/M2/project.html Rung 3 Required outputs (line ~206-212) and Lab 3 hypothesis ('It must print the same lines')", F,
    "Lab 3 prints 'unrounded price (cents)' and a 'backward' kink line. The module interface cannot produce either: bond_price_cents returns only the rounded int (no unrounded price function among the five required functions), and the Conventions (line ~226, ValueError (b)) plus test_project.py test_unknown_scheme_raises_value_error[backward] require fd_derivative to REJECT scheme 'backward'. So 'replace its calls to the price and the difference functions with calls to your module ... It must print the same lines' cannot be met as written.",
    "State which lines the report computes from its own cash-flow code (unrounded price) and how the backward quotient is formed (fd_derivative(f, x-h, h, 'forward')), or add an unrounded-price accessor to the interface and say so in Required outputs.")
row("m2e-one-bond-claim", "2.6-spec", "course/modules/M/M2/project.html line 53", F,
    "Text: 'Lab 1 and Lab 3 use one SIMULATED bond: a face value of 1000000 cents ... in Lab 1 and of 2500000 cents ... in Lab 3'. Lab 1 is 1000000 cents, 5.00 % coupon, 10 years, yield 4.00 %; Lab 3 is 2500000 cents, 6.00 % coupon, 12 years, yield 5.00 % (line 270 and Lab 1 hypothesis). Two different bonds are used.",
    "Replace 'one SIMULATED bond' with 'two SIMULATED bonds'.")
row("m2e-hess-tolerance-wording", "2.6-spec", "course/modules/M/M2/project.html Conventions 'Tolerances' (line 226)", F,
    "Spec: symmetry passes when the difference of the off-diagonal entries is at most 1e-6 against 'one plus the larger of them'. Read literally with signed values, a symmetric Hessian whose off-diagonal entries are -3 has tolerance 1 + (-3) = -2 and cannot pass. test_project.py test_hessian_is_symmetric uses scale = 1.0 + max(abs(got[0][1]), abs(got[1][0])), which the page does not state.",
    "Write 'one plus the larger of their absolute values'.")
row("m2e-rubric-c1-vague-level4", "2.6-spec (rubric rule 1)", "course/modules/M/M2/project.html rubric table row C1, level 4 cell (line 400)", F,
    "Level 4 requires 'names the step at which the sweep turns'. 'The step at which the sweep turns' is not defined anywhere on the page; level 3 names 'the step of smallest central error'. VERIFIER_RULES 2.6 rubric 1: every level descriptor must be observable.",
    "Replace with 'names the step of smallest central error and the step where the floating-point error overtakes the truncation error', or define the turning point.")
row("m2e-exemplar-b-C3-calibration", "2.6-rubric calibration", "course/modules/M/M2/project.html exemplar B (line 464 data-scores '4,4,4,3,4'; line 498 annotation 'Meets C3 level 4') vs rubric C3 level 3 (line 400)", F,
    "Blind scoring from the rubric: C3 level 3 requires, for each instance, the analytic, finite-difference AND automatic-differentiation value with tolerance and outcome. Exemplar B contains no automatic-differentiation value (grep for automatic/AD/dual/forward-mode in the exemplar B block: 0 hits). Blind C3 = 2 (level 2: analytic and FD reported, no AD value). Official 4 differs by 2 levels; VERIFIER_RULES 2.6 requires within one level.",
    "Either add the AD value of the first derivative (with the tolerance outcome) to exemplar B's C3 passage, or change exemplar B's C3 official score and annotation to level 2.")
row("m2e-exemplar-a-C3-annotation", "2.6-rubric calibration", "course/modules/M/M2/project.html line 458, exemplar A annotation 'Meets C3 level 2: reports the analytic and the finite-difference values'", F,
    "The exemplar A passage 'Agreement' says only 'The analytic derivative is compared with the central difference, and they agree.' No finite-difference value is printed anywhere in exemplar A (the only derivative value is the analytic -23407827). The annotation credits an element the text does not contain.",
    "Remove the claim that the FD value is reported, or print the FD value in the passage.")
row("m2e-richardson-claim", "2.6-spec / autograder mutation", "course/modules/M/M2/project.html 'What the suite does not check' (line 230) vs test_project.py test_central_error_is_of_order_h_squared", F,
    "Page claims: 'An implementation may use a Richardson extrapolation ... and the same suite accepts each of them.' Witness " + S + "alts/alt1/sensitivity_engine.py implements fd_derivative(scheme='central') as Richardson of the central quotient at h and h/2. run: QF_SEED=s pytest -q -W error test_project.py, s=0..49: 50/50 runs give '2 failed, 44 passed', both failures test_central_error_is_of_order_h_squared[inst0] and [inst1] (error ratio is about 16, not 4). The page also defines the central estimate as (f(x+h)-f(x-h))/(2h) (line 222), so the Richardson variant is also not the stated quotient. The claim and the test contradict each other.",
    "Delete Richardson from the list, or move the order test to the plain central quotient and state that fd_derivative(scheme='central') is the plain quotient while Richardson may be used elsewhere.")
row("m2e-forward-value-untested", "2.6-autograder (spec enforcement)", "course/modules/M/M2/project.html line 222 (forward estimate definition) and grader/test_project.py test_forward_error_is_of_order_h / test_forward_and_central_schemes_are_accepted", F,
    "The page defines the forward estimate as (f(x+h)-f(x))/h. No test checks its value: the only forward test compares the RATIO of errors at h=1e-2 and 5e-3 (1.9..2.1), which a backward difference or a (f(x+2h)-f(x))/(2h) quotient also satisfies. Mutants " + S.replace("scripts/M2-e-r1/","") + "mutants/m11_forward_estimate_is_the_backward_difference.py and m12_forward_uses_double_step_over_double_step.py both SURVIVE tools/mutate_graders.py --unit M2 --seeds 0-9 (verified by running it: 14/16 killed).",
    "Add a test that fd_derivative(f, x, h, 'forward') equals (f(x+h)-f(x))/h to a stated tolerance at a step where round-off is negligible (e.g. comparing with the analytic f'(x)+h f''(x)/2 + h^2 f'''/6 of the cubic).")
row("m2e-mutants-existing-suite", "2.6-mutation (existing builder mutants)", "ledgers/M2/mutants/m01..m10 (grader/test_project.py)", P,
    "tools/mutate_graders.py --unit M2 --seeds 0-9: m01..m10 each KILLED (e.g. m01 by test_central_difference_matches_the_analytic_derivative, m05 by test_price_is_the_half_even_rounding_of_the_exact_price, m10 by test_unknown_scheme_raises_value_error[backward]).")
row("m2e-mutants-own-killed", "2.6-mutation (verifier's own mutants)", "ledgers/M2/mutants/m13..m16", P,
    "Written by this verifier. m13 (Hessian takes abs of a negative step) KILLED by test_hessian_zero_or_negative_step_raises_value_error; m14 (scheme name case-folded) KILLED by test_unknown_scheme_raises_value_error[Central]; m15 (duration divides by round(price)) KILLED by test_named_ratios_are_the_stated_formulas[inst0]; m16 (final year drops coupon) KILLED by test_price_is_the_half_even_rounding_of_the_exact_price[inst0]. Seed 0 used for all.")
row("m2e-mutants-own-survivors", "2.6-mutation", "ledgers/M2/mutants/m11, m12", F,
    "Two plausible student errors survive (see m2e-forward-value-untested). Total: 14/16 killed; the mutation test fails.",
    "Add the forward-value test described in m2e-forward-value-untested; re-run tools/mutate_graders.py --unit M2 --seeds 0-9 to 16/16.")
row("m2e-alt-impls-pass", "2.6-autograder (over-constraint, alternatives)", "grader/test_project.py vs alts alt2 (complex-step ad_derivative), alt3 (reverse-mode tape), alt4 (exact Fraction price and loop closed-form sums), alt5 (NumPy)", P,
    S + "run_alts.sh: each of alt2, alt3, alt4, alt5 passes 46/46 on seeds 0-49 (50/50 runs each). Alternatives use different algorithms (complex step 1e-20; reverse-mode tape; exact rational pricing with round(Fraction); NumPy vector sums) and all pass.")
row("m2e-alt-richardson-fails", "2.6-autograder (over-constraint)", "alt1 (Richardson central) vs test_central_error_is_of_order_h_squared", F,
    "Alt1 fails 2 tests on 50/50 seeds (see m2e-richardson-claim). This is a correct implementation of a stated page claim, so it is an over-constraint.",
    "See m2e-richardson-claim.")
row("m2e-reference-50", "2.6-autograder", "course/modules/M/M2/grader/reference.py", P,
    "tools/run_graders.py --unit M2 --seeds 0-49: 'run_graders M2: PASS (reference 50/50 seeds, slowest 0.2 s)'. Also mypy --strict on reference, instance and starter passes (same tool).")
row("m2e-starter-fails", "2.6-autograder", "course/modules/M/M2/grader/starter.py", P,
    "run_graders.py starter check passes (empty implementation fails the suite). Signatures of starter, reference agree with project.html Required outputs (fd_derivative(f,x,h,scheme), ad_derivative(f,x), hessian_fd(f,x,h), bond_price_cents(instance)->int, sensitivities(instance)->dict[str,float]).")
row("m2e-instances", "2.6-autograder (instances, 20+ seeds)", "course/modules/M/M2/grader/instance.py", P,
    S + "instance_check.py: seeds 0-49 all valid (face in 1508220..49403540, inside the stated 1000000..50000000; maturity>=1; yield>-1), deterministic (same seed twice identical), 50 distinct dprice_dy and 50 distinct prices. Coupon 3..988 bps, years 1..30, yield 139..1465 bps, all inside the stated ranges.")
row("m2e-test-count", "2.6-spec (test count on page)", "project.html line ~ Grading mode ('runs 46 tests')", P,
    "pytest -q --collect-only test_project.py (scratch copy of grader): '46 tests collected'. Page says 46.")
row("m2e-tolerances-match-code", "2.6-spec (tolerances)", "project.html Conventions 'Tolerances' vs test_project.py", P,
    "Compared each: cubic central 1e-6 at h=1e-5 (test uses 1e-6, h=1e-5); forward-mode 1e-9; Hessian entries 1e-5 at h=1e-4; dprice_dy 1e-6 vs central at 1e-5; d2price_dy2 1e-4 vs second central at 1e-5; named ratios 1e-9; order ratios 1.9..2.1 and 3.8..4.2 at steps 1e-2, 5e-3 (test lines match). Only the symmetry wording differs (see m2e-hess-tolerance-wording).")
row("m2e-order-ratio-bounds", "2.6-autograder", "grader/test_project.py test_forward_error_is_of_order_h, test_central_error_is_of_order_h_squared", P,
    "Analytic check: central error for a cubic is exactly |p3| h^2 so ratio is 4; forward error is h f''/2 + h^2 f'''/6 with |f''|>=1, |f'''|<=6, giving ratio in about [1.98, 2.02] inside [1.9, 2.1]. Reference and alts 2-5 pass all 50 seeds.")
row("m2e-valueerror-conditions", "2.6-autograder (exception types)", "grader/test_project.py ValueError tests vs project.html constraint (a)-(c)", P,
    "Exactly three named conditions are tested in both directions: step <= 0 (fd_derivative and hessian_fd; tests zero, negative, positive accepted), scheme other than forward/central (parametrized backward, Central, empty; forward and central accepted), yield_bps <= -10000 (-10000 and -20000 raise; -9999 accepted) for bond_price_cents and sensitivities. No other exception type is required anywhere in the file (grep for pytest.raises/ValueError: only must_raise uses ValueError).")
row("m2e-messages-no-leak", "2.6-autograder (messages)", "grader/test_project.py require()/must_raise() messages", P,
    "Read every message. Each names a property (e.g. 'the forward difference's error must halve with its step: order h, not h squared'), plus a hint naming a lesson idea. None prints an expected numeric value. The only interpolated text is a key name in 'the sensitivities must include the key ...'.")
row("m2e-pyodide", "2.6-autograder (Pyodide)", "page_smoke --unit M2 --pages project", P,
    "tools/page_smoke.py --unit M2 --pages project: 'page_smoke modules/M/M2/project.html: PASS'. In-browser grader 'All 46 tests pass'; labs lab-M2-project-1/2/3 run in Pyodide (0.0 s each); boot 1.0 s.")
row("m2e-hours", "2.6-hours", "project.html Time budget table; index.html data-hours-project=60, data-hours-lessons=240; curriculum/01-foundations.yaml M2 hours 300", P,
    "Table rows 4+6+22+6+14+8 = 60 = declared 60 = hub data-hours-project. Lessons: 24 x data-hours=10 = 240 = hub data-hours-lessons. 240+60 = 300 = curriculum hours: 300. Arithmetic consistent. Own estimate of component times is within the 30 % band (not separately scored: the brief says hours are design targets).")
row("m2e-ladder", "2.6-spec (ladder)", "project.html ladder section", P,
    "Four rungs in order; rung 2 is class 'lab completion'; rung 3 grading mode 'both' (check_projects.py lists 'autograder' and 'rubric' in the grader and rubric sections); rung 4 open. tools/check_projects.py --unit M2: 'check_projects M2: PASS'.")
row("m2e-rubric-banned-words", "2.9-prose (banned and process words)", "project.html full text (textContent)", P,
    "Scanned for 'roughly half', 'about 6%', 'historically', ellipses, 'builder', 'build', 'round' (process sense), 'verifier', 'REQUEST', 'unit report': 0 hits. Scope words 'only' (11), 'every' (11), 'any' (10), 'same' (9), 'all' (2): each reviewed; each is a stated formula or a tested property.")
row("m2e-exemplar-a-blind", "2.6-rubric calibration", "project.html exemplar A (official data-scores 2,1,2,2,2)", P,
    "Blind scores from rubric text: C1 2 (orders stated, no sweep), C2 1 (no case), C3 1 or 2 (analytic reported, no FD value, no tolerance), C4 2 (orders with no derivation), C5 2 (price unit, derivative unit missing). Each within one level of official.")
row("m2e-dag", "2.8-DAG", "check_dag --unit M2; project links L13.html#def-finite-difference-derivative, L19.html#def-hessian", P,
    "tools/check_dag.py --unit M2: PASS. Both links point at defined ids (L13 line defines def-finite-difference-derivative; L19 defines def-hessian). Project concepts used by name only (duration, convexity previews) are prose, as Architect Q8 allows.")
row("m2e-references", "2.1-citations", "project.html Reading and References; references/references.json keys spivak2008calculus, hubbard2015vector", P,
    "tools/verify_refs.py --offline: '560 entries, 0 problems'. tools/verify_refs.py --unit M2 (live): '2 of 560 entries, 0 problems'. The page attributes no statement to either source and gives no locator (consistent with the open-items file). Its claim 'Taylor's theorem as stated in Lesson 8' matches course/modules/M/M2/L08.html Theorem 2.1 (Lagrange remainder).")
row("m2e-lint", "2.6-autograder lint", "course/modules/M/M2/grader, tests/labs/M2", P,
    "ruff check and ruff format --check on grader and lab twins: 'All checks passed', '31 files already formatted'. mypy --strict is applied by run_graders to reference, instance and starter (passes). Note: running mypy directly on test_project.py reports import-not-found for sensitivity_engine/instance, which is expected outside the grader's sys.path; not a gate.")
row("m2e-run-labs", "2.5-labs (all labs of the unit, incl. the three project labs)", "tools/run_labs.py --unit M2", P,
    "'run_labs M2: PASS (27/27)'. Direct runs of lab-M2-project-1/2/3 under python -I -W error give the same output as the page blocks.")

# ---- cards ----
row("m2e-cards-count-coverage", "2.7-cards", "course/modules/M/M2/cards.json", P,
    "375 cards, ids M2-c001..M2-c375, all keys present, lessons L01..L24 each with cards (per lesson 11..22). Grades: T 241, C 76 (all with a basis), absent 58 (definitions and conventions). No duplicate ids.")
row("m2e-cards-numbers-in-lesson", "2.7-cards", "cards.json (all numbers) vs course/modules/M/M2/L01..L24.html text", P,
    S + "cards_numbers_and_duplicates.py: every number token in every card front and back appears verbatim in its own lesson's text (0 missing, all 375 cards).")
row("m2e-cards-dup-scan", "2.7-cards (duplicates)", "cards.json", P,
    "Normalized-front scan (punctuation stripped): one collision, between M2-c342 'P'(y0)' and M2-c343 'P''(y0)' (both normalize to 'P y0'). The fronts differ in the prime count, so this is not a duplicate. No duplicate ids. No card repeated verbatim.")
row("m2e-cards-numeric-rederive", "2.7-cards (numbers re-derived)", "cards L01 (c006), L02 (c025,c026), L03 (c035), L04 (c046,c047,c050), L05 (c055..c058), L09 (c124..c131), L10 (c139,c140,c141), L11 (c151,c154,c155), L12 (c170,c172), L13 (c190,c193,c196,c197), L14 (c206,c209), L15 (c233,c234), L16, L17, L18, L19, L20 (c300,c301), L21, L23, L24 (c370)", P,
    S + "cards_L05_numbers.py, cards_L09_numbers.py and hand/Fraction checks. Values recomputed: L05 p'(1.5)=32.0625, central error 2.350e-07; q' 29/49 error 3.328e-10; c' 95.0625 error 8.550e-07; L09 U_128=0.337249755859375, L_128=0.329437255859375, U-L=1/n, nonuniform U-L=0.15933400 and mesh 0.19, midpoint error -0.00130208 at n=8; L10 U-L=3/n and -1.00585175 / -0.99413300 at n=256; L13 forward bound ratios 9.990..10.101 and central 98.91..101.11 recomputed from e^(xi) intervals; L24 c370 minimizers 1.8e-8 and 6.3e-6 recomputed. All match.")
row("m2e-cards-lab-outputs", "2.7-cards (lab-read grade)", "cards L13 (c191-c195), L19 (c287-c289), L23 (c341-c346, c352), L24 (c366-c369)", P,
    "Each quoted lab number matched the twin run under python -I (tests/labs/M2/lab-M2-L13-1.py, L18, L19, L23, L24): e.g. L23 'difference 1.9e+00', '-15 cents', 'first-order error 4.037716e+02'; L24 '6.603e-09 at 1e-8', '5.859e-11 at 1e-5', '3.903e-01 at 1e-15'; L19 '2.26e-11', '1.94e-11', ratios 3.9509/7.8836 etc. Grades C with basis naming the lab.")
row("m2e-cards-grade-C-basis", "2.3-grades (cards)", "cards.json grade C entries (76)", P,
    "All 76 grade-C cards carry a basis. Two (c188, c189) are grade C with basis 'Theorem 2.1 with the assumed fact that the derivative of exp is exp (Example 2.3)', which correctly records the assumption.")
row("m2e-cards-T-hypotheses-c131", "2.3-grades / 2.4 (proposition hypotheses)", "cards.json M2-c131 (L09)", F,
    "Card: 'Do upper and lower sums equal the integral at any finite n? No. They bracket the integral.' For a constant f, U(f,P)=L(f,P)=the integral for every partition, so the answer 'No' is false. The lesson's sentence 'they do not reach it at any finite n' (course/modules/M/M2/L09.html, Section 4, context of x^2) is stated more generally than its x^2 computation supports.",
    "Change the card to ask about x^2 specifically (n=128 values) and the lesson sentence to 'for f(x)=x^2 they do not reach it at any finite n', or say 'a non-constant strictly monotone f'.")
row("m2e-cards-T-hypotheses-c205", "2.3-grades (T with unproved assumption)", "cards.json M2-c205 (L14 Proposition 3.1)", F,
    "Card graded T; its back says the proof 'uses that the derivative of exp is exp, which the page assumes without proof and does not list among the hypotheses'. L14 text: 'the derivative of exp is exp (assumed here, as in Lesson L13 and not proved on this page)'. A proposition graded T whose proof needs a hypothesis the statement omits is a fail (Architect rule; VERIFIER_RULES 2.4).",
    "Grade c205 C with basis 'assumed fact: derivative of exp is exp', or add that fact to the hypotheses of the proposition on the lesson page.")
row("m2e-cards-T-needed-c319", "2.3-grades / 2.4 (overclaim)", "cards.json M2-c319 (L21 Section 3)", F,
    "Card: 'the condition F_y not 0 is needed (Section 3)'. A sufficient hypothesis is presented as necessary. Witness: F(x,y)=y^3 - x^3 at (0,0): F_y(0,0)=0, yet g(x)=x is the unique C^1 solution of F(x,g(x))=0 with g(0)=0 (g'(0)=1). Example 3.2 only shows that without F_y not 0 this particular relation has no function.",
    "Say 'the theorem assumes F_y not 0; Example 3.2 shows the conclusion can fail without it'. Remove 'needed'.")
row("m2e-cards-T-needed-c292", "2.4 (overclaim)", "cards.json M2-c292 (L19 Theorem 2.1)", F,
    "Card: 'Equality needs the continuity of f_xy at the point'. Theorem 2.1 gives continuity of f_xy at p as a SUFFICIENT hypothesis for f_yx(p)=f_xy(p). The card states it as necessary, which the lesson does not prove. (I did not construct a counterexample; the defect is the unsupported word 'needs'.)",
    "Replace 'Equality needs' with 'Equality follows when' (Theorem 2.1 gives sufficiency only).")
row("m2e-cards-lab-as-T-c294", "2.3-grades (lab number under T)", "cards.json M2-c294 (L19)", F,
    "Card graded T: 'Lab 1 prints an asymmetry of 1.94e-11 for a smooth function, which is a finite-difference error.' The 'which is a finite-difference error' is a causal claim read off a SIMULATED lab run and is not established by the lab or the lesson. Architect rule (e): results read off a lab are grade C naming the lab.",
    "Grade C with basis 'Lab 1 (L19, one run at step 1e-5)', or drop the causal clause.")
row("m2e-cards-lab-as-T-c371", "2.3-grades (lab number under T)", "cards.json M2-c371 (L24)", F,
    "Card graded T cites 'In Lab 1 the forward error rises from 6.603e-09 at 1e-8 to 2.154e-07 at 1e-9'. These are measured values of one double-precision run (lab output verified), so the sentence is lab-read and should carry grade C with basis 'Lab 1 (L24 part B)'. The proposition half of the card is T.",
    "Split the card: T for the bound (Proposition 4.2), C for the lab figures.")
row("m2e-cards-lesson-text-full", "2.7-cards (cards agree with the CURRENT lesson text)", "cards.json vs course/modules/M/M2/L01..L24.html", U,
    "Read all 375 cards in full and checked: every number appears in its lesson (automated); all numeric claims re-derived; every T card that depends on a stated hypothesis was checked for that hypothesis against the card (proposition hypotheses in cards c004-c373). I did NOT read all 24 lesson pages line by line (about 20 KB of text each): the card-to-lesson agreement is verified for the sentences I searched (e.g. L08 Lagrange, L09 section 4, L11 integrability, L13 Theorems 2.1-2.2, L14 exp assumption, L21 Section 3, L07 27 checks, L19 Theorem 2.1) and not for every sentence of every page.",
    "A full line-by-line card-to-lesson reading of L01..L24 is needed to convert this row to PASS.")

mutants = []
import glob, os
desc = {
 "m01": "The central scheme returns the forward difference, so its error is of order h, not h squared.",
 "m02": "The Hessian step is divided by a million before the second differences, below the round-off floor.",
 "m03": "The dual product drops the term self.dot times other.value, so the product rule is incomplete.",
 "m04": "The lower off-diagonal entry is the upper one shifted by the step, an asymmetric Hessian accepted as is.",
 "m05": "The bond price is truncated toward zero instead of rounded half to even.",
 "m06": "The bond price for seed 0 is a fixed number, not the price of the instance.",
 "m07": "The yield derivative has the wrong sign, so a bond's price is reported as rising with its yield.",
 "m08": "A negative step is taken as its absolute value instead of being refused.",
 "m09": "A yield of exactly -1 is accepted, so the discount factor divides by zero instead of raising ValueError.",
 "m10": "An unknown scheme is silently computed as the central difference instead of raising ValueError.",
 "m11": "The forward scheme returns the backward difference (f(x) - f(x-h)) / h, which has the same order h and passes the order test.",
 "m12": "The forward scheme returns (f(x + 2h) - f(x)) / (2h), which is of order h and passes the order test but is not the forward estimate.",
 "m13": "The Hessian takes the absolute value of a negative step instead of raising ValueError.",
 "m14": "The scheme name is matched case-insensitively, so 'Central' is accepted instead of raising ValueError.",
 "m15": "The duration and convexity divide by the rounded integer price instead of the unrounded price.",
 "m16": "The final year pays the face value but omits that year's coupon.",
}
killed = {
 "m01": "test_central_difference_matches_the_analytic_derivative[inst0] (seed 0)",
 "m02": "test_hessian_matches_the_analytic_hessian[inst0] (seed 0)",
 "m03": "test_forward_mode_matches_the_analytic_derivative[inst0] (seed 0)",
 "m04": "test_hessian_matches_the_analytic_hessian[inst0] (seed 0)",
 "m05": "test_price_is_the_half_even_rounding_of_the_exact_price[inst0] (seed 0)",
 "m06": "test_price_is_the_half_even_rounding_of_the_exact_price[inst0] (seed 0)",
 "m07": "test_first_derivative_matches_the_central_difference_of_the_price[inst0] (seed 0)",
 "m08": "test_negative_step_raises_value_error (seed 0)",
 "m09": "test_yield_at_minus_one_raises_for_price_and_sensitivities (seed 0)",
 "m10": "test_unknown_scheme_raises_value_error[backward] (seed 0)",
 "m13": "test_hessian_zero_or_negative_step_raises_value_error (seed 0)",
 "m14": "test_unknown_scheme_raises_value_error[Central] (seed 0)",
 "m15": "test_named_ratios_are_the_stated_formulas[inst0] (seed 0)",
 "m16": "test_price_is_the_half_even_rounding_of_the_exact_price[inst0] (seed 0)",
}
for k in sorted(desc):
    mutants.append({"id": k, "description": desc[k], "killed_by": killed.get(k)})
# survivors carry killed_by None -> counted as not killed

frag = {
 "unit": "M2",
 "slice": "M2-e",
 "round": 1,
 "verifier": "Claude Haiku 5.5 (independent verifier, round 1; did not build M2; no shared context with builders)",
 "pin": "c11ae01 (detached worktree /tmp/verifyB1-M2-e)",
 "base": "none",
 "checkout": "/tmp/verifyB1-M2-e",
 "scratch": "/tmp/M2-v/M2-e",
 "verified_at": "2026-10-28T12:38:24+00:00",
 "verdict": "FAIL",
 "rows": rows,
 "mutants": mutants,
 "registry_flags": [],
 "freshness_flags": [],
 "notes": "Round 1 first independent verification of M2 slice e (project.html incl. rubric, grader, project labs, cards.json). Commands run on pin: check_projects --unit M2 PASS; run_graders --unit M2 --seeds 0-49 PASS 50/50; mutate_graders --unit M2 --seeds 0-9 FAIL 14/16 (m11, m12 survive; m13-m16 are verifier mutants); run_labs --unit M2 PASS 27/27; page_smoke --unit M2 --pages project PASS; check_dag --unit M2 PASS; verify_refs --offline 560/0 and --unit M2 live 2/0; ruff check/format PASS. Alternatives (scripts under " + S + "alts) pass 50/50 except alt1 (Richardson), which fails 2 tests on every seed. Not done: a line-by-line read of all 24 lesson pages for the card comparison (row m2e-cards-lesson-text-full); no git commit or push; no slice file edited.",
 "summary": None,
}
n = len(rows)
frag["summary"] = {"rows": n, "pass": sum(r["status"] == P for r in rows), "fail": sum(r["status"] == F for r in rows),
                   "unverifiable": sum(r["status"] == U for r in rows), "mutants": len(mutants),
                   "mutants_killed": sum(1 for m in mutants if m["killed_by"])}
os.makedirs("ledgers/M2", exist_ok=True)
json.dump(frag, open("ledgers/M2/M2-e.json", "w", encoding="utf-8"), indent=2, ensure_ascii=False)
print(frag["summary"])
