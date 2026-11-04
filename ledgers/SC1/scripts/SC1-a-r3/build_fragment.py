"""Write the round-3 SC1-a fragment from the verification results recorded in this round.

Run from the checkout root: .venv/bin/python ledgers/SC1/scripts/SC1-a-r3/build_fragment.py
"""

import json
from pathlib import Path

S = "ledgers/SC1/scripts/SC1-a-r3/out/"
G1 = "gates_1.txt (check_pages, check_dag, check_projects, run_labs 11/11, twins under python -I -W error)"
rows = []


def row(rid, check, loc, status, evidence, fix=None):
    r = {"id": rid, "check": check, "location": loc, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    rows.append(r)


row("SC1a-gate-check-pages", "2.9-structure-tool", "course/modules/SC/SC1/index.html, L01.html, L02.html, L03.html", "PASS",
    f"Re-run at 67a2d13e: tools/check_pages.py --unit SC1 printed 'check_pages SC1: PASS', exit 0 ({S}{G1}).")
row("SC1a-gate-check-dag", "2.9-dag-tool", "course/modules/SC/SC1/index.html, L01.html, L02.html, L03.html", "PASS",
    f"Re-run: tools/check_dag.py --unit SC1 printed 'check_dag SC1: PASS', exit 0 ({S}{G1}). Closure concept names checked separately in SC1a-hub-concept-list.")
row("SC1a-gate-run-labs", "2.5-labs-run", "tests/labs/SC1/lab-SC1-L01-1.py, lab-SC1-L02-1.py, lab-SC1-L03-1.py", "PASS",
    f"Re-run: run_labs.py --unit SC1 'PASS (11/11)', and --page L01, L02, L03 each PASS ({S}{G1}).")
row("SC1a-gate-page-smoke", "2.9-page-smoke", "course/modules/SC/SC1/index.html, L01.html, L02.html, L03.html", "PASS",
    f"Run alone: tools/page_smoke.py --unit SC1 --pages index L01 L02 L03 printed 'page_smoke SC1: PASS', exit 0; lab runtimes L01 0.0 s, L02 0.2 s, L03 0.1 s ({S}page_smoke.txt).")
row("SC1a-gate-lint-types-tests", "2.5-ruff-mypy-pytest", "tests/labs/SC1/lab-SC1-L01-1.py, lab-SC1-L02-1.py, lab-SC1-L03-1.py; tests/test_labs.py, test_run_labs.py, test_page_checks.py", "PASS",
    f"ruff check on the three twins: All checks passed; ruff format --check: 3 files already formatted; mypy --no-incremental: Success, 3 source files; pytest -q -k SC1 over the three test files: 11 passed, exit 0 ({S}gates_2.txt, {S}pytest_exit.txt).")
row("SC1a-gate-verify-refs", "2.1-citations", "course/modules/SC/SC1/index.html:182 (data-cite shreve2004stochastic)", "PASS",
    f"tools/verify_refs.py --offline: 'offline integrity: 560 entries, 0 problems'; tools/verify_refs.py --unit SC1 (live): 'live re-verification of SC1: 1 of 560 entries, 0 problems', exit 0 ({S}gates_2.txt, {S}verify_refs_live.txt).")
row("SC1a-lab-L01-twin", "2.5-lab-L01", "tests/labs/SC1/lab-SC1-L01-1.py; L01.html:137-206", "PASS",
    f"embed_check.py: page code equals twin (trailing newline ignored); python -I -W error exit 0, 0 stderr bytes; stdout 6 lines equal the expected block ({S}embed_check.txt; script ledgers/SC1/scripts/SC1-a-r3/embed_check.py).")
row("SC1a-lab-L02-twin", "2.5-lab-L02", "tests/labs/SC1/lab-SC1-L02-1.py; L02.html:159-251", "PASS",
    f"embed_check.py: page code equals twin; exit 0, 0 stderr bytes; stdout 12 lines equal the expected block at L02.html:251-262 ({S}embed_check.txt). Docstring claim checked in SC1a-lab-L02-docstring.")
row("SC1a-lab-L03-twin", "2.5-lab-L03", "tests/labs/SC1/lab-SC1-L03-1.py; L03.html:134-252", "PASS",
    f"embed_check.py: page code equals twin; exit 0, 0 stderr bytes; stdout 35 lines equal the expected block ({S}embed_check.txt). Printed values reproduced by recompute_r3.py ({S}recompute_r3.txt).")
row("SC1a-lab-claims-L01", "2.5-lab-claims", "tests/labs/SC1/lab-SC1-L01-1.py:5-7 (docstring, shown to the learner at L01.html:141-143); course/modules/SC/SC1/L01.html:207 (interpretation)", "FAIL",
    f"The docstring says the lab checks 'the algebra that Proposition 1.2 of the page proves in general: the increment variances over a dyadic partition of [0, t] sum to t, and the covariance ...'. Proposition 1.2 (L01.html:84-89) proves only the covariance identity; the dyadic variance sum is arithmetic from (D2) and is not a result of Proposition 1.2. L01.html:207 repeats it ('The lab checks the algebra of Proposition 1.2'). The printed numbers themselves reproduce (recompute_r3.py: 15 of 15, 81 of 81, Cov(B_1/4,B_5/8)=1/4; {S}recompute_r3.txt).",
    "Reword the twin docstring (and then re-embed with tools/embed_labs.py L01 --refresh) and L01.html:207 to attribute the dyadic sums to Definition 1.1 (D2) and the covariance identity to Proposition 1.2, e.g. 'the algebra of Definition 1.1 (D2) for the dyadic sums and of Proposition 1.2 for the covariance'. Keep the page code and the twin identical.")
row("SC1a-lab-claims-L03", "2.5-lab-claims", "course/modules/SC/SC1/L03.html:133 (hypothesis), :253 (interpretation), :343 (E1)", "PASS",
    f"Hypothesis: SE H*sqrt(2/N)/20 follows from Var(Q)=2H^2/N (Theorem 2.3 with Assumption 3.2) and 400 paths; recomputed. Interpretation: largest |z| 2.39 at H=1,N=2 and next 1.84 (recompute_r3.txt); SE 0.0718 vs 0.0707 at H=1,N=1; 0.0125 at H=2,N=128 ({S}recompute_r3.txt).")
row("SC1a-numbers-L01", "2.2-numbers", "course/modules/SC/SC1/L01.html:132, :229, :298, :305, :348-352, :393, :398, :412, :426", "PASS",
    f"Recomputed with exact Fractions and sqrt: 1/2, 1/10, sd of increment 1/2 at h=1/4, 10 at h=1/100, 3/64 x 16 = 3/4, 1/4 = Cov(B_{{2/8}},B_{{5/8}}), 81 pairs, Var(3B1-B2)=5, E[B_3^2]=3 ({S}recompute_r3.txt, L01 section).")
row("SC1a-numbers-L02", "2.2-numbers", "course/modules/SC/SC1/L02.html:263, :385, :392, :399, :405-406, :444, :486, :493, :514-516", "FAIL",
    f"Printed lab numbers reproduced by recompute_r3.py and seed_identity_check.py (216 of 216, 8 of 8, sups and bounds, 0.348139, 1.309399). Prose at L02.html:406 (E3) says 'the printed value implies |xi_{{1,1}}| approximately 0.233178'. The unrounded value is 2 x 0.11658934... = 0.23317869..., which rounds to 0.233179 at six decimals. 0.233178 is twice the displayed digits 0.116589, not a value computed from unrounded numbers ({S}recompute_r3.txt, E3 line). Other prose numbers at :263 (36 pairs, 17 distinct points), :392, :399 (216), :514-516 (9 points), :444 reproduce.",
    "At L02.html:406 replace 0.233178 with 0.233179 (unrounded 0.2331787), or write 'twice the printed 0.116589, that is 0.233178'. State the rounding rule once if the unrounded value is quoted.")
row("SC1a-numbers-L03", "2.2-numbers", "course/modules/SC/SC1/L03.html:253, :270, :275, :343, :350, :357, :368, :375, :398, :434, :457, :475", "PASS",
    f"Recomputed: 2.65625 = 16*255/1536; 0.0125 = 2*sqrt(2/128)/20; 0.625 = 15/24; 0.166664 and 0.010417 match closed form; 1/8 and sqrt(2/pi) identities; z values and SE gaps from recompute_r3.txt.")
row("SC1a-grade-L01", "2.3-grades", "course/modules/SC/SC1/L01.html:83, :101, :119, :349-352", "PASS",
    "Proposition 1.2 (T, Assuming A1(a)), Remark 1.3 (T, A1(a),(b)), Example 1.4 (T), key-results rows T with the assumptions named. Independently regraded: all T claims are proved on the page.")
row("SC1a-grade-L02", "2.3-grades", "course/modules/SC/SC1/L02.html:74, :93, :110, :134, :274, :287, :436-447", "PASS",
    "Lemma 2.2, 2.1, 2.3 (T), Proposition 2.4 (T), Theorem 2.5 (T, under A2), Remark 2.6 (T, under A1(a),(b),(e) and A2), key-results rows match. A2 is stated with its sketch labelled as one (L02.html:266-271).")
row("SC1a-grade-L03", "2.3-grades", "course/modules/SC/SC1/L03.html:77, :90, :99, :118, :394-398", "PASS",
    "Lemma 2.1, 2.2, Theorem 2.3, Proposition 2.4 graded T with proofs on the page; the Lab 1 row is graded C with basis 'Lab 1 (SIMULATED), one seed, 400 paths', matching BLUEPRINT section 3.")
row("SC1a-math-L01-prop1.2", "2.4-math", "course/modules/SC/SC1/L01.html:92-99", "PASS",
    "Proof re-derived: symmetry; s=0 and s=t cases; (D3) with t0=0,t1=s,t2=t gives independence of B_s and B_t-B_s; A1(a) gives E[XY]=0; Cov = s = min(s,t). Integrability by Cauchy-Schwarz (unnumbered standard inequality, not a prerequisite fact the hub names).")
row("SC1a-math-L01-remark1.3", "2.4-math", "course/modules/SC/SC1/L01.html:101-113", "PASS",
    "Re-derived: increments independent by (D3), normal by (D2), linear combinations normal by A1(b), covariance by Prop 1.2 (A1(a)). Assumptions A1(a),(b) named in the statement.")
row("SC1a-math-L01-canon-construction", "2.4-math", "course/modules/SC/SC1/L01.html:214 (canon-break 1), :215, :233", "PASS",
    "Re-derived: B~_t = B_t + 1{t=U} has the same finite-dimensional laws as B since P(U in F)=0 for finite F; (D1)-(D3) hold; B~_U = B_U + 1 and B~ is discontinuous at U on every outcome. Ungraded canon-break wording at :216 is in SC1a-canon-breaks-ungraded.")
row("SC1a-math-L02-lemmas-2.1-2.2", "2.4-math", "course/modules/SC/SC1/L02.html:73-107", "PASS",
    "Re-derived Lemma 2.2 (a)-(e) and Lemma 2.1 (MGF e^{theta^2/2}, indicator bound, theta=lambda, two-sided sum 2e^{-lambda^2/2}). Lemma 2.1 cites monotonicity of the integral by name (L02.html:105); that unnumbered attribution is in SC1a-assump-prereq-facts.")
row("SC1a-math-L02-lemma2.3-arithmetic", "2.4-math", "course/modules/SC/SC1/L02.html:121-128", "PASS",
    "Re-derived: c=2^{-(n+2)/2}; U_j, V_j variance 2^{-(n+2)}+2^{-(n+2)}=2^{-(n+1)}; covariance 2^{-(n+2)}-2^{-(n+2)}=0; A1(e) block independence; recomputed the identities for n=0..4 (recompute_r3.txt).")
row("SC1a-math-L02-prop2.4", "2.4-math", "course/modules/SC/SC1/L02.html:142-154", "PASS",
    "Re-derived union bound 2^{m-1}*2e^{-lambda_m^2/2}=2^{-m} (asserted numerically); summability sum m r^m; Cauchy argument; continuity step. Identity M_m = sqrt(2 log2) sqrt(m) 2^{-m/2} asserted numerically (recompute_r3.py).")
row("SC1a-math-L02-A2-sketch", "2.4-math", "course/modules/SC/SC1/L02.html:266-271", "PASS",
    "Labelled 'Sketch, not a proof'; names the skipped step (passage of characteristic functions and joint version). Lemma 2.3 proves A2 for dyadic times only, as stated.")
row("SC1a-math-L02-thm2.5", "2.4-math", "course/modules/SC/SC1/L02.html:273-285", "PASS",
    "Re-derived: B_0=0 via P2 (S_M(0)=0); (D2),(D3) via A2; continuity on Omega*, zero off it. Hypothesis A2 named.")
row("SC1a-math-L03-thm2.3", "2.4-math", "course/modules/SC/SC1/L03.html:99-115", "PASS",
    "Re-derived: E[Q]=t by Lemma 2.2; Var(Q)=sum 2 Delta_k^2 by Assumption 3.2(a),(b); sum Delta_k^2 <= |P| t; mean-square limit under 3.1. All assumptions named.")
row("SC1a-math-L03-prop2.4", "2.4-math", "course/modules/SC/SC1/L03.html:117-129", "PASS",
    "Re-derived: (b^2-a^2)^2 <= 4H^2(b-a)^2; sum bound 4H^3|P|; equal-step sum H^4(4N^2-1)/(3N^3) by induction with S(N)=sum (2j+1)^2 = N(4N^2-1)/3 (checked in recompute_r3.py and by exact Fractions for N=1..128).")
row("SC1a-math-L03-misc-claims", "2.4-math", "course/modules/SC/SC1/L03.html:259-261, :270, :274-279, :366-382", "PASS",
    "Re-derived: E|Z|=sqrt(2/pi) by P3; counterexample N X_N^2 has variance 2t^2 for every N; R2 least constant c=2; misconception 2 expectation sqrt(2Nt/pi) (recomputed: 2.256758 at N=8, t=1).")
row("SC1a-exercises-L01-L03", "2.4-problems", "course/modules/SC/SC1/L01.html:243-331, :357-427; L02.html:331-427, :446-520; L03.html:286-383, :404-476", "FAIL",
    "Every worked solution re-derived. One solution number is wrong at the last displayed digit: L02.html:406 (Problem E3) gives |xi_{1,1}| approximately 0.233178; the unrounded value is 0.2331787, which rounds to 0.233179 (see SC1a-numbers-L02). All other solutions and quiz explanations reproduce (L03 E2 2.65625, E3 0.0125, R1 2t^2/N, R2, R3; L01 M1-M3, P1-P3, E1-E3, R1-R3).",
    "Fix L02.html:406 as stated in SC1a-numbers-L02.")
row("SC1a-misconceptions-canon", "2.4-canon", "course/modules/SC/SC1/L01.html:219-235, L02.html:307-330, L03.html:256-281", "PASS",
    "Each misconception has a wrong belief, a reason, and evidence; L02 harmonic-series argument recomputed (partial sum >= 1 + k/2); L03 E|Z| argument consistent.")
row("SC1a-notation-macros", "2.4-notation", "course/modules/SC/SC1/index.html, L01.html, L02.html, L03.html", "PASS",
    f"notation_scan.py ({S}notation_scan.txt): registered macros used are \\E, \\Prob, \\Var, \\Cov, \\Normal, \\indic; no unregistered custom macro. Standard TeX commands (\\Lambda, \\sum, \\varphi and similar) are not program macros. One standard blackboard form, \\mathbb Z at L02.html:78, has no registry entry; it is not a registered symbol and collides with nothing (observation, not a row failure).")
row("SC1a-notation-no-registered-collision", "2.4-notation", "course/modules/SC/SC1/L01.html, L02.html, L03.html", "PASS",
    f"notation_scan.py: the only bare T in math is the reserved-symbol mention at L03.html:120; no Phi, gamma, R*, R_f, or \\mathbb{{Q}} in the slice; plain Q is the quadratic variation (not the registered \\mathbb{{Q}}); N, S, m, c, sigma-type letters are local per notation.json.")
row("SC1a-notation-T-subscript", "2.4-notation", "course/modules/SC/SC1/L02.html:431 (R3 solution, formerly T_m)", "PASS",
    f"Round-2 defect fixed: the R3 solution now uses Y_m (L02.html:431). notation_scan.txt shows no T used as a level term in L02. The page and twin use Y_m consistently.")
row("SC1a-notation-H-horizon", "2.4-notation", "course/modules/SC/SC1/L03.html:120, :122, :128, :133; tests/labs/SC1/lab-SC1-L03-1.py", "PASS",
    "H is the horizon throughout L03 and in the twin (HORIZONS=(1.0, 2.0)); the reserved T is named once at :120 as the notation.json meaning requires.")
row("SC1a-grade-L02-remark2.6", "2.4-math", "course/modules/SC/SC1/L02.html:287-302", "PASS",
    "Re-derived: W_t = sum of unit copies plus the fractional piece; continuity at integers; (D2) and (D3) via refinement with distinct independent copies, A1(a),(b),(e) and A2 named as H2.")
row("SC1a-math-L03-density", "2.4-math", "course/modules/SC/SC1/L03.html:78 (Lemma 2.1 density), :332 (P3)", "PASS",
    "phi is the standard normal density in both places; P3 uses zphi(z) = -phi'(z) consistently with Lemma 2.1.")
row("SC1a-process-words", "2.9-prose", "course/modules/SC/SC1/index.html, L01.html, L02.html, L03.html; tests/labs/SC1/lab-SC1-L01-1.py, lab-SC1-L02-1.py, lab-SC1-L03-1.py", "PASS",
    f"grep for build, builder, round, verifier, REQUEST, unit report in learner text: only content uses ('This module builds', 'the rounded/rounding' wording, 'does not verify the limit'); no process words ({S}process_banned_wordcount.txt).")
row("SC1a-banned-phrases", "2.9-prose", "course/modules/SC/SC1/index.html, L01.html, L02.html, L03.html", "PASS",
    f"Banned strings (TODO, TBD, lorem, for brevity, details omitted, beyond the scope, left as an exercise, you can add more, it is important to note, studies show, experts agree, it is well known, obviously, clearly) and ellipses: 0 hits outside code ({S}process_banned_wordcount.txt); check_pages PASS.")
row("SC1a-structure-L01-L03", "2.9-structure", "course/modules/SC/SC1/L01.html, L02.html, L03.html", "PASS",
    f"why-it-matters words: L01 99, L02 98, L03 117 (limit 120; {S}process_banned_wordcount.txt). Misconceptions 3 each. Problems 3 per tier per lesson with details.solution. Quiz 10 items each (8 to 15). Canon-breaks present. Key-results table present. Hours data-hours=9 each. Structure order as BUILDER_RULES 4.2.")
row("SC1a-scope-words-L02-L03", "2.4-scope", "course/modules/SC/SC1/L02.html:122, :139, :158, :263, :316, :385, :417; L03.html:85, :104, :115, :261, :278", "PASS",
    "Each 'every', 'all', 'always', 'any', 'exactly', 'converge' claim re-read: each is computed (dyadic identities over 216 cases, sums per level), proved, or stated as a mean-square statement; L03:115 and :261 disclaim a pathwise limit.")
row("SC1a-simulated-labels", "2.5-labels", "course/modules/SC/SC1/L02.html:158 and lab-SC1-L02-1.py:1-6; L03.html:132-133 and lab-SC1-L03-1.py:1-3", "PASS",
    "SIMULATED label present on the L02 and L03 lab hypotheses and in both twin docstrings. L01 and the L01 lab use no generated paths and carry no SIMULATED label, correctly.")
row("SC1a-hub-hours", "2.9-hours", "course/modules/SC/SC1/index.html:29, :39-42, :150; project.html:33, :262-273", "PASS",
    "data-hours-lessons=72, data-hours-project=28; eight lesson pages each data-hours=9 (grep on L01-L08); 72+28=100; check_projects PASS for the project hours table.")
row("SC1a-hub-placement", "2.9-structure", "course/modules/SC/SC1/index.html:72-145", "PASS",
    "Nine items; seven prerequisite items and two data-skill items; mastery 0.8; 7/9=77.8%, 8/9=88.9% (recomputed); skill checks are data-skill.")
row("SC1a-hub-prereq-chain", "2.9-structure", "course/modules/SC/SC1/index.html:35, :58-68; curriculum/curriculum.json (parts)", "PASS",
    "Curriculum json: SC1 prereqs [M6]; M6 prereqs [M4, M5]; M4 [M2]; M5 [M2]; M2 [M1]; M1 [P0.1]; P0.1 []. Hub text at :60 matches.")
row("SC1a-hub-concept-list", "2.9-structure", "course/modules/SC/SC1/index.html:61-67", "PASS",
    "All 24 concepts named in the hub exist in curriculum.json for M1, M2, M4, M5, M6 and P0.1 (geometric-series, proof-by-contradiction, limit, derivative, random-variable, normal-distribution, multivariate-normal, independence, expectation, variance, moment-generating-function, characteristic-function, cauchy-sequence, completeness-of-reals, uniform-convergence, probability-space, sigma-algebra, filtration, martingale, stopping-time, optional-stopping-theorem, dominated-convergence-theorem, evidence-grade, project-ladder).")
row("SC1a-hub-cards-L01-L03", "2.7-cards-copy", "course/modules/SC/SC1/index.html:152-154", "PASS",
    "Hub card text for L01-L03 matches each lesson's content (Definition 1.1, Prop 1.2, Example 1.4, Assumption A2 in L02, Theorem 2.3, Proposition 2.4). No cards.json content judged here.")
row("SC1a-hub-grade-definition", "2.3-grades", "course/modules/SC/SC1/index.html:79; BLUEPRINT.md:158", "PASS",
    "The T definition 'A theorem, proved on the page or with a precisely cited proof' matches BLUEPRINT section 3 (grade T row).")
row("SC1a-hub-ladder-objectives", "2.9-structure", "course/modules/SC/SC1/index.html:45-56, :163-171", "PASS",
    "Six objectives with measurable verbs (Define, Construct, Prove, Verify, State, Prove) mapped to Lessons 1 to 8; ladder rungs 1 to 4 present; rung headings in project.html (lines 41-47 ladder, 52 rungs 1-2, 208 rung 3, 294 report) match the hub's four-rung description.")
row("SC1a-hub-data-status", "2.8-data", "course/modules/SC/SC1/index.html:37, :174-177", "PASS",
    "grep -c data-files on index.html, L01, L02, L03: 0 on each; no MANIFEST entry used; SIMULATED labels as in SC1a-simulated-labels.")
row("SC1a-dag-hub-prose", "2.9-dag", "course/modules/SC/SC1/index.html:33, :53, :150", "PASS",
    "Hub prose mentions only closure concepts and SC1 concepts; no SC2/SC3 term (Ito, SDE, Girsanov, Ornstein, geometric Brownian motion) appears in the slice (grep).")
row("SC1a-reference-section-L02-L03", "2.1-citations", "course/modules/SC/SC1/L01.html:433; L02.html:532; L03.html:491", "PASS",
    "Each reference section states no passage is attributed; L03 names shreve2004stochastic at book level with no locator. No unregistered citation.")
row("SC1a-attrib-L01-A1-parts", "2.4-assumptions", "course/modules/SC/SC1/L01.html:37, :72-80", "PASS",
    "A1 has parts (a) to (e) as the uses line says; parts are standard facts of M4 and M6 stated without proof and labelled as such (:80).")
row("SC1a-assump-L01-P3", "2.4-assumptions", "course/modules/SC/SC1/L01.html:285-287", "PASS",
    "P3 says 'Assuming A1(a)' and uses it only for symmetry plus Proposition 1.2, which itself uses A1(a).")
row("SC1a-scope-L01-prop1.2-only", "2.4-scope", "course/modules/SC/SC1/L01.html:216 (canon-break 3)", "PASS",
    "Statement that Proposition 1.2 still holds with a non-normal law of the same mean and variance is correct (the proof uses only mean, variance, independence, A1(a)). The companion 'breaks Remark 1.3' claim is in SC1a-canon-breaks-ungraded.")
row("SC1a-ref-L01-every-result", "2.1-citations", "course/modules/SC/SC1/L01.html:433", "PASS",
    "'Every result is proved on this page from Definition 1.1 and, where it says so, from Assumption A1' holds for the results in L01: the proofs use only (D1)-(D3), A1(a)-(b), and the Cauchy-Schwarz inequality for integrability (a standard inequality, observation only). The unnumbered prerequisite attributions are in L02 and are in SC1a-hub-assumption-promise.")
row("SC1a-numbers-L02-36-points", "2.2-numbers", "course/modules/SC/SC1/L02.html:263", "PASS",
    "36 (depth, point) pairs = 2+3+5+9+17; 17 distinct points at depth 4; each compared with levels n..8 gives 216 (recompute_r3.txt).")
row("SC1a-attrib-L02-lemma2.1-union", "2.4-attribution", "course/modules/SC/SC1/L02.html:158, :263", "PASS",
    "Union bound over 2^{m-1} coefficients with Lemma 2.1 gives 2^{-m}; the lab text attributes the bound to Lemma 2.1 correctly (asserted numerically).")
row("SC1a-assump-L02-grouping", "2.4-assumptions", "course/modules/SC/SC1/L02.html:113, :127-128", "PASS",
    "Lemma 2.3 H2 names A1(b), A1(c), A1(e); the proof uses A1(e) for grouping and A1(c) for uncorrelated jointly normal variables. Consistent.")
row("SC1a-define-dyadic", "2.9-define-before-use", "course/modules/SC/SC1/L01.html:132 (first use of dyadic partition), L02.html:71 (dyadic time, dyadic partition), L03.html:55", "PASS",
    "Round-2 defect fixed: L01.html:132 now defines 'dyadic partition' in a plain <dfn id=\"def-dyadic-partition\">; L02.html:71 defines 'dyadic time' and links the partition to L01; L03.html:55 links to L01. First occurrences checked by grep (L01 first at :132, L02 first at :71, L03 first at :55).")
row("SC1a-numbers-L03-SE-follow", "2.2-numbers", "course/modules/SC/SC1/L03.html:398 (key-results row, grade C)", "PASS",
    "Re-computed gaps: max |gap| 13.22% (unrounded), 13.21% from 4-decimal printed values, at H=2,N=1; all 16 gaps within 14% (recompute_r3.txt). Row wording matches.")
row("SC1a-scope-L03-converge", "2.4-scope", "course/modules/SC/SC1/L03.html:270 (misconception 1)", "PASS",
    "'For s to s^2 the sums vanish in the limit, and for Brownian motion their mean converges to the elapsed time, with mean-square error tending to zero' is Proposition 2.4(a) and Theorem 2.3; 'mean converges' is an identity E[Q]=t, not a pathwise statement.")
row("SC1a-hub-quiz-cross", "2.9-hub-quiz", "course/modules/SC/SC1/index.html:143 (skill check 2 explanation)", "FAIL",
    f"The explanation says 'The count is the completion line of rung 2.' The rung-2 completion (course/modules/SC/SC1/project.html:158-200, lab-SC1-project-2.py) computes the walks for n=6, a=2 and prints 'walks with maximum >= a: 29' (out/rung2_count.txt). It does not print 2. The hub's count 2 is the same reflection count for n=2, a=1 ({S}rung2_count.txt).",
    "Reword index.html:143 to: 'The count is the reflection count of rung 2 for n = 2 and a = 1; rung 2 computes the same quantity for n = 6 and a = 2.' Keep the answer 2.")
row("SC1a-lab-L02-docstring", "2.5-lab-claims", "tests/labs/SC1/lab-SC1-L02-1.py:1-7 (docstring, shown at L02.html:159)", "PASS",
    f"Round-2 defect fixed. seed_identity_check.py ({S}seed_identity_check.txt): the dyadic line is '216 of 216' and the grid-sup line is True for all 300 seeds tested, so 'identities that hold for every seed' is true; the bound lines are the sample-dependent ones.")
row("SC1a-prose-L01-three-conditions", "2.9-prose", "course/modules/SC/SC1/index.html:49; course/modules/SC/SC1/L01.html:51", "PASS",
    "Round-2 defect fixed: both places now say 'three conditions on the process and its increments' (D1 concerns B_0, D2 and D3 the increments). Consistent with L01.html:61-63.")
row("SC1a-attrib-L02-eponym", "2.1-citations", "course/modules/SC/SC1/L02.html:7 (meta description); tests/labs/SC1/lab-SC1-L02-1.py:1 (docstring)", "PASS",
    f"Round-2 defect fixed: grep -i 'ciesielski|lévy|levy' over index.html, L01-L03 and the three twins: 0 matches (run at 67a2d13e). The construction is described without an eponym.")
row("SC1a-hub-assumption-promise", "2.4-assumptions", "course/modules/SC/SC1/index.html:69 (promise), :184 (promise); L02.html:105 ('monotonicity of the integral, M6'), L02.html:152 ('by completeness of the reals (M5)')", "FAIL",
    "index.html:69 promises: 'Where a lesson uses a standard fact of a prerequisite that the page does not prove, the fact is stated as a numbered Assumption in that lesson.' index.html:184 says every result is 'proved on its page from the numbered Assumptions it names'. L02 uses two named prerequisite facts with no numbered Assumption: monotonicity of the integral (M6) in Lemma 2.1 (L02.html:105) and completeness of the reals (M5) in Proposition 2.4 step 3 (L02.html:152). Neither is in A1 or A2, so the promise is not kept. Remark 2.6 and Lemma 2.3 use A1 parts only.",
    "Either add numbered Assumption items to L02 for completeness of the reals and monotonicity of the integral (and cite them as 'Assuming A3...' style items), or delete the two parenthetical attributions and state them as used Assumptions; then make index.html:69 and :184 match what the lessons do.")
row("SC1a-canon-breaks-ungraded", "2.3-grades", "course/modules/SC/SC1/L02.html:310 ('Dyadic times do not determine the laws at other times'); course/modules/SC/SC1/L01.html:216 ('A non-normal increment law breaks Remark 1.3')", "FAIL",
    "Two substantive 'canon-break' claims are asserted with no grade, no proof and no counterexample. L02:310 states a general fact about laws at non-dyadic times. L01:216 says a non-normal increment law breaks Remark 1.3; the text gives only the reason that A1(b) concerns normal variables, not an example in which the conclusion (multivariate normality) fails. BUILDER_RULES section 2.2 requires a grade on every substantive claim.",
    "Give each a counterexample or a grade with its basis. For L01:216, a two-point increment law (for example B_1 = +-1 with probability 1/2 each) gives a marginal that is not normal, so the vector is not multivariate normal. For L02:310, a process equal to B at dyadic times and differing at a non-dyadic time gives a different law there. Either state the example or grade the claim C with its basis.")

frag = {
    "unit": "SC1",
    "slice": "SC1-a",
    "round": 3,
    "verifier": "Haiku independent verifier, SC1-a round 3 (did not build SC1; round-2 PASS rows were re-verified in this round, not carried)",
    "pin": "67a2d13e",
    "base": "67c47689 (round-2 pin). Slice files changed since then: course/modules/SC/SC1/index.html, L01.html, L02.html, L03.html and tests/labs/SC1/lab-SC1-L02-1.py (see git diff 67c47689..67a2d13e -- those paths). lab-SC1-L01-1.py and lab-SC1-L03-1.py unchanged.",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE3-SC1-a (detached at 67a2d13e, .venv symlinked)",
    "scratch": "ledgers/SC1/scripts/SC1-a-r3/ (embed_check.py, recompute_r3.py, notation_scan.py, seed_identity_check.py, build_fragment.py; outputs under out/)",
    "verified_at": "2026-11-04",
    "verdict": "FAIL",
    "slice_files": [
        "course/modules/SC/SC1/index.html (190 lines)",
        "course/modules/SC/SC1/L01.html (445 lines)",
        "course/modules/SC/SC1/L02.html (545 lines)",
        "course/modules/SC/SC1/L03.html (504 lines)",
        "tests/labs/SC1/lab-SC1-L01-1.py (64 lines)",
        "tests/labs/SC1/lab-SC1-L02-1.py (92 lines)",
        "tests/labs/SC1/lab-SC1-L03-1.py (84 lines)",
    ],
    "rows": rows,
    "mutants": [],
    "registry_flags": [
        "shreve2004stochastic: live verify_refs --unit SC1 '1 of 560 entries, 0 problems' at 67a2d13e; the only key the slice cites, at book level with no locator.",
        "Karatzas and Shreve (second curriculum source) has no record in references/references.json (grep: no match); the hub says so at index.html:184.",
    ],
    "freshness_flags": [],
    "notes": [
        "Mutation testing not applicable to this slice: the lab twins are demonstrations (architect ruling). No project grader is in slice a, so no mutants are listed; run_graders and mutate_graders were not run.",
        "Every round-2 row is re-verified in this round (none carried). Round-2 FAIL rows SC1a-notation-T-subscript, SC1a-define-dyadic, SC1a-lab-L02-docstring, SC1a-prose-L01-three-conditions, SC1a-attrib-L02-eponym are now PASS with the cited evidence.",
        "Seed sensitivity: the L02 lab's identity lines hold for 300 seeds (seed_identity_check.py); the bound lines are sample-dependent, as the page says.",
        "Round-2 observation carried as an accepted wording point: index.html:143 is now a FAIL (SC1a-hub-quiz-cross), because the rung-2 completion prints 29 for n=6, a=2.",
        "Citation markup: BLUEPRINT section 3 asks for a citation key on every substantive claim; the architect restricts citations to shreve2004stochastic and the SC1 pages cite no key on derived results. Accepted as the architect decision (not a row).",
        "Not judged in slice a (other slices): cards.json, project.html, grader, L04 to L08 (read only for data-hours and the hub's 'every result' claim), lab-SC1-L04..L08, project labs.",
    ],
    "summary": "",
}
statuses = [r["status"] for r in rows]
frag["summary"] = (f"SC1-a round 3: verdict FAIL. {len(rows)} rows: {statuses.count('PASS')} PASS, {statuses.count('FAIL')} FAIL, "
                   f"{statuses.count('UNVERIFIABLE')} UNVERIFIABLE. Gates re-run at 67a2d13e and all pass (check_pages, check_dag, check_projects, run_labs 11/11, twins under python -I -W error, page_smoke on the four pages alone, ruff, mypy, pytest -k SC1 11 passed, verify_refs offline and live SC1). "
                   "Open FAILs: lab-claims-L01 (Proposition 1.2 attributed with the dyadic sum), numbers-L02 and exercises (0.233178 vs unrounded 0.233179 at L02:406), hub-quiz-cross (index:143 'completion line of rung 2' prints 29), hub-assumption-promise (completeness and monotonicity cited without numbered Assumptions), canon-breaks-ungraded (L02:310, L01:216).")
Path("ledgers/SC1/SC1-a.json").write_text(json.dumps(frag, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(len(rows), statuses.count("PASS"), statuses.count("FAIL"))
