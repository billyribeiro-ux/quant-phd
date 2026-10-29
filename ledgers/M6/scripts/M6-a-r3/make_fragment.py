"""Write the round-3 verifier fragment for M6 slice a (hub index.html, L01-L04 and their lab twins)."""
import json
import pathlib
import sys

ROOT = pathlib.Path(sys.argv[1])
P = "PASS"
F = "FAIL"
U = "UNVERIFIABLE"
CMD = "run: "

rows = [
    # --- commands (run by this verifier at pin ccfdf4c) ---
    dict(id="CMD-check_pages", check="tools/check_pages.py for hub, L01-L04 and unit", location="course/modules/M/M6/index.html, L01-L04.html, cards.json",
         status=P, evidence=CMD + "check_pages.py --unit M6 --page L01..L04 and --unit M6: every line 'PASS', exit 0"),
    dict(id="CMD-check_dag", check="tools/check_dag.py --unit M6 (concept usage, prerequisite closure)", location="all M6 pages",
         status=P, evidence=CMD + "check_dag.py --unit M6: 'check_dag M6: PASS', exit 0"),
    dict(id="CMD-run_labs", check="tools/run_labs.py --unit M6 --page L01..L04", location="labs in L01-L04",
         status=P, evidence=CMD + "run_labs M6: PASS (1/1) for each of L01, L02, L03, L04, exit 0"),
    dict(id="CMD-twins-isolated", check="each twin tests/labs/M6/lab-M6-L0n-1.py run alone under python -I -W error", location="tests/labs/M6/lab-M6-L01..04-1.py",
         status=P, evidence=CMD + ".venv/bin/python -I -W error <twin>: exit 0 for all four; stdout in /tmp/twin_*.out"),
    dict(id="CMD-twin-lint", check="ruff check, ruff format --check, mypy --no-incremental on the four twins", location="tests/labs/M6/lab-M6-L01..04-1.py",
         status=P, evidence=CMD + "ruff check: no errors; ruff format --check: '4 files already formatted'; mypy: 'Success: no issues found in 4 source files'"),
    dict(id="CMD-page-code-expected", check="page lab code equals twin; expected block equals twin stdout", location="L01.html:124-236, L02.html:149-281, L03.html:172-267, L04.html:153-251",
         status=P, evidence="ledgers/M6/scripts/M6-a-r3/twin_vs_page.py: page code == twin True x4; expected == observed stdout True x4 (exit 0, empty stderr)"),
    dict(id="CMD-pytest-relevant", check="relevant pytest modules: test_labs.py, test_run_labs.py, test_page_checks.py", location="tests/",
         status=P, evidence=CMD + ".venv/bin/pytest -q tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py: all passed (4 progress lines, 100%)"),
    dict(id="CMD-page_smoke", check="tools/page_smoke.py --unit M6 --pages index L01 L02 L03 L04 --skip-sweep (render and runtime)", location="M6 hub and L01-L04 (rendered)",
         status=U, evidence=CMD + "page_smoke.py ... exited 1: BrowserType.launch: Executable doesn't exist at /Users/billyribeiro/Library/Caches/ms-playwright/chromium_headless_shell-1248; no rendered page checked, so no render or runtime evidence exists for this slice",
         fix="Install the Playwright chromium build for the project venv (project dependency, not a toolchain change), then rerun page_smoke.py --unit M6 --pages index L01 L02 L03 L04 --skip-sweep and record its output"),
    dict(id="CMD-verify_refs", check="tools/verify_refs.py offline integrity and live run for M6 entries", location="references/references.json (billingsley2012probability, williams1991probability)",
         status=P, evidence=CMD + "verify_refs.py --offline: '560 entries, 0 problems'; verify_refs.py --unit M6 (live): '2 of 560 entries, 0 problems'; git status clean"),
    dict(id="CMD-notation", check="every macro used in the slice is a registered notation macro or a standard KaTeX command; registered meanings respected", location="notation/notation.json macros \\E \\Prob \\N \\indic; slice pages",
         status=P, evidence="counted macros in index.html, L01-L04.html: \\Prob (104), \\E (5), \\indic (21), \\N (3) used with registered meanings (probability measure, expectation, indicator, natural numbers); all other control words are standard KaTeX; local letters (mu, lambda, nu, N, c, k) are allowed by notation.json 'about'"),
    dict(id="CMD-process-words", check="no process words or banned strings in learner text", location="index.html, L01-L04.html",
         status=P, evidence="grep -i 'round|verif|builder|agent|twin|fragment|ledger|draft|pending|TODO' in the five files: only 'verify' as a learning verb (index.html:52) and 'verifies' of a grader (index.html:164)"),
    dict(id="CMD-data-status", check="hub data status: no lab reads a data file", location="index.html data section; tests/labs/M6/lab-M6-L01..04-1.py",
         status=P, evidence="grep for open(, read_text, csv, .json in the four twins: no match; no data-files attribute on any slice page"),
    dict(id="DELTA-r2", check="every hunk of e22feb3..ccfdf4c in the slice read", location="index.html, L01-L04.html (49 changed lines)",
         status=P, evidence="git diff e22feb3 ccfdf4c read in full: round-2 hunks checked (L01:4 Prop 1.3(d) cross-reference, L02:8 Prop 1.3(a)/602 wording, L03:4 canon-breaks, L04:10 Prop 4.2 and Thm 2.1 wording, index:6 prose); tests/labs unchanged in the delta"),
    # --- hub ---
    dict(id="HUB-hours", check="hub hours arithmetic: 12 x 9 = 108 lessons; 108 + 42 = 150; project 42/150 = 28%; split widths 72/28", location="index.html:24-34 (data-hours-lessons=108, data-hours-project=42), 'hours-split' spans",
         status=P, evidence="own recomputation (recompute_a_r3.py): 12*9=108, 108+42=150, 42/150=0.28; curriculum hours 150 (curriculum.json M6)"),
    dict(id="HUB-placement-numbers", check="placement: nine items, seven prerequisite items, two skill checks; answers; 80% bar = 8 of 9; 7/9 and 8/9 percentages", location="index.html 'placement' section",
         status=P, evidence="recompute_a_r3.py: 7/9=77.8, 8/9=88.9; 0.8*9=7.2 so 8 correct; items: 0.5 (Int_0^1 x), 3.5 (die), 1.5 (E[X|A]), rung-1 E[S_tau]=1/2*1+1/2*(1/2*0+1/2*(-2))=0, rung-2 1+2+4=7"),
    dict(id="HUB-prereq-closure", check="prerequisite closure M6->M4,M5; M4,M5->M2; M2->M1; M1->P0.1", location="index.html:60, curriculum/curriculum.json (M1,M2,M4,M5,M6 prereqs)",
         status=P, evidence="curriculum.json: M6 prereqs [M4,M5]; M4 [M2]; M5 [M2]; M2 [M1]; M1 [P0.1]; closure {M1,M2,M4,M5,P0.1} as the page states"),
    dict(id="HUB-concept-count", check="'M6 introduces 15 concepts'", location="index.html:~70 prerequisites paragraph; curriculum.json M6 'introduces'",
         status=P, evidence="curriculum.json M6 'introduces' has 15 keys (sigma-algebra ... doubling-strategy)"),
    dict(id="HUB-cards", check="hub card summaries match lesson content for L01-L04", location="index.html lesson map cards L01-L04",
         status=P, evidence="L01 card 'partition sigma-algebra, countable unions' = L01 Def 1.1, Prop 2.1, Ex 3.1; L02 card = Def 1.1-1.2, Prop 1.3 (monotone, additive, continuity from below), Prop 1.5; L03 card 'dyadic bracket of x^2' = Prop 4.1; L04 card 'integrals stay at one, limit zero' = Prop 4.2; DCT card says 'with its hypotheses' only, matching the not-proved status"),
    dict(id="HUB-reading", check="core reading keys exist and registry titles match the pages' attributions", location="index.html reading section; references/references.json",
         status=P, evidence="registry: billingsley2012probability title 'Probability and measure' (Billingsley 2012, OpenLibrary); williams1991probability title 'Probability with Martingales' (Crossref 10.1017/cbo9780511813658); pages say no passage read; curriculum sources list both"),
    dict(id="HUB-objectives-L1-4", check="objectives that name Lessons 3 and 4 are taught there", location="index.html objectives 2 (Lessons 3 and 4)",
         status=P, evidence="L03 Def 2.1 (simple integral), Prop 3.2, Prop 4.1 bracket; L04 Thm 2.1 (proved) and Thm 3.1 (stated, with checked hypotheses in Ex 3.2 and Prop 4.1)"),
    dict(id="HUB-prereq-built", check="hub: prerequisite concept links point to the index 'because those module pages are not built yet'", location="course/modules/M/M6/index.html:60",
         status=F, evidence="course/modules/M/M1/index.html and L01-L08.html, project.html exist at pin ccfdf4c (M1 is built), so 'those module pages are not built yet' is false for M1; M2, M4, M5 and P0.1 are not built (no course/modules directories for them)",
         fix="Reword to name only the unbuilt prerequisites (M2, M4, M5, P0.1), e.g. 'M2, M4, M5 and P0.1 pages are not built yet, so their concept links go to the index'"),
    dict(id="HUB-lessons-scope", check="prose: 'Lessons 1 to 4 develop the integral and its convergence theorems'", location="index.html:141 (Lessons section)",
         status=F, evidence="L01 (sigma-algebras) and L02 (measures) contain no integral; the Lebesgue integral is first defined in L03 Definition 3.1 (L03.html:99)",
         fix="Replace with 'Lessons 1 and 2 build the measure space; Lessons 3 and 4 develop the integral and its convergence theorems'"),
    # --- L01 ---
    dict(id="L01-DEF-PROP", check="Def 1.1 and Prop 1.3 (a)-(c): sigma-algebra consequences", location="L01.html:59-88",
         status=P, evidence="re-derived by hand: (a) empty = Omega^c; (b) A u B via countable sequence A,B,empty,...; A n B = (A^c u B^c)^c; (c) complements of countable union. Each step cites an axiom correctly"),
    dict(id="L01-PROP21", check="Prop 2.1 (sigma-algebra of a partition): (a) sigma-algebra, (b) 2^k members, (c) smallest", location="L01.html:96-112",
         status=P, evidence="re-derived: i(x) argument gives U_J^c = U_{J^c} and countable unions = U_J; injectivity via nonempty blocks; Lab 1 counts 4, 16, 8 = 2^k (recompute_a_r3.py)"),
    dict(id="L01-EX31", check="Example 3.1 (finite-cofinite not closed under countable unions) proof", location="L01.html:245-248",
         status=P, evidence="A finite, B cofinite: complement of A u B subset of finite B^c; both cofinite: A^c n B^c finite; A_n = {2n}, union = evens, neither finite nor cofinite"),
    dict(id="L01-LAB", check="Lab 1: hypothesis, output, interpretation; candidate fails complement only", location="L01.html:121-238; tests/labs/M6/lab-M6-L01-1.py",
         status=P, evidence="twin output: 4/16/8 members; candidate complement closed False, missing {2, 3}; overlapping blocks rejected; hypothesis predicted all of this"),
    dict(id="L01-NUMBERS", check="numbers in L01 prose, problems and quiz: 8 (M1), 32 (M3, quiz five singletons), 8 (six-point), 16 (four-point subsets), 2^4", location="L01.html:289-466",
         status=P, evidence="recompute_a_r3.py: five blocks 2^5=32, three blocks 2^3=8, two blocks 4, four singletons 16; M1 family of blocks {1},{2,3},{4,5} has 8 members listed correctly"),
    dict(id="L01-CROSSREF", check="cross-reference 'continuity from below in Lesson 2, Proposition 1.3(d)'", location="L01.html:256",
         status=P, evidence="L02.html:83 Prop 1.3(d) is continuity from below; reference exact"),
    dict(id="L01-PROBLEMS-QUIZ", check="problem solutions and quiz answers and explanations", location="L01.html:285-466",
         status=P, evidence="re-derived each solution; quiz Q1 explanation (third family fails S2 and S3 via {1,2}) and Q6 (Example 1.2) are correct"),
    # --- L02 ---
    dict(id="L02-PROP13-15", check="Prop 1.3 (a)-(d) and Prop 1.5 proofs; Remark 1.4 scope", location="L02.html:72-111",
         status=P, evidence="(d) disjointification D_n = A_n \\ A_{n-1} and sum partial sums; (b) uses Prop 1.3(a); Prop 1.5 proof correct; Remark 1.4 says the page does not build a counterexample (honest)"),
    dict(id="L02-PROP21", check="Prop 2.1 (a)-(b) on finite space; Ex 2.2 numbers", location="L02.html:119-142",
         status=P, evidence="(a) finite support argument valid; biased weights sum to 1; P({1,2}) = 1/2+1/4 = 3/4 (recomputed)"),
    dict(id="L02-EX23", check="Ex 2.3: nu(A)=(|A|/6)^2 not additive; 4/36 vs 2/36", location="L02.html:141",
         status=P, evidence="recompute: nu({1,2}) = (2/6)^2 = 4/36; nu({1})+nu({2}) = 2/36"),
    dict(id="L02-LAB", check="Lab 2 output, hypothesis and interpretation: 602 of 729, 9/10 total mass, P(even)=1/2, 2/3 vs 1/2", location="L02.html:146-283; tests/labs/M6/lab-M6-L02-1.py",
         status=P, evidence="twin output: 64 subsets; 602 of 729 failing pairs for nu; fair/biased/point mass pass; 3/20 weights fail total mass only; hypothesis 3^6 - (64+64-1) = 602 recomputed"),
    dict(id="L02-PROP31-MISC", check="Prop 3.1 identity; misconceptions 1-3 (602, 2/3 vs 1/2 with correction 1/6, zero-probability non-empty)", location="L02.html:289-329",
         status=P, evidence="recompute: P({1,2,3}) = 1/2, P({2}) = 1/6, 2/3 - 1/6 = 1/2; overlap correction equals P(A n B)"),
    dict(id="L02-PROBLEMS-QUIZ", check="problem solutions, empirical items, quiz answers", location="L02.html:331-516",
         status=P, evidence="M2: 21/32 recomputed; E1 2ab/36 cross term; E3 3^4=81; quiz Q4 tolerance 1e-6 vs 2/3 accepts 0.666667; Q8 correct option Prop 1.3(d)"),
    # --- L03 ---
    dict(id="L03-SIMPLE-MONO", check="Def 1.1, Def 2.1, Prop 2.2 (monotonicity of simple integral) proof", location="L03.html:58-93",
         status=P, evidence="proof via A_i n B_j partition and a_i <= b_j on nonempty intersections; zero-measure terms vanish; valid"),
    dict(id="L03-SUP-PROP32", check="Def 3.1 and Prop 3.2 (a)-(b)", location="L03.html:97-118",
         status=P, evidence="(a) supremum contains s; (b) inclusion of admissible sets; valid"),
    dict(id="L03-PROP33", check="Prop 3.3: value at a point of measure zero does not change a simple integral", location="L03.html:120-133",
         status=P, evidence="proof valid in substance (mu(A minus {x0}) = mu(A) lemma; level sets change by a null set); phrase 'same values times the same measures' is loose but the conclusion holds"),
    dict(id="L03-PROP41", check="Assumption L and Prop 4.1 (dyadic bracket) proofs and level-set lengths", location="L03.html:139-160",
         status=P, evidence="re-derived: level set k is [sqrt(k/2^n), sqrt((k+1)/2^n)); k=2^n is {1} with length 0; I_n = sum k/2^n (sqrt((k+1)/2^n)-sqrt(k/2^n)); I_1 = (1/2)(1-sqrt(1/2)) = 0.1464466094"),
    dict(id="L03-NUMBERS-TABLE", check="Part B table: I_n, 1/3 - I_n, 2^-n for n = 1..10 (10 decimals)", location="L03.html:257-266 (expected block); tests/labs/M6/lab-M6-L03-1.py",
         status=P, evidence="recompute_a_r3.py prints the same I_n, error and bound for n=1..10 to 10 decimals (e.g. n=10: I=0.3328513565, err=0.0004819768, bound=0.0009765625)"),
    dict(id="L03-NUMBERS-PROSE", check="prose numbers: 0.1464, 0.1869, 0.3333, 0.0004819768, 0.0009765625, E3 I_2 terms 0.0518/0.0795/0.1005 and sum 0.231717 / 0.2318", location="L03.html:291, 264, 367, 374, 448-451",
         status=P, evidence="recompute: 1/3-I_1 = 0.1868867 -> 0.1869; I_2 rounded terms 0.051777, 0.079459, 0.100481; sums 0.231717 and 0.2318 (rounded-then-added = 0.2318)"),
    dict(id="L03-LAB-PARTA", check="Lab 3 Part A: moved value at x=1/2 to 5 leaves integral 1 'by Proposition 3.3' and the page says the lab prints 1 before and after", location="L03.html:169-171, 229-235, 295, 474; tests/labs/M6/lab-M6-L03-1.py:58-64",
         status=F, evidence="The 'moved' function is the same pieces with a zero-length piece (0, 5) appended, and simple_integral (twin lines 26-27, docstring: 'A piece of length 0 is a single point and contributes nothing') gives 1 for that piece with value 5, 1000000 and -7 alike (run in this checkout). The printed equality is therefore true by construction and cannot fail, so the lab does not test Prop 3.3; the line label 'same function with the value ... set to 5' overstates what the code does",
         fix="Represent Part A as a function on labelled points (a partition into level sets), change the value at 1/2 in that representation, and recompute the integral from the changed level sets using the measure of each level set (the null point changes only its own level set); or relabel the line and the page sentences at L03.html:171, 295, 474 as a construction that holds by definition, not a check of Proposition 3.3"),
    dict(id="L03-PROBLEMS-QUIZ", check="problem solutions and quiz answers", location="L03.html:300-495",
         status=P, evidence="M1 = 4 (2*1/3+5*2/3), M2 = 3/4, M3 I_1 closed form, R3 infinite integral (mu of nonempty = infinity, integral of 1 = infinity) all re-derived; quiz Q2 tolerance 1e-4 vs 0.1464466 accepted"),
    # --- L04 ---
    dict(id="L04-THM21", check="Thm 2.1 monotone convergence proof (measurability, upper bound, lower bound via E_n and c<1)", location="L04.html:64-83",
         status=P, evidence="re-derived each step: E_n increasing; cover of Omega (s=0 in E_1; s=a>0 gives f>ca); t_n = c s 1{E_n} <= f_n; continuity from below of A_i n E_n; limit c -> 1; supremum over s"),
    dict(id="L04-EX22", check="Ex 2.2: f_n = n 1{(0,1/n]} not non-decreasing; f_1 = 1 on (1/2,1], f_2 = 0 there", location="L04.html:85-88",
         status=P, evidence="f_1 = 1{(0,1]} takes 1 on (1/2,1]; f_2 = 2*1{(0,1/2]} is 0 there"),
    dict(id="L04-THM31-stated", check="Thm 3.1 is labelled stated, not proved, and is not graded", location="L04.html:92-102; key results row 'not graded' (L04.html:399)",
         status=P, evidence="block title 'stated, not proved here' and no data-grade attribute; key-results row says 'not graded'; no proof claimed"),
    dict(id="L04-EX32", check="Ex 3.2: min(n,x^-1/2) integrals 2 - 1/n; calculus assumption stated", location="L04.html:104-108",
         status=P, evidence="recompute: f_n = n on (0,1/n^2]; int = n/n^2 + (2 - 2/n) = 2 - 1/n; int_0^1 x^-1/2 = 2; assumption that calculus value = Lebesgue integral is stated in the example title and text"),
    dict(id="L04-PROP41", check="Prop 4.1 (no integrable bound): proof via I_n = (1/(n+1), 1/n] and grouping of 2..2^m", location="L04.html:112-128",
         status=P, evidence="re-derived: lengths 1/(n(n+1)); h_N <= g; int h_N = sum 1/(n+1); blocks {2^(j-1)+1..2^j} each >= 1/2; sum_{k=2}^{2^m} 1/k >= m/2 checked exactly for m<=10 (lab Part C)"),
    dict(id="L04-PROP42", check="Prop 4.2 (integrals stay at 1, limit 0): assumptions complete for a T-graded claim", location="L04.html:131-132 (statement and Assumptions), proof 137-140; graded T at 131",
         status=F, evidence="Assumptions read 'Assumptions. [0, 1] carries lambda, and f_n = n 1{(0,1/n]}' and never refer to Lesson 3, Assumption L (L03.html:140-141: lambda([a,b]) = b - a). The proof of (a) uses lambda((0,1/n]) = 1/n, which is exactly that length rule; Prop 4.1 (L04.html:116) cites Assumption L but Prop 4.2 does not. A T-graded result whose proof needs a hypothesis its statement omits fails VERIFIER_RULES 2.4 / the round rule",
         fix="Add to Proposition 4.2's Assumptions: 'lambda is the length measure of Lesson 3, Assumption L, so lambda((a,b]) = b - a'"),
    dict(id="L04-REM43", check="Remark 4.3: both theorems silent; no claim beyond the proofs", location="L04.html:143-146",
         status=P, evidence="Thm 2.1 fails since f_1 <= f_2 fails; Thm 3.1 fails since Prop 4.1 excludes an integrable dominator; text says the example does not isolate a hypothesis (true)"),
    dict(id="L04-LAB", check="Lab 4 hypothesis, output and interpretation", location="L04.html:148-253; tests/labs/M6/lab-M6-L04-1.py",
         status=P, evidence="twin output: integrals True for n=1..20; f_n(1/5) = 1,2,3,4,5,0,0,0; first zero 6 and 51 equal floor(1/x)+1; contributions 1/2..1/6; partial sums 2.019877 and 4.197279 (recomputed); grouping True"),
    dict(id="L04-CANON-MISC", check="canon-breaks and misconceptions 1-3 claims", location="L04.html:255-282",
         status=P, evidence="Ex 2.2 fails monotonicity and Prop 4.1 fails domination; 'Monotonicity ... does not isolate' is correct; 'dominating function need not be bounded' supported by Ex 3.2 (under the stated assumption)"),
    dict(id="L04-PROBLEMS-QUIZ", check="problem solutions (M2 (1 - x^n), M3 3/2, R2 g=floor(x^-1/2) integral finite) and quiz answers", location="L04.html:284-480",
         status=P, evidence="M2: 1-x^n nondecreasing, integral n/(n+1) -> 1; M3 = 2*(1/4)+1 = 3/2 (numerical check 1.4999999); R2: g=1 on (1/4,1], level n has length (2n+1)/(n^2(n+1)^2), each term <= 3/n^2; quiz Q4 1.5, Q6 2.019877 within 1e-6 (recomputed 2.0198773)"),
    dict(id="L04-META-LABEL", check="label clarity: '(M2)' in the Uses line refers to module M2, while (M2) is the countable-additivity axiom in Lesson 2", location="L04.html:37 (meta row); L02.html:62 (axiom (M2))",
         status=F, evidence="L04 Uses line reads 'the limit of a sequence of real numbers (M2)' meaning the module; the same label denotes axiom (M2) in L02 and in Remark 1.4 of this unit's pages; the two meanings sit in one unit's series",
         fix="Write 'the limit of a sequence of real numbers (module M2)'"),
    dict(id="L04-CROSSREF", check="cross-references: L02 Prop 1.3(d), L03 Def 3.1, L03 Remark 4.2, L03 Assumption L, Thm numbers", location="L04.html:37, 81, 106, 116",
         status=P, evidence="L02.html:83 has Prop 1.3(d); L03.html:99 Def 3.1 anchor def-lebesgue-integral; L03.html:164 Remark 4.2; L03.html:140 Assumption L"),
]

fragment = {
    "unit": "M6",
    "slice": "M6-a",
    "round": 3,
    "verifier": "Haiku independent verifier, M6 slice a, round 3 (did not build M6)",
    "pin": "ccfdf4c",
    "base": "e22feb3 (delta e22feb3..ccfdf4c read for the slice; no round-2 fragment was present in /Users/billyribeiro/.fanout/frags, so no PASS row is carried)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyC3-M6-a (detached at ccfdf4c, .venv symlinked)",
    "scratch": "/tmp/m6a_*.txt and /tmp/twin_*.out",
    "verified_at": "2026-10-28",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "Slice: hub index.html, L01-L04 and their lab twins. Full read of index.html and L01-L04.html (line by line), "
        "all four twins, and the e22feb3..ccfdf4c delta hunks. Not checked: page_smoke rendering and runtime (Playwright chromium absent); "
        "the sweep of figures (not applicable, --skip-sweep not run for render); cards.json and the L05+ pages (outside this slice); "
        "live Crossref/OpenLibrary bibliographic facts beyond the two registry entries (verify_refs --unit M6 ran live with 0 problems). "
        "No mutants written: this is a lesson slice, not a project grader slice."
    ),
    "summary": "M6 slice a round 3 at ccfdf4c: FAIL. Two substantive defects (L03 Part A moved-point check is true by construction; L04 Prop 4.2 omits Assumption L), three low prose/label defects (hub prerequisite rationale, hub Lessons 1-4 scope, L04 (M2) label), and page_smoke not runnable here (UNVERIFIABLE). Every other row PASS by command output or hand recomputation.",
}

out = ROOT / "ledgers/M6/M6-a.json"
out.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out, "rows", len(rows), "pass", sum(r["status"] == "PASS" for r in rows), "fail", sum(r["status"] == "FAIL" for r in rows), "unverifiable", sum(r["status"] == "UNVERIFIABLE" for r in rows))
