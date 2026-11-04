# Builds ledgers/SC1/SC1-a.json (round 6) from rows decided in this round. Run with python3 -I.
import json

R = "Round 6 at 4bd8cb9 (re-read this round): "
G = "gate re-run this round"
rows = []

def row(rid, check, location, status, evidence, fix=None):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    rows.append(r)

S = "ledgers/SC1/scripts/SC1-a-r6/"
# gates and labs
row("SC1a-gate-check-pages", "2.9-structure-tool", "course/modules/SC/SC1/index.html, L01.html, L02.html, L03.html",
    "PASS", R + "tools/check_pages.py --unit SC1 -> 'check_pages SC1: PASS', exit 0 (" + S + "check_pages.out).")
row("SC1a-gate-check-dag", "2.9-dag-tool", "course/modules/SC/SC1/index.html, L01.html, L02.html, L03.html",
    "PASS", R + "tools/check_dag.py --unit SC1 -> 'check_dag SC1: PASS', exit 0 (" + S + "check_dag.out). check_projects --unit SC1 PASS (" + S + "check_projects.out).")
row("SC1a-gate-run-labs", "2.5-labs-run", "tests/labs/SC1/lab-SC1-L01-1.py, lab-SC1-L02-1.py, lab-SC1-L03-1.py",
    "PASS", R + "tools/run_labs.py --unit SC1 -> 'run_labs SC1: PASS (11/11)', exit 0 (" + S + "run_labs_unit.txt).")
row("SC1a-gate-page-smoke", "2.9-page-smoke", "index.html, L01.html, L02.html, L03.html",
    "PASS", R + "tools/page_smoke.py --unit SC1 --pages index.html L01.html L02.html L03.html --skip-sweep -> 'page_smoke SC1: PASS', exit 0 (" + S + "page_smoke.out). The figure sweep was skipped (no live figures in these pages).")
row("SC1a-gate-lint-types-tests", "2.5-ruff-mypy-pytest", "tests/labs/SC1/lab-SC1-L01-1.py, lab-SC1-L02-1.py, lab-SC1-L03-1.py; pytest -k SC1",
    "PASS", R + "ruff check and ruff format --check on tests/labs/SC1 pass (" + S + "ruff.out); mypy --no-incremental on the three twins: 'Success: no issues found in 3 source files' (" + S + "mypy.out); pytest tests/test_labs.py -k SC1 exit 0 (" + S + "pytest_labs_sc1.out).")
row("SC1a-gate-verify-refs", "2.1-citations", "course/modules/SC/SC1/index.html:182 (data-cite shreve2004stochastic)",
    "PASS", R + "tools/verify_refs.py --offline -> 'offline integrity: 560 entries, 0 problems', exit 0 (" + S + "verify_refs.out). The cited key exists in references/references.json:20732.")
row("SC1a-lab-L01-twin", "2.5-lab-L01", "tests/labs/SC1/lab-SC1-L01-1.py; L01.html:137-206",
    "PASS", R + "twin run as python3 -I -W error from an empty scratch dir: exit 0, no stderr; stdout equals the page expected block (" + S + "twin-L01.out; compared programmatically).")
row("SC1a-lab-L02-twin", "2.5-lab-L02", "tests/labs/SC1/lab-SC1-L02-1.py; L02.html:168-279",
    "PASS", R + "twin run under -I -W error: exit 0, stdout equals the expected block (" + S + "twin-L02.out). The twin changed this round (docstring only); page code equals twin per run_labs.")
row("SC1a-lab-L03-twin", "2.5-lab-L03", "tests/labs/SC1/lab-SC1-L03-1.py; L03.html:131-252",
    "PASS", R + "twin run under -I -W error: exit 0, stdout equals the expected block (" + S + "twin-L03.out).")
row("SC1a-lab-claims-L01", "2.5-lab-claims", "tests/labs/SC1/lab-SC1-L01-1.py:1-9 (docstring, shown at L01.html:137-145); L01.html:136 and :208",
    "PASS", R + "docstring claims checked against code and output: 15 of 15 (3 times x depths 0-4), 81 of 81 grid pairs, exact Fraction comparisons, Cov(B_1/4,B_5/8)=1/4 all match (" + S + "twin-L01.out).")
row("SC1a-lab-claims-L03", "2.5-lab-claims", "course/modules/SC/SC1/L03.html:133 (hypothesis), :253 (interpretation), :343 (E1)",
    "PASS", R + "SE formula H*sqrt(2/N)/20 with 400 paths; |z| max 2.39 at H=1,N=2 (second largest 1.84); exact-sum closed form matches all 16 rows (" + S + "recompute.out, twin-L03.out).")
row("SC1a-lab-L02-docstring", "2.5-lab-claims", "tests/labs/SC1/lab-SC1-L02-1.py:1-8 (docstring, shown at L02.html:171-178)",
    "PASS", R + "the changed docstring claims ('hat values at dyadic points are exact binary fractions'; 'every level term beyond the depth of the point is exactly 0.0') checked: zero check over all dyadic points and levels m>n gives 8844 cases with 0 nonzero hat values (" + S + "recompute.out).")
row("SC1a-r4-seed-sweep-L02", "2.5-lab-seed", "tests/labs/SC1/lab-SC1-L02-1.py; L02.html:170 (SIMULATED claim)",
    "PASS", R + "the lab with SEED replaced by 20260101 through 20260150 (50 seeds): the dyadic line is '216 of 216 cases' and the grid-supremum line is True in all 50 runs (identity lines only; bound lines describe one sample, as the page says).")
# numbers
row("SC1a-numbers-L01", "2.2-numbers", "course/modules/SC/SC1/L01.html:132, :229, :298, :305, :348-352, :393, :398, :412, :426",
    "PASS", R + "1/4 and 1/10 standard deviations, 3/64 and 16*3/64=3/4, 1/4 covariance, 1/2 and 10 ratios, Var(3B_1-B_2)=5, E[B_3^2]=3 recomputed by hand.")
row("SC1a-numbers-L02", "2.2-numbers", "course/modules/SC/SC1/L02.html:263 (printed bound lines), :274, :385, :392, :399, :405-406",
    "PASS", R + "recompute.py: all eight printed level suprema and bounds (m=1..8) reproduced to six decimals and each supremum is within its bound; grid sup |Sigma_8-Sigma_4| = 0.348139 and sum of bounds 5..8 = 1.309399 match (" + S + "recompute.out).")
row("SC1a-numbers-L03", "2.2-numbers", "course/modules/SC/SC1/L03.html:253, :270, :275, :343, :350, :357, :368, :375, :398, :434",
    "PASS", R + "recompute.py: 0.166664 for H=2,N=128 and the closed form values match; 2.65625 = 4080/1536; 0.625 = 15/24; 1/80 = 0.0125 (" + S + "recompute.out).")
row("SC1a-numbers-L02-36-points", "2.2-numbers", "course/modules/SC/SC1/L02.html:263 (interpretation); :411-414 (E2)",
    "PASS", R + "dyadic point counts 2,3,5,9,17 (36 pairs) and 18+24+35+54+85=216 recomputed.")
row("SC1a-numbers-L03-SE-follow", "2.2-numbers", "course/modules/SC/SC1/L03.html:398 (key-results row, grade C)",
    "PASS", R + "recompute.py gap = printed SE / (H*sqrt(2/N)/20) - 1 over all 16 rows: largest |gap| 13.21% at H=2,N=1 (within the stated 14 percent); the row's wording matches (" + S + "recompute.out).")
# grades
row("SC1a-grade-L01", "2.3-grades", "course/modules/SC/SC1/L01.html:83, :101, :119, :349-353",
    "PASS", R + "T grades sit on Proposition 1.2, Remark 1.3, Example 1.4 and on key-results rows that are proved on the page; the row 4 T is conditional on the named A1, A2 and Assumption 2.1, which the row states.")
row("SC1a-grade-L02", "2.3-grades", "course/modules/SC/SC1/L02.html:74, :93, :110, :134, :274, :287, :458-462",
    "PASS", R + "T grades on Lemmas 2.1-2.3, Proposition 2.4, Theorem 2.5 are proved on the page given the named hypotheses; A2 is stated as an Assumption with a labelled sketch (L02.html:281-286), not graded T.")
row("SC1a-grade-L03", "2.3-grades", "course/modules/SC/SC1/L03.html:77, :90, :99, :118, :394-398",
    "PASS", R + "T grades match proofs on the page; the C row at L03.html:398 is labelled SIMULATED with one seed.")
row("SC1a-hub-grade-definition", "2.3-grades", "course/modules/SC/SC1/index.html:79; BLUEPRINT.md:158",
    "PASS", R + "index.html:79 (placement item 1 answer 'A theorem, proved on the page or with a precisely cited proof') matches BLUEPRINT.md:158 (T). index.html changed only at line 33 this round, so passage 79 is byte-identical to round 5 (carried from round 5, passage index.html:79 and BLUEPRINT.md:158 byte-identical since the previous pin).")
# math
row("SC1a-math-L01-prop1.2", "2.4-math", "course/modules/SC/SC1/L01.html:84-98 (Proposition 1.2 and proof)",
    "PASS", R + "proof re-derived: E[XY]=E X E Y under A1(a); Cov(B_s,B_t)=E X^2 = s; integrability of XY from |XY|<=(X^2+Y^2)/2.")
row("SC1a-math-L01-remark1.3", "2.4-math", "course/modules/SC/SC1/L01.html:102-113",
    "PASS", R + "linear combinations of independent normals under A1(b); mean 0; covariance min(t_i,t_j) from Prop 1.2 (A1(a)). Hypotheses H2 list A1(b) and A1(a) as used.")
row("SC1a-math-L01-canon-construction", "2.4-math", "course/modules/SC/SC1/L01.html:215 (canon item 1)",
    "FAIL",
    R + "the construction of the counterexample uses a uniform U independent of B on the same probability space (L01.html:215: 'Let U be uniform on (0,1) and independent of B'). The sentence before it says only that Remark 2.6 'gives such a process on a probability space that carries independent coefficient families as in Hypothesis H1 of Lesson 2'. Nothing in the hypotheses of Remark 2.6 (L02.html:305) puts a uniform U on that space, so the step 'Let U ... be independent of B' is not supplied by the cited result. The rest of item 1 (D1), the fdd equality, the discontinuity at U on every outcome) re-derived correctly.",
    "State the space as one that also carries a uniform U independent of the coefficient families and of B (for example a product extension of the Remark 2.6 space), in L01.html:215 and in the Key results row at :353.")
row("SC1a-math-L02-lemmas-2.1-2.2", "2.4-math", "course/modules/SC/SC1/L02.html:73-117",
    "PASS", R + "Lemma 2.2 (a)-(e) and Lemma 2.1 re-derived: the union of exponential bound e^{theta^2/2}, theta=lambda, and the two-sided bound 2e^{-lambda^2/2}; Lemma 2.2(c) integer parity argument.")
row("SC1a-math-L02-lemma2.3-arithmetic", "2.4-math", "course/modules/SC/SC1/L02.html:121-141",
    "PASS", R + "U_j = D_j/2 + c eta_j, V_j = D_j/2 - c eta_j with c = 2^{-(n+2)/2}; Var U_j = 2^{-(n+2)} + 2^{-(n+2)} = 2^{-(n+1)}; Cov(U_j,V_j) = 0; A1(b),(c),(e) used as stated in H2.")
row("SC1a-math-L02-prop2.4", "2.4-math", "course/modules/SC/SC1/L02.html:145-165",
    "PASS", R + "P(E_m^c) <= 2^{m-1} * 2 * 4^{-m} = 2^{-m}; sum over m>=m0 gives 2^{1-m0}; M_m = sqrt(2 log 2) sqrt(m) 2^{-m/2} <= sqrt(2 log 2) m r^m summable; Cauchy and uniform convergence as written.")
row("SC1a-math-L02-A2-sketch", "2.4-math", "course/modules/SC/SC1/L02.html:281-286",
    "PASS", R + "A2 is labelled 'Sketch, not a proof' and names the skipped step (passage of characteristic functions to the limit and the joint version). The sketch is consistent with Lemma 2.3 for dyadic times.")
row("SC1a-math-L02-thm2.5", "2.4-math", "course/modules/SC/SC1/L02.html:288-300",
    "PASS", R + "(D1) from Sigma_M(0)=0 and off-Omega* definition; (D2)/(D3) from A2 as stated; continuity from Prop 2.4(b).")
row("SC1a-math-L03-thm2.3", "2.4-math", "course/modules/SC/SC1/L03.html:99-115",
    "PASS", R + "E Q = t; Var Q = sum 2 Delta_k^2 by Lemma 2.2 and Assumption 3.2(a),(b); sum Delta_k^2 <= |P| t gives the mean-square bound 2t|P|.")
row("SC1a-math-L03-prop2.4", "2.4-math", "course/modules/SC/SC1/L03.html:117-129",
    "PASS", R + "(a) (b^2-a^2)^2 <= 4H^2(b-a)^2 and sum <= 4H^3|P|; (b) S(N) = N(4N^2-1)/3 by induction re-checked, giving H^4(4N^2-1)/(3N^3).")
row("SC1a-math-L03-misc-claims", "2.4-math", "course/modules/SC/SC1/L03.html:259-261, :270, :274-279, :366-382",
    "PASS", R + "E|Z| = sqrt(2/pi) and the absolute-sum growth sqrt(2Nt/pi) re-derived; variance 2t^2 of the dependent family re-derived; R2 least constant 2 re-derived.")
row("SC1a-math-L03-density", "2.4-math", "course/modules/SC/SC1/L03.html:78 (Lemma 2.1 density), :332 (P3)",
    "PASS", R + "phi'(z) = -z phi(z); integration by parts E Z^4 = 3; int_0^R z phi = phi(0) - phi(R).")
row("SC1a-grade-L02-remark2.6", "2.4-math", "course/modules/SC/SC1/L02.html:302-318",
    "PASS", R + "Remark 2.6 re-derived: W continuous at integers because B^{(k)}_0 = 0 and copies are continuous; (D2) by refinement and independence of distinct copies (H1); (D3) by A1(e) over blocks. The T grade is conditional on the named A1(a),(b),(e), A2 and Assumption 2.1 (H2 lists them). The plan's Q5 asked for a sketch label for this extension; the page proves it under A2 instead, which is stronger and is not a T beyond the stated hypotheses.")
row("SC1a-math-L02-thm2.5-extension", "2.4-math", "course/modules/SC/SC1/L02.html:302-318",
    "PASS", R + "same as SC1a-grade-L02-remark2.6: the (D2) refinement and (D3) block argument re-checked line by line.")
row("SC1a-exercises-L01-L03", "2.4-problems", "course/modules/SC/SC1/L01.html:246-427; L02.html:351-520; L03.html:289-385",
    "PASS", R + "every worked solution re-checked: L01 M1-M3, P1-P3, E1-E3, R1-R3; L02 M1-M3 (M3: 1/8+1/8=1/4), P1-P3, E1-E3 (E3 recomputed: 0.116589 and 0.233179 vs doubling 0.233178), R1-R3; L03 M1-M3, P1-P3, E1-E3, R1-R3.")
row("SC1a-misconceptions-canon", "2.4-canon", "course/modules/SC/SC1/L01.html:219-235, L02.html:307-330, L03.html:256-281",
    "PASS", R + "each misconception re-derived; L02 series misconception block bound 1+k/2 re-checked; L03 misconception 2 expectation re-derived.")
row("SC1a-canon-breaks-ungraded", "2.3-grades", "course/modules/SC/SC1/L02.html:319-327; L01.html:215-217; L03.html:259-261",
    "PASS", R + "canon-break items carry no T grade of their own; their claims re-derived (L02 item 4 X_{1/3}=0 counterexample; L03 item 2 X_N example).")
# notation
row("SC1a-notation-macros", "2.4-notation", "course/modules/SC/SC1/index.html, L01.html, L02.html, L03.html",
    "PASS", R + "macros used on the four pages (\\E, \\Prob, \\Var, \\Cov, \\Normal, \\indic) are all in notation/notation.json macros.")
row("SC1a-notation-no-registered-collision", "2.4-notation", "course/modules/SC/SC1/L01.html, L02.html, L03.html",
    "PASS", R + "grep of \\(...\\) symbols on the three lessons: no registered symbol (T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q}) is used with another meaning; plain R in L03 Lemma 2.1 is unregistered (R^\\ast is) and local.")
row("SC1a-notation-T-subscript", "2.4-notation", "course/modules/SC/SC1/L01.html, L02.html, L03.html",
    "PASS", R + "T appears in L03.html only as the mention 'the program's notation reserves T for the number of return observations' (L03.html:120), which matches notation.json symbol T; no other use of T.")
row("SC1a-notation-H-horizon", "2.4-notation", "course/modules/SC/SC1/L03.html:120, :122, :128, :133; tests/labs/SC1/lab-SC1-L03-1.py",
    "PASS", R + "H is the horizon, not a registered symbol; consistent in prose and lab (HORIZONS = (1.0, 2.0)).")
row("SC1a-r4-notation-S-symbol-L02", "2.4-notation", "course/modules/SC/SC1/L02.html:67-68, 126, 132-134, 139, 151, 163-165, 282, 296",
    "PASS", R + "Sigma is used consistently for the partial sum and its limit; no stray S remains in L02 (grep); Sigma_M, Sigma, Sigma_n are the same object in each place.")
row("SC1a-r4-thm23-counterexample-L03", "2.4-math", "course/modules/SC/SC1/L03.html:260 ('Independence is not optional'); L03.html:382 (R3 solution)",
    "PASS", R + "X_N example: Q = N X_N^2, E Q = t, Var Q = 2t^2 for every N, mesh to 0; R3 names the failing hypotheses (H1 independence; Assumption 3.2 needs independence). The wording 'H2 fails because Assumption 3.2 needs the same independence' is accepted as a description of the failed hypothesis of the implication.")
row("SC1a-process-words", "2.9-prose", "index.html, L01.html, L02.html, L03.html; lab twins L01-L03",
    "PASS", R + "grep for builder, verifier, fixer, ledger, round, draft, agent, reviewer, audit in the four pages: no hits.")
row("SC1a-banned-phrases", "2.9-prose", "index.html, L01.html, L02.html, L03.html; lab twins",
    "PASS", R + "tools/check_pages.py --unit SC1 PASS covers the banned-string list (TODO, TBD, lorem, 'for brevity', 'details omitted', 'beyond the scope'). A grep for roughly, historically, typically, clearly, obviously, simply, about N finds only 'about normal' (L01.html:217), which is not a banned phrase.")
row("SC1a-structure-L01-L03", "2.9-structure", "course/modules/SC/SC1/L01.html, L02.html, L03.html",
    "PASS", R + "check_pages PASS; each lesson has grade legend, problem set, key results, quiz, references, lesson-nav.")
row("SC1a-scope-words-L02-L03", "2.4-scope", "course/modules/SC/SC1/L02.html:122, :139, :158, :263, :316, :385, :417; L03.html:85, :104, :133, :253, :270",
    "PASS", R + "'every'/'all'/'only'/'exactly' uses checked: each is backed by a computation or an explicit hypothesis (for example 'every outcome in Omega*' with Prop 2.4(b); 'exactly 0.0' with the zero check).")
row("SC1a-scope-L01-prop1.2-only", "2.4-scope", "course/modules/SC/SC1/L01.html:216 (canon-break 2)",
    "PASS", R + "item 2 now reads 'Under the assumptions of the first item'; the event-level claims (continuous on every outcome for B, on no outcome for B~) re-derived.")
row("SC1a-ref-L01-every-result", "2.1-citations", "course/modules/SC/SC1/L01.html:434",
    "PASS", R + "the References paragraph says every result is proved on the page from Definition 1.1 and A1, and that §4 also uses Lesson 2 (Remark 2.6 under A1(a),(b),(e), A2, Assumption 2.1). That is accurate for §4 as stated.")
row("SC1a-r4-cauchy-schwarz-L01", "2.4-assumptions", "course/modules/SC/SC1/L01.html:95; index.html:69 (promise)",
    "PASS", R + "L01.html:95 proves integrability of XY from |XY| <= (X^2+Y^2)/2 with no Cauchy-Schwarz; the promise at index.html:69 holds for the numbered A1 and Assumption 2.1.")
row("SC1a-hub-assumption-promise", "2.4-assumptions", "course/modules/SC/SC1/index.html:69 (promise), :184; L02.html:93-99 (Assumption 2.1), :105",
    "PASS", R + "every lemma and theorem names its assumption (checked for L01-L03); the promise at index.html:69 is kept (Assuming ... by number).")
row("SC1a-attrib-L01-A1-parts", "2.4-assumptions", "course/modules/SC/SC1/L01.html:37, :72-80",
    "PASS", R + "A1 heading says 'facts from M4' while part (d) is a measurability fact; the text at L01.html:80 attributes (d) to M6 and says the page does not reprove them. The label is a summary, not a false attribution; not a FAIL.")
row("SC1a-assump-L01-P3", "2.4-assumptions", "course/modules/SC/SC1/L01.html:285-287",
    "PASS", R + "P3 uses symmetry of covariance and Prop 1.2 for the pair (t,s); no unnumbered assumption.")
row("SC1a-assump-L02-grouping", "2.4-assumptions", "course/modules/SC/SC1/L02.html:113, :127-128",
    "PASS", R + "the Gaussian-tail and grouping facts are named as Assumption 2.1(a) and A1(e) where used.")
row("SC1a-attrib-L02-lemma2.1-union", "2.4-attribution", "course/modules/SC/SC1/L02.html:158, :263",
    "PASS", R + "the union bound is attributed to Assumption 2.1(c) and Lemma 2.1; no external attribution.")
row("SC1a-attrib-L02-eponym", "2.1-citations", "course/modules/SC/SC1/L02.html:7 (meta description); tests/labs/SC1/lab-SC1-L02-1.py:1-8",
    "PASS", R + "no person or source is named for the construction in the page or the twin; the construction is described, not attributed.")
row("SC1a-reference-section-L02-L03", "2.1-citations", "course/modules/SC/SC1/L02.html:547; L03.html:491; L01.html:434",
    "PASS", R + "each References section cites no passage; L03 mentions Shreve by key only with 'No passage locator ... so no statement is attributed to it'.")
row("SC1a-hub-hours", "2.9-hours", "course/modules/SC/SC1/index.html:29, :39-42, :150; project.html:272-280",
    "PASS", R + "data-hours=9 on each of L01-L08 (grep); 8 x 9 = 72 lesson hours; 72/28 split and 28% of 100 h match index.html:29-42; project hours cited from project.html.")
row("SC1a-hub-placement", "2.9-structure", "course/modules/SC/SC1/index.html:72-145",
    "PASS", R + "nine items (seven prerequisite, two skill); 7/9 = 77.8%, 8/9 = 88.9%, bar 80% needs 8 correct; correct options and numeric answers re-checked.")
row("SC1a-r4-hub-quiz-keys", "2.9-structure", "course/modules/SC/SC1/index.html:72-145 (data-correct / data-answer)",
    "PASS", R + "answer keys match the arithmetic: item 3 = 1, item 4 = 2, skill 2 = 2 (walk count recomputed by enumeration: 2 walks reach 1 out of 4).")
row("SC1a-hub-prereq-chain", "2.9-structure", "course/modules/SC/SC1/index.html:35, :58-68; curriculum/01-foundations.yaml:261-263 (M6 prereqs)",
    "PASS", R + "curriculum: SC1 prereqs [M6]; M6 prereqs [M4, M5]; M5 and M4 prereqs [M2]; M2 prereqs [M1]; M1 prereqs [P0.1]. Closure M1, M2, M4, M5, M6, P0.1 matches the hub.")
row("SC1a-hub-concept-list", "2.9-structure", "course/modules/SC/SC1/index.html:61-67",
    "PASS", R + "concept links are in the prerequisite closure (M1, M2, M4, M5, M6, P0.1); check_dag PASS.")
row("SC1a-hub-cards-L01-L03", "2.7-cards-copy", "course/modules/SC/SC1/index.html:152-154",
    "PASS", R + "the three hub card blurbs match L01-L03 (Brownian definition and covariance; construction with Assumption A2; quadratic variation and t squared). cards.json is outside this slice; its SC1-c008 wording no longer contains 'all finite-dimensional vectors' (grep count 0).")
row("SC1a-hub-ladder-objectives", "2.9-structure", "course/modules/SC/SC1/index.html:45-56, :163-171",
    "PASS", R + "objectives and ladder re-read; the lesson numbers and Assumption A3 (stated in Lesson 5, L05.html:270) match.")
row("SC1a-simulated-labels", "2.5-labels", "course/modules/SC/SC1/L02.html:170 and :173 (lab-SC1-L02-1.py:3); L03.html:132 and :136",
    "PASS", R + "SIMULATED is stated on the L02 and L03 labs and their twins; L01's lab is exact and not labelled SIMULATED.")
row("SC1a-hub-data-status", "2.8-data", "course/modules/SC/SC1/index.html:37, :174-177; L01-L03",
    "PASS", R + "no real data is used in L01-L03 (no data-files attribute on any lab; grep).")
row("SC1a-dag-hub-prose", "2.9-dag", "course/modules/SC/SC1/index.html:33, :53, :150",
    "PASS", R + "check_dag PASS; the hub prose matches the curriculum prerequisites.")
row("SC1a-prose-L01-three-conditions", "2.9-prose", "course/modules/SC/SC1/index.html:49; L01.html:51",
    "PASS", R + "L01.html:51 now says 'defined in §1 (Definition 1.1) by three conditions'; Definition 1.1 has exactly (D1)-(D3); hub line 49 matches.")
row("SC1a-define-dyadic", "2.9-define-before-use", "course/modules/SC/SC1/L01.html:132 (dfn def-dyadic-partition), L02.html:71, L03.html:55",
    "PASS", R + "dyadic partition defined in L01 before its use in L02 and L03 (with links).")
row("SC1a-scope-L03-converge", "2.4-scope", "course/modules/SC/SC1/L03.html:270 (misconception 1)",
    "PASS", R + "the changed sentence 'their mean is the elapsed time for every partition' is correct by Theorem 2.3 (E Q = t for every partition).")
row("SC1a-hub-quiz-cross", "2.9-hub-quiz", "course/modules/SC/SC1/index.html:143 (skill check 2 explanation)",
    "PASS", R + "the explanation's count 29 = 22 + 7 for n=6, a=2 matches the enumeration (29) and project.html:206 expected output 29.")
row("SC1a-prose-two-sources", "2.1-citations", "course/modules/SC/SC1/index.html:184; references/references.json",
    "PASS", R + "index.html:184 states one registry key cited at book level; references.json contains shreve2004stochastic (line 20732) and no Karatzas record.")
row("SC1a-lab-L02-hypothesis-expected", "2.5-lab-claims", "course/modules/SC/SC1/L02.html:170 (hypothesis), :275-278 (interpretation)",
    "PASS", R + "216 cases (36 pairs), 8 of 8 bounds, 2^-m exceedance statement: all match the printed output and the code.")
row("SC1a-r4-twin-timing-and-purity", "2.5-labs", "tests/labs/SC1/lab-SC1-L01-1.py, lab-SC1-L02-1.py, lab-SC1-L03-1.py",
    "PASS", R + "each twin runs under python -I -W error, with no network and no file read (the twins read no data file), exit 0 and no stderr; run_labs PASS (11/11) applies its time limit to every lab.")
row("SC1a-r5-gaussian-process-scope-L01", "2.4-scope", "course/modules/SC/SC1/L01.html:107 (Remark 1.3 scope) and :115 (Gaussian process definition)",
    "PASS", R + "round 5 FAIL re-verified as fixed: L01.html:115 now defines the Gaussian process over vectors with 0<t_1<...<t_r, matching Remark 1.3 (L01.html:107). The cards.json sentence the round-5 note mentioned is no longer present (grep 0 matches).")
# new rows
row("SC1a-r6-variance-t0-L01", "2.4-math", "course/modules/SC/SC1/L01.html:67 ('Standard' paragraph)",
    "FAIL",
    R + "the paragraph says '(D2) gives Var(B_t)=t for every t>=0'. (D2) is stated for 0<=s<t, so with s=0 it gives Var(B_t)=t only for t>0; the t=0 case comes from (D1) (B_0=0, variance 0). The value is right, the attribution to (D2) alone is not.",
    "Change to: '(D1) and (D2) give Var(B_t)=t for every t>=0' at L01.html:67.")
row("SC1a-r6-quiz-mesh-hypothesis-L03", "2.4-quiz", "course/modules/SC/SC1/L03.html:437-443 (quiz item 5)",
    "FAIL",
    R + "the question asks 'Which hypothesis of Theorem 2.3 is the mesh condition?' with the keyed answer 'Assumption 3.1'. Theorem 2.3 lists only H1 and H2 (H2: Assuming Assumption 3.2, L03.html:101-103). Assumption 3.1 enters only in the conclusion ('Assuming also Assumption 3.1', L03.html:104). The keyed answer is therefore not a hypothesis of the theorem as written.",
    "Reword the question to 'Which assumption, added in the conclusion of Theorem 2.3, is the mesh condition?' (L03.html:437) and the explanation to match (L03.html:443).")

fragment = {
    "unit": "SC1",
    "slice": "SC1-a",
    "round": 6,
    "verifier": "Claude Haiku 5.5, independent verifier SC1-a round 6 (did not build SC1; re-read the full slice at 4bd8cb9; re-ran all gates; lab twins and numbers re-derived)",
    "pin": "4bd8cb94a8e171e80c4c34da1b3f32be7cb93f07",
    "base": "7376a5e2 (round-5 pin, E-SC1-a.round5.json). Slice delta 7376a5e..4bd8cb9: index.html (line 33 A3 cross-reference), L01.html (lines 51, 77, 115, 215-217, 329-336, 353, 434), L02.html (lines 51, 175-177 lab docstring), L03.html (lines 51, 59, 270), tests/labs/SC1/lab-SC1-L02-1.py (docstring). Lab twins L01 and L03 and their pages' code are byte-identical to the previous pin.",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE6-SC1-a (detached at 4bd8cb9, .venv symlinked; vendor present under course/assets/vendor)",
    "scratch": "ledgers/SC1/scripts/SC1-a-r6/ (recompute.py and recompute.out, build_fragment.py, gate and lab outputs, mutant outputs)",
    "verified_at": "2026-11-04",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [
        {"id": "SC1a-r6-lab-mut1-L01-min-to-max", "description": "lab-SC1-L01-1: covariance_from_increments uses max(i, j) instead of min(i, j) (sum over the wrong number of increments)", "killed_by": "run of the mutated twin: output line 'covariance equals min(s, t) on the grid: 9 of 81 pairs' differs from the expected block '81 of 81' (ledgers/SC1/scripts/SC1-a-r6/SC1a-r6-lab-mut1-L01-min-to-max.out)"},
        {"id": "SC1a-r6-lab-mut2-L02-scale", "description": "lab-SC1-L02-1: level-term supremum uses 2**(-m/2) instead of 2**(-(m+1)/2)", "killed_by": "run of the mutated twin: the bound and sup lines differ from the expected block, and 'grid supremum ... True' becomes False (ledgers/SC1/scripts/SC1-a-r6/SC1a-r6-lab-mut2-L02-scale.out)"},
        {"id": "SC1a-r6-lab-mut3-L03-closed-form", "description": "lab-SC1-L03-1: closed form uses 4N^2 + 1 instead of 4N^2 - 1", "killed_by": "run of the mutated twin: 'closed form matches: False' on all 16 rows, differing from the expected block (ledgers/SC1/scripts/SC1-a-r6/SC1a-r6-lab-mut3-L03-closed-form.out)"},
    ],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "Round 6 on 4bd8cb9. Full slice read (index.html 190 lines; L01 446; L02 561 including the lab; L03 505). "
        "Non-PASS rows: SC1a-math-L01-canon-construction (FAIL, the uniform U in canon item 1 is not supplied by the cited Remark 2.6 hypotheses or the sentence before it); "
        "SC1a-r6-variance-t0-L01 (FAIL, minor: (D2) alone does not give Var(B_0)=0); "
        "SC1a-r6-quiz-mesh-hypothesis-L03 (FAIL, minor: Assumption 3.1 is not a hypothesis of Theorem 2.3 as written). "
        "Not graded here: cards.json (outside this slice, grep checked only); run_graders and mutate_graders (no grader in this slice); the full pytest suite, render_curriculum, build_site --check and fetch_data --check (no curriculum, site data or market input changed in this slice); verify_refs live (no reference changed); the 50-seed sweep covered the L02 identities only, not the bound lines. "
        "Plan deviation noted, not a FAIL: the plan (Q5) asked for the [0,1] to [0,infinity) extension to be a labelled sketch; Remark 2.6 is proved under A2 and graded T with its hypotheses listed. "
        "The gate tool check_pages --page index is not the gate (see round 5 note); the unit-level run is used."
    ),
    "summary": (
        "SC1-a round 6 at 4bd8cb9: verdict FAIL. "
        f"{len(rows)} rows: {sum(1 for r in rows if r['status']=='PASS')} PASS, {sum(1 for r in rows if r['status']=='FAIL')} FAIL, 0 UNVERIFIABLE. "
        "Gates re-run and passing: check_pages, check_dag, check_projects, run_labs 11/11, page_smoke (index, L01-L03), ruff check and format, mypy, pytest -k SC1, verify_refs offline. "
        "Twins under python -I -W error equal the expected blocks. Three lab sanity mutants, all killed. Three FAIL rows, all in L01 or L03 prose."
    ),
}

import pathlib
out = pathlib.Path("ledgers/SC1/SC1-a.json")
out.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("rows", len(rows), "pass", sum(1 for r in rows if r['status']=='PASS'), "fail", sum(1 for r in rows if r['status']=='FAIL'))
