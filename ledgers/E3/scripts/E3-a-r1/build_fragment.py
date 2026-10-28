import json, datetime
R = []
def row(i, check, loc, status, evidence, fix=None):
    d = {"id": i, "check": check, "location": loc, "status": status, "evidence": evidence}
    if status != "PASS":
        d["fix"] = fix
    R.append(d)

S = "ledgers/E3/scripts/E3-a-r1/"
# ---- gates and commands
row("E3a-cmd-check_pages", "2.9-structure", "tools/check_pages.py; course/modules/E/E3/index.html, L01.html, L02.html, L03.html", "PASS",
    "`.venv/bin/python tools/check_pages.py --unit E3` -> 'check_pages E3: PASS', exit 0 (run in checkout at 55b5634).")
row("E3a-cmd-check_dag", "DAG", "tools/check_dag.py; course/modules/E/E3/*", "PASS",
    "`.venv/bin/python tools/check_dag.py --unit E3` -> 'check_dag E3: PASS', exit 0.")
row("E3a-cmd-run_labs", "2.5-lab", "tools/run_labs.py; tests/labs/E3/*", "PASS",
    "`.venv/bin/python tools/run_labs.py --unit E3` -> 'run_labs E3: PASS (11/11)', exit 0 (covers the three slice twins plus L04-L08 and project twins).")
row("E3a-cmd-page_smoke", "2.5-lab / 2.9-structure", "tools/page_smoke.py --unit E3 --pages index L01 L02 L03", "PASS",
    "`.venv/bin/python tools/page_smoke.py --unit E3 --pages index L01 L02 L03` -> PASS for modules/E/E3/index.html, L01.html, L02.html, L03.html and 'page_smoke E3: PASS'. Runtime boot 1.1 to 1.2 s; lab steps 0.0 s.")
row("E3a-cmd-twins-isolated", "2.5-lab", f"tests/labs/E3/lab-E3-L01-1.py, lab-E3-L02-1.py, lab-E3-L03-1.py; {S}embed_check.py", "PASS",
    "`.venv/bin/python -I -W error tests/labs/E3/lab-E3-L0N-1.py` exits 0 for N = 1, 2, 3; stdout compared with each page's <pre class=\"expected\"> block by `.venv/bin/python -I ledgers/E3/scripts/E3-a-r1/embed_check.py` -> 'L01 exit 0 embedded_equals_run True lines 23', 'L02 ... True lines 16', 'L03 ... True lines 19', 'ALL True'.")
row("E3a-cmd-ruff-mypy", "2.5-lab", "tests/labs/E3/lab-E3-L01-1.py, lab-E3-L02-1.py, lab-E3-L03-1.py", "PASS",
    "`.venv/bin/ruff check` on the three twins: 'All checks passed!'; `.venv/bin/ruff format --check`: '3 files already formatted'; `.venv/bin/mypy` on the three twins: 'Success: no issues found in 3 source files'.")
row("E3a-cmd-verify_refs", "2.1-citations", "tools/verify_refs.py --unit E3; references/references.json", "PASS",
    "`.venv/bin/python tools/verify_refs.py --unit E3` -> 'live re-verification of E3: 5 of 560 entries, 0 problems'. `.venv/bin/python tools/verify_refs.py --offline` -> 'offline integrity: 560 entries, 0 problems'. Registry records read for pratt1964risk (Pratt, Econometrica 32(1-2), JSTOR), kahneman1979prospect (Econometrica 47(2)), epstein1989substitution (Econometrica 57(4)), ellsberg1961risk (QJE 75(4)), gilboa1989maxmin (J. Math. Econ. 18(2)); the slice cites them only at work level (hub reading list, L02 References 'for the name only').")
row("E3a-cmd-mutants-na", "2.6-mutation", "course/modules/E/E3/index.html, L01.html, L02.html, L03.html", "PASS",
    "Not a project slice: the slice holds no grader. Per the architect ruling (mutation testing applies to project graders only) no mutant is required here and none is listed. The ten builder mutants in ledgers/E3/mutants/ belong to the project slice and were not run against this slice.")

# ---- hub index.html
row("E3a-hub-hours", "2.9-structure / 2.6-hours", "course/modules/E/E3/index.html:29,43; L01-L08 data-hours", "PASS",
    "index.html line 29 data-hours-lessons=\"56\", data-hours-project=\"14\"; line 43 '56 h lessons · 14 h project (20%)'. Lesson attributes data-hours=\"7\" in all eight lessons (grep of L01-L08). 8 x 7 = 56; 56 + 14 = 70 = curriculum/02-economics-finance-core.yaml hours. Hours-split bar widths 80% / 20% match 56/70 and 14/70. Pace not judged (architect ruling).")
row("E3a-hub-placement", "2.9-structure / quiz", "course/modules/E/E3/index.html:66-122", "PASS",
    "Eight items (six prerequisite, two marked data-skill). 6/8 = 75 percent and 7/8 = 87.5 percent (line 68) correct. Keys recomputed: 100 x 1/2 = 50; E[X^2] = 2, variance = 1; d/dx ln x at 2 = 0.5; 100/1.1 = 90.90909 (tolerance 0.001 covers 90.909); E[u] = 5000 for u=x^2 on {0,100}; logit form 1/(1+exp[-kappa(CE_A-CE_B)]) matches the E3 spec in plans/E3-build-plan.md section 6.2.")
row("E3a-hub-prereq-unlock", "DAG / 2.9", "course/modules/E/E3/index.html:35-36,63; curriculum/curriculum.json", "PASS",
    "Prerequisites E1 'Microeconomics' and M4 'Probability' match curriculum.json titles and E3 prereqs [E1, M4]. Unlocks E4 (prereqs [E2, E3, M7]), AP2 'Mean-Variance, CAPM, ICAPM & APT' (prereqs [M7, S1, E3]) and AP7 'Behavioral Finance' (prereqs [AP5, E3]) all list E3 as a prerequisite.")
row("E3a-hub-concept-links", "DAG", "course/modules/E/E3/index.html:63", "PASS",
    "Links to concepts.html#utility-maximization, #random-variable, #expectation, #variance, #derivative, #exponential-and-logarithm, #discount-factor each resolve to one anchor in course/concepts.html; the entries read 'not yet released' (e.g. line 305, utility-maximization). Concept owners in curriculum.json are E1, M4, M2, M1, M1 respectively; all are in the prerequisite closure {E1, M1, M2, M4, P0.1}.")
row("E3a-hub-objectives", "2.9-structure / scope", "course/modules/E/E3/index.html:50-53", "PASS",
    "Objectives 1-3 map to L01 (expected utility, linearity), L02 (CE, Arrow-Pratt, CE <= E X) and L03 (CRRA CE in whole cents, homogeneity), each claim traced to a proposition or lab check on those pages (see L01-L03 rows). Objectives 4-8 point at L04-L08 and were not verified here (outside this slice); eight measurable verbs are present (line 48-58).")
row("E3a-hub-cards-L01-L03", "2.7-cards (hub cards)", "course/modules/E/E3/index.html:129-131", "PASS",
    "Hub card text for L01 (linearity; invariance under positive affine transformations) matches Propositions 2.3 and 3.3; L02 (CE does not exceed E X; second-order approximation of the premium) matches Propositions 1.3 and 3.1; L03 (CRRA family, logarithmic limit, whole cents, homogeneity) matches Propositions 1.4, 2.4, 2.6. Card kicker hours (7 h) match data-hours.")
row("E3a-hub-reading", "2.1-citations / 2.9-structure", "course/modules/E/E3/index.html:157-167; L01.html:562-565; L02.html:602-605; L03.html:551-553", "PASS",
    "Hub reading list cites the five curriculum keys (five strings at curriculum/02-economics-finance-core.yaml:109-114). grep for Pratt, Kahneman, Tversky, Ellsberg, Gilboa, Epstein, Schmeidler, 1961, 1964, 1979, 1989 over course/modules/E/E3/*.html: L02 cites Pratt for the name only; L05 (grade D), L07 (grade C, title only), L08 (grade C, title only) cite works at title or work level and state no result. No result is attributed to any of them in L01-L03.")
row("E3a-hub-data-status", "2.8-data / 2.9", "course/modules/E/E3/index.html:38,152-155", "PASS",
    "No dataset is read in L01-L03: the labs use fixed lotteries (L01 LOTTERIES dict; L02 GAMBLE; L03 PRIZES_CENTS) and state 'no data' in their docstrings. No generated lottery or participant appears in the slice, so no SIMULATED label is needed here.")
row("E3a-hub-privacy-claim", "2.9-structure / 2.6-project", "course/modules/E/E3/index.html:154", "UNVERIFIABLE",
    "Hub sentence 'They stay in the browser and are never sent to a server' is a statement about the project's code. The project page footer (project.html:651) says 'nothing you write leaves it', and project.html:252 says the code is saved in the browser. The project grader and its JavaScript were not read in this slice, so 'never sent to a server' is not verified.",
    "Either have the project-slice verifier confirm there is no network call in the project code, or soften the hub sentence to what project.html states.")

# ---- L01
row("E3a-L01-structure", "2.9-structure", "course/modules/E/E3/L01.html", "PASS",
    "Order: why-it-matters (115 words, line 51), core sections 1-3, lab (line 161), canon-breaks (328), misconceptions (3, lines 341-350), problems (mechanics M1-M3, proof P1-P3, empirical E1-E3, research R1-R3; 12 solutions, all >= 15 words), key results table (line 464), quiz (10 items, 10 explain blocks), references (data-references). data-hours=\"7\".")
row("E3a-L01-numbers", "2.2-numbers", "course/modules/E/E3/L01.html:79,143,158,163,325,343,347,366-367,373,416,423,455; recomputed by ledgers/E3/scripts/E3-a-r1/recompute_numbers.py", "PASS",
    "Example 1.4: E X = 150 CU, E u = 45000 CU^2 (recomputed exact). Example 3.4: E u(C) = 37500, 37500 < 45000. Lab expected values 15000 / 12500 / 15000 cents and quadratic 45000 / 21250 / 37500 recomputed from x^2/10000 (exact). M1: E X = 59, E u = 4030, u(59) = 3481, difference 549. M2: 133.333 = 400/3. M3: E v = 65, 95. E1: 45000 - 37500 = 7500. R3: 25000 and 22500. All match. Class (a) for lab-printed values, (c) for hand values.")
row("E3a-L01-lab", "2.5-lab", "course/modules/E/E3/L01.html:161-326; tests/labs/E3/lab-E3-L01-1.py", "PASS",
    "Hypothesis (line 163) predicts 45000, 21250, 37500 squared CU, six 'True' linearity lines, six order lines, and two ValueError rejections: all four match the run output (embedded_equals_run True). Interpretation (line 325) names only the printed checks and states 'it does not check any preference ordering over lotteries'. Lab uses no random draws; standard library only.")
row("E3a-L01-proofs", "2.4-mathematics", "course/modules/E/E3/L01.html:84-154 (Def 2.1, Prop 2.2, 2.3, 3.1, 3.3, Def 3.2)", "PASS",
    "Re-derived: Prop 2.2 weights sum to 1 (sum of alpha p_L + (1-alpha) p_M = 1), Prop 2.3 split of a finite sum, Prop 3.1 sum p_i (a + b x_i) = a + b E X, Prop 3.3 difference E v(L) - E v(M) = b (E u(L) - E u(M)). Assumptions A1 stated (line 73); every proposition carries T (lines 90, 104, 132, 147). Remark 2.4 correctly disclaims the representation claim.")
row("E3a-L01-Q7-mixture", "2.7-cards / quiz", "course/modules/E/E3/L01.html:532-538", "FAIL",
    "Quiz stem: 'A mixture 1/3 A + 2/3 B of lotteries A and B gives 0 CU with probability 1/2 under A and 1/4 under B'. Example 1.4 (line 79) defines A with P(0 CU) = 1/4, not 1/2. Lottery B is not defined anywhere in the lesson text (it appears only in the lab's LOTTERIES dict, which has no 0-CU outcome). The stated probability under A contradicts the lesson's A.",
    "Define both lotteries in the stem consistently with the lesson. Example: 'A pays 0 CU with probability 1/4 (as in Example 1.4) and B pays 0 CU with probability 1/4'; the mixture 1/3 A + 2/3 B then gives 0 CU with probability 1/4, and the explanation changes accordingly.")
row("E3a-L01-necessity", "2.4-mathematics / 2.3-grades", "course/modules/E/E3/L01.html:343 (misconception 1), 504-512 (quiz item L01q4 and its explanation at line 511)", "FAIL",
    "Quiz asks 'Under which condition is E u(X) = u(E X) for every finite lottery X?' with the answer 'u is affine'. Misconception 1 (line 343) says the equality 'holds only when u is affine'. The lesson proves only the sufficiency direction (Prop 3.1, line 133). The necessity direction (equality for every finite lottery forces u to be affine on the outcome domain) is not proved or cited anywhere in L01. The explanation at line 511 shows only the failure for x^2.",
    "Add a short proof of necessity on the page: with two-point lotteries p x + (1-p) y, the equality for every p in [0,1] gives p u(x) + (1-p) u(y) = u(p x + (1-p) y) for all x, y, p, which is the affine condition on the domain; or restrict the quiz and misconception to sufficiency ('u affine implies ...').")
row("E3a-L01-R2-claim", "2.3-grades / 2.4-mathematics", "course/modules/E/E3/L01.html:448 (problem R2 solution)", "FAIL",
    "R2 solution: 'A representation theorem also requires a continuity condition, and this lesson does not state one', and 'a representation would need ... must also respect mixtures'. These are necessity claims about representation theorems with no grade, no registry key and no proof on the page. They are not graded and not attributed.",
    "Either grade the claim (e.g. with a registry key if it is taken from a source that can be read) or rephrase it as a remark that a representation result needs further conditions, which this lesson does not state, without the word 'requires'.")
row("E3a-L01-terms-define", "2.9-structure / DAG", "course/modules/E/E3/L01.html:59-69,73,133,141-143", "PASS",
    "Terms in order: lottery (Def 1.1), expectation (Def 1.2, M4), Bernoulli utility and expected utility (Def 1.3, the only dfn with data-concept expected-utility, line 69), A1, mixture (Def 2.1), affine (as a+bx in Prop 3.1), risk neutral (Def 3.2). Only M4 concepts are linked from L01 (random-variable, expectation). check_dag passes.")
row("E3a-L01-banned-process", "2.9-structure", "course/modules/E/E3/L01.html", "PASS",
    "grep for TODO, TBD, lorem, for brevity, details omitted, beyond the scope, left as an exercise, you can add more, it is important to note, studies show, experts agree, it is well known, obviously, clearly, historically, roughly, ellipsis, builder, verifier, round N, REQUEST, unit report: no hit. check_pages (banned strings) PASS.")
row("E3a-L01-scope-words", "2.4 / scope", "course/modules/E/E3/L01.html:74,105,298,331,334,441,455,565", "PASS",
    "Scope words checked: 'every' (A1 sums, line 74) is backed by the finiteness argument and the proofs; 'any' / 'no result here allows' (line 74, 331) hold for the finite-sum formulas; 'every finite lottery' (line 147 uses A1); R1 'Among all finite lotteries on this set' is computed in R1; 'only the sign of the scale factor matters' (line 351) is backed by Prop 3.3 and P2, with b = 0 excluded by the proposition's b > 0 hypothesis. R3 'does not establish a general pattern' is honest.")

# ---- L02
row("E3a-L02-structure", "2.9-structure", "course/modules/E/E3/L02.html", "PASS",
    "Why-it-matters 120 words (line 51, at the limit but within 120). Sections 1-3, lab (line 195), canon-breaks (372-380, four bullets), misconceptions (3), problems M1-M3, P1-P3, E1-E3, R1-R3 (12 solutions, all >= 15 words), key results (5 rows, all T), quiz (10 items, 10 explanations), references, data-hours=\"7\".")
row("E3a-L02-A4-hypothesis", "2.4-mathematics / hypothesis", "course/modules/E/E3/L02.html:71-72 (A4), 94 (Prop 1.3(b)), 114 (proof), 442 (P2), 497 (R3)", "FAIL",
    "Assumption A4 (strict concavity) is printed as 'u(y) < 0 for every y in I'. Proposition 1.3(b) line 94 cites 'Assumption A4' for the hypothesis 'u''(y) < 0 for every y in I', and the proof (line 114) uses the strict sign of u''(xi). Problem R3 (line 497) writes 'A2 holds with u'' < 0 on I (A4)'. The printed A4 is therefore not the hypothesis the proof uses, and a reader who checks A4 as printed cannot verify Prop 1.3(b). P2 (line 442) argues 'A4 fails' from u = x, which is consistent only with the intended u'' < 0 reading.",
    "Restate A4 as \"u''(y) < 0 for every y in I\" (the hypothesis of Prop 1.3(b) and of Problems P2, P3, R3). Keep the Assumption label. P2 and P3 remain correct because u'' = 0 for u = x.")
row("E3a-L02-numbers", "2.2-numbers", "course/modules/E/E3/L02.html:124,147,369,375,387,391,458-460,467,474-475; recomputed by recompute_numbers.py", "FAIL",
    "Recomputed and correct: Example 1.5 E sqrt(W) = 9.7434164902..., CE = 94.934164902..., premium 5.065835097... (printed 94.934165 and 5.065835, both correct at six decimals); 9.743416 (displayed, rounds down from 9.7434164...) correct; cent values 9493.4165 -> 9493 and 506.5835 -> 507 correct; Part B gaps 0.565835, 0.119495, 0.028811, 0.004565, 0.000046 correct; error share 0.565835/5.065835 = 0.111696 -> 11.17 percent correct; 0.565835/4.5 = 0.125741 -> 12.57 percent correct; 900/5.065835 = 177.66 -> 'about 178' correct; 0.028811/0.004565 = 6.31 but line 459 says 'a factor of about six'.",
    "Write 'a factor of about 6.3' (0.028811 / 0.004565 = 6.31 from the displayed digits), or state the basis of 'about six'.")
row("E3a-L02-lab", "2.5-lab", "course/modules/E/E3/L02.html:195-370; tests/labs/E3/lab-E3-L02-1.py", "PASS",
    "Embedded expected block equals the isolated run (embed_check.py, 16 lines). Hypothesis numbers: variance 1800 (recomputed), Pratt approximation 4.5 (recomputed), premium above 4.5 (5.065835), gaps shrink (True, recomputed by recompute_numbers.py). Part C: linear premium 0 at 1.0, 0.5, 0.1. Interpretation (line 369) says 'a check of the limit ... not a proof'; R2 consistent. Canon/Remark 3.2 claims match Part A/B output.")
row("E3a-L02-proofs", "2.4-mathematics", "course/modules/E/E3/L02.html:75-125 (Prop 1.1, 1.3), 135-148 (Prop 2.2), 159-188 (Prop 3.1)", "PASS",
    "Re-derived: Prop 1.1 (IVT, injectivity by strict monotonicity); Prop 1.3(a) Taylor-Lagrange with u'' <= 0 gives u(y) <= u(m) + u'(m)(y-m), averaging gives E u <= u(m), then c <= m; (b) strictness for x_i != m under u'' < 0 (A4 as intended; see E3a-L02-A4-hypothesis). Prop 2.2 derivatives of a+bu cancel b. Prop 3.1 steps 1-3 re-derived; q(eps)[eta - u'(w)] = (1/2) u'' s^2 + rho, limit -(1/2) u'' s^2 / u' = (1/2) r_A s^2 correct. The E X = 0 hypothesis is in the section preamble only (see E3a-L02-prop31-hyp).")
row("E3a-L02-prop31-hyp", "2.4-mathematics / hypothesis", "course/modules/E/E3/L02.html:161 (statement), 152 (preamble), 171 (proof), 577-584 (quiz L02q8)", "FAIL",
    "Proposition 3.1 is stated 'Under A1 and A5' with the conclusion pi(eps)/eps^2 -> (1/2) r_A(w) s^2, where s^2 = Var(X) only when E X = 0. The proof uses sum p_i x_i = 0 (line 171). The hypothesis E X = 0 is stated in the section preamble (line 152), not in the proposition, so the proposition as stated omits a hypothesis its proof needs. Quiz L02q8 (line 579) asks for the limit as '(1/2) r_A(w) Var(X)' with no E X = 0 condition.",
    "Add 'and E X = 0' to the statement of Proposition 3.1, and add 'for a gamble with E X = 0' to the quiz stem of L02q8.")
row("E3a-L02-refs-facts", "2.9-structure / 2.4", "course/modules/E/E3/L02.html:604 (references paragraph), 177 (Step 2)", "FAIL",
    "References paragraph says the lesson uses 'two calculus facts that the proofs name: the intermediate value theorem and Taylor's theorem, in its Lagrange and Peano forms'. That list has three facts. Step 2 of Prop 3.1 (line 177) also uses 'the inverse of a continuous, strictly increasing function on an interval is continuous', which is not in the list. The count and the list are inconsistent.",
    "Change 'two' to 'three' and list the continuity of the inverse of a strictly increasing continuous function, or say 'calculus facts' and list all of them.")
row("E3a-L02-quiz", "2.7-cards / quiz", "course/modules/E/E3/L02.html:525-599", "PASS",
    "Each answer checked: L02q1 (Def 1.2), q2 (Prop 1.3(a)), numeric 9 (sqrt(W)=3 gives 9), numeric 1 (10 - 9), L02q5 (1/w), numeric 0.5 (r_R at 100), L02q7 (Prop 2.2 with b > 0), L02q9 (Remark 3.2, Problem R2), numeric 2 (r_A of -e^{-2w}). L02q8 is flagged in E3a-L02-prop31-hyp.")
row("E3a-L02-misconceptions-canon", "2.4 / 2.9 / 2.2-numbers", "course/modules/E/E3/L02.html:375-395", "PASS",
    "Canon bullet 1 (11.17 percent) checked; misconception 1 (900 CU, 4.5, 5.065835, about 178 times) checked; misconception 2 (r_A = 0.005 per CU, r_R = 0.5, units) checked; misconception 3 (CE = E X for u(w)=w) follows from the identity utility and P2. The 'risk premium is half the variance' misconception is correctly contradicted.")
row("E3a-L02-notation", "notation", "course/modules/E/E3/L02.html (macros used: \\E, \\Var, \\R, \\pi, \\rho, \\mathrm{CE}); notation/notation.json", "PASS",
    "Registered macros used as registered (\\E, \\Var, \\R). \\pi (risk premium) and \\rho (remainder function in Prop 3.1 proof) are not registered and have no other meaning in L02-L03. Note for the L08 verifier: plans/E3-build-plan.md section 4 says E3 never uses rho, and L08 defines rho = 1 - 1/psi (outside this slice).")
row("E3a-L02-grades", "2.3-grades", "course/modules/E/E3/L02.html:76,90,135,145,159,512-515", "PASS",
    "Propositions 1.1, 1.3, 2.2, 3.1 and Example 2.3 (T; the key-results table has five rows, all T) are derivations on the page and the proofs are complete under the stated hypotheses (the Prop 1.3(b) and Prop 3.1 hypothesis gaps are separate rows). No empirical or lab claim is graded T on this lesson.")

# ---- L03
row("E3a-L03-structure", "2.9-structure", "course/modules/E/E3/L03.html", "PASS",
    "Why-it-matters (106 words, line 51), sections 1-2, Remark 2.8 (rounding, line 176), lab (179-316), canon-breaks (318-327, four bullets), misconceptions (3), problems M1-M3, P1-P3, E1-E3, R1-R3 (12 solutions, all >= 15 words), key results (8 rows; the lab row is C), quiz (9 items, 9 explanations), references, data-hours=\"7\".")
row("E3a-L03-dangling-refs", "2.4-mathematics / cross-references", "course/modules/E/E3/L03.html:82 (Proposition 2.5 and Proposition 1.6), 99 (Proposition 1.6 shows)", "FAIL",
    "The lesson has no Proposition 1.6 and no Proposition 2.5 (grep of L03 for 'Proposition 1.6' and 'Proposition 2.5' finds only the citations). Definition 1.3 (line 82) cites 'Proposition 2.5' for the certainty-equivalent invariance (which is Proposition 2.7) and 'Proposition 1.6' for the Arrow-Pratt invariance (which is L02 Proposition 2.2; Proposition 1.7 is the CRRA measure). Example 1.5 (line 99) says concavity of u_2 is 'as Proposition 1.6 shows' (the concavity follows from Proposition 1.7 with gamma = 2 > 0).",
    "Replace 'Proposition 2.5' with 'Proposition 2.7', replace the Arrow-Pratt citation with 'L02 Proposition 2.2' (the constant shift is an affine change with a > 0 and b = 1), and replace 'Proposition 1.6 shows' with 'Proposition 1.7 shows'.")
row("E3a-L03-linear-wording", "2.9-structure / DAG terms", "course/modules/E/E3/L03.html:99 (Example 1.5), 396 (P3 solution)", "FAIL",
    "Example 1.5 says u_0(w) = w - 1 'is linear in wealth and therefore risk neutral'; P3 says 'u_0 is linear'. w - 1 is affine, not linear. L01 Proposition 3.1 uses 'affine' for a + bx (line 133), and L01 Definition 3.2 defines risk neutrality only for u(x) = bx (line 143). L03 contradicts L01's own usage.",
    "Write 'affine in wealth' and cite L01 Proposition 3.1 with a = -1, b = 1; state that the ranking is by expected value, as in L01 Definition 3.2 and Proposition 3.3.")
row("E3a-L03-cents-bound-explanation", "2.4-mathematics", "course/modules/E/E3/L03.html:421 (E3 solution), 176 (Remark 2.8)", "FAIL",
    "E3 solution: the bound is 5.5 cents 'because the second quantity multiplies a rounding error of up to half a cent by ten'. That accounts for 5 cents only. The remaining 0.5 cent comes from the first rounding |R(10 CE) - 10 CE| <= 1/2, as in the Remark 2.8 proof (line 176). The explanation does not give the full bound.",
    "Add the two terms: the first rounding contributes at most 1/2 cent and multiplying the second rounding error by 10 contributes at most 5 cents, so the total is 5.5 cents.")
row("E3a-L03-ce-cents-misc", "2.2-numbers", "course/modules/E/E3/L03.html:181,297-314,407,412,419,421; recomputed by recompute_numbers.py", "PASS",
    "Recomputed: CE at gamma 0, 0.25, 0.5, 1, 2, 4 = 11250.0, 10931.773303, 10615.800859, 10000.0, 8888.888889, 7337.616109 (all match the printed lines). Half-up rounding: 10932, 10616, 8889, 7338 match. Exact 80000/9 (line 304) correct; expected prize 11250 correct; E1 (10615.8009, 10616) correct; E2 (M = 9/80000, 80000/9 = 8888.8889) correct; E3 (k+1)/2 = 5.5 correct. M2 (1/3000 -> 3000), M3 (1/9000 -> 9000), Ex 2.5 (1600, 2000) correct. Mechanics M1 r_A(4) = 1/8 and r_R = 1/2 correct.")
row("E3a-L03-lab", "2.5-lab", "course/modules/E/E3/L03.html:179-316; tests/labs/E3/lab-E3-L03-1.py", "PASS",
    "Embedded expected block equals the isolated run (embed_check.py, 19 lines). The hypothesis predictions (11250, 10000, 80000/9 about 8888.89 -> 8889, falling order over six exponents, limit and scaling checks) all match printed lines. Interpretation (line 315) labels the grid checks C and states they are 'not proofs'; the C grade is shown in the page. Remark 2.8's bound is checked by the lab (cents_ok True).")
row("E3a-L03-proofs", "2.4-mathematics", "course/modules/E/E3/L03.html:91-94 (Prop 1.4), 112-114 (Prop 1.7), 124-127 (Thm 2.1), 144-147 (Prop 2.4), 159-162 (Prop 2.6), 169-171 (Prop 2.7), 176 (Remark 2.8)", "PASS",
    "Re-derived: Prop 1.4 with h = s L and (e^h - 1)/h -> 1 (A2) gives L; Prop 1.7 u' = w^{-gamma}, u'' = -gamma w^{-gamma-1}, r_A = gamma/w, r_R = gamma; Thm 2.1 g' = 0 gives u' = K w^{-gamma}, hence u = K u_gamma + C with the stated hypotheses; Prop 2.4 gives (M-1)/s and c^s = M; Prop 2.6 (k^s)^{1/s} = k; Prop 2.7 affine invariance. Each proposition states its T grade and its hypotheses (A1 positivity, A2 limit, A3/A4 in Thm 2.1).")
row("E3a-L03-M1-crossref", "DAG / cross-unit", "course/modules/E/E3/L03.html:65,75,146,161; course/modules/M/M1/L03.html:63,92,112,118", "PASS",
    "The cited M1 results exist and say what L03 says: M1 L03 Prop 1.4 (ln inverts exp), Prop 1.6(b) (ln(ab) = ln a + ln b), A2 (addition rule e^{x+z} = e^x e^z), A3 (unique inverse, the uniqueness used in Prop 2.4). M1 L03 line 63 says 'The number e is defined as e^1' and the unit does not derive the limit (e^h - 1)/h -> 1 (no 'lim' in M1 L03), so L03's statement that M1 'does not derive this limit' (A2, line 59) is correct.")
row("E3a-L03-misconceptions-canon", "2.9 / scope / causal", "course/modules/E/E3/L03.html:320-342", "PASS",
    "Canon bullets (four) and misconceptions 1-3 checked against Prop 1.7, Prop 2.6, Lab 1 (gamma = 1 +/- 1e-6 check and k = 2, 3, 10 loop over GAMMAS). 'The lab checks the identity for k = 2, 3, 10 at every exponent on its grid' is true of the code (loop over GAMMAS, lines 284-292).")
row("E3a-L03-causal-interpretation", "2.4 / causal-directional", "course/modules/E/E3/L03.html:334", "FAIL",
    "Misconception 1 says 'a larger wealth makes the same gamble less important in absolute terms'. The page computes r_A(w) = gamma/w, which falls with w, but the page never links that to the size of a premium or of a gamble's importance. The only link on the page is the small-risk approximation of L02 Proposition 3.1, which is asymptotic and is not cited here. The directional interpretation is unsupported on the page.",
    "Either cite L02 Proposition 3.1 for the small-gamble premium ~ (1/2) r_A(w) Var(X) and state that it falls with w for gamma > 0 (asymptotically), or remove 'less important in absolute terms'.")
row("E3a-L03-quiz", "2.7-cards / quiz", "course/modules/E/E3/L03.html:475-548", "PASS",
    "Nine items, each explained; answers checked: L03q1 (ln w), numeric 0.5 (r_R = gamma), L03q3 (r_A falls), numeric 3000 (M2), L03q5 (doubles), L03q6 (subtraction gives finite limit at gamma = 1; explanation cites Prop 2.7), L03q7 (Thm 2.1), L03q8 (CE_0 = E X), L03q9 (grid check). Distractors are wrong as stated.")
row("E3a-L03-grades", "2.3-grades", "course/modules/E/E3/L03.html:69,90,108,119,140,155,460-465", "PASS",
    "Propositions 1.2, 1.4, 1.7, Theorem 2.1, Props 2.4, 2.6 and Remark 2.8 are T, each with a complete proof. Lab-based results (the grid, the difference quotient, the homogeneity check) are C and named as Lab 1 (line 315 and table row 465). Over- or under-grading: none found.")
row("E3a-L03-DAG", "DAG", "course/modules/E/E3/L03.html:37,65,80,136", "PASS",
    "L03 uses expected-utility (L01), arrow-pratt-risk-aversion and certainty-equivalent (L02), random-variable, expectation (M4), derivative (M2), exponential-and-logarithm (M1), and defines crra-utility (line 80). All are in the closure of E3 or defined earlier in E3. check_dag passes.")

# ---- cross-slice / notation
row("E3a-notation-slice", "notation", "course/modules/E/E3/index.html, L01.html, L02.html, L03.html; notation/notation.json", "PASS",
    "Registry symbols T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, Q are not used in the slice. Macros used: \\E, \\Prob (L01 Def 1.1), \\Var (L02), \\R (L02 M3). No registered symbol is given a second meaning. Local letters (w, x, p, u, v, V, CE, pi, gamma, alpha, a, b, K, C, s, eps) are defined where first used.")
row("E3a-DAG-slice", "DAG / 2.9", "check_dag.py --unit E3; grep of links in the slice", "PASS",
    "check_dag E3 PASS. Manual check: no slice page links or uses a concept of a later lesson (L01 uses only L01 and M4 concepts; L02 uses L01 and M2/M4; L03 uses L01, L02, M1, M2, M4). Concepts E3 introduces in L01-L03 are defined once each (expected-utility L01 line 69; certainty-equivalent and arrow-pratt-risk-aversion L02 lines 87, 132; crra-utility L03 line 80).")
row("E3a-hours-arith", "2.6-hours", "course/modules/E/E3/index.html:29,43; L01-L03 data-hours", "PASS",
    "Hub split arithmetic is consistent (56 = 8 x 7; 56 + 14 = 70 = curriculum). Individual hour estimates not judged (architect ruling).")

fragment = {
    "unit": "E3",
    "slice": "E3-a",
    "round": 1,
    "verifier": "Haiku verifier, E3 slice a (hub index.html, L01-L03 and their twins); did not build E3; round 1, first independent verification of this slice",
    "pin": "55b5634",
    "base": "none",
    "checkout": "/tmp/verifyC1-E3-a (detached at 55b5634; .venv symlinked; vendor copied)",
    "scratch": "/tmp/e3-v/a",
    "verified_at": datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat(),
    "verdict": "FAIL",
    "rows": R,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Pin: the task names 55b5634 (the checkout's HEAD); the brief text mentions b4590f6. The task's pin was used.",
        "Not a project slice: no grader, so the ten existing builder mutants (ledgers/E3/mutants/) were not run against this slice, and no new mutants are listed; the architect ruling on lab twins applies.",
        "Lab twins are demonstrations with embedded real output; they were checked for printed-output agreement, hypothesis-first ordering and the interpretation claims, not as graders.",
        "Scripts backing rows: ledgers/E3/scripts/E3-a-r1/recompute_numbers.py (decimal and Fraction recomputation of every displayed number in L01-L03) and ledgers/E3/scripts/E3-a-r1/embed_check.py (runs each twin under python -I -W error and compares with the embedded block).",
        "Cross-slice observation for the L08 verifier: L08 defines rho = 1 - 1/psi, while plans/E3-build-plan.md section 4 says E3 never uses rho. Not a row in this slice.",
        "Hub sentences about L04-L08 (objectives 4-8, the reading list statement) were checked only as far as the grep of attributions and hours reaches; the lessons themselves are outside this slice.",
    ],
    "summary": "E3 slice a: hub, L01-L03 and twins. Gates PASS (check_pages, check_dag, run_labs, page_smoke, twins under -I -W error, ruff, mypy, verify_refs). Numbers recomputed and correct except one rounding phrase. FAIL rows: L02 A4 printed as u(y)<0 while used as u''<0; L03 dangling references to Propositions 1.6 and 2.5; L01 quiz lottery probabilities contradict Example 1.4; L01 necessity claim (u affine) unproved; L02 Prop 3.1 omits E X = 0; L02 'two facts' miscount; L03 'linear' for an affine utility; L03 incomplete cent-bound explanation; L03 unsupported directional wealth claim; L01 ungraded representation claim; L02 'about six' for 6.31. UNVERIFIABLE: hub privacy claim about project code.",
}
import pathlib
out = pathlib.Path("/tmp/verifyC1-E3-a/ledgers/E3/E3-a.json")
out.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(len(R), sum(1 for r in R if r["status"]=="PASS"), sum(1 for r in R if r["status"]=="FAIL"), sum(1 for r in R if r["status"]=="UNVERIFIABLE"))
