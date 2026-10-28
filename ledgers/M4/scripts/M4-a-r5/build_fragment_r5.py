"""Writes the round-5 M4-a verification fragment (ledgers/M4/M4-a.json). Run with -I from the checkout root."""
import json
import sys

S = "/tmp/m4-v/a-r5"
R = "ledgers/M4/scripts/M4-a-r5"
P = []

def row(rid, check, loc, status, evidence, fix=None):
    d = {"id": rid, "check": check, "location": loc, "status": status, "evidence": evidence}
    if status != "PASS":
        d["fix"] = fix
    P.append(d)

# ---- hub index.html ----
row("M4-a-hub-moments-before-definition", "Moment words used before definition on the hub",
    "course/modules/M/M4/index.html (Lessons paragraph; project paragraph)", "PASS",
    f"grep -i moment {S}/index.txt returns no line; the hub uses no moment term.")
row("M4-a-cmd-check-pages", "tools/check_pages.py --unit M4", "course/modules/M/M4/index.html, L01.html-L04.html", "PASS",
    "Command output: 'check_pages M4: PASS'.")
row("M4-a-cmd-check-dag", "tools/check_dag.py --unit M4", "course/modules/M/M4/index.html, L01.html-L04.html", "PASS",
    "Command output: 'check_dag M4: PASS'.")
row("M4-a-cmd-run-labs", "tools/run_labs.py --unit M4; each twin under python -I -W error", "tests/labs/M4/lab-M4-L01-1.py .. lab-M4-L04-1.py", "PASS",
    "run_labs output 'run_labs M4: PASS (13/13)'. Each of the four twins exited 0 under python -I -W error; outputs in " + S + "/lab-M4-L0n-1.out. Command: .venv/bin/python -I -W error tests/labs/M4/lab-M4-L0n-1.py.")
row("M4-a-cmd-page-smoke", "tools/page_smoke.py --unit M4 --pages index L01 L02 L03 L04", "course/modules/M/M4/index.html, L01.html-L04.html", "PASS",
    "Output 'page_smoke M4: PASS'; per-lab timings 0.0 s under the Pyodide run (runtime boot 1.1 s).")
row("M4-a-lint-mypy-pytest", "ruff check, ruff format --check, mypy --no-incremental and pytest -k M4 for the lab suites",
    "tests/labs/M4/lab-M4-L01-1.py .. lab-M4-L04-1.py; tests/test_labs.py; tests/test_run_labs.py", "PASS",
    "ruff check: 'All checks passed!'; ruff format --check: '4 files already formatted'; mypy --no-incremental: 'Success: no issues found in 4 source files'; pytest -q -k M4 on tests/test_labs.py and tests/test_run_labs.py: 13 dots printed and no failure marks (the -q run printed no summary line).")
row("M4-a-refs-live-and-offline", "tools/verify_refs.py --unit M4 (live) and --offline", "references/references.json (key blitzstein2019introduction); tools/verify_refs.py", "PASS",
    "Live: 'live re-verification of M4: 1 of 560 entries, 0 problems'. Offline: 'offline integrity: 560 entries, 0 problems'.")
row("M4-a-blitzstein-attribution", "No statement attributed to Blitzstein that was not read",
    "course/modules/M/M4/index.html (Core reading); L01.html-L04.html (References section)", "PASS",
    "index.txt Core reading and each lesson's References section say no passage from the book has been read and attribute no statement. grep -i blitzstein in the slice pages finds only the citation sentences and the registry key. The DOI was not fetched; no content from the book is cited.")
row("M4-a-hub-hours", "Hub split against lesson hours (arithmetic only)",
    "course/modules/M/M4/index.html (data-hours-lessons=90, data-hours-project=30; eyebrow; Lessons paragraph); L01-L04 header hours", "PASS",
    "data-hours-lessons=90 and data-hours-project=30; 10 lessons x 9 h = 90 (Lessons paragraph: 'Ten lessons of nine study hours'); 30/120 = 25% (eyebrow '25% of 120 h'); L01-L04 headers each read '9 study hours'. Hour pace not judged (architect ruling).")
row("M4-a-hub-objectives-map-ladder", "Objectives, lesson map and ladder agree with lessons",
    "course/modules/M/M4/index.html (#objectives, #lessons cards, ladder)", "PASS",
    "Each objective maps to a lesson whose content exists (L01 Def 3.1/Prop 3.2; L02 Prop 2.2/2.3; L03 Ex 2.5 and §4; L04-L05 covariance and matrix; L06 Prop 2.6; L09/L10). The L09 hub card matches L09 text: characteristic-function limit proved (Prop 2.3(b)), distribution-function limit 'not established on this page' (" + S + "/L09.txt). The L10 card matches L10 text: Lab 1 covers Cauchy and Student-t(3) sample means; Definition 2.4 is the failure of the CLT under infinite variance.")
row("M4-a-hub-placement-answers", "Placement items, keys, mastery bar and rung checks",
    "course/modules/M/M4/index.html (#placement, items 1-10, explain blocks; skill checks rung 1 and rung 2)", "PASS",
    "Keys checked: item 1 'some student has not passed' (M1 Theorem 3.1); item 6 1+1/2+1/4+1/8 = 15/8 = 1.875; item 7 1/(1+r); item 8 2xy; rung 1 quantile F(0)=1/4<1/2<=F(1)=3/4 gives 1; rung 2 Var(t_5)=5/3, s^2=3/5=0.6 (" + R + "/recheck_r5.py hub rows). Eight prerequisite items plus two skill checks; bar 8 of 10.")
row("M4-a-hub-data-status", "No real data; SIMULATED labels", "course/modules/M/M4/index.html (#data, footer); L02.html and L03.html lab sections", "PASS",
    "grep for open(, read and Path in tests/labs/M4/*.py: no file read in any M4 twin. Seeded samples are labelled SIMULATED on L02 and L03 (see M4-a-simulated-label).")
row("M4-a-simulated-label", "Seeded-sample labs labelled SIMULATED", "course/modules/M/M4/L02.html (Lab 2 section); course/modules/M/M4/L03.html (Lab 3 section)", "PASS",
    "L02 Lab 2 text: 'The seeded samples are SIMULATED'; L03 Lab 3 text: 'The seeded sample of 20000 draws is SIMULATED'.")
row("M4-a-hub-rung2-scale-prompt", "Rung 2 placement prompt states the scale rule as a fact",
    "course/modules/M/M4/index.html (skill check rung 2, prompt and explain block)", "PASS",
    "The stem (index.txt line 72) asserts that multiplying a Student-t variable by s multiplies its variance by s^2 without a hypothesis; the explain block (index.txt line 74) names 'Assumption 1 of this hub (not proved on this page)' and says Lesson 2 proves the scale rule for finite laws only, which matches L02 Prop 2.3 under its finite standing assumption. Accepted as a flagged skill check (judgement, not a failure); the stem is the only unflagged statement.")
row("M4-a-hub-cards-L09-L10-and-text", "Hub card text agrees with L07-L10 current text", "course/modules/M/M4/index.html (cards L07, L08, L09, L10)", "PASS",
    "L07 card: completing the square (L07.txt line 37) and the two-point characteristic function (Prop 2.5, Lab 1). L08 card: Prop 2.1 singular covariance has no inverse. L09 and L10 as in M4-a-hub-objectives-map-ladder.")
row("M4-a-registry-edition", "Registry record and edition statement", "references/references.json (key blitzstein2019introduction); course/modules/M/M4/index.html (Core reading)", "PASS",
    "Registry entry: year 2019, print_year null, no edition key; source_strings holds 'Blitzstein & Hwang, Introduction to Probability, 2nd ed. (2019)' copied from curriculum/01-foundations.yaml line 220. The hub's statement ('no edition field') is accurate; the edition is not confirmed by a structured field.")

# ---- L01 ----
row("M4-a-L01-numbers", "Every number on L01 recomputed exactly",
    "course/modules/M/M4/L01.html (Examples 1.3, 3.5, 3.6; Propositions 2.2, 3.2, 3.4; Lab 1; Misconceptions 1-3; problems M1-M3, E1-E3, R1)", "PASS",
    "Exact Fraction recomputation " + R + "/recheck_r5.py: F values 1/10,3/10,3/5,4/5,9/10,1; Q(1/2)=Q(3/5)=0, Q(61/100)=1, Q(9/10)=2, Q(99/100)=3; ceil(0.99*150)=149 with pn=297/2; ceil(0.99*200)=198; 148/150 = 74/75 = 0.987 displayed; 40*0.901=36.04 gives index 37; F(5)=7/10. All checks OK.")
row("M4-a-L01-proofs", "Proofs of Propositions 2.2, 3.2, 3.4, Remark 3.3 and problems P1-P3",
    "course/modules/M/M4/L01.html (Proposition 2.2 proof; Proposition 3.2 proof; Remark 3.3 proof; Proposition 3.4 proof; problems P1-P3, R1)", "PASS",
    "Each proof read line by line in " + S + "/L01.txt lines 39, 47, 50, 54. Prop 3.2 minimality step and the x_1 <= x case check; Remark 3.3 left-continuity at F_(k-1) handled; Prop 3.4 uses ceil(pn) between 1 and n. P1-P3 solutions verified step by step.")
row("M4-a-L01-lab-1", "Lab 1 hypothesis, interpretation and printed lines",
    "course/modules/M/M4/L01.html (Lab 1 section); tests/labs/M4/lab-M4-L01-1.py", "PASS",
    "The 20 printed lines of the run appear verbatim in the page (lines_in_page.py: 20 of 20). The docstring's claims (scan vs definition on 100 grid points; F(Q(p)) >= p; Q(F(x)) = x at each support point; jumps at F(x)+eps for x = -2..2) match the code and output. Predicted values (L01.txt line 60) recomputed.")
row("M4-a-L01-grades", "Grades of propositions, remarks and key-results table",
    "course/modules/M/M4/L01.html (Propositions 2.2, 3.2, 3.4, Remark 3.3; key results table)", "PASS",
    "All four claim blocks have data-grade='T' and their proofs appear on the page; the key-results table grades them T with 'Proved in §2/§3'; Example 3.5 is 'Arithmetic on the page'.")
row("M4-a-L01-R1-prose", "Problem R1 prose sentence", "course/modules/M/M4/L01.html (problem R1 solution)", "PASS",
    "'For a finite law and p < 1, the strict rule returns x_{k+1} when p = F_k ... agrees with Q at every other p' matches the proof given in the same solution (cases p = F_k and F_(k-1) < p < F_k) and the recomputed Q^s(3/5) = 1.")
row("M4-a-L01-misc-scope", "Scope words and misconception wording on L01 (except misconception 3)",
    "course/modules/M/M4/L01.html ('4 Where the canon breaks', bullet 2; misconception 2 'Proposition 3.2 gives ...')", "PASS",
    "'Four caveats' (L01.html line 275): four bullets follow (" + S + "/L01.txt lines 170-173). 'Every proof here uses a finite list' is true of the page's proofs. Misconception 2 'Proposition 3.2 gives F(Q(p)) >= p, not equality' and the 100-of-100 claim match Lab 1 output line 159-160.")
row("M4-a-L01-R1-strict-claim", "Problem R1 strict-convention claim and proof", "course/modules/M/M4/L01.html (problem R1 solution)", "PASS",
    "Q^s(3/5) = 1 recomputed (F(0)=3/5 is not > 3/5; F(1)=4/5 > 3/5). The general claim for finite laws with p < 1 is proved in the solution by cases; the 'at p = 1 the set is empty' remark is exact.")
row("M4-a-L01-order-statistic-undefined", "Term 'order statistic' used before definition on the slice",
    "course/modules/M/M4/L01.html (bullet 2 of '4 Where the canon breaks'; quiz items for 200 and 150 losses)", "PASS",
    "grep -c 'order statistic' over L01-L04 and index text dumps returns 0 for every page. The term no longer appears.")
row("M4-a-L01-R1-strict-claim-check-index", "Index cases in R1 strict-convention proof", "course/modules/M/M4/L01.html (problem R1 solution)", "PASS",
    "Cases p = F_k (k < m) and F_(k-1) < p < F_k checked; at p = 1 the set {x : F(x) > 1} is empty as stated.")
row("M4-a-L01-misconception-3-rounds", "Misconception 3 and canon bullet 2 agree on the index rule",
    "course/modules/M/M4/L01.html line 297 (misconception 3 'Proposition 3.4 gives the index ... so 148.5 rounds up to 149, not down'); line 278 (canon bullet 'The off-by-one index is a convention error, not a rounding detail.')", "FAIL",
    "Line 297 says '148.5 rounds up to 149'. Ordinary rounding is convention-dependent: " + R + "/extra_checks_r5.py prints round(148.5) = 148 (Python round-half-to-even) and math.ceil(148.5) = 149. Line 278 says the index is 'a convention error, not a rounding detail', so line 297 contradicts it. The result 149 is correct only under the ceiling rule.",
    "Line 297: replace 'so 148.5 rounds up to 149, not down' with 'so the index is the ceiling of 148.5, which is 149, not the floor, 148'.")

# ---- L02 ----
row("M4-a-L02-numbers", "Every number on L02 recomputed exactly",
    "course/modules/M/M4/L02.html (Examples 1.4, 1.5, 2.5, 2.6; Definition 1.6; problems R2, E1-E2; Lab 2 interpretation)", "PASS",
    "recheck_r5.py L02 block: die E=7/2, E[X^2]=91/6, Var=35/12, sd 1.708; loss E=12500, E[L^2]=3125000000, Var=2968750000, sd displayed 54486.24; R2 Var(D)=296875, sd 544.8624; M2 Var 2.25e8, sd 15000; E1 expected count 500, gap 11; die gap -0.031. All OK.")
row("M4-a-L02-lab-2", "Lab 2 hypothesis, docstring, interpretation and printed lines",
    "course/modules/M/M4/L02.html line 263 (Lab 2 interpretation: 'The first block is exact'); tests/labs/M4/lab-M4-L02-1.py", "FAIL",
    "The 10 printed lines appear verbatim (lines_in_page.py 10 of 10). But the first block includes line 6 of " + S + "/lab-M4-L02-1.out, 'standard deviation of the loss in cents: 54486.24', which is math.sqrt(...) printed to two decimals (lab code line: f'{math.sqrt(var_loss):.2f}'). The page's sentence 'The first block is exact' is therefore false for that line. Docstring claims (one seed per law; Var(2X) check; 20-point definitions) match the code.",
    "L02.html line 263: replace 'The first block is exact: the fractions and integers are printed as computed' with 'The fractions and integers in the first block are exact; the standard deviation is a float rounded to two decimals'.")
row("M4-a-L02-P3-R2-problems", "Problems M1-M3, P1-P3, R1-R3 on L02", "course/modules/M/M4/L02.html (problems M1-M3, P1-P3, R1-R3)", "PASS",
    "M1 Var = 21/100; M2 Var 2.25e8, sd 15000; M3 Var(3X-2)=36 and Var(X+10)=4; P2 identity; P3 sides 0 and 2; R1 sample variance identity; R2 Var(D)=296875 and sd factors 1e-4 and 1e-2; R3 Q(1/2)=0 and E=3/10 (all recomputed).")
row("M4-a-L02-quiz-and-misc", "Quiz answers and misconception 3 numbers", "course/modules/M/M4/L02.html (section 7 quiz; section 4 misconceptions)", "PASS",
    "Quiz: E=2, E[X^2]=5 gives Var 1; Var 3 gives Var(2X)=12; loss 5000 and 2.25e8; E[3X-1]=5. Misconception 3: 91/6 about 15.17 and 35/12 about 2.92 (recomputed).")
row("M4-a-L02-section-ref", "Section cross-reference in Uses row", "course/modules/M/M4/L02.html (Uses row, meta)", "PASS",
    "Uses row: 'random variable and its distribution (Lesson 1); definite integral and limit (M2), in the integral form of §1'; the integral form is Definition 1.6 in §1.")
row("M4-a-L02-every-proved", "'Every result is proved' claims on L02", "course/modules/M/M4/L02.html (Definition 1.6; section 8 references; footer)", "PASS",
    "Every proposition is proved on the page; Definition 1.6 states 'No result of this lesson uses this definition', consistent with the claim.")
row("M4-a-L02-second-moment-before-definition", "'Second moment' or 'moment' used before defined on L02", "course/modules/M/M4/L02.html (Lab 2 heading; canon; misconceptions)", "PASS",
    "The prose of L02 uses E[X^2] and never the words 'second moment' or 'moment'; the only occurrence is the Python function name second_moment in the lab code (L02.html lines 189-234).")
row("M4-a-L02-throughout-scope", "Scope of the finite-space standing assumption in section 1", "course/modules/M/M4/L02.html (section 1 opening sentence; Definition 1.6; canon bullet 1)", "PASS",
    "Section 1 opening: 'In §1 and §2, except in Definition 1.6, X is a random variable on a finite probability space with positive weights'. Definition 1.6 is the continuous case and is not used. The canon bullet about E[X^2] is consistent.")
row("M4-a-L02-cross-refs", "Cross-references to other lessons keep their hypotheses (Lesson 6, Lesson 10, Lesson 5)",
    "course/modules/M/M4/L02.html (canon bullet 'The variance needs a finite E[X^2]'; problem P3 'Lesson 5 treats covariance'; misconception 2)", "PASS",
    "Round-4 defect fixed: the bullet now reads 'Lesson 6 (Proposition 2.6, under that lesson's Assumption 1)'; L06.txt Proposition 2.6 is stated under Assumption 1 and gives E[t^2] = infinity for nu <= 2. L05 Proposition 1.1 is the covariance bilinearity that gives Var(X+Y) (L05.txt lines 23-24, 189). Lesson 10 treats heavy tails (L10.txt Definition 1.1).")

# ---- L03 ----
row("M4-a-L03-numbers", "Every number on L03 recomputed exactly",
    "course/modules/M/M4/L03.html (Example 2.5; section 3; section 4; misconceptions; problems M1-M3, E1-E3)", "PASS",
    "recheck_r5.py L03 block: mean 7/4; m2=163/16; m3=2157/32; m4=149461/256; m3 terms -1372/512, -54/512, +1/512, +35937/512; squared skewness 18610596/4330747; kurtosis 149461/26569 displayed 5.6254; skewness displayed 2.0730; Bernoulli p=1/10 gives 64/9 and 73/9 (8.11); p=1/4 gives 7/3 and 2/sqrt(3)=1.155; section 4 law: mean 0, m2 3, m4 15, kappa 5/3; E1 gaps 0.008 and 0.045 from printed three-decimal values. All OK.")
row("M4-a-L03-m3-terms-sentence", "Third-moment term sentence in section 3", "course/modules/M/M4/L03.html (section 3 paragraph)", "PASS",
    "Recomputed: value 10 term 35937/512 exceeds 34512/512; other three terms sum to -1425/512 (two negative, one positive); total 34512/512 = 2157/32.")
row("M4-a-L03-remark-2.6-lesson6-derives", "Remark 2.6 says the page does not derive normal skewness or kurtosis", "course/modules/M/M4/L03.html (Remark 2.6; section 9 references)", "PASS",
    "Remark 2.6 text: 'This page does not define the normal law and does not derive its skewness or kurtosis. No value or result on this page depends on those values'.")
row("M4-a-L03-every-proved", "'Every result is proved' claims on L03", "course/modules/M/M4/L03.html (section 9 references; footer; key results table)", "PASS",
    "Key results table: Prop 1.1, 2.2, 2.3, 2.4 graded T with proofs on the page; the 'Arithmetic on the page' row for the left-skewed law is an exact computation.")
row("M4-a-L03-canon-lessons6-and-10", "Lesson 10 cross-reference keeps Assumption 1", "course/modules/M/M4/L03.html (section 4, bullet 'The moments must be finite')", "PASS",
    "L10.txt Proposition 2.3 is 'Assuming Assumption 1, for the Student-t law V with nu = 3, E[V^4] = infinity'; L03 says 'under its Assumption 1'.")
row("M4-a-L03-uses-quantile", "Uses row and Lesson 2 cross-reference", "course/modules/M/M4/L03.html (meta Uses row, Proposition 1.1 proof, Definition 2.1 cross-reference to Lesson 2 Proposition 2.4)", "PASS",
    "Uses: 'random variable (Lesson 1); expectation and variance (Lesson 2)'. Definition 2.1 cites Lesson 2 Proposition 2.4 for sigma > 0 when X takes two values; L02 Proposition 2.4 is 'Var(X) = 0 iff X takes exactly one value'. Correct.")
row("M4-a-L03-m3-sign-sentence", "Problem M3 sign sentence", "course/modules/M/M4/L03.html (problem M3 solution)", "PASS",
    "m3 = 2157/32 > 0 and sigma > 0 give gamma > 0 (Definition 2.2 and Proposition 2.2). The four terms are recomputed.")
row("M4-a-L03-lab-3", "Lab 3 hypothesis, docstring, interpretation and printed lines",
    "course/modules/M/M4/L03.html (Lab 3 section; section 4 'sample value is an estimate'; interpretation paragraph); tests/labs/M4/lab-M4-L03-1.py", "PASS",
    "All 8 printed lines appear verbatim (lines_in_page.py 8 of 8). Docstring: closed forms for p=1/10, 20000 draws with seed 2026, divisor n: matches code. Interpretation: sample gaps 2.073-2.065=0.008 and 5.625-5.580=0.045 match the printed values.")
row("M4-a-L03-m3-sign-sentence-2", "Canon zero-skew example, kurtosis claims in misconceptions", "course/modules/M/M4/L03.html (section 4; misconceptions 1-3)", "PASS",
    "Law -2,1,3 with 2/5,1/2,1/10: mean 0, m3 0, m2 3, m4 15 (recomputed). Reflection of -2 is 2 which has probability 0, so not symmetric. Sign-reversal claim: gamma_Y = sign(a) gamma_X.")
row("M4-a-L03-prop-2.3-hypothesis", "Proposition 2.3 (affine maps) states the hypothesis its proof needs",
    "course/modules/M/M4/L03.html line 91 (Proposition 2.3 statement 'Let Y = aX + b with constants a != 0 and b'); line 96 (proof divides by sigma_X); line 71 (Definition 2.1: 'Let X take at least two values')", "FAIL",
    "The proof of Proposition 2.3 writes Z_Y = a(X - mu_X)/(|a| sigma_X), which divides by sigma_X; for a constant X, sigma_X = 0 and gamma_X, kappa_X are undefined (Definition 2.1 requires at least two values). The statement omits this hypothesis, though it is graded T (key results row 219). Same omission in card M4-c039 and in quiz item 'Proposition 2.3: kappa is invariant under every affine map with a != 0' (L03.html line 436).",
    "Line 91: replace with 'Let X take at least two values, and let Y = aX + b with constants a != 0 and b.' Then update card M4-c039 and the quiz line to match.")
row("M4-a-L03-quiz-m1-finite-mean", "Retrieval quiz item 'of any law with finite mean' matches Proposition 1.1's hypothesis",
    "course/modules/M/M4/L03.html line 402 (quiz prompt 'What is m_1 ... of any law with finite mean?'); line 58-59 (Proposition 1.1 'For a random variable X on a finite probability space with positive weights')", "FAIL",
    "The answer cites Proposition 1.1, which is stated and proved for a finite probability space with positive weights. The prompt generalises it to any law with finite mean, a claim the page does not prove (the proof uses finite sums). Not a computation on the page.",
    "Line 402: replace 'of any law with finite mean' with 'of a finite law' (or 'of a law on a finite probability space with positive weights').")
row("M4-a-L03-canon-zero-skew-and-R1-R3", "Zero-skewness example, misconceptions, problems R1-R3, quiz answers",
    "course/modules/M/M4/L03.html (section 4; problems R1-R3; misconceptions 1-3; quiz)", "PASS",
    "R1: finite laws with kappa = 1 are exactly the symmetric two-point laws at mu +/- sigma (proof via Lesson 2 Proposition 2.4 applied to W = Z^2, with at least two values). R3 and the quiz answers recomputed.")

# ---- L04 ----
row("M4-a-L04-numbers", "Every number on L04 recomputed", "course/modules/M/M4/L04.html (Example 1.9; Example 2.5; Lab 1 printed lines; problems M1, M2, E1-E3, R1-R3; quiz)", "PASS",
    "recheck_r5.py L04 block: Example 1.9 cell 1/3 vs 1/9 and E[XY]=0; Example 2.5 marginals 2/5, 3/5, E[X]=4/5, E[X|Y=0]=1, E[X|Y=1]=2/3, total 4/5; M1 0.12 vs 0.1; M2 2/3; M3 1/8; E2 ratio 3; E3 ratio 5/8; product cell 3/50. All OK.")
row("M4-a-L04-grade-legend", "Grade legend item C wording on L04", "course/modules/M/M4/L04.html line 47 (ul.grade-legend, grade C)", "PASS",
    "Legend item C reads 'Csingle study or lab result', identical to the standard legend.")
row("M4-a-L04-lab-1", "Lab 1 hypothesis, interpretation and printed lines", "course/modules/M/M4/L04.html (Lab 1 section; interpretation paragraph); tests/labs/M4/lab-M4-L04-1.py", "PASS",
    "All 18 printed lines appear verbatim in the page (lines_in_page.py 18 of 18). The interpretation's statements (Part A independent True/False, cell (0,0) 3/50 and 1/10 vs 4/25; Part B covariance 0 with independence False; Part C values and True lines) match the output. Lab text 'checks three exact tables' matches the code.")
row("M4-a-L04-theorems", "Proofs in sections 1-2 of L04", "course/modules/M/M4/L04.html (sections 1-2)", "PASS",
    "Prop 1.4, 1.5 (changed proof sentence: cells partition the outcomes, grouping as in L02 Proposition 1.2 gives E[XY] = sum xy p(x,y); independence factors the sum), 1.7, 1.8, 2.3 and 2.4 read line by line; each step follows. The L02 Proposition 1.2 analogy is a method reference, not a claim about W = XY.")
row("M4-a-L04-canon-and-links", "Canon bullets and misconceptions on L04", "course/modules/M/M4/L04.html (why-it-matters; section 1 definition paragraph; section 3 bullets 1-4; misconceptions 1-4)", "PASS",
    "Canon: marginals do not fix the joint table (1/2 vs 1/4); X=+-1 with Y=X gives E[XY]=1 vs 0; conditional expectation only for finite tables. Misconceptions 1-4 recomputed.")
row("M4-a-L04-introduces-line", "L04 'Introduces' line lists every concept L04 defines",
    "course/modules/M/M4/L04.html line 39 (Introduces: independence, conditional distribution and conditional expectation (elementary)); line 98 (Definition 1.6 covariance, 'defined here and studied in L05')", "FAIL",
    "Definition 1.6 defines covariance in L04, but the Introduces line omits it. L05.html line 39 lists 'covariance and correlation' as introduced by L05, so covariance is listed as introduced in two lessons. The curriculum's concept is 'Covariance and correlation' (curriculum/01-foundations.yaml line 204).",
    "L04.html line 39: add covariance (the formula, Definition 1.6) to the Introduces list. Cross-slice note for the L05 owner: L05 Introduces should then name only correlation and the covariance matrix, or the Definition 1.6 should move to L05.")
row("M4-a-slice-coverage", "Every page of the slice read in full", "course/modules/M/M4/index.html, L01.html-L04.html, cards.json (L01-L04 entries and M4-c173), tests/labs/M4/lab-M4-L01-1.py .. lab-M4-L04-1.py", "PASS",
    "Full text dumps read: " + S + "/index.txt (102 lines), L01.txt (293), L02.txt (278), L03.txt (273), L04.txt (307). All 67 L01-L04 cards and M4-c173 printed and read (" + S + "/cards_L01_04.txt). All four twins read in full.")
row("M4-a-displayed-digits", "Displayed decimals versus unrounded values", "course/modules/M/M4/L01.html-L04.html, index.html", "PASS",
    "Displayed decimals recomputed from unrounded values: 1.708 (sqrt 35/12), 0.987 (74/75), 2.0730 and 5.6254 (L03 skewness and kurtosis), 8.11 (73/9), 1.155 (2/sqrt3), 0.6667 (2/3), 0.625 (5/8), 544.8624, 54486.24, 15.17, 2.92; all match to the displayed digits.")
row("M4-a-cards-L01-L04", "Cards L01-L04 agree with the CURRENT lesson text and drop no hypothesis",
    "course/modules/M/M4/cards.json (entries with lesson L01-L04); M4-c039 at cards.json line 271; lesson text at L03.html line 91", "FAIL",
    "Round-4 defect fixed: M4-c007 now reads 'used in this lesson', matching L01 Definition 3.1. All other L01-L04 cards agree with the current text (checked one by one; " + R + "/extra_checks_r5.py prints the cards). Duplicate scan over all 180 M4 cards: no duplicate ids, no duplicate fronts. But M4-c039 ('How do skewness and kurtosis change under Y = aX + b with a not zero?') drops the at-least-two-values hypothesis that Prop 2.3's proof needs (see M4-a-L03-prop-2.3-hypothesis).",
    "Add 'Hypothesis: X takes at least two values.' to the back of M4-c039 once the Proposition 2.3 statement is fixed.")
row("M4-a-dag-closure", "Prerequisite closure of links and concepts on the slice", "course/modules/M/M4/index.html (Prerequisites paragraph); L01-L04 data-concept links", "PASS",
    "check_dag M4 PASS. Links on the slice: index quantifiers, exponential-and-logarithm, limit, definite-integral (M1, M2: in the closure). L01-L04 link M4 concepts (random-variable, quantile-function, expectation, variance, skewness, kurtosis, independence, conditional-expectation-elementary) defined on those pages. 'moment' is plain prose (Architect Q3). No M3 concept is used.")

frag = {
    "unit": "M4",
    "slice": "M4-a",
    "round": 5,
    "verifier": "Haiku independent verifier, round 5, slice M4-a (hub index.html, L01-L04 pages, cards L01-L04 in cards.json, lab twins L01-L04). Did not build M4; shares no context with the builders.",
    "pin": "09b8751",
    "base": "2657ab5 (round-4 pin). Delta: git diff 2657ab5 09b8751 changed index.html, L01.html, L02.html, L03.html, L04.html and cards.json (M4-c007 and L06-L10 entries). Lab twins L01-L04 unchanged since 2657ab5.",
    "checkout": "/tmp/verifyB5-M4-a (detached at 09b8751, .venv symlinked)",
    "scratch": S,
    "verified_at": "2026-10-28",
    "verdict": "FAIL",
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Carried rows: none. Every cited file changed or was re-read in full this round, so each row was re-verified from scratch (VERIFIER_RULES carry rule not applied; the prefix would have been inaccurate for changed files).",
        "Round-4 FAIL rows: M4-a-L02-cross-refs is now PASS (Lesson 6 Proposition 2.6 Assumption 1 restored in L02). M4-a-cards-L01-L04 is FAIL again, now for M4-c039 (a new finding on an unchanged card: it drops the at-least-two-values hypothesis of Proposition 2.3, which round 4 did not check).",
        "New round-5 FAIL rows: M4-a-L01-misconception-3-rounds, M4-a-L02-lab-2, M4-a-L03-prop-2.3-hypothesis, M4-a-L03-quiz-m1-finite-mean, M4-a-L04-introduces-line. Each has a fix in its fix field.",
        "Mutation testing and alternative implementations are not applicable: the slice has no project grader (ARCHITECT RULING: lab twins are demonstrations). mutants is empty.",
        "Judgement, not failed: M4-a-hub-rung2-scale-prompt (stem asserts the scale rule for a Student-t variable; the explain block flags Assumption 1).",
        "Not checked: the Blitzstein book (no content was fetched; no DOI or publisher page was requested, so no HTTP status is recorded). No bot check or access block was encountered or bypassed. Lab twins for L05-L10 and the project are outside this slice.",
        "Scripts: ledgers/M4/scripts/M4-a-r5/dump_text.py (text dumps), lines_in_page.py (printed lines verbatim), recheck_r5.py (exact Fraction recomputation; 98 checks, all OK), extra_checks_r5.py (round(148.5); card duplicate scan; cards with changed text). The fragment is built by ledgers/M4/scripts/M4-a-r5/build_fragment_r5.py.",
    ],
    "summary": "",
    "rows": P,
}
nonpass = [r["id"] for r in P if r["status"] != "PASS"]
frag["summary"] = (f"M4-a round 5: {len(P)} rows; {len(P) - len(nonpass)} PASS, {len(nonpass)} FAIL "
                   f"({', '.join(nonpass)}). Verdict FAIL.")
json.dump(frag, open("ledgers/M4/M4-a.json", "w", encoding="utf-8"), indent=2, ensure_ascii=False)
print("rows", len(P), "fails", len(nonpass))
