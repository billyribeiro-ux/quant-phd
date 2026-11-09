"""Writes the round-2 fragment for unit M4, slice c (L08 to L10 pages, lab twins, cards). Verifier-authored."""
import json
import pathlib
import sys

ROOT = pathlib.Path(sys.argv[1]).resolve()
S = "ledgers/M4/scripts/M4-c-r2/"
P = []


def row(rid, check, location, status, evidence, fix=None):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    P.append(r)


# ---------- commands and gates (re-run on pin 9294b914) ----------
row("M4c2-CMD-CHECK-PAGES", "tools/check_pages.py --unit M4", "structure, banned phrases, lab ids, card presence, hours",
    "PASS", f"Run on pin: exit 0, output 'check_pages M4: PASS' ({S}check_pages_M4_r2.txt).")
row("M4c2-CMD-CHECK-DAG", "tools/check_dag.py --unit M4", "DAG of M4 pages", "PASS",
    f"Run on pin: exit 0, 'check_dag M4: PASS' ({S}check_dag_M4_r2.txt). Manual read of concept links on L08-L10 "
    "(each dfn once; links point to earlier lessons or M1/M2/M4 prerequisites) found no fault except the non-dfn "
    "covariance link row M4c2-DAG-COVARIANCE-LINK.")
row("M4c2-CMD-CHECK-PROJECTS", "tools/check_projects.py --unit M4", "unit-level project checks (outside slice; run as a gate)",
    "PASS", f"Run on pin: exit 0, 'check_projects M4: PASS' ({S}check_projects_M4_r2.txt).")
row("M4c2-CMD-RUN-LABS", "tools/run_labs.py --unit M4 --page L08 / L09 / L10 and --unit M4", "lab-M4-L08-1, lab-M4-L09-1, lab-M4-L10-1",
    "PASS", f"Each page: exit 0, 'run_labs M4: PASS (1/1)'. Unit: 'run_labs M4: PASS (13/13)' ({S}run_labs_L08.txt, "
    f"run_labs_L09.txt, run_labs_L10.txt, run_labs_M4_all.txt).")
row("M4c2-CMD-TWIN-ISOLATED", "python -I -W error tests/labs/M4/lab-M4-L0{8,9,10}-1.py (cwd /tmp)",
    "tests/labs/M4/lab-M4-L08-1.py, lab-M4-L09-1.py, lab-M4-L10-1.py", "PASS",
    f"Each twin exit 0, stderr 0 bytes; stdout 9, 13 and 29 lines; saved to {S}twin_L08_r2.txt, twin_L09_r2.txt, twin_L10_r2.txt "
    f"(produced by {S}check_twin_match_r2.py).")
row("M4c2-CMD-CODE-EQ-TWIN-AND-EXPECTED", f"{S}check_twin_match_r2.py (python -I)",
    "course/modules/M/M4/L08.html:126-233, L09.html:153-270, L10.html:171-361", "PASS",
    f"Output in {S}check_twin_match_r2.out: L08, L09 and L10 'code_equals_twin=True'; 'expected_equals_output=True' for each.")
row("M4c2-CMD-PAGE-SMOKE", "tools/page_smoke.py --unit M4 --pages L08 L09 L10", "L08.html, L09.html, L10.html", "PASS",
    f"Exit 0; 'page_smoke modules/M/M4/L08.html: PASS', L09 PASS, L10 PASS, 'page_smoke M4: PASS' ({S}page_smoke_L08-L10_r2.txt). "
    "Lab runtimes 0.1, 0.4, 0.3 s in Pyodide. Light/dark and 360 px checks are page_smoke's; no screenshot taken by me.")
row("M4c2-CMD-RUFF", "ruff check and ruff format --check on tests/labs/M4 and course/modules/M/M4; repo ruff check . and format --check .",
    "tests/labs/M4/*.py", "PASS",
    f"'All checks passed!', '13 files already formatted'; repo 'All checks passed!' and '553 files already formatted' "
    f"({S}ruff_check_M4_r2.txt, ruff_format_M4_r2.txt, ruff_check_repo_r2.txt, ruff_format_repo_r2.txt).")
row("M4c2-CMD-MYPY", ".venv/bin/mypy --no-incremental (repo config, files = tools, tests)", "pyproject.toml; tests/labs/M4", "PASS",
    f"'Success: no issues found in 385 source files' ({S}mypy_r2.txt).")
row("M4c2-CMD-PYTEST-RELEVANT", "pytest tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py -q", "lab and page-check suites",
    "PASS", f"Exit 0, all progress lines dots, 100% ({S}pytest_relevant_r2.txt).")
row("M4c2-CMD-VERIFY-REFS", "tools/verify_refs.py --offline", "references/references.json (560 entries)", "PASS",
    f"'offline integrity: 560 entries, 0 problems' ({S}verify_refs_offline_r2.txt). No citation changed in the slice; live run not needed.")
row("M4c2-CARD-INTEGRITY-SCRIPT", f"{S}cards_check_r2.py", "course/modules/M/M4/cards.json (213 cards, 69 in L08-L10)", "PASS",
    f"{S}cards_check_r2.out: 0 duplicate ids, 0 duplicate fronts; per-lesson L08 16, L09 26, L10 27; all grades in T/A/B/C/D/X; "
    "every non-T slice card has a basis; the three unmatched tokens 1/2, 1/4, 3/4 are TeX \\tfrac in the lesson text.")

# ---------- numbers, recomputed independently ----------
row("M4c2-NUM-L08", f"{S}numbers_L08_L10_r2.py (L08 block)", "L08.html:124, :128, :130-232, :336 (E3), :320-337 (E1, E2)", "PASS",
    f"Independent run ({S}numbers_L08_L10_r2.out): AA^T=((4,2),(2,2)); B=AQ=((0,-2),(1,-1)), BB^T=Sigma; A^TA=((5,1),(1,1)); "
    "A^TA-Sigma=((1,-1),(-1,-1)); seed-2026 mean (0.977, -2.0055); cov X ((4.0073,2.0187),(2.0187,1.9936)); gap 0.0187 and 1.0187; "
    "cov Y ((3.907,1.9385),(1.9385,1.9636)); gap 0.093. All printed values and E1/E2 gaps reproduce.")
row("M4c2-NUM-L09", f"{S}numbers_L08_L10_r2.py (L09 block)", "L09.html:256-268 (expected), :269, :275-277, :286, :290, :309, :323, :359, :366-367, :373", "PASS",
    f"Independent run ({S}numbers_L08_L10_r2.out): exact die-sum probabilities 0.833333, 0.847994, 0.843496, 0.835793, 0.833926 "
    "at thresholds 5, 21, 40, 77, 150 with Fraction arithmetic; Phi(1)=0.841345; path means 3.8000, 3.8100, 3.6090, 3.4689; Chebyshev "
    "1.1667, 0.1167, 0.0117, 0.0012; MC hits 3421, 3419, 3407 of 4000 (est 0.8552, 0.8548, 0.8518; se 0.0056). E2: 0.85525 "
    "gives se 0.005563 and ratio 2.50. E1: 40.4006. M1 7/60, M2 35/48, M3 bound 2. All reproduce.")
row("M4c2-NUM-L10", f"{S}numbers_L08_L10_r2.py (L10 block)", "L10.html:331-359 (expected), :360, :366-368, :377, :381, :385, :407, :414, :450, :457, :464", "PASS",
    f"Independent run ({S}numbers_L08_L10_r2.out): midpoint and closed form of F_V(2)-F_V(-2) both 0.860674031; P(|C|>10)=0.063451; "
    "P(|V|>10)=0.002128 (also by a midpoint integral on [10,2000] doubled); erfc(10/sqrt2)=1.5240e-23; ratio 4.1635e21; Part D "
    "0.634510/0.636599/0.636620 and 2.128399/2.204522/2.205308; limits 2/pi=0.636620, 4sqrt3/pi=2.205316; running means for seeds "
    "2026/2027/2028 (normal -0.2212..+0.0031, t3 -0.1397..-0.0235, Cauchy -57.9246..+0.9919); IQR 0.4116, 0.1279, 0.6121, 0.2302, "
    "1.8220, 1.8838; variances 1.0211, 0.9396, 0.8807, 1.1987; exact Cauchy IQR 2.0; F_V(sqrt3)=3/4+1/(2pi)=0.909155. All reproduce.")
row("M4c2-MATH-L08", "re-derivation of L08 Props 1.1, 1.3, 1.6, 2.1, Remark 1.4, Example 1.5, Section 4, M1-M3, P1-P3, R1-R3, E1-E3, quiz keys",
    "course/modules/M/M4/L08.html:55-120, :262-365, :369-383, :387-461", "PASS",
    "Re-derived each proof by hand: Prop 1.1 product rule via positive/negative parts (Lesson 6 Remark 2.2); Prop 1.3 "
    "linearity; Remark 1.4 (AQ)(AQ)^T=AA^T; Prop 1.6 transpose argument; Prop 2.1 (u=A^Tw, u^Tu=0 forces Sigma w=0); "
    "Example 1.5 quadratic form (2w1+w2)^2+w2^2; R1 lower-triangular uniqueness a=2,b=1,c=1; R3 evenness; Section 4 "
    "P(X+Y=0)>=1/2 and P(X+X'=0)=0; quiz numeric answers 4, 2, 5, 10, 0.5 match.")
row("M4c2-MATH-L09-THEOREMS", "re-derivation of L09 Props 1.1, 2.1, 2.2, 2.3, Thm 1.3, Defs 1.4, 2.4, Section 3 and misconceptions",
    "course/modules/M/M4/L09.html:57-148, :102-141, :156-268, :275-296", "PASS",
    "Chebyshev indicator bound; Theorem 1.3 from Prop 1.1 with v=sigma^2/n and 1/n -> 0; Prop 2.2 bounds f(x)=cos x-1+x^2/2 "
    "and g(x)=sin x-x (|f|+|g| <= 5|x|^3/24 <= |x|^3/3 for |x|<=1); Prop 2.3(b) telescoping and b_n^n -> e^{-t^2/2} with "
    "n ln(1-x/n) -> -x; Section 3 jump argument; misconception numbers 0.30/0.31 and 0.0139 match the output.")
row("M4c2-MATH-L10-THEOREMS", "re-derivation of L10 Props 1.3, 1.4, 1.5(a)-(c), 1.7, 2.1, 2.3, Remark 2.2, Defs 1.1, 1.2, 2.4, Assumptions 1-3",
    "course/modules/M/M4/L10.html:79-169, :391-493", "PASS",
    "F_V derivative sums to 2/(sqrt3(1+x^2/3)^2) (Prop 1.3); P(|V|>x) closed form equals 2(1-F_V(x)) (Prop 1.4); h'(u)=u^4/(1+u^2) "
    "gives arctan u >= u - u^3/3; (2/pi)(1/x - 1/(3x^3)) >= 1/(pi x) for x>=1; f_V >= 9/(4t^4) factor and integral sqrt3/(2 pi x^3) "
    "(Prop 1.5b); Chernoff with s=x gives P(Z>x) <= e^{-x^2/2} (Prop 1.5c); Prop 1.7 expansion (2/3)y^3 gives 4sqrt3/pi; "
    "Prop 2.1 E|C| and E[C^2] infinite; Prop 2.3 integrand >= 3sqrt3/(2 pi t^4) gives E[V^4]=infinity; R1 c=1/2; R2 E|V|^3 infinite; "
    "E1-E3 and M1-M3 solutions re-derived.")
row("M4c2-MATH-L10-R2-CHECK", "L10 Remark 2.2 and Lesson 6/7 cross-references",
    "course/modules/M/M4/L10.html:66, :76, :104, :112, :146; course/modules/M/M4/L06.html Def 2.5, Prop 2.6; L07.html Prop 1.3", "PASS",
    "Verified in L06.html: Definition 2.1 (chi-square as sum of squares), Definition 2.5 (Z/sqrt(W_nu/nu), W independent of Z), "
    "Proposition 2.6 (variance nu/(nu-2) under Assumption 1), Proposition 1.5 (E Z=0, E Z^2=1), Remark 2.2 (product rule for "
    "nonnegative functions); L07.html Proposition 1.3 (normal MGF exp(mu t + sigma^2 t^2/2)). grep for a Student-t density in "
    "L06.html returns no formula, so the Assumption 1 statement at L10:66 is accurate.")

# ---------- lab claims vs code and output ----------
row("M4c2-LAB-CLAIMS-L08", "hypothesis and interpretation vs code and output", "L08.html:51, :128, :129-140, :232, :223-231", "PASS",
    "Docstring (twin lines 2-12) matches the code: exact Part A, seeded Part B with n=20000 and gauss pairs, the same Z for X and Y, "
    "divisor n-1. Predicted Part A lines match the output; the 'closer to Sigma than A^TA' prediction holds (0.0187 vs 1.0187). "
    "'Does not test joint normality' is true of the code.")
row("M4c2-LAB-CLAIMS-L09", "hypothesis and interpretation vs code and output", "L09.html:51, :155, :156-168, :269, :290", "PASS",
    "Part A uses Fraction convolution and floor of 3.5n+sqrt(35n/12), matching the printed thresholds; Part B seeded path with "
    "checkpoints 10, 100, 1000, 10000 and Chebyshev bound with eps=0.5; Part C reseeds 2026 per size (rng created inside loop, "
    "matching 'restart the seed' at :269). 'Prints no spread of the sample mean' is true (Part C prints SE of an estimate).")
row("M4c2-LAB-CLAIMS-L10", "hypothesis and interpretation vs code and output", "L10.html:173, :360, :366-368, :377, :381, :385; twin docstring lines 1-14", "PASS",
    "Seeds 2026, 2027, 2028 for Part B and seed+100n in Part C as coded; Part A prints the 1e-8 agreement as True; IQR and variance "
    "figures match the output. The revised sentence at :360 ('below that value in this run', 1.8220 and 1.8838 < 2) is true. "
    "The docstring sentence 'about six significant digits are lost' is consistent with a difference of about 2e-6 times each term.")
row("M4c2-GRADES", "re-grade of every graded span and key-results row (BLUEPRINT section 3)",
    "L08.html:373-380; L09.html:410-419; L10.html:501-513", "PASS",
    "Theorems and derivations are T and proved on the page, or are closed-form evaluations (T with basis). Lab Part B and Part C rows are C "
    "with a SIMULATED basis. The erfc row is C with a stated library basis (L10.html:510). No B or C claim omits a published counter-source "
    "(no registry key is cited for a grade in the slice). Assumption 3 is handled in row M4c2-GRADE-ASSUMPTION3.")
row("M4c2-STRUCTURE", "section order, minimum counts, hours, quiz sizes, why-it-matters length",
    "L08.html, L09.html, L10.html", "PASS",
    "Order: why-it-matters, core sections, lab inside core, canon breaks, misconceptions (3 each), problem set (3 per tier), key results, "
    "quiz (L08 10 items, L09 8, L10 10), references, complete button, nav. data-hours=9 on each page. why-it-matters 89, 118, 67 words (<=120).")
row("M4c2-PROSE-SCOPE-WORDS", "scope words and banned phrases in visible prose", "L08.html, L09.html, L10.html", "PASS",
    "check_pages BANNED scan passes. Scope words checked: 'heavy'/'heavier' (L10:366, :377, :120) are backed by 4.164e21 and 0.063451 on "
    "the same page; 'large' (L10:377) by the same numbers; 'close to sqrt10' (L10:368) by 3.2 vs 3.16; 'every' and 'only' are "
    "logical or existential statements, not numerical claims.")
row("M4c2-NOTATION", "symbols vs notation/notation.json", "L08.html, L09.html, L10.html", "PASS",
    "Registered symbols used: Phi (L09.html:51, :147, :416; L10.html:366) is the standard normal CDF, as registered. T, gamma_3, "
    "gamma_4, R^ast do not occur in the slice. Macros used are raw LaTeX (\\operatorname, \\Sigma, \\varphi), none unregistered. "
    "Note (not a row): phi is the standard normal density in L06 and L08 and the characteristic function phi_X in L07 and L09; "
    "the two uses are never on one page, and phi is not a registered symbol.")
row("M4c2-REFS", "citations and data attributes in the slice", "L08.html:463-466; L09.html:488-491; L10.html:596-600", "PASS",
    "No data-cite or data-locator attribute on the three pages (grep). The only registry key named is blitzstein2019introduction, "
    "with the statement that no passage was read; no claim is attributed to it. No DATA_REQUESTS or data-files in the slice.")

# ---------- round-1 FAIL rows, re-verified ----------
row("M4c2-PRIOR-DEF-L10-INDEP", "round-1 FAIL: W independent of Z stated where Lesson 6's t is used",
    "course/modules/M/M4/L10.html:66, :76; tests/labs/M4/lab-M4-L10-1.py lines 4-6", "PASS",
    "Both sentences now state 'with W independent of Z (Lesson 6, Definition 2.5)'. Twin docstring lines 5-6 now say 'W independent of Z'. "
    "Re-read on pin; the page code block equals the twin (M4c2-CMD-CODE-EQ-TWIN-AND-EXPECTED).")
row("M4c2-PRIOR-HYP-STATEMENTS", "round-1 FAIL: derivation statements omit the proposition's hypothesis",
    "course/modules/M/M4/L08.html:277, :295, :352; course/modules/M/M4/L10.html:397, :447", "PASS",
    "L08 M2, P1 and R2 now begin 'Assuming Lesson 6's Assumption 1'; L10 M1 and E1 now begin 'Assuming Assumption 2'. "
    "The E3 statement on L10 is a new, separate defect (row M4c2-HYP-E3).")
row("M4c2-PRIOR-KEYROW-L10-ERFC", "round-1 FAIL: key-results source for the normal tail",
    "course/modules/M/M4/L10.html:510", "PASS",
    "The row is now graded C with basis 'library value of erfc(10/sqrt2); the identity P(|Z|>x)=erfc(x/sqrt2) is not derived on this page'. "
    "The source now matches the code path (tests/labs/M4/lab-M4-L10-1.py, math.erfc).")
row("M4c2-PRIOR-CARD-TRIVIA", "round-1 FAIL: cards that ask for one printed number from a seeded run",
    "course/modules/M/M4/cards.json", "PASS",
    "The 23 round-1 cards (M4-c126, c143, c162, c165 to c172, c185, c188 to c190, c233 to c240) are no longer in the file; the slice has 69 cards "
    "(M4-c114 to M4-c256). Remaining printed-number cards (M4-c161, c251) carry a concept and a comparison (2/pi limit; the Cauchy range vs 2) and are kept.")

# ---------- cards ----------
row("M4c2-CARD-SAMPLE-L08", "10-card sample plus full read of the 16 L08 cards", "cards.json M4-c114, c115, c116, c117, c118, c119, c120, c121, c122, c125, c175, c176, c207, c208, c231, c246",
    "PASS", "Each back checked against L08.html: Definition 1.2 (c116), Prop 1.1 (c115), Prop 1.3 (c117, c231), Remark 1.4 with its "
    "hypothesis (c118), Example 1.5 numbers (c119, c207, c208), Prop 1.6 (c120), Prop 2.1 (c121), Section 4 (c122), P3 (c125), "
    "Section 1 and 3 definitions (c175, c176), lab sample (c246, C with basis).")
row("M4c2-CARD-SAMPLE-L09", "10-card sample plus full read of the 26 L09 cards", "cards.json M4-c127 to c218, c247 to c250, c256",
    "PASS", "Hypotheses checked against L09.html: c128 and c217 (Prop 1.2), c129 (Thm 1.3), c131 (text after Thm 1.3), c132 (Prop 2.1), "
    "c133 (Prop 2.2), c134 (Prop 2.3(a)), c218 (Prop 2.3(b) with Assumption 1); c137 (Problem M3 bound 2); c142 (Problem E1, 40); "
    "misconceptions c138 to c140; lab cards c247 to c250 and c256 with C grades and bases.")
row("M4c2-CARD-SAMPLE-L10", "10-card sample plus full read of the 27 L10 cards", "cards.json M4-c144 to c161, c180, c186, c187, c209, c232, c251 to c255",
    "PASS", "Checked against L10.html: Def 1.1 (c144), Def 1.2 (c145, c209), Props 1.3 to 1.7 (c146 to c151, c186, c187, c232), "
    "Prop 2.1 (c152), Remark 2.2 (c153), Prop 2.3 (c154), Def 2.4 (c155), misconceptions (c157 to c159), P2 (c160), "
    "E1 (c161), lab cards (c251 to c255 with C or T and bases).")
row("M4c2-CARD-DUPLICATES", "full-file duplicate scan", "course/modules/M/M4/cards.json (213 cards)", "PASS",
    f"{S}cards_check_r2.out: 0 duplicate ids, 0 duplicate fronts; token-Jaccard >= 0.45 pairs involving slice cards (e.g. c128/c217, "
    "c119/c207, c147/c149) are distinct facts (mean vs variance, A^TA vs AA^T, distribution function vs tail).")
row("M4c2-CARD-COVERAGE", "every definition, theorem, key formula, key result and misconception has a card", "cards.json vs L08-L10",
    "PASS", "L08: defs c114, c116, c175, c176; Prop 1.1 c115; Prop 1.3 c117, c231; Remark 1.4 c118; Example 1.5 c119, c207, c208; "
    "Prop 1.6 c120; Prop 2.1 c121; misconceptions c118, c122, c231. L09: defs c130, c136, c177 to c179; Props c127, c128, c132 to c134, "
    "c217, c218; Thm 1.3 c129; misconceptions c138 to c140; lab c247 to c250, c256. L10: defs c144, c145, c155, c180, c209; Props c146 to "
    "c154, c186, c187, c232; misconceptions c157 to c159; lab c251 to c255.")
row("M4c2-CARD-HYPOTHESES", "cards carry their proposition's hypotheses", "cards.json", "PASS",
    "c117, c118 (Lesson 6 Assumption 1); c133, c134 (finite values; sigma^2 > 0); c128, c129, c217 (identically distributed, pairwise "
    "independence, finite variance); c146, c148, c150, c151 (Assumption 2); c147, c149, c154, c187, c209, c218, c232 (Assumption 1 and/or 2 as "
    "named). Each matches its lesson statement.")
row("M4c2-CARD-NUMBERS", f"every card number appears in its lesson ({S}cards_check_r2.py)", "cards.json slice backs", "PASS",
    f"{S}cards_check_r2.out: no decimal or 2+ digit token is missing from its lesson; the three fraction tokens are TeX \\tfrac in the "
    "lesson text.")
row("M4c2-CARD-TRIVIA", "cards are atomic and not trivia (VERIFIER_RULES 2.7)", "cards.json M4-c161, c251, c255", "PASS",
    "No slice card asks the learner to recall a single seeded-run value. c161 (closed-form value at x=10 and its gap to 2/pi) and "
    "c255 (what Part D evaluates) are kept as lab-design or closed-form facts; c251 is a shrinkage question with C grade and basis.")

# ---------- FAIL rows ----------
row("M4c2-PROOF-PROP12-GAP", "Proposition 1.2 proof and the claim that it needs no finitely-valued hypothesis",
    "course/modules/M/M4/L09.html:55 (claim), :74 (proof); course/modules/M/M4/L10.html:169 (claim); L10.html:464 (E3 uses it)",
    "FAIL",
    "L09.html:74 proves E[(X_i-mu)(X_j-mu)] = E[X_i-mu]E[X_j-mu] for i != j 'by independence (Lesson 4)'. Lesson 4's independence "
    "is Definition 1.2 (L04.html, 'Discrete random variables X and Y are independent when p(x,y)=P(X=x)P(Y=y)'), i.e. finitely or discretely "
    "valued laws only. Proposition 1.2 is stated for general identically distributed laws with finite variance, and L09:55 says it "
    "'needs only ... pairwise independence', L10:169 says it 'needs no finitely-valued hypothesis', and L10:464 applies it to the "
    "continuous Student-t law V. The product rule for general independent integrable variables is not stated on the page: L06 "
    "Remark 2.2 covers nonnegative functions only. L08 Proposition 1.1 closes exactly this gap by splitting into positive and "
    "negative parts; L09 does not.",
    "Either (a) in the proof of Proposition 1.2, cite Lesson 6 Remark 2.2 (under its Assumption 1(d)) and add the positive/negative-part "
    "step for the signed factors X_i-mu and X_j-mu (each has finite expectation because its second moment is finite), replacing "
    "'(Lesson 4)'; or (b) restrict Proposition 1.2 and Theorem 1.3's pairwise-independence use to discrete laws and delete "
    "'needs only' at L09:55 and 'needs no finitely-valued hypothesis' at L10:169, and remove the claim that Problem E3 applies it to V.")
row("M4c2-HYP-E3", "Derivation statement omits the hypothesis of the value it asks for",
    "course/modules/M/M4/L10.html:462 (E3 prompt), :464 (solution)", "FAIL",
    "E3 asks for 'the value that the finite-variance calculation of Lesson 9 gives' for Var(sqrt(n) Xbar_n / sqrt3), whose value 1 needs "
    "Var(V) = 3. The solution takes Var(V) = 3 from Remark 2.2, which is Lesson 6, Proposition 2.6 under Lesson 6's Assumption 1. The "
    "prompt does not state that assumption, and it relies on the Proposition 1.2 step flagged in M4c2-PROOF-PROP12-GAP.",
    "Change the E3 prompt to begin 'Assuming Lesson 6's Assumption 1, ...' (or add 'and Remark 2.2' with its hypothesis) so that the "
    "value 1 is stated under the hypotheses it uses.")
row("M4c2-HYP-SEC4-EXAMPLE", "Example in Section 4 uses Lesson 6 facts without stating Assumption 1",
    "course/modules/M/M4/L08.html:238", "FAIL",
    "The normal-margins example takes X standard normal and uses the density phi, the product rule for independent variables "
    "(Cov(X,Y)=E[eps X^2]=E[eps]E[X^2]=0, and the joint density phi(x)phi(x') of (X,X')), and the symmetry of the normal law. These "
    "rely on Lesson 6's Assumption 1 (d) and Proposition 1.5. The example and the section opening (L08.html:110) do not state that "
    "hypothesis, although the rest of the page does (Propositions 1.1, 1.3, Remark 1.4).",
    "Add 'Assuming Lesson 6's Assumption 1,' at the start of the Section 4 example (L08.html:238), or add the same sentence to the "
    "section opening at L08.html:110.")
row("M4c2-DAG-COVARIANCE-LINK", "concept link target for 'covariance' in the Uses lines",
    "course/modules/M/M4/L08.html:37; course/modules/M/M4/L09.html:37", "FAIL",
    "The Uses line says 'covariance (Lesson 5)' but links to L05.html#def-correlation, which defines correlation. Covariance is defined in "
    "Lesson 4, Definition 1.6 ('defined here and studied in L05'), which carries no id, so no anchor exists for it. The link does not "
    "lead to the definition named by its label.",
    "Change the text to 'covariance (Lesson 4, Definition 1.6)' and link to L04.html (page), or add an id to L04 Definition 1.6 and link "
    "to it. Do not link to def-correlation.")
row("M4c2-GRADE-ASSUMPTION3", "Ungraded substantive claim where the plan specifies grade D",
    "course/modules/M/M4/L10.html:165-166 (Assumption 3 remark, 'gives it no grade'); :508 (key row 'not graded')", "FAIL",
    "plans/M4-build-plan.md, section 'Lesson content guidance', L10 item, says the stable-limit statement is 'graded D until a source is "
    "admitted'. The page gives it no grade in both places. BUILDER_RULES section 2.1 requires every substantive claim to carry a grade; "
    "the statement is a substantive claim (the Cauchy sample mean is Cauchy for every n). This is a plan deviation, not a numerical error.",
    "Grade the Assumption 3 remark D (span.claim data-grade='D', with the text 'no source admitted') and change the key-results row "
    "at L10.html:508 to grade D, or record the architect's ruling that grade is withheld.")

for r in P:
    r.setdefault("fix", None)
    if r["status"] == "PASS":
        r.pop("fix", None)

nonpass = [r for r in P if r["status"] != "PASS"]
frag = {
    "unit": "M4",
    "slice": "c",
    "round": 2,
    "verifier": "Haiku 5.5 independent verifier, unit M4 slice c (L08-L10 pages, lab twins, cards), round 2",
    "pin": "9294b914a51647c66d2dee62c4a112c76ba04900",
    "base": "aeb512b65b7774b59b84f836a13984fcfe9d0d1f (round-1 pin; delta read in full for slice files)",
    "checkout": str(ROOT),
    "scratch": str(ROOT / S.rstrip("/")),
    "verified_at": "2026-11-08",
    "verdict": "FAIL" if nonpass else "PASS",
    "rows": P,
    "mutants": [],
    "registry_flags": [
        "blitzstein2019introduction: no locator read and none cited; the 2nd ed. claim is unconfirmed (no edition field), as in plan Q6."
    ],
    "freshness_flags": [],
    "notes": [
        "Delta since round-1 pin aeb512b6: L08.html (4 hunks), L09.html (2 hunks), L10.html (about 10 hunks), cards.json (239-line change), "
        "tests/labs/M4/lab-M4-L08-1.py, lab-M4-L10-1.py. Every changed hunk in the slice was read; L09 twin unchanged.",
        "All round-1 rows were re-run or re-derived on the new pin; none carried forward.",
        "Lab twins are demonstrations (ruling): no mutants written. Slice has no project grader.",
        "Pre-existing tracked files ledgers/M4/scripts/M4-c-r2/page_text.py and recheck_L08_L10_r2.py (commit aa3c26c5) were not used as evidence; my scripts have distinct names.",
        "Not checked: hub index.html and L01-L07 (outside slice); project.html and grader (outside slice); repo-wide check_pages --all, build_site, render_curriculum (architect gates); fetch_data (no data in slice); live Crossref (no citation changed); Blitzstein locators (book not read); visual screenshots (page_smoke only).",
        "Observation outside slice: L06.html:275 and :284 refer forward to L10 (round-1 note; not a concept link, check_dag passes).",
    ],
}
frag["summary"] = {
    "rows": len(P),
    "pass": sum(1 for r in P if r["status"] == "PASS"),
    "fail": sum(1 for r in P if r["status"] == "FAIL"),
    "unverifiable": sum(1 for r in P if r["status"] == "UNVERIFIABLE"),
    "mutants_killed": 0,
    "mutants": 0,
}
out = ROOT / "ledgers/M4/M4-c.json"
out.write_text(json.dumps(frag, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out, frag["summary"], frag["verdict"])
