"""Builds ledgers/M7/M7-b.json (round 4) from the round 3 row ids plus the round 4 rows.

Every round 3 id is kept. Status and evidence are the round 4 results recorded by the verifier.
"""

import datetime
import json
import pathlib

ROOT = pathlib.Path("/tmp/verifyB4-M7-b")
R3 = pathlib.Path("/tmp/fanout-frags/B-M7-b.round3.json")

RE = "Re-verified in round 4 on pin 2657ab5 (L04-L06 pages and cards changed since aa3c26c): "

P = {}  # id -> (status, evidence, fix)


def ok(i, ev):
    P[i] = ("PASS", ev, "")


def bad(i, ev, fix):
    P[i] = ("FAIL", ev, fix)


ok("M7b-cmd-check-pages", RE + "`.venv/bin/python tools/check_pages.py --unit M7 --page L04` (and --page L05, --page L06) -> 'check_pages M7 L04: PASS', 'L05: PASS', 'L06: PASS' (rc 0).")
ok("M7b-cmd-check-dag", RE + "`.venv/bin/python tools/check_dag.py --unit M7` -> 'check_dag M7: PASS' (rc 0).")
bad(
    "M7b-dag-prose-terms",
    RE
    + "Links on L04-L06 point to closure or own-unit concepts (data-concept at L04.html:37,59; L05.html:38-39,60; L06.html:38-39,65,120). "
    "The plan's section 2 table lists `variance` as an M4 concept outside the closure, and the page uses it by name without a link "
    "(L06.html:52, 90, 150, 405, 424, 549, 586; see M7b-r4-L06-variance-term). Prose-only 'efficient frontier' (L06.html:87, 149) and "
    "'convexity' (L04.html:76, 275, 412, 503) are not on the link list, so they pass.",
    "Remove the by-name M4 term 'variance' from L06 prose as M7b-r4-L06-variance-term requires.",
)
ok(
    "M7b-cmd-run-labs",
    RE + "`.venv/bin/python tools/run_labs.py --unit M7 --page L04` (and L05, L06) -> 'run_labs M7: PASS (1/1)' each. "
    "The runner reports the unit, so the three runs are the same unit check.",
)
ok("M7b-lab-L04-twin-run", RE + "`.venv/bin/python -I -W error tests/labs/M7/lab-M7-L04-1.py` exit 0; embed check (ledgers/M7/scripts/M7-b-r4/embed_compare.py): 'L04 code == twin: True', 'L04 expected == run output: True'.")
ok("M7b-lab-L05-twin-run", RE + "`python -I -W error tests/labs/M7/lab-M7-L05-1.py` exit 0; embed check: 'L05 code == twin: True', 'L05 expected == run output: True'. Output matches the page block at L05.html:367-389 line by line.")
ok("M7b-lab-L06-twin-run", RE + "`python -I -W error tests/labs/M7/lab-M7-L06-1.py` exit 0 (output saved at ledgers/M7/scripts/M7-b-r4/lab-M7-L06-1.run.txt); embed check: 'L06 code == twin: True', 'L06 expected == run output: True'.")
ok("M7b-lab-lint-types", RE + "`.venv/bin/ruff check tests/labs/M7` -> 'All checks passed!'; `ruff format --check tests/labs/M7` -> '11 files already formatted'; `.venv/bin/mypy --no-incremental` on the three slice twins -> 'Success: no issues found in 3 source files'.")
ok("M7b-lab-pytest", RE + "`.venv/bin/pytest -q tests/test_labs.py -k M7` -> 11 tests, '[100%]', no failures. (Selection by -k M7; the whole file was not run.)")
ok("M7b-smoke", RE + "`.venv/bin/python tools/page_smoke.py --unit M7 --pages L04 L05 L06` -> 'page_smoke modules/M/M7/L06.html: PASS', 'page_smoke M7: PASS'; lab-M7-L06-1 0.0 s, runtime boot 1.1 s.")
ok("M7b-refs-live", RE + "`.venv/bin/python tools/verify_refs.py --unit M7` -> 'live re-verification of M7: 2 of 560 entries, 0 problems' (ledgers/M7/scripts/M7-b-r4/verify_refs_live_M7.txt); `verify_refs.py --offline` -> '560 entries, 0 problems'. data-references on L04, L05, L06 are empty (the slice cites no key).")
ok("M7b-citation-boyd-attribution", RE + "`grep -ci boyd` on L04.html, L05.html, L06.html, cards.json -> 0 each. No bibliographic claim is attributed to Boyd in the slice.")
ok(
    "M7b-2.2-numbers-L04",
    RE + "ledgers/M7/scripts/M7-b-r4/indep_r4.py (Fraction arithmetic, own code), output indep_r4.out: g(0,0) = -199/300 (L04.html:247, 324); mu'Sigma^-1 mu = 199/150; "
    "weak duality 27951 of 27951 pairs (L04.html:241); largest grid dual -1/2 attained at one point; smallest primal -1/2 at (1,0); grid gap 0 (L04.html:243-245); "
    "g(0,-3/5) = g(0,-7/10) = -157/300 and g(0,-13/20) = -209/400 (L04.html:397-399); R3 grid gap 7/300; KKT dual value -1/2 (L04.html:415, 121).",
)
ok(
    "M7b-2.2-numbers-L05",
    RE + "indep_r4.py: x = (13,3,3)/19, lambda = (-36,11)/19, det K = 19 (L05.html:370-372); objective 29/38 = 551/722 = 0.7631578947 (L05.html:375, E1 L05.html:482); "
    "v'Qv = 19 with Qv = (-7,2,3) (L05.html:611); Part B f(3/2,0) = -9/4; grid 1089 points, none below (L05.html:387-389, 390); Example 3.6 gradient (0, 5/2) (L05.html:176).",
)
ok(
    "M7b-2.2-numbers-L06",
    RE + "indep_r4.py with an independent LCG: M, mu = (7/100, 1/20, 3/25, 1/50), Sigma diagonal (49/40, 27/20, 103/80, 103/80) (L06.html:405); "
    "Part A return, variance, objective at gamma = 1, 2, 4, 8, 16 match the printed six-place values (page output block L06.html:376-387 and interpretation L06.html:405); "
    "Part B zero set {A4} and one passing candidate per gamma; constrained weights at gamma = 1 (0.388425, 0.203679, 0.407895, 0); "
    "unrounded turnover at gamma = 4 is 0.5588607333 (L06.html:511); unrounded E2 difference 0.5722548316 (L06.html:504).",
)
ok(
    "M7b-2.2-misc-numbers",
    RE + "Checked against indep_r4.out: L06.html:405 (weights 0.434783..-0.524154 and 0.388425..0 at gamma = 1; return 0.113798 -> 0.106241; variance 0.123809 -> 0.115780 monotone), "
    "L06.html:428 (four weights at gamma = 1), 504 (E2), 511 (E3); L05.html:390 and 482; L04.html:287 (49/300) and 291 (-199/300). All match to the printed digits.",
)
ok(
    "M7b-2.3-grades-L04",
    RE + "T rows Prop 1.2, 1.3, 1.4, 2.1, Example 2.2, Example 3.4 (L04.html:62-122, 117-121, 266-268) re-proved from the text; "
    "the C row L04.html:417 names Lab 1. Rows at L04.html:411-416 match the proofs.",
)
ok(
    "M7b-2.3-grades-L05",
    RE + "L05.html:533-538: Lemma 1.3, Proposition 2.1, Theorem 2.3, Theorem 3.1, Proposition 3.4 and Example 3.6 are T and proved on the page (L05.html:70-180, 175-177). The Lab 1 claims are attributed to Lab 1 in the rows.",
)
ok(
    "M7b-2.3-grades-L06",
    RE + "L06.html:548-552: Theorem 1.3, Proposition 2.1, Proposition 2.3, Proposition 3.4 are T with proofs on the page (L06.html:76-78, 92-98, 111-113, 137-141); the closed-form/KKT row (L06.html:552) is C and names Lab 1 Part A (SIMULATED).",
)
bad(
    "M7b-cards-L04-c056-c065",
    RE + "cards.json M7-c056..c065 read against L04.html:55-268 and 254-256. c056-c060, c062-c065 agree with the current text. c061 names the minimiser x* while Proposition 2.1 (L04.html:107) now names it x-hat.",
    "Rename x* to x-hat in M7-c061 (see M7b-r4-cards-xstar).",
)
ok(
    "M7b-cards-L04-c066-c072",
    RE + "cards.json M7-c067..c071 read against L04.html:259-295: c067 (Remark 3.3), c068 (Example 3.4), c069 (L04.html:287), c070 (L04.html:291), c071 (L04.html:295, Remark 1.5 at L04.html:100) agree with the current text. c066 and c072 are absent. Duplicate pairs are in M7b-cards-duplicates.",
)
bad(
    "M7b-cards-L05-c073-c084",
    RE + "cards.json M7-c073..c084 read against L05.html:58-172. c073-c078, c080-c082, c084 agree. c083 repeats the Definition 3.3 sentence 'found from Theorem 2.3 if the restriction of Q to the free components is positive definite', which misstates Theorem 2.3 (see M7b-r3-L05-def33-theorem23-hypothesis). c079 names the minimiser x* while Theorem 2.3 (L05.html:115) names it x-hat.",
    "Correct M7-c083 to the Theorem 2.3 hypothesis (Q symmetric positive definite, rows of A and of G_i for i in S linearly independent) and rename x* to x-hat in M7-c079.",
)
bad(
    "M7b-cards-L05-c085-c096",
    RE + "cards.json M7-c085..c093 read against L05.html:128-180 and 390-496 (c094-c096 are absent). c085, c086 (Example 3.6, but x* where L05.html:176 uses x-bar), c087-c091 agree with the page and the lab output. "
    "c092 says 'Stationarity together with feasibility and that sign certifies optimality', which omits complementary slackness required by Theorem 3.1 (L05.html:141). c093 names the minimiser x*.",
    "Add complementary slackness (mu-bar_i (G x-bar - h)_i = 0) to M7-c092 (see M7b-r4-card-c092-CS); rename x* to x-hat in M7-c093 and x-bar or x-hat consistently in M7-c086 (see M7b-r4-cards-xstar).",
)
bad(
    "M7b-cards-L06-c097-c108",
    RE + "cards.json M7-c097..c108 read against L06.html:58-146. c097 now carries the covariance hypothesis and agrees with Definition 1.1 (fixed). c098-c101, c103-c108 agree (Definitions 1.2, 3.1, 3.2, Theorem 1.3, Remarks 1.4, 3.3, 3.5, Propositions 2.3, 3.4). "
    "c102 calls w'Sigma w 'the variance V(gamma)' without the covariance hypothesis.",
    "Rewrite M7-c102 to say 'the quadratic risk term V(gamma) = w'Sigma w' (see M7b-r4-L06-variance-term).",
)
bad(
    "M7b-cards-L06-c109-c120",
    RE + "cards.json M7-c108..c118 (c108, c109 ... c118; c119 and c120 absent) read against L06.html:404-430, 552. Values verified: diagonal 49/40, 27/20, 103/80, 103/80 (c109); A4 negative at all five gammas (c111); zero set {A4} (c112); 0.5722548 (c113); 0.5588607 and 0.558860 (c114); c115, c116, c117, c118 agree. c110 labels the lab column 'variance'.",
    "Relabel the lab's w'Sigma w column and c110 as the quadratic risk term (see M7b-r4-L06-variance-term).",
)
bad(
    "M7b-cards-duplicates",
    RE + "Full scan of the 63 cards M7-c056..c118 (all read). Pairs with the same locator and same answer still present: c058 (Prop 1.3: 'g <= p*, hence d* <= p*') and c069 (L04.html:287: 'weak duality gives only d* <= p*'); "
    "c059 (Prop 1.4 bound) and c071 (L04.html:295: zero grid gap forces zero true gap by Prop 1.4); c082 (Remark 3.2, multiplier -1) and c092 (L05.html:412-413, Remark 3.2 sign). "
    "No new duplicate found (c079/c083 and c081/c092 differ in locator or claim).",
    "Merge M7-c069 into M7-c058 and M7-c071 into M7-c059, and make M7-c092 test the sign condition of Theorem 3.1 with a different witness or merge it with M7-c082.",
)
ok("M7b-2.9-structure", RE + "Section order in L04, L05, L06: why-it-matters, core sections, lab, where the canon breaks, misconceptions, problem set, key results, quiz, references (check_pages PASS).")
ok("M7b-2.9-banned", RE + "check_pages banned-string scan PASS on all three pages (run in the command row). Remaining ellipses are list or math continuations.")
ok("M7b-2.9-process-words", RE + "grep -in for build, builder, verifier, REQUEST, unit report on L04, L05, L06 -> 0 each. 'round' occurs only as 'unrounded' or 'rounds' (L06.html:504, 511).")
ok("M7b-hours", RE + "data-hours L01 9, L02 9, L03 10, L04 10, L05 10, L06 10, L07 9, L08 10: sum 77 = index.html data-hours-lessons 77; data-hours-project 33; 77 + 33 = 110 = curriculum hours. No arithmetic mismatch (pace not judged, per the architect ruling).")
ok("M7b-L04-prop32", RE + "L04.html:256 'It is the hypothesis of Open item 3.2 in Lesson 3, the necessity statement'; L03.html:134 is the Open item 3.2 remark (Slater's condition is one of its hypotheses). Consistent.")
ok("M7b-L04-lab-numbering", RE + "grep -c 'Lab 2' on L04.html, L05.html, L06.html -> 0 each; 'Lab 1' is the only lab label used in the three pages.")
ok("M7b-L04-quiz-hypotheses", RE + "L04.html:497-503: the correct option 'A KKT point, with differentiable convex f and g_i and affine h_j' matches Proposition 2.1 (L04.html:107); the explanation's 'Slater's condition is not needed' matches the proof (L04.html:110-115).")
ok("M7b-L04-causal", RE + "L04.html:295: 'The implication uses only Propositions 1.3 and 1.4' is true: the argument uses Prop 1.4 (grid gap >= p*-d*) and Prop 1.3 (p*-d* >= 0). Card M7-c071 agrees.")
ok("M7b-L04-term-before-definition", RE + "'Slater' first appears in the body at L04.html:252 (section heading) and is defined at L04.html:255-256; the only earlier use is the meta description at L04.html:7 (head, not learner text). 'dual feasible' is defined at L04.html:59 before Proposition 1.3 (L04.html:76).")
ok("M7b-L05-lemma14", RE + "L05.html:83-89: the chord identity theta f(x) + (1-theta) f(y) - f(z) = (1/2) theta (1-theta) (x-y)'Q(x-y) follows from the quadratic and linear parts (linear part cancels); verified by the expansion; the convexity clause cites L01 Definition 2.1 (L01.html:82-83), unchanged.")
ok("M7b-L05-prop34-step", RE + "L05.html:166: f(x)+f(y) = 2f(z)+u'Qu with u = (x-y)/2 and u'Qu = (1/4)(x-y)'Q(x-y); f(z) = (f(x)+f(y))/2 - (1/8)(x-y)'Q(x-y); strict negativity from Q positive definite and x != y. Verified algebraically.")
ok("M7b-L05-why-xref", RE + "L05.html:52 cites Proposition 3.4 for the midpoint result; Proposition 3.4 is at L05.html:160-166. Consistent.")
ok("M7b-L05-misc3", RE + "L05.html:417: gradient at the minimiser is -A'lambda*, zero exactly when lambda* = 0 because A has full row rank; lambda* = (-36/19, 11/19) printed by Lab 1 (L05.html:372). Consistent.")
ok("M7b-L05-canon-heading", RE + "L05.html:396 heading 'An indefinite Hessian can leave a QP with no minimiser' is qualified by the body (a QP can have no minimiser at all, as Misconception 1 shows), and Misconception 1 (L05.html:409) uses an indefinite Q.")
ok("M7b-L05-lab-variables", RE + "L05.html:390: 'three variables in Part A and two in Part B, examines four candidate sets' matches the twin (Q_A is 3x3, Q_B is 2x2; four masks in part_b).")
ok("M7b-L05-why-scope", RE + "L05.html:52: 'A quadratic program minimises a quadratic objective under linear constraints' is the Definition 1.1 scope (L05.html:59-62).")
ok("M7b-L06-why-scope", RE + "L06.html:52: 'The mean-variance problem of this lesson is a quadratic program' is scoped to the problem of Definition 1.2 (L06.html:64-65), which is a QP with Q = gamma Sigma, c = -mu. The word 'variance' in the same sentence is in M7b-r4-L06-variance-term.")
ok("M7b-L06-partB-count", RE + "L06.html:150, 168-170: '15 sets that leave at least one asset free'. Twin nonnegative_candidates loops over 2^4 masks and skips the all-fixed mask: 15 candidates. Output 'candidates_passing 1' per gamma (1 kept). Consistent.")
ok("M7b-L06-partD-true", RE + "L06.html:431-432 and output lines 401-403: linear_form_feasible True, linear_form_sum_equals_turnover True, feasible_perturbations_at_least_turnover 20 of 20 (checked against the twin run output).")
ok("M7b-L06-misc2", RE + "L06.html:427-428: the four weights at gamma = 1 move from 0.434783, 0.526836, 0.562535, -0.524154 to 0.388425, 0.203679, 0.407895, 0.000000 (all four change; verified by indep_r4.py).")
ok("M7b-L06-covariance-docstring", RE + "grep -n covariance L06.html gives L06.html:56 (disclaimer 'estimating a covariance matrix is outside M7'), :60 and :412 (conditional hypothesis of Definition 1.1 and the canon item). The lab docstring (tests/labs/M7/lab-M7-L06-1.py:1-30) does not use the word covariance and states that Sigma is not estimated.")
ok("M7b-L06-R1-unproved", RE + "L06.html:518-524: the limit w(gamma) -> (1/n)1 follows from P3 (mu/gamma -> 0 and 1'mu/gamma -> 0). The μ = 0 remark gives (1/n)1 as the minimiser of (1/2)w'w under the budget. Verified.")
ok("M7b-L06-term-before-definition", RE + "L06.html:52 says 'a sum of absolute values' and does not use the word turnover before Definition 3.2 (L06.html:124). 'turnover' appears first in the Definition 3.1 forward reference (L06.html:120) to Definition 3.2, which is on the page.")
ok("M7b-L06-lab-claims-ok", RE + "L06.html:404-405 interpretation checked sentence by sentence against the output: budget True at each gamma; A4 negative at each gamma (-0.524154 ... -0.409145); return falls 0.113798 -> 0.106241; zero set {A4}; constrained objective at least the unconstrained (five True lines); turnover 0.558861. The word 'variance' in the same paragraph is in M7b-r4-L06-variance-term.")
ok("M7b-2.4-L04-proofs", RE + "L04.html:67-115 (Prop 1.2 infimum of sum >= sum of infima; Prop 1.3 lambda_i g_i <= 0 and h_j = 0), 93-96 (Prop 1.4), 110-115 (Prop 2.1 with (K1)-(K4) of L03.html:64-67 and Lemma 1.4 and Theorem 2.1 of L03.html:78-113) re-derived; no gap.")
ok("M7b-2.4-L05-proofs", RE + "L05.html:70-180: Lemma 1.3 expansion, Lemma 1.4 (tangent and chord), Prop 2.1 (K nonsingular, Kv=0 argument), Thm 2.3, Remark 2.4 completed square and line, Thm 3.1, Remark 3.2, Prop 3.4 re-derived. Sign conventions consistent with Section 3 (L05.html:130-137).")
ok("M7b-2.4-L06-proofs", RE + "L06.html:68-146: Theorem 1.3 (KKT solve, lambda formula, 1'b = b'Sigma b > 0 from Sigma b = 1), Remark 1.4, Proposition 2.1 (two minimality inequalities; sign of the bounds re-derived), Proposition 2.3, Proposition 3.4 (both directions incl. tau < 0) re-derived.")
ok("M7b-2.4-quiz", RE + "Numeric keys: L04 -0.5 (exact), 2 (exact), -0.6633 with tolerance 5e-5 (-199/300 = -0.66333; diff 3.3e-5); L05 19 (exact), 0.7632 with tolerance 5e-5 (551/722 = 0.763158; diff 4.2e-5), -2.25 (exact), 19 (exact); L06 0.113798, 0.184631, 0.007996 (tolerance 5e-7), 0.2, 0.5125 (exact). Distractors checked against the text.")
ok("M7b-2.5-L04-misc", RE + "L04.html:126, 249, 285-295, 372-374: the grid contains (0, 3/10) and nu = -1/2 (lambda_2 = 3/10 on the 1/10 grid); grid counts 1331, 21, 27951 re-derived.")
ok("M7b-footer-L05-L06", RE + "L05.html:638 and L06.html:657 footers: 'Each lemma, proposition and theorem carries an evidence grade, and this lesson cites no registry source.' L04 footer (L04.html:521) consistent with the T and C rows used.")
bad(
    "M7b-r3-L05-def33-theorem23-hypothesis",
    RE + "Still open. L05.html:156 now reads 'found from Theorem 2.3 if the restriction of Q to the free components is positive definite and the rows used are independent'. "
    "Theorem 2.3 (L05.html:114-115) requires Q symmetric positive definite on R^n and A of full row rank; the restriction of Q is not its hypothesis. "
    "'free components' is not defined in Definition 3.3; it is first defined in the lab docstring (L05.html:195; twin line 195). Card M7-c083 repeats the sentence.",
    "State Theorem 2.3's hypotheses exactly for the S-candidate: Q symmetric positive definite and the rows of A and G_i (i in S) linearly independent. Remove 'the restriction of Q to the free components'. Correct M7-c083.",
)
ok(
    "M7b-r3-L06-def11-variance-identity",
    RE + "Fixed. L06.html:60 now says 'If Sigma is the covariance matrix of the one-period returns, this form is the portfolio variance of the return; the unit takes Sigma as an input and does not check that identity'; card M7-c097 carries the same hypothesis. The later by-name uses of 'variance' are a separate FAIL (M7b-r4-L06-variance-term).",
)
ok("M7b-r3-L01-convexity-definition", RE + "L01.html:80-83 (Definition 2.1) defines a convex function on a convex set S by the chord inequality, as cited by L05.html:84. Unchanged on this pin.")
ok("M7b-r3-L05-remark24-decomposition", RE + "Remark 2.4: (2x1 + x2/2)^2 + (11/4)(x2 + 4x3/11)^2 + (18/11)x3^2 expanded equals 4x1^2 + 3x2^2 + 2x3^2 + 2x1x2 + 2x2x3 (indep_r4.py sample identity True); Av = 0 for v = (-2,1,1); Qv = (-7,2,3), v'Qv = 19.")
ok("M7b-r3-L06-prop34-no-sign", RE + "L06.html:134-141: the proof works for any real tau. If tau < 0, the turnover inequality fails (LHS >= 0) and no t exists (sum t >= 0), so the equivalence holds.")
ok("M7b-r3-L06-def31-scope", RE + "L06.html:120: 'Section 2 and Part B of Lab 1 use the budget and nonnegativity constraints. The sector constraint is defined here and not used on this page.' grep for 'sector' and 'box' on L06 finds them only in L06.html:120, so the statement is consistent.")
ok("M7b-r3-lab-hypothesis-vs-output", RE + "L04.html:126 predictions (1331, 21, 27951, one grid point at -1/2, grid gap 0, -199/300, KKT True) match L04.html:239-248; L05.html:183 predictions (17 values of t, one passing set, 33x33 grid) match L05.html:367-389; L04 and L05 docstrings match the code.")
ok("M7b-r3-notation", RE + "No registered symbol changed meaning. L04 uses the registered \\R macro; L05 uses \\mathbb{R} five times and L06 twice (raw KaTeX for the same set, \\R maps to \\mathbb{R} in notation.json). The hat notation x-hat is not registered and is local to L04-L05 (defined in each statement).")
bad(
    "M7b-r4-L06-variance-term",
    RE + "Definition 1.1 (L06.html:60) says w'Sigma w is 'the portfolio variance of the return' only if Sigma is the covariance matrix, and the unit does not check that identity. "
    "The page then calls w'Sigma w 'variance' by name: L06.html:52 ('a quadratic penalty on variance'), 90 (Proposition 2.1 title 'variance falls and return falls as gamma rises'), 150 (Part C 'the variance falls'), 405 ('the variance column'), 424 ('the variance term'), 549 (Key results 'variance does not rise'), 586 (quiz 'the variance w'Sigma w'); lab output header (L06.html:313); cards M7-c102 and M7-c110. "
    "plans/M7-build-plan.md section 2 lists 'variance' as an M4 concept outside the closure (T3: prose use is read by the verifier). Proposition 2.1 itself (L06.html:91) is stated for V(gamma) = w'Sigma w and its T grade is unaffected; the title and the summary row overstate it.",
    "Use 'the quadratic risk term w'Sigma w' (or V) in these places, keep the word variance only in the Definition 1.1 hypothesis sentence, rename the Proposition 2.1 title to '(the risk term and the return fall as gamma rises)', relabel the lab header and column, and align cards M7-c102 and M7-c110.",
)
bad(
    "M7b-r4-card-c092-CS",
    RE + "cards.json M7-c092 back: 'Stationarity together with feasibility and that sign certifies optimality; stationarity alone does not.' Theorem 3.1 (L05.html:141) also requires complementary slackness mu-bar_i (G x-bar - h)_i = 0 for every i, and the proof (L05.html:146) uses it. The card drops a hypothesis of the theorem it cites.",
    "Rewrite M7-c092 to list stationarity, feasibility, mu-bar >= 0 and complementary slackness.",
)
bad(
    "M7b-r4-L05-E3-PD",
    RE + "L05.html:496 (E3 solution): 'The positive definiteness of Q is proved directly in Remark 2.4, not by the printed line.' The lab prints 'q_positive_definite True' (L05.html:369), computed by leading principal minors (twin lines 255-261; minors 4, 11, 18 by indep_r4.py), an exact Sylvester test that does establish positive definiteness for this Q. The sentence misstates what the printed line establishes.",
    "Say that the printed line is an exact leading-minor test for this Q, and that Remark 2.4 gives a completed-square proof that does not depend on the lab.",
)
bad(
    "M7b-r4-L05-references-one-instance",
    RE + "L05.html:627: 'Lab 1 checks one instance in exact arithmetic.' Lab 1 has two instances: Part A (Q_A 3x3, c_A, A 2x3, b; twin lines 207-218) and Part B (Q_B 2x2, c_B; twin lines 220-221). L05.html:183 and 390 say so.",
    "Replace 'checks one instance' with 'checks two small instances in exact arithmetic (Part A, three variables; Part B, two variables)'.",
)
bad(
    "M7b-r4-cards-xstar",
    RE + "Notation mismatch between cards and current lesson text: cards.json M7-c061 names the KKT minimiser x* (lesson: x-hat at L04.html:107), M7-c079 names x* (lesson: x-hat at L05.html:115), M7-c086 names x* (lesson: x-bar at L05.html:176 and x-hat at L05.html:390, 538), M7-c093 names x* (lesson: x-hat at L05.html:417).",
    "Rename the minimiser in cards M7-c061, M7-c079, M7-c093 to x-hat and in M7-c086 to x-bar (or x-hat) so each card matches the lesson it cites.",
)

r3 = json.loads(R3.read_text(encoding="utf-8"))
ids = [r["id"] for r in r3["rows"]]
rows = []
for r in r3["rows"]:
    i = r["id"]
    status, evidence, fix = P[i]
    row = {"id": i, "check": r["check"], "location": r["location"], "status": status, "evidence": evidence}
    if status != "PASS":
        row["fix"] = fix
    rows.append(row)

new_ids = [
    "M7b-r4-L06-variance-term",
    "M7b-r4-card-c092-CS",
    "M7b-r4-L05-E3-PD",
    "M7b-r4-L05-references-one-instance",
    "M7b-r4-cards-xstar",
]
for i in new_ids:
    status, evidence, fix = P[i]
    loc = {
        "M7b-r4-L06-variance-term": "course/modules/M/M7/L06.html:52, 90, 150, 405, 424, 549, 586, 313; course/modules/M/M7/cards.json M7-c102, M7-c110",
        "M7b-r4-card-c092-CS": "course/modules/M/M7/cards.json M7-c092; course/modules/M/M7/L05.html:141",
        "M7b-r4-L05-E3-PD": "course/modules/M/M7/L05.html:496, 369; tests/labs/M7/lab-M7-L05-1.py:255-261",
        "M7b-r4-L05-references-one-instance": "course/modules/M/M7/L05.html:627; tests/labs/M7/lab-M7-L05-1.py:207-221",
        "M7b-r4-cards-xstar": "course/modules/M/M7/cards.json M7-c061, M7-c079, M7-c086, M7-c093",
    }[i]
    rows.append(
        {
            "id": i,
            "check": "round 4 new row: " + i.replace("M7b-r4-", "").replace("-", " "),
            "location": loc,
            "status": status,
            "evidence": evidence,
            "fix": fix,
        }
    )

counts = {"PASS": 0, "FAIL": 0, "UNVERIFIABLE": 0}
for r in rows:
    counts[r["status"]] += 1
fail_ids = [r["id"] for r in rows if r["status"] != "PASS"]

fragment = {
    "unit": "M7",
    "slice": "M7-b",
    "round": 4,
    "verifier": "round-4 independent verifier for slice M7-b (L04 to L06 and their lab twins); did not build M7 and shares no context with its builders",
    "pin": "2657ab5",
    "base": "aa3c26c",
    "checkout": "/tmp/verifyB4-M7-b (detached worktree at 2657ab5; .venv symlink)",
    "scratch": "/tmp/M7-v/b4",
    "verified_at": datetime.datetime.now(datetime.UTC).replace(microsecond=0).isoformat(),
    "verdict": "FAIL",
    "registry_flags": [],
    "freshness_flags": [],
    "rows": rows,
    "mutants": [],
    "notes": (
        "Delta from aa3c26c: L04.html (Remark 1.5, Prop 2.1, P3 notation), L05.html (Def 3.3, Thm 2.3 wording, Remark 2.4 notation, E3/quiz/references lines), "
        "L06.html (Def 1.1, Def 3.1, Lab 1 hypothesis and interpretation, notation), cards.json (M7-c069, c071, c083, c092, c097 and the L01-L02/L08 cards outside this slice), "
        "twins tests/labs/M7/lab-M7-L04-1.py, lab-M7-L05-1.py, lab-M7-L06-1.py byte-identical to aa3c26c. "
        "All slice rows re-verified on 2657ab5 (commands re-run; numbers recomputed in ledgers/M7/scripts/M7-b-r4/indep_r4.py). "
        "Project slice mutants are not part of this slice (lesson slice); the mutant run is not applicable here. "
        "Not checked: any web access (no SEC/Crossref live call needed: the slice cites no key). Not checked: pace of hours (architect ruling). "
        "Scope of this slice is lessons and twins only; project.html and grader are other slices."
    ),
    "summary": {
        "rows": len(rows),
        "pass": counts["PASS"],
        "fail": counts["FAIL"],
        "unverifiable": counts["UNVERIFIABLE"],
        "fail_ids": fail_ids,
    },
}

out = ROOT / "ledgers" / "M7" / "M7-b.json"
out.write_text(json.dumps(fragment, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("wrote", out, counts, "round3 ids kept:", all(i in [r["id"] for r in rows] for i in ids))
